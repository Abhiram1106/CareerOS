# CareerOS — MVP v0.1

> AI-powered career intelligence platform. ATS resume scoring, job matching, and analytics — all in one.

## Quick Start

```bash
cd backend/legacy/v0-prototype-monolith
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000**

## Demo Flow

1. **Register** — create an account with name / email / password
2. **Career Profile** — fill city, status, target role, skills → Save Profile
3. **Resume Builder** — click "Autofill Sample" → Generate Resume → see live preview
4. **ATS Scanner** — paste any job description → Run ATS Scan → see 6 scores + actionable suggestions
5. **Job Matches** — click Refresh → see 15 ranked job listings with match %
6. **Analytics** — click Refresh → see all career health metrics

## What's Working

| Module | Status | Details |
|--------|--------|---------|
| Auth (Register / Login) | ✅ | Token-based sessions, SQLite persistence |
| Career Profile | ✅ | 6-field persistent career profile |
| Resume Builder | ✅ | 3 templates, live preview, backend save |
| ATS Scanner | ✅ | 6-dimension scoring + actionable suggestions + missing keywords |
| Job Matching | ✅ | 15 curated listings, skill-match ranked |
| Analytics Dashboard | ✅ | 6 live metrics, profile completeness bar |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, FastAPI, SQLAlchemy |
| Database | SQLite (careeros_dev.db) |
| Frontend | Vanilla HTML / CSS / JS (no build step) |
| Auth | Bearer token sessions |

## ATS Scoring Model

The ATS engine scores resumes across 6 dimensions:

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Keyword Match | 30% | Overlap between resume tokens and JD tokens |
| Format Quality | 20% | ATS-safe structure (simulated) |
| Content Quality | 20% | Action verbs + quantified achievements |
| Completeness | 15% | All profile fields filled |
| Contact Info | 15% | Email presence |
