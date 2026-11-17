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

# The container engine: Docker when it is installed, else Podman (docs/podman.md).
# Force one with ENGINE=podman / ENGINE=docker.
ENGINE  ?= $(if $(shell command -v docker 2>/dev/null),docker,podman)
# Podman goes through podman-compose (it maps `devices: nvidia.com/gpu=all` to CDI)
# and starts the GPU worker as the CDI service; Docker uses its device reservation.
ifeq ($(ENGINE),podman)
COMPOSE     ?= podman-compose
GPU_PROFILE ?= gpu-cdi
else
COMPOSE     ?= docker compose
GPU_PROFILE ?= gpu
endif

# The running worker container: the GPU one, else the CPU one.
WORKER = $(shell $(ENGINE) ps --format '{{.Names}}' | grep -xE 'nomergon-worker(-cpu|-cdi)?' | head -n1)
# The worker's CLIs (nomergon, nomoscope-workflow, nomokrisis-eval) live in its venv.
BIN = /app/.venv/bin
# Software OpenGL for the Tauri apps under WSL.
TAURI_ENV = $(if $(shell grep -qi microsoft /proc/version 2>/dev/null && echo wsl),LIBGL_ALWAYS_SOFTWARE=1)

.DEFAULT_GOAL := help
.PHONY: help up-gpu up-cpu up down logs status jobs init-db \
        update ui rag-ui embed translate batch stop-batch _worker \
        sync test test-python test-apps migrate lint

help: ## List the targets
	@grep -hE '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-10s %s\n", $$1, $$2}'
	@echo ""
	@echo "  Engine: $(ENGINE) ($(COMPOSE))"
	@echo "  Variables: COUNTRY=$(COUNTRY) YEAR=$(YEAR) MODEL=<from the worker's list> LIMIT=<n> FORCE=1"

# --------------------------------------------------------------------- stack --

up-gpu: ## Start Postgres, pgAdmin, Phoenix and the worker on the NVIDIA GPU
	$(COMPOSE) --profile $(GPU_PROFILE) up -d --build

up-cpu: ## Same, with the worker on the CPU (no NVIDIA runtime needed)
	$(COMPOSE) --profile cpu up -d --build

up: ## Start only Postgres, pgAdmin and Phoenix (no worker)
	$(COMPOSE) up -d

down: ## Stop the stack (keeps the data; never use `down -v` without a backup)
	$(COMPOSE) --profile gpu --profile gpu-cdi --profile cpu down

logs: _worker ## Follow the worker's log
	$(ENGINE) logs -f $(WORKER)

status: _worker ## Workers and the models they publish
	$(ENGINE) exec $(WORKER) $(BIN)/nomergon status

jobs: _worker ## The latest jobs
	$(ENGINE) exec $(WORKER) $(BIN)/nomergon jobs

init-db: _worker ## Create the params and eval schemas (idempotent; once after the first start)
	$(ENGINE) exec $(WORKER) $(BIN)/nomoscope-workflow init-param-db
	$(ENGINE) exec $(WORKER) $(BIN)/nomokrisis-eval init-db

# ------------------------------------------------------------------ workflow --

update: _worker ## Agentic update of every parameter of COUNTRY for system year YEAR
	$(ENGINE) exec $(WORKER) $(BIN)/nomergon submit workflow --wait \
	  country=$(COUNTRY) year=$(YEAR) \
	  $(if $(MODEL),model=$(MODEL)) $(if $(LIMIT),limit=$(LIMIT)) $(if $(FORCE),force=true)

# ----------------------------------------------------------------------- UIs --

ui: ## Run the validation UI (desktop app)
	cd Nomoscope-agentic-workflow/ui && { [ -d node_modules ] || npm install; } && $(TAURI_ENV) npm run tauri dev

rag-ui: ## Run the RAG chat (desktop app)
	cd Nomoscope-agentic-workflow/rag-ui && { [ -d node_modules ] || npm install; } && $(TAURI_ENV) npm run tauri dev

# ------------------------------------------------------------------- batches --

embed: _worker ## Embed every chunk that has no vector yet
	$(ENGINE) exec $(WORKER) $(BIN)/nomergon submit embed --wait

# The model defaults to EUROMOD_TRANSLATE_MODEL, else WORKFLOW_MODEL, from .env.
translate: _worker ## Translate non-English texts to English (MODEL= to override)
	$(ENGINE) exec -e MODEL_ARG=$(MODEL) $(WORKER) sh -c '$(BIN)/nomergon submit translate --wait \
	  model="$${MODEL_ARG:-$${EUROMOD_TRANSLATE_MODEL:-$$WORKFLOW_MODEL}}" target_lang=en'

batch: translate embed ## The nightly batch: translate, then embed (originals and translations)

# Safe in a cron entry: committed translations and vectors are kept, the next
# batch resumes where this one stopped, and no batch running is not an error.
stop-batch: _worker ## Stop the nightly batch: cancel queued/running translate and embed jobs
	$(ENGINE) exec $(WORKER) $(BIN)/nomergon cancel --type translate --type translate-params --type embed

# ---------------------------------------------------------------- migrations --
# Apply, in order, each Nomotheca-RAG/db/migrations/*.sql the database has not
# recorded in schema_migrations, and record it. Fresh databases (schema.sql)
# start with every migration recorded.

DB_CONTAINER ?= nomotheca-legislation-db
PSQL = $(ENGINE) exec -i $(DB_CONTAINER) psql -U jrc -d legislation -v ON_ERROR_STOP=1 -q

migrate: ## Apply the legislation-DB migrations this database has not recorded
	@$(PSQL) -c "CREATE TABLE IF NOT EXISTS schema_migrations (name text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now())"
	@for f in Nomotheca-RAG/db/migrations/*.sql; do \
	  name=$$(basename $$f .sql); \
	  applied=$$($(PSQL) -Atc "SELECT 1 FROM schema_migrations WHERE name = '$$name'"); \
	  if [ -z "$$applied" ]; then echo "applying $$name"; \
	    $(PSQL) < $$f && $(PSQL) -c "INSERT INTO schema_migrations (name) VALUES ('$$name') ON CONFLICT DO NOTHING"; \
	  fi; \
	done; echo "migrations up to date"

# --------------------------------------------------------------------- tests --
# Every suite, on the host. Python runs on the one workspace lock (root
# uv.lock); suites needing the stack skip their live tests when it is down.

PY_PACKAGES = nomos-llm Nomotheca-RAG/ingest Nomoscope-agentic-workflow/pipeline \
              Nomokrisis-evaluation_pipeline Nomergon-worker mcp-server

sync: ## Install every Python package into the workspace .venv (one lock)
	uv sync --all-packages --extra embeddings

lint: ## Lint the five Python packages (root ruff.toml)
	uvx ruff@0.15.0 check $(PY_PACKAGES)

test: test-python test-apps ## Run every test suite (Python packages, both Tauri apps)

test-python:
	@set -e; for p in $(PY_PACKAGES); do echo "== $$p"; (cd "$$p" && uv run --frozen pytest -q); done

test-apps:
	cd Nomoscope-agentic-workflow/ui && npm test
	cd Nomoscope-agentic-workflow/rag-ui && npm test
	cd Nomoscope-agentic-workflow/ui/src-tauri && cargo test
	cd Nomoscope-agentic-workflow/rag-ui/src-tauri && cargo test

_worker:
	@if [ -z "$(WORKER)" ]; then \
	  echo "No worker running: start it with 'make up-gpu' or 'make up-cpu'." >&2; exit 1; fi
