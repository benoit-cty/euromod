# Harvesting Legislation — Source Strategy (FR pilot, LF2025 / LF2026)

*Companion to [`11_database-model.md`](11_database-model.md). Question: where does the fetch skill get legal text from? Scope for the pilot: the French fiscal law relevant to the previous year (LF2025) and the current year (LF2026), designed so the same pattern extends to the other pilot countries. All findings below were verified hands-on on 2026-07-08.*

---

## 1. Framing: what we actually need to ingest

The two anchor texts:

| | Loi | JORF id | Published |
|---|---|---|---|
| LF2025 | LOI n° 2025-127 du 14 février 2025 de finances pour 2025 | `JORFTEXT000051168007` | JO 2025-02-15 |
| LF2026 | LOI n° 2026-103 du 19 février 2026 de finances pour 2026 | `JORFTEXT000053508155` | JO 2026-02-20 |

(Plus, for context, the *loi spéciale* n° 2025-1316 du 26 décembre 2025 that bridged the gap before LF2026.)

**A loi de finances is mostly an *amending* text.** Its articles rewrite articles of the CGI, CSS, etc. What EUROMOD parameters cite — and what point-in-time retrieval must serve — is the **consolidated code article** (e.g. CGI art. 197 *version in force on 2025-06-01*), not the LF article that produced it. So the crawler has two targets, mapping onto two DILA fonds:

1. **JORF** — the LF as published (authentic, frozen). Ingested as an `instrument` whose units answer *"what did the budget law change this year?"* and provide the `instrument_relations` (amends) edges.
2. **LEGI** — the consolidated, dated versions of the code articles the LF touches. These become `legal_unit_versions` with `daterange` validity; this is where the citation fast path and point-in-time queries land.

Concrete proof of why versions matter — CGI art. 197 §1 first-bracket threshold across the three consolidations:

| Version id | In force from | Threshold | Produced by |
|---|---|---|---|
| `LEGIARTI000048805432` | 2024-01-01 | 11 294 € | LF2024 |
| `LEGIARTI000051212954` | 2025-02-16 | 11 497 € | LF2025 |
| `LEGIARTI000053542636` | 2026-02-21 | 11 600 € | LF2026 art. 4 |

## 2. Candidate sources, evaluated

### A. Tricoteuses git mirror — `git.tricoteuses.fr/dila/donnees_juridiques` (JSON)

Community project ([tricoteuses.fr](https://tricoteuses.fr/)) that converts the official DILA dumps to per-document JSON files in git. Fusion of **LEGI + JORF**, ~6.3 GB packed, updated from DILA incremental tarballs **daily** (commit messages name the exact `LEGI_YYYYMMDD-*.tar.gz` applied).

- Path scheme: `{FOND}/{TYPE}/` + the id's digits 9–16 in pairs, e.g. `JORFTEXT000051168007` → `JORF/TEXT/00/00/51/16/80/JORFTEXT000051168007.json`. Raw fetch: `https://git.tricoteuses.fr/dila/donnees_juridiques/raw/branch/main/<path>`.
- A `JORFTEXT`/`LEGITEXT` file is **metadata + structure skeleton only** (~6 KB): ELI, NOR, dates, and `STRUCT.LIEN_SECTION_TA` / `LIEN_ART` links. Sections are separate `SCTA` files, article versions separate `ARTI` files. "One chunk per article" therefore means walking `TEXT → SCTA* → ARTI`.
- `ARTI` files carry exactly what the DB model needs: `DATE_DEBUT`/`DATE_FIN` (→ `legal_unit_versions.validity`), `ETAT`, ELI, `CONTEXTE` (ancestry), `BLOC_TEXTUEL.CONTENU` (HTML), `LIENS` (amends/cites edges → `instrument_relations`), and the full sibling-version list.

**Two traps found by probing:**

1. **Anti-bot protection (Anubis).** Browser-like user agents get a challenge page; plain `curl`, the git protocol and the Gitea API pass *today*. Any fetch skill must treat access as fragile and be polite (low volume, cache-everything — which the lazy design does anyway).
2. **Stale navigation metadata.** The new version files are present (both LF2025 and LF2026 versions of art. 197 exist as files), **but** the CGI structure files and superseded article files are not consistently rewritten: the section file still lists the 2024-01-01 version as `VIGUEUR`/`fin 2999-01-01`, and the CGI `TEXT` file claims `DERNIERE_MODIFICATION: 2024-11-21`. A naive tree walk therefore returns the **wrong "in force" version** (it served us the 11 294 € barème as current). Direct fetches by known `LEGIARTI` id are fine; *discovering* the right id from the mirror's tree is not reliable.

### B. Cloning the repo(s) locally

`git clone` works (no Anubis on the git endpoint). Gives offline access plus **git history as a reproducibility mechanism** — a commit SHA is a perfect `fetch_runs.frozen_label`. But: ~6.3 GB (JSON) or ~29 GB (Markdown repo, see E) for *all* of LEGI+JORF when we need a few dozen articles — the opposite of the lazy, agent-populated design. Sparse checkout doesn't help much because target ids are not known in advance. Verdict: **not for the pilot**; reconsider only if we move to bulk pre-ingestion.

### C. Tricoteuses MCP server — `https://mcp.code4code.eu/mcp` ✔ freshest

MCP server "moulineuse" over the Tricoteuses PostgreSQL database (legal + parliamentary data). Tools verified live: `search_recipes`/`get_recipe`, `search_legal_texts` (Typesense FTS), `list_tables`/`describe_table`/`query_sql` (schemas: `legifrance`, `assemblee`, `senat`, `annuaire`, `droits_et_demarches`), `get_pastilled_article`, `run_script`, real-time Assemblée events. The `legifrance` schema holds `article`, `texte_version`, `section_ta`, `article_lien`, … with the raw DILA JSON in a `data jsonb` column, indexed by `(texte cid, num)`.

**Freshness verified**: `query_sql` for CGI art. 197 returns the 2026-02-21 version as `VIGUEUR` and correctly marks 2024/2025 ones `MODIFIE` — i.e. the database *does not have* the stale-metadata problem of the git mirror's file tree. One SQL query resolves *(code, article number, date)* → exact `LEGIARTI` id. This is precisely the **resolve** step the retrieval pipeline needs.

Caveats: community-run, no SLA, no authentication story, and for JRC provenance the *content* we archive should still be traceable to an official identifier (ELI / Légifrance URL), not just to a third-party DB.

### D. Local PostgreSQL dump — `/home/ben/legi.sql.gz` (3.8 GB)

Same moulineuse schema as C (`public.article`, `texte_version`, `section_ta`, `last_update`, …; needs `ltree` + `pg_trgm`). Its `last_update` table pins the source git commits; the LEGI commit dates to **2025-12-09** → the dump **contains LF2025 consolidations but predates LF2026** (promulgated 2026-02-19). Usable as a zero-latency local resolver for LF2025 work, but needs a refresh (or the MCP fallback) for anything the LF2026 changed. Same JSON payloads as A, so the extraction code is shared.

### E. Tricoteuses Markdown repo — `git.tricoteuses.fr/dila/textes_juridiques`

Same layout as A but every text/section/article rendered as **Markdown with YAML frontmatter** (état, validity dates, id) and — very usefully — the **full ancestry breadcrumb** (`Code général des impôts › Livre premier › … › Section V`) at the top. That is our `chunks.context_header` pre-computed, and clean text for embedding with zero HTML scrubbing. Verified: the LF2025 version of art. 197 exists (`LEGI/ARTI/00/00/51/21/29/LEGIARTI000051212954.md`, 11 497 €), **but the LF2026 id range is absent** — the Markdown rendition lags the JSON repo by months. Use as a *formatting* source when it has the id, never as the discovery/freshness source.

### F. Official channels — Légifrance / DILA

- **legifrance.gouv.fr HTML** (`/loda/id/JORFTEXT…`, `/codes/article_lc/LEGIARTI…`): the canonical *human* URLs, protected by Datadome; scraping is fragile and inappropriate. Use only as the citation URL recorded in provenance, and as a manual spot-check (it's how the staleness in A was confirmed).
- **DILA open data** (`echanges.dila.gouv.fr`): full + daily incremental tar.gz of LEGI/JORF **XML**. Authoritative, no auth — but consuming it means rebuilding exactly the stock+delta pipeline Tricoteuses already runs. Wrong effort/value for a pilot.
- **Légifrance API on PISTE** (AIFE platform, OAuth2, free registration with approval): official JSON API (`/consult/getArticle`, `/consult/legiPart`, `/consult/lawDecree`…), point-in-time capable. For an institutional JRC deployment this is the defensible long-term fetch source. Costs: account approval latency, rate limits, and a heavier client. **Decision: pilot on Tricoteuses, keep the adapter interface API-shaped so PISTE can be swapped in without touching the DB or the pipeline.**

## 3. Recommended design: split *resolve* from *fetch*

The country skill contract has two operations; each source above is good at exactly one of them.

**Resolve** — citation or query → exact version id at a date:
```sql
-- moulineuse schema (local Postgres now, MCP query_sql as freshness fallback)
SELECT id FROM legifrance.article
WHERE data->'CONTEXTE'->'TEXTE'->>'@cid' = 'LEGITEXT000006069577'   -- CGI
  AND num = '197'
  AND daterange((data->'META'->'META_SPEC'->'META_ARTICLE'->>'DATE_DEBUT')::date,
                (data->'META'->'META_SPEC'->'META_ARTICLE'->>'DATE_FIN')::date) @> :as_of::date;
```

**Fetch** — version id → archived authentic content:
- GET the JSON file from the git mirror **by direct id path** (never by tree walk — trap A.2);
- store the HTTP response verbatim in `fetch_snapshots` (URL, sha256, timestamp), the parsed result in `legal_unit_versions` / `unit_texts`;
- record the official ELI + Légifrance URL from `META_COMMUN` as the canonical citation;
- if the Markdown repo has the same id, prefer its body + breadcrumb for `chunks` (`context_header` = breadcrumb); otherwise strip the JSON's `BLOC_TEXTUEL` HTML.

**Freshness canary.** Before trusting any resolver for a given tax year, assert a known fact: *latest version of CGI art. 197 must have `DATE_DEBUT` ≥ the LF's effective date* (2025-02-16 for LF2025, 2026-02-21 for LF2026). The local dump currently fails the LF2026 canary → route those resolves to the MCP until the dump is refreshed. This check is one SQL/MCP call and would have caught every staleness issue found today.

**Ingestion plan for the pilot corpus:**
1. Fetch the two JORF texts (skeleton + `SCTA` tree + every `JORFARTI`) → ~2 instruments, a few hundred units. LF2025 verified end-to-end today (structure at `JORF/TEXT/00/00/51/16/80/`, articles as `JORFARTI…` with HTML `BLOC_TEXTUEL`).
2. From each LF article's `LIENS` (and the `references_donnees_juridiques` repo, which materializes reverse references), collect the set of modified `LEGIARTI` cids → `instrument_relations`.
3. For each touched code article, fetch the versions in force in 2025 and 2026 (+ the immediately preceding one, for diffing) → `legal_unit_versions` with proper `daterange`, superseded rows' ranges closed in the same transaction.
4. Chunk per article with breadcrumb header; embed lazily (lexical leg is live immediately — DB doc §4).

At this scale (two laws + a few hundred consolidated articles) volume is trivial: politeness toward the community mirror and PISTE rate limits are non-issues.

## 4. Generalizing to the other pilot countries

The FR investigation generalizes as a *pattern*, not as code: every country has the same triangle — **official portal (human), official bulk/API (authoritative, heavy), community/derived mirror (convenient, unguaranteed)** — and the same two-operation contract (*resolve*, *fetch*) absorbs whichever corner is best locally. What varies is only the adapter internals, which is exactly where the country-skill architecture puts them.

Two invariants to carry over from the FR findings: **(1) never trust a mirror's navigation metadata without a freshness canary** anchored to a fact you know changed (each country has its own "art. 197"); **(2) archive the official identifier (ELI or national) with every snapshot**, so the convenience source can be swapped for the official one without re-citing anything.

See [RAG\fscal_law_sources.md](RAG\fscal_law_sources.md) for the data source for each countries.

## 5. Open points

1. Register for a PISTE/Légifrance API account now (approval latency), even if the pilot runs on Tricoteuses.
2. Refresh path for the local `legi.sql.gz`: re-download vs. rebuild from the daily git increments — and whether the JRC deployment hosts its own moulineuse instance instead.
3. Whether to add the Tricoteuses MCP as a configured MCP server for the fetch skill (`{"transport":"http","url":"https://mcp.code4code.eu/mcp"}`) or to call its SQL via a thin HTTP client — MCP is the natural fit for the *agentic* fetch step in the retrieval pipeline (§5.3 of the DB doc).
4. Ask Tricoteuses (tricoteuses@tricoteuses.fr) about the stale `ETAT`/section metadata in `donnees_juridiques` — bug or known limitation of the stock+delta fusion?
5. LF2026 Markdown rendition missing — monitor whether `textes_juridiques` catches up; until then FR chunking needs the HTML-strip path.
