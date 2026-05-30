"""ATS parse-safety scoring — single source of truth.

Two entry points:
  - ``analyze_ats(text, ats_flags)`` — the real, content-aware analyzer. Reads the
    actual resume text across seven weighted dimensions and returns a differentiated
    score plus per-dimension checks and actionable issues. This is what produces
    distinct scores for distinct resumes.
  - ``ats_parse_safety_from_flags(flags)`` — legacy flag-only penalty model, kept for
    callers that only have structural flags and no text.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

FLAG_PENALTIES: dict[str, int] = {
    "two_column": 12,
    "two_column_layout": 12,
    "tab_heavy_may_be_multi_column": 12,
    "contact_in_header": 10,
    "table_detected": 10,
    "table_based_layout": 10,
    "possible_image_content": 8,
    "image_detected": 8,
    "scanned_no_text": 8,
    "missing_standard_headings": 6,
    "no_standard_sections": 6,
    "non_standard_dates": 5,
    "file_too_large": 5,
    "partial_parse": 4,
    "incomplete_employer": 4,
    "no_email_found": 4,
}


def ats_parse_safety_from_flags(flags: list[str]) -> float:
    """100 minus sum of known penalties; unknown flags ignored."""
    penalty = 0
    for flag in flags:
        key = flag.strip().lower().replace(" ", "_")
        penalty += FLAG_PENALTIES.get(key, 0)
    return max(0.0, min(100.0, round(100 - penalty, 1)))


# --------------------------------------------------------------------------- #
# Content-aware analyzer
# --------------------------------------------------------------------------- #

_EMAIL_RE = re.compile(r"[\w.+%-]+@[\w-]+\.[\w.-]+")
_PHONE_RE = re.compile(r"(?:\+?91[\s-]?)?(?<!\d)[6-9]\d{9}(?!\d)")
_LINKEDIN_RE = re.compile(r"linkedin\.com/\S+", re.IGNORECASE)
_GITHUB_RE = re.compile(r"(?:github\.com|gitlab\.com)/\S+", re.IGNORECASE)
_PORTFOLIO_RE = re.compile(r"https?://\S+", re.IGNORECASE)
_URL_BARE_RE = re.compile(r"\b\w[\w-]*\.(?:dev|io|me|com|in|tech|app)\b", re.IGNORECASE)

_STANDARD_SECTIONS: dict[str, list[str]] = {
    "education": ["education", "academic", "qualification", "schooling"],
    "experience": ["experience", "work history", "employment", "internship"],
    "skills": ["skills", "technical skills", "technologies", "core competenc"],
    "projects": ["project"],
    "summary": ["summary", "objective", "profile", "about me"],
    "certifications": ["certification", "certificate", "courses"],
    "achievements": ["achievement", "award", "honor", "honour", "accomplishment"],
}

_ACTION_VERBS = [
    "built", "developed", "designed", "implemented", "led", "optimized", "optimised",
    "deployed", "created", "engineered", "automated", "launched", "improved",
    "reduced", "increased", "managed", "architected", "delivered", "integrated",
    "analyzed", "analysed", "researched", "collaborated", "spearheaded", "migrated",
]

_BULLET_CHARS = ("•", "◦", "▪", "‣", "·", "-", "*", "–", "→", "»")

_DATE_PATTERNS = {
    "month_year": re.compile(
        r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*'?\d{2,4}",
        re.IGNORECASE,
    ),
    "year_range": re.compile(r"\b(19|20)\d{2}\s*[-–—]\s*((19|20)\d{2}|present|current)", re.IGNORECASE),
    "numeric_slash": re.compile(r"\b\d{1,2}/\d{2,4}\b"),
    "iso": re.compile(r"\b(19|20)\d{2}-\d{1,2}(-\d{1,2})?\b"),
}


@dataclass
class _Dimension:
    key: str
    label: str
    weight: float
    score: float
    issues: list[dict] = field(default_factory=list)


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, round(value, 1)))


def _bucket(score: float) -> str:
    if score >= 85:
        return "excellent"
    if score >= 70:
        return "good"
    if score >= 55:
        return "fair"
    return "poor"


def _score_contact(text: str) -> _Dimension:
    issues: list[dict] = []
    score = 0.0
    if _EMAIL_RE.search(text):
        score += 40
    else:
        issues.append({
            "id": "no_email",
            "severity": "high",
            "message": "No email address detected. ATS systems index candidates by email.",
            "fix": "Add a professional email at the top of your resume (e.g. name@gmail.com).",
        })
    if _PHONE_RE.search(text):
        score += 25
    else:
        issues.append({
            "id": "no_phone",
            "severity": "high",
            "message": "No phone number detected.",
            "fix": "Add a 10-digit mobile number in the contact header.",
        })
    if _LINKEDIN_RE.search(text):
        score += 15
    else:
        issues.append({
            "id": "no_linkedin",
            "severity": "medium",
            "message": "No LinkedIn profile link found. Recruiters expect one for freshers.",
            "fix": "Add your linkedin.com/in/<handle> URL.",
        })
    if _GITHUB_RE.search(text) or _PORTFOLIO_RE.search(text) or _URL_BARE_RE.search(text):
        score += 12
    else:
        issues.append({
            "id": "no_portfolio",
            "severity": "low",
            "message": "No GitHub / portfolio link found.",
            "fix": "For technical roles, add your GitHub or portfolio URL.",
        })
    if re.search(r"\b(bangalore|bengaluru|hyderabad|chennai|mumbai|delhi|pune|kolkata|noida|gurgaon|gurugram)\b", text, re.IGNORECASE):
        score += 8
    return _Dimension("contact_reachability", "Contact reachability", 0.18, _clamp(score), issues)


def _score_sections(text: str) -> _Dimension:
    low = text.lower()
    present = [name for name, aliases in _STANDARD_SECTIONS.items() if any(a in low for a in aliases)]
    issues: list[dict] = []
    core = {"education", "experience", "skills", "projects"}
    missing_core = sorted(core - set(present))
    score = min(100.0, len(present) / 6 * 100 + (15 if "summary" in present else 0))
    if missing_core:
        score -= 10 * len(missing_core)
        issues.append({
            "id": "missing_sections",
            "severity": "high" if len(missing_core) >= 2 else "medium",
            "message": f"Missing standard section heading(s): {', '.join(missing_core)}.",
            "fix": "ATS parsers map content by standard headings. Add clear headings: "
                   "Education, Experience, Skills, Projects.",
        })
    return _Dimension("section_structure", "Section structure", 0.20, _clamp(score), issues)


def _score_formatting(text: str, ats_flags: list[str]) -> _Dimension:
    issues: list[dict] = []
    score = 100.0
    flag_set = {f.strip().lower().replace(" ", "_") for f in ats_flags}

    if "│" in text or "┌" in text or "┐" in text or "├" in text or "table_detected" in flag_set or "table_based_layout" in flag_set:
        score -= 18
        issues.append({
            "id": "tables",
            "severity": "high",
            "message": "Table-based layout detected. Many ATS parsers scramble table cells.",
            "fix": "Replace tables with simple single-column bullet lists.",
        })
    if text.count("\t") > 25 or "tab_heavy_may_be_multi_column" in flag_set or "two_column" in flag_set or "two_column_layout" in flag_set:
        score -= 18
        issues.append({
            "id": "multi_column",
            "severity": "high",
            "message": "Multi-column / tab-heavy layout detected. ATS reads left-to-right and mixes columns.",
            "fix": "Use a single-column layout. Avoid side-by-side text boxes.",
        })
    if re.search(r"(?i)\b(photo|image|logo|picture)\b", text) or "possible_image_content" in flag_set or "image_detected" in flag_set:
        score -= 12
        issues.append({
            "id": "images",
            "severity": "medium",
            "message": "Image / photo content referenced. Images are invisible to ATS and waste space.",
            "fix": "Remove photos, logos and graphics. Keep the resume text-only.",
        })
    non_ascii = sum(1 for ch in text if ord(ch) > 0x2122)
    if non_ascii > 15:
        score -= 8
        issues.append({
            "id": "special_glyphs",
            "severity": "low",
            "message": "Unusual symbols / decorative glyphs detected; some ATS drop them.",
            "fix": "Use plain bullet characters (•, -) and standard punctuation.",
        })
    if "contact_in_header" in flag_set:
        score -= 10
        issues.append({
            "id": "header_contact",
            "severity": "medium",
            "message": "Contact details appear inside a header/footer region — often skipped by ATS.",
            "fix": "Move email/phone into the main body, not the page header or footer.",
        })
    return _Dimension("formatting_safety", "Formatting safety", 0.22, _clamp(score), issues)


def _score_dates(text: str) -> _Dimension:
    formats_found = [name for name, rx in _DATE_PATTERNS.items() if rx.search(text)]
    total_dates = sum(len(rx.findall(text)) for rx in _DATE_PATTERNS.values())
    issues: list[dict] = []
    if total_dates == 0:
        return _Dimension(
            "date_consistency", "Date consistency", 0.10, 45.0,
            [{
                "id": "no_dates",
                "severity": "medium",
                "message": "No recognizable dates found in experience/education.",
                "fix": "Add date ranges like 'Jun 2023 – Aug 2023' to roles and education.",
            }],
        )
    score = 100.0
    if len(formats_found) >= 3:
        score -= 25
        issues.append({
            "id": "mixed_date_formats",
            "severity": "medium",
            "message": f"{len(formats_found)} different date formats detected; inconsistent dating confuses parsers.",
            "fix": "Pick one date format (e.g. 'Mon YYYY') and use it everywhere.",
        })
    elif len(formats_found) == 2:
        score -= 10
        issues.append({
            "id": "two_date_formats",
            "severity": "low",
            "message": "Two date formats detected; standardize for consistency.",
            "fix": "Use a single date style throughout.",
        })
    return _Dimension("date_consistency", "Date consistency", 0.10, _clamp(score), issues)


def _score_density(text: str) -> _Dimension:
    words = len(text.split())
    issues: list[dict] = []
    if words < 150:
        score = max(20.0, words / 150 * 60)
        issues.append({
            "id": "too_short",
            "severity": "high",
            "message": f"Resume has only ~{words} words. Too sparse for a meaningful ATS profile.",
            "fix": "Expand projects and experience with concrete, quantified bullet points.",
        })
    elif words > 1200:
        score = max(55.0, 100 - (words - 1200) / 40)
        issues.append({
            "id": "too_long",
            "severity": "medium",
            "message": f"Resume is very long (~{words} words). Freshers should target a single page.",
            "fix": "Trim to the most relevant content; aim for ~400–700 words on one page.",
        })
    else:
        score = 100.0
    return _Dimension("content_density", "Content density", 0.12, _clamp(score), issues)


def _score_bullets(text: str) -> _Dimension:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    bullet_lines = sum(1 for ln in lines if ln[:1] in _BULLET_CHARS)
    low = text.lower()
    action_count = sum(1 for v in _ACTION_VERBS if v in low)
    metric_count = len(re.findall(r"\b\d+(?:\.\d+)?\s?(?:%|x|k|m|l|cr|lpa|\+)\b", low))
    issues: list[dict] = []
    score = 30.0
    score += min(30.0, bullet_lines * 4)
    score += min(25.0, action_count * 4)
    score += min(15.0, metric_count * 5)
    if bullet_lines < 3:
        issues.append({
            "id": "few_bullets",
            "severity": "medium",
            "message": "Very few bullet points detected. ATS and recruiters scan bullets, not paragraphs.",
            "fix": "Rewrite experience/projects as bullet points starting with action verbs.",
        })
    if action_count < 3:
        issues.append({
            "id": "weak_verbs",
            "severity": "medium",
            "message": "Few strong action verbs detected.",
            "fix": "Start bullets with verbs like Built, Developed, Optimized, Led.",
        })
    if metric_count == 0:
        issues.append({
            "id": "no_metrics",
            "severity": "low",
            "message": "No quantified impact found (numbers, %, x).",
            "fix": "Quantify results, e.g. 'reduced load time by 40%'.",
        })
    return _Dimension("bullet_structure", "Bullet & impact structure", 0.10, _clamp(score), issues)


def _score_cleanliness(text: str) -> _Dimension:
    issues: list[dict] = []
    score = 100.0
    if "�" in text or "\x00" in text:
        score -= 25
        issues.append({
            "id": "encoding_artifacts",
            "severity": "high",
            "message": "Encoding artifacts (�) detected — the PDF did not extract cleanly.",
            "fix": "Re-export the resume as a fresh text-based PDF from your editor.",
        })
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if lines:
        caps_lines = sum(1 for ln in lines if ln.isupper() and len(ln) > 12)
        if caps_lines / len(lines) > 0.3:
            score -= 12
            issues.append({
                "id": "excessive_caps",
                "severity": "low",
                "message": "Large blocks of ALL-CAPS text detected; harder to parse and read.",
                "fix": "Reserve capitals for section headings; use sentence case elsewhere.",
            })
        long_lines = sum(1 for ln in lines if len(ln) > 200)
        if long_lines > 2:
            score -= 10
            issues.append({
                "id": "wall_of_text",
                "severity": "low",
                "message": "Very long unbroken lines detected (possible merged columns).",
                "fix": "Break dense paragraphs into discrete bullet points.",
            })
    return _Dimension("parse_cleanliness", "Parse cleanliness", 0.08, _clamp(score), issues)


def analyze_ats(text: str, ats_flags: list[str] | None = None) -> dict:
    """Content-aware ATS parse-safety analysis.

    Returns a differentiated 0–100 score, per-dimension checks, and a flat,
    severity-ranked issue list with concrete fixes.
    """
    text = text or ""
    ats_flags = ats_flags or []

    dimensions = [
        _score_contact(text),
        _score_sections(text),
        _score_formatting(text, ats_flags),
        _score_dates(text),
        _score_density(text),
        _score_bullets(text),
        _score_cleanliness(text),
    ]

    overall = _clamp(sum(d.weight * d.score for d in dimensions))

    checks = [
        {
            "key": d.key,
            "label": d.label,
            "score": d.score,
            "weight": round(d.weight, 2),
            "status": _bucket(d.score),
        }
        for d in dimensions
    ]

    severity_rank = {"high": 0, "medium": 1, "low": 2}
    issues: list[dict] = []
    for d in dimensions:
        for issue in d.issues:
            issues.append({**issue, "dimension": d.key})
    issues.sort(key=lambda i: severity_rank.get(i.get("severity", "low"), 3))

    return {
        "ats_parse_safety": overall,
        "bucket": _bucket(overall),
        "checks": checks,
        "issues": issues,
    }
