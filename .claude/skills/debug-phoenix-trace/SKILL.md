---
name: debug-phoenix-trace
description: Diagnose a Nomoscope workflow run from an Arize Phoenix trace id — inspect the trace's spans straight in the phoenix DB (Postgres in docker), cross-check the legislation corpus, and identify which known failure mode caused a not_found. Use whenever the user gives a Phoenix trace id or asks why a workflow run failed.
argument-hint: <trace-id>
---

# Debug a workflow run from a Phoenix trace id

The argument is a Phoenix trace id (32 hex chars, e.g. `0eeb79ae87efb09d1156918824483f43`).
Inspect it straight in the `phoenix` DB inside the shared Postgres container
(`nomotheca-legislation-db`, host port 5434) — faster and more scriptable than the UI.

## 1. Inspect the trace

```bash
# Locate the trace (project + wall-clock)
docker exec nomotheca-legislation-db psql -U jrc -d phoenix -c "
  SELECT t.trace_id, p.name, t.start_time, t.end_time
  FROM traces t JOIN projects p ON p.id = t.project_rowid
  WHERE t.trace_id = '<TRACE_ID>';"

# Span timeline — the pipeline steps appear as span names
# (frame/retrieve/propose/critique/scout/diff/enqueue); look for the
# span whose duration dominates and for repeated retrieve→propose
# (the scout retry loop)
docker exec nomotheca-legislation-db psql -U jrc -d phoenix -c "
  SELECT s.name, s.span_kind, s.status_code, s.start_time, s.end_time
  FROM spans s JOIN traces t ON t.id = s.trace_rowid
  WHERE t.trace_id = '<TRACE_ID>' ORDER BY s.start_time;"

# Step inputs/outputs live in spans.attributes (JSONB):
# attributes->'input'->>'value' and attributes->'output'->>'value'
# are the step's JSON payloads. Key reads:
# - propose output: found=false + reasoning → retrieval never surfaced the act
# - critique output: issues[] + verdict
# - scout output: queries / urls / candidate_ids / ingested / errors —
#   errors like "embeddings build timed out" or discarded candidate ids
#   in urls are usually the root cause
# - diff output: routing (not_found / needs_review / …)
docker exec nomotheca-legislation-db psql -U jrc -d phoenix -t -c "
  SELECT jsonb_pretty(s.attributes) FROM spans s
  JOIN traces t ON t.id = s.trace_rowid
  WHERE t.trace_id = '<TRACE_ID>' AND s.name = 'scout';"
```

## 2. Cross-check the legislation DB

Most `not_found` runs are corpus problems, not LLM problems:

```bash
# Chunk + embedding coverage of an instrument the scout claims it ingested
# (chunks without embeddings are invisible to the vector leg of retrieval)
docker exec nomotheca-legislation-db psql -U jrc -d legislation -c "
  SELECT i.national_id, count(DISTINCT c.id) chunks, count(DISTINCT e.chunk_id) embedded
  FROM instruments i
  JOIN legal_units lu ON lu.instrument_id = i.id
  JOIN legal_unit_versions v ON v.legal_unit_id = lu.id
  JOIN unit_texts ut ON ut.version_id = v.id
  JOIN chunks c ON c.unit_text_id = ut.id
  LEFT JOIN embeddings e ON e.chunk_id = c.id
  WHERE i.national_id = '<ID>' GROUP BY i.national_id;"

# Is the value anywhere in the corpus at all? (regex over chunk content)
docker exec nomotheca-legislation-db psql -U jrc -d legislation -c "
  SELECT c.id, left(c.content, 120)
  FROM chunks c WHERE c.content ~ '<VALUE_REGEX>';"
# If 0 rows: the act that sets the value was never ingested → gap-fill it,
# e.g. cd Nomotheca-RAG/ingest && uv run python -m nomotheca_ingest.cli \
#      instrument fr LEGIARTI…/JORFTEXT…
```

## 3. Known failure modes

(a) **Embeddings backlog.** The scout ingests an instrument but the follow-up
embeddings build times out — new chunks then exist without vectors, and the
retrieval retry ranks old embedded chunks above them (the vector top-3 bonus
in `retrieval.py` only reaches embedded chunks). Clear the backlog with:

```bash
cd Nomotheca-RAG/ingest && uv run --extra embeddings \
  python -m nomotheca_ingest.cli embeddings build \
  --backend openvino --model-path models/bge-m3-openvino \
  -d postgresql://jrc:jrc@localhost:5434/legislation
```

Per-batch commits make it resumable; the scout's own limit is
`WORKFLOW_SCOUT_EMBED_TIMEOUT` (default 1800 s).

(b) **Id filtered out.** The scout's web search finds the right consolidated
code article but the id is discarded by the country `id_pattern` in
`scout.py` — compare the `urls` list in the scout span against
`candidate_ids`.

(c) **The value genuinely lives elsewhere** (annual arrêté vs. code article) —
verify with the regex corpus search before touching pipeline code.

(d) **`no scout source rules for <CC>`** in the scout span's `errors`: the
country has no entry in `scout.COUNTRY_SOURCES`, so gap-fill never ran. Add
one (domains, `id_pattern`, `act_kinds`, and `ingest_suffix`/`known_key` where
the portal id is not what the ingester fetches or not what the loader stores)
— see Step 5 of the `add-country` skill.

(e) **The parameter has no legal source at all.** Values the national team
assumes rather than reads off a law (LT childcare fees, set by municipal
council resolutions) will be `not_found` on every run forever. Tell-tale: the
regex/term search finds the concept only in incidental clauses, and the
parameter's own description points at a non-legislative schedule. The fix is
not retrieval — flag it `source_type: national_team` in
`Nomoscope-agentic-workflow/pipeline/curation/<CC>.curation.yaml`, apply with
`curate-params`, and the run short-circuits to `national_team_source` before
spending an LLM call.

## 4. Verify the fix

Re-run just the affected parameter and compare the new trace with the same
queries:

```bash
cd Nomoscope-agentic-workflow/pipeline && \
  uv run nomoscope-workflow run-targets '<model_target>' --as-of <date> --force
```
