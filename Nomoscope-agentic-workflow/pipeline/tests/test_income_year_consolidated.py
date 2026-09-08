"""Consolidated code articles as income-year evidence, and query cleaning.

Both came out of the 8 Sep 2026 Sol/Luna review: four correct CEHR proposals
(CGI art. 223 sexies, unchanged since 2018) were rejected because no finance
act for income year 2024 restates a value that did not move, and the barème
thresholds were never retrieved because the framed query carried the export's
own wrong number and EUROMOD identifiers.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

from nomoscope_workflow.pipeline import (
    _clean_query_text,
    _consolidated_in_force,
    _income_year_date_issues,
)
from nomoscope_workflow.retrieval import validity_end, validity_start

RETRIEVAL_AS_OF = date(2025, 7, 1)  # system year 2025 -> income year 2024 -> 1 July 2025


def _prov(validity: str, instrument_type: str = "code", retrieved: str = "2026-09-01"):
    return {
        "instrument_type": instrument_type,
        "validity": validity,
        "open_ended": validity.endswith(",)"),
        "retrieved_at": datetime.fromisoformat(retrieved).replace(tzinfo=timezone.utc),
    }


def test_validity_end_parses_closed_and_open_ranges():
    assert validity_start("[2025-02-16,2026-02-21)") == date(2025, 2, 16)
    assert validity_end("[2025-02-16,2026-02-21)") == date(2026, 2, 21)
    assert validity_end("[2018-01-01,)") is None


def test_bareme_version_in_force_on_the_retrieval_date_is_the_income_year_text():
    # CGI art. 197 "en vigueur du 16 février 2025 au 21 février 2026": the 2024-income barème
    assert _consolidated_in_force(_prov("[2025-02-16,2026-02-21)"), RETRIEVAL_AS_OF, 2024, "")


def test_old_open_ended_code_version_counts_when_the_snapshot_is_fresh():
    # CGI art. 223 sexies has read the same since 2018: the CEHR thresholds never moved
    assert _consolidated_in_force(_prov("[2018-01-01,)", retrieved="2026-09-01"), RETRIEVAL_AS_OF, 2024, "")
    # ...but a copy fetched before the retrieval date may predate the finance act
    assert not _consolidated_in_force(_prov("[2018-01-01,)", retrieved="2025-01-10"), RETRIEVAL_AS_OF, 2024, "")


def test_presumption_is_for_code_articles_in_force_on_the_date_only():
    assert not _consolidated_in_force(_prov("[2018-01-01,)", instrument_type="loi"), RETRIEVAL_AS_OF, 2024, "")
    # superseded before the retrieval date
    assert not _consolidated_in_force(_prov("[2024-01-01,2025-01-01)"), RETRIEVAL_AS_OF, 2024, "")
    # not yet in force on it
    assert not _consolidated_in_force(_prov("[2026-02-21,)"), RETRIEVAL_AS_OF, 2024, "")
    assert not _consolidated_in_force(None, RETRIEVAL_AS_OF, 2024, "")


def test_text_naming_the_next_income_year_is_not_this_years():
    # CDHR: art. 224 in force Feb 2025, "applicables à l'imposition des revenus de l'année 2025"
    cdhr = "Les I et II de l'article précité sont applicables à l'imposition des revenus de l'année 2025."
    assert not _consolidated_in_force(_prov("[2025-02-16,)"), RETRIEVAL_AS_OF, 2024, cdhr)
    # for income year 2025 it is exactly the text wanted
    assert _consolidated_in_force(_prov("[2025-02-16,)"), date(2026, 7, 1), 2025, cdhr)


def test_income_year_date_issues_accepts_a_consolidated_version():
    # the old rule: a 2018 version cited for income 2024 is "probably last year's value"
    issues, provisional = _income_year_date_issues(date(2024, 1, 1), date(2018, 1, 1), 2024)
    assert provisional and any("provisional" in i for i in issues)
    # with the consolidated presumption established from the corpus, it is consistent
    assert _income_year_date_issues(date(2024, 1, 1), date(2018, 1, 1), 2024, "", True) == ([], False)
    # the back-dating check is untouched by it
    issues, provisional = _income_year_date_issues(date(2025, 2, 16), date(2018, 1, 1), 2024, "", True)
    assert any("2024-01-01" in i for i in issues) and not provisional


def test_clean_query_text_strips_euromod_noise_and_keeps_the_law_words():
    text = (
        "Limite supérieure pour la tranche 1 Seuil de revenu supérieur de la première tranche (0 %) "
        "du barème progressif de l’impôt sur le revenu, fixé à 11 496 EUR pour le revenu imposable "
        "2025 (tableau 2.77). Il est utilisé comme paramètre Band_UpLim dans le calcul tin_fr "
        "« Taxe sur le revenu brut (avant toute correction IMAX) » et le début de la tranche "
        "suivante imposée ($tin_rate3)."
    )
    cleaned = _clean_query_text(text)
    for noise in ("tableau", "Band_UpLim", "tin_fr", "IMAX", "$tin_rate3", "(", "«"):
        assert noise not in cleaned
    # numbers stay: the export's value usually still is the law's, and it is
    # what finds the arrêté ("11,88" for the SMIC)
    for kept in ("barème progressif", "impôt sur le revenu", "tranche", "Seuil de revenu", "11 496"):
        assert kept in cleaned
    # plain text passes through
    assert _clean_query_text("Income tax: higher tax rate") == "Income tax: higher tax rate"
    assert _clean_query_text("") == ""
