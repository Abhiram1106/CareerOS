from __future__ import annotations

import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ....adapter.db.persistence.jd.jd_repo import JDRepo
from ....adapter.db.persistence.profile.profile_view import ProfileView
from ....adapter.db.persistence.resume.resume_view import ResumeView
from ....adapter.db.persistence.scorecard.scorecard_repo import ScorecardRepo
from ....models.entities import User
from ....services.clients import (
    get_adjacent_skills,
    match_resume_to_jd,
    parse_jd_text,
    skill_gap_with_graph,
    vector_index_jd,
    vector_index_resume,
)
import asyncio

from ..dto.scorecard_dto import GraphGapItem, QualityClassInfo, ScoreComponents, ScorecardScoreRequest, ScorecardScoreResponse

from careeros_scoring import (
    analyze_ats,
    classify_resume_quality,
    compute_placement_readiness,
    evidence_quality_score,
    interview_readiness_score,
    keyword_gap_analysis,
    placement_hygiene_score,
    profile_completeness_score,
    QUALITY_CLASS_GUIDANCE,
    QUALITY_CLASS_LABELS,
    resume_text_from_sections,
    simulate_vendors,
)
from careeros_scoring.formula import JdMatchBreakdown


class ScoreResumeHandler:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._resumes = ResumeView(db)
        self._profiles = ProfileView(db)
        self._jds = JDRepo(db)
        self._scorecards = ScorecardRepo(db)

    async def execute(self, user: User, payload: ScorecardScoreRequest) -> dict:
        resume = self._resumes.find_by_id_for_user(payload.resume_id, user.id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")

        sections = self._resumes.sections_for_resume(payload.resume_id)
        section_dicts = [
            {
                "section_name": s.section_name,
                "content_json": ResumeView.parse_section_content(s.content_json),
            }
            for s in sections
        ]
        resume_text = resume_text_from_sections(section_dicts)
        if resume.content_text and len(resume.content_text) > len(resume_text):
            resume_text = resume.content_text

        profile = self._profiles.find_by_user_id(user.id)
        profile_dict = {
            "skills_csv": profile.skills_csv if profile else "",
            "target_role": profile.target_role if profile else "",
            "city": profile.city if profile else "",
            "cgpa": profile.cgpa if profile else None,
            "active_backlogs": profile.active_backlogs if profile else 0,
            "branch": profile.branch if profile else "",
            "grad_year": profile.grad_year if profile else None,
        }

        jd_id = payload.jd_id
        required_skills: list[str] = []
        if jd_id:
            jd_row = self._jds.find_by_id(jd_id)
            if not jd_row:
                raise HTTPException(status_code=404, detail="Job description not found")
            jd_text = jd_row.raw_text
            skills = json.loads(jd_row.skills_json or "{}")
            required_skills = skills.get("required", [])
        else:
            jd_text = payload.jd_text
            parsed = await parse_jd_text(jd_text)
            required_skills = parsed.get("required_skills", [])
            company = payload.company.strip() or parsed.get("company", "Unknown")
            role = payload.role.strip() or parsed.get("role", "Role")
            jd_row = self._jds.create(
                created_by=user.id,
                company=company,
                role=role,
                raw_text=jd_text,
                skills_json=json.dumps(
                    {
                        "required": required_skills,
                        "optional": parsed.get("optional_skills", []),
                        "all": parsed.get("all_skills", []),
                    }
                ),
                eligibility_json=json.dumps(parsed.get("eligibility", {})),
            )
            jd_id = jd_row.id

        match = await match_resume_to_jd(
            {
                "resume_text": resume_text,
                "jd_text": jd_text,
                "required_skills": required_skills,
                "student_profile": profile_dict,
            }
        )

        breakdown = JdMatchBreakdown(
            tfidf_cosine=float(match["tfidf_cosine"]),
            embedding_cosine=float(match["embedding_cosine"]),
            required_skill_recall=float(match["required_skill_recall"]),
            eligibility_rule_score=float(match["eligibility_rule_score"]),
        )

        ats_report = analyze_ats(resume_text, payload.ats_flags)
        ats_safety = ats_report["ats_parse_safety"]
        evidence = evidence_quality_score(section_dicts)
        completeness = profile_completeness_score(section_dicts)
        interview = interview_readiness_score(section_dicts)
        hygiene = placement_hygiene_score(section_dicts, payload.ats_flags)

        placement = compute_placement_readiness(
            jd_match=breakdown.jd_match,
            ats_parse_safety=ats_safety,
            evidence_quality=evidence,
            profile_completeness=completeness,
            interview_readiness=interview,
            placement_hygiene=hygiene,
            jd_match_breakdown=breakdown,
        )

        weighted = {
            "jd_match": round(0.35 * placement.jd_match, 1),
            "ats_safety": round(0.20 * placement.ats_parse_safety, 1),
            "evidence": round(0.20 * placement.evidence_quality, 1),
            "completeness": round(0.10 * placement.profile_completeness, 1),
            "interview": round(0.10 * placement.interview_readiness, 1),
            "hygiene": round(0.05 * placement.placement_hygiene, 1),
        }

        detail = {
            "jd_match_breakdown": {
                "tfidf_cosine": breakdown.tfidf_cosine,
                "embedding_cosine": breakdown.embedding_cosine,
                "required_skill_recall": breakdown.required_skill_recall,
                "eligibility_rule_score": breakdown.eligibility_rule_score,
            },
            "raw_scores": {
                "jd_match": placement.jd_match,
                "ats_parse_safety": placement.ats_parse_safety,
                "evidence_quality": placement.evidence_quality,
                "profile_completeness": placement.profile_completeness,
                "interview_readiness": placement.interview_readiness,
                "placement_hygiene": placement.placement_hygiene,
            },
            "weighted_components": weighted,
            "match_method": match.get("match_method"),
            "semantic_method": match.get("semantic_method", "char_ngram_proxy"),
            "ats_flags": list(payload.ats_flags),
            "ats_checks": ats_report["checks"],
            "ats_issues": ats_report["issues"],
            "ats_bucket": ats_report["bucket"],
            "vendor_simulation": simulate_vendors(resume_text, jd_text),
            "keyword_gap": keyword_gap_analysis(resume_text, jd_text),
        }

        row = self._scorecards.create_from_result(
            resume_id=payload.resume_id,
            jd_id=jd_id,
            result={
                "jd_match": placement.jd_match,
                "ats_parse_safety": placement.ats_parse_safety,
                "evidence_quality": placement.evidence_quality,
                "profile_completeness": placement.profile_completeness,
                "interview_readiness": placement.interview_readiness,
                "placement_hygiene": placement.placement_hygiene,
                "overall_score": placement.overall_score,
                "bucket": placement.bucket,
            },
            detail=detail,
        )

        # CARE-RAG Layer 2: compute diagnostic quality class
        qc_key = classify_resume_quality(
            overall_score=placement.overall_score,
            ats_parse_safety=placement.ats_parse_safety,
            jd_match=placement.jd_match,
            evidence_quality=placement.evidence_quality,
            profile_completeness=placement.profile_completeness,
            required_skill_recall=float(breakdown.required_skill_recall),
            ats_flags=list(payload.ats_flags),
        )
        quality_class_info = QualityClassInfo(
            key=qc_key,
            label=QUALITY_CLASS_LABELS[qc_key],
            guidance=QUALITY_CLASS_GUIDANCE[qc_key],
        )

        # CARE-RAG Layer 3: fire-and-forget indexing into vector knowledge base
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(
                self._background_index(
                    user=user,
                    resume_text=resume_text,
                    qc_key=qc_key,
                    overall_score=placement.overall_score,
                    evidence_quality=placement.evidence_quality,
                    jd_id=jd_id,
                    jd_text=jd_text,
                    jd_role=getattr(jd_row, "role", "") if jd_row else "",
                    required_skills=required_skills,
                )
            )
        except RuntimeError:
            pass  # no running event loop in sync context — skip indexing

        return ScorecardScoreResponse(
            scorecard_id=row.id,
            jd_id=jd_id,
            overall_score=placement.overall_score,
            bucket=placement.bucket,
            quality_class=quality_class_info,
            components=ScoreComponents(**weighted),
            raw={
                "jd_match": placement.jd_match,
                "ats_parse_safety": placement.ats_parse_safety,
                "evidence_quality": placement.evidence_quality,
                "profile_completeness": placement.profile_completeness,
                "interview_readiness": placement.interview_readiness,
                "placement_hygiene": placement.placement_hygiene,
            },
            missing_required_skills=match.get("missing_required_skills", []),
            matched_skills=match.get("matched_skills", []),
            semantic_method=match.get("semantic_method", "char_ngram_proxy"),
            ats_bucket=ats_report["bucket"],
            ats_checks=ats_report["checks"],
            ats_issues=ats_report["issues"],
            vendor_simulation=detail["vendor_simulation"],
            keyword_gap=detail["keyword_gap"],
            graph_gap=[
                GraphGapItem(**item)
                for item in await skill_gap_with_graph(
                    known_skills=match.get("matched_skills", []),
                    missing_skills=match.get("missing_required_skills", []),
                )
            ],
        ).model_dump()

    async def _background_index(
        self,
        user: User,
        resume_text: str,
        qc_key: str,
        overall_score: float,
        evidence_quality: float,
        jd_id: int,
        jd_text: str,
        jd_role: str,
        required_skills: list,
    ) -> None:
        """Fire-and-forget: index into CARE-RAG vector store after scoring.

        Only resumes classified as interview_ready are indexed into Resume Patterns
        (so the knowledge base contains only successful examples).
        All JDs are indexed for the JD Intelligence Index.
        Errors are silently swallowed — vector indexing must never break scoring.
        """
        try:
            # Always index the JD
            await vector_index_jd(
                jd_id=jd_id,
                jd_text=jd_text,
                role=jd_role,
                required_skills=required_skills,
            )
            # Only index Interview Ready resumes into Resume Patterns
            if qc_key == "interview_ready" and resume_text.strip():
                await vector_index_resume({
                    "resume_id": 0,  # anonymised — no resume_id leaked
                    "user_id": user.id,
                    "resume_text": resume_text,
                    "role_family": jd_role,
                    "quality_class": qc_key,
                    "overall_score": overall_score,
                    "evidence_score": evidence_quality,
                })
        except Exception:
            pass  # non-blocking — never raise
