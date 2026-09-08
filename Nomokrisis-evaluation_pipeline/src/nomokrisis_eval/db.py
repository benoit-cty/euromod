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
    """Insert the run row and all case results in one transaction; returns runs.id.

    Idempotent per run_id: storing a run twice (a resumed run whose first store
    failed, say) replaces that run's rows rather than raising on the unique key.
    """
    with conn.transaction():
        row = conn.execute(
            """
            INSERT INTO eval.runs (run_id, created_at, as_of, model_provider, model_name,
                                   critique_model, resolved_model, resolved_critique_model,
                                   prompt_version, agent_version, eval_version,
                                   dataset_version, git_commit, countries, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (run_id) DO UPDATE SET
                created_at = EXCLUDED.created_at,
                as_of = EXCLUDED.as_of,
                model_provider = EXCLUDED.model_provider,
                model_name = EXCLUDED.model_name,
                critique_model = EXCLUDED.critique_model,
                resolved_model = EXCLUDED.resolved_model,
                resolved_critique_model = EXCLUDED.resolved_critique_model,
                prompt_version = EXCLUDED.prompt_version,
                agent_version = EXCLUDED.agent_version,
                eval_version = EXCLUDED.eval_version,
                dataset_version = EXCLUDED.dataset_version,
                git_commit = EXCLUDED.git_commit,
                countries = EXCLUDED.countries,
                notes = EXCLUDED.notes
            RETURNING id
            """,
            (
                manifest.run_id,
                manifest.created_at,
                manifest.as_of,
                manifest.model_provider,
                manifest.model_name,
                manifest.critique_model,
                manifest.resolved_model,
                manifest.resolved_critique_model,
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
        conn.execute("DELETE FROM eval.results WHERE run_pk = %s", (run_pk,))
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO eval.results (run_pk, case_id, country, language, model_target,
                                          difficulty, hazards, source_class, routing_expected,
                                          routing_actual, routing_correct, value_correct,
                                          date_correct, citation_correct, extract_verbatim,
                                          supportedness, critique_pass,
                                          hallucination, retrieval_hit, abstained,
                                          guidance_only,
                                          corpus_available, readiness, confidence,
                                          latency_ms, error, details,
                                          phoenix_trace_id, llm_calls, tokens_prompt,
                                          tokens_completion, energy_kwh, gwp_kgco2eq,
                                          impact_estimated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s)
                """,
                [
                    (
                        run_pk,
                        r.case_id,
                        r.country,
                        r.language,
                        r.model_target,
                        r.difficulty,
                        r.hazards,
                        r.source_class,
                        r.routing_expected,
                        r.routing_actual,
                        r.routing_correct,
                        r.value_correct,
                        r.date_correct,
                        r.citation_correct,
                        r.extract_verbatim,
                        r.supportedness,
                        r.critique_pass,
                        r.hallucination,
                        r.retrieval_hit,
                        r.abstained,
                        r.guidance_only,
                        r.corpus_available,
                        r.readiness,
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
                        r.impact_estimated,
                    )
                    for r in results
                ],
            )
    return run_pk


def fetch_difficulty(conn: psycopg.Connection, run_pks: list[int]) -> list[dict]:
    """Rows from eval.run_difficulty for the given runs (ready cases only)."""
    if not run_pks:
        return []
    with conn.cursor(row_factory=dict_row) as cur:
        return cur.execute(
            "SELECT * FROM eval.run_difficulty WHERE run_pk = ANY(%s) "
            "ORDER BY run_pk, language, difficulty",
            (run_pks,),
        ).fetchall()


def fetch_hazards(conn: psycopg.Connection, run_pks: list[int]) -> list[dict]:
    """Rows from eval.run_hazards for the given runs (ready cases only)."""
    if not run_pks:
        return []
    with conn.cursor(row_factory=dict_row) as cur:
        return cur.execute(
            "SELECT * FROM eval.run_hazards WHERE run_pk = ANY(%s) "
            "ORDER BY run_pk, language, hazard",
            (run_pks,),
        ).fetchall()


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
