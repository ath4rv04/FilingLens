from functools import lru_cache

from sentence_transformers import SentenceTransformer
import torch

from filinglens.settings import EMBEDDING_MODEL
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


class EmbeddingService:
    """Loads and serves the embedding model."""

    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        logger.info("Loading embedding model...")

        self.model = SentenceTransformer(
            EMBEDDING_MODEL,
            device=self.device,
        )

        logger.info(
            "Model loaded on %s",
            self.device,
        )

    def embed(self, texts: str | list[str]):
        if isinstance(texts, str):
            texts = [texts]

        return self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=True,
        )


@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    """Return a cached EmbeddingService instance."""
    return EmbeddingService()
