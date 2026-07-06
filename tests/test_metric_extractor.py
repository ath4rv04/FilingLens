from filinglens.models.document_chunk import DocumentChunk
from filinglens.finance.extractor import FinancialMetricExtractor


def test_extractor_identifies_metrics():
    extractor = FinancialMetricExtractor()
    chunk = DocumentChunk(
        id="chunk-1",
        company="TCS",
        year="FY2024",
        page=10,
        chunk=1,
        text="The Net Sales of ₹ 245,315 crore was an increase. EBITDA stood at 45000 crore.",
    )

    metrics = extractor.extract_from_chunk(chunk)
    assert len(metrics) == 2

    # Validation against normalized labels
    revenue = next(m for m in metrics if m.metric == "Revenue")
    assert revenue.value == 245315.0

    ebitda = next(m for m in metrics if m.metric == "EBITDA")
    assert ebitda.value == 45000.0
