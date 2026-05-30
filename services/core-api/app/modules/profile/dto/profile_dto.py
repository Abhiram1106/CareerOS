from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from ...common.dto.strict import StrictModel


class ProfileUpsert(StrictModel):
    city: str
    professional_status: str
    target_role: str
    skills_csv: str
    summary: str
    experience_bullet: str
    cgpa: Optional[float] = Field(default=None, ge=0.0, le=10.0)
    active_backlogs: int = Field(default=0, ge=0)
    branch: str = ""
    grad_year: Optional[int] = Field(default=None, ge=2000, le=2100)


class ProfileResponse(BaseModel):
    full_name: str
    email: EmailStr
    city: str
    professional_status: str
    target_role: str
    skills_csv: str
    summary: str
    experience_bullet: str
    cgpa: Optional[float] = None
    active_backlogs: int = 0
    branch: str = ""
    grad_year: Optional[int] = None


class ProfileUpdateResponse(BaseModel):
    ok: bool = True
