# Nomergon: the worker that owns every model call

Status: implemented 2026-09-22 (issues/ 01–06 done; container image build and JRC roles.sql run are deployment steps)

Decision record: [docs/adr/0004](../../docs/adr/0004-model-access-lives-only-in-a-worker-fed-by-a-postgres-job-table.md).
Glossary terms: Job, Job type, Worker, Workstation, Golden source, Golden case, Golden set
hash in [CONTEXT.md](../../CONTEXT.md). Deployment view: [it_needs_for_deployment.md](../../it_needs_for_deployment.md) §6.

## Goal

Move every LLM call, every embedding computation and every internet fetch off the analyst's
workstation into one server-side process, so that (1) API keys exist on one machine,
(2) embedding and translation batches can run overnight on a server, and (3) JRC can put
its own GPUs and its own OpenAI-compatible gateway behind the system.

## Starting point (facts, verified 2026-09-22)

- The Tauri UI holds no key and no model. It spawns `uv run` children (`ingest.rs`,
  `workflow.rs`, `encoder.rs`) that inherit its env and call `load_dotenv()`. That is where
  the keys and BGE-M3 live today.
- No HTTP service, job table, queue or scheduler exists anywhere in the repo. Run state is an
  in-memory `HashMap<run_id, oneshot::Sender>` in the UI.
- The UI reads from the workstation's disk: `data/queue/*.json` (review items),
  `decisions.jsonl`, `export/`, and the golden dataset directory (`golden.rs`).
- Two LLM code paths: `nomoscope_workflow.llm` (PydanticAI, provider-prefixed) used by
  propose, critique, scout, both translators; and `nomokrisis_eval.build_dataset`, which
  calls the raw Anthropic SDK with a server-side fallback beta.
- Two module-global latches never reset in a long-lived process: `scout._web_search_unavailable`
  (Tavily HTTP 432) and `query_encoder._disabled`.
- `eval.runs` / `eval.results` already duplicate the on-disk `manifest.json`.
- `.env` is gitignored.

## Decisions (the design tree)

### Topology
1. **Execution moves to a server** (option B). Model endpoints are not built now; they
   remain possible as backends of the worker (`EmbeddingBackend` HTTP impl; `jrc/` prefix).
2. **Full remote.** The UI never spawns a process. Local dev runs the worker as a Docker
   container with NVIDIA GPU access (`gpus: all`); automatic CPU/OpenVINO fallback when no
   CUDA is visible. No `/dev/dri`. Chromium is in the image (Légifrance tier-3 fallback,
   ADR 0002; other countries will need it).
3. **The workstation holds one credential: its per-analyst Postgres login.** The UI's
   query vector for semantic search comes from the worker (an `encode` job). When no worker
   is alive the search degrades to full-text and says so.
4. **Transport is a Postgres job table, no HTTP API.** Schema `ops`: `ops.jobs`
   (`id, job_type, payload jsonb, priority, status, submitted_by default current_user,
   submitted_at, started_at, finished_at, cancel_requested, result jsonb, error`),
   `ops.job_events` (`job_id, seq, at, level, line`), `ops.workers` (heartbeat),
   `ops.worker_models` (the list the UI offers). Worker claims with `FOR UPDATE SKIP LOCKED`.
5. **The UI polls**, by last-seen event id for logs and for `encode` results. No NOTIFY.

### Jobs
6. **Job types**: `workflow`, `ingest`, `embed`, `translate`, `translate-params`, `encode`,
   `eval`, `draft-golden`, `impact`. Rule: everything the UI triggers is a job; a developer
   command that needs a model runs from the worker's checkout; one that needs only the DB
   runs anywhere.
7. **Structured JSON payload per job type**, validated by a Pydantic model on the worker;
   the worker composes the CLI argv. Rust stays loosely typed.
8. **Worker runs each job as a subprocess of the existing CLIs** (isolation, latch reset,
   `@progress` lines → `job_events`). `encode` is in-process with the model warm, a priority
   lane that never waits behind a GPU job.
9. **One job at a time**, one worker, plus the encode lane.
10. **Lifecycle** `queued → running → succeeded | failed | cancelled`. Cancel =
    `cancel_requested` set by the submitter (row-level security), worker kills the child.
    Heartbeat; a job whose worker died is marked `failed` at next start. **No automatic
    requeue.** `job_events` pruned after 30 days.
11. **Nightly batches are submitted by hand** for now (UI or CLI); document how. No scheduler.

### Models and credentials
12. **`jrc/<served name>`** is a new provider prefix in `llm.py`, OpenAI-compatible, reading
    `JRC_LLM_BASE_URL` / `JRC_LLM_API_KEY` on the worker only.
13. **Embeddings stay in-process on the worker's GPU** (today's torch/CUDA path). HTTP
    backend not built now.
14. **The worker publishes its model list** from `WORKER_MODELS` at startup into
    `ops.worker_models`; the UI's model picker reads it; no free-text model strings. Critique
    model stays the worker's default.
15. **The golden-set drafter is rewritten on `llm.run_agent`** (PydanticAI structured
    output), dropping the raw Anthropic SDK call and its fallback beta.
16. **Everything migrates**: eval runs (`eval` job), the drafter (`draft-golden`), the MCP
    server's query encoding (`encode` job → it needs a login role, loses
    `default_transaction_read_only`).

### Data: nothing runtime on disk
17. Files that stay in git as inputs: EUROMOD enriched exports, curation YAML overlays,
    Country Report markdown. Everything else runtime becomes rows:
    - review queue → `params.review_queue` (item id, jsonb, status); the decide path becomes
      one transaction (prepare → insert decision → update item).
    - `decisions.jsonl` dropped (`params.review_decisions` is the record).
    - `data/parameters/db|eval/` dropped; runs read `params.*` directly (as `run-targets`
      already does for groups).
    - eval `manifest.json` dropped (`eval.runs` has it).
    - golden **sources** and built golden **cases** → `eval.golden_sources`,
      `eval.golden_cases` (`verified, verified_by, verified_at` from `current_user`); each
      eval run records the **golden set hash** of the cases it scored. No git dump.
18. **The EUROMOD export is the only workstation file**: built UI-side in Rust from DB rows,
    **one file per country**, saved through a file picker. The Python `export` command reads
    the DB too; both file-walking twins are deleted.
19. **Migration of existing dev state**: import the golden cases once; reset decisions and
    the queue (test data); drop run manifests.

### Roles
20. `nomos_admin` (DDL), `nomos_worker` (all DML on public/params/eval/ops),
    `nomos_reviewer` (group, NOLOGIN: SELECT everywhere; INSERT `params.review_decisions`,
    `ops.jobs`; UPDATE `ops.jobs.cancel_requested` on own rows via RLS; UPDATE verification
    columns of `eval.golden_cases`), one LOGIN role per analyst `IN ROLE nomos_reviewer`.
    Shipped as `db/roles.sql`. Reviewer identity and `submitted_by` come from `current_user`;
    the `REVIEWER`/`USER` env guess goes.

### Naming
21. Subproject dir `Nomergon-worker/`, package `nomergon-worker` (module `nomergon`), CLI
    `nomergon` (`nomergon serve`, `nomergon submit <job-type> …`). Same image for JRC's
    compose deployment and the dev box. CLAUDE.md's naming section gains the fourth codename.

## Out of scope (explicitly)
- A scheduler for nightly jobs.
- HTTP embedding backend, HTTP job API.
- Multi-worker / parallel GPU jobs.
- Automatic requeue.

## Consequences to keep in view during implementation
- CLAUDE.md rule "a decision the DB refuses fails outright" is preserved and simplified
  by the queue-as-rows transaction; never let the UI write the item before the decision.
- The verbatim-extract rule, the source-trust filtering and jurisdiction scoping are
  untouched: the pipeline code runs unchanged inside the worker's subprocesses.
- `resolved_model` in eval manifests must keep working with `jrc/` (Phoenix
  `llm.model_name` agreement check in CLAUDE.md).
- Memory note: two concurrent eval runs OOM the 1080 Ti — the serial worker is the fix.
