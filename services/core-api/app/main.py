from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session

from .database import get_db
from .db_bootstrap import DatabaseNotReadyError, bootstrap_database
from .dependencies import current_user
from .models.entities import (
    ATSScan,
    CareerProfile,
    Resume,
    ResumeExportJob,
    User,
)
from .schemas.contracts import (
    ATSScanRequest,
    ExportResumeRequest,
    LoginRequest,
    ProfileUpsert,
    RegisterRequest,
    ResumeGenerateRequest,
)
from .services.auth import create_session, hash_password, verify_password
from .services.clients import generate_resume_content, run_ats_scan
from .services.pdf_export import generate_download_target, infer_filename
from .workers.tasks import generate_resume_export

app = FastAPI(title="CareerOS Campus AI — Core API", version="0.3.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def startup_db_guard():
    try:
        bootstrap_database()
    except DatabaseNotReadyError as exc:
        raise RuntimeError(str(exc)) from exc


@app.post("/auth/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(email=payload.email, password_hash=hash_password(payload.password), full_name=payload.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)

    profile = CareerProfile(user_id=user.id)
    db.add(profile)
    db.commit()

    token = create_session(db, user)
    return {"token": token, "email": user.email, "full_name": user.full_name}


@app.post("/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_session(db, user)
    return {"token": token, "email": user.email, "full_name": user.full_name}


@app.get("/profile")
def get_profile(user=Depends(current_user), db: Session = Depends(get_db)):
    profile = db.query(CareerProfile).filter(CareerProfile.user_id == user.id).first()
    return {
        "full_name": user.full_name,
        "email": user.email,
        "city": profile.city,
        "professional_status": profile.professional_status,
        "target_role": profile.target_role,
        "skills_csv": profile.skills_csv,
        "summary": profile.summary,
        "experience_bullet": profile.experience_bullet,
    }


@app.put("/profile")
def update_profile(payload: ProfileUpsert, user=Depends(current_user), db: Session = Depends(get_db)):
    profile = db.query(CareerProfile).filter(CareerProfile.user_id == user.id).first()
    if not profile:
        profile = CareerProfile(user_id=user.id)
        db.add(profile)

    profile.city = payload.city
    profile.professional_status = payload.professional_status
    profile.target_role = payload.target_role
    profile.skills_csv = payload.skills_csv
    profile.summary = payload.summary
    profile.experience_bullet = payload.experience_bullet
    db.commit()
    return {"ok": True}


@app.post("/resumes/generate")
async def generate_resume(payload: ResumeGenerateRequest, user=Depends(current_user), db: Session = Depends(get_db)):
    profile = db.query(CareerProfile).filter(CareerProfile.user_id == user.id).first()
    ai_payload = {
        "full_name": user.full_name,
        "target_role": profile.target_role,
        "city": profile.city,
        "skills_csv": profile.skills_csv,
        "summary": profile.summary,
        "experience_bullet": profile.experience_bullet,
        "template_name": payload.template_name,
    }
    generated = await generate_resume_content(ai_payload)

    resume = Resume(user_id=user.id, template_name=payload.template_name, content_text=generated["content"])
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {"resume_id": resume.id, "content": resume.content_text}


@app.get("/resumes")
def list_resumes(user=Depends(current_user), db: Session = Depends(get_db)):
    rows = db.query(Resume).filter(Resume.user_id == user.id).order_by(Resume.created_at.desc()).all()
    return {
        "resumes": [
            {"id": row.id, "template_name": row.template_name, "created_at": row.created_at.isoformat()}
            for row in rows
        ]
    }


@app.get("/resumes/{resume_id}")
def get_resume(resume_id: int, user=Depends(current_user), db: Session = Depends(get_db)):
    row = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {
        "id": row.id,
        "template_name": row.template_name,
        "content": row.content_text,
        "created_at": row.created_at.isoformat(),
    }


@app.delete("/resumes/{resume_id}")
def delete_resume(resume_id: int, user=Depends(current_user), db: Session = Depends(get_db)):
    row = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Resume not found")
    db.delete(row)
    db.commit()
    return {"ok": True}


@app.post("/resumes/export")
def export_resume(payload: ExportResumeRequest, user=Depends(current_user), db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == payload.resume_id, Resume.user_id == user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    job = ResumeExportJob(user_id=user.id, resume_id=resume.id, status="queued")
    db.add(job)
    db.commit()
    db.refresh(job)
    try:
        generate_resume_export.delay(job.id)
    except Exception:
        generate_resume_export.apply(args=[job.id])
    return {"job_id": job.id, "status": job.status}


@app.get("/resumes/export/{job_id}")
def export_status(job_id: int, user=Depends(current_user), db: Session = Depends(get_db)):
    job = db.query(ResumeExportJob).filter(ResumeExportJob.id == job_id, ResumeExportJob.user_id == user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Export job not found")
    return {"job_id": job.id, "status": job.status, "error_message": job.error_message, "has_file": bool(job.file_path)}


@app.get("/resumes/export/{job_id}/download")
def export_download(job_id: int, user=Depends(current_user), db: Session = Depends(get_db)):
    job = db.query(ResumeExportJob).filter(ResumeExportJob.id == job_id, ResumeExportJob.user_id == user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Export job not found")
    if job.status != "completed" or not job.file_path:
        raise HTTPException(status_code=400, detail="Export not ready")
    kind, value = generate_download_target(job.file_path)
    if kind == "redirect":
        return RedirectResponse(url=value, status_code=307)

    path = Path(value)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Export file missing")
    return FileResponse(path=str(path), filename=infer_filename(job.file_path), media_type="application/pdf")


@app.post("/ats/scan")
async def ats_scan(payload: ATSScanRequest, user=Depends(current_user), db: Session = Depends(get_db)):
    profile = db.query(CareerProfile).filter(CareerProfile.user_id == user.id).first()
    scan_payload = {
        "full_name": user.full_name,
        "email": user.email,
        "city": profile.city,
        "target_role": profile.target_role,
        "skills_csv": profile.skills_csv,
        "summary": profile.summary,
        "experience_bullet": profile.experience_bullet,
        "jd_text": payload.jd_text,
    }
    result = await run_ats_scan(scan_payload)

    row = ATSScan(
        user_id=user.id,
        composite_score=result["composite"],
        keyword_score=result["keyword"],
        format_score=result["format"],
        quality_score=result["quality"],
        completeness_score=result["complete"],
        contact_score=result["contact"],
    )
    db.add(row)
    db.commit()
    return result


@app.get("/ats/scans")
def ats_history(user=Depends(current_user), db: Session = Depends(get_db)):
    scans = db.query(ATSScan).filter(ATSScan.user_id == user.id).order_by(ATSScan.created_at.desc()).all()
    return {
        "scans": [
            {
                "id": scan.id,
                "composite_score": scan.composite_score,
                "keyword_score": scan.keyword_score,
                "format_score": scan.format_score,
                "quality_score": scan.quality_score,
                "completeness_score": scan.completeness_score,
                "contact_score": scan.contact_score,
                "created_at": scan.created_at.isoformat(),
            }
            for scan in scans
        ]
    }


@app.get("/dashboard")
def dashboard(user=Depends(current_user), db: Session = Depends(get_db)):
    profile = db.query(CareerProfile).filter(CareerProfile.user_id == user.id).first()
    scans = db.query(ATSScan).filter(ATSScan.user_id == user.id).all()
    resumes_count = db.query(Resume).filter(Resume.user_id == user.id).count()

    best_ats = max((s.composite_score for s in scans), default=0)
    fields = [profile.city, profile.professional_status, profile.target_role, profile.skills_csv, profile.summary, profile.experience_bullet]
    profile_completeness = round(100 * (sum(1 for f in fields if f) / len(fields)))

    return {
        "best_ats_score": best_ats,
        "total_resumes": resumes_count,
        "scans_performed": len(scans),
        "profile_completeness": profile_completeness,
    }
