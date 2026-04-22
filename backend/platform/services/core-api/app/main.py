from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session

from .database import get_db
from .db_bootstrap import DatabaseNotReadyError, bootstrap_database
from .dependencies import current_user
from .models.entities import (
    ATSScan,
    AlertNotification,
    ApplicationTrack,
    CareerProfile,
    JobAlert,
    PaymentTransaction,
    Resume,
    ResumeExportJob,
    Subscription,
    User,
)
from .schemas.contracts import (
    ATSScanRequest,
    ApplicationCreate,
    ApplicationUpdate,
    CheckoutRequest,
    ExportResumeRequest,
    JobAlertCreate,
    LoginRequest,
    ProfileUpsert,
    RegisterRequest,
    ResumeGenerateRequest,
    SubscribeRequest,
)
from .services.auth import create_session, hash_password, verify_password
from .services.clients import (
    generate_resume_content,
    get_job_matches,
    nexus_delete,
    nexus_get,
    nexus_patch,
    nexus_post,
    run_ats_scan,
)
from .services.payment import (
    PaymentError,
    create_checkout,
    get_plans,
    parse_razorpay_webhook,
    parse_stripe_webhook,
    plan_amount_inr,
)
from .services.pdf_export import generate_download_target, infer_filename
from .workers.tasks import dispatch_job_alerts, generate_resume_export

app = FastAPI(title="CareerOS Core API", version="0.2.0")
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
        # Local fallback when broker is unavailable.
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


@app.post("/nexus-ats/requisitions")
async def nexus_create_requisition(payload: dict, user=Depends(current_user), db: Session = Depends(get_db)):
    profile = db.query(CareerProfile).filter(CareerProfile.user_id == user.id).first()
    data = {
        "org_id": "nexus-default-org",
        "title": payload.get("title", "New Requisition"),
        "department": payload.get("department", ""),
        "hiring_manager_id": payload.get("hiring_manager_id", str(user.id)),
        "recruiter_id": payload.get("recruiter_id", str(user.id)),
        "location_type": payload.get("location_type", "onsite"),
        "description_raw": payload.get("description_raw", ""),
        "required_skills_csv": payload.get("required_skills_csv", profile.skills_csv if profile else ""),
    }
    return await nexus_post("/api/v1/requisitions", data)


@app.get("/nexus-ats/requisitions")
async def nexus_list_requisitions(status: str | None = None, q: str | None = None, user=Depends(current_user)):
    params = {}
    if status:
        params["status"] = status
    if q:
        params["q"] = q
    return await nexus_get("/api/v1/requisitions", params=params)


@app.post("/nexus-ats/candidates")
async def nexus_upsert_candidate(payload: dict, user=Depends(current_user), db: Session = Depends(get_db)):
    profile = db.query(CareerProfile).filter(CareerProfile.user_id == user.id).first()
    data = {
        "email": payload.get("email", user.email),
        "full_name": payload.get("full_name", user.full_name),
        "phone": payload.get("phone", ""),
        "headline": payload.get("headline", profile.target_role if profile else ""),
        "location": payload.get("location", profile.city if profile else ""),
        "linkedin_url": payload.get("linkedin_url", ""),
        "skills_csv": payload.get("skills_csv", profile.skills_csv if profile else ""),
        "resume_text": payload.get("resume_text", profile.summary if profile else ""),
    }
    return await nexus_post("/api/v1/candidates", data)


@app.get("/nexus-ats/candidates")
async def nexus_list_candidates(q: str | None = None, user=Depends(current_user)):
    params = {"q": q} if q else None
    return await nexus_get("/api/v1/candidates", params=params)


@app.post("/nexus-ats/applications")
async def nexus_create_application(payload: dict, user=Depends(current_user)):
    data = {
        "org_id": "nexus-default-org",
        "candidate_id": payload.get("candidate_id"),
        "requisition_id": payload.get("requisition_id"),
        "source_channel": payload.get("source_channel", "direct"),
    }
    return await nexus_post("/api/v1/applications", data)


@app.get("/nexus-ats/applications")
async def nexus_list_applications(requisition_id: str | None = None, candidate_id: str | None = None, user=Depends(current_user)):
    params = {}
    if requisition_id:
        params["requisition_id"] = requisition_id
    if candidate_id:
        params["candidate_id"] = candidate_id
    return await nexus_get("/api/v1/applications", params=params if params else None)


@app.post("/nexus-ats/applications/{application_id}/stage")
async def nexus_move_application_stage(application_id: str, payload: dict, user=Depends(current_user)):
    data = {
        "stage_id": payload.get("stage_id", "screening"),
        "stage_name": payload.get("stage_name", "Screening"),
        "note": payload.get("note", ""),
    }
    return await nexus_post(f"/api/v1/applications/{application_id}/stage", data)


@app.get("/nexus-ats/requisitions/{req_id}/analytics")
async def nexus_requisition_analytics(req_id: str, user=Depends(current_user)):
    return await nexus_get(f"/api/v1/requisitions/{req_id}/analytics")


@app.post("/nexus-ats/ai/match")
async def nexus_ai_match(payload: dict, user=Depends(current_user)):
    data = {"candidate_id": payload.get("candidate_id"), "requisition_id": payload.get("requisition_id")}
    return await nexus_post("/api/v1/ai/match", data)


@app.post("/nexus-ats/interviews")
async def nexus_create_interview(payload: dict, user=Depends(current_user)):
    data = {
        "application_id": payload.get("application_id"),
        "interview_type": payload.get("interview_type", "live"),
        "scheduled_at": payload.get("scheduled_at"),
        "timezone": payload.get("timezone", "UTC"),
        "panel_csv": payload.get("panel_csv", ""),
    }
    return await nexus_post("/api/v1/interviews", data)


@app.post("/nexus-ats/interviews/{interview_id}/confirm")
async def nexus_confirm_interview(interview_id: str, user=Depends(current_user)):
    return await nexus_post(f"/api/v1/interviews/{interview_id}/confirm", {})


@app.post("/nexus-ats/scorecards")
async def nexus_create_scorecard(payload: dict, user=Depends(current_user)):
    data = {
        "interview_id": payload.get("interview_id"),
        "application_id": payload.get("application_id"),
        "reviewer_id": payload.get("reviewer_id", str(user.id)),
        "competency_scores": payload.get("competency_scores", "{}"),
        "recommendation": payload.get("recommendation", "hold"),
        "comments": payload.get("comments", ""),
    }
    return await nexus_post("/api/v1/scorecards", data)


@app.post("/nexus-ats/offers")
async def nexus_create_offer(payload: dict, user=Depends(current_user)):
    data = {"application_id": payload.get("application_id"), "base_salary": payload.get("base_salary", 0), "currency": payload.get("currency", "USD")}
    return await nexus_post("/api/v1/offers", data)


@app.post("/nexus-ats/offers/{offer_id}/send")
async def nexus_send_offer(offer_id: str, user=Depends(current_user)):
    return await nexus_post(f"/api/v1/offers/{offer_id}/send", {})


@app.post("/nexus-ats/offers/{offer_id}/respond")
async def nexus_respond_offer(offer_id: str, payload: dict, user=Depends(current_user)):
    return await nexus_post(f"/api/v1/offers/{offer_id}/respond", {"action": payload.get("action", "accepted")})


@app.get("/nexus-ats/webhooks/events")
async def nexus_webhook_events(event_name: str | None = None, user=Depends(current_user)):
    params = {"event_name": event_name} if event_name else None
    return await nexus_get("/api/v1/webhooks/events", params=params)


@app.get("/nexus-ats/requisitions/{req_id}")
async def nexus_get_requisition(req_id: str, user=Depends(current_user)):
    return await nexus_get(f"/api/v1/requisitions/{req_id}")


@app.patch("/nexus-ats/requisitions/{req_id}")
async def nexus_update_requisition(req_id: str, payload: dict, user=Depends(current_user)):
    return await nexus_patch(f"/api/v1/requisitions/{req_id}", payload)


@app.post("/nexus-ats/requisitions/{req_id}/publish")
async def nexus_publish_requisition(req_id: str, payload: dict, user=Depends(current_user)):
    return await nexus_post(
        f"/api/v1/requisitions/{req_id}/publish",
        {"boards": payload.get("boards", []), "schedule_at": payload.get("schedule_at")},
    )


@app.post("/nexus-ats/requisitions/{req_id}/approve")
async def nexus_approve_requisition(req_id: str, payload: dict, user=Depends(current_user)):
    return await nexus_post(
        f"/api/v1/requisitions/{req_id}/approve",
        {"decision": payload.get("decision", "approved"), "notes": payload.get("notes", "")},
    )


@app.post("/nexus-ats/requisitions/{req_id}/close")
async def nexus_close_requisition(req_id: str, payload: dict, user=Depends(current_user)):
    return await nexus_post(
        f"/api/v1/requisitions/{req_id}/close",
        {"reason": payload.get("reason", "filled"), "hired_application_id": payload.get("hired_application_id")},
    )


@app.get("/nexus-ats/candidates/{candidate_id}")
async def nexus_get_candidate(candidate_id: str, user=Depends(current_user)):
    return await nexus_get(f"/api/v1/candidates/{candidate_id}")


@app.patch("/nexus-ats/candidates/{candidate_id}")
async def nexus_update_candidate(candidate_id: str, payload: dict, user=Depends(current_user)):
    return await nexus_patch(f"/api/v1/candidates/{candidate_id}", payload)


@app.delete("/nexus-ats/candidates/{candidate_id}")
async def nexus_delete_candidate(candidate_id: str, user=Depends(current_user)):
    return await nexus_delete(f"/api/v1/candidates/{candidate_id}")


@app.post("/nexus-ats/candidates/{candidate_id}/resume")
async def nexus_upload_candidate_resume(candidate_id: str, payload: dict, user=Depends(current_user)):
    return await nexus_post(f"/api/v1/candidates/{candidate_id}/resume", {"text": payload.get("text", "")})


@app.get("/nexus-ats/candidates/{candidate_id}/similar")
async def nexus_similar_candidates(candidate_id: str, top_n: int = 10, source: str = "all", user=Depends(current_user)):
    return await nexus_get(
        f"/api/v1/candidates/{candidate_id}/similar",
        params={"top_n": top_n, "source": source},
    )


@app.post("/nexus-ats/candidates/{candidate_id}/gdpr/export")
async def nexus_candidate_gdpr_export(candidate_id: str, user=Depends(current_user)):
    return await nexus_post(f"/api/v1/candidates/{candidate_id}/gdpr/export", {})


@app.post("/nexus-ats/candidates/search")
async def nexus_candidate_search(payload: dict, user=Depends(current_user)):
    return await nexus_post(
        "/api/v1/candidates/search",
        {"query": payload.get("query", ""), "skill_ids": payload.get("skill_ids", []), "include_internal": payload.get("include_internal", True)},
    )


@app.get("/nexus-ats/candidates/{candidate_id}/match/{req_id}")
async def nexus_candidate_match(candidate_id: str, req_id: str, user=Depends(current_user)):
    return await nexus_get(f"/api/v1/candidates/{candidate_id}/match/{req_id}")


@app.patch("/nexus-ats/applications/{application_id}/status")
async def nexus_set_application_status(application_id: str, payload: dict, user=Depends(current_user)):
    return await nexus_patch(
        f"/api/v1/applications/{application_id}/status",
        {"status": payload.get("status", ""), "note": payload.get("note", "")},
    )


@app.post("/nexus-ats/applications/{application_id}/reject")
async def nexus_reject_application(application_id: str, payload: dict, user=Depends(current_user)):
    return await nexus_post(f"/api/v1/applications/{application_id}/reject", {"reason": payload.get("reason", "Not selected")})


@app.get("/nexus-ats/applications/bulk")
async def nexus_bulk_applications(user=Depends(current_user)):
    return await nexus_get("/api/v1/applications/bulk")


@app.post("/nexus-ats/ai/parse-resume")
async def nexus_ai_parse_resume(payload: dict, user=Depends(current_user)):
    return await nexus_post("/api/v1/ai/parse-resume", {"text": payload.get("text", "")})


@app.post("/nexus-ats/ai/jd-enhance")
async def nexus_ai_jd_enhance(payload: dict, user=Depends(current_user)):
    return await nexus_post("/api/v1/ai/jd-enhance", {"jd_text": payload.get("jd_text", "")})


@app.post("/nexus-ats/ai/predict/time-to-fill")
async def nexus_ai_predict_ttf(payload: dict, user=Depends(current_user)):
    return await nexus_post("/api/v1/ai/predict/time-to-fill", {"requisition_id": payload.get("requisition_id")})


@app.post("/nexus-ats/ai/predict/offer-acceptance")
async def nexus_ai_predict_offer_acceptance(payload: dict, user=Depends(current_user)):
    return await nexus_post(
        "/api/v1/ai/predict/offer-acceptance",
        {"application_id": payload.get("application_id"), "offer_params": payload.get("offer_params", {})},
    )


@app.post("/nexus-ats/ai/bias-scan/pipeline")
async def nexus_ai_bias_scan(payload: dict, user=Depends(current_user)):
    return await nexus_post(
        "/api/v1/ai/bias-scan/pipeline",
        {"requisition_id": payload.get("requisition_id"), "stage_id": payload.get("stage_id")},
    )


@app.post("/nexus-ats/ai/scorecard-insights")
async def nexus_ai_scorecard_insights(payload: dict, user=Depends(current_user)):
    return await nexus_post("/api/v1/ai/scorecard-insights", {"application_id": payload.get("application_id")})


@app.post("/nexus-ats/ai/talent-rediscovery")
async def nexus_ai_talent_rediscovery(payload: dict, user=Depends(current_user)):
    return await nexus_post(
        "/api/v1/ai/talent-rediscovery",
        {
            "requisition_id": payload.get("requisition_id"),
            "max_results": payload.get("max_results", 20),
            "min_match_score": payload.get("min_match_score", 60),
        },
    )


@app.post("/nexus-ats/ai/chat/candidate")
async def nexus_ai_chat_candidate(payload: dict, user=Depends(current_user)):
    return await nexus_post(
        "/api/v1/ai/chat/candidate",
        {
            "session_id": payload.get("session_id", f"user-{user.id}"),
            "message": payload.get("message", ""),
            "application_id": payload.get("application_id"),
        },
    )


@app.post("/nexus-ats/ai/chat/recruiter")
async def nexus_ai_chat_recruiter(payload: dict, user=Depends(current_user)):
    return await nexus_post(
        "/api/v1/ai/chat/recruiter",
        {"session_id": payload.get("session_id", f"user-{user.id}"), "message": payload.get("message", ""), "context": payload.get("context", {})},
    )


@app.get("/jobs/matches")
async def jobs_matches(user=Depends(current_user), db: Session = Depends(get_db)):
    profile = db.query(CareerProfile).filter(CareerProfile.user_id == user.id).first()
    payload = {"target_role": profile.target_role, "skills_csv": profile.skills_csv, "city": profile.city}
    return await get_job_matches(payload)


@app.post("/jobs/alerts")
def create_job_alert(payload: JobAlertCreate, user=Depends(current_user), db: Session = Depends(get_db)):
    row = JobAlert(user_id=user.id, query=payload.query, location=payload.location, min_score=payload.min_score, is_active=True)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "query": row.query, "location": row.location, "min_score": row.min_score, "is_active": row.is_active}


@app.get("/jobs/alerts")
def list_job_alerts(user=Depends(current_user), db: Session = Depends(get_db)):
    rows = db.query(JobAlert).filter(JobAlert.user_id == user.id).order_by(JobAlert.created_at.desc()).all()
    return {
        "alerts": [
            {"id": row.id, "query": row.query, "location": row.location, "min_score": row.min_score, "is_active": row.is_active}
            for row in rows
        ]
    }


@app.delete("/jobs/alerts/{alert_id}")
def delete_job_alert(alert_id: int, user=Depends(current_user), db: Session = Depends(get_db)):
    row = db.query(JobAlert).filter(JobAlert.id == alert_id, JobAlert.user_id == user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(row)
    db.commit()
    return {"ok": True}


@app.post("/jobs/alerts/dispatch")
def dispatch_alerts(user=Depends(current_user)):
    # Trigger asynchronous dispatch sweep.
    try:
        dispatch_job_alerts.delay()
    except Exception:
        dispatch_job_alerts.apply()
    return {"ok": True}


@app.get("/jobs/alerts/notifications")
def list_notifications(user=Depends(current_user), db: Session = Depends(get_db)):
    rows = (
        db.query(AlertNotification)
        .filter(AlertNotification.user_id == user.id)
        .order_by(AlertNotification.created_at.desc())
        .all()
    )
    return {
        "notifications": [
            {"id": row.id, "title": row.title, "body": row.body, "is_read": row.is_read, "created_at": row.created_at.isoformat()}
            for row in rows
        ]
    }


@app.put("/jobs/alerts/notifications/{notification_id}/read")
def mark_notification_read(notification_id: int, user=Depends(current_user), db: Session = Depends(get_db)):
    row = (
        db.query(AlertNotification)
        .filter(AlertNotification.id == notification_id, AlertNotification.user_id == user.id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Notification not found")
    row.is_read = True
    db.commit()
    return {"ok": True}


@app.post("/applications")
def create_application(payload: ApplicationCreate, user=Depends(current_user), db: Session = Depends(get_db)):
    row = ApplicationTrack(user_id=user.id, company=payload.company, role=payload.role, status=payload.status, notes=payload.notes)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "company": row.company, "role": row.role, "status": row.status, "notes": row.notes, "applied_on": row.applied_on.isoformat()}


@app.get("/applications")
def list_applications(user=Depends(current_user), db: Session = Depends(get_db)):
    rows = db.query(ApplicationTrack).filter(ApplicationTrack.user_id == user.id).order_by(ApplicationTrack.applied_on.desc()).all()
    return {
        "applications": [
            {"id": row.id, "company": row.company, "role": row.role, "status": row.status, "notes": row.notes, "applied_on": row.applied_on.isoformat()}
            for row in rows
        ]
    }


@app.put("/applications/{application_id}")
def update_application(application_id: int, payload: ApplicationUpdate, user=Depends(current_user), db: Session = Depends(get_db)):
    row = db.query(ApplicationTrack).filter(ApplicationTrack.id == application_id, ApplicationTrack.user_id == user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")
    row.status = payload.status
    row.notes = payload.notes
    db.commit()
    return {"ok": True}


@app.delete("/applications/{application_id}")
def delete_application(application_id: int, user=Depends(current_user), db: Session = Depends(get_db)):
    row = db.query(ApplicationTrack).filter(ApplicationTrack.id == application_id, ApplicationTrack.user_id == user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(row)
    db.commit()
    return {"ok": True}


@app.get("/billing/plans")
def billing_plans():
    return {"plans": get_plans()}


@app.post("/billing/subscribe")
def subscribe(payload: SubscribeRequest, user=Depends(current_user), db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.user_id == user.id).first()
    if not sub:
        sub = Subscription(user_id=user.id, plan_code=payload.plan_code, status="active")
        db.add(sub)
    else:
        sub.plan_code = payload.plan_code
        sub.status = "active"
    db.commit()
    return {"ok": True, "plan_code": payload.plan_code, "status": "active"}


@app.post("/billing/checkout")
def billing_checkout(payload: CheckoutRequest, user=Depends(current_user), db: Session = Depends(get_db)):
    try:
        amount = plan_amount_inr(payload.plan_code)
    except PaymentError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    tx = PaymentTransaction(
        user_id=user.id,
        provider=payload.provider,
        plan_code=payload.plan_code,
        amount_inr=amount,
        currency="INR",
        status="created",
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    try:
        checkout = create_checkout(
            provider=payload.provider,
            plan_code=payload.plan_code,
            transaction_id=tx.id,
            amount_inr=amount,
            email=user.email,
            full_name=user.full_name,
        )
    except PaymentError as exc:
        tx.status = "failed"
        db.commit()
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    tx.external_ref = str(checkout.get("external_ref", ""))
    db.commit()
    return {"transaction_id": tx.id, **checkout}


@app.post("/billing/webhook/{provider}")
async def billing_webhook(provider: str, request: Request, db: Session = Depends(get_db)):
    raw_body = await request.body()
    headers = {k.lower(): v for k, v in request.headers.items()}

    try:
        if provider == "stripe":
            data = parse_stripe_webhook(raw_body, headers)
        elif provider == "razorpay":
            data = parse_razorpay_webhook(raw_body, headers)
        else:
            raise HTTPException(status_code=400, detail="Unsupported provider")
    except HTTPException:
        raise
    except PaymentError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Webhook parse failed: {exc}") from exc

    if data.get("ignore"):
        return {"ok": True, "ignored": data.get("reason", "event ignored")}

    tx = None
    transaction_id = data.get("transaction_id")
    if transaction_id:
        tx = db.query(PaymentTransaction).filter(PaymentTransaction.id == int(transaction_id)).first()
    if not tx and data.get("external_ref"):
        tx = (
            db.query(PaymentTransaction)
            .filter(PaymentTransaction.provider == provider, PaymentTransaction.external_ref == str(data.get("external_ref")))
            .first()
        )
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    status = str(data.get("status", ""))
    tx.status = status or tx.status
    if data.get("external_ref") and not tx.external_ref:
        tx.external_ref = str(data.get("external_ref"))

    if status in {"paid", "captured", "succeeded"}:
        target_plan = str(data.get("plan_code") or tx.plan_code)
        sub = db.query(Subscription).filter(Subscription.user_id == tx.user_id).first()
        if not sub:
            sub = Subscription(user_id=tx.user_id, plan_code=target_plan, status="active")
            db.add(sub)
        else:
            sub.plan_code = target_plan
            sub.status = "active"
    db.commit()
    return {"ok": True}


@app.get("/billing/me")
def my_subscription(user=Depends(current_user), db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.user_id == user.id).first()
    if not sub:
        return {"plan_code": "free", "status": "active"}
    return {"plan_code": sub.plan_code, "status": sub.status, "renews_on": sub.renews_on.isoformat()}


@app.get("/dashboard")
async def dashboard(user=Depends(current_user), db: Session = Depends(get_db)):
    profile = db.query(CareerProfile).filter(CareerProfile.user_id == user.id).first()
    scans = db.query(ATSScan).filter(ATSScan.user_id == user.id).all()
    resumes_count = db.query(Resume).filter(Resume.user_id == user.id).count()
    applications_count = db.query(ApplicationTrack).filter(ApplicationTrack.user_id == user.id).count()
    jobs = await get_job_matches({"target_role": profile.target_role, "skills_csv": profile.skills_csv, "city": profile.city})

    best_ats = max((s.composite_score for s in scans), default=0)
    fields = [profile.city, profile.professional_status, profile.target_role, profile.skills_csv, profile.summary, profile.experience_bullet]
    profile_completeness = round(100 * (sum(1 for f in fields if f) / len(fields)))

    return {
        "best_ats_score": best_ats,
        "total_resumes": resumes_count,
        "scans_performed": len(scans),
        "jobs_matched_over_70": len([j for j in jobs["jobs"] if j["score"] >= 70]),
        "applications_tracked": applications_count,
        "profile_completeness": profile_completeness,
    }
