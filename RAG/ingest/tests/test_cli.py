"""Tests for ingestion CLI wiring."""

from __future__ import annotations

from typer.testing import CliRunner

from euromod_ingest.cli import app


def test_embeddings_build_help_exposes_backend_option() -> None:
    """Operators can select Torch or OpenVINO from the embedding command."""
    result = CliRunner().invoke(app, ["embeddings", "build", "--help"])

    assert result.exit_code == 0
    assert "--backend" in result.output
    assert "--progress" in result.output
    assert "torch" in result.output
    assert "openvino" in result.output


def test_embedding_progress_status_mentions_encoding_batch() -> None:
    """Progress status exposes batch-level movement during slow model calls."""
    from euromod_ingest.cli import _embedding_progress_status

    status = _embedding_progress_status(
        {"phase": "encoding", "scanned": 32, "embedded": 16, "batch_size": 16},
        dry_run=False,
    )

    assert "encoding batch=16" in status
    assert "embedded=16" in status