---
date: 2026-06-02
tool: claude-code
model: claude-sonnet-4-6
tags: [session, ci, workflows, disabled]
type: session
links: [active-goals]
---

# Session 2026-06-02 (2) — CI workflows disabled

## What was done

Temporarily disabled all three GitHub Actions workflows so teammates can push without CI blocking.

### How it was done
Replaced the `on: push/pull_request` triggers in each workflow with `on: workflow_dispatch` only.
The workflow files are preserved — CI can be re-enabled with a one-line revert per file.

### Files changed
- `.github/workflows/ci.yml` — was: `push: branches: [main]` → now: `workflow_dispatch` only
- `.github/workflows/secrets-scan.yml` — same change
- `.github/workflows/security-audit.yml` — same change (also removed `schedule:`)

### To re-enable CI
In each workflow file, restore:
```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```
For `security-audit.yml`, also restore the `schedule: - cron: "0 3 * * 1"` line.

---

_Related: [[active-goals]]_
