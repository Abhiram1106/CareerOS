from __future__ import annotations

from careeros_scoring.parse_safety import FLAG_PENALTIES, ats_parse_safety_from_flags

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

        score = ats_parse_safety_from_flags(flags)
        return ParseSafetyResponse(
            ats_parse_safety=score,
            penalties=penalties,
            unknown_flags=unknown,
        ).model_dump()
