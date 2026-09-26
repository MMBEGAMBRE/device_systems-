import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        response = await call_next(request)

        process_time = time.perf_counter() - start_time
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-API-Version"] = "4.0"
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-Request-ID"] = request_id

        print(f"{request.method} {request.url.path} -> {response.status_code} ({process_time:.4f}s)")
        return response
