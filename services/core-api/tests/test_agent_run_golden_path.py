from __future__ import annotations

import json
from typing import Any

import pytest

from app.models.entities import Resume, ResumeSection, User
from app.services.auth import create_session


JD_TEXT = (
    "We are hiring a backend engineer with Python, FastAPI, and SQL skills. "
    "Experience building REST APIs and basic cloud deployment is preferred."
)


async def _async(value: Any) -> Any:
    return value


def _fake_parse_jd(_jd_text: str) -> dict[str, Any]:
    return {
        "company": "Acme Corp",
        "role": "Backend Engineer",
        "required_skills": ["python", "fastapi", "sql"],
        "optional_skills": ["docker", "aws"],
        "all_skills": ["python", "fastapi", "sql", "docker", "aws"],
        "eligibility": {"min_cgpa": 7.0},
    }


def _fake_match(_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "tfidf_cosine": 72.0,
        "embedding_cosine": 70.0,
        "required_skill_recall": 100.0,
        "eligibility_rule_score": 100.0,
        "jd_match": 79.0,
        "missing_required_skills": [],
        "matched_skills": ["python", "fastapi", "sql"],
        "match_method": "lexical_dual_tfidf",
        "semantic_method": "char_ngram_proxy",
    }


def _fake_rewrite(_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "top_issues": [{"type": "ATS_FORMAT", "severity": "medium", "message": "Keep bullets concise"}],
        "section_rewrites": [
            {
                "section": "experience",
                "original": "Built APIs",
                "rewrite": "Built REST APIs in FastAPI and improved endpoint reliability.",
                "evidence_ids": ["exp_1"],
                "confidence": 0.86,
            }
        ],
        "unsupported_claims": [],
        "requires_confirmation": [],
    }


class _FakeTask:
    @staticmethod
    def delay(*_args, **_kwargs):
        return None

    @staticmethod
    def apply(*_args, **_kwargs):
        return None


@pytest.fixture()
def patch_agent_clients(monkeypatch):
    monkeypatch.setattr(
        "app.modules.agent.state_machine.run_ats_parse_safety",
        lambda _flags: _async({"parse_safety_score": 82.0, "penalty_weight": 0.18}),
    )
    monkeypatch.setattr(
        "app.modules.scorecard.mutation.score_resume_handler.parse_jd_text",
        lambda jd: _async(_fake_parse_jd(jd)),
    )
    monkeypatch.setattr(
        "app.modules.scorecard.mutation.score_resume_handler.match_resume_to_jd",
        lambda payload: _async(_fake_match(payload)),
    )
    monkeypatch.setattr(
        "app.modules.recommendation.mutation.run_rewrite_handler.proof_linked_rewrite",
        lambda payload: _async(_fake_rewrite(payload)),
    )
    monkeypatch.setattr(
        "app.modules.export.mutation.queue_export_handler.generate_resume_export",
        _FakeTask(),
    )


def _seed_student_token(db_session) -> str:
    user = User(
        email="agent-student@example.com",
        password_hash="test-hash",
        full_name="Agent Student",
        role="student",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return create_session(db_session, user)


def _seed_resume(db_session) -> int:
    user = db_session.query(User).filter(User.email == "agent-student@example.com").one()
    resume = Resume(
        user_id=user.id,
        template_name="uploaded",
        content_text="Python backend engineer profile",
        source_format="pdf",
    )
    db_session.add(resume)
    db_session.flush()
    db_session.add(
        ResumeSection(
            resume_id=resume.id,
            section_name="experience",
            content_json=json.dumps(
                {
                    "items": [
                        {"title": "Backend Intern", "bullets": ["Built APIs", "Wrote SQL queries"]},
                    ]
                }
            ),
        )
    )
    db_session.commit()
    return resume.id


def test_agent_run_golden_path(client, db_session, patch_agent_clients):
    token = _seed_student_token(db_session)
    resume_id = _seed_resume(db_session)
    headers = {"Authorization": f"Bearer {token}"}

    run_resp = client.post(
        "/agent/run",
        json={"resume_id": resume_id, "jd_text": JD_TEXT, "ats_flags": ["two_column_layout_detected"]},
        headers=headers,
    )
    assert run_resp.status_code == 200, run_resp.text
    body = run_resp.json()
    assert body["status"] == "completed"
    assert body["current_step"] == "DONE"
    assert body["scorecard_id"] > 0
    assert body["run_id"] > 0
    assert body["export_job_id"] > 0

    get_resp = client.get(f"/agent/runs/{body['run_id']}", headers=headers)
    assert get_resp.status_code == 200, get_resp.text
    readback = get_resp.json()
    assert readback["current_step"] == "DONE"
    assert readback["status"] == "completed"
