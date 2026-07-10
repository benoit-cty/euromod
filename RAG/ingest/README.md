# EUROMOD Legislation Ingest

Initial Python implementation of the archive-first ingestion architecture described in
[`../12_ingestion-architecture.md`](../12_ingestion-architecture.md).

The package is library-first: CLI commands call the same `ingest_citation` and
`ingest_instrument` functions that an agentic cache-miss workflow can call in-process.

## Build embeddings

Ingestion writes `chunks` synchronously. Vector embeddings are derived afterward with
the local BGE-M3 worker command. On an Intel Core Ultra 7 265H, prefer OpenVINO
over ONNX for this local CPU path: it is Intel's inference runtime, tends to have
better CPU/iGPU optimization on this hardware, and is directly supported by
`sentence-transformers`. ONNX Runtime is still useful for portability, but it is
not the first choice for this Intel-only workstation setup.

```bash
uv sync --extra embeddings
uv run python -m euromod_ingest.cli embeddings build \
	--database-url postgresql://jrc:jrc@localhost:5434/legislation \
	--model-path BAAI/bge-m3 \
	--backend torch \
	--batch-size 16
```

Use `--model-path /path/to/local/bge-m3` to point at an already downloaded model.
Use `--dry-run` to count chunks that need fresh embeddings without loading the model
or writing rows.

### OpenVINO export

Export the canonical `BAAI/bge-m3` model to a local OpenVINO directory:

```bash
uv run python scripts/optimize_bge_m3_openvino.py \
	--source-model models/bge-m3 \
	--output-dir models/bge-m3-openvino \
	--device cpu
```

Then build embeddings with the exported model:

```bash
uv run python -m euromod_ingest.cli embeddings build \
	--database-url postgresql://jrc:jrc@localhost:5434/legislation \
	--model-path models/bge-m3-openvino \
	--backend openvino \
	--device cpu \
	--batch-size 16
```

For the 329 chunks of the French fiscal bill it tooks 13 minutes on a Intel Ultra 7 265H, in cpu mode.

The command shows a live progress bar by default. Use `--no-progress` when
capturing logs in non-interactive scripts.

Use `CPU` first on the Ultra 7 265H. OpenVINO can expose other devices depending
on the installed drivers, but BGE-M3 should be benchmarked before targeting the
iGPU or NPU. If you pass `--device cpu`, OpenVINO will not use the NPU; try
`--device NPU` or `--device AUTO` only after confirming those devices are listed
by your OpenVINO installation. For both export and embedding builds, the script
keeps the SentenceTransformers/Torch wrapper on CPU and forwards `--device` to
the OpenVINO backend; passing `--device NPU` should therefore fail only if
OpenVINO itself cannot see or compile for the NPU.

The export script saves the OpenVINO IR before device validation. If NPU
validation fails because the Intel NPU compiler plugin is missing, the exported
model remains usable on CPU and the script falls back to CPU validation. Add
`--strict-device` if you want the export command to fail instead. The missing
`libopenvino_intel_npu_compiler_loader.so` failure is tracked upstream in
[openvinotoolkit/openvino#36374](https://github.com/openvinotoolkit/openvino/issues/36374);
it means the PyPI Linux OpenVINO package can expose the NPU plugin while omitting
the plugin compiler libraries needed for NPU compilation.

Transformers may print a `fix_mistral_regex=True` warning for this exported
XLM-R/BGE tokenizer. Do not enable that flag for BGE-M3 unless a future
Transformers release fixes it: in the current stack it breaks loading with
`Metaspace object does not support item assignment`. The CLI exposes
`--fix-mistral-regex` only as an opt-in for models that actually need it.

