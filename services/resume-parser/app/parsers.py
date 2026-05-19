"""PDF and DOCX text extraction."""
from __future__ import annotations

import io
from typing import Tuple


def extract_pdf(content: bytes) -> Tuple[str, list[str]]:
    """
    Extract text from a native (machine-generated) PDF.
    Returns (full_text, warnings).
    """
    try:
        import pdfplumber
    except ImportError:
        return "", ["pdfplumber_not_installed"]

    warnings: list[str] = []
    pages_text: list[str] = []

    try:
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                text = page.extract_text(x_tolerance=3, y_tolerance=3)
                if text:
                    pages_text.append(text)
                else:
                    warnings.append(f"page_{page.page_number}_no_text_extracted")
    except Exception as exc:
        warnings.append(f"pdf_parse_error:{exc}")

    full_text = "\n".join(pages_text)

    # Heuristic: if very little text extracted and file is large → likely scanned
    if len(full_text.strip()) < 200 and len(content) > 50_000:
        warnings.append("likely_scanned_resume_ocr_fallback_needed")

    return full_text, warnings


def extract_docx(content: bytes) -> Tuple[str, list[str]]:
    """Extract text from a DOCX file. Returns (full_text, warnings)."""
    try:
        from docx import Document
    except ImportError:
        return "", ["python_docx_not_installed"]

    warnings: list[str] = []
    paragraphs: list[str] = []

    try:
        doc = Document(io.BytesIO(content))
        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text)

        # Also pull text from tables (common for skills sections)
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    paragraphs.append(row_text)
                    if not any("table" in w for w in warnings):
                        warnings.append("table_content_detected_may_affect_ats")
    except Exception as exc:
        warnings.append(f"docx_parse_error:{exc}")

    return "\n".join(paragraphs), warnings
