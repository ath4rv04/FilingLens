from __future__ import annotations

import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from filinglens.downloader.models import Filing, DownloadResult
from filinglens.downloader.registry import CompanyRegistry
from filinglens.downloader.sources.base import FilingSource
from filinglens.downloader.validator import FilingValidator
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


class InvestorRelationsSource(FilingSource):
    """Best-effort crawler for Investor Relations websites."""

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/138.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    PDF_PATTERN = re.compile(r"\.pdf($|\?)", re.IGNORECASE)

    KEYWORDS = [
        "annual",
        "annual report",
        "integrated",
        "integrated report",
    ]

    @property
    def name(self) -> str:
        return "Investor Relations"

    # ---------------------------------------------------------

    def list_filings(
        self,
        company: str,
        years: list[str],
    ) -> list[Filing]:

        registry = CompanyRegistry()
        profile = registry.get(company)

        if not profile.investor_relations_url:
            logger.warning(
                "%s has no Investor Relations URL.",
                company,
            )
            return []

        try:

            response = requests.get(
                profile.investor_relations_url,
                headers=self.HEADERS,
                timeout=20,
            )

            response.raise_for_status()

        except requests.RequestException as e:

            logger.warning(
                "Unable to access %s (%s)",
                profile.investor_relations_url,
                e,
            )

            return []

        soup = BeautifulSoup(
            response.text,
            "lxml",
        )

        filings = []

        for year in years:

            links = self._find_candidate_links(
                soup,
                profile.investor_relations_url,
                year,
            )

            for url in links:

                filings.append(
                    Filing(
                        company=company,
                        year=year,
                        filing_type="Annual Report",
                        source=self.name,
                        url=url,
                        filename="annual_report.pdf",
                    )
                )

        logger.info(
            "Discovered %d filing candidates.",
            len(filings),
        )

        return filings

    # ---------------------------------------------------------

    def download(
        self,
        filing: Filing,
    ) -> DownloadResult:

        try:

            response = requests.get(
                filing.url,
                headers=self.HEADERS,
                timeout=30,
            )

            response.raise_for_status()

        except requests.RequestException as e:

            return DownloadResult(
                filing=filing,
                success=False,
                path=None,
                size=0,
                checksum=None,
                error=str(e),
            )

        content = response.content

        valid, pages, message = (
            FilingValidator.is_valid_pdf_content(content)
        )

        if not valid:

            return DownloadResult(
                filing=filing,
                success=False,
                path=None,
                size=len(content),
                checksum=None,
                error=message,
            )

        result = DownloadResult(
            filing=filing,
            success=True,
            path=None,
            size=len(content),
            checksum=None,
            error=None,
        )

        result._raw_content = content
        result._pages = pages

        return result

    # ---------------------------------------------------------

    def _find_candidate_links(
        self,
        soup: BeautifulSoup,
        base_url: str,
        year: str,
    ) -> list[str]:

        candidates = []

        year_tokens = [
            year,
            year.replace("FY", ""),
            year.replace("FY20", ""),
        ]

        for anchor in soup.find_all("a", href=True):

            href = anchor["href"]

            if not self.PDF_PATTERN.search(href):
                continue

            text = anchor.get_text(
                " ",
                strip=True,
            ).lower()

            href_lower = href.lower()

            score = 0

            for keyword in self.KEYWORDS:

                if keyword in text:
                    score += 5

                if keyword in href_lower:
                    score += 5

            for token in year_tokens:

                if token.lower() in text:
                    score += 10

                if token.lower() in href_lower:
                    score += 10

            if score == 0:
                continue

            candidates.append(
                (
                    score,
                    urljoin(base_url, href),
                )
            )

        candidates.sort(
            reverse=True,
            key=lambda item: item[0],
        )

        return [
            url
            for _, url in candidates
        ]