---
name: review-eval
description: Review a Nomokrisis evaluation run and improve the golden set behind it — separate real model failures from scoring artifacts, corpus gaps and mislabelled ground truth, then fix the selection files. Use when asked to review, interpret or sanity-check eval results ("is the eval correct?", "why is the score so low?", "did the model really fail these?"), or to add/repair golden cases.
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
uv run nomokrisis-eval list-runs            # run ids, model, progress
ls .eval_runs/<run-id>/                     # manifest.json cases.json results.json queue/
```

A run directory is self-contained and is the thing to read:

| file | what it is |
|---|---|
| `manifest.json` | model, **critique_model**, prompt/agent/eval versions, dataset hash, `as_of` |
| `cases.json` | the golden cases **frozen at run start** — the expectations actually used |
| `results.json` | one scored `CaseResult` per case |
| `queue/<item_id>.json` | the full `ReviewItem`: proposal, references, critique, retrieval trace |

`results.json` alone cannot tell you *why* anything scored as it did. The
answer is nearly always in the matching `queue/` item — read it.

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
uv run python - <<'PY'
import json, collections
R = ".eval_runs/<run-id>"
cases = {c["id"]: c for c in json.load(open(R + "/cases.json"))}
res = json.load(open(R + "/results.json"))
counts = collections.Counter()
for r in res:
    if r["date_correct"] is False:
        item = json.load(open(f"{R}/queue/{r['item_id']}.json")) if r["item_id"] else {}
        prop = (item.get("proposed_value") or {}).get("valid_from")
        counts[(cases[r["case_id"]]["expected"]["valid_from"], prop, r["routing_actual"])] += 1
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

### b. Corpus gap — could any model have answered?

First check whether it is really a gap. The gap-fill scout records what the
proposal said it was missing and what it did about it, on every review item:

```bash
uv run python -c "
import json,sys; d=json.load(open(sys.argv[1]))
print(json.dumps(d.get('scout'), indent=2, ensure_ascii=False))" .eval_runs/<run-id>/queue/<item_id>.json
```

`needs` is the analyst's own account of the missing document, `ingested` is what
the scout fetched. `needs` set but `ingested` empty means one of: the act is not
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
label a human set in `golden_sources/` (`labels_drafted: false`), because the
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
the selection file is wrong — fix it there, never in `dataset/`.

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
uv run python - <<'PY'
import json, glob
for p in sorted(glob.glob("dataset/**/*.json", recursive=True)):
    c = json.load(open(p))
    for part in (c.get("notes") or "").split(" | "):
        if part.startswith("drafting warning"):
            print(f"{c['id']:46s} verified={c['verified']} :: {part[:140]}")
PY
```

A `verified: true` case carrying a drafting warning is the dangerous
combination: the drafter doubted it and a human waved it through anyway.

### d. Input defect — is the parameter under test itself sound?

`$Minwage_hourly` carries unit `currency/month` and the raw value `11.88#m`
although 11.88 is the *hourly* SMIC. A correct model finds "11,88 euros par
heure" and refuses to present it as monthly — scoring `not_found` for a reason
that is neither the model's nor the corpus's. `unit` comes from the read-only
EUROMOD export and `ingest-params` overwrites it, so these cannot be curated
away: record them in the selection file's `note` and report them to the
economists team, as the set already does for the FR barème 1-€ erratum and IE's
27 382/27 383.

### e. Model failure — what is left

Only now read the proposals. For refusals, the reason is in the critique:

```bash
uv run python - <<'PY'
import json
R = ".eval_runs/<run-id>"
for r in json.load(open(R + "/results.json")):
    if r["routing_actual"] != "not_found":
        continue
    item = json.load(open(f"{R}/queue/{r['item_id']}.json"))
    reasons = [i for i in (item.get("critique") or {}).get("issues", []) if i.startswith("model:")]
    print(f"--- {r['case_id']}  retrieval_hit={r['retrieval_hit']}")
    print("   ", (reasons[0] if reasons else str((item.get('critique') or {}).get('issues')))[:300])
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
uv run nomokrisis-eval rescore <run-id> --write    # persist (results.json + Postgres)
```

It replays the run's stored `ReviewItem`s against the run's **frozen**
`cases.json`, so what you see is the effect of the scoring change alone. To
measure a golden-set change, start a new run.

## 3. Improving the golden set

Cases are **generated**, never hand-written. Edit
`golden_sources/{openfisca_fr,ie,lt}.json` and rebuild:

```bash
uv run nomokrisis-eval build-openfisca-dataset --year 2025 --country FR
uv run nomokrisis-eval build-curated-dataset  --year 2025 --country IE
```

Never edit a file under `dataset/` by hand — the next rebuild overwrites it.

A rebuild **keeps the human verdict when the ground truth is unchanged** and
resets it to `verified: false` when `expected`, the parameter file or `as_of`
moved (`dataset.save_drafted_case`). A reset is printed; act on it, because
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
- **Write the citation exactly as `legal_units.citation` spells it.**
  `citation_matches` is one-way containment, so a golden citation carrying more
  than the corpus does can never match. LT scored **citation 0% and recall 0%**
  on a whole run while the pipeline had cited the right article in four of seven
  cases, purely because the selection file wrote `GPMĮ IX-1007, 20 straipsnis`
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
- **Correct a difficulty label in the selection file, not the case file.** Set
  `difficulty` / `hazards` on the `golden_sources/<cc>.json` entry: the builders
  prefer an explicit entry value over anything drafted, mark the case
  `labels_drafted: false`, and a rebuild will not undo you. Editing the
  materialized case in `dataset/` loses the change on the next build.
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
--reviewer <name>` (or the UI's Golden set tab) is the only way to flip it.
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
