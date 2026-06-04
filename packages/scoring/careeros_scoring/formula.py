"""PlacementReadinessScore weights and composition — do not duplicate elsewhere."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JdMatchBreakdown:
    """Components of the JD match sub-score.

    Note on ``embedding_cosine``: this slot is named for the role it plays
    in the formula, not for its current implementation. In Week 2 it is fed
    by a char-n-gram TF-IDF cosine (see ``services/match-engine``), which is
    a fast lexical proxy for semantic overlap. Week 5 swaps in a real
    sentence-embedding signal (OpenVINO MiniLM) without changing this slot.
    Consumers that need to display the actual method to the user should
    read ``semantic_method`` from the match-engine response, not invent it
    from this field name.
    """

    tfidf_cosine: float
    embedding_cosine: float
    required_skill_recall: float
    eligibility_rule_score: float

    @property
    def jd_match(self) -> float:
        return compute_jd_match(
            self.tfidf_cosine,
            self.embedding_cosine,
            self.required_skill_recall,
            self.eligibility_rule_score,
        )


@dataclass(frozen=True)
class PlacementReadinessResult:
    jd_match: float
    ats_parse_safety: float
    evidence_quality: float
    profile_completeness: float
    interview_readiness: float
    placement_hygiene: float
    overall_score: float
    bucket: str
    jd_match_breakdown: JdMatchBreakdown


def _clamp(score: float) -> float:
    return max(0.0, min(100.0, round(score, 1)))


def compute_jd_match(
    tfidf_cosine: float,
    embedding_cosine: float,
    required_skill_recall: float,
    eligibility_rule_score: float,
) -> float:
    return _clamp(
        0.35 * tfidf_cosine
        + 0.35 * embedding_cosine
        + 0.20 * required_skill_recall
        + 0.10 * eligibility_rule_score
    )


def bucket_label(overall_score: float) -> str:
    if overall_score >= 85:
        return "strong"
    if overall_score >= 70:
        return "ready"
    if overall_score >= 50:
        return "borderline"
    return "high-risk"


# ── CARE-RAG Layer 2: 7-class diagnostic quality classifier ──────────────────

QUALITY_CLASSES = (
    "ats_broken",
    "structurally_weak",
    "keyword_weak",
    "impact_weak",
    "role_misaligned",
    "high_potential_underwritten",
    "interview_ready",
)

QUALITY_CLASS_LABELS: dict[str, str] = {
    "ats_broken":                  "ATS Broken",
    "structurally_weak":           "Structurally Weak",
    "keyword_weak":                "Keyword Weak",
    "impact_weak":                 "Impact Weak",
    "role_misaligned":             "Role Misaligned",
    "high_potential_underwritten": "High Potential, Underwritten",
    "interview_ready":             "Interview Ready",
}

QUALITY_CLASS_GUIDANCE: dict[str, str] = {
    "ats_broken": (
        "ATS systems cannot parse your resume. "
        "Fix formatting first: remove tables, multi-column layouts, and images."
    ),
    "structurally_weak": (
        "Critical sections are missing or nearly empty. "
        "Add Education, Experience, Skills, and Projects sections."
    ),
    "keyword_weak": (
        "Your skills match the job, but they are not in your resume. "
        "Add exact JD keywords to your skills and experience sections."
    ),
    "impact_weak": (
        "Your bullets describe tasks, not outcomes. "
        "Add numbers: reduced X by 40%, built Y serving 2M requests/day."
    ),
    "role_misaligned": (
        "Your resume is well-written but targets a different role. "
        "Tailor it to this JD: lead with matching skills and relevant projects."
    ),
    "high_potential_underwritten": (
        "You have the right skills but your resume does not show it. "
        "Rewrite bullets to highlight what you built, how, and the impact."
    ),
    "interview_ready": (
        "Strong profile. Focus on JD-specific keyword tailoring "
        "and quantifying your top 2–3 achievements."
    ),
}


def classify_resume_quality(
    *,
    overall_score: float,
    ats_parse_safety: float,
    jd_match: float,
    evidence_quality: float,
    profile_completeness: float,
    required_skill_recall: float,
    ats_flags: list[str] | None = None,
) -> str:
    """Return the CARE-RAG Layer 2 quality class for this resume.

    Classes are evaluated in priority order — a resume can only have one class,
    the most severe applicable one wins. This keeps the diagnosis actionable:
    fix ATS Broken before worrying about keyword density.

    Returns one of the keys in ``QUALITY_CLASSES``.
    """
    flags = set(ats_flags or [])

    # 1. ATS Broken — parser cannot read the resume
    structural_flags = {
        "two_column", "two_column_layout", "table_detected", "table_based_layout",
        "tab_heavy_may_be_multi_column", "scanned_no_text",
    }
    if ats_parse_safety < 40 or flags & structural_flags:
        return "ats_broken"

    # 2. Structurally Weak — sections incomplete / missing
    if profile_completeness < 40:
        return "structurally_weak"

    # 3. Interview Ready — check before role_misaligned so a strong resume wins
    if overall_score >= 70:
        return "interview_ready"

    # 4. Role Misaligned — good resume structure, bad JD fit
    if ats_parse_safety >= 65 and jd_match < 35:
        return "role_misaligned"

    # 5. High Potential, Underwritten — parsed well but no evidence of impact
    if ats_parse_safety >= 65 and evidence_quality < 40:
        return "high_potential_underwritten"

    # 6. Keyword Weak — JD fit is low AND skill recall is low
    if jd_match < 40 and required_skill_recall < 30:
        return "keyword_weak"

    # 7. Impact Weak — default: content exists but bullets lack outcomes
    return "impact_weak"


def compute_placement_readiness(
    *,
    jd_match: float,
    ats_parse_safety: float,
    evidence_quality: float,
    profile_completeness: float,
    interview_readiness: float,
    placement_hygiene: float,
    jd_match_breakdown: JdMatchBreakdown | None = None,
) -> PlacementReadinessResult:
    jd = _clamp(jd_match)
    ats = _clamp(ats_parse_safety)
    evidence = _clamp(evidence_quality)
    complete = _clamp(profile_completeness)
    interview = _clamp(interview_readiness)
    hygiene = _clamp(placement_hygiene)

    overall = _clamp(
        0.35 * jd
        + 0.20 * ats
        + 0.20 * evidence
        + 0.10 * complete
        + 0.10 * interview
        + 0.05 * hygiene
    )

    breakdown = jd_match_breakdown or JdMatchBreakdown(
        tfidf_cosine=jd,
        embedding_cosine=jd,
        required_skill_recall=jd,
        eligibility_rule_score=jd,
    )

    return PlacementReadinessResult(
        jd_match=jd,
        ats_parse_safety=ats,
        evidence_quality=evidence,
        profile_completeness=complete,
        interview_readiness=interview,
        placement_hygiene=hygiene,
        overall_score=overall,
        bucket=bucket_label(overall),
        jd_match_breakdown=breakdown,
    )
