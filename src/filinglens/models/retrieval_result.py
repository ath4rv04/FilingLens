from dataclasses import dataclass

from filinglens.models.document_chunk import DocumentChunk


@dataclass(slots=True)
class RetrievalResult:
    """
    Normalized retrieval result used by RAG.

    Supports dense, sparse and hybrid retrieval.
    """

    chunk: DocumentChunk

    score: float

    source: str

    @property
    def id(self) -> str:
        return self.chunk.id

    @property
    def text(self) -> str:
        return self.chunk.text
