"""One-off import of the on-disk golden set into the eval schema (ADR 0004).

Reads what used to be the git-versioned golden set —

    dataset/<cc>/*.json            golden cases        -> eval.golden_cases
    dataset_embedding/<cc>/*.json  retrieval cases     -> eval.embedding_cases
    golden_sources/<cc>.json       curated selection   -> eval.golden_selections (kind curated)
    golden_sources/openfisca_<cc>.json                 -> eval.golden_selections (kind openfisca)

— and upserts it, so running it twice changes nothing. This module is the only
place that still understands the file layout, and the only place allowed to
read a case carrying the legacy `parameter_file` key.

Mapping `parameter_file` -> `parameter_target`, in order:

1. The materialized file exists under the repo root: its
   `information.model_target` is the target. A group record's id is derived,
   `euromod://<cc>/<policy>/group/<name>` (paramdb.load_group_record), and is
   mapped back to `group:<group_id>` through params.parameter_groups, whose
   `group_id` is `<cc>:<policy>:<name>`.
2. The file is missing: the case id (`<cc>_<slug>_<as_of>`) is matched against
   the slug every selection entry of that country would produce
   (`openfisca_golden.stale_case_id`), and the entry's `model_target` /
   `group_id` gives the target.
3. Neither: the case is reported as unresolved and skipped.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

import psycopg

from .config import EVAL_ROOT, REPO_ROOT
from .golden_store import (
    restore_verdict,
    save_case,
    save_embedding_case,
    save_selection,
)
from .openfisca_golden import GROUP_PREFIX, stale_case_id
from .schema import EmbeddingCase, GoldenCase

DEFAULT_DATASET_DIR = EVAL_ROOT / "dataset"
DEFAULT_EMBEDDING_DATASET_DIR = EVAL_ROOT / "dataset_embedding"
DEFAULT_SOURCES_DIR = EVAL_ROOT / "golden_sources"

_GROUP_TARGET = re.compile(r"^euromod://([^/]+)/([^/]+)/group/([^/]+)$")
_LEGACY_CONTEXT = {"legacy_parameter_file": True}


@dataclass
class ImportReport:
    selections: int = 0
    cases: int = 0
    cases_verified: int = 0
    embedding_cases: int = 0
    unresolved: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    resolved_by: dict[str, int] = field(default_factory=dict)

    def note_resolution(self, how: str) -> None:
        self.resolved_by[how] = self.resolved_by.get(how, 0) + 1


# --------------------------------------------------------------------------- #
# Readers (the last file-based loaders)
# --------------------------------------------------------------------------- #


def read_selection_files(sources_dir: Path) -> list[tuple[str, str, dict, list[dict]]]:
    """(country, kind, header, entries) per golden_sources/*.json."""
    out: list[tuple[str, str, dict, list[dict]]] = []
    for path in sorted(sources_dir.glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        kind = "openfisca" if path.stem.startswith("openfisca_") else "curated"
        country = (doc.get("country") or path.stem.removeprefix("openfisca_")).upper()
        header = {k: v for k, v in doc.items() if k != "entries"}
        out.append((country, kind, header, list(doc.get("entries", []))))
    return out


def read_case_files(dataset_dir: Path) -> list[tuple[Path, dict]]:
    return [
        (path, json.loads(path.read_text(encoding="utf-8")))
        for path in sorted(dataset_dir.rglob("*.json"))
    ]


def read_embedding_case_files(dataset_dir: Path) -> list[EmbeddingCase]:
    return [
        EmbeddingCase.model_validate_json(path.read_text(encoding="utf-8"))
        for path in sorted(dataset_dir.rglob("*.json"))
    ]


# --------------------------------------------------------------------------- #
# parameter_file -> parameter_target
# --------------------------------------------------------------------------- #


def group_target_from_model_target(conn: psycopg.Connection, model_target: str) -> tuple[str | None, str | None]:
    """`euromod://<cc>/<policy>/group/<name>` -> (`group:<group_id>`, warning).

    Inverts paramdb.load_group_record's id derivation: group_id is
    `<cc>:<policy>:<name>`, looked up in params.parameter_groups by country,
    policy and that id. A miss still yields the derived id (the derivation is
    deterministic) with a warning, so an import into a database whose
    parameter store is not loaded yet does not drop the case.
    """
    match = _GROUP_TARGET.match(model_target)
    if match is None:
        return None, None
    country, policy, name = match.groups()
    derived = f"{country}:{policy}:{name}"
    row = conn.execute(
        """
        SELECT group_id FROM params.parameter_groups
        WHERE country = %s AND policy = %s AND group_id = %s
        """,
        (country, policy, derived),
    ).fetchone()
    if row is None:
        return f"{GROUP_PREFIX}{derived}", f"group {derived} not in params.parameter_groups (ingest-params first)"
    return f"{GROUP_PREFIX}{row[0]}", None


def target_from_parameter_file(
    conn: psycopg.Connection, parameter_file: str
) -> tuple[str | None, str | None]:
    """(target, warning) from the materialized parameter file, or (None, reason)."""
    path = REPO_ROOT / parameter_file
    if not path.exists():
        return None, f"materialized file missing: {parameter_file}"
    try:
        model_target = json.loads(path.read_text(encoding="utf-8"))["information"]["model_target"]
    except (ValueError, KeyError, TypeError) as exc:
        return None, f"cannot read information.model_target from {parameter_file}: {exc}"
    group_target, warning = group_target_from_model_target(conn, model_target)
    if group_target is not None:
        return group_target, warning
    exists = conn.execute(
        "SELECT 1 FROM params.parameters WHERE model_target = %s", (model_target,)
    ).fetchone()
    if exists is None:
        warning = f"{model_target} not in params.parameters (ingest-params first)"
    return model_target, warning


def target_from_selection(
    case_id: str, as_of: date, country: str, selections: list[tuple[str, str, dict, list[dict]]]
) -> str | None:
    """Match the case id against the id each selection entry of the country
    would produce; the entry names the target."""
    for sel_country, _kind, _header, entries in selections:
        if sel_country != country.upper():
            continue
        for entry in entries:
            if stale_case_id(entry, as_of, country) == case_id:
                if entry.get("group_id"):
                    return f"{GROUP_PREFIX}{entry['group_id']}"
                return entry.get("model_target")
    return None


def resolve_case(
    conn: psycopg.Connection,
    payload: dict,
    selections: list[tuple[str, str, dict, list[dict]]],
    report: ImportReport,
) -> GoldenCase | None:
    """A GoldenCase with `parameter_target`, or None (reported) when unresolvable."""
    data = dict(payload)
    case_id = data.get("id", "?")
    if "parameter_target" not in data:
        parameter_file = data.pop("parameter_file", None)
        target, warning = (None, "no parameter_file and no parameter_target")
        if parameter_file:
            target, warning = target_from_parameter_file(conn, parameter_file)
            if target is not None:
                report.note_resolution("materialized file")
        if target is None:
            fallback = target_from_selection(
                case_id, date.fromisoformat(data["as_of"]), data["country"], selections
            )
            if fallback is not None:
                target, warning = fallback, None
                report.note_resolution("selection entry")
        if target is None:
            report.unresolved.append(f"{case_id}: {warning}")
            return None
        if warning:
            report.warnings.append(f"{case_id}: {warning}")
        data["parameter_target"] = target
    else:
        report.note_resolution("already a target")
    return GoldenCase.model_validate(data, context=_LEGACY_CONTEXT)


# --------------------------------------------------------------------------- #
# The import
# --------------------------------------------------------------------------- #


def import_golden(
    conn: psycopg.Connection,
    dataset_dir: Path = DEFAULT_DATASET_DIR,
    embedding_dataset_dir: Path = DEFAULT_EMBEDDING_DATASET_DIR,
    sources_dir: Path = DEFAULT_SOURCES_DIR,
    dry_run: bool = False,
) -> ImportReport:
    report = ImportReport()

    selections = read_selection_files(sources_dir) if sources_dir.exists() else []
    for country, kind, header, entries in selections:
        if not dry_run:
            save_selection(conn, country, kind, header, entries)
        report.selections += 1

    if dataset_dir.exists():
        for path, payload in read_case_files(dataset_dir):
            case = resolve_case(conn, payload, selections, report)
            if case is None:
                continue
            if case.reviewed_by and case.reviewed_at is None:
                # The file never recorded when the verdict was given; its
                # mtime is the closest thing to it.
                case.reviewed_at = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            if not dry_run:
                save_case(conn, case)
                restore_verdict(conn, case)
            report.cases += 1
            if case.verified:
                report.cases_verified += 1

    if embedding_dataset_dir.exists():
        for case in read_embedding_case_files(embedding_dataset_dir):
            if not dry_run:
                save_embedding_case(conn, case)
            report.embedding_cases += 1
    return report
