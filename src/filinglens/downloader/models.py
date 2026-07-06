from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(slots=True)
class Filing:
    company: str
    year: str
    filing_type: str
    source: str
    url: str
    filename: str


@dataclass(slots=True)
class CompanyProfile:
    name: str
    bse_code: Optional[str]
    nse_symbol: Optional[str]
    investor_relations_url: Optional[str]


@dataclass(slots=True)
class DownloadResult:
    filing: Filing
    success: bool
    path: Optional[Path]
    size: int
    checksum: Optional[str]
    error: Optional[str]
