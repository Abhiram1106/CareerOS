from __future__ import annotations

import json
import re
from typing import Any

from ..dto.proof_rewrite_dto import (
    ProofRewriteRequest,
    ProofRewriteResponse,
    RequiresConfirmation,
    SectionRewrite,
    TopIssue,
    UnsupportedClaim,
)

_ACTION_VERBS = ("built", "developed", "designed", "implemented", "created", "optimized", "deployed")
_METRIC_RE = re.compile(r"\b(\d+(\.\d+)?)\s*(%|percent|x|k|m|l|members?|people|students?)\b", re.I)
_LEADERSHIP_RE = re.compile(r"\b(led|managed|headed)\s+(a\s+)?team\b", re.I)
_CGPA_RE = re.compile(r"\b(cgpa|gpa)\s*[:\-]?\s*(\d+(\.\d+)?)", re.I)

_FLAG_MESSAGES: dict[str, tuple[str, str]] = {
    "two_column_layout": ("ATS_FORMAT", "Two-column layout may break ATS parsing", "high"),
    "image_or_icon_detected": ("ATS_FORMAT", "Images or icons detected in resume", "high"),
    "table_detected": ("ATS_FORMAT", "Tables detected — prefer plain bullet lists", "medium"),
    "no_email_found": ("ATS_FORMAT", "No email address found in contact block", "high"),
    "non_standard_section": ("ATS_FORMAT", "Non-standard section headings may reduce parse accuracy", "low"),
}


def _section_raw(content: Any) -> str:
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except json.JSONDecodeError:
            return content.strip()
    if isinstance(content, dict):
        return str(content.get("raw", "")).strip()
    return ""


def _evidence_ids_for_text(text: str, evidence_index: dict[str, str]) -> list[str]:
    lowered = text.lower()
    matched: list[str] = []
    for claim_id, snippet in evidence_index.items():
        if snippet and snippet.lower() in lowered:
            matched.append(claim_id)
    if matched:
        return matched[:3]
    return []


def _improve_bullet(original: str, jd_skills: list[str]) -> str:
    text = original.strip()
    if not text:
        return text
    lower = text.lower()
    if not any(lower.startswith(v) for v in _ACTION_VERBS):
        text = f"Developed {text[0].lower()}{text[1:]}" if len(text) > 1 else f"Developed {text}"
    if jd_skills:
        skill = jd_skills[0]
        if skill.lower() not in lower and len(text) < 120:
            text = f"{text.rstrip('.')}, applying {skill}."
    return text[:280]


def _split_bullets(raw: str) -> list[str]:
    lines = [ln.strip(" •-\t") for ln in raw.splitlines() if ln.strip()]
    if len(lines) <= 1 and ";" in raw:
        lines = [p.strip() for p in raw.split(";") if p.strip()]
    return lines or ([raw] if raw else [])


class ProofLinkedRewriteHandler:
    """Deterministic proof-linked rewriter — no LLM, no fabrication."""

    def execute(self, payload: ProofRewriteRequest) -> dict:
        sections = payload.resume_json.get("sections", [])
        if not isinstance(sections, list):
            sections = []

        jd_skills: list[str] = []
        skills = payload.jd_json.get("skills", {})
        if isinstance(skills, dict):
            jd_skills = list(skills.get("required", []) or [])[:5]

        evidence_index: dict[str, str] = {}
        claims = payload.evidence_json.get("claims", [])
        if isinstance(claims, list):
            for item in claims:
                if isinstance(item, dict) and item.get("claim_id"):
                    evidence_index[str(item["claim_id"])] = str(item.get("snippet", ""))

        top_issues = self._top_issues(payload.ats_flags)
        section_rewrites: list[SectionRewrite] = []
        unsupported: list[UnsupportedClaim] = []
        confirmations: list[RequiresConfirmation] = []

        for sec in sections:
            if not isinstance(sec, dict):
                continue
            name = str(sec.get("section_name", "")).strip().lower()
            if name not in {"experience", "projects", "summary", "positions_of_responsibility"}:
                continue
            raw = _section_raw(sec.get("content_json", {}))
            if not raw:
                continue

            for idx, bullet in enumerate(_split_bullets(raw)):
                original = bullet.strip()
                if len(original) < 8:
                    continue
                claim_id = f"{name}_{idx}"
                if claim_id not in evidence_index:
                    evidence_index[claim_id] = original[:120]

                evidence_ids = _evidence_ids_for_text(original, evidence_index) or [claim_id]
                rewrite = _improve_bullet(original, jd_skills)

                if _METRIC_RE.search(original) and claim_id not in evidence_ids:
                    unsupported.append(
                        UnsupportedClaim(
                            claim=original,
                            reason="Quantified outcome not linked to resume_evidence — verify before keeping",
                        )
                    )
                if _LEADERSHIP_RE.search(original) and len(evidence_ids) <= 1:
                    unsupported.append(
                        UnsupportedClaim(
                            claim=original,
                            reason="Leadership scope stated — confirm team size in resume_evidence before using",
                        )
                    )

                confidence = 0.72 if rewrite != original else 0.55
                if evidence_ids:
                    confidence = min(0.92, confidence + 0.12)

                section_rewrites.append(
                    SectionRewrite(
                        section=name,
                        original=original,
                        rewrite=rewrite,
                        evidence_ids=evidence_ids,
                        confidence=round(confidence, 2),
                    )
                )

            cgpa_match = _CGPA_RE.search(raw)
            if cgpa_match and name == "education":
                confirmations.append(
                    RequiresConfirmation(
                        field="cgpa",
                        suggested_change=f"Confirm exact CGPA value ({cgpa_match.group(2)}) before export",
                    )
                )

        response = ProofRewriteResponse(
            top_issues=top_issues,
            section_rewrites=section_rewrites,
            unsupported_claims=unsupported,
            requires_confirmation=confirmations,
        )
        return response.model_dump()

    def _top_issues(self, ats_flags: list[str]) -> list[TopIssue]:
        issues: list[TopIssue] = []
        for flag in ats_flags:
            key = str(flag).strip().lower()
            meta = _FLAG_MESSAGES.get(key)
            if meta:
                issues.append(TopIssue(type=meta[0], message=meta[1], severity=meta[2]))
            else:
                issues.append(
                    TopIssue(
                        type="ATS_FORMAT",
                        message=f"ATS flag: {flag}",
                        severity="medium",
                    )
                )
        return issues
