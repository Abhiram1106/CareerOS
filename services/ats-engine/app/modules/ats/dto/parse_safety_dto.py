from __future__ import annotations

from pydantic import BaseModel, Field


class ParseSafetyRequest(BaseModel):
    ats_flags: list[str] = Field(default_factory=list)
    resume_text: str = ""


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


class ParseSafetyResponse(BaseModel):
    ats_parse_safety: float
    bucket: str
    checks: list[ATSCheck] = Field(default_factory=list)
    issues: list[ATSIssue] = Field(default_factory=list)
    penalties: dict[str, int] = Field(default_factory=dict)
    unknown_flags: list[str] = Field(default_factory=list)
