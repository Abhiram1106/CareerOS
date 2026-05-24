from __future__ import annotations

from sqlalchemy.orm import Session

from .....models.entities import CareerProfile, Resume, Scorecard, User


class OfficerCohortView:
    """Read path: latest scorecard per student with profile context."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def latest_scorecards_by_student(
        self,
    ) -> list[tuple[Scorecard, Resume, User, CareerProfile | None]]:
        rows = (
            self._db.query(Scorecard, Resume, User, CareerProfile)
            .join(Resume, Scorecard.resume_id == Resume.id)
            .join(User, Resume.user_id == User.id)
            .outerjoin(CareerProfile, CareerProfile.user_id == User.id)
            .order_by(Scorecard.created_at.desc())
            .all()
        )
        latest: dict[int, tuple[Scorecard, Resume, User, CareerProfile | None]] = {}
        for scorecard, resume, user, profile in rows:
            if user.id not in latest:
                latest[user.id] = (scorecard, resume, user, profile)
        return list(latest.values())
