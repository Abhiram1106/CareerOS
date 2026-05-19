# Anti-patterns

> Prevention rules promoted from recurring errors. Each entry references the
> incident in `error-memory.md`.

---

## Don't commit after `git mv` + edit without re-staging

When restructuring a tree with `git mv` followed by content edits on the
moved files, **always run `git add -u` before `git commit`**. The rename is
staged at mv time; the subsequent edits are not. A commit at this point
captures only the move with the original content, silently losing the edits.

**Verify** with `git show HEAD -- <edited-path>` before declaring done.

**Source**: `error-memory.md` → 2026-05-19 incident during Phase 1 restructure.

---

## Don't blanket-ignore AI-tool directories

`.gitignore` patterns like `.claude/`, `.omnix/`, `.cursor/`,
`.obsidian-ai-memory/` look reasonable but lose the **team-shared** parts.
The right pattern is **track committed config, ignore personal runtime
caches**:

```gitignore
# Omnix
.omnix/memory/
.omnix/cache/
# Cursor
.cursor/*
!.cursor/rules/
!.cursor/rules/**
# Claude
.claude/settings.local.json
.claude/CLAUDE.local.md
# Obsidian-AI memory vault — fully tracked (intentionally not ignored)
```

**Source**: 2026-05-19 Phase 2 — first-pass `.gitignore` had `.claude/` and
`.obsidian-ai-memory/` blanket-ignored; corrected before commit.

---

## Don't rewrite multiple files in parallel when they import each other

When stripping a large surface (e.g. core-api: main.py + entities.py +
clients.py + schemas/contracts.py + workers/tasks.py + celery_app.py +
config.py + migrations/0001), do edits **sequentially** and AST-parse the
whole tree at the end before committing. Parallel `Write` calls on
interdependent Python files risk one file referencing symbols another file
hasn't dropped yet, and the failure mode is import-time at runtime, not at
edit time.

**Source**: Phase 1 strip on `services/core-api/` (2026-05-19). Avoided by
doing the rewrites sequentially and running `python -c "ast.parse(...)"`
across all touched files before committing.

---

## Don't commit `.tsbuildinfo`, `.pyc`, `*.db`, generated PDFs

These are build/runtime artefacts. They blow up diff size, leak local state
(SQLite contents), and break reproducibility. Gitignore covers them now —
verify with `git status --ignored` before each new file type.

**Source**: Phase 1 surfaced committed `*.db` and PDF exports from the
pre-pivot MVP. Removed and gitignored.
