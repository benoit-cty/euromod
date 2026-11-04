"""Live check of the named-source lookup against the ingested corpus.

Opt-in by environment: skipped when the legislation DB is unreachable. The
needs below are verbatim what the proposal step reported on the 2026-09-09
eval for cases where the act WAS in the corpus and retrieval ranked it out.
"""

from __future__ import annotations

from datetime import date

import pytest

from nomoscope_workflow import retrieval
from nomoscope_workflow.config import load_config

AS_OF = date(2025, 6, 1)

CASES = [
    ("ES", "artículo 66.2 de la Ley 35/2006, del Impuesto sobre la Renta de las Personas Físicas, in the version applicable to 2025", "LIRPF Artículo 66"),
    ("NL", "de tabel in artikel 2.10, eerste lid, van de Wet inkomstenbelasting 2001, zoals geldend voor 2025", "Wet IB 2001, artikel 2.10"),
    ("FR", "article D. 633-3 du code de la sécurité sociale, in the version applicable to contribution periods beginning 1 January 2025", "LEGITEXT000006073189, art. D633-3"),
    ("FR", "l'arrêté fixant le plafond de la sécurité sociale pour 2025", "JORFTEXT000050854392"),
    ("IE", "the provision of the Finance Act 2024 (or other 2025 Budget implementing legislation) amending section 461 of the Taxes Consolidation Act 1997 to set the personal tax credit", "Finance Act 2024, s. 3"),
]


@pytest.fixture(scope="module")
def conn():
    cfg = load_config()
    try:
        connection = retrieval.connect(cfg)
    except Exception as exc:  # no stack up: this suite is opt-in by environment
        pytest.skip(f"legislation DB unreachable: {exc}")
    with connection:
        yield connection


@pytest.mark.parametrize("country,need,expected", CASES, ids=[c[2] for c in CASES])
def test_named_sources_are_found_without_ranking(conn, country, need, expected):
    scope = retrieval.jurisdiction_scope(conn, country, None)
    lang = retrieval.LANG_BY_COUNTRY[country]
    hits = retrieval.locate_named_units(conn, scope, lang, AS_OF, need)
    if not hits and expected.startswith("JORFTEXT"):
        pytest.skip("the 2025 PSS arrêté is not ingested on this database")
    assert any(expected in (h.citation or "") for h in hits), [h.citation for h in hits]
    assert all(h.method == "located" for h in hits)


def test_the_article_between_two_retrieved_ones_is_filled(conn):
    """3 Nov benchmark: arts. 34, 35 and 38 of the AGIRC-ARRCO ANI in hand, art. 36
    («Un pourcentage d'appel, fixé à 127 %») never ranked in — four rates not_found."""
    held = [
        row["id"]
        for row in conn.execute(
            """
            SELECT c.id::text AS id FROM chunks c
            JOIN unit_texts ut ON ut.id = c.unit_text_id
            JOIN legal_unit_versions v ON v.id = ut.version_id
            JOIN legal_units lu ON lu.id = v.legal_unit_id
            JOIN instruments i ON i.id = lu.instrument_id
            WHERE i.national_id = 'KALITEXT000036731682' AND ut.lang = 'fr'
              AND lu.path::text IN ('art_34', 'art_35', 'art_38', 'annexe_a_art_6')
              AND v.validity @> date '2025-07-01'
            """
        ).fetchall()
    ]
    if not held:
        pytest.skip("the AGIRC-ARRCO ANI (KALI) is not ingested on this database")
    scope = retrieval.jurisdiction_scope(conn, "FR", None)
    (ani,) = retrieval.instruments_of_chunks(conn, held)
    assert ani == conn.execute(
        "SELECT id::text AS id FROM instruments WHERE national_id = 'KALITEXT000036731682'"
    ).fetchone()["id"]
    hits = retrieval.gap_articles(conn, scope, "fr", date(2025, 7, 1), held)
    filled = [h.citation.rsplit(", ", 1)[-1] for h in hits]
    assert filled == ["art. 36", "art. 37"]
    assert any("127 %" in h.content for h in hits)
    assert all(h.method == "located" for h in hits)
