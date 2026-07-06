from typing import Optional
from filinglens.finance.repository import FinanceRepository
from filinglens.finance.normalizer import normalize_metric_name
from filinglens.utils.timer import Timer


class FinanceQA:
    """Bypasses LLMs fetching deterministic responses entirely off analytic metric mappings."""

    def __init__(self, repository: FinanceRepository):
        self.repository = repository

    def answer_metric(
        self, company: str, year: str, query: str
    ) -> tuple[Optional[str], dict]:
        with Timer("finance_qa_metric") as t:
            # Simple heuristic attempting to parse which metric the user specifically wanted
            metric_target = normalize_metric_name(query)

            # Retrieve directly matching explicitly cached targets
            result = self.repository.find(company, year, metric_target)

            output = None
            if result:
                output = f"{company} reported {result.metric} of {result.value} {result.unit} {result.currency} in {year} (Source: {result.source_text} - Page {result.page})."

            metrics = {
                "retrieval_ms": t.elapsed_ms,
                "llm_ms": 0.0,
                "total_ms": t.elapsed_ms,
            }

        return output, metrics
