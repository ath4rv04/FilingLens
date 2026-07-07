import pytest
from filinglens.retrieval.table import TableRetriever

def test_table_retriever():
    retriever = TableRetriever()
    assert hasattr(retriever, "retrieve")
    assert retriever.retrieve("EBITDA", top_k=2) == []
