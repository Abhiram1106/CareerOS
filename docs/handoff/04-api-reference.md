# 04 — API Reference

Base URL: `http://localhost:8000`
Auth: `Authorization: Bearer <jwt>` on all protected routes.
Full interactive docs: http://localhost:8000/docs

---

## Auth

| Method | Path | Auth | Notes |
|---|---|---|---|
| POST | `/auth/register` | No | `{email, password, full_name}` → `{token, email, full_name, role}` |
| POST | `/auth/login` | No | `{email, password}` → `{token, ...}` |
| POST | `/auth/logout` | Yes | Revokes session token |
| POST | `/auth/reset-request` | No | `{email}` → prints token to server logs |
| POST | `/auth/reset-confirm` | No | `{token, new_password}` → updates hash, revokes all sessions |

---

## Profile (basic)

| Method | Path | Notes |
|---|---|---|
| GET | `/profile` | Returns `{full_name, email, city, target_role, skills_csv, summary, experience_bullet, cgpa, active_backlogs, branch, grad_year}` |
| PUT | `/profile` | Updates all basic profile fields |
| PUT | `/profile/links` | `{phone, linkedin_url, github_url, portfolio_url}` |
| GET | `/profile/complete` | Returns full structured profile: user links + all sections in one call |

---

## Profile sections (structured — new)

All return the created/updated object. Delete returns 204.

### Work Experience
```
GET    /profile/work-experience                 → {work_experiences: [...]}
POST   /profile/work-experience                 → WorkExperience
PUT    /profile/work-experience/{id}            → WorkExperience
DELETE /profile/work-experience/{id}            → 204
```
Fields: `company, title, employment_type, location, start_date, end_date, is_current, bullets: string[]`

### Education
```
GET    /profile/education                       → {educations: [...]}
POST   /profile/education                       → Education
PUT    /profile/education/{id}                  → Education
DELETE /profile/education/{id}                  → 204
```
Fields: `institution, degree, field, start_year, end_year, cgpa, percentage, coursework`

### Skills
```
GET    /profile/skills                          → {skills: [...]}
POST   /profile/skills                          → Skill
POST   /profile/skills/bulk                     → {skills: [...]} (replaces all)
DELETE /profile/skills/{id}                     → 204
```
Fields: `name, category (technical/soft/tool/language), proficiency (beginner/intermediate/advanced/expert)`

### Projects
```
GET    /profile/projects                        → {projects: [...]}
POST   /profile/projects                        → Project
PUT    /profile/projects/{id}                   → Project
DELETE /profile/projects/{id}                   → 204
```
Fields: `title, description, tech_stack: string[], github_url, live_url, start_date, end_date`

### Certifications
```
GET    /profile/certifications                  → {certifications: [...]}
POST   /profile/certifications                  → Certification
PUT    /profile/certifications/{id}             → Certification
DELETE /profile/certifications/{id}             → 204
```
Fields: `name, issuer, issue_date, expiry_date, credential_id, credential_url`

---

## Resumes

| Method | Path | Notes |
|---|---|---|
| GET | `/resumes` | List user's resumes |
| POST | `/resumes/upload` | Multipart PDF/DOCX → `{resume_id, sections, ats_flags, char_count}` |
| GET | `/resumes/{id}/sections` | Parsed sections for a resume |
| POST | `/resumes/generate` | `{template_name}` → `{resume_id, content}` |
| POST | `/resumes/export` | `{resume_id}` → `{job_id, status}` |
| GET | `/resumes/export/{job_id}` | Poll export status |
| GET | `/resumes/export/{job_id}/download` | Download PDF blob |

---

## Scoring

| Method | Path | Notes |
|---|---|---|
| POST | `/jd/parse` | `{jd_text}` → `{jd_id, company, role, required_skills, optional_skills, eligibility}` |
| POST | `/scorecards/score` | `{resume_id, jd_text, jd_id?, ats_flags?}` → full scorecard |
| POST | `/ats/parse-safety` | `{resume_id, ats_flags}` → `{ats_parse_safety, bucket, checks, issues}` |
| GET | `/ats/scans` | User's ATS scan history |

**Scorecard response shape:**
```json
{
  "scorecard_id": 11,
  "overall_score": 62.4,
  "bucket": "borderline",
  "components": {"jd_match":22.1,"ats_safety":15.2,"evidence":12.0,"completeness":7.0,"interview":4.8,"hygiene":1.3},
  "raw": {"jd_match":63.1,"ats_parse_safety":76.0,...},
  "missing_required_skills": ["docker","sql"],
  "matched_skills": ["python","fastapi"],
  "semantic_method": "sentence_embedding",
  "ats_bucket": "fair",
  "ats_checks": [...],
  "ats_issues": [...]
}
```

---

## Recommendations / Rewrite

| Method | Path | Notes |
|---|---|---|
| POST | `/recommendations/rewrite` | `{scorecard_id}` → `{top_issues, section_rewrites, unsupported_claims, requires_confirmation}` |
| GET | `/recommendations/{scorecard_id}` | Fetch cached rewrite |

---

## Jobs

| Method | Path | Notes |
|---|---|---|
| GET | `/jobs/search?q=python&loc=India&page=1` | Returns paged job results with `source`, `results` |

---

## Job Applications (tracker)

| Method | Path | Notes |
|---|---|---|
| GET | `/applications` | List user's saved/tracked jobs |
| POST | `/applications` | `{job_external_id, job_title, company, apply_url}` → saved application |
| PUT | `/applications/{id}` | `{status, notes, resume_id}` — update status workflow |
| DELETE | `/applications/{id}` | 204 |

Status flow: `saved` → `applied` → `screening` → `interview` → `offer` | `rejected`
Setting status to `applied` auto-sets `applied_at` timestamp.

---

## Dashboard + Assistant

| Method | Path | Notes |
|---|---|---|
| GET | `/dashboard` | `{best_ats_score, total_resumes, scans_performed, profile_completeness}` |
| GET | `/ready` | `{status:"ready", database:"ok"}` — health check |
| POST | `/assistant/chat` | `{message}` → `{answer, sources, suggested_actions, provider}` |
| GET | `/benchmarks` | Intel performance measurements |

---

## Agent

| Method | Path | Notes |
|---|---|---|
| POST | `/agent/run` | `{resume_id, job_id?, jd_text?, job_query?}` → starts automated pipeline |
| GET | `/agent/runs/{run_id}` | Poll run status |
