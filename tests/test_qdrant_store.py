from types import SimpleNamespace

import pytest

from filinglens.models.document_chunk import DocumentChunk
from filinglens.vectorstore import QdrantVectorStore


class FakeDistance:
    COSINE = "Cosine"


class FakeVectorParams:
    def __init__(self, size, distance):
        self.size = size
        self.distance = distance


class FakePointStruct:
    def __init__(self, id, vector, payload):
        self.id = id
        self.vector = vector
        self.payload = payload


class FakeModels:
    Distance = FakeDistance
    VectorParams = FakeVectorParams
    PointStruct = FakePointStruct


class FakeQdrantClient:
    def __init__(self):
        self.collections = set()
        self.points = []
        self.deleted = []

    def collection_exists(self, collection_name):
        return collection_name in self.collections

    def create_collection(self, collection_name, vectors_config):
        self.collections.add(collection_name)
        self.vectors_config = vectors_config

    def delete_collection(self, collection_name):
        self.collections.discard(collection_name)
        self.deleted.append(collection_name)

    def upsert(self, collection_name, points, wait):
        self.upsert_collection = collection_name
        self.upsert_wait = wait
        self.points.extend(points)

    def search(
        self, collection_name, query_vector, limit, with_payload, query_filter=None
    ):
        self.search_args = (collection_name, query_vector, limit, with_payload)
        return [
            SimpleNamespace(
                id="point-1",
                score=0.91,
                payload={
                    "chunk_id": "chunk-1",
                    "text": "Revenue grew",
                    "page": 4,
                    "company": "ABC",
                    "year": "FY2024",
                    "chunk": 0,
                },
            )
        ]

    def get_collection(self, collection_name):
        return SimpleNamespace(
            points_count=len(self.points),
            vectors_count=len(self.points),
            status="green",
        )


def make_store(client):
    return QdrantVectorStore(
        collection_name="test_filings",
        vector_size=3,
        client=client,
        models_module=FakeModels,
    )


def test_create_collection_uses_configured_vector_size():
    client = FakeQdrantClient()
    store = make_store(client)

    store.create_collection()

    assert "test_filings" in client.collections
    assert client.vectors_config.size == 3
    assert client.vectors_config.distance == FakeDistance.COSINE


def test_recreate_collection_deletes_existing_collection():
    client = FakeQdrantClient()
    client.collections.add("test_filings")
    store = make_store(client)

    store.create_collection(recreate=True)

    assert client.deleted == ["test_filings"]
    assert "test_filings" in client.collections


def test_upload_chunks_stores_chunk_id_in_payload():
    client = FakeQdrantClient()
    store = make_store(client)
    chunk = DocumentChunk(
        id="TCS_FY2024_page_1_chunk_0",
        company="TCS",
        year="FY2024",
        page=1,
        chunk=0,
        text="Operating margin improved.",
    )

    store.upload_chunks([chunk], [[0.1, 0.2, 0.3]])

    point = client.points[0]
    assert point.vector == [0.1, 0.2, 0.3]
    assert point.payload["chunk_id"] == chunk.id
    assert "id" not in point.payload


def test_upload_chunks_rejects_mismatched_embedding_count():
    store = make_store(FakeQdrantClient())

    with pytest.raises(ValueError, match="mismatch"):
        store.upload_chunks([], [[0.1, 0.2, 0.3]])


def test_upload_chunks_rejects_invalid_batch_size():
    store = make_store(FakeQdrantClient())

    with pytest.raises(ValueError, match="batch_size"):
        store.upload_chunks([], [], batch_size=0)


def test_search_returns_result_objects():
    client = FakeQdrantClient()
    store = make_store(client)

    results = store.search([[0.1, 0.2, 0.3]], top_k=1)

    assert results[0].score == 0.91
    assert results[0].chunk.text == "Revenue grew"
    assert client.search_args == ("test_filings", [0.1, 0.2, 0.3], 1, True)


def test_collection_stats_reports_counts():
    client = FakeQdrantClient()
    store = make_store(client)
    store.upload_chunks(
        [
            {
                "id": "chunk-1",
                "company": "ABC",
                "year": "FY2024",
                "page": 1,
                "chunk": 0,
                "text": "x",
            }
        ],
        [[0.1, 0.2, 0.3]],
    )

    assert store.collection_stats()["points"] == 1
