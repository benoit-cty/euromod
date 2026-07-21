# Using OpenFisca Parameter Corpora in the Assisted-Update Pipeline

*Reflection note — companion to [08_schema-proposal-for-validation.md](08_schema-proposal-for-validation.md).*

## 1. What OpenFisca-France offers

OpenFisca-France maintains a human-curated database of French tax-benefit
parameters as YAML files (`openfisca_france/parameters/**.yaml`): **4,012
parameter files, ~2,500 of them carrying legal references**. One file, e.g.
`impot_revenu/bareme_ir_depuis_1945/bareme.yaml`, contains:

- the full value history (the income-tax scale back to 1945), as date-keyed
  scalars or bracket structures;
- per-date `metadata.reference` entries: `{title: "Loi 63-1241 du 19/12/1963
  (LF pour 1964)", href: "https://www.legifrance.gouv.fr/...JORFTEXT000000875392"}`;
- per-date `official_journal_date`;
- `description` and `short_label` written in the law's own language (French),
  sometimes an English label;
- units (`rate_unit`, `threshold_unit`) and curated historical notes.

Two properties make this directly useful:

1. **The reference hrefs embed `LEGIARTI`/`JORFTEXT` identifiers** — the same
   national ids the legislation database keys on (`legal_units.national_id`)
   and that the retrieval citation fast path matches directly.
2. **The file format is defined by openfisca-core, not by the France
   package.** Every OpenFisca country package (and the PolicyEngine forks for
   UK/US/CA) uses the same `values:/brackets:/metadata:` layout. A single
   ingester covers all of them.

Coverage varies by pilot member state: France is excellent; Spain and Belgium
packages exist but are thinner; Ireland and Lithuania have none. OpenFisca is
therefore an **optional per-country enrichment, never a dependency** — the
same philosophy as the ingest country adapters.

## 2. Storage: ingest first, match later

The key design decision: **storage does not require a mapping to EUROMOD.**
The corpus is ingested under its own identity (its dotted path, e.g.
`impot_revenu.bareme_ir_depuis_1945.bareme`); linking to EUROMOD parameters is
a separate, sparse, later step. Implemented tables in the `params` schema
(loaded with `nomoscope-workflow ingest-openfisca`; for France: 2,836 external
parameters, 19,391 value points, 16,788 references at commit-pinned state):

- `external_corpora` — one row per source:
  `(kind='openfisca', country, repo_url, commit, license)`. Pinning the git
  commit keeps every downstream use reproducible, like the eval golden set.
- `external_parameters` — `(corpus_id, path, description, short_label, unit,
  metadata jsonb)`, keyed by the corpus-native path.
- `external_values` — the date-keyed history, one row per
  `(external_parameter_id, valid_from)`, with scalar and bracket forms.
- `external_references` — per-date `{title, href, national_id, official_journal_date}`,
  with the `LEGIARTI`/`JORFTEXT` id parsed out of the href at ingest time.
- `parameter_links` — the EUROMOD mapping, **initially empty**:
  `(parameter_id → params.parameters, external_parameter_id, match_method,
  score, validated_by, validated_at)`.

An unmatched external parameter is the normal state, not an error. The corpus
is useful even before any link exists (e.g. as a browsable reference in the
UI, and as a source of native-language vocabulary).

## 3. The matching problem, honestly

There is **no shared key** between `euromod://FR/tinkt_fr/def_const/$tin_upthres1`
and `impot_revenu.bareme_ir_depuis_1945.bareme`. Names, granularity and
structure all differ (EUROMOD stores the scale as ten separate scalar
constants; OpenFisca stores one bracket object). Any automated matching can
only produce **suggestions**; a human validates them in the UI, exactly like
the `parameter_group` mappings in the format proposal. `match_method` and
`score` are recorded so a bad heuristic can be rolled back wholesale.

Candidate signals, in order of trustworthiness:

1. **Value-fingerprint matching (deterministic, strongest).** Both sides hold
   multi-year numeric histories. `$tin_upthres1` = 10,777 / 11,294 / 11,496
   for 2023/2024/2025; the OpenFisca scale's second threshold holds nearly the
   same series. Matching = same value in a majority of overlapping years,
   within a tolerance — *not* exact equality, because the divergences are
   precisely what the pipeline exists to surface (EUROMOD has 11,496 where the
   law says 11,497). A ≥3-year fingerprint match is close to conclusive; the
   same signal generalises to any country with no language dependence.
2. **Structural compatibility (deterministic filter).** Units must be
   compatible (`/1` rate ↔ `rate_unit: /1`; currency/year ↔
   `currency_next_year`), bracket-group shape must fit (5 thresholds + 6 rates
   ↔ a 5-bracket scale), COICOP codes narrow consumption-tax parameters.
3. **Multilingual embedding similarity** between EUROMOD descriptions and
   OpenFisca descriptions (BGE-M3 is already in the stack and is
   cross-lingual, so English EUROMOD text scores against French OpenFisca text
   without translation). Good for ranking candidates, not for deciding.
4. **LLM adjudication of the top-k candidates** produced by 1–3, with the
   verdict stored as a suggestion (`match_method='llm_suggested'`), never
   auto-validated.

Realistic expectation: fingerprints + structure alone should link the
high-value numeric parameters (schedules, thresholds, rates with several years
of history); text similarity mops up part of the rest; a tail stays unmatched
and that is acceptable.

## 4. What a validated link buys the pipeline

1. **Retrieval hints — the biggest win.** Today `frame` derives citations from
   previous `values[].references`, which are empty in the whole FR export. A
   linked parameter contributes the OpenFisca reference titles and parsed
   `LEGIARTI`/`JORFTEXT` ids for dates near `as_of` to the citation fast path,
   and tells `nomotheca-ingest` exactly which instruments to fetch on a cache
   miss. This attacks the hardest problem — *finding the right article* — with
   human-curated pointers.
2. **Cross-validation in critique — corroboration, never evidence.** A
   deterministic check compares the proposal against the linked OpenFisca
   value at `as_of`: agreement is noted on the critique report; disagreement
   becomes an issue for the reviewer ("OpenFisca has 11,497 from 2025-01-01").
   The verbatim-extract anti-hallucination rule is untouched: OpenFisca is a
   curated *secondary* source and can never serve as the `supporting_extract`
   for a legislation-sourced proposal. (`Lineage.proposed_by` already includes
   `"openfisca"` for values that originate there.)
3. **Golden-set expansion (Activity 4).** Per-date values + official-journal
   dates + citations are human-curated `(value, effective date, reference)`
   triples — candidate `expected` blocks for eval cases, generated cheaply and
   confirmed by a human.
4. **Native-language parameter text for free.** OpenFisca descriptions are
   human-written in the law's language — better than any machine translation
   for the search problem below.

## 5. Native-language search text (implemented)

The enriched EUROMOD export carries English-only labels and descriptions,
while the legislation chunks are indexed with language-specific FTS (`fts_fr`
for France). The vector leg of hybrid retrieval is multilingual (BGE-M3), but
the full-text leg was effectively crippled cross-language.

The fix, implemented in the workflow package:

- `params.parameter_texts` stores derived renderings of `label` /
  `short_label` / `description` per language, with provenance
  (`origin: machine_translation | openfisca | manual`, plus the engine used).
  Received Stage A jsonb fields stay untouched — translations are Stage B
  enrichment, marked as such.
- `nomoscope-workflow translate-params` machine-translates the English texts
  into the law language (batched, provider-agnostic via the shared `llm.py`).
- `frame` prefers the law-language text when present for the retrieval query,
  keeping the received text as a secondary signal. No translation, no DB —
  behaviour is unchanged.

Where a validated OpenFisca link exists, its human-written description should
replace the machine translation (`origin='openfisca'` wins over
`origin='machine_translation'`).

## 6. Caveats

- **License:** openfisca-france is AGPL-3.0. Using the data as a reference
  input and storing derived rows is fine for the prototype; flag it in the
  contract documentation before any redistribution.
- **OpenFisca is not the law.** It is curated and occasionally wrong or
  lagging; that is why it corroborates but never evidences.
- **Mappings decay.** Both sides evolve; `parameter_links` carries the corpus
  commit so a re-ingest can flag links whose external side changed.

## 7. Suggested build order

1. ~~`parameter_texts` + law-language query in `frame`~~ — done (see §5).
2. ~~`ingest-openfisca` CLI walking a country package's YAML tree into the
   `external_*` tables (no matching required)~~ — done. Note for the matcher:
   OpenFisca dates income-tax parameters by income year while EUROMOD dates by
   system year, so fingerprint matching must tolerate a ±1-year offset.
3. Fingerprint + structure matcher producing `parameter_links` suggestions;
   validation affordance in the UI.
4. Citation hints in `frame` from validated links; critique cross-check;
   golden-set generation.
