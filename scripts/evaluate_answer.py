import argparse

from filinglens.evaluation import evaluate_answer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--answer", required=True)
    parser.add_argument("--context", required=True)
    parser.add_argument("--expected-term", action="append", default=[])
    args = parser.parse_args()

    result = evaluate_answer(
        answer=args.answer,
        expected_terms=args.expected_term,
        context=args.context,
    )
    print(result)


if __name__ == "__main__":
    main()
