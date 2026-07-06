from filinglens.api.dependencies import (
    get_hybrid_retriever,
    get_embedder,
    get_qdrant_store,
    get_llm_provider,
    get_qa_service,
)
from filinglens.evaluation.runner import EvaluationRunner
from filinglens.settings import PROJECT_ROOT


def main():
    embedder = get_embedder()
    store = get_qdrant_store()
    retriever = get_hybrid_retriever(embedder, store)
    llm = get_llm_provider()

    qa_service = get_qa_service(retriever, llm)

    reports_dir = PROJECT_ROOT / "reports"
    datasets_dir = PROJECT_ROOT / "evaluation" / "datasets"
    datasets_dir.mkdir(parents=True, exist_ok=True)

    runner = EvaluationRunner(qa_service, datasets_dir, reports_dir)
    runner.run()


if __name__ == "__main__":
    main()
