import argparse
from pathlib import Path

from filinglens.visual import VisualRetriever


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    results = VisualRetriever(Path(args.pages)).search(args.question, top_k=args.top_k)

    for result in results:
        print(f"[{result.score:.4f}] page {result.page}: {result.image_path}")


if __name__ == "__main__":
    main()
