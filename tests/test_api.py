from fastapi.testclient import TestClient

from filinglens.api.app import app
from filinglens.api.dependencies import (
    get_qa_service,
    get_indexing_service,
)
from filinglens.llm.response import LLMResponse
from filinglens.rag.context import ContextBlock, Citation


class FakeQAService:
    def answer(self, question, company, year):
        block = ContextBlock(
            citation=Citation(
                company="TCS", year="FY2024", page=1, chunk=1, chunk_id="chunk-1"
            ),
            text="Revenue up.",
            score=0.99,
            source="hybrid",
        )
        response = LLMResponse(answer="Fake Answer", model="fake", latency_ms=10.0)
        return response, [block], {"retrieval_ms": 5.0, "llm_ms": 5.0, "total_ms": 10.0}


class FakeIndexingService:
    def index_company_year(self, company, year):
        if company == "FAIL":
            raise FileNotFoundError("Chunks missing")
        return 100, "test_collection"


# Override dependencies
app.dependency_overrides[get_qa_service] = lambda: FakeQAService()
app.dependency_overrides[get_indexing_service] = lambda: FakeIndexingService()

client = TestClient(app)


def test_health_check_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "3.0"}


def test_ask_endpoint_returns_valid_schema():
    response = client.post(
        "/ask", json={"company": "TCS", "year": "FY2024", "question": "What happened?"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Fake Answer"
    assert data["sources"][0]["company"] == "TCS"
    assert data["latency_ms"] == 10.0


def test_index_endpoint_generates_schema():
    response = client.post("/index", json={"company": "TCS", "year": "FY2024"})
    assert response.status_code == 200
    data = response.json()
    assert data["chunks_indexed"] == 100


def test_index_raises_404_on_file_not_found_override():
    response = client.post("/index", json={"company": "FAIL", "year": "FY2024"})
    assert response.status_code == 404
    assert "Chunks missing" in response.json()["detail"]


def test_validation_exception_handler_returns_422():
    response = client.post(
        "/ask",
        json={
            "company": "TCS"
            # missing question & year
        },
    )
    assert response.status_code == 422
