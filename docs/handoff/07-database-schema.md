# 07 — Database Schema

Database: PostgreSQL 16. ORM: SQLAlchemy 2.0 mapped-column style.
All migrations in `services/core-api/migrations/versions/`.

---

## Tables

### users
Primary user account.
```
id (PK)          email (unique, index)    password_hash
full_name         role (student/admin)     phone
linkedin_url      github_url               portfolio_url
created_at
```

### session_tokens
JWT sessions (one per login).
```
id (PK)    token (unique, index)    user_id (FK→users)
is_active   created_at
```

### career_profiles
Basic profile fields. One per user.
```
id (PK)         user_id (unique FK→users)    city
professional_status    target_role              skills_csv
summary         experience_bullet            cgpa
active_backlogs  branch                       grad_year
updated_at
```
Note: `skills_csv` and `experience_bullet` are legacy flat text. New structured tables below.

### work_experiences *(migration 0003)*
```
id (PK)    user_id (FK→users, index)    company    title
employment_type    location    start_date    end_date
is_current    bullets (JSON array as Text)    sort_order
created_at    updated_at
```

### educations *(migration 0003)*
```
id (PK)    user_id (FK→users, index)    institution    degree    field
start_year    end_year    cgpa    percentage    coursework
sort_order    created_at    updated_at
```

### skills *(migration 0003)*
```
id (PK)    user_id (FK→users, index)
name    category (technical/soft/tool/language)
proficiency (beginner/intermediate/advanced/expert)
created_at
```

### projects *(migration 0003)*
```
id (PK)    user_id (FK→users, index)    title    description
tech_stack (JSON array as Text)    github_url    live_url
start_date    end_date    sort_order    created_at    updated_at
```

### certifications *(migration 0003)*
```
id (PK)    user_id (FK→users, index)    name    issuer
issue_date    expiry_date    credential_id    credential_url
sort_order    created_at
```

### job_applications *(migration 0003)*
```
id (PK)    user_id (FK→users, index)    job_external_id    job_title
company    apply_url    status    resume_id (FK→resumes, nullable)
notes    applied_at (nullable)    created_at    updated_at
```
Status enum: saved → applied → screening → interview → offer | rejected

### resumes
One row per uploaded or generated resume.
```
id (PK)    user_id (FK→users)    template_name    content_text
file_uri    source_format    created_at
```

### resume_sections
Parsed sections from resume-parser.
```
id (PK)    resume_id (FK→resumes, index)    section_name
content_json (Text)    confidence    created_at
```

### resume_evidence
Proof linkage for anti-fabrication (future use).
```
id (PK)    resume_id (FK)    claim_id    proof_uri
verified_by (FK→users)    status    created_at
```

### resume_export_jobs
Celery-backed PDF export tracking.
```
id (PK)    user_id (FK)    resume_id (FK)    status
file_path    error_message    created_at    updated_at
```

### job_descriptions
User-pasted JDs stored after parsing.
```
id (PK)    created_by (FK→users)    company    role
raw_text    skills_json    eligibility_json    created_at
```

### jobs
Job listings from Adzuna or seed data.
```
id (PK)    source    external_id (index)    title    company
location    skills_required (JSON)    raw_jd_text    fetched_at    expires_at
```

### scorecards
One per (resume, JD) scoring run.
```
id (PK)    resume_id (FK)    jd_id (FK)
jd_match    ats_safety    evidence_quality    profile_completeness
interview_readiness    placement_hygiene    overall_score    bucket
score_detail_json    created_at
```

### recommendations
Rewrite bundles per scorecard.
```
id (PK)    scorecard_id (FK)    rec_type    section
before_text    after_text    evidence_ids    confidence
accepted (nullable)    created_at
```

### agent_runs
Deterministic agent pipeline runs.
```
id (PK)    student_id (FK)    resume_id (FK)    job_id (FK, nullable)
scorecard_id (FK, nullable)    current_step    summary_json
status    started_at    finished_at
```

### ats_scans
ATS scan history.
```
id (PK)    user_id (FK)    composite_score    keyword_score
format_score    quality_score    completeness_score    contact_score
created_at
```

### events_audit
All significant actions logged here.
```
id (PK)    actor_id (FK)    action    target_type
target_id    payload_json    ts
```

### benchmark_runs
Intel performance measurements.
```
id (PK)    workload    dataset_size    baseline_ms    intel_ms
throughput_rph    accuracy_delta    memory_mb    hw_label    notes    created_at
```

---

## Migrations

| File | What it does |
|---|---|
| `0001_student_baseline.py` | Creates all original tables (users, resumes, scorecards, etc.) |
| `0002_profile_eligibility_fields.py` | Adds cgpa, active_backlogs, branch, grad_year to career_profiles |
| `0003_structured_profile.py` | Creates work_experiences, educations, skills, projects, certifications, job_applications + user social links |

To run all migrations from scratch:
```bash
docker compose exec core-api alembic upgrade head
```

To add a new migration:
1. Edit `entities.py`
2. Create `migrations/versions/000N_description.py`
3. Apply to running DB: `docker compose exec postgres psql -U careeros -d careeros -c "ALTER TABLE..."`
4. Also add to the migration file for reproducibility

---

## JSON fields

Several fields store JSON as Text (not JSONB) for simplicity:

| Table.Column | Content | Example |
|---|---|---|
| `work_experiences.bullets` | `["Built X", "Deployed Y"]` | Parsed with `json.loads()` |
| `projects.tech_stack` | `["Python","Docker"]` | Parsed with `json.loads()` |
| `scorecards.score_detail_json` | Full breakdown dict | Raw JSON blob |
| `resume_sections.content_json` | `{"raw": "...text..."}` | Parsed by `_section_text()` |
| `jobs.skills_required` | `["Python","SQL"]` | Parsed in job feed |
