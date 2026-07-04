from filinglens.tables import PdfPlumberTableExtractor


class FakePage:
    def __init__(self, tables):
        self.tables = tables

    def extract_tables(self):
        return self.tables


class FakePdf:
    def __init__(self, pages):
        self.pages = pages

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False


class FakePdfPlumber:
    def __init__(self, pages):
        self.pages = pages

    def open(self, pdf_path):
        self.pdf_path = pdf_path
        return FakePdf(self.pages)


def test_pdfplumber_table_extractor_normalizes_tables(tmp_path):
    fake_pdfplumber = FakePdfPlumber(
        [
            FakePage(
                [
                    [
                        ["Metric", "FY2024"],
                        ["Revenue", "100"],
                        [None, None],
                    ]
                ]
            )
        ]
    )
    extractor = PdfPlumberTableExtractor(pdfplumber_module=fake_pdfplumber)

    tables = extractor.extract(tmp_path / "annual_report.pdf")

    assert len(tables) == 1
    assert tables[0].id == "annual_report_page_1_table_0"
    assert tables[0].rows == [["Metric", "FY2024"], ["Revenue", "100"]]
    assert tables[0].cell_count == 4
    assert tables[0].cells[2].text == "Revenue"


def test_pdfplumber_table_extractor_writes_csvs(tmp_path):
    fake_pdfplumber = FakePdfPlumber(
        [FakePage([[[("Metric"), "FY2024"], ["Revenue", "100"]]])]
    )
    extractor = PdfPlumberTableExtractor(pdfplumber_module=fake_pdfplumber)
    tables = extractor.extract(tmp_path / "annual_report.pdf")

    written_paths = extractor.write_csvs(tables, tmp_path / "tables")

    assert len(written_paths) == 1
    assert written_paths[0].read_text(encoding="utf-8").splitlines() == [
        "Metric,FY2024",
        "Revenue,100",
    ]
