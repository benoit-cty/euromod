"""Tests for ingestion CLI wiring."""

from __future__ import annotations

import json

from typer.testing import CliRunner

from nomotheca_ingest.cli import PROGRESS_PREFIX, app

# Rich truncates long option names at the default 80-column width; render help
# wide so assertions see full flag names regardless of how many options exist.
WIDE = {"COLUMNS": "200"}


def test_embeddings_build_help_exposes_backend_option() -> None:
    """Operators can select Torch or OpenVINO from the embedding command."""
    result = CliRunner().invoke(app, ["embeddings", "build", "--help"], env=WIDE)

    assert result.exit_code == 0
    assert "--backend" in result.output
    assert "--progress" in result.output
    assert "torch" in result.output
    assert "openvino" in result.output


def test_both_batch_commands_expose_progress_json() -> None:
    """Wrapping UIs can request machine-readable progress lines."""
    for command in (["embeddings", "build"], ["translate", "run"]):
        result = CliRunner().invoke(app, [*command, "--help"], env=WIDE)

        assert result.exit_code == 0
        assert "--progress-json" in result.output


def test_translation_json_progress_emits_prefixed_json(capsys) -> None:
    """Each translation event becomes one parseable '@progress' stdout line."""
    from nomotheca_ingest.cli import _translation_json_progress

    update = _translation_json_progress(total=10)
    update({"phase": "translated", "scanned": 3, "translated": 2, "failed": 1, "detail": "CGI art. 197"})

    out = capsys.readouterr().out.strip()
    assert out.startswith(PROGRESS_PREFIX)
    payload = json.loads(out[len(PROGRESS_PREFIX):])
    assert payload == {
        "task": "translate",
        "phase": "translated",
        "done": 3,
        "total": 10,
        "translated": 2,
        "failed": 1,
        "detail": "CGI art. 197",
    }


def test_embedding_json_progress_skips_per_chunk_candidate_events(capsys) -> None:
    """Only batch-level events are emitted, so stdout stays small on big corpora."""
    from nomotheca_ingest.cli import _embedding_json_progress

    update = _embedding_json_progress(total=100)
    update({"phase": "candidate", "scanned": 1, "embedded": 0, "batch_size": 1})
    update({"phase": "embedded", "scanned": 16, "embedded": 16, "batch_size": 16})

    lines = capsys.readouterr().out.strip().splitlines()
    assert len(lines) == 1
    payload = json.loads(lines[0][len(PROGRESS_PREFIX):])
    assert payload["task"] == "embeddings"
    assert payload["done"] == 16
    assert payload["total"] == 100


def test_translate_run_help_exposes_request_timeout_option() -> None:
    """Operators can bound slow or stuck provider calls."""
    result = CliRunner().invoke(app, ["translate", "run", "--help"], env=WIDE)

    assert result.exit_code == 0
    assert "--request-timeout" in result.output
    assert "Per-provider-request timeout" in result.output


def test_embedding_progress_status_mentions_encoding_batch() -> None:
    """Progress status exposes batch-level movement during slow model calls."""
    from nomotheca_ingest.cli import _embedding_progress_status

    status = _embedding_progress_status(
        {"phase": "encoding", "scanned": 32, "embedded": 16, "batch_size": 16},
        dry_run=False,
    )

    assert "encoding batch=16" in status
    assert "embedded=16" in status