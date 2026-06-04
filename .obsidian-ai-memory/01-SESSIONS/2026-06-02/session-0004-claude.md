---
date: 2026-06-02
tool: claude-code
model: claude-sonnet-4-6
tags: [session, M3, vendor-simulation, keyword-gap, ats]
type: session
links: [error-memory, active-goals]
---

# Session 2026-06-02 (5) — M3: Multi-vendor ATS simulation

## What was done

### M3 — Multi-vendor ATS simulation + keyword gap analysis

**`packages/scoring/careeros_scoring/vendor_simulation.py`** (new, 501 lines):

7 vendor rule engines, each scoring 0–100 with distinct logic:

| Vendor | Weight | Key signals |
|---|---|---|
| Taleo (Oracle) | 18% | Strict section headers (40pts), no tables (20pts), keyword overlap (30pts) |
| Workday | 16% | Keyword matching (35pts), skills (25pts), action verbs + metrics (15pts) |
| Naukri RMS | 15% | CGPA (12pts), Indian degrees (8pts), IIT/NIT bonus, phone (8pts) |
| Greenhouse | 12% | GitHub (15pts), keyword density (35pts), metrics (20pts) |
| PeopleStrong | 10% | CGPA + 10th/12th (30pts), phone priority (10pts), format tolerance |
| Darwinbox | 9% | Keyword (30pts), LinkedIn+GitHub (15pts), section structure (25pts) |
| Lever | 8% | GitHub (20pts), metrics (25pts), most lenient on format |

`simulate_vendors()` returns weighted composite + per-vendor breakdown.
`keyword_gap_analysis()` extracts JD keywords, scores presence/absence with
position-based importance (first third of JD = high, middle = medium, end = low).

**Injected everywhere:**
- Every `POST /scorecards/score` response now includes `vendor_simulation` + `keyword_gap`
- Standalone: `POST /ats/vendor-simulation`, `POST /ats/keyword-gap`

**Frontend:**
- `api.ts`: `VendorSimulation`, `VendorScore`, `KeywordGap` types; `ScorecardResult` extended
- `usePlacementWorkspace.ts`: `vendorSimulation` + `keywordGap` state populated from response
- `match/page.tsx`: vendor bar chart (colour-coded by score) + keyword gap chips (importance-coloured)

**Verified:**
- Strong resume (GitHub + metrics + CGPA): composite 61, Greenhouse/Lever 70+
- Thin resume (no GitHub, no metrics): composite 44, Taleo 58 vs Lever 25
- Keyword gap: correctly identifies present/missing with high/medium/low importance

---

## What's next: M4 — Application tracker UI

DB table + 24 API endpoints already live.
Need:
- "Save job" button on JobCard → POST /applications
- `/applications` page: kanban columns (saved → applied → screening → interview → offer/rejected)
- Status update via dropdown
- Resume version linked to each application

_Related: [[active-goals]] · [[error-memory]]_
