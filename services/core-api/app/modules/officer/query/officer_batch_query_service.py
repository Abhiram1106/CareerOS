from __future__ import annotations

from sqlalchemy.orm import Session

from ....adapter.db.persistence.officer.officer_batch_view import OfficerBatchView
from ..dto.officer_dto import OfficerBatchItem, OfficerBatchListResponse
from ..officer_scope import resolve_officer_college_id


class OfficerBatchQueryService:
    def __init__(self, db: Session) -> None:
        self._view = OfficerBatchView(db)
        self._college_id = resolve_officer_college_id(db)

    def list_batches(self) -> OfficerBatchListResponse:
        batches = self._view.list_batches(self._college_id)
        items = [
            OfficerBatchItem(
                id=batch.id,
                name=batch.name,
                grad_year=batch.grad_year,
                college_id=batch.college_id,
                dept_id=batch.dept_id,
                created_at=batch.created_at.isoformat(),
            )
            for batch in batches
        ]
        return OfficerBatchListResponse(batches=items)
