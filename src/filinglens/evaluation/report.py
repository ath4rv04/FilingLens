import json
from pathlib import Path
from datetime import datetime


class ReportGenerator:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, results: list[dict], global_metrics: dict) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d")

        report_data = {
            "summary": global_metrics,
            "queries_executed": len(results),
            "results": results,
        }

        out_path = self.output_dir / f"evaluation_{timestamp}.json"

        with out_path.open("w") as f:
            json.dump(report_data, f, indent=4)

        print("\n" + "=" * 40)
        print("Benchmark Results")
        print("=" * 40)
        print(f"Questions: {len(results)}\n")
        print(f"Recall@5: {global_metrics.get('avg_recall_at_5', 0):.2f}")
        print(f"Precision@5: {global_metrics.get('avg_precision_at_5', 0):.2f}")
        print(f"MRR: {global_metrics.get('avg_mrr', 0):.2f}")
        print(
            f"Citation Accuracy: {global_metrics.get('avg_citation_accuracy', 0):.2f}"
        )
        print(
            f"Context Coverage: {global_metrics.get('avg_context_coverage', 0):.2f}\n"
        )
        print(
            f"Average Retrieval Latency: {global_metrics.get('avg_retrieval_ms', 0):.2f} ms"
        )
        print(
            f"Average LLM Latency: {global_metrics.get('avg_llm_ms', 0) / 1000.0:.2f} s"
        )
        print(
            f"Average Total Latency: {global_metrics.get('avg_total_ms', 0) / 1000.0:.2f} s"
        )
        print("=" * 40)
        print(f"Saved artifacts to {out_path}")
