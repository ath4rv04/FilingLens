import statistics
from pathlib import Path

from filinglens.llm.qa_service import QAService
from filinglens.evaluation.dataset import discover_datasets
from filinglens.evaluation.benchmark import BenchmarkExecutor
from filinglens.evaluation.report import ReportGenerator


class EvaluationRunner:
    def __init__(self, qa_service: QAService, datasets_dir: Path, output_dir: Path):
        self.qa_service = qa_service
        self.datasets_dir = datasets_dir
        self.output_dir = output_dir

    def run(self):
        datasets = discover_datasets(self.datasets_dir)
        executor = BenchmarkExecutor(self.qa_service)

        all_results = []

        for dataset in datasets:
            for question in dataset.questions:
                result = executor.run_question(
                    company=dataset.company, year=dataset.year, question=question
                )
                all_results.append(result)

        if not all_results:
            print("No evaluation questions were run!")
            return

        summary = {
            "avg_recall_at_5": statistics.mean(r["recall_at_5"] for r in all_results),
            "avg_precision_at_5": statistics.mean(
                r["precision_at_5"] for r in all_results
            ),
            "avg_mrr": statistics.mean(r["mrr"] for r in all_results),
            "avg_citation_accuracy": statistics.mean(
                r["citation_accuracy"] for r in all_results
            ),
            "avg_context_coverage": statistics.mean(
                r["context_coverage"] for r in all_results
            ),
            "avg_retrieval_ms": statistics.mean(
                r["retrieval_latency"] for r in all_results
            ),
            "avg_llm_ms": statistics.mean(r["llm_latency"] for r in all_results),
            "avg_total_ms": statistics.mean(r["total_latency"] for r in all_results),
        }

        ReportGenerator(self.output_dir).generate(all_results, summary)
