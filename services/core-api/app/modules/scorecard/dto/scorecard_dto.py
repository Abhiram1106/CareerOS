from __future__ import annotations

from pydantic import BaseModel, Field


class ScorecardScoreRequest(BaseModel):
    resume_id: int
    jd_text: str = Field(min_length=20)
    jd_id: int | None = None
    company: str = ""
    role: str = ""
    ats_flags: list[str] = Field(default_factory=list)
    college_id: int | None = None


class ScoreComponents(BaseModel):
    jd_match: float
    ats_safety: float
    evidence: float
    completeness: float
    interview: float
    hygiene: float


class ScorecardScoreResponse(BaseModel):
    scorecard_id: int
    jd_id: int
    overall_score: float
    bucket: str
    components: ScoreComponents
    raw: dict
    missing_required_skills: list[str]
    matched_skills: list[str]
    semantic_method: str = "char_ngram_proxy"
