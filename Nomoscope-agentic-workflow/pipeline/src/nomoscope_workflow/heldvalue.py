"""Recent texts that state the figure EUROMOD holds for the year before.

An act that amends by substitution names the old figure next to the new one
and shares no word with the parameter's description: Finance Act 2024 s. 3,
«by the substitution of “€44,000” for “€42,000”», is the 2025 standard-rate
band, was in the corpus, embedded and in force, and reached none of the
three models on the 18 Nov 2026 Irish panel. The held figure is an input of
the run, so searching for it reveals nothing about the answer; a text that
still states it unchanged confirms it just as well.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import date, timedelta

import psycopg

from .corpus import CHUNK_JOINS, HIT_COLUMNS, Scope, fetch_dicts, scope_codes
from .schema import ParameterValue, RetrievalHit

#: Chunks the leg may add to a run.
HELD_VALUE_MAX = 4
#: Figures searched for one parameter (a schedule holds many).
HELD_FIGURES_MAX = 6
#: A figure shorter than this is everywhere («20», «1.5») and is not searched.
MIN_DIGITS = 3

# Between two groups of three digits: nothing, a comma, a dot, a space, a
# no-break space or a narrow no-break space.
_GROUP = "[ ,.  ]?"


def _figure_pattern(number: float) -> str | None:
    """A regex for `number` as a legal text may write it, None when too short.

    42000 → 42 000, 42,000, 42.000, 42000 (and 42,000.00); 181.7 → 181.70,
    181,7. Never part of a longer number: 1 801,80 does not state 801,80.
    """
    if not math.isfinite(number) or number <= 0:
        return None
    text = f"{number:.6f}".rstrip("0").rstrip(".")
    whole, _, frac = text.partition(".")
    if len(whole.lstrip("0")) + len(frac) < MIN_DIGITS:
        return None
    groups = []
    while len(whole) > 3:
        groups.insert(0, whole[-3:])
        whole = whole[:-3]
    body = _GROUP.join([whole, *groups])
    if frac:
        # 181.7 is written 181.70; 0.125 stays as it is.
        body += "[.,]" + frac + ("0?" if len(frac) == 1 else "")
    else:
        body += "(?:[.,]00)?"
    return rf"(?<![\d.,])(?<!\d[ \u00a0\u202f]){body}(?![\d])(?![.,]\d)"


def held_figures(value: ParameterValue | None, unit: str | None) -> list[str]:
    """Regexes for the figures of the value EUROMOD holds, most telling first.

    A `/1` rate is held as a fraction and legislated in percent, so 0.1105 is
    searched as 11.05. Formula strings and booleans carry no figure.
    """
    raw = value.value if value is not None else None
    numbers: list[float] = []
    if isinstance(raw, bool) or raw is None:
        return []
    if isinstance(raw, (int, float)):
        numbers.append(float(raw) * 100 if unit == "/1" else float(raw))
    elif isinstance(raw, str):
        head = raw.split("#", 1)[0].strip()
        try:
            numbers.append(float(head))
        except ValueError:
            return []
    else:
        for bracket in raw:
            for name in ("threshold", "amount"):
                figure = getattr(bracket, name, None)
                if isinstance(figure, (int, float)):
                    numbers.append(float(figure))
            rate = getattr(bracket, "rate", None)
            if isinstance(rate, (int, float)):
                numbers.append(float(rate) * 100)
    patterns = dict.fromkeys(p for p in map(_figure_pattern, numbers) if p)
    # Longest first: the longer the figure, the fewer texts state it by chance.
    return sorted(patterns, key=len, reverse=True)[:HELD_FIGURES_MAX]


_SQL = f"""
WITH candidates AS MATERIALIZED (
  SELECT ch.id,
         (SELECT count(*) FROM unnest(%(patterns)s::text[]) p WHERE ch.content ~ p) AS stated
  FROM chunks ch
  {CHUNK_JOINS}
  JOIN jurisdictions j ON j.id = i.jurisdiction_id
  WHERE j.code = ANY(%(jurisdictions)s::text[])
    AND t.lang = %(lang)s
    AND i.source_trust_class <> 'context'
    AND lower(v.validity) > %(since)s::date AND lower(v.validity) <= %(until)s::date
    AND ch.content ~ ANY(%(patterns)s::text[])
)
SELECT {HIT_COLUMNS},
       c.stated::float8 AS score
FROM candidates c
JOIN chunks ch ON ch.id = c.id
{CHUNK_JOINS}
LEFT JOIN embeddings e ON e.chunk_id = ch.id AND e.model_id = %(model_id)s
ORDER BY c.stated DESC,
         {{distance}} NULLS LAST,
         lower(v.validity) DESC, ch.id
LIMIT %(k)s
"""


def held_value_passages(
    conn: psycopg.Connection,
    country: Scope,
    lang: str,
    as_of: date,
    until: date,
    patterns: Sequence[str],
    model_id: int,
    query_vector: str | None = None,
    known: set[str] | frozenset[str] = frozenset(),
) -> list[RetrievalHit]:
    """Chunks of texts entered into force in the year before `as_of`, or by
    `until`, that state a held figure — nearest to the query first.

    The window opens a year before the reference date: the act that set the
    held value itself (in force a full year earlier) stays out, the act that
    replaces it (voted in the autumn, in force on 1 January, or later in the
    system year) is in. They are `located` hits: in the list on purpose, and
    checked like any other chunk if cited.
    """
    if not patterns:
        return []
    distance = "e.embedding <=> %(qvec)s::halfvec(1024)" if query_vector is not None else "NULL::float8"
    rows = fetch_dicts(
        conn,
        _SQL.format(distance=distance),
        {
            "patterns": list(patterns),
            "jurisdictions": scope_codes(country),
            "lang": lang,
            "since": as_of - timedelta(days=365),
            "until": max(until, as_of),
            "model_id": model_id,
            "qvec": query_vector,
            "k": HELD_VALUE_MAX + len(known),
        },
    )
    hits = [RetrievalHit(method="located", **row) for row in rows if row["chunk_id"] not in known]
    return hits[:HELD_VALUE_MAX]
