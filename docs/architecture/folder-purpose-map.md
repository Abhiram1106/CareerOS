# Folder Purpose Map

This map documents why each active folder exists after the student-only cleanup.

## Top-level folders

| Folder | Why it exists |
|---|---|
| `.claude/` | Local agent configs, rules, and skills metadata |
| `.cursor/` | Cursor workflow rules, memory workflow, and context docs |
| `.github/` | CI/CD and repository automation config |
| `.obsidian-ai-memory/` | Session continuity and project memory vault |
| `apps/` | Deployable application frontends |
| `docs/` | Product, architecture, security, ADR, and deployment documentation |
| `infra/` | Seed artifacts and infrastructure support files |
| `packages/` | Shared package code (notably scoring formula source of truth) |
| `platform/` | Platform-level configuration and support assets |
| `scripts/` | Utility scripts for setup, benchmark, and maintenance |
| `services/` | Backend runtime services (API + processing engines) |
| `tests/` | Cross-cutting and integration test assets |

## `apps/web` key folders

| Folder | Why it exists |
|---|---|
| `app/` | Next.js App Router pages and layouts |
| `components/` | Shared and page-composed UI components |
| `hooks/` | Shared client hooks used across features |
| `lib/` | API client and browser auth helpers |
| `modules/assistant/` | Student assistant hook/service/types |
| `modules/auth/` | Student auth service wrappers |
| `modules/intel/` | Intel benchmark panel hook/service/types |
| `modules/resume/` | Resume upload/export service wrappers |
| `modules/scorecard/` | JD scorecard service wrappers |

No empty placeholder module folders are kept.

## `services` key folders

| Folder | Why it exists |
|---|---|
| `core-api/` | Main FastAPI orchestration service |
| `resume-parser/` | Resume extraction and parsing |
| `ats-engine/` | ATS parse-safety heuristics |
| `ai-rewriter/` | Rewrite recommendation engine |
| `jobs-feed/` | Jobs ingestion and seed fallback |

## Migration state

| Path | Why it exists |
|---|---|
| `services/core-api/migrations/versions/0001_student_baseline.py` | Single Alembic baseline for fresh student-only setup |

No legacy split migrations remain in the versions directory.
