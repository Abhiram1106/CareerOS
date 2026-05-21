from __future__ import annotations

from sqlalchemy.orm import Session

from .....models.entities import ATSScan


class ATSRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create_from_scan_result(self, *, user_id: int, result: dict[str, float]) -> ATSScan:
        row = ATSScan(
            user_id=user_id,
            composite_score=result["composite"],
            keyword_score=result["keyword"],
            format_score=result["format"],
            quality_score=result["quality"],
            completeness_score=result["complete"],
            contact_score=result["contact"],
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return row
