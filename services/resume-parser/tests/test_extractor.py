"""Extractor hardening tests (Phase 1 data-pipeline fix).

Guards the three regressions that previously collapsed scores toward constants:
  1. Alias headings that are neither ALL-CAPS nor strict Title-Case are detected.
  2. The ``header`` bucket (contact line + pre-heading text) is preserved, not
     silently dropped — so no resume text is lost before scoring.
  3. Section confidence varies with match quality + richness instead of being a
     hardcoded 0.9 / 0.6.
"""

from __future__ import annotations

from app.extractor import (
    _is_heading_candidate,
    build_section_payload,
    split_into_sections,
)

STRONG = """RAHUL SHARMA
rahul@gmail.com | +91 9876543210 | linkedin.com/in/rahul
Education:
B.Tech CS, NIT Trichy, 2025, CGPA 8.4
Work Experience
- Built payment service in Python, cut latency 40%
- Deployed on Docker and Kubernetes
Skills
Python, SQL, Docker, Kubernetes"""


def _payload(text: str):
    return build_section_payload(split_into_sections(text.split("\n")))


def test_alias_headings_detected_without_caps_or_titlecase():
    assert _is_heading_candidate("Education:") is True
    assert _is_heading_candidate("Work Experience") is True


def test_body_line_is_not_a_heading():
    assert _is_heading_candidate("Built a payment service in Python reducing effort") is False


def test_header_bucket_preserved_with_contact():
    payload = _payload(STRONG)
    names = {s["section_name"] for s in payload}
    assert "header" in names
    header = next(s for s in payload if s["section_name"] == "header")
    assert "rahul@gmail.com" in header["content_json"]["raw"]


def test_standard_sections_extracted():
    names = {s["section_name"] for s in _payload(STRONG)}
    assert {"education", "experience", "skills"} <= names


def test_confidence_varies_and_is_bounded():
    payload = _payload(STRONG)
    confidences = [s["confidence"] for s in payload]
    assert len(set(confidences)) > 1, "confidence is a hardcoded constant"
    assert all(0.2 <= c <= 0.99 for c in confidences)
    # A populated canonical section should out-confidence the catch-all header.
    by_name = {s["section_name"]: s["confidence"] for s in payload}
    assert by_name["experience"] > by_name["header"]
