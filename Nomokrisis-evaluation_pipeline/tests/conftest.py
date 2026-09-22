"""Shared fixtures. DB-backed tests run only when the dev Postgres (docker
compose, port 5434) is reachable and `nomokrisis-eval init-db` has created the
eval tables; otherwise they are skipped, never failed."""

from __future__ import annotations

import pytest

from nomokrisis_eval.config import load_eval_config

TEST_PREFIX = "zz_test_"


@pytest.fixture(scope="session")
def database_url() -> str:
    return load_eval_config().database_url


@pytest.fixture
def db(database_url: str):
    """A connection to the dev DB, with every `zz_test_*` row removed afterwards."""
    psycopg = pytest.importorskip("psycopg")
    try:
        conn = psycopg.connect(database_url, connect_timeout=2)
    except Exception as exc:  # stack down: skip, do not fail
        pytest.skip(f"dev Postgres not reachable at {database_url}: {exc}")
    try:
        conn.execute("SELECT 1 FROM eval.golden_cases LIMIT 0")
        conn.execute("SELECT 1 FROM eval.run_cases LIMIT 0")
    except Exception as exc:
        conn.close()
        pytest.skip(f"eval schema not applied (run `nomokrisis-eval init-db`): {exc}")
    conn.rollback()
    try:
        yield conn
    finally:
        conn.rollback()
        _cleanup(conn)
        conn.close()


def _cleanup(conn) -> None:
    like = TEST_PREFIX + "%"
    conn.execute("DELETE FROM eval.golden_cases WHERE id LIKE %s", (like,))
    conn.execute("DELETE FROM eval.embedding_cases WHERE id LIKE %s", (like,))
    conn.execute("DELETE FROM eval.golden_selections WHERE country = 'ZZ'")
    conn.execute("DELETE FROM eval.runs WHERE run_id LIKE %s", (like,))  # cascades to run_cases/results
    conn.execute("DELETE FROM eval.embedding_runs WHERE run_id LIKE %s", (like,))
    conn.commit()
