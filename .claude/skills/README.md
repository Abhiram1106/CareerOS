# .claude/skills/

Project-specific Claude Code skills (slash commands). Empty for now.

Add a project skill when there's a workflow specific to this repo that the
team wants reproducible via `/<skill-name>`, e.g.:

- `/score-resume` — run the PlacementReadinessScore pipeline on a fixture
- `/intel-bench` — kick off the Intel benchmark harness
- `/officer-demo` — seed the officer dashboard demo dataset

Format: `<skill-name>/SKILL.md` with YAML frontmatter (`name`, `description`).
