from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


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


class OfficerHeatmapRow(BaseModel):
    name: str
    strong: int
    ready: int
    borderline: int
    risk: int


class OfficerHeatmapResponse(BaseModel):
    departments: list[OfficerHeatmapRow]


class OfficerSkillGapItem(BaseModel):
    skill: str
    student_count: int


class OfficerSkillGapsResponse(BaseModel):
    items: list[OfficerSkillGapItem]


class OfficerCreateBatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=200)
    grad_year: int = Field(ge=2020, le=2035)
    dept_id: int | None = None


class OfficerCreateBatchResponse(BaseModel):
    batch: OfficerBatchItem


class OfficerBatchUploadResult(BaseModel):
    batch_id: int
    uploaded: int
    resume_ids: list[int]
    errors: list[str]
