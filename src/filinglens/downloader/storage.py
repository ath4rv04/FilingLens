import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

from filinglens.settings import DATA_DIR
from filinglens.downloader.models import Filing


class StorageManager:
    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or DATA_DIR
        self.raw_dir = self.data_dir / "raw"
        self.manifest_path = self.data_dir / "download_manifest.json"
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> dict:
        if self.manifest_path.exists():
            with self.manifest_path.open() as f:
                return json.load(f)
        return {}

    def _save_manifest(self):
        with self.manifest_path.open("w") as f:
            json.dump(self.manifest, f, indent=2)

    def compute_checksum(self, file_path: Path) -> str:
        sha256 = hashlib.sha256()
        with file_path.open("rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256.update(block)
        return sha256.hexdigest()

    def get_filing_path(self, filing: Filing) -> Path:
        target = self.raw_dir / filing.company / filing.year / filing.filename
        target.parent.mkdir(parents=True, exist_ok=True)
        return target

    def save(self, filing: Filing, content_bytes: bytes, pages: int = 0) -> Path:
        target = self.get_filing_path(filing)
        target.write_bytes(content_bytes)

        checksum = self.compute_checksum(target)
        size = len(content_bytes)

        key = f"{filing.company}_{filing.year}"
        self.manifest[key] = {
            "source": filing.source,
            "url": getattr(filing, "url", ""),
            "landing_page": getattr(filing, "landing_page", ""),
            "downloaded_at": datetime.now(timezone.utc).isoformat(),
            "checksum": checksum,
            "pages": pages,
            "size": size,
            "downloaded": True,
            "status": "success",
        }
        self._save_manifest()
        return target

    def get_cached_url(self, company: str, year: str) -> str:
        """Retrieves verified URL avoiding duplicate search lookups strictly."""
        key = f"{company}_{year}"
        if key in self.manifest and self.manifest[key].get("downloaded"):
            return self.manifest[key].get("url")
        return None

    def exists(self, filing: Filing) -> bool:
        """Determines if target exists natively avoiding identical redownloads gracefully."""
        key = f"{filing.company}_{filing.year}"
        if key in self.manifest and self.manifest[key].get("status") == "success":
            target = self.get_filing_path(filing)
            return target.exists()
        return False
