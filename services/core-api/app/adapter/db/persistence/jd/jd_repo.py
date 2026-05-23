from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from .....models.entities import JobDescription


class JDRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def find_by_id(self, jd_id: int) -> Optional[JobDescription]:
        return self._db.query(JobDescription).filter(JobDescription.id == jd_id).first()

    def create(
        self,
        *,
        created_by: int,
        college_id: int | None,
        company: str,
        role: str,
        raw_text: str,
        skills_json: str,
        eligibility_json: str,
    ) -> JobDescription:
        row = JobDescription(
            created_by=created_by,
            college_id=college_id,
            company=company,
            role=role,
            raw_text=raw_text,
            skills_json=skills_json,
            eligibility_json=eligibility_json,
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return row
