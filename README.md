# Euromod



## Agentic workflow (Activity 3)

Working prototype in [agentic-workflow/](agentic-workflow/): LangGraph pipeline
(retrieve → propose → critique → diff → review queue) over the legislation DB,
traced to Arize Phoenix, plus a Tauri (Rust) + Svelte validation UI with review
queue, side-by-side diff, citation viewer, audit log and a database explorer tab.
See [agentic-workflow/README.md](agentic-workflow/README.md).

```bash
cd agentic-workflow/pipeline && uv sync && uv run euromod-workflow run-all --as-of 2025-06-01
cd ../ui && npm install && npm run tauri dev
```

Things to install to allow better works for agentic coding.

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
    # For pdfinfo
    poppler-utils \
    socat \
    && sudo apt-get clean && sudo rm -rf /var/lib/apt/lists/*

In PowerShell :

winget install jqlang.jq

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
