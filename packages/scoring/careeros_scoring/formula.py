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
