from __future__ import annotations

from sqlalchemy.orm import Session

from ....adapter.db.persistence.officer.officer_cohort_view import OfficerCohortView
from ..dto.officer_dto import OfficerReviewItem, OfficerReviewListResponse
from ..officer_scope import resolve_officer_college_id


class OfficerReviewQueryService:
    def __init__(self, db: Session) -> None:
        self._view = OfficerCohortView(db)
        self._college_id = resolve_officer_college_id(db)

    def get_review_queue(self, limit: int = 50) -> OfficerReviewListResponse:
        rows = self._view.latest_scorecards_by_student(self._college_id)
        review: list[OfficerReviewItem] = []

        for scorecard, resume, user, profile in rows:
            bucket = scorecard.bucket or "high-risk"
            review.append(
                OfficerReviewItem(
                    student_name=user.full_name or user.email,
                    target_role=(profile.target_role if profile else "") or "—",
                    overall_score=float(scorecard.overall_score),
                    bucket=bucket,
                    scorecard_id=scorecard.id,
                    resume_id=resume.id,
                )
            )

        review.sort(key=lambda item: item.overall_score)
        return OfficerReviewListResponse(items=review[:limit])
