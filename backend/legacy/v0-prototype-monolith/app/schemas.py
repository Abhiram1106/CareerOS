from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProfileUpdateRequest(BaseModel):
    full_name: str
    city: str
    professional_status: str
    target_role: str
    skills_csv: str
    summary: str
    experience_bullet: str


class ResumeGenerateRequest(BaseModel):
    template_name: str = "classic"


class ATSScanRequest(BaseModel):
    jd_text: str
