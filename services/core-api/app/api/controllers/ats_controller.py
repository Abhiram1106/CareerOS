from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import require_student
from ...models.entities import User
from ...modules.ats.dto.ats_dto import ATSParseSafetyRequest
from ...modules.ats.mutation.run_ats_scan_handler import RunATSParseSafetyHandler
from ...modules.ats.query.ats_query_service import ATSQueryService

router = APIRouter()


@router.post("/ats/parse-safety")
async def ats_parse_safety(
    payload: ATSParseSafetyRequest,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return await RunATSParseSafetyHandler(db).execute(user, payload)


@router.get("/ats/scans")
def ats_history(user: User = Depends(require_student), db: Session = Depends(get_db)):
    return ATSQueryService(db).history_for_user(user).model_dump()
