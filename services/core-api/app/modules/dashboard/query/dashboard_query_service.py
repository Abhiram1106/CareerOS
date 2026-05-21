from __future__ import annotations

from sqlalchemy.orm import Session

from ....adapter.db.persistence.dashboard.dashboard_view import DashboardView
from ....models.entities import User
from ..dto.dashboard_dto import DashboardResponse


class DashboardQueryService:
    def __init__(self, db: Session) -> None:
        self._view = DashboardView(db)

    def get_for_user(self, user: User) -> DashboardResponse:
        profile = self._view.profile_for_user(user.id)
        scans = self._view.scans_for_user(user.id)
        resumes_count = self._view.resume_count_for_user(user.id)
        best_ats = max((s.composite_score for s in scans), default=0)
        if profile is None:
            profile_completeness = 0
        else:
            fields = [
                profile.city,
                profile.professional_status,
                profile.target_role,
                profile.skills_csv,
                profile.summary,
                profile.experience_bullet,
            ]
            profile_completeness = round(100 * (sum(1 for f in fields if f) / len(fields)))
        return DashboardResponse(
            best_ats_score=best_ats,
            total_resumes=resumes_count,
            scans_performed=len(scans),
            profile_completeness=profile_completeness,
        )
