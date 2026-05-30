from __future__ import annotations

from typing import Optional

from ....models.entities import CareerProfile, User
from ..dto.profile_dto import ProfileResponse

_DEFAULT_STATUS = "Fresher"
_DEFAULT_ROLE = "Software Engineer"


def profile_fields_for_scan(user: User, profile: Optional[CareerProfile]) -> dict[str, str]:
    if profile is None:
        return {
            "full_name": user.full_name,
            "email": user.email,
            "city": "",
            "target_role": _DEFAULT_ROLE,
            "skills_csv": "",
            "summary": "",
            "experience_bullet": "",
        }
    return {
        "full_name": user.full_name,
        "email": user.email,
        "city": profile.city,
        "target_role": profile.target_role,
        "skills_csv": profile.skills_csv,
        "summary": profile.summary,
        "experience_bullet": profile.experience_bullet,
    }


def to_profile_response(user: User, profile: Optional[CareerProfile]) -> ProfileResponse:
    if profile is None:
        return ProfileResponse(
            full_name=user.full_name,
            email=user.email,
            city="",
            professional_status=_DEFAULT_STATUS,
            target_role=_DEFAULT_ROLE,
            skills_csv="",
            summary="",
            experience_bullet="",
        )
    return ProfileResponse(
        full_name=user.full_name,
        email=user.email,
        city=profile.city,
        professional_status=profile.professional_status,
        target_role=profile.target_role,
        skills_csv=profile.skills_csv,
        summary=profile.summary,
        experience_bullet=profile.experience_bullet,
        cgpa=profile.cgpa,
        active_backlogs=profile.active_backlogs,
        branch=profile.branch,
        grad_year=profile.grad_year,
    )
