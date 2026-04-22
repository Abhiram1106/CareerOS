from .ats import parse_skills

JOBS = [
    {"id": 1, "title": "Software Engineer I", "company": "Flipkart", "location": "Bengaluru", "skills": ["python", "react", "sql", "aws"]},
    {"id": 2, "title": "Backend Developer", "company": "Razorpay", "location": "Remote", "skills": ["python", "fastapi", "postgresql", "redis"]},
    {"id": 3, "title": "Graduate Engineer Trainee", "company": "TCS", "location": "Hyderabad", "skills": ["java", "sql", "communication", "git"]},
    {"id": 4, "title": "Full Stack Developer", "company": "Zoho", "location": "Chennai", "skills": ["javascript", "react", "node", "mysql"]},
    {"id": 5, "title": "Associate Product Engineer", "company": "Freshworks", "location": "Chennai", "skills": ["python", "api", "debugging", "aws"]},
]


def compute_matches(profile: dict) -> list[dict]:
    user_skills = set(parse_skills(profile.get("skills_csv", "")))
    role = (profile.get("target_role") or "").lower()

    scored = []
    for job in JOBS:
        skill_overlap = len(user_skills.intersection(set(job["skills"])))
        role_bonus = 12 if role and any(token in job["title"].lower() for token in role.split()) else 0
        score = min(98, 50 + skill_overlap * 10 + role_bonus)
        scored.append({**job, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored
