from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from filinglens.tables.models import ExtractedTable


class PdfPlumberTableExtractor:
    """Extracts tabular data from text-native PDFs using pdfplumber."""

    def __init__(self, pdfplumber_module: Any | None = None) -> None:
        self.pdfplumber = pdfplumber_module

    def extract(self, pdf_path: str | Path) -> list[ExtractedTable]:
        pdf_path = Path(pdf_path)
        pdfplumber = self._pdfplumber()
        tables: list[ExtractedTable] = []

        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                for table_index, raw_table in enumerate(page.extract_tables()):
                    rows = self._normalize_rows(raw_table)
                    if not rows:
                        continue

                    tables.append(
                        ExtractedTable(
                            id=f"{pdf_path.stem}_page_{page_number}_table_{table_index}",
                            page=page_number,
                            table_index=table_index,
                            rows=rows,
                        )
                    )

        return tables

    def write_csvs(
        self,
        tables: list[ExtractedTable],
        output_dir: str | Path,
    ) -> list[Path]:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        written_paths: list[Path] = []

        for table in tables:
            output_path = output_dir / f"{table.id}.csv"
            with output_path.open("w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(table.rows)

            written_paths.append(output_path)

        return written_paths

    def _pdfplumber(self) -> Any:
        if self.pdfplumber is not None:
            return self.pdfplumber

        import pdfplumber

        self.pdfplumber = pdfplumber
        return pdfplumber

    @staticmethod
    def _normalize_rows(raw_table: list[list[Any]]) -> list[list[str]]:
        rows: list[list[str]] = []

        for row in raw_table:
            normalized_row = [
                "" if value is None else str(value).strip() for value in row
            ]
            if any(normalized_row):
                rows.append(normalized_row)

        return rows
