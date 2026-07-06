from unittest.mock import patch
from filinglens.downloader.sources.investor_relations import InvestorRelationsSource
from filinglens.downloader.models import Filing


@patch("requests.get")
def test_investor_relations_list_filings(mock_get):
    class FakeResponse:
        text = '<a href="annual_report_2024.pdf">AR</a>'
        headers = {'Content-Type': 'text/html'}
        def raise_for_status(self): pass
    mock_get.return_value = FakeResponse()

    source = InvestorRelationsSource()
    filings = source.list_filings("TCS", ["FY2024"])

    assert len(filings) == 1
    assert "tcs" in filings[0].url.lower()


@patch("requests.get")
def test_investor_relations_download_verifies_pdf(mock_get):
    class FakeResponse:
        content = b"fake_data_too_small"
        headers = {"Content-Type": "application/pdf"}

        def raise_for_status(self):
            pass

    mock_get.return_value = FakeResponse()

    source = InvestorRelationsSource()
    filing = Filing("TCS", "FY2024", "AR", "IR", "http://", "report.pdf")

    result = source.download(filing)
    assert result.success is False
    assert "magic bytes" in result.error.lower()
