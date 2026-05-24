from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from ...common.dto.strict import StrictModel


class AgentRunRequest(StrictModel):
    resume_id: int
    job_id: int | None = None
    jd_text: str = ""
    job_query: str = ""
    location: str = ""
    ats_flags: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_jd_source(self) -> "AgentRunRequest":
        has_job_id = self.job_id is not None
        has_jd_text = bool(self.jd_text.strip())
        has_query = bool(self.job_query.strip())
        if not (has_job_id or has_jd_text or has_query):
            raise ValueError("Provide one of: job_id, jd_text, or job_query")
        return self


class AgentRunStepState(BaseModel):
    run_id: int
    status: str
    current_step: str
    scorecard_id: int | None = None
    job_id: int | None = None
    export_job_id: int | None = None
    summary: dict = Field(default_factory=dict)
