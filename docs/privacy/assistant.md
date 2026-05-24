# Campus Assistant — privacy notice

## What we send

- **FAQ mode (default):** Your question is matched against static product FAQ text on our server. No third-party LLM is called.
- **Optional LLM mode:** When `LLM_API_KEY` is configured server-side, we send:
  - Retrieved FAQ excerpts
  - Anonymized score bands (overall, bucket, JD match, ATS safety) — not resume text or scorecard IDs
  - Your question inside a delimited block

## What we do not send

- Full resume text
- Email, phone, or other profile PII
- Other students' data

## Logging

- Audit events record provider, source ids, and message length — not full chat bodies in application logs.
- Prompt-injection patterns are rejected before any LLM call.

## Your controls

- Assistant requires student login (JWT).
- Answers include suggested links only — no autonomous writes to your resume.
