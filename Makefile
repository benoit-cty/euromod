# Nómos — the everyday commands, from the repo root.  `make` lists them.
#
# Everything that runs a model goes through the worker (ADR 0004): these targets
# submit jobs with `nomergon submit` inside the worker container, so each run is
# an ops.jobs row with its log, visible in the UI's Jobs page.

COUNTRY ?= FR
YEAR    ?= 2025
MODEL   ?=
LIMIT   ?=
FORCE   ?=

# The running worker container: the GPU one, else the CPU one.
WORKER = $(shell docker ps --format '{{.Names}}' | grep -xE 'nomergon-worker(-cpu)?' | head -n1)
# The worker's CLIs (nomergon, nomoscope-workflow, nomokrisis-eval) live in its venv.
BIN = /app/Nomergon-worker/.venv/bin
# Software OpenGL for the Tauri apps under WSL.
TAURI_ENV = $(if $(shell grep -qi microsoft /proc/version 2>/dev/null && echo wsl),LIBGL_ALWAYS_SOFTWARE=1)

.DEFAULT_GOAL := help
.PHONY: help up-gpu up-cpu up down logs status jobs init-db \
        update ui rag-ui embed translate batch stop-batch _worker

help: ## List the targets
	@grep -hE '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-10s %s\n", $$1, $$2}'
	@echo ""
	@echo "  Variables: COUNTRY=$(COUNTRY) YEAR=$(YEAR) MODEL=<from the worker's list> LIMIT=<n> FORCE=1"

# --------------------------------------------------------------------- stack --

up-gpu: ## Start Postgres, pgAdmin, Phoenix and the worker on the NVIDIA GPU
	docker compose --profile gpu up -d --build

up-cpu: ## Same, with the worker on the CPU (no NVIDIA runtime needed)
	docker compose --profile cpu up -d --build

up: ## Start only Postgres, pgAdmin and Phoenix (no worker)
	docker compose up -d

down: ## Stop the stack (keeps the data; never use `down -v` without a backup)
	docker compose --profile gpu --profile cpu down

logs: _worker ## Follow the worker's log
	docker logs -f $(WORKER)

status: _worker ## Workers and the models they publish
	docker exec $(WORKER) $(BIN)/nomergon status

jobs: _worker ## The latest jobs
	docker exec $(WORKER) $(BIN)/nomergon jobs

init-db: _worker ## Create the params and eval schemas (idempotent; once after the first start)
	docker exec $(WORKER) $(BIN)/nomoscope-workflow init-param-db
	docker exec $(WORKER) $(BIN)/nomokrisis-eval init-db

# ------------------------------------------------------------------ workflow --

update: _worker ## Agentic update of every parameter of COUNTRY for system year YEAR
	docker exec $(WORKER) $(BIN)/nomergon submit workflow --wait \
	  country=$(COUNTRY) year=$(YEAR) \
	  $(if $(MODEL),model=$(MODEL)) $(if $(LIMIT),limit=$(LIMIT)) $(if $(FORCE),force=true)

# ----------------------------------------------------------------------- UIs --

ui: ## Run the validation UI (desktop app)
	cd Nomoscope-agentic-workflow/ui && { [ -d node_modules ] || npm install; } && $(TAURI_ENV) npm run tauri dev

rag-ui: ## Run the RAG chat (desktop app)
	cd Nomoscope-agentic-workflow/rag-ui && { [ -d node_modules ] || npm install; } && $(TAURI_ENV) npm run tauri dev

# ------------------------------------------------------------------- batches --

embed: _worker ## Embed every chunk that has no vector yet
	docker exec $(WORKER) $(BIN)/nomergon submit embed --wait

# The model defaults to EUROMOD_TRANSLATE_MODEL, else WORKFLOW_MODEL, from .env.
translate: _worker ## Translate non-English texts to English (MODEL= to override)
	docker exec -e MODEL_ARG=$(MODEL) $(WORKER) sh -c '$(BIN)/nomergon submit translate --wait \
	  model="$${MODEL_ARG:-$${EUROMOD_TRANSLATE_MODEL:-$$WORKFLOW_MODEL}}" target_lang=en'

batch: translate embed ## The nightly batch: translate, then embed (originals and translations)

# Safe in a cron entry: committed translations and vectors are kept, the next
# batch resumes where this one stopped, and no batch running is not an error.
stop-batch: _worker ## Stop the nightly batch: cancel queued/running translate and embed jobs
	docker exec $(WORKER) $(BIN)/nomergon cancel --type translate --type translate-params --type embed

_worker:
	@if [ -z "$(WORKER)" ]; then \
	  echo "No worker running: start it with 'make up-gpu' or 'make up-cpu'." >&2; exit 1; fi
