"""Long-lived JSON-lines query encoder for local BGE-M3 retrieval."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from nomotheca_ingest.core.embeddings import BGE_M3_MODEL, SentenceTransformerBackend, halfvec_literal


def _default_model_path() -> str:
    local_model = Path("models/bge-m3-openvino")
    return str(local_model) if local_model.is_dir() else BGE_M3_MODEL


def main() -> None:
    parser = argparse.ArgumentParser(description="Encode retrieval queries as normalized BGE-M3 vectors.")
    parser.add_argument("--model-path", default=_default_model_path())
    parser.add_argument("--backend", choices=("torch", "openvino"), default="openvino")
    parser.add_argument("--device", default="CPU")
    args = parser.parse_args()

    backend = SentenceTransformerBackend(
        model_path=args.model_path,
        backend=args.backend,
        device=args.device,
    )
    print(json.dumps({"ready": True, "model": args.model_path}), flush=True)

    for line in sys.stdin:
        try:
            request = json.loads(line)
            query = request["query"].strip()
            if not query:
                raise ValueError("query must not be empty")
            vector = backend.encode([query])[0]
            print(json.dumps({"halfvec": halfvec_literal(vector)}, separators=(",", ":")), flush=True)
        except Exception as exc:
            print(json.dumps({"error": str(exc)}), flush=True)


if __name__ == "__main__":
    main()
