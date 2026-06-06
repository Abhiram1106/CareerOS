"""Golden-path API test: register → seed resume → score → assert shape.

This test deliberately avoids the resume-parser/match-engine HTTP services by
seeding a Resume + ResumeSection directly and monkey-patching the two cross-
service clients used by the scoring handler. It exercises the full FastAPI
stack including auth, RBAC (``require_student``), DTO validation, the scoring
formula, scorecard persistence, and the response contract that the web app
depends on.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from app.models.entities import Resume, ResumeSection, User
from app.services.auth import create_session


JD_TEXT = (
    "We are hiring a Software Engineer with strong Python, FastAPI, and SQL skills. "
    "Required: Python, FastAPI, SQL. Bonus: Docker, Kubernetes. CGPA above 7."
)

RESUME_TEXT = (
    "Ada Lovelace — Software Engineer\n\n"
    "Skills: Python, FastAPI, SQL, Docker, Git\n\n"
    "Experience: Built REST APIs in Python and FastAPI, designed Postgres schemas, "
    "shipped to Docker on Kubernetes."
)


def _fake_parse_jd(_jd_text: str) -> dict[str, Any]:
    return {
        "company": "Acme Corp",
        "role": "Software Engineer",
        "required_skills": ["python", "fastapi", "sql"],
        "optional_skills": ["docker", "kubernetes"],
        "all_skills": ["python", "fastapi", "sql", "docker", "kubernetes"],
        "eligibility": {"min_cgpa": 7.0},
    }


def _fake_match(_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "tfidf_cosine": 72.0,
        "embedding_cosine": 68.0,
        "required_skill_recall": 100.0,
        "eligibility_rule_score": 100.0,
        "jd_match": 78.0,
        "missing_required_skills": [],
        "matched_skills": ["python", "fastapi", "sql"],
        "match_method": "lexical_dual_tfidf",
        "semantic_method": "char_ngram_proxy",
    }


@pytest.fixture()
def patch_clients(monkeypatch):
    """Stub external HTTP clients so the test stays in-process."""
    monkeypatch.setattr(
        "app.modules.scorecard.mutation.score_resume_handler.parse_jd_text",
        lambda jd: _async(_fake_parse_jd(jd)),
    )
    monkeypatch.setattr(
        "app.modules.scorecard.mutation.score_resume_handler.match_resume_to_jd",
        lambda payload: _async(_fake_match(payload)),
    )
    monkeypatch.setattr(
        "app.modules.jd.mutation.parse_jd_handler.parse_jd_text",
        lambda jd: _async(_fake_parse_jd(jd)),
    )


async def _async(value):
    return value


def _seed_user_token(db_session, role: str = "student") -> str:
    user = User(
        email=f"{role}@example.com",
        password_hash="test-hash",
        full_name=f"{role.title()} User",
        role=role,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return create_session(db_session, user)


def _seed_resume(db_session, email: str) -> int:
    user = db_session.query(User).filter(User.email == email).one()
    resume = Resume(
        user_id=user.id,
        template_name="classic",
        content_text=RESUME_TEXT,
        source_format="md",
    )
    db_session.add(resume)
    db_session.flush()
    sections = [
        ResumeSection(
            resume_id=resume.id,
            section_name="summary",
            content_json=json.dumps({"text": "Software engineer with Python and FastAPI experience."}),
        ),
        ResumeSection(
            resume_id=resume.id,
            section_name="skills",
            content_json=json.dumps({"items": ["Python", "FastAPI", "SQL", "Docker"]}),
        ),
        ResumeSection(
            resume_id=resume.id,
            section_name="experience",
            content_json=json.dumps(
                {
                    "items": [
                        {
                            "title": "Backend Engineer",
                            "company": "ABC",
                            "bullets": ["Shipped REST APIs in FastAPI", "Optimized Postgres queries"],
                        }
                    ]
                }
            ),
        ),
    ]
    db_session.add_all(sections)
    db_session.commit()
    return resume.id


def test_golden_path_register_seed_score(client, db_session, patch_clients):
    """Full flow: register student → seed resume → score → assert response contract."""
    token = _seed_user_token(db_session, role="student")
    resume_id = _seed_resume(db_session, "student@example.com")

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "resume_id": resume_id,
        "jd_text": JD_TEXT,
        "company": "Acme Corp",
        "role": "Software Engineer",
        "ats_flags": ["two_column_layout_detected"],
    }
    res = client.post("/scorecards/score", json=payload, headers=headers)
    assert res.status_code == 200, res.text
    body = res.json()

    # Contract surface the web app reads.
    assert body["scorecard_id"] > 0
    assert body["jd_id"] > 0
    assert 0 <= body["overall_score"] <= 100
    assert body["bucket"] in {"strong", "ready", "borderline", "high-risk"}
    assert body["semantic_method"] == "char_ngram_proxy"
    assert set(body["components"]) == {
        "jd_match",
        "ats_safety",
        "evidence",
        "completeness",
        "interview",
        "hygiene",
    }
    for key in ("jd_match", "ats_parse_safety", "evidence_quality"):
        assert 0 <= body["raw"][key] <= 100
    assert "python" in body["matched_skills"]
    assert isinstance(body["missing_required_skills"], list)


def test_scorecards_rejects_non_student_role(client, db_session, patch_clients):
    """RBAC: any non-student role must NOT call the student scoring route."""
    non_student_token = _seed_user_token(db_session, role="admin")
    student_token = _seed_user_token(db_session, role="student")
    resume_id = _seed_resume(db_session, "student@example.com")

    res = client.post(
        "/scorecards/score",
        json={"resume_id": resume_id, "jd_text": JD_TEXT},
        headers={"Authorization": f"Bearer {non_student_token}"},
    )
    assert res.status_code == 403, res.text

    res_ok = client.post(
        "/scorecards/score",
        json={"resume_id": resume_id, "jd_text": JD_TEXT},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res_ok.status_code == 200, res_ok.text


def test_scorecards_rejects_unauthenticated(client):
    res = client.post("/scorecards/score", json={"resume_id": 1, "jd_text": JD_TEXT})
    assert res.status_code == 401
