# Debugging Lessons — CareerOS Campus AI

> Hard-won lessons from debugging sessions. Loaded by AI tools during
> error diagnosis tasks (deep mode). Append new lessons as they are learned.

---

## 2026-05-19 — git mv + post-rename edit = silent content loss in commit

**Context**: Restructuring `frontend/` → `apps/web/` with `git mv`, then
editing files in the new location before committing.

**What happened**: `git mv` stages the rename. Subsequent `Write`/`Edit` on
the moved file modifies the working tree but does NOT auto-stage that edit.
Running `git commit` without `git add -u` first commits the original content
under the new path — the edits are silently lost.

**How to detect**: `git show HEAD -- <path>` shows the original content.
`git diff HEAD -- <path>` shows the edits still uncommitted.

**Fix**: `git add -u` (or `git add <specific paths>`) AFTER editing renamed
files, BEFORE `git commit`.

**Prevention rule**: After any `git mv` + content edit, always run
`git add -u` and verify with `git diff --cached --stat` before committing.

**Class of error**: git staging model — the index tracks renames separately
from content changes. Both must be staged to commit both.

---

## 2026-05-19 — Blanket `.gitignore` for AI config dirs loses team-shared files

**Context**: Added `.claude/`, `.omnix/`, `.obsidian-ai-memory/` to
`.gitignore` to keep AI tool runtime state out of the repo.

**What happened**: The gitignore was too broad — it also excluded the
_team-shared_ config files (CLAUDE.md, rules/, agents/, settings.json,
the full memory vault) that MUST be committed for cross-platform coherence.

**Fix**: Granular gitignore — track shared config, ignore only runtime
caches and personal overrides:
```gitignore
.omnix/memory/
.omnix/cache/
.cursor/*
!.cursor/rules/
!.cursor/rules/**
.claude/settings.local.json
.claude/CLAUDE.local.md
```
The full `.obsidian-ai-memory/` vault is tracked (not ignored).

**Prevention rule**: Never blanket-ignore AI tool directories. Always
distinguish between runtime cache (ignore) and team-shared config (track).

---

## Template: new lesson

**Context**: ___

**What happened**: ___

**How to detect**: ___

**Fix**: ___

**Prevention rule**: ___

**Class of error**: ___

---

_Append new lessons here after every debugging session that reveals a non-obvious root cause._
_Last updated: 2026-05-19_
