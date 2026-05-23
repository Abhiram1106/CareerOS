from __future__ import annotations

import json

from sqlalchemy.orm import Session

from .....models.entities import Recommendation


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

    def add_rows(self, rows: list[Recommendation]) -> None:
        for row in rows:
            self._db.add(row)
        self._db.commit()

    @staticmethod
    def evidence_ids_json(ids: list[str]) -> str:
        return json.dumps(ids)
