"""The small helpers every corpus lookup shares (code audit 4)."""

from __future__ import annotations

from nomoscope_workflow.corpus import add_unseen, located


def _row(chunk_id: str) -> dict:
    return {"chunk_id": chunk_id, "citation": f"art. {chunk_id}", "content": "x"}


def test_add_unseen_skips_seen_chunks_marks_kept_ones_and_stops_at_the_cap():
    seen = {"a"}
    kept = add_unseen(located(_row(c) for c in ["a", "b", "b", "c", "d"]), seen, cap=2)

    assert [h.chunk_id for h in kept] == ["b", "c"]
    assert all(h.method == "located" for h in kept)
    assert seen == {"a", "b", "c"}  # "d" was past the cap: still unseen
    assert add_unseen(located([_row("e")]), seen, cap=0) == []
    assert [h.chunk_id for h in add_unseen(located(_row(c) for c in "bde"), seen)] == ["d", "e"]
