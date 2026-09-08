"""Golden-set loading: every committed case must parse, and filters must work."""

from __future__ import annotations

from pathlib import Path

from nomokrisis_eval.dataset import dataset_version, load_cases

DATASET_DIR = Path(__file__).resolve().parents[1] / "dataset"


def test_committed_cases_parse():
    cases = load_cases(DATASET_DIR)
    assert len(cases) >= 2
    # FR is drafted from the OpenFisca corpus, IE, LT, ES and NL from their
    # curated selection files; each case sits in dataset/<country>/ (save_case).
    assert {c.country for c in cases} <= {"FR", "IE", "LT", "ES", "NL"}
    assert all(
        (DATASET_DIR / c.country.lower() / f"{c.id}.json").exists() for c in cases
    )


def test_every_case_points_at_a_parameter_file():
    """A case whose parameter file is missing fails only at run time, one case in."""
    repo_root = DATASET_DIR.parents[1]
    missing = [c.id for c in load_cases(DATASET_DIR) if not (repo_root / c.parameter_file).exists()]
    assert not missing, f"parameter_file missing for {missing}"


def test_filters():
    assert load_cases(DATASET_DIR, countries=["fr"]) == load_cases(DATASET_DIR, countries=["FR"])
    assert load_cases(DATASET_DIR, languages=["de"]) == []
    verified = load_cases(DATASET_DIR, verified_only=True)
    assert all(c.verified for c in verified)


def test_dataset_version_is_stable():
    assert dataset_version(DATASET_DIR) == dataset_version(DATASET_DIR)
    assert len(dataset_version(DATASET_DIR)) == 12
