import json
from pathlib import Path
from pydantic import BaseModel


class BenchmarkQuestion(BaseModel):
    question: str
    expected_answer: str
    expected_pages: list[int]


class BenchmarkDataset(BaseModel):
    company: str
    year: str
    questions: list[BenchmarkQuestion]


def load_dataset(filepath: Path) -> BenchmarkDataset:
    with filepath.open() as f:
        data = json.load(f)
    return BenchmarkDataset(**data)


def discover_datasets(datasets_dir: Path) -> list[BenchmarkDataset]:
    datasets = []
    if not datasets_dir.exists():
        return datasets

    for p in datasets_dir.glob("*.json"):
        datasets.append(load_dataset(p))

    return datasets
