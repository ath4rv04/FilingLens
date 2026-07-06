from filinglens.evaluation.benchmark import BenchmarkExecutor
from filinglens.evaluation.dataset import BenchmarkQuestion


class FakeQA:
    def answer(self, question, company, year, top_k):
        class FakeBlock:
            class FakeCitation:
                page = 117

            citation = FakeCitation()

        class FakeResponse:
            answer = "Revenue grew."

        return (
            FakeResponse(),
            [FakeBlock()],
            {"retrieval_ms": 10, "llm_ms": 50, "total_ms": 60},
        )


def test_benchmark_executor():
    qa = FakeQA()
    ex = BenchmarkExecutor(qa)

    q = BenchmarkQuestion(question="q", expected_answer="ans", expected_pages=[117])

    res = ex.run_question("TCS", "FY2024", q)
    assert res["recall_at_5"] == 1.0
    assert res["citation_accuracy"] == 1.0
    assert res["retrieval_latency"] == 10
