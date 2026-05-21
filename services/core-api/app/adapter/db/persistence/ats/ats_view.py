from __future__ import annotations

from sqlalchemy.orm import Session

from .....models.entities import ATSScan


class ATSView:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_for_user(self, user_id: int) -> list[ATSScan]:
        return (
            self._db.query(ATSScan)
            .filter(ATSScan.user_id == user_id)
            .order_by(ATSScan.created_at.desc())
            .all()
        )

    def all_for_user(self, user_id: int) -> list[ATSScan]:
        return self._db.query(ATSScan).filter(ATSScan.user_id == user_id).all()
