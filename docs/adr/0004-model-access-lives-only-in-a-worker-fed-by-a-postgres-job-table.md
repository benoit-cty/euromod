---
status: accepted
date: 2026-09-22
---

# Model access lives only in a worker fed by a Postgres job table

Until now every model call happened on the analyst's workstation. The Tauri UI holds no key
and loads no model, but it spawns `uv run` children (workflow runs, ingestion, embedding
builds, translation, a long-lived BGE-M3 query encoder) that inherit its environment, load
`.env`, and therefore need every provider key and a 2.5 GB model on each machine. Nightly
batches had no machine to run on, and JRC's internal GPUs were unreachable from a laptop.

We decided that **a fourth subproject, Nomergon (the worker), is the only process that holds
model credentials or loads a model**. It runs on a server (a Docker container with NVIDIA GPU
access, the same image for JRC and for local dev). **The UI never executes anything**: it
inserts a row into `ops.jobs` and polls `ops.jobs` / `ops.job_events`; the worker claims rows
with `FOR UPDATE SKIP LOCKED`, runs each job as a subprocess of the existing CLIs, and streams
their progress into `ops.job_events`. **The workstation holds exactly one credential, its
per-analyst Postgres login**, and the roles are least-privilege: `nomos_reviewer` may read,
append decisions, submit jobs and cancel its own; only `nomos_worker` writes the corpus, the
parameter store and the queue. **There is no HTTP API.** All runtime state that used to be a
file on the machine that ran the job (review queue items, decisions log, eval run manifests,
materialized parameter files, built golden cases and their sources) becomes rows; the only
file the workstation ever writes is the EUROMOD export, one file per country.

## Considered options

- **Model endpoints only** (TEI for BGE-M3, vLLM behind an OpenAI-compatible API), the
  pipeline still running on the workstation. Rejected as the first step: the workstation
  still needs a token per endpoint, nightly batches still need a host, and every analyst
  machine still needs the Python pipeline. Endpoints remain a later backend *of the worker*:
  the `EmbeddingBackend` protocol already admits an HTTP implementation, and an
  OpenAI-compatible LLM is the `jrc/` prefix.
- **An HTTP job API** (FastAPI or axum) in front of the worker. Rejected: it is a second
  network surface for JRC IT to approve when direct Postgres access from workstations is
  already the one thing they must allow; a job row is the API. The trade-off is that a reader
  looking for "the API" finds a table. Think of it as an asynchronous bus, as one would use
  Redis, except the bus is the database that already holds everything else and survives
  restarts (today's run state is an in-memory map that dies with the app).
- **A shared filesystem** between worker and workstations so the file-based review queue
  survives unchanged. Rejected: a network share is a second thing to approve and a locking
  hazard, and the queue as rows makes "a decision the DB refuses fails outright" one
  transaction instead of a three-step protocol.
- **`LISTEN/NOTIFY` for live progress.** Deferred: the UI's Postgres crate is synchronous, and
  polling by last-seen event id is one mechanism that survives a dropped connection. The
  `encode` job (a query vector for the UI's search) runs in a priority lane with the model
  kept warm, and a 100 ms poll is within budget.

## Consequences

- One worker, one job at a time (plus the in-process `encode` lane): embedding, translation
  and scouted workflow runs share one GPU, and two at once already OOM an 11 GB card.
  Analysts sometimes wait behind a translation batch; the job list says why.
- No automatic requeue. A job whose worker died is marked failed at the next start; a human
  resubmits. Embedding and translation are resumable by construction (they select what is
  missing at startup), so nothing is lost.
- Nightly batches are jobs like any other, submitted by hand for now; scheduling is a later,
  separate decision.
- Subprocess per job resets the module-level latches (Tavily quota, "vector leg disabled")
  that would otherwise stick for the life of a long-lived process.
- The model list an analyst can pick from is published by the worker, not typed: free-text
  model strings are how the Azure deployment mix-up went unnoticed for a month (see
  `llm.py`). `jrc/<served name>` is its own prefix for the same reason, even though the
  endpoint is OpenAI-compatible.
- The golden-set drafter is rewritten on `llm.run_agent`, losing the Anthropic-only
  server-side fallback, so that "all LLM calls in one place" means one code path, not one
  machine. The MCP server submits `encode` jobs and so needs a login, not a read-only one.
- Per-analyst logins make `submitted_by` and each decision's reviewer come from
  `current_user`, replacing the `REVIEWER`/`USER` env-var guess.
