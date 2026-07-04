from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from scripts.build_index import load_chunks

from filinglens.embeddings.embedder import get_embedding_service
from filinglens.ingestion.document_processor import DocumentProcessor
from filinglens.retrieval import BM25Retriever, DenseRetriever, HybridRetriever
from filinglens.tables import PdfPlumberTableExtractor
from filinglens.vectorstore import QdrantVectorStore


class ProcessRequest(BaseModel):
    input: str


class IndexRequest(BaseModel):
    chunks: str
    collection: str | None = None
    recreate: bool = False


class SearchRequest(BaseModel):
    question: str
    chunks: str | None = None
    collection: str | None = None
    top_k: int = 5


def create_app() -> FastAPI:
    api = FastAPI(title="FilingLens-IN API")

    @api.post("/process")
    def process(request: ProcessRequest) -> dict[str, str]:
        DocumentProcessor(request.input).process()
        return {"status": "processed", "input": request.input}

    @api.post("/index")
    def index(request: IndexRequest) -> dict[str, object]:
        chunks = load_chunks(Path(request.chunks))
        embeddings = get_embedding_service().embed([chunk.text for chunk in chunks])
        store = QdrantVectorStore(
            **({"collection_name": request.collection} if request.collection else {})
        )
        store.create_collection(recreate=request.recreate)
        store.upload_chunks(chunks, embeddings)
        return store.collection_stats()

    @api.post("/search")
    def search(request: SearchRequest) -> dict[str, object]:
        store = QdrantVectorStore(
            **({"collection_name": request.collection} if request.collection else {})
        )
        dense = DenseRetriever(embedder=get_embedding_service(), vector_store=store)

        if request.chunks:
            retriever = HybridRetriever(
                dense_retriever=dense,
                bm25_retriever=BM25Retriever(load_chunks(Path(request.chunks))),
            )
        else:
            retriever = dense

        results = retriever.search(request.question, top_k=request.top_k)
        return {
            "results": [result.payload | {"score": result.score} for result in results]
        }

    @api.post("/chat")
    def chat(request: SearchRequest) -> dict[str, object]:
        search_response = search(request)
        return {
            "answer": "LLM generation is not configured yet.",
            "context": search_response["results"],
        }

    @api.post("/tables/extract")
    def extract_tables(request: ProcessRequest) -> dict[str, object]:
        pdf_path = Path(request.input)
        output_dir = pdf_path.parent / "tables"
        extractor = PdfPlumberTableExtractor()
        tables = extractor.extract(pdf_path)
        written = extractor.write_csvs(tables, output_dir)
        return {"tables": len(written), "output": str(output_dir)}

    return api


app = create_app()
