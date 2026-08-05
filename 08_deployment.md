# Deployment Guide — what the IT team needs to provide

**Audience:** the JRC / EUROMOD IT team.
**Purpose:** describe what has to be hosted for the Nómos prototype to run, what is
*mandatory* versus *nice to have*, and which decisions we need from IT (Docker or not,
managed PostgreSQL or not, self-hosted GPU or not).

> **Short version.** The only thing that *must* be hosted centrally is **one PostgreSQL 17
> database with the pgvector extension**. Everything else can run on developer /
> analyst machines. If in addition you can give us **a self-hosted embeddings endpoint on a
> GPU** and **a self-hosted LLM endpoint**, the whole system runs inside the JRC network
> with no external API calls at all — that is the target architecture.

---

## 1. Components at a glance

| # | Component | What it is | Where it can run | Needed for a minimal deployment? |
|---|---|---|---|---|
| 1 | **Legislation database** (`Nomotheca`) | PostgreSQL 17 + pgvector. Holds legal texts, chunks, embeddings, the parameter store and the evaluation results | Central server / managed service | **YES — mandatory, shared** |
| 2 | **Ingestion pipeline** (`nomotheca-ingest`) | Python CLI. Fetches legislation from official national sources, snapshots, parses, chunks, loads, embeds, translates | Batch machine (a VM, or a dev workstation) | Yes, but runs anywhere with DB + internet access |
| 3 | **Agentic workflow** (`nomoscope-workflow`) | Python CLI. Proposes parameter updates with an LLM | Analyst workstation (launched by the UI) or a batch VM | Yes, runs anywhere with DB + LLM access |
| 4 | **Validation UI** (`Nomoscope`) | **Tauri 2 desktop application** (Rust + Svelte) — an `.exe` / AppImage, *not* a web app | Analyst workstation | Yes — it is the human-in-the-loop step |
| 5 | **Evaluation pipeline** (`nomokrisis-eval`) | Python CLI, scores the workflow against a golden set | Dev workstation or batch VM | Optional (project internal) |
| 6 | **Arize Phoenix** | LLM observability (traces, token counts, cost, energy) | One small container — **better centrally hosted**, dev machine as fallback | Not for the system to *run*, but see §8 |
| 7 | **pgAdmin** | Database web console | Dev machine, or replaced by IT's own console | **No — droppable** |
| 8 | **Embeddings service** | BGE-M3, 1024-dim vectors | GPU server (**strongly preferred**) or CPU fallback on each workstation | Not strictly — but see §6 |
| 9 | **LLM endpoint** | Open-weight model behind an OpenAI-compatible API | GPU server (**preferred**) or external API | Yes, in one form or another |

### The ask, in three tiers

* **Must have — component 1.** Without the database there is no system. If IT can provide
  exactly one thing, this is it.
* **Should have — components 8, 9 and 6.** The GPU endpoints (§6, §7) are what make the
  system fast and keep all data inside the JRC perimeter. **Phoenix (§8) is the one piece
  of "tooling" we would argue for hosting centrally**, because it holds the project's
  evidence base, not just developer convenience — reasons in §8.
* **Nice to have — components 2, 5 and 7, plus a small batch VM.** These can live on
  development machines for the whole pilot without anyone noticing.

---

## 2. Deployment options — pick one

### Option A — Docker Compose on one VM (simplest, what we use today)

A single [`docker-compose.yml`](docker-compose.yml) at the repo root starts PostgreSQL +
pgvector, pgAdmin and Phoenix, and auto-applies the schema. One `docker compose up -d`
and the server side is running.

* Requires: one Linux VM, Docker + Docker Compose, ~4 vCPU / 8 GB RAM / 100 GB disk.
* Pros: fastest, reproducible, exactly what has been tested; schema and extensions come
  pre-provisioned in the `pgvector/pgvector:pg17` image.
* Cons: you own the backups and the patching of a self-hosted database.

### Option B — Managed PostgreSQL + no Docker (if Docker is not allowed)

The database is a managed service (Azure Database for PostgreSQL Flexible Server,
AWS RDS/Aurora, or an internal DBaaS); we apply the schema over the network with `psql`.
The Python components are installed with `uv` (a single static binary, no Docker), the UI
is a signed desktop installer.

* This works, **provided the required extensions are available** — see §3.2. This is the
  one blocking question for Option B.
* pgAdmin can simply be dropped. Phoenix still needs somewhere to run — a small container
  host, or a dev machine as fallback (§8.1).

### Option C — Hybrid (our recommendation)

Managed PostgreSQL (backed up, monitored, patched by IT) **+** a small Linux VM for batch
jobs (ingestion, scheduled workflow runs) and the Phoenix container **+** desktop UI on the
analysts' machines **+** pgAdmin dropped in favour of IT's own database console.

---

## 3. The database (mandatory)

### 3.1 Version and layout

* **PostgreSQL 16 or later** (tested on **17**).
* Two logical databases on the same instance:

| Database | Contents | Who writes |
|---|---|---|
| `legislation` | `public` schema — legal instruments, texts, chunks, embeddings, fetch snapshots. `params` schema — the EUROMOD parameter store, proposals and extraction runs. `eval` schema — evaluation results | ingestion, workflow, evaluation |
| `phoenix` | LLM trace storage for Arize Phoenix | Phoenix only |

If Phoenix is not deployed, the `phoenix` database is not needed.

### 3.2 Required extensions — **please confirm these are available**

| Extension | Why |
|---|---|
| **`vector` (pgvector ≥ 0.7)** | Vector search. **Version 0.7+ is required** — we store `halfvec(1024)` (fp16) with an HNSW index; earlier versions do not have `halfvec` |
| `pg_trgm` | Fuzzy matching of legal citations / identifiers |
| `btree_gist` | UUID equality inside GiST exclusion constraints (temporal validity) |
| `unaccent` | Diacritics-insensitive full-text search |
| `ltree` | Legal hierarchy paths (book → title → chapter → article) |

`CREATE EXTENSION` normally requires a superuser or a specially privileged role. On managed
services the extensions must usually be **allow-listed** first (e.g. the `azure.extensions`
server parameter on Azure, the `shared_preload_libraries` / parameter group on RDS). We
need either that allow-listing plus a role that can create them, or a DBA to run
[`Nomotheca-RAG/db/schema.sql`](Nomotheca-RAG/db/schema.sql) once for us.

The schema also creates **per-language full-text search configurations** (French, Dutch,
German, Spanish, English, Lithuanian, Irish …) built on the standard PostgreSQL stemmers —
no third-party dictionary is needed.

### 3.3 Sizing

Today's pilot corpus (partial, 5 countries, ~70 instruments) is **228 MB**:

| Table | Size | Note |
|---|---|---|
| `chunks` | 64 MB | retrieval units + FTS index |
| `unit_texts` | 57 MB | original + machine-translated text |
| `embeddings` | 48 MB | 8 845 vectors, halfvec(1024) + HNSW |
| `fetch_snapshots` | 17 MB | raw archived payloads (provenance) |

Extrapolating to the five pilot countries fully ingested, with English translations and
embeddings, we expect **10–30 GB**. **Provision 100 GB with room to grow**, and expect the
vector index to want to sit in RAM: **8–16 GB RAM** on the instance is comfortable,
4 vCPU is plenty. There is no high write throughput — ingestion is batch, the workflow is
mostly reads.

### 3.4 Backup

Standard nightly backup + PITR is more than enough. Nothing here is unrecoverable in
principle (the corpus can be re-ingested from official sources), but re-ingestion is slow
and re-embedding costs GPU hours, so a normal backup policy saves real time.
The one genuinely irreplaceable artefact is **`data/decisions.jsonl`**, the append-only
human-decision audit log, which lives on the analyst workstation / a shared folder — see §5.

---

## 4. Database accounts (security)

We currently use one all-powerful `jrc` user because it is a local prototype. **For a real
deployment we recommend separate least-privilege roles**, one per component. This also
makes the audit trail meaningful — you can tell from `pg_stat_activity` which component
did what.

| Role | Rights | Used by |
|---|---|---|
| `nomos_admin` | Owner of the schemas, runs migrations | DBA / dev team, manual |
| `nomos_ingest` | **read/write** on `public` (legislation, chunks, embeddings, snapshots) | ingestion pipeline (component 2) |
| `nomos_workflow` | **read-only** on `public`, **read/write** on `params` | agentic workflow (component 3) |
| `nomos_ui` | **read-only** on `public` and `params`; read-only on `phoenix` | validation UI Database tab (component 4) |
| `nomos_eval` | read-only on `public`/`params`, read/write on `eval` | evaluation pipeline (component 5) |
| `phoenix` | owner of the `phoenix` database only | Phoenix container (component 6) |

Sketch of the grants (to be run by a DBA after the schema is applied):

```sql
CREATE ROLE nomos_workflow LOGIN PASSWORD '…';
GRANT CONNECT ON DATABASE legislation TO nomos_workflow;
GRANT USAGE ON SCHEMA public TO nomos_workflow;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO nomos_workflow;
GRANT USAGE, CREATE ON SCHEMA params TO nomos_workflow;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA params TO nomos_workflow;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO nomos_workflow;
```

**Caveat — the gap-fill "scout".** If the optional scout feature is enabled
(`WORKFLOW_SCOUT=llm|tavily`), the workflow ingests a missing legal act on the fly and
therefore needs `nomos_ingest`-level write rights on `public`. With the scout off (the
default) `nomos_workflow` can stay read-only there. Tell us which you prefer; the pipeline
works either way.

**Connection security:** all components accept a standard PostgreSQL URL and support TLS
(`?sslmode=require`). Please issue **TLS-only** accounts. Credentials are read from
environment variables (`WORKFLOW_DATABASE_URL`, `EUROMOD_DATABASE_URL`) — they can come
from a vault, a systemd unit, or a `.env` file, whatever fits JRC practice. Nothing is
hard-coded.

---

## 5. Who connects to the database, from where

This is the part most likely to need a firewall rule, because **the validation UI is a
desktop application, not a web app**. It talks to PostgreSQL directly.

| Client | Host | Connection | Notes |
|---|---|---|---|
| Validation UI (Tauri desktop app) | Analyst laptop/workstation | PostgreSQL TCP 5432 (TLS) | Read-only Database tab + the review queue; also **spawns the workflow CLI as a child process**, so the workstation needs the Python pipeline installed and access to the LLM endpoint |
| Agentic workflow CLI | Same workstation, or a batch VM | PostgreSQL TCP 5432 | |
| Ingestion CLI | Batch VM or dev workstation | PostgreSQL TCP 5432 **+ outbound HTTPS to official national legislation portals** (Légifrance/DILA, eISB, e-tar.lt, BOE, …) | Outbound internet access is required for ingestion, and only for ingestion |
| Evaluation CLI | Dev workstation / VM | PostgreSQL TCP 5432 | |
| Phoenix | Small VM / container host (preferred), or a dev machine | PostgreSQL TCP 5432 to the `phoenix` DB; receives OTLP traces on 6006/4317 **from every machine that runs the workflow** | See §8.1 |
| pgAdmin | Dev machine | PostgreSQL TCP 5432 | Optional |

If direct database access from user workstations is not acceptable, the alternatives are a
VPN (simplest), a bastion/SSH tunnel, or restricting the desktop UI to a small group of
analyst machines on a dedicated subnet. **Please tell us which model applies** — it does
not change the code, only the connection string.

**Review queue and decision log.** The UI writes `ReviewItem` JSON files and appends to
`data/decisions.jsonl`. Today these are local files. If several analysts must share one
queue, point `WORKFLOW_DATA_DIR` at a shared network drive, or ask us to move the queue
into the `params` schema (moderate change, already half done — proposals are persisted in
the database).

---

## 6. Embeddings service (GPU) — **strongly recommended**

**Model: `BAAI/bge-m3`**, 1024-dimensional, multilingual (covers all the pilot languages —
this is why it was chosen over English-centric encoders).

Embeddings are needed in two places:

1. **Batch** — every ingested chunk is embedded once. This is the heavy job: hundreds of
   thousands of chunks for a full 5-country corpus.
2. **Query time** — *every workflow run* encodes its query. This happens on whichever
   machine runs the workflow, i.e. today on the analyst's laptop.

Currently we run BGE-M3 locally on CPU (OpenVINO on Intel Core Ultra, or PyTorch). It
works, but it is slow for batch and it forces a ~2.5 GB model download plus a heavy Python
extra onto every machine that runs the workflow.

**A shared self-hosted embeddings endpoint on a GPU would be clearly better:**

* Batch embedding of a national corpus drops from days to hours.
* Workstations no longer need the model or the ML dependencies — just an HTTP call.
* One model version for everybody → embeddings stay comparable (mixing encoder versions
  silently degrades retrieval).

| Requirement | Value |
|---|---|
| Model | `BAAI/bge-m3` (Apache-like MIT licence, freely redistributable) |
| VRAM | ~4 GB fp16 (~2.3 GB weights + activations at 8 k context). **Any 8–16 GB GPU is ample** |
| Serving stack | Hugging Face **TEI** (Text Embeddings Inference), **Infinity**, or vLLM — all expose an OpenAI-compatible `/v1/embeddings` endpoint |
| Interface | HTTP, internal network only |

> **Small development note:** the ingestion package currently talks to a *local* encoder
> (`torch` / `openvino` backends behind an `EmbeddingBackend` protocol). Pointing it at an
> HTTP endpoint is a new backend implementing one method (`encode(list[str]) -> list[list[float]]`)
> — a small, well-isolated change on our side, not a redesign. If IT provides the endpoint,
> we add the backend.

Note that embedding dimensions are baked into the schema (`halfvec(1024)`), so a different
embedding model would require a schema change and a full re-embed. Sticking to BGE-M3 is
the low-friction path.

---

## 7. LLM endpoint — self-hosted preferred

### 7.1 How the software talks to an LLM

Models are configured everywhere as **provider-prefixed strings** (`anthropic/…`,
`openai/…`, `azure_openai/…`, `openrouter/…`, `together/…`, plus `mock/…` for key-less
offline demos). Nothing in the pipeline knows the provider — endpoint flexibility is a hard
contractual requirement, because Activity 5 has to compare several models.

**A self-hosted model served behind an OpenAI-compatible API** (vLLM, SGLang, TGI, Ollama,
LM Studio, or any internal gateway) is consumed through the `openai/` prefix with the base
URL pointed at the internal server — an environment-variable change:

```bash
WORKFLOW_MODEL=openai/mistral-small-3.2
OPENAI_BASE_URL=https://llm.internal.jrc/v1
OPENAI_API_KEY=<token issued by the gateway>
```

If the internal gateway is not OpenAI-compatible, adding a provider prefix is ~10 lines in
[`llm.py`](Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/llm.py).

### 7.2 What the LLM is used for

| Use | Volume | Notes |
|---|---|---|
| `propose` step | 1 call per parameter per run | Structured output (JSON schema), long RAG context |
| `critique` step | 1 call per parameter per run, can use a different/cheaper model | |
| **Bulk translation** of non-English legal text to English | **This is the volume driver** — every ingested legal unit | Segmented ~6 k characters per call; a self-hosted model makes this essentially free |
| Optional "scout" gap-fill | rare | |

Requirements: **structured / JSON output support**, a **long context window** (32 k+, RAG
prompts carry many legal chunks), and solid **multilingual** ability for the pilot
languages (FR, NL, LT, GA, ES …).

### 7.3 Models

The models EUROMOD already runs are all suitable, and are what we would target first:

| Model | Total / active params | VRAM (Q4/FP8) | Comment |
|---|---|---|---|
| **Mistral Small 3.2** (24B) | 24B | ~15 GB | Apache 2.0, strong EU-language coverage. **Best fit for a single 24 GB GPU** |
| **gpt-oss** (20b / 120b) | 21B/3.6B · 117B/5.1B | ~16 GB (native MXFP4) / ~80 GB | Apache 2.0, MoE → fast. English-centric: check quality on FR/LT/GA legal text before relying on it |
| **MiniMax 2.7** | large MoE | multi-GPU | Very long context — useful for the RAG prompts |
| **Llama 3.3 70B** | 70B | ~40–48 GB | ⚠️ Llama Community Licence (700 M-MAU cap, branding obligations). Covers 8 languages — Lithuanian and Irish are *not* among them |

Alternatives worth knowing about, if EU-language parity turns out to be the binding
constraint: **EuroLLM-9B** and **Teuken-7B** are the only open models trained from scratch
on all 24 EU official languages, and both run in ~6 GB. See
[`Nomoscope-agentic-workflow/models_choice.md`](Nomoscope-agentic-workflow/models_choice.md)
for the full comparison.

Suggested hardware: **one 24 GB GPU** (RTX 4090 / L4 / A5000) serves Mistral Small 3.2 for
a small analyst team. **One 80 GB GPU** (A100/H100) covers gpt-oss-120b or Llama 3.3 70B
and comfortable throughput for bulk translation. The same GPU can host the embeddings model
alongside — BGE-M3 needs only ~4 GB.

### 7.4 If self-hosting is not possible

The system also works against external APIs (Anthropic, OpenAI, Azure OpenAI, OpenRouter,
Together). This is a **data-governance decision, not a technical one**: the content sent to
the model is published national legislation plus EUROMOD parameter metadata — public data,
no personal data — but it does leave the JRC perimeter. **Azure OpenAI in an EU region** is
the usual middle ground. We need a written answer on this (it is question Q13 / assumption
A4 of [`07_risks-and-decisions.md`](07_risks-and-decisions.md)).

---

## 8. Observability (Phoenix) and the database console (pgAdmin)

Neither is required for the system to *run*. They are not, however, in the same category,
and we would ask IT to treat them differently.

### 8.1 Arize Phoenix — we recommend hosting it centrally

Phoenix (http://localhost:6006 in the dev stack) collects an OpenTelemetry trace of every
LLM call: the prompt, the retrieved chunks, token counts, latency, cost, and the
energy/CO₂ estimate. Three reasons it belongs on IT infrastructure rather than a
developer's laptop:

1. **It holds a project deliverable, not just debug output.** Activity 5's multi-model
   comparison and the environmental-impact KPIs are computed *from these traces*. If the
   trace history lives on a contractor machine, the evidence base for the final technical
   report disappears at the end of the contract.
2. **The data is already central anyway.** Phoenix stores everything in the `phoenix`
   database inside the same PostgreSQL instance (`PHOENIX_SQL_DATABASE_URL`). Only the web
   container is local today. So hosting it properly is a small increment — the state that
   needs backing up is already in the database IT is backing up.
3. **Debugging is a shared activity.** When an analyst reports a wrong or missing
   proposal, diagnosing it means opening that run's trace. With Phoenix on one developer's
   machine, only that developer can answer the question.

What it costs IT: **one container** (`arizephoenix/phoenix:latest`), ~1 GB RAM, its own
database user on the `phoenix` DB, and two ports — 6006 (web UI + OTLP/HTTP) and 4317
(OTLP/gRPC) — reachable from wherever the workflow runs.

Two caveats to plan for:

* **The open-source image has no authentication by default.** Behind a reverse proxy with
  JRC SSO, or restricted to an internal subnet. The content is prompts over public legal
  text, so the confidentiality risk is low, but it should not be an open web app.
* It is a fast-moving project — **pin a version tag** rather than tracking `:latest` as our
  dev compose file does.

**Fallback:** if this is a step too far, we run it in Docker on a development machine and
accept that the trace history is not preserved past the contract. Tracing can also be
disabled entirely (`WORKFLOW_TRACING=false`); the pipeline then has no dependency on
Phoenix at all, and we lose the model-comparison and energy KPIs.

### 8.2 pgAdmin — genuinely optional, and the first thing to drop

pgAdmin (http://localhost:5050 in the dev stack) is a convenience console with no data of
its own. Any PostgreSQL client replaces it — DBeaver, `psql`, or the validation UI's own
read-only Database tab. It is also a web console holding cached database credentials,
i.e. an attack surface that buys nothing unique.

**If IT already provides a database console or a standard client, we use that and drop
pgAdmin.** We only kept it in the development stack because it ships in the same
`docker compose up`.

### 8.3 Credentials

Both currently run with demo credentials (`admin@euromod.eu` / `admin`, `jrc` / `jrc`).
These are development defaults and must be replaced before either is exposed beyond a
developer machine.

---

## 9. Workstation requirements (analysts)

| Item | Requirement |
|---|---|
| OS | Windows 10/11, macOS, or Linux (Tauri 2 builds for all three; developed on WSL2/Linux) |
| Validation UI | Installer (~15 MB). On Windows it uses the system WebView2 runtime |
| Python pipeline | Installed via `uv` (single binary, no admin rights needed); Python 3.11+ |
| Network | PostgreSQL TCP to the database; HTTPS to the LLM endpoint |
| Local disk | ~1 GB, plus ~2.5 GB if BGE-M3 runs locally instead of on a shared GPU |
| GPU | Not needed on the workstation if §6 is provided |

Build-side only (dev team): Rust toolchain + Node.js for compiling the UI, and the usual
Linux WebKitGTK dev packages.

---

## 10. Security and data protection summary

* **Data classification: public.** The corpus is published national legislation, plus
  EUROMOD parameter values and Country Reports. **No personal data, no microdata, no
  EU-SILC data** ever enters this system.
* **Outbound traffic:** ingestion fetches from official national legislation portals; the
  workflow calls the LLM endpoint. With a self-hosted LLM and a pre-ingested corpus, the
  system needs **no internet access at all** at run time.
* **The system never writes into EUROMOD.** It is export-first and human-gated: proposals
  go into a review queue, a human accepts or rejects in the UI, and only accepted values
  are exported. There is no write path into EUROMOD parameter files.
* **Audit trail:** every proposal carries its citations (chunk id + character offsets into
  the source text), and every human decision is appended to an immutable
  `decisions.jsonl`. This is a contractual property, worth protecting with the same care
  as the database.
* **Secrets:** database URLs and API keys come from environment variables / `.env` files.
  They can be sourced from a vault or a systemd `EnvironmentFile` — nothing needs a
  credential file on disk if JRC practice forbids it.

---

## 11. What we need from IT — decision checklist

| # | Question | Our preference |
|---|---|---|
| 1 | **Is Docker allowed** on a server VM? | Yes → Option A, running today, zero setup work |
| 2 | If not: **managed PostgreSQL 16+** available? | Fine — see §3 |
| 3 | Can **pgvector ≥ 0.7, pg_trgm, btree_gist, unaccent, ltree** be enabled? | **Blocking for Option B.** Needs allow-listing on most managed services |
| 4 | Who runs `schema.sql` — us with a privileged role, or a DBA? | Either |
| 5 | **Dedicated DB accounts** per component, TLS-only? | Yes, per §4 |
| 6 | Can analyst workstations reach the DB on 5432 (directly / VPN / bastion)? | VPN is fine; we need to know which |
| 7 | Is a **GPU embeddings endpoint** (BGE-M3, ~4 GB VRAM) possible? | **Strongly wanted** |
| 8 | Is a **self-hosted LLM endpoint** possible, OpenAI-compatible? Which of Mistral Small 3.2 / gpt-oss / MiniMax 2.7 / Llama 3.3 70B are already served? | **Strongly wanted**; Mistral Small 3.2 first |
| 9 | If not: is an **external LLM API** (Azure OpenAI EU, Anthropic, …) authorised for public legal text? | Needed for Activity 5's multi-model comparison either way |
| 10 | Can **Phoenix** be hosted centrally (one container, ~1 GB RAM, behind SSO)? | **Yes, please** — it holds the Activity 5 evidence base, §8.1. Fallback: dev machine |
| 11 | Do you already provide a **database console**? Then we drop pgAdmin | Your tooling wins |
| 12 | Shared network folder for the review queue and `decisions.jsonl`, or move the queue into PostgreSQL? | Either; database is cleaner long-term |
| 13 | A small **batch VM** for scheduled ingestion (outbound HTTPS to national portals)? | Nice to have; a dev workstation can do it during the pilot |
| 14 | Backup policy on the `legislation` database? | Standard nightly + PITR |

---

## 12. Minimal viable deployment (if the answer to most of the above is "no")

1. One PostgreSQL 17 instance with pgvector, one database, one account. *(IT)*
2. Everything else on the dev/analyst machines: ingestion, workflow, UI, Phoenix in local
   Docker, embeddings on CPU. *(us)*
3. LLM: whatever endpoint is authorised — external API, or `mock/…` for offline demos.

That is enough to run the full pilot end-to-end. Every other item in this document is an
improvement in speed, security or operability, not a precondition — **with one thing worth
knowing before you choose it**: in this configuration the LLM traces live on a development
machine, so the raw evidence behind the Activity 5 model comparison and the
environmental-impact figures is not preserved beyond the project. If only one item above
the minimum can be granted, §8.1 (Phoenix, one small container against a database you are
already backing up) is the cheapest one to grant.
