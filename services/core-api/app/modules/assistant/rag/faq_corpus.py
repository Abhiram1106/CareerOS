from __future__ import annotations

FAQ_CHUNKS: list[dict[str, str]] = [
    {
        "id": "upload-resume",
        "text": (
            "Upload your resume on the Workspace Document Intelligence tab. "
            "CareerOS parses PDF or DOCX, extracts sections, and flags ATS parse-safety issues."
        ),
    },
    {
        "id": "jd-match",
        "text": (
            "Run a JD Match Scan by pasting a job description on the Workspace scan tab. "
            "You receive PlacementReadinessScore with JD match, ATS safety, and evidence quality."
        ),
    },
    {
        "id": "proof-rewrite",
        "text": (
            "Proof-linked rewrite suggests bullet improvements tied to evidence in your resume. "
            "Unsupported claims appear in unsupported_claims — never fabricate metrics."
        ),
    },
    {
        "id": "builder-jobs",
        "text": (
            "Builder Wizard helps structure a fresher resume. Jobs Feed shows curated roles "
            "matched to your skills — run the agent from a job card for an end-to-end pass."
        ),
    },
    {
        "id": "score-buckets",
        "text": (
            "Readiness buckets: 0–49 high risk, 50–69 borderline, 70–84 ready, 85–100 strong. "
            "Improve JD match and ATS parse safety first for the biggest gains."
        ),
    },
    {
        "id": "intel-lab",
        "text": (
            "Intel Performance Lab shows measured sklearnex and OpenVINO benchmarks only — "
            "never vendor headline numbers. Run services/intel-bench/run.py on target hardware."
        ),
    },
]
