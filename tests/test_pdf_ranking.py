from filinglens.downloader.ranking import PDFRanker


def test_pdf_ranker_logic():
    # Assert specific keywords target priorities intelligently.

    perfect_score = PDFRanker.score_candidate(
        "https://tcs.com/annual_report_2024.pdf", "FY2024", "TCS"
    )
    assert perfect_score > 60

    q1_score = PDFRanker.score_candidate("https://tcs.com/q1_presentation_2024.pdf", "FY2024", "TCS")
    assert q1_score <= 0

    urls = [
        "https://tcs.com/q1_presentation.pdf",
        "https://tcs.com/annual_report_2024.pdf",
        "https://tcs.com/esg_report.pdf",
        "https://tcs.com/integrated_annual_report_2024.pdf",
    ]

    ranked = PDFRanker.rank_candidates(urls, "FY2024", "TCS", top_k=2)

    assert len(ranked) == 2
    assert "annual_report" in ranked[0][1] or "integrated" in ranked[0][1]
