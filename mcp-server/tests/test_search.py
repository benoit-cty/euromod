from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from nomotheca_mcp.search import _search_sql, search


@pytest.mark.parametrize("mode", ["hybrid", "full_text", "vector"])
def test_search_sql_exposes_rank_components(mode: str) -> None:
    sql = _search_sql(mode)

    assert "default_transaction_read_only" not in sql
    assert "full_text_contribution" in sql
    assert "vector_contribution" in sql
    assert "%(country)s" in sql
    assert "%(as_of)s" in sql
    assert "%(languages)s" in sql


def test_full_text_search_does_not_require_vector() -> None:
    cursor = MagicMock()
    cursor.__enter__.return_value = cursor
    cursor.fetchall.return_value = []
    conn = MagicMock()
    conn.cursor.return_value = cursor

    assert search(conn, query="income tax threshold", mode="full_text", query_vector=None) == []
    params = cursor.execute.call_args.args[1]
    assert params["query_vector"] is None
    assert params["limit"] == 32


def test_vector_search_requires_vector() -> None:
    with pytest.raises(ValueError, match="requires a query vector"):
        search(MagicMock(), query="income tax", mode="vector", query_vector=None)


def test_search_rejects_unbounded_limit() -> None:
    with pytest.raises(ValueError, match="between 1 and 50"):
        search(MagicMock(), query="income tax", mode="full_text", query_vector=None, limit=51)
