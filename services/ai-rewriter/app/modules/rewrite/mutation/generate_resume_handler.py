from ..dto.resume_prompt_dto import ResumeGenerateResponse, ResumePrompt


class GenerateResumeHandler:
    def execute(self, payload: ResumePrompt) -> dict:
        summary = payload.summary or (
            f"Motivated {payload.target_role} candidate with practical skills in {payload.skills_csv}."
        )
        exp = payload.experience_bullet or "Delivered high-impact projects with measurable outcomes."

        content = (
            f"{payload.full_name}\n"
            f"{payload.target_role} | {payload.city}\n\n"
            f"Template: {payload.template_name}\n\n"
            "Professional Summary\n"
            f"{summary}\n\n"
            "Experience\n"
            f"- {exp}\n\n"
            "Skills\n"
            f"{payload.skills_csv}\n"
        )

        return ResumeGenerateResponse(content=content).model_dump()
