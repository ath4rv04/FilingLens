from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TableCell:
    row: int
    column: int
    text: str


@dataclass(slots=True)
class ExtractedTable:
    id: str
    page: int
    table_index: int
    rows: list[list[str]]

    @property
    def cell_count(self) -> int:
        return sum(len(row) for row in self.rows)

    @property
    def cells(self) -> list[TableCell]:
        return [
            TableCell(row=row_index, column=column_index, text=value)
            for row_index, row in enumerate(self.rows)
            for column_index, value in enumerate(row)
        ]
