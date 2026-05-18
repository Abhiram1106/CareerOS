# CLAUDE.md — Omnix

> Claude Code reads this file on every session.

@AGENTS.md

## Claude Code-specific settings

**Memory retrieval mode:** balanced by default. Switch to `deep` for architecture changes, `debugging` for error investigation, `minimal` for one-liner answers.

**Active skills** (uncomment to activate):
<!-- @packages/core/skills/debugging-specialist/SKILL.md -->
<!-- @packages/core/skills/test-architect/SKILL.md -->
<!-- @packages/core/skills/security-threat-modeler/SKILL.md -->
<!-- @packages/core/skills/context-manager/SKILL.md -->

**Completion gate — do not say "done" until:**
- [ ] Changed files are correct and match intent
- [ ] Tests/typecheck ran (state result or reason skipped)
- [ ] Docs updated if behavior changed
- [ ] Session digest written (skip only for read-only sessions)
- [ ] Error memory updated if a bug was fixed
- [ ] No secrets in any written file
- [ ] Open risks listed if any remain
