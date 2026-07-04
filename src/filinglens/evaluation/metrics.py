from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(slots=True)
class EvaluationResult:
    faithfulness: float
    context_recall: float
    citation_coverage: float


def evaluate_answer(
    *,
    answer: str,
    expected_terms: list[str],
    context: str,
) -> EvaluationResult:
    answer_tokens = set(_tokens(answer))
    context_tokens = set(_tokens(context))
    expected = {term.lower() for term in expected_terms}

    faithfulness = _ratio(answer_tokens & context_tokens, answer_tokens)
    context_recall = _ratio(expected & answer_tokens, expected)
    citation_coverage = 1.0 if re.search(r"\[\d+\]", answer) else 0.0

    return EvaluationResult(
        faithfulness=faithfulness,
        context_recall=context_recall,
        citation_coverage=citation_coverage,
    )


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def _ratio(numerator: set[str], denominator: set[str]) -> float:
    if not denominator:
        return 0.0
    return len(numerator) / len(denominator)
