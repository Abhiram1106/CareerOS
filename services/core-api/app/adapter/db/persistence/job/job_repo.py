from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from .....models.entities import Job


class JobRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def find_by_id(self, job_id: int) -> Optional[Job]:
        return self._db.query(Job).filter(Job.id == job_id).first()

    def find_by_external_id(self, external_id: str) -> Optional[Job]:
        return self._db.query(Job).filter(Job.external_id == external_id).first()

    def upsert_from_feed(self, row: dict, ttl_hours: int = 24) -> Job:
        external_id = str(row.get("external_id", "")).strip()
        existing = self.find_by_external_id(external_id) if external_id else None

        skills = row.get("skills_required", [])
        if not isinstance(skills, list):
            skills = []
        skills_json = json.dumps([str(s) for s in skills])
        now = datetime.utcnow()
        expires = now + timedelta(hours=ttl_hours)

        if existing:
            existing.source = str(row.get("source", existing.source or "seed"))
            existing.title = str(row.get("title", existing.title or "")).strip()
            existing.company = str(row.get("company", existing.company or "")).strip()
            existing.location = str(row.get("location", existing.location or "")).strip()
            existing.skills_required = skills_json
            existing.raw_jd_text = str(row.get("raw_jd_text", existing.raw_jd_text or "")).strip()
            existing.fetched_at = now
            existing.expires_at = expires
            self._db.commit()
            self._db.refresh(existing)
            return existing

        created = Job(
            source=str(row.get("source", "seed")),
            external_id=external_id or f"seed-{int(now.timestamp())}",
            title=str(row.get("title", "")).strip(),
            company=str(row.get("company", "")).strip(),
            location=str(row.get("location", "")).strip(),
            skills_required=skills_json,
            raw_jd_text=str(row.get("raw_jd_text", "")).strip(),
            fetched_at=now,
            expires_at=expires,
        )
        self._db.add(created)
        self._db.commit()
        self._db.refresh(created)
        return created
