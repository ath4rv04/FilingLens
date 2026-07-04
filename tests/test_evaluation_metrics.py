from filinglens.evaluation import evaluate_answer


def test_evaluate_answer_scores_context_and_citations():
    result = evaluate_answer(
        answer="Revenue grew due to demand [1].",
        expected_terms=["revenue", "demand"],
        context="Revenue grew due to strong demand in FY2024.",
    )

    assert result.faithfulness > 0
    assert result.context_recall == 1.0
    assert result.citation_coverage == 1.0
