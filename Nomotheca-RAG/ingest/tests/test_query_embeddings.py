"""The Database tab's JSON-lines query encoder protocol."""

from __future__ import annotations

import pytest

from nomotheca_ingest.query_embeddings import handle_request


class FakeBackend:
    """Deterministic unit vectors: the query is (1, 0), sentences rotate away from it."""

    def encode(self, inputs):
        vectors = []
        for text in inputs:
            if text == "query":
                vectors.append([1.0, 0.0])
            elif text == "same":
                vectors.append([1.0, 0.0])
            elif text == "orthogonal":
                vectors.append([0.0, 1.0])
            else:
                vectors.append([0.6, 0.8])
        return vectors


def test_query_only_returns_halfvec(monkeypatch):
    monkeypatch.setattr("nomotheca_ingest.query_embeddings.halfvec_literal", lambda v: str(v))
    response = handle_request(FakeBackend(), {"query": "query"})
    assert response == {"halfvec": "[1.0, 0.0]"}


def test_sentences_return_cosine_against_query():
    response = handle_request(FakeBackend(), {"query": "query", "sentences": ["same", "orthogonal", "other"]})
    assert response["similarities"] == pytest.approx([1.0, 0.0, 0.6])


def test_empty_sentences_are_fine():
    assert handle_request(FakeBackend(), {"query": "query", "sentences": []}) == {"similarities": []}


@pytest.mark.parametrize("request_", [{"query": "  "}, {"query": "query", "sentences": "not a list"}, {"query": "query", "sentences": [1]}])
def test_bad_requests_raise(request_):
    with pytest.raises(ValueError):
        handle_request(FakeBackend(), request_)
