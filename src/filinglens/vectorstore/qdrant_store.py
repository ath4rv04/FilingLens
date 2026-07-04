from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from filinglens.models.document_chunk import DocumentChunk
from filinglens.settings import QDRANT_COLLECTION, QDRANT_URL, VECTOR_DIMENSION


@dataclass(slots=True)
class QdrantSearchResult:
    id: str
    score: float
    payload: dict[str, Any]

    @property
    def text(self) -> str:
        return str(self.payload.get("text", ""))


class QdrantVectorStore:
    """Small Qdrant wrapper for dense filing chunk retrieval."""

    def __init__(
        self,
        *,
        collection_name: str = QDRANT_COLLECTION,
        vector_size: int = VECTOR_DIMENSION,
        url: str = QDRANT_URL,
        client: Any | None = None,
        models_module: Any | None = None,
    ) -> None:
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.client = client or self._create_client(url)
        self.models = models_module

    def create_collection(self, *, recreate: bool = False) -> None:
        if recreate and self.collection_exists():
            self.delete_collection()

        if self.collection_exists():
            return

        models = self._models()
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=self.vector_size,
                distance=models.Distance.COSINE,
            ),
        )

    def delete_collection(self) -> None:
        if self.collection_exists():
            self.client.delete_collection(collection_name=self.collection_name)

    def collection_exists(self) -> bool:
        if hasattr(self.client, "collection_exists"):
            return bool(self.client.collection_exists(self.collection_name))

        collections = self.client.get_collections().collections
        return any(
            collection.name == self.collection_name for collection in collections
        )

    def upload_chunks(
        self,
        chunks: list[DocumentChunk | dict[str, Any]],
        embeddings: Any,
        *,
        batch_size: int = 64,
    ) -> None:
        if batch_size < 1:
            raise ValueError("batch_size must be at least 1")

        if len(chunks) != len(embeddings):
            raise ValueError("chunks and embeddings must have the same length")

        models = self._models()

        for start in range(0, len(chunks), batch_size):
            batch_chunks = chunks[start : start + batch_size]
            batch_embeddings = embeddings[start : start + batch_size]

            points = [
                models.PointStruct(
                    id=self._point_id(chunk),
                    vector=self._vector_to_list(vector),
                    payload=self._payload(chunk),
                )
                for chunk, vector in zip(batch_chunks, batch_embeddings, strict=True)
            ]

            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
                wait=True,
            )

    def search(self, query_vector: Any, *, top_k: int = 5) -> list[QdrantSearchResult]:
        vector = self._vector_to_list(query_vector)

        if hasattr(self.client, "search"):
            hits = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=top_k,
                with_payload=True,
            )
        else:
            response = self.client.query_points(
                collection_name=self.collection_name,
                query=vector,
                limit=top_k,
                with_payload=True,
            )
            hits = response.points

        return [
            QdrantSearchResult(
                id=str(hit.id),
                score=float(hit.score),
                payload=dict(hit.payload or {}),
            )
            for hit in hits
        ]

    def collection_stats(self) -> dict[str, Any]:
        collection = self.client.get_collection(collection_name=self.collection_name)
        stats: dict[str, Any] = {"collection_name": self.collection_name}

        points_count = getattr(collection, "points_count", None)
        if points_count is not None:
            stats["points_count"] = points_count

        vectors_count = getattr(collection, "vectors_count", None)
        if vectors_count is not None:
            stats["vectors_count"] = vectors_count

        status = getattr(collection, "status", None)
        if status is not None:
            stats["status"] = str(status)

        return stats

    def _models(self) -> Any:
        if self.models is not None:
            return self.models

        from qdrant_client import models

        self.models = models
        return models

    @staticmethod
    def _create_client(url: str) -> Any:
        from qdrant_client import QdrantClient

        return QdrantClient(url=url)

    @staticmethod
    def _payload(chunk: DocumentChunk | dict[str, Any]) -> dict[str, Any]:
        if is_dataclass(chunk):
            payload = asdict(chunk)
        else:
            payload = dict(chunk)

        payload["chunk_id"] = payload.pop("id")
        return payload

    @classmethod
    def _point_id(cls, chunk: DocumentChunk | dict[str, Any]) -> str:
        chunk_id = chunk.id if isinstance(chunk, DocumentChunk) else str(chunk["id"])
        return str(uuid5(NAMESPACE_URL, chunk_id))

    @staticmethod
    def _vector_to_list(vector: Any) -> list[float]:
        if hasattr(vector, "tolist"):
            vector = vector.tolist()

        if vector and isinstance(vector[0], list):
            vector = vector[0]

        return [float(value) for value in vector]
