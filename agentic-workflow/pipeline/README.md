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

# Parameter store (params schema in the legislation DB — db/params_schema.sql)
uv run euromod-workflow init-param-db
uv run euromod-workflow ingest-params ../../extracted_parameters/enriched/FR.enriched.json
uv run euromod-workflow translate-params --country FR   # law-language search text (real model needed)
uv run euromod-workflow ingest-openfisca ~/Euromod/openfisca-france/openfisca_france/parameters --country FR
```

`ingest-params` accepts both export envelopes (the bare record list and the
0.2.0 `{schema_version, country, parameters, groups}` object) and prefers
received Stage B fields over local derivations. `translate-params` fills
`params.parameter_texts` with law-language renderings of the English
labels/descriptions; `frame` prefers them when building the retrieval query so
the FTS leg of hybrid search is no longer cross-language (see
[Param_Schema/openfisca_france_usage.md](../../Param_Schema/openfisca_france_usage.md) §5).

Configuration: see [../.env.example](../.env.example). Set `WORKFLOW_MODEL`
(e.g. `anthropic/claude-sonnet-5`) to use a real LLM. Traces land in Phoenix
at http://localhost:6006 (project `euromod-agentic-workflow`).

Every run also writes a `params.extraction_runs` row (plus `params.proposals`
and `params.proposal_references`) carrying `phoenix_trace_id`, the OTel trace
id of the run's root span — the link from a stored proposal to the full agent
trace in Phoenix. The same id is on each queue item as `phoenix_trace_id`.
The DB write is best-effort: if the params schema is missing, the run still
completes on the file queue and prints a `[paramdb]` warning.
