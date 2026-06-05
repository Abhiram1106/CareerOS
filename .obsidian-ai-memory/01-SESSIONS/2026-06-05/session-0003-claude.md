---
date: 2026-06-05
tool: claude-code
model: claude-sonnet-4-6
tags: [session, ui-fix, css, frontend, globals-css]
type: session
links: [active-goals]
---

# Session 2026-06-05 (4) — UI Repair: 60+ Missing CSS Classes

## Problem

The entire webapp was visually broken. `globals.css` defined the design tokens and a handful
of layout primitives, but was completely missing every domain-specific CSS class referenced
by the components.

## Root cause

The Clinical Data Studio redesign (session-0002) rewrote the CSS token layer but did not
carry forward the component-level classes. Approx 60 class names were used in TSX but had
no definitions — they rendered as unstyled raw HTML.

## Missing classes added to globals.css

| Category | Classes |
|---|---|
| Layout | `--page-max`, `workspace-grid`, `readiness-stack` |
| Cards | `content-card`, `content-card-header`, `content-card-body`, `content-card-title` |
| Primitives | `card-header`, `card-header-left`, `card-badge`, `card-action`, `card-subtitle`, `field-hint` |
| Chips | `chip`, `chip-primary`, `chip-success`, `chip-warn`, `chip-danger`, `chip-mono` |
| Scan/JD | `scan-grid`, `scan-intro`, `scan-hint-banner`, `scan-meta-row`, `scan-meta-small`, `jd-textarea` |
| Section list | `section-heading`, `section-list-heading`, `section-list`, `section-list-item`, `section-list-name`, `section-conf-badge` |
| ATS warnings | `ats-warning-panel`, `ats-warning-title`, `ats-warning-list`, `ats-flag-badge` |
| Export | `export-actions`, `export-status-line`, `btn-flex`, `btn-icon` |
| Score breakdown | `score-breakdown`, `score-overall`, `score-overall-value`, `score-overall-label`, `score-bucket-pill`, `score-bars`, `score-bar-row`, `score-bar-meta`, `score-bar-track`, `score-bar-fill`, `score-bar-value`, `score-bar-weight`, `score-method-note` |
| ScoreBarsInline | `score-inline-row`, `score-inline-label`, `score-inline-weight`, `score-inline-track`, `score-inline-fill`, `score-inline-value`, `score-inline-total`, `score-inline-total-end`, `score-inline-total-num` |
| Rewrite panel | `rewrite-stack`, `rewrite-toolbar`, `rewrite-intro`, `rewrite-empty`, `rewrite-panel`, `rewrite-panel--warn`, `rewrite-panel--info`, `rewrite-panel-title`, `rewrite-diff-list`, `rewrite-diff-card`, `rewrite-diff-header`, `rewrite-diff-columns`, `rewrite-diff-col`, `rewrite-diff-label`, `rewrite-diff-text`, `rewrite-diff-text--before`, `rewrite-diff-text--after`, `rewrite-conf`, `rewrite-conf--high`, `rewrite-conf--medium`, `rewrite-conf--review`, `rewrite-evidence`, `rewrite-evidence-id`, `rewrite-unsupported-list`, `rewrite-unsupported-claim`, `rewrite-unsupported-reason`, `rewrite-confirm-list` |
| Assistant | `typing-indicator`, `assistant-score-context` |
| Dashboard | `dashboard-score-sub`, `dashboard-actions`, `dashboard-action-link`, `section-heading` |
| Utilities | `workspace-error`, `scan-empty`, `scan-empty-state`, `workspace-select`, `skill-lists`, `skill-lists-missing`, `settings-entry-card` |

## TypeScript fixes

- `dashboard/page.tsx`: `FileText` used in checklist but not imported → added to lucide import
- `dashboard/page.tsx`: `AnimatedCounter` has no `style` prop → removed `style`, added `score-overall-value` class instead

## Hardcoded color cleanup

Replaced raw hex strings with CSS variables across:
- `resume/page.tsx` — template selector buttons
- `match/page.tsx` — vendor sim bars, heatmap track
- `applications/page.tsx` — card text colors
- `AtsBreakdown.tsx` — issue cards
- `AssistantPanel.tsx` — chat bubble colors, chat container
- `JobCard.tsx` — muted text

## Verification

- `tsc --noEmit`: clean (0 errors)

*Related: [[active-goals]]*
