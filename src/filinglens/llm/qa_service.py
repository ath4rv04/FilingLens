from filinglens.llm.base import BaseLLMProvider
from filinglens.llm.response import LLMResponse
from filinglens.rag.context import ContextAssembler
from filinglens.rag.prompts import RagPromptBuilder
from filinglens.utils.timer import Timer
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


class QAService:
    """Orchestrates RAG retrieval, context assembly, and LLM text generation."""

    def __init__(
        self,
        retriever,
        llm: BaseLLMProvider,
    ):
        self.retriever = retriever
        self.llm = llm
        
        from filinglens.retrieval.router import IntentRouter
        self.router = IntentRouter()
        
        self.context_assembler = ContextAssembler()
        self.prompt_builder = RagPromptBuilder()

    def answer(
        self,
        question: str,
        company: str | None = None,
        year: str | None = None,
        top_k: int = 5,
    ) -> tuple[LLMResponse, list, dict[str, float]]:

        filters = {}
        if company:
            filters["company"] = company
        if year:
            filters["year"] = year

        intents = self.router.route(question)
        
        with Timer("retrieval") as ret_timer:
            if hasattr(self.retriever, "retrieve"):
                results = self.retriever.retrieve(
                    question,
                    top_k=top_k,
                    filters=filters if filters else None,
                    intents=intents
                )
            else:
                results = self.retriever.search(
                    question,
                    top_k=top_k,
                    filters=filters if filters else None,
                )

        logger.info(
            "Retrieval Step",
            extra={
                "company": company,
                "year": year,
                "top_k": top_k,
                "retrieved_chunk_ids": [r.chunk.id for r in results],
                "retrieval_latency": ret_timer.elapsed_ms,
            },
        )

        context_blocks = self.context_assembler.assemble(results)

        prompt = self.prompt_builder.build(question, context_blocks)

        logger.info(
            "Prompt assembled: length %d chars", len(prompt.system) + len(prompt.user)
        )

        with Timer("llm_generation") as llm_timer:
            llm_response = self.llm.generate(
                system=prompt.system,
                user=prompt.user,
            )

        logger.info(
            "LLM Generation Step",
            extra={
                "model": llm_response.model,
                "llm_latency": llm_timer.elapsed_ms,
                "total_latency": ret_timer.elapsed_ms + llm_timer.elapsed_ms,
            },
        )

        metrics = {
            "retrieval_ms": ret_timer.elapsed_ms,
            "llm_ms": llm_timer.elapsed_ms,
            "total_ms": ret_timer.elapsed_ms + llm_timer.elapsed_ms,
            "prompt_preview": f"System:\n{prompt.system}\n\nUser:\n{prompt.user}"
        }

        return llm_response, context_blocks, metrics
