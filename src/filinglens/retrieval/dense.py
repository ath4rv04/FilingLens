from __future__ import annotations


from filinglens.embeddings.embedder import EmbeddingService
from filinglens.models import RetrievalResult
from filinglens.vectorstore import QdrantVectorStore
from filinglens.embeddings.embedder import (
    get_embedding_service,
)


from filinglens.retrieval.filtering import normalize_filters
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)

class DenseRetriever:
    def __init__(
        self,
        *,
        vector_store: QdrantVectorStore,
        embedder: EmbeddingService | None = None,
    ) -> None:

        self.embedder = embedder or get_embedding_service()
        self.vector_store = vector_store

    def search(
        self, query: str, *, top_k: int = 5, filters: dict | None = None
    ) -> list[RetrievalResult]:
        filters = normalize_filters(filters)
        logger.info("Dense Search initiated | Query: '%s' | Filters: %s | top_k: %d", query, filters, top_k)
        
        query_vector = self.embedder.embed(
            query,
            show_progress_bar=False,
        )[0]
        
        logger.info("Generated embedding of dimension %d", len(query_vector))
        
        results = self.vector_store.search(query_vector, top_k=top_k, filters=filters)
        
        if not results:
            logger.warning("Dense Retrieval dropped all chunks! 0 results matched vector distances or filter expressions.")
        else:
            logger.info("Dense Retrieval returned %d results mapping directly onto Qdrant points.", len(results))

        return [
            RetrievalResult(
                chunk=result.chunk,
                score=result.score,
                source="dense",
            )
            for result in results
        ]
