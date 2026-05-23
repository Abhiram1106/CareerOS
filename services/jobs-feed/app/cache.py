from __future__ import annotations

import json
import os
from typing import Any

from redis.asyncio import Redis

_redis_client: Redis | None = None


def _redis() -> Redis | None:
    global _redis_client
    redis_url = os.getenv("REDIS_URL", "").strip()
    if not redis_url:
        return None
    if _redis_client is None:
        _redis_client = Redis.from_url(redis_url, decode_responses=True)
    return _redis_client


async def get_cached_jobs(cache_key: str) -> dict[str, Any] | None:
    client = _redis()
    if client is None:
        return None
    raw = await client.get(cache_key)
    if not raw:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


async def set_cached_jobs(cache_key: str, payload: dict[str, Any], ttl_seconds: int) -> None:
    client = _redis()
    if client is None:
        return
    await client.set(cache_key, json.dumps(payload), ex=ttl_seconds)
