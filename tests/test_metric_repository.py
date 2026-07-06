from filinglens.finance.repository import FinanceRepository
from filinglens.finance.models import FinancialMetric


def test_repository_saves_and_retrieves_accurately(tmp_path):
    db_file = tmp_path / "test.db"
    repo = FinanceRepository(db_path=db_file)

    metric = FinancialMetric(
        company="Info",
        year="2024",
        statement="",
        metric="Revenue",
        value=100.0,
        unit="mn",
        currency="USD",
        page=1,
        source_text="",
    )

    repo.save(metric)

    fetched = repo.find("Info", "2024", "Revenue")
    assert fetched.value == 100.0


def test_repository_lists_metrics(tmp_path):
    db_file = tmp_path / "test.db"
    repo = FinanceRepository(db_path=db_file)

    repo.save_many(
        [
            FinancialMetric("A", "Y", "", "M1", 1, "", "", 1, ""),
            FinancialMetric("A", "Y", "", "M2", 2, "", "", 1, ""),
        ]
    )

    assert len(repo.list_metrics("A", "Y")) == 2
