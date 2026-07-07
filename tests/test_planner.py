from unittest.mock import MagicMock
from filinglens.agents.planner import PlannerNode

def test_planner_node_extraction():
    mock_llm = MagicMock()
    mock_llm.generate.return_value.answer = '{"intent": "finance", "required_agents": ["financial"]}'
    
    planner = PlannerNode(mock_llm)
    state = {"question": "What is revenue?"}
    
    res = planner(state)
    assert res["intent"] == "finance"
    assert "financial" in res["required_agents"]
