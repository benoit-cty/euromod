# 02 — Decide how a regional act is scoped: child jurisdiction or ES + region tag

Status: resolved (decision taken by the agent on the user's instruction to implement; ADR 0003 is the record to contest)
Blocked by: 01

## The decision

`retrieval.py` filters `j.code = %(country)s` exactly, in both
`_LIVE_VERSION_CTE` and `_CR_SEARCH_SQL`. Two options, both needing code:

**A. Child jurisdictions.** `jurisdictions.parent_id` exists and the seed's ES
row already says "comunidades autonomas join later as child jurisdictions (ISO
3166-2)". Ingest Aragón's decree under `ES-AR`. Retrieval then has to walk the
tree (`j.code = country OR j.parent_id = (SELECT id …)`), and a region-scoped
run narrows to one child. Honest data model; touches the retrieval predicate,
which every country shares.

**B. Stay under `ES`, tag the region.** Regional acts are retrievable the day
they are ingested, no SQL change. But nothing stops a proposal for Aragón's
`$bsarg_rg24_basic_amt` quoting Asturias's decree verbatim — the extract check
passes, because the quote is real and only the region is wrong. Needs a region
filter somewhere regardless, so the SQL change is deferred, not avoided.

Recommendation: **A**, because B's failure is silent and produces a
*confidently wrong* proposal with a valid verbatim extract, which is precisely
the failure mode the pipeline's anti-hallucination rule exists to exclude.

## Whichever is chosen

The region key is already available on both sides and needs no inference:
- parameter side — `bsarg_rgNN` / `bchrg_regNN` are NUTS-2 codes (verified).
- corpus side — BOE metadata carries `ambito: Autonómico`, `ambito_codigo`
  and `departamento: Comunidad Autónoma de <name>`.

What is missing is the mapping table between them (NUTS-2 `ES12` ↔ ISO 3166-2
`ES-AS` ↔ BOE `departamento` string). Write it once, in one place, and derive
everything from it — the same rule `schema.income_year_for` follows for FR.

## Deliverable

An ADR under `docs/adr/`, since this changes a shared retrieval predicate and
binds every country, not just ES.

## Answer (2026-09-08)

**Option A**, as recommended — recorded in
[docs/adr/0003-regional-acts-are-child-jurisdictions-scoped-by-the-parameter-region.md](../../../docs/adr/0003-regional-acts-are-child-jurisdictions-scoped-by-the-parameter-region.md).

Two refinements over the text above, both from issue 01's measurement:

- The **scope is `[country]` for a national parameter and `[country, child]`
  for a regional one — never `country OR parent = country`.** The tree walk
  would have re-created option B: every Spanish run seeing every region. The
  practical effect showed up immediately: the Galicia decree (`DL 1/2011`,
  ingested in August under `ES`) was being retrieved for the *national*
  personal minimum and for the savings rate (`baseline_before.json` vs
  `baseline_after.json`: `DL 1/2011 Galicia Artículo 4 bis` ranked among the
  FTS top-10 for «mínimo del contribuyente»). It now serves `…rg11…`
  parameters only. FR/IE/LT/NL results are byte-identical.
- The **mapping table lives in one place**,
  `Nomotheca-RAG/ingest/src/nomotheca_ingest/countries/es/regions.py`
  (ISO 3166-2 ↔ NUTS-2 ↔ BOE `departamento` ↔ ELI segment); `db/seed.sql` and
  `db/migrations/0002_es_autonomous_communities.sql` are generated from it and
  `tests/test_es_regions.py` fails when either drifts. The pipeline never
  copies it: it reads `jurisdictions.metadata->>'nuts2'` from the DB.
- The **region key is read off the parameter name, not curated**: unlike
  `temporal_basis`, EUROMOD's naming convention states it (`_rgNN_`, `_regNN_`,
  `…rgNN_` — 689 ES parameters across `bsarg_es`, `bchrg_es`, `poanc_es`,
  `tin_cons_es`, every one a valid NUTS-2 code, 0 strays). The ELI's
  jurisdiction segment (`/eli/es-ga/…`) places an act at parse time, with
  BOE's `departamento` as fallback; an *Autonómico* act neither can place is
  refused, not filed under `ES`.
