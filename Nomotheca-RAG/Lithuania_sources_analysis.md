# Harvesting Legislation — Source Strategy (LT pilot)

*Companion to [`11_database-model.md`](11_database-model.md) and [`France_sources_analysis.md`](France_sources_analysis.md) (the FR pattern this transposes). Question: where does the LT fetch skill get legal text from? All findings below were verified hands-on on 2026-08-04 against the live APIs.*

---

## 1. Framing: what we actually need to ingest

Unlike France, Lithuania has **no annual omnibus finance act** driving most parameter changes. Fiscal parameters move through three channels:

1. **Amendments to the substantive acts** (PIT rates and the NPD formula are *in* the GPMĮ itself, art. 6 and 20 — not in a budget law);
2. **Annual government resolutions** (nutarimai) setting the MMA (minimum monthly wage) and base amounts (BSI — bazinė socialinė išmoka, SPB — state pension base);
3. **Automatic indexation** for many benefits (the applied values live in resolutions and Sodra/SADM tables, not in re-legislated text).

What EUROMOD parameters cite — and what point-in-time retrieval must serve — is the **dated consolidated version** of an act ("suvestinė redakcija"), the exact analogue of the FR LEGI consolidation. TAR (Teisės aktų registras, the official Register of Legal Acts) maintains these natively with validity dates.

The anchor acts, resolved to their TAR identifiers (live-verified 2026-08-04, all `galioja` = in force):

| Act | Official no. | `dokumento_id` | Covers |
|---|---|---|---|
| Gyventojų pajamų mokesčio įstatymas (**GPMĮ**, PIT law) | IX-1007 (2002-07-02) | `TAR.C677663D2202` | PIT rates (art. 6), NPD tax-exempt amount formula (art. 20) |
| Valstybinio socialinio draudimo įstatymas (**VSDĮ**, Sodra law) | I-1336 | `TAR.0F9036415DBD` | Social insurance contributions |
| Ligos ir motinystės socialinio draudimo įstatymas | IX-110 | `TAR.068516AF734B` | Sickness/maternity/paternity/childcare benefits |
| Išmokų vaikams įstatymas | I-621 | `TAR.1DEDD43B92AE` | Child benefits (universal + additional) |
| Piniginės socialinės paramos nepasiturintiems gyventojams įstatymas | IX-1675 | `TAR.3EEE59417F13` | Social assistance (cash) |
| Nedarbo socialinio draudimo įstatymas | IX-1904 | `TAR.FDF42614DE52` | Unemployment insurance |

Two identifier systems coexist: the **e-tar document id** (`dokumento_id`, e.g. `TAR.C677663D2202` for pre-2014 acts, a 32-hex UUID-ish string for newer ones) and the **TAR registration code** (`tar_kodas`, e.g. `1021010ISTA0IX-1007` for old acts, `2014-21296`-style for post-2014). The `dokumento_id` is the stable citation key — it is what the canonical e-tar URL carries.

## 2. Candidate sources, evaluated

### A. e-tar.lt portal (HTML) ✘ blocked

The official portal (`www.e-tar.lt/portal/lt/legalAct/{id}` and `.../asr` for the current consolidation) **403s every plain HTTP client** — verified independently by the Triangulator project (July 2026: all 14 e-tar URLs in the LT country report failed with 403; see `08 - EUROMOD Triangulator/legislation/LT/PENDING.md`) and reconfirmed by probing. Browser-impersonation (curl_cffi) works but is exactly the fragile scraping the archive-first design avoids. **Use e-tar.lt URLs only as the canonical citation recorded in provenance, never as the fetch source.**

### B. **data.gov.lt Spinta open-data API** ✔ the fetch source

Lithuania publishes the *entire TAR register* — including full texts and all consolidated versions — through the national open-data platform, keyless, JSON, CC BY 4.0:

```
https://get.data.gov.lt/datasets/gov/lrsk/teises_aktai/{model}
```

Three models (namespace listing verified live):

| Model | Content | Key fields |
|---|---|---|
| `Dokumentas` | Every registered legal act, **full text as published** | `dokumento_id`, `tar_kodas`, `rusis` (type: Įstatymas, Nutarimas, Įsakymas…), `atv_dok_nr` (official no.), `pavadinimas` (title), `tekstas_lt` (full text), `nuoroda` (canonical e-tar URL), `priimtas`, `paskelbta_tar`, `isigalioja`, `negalioja`, `galioj_busena`, `priemusi_inst` |
| `Suvestine` | **Every dated consolidated version** of every act | `dokumento_id` (parent act), `suvestines_id`, `galioja_nuo`, `galioja_iki`, `tekstas_lt` (full consolidated text), `nuoroda` (`…/legalAct/{dokumento_id}/{suvestines_id}`) |
| `Priedas` | Annex texts | — |

Queries use the Spinta expression syntax in the raw query string — `select()`, `sort()`, `limit()`, exact match `field="value"`, substring `field.contains("…")`:

```
# resolve: all consolidations of the GPMĮ, validity ranges only (no heavy text)
…/Suvestine?dokumento_id="TAR.C677663D2202"&select(suvestines_id,galioja_nuo,galioja_iki,nuoroda)&sort(galioja_nuo)

# fetch: one consolidation with full text
…/Suvestine?dokumento_id="TAR.C677663D2202"&suvestines_id="ExnKtBqZbP"

# act metadata by official number
…/Dokumentas?atv_dok_nr="IX-1007"&rusis="Įstatymas"
```

(Values must be percent-encoded with `()=&.,!*` kept safe; `"` and non-ASCII encoded.)

**Verified against the GPMĮ:** 82 consolidations, contiguous validity ranges, the latest open-ended from **2025-01-02** (`galioja_iki = null`); the 2024-01-01→2024-05-30 consolidation is 201 KB of clean plain text. `galioja_nuo`/`galioja_iki` map directly onto `legal_unit_versions.validity` — **the point-in-time requirement is satisfied natively**, with full history (the FR "thin history" concern does not apply to LT).

**Text structure** (drives the parser): plain text, one act per payload, articles introduced by `N straipsnis. Title` (including suffixed numbers like `20-1 straipsnis`), chapters as `I SKYRIUS` headings, amendment trails as `Straipsnio pakeitimai:` blocks, and a first line `Suvestinė redakcija nuo YYYY-MM-DD iki YYYY-MM-DD` self-describing the validity. Splitting on the straipsnis regex yields exactly the per-article chunks the DB wants (~40 articles for the GPMĮ).

### C. Community prior art — read as documentation

- **matematicsolutions/lt-eli-mcp** (PyPI `lt-eli-mcp`): MCP server over the same Spinta API. Confirms the endpoint, the query-escaping rules, retry statuses (429/5xx), and the citation contract (e-tar URL as the stable national identifier — Lithuania has **no data.europa.eu ELI dataset**). Notably it only uses `Dokumentas` — it does *not* exploit `Suvestine`, so it cannot do point-in-time; our adapter goes further.
- **Ansvar-Systems/Lithuanian-law-mcp**: "TAR API → parse → SQLite FTS5" over 12k+ statutes — same pattern, same source.

### D. e-Seimas (e-seimas.lrs.lt) — convenience only

Parliament's database; has some **English translations** of major laws, but not kept current. Treat as a display convenience, never as source of truth. The legacy `www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=…` URLs cited in older Country Reports still resolve and are scrapeable (the Triangulator successfully archived several) — useful for pre-TAR (pre-2014) historical versions if ever needed.

### E. Administrative sources (parameter values)

- **VMI** (State Tax Inspectorate, vmi.lt) — NPD calculators, applied rates.
- **Sodra** (sodra.lt) — contribution rates, base amounts; **403s scrapers** like e-tar (verified by the Triangulator).
- **SADM** (Ministry of Social Security and Labour) — benefit amounts.

These matter because MMA/BSI/SPB values are set by government *nutarimai* — which are themselves in TAR (`rusis="Nutarimas"`), so the same API fetches them; the administrative sites are only cross-checks.

## 3. Recommended design: resolve and fetch on the same API

Unlike FR (where resolve and fetch needed different sources), LT's single API serves both — the split survives as *two query shapes*, not two sources:

**Resolve** — citation (+ date) → exact consolidation:
1. Alias table maps EUROMOD-style citations (GPMĮ, VSDĮ…) → `dokumento_id`;
2. One `Suvestine` query with `select(suvestines_id, galioja_nuo, galioja_iki)` — no text — picks the version whose range contains `as_of`.

**Fetch** — consolidation id → archived authentic content:
- GET the single `Suvestine` row with `tekstas_lt`, store the HTTP response verbatim in `fetch_snapshots`;
- record the canonical e-tar URL (`nuoroda`) as the citation URL, the `dokumento_id` as `instruments.national_id` anchor;
- parse: split into straipsniai → one `legal_unit` per article, one `legal_unit_versions` row per (article × consolidation) with `validity [galioja_nuo, galioja_iki)`, `unit_texts` with `lang='lt'`, `authenticity='authentic'`.

**Freshness canary.** *Latest consolidation of the GPMĮ must have `galioja_nuo` ≥ 2025-01-02* (live-verified today). Assert before trusting the API for a tax year; extend with one known-changed fact per year (e.g. the 2025 NPD step: monthly allowance 747 € below MMA 1038 €, withdrawal 0.49 to 2 387.29 €, then 0.18 — CR Y16 §2.2.3).

**Ingestion plan for the pilot corpus:**
1. For each of the six anchor acts: fetch the `Dokumentas` row (instrument skeleton: title, official no., dates, canonical URL).
2. List its `Suvestine` versions; keep those overlapping the EUROMOD window (validity end ≥ 2022-01-01) — ~10 per act instead of all 82.
3. Fetch each kept consolidation, split per article, load with proper `daterange` (the loader's supersession logic closes nothing here — TAR ranges arrive already closed and contiguous).
4. Chunk per article with breadcrumb header (`{act title} > {N straipsnis} (vig. {date})`); machine-translate to EN via the existing `translate run` worker (LT is already in `LANG_NAMES`); embed with BGE-M3 (Lithuanian is in its coverage — this is the multilingual test case the project wanted).

Scale check: 6 acts × ~10 consolidations ≈ 60 requests of 100–300 KB — trivial; the API is a state open-data platform designed for bulk consumption, no politeness concerns beyond the client's existing single-flight behaviour.

## 4. What transposes from the FR findings

- **Same triangle, different winner.** Official portal (human, blocked) / official open-data API (authoritative, excellent) / community mirror (documentation only). For LT the official API corner wins outright — no Tricoteuses-style intermediary needed, and *resolve* needs no separate database at all.
- **Canary invariant holds.** The mirror-staleness trap that bit FR can't be ruled out here either (`suv_duom_atnaujinimas` on `Suvestine` rows shows refresh lag is possible) — the canary is still mandatory before each tax-year run.
- **Identifier invariant holds.** Every snapshot records the canonical e-tar URL + `dokumento_id` + `tar_kodas`, so if the fetch source ever changes (e.g. a future TAR API v2), nothing needs re-citing.
- **Language.** LT is the project's strongest multilingual-RAG test: consolidations are Lithuanian-only. FTS falls back to `fts_lt` (`simple` + unaccent — already in the schema); semantic search rides the MT-EN chunks and BGE-M3's native LT support.

## 5. Open points

1. `Suvestine` covers consolidations from ~2014 (TAR's creation). For parameters needing pre-2014 versions, the fallback is e-Seimas legacy pages (`www3.lrs.lt`) — not needed for the 2022-2025 EUROMOD window.
2. Government *nutarimai* for MMA/BSI/SPB: same API, but the values are in short standalone resolutions rather than consolidated acts — decide whether to ingest them as one-version instruments or route them via `national_team_source`.
3. English translations on e-Seimas: worth ingesting as `authenticity='official_translation'` where they exist and are dated? (Convenience for the UI; MT-EN remains the retrieval path.)
4. Rate limits / ToS: CC BY 4.0, keyless. Confirm no burst limits on get.data.gov.lt before a full 6-act seed (the lt-eli-mcp client retries on 429, suggesting they exist).
