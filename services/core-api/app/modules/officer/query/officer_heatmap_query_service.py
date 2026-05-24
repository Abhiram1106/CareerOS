from __future__ import annotations

from sqlalchemy.orm import Session

from ....adapter.db.persistence.officer.officer_cohort_view import OfficerCohortView
from ..dto.officer_dto import OfficerBucketCounts, OfficerHeatmapResponse, OfficerHeatmapRow
from ..officer_scope import resolve_officer_college_id


def _bucket_key(bucket: str) -> str:
    if bucket == "strong":
        return "strong"
    if bucket == "ready":
        return "ready"
    if bucket == "borderline":
        return "borderline"
    return "risk"


class OfficerHeatmapQueryService:
    def __init__(self, db: Session) -> None:
        self._view = OfficerCohortView(db)
        self._college_id = resolve_officer_college_id(db)

    def get_heatmap(self) -> OfficerHeatmapResponse:
        rows = self._view.latest_scorecards_by_student(self._college_id)
        matrix: dict[str, dict[str, int]] = {}

        for scorecard, _resume, user, _profile in rows:
            dept = self._view.department_for_user(user.id, self._college_id)
            bucket = _bucket_key(scorecard.bucket or "high-risk")
            if dept not in matrix:
                matrix[dept] = {"strong": 0, "ready": 0, "borderline": 0, "risk": 0}
            matrix[dept][bucket] += 1

        departments = [
            OfficerHeatmapRow(
                name=name,
                strong=counts["strong"],
                ready=counts["ready"],
                borderline=counts["borderline"],
                risk=counts["risk"],
            )
            for name, counts in sorted(matrix.items(), key=lambda item: item[0].lower())
        ]
        return OfficerHeatmapResponse(departments=departments)
