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
`GoldenCase.corpus_available` records this; the report prints the split.

```bash
uv run nomokrisis-eval report --run-id <run-id>     # prints "source not in corpus: N case(s)"
```

The first run reviewed this way split hard: **73% routing / 73% value on the 45
cases whose act was ingested, 11% / 11% on the 18 where it was not** — against a
54%/52% headline. Report both numbers or neither.

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
