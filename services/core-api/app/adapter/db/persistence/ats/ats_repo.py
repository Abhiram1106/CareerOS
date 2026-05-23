from __future__ import annotations

from sqlalchemy.orm import Session

from .....models.entities import ATSScan


class ATSRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create_from_parse_safety(self, *, user_id: int, ats_parse_safety: float) -> ATSScan:
        """Persist parse-safety score; legacy columns mirror composite for history UI."""
        row = ATSScan(
            user_id=user_id,
            composite_score=ats_parse_safety,
            keyword_score=0.0,
            format_score=ats_parse_safety,
            quality_score=0.0,
            completeness_score=0.0,
            contact_score=0.0,
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return row
