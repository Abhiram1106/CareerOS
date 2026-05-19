from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Literal["student", "officer", "admin"] = "student"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    email: EmailStr
    full_name: str
    role: str


class ProfileUpsert(BaseModel):
    city: str
    professional_status: str
    target_role: str
    skills_csv: str
    summary: str
    experience_bullet: str


class ResumeGenerateRequest(BaseModel):
    template_name: str = "classic"


class ATSScanRequest(BaseModel):
    jd_text: str


class ATSScanResponse(BaseModel):
    composite: float
    keyword: float
    format: float
    quality: float
    complete: float
    contact: float


class ExportResumeRequest(BaseModel):
    resume_id: int


# ── Resume parser ─────────────────────────────────────────────────────────────

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
