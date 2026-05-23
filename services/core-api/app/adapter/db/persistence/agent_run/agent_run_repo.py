from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from .....models.entities import AgentRun


class AgentRunRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, *, student_id: int, resume_id: int, summary_json: str, status: str) -> AgentRun:
        row = AgentRun(
            student_id=student_id,
            resume_id=resume_id,
            summary_json=summary_json,
            status=status,
            current_step="INIT",
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return row

    def find_for_user(self, run_id: int, student_id: int) -> Optional[AgentRun]:
        return (
            self._db.query(AgentRun)
            .filter(AgentRun.id == run_id, AgentRun.student_id == student_id)
            .first()
        )

    def update_step(
        self,
        row: AgentRun,
        *,
        current_step: str,
        summary_json: str,
        status: Optional[str] = None,
        scorecard_id: Optional[int] = None,
        job_id: Optional[int] = None,
        finished: bool = False,
    ) -> AgentRun:
        row.current_step = current_step
        row.summary_json = summary_json
        if status is not None:
            row.status = status
        if scorecard_id is not None:
            row.scorecard_id = scorecard_id
        if job_id is not None:
            row.job_id = job_id
        if finished:
            row.finished_at = datetime.utcnow()
        self._db.commit()
        self._db.refresh(row)
        return row
