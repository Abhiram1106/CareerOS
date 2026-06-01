# 03 — Codebase Guide

## Monorepo layout

```
CareerOS/
├── apps/
│   └── web/                          Next.js 14 (TypeScript strict)
│       ├── app/
│       │   ├── (app)/                Protected routes (require JWT)
│       │   │   ├── dashboard/        Career overview page
│       │   │   ├── resume/           Upload + parse + export
│       │   │   ├── match/            JD scoring
│       │   │   ├── rewrite/          Proof-linked rewrites
│       │   │   ├── jobs/             Job search
│       │   │   ├── assistant/        FAQ chatbot
│       │   │   └── settings/         Profile editor
│       │   ├── (auth)/               Unauthenticated routes
│       │   │   ├── login/
│       │   │   ├── register/
│       │   │   └── reset-password/
│       │   └── layout.tsx            Root HTML shell
│       ├── components/
│       │   ├── ui/                   Primitives (toast, etc.)
│       │   ├── workspace/            Feature components (ScoreBreakdown, RewriteDiffPanel, etc.)
│       │   └── intel/                Intel benchmark panel components
│       ├── hooks/
│       │   └── usePlacementWorkspace.ts   Master workspace state hook
│       ├── lib/
│       │   ├── api.ts                All HTTP calls — ONLY place to call the API
│       │   ├── auth.ts               JWT localStorage helpers
│       │   ├── errors.ts             Error message extractor
│       │   └── placement.ts          Score component config
│       └── modules/
│           ├── auth/                 Auth service + types
│           ├── assistant/            Chat hook + service
│           └── intel/                Benchmark hook + service
│
├── services/
│   ├── core-api/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   ├── controllers/      Route handlers (slim — delegate to handlers)
│   │   │   │   └── router.py         Mounts all routers
│   │   │   ├── modules/
│   │   │   │   ├── auth/             register, login, logout, reset
│   │   │   │   ├── profile/          basic profile + sections DTOs/handlers
│   │   │   │   ├── resume/           upload, generate, export
│   │   │   │   ├── scorecard/        score computation
│   │   │   │   ├── recommendation/   rewrite + history
│   │   │   │   ├── jd/               JD parse
│   │   │   │   ├── jobs/             job search proxy
│   │   │   │   ├── dashboard/        aggregated metrics
│   │   │   │   ├── ats/              ATS scan + history
│   │   │   │   └── agent/            deterministic agent run
│   │   │   ├── adapter/db/
│   │   │   │   └── persistence/      Repos (UserRepo, WorkExpRepo, etc.)
│   │   │   ├── models/
│   │   │   │   └── entities.py       All SQLAlchemy mapped entities
│   │   │   ├── services/
│   │   │   │   ├── clients.py        All inter-service HTTP calls
│   │   │   │   ├── auth.py           JWT + bcrypt helpers
│   │   │   │   ├── audit.py          EventAudit logger
│   │   │   │   └── pdf_export.py     WeasyPrint + fallback
│   │   │   ├── dependencies.py       FastAPI DI exports
│   │   │   ├── handler_dependencies.py  Handler factories
│   │   │   └── config.py             Env var reads
│   │   └── migrations/versions/      Alembic migration files
│   │
│   ├── resume-parser/app/
│   │   ├── parsers.py                extract_pdf, extract_docx, ocr_pdf
│   │   └── extractor.py              split_into_sections, _extract_ats_flags
│   │
│   ├── match-engine/app/
│   │   ├── matcher.py                compute_match (TF-IDF + embedding)
│   │   ├── embedder.py               Backend selector (OpenVINO > PyTorch > fallback)
│   │   ├── skill_taxonomy.py         70 skills + 50 aliases + span-claimed matching
│   │   ├── jd_parser.py              Rule-based JD skill + eligibility extraction
│   │   └── intel_patch.py            patch_sklearn_if_available()
│   │
│   ├── ats-engine/app/modules/ats/mutation/
│   │   └── parse_safety_handler.py   Routes to analyze_ats (text path) or flag path
│   │
│   └── ai-rewriter/app/modules/rewrite/mutation/
│       ├── proof_linked_rewrite_handler.py
│       └── generate_resume_handler.py
│
├── packages/
│   └── scoring/careeros_scoring/
│       ├── formula.py                compute_placement_readiness, compute_jd_match
│       ├── parse_safety.py           analyze_ats (7-dimension), ats_parse_safety_from_flags
│       └── resume_components.py      evidence_quality, interview_readiness, placement_hygiene, profile_completeness
│
├── tests/golden/
│   ├── corpus.py                     7 resume personas
│   ├── _runner.py                    Discrimination gate script
│   └── _audit_phase4.py              21 sub-score correctness tests
│
└── docs/
    ├── handoff/                      ← teammate onboarding (this folder)
    ├── benchmarks/                   Intel performance measurements
    └── CareerOS_Complete_Documentation.md  Full product vision
```

---

## Layered architecture (backend)

Every feature follows the same pattern. Never skip layers.

```
Controller (api/controllers/)   ← validate input, call handler, return response
    ↓
Handler (modules/.../mutation/) ← business logic, calls repos + services
    ↓
Repository (adapter/db/)        ← database reads/writes only
    ↓
Entity (models/entities.py)     ← SQLAlchemy mapped class
```

For reads:
```
Controller → QueryService → View (read-only repo) → Entity
```

---

## Python conventions

- **SQLAlchemy 2.0** mapped-column style: `Mapped[T]` / `mapped_column(...)` — never `Column()`
- **Pydantic v2**: `model_dump()` not `.dict()`, `model_validate()` not `.parse_obj()`
- **FastAPI handlers stay slim** — one job: validate, delegate, return
- **All cross-service HTTP** via `services/core-api/app/services/clients.py` (httpx, never requests)
- **Schema changes** → Alembic migration file, never `entities.py` alone
- **sklearnex** must be patched before any sklearn import (see `intel_patch.py`)

---

## TypeScript conventions

- `strict: true` — no `any`. Unknown → `unknown`, then narrow
- `"use client"` only when the file needs hooks, browser APIs, or event handlers. Default: server component
- **All HTTP via `apps/web/lib/api.ts`** — never `fetch()` inline in components
- **No Tailwind, no CSS-in-JS** — CSS variables in `apps/web/app/globals.css`
- `CardSection`, `FormField`, `MetricTile` from `apps/web/components/ui/primitives.tsx` first

---

## Adding a new backend endpoint

1. Add entity fields to `entities.py` + Alembic migration
2. Add DTO in `modules/<domain>/dto/`
3. Add handler in `modules/<domain>/mutation/` or `query/`
4. Add repo method in `adapter/db/persistence/`
5. Add controller route in `api/controllers/`
6. Mount router in `api/router.py`
7. Add typed wrapper in `apps/web/lib/api.ts`
8. Run `tsc --noEmit` — must be clean

---

## Adding a new frontend page

1. Create `apps/web/app/(app)/<route>/page.tsx`
2. Add nav link in `apps/web/app/(app)/layout.tsx` PRIMARY_NAV array
3. Use `getStoredAuth()` for the token — never hardcode
4. All API calls via `api.<method>(token, ...)` from `lib/api.ts`
5. CSS classes from `globals.css` — no inline styles for reusable components
