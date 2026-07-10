"""Export BGE-M3 to a local OpenVINO sentence-transformers model directory."""

from __future__ import annotations

import argparse
from importlib import import_module
from pathlib import Path
import sys
from typing import Any

from euromod_ingest.core.embeddings import processor_kwargs_for


TORCH_EXPORT_DEVICE = "cpu"
OPENVINO_EXPORT_DEVICE = "CPU"
OPENVINO_NPU_COMPILER_ISSUE_URL = "https://github.com/openvinotoolkit/openvino/issues/36374"
NPU_COMPILER_LOADER_LIBRARY = "libopenvino_intel_npu_compiler_loader.so"


def openvino_export_model_kwargs() -> dict[str, object]:
    """Return OpenVINO backend kwargs for conversion without device compilation."""
    return {"export": True, "device": OPENVINO_EXPORT_DEVICE, "compile": False}


def openvino_validation_model_kwargs(device: str) -> dict[str, object]:
    """Return OpenVINO backend kwargs for post-export validation."""
    return {"device": device.upper()}


def main() -> None:
    """Export a Hugging Face/SentenceTransformers model to OpenVINO IR."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-model", default="BAAI/bge-m3", help="Source model id or local Torch model directory.")
    parser.add_argument("--output-dir", default="models/bge-m3-openvino", help="Directory for the exported OpenVINO model.")
    parser.add_argument("--device", default="CPU", help="OpenVINO target used for export validation, usually CPU.")
    parser.add_argument("--strict-device", action="store_true", help="Fail if validation cannot compile on --device.")
    parser.add_argument("--trust-remote-code", action="store_true", help="Forward trust_remote_code to sentence-transformers.")
    parser.add_argument("--fix-mistral-regex", action="store_true", help="Forward fix_mistral_regex=True to the tokenizer.")
    parser.add_argument("--slow-tokenizer", action="store_true", help="Use the slow tokenizer; may require sentencepiece.")
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
        device=TORCH_EXPORT_DEVICE,
        trust_remote_code=args.trust_remote_code,
        model_kwargs=openvino_export_model_kwargs(),
        processor_kwargs=processor_kwargs_for(
            fix_mistral_regex=args.fix_mistral_regex,
            slow_tokenizer=args.slow_tokenizer,
        ),
    )
    model.save_pretrained(output_dir)

    sample = ["passage: Code general des impots > Art. 197\nBareme de l'impot sur le revenu."]
    validation_device = args.device.upper()
    vector, actual_device = _validate_export(
        sentence_transformers,
        output_dir,
        sample,
        validation_device=validation_device,
        strict_device=args.strict_device,
        trust_remote_code=args.trust_remote_code,
        fix_mistral_regex=args.fix_mistral_regex,
        slow_tokenizer=args.slow_tokenizer,
    )
    print(f"exported={output_dir}")
    print(f"backend=openvino device={actual_device} dim={len(vector)}")


def _validate_export(
    sentence_transformers: Any,
    output_dir: Path,
    sample: list[str],
    *,
    validation_device: str,
    strict_device: bool,
    trust_remote_code: bool,
    fix_mistral_regex: bool,
    slow_tokenizer: bool,
) -> tuple[object, str]:
    """Validate exported IR, falling back to CPU when an optional device is unavailable."""
    try:
        vector = _encode_sample(
            sentence_transformers,
            output_dir,
            sample,
            device=validation_device,
            trust_remote_code=trust_remote_code,
            fix_mistral_regex=fix_mistral_regex,
            slow_tokenizer=slow_tokenizer,
        )
        return vector, validation_device
    except RuntimeError as exc:
        if strict_device or validation_device == OPENVINO_EXPORT_DEVICE:
            msg = _validation_failure_message(validation_device, exc, fallback=False)
            raise SystemExit(msg) from None
        print(
            _validation_failure_message(validation_device, exc, fallback=True),
            file=sys.stderr,
        )
        vector = _encode_sample(
            sentence_transformers,
            output_dir,
            sample,
            device=OPENVINO_EXPORT_DEVICE,
            trust_remote_code=trust_remote_code,
            fix_mistral_regex=fix_mistral_regex,
            slow_tokenizer=slow_tokenizer,
        )
        return vector, OPENVINO_EXPORT_DEVICE


def _encode_sample(
    sentence_transformers: Any,
    output_dir: Path,
    sample: list[str],
    *,
    device: str,
    trust_remote_code: bool,
    fix_mistral_regex: bool,
    slow_tokenizer: bool,
) -> object:
    """Load the exported model on one OpenVINO device and encode a sample."""
    model = sentence_transformers.SentenceTransformer(
        str(output_dir),
        backend="openvino",
        device=TORCH_EXPORT_DEVICE,
        trust_remote_code=trust_remote_code,
        model_kwargs=openvino_validation_model_kwargs(device),
        processor_kwargs=processor_kwargs_for(
            fix_mistral_regex=fix_mistral_regex,
            slow_tokenizer=slow_tokenizer,
        ),
    )
    return model.encode(sample, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False)[0]


def _validation_failure_detail(exc: RuntimeError) -> str:
    """Return a concise explanation for known OpenVINO validation failures."""
    message = str(exc)
    if NPU_COMPILER_LOADER_LIBRARY in message:
        return (
            f"OpenVINO's Linux NPU package is missing {NPU_COMPILER_LOADER_LIBRARY}. "
            f"This matches upstream issue {OPENVINO_NPU_COMPILER_ISSUE_URL}."
        )
    return message


def _validation_failure_message(validation_device: str, exc: RuntimeError, *, fallback: bool) -> str:
    """Return the operator-facing validation failure message."""
    detail = _validation_failure_detail(exc)
    if fallback:
        return (
            f"warning: OpenVINO validation on {validation_device} failed; "
            f"exported model was saved and CPU validation will be used.\n{detail}"
        )
    return (
        f"OpenVINO validation on {validation_device} failed after the exported model was saved.\n"
        f"{detail}\n"
        "Run without --strict-device to keep the export and validate on CPU."
    )


if __name__ == "__main__":
    main()