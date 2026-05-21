from fastapi import APIRouter

from ...modules.ats.dto.scan_dto import ScanRequest
from ...modules.ats.mutation.scan_handler import ScanHandler

router = APIRouter()


@router.post("/scan")
def scan(payload: ScanRequest):
    return ScanHandler().execute(payload)
