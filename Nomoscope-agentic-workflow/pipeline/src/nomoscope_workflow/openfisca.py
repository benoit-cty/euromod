"""Ingest an OpenFisca-format parameter corpus into params.external_*.

The values:/brackets:/metadata: YAML layout is defined by openfisca-core, so
one walker covers every OpenFisca country package (and PolicyEngine forks).
The corpus is stored under its own dotted-path identity; no EUROMOD mapping is
required or attempted here — params.parameter_links stays a separate,
human-validated step. See Param_Schema/openfisca_france_usage.md.

Bracket scales are flattened to one time series per band component
('brackets[2].rate', 'brackets[2].threshold', ...): exactly the grain EUROMOD
scalar constants are fingerprint-matched against.
"""

from __future__ import annotations

import json
import re
import subprocess
from datetime import date, datetime
from pathlib import Path

import psycopg
import yaml

# National ids embedded in Legifrance (and similar) hrefs.
_NATIONAL_ID = re.compile(r"((?:LEGIARTI|LEGITEXT|JORFTEXT|JORFARTI|LEGISCTA)\d+)")

_BRACKET_COMPONENTS = ("threshold", "rate", "amount", "average_rate", "base")


def _as_date(key) -> date | None:
    """YAML keys parse as date objects when unquoted, strings otherwise."""
    if isinstance(key, date):
        return key
    try:
        return datetime.strptime(str(key), "%Y-%m-%d").date()
    except ValueError:
        return None


def _numeric(value) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _json_safe(value):
    """YAML parses unquoted dates as date objects, including as dict KEYS,
    which json.dumps(default=...) does not handle — stringify keys recursively."""
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if isinstance(value, date):
        return value.isoformat()
    return value


def _git(repo: Path, *args: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=10
        )
        return out.stdout.strip() or None
    except Exception:
        return None


def ingest_corpus(
    conn: psycopg.Connection,
    parameters_dir: Path,
    country: str,
    kind: str = "openfisca",
    license: str | None = None,
    echo=print,
) -> dict:
    """Walk a parameters/ tree and (re)load it as one external corpus."""
    repo_url = _git(parameters_dir, "remote", "get-url", "origin")
    commit = _git(parameters_dir, "rev-parse", "HEAD")
    stats = {"parameters": 0, "values": 0, "references": 0, "skipped_files": 0, "errors": 0}
    files = sorted(parameters_dir.rglob("*.yaml"))
    with conn.transaction():
        corpus_id = conn.execute(
            """
            INSERT INTO params.external_corpora (kind, country, repo_url, commit_sha, license, ingested_at)
            VALUES (%s, %s, %s, %s, %s, now())
            ON CONFLICT (kind, country) DO UPDATE SET
                repo_url = EXCLUDED.repo_url, commit_sha = EXCLUDED.commit_sha,
                license = EXCLUDED.license, ingested_at = now()
            RETURNING id
            """,
            (kind, country, repo_url, commit, license),
        ).fetchone()[0]
        # Re-ingest replaces the corpus wholesale (children cascade).
        conn.execute(
            "DELETE FROM params.external_parameters WHERE corpus_id = %s", (corpus_id,)
        )
        for i, path in enumerate(files, 1):
            try:
                doc = yaml.safe_load(path.read_text(encoding="utf-8"))
            except Exception:
                stats["errors"] += 1
                continue
            if not isinstance(doc, dict) or not ("values" in doc or "brackets" in doc):
                stats["skipped_files"] += 1  # node-level description files
                continue
            _ingest_parameter(
                conn, corpus_id, path.relative_to(parameters_dir), doc, stats
            )
            if i % 500 == 0:
                echo(f"{country}/{kind}: {i}/{len(files)} files processed")
    return stats


def _ingest_parameter(
    conn: psycopg.Connection, corpus_id: int, rel_path: Path, doc: dict, stats: dict
) -> None:
    dotted = str(rel_path.with_suffix("")).replace("/", ".")
    metadata = dict(doc.get("metadata") or {})
    reference = metadata.pop("reference", None)
    oj_dates = _date_keyed(metadata.get("official_journal_date") or {})
    value_kind = "bracket_schedule" if "brackets" in doc else "scalar"
    external_parameter_id = conn.execute(
        """
        INSERT INTO params.external_parameters
            (corpus_id, path, value_kind, description, short_label, unit, metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            corpus_id,
            dotted,
            value_kind,
            doc.get("description"),
            metadata.get("short_label"),
            metadata.get("unit") or metadata.get("rate_unit"),
            json.dumps(_json_safe(metadata), ensure_ascii=False, default=str),
        ),
    ).fetchone()[0]
    stats["parameters"] += 1

    value_rows: list[tuple] = []
    if value_kind == "scalar":
        _series_rows(external_parameter_id, "value", doc.get("values") or {}, value_rows)
    else:
        for index, bracket in enumerate(doc.get("brackets") or [], start=1):
            if not isinstance(bracket, dict):
                continue
            for component in _BRACKET_COMPONENTS:
                if component in bracket:
                    _series_rows(
                        external_parameter_id,
                        f"brackets[{index}].{component}",
                        bracket[component] or {},
                        value_rows,
                    )
    if value_rows:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO params.external_values
                    (external_parameter_id, component, valid_from, value_numeric, value_raw)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (external_parameter_id, component, valid_from) DO NOTHING
                """,
                value_rows,
            )
    stats["values"] += len(value_rows)
    stats["references"] += _ingest_references(
        conn, external_parameter_id, reference, oj_dates
    )


def _series_rows(
    external_parameter_id: int, component: str, series: dict, out: list[tuple]
) -> None:
    if not isinstance(series, dict):
        return
    for key, entry in series.items():
        valid_from = _as_date(key)
        if valid_from is None:
            continue
        value = entry.get("value") if isinstance(entry, dict) else entry
        out.append(
            (
                external_parameter_id,
                component,
                valid_from,
                _numeric(value),
                json.dumps(_json_safe(value), ensure_ascii=False, default=str),
            )
        )


def _date_keyed(mapping) -> dict[date, str]:
    out: dict[date, str] = {}
    if isinstance(mapping, dict):
        for key, value in mapping.items():
            keyed = _as_date(key)
            if keyed is not None:
                out[keyed] = str(value)
    return out


def _ingest_references(
    conn: psycopg.Connection,
    external_parameter_id: int,
    reference,
    oj_dates: dict[date, str],
) -> int:
    """metadata.reference is a single entry, a list, or a date-keyed mapping."""
    rows: list[tuple] = []

    def add(valid_from: date | None, entry) -> None:
        if isinstance(entry, list):
            for sub in entry:
                add(valid_from, sub)
            return
        if isinstance(entry, str):
            entry = {"title": entry}
        if not isinstance(entry, dict):
            return
        href = entry.get("href")
        match = _NATIONAL_ID.search(href or "")
        rows.append(
            (
                external_parameter_id,
                valid_from,
                entry.get("title"),
                href,
                match.group(1) if match else None,
                oj_dates.get(valid_from) if valid_from else None,
            )
        )

    if isinstance(reference, dict) and any(_as_date(k) for k in reference):
        for key, entry in reference.items():
            add(_as_date(key), entry)
    elif reference is not None:
        add(None, reference)
    if rows:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO params.external_references
                    (external_parameter_id, valid_from, title, href, national_id, official_journal_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                rows,
            )
    return len(rows)
