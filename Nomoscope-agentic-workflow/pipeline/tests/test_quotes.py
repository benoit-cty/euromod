"""The verbatim-quote rule: verification, hints, chunk-id resolution, repointing."""

from __future__ import annotations

import re
from unittest.mock import MagicMock

from nomoscope_workflow.derivation import _check_derivation
from nomoscope_workflow.quotes import (
    _split_word_pattern,
    check_quote,
    closest_passage,
    misquote_hint,
    repoint_misquoted,
    verify_extract,
)
from nomoscope_workflow.schema import (
    Operand,
    RetrievalHit,
)

from workflow_fixtures import AKW_TEXT, _derived, _hit, _verify_in

CSG_TEXT = (
    "2° Sont assujetties à la contribution au taux de 8,3 % les pensions de retraite, et les "
    "pensions d'invalidité. III.-Par dérogation aux I, II et III bis, sont assujettis"
)


def test_a_tidied_quote_is_answered_with_the_passage_it_tried_to_quote():
    # 3 Nov full run: the model "corrected" la contribution into la contribution
    # sociale, and the bare retry repeated the same quote.
    tidied = "2° Sont assujetties à la contribution sociale au taux de 8,3 % les pensions de retraite, et les pensions d'invalidité."
    assert closest_passage(CSG_TEXT, tidied) == (
        "2° Sont assujetties à la contribution au taux de 8,3 % les pensions de retraite, et les "
        "pensions d'invalidité."
    )
    assert closest_passage(CSG_TEXT, "Le taux forfaitaire est fixé à 12,8 %") is None
    hint = misquote_hint([_hit(chunk_id="csg", content=CSG_TEXT)], "csg", tidied)
    assert hint.startswith("the cited chunk reads: «2° Sont assujetties à la contribution au taux")


def test_a_paraphrased_operand_gets_the_same_hint():
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    draft = _derived(operands=[
        Operand(name="a", value=347.83, citation_chunk_id="akw",
                supporting_extract="b. 6 jaar of ouder en jonger dan 12 jaar: € 347,83"),
        Operand(name="b", value=286.45, citation_chunk_id="akw",
                supporting_extract="jonger is dan 6 jaar: € 286,45"),
    ])
    issues, _, _ = _check_derivation(draft, hits, _verify_in(hits))
    assert issues[0] == "derivation: operand a's extract is not a verbatim quote of its chunk"
    assert "«b. 6 jaar of ouder, maar jonger is dan 12 jaar: € 347,83" in issues[1]


def test_a_mistyped_operand_chunk_id_is_resolved_by_its_extract():
    # 3 Nov full run: 11 derivations rejected as "cites a chunk that was not
    # retrieved" — the ids were a citation string or one hex digit off.
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    draft = _derived(operands=[
        Operand(name="a", value=347.83, citation_chunk_id="JORFTEXT000051393086",
                supporting_extract="6 jaar of ouder, maar jonger is dan 12 jaar: € 347,83"),
        Operand(name="b", value=286.45, citation_chunk_id="akw",
                supporting_extract="jonger is dan 6 jaar: € 286,45"),
    ])
    issues, offsets, _ = _check_derivation(draft, hits, _verify_in(hits))
    assert issues == [] and None not in offsets
    assert draft.operands[0].citation_chunk_id == "akw"
    # Not in any retrieved chunk: still refused, nothing guessed.
    draft.operands[0].citation_chunk_id = "elsewhere"
    draft.operands[0].supporting_extract = "between 6 and 12 years: € 347,83"
    issues, _, _ = _check_derivation(draft, hits, _verify_in(hits))
    assert any("not retrieved" in i for i in issues)


def test_a_word_split_by_pdf_extraction_still_matches_but_digits_do_not():
    chunk = "en pourcentage duquel sont fixées les prestati ons \nfamiliales, est donc porté de 466,44 €"
    assert re.search(_split_word_pattern("sont fixées les prestations familiales, est donc"), chunk)
    assert not re.search(_split_word_pattern("sont fixées les prestataires familiales"), chunk)
    assert not re.search(_split_word_pattern("25 %"), "taux 2 5 %")
    assert not re.search(_split_word_pattern("466,44 €"), "46 6,44 €")


def test_a_quote_ending_on_other_punctuation_than_the_text_still_verifies():
    conn = MagicMock()
    content = "2° A 16 % du montant forfaitaire calculé pour deux personnes lorsque le foyer se compose de deux personnes ; 3° A 16,5 %"
    conn.execute.return_value.fetchone.return_value = {"content": content, "char_start": 0}
    assert verify_extract(conn, "c", "2° A 16 % du montant forfaitaire calculé pour deux personnes lorsque le foyer se compose de deux personnes.")
    assert verify_extract(conn, "c", "« 2° A 16 % du montant forfaitaire »")
    assert verify_extract(conn, "c", "2° A 17 % du montant forfaitaire.") is None


def test_a_quote_citing_the_wrong_retrieved_chunk_is_repointed_to_the_one_holding_it():
    hits = [
        RetrievalHit(chunk_id="r5222", citation="CSS R522-2", content="Le plafond est majoré de 25 %"),
        RetrievalHit(chunk_id="dss", citation="DSS/2B/2025/38", content="PREPARE\nTaux plein 96,62 % 458,34"),
        RetrievalHit(chunk_id="dss2", citation="DSS/2B/2025/38", content="CMG maximal 540,97"),
    ]
    assert repoint_misquoted(hits, "r5222", "Taux plein 96,62 % 458,34") == "dss"
    assert repoint_misquoted(hits, "dss", "Taux plein 96,62 % 458,34") is None  # already right
    assert repoint_misquoted(hits, "r5222", "Taux plein 99 %") is None  # nowhere: the failure stands


def test_check_quote_is_the_one_sequence_for_every_quote():
    """resolve -> repoint -> verify -> hint (code audit 2.1)."""
    hits = [
        RetrievalHit(chunk_id="a", citation="CSS R522-2", content="Le plafond est majoré de 25 %"),
        RetrievalHit(chunk_id="b", citation="DSS/2B/2025/38", content="Taux plein 96,62 % 458,34"),
    ]

    def verify(chunk_id, extract):
        content = next(h.content for h in hits if h.chunk_id == chunk_id)
        i = content.find(extract)
        return (i, i + len(extract)) if i >= 0 else None

    typo = check_quote(hits, "a-typo", "Taux plein 96,62 %", verify)
    assert (typo.chunk_id, typo.status, typo.resolved_from) == ("b", "verified", "a-typo")
    swapped = check_quote(hits, "a", "Taux plein 96,62 %", verify)
    assert (swapped.chunk_id, swapped.status) == ("b", "verified") and swapped.notes
    tidied = check_quote(hits, "a", "Le plafond est majoré de 25 % au plus", verify)
    assert tidied.status == "misquoted" and tidied.hint and "majoré de 25 %" in tidied.hint
    assert check_quote(hits, "nowhere", "absent", verify).status == "not_retrieved"


def test_typographic_variants_of_one_character_are_equal():
    from nomoscope_workflow.quotes import quote_span

    chunk = "soit : \n 0,50 €/heure pour l’accueil collectif conventionnée avec la Caf, – au plus"
    quote = "0,50 €/heure pour l'accueil collectif conventionnée avec la Caf"
    span = quote_span(chunk, quote)
    assert span is not None and chunk[span[0] : span[1]].startswith("0,50 €/heure pour l’accueil")
    assert quote_span(chunk, "avec la Caf, - au plus") is not None
    # a line break typed as backslash-n is the whitespace it stands for
    assert quote_span("Tranche 1  \n(≤ 1 PSS) 6,20 %", "Tranche 1\\n(≤ 1 PSS) 6,20 %") is not None
    # nothing else is folded: another digit, another word, a skipped cell
    assert quote_span(chunk, "0,55 €/heure pour l'accueil collectif") is None
    assert quote_span(chunk, "0,50 €/heure pour l'accueil familial") is None
    assert quote_span("3 enfants \n4 enfants \n≤ 78 565 \n≤ 85 111", "3 enfants ≤ 85 111") is None
