"""IDOR and RBAC tests — cross-user access must fail closed."""

from __future__ import annotations

import json

from app.adapter.db.persistence.agent_run.agent_run_repo import AgentRunRepo
from app.models.entities import Resume, ResumeSection, User
from app.services.auth import create_session


def _seed_user(db_session, email: str, role: str = "student") -> tuple[User, str]:
    user = User(
        email=email,
        password_hash="test-hash",
        full_name=email.split("@")[0],
        role=role,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user, create_session(db_session, user)


def _seed_resume(db_session, user: User) -> int:
    resume = Resume(user_id=user.id, template_name="classic", content_text="Ada Lovelace", source_format="md")
    db_session.add(resume)
    db_session.commit()
    db_session.refresh(resume)
    db_session.add(
        ResumeSection(
            resume_id=resume.id,
            section_name="experience",
            content_json=json.dumps({"bullets": ["Built APIs"]}),
            confidence=0.9,
        )
    )
    db_session.commit()
    return resume.id


def test_resume_idor_other_user_gets_404(client, db_session):
    owner, _owner_token = _seed_user(db_session, "owner@example.com")
    _, intruder_token = _seed_user(db_session, "intruder@example.com")
    resume_id = _seed_resume(db_session, owner)

    resp = client.get(
        f"/resumes/{resume_id}",
        headers={"Authorization": f"Bearer {intruder_token}"},
    )
    assert resp.status_code == 404


def test_agent_run_idor_other_user_gets_404(client, db_session):
    owner, _owner_token = _seed_user(db_session, "agent-owner@example.com")
    _, intruder_token = _seed_user(db_session, "agent-intruder@example.com")
    resume_id = _seed_resume(db_session, owner)

    run = AgentRunRepo(db_session).create(
        student_id=owner.id,
        resume_id=resume_id,
        summary_json="{}",
        status="completed",
    )

    peek = client.get(
        f"/agent/runs/{run.id}",
        headers={"Authorization": f"Bearer {intruder_token}"},
    )
    assert peek.status_code == 404


def test_logout_revokes_token(client, db_session):
    _, token = _seed_user(db_session, "logout@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    ok = client.post("/auth/logout", headers=headers)
    assert ok.status_code == 200
    assert ok.json()["revoked"] is True

    profile = client.get("/profile", headers=headers)
    assert profile.status_code == 401


def test_officer_cohort_requires_officer_role(client, db_session):
    _, student_token = _seed_user(db_session, "student-cohort@example.com", role="student")
    _, officer_token = _seed_user(db_session, "officer-cohort@example.com", role="officer")

    denied = client.get("/officer/cohort", headers={"Authorization": f"Bearer {student_token}"})
    assert denied.status_code == 403

    allowed = client.get("/officer/cohort", headers={"Authorization": f"Bearer {officer_token}"})
    assert allowed.status_code == 200
    assert "kpis" in allowed.json()


def test_security_headers_present(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.headers.get("X-Content-Type-Options") == "nosniff"
    assert resp.headers.get("X-Frame-Options") == "DENY"
