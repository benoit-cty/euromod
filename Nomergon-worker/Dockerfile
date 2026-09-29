# Nomergon worker image: the one process that holds model credentials and
# loads models (ADR 0004). Build context is the repo root, so the four Python
# packages are copied in and installed into one environment:
#   docker compose --profile gpu build worker        (WORKER_VARIANT=gpu)
#   docker compose --profile cpu build worker-cpu    (WORKER_VARIANT=cpu)
#
# gpu: CUDA comes from the torch cu126 wheels (they bundle the CUDA runtime), so
# a plain Python base is enough; the NVIDIA container toolkit injects the driver
# when the compose service reserves a GPU. cpu: the CPU-only torch wheel, no
# nvidia-* libraries (~4 GB less to download and extract). Chromium is installed for the Légifrance
# tier-3 fallback (ADR 0002).
FROM python:3.13-slim-bookworm

# gpu or cpu: the extra of Nomergon-worker/pyproject.toml that picks the torch build.
ARG WORKER_VARIANT=gpu

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    # BGE-M3 (2.3 GB) is cached in the hf-cache volume, not the image.
    HF_HOME=/models \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    NOMOS_REPO_ROOT=/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl git \
    && rm -rf /var/lib/apt/lists/*

# Same major as the uv that wrote uv.lock (0.12.x on the dev box).
COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /uvx /bin/

WORKDIR /app

# The three packages the worker runs, then the worker itself. Each is an
# editable path dependency of Nomergon-worker/pyproject.toml, so one `uv sync`
# resolves all four (torch from the index of the chosen extra).
COPY Nomotheca-RAG/ingest /app/Nomotheca-RAG/ingest
COPY Nomoscope-agentic-workflow/pipeline /app/Nomoscope-agentic-workflow/pipeline
COPY Nomokrisis-evaluation_pipeline /app/Nomokrisis-evaluation_pipeline
COPY Nomergon-worker /app/Nomergon-worker

WORKDIR /app/Nomergon-worker
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --extra "${WORKER_VARIANT}"

# Playwright's Chromium and its system libraries (Legifrance ELI tier 3).
RUN --mount=type=cache,target=/root/.cache/uv \
    uv run --frozen --no-dev playwright install --with-deps chromium \
    && rm -rf /var/lib/apt/lists/*

VOLUME ["/models"]

ENTRYPOINT ["uv", "run", "--frozen", "--no-dev", "--no-sync", "nomergon"]
CMD ["serve"]
