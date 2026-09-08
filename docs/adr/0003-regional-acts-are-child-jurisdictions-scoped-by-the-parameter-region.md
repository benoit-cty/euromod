---
status: accepted
date: 2026-09-08
---

# Regional acts are child jurisdictions, and retrieval is scoped by the parameter's region

Two ES parameter families (`bsarg_es`, regional minimum incomes, 32 constants; `bchrg_es`,
regional child benefits, 49) and two more that share the naming (`poanc_es`, and the 547
regional IRPF constants of `tin_cons_es`) hold amounts that each autonomous community fixes
in its own law. Nothing in the state acts states them, so every such run was `not_found`.
BOE's consolidated database already carries autonomous-community law under ordinary
`BOE-A-` ids and the existing ES adapter already fetches it (the Galicia decree
`BOE-A-2011-18161` has been in the corpus since August) — but it was filed under `ES`, and
evidence retrieval filtered on `j.code = country` exactly.

We decided that **an autonomous-community act is filed under a child jurisdiction**
(`ES-AR`, `ES-CN`, … — ISO 3166-2 codes, `jurisdictions.parent_id = ES`, seeded from one
table in `countries/es/regions.py`), that **the ES parser places it there at ingest time**
from the ELI's jurisdiction segment (fallback: BOE's `departamento`), and that **evidence
retrieval filters on a jurisdiction *scope*** — the country's code plus, for a regional
parameter, its own community's code — instead of on one country. The region of a parameter
is read off its name (`$bsarg_rg24_*`, `$bchrg_reg24_*`, `$tin_depallrg24_*` carry the NUTS-2
digits `24` = Aragón) and mapped to the child through `jurisdictions.metadata->>'nuts2'`.

## Considered options

- **Stay under `ES`, tag the region in metadata.** Regional acts are retrievable the day
  they are ingested, no SQL change. Rejected because nothing then stops a proposal for
  Aragón's `$bsarg_rg24_basic_amt` from quoting Asturias's decree verbatim: the extract
  check passes, because the quote is real and only the region is wrong. That is a new class
  of *confidently wrong* proposal the mechanical anti-hallucination rule cannot catch, and it
  fails silently.
- **Curate the region on the parameter** (an overlay key like `temporal_basis`). Rejected as
  redundant: unlike the temporal basis, the region *is* in the export — EUROMOD's own naming
  convention embeds the NUTS-2 code — so deriving it is reading, not inferring. The digits
  are checked against the country's NUTS-2 set, so `…rate10_` can never become a region.
- **Widen the country filter to the whole tree** (`j.code = country OR parent = country`).
  Rejected: that is option one with more rows — every Spanish run would see every region.

## Consequences

- `retrieval._LIVE_VERSION_CTE` filters `j.code = ANY(%(jurisdictions)s)`; the retrieval
  functions accept a scope where they took a country string, and every existing caller still
  passes a string. FR/IE/LT/NL results are unchanged (verified by diffing stored results
  before and after). **National ES runs no longer see regional acts** — the Galicia decree
  used to be retrievable for Madrid's regional IRPF constants, a latent instance of the same
  false positive; it now serves `…rg11…` parameters only.
- A region the database does not know scopes to the country alone: the failure mode is
  `not_found`, never a sibling region's value. The scope travels on the `retrieve` span
  (`retrieval.jurisdictions`) and in the workflow state.
- Country Report search stays country-wide (the CR is filed under the country and describes
  the regional parameters too), and the proposal prompt names the region for a regional
  parameter.
- Existing databases run `db/migrations/0002_es_autonomous_communities.sql`, which seeds the
  19 children, re-homes acts already ingested under `ES` by ELI or `departamento`, and
  **fails loudly** if an act BOE labels *Autonómico* is still under `ES` afterwards. An
  unplaceable regional act is refused at parse time for the same reason.
- The UI's per-jurisdiction statistics and the MCP/UI country filters roll children up into
  their country, so `ES` still means "Spain, all of it" for a human browsing the corpus.
- Citations of regional acts are qualified by region (`Ley 3/2021 Asturias Artículo 14`):
  Asturias and Aragón both have a Ley 3/2021. The resolver refuses a bare regional number
  and names the candidates.
- Coverage finding, measured 2026-09-08: BOE consolidates the communities' *framework* laws
  (all 14 regions present in `bsarg_es`/`bchrg_es` but Ceuta and Melilla) and **none of the
  annual budget laws** that carry the current amounts — those are published in the daily
  gazette (`diario_boe/xml.php`, one version, no consolidation) and reachable only through
  a second fetch path, tracked as `.scratch/es-autonomous-communities/issues/06`. Regional
  decretos and órdenes (all of `bchrg_es`) are not in BOE at all.

Refines the "regional layer" open point of `07_risks-and-decisions.md` and
`Nomotheca-RAG/Spain_sources_analysis.md` §E.
