from __future__ import annotations

from pydantic import BaseModel, Field


class RunRewriteRequest(BaseModel):
    scorecard_id: int


class RecommendationItem(BaseModel):
    id: int
    rec_type: str
    section: str
    before_text: str
    after_text: str
    evidence_ids: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    accepted: bool | None = None


class RunRewriteResponse(BaseModel):
    scorecard_id: int
    top_issues: list[dict] = Field(default_factory=list)
    section_rewrites: list[dict] = Field(default_factory=list)
    unsupported_claims: list[dict] = Field(default_factory=list)
    requires_confirmation: list[dict] = Field(default_factory=list)
    recommendations: list[RecommendationItem] = Field(default_factory=list)
