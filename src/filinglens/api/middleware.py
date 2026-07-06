import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from filinglens.utils.logging import get_logger
from filinglens.utils.timer import request_id_ctx_var

logger = get_logger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = str(uuid.uuid4())
        request_id_ctx_var.set(req_id)

        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time
        process_time_ms = process_time * 1000

        response.headers["X-Process-Time"] = str(process_time_ms)

        retrieval_time = getattr(request.state, "retrieval_time", None)
        llm_time = getattr(request.state, "llm_time", None)

        log_extra = {
            "request_id": req_id,
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "latency_ms": process_time_ms,
        }

        if retrieval_time is not None:
            response.headers["X-Retrieval-Time"] = str(retrieval_time)
            log_extra["retrieval_ms"] = retrieval_time

        if llm_time is not None:
            response.headers["X-LLM-Time"] = str(llm_time)
            log_extra["llm_ms"] = llm_time

        logger.info(
            f"{request.method} {request.url.path} - HTTP {response.status_code}",
            extra=log_extra,
        )

        return response
