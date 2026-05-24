from __future__ import annotations

from sqlalchemy.orm import Session

from ..dto.officer_dto import OfficerCohortResponse
from .officer_dashboard_query_service import OfficerDashboardQueryService
from .officer_review_query_service import OfficerReviewQueryService


class OfficerCohortQueryService:
    """Composes dashboard + review read models (legacy `/officer/cohort`)."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_cohort(self) -> OfficerCohortResponse:
        dashboard = OfficerDashboardQueryService(self._db).get_dashboard()
        review = OfficerReviewQueryService(self._db).get_review_queue()
        return OfficerCohortResponse(
            kpis=dashboard.kpis,
            buckets=dashboard.buckets,
            review_queue=review.items,
        )
