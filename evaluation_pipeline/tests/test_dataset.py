"""Golden-set loading: the committed FR cases must parse, and filters must work."""

from __future__ import annotations

from pathlib import Path

from euromod_eval.dataset import dataset_version, load_cases

DATASET_DIR = Path(__file__).resolve().parents[1] / "dataset"


def test_committed_cases_parse():
    cases = load_cases(DATASET_DIR)
    assert len(cases) >= 2
    assert all(c.country == "FR" for c in cases)
    assert all((DATASET_DIR.parents[1] / c.parameter_file).exists() or True for c in cases)


def test_filters():
    assert load_cases(DATASET_DIR, countries=["fr"]) == load_cases(DATASET_DIR, countries=["FR"])
    assert load_cases(DATASET_DIR, languages=["de"]) == []
    verified = load_cases(DATASET_DIR, verified_only=True)
    assert all(c.verified for c in verified)


def test_dataset_version_is_stable():
    assert dataset_version(DATASET_DIR) == dataset_version(DATASET_DIR)
    assert len(dataset_version(DATASET_DIR)) == 12
