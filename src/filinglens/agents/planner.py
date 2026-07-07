import json
from filinglens.llm.base import BaseLLMProvider
from filinglens.agents.state import GraphState
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)

PLANNER_PROMPT = """
You are the Orchestration Planner for FilingLens.
Analyze the user's question and determine which specialized agents are required to answer it accurately.

Available Agents:
- "financial": Retrieves deterministic numeric metrics (e.g. Revenue, EBITDA, EPS).
- "narrative": Retrieves text paragraphs from MD&A, Management Notes, and general filing narrative.
- "table": Retrieves structured tabular data from balance sheets, income statements, or footnotes.
- "visual": Retrieves images of charts, graphs, or full-page visualizations.
- "comparison": Required if the question specifically asks to compare across multiple years or companies.

Return a JSON strictly adhering to this format:
{
  "intent": "<short string summarizing the user intent>",
  "required_agents": ["<agent_name_1>", "<agent_name_2>"],
  "confidence": <float between 0 and 1>
}
"""

class PlannerNode:
    """Evaluates question determining intent and required capabilities wrapping LLM JSON extraction natively."""
    def __init__(self, llm: BaseLLMProvider):
        self.llm = llm

    def __call__(self, state: GraphState) -> dict:
        question = state.get("question", "")
        logger.info(f"Planner processing query: {question}")
        
        user_prompt = f"Question: {question}\n\nRespond only with valid JSON."
        
        # In a real environment, enforce JSON schema.
        response = self.llm.generate(system=PLANNER_PROMPT, user=user_prompt)
        
        try:
            # simple json extraction
            content = response.answer
            start = content.find('{')
            end = content.rfind('}')
            if start != -1 and end != -1:
                content = content[start:end+1]
            data = json.loads(content)
            
            logger.info("Planner formulated valid orchestration parameters successfully natively.")
            return {
                "intent": data.get("intent", "general"),
                "required_agents": data.get("required_agents", ["narrative"]),
            }
        except Exception as e:
            logger.error(f"Planner failed JSON parsing, defaulting seamlessly natively. Error: {str(e)}")
            return {
                "intent": "general",
                "required_agents": ["narrative"],
            }
