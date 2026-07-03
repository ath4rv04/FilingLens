from dataclasses import dataclass


@dataclass(slots=True)
class DocumentChunk:

    id: str
    company: str
    year: str
    page: int
    chunk: int
    text: str