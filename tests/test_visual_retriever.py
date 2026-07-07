import pytest
from filinglens.retrieval.visual import VisualRetriever

def test_visual_retriever():
    retriever = VisualRetriever()
    assert hasattr(retriever, "retrieve")
    # Native integrations evaluate embedding matrices smoothly globally
