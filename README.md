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

## Agentic workflow (Activity 3)

Working prototype in [Nomoscope-agentic-workflow/](Nomoscope-agentic-workflow/): PydanticAI-based pipeline
(retrieve → propose → critique → diff → review queue) over the legislation DB,
traced to Arize Phoenix, plus a Tauri (Rust) + Svelte validation UI with review
queue, side-by-side diff, citation viewer, audit log and a database explorer tab.
See [Nomoscope-agentic-workflow/README.md](Nomoscope-agentic-workflow/README.md).

```bash
cd Nomoscope-agentic-workflow/pipeline && uv sync && uv run nomoscope-workflow run-all --as-of 2025-06-01
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

```sh
cd Param_Schema
sed 's/^```mermaid$/```{mermaid}/' parameter_report.md > parameter_report.qmd
quarto render parameter_report.qmd --to typst \
  -M toc:true -M toc-depth:2 -M papersize:a4 \
  -M shift-heading-level-by:-1 -M date:2026-07-21
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
