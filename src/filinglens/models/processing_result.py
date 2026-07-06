from dataclasses import dataclass


@dataclass(slots=True)
class ProcessingResult:
    """Summary returned after processing a PDF."""

    company: str

    year: str

    page_count: int

    scanned_pages: list[int]

    chunk_count: int

    @property
    def scanned_page_count(self) -> int:
        return len(self.scanned_pages)
