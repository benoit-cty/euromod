"""EUROMOD Country Report ingestion — a separate, non-legislative corpus class.

Country Reports describe the EUROMOD model itself, so they must never become
citable evidence for parameter proposals: everything loaded here carries the
``context`` source-trust class and the Nomoscope evidence retrieval excludes
that class. The corpus exists so the frame/scout steps and the validation UI
can search it (parameter acronym -> semantic description), with the same
FTS/vector machinery as the legislation corpus.

File-based: the "fetch" is reading a Markdown file already converted from the
official Word/PDF report, archived as a fetch_snapshot like any other source.
"""

from __future__ import annotations

from datetime import date
from hashlib import sha256
from pathlib import Path
from uuid import UUID

import psycopg

from nomotheca_ingest.core.db import create_fetch_run, finish_fetch_run
from nomotheca_ingest.core.documents import build_document
from nomotheca_ingest.core.ir import (
    InstrumentIR,
    ParsedDoc,
    SourceRef,
    SourceTrustClass,
    Trigger,
)
from nomotheca_ingest.core.loader import LegislationLoader, LoadStats

INSTRUMENT_TYPE = "country_report"
ID_SYSTEM = "euromod_cr"
SKILL_VERSION = "cr-md-0.1"

_UNIT_TYPE_BY_DEPTH = {2: "section"}


def source_code_for(jurisdiction: str) -> str:
    """Source registry code for a jurisdiction's Country Report corpus."""
    return f"{jurisdiction.upper()}-EUROMOD-CR"


def parse_country_report(
    markdown: str,
    jurisdiction: str,
    vintage: str,
    source_code: str,
    valid_from: date,
    snapshot_id: UUID,
    lang: str = "en",
) -> InstrumentIR:
    """Convert one Country Report Markdown file into a loadable InstrumentIR.

    Every heading becomes a legal_unit; the text between a heading and the
    next heading (of any level) is that unit's own content. Hierarchy follows
    markdown levels only — the CRs' decimal numbering is not trusted (the FR
    report reuses '2.' for two different chapters).

    The shape is the shared `documents.build_document`; what is said here is
    only what a Country Report *is*: a context corpus, titled by its own h1,
    cited as "CR <CC> <vintage>", and versioned once per vintage.
    """
    jurisdiction = jurisdiction.upper()
    national_id = f"CR-{jurisdiction}-{vintage}"
    return build_document(
        text=markdown,
        jurisdiction=jurisdiction,
        source_code=source_code,
        instrument_type=INSTRUMENT_TYPE,
        source_trust_class=SourceTrustClass.CONTEXT,
        national_id=national_id,
        title=f"EUROMOD Country Report {jurisdiction} {vintage}",
        title_from_heading=True,
        lang=lang,
        valid_from=valid_from,
        snapshot_id=snapshot_id,
        citation_prefix=f"CR {jurisdiction} {vintage}",
        pattern="markdown",
        version_key=f"{national_id}@{valid_from.isoformat()}",
        unit_type_by_depth=_UNIT_TYPE_BY_DEPTH,
        metadata={"vintage": vintage, "corpus_class": INSTRUMENT_TYPE},
    )


def _ensure_source(conn: psycopg.Connection, jurisdiction: str, source_code: str) -> None:
    """Idempotently register the per-country EUROMOD-CR source row."""
    row = conn.execute(
        "SELECT id FROM jurisdictions WHERE code = %s", (jurisdiction,)
    ).fetchone()
    if row is None:
        msg = f"Unknown jurisdiction: {jurisdiction} (seed it before ingesting its CR)"
        raise ValueError(msg)
    conn.execute(
        """
        INSERT INTO sources (jurisdiction_id, code, name, id_system, fetch_skill, terms)
        VALUES (%s, %s, %s, %s, 'core/country_reports',
                '{"note": "non-legislative corpus: excluded from evidence retrieval"}'::jsonb)
        ON CONFLICT (code) DO NOTHING
        """,
        (row[0], source_code, f"EUROMOD Country Report ({jurisdiction})", ID_SYSTEM),
    )


def _write_file_snapshot(
    conn: psycopg.Connection, run_id: UUID, source_code: str, path: Path, content: bytes
) -> UUID:
    """Archive the Markdown file bytes as the version's provenance snapshot."""
    row = conn.execute(
        """
        INSERT INTO fetch_snapshots (run_id, source_id, url, content_type, content_hash, raw_content)
        VALUES (%s, (SELECT id FROM sources WHERE code = %s), %s, 'text/markdown', %s, %s)
        RETURNING id
        """,
        (run_id, source_code, path.resolve().as_uri(), sha256(content).hexdigest(), content),
    ).fetchone()
    return row[0]


def ingest_country_report(
    path: str | Path,
    jurisdiction: str,
    database_url: str,
    *,
    vintage: str = "Y16",
    valid_from: date = date(2022, 1, 1),
    lang: str = "en",
) -> LoadStats:
    """Load one Country Report Markdown file into the legislation DB.

    Idempotent: re-running updates texts and regenerates chunks in place
    (versions are deduplicated on source_version_id).
    """
    file_path = Path(path)
    raw = file_path.read_bytes()
    jurisdiction = jurisdiction.upper()
    source_code = source_code_for(jurisdiction)

    with psycopg.connect(database_url) as conn:
        _ensure_source(conn, jurisdiction, source_code)
        run_id = create_fetch_run(conn, source_code, SKILL_VERSION, Trigger.BULK_SEED)
        try:
            snapshot_id = _write_file_snapshot(conn, run_id, source_code, file_path, raw)
            instrument = parse_country_report(
                raw.decode("utf-8"), jurisdiction, vintage, source_code, valid_from, snapshot_id, lang
            )
            ref = SourceRef(
                jurisdiction=jurisdiction,
                source_code=source_code,
                source_id=instrument.national_id or file_path.name,
                source_type=INSTRUMENT_TYPE,
            )
            stats = LegislationLoader(conn).load(ParsedDoc(ref=ref, instruments=[instrument]))
            finish_fetch_run(
                conn,
                run_id,
                "succeeded",
                {
                    "trigger": Trigger.BULK_SEED.value,
                    "file": file_path.name,
                    "instruments": stats.instruments,
                    "units": stats.units,
                    "versions": stats.versions,
                    "texts": stats.texts,
                    "chunks": stats.chunks,
                },
            )
        except Exception as exc:
            finish_fetch_run(conn, run_id, "failed", {"trigger": Trigger.BULK_SEED.value, "error": str(exc)})
            raise
    return stats
