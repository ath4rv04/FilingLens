from typing import List
from filinglens.downloader.sources.base import FilingSource
from filinglens.downloader.models import Filing, DownloadResult


class MCASource(FilingSource):
    @property
    def name(self) -> str:
        return "MCA"

    def list_filings(self, company: str, years: List[str]) -> List[Filing]:
        return []

    def download(self, filing: Filing) -> DownloadResult:
        return DownloadResult(filing, False, None, 0, None, "Not Implemented")
