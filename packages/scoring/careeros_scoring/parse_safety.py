"""ATS parse-safety from resume-parser flags (research-aligned penalties)."""

from __future__ import annotations

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
