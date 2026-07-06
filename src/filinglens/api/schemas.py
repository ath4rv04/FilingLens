from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str


class Source(BaseModel):
    company: str
    year: str
    page: int | None
    chunk: int | None
    chunk_id: str
    text: str


class AskRequest(BaseModel):
    company: str
    year: str
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]
    model: str
    latency_ms: float


class ProcessResponse(BaseModel):
    company: str
    year: str
    page_count: int
    scanned_pages: int
    chunk_count: int


class IndexRequest(BaseModel):
    company: str
    year: str


class IndexResponse(BaseModel):
    chunks_indexed: int
    collection: str


class ErrorResponse(BaseModel):
    detail: str
