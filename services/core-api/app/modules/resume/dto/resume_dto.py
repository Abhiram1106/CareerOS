from __future__ import annotations

from pydantic import BaseModel, Field


class ResumeGenerateRequest(BaseModel):
    template_name: str = "classic"


class ResumeListItem(BaseModel):
    id: int
    template_name: str
    created_at: str


class ResumeListResponse(BaseModel):
    resumes: list[ResumeListItem]


class ResumeDetailResponse(BaseModel):
    id: int
    template_name: str
    content: str
    created_at: str


class ResumeGenerateResponse(BaseModel):
    resume_id: int
    content: str


class ResumeSectionItem(BaseModel):
    section_name: str
    content_json: dict
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)


class ResumeSectionsResponse(BaseModel):
    resume_id: int
    source_format: str
    sections: list[ResumeSectionItem]


class ResumeUploadResponse(BaseModel):
    resume_id: int
    source_format: str
    sections: list[dict]
    ats_flags: list[str]
    parse_warnings: list[str]
    char_count: int


class ResumeDeleteResponse(BaseModel):
    ok: bool = True
