from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from .....models.entities import Batch, BatchResume


class OfficerBatchRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def find_by_id(self, batch_id: int) -> Optional[Batch]:
        return self._db.query(Batch).filter(Batch.id == batch_id).first()

    def create(
        self,
        *,
        college_id: int,
        created_by: int,
        name: str,
        grad_year: int,
        dept_id: int | None,
    ) -> Batch:
        batch = Batch(
            college_id=college_id,
            created_by=created_by,
            name=name,
            grad_year=grad_year,
            dept_id=dept_id,
        )
        self._db.add(batch)
        self._db.commit()
        self._db.refresh(batch)
        return batch

    def link_resume(self, *, batch_id: int, resume_id: int) -> BatchResume:
        row = BatchResume(batch_id=batch_id, resume_id=resume_id, status="uploaded")
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return row
