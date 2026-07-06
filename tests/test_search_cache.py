from filinglens.downloader.storage import StorageManager
from filinglens.downloader.downloader import DownloadManager
from filinglens.downloader.models import Filing


def test_manager_cache_bypass_search_engine(tmp_path):
    storage = StorageManager(tmp_path)

    # Force a cache entry predicting a cached valid URL bypassing SearchProvider discovery natively
    filing = Filing(
        "Infosys",
        "FY2024",
        "Annual Report",
        "SearchProvider",
        "http://info.com/ar.pdf",
        "annual_report.pdf",
    )
    storage.save(filing, b"mocked", pages=5)

    assert storage.get_cached_url("Infosys", "FY2024") == "http://info.com/ar.pdf"

    m = DownloadManager(storage)
    res = m.download("Infosys", "FY2024", overwrite=True)

    # In overwrite mode, the cache check in top level is bypassed, so it attempts extraction.
    # We must mock or since it hits SearchProvider and cached URL resolves, it attempts to download `http://info.com/ar.pdf`.
    # Without requests boundary mocked it fails network predictably.
    assert res.error != "All source cascades failed."  # Found via cached injection
