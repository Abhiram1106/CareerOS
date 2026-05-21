from __future__ import annotations

from pydantic import BaseModel


class ExportResumeRequest(BaseModel):
    resume_id: int


class ExportQueueResponse(BaseModel):
    job_id: int
    status: str


class ExportStatusResponse(BaseModel):
    job_id: int
    status: str
    error_message: str | None = None
    has_file: bool
