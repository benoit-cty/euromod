# Harvesting Legislation — Source Strategy (NL pilot)

*Companion to [`11_database-model.md`](11_database-model.md), [`France_sources_analysis.md`](France_sources_analysis.md) (the original pattern) and [`Lithuania_sources_analysis.md`](Lithuania_sources_analysis.md) (the adapter this most closely follows). Question: where does the NL fetch skill get legal text from? Every finding below was verified hands-on on 2026-09-01 against the live services; the exact queries are reproduced so they can be re-run.*

---

## 1. Framing: what we actually need to ingest

The Netherlands is, on paper, the best-instrumented of the six pilot countries — and it is the only one where the *fetch* problem is trivially solved and the *selection* problem is the hard part. Fiscal parameters move through three channels:

1. **The annual Belastingplan**, which amends the substantive acts (Wet IB 2001, Wet LB 1964) directly — the tariff table lives *in* Wet IB 2001 art. 2.10, not in a separate schedule;
2. **Bijstellingsregelingen** — ministerial indexation regulations published each December in the Staatscourant, which rewrite the amounts inside the acts. Note the canary below: art. 2.10's 2025 version has `bron="Stcrt.2024-38492"`, i.e. the operative source of the 2025 brackets is an indexation *regulation*, not the Belastingplan;
3. **Automatic indexation of benefit amounts** (toeslagen, bijstandsnormen), where the applied values land in AMvBs and ministerial regulations rather than in the framework act.

What EUROMOD parameters cite — and what point-in-time retrieval must serve — is the **dated consolidated version** of an act, which the Dutch call a **`toestand`** ("state"). The Basiswettenbestand (BWB) maintains these natively, retains every one ever published, and — uniquely among the six — models them **bitemporally** (see §2C, the single most important finding in this document).

The anchor acts, resolved to their BWB identifiers and live-verified in force at 2025-06-30 (all fourteen resolved successfully on 2026-09-01):

| Act | Abbrev. | BWB id | `toestand` count | Covers |
|---|---|---|---|---|
| Wet inkomstenbelasting 2001 | Wet IB 2001 | `BWBR0011353` | 733 | PIT boxes, **tariff table (art. 2.10)**, heffingskortingen |
| Wet op de loonbelasting 1964 | Wet LB 1964 | `BWBR0002471` | 235 | Wage tax, payroll credits |
| Algemene wet inkomensafhankelijke regelingen | AWIR | `BWBR0018472` | 100 | Common framework for all means-tested toeslagen |
| Wet op de zorgtoeslag | — | `BWBR0018451` | 49 | Health-care allowance |
| Wet op de huurtoeslag | — | `BWBR0008659` | 121 | Rent allowance (`bho_nl`) |
| Wet op het kindgebonden budget | WKB | `BWBR0022751` | 62 | Child-related budget (`chall_nl`) |
| Algemene Kinderbijslagwet | AKW | `BWBR0002368` | 96 | Child benefit (`bfa_nl`) |
| Participatiewet | Pw | `BWBR0015703` | 213 | Social assistance (`bsanet_nl`) |
| Algemene Ouderdomswet | AOW | `BWBR0002221` | 172 | State pension (`poa_nl`) |
| Wet kinderopvang | Wko | `BWBR0017017` | 122 | Childcare allowance |
| Werkloosheidswet | WW | `BWBR0004045` | 313 | Unemployment benefit (`bunct_nl`) |
| Wet financiering sociale verzekeringen | Wfsv | `BWBR0017745` | 195 | **Contribution rates** (`ersic_nl`, `peoplesic_nl`) |
| Algemene nabestaandenwet | Anw | `BWBR0007795` | 189 | Survivor benefit (`psu_nl`) |
| Wet arbeid en zorg | Wazo | `BWBR0013008` | 76 | Pregnancy/childbirth allowance (`bma_nl`) |

`BWBR…` is the stable key, and it is stable across **renaming**: `BWBR0015703` was enacted as the *Wet werk en bijstand* and is today the *Participatiewet*, same id throughout. This is why the adapter carries a curated id table rather than resolving by title at runtime (§2D).

## 2. Candidate sources, evaluated

### A. wetten.overheid.nl portal (HTML) ✘ not the fetch source

The human-facing portal. Serves the same consolidations behind Juriconnect URLs carrying both temporal axes — `https://wetten.overheid.nl/jci1.3:c:BWBR0011353&artikel=2.10&z=2025-01-01&g=2025-01-01`. The Triangulator project scraped it in July 2026 and had to reach for **`curl_cffi` browser impersonation to avoid HTTP 429** (`08 - EUROMOD Triangulator/.claude/skills/law-scraper/scripts/scrape_NL.py`), and resolved law titles by scraping *Yahoo* because the portal has no usable search API. That is exactly the fragile scraping the archive-first design exists to avoid.

**Use wetten.overheid.nl URLs only as the canonical human-readable citation recorded in provenance, never as the fetch source.** The Juriconnect reference is worth constructing and storing precisely because it is the citation a Dutch lawyer recognises.

### B. **BWB repository (repository.officiele-overheidspublicaties.nl)** ✔ the fetch source

KOOP publishes the entire Basiswettenbestand as static XML over plain HTTPS — keyless, no auth, no rate limiting observed, empty `robots.txt`. Three objects per act:

| URL | Content |
|---|---|
| `…/bwb/{BWB}/manifest.xml` | **Every `toestand` ever published**, with both temporal axes, size and hash. 525 KB for Wet IB 2001. |
| `…/bwb/{BWB}/{label}/xml/{BWB}_{label}.xml` | **One dated consolidation**, full text, ~2.5 MB average |
| `…/bwb/{BWB}/{BWB}.WTI` | Legal-technical info (citeertitels, abbreviations, amendment history). **21 MB** for Wet IB 2001 — too heavy for routine use; the manifest carries what the adapter needs. |

`https://repository.officiele-overheidspublicaties.nl/bwb/{BWB}` (no trailing path) 301-redirects to `manifest.xml`, so the bare BWB id is a legitimate fetch reference.

A manifest entry:

```xml
<expression label="2025-04-25_3">
  <metadata>
    <datum_inwerkingtreding>2025-04-25</datum_inwerkingtreding>
    <einddatum>2025-07-18</einddatum>
    <zichtdatum_start>2026-02-21</zichtdatum_start>
    <zichtdatum_eind>9999-12-31</zichtdatum_eind>
  </metadata>
  <manifestation label="xml">
    <metadata><hashcode>…</hashcode><size>2962580</size></metadata>
    <item label="BWBR0011353_2025-04-25_3.xml" _deleted="false"/>
  </manifestation>
</expression>
```

The root element also carries `_latestItem="2026-01-01_1/xml/BWBR0011353_2026-01-01_1.xml"` — a free freshness signal on every fetch.

### C. The bitemporal trap: `geldigheid` vs `zicht` ⚠️ **the finding that shapes the adapter**

BWB is the only pilot source that is genuinely **bitemporal**, and getting this wrong silently returns superseded text. Two independent axes:

- **`geldigheid`** (validity) — when the law *was in force*. This is what `legal_unit_versions.validity` means, and the only axis EUROMOD cares about.
- **`zicht`** (view/knowledge) — *what KOOP knew when*. When a later amendment is published with retroactive or deferred effect, KOOP mints a **new `toestand` for the same validity window** reflecting the updated knowledge.

Querying the version in force at 2025-06-30 returns **four** documents, all with identical validity:

```
geldig 2025-04-25→2025-07-18   zicht 2025-03-15→2025-07-18   BWBR0011353/2025-04-25_0
geldig 2025-04-25→2025-07-18   zicht 2025-07-19→2025-12-31   BWBR0011353/2025-04-25_1
geldig 2025-04-25→2025-07-18   zicht 2026-01-01→2026-02-20   BWBR0011353/2025-04-25_2
geldig 2025-04-25→2025-07-18   zicht 2026-02-21→9999-12-31   BWBR0011353/2025-04-25_3   ← current knowledge
```

The `_N` suffix on the label is the zicht generation, **not** a version number. Picking `_0` — the obvious "first match" — gives you what the government believed in March 2025, not what the law is now understood to have been.

**Rule, enforced in `countries/nl/parser.py::select_toestanden`: among the expressions whose `[datum_inwerkingtreding, einddatum]` contains the target date, take the one with `zichtdatum_eind = 9999-12-31`.** That is always exactly one. `9999-12-31` is also the sentinel for an open-ended `einddatum`, mapped to `valid_to=None`.

### D. SRU 2.0 search service (zoekservice.overheid.nl) ✔ resolve-by-name only

The BWB collection is also exposed through KOOP's SRU 2.0 endpoint — `https://zoekservice.overheid.nl/sru/Search?x-connection=BWB` — reporting **147,979 records, `lastUpdate` 2026-09-01** (i.e. same-day freshness). Searchable indexes, from `operation=explain`: `dcterms.identifier`, `dcterms.modified`, `dcterms.type`, `overheid.authority`, and `overheidbwb.{rechtsgebied, overheidsdomein, titel, afkorting, wetsfamilie, geldigheidsdatum, zichtdatum, bekendmaking, dossiernummer}`.

Two traps, both verified:

- **It answers `HTTP 406` unless you send `Accept: application/xml`** — while still returning a perfectly valid body. Exactly the failure mode already documented for the ES BOE API, and the reason `SnapshotClient.get` takes a `headers` argument.
- **`overheidbwb.titel` is a substring match that ranks amending acts first.** `titel="Wet op de loonbelasting 1964"` returns *Wijzigingswet Wet op de loonbelasting 1964, enz.* as record 1 of 428; `titel="Algemene Kinderbijslagwet"` returns *Wijzigingswet Algemene Kinderbijslagwet (aanpassing kinderbijslag 1993)*. Naive title resolution ingests the wrong act.

`overheidbwb.afkorting` is far better behaved — `AWIR`, `AKW`, `AOW`, `WW`, `Wfsv`, `ANW` and `Wet IB 2001` each return the base act as record 1 — but it is not safe either (`Pw` returns the *Pensioenwet*, not the Participatiewet). The reliable programmatic form is an **exact case-insensitive match on `dcterms:title` over a page of results**, which cleanly recovered AWIR, AOW, WW and the Wet op de huurtoeslag.

**Conclusion: SRU is the discovery layer, not the fetch layer.** The adapter carries a curated `KNOWN_ACTS` table for the fourteen anchor acts (the LT pattern), and uses SRU only to resolve an unknown name to a BWB id. Point-in-time selection needs no SRU call at all — the manifest carries both axes, so a known act costs **one** extra request rather than one per target date.

For the record, SRU *can* do point-in-time directly, and this is the form to use if the manifest ever becomes unavailable:

```
?version=2.0&operation=searchRetrieve&x-connection=BWB
&query=dcterms.identifier=BWBR0011353 and overheidbwb.geldigheidsdatum=2025-06-30
```

returning `<overheidbwb:locatie_toestand>` — the direct repository XML URL — per zicht generation. `overheidbwb.rechtsgebied=Belastingrecht` matches **12,126** records, which is the documented "Belastingdienst ingests all tax law" use case and the natural basis for a future bulk seed.

### E. Text structure (drives the parser)

The `toestand` XML is a well-formed, schema-validated document (`toestand_2016-1.xsd`), *not* HTML — no scraping, no `BeautifulSoup`. Wet IB 2001 at 2025-01-01 is 2.9 MB containing **498 `<artikel>` elements** nested under `<hoofdstuk>`/`<afdeling>`/`<paragraaf>`.

Every article carries its own version identity as attributes — and this is the second load-bearing finding:

```xml
<artikel bwb-ng-variabel-deel="/Hoofdstuk2/Afdeling2.3/Artikel2.10"
         stam-id="2833703" versie-id="30526332" label="Artikel 2.10"
         inwerking="2025-01-01" bron="Stcrt.2024-38492" effect="wijziging" status="goed">
  <kop><label>Artikel</label><nr>2.10</nr><titel>Tarief belastbaar inkomen uit werk en woning</titel></kop>
  <lid><lidnr>1</lidnr><al>…</al><table>…</table></lid>
</artikel>
```

| Attribute | Meaning | Maps to |
|---|---|---|
| `stam-id` | stable identity of the article **across all versions** | `legal_units.national_id` |
| `versie-id` | identity of *this* version of the article | `legal_unit_versions.source_version_id` |
| `inwerking` | when **this article** entered into force | `validity` lower bound |
| `bron` | the act/regulation that produced it (`Stb.2020-543`, `Stcrt.2024-38492`) | `amendment_note` |
| `effect` | `nieuwe-regeling` / `wijziging` / `vervallen` | `amendment_note` |
| `status` | `goed` / `vervallen` | `version_status` (`vervallen` → `repealed`) |

This solves the problem that would otherwise sink NL ingestion — see §3.

**Tables.** Unlike FR and LT, the Dutch fiscal parameters that matter most are in **CALS tables**, not prose. Art. 2.10's tariff is a four-column `<table>`; a parser that only collects `<al>` text emits the numbers as a meaningless run of fragments. The parser renders tables as pipe-delimited rows so the figures stay adjacent to their headers and, critically, so an LLM's `supporting_extract` can be matched character-for-character against the stored chunk. **This is the NL-specific parser risk; the tests pin it.**

### F. Administrative / parameter-value sources

- **Belastingdienst** — *Handboek Loonheffingen* (annual), rate tables, newsletters.
- **Rijksoverheid.nl / Toeslagen** — published benefit amounts.
- **SVB** (AKW, AOW, Anw) and **UWV** (WW, Wazo) — applied amounts.

These are cross-checks. Because Dutch indexation is done by *bijstellingsregeling* and those regulations are themselves in BWB, the repository already serves the operative text; the administrative sites do not need to be scraped.

## 3. Recommended design: manifest as index, toestand as content

Both operations run against the repository; SRU is reserved for name lookup. Source ids mirror the LT adapter's two shapes:

- `BWBR0011353` → the act's **version index** (`manifest.xml`)
- `BWBR0011353/2025-01-01_0` → **one dated consolidation** (the toestand XML)

**Resolve** — citation (+ date) → exact toestand:
1. `KNOWN_ACTS` maps EUROMOD-style citations (Wet IB 2001, AOW, AWIR…) → BWB id;
2. the returned reference is the act's manifest, which expansion turns into the toestanden actually needed. Unknown names fall back to SRU exact-title/afkorting lookup.

**Fetch** — id → archived authentic content: a plain GET of static XML, stored verbatim in `fetch_snapshots`, parsed from the archived bytes only.

### The version cross-product, and why `versie-id` dissolves it

The naive approach fails badly. Wet IB 2001 has 733 toestanden; each is the **whole act** (2.5 MB, 498 articles) because the Netherlands republishes the entire act on every amendment. Loading every article of every toestand in the 2021+ window would mean 81 fetches × 2.5 MB ≈ 200 MB **for one act**, producing ~40,000 `legal_unit_versions` rows of which the overwhelming majority are byte-identical restatements of an unchanged article.

Two mechanisms cut this down:

1. **Sample, don't sweep.** Fetch one toestand per EUROMOD policy date (1 January of each year in the window, plus current knowledge) rather than every published state — ~6 fetches per act. Because each article carries its own `inwerking`, the validity we record is still the *true* legal start date, not the sampling date. The tradeoff is honest and bounded: an article version that both began and ended strictly between two sampled dates is not captured. For a system that asks "what was the law on 1 January of system year Y", that is the right thing to miss; it is recorded as open point §6.1.
2. **Dedupe on `versie-id`.** Emitting `source_version_id = versie-id` makes `LegislationLoader._upsert_version` a no-op for every article that did not change between two sampled toestanden — it looks up `(legal_unit_id, source_version_id)` before inserting. The 498 articles of the second and later fetches collapse to just the ones that actually moved.

Versions are emitted **open-ended** (`valid_to=None`) and the loader's `_chain_versions` closes the predecessor where the successor begins — the FR-style chain, which is correct here precisely because `inwerking` is a start date with no matching per-article end date. (LT's already-closed contiguous ranges are the other case.)

**Freshness canary.** Wet IB 2001 art. 2.10, version in force 2025-01-01, must show the three-band schedule introduced for 2025:

| Bracket | Threshold | Rate in the law |
|---|---|---|
| 1 | up to € 38.441 | 8,17% |
| 2 | € 38.441 – € 76.817 | 37,48% |
| 3 | above € 76.817 | 49,50% |

⚠️ **Read the rate column carefully.** CR Y16 §2.2.3 states the 2025 first-band rate as **35.82%** and explicitly qualifies it "*(including contributions national insurances)*". The statute says **8,17%**, because Wet IB 2001 art. 2.10 fixes the *tax* component only; the premies volksverzekeringen are levied alongside under the Wfsv and the combined rate is what the Belastingdienst publishes. The thresholds (38.441 / 76.817) and the upper two rates (37,48% / 49,50%) are identical in both, because national-insurance premiums are only levied in the first band. Any NL parameter mapping must state which of the two bases it uses — this is the NL analogue of the FR Country Report's mislabelled Table 2.77, and it is a far easier mistake to make because *both numbers are correct*.

**Ingestion plan for the pilot corpus:**
1. For each anchor act, fetch `manifest.xml` and select the toestand for each EUROMOD policy date at current knowledge.
2. Fetch each selected toestand; split into `<artikel>` units under their `<hoofdstuk>`/`<afdeling>` containers; emit `unit_texts` with `lang='nl'`, `authenticity='authentic'`.
3. Chunk per article with breadcrumb header (`{citeertitel} > {Artikel N} (vig. {date})`); machine-translate to EN via `translate run`; embed with BGE-M3 (Dutch is well covered).
4. Ingest the Country Report as context (`instrument_type='country_report'`).

Scale check: 14 acts × ~6 toestanden × ~1.5 MB ≈ 125 MB of static XML — comparable to the LT sweep, and against infrastructure explicitly built for the Belastingdienst to bulk-consume.

```sh
cd Nomotheca-RAG/ingest
export EUROMOD_DATABASE_URL=postgresql://jrc:jrc@localhost:5434/legislation

# Ingest the Country Report (context, never evidence)
uv run python -m nomotheca_ingest.cli country-report nl "../../08 - EUROMOD Triangulator/country-reports/Y16/NL_Y16.md"

# Ingest the legislation
for id in BWBR0011353 BWBR0002471 BWBR0018472 BWBR0018451 BWBR0008659 BWBR0022751 \
          BWBR0002368 BWBR0015703 BWBR0002221 BWBR0017017 BWBR0004045 BWBR0017745 \
          BWBR0007795 BWBR0013008; do
  echo "=== $id ==="
  uv run python -m nomotheca_ingest.cli instrument nl "$id" 2>&1 | tail -3
done
```

## 4. What transposes from the FR/LT findings

- **Same triangle, official-bulk corner wins again.** Human portal (rate-limited, needs browser impersonation) / official bulk repository (static XML, excellent) / community mirror (WetSuite's catalogue at wetsuite.nl, documentation only). As in LT, no intermediary is needed — but unlike LT, *resolve* and *fetch* genuinely are different services (SRU vs repository), even though the common case touches only one.
- **Canary invariant holds, and NL makes it cheap.** `manifest.xml/@_latestItem` and SRU's `lastUpdate` both expose freshness without a content fetch.
- **Identifier invariant holds.** Every snapshot records the BWB id, the toestand label (with its zicht generation) and the Juriconnect citation, so a future source change re-cites nothing.
- **New failure mode, not present in FR/LT: bitemporality.** FR and LT expose one time axis; NL exposes two and will happily serve a stale-knowledge document that is *not* wrong, merely superseded. This cannot be caught by a canary on the latest version — the stale document is a real historical artefact with correct-looking dates. It is caught only by the selection rule in §2C, which is why that rule is unit-tested rather than left to a code comment.
- **Language.** Dutch has a PostgreSQL stemmer, so `fts_nl` (`dutch` + unaccent) was already in the schema; NL is the easy multilingual case, not the hard one.

## 5. Seed rows

`db/seed.sql` and `db/schema.sql` already carry everything NL needs — the `jurisdictions` row (`NL`, `{nl}`), the `sources` row **`NL-BWB`** (`id_system='bwb_juriconnect'`, `supports_point_in_time=true`, `supports_eli=false`), the `fts_nl` text-search configuration and its `lang_fts_config` row. The `sources.base_url` deliberately stays `https://wetten.overheid.nl` — the citation base — while the fetcher targets the repository host.

`supports_eli=false` is correct and was re-verified: the BWB XML contains no ELI attributes anywhere. The Netherlands uses Juriconnect (`jci1.3:c:BWBR0011353&artikel=2.10&z=…&g=…`) as its citation scheme, and the two Juriconnect parameters `z` and `g` are precisely the zicht/geldigheid pair of §2C.

## 6. Open points

1. **Sampling granularity.** One toestand per policy date misses article versions that lived entirely between two sampled dates. Raising the sampling to every distinct `datum_inwerkingtreding` in the window is a one-line change to the date list at ~13× the bytes; do it if a parameter is ever traced to a mid-year change the corpus cannot see.
2. **Toeslagen amounts are in AMvBs, not the acts.** The Wet op de zorgtoeslag sets the *formula*; the standard premium is fixed by a separate `besluit`. These are BWB documents too (same adapter, different ids) — they need enumerating per benefit, or routing via `national_team_source`.
3. **The 8,17% vs 35,82% basis question** (§3) needs a decision recorded in the NL curation file before any NL tax-schedule parameter is run, not after.
4. **Combined-rate parameters may be genuinely uncitable from legislation alone** where EUROMOD models tax and premium as one rate: no single article states 35,82%. Candidate for `source_type: national_team`.
5. **Bulk seed.** `rechtsgebied=Belastingrecht` (12,126 records) plus the KOOP full-set request (~160 GB, 14 GB zipped, via wetten@overheid.nl) is the path to corpus-wide coverage if targeted ingestion proves too narrow.
6. **Rate limits / ToS.** No limits observed and `robots.txt` is empty, but no published quota was found either. Confirm with servicedesk@koop.overheid.nl before a full-corpus sweep; the targeted plan in §3 is well inside any plausible limit.

## 7. Status (2026-09-01)

All fourteen anchor acts are ingested end-to-end via `countries/nl/`, plus the Country Report as a separate corpus class:

| Act | BWB id | Units | Dated versions |
|---|---|---|---|
| Wet IB 2001 | BWBR0011353 | 512 | 807 |
| Participatiewet | BWBR0015703 | 175 | 292 |
| Wet LB 1964 | BWBR0002471 | 168 | 286 |
| WW | BWBR0004045 | 227 | 239 |
| Wfsv | BWBR0017745 | 183 | 210 |
| Wko | BWBR0017017 | 173 | 203 |
| AWIR | BWBR0018472 | 86 | 171 |
| Anw | BWBR0007795 | 136 | 150 |
| AOW | BWBR0002221 | 111 | 127 |
| Wet op de huurtoeslag | BWBR0008659 | 80 | 123 |
| Wazo | BWBR0013008 | 88 | 103 |
| AKW | BWBR0002368 | 77 | 95 |
| WKB | BWBR0022751 | 13 | 27 |
| Wet op de zorgtoeslag | BWBR0018451 | 10 | 22 |

Total: **2 039 units, 2 855 dated versions, 2 866 chunks**, from 84 fetched toestanden (~14 minutes wall clock, no rate limiting encountered).

Verified after loading:

- **The canary passes.** `validity @> '2025-06-30'` on Wet IB 2001 art. 2.10 returns the three-band table with `| – | € 38.441 | – | 8,17% |`, `| € 38.441 | € 76.817 | € 3.140 | 37,48% |`, `| € 76.817 | – | € 17.523 | 49,50% |`. The same query at `'2024-06-30'` returns the 2024 schedule (`€ 38.098 | € 75.518 | € 3.550 | 36,97%`) — point-in-time retrieval genuinely discriminates, it is not returning the latest text for every date.
- **Zero overlapping validity ranges** across all 2 855 versions: the open-ended emit plus the loader's `_chain_versions` produces a clean chain (art. 2.10: 2022→2023→2024→2025→2026, each closed by its successor).
- **The `versie-id` dedupe works as designed.** Six toestanden × 512 units would be 3 072 version rows for Wet IB 2001; the load produced **807**, with 366 articles carrying a single version because they did not change anywhere in the window.
- **Reconciliation onto the seed row works.** `db/seed.sql` already carried art. 2.10 under the flat path `art_2_10`; the real ingest, whose path is the nested `hoofdstuk2.afdeling2_3.artikel2_10`, matched it on `national_id` (`BWBR0011353-2.10`) and updated it rather than inserting a duplicate, exactly as `_existing_unit_id` intends.
- **Chunk breadcrumbs read correctly** (`Algemene Ouderdomswet > AOW, artikel 12 (vig. 2015-01-01)`), and 9 articles land as `not_yet_in_force`.
- The Country Report is loaded as `instrument_type='country_report'` (125 units), the separate corpus class Nomoscope's evidence retrieval excludes.

Registered with the Nomoscope scout (`COUNTRY_SOURCES["NL"]` + `ID_HINTS["NL"]`): domain `wetten.overheid.nl`, id pattern `BWBR\d{7}` (matching both the plain and Juriconnect URL forms while excluding `BWBV…` treaty ids), no `ingest_suffix` and no `known_key` — a bare BWB id is what `NlResolver` returns and what `instruments.national_id` stores.

**Not done, and blocked rather than skipped:** the curation file `Nomoscope-agentic-workflow/pipeline/curation/NL.curation.yaml`. Authoring the `source_type: national_team` flags requires the EUROMOD parameter export, and `extracted_parameters/enriched/NL.enriched.json` has not been delivered (only FR, IE and LT are present). Writing it now would mean inventing parameter names. The candidates to flag once the export arrives are named in §6.2 and §6.4 — toeslagen amounts fixed by AMvB rather than by the framework act, and any parameter carrying a *combined* tax-plus-premium rate, which no single article states.

Next: `translate run` and `embeddings build` over the NL corpus.
