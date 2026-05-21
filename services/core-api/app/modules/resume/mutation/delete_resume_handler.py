from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ....adapter.db.persistence.resume.resume_repo import ResumeRepo
from ....models.entities import User
from ..dto.resume_dto import ResumeDeleteResponse


class DeleteResumeHandler:
    def __init__(self, db: Session) -> None:
        self._resumes = ResumeRepo(db)

    def execute(self, user: User, resume_id: int) -> dict:
        if not self._resumes.delete_for_user(resume_id, user.id):
            raise HTTPException(status_code=404, detail="Resume not found")
        return ResumeDeleteResponse().model_dump()
