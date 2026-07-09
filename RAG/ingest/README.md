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
	--source-model BAAI/bge-m3 \
	--output-dir models/bge-m3-openvino \
	--device CPU
```

Then build embeddings with the exported model:

```bash
uv run python -m euromod_ingest.cli embeddings build \
	--database-url postgresql://jrc:jrc@localhost:5434/legislation \
	--model-path models/bge-m3-openvino \
	--backend openvino \
	--device CPU \
	--batch-size 16
```

Use `CPU` first on the Ultra 7 265H. OpenVINO can expose other devices depending
on the installed drivers, but BGE-M3 should be benchmarked before targeting the
iGPU or NPU.

