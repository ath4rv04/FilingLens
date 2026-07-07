from unittest.mock import MagicMock
from filinglens.agents.specialized import SpecializedAgents

def test_table_agent():
    tools = MagicMock()
    tools.retrieve_tables.return_value = []
    
    agents = SpecializedAgents(tools, MagicMock())
    state = {"question": "Table?", "company": "TCS", "year": "2024"}
    
    res = agents.table_node(state)
    assert len(res["draft_findings"]) == 1
    assert "source" in res["draft_findings"][0]
