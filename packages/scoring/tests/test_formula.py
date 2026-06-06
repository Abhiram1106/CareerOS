"""Hardened tests for PlacementReadinessScore formula and helpers.

Covers:
* JD match weighted average (0.35/0.35/0.20/0.10)
* PlacementReadiness weighted average (0.35/0.20/0.20/0.10/0.10/0.05)
* Bucket boundaries: 85=strong, 70=ready, 50=borderline, <50=high-risk
* Clamping behaviour at extremes
* ATS parse-safety penalty composition and unknown-flag handling
* Resume component heuristics (evidence, completeness, interview, hygiene)
"""

from __future__ import annotations

import json

import pytest

from careeros_scoring import (
    ats_parse_safety_from_flags,
    bucket_label,
    compute_jd_match,
    compute_placement_readiness,
    evidence_quality_score,
    interview_readiness_score,
    placement_hygiene_score,
    profile_completeness_score,
    resume_text_from_sections,
)
from careeros_scoring.formula import JdMatchBreakdown


# ── compute_jd_match ──────────────────────────────────────────────────────────


def test_jd_match_perfect_inputs_returns_100():
    assert compute_jd_match(100, 100, 100, 100) == 100.0


def test_jd_match_zero_inputs_returns_0():
    assert compute_jd_match(0, 0, 0, 0) == 0.0


def test_jd_match_weighted_average_formula():
    # 0.35*80 + 0.35*70 + 0.20*60 + 0.10*100 = 28 + 24.5 + 12 + 10 = 74.5
    assert compute_jd_match(80, 70, 60, 100) == 74.5


def test_jd_match_clamps_above_100():
    # Defensive: even if inputs overshoot, output stays bounded.
    assert compute_jd_match(150, 150, 150, 150) == 100.0


def test_jd_match_clamps_below_0():
    assert compute_jd_match(-50, -50, -50, -50) == 0.0


# ── JdMatchBreakdown ──────────────────────────────────────────────────────────


def test_breakdown_jd_match_property_matches_formula():
    b = JdMatchBreakdown(80, 70, 50, 100)
    # 0.35*80 + 0.35*70 + 0.20*50 + 0.10*100 = 28 + 24.5 + 10 + 10 = 72.5
    assert b.jd_match == 72.5


# ── compute_placement_readiness ───────────────────────────────────────────────


def test_placement_readiness_strong_bucket():
    r = compute_placement_readiness(
        jd_match=90,
        ats_parse_safety=90,
        evidence_quality=90,
        profile_completeness=90,
        interview_readiness=90,
        placement_hygiene=90,
    )
    assert r.bucket == "strong"
    assert r.overall_score >= 85


def test_placement_readiness_weighted_formula():
    r = compute_placement_readiness(
        jd_match=80,
        ats_parse_safety=70,
        evidence_quality=60,
        profile_completeness=50,
        interview_readiness=40,
        placement_hygiene=30,
    )
    # 0.35*80 + 0.20*70 + 0.20*60 + 0.10*50 + 0.10*40 + 0.05*30 = 28 + 14 + 12 + 5 + 4 + 1.5 = 64.5
    assert r.overall_score == 64.5
    assert r.bucket == "borderline"


def test_placement_readiness_high_risk_bucket():
    r = compute_placement_readiness(
        jd_match=20,
        ats_parse_safety=20,
        evidence_quality=20,
        profile_completeness=20,
        interview_readiness=20,
        placement_hygiene=20,
    )
    assert r.bucket == "high-risk"
    assert r.overall_score < 50


# ── bucket_label boundaries ───────────────────────────────────────────────────


@pytest.mark.parametrize(
    "score,expected",
    [
        (100.0, "strong"),
        (85.0, "strong"),
        (84.9, "ready"),
        (70.0, "ready"),
        (69.9, "borderline"),
        (50.0, "borderline"),
        (49.9, "high-risk"),
        (0.0, "high-risk"),
    ],
)
def test_bucket_label_at_boundaries(score, expected):
    assert bucket_label(score) == expected


# ── ATS parse-safety ──────────────────────────────────────────────────────────


def test_ats_parse_safety_no_flags_is_perfect():
    assert ats_parse_safety_from_flags([]) == 100.0


def test_ats_parse_safety_known_flags_compose():
    # table_detected (10) + two_column (12) = 22 → 78
    assert ats_parse_safety_from_flags(["table_detected", "two_column"]) == 78.0


def test_ats_parse_safety_unknown_flags_ignored():
    # Unknown flags must not reduce the score; this guards against silent typos.
    assert ats_parse_safety_from_flags(["wat_is_this", "nonsense_flag"]) == 100.0


def test_ats_parse_safety_normalizes_case_and_spaces():
    # "Two Column" should match "two_column".
    assert ats_parse_safety_from_flags(["Two Column"]) == 88.0


def test_ats_parse_safety_floor_at_zero():
    massive = ["two_column", "table_detected", "contact_in_header"] * 20
    assert ats_parse_safety_from_flags(massive) == 0.0


# ── resume_text_from_sections ─────────────────────────────────────────────────


def test_resume_text_from_sections_handles_string_json():
    sections = [
        {"section_name": "summary", "content_json": json.dumps({"raw": "Engineer with FastAPI."})},
        {"section_name": "skills", "content_json": json.dumps({"raw": "Python, SQL"})},
    ]
    text = resume_text_from_sections(sections)
    assert "Engineer with FastAPI." in text
    assert "Python, SQL" in text


def test_resume_text_from_sections_handles_dict_json():
    sections = [{"section_name": "summary", "content_json": {"raw": "Hello world"}}]
    assert "Hello world" in resume_text_from_sections(sections)


# ── resume component sub-scores ───────────────────────────────────────────────


def test_evidence_quality_with_metrics_and_actions():
    sections = [
        {
            "section_name": "experience",
            "content_json": {
                "raw": "• Built high-performance REST API using Python and AWS. Optimized SQL queries by 40%.\n"
                       "• Led team of 5 members. Developed React frontend. Engineered reliable CI/CD pipeline.\n"
                       "• Spearheaded migration to microservices, improved system uptime by 99.9%."
            },
        }
    ]
    score = evidence_quality_score(sections)
    # Added more verbs and metrics to cross the 60.0 threshold comfortably.
    assert score > 60.0


def test_evidence_quality_empty_returns_baseline():
    # Implementation returns 0.0 for empty text.
    assert evidence_quality_score([]) == 0.0


def test_profile_completeness_full_profile():
    sections = [
        {"section_name": name, "content_json": {"raw": "This is a substantive piece of content for section " + name + " that easily meets the word count threshold requirements."}}
        for name in ("summary", "education", "experience", "projects", "skills")
    ]
    # Each basic string above is 18 words, which exceeds all thresholds (max is 12 for experience).
    assert profile_completeness_score(sections) == 100.0


def test_profile_completeness_missing_sections():
    sections = [{"section_name": "summary", "content_json": {"raw": "This is a substantive summary content piece that is definitely exceeding the ten word count threshold required."}}]
    # Summary weight is 0.10. 0.10 * 1.0 * 100 = 10.0
    assert profile_completeness_score(sections) == 10.0


def test_interview_readiness_thin_resume():
    assert interview_readiness_score([]) == 0.0


def test_interview_readiness_dense_resume():
    content = (
        "Built REST API using Python and AWS in Jan 2024. Optimized SQL queries by 40%.\n"
        "Led team of 5 members. Developed React frontend. Engineered CI/CD pipeline.\n"
    )
    long_text = " ".join([content] * 10)
    sections = [
        {"section_name": "experience", "content_json": {"raw": long_text}},
        {"section_name": "projects", "content_json": {"raw": "Built a Python SQL project with AWS and REST API in Feb 2023."}}
    ]
    score = interview_readiness_score(sections)
    assert score > 70.0
    assert score <= 100.0


def test_placement_hygiene_penalises_missing_email_flag():
    # Include an email in the text so the text-check passes, leaving only the flag penalty
    sections = [{"section_name": "summary", "content_json": {"raw": "Contact me at test@example.com. " + "X" * 300}}]
    with_flag = placement_hygiene_score(sections, ["no_email_found"])
    without_flag = placement_hygiene_score(sections, [])
    assert with_flag < without_flag
