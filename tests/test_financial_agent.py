from unittest.mock import MagicMock
from filinglens.agents.specialized import SpecializedAgents

def test_financial_agent():
    tools = MagicMock()
    tools.retrieve_metrics.return_value = [{"metric": "Revenue", "value": 100}]
    
    agents = SpecializedAgents(tools, MagicMock())
    state = {"question": "Rev?", "company": "TCS", "year": "2024"}
    
    res = agents.financial_node(state)
    assert len(res["draft_findings"]) == 1
    assert "Revenue" in str(res["draft_findings"][0]["data"])
