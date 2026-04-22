from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CareerOS Job Intelligence", version="0.1.0")

JOBS = [
    {"id": 1, "title": "Software Engineer I", "company": "Flipkart", "location": "Bengaluru", "skills": ["python", "react", "sql", "aws"]},
    {"id": 2, "title": "Backend Developer", "company": "Razorpay", "location": "Remote", "skills": ["python", "fastapi", "postgresql", "redis"]},
    {"id": 3, "title": "Graduate Engineer Trainee", "company": "TCS", "location": "Hyderabad", "skills": ["java", "sql", "communication", "git"]},
    {"id": 4, "title": "Full Stack Developer", "company": "Zoho", "location": "Chennai", "skills": ["javascript", "react", "node", "mysql"]},
]


class MatchRequest(BaseModel):
    target_role: str
    skills_csv: str
    city: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/matches")
def matches(payload: MatchRequest):
    user_skills = {s.strip().lower() for s in payload.skills_csv.split(",") if s.strip()}
    role_tokens = set(payload.target_role.lower().split())

    scored = []
    for job in JOBS:
        overlap = len(user_skills.intersection(set(job["skills"])))
        role_bonus = 10 if role_tokens.intersection(set(job["title"].lower().split())) else 0
        city_bonus = 8 if payload.city and payload.city.lower() in job["location"].lower() else (6 if job["location"].lower() == "remote" else 0)
        score = min(98, 45 + overlap * 12 + role_bonus + city_bonus)
        scored.append({**job, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return {"jobs": scored}
