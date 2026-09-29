"""Long-lived JSON-lines query encoder for local retrieval (BGE-M3 unless --model)."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from nomotheca_ingest.core.embedding_models import DEFAULT_MODEL, EmbeddingModelSpec, get_model
from nomotheca_ingest.core.embeddings import (
    SentenceTransformerBackend,
    halfvec_literal,
    torch_module,
)


def _default_backend() -> str:
    """Prefer CUDA over the OpenVINO CPU path when this box has a usable GPU."""
    torch = torch_module()
    return "torch" if torch is not None and torch.cuda.is_available() else "openvino"


def _default_model_path(backend: str, spec: EmbeddingModelSpec = DEFAULT_MODEL) -> str:
    """Return the local export matching the backend, else the Hugging Face id."""
    suffix = "-openvino" if backend == "openvino" else ""
    local_model = Path(f"models/{spec.key}{suffix}")
    return str(local_model) if (local_model / "config.json").is_file() else spec.hf_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Encode retrieval queries as normalized vectors.")
    parser.add_argument("--model", default=str(DEFAULT_MODEL.id), help="Registry key or id (default: 1 = BGE-M3).")
    parser.add_argument("--model-path", default=None)
    parser.add_argument("--backend", choices=("auto", "torch", "openvino"), default="auto")
    parser.add_argument("--device", default=None, help="Default: cuda when available, else the backend default.")
    parser.add_argument("--precision", default="auto")
    args = parser.parse_args()

    spec = get_model(args.model)
    backend_name = _default_backend() if args.backend == "auto" else args.backend
    model_path = args.model_path or _default_model_path(backend_name, spec)
    device = args.device or ("CPU" if backend_name == "openvino" else None)

    backend = SentenceTransformerBackend(
        model_path=model_path,
        backend=backend_name,
        device=device,
        spec=spec,
        precision=args.precision,
    )
    # stdout is a strict JSON-lines protocol; diagnostics go to stderr.
    print(backend.description, file=sys.stderr, flush=True)
    print(
        json.dumps({"ready": True, "model": model_path, "model_id": spec.id, "backend": backend_name}),
        flush=True,
    )

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
        return {"halfvec": halfvec_literal(_encode_queries(backend, [query])[0])}
    sentences = request["sentences"]
    if not isinstance(sentences, list) or not all(isinstance(s, str) for s in sentences):
        raise ValueError("sentences must be a list of strings")
    if not sentences:
        return {"similarities": []}
    query_vector = _encode_queries(backend, [query])[0]
    return {"similarities": [dot(query_vector, v) for v in backend.encode(sentences)]}


def _encode_queries(backend: SentenceTransformerBackend, queries: list[str]) -> list[list[float]]:
    """The query side of an asymmetric model (its prompt); plain encode for a stub backend."""
    encode_queries = getattr(backend, "encode_queries", None)
    return encode_queries(queries) if encode_queries else backend.encode(queries)


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    """Cosine similarity of two already-normalized vectors."""
    return float(sum(x * y for x, y in zip(a, b)))


if __name__ == "__main__":
    main()
