"""Live adversarial test for ADR 0003, against the running legislation DB.

The false positive a region-blind corpus produces cannot be caught by the
verbatim-extract check: a quote from Asturias's decree is a real quote, it is
merely the wrong region's law for Aragón's parameter. So the guarantee has to
hold at retrieval, and it is asserted here against real chunks: Aragón's scope
never returns an Asturias chunk — not even when the Asturias citation is named
explicitly — while Asturias's own scope does return it (so the test cannot pass
vacuously), and the national scope returns no regional chunk at all.

Skipped when the DB is unreachable or the regional acts are not ingested.
"""

from __future__ import annotations

from datetime import date

import pytest

from nomoscope_workflow import retrieval
from nomoscope_workflow.config import load_config
from nomoscope_workflow.regions import region_key

AS_OF = date(2025, 6, 1)
ARAGON = "euromod://ES/bsarg_es/def_const/$bsarg_rg24_basic_amt"
ASTURIAS_CITATION = "Ley 3/2021 Asturias Artículo\u00a014"  # BOE unit titles carry a NBSP
QUERY = "salario social básico cuantía mensual prestación garantía de derechos vitales Asturias"

_CHUNK_JURISDICTION = """
SELECT j.code
FROM chunks c
JOIN unit_texts t          ON t.id = c.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u         ON u.id = v.legal_unit_id
JOIN instruments i         ON i.id = u.instrument_id
JOIN jurisdictions j       ON j.id = i.jurisdiction_id
WHERE c.id = %(chunk_id)s::uuid
"""


@pytest.fixture(scope="module")
def conn():
    cfg = load_config()
    try:
        connection = retrieval.connect(cfg)
    except Exception as exc:  # no stack up: this suite is opt-in by environment
        pytest.skip(f"legislation DB unreachable: {exc}")
    with connection:
        for code in ("ES-AS", "ES-AR"):
            row = connection.execute(
                "SELECT count(*) AS n FROM instruments i JOIN jurisdictions j ON j.id = i.jurisdiction_id "
                "WHERE j.code = %s",
                (code,),
            ).fetchone()
            if not row["n"]:
                pytest.skip(f"no instrument ingested under {code}")
        yield connection


def _jurisdictions_of(conn, hits) -> set[str]:
    return {conn.execute(_CHUNK_JURISDICTION, {"chunk_id": h.chunk_id}).fetchone()["code"] for h in hits}


def test_the_aragon_scope_is_the_country_plus_aragon(conn):
    assert retrieval.jurisdiction_scope(conn, "ES", region_key("ES", ARAGON)) == ["ES", "ES-AR"]
    assert retrieval.jurisdiction_scope(conn, "ES", None) == ["ES"]
    # an unknown region falls back to the country alone, the safe side
    assert retrieval.jurisdiction_scope(conn, "ES", "ES99") == ["ES"]


def test_aragons_run_cannot_retrieve_asturias_even_by_an_asturias_query(conn):
    aragon = retrieval.jurisdiction_scope(conn, "ES", "ES24")
    asturias = retrieval.jurisdiction_scope(conn, "ES", "ES12")
    in_aragon = retrieval.hybrid_search(conn, aragon, "es", AS_OF, QUERY, 0, 50, None)
    in_asturias = retrieval.hybrid_search(conn, asturias, "es", AS_OF, QUERY, 0, 50, None)
    assert _jurisdictions_of(conn, in_aragon) <= {"ES", "ES-AR"}
    reached = _jurisdictions_of(conn, in_asturias)
    assert "ES-AS" in reached, "the Asturias act is not retrievable in its own scope — vacuous test"
    assert "ES-AR" not in reached


def test_naming_the_sibling_citation_does_not_pull_it_into_the_scope(conn):
    aragon = retrieval.jurisdiction_scope(conn, "ES", "ES24")
    asturias = retrieval.jurisdiction_scope(conn, "ES", "ES12")
    # The citation fast path is a trigram match, so "Ley 3/2021 Asturias
    # Artículo 14" also resembles Aragón's own "Ley 3/2021 Aragón Artículo 14"
    # closely enough to return it — that is in scope and fine. What must never
    # come back is an ES-AS chunk.
    in_aragon = retrieval.citation_fast_path(conn, aragon, "es", AS_OF, [ASTURIAS_CITATION], 10)
    assert _jurisdictions_of(conn, in_aragon) <= {"ES", "ES-AR"}
    in_asturias = retrieval.citation_fast_path(conn, asturias, "es", AS_OF, [ASTURIAS_CITATION], 10)
    assert "ES-AS" in _jurisdictions_of(conn, in_asturias)


def test_the_national_scope_sees_no_regional_act(conn):
    hits = retrieval.hybrid_search(conn, ["ES"], "es", AS_OF, QUERY, 0, 50, None)
    assert hits, "no state-law hit at all for a Spanish query"
    assert _jurisdictions_of(conn, hits) == {"ES"}
