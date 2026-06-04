from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...dependencies import get_ats_query_service, get_ats_scan_handler, require_student
from ...models.entities import User
from ...modules.ats.dto.ats_dto import ATSParseSafetyRequest
from ...modules.ats.mutation.run_ats_scan_handler import RunATSParseSafetyHandler
from ...modules.ats.query.ats_query_service import ATSQueryService
from careeros_scoring import keyword_gap_analysis, simulate_vendors

router = APIRouter()


@router.post("/ats/parse-safety")
async def ats_parse_safety(
    payload: ATSParseSafetyRequest,
    user: User = Depends(require_student),
    handler: RunATSParseSafetyHandler = Depends(get_ats_scan_handler),
):
    return await handler.execute(user, payload)


@router.get("/ats/scans")
def ats_history(
    user: User = Depends(require_student),
    service: ATSQueryService = Depends(get_ats_query_service),
):
    return service.history_for_user(user).model_dump()


class VendorSimRequest(BaseModel):
    resume_text: str
    jd_text: str = ""


class KeywordGapRequest(BaseModel):
    resume_text: str
    jd_text: str


@router.post("/ats/vendor-simulation")
def vendor_simulation(
    payload: VendorSimRequest,
    user: User = Depends(require_student),
):
    """Simulate how 7 ATS vendors would score this resume. Returns composite + breakdown."""
    return simulate_vendors(payload.resume_text, payload.jd_text)


@router.post("/ats/keyword-gap")
def keyword_gap(
    payload: KeywordGapRequest,
    user: User = Depends(require_student),
):
    """Identify JD keywords present/missing in the resume."""
    return keyword_gap_analysis(payload.resume_text, payload.jd_text)
