from __future__ import annotations

import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ....adapter.db.persistence.agent_run.agent_run_repo import AgentRunRepo
from ....models.entities import User
from ..dto.agent_dto import AgentRunStepState


class AgentRunQueryService:
    def __init__(self, db: Session) -> None:
        self._runs = AgentRunRepo(db)

    def get_for_student(self, user: User, run_id: int) -> dict:
        row = self._runs.find_for_user(run_id, user.id)
        if not row:
            raise HTTPException(status_code=404, detail="Agent run not found")
        try:
            summary = json.loads(row.summary_json or "{}")
        except json.JSONDecodeError:
            summary = {}
        if not isinstance(summary, dict):
            summary = {}
        export_job_id = None
        export_state = summary.get("export")
        if isinstance(export_state, dict):
            raw_job_id = export_state.get("job_id")
            if isinstance(raw_job_id, int):
                export_job_id = raw_job_id
        return AgentRunStepState(
            run_id=row.id,
            status=row.status,
            current_step=row.current_step,
            scorecard_id=row.scorecard_id,
            job_id=row.job_id,
            export_job_id=export_job_id,
            summary=summary,
        ).model_dump()
