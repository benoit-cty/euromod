# ES autonomous communities: their own decrees as citable evidence

Status: in-progress — 01, 02, 03, 04 resolved; 05 partially (see the issue); 06 opened for the amounts
Created: 2026-09-08

## Why

Two ES parameter families hold amounts that no state act states, because each
autonomous community fixes them in its own decree:

| Policy | Constants | Regions present |
|---|---|---|
| `bsarg_es` — Rentas Mínimas de Inserción | 32 | 12, 21, 22, 24, 30, 42, 51, 53, 63, 64, 70 |
| `bchrg_es` — regional child benefits | 49 | 11, 12, 13, 21, 24, 30, 42, 51, 61 |

Union: 14 of the 19 communities. Today the ES corpus holds 7 instruments
(LIRPF, RIRPF, LGSS, Ley 19/2021 IMV, RD 87/2025 SMI, one Galicia decreto
legislativo, the Country Report) and no regional social legislation, so all 81
parameters route `not_found`.

They are deliberately **not** flagged `national_team` in
`curation/ES.curation.yaml`: these values are legislation, and flagging them
would freeze a corpus gap into a permanent "no law exists" claim. Closing the
gap is this effort.

## What is already true (verified 2026-09-08)

1. **BOE's consolidated database already carries autonomous-community law, and
   the existing adapter already fetches it.** `BOE-A-2011-18161` (Galicia's
   Decreto Legislativo 1/2011) is in the corpus and re-fetches 200 from
   `legislacion-consolidada/id/…` with `Accept: application/xml`. No new
   source, fetcher or parser is needed to ingest a regional act — only its id.
2. **The region is already in the data we store.** That instrument's
   `instruments.metadata` carries `"ambito": "Autonómico"`, `"ambito_codigo":
   "2"`, `"departamento": "Comunidad Autónoma de Galicia"`. The parser
   preserves the BOE metadata block as-is.
3. **The parameter names already carry the region key.** `bsarg_rgNN` and
   `bchrg_regNN` are NUTS-2 codes, verified against the enriched descriptions:
   12 Asturias, 21 País Vasco, 22 Navarra, 24 Aragón, 30 Madrid, 42
   Castilla-La Mancha, 51 Cataluña, 53 Illes Balears, 63 Ceuta, 64 Melilla,
   70 Canarias, 11 Galicia, 13 Cantabria, 61 Andalucía.
4. **The Country Report names the acts.** Every region's subsection under
   `bsarg_es` ends in a `**Legal sources**` block citing its decrees by
   number and date (e.g. Aragón "Decreto-Ley 1/2025, de 9 de abril"; Canarias
   "Ley 5/2022, de 19 de diciembre, de la renta canaria de ciudadanía").
   The CR is `context` and can never be cited as evidence — but it is the
   right place to *find out what to ingest*.
5. **BOE's search API is unusable**, as it already is for state acts: every
   documented `query=` form answers HTTP 500 (`Server error - Code: 109`).
   Resolution must run off a curated alias table, exactly as `EsResolver`
   already does for the 5 state acts.

## The load-bearing design question

`retrieval.py` filters candidates with `j.code = %(country)s` — an exact
match, in both `_LIVE_VERSION_CTE` and `_CR_SEARCH_SQL`. So:

- If regional acts are ingested as **child jurisdictions** (`ES-AS`, `ES-CN`,
  … — what `schema.sql` anticipates with `jurisdictions.parent_id` and the
  seed's `regional_note`), every one of them becomes **invisible** to
  retrieval until that predicate walks the jurisdiction tree.
- If they stay under `ES`, they are retrievable immediately — but nothing
  scopes a *region's* parameter to that region's law. Aragón's
  `$bsarg_rg24_basic_amt` could then be "supported" by a verbatim quote from
  Asturias's decree. The extract check would pass: the quote is real, it is
  simply the wrong region's law. That is a new class of false positive the
  mechanical anti-hallucination rule cannot catch.

Both options need work; the second is the more dangerous default because it
fails silently. Decide before ingesting the first regional act.

## Out of scope

- Regional IRPF (`tin_cons_es`, 623 constants). Same shape of problem, much
  larger; handle it once the pattern is proven on `bsarg_es`.
- Communities whose social legislation BOE does not consolidate. Feasibility
  is proven for Galicia only; issue 01 measures the real coverage.
