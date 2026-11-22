"""Reference dates: income-year and start-of-year bases, validity ranges, year anchors."""

from __future__ import annotations

from datetime import date

from nomoscope_workflow import mock
from nomoscope_workflow.corpus import validity_start
from nomoscope_workflow.locate import _entered_since
from nomoscope_workflow.prompts import _parameter_block
from nomoscope_workflow.schema import (
    Bracket,
    ParameterRecord,
    TemporalBasis,
    income_year_for,
    system_year_anchor,
)
from nomoscope_workflow.temporal import (
    _cross_article_year_proof,
    _income_year_date_issues,
    _later_until,
    _retrieval_as_of,
)
from workflow_fixtures import _hit, _record


def test_income_year_maps_system_year_to_the_previous_income_year():
    # «impôt 2025 sur les revenus 2024»: system year 2025 holds the schedule the law labels income 2024.
    assert income_year_for(2025) == 2024


def test_income_year_shifts_retrieval_date():
    # System year 2025 = income year 2024, whose barème is enacted by LF 2025
    # (Feb 2025) — so version selection targets mid-2025, not as_of.
    bareme = _record("bracket_schedule", "/1", None, temporal_basis=TemporalBasis.INCOME_YEAR)
    assert _retrieval_as_of(bareme, date(2025, 6, 1)) == date(2025, 7, 1)
    in_force = _record("scalar", "/1", 0.45)  # default basis: unchanged
    assert _retrieval_as_of(in_force, date(2025, 6, 1)) == date(2025, 6, 1)


def test_start_of_year_retrieves_on_1_january_and_ignores_later_versions():
    # $tpr_threshold4: CGI 1417 is revised each June; EUROMOD 2025 holds 6 843,
    # the version in force on 1 January 2025, not the 6 966 of 19 June.

    threshold = _record("scalar", "currency", 6843, temporal_basis=TemporalBasis.START_OF_YEAR)
    assert _retrieval_as_of(threshold, date(2025, 7, 1)) == date(2025, 1, 1)
    assert _later_until(threshold, date(2025, 7, 1)) is None
    assert _later_until(_record("scalar", "currency", 1.0), date(2025, 7, 1)) == date(2025, 12, 31)


def test_income_year_mock_backdates_valid_from_to_income_year_start():
    record = _record(
        "bracket_schedule",
        "/1",
        [Bracket(threshold=0, rate=0.0)],
        temporal_basis=TemporalBasis.INCOME_YEAR,
    )
    # version consolidated 2025-02-14 (LF 2025) -> proposal back-dated to the
    # income year it governs, 2024-01-01 — not to the system year.
    draft = mock.propose_with_mock(record, date(2025, 6, 1), [_hit(validity="[2025-02-14,)")])
    assert draft.found
    assert draft.valid_from == date(2024, 1, 1)


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
    issues, provisional = _income_year_date_issues(date(2025, 1, 1), date(2025, 2, 15), 2025, "revenus de l'année 2024")
    assert provisional
    # no cited version validity -> only the back-dating check applies
    assert _income_year_date_issues(date(2025, 1, 1), None, 2025) == ([], False)


def test_cross_article_year_proof():
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


def test_cross_article_year_proof_reads_a_terminal_applicability_clause():
    """How finance acts are actually drafted: the amendment at the top, the
    clause that dates it at the bottom. In LF 2025 art. 2 those are 5 166
    characters apart, so a proximity window can never connect them — and every
    FR barème case refused because of it."""
    lf_art2 = (
        "I. - Le code général des impôts est ainsi modifié : B. - Le I de l'article 197 "
        "est ainsi modifié : a) le montant « 11 294 € » est remplacé par « 11 497 € » ; " + "b) " + "x" * 5000 + " ; "
        "II. - Les A et B du I s'appliquent à l'impôt sur le revenu dû au titre de "
        "l'année 2024 et des années suivantes."
    )
    assert _cross_article_year_proof("CGI, art. 197", lf_art2, 2024)
    # the clause dates the whole article, but only for articles it actually
    # names: an article the text never mentions is still not proven
    assert not _cross_article_year_proof("CGI, art. 196 B", lf_art2, 2024)
    # and it proves only the year it names
    assert not _cross_article_year_proof("CGI, art. 197", lf_art2, 2023)
    # a bare year with no applicability clause in front of it is not a proof
    bare = "Le I de l'article 197 est ainsi modifié. " + "x" * 5000 + " Rapport 2024."
    assert not _cross_article_year_proof("CGI, art. 197", bare, 2024)


def test_income_year_prompt_states_the_income_year_not_the_system_year():
    """The prompt and the mechanical date check must agree on the year, or the
    model is asked to prove something the act does not say and refuses. They
    disagreed: the prompt demanded valid_from 2025-01-01 for system year 2025
    while _income_year_date_issues demanded 2024-01-01."""
    record = ParameterRecord.model_validate(
        {
            "information": {
                "country": "FR",
                "model_target": "euromod://FR/tinkt_fr/def_const/$tin_rate1",
                "value_type": "scalar",
                "unit": "rate",
                "temporal_basis": "income_year",
            },
            "values": [],
        }
    )
    block = _parameter_block(record, date(2025, 6, 1))
    assert "income year 2024" in block
    assert "valid_from must be 2024-01-01" in block
    assert "2025-01-01" not in block


def test_year_anchor_and_cli_mapping():
    assert system_year_anchor(2025) == date(2025, 7, 1)


def test_validity_start_parses_pg_daterange():
    assert validity_start("[2025-02-15,)") == date(2025, 2, 15)
    assert validity_start("(2025-02-15,2026-01-01)") == date(2025, 2, 15)
    assert validity_start(None) is None
    assert validity_start("empty") is None


def test_a_version_entered_since_reads_the_range_start():
    assert _entered_since("[2025-04-01,)", date(2024, 7, 1))
    assert not _entered_since("[2006-01-01,)", date(2024, 7, 1))
    assert not _entered_since(None, date(2024, 7, 1))
