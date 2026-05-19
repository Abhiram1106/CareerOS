# platform/omnix/

Committed Omnix Runtime configuration: agents, workflows, commands, and
settings that ship with the repo so every collaborator gets the same Omnix
behaviour.

## Relationship to `.omnix/` and `.obsidian-ai-memory/`

| Location | Content | Tracked? |
|---|---|---|
| `.omnix/` (repo root) | Runtime cache + memory cache | **No** — gitignored |
| `platform/omnix/` (here) | Committed runtime config: agents, workflows, commands, settings | **Yes** |
| `.obsidian-ai-memory/` (repo root) | Long-term engineering memory vault: sessions, decisions, errors, architecture | **Yes** — committed per Omnix convention |

The split exists because Omnix originally puts everything under `.omnix/` for
discovery, but the *committed* parts (agents/workflows/commands/settings)
belong with the rest of the engineering platform under `platform/`. The
runtime cache stays at `.omnix/` per Omnix tooling expectations.

For now, the canonical sources still live at the repo root (`.omnix/agents/`,
`.omnix/workflows/`, `.omnix/commands/`, `.omnix/settings/`). This directory
exists as the **target** for those moves once Omnix tooling supports a
configurable committed-config path; until then it documents the intended
home.
