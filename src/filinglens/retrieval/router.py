from filinglens.utils.logging import get_logger

logger = get_logger(__name__)

class IntentRouter:
    """Classifies user queries dynamically routing across discrete modal bindings explicitly."""
    def route(self, query: str) -> list[str]:
        query_lower = query.lower()
        intents = ["dense", "bm25"]
        
        if "table" in query_lower or "balance sheet" in query_lower or "financials" in query_lower:
            intents.append("table")
        if "chart" in query_lower or "image" in query_lower or "picture" in query_lower or "graph" in query_lower:
            intents.append("visual")
        if "chairman" in query_lower or "letter" in query_lower or "section" in query_lower or "md&a" in query_lower:
            intents.append("layout")
            
        logger.info(f"Intent routing determined logical paths: {intents}")
        return intents
