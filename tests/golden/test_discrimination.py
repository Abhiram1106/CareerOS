"""Discrimination gate: the scoring stack must NOT return constant outputs.

This is the anti-"same output for any input" guard. For every sub-score we feed
the full corpus of distinct resume personas and assert:

  1. SPREAD — the score range (max - min) across personas exceeds a floor. A
     heuristic that bins everything into one or two values fails here.
  2. DISTINCT VALUES — the score takes at least N distinct values across the
     corpus, so it isn't a 2-bucket step function masquerading as a score.
  3. ORDERING — strong-tier personas outscore weak-tier personas on the
     overall placement score (the stack is directionally correct).

These run inside the core-api container where ``careeros_scoring`` and its deps
are installed:

    docker compose exec -T core-api python -m pytest tests/golden -q

Phases 1-4 of the fine-tune plan are expected to move several of these from
FAIL (today) to PASS. The thresholds below encode the target, not the current
state — a failing test here is the proof a sub-score is still theater.
"""

from __future__ import annotations

import statistics

import pytest

from careeros_scoring import (
    analyze_ats,
    evidence_quality_score,
    interview_readiness_score,
    placement_hygiene_score,
    profile_completeness_score,
)

from .corpus import ALL_PERSONAS


def _ats(persona) -> float:
    return analyze_ats(persona.text, [])["ats_parse_safety"]


def _evidence(persona) -> float:
    return evidence_quality_score(persona.sections)


def _interview(persona) -> float:
    return interview_readiness_score(persona.sections)


def _hygiene(persona) -> float:
    return placement_hygiene_score(persona.sections, [])


def _completeness(persona) -> float:
    return profile_completeness_score(persona.sections)


SUBSCORES = {
    "ats_parse_safety": _ats,
    "evidence_quality": _evidence,
    "interview_readiness": _interview,
    "placement_hygiene": _hygiene,
    "profile_completeness": _completeness,
}

# A real score across 7 varied resumes should span a wide range and take many
# distinct values. Heuristics that clamp/bin fall below these floors.
MIN_SPREAD = 30.0
MIN_DISTINCT_VALUES = 5


@pytest.mark.parametrize("name", list(SUBSCORES))
def test_subscore_has_spread(name):
    fn = SUBSCORES[name]
    values = [fn(p) for p in ALL_PERSONAS]
    spread = max(values) - min(values)
    assert spread >= MIN_SPREAD, (
        f"{name} spread only {spread:.1f} across {len(values)} distinct resumes "
        f"(values={values}); looks like a clustered/constant score."
    )


@pytest.mark.parametrize("name", list(SUBSCORES))
def test_subscore_has_distinct_values(name):
    fn = SUBSCORES[name]
    values = [round(fn(p), 1) for p in ALL_PERSONAS]
    distinct = len(set(values))
    assert distinct >= MIN_DISTINCT_VALUES, (
        f"{name} produced only {distinct} distinct values across "
        f"{len(values)} distinct resumes (values={values}); "
        f"this is a step-function, not a score."
    )


@pytest.mark.parametrize("name", list(SUBSCORES))
def test_subscore_strong_beats_weak(name):
    fn = SUBSCORES[name]
    strong = statistics.mean(fn(p) for p in ALL_PERSONAS if p.tier == "strong")
    weak = statistics.mean(fn(p) for p in ALL_PERSONAS if p.tier == "weak")
    assert strong > weak, (
        f"{name}: strong-tier mean {strong:.1f} did not beat weak-tier mean "
        f"{weak:.1f}; the score is not directionally correct."
    )
