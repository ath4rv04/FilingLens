from filinglens.retrieval.multimodal import MultimodalRetriever
from filinglens.finance.repository import FinanceRepository
from filinglens.models.retrieval_result import RetrievalResult
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)

class AgentTools:
    """Wraps core FilingLens architectures establishing modular node execution bounds reliably comfortably."""
    def __init__(self, multimodal_retriever: MultimodalRetriever, finance_repository: FinanceRepository):
        self.retriever = multimodal_retriever
        self.repo = finance_repository

    def retrieve_text(self, question: str, filters: dict, top_k: int = 5) -> list[RetrievalResult]:
        logger.info("[Tool] Retrieving Narrative Context")
        return self.retriever.retrieve(question, filters=filters, top_k=top_k, intents=["dense", "bm25"])

    def retrieve_tables(self, question: str, filters: dict, top_k: int = 3) -> list:
        logger.info("[Tool] Retrieving Tabular Data")
        return self.retriever.retrieve(question, filters=filters, top_k=top_k, intents=["table"])

    def retrieve_visual(self, question: str, filters: dict, top_k: int = 2) -> list:
        logger.info("[Tool] Retrieving Visual Elements")
        return self.retriever.retrieve(question, filters=filters, top_k=top_k, intents=["visual"])

    def retrieve_layout(self, question: str, filters: dict, top_k: int = 2) -> list:
        logger.info("[Tool] Retrieving Layout Context")
        return self.retriever.retrieve(question, filters=filters, top_k=top_k, intents=["layout"])

    def retrieve_metrics(self, company: str, year: str) -> list:
        logger.info(f"[Tool] Retrieving Metrics for {company} {year}")
        if not company or not year:
            return []
        metrics = self.repo.list_metrics(company, year)
        return [m.__dict__ for m in metrics]

    def generate_chart_summary(self, chart_id: str) -> str:
        # Mock logic extending visual analysis bounds structurally gracefully
        return f"Chart summary derived from logical capabilities natively for {chart_id}"

    def search_company(self, query: str) -> list[str]:
        # Typically maps towards global indices
        return []

    def search_year(self, query: str) -> list[str]:
        return []
