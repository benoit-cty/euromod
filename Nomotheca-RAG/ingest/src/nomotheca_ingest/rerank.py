"""Long-lived JSON-lines cross-encoder scorer (the reranker twin of query_embeddings).

``{"query": q, "passages": [...]}`` answers ``{"scores": [...]}``, one relevance
score per passage, higher is more relevant. stdout is the protocol; diagnostics
go to stderr.
"""

from __future__ import annotations

import argparse
import json
import sys
from importlib import import_module
from typing import Any

from nomotheca_ingest.core.embeddings import (
    cuda_oom_errors,
    is_cuda_device,
    raise_for_unsupported_cuda_arch,
    resolve_torch_device,
    torch_module,
)
from nomotheca_ingest.core.rerankers import RerankerSpec, get_reranker


class CrossEncoderReranker:
    """A sentence-transformers CrossEncoder, fp32 (see embeddings.CUDA_FP16_MIN_CAPABILITY)."""

    def __init__(self, spec: RerankerSpec, device: str | None = None, batch_size: int = 8) -> None:
        sentence_transformers = import_module("sentence_transformers")
        self.spec = spec
        self.device = resolve_torch_device(device, backend="torch")
        self._torch = torch_module() if is_cuda_device(self.device) else None
        if self._torch is not None:
            raise_for_unsupported_cuda_arch(self._torch, self.device)
        self.batch_size = batch_size
        self.model = sentence_transformers.CrossEncoder(
            spec.hf_id, device=self.device, max_length=spec.max_length
        )

    def score(self, query: str, passages: list[str]) -> list[float]:
        pairs = [self.spec.pair(query, passage) for passage in passages]
        while True:
            try:
                scores = self.model.predict(pairs, batch_size=self.batch_size, show_progress_bar=False)
                return [float(score) for score in scores]
            except cuda_oom_errors(self._torch):
                if self.batch_size <= 1:
                    raise
                self.batch_size = max(1, self.batch_size // 2)
                print(f"warning: CUDA out of memory; rerank batch size {self.batch_size}", file=sys.stderr)
                self._torch.cuda.empty_cache()


def handle_request(reranker: Any, request: dict) -> dict:
    query = str(request.get("query", "")).strip()
    if not query:
        raise ValueError("query must not be empty")
    passages = request.get("passages")
    if not isinstance(passages, list) or not all(isinstance(p, str) for p in passages):
        raise ValueError("passages must be a list of strings")
    return {"scores": reranker.score(query, passages) if passages else []}


def main() -> None:
    parser = argparse.ArgumentParser(description="Score (query, passage) pairs with a cross-encoder.")
    parser.add_argument("--model", default="bge-reranker-v2-m3", help="Reranker registry key.")
    parser.add_argument("--device", default=None)
    args = parser.parse_args()

    reranker = CrossEncoderReranker(get_reranker(args.model), device=args.device)
    print(f"reranker={args.model} device={reranker.device}", file=sys.stderr, flush=True)
    print(json.dumps({"ready": True, "model": args.model}), flush=True)
    for line in sys.stdin:
        try:
            print(json.dumps(handle_request(reranker, json.loads(line)), separators=(",", ":")), flush=True)
        except Exception as exc:
            print(json.dumps({"error": str(exc)}), flush=True)


if __name__ == "__main__":
    main()
