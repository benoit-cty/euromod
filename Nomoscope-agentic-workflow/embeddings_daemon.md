# Embeddings Daemon

A daemon was implemented as part of the Database tab's semantic search. It's lifetime is tied to the UI. Here's how it fits together:

## The three pieces

### Python side
query_embeddings.py is a long-lived JSON-lines worker: it loads BGE-M3 once, prints {"ready": true}, then reads one query per line from stdin and answers with a pgvector halfvec literal on stdout. Its default backend is auto: torch on CUDA when the machine has a usable GPU, otherwise the local OpenVINO export in Nomotheca-RAG/ingest/models/bge-m3-openvino. Diagnostics (the resolved device) go to stderr — stdout is the protocol.

### Rust side
encoder.rs manages it as EmbeddingState: it spawns uv run --extra embeddings python -m nomotheca_ingest.query_embeddings inside the ingest package dir (located by walking up, or via EUROMOD_INGEST_DIR), waits for the ready handshake, and keeps the process behind a mutex. If an encode fails it kills and respawns once, transparently. The extra it passes is chosen by ingest.rs::embedding_environment, so the UI's semantic search runs on the GPU wherever .venv-cuda is installed.

### Wiring
lib.rs:150-159: the search_articles command calls state.encode(...) only when the search mode uses vectors, then passes the vector into the hybrid SQL search in db.rs.
Lifecycle — only while the UI runs, and even less than that

The process is spawned lazily: nothing starts at UI launch. The model only loads the first time you run a semantic or hybrid search in the Database tab (so the first search pays the model-load latency; subsequent searches are fast).
It stays warm for the rest of the session, and dies when the UI closes — the guarantee isn't the Rust Drop (Tauri exits via process::exit, so destructors may not run) but the pipe itself: when the UI process ends, the kernel closes the encoder's stdin, its for line in sys.stdin loop hits EOF, and the Python process exits on its own. That holds even if the UI crashes or is force-killed, so you won't get an orphaned multi-GB model process.

The only prerequisite is that the ingest package has its embeddings extra synced (uv sync --extra embeddings in Nomotheca-RAG/ingest) — otherwise the spawn fails and the search falls back with an error.

## GPU

On a machine with an NVIDIA card, the ingest package's CUDA wheels live in a second environment (UV_PROJECT_ENVIRONMENT=.venv-cuda uv sync --extra embeddings-cuda; CUDA and CPU torch are conflicting extras). query_encoder.embedding_process() is the single place that decides: if that environment exists it runs uv with --extra embeddings-cuda and UV_PROJECT_ENVIRONMENT pointed at it, otherwise nothing changes. scout.py's incremental embeddings build goes through the same helper — and skips the OpenVINO model path there, since the IR only loads under the OpenVINO backend. The Rust side has the same decision in ingest.rs::embedding_environment, used by both the encoder daemon and the Ingest tab's embeddings build (which logs the environment it picked). Measured on the GTX 1080 Ti box: ~18.7 chunks/s against ~0.93 on the CPU.
