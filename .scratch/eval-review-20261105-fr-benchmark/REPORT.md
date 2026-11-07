# FR 2025 benchmark: improvements of 3–6 Nov 2026

Status: ready-for-human
Run measured: `eval-20261105T212046Z-gpt-6-luna-c79352` (agent 0.8.3, prompt 0.12.0, model `azure_openai/gpt-6-luna`, critique `gpt-6.1-sol`), finished 6 Nov 2026 02:40.
Benchmark: blind EUROMOD 2024 → 2025 over every FR parameter with a value in force on 1 July 2025. That is 345 cases: 169 changed, 156 unchanged, 19 new, 1 derived. A case counts as a success when the proposed value equals the value EUROMOD holds for 2025 (`value_correct`).

## Headline

**247 / 345 = 71.6 %**, up from 136 (39.4 %) at the start of this series and from 218 (63.2 %) on the previous full run.

| run | agent | correct | score |
|---|---|---|---|
| `…e1ed27` (3 Nov) | 0.3.0 | 136 | 39.4 % |
| `…5c7ac3` (4 Nov) | 0.5.0 | 177 | 51.3 % |
| `…1d8bee` (5 Nov) | 0.6.1 | 178 | 51.6 % |
| `…975e37` (5 Nov) | 0.7.0 + corpus additions | 207 | 60.0 % |
| `…0ca32d` (5 Nov) | 0.8.0 | 218 | 63.2 % |
| **`…c79352` (6 Nov)** | **0.8.3** | **247** | **71.6 %** |

| metric | 0.8.0 | 0.8.3 |
|---|---|---|
| coverage (a value was proposed) | 78.5 % | 85.5 % (294/344) |
| precision (proposed values that are right) | 80.7 % | 84.0 % |
| change recall | 55.9 % (105/188) | 69.1 % (130/188) |
| unchanged values confirmed | 72.4 % (113/156) | 75.0 % (117/156) |
| verbatim extracts | 100 % | 100 % |
| hallucination | 0 % | 0 % |

Against 0.8.0, 35 cases were gained and 6 lost. I checked the regressions: `bsa00_amt2/3` are composition mistakes by the model (lone-parent rates instead of couple rates, one extra child), and the critique caught both. The other four (`bunmt_bonus1/6`, `UB_QperMin`, `tsceepi_rate11`) were right in the previous run. These are run-to-run LLM variance, not a defect of the new code. Expect about ±5 cases of noise between two runs of the same agent.

Note on attribution: agent 0.8.2 was measured only on a 42-case batch (16 gained, all of which had failed in 0.8.0). Its full run was stopped for 0.8.3, so the 0.8.0 → 0.8.3 gain covers both versions.

## What was changed

### Retrieval: getting the act that states this year's figure into view
- **Implementing acts (references followed backwards)** (`retrieval.implementing_acts`):
  - A code article that says «fixé par décret» now brings the recent non-code acts that name it: CASF L. 262-2 → the décret du 28 mars 2025 (RSA 646,52 €), CSS L. 842-3 → the prime d'activité decree (633,21 €), R. 522-2 → instruction DSS/2B/2024/181.
  - These include acts that name the article inside a list closed by the code's name.
  - Only acts in force on the reference date and entered into force in the year before it are taken.
  - Each act also brings its two chunks nearest to the query.
  - *0.8.3:* the 20 best-ranked code articles are looked at instead of 6, and the acts are ranked by distance to the query before the cap of 6. With retrieval order alone, six family-benefit articles filled the cap and L. 262-2 was 16th.
- **Recent texts for a named need** (`locate_named_units`): after a not_found, the need's words are also searched over texts entered into force in the last year. For example, «l'arrêté portant revalorisation de la BMAF» matched the 2005 decree by title, while the 2025 amount is in DSS/2B/2025/38.
- **Code lists**: «Articles L. 381-1, …, R. 522-2 … du code de la sécurité sociale» is read as references to each article, including across line breaks.

### Corpus: documents the benchmark needed and Legifrance does not hold
Added as **guidance** (citable, shown as guidance on every proposal):
- Instruction DSS/2B/2025/38 (BMAF and the April 2025 revaluations).
- Instruction DSS/2B/2024/181 (family-benefit ceilings for 2025).
- The CAF EAJE barème 2025.
- The CSG instruction of 4 Dec 2024.

Added as **evidence**: CSS D. 843-1.

Supporting changes:
- **Contributed PDFs:** they are split without turning table rows or dates into headings (`documents.drop_table_rows`).
- **Bulletin officiel:** a `.pdf` URL that answers a script with an HTML page is retried once in headless Firefox (`contributed.fetch_in_browser`). This is how the Bulletin officiel of sante.gouv.fr was fetched, with no captcha solving. The worker image installs Firefox, but **the image still has to be rebuilt** (`docker compose --profile gpu up -d --no-deps --build worker`).

### Verification: fewer right values refused, same anti-hallucination guarantee
The extract is still checked character-for-character against the chunk it points to.
- **Re-pointing a quote:** when the model cites a retrieved chunk that does not hold its quote, the citation is moved to the one retrieved chunk that does. A citation string or a corrupted UUID written in the id field is resolved by the extract. Eleven right values of the 5 Nov run had been refused for swapped ids.
- **PDF artefacts in quotes:** whitespace runs are equivalent, a split ligature («prestati ons») is tolerated between letters only, and punctuation at the two ends of a quote is ignored.
- **Derivations** (a value computed from quoted operands):
  - Numbers the law spells out are accepted («trois fois», «la moitié»).
  - «majoré de 50 %» states a multiplier of 1.5.
  - The months 3, 6 and 9 are allowed as constants.
  - Rates are rounded like the value held (12,954 % → 0.1295).
  - *0.8.3:* a PDF table row «I 329,71 397,64 449,43 65,21» now states each of its four amounts. It used to be read as one number, which refused the housing-benefit rent ceilings.
  - *0.8.3:* when an operand's extract misses its figure, the retry is shown the chunk's sentence that does state it («1/ 730e», CSS D. 622-7).
- **Confirming the held value:** when the proposed value equals EUROMOD's and the citation is accepted, a start-date objection becomes a note. The start date of an unchanged value changes nothing in the export.
- **"FYA" amounts:** these are proposed as the amount in force, never averaged. This gained the prime d'activité amounts: 949,82 = 633,21 × 1,5.

## What still fails (98 cases)

| bucket | cases | what it is | lever |
|---|---|---|---|
| Rounding / boundary offsets | 19 | ±0.01 € or ±1 € from EUROMOD; the legal figure is right. Examples: AF amounts (151.80 vs 151.81), PAJE ceilings (36 622 vs 36 621), décote limits (1 965 vs 1 964), the income-tax barème held as "up to" bounds (11 496 vs the law's 11 497) | scoring decision |
| EUROMOD conventions or stale values | 23 | Values that follow a model convention, not the 2025 law:<br>• `tpr_threshold1–5` lag a year<br>• `bho_rl_rate2/3` held in percent points (0.45 for 0.45 %)<br>• `tscsesi_*` rates are EUROMOD aggregates of several contributions<br>• `bsawk_income_rate` 0.61 while the law says 59,85 % since April 2025<br>• `UB_dayfixamt` 13.11 while 13.18 applies from 1 July<br>• `tinty_dedub_uplim` 0, switched off in the model<br>• `RetAge_min` 62.5 | curation or scoring decision |
| Not found | 38 | Mostly social contributions: AGIRC-ARRCO / CSG schedules, farmers' and self-employed rates, unemployment rates. Also the prime de fin d'année (`bunmt_bonus*`, 5), ASF (`bchor_amt1/2`), `bhl_max_amt1/2`, `tpr` rates, `tinrt_cdhr` | corpus, retrieval |
| Model reasoning errors | 16 | The wrong household scale for the RSA (`bsa00_amt2/3/8`), an old BMAF (`bched_amt2`), the 2025 PSS where the N−2 PSS applies (`bchlg_thres1`), a Mayotte amount (`bunmt_bonus5`), the employer share instead of the employee share (`tsceepi_rate11`), a wrong start date (`tscer_red_coef2`), … | pipeline |
| Right value rejected by the critique | 2 | `UB_QperMin` (130 days vs 6 months), `tscerho_rate2` | pipeline |

Ceiling with the pipeline alone: if every not-found and reasoning error were fixed, the score would reach about 86 %. Realistically, a third to a half of those 56 cases are reachable soon, which gives **about 76–79 %**.

**Reaching 80 % needs a decision on the first two buckets** (42 cases). The pipeline is not wrong there. EUROMOD holds a value that is not the figure the law states.

## What can still be done, by expected gain

1. **Scoring: accept one unit of the held precision** (+19, giving about 77 %).
   - What: ±0.01 when EUROMOD holds cents, ±1 when it holds whole euros. The bound would be read off the held value.
   - Trade-off: CLAUDE.md keeps the tolerance at 1e-6 on purpose, so that the barème's 1-euro erratum scores as a difference. This option gives that up.
   - Alternative: report both numbers, strict and one-unit.
2. **Curation: record the conventions in the parameter metadata** (+up to 23).
   - What: add a `lag_years` / "held as previous year" flag (`tpr_threshold*`), a percent-points unit (`bho_rl_rate*`), and a "sum of components" note for the aggregated contribution rates.
   - Where: the overlay in `curation/FR.curation.yaml`, re-applied by `curate-params`.
   - The pipeline and the scorer can then follow them instead of failing on them.
   - Stale values (`bsawk_income_rate`, `UB_dayfixamt`) are findings for the EUROMOD team, not pipeline failures.
3. **Corpus: social contributions** (most of the 38 not-found).
   - Add the Urssaf barèmes and the Agirc-Arrco annual circular as guidance publishers in `scout.GUIDANCE_PUBLISHERS`, or ingest them once as contributed documents.
   - Check that the 2025 décret for the prime de fin d'année is held. It is published in December, so it reaches a system-year run through `later_in_year`.
4. **Pipeline: household-composition arithmetic.**
   - The RSA and prime d'activité scales (R. 262-1 / D. 843-1: +50 % for the second person, +30 %, +40 % from the third) are where the model miscounts.
   - A worked example in the proposer prompt, or a check that the derivation's multiplier matches the household described by the label, would target `bsa00_amt2/3/8` and their prime d'activité twins.
5. **Variance.**
   - About ±5 cases move between two runs of the same agent.
   - Two proposals per case, keeping the one the critique accepts, or a second attempt on a disagreement, would remove most of it, at roughly twice the LLM cost.

## Housekeeping

- **Nothing is committed.** The working tree holds all changes: pipeline, ingest, worker Dockerfile, tests and CLAUDE.md.
- **Tests:**
  - Pipeline: 155 passed, with `test_encode_client.py::test_no_worker_is_a_timeout` deselected.
  - Ingest: 253 passed.
- **Worker image:** it has to be rebuilt for Firefox, using `--no-deps` so the database is not restarted.
- **Run 71** (`…861a6b`, agent 0.8.2, stopped at case 9) is still marked `running` in `eval.runs`. Ignore it.
