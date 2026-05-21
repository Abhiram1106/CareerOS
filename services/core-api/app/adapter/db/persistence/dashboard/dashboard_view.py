from __future__ import annotations

from sqlalchemy.orm import Session

from .....models.entities import ATSScan, CareerProfile, Resume


class DashboardView:
    def __init__(self, db: Session) -> None:
        self._db = db

    def profile_for_user(self, user_id: int) -> CareerProfile | None:
        return self._db.query(CareerProfile).filter(CareerProfile.user_id == user_id).first()

    def scans_for_user(self, user_id: int) -> list[ATSScan]:
        return self._db.query(ATSScan).filter(ATSScan.user_id == user_id).all()

    def resume_count_for_user(self, user_id: int) -> int:
        return self._db.query(Resume).filter(Resume.user_id == user_id).count()
