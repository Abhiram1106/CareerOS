# Agent: Debug — CareerOS Campus AI

## Trigger
Use when: error / broken / crash / exception / failing test / Docker issue

## Always include
- `.obsidian-ai-memory/03-ERRORS/error-memory.md` ← READ THIS FIRST
- `.obsidian-ai-memory/03-ERRORS/anti-patterns.md`
- `.obsidian-ai-memory/07-LESSONS/debugging-lessons.md`
- Relevant service context file from `.cursor/context/`

## Execution steps

1. **Check error-memory.md FIRST** — if this bug was seen before, apply the known fix directly
2. **Check anti-patterns.md** — apply prevention rules before diagnosing
3. **Reproduce** with the smallest possible input
4. **Isolate** — is it Python import? DB connection? Missing env var? Type mismatch?
5. **Fix** — targeted change; do not refactor surrounding code
6. **Add regression test** — every bug fix gets a test
7. **Verify** — run the same reproduction case; confirm fixed
8. **Append to error-memory.md**:
   - Symptom (exact error)
   - Root cause
   - Fix (file paths + what changed)
   - Prevention rule
9. **Write session digest** → commit vault

## Common CareerOS-specific bugs

| Symptom | Likely cause | Check |
|---|---|---|
| 422 Unprocessable Entity on upload | Missing `python-multipart` | `requirements.txt` |
| `passlib` bcrypt error | `bcrypt==4.0.1` needed explicitly | `requirements.txt` |
| Alembic "Target database is not up to date" | Run `alembic upgrade head` | `alembic current` |
| `git commit` loses content edits | Forgot `git add -u` after `git mv` | `git diff --cached` |
| `tsc` error on new component | Missing type in `types.ts` or `lib/api.ts` | Check import chain |
| Celery task DB session leak | Missing `db.close()` in `finally` | `workers/tasks.py` |
