from __future__ import annotations

import sys
from pathlib import Path

_SCORING_ROOT = Path(__file__).resolve().parents[6] / "packages" / "scoring"
if _SCORING_ROOT.is_dir() and str(_SCORING_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCORING_ROOT))

from careeros_scoring.parse_safety import FLAG_PENALTIES, ats_parse_safety_from_flags  # noqa: E402

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
