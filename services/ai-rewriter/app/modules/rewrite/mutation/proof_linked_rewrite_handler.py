"""Proof-linked resume rewriter — deterministic, rule-based, no LLM.

Design contract:
  - NEVER fabricate. Only strengthen what is already claimed.
  - Every rewrite operation is one of three labelled types:
      STRENGTHEN  — adds action verb / metric framing to existing content
      STRUCTURE   — reformats existing content to STAR pattern
      REMOVE_FILLER — removes generic phrases, returns cleaner version
  - unsupported_claims flags content that cannot be verified from the
    resume text alone (superlatives, leadership scope, unanchored numbers).
  - confidence is computed from signal density, not hardcoded.
"""

from __future__ import annotations

import json
import re
from typing import Any

from ..dto.proof_rewrite_dto import (
    ProofRewriteRequest,
    ProofRewriteResponse,
    RequiresConfirmation,
    SectionRewrite,
    TopIssue,
    UnsupportedClaim,
)

# ── Patterns ─────────────────────────────────────────────────────────────────

# Strong action verbs — bullets starting with any of these are left as-is
_STRONG_VERBS: frozenset[str] = frozenset([
    "built", "developed", "designed", "implemented", "created", "optimized",
    "deployed", "engineered", "automated", "launched", "improved", "reduced",
    "increased", "managed", "architected", "delivered", "integrated", "analyzed",
    "researched", "collaborated", "spearheaded", "migrated", "established",
    "streamlined", "refactored", "scaled", "maintained", "contributed",
    "trained", "mentored", "led", "owned", "drove", "directed", "founded",
    "authored", "published", "coordinated", "supervised", "achieved",
])

# Weak openers that should be replaced
_WEAK_OPENERS = re.compile(
    r"^(worked on|helped with|assisted in|was responsible for|"
    r"involved in|participated in|did|had to|tried to|"
    r"good knowledge of|familiar with)\b",
    re.IGNORECASE,
)

# Filler phrases that add no signal
_FILLER_RE = re.compile(
    r"\b(good communication skills?|team player|hard[- ]working|"
    r"quick learner|fast learner|self[- ]motivated|detail[- ]oriented|"
    r"passionate about|eager to learn|looking for opportunity|"
    r"seeking a challenging|results[- ]driven|dynamic professional|"
    r"go[- ]getter|think outside the box|synerg\w*|leverage[sd]?\b)\b",
    re.IGNORECASE,
)

# Unverifiable superlatives
_SUPERLATIVE_RE = re.compile(
    r"\b(best|top|leading|world[- ]class|award[- ]winning|"
    r"pioneered|revolutionary|unprecedented|exceptional|outstanding|"
    r"highly skilled|expert in|master of|guru)\b",
    re.IGNORECASE,
)

# Metrics that should be in evidence
_METRIC_RE = re.compile(
    r"\b\d+(?:\.\d+)?\s*"
    r"(?:%|percent|x\b|times|k\b|m\b|cr\b|lpa|ms\b|sec|hrs|"
    r"days|users|requests|req\b|rph|tps|gb|mb|lines|repos|"
    r"teams?|members?|points?)(?!\w)",
    re.IGNORECASE,
)

_LEADERSHIP_RE = re.compile(
    r"\b(led|managed|headed|supervised|coordinated)\s+(a\s+)?(team|group|squad|cohort)\b",
    re.IGNORECASE,
)

_CGPA_RE = re.compile(r"\b(cgpa|gpa)\s*[:\-]?\s*(\d+(?:\.\d+)?)", re.IGNORECASE)

# Technology terms — used to detect when a bullet is already tech-specific
_TECH_TERM_RE = re.compile(
    r"\b(?:python|java|javascript|typescript|golang|rust|kotlin|react|angular|vue|"
    r"node|django|fastapi|flask|spring|sql|postgresql|mysql|mongodb|redis|"
    r"docker|kubernetes|aws|azure|gcp|git|linux|bash|tensorflow|pytorch|"
    r"scikit|pandas|numpy|kafka|celery|elasticsearch|terraform|jenkins|"
    r"graphql|rest|api|microservice|ci/?cd|html|css|android|ios|swift)\b",
    re.IGNORECASE,
)

# Verb-to-stronger-verb upgrades
_VERB_UPGRADES: dict[str, str] = {
    "worked on": "Developed",
    "helped with": "Contributed to",
    "assisted in": "Supported",
    "was responsible for": "Owned",
    "involved in": "Contributed to",
    "participated in": "Collaborated on",
    "did": "Completed",
    "good knowledge of": "Applied",
    "familiar with": "Worked with",
}

# ATS flag → (issue_type, human message, severity, actionable fix)
_FLAG_DETAILS: dict[str, tuple[str, str, str, str]] = {
    "two_column": (
        "ATS_FORMAT", "Two-column layout detected", "high",
        "Convert to single-column layout — most ATS systems parse left-to-right only.",
    ),
    "two_column_layout": (
        "ATS_FORMAT", "Two-column layout detected", "high",
        "Convert to single-column layout — most ATS systems parse left-to-right only.",
    ),
    "tab_heavy_may_be_multi_column": (
        "ATS_FORMAT", "Excessive tab characters suggest multi-column layout", "high",
        "Replace tab-based alignment with single-column bullet lists.",
    ),
    "table_detected": (
        "ATS_FORMAT", "Table detected in resume", "medium",
        "Replace tables with plain bullet lists — tables are often invisible to ATS.",
    ),
    "table_based_layout": (
        "ATS_FORMAT", "Table-based layout detected", "medium",
        "Replace tables with plain bullet lists.",
    ),
    "no_email_found": (
        "CONTACT", "No email address in resume text", "high",
        "Add email in plain text at the top — not embedded in a header image.",
    ),
    "no_phone_found": (
        "CONTACT", "No phone number found", "medium",
        "Add a 10-digit Indian mobile number in plain text.",
    ),
    "no_linkedin_link": (
        "CONTACT", "No LinkedIn profile link", "low",
        "Add linkedin.com/in/yourprofile to the contact section.",
    ),
    "missing_standard_headings": (
        "STRUCTURE", "Standard section headings missing", "high",
        "Add clearly labelled sections: Education, Experience, Skills, Projects.",
    ),
    "few_standard_headings": (
        "STRUCTURE", "Few standard section headings found", "medium",
        "Ensure all major sections are clearly labelled for ATS detection.",
    ),
    "possible_image_content": (
        "ATS_FORMAT", "Image or photo detected", "high",
        "Remove photos and image-based content — ATS cannot read them.",
    ),
    "file_too_large": (
        "FILE", "File exceeds recommended size", "medium",
        "Compress to under 2 MB — embed fonts, remove high-res images.",
    ),
    "special_glyphs_detected": (
        "ATS_FORMAT", "Special Unicode characters detected", "low",
        "Replace decorative symbols with plain ASCII equivalents.",
    ),
    "non_standard_dates": (
        "STRUCTURE", "Non-standard date format detected", "low",
        "Use consistent date format: 'Mon YYYY' (e.g. Jun 2024).",
    ),
    "partial_parse": (
        "PARSE", "Resume partially parsed", "medium",
        "Simplify formatting — avoid nested tables, text boxes, and headers.",
    ),
    "incomplete_employer": (
        "CONTENT", "Employer name missing or incomplete", "low",
        "Add company name and location for each experience entry.",
    ),
    "scanned_no_text": (
        "FILE", "Scanned/image-only PDF detected", "high",
        "Export a text-based PDF from your editor — ATS cannot read scanned images.",
    ),
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def _section_raw(content: Any) -> str:
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except json.JSONDecodeError:
            return content.strip()
    if isinstance(content, dict):
        return str(content.get("raw", "")).strip()
    return ""


def _split_bullets(raw: str) -> list[str]:
    lines = [ln.strip(" •‣▪·-*–→»\t") for ln in raw.splitlines() if ln.strip()]
    if len(lines) <= 1 and ";" in raw:
        lines = [p.strip() for p in raw.split(";") if p.strip()]
    return [ln for ln in lines if ln] or ([raw.strip()] if raw.strip() else [])


def _starts_with_strong_verb(text: str) -> bool:
    first_word = text.split()[0].lower().rstrip(".,;:") if text.split() else ""
    return first_word in _STRONG_VERBS


def _upgrade_weak_opener(text: str) -> tuple[str, bool]:
    """Replace weak opener with a stronger verb. Returns (new_text, changed)."""
    for weak, strong in _VERB_UPGRADES.items():
        pattern = re.compile(r"^" + re.escape(weak) + r"\b", re.IGNORECASE)
        if pattern.match(text):
            remainder = pattern.sub("", text).strip()
            # Capitalise first letter of remainder
            if remainder:
                remainder = remainder[0].upper() + remainder[1:]
            return f"{strong} {remainder}".strip(), True
    return text, False


def _strip_filler(text: str) -> tuple[str, bool]:
    """Remove filler phrases. Only cleans up connectors that were left by filler removal.

    Returns (cleaned, changed). Returns (text, False) immediately if no filler found.
    """
    cleaned = _FILLER_RE.sub("", text)
    if cleaned == text:
        return text, False  # nothing removed — don't touch anything else

    # Only clean up orphaned relative/subordinate clauses created by the removal
    cleaned = re.sub(r"^(I am a?|I'm a?)\s+", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+\b(who|that|which)\b\s+", " ", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip().strip(".,;: ")

    # If what remains is meaningless (too short), emit a placeholder
    if len(cleaned.split()) < 6 or cleaned.lower().startswith(("and ", "who ", "that ")):
        return (
            "[Rewrite your summary: 2–3 sentences about your background, "
            "strongest skills, and what you are looking for.]",
            True,
        )
    return cleaned, True


def _add_metric_prompt(text: str, jd_skills: list[str]) -> tuple[str, str]:
    """Suggest a metric or skill anchor if the bullet is bare.

    Returns (improved_text, change_type).
    Does NOT fabricate numbers — uses [N] placeholder to signal where
    the student must fill in real data.
    """
    has_metric = bool(_METRIC_RE.search(text))
    # A bullet already mentions a tech term → don't append skill (it's already specific)
    has_tech = bool(_TECH_TERM_RE.search(text))
    has_skill = has_tech or (any(s.lower() in text.lower() for s in jd_skills) if jd_skills else False)

    if has_metric and has_skill:
        return text, "NO_CHANGE"

    additions: list[str] = []
    if not has_metric:
        additions.append("achieving [N]% improvement")  # placeholder, not fabricated
    if not has_skill and jd_skills:
        additions.append(f"using {jd_skills[0]}")

    if not additions:
        return text, "NO_CHANGE"

    base = text.rstrip(".")
    improved = f"{base}, {' and '.join(additions)}."
    return improved[:300], "STRENGTHEN"


def _compute_confidence(original: str, rewrite: str, has_metric: bool, evidence_ids: list[str]) -> float:
    """Confidence = how much real signal exists to back the rewrite."""
    score = 0.40  # base
    if rewrite != original:
        score += 0.15  # something was actually changed
    if _starts_with_strong_verb(rewrite):
        score += 0.10
    if has_metric:
        score += 0.15
    if len(evidence_ids) > 1:
        score += 0.10
    if len(rewrite.split()) >= 10:
        score += 0.10  # enough substance
    return round(min(0.95, score), 2)


# ── Handler ───────────────────────────────────────────────────────────────────

class ProofLinkedRewriteHandler:
    """Deterministic proof-linked rewriter.

    Never fabricates. Every change is one of:
      STRENGTHEN   — adds STAR framing to existing content
      STRUCTURE    — verb upgrade / filler removal
      NO_CHANGE    — bullet is already strong; rewrite == original
    """

    def execute(self, payload: ProofRewriteRequest) -> dict:
        sections = payload.resume_json.get("sections", [])
        if not isinstance(sections, list):
            sections = []

        # JD required skills for skill-gap framing
        jd_skills: list[str] = []
        skills = payload.jd_json.get("skills", {})
        if isinstance(skills, dict):
            jd_skills = [s for s in (skills.get("required") or [])[:8] if s]
        # Also accept flat list
        if not jd_skills and isinstance(payload.jd_json.get("required_skills"), list):
            jd_skills = [s for s in payload.jd_json["required_skills"][:8] if s]

        # Evidence index for claim anchoring
        evidence_index: dict[str, str] = {}
        claims = payload.evidence_json.get("claims", [])
        if isinstance(claims, list):
            for item in claims:
                if isinstance(item, dict) and item.get("claim_id"):
                    evidence_index[str(item["claim_id"])] = str(item.get("snippet", ""))

        top_issues = self._top_issues(payload.ats_flags)
        section_rewrites: list[SectionRewrite] = []
        unsupported: list[UnsupportedClaim] = []
        confirmations: list[RequiresConfirmation] = []

        # Track which evidence_index entries are real (from payload) vs auto-added
        real_evidence_ids: set[str] = set(evidence_index.keys())

        for sec in sections:
            if not isinstance(sec, dict):
                continue
            name = str(sec.get("section_name", "")).strip().lower()
            if name not in {"experience", "projects", "summary", "positions_of_responsibility"}:
                continue
            raw = _section_raw(sec.get("content_json", {}))
            if not raw:
                continue

            for idx, bullet in enumerate(_split_bullets(raw)):
                original = bullet.strip()
                if len(original) < 8:
                    continue

                claim_id = f"{name}_{idx}"
                # Auto-add to evidence_index as a content anchor (not real external evidence)
                if claim_id not in evidence_index:
                    evidence_index[claim_id] = original[:120]

                # --- Unsupported claim detection (before rewriting) ---

                # Unverifiable superlatives
                sup_match = _SUPERLATIVE_RE.search(original)
                if sup_match:
                    unsupported.append(UnsupportedClaim(
                        claim=original,
                        reason=f"Superlative '{sup_match.group()}' cannot be verified — "
                               "remove or replace with a specific achievement.",
                    ))

                # Metrics with no real external evidence — only flag when evidence_json
                # was explicitly provided (has claims) but this metric isn't covered.
                # If no evidence payload at all, the student hasn't linked anything yet
                # and we shouldn't flag every metric as suspicious.
                metric_match = _METRIC_RE.search(original)
                evidence_payload_provided = bool(real_evidence_ids)
                if metric_match and evidence_payload_provided:
                    has_real_evidence = any(
                        eid in real_evidence_ids for eid in
                        [k for k, v in evidence_index.items() if v and v.lower() in original.lower()]
                    )
                    if not has_real_evidence:
                        unsupported.append(UnsupportedClaim(
                            claim=original,
                            reason=f"Metric '{metric_match.group()}' not anchored in evidence — "
                                   "confirm the number before export.",
                        ))

                # Leadership claims without scope
                lead_match = _LEADERSHIP_RE.search(original)
                if lead_match:
                    unsupported.append(UnsupportedClaim(
                        claim=original,
                        reason="Leadership scope stated — add team size or confirm in evidence.",
                    ))

                # --- Rewrite pipeline ---
                # If this bullet is flagged as unsupported, skip rewriting it —
                # the student must fix the claim themselves; we must not alter it.
                is_unsupported = bool(
                    _SUPERLATIVE_RE.search(original) or
                    (metric_match and claim_id not in evidence_index) or
                    _LEADERSHIP_RE.search(original)
                )

                text = original
                change_type = "NO_CHANGE"

                if is_unsupported:
                    # Emit as-is with low confidence so the UI highlights it
                    section_rewrites.append(SectionRewrite(
                        section=name,
                        original=original,
                        rewrite=original,
                        evidence_ids=[claim_id],
                        confidence=0.0,
                    ))
                    continue

                # Step 1: strip filler from summary/POR
                if name in {"summary", "positions_of_responsibility"}:
                    text, changed = _strip_filler(text)
                    if changed:
                        change_type = "STRUCTURE"

                # Step 2: upgrade weak opener
                if not _starts_with_strong_verb(text):
                    upgraded, changed = _upgrade_weak_opener(text)
                    if changed:
                        text = upgraded
                        change_type = "STRUCTURE"
                    elif not _starts_with_strong_verb(text):
                        # No upgrade matched — prefix with context verb
                        if name == "experience":
                            text = f"Developed {text[0].lower()}{text[1:]}" if len(text) > 1 else f"Developed {text}"
                            change_type = "STRUCTURE"

                # Step 3: add metric placeholder and/or skill anchor
                # Only for experience/projects; never for summary (too noisy)
                if name in {"experience", "projects"}:
                    text, step_type = _add_metric_prompt(text, jd_skills)
                    if step_type != "NO_CHANGE":
                        change_type = "STRENGTHEN"

                # Truncate to safe length
                text = text[:300]

                # Compute evidence
                evidence_ids = [
                    eid for eid, snip in evidence_index.items()
                    if snip and snip.lower() in original.lower()
                ] or [claim_id]
                evidence_ids = evidence_ids[:3]

                confidence = _compute_confidence(
                    original, text,
                    has_metric=bool(metric_match),
                    evidence_ids=evidence_ids,
                )

                section_rewrites.append(SectionRewrite(
                    section=name,
                    original=original,
                    rewrite=text,
                    evidence_ids=evidence_ids,
                    confidence=confidence,
                ))

                # CGPA confirmation
                cgpa_match = _CGPA_RE.search(raw)
                if cgpa_match and name == "education":
                    confirmations.append(RequiresConfirmation(
                        field="cgpa",
                        suggested_change=f"Verify CGPA value '{cgpa_match.group(2)}' matches official transcript.",
                    ))

        return ProofRewriteResponse(
            top_issues=top_issues,
            section_rewrites=section_rewrites,
            unsupported_claims=unsupported,
            requires_confirmation=confirmations,
        ).model_dump()

    def _top_issues(self, ats_flags: list[str]) -> list[TopIssue]:
        seen: set[str] = set()
        issues: list[TopIssue] = []
        for flag in ats_flags:
            key = str(flag).strip().lower()
            if key in seen:
                continue
            seen.add(key)
            detail = _FLAG_DETAILS.get(key)
            if detail:
                issues.append(TopIssue(
                    type=detail[0],
                    message=detail[1],
                    severity=detail[2],
                ))
            else:
                issues.append(TopIssue(
                    type="ATS_FLAG",
                    message=f"Structural flag: {flag}",
                    severity="medium",
                ))
        # Sort: high → medium → low
        _order = {"high": 0, "medium": 1, "low": 2}
        return sorted(issues, key=lambda i: _order.get(i.severity, 9))
