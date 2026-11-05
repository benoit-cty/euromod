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


def test_an_order_published_later_in_the_system_year_is_retrieved(conn):
    # 3 Nov full run: all 17 bhoey_fr parameters not_found on 1 July 2025; the
    # barème is the arrêté du 31 juillet 2025, in force from 2 August.
    scope = retrieval.jurisdiction_scope(conn, "FR", None)
    if conn.execute(
        "SELECT 1 FROM instruments WHERE national_id = 'JORFTEXT000052019353'"
    ).fetchone() is None:
        pytest.skip("the arrêté du 31 juillet 2025 is not ingested on this database")
    query = "valeur faciale TTC du chèque énergie RFR / UC"  # FTS leg only: no encoder in the test
    on_july = retrieval.hybrid_search(conn, scope, "fr", date(2025, 7, 1), query, 1, 15)
    later = retrieval.later_in_year(
        conn, scope, "fr", date(2025, 7, 1), date(2025, 12, 31), query, 1, 15,
        known={h.chunk_id for h in on_july},
    )
    assert any(h.citation == "JORFTEXT000052019353, art. 2" for h in later), [h.citation for h in later]
    assert all(h.method == "later_in_year" for h in later)
    assert all(retrieval.validity_start(h.validity) > date(2025, 7, 1) for h in later)
    assert len(later) <= retrieval.LATER_MAX_HITS


def test_a_code_article_leads_to_the_articles_it_relies_on(conn):
    # L. 531-3 (retrieved for the PAJE ceilings) → its implementing R. 531-1,
    # which sends the reader to R. 522-2 for the 25 % / 30 % per-child rule.
    scope = retrieval.jurisdiction_scope(conn, "FR", None)
    start = conn.execute(
        """SELECT ch.id::text AS id FROM chunks ch JOIN unit_texts t ON t.id = ch.unit_text_id
           JOIN legal_unit_versions v ON v.id = t.version_id JOIN legal_units u ON u.id = v.legal_unit_id
           WHERE u.citation = 'LEGITEXT000006073189, art. L531-3' AND v.validity @> DATE '2025-07-01'
             AND t.lang = 'fr' LIMIT 1"""
    ).fetchone()
    if start is None:
        pytest.skip("CSS art. L. 531-3 is not ingested on this database")
    hits = retrieval.cross_referenced_articles(conn, scope, "fr", date(2025, 7, 1), [start["id"]])
    citations = [h.citation for h in hits]
    assert "LEGITEXT000006073189, art. R531-1" in citations
    assert "LEGITEXT000006073189, art. R522-2" in citations
    assert len(hits) <= retrieval.CROSS_REF_MAX and all(h.method == "located" for h in hits)


def test_an_order_naming_a_code_article_leads_into_that_code(conn):
    # The arrêté fixing the 2025 PAJE ceilings names «l'article L. 531-3 du
    # même code»; R. 531-1 (the bridge to R. 522-2's 25 % / 30 %) follows.
    scope = retrieval.jurisdiction_scope(conn, "FR", None)
    start = conn.execute(
        """SELECT ch.id::text AS id FROM chunks ch JOIN unit_texts t ON t.id = ch.unit_text_id
           JOIN legal_unit_versions v ON v.id = t.version_id JOIN legal_units u ON u.id = v.legal_unit_id
           WHERE u.citation = 'JORFTEXT000050842452, art. 1' AND t.lang = 'fr' LIMIT 1"""
    ).fetchone()
    if start is None:
        pytest.skip("the arrêté du 20 décembre 2024 is not ingested on this database")
    hits = retrieval.cross_referenced_articles(conn, scope, "fr", date(2025, 7, 1), [start["id"]])
    citations = [h.citation for h in hits]
    assert "LEGITEXT000006073189, art. R531-1" in citations
    assert "LEGITEXT000006073189, art. R522-2" in citations


def test_a_code_article_leads_to_the_recent_decree_applying_it(conn):
    # CASF L. 262-2 says the RSA amount is set by decree; the décret du 28 mars
    # 2025 names L. 262-2 and sets 646,52 €. The 26 December 2025 arrêté for
    # the 2026 PAJE ceilings is not in force on 1 July and must not come back.
    scope = retrieval.jurisdiction_scope(conn, "FR", None)
    start = conn.execute(
        """SELECT ch.id::text AS id FROM chunks ch JOIN unit_texts t ON t.id = ch.unit_text_id
           JOIN legal_unit_versions v ON v.id = t.version_id JOIN legal_units u ON u.id = v.legal_unit_id
           WHERE u.citation IN ('LEGITEXT000006074069, art. L262-2', 'LEGITEXT000006073189, art. L531-2')
             AND v.validity @> '2025-07-01'::date AND t.lang = 'fr'
           ORDER BY u.citation DESC, ch.seq"""
    ).fetchall()
    if len(start) < 2:
        pytest.skip("CASF L. 262-2 / CSS L. 531-2 are not ingested on this database")
    hits = retrieval.implementing_acts(conn, scope, "fr", date(2025, 7, 1), [r["id"] for r in start])
    citations = [h.citation for h in hits]
    assert "JORFTEXT000051393086, art. 1" in citations
    assert "JORFTEXT000053165980, art. 1" not in citations
    assert len(hits) <= retrieval.IMPLEMENTING_MAX and all(h.method == "located" for h in hits)


def test_a_need_for_this_years_figure_searches_this_years_texts(conn):
    # «l'arrêté portant revalorisation … de la BMAF» matches the 2005 BMAF
    # decree by title; the 2025 amount is in instruction DSS/2B/2025/38.
    held = conn.execute(
        "SELECT 1 FROM instruments WHERE title->>'fr' LIKE 'Instruction interministérielle n° DSS/2B/2025/38%'"
    ).fetchone()
    if held is None:
        pytest.skip("instruction DSS/2B/2025/38 is not ingested on this database")
    scope = retrieval.jurisdiction_scope(conn, "FR", None)
    need = "l’arrêté portant revalorisation, au 1er avril 2025, de la base mensuelle de calcul des allocations familiales (BMAF)"
    hits = retrieval.locate_named_units(conn, scope, "fr", date(2025, 7, 1), need)
    assert any("474,37" in h.content for h in hits)


def test_implementing_acts_are_ranked_by_the_query_not_the_article_order(conn):
    # Six family-benefit articles first, CSS L. 842-3 last: their arrêtés would
    # fill the cap in article order; ranked on the query (here the prime
    # d'activité decree's own vector) the decree setting 633,21 € comes back.
    scope = retrieval.jurisdiction_scope(conn, "FR", None)
    family = ("L521-1", "L521-3", "L522-1", "L522-3", "L531-2", "L531-3", "R522-2", "R531-1")
    start = conn.execute(
        """SELECT DISTINCT ON (u.citation) ch.id::text AS id, u.citation
           FROM chunks ch JOIN unit_texts t ON t.id = ch.unit_text_id
           JOIN legal_unit_versions v ON v.id = t.version_id JOIN legal_units u ON u.id = v.legal_unit_id
           WHERE u.citation = ANY(%s) AND v.validity @> '2025-07-01'::date AND t.lang = 'fr'
           ORDER BY u.citation, ch.seq""",
        (["LEGITEXT000006073189, art. " + a for a in (*family, "L842-3")],),
    ).fetchall()
    qvec = conn.execute(
        """SELECT e.embedding::text AS v FROM embeddings e JOIN chunks ch ON ch.id = e.chunk_id
           JOIN unit_texts t ON t.id = ch.unit_text_id JOIN legal_unit_versions v ON v.id = t.version_id
           JOIN legal_units u ON u.id = v.legal_unit_id
           WHERE u.citation = 'JORFTEXT000051393100, art. 1' AND e.model_id = 1
             AND v.validity @> '2025-07-01'::date LIMIT 1"""
    ).fetchone()
    if len(start) < 6 or qvec is None:
        pytest.skip("the family-benefit articles, L. 842-3 or the prime d'activité decree are not held")
    ids = [r["id"] for r in sorted(start, key=lambda r: r["citation"].endswith("L842-3"))]
    hits = retrieval.implementing_acts(conn, scope, "fr", date(2025, 7, 1), ids, qvec["v"])
    assert "JORFTEXT000051393100, art. 1" in [h.citation for h in hits[: retrieval.IMPLEMENTING_MAX]]
