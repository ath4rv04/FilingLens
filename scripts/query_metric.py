import argparse
from filinglens.settings import FINANCE_DB_PATH
from filinglens.finance.repository import FinanceRepository
from filinglens.finance.qa import FinanceQA


def main():
    parser = argparse.ArgumentParser(
        description="Query Financial Intelligence Repository."
    )
    parser.add_argument("--company", required=True)
    parser.add_argument("--year", required=True)
    parser.add_argument("--metric", required=True)
    args = parser.parse_args()

    repo = FinanceRepository(db_path=FINANCE_DB_PATH)
    qa = FinanceQA(repo)

    response, _ = qa.answer_metric(args.company, args.year, args.metric)
    if response:
        print(f"Result: {response}")
    else:
        print("Metric unavailable in analytical cache.")


if __name__ == "__main__":
    main()
