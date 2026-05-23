from fastapi import APIRouter

from ...modules.ats.dto.parse_safety_dto import ParseSafetyRequest
from ...modules.ats.mutation.parse_safety_handler import ParseSafetyHandler

router = APIRouter()


@router.post("/parse-safety")
def parse_safety(payload: ParseSafetyRequest) -> dict:
    return ParseSafetyHandler().execute(payload)
