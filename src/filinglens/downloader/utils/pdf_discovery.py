import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


class PDFDiscovery:
    """Discovers internal document endpoints recursively parsing DOM definitions accurately ignoring false properties."""

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/138.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    PDF_PATTERN = re.compile(r"\.pdf($|\?)", re.IGNORECASE)

    @classmethod
    def discover_pdf_links(cls, url: str) -> list[str]:
        """Fetches raw endpoints iterating strings checking mapping formats flawlessly rendering paths linearly!"""
        try:
            response = requests.get(url, headers=cls.HEADERS, timeout=15)
            response.raise_for_status()

            # Protect boundaries blocking explicitly massive arbitrary configurations cleanly parsing properly.
            if "text/html" not in response.headers.get("Content-Type", "").lower():
                logger.warning(f"Skipping non-HTML target: {url}")
                return []

        except Exception as e:
            logger.warning(f"Discovery payload terminated mapping: {url} -> {e}")
            return []

        # Parse explicitly inside standard BS4
        try:
            soup = BeautifulSoup(response.text, "lxml")

            candidates = set()
            for anchor in soup.find_all("a", href=True):
                href = anchor["href"]
                # Normalizes internal properties targeting absolute bounds gracefully
                target = urljoin(url, href)

                # Check regex bounding accurately mapping bounds linearly
                if cls.PDF_PATTERN.search(target):
                    clean = target.split("#")[0].strip()
                    candidates.add(clean)

            logger.info(f"Target {url} mapped {len(candidates)} pdf candidates.")
            return list(candidates)

        except Exception as e:
            logger.error(f"DOM parsing boundaries violated gracefully: {e}")
            return []
