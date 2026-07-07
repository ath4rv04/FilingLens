from unittest.mock import MagicMock
from filinglens.agents.tools import AgentTools

def test_tools_retrieve_metrics():
    repo_mock = MagicMock()
    tools = AgentTools(multimodal_retriever=MagicMock(), finance_repository=repo_mock)
    
    tools.retrieve_metrics("TCS", "2024")
    repo_mock.list_metrics.assert_called_with("TCS", "2024")
