from pydantic import BaseModel


class QAQualityMetrics(BaseModel):
    recall_at_k: float
    precision_at_k: float
    mrr: float
    citation_accuracy: float
    context_coverage: float


def compute_recall_at_k(expected: set[int], retrieved: list[int], k: int) -> float:
    if not expected:
        return 1.0
    retrieved_at_k = set(retrieved[:k])
    return len(expected & retrieved_at_k) / len(expected)


def compute_precision_at_k(expected: set[int], retrieved: list[int], k: int) -> float:
    if not retrieved[:k]:
        return 1.0
    retrieved_at_k = set(retrieved[:k])
    return len(expected & retrieved_at_k) / len(retrieved_at_k)


def compute_mrr(expected: set[int], retrieved: list[int]) -> float:
    for i, page in enumerate(retrieved):
        if page in expected:
            return 1.0 / (i + 1)
    return 0.0


def compute_citation_accuracy(
    expected_pages: set[int], llm_output: str, citations: list[int]
) -> float:
    """Evaluate if the generated citations match the expected source bounding."""
    if not expected_pages:
        return 1.0
    if not citations:
        return 0.0
    valid_citations = [c for c in citations if c in expected_pages]
    return len(valid_citations) / len(citations)


def compute_context_coverage(
    expected_pages: set[int], retrieved_context_pages: set[int]
) -> float:
    """Measure if the retrieved context inherently spanned the required source text natively."""
    if not expected_pages:
        return 1.0
    return len(expected_pages & retrieved_context_pages) / len(expected_pages)
