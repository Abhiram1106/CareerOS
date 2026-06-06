import argparse
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.db_bootstrap import bootstrap_database
from app.models.entities import (
    ATSScan,
    JobApplication,
    CareerProfile,
    Resume,
    User,
)
from app.services.auth import hash_password


def seed(email: str, password: str, full_name: str) -> None:
    bootstrap_database()
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(email=email, password_hash=hash_password(password), full_name=full_name)
            db.add(user)
            db.commit()
            db.refresh(user)

        profile = db.query(CareerProfile).filter(CareerProfile.user_id == user.id).first()
        if not profile:
            profile = CareerProfile(
                user_id=user.id,
                city="Bengaluru",
                professional_status="Fresher",
                target_role="Software Engineer",
                skills_csv="Python,FastAPI,SQL,React",
                summary="Backend-leaning engineer focused on API reliability and product velocity.",
                experience_bullet="Built internal tools that reduced manual reporting time by 40%.",
            )
            db.add(profile)

        if db.query(Resume).filter(Resume.user_id == user.id).count() == 0:
            db.add(
                Resume(
                    user_id=user.id,
                    template_name="classic",
                    content_text=f"{full_name}\nSoftware Engineer\nSkills: Python, FastAPI, SQL, React",
                )
            )

        if db.query(ATSScan).filter(ATSScan.user_id == user.id).count() == 0:
            db.add(
                ATSScan(
                    user_id=user.id,
                    composite_score=78.0,
                    keyword_score=80.0,
                    format_score=85.0,
                    quality_score=74.0,
                    completeness_score=76.0,
                    contact_score=95.0,
                )
            )

        if db.query(JobApplication).filter(JobApplication.user_id == user.id).count() == 0:
            db.add(
                JobApplication(
                    user_id=user.id,
                    company="Example Labs",
                    job_title="Backend Engineer",
                    status="applied",
                    notes="Referred by alumni network",
                    job_external_id="seed-12345"
                )
            )

        db.commit()
        print(f"Seed complete for user: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed CareerOS Core API dev data")
    parser.add_argument("--email", default="demo@careeros.dev")
    parser.add_argument("--password", default="DemoPass123")
    parser.add_argument("--full-name", default="Demo User")
    args = parser.parse_args()
    seed(email=args.email, password=args.password, full_name=args.full_name)
