from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from .....models.entities import CareerProfile, User


class ProfileRepo:
    """Write-side persistence for career profiles."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def find_by_user_id(self, user_id: int) -> Optional[CareerProfile]:
        return self._db.query(CareerProfile).filter(CareerProfile.user_id == user_id).first()

    def create_default_for_user(self, user: User) -> CareerProfile:
        profile = CareerProfile(user_id=user.id)
        self._db.add(profile)
        self._db.commit()
        self._db.refresh(profile)
        return profile

    def upsert_for_user(
        self,
        *,
        user_id: int,
        city: str,
        professional_status: str,
        target_role: str,
        skills_csv: str,
        summary: str,
        experience_bullet: str,
        cgpa: float | None = None,
        active_backlogs: int = 0,
        branch: str = "",
        grad_year: int | None = None,
    ) -> CareerProfile:
        profile = self.find_by_user_id(user_id)
        if profile is None:
            profile = CareerProfile(user_id=user_id)
            self._db.add(profile)

        profile.city = city
        profile.professional_status = professional_status
        profile.target_role = target_role
        profile.skills_csv = skills_csv
        profile.summary = summary
        profile.experience_bullet = experience_bullet
        profile.cgpa = cgpa
        profile.active_backlogs = active_backlogs
        profile.branch = branch
        profile.grad_year = grad_year
        self._db.commit()
        self._db.refresh(profile)
        return profile
