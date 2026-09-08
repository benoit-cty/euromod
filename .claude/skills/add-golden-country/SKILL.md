---
name: add-golden-country
description: Add a country to the Nomokrisis golden set — readiness gate (corpus, embeddings, translation, parameter store, curation overlay, scout), select ~10 parameters spread across the difficulty ladder and the routing traps, establish each ground truth against the ingested act, write golden_sources/<cc>.json + golden_set_<CC>.md + curation/<CC>.curation.yaml, build, smoke-run, hand the drafts to a human. Use when asked to add a country to the golden set or evaluation dataset ("add ES and NL to the golden set", "golden cases for the Netherlands"), or to extend an existing country's set with new difficulty tiers.
argument-hint: <CC> [--year 2025]
---

# Add a country to the golden set

The golden set exists to make improvements legible over time. That only works
if every case sits on a known rung of the **ladder** (`verbatim` · `combine` ·
`derive` · `table`) and every case that fails today names the **one change
that flips it** — an act to ingest, a scoring rule, a pipeline capability.
A set of easy `unchanged` cases measures nothing but resistance to change:
the first FR set was 42/47 `unchanged`, all `verbatim`, and could not show
whether the pipeline could combine provisions at all. The hand-curated IE and
LT sets are the template — read
[golden_set_IE.md](../../../Nomokrisis-evaluation_pipeline/golden_set_IE.md) and
[golden_sources/lt.json](../../../Nomokrisis-evaluation_pipeline/golden_sources/lt.json)
once before starting, then copy their shape.

**Done means all five exist and the last one is a list, not a promise:**

1. `Nomoscope-agentic-workflow/pipeline/curation/<CC>.curation.yaml`, applied.
2. `Nomokrisis-evaluation_pipeline/golden_sources/<cc>.json` meeting the
   spread table in §2, every entry's ground truth checked against the act (§3).
3. `Nomokrisis-evaluation_pipeline/golden_set_<CC>.md`, the rationale and gaps.
4. `dataset/<cc>/` drafted by the builder with **zero skips**, every warning read.
5. A `mock/extractor` run over the drafts, and the case ids handed to the user
   to verify. **Never run `verify` yourself** — `verified: true` is a human's
   signature.

Ground truth is generated, never hand-written: edit the selection file and
rebuild. Never edit a file under `dataset/`.

## 0. Readiness gate

A golden case for a country whose acts are not in the corpus measures ingest,
not the model. Establish the state before choosing anything:

```bash
cd Nomokrisis-evaluation_pipeline
DB=$(docker compose -f ../docker-compose.yml ps -q db); CC=ES
docker exec $DB psql -U jrc -d legislation -A -c "
SELECT i.instrument_type, count(*) FROM instruments i JOIN jurisdictions j ON j.id=i.jurisdiction_id
WHERE j.code='$CC' GROUP BY 1;"                                        # acts ingested (+ the country_report row)
docker exec $DB psql -U jrc -d legislation -A -c "
SELECT ut.lang, count(DISTINCT c.id) chunks, count(DISTINCT e.chunk_id) embedded
FROM instruments i JOIN jurisdictions j ON j.id=i.jurisdiction_id
JOIN legal_units lu ON lu.instrument_id=i.id JOIN legal_unit_versions v ON v.legal_unit_id=lu.id
JOIN unit_texts ut ON ut.version_id=v.id JOIN chunks c ON c.unit_text_id=ut.id
LEFT JOIN embeddings e ON e.chunk_id=c.id
WHERE j.code='$CC' AND i.instrument_type<>'country_report' GROUP BY 1;"   # native + 'en' rows: embedded and translated?
docker exec $DB psql -U jrc -d legislation -A -c "
SELECT count(*), count(*) FILTER (WHERE temporal_basis<>'in_force') curated_basis FROM params.parameters WHERE country='$CC';
SELECT group_id, kind FROM params.parameter_groups WHERE country='$CC';"
ls ../Nomoscope-agentic-workflow/pipeline/curation/$CC.curation.yaml
grep -n "\"$CC\"" ../Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/scout.py | head -2
```

| check | if missing |
|---|---|
| acts ingested | stop: run the `add-country` skill / `nomotheca_ingest.cli <cc> instrument …` first |
| chunks embedded | `nomotheca_ingest.cli embeddings build` (see CLAUDE.md); a case over unembedded text is a retrieval miss by construction |
| `en` chunks ≈ native chunks | translation not run — does not block the set, but record it under *Prerequisites and gaps*: the English query leg has nothing to hit |
| `params.parameters` rows | `nomoscope-workflow ingest-params ../../extracted_parameters/enriched/<CC>.enriched.json` |
| curation overlay | written in §4 — every country needs one for the `national_team_source` trap |
| scout entry | add `COUNTRY_SOURCES`/`ID_HINTS` in `scout.py` (the IE/LT commit shows the shape); without it the `not_found` case can never flip |

Then pick the **drafter branch**. `SELECT kind, country FROM params.external_corpora;`
— a row for the country means the OpenFisca path (FR: `build-openfisca-dataset`,
README "Building it from OpenFisca-France"). No row means the curated path,
which is the rest of this skill. Today only FR has a corpus.

State of ES and NL when this skill was written, with the traps already found:
[country-notes.md](country-notes.md). Re-run the queries above anyway.

## 1. Survey what the store holds

Choose from what the store can materialize, never from the export file:

```bash
docker exec $DB psql -U jrc -d legislation -A -c "
SELECT p.policy, count(*) total,
       count(*) FILTER (WHERE v.value_numeric IS NOT NULL) numeric_at_asof,
       count(*) FILTER (WHERE v.raw_euromod_value LIKE '%\$%') dollar_refs,
       count(*) FILTER (WHERE v.raw_euromod_value LIKE '%\%%') pct_strings,
       count(*) FILTER (WHERE v.raw_euromod_value = 'n/a') na
FROM params.parameters p
LEFT JOIN LATERAL (SELECT mv.value_numeric, mv.raw_euromod_value FROM params.model_values mv
   WHERE mv.parameter_id=p.id AND mv.valid_from <= DATE '2025-06-01'
     AND (mv.valid_to IS NULL OR mv.valid_to >= DATE '2025-06-01')
   ORDER BY mv.valid_from DESC LIMIT 1) v ON true
WHERE p.country='$CC' GROUP BY 1 ORDER BY 2 DESC;"
```

Read the columns as a map of the ladder: `dollar_refs` are the `derived`
candidates, `pct_strings` the percent-literal parameters, `na` and
`numeric_at_asof = 0` families (consumption-tax `tco_*`, calibrated regional
schemes) the `national_team_source` candidates. A parameter with no value at
`as_of` makes a case about nothing.

Assemble every `bracket_schedule` group before promising a `table` case —
the LT schedule came out rates-only, the ES and NL PIT schedules worse:

```bash
(cd ../Nomoscope-agentic-workflow/pipeline && uv run python -c "
from nomoscope_workflow import paramdb; from nomoscope_workflow.config import load_config
with paramdb.connect(load_config()) as conn:
    r = paramdb.load_group_record(conn, '$CC:<policy>:<group>')
    for v in r.values[-2:]: print(v.valid_from, v.valid_to, v.value)")
```

Then read, as context never evidence: the Country Report's *Main policy
changes between 2024-2025* section
(`08 - EUROMOD Triangulator/country-reports/Y16/<CC>_Y16.md`) for parameters
where EUROMOD may be stale, and the *Open points* of
`Nomotheca-RAG/<Country>_sources_analysis.md` for the country's own hazards
(instrument classes not ingested, effect-date quirks, state-vs-total rates).

## 2. Select the entries — the spread is the deliverable

Ten to twelve entries, one per parameter family the JRC would ask about by
name (PIT schedule and bands, minimum wage, main benefit amounts, SIC rates,
credits). Fill this table before writing JSON; a set that cannot fill a row
records *why* in `golden_set_<CC>.md` instead of inventing a case:

| axis | minimum | what it measures |
|---|---|---|
| ladder `verbatim` | 3 | the happy path, and the no-change trap (surrounding values move, this one does not) |
| ladder `combine` | 2 | two provisions or two instruments read together (a coefficient × a base fixed elsewhere) |
| ladder `derive` | 1 | a `$`-referenced value (routes `derived`, value unscored) — and, if any stating act is ingested, one *scorable* arithmetic case |
| ladder `table` | 1 | a full bracket schedule via `group_id`, only if the assembled record is sound |
| routing `changed` | 2 | EUROMOD genuinely stale against the law — found in the CR's policy-changes section, never by relabelling |
| routing `not_found` today | 1 | `corpus_available: false`, `citations: []`, the act named in `note` — the ingest metric |
| routing `national_team_source` | 1 | a family with no legal source, flagged in the curation overlay (§4) |
| hazards | the country's own | `mid_year_change`, `unit_conversion`, `cross_instrument`, `budget_act_window`, `income_year` — each named where it applies; the drafter cannot see the first three |

Tier every entry in its `note` — `EASY` / `MEDIUM` / `HARD` /
`IMPOSSIBLE today` / `IMPOSSIBLE by design` — and for every `HARD` and
`IMPOSSIBLE today` entry write the single change that turns it green
("ingest the annual *nutarimas*", "anchor resolution for `$`-values",
"schedule derivation"). That sentence is what makes a later KPI delta
attributable. `IMPOSSIBLE by design` is the refusal case: correct behaviour is
a `national_team_source` routing, never a proposal.

## 3. Establish each ground truth against the act

For every entry, in the corpus, not from memory or the Country Report:

```bash
docker exec $DB psql -U jrc -d legislation -A -c "
SELECT i.national_id, lu.citation, v.validity, left(regexp_replace(c.content,'\s+',' ','g'),120)
FROM chunks c JOIN unit_texts ut ON ut.id=c.unit_text_id
JOIN legal_unit_versions v ON v.id=ut.version_id JOIN legal_units lu ON lu.id=v.legal_unit_id
JOIN instruments i ON i.id=lu.instrument_id JOIN jurisdictions j ON j.id=i.jurisdiction_id
WHERE j.code='$CC' AND ut.authenticity='authentic' AND v.validity @> DATE '2025-06-01'
  AND c.content ~ '<value as the gazette spells it>';"
```

Zero rows and the act is in §0's list: the value is stated elsewhere (a
regulation, an annex, a different spelling — BOE writes `1184` without a
separator, BWB writes `€ 38.441`). Zero rows and the act is absent: this is
the `corpus_available: false` entry, cite nothing, name the act in `note`.

What each field must satisfy — the full rules are §3 *What makes a good
case* of [review-eval](../review-eval/SKILL.md); the ones that bite at
authoring time:

- **`citations`** spelled exactly as `legal_units.citation` returns it
  (`RD SMI 2025 Artículo 1`, `Wet IB 2001, artikel 2.10`). Matching is
  one-way containment, so anything longer than the corpus form never matches.
  The act's full name goes in `note`.
- **`expected_value`** in EUROMOD's own spelling (`1184#m`, `'37.48%'`,
  `'$EI_Maxpremwag'`), the law's value even where EUROMOD is off by one —
  the difference is the finding, reported to the economists, never absorbed.
  Check the spelling normalises:
  `uv run python -c "from nomokrisis_eval.scoring import normalise_value; print(normalise_value('1184#m'))"`.
- **`routing`** omitted unless the entry pins a trap. A stored value carrying
  `$` owes `derived` with `expected_value: null`. A stated routing that
  contradicts the store *skips* the entry at build time — that skip means the
  selection is wrong, and the fix is the entry, never `dataset/`.
- **`expected_valid_from`** is the fiscal effect date, not the gazette's
  entry-into-force date (ES `fecha_vigencia` 2024-12-22 for a measure "con
  efectos desde el 1 de enero de 2025"). Omit it on an `unchanged` entry —
  the pipeline keeps EUROMOD's window there and the leg is unscored.
- **`difficulty` / `hazards`** only where the drafter would get them wrong:
  `table` for a group, `combine` when the second provision is in the same
  instrument, and every hazard it is blind to. Setting either locks the
  case (`labels_drafted: false`).

## 4. Curation overlay

`Nomoscope-agentic-workflow/pipeline/curation/<CC>.curation.yaml`, three
sections, each a list of rules with a `note` and `targets` — copy
`LT.curation.yaml` (`source_type`) and `FR.curation.yaml`
(`temporal_basis`, `unit`) for the shape:

- `source_type: national_team` — the `IMPOSSIBLE by design` family. Confirm
  in the corpus that nothing states the value before flagging (LT grepped
  `ikimokyklin*` and found only eligibility clauses). The builder warns, and
  the pipeline cannot route the case, until this is applied.
- `temporal_basis` — only when the country assesses year Y on year Y−1
  income (FR). ES and NL are `in_force`; say so in the file's header comment
  and in the selection's `conventions`, so nobody re-derives it.
- `unit` — a rate delivered as `currency`, or a `/100` that is really `/1`:
  the proposal prompt's percent normalisation and the critique's range check
  key on it.

```bash
cd ../Nomoscope-agentic-workflow/pipeline
uv run nomoscope-workflow ingest-params ../../extracted_parameters/enriched/$CC.enriched.json   # once per DB reset
uv run nomoscope-workflow curate-params curation/$CC.curation.yaml     # after EVERY ingest-params; '! not in params DB' = a typo
```

## 5. Write the two files

`golden_sources/<cc>.json` — `"corpus": "curated"`, `country`, `language`
(the legislation's, `es` / `nl`), a `description`, a `conventions` block
stating `temporal_basis`, `expected_value` spelling, the routing semantics
and the source rule (copy LT's wording; they are what a reviewer reads), and
`entries`:

```jsonc
// every field the builder reads; a real entry carries only what applies
{
  "model_target": "euromod://ES/ConstDef_es/def_const/$IPREM",   // or "group_id": "ES:twl_es:twl_schedule"
  "id": "constdef_iprem",                    // case id = <cc>_<id>_<as_of>
  "source_class": "codified_law",            // codified_law | gazette | national_team
  "expected_value": "600#m",                 // null = value leg unscored
  "expected_valid_from": "2025-01-01",       // fiscal effect date; omit on unchanged
  "citations": ["<exactly legal_units.citation>"],
  "corpus_available": true,                  // false + citations [] for the not_found case
  "routing": "derived",                      // only to pin a trap
  "difficulty": "combine", "hazards": ["unit_conversion"],   // only where the drafter is blind
  "note": "MEDIUM — what the law says, where, why this rung, what flips it"
}
```

`golden_set_<CC>.md` — mirror IE/LT section for section: why the country is
built this way, the build procedure, *Prerequisites and gaps* dated today
(translation, group defects, scoring gaps found in §3), the N-cases table
(`# | target | 2025 value | difficulty | expected routing | source`), the
rationale per tier, and *What this fixes in the existing sets' blind spots*.

## 6. Build, read every line, fix at the source

```bash
cd ../../Nomokrisis-evaluation_pipeline
uv run nomokrisis-eval build-curated-dataset --country $CC --year 2025
```

Every `~ skipped` line is a defect in the selection: `contested routing`
(drop `routing:` or fix the value), `parameter not available` (wrong
`model_target` — check the exact name in the store, `$SMI` vs `$SMI2`),
`no routing … cannot be normalised` (state `routing:` for a percent string
or a raw value the scorer refuses). Every `!` warning is read and either
resolved or copied into *Prerequisites and gaps*. Rebuild until zero skips.

Then check the spread and the drafter's labels against §2:

```bash
uv run nomokrisis-eval label-cases --country $CC       # proposals + reasons; '=' rows are yours, locked
uv run nomokrisis-eval list-cases --country $CC
```

A rung with zero cases and no written reason in the `.md` is not done.

## 7. Smoke run and hand-off

```bash
uv run nomokrisis-eval run --as-of 2025-06-01 --model mock/extractor --country $CC --include-drafts --no-db
uv run nomokrisis-eval report --run-id <run-id>
```

The mock cannot read law; what this proves is that every case loads, its
parameter file materializes, the `derived` and `national_team_source` cases
route without an LLM, and `report` prints the readiness split
(`N source not in corpus`) you intended.

Report to the user: the spread table filled in, the gaps recorded, the
defects found on the EUROMOD side (an off-by-one, a mislabelled unit — these
go to the economists team, not into the ground truth), and the list of case
ids awaiting `nomokrisis-eval verify <id> --reviewer <name>` or the UI's
Golden set tab. Cases stay `verified: false` until then, and `run` drops them
by default.
