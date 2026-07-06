from filinglens.llm.base import BaseLLMProvider
from filinglens.llm.response import LLMResponse
from filinglens.llm.qa_service import QAService
from filinglens.models import RetrievalResult, DocumentChunk


class FakeRetriever:
    def search(self, query, top_k, filters=None):
        self.query = query
        self.filters = filters
        return [
            RetrievalResult(
                chunk=DocumentChunk(
                    id="chunk-1",
                    company="TCS",
                    year="FY2024",
                    page=1,
                    chunk=0,
                    text="Revenue increased.",
                ),
                score=0.9,
                source="dense",
            )
        ]


class FakeLLM(BaseLLMProvider):
    def generate(self, *, system, user):
        self.system = system
        self.user = user
        return LLMResponse(answer="Revenue grew...", model="fake", latency_ms=10.0)

    def generate_stream(self, *, system, user):
        pass


def test_qa_service_orchestrates_retrieval_and_llm():
    retriever = FakeRetriever()
    llm = FakeLLM()
    service = QAService(retriever=retriever, llm=llm)

    response, blocks, metrics = service.answer(
        question="What happened?", company="TCS", year="FY2024"
    )

    assert response.answer == "Revenue grew..."
    assert retriever.query == "What happened?"
    assert retriever.filters == {"company": "TCS", "year": "FY2024"}
    assert "Revenue increased" in llm.user
    assert "What happened?" in llm.user
