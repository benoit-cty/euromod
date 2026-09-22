---
name: review-eval
description: Review a Nomokrisis evaluation run and improve the golden set behind it — separate real model failures from scoring artifacts, corpus gaps and mislabelled ground truth, then fix the golden selections in the database. Use when asked to review, interpret or sanity-check eval results ("is the eval correct?", "why is the score so low?", "did the model really fail these?"), or to add/repair golden cases.
argument-hint: [run-id]
---

# Review an evaluation run, and improve the golden set

A low KPI is a claim about the model. Before repeating it, prove the number is
about the model at all. In this pipeline four other things produce the same
low number: a scoring rule comparing incommensurable quantities, a golden case
whose ground truth is wrong, a source act that is not in the corpus, and a
defect in the parameter under test. Each has a different owner and a different
fix.

**Never report a headline rate without saying which of the five it measures.**

## 0. Orient

```bash
cd Nomokrisis-evaluation_pipeline
uv run nomokrisis-eval list-runs            # run ids, model, done/total, status
uv run nomokrisis-eval report --run-id <run-id>
```

A run lives in the database alone (ADR 0004) — there is no run directory,
no `manifest.json`, `cases.json`, `results.json` or `queue/`. Everything a
review needs is in four places:

| where | what it is |
|---|---|
| `eval.runs` | the manifest: `model`, **`critique_model`**, **`resolved_model` / `resolved_critique_model`** (what the provider layer actually called), prompt/agent/eval versions, `dataset_version` (the golden set hash), `as_of`, `status`, `submitted_by`, `notes` (`smoke` = ignore) |
| `eval.run_cases` | the golden cases **frozen at run start** (`"case"` jsonb) — the expectations actually used |
| `eval.results` | one scored `CaseResult` per case: the KPI columns, `details` (the full dump), `phoenix_trace_id` |
| `eval.results.review_item` | the full `ReviewItem` (jsonb): proposal, references, critique, scout, retrieval trace |

The KPI columns alone cannot tell you *why* anything scored as it did. The
answer is nearly always in the matching `review_item` — read it.

**One loader for every snippet below.** Save it once as `/tmp/eval_run.py`;
each snippet starts with `from eval_run import load_run` and runs from
`Nomokrisis-evaluation_pipeline/` as `PYTHONPATH=/tmp uv run python - <<'PY'`:

```python
# /tmp/eval_run.py — a run's manifest, frozen cases, results and review items, from the DB
from nomokrisis_eval import db as evaldb
from nomokrisis_eval.config import load_eval_config


def load_run(run_id: str):
    """(manifest, cases, results, items).

    manifest: RunManifest (attributes: model, critique_model, resolved_model, ...)
    cases:    {case_id: dict}  eval.run_cases  — the frozen GoldenCase, with `expected`
    results:  {case_id: dict}  eval.results    — the scored CaseResult
    items:    {case_id: dict}  eval.results.review_item — the ReviewItem (None-free)
    """
    conn = evaldb.connect(load_eval_config().database_url)
    loaded = evaldb.load_run(conn, run_id)
    if loaded is None:
        raise SystemExit(f"no run {run_id} in eval.runs — `nomokrisis-eval list-runs`")
    run_pk, manifest = loaded
    cases = {c.id: c.model_dump(mode="json") for c in evaldb.load_run_cases(conn, run_pk)}
    results = {r.case_id: r.model_dump(mode="json") for r in evaldb.load_results(conn, run_pk)}
    items = evaldb.load_review_items(conn, run_pk)
    return manifest, cases, results, items
```

The same rows straight from psql, when one field is all you need:

```bash
DB=$(docker compose -f ../docker-compose.yml ps -q db)
docker exec $DB psql -U jrc -d legislation -A -c "
SELECT res.case_id, res.routing_actual, res.routing_correct, res.value_correct, res.citation_correct,
       jsonb_pretty(res.review_item->'critique')
FROM eval.results res JOIN eval.runs r ON r.id=res.run_pk WHERE r.run_id='<run-id>' AND res.case_id='<case-id>';"
```

### Before comparing two runs: prove they ran two models

A comparison is only about the models if the two runs reached two models.
`eval.runs.model` is what was *asked for*; Phoenix records what was *called*.
For `azure_openai/<name>` the name is the deployment, and until 8 Sep 2026
`AZURE_OPENAI_DEPLOYMENT` in `.env` overrode it — so a "Sol vs Luna" pair,
judge included, was Luna vs Luna, and every `azure_openai/*` run since
5 Aug 2026 (terra, nano-2, Mistral-Large-3, DeepSeek-V4-Flash, sol) is the
same. The differences between such runs are sampling noise at temperature
0.2, and reading behaviour into them ("Sol refuses more") is exactly the
mistake that was made. Check both runs before anything else:

```bash
docker exec $DB psql -U jrc -d legislation -A -c "
SELECT run_id, model, resolved_model, critique_model, resolved_critique_model, notes
FROM eval.runs WHERE run_id IN ('<run-a>', '<run-b>');"
```

Then confirm against the traces — every result carries `phoenix_trace_id`
(the same id is on the review item), and the two databases share one server:

```bash
docker exec $DB psql -U jrc -d legislation -A -t -c "
SELECT string_agg(quote_literal(res.phoenix_trace_id), ',') FROM eval.results res
JOIN eval.runs r ON r.id=res.run_pk WHERE r.run_id='<run-id>' AND res.phoenix_trace_id IS NOT NULL;"
docker exec $DB psql -U jrc -d phoenix -A -c "
SELECT s.attributes->'llm'->>'model_name', count(*) FROM spans s JOIN traces t ON t.id=s.trace_rowid
WHERE s.span_kind='LLM' AND t.trace_id IN (<the list above>) GROUP BY 1;"
```

One model name across both runs means there is nothing to compare. Runs
stored before the `resolved_*` columns existed have them NULL; for those only
Phoenix can tell.

## 1. The five explanations, in the order that costs least to check

Work top-down. Each step removes cases from the pool before you judge the model.

### a. Scoring artifact — is the KPI comparing like with like?

The trap that already bit once: **`date_correct` on an `unchanged` verdict.**
`pipeline._unchanged_window` deliberately keeps the validity window EUROMOD
already holds, while the golden `valid_from` is the date the *law* took effect.
Those are different quantities; comparing them scored correct no-change
verdicts as date errors on 22 of 26 FR cases. `scoring.score_item` now leaves
the leg unscored when both sides route `unchanged`.

Generalise the check. For every KPI that looks bad, ask what the pipeline
*emits* in that field versus what the golden set *records*, and read both
definitions rather than assuming they match:

```bash
PYTHONPATH=/tmp uv run python - <<'PY'
import collections
from eval_run import load_run
manifest, cases, results, items = load_run("<run-id>")
counts = collections.Counter()
for case_id, r in results.items():
    if r["date_correct"] is False:
        item = items.get(case_id) or {}
        prop = (item.get("proposed_value") or {}).get("valid_from")
        counts[(cases[case_id]["expected"].get("valid_from"), prop, r["routing_actual"])] += 1
for k, n in counts.most_common():
    print(f"  expected={k[0]}  proposed={k[1]}  routing={k[2]}  n={n}")
PY
```

A single (expected, proposed) pair repeating across many cases is a systematic
mismatch, not a model that is wrong the same way ten times.

**The same trap, second instance: the evidence legs on a `derived` verdict.**
`pipeline._derived_refs` short-circuits any parameter whose stored value carries
a `$`-reference straight to `Routing.DERIVED`, *before* retrieval and before any
LLM call — `$PSS * 4` has no independent legislative existence, so the anchor is
what legislation sets. There is therefore deliberately no proposal, no citation
and an empty retrieval trace, and scoring those as misses penalises the pipeline
for behaving correctly. `score_item` leaves `citation_correct` and
`retrieval_hit` unscored when both sides route `derived`; one side alone still
scores them, because then the routing is in dispute and the evidence settles it.

Two more scoring rules worth knowing:

- **`hallucination` is the mechanical leg only** — the extract is not verbatim
  in the cited chunk. A critique that failed on dates or units is *not* a
  hallucination; that is `critique_pass`.
- **`supportedness` is LLM-assisted** (`citation_verified` = the verbatim check
  AND the critique model's `citation_supports_value`). If `manifest.critique_model`
  equals the model under test, the model graded itself — never compare that
  column across models. Pin a judge with `EVAL_CRITIQUE_MODEL` first.

**Retrieval: read the framed query before blaming the corpus.** The frame step
builds the query from the parameter's label and description, which the
enrichment wrote for EUROMOD readers: Country Report table references, EUROMOD
function names and identifiers, and the export's own — often stale or wrong —
value («fixé à 11 496 EUR pour le revenu imposable 2025»). In an OR-of-terms
FTS leg every such token pulls unrelated chunks; on the FR barème thresholds
CGI art. 197 sat at rank 22 of 60 and no threshold case could be answered.
`pipeline._clean_query_text` now strips parentheticals, «quoted» titles and
`_identifiers`/`$refs` — not numbers: the export's value is usually still the
law's and "11,88" is what finds the SMIC arrêté — which moved it to rank 8 and,
measured offline over the 39 ready FR cases with a golden citation, raised
golden-citation recall at k=15 from 31 to 34 with no case lost. The Phoenix `frame` span shows
the query a run used; re-run `retrieval.retrieve` with it at a larger k to see
where the golden article ranks before concluding it is missing.

**Third instance: a bare proposal against a golden value with a period.**
Proposals are floats on the parameter's own basis; the golden `747#m` for a
parameter EUROMOD holds as `8964#y` could never compare until `score_item`
started completing the proposal with the stored value's suffix. If a value leg
fails on a `#m`/`#y` golden spelling, check the stored raw value's suffix first.

**Readiness lies when the resolving citation is not the value-bearing one.**
The four CSG threshold cases resolved CSS art. L136-8 (OpenFisca's own title:
«seuils avant revalorisation») and scored as model failures for a year whose
amounts live in a ministerial letter with no Legifrance id. `readiness` is
derived from the reference list: a reference OpenFisca marks as pre-indexation
no longer counts, and a selection entry can set `corpus_available` explicitly.
Before blaming a model for a value, ask whether ANY ingested text states it.

**A version gap is a corpus gap the readiness flag cannot see.** An article can
be ingested and still absent at the as-of date — CSS D242-4 had versions to
2023-12-31 and from 2026-01-01, nothing in between, so the as-of filter could
never return it; SWCA 2005 s. 13 stops in 2022 (enacted text only); LIRPF DA 61
starts after the as-of date. Check `legal_unit_versions.validity` around the
as-of date, and the stored DILA JSON's `VERSIONS` block lists the sibling
LEGIARTI ids to ingest.

### b. Corpus gap — could any model have answered?

First check whether it is really a gap. The gap-fill scout records what the
proposal said it was missing and what it did about it, on every review item:

```bash
docker exec $DB psql -U jrc -d legislation -A -t -c "
SELECT jsonb_pretty(res.review_item->'scout') FROM eval.results res JOIN eval.runs r ON r.id=res.run_pk
WHERE r.run_id='<run-id>' AND res.case_id='<case-id>';"
```

`needs` is the analyst's own account of the missing document, `ingested` is what
the scout fetched, `located` the citations the corpus lookup found for those
needs without fetching anything. **Read `errors` first**: `432` on every
Tavily call means the plan quota is spent and the web leg ran blind for the
whole run (both 2026-09-09 runs) — a "corpus gap" then measures nothing.

**A refusal that names an act we hold is a ranking miss, not a gap.** On the
2026-09-09 pair, six of nine `retrieval_hit=False` misses named acts already
ingested (LIRPF art. 66 was not in the top 60 for its framed query); the
`locate` step now looks named articles up directly. Re-run
`retrieval.locate_named_units` with the item's `scout.needs` before ingesting
anything. **A refusal "cannot be supplied by calculation" is now answerable**
when every operand is stated by an extract (NL `$bfa_mult2`, `$chall_b2`):
the proposal may carry a `derivation`, mechanically checked; a refusal of that
kind after prompt 0.8.0 is a model choice, not a rule. `needs` set but `ingested` empty means one of: the act is not
findable on the country's official domains, the country has no
`scout.COUNTRY_SOURCES` entry, or — check this one — **the act is in the corpus
and retrieval simply did not surface it**, which is a retrieval problem wearing a
corpus problem's clothes. Confirm against the DB before believing either:

```bash
docker exec nomotheca-legislation-db psql -U jrc -d legislation -c \
  "SELECT national_id, left(title::text,80) FROM instruments WHERE title::text ILIKE '%<words from needs>%';"
```


If no ground-truth reference resolves in the legislation corpus, the text
stating the value was never retrievable and the case measures ingest breadth.

This is one of two **readiness** states — reasons a case cannot measure a model
at all, both properties of the golden set rather than of the model:

| `GoldenCase.readiness` | meaning | how you close it |
|---|---|---|
| `no_corpus` | `corpus_available: false` — the act is not ingested | ingest the act |
| `undocumented` | no ground-truth citation was ever recorded, so `retrieval_hit` is unscorable and nobody established where the answer lives | find the provision, add the citation |
| `ready` | neither | — |

`report` and the console summary both print the split, and every rate is
recomputed over the ready cases alone:

```bash
uv run nomokrisis-eval report --run-id <run-id>   # "not ready (N source not in corpus, M no ground-truth citation)"
```

The first run reviewed this way split hard: **73% routing / 73% value on the 45
cases whose act was ingested, 11% / 11% on the 18 where it was not** — against a
54%/52% headline. Report both numbers or neither.

Measured on that run, citation count and corpus availability turned out to be
the *same* population (18/18 and 34/34), and it was by far the strongest signal
in the data — 14% routing at zero citations, 65% at one, 80% at two. Before
concluding anything about a model, check that you are not looking at this.

#### Difficulty and hazards: the breakdown that explains a headline

Once the unready cases are out, `report` splits the rest two ways. Both are
assigned from the ground truth, **never** from a run's outcome — a ladder fitted
to outcomes reports that the hard cases are the ones we got wrong.

`difficulty`, ordered by the work the parameter demands (highest applicable wins):
`verbatim` (the value is literally in one provision) · `combine` (two or more
provisions) · `derive` (arithmetic: a formula, a `$`-constant, a weighted
average, a period conversion) · `table` (a full bracket schedule).

`hazards`, orthogonal flags that compose — a `verbatim` case can still be an
income-year case: `income_year` · `mid_year_change` · `budget_act_window` ·
`cross_instrument` · `unit_conversion`.

```bash
uv run nomokrisis-eval label-cases              # proposals + reasons, writes nothing
uv run nomokrisis-eval label-cases --apply      # writes difficulty/hazards only
```

`label-cases` drafts from the expected value, the citations and the parameter's
`temporal_basis`. It is blind to `mid_year_change`, `unit_conversion` and
`budget_act_window` — those need a human. It also refuses to touch a case whose
label a human set in the selection (`labels_drafted: false`), because the
drafter sees less than a reviewer does: once a case is materialized it cannot
tell a bracket group from a scalar.

Beware the trap the old field fell into. `difficulty` used to be assigned as
`"table" if brackets else "plain"` in three builders, which measured "is this a
bracket schedule" — 58 of 67 cases in one bucket, separating nothing (plain 53%
vs combine 50%). If a breakdown shows every bucket scoring alike, suspect the
labels before you conclude the axis does not matter.

### c. Mislabelled ground truth — is `expected` what a correct pipeline owes?

The recurring failure is **routing semantics**. The pipeline's routing answers
*"does the proposal differ from the value EUROMOD currently holds?"* — not *"did
the law change this year?"*. The system-year N export already encodes the law of
year N, so a parameter the legislature changed for N and that EUROMOD already
carries routes `unchanged`. Nine IE/LT cases were labelled `changed` on the
other reading and scored as model failures.

`curated_golden.draft_case` now **skips** an entry whose stated `routing:`
contradicts `route_against_current`, instead of warning. If you see that skip,
the selection is wrong — fix the entry (§3: export, edit, import, rebuild),
never the case row in `eval.golden_cases`.

**A `$`-formula parameter owes `derived`, not `unchanged`.** The cross-check
above cannot catch this: `route_against_current` only asks whether the proposal
differs from the stored value, and knows nothing about the short-circuit. Two
cases were written expecting `unchanged` for `$PSS * 4` and `100%*$MMS`, and the
run scored a correct `derived` verdict as a model failure. If the stored value
contains a `$`, the entry wants `routing: derived` and `expected_value: null` —
the value leg is not scorable, and what the case tests is that the pipeline
recognises the formula instead of hunting the corpus for a number that is not in
it.

Check the drafting warnings that did survive:

```bash
docker exec $DB psql -U jrc -d legislation -A -c "
SELECT id, verified, left(part, 140) FROM eval.golden_cases,
     unnest(string_to_array(\"case\"->>'notes', ' | ')) AS part
WHERE part LIKE 'drafting warning%' ORDER BY id;"
```

A `verified: true` case carrying a drafting warning is the dangerous
combination: the drafter doubted it and a human waved it through anyway.

**Income-year cases: a consolidated code article in force on the retrieval
date is evidence, whatever its version start.** France assesses income year Y
in Y+1, so the code article as consolidated on 1 July Y+1 is the text that
assessment applies: CGI art. 197 «en vigueur du 16 février 2025 au 21 février
2026» is the 2024-income barème, and art. 223 sexies has read the same since
2018 because the CEHR thresholds never moved. The critique used to treat any
version older than the budget-act window as "probably last year's value" and
demand a finance-act clause naming Y — which rejected four correct CEHR
proposals in one run (`the cited article never names income year 2024, but
(JORFTEXT000048727345, …) does`). `pipeline._consolidated_in_force` now grants
the presumption when the cited text is a `code` instrument whose version
contains the retrieval date and whose corpus snapshot is at least that fresh,
unless its application note names the *next* income year (the CDHR). If you
still see that rejection on an unchanged value, check the snapshot date of the
cited version (`fetch_snapshots.retrieved_at`) before anything else. The NOTA
application notes are ingested since 8 Sep 2026 (`cli reparse`), so a
year-naming clause may now sit at the end of the consolidated article itself.

**Income-year cases: check the year the prompt states before blaming the model.**
`schema.income_year_for` is the single place the system-year → income-year
mapping is decided (offset −1), and CLAUDE.md forbids re-deriving `as_of.year ± 1`
at a call site. Two call sites did it anyway — `prompts._parameter_block` and the
cross-article proof — so the model was told the 2025 barème governs 2025 income
and asked to find a year the act never names, while the mechanical check next
door demanded the 2024 date off the correct mapping. Sixteen FR refusals in one
run, six of them with the right article retrieved. Grep before you conclude:

```bash
grep -rn "as_of.year" src/nomoscope_workflow/   # every hit outside item_id/system_year is suspect
```

### d. Input defect — is the parameter under test itself sound?

`$Minwage_hourly` carries unit `currency/month` and the raw value `11.88#m`
although 11.88 is the *hourly* SMIC. A correct model finds "11,88 euros par
heure" and refuses to present it as monthly — scoring `not_found` for a reason
that is neither the model's nor the corpus's. `unit` comes from the read-only
EUROMOD export, but the curation overlay can override it
(`curation/<CC>.curation.yaml`, `unit:` rules, re-applied after every
`ingest-params`): the FR export labelled all 146 `*rate*` parameters
`currency` (IE 48 and LT 54 rate-like parameters too, curated the same way —
membership by value, never by name), and under that unit the proposal prompt never normalises "11 %" to
0.11 and the critique's `values_sane` either refuses the fraction or skips its
range check — one model refused the barème's 0 % band as "a currency amount",
another had every rate it proposed rejected. Curate the unit and re-apply
`curate-params`: a run loads the parameter from the store by the case's
`parameter_target` at run time, so the curated unit reaches the next run
without a rebuild. Rebuild the country's cases anyway when the selection's
routing cross-check or the "value EUROMOD holds" note depended on it (the
human verdicts survive while the ground truth is unchanged), and still report
the defect to the economists team, as the set already does for
`$Minwage_hourly`, the FR barème 1-€ erratum and IE's 27 382/27 383. What
cannot be curated (a wrong value, a mislabelled period) goes in the selection
entry's `note`.

**The critique verdict gates routing and value.** `pipeline.diff` routes on the
value alone, so a proposal the critique rejected still lands as `unchanged` when
it echoes the stored value; `score_item` marks such a case `rejected` and scores
routing/value/date False. Before that rule one model gained eight "correct"
verdicts on a 66-case run — four of them the barème's stale value with a
citation the critique had refused, one with a mistyped chunk id on all four
attempts — and came out ahead of a model that had refused instead. The console
summary prints `rejected=N` next to `abstained`; a large N with a high routing
rate on the *other* model is that artifact.

**The store, not the export, is what the run saw.** Compare
`params.parameters.ingested_at` with the export's commit date before reading a
unit defect into a run: FR/IE/LT ran for a month on the August export after the
September one changed `$PensionAgeFemale` to `age_years`. Percent literals
(`8.17%`) are scalars in the store since 8 Sep 2026; a `null` current value on a
rate parameter means an older ingest. A bracket-schedule group runs with a
composed label — a frame query of `LT` or `ES Tax schedule` means it did not.

**A rejected proposal with the right value is worth a look.** `citation_chunk_id
missing or not among retrieved chunks` twice on the same case was a one-hex-digit
transcription of the retrieved id; the critique now resolves the id from the
extract when exactly one retrieved chunk contains it. If you still see it, the
extract was in no retrieved chunk at all — a real failure.

### e. Model failure — what is left

Only now read the proposals. For refusals, the reason is in the critique:

```bash
PYTHONPATH=/tmp uv run python - <<'PY'
from eval_run import load_run
manifest, cases, results, items = load_run("<run-id>")
for case_id, r in results.items():
    if r["routing_actual"] != "not_found" or case_id not in items:
        continue
    critique = items[case_id].get("critique") or {}
    reasons = [i for i in critique.get("issues", []) if i.startswith("model:")]
    print(f"--- {case_id}  retrieval_hit={r['retrieval_hit']}")
    print("   ", (reasons[0] if reasons else str(critique.get("issues")))[:300])
PY
```

Read them, do not count them. A well-argued refusal ("the extract states an
hourly rate, the parameter declares monthly") is correct behaviour that costs
three KPIs — that is what `abstained` is for. A refusal with
`retrieval_hit: true` is the interesting one: the right document was retrieved
and the model still would not commit.

Cross-check a wrong value against the citation it used. A confident wrong answer
is usually the corpus offering a near-miss — three FR `bch00` "false alarms"
came from the only ingested arrêté stating a Saint-Pierre-et-Miquelon ceiling,
the metropolitan value living in a *circulaire* with no Legifrance id.

## 2. Re-score instead of re-running

After changing `scoring.py`, apply it to past runs for free — no LLM calls:

```bash
uv run nomokrisis-eval rescore <run-id>            # dry run: prints the KPI delta
uv run nomokrisis-eval rescore <run-id> --write    # persist into eval.results (review_item kept)
```

It replays the run's stored `ReviewItem`s (`eval.results.review_item`) against
the run's **frozen** cases (`eval.run_cases`), so what you see is the effect of
the scoring change alone. To measure a golden-set change, start a new run:

```bash
uv run nomokrisis-eval run --as-of 2025-06-01 --model <provider/model> --country FR
uv run nomokrisis-eval run --as-of 2025-06-01 --model mock/extractor --country FR --include-drafts --notes smoke   # loads every case, no LLM
```

A run can equally be submitted to the worker, which holds the keys and the GPU:
`nomergon submit eval --payload '{"as_of": "2025-06-01", "model": "<provider/model>", "countries": ["FR"]}'`
(`{"resume": "<run_id>"}` continues one). Either way it lands in `eval.runs`;
a smoke run is not deleted, its `notes` say `smoke`.

## 3. Improving the golden set

Cases are **generated**, never hand-written. The selection behind a country's
cases is one row, `eval.golden_selections (country, kind, header, entries)` —
`kind` is `openfisca` (FR) or `curated` (IE, LT, ES, NL) — edited as the JSON
file it used to be, then written back and rebuilt:

```bash
uv run nomokrisis-eval selections                                   # every row: country, kind, entries, updated_at/by
uv run nomokrisis-eval selection-export IE --out /tmp/ie.json       # --kind curated|openfisca when a country has both
#   ... edit /tmp/ie.json (header keys + "entries": [...]) ...
uv run nomokrisis-eval selection-import /tmp/ie.json                # country/kind read from its header; prints the entry count
uv run nomokrisis-eval build-curated-dataset  --year 2025 --country IE
uv run nomokrisis-eval build-openfisca-dataset --year 2025 --country FR   # for the openfisca kind
```

Never UPDATE a row of `eval.golden_cases` by hand — the next rebuild
overwrites it, and the verdict columns are the reviewer's. (There is no
`dataset/` directory any more; `import-golden` was the one-off migration.)
The `golden_set_<CC>.md` narratives stay in git as the rationale documents;
update the one for the country when the selection changes.

To read the cases as they stand: `nomokrisis-eval list-cases --country IE`,
or the rows — `"case"` is the GoldenCase minus the verdict, the verdict is in
`verified` / `reviewed_by` / `reviewed_at` / `review_note`, and the parameter
under test is `"case"->>'parameter_target'` (`euromod://…` or `group:<group_id>`,
loaded from the params DB at run time — there is no `parameter_file`):

```bash
docker exec $DB psql -U jrc -d legislation -A -c "
SELECT id, verified, reviewed_by, \"case\"->>'parameter_target', \"case\"->'expected'->>'routing', \"case\"->'expected'->>'value'
FROM eval.golden_cases WHERE country='IE' ORDER BY id;"
```

A rebuild **keeps the human verdict when the ground truth is unchanged** and
resets it to `verified: false` when `expected`, `parameter_target` or `as_of`
moved (`golden_store.save_drafted_case`). A reset is printed; act on it, because
`nomokrisis-eval run` is `--verified-only` by default and silently drops
unverified cases from the next run.

### What makes a good case

- **State the routing the pipeline owes**, per §1c. Better still, omit
  `routing:` and let `route_against_current` derive it; state it only where the
  stored value cannot be normalised (percent strings) or the case pins a trap
  (`derived`, `national_team_source`).
- **Set `corpus_available: false`** when the act is not ingested, so the case
  scores ingest coverage instead of poisoning the quality headline. It stays a
  useful case — it is how ingest progress becomes a KPI delta.
- **Give citations only for acts the corpus holds.** An instrument-level id of
  an act we do not have is provenance, not ground truth: scoring against it
  manufactures a permanent miss. `openfisca_golden` keeps `JORFTEXT`/`LEGITEXT`
  ids (a correct pipeline citation contains them) and drops article-level ids of
  acts we lack.
- **List every citation a correct pipeline may produce.** `citation_correct`
  and `retrieval_hit` accept ANY listed citation, so a golden set that names
  only the finance act scores the consolidated code article as a miss (and vice
  versa); name both, and the act stating the amount next to the by-reference
  rule (`Ley IMV art. 13` + `RDL 1/2025 art. 65`). Say in `note` why each is
  acceptable.
- **Write the citation exactly as `legal_units.citation` spells it.**
  `citation_matches` is one-way containment, so a golden citation carrying more
  than the corpus does can never match. LT scored **citation 0% and recall 0%**
  on a whole run while the pipeline had cited the right article in four of seven
  cases, purely because the selection wrote `GPMĮ IX-1007, 20 straipsnis`
  where the corpus — and so the pipeline — writes `GPMĮ 20 straipsnis`. Check a
  new citation against the DB before relying on it:
  ```bash
  docker exec $(docker compose ps -q db) psql -U jrc -d legislation -t -A -c \
    "SELECT citation FROM legal_units WHERE citation ILIKE '%<act>%' LIMIT 10;"
  ```
  The act's full name belongs in `note`, not in `citations`.
- **Keep the value in EUROMOD's own spelling.** `normalise_value` reads
  `11496#y`, `$PSS * 4`, `(1766.92*10+1801.80*2)/12#m` and percent literals
  (`'4.1%'` -> 0.041, so it compares against the unit-/1 form OpenFisca uses).
  What it still refuses: multiplicative unit suffixes (`×1000`) and anything
  else that is not a scalar — those fall back to strict equality, which silently
  turns the value leg into a string comparison. Check a new spelling against
  `normalise_value` before relying on it.
- **Say why in `note:`.** It lands in the case's `notes` and is what a reviewer
  reads at the verification gate. Difficulty tiers ("EASY / HARD / IMPOSSIBLE
  today") are how the IE and LT sets make future improvements legible.
- **Correct a difficulty label in the selection, not the case row.** Set
  `difficulty` / `hazards` on the entry (export, edit, import): the builders
  prefer an explicit entry value over anything drafted, mark the case
  `labels_drafted: false`, and a rebuild will not undo you. Updating the case
  row in `eval.golden_cases` loses the change on the next build.
- **Aim for spread across the ladder.** A set that is all `verbatim` cannot show
  whether the pipeline can combine provisions. `derive` is the rung to watch:
  every formula-valued parameter in the store is currently either `$`-referenced
  (short-circuited to `derived`, so it never exercises reading-and-computing) or
  arithmetic-only with its stating act **not ingested** — IE's PRSI credit taper
  (`1/6`, a 2016 amendment to SWCA 2005 s.13), FR's housing weighted averages
  (`bhotn_fr`, the APL arrêtés), FR's sick-pay `2/3` (Code du travail L1226-1,
  of which 4 units are ingested). So a *ready* `derive` case does not exist in
  FR, IE or LT today, and ingesting any one of those acts creates the first one.
  That is a corpus finding, not a reason to invent a case.
- **Balance the set.** 47 of the first 67 cases expected `unchanged`, so
  routing accuracy was largely a measure of resisting change. Get `changed`
  cases from parameters where EUROMOD is genuinely stale — not by relabelling
  ones where it is not.

### Verification is a human gate

`verified: true` means a person checked the ground truth against the act.
Drafters always emit `verified: false`, and `nomokrisis-eval verify <id>
[--note …]` (or the UI's Golden set tab) is the only way to flip it — the
reviewer recorded is the database login (`current_user`), there is no
`--reviewer` flag to put someone else's name on it.
**Never verify cases on the user's behalf** — list what needs re-verifying and
why, and let them.

## 4. Reporting the review

Lead with the split, not the headline. State, in this order: how many cases were
unanswerable (corpus), how many expectations were wrong (golden set), how many
KPIs were measuring the wrong thing (scoring), and only then what the model got
right and wrong. Give the corrected numbers next to the raw ones and say which
fix moves which.

Note which direction each defect pushed. In the first review every one of them
pushed the reported score *down* — worth saying explicitly, because it is the
difference between "the eval is pessimistic" and "the eval is broken".
