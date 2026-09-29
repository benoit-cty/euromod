"""Embedding-eval unit tests: rank/metric arithmetic is right, the set hash is stable.

No database needed — the DB-touching paths (vector_search, run_embedding_eval,
eval.embedding_cases round trips) are exercised in test_golden_store.py against
the dev stack and by `nomokrisis-eval run-embeddings`.
"""

from __future__ import annotations

from datetime import date

from nomoscope_workflow.schema import RetrievalHit

from nomokrisis_eval.embedding_eval import first_relevant_rank, rank_metrics
from nomokrisis_eval.golden_store import embedding_set_hash
from nomokrisis_eval.schema import EmbeddingCase
from nomokrisis_eval.scoring import citation_equal


def _hit(citation: str) -> RetrievalHit:
    return RetrievalHit(chunk_id="00000000-0000-0000-0000-000000000000", citation=citation)


def _case(case_id: str = "fr_pss_2025", verified: bool = False) -> EmbeddingCase:
    return EmbeddingCase(
        id=case_id,
        country="FR",
        language="fr",
        as_of=date(2025, 6, 1),
        query="plafond de la sécurité sociale 2025",
        expected_citations=["JORFTEXT000050854392, art. 1"],
        verified=verified,
    )


def test_citation_equal_is_strict():
    assert citation_equal("CGI, art. 197", "cgi art 197")
    # containment must NOT match: 'art. 2' is a prefix of 'art. 20' once normalised
    assert not citation_equal("JORFTEXT000051168007, art. 2", "JORFTEXT000051168007, art. 20")
    assert not citation_equal("CGI, art. 197", None)
    assert not citation_equal("CGI, art. 197", "CGI")


def test_first_relevant_rank():
    hits = [_hit("CGI, art. 224"), _hit("CGI, art. 197"), _hit("CGI, art. 1417")]
    assert first_relevant_rank(["CGI, art. 197"], hits) == 2
    assert first_relevant_rank(["CGI, art. 224", "CGI, art. 197"], hits) == 1
    assert first_relevant_rank(["CGI, art. 999"], hits) is None
    assert first_relevant_rank(["CGI, art. 197"], []) is None


def test_rank_metrics():
    metrics = rank_metrics([1, 2, None, 4], k=10)
    assert metrics["cases"] == "4"
    assert metrics["hit@1"] == "25%"
    assert metrics["hit@10"] == "75%"
    assert metrics["hit@3"] == "50%"
    assert metrics["mrr"] == f"{(1 + 0.5 + 0 + 0.25) / 4:.2f}"
    assert rank_metrics([], k=10) == {}


def test_embedding_set_hash_ignores_the_verdict_and_the_order():
    a, b = _case("a"), _case("b")
    assert len(embedding_set_hash([a, b])) == 12
    assert embedding_set_hash([a, b]) == embedding_set_hash([b, a])
    assert embedding_set_hash([a, b]) == embedding_set_hash([_case("a", verified=True), b])
    assert embedding_set_hash([a]) != embedding_set_hash([a, b])


class _Rows:
    """A connection stub answering the in-scope units query."""

    def __init__(self, rows: list[tuple[str, str]]):
        self.rows = [{"citation": c, "context_header": h} for c, h in rows]

    def execute(self, *_args):
        return self

    def fetchall(self):
        return self.rows


def test_resolve_citations_prefers_the_exact_article():
    from nomokrisis_eval.embedding_eval import resolve_citations

    conn = _Rows([
        ("CGI, art. 197", "Code général des impôts > CGI, art. 197"),
        ("CGI, art. 197 A", "Code général des impôts > CGI, art. 197 A"),
        ("Wet IB 2001, artikel 2.10a", "Wet inkomstenbelasting 2001 > artikel 2.10a"),
    ])
    assert resolve_citations(conn, ["CGI, art. 197"], ["FR"], "fr", date(2025, 7, 1)) == ["CGI, art. 197"]
    # No exact match: the main eval's containment rule, against the header too.
    assert resolve_citations(conn, ["artikel 2.10a"], ["NL"], "nl", date(2025, 6, 1)) == [
        "Wet IB 2001, artikel 2.10a"
    ]


def test_resolve_citations_drops_instrument_level_citations():
    from nomokrisis_eval.embedding_eval import resolve_citations

    conn = _Rows([(f"VSDĮ {n} straipsnis", f"VSDĮ > {n} straipsnis") for n in range(1, 10)]
                 + [("GPMĮ 6 straipsnis", "GPMĮ > 6 straipsnis")])
    # "VSDĮ" names every article of the act: any hit would count, so it is dropped.
    assert resolve_citations(conn, ["VSDĮ", "GPMĮ 6 straipsnis"], ["LT"], "lt", date(2025, 6, 1)) == [
        "GPMĮ 6 straipsnis"
    ]


def _run(model: str, model_id: int, ranks: dict[str, int | None]) -> dict:
    return {
        "run_id": f"run-{model}",
        "manifest": {"embedding_model": model, "embedding_model_id": model_id},
        "results": [
            {"case_id": case_id, "country": "FR", "language": "fr", "corpus_lang": "fr", "k": 15,
             "ranks": {"vector": rank}}
            for case_id, rank in ranks.items()
        ],
    }


def test_compare_runs_scores_only_the_cases_every_run_has():
    from nomokrisis_eval.embedding_eval import compare_runs

    rows = compare_runs([
        _run("bge-m3", 1, {"a": 1, "b": None, "c": 2}),
        _run("qwen3", 2, {"a": 2, "b": 1}),  # never asked c
    ])
    by_model = {(r["model"], r["lang"]): r for r in rows}
    assert by_model[("bge-m3", "all")]["cases"] == "2"
    assert by_model[("bge-m3", "all")]["hit@1"] == "50%"
    assert by_model[("qwen3", "all")]["hit@1"] == "50%"
    assert by_model[("qwen3", "fr")]["mrr"] == f"{(0.5 + 1) / 2:.2f}"
