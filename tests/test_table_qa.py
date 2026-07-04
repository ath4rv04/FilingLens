import pytest

from filinglens.tables import ExtractedTable, TableQuestionAnswerer, TableRepository


def test_table_question_answerer_returns_matching_rows_with_header():
    table = ExtractedTable(
        id="annual_report_page_12_table_0",
        page=12,
        table_index=0,
        rows=[
            ["Metric", "FY2023", "FY2024"],
            ["Revenue", "90", "100"],
            ["Profit", "10", "15"],
        ],
    )
    answerer = TableQuestionAnswerer([table])

    answers = answerer.answer("FY2024 revenue", top_k=1)

    assert len(answers) == 1
    assert answers[0].page == 12
    assert answers[0].rows == [
        ["Metric", "FY2023", "FY2024"],
        ["Revenue", "90", "100"],
    ]


def test_table_repository_loads_extractor_csv_ids(tmp_path):
    table_path = tmp_path / "annual_report_page_7_table_2.csv"
    table_path.write_text("Metric,FY2024\nRevenue,100\n", encoding="utf-8")

    repository = TableRepository.from_csv_dir(tmp_path)

    assert repository.tables[0].id == "annual_report_page_7_table_2"
    assert repository.tables[0].page == 7
    assert repository.tables[0].table_index == 2


def test_table_repository_rejects_empty_directory(tmp_path):
    with pytest.raises(ValueError, match="No table CSV"):
        TableRepository.from_csv_dir(tmp_path)
