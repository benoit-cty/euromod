"""Database loader for country-neutral legislation IR."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any
from uuid import UUID

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from nomotheca_ingest.core.chunker import chunk_text
from nomotheca_ingest.core.ir import InstrumentIR, ParsedDoc, TextIR, UnitIR, VersionIR


@dataclass(slots=True)
class LoadStats:
    """Counts of rows touched by a loader run."""

    instruments: int = 0
    units: int = 0
    versions: int = 0
    texts: int = 0
    chunks: int = 0
    retained_chunks: int = 0   # cited chunks past the new end of a shrunken text


class LegislationLoader:
    """Load parsed legal instruments into the invariant legislation schema."""

    def __init__(self, conn: Connection) -> None:
        """Create a loader bound to an open psycopg connection."""
        self.conn = conn

    def load(self, doc: ParsedDoc) -> LoadStats:
        """Load all instruments in one parsed document inside a transaction."""
        stats = LoadStats()
        with self.conn.transaction():
            for instrument in doc.instruments:
                instrument_id = self._upsert_instrument(instrument)
                stats.instruments += 1
                unit_ids = self._upsert_units(instrument_id, instrument.units, stats)
                for unit in instrument.units:
                    for version in unit.versions:
                        version_id = self._upsert_version(unit_ids[unit.path], version)
                        stats.versions += 1
                        for text in version.texts:
                            text_id = self._upsert_text(version_id, text)
                            stats.texts += 1
                            self._replace_chunks(text_id, instrument, unit, version, text, stats)
        return stats

    def _upsert_instrument(self, instrument: InstrumentIR) -> UUID:
        """Insert or update an instrument using the schema natural key."""
        jurisdiction_id = self._jurisdiction_id(instrument.jurisdiction)
        source_id = self._source_id(instrument.source_code)
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO instruments
                  (jurisdiction_id, source_id, instrument_type, eli, national_id, title,
                   adoption_date, publication_date, metadata)
                VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s::jsonb)
                ON CONFLICT (source_id, national_id) DO UPDATE
                SET title = EXCLUDED.title,
                    eli = COALESCE(instruments.eli, EXCLUDED.eli),
                    metadata = instruments.metadata || EXCLUDED.metadata
                RETURNING id
                """,
                (
                    jurisdiction_id,
                    source_id,
                    instrument.instrument_type,
                    instrument.eli,
                    instrument.national_id,
                    Jsonb(instrument.title),
                    instrument.adoption_date,
                    instrument.publication_date,
                    Jsonb(instrument.metadata),
                ),
            )
            return cur.fetchone()[0]

    def _existing_unit_id(self, instrument_id: UUID, unit: UnitIR) -> UUID | None:
        """Find the same article already loaded under a different structural path.

        A full-code ingest nests articles under their book/chapter (path
        'liv_1.art_197'); fetching that same article standalone — what the
        workflow's scout does — yields a flat path ('art_197'). Keyed on path
        alone the two become separate legal_units, and because the
        no-overlap EXCLUDE constraint is per legal_unit, a superseded
        consolidation then stays open-ended next to its replacement and can
        outrank it in retrieval. Match on the stable article identity first.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT id FROM legal_units
                WHERE instrument_id = %s
                  AND ((national_id IS NOT NULL AND national_id = %s)
                       OR (citation IS NOT NULL AND citation = %s))
                ORDER BY (national_id = %s) DESC, nlevel(path) DESC
                LIMIT 1
                """,
                (instrument_id, unit.national_id, unit.citation, unit.national_id),
            )
            row = cur.fetchone()
        return row[0] if row else None

    def _upsert_units(self, instrument_id: UUID, units: list[UnitIR], stats: LoadStats) -> dict[str, UUID]:
        """Insert or update structural units and return ids keyed by IR path."""
        unit_ids: dict[str, UUID] = {}
        for unit in sorted(units, key=lambda item: item.path.count(".")):
            parent_id = unit_ids.get(unit.parent_path) if unit.parent_path else None
            if not unit.is_container:
                existing = self._existing_unit_id(instrument_id, unit)
                if existing is not None:
                    unit_ids[unit.path] = existing
                    stats.units += 1
                    continue
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO legal_units
                      (instrument_id, parent_id, unit_type, ordinal, path, citation, eli,
                       national_id, is_container, metadata)
                    VALUES (%s, %s, %s, %s, %s::ltree, %s, %s, %s, %s, %s::jsonb)
                    ON CONFLICT (instrument_id, path) DO UPDATE
                    SET citation = EXCLUDED.citation,
                        eli = COALESCE(legal_units.eli, EXCLUDED.eli),
                        national_id = COALESCE(legal_units.national_id, EXCLUDED.national_id),
                        metadata = legal_units.metadata || EXCLUDED.metadata
                    RETURNING id
                    """,
                    (
                        instrument_id,
                        parent_id,
                        unit.unit_type,
                        unit.ordinal,
                        unit.path,
                        unit.citation,
                        unit.eli,
                        unit.national_id,
                        unit.is_container,
                        Jsonb(unit.metadata),
                    ),
                )
                unit_ids[unit.path] = cur.fetchone()[0]
                stats.units += 1
        return unit_ids

    def _chain_versions(self, unit_id: UUID, version: VersionIR) -> Any:
        """Close the version a new consolidation supersedes; bound the new one.

        Legifrance mints a fresh consolidated text (open-ended validity) every
        time an article is amended, and says nothing about the previous one.
        Loaded verbatim, two versions of the same article stay 'in_force' at
        once and `validity @> as_of` — the temporal filter every consumer
        relies on — stops discriminating. Chain them instead: the older
        version ends where the newer begins.

        Returns the upper bound to use for the incoming version: its own
        valid_to, or the start of an already-loaded later version when it is
        open-ended.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE legal_unit_versions
                SET validity = daterange(lower(validity), %(from)s, '[)'),
                    version_status = CASE WHEN version_status = 'in_force'
                                          THEN 'repealed' ELSE version_status END
                WHERE legal_unit_id = %(unit)s
                  AND lower(validity) < %(from)s
                  AND (upper(validity) IS NULL OR upper(validity) > %(from)s)
                """,
                {"unit": unit_id, "from": version.valid_from},
            )
            if version.valid_to is not None:
                return version.valid_to
            cur.execute(
                "SELECT min(lower(validity)) FROM legal_unit_versions "
                "WHERE legal_unit_id = %s AND lower(validity) > %s",
                (unit_id, version.valid_from),
            )
            row = cur.fetchone()
        return row[0] if row else None

    def _upsert_version(self, unit_id: UUID, version: VersionIR) -> UUID:
        """Insert a legal unit version unless its source version already exists."""
        if version.source_version_id:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id FROM legal_unit_versions
                    WHERE legal_unit_id = %s AND source_version_id = %s
                    """,
                    (unit_id, version.source_version_id),
                )
                row = cur.fetchone()
            if row is not None:
                return row[0]

        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM legal_unit_versions "
                "WHERE legal_unit_id = %s AND lower(validity) = %s",
                (unit_id, version.valid_from),
            )
            row = cur.fetchone()
        if row is not None:
            return row[0]

        valid_to = self._chain_versions(unit_id, version)
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO legal_unit_versions
                  (legal_unit_id, validity, version_status, source_version_id, eli_version,
                   citation_label, fetch_snapshot_id, amendment_note, metadata)
                VALUES (%s, daterange(%s, %s, '[)'), %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb)
                RETURNING id
                """,
                (
                    unit_id,
                    version.valid_from,
                    valid_to,
                    version.status.value,
                    version.source_version_id,
                    version.eli_version,
                    version.citation_label,
                    version.fetch_snapshot_id,
                    Jsonb(version.amendment_note),
                    Jsonb(version.metadata),
                ),
            )
            return cur.fetchone()[0]

    def _upsert_text(self, version_id: UUID, text: TextIR) -> UUID:
        """Insert or replace a language text for a legal unit version."""
        content_hash = _sha256_text(text.content)
        mt_engine = text.metadata.get("mt_engine") if text.authenticity.value == "machine_translation" else None
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO unit_texts
                  (version_id, lang, authenticity, content, content_html, search_config,
                   mt_engine, content_hash, metadata)
                VALUES (
                  %s, %s, %s, %s, %s,
                  (SELECT config FROM lang_fts_config WHERE lang = %s),
                  %s, %s, %s::jsonb
                )
                ON CONFLICT (version_id, lang, authenticity) DO UPDATE
                SET content = EXCLUDED.content,
                    content_html = EXCLUDED.content_html,
                    content_hash = EXCLUDED.content_hash,
                    metadata = unit_texts.metadata || EXCLUDED.metadata
                RETURNING id
                """,
                (
                    version_id,
                    text.lang,
                    text.authenticity.value,
                    text.content,
                    text.content_html,
                    text.lang,
                    mt_engine,
                    content_hash,
                    Jsonb(text.metadata),
                ),
            )
            return cur.fetchone()[0]

    def _replace_chunks(
        self,
        text_id: UUID,
        instrument: InstrumentIR,
        unit: UnitIR,
        version: VersionIR,
        text: TextIR,
        stats: LoadStats,
    ) -> None:
        """Regenerate retrieval chunks for a loaded unit text.

        Chunks are upserted on (unit_text_id, seq) instead of dropped and
        recreated, so re-ingesting a text keeps chunk ids stable. Two things
        depend on that: citation_registry references chunks with a plain FK
        (the retention rule — a cited chunk cannot be hard-deleted, and a
        delete/insert re-ingest raised a ForeignKeyViolation that failed the
        whole run), and embeddings hang off chunk ids, staleness being decided
        by input_hash — so unchanged chunks keep the vectors they already have.
        Chunks past the end of a now-shorter text are dropped unless cited;
        a cited leftover is retained and counted rather than deleted.
        """
        context_header = _context_header(instrument, unit, version, text.lang)
        chunks = chunk_text(text.content, context_header)
        with self.conn.cursor() as cur:
            for chunk in chunks:
                cur.execute(
                    """
                    INSERT INTO chunks
                      (unit_text_id, seq, char_start, char_end, content, context_header,
                       search_config, token_count)
                    VALUES (
                      %s, %s, %s, %s, %s, %s,
                      (SELECT search_config FROM unit_texts WHERE id = %s),
                      %s
                    )
                    ON CONFLICT (unit_text_id, seq) DO UPDATE
                    SET char_start = EXCLUDED.char_start,
                        char_end = EXCLUDED.char_end,
                        content = EXCLUDED.content,
                        context_header = EXCLUDED.context_header,
                        search_config = EXCLUDED.search_config,
                        token_count = EXCLUDED.token_count
                    """,
                    (
                        text_id,
                        chunk.seq,
                        chunk.char_start,
                        chunk.char_end,
                        chunk.content,
                        chunk.context_header,
                        text_id,
                        _rough_token_count(chunk.content),
                    ),
                )
            cur.execute(
                """
                DELETE FROM chunks
                WHERE unit_text_id = %s
                  AND seq >= %s
                  AND id NOT IN (SELECT cited_chunk_id FROM citation_registry
                                 WHERE cited_chunk_id IS NOT NULL)
                """,
                (text_id, len(chunks)),
            )
            cur.execute(
                "SELECT count(*) FROM chunks WHERE unit_text_id = %s AND seq >= %s",
                (text_id, len(chunks)),
            )
            stats.retained_chunks += cur.fetchone()[0]
        stats.chunks += len(chunks)

    def _jurisdiction_id(self, code: str) -> int:
        """Resolve a jurisdiction code to its database identity."""
        return self._single_value("SELECT id FROM jurisdictions WHERE code = %s", (code,))

    def _source_id(self, code: str) -> int:
        """Resolve a source code to its database identity."""
        return self._single_value("SELECT id FROM sources WHERE code = %s", (code,))

    def _single_value(self, query: str, params: tuple[Any, ...]) -> Any:
        """Return a single scalar value or raise a lookup error."""
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, params)
            row = cur.fetchone()
        if row is None:
            msg = f"Lookup failed for query: {query}"
            raise ValueError(msg)
        return next(iter(row.values()))


def _context_header(instrument: InstrumentIR, unit: UnitIR, version: VersionIR, lang: str) -> str:
    """Build the breadcrumb header stored beside retrieval chunks."""
    title = instrument.title.get(lang) or next(iter(instrument.title.values()))
    return f"{title} > {unit.citation} (vig. {version.valid_from.isoformat()})"


def _sha256_text(value: str) -> str:
    """Return the sha256 hex digest of UTF-8 text content."""
    return sha256(value.encode("utf-8")).hexdigest()


def _rough_token_count(value: str) -> int:
    """Estimate token count cheaply until a tokenizer-backed worker exists."""
    return len(value.split())
