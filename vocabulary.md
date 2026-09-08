# Vocabulary — Nómos / EUROMOD assisted parameter update

A glossary for this repository: the words used in the code, the docs and the UI, with a
pointer to where each one is actually implemented. Terms come from four different worlds
that meet here — **EU legal informatics** (ELI, consolidation, hierarchy of norms),
**national legal data sources** (Légifrance, DILA, Tricoteuses, TAR, eISB), **EUROMOD**
(system year, `def_const`, spine) and **RAG / agentic pipelines** (chunk, hybrid retrieval,
frame, scout, critique).

The last section — [What the confidence score really means](#10-what-the-confidence-score-really-means) —
is the one to read before trusting any number shown in the validation UI.

---

## Contents

1. [Project codenames and activities](#1-project-codenames-and-activities)
2. [The workflow steps](#2-the-workflow-steps-frame--retrieve--propose--critique--diff--enqueue)
3. [Scout — the gap-filler](#3-scout--the-gap-filler)
4. [Levels of law](#4-levels-of-law)
5. [Identifiers: ELI, national ids, `rag://`, `euromod://`](#5-identifiers-eli-national-ids-rag-euromod)
6. [Legal data sources per country](#6-legal-data-sources-per-country)
7. [OpenFisca](#7-openfisca)
8. [EUROMOD vocabulary](#8-euromod-vocabulary)
9. [RAG and retrieval vocabulary](#9-rag-and-retrieval-vocabulary)
10. [What the confidence score really means](#10-what-the-confidence-score-really-means)
11. [Routing, verdicts and statuses — the terms a reviewer sees](#11-routing-verdicts-and-statuses--the-terms-a-reviewer-sees)

---

## 1. Project codenames and activities

| Term | Meaning |
|---|---|
| **Nómos** | Codename of the whole project (Greek *νόμος*, "law"). |
| **Nomotheca** | The legislation store + ingester ("library of laws"). Directory [Nomotheca-RAG/](Nomotheca-RAG/), Python package `nomotheca_ingest`. Implements **Activity 2**. |
| **Nomosync** | The ingestion side of Nomotheca (fetch → snapshot → parse → chunk → load). |
| **Nomoscope** | The agentic workflow + validation UI ("looking at the law"). Directory [Nomoscope-agentic-workflow/](Nomoscope-agentic-workflow/), package `nomoscope_workflow`. Implements **Activity 3**. |
| **Nomokrisis** | The evaluation pipeline ("judgement of the law"). Directory [Nomokrisis-evaluation_pipeline/](Nomokrisis-evaluation_pipeline/), package `nomokrisis_eval`. Implements **Activity 4**. |
| **Activity 1–5** | The five contractual deliverables ([00_project-overview.md](00_project-overview.md)): 1 parameter format, 2 RAG architecture, 3 agentic workflow, 4 validation, 5 technical report. |
| **Triangulator** | An earlier prototype kept for harvesting, [08 - EUROMOD Triangulator/](08%20-%20EUROMOD%20Triangulator/). "Triangulation" there = cross-checking a parameter across **three** sources: the EUROMOD XML, the Country Report and the national legislation. |

The three packages depend on each other in a line — **ingest → agentic workflow → evaluation** —
and all read/write one shared Postgres.

---

## 2. The workflow steps: frame → retrieve → propose → critique → diff → enqueue

One run = one `(country, parameter, system year)` triple. The pipeline is a plain function,
not a free-roaming agent: only **propose** and **critique** call an LLM, everything else is
SQL and pure functions ([pipeline.py](Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/pipeline.py)).

### frame
Turns a parameter into a **search query**. The parameter itself is a cryptic EUROMOD id
(`$tin_upthres1`) with labels and a description; framing:

- picks the **law's language** rather than English (French law is searched in French — the
  full-text-search leg is language-specific), pulling native labels from `params.parameter_texts`;
- enriches the query with **Country Report terms**: the CR section headings translate EUROMOD
  acronyms into the official national name of the benefit or tax (`tinto01_s` →
  *"Contribution différentielle sur les hauts revenus"*);
- collects the **citations already recorded** on the previous value — these feed the citation
  fast path in retrieval.

"Framing" is therefore the step that converts *model vocabulary* into *legal vocabulary*.
It is also the step where most `not_found` failures are actually born.

### retrieve
Deterministic SQL. Three legs, merged: an exact **citation fast path** (trigram match on
`legal_units.citation`), **FTS** (Postgres `tsvector` in the law's language) and **vector**
search (BGE-M3 embeddings). Point-in-time is a `WHERE validity @> as_of` filter.

### propose
The first LLM call (PydanticAI structured output → `ProposalDraft`). It must return the value
**plus** a `citation_chunk_id` and a `supporting_extract` quoted **verbatim** from that chunk.

### critique
Mechanical checks first, LLM second:

- **the verbatim check** — `supporting_extract` is searched character-for-character inside the
  cited chunk in the database ([`retrieval.verify_extract`](Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/retrieval.py)).
  No match → fail. This is the anti-hallucination guarantee, and it is code, not a prompt;
- date consistency (with a special branch for `income_year` parameters, below);
- value sanity (rates within [0,1] for unit `/1`, ascending bracket thresholds, magnitude);
- then a sceptical LLM pass restricted to exactly three booleans.

One retry is allowed, with the failed critique's issues fed back into the second proposal.

### diff
Compares the proposed value with the current one (float tolerance, bracket-by-bracket) and
assigns the **routing** (`unchanged` / `changed` / `new` / `not_found` / …, see §11).

### enqueue
Writes a `ReviewItem` JSON into `data/queue/`. Nothing is written into EUROMOD files —
the pipeline is **export-first and human-gated**. Reviewed items are immutable to re-runs
unless `--force`; decisions are appended to `params.review_decisions` in the database.

---

## 3. Scout — the gap-filler

**Scout** is what runs when retrieval finds nothing usable ([scout.py](Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/scout.py)).
The usual cause of a `not_found` is not a bad LLM but a **missing instrument** in the corpus —
e.g. the French *plafond de la sécurité sociale* is fixed each year by an *arrêté* that no
*loi de finances* contains.

The scout closes that gap without weakening the evidence rules:

1. an LLM (mode `llm`) and optionally a **web search restricted to official domains**
   (mode `tavily`, e.g. `legifrance.gouv.fr`, `e-seimas.lrs.lt`) **discover an identifier** —
   `JORFTEXT…`, `LEGIARTI…`, a TAR document id;
2. that identifier is handed to Nomotheca's normal archive-first ingest (fetch → snapshot →
   parse → chunk), then embedded;
3. retrieval runs again against the database.

**Web text is never evidence.** The scout discovers *what to ingest*; the text always enters
through the ingester and is still subject to the verbatim-quote check. Modes are set with
`WORKFLOW_SCOUT` (`off` | `llm` | `tavily`). What the scout did is recorded on the review item
(`ReviewItem.scout`) so a reviewer can see the corpus was extended by that run.

---

## 4. Levels of law

"Level" is used in three different senses in this repo. They are worth keeping apart.

### 4.1 Hierarchy of norms (which text is legally superior)

The classical pyramid, in the words each country uses:

| Level | France | Lithuania | Ireland |
|---|---|---|---|
| Statute (parliament) | *loi* — incl. the annual *loi de finances* (LF) and *loi de financement de la sécurité sociale* (LFSS) | *įstatymas* | Act (e.g. Finance Act) |
| Government regulation | *décret* | *Vyriausybės nutarimas* | Statutory Instrument (SI) |
| Ministerial order | *arrêté* | *ministro įsakymas* | Ministerial regulation |
| Administrative guidance | *circulaire*, BOFiP | official commentary | Revenue guidance |

This matters practically, not theoretically: **many EUROMOD values are not in the statute**.
The statute defines the concept and delegates the number to an annual *arrêté* / *nutarimas* /
SI. That is why the scout's per-country configuration lists exactly these act kinds.

### 4.2 Codified vs. amending text (the consolidation level)

A *loi de finances* is mostly an **amending** text: its articles rewrite articles of the CGI,
CSS, etc. What a parameter should cite — and what point-in-time retrieval serves — is the
**consolidated code article as in force on a date** (CGI art. 197, version of 2025-01-01),
not the LF article that produced it. Hence two ingestion targets, mapping onto the two French
*fonds* (see §6): **JORF** = the act as published (authentic, frozen); **LEGI** = the
consolidated dated versions.

### 4.3 Structural levels in the database

The five nested levels of [Nomotheca-RAG/db/schema.sql](Nomotheca-RAG/db/schema.sql):

```
instrument            a law / code / act as a citable whole      ("Code général des impôts")
 └─ legal_unit        a timeless structural slot                 ("CGI, art. 197")
     └─ legal_unit_version   one consolidated state + validity daterange   ← the temporal truth
         └─ unit_text        one language rendering (authentic / official / machine translation)
             └─ chunk        the retrieval grain AND the citable target
```

Key rules encoded there:

- **point-in-time = `WHERE validity @> :as_of`**. Amendment relations (`instrument_relations`)
  are metadata for provenance and discovery; they never drive point-in-time answers.
- a renumbered article is a **new** `legal_units` row, never a mutated one;
- an exclusion constraint forbids two overlapping versions of the same unit — closing the old
  version and inserting the new one happen in the same transaction;
- `chunks.id` is the **`jrc_database_id`** a parameter citation carries, with character offsets
  into `unit_texts.content`, which is what makes the verbatim check mechanical.

### 4.4 Source-trust levels (which text may be used as evidence)

Inherited from the Triangulator prototype's rule *"Legislation is King"*:

| Class | Role here |
|---|---|
| National legislation | **Evidence.** The only thing `propose` / `critique` may cite. |
| Country Report (EUROMOD) | **Context, never evidence.** Ingested as `instrument_type='country_report'`, excluded from evidence retrieval SQL; readable only through `retrieval.country_report_search()` (query framing, UI display). Citing it would be circular — the CR describes the model, not the law. |
| Administrative guidance (circulars, BOFiP doctrine) | **Evidence, labelled.** Added by a reviewer as a *contributed document*; the instrument carries `source_trust_class='guidance'`, each citation carries the class, and the critique records a "supported by guidance only" finding. Ranked equal to legislation in retrieval. See [ADR-0001](docs/adr/0001-guidance-is-citable-evidence-with-a-visible-class.md). |
| Statistics, press | Not ingested. |
| Web search results | Never evidence — discovery only (§3). |

---

## 5. Identifiers: ELI, national ids, `rag://`, `euromod://`

**ELI — European Legislation Identifier.** An EU-wide convention (Council conclusions
2012/C 325/02) for giving every legal act a stable, structured HTTP URI, so that acts can be
cited and linked across member states. Example:

```
https://www.legifrance.gouv.fr/eli/loi/2025/2/14/ECOX2423405L/jo/texte
```

Three things to know when reading this repo:

- **Deployment is uneven.** `sources.supports_eli` is a per-source boolean; Ireland's eISB mints
  clean ELIs (`.../eli/1997/act/39/section/15`), France exposes an `ELI_ALIAS` in the DILA
  metadata, Belgium's Justel has only partial ELI.
- **Three ELI columns exist**, at three levels: `instruments.eli` (the act),
  `legal_units.eli` (the article), `legal_unit_versions.eli_version` (that article *at a date*,
  when the source mints a versioned ELI).
- ELI is a *citation* identity, not the internal key. Internally everything is a UUID.

**National ids** — the identifier the national system actually keys on, stored in
`instruments.national_id` / `legal_units.national_id` / `legal_unit_versions.source_version_id`:
`JORFTEXT000051168007` (a French act as published), `LEGIARTI000051212954` (one consolidated
version of one article), `LEGITEXT…` (a whole code), `NOR` (the French inter-ministerial
reference), `TAR.xxxxxxxxxxxx` or a 32-hex id (Lithuania), `1997/act/39` (Ireland), `numac`
(Belgium), `BOE-A-…` (Spain).

**`rag://` URIs** — the contract between the parameter JSON (which lives in git, outside the
legislation DB) and the database, resolved by the SQL function `resolve_rag_uri()`:

```
rag://chunk/{uuid}              exact chunk
rag://version/{uuid}            a specific consolidated version
rag://unit/{uuid}               unit, version in force today
rag://unit/{uuid}@2025-06-01    unit, version in force at that date
```

**`euromod://` URIs** — the identity of a parameter on the model side:

```
euromod://FR/tinkt_fr/def_const/$tin_upthres1
        country / policy / function / parameter
```

---

## 6. Legal data sources per country

### France

| Term | What it is |
|---|---|
| **Légifrance** | The official French legal portal (legifrance.gouv.fr) — the canonical *human* URL for a citation. Protected by DataDome anti-bot; scraping it is inappropriate and fragile, so it is used as the citation URL and for manual spot-checks, not as a fetch source. The one exception is *resolution*: an ELI-form URL is followed to its `/jorf/id/JORFTEXT…` redirect (headless browser as fallback) to obtain the DILA id, and nothing else is read. See [ADR-0002](docs/adr/0002-legifrance-eli-urls-resolve-through-a-browser-fallback.md). |
| **DILA** | *Direction de l'information légale et administrative* — the public body that publishes Légifrance and, crucially, the **open-data dumps** (`echanges.dila.gouv.fr`): full + daily incremental `tar.gz` of the LEGI and JORF XML. Authoritative, no auth, but consuming it means rebuilding a stock+delta pipeline. |
| **JORF** | *Journal officiel de la République française* — the *fonds* of acts **as published** (authentic, frozen). Ids `JORFTEXT…`. |
| **LEGI** | The *fonds* of **consolidated, dated** versions of codes and articles. Ids `LEGITEXT…` (code), `LEGIARTI…` (article version). This is where point-in-time retrieval lands. |
| **Tricoteuses** | A community project ([tricoteuses.fr](https://tricoteuses.fr/), named after the *tricoteuses* of the French Revolution) that converts the DILA dumps into **per-document JSON files in git**, updated daily, fusing LEGI + JORF. This is what the FR adapter actually fetches from: `git.tricoteuses.fr/dila/donnees_juridiques`, path scheme `{FOND}/{TYPE}/` + the id's digits 9–16 in pairs. Advantages: no anti-bot, id-addressable, and a git commit SHA makes a perfect reproducibility marker. See [France_sources_analysis.md](Nomotheca-RAG/France_sources_analysis.md). |
| **Moulineuse** | The Tricoteuses PostgreSQL database (schemas `legifrance`, `assemblee`, `senat`, …) and its MCP server at `mcp.code4code.eu`. Used as a **resolver** ("which `LEGIARTI` is CGI art. 197 on this date?"), not as the text source. A local dump can serve the same role offline. |
| **Canutes** | A sister community API built on the same DILA data (named after the Lyon silk workers), noted in [fiscal_law_sources.md](Nomotheca-RAG/fiscal_law_sources.md) alongside Tricoteuses; prior experience there includes Anubis anti-bot blocking. |
| **PISTE** | The French state API platform (AIFE) hosting the **official Légifrance API** (OAuth2, point-in-time capable: `/consult/getArticle`, `/consult/legiPart`…). The decided long-term fetch source for an institutional JRC deployment; the FR fetcher interface is deliberately shaped like it so the swap touches one file. |

The FR design splits **resolve** (citation → version id, via Moulineuse/MCP) from **fetch**
(version id → raw JSON, via Tricoteuses) precisely so each half can be replaced independently.

### Other pilot countries

| Country | Source | Notes |
|---|---|---|
| **Ireland** | **eISB** (Irish Statute Book) + the **Oireachtas** Open Data API | eISB serves whole-act XML at ELI-pattern URLs but has no query API; the Oireachtas API is used as a *resolver only* (act year/title → act number + `statutebookURI`). |
| **Lithuania** | **TAR** (*Teisės aktų registras*), portals `e-seimas.lrs.lt` / `e-tar.lt`, Spinta open-data API | The official API wins outright — no community mirror needed. `/asr` is the index of dated **consolidations** (the value history); a bare id fetches only the act as published. |
| **Belgium** | **Justel / Moniteur belge** | `numac` identifiers, partial ELI, and two *authentic* language versions (fr + nl [+ de]) — which is why `unit_texts` allows several rows with `authenticity='authentic'`. |
| **Spain** | **BOE** | Ids `BOE-A-…`; the strongest machine-readable access of the six; adds a regional dimension. |
| **Netherlands** | **wetten.overheid.nl** / BWB, Juriconnect refs | Ids `BWBR…`. |

---

## 7. OpenFisca

**OpenFisca** is an open-source framework for writing tax-and-benefit rules as code. Each
country package (e.g. `openfisca-france`, and PolicyEngine forks of it) ships a
`parameters/**.yaml` tree where every parameter is a **dated time series** with legal
references:

```yaml
# parameters/impot_revenu/bareme_ir_depuis_1945/bareme/…
values:
  2024-01-01:
    value: 0.11
metadata:
  reference:
    2024-01-01: https://www.legifrance.gouv.fr/…/LEGIARTI000048841464
```

In this repo it plays **three** roles ([openfisca.py](Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/openfisca.py),
[Param_Schema/openfisca_france_usage.md](Param_Schema/openfisca_france_usage.md)):

1. **A second, independent corpus of values** — ingested into `params.external_*` under its own
   dotted-path identity, with the `LEGIARTI`/`JORFTEXT` ids parsed out of its reference URLs.
   Those ids are ready-made ingestion targets for Nomotheca.
2. **A cross-check / triangulation source** — an OpenFisca value that agrees with the pipeline's
   proposal for the same date is strong corroboration; a disagreement is a good eval case.
3. **A source of native-language search text** — its French parameter descriptions help the
   frame step.

Two conventions worth knowing because the pipeline mirrors them: OpenFisca stores bracket
scales as bands, which are **flattened** here to one series per component
(`brackets[2].rate`, `brackets[2].threshold`) — exactly the grain of EUROMOD scalar constants;
and OpenFisca **back-dates** an income-tax value to the start of the income year, which is the
convention `temporal_basis: income_year` reproduces (§8).

Note: no EUROMOD ↔ OpenFisca mapping is attempted automatically. `params.parameter_links` is a
separate, human-validated step — the two models name things differently and disagree about
what is "one parameter".

---

## 8. EUROMOD vocabulary

| Term | Meaning |
|---|---|
| **EUROMOD** | The EU-wide tax-benefit microsimulation model maintained by JRC.B.2 — the consumer of everything here. |
| **System / system year** | EUROMOD ships one system per country per year (`FR_2025`). One workflow run verifies exactly **one** system year (`--year 2025`). |
| **Policy** | A block of the model's spine (`tin_fr` = income tax, `tscse_fr` = employee social contributions, `bch00_fr` = child benefit). |
| **`def_const`** | The "define constants" function of a policy — where the numeric constants live. ~700 exported `def_const` constants form the parameter corpus of the pilot. |
| **`model_target`** | The `euromod://COUNTRY/policy/function/$param` URI identifying one parameter (§5). |
| **`spine_order`** | The position of the parameter's policy in EUROMOD's ordered execution spine — ordering information carried through from the export. |
| **Country Report (CR)** | The annual, per-country prose documentation of what the model implements. **Context, never evidence** (§4.4), but the best acronym → national-name dictionary available; it drives the frame step's enrichment. |
| **`as_of` / reference date** | The date used to select in-force law. `--as-of` is a deprecated alias for `--year`. |
| **`temporal_basis`** | `in_force` (default) or `income_year`. |
| **`income_year`** | The FR income-tax family: the EUROMOD system year *is* the income year, but the enacting *loi de finances* is voted at the end of that year or in the next one, and applies retroactively. So retrieval looks a year ahead (1 July of `year+1`), proposals **back-date** `valid_from` to 1 January of the income year, and the critique's budget-act-window check catches a version too old to be that year's value. The flag is **curated** (in the parameter JSON), never derived from the export. |
| **`provisional`** | Routing for an `income_year` parameter whose enacting act is not in the corpus yet: there *is* a best-available value, but it cannot be confirmed for year Y. Accept is blocked in the UI. Distinct from `not_found` — this is a normal state of the world, not a failure. |
| **`national_team_source`** | Parameters that are not legislation-derivable (national-team estimates, imputations). They route around the pipeline and are **never overwritten**. |
| **`derived`** | Parameters whose value is a formula over others (`$PSS * 4`, ~75 % of FR params are formula strings). Legislation never states them directly, so the **anchor** parameter is what gets updated. |
| **Readiness** | A pre-run corpus check ([readiness.py](Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/readiness.py)): are the two finance-act vintages for year Y ingested *and embedded*? Printed once as a banner instead of surfacing as N critique failures. |
| **Weighted average / period suffixes** | EUROMOD encodes a mid-year change as a weighted annual average, and carries period suffixes (`#m`, `#y`, …). Value comparison must **normalise to an annualised value**, never string-match. |
| **99999999999** | An instrumental EUROMOD value meaning *infinity*; must be excluded from value comparisons. |
| **The June 30th rule** | A EUROMOD policy year reflects the law as of **30 June**, not 1 January — which is why `as_of` dates in the queue are mid-year (`2025-07-01`). |

---

## 9. RAG and retrieval vocabulary

| Term | Meaning |
|---|---|
| **RAG** | Retrieval-Augmented Generation. Here it is a **lazy, agent-populated** RAG: the corpus is not crawled upfront, it grows as parameters need it (see [10_retrieval-strategy-challenge.md](Nomotheca-RAG/10_retrieval-strategy-challenge.md)). |
| **Archive-first** | Nothing is parsed before the raw payload is snapshotted with its sha256 into `fetch_snapshots`. No text exists in the DB without an origin row — `legal_unit_versions.fetch_snapshot_id` is `NOT NULL`. |
| **Chunk** | The retrieval grain and the citable target. `seq = 0` is the whole unit; large units split into `seq 1..n` with character offsets into `unit_texts.content`. |
| **`context_header`** | The breadcrumb prefixed to a chunk for search and display: *"Code général des impôts > Art. 197 (vig. 2024-01-01)"*. It is indexed with higher weight (`setweight(…, 'A')`) than the body. |
| **FTS** | Postgres full-text search over `tsvector`, with a **per-language configuration** (`fts_fr`, `fts_lt`, …) combining a stemmer with `unaccent`. Lithuanian and Irish have no built-in stemmer and fall back to `simple`. |
| **BGE-M3** | The multilingual embedding model used for the vector leg (1024 dimensions), run locally via **OpenVINO** (preferred on the Intel Ultra 7 target) or torch. Its `fix_mistral_regex` flag is a known breakage — leave it off. |
| **`halfvec`** | pgvector's fp16 vector type: half the storage, negligible recall loss. Indexed with **HNSW**. |
| **Hybrid search / RRF** | The two legs, full text search and embeddings vector proximity, are merged with **Reciprocal Rank Fusion**: `1/(60+rank_fts) + 1/(60+rank_vector)`, plus a guaranteed bonus for the vector top-3 (because `ts_rank_cd` has no IDF, common fiscal terms let long amending acts crowd the FTS leg). |
| **Citation fast path** | Before any search: a trigram match of the previously-recorded citation against `legal_units.citation`. If a parameter already cites CGI art. 197, go straight there. |
| **`method`** on a hit | How a chunk reached the trace: `citation`, `fts`, `vector`, `hybrid`, `country_report`, or **`sibling`** — not retrieved by search at all, but pulled in because it is another chunk of an already-retrieved article (needed when a value and its applicability clause sit in different chunks of the same article). |
| **`score`** on a hit | The **RRF fusion score** — an unbounded, run-relative pseudo-rank. It is not a probability and not comparable across runs. Do not read it as confidence (§10). |
| **`recall@k` / `retrieval_hit`** | Eval KPI: did the ground-truth citation appear anywhere in the retrieval trace? Distinguishes "retrieval missed it" from "the model misread it". |
| **PydanticAI** | The library used for the two LLM calls; the model is forced to return a validated Pydantic object (`ProposalDraft`, `CritiqueFindings`) rather than free text. |
| **Provider-prefixed model string** | Every model is named `provider/model` — `anthropic/…`, `openai/…`, `azure_openai/…`, `openrouter/…`, `together/…`, plus `mock/…` for key-less demos and deterministic tests. Nothing in the pipeline knows the provider: multi-provider support is a contractual requirement (Activity 5 compares LLMs). |
| **Phoenix** | Arize Phoenix, the OTLP trace viewer at `localhost:6006`. Every run is one trace; `ReviewItem.phoenix_trace_id` links a queue item to it. Mock runs trace identically to real ones. |
| **EcoLogits** | The methodology used to estimate the environmental impact of LLM calls, computed offline from Phoenix token counts ([impact.py](Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/impact.py)). |

---

## 10. What the confidence score really means

Short answer: **it is the LLM's own self-report, on an anchor supplied by our prompt. It is
not a probability, it is not calibrated, and nothing in the system uses it to make a
decision.** Read it as a weak triage hint, never as a measure of correctness.

### Where it comes from

One field on the proposal model, filled by the model itself:

```python
# schema.py — ProposalDraft
confidence: float = 0.0
```

and one line of the proposal prompt tells it how to fill it
([prompts.py:53](Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/prompts.py#L53)):

> `confidence in [0,1]: 0.9+ only when the extract states the value explicitly and unambiguously.`

That is the entire specification. There is no logprob, no ensemble, no agreement measure,
no calibration set behind it. In mock runs it is simply hard-coded — 0.9 for a bracket
schedule, 0.75 for the scalar-rate heuristic — which is a fair summary of how much
information it carries.

### Where it goes

It is copied verbatim from the draft onto the value's lineage
([pipeline.py:714](Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/pipeline.py#L714)),
then displayed in the queue list, the detail panel and the audit log of the UI, and recorded
as a column on eval results. **That is all it does.** Grep confirms there is no threshold
anywhere: it never gates routing, never influences the critique verdict, never blocks or
enables Accept, and is never used in scoring.

### What the data actually looks like

Across the 36 queue items that carry a confidence value:

| Model | Confidence | Items |
|---|---|---|
| `azure_openai/gpt-5.4-nano` | **0.90** | 22 |
| `azure_openai/gpt-5.4-nano` | 0.86 | 2 |
| `azure_openai/gpt-5.4-nano` | 0.95 | 1 |
| `azure_openai/gpt-5.4-nano` | 0.55 | 1 |
| `azure_openai/gpt-5.6-luna` | 0.90 / 0.94 / 0.97 | 4 |
| `mock/extractor` | 0.90 / 0.75 | 6 |

Two things follow. First, **the distribution is a spike on the number written in the prompt**:
28 of 36 values are exactly 0.9, 22 of them from a single real model. The score is measuring
our prompt's anchor far more than the model's epistemic state. Second, **high confidence and a
failed critique coexist happily**: of those same 36 items, 23 carry a critique verdict of
`fail` — including items at 0.90. A confident proposal whose quote is not in the cited chunk
is still rejected, and rightly so.

### What to trust instead

The signals that are mechanical, and therefore meaningful:

| Signal | Why it is trustworthy |
|---|---|
| `critique.citation_verified` | The extract was found **character-for-character** in the cited chunk, by SQL. This is the anti-hallucination guarantee. |
| `critique.verdict` (`pass`/`fail`) and `issues` | The merge of the mechanical checks with the sceptical LLM pass; issues name the concrete error. |
| `routing` | Says what kind of answer this is (`changed`, `not_found`, `provisional`, `derived` …) — far more actionable than a number. |
| `retrieval_trace` | Shows *what the model was allowed to see*. A `not_found` with an empty or off-topic trace is a corpus problem, not a model problem. |
| Readiness banner / `provisional` | Says up front that the enacting act is not in the corpus yet. |
| `legal_status` | The **law's** lifecycle (`enacted_in_force`, `bill_proposed`, …). Deliberately kept distinct from confidence — [01_activity1_parameter-format.md](Param_Schema/01_activity1_parameter-format.md) states the separation explicitly: *law lifecycle vs. extraction reliability*. |

### Terms confidence is easily confused with

- **retrieval `score`** — the RRF fusion score of a chunk (§9). Different object, different
  scale, also not a probability.
- **`legal_status`** — a property of the legislation, not of the extraction.
- **eval KPIs** (`value_correct`, `citation_correct`, `supportedness`, `hallucination`,
  `retrieval_hit`) — these *are* measures of correctness, computed deterministically against a
  golden set with **no LLM judge**. They are the honest answer to "how much can I trust this
  pipeline"; confidence is not.

### How to use it anyway

It is not worthless, but its useful signal is one-sided:

- **A low value is informative.** 0.55 means the model itself flagged an ambiguity — worth a
  closer look, and worth reading `reasoning` and the extract.
- **A high value is not informative.** 0.9 is the default the prompt invites; it says nothing
  beyond "the model did not flag a doubt".
- Sort by it only as a *tie-break within the same routing and verdict*, never as a review
  priority on its own, and never as an auto-accept criterion. The workflow is human-gated by
  design; confidence is one of the weakest inputs to that human decision.

If a calibrated number is ever needed, it has to be **built**, not asked for: agreement across
independent runs or models, retrieval-rank features, and the eval pipeline's per-slice accuracy
are the raw material. That work does not exist today, and the field should be read accordingly.

---

## 11. Routing, verdicts and statuses — the terms a reviewer sees

**`routing`** — what kind of answer the run produced:

| Value | Meaning |
|---|---|
| `unchanged` | A value was found and it matches the current one. |
| `changed` | A value was found and it differs — the most valuable outcome. |
| `new` | No current value existed. |
| `not_found` | No extract stated a value for this concept on the reference date. **Usually a corpus problem**, not an LLM problem: the act is not ingested, or ingested but not yet embedded. |
| `national_team_source` | Not legislation-derivable; routed around the pipeline, never overwritten. |
| `derived` | The value is a formula over other parameters (`derived_from` lists them); the anchor is what needs updating. |
| `provisional` | `income_year` parameter whose enacting act is not in the corpus yet. Accept is blocked in the UI. |

**`critique.verdict`** — `pass` / `fail`, from the merged mechanical + LLM checks
(`schema_valid`, `citation_verified`, `dates_consistent`, `values_sane`).

**`status`** (the human decision, `ItemStatus`) — `pending`, `accepted`, `rejected`, `edited`,
`escalated`. Written to the append-only `params.review_decisions` table (with
`data/decisions.jsonl` as a local write-ahead mirror); that log is itself future
training and validation data.

**`legal_status`** (the law's lifecycle, on a value) — `enacted_in_force`,
`enacted_not_yet_in_force`, `adopted_pending_publication`, `bill_proposed`, `announced`,
`national_team_estimate`.

**`source_type`** — `legislation`, `national_team`, `administrative_guidance`,
`official_statistics`, `parliamentary_bill`, `government_announcement`, `other`.

**`authenticity`** (on a text) — `authentic` (the original-language legal text),
`official_translation`, `machine_translation`. Belgium legitimately has two `authentic` rows;
machine translations are ordinary rows flagged as derived, carrying `mt_engine` and
`source_lang`.

---

### Where to look next

- Contract and activities: [00_project-overview.md](00_project-overview.md)
- Database model: [Nomotheca-RAG/11_database-model.md](Nomotheca-RAG/11_database-model.md), [Nomotheca-RAG/db/schema.sql](Nomotheca-RAG/db/schema.sql)
- Ingestion (shared vs. adapter boundary): [Nomotheca-RAG/12_ingestion-architecture.md](Nomotheca-RAG/12_ingestion-architecture.md)
- Why a lazy RAG: [Nomotheca-RAG/10_retrieval-strategy-challenge.md](Nomotheca-RAG/10_retrieval-strategy-challenge.md)
- Parameter format: [Param_Schema/01_activity1_parameter-format.md](Param_Schema/01_activity1_parameter-format.md), [Param_Schema/parameter_sample.jsonc](Param_Schema/parameter_sample.jsonc)
- What value scoring can and cannot do: [Nomokrisis-evaluation_pipeline/README.md](Nomokrisis-evaluation_pipeline/README.md)
