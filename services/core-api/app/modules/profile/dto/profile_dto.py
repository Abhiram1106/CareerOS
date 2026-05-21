from __future__ import annotations

from pydantic import BaseModel, EmailStr


class ProfileUpsert(BaseModel):
    city: str
    professional_status: str
    target_role: str
    skills_csv: str
    summary: str
    experience_bullet: str


class ProfileResponse(BaseModel):
    full_name: str
    email: EmailStr
    city: str
    professional_status: str
    target_role: str
    skills_csv: str
    summary: str
    experience_bullet: str


class ProfileUpdateResponse(BaseModel):
    ok: bool = True
