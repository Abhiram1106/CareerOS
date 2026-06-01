"""Resume template renderer — rule-based, structured, no fabrication.

Generates a clean plain-text resume from profile fields. Uses only what
the student has actually provided; never invents content.

Placeholder guidance (e.g. "[Add a 2–3 sentence summary here]") is emitted
when a required field is empty so the student knows exactly what to fill in,
rather than receiving silent boilerplate.
"""

from __future__ import annotations

import re

from ..dto.resume_prompt_dto import ResumeGenerateResponse, ResumePrompt

_HORIZONTAL = "─" * 60


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _bullets(csv_or_prose: str) -> str:
    """Convert comma-separated or prose skills into a bullet list."""
    items = [i.strip() for i in csv_or_prose.split(",") if i.strip()]
    if not items:
        return csv_or_prose.strip()
    # Group into rows of 4 for readability
    rows = []
    for i in range(0, len(items), 4):
        rows.append("  " + "  |  ".join(items[i:i + 4]))
    return "\n".join(rows)


def _section(title: str, body: str) -> str:
    return f"\n{title}\n{_HORIZONTAL}\n{body}\n"


class GenerateResumeHandler:
    def execute(self, payload: ResumePrompt) -> dict:
        name = _clean(payload.full_name) or "[Full Name]"
        role = _clean(payload.target_role) or "Software Engineer"
        city = _clean(payload.city) or ""
        skills_csv = _clean(payload.skills_csv)
        summary = _clean(payload.summary)
        exp_bullet = _clean(payload.experience_bullet)

        # ── Contact header ────────────────────────────────────────────────
        contact_parts = [name]
        if role:
            contact_parts.append(role)
        if city:
            contact_parts.append(city)

        header = "\n".join(contact_parts)
        header += "\n[Add email | phone | linkedin | github]"

        # ── Summary ───────────────────────────────────────────────────────
        if summary:
            summary_body = summary
        else:
            summary_body = (
                f"[Write 2–3 sentences about your background and what you bring to {role} roles. "
                "Focus on your strongest technical skills and one standout achievement.]"
            )

        # ── Experience ────────────────────────────────────────────────────
        if exp_bullet:
            # Each sentence on its own bullet line
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", exp_bullet) if s.strip()]
            exp_body = "\n".join(f"• {s}" for s in sentences)
        else:
            exp_body = (
                "Company Name | Role Title | Month YYYY – Month YYYY\n"
                "• [Describe your most impactful contribution. Start with a strong action verb.]\n"
                "• [Quantify the outcome: 'reduced X by Y%' or 'served Z users'.]\n"
                "• [Add a third bullet if you have another distinct achievement.]"
            )

        # ── Skills ────────────────────────────────────────────────────────
        if skills_csv:
            skills_body = _bullets(skills_csv)
        else:
            skills_body = "[List your technical skills: languages, frameworks, tools, platforms]"

        # ── Education ────────────────────────────────────────────────────
        education_body = (
            "[Degree] | [Institution] | [City] | [Month YYYY – Month YYYY] | CGPA: [X.X/10]\n"
            "• Relevant coursework: [list 3–5 relevant courses]"
        )

        # ── Projects ─────────────────────────────────────────────────────
        projects_body = (
            "Project Name | [Tech stack used]\n"
            "• [What you built and why. Start with an action verb.]\n"
            "• [Impact or scale: 'served N users', 'reduced runtime by X%', 'deployed on AWS']."
        )

        # ── Template note ─────────────────────────────────────────────────
        template_note = (
            f"\n\n── Template: {payload.template_name} ──\n"
            "Replace all [bracketed placeholders] with your actual information.\n"
            "Delete any section you don't have content for.\n"
            "Export as PDF when complete."
        )

        content = (
            header
            + _section("PROFESSIONAL SUMMARY", summary_body)
            + _section("EXPERIENCE", exp_body)
            + _section("PROJECTS", projects_body)
            + _section("SKILLS", skills_body)
            + _section("EDUCATION", education_body)
            + template_note
        )

        return ResumeGenerateResponse(content=content).model_dump()
