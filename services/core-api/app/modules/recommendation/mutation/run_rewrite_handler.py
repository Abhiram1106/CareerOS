from __future__ import annotations

import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ....adapter.db.persistence.jd.jd_repo import JDRepo
from ....adapter.db.persistence.recommendation.recommendation_repo import RecommendationRepo
from ....adapter.db.persistence.resume.resume_view import ResumeView
from ....adapter.db.persistence.scorecard.scorecard_repo import ScorecardRepo
from ....models.entities import Recommendation, ResumeEvidence, User
from ....services.clients import proof_linked_rewrite
from ..dto.recommendation_dto import RecommendationItem, RunRewriteRequest, RunRewriteResponse


class RunRewriteHandler:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._scorecards = ScorecardRepo(db)
        self._resumes = ResumeView(db)
        self._jds = JDRepo(db)
        self._recommendations = RecommendationRepo(db)

    async def execute(self, user: User, payload: RunRewriteRequest) -> dict:
        scorecard = self._scorecards.find_by_id(payload.scorecard_id)
        if not scorecard:
            raise HTTPException(status_code=404, detail="Scorecard not found")

        resume = self._resumes.find_by_id_for_user(scorecard.resume_id, user.id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")

        sections = self._resumes.sections_for_resume(scorecard.resume_id)
        section_dicts = [
            {
                "section_name": s.section_name,
                "content_json": ResumeView.parse_section_content(s.content_json),
            }
            for s in sections
        ]

        jd_row = self._jds.find_by_id(scorecard.jd_id)
        if not jd_row:
            raise HTTPException(status_code=404, detail="Job description not found")

        skills = json.loads(jd_row.skills_json or "{}")
        detail = json.loads(scorecard.score_detail_json or "{}")
        ats_flags = list(detail.get("ats_flags", []))

        evidence_rows = (
            self._db.query(ResumeEvidence).filter(ResumeEvidence.resume_id == scorecard.resume_id).all()
        )
        claims = [
            {"claim_id": row.claim_id, "snippet": row.proof_uri or row.claim_id, "status": row.status}
            for row in evidence_rows
        ]

        rewrite_payload = {
            "resume_json": {"sections": section_dicts},
            "jd_json": {
                "company": jd_row.company,
                "role": jd_row.role,
                "skills": skills,
                "raw_text": jd_row.raw_text[:2000],
            },
            "evidence_json": {"claims": claims},
            "ats_flags": ats_flags,
        }

        result = await proof_linked_rewrite(rewrite_payload)
        self._recommendations.delete_for_scorecard(scorecard.id)
        rows = self._rows_from_result(scorecard.id, result)
        if rows:
            self._recommendations.add_rows(rows)

        stored = self._recommendations.list_for_scorecard(scorecard.id)
        return RunRewriteResponse(
            scorecard_id=scorecard.id,
            top_issues=result.get("top_issues", []),
            section_rewrites=result.get("section_rewrites", []),
            unsupported_claims=result.get("unsupported_claims", []),
            requires_confirmation=result.get("requires_confirmation", []),
            recommendations=[self._to_item(r) for r in stored],
        ).model_dump()

    def _rows_from_result(self, scorecard_id: int, result: dict) -> list[Recommendation]:
        rows: list[Recommendation] = []
        for issue in result.get("top_issues", []):
            rows.append(
                Recommendation(
                    scorecard_id=scorecard_id,
                    rec_type="ATS_FORMAT",
                    section="",
                    before_text=str(issue.get("message", "")),
                    after_text=str(issue.get("severity", "medium")),
                    evidence_ids="[]",
                    confidence=0.9,
                )
            )
        for item in result.get("section_rewrites", []):
            rows.append(
                Recommendation(
                    scorecard_id=scorecard_id,
                    rec_type="REWRITE",
                    section=str(item.get("section", "")),
                    before_text=str(item.get("original", "")),
                    after_text=str(item.get("rewrite", "")),
                    evidence_ids=RecommendationRepo.evidence_ids_json(
                        list(item.get("evidence_ids", []))
                    ),
                    confidence=float(item.get("confidence", 0)),
                )
            )
        for item in result.get("unsupported_claims", []):
            rows.append(
                Recommendation(
                    scorecard_id=scorecard_id,
                    rec_type="UNSUPPORTED",
                    section="",
                    before_text=str(item.get("claim", "")),
                    after_text=str(item.get("reason", "")),
                    evidence_ids="[]",
                    confidence=0.0,
                )
            )
        for item in result.get("requires_confirmation", []):
            rows.append(
                Recommendation(
                    scorecard_id=scorecard_id,
                    rec_type="REQUIRES_CONFIRMATION",
                    section=str(item.get("field", "")),
                    before_text=str(item.get("field", "")),
                    after_text=str(item.get("suggested_change", "")),
                    evidence_ids="[]",
                    confidence=0.0,
                )
            )
        return rows

    @staticmethod
    def _to_item(row: Recommendation) -> RecommendationItem:
        try:
            evidence_ids = json.loads(row.evidence_ids or "[]")
        except json.JSONDecodeError:
            evidence_ids = []
        if not isinstance(evidence_ids, list):
            evidence_ids = []
        return RecommendationItem(
            id=row.id,
            rec_type=row.rec_type,
            section=row.section,
            before_text=row.before_text,
            after_text=row.after_text,
            evidence_ids=[str(x) for x in evidence_ids],
            confidence=row.confidence,
            accepted=row.accepted,
        )
