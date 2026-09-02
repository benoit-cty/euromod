# Observability — Choosing Arize Phoenix (Decision Document)

*Covers the agentic workflow (Activity 3) and the query-time RAG (Activity 2); companion to `03_activity3_agentic-workflow.md` §4.7 ("Observability: run IDs, retrieval traces, token/cost logging") and to Activity 4/5's need to slice KPIs by model and retrieval strategy.*

---

## 1. What we need observability for

- **Trace the pipeline, not just log it.** The workflow is retrieval → proposal → critique → diff ([03_activity3_agentic-workflow.md](../03_activity3_agentic-workflow.md) §1) — a structured pipeline with LLM steps, not a free-roaming agent. Each run of (country, instrument, reference date) should produce one trace with nested spans: retrieval (candidate chunks, scores, `as_of` filter), proposal generation, critique, diff/routing.
- **Multi-provider by contract.** Activity 5 requires comparing *different LLMs* — Anthropic, Bedrock, Azure/OpenAI, possibly open-weight. Whatever we adopt has to sit underneath the provider, not be coupled to one.
- **Feed the KPI report.** Activity 4's protocol (golden set, recall@k, citation accuracy) and Activity 5's report (per-model, per-retrieval-strategy comparison) both need traces sliceable by run manifest, not just eyeballed logs.
- **Stay inside the reproducibility backbone we already committed to.** Run manifests (pinned model/prompt/config) live in GitLab; the ingested corpus is pinned via `fetch_runs.frozen_label` ([11_database-model.md](../Nomotheca-RAG/11_database-model.md) §7). Observability tooling should sit *on top of* that record, not replace it.

## 2. Candidates considered

| | Langfuse | Arize Phoenix | Laminar | Helicone |
|---|---|---|---|---|
| License | MIT (self-host) | **Elastic 2.0** (source-available) | Apache-2.0 (core; Signals/alerts need a license key) | Apache-2.0 |
| Self-host footprint | Postgres + ClickHouse + Redis + S3 | **1 container** (SQLite, optional Postgres) | Postgres + ClickHouse + RabbitMQ (Rust app) | 4 containers incl. ClickHouse + MinIO |
| Integration model | OTel-based SDK, PydanticAI/OpenAI/Bedrock callbacks | OTel spans (OpenInference) | OTel spans | **Proxy** — change the base URL |
| Evals / datasets | Strong — datasets, experiments, LLM-as-judge, prompt versioning | Strong — datasets, experiments, LLM-as-judge, notebook-friendly | Code-first eval SDK, good | Weak — analytics-first, no real evals/datasets |
| Built for | General LLM app observability | RAG + LLM-pipeline tracing and experimentation | Long-running autonomous agents (transcript views, session replay) | Cost/usage analytics, caching, rate limits |

### Langfuse — rejected on infra weight

Strong fit on paper (self-hostable, OTel-based, multi-provider, human-decision scoring, datasets/experiments matching the golden-set protocol). Rejected because its self-host stack (Postgres + ClickHouse + Redis + S3-compatible storage) is a heavy ask next to the project's current "one Postgres" footprint, for a 20-day-budget pilot. Kept as the fallback if Phoenix's footprint or license becomes a blocker.

### Laminar — rejected on shape mismatch + infra weight

Apache-2.0 across the board and OTel-native, with a genuinely strong UX for long-running autonomous agents (conversation transcripts, session replay, coding-agent debugging, SQL over traces). Two reasons it's not the fit here:
1. Our design stance is explicitly a **structured pipeline with LLM steps, not a free-roaming agent** ([03_activity3_agentic-workflow.md](../03_activity3_agentic-workflow.md) §1) — Laminar's agent-transcript strengths would go mostly unused; a span-tree view (Phoenix) matches our shape better.
2. Its self-host stack (Postgres + ClickHouse + RabbitMQ) is Langfuse-weight infrastructure — the exact thing ruled out above. It's also a young company (YC S24), a continuity consideration for a project reporting through end-2026.

### Helicone — rejected on wrong abstraction level

Helicone is a **proxy**: integration is "change the base URL," and it logs request/response pairs rather than spans. Multi-step workflows get stitched together after the fact; no transcript view, no real evals/datasets, so it can't carry the Activity 4 golden-set experiments. It would be a reasonable *complement* later (uniform cost accounting/caching/rate-limits across Anthropic/Bedrock/Azure) but puts a component in the critical path of every LLM call — a separate governance discussion, not a substitute for tracing. Self-host is also ClickHouse + MinIO, not lighter than Phoenix.

## 3. Why Phoenix

- **Lightest self-host by far.** One container (`arizephoenix/phoenix`), SQLite by default, optional Postgres backing for durability. Fits the existing single-Postgres footprint far better than any ClickHouse-based alternative.
- **OpenTelemetry-native (OpenInference).** Multi-provider is a hard requirement (Activity 5); instrumenting via plain OTel spans means the model/provider underneath is irrelevant to the tracing code.
- **Datasets, experiments, and LLM-as-judge evals map directly onto our validation protocol.** Freeze the golden set as a Phoenix dataset, run each (model × retrieval strategy) configuration as an experiment, attach scores — this is close to a drop-in for the KPI slicing Activity 4/5 need.
- **Span-tree UX matches our pipeline shape.** Retrieval → proposal → critique → diff is naturally nested spans, which is exactly what Phoenix is built to visualize — unlike Laminar, which is optimized for agent conversation replay we don't need.

### Caveat to raise with JRC

Phoenix is **Elastic License 2.0**, not OSI-approved open source — source-available, free for internal self-hosted use, restricted only from being resold as a managed service to third parties. Fine for JRC-internal use (even shared across JRC services), but worth surfacing explicitly at kick-off/procurement review rather than letting it surface later. The instrumentation SDKs (OpenInference) are Apache/MIT, so no ELv2 dependency leaks into our own code.

## 4. Scope boundaries

- **Query-time RAG (retrieve → rerank → generate) and the agentic workflow (proposal/critique/diff):** traced in Phoenix. This is where "retrieval miss vs. extraction error vs. reasoning error" (the failure taxonomy in `05_activity5_technical-report.md` §6) becomes diagnosable per-trace.
- **Structured extraction pass** (rate tables/schedules, [02_activity2_rag-architecture.md](../Nomotheca-RAG/02_activity2_rag-architecture.md) §1.4): traced like any other generation step — it's an LLM call whose errors matter for the KPI report.
- **Ingestion (resolve → fetch → parse → load):** *not* instrumented via Phoenix. It's a data pipeline with almost no LLM in it, and already has purpose-built observability of its own: `fetch_runs` status/stats, append-only `fetch_snapshots`, freshness canaries ([12_ingestion-architecture.md](../Nomotheca-RAG/12_ingestion-architecture.md) §5–6). Adding LLM tracing there is a dependency without added signal.
- **Reproducibility backbone stays external to Phoenix.** GitLab run manifests (pinned model/prompt/config) and `fetch_runs.frozen_label` remain the source of truth; Phoenix is the observation/analysis layer over those runs, not the registry. Same for prompts — GitLab-versioned, tagged onto traces, not authored inside Phoenix's UI.

## 5. Exit strategy

Instrument with plain OpenTelemetry semantics rather than a vendor SDK's proprietary API. Phoenix, Laminar, and Langfuse all ingest OTel traces, so if the ELv2 license or Phoenix's tooling becomes a blocker mid-project, swapping the backend is a config change (`OTEL_EXPORTER_OTLP_ENDPOINT`), not a re-instrumentation.

## 6. Running it

Phoenix runs alongside the legislation DB in the repo-root `docker-compose.yml`:

```bash
docker compose up -d        # ... + Phoenix on http://localhost:6006 (UI + OTLP HTTP), 4317 (OTLP gRPC)
```

Instrument pipeline code by pointing an OTel exporter at `http://localhost:6006` (HTTP) or `localhost:4317` (gRPC) — see `arize-phoenix-otel` for a minimal Python setup helper.

## 7. Recommendation

Adopt **Arize Phoenix**, scoped to the agentic workflow, the query-time RAG, and the structured-extraction step; leave ingestion monitoring to `fetch_runs`/canaries; keep GitLab manifests and `frozen_label` as the reproducibility backbone. Flag the ELv2 license at kick-off. Fallback if footprint or license becomes a blocker: Langfuse (self-host, heavier) or Arize Phoenix Cloud (EU region, if self-hosting stalls).
