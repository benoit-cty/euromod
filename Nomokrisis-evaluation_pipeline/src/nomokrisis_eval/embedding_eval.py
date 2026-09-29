"""Embedding (retrieval) evaluation: rank ground-truth chunks under each search leg.

Isolates the Activity 2 retrieval layer from the LLM workflow: each case is a
search query plus the citation(s) of the legal unit(s) a correct retriever must
surface. Every case is scored under three methods over the same as-of/country/
lang candidate set the production pipeline uses (Country Reports excluded):

  fts     FTS-only leg (nomoscope_workflow.retrieval.hybrid_search, no vector)
  vector  pure cosine ranking over `embeddings` — the number that moves when
          the embedding model/backend changes; this is the embedding eval proper
  hybrid  the production RRF fusion (what the workflow actually retrieves with)

Scoring is pure rank arithmetic — hit@1, hit@3, hit@k, MRR — with strict
normalised citation equality (see scoring.citation_equal), no LLM anywhere.
Query encoding goes through the workflow's query encoder for the model under
test (`--embedding-model-id N` is a nomotheca_ingest embedding-registry id, the
same id its chunk vectors are stored under), so each model is scored with its
own query prompt; `--embedding-model-id 99` selects the in-SQL placeholder
embedder for key-less, encoder-less demos.

Two sources of cases:

- hand-written retrieval cases (the original eval.embedding_cases rows);
- `cases_from_golden`: one case per verified golden case that expects a
  citation, searched with the query the workflow's `frame` step builds for that
  parameter (pipeline.frame_query), on the date and jurisdiction scope a run
  would use. This is what compares embedding models on the task itself rather
  than on a paraphrase of it.

`compare_runs` puts the latest run of each model side by side.

With a reranker (`--reranker <key>`, nomotheca_ingest.core.rerankers), two more
legs are scored: `rerank` — the production hybrid candidates, `rerank_pool` of
them, re-ordered by a cross-encoder reading query and chunk together, cut at k —
and `pool`, where the relevant chunk sits in that uncut candidate list: the
reranker's ceiling (it can only promote what the pool contains).
"""

from __future__ import annotations

import subprocess
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone

import psycopg
from psycopg.rows import dict_row

from nomoscope_workflow import regions, retrieval
from nomoscope_workflow.config import WorkflowConfig
from nomoscope_workflow.schema import RetrievalHit

from . import EVAL_VERSION
from .config import REPO_ROOT, EvalConfig
from .golden_store import embedding_set_hash
from .schema import EmbeddingCase, EmbeddingCaseResult, GoldenCase, Routing
from .scoring import citation_equal, citation_matches

#: Id prefix of the retrieval cases derived from golden cases.
GOLDEN_CASE_PREFIX = "golden:"

# Same candidate filter as retrieval.py's hybrid CTE: in force at as_of, one
# jurisdiction+lang, trust class 'context' excluded (Country Reports describe
# the model, not the law — retrieving one can never be a "relevant" outcome).
#
# Ranked by the computed `score`, never by `e.embedding <=> q` directly: that
# form lets the planner walk a model's HNSW index, which returns the 40 nearest
# chunks of the WHOLE corpus and only then applies the filters — a Lithuanian
# query got 2 rows out of 15 that way, and only the model that had an index
# (BGE-M3) was penalised. Exact ranking over one country's candidates is a few
# milliseconds and the same for every model. (retrieval.py's vector leg ranks
# inside a window function and never takes the index.)
_VECTOR_SQL_TEMPLATE = """
SELECT ch.id::text AS chunk_id, u.citation, ch.context_header, ch.content, t.lang,
       v.validity::text AS validity, v.version_status,
       (1 - (e.embedding <=> {qexpr}))::float8 AS score
FROM embeddings e
JOIN chunks ch             ON ch.id = e.chunk_id
JOIN unit_texts t          ON t.id = ch.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u         ON u.id = v.legal_unit_id
JOIN instruments i         ON i.id = u.instrument_id
JOIN jurisdictions j       ON j.id = i.jurisdiction_id
WHERE e.model_id = %(model_id)s
  AND j.code = ANY(%(jurisdictions)s::text[]) AND t.lang = %(lang)s
  AND v.validity @> %(as_of)s::date
  AND i.source_trust_class <> 'context'
ORDER BY score DESC
LIMIT %(k)s
"""

_CANDIDATES_SQL = """
SELECT count(*)::int AS chunks, count(e.chunk_id)::int AS embedded
FROM chunks ch
JOIN unit_texts t          ON t.id = ch.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u         ON u.id = v.legal_unit_id
JOIN instruments i         ON i.id = u.instrument_id
JOIN jurisdictions j       ON j.id = i.jurisdiction_id
LEFT JOIN embeddings e     ON e.chunk_id = ch.id AND e.model_id = %(model_id)s
WHERE j.code = ANY(%(jurisdictions)s::text[]) AND t.lang = %(lang)s
  AND v.validity @> %(as_of)s::date
  AND i.source_trust_class <> 'context'
"""

METHODS = ("fts", "vector", "hybrid", "rerank", "pool")


def vector_search(
    conn: psycopg.Connection,
    country: retrieval.Scope,
    lang: str,
    as_of,
    query: str,
    model_id: int,
    k: int,
    query_vector: str | None,
) -> list[RetrievalHit]:
    """Pure cosine ranking over the embedded candidate set (no FTS leg)."""
    use_placeholder = model_id == 99  # demo embedder lives in SQL, as in retrieval.py
    sql = _VECTOR_SQL_TEMPLATE.format(
        qexpr="placeholder_embedding(%(q)s)" if use_placeholder else "%(qvec)s::halfvec(1024)"
    )
    rows = conn.execute(
        sql,
        {
            "jurisdictions": retrieval.scope_codes(country),
            "lang": lang,
            "as_of": as_of,
            "q": query,
            "qvec": query_vector,
            "model_id": model_id,
            "k": k,
        },
    ).fetchall()
    return [RetrievalHit(method="vector", **row) for row in rows]


def first_relevant_rank(expected_citations: list[str], hits: list[RetrievalHit]) -> int | None:
    """1-based rank of the first hit whose citation equals an expected one, else None."""
    for rank, hit in enumerate(hits, start=1):
        if any(citation_equal(expected, hit.citation) for expected in expected_citations):
            return rank
    return None


def rank_metrics(ranks: list[int | None], k: int) -> dict[str, str]:
    """hit@1 / hit@3 / hit@k / MRR over one method's ranks (misses count as 0
    reciprocal rank). hit@3 is the production cut: the hybrid fusion guarantees
    the vector leg's top 3 a place in what the model reads."""
    n = len(ranks)
    if n == 0:
        return {}
    metrics = {
        "cases": str(n),
        "hit@1": f"{100 * sum(1 for r in ranks if r == 1) / n:.0f}%",
        "hit@3": f"{100 * sum(1 for r in ranks if r is not None and r <= 3) / n:.0f}%",
        f"hit@{k}": f"{100 * sum(1 for r in ranks if r is not None and r <= k) / n:.0f}%",
        "mrr": f"{sum(1 / r for r in ranks if r) / n:.2f}",
    }
    # The `pool` leg ranks past k (the whole reranker input): say how much of it
    # the reranker could possibly promote.
    if any(r is not None and r > k for r in ranks):
        metrics["found"] = f"{100 * sum(1 for r in ranks if r is not None) / n:.0f}%"
    return metrics


def rerank_hits(query: str, hits: list[RetrievalHit], reranker: str) -> list[RetrievalHit]:
    """`hits` re-ordered by the cross-encoder's score (stable on ties)."""
    from nomoscope_workflow import query_encoder

    if not hits:
        return []
    scores = query_encoder.rerank(
        query, [f"{hit.context_header or ''}\n{hit.content or ''}" for hit in hits], reranker
    )
    order = sorted(range(len(hits)), key=lambda i: -scores[i])
    return [hits[i] for i in order]


def run_embedding_eval(
    cfg: EvalConfig,
    cases: list[EmbeddingCase],
    k: int = 10,
    embedding_model_id: int = 1,
    notes: str | None = None,
    reranker: str | None = None,
    rerank_pool: int = 50,
) -> tuple[dict, list[EmbeddingCaseResult]]:
    """Score every case under fts / vector / hybrid; returns (manifest, results)."""
    from nomoscope_workflow import query_encoder  # deferred: spawns a subprocess lazily

    run_id = (
        f"embeval-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}"
        f"-m{embedding_model_id}-{uuid.uuid4().hex[:6]}"
    )
    manifest = {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "embedding_model_id": embedding_model_id,
        "embedding_model": _model_name(cfg.database_url, embedding_model_id),
        "k": k,
        "eval_version": EVAL_VERSION,
        "dataset_version": embedding_set_hash(cases),
        "git_commit": _git_commit(),
        "countries": sorted({c.country for c in cases}),
        "cases": len(cases),
        "notes": notes,
        "reranker": reranker,
        "rerank_pool": rerank_pool if reranker else None,
    }

    results: list[EmbeddingCaseResult] = []
    encode_seconds: list[float] = []
    rerank_seconds: list[float] = []
    with psycopg.connect(cfg.database_url, row_factory=dict_row) as conn:
        for case in cases:
            corpus_lang = case.corpus_lang or case.language
            result = EmbeddingCaseResult(
                case_id=case.id,
                country=case.country,
                language=case.language,
                corpus_lang=corpus_lang,
                k=k,
            )
            try:
                # Same scope rule as the pipeline (ADR 0003): the country, plus
                # the region's child jurisdiction when the case names a region.
                scope = retrieval.jurisdiction_scope(conn, case.country.upper(), case.region)
                common = (conn, scope, corpus_lang, case.as_of, case.query)
                counts = conn.execute(
                    _CANDIDATES_SQL,
                    {
                        "jurisdictions": scope,
                        "lang": corpus_lang,
                        "as_of": case.as_of,
                        "model_id": embedding_model_id,
                    },
                ).fetchone()
                result.candidate_chunks = counts["chunks"]
                result.embedded_chunks = counts["embedded"]

                # model_id is irrelevant without a vector leg; 0 avoids the 99 placeholder path
                fts_hits = retrieval.hybrid_search(*common, model_id=0, k=k, query_vector=None)
                result.ranks["fts"] = first_relevant_rank(case.expected_citations, fts_hits)

                qvec = None
                if embedding_model_id != 99:
                    started = time.monotonic()
                    qvec = query_encoder.encode(case.query, cfg.database_url, embedding_model_id)
                    encode_seconds.append(time.monotonic() - started)
                if embedding_model_id == 99 or qvec is not None:
                    vec_hits = vector_search(*common, embedding_model_id, k, qvec)
                    result.ranks["vector"] = first_relevant_rank(case.expected_citations, vec_hits)
                    hyb_hits = retrieval.hybrid_search(
                        *common, model_id=embedding_model_id, k=k, query_vector=qvec
                    )
                    result.ranks["hybrid"] = first_relevant_rank(case.expected_citations, hyb_hits)
                    if reranker:
                        pool = retrieval.hybrid_search(
                            *common, model_id=embedding_model_id, k=rerank_pool, query_vector=qvec
                        )
                        result.ranks["pool"] = first_relevant_rank(case.expected_citations, pool)
                        started = time.monotonic()
                        reranked = rerank_hits(case.query, pool, reranker)[:k]
                        rerank_seconds.append(time.monotonic() - started)
                        result.ranks["rerank"] = first_relevant_rank(case.expected_citations, reranked)
                else:
                    result.error = "query encoder unavailable — vector/hybrid not scored"
            except Exception as exc:  # score the failure, keep the run going
                result.error = f"{exc.__class__.__name__}: {exc}"
                conn.rollback()
            results.append(result)
    # The first query pays the model load; the median is the per-query cost.
    if len(encode_seconds) > 1:
        manifest["query_encode_ms_median"] = round(1000 * sorted(encode_seconds[1:])[len(encode_seconds[1:]) // 2])
    if len(rerank_seconds) > 1:
        manifest["rerank_ms_median"] = round(1000 * sorted(rerank_seconds[1:])[len(rerank_seconds[1:]) // 2])
    return manifest, results


def summarize_embedding(results: list[EmbeddingCaseResult]) -> dict[str, dict[str, dict[str, str]]]:
    """{query language: {method: metrics}} over the cases each method scored."""
    by_lang: dict[str, list[EmbeddingCaseResult]] = defaultdict(list)
    for result in results:
        by_lang[result.language].append(result)

    table: dict[str, dict[str, dict[str, str]]] = {}
    for lang, rows in sorted(by_lang.items()):
        k = rows[0].k
        table[lang] = {
            method: rank_metrics([r.ranks[method] for r in rows if method in r.ranks], k)
            for method in METHODS
        }
    return table


def _model_name(database_url: str, model_id: int) -> str | None:
    with psycopg.connect(database_url) as conn:
        row = conn.execute("SELECT name FROM embedding_models WHERE id = %s", (model_id,)).fetchone()
    return row[0] if row else None


# --------------------------------------------------------------------------- #
# Cases derived from the golden set
# --------------------------------------------------------------------------- #

_UNITS_IN_SCOPE_SQL = """
SELECT DISTINCT u.citation, ch.context_header
FROM chunks ch
JOIN unit_texts t          ON t.id = ch.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u         ON u.id = v.legal_unit_id
JOIN instruments i         ON i.id = u.instrument_id
JOIN jurisdictions j       ON j.id = i.jurisdiction_id
WHERE j.code = ANY(%(jurisdictions)s::text[]) AND t.lang = %(lang)s
  AND v.validity @> %(as_of)s::date
  AND i.source_trust_class <> 'context'
  AND u.citation IS NOT NULL
"""

#: Routings with no evidence to find: `derived` short-circuits before retrieval,
#: `national_team_source` routes around the pipeline.
_NO_RETRIEVAL_ROUTINGS = {Routing.DERIVED, Routing.NATIONAL_TEAM_SOURCE}


@dataclass(slots=True)
class GoldenCaseDerivation:
    """What `cases_from_golden` produced, and why it skipped the rest."""

    cases: list[EmbeddingCase] = field(default_factory=list)
    skipped: dict[str, str] = field(default_factory=dict)


#: A golden citation naming more articles than this is instrument-level ("VSDĮ",
#: "JORFTEXT000025044460"): any article of the act would count as a hit, which
#: says nothing about ranking. It is dropped from the retrieval case.
MAX_UNITS_PER_CITATION = 3


def resolve_citations(
    conn: psycopg.Connection, expected: list[str], jurisdictions: list[str], lang: str, as_of
) -> list[str]:
    """The exact `legal_units.citation` strings a golden citation list names.

    A golden citation is written the way the main eval's `retrieval_hit`
    matches it — `citation_matches` against the unit's citation OR the chunk's
    context header ("Wet IB 2001, artikel 2.10a"), one-directional containment.
    The retrieval eval compares by strict equality, so each is resolved here,
    once, to the units in the searched candidate set that satisfy it (an exact
    citation match, when there is one, wins over containment); one that
    resolves to more than MAX_UNITS_PER_CITATION units is too coarse to rank.
    """
    rows = conn.execute(
        _UNITS_IN_SCOPE_SQL, {"jurisdictions": jurisdictions, "lang": lang, "as_of": as_of}
    ).fetchall()
    resolved: dict[str, None] = {}
    for exp in expected:
        # Exact first: containment lets "CGI, art. 197" claim "CGI, art. 197 A".
        units = {row["citation"] for row in rows if citation_equal(exp, row["citation"])} or {
            row["citation"]
            for row in rows
            if citation_matches(exp, row["citation"]) or citation_matches(exp, row["context_header"])
        }
        if len(units) <= MAX_UNITS_PER_CITATION:
            resolved.update(dict.fromkeys(sorted(units)))
    return sorted(resolved)


def cases_from_golden(
    params_conn: psycopg.Connection,
    conn: psycopg.Connection,
    wf_cfg: WorkflowConfig,
    golden: list[GoldenCase],
) -> GoldenCaseDerivation:
    """One retrieval case per golden case that has evidence to find.

    Query, date and scope are the workflow's own for that parameter: the
    `frame` step's query (pipeline.frame_query), `_retrieval_as_of` (1 July
    after the income year for income_year parameters), and the region scope of
    ADR 0003. The case is `verified` when its golden case is.

    Two connections because the two libraries read rows differently:
    `params_conn` (tuple rows) loads parameter records through paramdb,
    `conn` (dict rows) runs the retrieval helpers.
    """
    from nomoscope_workflow import pipeline

    from .runner import load_case_record

    out = GoldenCaseDerivation()
    for case in golden:
        if not case.expected.citations:
            out.skipped[case.id] = "no expected citation"
            continue
        if case.expected.routing in _NO_RETRIEVAL_ROUTINGS:
            out.skipped[case.id] = f"routing {case.expected.routing.value}: nothing is retrieved"
            continue
        if case.corpus_available is False:
            out.skipped[case.id] = "corpus_available=false"
            continue
        try:
            record = load_case_record(params_conn, case.parameter_target)
            country = record.information.country
            lang = retrieval.LANG_BY_COUNTRY.get(country, "en")
            as_of = pipeline._retrieval_as_of(record, case.as_of)
            region = regions.region_key(country, record.information.model_target)
            scope = retrieval.jurisdiction_scope(conn, country, region)
            framed = pipeline.frame_query(wf_cfg, record, case.as_of)
            expected = resolve_citations(conn, list(case.expected.citations), scope, lang, as_of)
        except Exception as exc:  # noqa: BLE001 - report it, keep building the rest
            params_conn.rollback()
            conn.rollback()
            out.skipped[case.id] = f"{exc.__class__.__name__}: {exc}"
            continue
        if not expected:
            out.skipped[case.id] = (
                f"no pinpoint citation in the searched corpus ({'; '.join(case.expected.citations)} "
                f"in {'/'.join(scope)} {lang} at {as_of})"
            )
            continue
        out.cases.append(
            EmbeddingCase(
                id=f"{GOLDEN_CASE_PREFIX}{case.id}",
                country=country,
                language=lang,
                as_of=as_of,
                query=framed["query"],
                region=region,
                expected_citations=expected,
                verified=case.verified,
                drafted_by=f"golden:{case.id}",
                notes=f"framed from {case.parameter_target}; golden citations: "
                + "; ".join(case.expected.citations),
            )
        )
    return out


# --------------------------------------------------------------------------- #
# Side-by-side comparison
# --------------------------------------------------------------------------- #

_LATEST_RUNS_SQL = """
SELECT DISTINCT ON ((manifest->>'embedding_model_id')::int)
       run_id, manifest, results
FROM eval.embedding_runs
WHERE (%(dataset)s::text IS NULL OR manifest->>'dataset_version' = %(dataset)s)
ORDER BY (manifest->>'embedding_model_id')::int, (manifest->>'created_at') DESC
"""


def latest_runs(conn: psycopg.Connection, dataset_version: str | None = None) -> list[dict]:
    """The most recent embedding run of every model (optionally on one case set)."""
    with conn.cursor(row_factory=dict_row) as cur:
        return cur.execute(_LATEST_RUNS_SQL, {"dataset": dataset_version}).fetchall()


def compare_runs(runs: list[dict], method: str = "vector") -> list[dict[str, str]]:
    """One row per (model, language, all): `method`'s metrics from each run.

    Only cases present in EVERY run are compared, so a model is never credited
    or blamed for a case another model was not asked.
    """
    if not runs:
        return []
    shared = set.intersection(*({r["case_id"] for r in run["results"]} for run in runs))
    rows: list[dict[str, str]] = []
    for run in runs:
        manifest = run["manifest"]
        name = manifest.get("embedding_model") or f"model {manifest['embedding_model_id']}"
        results = [
            EmbeddingCaseResult.model_validate(r) for r in run["results"] if r["case_id"] in shared
        ]
        groups: dict[str, list[EmbeddingCaseResult]] = defaultdict(list)
        for result in results:
            groups[result.language].append(result)
            groups["all"].append(result)
        for lang, group in sorted(groups.items(), key=lambda item: (item[0] == "all", item[0])):
            ranks = [r.ranks[method] for r in group if method in r.ranks]
            metrics = rank_metrics(ranks, group[0].k)
            if metrics:
                rows.append({"model": name, "lang": lang, **metrics})
    return rows


def _git_commit() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        return None
