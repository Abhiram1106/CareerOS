from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import (
    get_create_officer_batch_handler,
    get_officer_batch_query_service,
    get_officer_cohort_service,
    get_officer_dashboard_service,
    get_officer_heatmap_service,
    get_officer_readiness_report_service,
    get_officer_review_service,
    get_officer_skill_gaps_service,
    get_upload_officer_batch_handler,
    require_officer,
)
from ...models.entities import User
from ...modules.officer.dto.officer_dto import OfficerCreateBatchRequest
from ...modules.officer.mutation.officer_batch_handlers import CreateOfficerBatchHandler, UploadOfficerBatchHandler
from ...modules.officer.query.officer_batch_query_service import OfficerBatchQueryService
from ...modules.officer.query.officer_cohort_query_service import OfficerCohortQueryService
from ...modules.officer.query.officer_dashboard_query_service import OfficerDashboardQueryService
from ...modules.officer.query.officer_heatmap_query_service import OfficerHeatmapQueryService
from ...modules.officer.query.officer_readiness_report_service import OfficerReadinessReportService
from ...modules.officer.query.officer_review_query_service import OfficerReviewQueryService
from ...modules.officer.query.officer_skill_gaps_query_service import OfficerSkillGapsQueryService
from ...services.audit import record_audit

router = APIRouter(prefix="/officer", tags=["officer"])


@router.get("/dashboard")
def officer_dashboard(
    user: User = Depends(require_officer),
    db: Session = Depends(get_db),
    service: OfficerDashboardQueryService = Depends(get_officer_dashboard_service),
):
    result = service.get_dashboard().model_dump()
    record_audit(
        db,
        actor_id=user.id,
        action="officer.dashboard.view",
        target_type="cohort",
        payload={"students_scored": result["kpis"]["students_scored"]},
    )
    return result


@router.get("/heatmap")
def officer_heatmap(
    user: User = Depends(require_officer),
    db: Session = Depends(get_db),
    service: OfficerHeatmapQueryService = Depends(get_officer_heatmap_service),
):
    result = service.get_heatmap().model_dump()
    record_audit(
        db,
        actor_id=user.id,
        action="officer.heatmap.view",
        target_type="cohort",
        payload={"departments": len(result["departments"])},
    )
    return result


@router.get("/skill-gaps")
def officer_skill_gaps(
    user: User = Depends(require_officer),
    db: Session = Depends(get_db),
    service: OfficerSkillGapsQueryService = Depends(get_officer_skill_gaps_service),
):
    result = service.get_skill_gaps().model_dump()
    record_audit(
        db,
        actor_id=user.id,
        action="officer.skill_gaps.view",
        target_type="cohort",
        payload={"gaps": len(result["items"])},
    )
    return result


@router.get("/review")
def officer_review_queue(
    user: User = Depends(require_officer),
    db: Session = Depends(get_db),
    service: OfficerReviewQueryService = Depends(get_officer_review_service),
):
    result = service.get_review_queue().model_dump()
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
    service: OfficerBatchQueryService = Depends(get_officer_batch_query_service),
):
    result = service.list_batches().model_dump()
    record_audit(
        db,
        actor_id=user.id,
        action="officer.batches.view",
        target_type="batch",
        payload={"batch_count": len(result["batches"])},
    )
    return result


@router.post("/batches")
def officer_create_batch(
    payload: OfficerCreateBatchRequest,
    user: User = Depends(require_officer),
    db: Session = Depends(get_db),
    handler: CreateOfficerBatchHandler = Depends(get_create_officer_batch_handler),
):
    result = handler.execute(user, payload).model_dump()
    record_audit(
        db,
        actor_id=user.id,
        action="officer.batch.create",
        target_type="batch",
        target_id=result["batch"]["id"],
        payload={"name": result["batch"]["name"]},
    )
    return result


@router.post("/batches/{batch_id}/upload")
async def officer_batch_upload(
    batch_id: int,
    files: list[UploadFile] = File(...),
    user: User = Depends(require_officer),
    db: Session = Depends(get_db),
    handler: UploadOfficerBatchHandler = Depends(get_upload_officer_batch_handler),
):
    result = await handler.execute(user, batch_id, files)
    record_audit(
        db,
        actor_id=user.id,
        action="officer.batch.upload",
        target_type="batch",
        target_id=batch_id,
        payload={"uploaded": result.uploaded, "errors": len(result.errors)},
    )
    return result.model_dump()


@router.get("/reports/readiness")
def officer_readiness_report(
    user: User = Depends(require_officer),
    db: Session = Depends(get_db),
    service: OfficerReadinessReportService = Depends(get_officer_readiness_report_service),
):
    pdf_bytes = service.generate_pdf_bytes()
    record_audit(
        db,
        actor_id=user.id,
        action="officer.report.readiness",
        target_type="cohort",
        payload={"bytes": len(pdf_bytes)},
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="cohort-readiness-report.pdf"'},
    )


@router.get("/cohort")
def officer_cohort(
    user: User = Depends(require_officer),
    db: Session = Depends(get_db),
    service: OfficerCohortQueryService = Depends(get_officer_cohort_service),
):
    result = service.get_cohort().model_dump()
    record_audit(
        db,
        actor_id=user.id,
        action="officer.cohort.view",
        target_type="cohort",
        payload={"students_scored": result["kpis"]["students_scored"]},
    )
    return result
