from dataclasses import dataclass


@dataclass(slots=True)
class ProcessingResult:
    company: str
    year: str

    page_count: int

    scanned_pages: list[int]

    chunk_count: int