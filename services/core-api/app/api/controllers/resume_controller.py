from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile

from ...dependencies import (
    get_delete_resume_handler,
    get_generate_resume_handler,
    get_resume_query_service,
    get_upload_resume_handler,
    require_student,
)
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
    handler: GenerateResumeHandler = Depends(get_generate_resume_handler),
):
    return await handler.execute(user, payload)


@router.get("/resumes")
def list_resumes(
    user: User = Depends(require_student),
    service: ResumeQueryService = Depends(get_resume_query_service),
):
    return service.list_for_user(user).model_dump()


@router.post("/resumes/upload")
async def upload_resume(
    file: UploadFile = File(...),
    user: User = Depends(require_student),
    handler: UploadResumeHandler = Depends(get_upload_resume_handler),
):
    return await handler.execute(user, file)


@router.get("/resumes/{resume_id}/sections")
def get_resume_sections(
    resume_id: int,
    user: User = Depends(require_student),
    service: ResumeQueryService = Depends(get_resume_query_service),
):
    return service.sections_for_user(user, resume_id).model_dump()


@router.get("/resumes/{resume_id}")
def get_resume(
    resume_id: int,
    user: User = Depends(require_student),
    service: ResumeQueryService = Depends(get_resume_query_service),
):
    return service.get_for_user(user, resume_id).model_dump()


@router.delete("/resumes/{resume_id}")
def delete_resume(
    resume_id: int,
    user: User = Depends(require_student),
    handler: DeleteResumeHandler = Depends(get_delete_resume_handler),
):
    return handler.execute(user, resume_id)
