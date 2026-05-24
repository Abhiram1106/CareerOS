from __future__ import annotations

from pydantic import BaseModel


class OfficerCohortKpi(BaseModel):
    students_scored: int
    avg_readiness: float
    parse_safe_rate: float
    ready_count: int


class OfficerBucketCounts(BaseModel):
    strong: int
    ready: int
    borderline: int
    risk: int


class OfficerReviewItem(BaseModel):
    student_name: str
    target_role: str
    overall_score: float
    bucket: str
    scorecard_id: int
    resume_id: int


class OfficerDashboardResponse(BaseModel):
    kpis: OfficerCohortKpi
    buckets: OfficerBucketCounts


class OfficerReviewListResponse(BaseModel):
    items: list[OfficerReviewItem]


class OfficerBatchItem(BaseModel):
    id: int
    name: str
    grad_year: int
    college_id: int
    dept_id: int | None
    created_at: str


class OfficerBatchListResponse(BaseModel):
    batches: list[OfficerBatchItem]


class OfficerCohortResponse(BaseModel):
    """Legacy aggregate for clients that fetch dashboard + queue in one call."""

    kpis: OfficerCohortKpi
    buckets: OfficerBucketCounts
    review_queue: list[OfficerReviewItem]
