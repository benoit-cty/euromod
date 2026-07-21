"""Postgres persistence for evaluation runs (schema: db/eval_schema.sql)."""

from __future__ import annotations

import json
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

from .schema import CaseResult, RunManifest

SCHEMA_SQL = Path(__file__).resolve().parents[2] / "db" / "eval_schema.sql"


def connect(database_url: str) -> psycopg.Connection:
    return psycopg.connect(database_url)


def apply_schema(conn: psycopg.Connection) -> None:
    conn.execute(SCHEMA_SQL.read_text(encoding="utf-8"))
    conn.commit()


def insert_run(conn: psycopg.Connection, manifest: RunManifest, results: list[CaseResult]) -> int:
    """Insert the run row and all case results in one transaction; returns runs.id."""
    with conn.transaction():
        row = conn.execute(
            """
            INSERT INTO eval.runs (run_id, created_at, as_of, model_provider, model_name,
                                   prompt_version, agent_version, eval_version,
                                   dataset_version, git_commit, countries, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                manifest.run_id,
                manifest.created_at,
                manifest.as_of,
                manifest.model_provider,
                manifest.model_name,
                manifest.prompt_version,
                manifest.agent_version,
                manifest.eval_version,
                manifest.dataset_version,
                manifest.git_commit,
                manifest.countries,
                manifest.notes,
            ),
        ).fetchone()
        run_pk = row[0]
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO eval.results (run_pk, case_id, country, language, model_target,
                                          difficulty, source_class, routing_expected,
                                          routing_actual, routing_correct, value_correct,
                                          date_correct, citation_correct, supportedness,
                                          hallucination, retrieval_hit, confidence,
                                          latency_ms, error, details,
                                          phoenix_trace_id, llm_calls, tokens_prompt,
                                          tokens_completion, energy_kwh, gwp_kgco2eq)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s)
                """,
                [
                    (
                        run_pk,
                        r.case_id,
                        r.country,
                        r.language,
                        r.model_target,
                        r.difficulty,
                        r.source_class,
                        r.routing_expected,
                        r.routing_actual,
                        r.routing_correct,
                        r.value_correct,
                        r.date_correct,
                        r.citation_correct,
                        r.supportedness,
                        r.hallucination,
                        r.retrieval_hit,
                        r.confidence,
                        r.latency_ms,
                        r.error,
                        json.dumps(r.model_dump(mode="json")),
                        r.phoenix_trace_id,
                        r.llm_calls,
                        r.tokens_prompt,
                        r.tokens_completion,
                        r.energy_kwh,
                        r.gwp_kgco2eq,
                    )
                    for r in results
                ],
            )
    return run_pk


def fetch_summary(conn: psycopg.Connection, run_id: str | None = None, limit: int = 20) -> list[dict]:
    """Rows from eval.run_summary, most recent runs first."""
    query = "SELECT * FROM eval.run_summary"
    params: tuple = ()
    if run_id:
        query += " WHERE run_id = %s"
        params = (run_id,)
    query += " ORDER BY created_at DESC, language LIMIT %s"
    with conn.cursor(row_factory=dict_row) as cur:
        return cur.execute(query, (*params, limit)).fetchall()
