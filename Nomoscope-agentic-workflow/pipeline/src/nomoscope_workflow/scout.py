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

import re
import time
from dataclasses import dataclass, field
from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from . import llm, retrieval, scout_ingest, web
from .config import PLACEHOLDER_MODEL_ID, WorkflowConfig
from .schema import ParameterRecord
from .scout_ingest import INGEST_TIMEOUT, embed_timeout, known_instruments  # noqa: F401
from .scout_sources import (  # noqa: F401  (re-exported: scout is the facade)
    COUNTRY_SOURCES,
    GUIDANCE_PUBLISHERS,
    ID_HINTS,
    GuidanceDocument,
    canonical_url,
    guidance_document,
)
from .tracing import progress
from .web import QUOTA_EXHAUSTED, WebSearchUnavailable, web_search  # noqa: F401

#: The corpus-side lookup of the analyst's named sources; it touches neither
#: web nor ingest and lives with the rest of retrieval.
locate = retrieval.locate_sources

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
    if cfg.scout == "tavily" and cfg.tavily_api_key:
        for query in result.queries:
            try:
                for hit in web_search(cfg.tavily_api_key, query, rules["domains"]):
                    url = hit.get("url", "")
                    result.urls.append(url)
                    for found in pattern.findall(url):
                        ids.append(found)
                        titles.setdefault(found, hit.get("title", ""))
            except WebSearchUnavailable as exc:
                result.errors.append(str(exc))
                progress(f"  [scout] ✗ {exc}")
                break
            except Exception as exc:
                result.errors.append(f"tavily search failed: {exc}")

    documents = _search_guidance(cfg, info.country, suggestion, result)

    result.candidate_ids = list(dict.fromkeys(ids))
    if len(result.candidate_ids) > 1 and titles:
        result.candidate_ids = _rank_candidates(cfg, info, result.candidate_ids, titles)
    known = scout_ingest.known_instruments(cfg, result.candidate_ids, rules) | set(attempted or ())
    to_ingest = [i for i in result.candidate_ids if i not in known][: cfg.scout_max_ingest]
    if result.candidate_ids:
        progress(
            f"  [scout] {len(result.candidate_ids)} candidate instrument(s), "
            f"{len(known)} already in DB, {len(to_ingest)} to ingest"
        )
    suffix = rules.get("ingest_suffix", "")
    jobs = [
        _IngestJob(
            key=instrument_id,
            label=instrument_id + suffix,
            args=scout_ingest.instrument_args(cfg, info.country, instrument_id + suffix),
            announce=(
                f"{instrument_id}{suffix} "
                f"(archive-first: fetch → snapshot → parse → chunk; up to {INGEST_TIMEOUT}s)"
            ),
        )
        for instrument_id in to_ingest
    ]
    jobs += _guidance_jobs(cfg, info.country, documents, result, set(attempted or ()))
    _ingest_all(cfg, jobs, result)
    if not result.candidate_ids and not result.errors:
        progress("  [scout] no candidate instrument found for the stated needs")
    if result.ingested and cfg.embedding_model_id != PLACEHOLDER_MODEL_ID:
        progress(
            "  [scout] embedding new chunks with BGE-M3 "
            f"(~1 chunk/s on CPU — expect high CPU, up to {embed_timeout()}s)…"
        )
        started = time.monotonic()
        error = scout_ingest.build_embeddings(cfg)
        if error:
            result.errors.append(error)  # FTS still covers the new chunks
            progress(f"  [scout] ✗ {error}")
        else:
            progress(f"  [scout] ✓ embeddings up to date ({time.monotonic() - started:.0f}s)")
    return result


#: At most this many guidance documents ingested per round (each is one PDF).
GUIDANCE_MAX_INGEST = 2

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
    if not publishers or cfg.scout != "tavily" or not cfg.tavily_api_key or web.unavailable():
        return []
    queries = [q for q in suggestion.guidance_queries if q.strip()][:2]
    if not queries:
        queries = [n[:_NEED_CHARS] for n in result.needs if _GUIDANCE_HINT.search(n)][:1]
    documents: dict[str, GuidanceDocument] = {}
    domains = [p["domain"] for p in publishers]
    for query in queries:
        result.queries.append(query)
        try:
            hits = web_search(cfg.tavily_api_key, query, domains)
        except WebSearchUnavailable as exc:
            result.errors.append(str(exc))
            break
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


@dataclass(frozen=True)
class _IngestJob:
    """One archive-first ingest the scout decided on."""

    key: str  # what `ScoutResult.ingested` records: the instrument id or the URL
    label: str  # what progress and error lines name
    args: list[str]  # the Nomotheca CLI command
    announce: str  # the "ingesting …" progress line


def _guidance_jobs(
    cfg: WorkflowConfig,
    country: str,
    documents: list[GuidanceDocument],
    result: ScoutResult,
    attempted: set[str],
) -> list[_IngestJob]:
    """The new guidance documents, as contributed documents of their publisher's kind."""
    if not documents:
        return []
    urls = [d.url for d in documents]
    result.candidate_ids += [u for u in urls if u not in result.candidate_ids]
    known = scout_ingest.known_instruments(cfg, urls, {}) | attempted
    fresh = [d for d in documents if d.url not in known][:GUIDANCE_MAX_INGEST]
    progress(
        f"  [scout] {len(documents)} guidance document(s) "
        f"({', '.join(sorted({d.publisher for d in documents}))}), "
        f"{len(documents) - len([d for d in documents if d.url not in known])} already in DB, "
        f"{len(fresh)} to ingest"
    )
    return [
        _IngestJob(
            key=document.url,
            label=document.title,
            args=[
                "document", document.url,
                "--database-url", cfg.database_url,
                "--jurisdiction", country,
                "--lang", retrieval.LANG_BY_COUNTRY.get(country, "en"),
                "--title", document.title,
                "--kind", document.kind,
                "--valid-from", document.valid_from.isoformat(),
                "--trigger", "cache_miss",
            ],
            announce=f"{document.title} as {document.kind} (guidance)",
        )
        for document in fresh
    ]


def _ingest_all(cfg: WorkflowConfig, jobs: list[_IngestJob], result: ScoutResult) -> None:
    """The scout's one ingest loop: instruments and guidance documents alike."""
    for job in jobs:
        progress(f"  [scout] ingesting {job.announce}…")
        started = time.monotonic()
        error = scout_ingest.run_ingest_cli(cfg, job.args, job.label)
        if error is None:
            result.ingested.append(job.key)
            progress(f"  [scout] ✓ {job.label} ingested ({time.monotonic() - started:.0f}s)")
        else:
            result.errors.append(error)
            progress(f"  [scout] ✗ {error}")
