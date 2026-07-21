# Embeddings Daemon

A daemon was implemented as part of the Database tab's semantic search. It's lifetime is tied to the UI. Here's how it fits together:

## The three pieces

### Python side
query_embeddings.py is a long-lived JSON-lines worker: it loads BGE-M3 once (preferring the local OpenVINO export in Nomotheca-RAG/ingest/models/bge-m3-openvino, which is present on disk), prints {"ready": true}, then reads one query per line from stdin and answers with a pgvector halfvec literal on stdout.

### Rust side
encoder.rs manages it as EmbeddingState: it spawns uv run --extra embeddings python -m nomotheca_ingest.query_embeddings inside the ingest package dir (located by walking up, or via EUROMOD_INGEST_DIR), waits for the ready handshake, and keeps the process behind a mutex. If an encode fails it kills and respawns once, transparently.

### Wiring
lib.rs:150-159: the search_articles command calls state.encode(...) only when the search mode uses vectors, then passes the vector into the hybrid SQL search in db.rs.
Lifecycle — only while the UI runs, and even less than that

The process is spawned lazily: nothing starts at UI launch. The model only loads the first time you run a semantic or hybrid search in the Database tab (so the first search pays the model-load latency; subsequent searches are fast).
It stays warm for the rest of the session, and dies when the UI closes — the guarantee isn't the Rust Drop (Tauri exits via process::exit, so destructors may not run) but the pipe itself: when the UI process ends, the kernel closes the encoder's stdin, its for line in sys.stdin loop hits EOF, and the Python process exits on its own. That holds even if the UI crashes or is force-killed, so you won't get an orphaned multi-GB model process.

The only prerequisite is that the ingest package has its embeddings extra synced (uv sync --extra embeddings in Nomotheca-RAG/ingest) — otherwise the spawn fails and the search falls back with an error.
