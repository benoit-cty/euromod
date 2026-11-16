"""Small text helpers every parser needs: path tokens, folding, hashes, tables,
month names, unique citations.

Nothing here knows a country. Language-specific data (month names) is keyed
by language code.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable
from hashlib import sha256

# ---------------------------------------------------------------------------
# Folding, tokens, hashes
# ---------------------------------------------------------------------------


def fold_accents(value: str) -> str:
    """Strip diacritics (NFKD, combining marks dropped); case is kept."""
    decomposed = unicodedata.normalize("NFKD", value)
    return "".join(char for char in decomposed if not unicodedata.combining(char))


_NON_TOKEN = re.compile(r"[^0-9A-Za-z]+")


def path_token(value: str, *, fold: bool = False) -> str:
    """Sanitize a label into one ltree-compatible path token ("unknown" if empty).

    With ``fold``, accented letters keep their base letter («Disposición» →
    ``disposicion``) instead of becoming a separator.
    """
    if fold:
        value = fold_accents(value.strip().lower())
    token = _NON_TOKEN.sub("_", value).strip("_").lower()
    return token or "unknown"


def sha256_hex(data: str | bytes) -> str:
    """Hex sha256 of bytes, or of text encoded as UTF-8."""
    return sha256(data.encode("utf-8") if isinstance(data, str) else data).hexdigest()


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------


def pipe_rows(rows: Iterable[Iterable[str]], *, edges: bool = False) -> list[str]:
    """Render table rows one per line, cells separated by `` | ``.

    A figure stays on the line of its row heading, so a proposal can quote
    the row verbatim. Rows with no text are dropped. ``edges`` adds the
    leading and trailing bars (``| a | b |``).
    """
    rendered: list[str] = []
    for row in rows:
        cells = list(row)
        if any(cells):
            line = " | ".join(cells)
            rendered.append(f"| {line} |" if edges else line)
    return rendered


# ---------------------------------------------------------------------------
# Month names, by language
# ---------------------------------------------------------------------------

#: Month names as they appear in dates, per language (lowercase; accented and
#: unaccented spellings both listed where portals use both).
MONTHS: dict[str, dict[str, int]] = {
    "fr": {
        "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6,
        "juillet": 7, "août": 8, "aout": 8, "septembre": 9, "octobre": 10, "novembre": 11,
        "décembre": 12, "decembre": 12,
    },
    "en": {
        "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
        "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    },
}


def month_names(langs: Iterable[str] | None = None) -> dict[str, int]:
    """One name → month table for the given languages (all known when None)."""
    table: dict[str, int] = {}
    for lang in MONTHS if langs is None else langs:
        table.update(MONTHS.get(lang, {}))
    return table


def month_alternation(langs: Iterable[str] | None = None) -> str:
    """The month names of these languages as a regex alternation."""
    return "|".join(re.escape(name) for name in month_names(langs))


# ---------------------------------------------------------------------------
# Unique citations
# ---------------------------------------------------------------------------


class UniqueCitations:
    """Hands out citations unique within one act.

    The loader matches a unit by its ``national_id`` *or* its citation, so two
    units sharing a citation silently collapse into one and the second one's
    text is lost or grafted onto the first (BOE's repeated «Disposición
    transitoria primera» blocks; DSS/2B/2025/38's column header printed over
    six tables). A repeat gets `` (2)``, `` (3)``…; with ``max_len`` the base is
    cut so base plus suffix still fit.
    """

    def __init__(self, *, max_len: int | None = None) -> None:
        self._max_len = max_len
        self._used: set[str] = set()

    def claim(self, base: str) -> str:
        citation = self._fit(base, "")
        n = 2
        while citation in self._used:
            citation = self._fit(base, f" ({n})")
            n += 1
        self._used.add(citation)
        return citation

    def _fit(self, base: str, suffix: str) -> str:
        if self._max_len is None:
            return base + suffix
        return base[: self._max_len - len(suffix)] + suffix
