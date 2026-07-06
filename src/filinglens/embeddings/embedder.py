from functools import lru_cache

import numpy as np
import torch
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer

from filinglens.settings import (
    EMBEDDING_BATCH_SIZE,
    EMBEDDING_MODEL,
)
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

    @property
    def embedding_dimension(self) -> int:
        """Return the embedding dimension."""
        return self.model.get_embedding_dimension()

    def embed(
        self,
        texts: str | list[str],
        show_progress_bar: bool = False,
    ) -> NDArray[np.float32]:

        if isinstance(texts, str):
            texts = [texts]

        if not texts:
            return np.empty(
                (0, self.embedding_dimension),
                dtype=np.float32,
            )

        embeddings = self.model.encode(
            texts,
            batch_size=EMBEDDING_BATCH_SIZE,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=show_progress_bar,
        )

        return embeddings.astype(np.float32)


@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    """Return a cached EmbeddingService instance."""
    return EmbeddingService()
