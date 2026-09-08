"""Embedding (retrieval) evaluation: rank ground-truth chunks under each search leg.

Isolates the Activity 2 retrieval layer from the LLM workflow: each case is a
search query plus the citation(s) of the legal unit(s) a correct retriever must
surface. Every case is scored under three methods over the same as-of/country/
lang candidate set the production pipeline uses (Country Reports excluded):

  fts     FTS-only leg (nomoscope_workflow.retrieval.hybrid_search, no vector)
  vector  pure cosine ranking over `embeddings` — the number that moves when
          the embedding model/backend changes; this is the embedding eval proper
  hybrid  the production RRF fusion (what the workflow actually retrieves with)

Scoring is pure rank arithmetic — hit@1, hit@k, MRR — with strict normalised
citation equality (see scoring.citation_equal), no LLM anywhere. Query encoding
reuses the workflow's BGE-M3 subprocess encoder; `--embedding-model-id 99`
selects the in-SQL placeholder embedder for key-less, encoder-less demos.
"""

from __future__ import annotations

import subprocess
import uuid
from collections import defaultdict
from datetime import datetime, timezone

import psycopg
from psycopg.rows import dict_row

from nomoscope_workflow import retrieval
from nomoscope_workflow.schema import RetrievalHit

from . import EVAL_VERSION
from .config import REPO_ROOT, EvalConfig
from .dataset import dataset_version
from .schema import EmbeddingCase, EmbeddingCaseResult
from .scoring import citation_equal

# Same candidate filter as retrieval.py's hybrid CTE: in force at as_of, one
# jurisdiction+lang, Country Reports excluded (they describe the model, not the
# law — retrieving one can never be a "relevant" outcome).
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
  AND i.instrument_type <> 'country_report'
ORDER BY e.embedding <=> {qexpr}
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
  AND i.instrument_type <> 'country_report'
"""

METHODS = ("fts", "vector", "hybrid")


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
    """hit@1 / hit@k / MRR over one method's ranks (misses count as 0 reciprocal rank)."""
    n = len(ranks)
    if n == 0:
        return {}
    return {
        "cases": str(n),
        "hit@1": f"{100 * sum(1 for r in ranks if r == 1) / n:.0f}%",
        f"hit@{k}": f"{100 * sum(1 for r in ranks if r is not None) / n:.0f}%",
        "mrr": f"{sum(1 / r for r in ranks if r) / n:.2f}",
    }


def run_embedding_eval(
    cfg: EvalConfig,
    cases: list[EmbeddingCase],
    k: int = 10,
    embedding_model_id: int = 1,
    notes: str | None = None,
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
        "k": k,
        "eval_version": EVAL_VERSION,
        "dataset_version": dataset_version(cfg.embedding_dataset_dir),
        "git_commit": _git_commit(),
        "countries": sorted({c.country for c in cases}),
        "cases": len(cases),
        "notes": notes,
    }

    results: list[EmbeddingCaseResult] = []
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
                    qvec = query_encoder.encode(case.query)
                if embedding_model_id == 99 or qvec is not None:
                    vec_hits = vector_search(*common, embedding_model_id, k, qvec)
                    result.ranks["vector"] = first_relevant_rank(case.expected_citations, vec_hits)
                    hyb_hits = retrieval.hybrid_search(
                        *common, model_id=embedding_model_id, k=k, query_vector=qvec
                    )
                    result.ranks["hybrid"] = first_relevant_rank(case.expected_citations, hyb_hits)
                else:
                    result.error = "query encoder unavailable — vector/hybrid not scored"
            except Exception as exc:  # score the failure, keep the run going
                result.error = f"{exc.__class__.__name__}: {exc}"
                conn.rollback()
            results.append(result)
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


def _git_commit() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        return None
