"""Batch machine translation of unit texts into English.

Finds legal_unit_versions that have no English unit_texts row — or whose
machine translation was made from a source text that has changed since —
translates their best available source text with an LLM (via
nomos_llm.providers), and writes the result as an ordinary unit_texts row
flagged authenticity='machine_translation', plus its retrieval chunks (the
loader's chunk upsert, so chunk ids, cited chunks and unchanged vectors
survive). Idempotent: versions translated from their current source are
skipped.

Staleness: every machine translation records the source text's content hash
in `metadata.source_content_hash`. A `reparse` that changes the source makes
the hashes differ and the next run re-translates it. Before 16 Nov 2026 a
version counted as translated as soon as any English row existed, so the
English text and chunks kept the pre-reparse wording (code audit D10);
migration 0006 stamped the existing rows with their source's current hash.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from typing import Protocol
from uuid import UUID

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from nomotheca_ingest.core.chunker import chunk_text
from nomotheca_ingest.core.loader import LegislationLoader, LoadStats
from nomotheca_ingest.core.text import sha256_hex
from nomotheca_ingest.core.progress import BatchStats, ProgressCallback, emit

#: A version needs a translation when it has no target-language row, or when
#: its machine translation was made from another state of this source text.
#: `t` is the candidate source row; `%(target)s` the target language.
_NEEDS_TRANSLATION = """
    t.lang <> %(target)s
    AND NOT EXISTS (
        SELECT 1 FROM unit_texts e
        WHERE e.version_id = t.version_id AND e.lang = %(target)s
          AND NOT (e.authenticity = 'machine_translation'
                   AND e.translation_of = t.id
                   AND e.metadata ->> 'source_content_hash' IS DISTINCT FROM t.content_hash)
    )
"""

DEFAULT_TARGET_LANG = "en"
DEFAULT_TRANSLATION_REQUEST_TIMEOUT_SECONDS = 120.0
# Newline-aware split size for LLM calls; keeps each completion well under
# the 8k max_tokens configured in nomos_llm.providers.run_agent.
TRANSLATION_SEGMENT_CHARS = 6_000

LANG_NAMES = {
    "fr": "French",
    "nl": "Dutch",
    "de": "German",
    "es": "Spanish",
    "lt": "Lithuanian",
    "ga": "Irish",
    "en": "English",
}

TRANSLATION_SYSTEM_PROMPT = """\
You are a professional legal translator working on national tax-benefit legislation.
Translate the user's text from {source_lang} to {target_lang}.

Rules:
- Preserve the document structure exactly: paragraph breaks, article/paragraph numbering,
  list markers, indentation and blank lines.
- Never alter numbers, amounts, percentages, dates or legal identifiers.
- Keep untranslatable proper nouns and official act names in the original language,
  optionally followed by an English gloss in parentheses the first time they appear.
- Do not summarize, comment, or add headers. Output ONLY the translated text.
"""


@dataclass(frozen=True, slots=True)
class TextForTranslation:
    """A source unit_texts row that has no target-language sibling yet."""

    id: UUID
    version_id: UUID
    lang: str
    content: str
    content_hash: str
    citation: str
    title: dict[str, str]
    valid_from: date | None


class TranslationBackend(Protocol):
    """Minimal interface used by the database translation builder."""

    engine: str

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Return the translation of one plain-text segment."""


class LLMTranslationBackend:
    """Translate through nomos_llm.providers's provider-prefixed PydanticAI agents."""

    def __init__(self, model: str, *, request_timeout: float | None = DEFAULT_TRANSLATION_REQUEST_TIMEOUT_SECONDS) -> None:
        """Load .env credentials and keep the provider-prefixed model name."""
        try:
            from nomos_llm.env import load_env_file
            from nomos_llm.providers import run_agent
        except ImportError as exc:  # pragma: no cover - exercised by operator environment
            msg = "Install translation dependencies with: uv sync --extra translate"
            raise RuntimeError(msg) from exc

        load_env_file()  # the provider API keys
        self.engine = model
        self._run_agent = run_agent
        self._request_timeout = request_timeout

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate one segment, retrying transient provider errors."""
        from tenacity import retry, stop_after_attempt, wait_random_exponential

        system = TRANSLATION_SYSTEM_PROMPT.format(
            source_lang=LANG_NAMES.get(source_lang, source_lang),
            target_lang=LANG_NAMES.get(target_lang, target_lang),
        )

        @retry(wait=wait_random_exponential(min=1, max=30), stop=stop_after_attempt(3), reraise=True)
        def _invoke() -> str:
            return self._run_agent(
                self.engine, system, text, temperature=0.0, timeout=self._request_timeout
            ).strip()

        return _invoke()


def build_translations(
    conn: Connection,
    backend: TranslationBackend | None,
    *,
    target_lang: str = DEFAULT_TARGET_LANG,
    limit: int | None = None,
    dry_run: bool = False,
    progress: ProgressCallback | None = None,
) -> BatchStats:
    """Translate every version lacking a target-language text, one row per version.

    Commits after each stored translation so an interrupted run keeps the
    LLM output already paid for.
    """
    stats = BatchStats()

    for source in iter_texts_needing_translation(conn, target_lang=target_lang, limit=limit):
        stats = stats.plus(scanned=1)
        emit(progress, "translating", stats, detail=source.citation)
        if dry_run:
            stats = stats.plus(done=1)  # would translate
            continue
        try:
            translated = translate_content(backend, source.content, source.lang, target_lang)
            store_translation(conn, source, translated, target_lang=target_lang, engine=backend.engine)
            conn.commit()
            stats = stats.plus(done=1)
            emit(progress, "translated", stats, detail=source.citation)
        except Exception as exc:  # keep the batch going; report failures at the end
            conn.rollback()
            stats = stats.plus(failed=1)
            emit(progress, "failed", stats, detail=f"{source.citation}: {exc}")

    emit(progress, "done", stats)
    return stats


def count_texts_needing_translation(
    conn: Connection,
    *,
    target_lang: str = DEFAULT_TARGET_LANG,
    limit: int | None = None,
) -> int:
    """Count the versions `iter_texts_needing_translation` would yield.

    Same WHERE clause as the iterator (which keeps one source row per
    version), so a progress display can know the total upfront.
    """
    query = f"""
        SELECT count(DISTINCT t.version_id)
        FROM unit_texts t
        WHERE {_NEEDS_TRANSLATION}
    """
    with conn.cursor() as cur:
        cur.execute(query, {"target": target_lang})
        total = int(cur.fetchone()[0])
    return min(total, limit) if limit is not None else total


def iter_texts_needing_translation(
    conn: Connection,
    *,
    target_lang: str = DEFAULT_TARGET_LANG,
    limit: int | None = None,
) -> Iterable[TextForTranslation]:
    """Yield the best source text per version that has no target-language row.

    One candidate per version: authentic texts win over official translations,
    which win over machine translations; ties (BE fr+nl) break on lang order.
    """
    query = f"""
        SELECT DISTINCT ON (t.version_id)
               t.id, t.version_id, t.lang, t.content, t.content_hash,
               u.citation, i.title, lower(v.validity) AS valid_from
        FROM unit_texts t
        JOIN legal_unit_versions v ON v.id = t.version_id
        JOIN legal_units u ON u.id = v.legal_unit_id
        JOIN instruments i ON i.id = u.instrument_id
        WHERE {_NEEDS_TRANSLATION}
        ORDER BY t.version_id,
                 CASE t.authenticity
                     WHEN 'authentic' THEN 0
                     WHEN 'official_translation' THEN 1
                     ELSE 2
                 END,
                 t.lang
    """
    if limit is not None:
        query += " LIMIT %(limit)s"
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, {"target": target_lang, "limit": limit})
        for row in cur:
            yield TextForTranslation(
                id=row["id"],
                version_id=row["version_id"],
                lang=row["lang"],
                content=row["content"],
                content_hash=row["content_hash"],
                citation=row["citation"],
                title=row["title"],
                valid_from=row["valid_from"],
            )


def translate_content(
    backend: TranslationBackend, content: str, source_lang: str, target_lang: str
) -> str:
    """Translate a full text, splitting long content into newline-aware segments.

    When the source is already in the target language (e.g. English-authentic
    Irish legislation), the text is copied verbatim: no LLM call, no cost, and
    no risk of the model paraphrasing an already-correct rendering.
    """
    if source_lang == target_lang:
        return content
    segments = chunk_text(content, context_header="", max_chars=TRANSLATION_SEGMENT_CHARS)
    translated = [backend.translate(segment.content, source_lang, target_lang) for segment in segments]
    return "\n".join(part for part in translated if part)


def store_translation(
    conn: Connection,
    source: TextForTranslation,
    translated: str,
    *,
    target_lang: str,
    engine: str,
) -> UUID | None:
    """Write the machine_translation unit_texts row and its retrieval chunks.

    A new translation of a changed source replaces the stale row in place
    (same id); its chunks go through the loader's upsert, so chunk ids stay
    stable, cited chunks are retained and an unchanged chunk keeps its vector.
    Returns None when a concurrent run already wrote this exact translation.
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO unit_texts
              (version_id, lang, authenticity, content, search_config,
               translation_of, source_lang, mt_engine, content_hash, metadata)
            VALUES (
              %(version)s, %(target)s, 'machine_translation', %(content)s,
              (SELECT config FROM lang_fts_config WHERE lang = %(target)s),
              %(source)s, %(source_lang)s, %(engine)s, %(hash)s, %(metadata)s
            )
            ON CONFLICT (version_id, lang, authenticity) DO UPDATE
            SET content = EXCLUDED.content,
                translation_of = EXCLUDED.translation_of,
                source_lang = EXCLUDED.source_lang,
                mt_engine = EXCLUDED.mt_engine,
                content_hash = EXCLUDED.content_hash,
                metadata = unit_texts.metadata || EXCLUDED.metadata
            WHERE unit_texts.metadata ->> 'source_content_hash'
                  IS DISTINCT FROM EXCLUDED.metadata ->> 'source_content_hash'
            RETURNING id
            """,
            {
                "version": source.version_id,
                "target": target_lang,
                "content": translated,
                "source": source.id,
                "source_lang": source.lang,
                "engine": engine,
                "hash": sha256_hex(translated),
                "metadata": Jsonb(
                    {
                        "translated_from_text_id": str(source.id),
                        "source_content_hash": source.content_hash,
                    }
                ),
            },
        )
        row = cur.fetchone()
    if row is None:  # a concurrent run already wrote this translation
        return None
    text_id = row[0]
    LegislationLoader(conn).write_chunks(
        text_id, chunk_text(translated, _context_header(source, target_lang)), LoadStats()
    )
    return text_id


def _context_header(source: TextForTranslation, target_lang: str) -> str:
    """Build the breadcrumb header for translated chunks (same shape as the loader's)."""
    title = source.title.get(target_lang) or source.title.get(source.lang) or next(iter(source.title.values()))
    suffix = f" (vig. {source.valid_from.isoformat()})" if source.valid_from else ""
    return f"{title} > {source.citation}{suffix}"
