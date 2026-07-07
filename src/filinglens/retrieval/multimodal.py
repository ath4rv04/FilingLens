from filinglens.models.retrieval_result import RetrievalResult
from filinglens.retrieval.rrf import reciprocal_rank_fusion
from filinglens.retrieval.dense import DenseRetriever
from filinglens.retrieval.bm25 import BM25Retriever
from filinglens.retrieval.visual import VisualRetriever
from filinglens.retrieval.table import TableRetriever
from filinglens.retrieval.layout import LayoutRetriever
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)

class MultimodalRetriever:
    """Orchestrates comprehensive RRF fusion measuring Text, Visual, and Tabular bounds holistically natively."""
    def __init__(self, dense_retriever=None, bm25_retriever=None):
        self.dense = dense_retriever
        self.bm25 = bm25_retriever
        self.visual = VisualRetriever()
        self.table = TableRetriever()
        self.layout = LayoutRetriever()
        
    def retrieve(self, query: str, filters: dict | None = None, top_k: int = 5, intents: list[str] | None = None) -> list[RetrievalResult]:
        logger.info("Executing Multimodal Retrieval merging multi-faceted frameworks gracefully.")
        intents = intents or ["dense", "bm25"]
        all_results = []
        
        if "dense" in intents and self.dense:
            all_results.append(self.dense.retrieve(query, filters, top_k) if hasattr(self.dense, "retrieve") else self.dense.search(query, top_k=top_k, filters=filters))
        if "bm25" in intents and self.bm25:
            all_results.append(self.bm25.retrieve(query, filters, top_k) if hasattr(self.bm25, "retrieve") else self.bm25.search(query, top_k=top_k, filters=filters))
        if "visual" in intents:
            all_results.append(self.visual.retrieve(query, filters, top_k))
        if "table" in intents:
            all_results.append(self.table.retrieve(query, filters, top_k))
        if "layout" in intents:
            comp = filters.get("company", "") if filters else ""
            yr = filters.get("year", "") if filters else ""
            all_results.append(self.layout.retrieve(query, comp, yr, top_k))
            
        return reciprocal_rank_fusion(all_results, top_k=top_k)
