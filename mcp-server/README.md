# EUROMOD legislation MCP server

Model Context Protocol tools for the shared legislation database. The server
accepts English queries and supports full-text, multilingual BGE-M3 vector, or
reciprocal-rank-fused hybrid retrieval. It returns citable chunk IDs, provenance,
and the component ranks used to build each result.

The server **never loads a model** (ADR 0004). A hybrid or vector query is
encoded by submitting an `encode` job to `ops.jobs`; the Nomergon worker keeps
BGE-M3 warm in its priority lane, writes `{"halfvec": "[...]"}` into the job's
`result`, and the server polls the row every 100 ms. Full-text calls need no
worker at all.

## Tools

- `search_legislation` searches bounded legislation chunks with optional country,
  point-in-time, and language filters. `hybrid` is the default mode.
- `get_legislation_chunk` resolves one exact chunk UUID for citation and quote
  verification.

The server exposes no arbitrary SQL. Search and chunk lookup run on a read-only
connection with a 30-second statement timeout; job submission uses a second,
autocommit connection with the same login.

## Requirements

- PostgreSQL with the legislation schema, `params`, and `ops` (applied by
  `docker compose up -d` at the repo root; on an existing dev database run
  `docker exec -i nomotheca-legislation-db psql -U jrc -d legislation < Nomergon-worker/db/ops_schema.sql`).
- **A login in `nomos_reviewer`** (`Nomergon-worker/db/roles.sql`): the server
  needs SELECT everywhere, INSERT on `ops.jobs` and UPDATE of `cancel_requested`
  on its own jobs. Read-only logins can only serve `mode="full_text"`. The dev
  stack's `jrc` superuser works as-is.
- **A running Nomergon worker** for `hybrid` / `vector` modes. The server checks
  `ops.workers.heartbeat_at` (within 60 s) before submitting and refuses with a
  clear error naming the worker when none is alive; it does not queue a job that
  nothing will run.
- Model-1 (BGE-M3) embeddings built for the corpus, which is itself an `embed`
  job the worker runs.

## Run

```bash
cd ..
docker compose up -d
# start the worker, see Nomergon-worker/README.md
cd mcp-server
uv sync
uv run nomotheca-legislation-mcp
```

Configuration:

- `DATABASE_URL` defaults to `postgresql://jrc:jrc@localhost:5434/legislation`;
  in a shared deployment it carries the analyst's own login.
- `EUROMOD_ENCODE_TIMEOUT` seconds to wait for the worker to encode one query
  (default `60`). On expiry the job's `cancel_requested` is set and the tool
  fails with the worker's status (busy behind a batch, or gone).

The old `EUROMOD_EMBEDDING_MODEL` / `EUROMOD_EMBEDDING_BACKEND` /
`EUROMOD_EMBEDDING_DEVICE` variables are gone: the model path is the worker's
`WORKER_EMBEDDING_MODEL_PATH`.

## Test and debug

```bash
uv sync
uv run pytest
uv run mcp dev src/nomotheca_mcp/server.py
```

`tests/test_encoder.py` drives the polling loop with a fake connection (no
database). Its last test is a smoke test that skips itself unless the dev
Postgres at `localhost:5434` with `ops.jobs` is reachable; it inserts a real
`encode` job, completes it from a thread the way the worker would, and reads
the vector back.

The repository's `.vscode/mcp.json` also registers the stdio server for VS Code.
