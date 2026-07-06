from unittest.mock import patch
from filinglens.downloader.utils.pdf_discovery import PDFDiscovery


@patch("requests.get")
def test_pdf_discovery_finds_pdf_links(mock_get):
    class FakeResponse:
        text = """
        <html>
            <body>
                <a href="/reports/annual_report_2024.pdf">Annual Report</a>
                <a href="/about.html">About us</a>
                <a href="https://example.com/other.pdf?download=1">Other</a>
                <a href="/reports/annual_report_2024.pdf">Duplicate Link</a>
            </body>
        </html>
        """
        headers = {"Content-Type": "text/html"}

        def raise_for_status(self):
            pass

    mock_get.return_value = FakeResponse()

    links = PDFDiscovery.discover_pdf_links("https://tcs.com")

    assert len(links) == 2

    assert "https://tcs.com/reports/annual_report_2024.pdf" in links
    assert "https://example.com/other.pdf?download=1" in links
    assert "https://tcs.com/about.html" not in links


@patch("requests.get")
def test_pdf_discovery_ignores_non_html(mock_get):
    class FakeResponse:
        text = "bunch of binary"
        headers = {"Content-Type": "application/json"}

        def raise_for_status(self):
            pass

    mock_get.return_value = FakeResponse()
    links = PDFDiscovery.discover_pdf_links("https://tcs.com")
    assert len(links) == 0
