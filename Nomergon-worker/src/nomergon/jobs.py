"""Job types: one payload model per type, and the argv each one runs.

This is the whole mapping from "what the UI described" to "what the worker
executes", kept as pure functions so it can be tested without a database or
a subprocess. The table it implements is `.scratch/nomergon-worker/contracts.md`.
"""

from __future__ import annotations

import json
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .config import WorkerConfig

INGEST_MODULE = "nomotheca_ingest.cli"
WORKFLOW_MODULE = "nomoscope_workflow.cli"
EVAL_MODULE = "nomokrisis_eval.cli"

#: The encode lane answers query vectors for searches someone is waiting on.
ENCODE_PRIORITY = 100
#: A chat turn is interactive: ahead of batches, behind the encode lane.
CHAT_PRIORITY = 50


def _python(module: str) -> list[str]:
    return [sys.executable, "-m", module]


def _number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else str(value)


class _Payload(BaseModel):
    """A job's payload; each subprocess type maps itself to the argv it runs.

    The ingest CLIs take the database as ``--database-url`` (last); the
    workflow and eval CLIs read it from the environment the runner sets.
    """

    model_config = ConfigDict(extra="forbid")

    def to_argv(self, cfg: WorkerConfig, scratch_dir: Path | None) -> list[str]:
        """The argv for this job, always ``sys.executable -m <module> …``."""
        raise NotImplementedError


class WorkflowPayload(_Payload):
    """Either ``targets`` (run-targets) or a whole ``country`` (run-country), never both."""

    targets: list[str] = Field(default_factory=list)
    country: str | None = None
    #: run-country only: at most N parameters (a smoke run).
    limit: int | None = Field(default=None, ge=1)
    year: int
    model: str | None = None
    force: bool = False
    #: Also run parameters EUROMOD holds as n/a in that system year (skipped by default).
    include_na: bool = False

    @model_validator(mode="after")
    def _targets_or_country(self) -> WorkflowPayload:
        if bool(self.targets) == bool(self.country):
            msg = "give either targets or a country"
            raise ValueError(msg)
        if self.limit is not None and not self.country:
            msg = "limit applies to a country run only"
            raise ValueError(msg)
        return self

    def to_argv(self, cfg: WorkerConfig, scratch_dir: Path | None) -> list[str]:
        if self.country:
            argv = _python(WORKFLOW_MODULE) + ["run-country", self.country, "--year", str(self.year)]
            if self.limit:
                argv += ["--limit", str(self.limit)]
        else:
            argv = _python(WORKFLOW_MODULE) + ["run-targets", *self.targets, "--year", str(self.year)]
        if self.model:
            argv += ["--model", self.model]
        if self.force:
            argv.append("--force")
        if self.include_na:
            argv.append("--include-na")
        return argv


IngestCommand = Literal["instrument", "citation", "document", "route"]

#: The fields each ingest command needs; the others must be absent.
_INGEST_REQUIRED: dict[str, tuple[str, ...]] = {
    "instrument": ("jurisdiction", "national_id"),
    "citation": ("jurisdiction", "citation", "as_of"),
    "document": ("source", "jurisdiction", "lang", "title", "kind", "valid_from"),
    "route": (),
}
_INGEST_ALLOWED: dict[str, tuple[str, ...]] = {
    "instrument": ("jurisdiction", "national_id", "source_code", "max_items"),
    "citation": ("jurisdiction", "citation", "as_of", "source_code", "max_items"),
    "document": ("source", "jurisdiction", "lang", "title", "kind", "valid_from", "implements"),
    "route": ("source",),
}

#: The legacy ``args`` form, read through an allow-list: per command, the
#: positionals in order (the trailing ones of ``route`` optional) and the
#: flags with the field each one fills. ``--progress-json`` is accepted and
#: implied; ``--database-url``, ``--trigger`` or any other flag is refused.
_LEGACY_POSITIONALS: dict[str, tuple[str, ...]] = {
    "instrument": ("jurisdiction", "national_id"),
    "citation": ("jurisdiction", "citation", "as_of"),
    "document": ("source",),
    "route": ("source",),
}
_LEGACY_FLAGS: dict[str, dict[str, str]] = {
    "instrument": {"--source-code": "source_code", "--max-items": "max_items"},
    "citation": {"--source-code": "source_code", "--max-items": "max_items"},
    "document": {
        "--jurisdiction": "jurisdiction",
        "--lang": "lang",
        "--title": "title",
        "--kind": "kind",
        "--valid-from": "valid_from",
        "--implements": "implements",
    },
    "route": {},
}
_LEGACY_SWITCHES: dict[str, tuple[str, ...]] = {"document": ("--progress-json",)}

_URL_PREFIXES = ("http://", "https://")


def _legacy_ingest_fields(command: str, args: list[str]) -> dict[str, Any]:
    """Read the ``args`` the desktop apps still send into the typed fields."""
    positionals = _LEGACY_POSITIONALS.get(command, ())
    flags = _LEGACY_FLAGS.get(command, {})
    switches = _LEGACY_SWITCHES.get(command, ())
    fields: dict[str, Any] = {}
    values: list[str] = []
    rest = list(args)
    while rest:
        token = rest.pop(0)
        if token in switches:
            continue
        if token in flags:
            if not rest:
                msg = f"ingest {command}: {token} needs a value"
                raise ValueError(msg)
            fields[flags[token]] = rest.pop(0)
            continue
        if token.startswith("-"):
            msg = f"ingest {command}: option {token!r} is not allowed (allowed: {', '.join([*flags, *switches]) or 'none'})"
            raise ValueError(msg)
        values.append(token)
    if len(values) > len(positionals):
        msg = f"ingest {command}: too many arguments ({len(values)} for {len(positionals)})"
        raise ValueError(msg)
    fields.update(zip(positionals, values, strict=False))
    return fields


class IngestPayload(_Payload):
    """One ingest CLI run: an official act by id or by citation, a contributed
    document, or the ``route`` pre-check. Only these four commands and these
    fields reach ``nomotheca_ingest.cli``; the database URL is the worker's."""

    command: IngestCommand
    jurisdiction: str | None = Field(
        default=None, pattern=r"^[A-Za-z]{2}(-[A-Za-z0-9]{1,8})?$", description="Country code, e.g. fr, ES-AR"
    )
    national_id: str | None = Field(default=None, min_length=1, description="instrument: the act's national id")
    citation: str | None = Field(default=None, min_length=1, description="citation: the citation text to resolve")
    as_of: date | None = Field(default=None, description="citation: the date the citation is resolved at")
    source_code: str | None = Field(default=None, pattern=r"^[A-Za-z0-9_-]{1,32}$", description="e.g. FR-KALI")
    max_items: int | None = Field(default=None, ge=1, le=10_000)
    source: str | None = Field(
        default=None,
        description="document/route: an http(s) URL, or a file under the worker's WORKER_DOCUMENT_DIR",
    )
    lang: str | None = Field(default=None, pattern=r"^[a-z]{2,3}$")
    title: str | None = Field(default=None, min_length=1)
    kind: str | None = Field(default=None, pattern=r"^[\w-]{1,40}$", description="in the country's own words")
    valid_from: date | None = None
    implements: str | None = Field(default=None, min_length=1, description="national_id of the implemented act")
    args: list[str] | None = Field(
        default=None,
        description="Deprecated: the CLI arguments the desktop apps build; read through an allow-list "
        "into the fields above, never passed through. Give either args or the fields.",
    )

    @model_validator(mode="before")
    @classmethod
    def _read_legacy_args(cls, data: Any) -> Any:
        if not isinstance(data, dict) or data.get("args") is None:
            return data
        others = sorted(set(data) - {"command", "args"})
        if others:
            msg = f"give either args or the typed fields, not both ({', '.join(others)})"
            raise ValueError(msg)
        args = data["args"]
        if not isinstance(args, list) or not all(isinstance(a, str) for a in args):
            msg = "args must be a list of strings"
            raise ValueError(msg)
        return {"command": data.get("command"), **_legacy_ingest_fields(str(data.get("command")), args)}

    @model_validator(mode="after")
    def _fields_for_command(self) -> IngestPayload:
        given = {name for name in self.model_fields_set if getattr(self, name) is not None} - {"command", "args"}
        missing = [name for name in _INGEST_REQUIRED[self.command] if getattr(self, name) in (None, "")]
        if missing:
            msg = f"ingest {self.command} needs {', '.join(missing)}"
            raise ValueError(msg)
        extra = sorted(given - set(_INGEST_ALLOWED[self.command]))
        if extra:
            msg = f"ingest {self.command} takes no {', '.join(extra)}"
            raise ValueError(msg)
        # A value starting with '-' would be read as an option by the CLI.
        for name in ("jurisdiction", "national_id", "citation", "source"):
            value = getattr(self, name)
            if isinstance(value, str) and value.startswith("-"):
                msg = f"{name} must not start with '-'"
                raise ValueError(msg)
        return self

    def to_argv(self, cfg: WorkerConfig, scratch_dir: Path | None) -> list[str]:
        argv = _python(INGEST_MODULE) + [self.command]
        if self.command in ("instrument", "citation"):
            argv.append(str(self.jurisdiction))
            if self.command == "instrument":
                argv.append(str(self.national_id))
            else:
                argv += [str(self.citation), str(self.as_of)]
            if self.source_code:
                argv += ["--source-code", self.source_code]
            if self.max_items is not None:
                argv += ["--max-items", str(self.max_items)]
        elif self.command == "document":
            argv += [
                _document_source(str(self.source), cfg),
                "--jurisdiction",
                str(self.jurisdiction),
                "--lang",
                str(self.lang),
                "--title",
                str(self.title),
                "--kind",
                str(self.kind),
                "--valid-from",
                str(self.valid_from),
            ]
            if self.implements:
                argv += ["--implements", self.implements]
            argv.append("--progress-json")
        elif self.source:
            argv.append(_document_source(self.source, cfg))
        return argv + ["--database-url", cfg.database_url]


def _document_source(source: str, cfg: WorkerConfig) -> str:
    """A URL as given; a file only inside ``WORKER_DOCUMENT_DIR``.

    The ingester reads any path it is handed and loads it into the shared
    corpus, so a path from a submitter could otherwise read the worker's own
    files (its environment holds every model key, ADR 0004).
    """
    if source.startswith(_URL_PREFIXES):
        return source
    if cfg.document_dir is None:
        msg = "a document source must be an http(s) URL (set WORKER_DOCUMENT_DIR to accept files from one directory)"
        raise ValueError(msg)
    root = cfg.document_dir.resolve()
    path = (root / source).resolve()
    if not path.is_relative_to(root):
        msg = f"a document file must be under WORKER_DOCUMENT_DIR ({root})"
        raise ValueError(msg)
    return str(path)


class EmbedPayload(_Payload):
    #: Registry id (nomotheca_ingest.core.embedding_models); 1 = BGE-M3.
    model_id: int = 1
    batch_size: int = Field(default=16, ge=1)
    limit: int | None = Field(default=None, ge=1)
    dry_run: bool = False
    precision: Literal["auto", "fp32", "fp16", "bf16"] = "auto"
    #: Skip machine translations — what a candidate model under evaluation needs.
    authentic_only: bool = False

    def to_argv(self, cfg: WorkerConfig, scratch_dir: Path | None) -> list[str]:
        argv = _python(INGEST_MODULE) + ["embeddings", "build", "--backend", "torch"]
        # The configured path holds BGE-M3's weights; any other registry
        # model loads from its own Hugging Face id.
        if self.model_id == 1:
            argv += ["--model-path", cfg.embedding_model_path]
        argv += ["--model-id", str(self.model_id), "--batch-size", str(self.batch_size)]
        if self.precision != "auto":
            argv += ["--precision", self.precision]
        if self.authentic_only:
            argv.append("--authentic-only")
        if self.limit is not None:
            argv += ["--limit", str(self.limit)]
        if self.dry_run:
            argv.append("--dry-run")
        return argv + ["--progress-json", "--database-url", cfg.database_url]


class TranslatePayload(_Payload):
    model: str
    target_lang: str = "en"
    limit: int | None = Field(default=None, ge=1)
    request_timeout: float = Field(default=120, ge=0)
    dry_run: bool = False

    def to_argv(self, cfg: WorkerConfig, scratch_dir: Path | None) -> list[str]:
        argv = _python(INGEST_MODULE) + [
            "translate",
            "run",
            "--model",
            self.model,
            "--target-lang",
            self.target_lang,
            "--progress-json",
            "--request-timeout",
            _number(self.request_timeout),
        ]
        if self.limit is not None:
            argv += ["--limit", str(self.limit)]
        if self.dry_run:
            argv.append("--dry-run")
        return argv + ["--database-url", cfg.database_url]


class TranslateParamsPayload(_Payload):
    country: str
    lang: str | None = None
    model: str | None = None
    batch_size: int = Field(default=20, ge=1)
    limit: int | None = Field(default=None, ge=1)
    force: bool = False

    def to_argv(self, cfg: WorkerConfig, scratch_dir: Path | None) -> list[str]:
        argv = _python(WORKFLOW_MODULE) + ["translate-params", "--country", self.country]
        if self.lang:
            argv += ["--lang", self.lang]
        if self.model:
            argv += ["--model", self.model]
        argv += ["--batch-size", str(self.batch_size)]
        if self.limit is not None:
            argv += ["--limit", str(self.limit)]
        if self.force:
            argv.append("--force")
        return argv


class EncodePayload(_Payload):
    query: str
    sentences: list[str] | None = None
    #: Registry id of the model whose vectors the query is compared with.
    model_id: int = 1

    @model_validator(mode="after")
    def _query_not_blank(self) -> EncodePayload:
        if not self.query.strip():
            msg = "query must not be empty"
            raise ValueError(msg)
        return self

    def to_argv(self, cfg: WorkerConfig, scratch_dir: Path | None) -> list[str]:
        msg = "encode jobs are answered in-process by the encode lane"
        raise ValueError(msg)


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

    def to_argv(self, cfg: WorkerConfig, scratch_dir: Path | None) -> list[str]:
        if self.resume is not None:
            return _python(EVAL_MODULE) + ["resume", self.resume]
        argv = _python(EVAL_MODULE) + ["run", "--as-of", str(self.as_of), "--model", str(self.model)]
        for country in self.countries:
            argv += ["--country", country]
        for language in self.languages:
            argv += ["--language", language]
        if self.include_drafts:
            argv.append("--include-drafts")
        if self.notes:
            argv += ["--notes", self.notes]
        return argv


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

    def to_argv(self, cfg: WorkerConfig, scratch_dir: Path | None) -> list[str]:
        if self.source == "document":
            # The text goes through a file under the job's scratch directory.
            path = write_document_text(self.text or "", scratch_dir)
            argv = _python(EVAL_MODULE) + ["build-dataset", str(path), "--country", self.country, "--as-of", str(self.as_of)]
            if self.language:
                argv += ["--language", self.language]
            for target in self.targets:
                argv += ["--target", target]
            if self.model:
                argv += ["--model", self.model]
            return argv
        command = "build-openfisca-dataset" if self.source == "openfisca" else "build-curated-dataset"
        argv = _python(EVAL_MODULE) + [command, "--country", self.country, "--year", str(self.year)]
        if self.as_of:
            argv += ["--as-of", self.as_of]
        if self.source == "openfisca":
            # Only the OpenFisca builder tops a selection up from parameter_links.
            argv += ["--limit", str(self.limit), "--fill" if self.fill else "--curated-only"]
        return argv


class ImpactPayload(_Payload):
    project: str = ""
    since: str | None = None
    until: str | None = None
    zone: str = ""

    def to_argv(self, cfg: WorkerConfig, scratch_dir: Path | None) -> list[str]:
        argv = _python(WORKFLOW_MODULE) + ["impact", "--json"]
        if self.project:
            argv += ["--project", self.project]
        if self.since:
            argv += ["--since", self.since]
        if self.until:
            argv += ["--until", self.until]
        if self.zone:
            argv += ["--zone", self.zone]
        return argv


class ChatMessage(_Payload):
    role: Literal["user", "assistant"]
    content: str
    #: An earlier assistant turn's verified quotes (chunk ids the follow-up may name).
    quotes: list[dict[str, Any]] = Field(default_factory=list)


class ChatPayload(_Payload):
    """One assistant turn of the RAG chat (rag-ui): the whole conversation so far."""

    messages: list[ChatMessage] = Field(min_length=1)
    #: Groups the turns of one conversation, so the UI can rebuild it from
    #: ops.jobs instead of keeping a local copy.
    conversation_id: str | None = None
    country: str | None = None
    as_of: str | None = None
    model: str | None = None
    web: bool = True

    @model_validator(mode="after")
    def _ends_with_a_question(self) -> ChatPayload:
        last = self.messages[-1]
        if last.role != "user" or not last.content.strip():
            msg = "a chat job's last message must be a non-empty user message"
            raise ValueError(msg)
        return self

    def to_argv(self, cfg: WorkerConfig, scratch_dir: Path | None) -> list[str]:
        # The conversation goes through a file: it grows with every turn
        # and a single argv string is capped at 128 KiB on Linux.
        return _python(WORKFLOW_MODULE) + ["chat", str(write_chat_request(self, scratch_dir))]


Package = Literal["ingest", "pipeline", "eval"]
#: Where a succeeded job's ``ops.jobs.result`` comes from: the child's
#: ``@result`` line, its last ``@progress`` line, or nothing.
ResultSource = Literal["result_line", "progress", "none"]


@dataclass(frozen=True, slots=True)
class JobSpec:
    """Everything the worker varies on per job type, in one row.

    The SQL ``CHECK`` on ``ops.jobs.job_type`` and ``job_types.json`` (what
    the desktop UI imports) are kept equal to this table by tests.
    """

    name: str
    payload: type[_Payload]
    description: str
    #: The sub-project the job runs from (its cwd); None for an in-process type.
    package: Package | None
    result: ResultSource = "none"
    #: The priority a submitter uses when it gives none (higher runs first).
    priority: int = 0
    #: Walks a shared backlog (chunks without a vector, texts without a
    #: translation): two at once would do, and bill, the same work twice, so a
    #: worker runs at most one of the type. Every other type runs in parallel
    #: up to WORKER_CONCURRENCY. The GPU is guarded separately, by the advisory
    #: lock ``embeddings build`` takes (the scout's builds included).
    singleton: bool = False

    @property
    def in_process(self) -> bool:
        """Answered by the encode lane inside the worker, never as a subprocess."""
        return self.package is None


JOB_SPECS: dict[str, JobSpec] = {
    spec.name: spec
    for spec in (
        JobSpec("workflow", WorkflowPayload, "Agentic workflow run (run-targets / run-country)", "pipeline", "result_line"),
        JobSpec("ingest", IngestPayload, "Legislation or contributed-document ingest", "ingest", "result_line"),
        JobSpec("embed", EmbedPayload, "Embed the chunks with no vector", "ingest", "progress", singleton=True),
        JobSpec("translate", TranslatePayload, "Machine-translate unit texts", "ingest", "progress", singleton=True),
        JobSpec("translate-params", TranslateParamsPayload, "Translate parameter texts", "pipeline", singleton=True),
        JobSpec("encode", EncodePayload, "Query vectors for a search (in-process)", None, priority=ENCODE_PRIORITY),
        JobSpec("eval", EvalPayload, "Evaluation run over the golden set", "eval", "result_line"),
        JobSpec("draft-golden", DraftGoldenPayload, "Draft golden cases", "eval", "result_line"),
        JobSpec("impact", ImpactPayload, "Environmental impact report of traced LLM calls", "pipeline", "result_line"),
        JobSpec("chat", ChatPayload, "One RAG chat turn", "pipeline", "result_line", priority=CHAT_PRIORITY),
    )
}

JOB_TYPES = tuple(JOB_SPECS)
PAYLOAD_MODELS: dict[str, type[_Payload]] = {name: spec.payload for name, spec in JOB_SPECS.items()}
#: Job types answered in-process by the encode lane, never as a subprocess.
IN_PROCESS_JOB_TYPES = tuple(name for name, spec in JOB_SPECS.items() if spec.in_process)
SINGLETON_JOB_TYPES = tuple(name for name, spec in JOB_SPECS.items() if spec.singleton)


def job_spec(job_type: str) -> JobSpec:
    """The spec of one job type (``ValueError`` naming the known ones otherwise)."""
    try:
        return JOB_SPECS[job_type]
    except KeyError:
        msg = f"unknown job type: {job_type!r} (one of {', '.join(JOB_TYPES)})"
        raise ValueError(msg) from None


def default_priority(job_type: str) -> int:
    return job_spec(job_type).priority


def parse_payload(job_type: str, payload: dict[str, Any] | None) -> _Payload:
    """Validate a job's payload against its type's model (``ValueError`` on a bad one)."""
    return job_spec(job_type).payload.model_validate(payload or {})


def package_dir(job_type: str, cfg: WorkerConfig) -> Path:
    """The sub-project a job runs from (its cwd), so its relative paths resolve."""
    package = job_spec(job_type).package
    if package is None:
        msg = f"{job_type} does not run as a subprocess"
        raise ValueError(msg)
    return {"ingest": cfg.ingest_dir, "pipeline": cfg.pipeline_dir, "eval": cfg.eval_dir}[package]


def job_types_document() -> dict[str, Any]:
    """The job-type table as JSON, for the desktop UI (``nomergon job-types``).

    Written to ``Nomergon-worker/job_types.json`` and kept equal to it by a test.
    """
    return {
        "generated_by": "nomergon job-types --write",
        "job_types": [
            {
                "name": spec.name,
                "description": spec.description,
                "priority": spec.priority,
                "singleton": spec.singleton,
                "in_process": spec.in_process,
                "result": spec.result,
                "payload_schema": spec.payload.model_json_schema(),
            }
            for spec in JOB_SPECS.values()
        ],
    }


def build_command(
    job_type: str,
    payload: _Payload,
    cfg: WorkerConfig,
    *,
    scratch_dir: Path | None = None,
) -> list[str]:
    """The argv for one job: its payload's ``to_argv``.

    A job that writes a file (a ``draft-golden`` document, a ``chat``
    conversation) writes it under ``scratch_dir``.
    """
    spec = job_spec(job_type)
    if not isinstance(payload, spec.payload):
        msg = f"a {job_type} job needs a {spec.payload.__name__}, not {type(payload).__name__}"
        raise TypeError(msg)
    return payload.to_argv(cfg, scratch_dir)


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


def write_chat_request(payload: ChatPayload, scratch_dir: Path | None) -> Path:
    """Write a chat job's payload where ``nomoscope-workflow chat`` reads it."""
    text = payload.model_dump_json()
    if scratch_dir is not None:
        path = scratch_dir / "chat.json"
        path.write_text(text, encoding="utf-8")
        return path
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", prefix="nomergon-chat-", suffix=".json", delete=False) as fh:
        fh.write(text)
        return Path(fh.name)


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
    if job_type == "impact" or (job_type == "ingest" and getattr(payload, "command", None) == "route"):
        return last_json_line(stdout_tail)
    source = job_spec(job_type).result
    if source == "progress":
        return last_progress
    if source == "result_line" and job_type != "ingest":
        return result_line
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
