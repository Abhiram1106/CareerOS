# .claude/agents/

Project-specific Claude Code subagents. Empty for now — all agents come from
the global library.

Add a project subagent when:
- A task pattern is specific to this codebase (e.g. "validate a
  PlacementReadinessScore implementation against `packages/scoring/`").
- A global agent's instructions repeatedly need to be re-specialized for
  CareerOS.

Format: `<agent-name>.md` with YAML frontmatter (`name`, `description`,
`tools`). Reference from root `CLAUDE.md` / `AGENTS.md` when stable.
