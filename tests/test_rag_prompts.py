from filinglens.rag import Citation, ContextBlock, RagPromptBuilder


def test_rag_prompt_builder_includes_question_context_and_citation_instruction():
    block = ContextBlock(
        citation=Citation(
            company="TCS",
            year="FY2024",
            page=5,
            chunk=1,
            chunk_id="chunk-1",
        ),
        text="Revenue increased due to strong demand.",
        score=0.9,
        source="hybrid",
    )

    prompt = RagPromptBuilder().build("Why did revenue grow?", [block])

    assert "Answer ONLY using the supplied context" in prompt.system
    assert "Why did revenue grow?" in prompt.user
    assert "[1] TCS FY2024 Page 5 Chunk 1" in prompt.user
    assert "Use citations like [1]." in prompt.user


def test_rag_prompt_builder_handles_empty_context():
    prompt = RagPromptBuilder().build("What changed?", [])

    assert "No context available." in prompt.user
