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

### Why these names

Every name is built on the Greek root **νόμος (_nómos_)**, "law" — fitting for a system that
reads and reasons over fiscal legislation.

- **Nómos** (νόμος, "law") — the project as a whole.
- **Nomotheca** — _nómos_ + _thēkē_ (θήκη, "repository/case", as in _bibliotheca_): **the law library**, i.e. the legislation database.
- **Nomosync** — _nómos_ + _sync_: **keeping the law in sync**, i.e. the ingestion pipeline that fetches, snapshots and loads legislation into Nomotheca. It is a pipeline within the Nomotheca-RAG subproject, not a separate package — the code ships as `nomotheca-ingest`.
- **Nomoscope** — _nómos_ + _-scope_ (_skopein_, "to examine/observe"): **the law examiner**, i.e. the agentic workflow that inspects legislation and proposes parameter updates.
- **Nomokrisis** — _nómos_ + _krisis_ (κρίσις, "judgment/decision", root of _critic_): **the judgment of the law**, i.e. the evaluation pipeline that scores the proposals.

## Quick start

Launch the server side:
```sh
git clone XXXX
cd XXXX
docker compose up
```

- Database interface: pgAdmin: http://localhost:5050
- Phoenix (LLM traces / evals): http://localhost:6006

Launch the UI in another terminal:
```sh
cd Nomoscope-agentic-workflow/ui
npm install
npm run tauri dev
LIBGL_ALWAYS_SOFTWARE=1 npm run tauri dev
```

## Backup and restore

All persistent state lives in the one Postgres 17 + pgvector container (`nomotheca-legislation-db`, port 5434), which holds two databases:

- `legislation` — the RAG corpus (`public` schema), plus the `params` schema (review queue / decisions, bootstrapped by `nomoscope-workflow`) and the `eval` schema (bootstrapped by `nomokrisis-eval init-db`) — all three live in this one database.
- `phoenix` — Arize Phoenix trace storage.

### Backup

Logical dump (recommended — portable across Postgres versions, works while the stack is running):

```bash
mkdir -p backups
docker exec nomotheca-legislation-db pg_dump -U jrc -Fc -d legislation > backups/legislation_$(date +%Y%m%d).dump
docker exec nomotheca-legislation-db pg_dump -U jrc -Fc -d phoenix     > backups/phoenix_$(date +%Y%m%d).dump
```

`-Fc` (custom format) is compressed and restorable with `pg_restore`, including selective/parallel restore. For a plain-SQL dump instead (diff-friendly, restorable with `psql`):

```bash
docker exec nomotheca-legislation-db pg_dump -U jrc -d legislation > backups/legislation_$(date +%Y%m%d).sql
```

Whole-cluster alternative (both databases + roles in one file):

```bash
docker exec nomotheca-legislation-db pg_dumpall -U jrc > backups/cluster_$(date +%Y%m%d).sql
```

Volume-level (cold) backup — stop the DB first for a consistent snapshot; faster for full-disaster recovery but not portable across Postgres major versions:

```bash
docker compose stop db
docker run --rm -v euromod_pgdata:/data -v "$(pwd)/backups":/backup alpine \
  tar czf /backup/pgdata_$(date +%Y%m%d).tar.gz -C /data .
docker compose start db
```

(`euromod_pgdata` is the Compose-generated volume name for this repo directory — check with `docker volume ls | grep pgdata` if you cloned it elsewhere.)

### Restore

Into a running stack, from a custom-format dump (`--clean --if-exists` drops existing objects first, so this also works for overwriting a stack that already has data):

```bash
docker exec -i nomotheca-legislation-db pg_restore -U jrc -d legislation --clean --if-exists < backups/legislation_20260901.dump
docker compose stop phoenix

docker exec -i nomotheca-legislation-db psql -U jrc -d postgres -c "DROP DATABASE IF EXISTS phoenix;"
docker exec -i nomotheca-legislation-db psql -U jrc -d postgres -c "CREATE DATABASE phoenix OWNER jrc;"
docker exec -i nomotheca-legislation-db pg_restore -U jrc -d phoenix < backups/phoenix_20260901.dump

docker compose start phoenix
```

From a plain-SQL dump:

```bash
docker exec -i nomotheca-legislation-db psql -U jrc -d legislation < backups/legislation_20260901.sql
```

From scratch (e.g. after `docker compose down -v`): bring the stack up first so the init scripts create the base `legislation`/`phoenix` databases, then restore — `pg_restore --clean` (or the dump's own `DROP SCHEMA`/`CREATE SCHEMA` statements) recreates `params`/`eval` along with everything else, so there's no need to run the app-level schema bootstraps separately first.

```bash
docker compose up -d
docker exec -i nomotheca-legislation-db pg_restore -U jrc -d legislation --clean --if-exists < backups/legislation_20260901.dump
docker exec -i nomotheca-legislation-db pg_restore -U jrc -d phoenix     --clean --if-exists < backups/phoenix_20260901.dump
```

Volume-level restore (full disaster recovery — replaces everything, matching Postgres major version required):

```bash
docker compose down
docker volume rm euromod_pgdata
docker run --rm -v euromod_pgdata:/data -v "$(pwd)/backups":/backup alpine \
  tar xzf /backup/pgdata_20260901.tar.gz -C /data
docker compose up -d
```

### Notes

- `docker compose down -v` deletes the `pgdata` volume — never run it without a recent backup once a run holds real (non-seed) data.
- Human review decisions are the one piece of state with a redundant copy outside Postgres: `Nomoscope-agentic-workflow/pipeline/data/decisions.jsonl` mirrors `params.review_decisions`. If a restore loses recent decisions, replay them with `uv run nomoscope-workflow sync-decisions` (from `Nomoscope-agentic-workflow/pipeline`) instead of re-deciding in the UI.
- The review queue itself (`Nomoscope-agentic-workflow/pipeline/data/queue/`) and materialized parameter files under `data/parameters/db|eval/` are files, not database state — back them up separately (or regenerate the parameter files from the DB) if you need them.

## Agentic workflow (Activity 3)

Working prototype in [Nomoscope-agentic-workflow/](Nomoscope-agentic-workflow/): PydanticAI-based pipeline
(retrieve → propose → critique → diff → review queue) over the legislation DB,
traced to Arize Phoenix, plus a Tauri (Rust) + Svelte validation UI with review
queue, side-by-side diff, citation viewer, audit log and a database explorer tab.
See [Nomoscope-agentic-workflow/README.md](Nomoscope-agentic-workflow/README.md).

```bash
cd Nomoscope-agentic-workflow/pipeline && uv sync
uv run nomoscope-workflow run-targets group:FR:tinkt_fr:tin_schedule 'euromod://FR/tin_fr/def_const/$tinrt_cdhr' --year 2025   # mock model, no API key needed
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
sed 's/^```mermaid$/```{mermaid}/' it_needs_for_deployment.md > it_needs_for_deployment.qmd
quarto render it_needs_for_deployment.qmd --to typst \
  -M toc:true -M toc-depth:2 -M papersize:a4 \
  -M shift-heading-level-by:-1 -M date:2026-08-11
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
