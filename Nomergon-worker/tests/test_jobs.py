"""Payload validation and argv composition for every job type (no DB, no subprocess)."""

from __future__ import annotations

import json
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


def test_every_subprocess_payload_maps_itself_to_an_argv() -> None:
    for spec in jobs.JOB_SPECS.values():
        if not spec.in_process:
            assert spec.payload.to_argv is not jobs._Payload.to_argv, spec.name


def test_build_command_refuses_another_types_payload(cfg: WorkerConfig) -> None:
    with pytest.raises(TypeError, match="ImpactPayload"):
        jobs.build_command("impact", jobs.parse_payload("embed", {}), cfg)


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


def test_workflow_include_na(cfg: WorkerConfig) -> None:
    assert "--include-na" not in build("workflow", {"targets": ["x"], "year": 2025}, cfg)
    argv = build("workflow", {"targets": ["x"], "year": 2025, "include_na": True}, cfg)
    assert argv[-1] == "--include-na"


def test_workflow_needs_a_target_and_a_year() -> None:
    with pytest.raises(ValueError):
        jobs.parse_payload("workflow", {"targets": [], "year": 2025})
    with pytest.raises(ValueError):
        jobs.parse_payload("workflow", {"targets": ["euromod://FR/x"]})


def test_workflow_country_runs_run_country(cfg: WorkerConfig) -> None:
    argv = build("workflow", {"country": "FR", "year": 2025, "limit": 5, "model": "mock/extractor"}, cfg)
    assert argv[3:] == ["run-country", "FR", "--year", "2025", "--limit", "5", "--model", "mock/extractor"]


def test_workflow_takes_targets_or_a_country_not_both() -> None:
    with pytest.raises(ValueError):
        jobs.parse_payload("workflow", {"targets": ["x"], "country": "FR", "year": 2025})
    with pytest.raises(ValueError):
        jobs.parse_payload("workflow", {"targets": ["x"], "limit": 3, "year": 2025})


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


DOCUMENT_ARGS = [
    "https://www.urssaf.fr/circulaire-2025.pdf",
    "--jurisdiction", "fr",
    "--lang", "fr",
    "--title", "Circulaire 2025-01",
    "--kind", "circulaire",
    "--valid-from", "2025-04-01",
    "--implements", "JORFTEXT000051168007",
    "--progress-json",
]  # fmt: skip


def test_ingest_document_legacy_args_give_the_same_argv(cfg: WorkerConfig) -> None:
    """IngestTab.documentArgs(): read through the allow-list, rebuilt identically."""
    argv = build("ingest", {"command": "document", "args": DOCUMENT_ARGS}, cfg)
    assert argv[3:] == ["document", *DOCUMENT_ARGS, "--database-url", DB]


def test_ingest_typed_payloads(cfg: WorkerConfig) -> None:
    typed = {
        "command": "document",
        "source": "https://www.urssaf.fr/circulaire-2025.pdf",
        "jurisdiction": "fr",
        "lang": "fr",
        "title": "Circulaire 2025-01",
        "kind": "circulaire",
        "valid_from": "2025-04-01",
        "implements": "JORFTEXT000051168007",
    }
    assert build("ingest", typed, cfg)[3:] == ["document", *DOCUMENT_ARGS, "--database-url", DB]
    citation = {"command": "citation", "jurisdiction": "fr", "citation": "CGI art. 197", "as_of": "2025-06-01", "max_items": 50}
    assert build("ingest", citation, cfg)[3:] == [
        "citation", "fr", "CGI art. 197", "2025-06-01", "--max-items", "50", "--database-url", DB,
    ]  # fmt: skip
    legacy = ["fr", "CGI art. 197", "2025-06-01", "--source-code", "FR-LEGI", "--max-items", "50"]
    assert build("ingest", {"command": "citation", "args": legacy}, cfg)[3:] == [
        "citation", *legacy, "--database-url", DB,
    ]  # fmt: skip
    instrument = {"command": "instrument", "jurisdiction": "fr", "national_id": "KALITEXT000005678", "source_code": "FR-KALI"}
    assert build("ingest", instrument, cfg)[3:] == [
        "instrument", "fr", "KALITEXT000005678", "--source-code", "FR-KALI", "--database-url", DB,
    ]  # fmt: skip


def test_ingest_route_with_and_without_a_source(cfg: WorkerConfig) -> None:
    assert build("ingest", {"command": "route", "args": []}, cfg)[3:] == ["route", "--database-url", DB]
    assert build("ingest", {"command": "route"}, cfg)[3:] == ["route", "--database-url", DB]
    url = "https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000051168007"
    assert build("ingest", {"command": "route", "args": [url]}, cfg)[3:] == ["route", url, "--database-url", DB]


def test_ingest_refuses_commands_outside_the_contract() -> None:
    with pytest.raises(ValueError):
        jobs.parse_payload("ingest", {"command": "reparse", "args": []})
    with pytest.raises(ValueError):
        jobs.parse_payload("ingest", {"command": "reparse", "jurisdiction": "fr"})


@pytest.mark.parametrize(
    "args",
    [
        ["fr", "JORFTEXT000051168007", "--database-url", "postgresql://evil/db"],
        ["fr", "JORFTEXT000051168007", "-d", "postgresql://evil/db"],
        ["fr", "JORFTEXT000051168007", "--max-items=5"],
        ["fr", "JORFTEXT000051168007", "--trigger", "cache_miss"],
        ["fr", "JORFTEXT000051168007", "extra-positional"],
        ["fr", "JORFTEXT000051168007", "--max-items"],
        ["fr", "JORFTEXT000051168007", "--max-items", "lots"],
        ["fr"],
    ],
)
def test_ingest_legacy_args_outside_the_allow_list_are_refused(args: list[str]) -> None:
    with pytest.raises(ValueError):
        jobs.parse_payload("ingest", {"command": "instrument", "args": args})


def test_ingest_document_refuses_unlisted_flags_and_mixed_forms() -> None:
    with pytest.raises(ValueError, match="not allowed"):
        jobs.parse_payload("ingest", {"command": "document", "args": [*DOCUMENT_ARGS, "--trigger", "cache_miss"]})
    with pytest.raises(ValueError, match="either args"):
        jobs.parse_payload("ingest", {"command": "route", "args": [], "source": "https://x"})
    with pytest.raises(ValueError, match="needs valid_from"):
        jobs.parse_payload("ingest", {"command": "document", "args": DOCUMENT_ARGS[:9]})
    with pytest.raises(ValueError, match="takes no national_id"):
        jobs.parse_payload("ingest", {"command": "route", "national_id": "x"})
    with pytest.raises(ValueError, match="must not start"):
        jobs.parse_payload("ingest", {"command": "instrument", "jurisdiction": "fr", "national_id": "--help"})


def test_ingest_files_only_from_the_document_dir(cfg: WorkerConfig, tmp_path: Path) -> None:
    """A path would let a submitter load the worker's own files (its keys) into the corpus."""
    for source in ("/proc/self/environ", "notes.md"):
        payload = jobs.parse_payload("ingest", {"command": "route", "source": source})
        with pytest.raises(ValueError, match="http"):
            jobs.build_command("ingest", payload, cfg)
    cfg.document_dir = tmp_path / "contributed"
    inside = jobs.parse_payload("ingest", {"command": "route", "source": "ani-apec-2011.md"})
    assert jobs.build_command("ingest", inside, cfg)[4] == str((tmp_path / "contributed" / "ani-apec-2011.md").resolve())
    for source in ("../.env", "/proc/self/environ"):
        outside = jobs.parse_payload("ingest", {"command": "route", "source": source})
        with pytest.raises(ValueError, match="under WORKER_DOCUMENT_DIR"):
            jobs.build_command("ingest", outside, cfg)


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


def test_embed_candidate_model_loads_its_own_weights(cfg: WorkerConfig) -> None:
    # The configured path holds BGE-M3; a registry candidate must not be built from it.
    argv = build("embed", {"model_id": 2, "precision": "fp16", "authentic_only": True}, cfg)
    assert "--model-path" not in argv
    assert argv[argv.index("--precision") + 1] == "fp16"
    assert "--authentic-only" in argv


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


# -------------------------------------------------------------------- chat --


def test_chat_writes_the_conversation_to_a_scratch_file(cfg: WorkerConfig, tmp_path: Path) -> None:
    messages = [
        {"role": "user", "content": "Quel est le barème 2025 ?"},
        {"role": "assistant", "content": "Voir [1].", "quotes": [{"chunk_id": "c1", "extract": "11 %"}]},
        {"role": "user", "content": "Et pour 2026 ?"},
    ]
    argv = build("chat", {"messages": messages, "country": "FR", "as_of": "2026-01-01"}, cfg, scratch_dir=tmp_path)
    assert argv == [sys.executable, "-m", "nomoscope_workflow.cli", "chat", str(tmp_path / "chat.json")]
    written = json.loads((tmp_path / "chat.json").read_text(encoding="utf-8"))
    assert written["messages"][1]["quotes"] == [{"chunk_id": "c1", "extract": "11 %"}]
    assert written["country"] == "FR" and written["web"] is True
    assert jobs.package_dir("chat", cfg) == cfg.pipeline_dir


def test_chat_must_end_with_a_question() -> None:
    with pytest.raises(ValueError, match="last message"):
        jobs.parse_payload("chat", {"messages": [{"role": "assistant", "content": "hello"}]})
    with pytest.raises(ValueError, match="last message"):
        jobs.parse_payload("chat", {"messages": [{"role": "user", "content": "  "}]})
    with pytest.raises(ValueError):
        jobs.parse_payload("chat", {"messages": []})


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
    instrument = jobs.parse_payload("ingest", {"command": "instrument", "args": ["fr", "JORFTEXT000051168007"]})
    assert jobs.extract_result("ingest", instrument, result_line=None, last_progress=None, stdout_tail=['{"x": 1}']) is None
    impact = jobs.parse_payload("impact", {})
    assert jobs.extract_result("impact", impact, result_line=None, last_progress=None, stdout_tail=['{"total_kwh": 0.1}']) == {"total_kwh": 0.1}
    assert jobs.extract_result("translate-params", jobs.parse_payload("translate-params", {"country": "FR"}), result_line=None, last_progress=progress, stdout_tail=[]) is None
    chat = jobs.parse_payload("chat", {"messages": [{"role": "user", "content": "q"}]})
    assert jobs.extract_result("chat", chat, result_line={"answer": "a"}, last_progress=progress, stdout_tail=[]) == {"answer": "a"}


def test_workflow_model_is_published_first_and_once() -> None:
    from nomergon.config import published_models

    assert published_models("azure_openai/gpt-5.6-sol", "jrc/mistral, azure_openai/gpt-5.6-sol,") == [
        "azure_openai/gpt-5.6-sol",
        "jrc/mistral",
    ]
    assert published_models("", "jrc/mistral") == ["jrc/mistral"]
    assert published_models("", "") == []
