from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
import re

from filinglens.tables.models import ExtractedTable

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")
TABLE_ID_PATTERN = re.compile(r"page_(?P<page>\d+)_table_(?P<table>\d+)")


@dataclass(slots=True)
class TableAnswer:
    table_id: str
    page: int | None
    table_index: int | None
    score: float
    rows: list[list[str]]

    def render(self) -> str:
        location = []
        if self.page is not None:
            location.append(f"p. {self.page}")
        if self.table_index is not None:
            location.append(f"table {self.table_index}")

        suffix = f" ({', '.join(location)})" if location else ""
        rows = [" | ".join(row) for row in self.rows]
        return f"{self.table_id}{suffix}\n" + "\n".join(rows)


class TableRepository:
    """Loads extracted filing tables from CSV files."""

    def __init__(self, tables: list[ExtractedTable]) -> None:
        self.tables = tables

    @classmethod
    def from_csv_dir(cls, table_dir: str | Path) -> TableRepository:
        table_dir = Path(table_dir)
        if not table_dir.exists():
            raise FileNotFoundError(f"Table directory not found: {table_dir}")

        tables = [cls._read_csv(path) for path in sorted(table_dir.glob("*.csv"))]
        if not tables:
            raise ValueError(f"No table CSV files found in: {table_dir}")

        return cls(tables)

    @staticmethod
    def _read_csv(path: Path) -> ExtractedTable:
        with path.open(encoding="utf-8", newline="") as file:
            rows = [[cell.strip() for cell in row] for row in csv.reader(file)]

        match = TABLE_ID_PATTERN.search(path.stem)
        page = int(match.group("page")) if match else 0
        table_index = int(match.group("table")) if match else 0

        return ExtractedTable(
            id=path.stem,
            page=page,
            table_index=table_index,
            rows=rows,
        )


class TableQuestionAnswerer:
    """Answers simple metric lookup questions over extracted tables."""

    def __init__(self, tables: list[ExtractedTable]) -> None:
        self.tables = tables

    def answer(self, question: str, *, top_k: int = 3) -> list[TableAnswer]:
        query_tokens = set(self._tokenize(question))
        if not query_tokens:
            return []

        scored_answers = [
            answer
            for table in self.tables
            if (answer := self._score_table(table, query_tokens)) is not None
        ]
        scored_answers.sort(key=lambda answer: answer.score, reverse=True)
        return scored_answers[:top_k]

    def _score_table(
        self,
        table: ExtractedTable,
        query_tokens: set[str],
    ) -> TableAnswer | None:
        matching_rows: list[list[str]] = []
        score = 0.0

        header = table.rows[0] if table.rows else []
        header_tokens = set(self._tokenize(" ".join(header)))

        for row in table.rows:
            row_tokens = set(self._tokenize(" ".join(row)))
            overlap = len(query_tokens & row_tokens)
            if overlap == 0:
                continue

            matching_rows.append(row)
            score += overlap

        if not matching_rows:
            return None

        score += 0.25 * len(query_tokens & header_tokens)
        rows = self._with_header(table.rows, matching_rows)
        return TableAnswer(
            table_id=table.id,
            page=table.page,
            table_index=table.table_index,
            score=score,
            rows=rows,
        )

    @staticmethod
    def _with_header(
        all_rows: list[list[str]],
        matching_rows: list[list[str]],
    ) -> list[list[str]]:
        if not all_rows:
            return matching_rows

        header = all_rows[0]
        if matching_rows and matching_rows[0] == header:
            return matching_rows

        return [header, *matching_rows]

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return TOKEN_PATTERN.findall(text.lower())
