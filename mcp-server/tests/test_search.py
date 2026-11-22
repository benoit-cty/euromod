from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from nomotheca_mcp.search import _SEARCH_SQL, search


def test_search_sql_is_the_shared_function_and_exposes_rank_components() -> None:
    assert "search_chunks(" in _SEARCH_SQL
    assert "source_trust_class" in _SEARCH_SQL
    assert "full_text_contribution" in _SEARCH_SQL
    assert "vector_contribution" in _SEARCH_SQL
    # Never the shape that walks HNSW and filters afterwards (code audit D9).
    assert "ORDER BY e.embedding" not in _SEARCH_SQL


def test_full_text_search_does_not_require_vector() -> None:
    cursor = MagicMock()
    cursor.__enter__.return_value = cursor
    cursor.fetchall.return_value = []
    conn = MagicMock()
    conn.cursor.return_value = cursor

    assert search(conn, query="income tax threshold", mode="full_text", query_vector=None, model_id=1) == []
    params = cursor.execute.call_args.args[1]
    assert params["query_vector"] is None
    assert params["candidates"] == 32
    assert params["use_fts"] is True


def test_vector_search_requires_vector() -> None:
    with pytest.raises(ValueError, match="requires a query vector"):
        search(MagicMock(), query="income tax", mode="vector", query_vector=None, model_id=1)


def test_search_rejects_unbounded_limit() -> None:
    with pytest.raises(ValueError, match="between 1 and 50"):
        search(MagicMock(), query="income tax", mode="full_text", query_vector=None, model_id=1, limit=51)


def test_country_reports_are_never_returned() -> None:
    """Live: a query that matches Country Report text returns no 'context' chunk (D2)."""
    import os

    import psycopg

    url = os.getenv("DATABASE_URL", "postgresql://jrc:jrc@localhost:5434/legislation")
    try:
        conn = psycopg.connect(url, connect_timeout=2)
    except psycopg.OperationalError:
        pytest.skip("database not reachable")
    with conn:
        hits = search(
            conn,
            query="EUROMOD simulates the income tax",
            mode="full_text",
            query_vector=None,
            model_id=1,
            country="FR",
            languages=["en"],
            limit=20,
        )
    assert hits
    assert all(hit.source_trust_class != "context" for hit in hits)
