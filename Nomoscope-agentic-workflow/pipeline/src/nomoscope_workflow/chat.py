"""Chat with the legislation corpus: one tool-using agent turn per `chat` job.

The RAG assistant behind `rag-ui`. Unlike the parameter pipeline this is a
free-roaming PydanticAI agent, but it keeps the pipeline's two guarantees:

* **Quotes are mechanical.** The answer's `quotes` must each be found
  character-for-character (whitespace-tolerant, `retrieval.verify_extract`) in
  the chunk they name. A mistyped chunk id is resolved by its extract among the
  chunks this turn retrieved (one candidate only), as the critique does; a quote
  still unverified after one model retry is returned flagged, never silently.
* **Web text is never evidence.** `web_search` (Tavily, restricted to the
  country's official portals by default) only DISCOVERS acts. An act the corpus
  lacks comes back as a *discovery* the analyst may ingest — through the normal
  archive-first `ingest` job, from the UI, never from here.

Evidence retrieval reuses `retrieval.hybrid_search`, so the `context` class
(Country Reports) stays out exactly as it does for the pipeline (ADR 0001), and
a regional search is scoped to the country plus that one region (ADR 0003).

Each tool call prints one `@progress` line (start, then done with a summary),
so the UI can show what the assistant is doing; the turn ends with the one
`@result {json}` line the worker stores in `ops.jobs.result`.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Literal

import psycopg
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
)
from pydantic_ai.models.function import AgentInfo, FunctionModel
from pydantic_ai.settings import ModelSettings
from pydantic_ai.usage import UsageLimits

from . import llm, query_encoder, retrieval, scout
from .config import WorkflowConfig

#: Characters of a chunk handed to the model per search hit. Chunks average
#: ~2.3k and top out at 6k; a prefix is still verbatim, and `read_article`
#: returns the whole article when the model needs the rest.
HIT_CHARS = 2500
#: Model requests per turn (each tool round trip is one).
REQUEST_LIMIT = 14
#: Chunk ids are uuids; anything else is refused before it reaches SQL.
_UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

SYSTEM = """You are a research assistant for EUROMOD analysts at the EU Joint Research Centre.
You answer questions about the tax-benefit legislation of FR, BE, NL, ES, IE and LT from a
legislation database, and you help find sources the database does not hold yet.

Tools:
- search_legislation: hybrid (full-text + BGE-M3 vector) search over the legal texts in force
  on a date. Search in the law's own language when you can (e.g. French terms for FR); the
  vector leg is multilingual. language="en" searches English renderings (often machine
  translations). For a Spanish regional parameter pass the region code (e.g. "ES-AR").
- find_article: look up a named act/article ("article 197 du CGI", "Ley 35/2006 artículo 66").
- read_article: the full text of the article a chunk belongs to, all its chunks in order.
- web_search: search the web (official legal portals of the country by default) for acts the
  database lacks. Web results are LEADS, never evidence: never quote them as support for a value.

Rules:
- Ground every factual statement about the law in the database. Search before answering; if
  the first search misses, rephrase (law-language terms, article numbers) before giving up.
- quotes: each must be copied CHARACTER FOR CHARACTER from the content of the chunk whose
  chunk_id you give — no paraphrase, no ellipsis, no reformatted numbers. Keep each short
  (one sentence or one table row). These quotes are checked mechanically.
- In the answer, refer to quote i as [i] (1-based, in the order of `quotes`).
- Say which version you used (validity dates) when the date matters, and that a value comes
  from guidance rather than legislation when the source class is "guidance".
- If the database does not hold the source, say so plainly, then use web_search to locate the
  official act and report what you found as discoveries (the analyst decides whether to ingest).
- Answer in the language of the user's question. Be concise; use Markdown."""


# --------------------------------------------------------------------- request


class Quote(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chunk_id: str = Field(description="chunks.id of the chunk the extract is copied from")
    extract: str = Field(description="verbatim text copied from that chunk's content")


class ChatAnswer(BaseModel):
    """What the model returns; quotes are verified before the turn ends."""

    model_config = ConfigDict(extra="forbid")

    answer: str = Field(description="Markdown answer; cite quote i as [i]")
    quotes: list[Quote] = Field(default_factory=list)
    web_urls: list[str] = Field(
        default_factory=list, description="URLs from web_search results the answer mentions"
    )


class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")

    role: Literal["user", "assistant"]
    content: str
    #: An earlier assistant turn's verified quotes, so "tell me more about [2]"
    #: can be resolved to a chunk id.
    quotes: list[dict[str, Any]] = Field(default_factory=list)


class ChatRequest(BaseModel):
    """The `chat` job payload (the worker validates the same shape in jobs.py)."""

    model_config = ConfigDict(extra="ignore")

    messages: list[ChatMessage] = Field(min_length=1)
    conversation_id: str | None = None
    country: str | None = None
    as_of: date | None = None
    model: str | None = None
    web: bool = True

    @model_validator(mode="after")
    def _ends_with_a_question(self) -> ChatRequest:
        last = self.messages[-1]
        if last.role != "user" or not last.content.strip():
            msg = "the last message must be a non-empty user message"
            raise ValueError(msg)
        return self


# ------------------------------------------------------------------- the agent


def emit(event: dict[str, Any]) -> None:
    """One `@progress` line: the worker turns it into a progress event."""
    print("@progress " + json.dumps(event, ensure_ascii=False, default=str), flush=True)


@dataclass
class ChatDeps:
    cfg: WorkflowConfig
    conn: psycopg.Connection
    as_of: date
    country: str | None
    web: bool
    #: Every chunk a tool returned this turn, by id (the UI's source panel).
    sources: dict[str, dict[str, Any]] = field(default_factory=dict)
    #: Every web result returned this turn, by URL.
    web_results: dict[str, dict[str, Any]] = field(default_factory=dict)
    #: Official acts found on the web and missing from the corpus, by id.
    discoveries: dict[str, dict[str, Any]] = field(default_factory=dict)
    #: The query vector of each searched string, so a multi-country search
    #: encodes once.
    vectors: dict[str, str | None] = field(default_factory=dict)

    def register(self, hit: retrieval.RetrievalHit, country: str | None) -> dict[str, Any]:
        row = {
            "chunk_id": hit.chunk_id,
            "citation": hit.citation,
            "context_header": hit.context_header,
            "content": hit.content,
            "lang": hit.lang,
            "validity": hit.validity,
            "version_status": hit.version_status,
            "source_trust_class": str(hit.source_trust_class),
            "country": country,
            "method": hit.method,
            "score": hit.score,
        }
        self.sources.setdefault(hit.chunk_id, row)
        return row


def _hit_for_model(row: dict[str, Any]) -> dict[str, Any]:
    content = row["content"] or ""
    out = {k: row[k] for k in ("chunk_id", "citation", "context_header", "validity", "source_trust_class", "lang")}
    out["content"] = content[:HIT_CHARS]
    if len(content) > HIT_CHARS:
        out["truncated"] = True
    return out


def _countries(deps: ChatDeps, country: str | None) -> list[str]:
    code = (country or deps.country or "").upper()
    if code:
        return [code.split("-")[0]]
    return [c for c in retrieval.LANG_BY_COUNTRY if c != "BE"]


def _as_of(deps: ChatDeps, as_of: str | None) -> date:
    if not as_of:
        return deps.as_of
    try:
        return date.fromisoformat(as_of)
    except ValueError as exc:
        raise ModelRetry(f"as_of must be YYYY-MM-DD, got {as_of!r}") from exc


def _scope(deps: ChatDeps, country: str, region: str | None) -> list[str]:
    if region and region.upper().startswith(country + "-"):
        return [country, region.upper()]
    return [country]


def search_legislation(
    ctx: RunContext[ChatDeps],
    query: str,
    country: str | None = None,
    region: str | None = None,
    language: Literal["original", "en"] = "original",
    as_of: str | None = None,
    k: int = 8,
) -> list[dict[str, Any]]:
    """Hybrid search of the legal texts in force on `as_of` (default: the chat's date).

    Args:
        query: what to look for, ideally in the law's own language.
        country: FR, BE, NL, ES, IE or LT; omitted = the chat's country, else all.
        region: a Spanish autonomous community (e.g. "ES-AR") to search with its country.
        language: "original" (the law's language) or "en" (English renderings).
        as_of: YYYY-MM-DD; the version in force on that day is searched.
        k: number of passages to return (max 15).
    """
    deps = ctx.deps
    day = _as_of(deps, as_of)
    countries = _countries(deps, country)
    k = max(1, min(int(k), 15))
    per_country = k if len(countries) == 1 else max(2, k // 2)
    emit({"event": "tool", "status": "start", "tool": "search_legislation",
          "args": {"query": query, "countries": countries, "region": region, "language": language, "as_of": day}})
    if query not in deps.vectors:
        deps.vectors[query] = (
            query_encoder.encode(query, deps.cfg.database_url, deps.cfg.embedding_model_id)
            if deps.cfg.embedding_model_id != 99
            else None
        )
    rows: list[dict[str, Any]] = []
    for code in countries:
        lang = "en" if language == "en" else retrieval.LANG_BY_COUNTRY.get(code, "en")
        hits = retrieval.hybrid_search(
            deps.conn, _scope(deps, code, region), lang, day, query,
            deps.cfg.embedding_model_id, per_country, deps.vectors[query],
        )
        rows += [deps.register(hit, code) for hit in hits]
    rows.sort(key=lambda r: -(deps.sources[r["chunk_id"]].get("score") or 0))
    emit({"event": "tool", "status": "done", "tool": "search_legislation",
          "summary": f"{len(rows)} passage(s)", "chunk_ids": [r["chunk_id"] for r in rows]})
    return [_hit_for_model(r) for r in rows]


def find_article(
    ctx: RunContext[ChatDeps], reference: str, country: str | None = None, as_of: str | None = None
) -> list[dict[str, Any]]:
    """Look up a named act or article directly (title + article number), no ranking.

    Args:
        reference: the act/article as the law names it, e.g. "article 197 du code général des impôts".
        country: FR, BE, NL, ES, IE or LT (default: the chat's country).
        as_of: YYYY-MM-DD (default: the chat's date).
    """
    deps = ctx.deps
    day = _as_of(deps, as_of)
    code = _countries(deps, country)[0] if (country or deps.country) else None
    if code is None:
        raise ModelRetry("find_article needs a country")
    emit({"event": "tool", "status": "start", "tool": "find_article",
          "args": {"reference": reference, "country": code, "as_of": day}})
    lang = retrieval.LANG_BY_COUNTRY.get(code, "en")
    hits = retrieval.locate_named_units(deps.conn, [code], lang, day, reference)
    rows = [deps.register(hit, code) for hit in hits]
    emit({"event": "tool", "status": "done", "tool": "find_article",
          "summary": f"{len(rows)} passage(s)", "chunk_ids": [r["chunk_id"] for r in rows]})
    return [_hit_for_model(r) for r in rows]


def read_article(ctx: RunContext[ChatDeps], chunk_id: str) -> dict[str, Any]:
    """The full article a chunk belongs to: every chunk in order, plus its provenance.

    Args:
        chunk_id: a chunk_id returned by search_legislation or find_article.
    """
    deps = ctx.deps
    if not _UUID.match(chunk_id or ""):
        raise ModelRetry(f"{chunk_id!r} is not a chunk_id (a uuid from a search result)")
    emit({"event": "tool", "status": "start", "tool": "read_article", "args": {"chunk_id": chunk_id}})
    hits = retrieval.unit_chunks(deps.conn, chunk_id)
    if not hits:
        emit({"event": "tool", "status": "done", "tool": "read_article", "summary": "no such chunk"})
        return {"error": f"no chunk {chunk_id}"}
    country = deps.sources.get(chunk_id, {}).get("country")
    rows = [deps.register(hit, country) for hit in hits]
    provenance = retrieval.version_provenance(deps.conn, chunk_id) or {}
    emit({"event": "tool", "status": "done", "tool": "read_article",
          "summary": f"{rows[0]['citation'] or 'article'} — {len(rows)} chunk(s)",
          "chunk_ids": [r["chunk_id"] for r in rows]})
    return {
        "citation": rows[0]["citation"],
        "validity": rows[0]["validity"],
        "instrument_type": provenance.get("instrument_type"),
        "snapshot_retrieved_at": str(provenance.get("retrieved_at") or ""),
        "chunks": [{"chunk_id": r["chunk_id"], "content": r["content"]} for r in rows],
    }


def web_search(
    ctx: RunContext[ChatDeps], query: str, country: str | None = None, official_only: bool = True
) -> dict[str, Any]:
    """Search the web for legislation the database lacks. Results are leads, not evidence.

    Args:
        query: a short query, in the law's language, phrased to find the act.
        country: FR, BE, NL, ES, IE or LT (default: the chat's country).
        official_only: restrict to the country's official legal portals (recommended).
    """
    deps = ctx.deps
    if not deps.web:
        return {"error": "web search is switched off for this chat"}
    if not deps.cfg.tavily_api_key:
        return {"error": "web search is not configured on the worker (no TAVILY_API_KEY)"}
    if scout._web_search_unavailable:
        return {"error": scout._web_search_unavailable}
    code = _countries(deps, country)[0] if (country or deps.country) else None
    rules = scout.COUNTRY_SOURCES.get(code or "", {})
    domains = rules.get("domains", []) if official_only else []
    emit({"event": "tool", "status": "start", "tool": "web_search",
          "args": {"query": query, "country": code, "domains": domains}})
    try:
        results = scout._tavily_search(deps.cfg.tavily_api_key, query, domains)
    except Exception as exc:
        if "432" in str(exc):
            scout._web_search_unavailable = "web search unavailable: the Tavily plan's usage limit is exhausted (HTTP 432)"
        emit({"event": "tool", "status": "done", "tool": "web_search", "summary": f"failed: {exc}"})
        return {"error": f"web search failed: {exc}"}

    pattern = rules.get("id_pattern")
    ids_by_url = {
        r.get("url", ""): list(dict.fromkeys(pattern.findall(r.get("url", "")))) if pattern else []
        for r in results
    }
    all_ids = [i for ids in ids_by_url.values() for i in ids]
    known = scout._known_instruments(deps.cfg, all_ids, rules) if all_ids else set()
    out = []
    for r in results:
        url = r.get("url", "")
        row = {
            "title": r.get("title", ""),
            "url": url,
            "snippet": (r.get("content") or "")[:600],
            "instrument_ids": [{"id": i, "in_corpus": i in known} for i in ids_by_url[url]],
        }
        deps.web_results.setdefault(url, row)
        for i in ids_by_url[url]:
            if i not in known and code:
                deps.discoveries.setdefault(i, {
                    "country": code,
                    "instrument_id": i,
                    "ingest_id": i + rules.get("ingest_suffix", ""),
                    "title": row["title"],
                    "url": url,
                })
        out.append(row)
    emit({"event": "tool", "status": "done", "tool": "web_search",
          "summary": f"{len(out)} result(s), {sum(1 for i in all_ids if i not in known)} act(s) not in the corpus",
          "urls": [r["url"] for r in out]})
    return {
        "results": out,
        "note": "Leads only. Acts with in_corpus=false can be ingested by the analyst; do not quote web text as evidence.",
    }


TOOLS = (search_legislation, find_article, read_article, web_search)


# ------------------------------------------------------------- verification


def resolve_quote(conn: psycopg.Connection, quote: Quote, sources: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Verify one quote against its chunk; rewrite a wrong id only to the ONE
    retrieved chunk that contains the extract (`pipeline._resolve_chunk_by_extract`)."""
    chunk_id = quote.chunk_id.strip()
    offsets = retrieval.verify_extract(conn, chunk_id, quote.extract) if _UUID.match(chunk_id) else None
    resolved_from = None
    if offsets is None:
        candidates = [
            cid for cid, row in sources.items()
            if cid != chunk_id and _contains(row.get("content") or "", quote.extract)
        ]
        if len(candidates) == 1:
            resolved_from, chunk_id = chunk_id, candidates[0]
            offsets = retrieval.verify_extract(conn, chunk_id, quote.extract)
    return {
        "chunk_id": chunk_id,
        "extract": quote.extract,
        "verified": offsets is not None,
        "char_start": offsets[0] if offsets else None,
        "char_end": offsets[1] if offsets else None,
        "resolved_from": resolved_from,
    }


def _contains(content: str, extract: str) -> bool:
    if not extract.strip():
        return False
    if extract in content:
        return True
    return re.search(r"\s+".join(re.escape(p) for p in extract.split()), content) is not None


def _validate(ctx: RunContext[ChatDeps], output: ChatAnswer) -> ChatAnswer:
    """One retry for quotes that are not verbatim; after that they go out flagged."""
    if ctx.retry >= 1:
        return output
    bad = [
        i + 1 for i, q in enumerate(output.quotes)
        if not resolve_quote(ctx.deps.conn, q, ctx.deps.sources)["verified"]
    ]
    if bad:
        raise ModelRetry(
            f"quote(s) {bad} are not verbatim in the chunk they name. Copy the exact text "
            "from that chunk's content (same characters, numbers and punctuation), or drop the quote."
        )
    return output


# --------------------------------------------------------------- mock model


def _mock_model() -> FunctionModel:
    """`mock/…`: search once with the question, answer with the top passages.

    Drives the real tool loop and output validation with no key — for tests and
    demos, like mock.py for the pipeline.
    """

    def turn(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        last = messages[-1]
        returns = [p for p in last.parts if isinstance(p, ToolReturnPart)] if isinstance(last, ModelRequest) else []
        if not returns:
            question = next(
                p.content for m in reversed(messages) if isinstance(m, ModelRequest)
                for p in m.parts if isinstance(p, UserPromptPart)
            )
            return ModelResponse(parts=[ToolCallPart("search_legislation", {"query": str(question), "k": 3})])
        hits = returns[0].content if isinstance(returns[0].content, list) else []
        quotes = [{"chunk_id": h["chunk_id"], "extract": _first_line(h["content"])} for h in hits]
        lines = [f"- {h['citation'] or h['context_header']} [{i + 1}]" for i, h in enumerate(hits)]
        answer = "Top passages (mock model, no LLM):\n" + ("\n".join(lines) or "- nothing found")
        output_tool = info.output_tools[0].name
        return ModelResponse(parts=[ToolCallPart(output_tool, {"answer": answer, "quotes": quotes, "web_urls": []})])

    return FunctionModel(turn, model_name="mock-chat")


def _first_line(content: str) -> str:
    line = next((ln.strip() for ln in content.splitlines() if ln.strip()), "")
    return line[:200]


# -------------------------------------------------------------------- driver


def _history(messages: list[ChatMessage]) -> list[ModelMessage]:
    out: list[ModelMessage] = []
    for m in messages:
        if m.role == "user":
            out.append(ModelRequest(parts=[UserPromptPart(m.content)]))
            continue
        text = m.content
        if m.quotes:
            listing = "\n".join(
                f"[{i + 1}] chunk_id={q.get('chunk_id')} — {q.get('citation') or ''}: «{q.get('extract', '')[:200]}»"
                for i, q in enumerate(m.quotes)
            )
            text += f"\n\nQuotes of that answer:\n{listing}"
        out.append(ModelResponse(parts=[TextPart(text)]))
    return out


def _context_line(request: ChatRequest, as_of: date) -> str:
    country = request.country or "any of FR, BE, NL, ES, IE, LT"
    web = "available" if request.web else "switched off"
    return f"Chat settings — country: {country}; reference date: {as_of.isoformat()}; web search: {web}."


def run_turn(cfg: WorkflowConfig, request: ChatRequest) -> dict[str, Any]:
    """Answer the last user message; returns the job's `@result` payload."""
    model_name = request.model or cfg.model
    as_of = request.as_of or date.today()
    if model_name.startswith("mock/"):
        model = _mock_model()
        settings: ModelSettings = {}
    else:
        model = llm.get_model(model_name)
        settings = llm.model_settings(model_name, temperature=0.2)
    agent = Agent(
        model,
        deps_type=ChatDeps,
        output_type=ChatAnswer,
        instructions=SYSTEM + "\n\n" + _context_line(request, as_of),
        tools=list(TOOLS),
        model_settings=settings,
        retries=2,
    )
    agent.output_validator(_validate)

    question = request.messages[-1].content
    with retrieval.connect(cfg) as conn:
        conn.read_only = True
        deps = ChatDeps(cfg=cfg, conn=conn, as_of=as_of, country=(request.country or None) and request.country.upper(), web=request.web)
        result = agent.run_sync(
            question,
            deps=deps,
            message_history=_history(request.messages[:-1]),
            usage_limits=UsageLimits(request_limit=REQUEST_LIMIT),
        )
        output: ChatAnswer = result.output
        quotes = []
        for q in output.quotes:
            checked = resolve_quote(conn, q, deps.sources)
            if checked["chunk_id"] not in deps.sources:
                for hit in retrieval.unit_chunks(conn, checked["chunk_id"]) if checked["verified"] else []:
                    deps.register(hit, None)
            row = deps.sources.get(checked["chunk_id"], {})
            checked.update({k: row.get(k) for k in ("citation", "validity", "source_trust_class", "lang")})
            quotes.append(checked)

    usage = result.usage
    return {
        "answer": output.answer,
        "quotes": quotes,
        "web": [deps.web_results[u] for u in output.web_urls if u in deps.web_results],
        "web_results": list(deps.web_results.values()),
        "discoveries": list(deps.discoveries.values()),
        "sources": list(deps.sources.values()),
        "model": model_name,
        "as_of": as_of.isoformat(),
        "country": deps.country,
        "usage": {"requests": usage.requests, "input_tokens": usage.input_tokens, "output_tokens": usage.output_tokens},
    }
