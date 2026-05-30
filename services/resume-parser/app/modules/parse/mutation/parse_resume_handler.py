from __future__ import annotations

from fastapi import HTTPException, UploadFile

from ....extractor import _extract_ats_flags, build_section_payload, split_into_sections
from ....parsers import extract_docx, extract_pdf, ocr_pdf
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

        # Scanned / image-only PDF: pdfplumber yields little or no text from a
        # large file — that combination indicates an image-only scan, not a sparse
        # resume. A legitimate sparse resume is small; a scanned PDF is large.
        if "pdf" in content_type and len(text.strip()) < 200 and len(raw) > 50_000:
            ocr_text, ocr_warnings = ocr_pdf(raw)
            parse_warnings.extend(ocr_warnings)
            if len(ocr_text.strip()) > len(text.strip()):
                text = ocr_text

        if not text.strip():
            raise HTTPException(
                status_code=422,
                detail="Could not extract any text from this file. It appears to be a "
                "scanned image with no recognizable text. Re-export a text-based PDF "
                "from your editor (File → Save as PDF), or upload a DOCX.",
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
            full_text=text,
        ).model_dump()
