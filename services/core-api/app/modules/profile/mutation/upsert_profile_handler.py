from __future__ import annotations

from sqlalchemy.orm import Session

from ....adapter.db.persistence.profile.profile_repo import ProfileRepo
from ....models.entities import User
from ..dto.profile_dto import ProfileUpdateResponse, ProfileUpsert


class UpsertProfileHandler:
    def __init__(self, db: Session) -> None:
        self._profiles = ProfileRepo(db)

    def execute(self, user: User, payload: ProfileUpsert) -> dict:
        self._profiles.upsert_for_user(
            user_id=user.id,
            city=payload.city,
            professional_status=payload.professional_status,
            target_role=payload.target_role,
            skills_csv=payload.skills_csv,
            summary=payload.summary,
            experience_bullet=payload.experience_bullet,
            cgpa=payload.cgpa,
            active_backlogs=payload.active_backlogs,
            branch=payload.branch,
            grad_year=payload.grad_year,
        )
        return ProfileUpdateResponse().model_dump()
