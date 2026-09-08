"""Which path a pasted URL belongs on: an adapter, a contributed document, or neither.

A reviewer pastes whatever the source document cites. Sometimes that is an
official act on a national portal, in which case ingesting the *page* would be
wrong twice over — the portal chrome is not the law, and the same act would
end up stored under two identities once the adapter fetches it properly. So a
URL is classified first:

  ``adapter``      a known official source: the jurisdiction and the national
                   id the existing legislation ingester already accepts;
  ``contributed``  anything else: fetch it, archive it, ingest it as the
                   reviewer's document;
  ``refused``      recognised, but not something to ingest this way, with a
                   hint saying what to do instead.

The UI calls this before starting a run so it can announce a switch; the
`document` command calls it again when the run starts, so the library never
trusts the caller's classification.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, Literal

RouteKind = Literal["contributed", "adapter", "refused"]

#: Per-country URL shapes, mirroring the scout's harvesting rules
#: (nomoscope_workflow.scout.COUNTRY_SOURCES) so the two cannot disagree about
#: what a portal's id looks like.
KNOWN_SOURCES: dict[str, dict] = {
    "FR": {
        "name": "Legifrance",
        "domains": ("legifrance.gouv.fr",),
        # JORF texts and single consolidated code articles. Deliberately not
        # LEGITEXT: see `WHOLE_CODE_PATTERN`.
        "id_pattern": re.compile(r"\b(?:JORFTEXT|LEGIARTI)\d{12}\b"),
    },
    "ES": {
        "name": "BOE",
        "domains": ("boe.es",),
        "id_pattern": re.compile(r"\bBOE-A-\d{4}-\d+\b"),
    },
    "NL": {
        "name": "wetten.overheid.nl",
        "domains": ("wetten.overheid.nl",),
        "id_pattern": re.compile(r"\bBWBR\d{7}\b"),
    },
    "IE": {
        "name": "electronic Irish Statute Book",
        "domains": ("irishstatutebook.ie",),
        "id_pattern": re.compile(r"\b(?:19|20)\d{2}/act/\d{1,3}\b"),
    },
    "LT": {
        "name": "e-seimas / e-tar",
        "domains": ("e-seimas.lrs.lt", "e-tar.lt"),
        "id_pattern": re.compile(r"\b(?:TAR\.[0-9A-F]{12}|[0-9a-f]{32})\b"),
    },
}

#: A Legifrance whole-code URL. Ingesting one by accident is two thousand
#: articles, not a document — the same exclusion the scout applies.
WHOLE_CODE_PATTERN = re.compile(r"\bLEGITEXT\d{12}\b")

WHOLE_CODE_HINT = (
    "that is a whole Legifrance code (LEGITEXT), not one document — paste the "
    "article URL (LEGIARTI...) or the JORF text (JORFTEXT...) instead"
)

ELI_HINT = (
    "this Legifrance ELI URL carries a NOR, not a DILA id, and could not be "
    "resolved — paste the JORFTEXT id or upload the saved file"
)

#: Legifrance ELI form: /eli/arrete/2020/12/28/CCPD2036946A/jo/texte
ELI_PATTERN = re.compile(r"legifrance\.gouv\.fr/(?:eli|jorf/id)/", re.IGNORECASE)


@dataclass(slots=True)
class RouteOutcome:
    """What to do with one pasted URL."""

    kind: RouteKind
    url: str
    #: adapter only: what the legislation ingester needs.
    jurisdiction: str | None = None
    national_id: str | None = None
    source_name: str | None = None
    #: How the id was found: 'url' or a resolver tier ('database', 'http', 'browser').
    resolved_by: str | None = None
    #: refused only: what the reviewer should do instead.
    hint: str | None = None
    #: contributed only: prefill for the title and validity fields.
    suggestions: dict = field(default_factory=dict)

    def as_json(self) -> dict:
        """One flat, machine-readable line for the UI's route pre-check."""
        return {
            "outcome": self.kind,
            "url": self.url,
            "jurisdiction": self.jurisdiction,
            "national_id": self.national_id,
            "source": self.source_name,
            "resolved_by": self.resolved_by,
            "hint": self.hint,
            "suggestions": self.suggestions,
        }


def _host(url: str) -> str:
    """Lowercased host of a URL, with no port and no leading 'www.'."""
    from urllib.parse import urlsplit

    host = urlsplit(url.strip()).hostname or ""
    return host.lower().removeprefix("www.")


def _matches(host: str, domains: tuple[str, ...]) -> bool:
    """True when a host is one of a source's domains, or below one."""
    return any(host == domain or host.endswith(f".{domain}") for domain in domains)


def known_source(url: str) -> tuple[str, dict] | None:
    """The (jurisdiction, rules) whose portal this URL belongs to, if any."""
    host = _host(url)
    for jurisdiction, rules in KNOWN_SOURCES.items():
        if _matches(host, rules["domains"]):
            return jurisdiction, rules
    return None


def route_url(
    url: str,
    *,
    resolve_legifrance: Callable[[str], object | None] | None = None,
) -> RouteOutcome:
    """Classify one URL.

    ``resolve_legifrance`` turns an ELI-form Legifrance URL into a DILA id
    (see `countries.fr.resolver.resolve_legifrance_url`). It is injected so
    routing stays a pure function under test, and so the network and browser
    tiers are the caller's decision, never a hidden side effect of routing.
    """
    url = url.strip()
    found = known_source(url)
    if found is None:
        return RouteOutcome(kind="contributed", url=url)

    jurisdiction, rules = found
    if jurisdiction == "FR" and WHOLE_CODE_PATTERN.search(url):
        return RouteOutcome(kind="refused", url=url, hint=WHOLE_CODE_HINT)

    match = rules["id_pattern"].search(url)
    if match:
        return RouteOutcome(
            kind="adapter",
            url=url,
            jurisdiction=jurisdiction,
            national_id=match.group(0),
            source_name=rules["name"],
            resolved_by="url",
        )

    if jurisdiction == "FR" and resolve_legifrance is not None:
        resolution = resolve_legifrance(url)
        if resolution is not None:
            return RouteOutcome(
                kind="adapter",
                url=url,
                jurisdiction="FR",
                national_id=resolution.national_id,
                source_name=rules["name"],
                resolved_by=resolution.tier,
            )

    hint = ELI_HINT if jurisdiction == "FR" else (
        f"this is a {rules['name']} URL but it carries no ingestible id — paste "
        "the document id, or upload the saved file"
    )
    return RouteOutcome(kind="refused", url=url, hint=hint)
