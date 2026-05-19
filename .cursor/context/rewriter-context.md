# AI Rewriter Context — CareerOS Campus AI
# @include when working in services/ai-rewriter/ or on rewrite-related endpoints

## What the rewriter does

Takes structured inputs → returns structured JSON with section rewrites.
NEVER generates free-form text from scratch. NEVER fabricates facts.

## Inputs (strict schema)

```json
{
  "resume_json": { /* parsed sections from resume_sections table */ },
  "jd_json": { /* parsed JD from job_descriptions table */ },
  "evidence_json": { /* resume_evidence records for this resume */ },
  "ats_flags": ["flag1", "flag2"]
}
```

## Output schema (strict — no deviations)

```json
{
  "top_issues": [
    {"type": "ATS_FORMAT", "message": "Contact info in header", "severity": "high"}
  ],
  "section_rewrites": [
    {
      "section": "projects",
      "original": "Built a website using Python",
      "rewrite": "Built a Python-based web application for ___ using ___",
      "evidence_ids": ["proj_12"],
      "confidence": 0.81
    }
  ],
  "unsupported_claims": [
    {"claim": "Led a 5-member team", "reason": "No supporting evidence found"}
  ],
  "requires_confirmation": [
    {"field": "cgpa", "suggested_change": "Use 8.34 instead of rounded 8.3"}
  ]
}
```

## ABSOLUTE guardrails (enforced in system prompt)

The rewriter MUST NOT:
- Invent internships, projects, tools, metrics, percentages, or certifications
- Change CGPA, exam scores, dates, company names, or job titles without user confirmation
- Add "worked on AI/ML" if evidence only shows coursework
- Inflate role scope ("team member" → "team lead") without evidence
- Replace weak bullets with fabricated metrics

The rewriter MUST:
- Prefer rewriting existing content over generating new content
- Attach every `section_rewrites` entry to `evidence_ids[]`
- Return confidence score (0.0–1.0) per suggestion
- Put unsupported claims in `unsupported_claims[]` — never silently include them
- Preserve Indian academic context: CGPA format, X/XII board scores, semester references

## System prompt template (in services/ai-rewriter/app/main.py)

```xml
<system>
You are a placement-readiness resume editor for Indian college students.
Improve ATS safety and JD fit without fabricating facts.

Hard rules:
- Use only facts in <resume_json> and <evidence_json>.
- Never invent metrics, tools, certifications, team size, or ownership.
- If a bullet lacks measurable evidence, improve clarity but do not quantify.
- Keep output ATS-safe: no tables, icons, columns, or decorative language.
- Preserve Indian education context: CGPA, X/XII, semester, backlog.
- Return valid JSON matching the schema exactly.
</system>
```

## Storage

Rewriter output is stored in `recommendations` table:
- `rec_type`: "REWRITE" | "ATS_FORMAT" | "UNSUPPORTED" | "REQUIRES_CONFIRMATION"
- `evidence_ids`: JSON array of `resume_evidence.claim_id` strings
- `accepted`: null (pending) | true | false (after student decision)

## Current status (Week 1)

`services/ai-rewriter/app/main.py` still has the old template-fill generator.
Week 3 target: replace with the proof-linked rewriter using the schema above.
Do not add new features to the old template-fill logic.
