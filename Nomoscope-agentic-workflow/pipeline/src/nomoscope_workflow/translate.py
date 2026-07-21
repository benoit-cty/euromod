"""Machine translation of parameter texts into the law's language.

The enriched EUROMOD export carries English-only labels/descriptions while
legislation chunks are FTS-indexed in the source language, so the full-text
leg of hybrid retrieval was cross-language. This module fills
params.parameter_texts (origin='machine_translation') with law-language
renderings; frame() then prefers them when building the retrieval query.
Received Stage A fields are never modified — translations are Stage B
enrichment with provenance. See Param_Schema/openfisca_france_usage.md §5.
"""

from __future__ import annotations

import psycopg
from pydantic import BaseModel, ConfigDict, Field
from tenacity import retry, stop_after_attempt, wait_random_exponential

from .llm import run_agent
from .retrieval import LANG_BY_COUNTRY

LANG_NAMES = {
    "fr": "French",
    "nl": "Dutch",
    "es": "Spanish",
    "de": "German",
    "lt": "Lithuanian",
    "ga": "Irish",
    "en": "English",
}

FIELDS = ("label", "short_label", "description")

_SYSTEM = """You translate metadata of tax-benefit policy parameters from English into {language}.
The texts describe parameters of the {country} tax-benefit system as modelled in EUROMOD.
Use the official terminology of {country} fiscal and social legislation (the wording a national
tax code or official journal would use), because the translations are used to search the
legislation full-text.
Rules:
- Return one entry per input parameter, with its index copied UNCHANGED.
- Do not translate parameter codes (e.g. $tin_upthres1), acronyms, currency amounts or numbers.
- Translate only the fields provided; leave a field null when the input field is null.
- No commentary, no added information."""


class ParameterTranslation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Items are matched back by index: model_target strings can contain
    # characters (e.g. a trailing '$') that LLMs fail to echo verbatim.
    index: int = Field(description="Copied unchanged from the input")
    label: str | None = None
    short_label: str | None = None
    description: str | None = None


class TranslationBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    translations: list[ParameterTranslation]


def pending(
    conn: psycopg.Connection, country: str, lang: str, force: bool = False
) -> list[dict]:
    """Parameters of a country with English text but no MT rendering in lang yet."""
    condition = "" if force else """
        AND NOT EXISTS (
            SELECT 1 FROM params.parameter_texts t
            WHERE t.parameter_id = p.id AND t.lang = %(lang)s
              AND t.origin = 'machine_translation'
        )"""
    rows = conn.execute(
        f"""
        SELECT p.id, p.model_target,
               p.label ->> 'en' AS label,
               p.short_label ->> 'en' AS short_label,
               p.description ->> 'en' AS description
        FROM params.parameters p
        WHERE p.country = %(country)s
          AND coalesce(p.label ->> 'en', p.short_label ->> 'en', p.description ->> 'en')
              IS NOT NULL
          AND (p.label ->> %(lang)s) IS NULL {condition}
        ORDER BY p.model_target
        """,
        {"country": country, "lang": lang},
    ).fetchall()
    return [
        dict(zip(("id", "model_target", "label", "short_label", "description"), row))
        for row in rows
    ]


@retry(wait=wait_random_exponential(min=1, max=30), stop=stop_after_attempt(3), reraise=True)
def translate_batch(model: str, country: str, lang: str, items: list[dict]) -> TranslationBatch:
    """One structured-output LLM call translating a batch of parameters."""
    payload = "\n\n".join(
        f"index: {i}\n"
        f"label: {item['label']}\n"
        f"short_label: {item['short_label']}\n"
        f"description: {item['description']}"
        for i, item in enumerate(items)
    )
    return run_agent(
        model,
        _SYSTEM.format(language=LANG_NAMES.get(lang, lang), country=country),
        payload,
        output_type=TranslationBatch,
        timeout=180,
    )


def store(
    conn: psycopg.Connection,
    parameter_id: int,
    lang: str,
    translation: ParameterTranslation,
    engine: str,
    source: dict | None = None,
) -> int:
    """Upsert the MT rows for one parameter; returns rows written."""
    written = 0
    for field in FIELDS:
        content = getattr(translation, field)
        # An unchanged text (e.g. a short_label that is just the parameter
        # code) carries no cross-language signal — don't store it.
        if not content or (source and content.strip() == (source.get(field) or "").strip()):
            continue
        conn.execute(
            """
            INSERT INTO params.parameter_texts
                (parameter_id, lang, field, content, origin, engine)
            VALUES (%s, %s, %s, %s, 'machine_translation', %s)
            ON CONFLICT (parameter_id, lang, field, origin)
            DO UPDATE SET content = EXCLUDED.content, engine = EXCLUDED.engine,
                          created_at = now()
            """,
            (parameter_id, lang, field, content, engine),
        )
        written += 1
    return written


def translate_country(
    conn: psycopg.Connection,
    model: str,
    country: str,
    lang: str | None = None,
    batch_size: int = 8,
    limit: int = 0,
    force: bool = False,
    echo=print,
) -> dict:
    """Translate all pending parameters of a country; commits per batch."""
    lang = lang or LANG_BY_COUNTRY.get(country, "en")
    if lang == "en":
        echo(f"{country}: law language is English, nothing to translate")
        return {"parameters": 0, "texts": 0, "mismatches": 0}
    todo = pending(conn, country, lang, force=force)
    # Close the implicit transaction opened by the SELECT: each batch below
    # must commit durably and release its locks before the (slow) next LLM
    # call, or a whole run stays one open transaction blocking other writers.
    conn.commit()
    if limit:
        todo = todo[:limit]
    stats = {"parameters": 0, "texts": 0, "mismatches": 0}
    for start in range(0, len(todo), batch_size):
        batch = todo[start : start + batch_size]
        result = translate_batch(model, country, lang, batch)
        with conn.transaction():
            for translation in result.translations:
                item = batch[translation.index] if 0 <= translation.index < len(batch) else None
                if item is None:
                    stats["mismatches"] += 1
                    continue
                stats["texts"] += store(
                    conn, item["id"], lang, translation, engine=model, source=item
                )
                stats["parameters"] += 1
        conn.commit()
        echo(f"{country}: {min(start + batch_size, len(todo))}/{len(todo)} parameters translated")
    return stats


def law_language_texts(conn: psycopg.Connection, model_target: str, lang: str) -> dict[str, str]:
    """Best available rendering per field for one parameter (manual > openfisca > MT)."""
    rows = conn.execute(
        """
        SELECT DISTINCT ON (field) field, content
        FROM params.parameter_texts t
        JOIN params.parameters p ON p.id = t.parameter_id
        WHERE p.model_target = %s AND t.lang = %s
        ORDER BY field,
                 CASE origin WHEN 'manual' THEN 0 WHEN 'openfisca' THEN 1 ELSE 2 END
        """,
        (model_target, lang),
    ).fetchall()
    return {field: content for field, content in rows}
