from filinglens.finance.constants import METRIC_ALIASES


class IntentRouter:
    """Classifies prompts directing requests either to Analytics Repo or Hybrid Semantic Retrieval."""

    @staticmethod
    def route(query: str) -> str:
        q_lower = query.lower()

        # Check comparison query natively
        if "compare" in q_lower or "vs" in q_lower or "versus" in q_lower:
            return "ComparisonQuery"

        if "table" in q_lower or "grid" in q_lower or "sheet" in q_lower:
            return "TableQuery"

        # Check explicit metric mappings matching our analytic scopes
        for alias in METRIC_ALIASES.keys():
            if alias in q_lower:
                # If they explicitly ask 'what was X', it's a structural request.
                return "MetricQuery"

        return "NarrativeQuery"
