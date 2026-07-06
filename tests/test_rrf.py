from filinglens.retrieval import RetrievalResult, reciprocal_rank_fusion


class FakeChunk:
    def __init__(self, id):
        self.id = id


def result(chunk_id, score, source):
    return RetrievalResult(
        chunk=FakeChunk(id=chunk_id),
        score=score,
        source=source,
    )


def test_reciprocal_rank_fusion_combines_duplicate_chunks():
    fused = reciprocal_rank_fusion(
        [
            [result("a", 0.9, "dense"), result("b", 0.8, "dense")],
            [result("b", 7.0, "bm25"), result("c", 6.0, "bm25")],
        ],
        top_k=3,
        k=60,
    )

    assert [item.id for item in fused] == ["b", "a", "c"]
    assert fused[0].source == "hybrid"


def test_reciprocal_rank_fusion_respects_top_k():
    fused = reciprocal_rank_fusion(
        [[result("a", 0.9, "dense"), result("b", 0.8, "dense")]],
        top_k=1,
    )

    assert [item.id for item in fused] == ["a"]
