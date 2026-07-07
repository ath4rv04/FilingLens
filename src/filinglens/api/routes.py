import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, Request
from typing import Annotated

from filinglens.api.schemas import (
    HealthResponse,
    AskRequest,
    AskResponse,
    Source,
    ProcessResponse,
    IndexRequest,
    IndexResponse,
)
from filinglens.api.dependencies import (
    get_qa_service,
    get_indexing_service,
)
from filinglens.ingestion.document_processor import DocumentProcessor
from filinglens.llm.qa_service import QAService
from filinglens.services.indexing_service import IndexingService
from filinglens.finance.repository import FinanceRepository
from filinglens.api.dependencies import get_finance_repository
from filinglens.settings import PROCESSED_DATA_DIR, RAW_DATA_DIR

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok", version="3.0")


@router.post("/process", response_model=ProcessResponse)
def process_document(
    company: Annotated[str, Form()],
    year: Annotated[str, Form()],
    file: UploadFile = File(...),
):
    target_dir = RAW_DATA_DIR / company / year
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / file.filename

    with target_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    processor = DocumentProcessor(str(target_path))
    result = processor.process()

    return ProcessResponse(
        company=result.company,
        year=result.year,
        page_count=result.page_count,
        scanned_pages=result.scanned_pages,
        chunk_count=result.chunk_count,
    )


@router.post("/index", response_model=IndexResponse)
def index_documents(
    request: IndexRequest,
    indexing_service: Annotated[IndexingService, Depends(get_indexing_service)],
):
    count, collection = indexing_service.index_company_year(
        request.company, request.year
    )
    return IndexResponse(chunks_indexed=count, collection=collection)


@router.post("/ask", response_model=AskResponse)
def ask_question(
    request_data: AskRequest,
    request: Request,
    qa_service: Annotated[QAService, Depends(get_qa_service)],
):
    response, context_blocks, metrics = qa_service.answer(
        question=request_data.question,
        company=request_data.company,
        year=request_data.year,
    )

    request.state.retrieval_time = metrics["retrieval_ms"]
    request.state.llm_time = metrics["llm_ms"]

    sources = [
        Source(
            company=block.citation.company,
            year=block.citation.year,
            page=block.citation.page,
            chunk=block.citation.chunk,
            chunk_id=block.citation.chunk_id,
            text=block.text,
        )
        for block in context_blocks
    ]

    return AskResponse(
        answer=response.answer,
        sources=sources,
        model=response.model,
        latency_ms=response.latency_ms,
    )


@router.get("/companies", response_model=list[str])
def list_companies():
    if not PROCESSED_DATA_DIR.exists():
        return []
    return sorted([d.name for d in PROCESSED_DATA_DIR.iterdir() if d.is_dir()])


@router.get("/companies/{company}/years", response_model=list[str])
def list_years(company: str):
    company_dir = PROCESSED_DATA_DIR / company
    if not company_dir.exists():
        return []
    return sorted([d.name for d in company_dir.iterdir() if d.is_dir()])


@router.get("/metrics")
def get_all_metrics(
    company: str = None,
    year: str = None,
    repo: FinanceRepository = Depends(get_finance_repository),
):
    # Standardize output for broad configurations returning mappings seamlessly.
    # Note: SQLite repository doesn't have an empty 'list_all' in prototype but we can query by filtering natively.
    return repo.compare(
        metric="Revenue",
        companies=[company] if company else None,
        years=[year] if year else None,
    )


@router.get("/metrics/{company}/{year}")
def list_company_metrics(
    company: str, year: str, repo: FinanceRepository = Depends(get_finance_repository)
):
    return [m.__dict__ for m in repo.list_metrics(company, year)]


@router.get("/metrics/query")
def query_metric(
    company: str,
    year: str,
    metric: str,
    repo: FinanceRepository = Depends(get_finance_repository),
):
    from filinglens.finance.normalizer import normalize_metric_name

    m = repo.find(company, year, normalize_metric_name(metric))
    return m.__dict__ if m else None


@router.post("/metrics/extract")
def extract_metrics(
    company: str, year: str, repo: FinanceRepository = Depends(get_finance_repository)
):
    chunk_dir = PROCESSED_DATA_DIR / company / year / "chunks"
    if not chunk_dir.exists():
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Processed chunks not found.")

    from filinglens.indexing.loader import load_chunks
    from filinglens.finance.extractor import FinancialMetricExtractor

    chunks = load_chunks(chunk_dir)
    extractor = FinancialMetricExtractor()
    all_metrics = []

    for chunk in chunks:
        all_metrics.extend(extractor.extract_from_chunk(chunk))

    repo.save_many(all_metrics)
    return {"extracted": len(all_metrics)}

@router.get("/pages/{company}/{year}/{page}")
def get_page(company: str, year: str, page: int):
    # Dummy mock mapping retrieving pure layout bindings structurally gracefully
    return {"company": company, "year": year, "page": page, "image_path": f"data/processed/images/{company}/{year}/page_{page}.png"}

@router.get("/layout/{company}/{year}")
def get_layout(company: str, year: str):
    return {"company": company, "year": year, "sections": []}

@router.get("/tables/{company}/{year}")
def get_tables(company: str, year: str):
    return {"company": company, "year": year, "tables": []}

@router.get("/charts/{company}/{year}")
def get_charts(company: str, year: str):
    return {"company": company, "year": year, "charts": []}

@router.post("/visual-search")
def visual_search(query: str, company: str = None, year: str = None):
    return {"results": []}

@router.post("/agent-ask")
def agent_ask(
    request_data: dict, # Temporarily mock raw mappings securely cleanly
    request: Request,
):
    # Dummy handler mapping logical paths bypassing complex orchestration instances accurately cleanly
    question = request_data.get("question", "")
    company = request_data.get("company", None)
    year = request_data.get("year", None)
    debug = request_data.get("debug", False)
    
    # Normally instantiated via dependencies passing singletons natively properly
    # mock trace output
    res = {
        "answer": "This is a synthesized analyst response mimicking structural native Agent endpoints globally cleanly.",
        "planner": {"intent": "general"},
        "agents_used": ["narrative", "table"],
        "confidence": 0.98,
        "citations": [{"claim": "example", "citations": ["doc"]}]
    }
    
    if debug:
        res["execution_trace"] = [
            {"node": "PlannerNode", "latency_ms": 120},
            {"node": "NarrativeAgent", "latency_ms": 1500},
            {"node": "WriterAgent", "latency_ms": 600}
        ]
        
    return res
