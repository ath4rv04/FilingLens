import time
import logging
from types import TracebackType

logger = logging.getLogger(__name__)

class Timer:
    """Context manager for measuring execution latency."""

    def __init__(self) -> None:
        self.start: float = 0.0
        self.end_time: float = 0.0
        self.elapsed_ms: float = 0.0

    def __enter__(self) -> "Timer":
        self.start = time.perf_counter()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.end_time = time.perf_counter()
        self.elapsed_ms = (self.end_time - self.start) * 1000
