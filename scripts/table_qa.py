import argparse
from pathlib import Path

from filinglens.tables import TableQuestionAnswerer, TableRepository


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tables", required=True, help="Directory of extracted table CSVs"
    )
    parser.add_argument("--question", required=True)
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    repository = TableRepository.from_csv_dir(Path(args.tables))
    answerer = TableQuestionAnswerer(repository.tables)
    answers = answerer.answer(args.question, top_k=args.top_k)

    if not answers:
        print("No table answers found.")
        return

    for answer in answers:
        print(answer.render())
        print()


if __name__ == "__main__":
    main()
