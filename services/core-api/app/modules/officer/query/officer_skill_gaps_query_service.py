from __future__ import annotations

import json
from collections import Counter

from sqlalchemy.orm import Session

from ....adapter.db.persistence.officer.officer_cohort_view import OfficerCohortView
from ..dto.officer_dto import OfficerSkillGapItem, OfficerSkillGapsResponse
from ..officer_scope import resolve_officer_college_id


class OfficerSkillGapsQueryService:
    def __init__(self, db: Session) -> None:
        self._view = OfficerCohortView(db)
        self._college_id = resolve_officer_college_id(db)

    def get_skill_gaps(self, *, limit: int = 8) -> OfficerSkillGapsResponse:
        rows = self._view.latest_scorecards_by_student(self._college_id)
        counter: Counter[str] = Counter()

        for scorecard, _resume, _user, _profile in rows:
            try:
                detail = json.loads(scorecard.score_detail_json or "{}")
            except json.JSONDecodeError:
                detail = {}
            missing = detail.get("missing_required_skills") or []
            if isinstance(missing, list):
                for skill in missing:
                    if isinstance(skill, str) and skill.strip():
                        counter[skill.strip()] += 1

        items = [
            OfficerSkillGapItem(skill=skill, student_count=count)
            for skill, count in counter.most_common(limit)
        ]
        return OfficerSkillGapsResponse(items=items)
