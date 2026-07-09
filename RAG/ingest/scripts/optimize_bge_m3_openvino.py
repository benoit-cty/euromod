"""Export BGE-M3 to a local OpenVINO sentence-transformers model directory."""

from __future__ import annotations

import argparse
from importlib import import_module
from pathlib import Path


def main() -> None:
    """Export a Hugging Face/SentenceTransformers model to OpenVINO IR."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-model", default="BAAI/bge-m3", help="Source model id or local Torch model directory.")
    parser.add_argument("--output-dir", default="models/bge-m3-openvino", help="Directory for the exported OpenVINO model.")
    parser.add_argument("--device", default="CPU", help="OpenVINO target used for export validation, usually CPU.")
    parser.add_argument("--trust-remote-code", action="store_true", help="Forward trust_remote_code to sentence-transformers.")
    args = parser.parse_args()

    try:
        sentence_transformers = import_module("sentence_transformers")
    except ImportError as exc:
        msg = "Install dependencies first: uv sync --extra embeddings"
        raise SystemExit(msg) from exc

    output_dir = Path(args.output_dir)
    output_dir.parent.mkdir(parents=True, exist_ok=True)

    model = sentence_transformers.SentenceTransformer(
        args.source_model,
        backend="openvino",
        device=args.device,
        trust_remote_code=args.trust_remote_code,
        model_kwargs={"export": True},
    )
    model.save_pretrained(output_dir)

    sample = ["passage: Code general des impots > Art. 197\nBareme de l'impot sur le revenu."]
    vector = model.encode(sample, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False)[0]
    print(f"exported={output_dir}")
    print(f"backend=openvino device={args.device} dim={len(vector)}")


if __name__ == "__main__":
    main()