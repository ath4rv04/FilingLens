from dataclasses import dataclass


@dataclass(slots=True)
class DocumentMetadata:
    page_count: int

    title: str | None

    author: str | None

    producer: str | None

    creator: str | None
