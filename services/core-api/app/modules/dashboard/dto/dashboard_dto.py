from __future__ import annotations

from pydantic import BaseModel


class DashboardResponse(BaseModel):
    best_ats_score: float
    total_resumes: int
    scans_performed: int
    profile_completeness: int
