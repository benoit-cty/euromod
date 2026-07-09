# euromod-agentic-workflow (pipeline)

Structured pipeline with LLM steps: frame → retrieve (hybrid SQL over the
legislation DB) → propose (LLM) → critique (mechanical checks + LLM) →
diff/route → human review queue. Traced to Arize Phoenix via OpenTelemetry.

See [../README.md](../README.md) for the architecture document.

```bash
docker compose up -d               # repo root: legislation DB + Phoenix
cd agentic-workflow/pipeline
uv sync
uv run euromod-workflow run-all --as-of 2025-06-01     # mock model, no API key needed
uv run euromod-workflow queue
uv run euromod-workflow export
```

Configuration: see [../.env.example](../.env.example). Set `WORKFLOW_MODEL`
(e.g. `anthropic/claude-sonnet-5`) to use a real LLM. Traces land in Phoenix
at http://localhost:6006 (project `euromod-agentic-workflow`).
