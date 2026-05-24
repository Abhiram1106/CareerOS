from __future__ import annotations

from pydantic import BaseModel, Field

from ...common.dto.strict import StrictModel


class ATSParseSafetyRequest(StrictModel):
    """ATS parse-safety only — flags from resume-parser (not a JD keyword scan)."""

    resume_id: int
    ats_flags: list[str] = Field(default_factory=list)


class ATSParseSafetyResponse(BaseModel):
    scan_id: int
    resume_id: int
    ats_parse_safety: float
    penalties: dict[str, int] = Field(default_factory=dict)
    unknown_flags: list[str] = Field(default_factory=list)


class ATSScanHistoryItem(BaseModel):
    id: int
    ats_parse_safety: float
    created_at: str


class ATSScanHistoryResponse(BaseModel):
    scans: list[ATSScanHistoryItem]
