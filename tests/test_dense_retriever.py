from types import SimpleNamespace

from filinglens.retrieval import DenseRetriever


class FakeEmbedder:
    def embed(self, query, **kwargs):
        self.query = query
        self.kwargs = kwargs
        return [[0.1, 0.2, 0.3]]


class FakeChunk:
    def __init__(self, id):
        self.id = id


class FakeVectorStore:
    def search(self, query_vector, top_k):
        self.query_vector = query_vector
        self.top_k = top_k
        return [SimpleNamespace(score=0.92, chunk=FakeChunk(id="chunk-1"))]


def test_dense_retriever_embeds_query_and_searches_vector_store():
    embedder = FakeEmbedder()
    vector_store = FakeVectorStore()
    retriever = DenseRetriever(embedder=embedder, vector_store=vector_store)

    results = retriever.search("revenue growth", top_k=3)

    assert embedder.query == "revenue growth"
    assert vector_store.query_vector == [0.1, 0.2, 0.3]
    assert vector_store.top_k == 3
    assert results[0].id == "chunk-1"
    assert results[0].source == "dense"
