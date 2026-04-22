import hashlib
import secrets
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import ATSScan, Resume, SessionToken, User
from .schemas import ATSScanRequest, LoginRequest, ProfileUpdateRequest, RegisterRequest, ResumeGenerateRequest
from .services.ats import ats_scan
from .services.jobs import compute_matches

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CareerOS Working Model", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def issue_token(db: Session, user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    db.add(SessionToken(token=token, user_id=user_id, is_active=True))
    db.commit()
    return token


def get_current_user(
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(default=None),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.split(" ", 1)[1]
    session = db.query(SessionToken).filter(SessionToken.token == token, SessionToken.is_active.is_(True)).first()
    if not session:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.get("/")
def root():
    return FileResponse("app/static/index.html")


@app.post("/api/auth/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = issue_token(db, user.id)
    return {"token": token, "user": {"email": user.email, "full_name": user.full_name}}


@app.post("/api/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or user.password_hash != hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = issue_token(db, user.id)
    return {"token": token, "user": {"email": user.email, "full_name": user.full_name}}


@app.get("/api/profile")
def get_profile(user: User = Depends(get_current_user)):
    return {
        "full_name": user.full_name,
        "email": user.email,
        "city": user.city,
        "professional_status": user.professional_status,
        "target_role": user.target_role,
        "skills_csv": user.skills_csv,
        "summary": user.summary,
        "experience_bullet": user.experience_bullet,
    }


@app.put("/api/profile")
def update_profile(payload: ProfileUpdateRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user.full_name = payload.full_name
    user.city = payload.city
    user.professional_status = payload.professional_status
    user.target_role = payload.target_role
    user.skills_csv = payload.skills_csv
    user.summary = payload.summary
    user.experience_bullet = payload.experience_bullet
    db.commit()

    return {"ok": True}


@app.post("/api/resumes/generate")
def generate_resume(payload: ResumeGenerateRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    content = (
        f"{user.full_name}\n"
        f"{user.target_role} | {user.city}\n\n"
        f"Summary\n{user.summary}\n\n"
        f"Experience\n- {user.experience_bullet}\n\n"
        f"Skills\n{user.skills_csv}\n"
    )
    resume = Resume(user_id=user.id, template_name=payload.template_name, content_text=content)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return {"resume_id": resume.id, "content": content}


@app.post("/api/ats/scan")
def scan(payload: ATSScanRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    profile = {
        "full_name": user.full_name,
        "email": user.email,
        "city": user.city,
        "target_role": user.target_role,
        "skills_csv": user.skills_csv,
        "summary": user.summary,
        "experience_bullet": user.experience_bullet,
    }
    result = ats_scan(profile, payload.jd_text)

    scan_row = ATSScan(
        user_id=user.id,
        composite_score=result["composite"],
        keyword_score=result["keyword"],
        format_score=result["format"],
        quality_score=result["quality"],
        completeness_score=result["complete"],
        contact_score=result["contact"],
    )
    db.add(scan_row)
    db.commit()

    return result


@app.get("/api/jobs/matches")
def job_matches(user: User = Depends(get_current_user)):
    profile = {"skills_csv": user.skills_csv, "target_role": user.target_role}
    return {"jobs": compute_matches(profile)}


@app.get("/api/dashboard")
def dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    scans = db.query(ATSScan).filter(ATSScan.user_id == user.id).all()
    resumes = db.query(Resume).filter(Resume.user_id == user.id).count()
    best_score = max((scan.composite_score for scan in scans), default=0)
    matched_jobs = len([j for j in compute_matches({"skills_csv": user.skills_csv, "target_role": user.target_role}) if j["score"] >= 70])

    profile_fields = [user.full_name, user.city, user.target_role, user.skills_csv, user.summary, user.experience_bullet]
    profile_completeness = round(100 * (sum(1 for field in profile_fields if field) / len(profile_fields)))

    return {
        "best_ats_score": best_score,
        "total_resumes": resumes,
        "scans_performed": len(scans),
        "jobs_matched_over_70": matched_jobs,
        "applications_tracked": 0,
        "profile_completeness": profile_completeness,
    }
