from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ....adapter.db.persistence.export.export_repo import ExportRepo
from ....adapter.db.persistence.resume.resume_repo import ResumeRepo
from ....models.entities import User
from ....services.audit import record_audit
from ....workers.tasks import generate_resume_export
from ..dto.export_dto import ExportQueueResponse, ExportResumeRequest


class QueueExportHandler:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._exports = ExportRepo(db)
        self._resumes = ResumeRepo(db)

    def execute(self, user: User, payload: ExportResumeRequest) -> dict:
        resume = self._resumes.find_by_id_for_user(payload.resume_id, user.id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        job = self._exports.create_job(user_id=user.id, resume_id=resume.id)
        record_audit(
            self._db,
            actor_id=user.id,
            action="export.queue",
            target_type="resume_export_job",
            target_id=job.id,
            payload={"resume_id": resume.id},
        )
        try:
            generate_resume_export.delay(job.id)
        except Exception:
            generate_resume_export.apply(args=[job.id])
        return ExportQueueResponse(job_id=job.id, status=job.status).model_dump()
