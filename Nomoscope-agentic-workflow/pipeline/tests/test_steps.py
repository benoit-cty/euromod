"""The workflow's steps called directly (code audit 4: critique and diff had no direct test).

No database and no LLM: `retrieval.connect` and `quotes.verify_extract` are
replaced by in-memory fakes and the critic is injected through StepContext.
"""

from __future__ import annotations

from contextlib import nullcontext
from datetime import date

import pytest
from opentelemetry import trace

from nomoscope_workflow import pipeline, quotes, retrieval
from nomoscope_workflow.config import load_config
from nomoscope_workflow.schema import (
    CritiqueFindings,
    ParameterInformation,
    ParameterRecord,
    ParameterValue,
    ProposalDraft,
    RetrievalHit,
    Routing,
)

AS_OF = date(2025, 7, 1)
TEXT = "Le montant forfaitaire mentionné à l'article L. 262-2 est fixé à 646,52 euros."


def _hit(**kw) -> RetrievalHit:
    base = dict(chunk_id="rsa", citation="Décret n° 2025-283, art. 1", method="hybrid",
                validity="[2025-04-01,)", version_status="in_force", lang="fr", content=TEXT)
    return RetrievalHit(**{**base, **kw})


def _record(held=635.71) -> ParameterRecord:
    return ParameterRecord(
        information=ParameterInformation(
            country="FR", model_target="euromod://FR/test/$rsa", value_type="scalar", unit="currency"
        ),
        values=[ParameterValue(value=held, valid_from=date(2024, 4, 1))],
    )


@pytest.fixture
def ctx(monkeypatch):
    contents = {"rsa": TEXT}

    def verify(conn, chunk_id, extract):
        i = contents.get(chunk_id, "").find(extract) if extract else -1
        return (i, i + len(extract)) if i >= 0 else None

    monkeypatch.setattr(retrieval, "connect", lambda cfg: nullcontext(None))
    monkeypatch.setattr(quotes, "verify_extract", verify)
    monkeypatch.setattr(retrieval, "version_provenance", lambda conn, chunk_id: None, raising=False)
    calls = []

    def critic(record, as_of, draft, hits, notes):
        calls.append(notes)
        return CritiqueFindings(citation_supports_value=True, dates_consistent=True)

    context = pipeline.StepContext(
        cfg=load_config(), tracer=trace.get_tracer("test"),
        proposer=lambda *a: None, critic=critic, deterministic=True,
    )
    return context, calls


def _state(draft: ProposalDraft, held=635.71) -> dict:
    return {"record": _record(held), "as_of": AS_OF, "retrieval_as_of": AS_OF, "draft": draft,
            "hits": [_hit()], "run_id": "run-test", "attempts": 1}


def _draft(**kw) -> ProposalDraft:
    base = dict(found=True, value_scalar=646.52, valid_from=date(2025, 4, 1), citation_chunk_id="rsa",
                supporting_extract="est fixé à 646,52 euros")
    return ProposalDraft(**{**base, **kw})


def test_critique_verifies_a_verbatim_extract(ctx):
    ctx, _ = ctx
    report = pipeline.critique(ctx, _state(_draft()))["critique"]
    assert report.citation_verified and report.extract_offsets is not None
    assert report.verdict == "pass", report.issues


def test_critique_fails_a_paraphrase_and_quotes_the_passage(ctx):
    ctx, _ = ctx
    report = pipeline.critique(ctx, _state(_draft(supporting_extract="est fixé à 646,52 € par mois")))["critique"]
    assert report.verdict == "fail" and not report.citation_verified
    assert "supporting_extract is not a verbatim quote of the cited chunk" in report.issues
    assert any(i.startswith("the cited chunk reads: «") for i in report.issues)


def test_critique_resolves_a_mistyped_chunk_id(ctx):
    ctx, calls = ctx
    state = _state(_draft(citation_chunk_id="Décret n° 2025-283, art. 1"))
    report = pipeline.critique(ctx, state)["critique"]
    assert report.citation_verified and state["draft"].citation_chunk_id == "rsa"
    assert any("resolved to rsa" in n for n in calls[-1] or [])


def test_diff_routes_a_verified_change(ctx):
    ctx, _ = ctx
    state = _state(_draft())
    state.update(pipeline.critique(ctx, state))
    out = pipeline.diff(ctx, state)
    assert out["routing"] == Routing.CHANGED
    assert out["item"].proposed_value.value == 646.52


def test_diff_routes_unchanged_and_not_found(ctx):
    ctx, _ = ctx
    state = _state(_draft(), held=646.52)
    state.update(pipeline.critique(ctx, state))
    assert pipeline.diff(ctx, state)["routing"] == Routing.UNCHANGED
    nothing = _state(ProposalDraft(found=False))
    nothing.update(pipeline.critique(ctx, nothing))
    assert pipeline.diff(ctx, nothing)["routing"] == Routing.NOT_FOUND
