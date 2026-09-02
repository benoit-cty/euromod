"""Load/save golden cases: one JSON file per case under dataset/<country>/.

Embedding (retrieval) cases follow the same one-file-per-case layout under
dataset_embedding/<country>/ — a separate tree because load_cases rglobs every
JSON below its root."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .schema import EmbeddingCase, GoldenCase


def load_cases(
    dataset_dir: Path,
    countries: list[str] | None = None,
    languages: list[str] | None = None,
    verified_only: bool = False,
) -> list[GoldenCase]:
    cases: list[GoldenCase] = []
    for path in sorted(dataset_dir.rglob("*.json")):
        case = GoldenCase.model_validate_json(path.read_text(encoding="utf-8"))
        if countries and case.country.upper() not in {c.upper() for c in countries}:
            continue
        if languages and case.language.lower() not in {l.lower() for l in languages}:
            continue
        if verified_only and not case.verified:
            continue
        cases.append(case)
    return cases


def save_case(dataset_dir: Path, case: GoldenCase) -> Path:
    folder = dataset_dir / case.country.lower()
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{case.id}.json"
    path.write_text(case.model_dump_json(indent=2, exclude_none=True) + "\n", encoding="utf-8")
    return path


#: What a reviewer actually approved. Everything else a drafter writes (notes,
#: drafted_by, corpus_available) is provenance that can be refreshed freely.
def _ground_truth(case: GoldenCase) -> str:
    return json.dumps(
        {
            "expected": case.expected.model_dump(mode="json"),
            "parameter_file": case.parameter_file,
            "as_of": case.as_of.isoformat(),
        },
        sort_keys=True,
    )


def save_drafted_case(dataset_dir: Path, case: GoldenCase) -> tuple[Path, bool]:
    """Write a freshly drafted case, carrying the human verdict over when the
    ground truth did not change.

    Drafters always emit `verified: false`. Writing that blindly would discard
    every review each time the set is rebuilt — and a golden set nobody dares
    rebuild stops tracking the parameter store. Keeping the verdict blindly is
    worse: a changed expectation would inherit approval of a different value.
    So the verdict survives exactly when the ground truth (`expected`, the
    parameter under test, `as_of`) is identical to what the reviewer approved,
    and is dropped the moment any of it moves.

    Returns (path, reset), reset=True when a previous verdict was dropped.
    """
    folder = dataset_dir / case.country.lower()
    path = folder / f"{case.id}.json"
    reset = False
    if path.exists():
        try:
            previous = GoldenCase.model_validate_json(path.read_text(encoding="utf-8"))
        except ValueError:
            previous = None
        if previous is not None and (previous.verified or previous.reviewed_by):
            if _ground_truth(previous) == _ground_truth(case):
                case.verified = previous.verified
                case.reviewed_by = previous.reviewed_by
                case.review_note = previous.review_note
            else:
                reset = True
    return save_case(dataset_dir, case), reset


def load_embedding_cases(
    dataset_dir: Path,
    countries: list[str] | None = None,
    languages: list[str] | None = None,
    verified_only: bool = False,
) -> list[EmbeddingCase]:
    cases: list[EmbeddingCase] = []
    for path in sorted(dataset_dir.rglob("*.json")):
        case = EmbeddingCase.model_validate_json(path.read_text(encoding="utf-8"))
        if countries and case.country.upper() not in {c.upper() for c in countries}:
            continue
        if languages and case.language.lower() not in {l.lower() for l in languages}:
            continue
        if verified_only and not case.verified:
            continue
        cases.append(case)
    return cases


def save_embedding_case(dataset_dir: Path, case: EmbeddingCase) -> Path:
    folder = dataset_dir / case.country.lower()
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{case.id}.json"
    path.write_text(case.model_dump_json(indent=2, exclude_none=True) + "\n", encoding="utf-8")
    return path


def dataset_version(dataset_dir: Path) -> str:
    """Deterministic fingerprint of the golden set (content hash of every case file)."""
    digest = hashlib.sha256()
    for path in sorted(dataset_dir.rglob("*.json")):
        digest.update(path.relative_to(dataset_dir).as_posix().encode())
        # Normalise whitespace/key order so cosmetic re-saves don't bump the version.
        digest.update(
            json.dumps(json.loads(path.read_text(encoding="utf-8")), sort_keys=True).encode()
        )
    return digest.hexdigest()[:12]
