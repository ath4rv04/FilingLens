from dataclasses import dataclass

from filinglens.models.document_chunk import DocumentChunk


@dataclass(slots=True)
class SearchResult:
    """
    Dense vector search result.

    Returned directly by Qdrant.
    """

    chunk: DocumentChunk

    score: float
