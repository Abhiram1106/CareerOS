# AI Rewriter Context — CareerOS Student AI
# @include when working in `services/ai-rewriter/`

## Purpose

Transform resume bullets into clearer, ATS-safer, JD-aligned alternatives without inventing facts.

## Input contract

- `resume_json`
- `jd_json`
- `evidence_json`
- `ats_flags`

## Output contract

- `top_issues`
- `section_rewrites[]` with evidence IDs and confidence
- `unsupported_claims[]`
- `requires_confirmation[]`

## Hard guardrails

- Never fabricate projects, metrics, ownership, dates, or credentials.
- Never change factual claims without user confirmation.
- Every rewrite must be grounded in provided evidence.
- Unsupported claims must be explicit in `unsupported_claims`.

## Storage target

Rewrite outputs persist in `recommendations` with evidence linkage and acceptance state.
