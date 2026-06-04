---
date: 2026-06-02
tool: claude-code
model: claude-sonnet-4-6
tags: [session, M4, M5, applications, tracker, analytics, sparkline]
type: session
links: [error-memory, active-goals]
---

# Session 2026-06-02 (7) — M4 Application Tracker + M5 Score History

## M4 — Application tracker

**JobCard.tsx**: save button → POST /applications; status badge colour-coded;
Apply ↗ link; skills as chips.

**jobs/page.tsx**: loads saved map on mount; "My applications (N)" badge;
Enter key submits search.

**applications/page.tsx** (new): kanban (6 columns) + list view toggle;
inline status dropdown; applied_at auto-set server-side; optimistic UI;
remove button; empty state.

**layout.tsx**: Applications in PRIMARY_NAV (ClipboardList icon).

**api.ts**: JobSearchItem.apply_url added.

---

## M5 — Score history analytics

**dashboard_controller.py**: GET /analytics/score-history → up to 50 scorecards
ordered chronologically with delta from first to last.

**ScoreSparkline**: pure SVG polyline + dots, colour by latest bucket
(green ≥70, amber ≥50, blue otherwise). Shown on dashboard when ≥2 scans.

**Delta badge**: ↑/↓ pts overall. Non-blocking (failure doesn't break dashboard).

Verified: 11 historical entries, delta computed correctly, tsc clean.

---

## What's next

All 5 MVP milestones (M1–M5) are complete:
- M1 ✅ Structured profile editor
- M2 ✅ Resume builder (3 templates from structured data)
- M3 ✅ Multi-vendor ATS simulation + keyword gap
- M4 ✅ Application tracker (kanban + list)
- M5 ✅ Score history sparkline

**Remaining work (post-MVP):**
- M6 Guided AI resume wizard
- B2B officer portal
- LinkedIn OAuth
- Native mobile app
- OpenVINO IR for embeddings

_Related: [[active-goals]] · [[error-memory]]_
