from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import require_officer
from ...models.entities import User
from ...modules.officer.query.officer_cohort_query_service import OfficerCohortQueryService
from ...services.audit import record_audit

router = APIRouter(prefix="/officer", tags=["officer"])


@router.get("/cohort")
def officer_cohort(
    user: User = Depends(require_officer),
    db: Session = Depends(get_db),
):
    result = OfficerCohortQueryService(db).get_cohort().model_dump()
    record_audit(
        db,
        actor_id=user.id,
        action="officer.cohort.view",
        target_type="cohort",
        payload={"students_scored": result["kpis"]["students_scored"]},
    )
    return result
