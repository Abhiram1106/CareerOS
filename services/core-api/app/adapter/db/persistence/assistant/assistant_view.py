from __future__ import annotations

from sqlalchemy.orm import Session

from .....models.entities import Resume, Scorecard


class AssistantView:
    def __init__(self, db: Session) -> None:
        self._db = db

    def latest_scorecard_for_user(self, user_id: int) -> Scorecard | None:
        return (
            self._db.query(Scorecard)
            .join(Resume, Resume.id == Scorecard.resume_id)
            .filter(Resume.user_id == user_id)
            .order_by(Scorecard.id.desc())
            .first()
        )
