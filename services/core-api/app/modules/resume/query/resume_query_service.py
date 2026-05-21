from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ....adapter.db.persistence.resume.resume_view import ResumeView
from ....models.entities import User
from ..dto.resume_dto import (
    ResumeDetailResponse,
    ResumeListItem,
    ResumeListResponse,
    ResumeSectionItem,
    ResumeSectionsResponse,
)


class ResumeQueryService:
    def __init__(self, db: Session) -> None:
        self._view = ResumeView(db)

    def list_for_user(self, user: User) -> ResumeListResponse:
        rows = self._view.list_for_user(user.id)
        return ResumeListResponse(
            resumes=[
                ResumeListItem(
                    id=row.id,
                    template_name=row.template_name,
                    created_at=row.created_at.isoformat(),
                )
                for row in rows
            ]
        )

    def get_for_user(self, user: User, resume_id: int) -> ResumeDetailResponse:
        row = self._view.find_by_id_for_user(resume_id, user.id)
        if not row:
            raise HTTPException(status_code=404, detail="Resume not found")
        return ResumeDetailResponse(
            id=row.id,
            template_name=row.template_name,
            content=row.content_text or "",
            created_at=row.created_at.isoformat(),
        )

    def sections_for_user(self, user: User, resume_id: int) -> ResumeSectionsResponse:
        resume = self._view.find_by_id_for_user(resume_id, user.id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        sections = self._view.sections_for_resume(resume_id)
        return ResumeSectionsResponse(
            resume_id=resume_id,
            source_format=resume.source_format,
            sections=[
                ResumeSectionItem(
                    section_name=s.section_name,
                    content_json=ResumeView.parse_section_content(s.content_json),
                    confidence=s.confidence,
                )
                for s in sections
            ],
        )
