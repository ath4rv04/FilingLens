from filinglens.finance.qa import FinanceQA
from filinglens.finance.models import FinancialMetric


class FakeRepo:
    def find(self, *args):
        if args[2] == "Revenue":
            return FinancialMetric(
                company="TCS",
                year="FY2024",
                statement="",
                metric="Revenue",
                value=100.0,
                unit="cr",
                currency="",
                page=1,
                source_text="Rev was 100",
            )
        return None


def test_finance_qa_orchestration():
    qa = FinanceQA(FakeRepo())

    answer, metrics = qa.answer_metric("TCS", "FY2024", "net sales")
    assert answer is not None
    assert "100.0" in answer
    assert "Revenue" in answer
    assert metrics["retrieval_ms"] >= 0.0
    assert metrics["llm_ms"] == 0.0
