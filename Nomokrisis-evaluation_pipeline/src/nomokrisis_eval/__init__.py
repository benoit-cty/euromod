"""EUROMOD Activity 4 evaluation pipeline: golden dataset + KPI runs."""

from __future__ import annotations

import hashlib
from pathlib import Path

#: Bumped by hand when the meaning of a stored result changes. Rows written
#: under 0.1.0 (until 17 Nov 2026) cannot say which scoring rules produced
#: them: scoring.py changed on eight dates under that one number.
EVAL_VERSION = "0.2.0"

SCORING_PY = Path(__file__).with_name("scoring.py")


def scoring_hash(path: Path = SCORING_PY) -> str:
    """First 8 hex digits of the SHA-256 of scoring.py's source — moves with
    every edit to the scoring rules, whether or not anyone bumped EVAL_VERSION.
    Line endings are normalised so a Windows checkout hashes the same."""
    source = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(source).hexdigest()[:8]


def eval_version() -> str:
    """What eval.runs.eval_version records: `<EVAL_VERSION>+scoring.<hash>`,
    e.g. `0.2.0+scoring.1a2b3c4d`. Two runs with the same string were scored
    by the same rules."""
    return f"{EVAL_VERSION}+scoring.{scoring_hash()}"
