from __future__ import annotations

from pydantic import BaseModel


class ATSScanRequest(BaseModel):
    jd_text: str


class ATSScanResponse(BaseModel):
    composite: float
    keyword: float
    format: float
    quality: float
    complete: float
    contact: float


class ATSScanHistoryItem(BaseModel):
    id: int
    composite_score: float
    keyword_score: float
    format_score: float
    quality_score: float
    completeness_score: float
    contact_score: float
    created_at: str


class ATSScanHistoryResponse(BaseModel):
    scans: list[ATSScanHistoryItem]
