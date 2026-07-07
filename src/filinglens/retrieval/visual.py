from filinglens.models.retrieval_result import RetrievalResult
from filinglens.visual.visual_store import VisualQdrantStore
from filinglens.visual.embedder import VisualEmbedder
from filinglens.utils.logging import get_logger
from filinglens.retrieval.filtering import build_qdrant_filter

logger = get_logger(__name__)

class VisualRetriever:
    """Retrieves document pages utilizing ColQwen embeddings parsing visual architectures directly natively."""
    def __init__(self):
        self.store = VisualQdrantStore()
        self.embedder = VisualEmbedder()
        
    def retrieve(self, query: str, filters: dict | None = None, top_k: int = 5) -> list[RetrievalResult]:
        logger.info("Executing Visual Multimodal search for: '%s'", query)
        
        query_vector = self.embedder.embed_query(query)
        qdrant_filter = build_qdrant_filter(filters)
        
        points = self.store.search(
            query_vector=query_vector,
            limit=top_k,
            filter_conditions=qdrant_filter
        )
        
        from filinglens.models.document_chunk import DocumentChunk
        results = []
        for pt in points:
            chunk = DocumentChunk(
                id=pt.id,
                chunk_id=pt.id,
                text=f"[Visual Reference] {pt.payload.get('image_path', '')}",
                company=pt.payload.get("company", ""),
                year=str(pt.payload.get("year", "")),
                page=pt.payload.get("page", 0)
            )
            results.append(RetrievalResult(
                chunk=chunk,
                score=pt.score,
                source="visual"
            ))
            
        return results
