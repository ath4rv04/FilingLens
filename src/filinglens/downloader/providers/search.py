import requests
from typing import List
from urllib.parse import urlparse
from filinglens.downloader.sources.base import FilingSource
from filinglens.downloader.models import Filing, DownloadResult
from filinglens.downloader.providers.backends import SearchBackend, DuckDuckGoBackend
from filinglens.downloader.registry import CompanyRegistry
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


from filinglens.downloader.utils.pdf_discovery import PDFDiscovery
from filinglens.downloader.ranking import PDFRanker


class SearchProvider(FilingSource):
    def __init__(self, backend: SearchBackend = None):
        self.backend = backend or DuckDuckGoBackend()

    @property
    def name(self) -> str:
        return "SearchProvider"

    def _generate_queries(self, company: str, year: str) -> List[str]:
        registry = CompanyRegistry()
        try:
            profile = registry.get(company)
            domain = (
                f"site:{urlparse(profile.investor_relations_url).netloc} "
                if profile.investor_relations_url
                else ""
            )
        except Exception:
            domain = ""

        return [
            f"{company} {year} annual report",
            f"{company} {year.replace('FY', '')} annual report",
            f"{company} integrated report",
            f"{company} annual report 2023-24",
            f"{company} investor relations",
            f"{domain}annual report",
            f"{domain}integrated report",
            f'"{company}" pdf annual report',
            f'"{company}" {year} pdf',
        ]

    def _verify_pdf_header(self, url: str) -> bool:
        """Validate cleanly mimicking HEAD / Stream mapping natively skipping payload sizes proactively."""
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
            if (
                r.status_code == 200
                and "application/pdf" in r.headers.get("Content-Type", "").lower()
            ):
                return True

            if (
                r.status_code == 405
                or "application/pdf" not in r.headers.get("Content-Type", "").lower()
            ):
                stream = requests.get(
                    url, headers=headers, timeout=10, allow_redirects=True, stream=True
                )
                if (
                    stream.status_code == 200
                    and "application/pdf"
                    in stream.headers.get("Content-Type", "").lower()
                ):
                    stream.close()
                    return True
        except Exception as e:
            logger.warning(f"Header resolution skipped over {url}: {e}")
        return False

    def list_filings(self, company: str, years: List[str]) -> List[Filing]:
        candidates = []
        for year in years:
            queries = self._generate_queries(company, year)
            found_landing_pages = set()
            pdf_candidates = set()

            # Step 1: Discover Landing Pages
            logger.info(f"Generated {len(queries)} search queries.")
            landing_pages = []
            for query in queries:
                results = self.backend.search(query)
                for res in results:
                    clean = res.url.split("#")[0].strip()
                    if clean not in found_landing_pages:
                        found_landing_pages.add(clean)
                        landing_pages.append(clean)

            logger.info(f"Search produced {len(landing_pages)} landing pages.")

            # Step 2: Extract PDF links across landing pages natively.
            for page in landing_pages:
                pdf_links = PDFDiscovery.discover_pdf_links(page)
                for link in pdf_links:
                    pdf_candidates.add((link, page))

            logger.info(f"Discovered {len(pdf_candidates)} PDF links.")

            # Step 3: Rank Candidates
            mapped_urls = [c[0] for c in pdf_candidates]
            ranked = PDFRanker.rank_candidates(mapped_urls, year, company, top_k=5)
            logger.info(f"Ranked {len(ranked)} candidates.")

            # Step 4: Validate via HTTP Head and emit Filings
            top_candidates = []
            valid_count = 0
            for score, url in ranked:
                # find the original landing page
                landing = next((c[1] for c in pdf_candidates if c[0] == url), "")

                if self._verify_pdf_header(url):
                    valid_count += 1
                    filing = Filing(
                        company=company,
                        year=year,
                        filing_type="Annual Report",
                        source=self.name,
                        url=url,
                        filename="annual_report.pdf",
                    )
                    setattr(filing, "landing_page", landing)
                    top_candidates.append(filing)

            logger.info(f"Validated {valid_count} PDFs. Selected targets.")
            candidates.extend(top_candidates)

        return candidates

    def download(self, filing: Filing) -> DownloadResult:
        # Re-using the logic executed properly across native sources flawlessly retrieving binaries iteratively without repetition.
        # Fallback implemented properly across the specific manager bounds structurally
        import requests

        try:
            res = requests.get(
                filing.url, timeout=30, headers={"User-Agent": "Mozilla/5.0"}
            )
            res.raise_for_status()

            from filinglens.downloader.validator import FilingValidator

            valid, pages, msg = FilingValidator.is_valid_pdf_content(res.content)
            if not valid:
                return DownloadResult(filing, False, None, len(res.content), None, msg)
                
            return DownloadResult(
                filing, True, None, len(res.content), None, None,
                raw_content=res.content, pages=pages
            )
        except Exception as e:
            return DownloadResult(filing, False, None, 0, None, str(e))
