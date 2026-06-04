from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ResumePrompt(BaseModel):
    """Legacy flat-field prompt — kept for backward compatibility."""
    full_name: str
    target_role: str
    city: str
    skills_csv: str
    summary: str
    experience_bullet: str
    template_name: str


class ResumeStructuredPrompt(BaseModel):
    """Structured prompt — reads from GET /profile/complete payload."""
    template_name: str
    profile_data: dict[str, Any]


class ResumeGenerateResponse(BaseModel):
    content: str
