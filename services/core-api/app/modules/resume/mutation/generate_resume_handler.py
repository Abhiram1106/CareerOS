from __future__ import annotations

from sqlalchemy.orm import Session

from ....adapter.db.persistence.profile.profile_view import ProfileView
from ....adapter.db.persistence.resume.resume_repo import ResumeRepo
from ....models.entities import User
from ....services.clients import generate_resume_content
from ...profile.mapper.profile_mapper import profile_fields_for_scan
from ..dto.resume_dto import ResumeGenerateRequest, ResumeGenerateResponse


class GenerateResumeHandler:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._resumes = ResumeRepo(db)
        self._profiles = ProfileView(db)

    async def execute(self, user: User, payload: ResumeGenerateRequest) -> dict:
        profile = self._profiles.find_by_user_id(user.id)
        fields = profile_fields_for_scan(user, profile)
        ai_payload = {**fields, "template_name": payload.template_name}
        generated = await generate_resume_content(ai_payload)
        resume = self._resumes.create_generated(
            user_id=user.id,
            template_name=payload.template_name,
            content_text=generated["content"],
        )
        return ResumeGenerateResponse(resume_id=resume.id, content=resume.content_text).model_dump()
