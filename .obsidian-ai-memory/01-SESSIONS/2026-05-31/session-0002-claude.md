---
date: 2026-05-31
tool: claude-code
model: claude-sonnet-4-6
tags: [session, phase5, rewriter, anti-fabrication, rule-based]
type: session
links: [error-memory, active-goals, scoring-knowledge]
---

# Session 2026-05-31 (3) — Phase 5: Rewriter rebuilt

← [[_INDEX]] · [[error-memory]] · [[active-goals]]

## What was done

### Phase 5 — Rule-based rewriter rebuilt (no LLM, no fabrication)

**Decision:** Keep as rule-based (user chose this over LLM). Make it actually good.

**Problems with old rewriter:**
- `_improve_bullet` blindly prepended "Developed" to every bullet
- Appended the first JD skill regardless of whether bullet was already tech-specific
- Only 2 unsupported claim patterns (metrics + leadership) — missed superlatives
- `confidence` hardcoded 0.72/0.55 — meaningless
- `top_issues` only covered 5 ATS flags with no fix guidance
- `generate_resume_handler` returned identical boilerplate for all users

**What was rebuilt:**

`proof_linked_rewrite_handler.py`:
- 30-verb `_STRONG_VERBS` set including leadership verbs (led, owned, directed)
- `_WEAK_OPENERS` dict: 9 specific upgrades ("worked on"→"Developed", etc.)
- `_FILLER_RE`: 15 generic phrases; broken fragments → placeholder (not garbled text)
- `_SUPERLATIVE_RE`: 14 unverifiable claims flagged (best, pioneered, world-class)
- `_TECH_TERM_RE`: prevents skill appending when bullet already tech-specific
- Unsupported bullets emitted unchanged with confidence=0.0 — never rewritten
- Metric flagging only when evidence_json explicitly provided (not on every metric)
- `_compute_confidence`: signal-derived (verb + metric + evidence + length)
- 16 ATS flags → full human-readable message + actionable fix
- Top issues sorted high→medium→low, deduplicated

`generate_resume_handler.py`:
- Uses all profile fields (name, role, city, skills, summary, experience)
- [Bracketed placeholders] when fields empty — tells student what to write
- Skills rendered in grouped columns; experience split into per-bullet lines

**Bugs fixed during development:**
1. `_strip_filler` stripped "and" globally → "Python and FastAPI" → "Python FastAPI"
   Fix: only remove connectors when filler was actually removed
2. Superlative bullets were being rewritten (wrong) → now emitted as-is
3. "Led" not in `_STRONG_VERBS` → double-prefix "Developed led a team"
4. Metric flagged as unsupported even with no evidence payload provided
5. Skill appended to "Reduced query time by 35% using Redis" (already has tech term)

**8/8 correctness cases: ALL PASS**

---

### Files changed
- `services/ai-rewriter/app/modules/rewrite/mutation/proof_linked_rewrite_handler.py`
- `services/ai-rewriter/app/modules/rewrite/mutation/generate_resume_handler.py`

### Verified end-to-end
- Scorecard: `semantic_method: sentence_embedding` ✅ (Phase 3 still live)
- Rewrite: strong bullet unchanged (conf 0.65), bare bullet gets metric placeholder
- Unsupported claim: superlative flagged, bullet emitted unchanged

---

## What's next

- **Phase 6** — Frontend honesty + continuity fixes
- **Phase 7** — Full regression + benchmark docs + final memory commit

---

*Related: [[error-memory]] · [[active-goals]] · [[scoring-knowledge]]*
