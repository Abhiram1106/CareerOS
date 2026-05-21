---
tags: [hub, errors, bugs, prevention, moc]
type: moc
created: 2026-05-21
updated: 2026-05-21
links: [_INDEX, 03-ERRORS/error-memory, 03-ERRORS/anti-patterns, 07-LESSONS/debugging-lessons]
---

# 🐛 Errors Index — MOC

> Map of Content for bugs, prevention rules, and debugging lessons.  
> **Read this hub before diagnosing** — then drill into append-only logs.

← [[_INDEX]] | [[06-WORKFLOWS/README#Fixing a bug]]

---

## Bug log (append-only)

| Date | Incident | Symptom | Fix summary |
|------|----------|---------|-------------|
| 2026-05-19 | [[03-ERRORS/error-memory#2026-05-19 — `git mv` + post-rename Edit lost in single commit]] | Commit had rename but not content edits | `git add -u` before commit; verify `git show HEAD` |

→ Full log: [[03-ERRORS/error-memory]]

---

## Anti-patterns (prevention rules)

| Rule | Topic | Source lesson |
|------|-------|----------------|
| [[03-ERRORS/anti-patterns#Don't commit after `git mv` + edit without re-staging]] | Git staging | [[07-LESSONS/debugging-lessons#2026-05-19 — git mv + post-rename edit]] |
| [[03-ERRORS/anti-patterns#Don't blanket-ignore AI-tool directories]] | `.gitignore` | [[07-LESSONS/debugging-lessons#2026-05-19 — Blanket `.gitignore`]] |
| [[03-ERRORS/anti-patterns#Don't rewrite multiple files in parallel when they import each other]] | Python strip | Phase 1 core-api |
| [[03-ERRORS/anti-patterns#Don't commit `.tsbuildinfo`, `.pyc`, `*.db`, generated PDFs]] | Artefacts | Phase 1 cleanup |

→ Full list: [[03-ERRORS/anti-patterns]]

---

## Debugging lessons

| Lesson | Class |
|--------|-------|
| [[07-LESSONS/debugging-lessons#2026-05-19 — git mv + post-rename edit = silent content loss in commit]] | Git index vs working tree |
| [[07-LESSONS/debugging-lessons#2026-05-19 — Blanket `.gitignore` for AI config dirs loses team-shared files]] | Repo hygiene |

→ Template for new entries at bottom of [[07-LESSONS/debugging-lessons]]

---

## Before every commit — checklist

1. Read [[03-ERRORS/error-memory]] — is this bug already known?
2. Read [[03-ERRORS/anti-patterns]] — any rule violated?
3. After `git mv` + edits: **`git add -u`** then `git diff --cached --stat`
4. Verify intended paths: `git show HEAD -- <path>` for critical files
5. No secrets in diff; no `.db` / `.tsbuildinfo` / generated PDFs staged
6. `tsc --noEmit` (apps/web) + Python AST parse (touched services)
7. One concern per commit on `main` — trunk must stay buildable ([[04-DECISIONS/decisions]])
8. Memory vs code: separate commits — [[MEMORY-WRITE-PROTOCOL]]

---

## Workflow integration

| Task | Procedure |
|------|-----------|
| Fix a bug | [[06-WORKFLOWS/README#Fixing a bug]] |
| Add endpoint | [[06-WORKFLOWS/README#Adding a new FastAPI endpoint]] |
| Layered migration | [[05-ARCHITECTURE/layered-modules]] |

---

## Graph cluster

```
errors-index (this note)
    ├── 03-ERRORS/error-memory
    ├── 03-ERRORS/anti-patterns
    └── 07-LESSONS/debugging-lessons
```

Linked from [[_INDEX#Tier 4 — Error Knowledge]].

---

*Related: [[_INDEX]] · [[03-ERRORS/error-memory]] · [[03-ERRORS/anti-patterns]] · [[07-LESSONS/debugging-lessons]] · [[06-WORKFLOWS/README]] · [[MEMORY-WRITE-PROTOCOL]]*
