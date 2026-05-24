from __future__ import annotations

from sqlalchemy.orm import Session

from .....models.entities import (
    Batch,
    BatchResume,
    CareerProfile,
    Department,
    JobDescription,
    Resume,
    Scorecard,
    User,
)


class OfficerCohortView:
    """Read path: latest scorecard per student with profile context."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def latest_scorecards_by_student(
        self,
        college_id: int | None = None,
    ) -> list[tuple[Scorecard, Resume, User, CareerProfile | None]]:
        rows = (
            self._db.query(Scorecard, Resume, User, CareerProfile)
            .join(Resume, Scorecard.resume_id == Resume.id)
            .join(User, Resume.user_id == User.id)
            .outerjoin(CareerProfile, CareerProfile.user_id == User.id)
            .order_by(Scorecard.created_at.desc())
            .all()
        )
        if college_id is not None:
            allowed_user_ids = self._user_ids_for_college(college_id)
            rows = [row for row in rows if row[2].id in allowed_user_ids]

        latest: dict[int, tuple[Scorecard, Resume, User, CareerProfile | None]] = {}
        for scorecard, resume, user, profile in rows:
            if user.id not in latest:
                latest[user.id] = (scorecard, resume, user, profile)
        return list(latest.values())

    def _user_ids_for_college(self, college_id: int) -> set[int]:
        batch_user_ids = {
            uid
            for (uid,) in self._db.query(Resume.user_id)
            .join(BatchResume, BatchResume.resume_id == Resume.id)
            .join(Batch, Batch.id == BatchResume.batch_id)
            .filter(Batch.college_id == college_id)
            .distinct()
            .all()
        }
        jd_user_ids = {
            uid
            for (uid,) in self._db.query(Resume.user_id)
            .join(Scorecard, Scorecard.resume_id == Resume.id)
            .join(JobDescription, JobDescription.id == Scorecard.jd_id)
            .filter(JobDescription.college_id == college_id)
            .distinct()
            .all()
        }
        return batch_user_ids | jd_user_ids

    def department_for_user(self, user_id: int, college_id: int | None) -> str:
        row = (
            self._db.query(Department.name)
            .join(Batch, Batch.dept_id == Department.id)
            .join(BatchResume, BatchResume.batch_id == Batch.id)
            .join(Resume, Resume.id == BatchResume.resume_id)
            .filter(Resume.user_id == user_id)
            .order_by(BatchResume.created_at.desc())
            .first()
        )
        if row:
            return row[0]
        profile = self._db.query(CareerProfile).filter(CareerProfile.user_id == user_id).first()
        if profile and profile.target_role:
            return profile.target_role
        return "Unassigned"
