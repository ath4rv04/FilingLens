from filinglens.downloader.storage import StorageManager
from filinglens.downloader.models import Filing


def test_discovery_cache_tracks_landing_pages(tmp_path):
    storage = StorageManager(tmp_path)

    filing = Filing(
        "TCS",
        "FY2024",
        "Annual Report",
        "SearchProvider",
        "http://tcs.com/ar.pdf",
        "annual_report.pdf",
    )
    setattr(filing, "landing_page", "http://tcs.com/investor-relations")

    storage.save(filing, b"mocked", pages=1)

    key = "TCS_FY2024"
    assert storage.manifest[key]["landing_page"] == "http://tcs.com/investor-relations"
    assert storage.manifest[key]["url"] == "http://tcs.com/ar.pdf"
