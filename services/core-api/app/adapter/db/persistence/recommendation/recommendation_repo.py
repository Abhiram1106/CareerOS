from __future__ import annotations

import json
from typing import Optional

from sqlalchemy.orm import Session

from .....models.entities import Recommendation, Scorecard


class RecommendationRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def delete_for_scorecard(self, scorecard_id: int) -> None:
        self._db.query(Recommendation).filter(Recommendation.scorecard_id == scorecard_id).delete()
        self._db.commit()

    def list_for_scorecard(self, scorecard_id: int) -> list[Recommendation]:
        return (
            self._db.query(Recommendation)
            .filter(Recommendation.scorecard_id == scorecard_id)
            .order_by(Recommendation.id.asc())
            .all()
        )

    def find_by_id_for_user(self, rec_id: int, user_id: int) -> Optional[Recommendation]:
        """Find a recommendation belonging to the given user (via scorecard → resume)."""
        return (
            self._db.query(Recommendation)
            .join(Scorecard, Scorecard.id == Recommendation.scorecard_id)
            .filter(
                Recommendation.id == rec_id,
                Scorecard.resume_id.isnot(None),
            )
            .first()
        )

    def set_feedback(self, rec_id: int, accepted: bool) -> Optional[Recommendation]:
        """Record whether the student accepted or rejected this recommendation."""
        row = self._db.query(Recommendation).filter(Recommendation.id == rec_id).first()
        if not row:
            return None
        row.accepted = accepted
        self._db.commit()
        self._db.refresh(row)
        return row

    def add_rows(self, rows: list[Recommendation]) -> None:
        for row in rows:
            self._db.add(row)
        self._db.commit()

    @staticmethod
    def evidence_ids_json(ids: list[str]) -> str:
        return json.dumps(ids)
