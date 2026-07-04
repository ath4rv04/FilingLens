from filinglens.retrieval import RetrievalResult, reciprocal_rank_fusion


def result(chunk_id, score, source):
    return RetrievalResult(
        id=chunk_id,
        score=score,
        payload={"chunk_id": chunk_id, "text": chunk_id},
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

    assert [item.chunk_id for item in fused] == ["b", "a", "c"]
    assert fused[0].source == "hybrid"
    assert fused[0].payload["retrieval_sources"] == ["bm25", "dense"]


def test_reciprocal_rank_fusion_respects_top_k():
    fused = reciprocal_rank_fusion(
        [[result("a", 0.9, "dense"), result("b", 0.8, "dense")]],
        top_k=1,
    )

    assert [item.chunk_id for item in fused] == ["a"]
