from __future__ import annotations

from dataclasses import dataclass, field

from filinglens.agents.router import AgentRoute, QueryRouter
from filinglens.rag import ContextAssembler, RagPrompt, RagPromptBuilder
from filinglens.retrieval import RetrievalResult
from filinglens.tables import TableAnswer


@dataclass(slots=True)
class WorkflowState:
    question: str
    route: AgentRoute | None = None
    retrieval_results: list[RetrievalResult] = field(default_factory=list)
    table_answers: list[TableAnswer] = field(default_factory=list)
    prompt: RagPrompt | None = None


class FilingLensWorkflow:
    """Small multi-agent coordinator; replaceable with LangGraph nodes later."""

    def __init__(
        self,
        *,
        router: QueryRouter,
        retriever,
        table_answerer=None,
        context_assembler: ContextAssembler | None = None,
        prompt_builder: RagPromptBuilder | None = None,
    ) -> None:
        self.router = router
        self.retriever = retriever
        self.table_answerer = table_answerer
        self.context_assembler = context_assembler or ContextAssembler()
        self.prompt_builder = prompt_builder or RagPromptBuilder()

    def run(self, question: str, *, top_k: int = 5) -> WorkflowState:
        state = WorkflowState(question=question)
        state.route = self.router.route(question)

        if state.route.use_retrieval:
            state.retrieval_results = self.retriever.search(question, top_k=top_k)

        if state.route.use_tables and self.table_answerer is not None:
            state.table_answers = self.table_answerer.answer(question, top_k=top_k)

        context_blocks = self.context_assembler.assemble(state.retrieval_results)
        state.prompt = self.prompt_builder.build(question, context_blocks)
        return state
