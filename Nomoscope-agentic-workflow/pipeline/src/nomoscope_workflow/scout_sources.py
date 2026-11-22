"""Static per-country tables for the gap-fill scout.

Which official domains a member state publishes on, the id shapes its
archive-first ingester can fetch, the hints the discovery prompt gives the
model, and the publishers of administrative guidance whose document URLs the
scout may ingest (ADR 0001). Data only: no web, no database, no subprocess.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class CountrySource:
    """One country's discovery rules (see the table below for each field)."""

    domains: tuple[str, ...]
    id_pattern: re.Pattern
    act_kinds: str
    ingest_suffix: str = ""
    known_key: str | None = None


@dataclass(frozen=True)
class GuidancePublisher:
    """One official publisher of administrative guidance (see GUIDANCE_PUBLISHERS)."""

    name: str
    domain: str
    kind: str
    document: re.Pattern
    title: str


# Per-country discovery rules: the official domains web search is restricted
# to, and the id shapes the archive-first ingester can fetch directly.
#
# The first two are a DELIBERATE COPY of what each ingest adapter declares as
# its `countries.base.UrlSource` — the same domains and the same id regex the
# ingester's URL router uses. Nothing imports them across: the dependency
# between the two packages runs one way only (nomotheca-ingest may import this
# package, as its optional `translate` extra; never the reverse), which is why
# the scout reaches the ingester by subprocess. A copy guarantees nothing on its
# own, so two tests hold it in place — one per suite, because each catches the
# edit made on its own side:
#   Nomoscope-agentic-workflow/pipeline/tests/test_scout.py::test_scout_portal_facts_still_match_the_adapters_that_own_them
#   Nomotheca-RAG/ingest/tests/test_routing.py::test_the_nomoscope_scout_copies_these_portals_without_altering_them
# Change a domain or an id shape here and you must change the adapter too.
#
# Fields:
#   domains      — official domains the web search is restricted to (adapter's)
#   id_pattern   — id shapes harvested from result URLs and from the LLM's
#                  answer (adapter's; it is also what `cli instrument` accepts)
#   act_kinds    — the country's own words for the acts that fix values (prompt)
#   ingest_suffix— appended to a bare id to make it what the ingester should fetch
#   known_key    — instruments.metadata key holding this id, when national_id is
#                  something else (else the known-check misses and we re-ingest)
COUNTRY_SOURCES: dict[str, CountrySource] = {
    "FR": CountrySource(
        domains=("legifrance.gouv.fr",),
        # JORF instruments (lois, décrets, arrêtés), single consolidated
        # code articles (LEGIARTI — where most rates actually live once
        # codified) and collective agreements (KALITEXT/KALIARTI, Légifrance
        # /conv_coll/ URLs — ADR 0006) — deliberately not LEGITEXT or KALICONT:
        # ingesting a whole code or convention by accident is not a gap-fill.
        id_pattern=re.compile(r"\b(?:JORFTEXT|LEGIARTI|KALITEXT|KALIARTI)\d{12}\b"),
        # The social partners, not the State, set the AGIRC-ARRCO, APEC and
        # cadres' prévoyance rates: on the 3 Nov benchmark 14 of 34 FR misses
        # asked for exactly those agreements, and the web search found their
        # /conv_coll/ pages only for the id filter to drop them.
        act_kinds=(
            "loi, décret or arrêté — or, for contributions the social partners set "
            "(retraite complémentaire AGIRC-ARRCO, APEC, prévoyance des cadres), the "
            "accord national interprofessionnel or its avenant"
        ),
    ),
    "ES": CountrySource(
        # boe.es is both the official gazette and the consolidated-legislation
        # service; the same domain serves the human view and the open-data API
        # Nomotheca fetches, so one domain covers discovery and ingestion.
        domains=("boe.es",),
        # The BOE analytical id, as it appears in /buscar/act.php?id=… and
        # /diario_boe/txt.php?id=… URLs. Restricted to the -A- series: that is
        # the "disposiciones generales" series, and the only one the
        # legislacion-consolidada API serves (-B- and -S- are not consolidated).
        # A community's act BOE consolidates but did not publish keeps its
        # regional-gazette id there (BOA-d-2005-90006, BOCM-m-2010-90068): the
        # consolidated regional tax texts, where the income-tax scales live.
        id_pattern=re.compile(r"\b(?:BOE-A|(?:BO[A-Z]{1,3}|DO[A-Z]{1,2})-[a-z])-\d{4}-\d+\b"),
        # The LPGE was prorogued for 2024 and 2025, so recent values arrive via
        # ordinary laws and decree-laws rather than the budget law — the scout
        # must not look only for "Ley de Presupuestos".
        act_kinds="ley, real decreto-ley, real decreto legislativo or real decreto",
        # No ingest_suffix: a bare BOE id is exactly what EsResolver returns and
        # what the API serves in full (metadata + every block + every version).
        # No known_key: instruments.national_id *is* the BOE id.
    ),
    "NL": CountrySource(
        # wetten.overheid.nl is the human-facing portal for the Basiswettenbestand;
        # it rate-limits plain clients, but the scout only harvests BWB ids from
        # the URLs, it never reads the page. The repository host Nomotheca
        # actually fetches from serves no search results, so it is not listed.
        domains=("wetten.overheid.nl",),
        # The BWB regulation id, as it appears both in the plain path
        # (/BWBR0011353/2025-01-01) and in the Juriconnect form
        # (/jci1.3:c:BWBR0011353&artikel=2.10&z=2025-01-01). BWBV… ids are
        # treaties, deliberately excluded.
        id_pattern=re.compile(r"\bBWBR\d{7}\b"),
        # Dutch fiscal values are usually fixed by the annual Belastingplan or by
        # a December bijstellingsregeling in the Staatscourant, not by the
        # substantive act itself.
        act_kinds="wet, algemene maatregel van bestuur or ministeriële regeling",
        # No ingest_suffix: a bare BWB id is exactly what NlResolver returns, and
        # the repository serves it as the act's manifest — the version index
        # listing every dated toestand. No known_key: instruments.national_id
        # *is* the BWB id.
    ),
    "IE": CountrySource(
        # eISB (electronic Irish Statute Book) is the official statute book;
        # the ELI act id in its URLs is exactly what the IE adapter fetches
        # (irishstatutebook.ie/eli/<year>/act/<no>/enacted/en/xml) and what it
        # stores as instruments.national_id (e.g. 1997/act/39 = TCA 1997).
        # oireachtas.ie only serves bill pages and the act index — useful
        # search context, but no harvestable instrument id in its URLs.
        domains=("irishstatutebook.ie",),
        # The eISB ELI id: <year>/act/<number>, or <year>/si/<number> for a
        # statutory instrument (ministerial regulations and orders, where
        # «as may be prescribed» amounts live; ingested as made). Groups are
        # non-capturing on purpose: findall must return the whole id.
        id_pattern=re.compile(r"\b(?:19|20)\d{2}/(?:act/\d{1,3}|si/\d{1,4})\b"),
        # Fiscal values arrive via annual amending acts (never consolidated,
        # never repealed): PIT/USC via the Finance Act, welfare rates and PRSI
        # via the Social Welfare Act(s) of the preceding December.
        act_kinds="Finance Act, Social Welfare Act, other Act of the Oireachtas, or statutory instrument (S.I., for amounts an Act leaves to regulations)",
        # No ingest_suffix: `instrument ie <year>/act/<no>` is the exact CLI
        # form. No known_key: instruments.national_id *is* the ELI act id.
    ),
    "LT": CountrySource(
        # e-seimas is the register's public portal; e-tar.lt serves the same
        # acts. Both put the TAR document id in the /legalAct/ URL path, which
        # is the id the Spinta open-data API (what Nomotheca fetches) keys on.
        domains=("e-seimas.lrs.lt", "e-tar.lt"),
        # Two id generations coexist in TAR: "TAR." + 12 uppercase hex for acts
        # migrated into the register in 2014, and a 32-lowercase-hex
        # registration id for everything since.
        id_pattern=re.compile(r"\b(?:TAR\.[0-9A-F]{12}|[0-9a-f]{32})\b"),
        act_kinds="įstatymas, Vyriausybės nutarimas or ministro įsakymas",
        # A bare id fetches the act as published; its value history lives in the
        # dated consolidations listed by the /asr index — the same reference
        # LtResolver returns for a citation. Ingest the index, not the original.
        ingest_suffix="/asr",
        # LT instruments are keyed by official number (IX-1007); the TAR id the
        # scout harvests is kept in instruments.metadata.
        known_key="dokumento_id",
    ),
}

ID_HINTS = {
    "ES": (
        "for Spain the BOE-A-YYYY-NNNNN identifier shown in boe.es "
        "/buscar/act.php?id=<id> and /diario_boe/txt.php?id=<id> URLs, or for an "
        "autonomous community's consolidated act the regional-gazette id of that "
        "same URL (BOA-d-2005-90006, BOCM-m-2010-90068) "
        "(note the ELI URL, boe.es/eli/es/l/2006/11/28/35, does NOT contain it)"
    ),
    "FR": (
        "for France the JORFTEXT############ id shown in Légifrance JORF URLs, "
        "the LEGIARTI############ id of the consolidated code article, or for a "
        "collective agreement the KALITEXT############ (agreement) or "
        "KALIARTI############ (article) id of its Légifrance /conv_coll/id/ URL"
    ),
    "NL": (
        "for the Netherlands the BWBR####### identifier shown in wetten.overheid.nl "
        "URLs — either /BWBR0011353/<date> or the Juriconnect form jci1.3:c:BWBR0011353"
    ),
    "IE": (
        "for Ireland the eISB ELI act id — the <year>/act/<number> path segment of "
        "irishstatutebook.ie/eli/<year>/act/<number>/… URLs (e.g. 1997/act/39 for the "
        "Taxes Consolidation Act 1997)"
    ),
    "LT": (
        "for Lithuania the TAR document id shown in e-seimas /portal/legalAct/lt/TAD/<id> "
        "URLs — either TAR.############ or a 32-character hexadecimal id"
    ),
}


#: Official publishers of administrative guidance, per country (ADR 0001). Some
#: values are published by an administration, not in any act: the Cnav circular
#: gives the year's ASPA/ASI resource ceilings after the 1 April revaluation, an
#: Unédic circular the unemployment-benefit amounts, BOFiP the tax doctrine.
#: Their documents carry no official id, so they are discovered by URL and enter
#: as contributed documents with the kind fixed HERE, never chosen by the model.
#: Every kind is a guidance kind: a web-discovered document is never granted
#: evidence (Nomotheca-RAG/ingest/tests/test_routing.py checks each kind against
#: the ingester's kinds table).
#:
#: `document` matches the URL of one document — not a listing or a news page —
#: and names what the title and the validity date are read from, so nothing is
#: guessed: no full date in the URL, no ingest.
#:   title — format string over the match's groups
#:   date  — groups dd + (mm | month, in the country's own words) + yyyy
GUIDANCE_PUBLISHERS: dict[str, tuple[GuidancePublisher, ...]] = {
    "FR": (
        GuidancePublisher(
            name="Cnav",
            domain="legislation.lassuranceretraite.fr",
            kind="circulaire",
            # …/Pdf/circulaire_cnav_2025_13_03042025.pdf = Circulaire Cnav 2025/13 du 03/04/2025
            document=re.compile(
                r"https://legislation\.lassuranceretraite\.fr/(?:[\w/]+/)?Pdf/circulaire_cnav_"
                r"(?P<year>\d{4})_(?P<num>\d+)_(?P<dd>\d{2})(?P<mm>\d{2})(?P<yyyy>\d{4})\.pdf",
                re.IGNORECASE,
            ),
            title="Circulaire Cnav {year}/{num} du {dd}/{mm}/{yyyy}",
        ),
        GuidancePublisher(
            name="Unédic",
            domain="unedic.org",
            kind="circulaire",
            # …/PRE-CIRC-Circulaire_n_2025-03_du_1er_avril_2025_uid_….pdf
            document=re.compile(
                r"https://www\.unedic\.org/storage/uploads/[\d/]+/PRE-CIRC-Circulaire_n_"
                r"(?P<year>\d{4})-(?P<num>\d+)_du_(?P<dd>\d{1,2})(?:er)?_(?P<month>[a-zéû]+)_(?P<yyyy>\d{4})"
                r"[\w-]*\.pdf",
                re.IGNORECASE,
            ),
            title="Circulaire Unédic n° {year}-{num} du {dd} {month} {yyyy}",
        ),
        GuidancePublisher(
            name="BOFiP",
            domain="bofip.impots.gouv.fr",
            kind="doctrine",
            # …/bofip/2491-PGP.html/identifiant=BOI-IR-LIQ-20-20-10-20250414: the
            # suffix is the date this version of the commentary was published.
            document=re.compile(
                r"https://bofip\.impots\.gouv\.fr/bofip/\d+-PGP\.html/identifiant="
                r"(?P<boi>BOI-[A-Z0-9-]+?)-(?P<yyyy>\d{4})(?P<mm>\d{2})(?P<dd>\d{2})(?![\d-])"
            ),
            title="{boi} du {dd}/{mm}/{yyyy}",
        ),
    ),
}

#: Month names a publisher spells out in its URLs.
_MONTHS = {
    "FR": {
        name: number
        for number, name in enumerate(
            (
                "janvier",
                "fevrier",
                "mars",
                "avril",
                "mai",
                "juin",
                "juillet",
                "aout",
                "septembre",
                "octobre",
                "novembre",
                "decembre",
            ),
            start=1,
        )
    },
}


@dataclass(frozen=True)
class GuidanceDocument:
    """A publisher's document found by URL, with what the URL itself states."""

    url: str
    publisher: str
    kind: str
    title: str
    valid_from: date


def guidance_document(country: str, url: str) -> GuidanceDocument | None:
    """The publisher document a result URL is, or None (a listing, a news page…)."""
    for publisher in GUIDANCE_PUBLISHERS.get(country, ()):
        match = publisher.document.match(url)
        if not match:
            continue
        groups = match.groupdict()
        if groups.get("mm"):
            month = int(groups["mm"])
        else:
            plain = groups["month"].lower().translate(str.maketrans("éû", "eu"))
            month = _MONTHS.get(country, {}).get(plain)
            if month is None:
                return None
        try:
            valid_from = date(int(groups["yyyy"]), month, int(groups["dd"]))
        except ValueError:
            return None
        return GuidanceDocument(
            url=canonical_url(url),
            publisher=publisher.name,
            kind=publisher.kind,
            title=publisher.title.format(**groups),
            valid_from=valid_from,
        )
    return None


def canonical_url(url: str) -> str:
    """The contributed document's national_id for a URL.

    A copy of `nomotheca_ingest.core.contributed.canonical_url` (the packages do
    not import each other): lowercased scheme and host, no fragment, no trailing
    slash — what the "already held" check must compare against.
    """
    from urllib.parse import urlsplit, urlunsplit

    parts = urlsplit(url.strip())
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))
