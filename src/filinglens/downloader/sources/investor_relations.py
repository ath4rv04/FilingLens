from __future__ import annotations


from filinglens.downloader.models import Filing, DownloadResult
from filinglens.downloader.registry import CompanyRegistry
from filinglens.downloader.sources.base import FilingSource
from filinglens.downloader.validator import FilingValidator
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


from filinglens.downloader.utils.pdf_discovery import PDFDiscovery
from filinglens.downloader.ranking import PDFRanker


class InvestorRelationsSource(FilingSource):
    """Best-effort crawler for Investor Relations websites."""

    @property
    def name(self) -> str:
        return "Investor Relations"

    def list_filings(self, company: str, years: list[str]) -> list[Filing]:
        registry = CompanyRegistry()
        try:
            profile = registry.get(company)
        except Exception:
            return []

        if not profile.investor_relations_url:
            logger.warning("%s has no Investor Relations URL.", company)
            return []

        candidates = []
        raw_links = PDFDiscovery.discover_pdf_links(profile.investor_relations_url)

        for year in years:
            ranked = PDFRanker.rank_candidates(raw_links, year, company, top_k=5)
            for _, url in ranked:
                candidates.append(
                    Filing(
                        company=company,
                        year=year,
                        filing_type="Annual Report",
                        source=self.name,
                        url=url,
                        filename="annual_report.pdf",
                    )
                )

        logger.info("IR Source Discovered %d filing candidates.", len(candidates))
        return candidates

    def download(self, filing: Filing) -> DownloadResult:
        try:
            import requests

            response = requests.get(
                filing.url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30
            )
            response.raise_for_status()
        except Exception as e:
            return DownloadResult(
                filing=filing,
                success=False,
                path=None,
                size=0,
                checksum=None,
                error=str(e),
            )

        content = response.content
        valid, pages, message = FilingValidator.is_valid_pdf_content(content)

        if not valid:
            return DownloadResult(filing=filing, success=False, path=None, size=len(content), checksum=None, error=message)

        return DownloadResult(
            filing=filing, success=True, path=None, size=len(content), 
            checksum=None, error=None, raw_content=content, pages=pages
        )
