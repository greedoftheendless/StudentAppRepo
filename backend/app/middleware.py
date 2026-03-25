import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.metrics import HTTP_REQUESTS_TOTAL, HTTP_REQUEST_DURATION


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path == "/metrics":
            return await call_next(request)

        method = request.method
        handler = request.url.path

        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        status_code = str(response.status_code)

        HTTP_REQUESTS_TOTAL.labels(method=method, handler=handler, status=status_code).inc()
        HTTP_REQUEST_DURATION.labels(method=method, handler=handler).observe(duration)

        return response
