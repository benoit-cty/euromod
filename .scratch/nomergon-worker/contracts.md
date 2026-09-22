# Nomergon contracts (shared by every work package)

Read this before touching anything. The schemas it names are already written:
- `Nomergon-worker/db/ops_schema.sql` — `ops.jobs`, `ops.job_events`, `ops.workers`, `ops.worker_models`
- `Nomergon-worker/db/roles.sql` — roles, grants, RLS
- `Nomoscope-agentic-workflow/pipeline/db/params_schema.sql` — `params.review_queue`, `params.decide_review_item()`
- `Nomokrisis-evaluation_pipeline/db/eval_schema.sql` — `eval.golden_selections`, `eval.golden_cases`, `eval.embedding_cases`, `eval.run_cases`, `eval.embedding_runs`, new columns on `eval.runs` / `eval.results`

## Job types, payloads, what the worker runs, result

The worker validates `payload` with a Pydantic model per type (`nomergon/jobs.py`)
and composes the argv. Every subprocess runs from the worker's own Python
(`sys.executable -m …`, never `uv run`), with `--database-url` / env pointing at
the worker's database URL, and `PYTHONUNBUFFERED=1`. Lines on stdout/stderr
become `ops.job_events` rows (`stream` stdout|stderr); a line starting with
`@progress ` is parsed, stored as a `progress` event with `data`, and copied
into `ops.jobs.progress`. Exit 0 → `succeeded`, otherwise `failed` with `error`
= last stderr lines. `cancel_requested` → SIGTERM, 10 s, SIGKILL → `cancelled`.

| job_type | payload (JSON) | command | result |
|---|---|---|---|
| `workflow` | `{"targets": ["euromod://FR/…", "group:FR:tinkt_fr:tin_schedule"], "year": 2025, "model": "azure_openai/gpt-5.6-luna" \| null, "force": false}` | `nomoscope_workflow.cli run-targets <targets…> --year Y [--model M] [--force]` | `{"item_ids": [...]}` parsed from the CLI's final `@result {json}` line |
| `ingest` | `{"command": "instrument"\|"citation"\|"document"\|"route", "args": ["fr", "JORFTEXT…", "--max-items", "500"]}` — `args` exactly what the UI built today (`IngestTab.buildRequest`), minus `--database-url` | `nomotheca_ingest.cli <command> <args…> --database-url <url>` | `route`: the JSON the command prints; others: null |
| `embed` | `{"model_id": 1, "batch_size": 16, "limit": null, "dry_run": false}` | `nomotheca_ingest.cli embeddings build --backend torch --model-path <WORKER_EMBEDDING_MODEL_PATH or BAAI/bge-m3> --model-id … --batch-size … [--limit n] [--dry-run] --progress-json --database-url …` | last progress |
| `translate` | `{"model": "…", "target_lang": "en", "limit": null, "request_timeout": 120, "dry_run": false}` | `nomotheca_ingest.cli translate run --model … --target-lang … --progress-json [--request-timeout n] [--limit n] [--dry-run] --database-url …` | last progress |
| `translate-params` | `{"country": "FR", "lang": "fr", "model": "…", "batch_size": 20, "limit": null, "force": false}` | `nomoscope_workflow.cli translate-params --country … --lang … --model … [--batch-size n] [--limit n] [--force]` | null |
| `encode` | `{"query": "…"}` or `{"query": "…", "sentences": ["…", …]}` | in-process, warm BGE-M3 (priority 100, its own lane) | `{"halfvec": "[…1024 floats…]"}` or `{"similarities": [...]}` |
| `eval` | `{"as_of": "2025-06-01", "model": "…", "countries": [] , "languages": [], "include_drafts": false, "notes": null}` or `{"resume": "<run_id>"}` | `nomokrisis_eval.cli run --as-of … --model … [--country c]* [--language l]* [--include-drafts] [--notes …]` / `nomokrisis_eval.cli resume <run_id>` | `{"run_id": "…"}` from `@result` |
| `draft-golden` | `{"source": "openfisca"\|"curated", "country": "FR", "year": 2025, "as_of": null, "limit": 50, "fill": true}` or `{"source": "document", "country": "FR", "as_of": "2025-06-01", "language": "fr", "targets": ["euromod://…"], "text": "<the trusted document text>", "model": null}` | `nomokrisis_eval.cli build-openfisca-dataset …` / `build-curated-dataset …` / `build-dataset <tmpfile written from text> --country … --as-of … [--language …] [--target t]* [--model M]` | `{"written": n}` from `@result` |
| `impact` | `{"project": "" , "since": null, "until": null, "zone": ""}` | `nomoscope_workflow.cli impact --json [--project p] [--since d] [--until d] [--zone z]` | the report JSON (the command's single stdout line) |

**`@result {json}`**: a CLI that has a result prints exactly one line
`@result <json>` on stdout at the end; the worker stores it in `ops.jobs.result`.
`run-targets` prints `@result {"item_ids": [...]}`; `nomokrisis-eval run/resume`
prints `@result {"run_id": "..."}`; the golden builders print `@result {"written": n}`.

**Submitting from Python** (worker package provides it, others may import):
`nomergon.client.submit(conn, job_type, payload, priority=0) -> int`,
`nomergon.client.wait(conn, job_id, timeout, poll=0.1) -> row`. The pipeline
must not import nomergon (dependency direction is worker → packages); it gets
its own tiny copy in `nomoscope_workflow/encode_client.py` (below).

## Environment switches the packages must honour

- `NOMOS_PYTHON` — when set, every subprocess the pipeline spawns (scout ingest,
  scout embeddings build, the query encoder) runs `[NOMOS_PYTHON, "-m", module, …]`
  in the current working directory, no `uv`, no ingest-dir walk. The worker sets
  it to `sys.executable`.
- `WORKFLOW_ENCODER` — `subprocess` (today's behaviour, default) or `db`: the
  query vector is obtained by submitting an `encode` job and polling
  (`nomoscope_workflow/encode_client.py: encode_via_jobs(database_url, query,
  timeout=60.0) -> str halfvec`, and `score_via_jobs(database_url, query,
  sentences)`). The worker runs workflow jobs with `WORKFLOW_ENCODER=db`, so the
  subprocess never loads the model itself. Any failure keeps today's semantics:
  vector leg disabled for the process, FTS-only, one console note.
- `WORKER_MODELS` — comma-separated provider-prefixed LLM names the worker
  publishes (first is default). `WORKER_EMBEDDING_MODEL_PATH` — local BGE-M3
  path or the HF id. `WORKER_DATABASE_URL` (falls back to `WORKFLOW_DATABASE_URL`).
- `JRC_LLM_BASE_URL`, `JRC_LLM_API_KEY` — the `jrc/` prefix in `llm.py`.

## Data that moves from disk to rows (what each package must do)

- Review queue: `params.review_queue`. Pipeline `queue_store` becomes DB-backed
  (`write_item(conn, item, force)`, `load_items(conn)`, `export_accepted(conn) ->
  dict[country, list[record]]`); no `queue/`, `decisions.jsonl`, `export/`,
  `parameters/` directories; `WorkflowConfig.data_dir` goes away (eval's scratch
  dir went with it — eval passes `queue_sink=None`-style: see below).
- `run_parameter(cfg, tracer, record: ParameterRecord, as_of, force=False,
  parameter_ref: str | None = None, enqueue: bool = True) -> ReviewItem`: takes
  a record, not a path. `run-targets` loads from the params DB and runs; no
  materialization. `run-all` becomes `run-country <CC> --year Y` (every
  parameter of a country in the params DB) — or is dropped if that is simpler;
  `run` (files) is dropped. Eval calls `run_parameter(..., enqueue=False)` and
  keeps the item itself.
- Golden set: `eval.golden_selections` (one row per (country, kind), verbatim
  header + entries of the old JSON), `eval.golden_cases`, `eval.embedding_cases`.
  `GoldenCase.parameter_file` → `parameter_target: str` (a `euromod://…` id or
  `group:<group_id>`), loaded via `paramdb.load_record` / `load_group_record`.
  Scoring constants come from `openfisca_golden.db_constants(conn, country, as_of)`.
  `nomokrisis-eval import-golden` imports the on-disk dataset/, dataset_embedding/
  and golden_sources/ once (mapping parameter_file → target by reading the
  materialized file's `information.model_target`; a group record's id is
  `euromod://<cc>/<policy>/group/<name>` — map it back through
  `params.parameter_groups`).
- Eval runs: `eval.runs` row at start (`status='running'`, `submitted_by`),
  `eval.run_cases` frozen list, `eval.results` upserted per case as scored
  (with `review_item`), `status='complete'` at the end. `resume <run_id>` reads
  all of that back; `rescore` reads `review_item`. `list-runs` reads the table.
  No `.eval_runs/`.
- `golden_set_hash` = sha256 over the sorted `(id, case JSON with review fields
  stripped)` of the cases in the run, first 12 hex chars, stored in
  `eval.runs.dataset_version`.

## Roles and identity

- Reviewer identity is `current_user` on the server: `decide_review_item`
  ignores the entry's `reviewer`; `ops.jobs.submitted_by` defaults to it;
  golden verdicts set `reviewed_by = current_user`.
- The UI connects with the analyst's own login (still from `WORKFLOW_DATABASE_URL`
  for now). It reads `SELECT current_user` once and shows it where the Reviewer
  input used to be.

## UI ↔ worker (Rust)

`jobs.rs` (replaces ingest.rs, workflow.rs, encoder.rs):
- `submit_job {db_url, job_type, payload, priority?} -> {id}`
- `job_status {db_url, id} -> {id, job_type, status, progress, result, error, submitted_by, submitted_at, started_at, finished_at}`
- `job_events {db_url, id, after} -> {events: [{id, at, stream, line, data}]}`
- `cancel_job {db_url, id}`
- `list_jobs {db_url, limit} -> {jobs: [...]}` (newest first, for a Jobs panel)
- `worker_status {db_url} -> {workers: [...], models: [{model, kind, is_default}]}`
- `encode_query {db_url, query, sentences?}` submits an `encode` job with
  priority 100 and polls every 100 ms up to 60 s; error text when no worker is
  alive (`ops.workers.heartbeat_at` older than 60 s).
Svelte `lib/jobs.js`: `followJob(dbUrl, id, {onLine, onProgress}, pollMs=1000)`
resolves with the final status row; the Ingest/Params tabs use it exactly where
they used `runIngest`/`runWorkflow` + the log events.
