from filinglens.retrieval import HybridRetriever, RetrievalResult


class FakeChunk:
    def __init__(self, id):
        self.id = id


class FakeRetriever:
    def __init__(self, source, chunks):
        self.source = source
        self.chunks = chunks

    def search(self, query, top_k):
        self.query = query
        self.top_k = top_k
        return [
            RetrievalResult(
                chunk=FakeChunk(id=chunk_id),
                score=score,
                source=self.source,
            )
            for chunk_id, score in self.chunks
        ]


def test_hybrid_retriever_fuses_dense_and_bm25_results():
    dense = FakeRetriever("dense", [("a", 0.9), ("b", 0.8)])
    bm25 = FakeRetriever("bm25", [("b", 3.0), ("c", 2.0)])
    retriever = HybridRetriever(dense_retriever=dense, bm25_retriever=bm25)

    results = retriever.search("margin expansion", top_k=2, candidate_k=10)

    assert dense.query == "margin expansion"
    assert bm25.query == "margin expansion"
    assert dense.top_k == 10
    assert bm25.top_k == 10
    assert [result.id for result in results] == ["b", "a"]
