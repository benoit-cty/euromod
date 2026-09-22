"""import-golden on a temp copy of real files: dry run resolves, the real run
upserts (twice, idempotently), rows carry the file's verdict."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from nomokrisis_eval import golden_store
from nomokrisis_eval.import_golden import import_golden, read_selection_files

from conftest import TEST_PREFIX

EVAL_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def temp_golden(tmp_path: Path) -> Path:
    """Two real cases (one scalar, one group), one real curated selection and
    one embedding case, copied with zz_test_/ZZ identities."""
    src_cases = [
        EVAL_ROOT / "dataset" / "fr" / "fr_constdef_pss_2025-06-01.json",
        EVAL_ROOT / "dataset" / "es" / "es_tin_capinc_schedule_2025-06-01.json",
    ]
    for path in src_cases:
        if not path.exists():
            pytest.skip(f"on-disk golden set already removed: {path}")
    dataset = tmp_path / "dataset"
    for path in src_cases:
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["id"] = TEST_PREFIX + payload["id"]
        folder = dataset / path.parent.name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{payload['id']}.json").write_text(json.dumps(payload), encoding="utf-8")
    # A third case whose file is gone and whose id matches no selection entry.
    orphan = json.loads(src_cases[0].read_text(encoding="utf-8"))
    orphan["id"] = TEST_PREFIX + "orphan_2025-06-01"
    orphan["parameter_file"] = "Nomoscope-agentic-workflow/data/parameters/eval/does_not_exist.json"
    (dataset / "fr" / f"{orphan['id']}.json").write_text(json.dumps(orphan), encoding="utf-8")

    sources = tmp_path / "golden_sources"
    sources.mkdir()
    selection = json.loads((EVAL_ROOT / "golden_sources" / "es.json").read_text(encoding="utf-8"))
    selection["country"] = "ZZ"
    (sources / "zz.json").write_text(json.dumps(selection), encoding="utf-8")

    embedding = tmp_path / "dataset_embedding" / "fr"
    embedding.mkdir(parents=True)
    emb = json.loads((EVAL_ROOT / "dataset_embedding" / "fr" / "fr_pss_2025.json").read_text(encoding="utf-8"))
    emb["id"] = TEST_PREFIX + emb["id"]
    (embedding / f"{emb['id']}.json").write_text(json.dumps(emb), encoding="utf-8")
    return tmp_path


def test_selection_files_read_kind_and_header():
    if not (EVAL_ROOT / "golden_sources").exists():
        pytest.skip("golden_sources/ already removed")
    rows = {(country, kind): (header, entries) for country, kind, header, entries in read_selection_files(EVAL_ROOT / "golden_sources")}
    assert ("FR", "openfisca") in rows and ("FR", "curated") in rows
    header, entries = rows[("FR", "openfisca")]
    assert "entries" not in header and header["corpus"] == "openfisca" and entries


def test_dry_run_then_import_twice(db, temp_golden: Path):
    kwargs = dict(
        dataset_dir=temp_golden / "dataset",
        embedding_dataset_dir=temp_golden / "dataset_embedding",
        sources_dir=temp_golden / "golden_sources",
    )
    dry = import_golden(db, dry_run=True, **kwargs)
    assert (dry.selections, dry.cases, dry.embedding_cases) == (1, 2, 1)
    assert len(dry.unresolved) == 1 and "orphan" in dry.unresolved[0]
    assert dry.resolved_by.get("materialized file") == 2
    assert golden_store.load_case(db, TEST_PREFIX + "fr_constdef_pss_2025-06-01") is None
    with pytest.raises(KeyError):
        golden_store.load_selection(db, "ZZ", "curated")

    for _ in range(2):  # idempotent
        report = import_golden(db, **kwargs)
        assert (report.selections, report.cases, report.cases_verified, report.embedding_cases) == (1, 2, 2, 1)

    pss = golden_store.load_case(db, TEST_PREFIX + "fr_constdef_pss_2025-06-01")
    assert pss.parameter_target == "euromod://FR/ConstDef_fr/def_const/$PSS"
    assert pss.verified and pss.reviewed_by == "ben" and pss.reviewed_at is not None

    group = golden_store.load_case(db, TEST_PREFIX + "es_tin_capinc_schedule_2025-06-01")
    assert group.parameter_target == "group:ES:tin_cons_es:tin_capinc_schedule"
    assert isinstance(group.expected.value, list) and len(group.expected.value) == 5

    header, entries = golden_store.load_selection(db, "ZZ", "curated")
    assert header["corpus"] == "curated" and "entries" not in header and len(entries) >= 10
    emb = [c for c in golden_store.load_embedding_cases(db, countries=["FR"]) if c.id.startswith(TEST_PREFIX)]
    assert len(emb) == 1 and emb[0].expected_citations == ["JORFTEXT000050854392, art. 1"]
