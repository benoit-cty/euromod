"""Postgres persistence for evaluation runs (schema: db/eval_schema.sql).

A run is rows only (ADR 0004): eval.runs (the manifest, with `status`),
eval.run_cases (the frozen case list) and eval.results (one row per scored
case, upserted as it lands, carrying the ReviewItem for `rescore`). The golden
set itself lives in `golden_store`."""

from __future__ import annotations

from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from .schema import CaseResult, GoldenCase, RunManifest

SCHEMA_SQL = Path(__file__).resolve().parents[2] / "db" / "eval_schema.sql"


def connect(database_url: str) -> psycopg.Connection:
    return psycopg.connect(database_url)


def apply_schema(conn: psycopg.Connection) -> None:
    conn.execute(SCHEMA_SQL.read_text(encoding="utf-8"))
    conn.commit()


def insert_run(conn: psycopg.Connection, manifest: RunManifest) -> int:
    """Upsert the eval.runs row for a manifest; returns runs.id.

    Idempotent per run_id, so a manifest can be re-stored (rescore, status
    flip) without touching the results already attached to it.
    """
    row = conn.execute(
        """
        INSERT INTO eval.runs (run_id, created_at, as_of, model, model_provider, model_name,
                               critique_model, resolved_model, resolved_critique_model,
                               prompt_version, agent_version, eval_version,
                               dataset_version, git_commit, countries, notes,
                               status, submitted_by, finished_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, coalesce(%s, current_user), %s)
        ON CONFLICT (run_id) DO UPDATE SET
            created_at = EXCLUDED.created_at,
            as_of = EXCLUDED.as_of,
            model = EXCLUDED.model,
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
            notes = EXCLUDED.notes,
            status = EXCLUDED.status,
            finished_at = EXCLUDED.finished_at
        RETURNING id
        """,
        (
            manifest.run_id,
            manifest.created_at,
            manifest.as_of,
            manifest.model,
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
            manifest.status,
            manifest.submitted_by,
            manifest.finished_at,
        ),
    ).fetchone()
    conn.commit()
    return row[0]


def freeze_run_cases(conn: psycopg.Connection, run_pk: int, cases: list[GoldenCase]) -> None:
    """The case list a run scores, frozen at start: resuming replays exactly
    it, not whatever the golden set filters would select later."""
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO eval.run_cases (run_pk, case_id, "case") VALUES (%s, %s, %s)
            ON CONFLICT (run_pk, case_id) DO UPDATE SET "case" = EXCLUDED."case"
            """,
            [(run_pk, case.id, Jsonb(case.model_dump(mode="json", exclude_none=True))) for case in cases],
        )
    conn.commit()


def set_run_status(conn: psycopg.Connection, run_pk: int, status: str) -> None:
    conn.execute(
        """UPDATE eval.runs SET status = %s,
                  finished_at = CASE WHEN %s = 'running' THEN NULL ELSE now() END
           WHERE id = %s""",
        (status, status, run_pk),
    )
    conn.commit()


def upsert_result(
    conn: psycopg.Connection, run_pk: int, result: CaseResult, review_item: dict | None = None
) -> None:
    """One eval.results row per (run, case), written the moment the case is
    scored — the crash-safety that results.jsonl used to give. `review_item`
    is the ReviewItem dump so `rescore` can replay scoring without tokens; a
    None keeps whatever the row already holds."""
    conn.execute(
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
                                  impact_estimated, review_item)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s)
        ON CONFLICT (run_pk, case_id) DO UPDATE SET
            country = EXCLUDED.country,
            language = EXCLUDED.language,
            model_target = EXCLUDED.model_target,
            difficulty = EXCLUDED.difficulty,
            hazards = EXCLUDED.hazards,
            source_class = EXCLUDED.source_class,
            routing_expected = EXCLUDED.routing_expected,
            routing_actual = EXCLUDED.routing_actual,
            routing_correct = EXCLUDED.routing_correct,
            value_correct = EXCLUDED.value_correct,
            date_correct = EXCLUDED.date_correct,
            citation_correct = EXCLUDED.citation_correct,
            extract_verbatim = EXCLUDED.extract_verbatim,
            supportedness = EXCLUDED.supportedness,
            critique_pass = EXCLUDED.critique_pass,
            hallucination = EXCLUDED.hallucination,
            retrieval_hit = EXCLUDED.retrieval_hit,
            abstained = EXCLUDED.abstained,
            guidance_only = EXCLUDED.guidance_only,
            corpus_available = EXCLUDED.corpus_available,
            readiness = EXCLUDED.readiness,
            confidence = EXCLUDED.confidence,
            latency_ms = EXCLUDED.latency_ms,
            error = EXCLUDED.error,
            details = EXCLUDED.details,
            phoenix_trace_id = EXCLUDED.phoenix_trace_id,
            llm_calls = EXCLUDED.llm_calls,
            tokens_prompt = EXCLUDED.tokens_prompt,
            tokens_completion = EXCLUDED.tokens_completion,
            energy_kwh = EXCLUDED.energy_kwh,
            gwp_kgco2eq = EXCLUDED.gwp_kgco2eq,
            impact_estimated = EXCLUDED.impact_estimated,
            review_item = coalesce(EXCLUDED.review_item, eval.results.review_item)
        """,
        (
            run_pk,
            result.case_id,
            result.country,
            result.language,
            result.model_target,
            result.difficulty,
            result.hazards,
            result.source_class,
            result.routing_expected,
            result.routing_actual,
            result.routing_correct,
            result.value_correct,
            result.date_correct,
            result.citation_correct,
            result.extract_verbatim,
            result.supportedness,
            result.critique_pass,
            result.hallucination,
            result.retrieval_hit,
            result.abstained,
            result.guidance_only,
            result.corpus_available,
            result.readiness,
            result.confidence,
            result.latency_ms,
            result.error,
            Jsonb(result.model_dump(mode="json")),
            result.phoenix_trace_id,
            result.llm_calls,
            result.tokens_prompt,
            result.tokens_completion,
            result.energy_kwh,
            result.gwp_kgco2eq,
            result.impact_estimated,
            Jsonb(review_item) if review_item is not None else None,
        ),
    )
    conn.commit()


def _manifest_from_row(row: dict) -> RunManifest:
    return RunManifest(
        run_id=row["run_id"],
        created_at=row["created_at"],
        status=row["status"],
        submitted_by=row["submitted_by"],
        finished_at=row["finished_at"],
        as_of=row["as_of"],
        # Runs stored before `model` existed: rebuild the prefixed string.
        model=row["model"] or f"{row['model_provider']}/{row['model_name']}",
        model_provider=row["model_provider"],
        model_name=row["model_name"],
        critique_model=row["critique_model"],
        resolved_model=row["resolved_model"],
        resolved_critique_model=row["resolved_critique_model"],
        prompt_version=row["prompt_version"],
        agent_version=row["agent_version"],
        eval_version=row["eval_version"],
        dataset_version=row["dataset_version"],
        git_commit=row["git_commit"],
        countries=list(row["countries"] or []),
        notes=row["notes"],
    )


def load_run(conn: psycopg.Connection, run_id: str) -> tuple[int, RunManifest] | None:
    with conn.cursor(row_factory=dict_row) as cur:
        row = cur.execute("SELECT * FROM eval.runs WHERE run_id = %s", (run_id,)).fetchone()
    return (row["id"], _manifest_from_row(row)) if row else None


def list_runs(conn: psycopg.Connection, limit: int | None = None) -> list[dict]:
    """Every run, newest first: manifest + done/total progress from the tables."""
    query = """
        SELECT r.*,
               (SELECT count(*) FROM eval.run_cases rc WHERE rc.run_pk = r.id) AS total,
               (SELECT count(*) FROM eval.results res WHERE res.run_pk = r.id) AS done
        FROM eval.runs r
        ORDER BY r.created_at DESC
    """
    params: tuple = ()
    if limit is not None:
        query += " LIMIT %s"
        params = (limit,)
    with conn.cursor(row_factory=dict_row) as cur:
        rows = cur.execute(query, params).fetchall()
    return [
        {
            "run_id": row["run_id"],
            "run_pk": row["id"],
            "manifest": _manifest_from_row(row),
            "done": row["done"],
            "total": row["total"],
            "status": row["status"],
            # A run written before run_cases existed has no frozen list; it
            # was stored whole, so it is complete by construction.
            "complete": row["status"] == "complete"
            or (row["total"] > 0 and row["done"] >= row["total"]),
        }
        for row in rows
    ]


def load_run_cases(conn: psycopg.Connection, run_pk: int) -> list[GoldenCase]:
    rows = conn.execute(
        'SELECT "case" FROM eval.run_cases WHERE run_pk = %s ORDER BY case_id', (run_pk,)
    ).fetchall()
    return [GoldenCase.model_validate(row[0]) for row in rows]


def load_results(conn: psycopg.Connection, run_pk: int) -> list[CaseResult]:
    """Every result scored so far, from the full CaseResult dump in `details`."""
    rows = conn.execute(
        "SELECT details FROM eval.results WHERE run_pk = %s ORDER BY id", (run_pk,)
    ).fetchall()
    return [CaseResult.model_validate(row[0]) for row in rows if row[0]]


def load_review_items(conn: psycopg.Connection, run_pk: int) -> dict[str, dict]:
    """case_id -> ReviewItem dump, for the cases whose item was stored."""
    rows = conn.execute(
        "SELECT case_id, review_item FROM eval.results WHERE run_pk = %s AND review_item IS NOT NULL",
        (run_pk,),
    ).fetchall()
    return {case_id: item for case_id, item in rows}


def insert_embedding_run(conn: psycopg.Connection, manifest: dict, results: list) -> int:
    """A retrieval-eval run: manifest + results as JSON (was .eval_runs/embeval-*/)."""
    row = conn.execute(
        """
        INSERT INTO eval.embedding_runs (run_id, manifest, results) VALUES (%s, %s, %s)
        ON CONFLICT (run_id) DO UPDATE SET manifest = EXCLUDED.manifest, results = EXCLUDED.results
        RETURNING id
        """,
        (manifest["run_id"], Jsonb(manifest), Jsonb([r.model_dump(mode="json") for r in results])),
    ).fetchone()
    conn.commit()
    return row[0]


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
