---
tags: [hub, index, moc, root]
type: hub
created: 2026-05-21
updated: 2026-05-21
---

# 🧠 CareerOS Campus AI — Vault Root

> **Master entry point.** Every note in this vault links back here.  
> Start here. Navigate outward. The graph radiates from this node.

---

## 🗺️ Domain Hubs (MOCs)

| Hub | Domain | What lives there |
|-----|--------|-----------------|
| [[MASTER_PLAN]] | Mission & Roadmap | Week goals, demo script, scoring target |
| [[architecture-index]] | System Design | Services, data model, layered arch |
| [[session-index]] | Work History | All session digests, chronological |
| [[api-index]] | API Contracts | Endpoints, DTOs, service clients |
| [[scoring-knowledge]] | The Formula | PlacementReadinessScore, sub-components |
| [[intel-index]] | Intel Integration | OpenVINO, sklearnex, benchmarks |
| [[errors-index]] | Bugs & Prevention | Error memory, anti-patterns, lessons |

---

## 📦 Cluster Map (Graph Communities)

```
          [_INDEX]  ← you are here
         /    |    \
[MASTER_PLAN] [architecture-index] [session-index]
     |              |    \              |
[scoring-knowledge] [api-index] [intel-index]  [errors-index]
     |              |                  |              |
  05-ARCH/      06-WORKFLOWS/     07-LESSONS/    03-ERRORS/
  layered-modules  procedures     debugging      anti-patterns
     |
  02-PROJECTS/
  active-goals · current-state · project-context · bootcamp-brief
```

---

## 🏛️ Tier 1 — Always Read First

- [[MEMORY-READ-PROTOCOL]] — How any AI tool reads this vault
- [[MEMORY-WRITE-PROTOCOL]] — How any AI tool writes to this vault
- [[02-PROJECTS/project-context]] — Master project snapshot
- [[02-PROJECTS/active-goals]] — Live week-by-week checklist
- [[02-PROJECTS/current-state]] — Exact verification state right now
- [[02-PROJECTS/session-continuity]] — Rolling cross-tool handoff

---

## 🏗️ Tier 2 — Architecture

- [[architecture-index]] ← MOC
- [[05-ARCHITECTURE/README]] — System diagram + data flows
- [[05-ARCHITECTURE/layered-modules]] — 7-phase refactor map
- [[05-ARCHITECTURE/frontend-ux]] — UI surfaces, components, styling
- [[04-DECISIONS/decisions]] — All 5 architectural decisions

---

## 🔬 Tier 3 — Intelligence Layer

- [[scoring-knowledge]] ← MOC
- [[intel-index]] ← MOC
- [[api-index]] ← MOC

---

## 🐛 Tier 4 — Error Knowledge

- [[errors-index]] ← MOC
- [[03-ERRORS/error-memory]] — Bug log (append-only)
- [[03-ERRORS/anti-patterns]] — Prevention rules
- [[07-LESSONS/debugging-lessons]] — Hard-won lessons

---

## 📅 Tier 5 — Sessions

- [[session-index]] ← MOC (all sessions)
- [[02-PROJECTS/vault-index]] — Quick file-lookup map

---

## 🔧 Tier 6 — Workflows & Templates

- [[06-WORKFLOWS/README]] — 7 step-by-step procedures
- [[templates/session-digest]] — Template for new sessions
- [[templates/error-entry]] — Template for bug logs
- [[templates/decision-entry]] — Template for decisions

---

## 🎯 Current Focus (Week 2)

> **Goal:** JD parser → match-engine → `packages/scoring/` → score UI  
> See [[MASTER_PLAN]] for full roadmap and [[02-PROJECTS/active-goals]] for checkboxes.

---

*Related: [[MASTER_PLAN]] · [[architecture-index]] · [[session-index]] · [[scoring-knowledge]] · [[intel-index]] · [[errors-index]] · [[api-index]]*
