from __future__ import annotations

from sqlalchemy.orm import Session

from ....adapter.db.persistence.ats.ats_view import ATSView
from ....models.entities import User
from ..dto.ats_dto import ATSScanHistoryItem, ATSScanHistoryResponse


class ATSQueryService:
    def __init__(self, db: Session) -> None:
        self._view = ATSView(db)

    def history_for_user(self, user: User) -> ATSScanHistoryResponse:
        scans = self._view.list_for_user(user.id)
        return ATSScanHistoryResponse(
            scans=[
                ATSScanHistoryItem(
                    id=scan.id,
                    ats_parse_safety=scan.composite_score,
                    created_at=scan.created_at.isoformat(),
                )
                for scan in scans
            ]
        )
