"""When the run goes and fetches more law, and what routes it there."""

from __future__ import annotations

from nomoscope_workflow import issues as it
from nomoscope_workflow.pipeline import _needs_gap_fill
from nomoscope_workflow.quotes import misquoted_only
from nomoscope_workflow.schema import (
    CritiqueReport,
    ProposalDraft,
)


def _report(**kwargs) -> CritiqueReport:
    return CritiqueReport(**kwargs)


def test_gap_fill_triggers_when_no_value_was_found():
    assert _needs_gap_fill({}) is True
    assert _needs_gap_fill({"draft": ProposalDraft(found=False)}) is True


def test_gap_fill_stops_once_a_proposal_survives_the_critique():
    state = {
        "draft": ProposalDraft(found=True, value_scalar=0.11),
        "critique": _report(verdict="pass"),
    }
    assert _needs_gap_fill(state) is False


def test_gap_fill_ignores_a_critique_that_rejected_the_answer_itself():
    """Fetching more law cannot fix a unit error — only a missing source."""
    state = {
        "draft": ProposalDraft(found=True, value_scalar=4.1),
        "critique": _report(
            verdict="fail",
            issues=["values_sane: the parameter declares unit currency for a percentage rate"],
        ),
    }
    assert _needs_gap_fill(state) is False


def test_gap_fill_triggers_on_a_source_availability_failure():
    """The proposal exists, but nothing in the corpus ties it to the income
    year — the applicability clause is in an act we do not hold."""
    state = {
        "draft": ProposalDraft(found=True, value_scalar=0.11),
        "critique": _report(
            verdict="fail",
            issues=["the cited article never names income year 2025, but art. 10 does"],
        ),
    }
    assert _needs_gap_fill(state) is True

    provisional = {
        "draft": ProposalDraft(found=True, value_scalar=0.11),
        "critique": _report(verdict="fail", provisional=True),
    }
    assert _needs_gap_fill(provisional) is True


def test_a_misquote_alone_earns_the_extra_attempt():
    assert misquoted_only([
        "derivation: operand d's extract is not a verbatim quote of its chunk",
        "derivation: operand d: the cited chunk reads: «3° A 16,5 % du montant forfaitaire» — quote it exactly",
        "note: derived — a * b",
    ])
    assert misquoted_only([
        "supporting_extract is not a verbatim quote of the cited chunk",
        "the cited chunk reads: «… 0,72 % …» — quote it exactly as written, without correcting it",
    ])
    assert not misquoted_only([
        "supporting_extract is not a verbatim quote of the cited chunk",
        "citation_supports_value: the cited amendment does not state the first-band rate",
    ])
    assert not misquoted_only(["note: derived — a * b"])


def test_routed_issues_are_recognised_from_their_own_wording():
    """Rewording a routed issue cannot silently change routing (code audit 4)."""
    assert it.code_of(it.CITATION_NOT_RETRIEVED) in it.SOURCE_GAP
    assert it.code_of(it.operand_not_verbatim("b")) in it.MISQUOTE
    assert it.code_of(it.operand_hint("b", it.misquote_hint("x"))) in it.MISQUOTE
    assert it.code_of(it.operand_not_retrieved("b")) not in it.MISQUOTE
    assert it.code_of("note: derived") is None
