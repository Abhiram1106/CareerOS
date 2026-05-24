# Product screenshots

Capture these routes for the pitch deck (1920×1080 recommended):

| File | Route | Caption |
|------|-------|---------|
| `01-workspace-readiness.png` | `/workspace` → Readiness tab | Placement readiness score vs JD |
| `02-rewrite-diff.png` | `/workspace` → Rewrite tab | Proof-linked diff + unsupported claims |
| `03-officer-dashboard.png` | `/officer/dashboard` | Cohort KPIs + dept heatmap |
| `04-lab-intel.png` | `/lab/intel` | Intel benchmark panel |
| `05-assistant.png` | `/workspace?tab=assistant` | Campus Assistant |

Set `NEXT_PUBLIC_ENABLE_OFFICER_SURFACE=true` before officer screenshots.

## Capture (manual or Playwright)

1. Start stack: `docker compose up` (or `pnpm dev` in `apps/web` + core-api on :8000).
2. Log in as demo student / officer per `README.md`.
3. Save PNGs into this folder with the names above.

Optional one-liner with Playwright CLI (install globally: `npm i -g playwright` then `npx playwright install chromium`):

```powershell
$base = "http://localhost:3000"
npx playwright screenshot "$base/workspace" docs/pitch/screenshots/01-workspace-readiness.png --viewport-size=1920,1080
```

Repeat for each route in the table. Officer routes require officer session cookie after login.
