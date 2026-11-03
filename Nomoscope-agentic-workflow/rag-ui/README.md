# Nomoscope RAG chat (`rag-ui`)

A small Tauri 2 + Svelte 5 desktop app: chat with the Nomotheca legislation corpus, see every
passage behind an answer, and find official acts the corpus is missing. It is the RAG search of
the review UI (`../ui`) without the review queue, parameters, evaluation or ingestion tabs.

It follows the same rule (ADR 0004): **the app executes nothing and holds one credential, the
analyst's Postgres login.** Each question is a `chat` job in `ops.jobs`. The worker answers it
by running `nomoscope-workflow chat`, a PydanticAI agent with four tools:

| tool | what it does |
|---|---|
| `search_legislation` | `retrieval.hybrid_search`: FTS + BGE-M3, version in force on the date, `context` class excluded, Spanish regions scoped as ADR 0003 |
| `find_article` | `retrieval.locate_named_units`: a named act/article, looked up without ranking |
| `read_article` | every chunk of the article a hit belongs to, plus its provenance |
| `web_search` | Tavily, restricted to the country's official portals (`scout.COUNTRY_SOURCES`); ids found in result URLs are checked against the corpus |

Two guarantees carry over from the pipeline:

- **Quotes are mechanical.** Every quote in an answer is checked character-for-character
  (whitespace-tolerant) against the chunk it names. A mistyped chunk id is resolved by its
  extract when exactly one retrieved chunk contains it. The model gets one retry. A quote
  still unverified after that is shown flagged ✗, never dropped silently.
- **Web text is never evidence.** Web results are leads. An official act the corpus lacks is
  listed as a *discovery*. **Ingest** submits the normal archive-first `ingest` job and then an
  `embed` job. Ask again once it is in.

Conversations are rows too: every turn's job carries a `conversation_id` and the conversation
so far, and **History** rebuilds a conversation from the caller's own `chat` jobs.

The **Search** tab runs the review UI's Database-tab query directly, with no LLM. The job
channel (`jobs.rs`) and the search SQL (`db.rs`) are the review UI's own files, compiled in
with `#[path]`, so the two apps cannot drift.

## Run

The stack and a worker must be up (`docker compose --profile gpu up -d` from the repo root;
rebuild the worker image after pulling this change). The model picker offers what the worker
publishes (`WORKER_MODELS`); `mock/…` runs a key-less, deterministic turn (one search, top
passages quoted). Web search needs `TAVILY_API_KEY` on the worker.

```bash
npm install
npm run tauri dev          # WSL: prefix LIBGL_ALWAYS_SOFTWARE=1; Vite on :5174, beside the review UI's :5173
npm test                   # markdown rendering, message building, extract location
```

`WORKFLOW_DATABASE_URL` selects the database (default `postgresql://jrc:jrc@localhost:5434/legislation`).
A database created before the `chat` job type existed is widened by `Nomergon-worker/db/ops_schema.sql`
(applied at worker start; in a shared deployment the schema owner applies it once).
