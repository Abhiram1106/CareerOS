from fastapi import APIRouter, File, UploadFile

from ...modules.parse.mutation.parse_resume_handler import ParseResumeHandler

router = APIRouter()


@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    return await ParseResumeHandler().execute(file)
