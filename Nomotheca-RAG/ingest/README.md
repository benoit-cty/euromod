# EUROMOD Legislation Ingest

Initial Python implementation of the archive-first ingestion architecture described in
[`../12_ingestion-architecture.md`](../12_ingestion-architecture.md).

The package is library-first: CLI commands call the same `ingest_citation` and
`ingest_instrument` functions that an agentic cache-miss workflow can call in-process.

## Translate unit texts to English

`unit_texts` rows arrive in the source language ('fr', 'nl', ...). The batch
translation worker finds every `legal_unit_versions` row without an English text,
translates its best source text (authentic > official translation > machine
translation) with an LLM, and stores the result as an ordinary `unit_texts` row
with `authenticity='machine_translation'`, `source_lang`, `translation_of` and
`mt_engine` filled in, plus its retrieval `chunks` (run `embeddings build`
afterwards to vectorize them).

The LLM connection reuses
[`nomoscope_workflow.llm`](../../Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/llm.py):
models are provider-prefixed strings (`anthropic/...`, `openai/...`,
`azure_openai/...`, `openrouter/...`, `together/...`) and API keys are read from
the environment / repo `.env` files.

```bash
uv sync --extra embeddings --extra translate   # uv sync installs exactly the listed extras
uv run python -m nomotheca_ingest.cli translate run \
	--database-url postgresql://jrc:jrc@localhost:5434/legislation \
	--model=azure_openai/gpt-5.6-luna
```

`nomoscope_workflow.config.load_config()` only auto-loads `.env` from the `euromod`
repo root and `Nomoscope-agentic-workflow/`;

Use `--dry-run` to count untranslated texts without calling the LLM, `--limit N`
to translate a first batch, and `--target-lang` for another language registered in
`lang_fts_config`. The run is idempotent (already-translated versions are skipped)
and commits after every stored translation, so it can be interrupted and resumed.
Long texts are split into ~6k-character newline-aware segments per LLM call.
A per-text failure is reported and skipped; the command exits non-zero if any
text failed.

## Build embeddings

Ingestion writes `chunks` synchronously. Vector embeddings are derived afterward with
the local BGE-M3 worker command. On an Intel Core Ultra 7 265H, prefer OpenVINO
over ONNX for this local CPU path: it is Intel's inference runtime, tends to have
better CPU/iGPU optimization on this hardware, and is directly supported by
`sentence-transformers`. ONNX Runtime is still useful for portability, but it is
not the first choice for this Intel-only workstation setup.

```bash
uv sync --extra embeddings
uv run python -m nomotheca_ingest.cli embeddings build \
	--database-url postgresql://jrc:jrc@localhost:5434/legislation \
	--model-path BAAI/bge-m3 \
	--backend torch \
	--batch-size 16
```

Use `--model-path /path/to/local/bge-m3` to point at an already downloaded model.
Use `--dry-run` to count chunks that need fresh embeddings without loading the model
or writing rows.

### NVIDIA GPU (CUDA)

OpenVINO cannot drive an NVIDIA card — its GPU plugin is Intel-only — so the
workstation with the GTX 1080 Ti runs the **torch** backend on CUDA instead, and
needs no model export. CUDA and CPU torch wheels cannot share one environment
(they are declared as conflicting extras), so the CUDA build gets its own venv:

```bash
UV_PROJECT_ENVIRONMENT=.venv-cuda uv sync --extra embeddings-cuda
UV_PROJECT_ENVIRONMENT=.venv-cuda uv run python -m nomotheca_ingest.cli embeddings build \
	--database-url postgresql://jrc:jrc@localhost:5434/legislation \
	--backend torch \
	--batch-size 64 \
	--encode-batch-size 16
```

Measured on this box (Threadripper 1950X + GTX 1080 Ti), 128 chunk-sized French
fiscal texts (~3.9k characters each): **6.8 s on the GPU (18.7 chunks/s) against
137.8 s on the CPU (0.93 chunks/s)** — about 20x, i.e. the 329-chunk French
fiscal bill drops from minutes to ~18 s. An encode batch of 16 was the fastest;
8 gave 16.7 chunks/s and 32 or 64 fell back to ~12.5, so raise `--batch-size`
(commit granularity) rather than `--encode-batch-size` on this card.

The default `.venv` (`uv sync --extra embeddings`) keeps CPU torch + OpenVINO, so
the Tauri UI and `scout.py` — both of which spawn `uv run --extra embeddings` —
are unaffected.

With `--backend torch` and no `--device`, the build picks CUDA when a GPU is
visible and CPU otherwise (`--device cpu` forces the old path, `--device cuda:1`
selects a card, `--device auto` is the explicit spelling of the default). The
resolved device is printed on stderr, stdout stays reserved for the `@progress`
protocol:

```
backend=torch device=cuda gpu=NVIDIA GeForce GTX 1080 Ti vram=10.9GiB sm_61 dtype=float32
```

`query_embeddings.py` (the long-lived query encoder the UI and the workflow
spawn) makes the same choice: `--backend auto` prefers torch+CUDA when a GPU is
present and falls back to the local OpenVINO export otherwise.

Three things are specific to this card:

- **fp32, not fp16.** Pascal (sm_61) runs half precision at 1/64 of its fp32
  rate, so half precision is only requested from Volta (sm_70) on.
- **CUDA 12.6 wheels.** `embeddings-cuda` is routed to the cu126 index because
  the cu128+ channels start at sm_75 and CUDA 13 dropped Pascal outright. A
  torch build without kernels for the installed GPU is rejected at model load,
  with the arch list it does ship, instead of failing mid-run with "no kernel
  image is available for execution on the device".
- **`--encode-batch-size`** caps how many chunks enter one forward pass, so
  `--batch-size` can stay large (it is the commit granularity) without
  overflowing 11 GB of VRAM; it defaults to `--batch-size`. A CUDA
  out-of-memory halves the encode batch and retries instead of losing the run,
  and the smaller size sticks for the remaining batches. The run above peaked
  well under the card's memory, so OOM should only appear on unusually long
  chunks.

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
cd Nomotheca-RAG/ingest
uv run python -m nomotheca_ingest.cli embeddings build \
	--database-url postgresql://jrc:jrc@localhost:5434/legislation \
	--model-path models/bge-m3-openvino \
	--backend openvino \
	--device cpu \
	--batch-size 16
```

For the 329 chunks of the French fiscal bill it tooks 13 minutes on a Intel Ultra 7 265H, in cpu mode.

The command shows a live progress bar by default. Use `--no-progress` when
capturing logs in non-interactive scripts, or `--progress-json` to emit
machine-readable `@progress {json}` lines on stdout (one per encoded batch,
with an upfront total) — this is what the desktop UI's Ingest tab uses to
render its progress bar. `translate run` supports the same two flags.

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

#### Intel NPU usage

The command never asked for the NPU. embeddings build has a --device option, and without it OpenVINO falls back to its default device, which is CPU (cli.py:140, core/embeddings.py:108-115). That's also the documented intent in CLAUDE.md: OpenVINO was chosen over ONNX for the local CPU path on the Ultra 7 265H, not for NPU offload. The 71% CPU is the embedding work happening where it was routed.

Even if you passed --device NPU, it can't work under WSL. I just checked inside your venv: openvino.Core().available_devices returns ['CPU'], and there is no /dev/accel device node. WSL2 paravirtualizes the GPU (via /dev/dxg) but does not pass through the Intel NPU — Microsoft/Intel haven't shipped NPU passthrough for WSL2, so no Linux process in WSL can see it. Passing --device NPU would just make OpenVINO error out with "device not found".

If you actually want the NPU used, the realistic paths are:

Run the embedding build from native Windows (Windows Python + OpenVINO with the Intel NPU driver installed), pointing --database-url at the same Postgres on localhost:5434. Caveat: BGE-M3 uses dynamic input shapes, which the NPU plugin handles poorly — you'd likely need to reshape/pad to a static sequence length, and **throughput for this model may not beat the CPU anyway.**

Otherwise, stay on CPU in WSL — that's the supported, tested path for this repo. If 71% CPU is too disruptive, lowering --batch-size or nice-ing the process is simpler than chasing the NPU.
