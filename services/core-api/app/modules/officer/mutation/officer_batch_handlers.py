from __future__ import annotations

import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from ....adapter.db.persistence.officer.officer_batch_repo import OfficerBatchRepo
from ....adapter.db.persistence.resume.resume_repo import ResumeRepo
from ....adapter.db.persistence.resume.resume_section_repo import ResumeSectionRepo
from ....models.entities import User
from ....services.clients import parse_resume_file
from ..dto.officer_dto import OfficerBatchUploadResult, OfficerCreateBatchRequest, OfficerCreateBatchResponse, OfficerBatchItem
from ..officer_scope import ensure_officer_college_id, resolve_officer_college_id


class CreateOfficerBatchHandler:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._batches = OfficerBatchRepo(db)

    def execute(self, officer: User, payload: OfficerCreateBatchRequest) -> OfficerCreateBatchResponse:
        college_id = ensure_officer_college_id(self._db)
        batch = self._batches.create(
            college_id=college_id,
            created_by=officer.id,
            name=payload.name.strip(),
            grad_year=payload.grad_year,
            dept_id=payload.dept_id,
        )
        return OfficerCreateBatchResponse(
            batch=OfficerBatchItem(
                id=batch.id,
                name=batch.name,
                grad_year=batch.grad_year,
                college_id=batch.college_id,
                dept_id=batch.dept_id,
                created_at=batch.created_at.isoformat(),
            )
        )


class UploadOfficerBatchHandler:
    _ALLOWED = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    def __init__(self, db: Session) -> None:
        self._db = db
        self._batches = OfficerBatchRepo(db)
        self._resumes = ResumeRepo(db)
        self._sections = ResumeSectionRepo(db)

    async def execute(self, officer: User, batch_id: int, files: list[UploadFile]) -> OfficerBatchUploadResult:
        batch = self._batches.find_by_id(batch_id)
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")
        college_id = resolve_officer_college_id(self._db)
        if college_id is not None and batch.college_id != college_id:
            raise HTTPException(status_code=404, detail="Batch not found")

        resume_ids: list[int] = []
        errors: list[str] = []

        for file in files:
            try:
                resume_id = await self._ingest_one(batch_id=batch_id, file=file)
                resume_ids.append(resume_id)
            except HTTPException as exc:
                errors.append(f"{file.filename or 'file'}: {exc.detail}")
            except Exception:
                errors.append(f"{file.filename or 'file'}: upload failed")

        return OfficerBatchUploadResult(
            batch_id=batch_id,
            uploaded=len(resume_ids),
            resume_ids=resume_ids,
            errors=errors,
        )

    async def _ingest_one(self, *, batch_id: int, file: UploadFile) -> int:
        ct = file.content_type or ""
        fn = (file.filename or "").lower()
        if ct not in self._ALLOWED:
            if fn.endswith(".pdf"):
                ct = "application/pdf"
            elif fn.endswith(".docx"):
                ct = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            else:
                raise HTTPException(status_code=415, detail="Only PDF and DOCX accepted")

        content = await file.read()
        if len(content) > 5 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File must be under 5 MB")

        source_format = "pdf" if "pdf" in ct else "docx"
        student = self._ensure_intake_student(batch_id=batch_id, filename=file.filename or "resume")
        resume = self._resumes.create_uploaded(user_id=student.id, source_format=source_format)
        parse_result = await parse_resume_file(content, file.filename or f"resume.{source_format}", ct)
        self._sections.add_sections(resume.id, parse_result.get("sections", []))
        self._batches.link_resume(batch_id=batch_id, resume_id=resume.id)
        return resume.id

    def _ensure_intake_student(self, *, batch_id: int, filename: str) -> User:
        slug = uuid.uuid5(uuid.NAMESPACE_OID, f"{batch_id}:{filename}").hex[:12]
        email = f"batch{batch_id}-{slug}@intake.local"
        existing = self._db.query(User).filter(User.email == email).first()
        if existing:
            return existing
        user = User(
            email=email,
            password_hash="intake-no-login",
            full_name=filename.rsplit(".", 1)[0][:120] or "Intake Student",
            role="student",
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user
