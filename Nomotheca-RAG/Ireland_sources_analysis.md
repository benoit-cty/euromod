# Harvesting Legislation — Source Strategy (IE pilot)

*Companion to [`11_database-model.md`](11_database-model.md), [`France_sources_analysis.md`](France_sources_analysis.md) and [`Lithuania_sources_analysis.md`](Lithuania_sources_analysis.md). Question: where does the IE fetch skill get legal text from? All findings below were verified hands-on on 2026-08-04 against the live sites and APIs.*

---

## 1. Framing: Ireland is the "no consolidation" case

France ships dated consolidations (LEGI). Lithuania ships dated consolidations (TAR `Suvestinė`). **Ireland ships neither.** This is the single fact that shapes the whole adapter, and it is the reason the IE row in [`fiscal_law_sources.md`](fiscal_law_sources.md) is marked ★★ rather than ★★★.

What Ireland does have is a compensating property that turns out to be *better* for EUROMOD than a consolidation would be: fiscal parameters are set by an **annual pair of acts** whose sections state their own effective date and quote the new value verbatim.

- **Finance Act *YYYY*** — income tax rates/bands/credits and USC, all in Part 1.
- **Social Welfare Act *YYYY*** — PRSI thresholds and every weekly benefit rate (in Schedules).

Verified example, Finance Act 2024 (`2024/act/43`) s. 3, quoted from the live eISB XML:

> **3.** As respects the year of assessment 2025 and subsequent years of assessment, the Principal Act is amended—
> (a) in section 15 … by the substitution of the following Table for the Table to that section: … The first €44,000 — 20 per cent — the standard rate … PART 2 … The first €48,000 … PART 3 … The first €53,000 …
> (b) in section 461 … (iii) in paragraph (c), by the substitution of "€2,000" for "€1,875",
> (c) in section 462B(3), by the substitution of "€1,900" for "€1,750",
> (d) in section 465(1), by the substitution of "€3,800" for "€3,500",
> (e) in section 466(2), by the substitution of "€305" for "€245",
> (f) in section 466A(2), by the substitution of "€1,950" for "€1,800",
> (g) in section 468(2) … "€1,950" for "€1,650" … "€3,900" for "€3,300"

That **single section** carries essentially the entire EUROMOD IE personal-income-tax parameter set for system year 2025, and it matches the Country Report's Budget 2025 list item for item (`08 - EUROMOD Triangulator/country-reports/Y16/IE_Y16.md` §2.2 "Budget 2025"). The same act's s. 2 carries the USC bands (€12,012 / €15,370 / €42,662 / remainder at 0.5 / 2 / 3 / 8 %) and the €25,760 → €27,382 substitution.

Social Welfare Act 2024 (`2024/act/36`) is the same shape for benefits, and states commencement **per section**:

> **4.** (1) Section 49(1) … of the Principal Act is amended … "(ii) €289." (2) This section comes into operation on **6 January 2025**.

So: for Ireland the *evidence* is the annual amending act, not a consolidated code. Point-in-time is reconstructed from each section's own effective-date clause, which the source states explicitly and which parses deterministically.

## 2. Candidate sources, evaluated

### A. **eISB — electronic Irish Statute Book** ✔ the fetch source

`https://www.irishstatutebook.ie` — Office of the Attorney General, official, **ELI implemented**, and — unlike LT's e-tar or IE's own Sodra-equivalent portals — it **serves plain HTTP clients without a 403**. Verified: `curl` with the default ingester User-Agent returns 200 on every URL below. There is no `robots.txt` (404).

| ELI-pattern URL | What it returns | Verified |
|---|---|---|
| `/eli/{year}/act/{no}/enacted/en/xml` | whole act, structured XML | 200, TCA 1997 = 6.4 MB, FA 2024 = 621 KB, SW 2024 = 127 KB |
| `/eli/{year}/act/{no}/enacted/en/html` | whole act, HTML | 200 |
| `/eli/{year}/act/{no}/section/{n}/enacted/en/html` | one section, HTML | 200 |
| `/eli/{year}/act/{no}/section/{n}/enacted/en/xml` | — | **404** — there is no section-level XML |
| `/eli/isbc/{year}_{no}.html` | Legislation Directory: commencement + amendment table | 200, TCA entry = 4.9 MB, "Updated to 27 July 2026" |

**There is no query API** — no search endpoint, no bulk dump, no delta feed. Discovery must come from somewhere else (§B).

**The XML is the right fetch target**: whole-act, one request, structured, and cheap to snapshot. Its shape (verified across all three acts above):

```xml
<act>
  <metadata><title>FINANCE ACT 2024</title><number>43</number><year>2024</year>
            <dateofenactment>20241112</dateofenactment></metadata>
  <frontmatter>… long title, contents …</frontmatter>
  <body>
    <part id="PART1"><title>…</title>
      <chapter><title>…</title>
        <sect id="SEC1"><number>1.</number><title>…</title><p>…</p></sect>
      </chapter>
    </part>
    <schedule id="SCHED1"><title>…</title><table>…</table></schedule>
  </body>
</act>
```

Two dialects, both handled by one parser: newer acts emit `<sect>` with `<number>3.</number>` *before* `<title>`; TCA 1997 emits `<sect id="SEC15">` with `<title>` *before* `<number>15</number>`. Typography rides on self-closing elements rather than Unicode — `<euro/> <pound/> <emdash/> <odq/> <cdq/> <osq/> <csq/>` and the Irish fada set `<afada/> <Afada/> <efada/> <Efada/> <ifada/> <ofada/> <ufada/> <Ufada/>`, plus `<unicode ch="00D7"/>`. **Expanding these is load-bearing, not cosmetic**: drop `<euro/>` and Nomoscope's character-for-character `supporting_extract` check can never match a monetary amount.

Benefit rates live in `<schedule>` `<table>` grids (SW Act 2024 Schedule 1 = 924 `<td>`), so tables must be flattened to a stable, readable text rendering — the adapter emits pipe-delimited rows for exactly the same reason.

### B. **Oireachtas Open Data API** ✔ the resolver

`https://api.oireachtas.ie/v1/legislation` — keyless JSON, no rate limit encountered. This is Ireland's answer to "which act number is the Finance Act of 2025?", the question eISB cannot answer.

```
https://api.oireachtas.ie/v1/legislation?act_year=2025&bill_status=Enacted&limit=200
```

Each result carries `bill.act`: `actNo`, `actYear`, `dateSigned`, `shortTitleEn`, `shortTitleGa`, `longTitleEn`, and — decisively — **`statutebookURI`**, the eISB ELI of the enacted act. Resolve and fetch join on that field. Live results for the EUROMOD window (verified today):

| Year | Finance Act | Social Welfare Act |
|---|---|---|
| 2022 | Finance Act 2022 — `2022/act/44`, signed 2022-12-15 | Social Welfare Act 2022 — `2022/act/43`, signed 2022-12-15 |
| 2023 | Finance (No. 2) Act 2023 — `2023/act/39`, signed 2023-12-18 | Social Welfare (Miscellaneous Provisions) Act 2023 — `2023/act/37` |
| 2024 | Finance Act 2024 — `2024/act/43`, signed 2024-11-12 | Social Welfare Act 2024 — `2024/act/36`, signed 2024-10-28 |
| 2025 | Finance Act 2025 — `2025/act/18`, signed 2025-12-23 | Social Welfare and Automatic Enrolment Retirement Savings System (Amendment) Act 2025 — `2025/act/19` |

Note 2023 and 2025: the fiscal act is **not** always titled plainly "Finance Act *YYYY*" — 2023 has both a `Finance Act 2023` (May, `2023/act/11`, unrelated to Budget 2024) and the Budget act `Finance (No. 2) Act 2023`. Any resolver that string-matches `"Finance Act " + year` silently picks the wrong act. The adapter therefore resolves a **year** to *all* enacted acts whose short title matches the fiscal families and lets the ingest cover them, rather than guessing one.

### C. LRC Revised Acts ⚠ the consolidation corner — and it does *not* cover tax

`https://revisedacts.lawreform.ie` — the Law Reform Commission's administrative consolidations. Reachable by plain HTTP (200), ELI-patterned:
`/eli/{year}/act/{no}/revised/en/html` (whole act), `/eli/{year}/act/{no}/section/{n}/revised/en/html` (one section), `/front/revised/en/html`, and PDF with/without annotations.

**Two findings that correct [`fiscal_law_sources.md`](fiscal_law_sources.md), which claims the Revised Acts include "the two acts that matter most here":**

1. The chronological list (`/revacts/chron`) covers **599 acts** in 3 009 rows. The **Taxes Consolidation Act 1997 is not among them** — the string "Taxes" does not occur on the page at all. There is no free consolidated TCA 1997.
2. The **Social Welfare Consolidation Act 2005 *is*** there (`2005/act/26`, "updated 21 Jan 2026") — but with a **single** row, i.e. the current consolidation only. Acts that do have revision history expose it as extra hidden rows pointing at versioned S3 PDFs (`rev-acts.s3.eu-west-1.amazonaws.com/{year}/{no}/act.pdf?versionId=…`, up to 54 for one act); SWCA 2005 has none. So even where a Revised Act exists, **point-in-time is not offered for the acts we need**.

What the Revised Acts *do* offer, and what makes them the right v2 target, is a **dated amendment trail inline in the HTML**: text carries `F845[…]` markers resolved in an Annotations block —

> F845 Substituted (**1.01.2020**) by Social Welfare (No. 2) Act 2019 (48/2019), s. 8(1)(c)(i), commenced as per subs. (2).

That is machine-extractable provenance per amended fragment. It cannot reconstruct a past text (you cannot un-apply an amendment), but it can date the *current* consolidation honestly and attribute every changed fragment. Deferred to v2 (§7).

### D. eISB Legislation Directory ⚠ the amendment index — real, but expensive to parse

`/eli/isbc/1997_39.html` gives, for an act: per-section commencement ("Ss. 1 - 125 — 30 November 1997 — Commenced on enactment", "S. 284(3A) — 4 September 1998 — S.I. No. 321 of 1998, art. 2") and an "Amendments and other effects" table. It is authoritative and current ("Updated to 27 July 2026"). It is also 4.9 MB of deeply abbreviated citation shorthand (`44/2012, ss. 1(2), 26(12), 51(2)`) with no stable markup contract. Parsing it is a project in itself; it is the principled upgrade path for closing as-enacted validity ranges (§3), not pilot work.

### E. Revenue and DSP — parameter values, cross-check only

- **Revenue Notes for Guidance to the TCA 1997** (`revenue.ie/en/tax-professionals/legislation/notes-for-guidance/taxes-consolidation-act-tca.aspx`) — per-Part PDFs, republished annually "as amended up to and including Finance Act 2025". This is the closest thing to a consolidated TCA that exists publicly, but it is **guidance, not authentic text**. Same hazard class as EUROMOD Country Reports: usable as context, never as the cited evidence for a parameter value.
- **Revenue** rates/credits/bands pages, **DSP SW19** rates booklet, **budget.gov.ie** — fast authoritative statements of applied values, useful as canary cross-checks. `revenue.ie` serves plain clients (200).
- The Triangulator's prior art (`08 - EUROMOD Triangulator/legislation/IE/PENDING.md`) records what actually blocks: `welfare.ie` 503s, `tara.tcd.ie` 403s, several `cso.ie` URLs 404. **Neither irishstatutebook.ie nor revisedacts.lawreform.ie appears in the IE blocked list** — Ireland has no Anubis/Datadome problem. `scrape_IE.py` never touched the Statute Book at all; it scraped `citizensinformation.ie` for benefit descriptions.

### F. Internal asset — Hannes's Ireland JSON DB prototype

Per `fiscal_law_sources.md`, treat as the structured national-team source: the legislative corpus **validates against it**, it does not replace it. Nothing in this adapter consumes it; parameters it covers route through `national_team_source` as usual.

## 3. Recommended design: resolve on the API, fetch on eISB

The FR split (resolve ≠ fetch, different sources) applies here in its pure form — more so than for LT, where one API did both.

**Resolve** — year or citation → exact act ids:
1. `Finance Act 2025`, `Social Welfare Act 2025`, or a bare `2025` → one `Oireachtas` query for that act year;
2. filter `bill.act.shortTitleEn` against the fiscal-act families (`Finance …`, `Social Welfare …`), skipping the non-fiscal decoys (`Finance (State Guarantees …) Act 2024`, `Housing Finance Agency (Amendment) Act 2025`);
3. map each surviving `statutebookURI` to the ingest source id `{year}/act/{no}`.

A direct citation (`TCA 1997`, `Taxes Consolidation Act 1997`, `SWCA 2005`) short-circuits to a curated alias — the same `KNOWN_ACTS` device the LT adapter uses.

**Fetch** — act id → archived authentic content:
- GET `https://www.irishstatutebook.ie/eli/{year}/act/{no}/enacted/en/xml`, store the response verbatim in `fetch_snapshots`;
- record the ELI (`https://www.irishstatutebook.ie/eli/{year}/act/{no}`) on the instrument, `{year}/act/{no}` as `instruments.national_id`;
- parse: one `legal_unit` per `<sect>` and per `<schedule>`, nested under `<part>`/`<chapter>` containers, one `legal_unit_versions` row per section with the validity derived below, `unit_texts` `lang='en'`, `authenticity='authentic'`.

Snapshots of the resolver's API responses are archived too, under their own source (`IE-OIREACHTAS`) — archive-first applies to discovery, not only to text.

### The validity rule — Ireland's `galioja_nuo` substitute

Per section, in priority order, all read from the section's own text:

| Pattern found in the section | `valid_from` | Seen in |
|---|---|---|
| `comes into operation on 6 January 2025` | 2025-01-06 | Social Welfare Acts, per section |
| `As respects the year of assessment 2025 and subsequent years` | 2025-01-01 | Finance Acts, Part 1 |
| `applies for the year of assessment 2025` | 2025-01-01 | Finance Act 2024 s. 2(2) |
| none of the above | `<dateofenactment>` | definitions/interpretation sections |

`valid_to` is `NULL`: an amending provision, once commenced, stays in force. This is not a modelling convenience — it is what the text says.

### The as-enacted trap, and the mechanical guard against it

TCA 1997 s. 15 as enacted states the 1997 bands **in Irish pounds**. Loaded with open-ended validity it would satisfy `validity @> '2025-06-01'` and could outrank Finance Act 2024 s. 3 in retrieval — the FR staleness trap wearing a different hat, and worse, because here the stale text is genuinely authentic and genuinely uncorrected anywhere we can fetch.

Because no source tells us when each TCA section was last amended (§C, §D), the ingester must not *assert* that as-enacted text is in force during the EUROMOD window. The guard is mechanical and lives in the adapter, not in a prompt:

> Acts listed as **`BASELINE_ACTS`** (the principal consolidation acts — TCA 1997, SWCA 2005) are loaded with `version_status = 'unknown'` and validity **closed at the EUROMOD window start, `[commencement, 2022-01-01)`**.

They stay searchable for structure, definitions and cross-references — a proposal can still see what section 15 *is* — but they can never answer a point-in-time query inside the window, and `version_status` says plainly that we are not claiming currency. Everything the window actually needs comes from the annual acts, which do carry in-force statements. When the Legislation Directory parser lands (§7), those closed ranges get replaced by real per-section amendment dates and the flag disappears.

**Freshness canary.** *The latest Finance Act ingested for system year 2025 must contain the substitution of "€44,000" in section 15 and "€2,000" in section 461(c)* — Finance Act 2024 s. 3, cross-checked against IE_Y16 §2.2 "Budget 2025". A corpus that answers the 2025 standard-rate-band question with €42,000 is a stale corpus. Per-year canaries:

| System year | Fact | Source |
|---|---|---|
| 2023 | standard rate band (single) €40,000; personal/employee credit €1,775 | FA 2022, IE_Y16 §2.2 Budget 2023 |
| 2024 | standard rate band (single) €42,000; personal/employee credit €1,875; USC 2 % ceiling €25,760 | F(No. 2)A 2023, Budget 2024 |
| 2025 | standard rate band (single) €44,000; personal/employee credit €2,000; USC 2 % ceiling €27,382, middle rate 4 % → 3.5 % | FA 2024 ss. 2–3, Budget 2025 |

**Ingestion plan for the pilot corpus:**

```sh
cd Nomotheca-RAG/ingest
export EUROMOD_DATABASE_URL=postgresql://jrc:jrc@localhost:5434/legislation

# One command per system year: resolves the year's fiscal acts on the Oireachtas
# API and ingests each one's eISB XML.
for y in 2022 2023 2024 2025; do
  uv run python -m nomotheca_ingest.cli citation ie "$y" "$y-06-01"
done

# The as-enacted baselines (structure + definitions, window-closed, see above)
uv run python -m nomotheca_ingest.cli instrument ie 1997/act/39   # TCA 1997
uv run python -m nomotheca_ingest.cli instrument ie 2005/act/26   # SWCA 2005

# Country Report as context (never evidence)
uv run python -m nomotheca_ingest.cli country-report ie "../../08 - EUROMOD Triangulator/country-reports/Y16/IE_Y16.md"

# Derived rows
uv run --extra embeddings python -m nomotheca_ingest.cli embeddings build \
  --model-path models/bge-m3-openvino --backend openvino --model-id 1 --batch-size 16

# Country report
uv  run  nomoscope-workflow  ingest-params  ../../extracted_parameters/enriched/IE.enriched.json
```

No `translate` step: Ireland's authentic fiscal text is English, so the MT-EN leg is a no-op. Irish-language versions exist on eISB for some acts and are equally authentic constitutionally; they are out of scope for the pilot and would enter as a second `TextIR` with `lang='ga'` (the `fts_ga` config already exists in the schema).

Scale check: 8 annual acts of 0.1–0.6 MB + 2 baselines of 6.4 MB and 1.5 MB ≈ 12 requests. Trivial; no politeness concern beyond the client's single-flight behaviour.

## 4. What transposes from the FR and LT findings

- **The triangle holds, with a different winner again.** Official portal (eISB — *not* blocked, unlike FR/LT, and the fetch corner outright), official API (Oireachtas — discovery/resolve only, no text), community mirror (none needed; the LRC is an official body, and it is the *consolidation* corner rather than a mirror).
- **The canary invariant holds, inverted.** FR's trap was a mirror lying about what is in force. Ireland's trap is the *official* source telling the literal truth about a text that has been amended thirty times since — the as-enacted text is not stale, it is correct-and-superseded. The guard is the same: never let a version assert in-force status the source did not state.
- **The identifier invariant holds.** Every snapshot records the eISB ELI plus `{year}/act/{no}`; the Oireachtas `statutebookURI` is the join key between resolver and fetcher, so a future switch of fetch source re-cites nothing.
- **Language.** English-authentic. Ireland is the project's control case for the multilingual claim — retrieval quality here isolates the RAG from translation quality.
- **`InstrumentIR.title` is `{"en": …}`** with the Irish short title kept in `metadata.short_title_ga` when the API supplies it.

## 5. One consequence of an amendment-based corpus: order by start date

France and Lithuania give one *consolidated* text per point in time, so `validity @> as_of` returns one row. Ireland gives one *amending* provision per budget cycle, none of which is ever repealed — so the same query at 2025-06-01 legitimately returns all of them:

| In force at 2025-06-01 | starts | says |
|---|---|---|
| Finance Act 2022, s. 10 | 2023-01-01 | The first €40,000 \| 20 per cent |
| Finance (No. 2) Act 2023, s. 9 | 2024-01-01 | The first €42,000 \| 20 per cent |
| **Finance Act 2024, s. 3** | **2025-01-01** | **The first €44,000 \| 20 per cent** |

All three statements are true — FA 2022 s. 10 really is still on the statute book. Closing the older ones would assert a repeal that never happened, so the adapter does not. **Consumers must take the row with the greatest `lower(validity)` that is `<= as_of`, not merely the rows matching `validity @> as_of`.** For Ireland that ordering *is* the consolidation step, and it is also a useful property: the two superseded rows are exactly the diff context a proposal needs to justify a change.

## 6. Status (2026-08-04)

The adapter (`countries/ie/`) implements §3 in full: `IeResolver` over the Oireachtas API with a curated alias table, `fetch_ie` against the ELI-pattern URLs of both hosts, and a pure `parse_ie` handling both `<sect>` dialects, Part/Chapter nesting, backmatter schedules, and the full self-closing-entity inventory. `IE-OIREACHTAS` is seeded alongside the existing `IE-EISB` row.

Ingested and verified end-to-end against the local stack — 15 acts, 2 121 units, 2 122 dated versions, 2 611 chunks:

| Act | National id | Units | Chunks |
|---|---|---|---|
| Taxes Consolidation Act 1997 *(baseline)* | `1997/act/39` | 1 136 | 1 358 |
| Social Welfare Consolidation Act 2005 *(baseline)* | `2005/act/26` | 371 | 426 |
| Finance Act 2022 | `2022/act/44` | 107 | 167 |
| Social Welfare Act 2022 | `2022/act/43` | 20 | 22 |
| Finance Act 2023 | `2023/act/11` | 8 | 8 |
| Finance (No. 2) Act 2023 | `2023/act/39` | 103 | 178 |
| Social Welfare (Child Benefit) Act 2023 | `2023/act/13` | 2 | 2 |
| Social Welfare (Miscellaneous Provisions) Act 2023 | `2023/act/37` | 55 | 59 |
| Finance Act 2024 | `2024/act/43` | 120 | 159 |
| Social Welfare Act 2024 | `2024/act/36` | 21 | 23 |
| Social Welfare (Miscellaneous Provisions) Act 2024 | `2024/act/24` | 18 | 23 |
| Social Welfare and Civil Law (Misc. Provisions) Act 2024 | `2024/act/6` | 11 | 11 |
| Finance Act 2025 | `2025/act/18` | 108 | 131 |
| Social Welfare and Automatic Enrolment … Act 2025 | `2025/act/19` | 20 | 22 |
| Social Welfare (Bereaved Partner's Pension …) Act 2025 | `2025/act/8` | 21 | 22 |

Plus the IE_Y16 Country Report as context (`instrument_type='country_report'`, 109 units, excluded from evidence retrieval by construction).

Verified in SQL: no duplicate units, no overlapping versions on any unit, and the 2025 canary answered correctly (`€44,000` band and `€27,382` USC ceiling, both from Finance Act 2024 starting 2025-01-01) while the TCA's as-enacted s. 15 stays outside the window.

Quirks found on the full sweep, all handled in `countries/ie/parser.py`:

- **Two XML dialects.** Newer acts emit `<sect>` with `<number>3.</number>` before `<title>`; the TCA emits `<sect id="SEC15">` with `<title>` first and no trailing dot.
- **Schedules live in `<backmatter>`, not `<body>`** — and they carry the benefit rate tables, so missing them loses every weekly rate.
- **Schedule numbering is inconsistent.** The TCA gives `<schedule id="SCHED1">`; the Finance Acts emit a bare `<schedule>` whose only number is the "SCHEDULE 1" heading. Falling back to a running count silently produced "Schedule 120".
- **The TCA writes headings in `<pc>`, not `<p>`** — treated as inline, "SCHEDULE 2" runs into the schedule title.
- **Commencement is often staggered.** Social Welfare Act 2024 s. 16 commences on 26 December 2024 for jobseeker's benefit and on three later dates for other benefits; the section starts at the earliest and every stated date is kept in `amendment_note.commencement_dates`.
- **Seed collision.** `db/seed.sql`'s IE demo row identified the TCA as `1997/39`, so a real ingest inserted a second instrument and tripped the unique `eli` constraint instead of reconciling. The demo row now uses the adapter's `{year}/act/{no}` identifiers, and its demo version starts at the window boundary so it cannot overlap the as-enacted baseline.

## 7. Open points

1. **LRC Revised Acts as a second fetch source (`IE-LRC`).** SWCA 2005's revised HTML is a genuine current consolidation with a dated, parseable amendment trail (§C). Ingesting it would replace the window-closed as-enacted SWCA baseline with a real in-force text — the single highest-value follow-up. Blocked on nothing but parser work.
2. **eISB Legislation Directory parser (§D).** Would give real per-section commencement and amendment dates for TCA 1997, removing the `BASELINE_ACTS` window-closing device entirely.
3. **Statutory Instruments.** Several IE parameters (rent limits, some disregards) move by S.I. rather than by act. eISB serves them at `/eli/{year}/si/{no}/made/en/html`; the same fetcher pattern extends, but the Oireachtas API does not index S.I.s — discovery would need the eISB S.I. year lists.
4. **Irish-language texts.** Constitutionally the Irish text prevails on conflict. Ingesting `ga` alongside `en` is cheap (`fts_ga` exists) and would make IE a second dual-authentic case next to BE.
5. **Revenue Notes for Guidance.** Worth ingesting as a Country-Report-class context corpus (`instrument_type` outside the evidence set) rather than as legislation? It is the only per-section consolidated view of the TCA in existence publicly.
6. **Finance Act naming.** The `Finance (No. 2) Act 2023` case shows the fiscal act of a budget cycle is not identifiable by title alone. A more robust rule would read `longTitleEn` for the charging language, or cross-check `dateSigned` against the budget calendar.
