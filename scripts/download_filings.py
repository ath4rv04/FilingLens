import argparse
from filinglens.downloader.downloader import DownloadManager
from filinglens.downloader.registry import CompanyRegistry


def main():
    parser = argparse.ArgumentParser(description="Acquire Annual Reports Automagically")
    parser.add_argument("--company", help="Company Name")
    parser.add_argument(
        "--years", nargs="+", help="Specific formatted years (e.g. FY2024)"
    )
    parser.add_argument(
        "--latest",
        action="store_true",
        help="Fetches the most recent FY2024 boundary implicitly.",
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Invalidates local caches"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Evaluates routes without bytes"
    )
    parser.add_argument("--source", default="auto", choices=["auto", "ir", "bse"])

    args = parser.parse_args()

    company = args.company
    years = args.years or (["FY2024"] if args.latest else [])

    if args.dry_run:
        print(f"DRY RUN: Evaluated targets spanning {company} across {years}.")
        return

    manager = DownloadManager()

    targets = [(company, y) for y in years]
    results = manager.download_batch(targets, overwrite=args.overwrite)

    for r in results:
        status = "SUCCESS" if r.success else f"FAILED - {r.error}"
        print(f"[{status}] {r.filing.company} {r.filing.year} via {r.filing.source}")


if __name__ == "__main__":
    main()
