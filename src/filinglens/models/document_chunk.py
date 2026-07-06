from dataclasses import dataclass


@dataclass(slots=True)
class DocumentChunk:
    """Represents one chunk extracted from a filing."""

    id: str

    company: str

    year: str

    page: int

    chunk: int

    text: str

    @property
    def citation(self) -> str:
        return f"{self.company} {self.year} (Page {self.page}, Chunk {self.chunk})"
