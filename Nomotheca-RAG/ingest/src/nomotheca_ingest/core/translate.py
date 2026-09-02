"""Batch machine translation of unit texts into English.

Finds legal_unit_versions that have no English unit_texts row, translates their
best available source text with an LLM (via nomoscope_workflow.llm), and inserts
the result as an ordinary unit_texts row flagged authenticity='machine_translation',
plus its retrieval chunks. Idempotent: already-translated versions are skipped.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from typing import Protocol
from uuid import UUID

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from nomotheca_ingest.core.chunker import chunk_text

DEFAULT_TARGET_LANG = "en"
DEFAULT_TRANSLATION_REQUEST_TIMEOUT_SECONDS = 120.0
# Newline-aware split size for LLM calls; keeps each completion well under
# the 8k max_tokens configured in nomoscope_workflow.llm.run_agent.
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
    citation: str
    title: dict[str, str]
    valid_from: date | None


@dataclass(frozen=True, slots=True)
class TranslationBuildStats:
    """Counts returned by a translation build run."""

    scanned: int = 0
    translated: int = 0
    failed: int = 0


TranslationProgressCallback = Callable[[dict[str, int | str]], None]


class TranslationBackend(Protocol):
    """Minimal interface used by the database translation builder."""

    engine: str

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Return the translation of one plain-text segment."""


class LLMTranslationBackend:
    """Translate through nomoscope_workflow.llm's provider-prefixed PydanticAI agents."""

    def __init__(self, model: str, *, request_timeout: float | None = DEFAULT_TRANSLATION_REQUEST_TIMEOUT_SECONDS) -> None:
        """Load .env credentials and keep the provider-prefixed model name."""
        try:
            from nomoscope_workflow.config import load_config
            from nomoscope_workflow.llm import run_agent
        except ImportError as exc:  # pragma: no cover - exercised by operator environment
            msg = "Install translation dependencies with: uv sync --extra translate"
            raise RuntimeError(msg) from exc

        load_config()  # side effect: load_dotenv() for the provider API keys
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
    progress: TranslationProgressCallback | None = None,
) -> TranslationBuildStats:
    """Translate every version lacking a target-language text, one row per version.

    Commits after each stored translation so an interrupted run keeps the
    LLM output already paid for.
    """
    stats = TranslationBuildStats()

    for source in iter_texts_needing_translation(conn, target_lang=target_lang, limit=limit):
        stats = TranslationBuildStats(stats.scanned + 1, stats.translated, stats.failed)
        _emit_progress(progress, "translating", stats, source.citation)
        if dry_run:
            continue
        try:
            translated = translate_content(backend, source.content, source.lang, target_lang)
            store_translation(conn, source, translated, target_lang=target_lang, engine=backend.engine)
            conn.commit()
            stats = TranslationBuildStats(stats.scanned, stats.translated + 1, stats.failed)
            _emit_progress(progress, "translated", stats, source.citation)
        except Exception as exc:  # keep the batch going; report failures at the end
            conn.rollback()
            stats = TranslationBuildStats(stats.scanned, stats.translated, stats.failed + 1)
            _emit_progress(progress, "failed", stats, f"{source.citation}: {exc}")

    _emit_progress(progress, "done", stats, "")
    return stats


def _emit_progress(
    progress: TranslationProgressCallback | None,
    phase: str,
    stats: TranslationBuildStats,
    detail: str,
) -> None:
    """Emit a progress event if a callback is registered."""
    if progress is None:
        return
    progress(
        {
            "phase": phase,
            "scanned": stats.scanned,
            "translated": stats.translated,
            "failed": stats.failed,
            "detail": detail,
        }
    )


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
    query = """
        SELECT count(DISTINCT t.version_id)
        FROM unit_texts t
        WHERE t.lang <> %(target)s
          AND NOT EXISTS (
              SELECT 1 FROM unit_texts e
              WHERE e.version_id = t.version_id AND e.lang = %(target)s
          )
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
    query = """
        SELECT DISTINCT ON (t.version_id)
               t.id, t.version_id, t.lang, t.content,
               u.citation, i.title, lower(v.validity) AS valid_from
        FROM unit_texts t
        JOIN legal_unit_versions v ON v.id = t.version_id
        JOIN legal_units u ON u.id = v.legal_unit_id
        JOIN instruments i ON i.id = u.instrument_id
        WHERE t.lang <> %(target)s
          AND NOT EXISTS (
              SELECT 1 FROM unit_texts e
              WHERE e.version_id = t.version_id AND e.lang = %(target)s
          )
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
    """Insert the machine_translation unit_texts row and its retrieval chunks."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO unit_texts
              (version_id, lang, authenticity, content, search_config,
               translation_of, source_lang, mt_engine, content_hash, metadata)
            VALUES (
              %s, %s, 'machine_translation', %s,
              (SELECT config FROM lang_fts_config WHERE lang = %s),
              %s, %s, %s, %s, %s
            )
            ON CONFLICT (version_id, lang, authenticity) DO NOTHING
            RETURNING id
            """,
            (
                source.version_id,
                target_lang,
                translated,
                target_lang,
                source.id,
                source.lang,
                engine,
                sha256(translated.encode("utf-8")).hexdigest(),
                Jsonb({"translated_from_text_id": str(source.id)}),
            ),
        )
        row = cur.fetchone()
        if row is None:  # a concurrent run already inserted this translation
            return None
        text_id = row[0]

        context_header = _context_header(source, target_lang)
        for chunk in chunk_text(translated, context_header):
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
                    len(chunk.content.split()),
                ),
            )
    return text_id


def _context_header(source: TextForTranslation, target_lang: str) -> str:
    """Build the breadcrumb header for translated chunks (same shape as the loader's)."""
    title = source.title.get(target_lang) or source.title.get(source.lang) or next(iter(source.title.values()))
    suffix = f" (vig. {source.valid_from.isoformat()})" if source.valid_from else ""
    return f"{title} > {source.citation}{suffix}"
