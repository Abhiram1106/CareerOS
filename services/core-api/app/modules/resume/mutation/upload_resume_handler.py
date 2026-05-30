from __future__ import annotations

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from ....adapter.db.persistence.resume.resume_repo import ResumeRepo
from ....adapter.db.persistence.resume.resume_section_repo import ResumeSectionRepo
from ....models.entities import User
from ....services.clients import parse_resume_file
from ..dto.resume_dto import ResumeUploadResponse


class UploadResumeHandler:
    _ALLOWED = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    def __init__(self, db: Session) -> None:
        self._resumes = ResumeRepo(db)
        self._sections = ResumeSectionRepo(db)

    async def execute(self, user: User, file: UploadFile) -> dict:
        ct = file.content_type or ""
        fn = (file.filename or "").lower()
        if ct not in self._ALLOWED:
            if fn.endswith(".pdf"):
                ct = "application/pdf"
            elif fn.endswith(".docx"):
                ct = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            else:
                raise HTTPException(status_code=415, detail="Only PDF and DOCX files accepted")

        content = await file.read()
        if len(content) > 5 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File must be under 5 MB")

        source_format = "pdf" if "pdf" in ct else "docx"
        parse_result = await parse_resume_file(content, file.filename or f"resume.{source_format}", ct)
        resume = self._resumes.create_uploaded(
            user_id=user.id,
            source_format=source_format,
            content_text=parse_result.get("full_text", ""),
        )
        self._sections.add_sections(resume.id, parse_result.get("sections", []))

        return ResumeUploadResponse(
            resume_id=resume.id,
            source_format=source_format,
            sections=parse_result.get("sections", []),
            ats_flags=parse_result.get("ats_flags", []),
            parse_warnings=parse_result.get("parse_warnings", []),
            char_count=parse_result.get("char_count", 0),
        ).model_dump()
