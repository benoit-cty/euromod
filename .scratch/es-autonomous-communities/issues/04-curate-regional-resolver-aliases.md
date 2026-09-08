# 04 — Add the regional acts to EsResolver's alias table

Status: resolved
Blocked by: 01, 02

## What

`EsResolver._ALIASES` holds 5 state acts. BOE's search API is dead (HTTP 500
on every `query=` form), so regional acts resolve the same way: a curated
table, from issue 01's findings.

Keep the existing shape — alias → BOE id, matched with the word-boundary
regex — and add the regional entries. Aliases must be unambiguous across
regions: several communities have a "Ley 5/2022" and a "renta garantizada", so
a bare number or a scheme name is not a key. Prefix or qualify with the region.

## Also

- Extend `canary_facts()` with one regional canary, so a stale regional source
  is detected the same way a stale LIRPF is.
- Regional acts amend often via annual budget laws (the CR lists a different
  presupuestos law per year per region). Confirm the consolidated BOE payload
  carries those amendments as dated versions of the block — if it does not,
  point-in-time selection for regional parameters is unsound and that is a
  finding worth its own issue.

## Answer (2026-09-08)

Done in `countries/es/resolver.py` and `countries/es/parser.py`:

- **Region-qualified aliases** for 19 consolidated regional acts (the 14+1
  ingested plus Extremadura, La Rioja, Murcia framework laws), matched
  accent-insensitively (`Ley 3/2021 Aragón` = `ley 3/2021 aragon`). A **bare
  regional number is refused** with the candidates named — `Ley 3/2021` →
  "Ambiguous … one of ['LEY 3/2021 ARAGON', 'LEY 3/2021 ASTURIAS']" — because
  Asturias and Aragón really do share it. State numbers (`35/2006`) still
  resolve bare.
- **ELI resolution**: a citation carrying a BOE ELI path resolves by reading
  the ELI page's `<title>` (the one lookup BOE still answers). A *published but
  not consolidated* act (regional budget laws) is refused with its BOE id and
  the reason, instead of failing in the fetcher with a bare 404.
- **Short citations** in `KNOWN_ACTS` for every alias target, qualified by
  region (`Ley 5/2022 Canarias Artículo 8`), with a test that every alias
  target has one.
- **Regional canary**: `Ley 14/2022 País Vasco Artículo 13`, latest version
  ≥ 2025-12-30 (amended by `BOE-A-2026-1256`; art. 64 by `BOE-A-2026-1257`
  with effect 2026-01-01).

**Finding on the "Also" question — annual amendments as dated versions.** For
*consolidated* regional laws BOE does mint dated versions per block exactly as
for state law (Ley 14/2022 PV: 210 blocks / 225 versions; Ley 1/2007 Canarias:
67 / 111; Ley Foral 15/2016: 62 / 73), so point-in-time selection is sound for
them. But the **annual budget laws that set the amounts are not consolidated
at all** — not "consolidated without versions", absent — so for the amounts
the question is moot until issue 06 brings them in as one-version instruments
of the daily gazette. That is a sound model too (`validity` from
`fecha_vigencia`, open-ended until the next budget law supersedes it), but it
is a different ingestion path.
