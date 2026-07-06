from __future__ import annotations

import time
from dataclasses import asdict, is_dataclass
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from tqdm import tqdm

from filinglens.embeddings.embedder import get_embedding_service
from filinglens.models import (
    DocumentChunk,
    SearchResult,
)
from filinglens.settings import (
    QDRANT_COLLECTION,
    QDRANT_URL,
)
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


class QdrantVectorStore:
    """Qdrant wrapper for dense retrieval."""

    def __init__(
        self,
        *,
        collection_name: str = QDRANT_COLLECTION,
        url: str = QDRANT_URL,
        client: Any | None = None,
        models_module: Any | None = None,
        vector_size: int | None = None,
    ) -> None:

        self.collection_name = collection_name
        self.vector_size = vector_size

        if self.vector_size is None:
            embedder = get_embedding_service()
            self.vector_size = embedder.embedding_dimension

        self.client = client or self._create_client(url)
        self.models = models_module

    # --------------------------------------------------

    def create_collection(
        self,
        *,
        recreate: bool = False,
    ) -> None:

        if recreate and self.collection_exists():
            self.delete_collection()

        if self.collection_exists():
            logger.info(
                "Collection '%s' already exists.",
                self.collection_name,
            )
            return

        models = self._models()

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=self.vector_size,
                distance=models.Distance.COSINE,
            ),
        )

        logger.info(
            "Created collection '%s'.",
            self.collection_name,
        )

    # --------------------------------------------------

    def delete_collection(self) -> None:

        if self.collection_exists():
            self.client.delete_collection(
                collection_name=self.collection_name,
            )

            logger.info(
                "Deleted collection '%s'.",
                self.collection_name,
            )

    # --------------------------------------------------

    def collection_exists(self) -> bool:

        if hasattr(self.client, "collection_exists"):
            return bool(self.client.collection_exists(self.collection_name))

        collections = self.client.get_collections().collections

        return any(c.name == self.collection_name for c in collections)

    # --------------------------------------------------

    def upload_chunks(
        self,
        chunks: list[DocumentChunk | dict],
        embeddings,
        *,
        batch_size: int = 64,
    ) -> None:

        if len(chunks) != len(embeddings):
            raise ValueError("chunks and embeddings length mismatch.")

        if batch_size <= 0:
            raise ValueError("batch_size must be positive")

        models = self._models()

        logger.info(
            "Uploading %d chunks...",
            len(chunks),
        )

        for start in tqdm(
            range(0, len(chunks), batch_size),
            desc="Uploading",
        ):
            batch_chunks = chunks[start : start + batch_size]

            batch_embeddings = embeddings[start : start + batch_size]

            points = []

            for chunk, vector in zip(
                batch_chunks,
                batch_embeddings,
                strict=True,
            ):
                vector = self._vector_to_list(vector)

                if len(vector) != self.vector_size:
                    raise ValueError(
                        f"Expected vector length {self.vector_size}, got {len(vector)}"
                    )

                points.append(
                    models.PointStruct(
                        id=self._point_id(chunk),
                        vector=vector,
                        payload=self._payload(chunk),
                    )
                )

            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
                wait=True,
            )

        logger.info("Upload complete.")

    # --------------------------------------------------

    def search(
        self,
        query_vector,
        *,
        top_k: int = 5,
        filters: dict | None = None,
    ) -> list[SearchResult]:

        models = self._models()

        query_filter = None

        if filters:
            query_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key=k,
                        match=models.MatchValue(value=v),
                    )
                    for k, v in filters.items()
                ]
            )

        start = time.perf_counter()

        vector = self._vector_to_list(query_vector)

        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=query_filter,
            limit=top_k,
            with_payload=True,
        )

        elapsed = (time.perf_counter() - start) * 1000

        logger.info(
            "Search completed in %.2f ms.",
            elapsed,
        )

        results = []

        for hit in hits:
            payload = dict(hit.payload)

            chunk = DocumentChunk(
                id=payload.pop("chunk_id"),
                company=payload["company"],
                year=payload["year"],
                page=payload["page"],
                chunk=payload["chunk"],
                text=payload["text"],
            )

            results.append(
                SearchResult(
                    chunk=chunk,
                    score=float(hit.score),
                )
            )

        return results

    # --------------------------------------------------

    def collection_stats(self):

        collection = self.client.get_collection(collection_name=self.collection_name)

        return {
            "collection": self.collection_name,
            "points": collection.points_count,
            "vectors": collection.vectors_count,
            "status": str(collection.status),
        }

    # --------------------------------------------------

    def _models(self):

        if self.models is not None:
            return self.models

        from qdrant_client import models

        self.models = models

        return models

    # --------------------------------------------------

    @staticmethod
    def _create_client(url):

        from qdrant_client import QdrantClient

        return QdrantClient(url=url)

    # --------------------------------------------------

    @staticmethod
    def _payload(
        chunk: DocumentChunk | dict,
    ):

        if is_dataclass(chunk):
            payload = asdict(chunk)
        else:
            payload = dict(chunk)

        payload["chunk_id"] = payload.pop("id")

        return payload

    # --------------------------------------------------

    @classmethod
    def _point_id(cls, chunk):

        chunk_id = chunk.id if isinstance(chunk, DocumentChunk) else chunk["id"]

        return str(
            uuid5(
                NAMESPACE_URL,
                chunk_id,
            )
        )

    # --------------------------------------------------

    @staticmethod
    def _vector_to_list(vector):

        if hasattr(vector, "tolist"):
            vector = vector.tolist()

        if vector and isinstance(vector[0], list):
            vector = vector[0]

        return [float(v) for v in vector]
