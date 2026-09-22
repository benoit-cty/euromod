# Nomergon — the worker

Nomergon is the fourth Nómos subproject: **the one process that holds model
credentials, loads models and talks to the internet** ([ADR 0004](../docs/adr/0004-model-access-lives-only-in-a-worker-fed-by-a-postgres-job-table.md)).
The validation UI, the MCP server and developer tooling never execute anything:
they insert a row into `ops.jobs` and poll `ops.jobs` / `ops.job_events`. The
worker claims rows (`FOR UPDATE SKIP LOCKED`), runs each job as a subprocess of
the existing CLIs (`nomotheca_ingest.cli`, `nomoscope_workflow.cli`,
`nomokrisis_eval.cli`, from its own interpreter, never `uv run`), streams their
stdout/stderr into `ops.job_events`, and answers `encode` jobs in-process with
BGE-M3 kept warm. There is no HTTP API: the job table is the bus.

One worker, one job at a time, plus the encode lane. No automatic requeue: a
job whose worker died is marked `failed` at the next start and a human
resubmits (embedding and translation resume by construction).

## Job types

| job_type | payload | runs |
|---|---|---|
| `workflow` | `{"targets": [...], "year": 2025, "model": null, "force": false}` | `nomoscope_workflow.cli run-targets …` |
| `ingest` | `{"command": "instrument"\|"citation"\|"document"\|"route", "args": [...]}` | `nomotheca_ingest.cli <command> <args…> --database-url …` |
| `embed` | `{"model_id": 1, "batch_size": 16, "limit": null, "dry_run": false}` | `nomotheca_ingest.cli embeddings build --backend torch …` |
| `translate` | `{"model": "…", "target_lang": "en", "limit": null, "request_timeout": 120, "dry_run": false}` | `nomotheca_ingest.cli translate run …` |
| `translate-params` | `{"country": "FR", "lang": "fr", "model": "…", "batch_size": 20, "limit": null, "force": false}` | `nomoscope_workflow.cli translate-params …` |
| `encode` | `{"query": "…"}` or `{"query": "…", "sentences": [...]}` | in-process (priority 100) |
| `eval` | `{"as_of": "…", "model": "…", "countries": [], "languages": [], "include_drafts": false, "notes": null}` or `{"resume": "<run_id>"}` | `nomokrisis_eval.cli run` / `resume` |
| `draft-golden` | `{"source": "openfisca"\|"curated"\|"document", "country": "FR", …}` | `nomokrisis_eval.cli build-*-dataset` |
| `impact` | `{"project": "", "since": null, "until": null, "zone": ""}` | `nomoscope_workflow.cli impact --json` |

The binding table, with results per type, is
[`.scratch/nomergon-worker/contracts.md`](../.scratch/nomergon-worker/contracts.md);
the Pydantic models and the argv are in [`src/nomergon/jobs.py`](src/nomergon/jobs.py).
A job with no `model` runs on the worker's default (the first of
`WORKER_MODELS`, exported as `WORKFLOW_MODEL` to the child), which is also the
critique model of every workflow run.

Lifecycle: `queued → running → succeeded | failed | cancelled`. Lines the child
prints become `ops.job_events` rows (`stream` stdout|stderr|system|progress);
`@progress {json}` is also copied into `ops.jobs.progress`, `@result {json}`
into `ops.jobs.result`. Exit 0 → `succeeded`, otherwise `failed` with the last
20 stderr lines as `error`. A cancel is SIGTERM, 10 s, SIGKILL → `cancelled`.

## Running the worker

### In Docker (the same image JRC deploys)

From the repo root, with the [NVIDIA container toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) installed:

```bash
docker compose --profile gpu up -d --build      # stack + worker on the GPU
docker compose --profile cpu up -d --build      # stack + worker on the CPU (no NVIDIA runtime)
docker compose logs -f worker
```

Put `COMPOSE_PROFILES=gpu` (or `cpu`) in the repo-root `.env` and a plain
`docker compose up -d` includes the worker. The profiles exist because a GPU
reservation fails on a box without the NVIDIA runtime before the container
starts, and the stack must still come up there.

The container reads the repo-root `.env` (`env_file`) for provider keys and
`WORKER_MODELS`; `WORKER_DATABASE_URL`, `PHOENIX_COLLECTOR_ENDPOINT` and
`PHOENIX_DATABASE_URL` are set in the compose file to the in-network names.
BGE-M3 is downloaded from the Hugging Face hub on first run into the
`hf-cache` volume (`HF_HOME=/models`). The image is built from the repo root
(`build.context: .`) and installs the four packages into one environment; it
needs outbound internet at run time (legislation sources, LLM APIs, the hub).

### On the host (development)

```bash
cd Nomergon-worker
uv sync                    # torch cu126 wheels: ~2.5 GB, run on CPU too
uv run nomergon init-db    # ops schema (idempotent; the worker does it at start too)
WORKER_MODELS=mock/extractor uv run nomergon serve
```

Same `.env` files as the pipeline (repo root, then `Nomoscope-agentic-workflow/.env`).
The local `Nomotheca-RAG/ingest/models/bge-m3` checkout is used when present,
else `BAAI/bge-m3` from the hub. CUDA when torch sees a usable GPU (a wheel
with no kernels for the card falls back to the CPU with a warning), else CPU.

## Submitting and following jobs

```bash
nomergon submit encode query="barème de l'impôt sur le revenu" --wait
nomergon submit workflow targets=euromod://FR/tin_fr/def_const/\$tinrt_cdhr year=2025 model=mock/extractor --wait
nomergon submit ingest command=instrument args='["fr","JORFTEXT000051168007","--max-items","500"]'
nomergon submit impact --wait
nomergon submit eval --payload '{"as_of":"2025-06-01","model":"mock/extractor","countries":["FR"]}'

nomergon jobs --limit 20        # id, type, status, submitted_by, submitted_at, progress
nomergon events 42 --follow     # stream the log until the job is final
nomergon cancel 42
nomergon status                 # workers (heartbeat age) + published models
nomergon prune-events           # events older than WORKER_EVENT_RETENTION_DAYS
```

`key=value` pairs are JSON where they parse (`year=2025`, `force=true`,
`args='["fr", …]'`), plain strings otherwise, and a comma list for list
fields (`targets=a,b`); `--payload '<json>'` gives the whole payload at once.
`--wait` prints the events as they land and exits 0 on `succeeded`.

From Python (worker side; the pipeline has its own copy in
`nomoscope_workflow/encode_client.py` because the dependency direction is
worker → packages):

```python
from nomergon import client, db
with db.connect(url) as conn:
    job_id = client.submit(conn, "encode", {"query": "…"}, priority=100)
    row = client.wait(conn, job_id, timeout=60, poll=0.1)   # row["result"]["halfvec"]
```

## Nightly batches (by hand, for now)

There is no scheduler (ADR 0004). Submit in the evening; the worker runs them
one after the other and the log is in `ops.job_events`:

```bash
nomergon submit embed                                    # every chunk missing a fresh bge-m3 vector
nomergon submit translate model=openrouter/google/gemma-4-31b-it:free target_lang=en
nomergon submit translate-params country=FR lang=fr model=azure_openai/gpt-5.6-luna
nomergon jobs                                            # next morning
```

Both `embed` and `translate` select what is still missing at start, so a
failed or cancelled batch is simply resubmitted.

## Environment

| variable | default | meaning |
|---|---|---|
| `WORKER_DATABASE_URL` | `WORKFLOW_DATABASE_URL`, else `postgresql://jrc:jrc@localhost:5434/legislation` | the one database (also exported to every child as `WORKFLOW_DATABASE_URL`, `EUROMOD_DATABASE_URL`, `EVAL_DATABASE_URL`) |
| `WORKER_MODELS` | empty | comma-separated provider-prefixed LLMs to publish in `ops.worker_models`; the first is the default |
| `WORKER_EMBEDDING_MODEL_PATH` | local `Nomotheca-RAG/ingest/models/bge-m3` if present, else `BAAI/bge-m3` | BGE-M3 for the encode lane and `embed` jobs |
| `WORKER_POLL_SECONDS` | `1.0` | job-claim poll interval |
| `WORKER_ENCODE_POLL_SECONDS` | `0.05` | encode-lane poll interval |
| `WORKER_HEARTBEAT_SECONDS` | `10` | `ops.workers.heartbeat_at` refresh |
| `WORKER_STALE_SECONDS` | `60` | a running job whose worker's heartbeat is older is `failed` at the next start |
| `WORKER_EVENT_RETENTION_DAYS` | `30` | `ops.job_events` pruning window (daily, and `nomergon prune-events`) |
| `WORKER_ID` | `<hostname>-<pid>` | the worker's identity in `ops.workers` / `ops.jobs.worker_id` |
| `NOMOS_REPO_ROOT` | walk up from the package | where the four subprojects live (the container sets `/app`) |
| provider keys | — | `ANTHROPIC_API_KEY`, `AZURE_OPENAI_*`, `OPENROUTER_API_KEY`, `JRC_LLM_BASE_URL`/`JRC_LLM_API_KEY`, `TAVILY_API_KEY`, … as documented in `Nomoscope-agentic-workflow/.env.example`; the worker is the only process that holds them |

Every child also gets `PYTHONUNBUFFERED=1`, `NOMOS_PYTHON=<the worker's
interpreter>`, `WORKFLOW_ENCODER=db` and `WORKER_JOB_ID`, and runs from its
package directory (`Nomotheca-RAG/ingest`, `Nomoscope-agentic-workflow/pipeline`
or `Nomokrisis-evaluation_pipeline`) so relative paths resolve.

## Database roles

[`db/ops_schema.sql`](db/ops_schema.sql) is applied by `nomergon init-db`, by
the worker at start, and by the dev db container on a fresh volume.
[`db/roles.sql`](db/roles.sql) is for a shared deployment, run once by a DBA
after every schema (legislation, params, eval, ops) is in place:

```bash
psql "$ADMIN_URL" -f Nomergon-worker/db/roles.sql
psql "$ADMIN_URL" -c "ALTER ROLE nomos_worker PASSWORD '…'"
psql "$ADMIN_URL" -c "CREATE ROLE alice LOGIN PASSWORD '…' IN ROLE nomos_reviewer"
```

The worker then connects as `nomos_worker` (`WORKER_DATABASE_URL=postgresql://nomos_worker:…@host/legislation`);
each analyst's UI connects with their own login, which may read everything,
append decisions, submit jobs and cancel its own (row-level security on
`ops.jobs`; `submitted_by` is `current_user`). The dev stack's `jrc` superuser
needs none of this.

## Tests

```bash
cd Nomergon-worker && uv run pytest
```

`tests/test_jobs.py` and `tests/test_runner.py` need nothing; `tests/test_db_smoke.py`
runs against the Postgres at `WORKER_DATABASE_URL` (default: the dev stack)
and is skipped when none answers. Nothing in the tests calls a billed model.
