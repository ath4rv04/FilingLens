from filinglens.llm.factory import get_llm
from filinglens.rag.context import ContextAssembler
from filinglens.rag.prompts import RagPromptBuilder


class QAService:
    """Runs the RAG pipeline."""

    def __init__(self):

        self.llm = get_llm()

        self.context = ContextAssembler()

        self.prompt_builder = RagPromptBuilder()

    def answer(
        self,
        question: str,
        retrieval_results,
    ):

        context = self.context.assemble(
            retrieval_results,
        )

        prompt = self.prompt_builder.build(
            question,
            context,
        )

        return self.llm.generate(
            system=prompt.system,
            user=prompt.user,
        )
