from __future__ import annotations

import json
from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ...adapter.db.persistence.agent_run.agent_run_repo import AgentRunRepo
from ...adapter.db.persistence.job.job_repo import JobRepo
from ...adapter.db.persistence.resume.resume_view import ResumeView
from ...models.entities import User
from ...services.audit import record_audit
from ...services.clients import jobs_feed_search, run_ats_parse_safety
from ..export.dto.export_dto import ExportResumeRequest
from ..export.mutation.queue_export_handler import QueueExportHandler
from ..recommendation.dto.recommendation_dto import RunRewriteRequest
from ..recommendation.mutation.run_rewrite_handler import RunRewriteHandler
from ..scorecard.dto.scorecard_dto import ScorecardScoreRequest
from ..scorecard.mutation.score_resume_handler import ScoreResumeHandler
from .dto.agent_dto import AgentRunRequest, AgentRunStepState


class AgentStateMachine:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._runs = AgentRunRepo(db)
        self._jobs = JobRepo(db)
        self._resumes = ResumeView(db)

    async def execute(self, user: User, payload: AgentRunRequest) -> dict:
        resume = self._resumes.find_by_id_for_user(payload.resume_id, user.id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")

        run = self._runs.create(
            student_id=user.id,
            resume_id=resume.id,
            summary_json=json.dumps({}),
            status="running",
        )
        summary: dict[str, Any] = {}

        sections = self._resumes.sections_for_resume(resume.id)
        if not sections and not (resume.content_text or "").strip():
            self._runs.update_step(
                run,
                current_step="PARSED",
                summary_json=json.dumps({"error": "resume has no parsed sections"}),
                status="failed",
                finished=True,
            )
            raise HTTPException(status_code=400, detail="Resume is missing parsed sections")

        summary["parsed"] = {
            "resume_id": resume.id,
            "section_count": len(sections),
            "source_format": resume.source_format or "uploaded",
        }
        self._runs.update_step(run, current_step="PARSED", summary_json=json.dumps(summary))

        ats_result = await run_ats_parse_safety(payload.ats_flags)
        summary["ats"] = {
            "flags": payload.ats_flags,
            "parse_safety_score": float(ats_result.get("parse_safety_score", 0)),
            "penalty_weight": float(ats_result.get("penalty_weight", 0)),
        }
        self._runs.update_step(run, current_step="ATS_SCORED", summary_json=json.dumps(summary))

        job_row, jd_text, company, role = await self._resolve_job(run.id, payload)
        summary["jd_resolved"] = {
            "job_id": job_row.id if job_row else None,
            "company": company,
            "role": role,
            "jd_char_count": len(jd_text),
        }
        self._runs.update_step(
            run,
            current_step="JD_RESOLVED",
            summary_json=json.dumps(summary),
            job_id=job_row.id if job_row else None,
        )

        score_payload = ScorecardScoreRequest(
            resume_id=resume.id,
            jd_text=jd_text,
            jd_id=None,
            company=company,
            role=role,
            ats_flags=payload.ats_flags,
            college_id=None,
        )
        score_result = await ScoreResumeHandler(self._db).execute(user, score_payload)
        scorecard_id = int(score_result["scorecard_id"])
        summary["jd_matched"] = {
            "scorecard_id": scorecard_id,
            "overall_score": float(score_result.get("overall_score", 0)),
            "bucket": str(score_result.get("bucket", "high-risk")),
        }
        self._runs.update_step(
            run,
            current_step="JD_MATCHED",
            summary_json=json.dumps(summary),
            scorecard_id=scorecard_id,
        )

        rewrite_result = await RunRewriteHandler(self._db).execute(
            user,
            RunRewriteRequest(scorecard_id=scorecard_id),
        )
        summary["rewritten"] = {
            "top_issues": len(rewrite_result.get("top_issues", [])),
            "section_rewrites": len(rewrite_result.get("section_rewrites", [])),
            "unsupported_claims": len(rewrite_result.get("unsupported_claims", [])),
        }
        self._runs.update_step(run, current_step="REWRITTEN", summary_json=json.dumps(summary))

        export_result = QueueExportHandler(self._db).execute(user, ExportResumeRequest(resume_id=resume.id))
        summary["export"] = {
            "job_id": int(export_result.get("job_id", 0)),
            "status": str(export_result.get("status", "queued")),
        }
        self._runs.update_step(run, current_step="EXPORT_READY", summary_json=json.dumps(summary))

        self._runs.update_step(
            run,
            current_step="DONE",
            summary_json=json.dumps(summary),
            status="completed",
            finished=True,
        )
        record_audit(
            self._db,
            actor_id=user.id,
            action="agent.run.completed",
            target_type="agent_run",
            target_id=run.id,
            payload={"scorecard_id": scorecard_id, "resume_id": resume.id},
        )
        return AgentRunStepState(
            run_id=run.id,
            status="completed",
            current_step="DONE",
            scorecard_id=scorecard_id,
            job_id=job_row.id if job_row else None,
            export_job_id=summary["export"]["job_id"],
            summary=summary,
        ).model_dump()

    async def _resolve_job(self, run_id: int, payload: AgentRunRequest) -> tuple[Any, str, str, str]:
        if payload.job_id is not None:
            row = self._jobs.find_by_id(payload.job_id)
            if not row:
                raise HTTPException(status_code=404, detail="Job not found")
            return row, row.raw_jd_text, row.company or "Company", row.title or "Role"

        if payload.jd_text.strip():
            row = self._jobs.upsert_from_feed(
                {
                    "source": "manual",
                    "external_id": f"manual-{run_id}",
                    "title": "Manual JD",
                    "company": "Manual",
                    "location": payload.location or "India",
                    "skills_required": [],
                    "raw_jd_text": payload.jd_text.strip(),
                }
            )
            return row, row.raw_jd_text, row.company or "Manual", row.title or "Manual JD"

        feed = await jobs_feed_search(payload.job_query.strip(), payload.location.strip(), page=1)
        results = feed.get("results", [])
        if not isinstance(results, list) or not results:
            raise HTTPException(status_code=404, detail="No jobs found for query")
        first = results[0] if isinstance(results[0], dict) else {}
        row = self._jobs.upsert_from_feed(first)
        return row, row.raw_jd_text, row.company or "Company", row.title or "Role"
