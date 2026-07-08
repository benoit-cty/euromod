# Fiscal Law Sources — Pilot Countries (FR, NL, LT, ES, IE, BE)

**Purpose:** Reference catalogue of authoritative legal sources for the EUROMOD parameter update pipeline. For each country: the official consolidated legislation source, machine-readable access (crawler/RAG ingestion path), the tax/benefit administrative sources where parameter values actually live, and the key acts covering personal income tax and social benefits.

**Status:** Draft for team review — machine-access details verified July 2026 where flagged; items marked ⚠️ need confirmation.

---

## Cross-cutting notes

- **Statutory vs. administrative sources.** In every country the *legal basis* (acts, codes) and the *operational parameter values* (rates tables, indexed amounts, administrative guidance) live in different places. The pipeline needs both: the legislation source for provenance and `legal_status`, the administrative source for the actual numbers — especially where amounts are auto-indexed (BE, NL, LT) rather than re-legislated.
- **ELI (European Legislation Identifier)** is implemented, at least partially, in FR, ES, IE, and BE — usable as a stable identifier scheme in the parameter schema's provenance fields. NL uses its own BWB identifiers (BWBR…); LT uses TAR document identifiers.
- **EUROMOD Country Reports** (JRC/ISER, per country per year) remain the best bridge documentation: they map each policy/function to its legal basis and are the natural validation reference for extracted parameters.
- **EU level:** EUR-Lex via the Publications Office **Cellar SPARQL endpoint** (CELEX identifiers) for directives/regulations where relevant. Rarely the source of fiscal parameters themselves, but useful for cross-references.

---

## France 🇫🇷

### Primary legislation (consolidated)
- **Légifrance** — https://www.legifrance.gouv.fr — official consolidated codes and laws, maintained by DILA. Point-in-time versions available per article ("versions" with effective-date ranges — maps directly onto per-provision validity dates).
- Key codes/acts:
  - **Code général des impôts (CGI)** + annexes I–IV — PIT (IR), rates, quotient familial, décote, CEHR/CDHR
  - **Livre des procédures fiscales (LPF)**
  - **Code de la sécurité sociale (CSS)** — contributions, CSG/CRDS, family benefits, minimum pensions
  - **Code de l'action sociale et des familles (CASF)** — RSA, prime d'activité
  - Annual **Loi de finances** and **LFSS** — where most parameter changes originate

### Machine-readable access
- **DILA open data**: full **LEGI** (consolidated legislation), **JORF** (official journal), **KALI** datasets as XML bulk dumps — https://echanges.dila.gouv.fr / mirrored on data.gouv.fr. Free, no registration. Best option for building a local corpus.
- **Légifrance API via PISTE** — https://piste.gouv.fr — REST API over Légifrance (free registration, OAuth). Suited to targeted/lazy retrieval rather than bulk.
- **Tricoteuses / Canutes API** (community, from DILA data) — already under evaluation; note prior Anubis anti-bot blocking on spec retrieval.
- ELI implemented for JORF publications.

### Administrative / parameter-value sources
- **BOFiP-Impôts** — https://bofip.impots.gouv.fr — official tax administration doctrine; frequently the clearest statement of thresholds/rates as applied. Available as open data (data.economie.gouv.fr). ⚠️ confirm current dump format.
- **barème IR, plafonds** published annually via Loi de finances; **SMIC, plafond de la sécurité sociale (PASS)** via décrets/arrêtés in JORF.
- Prior art: **leximpact GitLab repo** (OpenFisca-France AI-assisted parameter updates) — reference implementation for FR.

---

## Netherlands 🇳🇱

### Primary legislation (consolidated)
- **wetten.overheid.nl** — the **Basiswettenbestand (BWB)**: official consolidated collection of all national laws, AMvBs, ministerial regulations, policy rules. Every historical version ("toestand") retained with validity dates.
- Key acts:
  - **Wet inkomstenbelasting 2001 (Wet IB 2001)** — PIT boxes, heffingskortingen
  - **Wet op de loonbelasting 1964** — wage tax
  - **Algemene wet inkomensafhankelijke regelingen (AWIR)** + **Wet op de zorgtoeslag / huurtoeslag / kindgebonden budget** — means-tested allowances (toeslagen)
  - **Participatiewet** (social assistance), **AOW**, **Wet kinderopvang**
  - Annual **Belastingplan** + **bijstellingsregelingen** (indexation regulations) — where yearly amounts land

### Machine-readable access
- **BWB open-data repository**: every regulation version as XML over HTTPS (repository.officiele-overheidspublicaties.nl), ~45,000 regulations / 100,000+ versions, with per-version legal-technical metadata (WTI files incl. in-force dates). Initial full set (~160 GB, 14 GB zipped) requested from KOOP (wetten@overheid.nl); daily deltas via **SRU 2.0 API** (`zoekservice.overheid.nl/sru`, collection `BWB`), filterable e.g. by `rechtsgebied == belastingrecht`.
- Documented use case in the SRU manual is literally "the Belastingdienst ingesting all tax-related regulations" — strong fit signal.
- **officielebekendmakingen.nl** (Staatsblad/Staatscourant) via the same KOOP SRU infrastructure for as-published texts.
- Helpful third-party guide: **WetSuite dataset catalogue** (wetsuite.nl) — maps the whole Dutch legal open-data landscape.

### Administrative / parameter-value sources
- **Belastingdienst** — rates/tables, **Handboek Loonheffingen** (annual), newsletters with parameter tables.
- **Rijksoverheid.nl** and toeslagen tables for benefit amounts.

---

## Lithuania 🇱🇹

### Primary legislation (consolidated)
- **TAR — Teisės aktų registras** (Register of Legal Acts) — https://www.e-tar.lt — the official state register since 2014, maintained by the Seimas Chancellery; includes consolidated versions ("suvestinės redakcijos") with validity dates. This is the authoritative source.
- **e-Seimas** — https://e-seimas.lrs.lt — parliament's legislative database; includes some **English translations** of major laws (not always current — treat as convenience, not source of truth).
- Key acts:
  - **Gyventojų pajamų mokesčio įstatymas** (Law on Personal Income Tax, No IX-1007) — rates, NPD (tax-exempt amount) formula
  - **Valstybinio socialinio draudimo įstatymas** — Sodra contributions
  - **Piniginės socialinės paramos nepasiturintiems gyventojams įstatymas** — social assistance
  - **Išmokų vaikams įstatymas** — child benefits
  - Annual government resolutions setting **MMA** (minimum monthly wage) and base amounts (**bazinė socialinė išmoka**, **VDU** references)

### Machine-readable access
- TAR provides a **data provision service / API** ("Data provision from TAR" on the portal). ⚠️ The exact interface spec needs retrieval — but it demonstrably works: the community **Ansvar-Systems/Lithuanian-law-mcp** project pipelines "TAR API → parse → SQLite FTS5" over 12,000+ statutes with EU-law cross-references, and is worth reading as API documentation (same pattern as the matematicsolutions repos).
- Bulk text also exists as an ELRC corpus on data.europa.eu (crawled from e-tar.lt) — useful for embedding experiments, not for provenance.
- **Language:** current consolidations are Lithuanian-only — this is the strongest multilingual-RAG test case among the six.

### Administrative / parameter-value sources
- **VMI** (State Tax Inspectorate) — https://www.vmi.lt — rates, NPD calculators, guidance.
- **Sodra** — https://www.sodra.lt — contribution rates, pension parameters.
- **SADM** (Ministry of Social Security and Labour) — benefit amounts.

---

## Spain 🇪🇸

### Primary legislation (consolidated)
- **BOE — Agencia Estatal Boletín Oficial del Estado** — https://www.boe.es — official journal *and* consolidated legislation service ("legislación consolidada"), covering state law and the most relevant autonomous-community law.
- Key acts:
  - **Ley 35/2006 (IRPF)** + **RD 439/2007** (reglamento) — PIT: scale, mínimos personales/familiares, deductions
  - **RDL 8/2015 — Ley General de la Seguridad Social (LGSS)** — contributions, pensions, IMV (ingreso mínimo vital via Ley 19/2021)
  - Annual **Ley de Presupuestos Generales del Estado (LPGE)** — where many yearly amounts are set
  - **RD on SMI** (minimum wage), **IPREM** (set in LPGE)

### Machine-readable access — the strongest of the six
- **BOE open-data REST API** — `boe.es/datosabiertos/api/legislacion-consolidada`: search over 50,000+ consolidated norms; per-norm metadata, **ELI metadata**, legal analysis (in-force status, modifying/modified relations), and — critically — **block-level consolidated text**: each norm is split into blocks (article/chapter level), each block carrying **all versions with publication dates and the identifier of the modifying norm**. This is almost exactly the per-provision, per-effective-date structure the schema needs, delivered natively. Free, documented (APIconsolidada.pdf + FAQ), no key required.
- Companion APIs for daily BOE/BORME summaries and auxiliary code tables.
- ELI fully implemented (boe.es/eli/…).
- Community reference: **ComputingVictor/MCP-BOE** wraps this API as an MCP server (search, block diffs between dates, PDF text extraction) — same "read as documentation" caveat as matematicsolutions.

### Administrative / parameter-value sources
- **Agencia Tributaria** — https://sede.agenciatributaria.gob.es — IRPF manuals, withholding tables.
- **Seguridad Social** — bases y tipos de cotización tables.

### Regional scope — confirmed against EUROMOD Country Report ES (Y16, 2022–2025)
- **Regional IRPF is fully in scope.** EUROMOD ES simulates the state/regional split of the PIT: separate state and regional general and savings schedules, with a **distinct regional general schedule per common-regime region** (CR Tables 2.62 ff., "own elaboration based on regional legal sources"), regional variants of personal/family tax credits in ~8 regions (Andalucía, Illes Balears, Canarias from 2024, Cataluña, Madrid, Galicia, La Rioja, C. Valenciana), and a large catalogue of region-specific tax credits (CR Annex 4).
- **Foral regimes are explicitly out of scope**: País Vasco and Comunidad Foral de Navarra specificities are *not* simulated — their residents are modelled under common-regime rules. → Foral PIT laws (outside BOE) can be excluded from ingestion.
- **Regional benefits layer**: regional child benefits simulated under regional rules (`bchrg_es`); regional minimum income schemes included via calibration rather than full rule simulation; some regional housing benefits.
- **Ingestion consequence**: parameters are set annually in the National Budget Law **and 19 regional budget laws**. State-level ES is the easiest of the six via the BOE API, but full ES scope inherits a multi-gazette problem: BOE's consolidated collection includes the "most relevant" autonomous-community norms (each region's *texto refundido* of ceded-tax provisions may be covered), but per-region coverage of annual tax-measure laws must be verified — and where BOE consolidation lags, the fallback is 15+ regional gazettes (DOGC, BOJA, BOCM, DOGV, …).

---

## Ireland 🇮🇪

### Primary legislation
- **eISB — electronic Irish Statute Book** — https://www.irishstatutebook.ie — official Acts and Statutory Instruments **as enacted**, with ELI implemented (irishstatutebook.ie/eli/…).
- **Revised Acts — Law Reform Commission** — https://revisedacts.lawreform.ie — the *consolidated* (administratively revised) versions, including the two acts that matter most here. ⚠️ Important split: eISB alone gives as-enacted text; consolidation lives at the LRC.
- Key acts:
  - **Taxes Consolidation Act 1997 (TCA 1997)** — income tax, USC (Part 18D), tax credits
  - Annual **Finance Acts** — where rates/credits/bands change each year
  - **Social Welfare Consolidation Act 2005** + annual **Social Welfare Acts** — benefit rates, PRSI

### Machine-readable access
- eISB offers XML/HTML per document via stable ELI-pattern URLs; no rich query API comparable to ES/NL — crawl via ELI URL structure. ⚠️ Verify current bulk options.
- **Internal asset:** Hannes's **Ireland JSON DB prototype** — treat as the structured national-team source in the hybrid architecture; the legislative crawl validates against it rather than replacing it.

### Administrative / parameter-value sources
- **Revenue** — https://www.revenue.ie — **Tax and Duty Manuals** plus current rates/credits/bands pages; usually the fastest authoritative statement of applied values.
- **Department of Social Protection** (gov.ie) — **SW19 rates of payment booklet** (annual) — canonical benefit-amount table.
- **Budget.gov.ie** — annual parameter announcements ahead of Finance Act codification (a concrete case of the "parliamentary/budget decision precedes formal consolidation" pattern → `legal_status` enum).

---

## Belgium 🇧🇪

### Primary legislation (consolidated)
- **Moniteur belge / Belgisch Staatsblad + Justel** — https://www.ejustice.just.fgov.be — official journal and the Justel consolidated-legislation database (FR/NL, partly DE). **ELI implemented** — stable URIs of the form `ejustice.just.fgov.be/eli/loi|wet/YYYY/MM/DD/{numac}`.
- Key acts:
  - **CIR 92 / WIB 92** (Code des impôts sur les revenus / Wetboek van de inkomstenbelastingen) + **AR/CIR 92** (implementing decree) — PIT scale, quotités exemptées, reductions
  - Social security framework laws + annual **loi-programme / programmawet** — frequent vehicle for parameter changes
  - **Indexation mechanism**: many amounts (benefits, tax brackets) are auto-indexed via the **health index / pivot index** rather than re-legislated — the applied values are published in MB notices and administrative tables. First-class case for source-tagging: the "source" is an indexation event, not an amending act.

### Machine-readable access
- ⚠️ **Weakest machine access of the six.** No documented public bulk API for Justel; ingestion likely via ELI URL patterns + scraping, or via the MB publication feeds. Budget crawler-hardening time here, and ask the BE national team what they use.
- Regional layer (PIT partly regionalized since the 6th state reform — e.g. housing-related tax credits): **Vlaamse Codex** (codex.vlaanderen.be), **Wallex** (wallex.wallonie.be), Brussels regional gazette.

### Administrative / parameter-value sources
- **Fisconetplus** — FPS Finance legal & tax database (public access via eservices.minfin.fgov.be, myMinfin platform): updated tax legislation, circulars, administrative commentary, case law. The de-facto operational source for applied tax parameters. ⚠️ Behind a JS-heavy portal with bot protection — test crawlability early.
- **SPF/FOD Finances** — https://fin.belgium.be — rates, indexed amounts.
- **ONSS/RSZ** and **SPF Sécurité sociale** — contribution rates, indexed benefit amounts.

---

## Summary matrix

| Country | Consolidated source | Bulk/API access | Identifier | Language(s) | Machine-access grade |
|---|---|---|---|---|---|
| FR | Légifrance (LEGI) | DILA XML dumps + PISTE API | ELI (JORF), LEGI ids | FR | ★★★ |
| NL | wetten.overheid.nl (BWB) | XML repository + SRU 2.0 deltas | BWBR | NL | ★★★ |
| LT | TAR (e-tar.lt) | TAR API (spec ⚠️) | TAR ids | LT only | ★★ |
| ES (state) | BOE legislación consolidada | REST API, block-level versions, ELI metadata | ELI, BOE-A | ES | ★★★★ |
| ES (regional, 15+ regions — required by EUROMOD) | BOE (partial) + regional gazettes | BOE API where consolidated; per-gazette otherwise ⚠️ | ELI (varies) | ES (+ co-official) | ★★ |
| IE | eISB + LRC Revised Acts | ELI-pattern URLs, no query API ⚠️ | ELI | EN | ★★ |
| BE | Justel / Moniteur belge | No public bulk API ⚠️ | ELI | FR/NL(/DE) | ★ |

**Implication for the vertical slice:** Spain is two-tier — state-level parameters are the easiest ingestion target of the six (BOE API serves block-level versioned consolidated text out of the box), but full EUROMOD ES scope requires the regional layer (per-region schedules and credits across 19 annual budget laws), pushing overall ES effort well above the state-only picture. Ireland remains the strongest slice candidate (existing JSON DB prototype, English-language corpus, single legislature), with France close behind via the leximpact prior art. Belgium should be tackled last. A pragmatic ES demo could scope to state schedule + one or two regions to prove the regional pattern without ingesting all gazettes.

---

## Open items

1. Retrieve TAR API specification (LT) — read Ansvar-Systems/Lithuanian-law-mcp source as interim documentation.
2. Test Fisconetplus crawlability (BE) and identify what the BE national team uses internally.
3. Confirm eISB bulk/XML retrieval options (IE) vs. crawling ELI URLs.
4. Confirm BOFiP open-data dump format and update cadence (FR).
5. ~~Clarify EUROMOD ES scope re: regional IRPF and foral regimes~~ — **resolved via CR Y16**: regional IRPF fully modelled per region; foral regimes excluded. Follow-ups: (a) ask the ES national team where they source the 19 annual budget laws and regional credit rules today; (b) test BOE API coverage of each region's ceded-tax *texto refundido* and annual tax-measure laws.
6. Request BWB initial set from KOOP (NL) if NL enters the slice — lead time for the USB/download delivery.
