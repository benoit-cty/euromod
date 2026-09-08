# ES and NL — state and traps when this skill was written (2026-09-08)

Everything here was read off the live DB and the exports on that date. The
readiness queries in `SKILL.md` §0 are the source of truth; this file is
what they will not tell you — the trap behind each number.

## Spain (ES) — legislation language `es`

**Corpus.** Six acts plus the Country Report, all embedded, and translated
(2 786 `es` chunks, 2 771 `en`): LIRPF `BOE-A-2006-20764`, RIRPF
`BOE-A-2007-6820`, LGSS `BOE-A-2015-11724`, IMV `BOE-A-2021-21007`, SMI
RD 87/2025 `BOE-A-2025-2576`, Galicia DL 1/2011 `BOE-A-2011-18161`. Detail
and open points: `Nomotheca-RAG/Spain_sources_analysis.md` §5–6.

**Store.** 1 219 parameters, 26 policies, 8 groups. No curation overlay yet.

- `tin_cons_es` is 623 parameters — the per-autonomous-community half of the
  PIT. 35 of them hold `n/a` at 2025-06-01. Regional PIT scales are only in
  the corpus for Galicia; a case on another community is `corpus_available: false`.
- `ConstDef_es` (82) holds 21 `$`-references (`$tscag_ee_rate5 = $tscft_ee_rate5`
  and siblings) — the `derived` candidates.
- `tco_es` (227), `bunct02_es` (12), `bwr_es` (3) have no numeric value at
  `as_of` — consumption-tax tables and imputations, the `national_team_source`
  candidates (IE's `tco_ie` precedent). `xcc_es` (regional childcare fees) and
  `bsarg_es` (calibrated regional minimum-income schemes) are the other two
  families the sources analysis names for the overlay.
- Names differ from the obvious: there is no `$SMI`; the minimum wage is
  `euromod://ES/ConstDef_es/def_const/$SMI2`, IPREM is `$IPREM`, both
  `currency/month`.
- Groups: `ES:tin_cons_es:tin_schedule` assembles **thresholds only** (every
  rate `None`) — not a sound `table` case until the group definition is fixed.
  `ES:twl_es:twl_schedule` (wealth tax, 8 bands, unchanged since 2010)
  assembles fully, but its stating act (Ley 19/1991) is not ingested.

**Traps.**

- **State share vs total.** LIRPF art. 66 holds two scales: paragraph 1 is
  the *state half* of the savings schedule (top rate 15 %), paragraph 2 the
  full rate for non-residents (30 %). The CR's "savings rate 28 % → 30 %" is
  state + regional. Before writing an expected rate, decide which one the
  EUROMOD parameter holds and say so in `note`.
- **Effect date ≠ in-force date.** BOE's `fecha_vigencia` is legal entry into
  force (savings scale: `[2024-12-22,)`) while the measure applies "con
  efectos desde el 1 de enero de 2025". `expected_valid_from` is the fiscal
  effect date; the amendment trail at the end of each version's text states it.
- **LPGE prorogued for 2024 and 2025.** Recent values arrive through ordinary
  laws and decree-laws (Ley 7/2024 for the 2025 savings rate), so the
  `not_found` case's `note` should name the actual instrument, not "the budget law".
- **SMI is stated twice.** RD 87/2025 art. 1 reads "39,47 euros/día o 1184
  euros/mes" (no thousands separator), 14 payments a year — a
  `unit_conversion` hazard if EUROMOD stores it on another basis.
- Foral regimes (País Vasco, Navarra) are out of scope by decision; never a case.
- Citation spellings in the corpus: `RD SMI 2025 Artículo 1`, `LGSS Artículo 332`,
  `LGSS Sección 2 (4)` — repeated block titles carry a `(n)` suffix. **The Ley IMV
  units use a non-breaking space** between `Artículo` and the number (bytes `c2a0`):
  an exact-match query with a plain space returns nothing, and so does the
  pipeline's citation match. Compare bytes:
  `SELECT encode(convert_to(citation,'UTF8'),'hex') FROM legal_units WHERE citation ILIKE '%IMV%13%'`.
- Shell quoting bites these queries: a `$` before a closing quote inside a
  double-quoted `docker exec … -c "…"` string starts a bash `$'…'` literal, and
  accented characters survive better through a heredoc (`docker exec -i … psql <<'SQL'`).
  Prefer the heredoc form for any query carrying `í`, `$` or ` `.

**Temporal basis.** `in_force`: the IRPF *período impositivo* is the calendar
year, EUROMOD system year Y states year Y. Record it in the overlay header and
the selection's `conventions`.

**Country Report.** `08 - EUROMOD Triangulator/country-reports/Y16/ES_Y16.md`,
section *Main policy changes between 2024-2025* (around line 2510). Ingested
as `country_report` (224 chunks).

## Netherlands (NL) — legislation language `nl`

**Corpus.** Fourteen acts plus the Country Report, all embedded — and **not
translated** (2 865 `nl` chunks, 1 `en`). Anchor ids in
`Nomotheca-RAG/Netherlands_sources_analysis.md` §1; Wet IB 2001 is
`BWBR0011353`, Wfsv `BWBR0017745`, Participatiewet `BWBR0015703`. Record the
translation gap under *Prerequisites and gaps* — the English query leg has
nothing to hit until `translate run` is done.

**Store.** 528 parameters, 19 policies, 14 groups. `NL.curation.yaml` exists
since the set was built (2026-09-08): `$xcc_amt` + 296 `$tco_t_*` national_team,
23 `/100` rates curated to `/1`, tax-rate basis decided (`$tin_br1` = statutory
8,17 %). Set: `golden_sources/nl.json`, rationale `golden_set_NL.md`.

- `tco_nl` is 373 of the 528 and has no numeric value — the
  `national_team_source` family.
- Percent literals everywhere in tax: `tin_nl` 12 of 18, `tintc_nl` 13 of 27,
  `peoplesic_nl` 3 of 3, `tschl_nl` 2 of 4 (`'6.1%'`, `'37.48%'` style).
  `normalise_value` reads them; keep the string spelling in `expected_value`
  and state `routing:` if the build refuses to cross-check.
- `$`-references: `tschl_nl/$tschl_uplim = '$EI_Maxpremwag'`, one in
  `ersic_NL` — the `derived` candidates.
- The export projects to 2026 (`$EI_maxdwag`: 290.67#d for 2025, 304.25#d for
  2026): read the value in force at `as_of`, never the last row.
- Units: `currency/day` on the *dagloon* parameters, and `/100` on 23
  rate parameters (`$peoplesic_aow_rate`) — check what the stored magnitude
  means before deciding whether the overlay must curate them to `/1`.
- `bho_nl` (rent allowance) holds 12 `n/a` values at `as_of`.
- Groups: `NL:tin_nl:tin_b_schedule` assembles as **one empty bracket** for
  2025 (rates are percent strings, so `value` is null) — not a sound `table`
  case. Assemble the other ten schedules before promising one.

**Traps.**

- **The indexation regulation is the operative source.** Wet IB 2001 art. 2.10's
  2025 text carries `bron="Stcrt.2024-38492"`: the bracket amounts were
  rewritten by a *bijstellingsregeling* that is not ingested, while the
  consolidated article states them. Cite the article (`Wet IB 2001, artikel 2.10`;
  Wet LB 1964 art. 20a mirrors it) and flag `cross_instrument`.
- **8,17 % vs 35,82 %.** Art. 2.10 states the *tax* rate of the first band
  (8,17 %); EUROMOD may hold the combined tax-plus-premium rate (35,82 %),
  which no single article states. Decide the basis and write it into
  `NL.curation.yaml` before any tax-schedule case; a combined-rate parameter
  is a `national_team_source` candidate (sources analysis §6.3–6.4).
- **Toeslagen amounts live in AMvBs**, not the framework acts: the Wet op de
  zorgtoeslag sets the formula, a separate *besluit* fixes the standard
  premium. Those are the honest `not_found` cases, each naming the BWB id to ingest.
- **Sampling granularity.** One *toestand* per policy date was fetched, so a
  mid-year change may be invisible to the corpus (sources analysis §6.1) —
  a `mid_year_change` hazard the corpus cannot currently evidence.
- **The drempelinkomen is the minimum wage.** WKB art. 1(1)(d) and Wet op de
  zorgtoeslag art. 1(1)(f) define it as 108 % × 12 × the WML art. 8(1)(b) monthly
  amount (`BWBR0002638`, NOT ingested): 28.406 = 1,08 × 12 × 2.191,80. Ingesting
  the WML flips the minimum-wage case and gives the `$chall_B2` combine case its base.
- **The parser drops `<formule>` elements** — Participatiewet art. 22a's
  kostendelersnorm formula is missing from its chunk. Tables survive, formulas do not.
- **Only 1 January toestanden are sampled**: one NL version in the whole corpus
  starts 2025-07-01, so the semi-annual indexation (WML, AKW, Pw, AOW) is invisible.
- Canary, verified: art. 2.10 at 2025-06-30 reads `– | € 38.441 | – | 8,17%`,
  `€ 38.441 | € 76.817 | € 3.140 | 37,48%`, `€ 76.817 | – | € 17.523 | 49,50%`;
  the 2024 text differs, so point-in-time retrieval discriminates. Amounts are
  spelled `€ 38.441` — regex with the dot escaped.

**Temporal basis.** `in_force`.

**Country Report.** `08 - EUROMOD Triangulator/country-reports/Y16/NL_Y16.md`,
section *Main policy changes between 2024 and 2025* (around line 1105).
Ingested as `country_report` (125 units).
