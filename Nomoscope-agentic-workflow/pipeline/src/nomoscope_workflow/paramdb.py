"""Parameter store in Postgres (schema: db/params_schema.sql).

Two responsibilities:
  1. Stage A/B ingestion — load an enriched country export
     (extracted_parameters/enriched/<CC>.enriched.json) into params.parameters,
     params.model_values and params.parameter_usage. Received fields are stored
     verbatim; the deterministic Stage B normalization (value_numeric,
     model_release, system_year, parsed model_address) is added alongside,
     never instead. Re-ingesting a file replaces its rows.
  2. Stage C persistence — record one extraction_runs row per pipeline run,
     carrying the Phoenix trace id of the run's root span, plus the proposal
     and its evidence references. The file queue stays the UI's primary store;
     the DB write is best-effort (see record_run_safe).
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import psycopg

from .config import WorkflowConfig
from .schema import (
    LegalStatus,
    Lineage,
    ParameterInformation,
    ParameterRecord,
    ParameterValue,
    Reference,
    ReviewItem,
    SourceType,
    TemporalBasis,
)

SCHEMA_SQL = Path(__file__).resolve().parents[2] / "db" / "params_schema.sql"

# ReviewItem source_type -> doc §8 source_class vocabulary.
_SOURCE_CLASS = {
    SourceType.LEGISLATION: "legislation",
    SourceType.ADMINISTRATIVE_GUIDANCE: "administrative_guidance",
    SourceType.OFFICIAL_STATISTICS: "official_statistics",
    SourceType.NATIONAL_TEAM: "national_team",
}


def connect(cfg: WorkflowConfig) -> psycopg.Connection:
    return psycopg.connect(cfg.database_url)


def apply_schema(conn: psycopg.Connection) -> None:
    """Create/refresh the params schema (idempotent)."""
    conn.execute(SCHEMA_SQL.read_text(encoding="utf-8"))
    conn.commit()


# ---------------------------------------------------------------------------
# Stage B: deterministic, explainable derivations (doc §§4-6). No LLM.
# ---------------------------------------------------------------------------


def parse_model_target(model_target: str) -> dict:
    """euromod://FR/tinkt_fr/def_const/$tin_upthres1 -> its structured parts."""
    parts = model_target.removeprefix("euromod://").split("/", 3)
    if len(parts) != 4:
        return {"policy": None, "function": None, "name": None}
    _, policy, function, name = parts
    return {"policy": policy, "function": function, "name": name}


def parse_model_release(lineage_model: str | None) -> str | None:
    """'euromod-connector:EUROMOD_MASTER_VERSION_J2.19' -> 'J2.19'."""
    if not lineage_model:
        return None
    match = re.search(r"EUROMOD_MASTER_VERSION_(.+)$", lineage_model)
    return match.group(1) if match else None


def normalise_value(value) -> tuple[float | None, str]:
    """Received value -> (value_numeric, value_kind). null means 'no scalar', not zero."""
    if isinstance(value, bool):
        return float(value), "numeric"
    if isinstance(value, (int, float)):
        return float(value), "numeric"
    if isinstance(value, str):
        if value.strip().lower() == "n/a":
            return None, "n_a"
        try:
            return float(value), "numeric"
        except ValueError:
            return None, "expression"
    return None, "expression"


def derive_system_year(valid_from: str, valid_to: str | None) -> int | None:
    """Year of a single-year (or open-ended latest) model interval; None for multi-year."""
    start = datetime.strptime(valid_from, "%Y-%m-%d").date()
    if (start.month, start.day) != (1, 1):
        return None
    if valid_to is None:
        return start.year
    end = datetime.strptime(valid_to, "%Y-%m-%d").date()
    if end.year == start.year and (end.month, end.day) == (12, 31):
        return start.year
    return None


def structured_unit(unit: str | None, raw_euromod_value: str | None) -> dict | None:
    """Convenience view of the received unit; never replaces it (doc §6)."""
    out: dict = {}
    if unit and "/" in unit:
        quantity, period = unit.split("/", 1)
        out["quantity"] = {"currency": "money"}.get(quantity, quantity)
        out["period"] = period
    if raw_euromod_value:
        match = re.search(r"#(\w+)$", raw_euromod_value)
        if match:
            out["euromod_suffix"] = f"#{match.group(1)}"
    return out or None


# ---------------------------------------------------------------------------
# Stage A ingestion
# ---------------------------------------------------------------------------


def ingest_file(conn: psycopg.Connection, path: Path) -> dict:
    """Load one enriched export; upsert parameters, replace values and usage.

    Accepts both envelopes: a bare list of records (export 0.1) and the
    0.2.0 object {schema_version, country, parameters, groups}. Received
    Stage B fields (model_address, structured_unit, normalized,
    parameter_group) take precedence; local derivations only fill gaps
    left by older exports.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    records = data["parameters"] if isinstance(data, dict) else data
    groups = data.get("groups", []) if isinstance(data, dict) else []
    stats = {"parameters": 0, "model_values": 0, "usage_edges": 0, "groups": 0}
    with conn.transaction():
        for record in records:
            info = record["information"]
            parameter_id = _upsert_parameter(conn, info, str(path))
            stats["parameters"] += 1
            stats["model_values"] += _replace_values(
                conn, parameter_id, record.get("values", []), info
            )
            stats["usage_edges"] += _replace_usage(conn, parameter_id, info.get("usage") or {})
        for group in groups:
            _upsert_group(conn, group, str(path))
            stats["groups"] += 1
    return stats


def _upsert_parameter(conn: psycopg.Connection, info: dict, source_file: str) -> int:
    address = info.get("model_address") or parse_model_target(info["model_target"])
    row = conn.execute(
        """
        INSERT INTO params.parameters
            (country, model_target, parameter_key, policy, function, name, spine_order,
             value_type, unit, unit_structured, label, short_label, description, explanation,
             classification, coicop, last_confirmed_valid_on, enrichment_lineage,
             parameter_group, source_file, ingested_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())
        ON CONFLICT (model_target) DO UPDATE SET
            country = EXCLUDED.country,
            parameter_key = EXCLUDED.parameter_key,
            policy = EXCLUDED.policy,
            function = EXCLUDED.function,
            name = EXCLUDED.name,
            spine_order = EXCLUDED.spine_order,
            value_type = EXCLUDED.value_type,
            unit = EXCLUDED.unit,
            unit_structured = coalesce(EXCLUDED.unit_structured, params.parameters.unit_structured),
            label = EXCLUDED.label,
            short_label = EXCLUDED.short_label,
            description = EXCLUDED.description,
            explanation = EXCLUDED.explanation,
            classification = EXCLUDED.classification,
            coicop = EXCLUDED.coicop,
            last_confirmed_valid_on = EXCLUDED.last_confirmed_valid_on,
            enrichment_lineage = EXCLUDED.enrichment_lineage,
            parameter_group = EXCLUDED.parameter_group,
            source_file = EXCLUDED.source_file,
            ingested_at = now()
        RETURNING id
        """,
        (
            info["country"],
            info["model_target"],
            info.get("parameter_id"),
            address.get("policy"),
            address.get("function"),
            address.get("name"),
            info.get("spine_order"),
            info["value_type"],
            info["unit"],
            _jsonb(info.get("structured_unit")),
            _jsonb(info.get("label")),
            _jsonb(info.get("short_label")),
            _jsonb(info.get("description")),
            _jsonb(info.get("explanation")),
            _jsonb(info.get("classification")),
            _jsonb(info.get("coicop")),
            info.get("last_confirmed_valid_on"),
            _jsonb(info.get("enrichment_lineage")),
            _jsonb(info.get("parameter_group")),
            source_file,
        ),
    ).fetchone()
    return row[0]


def _upsert_group(conn: psycopg.Connection, group: dict, source_file: str) -> None:
    conn.execute(
        """
        INSERT INTO params.parameter_groups
            (group_id, country, kind, policy, instances, components, source_file, ingested_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, now())
        ON CONFLICT (group_id) DO UPDATE SET
            country = EXCLUDED.country,
            kind = EXCLUDED.kind,
            policy = EXCLUDED.policy,
            instances = EXCLUDED.instances,
            components = EXCLUDED.components,
            source_file = EXCLUDED.source_file,
            ingested_at = now()
        """,
        (
            group["id"],
            group["id"].split(":", 1)[0],
            group.get("kind"),
            group.get("policy"),
            _jsonb(group.get("instances") or []),
            _jsonb(group.get("components") or []),
            source_file,
        ),
    )


def _replace_values(
    conn: psycopg.Connection, parameter_id: int, values: list[dict], info: dict | None = None
) -> int:
    conn.execute("DELETE FROM params.model_values WHERE parameter_id = %s", (parameter_id,))
    rows = []
    unit_probe = None
    for seq, value in enumerate(values):
        lineage = value.get("lineage") or {}
        normalized = value.get("normalized") or {}  # received Stage B (export >= 0.2.0)
        raw_euromod = normalized.get("raw_euromod_value") or lineage.get("model_answer")
        numeric, kind = normalise_value(value["value"])
        if "value" in normalized:
            # 0.2.0 normalizes upstream: value is the scalar or null, and only
            # raw_euromod_value distinguishes an 'n/a' from an expression.
            numeric = normalized["value"]
            if numeric is not None:
                kind = "numeric"
            elif raw_euromod and raw_euromod.strip().lower() == "n/a":
                kind = "n_a"
            else:
                kind = "expression"
        unit_probe = unit_probe or raw_euromod
        rows.append(
            (
                parameter_id,
                seq,
                json.dumps(value["value"], ensure_ascii=False),
                numeric,
                kind,
                raw_euromod,
                normalized.get("model_release") or parse_model_release(lineage.get("model")),
                normalized.get("system_year")
                or derive_system_year(value["valid_from"], value.get("valid_to")),
                value["valid_from"],
                value.get("valid_to"),
                value.get("legal_status"),
                value.get("source_type"),
                value.get("official_journal_date"),
                json.dumps(value.get("references") or [], ensure_ascii=False),
                json.dumps(lineage, ensure_ascii=False),
            )
        )
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO params.model_values
                (parameter_id, seq, value_raw, value_numeric, value_kind,
                 raw_euromod_value, model_release, system_year, valid_from, valid_to,
                 legal_status, source_type, official_journal_date,
                 received_references, lineage)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            rows,
        )
    # Stage B structured-unit hint, derived from unit + suffix — only when the
    # export did not already supply a received structured_unit.
    if not (info or {}).get("structured_unit"):
        row = conn.execute(
            "SELECT unit FROM params.parameters WHERE id = %s", (parameter_id,)
        ).fetchone()
        conn.execute(
            "UPDATE params.parameters SET unit_structured = %s WHERE id = %s",
            (_jsonb(structured_unit(row[0], unit_probe)), parameter_id),
        )
    return len(rows)


def _replace_usage(conn: psycopg.Connection, parameter_id: int, usage: dict) -> int:
    conn.execute("DELETE FROM params.parameter_usage WHERE parameter_id = %s", (parameter_id,))
    rows = []
    for edge in usage.get("defined_in") or []:
        rows.append(
            (
                parameter_id,
                "defined_in",
                edge.get("policy") or "",
                edge.get("function") or "",
                edge.get("function_comment"),
                edge.get("group") or None,
                None,
                edge.get("systems") or [],
                edge.get("source"),
            )
        )
    for edge in usage.get("used_by") or []:
        rows.append(
            (
                parameter_id,
                "used_by",
                edge.get("policy") or "",
                edge.get("function") or "",
                edge.get("function_comment"),
                None,
                edge.get("parameter"),
                edge.get("systems") or [],
                edge.get("source"),
            )
        )
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO params.parameter_usage
                (parameter_id, relation, policy, function, function_comment,
                 group_name, used_in_parameter, systems, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            rows,
        )
    return len(rows)


def _jsonb(value) -> str | None:
    return None if value is None else json.dumps(value, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Record reconstruction — params DB -> Activity 1 record, so the pipeline can
# run parameters that exist only in the DB (e.g. runs launched from the UI's
# Parameters tab). Received jsonb is filtered down to the strict Pydantic
# vocabulary: enriched exports carry extra fields the models reject.
# ---------------------------------------------------------------------------


def _maybe_enum(enum_cls, value):
    """Received text -> enum member, or None when outside the vocabulary."""
    if value is None:
        return None
    try:
        return enum_cls(value)
    except ValueError:
        return None


def _clean_reference(ref: dict) -> Reference | None:
    fields = {k: ref[k] for k in Reference.model_fields if ref.get(k) is not None}
    fields.setdefault("title", ref.get("href") or "reference")
    try:
        return Reference(**fields)
    except Exception:
        return None


def _clean_lineage(lineage: dict) -> Lineage | None:
    fields = {k: lineage[k] for k in Lineage.model_fields if lineage.get(k) is not None}
    if not fields:
        return None
    try:
        return Lineage(**fields)
    except Exception:
        return None


def load_record(conn: psycopg.Connection, target: str) -> ParameterRecord:
    """Rebuild the Activity 1 record for one parameter (model_target or
    parameter_key) from params.parameters + params.model_values."""
    row = conn.execute(
        """
        SELECT id, country, model_target, spine_order, value_type, unit,
               label, short_label, description, explanation, last_confirmed_valid_on,
               temporal_basis
        FROM params.parameters
        WHERE model_target = %s OR parameter_key = %s
        """,
        (target, target),
    ).fetchone()
    if row is None:
        raise KeyError(f"parameter not in params DB (see ingest-params): {target}")
    (parameter_id, country, model_target, spine_order, value_type, unit,
     label, short_label, description, explanation, last_confirmed, temporal_basis) = row

    information = ParameterInformation(
        country=country,
        model_target=model_target,
        spine_order=spine_order,
        value_type=value_type,
        unit=unit or "",
        label=label,
        short_label=short_label,
        description=description,
        explanation=explanation,
        last_confirmed_valid_on=last_confirmed,
        temporal_basis=_maybe_enum(TemporalBasis, temporal_basis) or TemporalBasis.IN_FORCE,
    )

    values: list[ParameterValue] = []
    for (value_raw, valid_from, valid_to, legal_status, source_type,
         oj_date, references, lineage) in conn.execute(
        """
        SELECT value_raw, valid_from, valid_to, legal_status, source_type,
               official_journal_date, received_references, lineage
        FROM params.model_values
        WHERE parameter_id = %s
        ORDER BY seq
        """,
        (parameter_id,),
    ).fetchall():
        envelope = dict(
            valid_from=valid_from,
            valid_to=valid_to,
            legal_status=_maybe_enum(LegalStatus, legal_status),
            source_type=_maybe_enum(SourceType, source_type),
            official_journal_date=oj_date,
            references=[r for r in map(_clean_reference, references or []) if r],
            lineage=_clean_lineage(lineage or {}),
        )
        try:
            values.append(ParameterValue(value=value_raw, **envelope))
        except Exception:
            # e.g. bracket lists with extra keys: keep the row, stringify the value
            values.append(
                ParameterValue(value=json.dumps(value_raw, ensure_ascii=False), **envelope)
            )

    return ParameterRecord(information=information, values=values)


# ---------------------------------------------------------------------------
# Stage C: one extraction_runs row (+ proposal + references) per pipeline run
# ---------------------------------------------------------------------------


def record_run(
    conn: psycopg.Connection,
    cfg: WorkflowConfig,
    item: ReviewItem,
    prompt_version: str,
    agent_version: str,
    started_at: datetime,
    finished_at: datetime,
) -> int:
    """Persist a completed run; returns extraction_runs.id."""
    with conn.transaction():
        parameter_id_row = conn.execute(
            "SELECT id FROM params.parameters WHERE model_target = %s", (item.model_target,)
        ).fetchone()
        parameter_id = parameter_id_row[0] if parameter_id_row else None
        run_pk = conn.execute(
            """
            INSERT INTO params.extraction_runs
                (run_id, parameter_id, country, model_target, as_of, model,
                 critique_model, prompt_version, agent_version, phoenix_project,
                 phoenix_trace_id, routing, critique_verdict, item_id,
                 retrieval_trace, started_at, finished_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                item.run_id,
                parameter_id,
                item.country,
                item.model_target,
                item.as_of,
                cfg.model,
                cfg.critique_model,
                prompt_version,
                agent_version,
                cfg.phoenix_project if item.phoenix_trace_id else None,
                item.phoenix_trace_id,
                item.routing.value,
                item.critique.verdict if item.critique else None,
                item.id,
                json.dumps(
                    [h.model_dump(mode="json", exclude={"content"}) for h in item.retrieval_trace],
                    ensure_ascii=False,
                ),
                started_at,
                finished_at,
            ),
        ).fetchone()[0]

        proposed = item.proposed_value
        if proposed is not None:
            value_json = proposed.model_dump(mode="json")["value"]
            lineage = proposed.lineage
            proposal_pk = conn.execute(
                """
                INSERT INTO params.proposals
                    (proposal_id, run_pk, parameter_id, model_target, proposed_value,
                     proposed_value_numeric, effective_from, effective_to, legal_status,
                     source_class, official_journal_date, confidence, reasoning)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    f"{item.run_id}/{item.id}",
                    run_pk,
                    parameter_id,
                    item.model_target,
                    json.dumps(value_json, ensure_ascii=False),
                    float(value_json) if isinstance(value_json, (int, float)) else None,
                    proposed.valid_from,
                    proposed.valid_to,
                    proposed.legal_status.value if proposed.legal_status else None,
                    _SOURCE_CLASS.get(proposed.source_type, "other"),
                    proposed.official_journal_date,
                    lineage.confidence if lineage else None,
                    lineage.model_answer if lineage else None,
                ),
            ).fetchone()[0]
            with conn.cursor() as cur:
                cur.executemany(
                    """
                    INSERT INTO params.proposal_references
                        (proposal_pk, title, href, legal_unit_ref, jrc_chunk_id,
                         supporting_extract, extract_start, extract_end)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [
                        (
                            proposal_pk,
                            ref.title,
                            ref.href,
                            ref.legal_unit_ref,
                            ref.jrc_database_id,
                            ref.supporting_extract,
                            ref.extract_offsets[0] if ref.extract_offsets else None,
                            ref.extract_offsets[1] if ref.extract_offsets else None,
                        )
                        for ref in proposed.references
                    ],
                )
    return run_pk


def record_run_safe(
    cfg: WorkflowConfig,
    item: ReviewItem,
    prompt_version: str,
    agent_version: str,
    started_at: datetime,
    finished_at: datetime,
) -> None:
    """record_run, best-effort: the file queue is the primary store, so a
    missing params schema or an unreachable DB must not fail the run."""
    try:
        with connect(cfg) as conn:
            record_run(conn, cfg, item, prompt_version, agent_version, started_at, finished_at)
    except Exception as exc:
        print(
            f"[paramdb] run {item.run_id} not recorded "
            f"({exc.__class__.__name__}: {exc}) — run `nomoscope-workflow init-param-db`?"
        )
