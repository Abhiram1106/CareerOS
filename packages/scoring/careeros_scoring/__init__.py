"""PlacementReadinessScore — single source of truth for CareerOS Campus AI."""

from .formula import (
    bucket_label,
    compute_jd_match,
    compute_placement_readiness,
)
from .parse_safety import analyze_ats, ats_parse_safety_from_flags
from .resume_components import (
    evidence_quality_score,
    interview_readiness_score,
    placement_hygiene_score,
    profile_completeness_score,
    resume_text_from_sections,
)

__all__ = [
    "analyze_ats",
    "ats_parse_safety_from_flags",
    "bucket_label",
    "compute_jd_match",
    "compute_placement_readiness",
    "evidence_quality_score",
    "interview_readiness_score",
    "placement_hygiene_score",
    "profile_completeness_score",
    "resume_text_from_sections",
]
