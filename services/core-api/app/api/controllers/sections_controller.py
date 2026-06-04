"""CRUD routes for all structured career profile sections."""

from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import require_student
from ...models.entities import User
from ...services.clients import vector_user_signal
from ...services.audit import record_audit
from ...adapter.db.persistence.profile.sections_repo import (
    CertificationRepo,
    EducationRepo,
    JobApplicationRepo,
    ProjectRepo,
    SkillRepo,
    WorkExpRepo,
)
from ...modules.profile.dto.sections_dto import (
    CertificationCreate,
    CertificationResponse,
    CertificationUpdate,
    EducationCreate,
    EducationResponse,
    EducationUpdate,
    JobApplicationCreate,
    JobApplicationResponse,
    JobApplicationUpdate,
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    SkillBulkUpsert,
    SkillCreate,
    SkillResponse,
    UserLinksUpdate,
    WorkExpCreate,
    WorkExpResponse,
    WorkExpUpdate,
)

router = APIRouter()


def _work_exp_out(row: Any) -> dict:
    return WorkExpResponse(
        id=row.id,
        company=row.company,
        title=row.title,
        employment_type=row.employment_type,
        location=row.location,
        start_date=row.start_date,
        end_date=row.end_date,
        is_current=row.is_current,
        bullets=json.loads(row.bullets) if row.bullets else [],
        sort_order=row.sort_order,
    ).model_dump()


def _edu_out(row: Any) -> dict:
    return EducationResponse(
        id=row.id,
        institution=row.institution,
        degree=row.degree,
        field=row.field,
        start_year=row.start_year,
        end_year=row.end_year,
        cgpa=row.cgpa,
        percentage=row.percentage,
        coursework=row.coursework or "",
        sort_order=row.sort_order,
    ).model_dump()


def _skill_out(row: Any) -> dict:
    return SkillResponse(id=row.id, name=row.name, category=row.category, proficiency=row.proficiency).model_dump()


def _proj_out(row: Any) -> dict:
    return ProjectResponse(
        id=row.id,
        title=row.title,
        description=row.description or "",
        tech_stack=json.loads(row.tech_stack) if row.tech_stack else [],
        github_url=row.github_url or "",
        live_url=row.live_url or "",
        start_date=row.start_date or "",
        end_date=row.end_date or "",
        sort_order=row.sort_order,
    ).model_dump()


def _cert_out(row: Any) -> dict:
    return CertificationResponse(
        id=row.id,
        name=row.name,
        issuer=row.issuer,
        issue_date=row.issue_date or "",
        expiry_date=row.expiry_date or "",
        credential_id=row.credential_id or "",
        credential_url=row.credential_url or "",
        sort_order=row.sort_order,
    ).model_dump()


def _app_out(row: Any) -> dict:
    return JobApplicationResponse(
        id=row.id,
        job_external_id=row.job_external_id,
        job_title=row.job_title or "",
        company=row.company or "",
        apply_url=row.apply_url or "",
        status=row.status,
        resume_id=row.resume_id,
        notes=row.notes or "",
        applied_at=row.applied_at.isoformat() if row.applied_at else None,
        created_at=row.created_at.isoformat(),
    ).model_dump()


# ── Work Experience ───────────────────────────────────────────────────────────

@router.get("/profile/work-experience")
def list_work_exp(user: User = Depends(require_student), db: Session = Depends(get_db)):
    return {"work_experiences": [_work_exp_out(r) for r in WorkExpRepo(db).list_for_user(user.id)]}


@router.post("/profile/work-experience", status_code=201)
def add_work_exp(payload: WorkExpCreate, user: User = Depends(require_student), db: Session = Depends(get_db)):
    row = WorkExpRepo(db).create(user.id, payload.model_dump())
    return _work_exp_out(row)


@router.put("/profile/work-experience/{item_id}")
def update_work_exp(item_id: int, payload: WorkExpUpdate, user: User = Depends(require_student), db: Session = Depends(get_db)):
    row = WorkExpRepo(db).update(item_id, user.id, {k: v for k, v in payload.model_dump().items() if v is not None})
    if not row:
        raise HTTPException(status_code=404, detail="Work experience not found")
    return _work_exp_out(row)


@router.delete("/profile/work-experience/{item_id}", status_code=204)
def delete_work_exp(item_id: int, user: User = Depends(require_student), db: Session = Depends(get_db)):
    if not WorkExpRepo(db).delete(item_id, user.id):
        raise HTTPException(status_code=404, detail="Work experience not found")


# ── Education ─────────────────────────────────────────────────────────────────

@router.get("/profile/education")
def list_education(user: User = Depends(require_student), db: Session = Depends(get_db)):
    return {"educations": [_edu_out(r) for r in EducationRepo(db).list_for_user(user.id)]}


@router.post("/profile/education", status_code=201)
def add_education(payload: EducationCreate, user: User = Depends(require_student), db: Session = Depends(get_db)):
    row = EducationRepo(db).create(user.id, payload.model_dump())
    return _edu_out(row)


@router.put("/profile/education/{item_id}")
def update_education(item_id: int, payload: EducationUpdate, user: User = Depends(require_student), db: Session = Depends(get_db)):
    row = EducationRepo(db).update(item_id, user.id, {k: v for k, v in payload.model_dump().items() if v is not None})
    if not row:
        raise HTTPException(status_code=404, detail="Education not found")
    return _edu_out(row)


@router.delete("/profile/education/{item_id}", status_code=204)
def delete_education(item_id: int, user: User = Depends(require_student), db: Session = Depends(get_db)):
    if not EducationRepo(db).delete(item_id, user.id):
        raise HTTPException(status_code=404, detail="Education not found")


# ── Skills ────────────────────────────────────────────────────────────────────

@router.get("/profile/skills")
def list_skills(user: User = Depends(require_student), db: Session = Depends(get_db)):
    return {"skills": [_skill_out(r) for r in SkillRepo(db).list_for_user(user.id)]}


@router.post("/profile/skills", status_code=201)
def add_skill(payload: SkillCreate, user: User = Depends(require_student), db: Session = Depends(get_db)):
    row = SkillRepo(db).add(user.id, payload.model_dump())
    return _skill_out(row)


@router.post("/profile/skills/bulk")
def bulk_upsert_skills(payload: SkillBulkUpsert, user: User = Depends(require_student), db: Session = Depends(get_db)):
    rows = SkillRepo(db).bulk_replace(user.id, [s.model_dump() for s in payload.skills])
    return {"skills": [_skill_out(r) for r in rows]}


@router.delete("/profile/skills/{skill_id}", status_code=204)
def delete_skill(skill_id: int, user: User = Depends(require_student), db: Session = Depends(get_db)):
    if not SkillRepo(db).delete(skill_id, user.id):
        raise HTTPException(status_code=404, detail="Skill not found")


# ── Projects ──────────────────────────────────────────────────────────────────

@router.get("/profile/projects")
def list_projects(user: User = Depends(require_student), db: Session = Depends(get_db)):
    return {"projects": [_proj_out(r) for r in ProjectRepo(db).list_for_user(user.id)]}


@router.post("/profile/projects", status_code=201)
def add_project(payload: ProjectCreate, user: User = Depends(require_student), db: Session = Depends(get_db)):
    row = ProjectRepo(db).create(user.id, payload.model_dump())
    return _proj_out(row)


@router.put("/profile/projects/{item_id}")
def update_project(item_id: int, payload: ProjectUpdate, user: User = Depends(require_student), db: Session = Depends(get_db)):
    row = ProjectRepo(db).update(item_id, user.id, {k: v for k, v in payload.model_dump().items() if v is not None})
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    return _proj_out(row)


@router.delete("/profile/projects/{item_id}", status_code=204)
def delete_project(item_id: int, user: User = Depends(require_student), db: Session = Depends(get_db)):
    if not ProjectRepo(db).delete(item_id, user.id):
        raise HTTPException(status_code=404, detail="Project not found")


# ── Certifications ────────────────────────────────────────────────────────────

@router.get("/profile/certifications")
def list_certifications(user: User = Depends(require_student), db: Session = Depends(get_db)):
    return {"certifications": [_cert_out(r) for r in CertificationRepo(db).list_for_user(user.id)]}


@router.post("/profile/certifications", status_code=201)
def add_certification(payload: CertificationCreate, user: User = Depends(require_student), db: Session = Depends(get_db)):
    row = CertificationRepo(db).create(user.id, payload.model_dump())
    return _cert_out(row)


@router.put("/profile/certifications/{item_id}")
def update_certification(item_id: int, payload: CertificationUpdate, user: User = Depends(require_student), db: Session = Depends(get_db)):
    row = CertificationRepo(db).update(item_id, user.id, {k: v for k, v in payload.model_dump().items() if v is not None})
    if not row:
        raise HTTPException(status_code=404, detail="Certification not found")
    return _cert_out(row)


@router.delete("/profile/certifications/{item_id}", status_code=204)
def delete_certification(item_id: int, user: User = Depends(require_student), db: Session = Depends(get_db)):
    if not CertificationRepo(db).delete(item_id, user.id):
        raise HTTPException(status_code=404, detail="Certification not found")


# ── Job Applications ──────────────────────────────────────────────────────────

@router.get("/applications")
def list_applications(user: User = Depends(require_student), db: Session = Depends(get_db)):
    return {"applications": [_app_out(r) for r in JobApplicationRepo(db).list_for_user(user.id)]}


@router.post("/applications", status_code=201)
def save_application(payload: JobApplicationCreate, user: User = Depends(require_student), db: Session = Depends(get_db)):
    existing = JobApplicationRepo(db).get_by_external(user.id, payload.job_external_id)
    if existing:
        return _app_out(existing)
    row = JobApplicationRepo(db).create(user.id, payload.model_dump())
    return _app_out(row)


@router.put("/applications/{item_id}")
async def update_application(item_id: int, payload: JobApplicationUpdate, user: User = Depends(require_student), db: Session = Depends(get_db)):
    row = JobApplicationRepo(db).update(item_id, user.id, payload.model_dump())
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")

    # CARE-RAG Layer 6: log positive outcome signal when application reaches interview or offer
    new_status = payload.status
    if new_status in ("interview", "offer"):
        content = (
            f"outcome_{new_status}: job={row.job_title} company={row.company} "
            f"application_id={row.id}"
        )
        # Find the most recent scorecard for this user to tag as a positive outcome
        from sqlalchemy import text as sql_text
        latest_sc = db.execute(
            sql_text(
                "SELECT sc.id FROM scorecards sc "
                "JOIN resumes r ON r.id = sc.resume_id "
                "WHERE r.user_id = :uid ORDER BY sc.created_at DESC LIMIT 1"
            ),
            {"uid": user.id},
        ).fetchone()
        scorecard_id = latest_sc[0] if latest_sc else 0

        await vector_user_signal(
            user_id=user.id,
            signal_type=f"outcome_{new_status}",
            scorecard_id=scorecard_id,
            content=content,
        )
        record_audit(
            db,
            actor_id=user.id,
            action=f"application.{new_status}",
            target_type="job_application",
            target_id=row.id,
            payload={"job_title": row.job_title, "company": row.company},
        )

    return _app_out(row)


@router.delete("/applications/{item_id}", status_code=204)
def delete_application(item_id: int, user: User = Depends(require_student), db: Session = Depends(get_db)):
    if not JobApplicationRepo(db).delete(item_id, user.id):
        raise HTTPException(status_code=404, detail="Application not found")


# ── User social links ─────────────────────────────────────────────────────────

@router.put("/profile/links")
def update_links(payload: UserLinksUpdate, user: User = Depends(require_student), db: Session = Depends(get_db)):
    user.phone = payload.phone
    user.linkedin_url = payload.linkedin_url
    user.github_url = payload.github_url
    user.portfolio_url = payload.portfolio_url
    db.commit()
    return {"ok": True}


@router.get("/profile/complete")
def full_profile(user: User = Depends(require_student), db: Session = Depends(get_db)):
    """Return the full structured profile in one call — used by resume builder."""
    return {
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone or "",
            "linkedin_url": user.linkedin_url or "",
            "github_url": user.github_url or "",
            "portfolio_url": user.portfolio_url or "",
        },
        "work_experiences": [_work_exp_out(r) for r in WorkExpRepo(db).list_for_user(user.id)],
        "educations": [_edu_out(r) for r in EducationRepo(db).list_for_user(user.id)],
        "skills": [_skill_out(r) for r in SkillRepo(db).list_for_user(user.id)],
        "projects": [_proj_out(r) for r in ProjectRepo(db).list_for_user(user.id)],
        "certifications": [_cert_out(r) for r in CertificationRepo(db).list_for_user(user.id)],
    }
