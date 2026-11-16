"""What the two reparse paths share: their stats and the reload step.

Archive-first means a parser change reaches documents already ingested by
replaying their stored bytes, never by refetching. Adapter-ingested acts
replay through `pipeline.reparse_snapshots` (the adapter's parser, the
SourceRef stored with the snapshot); contributed documents through
`contributed.reparse_documents` (the heading builder, the reviewer's
declaration read back from the instrument). Both end here: the re-parsed
document is loaded with the ordinary idempotent upsert and the texts whose
content changed are counted — their vectors are now stale for
`embeddings build` to refresh.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

import psycopg

from nomotheca_ingest.core.ir import ParsedDoc
from nomotheca_ingest.core.loader import LegislationLoader


@dataclass(slots=True)
class ReparseStats:
    """What a reparse pass did: archive rows seen, parsed, loaded, skipped."""

    snapshots: int = 0
    parsed: int = 0
    loaded: int = 0
    skipped: int = 0
    texts_changed: int = 0

    def as_dict(self) -> dict[str, int]:
        return {
            "snapshots": self.snapshots,
            "parsed": self.parsed,
            "loaded": self.loaded,
            "skipped": self.skipped,
            "texts_changed": self.texts_changed,
        }


def reload(
    conn: psycopg.Connection,
    loader: LegislationLoader,
    doc: ParsedDoc,
    stats: ReparseStats,
    *,
    replace_units_of: UUID | None = None,
) -> None:
    """Load a re-parsed document and count the texts whose content changed.

    ``replace_units_of`` drops that instrument's units and versions first, in
    the same transaction (a contributed document's sections are re-cut by the
    heading builder; the instrument row, its id, class and kind stay).
    """
    before = text_hashes(conn, doc)
    if replace_units_of is None:
        loader.load(doc)
    else:
        with conn.transaction():
            conn.execute(
                "DELETE FROM legal_unit_versions v USING legal_units u "
                "WHERE v.legal_unit_id = u.id AND u.instrument_id = %s",
                (replace_units_of,),
            )
            conn.execute("DELETE FROM legal_units WHERE instrument_id = %s", (replace_units_of,))
            loader.load(doc)
    stats.loaded += 1
    stats.texts_changed += sum(1 for h in text_hashes(conn, doc) if h not in before)


def text_hashes(conn: psycopg.Connection, doc: ParsedDoc) -> set[str]:
    """Content hashes of the unit texts a parsed document maps to (change detection)."""
    hashes: set[str] = set()
    for instrument in doc.instruments:
        for unit in instrument.units:
            for version in unit.versions:
                for row in conn.execute(
                    """
                    SELECT t.content_hash
                    FROM unit_texts t
                    JOIN legal_unit_versions v ON v.id = t.version_id
                    WHERE v.source_version_id = %s AND v.fetch_snapshot_id = %s
                    """,
                    (version.source_version_id, version.fetch_snapshot_id),
                ).fetchall():
                    hashes.add(row[0])
    return hashes
