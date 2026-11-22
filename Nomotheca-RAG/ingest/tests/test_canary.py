"""Freshness canaries against the corpus (needs the stack up)."""

from __future__ import annotations

import os
from datetime import date

import psycopg
import pytest
from nomotheca_ingest.core.canary import check_canaries, check_fact
from nomotheca_ingest.core.ir import CanaryFact
from nomotheca_ingest.countries.registry import jurisdictions

DB_URL = os.environ.get("EUROMOD_DATABASE_URL", "postgresql://jrc:jrc@localhost:5434/legislation")


@pytest.fixture
def conn():
    try:
        connection = psycopg.connect(DB_URL, connect_timeout=2)
    except psycopg.OperationalError:
        pytest.skip("database not reachable")
    with connection:
        yield connection


def test_no_canary_is_stale(conn):
    results = check_canaries(conn, jurisdictions())
    assert results
    assert [r for r in results if r.status == "stale"] == []


def test_citations_match_exactly_not_by_trigram(conn):
    """Trigram similarity equates «artikel 2.10» and «artikel 10.2»; the canary must not."""
    fact = CanaryFact(citation="Wet IB 2001, artikel 2.10", assert_latest_start_gte=date(2025, 1, 1), reason="t")
    result = check_fact(conn, "NL", fact)
    if result.matched is None:
        pytest.skip("Wet IB 2001 not ingested")
    assert result.matched == "Wet IB 2001, artikel 2.10"
