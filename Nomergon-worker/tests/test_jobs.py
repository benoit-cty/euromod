"""Payload validation and argv composition for every job type (no DB, no subprocess)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from nomergon import jobs
from nomergon.config import WorkerConfig

DB = "postgresql://jrc:secret@db:5432/legislation"


@pytest.fixture
def cfg(tmp_path: Path) -> WorkerConfig:
    return WorkerConfig(
        repo_root=tmp_path,
        database_url=DB,
        models=["jrc/mistral-small", "mock/extractor"],
        embedding_model_path="/models/bge-m3",
    )


def build(job_type: str, payload: dict, cfg: WorkerConfig, **kwargs) -> list[str]:
    return jobs.build_command(job_type, jobs.parse_payload(job_type, payload), cfg, **kwargs)


def test_every_contract_job_type_has_a_payload_model() -> None:
    assert set(jobs.PAYLOAD_MODELS) == set(jobs.JOB_TYPES)


def test_unknown_job_type_is_refused_by_name() -> None:
    with pytest.raises(ValueError, match="rm-rf"):
        jobs.parse_payload("rm-rf", {})


def test_unknown_payload_keys_are_refused() -> None:
    with pytest.raises(ValueError, match="extra"):
        jobs.parse_payload("impact", {"projct": "x"})


# ---------------------------------------------------------------- workflow --


def test_workflow_argv(cfg: WorkerConfig) -> None:
    argv = build(
        "workflow",
        {"targets": ["euromod://FR/tin_fr/def_const/$tinrt_cdhr", "group:FR:tinkt_fr:tin_schedule"], "year": 2025},
        cfg,
    )
    assert argv == [
        sys.executable,
        "-m",
        "nomoscope_workflow.cli",
        "run-targets",
        "euromod://FR/tin_fr/def_const/$tinrt_cdhr",
        "group:FR:tinkt_fr:tin_schedule",
        "--year",
        "2025",
    ]
    assert jobs.package_dir("workflow", cfg) == cfg.pipeline_dir


def test_workflow_model_and_force(cfg: WorkerConfig) -> None:
    argv = build("workflow", {"targets": ["euromod://FR/x"], "year": 2024, "model": "mock/extractor", "force": True}, cfg)
    assert argv[-5:] == ["--year", "2024", "--model", "mock/extractor", "--force"]


def test_workflow_needs_a_target_and_a_year() -> None:
    with pytest.raises(ValueError):
        jobs.parse_payload("workflow", {"targets": [], "year": 2025})
    with pytest.raises(ValueError):
        jobs.parse_payload("workflow", {"targets": ["euromod://FR/x"]})


# ------------------------------------------------------------------ ingest --


def test_ingest_argv_puts_the_database_url_last(cfg: WorkerConfig) -> None:
    argv = build("ingest", {"command": "instrument", "args": ["fr", "JORFTEXT000051168007", "--max-items", "500"]}, cfg)
    assert argv == [
        sys.executable,
        "-m",
        "nomotheca_ingest.cli",
        "instrument",
        "fr",
        "JORFTEXT000051168007",
        "--max-items",
        "500",
        "--database-url",
        DB,
    ]
    assert jobs.package_dir("ingest", cfg) == cfg.ingest_dir


def test_ingest_document_args_pass_through_untouched(cfg: WorkerConfig) -> None:
    args = ["/tmp/circulaire.pdf", "--jurisdiction", "fr", "--kind", "circulaire", "--valid-from", "2025-04-01", "--progress-json"]
    argv = build("ingest", {"command": "document", "args": args}, cfg)
    assert argv[3] == "document"
    assert argv[4 : 4 + len(args)] == args
    assert argv[-2:] == ["--database-url", DB]


def test_ingest_refuses_commands_outside_the_contract() -> None:
    with pytest.raises(ValueError):
        jobs.parse_payload("ingest", {"command": "reparse", "args": []})


# ------------------------------------------------------------------- embed --


def test_embed_argv(cfg: WorkerConfig) -> None:
    argv = build("embed", {}, cfg)
    assert argv == [
        sys.executable,
        "-m",
        "nomotheca_ingest.cli",
        "embeddings",
        "build",
        "--backend",
        "torch",
        "--model-path",
        "/models/bge-m3",
        "--model-id",
        "1",
        "--batch-size",
        "16",
        "--progress-json",
        "--database-url",
        DB,
    ]


def test_embed_limit_and_dry_run(cfg: WorkerConfig) -> None:
    argv = build("embed", {"model_id": 2, "batch_size": 8, "limit": 100, "dry_run": True}, cfg)
    assert "--limit" in argv and argv[argv.index("--limit") + 1] == "100"
    assert "--dry-run" in argv
    assert argv[argv.index("--model-id") + 1] == "2"
    assert argv[argv.index("--batch-size") + 1] == "8"
    assert argv[-2:] == ["--database-url", DB]


# --------------------------------------------------------------- translate --


def test_translate_argv(cfg: WorkerConfig) -> None:
    argv = build("translate", {"model": "openrouter/google/gemma-4-31b-it:free", "target_lang": "en"}, cfg)
    assert argv[:5] == [sys.executable, "-m", "nomotheca_ingest.cli", "translate", "run"]
    assert argv[argv.index("--model") + 1] == "openrouter/google/gemma-4-31b-it:free"
    assert argv[argv.index("--target-lang") + 1] == "en"
    assert argv[argv.index("--request-timeout") + 1] == "120"
    assert "--progress-json" in argv
    assert "--limit" not in argv and "--dry-run" not in argv
    assert argv[-2:] == ["--database-url", DB]


def test_translate_optional_flags(cfg: WorkerConfig) -> None:
    argv = build("translate", {"model": "m", "limit": 5, "request_timeout": 0, "dry_run": True}, cfg)
    assert argv[argv.index("--limit") + 1] == "5"
    assert argv[argv.index("--request-timeout") + 1] == "0"
    assert "--dry-run" in argv


def test_translate_needs_a_model() -> None:
    with pytest.raises(ValueError):
        jobs.parse_payload("translate", {"target_lang": "en"})


# -------------------------------------------------------- translate-params --


def test_translate_params_argv(cfg: WorkerConfig) -> None:
    argv = build(
        "translate-params",
        {"country": "FR", "lang": "fr", "model": "mock/extractor", "batch_size": 20, "limit": 10, "force": True},
        cfg,
    )
    assert argv == [
        sys.executable,
        "-m",
        "nomoscope_workflow.cli",
        "translate-params",
        "--country",
        "FR",
        "--lang",
        "fr",
        "--model",
        "mock/extractor",
        "--batch-size",
        "20",
        "--limit",
        "10",
        "--force",
    ]
    assert jobs.package_dir("translate-params", cfg) == cfg.pipeline_dir


def test_translate_params_minimal(cfg: WorkerConfig) -> None:
    argv = build("translate-params", {"country": "LT"}, cfg)
    assert argv[3:] == ["translate-params", "--country", "LT", "--batch-size", "20"]


# -------------------------------------------------------------------- eval --


def test_eval_run_argv(cfg: WorkerConfig) -> None:
    argv = build(
        "eval",
        {
            "as_of": "2025-06-01",
            "model": "mock/extractor",
            "countries": ["FR", "ES"],
            "languages": ["fr"],
            "include_drafts": True,
            "notes": "smoke",
        },
        cfg,
    )
    assert argv == [
        sys.executable,
        "-m",
        "nomokrisis_eval.cli",
        "run",
        "--as-of",
        "2025-06-01",
        "--model",
        "mock/extractor",
        "--country",
        "FR",
        "--country",
        "ES",
        "--language",
        "fr",
        "--include-drafts",
        "--notes",
        "smoke",
    ]
    assert jobs.package_dir("eval", cfg) == cfg.eval_dir


def test_eval_resume_argv(cfg: WorkerConfig) -> None:
    argv = build("eval", {"resume": "20260909-1438-abc"}, cfg)
    assert argv[3:] == ["resume", "20260909-1438-abc"]


def test_eval_needs_as_of_and_model_or_resume() -> None:
    with pytest.raises(ValueError, match="resume"):
        jobs.parse_payload("eval", {"as_of": "2025-06-01"})
    with pytest.raises(ValueError, match="resume"):
        jobs.parse_payload("eval", {"model": "mock/extractor"})


# ------------------------------------------------------------ draft-golden --


def test_draft_golden_openfisca_argv(cfg: WorkerConfig) -> None:
    argv = build("draft-golden", {"source": "openfisca", "country": "FR", "year": 2025}, cfg)
    assert argv[3:] == [
        "build-openfisca-dataset",
        "--country",
        "FR",
        "--year",
        "2025",
        "--limit",
        "50",
        "--fill",
    ]
    assert jobs.package_dir("draft-golden", cfg) == cfg.eval_dir


def test_draft_golden_openfisca_curated_only_and_as_of(cfg: WorkerConfig) -> None:
    argv = build(
        "draft-golden",
        {"source": "openfisca", "country": "FR", "year": 2025, "as_of": "2025-06-01", "limit": 10, "fill": False},
        cfg,
    )
    assert argv[argv.index("--as-of") + 1] == "2025-06-01"
    assert argv[-3:] == ["--limit", "10", "--curated-only"]


def test_draft_golden_curated_argv(cfg: WorkerConfig) -> None:
    argv = build("draft-golden", {"source": "curated", "country": "IE", "year": 2025}, cfg)
    assert argv[3:] == ["build-curated-dataset", "--country", "IE", "--year", "2025"]


def test_draft_golden_document_writes_the_text_to_a_scratch_file(cfg: WorkerConfig, tmp_path: Path) -> None:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    argv = build(
        "draft-golden",
        {
            "source": "document",
            "country": "FR",
            "as_of": "2025-06-01",
            "language": "fr",
            "targets": ["euromod://FR/a", "euromod://FR/b"],
            "text": "Le montant est de 100 €.\n",
            "model": "mock/extractor",
        },
        cfg,
        scratch_dir=scratch,
    )
    assert argv[3] == "build-dataset"
    document = Path(argv[4])
    assert document.parent == scratch
    assert document.read_text(encoding="utf-8") == "Le montant est de 100 €.\n"
    assert argv[5:] == [
        "--country",
        "FR",
        "--as-of",
        "2025-06-01",
        "--language",
        "fr",
        "--target",
        "euromod://FR/a",
        "--target",
        "euromod://FR/b",
        "--model",
        "mock/extractor",
    ]


def test_draft_golden_document_without_scratch_uses_a_temp_file(cfg: WorkerConfig) -> None:
    argv = build("draft-golden", {"source": "document", "country": "FR", "as_of": "2025-06-01", "text": "x"}, cfg)
    document = Path(argv[4])
    try:
        assert document.is_file()
        assert document.read_text(encoding="utf-8") == "x"
    finally:
        document.unlink(missing_ok=True)


def test_draft_golden_validation() -> None:
    with pytest.raises(ValueError, match="year"):
        jobs.parse_payload("draft-golden", {"source": "openfisca", "country": "FR"})
    with pytest.raises(ValueError, match="as_of"):
        jobs.parse_payload("draft-golden", {"source": "document", "country": "FR", "text": "x"})
    with pytest.raises(ValueError, match="text"):
        jobs.parse_payload("draft-golden", {"source": "document", "country": "FR", "as_of": "2025-06-01", "text": "  "})


# ------------------------------------------------------------------ impact --


def test_impact_argv(cfg: WorkerConfig) -> None:
    assert build("impact", {}, cfg) == [sys.executable, "-m", "nomoscope_workflow.cli", "impact", "--json"]
    argv = build("impact", {"project": "nomoscope", "since": "2026-09-01", "until": "2026-09-10", "zone": "WOR"}, cfg)
    assert argv[5:] == ["--project", "nomoscope", "--since", "2026-09-01", "--until", "2026-09-10", "--zone", "WOR"]
    assert jobs.package_dir("impact", cfg) == cfg.pipeline_dir


# ------------------------------------------------------------------ encode --


def test_encode_is_in_process(cfg: WorkerConfig) -> None:
    payload = jobs.parse_payload("encode", {"query": "barème de l'impôt", "sentences": ["a", "b"]})
    with pytest.raises(ValueError, match="in-process"):
        jobs.build_command("encode", payload, cfg)
    with pytest.raises(ValueError, match="empty"):
        jobs.parse_payload("encode", {"query": "   "})
    with pytest.raises(ValueError):
        jobs.package_dir("encode", cfg)


# ----------------------------------------------------------------- results --


def test_result_per_job_type(cfg: WorkerConfig) -> None:
    progress = {"phase": "done", "embedded": 3}
    result = {"item_ids": ["FR_x_2025"]}
    assert jobs.extract_result("workflow", jobs.parse_payload("workflow", {"targets": ["x"], "year": 2025}), result_line=result, last_progress=None, stdout_tail=[]) == result
    assert jobs.extract_result("embed", jobs.parse_payload("embed", {}), result_line=None, last_progress=progress, stdout_tail=[]) == progress
    route = jobs.parse_payload("ingest", {"command": "route", "args": ["https://x"]})
    assert jobs.extract_result("ingest", route, result_line=None, last_progress=None, stdout_tail=["noise", '{"outcome": {"kind": "adapter"}}']) == {"outcome": {"kind": "adapter"}}
    instrument = jobs.parse_payload("ingest", {"command": "instrument", "args": []})
    assert jobs.extract_result("ingest", instrument, result_line=None, last_progress=None, stdout_tail=['{"x": 1}']) is None
    impact = jobs.parse_payload("impact", {})
    assert jobs.extract_result("impact", impact, result_line=None, last_progress=None, stdout_tail=['{"total_kwh": 0.1}']) == {"total_kwh": 0.1}
    assert jobs.extract_result("translate-params", jobs.parse_payload("translate-params", {"country": "FR"}), result_line=None, last_progress=progress, stdout_tail=[]) is None
