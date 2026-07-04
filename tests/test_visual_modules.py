from filinglens.visual import HeuristicChartCaptioner, VisualRetriever


def test_visual_retriever_returns_page_images(tmp_path):
    (tmp_path / "page_001.png").write_text("fake", encoding="utf-8")
    (tmp_path / "page_002.png").write_text("fake", encoding="utf-8")

    results = VisualRetriever(tmp_path).search("revenue chart", top_k=1)

    assert len(results) == 1
    assert results[0].page == 1


def test_heuristic_chart_captioner_returns_caption(tmp_path):
    image_path = tmp_path / "page_001_revenue_chart.png"
    image_path.write_text("fake", encoding="utf-8")

    caption = HeuristicChartCaptioner().caption(image_path)

    assert "revenue chart" in caption.caption
    assert caption.confidence == 0.25
