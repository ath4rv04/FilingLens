import time
import logging
from types import TracebackType
from contextvars import ContextVar

logger = logging.getLogger(__name__)

request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="")


class Timer:
    """Context manager for measuring execution latency across distinct modules."""

    def __init__(self, name: str = "operation") -> None:
        self.name = name
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
        logger.info(
            f"Finished {self.name}",
            extra={
                "component": self.name,
                "latency_ms": self.elapsed_ms,
                "request_id": request_id_ctx_var.get(),
            },
        )
