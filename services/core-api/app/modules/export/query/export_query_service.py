from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ....adapter.db.persistence.export.export_repo import ExportRepo
from ....models.entities import User
from ....services.pdf_export import generate_download_target
from ..dto.export_dto import ExportStatusResponse


class ExportQueryService:
    def __init__(self, db: Session) -> None:
        self._exports = ExportRepo(db)

    def status_for_user(self, user: User, job_id: int) -> ExportStatusResponse:
        job = self._exports.find_by_id_for_user(job_id, user.id)
        if not job:
            raise HTTPException(status_code=404, detail="Export job not found")
        return ExportStatusResponse(
            job_id=job.id,
            status=job.status,
            error_message=job.error_message,
            has_file=bool(job.file_path),
        )

    def download_target_for_user(self, user: User, job_id: int) -> tuple[str, str]:
        job = self._exports.find_by_id_for_user(job_id, user.id)
        if not job:
            raise HTTPException(status_code=404, detail="Export job not found")
        if job.status != "completed" or not job.file_path:
            raise HTTPException(status_code=400, detail="Export not ready")
        return generate_download_target(job.file_path)
