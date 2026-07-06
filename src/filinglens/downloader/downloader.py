from __future__ import annotations

import concurrent.futures
import time
from typing import List

from filinglens.downloader.models import DownloadResult, Filing
from filinglens.downloader.sources.bse import BSESource
from filinglens.downloader.sources.investor_relations import InvestorRelationsSource
from filinglens.downloader.sources.mca import MCASource
from filinglens.downloader.sources.nse import NSESource
from filinglens.downloader.storage import StorageManager
from filinglens.downloader.providers.search import SearchProvider
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


class DownloadManager:
    """
    Coordinates all filing sources.

    Each source is treated independently. A failure in one source
    never terminates the overall acquisition process.
    """

    def __init__(
        self,
        storage_manager: StorageManager | None = None,
        *,
        max_workers: int = 4,
        retries: int = 2,
        retry_delay: float = 2.0,
    ) -> None:

        self.storage = storage_manager or StorageManager()

        # Prefer official sources first.
        self.sources = [
            SearchProvider(),
            BSESource(),
            NSESource(),
            InvestorRelationsSource(),
            MCASource(),
        ]

        self.max_workers = max_workers
        self.retries = retries
        self.retry_delay = retry_delay

    # ------------------------------------------------------------------

    def download(
        self,
        company: str,
        year: str,
        *,
        overwrite: bool = False,
    ) -> DownloadResult:

        dummy = Filing(
            company=company,
            year=year,
            filing_type="Annual Report",
            source="None",
            url="",
            filename="annual_report.pdf",
        )

        if not overwrite and self.storage.exists(dummy):
            logger.info(
                "Using cached filing for %s %s",
                company,
                year,
            )

            return DownloadResult(
                filing=dummy,
                success=True,
                path=self.storage.get_filing_path(dummy),
                size=0,
                checksum=None,
                error=None,
            )

        for source in self.sources:
            logger.info(
                "Trying source: %s",
                source.name,
            )

            # ----------------------------------------------------------
            # discover candidate filings
            # ----------------------------------------------------------

            # Attempt cached bypass natively avoiding searches iteratively.
            cached_url = self.storage.get_cached_url(company, year)
            if cached_url and getattr(source, "name", "") == "SearchProvider":
                logger.info(
                    f"Triggering cache bypassing {source.name} discovery boundaries cleanly."
                )
                candidates = [
                    Filing(
                        company=company,
                        year=year,
                        filing_type="Annual Report",
                        source=source.name,
                        url=cached_url,
                        filename="annual_report.pdf",
                    )
                ]
            else:
                try:
                    candidates = source.list_filings(
                        company,
                        [year],
                    )
                except Exception as exc:
                    logger.warning(
                        "Source %s failed while listing filings: %s", source.name, exc
                    )
                    continue

            if not candidates:
                logger.info(
                    "%s returned no candidates.",
                    source.name,
                )

                continue

            logger.info(
                "%s returned %d candidate(s).",
                source.name,
                len(candidates),
            )

            # ----------------------------------------------------------
            # attempt downloads
            # ----------------------------------------------------------

            for candidate in candidates:
                for attempt in range(1, self.retries + 2):
                    try:
                        result = source.download(candidate)

                    except Exception as exc:
                        logger.warning(
                            "%s download attempt %d failed: %s",
                            source.name,
                            attempt,
                            exc,
                        )

                        if attempt <= self.retries:
                            time.sleep(self.retry_delay)
                            continue

                        break

                    if not result.success:
                        logger.warning(
                            "%s rejected %s (%s)",
                            source.name,
                            candidate.url,
                            result.error,
                        )

                        if attempt <= self.retries:
                            time.sleep(self.retry_delay)
                            continue

                        break

                    path = self.storage.save(
                        candidate,
                        result.raw_content or b"",
                        result.pages or 0,
                    )

                    result.path = path

                    logger.info(
                        "Downloaded %s from %s",
                        candidate.filename,
                        source.name,
                    )

                    return result

        logger.error(
            "Unable to locate %s %s from any configured source.",
            company,
            year,
        )

        return DownloadResult(
            filing=dummy,
            success=False,
            path=None,
            size=0,
            checksum=None,
            error="No valid filing found.",
        )

    # ------------------------------------------------------------------

    def download_batch(
        self,
        targets: List[tuple[str, str]],
        *,
        overwrite: bool = False,
    ) -> List[DownloadResult]:

        results: List[DownloadResult] = []

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers,
        ) as executor:
            futures = [
                executor.submit(
                    self.download,
                    company,
                    year,
                    overwrite=overwrite,
                )
                for company, year in targets
            ]

            for future in concurrent.futures.as_completed(futures):
                try:
                    results.append(future.result())

                except Exception as exc:
                    logger.exception(
                        "Batch download failed: %s",
                        exc,
                    )

        return results
