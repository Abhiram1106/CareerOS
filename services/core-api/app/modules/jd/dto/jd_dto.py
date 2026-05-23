from __future__ import annotations

from pydantic import BaseModel, Field


class JDParseRequest(BaseModel):
    jd_text: str = Field(min_length=20)
    company: str = ""
    role: str = ""
    college_id: int | None = None


class JDParseResponse(BaseModel):
    jd_id: int
    company: str
    role: str
    required_skills: list[str]
    optional_skills: list[str]
    eligibility: dict
