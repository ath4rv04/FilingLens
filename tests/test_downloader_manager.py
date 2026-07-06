from filinglens.downloader.downloader import DownloadManager
from filinglens.downloader.storage import StorageManager
from filinglens.downloader.models import Filing


def test_download_manager_aborts_on_cache(tmp_path):
    storage = StorageManager(tmp_path)
    filing = Filing("Mock", "2024", "AR", "System", "", "annual_report.pdf")
    storage.save(filing, b"fake", pages=1)  # force exist

    manager = DownloadManager(storage_manager=storage)
    res = manager.download("Mock", "2024")

    assert res.success is True
    assert res.error is None
