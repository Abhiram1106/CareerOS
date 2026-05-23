from __future__ import annotations

import json

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...adapter.db.persistence.job.job_repo import JobRepo
from ...database import get_db
from ...dependencies import require_student
from ...services.clients import jobs_feed_search

router = APIRouter()


@router.get("/jobs/search")
async def search_jobs(
    q: str = Query(default="", min_length=0, max_length=120),
    loc: str = Query(default="", min_length=0, max_length=120),
    page: int = Query(default=1, ge=1, le=50),
    _user=Depends(require_student),
    db: Session = Depends(get_db),
):
    feed = await jobs_feed_search(q, loc, page=page)
    rows = feed.get("results", [])
    if not isinstance(rows, list):
        rows = []
    repo = JobRepo(db)
    persisted = [repo.upsert_from_feed(row) for row in rows if isinstance(row, dict)]

    return {
        "source": str(feed.get("source", "unknown")),
        "total": int(feed.get("total", len(persisted))),
        "page": int(feed.get("page", page)),
        "page_size": int(feed.get("page_size", 20)),
        "results": [
            {
                "id": item.id,
                "source": item.source,
                "external_id": item.external_id,
                "title": item.title,
                "company": item.company,
                "location": item.location,
                "skills_required": json.loads(item.skills_required or "[]"),
                "raw_jd_text": item.raw_jd_text,
            }
            for item in persisted
        ],
    }
