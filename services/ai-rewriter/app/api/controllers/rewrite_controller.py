from fastapi import APIRouter

from ...modules.rewrite.dto.resume_prompt_dto import ResumePrompt
from ...modules.rewrite.mutation.generate_resume_handler import GenerateResumeHandler

router = APIRouter()


@router.post("/generate/resume")
def generate_resume(payload: ResumePrompt):
    return GenerateResumeHandler().execute(payload)
