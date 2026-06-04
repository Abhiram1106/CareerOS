---
date: 2026-06-02
tool: claude-code
model: claude-sonnet-4-6
tags: [session, M4, applications, tracker, kanban]
type: session
links: [error-memory, active-goals]
---

# Session 2026-06-02 (6) — M4: Application tracker

## What was done

### M4 — Application tracker UI (full implementation)

**`JobCard.tsx`** (rebuilt):
- Save job button → POST /applications; shows `✓ Saved` + status badge immediately
- Status badge colour-coded (blue=applied, purple=screening, amber=interview, green=offer, red=rejected)
- Apply ↗ external link rendered when `apply_url` present
- Skills as chip tags, cleaner header layout

**`jobs/page.tsx`** (updated):
- Loads saved applications on mount → builds `externalId → JobApplication` map
- Passes `savedApplication` to each JobCard so saved state is pre-populated
- "My applications (N)" count badge links to /applications
- Enter key submits search

**`apps/web/app/(app)/applications/page.tsx`** (new):
- Kanban view: 6 colour-coded columns (Saved → Applied → Screening → Interview → Offer → Rejected)
- List view toggle for scrollable alternative
- Inline status dropdown on each card — optimistic UI (updates local state immediately)
- `applied_at` auto-set server-side when status moves to "applied"
- Remove button → DELETE /applications/{id}
- Empty state with Browse jobs link

**`layout.tsx`**: Applications added to PRIMARY_NAV (ClipboardList icon)

**`api.ts`**: `JobSearchItem.apply_url` added as optional field

**Verified**: save→applied→interview status flow, applied_at timestamp, tsc clean

---

## Next: M5 — Analytics / score history

scorecards table stores every scan. Need:
- GET /analytics/score-history → [{date, overall_score, bucket}] from scorecards table
- Dashboard sparkline showing score trend over time
- "Your score improved X points this week" callout

_Related: [[active-goals]] · [[error-memory]]_
