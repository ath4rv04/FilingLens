from filinglens.downloader.providers.search import SearchProvider


# Deleted legacy schema; replaced by PDFRanker tests.


def test_search_provider_deduplicates():
    from filinglens.downloader.providers.backends import SearchBackend, SearchResult

    class FakeBackend(SearchBackend):
        def search(self, query):
            return [
                SearchResult("AR", "https://tcs.com/ar.pdf", "Snippet"),
                SearchResult(
                    "AR", "https://tcs.com/ar.pdf#section", "Snippet 2"
                ),  # dedupe
            ]

    p = SearchProvider(backend=FakeBackend())
    filings = p.list_filings("TCS", ["FY2024"])

    urls = [f.url for f in filings]
    assert (
        len(urls) <= 1
    )  # the deduper bounds this explicitly within the internal loop correctly
