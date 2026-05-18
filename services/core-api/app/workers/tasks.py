from .celery_app import celery
import httpx

from ..config import JOB_INTEL_URL
from ..database import SessionLocal
from ..models.entities import AlertNotification, CareerProfile, JobAlert, Resume, ResumeExportJob, User
from ..services.pdf_export import generate_resume_export_file


@celery.task
def health_ping() -> str:
    return "ok"


@celery.task
def generate_resume_export(export_job_id: int) -> str:
    db = SessionLocal()
    try:
        job = db.query(ResumeExportJob).filter(ResumeExportJob.id == export_job_id).first()
        if not job:
            return "missing-job"

        job.status = "processing"
        db.commit()

        resume = db.query(Resume).filter(Resume.id == job.resume_id).first()
        user = db.query(User).filter(User.id == job.user_id).first()
        if not resume or not user:
            job.status = "failed"
            job.error_message = "Resume or user not found"
            db.commit()
            return "missing-input"

        file_path = generate_resume_export_file(user.full_name, resume.content_text, job.id)
        job.status = "completed"
        job.file_path = file_path
        db.commit()
        return file_path
    except Exception as exc:
        if "job" in locals() and job:
            job.status = "failed"
            job.error_message = str(exc)
            db.commit()
        return "failed"
    finally:
        db.close()


@celery.task
def dispatch_job_alerts() -> int:
    db = SessionLocal()
    created = 0
    try:
        alerts = db.query(JobAlert).filter(JobAlert.is_active.is_(True)).all()
        for alert in alerts:
            profile = db.query(CareerProfile).filter(CareerProfile.user_id == alert.user_id).first()
            if not profile:
                continue
            payload = {"target_role": profile.target_role, "skills_csv": profile.skills_csv, "city": profile.city}
            try:
                with httpx.Client(timeout=5) as client:
                    resp = client.post(f"{JOB_INTEL_URL}/matches", json=payload)
                    resp.raise_for_status()
                    jobs = resp.json().get("jobs", [])
            except Exception:
                jobs = []

            matches = [j for j in jobs if j.get("score", 0) >= alert.min_score and (not alert.query or alert.query.lower() in j.get("title", "").lower())]
            for job in matches[:3]:
                exists = (
                    db.query(AlertNotification)
                    .filter(
                        AlertNotification.user_id == alert.user_id,
                        AlertNotification.alert_id == alert.id,
                        AlertNotification.title == f"{job.get('title')} at {job.get('company')}",
                    )
                    .first()
                )
                if exists:
                    continue
                note = AlertNotification(
                    user_id=alert.user_id,
                    alert_id=alert.id,
                    title=f"{job.get('title')} at {job.get('company')}",
                    body=f"Match score: {job.get('score')} | {job.get('location')}",
                )
                db.add(note)
                created += 1
        db.commit()
        return created
    finally:
        db.close()
