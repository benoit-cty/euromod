"""Long-lived JSON-lines query encoder for local BGE-M3 retrieval."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from nomotheca_ingest.core.embeddings import (
    BGE_M3_MODEL,
    SentenceTransformerBackend,
    halfvec_literal,
    torch_module,
)


def _default_backend() -> str:
    """Prefer CUDA over the OpenVINO CPU path when this box has a usable GPU."""
    torch = torch_module()
    return "torch" if torch is not None and torch.cuda.is_available() else "openvino"


def _default_model_path(backend: str) -> str:
    """Return the local export matching the backend, else the Hugging Face id."""
    local_model = Path("models/bge-m3-openvino") if backend == "openvino" else Path("models/bge-m3")
    return str(local_model) if (local_model / "config.json").is_file() else BGE_M3_MODEL


def main() -> None:
    parser = argparse.ArgumentParser(description="Encode retrieval queries as normalized BGE-M3 vectors.")
    parser.add_argument("--model-path", default=None)
    parser.add_argument("--backend", choices=("auto", "torch", "openvino"), default="auto")
    parser.add_argument("--device", default=None, help="Default: cuda when available, else the backend default.")
    args = parser.parse_args()

    backend_name = _default_backend() if args.backend == "auto" else args.backend
    model_path = args.model_path or _default_model_path(backend_name)
    device = args.device or ("CPU" if backend_name == "openvino" else None)

    backend = SentenceTransformerBackend(
        model_path=model_path,
        backend=backend_name,
        device=device,
    )
    # stdout is a strict JSON-lines protocol; diagnostics go to stderr.
    print(backend.description, file=sys.stderr, flush=True)
    print(json.dumps({"ready": True, "model": model_path, "backend": backend_name}), flush=True)

    for line in sys.stdin:
        try:
            print(json.dumps(handle_request(backend, json.loads(line)), separators=(",", ":")), flush=True)
        except Exception as exc:
            print(json.dumps({"error": str(exc)}), flush=True)


def handle_request(backend: SentenceTransformerBackend, request: dict) -> dict:
    """Serve one JSON-lines request.

    ``{"query": q}`` answers ``{"halfvec": ...}`` for retrieval;
    ``{"query": q, "sentences": [...]}`` answers ``{"similarities": [...]}``, the
    cosine of each sentence against the query, so the Database tab can tint the
    sentence of a hit that most likely answers the question. One batch per
    request: the encoder is the slow part, not the dot products.
    """
    query = str(request.get("query", "")).strip()
    if not query:
        raise ValueError("query must not be empty")
    if "sentences" not in request:
        return {"halfvec": halfvec_literal(backend.encode([query])[0])}
    sentences = request["sentences"]
    if not isinstance(sentences, list) or not all(isinstance(s, str) for s in sentences):
        raise ValueError("sentences must be a list of strings")
    if not sentences:
        return {"similarities": []}
    vectors = backend.encode([query] + sentences)
    return {"similarities": [dot(vectors[0], v) for v in vectors[1:]]}


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    """Cosine similarity of two already-normalized vectors."""
    return float(sum(x * y for x, y in zip(a, b)))


if __name__ == "__main__":
    main()
