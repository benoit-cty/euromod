"""eval.runs.eval_version names the scoring rules that produced a run's rows."""

from __future__ import annotations

import hashlib
import re

from nomokrisis_eval import EVAL_VERSION, SCORING_PY, eval_version, scoring_hash


def test_the_version_carries_a_hash_of_the_scoring_source():
    expected = hashlib.sha256(SCORING_PY.read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:8]
    assert eval_version() == f"{EVAL_VERSION}+scoring.{expected}"
    assert re.fullmatch(r"\d+\.\d+\.\d+\+scoring\.[0-9a-f]{8}", eval_version())


def test_the_hash_is_deterministic_and_moves_with_any_edit(tmp_path):
    original = tmp_path / "scoring.py"
    original.write_bytes(b"TOLERANCE = 1e-9\n")
    windows = tmp_path / "scoring_crlf.py"
    windows.write_bytes(b"TOLERANCE = 1e-9\r\n")
    edited = tmp_path / "scoring_edited.py"
    edited.write_bytes(b"TOLERANCE = 1e-6\n")
    assert scoring_hash(original) == scoring_hash(original) == scoring_hash(windows)
    assert scoring_hash(original) != scoring_hash(edited)


def test_the_hand_bump_is_past_the_version_that_hid_eight_scoring_changes():
    assert EVAL_VERSION != "0.1.0"
