"""Content-aware sub-scorers from structured resume sections.

Every scorer in this module:
  - Returns a continuous float in [0, 100].
  - Reads actual text content (not just word counts or presence flags).
  - Produces differentiated scores across the quality spectrum — verified by the
    discrimination gate in tests/golden/.

The reference implementation is ``analyze_ats`` in ``parse_safety.py``:
multi-signal, continuous, per-issue actionable. All scorers here follow the
same pattern.
"""

from __future__ import annotations

import json
import re
from typing import Any

# ── Shared helpers ─────────────────────────────────────────────────────────────

_ACTION_VERBS: frozenset[str] = frozenset([
    "built", "developed", "designed", "implemented", "led", "optimized",
    "deployed", "created", "engineered", "automated", "launched", "improved",
    "reduced", "increased", "managed", "architected", "delivered", "integrated",
    "analyzed", "researched", "collaborated", "spearheaded", "migrated",
    "established", "streamlined", "refactored", "scaled", "maintained",
    "contributed", "trained", "mentored", "published", "authored",
])

_METRIC_RE = re.compile(
    r"\b\d+(?:\.\d+)?\s?"
    r"(?:%|percent|x\b|times|k\b|m\b|l\b|cr\b|lpa|ms\b|sec|hrs|days|users|requests|"
    r"req\b|rps|rpm|tps|gb|mb|kb|lines|loc\b|repos|teams?|members?|points?)"
    r"(?!\w)",  # no trailing word-char — handles "40%." and "40% " both
    re.IGNORECASE,
)

_BULLET_CHARS = frozenset("•◦▪‣·-*–→»")

_TECH_TERMS = re.compile(
    r"\b(?:api|sdk|rest|graphql|sql|nosql|docker|kubernetes|aws|gcp|azure|"
    r"python|java|javascript|typescript|golang|rust|react|angular|vue|"
    r"fastapi|django|flask|spring|node|postgresql|mysql|mongodb|redis|"
    r"tensorflow|pytorch|scikit|pandas|numpy|kafka|celery|redis|ci/?cd|"
    r"git|github|gitlab|linux|bash|microservices?|serverless|oauth|jwt)\b",
    re.IGNORECASE,
)


def resume_text_from_sections(sections: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for sec in sections:
        name = sec.get("section_name", "")
        content = sec.get("content_json", {})
        if isinstance(content, str):
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                content = {"raw": content}
        raw = ""
        if isinstance(content, dict):
            raw = str(content.get("raw", ""))
        parts.append(f"{name}\n{raw}")
    return "\n".join(parts)


def _section_text(sections: list[dict[str, Any]], name: str) -> str:
    for sec in sections:
        if sec.get("section_name") == name:
            content = sec.get("content_json", {})
            if isinstance(content, str):
                try:
                    content = json.loads(content)
                except json.JSONDecodeError:
                    return content
            if isinstance(content, dict):
                return str(content.get("raw", ""))
    return ""


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, round(v, 1)))


# ── Evidence quality ───────────────────────────────────────────────────────────

def evidence_quality_score(sections: list[dict[str, Any]]) -> float:
    """Content-aware evidence quality: STAR signals, metric density, verb variety.

    Signals (all continuous, not binary):
      - Verb variety: counts distinct action verbs (not repeated occurrences).
        A resume stuffed with "built built built" gets the same as one "built".
      - Metric density: ratio of quantified statements to total bullets/sentences.
      - Impact specificity: tech terms anchoring the impact statement.
      - Depth per bullet: median length of result-bearing bullets.

    Range: 0 (no content) → 100 (strong STAR structure throughout).
    """
    exp = _section_text(sections, "experience")
    proj = _section_text(sections, "projects")
    text = f"{exp} {proj}".strip()

    if not text:
        return 0.0

    low = text.lower()
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    bullets = [ln for ln in lines if ln[:1] in _BULLET_CHARS or
               re.match(r"^[-–•]\s", ln)]

    # Signal 1: distinct action verb count (variety, not repetition).
    # Calibration: 5 distinct verbs → 50pts; 10 → 100pts.
    distinct_verbs = sum(1 for v in _ACTION_VERBS if re.search(rf"\b{v}\b", low))
    verb_score = _clamp(distinct_verbs * 10)

    # Signal 2: metric count — each quantified outcome adds weight.
    # Calibration: 5 metrics → 70pts; 8+ → 100pts.
    metrics = _METRIC_RE.findall(low)
    metric_count = len(metrics)
    metric_score = _clamp(metric_count * 14)

    # Signal 3: tech-term specificity — grounds outcomes in real technology.
    # Calibration: 5 tech terms → 70pts; 10+ → 100pts.
    tech_hits = len(_TECH_TERMS.findall(text))
    tech_score = _clamp(tech_hits * 10)

    # Signal 4: bullet depth — longer bullets carry more context.
    # Calibration: 10-word median → 100pts.
    if bullets:
        median_len = sorted(len(b.split()) for b in bullets)[len(bullets) // 2]
        depth_score = _clamp(median_len * 10)
    else:
        depth_score = max(0.0, _clamp(len(text.split()) * 0.4))  # prose fallback

    # Weighted composite — verb variety and metrics are the strongest signals.
    composite = (
        0.30 * verb_score +
        0.30 * metric_score +
        0.25 * tech_score +
        0.15 * depth_score
    )

    # Floor: if there's experience/project text at all, score at least 20.
    return _clamp(max(20.0, composite) if text else 0.0)


# ── Profile completeness ───────────────────────────────────────────────────────

_MIN_WORD_COUNTS: dict[str, int] = {
    "summary": 10,
    "education": 5,
    "experience": 12,
    "projects": 10,
    "skills": 4,
    "certifications": 3,
    "achievements": 5,
}

_SECTION_WEIGHTS: dict[str, float] = {
    "summary": 0.10,
    "education": 0.20,
    "experience": 0.30,
    "projects": 0.25,
    "skills": 0.15,
}


def profile_completeness_score(sections: list[dict[str, Any]]) -> float:
    """Quality-aware completeness: presence AND richness, not just existence.

    Each expected section contributes its weight only when its content is
    substantive (meets a minimum word count). Empty or near-empty sections
    contribute 0 — a profile with "skills: " (blank) is not 20% complete.

    Range: 0 (nothing) → 100 (all five core sections richly populated).
    """
    total = 0.0
    for section, weight in _SECTION_WEIGHTS.items():
        text = _section_text(sections, section).strip()
        wc = len(text.split()) if text else 0
        min_wc = _MIN_WORD_COUNTS.get(section, 5)
        if wc == 0:
            contribution = 0.0
        elif wc < 3:
            contribution = 0.20  # almost nothing — e.g. a section name with one word
        elif wc < min_wc:
            contribution = 0.65  # has content but below the richness threshold
        else:
            contribution = 1.0   # meets threshold

        total += weight * contribution * 100

    return _clamp(total)


# ── Interview readiness ────────────────────────────────────────────────────────

def interview_readiness_score(sections: list[dict[str, Any]]) -> float:
    """Content-aware interview readiness: depth, complexity, leadership, breadth.

    Signals:
      - Experience depth: number of distinct roles/employers implied by date
        patterns and org structure.
      - Technical complexity: tech-term density in experience + projects.
      - Quantified impact: metric count (mirrors evidence but weighted differently).
      - Leadership/POR signals: leadership keywords beyond just "led".
      - Breadth: does the candidate have both experience AND projects?

    Range: 0 (nothing to talk about in an interview) → 100 (rich, multidimensional).
    """
    exp = _section_text(sections, "experience")
    proj = _section_text(sections, "projects")
    por = _section_text(sections, "positions_of_responsibility")
    text_all = f"{exp} {proj} {por}".strip()

    if not text_all:
        return 0.0

    low_all = text_all.lower()

    # Signal 1: technical complexity — tech terms per 100 words
    word_count = max(1, len(text_all.split()))
    tech_hits = len(_TECH_TERMS.findall(text_all))
    tech_density = tech_hits / word_count * 100
    tech_score = _clamp(tech_density * 15)  # 7 tech terms per 100 words → 100

    # Signal 2: quantified impact
    metrics = len(_METRIC_RE.findall(low_all))
    metric_score = _clamp(metrics * 12)  # 8 metrics → 96

    # Signal 3: leadership signals
    leadership_re = re.compile(
        r"\b(?:led|managed|mentored|headed|supervised|coordinated|facilitated|"
        r"directed|guided|founded|president|secretary|captain|chair)\b",
        re.IGNORECASE,
    )
    leadership_hits = len(leadership_re.findall(text_all))
    leadership_score = _clamp(leadership_hits * 25)  # 4 mentions → 100

    # Signal 4: breadth — has both experience/internship content AND project content
    has_exp = len(exp.split()) >= 15
    has_proj = len(proj.split()) >= 15
    breadth_score = 100.0 if (has_exp and has_proj) else (60.0 if (has_exp or has_proj) else 10.0)

    # Signal 5: role variety (date patterns suggest multiple stints)
    date_re = re.compile(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*'?\d{2,4}", re.IGNORECASE)
    date_count = len(date_re.findall(exp))
    variety_score = _clamp(date_count * 20)  # 5 date entries → 100

    composite = (
        0.25 * tech_score +
        0.25 * metric_score +
        0.20 * breadth_score +
        0.15 * leadership_score +
        0.15 * variety_score
    )

    return _clamp(max(15.0, composite) if text_all else 0.0)


# ── Placement hygiene ──────────────────────────────────────────────────────────

_CONTACT_RE = re.compile(r"[\w.+%-]+@[\w-]+\.[\w.-]+")
_PHONE_RE = re.compile(r"(?:\+?91[\s-]?)?(?<!\d)[6-9]\d{9}(?!\d)")
_LINK_RE = re.compile(r"(?:github\.com|linkedin\.com|gitlab\.com|portfolio|leetcode\.com)/\S+", re.IGNORECASE)

_FILLER_PHRASES = re.compile(
    r"\b(?:good communication skills?|team player|hard[- ]working|"
    r"quick learner|fast learner|self[- ]motivated|detail[- ]oriented|"
    r"passionate about|eager to learn|looking for opportunity|"
    r"seeking a challenging)\b",
    re.IGNORECASE,
)


def placement_hygiene_score(sections: list[dict[str, Any]], ats_flags: list[str]) -> float:
    """Placement hygiene: polish, completeness of contact, absence of filler phrases.

    Signals:
      - Contact reachability (email, phone, link).
      - Absence of generic filler phrases that dilute impact.
      - Consistent date formatting (via flag or text check).
      - Reasonable length (not too sparse, not bloated).
      - Skills section specificity (technology terms, not soft-skill keywords only).

    Range: 0 (no contact, all filler) → 100 (clean, complete, specific).
    """
    text = resume_text_from_sections(sections)
    low = text.lower()
    score = 100.0

    # Contact penalties
    if not _CONTACT_RE.search(text) or "no_email_found" in ats_flags:
        score -= 20
    if not _PHONE_RE.search(text) or "no_phone_found" in ats_flags:
        score -= 10
    if not _LINK_RE.search(text):
        score -= 8

    # Filler phrase penalty — each phrase costs points, cap at -20
    filler_hits = len(_FILLER_PHRASES.findall(text))
    score -= min(20.0, filler_hits * 7)

    # Length sanity — penalise only genuinely sparse resumes.
    # A well-structured concise resume (1 page, ~300 words) must not be penalised.
    word_count = len(text.split())
    if word_count < 25:
        score -= 18   # almost nothing written
    elif word_count < 50:
        score -= 8    # very thin
    elif word_count > 1500:
        score -= 10   # bloated wall-of-text

    # Skills section specificity: graded by how many distinct tech terms listed.
    # 0 terms = -10; 1 term = -5 (almost none); 2-5 = neutral; 6+ = +5 bonus.
    skills_text = _section_text(sections, "skills")
    if skills_text:
        tech_in_skills = len(_TECH_TERMS.findall(skills_text))
        if tech_in_skills == 0:
            score -= 10
        elif tech_in_skills == 1:
            score -= 5
        elif tech_in_skills >= 6:
            score += 5

    # ATS structural flags that affect hygiene
    if "missing_standard_headings" in ats_flags:
        score -= 10
    if "no_linkedin_link" in ats_flags and not _LINK_RE.search(text):
        score -= 5  # already penalized above if no link at all, just reduce here

    # Structure quality: penalise wall-of-text (no bullets, all prose)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    bullet_lines = sum(1 for ln in lines if ln[:1] in _BULLET_CHARS)
    if len(lines) > 6 and bullet_lines == 0:
        score -= 8  # has content but no structured bullets
    elif len(lines) > 10 and bullet_lines / len(lines) < 0.15:
        score -= 4  # very few bullets relative to content

    # Repetition signal: generic adjectives and vague filler in prose
    generic_re = re.compile(
        r"\b(?:many things|hard work|good marks?|dedicated|motivated|"
        r"passion(?:ate)?|eager|various|several|some|basic|etc\.?)\b",
        re.IGNORECASE,
    )
    generic_hits = len(generic_re.findall(text))
    score -= min(15.0, generic_hits * 5)

    return _clamp(score)
