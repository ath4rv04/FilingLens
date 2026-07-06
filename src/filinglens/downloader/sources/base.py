from abc import ABC, abstractmethod
from typing import List
from filinglens.downloader.models import Filing, DownloadResult


class FilingSource(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Identifier marking the explicit download source correctly."""
        pass

    @abstractmethod
    def list_filings(self, company: str, years: List[str]) -> List[Filing]:
        pass

    @abstractmethod
    def download(self, filing: Filing) -> DownloadResult:
        pass
