"""DTOs for structured career profile sections."""

from __future__ import annotations

import json
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator

from ...common.dto.strict import StrictModel


# ── Work Experience ───────────────────────────────────────────────────────────

class WorkExpCreate(StrictModel):
    company: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=200)
    employment_type: str = "Full-time"
    location: str = ""
    start_date: str = Field(min_length=1, max_length=20)
    end_date: str = ""
    is_current: bool = False
    bullets: list[str] = Field(default_factory=list, max_length=8)


class WorkExpUpdate(BaseModel):
    company: Optional[str] = Field(default=None, max_length=200)
    title: Optional[str] = Field(default=None, max_length=200)
    employment_type: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: Optional[bool] = None
    bullets: Optional[list[str]] = None


class WorkExpResponse(BaseModel):
    id: int
    company: str
    title: str
    employment_type: str
    location: str
    start_date: str
    end_date: str
    is_current: bool
    bullets: list[str]
    sort_order: int


# ── Education ─────────────────────────────────────────────────────────────────

class EducationCreate(StrictModel):
    institution: str = Field(min_length=1, max_length=300)
    degree: str = Field(min_length=1, max_length=200)
    field: str = Field(min_length=1, max_length=200)
    start_year: Optional[int] = Field(default=None, ge=1990, le=2030)
    end_year: Optional[int] = Field(default=None, ge=1990, le=2030)
    cgpa: Optional[float] = Field(default=None, ge=0.0, le=10.0)
    percentage: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    coursework: str = ""


class EducationUpdate(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    cgpa: Optional[float] = None
    percentage: Optional[float] = None
    coursework: Optional[str] = None


class EducationResponse(BaseModel):
    id: int
    institution: str
    degree: str
    field: str
    start_year: Optional[int]
    end_year: Optional[int]
    cgpa: Optional[float]
    percentage: Optional[float]
    coursework: str
    sort_order: int


# ── Skill ─────────────────────────────────────────────────────────────────────

SKILL_CATEGORIES = {"technical", "soft", "tool", "language"}
SKILL_PROFICIENCIES = {"beginner", "intermediate", "advanced", "expert"}


class SkillCreate(StrictModel):
    name: str = Field(min_length=1, max_length=100)
    category: str = "technical"
    proficiency: str = "intermediate"

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        if v not in SKILL_CATEGORIES:
            raise ValueError(f"category must be one of {SKILL_CATEGORIES}")
        return v

    @field_validator("proficiency")
    @classmethod
    def validate_proficiency(cls, v: str) -> str:
        if v not in SKILL_PROFICIENCIES:
            raise ValueError(f"proficiency must be one of {SKILL_PROFICIENCIES}")
        return v


class SkillBulkUpsert(StrictModel):
    """Replace all skills for a user in one shot."""
    skills: list[SkillCreate]


class SkillResponse(BaseModel):
    id: int
    name: str
    category: str
    proficiency: str


# ── Project ───────────────────────────────────────────────────────────────────

class ProjectCreate(StrictModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    tech_stack: list[str] = Field(default_factory=list)
    github_url: str = ""
    live_url: str = ""
    start_date: str = ""
    end_date: str = ""


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tech_stack: Optional[list[str]] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    tech_stack: list[str]
    github_url: str
    live_url: str
    start_date: str
    end_date: str
    sort_order: int


# ── Certification ─────────────────────────────────────────────────────────────

class CertificationCreate(StrictModel):
    name: str = Field(min_length=1, max_length=200)
    issuer: str = Field(min_length=1, max_length=200)
    issue_date: str = ""
    expiry_date: str = ""
    credential_id: str = ""
    credential_url: str = ""


class CertificationUpdate(BaseModel):
    name: Optional[str] = None
    issuer: Optional[str] = None
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None


class CertificationResponse(BaseModel):
    id: int
    name: str
    issuer: str
    issue_date: str
    expiry_date: str
    credential_id: str
    credential_url: str
    sort_order: int


# ── Job Application ───────────────────────────────────────────────────────────

APPLICATION_STATUSES = {"saved", "applied", "screening", "interview", "offer", "rejected"}


class JobApplicationCreate(StrictModel):
    job_external_id: str = Field(min_length=1, max_length=200)
    job_title: str = ""
    company: str = ""
    apply_url: str = ""
    resume_id: Optional[int] = None
    notes: str = ""


class JobApplicationUpdate(BaseModel):
    status: Optional[str] = None
    resume_id: Optional[int] = None
    notes: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in APPLICATION_STATUSES:
            raise ValueError(f"status must be one of {APPLICATION_STATUSES}")
        return v


class JobApplicationResponse(BaseModel):
    id: int
    job_external_id: str
    job_title: str
    company: str
    apply_url: str
    status: str
    resume_id: Optional[int]
    notes: str
    applied_at: Optional[str]
    created_at: str


# ── User social links update ──────────────────────────────────────────────────

class UserLinksUpdate(StrictModel):
    phone: str = ""
    linkedin_url: str = ""
    github_url: str = ""
    portfolio_url: str = ""
