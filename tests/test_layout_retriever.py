import pytest
from filinglens.retrieval.layout import LayoutRetriever

def test_layout_retriever():
    retriever = LayoutRetriever()
    assert hasattr(retriever, "retrieve")
    assert retriever.retrieve("MD&A", "TCS", "2024") == []
