from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import require_officer
from ...models.entities import User
from ...modules.officer.query.officer_batch_query_service import OfficerBatchQueryService
from ...modules.officer.query.officer_cohort_query_service import OfficerCohortQueryService
from ...modules.officer.query.officer_dashboard_query_service import OfficerDashboardQueryService
from ...modules.officer.query.officer_review_query_service import OfficerReviewQueryService
from ...services.audit import record_audit

router = APIRouter(prefix="/officer", tags=["officer"])


@router.get("/dashboard")
def officer_dashboard(
    user: User = Depends(require_officer),
    db: Session = Depends(get_db),
):
    result = OfficerDashboardQueryService(db).get_dashboard().model_dump()
    record_audit(
        db,
        actor_id=user.id,
        action="officer.dashboard.view",
        target_type="cohort",
        payload={"students_scored": result["kpis"]["students_scored"]},
    )
    return result


@router.get("/review")
def officer_review_queue(
    user: User = Depends(require_officer),
    db: Session = Depends(get_db),
):
    result = OfficerReviewQueryService(db).get_review_queue().model_dump()
    record_audit(
        db,
        actor_id=user.id,
        action="officer.review.view",
        target_type="cohort",
        payload={"queue_size": len(result["items"])},
    )
    return result


@router.get("/batches")
def officer_batches(
    user: User = Depends(require_officer),
    db: Session = Depends(get_db),
):
    result = OfficerBatchQueryService(db).list_batches().model_dump()
    record_audit(
        db,
        actor_id=user.id,
        action="officer.batches.view",
        target_type="batch",
        payload={"batch_count": len(result["batches"])},
    )
    return result


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
