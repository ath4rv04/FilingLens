from unittest.mock import MagicMock
from filinglens.agents.specialized import SpecializedAgents

def test_visual_agent():
    tools = MagicMock()
    tools.retrieve_visual.return_value = []
    
    agents = SpecializedAgents(tools, MagicMock())
    state = {"question": "Chart?", "company": "TCS", "year": "2024"}
    
    res = agents.visual_node(state)
    assert len(res["draft_findings"]) == 1
    assert res["draft_findings"][0]["source"] == "visual"
