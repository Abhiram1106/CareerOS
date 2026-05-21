from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy.orm import Session

from .....models.entities import ResumeSection


class ResumeSectionRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def add_sections(self, resume_id: int, sections: list[dict]) -> None:
        for sec in sections:
            content = sec.get("content_json", {})
            self._db.add(
                ResumeSection(
                    resume_id=resume_id,
                    section_name=sec["section_name"],
                    content_json=json.dumps(content),
                    confidence=sec.get("confidence", 1.0),
                    created_at=datetime.utcnow(),
                )
            )
        self._db.commit()
