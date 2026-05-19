# platform/ci/

Reusable GitHub Actions composite actions and workflow templates. Actual
triggered workflows live at `.github/workflows/`; this directory holds the
pieces they compose.

Skeleton. First workflow (graph-affected PR check) lands in Week 1 once
schemas exist.

Pattern (research §"CI/CD"): path filter wakes the workflow → project graph
computes affected → cached build/lint/test/typecheck per affected project.
