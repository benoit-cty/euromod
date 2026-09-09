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
from datetime import date, datetime, timedelta
from pathlib import Path

import psycopg
import yaml

from .config import WorkflowConfig
from .schema import (
    Bracket,
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
            pass
        percent = percent_literal(value)
        if percent is not None:
            return percent, "numeric"
        return None, "expression"
    return None, "expression"


_PERCENT_LITERAL = re.compile(r"^\s*([-+]?\d+(?:[.,]\d+)?)\s*%\s*$")


def percent_literal(value: str | None) -> float | None:
    """`8.17%` -> 0.0817: EUROMOD's own spelling for a rate, read as a fraction.

    The NL and LT exports state every rate as a percent literal and the IE export
    a few (`4.1%`); `normalized.value` is null for all of them, so without this
    the store held no scalar, `_current_value` had nothing to route against and
    a correct 0.495 proposal came back `changed`. The fraction is the "/1" form
    the rest of the store uses (and that the curation overlays give these
    parameters), the same reading `nomokrisis_eval.scoring.normalise_value`
    applies on the golden side.
    """
    if not isinstance(value, str):
        return None
    match = _PERCENT_LITERAL.match(value)
    if not match:
        return None
    # Round away the binary noise of the division (8.17 / 100 is not 0.0817 in
    # floating point); 12 significant digits is far below any EUROMOD precision.
    return float(f"{float(match.group(1).replace(',', '.')) / 100.0:.12g}")


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


def system_year_bounds(conn: psycopg.Connection, country: str) -> tuple[int, int] | None:
    """First and last EUROMOD system year the export defines for a country.

    EUROMOD ships one system per year (FR J2.19: 2006-2025) and the workflow
    verifies exactly one of them. A run anchored outside that range verifies a
    system that does not exist — it silently compares against the newest value
    it can find, so every parameter comes back `changed` on no evidence.
    Returns None when nothing is ingested for the country (no basis to judge).
    """
    row = conn.execute(
        "SELECT min(v.system_year), max(v.system_year) "
        "FROM params.model_values v JOIN params.parameters p ON p.id = v.parameter_id "
        "WHERE p.country = %s AND v.system_year IS NOT NULL",
        (country,),
    ).fetchone()
    if row is None or row[0] is None:
        return None
    return int(row[0]), int(row[1])


_TEMPORAL_BASIS_SQL = (
    "UPDATE params.parameters SET temporal_basis = %s "
    "WHERE model_target = %s AND temporal_basis IS DISTINCT FROM %s "
    "RETURNING model_target"
)

# source_type sits on the value rows, but curation states it for the parameter:
# what makes a value national-team-sourced (a municipal fee schedule, an
# assumption) is a property of the quantity, not of one version of it — so every
# value of the target gets the flag, and _current_value() finds it whatever the
# run's as_of.
_SOURCE_TYPE_SQL = (
    "UPDATE params.model_values v SET source_type = %s "
    "FROM params.parameters p "
    "WHERE v.parameter_id = p.id AND p.model_target = %s "
    "AND v.source_type IS DISTINCT FROM %s "
    "RETURNING p.model_target"
)


# The export's `unit` is what the proposal prompt normalises against ("11 % ->
# 0.11 for unit /1") and what the critique's `values_sane` range-checks, so a
# rate delivered as `currency` is a wrong hint on every LLM call: the proposer
# is told to keep a currency amount, the critique either refuses the fraction
# (unit implausible) or never checks its range. The FR export labels 146 rates
# that way while using "/1" for 215 others — an enrichment slip, reported to
# the economists team — and until a corrected export lands the fix is curated
# here. `unit_structured` follows, in the export's own shape for "/1".
_UNIT_SQL = (
    "UPDATE params.parameters SET unit = %s, unit_structured = %s "
    "WHERE model_target = %s AND unit IS DISTINCT FROM %s "
    "RETURNING model_target"
)

#: The unit vocabulary the export uses; a curated unit outside it is a typo.
#: Two units the export never ships are accepted on purpose: `currency/hour`
#: (the FR SMIC is legislated per hour and the export labels `$Minwage_hourly`
#: per month) and `ratio` (a dimensionless multiplier such as NL's
#: `$bfa_mult2` = 1.2143, which is not a fraction and fails the "/1" range
#: check the critique applies).
KNOWN_UNITS = frozenset(
    {
        "/1",
        "currency",
        "currency/hour",
        "currency/day",
        "currency/week",
        "currency/month",
        "currency/year",
        "ratio",
    }
)


def _curated_unit_structured(unit: str) -> dict | None:
    """The structured view of a curated unit, matching what the export ships."""
    if unit == "/1":
        return {"quantity": "rate", "scale": "/1"}
    if unit == "ratio":
        return {"quantity": "ratio"}
    return structured_unit(unit, None)


def _apply_curation_rule(
    conn: psycopg.Connection,
    stats: dict,
    sql: str,
    target: str,
    value: str,
    extra: tuple = (),
) -> None:
    """Run one curation UPDATE, classifying the target as updated/unchanged/missing.

    `sql` binds (value, *extra, target, value): the value to set, any further
    SET columns, then the WHERE clause's target and "IS DISTINCT FROM" guard.
    """
    if conn.execute(sql, (value, *extra, target, value)).fetchone() is not None:
        stats["updated"] += 1
        return
    exists = conn.execute(
        "SELECT 1 FROM params.parameters WHERE model_target = %s", (target,)
    ).fetchone()
    if exists is None:
        stats["missing"].append(target)
    else:
        stats["unchanged"] += 1


def apply_curation(conn: psycopg.Connection, path: Path) -> dict:
    """Apply a curation overlay (curation/<CC>.curation.yaml) onto ingested rows.

    The EUROMOD export carries no `temporal_basis`, its `source_type` is
    empty even where we know a value is not legislation-derivable, and its
    `unit` is wrong on every FR rate: that is knowledge we hold, not theirs,
    and the enriched JSON is read-only. Before
    this, the flag was a hand-run UPDATE recorded nowhere — lost on
    `docker compose down -v` and invisible to review. The overlay is the
    versioned source of truth; applying it is idempotent, so it is safe to
    re-run after every `ingest-params` — and it MUST be re-run, since ingesting
    a country file replaces its model_values rows.

    Unknown model_targets are reported rather than silently ignored: a typo or a
    parameter renamed in a new export would otherwise leave the flag unset and
    the affected runs quietly wrong.
    """
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    country = doc.get("country")
    stats = {"updated": 0, "unchanged": 0, "missing": []}
    with conn.transaction():
        for rule in doc.get("temporal_basis") or []:
            basis = TemporalBasis(rule["basis"]).value  # loud on a typo'd overlay
            for target in rule.get("targets") or []:
                _apply_curation_rule(conn, stats, _TEMPORAL_BASIS_SQL, target, basis)
        for rule in doc.get("source_type") or []:
            source_type = SourceType(rule["type"]).value
            for target in rule.get("targets") or []:
                _apply_curation_rule(conn, stats, _SOURCE_TYPE_SQL, target, source_type)
        for rule in doc.get("unit") or []:
            unit = str(rule["unit"])
            if unit not in KNOWN_UNITS:  # loud on a typo'd overlay
                raise ValueError(f"unknown unit {unit!r} in {path.name}; known: {sorted(KNOWN_UNITS)}")
            structured = _jsonb(_curated_unit_structured(unit))
            for target in rule.get("targets") or []:
                _apply_curation_rule(conn, stats, _UNIT_SQL, target, unit, (structured,))
    if country:
        stats["country"] = country
    return stats


def _upsert_parameter(conn: psycopg.Connection, info: dict, source_file: str) -> int:
    # An earlier FR export shipped a handful of targets with a trailing newline;
    # the upsert keys on model_target, so the untrimmed row and the clean one
    # collided on the parameter_key unique index instead of updating in place.
    info = {**info, "model_target": str(info["model_target"]).strip()}
    if info.get("parameter_id"):
        info["parameter_id"] = str(info["parameter_id"]).strip()
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
            if numeric is None:
                # The upstream normaliser leaves percent literals (`8.17%`)
                # unread; they are scalars in EUROMOD's own spelling.
                numeric = percent_literal(raw_euromod) if raw_euromod else None
                if numeric is None:
                    numeric = percent_literal(value["value"])
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


def record_value(value_raw, value_numeric: float | None, value_kind: str | None):
    """The value a materialized record carries for one model_values row.

    `value_raw` is the export's own normalized value, which is null for the
    percent literals the NL/LT/IE exports state rates as (`8.17%`, `4.1%`);
    `normalise_value` reads those into `value_numeric` at ingest, but the
    record was built from `value_raw` alone, so every such parameter reached
    the workflow with a null current value: `_current_value` had nothing to
    route against and a correct 0.495 proposal came back `changed` (NL
    `$tin_br3`, IE `$tscee_prsiA_rate1`, 2026-09-09 eval — on both models).
    Prefer the scalar the ingester established whenever the export gave none;
    formulas and brackets keep their raw form.
    """
    if value_raw is None and value_kind == "numeric" and value_numeric is not None:
        return value_numeric
    return value_raw


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
    for (value_raw, value_numeric, value_kind, valid_from, valid_to, legal_status,
         source_type, oj_date, references, lineage) in conn.execute(
        """
        SELECT value_raw, value_numeric, value_kind, valid_from, valid_to, legal_status,
               source_type, official_journal_date, received_references, lineage
        FROM params.model_values
        WHERE parameter_id = %s
        ORDER BY seq
        """,
        (parameter_id,),
    ).fetchall():
        value_raw = record_value(value_raw, value_numeric, value_kind)
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


def load_group_record(conn: psycopg.Connection, group_id: str) -> ParameterRecord:
    """Rebuild a bracket schedule as ONE Activity 1 record from params.parameter_groups.

    EUROMOD stores a schedule as separate scalar constants (the FR income-tax
    barème is 4 thresholds + 5 rates); the export's `groups` block says which
    constants form which band, and that block is the only place the schedule
    exists as an object. Assembling it here means a schedule-shaped parameter
    needs no hand-authored file: the DB stays the single source.

    Threshold semantics: the export's role is `upper_threshold`, while a
    Bracket's `threshold` is the band's LOWER bound — so band n's threshold is
    band n-1's upper limit, verbatim, and the first band starts at 0. Verbatim
    and not +1: in practice the exported values ARE the law's lower bounds (they
    match exactly through system year 2024). FR 2025 sits one euro below the law
    (11 496 where CGI art. 197 says 11 497); the EUROMOD economists team has
    confirmed that as an error on their side, to be corrected in a future
    release — so it must show up as a diff, not be silently normalised away.

    One value row per distinct member change date, each holding the schedule in
    force over that interval — the same shape as a scalar parameter's history.

    The record's id is derived, `euromod://<cc>/<policy>/group/<name>`: a
    schedule has no `model_target` of its own in the export, and inventing a
    def_const that EUROMOD does not define is exactly the kind of untraceable
    artefact this function exists to remove. db/seed.sql keys the barème's
    citation-registry rows on the derived id.
    """
    row = conn.execute(
        """
        SELECT group_id, country, kind, policy, components, instances
        FROM params.parameter_groups WHERE group_id = %s
        """,
        (group_id,),
    ).fetchone()
    if row is None:
        raise KeyError(f"parameter group not in params DB (see ingest-params): {group_id}")
    group_id, country, kind, policy, components, instances = row
    if kind != "bracket_schedule":
        raise ValueError(f"{group_id}: only bracket_schedule groups assemble into a record, not {kind!r}")

    # band_index -> {role: (parameter_id, model_target, [(valid_from, valid_to, value)])}
    bands: dict[int, dict[str, tuple[str, list]]] = {}
    for component in components:
        member = conn.execute(
            "SELECT id, model_target FROM params.parameters WHERE parameter_key = %s OR model_target = %s",
            (component.get("parameter_id"), component.get("parameter_id")),
        ).fetchone()
        if member is None:
            continue  # a component the export names but never defines: skip the band role
        history = conn.execute(
            """
            SELECT valid_from, valid_to, value_numeric FROM params.model_values
            WHERE parameter_id = %s ORDER BY valid_from
            """,
            (member[0],),
        ).fetchall()
        bands.setdefault(int(component.get("band_index", 0)), {})[component.get("role")] = (
            member[1], history
        )

    def value_on(history: list, on: date) -> float | None:
        for valid_from, valid_to, value in history:
            if valid_from <= on and (valid_to is None or valid_to >= on):
                return value
        return None

    starts = sorted({
        valid_from
        for roles in bands.values()
        for _, history in roles.values()
        for valid_from, _, _ in history
    })
    ordered = sorted(bands)
    values: list[ParameterValue] = []
    for i, start in enumerate(starts):
        end = starts[i + 1] - timedelta(days=1) if i + 1 < len(starts) else None
        schedule: list[Bracket] = []
        previous_upper: float | None = None
        for band_index in ordered:
            roles = bands[band_index]
            rate = value_on(roles["rate"][1], start) if "rate" in roles else None
            upper = value_on(roles["upper_threshold"][1], start) if "upper_threshold" in roles else None
            if rate is None and upper is None:
                continue  # band not in force in this interval (abolished or not yet created)
            schedule.append(Bracket(threshold=previous_upper or 0.0, rate=rate))
            previous_upper = upper
        if not schedule:
            continue
        if values and values[-1].value == schedule:
            values[-1].valid_to = end  # nothing in the schedule actually moved
            continue
        values.append(ParameterValue(value=schedule, valid_from=start, valid_to=end))

    members = ", ".join(
        f"band {band_index} {role}={bands[band_index][role][0]}"
        for band_index in ordered for role in sorted(bands[band_index])
    )
    label, description = _group_texts(conn, bands, ordered, group_id)
    information = ParameterInformation(
        country=country,
        model_target=f"euromod://{country}/{policy}/group/{group_id.rsplit(':', 1)[-1]}",
        value_type="bracket_schedule",
        unit="/1",
        label=label,
        short_label={"en": group_id},
        description=description,
        explanation={
            "en": f"Assembled from params.parameter_groups {group_id} ({members}). "
            "EUROMOD's role is upper_threshold; brackets carry the band's lower bound."
        },
        temporal_basis=_group_temporal_basis(conn, bands),
    )
    return ParameterRecord(information=information, values=values)


def _group_texts(
    conn: psycopg.Connection, bands: dict, ordered: list[int], group_id: str
) -> tuple[dict[str, str] | None, dict[str, str] | None]:
    """A label and description for the assembled schedule, from its members.

    A group has no text of its own in the export, and the frame step builds
    the retrieval query from label + description: with both empty the ES
    savings scale ran with the query `ES Tax schedule` and the LT PIT schedule
    with `LT`, and neither could be answered. The members' labels are what
    the enrichment wrote for the bands ("Capital income taxation: national
    rate 1"), so the schedule's label is the first band's label with its
    ordinal stripped, and the description lists every band's label and
    description once — the same words a human would search for.
    """
    labels: list[str] = []
    descriptions: list[str] = []
    for band_index in ordered:
        for role in ("rate", "upper_threshold"):
            if role not in bands[band_index]:
                continue
            row = conn.execute(
                "SELECT label, description FROM params.parameters WHERE model_target = %s",
                (bands[band_index][role][0],),
            ).fetchone()
            if row is None:
                continue
            for source, sink in ((row[0], labels), (row[1], descriptions)):
                text = (source or {}).get("en") if isinstance(source, dict) else None
                if text and text not in sink:
                    sink.append(text)
    if not labels:
        return None, None
    # "Capital income taxation: national rate 1" -> "Capital income taxation: national rate"
    head = re.sub(r"\s*\d+\s*$", "", labels[0]).strip(" :-") or labels[0]
    label = {"en": f"{head} schedule ({group_id.rsplit(':', 1)[-1]})"}
    description = {"en": " ".join([*labels, *descriptions])} if labels or descriptions else None
    return label, description


def _group_temporal_basis(conn: psycopg.Connection, bands: dict) -> TemporalBasis:
    """A schedule inherits its members' basis; mixed members fall back to in_force."""
    targets = [target for roles in bands.values() for target, _ in roles.values()]
    if not targets:
        return TemporalBasis.IN_FORCE
    rows = conn.execute(
        "SELECT DISTINCT temporal_basis FROM params.parameters WHERE model_target = ANY(%s)",
        (targets,),
    ).fetchall()
    if len(rows) == 1:
        return _maybe_enum(TemporalBasis, rows[0][0]) or TemporalBasis.IN_FORCE
    return TemporalBasis.IN_FORCE


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


# ---------------------------------------------------------------------------
# Stage D: reviewer decisions. params.review_decisions is the system of record —
# the UI's Accept/Reject/Edit fails if this insert does. data/decisions.jsonl is
# a redundant local copy, replayed by `nomoscope-workflow sync-decisions`.
# ---------------------------------------------------------------------------


def record_decision(conn: psycopg.Connection, entry: dict) -> int | None:
    """Insert one audit entry; returns its id, or None if it was already there.

    Deduplication is on (item_id, decided_at), so replaying the whole log is
    idempotent while a genuine re-decision (a new instant) still appends.
    """
    if not entry.get("action"):
        raise ValueError("decision entry has no action")
    item_id = entry.get("item_id")
    run_id = entry.get("run_id")
    proposal_pk = None
    if run_id and item_id:
        # record_run keys proposals as "<run_id>/<item_id>"
        row = conn.execute(
            "SELECT id FROM params.proposals WHERE proposal_id = %s", (f"{run_id}/{item_id}",)
        ).fetchone()
        proposal_pk = row[0] if row else None

    def as_json(key: str) -> str | None:
        value = entry.get(key)
        return None if value is None else json.dumps(value, ensure_ascii=False)

    row = conn.execute(
        """
        INSERT INTO params.review_decisions
            (proposal_pk, item_id, run_id, model_target, as_of, routing, action,
             reviewer, note, edited_value, edited_fields, confidence,
             critique_verdict, decided_at, logged_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                coalesce(%s::timestamptz, now()))
        ON CONFLICT DO NOTHING
        RETURNING id
        """,
        (
            proposal_pk,
            item_id,
            run_id,
            entry.get("model_target"),
            entry.get("as_of"),
            entry.get("routing"),
            entry["action"],
            entry.get("reviewer"),
            entry.get("note"),
            as_json("edited_value"),
            as_json("edited_fields"),
            entry.get("confidence"),
            entry.get("critique_verdict"),
            # log lines written before decided_at was added dedupe on logged_at,
            # which the UI set to the same instant
            entry.get("decided_at") or entry.get("logged_at"),
            entry.get("logged_at"),
        ),
    ).fetchone()
    return row[0] if row else None


# Old queue ids ended on the run's anchor date; the system-year id keeps its year.
_OLD_ITEM_ID = r"_(\d{4})-\d{2}-\d{2}$"


def remap_item_ids(cfg: WorkflowConfig, apply: bool = False) -> dict[str, int]:
    """Re-point stored item ids at the system-year queue ids (see
    queue_store.migrate_item_ids). Idempotent — rows already migrated don't match.

    extraction_runs.item_id is what the Parameters tab follows to open a review
    item, so a stale id there is a dead link; proposals.proposal_id embeds the
    item id as "<run_id>/<item_id>" and is how a decision finds its proposal.
    """
    statements = {
        "extraction_runs": (
            "UPDATE params.extraction_runs "
            "SET item_id = regexp_replace(item_id, %s, '_\\1') WHERE item_id ~ %s"
        ),
        "review_decisions": (
            "UPDATE params.review_decisions "
            "SET item_id = regexp_replace(item_id, %s, '_\\1') WHERE item_id ~ %s"
        ),
        # "<run_id>/<item_id>", and run ids never contain a slash
        "proposals": (
            "UPDATE params.proposals "
            "SET proposal_id = left(proposal_id, position('/' in proposal_id)) "
            "  || regexp_replace(substr(proposal_id, position('/' in proposal_id) + 1), "
            "                    %s, '_\\1') "
            "WHERE position('/' in proposal_id) > 0 "
            "  AND substr(proposal_id, position('/' in proposal_id) + 1) ~ %s"
        ),
    }
    counts: dict[str, int] = {}
    with connect(cfg) as conn:
        for table, sql in statements.items():
            # one transaction per table: a unique-index clash in the audit table
            # must not take the (independent) extraction_runs remap down with it
            with conn.transaction():
                counts[table] = conn.execute(sql, (_OLD_ITEM_ID, _OLD_ITEM_ID)).rowcount
                if not apply:
                    raise psycopg.Rollback
    return counts


def sync_decisions(cfg: WorkflowConfig, entries: list[dict]) -> tuple[int, int]:
    """Replay audit entries into params.review_decisions.

    Returns (inserted, skipped); skipped are entries already in the table, so
    replaying the whole log after every outage is safe.
    """
    inserted = 0
    with connect(cfg) as conn, conn.transaction():
        for entry in entries:
            if record_decision(conn, entry) is not None:
                inserted += 1
    return inserted, len(entries) - inserted
