from unittest.mock import patch
from filinglens.downloader.providers.search import SearchProvider


@patch("requests.head")
@patch("requests.get")
def test_verify_pdf_header_success(mock_get, mock_head):
    class FakeHead:
        status_code = 200
        headers = {"Content-Type": "application/pdf"}

    mock_head.return_value = FakeHead()

    p = SearchProvider()
    assert p._verify_pdf_header("http://fake.com") is True


@patch("requests.head")
@patch("requests.get")
def test_verify_pdf_header_fallback(mock_get, mock_head):
    class FakeHead:
        status_code = 405
        headers = {}

    mock_head.return_value = FakeHead()

    class FakeGet:
        status_code = 200
        headers = {"Content-Type": "application/pdf"}

        def close(self):
            pass

    mock_get.return_value = FakeGet()

    p = SearchProvider()
    assert p._verify_pdf_header("http://fake.com") is True
