"""Tests for URL routing and Legifrance ELI resolution."""

from __future__ import annotations

import ast
import re
from dataclasses import replace
from pathlib import Path

import pytest

from nomotheca_ingest.countries.base import UrlSource
from nomotheca_ingest.countries.fr.adapter import ELI_HINT, FR_URL_SOURCE, WHOLE_CODE_HINT
from nomotheca_ingest.countries.fr.resolver import (
    EliResolution,
    resolve_legifrance_url,
)
from nomotheca_ingest.countries.registry import url_sources
from nomotheca_ingest.core.routing import route_url

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
    sources = {
        "FR": replace(FR_URL_SOURCE, resolve=lambda url, database_url: resolution)
    }

    outcome = route_url(ELI_URL, sources=sources)

    assert outcome.kind == "adapter"
    assert outcome.jurisdiction == "FR"
    assert outcome.national_id == "JORFTEXT000042753489"
    assert outcome.resolved_by == "browser"


def test_the_router_knows_no_country_of_its_own() -> None:
    """Every portal fact comes from an adapter, so a sixth member state is an
    adapter and not an edit to `core/routing.py` (12_ingestion-architecture §7).
    """
    import inspect

    from nomotheca_ingest.core import routing

    source = inspect.getsource(routing)
    for code in url_sources():
        assert f'"{code}"' not in source, f"{code} is named in core/routing.py"


def test_a_portal_declared_by_an_adapter_is_all_the_router_needs() -> None:
    """A made-up member state routes without the router learning about it."""
    sources = {
        "XX": UrlSource(
            name="Gazette of Xanadu",
            domains=("gazette.xx",),
            id_pattern=re.compile(r"\bXX-\d{4}-\d+\b"),
        )
    }

    outcome = route_url("https://gazette.xx/acts/XX-2025-17", sources=sources)

    assert (outcome.kind, outcome.jurisdiction, outcome.national_id) == (
        "adapter",
        "XX",
        "XX-2025-17",
    )


def _scout_module() -> Path | None:
    """Locate the Nomoscope scout's source file, if that package is checked out."""
    for ancestor in Path(__file__).resolve().parents:
        candidate = (
            ancestor
            / "Nomoscope-agentic-workflow"
            / "pipeline"
            / "src"
            / "nomoscope_workflow"
            / "scout.py"
        )
        if candidate.is_file():
            return candidate
    return None


def _scout_portals(scout: Path) -> dict[str, tuple[tuple[str, ...], str]]:
    """`scout.COUNTRY_SOURCES`, reduced to the two facts the adapters also state.

    Read out of the syntax tree, not imported: `nomoscope_workflow` is only
    installed here under the optional `translate` extra, and a check that runs
    solely in an environment nobody syncs by default is no check at all.
    """
    tree = ast.parse(scout.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        target = getattr(node, "target", None)
        if getattr(target, "id", "") == "COUNTRY_SOURCES":
            table = node.value
            break
    else:
        raise AssertionError(f"{scout} declares no COUNTRY_SOURCES")
    portals = {}
    for country, rules in zip(table.keys, table.values):
        by_key = {key.value: value for key, value in zip(rules.keys, rules.values)}
        portals[country.value] = (
            tuple(ast.literal_eval(by_key["domains"])),
            # Always `re.compile(r"...")`; compare the pattern text.
            by_key["id_pattern"].args[0].value,
        )
    return portals


def test_the_nomoscope_scout_copies_these_portals_without_altering_them() -> None:
    """The gap-fill scout keeps its own copy of `domains` and `id_pattern`.

    It has to: the dependency between the two packages runs one way only —
    `nomotheca-ingest` may import `nomoscope-agentic-workflow` (the optional
    `translate` extra), never the reverse — and the workflow reaches this
    package by subprocess to keep it that way. So the scout restricts its web
    search and harvests instrument ids from result URLs using a hand-kept copy
    of what the adapters declare here, and drift breaks it in the worst way: it
    would harvest ids this package then refuses to fetch.

    The adapter is the original — it is what actually fetches the act — so this
    is the direction that matters when an adapter changes. The mirror image
    lives in the workflow's own suite, which is what catches an edit made to
    the scout; neither suite can see both files' edits on its own.
    """
    scout = _scout_module()
    if scout is None:
        pytest.skip("no Nomoscope-agentic-workflow checkout next to this package")

    portals = _scout_portals(scout)
    declared = url_sources()
    for country, (domains, id_pattern) in portals.items():
        assert country in declared, f"the scout hunts {country} ids that no adapter can fetch"
        # A country here but not in the scout is fine and deliberate: it simply
        # never gap-fills (`no scout source rules for <CC>`), which is a missing
        # feature, not a contradiction.
        assert declared[country].domains == domains, f"{country}: scout domains differ from {scout}"
        assert declared[country].id_pattern.pattern == id_pattern, (
            f"{country}: scout id_pattern differs from {scout}"
        )


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
    assert route_url(ELI_URL).hint == ELI_HINT
