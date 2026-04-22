from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    email: EmailStr
    full_name: str


class ProfileUpsert(BaseModel):
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


class ATSScanResponse(BaseModel):
    composite: float
    keyword: float
    format: float
    quality: float
    complete: float
    contact: float


class JobAlertCreate(BaseModel):
    query: str
    location: str
    min_score: int = 70


class JobAlertResponse(BaseModel):
    id: int
    query: str
    location: str
    min_score: int
    is_active: bool


class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: str = "applied"
    notes: str = ""


class ApplicationUpdate(BaseModel):
    status: str
    notes: str = ""


class ApplicationResponse(BaseModel):
    id: int
    company: str
    role: str
    status: str
    notes: str
    applied_on: str


class SubscribeRequest(BaseModel):
    plan_code: str


class CheckoutRequest(BaseModel):
    provider: str
    plan_code: str


class ExportResumeRequest(BaseModel):
    resume_id: int
