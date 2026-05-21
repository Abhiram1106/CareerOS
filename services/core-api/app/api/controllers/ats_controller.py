from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import current_user
from ...models.entities import User
from ...modules.ats.dto.ats_dto import ATSScanRequest
from ...modules.ats.mutation.run_ats_scan_handler import RunATSScanHandler
from ...modules.ats.query.ats_query_service import ATSQueryService

router = APIRouter()


@router.post("/ats/scan")
async def ats_scan(
    payload: ATSScanRequest,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    return await RunATSScanHandler(db).execute(user, payload)


@router.get("/ats/scans")
def ats_history(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return ATSQueryService(db).history_for_user(user).model_dump()
