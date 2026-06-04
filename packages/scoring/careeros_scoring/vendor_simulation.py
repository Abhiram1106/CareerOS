"""Multi-vendor ATS simulation engine.

Simulates how 7 major ATS systems parse and score a resume, weighted by
prevalence in Indian and global job markets. Returns a weighted composite
plus per-vendor breakdown so candidates can optimise for the systems most
used by their target companies.

Vendor weights (Indian + global market prevalence, 2024):
  Taleo (Oracle)  18% — strict headers, rejects tables, keyword matching
  Workday         16% — modern parser, strong keyword + skills scoring
  Naukri RMS      15% — India-specific, understands CGPA, degree names
  Greenhouse      12% — startup/product companies, keyword density focus
  PeopleStrong    10% — Indian HR tech, handles regional names + CGPA
  Darwinbox        9% — Indian enterprise, similar to Workday
  Lever            8% — startup, lenient formatting, experience-focused

Each vendor function returns a score 0–100 based on its specific rules.
The composite is a weighted average of all vendor scores.
"""

from __future__ import annotations

import re

# ── Shared helpers ─────────────────────────────────────────────────────────

_EMAIL_RE = re.compile(r"[\w.+%-]+@[\w-]+\.[\w.-]+")
_PHONE_RE = re.compile(r"(?:\+?91[\s-]?)?(?<!\d)[6-9]\d{9}(?!\d)")
_LINKEDIN_RE = re.compile(r"linkedin\.com/\S+", re.IGNORECASE)
_GITHUB_RE = re.compile(r"(?:github|gitlab)\.com/\S+", re.IGNORECASE)

_METRIC_RE = re.compile(
    r"\b\d+(?:\.\d+)?\s?(?:%|percent|x\b|times|k\b|m\b|cr\b|lpa|ms\b|sec|"
    r"days|users|requests|req\b|rps|tps|gb|mb|teams?|members?)(?!\w)",
    re.IGNORECASE,
)

_ACTION_VERBS = frozenset([
    "built", "developed", "designed", "implemented", "led", "optimized",
    "deployed", "created", "engineered", "automated", "launched", "improved",
    "reduced", "increased", "managed", "architected", "delivered", "integrated",
    "analyzed", "researched", "collaborated", "spearheaded", "migrated",
    "established", "streamlined", "refactored", "scaled", "mentored",
])

_STANDARD_HEADERS = [
    "education", "experience", "skills", "projects", "work experience",
    "internship", "technical skills", "certifications", "summary", "objective",
]

_INDIAN_DEGREES = [
    "b.tech", "btech", "b.e.", "be ", "m.tech", "mtech", "bca", "mca",
    "b.sc", "bsc", "m.sc", "msc", "mba", "b.com", "bcom",
]

_TABLE_CHARS = re.compile(r"[│┌┐└┘├┤┬┴┼╔╗╚╝║═]")
_BULLET_CHARS = frozenset("•◦▪‣·-*–→»")


def _word_count(text: str) -> int:
    return len(text.split())


def _has_standard_headers(text: str) -> int:
    """Count how many standard section headers are present."""
    low = text.lower()
    return sum(1 for h in _STANDARD_HEADERS if re.search(rf"\b{re.escape(h)}\b", low))


def _has_action_verbs(text: str) -> int:
    """Count distinct action verbs in the text."""
    low = text.lower()
    return sum(1 for v in _ACTION_VERBS if re.search(rf"\b{v}\b", low))


def _has_tables(text: str) -> bool:
    return bool(_TABLE_CHARS.search(text))


def _has_metrics(text: str) -> int:
    return len(_METRIC_RE.findall(text))


def _has_bullets(text: str) -> bool:
    lines = text.splitlines()
    bullet_lines = sum(1 for l in lines if l.strip() and l.strip()[0] in _BULLET_CHARS)
    return bullet_lines >= 3


def _bullet_fraction(text: str) -> float:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return 0.0
    bullet_lines = sum(1 for l in lines if l[0] in _BULLET_CHARS)
    return bullet_lines / len(lines)


def _keyword_overlap(resume: str, jd: str) -> float:
    """Fraction of meaningful JD words found in resume (0.0–1.0)."""
    stop = {
        "the", "a", "an", "and", "or", "in", "on", "at", "to", "for",
        "with", "of", "is", "are", "be", "we", "you", "will", "our",
        "have", "has", "this", "that", "from", "by", "as", "it", "its",
    }
    jd_words = {w.lower() for w in re.findall(r"\b[a-zA-Z]{3,}\b", jd) if w.lower() not in stop}
    if not jd_words:
        return 0.0
    res_words = {w.lower() for w in re.findall(r"\b[a-zA-Z]{3,}\b", resume)}
    matched = jd_words & res_words
    return len(matched) / len(jd_words)


# ── Vendor scorers ─────────────────────────────────────────────────────────

def score_taleo(resume_text: str, jd_text: str) -> float:
    """Oracle Taleo — strict about section headers, heavily penalises tables.

    Known quirks: requires exact standard section heading words, rejects any
    table-based layout, weights keyword matching heavily, likes single-column.
    """
    score = 0.0

    # Section headers (40 pts): Taleo is the strictest about standard headings
    header_count = _has_standard_headers(resume_text)
    score += min(40, header_count * 8)

    # No tables (20 pts): hard penalty
    if not _has_tables(resume_text):
        score += 20

    # Keyword overlap (30 pts): Taleo does lexical matching
    if jd_text:
        overlap = _keyword_overlap(resume_text, jd_text)
        score += round(overlap * 30, 1)

    # Contact info (10 pts)
    contact = (4 if _EMAIL_RE.search(resume_text) else 0) + \
              (3 if _PHONE_RE.search(resume_text) else 0) + \
              (3 if _LINKEDIN_RE.search(resume_text) else 0)
    score += contact

    return round(min(100.0, score), 1)


def score_workday(resume_text: str, jd_text: str) -> float:
    """Workday — modern parser, strong keyword + structured data extraction.

    More lenient on formatting than Taleo, but heavily weights keyword match
    and structured skill extraction.
    """
    score = 0.0

    # Keyword matching (35 pts): primary Workday signal
    if jd_text:
        overlap = _keyword_overlap(resume_text, jd_text)
        score += round(overlap * 35, 1)

    # Contact completeness (15 pts)
    score += (7 if _EMAIL_RE.search(resume_text) else 0)
    score += (5 if _PHONE_RE.search(resume_text) else 0)
    score += (3 if _LINKEDIN_RE.search(resume_text) else 0)

    # Section structure (25 pts): Workday extracts structured sections
    header_count = _has_standard_headers(resume_text)
    score += min(25, header_count * 5)

    # Content quality (15 pts): action verbs + metrics
    verbs = min(10, _has_action_verbs(resume_text) * 2)
    metrics = min(5, _has_metrics(resume_text))
    score += verbs + metrics

    # No tables bonus (10 pts)
    if not _has_tables(resume_text):
        score += 10

    return round(min(100.0, score), 1)


def score_naukri_rms(resume_text: str, jd_text: str) -> float:
    """Naukri RMS — India-specific, understands CGPA, Indian degree names, locations.

    Rewards Indian academic formatting, handles regional content well.
    Less strict about two-column layouts than Western ATS.
    """
    score = 0.0
    low = resume_text.lower()

    # Indian academic signals (25 pts)
    cgpa_match = re.search(r"\b(?:cgpa|gpa)\s*[:\-]?\s*(\d+(?:\.\d+)?)", low)
    if cgpa_match:
        score += 12
    if any(deg in low for deg in _INDIAN_DEGREES):
        score += 8
    if re.search(r"\b(iit|nit|bits|vit|srm|iiit|anna university|mumbai university)\b", low):
        score += 5

    # Contact (20 pts): phone is critical for Naukri
    score += (8 if _PHONE_RE.search(resume_text) else 0)
    score += (7 if _EMAIL_RE.search(resume_text) else 0)
    score += (5 if _LINKEDIN_RE.search(resume_text) else 0)

    # Keyword match (30 pts)
    if jd_text:
        overlap = _keyword_overlap(resume_text, jd_text)
        score += round(overlap * 30, 1)

    # Section completeness (15 pts)
    header_count = _has_standard_headers(resume_text)
    score += min(15, header_count * 3)

    # Work experience signals (10 pts)
    if re.search(r"\b(intern|internship|trainee|fresher)\b", low):
        score += 5
    if _has_action_verbs(resume_text) >= 3:
        score += 5

    return round(min(100.0, score), 1)


def score_greenhouse(resume_text: str, jd_text: str) -> float:
    """Greenhouse — startup/product companies, keyword density + experience quality.

    Used by tech-forward companies. Rewards quantified achievements, GitHub,
    clean formatting. Less strict on exact header names.
    """
    score = 0.0

    # Keyword density (35 pts): primary Greenhouse signal
    if jd_text:
        overlap = _keyword_overlap(resume_text, jd_text)
        score += round(overlap * 35, 1)

    # GitHub / portfolio (15 pts): Greenhouse recruiters check this
    if _GITHUB_RE.search(resume_text):
        score += 15
    elif re.search(r"https?://\S+", resume_text):
        score += 8

    # Quantified achievements (20 pts)
    metrics = _has_metrics(resume_text)
    score += min(20, metrics * 4)

    # Action verbs (15 pts)
    verbs = _has_action_verbs(resume_text)
    score += min(15, verbs * 3)

    # Contact (15 pts)
    score += (8 if _EMAIL_RE.search(resume_text) else 0)
    score += (7 if _LINKEDIN_RE.search(resume_text) else 0)

    return round(min(100.0, score), 1)


def score_peoplestrong(resume_text: str, jd_text: str) -> float:
    """PeopleStrong — Indian HR tech, handles regional names and CGPA, lenient format.

    Common in Indian mid-size companies. More lenient about two-column layouts,
    highly tuned for CGPA and Indian academic credentials.
    """
    score = 0.0
    low = resume_text.lower()

    # CGPA and Indian credentials (30 pts): PeopleStrong's main differentiator
    if re.search(r"\b(?:cgpa|gpa|percentage)\b", low):
        score += 15
    if any(deg in low for deg in _INDIAN_DEGREES):
        score += 10
    if re.search(r"\b(class x|class xii|10th|12th|ssc|hsc|cbse|icse)\b", low):
        score += 5

    # Keyword match (25 pts)
    if jd_text:
        overlap = _keyword_overlap(resume_text, jd_text)
        score += round(overlap * 25, 1)

    # Contact (20 pts): phone especially important
    score += (10 if _PHONE_RE.search(resume_text) else 0)
    score += (7 if _EMAIL_RE.search(resume_text) else 0)
    score += (3 if _LINKEDIN_RE.search(resume_text) else 0)

    # Work experience (15 pts)
    header_count = _has_standard_headers(resume_text)
    score += min(10, header_count * 2)
    if _has_action_verbs(resume_text) >= 2:
        score += 5

    # Format tolerance (10 pts): PeopleStrong doesn't penalise tables heavily
    if not _has_tables(resume_text):
        score += 10
    else:
        score += 5  # partial credit

    return round(min(100.0, score), 1)


def score_darwinbox(resume_text: str, jd_text: str) -> float:
    """Darwinbox — growing Indian enterprise ATS, similar to Workday architecture.

    Strong keyword matching, structured section extraction, rewards digital presence.
    """
    score = 0.0

    # Keyword overlap (30 pts)
    if jd_text:
        overlap = _keyword_overlap(resume_text, jd_text)
        score += round(overlap * 30, 1)

    # Section structure (25 pts)
    header_count = _has_standard_headers(resume_text)
    score += min(25, header_count * 5)

    # Digital presence (15 pts): Darwinbox tracks LinkedIn + GitHub
    score += (8 if _LINKEDIN_RE.search(resume_text) else 0)
    score += (7 if _GITHUB_RE.search(resume_text) else 0)

    # Contact (15 pts)
    score += (8 if _EMAIL_RE.search(resume_text) else 0)
    score += (4 if _PHONE_RE.search(resume_text) else 0)
    score += (3 if re.search(r"\b(bengaluru|mumbai|delhi|hyderabad|pune|chennai)\b", resume_text, re.I) else 0)

    # Content quality (15 pts)
    score += min(10, _has_action_verbs(resume_text) * 2)
    score += min(5, _has_metrics(resume_text))

    return round(min(100.0, score), 1)


def score_lever(resume_text: str, jd_text: str) -> float:
    """Lever — startup ATS, most lenient on formatting, focuses on experience quality.

    Used by tech startups. Rewards quantified impact and GitHub presence.
    Accepts two-column layouts, doesn't require exact header names.
    """
    score = 0.0

    # Keyword match (25 pts): still important but less weighted than others
    if jd_text:
        overlap = _keyword_overlap(resume_text, jd_text)
        score += round(overlap * 25, 1)

    # GitHub is almost mandatory for Lever positions (20 pts)
    if _GITHUB_RE.search(resume_text):
        score += 20
    elif re.search(r"https?://\S+", resume_text):
        score += 8

    # Quantified achievements (25 pts): Lever heavily rewards metrics
    metrics = _has_metrics(resume_text)
    score += min(25, metrics * 5)

    # Experience depth (15 pts)
    verbs = _has_action_verbs(resume_text)
    score += min(15, verbs * 3)

    # Contact (15 pts)
    score += (8 if _EMAIL_RE.search(resume_text) else 0)
    score += (7 if _LINKEDIN_RE.search(resume_text) else 0)

    # No table penalty: Lever is lenient (0 penalty)

    return round(min(100.0, score), 1)


# ── Vendor registry ────────────────────────────────────────────────────────

VENDORS: list[dict] = [
    {"id": "taleo",        "name": "Taleo (Oracle)",   "weight": 0.18, "fn": score_taleo},
    {"id": "workday",      "name": "Workday",           "weight": 0.16, "fn": score_workday},
    {"id": "naukri_rms",   "name": "Naukri RMS",        "weight": 0.15, "fn": score_naukri_rms},
    {"id": "greenhouse",   "name": "Greenhouse",        "weight": 0.12, "fn": score_greenhouse},
    {"id": "peoplestrong", "name": "PeopleStrong",      "weight": 0.10, "fn": score_peoplestrong},
    {"id": "darwinbox",    "name": "Darwinbox",         "weight": 0.09, "fn": score_darwinbox},
    {"id": "lever",        "name": "Lever",             "weight": 0.08, "fn": score_lever},
]

_WEIGHT_SUM = sum(v["weight"] for v in VENDORS)  # 0.88 (remaining 12% = other systems)


def simulate_vendors(resume_text: str, jd_text: str = "") -> dict:
    """Run all vendor simulations and return composite + per-vendor breakdown.

    Returns:
      {
        "composite_score": float,          # weighted average across vendors
        "vendors": [                       # per-vendor detail
          {"id": str, "name": str, "score": float, "weight_pct": int},
          ...
        ]
      }
    """
    resume = (resume_text or "").strip()
    jd = (jd_text or "").strip()

    vendor_results = []
    weighted_sum = 0.0

    for v in VENDORS:
        score = v["fn"](resume, jd)
        vendor_results.append({
            "id": v["id"],
            "name": v["name"],
            "score": score,
            "weight_pct": round(v["weight"] * 100),
        })
        weighted_sum += v["weight"] * score

    # Normalise to 100 (the 7 vendors cover 88% of market; scale up proportionally)
    composite = round(weighted_sum / _WEIGHT_SUM, 1)

    return {
        "composite_score": max(0.0, min(100.0, composite)),
        "vendors": vendor_results,
    }


# ── Keyword gap analysis ───────────────────────────────────────────────────

_STOP_WORDS = frozenset([
    "the", "a", "an", "and", "or", "in", "on", "at", "to", "for", "with",
    "of", "is", "are", "be", "we", "you", "will", "our", "have", "has",
    "this", "that", "from", "by", "as", "it", "its", "your", "their",
    "who", "which", "about", "into", "through", "during", "before", "after",
    "above", "below", "up", "down", "out", "over", "under", "again",
    "experience", "strong", "good", "excellent", "ability", "knowledge",
])

_TECH_WEIGHT_RE = re.compile(
    r"\b(?:required|must have|mandatory|essential|should|preferred|nice.to.have)\b",
    re.IGNORECASE,
)


def keyword_gap_analysis(resume_text: str, jd_text: str) -> dict:
    """Identify JD keywords present/missing in the resume.

    Returns:
      {
        "matched": [{"keyword": str, "context": str}],
        "missing": [{"keyword": str, "importance": "high"|"medium"|"low"}],
        "match_rate": float (0–100),
        "total_jd_keywords": int,
      }
    """
    if not jd_text:
        return {"matched": [], "missing": [], "match_rate": 0.0, "total_jd_keywords": 0}

    # Extract meaningful JD keywords (3+ chars, not stop words)
    jd_words = [
        w.lower() for w in re.findall(r"\b[a-zA-Z][a-zA-Z0-9.#+\-]{2,}\b", jd_text)
        if w.lower() not in _STOP_WORDS
    ]
    # Deduplicate preserving order
    seen: set[str] = set()
    unique_jd: list[str] = []
    for w in jd_words:
        if w not in seen:
            seen.add(w)
            unique_jd.append(w)

    if not unique_jd:
        return {"matched": [], "missing": [], "match_rate": 0.0, "total_jd_keywords": 0}

    res_lower = resume_text.lower()
    # Split JD into lines to determine importance (keywords in first half = higher priority)
    jd_lines = jd_text.splitlines()
    total_lines = max(1, len(jd_lines))

    matched: list[dict] = []
    missing: list[dict] = []

    # Pre-compute JD keyword frequency for heatmap intensity
    jd_lower = jd_text.lower()

    for kw in unique_jd:
        pattern = re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE)
        frequency = len(pattern.findall(jd_text))  # times keyword appears in JD

        if pattern.search(res_lower):
            # Find a short context snippet from the JD
            jd_match = pattern.search(jd_text)
            context = ""
            if jd_match:
                start = max(0, jd_match.start() - 30)
                end = min(len(jd_text), jd_match.end() + 30)
                context = "…" + jd_text[start:end].strip() + "…"
            matched.append({"keyword": kw, "context": context[:120], "frequency": frequency})
        else:
            # Determine importance: keywords in first third of JD are "required"
            for i, line in enumerate(jd_lines):
                if kw.lower() in line.lower():
                    position_ratio = i / total_lines
                    importance = "high" if position_ratio < 0.33 else "medium" if position_ratio < 0.66 else "low"
                    break
            else:
                importance = "medium"
            missing.append({"keyword": kw, "importance": importance, "frequency": frequency})

    total = len(unique_jd)
    match_rate = round(len(matched) / total * 100, 1) if total else 0.0

    return {
        "matched": matched[:30],   # cap for response size
        "missing": missing[:30],
        "match_rate": match_rate,
        "total_jd_keywords": total,
    }
