from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

from .cache import get_cached_jobs, set_cached_jobs
from .clients.adzuna import search_adzuna_jobs

app = FastAPI(title="CareerOS Jobs Feed", version="0.1.0")

# Default matches docker-compose volume: ./infra/seed → /app/infra/seed
SEED_PATH = Path(os.getenv("JOBS_SEED_PATH", "/app/infra/seed/jobs.seed.json"))


def _seed_jobs() -> list[dict]:
    if not SEED_PATH.exists():
        return []
    with SEED_PATH.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    if isinstance(raw, list):
        return raw
    return []


def _local_search(seed_rows: list[dict], query: str, location: str, page: int, page_size: int = 20) -> dict:
    q = query.strip().lower()
    loc = location.strip().lower()

    def _matches(row: dict) -> bool:
        title = str(row.get("title", "")).lower()
        company = str(row.get("company", "")).lower()
        jd = str(row.get("raw_jd_text", "")).lower()
        row_loc = str(row.get("location", "")).lower()
        query_ok = not q or q in title or q in company or q in jd
        loc_ok = not loc or loc in row_loc
        return query_ok and loc_ok

    filtered = [row for row in seed_rows if _matches(row)]
    start = max(page - 1, 0) * page_size
    end = start + page_size
    return {
        "source": "seed",
        "total": len(filtered),
        "page": page,
        "page_size": page_size,
        "results": filtered[start:end],
    }


def _find_seed_job(external_id: str) -> dict | None:
    for row in _seed_jobs():
        if str(row.get("external_id", "")).strip() == external_id:
            return row
    return None


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "jobs-feed"}


@app.get("/jobs/search")
async def jobs_search(
    q: str = Query(default="", min_length=0, max_length=120),
    loc: str = Query(default="", min_length=0, max_length=120),
    page: int = Query(default=1, ge=1, le=50),
) -> dict:
    cache_key = f"jobs:search:q={q.strip().lower()}:loc={loc.strip().lower()}:p={page}"
    cached = await get_cached_jobs(cache_key)
    if cached is not None:
        return {"cached": True, **cached}

    app_id = os.getenv("ADZUNA_APP_ID", "")
    app_key = os.getenv("ADZUNA_APP_KEY", "")

    if app_id and app_key:
        remote = await search_adzuna_jobs(query=q, location=loc, page=page, app_id=app_id, app_key=app_key)
        await set_cached_jobs(cache_key, remote, ttl_seconds=86400)
        return {"cached": False, **remote}

    fallback = _local_search(_seed_jobs(), query=q, location=loc, page=page)
    await set_cached_jobs(cache_key, fallback, ttl_seconds=86400)
    return {"cached": False, **fallback}


@app.get("/jobs/{external_id}")
async def job_detail(external_id: str) -> dict:
    cache_key = f"jobs:get:{external_id}"
    cached = await get_cached_jobs(cache_key)
    if cached is not None:
        return {"cached": True, **cached}

    found = _find_seed_job(external_id)
    if not found:
        raise HTTPException(status_code=404, detail="Job not found")

    payload = {"source": "seed", "job": found}
    await set_cached_jobs(cache_key, payload, ttl_seconds=86400)
    return {"cached": False, **payload}
