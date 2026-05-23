"""Rule-based JD parsing — skills + eligibility (Week 2 baseline)."""

from __future__ import annotations

import re
from typing import Any

from .skill_taxonomy import extract_skills_from_text, parse_required_skills_block


def _parse_company_role(jd_text: str) -> tuple[str, str]:
    lines = [ln.strip() for ln in jd_text.splitlines() if ln.strip()]
    company = ""
    role = ""
    for line in lines[:8]:
        m = re.match(r"(?i)(company|employer|organization)\s*[:\-]\s*(.+)", line)
        if m:
            company = m.group(2).strip()
        m = re.match(r"(?i)(role|position|title|designation)\s*[:\-]\s*(.+)", line)
        if m:
            role = m.group(2).strip()
    if not role and lines:
        role = lines[0][:200]
    if not company:
        company = "Unknown"
    return company, role


def _parse_eligibility(jd_text: str) -> dict[str, Any]:
    low = jd_text.lower()
    eligibility: dict[str, Any] = {
        "min_cgpa": None,
        "max_backlogs": None,
        "allowed_branches": [],
        "graduation_years": [],
        "notes": [],
    }

    cgpa = re.search(r"(?i)(?:cgpa|gpa)\s*(?:>|>=|minimum|min\.?|at least)?\s*([0-9]+\.?[0-9]*)", jd_text)
    if cgpa:
        try:
            eligibility["min_cgpa"] = float(cgpa.group(1))
        except ValueError:
            pass

    backlog = re.search(r"(?i)(?:no|zero|0)\s+backlogs?", low)
    if backlog:
        eligibility["max_backlogs"] = 0
    else:
        bl = re.search(r"(?i)backlogs?\s*(?:<=|≤|<|maximum|max\.?)?\s*(\d+)", jd_text)
        if bl:
            eligibility["max_backlogs"] = int(bl.group(1))

    branches = re.findall(
        r"\b(CSE|CS|IT|ECE|EEE|ME|CE|AIML|AI\s*&?\s*ML|Computer Science|Information Technology)\b",
        jd_text,
        re.IGNORECASE,
    )
    eligibility["allowed_branches"] = sorted({b.upper().replace(" ", "") for b in branches})

    years = re.findall(r"\b(20\d{2})\s*(?:batch|graduat)", low)
    eligibility["graduation_years"] = sorted({int(y) for y in years})

    return eligibility


def parse_jd(jd_text: str) -> dict[str, Any]:
    company, role = _parse_company_role(jd_text)
    required = parse_required_skills_block(jd_text)
    all_skills = extract_skills_from_text(jd_text)
    optional = [s for s in all_skills if s not in required]

    return {
        "company": company,
        "role": role,
        "required_skills": required,
        "optional_skills": optional[:30],
        "all_skills": all_skills[:50],
        "eligibility": _parse_eligibility(jd_text),
    }
