"""Self-contained discrimination runner (no pytest dependency).

Mirrors the assertions in ``test_discrimination.py`` but runs as a plain script
inside the core-api container via ``run_in_container.sh``. Exits non-zero if any
sub-score fails the spread / distinct-value / ordering gates, so it can act as a
CI gate.
"""

from __future__ import annotations

import statistics
import sys

sys.path.insert(0, "/tmp")
import corpus  # noqa: E402

from careeros_scoring import (  # noqa: E402
    analyze_ats,
    evidence_quality_score,
    interview_readiness_score,
    placement_hygiene_score,
    profile_completeness_score,
)

MIN_SPREAD = 30.0
MIN_DISTINCT = 5

SUBSCORES = {
    "ats_parse_safety": lambda p: analyze_ats(p.text, [])["ats_parse_safety"],
    "evidence_quality": lambda p: evidence_quality_score(p.sections),
    "interview_readiness": lambda p: interview_readiness_score(p.sections),
    "placement_hygiene": lambda p: placement_hygiene_score(p.sections, []),
    "profile_completeness": lambda p: profile_completeness_score(p.sections),
}


def main() -> int:
    failures: list[str] = []
    print(f"{'subscore':22} {'spread':>7} {'distinct':>9}  result  values")
    print("-" * 78)
    for name, fn in SUBSCORES.items():
        values = [round(fn(p), 1) for p in corpus.ALL_PERSONAS]
        spread = max(values) - min(values)
        distinct = len(set(values))

        strong = statistics.mean(fn(p) for p in corpus.ALL_PERSONAS if p.tier == "strong")
        weak = statistics.mean(fn(p) for p in corpus.ALL_PERSONAS if p.tier == "weak")

        reasons = []
        if spread < MIN_SPREAD:
            reasons.append(f"spread<{MIN_SPREAD}")
        if distinct < MIN_DISTINCT:
            reasons.append(f"distinct<{MIN_DISTINCT}")
        if not strong > weak:
            reasons.append("strong<=weak")

        status = "PASS" if not reasons else "FAIL(" + ",".join(reasons) + ")"
        if reasons:
            failures.append(f"{name}: {','.join(reasons)}")
        print(f"{name:22} {spread:>7.1f} {distinct:>9}  {status:6}  {values}")

    print("-" * 78)
    if failures:
        print(f"\nDISCRIMINATION GATE FAILED for {len(failures)} sub-score(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nDISCRIMINATION GATE PASSED: every sub-score discriminates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
