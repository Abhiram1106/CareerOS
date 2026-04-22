from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CareerOS AI Inference", version="0.1.0")


class ResumePrompt(BaseModel):
    full_name: str
    target_role: str
    city: str
    skills_csv: str
    summary: str
    experience_bullet: str
    template_name: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate/resume")
def generate_resume(payload: ResumePrompt):
    summary = payload.summary or f"Motivated {payload.target_role} candidate with practical skills in {payload.skills_csv}."
    exp = payload.experience_bullet or "Delivered high-impact projects with measurable outcomes."

    content = (
        f"{payload.full_name}\\n"
        f"{payload.target_role} | {payload.city}\\n\\n"
        f"Template: {payload.template_name}\\n\\n"
        "Professional Summary\\n"
        f"{summary}\\n\\n"
        "Experience\\n"
        f"- {exp}\\n\\n"
        "Skills\\n"
        f"{payload.skills_csv}\\n"
    )

    return {"content": content}
