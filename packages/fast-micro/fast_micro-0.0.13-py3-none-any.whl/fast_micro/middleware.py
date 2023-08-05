import time
from typing import Callable, List

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fast_micro.constants import HEADER_PROCESS_TIME
from fast_micro.logger import get_logger


logger = get_logger(__name__)

class RequestEncrichMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, skip_routes: List[str] = None) -> None:
        self.skip_routes = skip_routes if skip_routes else []
        super().__init__(app)

    def _should_be_skipped(self, request: Request) -> bool:
        return any(path for path in self.skip_routes if request.url.path.startswith(path))

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if self._should_be_skipped(request):
            return await call_next(request)

        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers[HEADER_PROCESS_TIME] = str(process_time)

        logger.info("request", method=request.method, url=request.url._url, status_code=response.status_code, process_time=f"{process_time:0.6f}")

        return response
