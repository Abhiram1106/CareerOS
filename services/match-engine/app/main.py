from fastapi import FastAPI
from pydantic import BaseModel, Field

from .jd_parser import parse_jd
from .matcher import compute_match

app = FastAPI(title="CareerOS Match Engine", version="0.1.0")


class ParseJdRequest(BaseModel):
    jd_text: str = Field(min_length=20)


class MatchRequest(BaseModel):
    resume_text: str = Field(min_length=10)
    jd_text: str = Field(min_length=20)
    required_skills: list[str] = Field(default_factory=list)
    student_profile: dict | None = None


@app.get("/health")
def health():
    return {"status": "ok", "service": "match-engine"}


@app.post("/jd/parse")
def jd_parse(payload: ParseJdRequest):
    return parse_jd(payload.jd_text)


@app.post("/match")
def match(payload: MatchRequest):
    parsed = parse_jd(payload.jd_text) if not payload.required_skills else None
    required = payload.required_skills or (parsed or {}).get("required_skills", [])
    return compute_match(
        payload.resume_text,
        payload.jd_text,
        required,
        payload.student_profile,
    )
