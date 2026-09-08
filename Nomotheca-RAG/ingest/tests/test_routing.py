"""Tests for URL routing and Legifrance ELI resolution."""

from __future__ import annotations

import pytest

from nomotheca_ingest.countries.fr.resolver import (
    EliResolution,
    resolve_legifrance_url,
)
from nomotheca_ingest.core.routing import ELI_HINT, WHOLE_CODE_HINT, route_url

ELI_URL = "https://www.legifrance.gouv.fr/eli/arrete/2020/12/28/CCPD2036946A/jo/texte"


@pytest.mark.parametrize(
    ("url", "jurisdiction", "national_id"),
    [
        (
            "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430",
            "ES",
            "BOE-A-2015-11430",
        ),
        (
            "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-27288",
            "ES",
            "BOE-A-2024-27288",
        ),
        (
            "https://wetten.overheid.nl/BWBR0011353/2025-01-01",
            "NL",
            "BWBR0011353",
        ),
        (
            "https://wetten.overheid.nl/jci1.3:c:BWBR0011353&artikel=2.10&z=2025-01-01",
            "NL",
            "BWBR0011353",
        ),
        (
            "https://www.irishstatutebook.ie/eli/1997/act/39/enacted/en/html",
            "IE",
            "1997/act/39",
        ),
        (
            "https://e-seimas.lrs.lt/portal/legalAct/lt/TAD/TAR.C7E2E0B77E63",
            "LT",
            "TAR.C7E2E0B77E63",
        ),
        (
            "https://www.e-tar.lt/portal/lt/legalAct/f6d686707e7011e6b969d7ae07280e89",
            "LT",
            "f6d686707e7011e6b969d7ae07280e89",
        ),
        (
            "https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000051168007",
            "FR",
            "JORFTEXT000051168007",
        ),
        (
            "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051521140",
            "FR",
            "LEGIARTI000051521140",
        ),
    ],
)
def test_a_known_portal_url_routes_to_its_adapter(url, jurisdiction, national_id) -> None:
    """The reviewer pastes a portal URL; the legislation ingester gets an id."""
    outcome = route_url(url)

    assert outcome.kind == "adapter"
    assert (outcome.jurisdiction, outcome.national_id) == (jurisdiction, national_id)
    assert outcome.resolved_by == "url"


def test_a_whole_legifrance_code_is_refused_with_a_hint() -> None:
    """Two thousand articles is not a document — the scout excludes it too."""
    outcome = route_url("https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006069577")

    assert outcome.kind == "refused"
    assert outcome.hint == WHOLE_CODE_HINT


def test_an_unresolvable_eli_url_says_what_to_do_next() -> None:
    outcome = route_url(ELI_URL)

    assert outcome.kind == "refused"
    assert outcome.hint == ELI_HINT


def test_an_unknown_domain_is_a_contributed_document() -> None:
    for url in (
        "https://bofip.impots.gouv.fr/bofip/12345-PGP.html",
        "https://www.unedic.org/publications/circulaire-2025-01",
    ):
        assert route_url(url).kind == "contributed"


# --- ELI resolution tiers -------------------------------------------------


def _tier(result: EliResolution | None):
    """A stand-in for one resolution tier: answers, or passes."""
    return lambda url: result


def test_resolution_stops_at_the_first_tier_that_answers() -> None:
    database = EliResolution(national_id="JORFTEXT000042753489", tier="database")
    http = EliResolution(national_id="JORFTEXT999999999999", tier="http")

    resolved = resolve_legifrance_url(ELI_URL, tiers=[_tier(database), _tier(http)])

    assert resolved == database


def test_the_http_tier_answers_when_the_database_does_not() -> None:
    http = EliResolution(national_id="JORFTEXT000042753489", tier="http")

    resolved = resolve_legifrance_url(ELI_URL, tiers=[_tier(None), _tier(http)])

    assert resolved.tier == "http"


def test_the_browser_tier_is_the_last_resort() -> None:
    browser = EliResolution(national_id="JORFTEXT000042753489", tier="browser")

    resolved = resolve_legifrance_url(ELI_URL, tiers=[_tier(None), _tier(None), _tier(browser)])

    assert resolved.tier == "browser"


def test_a_missing_browser_extra_simply_skips_the_third_tier() -> None:
    """The CPU-only default environment must keep working without Chromium."""
    assert resolve_legifrance_url(ELI_URL, tiers=[_tier(None), _tier(None), None]) is None


def test_all_tiers_failing_resolves_to_nothing_not_to_a_guess() -> None:
    assert resolve_legifrance_url(ELI_URL, tiers=[_tier(None), _tier(None), _tier(None)]) is None


def test_a_resolved_url_routes_to_the_fr_adapter() -> None:
    resolution = EliResolution(national_id="JORFTEXT000042753489", tier="browser")

    outcome = route_url(ELI_URL, resolve_legifrance=lambda url: resolution)

    assert outcome.kind == "adapter"
    assert outcome.jurisdiction == "FR"
    assert outcome.national_id == "JORFTEXT000042753489"
    assert outcome.resolved_by == "browser"


def test_the_resolver_result_carries_an_id_and_a_tier_and_nothing_else() -> None:
    """No Legifrance page content is ever returned, parsed or stored (ADR 0002)."""
    fields = set(EliResolution.__dataclass_fields__)

    assert fields == {"national_id", "tier"}


def test_a_bare_nor_is_resolved_as_the_legifrance_url_it_names() -> None:
    """Official documents print a NOR, not a URL; the resolver takes both."""
    from nomotheca_ingest.countries.fr.resolver import as_legifrance_url

    assert as_legifrance_url("CCPD2036946A").endswith("/jorf/nor/CCPD2036946A")
    resolved = resolve_legifrance_url(
        "CCPD2036946A",
        tiers=[_tier(EliResolution(national_id="JORFTEXT000042753489", tier="database"))],
    )
    assert resolved.national_id == "JORFTEXT000042753489"


def test_a_pasted_dila_id_needs_no_network_at_all() -> None:
    """The id is already there: no tier runs, so no request is ever made."""
    def explode(url):  # pragma: no cover - must never be called
        raise AssertionError("no tier should run when the id is already in the URL")

    resolved = resolve_legifrance_url(
        "https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000051168007", tiers=[explode]
    )

    assert resolved.national_id == "JORFTEXT000051168007"


def test_the_browser_tier_runs_only_on_a_datadome_block(monkeypatch) -> None:
    """ADR 0002 scopes Chromium to the 403 — nothing else may start it."""
    from nomotheca_ingest.countries.fr import resolver

    started: list[str] = []
    monkeypatch.setattr(resolver, "browser_available", lambda: True)
    monkeypatch.setattr(
        resolver,
        "resolve_in_browser",
        lambda url: started.append(url)
        or EliResolution(national_id="JORFTEXT000042753489", tier="browser"),
    )
    monkeypatch.setattr(resolver, "resolve_from_database", lambda url, db: None)

    # A page that answered but carried no id: unresolvable, no browser.
    monkeypatch.setattr(resolver, "http_attempt", lambda url, timeout=20.0: (None, 200))
    assert resolver.resolve_legifrance_url(ELI_URL) is None
    assert started == []

    # A request that never connected: still no browser.
    monkeypatch.setattr(resolver, "http_attempt", lambda url, timeout=20.0: (None, None))
    assert resolver.resolve_legifrance_url(ELI_URL) is None
    assert started == []

    # DataDome: this is the one case the browser exists for.
    monkeypatch.setattr(resolver, "http_attempt", lambda url, timeout=20.0: (None, 403))
    assert resolver.resolve_legifrance_url(ELI_URL).tier == "browser"
    assert started == [ELI_URL]


def test_a_missing_browser_extra_skips_the_tier_even_on_a_403(monkeypatch) -> None:
    """Without Chromium the outcome is the refusal hint, not a crash."""
    from nomotheca_ingest.countries.fr import resolver

    monkeypatch.setattr(resolver, "browser_available", lambda: False)
    monkeypatch.setattr(resolver, "resolve_from_database", lambda url, db: None)
    monkeypatch.setattr(resolver, "http_attempt", lambda url, timeout=20.0: (None, 403))

    assert resolver.resolve_legifrance_url(ELI_URL) is None
    assert route_url(ELI_URL, resolve_legifrance=resolver.resolve_legifrance_url).hint == ELI_HINT
