"""Embedding-eval unit tests: committed cases parse, rank/metric arithmetic is right.

No database needed — the DB-touching paths (vector_search, run_embedding_eval)
are exercised by `nomokrisis-eval run-embeddings` against the live stack.
"""

from __future__ import annotations

from pathlib import Path

from nomoscope_workflow.schema import RetrievalHit

from nomokrisis_eval.dataset import dataset_version, load_embedding_cases
from nomokrisis_eval.embedding_eval import first_relevant_rank, rank_metrics
from nomokrisis_eval.scoring import citation_equal

DATASET_DIR = Path(__file__).resolve().parents[1] / "dataset_embedding"


def _hit(citation: str) -> RetrievalHit:
    return RetrievalHit(chunk_id="00000000-0000-0000-0000-000000000000", citation=citation)


def test_committed_embedding_cases_parse():
    cases = load_embedding_cases(DATASET_DIR)
    assert len(cases) >= 10
    assert {c.country for c in cases} >= {"FR", "BE", "ES", "IE", "NL", "LT"}
    assert all(c.expected_citations for c in cases)
    # ids are unique — they double as result keys and dataset filenames
    assert len({c.id for c in cases}) == len(cases)


def test_filters_and_cross_lingual_default():
    assert load_embedding_cases(DATASET_DIR, countries=["fr"]) == load_embedding_cases(
        DATASET_DIR, countries=["FR"]
    )
    assert load_embedding_cases(DATASET_DIR, languages=["de"]) == []
    xlingual = [c for c in load_embedding_cases(DATASET_DIR) if c.corpus_lang]
    assert any(c.language != c.corpus_lang for c in xlingual)


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
    assert metrics["mrr"] == f"{(1 + 0.5 + 0 + 0.25) / 4:.2f}"
    assert rank_metrics([], k=10) == {}


def test_dataset_version_covers_embedding_dir():
    assert len(dataset_version(DATASET_DIR)) == 12
    assert dataset_version(DATASET_DIR) == dataset_version(DATASET_DIR)
