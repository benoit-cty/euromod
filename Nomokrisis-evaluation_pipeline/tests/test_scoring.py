"""Scoring unit tests: KPI semantics on synthetic ReviewItems."""

from __future__ import annotations

from datetime import date, datetime, timezone

from nomoscope_workflow.schema import (
    Bracket,
    CritiqueReport,
    ParameterValue,
    Reference,
    RetrievalHit,
    ReviewItem,
    Routing,
)

from nomokrisis_eval.schema import Expected, GoldenCase
from nomokrisis_eval.scoring import citation_matches, score_item, values_equal


def make_case(**expected_kwargs) -> GoldenCase:
    return GoldenCase(
        id="fr_test_case",
        country="FR",
        language="fr",
        parameter_file="agentic-workflow/data/parameters/fr_tinrt_top_rate.json",
        as_of=date(2025, 6, 1),
        expected=Expected(**expected_kwargs),
        verified=True,
    )


def make_item(
    routing: Routing = Routing.UNCHANGED,
    value=0.45,
    valid_from: date = date(2025, 1, 1),
    citation: str | None = "CGI, art. 197",
    citation_verified: bool = True,
    with_proposal: bool = True,
    trace_citation: str | None = "CGI, art. 197",
) -> ReviewItem:
    proposed = None
    if with_proposal:
        proposed = ParameterValue(
            value=value,
            valid_from=valid_from,
            references=[Reference(title=citation)] if citation else [],
        )
    return ReviewItem(
        id="fr_item",
        run_id="run",
        created_at=datetime.now(timezone.utc),
        country="FR",
        model_target="euromod://FR/tin_fr/def_const/$tinrt_top",
        as_of=date(2025, 6, 1),
        value_type="scalar",
        unit="/1",
        routing=routing,
        proposed_value=proposed,
        critique=CritiqueReport(citation_verified=citation_verified),
        retrieval_trace=(
            [RetrievalHit(chunk_id="c1", citation=trace_citation)] if trace_citation else []
        ),
    )


def test_all_correct_scalar():
    case = make_case(routing=Routing.UNCHANGED, value=0.45, valid_from=date(2025, 1, 1),
                     citations=["CGI, art. 197"])
    r = score_item(case, make_item())
    assert r.routing_correct and r.value_correct and r.date_correct
    assert r.citation_correct and r.supportedness and r.retrieval_hit
    assert not r.hallucination


def test_wrong_value_and_routing():
    case = make_case(routing=Routing.CHANGED, value=0.46, citations=["CGI, art. 197"])
    r = score_item(case, make_item(routing=Routing.UNCHANGED, value=0.45))
    assert r.routing_correct is False
    assert r.value_correct is False


def test_bracket_comparison():
    expected = [Bracket(threshold=0, rate=0.0), Bracket(threshold=11497, rate=0.11)]
    proposed = [Bracket(threshold=0, rate=0.0), Bracket(threshold=11497, rate=0.11)]
    assert values_equal(proposed, expected)
    assert not values_equal([Bracket(threshold=0, rate=0.0)], expected)
    assert not values_equal(
        [Bracket(threshold=0, rate=0.0), Bracket(threshold=11294, rate=0.11)], expected
    )


def test_unscored_kpis_are_none():
    case = make_case(routing=Routing.NOT_FOUND)  # no expected value/date/citations
    r = score_item(case, make_item(routing=Routing.NOT_FOUND, with_proposal=False))
    assert r.routing_correct is True
    assert r.value_correct is None and r.date_correct is None
    assert r.citation_correct is None and r.retrieval_hit is None
    assert r.supportedness is None and r.hallucination is False


def test_hallucination_flag():
    case = make_case(routing=Routing.UNCHANGED, value=0.45)
    r = score_item(case, make_item(citation_verified=False))
    assert r.hallucination is True
    assert r.supportedness is False


def test_missed_proposal_scores_false():
    case = make_case(routing=Routing.UNCHANGED, value=0.45, citations=["CGI, art. 197"])
    r = score_item(case, make_item(routing=Routing.NOT_FOUND, with_proposal=False,
                                   trace_citation=None))
    assert r.value_correct is False
    assert r.citation_correct is False
    assert r.retrieval_hit is False


def test_citation_normalisation():
    assert citation_matches("CGI, art. 197", "cgi art 197")
    assert citation_matches("CGI, art. 197", "Code général des impôts > CGI, art. 197 (vig. 2025)")
    assert not citation_matches("CGI, art. 197", "CGI, art. 200")
    assert not citation_matches("CGI, art. 197", None)
