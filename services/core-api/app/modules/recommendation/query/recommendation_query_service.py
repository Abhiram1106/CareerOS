from __future__ import annotations

import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ....adapter.db.persistence.recommendation.recommendation_repo import RecommendationRepo
from ....adapter.db.persistence.resume.resume_view import ResumeView
from ....adapter.db.persistence.scorecard.scorecard_repo import ScorecardRepo
from ....models.entities import Recommendation, User
from ..dto.recommendation_dto import RecommendationItem, RunRewriteResponse


class RecommendationQueryService:
    def __init__(self, db: Session) -> None:
        self._scorecards = ScorecardRepo(db)
        self._resumes = ResumeView(db)
        self._recommendations = RecommendationRepo(db)

    def for_scorecard(self, user: User, scorecard_id: int) -> dict:
        scorecard = self._scorecards.find_by_id(scorecard_id)
        if not scorecard:
            raise HTTPException(status_code=404, detail="Scorecard not found")
        resume = self._resumes.find_by_id_for_user(scorecard.resume_id, user.id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")

        stored = self._recommendations.list_for_scorecard(scorecard_id)
        rewrites = [r for r in stored if r.rec_type == "REWRITE"]
        return RunRewriteResponse(
            scorecard_id=scorecard_id,
            section_rewrites=[
                {
                    "section": r.section,
                    "original": r.before_text,
                    "rewrite": r.after_text,
                    "evidence_ids": _parse_evidence(r),
                    "confidence": r.confidence,
                }
                for r in rewrites
            ],
            unsupported_claims=[
                {"claim": r.before_text, "reason": r.after_text}
                for r in stored
                if r.rec_type == "UNSUPPORTED"
            ],
            requires_confirmation=[
                {"field": r.section or r.before_text, "suggested_change": r.after_text}
                for r in stored
                if r.rec_type == "REQUIRES_CONFIRMATION"
            ],
            top_issues=[
                {"type": "ATS_FORMAT", "message": r.before_text, "severity": r.after_text}
                for r in stored
                if r.rec_type == "ATS_FORMAT"
            ],
            recommendations=[_to_item(r) for r in stored],
        ).model_dump()


def _parse_evidence(row: Recommendation) -> list[str]:
    try:
        data = json.loads(row.evidence_ids or "[]")
    except json.JSONDecodeError:
        return []
    return [str(x) for x in data] if isinstance(data, list) else []


def _to_item(row: Recommendation) -> RecommendationItem:
    return RecommendationItem(
        id=row.id,
        rec_type=row.rec_type,
        section=row.section,
        before_text=row.before_text,
        after_text=row.after_text,
        evidence_ids=_parse_evidence(row),
        confidence=row.confidence,
        accepted=row.accepted,
    )
