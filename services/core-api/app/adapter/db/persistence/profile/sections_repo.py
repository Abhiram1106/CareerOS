"""CRUD persistence for all structured career profile sections."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy.orm import Session

from .....models.entities import (
    Certification,
    Education,
    JobApplication,
    Project,
    Skill,
    User,
    WorkExperience,
)


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


# ── WorkExperience ────────────────────────────────────────────────────────────

class WorkExpRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_for_user(self, user_id: int) -> list[WorkExperience]:
        return (
            self._db.query(WorkExperience)
            .filter(WorkExperience.user_id == user_id)
            .order_by(WorkExperience.sort_order, WorkExperience.created_at.desc())
            .all()
        )

    def get(self, item_id: int, user_id: int) -> Optional[WorkExperience]:
        return (
            self._db.query(WorkExperience)
            .filter(WorkExperience.id == item_id, WorkExperience.user_id == user_id)
            .first()
        )

    def create(self, user_id: int, data: dict[str, Any]) -> WorkExperience:
        bullets = data.get("bullets", [])
        row = WorkExperience(
            user_id=user_id,
            company=data["company"],
            title=data["title"],
            employment_type=data.get("employment_type", "Full-time"),
            location=data.get("location", ""),
            start_date=data["start_date"],
            end_date=data.get("end_date", ""),
            is_current=data.get("is_current", False),
            bullets=json.dumps(bullets),
            sort_order=self._next_sort(user_id),
            created_at=_now(),
            updated_at=_now(),
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return row

    def update(self, item_id: int, user_id: int, data: dict[str, Any]) -> Optional[WorkExperience]:
        row = self.get(item_id, user_id)
        if not row:
            return None
        for k, v in data.items():
            if v is None:
                continue
            if k == "bullets":
                setattr(row, k, json.dumps(v))
            else:
                setattr(row, k, v)
        row.updated_at = _now()
        self._db.commit()
        self._db.refresh(row)
        return row

    def delete(self, item_id: int, user_id: int) -> bool:
        row = self.get(item_id, user_id)
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True

    def _next_sort(self, user_id: int) -> int:
        count = self._db.query(WorkExperience).filter(WorkExperience.user_id == user_id).count()
        return count


# ── Education ─────────────────────────────────────────────────────────────────

class EducationRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_for_user(self, user_id: int) -> list[Education]:
        return (
            self._db.query(Education)
            .filter(Education.user_id == user_id)
            .order_by(Education.sort_order, Education.end_year.desc())
            .all()
        )

    def get(self, item_id: int, user_id: int) -> Optional[Education]:
        return (
            self._db.query(Education)
            .filter(Education.id == item_id, Education.user_id == user_id)
            .first()
        )

    def create(self, user_id: int, data: dict[str, Any]) -> Education:
        row = Education(
            user_id=user_id,
            institution=data["institution"],
            degree=data["degree"],
            field=data["field"],
            start_year=data.get("start_year"),
            end_year=data.get("end_year"),
            cgpa=data.get("cgpa"),
            percentage=data.get("percentage"),
            coursework=data.get("coursework", ""),
            sort_order=self._next_sort(user_id),
            created_at=_now(),
            updated_at=_now(),
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return row

    def update(self, item_id: int, user_id: int, data: dict[str, Any]) -> Optional[Education]:
        row = self.get(item_id, user_id)
        if not row:
            return None
        for k, v in data.items():
            if v is not None:
                setattr(row, k, v)
        row.updated_at = _now()
        self._db.commit()
        self._db.refresh(row)
        return row

    def delete(self, item_id: int, user_id: int) -> bool:
        row = self.get(item_id, user_id)
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True

    def _next_sort(self, user_id: int) -> int:
        return self._db.query(Education).filter(Education.user_id == user_id).count()


# ── Skill ─────────────────────────────────────────────────────────────────────

class SkillRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_for_user(self, user_id: int) -> list[Skill]:
        return (
            self._db.query(Skill)
            .filter(Skill.user_id == user_id)
            .order_by(Skill.category, Skill.name)
            .all()
        )

    def bulk_replace(self, user_id: int, skills: list[dict[str, Any]]) -> list[Skill]:
        self._db.query(Skill).filter(Skill.user_id == user_id).delete()
        rows = [
            Skill(
                user_id=user_id,
                name=s["name"],
                category=s.get("category", "technical"),
                proficiency=s.get("proficiency", "intermediate"),
                created_at=_now(),
            )
            for s in skills
        ]
        self._db.add_all(rows)
        self._db.commit()
        return rows

    def add(self, user_id: int, data: dict[str, Any]) -> Skill:
        row = Skill(
            user_id=user_id,
            name=data["name"],
            category=data.get("category", "technical"),
            proficiency=data.get("proficiency", "intermediate"),
            created_at=_now(),
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return row

    def delete(self, skill_id: int, user_id: int) -> bool:
        row = self._db.query(Skill).filter(Skill.id == skill_id, Skill.user_id == user_id).first()
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True


# ── Project ───────────────────────────────────────────────────────────────────

class ProjectRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_for_user(self, user_id: int) -> list[Project]:
        return (
            self._db.query(Project)
            .filter(Project.user_id == user_id)
            .order_by(Project.sort_order, Project.created_at.desc())
            .all()
        )

    def get(self, item_id: int, user_id: int) -> Optional[Project]:
        return (
            self._db.query(Project)
            .filter(Project.id == item_id, Project.user_id == user_id)
            .first()
        )

    def create(self, user_id: int, data: dict[str, Any]) -> Project:
        row = Project(
            user_id=user_id,
            title=data["title"],
            description=data.get("description", ""),
            tech_stack=json.dumps(data.get("tech_stack", [])),
            github_url=data.get("github_url", ""),
            live_url=data.get("live_url", ""),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date", ""),
            sort_order=self._next_sort(user_id),
            created_at=_now(),
            updated_at=_now(),
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return row

    def update(self, item_id: int, user_id: int, data: dict[str, Any]) -> Optional[Project]:
        row = self.get(item_id, user_id)
        if not row:
            return None
        for k, v in data.items():
            if v is None:
                continue
            if k == "tech_stack":
                setattr(row, k, json.dumps(v))
            else:
                setattr(row, k, v)
        row.updated_at = _now()
        self._db.commit()
        self._db.refresh(row)
        return row

    def delete(self, item_id: int, user_id: int) -> bool:
        row = self.get(item_id, user_id)
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True

    def _next_sort(self, user_id: int) -> int:
        return self._db.query(Project).filter(Project.user_id == user_id).count()


# ── Certification ─────────────────────────────────────────────────────────────

class CertificationRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_for_user(self, user_id: int) -> list[Certification]:
        return (
            self._db.query(Certification)
            .filter(Certification.user_id == user_id)
            .order_by(Certification.sort_order, Certification.created_at.desc())
            .all()
        )

    def get(self, item_id: int, user_id: int) -> Optional[Certification]:
        return (
            self._db.query(Certification)
            .filter(Certification.id == item_id, Certification.user_id == user_id)
            .first()
        )

    def create(self, user_id: int, data: dict[str, Any]) -> Certification:
        row = Certification(
            user_id=user_id,
            name=data["name"],
            issuer=data["issuer"],
            issue_date=data.get("issue_date", ""),
            expiry_date=data.get("expiry_date", ""),
            credential_id=data.get("credential_id", ""),
            credential_url=data.get("credential_url", ""),
            sort_order=self._next_sort(user_id),
            created_at=_now(),
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return row

    def update(self, item_id: int, user_id: int, data: dict[str, Any]) -> Optional[Certification]:
        row = self.get(item_id, user_id)
        if not row:
            return None
        for k, v in data.items():
            if v is not None:
                setattr(row, k, v)
        self._db.commit()
        self._db.refresh(row)
        return row

    def delete(self, item_id: int, user_id: int) -> bool:
        row = self.get(item_id, user_id)
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True

    def _next_sort(self, user_id: int) -> int:
        return self._db.query(Certification).filter(Certification.user_id == user_id).count()


# ── JobApplication ────────────────────────────────────────────────────────────

class JobApplicationRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_for_user(self, user_id: int) -> list[JobApplication]:
        return (
            self._db.query(JobApplication)
            .filter(JobApplication.user_id == user_id)
            .order_by(JobApplication.created_at.desc())
            .all()
        )

    def get(self, item_id: int, user_id: int) -> Optional[JobApplication]:
        return (
            self._db.query(JobApplication)
            .filter(JobApplication.id == item_id, JobApplication.user_id == user_id)
            .first()
        )

    def get_by_external(self, user_id: int, external_id: str) -> Optional[JobApplication]:
        return (
            self._db.query(JobApplication)
            .filter(JobApplication.user_id == user_id, JobApplication.job_external_id == external_id)
            .first()
        )

    def create(self, user_id: int, data: dict[str, Any]) -> JobApplication:
        row = JobApplication(
            user_id=user_id,
            job_external_id=data["job_external_id"],
            job_title=data.get("job_title", ""),
            company=data.get("company", ""),
            apply_url=data.get("apply_url", ""),
            status="saved",
            resume_id=data.get("resume_id"),
            notes=data.get("notes", ""),
            created_at=_now(),
            updated_at=_now(),
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return row

    def update(self, item_id: int, user_id: int, data: dict[str, Any]) -> Optional[JobApplication]:
        row = self.get(item_id, user_id)
        if not row:
            return None
        if "status" in data and data["status"] == "applied" and not row.applied_at:
            row.applied_at = _now()
        for k, v in data.items():
            if v is not None and k != "status":
                setattr(row, k, v)
        if "status" in data and data["status"] is not None:
            row.status = data["status"]
        row.updated_at = _now()
        self._db.commit()
        self._db.refresh(row)
        return row

    def delete(self, item_id: int, user_id: int) -> bool:
        row = self.get(item_id, user_id)
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True
