"""Source-trust classes: a proposal resting on guidance only is labelled (ADR 0001)."""

from __future__ import annotations

from datetime import date

from nomoscope_workflow import mock
from nomoscope_workflow.pipeline import GUIDANCE_ONLY_ISSUE, cited_classes, guidance_only
from nomoscope_workflow.schema import (
    Bracket,
    CritiqueReport,
    ParameterValue,
    ProposalDraft,
    Reference,
    ReviewItem,
    Routing,
    SourceTrustClass,
)

from workflow_fixtures import _hit, _record


def _draft_citing(chunk_id: str) -> ProposalDraft:
    return ProposalDraft(found=True, value_scalar=0.45, citation_chunk_id=chunk_id)


def test_retrieval_hits_and_mock_proposals_default_to_evidence():
    """Nothing that predates the class column silently becomes guidance."""
    record = _record("bracket_schedule", "/1", [Bracket(threshold=0, rate=0.0)])
    hit = _hit()

    assert hit.source_trust_class == SourceTrustClass.EVIDENCE
    draft = mock.propose_with_mock(record, date(2025, 6, 1), [hit])
    assert draft.found
    assert not guidance_only([hit.source_trust_class])


def test_guidance_only_needs_every_citation_to_be_guidance():
    """The informational finding fires on guidance alone, never on a mix."""
    guidance = SourceTrustClass.GUIDANCE
    evidence = SourceTrustClass.EVIDENCE

    assert guidance_only([guidance])
    assert guidance_only([guidance, guidance])
    assert not guidance_only([guidance, evidence])
    assert not guidance_only([evidence])
    # No citation at all is not "guidance-only": there is nothing to label.
    assert not guidance_only([])


def test_guidance_only_finding_leaves_the_verdict_alone():
    """The finding is appended to issues; the four verdict booleans are untouched."""
    report = CritiqueReport(
        schema_valid=True,
        citation_verified=True,
        dates_consistent=True,
        values_sane=True,
        verdict="pass",
    )

    report.issues.append(GUIDANCE_ONLY_ISSUE)

    assert report.verdict == "pass"
    assert GUIDANCE_ONLY_ISSUE in report.issues


def test_guidance_only_flag_survives_the_queue_roundtrip():
    """A reviewer reopening the queue still sees what the value rested on."""
    item = ReviewItem(
        id="fr_guidance_2025",
        run_id="run-g",
        created_at="2026-07-09T00:00:00Z",
        country="FR",
        model_target="euromod://FR/test",
        as_of=date(2025, 6, 1),
        system_year=2025,
        value_type="scalar",
        unit="/1",
        routing=Routing.CHANGED,
        guidance_only=True,
        proposed_value=ParameterValue(
            value=0.45,
            valid_from=date(2025, 1, 1),
            references=[
                Reference(
                    title="Circulaire Unedic n. 2025-01",
                    source_trust_class=SourceTrustClass.GUIDANCE,
                )
            ],
        ),
    )

    # the queue row stores item.model_dump(mode="json"); this is that round trip
    loaded = ReviewItem.model_validate(item.model_dump(mode="json"))

    assert loaded.guidance_only
    assert loaded.proposed_value.references[0].source_trust_class == SourceTrustClass.GUIDANCE


def test_the_finding_reads_the_class_of_the_chunk_the_draft_cites():
    """The wiring itself: only the CITED hit decides, not whatever was retrieved.

    A guidance document answering the question sits next to evidence chunks in
    every real run — reading the whole hit list instead of the cited chunk
    would label almost nothing.
    """
    guidance = _hit(chunk_id="c-guidance", source_trust_class=SourceTrustClass.GUIDANCE)
    evidence = _hit(chunk_id="c-evidence", source_trust_class=SourceTrustClass.EVIDENCE)
    hits = [evidence, guidance]

    assert guidance_only(cited_classes(_draft_citing("c-guidance"), hits))
    assert not guidance_only(cited_classes(_draft_citing("c-evidence"), hits))
    # A citation that is not among the retrieved chunks labels nothing: the
    # critique has already failed it on the citation leg.
    assert cited_classes(_draft_citing("c-unknown"), hits) == []
    assert not guidance_only(cited_classes(_draft_citing("c-unknown"), hits))
    # No proposal at all, and no citation on one, are both "nothing to label".
    assert cited_classes(None, hits) == []
    assert cited_classes(ProposalDraft(found=False), hits) == []
