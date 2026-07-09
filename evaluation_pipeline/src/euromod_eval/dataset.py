"""Load/save golden cases: one JSON file per case under dataset/<country>/."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .schema import GoldenCase


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
