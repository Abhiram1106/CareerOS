from __future__ import annotations

from pydantic import BaseModel, Field


class ParseSafetyRequest(BaseModel):
    ats_flags: list[str] = Field(default_factory=list)


class ParseSafetyResponse(BaseModel):
    ats_parse_safety: float
    penalties: dict[str, int]
    unknown_flags: list[str]
