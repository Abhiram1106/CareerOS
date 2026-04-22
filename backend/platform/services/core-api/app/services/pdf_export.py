from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import quote

import boto3

from ..config import (
    EXPORT_SIGNED_URL_TTL_SECONDS,
    EXPORT_STORAGE,
    EXPORTS_DIR,
    S3_ENDPOINT_URL,
    S3_EXPORT_BUCKET,
    S3_EXPORT_PREFIX,
    S3_REGION,
    WEASYPRINT_ENABLED,
)


def ensure_export_dir() -> Path:
    path = Path(EXPORTS_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _safe_name(value: str) -> str:
    normalized = re.sub(r"\s+", "_", value.strip())
    cleaned = re.sub(r"[^A-Za-z0-9_.-]", "", normalized)
    return cleaned or "resume"


def _render_resume_html(full_name: str, content: str) -> str:
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    body_items = "".join(f"<li>{html.escape(line)}</li>" for line in lines[:80]) or "<li>Content unavailable</li>"
    template_path = Path(__file__).resolve().parents[1] / "templates" / "resume_export.html"
    template = template_path.read_text(encoding="utf-8")
    return template.replace("{{FULL_NAME}}", html.escape(full_name)).replace("{{CONTENT_ITEMS}}", body_items)


def _build_pdf_bytes(full_name: str, content: str) -> bytes:
    html_doc = _render_resume_html(full_name, content)
    if WEASYPRINT_ENABLED:
        try:
            # Imported lazily so non-Linux local dev environments don't fail app startup.
            from weasyprint import HTML

            return HTML(string=html_doc).write_pdf()
        except Exception:
            pass

    # Development-safe minimal PDF fallback when native WeasyPrint libs are unavailable.
    snippet = content[:300].replace("(", "[").replace(")", "]")
    payload = (
        "%PDF-1.1\n"
        "1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        "2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n"
        "3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj\n"
        f"4 0 obj<</Length {len(snippet) + 40}>>stream\nBT /F1 12 Tf 72 740 Td ({full_name}) Tj ET\n"
        f"BT /F1 10 Tf 72 720 Td ({snippet}) Tj ET\n"
        "endstream endobj\n"
        "xref\n0 5\n0000000000 65535 f \n"
        "trailer<</Size 5/Root 1 0 R>>\nstartxref\n0\n%%EOF\n"
    )
    return payload.encode("latin-1", errors="ignore")


def _s3_client():
    kwargs = {"region_name": S3_REGION}
    if S3_ENDPOINT_URL:
        kwargs["endpoint_url"] = S3_ENDPOINT_URL
    return boto3.client("s3", **kwargs)


def _is_s3_enabled() -> bool:
    return EXPORT_STORAGE == "s3" and bool(S3_EXPORT_BUCKET)


def _s3_key(filename: str) -> str:
    prefix = S3_EXPORT_PREFIX.strip("/")
    return f"{prefix}/{filename}" if prefix else filename


def _save_local(filename: str, payload: bytes) -> str:
    out_dir = ensure_export_dir()
    full_path = out_dir / filename
    full_path.write_bytes(payload)
    return str(full_path)


def _save_s3(filename: str, payload: bytes) -> str:
    key = _s3_key(filename)
    _s3_client().put_object(Bucket=S3_EXPORT_BUCKET, Key=key, Body=payload, ContentType="application/pdf")
    return f"s3://{S3_EXPORT_BUCKET}/{key}"


def _parse_s3_uri(uri: str) -> tuple[str, str]:
    rest = uri[5:]
    bucket, key = rest.split("/", 1)
    return bucket, key


def is_s3_uri(path_or_uri: str) -> bool:
    return path_or_uri.startswith("s3://")


def generate_resume_export_file(full_name: str, content: str, export_job_id: int) -> str:
    filename = f"resume_{export_job_id}_{_safe_name(full_name)}.pdf"
    pdf_bytes = _build_pdf_bytes(full_name, content)
    if _is_s3_enabled():
        return _save_s3(filename, pdf_bytes)
    return _save_local(filename, pdf_bytes)


def generate_download_target(path_or_uri: str) -> tuple[str, str]:
    """
    Returns tuple: (kind, value)
    - ('local', absolute_path)
    - ('redirect', signed_url)
    """
    if is_s3_uri(path_or_uri):
        bucket, key = _parse_s3_uri(path_or_uri)
        url = _s3_client().generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key, "ResponseContentType": "application/pdf"},
            ExpiresIn=EXPORT_SIGNED_URL_TTL_SECONDS,
        )
        return "redirect", url

    return "local", str(Path(path_or_uri))


def infer_filename(path_or_uri: str) -> str:
    if is_s3_uri(path_or_uri):
        _, key = _parse_s3_uri(path_or_uri)
        return quote(key.rsplit("/", 1)[-1])
    return Path(path_or_uri).name
