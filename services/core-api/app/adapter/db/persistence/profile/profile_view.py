from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from .....models.entities import CareerProfile


class ProfileView:
    """Read-side persistence for career profiles."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def find_by_user_id(self, user_id: int) -> Optional[CareerProfile]:
        return self._db.query(CareerProfile).filter(CareerProfile.user_id == user_id).first()
