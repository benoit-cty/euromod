"""Deterministic scoring of a workflow ReviewItem against a GoldenCase.

Pure functions only — no LLM judge in v1. KPI semantics follow
04_activity4_validation.md:

  routing_correct   changed / unchanged / new / not_found / national_team_source
  value_correct     exact match (scalars, tolerance 1e-9) or structure+cell match (brackets)
  date_correct      proposed valid_from == expected valid_from
  citation_correct  pinpoint citation matches one of the accepted citations
  supportedness     the cited text verbatim-contains the extract (mechanical check
                    already done by the workflow critique: citation_verified)
  hallucination     a value was proposed but its citation does not support it
  retrieval_hit     the ground-truth citation appears in the retrieval trace (recall@k)
"""

from __future__ import annotations

import re

from nomoscope_workflow.schema import Bracket, ReviewItem

from .schema import CaseResult, GoldenCase

_NORM_RE = re.compile(r"[\s. ,;:'’-]+")


def _norm(text: str) -> str:
    return _NORM_RE.sub("", text).casefold()


def citation_matches(expected: str, candidate: str | None) -> bool:
    if not candidate:
        return False
    a, b = _norm(expected), _norm(candidate)
    return bool(a) and (a in b or b in a)


def values_equal(a, b) -> bool:
    """Scalar/bool/str/bracket-schedule comparison with float tolerance."""
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_brackets_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(float(a) - float(b)) < 1e-9
    return a == b


def _brackets_equal(a: Bracket, b: Bracket) -> bool:
    def eq(x: float | None, y: float | None) -> bool:
        return (x is None) == (y is None) and (x is None or abs(x - y) < 1e-9)

    return eq(a.threshold, b.threshold) and eq(a.rate, b.rate) and eq(a.amount, b.amount)


def score_item(case: GoldenCase, item: ReviewItem) -> CaseResult:
    expected = case.expected
    proposed = item.proposed_value

    result = CaseResult(
        case_id=case.id,
        country=case.country,
        language=case.language,
        model_target=item.model_target,
        difficulty=case.difficulty,
        source_class=case.source_class,
        routing_expected=expected.routing.value,
        routing_actual=item.routing.value,
        routing_correct=item.routing == expected.routing,
        item_id=item.id,
        phoenix_trace_id=item.phoenix_trace_id,
        confidence=(
            proposed.lineage.confidence if proposed is not None and proposed.lineage else None
        ),
        expected_value=_dump(expected.value),
        proposed_value=_dump(proposed.value) if proposed is not None else None,
    )

    if expected.value is not None:
        result.value_correct = proposed is not None and values_equal(proposed.value, expected.value)

    if expected.valid_from is not None:
        result.date_correct = proposed is not None and proposed.valid_from == expected.valid_from

    if expected.citations:
        result.citation_correct = proposed is not None and any(
            citation_matches(exp, ref.title)
            for exp in expected.citations
            for ref in proposed.references
        )
        result.retrieval_hit = any(
            citation_matches(exp, hit.citation) or citation_matches(exp, hit.context_header)
            for exp in expected.citations
            for hit in item.retrieval_trace
        )

    if proposed is not None:
        supported = bool(item.critique and item.critique.citation_verified)
        result.supportedness = supported
        result.hallucination = not supported

    return result


def _dump(value):
    if isinstance(value, list):
        return [b.model_dump(exclude_none=True) if isinstance(b, Bracket) else b for b in value]
    return value
