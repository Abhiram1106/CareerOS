from __future__ import annotations

import json

from sqlalchemy.orm import Session

from ....adapter.db.persistence.profile.profile_view import ProfileView
from ....adapter.db.persistence.profile.sections_repo import (
    CertificationRepo,
    EducationRepo,
    ProjectRepo,
    SkillRepo,
    WorkExpRepo,
)
from ....adapter.db.persistence.resume.resume_repo import ResumeRepo
from ....models.entities import User
from ....services.clients import generate_resume_from_profile
from ..dto.resume_dto import ResumeGenerateRequest, ResumeGenerateResponse


class GenerateResumeHandler:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._resumes = ResumeRepo(db)
        self._profiles = ProfileView(db)
        self._work_exp = WorkExpRepo(db)
        self._education = EducationRepo(db)
        self._skills = SkillRepo(db)
        self._projects = ProjectRepo(db)
        self._certs = CertificationRepo(db)

    async def execute(self, user: User, payload: ResumeGenerateRequest) -> dict:
        profile = self._profiles.find_by_user_id(user.id)

        def _we(row) -> dict:
            return {
                "company": row.company, "title": row.title,
                "employment_type": row.employment_type, "location": row.location,
                "start_date": row.start_date, "end_date": row.end_date,
                "is_current": row.is_current,
                "bullets": json.loads(row.bullets) if row.bullets else [],
            }

        def _ed(row) -> dict:
            return {
                "institution": row.institution, "degree": row.degree, "field": row.field,
                "start_year": row.start_year, "end_year": row.end_year,
                "cgpa": row.cgpa, "percentage": row.percentage, "coursework": row.coursework or "",
            }

        def _sk(row) -> dict:
            return {"name": row.name, "category": row.category, "proficiency": row.proficiency}

        def _pr(row) -> dict:
            return {
                "title": row.title, "description": row.description or "",
                "tech_stack": json.loads(row.tech_stack) if row.tech_stack else [],
                "github_url": row.github_url or "", "live_url": row.live_url or "",
                "start_date": row.start_date or "", "end_date": row.end_date or "",
            }

        def _ce(row) -> dict:
            return {
                "name": row.name, "issuer": row.issuer,
                "issue_date": row.issue_date or "", "expiry_date": row.expiry_date or "",
                "credential_id": row.credential_id or "", "credential_url": row.credential_url or "",
            }

        profile_data = {
            "user": {
                "full_name": user.full_name,
                "email": user.email,
                "phone": user.phone or "",
                "linkedin_url": user.linkedin_url or "",
                "github_url": user.github_url or "",
                "portfolio_url": user.portfolio_url or "",
            },
            "profile": {
                "target_role": profile.target_role if profile else "Software Engineer",
                "city": profile.city if profile else "",
                "skills_csv": profile.skills_csv if profile else "",
                "summary": profile.summary if profile else "",
            },
            "work_experiences": [_we(r) for r in self._work_exp.list_for_user(user.id)],
            "educations": [_ed(r) for r in self._education.list_for_user(user.id)],
            "skills": [_sk(r) for r in self._skills.list_for_user(user.id)],
            "projects": [_pr(r) for r in self._projects.list_for_user(user.id)],
            "certifications": [_ce(r) for r in self._certs.list_for_user(user.id)],
        }

        generated = await generate_resume_from_profile(payload.template_name, profile_data)
        resume = self._resumes.create_generated(
            user_id=user.id,
            template_name=payload.template_name,
            content_text=generated["content"],
        )
        return ResumeGenerateResponse(resume_id=resume.id, content=resume.content_text).model_dump()
