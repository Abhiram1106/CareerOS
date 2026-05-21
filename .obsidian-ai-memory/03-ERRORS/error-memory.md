---
tags: [errors, bugs, append-only]
type: error-log
updated: 2026-05-21
links: [errors-index, 03-ERRORS/anti-patterns]
---

# Error Memory

← [[errors-index]] · [[03-ERRORS/anti-patterns]]

> Log fixed bugs and how. Check this before diagnosing anything.

---

## 2026-05-19 — `git mv` + post-rename Edit lost in single commit

**Symptom**: After `git mv frontend/ apps/web/` followed by `Write`/`Edit` to
the moved files, the resulting commit captured only the renames — the content
edits were absent because they weren't re-staged before `git commit`. Git
showed the commit as `+0 -0` net change on edited paths.

**Root cause**: `git mv` stages the rename. Subsequent `Write`/`Edit`
modifies the working tree but does NOT auto-stage the change. `git commit`
without an explicit `git add -u` only commits what's in the index, which at
that point is the *original* content under the new path.

**Fix**: After post-rename edits, `git add -u` (or `git add <paths>`)
**before** `git commit`. Verified by `git show HEAD -- <path>` showing the
intended diff.

**Prevention**: see [[03-ERRORS/anti-patterns#Don't commit after `git mv` + edit without re-staging]].

---

*Related: [[errors-index]] · [[03-ERRORS/anti-patterns]] · [[07-LESSONS/debugging-lessons]] · [[06-WORKFLOWS/README#Fixing a bug]]*
