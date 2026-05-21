from __future__ import annotations

import json
from typing import Optional

from sqlalchemy.orm import Session

from .....models.entities import Resume, ResumeSection


class ResumeView:
    def __init__(self, db: Session) -> None:
        self._db = db

    def find_by_id_for_user(self, resume_id: int, user_id: int) -> Optional[Resume]:
        return (
            self._db.query(Resume)
            .filter(Resume.id == resume_id, Resume.user_id == user_id)
            .first()
        )

    def list_for_user(self, user_id: int) -> list[Resume]:
        return (
            self._db.query(Resume)
            .filter(Resume.user_id == user_id)
            .order_by(Resume.created_at.desc())
            .all()
        )

    def sections_for_resume(self, resume_id: int) -> list[ResumeSection]:
        return self._db.query(ResumeSection).filter(ResumeSection.resume_id == resume_id).all()

    @staticmethod
    def parse_section_content(raw: str) -> dict:
        if not raw:
            return {}
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}
