"""Backward-compatible API contracts — re-export from domain DTOs."""

from __future__ import annotations

from ..modules.ats.dto.ats_dto import ATSScanRequest, ATSScanResponse
from ..modules.auth.dto.auth_dto import AuthResponse, LoginRequest, RegisterRequest
from ..modules.export.dto.export_dto import ExportResumeRequest
from ..modules.profile.dto.profile_dto import ProfileResponse, ProfileUpdateResponse, ProfileUpsert
from ..modules.resume.dto.resume_dto import ResumeGenerateRequest

__all__ = [
    "RegisterRequest",
    "LoginRequest",
    "AuthResponse",
    "ProfileUpsert",
    "ProfileResponse",
    "ProfileUpdateResponse",
    "ResumeGenerateRequest",
    "ATSScanRequest",
    "ATSScanResponse",
    "ExportResumeRequest",
    "ParseResumeRequest",
    "ResumeSection",
    "ParseResumeResponse",
]


# ── Resume parser (legacy satellite contracts) ──────────────────────────────

from pydantic import BaseModel, Field


class ParseResumeRequest(BaseModel):
    resume_id: int


class ResumeSection(BaseModel):
    section_name: str
    content_json: dict
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)


class ParseResumeResponse(BaseModel):
    resume_id: int
    sections: list[ResumeSection]
    ats_flags: list[str]
    parse_warnings: list[str]
