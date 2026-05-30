from __future__ import annotations

from careeros_scoring.parse_safety import (
    FLAG_PENALTIES,
    analyze_ats,
    ats_parse_safety_from_flags,
)

from ..dto.parse_safety_dto import ParseSafetyRequest, ParseSafetyResponse


class ParseSafetyHandler:
    def execute(self, payload: ParseSafetyRequest) -> dict:
        flags = payload.ats_flags
        penalties: dict[str, int] = {}
        unknown: list[str] = []
        for raw in flags:
            key = raw.strip().lower().replace(" ", "_")
            if key in FLAG_PENALTIES:
                penalties[key] = FLAG_PENALTIES[key]
            elif key:
                unknown.append(raw)

        if payload.resume_text.strip():
            report = analyze_ats(payload.resume_text, flags)
            return ParseSafetyResponse(
                ats_parse_safety=report["ats_parse_safety"],
                bucket=report["bucket"],
                checks=report["checks"],
                issues=report["issues"],
                penalties=penalties,
                unknown_flags=unknown,
            ).model_dump()

        score = ats_parse_safety_from_flags(flags)
        return ParseSafetyResponse(
            ats_parse_safety=score,
            bucket="good" if score >= 70 else "fair" if score >= 55 else "poor",
            checks=[],
            issues=[],
            penalties=penalties,
            unknown_flags=unknown,
        ).model_dump()
