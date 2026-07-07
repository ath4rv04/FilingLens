from unittest.mock import MagicMock
from filinglens.agents.verifier import VerifierNode
from filinglens.agents.state import GraphState

def test_verifier_node():
    llm = MagicMock()
    verifier = VerifierNode(llm)
    state = {"draft_findings": [{"finding": "Valid claim", "source": "page_1"}]}
    
    result = verifier(state)
    assert len(result["verified_findings"]) == 1
