"""Lazy query encoding with the same BGE-M3 model used at ingestion time."""

from __future__ import annotations

import os
from pathlib import Path
from threading import Lock

from nomotheca_ingest.core.embeddings import (
    BGE_M3_MODEL,
    SentenceTransformerBackend,
    halfvec_literal,
)


class QueryEncoder:
    """Load BGE-M3 once and serialize calls through the local model."""

    def __init__(self) -> None:
        self._backend: SentenceTransformerBackend | None = None
        self._lock = Lock()

    @staticmethod
    def model_path() -> str:
        configured = os.getenv("EUROMOD_EMBEDDING_MODEL")
        if configured:
            return configured
        repository_root = Path(__file__).resolve().parents[3]
        local_model = repository_root / "RAG" / "ingest" / "models" / "bge-m3-openvino"
        return str(local_model) if local_model.is_dir() else BGE_M3_MODEL

    def encode_literal(self, query: str) -> str:
        """Return a PostgreSQL halfvec literal for one normalized query vector."""
        if not query.strip():
            raise ValueError("query must not be empty")
        with self._lock:
            if self._backend is None:
                self._backend = SentenceTransformerBackend(
                    model_path=self.model_path(),
                    backend=os.getenv("EUROMOD_EMBEDDING_BACKEND", "openvino"),
                    device=os.getenv("EUROMOD_EMBEDDING_DEVICE", "CPU"),
                )
            return halfvec_literal(self._backend.encode([query])[0])
