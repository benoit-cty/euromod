"""Derived values: arithmetic over quoted operands, figures, rounding, sanity."""

from __future__ import annotations

from datetime import date

import pytest
from nomoscope_workflow.derivation import (
    DERIVATION_CONSTANTS,
    _check_derivation,
    _extract_states,
    _figures_in,
    _round_like_held,
    _values_sane,
    evaluate_derivation,
)
from nomoscope_workflow.schema import (
    Bracket,
    Operand,
    ParameterValue,
    ProposalDraft,
)
from workflow_fixtures import AKW_TEXT, _derived, _hit, _verify_in


def test_derivation_over_quoted_operands_is_verified():
    hits = [_hit(chunk_id="akw", citation="AKW, artikel 12", lang="nl", content=AKW_TEXT)]
    issues, offsets, note = _check_derivation(_derived(), hits, _verify_in(hits))
    assert issues == []
    assert all(span is not None for span in offsets) and len(offsets) == 2
    assert "a = 347.83 (AKW, artikel 12)" in note and "= 1.2142" in note


def test_derivation_rejects_a_figure_that_is_not_quoted():
    """Statutory monthly hours remembered rather than quoted are not evidence."""
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    draft = _derived(derivation="a * 151.67", value_scalar=52755.0)
    issues, _, _ = _check_derivation(draft, hits, _verify_in(hits))
    assert issues and "151.67" in issues[0] and "not a quoted operand" in issues[0]


def test_derivation_allows_calendar_constants_only():
    assert evaluate_derivation("a * 12 + b", {"a": 2.0, "b": 1.0}) == 25.0
    assert 12.0 in DERIVATION_CONSTANTS
    for bad in ("a ** 2", "__import__('os').system('x')", "max(a, b)", "a.real", "0.5 * a"):
        with pytest.raises(ValueError):
            evaluate_derivation(bad, {"a": 1.0, "b": 2.0})


def test_derivation_rounds_where_the_text_says_so():
    # AGIRC-ARRCO art. 36: «Les taux ainsi appelés sont arrondis au centième».
    # 6,20 % × 127 % = 7,874 % -> 7,87 %; the 60 % employer share is 4,722 %.
    called = evaluate_derivation("round(a * b, 4)", {"a": 0.062, "b": 1.27})
    assert called == 0.0787
    assert evaluate_derivation("round(a * b, 4) * c", {"a": 0.062, "b": 1.27, "c": 0.6}) == pytest.approx(0.04722)
    # Half-up, as a legal text means it — Python's round(0.5) is 0.
    assert evaluate_derivation("round(a, 0)", {"a": 0.5}) == 1.0
    assert evaluate_derivation("round(a, 0)", {"a": 2.5}) == 3.0
    # The precision is a literal, never a figure smuggled in by another route.
    for bad in ("round(a, b)", "round(a, 1.5)", "round(a)", "round(a, 9)", "round(a, ndigits=2)", "round(a, -1)"):
        with pytest.raises(ValueError):
            evaluate_derivation(bad, {"a": 1.234, "b": 2.0})


def test_derivation_rejects_an_operand_the_extract_does_not_state():
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    draft = _derived(
        operands=[
            Operand(
                name="a",
                value=347.83,
                citation_chunk_id="akw",
                supporting_extract="6 jaar of ouder, maar jonger is dan 12 jaar: € 347,83",
            ),
            Operand(
                name="b",
                value=286.45,
                citation_chunk_id="akw",
                supporting_extract="12 jaar en ouder, maar jonger is dan 18 jaar: € 409,21",
            ),
        ]
    )
    issues, _, _ = _check_derivation(draft, hits, _verify_in(hits))
    assert issues[0] == "derivation: operand b's extract does not state 286.45"
    # The retry is shown where the chunk does state it (CSS D. 622-7's «1/ 730e»
    # was a sentence away from the one the model quoted twice).
    assert (
        issues[1] == "derivation: operand b: its chunk states 286.45 in «jonger is dan 6 jaar: € 286,45» — quote that"
    )


def test_derivation_rejects_a_paraphrased_operand_and_an_unretrieved_chunk():
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    draft = _derived(
        operands=[
            Operand(
                name="a", value=347.83, citation_chunk_id="akw", supporting_extract="between 6 and 12 years: € 347,83"
            ),
            Operand(
                name="b", value=286.45, citation_chunk_id="elsewhere", supporting_extract="jonger dan 6 jaar: € 286,45"
            ),
        ]
    )
    issues, offsets, _ = _check_derivation(draft, hits, _verify_in(hits))
    assert offsets == [None, None]
    assert any("not a verbatim quote" in i for i in issues)
    assert any("not retrieved" in i for i in issues)


def test_derivation_must_evaluate_to_the_proposed_value():
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    issues, _, _ = _check_derivation(_derived(value_scalar=1.3), hits, _verify_in(hits))
    assert issues and "evaluates to 1.21428" in issues[0]


def test_figures_are_read_in_every_european_spelling():
    assert 1801.80 in _figures_in("11,88 € par heure, soit 1 801,80 € par mois")
    assert 1801.80 in _figures_in("1.801,80 euros")
    assert 9139.0 in _figures_in("vermeerderd met € 9.139")  # Dutch thousands
    assert 2.1 in _figures_in("artikel 2.10") and 44000.0 in _figures_in("€44,000")


def test_a_table_row_states_each_of_its_amounts():
    # arrêté du 27 sept. 2019 art. 7, zone I: the PDF row is one run of digits
    row = _figures_in("I 329,71 397,64 449,43 65,21 II")
    assert {329.71, 397.64, 449.43, 65.21} <= row
    assert 801.80 not in _figures_in("1 801,80 €")


def test_a_schedule_may_derive_one_of_its_figures():
    # 3 Nov full run: five schedules with exactly EUROMOD's bands were rejected
    # as "only a scalar value can be derived" (AGIRC-ARRCO CET share a * b).
    text = "contribution d'équilibre technique, au taux de 0,35 % ... répartie à raison de 60 % à la charge des employeurs et 40 % à la charge des salariés"
    hits = [_hit(chunk_id="ani", content=text)]
    ops = [
        Operand(name="a", value=0.0035, citation_chunk_id="ani", supporting_extract="au taux de 0,35 %"),
        Operand(name="b", value=0.4, citation_chunk_id="ani", supporting_extract="40 % à la charge des salariés"),
    ]
    good = _derived(
        value_scalar=None,
        value_brackets=[Bracket(threshold=0.0, rate=0.0014)],
        derivation="a * b",
        operands=ops,
        supporting_extract="au taux de 0,35 %",
        citation_chunk_id="ani",
    )
    assert _check_derivation(good, hits, _verify_in(hits))[0] == []
    wrong = good.model_copy(update={"value_brackets": [Bracket(threshold=0.0, rate=0.0035)]})
    issues, _, _ = _check_derivation(wrong, hits, _verify_in(hits))
    assert issues == ["derivation: a * b evaluates to 0.0014, not any figure of the proposed schedule"]
    # A schedule's figure is not replaced by the result, so no 0.1 % slack:
    # 0.00140 is 0,14 %, 0.001401 is not what the law computes.
    near = good.model_copy(update={"value_brackets": [Bracket(threshold=0.0, rate=0.001401)]})
    assert _check_derivation(near, hits, _verify_in(hits))[0] != []


def test_a_negative_rate_is_sane_and_an_unnormalised_percentage_is_not():
    # «Majoration par personne à charge -0,06%» ($bho_Tf_rate8, 3 Nov run).
    assert _values_sane("/1", ProposalDraft(found=True, value_scalar=-0.0006))
    assert not _values_sane("/1", ProposalDraft(found=True, value_scalar=11.0))
    assert not _values_sane("/1", ProposalDraft(found=True, value_scalar=-6.0))


def test_a_rate_in_percentage_points_is_sane_under_unit_per_hundred():
    # $bho_rl_rate2 holds 0.45 for «0,45 %».
    assert _values_sane("/100", ProposalDraft(found=True, value_scalar=0.45))
    assert not _values_sane("/100", ProposalDraft(found=True, value_scalar=450.0))


def test_a_derived_amount_is_rounded_like_the_amount_held():
    # PAJE ceiling 29 169 × 1,8 = 52 504,2, published 52 504; RSA
    # 646,52 × 1,8 = 1 163,736, paid 1 163,74 (4 Nov round-2 run).
    def held(value):
        return ParameterValue(value=value, valid_from=date(2024, 1, 1))

    ceiling = ProposalDraft(found=True, value_scalar=52504.2)
    assert "52504" in _round_like_held("currency", ceiling, held(51229.0))
    assert ceiling.value_scalar == 52504
    half = ProposalDraft(found=True, value_scalar=8750.5)
    _round_like_held("currency", half, held(8546.0))
    assert half.value_scalar == 8751
    rsa = ProposalDraft(found=True, value_scalar=1163.736)
    _round_like_held("currency", rsa, held(1143.28))
    assert rsa.value_scalar == 1163.74
    # Unknown precision: cents. Already at the precision: untouched.
    loose = ProposalDraft(found=True, value_scalar=258.608)
    _round_like_held("currency", loose, None)
    assert loose.value_scalar == 258.61
    assert _round_like_held("currency", ProposalDraft(found=True, value_scalar=52504.0), held(1.0)) is None
    rate = ProposalDraft(found=True, value_scalar=0.0787)
    assert _round_like_held("/1", rate, held(0.08)) is None and rate.value_scalar == 0.0787
    # A rate held with four or more decimals: as many. A coarser one: untouched.
    pi = ProposalDraft(found=True, value_scalar=0.12954)
    assert _round_like_held("/1", pi, held(0.1295)) and pi.value_scalar == 0.1295
    fine = ProposalDraft(found=True, value_scalar=0.047244)
    _round_like_held("/1", fine, held(0.0472))
    assert fine.value_scalar == 0.0472
    coarse = ProposalDraft(found=True, value_scalar=0.0675)
    assert _round_like_held("/1", coarse, held(0.068)) is None and coarse.value_scalar == 0.0675


def test_the_derivation_result_is_rounded_not_the_typed_figure():
    # $bsa00_amt9: 646,52 × (1,28412 + 2 × 0,42804) = 1 383,682, typed 1 383,28
    # and accepted by the 0.1 % check (5 Nov full run).
    held = ParameterValue(value=1357.7, valid_from=date(2024, 1, 1))
    typo = ProposalDraft(found=True, value_scalar=1383.28)
    note = _round_like_held("currency", typo, held, 646.52 * (1.28412 + 2 * 0.42804))
    assert typo.value_scalar == 1383.68 and "the proposal said 1383.28" in note
    exact = ProposalDraft(found=True, value_scalar=276.74)
    assert _round_like_held("currency", exact, held, 0.42804 * 646.52) is None
    # No precision to round to: the derivation's result is proposed, never the
    # typed figure 0.1 % away from it.
    coarse = ProposalDraft(found=True, value_scalar=0.0675)
    note = _round_like_held("/1", coarse, ParameterValue(value=0.068, valid_from=date(2024, 1, 1)), 0.06752)
    assert coarse.value_scalar == 0.06752 and "the proposal said 0.0675" in note
    ratio = ProposalDraft(found=True, value_scalar=1.2142)
    _round_like_held("ratio", ratio, None, 347.83 / 286.45)
    assert ratio.value_scalar == 347.83 / 286.45
    # Not derived, no precision: nothing to change.
    assert (
        _round_like_held(
            "/1",
            ProposalDraft(found=True, value_scalar=0.0675),
            ParameterValue(value=0.068, valid_from=date(2024, 1, 1)),
        )
        is None
    )


def test_months_either_side_of_a_mid_year_revaluation_may_appear_unquoted():
    assert evaluate_derivation("(a * 3 + b * 9) / 12", {"a": 622.63, "b": 633.21}) == pytest.approx(630.565)


def test_a_figure_spelt_out_in_words_is_stated():
    assert _extract_states("dans la limite de trois fois ce plafond", 3.0)
    assert _extract_states("égal à la moitié du montant du plafond annuel", 0.5)
    assert not _extract_states("dans la limite de trois fois ce plafond", 4.0)


def test_a_multiplier_is_stated_by_the_increase_it_applies():
    assert _extract_states("est majoré de 50 % lorsque le foyer comporte deux personnes", 1.5)
    assert not _extract_states("est fixé à 50 % du plafond", 1.5)  # no increase: 50 % is 0.5
    assert not _extract_states("est majoré de 50 %", 1.3)
