# 06 — Frontend Guide

## Tech stack

- **Next.js 14** App Router — default server components, `"use client"` only when needed
- **TypeScript strict** — `strict: true`, no `any`
- **CSS variables** — dark/light tokens in `globals.css`, no Tailwind, no CSS-in-JS
- **pnpm 9** — package manager

---

## Route map

```
/                    → redirects to /dashboard (if auth'd) or /login
/login               → JWT email/password form
/register            → student registration
/reset-password      → two-stage password reset (request → confirm)

/dashboard           → career overview: score ring, checklist, gap callout
/resume              → upload, parse, ATS flags, template select, export
/match               → paste JD, run score, view 6-bar breakdown + ATS issues
/rewrite             → proof-linked diff panel, unsupported claims
/jobs                → job search by role + location
/assistant           → grounded FAQ chatbot
/settings            → profile editor (basic + eligibility + social links)
/lab/intel           → Intel benchmark panel
/privacy/assistant   → assistant privacy notice
```

Legacy workspace routes redirect:
- `/workspace` → `/dashboard`
- `/workspace/jobs` → `/jobs`
- `/workspace/builder` → `/dashboard`

---

## Layout (`app/(app)/layout.tsx`)

Shell for all protected routes:
- **Sidebar rail** (desktop): CO brand → primary nav links → secondary nav (Intel Lab, Settings)
- **Bottom nav** (mobile): icon + label for primary routes
- **Top bar**: profile completeness ring (reads from `/dashboard`) + user pill + sign out
- Auth check: `getStoredAuth()` → if null, redirect to `/login`
- Toast system: `useToast()` hook, `push({title, message, variant})` pattern

---

## State management

**Auth** (`lib/auth.ts`):
```typescript
getStoredAuth()    // returns {token, email, full_name, role} or null
storeAuth(user)    // saves to localStorage
clearAuth()        // removes from localStorage
```

**Workspace state** (`hooks/usePlacementWorkspace.ts`):
Central hook for the resume→score→rewrite flow. Persists to localStorage key `cos_workspace_state_v1`:
- `resume_id`, `jd_text`, `tab`, `score_snapshot`, `export_status`
- Returns: `parseResult`, `barScores`, `overallScore`, `rewriteBundle`, `agentRun`, etc.

**Assistant chat** (`modules/assistant/useAssistantChat.ts`):
Persists up to 20 messages to localStorage key `cos_assistant_chat_v1`.

---

## API layer (`lib/api.ts`)

**The only place HTTP calls are made.** Every endpoint has a typed wrapper function.

Pattern:
```typescript
// READ — no body, needs token
api.getProfile(token)

// WRITE — body, needs token
api.addWorkExp(token, { company: "Razorpay", title: "Intern", ... })

// Upload — multipart
api.uploadResume(token, file)
```

Requests go to `NEXT_PUBLIC_CORE_API_URL` (default `http://localhost:8000`).
Auth header attached centrally — never in components.

---

## CSS system (`globals.css`)

Design tokens:
```css
--bg: #eef0f3           /* page background */
--surface: #ffffff       /* card surface */
--ink: #0f1419          /* primary text */
--muted: #5c6570        /* secondary text */
--accent: #1a3a5c       /* brand navy */
--intel: #0071c5        /* Intel blue (used in scoring UI) */
```

Key utility classes:
```css
.page-canvas           /* page wrapper with consistent padding */
.content-card          /* white card with shadow */
.content-card-header   /* card title row */
.content-card-body     /* card body padding */
.page-title            /* H1 style */
.page-subtitle         /* subtitle style */
.btn-primary           /* blue CTA button */
.btn-secondary         /* ghost button */
.chip                  /* small badge */
.auth-input            /* form input */
.auth-label            /* form label */
```

Inline `style={{}}` is acceptable for one-off spacing. New reusable patterns go in `globals.css`.

---

## Component patterns

**Score display** (`components/workspace/ScoreBreakdown.tsx`):
- Takes `barScores`, `overallScore`, `scoreBucket`, `semanticMethod`
- Shows overall ring + 6 component bars + method note
- Tooltip on JD Match bar shows the formula

**ATS breakdown** (`components/workspace/AtsBreakdown.tsx`):
- Takes `ats_checks` and `ats_issues` from scorecard response
- Shows dimension scores + actionable issue list

**Rewrite diff** (`components/workspace/RewriteDiffPanel.tsx`):
- Shows original vs rewrite per bullet
- Highlights unsupported claims in red
- "Run rewrite" button when no bundle yet

**Toast** (`components/ui/toast.tsx`):
```typescript
const { push } = useToast();
push({ title: "Saved", variant: "success" });
push({ title: "Error", message: err.message, variant: "error" });
```

---

## Adding a new page

```typescript
// apps/web/app/(app)/my-feature/page.tsx
"use client";

import { useEffect, useState } from "react";
import { api } from "../../../lib/api";
import { getStoredAuth } from "../../../lib/auth";

export default function MyFeaturePage() {
  const token = getStoredAuth()?.token ?? "";
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!token) return;
    void api.someEndpoint(token).then(setData);
  }, [token]);

  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <h1 className="page-title">My Feature</h1>
      </div>
      {/* content */}
    </div>
  );
}
```

Then add to `PRIMARY_NAV` in `app/(app)/layout.tsx`.
