"""Batch commands over the corpus backlog: embeddings and machine translation."""

from __future__ import annotations

import json
import os
import time
from contextlib import ExitStack
from datetime import date
from typing import Annotated

import typer

from nomotheca_ingest.cli._app import DatabaseUrl, embeddings_app, translate_app
from nomotheca_ingest.core.embedding_models import MODELS, get_model
from nomotheca_ingest.core.embeddings import (
    DEFAULT_MAX_SEQ_LENGTH,
    EMBEDDING_BACKENDS,
    PRECISIONS,
    SentenceTransformerBackend,
    build_embeddings,
    count_chunks_needing_embeddings,
    embedding_build_lock,
)
from nomotheca_ingest.core.progress import EMBEDDINGS, TRANSLATIONS, batch_progress, emit_json
from nomotheca_ingest.core.translate import (
    DEFAULT_TARGET_LANG,
    DEFAULT_TRANSLATION_REQUEST_TIMEOUT_SECONDS,
    LLMTranslationBackend,
    build_translations,
    count_texts_needing_translation,
)
from nomotheca_ingest.core.db import connect


@embeddings_app.command("models")
def list_embedding_models() -> None:
    """List the embedding models the registry can build (id, key, dimension, licence)."""
    for spec in MODELS:
        typer.echo(
            f"{spec.id:>2}  {spec.key:<32} {spec.hf_id:<42} {spec.native_dim:>4}d "
            f"({spec.dim_fit}) ctx={spec.max_seq_length:<6} {spec.licence}"
        )
        if spec.notes:
            typer.echo(f"    {spec.notes}")


@embeddings_app.command("build")
def build_chunk_embeddings(
    database_url: DatabaseUrl,
    model: Annotated[
        str | None,
        typer.Option("--model", "-m", help="Registry key or id (see `embeddings models`); default: --model-id."),
    ] = None,
    model_path: Annotated[
        str | None,
        typer.Option("--model-path", help="Local path overriding the registry's Hugging Face id (same model)."),
    ] = None,
    backend: Annotated[
        str,
        typer.Option("--backend", help="sentence-transformers backend: torch or openvino."),
    ] = "torch",
    model_id: Annotated[int, typer.Option("--model-id", min=1, help="Registry id; 1 = BGE-M3.")] = 1,
    precision: Annotated[
        str,
        typer.Option("--precision", help="auto | fp32 | fp16 | bf16 (auto: see embeddings.cuda_dtype_for)."),
    ] = "auto",
    max_seq_length: Annotated[
        int,
        typer.Option("--max-seq-length", min=16, help="Token cap per chunk (longer chunks are truncated)."),
    ] = DEFAULT_MAX_SEQ_LENGTH,
    authentic_only: Annotated[
        bool,
        typer.Option("--authentic-only", help="Skip machine translations (evidence retrieval never searches them)."),
    ] = False,
    langs: Annotated[
        list[str] | None,
        typer.Option("--lang", help="Only chunks in this language (repeatable)."),
    ] = None,
    in_force_on: Annotated[
        list[str] | None,
        typer.Option("--in-force-on", help="Only versions in force on this YYYY-MM-DD (repeatable)."),
    ] = None,
    batch_size: Annotated[int, typer.Option("--batch-size", min=1)] = 16,
    limit: Annotated[int | None, typer.Option("--limit", min=1)] = None,
    device: Annotated[
        str | None,
        typer.Option(
            "--device",
            help="torch: cpu, cuda, cuda:1 (default: cuda when available). openvino: CPU, GPU, NPU.",
        ),
    ] = None,
    encode_batch_size: Annotated[
        int | None,
        typer.Option("--encode-batch-size", min=1, help="Texts per forward pass; defaults to --batch-size."),
    ] = None,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Count stale chunks without writing embeddings.")] = False,
    show_progress: Annotated[bool, typer.Option("--progress/--no-progress", help="Show live embedding progress.")] = True,
    progress_json: Annotated[
        bool,
        typer.Option("--progress-json", help="Emit '@progress {json}' lines for wrapping UIs."),
    ] = False,
    fix_mistral_regex: Annotated[
        bool,
        typer.Option("--fix-mistral-regex", help="Forward fix_mistral_regex=True to the tokenizer."),
    ] = False,
    slow_tokenizer: Annotated[
        bool,
        typer.Option("--slow-tokenizer", help="Use the slow tokenizer; may require sentencepiece."),
    ] = False,
) -> None:
    """Build local embeddings (BGE-M3 unless --model) for chunks missing fresh vectors."""
    if backend not in EMBEDDING_BACKENDS:
        allowed = ", ".join(EMBEDDING_BACKENDS)
        raise typer.BadParameter(f"backend must be one of: {allowed}")
    if precision not in PRECISIONS:
        raise typer.BadParameter(f"precision must be one of: {', '.join(PRECISIONS)}")
    try:
        spec = get_model(model if model is not None else model_id)
    except KeyError as exc:
        raise typer.BadParameter(str(exc.args[0])) from exc
    model_id = spec.id
    scope = {
        "authentic_only": authentic_only,
        "langs": langs or None,
        "in_force_on": [date.fromisoformat(day) for day in in_force_on] if in_force_on else None,
    }
    with ExitStack() as held:
        if not dry_run:
            # Before the model loads: a second BGE-M3 copy is what the lock
            # keeps off the GPU. build_embeddings takes it again (re-entrant).
            held.enter_context(embedding_build_lock(database_url, _lock_progress if progress_json else None))
        embedding_backend = (
            _DryRunEmbeddingBackend()
            if dry_run
            else SentenceTransformerBackend(
                model_path=model_path,
                device=device,
                backend=backend,
                fix_mistral_regex=fix_mistral_regex,
                slow_tokenizer=slow_tokenizer,
                encode_batch_size=encode_batch_size or batch_size,
                spec=spec,
                precision=precision,
                max_seq_length=max_seq_length,
            )
        )
        if not dry_run:
            # stderr: stdout carries the '@progress' protocol a wrapping UI parses.
            typer.echo(embedding_backend.description, err=True)
        started = time.monotonic()
        with connect(database_url) as conn:
            with batch_progress(
                EMBEDDINGS,
                json_total=(
                    (lambda: count_chunks_needing_embeddings(conn, model_id=model_id, limit=limit, **scope))
                    if progress_json
                    else None
                ),
                show=show_progress,
                limit=limit,
                dry_run=dry_run,
            ) as progress:
                stats = build_embeddings(
                    conn,
                    embedding_backend,
                    model_id=model_id,
                    batch_size=batch_size,
                    limit=limit,
                    dry_run=dry_run,
                    progress=progress,
                    **scope,
                )
            conn.commit()
        elapsed = time.monotonic() - started
        if dry_run:
            typer.echo(
                f"scanned={stats.scanned} would_embed={stats.done} "
                f"model_id={model_id} backend={backend} dry_run=True"
            )
        else:
            typer.echo(
                f"scanned={stats.scanned} embedded={stats.done} skipped={stats.skipped} "
                f"model={spec.key} model_id={model_id} backend={backend} device={embedding_backend.device} "
                f"seconds={elapsed:.0f} dry_run=False"
            )
            if stats.skipped:
                typer.echo(
                    f"note: {stats.skipped} chunk(s) were re-chunked by a concurrent ingest "
                    "during this run; re-run the build to embed the replacements."
                )
            result = {
                "model": spec.key,
                "model_id": model_id,
                "embedded": stats.done,
                "seconds": round(elapsed, 1),
                "chunks_per_second": round(stats.done / elapsed, 2) if elapsed and stats.done else None,
                "backend": embedding_backend.description,
                "peak_vram_gib": _peak_vram_gib(embedding_backend),
            }
            typer.echo("@result " + json.dumps(result))


def _lock_progress(phase: str, detail: str) -> None:
    """The lock's waiting/starting lines, as the worker reads them."""
    emit_json({"task": "embeddings", "phase": phase, "detail": detail})


def _translate_model(model: str | None) -> str:
    """The translation model: --model, else EUROMOD_TRANSLATE_MODEL, else WORKFLOW_MODEL.

    The root .env is only loaded once the workflow package is imported, after
    typer has read its envvars — hence the second look here.
    """
    if model:
        return model
    try:
        from nomoscope_workflow.config import load_config
    except ImportError as exc:  # pragma: no cover - operator environment
        raise typer.BadParameter("Install translation dependencies with: uv sync --extra translate") from exc
    load_config()  # side effect: loads the repo-root .env
    resolved = os.environ.get("EUROMOD_TRANSLATE_MODEL") or os.environ.get("WORKFLOW_MODEL")
    if not resolved or resolved.startswith("mock/"):
        raise typer.BadParameter(
            "no translation model: pass --model or set EUROMOD_TRANSLATE_MODEL / WORKFLOW_MODEL "
            "to a real provider model in the root .env (mock/ cannot translate)",
            param_hint="--model",
        )
    return resolved


@translate_app.command("run")
def run_translations(
    database_url: DatabaseUrl,
    model: Annotated[
        str | None,
        typer.Option(
            "--model",
            "-m",
            envvar="EUROMOD_TRANSLATE_MODEL",
            help="Provider-prefixed model (see nomoscope_workflow.llm); "
            "default EUROMOD_TRANSLATE_MODEL, else WORKFLOW_MODEL, from the root .env.",
        ),
    ] = None,
    target_lang: Annotated[str, typer.Option("--target-lang", help="Target language (must exist in lang_fts_config).")] = DEFAULT_TARGET_LANG,
    limit: Annotated[int | None, typer.Option("--limit", min=1)] = None,
    request_timeout: Annotated[
        float | None,
        typer.Option(
            "--request-timeout",
            min=1,
            help="Per-provider-request timeout in seconds. Use 0 to disable.",
        ),
    ] = DEFAULT_TRANSLATION_REQUEST_TIMEOUT_SECONDS,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Count untranslated texts without calling the LLM.")] = False,
    show_progress: Annotated[bool, typer.Option("--progress/--no-progress", help="Show live translation progress.")] = True,
    progress_json: Annotated[
        bool,
        typer.Option("--progress-json", help="Emit '@progress {json}' lines for wrapping UIs."),
    ] = False,
) -> None:
    """Translate every unit text version missing a target-language rendering."""
    timeout = None if request_timeout == 0 else request_timeout
    backend = None if dry_run else LLMTranslationBackend(_translate_model(model), request_timeout=timeout)
    with connect(database_url) as conn:
        with batch_progress(
            TRANSLATIONS,
            json_total=(
                (lambda: count_texts_needing_translation(conn, target_lang=target_lang, limit=limit))
                if progress_json
                else None
            ),
            show=show_progress,
            limit=limit,
            dry_run=dry_run,
        ) as progress:
            stats = build_translations(
                conn,
                backend,
                target_lang=target_lang,
                limit=limit,
                dry_run=dry_run,
                progress=progress,
            )
    action = "would_translate" if dry_run else "translated"
    typer.echo(
        f"scanned={stats.scanned} {action}={stats.done} "
        f"failed={stats.failed} model={model} target_lang={target_lang} dry_run={dry_run}"
    )
    if stats.failed:
        raise typer.Exit(code=1)


class _DryRunEmbeddingBackend:
    """Backend placeholder used when no vectors will be written."""

    def encode(self, inputs: list[str]) -> list[list[float]]:
        return []


def _peak_vram_gib(embedding_backend: object) -> float | None:
    """Peak GPU memory this process allocated, for sizing a card; None off-GPU."""
    torch = getattr(embedding_backend, "_torch", None)
    if torch is None:
        return None
    return round(torch.cuda.max_memory_allocated() / 1024**3, 2)
