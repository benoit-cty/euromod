"""Job types: one payload model per type, and the argv each one runs.

This is the whole mapping from "what the UI described" to "what the worker
executes", kept as pure functions so it can be tested without a database or
a subprocess. The table it implements is `.scratch/nomergon-worker/contracts.md`.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .config import WorkerConfig

INGEST_MODULE = "nomotheca_ingest.cli"
WORKFLOW_MODULE = "nomoscope_workflow.cli"
EVAL_MODULE = "nomokrisis_eval.cli"

JOB_TYPES = (
    "workflow",
    "ingest",
    "embed",
    "translate",
    "translate-params",
    "encode",
    "eval",
    "draft-golden",
    "impact",
)
#: Job types answered in-process by the encode lane, never as a subprocess.
IN_PROCESS_JOB_TYPES = ("encode",)
ENCODE_PRIORITY = 100


class _Payload(BaseModel):
    model_config = ConfigDict(extra="forbid")


class WorkflowPayload(_Payload):
    targets: list[str] = Field(min_length=1)
    year: int
    model: str | None = None
    force: bool = False


class IngestPayload(_Payload):
    command: Literal["instrument", "citation", "document", "route"]
    #: Exactly what the UI built today (``IngestTab.buildRequest``), minus ``--database-url``.
    args: list[str] = Field(default_factory=list)


class EmbedPayload(_Payload):
    model_id: int = 1
    batch_size: int = Field(default=16, ge=1)
    limit: int | None = Field(default=None, ge=1)
    dry_run: bool = False


class TranslatePayload(_Payload):
    model: str
    target_lang: str = "en"
    limit: int | None = Field(default=None, ge=1)
    request_timeout: float = Field(default=120, ge=0)
    dry_run: bool = False


class TranslateParamsPayload(_Payload):
    country: str
    lang: str | None = None
    model: str | None = None
    batch_size: int = Field(default=20, ge=1)
    limit: int | None = Field(default=None, ge=1)
    force: bool = False


class EncodePayload(_Payload):
    query: str
    sentences: list[str] | None = None

    @model_validator(mode="after")
    def _query_not_blank(self) -> EncodePayload:
        if not self.query.strip():
            msg = "query must not be empty"
            raise ValueError(msg)
        return self


class EvalPayload(_Payload):
    """A new run (``as_of`` + ``model``) or the continuation of one (``resume``)."""

    resume: str | None = None
    as_of: str | None = None
    model: str | None = None
    countries: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    include_drafts: bool = False
    notes: str | None = None

    @model_validator(mode="after")
    def _new_run_or_resume(self) -> EvalPayload:
        if self.resume is None and (not self.as_of or not self.model):
            msg = "an eval job needs either resume=<run_id> or both as_of and model"
            raise ValueError(msg)
        return self


class DraftGoldenPayload(_Payload):
    source: Literal["openfisca", "curated", "document"]
    country: str
    year: int | None = None
    as_of: str | None = None
    limit: int = Field(default=50, ge=1)
    fill: bool = True
    language: str | None = None
    targets: list[str] = Field(default_factory=list)
    text: str | None = None
    model: str | None = None

    @model_validator(mode="after")
    def _fields_for_source(self) -> DraftGoldenPayload:
        if self.source in ("openfisca", "curated") and self.year is None:
            msg = f"draft-golden from {self.source} needs a year"
            raise ValueError(msg)
        if self.source == "document":
            if not self.as_of:
                msg = "draft-golden from a document needs as_of"
                raise ValueError(msg)
            if not self.text or not self.text.strip():
                msg = "draft-golden from a document needs the document text"
                raise ValueError(msg)
        return self


class ImpactPayload(_Payload):
    project: str = ""
    since: str | None = None
    until: str | None = None
    zone: str = ""


PAYLOAD_MODELS: dict[str, type[_Payload]] = {
    "workflow": WorkflowPayload,
    "ingest": IngestPayload,
    "embed": EmbedPayload,
    "translate": TranslatePayload,
    "translate-params": TranslateParamsPayload,
    "encode": EncodePayload,
    "eval": EvalPayload,
    "draft-golden": DraftGoldenPayload,
    "impact": ImpactPayload,
}


def parse_payload(job_type: str, payload: dict[str, Any] | None) -> _Payload:
    """Validate a job's payload against its type's model (``ValueError`` on a bad one)."""
    try:
        model = PAYLOAD_MODELS[job_type]
    except KeyError:
        msg = f"unknown job type: {job_type!r} (one of {', '.join(JOB_TYPES)})"
        raise ValueError(msg) from None
    return model.model_validate(payload or {})


def package_dir(job_type: str, cfg: WorkerConfig) -> Path:
    """The sub-project a job runs from (its cwd), so its relative paths resolve."""
    if job_type in ("ingest", "embed", "translate"):
        return cfg.ingest_dir
    if job_type in ("workflow", "translate-params", "impact"):
        return cfg.pipeline_dir
    if job_type in ("eval", "draft-golden"):
        return cfg.eval_dir
    msg = f"{job_type} does not run as a subprocess"
    raise ValueError(msg)


def _python(module: str) -> list[str]:
    return [sys.executable, "-m", module]


def build_command(
    job_type: str,
    payload: _Payload,
    cfg: WorkerConfig,
    *,
    scratch_dir: Path | None = None,
) -> list[str]:
    """The argv for one job, always ``sys.executable -m <module> …``.

    The ingest CLIs take the database as ``--database-url`` (last); the
    workflow and eval CLIs read it from the environment the runner sets.
    A ``draft-golden`` job from a document writes its text to a file under
    ``scratch_dir`` (a fresh temp file when none is given) and passes the path.
    """
    match job_type:
        case "workflow":
            assert isinstance(payload, WorkflowPayload)
            argv = _python(WORKFLOW_MODULE) + ["run-targets", *payload.targets, "--year", str(payload.year)]
            if payload.model:
                argv += ["--model", payload.model]
            if payload.force:
                argv.append("--force")
            return argv
        case "ingest":
            assert isinstance(payload, IngestPayload)
            return _python(INGEST_MODULE) + [payload.command, *payload.args, "--database-url", cfg.database_url]
        case "embed":
            assert isinstance(payload, EmbedPayload)
            argv = _python(INGEST_MODULE) + [
                "embeddings",
                "build",
                "--backend",
                "torch",
                "--model-path",
                cfg.embedding_model_path,
                "--model-id",
                str(payload.model_id),
                "--batch-size",
                str(payload.batch_size),
            ]
            if payload.limit is not None:
                argv += ["--limit", str(payload.limit)]
            if payload.dry_run:
                argv.append("--dry-run")
            return argv + ["--progress-json", "--database-url", cfg.database_url]
        case "translate":
            assert isinstance(payload, TranslatePayload)
            argv = _python(INGEST_MODULE) + [
                "translate",
                "run",
                "--model",
                payload.model,
                "--target-lang",
                payload.target_lang,
                "--progress-json",
                "--request-timeout",
                _number(payload.request_timeout),
            ]
            if payload.limit is not None:
                argv += ["--limit", str(payload.limit)]
            if payload.dry_run:
                argv.append("--dry-run")
            return argv + ["--database-url", cfg.database_url]
        case "translate-params":
            assert isinstance(payload, TranslateParamsPayload)
            argv = _python(WORKFLOW_MODULE) + ["translate-params", "--country", payload.country]
            if payload.lang:
                argv += ["--lang", payload.lang]
            if payload.model:
                argv += ["--model", payload.model]
            argv += ["--batch-size", str(payload.batch_size)]
            if payload.limit is not None:
                argv += ["--limit", str(payload.limit)]
            if payload.force:
                argv.append("--force")
            return argv
        case "eval":
            assert isinstance(payload, EvalPayload)
            if payload.resume is not None:
                return _python(EVAL_MODULE) + ["resume", payload.resume]
            argv = _python(EVAL_MODULE) + ["run", "--as-of", str(payload.as_of), "--model", str(payload.model)]
            for country in payload.countries:
                argv += ["--country", country]
            for language in payload.languages:
                argv += ["--language", language]
            if payload.include_drafts:
                argv.append("--include-drafts")
            if payload.notes:
                argv += ["--notes", payload.notes]
            return argv
        case "draft-golden":
            assert isinstance(payload, DraftGoldenPayload)
            return _draft_golden_command(payload, scratch_dir)
        case "impact":
            assert isinstance(payload, ImpactPayload)
            argv = _python(WORKFLOW_MODULE) + ["impact", "--json"]
            if payload.project:
                argv += ["--project", payload.project]
            if payload.since:
                argv += ["--since", payload.since]
            if payload.until:
                argv += ["--until", payload.until]
            if payload.zone:
                argv += ["--zone", payload.zone]
            return argv
        case "encode":
            msg = "encode jobs are answered in-process by the encode lane"
            raise ValueError(msg)
        case _:
            msg = f"unknown job type: {job_type!r}"
            raise ValueError(msg)


def _draft_golden_command(payload: DraftGoldenPayload, scratch_dir: Path | None) -> list[str]:
    if payload.source == "document":
        path = write_document_text(payload.text or "", scratch_dir)
        argv = _python(EVAL_MODULE) + [
            "build-dataset",
            str(path),
            "--country",
            payload.country,
            "--as-of",
            str(payload.as_of),
        ]
        if payload.language:
            argv += ["--language", payload.language]
        for target in payload.targets:
            argv += ["--target", target]
        if payload.model:
            argv += ["--model", payload.model]
        return argv

    command = "build-openfisca-dataset" if payload.source == "openfisca" else "build-curated-dataset"
    argv = _python(EVAL_MODULE) + [command, "--country", payload.country, "--year", str(payload.year)]
    if payload.as_of:
        argv += ["--as-of", payload.as_of]
    if payload.source == "openfisca":
        # Only the OpenFisca builder tops a selection up from parameter_links.
        argv += ["--limit", str(payload.limit), "--fill" if payload.fill else "--curated-only"]
    return argv


def write_document_text(text: str, scratch_dir: Path | None) -> Path:
    """Write a trusted document's text to a file the eval builder can read.

    Under ``scratch_dir`` when the runner provides one (removed with the job);
    otherwise a named temp file the caller owns.
    """
    if scratch_dir is not None:
        path = scratch_dir / "document.md"
        path.write_text(text, encoding="utf-8")
        return path
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", prefix="nomergon-draft-", suffix=".md", delete=False) as fh:
        fh.write(text)
        return Path(fh.name)


def _number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else str(value)


def extract_result(
    job_type: str,
    payload: _Payload,
    *,
    result_line: dict[str, Any] | None,
    last_progress: dict[str, Any] | None,
    stdout_tail: list[str],
) -> Any:
    """What ``ops.jobs.result`` holds for a succeeded job, per the contract.

    ``@result`` lines are captured by the runner; ``route`` and ``impact`` print
    their report as a plain JSON line instead, so it is the last JSON line of
    stdout. ``embed`` and ``translate`` report their final progress.
    """
    if job_type in ("workflow", "eval", "draft-golden"):
        return result_line
    if job_type in ("embed", "translate"):
        return last_progress
    if job_type == "impact" or (job_type == "ingest" and getattr(payload, "command", None) == "route"):
        return last_json_line(stdout_tail)
    return None


def last_json_line(lines: list[str]) -> dict[str, Any] | None:
    """The last stdout line that parses as a JSON object, or None."""
    for line in reversed(lines):
        stripped = line.strip()
        if not stripped.startswith("{"):
            continue
        try:
            value = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None
