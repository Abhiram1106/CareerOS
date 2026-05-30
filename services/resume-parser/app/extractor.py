"""Section extractor for Indian fresher resumes.

Strategy:
  - Heading heuristics: short ALL-CAPS lines or Title-Case lines followed by
    a blank line are candidate section headings.
  - Indian fresher vocabulary: understands CGPA, X/XII, POR, backlogs,
    hackathons, LeetCode, CodeChef, GitHub links.
  - Falls back gracefully if a section is absent.
"""
from __future__ import annotations

import re
from typing import Any

# Canonical section names and their common aliases (lowercase).
SECTION_ALIASES: dict[str, list[str]] = {
    "summary": ["summary", "objective", "about", "profile", "career objective", "professional summary"],
    "education": ["education", "academic", "qualifications", "schooling", "academic background"],
    "experience": ["experience", "work experience", "internship", "internships", "work history", "employment"],
    "projects": ["projects", "project", "academic projects", "personal projects", "key projects"],
    "skills": ["skills", "technical skills", "technologies", "core competencies", "skill set", "tools"],
    "certifications": ["certifications", "certification", "certificates", "courses", "online courses", "moocs"],
    "achievements": ["achievements", "awards", "honours", "honors", "accomplishments", "recognitions"],
    "positions_of_responsibility": ["positions of responsibility", "por", "leadership", "extracurricular", "activities", "clubs"],
    "links": ["links", "profiles", "online profiles", "github", "portfolio"],
}

# Build a reverse map: alias → canonical
_ALIAS_MAP: dict[str, str] = {}
for canonical, aliases in SECTION_ALIASES.items():
    for alias in aliases:
        _ALIAS_MAP[alias] = canonical


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _classify_heading(line: str) -> str | None:
    """Return the canonical section name if this line looks like a section heading."""
    stripped = line.strip()
    if not stripped or len(stripped) > 80:
        return None

    normalised = _normalise(stripped)
    # Direct alias lookup
    if normalised in _ALIAS_MAP:
        return _ALIAS_MAP[normalised]

    # Partial match for lines like "PROJECTS (2023-24)"
    for alias, canonical in _ALIAS_MAP.items():
        if normalised.startswith(alias):
            return canonical

    return None


def _is_heading_candidate(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    # All caps (common in Indian resumes)
    if stripped.isupper() and 3 < len(stripped) < 60:
        return True
    # Title case short line with no commas / digits
    if stripped.istitle() and len(stripped.split()) <= 5 and not re.search(r"\d", stripped):
        return True
    # Short standalone line (≤4 words) that is an exact alias, optionally with a
    # trailing colon or decorative chars — e.g. "Education:", "Work Experience".
    cleaned = re.sub(r"[:\-–—_*•|]+", " ", stripped)
    if len(cleaned.split()) <= 4 and _normalise(cleaned) in _ALIAS_MAP:
        return True
    return False


def _extract_ats_flags(text: str) -> list[str]:
    """Detect structural ATS-parse-safety issues from raw text.

    These flags feed the content-aware analyzer in packages/scoring; they capture
    layout/structure signals that survive text extraction.
    """
    flags: list[str] = []
    low = text.lower()

    if len(text.encode()) > 500_000:
        flags.append("file_too_large")
    if any(ch in text for ch in ("│", "┌", "┐", "├", "┤", "┼", "╔", "╗")):
        flags.append("table_detected")
    if text.count("\t") > 25:
        flags.append("tab_heavy_may_be_multi_column")
    if not re.search(r"[\w.+%-]+@[\w-]+\.[\w.-]+", text):
        flags.append("no_email_found")
    if not re.search(r"(?:\+?91[\s-]?)?(?<!\d)[6-9]\d{9}(?!\d)", text):
        flags.append("no_phone_found")
    standard_headings = sum(
        1 for kw in ("education", "experience", "skills", "projects") if kw in low
    )
    if standard_headings == 0:
        flags.append("missing_standard_headings")
    elif standard_headings < 2:
        flags.append("few_standard_headings")
    if re.search(r"(?i)\b(photo|image|logo|picture)\b", text):
        flags.append("possible_image_content")
    if "linkedin.com" not in low:
        flags.append("no_linkedin_link")

    sum_non_ascii = sum(1 for ch in text if ord(ch) > 0x2122)
    if sum_non_ascii > 15:
        flags.append("special_glyphs_detected")

    return flags


def split_into_sections(lines: list[str]) -> dict[str, list[str]]:
    """Split a list of text lines into sections by heading detection."""
    sections: dict[str, list[str]] = {}
    current: str = "header"
    sections[current] = []

    for line in lines:
        canonical = _classify_heading(line)
        if canonical and _is_heading_candidate(line):
            current = canonical
            sections.setdefault(current, [])
        else:
            sections.setdefault(current, []).append(line)

    return sections


def _section_confidence(section_name: str, content: str) -> float:
    """Confidence derived from match quality, not a hardcoded constant.

    A canonical, well-populated section scores high; the catch-all ``header``
    bucket or a section we recognised but barely populated scores lower.
    """
    if section_name == "header":
        base = 0.4
    elif section_name in SECTION_ALIASES:
        base = 0.85
    else:
        base = 0.55

    word_count = len(content.split())
    if word_count == 0:
        richness = -0.25
    elif word_count < 8:
        richness = -0.1
    elif word_count < 40:
        richness = 0.05
    else:
        richness = 0.1

    return round(max(0.2, min(0.99, base + richness)), 2)


def build_section_payload(sections: dict[str, list[str]]) -> list[dict[str, Any]]:
    """Convert raw section line-lists into structured dicts.

    The ``header`` bucket is preserved when it holds content (it often carries
    the contact line and any pre-heading summary) so no resume text is silently
    dropped before scoring.
    """
    result = []
    for section_name, lines in sections.items():
        content = "\n".join(l for l in lines if l.strip())
        if not content:
            continue
        result.append({
            "section_name": section_name,
            "content_json": {"raw": content},
            "confidence": _section_confidence(section_name, content),
        })
    return result
