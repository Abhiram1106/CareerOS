from __future__ import annotations

from fastapi import HTTPException, UploadFile

from ....extractor import _extract_ats_flags, build_section_payload, split_into_sections
from ....parsers import extract_docx, extract_pdf
from ..dto.parse_dto import ParseResponse

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
MAX_BYTES = 5 * 1024 * 1024


class ParseResumeHandler:
    async def execute(self, file: UploadFile) -> dict:
        content_type = file.content_type or ""
        if content_type not in ALLOWED_CONTENT_TYPES:
            fn = (file.filename or "").lower()
            if fn.endswith(".pdf"):
                content_type = "application/pdf"
            elif fn.endswith(".docx"):
                content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            else:
                raise HTTPException(
                    status_code=415,
                    detail="Only PDF and DOCX files are accepted.",
                )

        raw = await file.read()
        if len(raw) > MAX_BYTES:
            raise HTTPException(status_code=413, detail="File exceeds 5 MB limit.")

        if "pdf" in content_type:
            text, parse_warnings = extract_pdf(raw)
        else:
            text, parse_warnings = extract_docx(raw)

        if not text.strip():
            raise HTTPException(
                status_code=422,
                detail="Could not extract any text from the resume. "
                "If this is a scanned resume, OCR support is coming in Week 2.",
            )

        lines = text.split("\n")
        raw_sections = split_into_sections(lines)
        sections = build_section_payload(raw_sections)
        ats_flags = _extract_ats_flags(text)

        return ParseResponse(
            sections=sections,
            ats_flags=ats_flags,
            parse_warnings=parse_warnings,
            char_count=len(text),
        ).model_dump()
