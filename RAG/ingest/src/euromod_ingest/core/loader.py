"""Database loader for country-neutral legislation IR."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any
from uuid import UUID

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from euromod_ingest.core.chunker import chunk_text
from euromod_ingest.core.ir import InstrumentIR, ParsedDoc, TextIR, UnitIR, VersionIR


@dataclass(slots=True)
class LoadStats:
    """Counts of rows touched by a loader run."""

    instruments: int = 0
    units: int = 0
    versions: int = 0
    texts: int = 0
    chunks: int = 0


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
                            stats.chunks += self._replace_chunks(text_id, instrument, unit, version, text)
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

    def _upsert_units(self, instrument_id: UUID, units: list[UnitIR], stats: LoadStats) -> dict[str, UUID]:
        """Insert or update structural units and return ids keyed by IR path."""
        unit_ids: dict[str, UUID] = {}
        for unit in sorted(units, key=lambda item: item.path.count(".")):
            parent_id = unit_ids.get(unit.parent_path) if unit.parent_path else None
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
                    version.valid_to,
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
    ) -> int:
        """Regenerate retrieval chunks for a loaded unit text."""
        context_header = _context_header(instrument, unit, version, text.lang)
        chunks = chunk_text(text.content, context_header)
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM chunks WHERE unit_text_id = %s", (text_id,))
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
        return len(chunks)

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
