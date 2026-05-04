from .ats import parse_skills

JOBS = [
    {"id": 1,  "title": "Software Engineer I",           "company": "Flipkart",      "location": "Bengaluru",  "type": "Full-time",    "skills": ["python", "react", "sql", "aws"]},
    {"id": 2,  "title": "Backend Developer",              "company": "Razorpay",      "location": "Remote",     "type": "Full-time",    "skills": ["python", "fastapi", "postgresql", "redis"]},
    {"id": 3,  "title": "Graduate Engineer Trainee",      "company": "TCS",           "location": "Hyderabad",  "type": "Full-time",    "skills": ["java", "sql", "communication", "git"]},
    {"id": 4,  "title": "Full Stack Developer",           "company": "Zoho",          "location": "Chennai",    "type": "Full-time",    "skills": ["javascript", "react", "node", "mysql"]},
    {"id": 5,  "title": "Associate Product Engineer",     "company": "Freshworks",    "location": "Chennai",    "type": "Full-time",    "skills": ["python", "api", "debugging", "aws"]},
    {"id": 6,  "title": "SDE Intern",                    "company": "Amazon",        "location": "Hyderabad",  "type": "Internship",   "skills": ["python", "java", "data structures", "algorithms"]},
    {"id": 7,  "title": "Data Analyst",                  "company": "Swiggy",        "location": "Bengaluru",  "type": "Full-time",    "skills": ["sql", "python", "excel", "tableau"]},
    {"id": 8,  "title": "DevOps Engineer",               "company": "Infosys",       "location": "Pune",       "type": "Full-time",    "skills": ["docker", "kubernetes", "aws", "linux", "ci/cd"]},
    {"id": 9,  "title": "React Developer",               "company": "Groww",         "location": "Remote",     "type": "Full-time",    "skills": ["react", "javascript", "typescript", "css"]},
    {"id": 10, "title": "ML Engineer Intern",            "company": "Google",        "location": "Hyderabad",  "type": "Internship",   "skills": ["python", "machine learning", "tensorflow", "numpy"]},
    {"id": 11, "title": "Systems Engineer",              "company": "Wipro",         "location": "Bengaluru",  "type": "Full-time",    "skills": ["java", "spring", "sql", "linux"]},
    {"id": 12, "title": "Product Analyst",               "company": "PhonePe",       "location": "Bengaluru",  "type": "Full-time",    "skills": ["sql", "analytics", "python", "excel"]},
    {"id": 13, "title": "Frontend Developer Intern",     "company": "Meesho",        "location": "Remote",     "type": "Internship",   "skills": ["html", "css", "javascript", "react"]},
    {"id": 14, "title": "Cloud Support Engineer",        "company": "AWS",           "location": "Hyderabad",  "type": "Full-time",    "skills": ["aws", "linux", "networking", "python"]},
    {"id": 15, "title": "Software Development Engineer", "company": "Microsoft",     "location": "Hyderabad",  "type": "Full-time",    "skills": ["c++", "algorithms", "system design", "python"]},
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
