from __future__ import annotations

from sqlalchemy.orm import Session

from ....models.entities import CareerProfile, Resume, Scorecard, User
from ..dto.officer_dto import (
    OfficerBucketCounts,
    OfficerCohortKpi,
    OfficerCohortResponse,
    OfficerReviewItem,
)


class OfficerCohortQueryService:
    """Aggregate placement readiness across students (demo cohort; college scope in Phase 4+)."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_cohort(self) -> OfficerCohortResponse:
        rows = (
            self._db.query(Scorecard, Resume, User, CareerProfile)
            .join(Resume, Scorecard.resume_id == Resume.id)
            .join(User, Resume.user_id == User.id)
            .outerjoin(CareerProfile, CareerProfile.user_id == User.id)
            .order_by(Scorecard.created_at.desc())
            .all()
        )

        if not rows:
            return OfficerCohortResponse(
                kpis=OfficerCohortKpi(
                    students_scored=0,
                    avg_readiness=0.0,
                    parse_safe_rate=0.0,
                    ready_count=0,
                ),
                buckets=OfficerBucketCounts(strong=0, ready=0, borderline=0, risk=0),
                review_queue=[],
            )

        latest_by_student: dict[int, tuple[Scorecard, Resume, User, CareerProfile | None]] = {}
        for scorecard, resume, user, profile in rows:
            if user.id not in latest_by_student:
                latest_by_student[user.id] = (scorecard, resume, user, profile)

        buckets = OfficerBucketCounts(strong=0, ready=0, borderline=0, risk=0)
        scores: list[float] = []
        ats_scores: list[float] = []
        review: list[OfficerReviewItem] = []

        for scorecard, resume, user, profile in latest_by_student.values():
            scores.append(float(scorecard.overall_score))
            ats_scores.append(float(scorecard.ats_safety))
            bucket = scorecard.bucket or "high-risk"
            if bucket == "strong":
                buckets.strong += 1
            elif bucket == "ready":
                buckets.ready += 1
            elif bucket == "borderline":
                buckets.borderline += 1
            else:
                buckets.risk += 1

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
        avg = sum(scores) / len(scores) if scores else 0.0
        parse_safe = sum(1 for s in ats_scores if s >= 70) / len(ats_scores) * 100 if ats_scores else 0.0
        ready_count = buckets.strong + buckets.ready

        return OfficerCohortResponse(
            kpis=OfficerCohortKpi(
                students_scored=len(latest_by_student),
                avg_readiness=round(avg, 1),
                parse_safe_rate=round(parse_safe, 1),
                ready_count=ready_count,
            ),
            buckets=buckets,
            review_queue=review[:25],
        )
