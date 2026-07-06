import pytest

from filinglens.rag import ContextAssembler
from filinglens.retrieval import RetrievalResult


from filinglens.models.document_chunk import DocumentChunk


def retrieval_result(text, chunk_id="chunk-1"):
    return RetrievalResult(
        chunk=DocumentChunk(
            id=chunk_id,
            company="TCS",
            year="FY2024",
            page=7,
            chunk=2,
            text=text,
        ),
        score=0.9,
        source="hybrid",
    )


def test_context_assembler_renders_numbered_citations():
    assembler = ContextAssembler(max_characters=1000)

    rendered = assembler.render([retrieval_result("Revenue   increased\nin FY2024.")])

    assert "[1] TCS FY2024 Page 7 Chunk 2" in rendered
    assert "Revenue increased in FY2024." in rendered


def test_context_assembler_respects_character_budget():
    assembler = ContextAssembler(max_characters=10)

    blocks = assembler.assemble([retrieval_result("1234567890 extra")])

    assert blocks[0].text == "1234567890"


def test_context_assembler_rejects_invalid_budget():
    with pytest.raises(ValueError, match="max_characters"):
        ContextAssembler(max_characters=0)
