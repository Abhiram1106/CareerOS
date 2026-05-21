# Cursor memory workflow — every chat

> **Mandatory for Cursor agents.** Complements root `AGENTS.md` and
> `.obsidian-ai-memory/MEMORY-WRITE-PROTOCOL.md`.
> Goal: **maximum context + traceability** across chats without re-explaining the repo.

---

## The contract

| When | What |
|------|------|
| **Start of chat** | Read memory (startup) + read `02-PROJECTS/session-continuity.md` first |
| **End of every chat** | Shutdown protocol below — **before** your final message to the user |

Skipping shutdown is only allowed when the chat was **pure Q&A with zero file reads/writes**
and the user did not ask for implementation. When in doubt, run shutdown.

---

## Startup (beginning of chat)

1. Read `.obsidian-ai-memory/02-PROJECTS/session-continuity.md` — **rolling handoff from last chat**
2. Read `project-context.md`, `active-goals.md`, `error-memory.md`, `anti-patterns.md`
3. Read `vault-index.md` — locate latest session file
4. Read **last 1–3** files in `01-SESSIONS/` (newest dates first)
5. Load `.cursor/context/*` for the area you will touch
6. Emit startup block (see `.cursor/AGENTS.md`)

---

## Shutdown (end of every chat) — do not skip

Execute in order. State what you did in your final reply (2–4 lines under **Memory**).

### 1. Session digest

| Situation | Action |
|-----------|--------|
| **New topic or first chat of the day** | Create `01-SESSIONS/YYYY-MM-DD/session-HHMM-cursor.md` from `templates/session-digest.md` |
| **Same day, same thread, short follow-up** | Append `## Chat follow-up — HH:MM` to **today’s latest** `session-*-cursor.md` |
| **This chat only changed docs/memory** | Still write digest; type = `docs` |

Minimum fields: user request, files changed, verification (tsc / Python AST), next 3 tasks.

### 2. Rolling continuity (chat-to-chat)

**Overwrite** `.obsidian-ai-memory/02-PROJECTS/session-continuity.md` using
`templates/session-continuity.md`.

This file is the **fast path** for the next Cursor chat — one screen of context.

### 3. Other vault updates (if applicable)

| Trigger | File |
|---------|------|
| Behaviour / phase changed | `02-PROJECTS/current-state.md` |
| Architecture changed | `05-ARCHITECTURE/*`, `docs/architecture/*` |
| Bug fixed | `03-ERRORS/error-memory.md` (append) |
| Decision made | `04-DECISIONS/decisions.md` (append) |
| Goal done | `02-PROJECTS/active-goals.md` `[x]` |
| New session row | `02-PROJECTS/vault-index.md` |

### 4. `.cursor` context (if layout or conventions changed)

Update the relevant file under `.cursor/context/` so Cursor rules stay truthful.

### 5. Git commit — memory only

**Separate commit** from code. User may say “no commit”; otherwise **always commit vault** at shutdown.

```bash
git add .obsidian-ai-memory/
git status
git commit -m "memory: YYYY-MM-DD cursor — <one-line summary>"
```

Commit message examples:

- `memory: 2026-05-21 cursor — phase 3 profile migration`
- `memory: 2026-05-21 cursor — cursor memory workflow docs`

**Do not** bundle unrelated code changes in the memory commit. Code commits stay one concern each.

### 6. Final user message must include

```markdown
## Memory
- Digest: `01-SESSIONS/.../session-HHMM-cursor.md` (created | appended)
- Continuity: `02-PROJECTS/session-continuity.md` updated
- Vault commit: `<hash or "skipped per user">`
- Next chat should start with: (one sentence)
```

---

## Traceability map

```
Chat N ends
  → session-continuity.md     (snapshot for Chat N+1 startup)
  → session-HHMM-cursor.md    (audit trail / full detail)
  → vault-index.md            (index of all sessions)
  → git log --grep="memory:"  (who wrote what when)
```

---

## Checklist (copy into digest)

```markdown
## Shutdown checklist
- [ ] session-continuity.md updated
- [ ] session digest created or appended
- [ ] vault-index.md updated
- [ ] current-state / architecture / errors (if needed)
- [ ] .cursor/context updated (if needed)
- [ ] memory commit pushed or user declined
```

---

## References

- Full write rules: `.obsidian-ai-memory/MEMORY-WRITE-PROTOCOL.md`
- Digest template: `.obsidian-ai-memory/templates/session-digest.md`
- Continuity template: `.obsidian-ai-memory/templates/session-continuity.md`
- Cursor agents: `.cursor/AGENTS.md`
