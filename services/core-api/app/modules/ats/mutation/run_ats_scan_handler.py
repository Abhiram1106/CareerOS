from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from careeros_scoring import resume_text_from_sections

from ....adapter.db.persistence.ats.ats_repo import ATSRepo
from ....adapter.db.persistence.resume.resume_view import ResumeView
from ....models.entities import User
from ....services.clients import run_ats_parse_safety
from ..dto.ats_dto import ATSParseSafetyRequest, ATSParseSafetyResponse


class RunATSParseSafetyHandler:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._scans = ATSRepo(db)
        self._resumes = ResumeView(db)

    async def execute(self, user: User, payload: ATSParseSafetyRequest) -> dict:
        resume = self._resumes.find_by_id_for_user(payload.resume_id, user.id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")

        sections = self._resumes.sections_for_resume(payload.resume_id)
        section_dicts = [
            {
                "section_name": s.section_name,
                "content_json": ResumeView.parse_section_content(s.content_json),
            }
            for s in sections
        ]
        resume_text = resume_text_from_sections(section_dicts)
        if resume.content_text and len(resume.content_text) > len(resume_text):
            resume_text = resume.content_text

        result = await run_ats_parse_safety(payload.ats_flags, resume_text)
        row = self._scans.create_from_parse_safety(
            user_id=user.id,
            ats_parse_safety=float(result["ats_parse_safety"]),
        )
        return ATSParseSafetyResponse(
            scan_id=row.id,
            resume_id=payload.resume_id,
            ats_parse_safety=float(result["ats_parse_safety"]),
            bucket=result.get("bucket", ""),
            checks=result.get("checks", []),
            issues=result.get("issues", []),
            penalties=result.get("penalties", {}),
            unknown_flags=result.get("unknown_flags", []),
        ).model_dump()
