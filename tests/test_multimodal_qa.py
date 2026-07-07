import pytest
from unittest.mock import MagicMock
from filinglens.llm.qa_service import QAService
from filinglens.retrieval.multimodal import MultimodalRetriever

def test_multimodal_qa_routing():
    dense_mock = MagicMock()
    dense_mock.search.return_value = []
    retriever = MultimodalRetriever(dense_retriever=dense_mock)
    llm = MagicMock()
    service = QAService(retriever=retriever, llm=llm)
    
    assert hasattr(service.router, "route")
    intents = service.router.route("Show me the balance sheet tables")
    assert "table" in intents
