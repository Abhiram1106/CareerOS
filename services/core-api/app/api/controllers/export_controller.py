from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import current_user
from ...models.entities import User
from ...modules.export.dto.export_dto import ExportResumeRequest
from ...modules.export.mutation.queue_export_handler import QueueExportHandler
from ...modules.export.query.export_query_service import ExportQueryService
from ...services.pdf_export import infer_filename

router = APIRouter()


@router.post("/resumes/export")
def export_resume(
    payload: ExportResumeRequest,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    return QueueExportHandler(db).execute(user, payload)


@router.get("/resumes/export/{job_id}")
def export_status(
    job_id: int,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    return ExportQueryService(db).status_for_user(user, job_id).model_dump()


@router.get("/resumes/export/{job_id}/download")
def export_download(
    job_id: int,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    kind, value = ExportQueryService(db).download_target_for_user(user, job_id)
    if kind == "redirect":
        return RedirectResponse(url=value, status_code=307)
    path = Path(value)
    return FileResponse(
        path=str(path),
        filename=infer_filename(value),
        media_type="application/pdf",
    )
