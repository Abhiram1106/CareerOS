from __future__ import annotations

from pydantic import BaseModel, Field

from ...common.dto.strict import StrictModel


class ScorecardScoreRequest(StrictModel):
    resume_id: int
    jd_text: str = Field(min_length=20)
    jd_id: int | None = None
    company: str = ""
    role: str = ""
    ats_flags: list[str] = Field(default_factory=list)


class ScoreComponents(BaseModel):
    jd_match: float
    ats_safety: float
    evidence: float
    completeness: float
    interview: float
    hygiene: float


class ATSCheck(BaseModel):
    key: str
    label: str
    score: float
    weight: float
    status: str


class ATSIssue(BaseModel):
    id: str
    dimension: str
    severity: str
    message: str
    fix: str


class VendorScore(BaseModel):
    id: str
    name: str
    score: float
    weight_pct: int


class VendorSimulation(BaseModel):
    composite_score: float
    vendors: list[VendorScore]


class KeywordItem(BaseModel):
    keyword: str
    context: str = ""
    frequency: int = 1  # times keyword appears in JD


class MissingKeyword(BaseModel):
    keyword: str
    importance: str  # "high" | "medium" | "low"
    frequency: int = 1  # times keyword appears in JD


class KeywordGap(BaseModel):
    matched: list[KeywordItem] = Field(default_factory=list)
    missing: list[MissingKeyword] = Field(default_factory=list)
    match_rate: float = 0.0
    total_jd_keywords: int = 0


class QualityClassInfo(BaseModel):
    """CARE-RAG Layer 2: diagnostic resume quality classification."""
    key: str        # machine key e.g. "impact_weak"
    label: str      # human label e.g. "Impact Weak"
    guidance: str   # actionable fix e.g. "Add numbers and outcomes..."


class ScorecardScoreResponse(BaseModel):
    scorecard_id: int
    jd_id: int
    overall_score: float
    bucket: str
    quality_class: QualityClassInfo | None = None   # CARE-RAG Layer 2
    components: ScoreComponents
    raw: dict
    missing_required_skills: list[str]
    matched_skills: list[str]
    semantic_method: str = "char_ngram_proxy"
    ats_bucket: str = ""
    ats_checks: list[ATSCheck] = Field(default_factory=list)
    ats_issues: list[ATSIssue] = Field(default_factory=list)
    vendor_simulation: VendorSimulation | None = None
    keyword_gap: KeywordGap | None = None
