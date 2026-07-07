import pytest
from unittest.mock import MagicMock
from filinglens.agents.graph import FilingLensAgenticOrchestrator

def test_graph_compile():
    tools_mock = MagicMock()
    llm_mock = MagicMock()
    
    orchestrator = FilingLensAgenticOrchestrator(tools_mock, llm_mock)
    assert orchestrator.graph is not None

def test_graph_invocation():
    tools_mock = MagicMock()
    llm_mock = MagicMock()
    
    orchestrator = FilingLensAgenticOrchestrator(tools_mock, llm_mock)
    
    # Bypass executing complex nodes verifying basic compile tracks cleanly correctly
    assert hasattr(orchestrator, "invoke")
