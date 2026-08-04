---
name: add-country
description: Integrate a new country into the Nomotheca legislation ingester — source analysis, seed rows, countries/<cc>/ adapter (resolver/fetcher/parser), registry entry, tests, and end-to-end verification. Use when asked to add, integrate, or implement ingestion for a new member state (e.g. "add the Netherlands", "start ingesting Spanish legislation").
---

# Add a country to the Nomotheca ingester

Adding country N is **an adapter, not a rewrite**: core (`loader`, `chunker`, `snapshots`, `pipeline`, CLI, schema) must not change. The full rationale is in `Nomotheca-RAG/12_ingestion-architecture.md`; worked examples: `Nomotheca-RAG/France_sources_analysis.md` (FR) and `Nomotheca-RAG/Lithuania_sources_analysis.md` (LT). Existing adapters live in `Nomotheca-RAG/ingest/src/nomotheca_ingest/countries/`.

## Step 0 — Source analysis first (a doc, not code)

Before any code, produce `Nomotheca-RAG/<Country>_sources_analysis.md` following the FR/LT template. Every country has the same triangle — official portal (human-facing, often bot-blocked), official bulk/API source, community mirror — and the analysis picks a corner for each of the two operations, **resolve** (citation + date → exact version id) and **fetch** (version id → raw content). Start from the country's row in `Nomotheca-RAG/fiscal_law_sources.md`.

Hands-on verification is mandatory, not optional:
- Probe the candidate API live (`curl`) and record exact URL patterns, one real payload, and its structure in the doc.
- Verify **point-in-time capability**: can you enumerate dated consolidated versions of the country's PIT law and fetch one by id? Map the version-validity fields onto `legal_unit_versions.validity`.
- Identify the country's "art. 197 equivalent" — one fact you know changed at a known date (a bracket threshold, an allowance amount) from the EUROMOD Country Report (`08 - EUROMOD Triangulator/country-reports/Y16/<CC>_Y16.md`, sections 2.2 "Main policy changes"). This becomes the freshness canary.
- Check the Triangulator's prior art: `08 - EUROMOD Triangulator/.claude/skills/law-scraper/scripts/scrape_<CC>.py` and `legislation/<CC>/PENDING.md` record which portals 403 plain HTTP clients.

## Step 1 — Seed rows (rows, not DDL)

Check `Nomotheca-RAG/db/seed.sql` and `db/schema.sql`. The country needs:
- a `jurisdictions` row (code, name, official langs);
- 1–2 `sources` rows — **note the `code` value** (e.g. `FR-LEGI`, `LT-TAR`); everything keys off it;
- a `lang_fts_config` row (+ `CREATE TEXT SEARCH CONFIGURATION fts_<lang>` in schema.sql if the language is new; languages without a PostgreSQL stemmer start from `simple` + unaccent).

FR/NL/LT/ES/IE/BE rows already exist. Reset with `docker compose down -v && docker compose up -d` to re-apply.

## Step 2 — The adapter package

Create `ingest/src/nomotheca_ingest/countries/<cc>/` with `adapter.py`, `fetcher.py`, `parser.py`, `resolver.py`. The contract is `countries/base.py::CountryAdapter` (protocol) and the IR types in `core/ir.py`. Register it in `countries/registry.py` (`"<CC>": <Cc>Adapter` + import). Mirror the LT adapter — it is the most complete example.

Load-bearing details the docs get subtly wrong (the **code** is authoritative):

- `parse(snapshot_bytes, ref, snapshot)` takes **three** args (the design doc shows two) — `snapshot.id` must land in every `VersionIR.fetch_snapshot_id`.
- **Adapters must construct with zero args** (`registry.get_adapter` calls `adapter_type()`).
- `pipeline.ingest_instrument` defaults `source_code` to `f"{CC}-LEGI"` unless the adapter defines `default_source_code`. Set `default_source_code = "<your sources.code>"` on the adapter class — the Nomoscope scout invokes the CLI without `--source-code`, so a wrong default fails with `Unknown source code`.
- `UnitIR.path` must be **ltree-safe** (letters/digits/underscore only — sanitize `6-1` → `6_1`); the loader casts it with `::ltree`.
- Emit a stable `national_id` and/or `citation` per unit — the loader reconciles re-ingested units by `national_id` OR `citation` (falling back to `(instrument_id, path)`); without one, the same article ingested via two routes duplicates.
- `InstrumentIR.jurisdiction` / `source_code`: take them from `ref`, don't hardcode (a copy-paste hazard from the FR parser).
- `InstrumentIR.title` is a `{lang: title}` dict — key it by the country language; the chunker's `context_header` picks from it.
- Versions with open-ended validity: `valid_to=None`. If the source supplies already-closed contiguous ranges (LT), emit them as-is; the loader's supersession logic (`_chain_versions`) handles open-ended chains (FR-style) by closing the previous row.
- `expand()` sees only the `ParsedDoc` — anything the next fetch generation needs must travel in `doc.metadata` (convention: a `child_refs` list of `{source_id, source_type, …}` dicts).
- `SnapshotClient` is a dumb GET (no retries, no rate limiting, no `sources.terms` read despite the design doc). Politeness, auth, or anti-bot handling belongs inside your `fetcher.py`. Archive-first: parse only the bytes the snapshot stored.
- `canary_facts()` must return at least one `CanaryFact` per supported tax year. (No core runner exists yet — the facts still document the trust anchor and tests can assert them.)
- Parsers are **pure functions** (no network/DB) — test them on inline fixture payloads.

## Step 3 — Tests

`ingest/tests/test_<cc>_parser.py` + `test_<cc>_fetcher.py`, following `test_lt_parser.py` / `test_fr_parser.py`: inline real payload excerpts (trimmed), assert instrument metadata, unit splitting, validity dates, ltree-safe paths, and `expand()` child refs. Run: `cd Nomotheca-RAG/ingest && uv run pytest -k <cc>`.

## Step 4 — Verify end-to-end

```bash
docker compose up -d      # from repo root
cd Nomotheca-RAG/ingest
uv run python -m nomotheca_ingest.cli instrument <cc> <national-or-source-id> -d postgresql://jrc:jrc@localhost:5434/legislation
```

Then check in SQL: instruments/units/versions/texts/chunks counts, a point-in-time query (`WHERE validity @> '<date>'`) returning the value your canary fact predicts, and `chunks.context_header` looking sane. Optionally ingest the Country Report (`cli country-report <cc> <path-to-md>` — fully generic, needs only the markdown; keep parameter codes in headings, the CR search enrichment depends on them) and build embeddings (`uv sync --extra embeddings`, then `cli embeddings build`).

## Anti-goals (hold the line)

No country-specific columns in the IR (use `metadata`; promote per the JSONB discipline). No `if jurisdiction == 'XX'` in `core/`. No adapter writing SQL. No tree-walk discovery of "current" versions without a canary — mirrors lie about what is in force (the FR staleness trap).
