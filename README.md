# Nómos

JRC expert-contract prototype that partially automates updating and validating EUROMOD
fiscal parameters from legislation. Project codename: **Nómos**. Package/container names
still use the `euromod-*` prefix; the top-level folders below carry a codename prefix
kept alongside the original descriptive name for readability:

| Codename | Folder | What it is |
|---|---|---|
| Nomotheca (+ Nomosync) | [Nomotheca-RAG/](Nomotheca-RAG/) | Legislation DB (Nomotheca) + its ingestion pipeline (Nomosync); package `nomotheca-ingest` (Activity 2) |
| Nomoscope | [Nomoscope-agentic-workflow/](Nomoscope-agentic-workflow/) | Agentic workflow + validation UI (Activity 3) |
| Nomokrisis | [Nomokrisis-evaluation_pipeline/](Nomokrisis-evaluation_pipeline/) | Evaluation pipeline (Activity 4) |
| Nomergon | [Nomergon-worker/](Nomergon-worker/) | The worker: the one process that runs every job (ingestion, embedding, translation, workflow runs, evaluation) and the only one that holds model credentials or loads a model ([ADR 0004](docs/adr/0004-model-access-lives-only-in-a-worker-fed-by-a-postgres-job-table.md)) |

### Why these names

Every name is built on the Greek root **νόμος (_nómos_)**, "law" — fitting for a system that
reads and reasons over fiscal legislation.

- **Nómos** (νόμος, "law") — the project as a whole.
- **Nomotheca** — _nómos_ + _thēkē_ (θήκη, "repository/case", as in _bibliotheca_): **the law library**, i.e. the legislation database.
- **Nomosync** — _nómos_ + _sync_: **keeping the law in sync**, i.e. the ingestion pipeline that fetches, snapshots and loads legislation into Nomotheca. It is a pipeline within the Nomotheca-RAG subproject, not a separate package — the code ships as `nomotheca-ingest`.
- **Nomoscope** — _nómos_ + _-scope_ (_skopein_, "to examine/observe"): **the law examiner**, i.e. the agentic workflow that inspects legislation and proposes parameter updates.
- **Nomokrisis** — _nómos_ + _krisis_ (κρίσις, "judgment/decision", root of _critic_): **the judgment of the law**, i.e. the evaluation pipeline that scores the proposals.
- **Nomergon** — _nómos_ + _érgon_ (ἔργον, "work"): **the work of the law**, i.e. the worker that executes every job the others submit. The desktop UI never runs anything itself: it inserts a job row into the shared database and the worker picks it up.

## Quick start

The main commands run from the repo root through `make` (`make` alone lists them;
on Windows, run them in WSL). The containers run on **Podman** (`podman` +
`podman-compose`, see [docs/podman.md](docs/podman.md) for the install and the GPU's
CDI setup). API keys come from the repo-root `.env`, read by the worker only:

```sh
git clone XXXX && cd XXXX
cp .env.example .env        # then set the keys the worker needs

make up-gpu                 # Postgres + pgAdmin + Phoenix + the worker on the NVIDIA GPU
make up-cpu                 #   ... or the worker on the CPU (no NVIDIA runtime needed)
make init-db                # once, after the first start: params and eval schemas

make update COUNTRY=FR YEAR=2025        # agentic update of every parameter of a country
make ui                                 # validation UI (review the proposals)
make rag-ui                             # RAG chat over the legislation corpus

make batch                  # nightly batch: translate the corpus to English, then embed
make translate              #   ... or each step alone
make embed
make stop-batch             # stop it (cancel), e.g. from a 07:30 cron entry; nothing done is lost
```

`make update` takes `MODEL=` (one the worker publishes: `make status`), `LIMIT=<n>`
for a smoke run and `FORCE=1` to re-run already-reviewed items; `MODEL=mock/extractor`
needs no key. `make translate` uses `EUROMOD_TRANSLATE_MODEL`, else `WORKFLOW_MODEL`,
from `.env`. Every run is a job the worker executes: `make jobs`, `make logs`, and the
UI's Jobs page show its log. `make down` stops the stack and keeps the data.

- Database interface: pgAdmin: http://localhost:5050 (admin@euromod.eu / admin)
- Phoenix (LLM traces / evals): http://localhost:6006

One-off after the first start with an existing checkout: import the golden set
that used to live in git (`podman exec nomergon-worker-cdi /app/.venv/bin/nomokrisis-eval import-golden`).

The underlying commands, without `make`: `podman-compose --profile gpu-cdi up -d`
(or `--profile cpu`), `podman exec nomergon-worker-cdi /app/.venv/bin/nomergon submit
workflow --wait country=FR year=2025` (`nomergon-worker-cpu` for the CPU worker), `cd Nomoscope-agentic-workflow/ui && npm install && npm run
tauri dev` (WSL: prefix `LIBGL_ALWAYS_SOFTWARE=1`), `nomergon submit translate`,
`nomergon submit embed`.

**Docker** runs the same compose file and `make` targets (picked automatically when
`podman` is absent, or `ENGINE=docker`); the GPU worker is then the service `worker`
(profile `gpu`, container `nomergon-worker`). See [docs/docker.md](docs/docker.md),
which also translates every Podman command below — the likely route for a server
deployment.

## Backup and restore

All persistent state lives in the one Postgres 17 + pgvector container (`nomotheca-legislation-db`, port 5434), which holds two databases:

- `legislation` — the RAG corpus (`public` schema), plus the `params` schema (review queue / decisions, bootstrapped by `nomoscope-workflow`) and the `eval` schema (bootstrapped by `nomokrisis-eval init-db`) — all three live in this one database.
- `phoenix` — Arize Phoenix trace storage.

### Backup

Logical dump (recommended — portable across Postgres versions, works while the stack is running):

```bash
mkdir -p ../backups
podman exec nomotheca-legislation-db pg_dump -U jrc -Fc -d legislation > ../backups/legislation_$(date +%Y%m%d).dump
podman exec nomotheca-legislation-db pg_dump -U jrc -Fc -d phoenix     > ../backups/phoenix_$(date +%Y%m%d).dump
```

`-Fc` (custom format) is compressed and restorable with `pg_restore`, including selective/parallel restore. For a plain-SQL dump instead (diff-friendly, restorable with `psql`):

```bash
podman exec nomotheca-legislation-db pg_dump -U jrc -d legislation > ../backups/legislation_$(date +%Y%m%d).sql
```

Whole-cluster alternative (both databases + roles in one file):

```bash
podman exec nomotheca-legislation-db pg_dumpall -U jrc > ../backups/cluster_$(date +%Y%m%d).sql
```

Volume-level (cold) backup — stop the DB first for a consistent snapshot; faster for full-disaster recovery but not portable across Postgres major versions:

```bash
podman stop nomotheca-legislation-db
podman run --rm -v euromod_pgdata:/data -v "$(pwd)/backups":/backup:z docker.io/library/alpine \
  tar czf /backup/pgdata_$(date +%Y%m%d).tar.gz -C /data .
podman start nomotheca-legislation-db
```

(`euromod_pgdata` is the Compose-generated volume name for this repo directory — check with `podman volume ls | grep pgdata` if you cloned it elsewhere.)

### Restore

Into a running stack, from a custom-format dump (`--clean --if-exists` drops existing objects first, so this also works for overwriting a stack that already has data):

```bash
podman exec -i nomotheca-legislation-db pg_restore -U jrc -d legislation --clean --if-exists < ../backups/legislation_20260901.dump
podman stop nomoscope-phoenix

podman exec -i nomotheca-legislation-db psql -U jrc -d postgres -c "DROP DATABASE IF EXISTS phoenix;"
podman exec -i nomotheca-legislation-db psql -U jrc -d postgres -c "CREATE DATABASE phoenix OWNER jrc;"
podman exec -i nomotheca-legislation-db pg_restore -U jrc -d phoenix < ../backups/phoenix_20260901.dump

podman start nomoscope-phoenix
```

From a plain-SQL dump:

```bash
podman exec -i nomotheca-legislation-db psql -U jrc -d legislation < backups/legislation_20260901.sql
```

From scratch (e.g. after `podman-compose down -v`): bring the stack up first so the init scripts create the base `legislation`/`phoenix` databases, then restore — `pg_restore --clean` (or the dump's own `DROP SCHEMA`/`CREATE SCHEMA` statements) recreates `params`/`eval` along with everything else, so there's no need to run the app-level schema bootstraps separately first.

```bash
podman-compose up -d
podman exec -i nomotheca-legislation-db pg_restore -U jrc -d legislation --clean --if-exists < backups/legislation_20260901.dump
podman exec -i nomotheca-legislation-db pg_restore -U jrc -d phoenix     --clean --if-exists < backups/phoenix_20260901.dump
```

Volume-level restore (full disaster recovery — replaces everything, matching Postgres major version required):

```bash
podman-compose down
podman volume rm euromod_pgdata
podman run --rm -v euromod_pgdata:/data -v "$(pwd)/backups":/backup:z docker.io/library/alpine \
  tar xzf /backup/pgdata_20260901.tar.gz -C /data
podman-compose up -d
```

### Notes

- With Docker, replace `podman` by `docker` and `podman-compose` by `docker compose` (container and volume names are the same; [docs/docker.md](docs/docker.md)). A database lives in one engine's volume: move it between engines with a dump.

- `podman-compose down -v` deletes the `pgdata` volume — never run it without a recent backup once a run holds real (non-seed) data.
- Everything is in the database: the review queue (`params.review_queue`), the decisions (`params.review_decisions`), the golden set (`eval.golden_selections`, `eval.golden_cases`), evaluation runs and the job log (`ops.*`). Nothing runtime lives on a workstation; the only file the UI writes is the EUROMOD export of accepted values, one per country, where the analyst chooses.

## Agentic workflow (Activity 3)

Working prototype in [Nomoscope-agentic-workflow/](Nomoscope-agentic-workflow/): PydanticAI-based pipeline
(retrieve → propose → critique → diff → review queue) over the legislation DB,
traced to Arize Phoenix, plus a Tauri (Rust) + Svelte validation UI with review
queue, side-by-side diff, citation viewer, audit log and a database explorer tab.
See [Nomoscope-agentic-workflow/README.md](Nomoscope-agentic-workflow/README.md).

```bash
# a run is a job the worker executes (mock model, no API key needed):
podman exec nomergon-worker-cdi /app/.venv/bin/nomergon submit workflow --wait \
  --payload '{"targets": ["group:FR:tinkt_fr:tin_schedule"], "year": 2025, "model": "mock/extractor"}'
# or, from a checkout with the stack up, directly:
uv sync --all-packages     # one workspace, one lockfile, one .venv at the repo root
cd Nomoscope-agentic-workflow/pipeline
uv run nomoscope-workflow run-targets group:FR:tinkt_fr:tin_schedule --year 2025 --model mock/extractor
cd ../ui && npm install && npm run tauri dev
```

Things to install to allow better works for agentic coding.

```sh
sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    less \
    procps \
    man-db \
    unzip \
    jq \
    nano \
    vim \
    fzf \
    python3 \
    python3-pip \
    python3-venv \
    python-is-python3 \
    ripgrep \
    make \
    poppler-utils \
    socat \
    && sudo apt-get clean && sudo rm -rf /var/lib/apt/lists/*
```

In PowerShell :
```sh
winget install jqlang.jq
```

## PDF from Markdown

Download Quarto from https://quarto.org/docs/download/

Convert it_needs_for_deployment.md:

```sh
cd docs
sed 's/^```mermaid$/```{mermaid}/' it_needs_for_deployment.md > it_needs_for_deployment.qmd
quarto render it_needs_for_deployment.qmd --to typst \
  -M toc:true -M toc-depth:2 -M papersize:a4 \
  -M shift-heading-level-by:-1 -M date:2026-09-22
rm it_needs_for_deployment.qmd
```

Convert Param_Schema/parameter_report.md:

```sh
cd Param_Schema
sed 's/^```mermaid$/```{mermaid}/' parameter_report.md > parameter_report.qmd
quarto render parameter_report.qmd --to typst \
  -M toc:true -M toc-depth:2 -M papersize:a4 \
  -M shift-heading-level-by:-1 -M date:2026-07-29
rm parameter_report.qmd
```

Convert Param_Schema/parameter_report.md:

```sh
cd Param_Schema
sed 's/^```mermaid$/```{mermaid}/' parameter_report.md > parameter_report.qmd
quarto render parameter_report.qmd --to typst \
  -M toc:true -M toc-depth:2 -M papersize:a4 \
  -M shift-heading-level-by:-1 -M date:2026-07-29
rm parameter_report.qmd
```

Convert Nomotheca-RAG/RAG_architecture_and_implementation.md:
```sh
cd Nomotheca-RAG
quarto render RAG_architecture_and_implementation.md --to typst \
  -M toc:true -M toc-depth:2 -M papersize:a4 \
  -M shift-heading-level-by:-1 -M date:2026-09-29
```

## Improvement Skill

When you want to understand why a pipeline fail, just copy-past the ID and ask the Skill:

`/debug-phoenix-trace <trace-id>`

## Questions

- Form of my reports for each part : Word documents ? PDF.
- Gitlab access ? Right now my code is on a Github private repo with access for Hannes.
- Code licensing ? EUPL v1.2

## Things to do for the Euromod team
- Parameters export to JSON. Already started by Hannes.
- How to deploy the project on Euromod IT infrastructure : Docker or Managed Postgresql at AWS ? Or Kubernetes ?
- How to run an embedding batch at night on the Euromod GPU ?
- How to run a translation batch at night on the Euromod GPU ?

## TODO:
- Support for other sources in the database.
- Bonus : Compare Country Report to legislation ?
- MCP around the RAG database to query it
- ~~Name the project Nómos and the database Nomotheca, ingestion pipeline Nomosync, and agentic-workflow Nomoscope.~~ Done — evaluation pipeline named Nomokrisis; see the naming table above.
- Document time needed for adapters.

Future improvement :
- VIGIL: A Reflective Runtime for Self-Healing LLM Agents : https://openreview.net/pdf?id=bE8nRXcWC1
- GraphRAG
