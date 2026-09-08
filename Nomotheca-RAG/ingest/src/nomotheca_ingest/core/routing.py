"""Which path a pasted URL belongs on: an adapter, a contributed document, or neither.

A reviewer pastes whatever the source document cites. Sometimes that is an
official act on a national portal, in which case ingesting the *page* would be
wrong twice over — the portal chrome is not the law, and the same act would end
up stored under two identities once the adapter fetches it properly. So a URL
is classified first:

  ``adapter``      a known official source: the jurisdiction and the national
                   id the existing legislation ingester already accepts;
  ``contributed``  anything else: fetch it, archive it, ingest it as the
                   reviewer's document;
  ``refused``      recognised, but not something to ingest this way, with a
                   hint saying what to do instead.

**No country lives here.** Which domains a member state publishes on, what its
ids look like, which URLs are not one document and how to recover an id that is
not in the path are all adapter facts, declared as a `countries.base.UrlSource`
and collected by `countries.registry.url_sources`. Adding a sixth member state
is an adapter, not an edit to this module.

The UI calls this before starting a run so it can announce a switch; the
`document` command calls it again when the run starts, so the library never
trusts the caller's classification.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal
from urllib.parse import urlsplit

from nomotheca_ingest.countries.base import UrlSource

RouteKind = Literal["contributed", "adapter", "refused"]


@dataclass(slots=True)
class RouteOutcome:
    """What to do with one pasted URL."""

    kind: RouteKind
    url: str
    #: adapter only: what the legislation ingester needs.
    jurisdiction: str | None = None
    national_id: str | None = None
    source_name: str | None = None
    #: How the id was found: 'url', or the tier a resolver answered on.
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
    host = urlsplit(url.strip()).hostname or ""
    return host.lower().removeprefix("www.")


def _serves(source: UrlSource, host: str) -> bool:
    """True when a host is one of a source's domains, or below one."""
    return any(host == domain or host.endswith(f".{domain}") for domain in source.domains)


def known_source(url: str, sources: dict[str, UrlSource]) -> tuple[str, UrlSource] | None:
    """The (jurisdiction, portal) this URL belongs to, if any does."""
    host = _host(url)
    for jurisdiction, source in sources.items():
        if _serves(source, host):
            return jurisdiction, source
    return None


def route_url(
    url: str,
    *,
    sources: dict[str, UrlSource] | None = None,
    database_url: str | None = None,
) -> RouteOutcome:
    """Classify one URL against the registered official portals.

    ``sources`` defaults to every adapter's declared portal; tests inject their
    own so routing stays a pure function, resolver and all.
    """
    if sources is None:
        from nomotheca_ingest.countries.registry import url_sources

        sources = url_sources()

    url = url.strip()
    found = known_source(url, sources)
    if found is None:
        return RouteOutcome(kind="contributed", url=url)

    jurisdiction, source = found
    for pattern, hint in source.refusals:
        if pattern.search(url):
            return RouteOutcome(kind="refused", url=url, hint=hint)

    match = source.id_pattern.search(url)
    if match:
        return RouteOutcome(
            kind="adapter",
            url=url,
            jurisdiction=jurisdiction,
            national_id=match.group(0),
            source_name=source.name,
            resolved_by="url",
        )

    if source.resolve is not None:
        resolution = source.resolve(url, database_url)
        if resolution is not None:
            return RouteOutcome(
                kind="adapter",
                url=url,
                jurisdiction=jurisdiction,
                national_id=resolution.national_id,
                source_name=source.name,
                resolved_by=resolution.tier,
            )

    return RouteOutcome(
        kind="refused",
        url=url,
        hint=source.no_id_hint
        or (
            f"this is a {source.name} URL but it carries no ingestible id — "
            "paste the document id, or upload the saved file"
        ),
    )
