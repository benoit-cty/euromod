# nomoscope-agentic-workflow (pipeline)

Structured pipeline with LLM steps: frame → retrieve (hybrid SQL over the
legislation DB) → propose (LLM) → critique (mechanical checks + LLM) →
diff/route → human review queue. Traced to Arize Phoenix via OpenTelemetry.

See [../README.md](../README.md) for the architecture document.

```bash
docker compose up -d               # repo root: legislation DB + Phoenix
cd Nomoscope-agentic-workflow/pipeline
uv sync
uv run nomoscope-workflow run-targets group:FR:tinkt_fr:tin_schedule 'euromod://FR/tin_fr/def_const/$tinrt_cdhr' --year 2025   # mock model, no API key needed
uv run nomoscope-workflow run-country FR --year 2025 --limit 20   # every FR parameter in the params DB (then its bracket-schedule groups)
uv run nomoscope-workflow queue --country FR --status pending
uv run nomoscope-workflow export --out-dir export                # one <CC>_accepted.json per country

# Parameter store (params schema in the legislation DB — db/params_schema.sql)
uv run nomoscope-workflow init-param-db
uv run nomoscope-workflow ingest-params ../../extracted_parameters/enriched/FR.enriched.json
uv run nomoscope-workflow ingest-params ../../extracted_parameters/curated/FR.in_function.json  # in-function params the connector cannot export
uv run nomoscope-workflow curate-params curation/FR.curation.yaml
uv run nomoscope-workflow translate-params --country FR   # law-language search text (real model needed)
uv run nomoscope-workflow ingest-openfisca ~/Euromod/openfisca-france/openfisca_france/parameters --country FR
uv run nomoscope-workflow match-openfisca --country FR --dry-run             # EUROMOD <-> OpenFisca link suggestions
uv run nomoscope-workflow match-openfisca --seed openfisca_fr.json   # a selection exported with `nomokrisis-eval selection-export FR --kind openfisca`
```

**Nothing runtime lives on disk** (ADR 0004). Parameters are read straight from
`params.*` (`run-targets` takes `euromod://…` targets or `group:<id>`;
`run-country` runs a whole country); every run writes its `ReviewItem` as a row
of `params.review_queue`, keyed `<country>_<target>_<system year>` so a re-run
replaces a pending review and never a decided one (unless `--force`). The UI
reads the queue from the DB and records a decision through
`params.decide_review_item()`, which appends to `params.review_decisions` and
updates the item in one transaction — a decision the DB refuses fails outright.
`export` is the only file writer: one `<CC>_accepted.json` array per country,
built from accepted/edited queue rows. `run-targets` and `run-country` end with
exactly one `@result {"item_ids": [...]}` line, which the Nomergon worker stores
as the job result. `pipeline.run_parameter(cfg, tracer, record, as_of, force,
parameter_ref, enqueue)` takes a `ParameterRecord`; the evaluation pipeline
calls it with `enqueue=False` and keeps the item itself.

Environment switches the worker relies on: `NOMOS_PYTHON` (every subprocess the
pipeline spawns — scout ingest, scout embeddings build, the query encoder — runs
`[NOMOS_PYTHON, -m, module, …]` in the current directory, no `uv`, no ingest-dir
walk); `WORKFLOW_ENCODER=db` (the query vector comes from an `encode` job in
`ops.jobs` via `encode_client`, instead of a BGE-M3 subprocess — on any failure
the vector leg is disabled for the process and retrieval is FTS-only, with one
console note); `JRC_LLM_BASE_URL` / `JRC_LLM_API_KEY` for the `jrc/<served name>`
model prefix (an OpenAI-compatible gateway).

`ingest-params` accepts both export envelopes (the bare record list and the
0.2.0 `{schema_version, country, parameters, groups}` object) and prefers
received Stage B fields over local derivations. `translate-params` fills
`params.parameter_texts` with law-language renderings of the English
labels/descriptions; `frame` prefers them when building the retrieval query so
the FTS leg of hybrid search is no longer cross-language (see
[Param_Schema/openfisca_france_usage.md](../../Param_Schema/openfisca_france_usage.md) §5).

Two things the EUROMOD export cannot give a parameter store on its own, both
handled through the same ingest path so nothing downstream reads a loose file:
**bracket schedules** exist only as separate scalar constants plus a `groups`
block saying which constant is which band — `paramdb.load_group_record` assembles
one back into a single `bracket_schedule` record (the FR barème:
`FR:tinkt_fr:tin_schedule`); and **parameters defined inside EUROMOD functions**
(the 2025 CDHR rate) are not exported at all, so they live in
`extracted_parameters/curated/<CC>.in_function.json`, ingested exactly like the
delivered export and flagged in `curation/<CC>.curation.yaml` like everything
else. `extracted_parameters/enriched/<CC>.enriched.json` stays read-only.

`ingest-openfisca` **replaces the corpus wholesale**, and `parameter_links`
references `external_parameters` `ON DELETE CASCADE` — so re-ingesting drops
every link, curated and validated alike. Always follow it with
`match-openfisca --seed <exported selection>` (`nomokrisis-eval selection-export FR --kind openfisca`) to rebuild them, and
re-check `validated_by` if anyone had signed links off.

`match-openfisca` suggests `params.parameter_links` rows between EUROMOD
parameters and the ingested OpenFisca corpus, by **value fingerprint**: both
sides hold multi-year numeric histories, so the same value in the same year at
least `--min-years` times is a link candidate (with a ±1-year offset, because
OpenFisca dates income-tax parameters by income year, and a `factor` for
EUROMOD's derived constants). `--seed` loads curated pairs as
`match_method='manual'`. Everything it writes is a **suggestion**: a link counts
as validated only once `validated_by` is set, and a validated row is never
overwritten by a re-run. The first consumer is the evaluation package's
OpenFisca golden-set drafter (`nomokrisis-eval build-openfisca-dataset`), which
re-derives the expected value from each parameter's `temporal_basis` rather than
trusting the link's own year alignment.

Configuration: see [../.env.example](../.env.example). Set `WORKFLOW_MODEL`
(e.g. `anthropic/claude-sonnet-5`) to use a real LLM. Traces land in Phoenix
at http://localhost:6006 (project `nomoscope-agentic-workflow`).

Every run also writes a `params.extraction_runs` row (plus `params.proposals`
and `params.proposal_references`) carrying `phoenix_trace_id`, the OTel trace
id of the run's root span — the link from a stored proposal to the full agent
trace in Phoenix. The same id is on each queue item as `phoenix_trace_id`.
That write is best-effort (a `[paramdb]` warning if it fails); the queue row
itself is not — a run whose item cannot be written fails.
