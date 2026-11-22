"""The retrieval eval's candidate set is search_chunks()' own (dev DB)."""

from __future__ import annotations

from datetime import date

import pytest
from nomokrisis_eval.embedding_eval import _CANDIDATE_CTE, _CANDIDATES_SQL

SCOPE = {"jurisdictions": ["FR"], "lang": "fr", "as_of": date(2025, 7, 1)}


def test_every_chunk_search_chunks_ranks_is_a_counted_candidate(db):
    try:
        hits = db.execute(
            "SELECT chunk_id FROM search_chunks(%s, NULL, 0, %s, %s, %s, 200)",
            ("plafond taux montant", ["FR"], ["fr"], SCOPE["as_of"]),
        ).fetchall()
    except Exception as exc:  # an older database without search_chunks()
        pytest.skip(f"search_chunks() unavailable: {exc}")
    if not hits:
        pytest.skip("no FR corpus in the dev DB")
    candidates = {row[0] for row in db.execute(_CANDIDATE_CTE + "SELECT chunk_id FROM candidate", SCOPE).fetchall()}
    assert {row[0] for row in hits} <= candidates
    chunks, embedded = db.execute(_CANDIDATES_SQL, {**SCOPE, "model_id": 1}).fetchone()
    assert chunks == len(candidates) and 0 <= embedded <= chunks
