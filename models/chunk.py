from dataclasses import dataclass
from typing import Dict


@dataclass
class DocumentChunk:
    company: str
    year: str
    page: int
    chunk_id: int
    text: str
    metadata: Dict