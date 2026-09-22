"""The golden set as rows: eval.golden_selections, eval.golden_cases, eval.embedding_cases.

Replaces the one-JSON-per-case trees (`dataset/`, `dataset_embedding/`) and
the `golden_sources/` selection files (ADR 0004). Three rules the file layout
enforced by convention are enforced here by construction:

- **The verdict is not part of the case.** `verified`, `reviewed_by`,
  `reviewed_at` and `review_note` are columns, so the reviewer role can be
  granted UPDATE on exactly those; the `case` jsonb never contains them.
  `save_case` therefore cannot touch a verdict: only `set_verified` (the human
  gate, identity from `current_user`) and `save_drafted_case`'s carry-over rule
  write those columns — plus `restore_verdict`, which exists for the one-off
  importer.
- **A rebuilt case keeps its verdict only while its ground truth is identical**
  (`save_drafted_case`): a changed expectation must never inherit approval of a
  different value.
- **A golden set is identified by content**: `golden_set_hash` fingerprints
  the cases a run scored, verdict stripped, so two runs are comparable exactly
  when they share it (`eval.runs.dataset_version`).
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from .schema import REVIEW_FIELDS, EmbeddingCase, GoldenCase

SELECTION_KINDS = ("openfisca", "curated")


# --------------------------------------------------------------------------- #
# Golden cases
# --------------------------------------------------------------------------- #


def case_payload(case: GoldenCase) -> dict:
    """The JSON stored in `case` — everything but the review verdict."""
    return case.model_dump(mode="json", exclude=set(REVIEW_FIELDS), exclude_none=True)


def _merge(row: dict) -> GoldenCase:
    payload = dict(row["case"])
    payload.update(
        verified=row["verified"],
        reviewed_by=row["reviewed_by"],
        reviewed_at=row["reviewed_at"],
        review_note=row["review_note"],
    )
    return GoldenCase.model_validate(payload)


def load_cases(
    conn: psycopg.Connection,
    countries: list[str] | None = None,
    languages: list[str] | None = None,
    verified_only: bool = False,
) -> list[GoldenCase]:
    """Every golden case matching the filters, ordered by id, verdict merged in."""
    clauses, params = [], []
    if countries:
        clauses.append("country = ANY(%s)")
        params.append([c.upper() for c in countries])
    if languages:
        clauses.append("language = ANY(%s)")
        params.append([l.lower() for l in languages])
    if verified_only:
        clauses.append("verified")
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with conn.cursor(row_factory=dict_row) as cur:
        rows = cur.execute(
            f"""SELECT id, "case", verified, reviewed_by, reviewed_at, review_note
                FROM eval.golden_cases {where} ORDER BY id""",
            params,
        ).fetchall()
    return [_merge(row) for row in rows]


def load_case(conn: psycopg.Connection, case_id: str) -> GoldenCase | None:
    with conn.cursor(row_factory=dict_row) as cur:
        row = cur.execute(
            """SELECT id, "case", verified, reviewed_by, reviewed_at, review_note
               FROM eval.golden_cases WHERE id = %s""",
            (case_id,),
        ).fetchone()
    return _merge(row) if row else None


def save_case(conn: psycopg.Connection, case: GoldenCase) -> None:
    """Upsert the case body. The verdict columns are deliberately NOT written:
    an existing row keeps its verdict, a new row starts unreviewed."""
    conn.execute(
        """
        INSERT INTO eval.golden_cases (id, country, language, as_of, "case")
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            country = EXCLUDED.country,
            language = EXCLUDED.language,
            as_of = EXCLUDED.as_of,
            "case" = EXCLUDED."case",
            updated_at = now()
        """,
        (case.id, case.country.upper(), case.language.lower(), case.as_of, Jsonb(case_payload(case))),
    )
    conn.commit()


def delete_case(conn: psycopg.Connection, case_id: str) -> bool:
    deleted = conn.execute("DELETE FROM eval.golden_cases WHERE id = %s", (case_id,)).rowcount
    conn.commit()
    return bool(deleted)


def set_verified(
    conn: psycopg.Connection, case_id: str, verified: bool, note: str | None = None
) -> GoldenCase | None:
    """The human gate. Reviewer identity is the connection's `current_user`
    (per-analyst logins, ADR 0004) — never a value the caller passes in.
    Returns the updated case, or None for an unknown id."""
    updated = conn.execute(
        """
        UPDATE eval.golden_cases
        SET verified = %s, reviewed_by = current_user, reviewed_at = now(),
            review_note = %s, updated_at = now()
        WHERE id = %s
        """,
        (verified, note, case_id),
    ).rowcount
    conn.commit()
    return load_case(conn, case_id) if updated else None


def restore_verdict(conn: psycopg.Connection, case: GoldenCase) -> None:
    """Write the verdict carried on a case object — for `import-golden` only,
    which replays verdicts recorded in the old case files (their `reviewed_by`
    is whatever the file says, not `current_user`)."""
    conn.execute(
        """
        UPDATE eval.golden_cases
        SET verified = %s, reviewed_by = %s, reviewed_at = %s, review_note = %s
        WHERE id = %s
        """,
        (case.verified, case.reviewed_by, case.reviewed_at, case.review_note, case.id),
    )
    conn.commit()


def _ground_truth(case: GoldenCase) -> str:
    """What a reviewer actually approved. Everything else a drafter writes
    (notes, drafted_by, corpus_available, labels) is provenance that can be
    refreshed freely."""
    return json.dumps(
        {
            "expected": case.expected.model_dump(mode="json"),
            "parameter_target": case.parameter_target,
            "as_of": case.as_of.isoformat(),
        },
        sort_keys=True,
    )


def save_drafted_case(conn: psycopg.Connection, case: GoldenCase) -> bool:
    """Write a freshly drafted case, carrying the human verdict over when the
    ground truth did not change.

    Drafters always emit `verified: false`. Writing that blindly would discard
    every review each time the set is rebuilt — and a golden set nobody dares
    rebuild stops tracking the parameter store. Keeping the verdict blindly is
    worse: a changed expectation would inherit approval of a different value.
    So the verdict survives exactly when the ground truth (`expected`, the
    parameter under test, `as_of`) is identical to what the reviewer approved,
    and is cleared the moment any of it moves.

    Returns True when a previous verdict was reset. On return `case` carries
    the verdict now on the row, so a caller can report it.
    """
    previous = load_case(conn, case.id)
    reset = False
    save_case(conn, case)
    if previous is not None and (previous.verified or previous.reviewed_by):
        if _ground_truth(previous) == _ground_truth(case):
            case.verified = previous.verified
            case.reviewed_by = previous.reviewed_by
            case.reviewed_at = previous.reviewed_at
            case.review_note = previous.review_note
        else:
            reset = True
            conn.execute(
                """
                UPDATE eval.golden_cases
                SET verified = false, reviewed_by = NULL, reviewed_at = NULL,
                    review_note = NULL, updated_at = now()
                WHERE id = %s
                """,
                (case.id,),
            )
            conn.commit()
            case.verified = False
            case.reviewed_by = case.reviewed_at = case.review_note = None
    return reset


# --------------------------------------------------------------------------- #
# Golden selections (what used to be golden_sources/<cc>.json)
# --------------------------------------------------------------------------- #


def load_selection(conn: psycopg.Connection, country: str, kind: str) -> tuple[dict, list[dict]]:
    """(header, entries) of the selection for (country, kind).

    Raises KeyError when there is none — the caller says how to get one
    (`import-golden` for the on-disk files, or the UI once it edits selections).
    """
    row = conn.execute(
        "SELECT header, entries FROM eval.golden_selections WHERE country = %s AND kind = %s",
        (country.upper(), kind),
    ).fetchone()
    if row is None:
        raise KeyError(f"no {kind} golden selection for {country.upper()} in eval.golden_selections")
    header, entries = row
    return dict(header), list(entries)


def save_selection(
    conn: psycopg.Connection, country: str, kind: str, header: dict, entries: list[dict]
) -> None:
    if kind not in SELECTION_KINDS:
        raise ValueError(f"selection kind must be one of {SELECTION_KINDS}, not {kind!r}")
    header = {k: v for k, v in header.items() if k != "entries"}
    conn.execute(
        """
        INSERT INTO eval.golden_selections (country, kind, header, entries)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (country, kind) DO UPDATE SET
            header = EXCLUDED.header,
            entries = EXCLUDED.entries,
            updated_at = now(),
            updated_by = current_user
        """,
        (country.upper(), kind, Jsonb(header), Jsonb(entries)),
    )
    conn.commit()


def list_selections(conn: psycopg.Connection) -> list[dict]:
    with conn.cursor(row_factory=dict_row) as cur:
        return cur.execute(
            """SELECT country, kind, jsonb_array_length(entries) AS entries, updated_at, updated_by
               FROM eval.golden_selections ORDER BY country, kind"""
        ).fetchall()


def selection_kinds(conn: psycopg.Connection, country: str) -> list[str]:
    """The kinds of selection a country has rows for, in SELECTION_KINDS order."""
    rows = conn.execute(
        "SELECT kind FROM eval.golden_selections WHERE country = %s", (country.upper(),)
    ).fetchall()
    present = {row[0] for row in rows}
    return [kind for kind in SELECTION_KINDS if kind in present]


def selection_document(header: dict, entries: list[dict]) -> dict:
    """The row in the shape the golden_sources/<cc>.json file had: the header
    keys in their stored order, then `"entries": [...]` last. This is what
    `selection-export` writes and `selection-import` reads back, so a
    selection can still be edited as a file (ADR 0004 moved the row, not the
    editing workflow)."""
    return {**{k: v for k, v in header.items() if k != "entries"}, "entries": list(entries)}


def selection_identity(doc: dict, filename: str | None = None) -> tuple[str, str]:
    """(country, kind) of a selection document, inferred the way
    `import_golden.read_selection_files` did for golden_sources/ files.

    Country: the header's `country`, else the file stem (`openfisca_fr` → FR).
    Kind: the header's `corpus` when it names a kind (`curated` / `openfisca`),
    else `openfisca` for an `openfisca_*` file, else `curated`.
    Raises ValueError when neither the header nor the filename says the country.
    """
    stem = Path(filename).stem if filename else ""
    country = (doc.get("country") or stem.removeprefix("openfisca_")).upper()
    if not country:
        raise ValueError("selection document has no `country` header and the filename does not say")
    corpus = doc.get("corpus")
    if corpus in SELECTION_KINDS:
        kind = corpus
    else:
        kind = "openfisca" if stem.startswith("openfisca_") else "curated"
    return country, kind


# --------------------------------------------------------------------------- #
# Embedding (retrieval) cases
# --------------------------------------------------------------------------- #


def load_embedding_cases(
    conn: psycopg.Connection,
    countries: list[str] | None = None,
    languages: list[str] | None = None,
    verified_only: bool = False,
) -> list[EmbeddingCase]:
    clauses, params = [], []
    if countries:
        clauses.append("country = ANY(%s)")
        params.append([c.upper() for c in countries])
    if languages:
        clauses.append("language = ANY(%s)")
        params.append([l.lower() for l in languages])
    if verified_only:
        clauses.append("verified")
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with conn.cursor(row_factory=dict_row) as cur:
        rows = cur.execute(
            f'SELECT "case", verified FROM eval.embedding_cases {where} ORDER BY id', params
        ).fetchall()
    return [EmbeddingCase.model_validate({**row["case"], "verified": row["verified"]}) for row in rows]


def save_embedding_case(conn: psycopg.Connection, case: EmbeddingCase) -> None:
    """Upsert a retrieval case. Its `verified` flag is a column too, written
    here because embedding cases have no separate review gate (this eval is
    diagnostic, not the contractual KPI freeze)."""
    conn.execute(
        """
        INSERT INTO eval.embedding_cases (id, country, language, "case", verified)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            country = EXCLUDED.country,
            language = EXCLUDED.language,
            "case" = EXCLUDED."case",
            verified = EXCLUDED.verified,
            updated_at = now()
        """,
        (
            case.id,
            case.country.upper(),
            case.language.lower(),
            Jsonb(case.model_dump(mode="json", exclude={"verified"}, exclude_none=True)),
            case.verified,
        ),
    )
    conn.commit()


# --------------------------------------------------------------------------- #
# Content hashes
# --------------------------------------------------------------------------- #


def _set_hash(pairs: Iterable[tuple[str, dict]]) -> str:
    digest = hashlib.sha256()
    for case_id, payload in sorted(pairs, key=lambda pair: pair[0]):
        digest.update(case_id.encode())
        digest.update(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode())
    return digest.hexdigest()[:12]


def golden_set_hash(cases: Iterable[GoldenCase]) -> str:
    """sha256 over the sorted (id, case JSON with the review fields stripped),
    first 12 hex chars. A verdict flip does not change the set; any edit to a
    case's content does."""
    return _set_hash((case.id, case_payload(case)) for case in cases)


def embedding_set_hash(cases: Iterable[EmbeddingCase]) -> str:
    return _set_hash(
        (case.id, case.model_dump(mode="json", exclude={"verified"}, exclude_none=True))
        for case in cases
    )
