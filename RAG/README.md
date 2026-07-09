# RAG Pipeline

## Start the stack

From the repo root (PostgreSQL + pgAdmin + Phoenix, schema and seed auto-applied):

```sh
docker compose up
```

- pgAdmin: http://localhost:5050
- Phoenix (LLM traces / evals): http://localhost:6006

## Start the ingest

```sh
cd RAG/ingest
uv run python -m euromod_ingest.cli tui
```
