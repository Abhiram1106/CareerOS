from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ProofRewriteRequest(BaseModel):
    resume_json: dict[str, Any] = Field(default_factory=dict)
    jd_json: dict[str, Any] = Field(default_factory=dict)
    evidence_json: dict[str, Any] = Field(default_factory=dict)
    ats_flags: list[str] = Field(default_factory=list)


class TopIssue(BaseModel):
    type: str
    message: str
    severity: str


class SectionRewrite(BaseModel):
    section: str
    original: str
    rewrite: str
    evidence_ids: list[str] = Field(default_factory=list)
    confidence: float = 0.0


class UnsupportedClaim(BaseModel):
    claim: str
    reason: str


class RequiresConfirmation(BaseModel):
    field: str
    suggested_change: str


class ProofRewriteResponse(BaseModel):
    top_issues: list[TopIssue] = Field(default_factory=list)
    section_rewrites: list[SectionRewrite] = Field(default_factory=list)
    unsupported_claims: list[UnsupportedClaim] = Field(default_factory=list)
    requires_confirmation: list[RequiresConfirmation] = Field(default_factory=list)
