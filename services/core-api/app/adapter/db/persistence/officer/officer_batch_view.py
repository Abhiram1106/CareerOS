from __future__ import annotations

from sqlalchemy.orm import Session

from .....models.entities import Batch


class OfficerBatchView:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_batches(self, limit: int = 50) -> list[Batch]:
        return (
            self._db.query(Batch)
            .order_by(Batch.created_at.desc())
            .limit(limit)
            .all()
        )
