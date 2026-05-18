from .celery_app import celery

from ..database import SessionLocal
from ..models.entities import Resume, ResumeExportJob, User
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
