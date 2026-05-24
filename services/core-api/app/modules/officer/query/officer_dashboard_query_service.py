from __future__ import annotations

from sqlalchemy.orm import Session

from ....adapter.db.persistence.officer.officer_cohort_view import OfficerCohortView
from ..dto.officer_dto import OfficerBucketCounts, OfficerCohortKpi, OfficerDashboardResponse


class OfficerDashboardQueryService:
    def __init__(self, db: Session) -> None:
        self._view = OfficerCohortView(db)

    def get_dashboard(self) -> OfficerDashboardResponse:
        rows = self._view.latest_scorecards_by_student()
        if not rows:
            return OfficerDashboardResponse(
                kpis=OfficerCohortKpi(
                    students_scored=0,
                    avg_readiness=0.0,
                    parse_safe_rate=0.0,
                    ready_count=0,
                ),
                buckets=OfficerBucketCounts(strong=0, ready=0, borderline=0, risk=0),
            )

        buckets = OfficerBucketCounts(strong=0, ready=0, borderline=0, risk=0)
        scores: list[float] = []
        ats_scores: list[float] = []

        for scorecard, _resume, _user, _profile in rows:
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

        avg = sum(scores) / len(scores) if scores else 0.0
        parse_safe = (
            sum(1 for s in ats_scores if s >= 70) / len(ats_scores) * 100 if ats_scores else 0.0
        )
        ready_count = buckets.strong + buckets.ready

        return OfficerDashboardResponse(
            kpis=OfficerCohortKpi(
                students_scored=len(rows),
                avg_readiness=round(avg, 1),
                parse_safe_rate=round(parse_safe, 1),
                ready_count=ready_count,
            ),
            buckets=buckets,
        )
