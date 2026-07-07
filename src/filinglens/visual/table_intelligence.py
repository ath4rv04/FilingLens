from dataclasses import dataclass

@dataclass(slots=True)
class TableCell:
    content: str
    row_span: int = 1
    col_span: int = 1
    is_header: bool = False
    bbox: tuple[float, float, float, float] | None = None

@dataclass(slots=True)
class TableRow:
    cells: list[TableCell]
    is_header_row: bool = False

@dataclass(slots=True)
class TableMetadata:
    company: str
    year: str
    page: int
    continued_from_previous_page: bool = False
    caption: str | None = None

@dataclass(slots=True)
class TableStructure:
    rows: list[TableRow]
    metadata: TableMetadata
    
    def normalize_numerics(self):
        for row in self.rows:
            for cell in row.cells:
                if not cell.is_header:
                    cell.content = self._normalize_value(cell.content)
                    
    def _normalize_value(self, val: str) -> str:
        clean = val.replace(",", "").replace("₹", "").strip()
        try:
            float(clean)
            return clean
        except ValueError:
            return val
