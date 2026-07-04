from __future__ import annotations

from filinglens.retrieval.models import RetrievalResult


def reciprocal_rank_fusion(
    result_sets: list[list[RetrievalResult]],
    *,
    top_k: int = 5,
    k: int = 60,
) -> list[RetrievalResult]:
    """Fuse ranked retrieval outputs with reciprocal rank fusion."""

    fused_scores: dict[str, float] = {}
    best_results: dict[str, RetrievalResult] = {}
    sources: dict[str, set[str]] = {}

    for results in result_sets:
        for rank, result in enumerate(results, start=1):
            chunk_id = result.chunk_id
            fused_scores[chunk_id] = fused_scores.get(chunk_id, 0.0) + 1 / (k + rank)
            sources.setdefault(chunk_id, set()).add(result.source)

            current = best_results.get(chunk_id)
            if current is None or result.score > current.score:
                best_results[chunk_id] = result

    ranked_ids = sorted(fused_scores, key=fused_scores.get, reverse=True)
    fused_results: list[RetrievalResult] = []

    for chunk_id in ranked_ids[:top_k]:
        result = best_results[chunk_id]
        payload = dict(result.payload)
        payload["retrieval_sources"] = sorted(sources[chunk_id])
        fused_results.append(
            RetrievalResult(
                id=result.id,
                score=fused_scores[chunk_id],
                payload=payload,
                source="hybrid",
            )
        )

    return fused_results
