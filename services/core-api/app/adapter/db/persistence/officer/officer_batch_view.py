from __future__ import annotations

from sqlalchemy.orm import Session

from .....models.entities import Batch


class OfficerBatchView:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_batches(self, college_id: int | None = None, limit: int = 50) -> list[Batch]:
        q = self._db.query(Batch).order_by(Batch.created_at.desc())
        if college_id is not None:
            q = q.filter(Batch.college_id == college_id)
        return q.limit(limit).all()
