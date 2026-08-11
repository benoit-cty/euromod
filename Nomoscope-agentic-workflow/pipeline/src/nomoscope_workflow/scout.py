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
from dataclasses import dataclass, field
from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from . import llm
from .config import WorkflowConfig
from .query_encoder import ingest_dir
from .schema import ParameterRecord
from .tracing import progress

INGEST_TIMEOUT = 600  # a single arrêté is seconds; a loi de finances, minutes
# The embedding pass covers the whole backlog of unembedded chunks, not just the
# scouted instrument (the CLI has no per-instrument scope), and BGE-M3 on CPU
# runs at roughly one chunk per second — a freshly ingested loi de finances
# alone is ~10 minutes. The build commits per batch, so even a timeout here
# keeps the vectors computed so far; the retry then resumes where it stopped.
EMBED_TIMEOUT = int(os.environ.get("WORKFLOW_SCOUT_EMBED_TIMEOUT", "1800"))

# Per-country discovery rules: the official domains web search is restricted
# to, and the id shapes the archive-first ingester can fetch directly.
#
# Keys:
#   domains      — official domains the web search is restricted to
#   id_pattern   — id shapes harvested from result URLs and from the LLM's answer
#   act_kinds    — the country's own words for the acts that fix values (prompt)
#   ingest_suffix— appended to a bare id to make it what the ingester should fetch
#   known_key    — instruments.metadata key holding this id, when national_id is
#                  something else (else the known-check misses and we re-ingest)
COUNTRY_SOURCES: dict[str, dict] = {
    "FR": {
        "domains": ["legifrance.gouv.fr"],
        # JORF instruments (lois, décrets, arrêtés) and single consolidated
        # code articles (LEGIARTI — where most rates actually live once
        # codified) — deliberately not LEGITEXT: ingesting a whole code by
        # accident is not a gap-fill.
        "id_pattern": re.compile(r"\b(?:JORFTEXT|LEGIARTI)\d{12}\b"),
        "act_kinds": "loi, décret or arrêté",
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

SCOUT_SYSTEM = """You are a legal-sources librarian for {country} tax-benefit legislation.
A retrieval system searched a legislation database and could not find the legal text that
sets the value of a policy parameter. Identify the official publication(s) that fix this
parameter's value (the specific {act_kinds} or equivalent — many values are set by
annual implementing acts rather than by the statutes that define them).
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
        "or the LEGIARTI############ id of the consolidated code article"
    ),
    "LT": (
        "for Lithuania the TAR document id shown in e-seimas /portal/legalAct/lt/TAD/<id> "
        "URLs — either TAR.############ or a 32-character hexadecimal id"
    ),
}


class ScoutSuggestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    search_queries: list[str] = Field(default_factory=list)
    instrument_ids: list[str] = Field(default_factory=list)
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

    def summary(self) -> dict:
        return {
            "mode": self.mode,
            "queries": self.queries,
            "urls": self.urls,
            "candidate_ids": self.candidate_ids,
            "ingested": self.ingested,
            "errors": self.errors,
            "reasoning": self.reasoning,
        }


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
    """Archive-first ingest of one instrument via the Nomotheca CLI; error text on failure."""
    directory = ingest_dir()
    if directory is None:
        return "could not locate Nomotheca-RAG/ingest (set EUROMOD_INGEST_DIR)"
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    env["PYTHONUNBUFFERED"] = "1"
    proc = subprocess.run(
        [
            "uv", "run", "python", "-m", "nomotheca_ingest.cli",
            "instrument", country.lower(), instrument_id,
            "--database-url", cfg.database_url,
        ],
        cwd=directory,
        env=env,
        capture_output=True,
        text=True,
        timeout=INGEST_TIMEOUT,
    )
    if proc.returncode != 0:
        return _proc_failure(f"{instrument_id}: ingest", proc)
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
    if directory is None:
        return "could not locate Nomotheca-RAG/ingest (set EUROMOD_INGEST_DIR)"
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    env["PYTHONUNBUFFERED"] = "1"
    command = [
        "uv", "run", "--extra", "embeddings", "python", "-m", "nomotheca_ingest.cli",
        "embeddings", "build", "--database-url", cfg.database_url,
        # Rich's live progress is noise in captured output and can bury the
        # real error; the per-batch commits do not depend on it.
        "--no-progress",
    ]
    if (directory / "models" / "bge-m3-openvino").is_dir():
        command += ["--backend", "openvino", "--model-path", "models/bge-m3-openvino"]
    proc = subprocess.run(
        command, cwd=directory, env=env, capture_output=True, text=True, timeout=EMBED_TIMEOUT
    )
    if proc.returncode != 0:
        return _proc_failure("embeddings build", proc)
    return None


def run(cfg: WorkflowConfig, record: ParameterRecord, as_of: date) -> ScoutResult:
    """Discover candidate instruments for a parameter and ingest the new ones."""
    info = record.information
    result = ScoutResult(mode=cfg.scout)
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
            ),
            (
                f"Parameter: {info.model_target}\n"
                f"Label: {(info.short_label or {}).get('en', '')} — {(info.label or {}).get('en', '')}\n"
                f"Description: {(info.description or {}).get('en', '')}\n"
                f"Reference date: {as_of.isoformat()} (find the act setting the value in force then)"
            ),
            output_type=ScoutSuggestion,
        )
    except Exception as exc:
        result.errors.append(f"scout LLM failed: {exc}")
        return result
    result.reasoning = suggestion.reasoning
    result.queries = suggestion.search_queries[:3]

    pattern: re.Pattern = rules["id_pattern"]
    ids = [m for text in suggestion.instrument_ids for m in pattern.findall(text)]
    titles: dict[str, str] = {}  # instrument id -> best search-result title
    if cfg.scout == "tavily" and cfg.tavily_api_key:
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

    result.candidate_ids = list(dict.fromkeys(ids))
    if len(result.candidate_ids) > 1 and titles:
        result.candidate_ids = _rank_candidates(cfg, info, result.candidate_ids, titles)
    known = _known_instruments(cfg, result.candidate_ids, rules)
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
