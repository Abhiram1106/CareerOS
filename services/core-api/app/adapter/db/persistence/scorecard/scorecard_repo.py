from __future__ import annotations

import json
from typing import Any, Optional

from sqlalchemy.orm import Session

from .....models.entities import Scorecard


class ScorecardRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def find_by_id(self, scorecard_id: int) -> Optional[Scorecard]:
        return self._db.query(Scorecard).filter(Scorecard.id == scorecard_id).first()

    def create_from_result(
        self,
        *,
        resume_id: int,
        jd_id: int,
        result: dict[str, Any],
        detail: dict[str, Any],
    ) -> Scorecard:
        row = Scorecard(
            resume_id=resume_id,
            jd_id=jd_id,
            jd_match=result["jd_match"],
            ats_safety=result["ats_parse_safety"],
            evidence_quality=result["evidence_quality"],
            profile_completeness=result["profile_completeness"],
            interview_readiness=result["interview_readiness"],
            placement_hygiene=result["placement_hygiene"],
            overall_score=result["overall_score"],
            bucket=result["bucket"],
            score_detail_json=json.dumps(detail),
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return row
