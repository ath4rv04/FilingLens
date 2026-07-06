from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass
import time
import random
import logging
from ddgs import DDGS

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class SearchResult:
    title: str
    url: str
    snippet: str


class SearchBackend(ABC):
    @abstractmethod
    def search(self, query: str) -> List[SearchResult]:
        pass


class DuckDuckGoBackend(SearchBackend):
    def __init__(self, retries: int = 3, backoff: float = 2.0):
        self.retries = retries
        self.backoff = backoff
        self.ddgs = DDGS()

    def search(self, query: str) -> List[SearchResult]:
        results = []
        for attempt in range(self.retries):
            try:
                # Add human-like random latency protecting DDGS rate limits
                time.sleep(random.uniform(1.5, 3.5))

                raw = list(self.ddgs.text(query, max_results=10))
                for r in raw:
                    results.append(
                        SearchResult(
                            title=r.get("title", ""),
                            url=r.get("href", ""),
                            snippet=r.get("body", ""),
                        )
                    )
                return results
            except Exception as e:
                logger.warning(f"DDGS failure on attempt {attempt + 1}: {e}")
                time.sleep(self.backoff * (2**attempt))

        return results
