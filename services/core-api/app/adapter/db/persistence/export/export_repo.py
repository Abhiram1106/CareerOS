from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from .....models.entities import ResumeExportJob


class ExportRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create_job(self, *, user_id: int, resume_id: int) -> ResumeExportJob:
        job = ResumeExportJob(user_id=user_id, resume_id=resume_id, status="queued")
        self._db.add(job)
        self._db.commit()
        self._db.refresh(job)
        return job

    def find_by_id_for_user(self, job_id: int, user_id: int) -> Optional[ResumeExportJob]:
        return (
            self._db.query(ResumeExportJob)
            .filter(ResumeExportJob.id == job_id, ResumeExportJob.user_id == user_id)
            .first()
        )
