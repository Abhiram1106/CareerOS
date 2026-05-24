# Student Assistant — Privacy Notice

## Purpose

The assistant helps students understand resume quality, scoring signals, and workflow steps.

## Data usage

- Input messages may include resume/job context supplied by the user.
- Responses may use internal FAQ logic and configured model providers.
- Session data is handled under authenticated user scope.

## Guardrails

- No intentional fabrication of user facts.
- Prompt-injection defenses are applied before model calls.
- Sensitive account operations remain API-authenticated.

## Retention

Retention follows environment policy for logs and audit records.
