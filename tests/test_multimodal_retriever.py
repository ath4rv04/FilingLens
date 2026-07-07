import pytest
from unittest.mock import MagicMock
from filinglens.retrieval.multimodal import MultimodalRetriever

def test_multimodal_retriever():
    dense_mock = MagicMock()
    dense_mock.search.return_value = []
    retriever = MultimodalRetriever(dense_retriever=dense_mock)
    res = retriever.retrieve("What is the total revenue?", intents=["dense"])
    assert isinstance(res, list)
