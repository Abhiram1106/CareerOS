from pydantic import BaseModel


class ResumePrompt(BaseModel):
    full_name: str
    target_role: str
    city: str
    skills_csv: str
    summary: str
    experience_bullet: str
    template_name: str


class ResumeGenerateResponse(BaseModel):
    content: str
