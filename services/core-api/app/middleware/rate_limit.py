from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Callable

from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from ..config import RATE_LIMIT_ENABLED, RATE_LIMIT_MAX_REQUESTS, RATE_LIMIT_WINDOW_SECONDS


def _client_key(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple sliding-window rate limiter (in-process; use Redis at scale)."""

    _buckets: dict[str, deque[float]] = defaultdict(deque)

    def __init__(
        self,
        app,
        *,
        path_prefixes: tuple[str, ...] = (
            "/auth/login",
            "/auth/register",
            "/agent/run",
            "/resumes/upload",
            "/assistant/chat",
            "/officer/batches",
        ),
    ) -> None:
        super().__init__(app)
        self._path_prefixes = path_prefixes

    def _is_limited_path(self, path: str) -> bool:
        return any(path.startswith(prefix) for prefix in self._path_prefixes)

    def _check(self, key: str) -> None:
        now = time.monotonic()
        window = RATE_LIMIT_WINDOW_SECONDS
        bucket = self._buckets[key]
        while bucket and now - bucket[0] > window:
            bucket.popleft()
        if len(bucket) >= RATE_LIMIT_MAX_REQUESTS:
            raise HTTPException(status_code=429, detail="Rate limit exceeded — try again shortly")
        bucket.append(now)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not RATE_LIMIT_ENABLED or request.method == "OPTIONS":
            return await call_next(request)
        if not self._is_limited_path(request.url.path):
            return await call_next(request)
        key = f"{_client_key(request)}:{request.url.path}"
        self._check(key)
        return await call_next(request)
