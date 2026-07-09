"""Tests for ingestion CLI wiring."""

from __future__ import annotations

from typer.testing import CliRunner

from euromod_ingest.cli import app


def test_embeddings_build_help_exposes_backend_option() -> None:
    """Operators can select Torch or OpenVINO from the embedding command."""
    result = CliRunner().invoke(app, ["embeddings", "build", "--help"])

    assert result.exit_code == 0
    assert "--backend" in result.output
    assert "torch or openvino" in result.output