from filinglens.agents import FilingLensWorkflow, QueryRouter
from filinglens.retrieval import RetrievalResult


class FakeRetriever:
    def search(self, question, top_k):
        return [
            RetrievalResult(
                id="chunk-1",
                score=0.9,
                payload={
                    "chunk_id": "chunk-1",
                    "company": "TCS",
                    "year": "FY2024",
                    "page": 1,
                    "chunk": 0,
                    "text": "Management discussed demand.",
                },
                source="hybrid",
            )
        ]


def test_workflow_routes_retrieves_and_builds_prompt():
    workflow = FilingLensWorkflow(router=QueryRouter(), retriever=FakeRetriever())

    state = workflow.run("Explain demand outlook", top_k=1)

    assert state.route is not None
    assert state.route.use_retrieval is True
    assert state.prompt is not None
    assert "Management discussed demand." in state.prompt.user
