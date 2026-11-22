"""How the ingest package is spawned: uv or the worker's interpreter, CPU or GPU."""

from __future__ import annotations

from pathlib import Path

from nomoscope_workflow import scout_ingest
from nomoscope_workflow.config import WorkflowConfig
from nomoscope_workflow.query_encoder import embedding_process
from nomoscope_workflow.scout_ingest import _embedding_model_args


def _ingest_package(tmp_path: Path, *, cuda: bool) -> Path:
    """Build a minimal ingest package layout, optionally with the GPU environment."""
    directory = tmp_path / "ingest"
    directory.mkdir()
    (directory / "pyproject.toml").write_text("")
    if cuda:
        (directory / ".venv-cuda").mkdir()
        (directory / ".venv-cuda" / "pyvenv.cfg").write_text("home = /usr/bin\n")
    return directory


def test_embedding_process_stays_on_the_cpu_environment_by_default(tmp_path: Path, monkeypatch) -> None:
    """Without .venv-cuda the spawn is exactly the CPU/OpenVINO invocation."""
    monkeypatch.delenv("UV_PROJECT_ENVIRONMENT", raising=False)
    monkeypatch.delenv("NOMOS_PYTHON", raising=False)
    directory = _ingest_package(tmp_path, cuda=False)

    spec = embedding_process(directory, "nomotheca_ingest.query_embeddings")

    assert spec.cuda is False
    assert spec.command == [
        "uv",
        "run",
        "--extra",
        "embeddings",
        "python",
        "-m",
        "nomotheca_ingest.query_embeddings",
    ]
    assert "UV_PROJECT_ENVIRONMENT" not in spec.env


def test_embedding_process_prefers_the_installed_cuda_environment(tmp_path: Path, monkeypatch) -> None:
    """An installed .venv-cuda routes the subprocess to the GPU wheels."""
    monkeypatch.delenv("UV_PROJECT_ENVIRONMENT", raising=False)
    monkeypatch.delenv("NOMOS_PYTHON", raising=False)
    directory = _ingest_package(tmp_path, cuda=True)

    spec = embedding_process(directory, "nomotheca_ingest.cli", "embeddings", "build")

    assert spec.cuda is True
    assert spec.command[:5] == ["uv", "run", "--extra", "embeddings-cuda", "python"]
    assert spec.command[-3:] == ["nomotheca_ingest.cli", "embeddings", "build"]
    assert spec.env["UV_PROJECT_ENVIRONMENT"] == str(directory / ".venv-cuda")
    assert "VIRTUAL_ENV" not in spec.env
    assert spec.cwd == directory


def test_embedding_process_uses_nomos_python_in_the_current_directory(tmp_path: Path, monkeypatch) -> None:
    """Inside the worker the spawn is its interpreter, -m module, here: no uv, no ingest-dir walk."""
    monkeypatch.setenv("NOMOS_PYTHON", "/opt/worker/bin/python")
    monkeypatch.setenv("VIRTUAL_ENV", "/somewhere/.venv")
    monkeypatch.chdir(tmp_path)
    directory = _ingest_package(tmp_path, cuda=True)  # would pick CUDA on the uv path

    spec = embedding_process(None, "nomotheca_ingest.cli", "embeddings", "build")

    assert spec.command == ["/opt/worker/bin/python", "-m", "nomotheca_ingest.cli", "embeddings", "build"]
    assert spec.cwd == Path.cwd()
    assert spec.cuda is False
    assert "VIRTUAL_ENV" not in spec.env
    assert "UV_PROJECT_ENVIRONMENT" not in spec.env
    # the walk-based directory is ignored even when it exists
    assert embedding_process(directory, "nomotheca_ingest.query_embeddings").command[0] == "/opt/worker/bin/python"


def test_scout_ingest_uses_nomos_python(tmp_path: Path, monkeypatch) -> None:
    """The scout's archive-first ingest follows the same switch."""
    monkeypatch.setenv("NOMOS_PYTHON", "/opt/worker/bin/python")
    monkeypatch.chdir(tmp_path)
    calls: list[dict] = []

    class _Done:
        returncode = 0
        stdout = stderr = ""

    def fake_run(command, **kwargs):
        calls.append({"command": command, **kwargs})
        return _Done()

    monkeypatch.setattr(scout_ingest.subprocess, "run", fake_run)
    cfg = WorkflowConfig(database_url="postgresql://u@h/db")

    args = scout_ingest.instrument_args(cfg, "FR", "JORFTEXT000051168007")
    assert scout_ingest.run_ingest_cli(cfg, args, "JORFTEXT000051168007") is None
    assert calls[0]["command"] == [
        "/opt/worker/bin/python",
        "-m",
        "nomotheca_ingest.cli",
        "instrument",
        "fr",
        "JORFTEXT000051168007",
        "--database-url",
        "postgresql://u@h/db",
    ]
    assert calls[0]["cwd"] == Path.cwd()
    assert "VIRTUAL_ENV" not in calls[0]["env"]

    assert scout_ingest.build_embeddings(cfg) is None
    assert calls[1]["command"] == [
        "/opt/worker/bin/python",
        "-m",
        "nomotheca_ingest.cli",
        "embeddings",
        "build",
        "--database-url",
        "postgresql://u@h/db",
        "--no-progress",
    ]


def test_embedding_model_args_never_send_the_openvino_export_to_the_gpu(tmp_path: Path) -> None:
    """The OpenVINO IR only loads under the OpenVINO backend, never under Torch."""
    directory = _ingest_package(tmp_path, cuda=True)
    (directory / "models").mkdir()
    (directory / "models" / "bge-m3-openvino").mkdir()

    assert _embedding_model_args(directory, cuda=True) == []
    assert _embedding_model_args(directory, cuda=False) == [
        "--backend",
        "openvino",
        "--model-path",
        "models/bge-m3-openvino",
    ]

    torch_model = directory / "models" / "bge-m3"
    torch_model.mkdir()
    (torch_model / "config.json").write_text("{}")
    assert _embedding_model_args(directory, cuda=True) == ["--model-path", "models/bge-m3"]
