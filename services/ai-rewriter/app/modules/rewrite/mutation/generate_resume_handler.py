"""Resume template renderer — reads structured career profile sections.

Generates clean, ATS-safe plain-text resumes from structured data.
Three templates:
  - classic     Single-column, maximum ATS compatibility
  - technical   Developer-focused: GitHub prominent, tech stack detail
  - fresher     Education-first, projects before experience

Never fabricates. Uses only what the student has actually provided.
[Bracketed placeholders] guide students to fill in missing content.
"""

from __future__ import annotations

import json
import re
from typing import Any

from ..dto.resume_prompt_dto import ResumeGenerateResponse, ResumeStructuredPrompt

_HR = "─" * 60
_HR_THIN = "·" * 60


def _c(text: str) -> str:
    """Clean whitespace."""
    return re.sub(r"\s+", " ", (text or "")).strip()


def _section(title: str, body: str, thin: bool = False) -> str:
    sep = _HR_THIN if thin else _HR
    return f"\n{title.upper()}\n{sep}\n{body.strip()}\n"


def _parse_list(raw: str) -> list[str]:
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return [str(i) for i in parsed if i]
    except (json.JSONDecodeError, TypeError):
        pass
    return [i.strip() for i in raw.split(",") if i.strip()]


# ── Contact header ────────────────────────────────────────────────────────────

def _contact_header(user: dict[str, Any], profile: dict[str, Any]) -> str:
    name = _c(user.get("full_name", "")) or "[Full Name]"
    role = _c(profile.get("target_role", "")) or "Software Engineer"
    city = _c(profile.get("city", ""))
    phone = _c(user.get("phone", ""))
    email = _c(user.get("email", ""))
    linkedin = _c(user.get("linkedin_url", ""))
    github = _c(user.get("github_url", ""))

    lines = [name, role]
    contacts = [x for x in [email, phone, city] if x]
    if contacts:
        lines.append("  ·  ".join(contacts))
    links = [x for x in [linkedin, github] if x]
    if links:
        lines.append("  ·  ".join(links))
    if not contacts and not links:
        lines.append("[email  ·  phone  ·  LinkedIn  ·  GitHub]")
    return "\n".join(lines)


def _contact_header_technical(user: dict[str, Any], profile: dict[str, Any]) -> str:
    """Technical template puts GitHub first."""
    name = _c(user.get("full_name", "")) or "[Full Name]"
    role = _c(profile.get("target_role", "")) or "Software Engineer"
    email = _c(user.get("email", ""))
    phone = _c(user.get("phone", ""))
    github = _c(user.get("github_url", ""))
    linkedin = _c(user.get("linkedin_url", ""))
    city = _c(profile.get("city", ""))

    contacts = [x for x in [github, email, phone, linkedin, city] if x]
    contact_line = "  |  ".join(contacts) if contacts else "[GitHub  |  Email  |  LinkedIn  |  City]"
    return f"{name}\n{role}\n{contact_line}"


# ── Work Experience ───────────────────────────────────────────────────────────

def _render_experiences(work_experiences: list[dict[str, Any]]) -> str:
    if not work_experiences:
        return (
            "[Company Name]  |  [Role Title]  |  [Start]–[End]\n"
            "• [Describe your most impactful contribution. Start with a strong action verb.]\n"
            "• [Quantify: 'reduced latency by 40%' / 'served 2M users'.]\n"
            "• [Add a third bullet for another achievement.]"
        )
    parts: list[str] = []
    for w in work_experiences:
        company = _c(w.get("company", ""))
        title = _c(w.get("title", ""))
        emp_type = _c(w.get("employment_type", ""))
        location = _c(w.get("location", ""))
        start = _c(w.get("start_date", ""))
        end = _c(w.get("end_date", "")) or ("Present" if w.get("is_current") else "")
        bullets_raw = w.get("bullets", "[]")
        bullets = _parse_list(bullets_raw) if isinstance(bullets_raw, str) else (bullets_raw or [])
        bullets = [b for b in bullets if b.strip()]

        meta_parts = [f"{company}"]
        if location:
            meta_parts.append(location)
        date_str = f"{start}–{end}" if end else start
        header_line = f"{title}  |  {'  |  '.join(meta_parts)}  |  {date_str}"
        if emp_type and emp_type.lower() not in ("full-time",):
            header_line += f"  ({emp_type})"

        bullet_lines = "\n".join(f"• {b}" for b in bullets) if bullets else "• [Add achievement bullets]"
        parts.append(f"{header_line}\n{bullet_lines}")

    return "\n\n".join(parts)


# ── Education ─────────────────────────────────────────────────────────────────

def _render_education(educations: list[dict[str, Any]]) -> str:
    if not educations:
        return (
            "[Degree]  |  [Institution]  |  [Start]–[End]  |  CGPA: [X.X/10]\n"
            "Relevant coursework: [Course 1, Course 2, Course 3]"
        )
    parts: list[str] = []
    for e in educations:
        inst = _c(e.get("institution", ""))
        deg = _c(e.get("degree", ""))
        field = _c(e.get("field", ""))
        sy = e.get("start_year", "")
        ey = e.get("end_year", "")
        cgpa = e.get("cgpa")
        pct = e.get("percentage")
        coursework = _c(e.get("coursework", ""))

        date_str = f"{sy}–{ey}" if sy and ey else (str(ey or sy or ""))
        grade = f"CGPA: {cgpa}/10" if cgpa else (f"{pct}%" if pct else "")
        header = f"{deg} in {field}  |  {inst}  |  {date_str}"
        if grade:
            header += f"  |  {grade}"

        body = header
        if coursework:
            body += f"\nRelevant coursework: {coursework}"
        parts.append(body)
    return "\n\n".join(parts)


# ── Skills ────────────────────────────────────────────────────────────────────

def _render_skills(skills: list[dict[str, Any]], profile: dict[str, Any]) -> str:
    if skills:
        by_cat: dict[str, list[str]] = {}
        for s in skills:
            cat = s.get("category", "technical").capitalize()
            by_cat.setdefault(cat, []).append(_c(s.get("name", "")))
        lines = []
        for cat, names in by_cat.items():
            lines.append(f"{cat}: {', '.join(names)}")
        return "\n".join(lines)

    # Fallback to skills_csv
    csv = _c(profile.get("skills_csv", ""))
    if csv:
        items = [i.strip() for i in csv.split(",") if i.strip()]
        return f"Technical: {', '.join(items)}"

    return "[Languages: Python, Java  ·  Frameworks: Django, React  ·  Tools: Docker, Git]"


def _render_skills_inline(skills: list[dict[str, Any]], profile: dict[str, Any]) -> str:
    """Compact one-liner for technical template."""
    if skills:
        names = [_c(s.get("name", "")) for s in skills if s.get("name")]
        return ", ".join(names)
    csv = _c(profile.get("skills_csv", ""))
    return csv or "[Python, Docker, SQL, React, Git]"


# ── Projects ──────────────────────────────────────────────────────────────────

def _render_projects(projects: list[dict[str, Any]]) -> str:
    if not projects:
        return (
            "[Project Name]  |  [Tech Stack]\n"
            "• [What you built and why — start with an action verb.]\n"
            "• [Impact: 'handled 10k req/s', 'reduced runtime by 40%']."
        )
    parts: list[str] = []
    for p in projects:
        title = _c(p.get("title", ""))
        desc = _c(p.get("description", ""))
        tech_raw = p.get("tech_stack", "[]")
        tech = _parse_list(tech_raw) if isinstance(tech_raw, str) else (tech_raw or [])
        github = _c(p.get("github_url", ""))
        live = _c(p.get("live_url", ""))

        tech_str = ", ".join(tech) if tech else ""
        header = f"{title}" + (f"  |  {tech_str}" if tech_str else "")
        if github:
            header += f"  |  {github}"
        if live:
            header += f"  |  {live}"
        body = header
        if desc:
            # Split description into bullet points if it's long
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", desc) if s.strip()]
            if len(sentences) > 1:
                body += "\n" + "\n".join(f"• {s}" for s in sentences)
            else:
                body += f"\n• {desc}"
        parts.append(body)
    return "\n\n".join(parts)


# ── Certifications ────────────────────────────────────────────────────────────

def _render_certifications(certifications: list[dict[str, Any]]) -> str:
    if not certifications:
        return ""
    parts: list[str] = []
    for c in certifications:
        name = _c(c.get("name", ""))
        issuer = _c(c.get("issuer", ""))
        date = _c(c.get("issue_date", ""))
        url = _c(c.get("credential_url", ""))
        line = f"{name}  |  {issuer}"
        if date:
            line += f"  |  {date}"
        if url:
            line += f"  |  {url}"
        parts.append(line)
    return "\n".join(parts)


# ── Templates ─────────────────────────────────────────────────────────────────

def _template_classic(data: dict[str, Any]) -> str:
    """Single-column, maximum ATS compatibility. Best for bulk applications."""
    user = data.get("user", {})
    profile = data.get("profile", {})
    work = data.get("work_experiences", [])
    edu = data.get("educations", [])
    skills = data.get("skills", [])
    projects = data.get("projects", [])
    certs = data.get("certifications", [])
    summary = _c(profile.get("summary", ""))

    cert_section = _render_certifications(certs)

    parts = [
        _contact_header(user, profile),
    ]
    if summary:
        parts.append(_section("Professional Summary", summary))
    parts.append(_section("Education", _render_education(edu)))
    if work:
        parts.append(_section("Work Experience", _render_experiences(work)))
    parts.append(_section("Projects", _render_projects(projects)))
    parts.append(_section("Skills", _render_skills(skills, profile)))
    if cert_section:
        parts.append(_section("Certifications", cert_section))
    return "\n".join(parts)


def _template_technical(data: dict[str, Any]) -> str:
    """Developer-focused: skills prominent, GitHub front-and-center."""
    user = data.get("user", {})
    profile = data.get("profile", {})
    work = data.get("work_experiences", [])
    edu = data.get("educations", [])
    skills = data.get("skills", [])
    projects = data.get("projects", [])
    certs = data.get("certifications", [])
    summary = _c(profile.get("summary", ""))

    cert_section = _render_certifications(certs)

    parts = [
        _contact_header_technical(user, profile),
        _section("Technical Skills", _render_skills(skills, profile)),
    ]
    if summary:
        parts.append(_section("Summary", summary))
    if work:
        parts.append(_section("Experience", _render_experiences(work)))
    parts.append(_section("Projects", _render_projects(projects)))
    parts.append(_section("Education", _render_education(edu)))
    if cert_section:
        parts.append(_section("Certifications & Courses", cert_section, thin=True))
    return "\n".join(parts)


def _template_fresher(data: dict[str, Any]) -> str:
    """Fresher-optimised: education first, projects over experience."""
    user = data.get("user", {})
    profile = data.get("profile", {})
    work = data.get("work_experiences", [])
    edu = data.get("educations", [])
    skills = data.get("skills", [])
    projects = data.get("projects", [])
    certs = data.get("certifications", [])
    summary = _c(profile.get("summary", ""))

    cert_section = _render_certifications(certs)

    parts = [_contact_header(user, profile)]
    if summary:
        parts.append(_section("Objective", summary))
    parts.append(_section("Education", _render_education(edu)))
    parts.append(_section("Projects", _render_projects(projects)))
    if work:
        parts.append(_section("Internships & Experience", _render_experiences(work)))
    parts.append(_section("Technical Skills", _render_skills(skills, profile)))
    if cert_section:
        parts.append(_section("Certifications", cert_section, thin=True))
    return "\n".join(parts)


_RENDERERS = {
    "classic": _template_classic,
    "technical": _template_technical,
    "fresher": _template_fresher,
}


class GenerateResumeHandler:
    """Renders a resume from structured profile data using the chosen template."""

    def execute(self, payload: ResumeStructuredPrompt) -> dict:
        data = payload.profile_data
        template = (payload.template_name or "classic").lower()
        renderer = _RENDERERS.get(template, _template_classic)
        content = renderer(data)
        return ResumeGenerateResponse(content=content).model_dump()
