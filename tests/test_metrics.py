from filinglens.evaluation.metrics import (
    compute_recall_at_k,
    compute_precision_at_k,
    compute_mrr,
    compute_citation_accuracy,
    compute_context_coverage,
)


def test_recall():
    assert compute_recall_at_k({1, 2}, [1, 3, 4], 5) == 0.5
    assert compute_recall_at_k(set(), [1, 2], 5) == 1.0


def test_precision():
    assert compute_precision_at_k({1, 2}, [1, 3], 2) == 0.5
    assert compute_precision_at_k({1}, [], 2) == 1.0


def test_mrr():
    assert compute_mrr({3}, [1, 2, 3]) == 1.0 / 3.0
    assert compute_mrr({5}, [1, 2]) == 0.0


def test_citation():
    assert compute_citation_accuracy({1, 2}, "output", [1, 3]) == 0.5


def test_coverage():
    assert compute_context_coverage({1, 2}, {1, 3}) == 0.5
