"""French citation resolver, ELI resolution, and freshness canary definitions.

Legifrance is never fetched for text: it is DataDome-protected, and the FR
adapter reads DILA JSON from Tricoteuses keyed by an 18-character
JORFTEXT/LEGIARTI id. But ELI is the form reviewers and official documents
actually cite (`/eli/arrete/2020/12/28/CCPD2036946A/jo/texte`), and it carries
a NOR, not a DILA id. Legifrance itself redirects such a URL to
`/jorf/id/JORFTEXT...`, so **only the redirect target is read** — no page
content is ever parsed or stored (ADR 0002).

Three tiers, in order, stopping at the first that answers:

1. our own database — the act may already be ingested with its ELI stored;
2. an HTTP request with browser-like headers, following the redirect;
3. a headless browser, only on a DataDome 403, and only when the optional
   ``legifrance`` extra is installed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from typing import Literal

from nomotheca_ingest.core.browser import browser_available, with_browser
from nomotheca_ingest.core.db import connect
from nomotheca_ingest.core.ir import CanaryFact, CitationRef, SourceRef

#: The DILA id shapes the FR adapter can fetch (KALI: collective agreements).
DILA_ID = re.compile(r"\b(?:JORFTEXT|LEGIARTI|KALITEXT|KALIARTI)\d{12}\b")

#: A bare NOR (ministerial reference), which reviewers also paste.
NOR = re.compile(r"\b[A-Z]{4}\d{7}[A-Z]\b")

ResolutionTier = Literal["url", "database", "http", "browser"]

#: Browser-like headers: Legifrance's edge rejects a bare client outright, and
#: the whole point of the request is to be told where the ELI URL points.
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
}


@dataclass(slots=True, frozen=True)
class EliResolution:
    """The whole result of resolving an ELI URL: an id and where it came from.

    Deliberately carries nothing else. The browser tier exists to read a
    redirect target and for no other purpose, and a result type with no place
    to put page content keeps that limit visible (ADR 0002).
    """

    national_id: str
    tier: ResolutionTier


#: Legifrance's own NOR route, which redirects to /jorf/id/JORFTEXT...
NOR_URL = "https://www.legifrance.gouv.fr/jorf/nor/{nor}"


def eli_url_for(url: str) -> str:
    """Normalise an ELI URL for an exact match against instruments.eli."""
    return url.strip().split("#", 1)[0].rstrip("/")


def as_legifrance_url(reference: str) -> str:
    """A bare NOR is what an official document prints; make it a URL to follow."""
    reference = reference.strip()
    if NOR.fullmatch(reference):
        return NOR_URL.format(nor=reference)
    return reference


def resolve_from_database(url: str, database_url: str | None) -> EliResolution | None:
    """Tier 1: the act may already be ingested, with this ELI stored on it."""
    if not database_url:
        return None
    normalised = eli_url_for(url)
    nor_match = NOR.search(url)
    with connect(database_url) as conn:
        row = conn.execute(
            """
            SELECT national_id FROM instruments
            WHERE national_id IS NOT NULL
              AND (eli = %(eli)s OR eli = %(eli)s || '/' OR eli = %(url)s
                   -- NULL when the URL carries no NOR, so the row simply does
                   -- not match; the cast is what tells Postgres the type.
                   OR metadata ->> 'nor' = %(nor)s::text)
            LIMIT 1
            """,
            {
                "eli": normalised,
                "url": url.strip(),
                "nor": nor_match.group(0) if nor_match else None,
            },
        ).fetchone()
    if row and row[0]:
        return EliResolution(national_id=row[0], tier="database")
    return None


def http_attempt(url: str, timeout: float = 20.0) -> tuple[EliResolution | None, int | None]:
    """Tier 2: follow the redirect with browser-like headers, read the final URL.

    Returns the resolution (or None) *and* the status code, because the status
    is what decides whether tier 3 runs at all: ADR 0002 scopes the headless
    browser to the DataDome 403 and to nothing else. A transport error or a
    page that simply carries no id is None with no status — unresolvable, and
    refused with a hint rather than guessed at.
    """
    import httpx

    try:
        with httpx.Client(timeout=timeout, follow_redirects=True, headers=BROWSER_HEADERS) as client:
            response = client.get(url)
    except Exception:
        return None, None
    match = DILA_ID.search(str(response.url))
    if match:
        return EliResolution(national_id=match.group(0), tier="http"), response.status_code
    return None, response.status_code


def resolve_in_browser(url: str, timeout_ms: int = 30000) -> EliResolution | None:
    """Tier 3: open the URL in a headless browser and read the final URL.

    Purpose-limited: the page is loaded so the redirect resolves, and only
    ``page.url`` is read. No HTML is returned, parsed or stored.
    """

    def final_url_of(browser) -> str:
        page = browser.new_page(user_agent=BROWSER_HEADERS["User-Agent"])
        page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        return page.url

    final_url = with_browser("chromium", final_url_of)
    if final_url is None:
        return None
    match = DILA_ID.search(final_url)
    return EliResolution(national_id=match.group(0), tier="browser") if match else None


def resolve_legifrance_url(
    url: str,
    database_url: str | None = None,
    *,
    tiers=None,
) -> EliResolution | None:
    """Turn an ELI-form Legifrance URL (or a bare NOR) into a DILA id.

    ``tiers`` overrides the three callables for tests; each takes the URL and
    returns an `EliResolution` or None. The browser tier is skipped entirely
    when the optional extra is absent, so the CPU-only default environment
    keeps working — the outcome is then the refusal hint.

    Exposed for reuse: the scout drops ELI-only URLs today and can turn them
    into ids with exactly this function.
    """
    url = as_legifrance_url(url)
    already = DILA_ID.search(url)
    if already:
        # Nothing to resolve: the id is right there in what was pasted.
        return EliResolution(national_id=already.group(0), tier="url")
    if tiers is None:
        tiers = default_tiers(database_url)
    for tier in tiers:
        if tier is None:
            continue
        resolution = tier(url)
        if resolution is not None:
            return resolution
    return None


def default_tiers(database_url: str | None = None) -> list:
    """The three tiers, in order, with the browser scoped to a DataDome block.

    The browser tier is a closure over what the HTTP tier saw, because ADR 0002
    limits it to the 403 case: a page that answered 200 without an id, or a
    request that never connected, is not a reason to start Chromium.
    """
    blocked_by_datadome = False

    def database_tier(target: str) -> EliResolution | None:
        return resolve_from_database(target, database_url)

    def http_tier(target: str) -> EliResolution | None:
        nonlocal blocked_by_datadome
        resolution, status = http_attempt(target)
        blocked_by_datadome = status == 403
        return resolution

    def browser_tier(target: str) -> EliResolution | None:
        if not blocked_by_datadome or not browser_available():
            return None
        return resolve_in_browser(target)

    return [database_tier, http_tier, browser_tier]


class FrResolver:
    """French citations a reviewer can actually paste: a DILA id, an ELI or
    Legifrance URL, or a bare NOR — resolved to the one DILA document.

    Free-text citations («CGI art. 197») are refused by name: there is no
    citation index to resolve them against, and guessing an article is how a
    stale or wrong text gets ingested. Until 16 Nov 2026 this was a
    placeholder that raised NotImplementedError for everything (code audit).
    """

    def __init__(self, database_url: str | None = None) -> None:
        self._database_url = database_url

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Resolve a DILA id, Legifrance URL or NOR to its DILA source reference."""
        citation = ref.citation.strip()
        if not (DILA_ID.search(citation) or NOR.fullmatch(citation) or "legifrance" in citation):
            msg = (
                f"FR citation {citation!r} is not resolvable: pass a DILA id (JORFTEXT…, LEGIARTI…, "
                "KALITEXT…), a Legifrance/ELI URL or a NOR — or use `instrument fr <id>`"
            )
            raise ValueError(msg)
        resolution = resolve_legifrance_url(citation, self._database_url)
        if resolution is None:
            msg = f"FR citation {citation!r} did not resolve to a DILA id (Legifrance unreachable or blocked)"
            raise ValueError(msg)
        source_code = "FR-KALI" if resolution.national_id.startswith("KALI") else "FR-LEGI"
        return [
            SourceRef(
                jurisdiction="FR",
                source_code=source_code,
                source_id=resolution.national_id,
                source_type="instrument",
            )
        ]


def canary_facts() -> list[CanaryFact]:
    """Return known French legal facts used to detect stale resolvers."""
    return [
        CanaryFact(
            citation="CGI art. 197",
            assert_latest_start_gte=date(2025, 2, 16),
            reason="LF2025 rewrote the income-tax brackets; older resolvers are stale.",
        )
    ]
