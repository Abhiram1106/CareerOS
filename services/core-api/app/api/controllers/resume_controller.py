from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import require_student
from ...models.entities import User
from ...modules.resume.dto.resume_dto import ResumeGenerateRequest
from ...modules.resume.mutation.delete_resume_handler import DeleteResumeHandler
from ...modules.resume.mutation.generate_resume_handler import GenerateResumeHandler
from ...modules.resume.mutation.upload_resume_handler import UploadResumeHandler
from ...modules.resume.query.resume_query_service import ResumeQueryService

router = APIRouter()


@router.post("/resumes/generate")
async def generate_resume(
    payload: ResumeGenerateRequest,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return await GenerateResumeHandler(db).execute(user, payload)


@router.get("/resumes")
def list_resumes(user: User = Depends(require_student), db: Session = Depends(get_db)):
    return ResumeQueryService(db).list_for_user(user).model_dump()


@router.post("/resumes/upload")
async def upload_resume(
    file: UploadFile = File(...),
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return await UploadResumeHandler(db).execute(user, file)


@router.get("/resumes/{resume_id}/sections")
def get_resume_sections(
    resume_id: int,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return ResumeQueryService(db).sections_for_user(user, resume_id).model_dump()


@router.get("/resumes/{resume_id}")
def get_resume(
    resume_id: int,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return ResumeQueryService(db).get_for_user(user, resume_id).model_dump()


@router.delete("/resumes/{resume_id}")
def delete_resume(
    resume_id: int,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return DeleteResumeHandler(db).execute(user, resume_id)
