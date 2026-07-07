from unittest.mock import MagicMock
from filinglens.agents.writer import WriterNode

def test_writer_node():
    llm = MagicMock()
    writer = WriterNode(llm)
    state = {"verified_findings": [{"claim": "Revenue was 1M", "citations": ["doc"]}]}
    
    result = writer(state)
    assert "Executive Summary" in result["final_answer"]
    assert "Revenue" in result["final_answer"]
    assert "doc" in result["final_answer"]
