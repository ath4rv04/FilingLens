from filinglens.downloader.storage import StorageManager
from filinglens.downloader.models import Filing


def test_storage_manager_caching_logic(tmp_path):
    storage = StorageManager(data_dir=tmp_path)
    filing = Filing("ACME", "FY2024", "Annual Report", "IR", "http://", "report.pdf")

    # Save dummy file
    storage.save(filing, b"fake_pdf_content", pages=3)

    assert storage.exists(filing) is True

    # Manifest validation
    key = "ACME_FY2024"
    assert key in storage.manifest
    assert storage.manifest[key]["pages"] == 3
    assert storage.manifest[key]["status"] == "success"
