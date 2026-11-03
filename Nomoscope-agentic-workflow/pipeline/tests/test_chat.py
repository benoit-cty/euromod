"""The RAG chat turn (rag-ui): quote verification, history, and a live mock run."""

from __future__ import annotations

from datetime import date

import pytest
from pydantic_ai.messages import ModelRequest, ModelResponse

from nomoscope_workflow import chat, retrieval
from nomoscope_workflow.config import load_config

CHUNK_A = "11111111-1111-1111-1111-111111111111"
CHUNK_B = "22222222-2222-2222-2222-222222222222"


@pytest.fixture
def fake_verify(monkeypatch):
    def install(contents: dict[str, str]):
        def verify(conn, chunk_id, extract):
            content = contents.get(chunk_id)
            if content is None or not extract:
                return None
            idx = content.find(extract)
            return (idx, idx + len(extract)) if idx >= 0 else None

        monkeypatch.setattr(retrieval, "verify_extract", verify)

    return install


def test_a_verbatim_quote_is_verified(fake_verify) -> None:
    fake_verify({CHUNK_A: "Le taux est fixé à 11 % pour la fraction supérieure à 11 497 €."})
    out = chat.resolve_quote(None, chat.Quote(chunk_id=CHUNK_A, extract="11 % pour la fraction"), {})
    assert out["verified"] and out["chunk_id"] == CHUNK_A and out["resolved_from"] is None


def test_a_paraphrase_is_flagged_not_dropped(fake_verify) -> None:
    fake_verify({CHUNK_A: "Le taux est fixé à 11 %."})
    out = chat.resolve_quote(None, chat.Quote(chunk_id=CHUNK_A, extract="the rate is 11%"), {})
    assert out["verified"] is False and out["chunk_id"] == CHUNK_A


def test_a_wrong_chunk_id_is_resolved_by_its_extract_when_unambiguous(fake_verify) -> None:
    contents = {CHUNK_A: "autre texte", CHUNK_B: "Le plafond est fixé à 47 100 euros."}
    fake_verify(contents)
    sources = {cid: {"content": text} for cid, text in contents.items()}
    out = chat.resolve_quote(None, chat.Quote(chunk_id=CHUNK_A, extract="fixé à 47 100 euros"), sources)
    assert out["verified"] and out["chunk_id"] == CHUNK_B and out["resolved_from"] == CHUNK_A


def test_two_candidate_chunks_keep_the_quote_unverified(fake_verify) -> None:
    text = "Le plafond est fixé à 47 100 euros."
    fake_verify({CHUNK_A: text, CHUNK_B: text})
    sources = {CHUNK_A: {"content": text}, CHUNK_B: {"content": text}}
    out = chat.resolve_quote(None, chat.Quote(chunk_id="not-a-uuid", extract="47 100 euros"), sources)
    assert out["verified"] is False


def test_history_carries_earlier_quotes_so_a_follow_up_can_name_them() -> None:
    messages = [
        chat.ChatMessage(role="user", content="barème ?"),
        chat.ChatMessage(role="assistant", content="Voir [1].", quotes=[{"chunk_id": CHUNK_A, "citation": "CGI art. 197", "extract": "11 %"}]),
    ]
    history = chat._history(messages)
    assert isinstance(history[0], ModelRequest) and isinstance(history[1], ModelResponse)
    assert CHUNK_A in history[1].parts[0].content and "CGI art. 197" in history[1].parts[0].content


def test_a_request_must_end_with_a_user_question() -> None:
    with pytest.raises(ValueError):
        chat.ChatRequest(messages=[chat.ChatMessage(role="assistant", content="hi")])


def test_mock_turn_runs_the_tool_loop_against_the_corpus() -> None:
    cfg = load_config()
    cfg.embedding_model_id = 99  # FTS + in-SQL placeholder: no encoder needed
    try:
        retrieval.connect(cfg).close()
    except Exception as exc:  # no stack up: this test is opt-in by environment
        pytest.skip(f"legislation DB unreachable: {exc}")
    request = chat.ChatRequest(
        messages=[chat.ChatMessage(role="user", content="impôt sur le revenu barème")],
        country="FR",
        as_of=date(2025, 6, 1),
        model="mock/chat",
        web=False,
    )
    result = chat.run_turn(cfg, request)
    assert result["sources"], "the mock searched and found nothing — is FR ingested?"
    assert result["quotes"] and all(q["verified"] for q in result["quotes"])
    source_ids = {s["chunk_id"] for s in result["sources"]}
    assert {q["chunk_id"] for q in result["quotes"]} <= source_ids
    assert all(s["source_trust_class"] != "context" for s in result["sources"])
