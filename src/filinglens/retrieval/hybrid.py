from __future__ import annotations

from filinglens.retrieval.bm25 import BM25Retriever
from filinglens.retrieval.dense import DenseRetriever
from filinglens.models import RetrievalResult
from filinglens.retrieval.rrf import reciprocal_rank_fusion


from filinglens.retrieval.filtering import normalize_filters
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)

class HybridRetriever:
    """Combines dense semantic retrieval with sparse BM25 retrieval."""

    def __init__(
        self,
        *,
        dense_retriever: DenseRetriever,
        bm25_retriever: BM25Retriever,
        fusion_k: int = 60,
    ) -> None:
        self.dense_retriever = dense_retriever
        self.bm25_retriever = bm25_retriever
        self.fusion_k = fusion_k

    def search(
        self,
        query: str,
        *,
        top_k: int = 5,
        candidate_k: int | None = None,
        filters: dict | None = None,
    ) -> list[RetrievalResult]:
        filters = normalize_filters(filters)
        logger.info("Hybrid Search | Query: '%s' | Filters: %s", query, filters)
        
        candidate_k = candidate_k or max(top_k * 4, top_k)
        
        dense_results = self.dense_retriever.search(
            query, top_k=candidate_k, filters=filters
        )
        bm25_results = self.bm25_retriever.search(
            query, top_k=candidate_k, filters=filters
        )
        
        logger.info("Hybrid Merging: Dense hits=%d, BM25 hits=%d", len(dense_results), len(bm25_results))

        fused = reciprocal_rank_fusion(
            [dense_results, bm25_results],
            top_k=top_k,
            k=self.fusion_k,
        )
        
        if not fused:
            logger.warning("Hybrid Retrieval produced 0 fused results! Both Dense and BM25 missed targets.")
        else:
            logger.info("Hybrid Retrieval succeeded emitting %d ranked results: %s", len(fused), [r.chunk.id for r in fused])
            
        return fused
