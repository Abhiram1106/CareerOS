# 05 — Scoring System

## The formula (packages/scoring — single source of truth)

```
PlacementReadinessScore =
  0.35 × JD_Match
+ 0.20 × ATS_Parse_Safety
+ 0.20 × Evidence_Quality
+ 0.10 × Profile_Completeness
+ 0.10 × Interview_Readiness
+ 0.05 × Placement_Hygiene

JD_Match =
  0.35 × TFIDF_Cosine           (word/bigram TF-IDF, sklearnex-accelerated)
+ 0.35 × Semantic_Cosine        (MiniLM all-MiniLM-L6-v2 sentence embeddings)
+ 0.20 × Required_Skill_Recall  (% of JD required skills found in resume)
+ 0.10 × Eligibility_Rule_Score (CGPA ≥ min, backlogs ≤ max, branch, grad year)

Buckets: 0–49 high-risk | 50–69 borderline | 70–84 ready | 85–100 strong
```

**Rule:** This formula lives **only** in `packages/scoring/careeros_scoring/formula.py`. Never duplicate it in a service or frontend.

---

## Sub-scorer details

### ATS_Parse_Safety (`parse_safety.py` → `analyze_ats`)
7-dimension weighted analysis of the resume text:

| Dimension | Weight | What it checks |
|---|---|---|
| contact_reachability | 0.20 | Email, phone, LinkedIn, portfolio present in text |
| section_structure | 0.20 | Education, Experience, Skills, Projects headings found |
| formatting_safety | 0.20 | No tables, no multi-column, no images, no special glyphs |
| date_consistency | 0.10 | Consistent date format throughout |
| content_density | 0.15 | Word count in 150–1200 optimal range |
| bullet_structure | 0.10 | Bullets start with action verbs, have metrics |
| parse_cleanliness | 0.05 | No encoding issues, reasonable line lengths |

Also accepts a list of `ats_flags` from the resume-parser which add structural penalties.

**Important:** The legacy `ats_parse_safety_from_flags` function (flag-only path) exists for backward compat. The real scorer is `analyze_ats(resume_text, flags)`. The scorecard handler always calls `analyze_ats`.

---

### Evidence_Quality (`resume_components.py`)
Reads `experience` and `projects` sections. 4-signal composite:

- **Verb variety (0.30):** Count of *distinct* action verbs from a 30-verb set. "built built built" = 1, not 6.
- **Metric density (0.30):** Regex for `\d+(%, x, k, m, ms, users, ...)` with `(?!\w)` lookahead (fixes `40%.` matching).
- **Tech-term specificity (0.25):** Count of recognized tech terms (Python, Docker, SQL, etc.)
- **Bullet depth (0.15):** Median word count of bullets — longer = more context

Floor: any resume with experience/project text scores at least 20.

---

### Interview_Readiness (`resume_components.py`)
Reads `experience`, `projects`, `positions_of_responsibility`. 5-signal composite:

- Tech density: tech terms per 100 words
- Metric count: same metric regex as above
- Breadth: has both experience AND projects text ≥ 15 words
- Leadership: count of led/managed/mentored/coordinated etc.
- Role variety: date patterns in experience section (multiple stints)

---

### Placement_Hygiene (`resume_components.py`)
Starts at 100, subtracts penalties:

- No email: −20 | No phone: −10 | No LinkedIn/GitHub link: −8
- Filler phrases (team player, quick learner, passionate about...): −7 each, max −20
- Wall of text (many lines, no bullets): −8
- Text too sparse: −18 (< 25 words total)
- Tech skill count in skills section: 0 terms = −10, 1 term = −5, 6+ terms = +5 bonus

---

### Profile_Completeness (`resume_components.py`)
Quality-aware — not just presence check. Each of 5 sections contributes weighted score:

| Section | Weight | Min words for full credit |
|---|---|---|
| summary | 0.10 | 10 |
| education | 0.20 | 5 |
| experience | 0.30 | 12 |
| projects | 0.25 | 10 |
| skills | 0.15 | 4 |

A section with < 3 words = 0.20 × weight. A section with content but below threshold = 0.65 × weight.

---

## Eligibility scoring (`match-engine/app/matcher.py`)

Compares student profile against JD-parsed eligibility criteria:

```
if CGPA < min_cgpa:        score -= min(35, gap × 12)
if backlogs > max_backlogs: score -= min(40, excess × 20)
if branch not in allowed:   score -= 15
if grad_year not in list:   score -= 20
```

Returns 0–100. Only fires when the JD has explicit criteria **and** the student has filled their profile. If no JD criteria → 100.

---

## Skill matching (`match-engine/app/skill_taxonomy.py`)

Two-pass algorithm to prevent false positives:
1. **Pass 1:** Scan 70-skill SKILL_TAXONOMY tokens longest-first, record claimed spans
2. **Pass 2:** Scan 50 SKILL_ALIASES (js→javascript, k8s→kubernetes, ml→machine learning etc.), skip if span is already claimed

Key bug-fixes made:
- `"go"` alias removed (false-positive in "let me go to the store")
- `"cv"` alias removed (false-positive in "CV of Rahul")
- `c++`, `ci/cd` use `(?<!\w)..(?!\w)` instead of `\b` (special char fix)
- `"js"` no longer matches inside `"next.js"` (span-claimed)

---

## Discrimination gate

Automated test in `tests/golden/`:
- 7 resume personas across strong/mid/weak tiers
- Each of 5 sub-scores must have: spread ≥ 30 AND distinct values ≥ 5
- Strong mean > weak mean

Run it: `docker compose exec core-api python /tmp/_runner.py` (after copying files)

**Current result: 5/5 PASS**
```
ats_parse_safety    spread=58.9  distinct=7  PASS
evidence_quality    spread=100.0 distinct=5  PASS
interview_readiness spread=89.5  distinct=5  PASS
placement_hygiene   spread=73.0  distinct=5  PASS
profile_completeness spread=93.5 distinct=5  PASS
```
