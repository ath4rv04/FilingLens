from filinglens.llm.qa_service import QAService
from filinglens.evaluation.dataset import BenchmarkQuestion
from filinglens.evaluation.metrics import (
    compute_recall_at_k,
    compute_precision_at_k,
    compute_mrr,
    compute_citation_accuracy,
    compute_context_coverage,
)


class BenchmarkExecutor:
    def __init__(self, qa_service: QAService, top_k: int = 5):
        self.qa_service = qa_service
        self.top_k = top_k

    def run_question(
        self, company: str, year: str, question: BenchmarkQuestion
    ) -> dict:
        llm_response, context_blocks, metrics = self.qa_service.answer(
            question=question.question,
            company=company,
            year=year,
            top_k=self.top_k,
        )

        retrieved_pages = []
        for block in context_blocks:
            page = block.citation.page
            if page is not None:
                retrieved_pages.append(page)

        expected_set = set(question.expected_pages)

        recall = compute_recall_at_k(expected_set, retrieved_pages, self.top_k)
        precision = compute_precision_at_k(expected_set, retrieved_pages, self.top_k)
        mrr = compute_mrr(expected_set, retrieved_pages)

        context_coverage = compute_context_coverage(expected_set, set(retrieved_pages))

        return {
            "question": question.question,
            "expected_pages": question.expected_pages,
            "retrieved_pages": retrieved_pages,
            "recall_at_5": recall,
            "precision_at_5": precision,
            "mrr": mrr,
            "citation_accuracy": compute_citation_accuracy(
                expected_set, llm_response.answer, retrieved_pages
            ),
            "context_coverage": context_coverage,
            "retrieval_latency": metrics["retrieval_ms"],
            "llm_latency": metrics["llm_ms"],
            "total_latency": metrics["total_ms"],
        }
