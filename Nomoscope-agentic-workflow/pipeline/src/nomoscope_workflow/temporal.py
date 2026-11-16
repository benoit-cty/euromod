"""Temporal rules: reference dates and the income-year vintage checks.

The retrieval date of a parameter (income-year shift, start-of-year basis),
how far into the system year a later version may come from, and the critique's
income-year checks — `_consolidated_in_force`, `_income_year_date_issues`,
the cross-article applicability proof (split out of pipeline.py, code audit 4).
Every income-year date derives from `schema.income_year_for`.
"""

from __future__ import annotations

import re
from datetime import date

from . import idiom, retrieval
from .schema import (
    ParameterRecord,
    TemporalBasis,
    income_year_for,
    start_of_year_as_of,
)

def _later_until(record: ParameterRecord, as_of: date) -> date | None:
    """How far past as_of retrieval looks for versions of the same system year.

    Only for in-force parameters: an income-year parameter already retrieves
    at 1 July of the following year (_retrieval_as_of), and a start-of-year
    one wants the value of 1 January.
    """
    if record.information.temporal_basis in (TemporalBasis.INCOME_YEAR, TemporalBasis.START_OF_YEAR):
        return None  # start_of_year: a change later in the year is next year's value
    return date(as_of.year, 12, 31)


def _retrieval_as_of(record: ParameterRecord, as_of: date) -> date:
    """The date used to select in-force legislation versions.

    income_year parameters (FR income tax family): the enacting finance act is
    published months AFTER the income year it governs, so look for versions
    consolidated mid-way through the year FOLLOWING the income year — for
    system year 2025 (income year 2024) that is 1 July 2025, when LF 2025 is
    consolidated. Open-ended current versions still match, and the critique's
    version-window check catches the act not being in the corpus yet.
    """
    if record.information.temporal_basis == TemporalBasis.INCOME_YEAR:
        return date(income_year_for(as_of.year) + 1, 7, 1)
    if record.information.temporal_basis == TemporalBasis.START_OF_YEAR:
        return start_of_year_as_of(as_of)
    return as_of


def _consolidated_in_force(
    provenance: dict | None, retrieval_as_of: date, income_year: int, article_text: str
) -> bool:
    """Is the cited text a consolidated code article in force on the retrieval date?

    France assesses income year Y in Y+1, and the code article as consolidated
    on 1 July Y+1 (`_retrieval_as_of`) is the text that assessment applies —
    CGI art. 197 "en vigueur du 16 février 2025 au 21 février 2026" is the
    barème for 2024 income. That holds however old the version is: art. 223
    sexies has read the same since 2018 because the CEHR thresholds never
    moved, and no finance act for Y restates it. The old rule treated every
    version older than the budget-act window as "probably last year's value"
    and demanded a finance-act clause naming Y, which rejected correct
    unchanged proposals. Two guards keep the presumption honest:

    * an open-ended version only proves "not amended" up to the day we
      fetched it, so the snapshot must postdate the retrieval date;
    * a text whose applicability clause names the NEXT income year (CDHR:
      "applicables à l'imposition des revenus de l'année 2025", in force
      Feb 2025) is for that year, not this one.
    """
    if not provenance or provenance.get("instrument_type") != "code":
        return False
    start = retrieval.validity_start(provenance.get("validity"))
    end = retrieval.validity_end(provenance.get("validity"))
    if start is None or start > retrieval_as_of or (end is not None and end <= retrieval_as_of):
        return False
    retrieved = provenance.get("retrieved_at")
    if provenance.get("open_ended") and retrieved is not None:
        retrieved_day = retrieved.date() if hasattr(retrieved, "date") else retrieved
        if retrieved_day < retrieval_as_of:
            return False
    names_this = re.search(rf"\b{income_year}\b", article_text) is not None
    for hit in re.finditer(rf"\b{income_year + 1}\b", article_text):
        if _APPLICABILITY.search(article_text[max(0, hit.start() - 200) : hit.start()]) and not names_this:
            return False
    return True


def _income_year_date_issues(
    valid_from: date | None,
    version_start: date | None,
    income_year: int,
    cited_text: str = "",
    consolidated_in_force: bool = False,
) -> tuple[list[str], bool]:
    """Mechanical date checks for income_year parameters.

    Returns (issues, provisional): issues empty = consistent; provisional=True
    when the cited version predates the budget-act window — the window opens
    1 December of the income year: finance acts for income year Y are normally
    promulgated late December Y (or later — Feb 2025 for LF 2025). An older
    version almost certainly states the previous year's value: the act for Y
    is not in the corpus (yet), which routes the item to PROVISIONAL rather
    than plain critique failure.

    Exemption: a cited text that NAMES the income year ("à compter de
    l'imposition des revenus de l'année 2025") proves its own vintage, however
    early it was enacted — the CDHR was instituted by LF 2025 (Feb 2025) FOR
    2025 income. Consolidated code articles drop such clauses (CGI art. 224
    never says 2025), so the year-naming extract is the finance-act article;
    the propose prompt nudges the model towards it.

    Second exemption, `consolidated_in_force` (decided by
    `_consolidated_in_force` from the corpus): the cited text is the code
    article as consolidated on the retrieval date, i.e. the text the income
    year's assessment applies — an old version start means the value did not
    change, not that the act is missing.
    """
    issues: list[str] = []
    provisional = False
    if valid_from != date(income_year, 1, 1):
        issues.append(
            f"income-year parameter: valid_from must be exactly {income_year}-01-01 "
            f"(the income-year start, NOT the act's publication or in-force date), got "
            f"{valid_from.isoformat() if valid_from else 'none'}"
        )
    window = date(income_year, 12, 1)
    names_year = re.search(rf"\b{income_year}\b", cited_text) is not None
    if (
        version_start is not None
        and version_start < window
        and not names_year
        and not consolidated_in_force
    ):
        provisional = True
        issues.append(
            f"cited version in force since {version_start.isoformat()} predates the "
            f"budget-act window for income year {income_year} and its text does not "
            f"name {income_year} — likely the previous year's value; the act for "
            f"{income_year} income may not be in the corpus yet (treat as provisional)"
        )
    return issues, provisional


_ARTICLE_NUM = re.compile(r"art(?:icle|\.)\s*([0-9]+(?:\s+[A-Za-z]+)*)", re.IGNORECASE)

_APPLICABILITY = idiom.FR_APPLICABILITY


def _cross_article_year_proof(cited_citation: str | None, text: str, income_year: int) -> bool:
    """True when `text` ties the CITED article to the income year.

    Finance acts often state the applicability of a code article they created
    in a cross-reference — LF 2025 art. 10: "La contribution mentionnée au I
    de l'article 224 du code général des impôts due au titre de l'imposition
    des revenus de l'année 2025…". A mention of the cited article number with
    the income year nearby (±400 chars) proves the vintage of the cited
    consolidated article, which itself names no year.
    """
    if not cited_citation:
        return False
    match = _ARTICLE_NUM.search(cited_citation)
    if not match:
        return False
    number = match.group(1).strip()
    mentions = list(re.finditer(rf"article\s+{re.escape(number)}\b", text, re.IGNORECASE))
    if not mentions:
        return False
    for hit in mentions:
        window = text[max(0, hit.start() - 400) : hit.end() + 400]
        if re.search(rf"\b{income_year}\b", window):
            return True
    # Proximity is the strong signal but it is not how finance acts are drafted.
    # `text` is ONE article (pulled whole via retrieval.unit_chunks), and its
    # closing applicability clause governs every amendment above it: LF 2025
    # art. 2 rewrites the barème in CGI art. 197 at offset 199 and only says
    # "dû au titre de l'année 2024" at offset 5365 — 5 166 characters later, so
    # the window could never see it and every FR barème case refused. Inside a
    # single article, "this article mentions the cited article" plus "this
    # article carries an applicability clause for the income year" is the proof.
    for hit in re.finditer(rf"\b{income_year}\b", text):
        if _APPLICABILITY.search(text[max(0, hit.start() - 200) : hit.start()]):
            return True
    return False


# Public name for the other packages (the eval used the private one).
retrieval_as_of = _retrieval_as_of
