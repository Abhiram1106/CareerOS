from __future__ import annotations

import json

from app.models.entities import (
    CareerProfile,
    JobDescription,
    Resume,
    Scorecard,
    User,
)
from app.services.auth import create_session


def _officer(db_session) -> str:
    user = User(
        email="officer-analytics@example.com",
        password_hash="hash",
        full_name="Officer",
        role="officer",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return create_session(db_session, user)


def _seed_scored_student(db_session, *, email: str, bucket: str, missing: list[str]) -> None:
    user = User(email=email, password_hash="hash", full_name=email.split("@")[0], role="student")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    db_session.add(CareerProfile(user_id=user.id, target_role="Software Engineer"))
    resume = Resume(user_id=user.id, template_name="classic", content_text="x", source_format="md")
    db_session.add(resume)
    db_session.commit()
    db_session.refresh(resume)
    jd = JobDescription(
        created_by=user.id,
        company="Acme",
        role="SWE",
        raw_text="Python required",
        skills_json="[]",
    )
    db_session.add(jd)
    db_session.commit()
    db_session.refresh(jd)
    db_session.add(
        Scorecard(
            resume_id=resume.id,
            jd_id=jd.id,
            overall_score=72,
            bucket=bucket,
            score_detail_json=json.dumps({"missing_required_skills": missing}),
        )
    )
    db_session.commit()


def test_officer_heatmap_and_skill_gaps(client, db_session):
    token = _officer(db_session)
    headers = {"Authorization": f"Bearer {token}"}
    _seed_scored_student(db_session, email="a@example.com", bucket="risk", missing=["Python"])
    _seed_scored_student(db_session, email="b@example.com", bucket="ready", missing=["Python", "SQL"])

    heat = client.get("/officer/heatmap", headers=headers)
    assert heat.status_code == 200
    assert len(heat.json()["departments"]) >= 1

    gaps = client.get("/officer/skill-gaps", headers=headers)
    assert gaps.status_code == 200
    items = gaps.json()["items"]
    assert items
    assert items[0]["skill"] == "Python"


def test_officer_create_batch(client, db_session):
    token = _officer(db_session)
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post(
        "/officer/batches",
        json={"name": "CSE 2026", "grad_year": 2026, "dept_id": None},
        headers=headers,
    )
    assert resp.status_code == 200
    batch_id = resp.json()["batch"]["id"]
    listed = client.get("/officer/batches", headers=headers)
    assert any(b["id"] == batch_id for b in listed.json()["batches"])
