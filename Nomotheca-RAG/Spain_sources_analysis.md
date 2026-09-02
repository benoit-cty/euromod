# Harvesting Legislation — Source Strategy (ES pilot)

*Companion to [`11_database-model.md`](11_database-model.md), [`France_sources_analysis.md`](France_sources_analysis.md) and [`Lithuania_sources_analysis.md`](Lithuania_sources_analysis.md) (the patterns this transposes). Question: where does the ES fetch skill get legal text from? Every finding below was verified hands-on on 2026-08-11 against the live API.*

---

## 1. Framing: what we actually need to ingest

Spain sets fiscal parameters through four channels:

1. **Amendments to the substantive acts** — the PIT general and savings schedules are *in* the LIRPF itself (arts. 63 and 66), as are the personal/family minima (arts. 57–61);
2. **The annual Ley de Presupuestos Generales del Estado (LPGE)** — historically the main vehicle (IPREM, pension indexation), but note the LPGE was **prorogued for 2024 and 2025**, so recent changes arrive through ordinary laws and decree-laws instead (e.g. Ley 7/2024 for the 2025 savings rate);
3. **Annual Reales Decretos** — SMI (minimum wage), contribution bases and rates;
4. **19 regional (autonomous-community) laws** — the regional half of the PIT schedule and a large catalogue of regional credits.

What EUROMOD parameters cite — and what point-in-time retrieval must serve — is the **consolidated text of an act at a date**. BOE maintains these natively, and (unlike FR's LEGI or LT's TAR, which mint a whole new consolidated document per amendment) **BOE versions at the level of the individual provision**: each `bloque` (article) carries its own list of dated versions. This is the closest native fit to `legal_unit_versions` of any of the six pilot countries.

Anchor acts, resolved to their BOE identifiers (live-verified 2026-08-11):

| Act | Official no. | BOE id | Covers |
|---|---|---|---|
| **Ley 35/2006** del IRPF (**LIRPF**) | 35/2006 | `BOE-A-2006-20764` | PIT: general scale (art. 63), savings scale (art. 66), mínimos personales y familiares (arts. 56–61), deductions |
| **RD 439/2007**, Reglamento del IRPF (**RIRPF**) | 439/2007 | `BOE-A-2007-6820` | Withholding tables, procedural detail |
| **RDL 8/2015**, texto refundido de la **LGSS** | 8/2015 | `BOE-A-2015-11724` | Contributions, pensions, contributory & non-contributory benefits |
| **Ley 19/2021** del Ingreso Mínimo Vital | 19/2021 | `BOE-A-2021-21007` | IMV (minimum income scheme) |
| **RD 87/2025**, salario mínimo interprofesional | 87/2025 | `BOE-A-2025-2576` | SMI (1 184 €/month × 14, 2025) |
| **DL 1/2011** Galicia, tributos cedidos *(regional exemplar)* | 1/2011 | `BOE-A-2011-18161` | Galician regional PIT scale and credits |

Two identifier systems coexist: the **BOE analytical id** (`BOE-A-YYYY-NNNNN` — the stable key, and what appears in every boe.es URL) and the **official number** (`35/2006`). The BOE id is the citation key *and* the fetch key, so — unlike LT — the adapter needs no `known_key` indirection.

## 2. Candidate sources, evaluated

### A. boe.es HTML (`/buscar/act.php?id=…`) — citation target only

The human-facing consolidated view. It does **not** block plain HTTP clients (no Anubis/403 problem as in FR/LT), but it is HTML built for reading and carries no version structure a parser should depend on. **Use it as the canonical citation URL recorded in provenance, never as the fetch source** — the API below serves the same content with explicit version metadata.

### B. **BOE open-data REST API (`legislacion-consolidada`)** ✔ the fetch *and* resolve source

```
https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{BOE-A-id}
```

Keyless, free, documented, no rate limit encountered.

> **Load-bearing quirk: the API is XML-only.** `Accept: application/xml` is **mandatory**. Every other value — including no header at all, `*/*`, and `application/json` — is rejected with `HTTP 400 "No soportado ningún mime type de la cabecera Accept"`. There is no query-parameter override (`?format=`, `?formato=`, `?output=`, `.xml` all fail). This contradicts the "JSON REST API" impression in [`fiscal_law_sources.md`](fiscal_law_sources.md) and is the single thing most likely to make a first implementation attempt fail.

Endpoints (verified against the LIRPF):

| Endpoint | Returns | Size (LIRPF) |
|---|---|---|
| `/id/{id}` | **everything**: `metadatos` + `analisis` + `metadata-eli` + `texto` | 3.5 MB |
| `/id/{id}/metadatos` | act-level metadata only | 1.4 KB |
| `/id/{id}/analisis` | subject codes + amendment graph (`anteriores`/`posteriores`) | 40 KB |
| `/id/{id}/texto` | all blocks, all versions | 3.2 MB |
| `/id/{id}/texto/indice` | block index (id, título, fecha_actualizacion) | 74 KB |
| `/id/{id}/texto/bloque/{bloque}` | one block, all its versions | 35 KB |
| `?limit=N` (collection root) | most-recently-updated consolidated norms | — |

`/id/{id}/indice` does **not** exist (404) — the index lives under `/texto/indice`. There is **no `?fecha=` point-in-time filter** on any endpoint (`400 "Parámetros no soportados"`): the API hands over the *entire* version history and point-in-time selection happens in SQL, which is exactly what the schema's `validity @> as_of` is for.

**Payload structure** (drives the parser):

```xml
<response><status><code>200</code></status><data>
  <metadatos>
    <identificador>BOE-A-2006-20764</identificador>
    <rango codigo="1300">Ley</rango>
    <numero_oficial>35/2006</numero_oficial>
    <fecha_disposicion>20061128</fecha_disposicion>
    <fecha_publicacion>20061129</fecha_publicacion>
    <ambito codigo="1">Estatal</ambito>
    <url_eli>https://www.boe.es/eli/es/l/2006/11/28/35</url_eli>
  </metadatos>
  <analisis>…</analisis>
  <metadata-eli>…RDF…</metadata-eli>
  <texto>
    <bloque id="a63" tipo="precepto" titulo="Artículo 63">
      <version id_norma="BOE-A-2006-20764" fecha_publicacion="20061129" fecha_vigencia="20070101">
        <p class="articulo">Artículo 63. Escala general del Impuesto.</p>
        <p class="parrafo">…</p>
        <table class="tabla">…</table>
      </version>
      <version id_norma="BOE-A-2020-17339" … fecha_vigencia="20210101">…</version>
    </bloque>
  </texto>
</data></response>
```

**This is the whole ingestion problem solved in one GET.** One request per act yields the complete instrument: metadata, every article, and every dated version of every article, each version naming the norm that made it (`id_norma`). No expansion generation, no N+1 fetching, one snapshot per act.

`bloque/@tipo` (verified on two acts): `precepto` (articles + disposiciones), `encabezado` (título/capítulo/sección headings), `nota_inicial`, `preambulo`, `firma`.

**Verified against the LIRPF:** 273 blocks, 649 versions; art. 63 has 8 versions (latest in force 2021-01-01), art. 66 has 8 (latest 2024-12-22). Against the LGSS: 631 blocks, 1 044 versions. The corpus is live — the LIRPF's `fecha_actualizacion` was 2026-04-29 and blocks carry versions dated as late as 2026-04-30.

### C. Community prior art — read as documentation

- **ComputingVictor/MCP-BOE** — wraps this API as an MCP server (search, block diffs between dates, PDF extraction). Confirms the endpoint shapes; same "read as documentation, don't depend on it" caveat as the FR/LT mirrors.

### D. Administrative sources (parameter values)

- **Agencia Tributaria** (`sede.agenciatributaria.gob.es`) — IRPF manuals, withholding tables;
- **Seguridad Social** — bases y tipos de cotización tables.

Both are cross-checks only: the SMI and contribution-base values are set by *reales decretos*, which are themselves in the BOE consolidated collection and fetched by the same adapter.

### E. Regional gazettes — partially avoidable

The BOE consolidated collection **does** include autonomous-community norms (`ambito = Autonómico`; 96 of 200 in a recent-updates listing), but **coverage of the regional ceded-tax laws is partial** — verified per region:

| Regional ceded-tax law | In BOE consolidada? |
|---|---|
| Galicia, DL 1/2011 | ✔ `BOE-A-2011-18161` — 78 blocks, 202 versions, art. 5 versioned through 2026-01-01 |
| C. Valenciana, Ley 13/1997 | ✔ `BOE-A-1998-8202` |
| Madrid, DL 1/2010 | ✘ absent |
| Andalucía, DL 1/2018 | ✘ absent |

So the regional layer needs **no new adapter** where BOE consolidates it — same API, same parser, only a different id. Where BOE does not (Madrid, Andalucía), the fallback is the regional gazette (BOCM, BOJA), which is a separate source and a separate effort. This resolves open item 5(b) in [`fiscal_law_sources.md`](fiscal_law_sources.md): the answer is *partial coverage, verified region by region*.

**Note on ELI:** `boe.es/eli/…` URIs exist and are the right citation URL, but they are **not an API lookup key** — `/datosabiertos/api/legislacion-consolidada/eli/{eli}` 404s. ELI resolution would mean scraping the HTML page. Resolve by BOE id instead.

## 3. Recommended design: one fetch per act, versions selected in SQL

Unlike FR (resolve and fetch on different sources) and like LT (one API, two query shapes), ES collapses further: **resolve and fetch are the same request**, because the payload contains the full history.

**Resolve** — citation → BOE id. There is **no usable search endpoint**: the collection root accepts `limit`/`from`/`to` but every documented `query=` form is rejected (`400 "El parámetro query tiene un formato no soportado"`). So resolution uses a curated alias table (the LT pattern): `LIRPF`, `Ley 35/2006`, `IRPF` → `BOE-A-2006-20764`. `as_of` plays no part in resolution — the fetched act carries every version, and the date filter is applied by `validity @> as_of` at query time.

**Fetch** — GET `/id/{BOE-A-id}` with `Accept: application/xml`, archive the response verbatim in `fetch_snapshots`.

**Parse** — one `legal_unit` per `bloque`, one `legal_unit_versions` row per `<version>`:
- `validity = [fecha_vigencia, next version's fecha_vigencia)`, last version open-ended;
- `amendment_note = {id_norma, fecha_publicacion}` — the norm that made this version;
- `unit_texts` with `lang='es'`, `authenticity='authentic'`;
- `encabezado` blocks become `is_container=true` units **with no versions**, preserving the título/capítulo/sección hierarchy without emitting near-empty "TÍTULO I" chunks into retrieval.

### Four quirks the parser must handle (all found in the live data, not hypothesised)

1. **Duplicate `fecha_vigencia` within one block.** Two norms can take effect the same day (LIRPF arts. 93 and 96 at 2023-01-01; 9 blocks in the LGSS). Naively chaining `valid_to = next start` then yields an empty range and `VersionIR` rejects it (`valid_to must be after valid_from`). Resolution: collapse same-date versions, keeping the last in document order (the later-published text).
2. **Out-of-order version chains.** Blocks are *not* reliably sorted by `fecha_vigencia` — LIRPF art. 7 goes `…20100113, 20100101…` and art. 94 `…20110112, 20101231…`. Sort before chaining or the ranges invert.
3. **Block ids are not ltree-safe.** 41 of 273 in the LIRPF and 146 of 631 in the LGSS contain hyphens (`ci-2`, `da-17`, `dt-6`). They must be sanitized (`-` → `_`) before the loader's `::ltree` cast.
4. **Tables must be rendered row-wise.** The scales *are* the EUROMOD parameters, and a naive `itertext()` over `<table>` yields whitespace soup with the numbers unmoored from their columns. Rendering each `<tr>` as ` | `-joined cells keeps the scale readable — which the verbatim-extract anti-hallucination check depends on.

**Freshness canaries** (verified live, tied to CR Y16 §2.2):
- *LIRPF art. 66 — latest version must start ≥ 2024-12-22*: Ley 7/2024 raised the top savings rate to 30 % above 300 000 € for 2025 (CR "Main policy changes between 2024-2025").
- *LIRPF art. 63 — latest version must start ≥ 2021-01-01*: the 47 % top general bracket (LPGE 2021), unchanged since.
- *LGSS art. 19 — latest version must start ≥ 2024-01-01*: contribution-base rules.

**Scale check:** 5 state acts + 1 regional ≈ 6 requests of 0.5–4 MB. Trivial, and the API is a state open-data service built for bulk consumption.

```sh
cd Nomotheca-RAG/ingest

# Ingest the Country Report (context, never evidence)
uv run python -m nomotheca_ingest.cli country-report es "../../08 - EUROMOD Triangulator/country-reports/Y16/ES_Y16.md" -d postgresql://jrc:jrc@localhost:5434/legislation

# Ingest the legislation
export EUROMOD_DATABASE_URL=postgresql://jrc:jrc@localhost:5434/legislation
for id in BOE-A-2006-20764 BOE-A-2007-6820 BOE-A-2015-11724 BOE-A-2021-21007 BOE-A-2025-2576; do
  uv run python -m nomotheca_ingest.cli instrument es "$id"
done
```

## 4. What transposes from the FR/LT findings

- **Same triangle, a new winner.** Official portal (human-facing) / official open-data API (authoritative) / community mirror (documentation). For ES the official API corner wins outright *and* is the best of the six: it is the only one that versions at provision level, so no consolidation-diffing is needed.
- **Canary invariant holds.** Nothing about BOE rules out refresh lag; the canary stays mandatory before trusting a tax year.
- **Identifier invariant holds.** Every snapshot records the BOE id and the ELI, so a future API v2 changes nothing about citations.
- **The blocked-portal problem does not apply.** Neither boe.es nor the API blocks plain clients — but the mandatory `Accept` header is the ES equivalent gotcha, and it lives in `fetcher.py` exactly where FR's anti-bot handling and LT's retry logic live.
- **Language.** Spanish has a native PostgreSQL stemmer, so `fts_es` (already in `schema.sql`) is a real stemming configuration rather than the `simple` fallback LT and IE need.

## 5. Open points

1. **Regional layer scope.** Galicia and C. Valenciana are ingestible today; Madrid and Andalucía are not in BOE consolidada and would need BOCM/BOJA adapters. A pragmatic demo scopes to state + Galicia to prove the pattern (as `fiscal_law_sources.md` suggests).
2. **LPGE prorogation.** With no 2024/2025 budget law, the scout must look for ordinary laws and decree-laws, not only "Ley de Presupuestos" — reflected in the `act_kinds` wording registered with the Nomoscope scout.
3. **`analisis` amendment graph** is fetched but not loaded: no adapter emits `InstrumentRelationIR` and nothing consumes `ParsedDoc.relations` yet. When an amendment-graph consumer exists, ES can populate it for free from the payload already archived.
4. **`fecha_vigencia` is the legal entry-into-force date, not the fiscal effect date.** The 2025 savings scale is a worked example: its version starts **2024-12-22** (when Ley 7/2024 entered into force) while the measure applies "con efectos desde el 1 de enero de 2025". LIRPF art. 63's LPGE-2008 version behaves the same way (starts 2008-01-16, applies to income year 2008). Retrieval at a mid-year `as_of` is unaffected — by 1 July the right version is in force either way — but a January `as_of`, or any attempt to read the effect date off `validity`, is not. The effect date is stated in prose in BOE's amendment trail, which is why that text is kept. Worth watching if ES parameters ever need a `temporal_basis: income_year` flag like the FR income-tax family.
5. **Foral regimes (País Vasco, Navarra) are out of scope** per CR Y16 — their PIT laws are outside BOE and are deliberately not ingested.

## 6. Status (2026-08-11)

All six anchor acts are ingested end-to-end through `countries/es/`, plus the ES Country Report (126 units, 224 chunks) as a separate corpus class:

| Act | BOE id | Ámbito | Units | Versions | Chunks |
|---|---|---|---|---|---|
| LIRPF — Ley 35/2006 | `BOE-A-2006-20764` | Estatal | 273 | 599 | 794 |
| RIRPF — RD 439/2007 | `BOE-A-2007-6820` | Estatal | 215 | 353 | 418 |
| LGSS — RDL 8/2015 | `BOE-A-2015-11724` | Estatal | 631 | 914 | 1 044 |
| IMV — Ley 19/2021 | `BOE-A-2021-21007` | Estatal | 94 | 101 | 125 |
| SMI — RD 87/2025 | `BOE-A-2025-2576` | Estatal | 11 | 12 | 12 |
| Tributos cedidos Galicia — DL 1/2011 | `BOE-A-2011-18161` | Autonómico | 78 | 179 | 392 |

**Total: 1 302 units, 2 158 dated versions, 2 785 chunks.** Re-ingestion is idempotent (row counts unchanged on a second run).

**Verification.** The point-in-time query is the one that matters:

```sql
SELECT luv.validity, ut.content
FROM legal_units lu
JOIN legal_unit_versions luv ON luv.legal_unit_id = lu.id
JOIN unit_texts ut ON ut.version_id = luv.id
JOIN instruments i ON i.id = lu.instrument_id
WHERE i.national_id = 'BOE-A-2006-20764'
  AND lu.metadata->>'bloque_id' = 'a66'
  AND luv.validity @> DATE '2025-07-01';
```

returns validity `[2024-12-22,)` and the savings scale carrying the new `300.000,00` bracket that Ley 7/2024 introduced for 2025. All three canaries hold as declared (`a63` → 2021-01-01, `a66` → 2024-12-22, LGSS `a19` → 2024-01-01), and RD 87/2025 art. 1 reads "39,47 euros/día o **1184** euros/mes" (BOE writes the SMI without a thousands separator — worth knowing before pattern-matching amounts).

> **Read art. 66 carefully — it holds two scales.** Paragraph 1 is the **state half** of the savings schedule and its top bracket reads `300.000,00 | 35.940 | En adelante | 15`; paragraph 2, for taxpayers resident abroad, carries the **full** rate: `300.000,00 | 71.880 | En adelante | 30`. The Country Report's "savings rate increased from 28 % to 30 %" is the combined state+regional figure, so a naive match of an EUROMOD savings rate against the first table in art. 66 finds 15 %, not 30 %. This is the ES face of the normalisation rule in `CLAUDE.md`: compare like with like, and for ES that means knowing whether a parameter is the state share or the total.

Each version's text also ends with BOE's own editorial amendment trail ("Se modifica, con efectos desde el 1 de enero de 2025, por la disposición final 7.1 de la Ley 7/2024, de 20 de diciembre. Ref. BOE-A-2024-26694#df-7"), which is retained: it is authentic published content and states the *fiscal effect* date that `fecha_vigencia` does not (see open point 4).

Two quirks beyond the four anticipated in §3 were found only by running the ingest, both now covered by tests:

- **`.//texto` is a trap.** `<analisis>` nests one `<texto>` element per amendment reference — 131 of them in the LIRPF payload — so a descendant search binds to the first reference blurb and the parse silently yields **zero units**. Both lookups are anchored to `./data/`.
- **Block titles repeat, and identical citations silently merge units.** An act accumulates several "Disposición transitoria primera" blocks over successive amendments (BOE tells them apart only by id: `dtprimera` vs `dtprimera-2`). Because the loader reconciles units by `national_id` *or* `citation`, the second provision's versions were being grafted onto the first — 3 units lost in the RIRPF, 1 each in the LGSS and the Galician text. Citations are now made unique within an act by suffixing repeats (`… primera (2)`).

**One core change was needed:** `SnapshotClient.get()` gained an optional `headers` argument, because the BOE API rejects every request without `Accept: application/xml` and there is no URL-level override. It is country-neutral (content negotiation is an HTTP concern), backward-compatible, and keeps fetching inside the archive-first client rather than letting the adapter bypass snapshotting.

Spain is registered with the Nomoscope scout (`COUNTRY_SOURCES["ES"]` + `ID_HINTS["ES"]`): domain `boe.es`, id pattern `BOE-A-\d{4}-\d+`, no `ingest_suffix` and no `known_key` (a bare BOE id is both the citation key and the fetch key).

**Not done:** `curation/ES.curation.yaml` — EUROMOD ES parameters have not been extracted yet (`extracted_parameters/enriched/` has FR, IE and LT only), so there is nothing to flag `source_type: national_team` against. This matters before the first ES workflow run: regional childcare fees, imputations and calibrated regional minimum-income schemes have no act to cite and would otherwise burn one LLM run per parameter per year rediscovering that. Next steps: extract ES parameters, then `translate` + `embeddings` over the ES corpus.
