"""Critique issues the workflow routes on: one wording, one classifier.

A critique issue is text the reviewer and the retrying model read. A few of
them also steer the run — a source gap earns a scout round, a misquote alone
earns an extra attempt — and those decisions used to match fragments of the
wording at the call site, so rewording a message silently changed routing
(code audit 4). Every routed issue is now written from the constants below
and recognised by `code_of`, built from the same constants.
"""

from __future__ import annotations

import re
from enum import Enum


class IssueCode(str, Enum):
    CITATION_NOT_RETRIEVED = "citation_not_retrieved"
    NOT_VERBATIM = "not_verbatim"
    MISQUOTE_HINT = "misquote_hint"
    OPERAND_NOT_RETRIEVED = "operand_not_retrieved"
    OPERAND_NOT_VERBATIM = "operand_not_verbatim"
    OPERAND_MISQUOTE_HINT = "operand_misquote_hint"
    PREDATES_BUDGET_WINDOW = "predates_budget_window"
    NEVER_NAMES_INCOME_YEAR = "never_names_income_year"
    GUIDANCE_ONLY = "guidance_only"


CITATION_NOT_RETRIEVED = "citation_chunk_id missing or not among retrieved chunks"
NOT_VERBATIM = "supporting_extract is not a verbatim quote of the cited chunk"
MISQUOTE_HINT_PREFIX = "the cited chunk reads: «"
PREDATES_BUDGET_WINDOW = "predates the budget-act window"
NEVER_NAMES_INCOME_YEAR = "never names income year"
GUIDANCE_ONLY = "supported by guidance only: no legislation among the cited sources"


def misquote_hint(passage: str) -> str:
    return f"{MISQUOTE_HINT_PREFIX}{passage}» — quote it exactly as written, without correcting it"


def operand_not_retrieved(name: str) -> str:
    return f"derivation: operand {name} cites a chunk that was not retrieved"


def operand_not_verbatim(name: str) -> str:
    return f"derivation: operand {name}'s extract is not a verbatim quote of its chunk"


def operand_hint(name: str, hint: str) -> str:
    return f"derivation: operand {name}: {hint}"


_PATTERNS: tuple[tuple[re.Pattern[str], IssueCode], ...] = (
    (re.compile(re.escape(CITATION_NOT_RETRIEVED)), IssueCode.CITATION_NOT_RETRIEVED),
    (re.compile(re.escape(NOT_VERBATIM) + "$"), IssueCode.NOT_VERBATIM),
    (re.compile(re.escape(MISQUOTE_HINT_PREFIX)), IssueCode.MISQUOTE_HINT),
    (re.compile(re.escape(operand_not_retrieved("NAME")).replace("NAME", r"\w+") + "$"), IssueCode.OPERAND_NOT_RETRIEVED),
    (re.compile(re.escape(operand_not_verbatim("NAME")).replace("NAME", r"\w+") + "$"), IssueCode.OPERAND_NOT_VERBATIM),
    (re.compile(re.escape(operand_hint("NAME", MISQUOTE_HINT_PREFIX)).replace("NAME", r"\w+")), IssueCode.OPERAND_MISQUOTE_HINT),
    (re.compile(re.escape(PREDATES_BUDGET_WINDOW)), IssueCode.PREDATES_BUDGET_WINDOW),
    (re.compile(re.escape(NEVER_NAMES_INCOME_YEAR)), IssueCode.NEVER_NAMES_INCOME_YEAR),
    (re.compile(re.escape(GUIDANCE_ONLY) + "$"), IssueCode.GUIDANCE_ONLY),
)

#: The corpus lacks the establishing text: worth a gap-fill round.
SOURCE_GAP = frozenset(
    {IssueCode.CITATION_NOT_RETRIEVED, IssueCode.PREDATES_BUDGET_WINDOW, IssueCode.NEVER_NAMES_INCOME_YEAR}
)
#: Nothing but a misquote: worth one more attempt with the passage in hand.
MISQUOTE = frozenset(
    {
        IssueCode.NOT_VERBATIM,
        IssueCode.MISQUOTE_HINT,
        IssueCode.OPERAND_NOT_VERBATIM,
        IssueCode.OPERAND_MISQUOTE_HINT,
    }
)
#: Shown to the reviewer, never an objection: the verdict ignores it, and so
#: must every decision taken on "nothing but …". Until 17 Nov 2026 the
#: guidance line had no code, so a misquote of a circular or an instruction —
#: the PDF tables where models misquote most — never earned its extra attempt
#: (31 of MiniMax M2.7's 54 FR rejections on 16 Nov carried both lines).
INFORMATIONAL = frozenset({IssueCode.GUIDANCE_ONLY})


def code_of(issue: str) -> IssueCode | None:
    """The routed kind of an issue, or None for one that routes nothing."""
    for pattern, code in _PATTERNS:
        if pattern.search(issue):
            return code
    return None
