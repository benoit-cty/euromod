"""The encode lane: BGE-M3 kept warm in-process, answering ``encode`` jobs.

A job naming another registry model (``model_id``, e.g. while that model is
evaluated against BGE-M3) loads it on first use and keeps it too; BGE-M3 is
the only one loaded at start.

A query vector for the UI's semantic search (or the pipeline's retrieval when
``WORKFLOW_ENCODER=db``) must never wait behind a GPU batch, so this thread
has its own connection and its own claim query. The answer format is that of
``nomotheca_ingest.query_embeddings`` (``{"halfvec": …}`` or
``{"similarities": […]}``), whose ``handle_request`` is reused as is.
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Any

from . import db
from .config import WorkerConfig

log = logging.getLogger("nomergon.encoder")

LOAD_RETRY_SECONDS = 60.0


def describe_device() -> str:
    """``cuda:<GPU name>`` when torch sees a usable GPU, else ``cpu``."""
    try:
        import torch
    except ImportError:
        return "cpu"
    if torch.cuda.is_available():
        try:
            return f"cuda:{torch.cuda.get_device_name(0)}"
        except Exception:  # noqa: BLE001 - a broken driver reads as no GPU
            return "cpu"
    return "cpu"


def load_backend(model_path: str | None, model_id: int = 1) -> Any:
    """Load ``SentenceTransformerBackend`` on CUDA when usable, else on the CPU.

    Mirrors ``query_embeddings.main``'s torch choices; the one addition is the
    fallback: a torch build with no kernels for this GPU
    (``raise_for_unsupported_cuda_arch``) or a CUDA load failure degrades to
    the CPU instead of leaving the lane dead.
    """
    from nomotheca_ingest.core.embedding_models import get_model
    from nomotheca_ingest.core.embeddings import SentenceTransformerBackend, resolve_torch_device

    spec = get_model(model_id)
    device = resolve_torch_device(None, backend="torch")
    if device.startswith("cuda"):
        try:
            return SentenceTransformerBackend(model_path=model_path, backend="torch", device=device, spec=spec)
        except RuntimeError as exc:
            log.warning("CUDA encoder unavailable (%s); falling back to the CPU", exc)
    return SentenceTransformerBackend(model_path=model_path, backend="torch", device="cpu", spec=spec)


class EncodeLane(threading.Thread):
    """Polls ``encode`` jobs and answers them with the warm model."""

    def __init__(self, cfg: WorkerConfig, stop: threading.Event) -> None:
        super().__init__(name="nomergon-encode", daemon=True)
        self.cfg = cfg
        self.stop_event = stop
        self.backend: Any = None
        self.extra_backends: dict[int, Any] = {}
        self.load_error: str | None = None
        self.ready = threading.Event()
        self._next_load_attempt = 0.0

    def run(self) -> None:
        conn = db.connect(self.cfg.database_url)
        try:
            self._ensure_backend()
            while not self.stop_event.is_set():
                try:
                    job = db.claim_encode_job(conn, self.cfg.worker_id)
                except Exception:  # noqa: BLE001 - keep polling through a DB hiccup
                    log.exception("encode lane: claim failed")
                    time.sleep(1.0)
                    continue
                if job is None:
                    time.sleep(self.cfg.encode_poll_seconds)
                    continue
                self._answer(conn, job)
        finally:
            conn.close()

    def _ensure_backend(self) -> bool:
        if self.backend is not None:
            return True
        if time.monotonic() < self._next_load_attempt:
            return False
        self._next_load_attempt = time.monotonic() + LOAD_RETRY_SECONDS
        try:
            started = time.monotonic()
            self.backend = load_backend(self.cfg.embedding_model_path)
            self.load_error = None
            log.info(
                "encoder ready: %s (%s, %.1fs)",
                self.cfg.embedding_model_path,
                getattr(self.backend, "description", "?"),
                time.monotonic() - started,
            )
            self.ready.set()
            return True
        except Exception as exc:  # noqa: BLE001 - reported per job, retried later
            self.load_error = f"{type(exc).__name__}: {exc}"
            log.error("encoder failed to load %s: %s", self.cfg.embedding_model_path, self.load_error)
            return False

    def _backend_for(self, model_id: int) -> Any:
        """The warm backend for a registry model; non-default ones load on first use."""
        if model_id not in self.extra_backends:
            started = time.monotonic()
            self.extra_backends[model_id] = load_backend(None, model_id)
            log.info("encoder ready for model %s (%.1fs)", model_id, time.monotonic() - started)
        return self.extra_backends[model_id]

    def _answer(self, conn: Any, job: dict[str, Any]) -> None:
        job_id = int(job["id"])
        payload = dict(job["payload"] or {})
        model_id = int(payload.pop("model_id", 1))
        if model_id == 1 and not self._ensure_backend():
            db.finish_job(conn, job_id, "failed", error=f"encoder unavailable: {self.load_error}")
            return
        try:
            from nomotheca_ingest.query_embeddings import handle_request

            backend = self.backend if model_id == 1 else self._backend_for(model_id)
            response = handle_request(backend, payload)
        except Exception as exc:  # noqa: BLE001
            db.finish_job(conn, job_id, "failed", error=f"{type(exc).__name__}: {exc}")
            return
        db.finish_job(conn, job_id, "succeeded", result=response)
