"""Reranker registry and JSON-lines protocol, without loading a model."""

from __future__ import annotations

import pytest

from nomotheca_ingest.core.rerankers import get_reranker
from nomotheca_ingest.rerank import handle_request


class _FakeReranker:
    def score(self, query: str, passages: list[str]) -> list[float]:
        return [float(len(p)) for p in passages]


def test_plain_cross_encoder_pairs_are_the_raw_texts():
    assert get_reranker("bge-reranker-v2-m3").pair("barème", "Art. 197") == ("barème", "Art. 197")


def test_qwen3_pairs_carry_the_chat_template_and_the_task():
    query, document = get_reranker("qwen3-reranker-0.6b").pair("barème", "Art. 197")
    assert "<Instruct>: Given the description of a tax-benefit parameter" in query
    assert query.endswith("<Query>: barème\n")
    assert document.startswith("<Document>: Art. 197") and document.endswith("</think>\n\n")


def test_handle_request_scores_every_passage():
    assert handle_request(_FakeReranker(), {"query": "q", "passages": ["a", "bbb"]}) == {"scores": [1.0, 3.0]}
    assert handle_request(_FakeReranker(), {"query": "q", "passages": []}) == {"scores": []}
    with pytest.raises(ValueError):
        handle_request(_FakeReranker(), {"query": " ", "passages": ["a"]})
    with pytest.raises(ValueError):
        handle_request(_FakeReranker(), {"query": "q", "passages": "a"})


def test_unknown_reranker_names_the_known_ones():
    with pytest.raises(KeyError, match="bge-reranker-v2-m3"):
        get_reranker("nope")
