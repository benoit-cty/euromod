"""Gap-fill scout: discover and ingest missing sources when retrieval fails.

When retrieval returns nothing usable (no hits, or the proposer answers
found=false), the corpus is usually missing the instrument that sets the
value — e.g. the French PSS is fixed by an annual arrêté that no loi de
finances contains. The scout closes the gap without weakening the
anti-hallucination contract: the LLM and the web search only DISCOVER what
to ingest (official instrument ids); the text itself always enters through
Nomotheca's archive-first ingest (fetch → snapshot → parse → chunk), and
the verbatim-quote rule keeps verifying against the database. Web text is
never evidence.

Modes (WORKFLOW_SCOUT): off — disabled; llm — the model names instrument
ids it is certain of; tavily — additionally web-search official domains and
harvest ids from the result URLs (the reliable path for post-training-cutoff
years).
"""

from __future__ import annotations

import os
import re
import subprocess
import time
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from . import llm, regions, retrieval
from .config import WorkflowConfig
from .query_encoder import embedding_process, ingest_dir, nomos_python
from .schema import ParameterRecord, RetrievalHit
from .tracing import progress

INGEST_TIMEOUT = 600  # a single arrêté is seconds; a loi de finances, minutes
# The embedding pass covers the whole backlog of unembedded chunks, not just the
# scouted instrument (the CLI has no per-instrument scope), and BGE-M3 on CPU
# runs at roughly one chunk per second — a freshly ingested loi de finances
# alone is ~10 minutes (roughly 20x faster when the .venv-cuda GPU environment
# is installed). The build commits per batch, so even a timeout here keeps the
# vectors computed so far; the retry then resumes where it stopped.
EMBED_TIMEOUT = int(os.environ.get("WORKFLOW_SCOUT_EMBED_TIMEOUT", "1800"))

#: Set once the web-search provider has refused for good in this process —
#: Tavily answers HTTP 432 when the plan's usage limit is spent. Both eval runs
#: of 2026-09-09 (212 cases) hit it on every single query and the only trace
#: was a per-item error string: the scout ran blind for a whole evaluation and
#: nobody saw. Remember it, say it once, and stop paying a round trip per query.
_web_search_unavailable: str | None = None

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
#   tests/test_workflow.py::test_scout_portal_facts_still_match_the_adapters_that_own_them
#   Nomotheca-RAG/ingest/tests/test_routing.py::test_the_nomoscope_scout_copies_these_portals_without_altering_them
# Change a domain or an id shape here and you must change the adapter too.
#
# Keys:
#   domains      — official domains the web search is restricted to (adapter's)
#   id_pattern   — id shapes harvested from result URLs and from the LLM's
#                  answer (adapter's; it is also what `cli instrument` accepts)
#   act_kinds    — the country's own words for the acts that fix values (prompt)
#   ingest_suffix— appended to a bare id to make it what the ingester should fetch
#   known_key    — instruments.metadata key holding this id, when national_id is
#                  something else (else the known-check misses and we re-ingest)
COUNTRY_SOURCES: dict[str, dict] = {
    "FR": {
        "domains": ["legifrance.gouv.fr"],
        # JORF instruments (lois, décrets, arrêtés), single consolidated
        # code articles (LEGIARTI — where most rates actually live once
        # codified) and collective agreements (KALITEXT/KALIARTI, Légifrance
        # /conv_coll/ URLs — ADR 0006) — deliberately not LEGITEXT or KALICONT:
        # ingesting a whole code or convention by accident is not a gap-fill.
        "id_pattern": re.compile(r"\b(?:JORFTEXT|LEGIARTI|KALITEXT|KALIARTI)\d{12}\b"),
        # The social partners, not the State, set the AGIRC-ARRCO, APEC and
        # cadres' prévoyance rates: on the 3 Nov benchmark 14 of 34 FR misses
        # asked for exactly those agreements, and the web search found their
        # /conv_coll/ pages only for the id filter to drop them.
        "act_kinds": (
            "loi, décret or arrêté — or, for contributions the social partners set "
            "(retraite complémentaire AGIRC-ARRCO, APEC, prévoyance des cadres), the "
            "accord national interprofessionnel or its avenant"
        ),
    },
    "ES": {
        # boe.es is both the official gazette and the consolidated-legislation
        # service; the same domain serves the human view and the open-data API
        # Nomotheca fetches, so one domain covers discovery and ingestion.
        "domains": ["boe.es"],
        # The BOE analytical id, as it appears in /buscar/act.php?id=… and
        # /diario_boe/txt.php?id=… URLs. Restricted to the -A- series: that is
        # the "disposiciones generales" series, and the only one the
        # legislacion-consolidada API serves (-B- and -S- are not consolidated).
        "id_pattern": re.compile(r"\bBOE-A-\d{4}-\d+\b"),
        # The LPGE was prorogued for 2024 and 2025, so recent values arrive via
        # ordinary laws and decree-laws rather than the budget law — the scout
        # must not look only for "Ley de Presupuestos".
        "act_kinds": "ley, real decreto-ley, real decreto legislativo or real decreto",
        # No ingest_suffix: a bare BOE id is exactly what EsResolver returns and
        # what the API serves in full (metadata + every block + every version).
        # No known_key: instruments.national_id *is* the BOE id.
    },
    "NL": {
        # wetten.overheid.nl is the human-facing portal for the Basiswettenbestand;
        # it rate-limits plain clients, but the scout only harvests BWB ids from
        # the URLs, it never reads the page. The repository host Nomotheca
        # actually fetches from serves no search results, so it is not listed.
        "domains": ["wetten.overheid.nl"],
        # The BWB regulation id, as it appears both in the plain path
        # (/BWBR0011353/2025-01-01) and in the Juriconnect form
        # (/jci1.3:c:BWBR0011353&artikel=2.10&z=2025-01-01). BWBV… ids are
        # treaties, deliberately excluded.
        "id_pattern": re.compile(r"\bBWBR\d{7}\b"),
        # Dutch fiscal values are usually fixed by the annual Belastingplan or by
        # a December bijstellingsregeling in the Staatscourant, not by the
        # substantive act itself.
        "act_kinds": "wet, algemene maatregel van bestuur or ministeriële regeling",
        # No ingest_suffix: a bare BWB id is exactly what NlResolver returns, and
        # the repository serves it as the act's manifest — the version index
        # listing every dated toestand. No known_key: instruments.national_id
        # *is* the BWB id.
    },
    "IE": {
        # eISB (electronic Irish Statute Book) is the official statute book;
        # the ELI act id in its URLs is exactly what the IE adapter fetches
        # (irishstatutebook.ie/eli/<year>/act/<no>/enacted/en/xml) and what it
        # stores as instruments.national_id (e.g. 1997/act/39 = TCA 1997).
        # oireachtas.ie only serves bill pages and the act index — useful
        # search context, but no harvestable instrument id in its URLs.
        "domains": ["irishstatutebook.ie"],
        # The eISB ELI act id: the <year>/act/<number> path segment. Acts of
        # the Oireachtas only — the IE fetcher builds act URLs; statutory
        # instruments (/eli/<year>/si/<no>) are not ingestible yet. Group is
        # non-capturing on purpose: findall must return the whole id.
        "id_pattern": re.compile(r"\b(?:19|20)\d{2}/act/\d{1,3}\b"),
        # Fiscal values arrive via annual amending acts (never consolidated,
        # never repealed): PIT/USC via the Finance Act, welfare rates and PRSI
        # via the Social Welfare Act(s) of the preceding December.
        "act_kinds": "Finance Act, Social Welfare Act or other Act of the Oireachtas",
        # No ingest_suffix: `instrument ie <year>/act/<no>` is the exact CLI
        # form. No known_key: instruments.national_id *is* the ELI act id.
    },
    "LT": {
        # e-seimas is the register's public portal; e-tar.lt serves the same
        # acts. Both put the TAR document id in the /legalAct/ URL path, which
        # is the id the Spinta open-data API (what Nomotheca fetches) keys on.
        "domains": ["e-seimas.lrs.lt", "e-tar.lt"],
        # Two id generations coexist in TAR: "TAR." + 12 uppercase hex for acts
        # migrated into the register in 2014, and a 32-lowercase-hex
        # registration id for everything since.
        "id_pattern": re.compile(r"\b(?:TAR\.[0-9A-F]{12}|[0-9a-f]{32})\b"),
        "act_kinds": "įstatymas, Vyriausybės nutarimas or ministro įsakymas",
        # A bare id fetches the act as published; its value history lives in the
        # dated consolidations listed by the /asr index — the same reference
        # LtResolver returns for a citation. Ingest the index, not the original.
        "ingest_suffix": "/asr",
        # LT instruments are keyed by official number (IX-1007); the TAR id the
        # scout harvests is kept in instruments.metadata.
        "known_key": "dokumento_id",
    },
}

SCOUT_SYSTEM = """You are a legal-sources librarian for {country} tax-benefit legislation
(collective agreements included: where the social partners set a rate, the agreement IS
the legal text).
A retrieval system searched a legislation database and could not find the legal text that
sets the value of a policy parameter. Identify the official publication(s) that fix this
parameter's value (the specific {act_kinds} or equivalent — many values are set by
annual implementing acts rather than by the statutes that define them).

You may be given what the analyst who read the retrieved extracts said it was missing, and
the citations retrieval already returned. Both matter:
- The analyst's account is the strongest signal you have. It usually names the missing act
  in the law's own words, or names the article a retrieved text cross-refers to. Hunt what
  it asks for, not what the parameter label alone suggests.
- The retrieved citations are context, NOT a list of what the database holds: retrieval
  returns what it ranked highest, which is often a similarly-named or similarly-numbered
  act rather than the one asked for. Never conclude from them that a document is already
  present, and never skip searching on that basis — whether an id is already held is
  checked against the database afterwards, and duplicates are dropped automatically.
  Use them only to avoid spending your instrument_ids on an act plainly already there.
- ALWAYS return search_queries when you have been told something is missing. An empty
  answer ends the hunt for this parameter.

Return:
- search_queries: 1-3 short web-search queries in the law's language, phrased to find the
  act on the official legal portal (results are restricted to official domains).
- instrument_ids: official database identifiers of the act, ONLY if you are certain of the
  exact identifier ({id_hint}). NEVER guess or reconstruct an identifier.
- reasoning: one sentence on what kind of act sets this value."""

ID_HINTS = {
    "ES": (
        "for Spain the BOE-A-YYYY-NNNNN identifier shown in boe.es "
        "/buscar/act.php?id=<id> and /diario_boe/txt.php?id=<id> URLs "
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
GUIDANCE_PUBLISHERS: dict[str, list[dict]] = {
    "FR": [
        {
            "name": "Cnav",
            "domain": "legislation.lassuranceretraite.fr",
            "kind": "circulaire",
            # …/Pdf/circulaire_cnav_2025_13_03042025.pdf = Circulaire Cnav 2025/13 du 03/04/2025
            "document": re.compile(
                r"https://legislation\.lassuranceretraite\.fr/(?:[\w/]+/)?Pdf/circulaire_cnav_"
                r"(?P<year>\d{4})_(?P<num>\d+)_(?P<dd>\d{2})(?P<mm>\d{2})(?P<yyyy>\d{4})\.pdf",
                re.IGNORECASE,
            ),
            "title": "Circulaire Cnav {year}/{num} du {dd}/{mm}/{yyyy}",
        },
        {
            "name": "Unédic",
            "domain": "unedic.org",
            "kind": "circulaire",
            # …/PRE-CIRC-Circulaire_n_2025-03_du_1er_avril_2025_uid_….pdf
            "document": re.compile(
                r"https://www\.unedic\.org/storage/uploads/[\d/]+/PRE-CIRC-Circulaire_n_"
                r"(?P<year>\d{4})-(?P<num>\d+)_du_(?P<dd>\d{1,2})(?:er)?_(?P<month>[a-zéû]+)_(?P<yyyy>\d{4})"
                r"[\w-]*\.pdf",
                re.IGNORECASE,
            ),
            "title": "Circulaire Unédic n° {year}-{num} du {dd} {month} {yyyy}",
        },
        {
            "name": "BOFiP",
            "domain": "bofip.impots.gouv.fr",
            "kind": "doctrine",
            # …/bofip/2491-PGP.html/identifiant=BOI-IR-LIQ-20-20-10-20250414: the
            # suffix is the date this version of the commentary was published.
            "document": re.compile(
                r"https://bofip\.impots\.gouv\.fr/bofip/\d+-PGP\.html/identifiant="
                r"(?P<boi>BOI-[A-Z0-9-]+?)-(?P<yyyy>\d{4})(?P<mm>\d{2})(?P<dd>\d{2})(?![\d-])"
            ),
            "title": "{boi} du {dd}/{mm}/{yyyy}",
        },
    ],
}

#: Month names a publisher spells out in its URLs.
_MONTHS = {
    "FR": {
        name: number
        for number, name in enumerate(
            ("janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet",
             "aout", "septembre", "octobre", "novembre", "decembre"),
            start=1,
        )
    },
}

#: At most this many guidance documents ingested per round (each is one PDF).
GUIDANCE_MAX_INGEST = 2


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
    for publisher in GUIDANCE_PUBLISHERS.get(country, []):
        match = publisher["document"].match(url)
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
            publisher=publisher["name"],
            kind=publisher["kind"],
            title=publisher["title"].format(**groups),
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


def _publisher_listing(country: str) -> str:
    """The publishers, for the scout prompt."""
    publishers = GUIDANCE_PUBLISHERS.get(country)
    if not publishers:
        return ""
    names = ", ".join(f"{p['name']} ({p['kind']}, {p['domain']})" for p in publishers)
    return (
        "\n\nSome values are published by an administration rather than in an act — for "
        f"{country}: {names}. A resource ceiling or benefit amount revalued every year is often "
        "stated only in such a circular. When that may be the case, ALSO return "
        "guidance_queries: 1-2 short web-search queries for that document, in the "
        "administration's own words (e.g. «circulaire Cnav 2025 plafonds ASPA ASI "
        "revalorisation»). Plain words only — no site: operators."
    )


class ScoutSuggestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    search_queries: list[str] = Field(default_factory=list)
    instrument_ids: list[str] = Field(default_factory=list)
    #: Searched on the country's GUIDANCE_PUBLISHERS domains only.
    guidance_queries: list[str] = Field(default_factory=list)
    reasoning: str | None = None


SELECT_SYSTEM = """You match web-search results to the official act that sets a policy parameter.
From the candidate instruments below, return the ids of the act(s) that fix THIS parameter's
value, best match first. Be strict about similarly-named quantities: e.g. a means-test
resource ceiling ("plafond de ressources") is NOT the social-security contribution ceiling
("plafond de la sécurité sociale"). Return ONLY ids from the candidate list; return an empty
list if none of them plausibly sets this parameter."""


class ScoutSelection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    instrument_ids: list[str] = Field(default_factory=list)


@dataclass
class ScoutResult:
    mode: str
    queries: list[str] = field(default_factory=list)
    urls: list[str] = field(default_factory=list)
    candidate_ids: list[str] = field(default_factory=list)
    ingested: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    reasoning: str | None = None
    #: Citations of sources the analyst named that turned out to be already in
    #: the corpus — looked up directly and handed to the retry (see `locate`).
    located: list[str] = field(default_factory=list)
    #: 1-based gap-fill round this result came from.
    round: int = 1
    #: What the analyst said it was missing, verbatim — the input that drove
    #: this round. Kept so a reviewer can see WHY these acts were fetched.
    needs: list[str] = field(default_factory=list)

    def summary(self) -> dict:
        return {
            "mode": self.mode,
            "round": self.round,
            "needs": self.needs,
            "queries": self.queries,
            "urls": self.urls,
            "candidate_ids": self.candidate_ids,
            "ingested": self.ingested,
            "located": self.located,
            "errors": self.errors,
            "reasoning": self.reasoning,
        }


def merge_results(results: list["ScoutResult"]) -> "ScoutResult":
    """Fold every gap-fill round of one run into the single ScoutResult the
    ReviewItem carries, keeping each round's fields in order."""
    if not results:
        return ScoutResult(mode="off")
    merged = ScoutResult(mode=results[0].mode, round=len(results))
    for r in results:
        merged.needs += [n for n in r.needs if n not in merged.needs]
        merged.queries += [q for q in r.queries if q not in merged.queries]
        merged.urls += [u for u in r.urls if u not in merged.urls]
        merged.candidate_ids += [c for c in r.candidate_ids if c not in merged.candidate_ids]
        merged.ingested += [i for i in r.ingested if i not in merged.ingested]
        merged.located += [c for c in r.located if c not in merged.located]
        merged.errors += r.errors
    merged.reasoning = " | ".join(r.reasoning for r in results if r.reasoning) or None
    return merged


def _tavily_search(api_key: str, query: str, domains: list[str]) -> list[dict]:
    import httpx  # dependency of pydantic-ai

    response = httpx.post(
        "https://api.tavily.com/search",
        json={
            "api_key": api_key,
            "query": query,
            "include_domains": domains,
            "max_results": 5,
        },
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json().get("results", [])


def _known_instruments(cfg: WorkflowConfig, ids: list[str], rules: dict) -> set[str]:
    """Ids already in the legislation DB — re-ingesting them cannot add chunks.

    Article-level ids (FR LEGIARTI…/JORFARTI…) are stored as legal_units under
    their parent code instrument, not as instruments — check both tables, or
    every re-run re-ingests the same article forever. Where the scouted id is
    not the stored national_id at all (LT keys instruments by official number
    and files the TAR id under metadata.dokumento_id), `known_key` says which
    metadata key to match instead.
    """
    import psycopg

    sql = (
        "SELECT national_id FROM instruments WHERE national_id = ANY(%(ids)s) "
        "UNION SELECT national_id FROM legal_units WHERE national_id = ANY(%(ids)s)"
    )
    if rules.get("known_key"):
        sql += (
            " UNION SELECT metadata->>%(key)s FROM instruments "
            "WHERE metadata->>%(key)s = ANY(%(ids)s)"
        )
    try:
        with psycopg.connect(cfg.database_url) as conn:
            rows = conn.execute(sql, {"ids": ids, "key": rules.get("known_key")}).fetchall()
        return {row[0] for row in rows}
    except Exception:
        return set()


def _proc_failure(what: str, proc: subprocess.CompletedProcess) -> str:
    """Failure text with exit code and the tail of BOTH streams.

    stderr alone is not enough: the benign BGE-M3 tokenizer warning always
    lands there and would mask the real error when it went to stdout, and a
    negative returncode (killed by a signal, e.g. memory pressure) leaves no
    traceback at all — the exit code is then the only evidence.
    """
    parts = []
    for stream, text in (("stderr", proc.stderr), ("stdout", proc.stdout)):
        lines = (text or "").strip().splitlines()
        if lines:
            parts.append(f"{stream}: {' | '.join(lines[-4:])}")
    detail = "; ".join(parts) or "no output"
    signal_hint = " — killed by a signal, likely memory pressure" if proc.returncode < 0 else ""
    return f"{what} failed (exit {proc.returncode}{signal_hint}): {detail}"


def _ingest_instrument(cfg: WorkflowConfig, country: str, instrument_id: str) -> str | None:
    """Archive-first ingest of one instrument via the Nomotheca CLI; error text on failure.

    Inside the worker (`NOMOS_PYTHON` set) the CLI runs from that interpreter
    in the current directory; otherwise through `uv run` in the ingest package.
    """
    args = ["instrument", country.lower(), instrument_id, "--database-url", cfg.database_url]
    return _run_ingest_cli(cfg, args, instrument_id)


def _run_ingest_cli(cfg: WorkflowConfig, args: list[str], what: str) -> str | None:
    """Run one Nomotheca CLI command; error text on failure."""
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    env["PYTHONUNBUFFERED"] = "1"
    python = nomos_python()
    if python:
        command, cwd = [python, "-m", "nomotheca_ingest.cli", *args], Path.cwd()
    else:
        cwd = ingest_dir()
        if cwd is None:
            return "could not locate Nomotheca-RAG/ingest (set EUROMOD_INGEST_DIR or NOMOS_PYTHON)"
        command = ["uv", "run", "python", "-m", "nomotheca_ingest.cli", *args]
    proc = subprocess.run(
        command, cwd=cwd, env=env, capture_output=True, text=True, timeout=INGEST_TIMEOUT
    )
    if proc.returncode != 0:
        return _proc_failure(f"{what}: ingest", proc)
    return None


def _rank_candidates(
    cfg: WorkflowConfig, info, candidates: list[str], titles: dict[str, str]
) -> list[str]:
    """LLM-select which candidate instruments actually set this parameter.

    Search results routinely include similarly-named acts (resource ceilings
    vs the contribution ceiling); with the ingest cap, arrival order would
    pick the wrong ones. Selected ids first, unselected kept as fallback.
    """
    listing = "\n".join(f"- {i}: {titles.get(i) or '(no title)'}" for i in candidates)
    try:
        selection = llm.run_agent(
            cfg.model,
            SELECT_SYSTEM,
            (
                f"Parameter: {info.model_target}\n"
                f"Label: {(info.short_label or {}).get('en', '')} — {(info.label or {}).get('en', '')}\n"
                f"Description: {(info.description or {}).get('en', '')}\n"
                f"Candidates:\n{listing}"
            ),
            output_type=ScoutSelection,
        )
    except Exception:
        return candidates
    picked = [i for i in selection.instrument_ids if i in candidates]
    return picked + [i for i in candidates if i not in picked]


def _build_embeddings(cfg: WorkflowConfig) -> str | None:
    """Embed chunks that are missing vectors (incremental) so the vector leg
    of the retrieval retry covers what the scout just ingested."""
    directory = ingest_dir()
    if nomos_python():
        # The worker's interpreter, current directory: no local model export to
        # point at, so the CLI falls back to the Hugging Face id and its own
        # device selection.
        model_args: list[str] = []
    elif directory is None:
        return "could not locate Nomotheca-RAG/ingest (set EUROMOD_INGEST_DIR or NOMOS_PYTHON)"
    else:
        model_args = _embedding_model_args(directory, cuda=_cuda_available(directory))
    spec = embedding_process(
        directory,
        "nomotheca_ingest.cli",
        "embeddings",
        "build",
        "--database-url",
        cfg.database_url,
        # Rich's live progress is noise in captured output and can bury the
        # real error; the per-batch commits do not depend on it.
        "--no-progress",
        *model_args,
    )
    proc = subprocess.run(
        spec.command, cwd=spec.cwd, env=spec.env, capture_output=True, text=True, timeout=EMBED_TIMEOUT
    )
    if proc.returncode != 0:
        return _proc_failure("embeddings build", proc)
    return None


def _cuda_available(directory: Path) -> bool:
    """Return whether the ingest package has its GPU environment installed."""
    return embedding_process(directory, "nomotheca_ingest.cli").cuda


def _embedding_model_args(directory: Path, *, cuda: bool) -> list[str]:
    """Pick the local model for the environment we are about to run in.

    The OpenVINO IR only loads under the OpenVINO backend, so on the GPU we ask
    for the Torch export if one was downloaded and otherwise let the CLI fall
    back to the Hugging Face id (device selection is the CLI's own job).
    """
    if cuda:
        torch_model = directory / "models" / "bge-m3"
        if (torch_model / "config.json").is_file():
            return ["--model-path", "models/bge-m3"]
        return []
    if (directory / "models" / "bge-m3-openvino").is_dir():
        return ["--backend", "openvino", "--model-path", "models/bge-m3-openvino"]
    return []


#: Cap on how much of the analyst's account is quoted into the scout prompt.
#: Its reasoning can run long; the useful part — the act it names — is at the front.
_NEED_CHARS = 400


def _evidence_block(needs: list[str], known_citations: list[str] | None) -> str:
    """Render the failure evidence for the scout prompt.

    Both halves earn their tokens: the needs tell it what to hunt, and the
    citations already held stop it spending its ingest budget re-fetching them
    (a second round would otherwise propose the same acts as the first).
    """
    parts = []
    if needs:
        listing = "\n".join(f"- {need[:_NEED_CHARS]}" for need in needs[:5])
        parts.append(
            "\n\nThe analyst who read the retrieved extracts reported these missing "
            f"source(s):\n{listing}"
        )
    if known_citations:
        held = ", ".join(dict.fromkeys(known_citations))[:800]
        parts.append(f"\n\nAlready in the database (do NOT hunt these): {held}")
    return "".join(parts)


def run(
    cfg: WorkflowConfig,
    record: ParameterRecord,
    as_of: date,
    needs: list[str] | None = None,
    known_citations: list[str] | None = None,
    attempted: set[str] | None = None,
    round_index: int = 1,
) -> ScoutResult:
    """Discover candidate instruments for a parameter and ingest the new ones.

    `needs` is what the proposal step said it was missing (its `missing_sources`,
    falling back to its prose reasoning) — the sharpest available description of
    the gap, since the analyst has just read the retrieved text and named the act
    it cross-refers to. `known_citations` are the citations retrieval already
    returns, so the scout skips hunting what we hold. `attempted` accumulates ids
    tried earlier in this run, so a second round never re-fetches a candidate
    that already failed or was already ingested.
    """
    info = record.information
    result = ScoutResult(mode=cfg.scout, round=round_index, needs=list(needs or []))
    rules = COUNTRY_SOURCES.get(info.country)
    if rules is None:
        result.errors.append(f"no scout source rules for {info.country}")
        return result

    try:
        suggestion = llm.run_agent(
            cfg.model,
            SCOUT_SYSTEM.format(
                country=info.country,
                id_hint=ID_HINTS.get(info.country, "exact official id"),
                act_kinds=rules.get("act_kinds", "act, decree or order"),
            )
            + _publisher_listing(info.country),
            (
                f"Parameter: {info.model_target}\n"
                f"Label: {(info.short_label or {}).get('en', '')} — {(info.label or {}).get('en', '')}\n"
                f"Description: {(info.description or {}).get('en', '')}\n"
                f"Reference date: {as_of.isoformat()} (find the act setting the value in force then)"
                + _evidence_block(result.needs, known_citations)
            ),
            output_type=ScoutSuggestion,
        )
    except Exception as exc:
        result.errors.append(f"scout LLM failed: {exc}")
        return result
    result.reasoning = suggestion.reasoning
    result.queries = suggestion.search_queries[:3]
    if not result.queries and not suggestion.instrument_ids and result.needs:
        # The model answered with nothing at all — usually because it talked
        # itself out of the hunt ("that act looks like one of the retrieved
        # citations"). The needs are already phrased in the law's own language,
        # which is exactly what an official-domain search wants, so fall back to
        # searching for them verbatim rather than losing the round.
        result.queries = [need[:_NEED_CHARS] for need in result.needs[:2]]
        result.errors.append("scout proposed nothing; searching the stated needs verbatim")

    pattern: re.Pattern = rules["id_pattern"]
    ids = [m for text in suggestion.instrument_ids for m in pattern.findall(text)]
    titles: dict[str, str] = {}  # instrument id -> best search-result title
    global _web_search_unavailable
    if cfg.scout == "tavily" and cfg.tavily_api_key and _web_search_unavailable:
        result.errors.append(_web_search_unavailable)
    elif cfg.scout == "tavily" and cfg.tavily_api_key:
        for query in result.queries:
            try:
                for hit in _tavily_search(cfg.tavily_api_key, query, rules["domains"]):
                    url = hit.get("url", "")
                    result.urls.append(url)
                    for found in pattern.findall(url):
                        ids.append(found)
                        titles.setdefault(found, hit.get("title", ""))
            except Exception as exc:
                result.errors.append(f"tavily search failed: {exc}")
                if "432" in str(exc):
                    _web_search_unavailable = (
                        "web search unavailable: the Tavily plan's usage limit is exhausted "
                        "(HTTP 432) — discovery runs on the model's own instrument ids and "
                        "the corpus lookup only until the quota resets or TAVILY_API_KEY changes"
                    )
                    progress(f"  [scout] ✗ {_web_search_unavailable}")
                    break

    documents = _search_guidance(cfg, info.country, suggestion, result)

    result.candidate_ids = list(dict.fromkeys(ids))
    if len(result.candidate_ids) > 1 and titles:
        result.candidate_ids = _rank_candidates(cfg, info, result.candidate_ids, titles)
    known = _known_instruments(cfg, result.candidate_ids, rules) | set(attempted or ())
    to_ingest = [i for i in result.candidate_ids if i not in known][: cfg.scout_max_ingest]
    if result.candidate_ids:
        progress(
            f"  [scout] {len(result.candidate_ids)} candidate instrument(s), "
            f"{len(known)} already in DB, {len(to_ingest)} to ingest"
        )
    suffix = rules.get("ingest_suffix", "")
    for instrument_id in to_ingest:
        progress(
            f"  [scout] ingesting {instrument_id}{suffix} "
            f"(archive-first: fetch → snapshot → parse → chunk; up to {INGEST_TIMEOUT}s)…"
        )
        started = time.monotonic()
        try:
            error = _ingest_instrument(cfg, info.country, instrument_id + suffix)
        except subprocess.TimeoutExpired:
            error = f"{instrument_id}: ingest timed out after {INGEST_TIMEOUT}s"
        if error is None:
            result.ingested.append(instrument_id)
            progress(f"  [scout] ✓ {instrument_id} ingested ({time.monotonic() - started:.0f}s)")
        else:
            result.errors.append(error)
            progress(f"  [scout] ✗ {error}")
    _ingest_guidance(cfg, info.country, documents, result, set(attempted or ()))
    if not result.candidate_ids and not result.errors:
        progress("  [scout] no candidate instrument found for the stated needs")
    if result.ingested and cfg.embedding_model_id != 99:
        progress(
            "  [scout] embedding new chunks with BGE-M3 "
            f"(~1 chunk/s on CPU — expect high CPU, up to {EMBED_TIMEOUT}s)…"
        )
        started = time.monotonic()
        try:
            error = _build_embeddings(cfg)
        except subprocess.TimeoutExpired:
            error = f"embeddings build timed out after {EMBED_TIMEOUT}s (partial vectors kept)"
        if error:
            result.errors.append(error)  # FTS still covers the new chunks
            progress(f"  [scout] ✗ {error}")
        else:
            progress(f"  [scout] ✓ embeddings up to date ({time.monotonic() - started:.0f}s)")
    return result


#: Words in the analyst's needs that point at a publisher's document rather than an act.
_GUIDANCE_HINT = re.compile(r"(?i)circulaire|instruction|doctrine|BOFiP|BOI-|Cnav|Unédic|Unedic")


def _search_guidance(
    cfg: WorkflowConfig, country: str, suggestion: ScoutSuggestion, result: ScoutResult
) -> list[GuidanceDocument]:
    """Web-search the country's guidance publishers; their document URLs, in rank order.

    Queries are the model's guidance_queries or, when it gave none but the
    analyst's needs name a circular or doctrine, those needs verbatim. Results
    are kept only when the URL is one document of a listed publisher.
    """
    publishers = GUIDANCE_PUBLISHERS.get(country)
    if not publishers or cfg.scout != "tavily" or not cfg.tavily_api_key or _web_search_unavailable:
        return []
    queries = [q for q in suggestion.guidance_queries if q.strip()][:2]
    if not queries:
        queries = [n[:_NEED_CHARS] for n in result.needs if _GUIDANCE_HINT.search(n)][:1]
    documents: dict[str, GuidanceDocument] = {}
    domains = [p["domain"] for p in publishers]
    for query in queries:
        result.queries.append(query)
        try:
            hits = _tavily_search(cfg.tavily_api_key, query, domains)
        except Exception as exc:
            result.errors.append(f"tavily guidance search failed: {exc}")
            continue
        for hit in hits:
            url = hit.get("url", "")
            result.urls.append(url)
            document = guidance_document(country, url)
            if document is not None:
                documents.setdefault(document.url, document)
    return list(documents.values())


def _ingest_guidance(
    cfg: WorkflowConfig,
    country: str,
    documents: list[GuidanceDocument],
    result: ScoutResult,
    attempted: set[str],
) -> None:
    """Ingest the new guidance documents as contributed documents of their publisher's kind."""
    if not documents:
        return
    urls = [d.url for d in documents]
    result.candidate_ids += [u for u in urls if u not in result.candidate_ids]
    known = _known_instruments(cfg, urls, {}) | attempted
    fresh = [d for d in documents if d.url not in known][:GUIDANCE_MAX_INGEST]
    progress(
        f"  [scout] {len(documents)} guidance document(s) "
        f"({', '.join(sorted({d.publisher for d in documents}))}), "
        f"{len(documents) - len([d for d in documents if d.url not in known])} already in DB, "
        f"{len(fresh)} to ingest"
    )
    for document in fresh:
        progress(f"  [scout] ingesting {document.title} as {document.kind} (guidance)…")
        args = [
            "document", document.url,
            "--database-url", cfg.database_url,
            "--jurisdiction", country,
            "--lang", retrieval.LANG_BY_COUNTRY.get(country, "en"),
            "--title", document.title,
            "--kind", document.kind,
            "--valid-from", document.valid_from.isoformat(),
            "--trigger", "cache_miss",
        ]
        try:
            error = _run_ingest_cli(cfg, args, document.title)
        except subprocess.TimeoutExpired:
            error = f"{document.title}: ingest timed out after {INGEST_TIMEOUT}s"
        if error is None:
            result.ingested.append(document.url)
            progress(f"  [scout] ✓ {document.title} ingested")
        else:
            result.errors.append(error)
            progress(f"  [scout] ✗ {error}")


def locate(
    cfg: WorkflowConfig,
    record: ParameterRecord,
    as_of: date,
    needs: list[str],
    known_chunk_ids: Iterable[str],
    later_until: date | None = None,
) -> tuple[list[RetrievalHit], list[str]]:
    """Look the analyst's named sources up in the corpus we already hold.

    The complement of `run`: that one fetches what is missing, this one finds
    what is present but was ranked out. Nothing here weakens the contract —
    the chunks come from the database like any retrieved chunk and the
    verbatim-quote check still applies to whatever gets cited from them.
    Returns the new chunks (not already among `known_chunk_ids`) and the
    citations they belong to, for the ScoutResult and the reviewer. With
    `later_until`, a named source whose version starts after `as_of` and by
    that date is found too, as a "later_in_year" hit (retrieval.later_in_year).
    """
    info = record.information
    seen = set(known_chunk_ids)
    hits: list[RetrievalHit] = []
    citations: list[str] = []
    with retrieval.connect(cfg) as conn:
        scope = retrieval.jurisdiction_scope(
            conn, info.country, regions.region_key(info.country, info.model_target)
        )
        lang = retrieval.LANG_BY_COUNTRY.get(retrieval.scope_codes(scope)[0], "en")
        held = retrieval.instruments_of_chunks(conn, list(seen))
        # Articles missing between two retrieved ones (AGIRC-ARRCO art. 36
        # between 35 and 38), then the code articles the retrieved ones send
        # the reader to (R. 531-1 → R. 522-2), come first: they need no named
        # source at all.
        for hit in [
            *retrieval.gap_articles(conn, scope, lang, as_of, list(seen)),
            *retrieval.cross_referenced_articles(conn, scope, lang, as_of, list(seen)),
            *retrieval.same_act_articles(conn, lang, list(seen)),
        ]:
            if hit.chunk_id in seen:
                continue
            seen.add(hit.chunk_id)
            hits.append(hit)
            if hit.citation and hit.citation not in citations:
                citations.append(hit.citation)
        for need in needs[:5]:
            found = retrieval.locate_named_units(
                conn, scope, lang, as_of, need, held_instrument_ids=held
            )
            if later_until is not None and later_until > as_of:
                found += [
                    hit.model_copy(update={"method": "later_in_year"})
                    for hit in retrieval.locate_named_units(
                        conn, scope, lang, later_until, need, held_instrument_ids=held
                    )
                    if (retrieval.validity_start(hit.validity) or date.min) > as_of
                ]
            for hit in found:
                if hit.chunk_id in seen:
                    continue
                seen.add(hit.chunk_id)
                hits.append(hit)
                if hit.citation and hit.citation not in citations:
                    citations.append(hit.citation)
    return hits, citations
