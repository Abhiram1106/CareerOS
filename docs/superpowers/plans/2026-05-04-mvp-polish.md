# CareerOS MVP Polish — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform the v0 monolith into a polished, demo-ready MVP for a college project review in 2 hours.

**Architecture:** Keep the existing FastAPI monolith backend unchanged except for (1) adding ATS suggestions to the scan response and (2) expanding the jobs list. Replace the vanilla HTML frontend with a fully redesigned single-file SPA that looks modern and professional, backed by the same API.

**Tech Stack:** Python 3.11+, FastAPI, SQLAlchemy, SQLite — existing stack. Frontend: vanilla HTML/CSS/JS (no build step, served by FastAPI static mount).

---

### Task 1: Enhance ATS engine — add suggestions output

**Files:**
- Modify: `backend/legacy/v0-prototype-monolith/app/services/ats.py`

- [ ] Replace the entire `ats.py` with this enhanced version that returns suggestions alongside scores:

```python
import re


def parse_skills(skills_csv: str) -> list[str]:
    return [s.strip().lower() for s in skills_csv.split(",") if s.strip()]


def ats_scan(profile: dict, jd_text: str) -> dict:
    jd = jd_text.lower()
    skills = parse_skills(profile.get("skills_csv", ""))
    summary = (profile.get("summary") or "").lower()
    exp = (profile.get("experience_bullet") or "").lower()

    # Keyword match
    jd_tokens = set(re.findall(r"[a-zA-Z0-9\+#\.]{3,}", jd))
    resume_tokens = set(re.findall(r"[a-zA-Z0-9\+#\.]{3,}", f"{' '.join(skills)} {summary} {exp}"))
    overlap = jd_tokens.intersection(resume_tokens)
    missing_keywords = list(jd_tokens - resume_tokens)[:8]
    keyword_score = min(95, max(20, len(overlap) * 4))

    # Format score
    format_score = 82

    # Quality score
    action_verbs = ["built", "developed", "designed", "improved", "led", "optimized", "deployed", "created", "managed", "reduced"]
    action_hits = sum(1 for v in action_verbs if v in exp)
    metric_hits = len(re.findall(r"\b\d+(%|x|k|m)?\b", exp))
    quality_score = min(95, 55 + action_hits * 5 + metric_hits * 6)

    # Completeness
    required_fields = [
        profile.get("full_name"),
        profile.get("city"),
        profile.get("target_role"),
        profile.get("skills_csv"),
        profile.get("summary"),
        profile.get("experience_bullet"),
    ]
    completeness_score = round(100 * sum(1 for f in required_fields if f) / len(required_fields))

    # Contact
    contact_score = 95 if profile.get("email") else 50

    composite = round(
        keyword_score * 0.30
        + format_score * 0.20
        + quality_score * 0.20
        + completeness_score * 0.15
        + contact_score * 0.15,
        1,
    )

    # Build suggestions
    suggestions = []
    if keyword_score < 70:
        kw_sample = ", ".join(missing_keywords[:5])
        suggestions.append(f"Add missing keywords from the JD: {kw_sample}")
    if quality_score < 75:
        suggestions.append("Use strong action verbs: built, optimized, deployed, led, reduced")
    if metric_hits == 0:
        suggestions.append("Quantify your achievements — e.g. 'reduced load time by 40%' or 'served 10k users'")
    if action_hits == 0:
        suggestions.append("Start each bullet with an action verb (Built, Designed, Improved, Deployed)")
    if completeness_score < 100:
        suggestions.append("Complete your profile — missing fields lower your ATS completeness score")
    if contact_score < 90:
        suggestions.append("Ensure your contact email is present in your profile")
    if not suggestions:
        suggestions.append("Strong resume! Tailor keywords per JD for each application.")

    return {
        "composite": composite,
        "keyword": round(keyword_score, 1),
        "format": round(format_score, 1),
        "quality": round(quality_score, 1),
        "complete": round(completeness_score, 1),
        "contact": round(contact_score, 1),
        "suggestions": suggestions,
        "missing_keywords": missing_keywords[:6],
    }
```

- [ ] Verify the file saved correctly:
```
cat backend/legacy/v0-prototype-monolith/app/services/ats.py
```

---

### Task 2: Expand job listings

**Files:**
- Modify: `backend/legacy/v0-prototype-monolith/app/services/jobs.py`

- [ ] Replace `jobs.py` with an expanded, realistic job list:

```python
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
```

---

### Task 3: Add suggestions field to ATS scan response stored in DB (main.py)

**Files:**
- Modify: `backend/legacy/v0-prototype-monolith/app/main.py`

- [ ] The `/api/ats/scan` endpoint already stores scores and returns the full result dict — `suggestions` and `missing_keywords` will now flow through automatically since `ats_scan()` returns them. No change needed to main.py. Verify by checking the return statement:

```python
# In main.py scan() — this line already returns the full result including new fields:
return result
```

- [ ] Also update the `/api/jobs/matches` response to include job `type` field — it already passes through since we do `{**job, "score": score}` in jobs.py. No change needed.

---

### Task 4: Build the new polished frontend

**Files:**
- Modify: `backend/legacy/v0-prototype-monolith/app/static/index.html`
- Modify: `backend/legacy/v0-prototype-monolith/app/static/styles.css`
- Modify: `backend/legacy/v0-prototype-monolith/app/static/app.js`

- [ ] Replace `index.html` with this complete redesigned version:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CareerOS — AI Career Intelligence</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/static/styles.css" />
</head>
<body>
  <div class="app">
    <!-- Sidebar -->
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-brand">
        <div class="brand-icon">C</div>
        <div>
          <div class="brand-name">CareerOS</div>
          <div class="brand-tag">AI Career Intelligence</div>
        </div>
      </div>

      <nav class="sidebar-nav">
        <button class="nav-item active" data-screen="onboarding">
          <span class="nav-icon">👤</span>
          <span>Profile</span>
        </button>
        <button class="nav-item" data-screen="resume">
          <span class="nav-icon">📄</span>
          <span>Resume Builder</span>
        </button>
        <button class="nav-item" data-screen="ats">
          <span class="nav-icon">🎯</span>
          <span>ATS Scanner</span>
        </button>
        <button class="nav-item" data-screen="jobs">
          <span class="nav-icon">💼</span>
          <span>Job Matches</span>
        </button>
        <button class="nav-item" data-screen="dashboard">
          <span class="nav-icon">📊</span>
          <span>Analytics</span>
        </button>
      </nav>

      <div class="sidebar-footer">
        <div class="auth-badge" id="authBadge">
          <div class="auth-dot offline"></div>
          <span id="authState">Not signed in</span>
        </div>
      </div>
    </aside>

    <!-- Main -->
    <main class="main">

      <!-- PROFILE SCREEN -->
      <section class="screen active" id="onboarding">
        <div class="page-header">
          <div>
            <h1>Career Profile</h1>
            <p class="page-sub">Your profile powers every module — fill it once.</p>
          </div>
          <div id="statusText" class="status-pill">Ready</div>
        </div>

        <div class="card-grid two">
          <div class="card">
            <div class="card-title">Account</div>
            <div class="form-group">
              <label>Full Name</label>
              <input id="nameInput" type="text" placeholder="Arjun Mehta">
            </div>
            <div class="form-group">
              <label>Email</label>
              <input id="emailInput" type="email" placeholder="arjun@example.com">
            </div>
            <div class="form-group">
              <label>Password</label>
              <input id="passwordInput" type="password" placeholder="min 6 characters">
            </div>
            <div class="btn-row">
              <button class="btn-primary" id="registerBtn">Register</button>
              <button class="btn-ghost" id="loginBtn">Login</button>
            </div>
          </div>

          <div class="card">
            <div class="card-title">Career Details</div>
            <div class="form-group">
              <label>City</label>
              <input id="cityInput" type="text" placeholder="Hyderabad">
            </div>
            <div class="form-group">
              <label>Status</label>
              <select id="statusInput">
                <option>Student</option>
                <option>Fresher</option>
                <option>Experienced</option>
                <option>Career Break</option>
              </select>
            </div>
            <div class="form-group">
              <label>Target Role</label>
              <input id="roleInput" type="text" placeholder="Software Engineer">
            </div>
            <div class="form-group">
              <label>Skills <span class="hint">(comma-separated)</span></label>
              <textarea id="skillsInput" rows="3" placeholder="Python, React, SQL, AWS, Git"></textarea>
            </div>
            <button class="btn-primary" id="saveProfileBtn">Save Profile</button>
          </div>
        </div>
      </section>

      <!-- RESUME SCREEN -->
      <section class="screen" id="resume">
        <div class="page-header">
          <div>
            <h1>Resume Builder</h1>
            <p class="page-sub">AI-guided, ATS-optimized resume generation.</p>
          </div>
        </div>

        <div class="card-grid two">
          <div class="card">
            <div class="card-title">Content</div>
            <div class="form-group">
              <label>Professional Summary</label>
              <textarea id="summaryInput" rows="5" placeholder="Results-driven software engineer with expertise in building scalable web applications..."></textarea>
            </div>
            <div class="form-group">
              <label>Experience Highlight</label>
              <textarea id="expInput" rows="5" placeholder="Built and deployed a REST API serving 10,000 users; reduced latency by 35%..."></textarea>
            </div>
            <div class="form-group">
              <label>Template</label>
              <select id="templateSelect">
                <option value="classic">Classic ATS</option>
                <option value="tech">Technical Focus</option>
                <option value="fresher">Fresher First</option>
              </select>
            </div>
            <div class="btn-row">
              <button class="btn-ghost" id="autofillBtn">✨ Autofill Sample</button>
              <button class="btn-ghost" id="saveProfileFromResumeBtn">💾 Save to Profile</button>
              <button class="btn-primary" id="generateResumeBtn">Generate Resume</button>
            </div>
          </div>

          <div class="card resume-preview">
            <div class="card-title">Preview</div>
            <div class="resume-doc">
              <div class="resume-header-block">
                <h2 id="pvName">Your Name</h2>
                <p id="pvRole" class="resume-role">Target Role</p>
              </div>
              <div class="resume-section">
                <div class="resume-section-title">Summary</div>
                <p id="pvSummary">Your professional summary will appear here.</p>
              </div>
              <div class="resume-section">
                <div class="resume-section-title">Experience</div>
                <ul><li id="pvExp">Your experience bullet will appear here.</li></ul>
              </div>
              <div class="resume-section">
                <div class="resume-section-title">Skills</div>
                <p id="pvSkills">Your skills will appear here.</p>
              </div>
            </div>
            <div class="resume-raw" id="resumeText"></div>
          </div>
        </div>
      </section>

      <!-- ATS SCREEN -->
      <section class="screen" id="ats">
        <div class="page-header">
          <div>
            <h1>ATS Scanner</h1>
            <p class="page-sub">See exactly how ATS systems score your resume — and how to fix it.</p>
          </div>
        </div>

        <div class="card">
          <div class="card-title">Paste Job Description</div>
          <textarea id="jdInput" rows="6" placeholder="Paste the full job description here. The more detail, the more accurate your score."></textarea>
          <div class="btn-row" style="margin-top:12px">
            <button class="btn-primary" id="scanBtn">🔍 Run ATS Scan</button>
          </div>
        </div>

        <div class="scores-grid" id="scoresGrid" style="display:none">
          <div class="score-card composite">
            <div class="score-label">Composite Score</div>
            <div class="score-ring" id="compositeRing">
              <svg viewBox="0 0 100 100">
                <circle class="ring-bg" cx="50" cy="50" r="40"/>
                <circle class="ring-fill" id="ringFill" cx="50" cy="50" r="40"/>
              </svg>
              <div class="score-number" id="composite">--</div>
            </div>
          </div>

          <div class="sub-scores">
            <div class="sub-score-card">
              <div class="sub-label">Keyword Match</div>
              <div class="sub-bar-wrap"><div class="sub-bar" id="barKeyword"></div></div>
              <div class="sub-val" id="keyword">--</div>
            </div>
            <div class="sub-score-card">
              <div class="sub-label">Format Quality</div>
              <div class="sub-bar-wrap"><div class="sub-bar" id="barFormat"></div></div>
              <div class="sub-val" id="format">--</div>
            </div>
            <div class="sub-score-card">
              <div class="sub-label">Content Quality</div>
              <div class="sub-bar-wrap"><div class="sub-bar" id="barQuality"></div></div>
              <div class="sub-val" id="quality">--</div>
            </div>
            <div class="sub-score-card">
              <div class="sub-label">Completeness</div>
              <div class="sub-bar-wrap"><div class="sub-bar" id="barComplete"></div></div>
              <div class="sub-val" id="complete">--</div>
            </div>
            <div class="sub-score-card">
              <div class="sub-label">Contact Info</div>
              <div class="sub-bar-wrap"><div class="sub-bar" id="barContact"></div></div>
              <div class="sub-val" id="contact">--</div>
            </div>
          </div>
        </div>

        <div class="card suggestions-card" id="suggestionsCard" style="display:none">
          <div class="card-title">💡 Actionable Suggestions</div>
          <ul id="suggestionsList" class="suggestions-list"></ul>
          <div id="missingKeywordsWrap" style="margin-top:16px;display:none">
            <div class="card-title" style="font-size:13px;margin-bottom:8px">Missing Keywords</div>
            <div id="missingKeywords" class="keyword-chips"></div>
          </div>
        </div>
      </section>

      <!-- JOBS SCREEN -->
      <section class="screen" id="jobs">
        <div class="page-header">
          <div>
            <h1>Job Matches</h1>
            <p class="page-sub">Ranked by skill match against your career profile.</p>
          </div>
          <button class="btn-primary" id="refreshJobsBtn">🔄 Refresh</button>
        </div>
        <div id="jobList" class="job-list"></div>
      </section>

      <!-- DASHBOARD SCREEN -->
      <section class="screen" id="dashboard">
        <div class="page-header">
          <div>
            <h1>Analytics Dashboard</h1>
            <p class="page-sub">Your career health at a glance.</p>
          </div>
          <button class="btn-primary" id="refreshDashBtn">🔄 Refresh</button>
        </div>

        <div class="metrics-grid">
          <div class="metric-card accent">
            <div class="metric-icon">🎯</div>
            <div class="metric-val" id="bestScore">0</div>
            <div class="metric-label">Best ATS Score</div>
          </div>
          <div class="metric-card">
            <div class="metric-icon">📄</div>
            <div class="metric-val" id="totalResumes">0</div>
            <div class="metric-label">Resumes Generated</div>
          </div>
          <div class="metric-card">
            <div class="metric-icon">🔍</div>
            <div class="metric-val" id="scansPerformed">0</div>
            <div class="metric-label">ATS Scans Run</div>
          </div>
          <div class="metric-card">
            <div class="metric-icon">💼</div>
            <div class="metric-val" id="jobs70">0</div>
            <div class="metric-label">Jobs Matched &gt;70%</div>
          </div>
          <div class="metric-card">
            <div class="metric-icon">📋</div>
            <div class="metric-val" id="appsTracked">0</div>
            <div class="metric-label">Applications Tracked</div>
          </div>
          <div class="metric-card">
            <div class="metric-icon">✅</div>
            <div class="metric-val" id="profileComplete">0%</div>
            <div class="metric-label">Profile Complete</div>
          </div>
        </div>

        <div class="card" style="margin-top:24px">
          <div class="card-title">Profile Completeness</div>
          <div class="progress-bar-wrap">
            <div class="progress-bar" id="profileBar"></div>
          </div>
          <p id="profileTip" class="profile-tip">Sign in and complete your profile to see full analytics.</p>
        </div>
      </section>

    </main>
  </div>

  <div class="toast" id="toast"></div>
  <script src="/static/app.js"></script>
</body>
</html>
```

- [ ] Replace `styles.css` with this complete stylesheet:

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface2: #22263a;
  --border: #2e3348;
  --accent: #6c63ff;
  --accent2: #4ecca3;
  --text: #e8eaf6;
  --text2: #8b92b8;
  --danger: #ff6b6b;
  --warn: #ffd166;
  --success: #06d6a0;
  --radius: 14px;
  --sidebar: 240px;
}

html, body { height: 100%; background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; font-size: 14px; }

.app { display: flex; height: 100vh; overflow: hidden; }

/* SIDEBAR */
.sidebar {
  width: var(--sidebar);
  background: var(--surface);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  padding: 20px 12px;
  flex-shrink: 0;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 10px 24px;
}

.brand-icon {
  width: 36px; height: 36px;
  background: var(--accent);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 18px; color: #fff;
  flex-shrink: 0;
}

.brand-name { font-weight: 800; font-size: 16px; color: var(--text); }
.brand-tag { font-size: 10px; color: var(--text2); margin-top: 1px; }

.sidebar-nav { display: flex; flex-direction: column; gap: 4px; flex: 1; }

.nav-item {
  display: flex; align-items: center; gap: 10px;
  width: 100%; padding: 10px 14px;
  border: none; background: transparent;
  color: var(--text2); font-size: 13px; font-weight: 500;
  border-radius: 10px; cursor: pointer;
  text-align: left; transition: all 0.15s;
}

.nav-item:hover { background: var(--surface2); color: var(--text); }
.nav-item.active { background: var(--accent); color: #fff; }
.nav-icon { font-size: 16px; }

.sidebar-footer { padding-top: 16px; border-top: 1px solid var(--border); }

.auth-badge {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 10px; border-radius: 8px;
  font-size: 12px; color: var(--text2);
}

.auth-dot {
  width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
}
.auth-dot.offline { background: var(--danger); }
.auth-dot.online { background: var(--success); }

/* MAIN */
.main {
  flex: 1; overflow-y: auto;
  padding: 32px 36px;
  background: var(--bg);
}

.screen { display: none; }
.screen.active { display: block; animation: fadeIn 0.2s ease; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }

.page-header {
  display: flex; align-items: flex-start; justify-content: space-between;
  margin-bottom: 28px;
}

.page-header h1 { font-size: 26px; font-weight: 800; color: var(--text); }
.page-sub { font-size: 13px; color: var(--text2); margin-top: 4px; }

.status-pill {
  background: var(--surface2); border: 1px solid var(--border);
  border-radius: 20px; padding: 4px 14px; font-size: 12px; color: var(--text2);
}

/* CARDS */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  margin-bottom: 20px;
}

.card-title {
  font-size: 13px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--text2); margin-bottom: 16px;
}

.card-grid { display: grid; gap: 20px; }
.card-grid.two { grid-template-columns: 1fr 1fr; }

/* FORMS */
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 12px; font-weight: 600; color: var(--text2); margin-bottom: 6px; }
.form-group input,
.form-group select,
.form-group textarea {
  width: 100%; background: var(--surface2);
  border: 1px solid var(--border); border-radius: 8px;
  color: var(--text); font-family: inherit; font-size: 13px;
  padding: 10px 12px; outline: none; transition: border-color 0.15s;
}
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus { border-color: var(--accent); }
.form-group textarea { resize: vertical; }
.form-group select { appearance: none; }
.hint { font-weight: 400; color: var(--text2); font-size: 11px; }

/* BUTTONS */
.btn-primary {
  background: var(--accent); color: #fff;
  border: none; border-radius: 8px;
  padding: 10px 20px; font-size: 13px; font-weight: 600;
  cursor: pointer; transition: opacity 0.15s; white-space: nowrap;
}
.btn-primary:hover { opacity: 0.85; }

.btn-ghost {
  background: var(--surface2); color: var(--text);
  border: 1px solid var(--border); border-radius: 8px;
  padding: 10px 16px; font-size: 13px; font-weight: 500;
  cursor: pointer; transition: border-color 0.15s; white-space: nowrap;
}
.btn-ghost:hover { border-color: var(--accent); }

.btn-row { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 6px; }

/* RESUME PREVIEW */
.resume-preview { overflow: hidden; }

.resume-doc {
  background: #fff; color: #111;
  border-radius: 8px; padding: 24px;
  font-family: 'Georgia', serif; font-size: 12px;
  line-height: 1.6;
}

.resume-header-block { border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 12px; }
.resume-header-block h2 { font-size: 18px; font-weight: 700; color: #1a1a2e; }
.resume-role { font-size: 12px; color: #555; margin-top: 2px; }
.resume-section { margin-bottom: 12px; }
.resume-section-title { font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #333; margin-bottom: 4px; border-bottom: 1px solid #ddd; padding-bottom: 2px; }
.resume-section ul { padding-left: 16px; }
.resume-raw { display: none; }

/* ATS SCORES */
.scores-grid {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.score-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}

.score-card.composite { background: linear-gradient(135deg, #1a1d27, #22263a); }

.score-label { font-size: 12px; font-weight: 700; color: var(--text2); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 16px; }

.score-ring { position: relative; width: 120px; height: 120px; }
.score-ring svg { width: 120px; height: 120px; transform: rotate(-90deg); }
.ring-bg { fill: none; stroke: var(--surface2); stroke-width: 8; }
.ring-fill { fill: none; stroke: var(--accent); stroke-width: 8; stroke-linecap: round; stroke-dasharray: 251; stroke-dashoffset: 251; transition: stroke-dashoffset 1s ease; }

.score-number {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  font-size: 28px; font-weight: 800; color: var(--text);
}

.sub-scores {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  display: flex; flex-direction: column; gap: 14px;
}

.sub-score-card { display: flex; align-items: center; gap: 12px; }
.sub-label { font-size: 12px; color: var(--text2); width: 120px; flex-shrink: 0; }
.sub-bar-wrap { flex: 1; height: 6px; background: var(--surface2); border-radius: 99px; overflow: hidden; }
.sub-bar { height: 100%; border-radius: 99px; background: var(--accent2); transition: width 0.8s ease; width: 0%; }
.sub-val { font-size: 13px; font-weight: 700; width: 36px; text-align: right; }

/* SUGGESTIONS */
.suggestions-card {}
.suggestions-list { list-style: none; display: flex; flex-direction: column; gap: 10px; }
.suggestions-list li {
  display: flex; align-items: flex-start; gap: 10px;
  background: var(--surface2); border-radius: 8px;
  padding: 12px 14px; font-size: 13px; color: var(--text);
}
.suggestions-list li::before { content: "→"; color: var(--accent); font-weight: 700; flex-shrink: 0; }

.keyword-chips { display: flex; flex-wrap: wrap; gap: 8px; }
.chip {
  background: var(--surface2); border: 1px solid var(--border);
  border-radius: 20px; padding: 4px 12px;
  font-size: 12px; color: var(--warn); font-weight: 600;
}

/* JOBS */
.job-list { display: flex; flex-direction: column; gap: 14px; }

.job-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 24px;
  display: flex; align-items: center; justify-content: space-between;
  transition: border-color 0.15s;
}
.job-card:hover { border-color: var(--accent); }

.job-left { display: flex; flex-direction: column; gap: 4px; }
.job-title { font-size: 15px; font-weight: 700; color: var(--text); }
.job-meta { font-size: 12px; color: var(--text2); display: flex; gap: 12px; }
.job-meta span::before { margin-right: 4px; }

.job-right { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; }

.match-badge {
  font-size: 20px; font-weight: 800;
  padding: 6px 14px; border-radius: 8px;
}
.match-high { background: rgba(6,214,160,0.15); color: var(--success); }
.match-mid { background: rgba(255,209,102,0.15); color: var(--warn); }
.match-low { background: rgba(255,107,107,0.15); color: var(--danger); }

.job-type-badge {
  font-size: 11px; font-weight: 600; padding: 2px 10px;
  border-radius: 20px; background: var(--surface2); color: var(--text2);
  border: 1px solid var(--border);
}

/* DASHBOARD */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.metric-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  display: flex; flex-direction: column; align-items: flex-start; gap: 8px;
}
.metric-card.accent { border-color: var(--accent); background: linear-gradient(135deg, #1a1d27, #1e1b3a); }

.metric-icon { font-size: 24px; }
.metric-val { font-size: 36px; font-weight: 800; color: var(--text); }
.metric-label { font-size: 12px; color: var(--text2); font-weight: 500; }

.progress-bar-wrap { height: 10px; background: var(--surface2); border-radius: 99px; overflow: hidden; margin-bottom: 12px; }
.progress-bar { height: 100%; border-radius: 99px; background: linear-gradient(90deg, var(--accent), var(--accent2)); transition: width 0.8s ease; width: 0%; }
.profile-tip { font-size: 12px; color: var(--text2); }

/* TOAST */
.toast {
  position: fixed; bottom: 24px; right: 24px;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 10px; padding: 12px 20px;
  font-size: 13px; color: var(--text);
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  transform: translateY(100px); opacity: 0;
  transition: all 0.25s ease; z-index: 9999;
}
.toast.show { transform: none; opacity: 1; }
.toast.success { border-color: var(--success); }
.toast.error { border-color: var(--danger); }

/* SCROLLBAR */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 99px; }

@media (max-width: 900px) {
  .card-grid.two { grid-template-columns: 1fr; }
  .scores-grid { grid-template-columns: 1fr; }
  .metrics-grid { grid-template-columns: 1fr 1fr; }
  .sidebar { width: 60px; }
  .sidebar .brand-name, .sidebar .brand-tag, .sidebar-nav span:not(.nav-icon), .auth-badge span { display: none; }
  .sidebar-brand { justify-content: center; }
  .main { padding: 20px 16px; }
}
```

- [ ] Replace `app.js` with the complete JS logic:

```javascript
const API = "";
let token = localStorage.getItem("cos_token") || null;

// ---- Utilities ----

function toast(msg, type = "info") {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.className = "toast show " + type;
  clearTimeout(el._t);
  el._t = setTimeout(() => (el.className = "toast"), 3000);
}

async function api(path, method = "GET", body = null) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json", ...(token ? { Authorization: "Bearer " + token } : {}) },
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(API + path, opts);
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Request failed");
  return data;
}

function setAuthState(name) {
  const dot = document.querySelector(".auth-dot");
  const state = document.getElementById("authState");
  if (name) {
    dot.className = "auth-dot online";
    state.textContent = name.split(" ")[0];
  } else {
    dot.className = "auth-dot offline";
    state.textContent = "Not signed in";
  }
}

// ---- Nav ----

document.querySelectorAll(".nav-item").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".nav-item").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".screen").forEach((s) => s.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(btn.dataset.screen).classList.add("active");
  });
});

// ---- Auth ----

document.getElementById("registerBtn").addEventListener("click", async () => {
  try {
    const data = await api("/api/auth/register", "POST", {
      full_name: document.getElementById("nameInput").value,
      email: document.getElementById("emailInput").value,
      password: document.getElementById("passwordInput").value,
    });
    token = data.token;
    localStorage.setItem("cos_token", token);
    setAuthState(data.user.full_name);
    document.getElementById("statusText").textContent = "Signed in";
    toast("Account created! Welcome to CareerOS.", "success");
  } catch (e) {
    toast(e.message, "error");
  }
});

document.getElementById("loginBtn").addEventListener("click", async () => {
  try {
    const data = await api("/api/auth/login", "POST", {
      email: document.getElementById("emailInput").value,
      password: document.getElementById("passwordInput").value,
    });
    token = data.token;
    localStorage.setItem("cos_token", token);
    setAuthState(data.user.full_name);
    document.getElementById("statusText").textContent = "Signed in";
    toast("Welcome back!", "success");
    loadProfile();
  } catch (e) {
    toast(e.message, "error");
  }
});

// ---- Profile ----

async function loadProfile() {
  if (!token) return;
  try {
    const d = await api("/api/profile");
    document.getElementById("nameInput").value = d.full_name || "";
    document.getElementById("cityInput").value = d.city || "";
    document.getElementById("statusInput").value = d.professional_status || "Fresher";
    document.getElementById("roleInput").value = d.target_role || "";
    document.getElementById("skillsInput").value = d.skills_csv || "";
    document.getElementById("summaryInput").value = d.summary || "";
    document.getElementById("expInput").value = d.experience_bullet || "";
    updateResumePreview();
    setAuthState(d.full_name);
  } catch (_) {}
}

document.getElementById("saveProfileBtn").addEventListener("click", async () => {
  try {
    await api("/api/profile", "PUT", {
      full_name: document.getElementById("nameInput").value,
      city: document.getElementById("cityInput").value,
      professional_status: document.getElementById("statusInput").value,
      target_role: document.getElementById("roleInput").value,
      skills_csv: document.getElementById("skillsInput").value,
      summary: document.getElementById("summaryInput").value,
      experience_bullet: document.getElementById("expInput").value,
    });
    toast("Profile saved!", "success");
    updateResumePreview();
  } catch (e) {
    toast(e.message, "error");
  }
});

// ---- Resume Builder ----

function updateResumePreview() {
  document.getElementById("pvName").textContent = document.getElementById("nameInput").value || "Your Name";
  document.getElementById("pvRole").textContent = document.getElementById("roleInput").value || "Target Role";
  document.getElementById("pvSummary").textContent = document.getElementById("summaryInput").value || "Your professional summary will appear here.";
  document.getElementById("pvExp").textContent = document.getElementById("expInput").value || "Your experience bullet will appear here.";
  document.getElementById("pvSkills").textContent = document.getElementById("skillsInput").value || "Your skills will appear here.";
}

["summaryInput", "expInput", "skillsInput", "nameInput", "roleInput"].forEach((id) => {
  document.getElementById(id).addEventListener("input", updateResumePreview);
});

document.getElementById("autofillBtn").addEventListener("click", () => {
  document.getElementById("summaryInput").value =
    "Results-driven software engineer with strong fundamentals in full-stack development. Passionate about building scalable, user-centric applications. Quick learner with hands-on experience in Python, React, and cloud infrastructure.";
  document.getElementById("expInput").value =
    "Built a REST API using FastAPI and PostgreSQL, serving 5,000+ daily users with 99.8% uptime. Reduced page load time by 40% through lazy loading and caching optimization. Led a team of 3 in delivering a college project within a 4-week sprint.";
  updateResumePreview();
  toast("Sample content loaded!", "success");
});

document.getElementById("saveProfileFromResumeBtn").addEventListener("click", async () => {
  try {
    await api("/api/profile", "PUT", {
      full_name: document.getElementById("nameInput").value,
      city: document.getElementById("cityInput").value,
      professional_status: document.getElementById("statusInput").value,
      target_role: document.getElementById("roleInput").value,
      skills_csv: document.getElementById("skillsInput").value,
      summary: document.getElementById("summaryInput").value,
      experience_bullet: document.getElementById("expInput").value,
    });
    toast("Saved to profile!", "success");
  } catch (e) {
    toast(e.message, "error");
  }
});

document.getElementById("generateResumeBtn").addEventListener("click", async () => {
  if (!token) { toast("Please sign in first.", "error"); return; }
  try {
    const d = await api("/api/resumes/generate", "POST", {
      template_name: document.getElementById("templateSelect").value,
    });
    document.getElementById("resumeText").style.display = "block";
    document.getElementById("resumeText").textContent = d.content;
    toast("Resume generated and saved!", "success");
  } catch (e) {
    toast(e.message, "error");
  }
});

// ---- ATS Scanner ----

function setBar(id, value) {
  document.getElementById(id).style.width = value + "%";
}

function scoreColor(v) {
  if (v >= 75) return "#06d6a0";
  if (v >= 55) return "#ffd166";
  return "#ff6b6b";
}

document.getElementById("scanBtn").addEventListener("click", async () => {
  if (!token) { toast("Please sign in first.", "error"); return; }
  const jd = document.getElementById("jdInput").value.trim();
  if (!jd) { toast("Please paste a job description.", "error"); return; }

  document.getElementById("scanBtn").textContent = "Scanning…";
  try {
    const d = await api("/api/ats/scan", "POST", { jd_text: jd });

    document.getElementById("scoresGrid").style.display = "grid";
    document.getElementById("composite").textContent = d.composite;

    // Animate ring
    const circumference = 251;
    const offset = circumference - (d.composite / 100) * circumference;
    const ring = document.getElementById("ringFill");
    ring.style.stroke = scoreColor(d.composite);
    setTimeout(() => (ring.style.strokeDashoffset = offset), 50);

    document.getElementById("keyword").textContent = d.keyword;
    document.getElementById("format").textContent = d.format;
    document.getElementById("quality").textContent = d.quality;
    document.getElementById("complete").textContent = d.complete;
    document.getElementById("contact").textContent = d.contact;

    setBar("barKeyword", d.keyword);
    setBar("barFormat", d.format);
    setBar("barQuality", d.quality);
    setBar("barComplete", d.complete);
    setBar("barContact", d.contact);

    // Suggestions
    document.getElementById("suggestionsCard").style.display = "block";
    const list = document.getElementById("suggestionsList");
    list.innerHTML = "";
    (d.suggestions || []).forEach((s) => {
      const li = document.createElement("li");
      li.textContent = s;
      list.appendChild(li);
    });

    if (d.missing_keywords && d.missing_keywords.length > 0) {
      document.getElementById("missingKeywordsWrap").style.display = "block";
      const chips = document.getElementById("missingKeywords");
      chips.innerHTML = d.missing_keywords.map((k) => `<span class="chip">${k}</span>`).join("");
    } else {
      document.getElementById("missingKeywordsWrap").style.display = "none";
    }

    toast("ATS scan complete!", "success");
  } catch (e) {
    toast(e.message, "error");
  } finally {
    document.getElementById("scanBtn").textContent = "🔍 Run ATS Scan";
  }
});

// ---- Job Matches ----

async function loadJobs() {
  if (!token) { toast("Please sign in first.", "error"); return; }
  try {
    const d = await api("/api/jobs/matches");
    const list = document.getElementById("jobList");
    list.innerHTML = "";
    d.jobs.forEach((j) => {
      const matchClass = j.score >= 75 ? "match-high" : j.score >= 60 ? "match-mid" : "match-low";
      list.innerHTML += `
        <div class="job-card">
          <div class="job-left">
            <div class="job-title">${j.title}</div>
            <div class="job-meta">
              <span>🏢 ${j.company}</span>
              <span>📍 ${j.location}</span>
              <span>🔧 ${j.skills.slice(0, 3).join(", ")}</span>
            </div>
          </div>
          <div class="job-right">
            <div class="match-badge ${matchClass}">${j.score}%</div>
            <div class="job-type-badge">${j.type || "Full-time"}</div>
          </div>
        </div>`;
    });
    toast("Jobs loaded!", "success");
  } catch (e) {
    toast(e.message, "error");
  }
}

document.getElementById("refreshJobsBtn").addEventListener("click", loadJobs);

// ---- Dashboard ----

async function loadDashboard() {
  if (!token) { toast("Please sign in first.", "error"); return; }
  try {
    const d = await api("/api/dashboard");
    document.getElementById("bestScore").textContent = d.best_ats_score;
    document.getElementById("totalResumes").textContent = d.total_resumes;
    document.getElementById("scansPerformed").textContent = d.scans_performed;
    document.getElementById("jobs70").textContent = d.jobs_matched_over_70;
    document.getElementById("appsTracked").textContent = d.applications_tracked;
    document.getElementById("profileComplete").textContent = d.profile_completeness + "%";
    document.getElementById("profileBar").style.width = d.profile_completeness + "%";
    document.getElementById("profileTip").textContent =
      d.profile_completeness === 100
        ? "🎉 Profile is 100% complete — all modules are fully powered."
        : `Fill in the remaining fields to reach 100% and boost your ATS scores.`;
    toast("Dashboard updated!", "success");
  } catch (e) {
    toast(e.message, "error");
  }
}

document.getElementById("refreshDashBtn").addEventListener("click", loadDashboard);

// ---- Init ----

if (token) loadProfile();
```

---

### Task 5: Verify backend runs

**Files:** none changed

- [ ] Install deps and start the server:
```bash
cd backend/legacy/v0-prototype-monolith
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Expected: Server starts at `http://localhost:8000`

- [ ] Open browser to `http://localhost:8000` — should see the new dark UI with sidebar nav.

- [ ] Test the full flow manually:
  1. Register with name/email/password
  2. Fill career details → Save Profile
  3. Go to Resume Builder → Autofill Sample → Generate Resume
  4. Go to ATS Scanner → paste any job description → Run ATS Scan → see scores + suggestions
  5. Go to Job Matches → Refresh → see 15 jobs with match %
  6. Go to Analytics → Refresh → see all 6 metrics populated

---

### Task 6: Write a clean README

**Files:**
- Modify: `backend/legacy/v0-prototype-monolith/README.md`

- [ ] Replace README with:

```markdown
# CareerOS — MVP v0.1

AI-powered career intelligence platform. ATS resume scoring, job matching, and analytics — all in one.

## Quick Start

```bash
cd backend/legacy/v0-prototype-monolith
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000

## What Works

| Module | Status |
|--------|--------|
| Auth (Register / Login) | ✅ |
| Career Profile | ✅ |
| Resume Builder (3 templates) | ✅ |
| ATS Scanner (6 dimensions + suggestions) | ✅ |
| Job Matching (15 live listings) | ✅ |
| Analytics Dashboard | ✅ |

## Tech Stack

- **Backend:** Python 3.11, FastAPI, SQLAlchemy, SQLite
- **Frontend:** Vanilla HTML/CSS/JS (no build step)
- **Database:** SQLite (file: careeros_dev.db)
```

---

### Task 7: Commit everything

- [ ] Stage and commit:
```bash
cd c:/Users/ADMIN/Desktop/CareerOS
git add backend/legacy/v0-prototype-monolith/
git commit -m "feat: polished MVP — new UI, ATS suggestions, 15 job listings"
```
