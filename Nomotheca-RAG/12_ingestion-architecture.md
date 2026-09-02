# Ingestion Architecture — Python Pipeline (FR/LF2025 first, 27 countries by design)

*Companion to [`11_database-model.md`](11_database-model.md) (target schema) and [`France_sources_analysis.md`](France_sources_analysis.md) (verified FR sources). Question: how is the Python code that ingests LF2025 structured so that country 2..27 is an adapter, not a rewrite?*

---

## 1. It is not a scraper — it is a targeted, archive-first ingester (library first, CLI second)

Three framing decisions before any code:

1. **Worklist-driven, not crawl-driven.** We never spider a portal. Every run starts from explicit identifiers (a JORF text id, a list of `LEGIARTI` ids, a citation + date) and expands them through *known* structural links (JORF `STRUCT` → `SCTA` → `ARTI`, LF `LIENS` → touched code articles). This kills the class of bugs found in the source analysis (stale tree walks) and keeps volume politely small. Consequence: **no Scrapy / crawl framework** — `httpx` + retries is the right size.
2. **Library first.** The retrieval pipeline's step 3 ("miss → agentic fetch") means the *country skill* must be able to ingest one article at cache-miss time with the same code the bulk seed uses. So the package exposes `ingest_citation(jurisdiction, citation, as_of)` and `ingest_instrument(jurisdiction, national_id)` as Python functions; the CLI (`nomotheca-ingest fr instrument JORFTEXT000051168007`) and the skill are both thin callers. Same path, different `fetch_runs.trigger` (`bulk_seed` vs `cache_miss`).
3. **Archive-first.** The HTTP response is written to `fetch_snapshots` *before* parsing is attempted; parsing reads the archived bytes, never the network. A parser bug is then a re-parse of existing snapshots (bump `parser_version`), not a re-fetch — and snapshots double as parser test fixtures.

## 2. Package layout — the shared/adapter boundary

```
ingest/
  pyproject.toml                      # package: nomotheca-legislation-ingest
  src/nomotheca_ingest/
    core/                             # country-agnostic ~80% (invariant, like the schema)
      ir.py            # pydantic intermediate representation (§3)
      snapshots.py     # SnapshotClient: a dumb archiving GET (sha256 hash, follow redirects,
                       #   UA + timeout). NO retries, NO rate limiting, NO sources.terms read —
                       #   politeness/auth/anti-bot handling belongs in each country's fetcher.
      loader.py        # the ONLY module that writes legislation tables (§4)
      chunker.py       # unit text → chunks rows (context_header build, splitting, offsets)
      pipeline.py      # orchestration: resolve → fetch → parse → load, worklist expansion,
                       #   default_source_code() (§3)
      db.py            # fetch_runs lifecycle (status, stats, frozen_label) + snapshot store
      country_reports.py  # non-legislative corpus (EUROMOD Country Reports)
      embeddings.py    # BGE-M3 vector build worker (separate from ingest, §4)
      translate.py     # MT-EN worker
    countries/
      base.py          # CountryAdapter protocol (§3)
      registry.py      # {"FR": FrAdapter, "LT": LtAdapter, ...} — instantiates with zero args
      fr/              # (lt/ has the same shape; it is the most complete example)
        adapter.py     # wires the three FR pieces below; class attrs: jurisdiction,
                       #   default_source_code, canary_facts()
        resolver.py    # (code, num, as_of) → LEGIARTI id: Moulineuse Postgres, MCP fallback
        fetcher.py     # direct-id raw JSON from git.tricoteuses.fr (id → path scheme)
        parser.py      # DILA JSON → IR: pure functions, no I/O (shared by JORF & LEGI fonds)
    cli.py             # typer entry points
    tui.py             # Textual ingestion monitor
  tests/               # parser/fetcher golden tests on inline real-payload excerpts
```

There is no `core/canary.py` runner (yet): `canary_facts()` lives on each adapter, documents the trust anchor, and is asserted by tests (§5).

The rule mirrors §6 of the DB doc: **the loader, chunker, snapshot store, canary runner and CLI never change when a country is added.** A country contributes one `countries/{cc}/` subpackage, seed rows (`jurisdictions`, `sources`, maybe `lang_fts_config`), fixtures, and a canary fact. Everything a source does strangely (Anubis politeness, Datadome avoidance, XML vs JSON vs HTML) is trapped inside its adapter.

## 3. The adapter contract and the intermediate representation

The FR analysis (§3) concluded *resolve* and *fetch* are separate operations best served by different sources. The adapter protocol encodes exactly that, plus pure parsing:

```python
class CountryAdapter(Protocol):
    jurisdiction: str                                     # 'FR'
    default_source_code: str                              # 'FR-LEGI' — must match a sources.code row

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Citation/national-id (+date) → exact fetchable version ids. May query
        a resolver DB/API. Never returns text."""

    def fetch(self, ref: SourceRef, http: SnapshotClient) -> Snapshot:
        """Version id → raw bytes, archived via SnapshotClient (which writes
        fetch_snapshots and returns the snapshot row id)."""

    def parse(self, snapshot_bytes: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
        """Pure function bytes → IR. No network, no DB. Unit-testable on fixtures.
        snapshot.id must land in every VersionIR.fetch_snapshot_id."""

    def expand(self, doc: ParsedDoc) -> list[WorkItem]:
        """Structural + amendment links found in the doc → new worklist items
        (JORF text → its sections/articles; LF article → touched LEGIARTI cids).
        Sees ONLY the ParsedDoc — anything the next fetch generation needs must
        travel in doc.metadata (convention: a child_refs list of
        {source_id, source_type, …} dicts)."""

    def canary_facts(self) -> list[CanaryFact]:
        """Known-truth assertions gating trust in the resolver (§5)."""
```

Contract details that carry load:

- **Adapters construct with zero args** — `registry.get_adapter` calls `adapter_type()`. Configuration goes in class attributes or env, not `__init__` parameters.
- **`default_source_code` is not cosmetic.** `pipeline.ingest_instrument` falls back to it when the caller passes no `--source-code` — and the Nomoscope scout always invokes the CLI without one. `pipeline.default_source_code()` defaults to `f"{CC}-LEGI"` if the attribute is missing, so a country whose `sources.code` is anything else (LT-TAR) fails with `Unknown source code` unless the adapter sets it.
- **`InstrumentIR.jurisdiction` / `source_code` come from `ref`**, never hardcoded in the parser — a copy-paste hazard when starting from the FR parser.
- **`InstrumentIR.title` is a `{lang: title}` dict** keyed by the country language; the chunker's `context_header` picks the title for the text's language from it.
- **`UnitIR.path` must be ltree-safe** (letters/digits/underscore only — sanitize `6-1` → `6_1`); the loader casts it with `::ltree` and PostgreSQL rejects anything else.
- **Emit a stable `national_id` and/or `citation` per unit** — the loader reconciles re-ingested units by them (§4); without one, the same article ingested via two routes duplicates.
- **Open-ended validity is `valid_to=None`.** If the source supplies already-closed contiguous ranges (LT), emit them as-is; the loader's supersession logic handles open-ended chains (FR-style) by closing the previous row (§4).

`ParsedDoc` is the country-neutral IR — pydantic models mirroring the DB entities one-to-one: `InstrumentIR`, `UnitIR` (with `path`, `unit_type`, `citation`), `VersionIR` (`validity` as explicit dates, `source_version_id`, `eli_version`), `TextIR` (`lang`, `authenticity`, `content`, `content_html`). Adapters produce IR; **only `core/loader.py` turns IR into SQL**. That keeps every DB integrity rule (exclusion constraint handling, snapshot FK, JSONB discipline) implemented exactly once, and makes "add NL" a parsing exercise, not a database exercise.

Sub-interfaces stay swappable *within* a country: `fr/resolver.py` has two implementations behind one interface — local Moulineuse Postgres (fast, currently stale past 2025-12-09) and the Tricoteuses MCP `query_sql` (fresh, no SLA) — chosen per call by the canary. The fetcher interface is deliberately shaped like the PISTE API (`get_article(version_id)`), so the decided long-term swap to the official Légifrance API replaces one file.

## 4. The loader — where the DB's integrity rules become code

`loader.py` is small but carries the load-bearing logic; everything is one transaction per unit-version:

- **Idempotent by natural key.** Upsert order: `instruments` on `(source_id, national_id)` → `legal_units` → `legal_unit_versions` on `source_version_id` (falling back to `(legal_unit_id, valid_from)`) → `unit_texts` on `(version_id, lang, authenticity)` → `chunks` (delete + regenerate per text). Re-running any ingest is a no-op, which makes **re-run the resume mechanism** — no checkpoint table, no partial-failure state to manage.
- **Units reconcile by article identity, not path.** A full-code ingest nests an article under its book/chapter (`liv_1.art_197`); the same article fetched standalone — what the Nomoscope scout does at cache-miss time — arrives with a flat path (`art_197`). Keyed on path alone the two become separate `legal_units`, and since the no-overlap constraint is per unit, a superseded consolidation stays open-ended next to its replacement. So non-container units match an existing row by `national_id` OR `citation` first, with `(instrument_id, path)` only as the upsert fallback — which is why adapters must emit a stable one (§3).
- **Supersession in one transaction.** Before inserting a version, `_chain_versions` closes whatever open (or overlapping) version precedes it — shrink to `[old_start, new_start)`, flip `in_force` → `repealed` — and, if the incoming version is open-ended but a *later* version already exists, bounds the new row at that later start. Insert, commit. The GiST exclusion constraint stays as the backstop: if an adapter emits contradictory consolidations the transaction still fails loudly (uncaught) instead of corrupting point-in-time answers.
- **Snapshot FK enforced by construction.** `VersionIR` cannot reach the loader without the `fetch_snapshot_id` returned by `SnapshotClient` — the "no text without origin" rule is unrepresentable to violate.
- **Chunking at load time, embedding never.** Chunks (with breadcrumb `context_header`) are written synchronously so the lexical leg is live immediately (DB doc §4). Embeddings are a **separate worker** that polls for chunks missing `(chunk_id, model_id)` rows or with stale `input_hash` — the scraper has no dependency on any embedding service.

DB access: **psycopg 3 + plain SQL** (no ORM). The schema is hand-written SQL with generated columns, ranges, ltree and exclusion constraints — an ORM adds impedance, not safety, at ~15 statements total.

## 5. Freshness canaries — a first-class pipeline stage

The single most valuable finding of the source analysis was that *convenient mirrors lie about what is in force*. So the pipeline runs canaries **before** trusting a resolver for a tax year:

```python
CanaryFact(citation="CGI art. 197", assert_latest_start_gte=date(2025, 2, 16),  # LF2025
           reason="LF2025 rewrote the barème; any resolver missing this is stale")
```

Outcome is three-valued per (resolver, tax-year): `fresh` → use it; `stale` → fall back to the next resolver in priority order (local dump → MCP → official API), logging the demotion into `fetch_runs.stats`; `unreachable` → fail the run. Each country ships at least one canary per supported tax year — the per-country "art. 197 equivalent" is part of the adapter's definition of done.

**Status: the core runner described above is not built yet.** What exists today is the contract half: every adapter's `canary_facts()` must return at least one `CanaryFact` per supported tax year — the facts document the trust anchor and tests can assert them against the ingested corpus. The gating/fallback runner (and running canaries in CI as an early-warning monitor) remains the design target.

## 6. LF2025 end-to-end (the concrete first run)

`nomotheca-ingest fr instrument JORFTEXT000051168007 --with-consolidations --as-of-years 2025` executes the plan from the source analysis §3 as four worklist generations:

1. **JORF skeleton** — direct-id fetch of the `JORFTEXT` file; parse → `InstrumentIR` (loi type, ELI, NOR); `expand` yields the `SCTA` ids.
2. **Structure + LF articles** — fetch each `SCTA`, then each `JORFARTI`; load ~2 instruments' worth of units/versions/texts/chunks (LF articles are single-version, validity `[2025-02-16, ∞)`). `expand` reads each article's `LIENS` → the set of touched `LEGIARTI` cids, loaded as `instrument_relations` (`amends`, with `to_ref_text` until the target exists).
3. **Consolidations** — for each touched CGI/CSS article: `resolve(code, num, as_of=2025-06-30)` plus the immediately preceding version (for diffing) via Moulineuse SQL; fetch each version's `ARTI` JSON by direct id path; load with proper `daterange`, closing superseded rows. Body text: prefer the Markdown repo rendition when the id exists there (pre-computed breadcrumb), else strip `BLOC_TEXTUEL` HTML — that preference lives inside `fr/fetcher.py`.
4. **Verify** — canary set for 2025 must pass against *the ingested corpus itself* (post-condition, not just resolver gate): `resolve_rag_uri('rag://unit/{art197}@2025-06-01')` must return the 11 497 € text. The run gets `frozen_label` when it seeds an evaluation set.

Scale check: two laws + a few hundred articles ≈ low thousands of HTTP requests worst case, well under any politeness threshold at 1 req/s per source. (No central rate limiter exists — `SnapshotClient` is a dumb GET and `sources.terms` is not read; any throttling, auth, or anti-bot handling a source needs lives in that country's `fetcher.py`.)

## 7. What country N actually costs

| Layer | FR (now) | Country N |
|---|---|---|
| Schema / loader / chunker / snapshots / canary runner / CLI | build once | **zero change** |
| Seed rows (`jurisdictions`, `sources`, `lang_fts_config`) | in `seed.sql` | ~3 rows |
| `resolve` | Moulineuse SQL / MCP | thin client for the local equivalent (BWB SRU for NL, e-TAR for LT, BOE API for ES, …) |
| `fetch` | Tricoteuses raw by id | national portal/API client — the genuinely new work |
| `parse` | DILA JSON → IR | national format → IR; pure + fixture-tested |
| Canary fact | CGI art. 197 barème | one known-changed fact per tax year |

Anti-goals to hold the line on, or 27 countries will erode the design: no country-specific columns in the IR (use `metadata`, promote later per the JSONB discipline); no country conditionals in `core/` (`if jurisdiction == 'FR'` in core is a bug by definition); no adapter writing SQL directly. The pattern already survived its first stress test conceptually — the six pilot peculiarities (BE dual-authentic texts, NL no-ELI, IE hierarchy shape) are all absorbed by the IR because the IR mirrors a schema designed for them.

## 8. Tech choices (deliberately boring)

`httpx` (HTTP/2, timeouts) + `tenacity` (retry/backoff, available to fetchers — the core `SnapshotClient` deliberately does not retry) + `pydantic` v2 (IR validation) + `psycopg` 3 (binary protocol, native range/ltree adapters) + `typer` (CLI) + `pytest` with inline real-payload fixtures. Python ≥3.12. No task queue, no scheduler, no crawl framework — at this volume they are pure liability; if bulk pre-ingestion ever replaces the lazy design, revisit then.

## 9. Open points

1. Where does the ingest package live — `Nomotheca-RAG/ingest/` next to `db/`, or a top-level `ingest/`? (Affects the skill's import path.)
2. Does the country *skill* call the library in-process (Python skill) or via the CLI (subprocess)? CLI keeps the skill language-agnostic; in-process gives structured errors.
3. MT-EN generation: same async worker as embeddings or a third worker? (Both are "derive rows from existing rows" jobs — likely one worker framework.)
4. Politeness defaults for the Tricoteuses mirror before their reply on the staleness question (§5 of the source analysis) — proposal: 1 req/s, `From:` header with contact email, cache-everything (already implied by archive-first).
