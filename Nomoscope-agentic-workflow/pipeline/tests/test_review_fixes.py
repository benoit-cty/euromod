"""Regressions from the 2026-09-08 eval review (eval-20260908T143801Z…luna)."""

from nomoscope_workflow.paramdb import normalise_value, percent_literal
from nomoscope_workflow.pipeline import _resolve_chunk_by_extract
from nomoscope_workflow.schema import RetrievalHit


def test_percent_literals_are_scalars_in_the_store():
    # NL/LT spell every rate as a percent literal; IE a few. They are the "/1"
    # fraction, the reading the eval's normalise_value and the curated unit use.
    assert percent_literal("8.17%") == 0.0817
    assert percent_literal("49,50%") == 0.495
    assert percent_literal(" 4.1 % ") == 0.041
    assert percent_literal("$PSS * 4") is None
    assert percent_literal("n/a") is None
    assert normalise_value("8.17%") == (0.0817, "numeric")
    assert normalise_value("2/3") == (None, "expression")
    assert normalise_value("n/a") == (None, "n_a")


def _hit(chunk_id: str, content: str) -> RetrievalHit:
    return RetrievalHit(chunk_id=chunk_id, citation="Finance Act 2024, s. 2", content=content)


def test_a_mistyped_chunk_id_resolves_to_the_one_chunk_holding_the_extract():
    hits = [
        _hit("4a56d5eb-c673-4faf-a54c-efbe35e1039d", "by the substitution of “€27,382” for “€25,760”, and"),
        _hit("d1f7d7ef-0000-4000-8000-000000000000", "an unrelated provision"),
    ]
    assert (
        _resolve_chunk_by_extract(hits, "substitution of “€27,382” for “€25,760”")
        == "4a56d5eb-c673-4faf-a54c-efbe35e1039d"
    )


def test_an_extract_present_in_two_chunks_does_not_resolve():
    # Two versions of the same article both carry the sentence: guessing would
    # cite a version the model never read, so the mechanical failure stands.
    hits = [_hit("a", "les revenus excèdent 14 548 €"), _hit("b", "les revenus excèdent 14 548 €")]
    assert _resolve_chunk_by_extract(hits, "excèdent 14 548 €") is None
    assert _resolve_chunk_by_extract(hits, "") is None
    assert _resolve_chunk_by_extract(hits, "not in any chunk") is None
