# EUROMOD legislation MCP server

Read-only Model Context Protocol tools for the shared legislation database.
The server accepts English queries and supports full-text, multilingual BGE-M3
vector, or reciprocal-rank-fused hybrid retrieval. It returns citable chunk IDs,
provenance, and the component ranks used to build each result.

## Tools

- `search_legislation` searches bounded legislation chunks with optional country,
  point-in-time, and language filters. `hybrid` is the default mode.
- `get_legislation_chunk` resolves one exact chunk UUID for citation and quote
  verification.

The server exposes no arbitrary SQL and opens PostgreSQL in read-only mode with a
30-second statement timeout.

## Run

Start PostgreSQL and ensure model-1 embeddings have been built:

```bash
cd ..
docker compose up -d
cd RAG/ingest
uv run euromod-ingest embeddings build --backend openvino
```

Then run the stdio server:

```bash
cd ../../mcp-server
uv sync
uv run euromod-legislation-mcp
```

Configuration:

- `DATABASE_URL` defaults to `postgresql://jrc:jrc@localhost:5434/legislation`.
- `EUROMOD_EMBEDDING_MODEL` overrides the local BGE-M3/OpenVINO model path.
- `EUROMOD_EMBEDDING_BACKEND` defaults to `openvino`.
- `EUROMOD_EMBEDDING_DEVICE` defaults to `CPU`.

The first hybrid or vector call loads BGE-M3 and is slower; later calls reuse the
same in-process model. Full-text calls do not load the model.

## Test and debug

```bash
uv run --with pytest pytest
uv run mcp dev src/euromod_mcp/server.py
```

The repository's `.vscode/mcp.json` also registers the stdio server for VS Code.
