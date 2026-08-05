"""DB-free unit tests: mock extraction, diff logic, queue round-trip."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from nomoscope_workflow import mock, queue_store
from nomoscope_workflow.pipeline import (
    _current_value,
    _income_year_date_issues,
    _retrieval_as_of,
    _unchanged_window,
    _values_equal,
)
from nomoscope_workflow.retrieval import validity_start
from nomoscope_workflow.schema import (
    Bracket,
    ItemStatus,
    ParameterInformation,
    ParameterRecord,
    ParameterValue,
    RetrievalHit,
    ReviewItem,
    Routing,
    TemporalBasis,
)

FR_TEXT = (
    "1. L'impôt est calculé en appliquant à la fraction de chaque part de revenu qui excède "
    "11 497 € le taux de : 11 % pour la fraction supérieure à 11 497 € et inférieure ou égale à "
    "29 315 € ; 30 % pour la fraction supérieure à 29 315 € et inférieure ou égale à 83 823 € ; "
    "45 % pour la fraction supérieure à 180 294 €. 2. La réduction d'impôt est de 45,25 % de son montant."
)


def _hit(**kwargs) -> RetrievalHit:
    defaults = dict(
        chunk_id="c1",
        citation="CGI, art. 197",
        method="citation",
        score=1.0,
        validity="[2025-01-01,)",
        version_status="in_force",
        lang="fr",
        content=FR_TEXT,
    )
    return RetrievalHit(**{**defaults, **kwargs})


def _record(value_type: str, unit: str, value, **info) -> ParameterRecord:
    return ParameterRecord(
        information=ParameterInformation(
            country="FR", model_target="euromod://FR/test", value_type=value_type, unit=unit, **info
        ),
        values=[ParameterValue(value=value, valid_from=date(2024, 1, 1))],
    )


def test_mock_extracts_brackets_with_leading_zero_band():
    record = _record("bracket_schedule", "/1", [Bracket(threshold=0, rate=0.0)])
    draft = mock.propose_with_mock(record, date(2025, 6, 1), [_hit()])
    assert draft.found
    assert [b.threshold for b in draft.value_brackets] == [0, 11497, 29315, 180294]
    assert draft.value_brackets[1].rate == 0.11
    assert draft.valid_from == date(2025, 1, 1)
    assert draft.supporting_extract in FR_TEXT  # verbatim contract


def test_mock_scalar_uses_band_rates_not_incidental_percentages():
    record = _record("scalar", "/1", 0.45)
    draft = mock.propose_with_mock(record, date(2025, 6, 1), [_hit()])
    assert draft.found
    assert draft.value_scalar == 0.45  # not the 45,25 % réduction clause


def test_mock_ignores_hybrid_only_hits():
    record = _record("scalar", "/1", 0.2)
    draft = mock.propose_with_mock(record, date(2025, 6, 1), [_hit(method="hybrid")])
    assert not draft.found


def test_values_equal_and_current_value():
    a = [Bracket(threshold=0, rate=0.0), Bracket(threshold=11294, rate=0.11)]
    b = [Bracket(threshold=0, rate=0.0), Bracket(threshold=11497, rate=0.11)]
    assert _values_equal(a, a.copy())
    assert not _values_equal(a, b)
    record = _record("scalar", "/1", 0.45)
    assert _current_value(record, date(2025, 6, 1)).value == 0.45
    assert _current_value(record, date(2023, 6, 1)) is None


def test_unchanged_routing_keeps_the_current_validity_window():
    # same value as the one in force -> no new period starts, whatever date the
    # model read off the (re-confirming) legal text
    current = ParameterValue(value=0.45, valid_from=date(2024, 1, 1))
    proposed = ParameterValue(
        value=0.45, valid_from=date(2025, 1, 1), valid_to=date(2025, 12, 31)
    )
    kept = _unchanged_window(proposed, current)
    assert kept.valid_from == date(2024, 1, 1)
    assert kept.valid_to is None
    assert kept.value == 0.45


def test_queue_roundtrip_preserves_reviewed_items(tmp_path: Path):
    record = _record("scalar", "/1", 0.45)
    item = ReviewItem(
        id="fr_test_2025-06-01",
        run_id="run-1",
        created_at="2026-07-09T00:00:00Z",
        country="FR",
        model_target="euromod://FR/test",
        as_of=date(2025, 6, 1),
        value_type="scalar",
        unit="/1",
        routing=Routing.UNCHANGED,
        proposed_record=record,
    )
    assert queue_store.write_item(item, tmp_path)
    loaded = queue_store.load_items(tmp_path)
    assert loaded[0].id == item.id

    # a decided item is not overwritten without force
    decided = item.model_copy(update={"status": ItemStatus.ACCEPTED})
    assert queue_store.write_item(decided, tmp_path, force=True)
    assert not queue_store.write_item(item, tmp_path)
    assert queue_store.write_item(item, tmp_path, force=True)


def test_derived_refs_detects_formula_parameters():
    from nomoscope_workflow.pipeline import _derived_refs
    from nomoscope_workflow.schema import Lineage

    record = ParameterRecord(
        information=ParameterInformation(
            country="FR",
            model_target="euromod://FR/tinty_fr/def_const/$csg_red_thres",
            value_type="scalar",
            unit="currency",
        ),
        values=[
            ParameterValue(
                value=185568.0,
                valid_from=date(2024, 1, 1),
                lineage=Lineage(model_answer="$PSS * 4"),
            )
        ],
    )
    current = _current_value(record, date(2025, 6, 1))
    assert _derived_refs(record, current) == ["$PSS"]

    # a plain numeric answer is not derived, and a self-reference does not count
    plain = record.model_copy(deep=True)
    plain.values[0].lineage.model_answer = "11496#y"
    assert _derived_refs(plain, _current_value(plain, date(2025, 6, 1))) == []
    self_ref = record.model_copy(deep=True)
    self_ref.values[0].lineage.model_answer = "$csg_red_thres"
    assert _derived_refs(self_ref, _current_value(self_ref, date(2025, 6, 1))) == []
    assert _derived_refs(record, None) == []


def test_income_year_shifts_retrieval_date():
    # FR barème: the finance act for income year 2025 is consolidated in 2026,
    # so version selection must look a year ahead of as_of.
    bareme = _record("bracket_schedule", "/1", None, temporal_basis=TemporalBasis.INCOME_YEAR)
    assert _retrieval_as_of(bareme, date(2025, 6, 1)) == date(2026, 7, 1)
    in_force = _record("scalar", "/1", 0.45)  # default basis: unchanged
    assert _retrieval_as_of(in_force, date(2025, 6, 1)) == date(2025, 6, 1)


def test_income_year_mock_backdates_valid_from_to_income_year_start():
    record = _record(
        "bracket_schedule", "/1", [Bracket(threshold=0, rate=0.0)],
        temporal_basis=TemporalBasis.INCOME_YEAR,
    )
    # version consolidated 2026-02-21 (LF 2026) -> proposal back-dated to 2025-01-01
    draft = mock.propose_with_mock(record, date(2025, 6, 1), [_hit(validity="[2026-02-21,)")])
    assert draft.found
    assert draft.valid_from == date(2025, 1, 1)


def test_income_year_date_issues():
    # act for income year 2025 consolidated Feb 2026, proposal back-dated: consistent
    assert _income_year_date_issues(date(2025, 1, 1), date(2026, 2, 21), 2025) == ([], False)
    # LF 2025 slipped to February 2025 (censure): still inside the 2024 window
    assert _income_year_date_issues(date(2024, 1, 1), date(2025, 2, 15), 2024) == ([], False)
    # valid_from not back-dated to the income-year start — a proposal defect, not provisional
    for wrong in (date(2026, 2, 21), date(2025, 2, 16)):
        issues, provisional = _income_year_date_issues(wrong, date(2026, 2, 21), 2025)
        assert any("2025-01-01" in i for i in issues) and not provisional
    # stale corpus: version from LF 2025 (2024-income barème) cited for income year 2025
    issues, provisional = _income_year_date_issues(date(2025, 1, 1), date(2025, 2, 15), 2025)
    assert any("provisional" in i for i in issues) and provisional
    # CDHR exemption: enacted Feb 2025 FOR 2025 income — the cited text names the
    # income year, which proves the vintage despite predating the December window
    cdhr = "Le I s'applique à compter de l'imposition des revenus de l'année 2025."
    assert _income_year_date_issues(date(2025, 1, 1), date(2025, 2, 15), 2025, cdhr) == ([], False)
    # ...but a text naming some OTHER year does not exempt
    issues, provisional = _income_year_date_issues(
        date(2025, 1, 1), date(2025, 2, 15), 2025, "revenus de l'année 2024"
    )
    assert provisional
    # no cited version validity -> only the back-dating check applies
    assert _income_year_date_issues(date(2025, 1, 1), None, 2025) == ([], False)


def test_cross_article_year_proof():
    from nomoscope_workflow.pipeline import _cross_article_year_proof

    # LF 2025 art. 10 ties CGI art. 224 to income year 2025 by cross-reference
    lf_text = (
        "III. - A. - 1. La contribution mentionnée au I de l'article 224 du code général "
        "des impôts due au titre de l'imposition des revenus de l'année 2025 donne lieu "
        "au versement d'un acompte entre le 1er décembre et le 15 décembre 2025."
    )
    assert _cross_article_year_proof("CGI, art. 224", lf_text, 2025)
    assert not _cross_article_year_proof("CGI, art. 224", lf_text, 2026)
    # a mention of a DIFFERENT article near the year is not proof
    assert not _cross_article_year_proof("CGI, art. 197", lf_text, 2025)
    assert not _cross_article_year_proof(None, lf_text, 2025)
    assert not _cross_article_year_proof("no article here", lf_text, 2025)


def test_year_anchor_and_cli_mapping():
    from nomoscope_workflow.cli import _anchor_date

    assert _anchor_date(2025, None) == date(2025, 7, 1)
    assert _anchor_date(None, "2025-06-01") == date(2025, 6, 1)  # deprecated alias
    import pytest
    import typer

    with pytest.raises(typer.Exit):
        _anchor_date(None, None)
    with pytest.raises(typer.Exit):
        _anchor_date(2025, "2025-06-01")


def test_validity_start_parses_pg_daterange():
    assert validity_start("[2025-02-15,)") == date(2025, 2, 15)
    assert validity_start("(2025-02-15,2026-01-01)") == date(2025, 2, 15)
    assert validity_start(None) is None
    assert validity_start("empty") is None


def test_fts_query_ors_distinct_terms():
    from nomoscope_workflow.retrieval import _fts_query

    q = _fts_query("Taux de la tranche 1 taux marginal de l'impôt")
    assert " OR " in q
    terms = q.split(" OR ")
    assert len(terms) == len(set(terms))  # deduplicated
    assert "taux" in terms and "marginal" in terms
    assert "or" not in terms  # websearch operator keyword never emitted as a term
    assert _fts_query("") == ""  # degenerate input falls through unchanged


def test_scout_country_rules_are_complete_and_render_the_prompt():
    from nomoscope_workflow.scout import COUNTRY_SOURCES, ID_HINTS, SCOUT_SYSTEM

    for country, rules in COUNTRY_SOURCES.items():
        assert rules["domains"] and rules["id_pattern"]
        # A country without an id hint would be asked for "exact official id",
        # which is how the LLM starts inventing identifiers.
        assert country in ID_HINTS
        SCOUT_SYSTEM.format(
            country=country, id_hint=ID_HINTS[country], act_kinds=rules["act_kinds"]
        )


def test_scout_lt_ids_are_harvested_from_e_seimas_urls():
    from nomoscope_workflow.scout import COUNTRY_SOURCES

    pattern = COUNTRY_SOURCES["LT"]["id_pattern"]
    # Both TAR id generations, as they appear in portal URLs.
    legacy = "https://e-seimas.lrs.lt/portal/legalAct/lt/TAD/TAR.C677663D2202/asr"
    modern = "https://e-seimas.lrs.lt/portal/legalAct/lt/TAD/ce0f95d090d111e4bb408baba2bdddf3?jfwid=-1c37ov9nb"
    assert pattern.findall(legacy) == ["TAR.C677663D2202"]
    assert pattern.findall(modern) == ["ce0f95d090d111e4bb408baba2bdddf3"]
    # The consolidation index is what gets ingested: the as-published text alone
    # carries no value history.
    assert COUNTRY_SOURCES["LT"]["ingest_suffix"] == "/asr"


def test_scout_fr_ids_still_exclude_whole_codes():
    from nomoscope_workflow.scout import COUNTRY_SOURCES

    pattern = COUNTRY_SOURCES["FR"]["id_pattern"]
    assert pattern.findall(
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051521140"
    ) == ["LEGIARTI000051521140"]
    assert pattern.findall("https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006069577") == []
