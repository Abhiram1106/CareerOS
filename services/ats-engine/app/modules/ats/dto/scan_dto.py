from pydantic import BaseModel


class ScanRequest(BaseModel):
    full_name: str
    email: str
    city: str
    target_role: str
    skills_csv: str
    summary: str
    experience_bullet: str
    jd_text: str


class ScanResponse(BaseModel):
    composite: float
    keyword: float
    format: float
    quality: float
    complete: float
    contact: float
