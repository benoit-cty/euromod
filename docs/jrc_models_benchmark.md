# Benchmark of non-OpenAI models for the Nómos workflow (LT 14–15 Nov, FR 16 Nov 2026)

JRC cannot use OpenAI models in production. This benchmark measures whether
JRC self-hosted models can replace the Azure GPT models
(gpt-6-luna proposing, gpt-6.1-sol critiquing) that all earlier evaluations
used.

Benchmark run through OpenRouter as the contractor don't have access to JRC network.

**Short answer.** On the 117 Lithuanian parameters, MiniMax M2.7 doing both
steps (propose and critique) is correct on **70.1 %** of parameters, against
**77.8 %** for GPT. More than half of the gap is 10 crashes caused by an
OpenRouter provider rejecting long prompts, not wrong answers. Precision stays
high (93.8 % vs 96.6 %). Mistral Small 3.2 is not usable 
(7.7 %): it does not reliably return the structured answer on long legal
prompts. Two fixes followed from the analysis (§7).

**On France** (345 parameters, §9), with those fixes in place, the gap is much
wider: all-MiniMax is correct on **38.8 %** against **65.2 %** for GPT, and
its precision falls to **74.6 %** (GPT 88.7 %). The crashes are gone, so the
gap is wrong values and abstentions. MiniMax is not yet a replacement on a
country as hard as France.

---

## 1. Runs compared

All five runs used the same code (agent 0.9.2, prompt 0.13.1, commit
`da152f0`) and the same corpus. They ran one after another on the same machine,
so the only thing that changes between runs is the model.

| Run | Proposes | Critiques | Run id (`eval.runs.run_id`) |
|---|---|---|---|
| smoke | MiniMax M2.7 | MiniMax M2.7 | `eval-20261114T101106Z-minimax-minimax-m2-7-bb9a31` (FR, 5 cases) |
| **A** | `azure_openai/gpt-6-luna` | `azure_openai/gpt-6.1-sol` | `eval-20261114T103255Z-gpt-6-luna-a3864f` |
| **B** | `openrouter/minimax/minimax-m2.7` | `azure_openai/gpt-6.1-sol` | `eval-20261114T115429Z-minimax-minimax-m2-7-c3daa0` |
| **C** | `openrouter/minimax/minimax-m2.7` | `openrouter/minimax/minimax-m2.7` | `eval-20261114T155329Z-minimax-minimax-m2-7-d75193` |
| **D** | `openrouter/mistralai/mistral-small-3.2-24b-instruct` | `openrouter/minimax/minimax-m2.7` | `eval-20261114T212657Z-mistralai-mistral-small-3-2-24b-instruct-d5c476` |

*Proposes* is the model doing the search and propose the value, *Critiques* is the model that validate the proposal.

- **A** is GPT reference.
- **B** changes only the proposer.
- **C** is the configuration JRC could deploy without OpenAI.
- **D** tests a small Mistral model as the proposer.

Phoenix's, the observability stack, LLM spans (`attributes->'llm'->>'model_name'`) confirm that each run
called the models listed:
- Run A: 279 gpt-6-luna and 111 gpt-6.1-sol calls.
- Run B: 410 MiniMax and 128 sol calls.
- Run C: 420 MiniMax calls and nothing else.

Each run was started with:

```bash
cd Nomokrisis-evaluation_pipeline
EVAL_CRITIQUE_MODEL=<critique model> uv run nomokrisis-eval run-benchmark LT --year 2025 --model <proposer>
uv run nomokrisis-eval benchmark-report <run_id>
```

## 2. How the evaluation works

### 2.1 The benchmark task: a blind year-on-year update

The benchmark (`nomokrisis_eval/benchmark.py`) asks the question a EUROMOD
country team asks each year: **starting from system year 2024, can the
workflow find each parameter's 2025 value in the law?**

- **One case per parameter.** Cases are drafted mechanically from the
  parameter store (`params.*`, loaded from EUROMOD's own export). Each bracket
  schedule counts as one case. For LT that gives **117 cases**. Another 34
  parameters were skipped because EUROMOD holds no value for them on 1 July
  2025, and 4 more because they are scored as part of their bracket schedule.
- **The workflow runs blind.** It sees the parameter record truncated before
  1 January 2025 (`paramdb.blind_record`), so it never sees the value it is
  scored against. The reference date is **1 July 2025**.
- **Ground truth is EUROMOD's own 2025 value.** The expected routing is
  computed against 2024:
  - `changed`: EUROMOD's 2025 value differs from 2024. 18 cases.
  - `unchanged` (kept): EUROMOD kept the 2024 value. 93 cases.
  - Not legislative: national-team or derived parameters, which the pipeline
    should route around without proposing a value. 6 cases.
- **No LLM judge.** Every score is computed by deterministic code
  (`scoring.py`). Values are compared after normalisation: EUROMOD formulas
  are evaluated, `$constant` references resolved, and `#m/#y` period suffixes
  converted. The relative tolerance is 1e-9, to absorb float noise only. Where
  EUROMOD stores a mid-year weighted average, the value in force on the
  reference date is also accepted.

### 2.2 What one case runs

The workflow (`Nomoscope-agentic-workflow/pipeline`) is a fixed pipeline, not
a free agent:

1. **frame.** Build a search query from the parameter's label and description.
2. **retrieve.** Hybrid search (text + embeddings) over the legislation in force on 1 July 2025:
   full-text search plus BGE-M3 vectors, fused by rank. It then follows the
   cross-references, the implementing acts and the same-act references, and
   adds versions that enter into force later in 2025.
3. **propose** (LLM, structured output). Return the value, a verbatim quote,
   the chunk it comes from and the date it takes effect. Otherwise return
   "not found" and name the missing sources.
4. **critique** (LLM, plus mechanical checks):
   - **Mechanical, independent of the model.** The quote must appear
     character for character in the cited chunk. The dates must be
     consistent. Any derivation must be arithmetic over quoted operands.
   - **The critique model.** It checks that the quote states the value, that
     the dates fit, and that the value is sane.
   - **On failure.** The proposer retries with the critique's feedback. After
     a "not found", the `locate` step looks up the named sources in the corpus
     and the proposer tries again.
5. **diff / enqueue.** Route the result as `changed`, `unchanged`,
   `not_found`, …, and write a review item.

The verbatim check is why **hallucination is 0 % in every run**: a quote that
is not in the law cannot pass. What the check cannot catch is a real quote
from the *wrong* text. **That was MiniMax's main reasoning error (§5.2).**

### 2.3 Language: did MiniMax read Lithuanian or English?

**It read Lithuanian law and was instructed in English.**

- **Extracts.** Retrieval filters on the country's law language
  (`retrieval.LANG_BY_COUNTRY["LT"] = "lt"`). The LT corpus holds 91,311
  authentic Lithuanian chunks. The 6,380 English machine-translation chunks
  feed the UI and are never sent to the model.
- **Instructions and parameter definition.** The system prompt is in English,
  and so are the parameter's labels and description (EUROMOD's English
  texts).
- **Output.** The model quotes the Lithuanian text verbatim (it must, to pass
  the verbatim check) and adds its own English translation of the quote
  (`english_translation`) for the reviewer.
- **The search query is in English for LT.** FR parameters have
  law-language labels (1,277 machine-translated texts in
  `params.parameter_texts`), but LT parameters have none. The LT frame query
  is therefore EUROMOD's English text:
  - The BGE-M3 vector leg is multilingual, so it still finds Lithuanian law
    from an English query.
  - The full-text leg, which uses Lithuanian stemming, gets little from
    English words.
  - This affects every model equally, so it does not bias the comparison. It
    does probably cost recall for all of them (§8).

### 2.4 The metrics

`benchmark-report` places every case in a matrix:

- **Rows: what EUROMOD did** between 2024 and 2025: changed, or kept.
- **Columns: what the workflow answered:**
  - **same value**: equals EUROMOD 2025.
  - **EUROMOD off the law**: a finding. EUROMOD is exactly one cent or one
    euro off the figure the quoted law states.
  - **different value**: a value that is neither of the above.
  - **kept Y-1 value**: routed `unchanged`, but the value is not EUROMOD
    2025.
  - **not found**: the workflow abstained.
  - **rejected**: the critique failed the proposal. A rejected proposal is
    never credited, even if its value is right, because the pipeline does not
    stand behind it.
  - **error**: the case crashed.

The headline rates are computed from that matrix. *Legislative* means the 111
cases with a value to find, i.e. excluding the 6 national-team or derived
parameters.

| Metric | Formula | Question it answers |
|---|---|---|
| **correct** | (same value + not-legislative cases routed as expected) / all 117 | Overall, how often did the workflow do the right thing? |
| **coverage** | answered / 111 legislative, where *answered* = same value + off the law + different value + kept Y-1 value | How often does it commit to a value rather than abstain, get rejected or crash? |
| **precision** | same value / answered | **When it does commit to a value, how often is it right?** This is what a reviewer experiences: a low-precision model floods the queue with wrong proposals. |
| **change recall** | same value / 18 parameters EUROMOD changed | **Of the real changes in the law, how many did it find?** This is the most valuable outcome and the hardest. |
| **unchanged confirmed** | same value / 93 parameters EUROMOD kept | How often does it confirm, with a quote, that a value did not change? |

Precision and recall pull in opposite directions. A model that abstains
whenever it is unsure has high precision and low coverage and recall. A model
that always answers has the reverse. Because every proposal goes to a human,
**precision matters more than coverage**: an abstention costs the analyst a
manual lookup, while a wrong value with a convincing quote can be accepted by
mistake.

## 3. Results

| LT 2024→2025, 117 parameters | A: GPT | B: MiniMax + sol | C: all-MiniMax | D: Mistral + MiniMax |
|---|---|---|---|---|
| **correct** | **77.8 %** (91) | 59.0 % (69) | **70.1 %** (82) | 7.7 % (9) |
| coverage | 79.3 % (88/111) | 61.3 % (68) | 73.0 % (81) | 2.7 % (3) |
| **precision** | **96.6 %** (85/88) | 92.6 % (63/68) | **93.8 %** (76/81) | 100 % (3/3) |
| change recall | 44.4 % (8/18) | 33.3 % (6) | 38.9 % (7) | 0 % |
| unchanged confirmed | 82.8 % (77/93) | 61.3 % (57) | 74.2 % (69) | 3.2 % (3) |
| findings (EUROMOD off the law) | 0 | 0 | 0 | 0 |
| different value + kept Y-1 | 3 | 5 | 5 | 0 |
| not found | 14 | 19 | 18 | 59 |
| rejected by the critique | 9 | 15 | 2 | 2 |
| **error (crash)** | **0** | **9** | **10** | **47** |
| LLM calls | 390 | 472 | 447 | 526 |
| prompt / completion tokens | 10.8 M / 0.20 M | 16.0 M / 0.40 M | 16.8 M / 0.67 M | 21.6 M / 1.66 M |
| mean time per case | 42 s | 122 s | 171 s | 1 009 s |
| wall time | 1 h 21 | 3 h 59 | ~4 h | 8 h 24 |

The matrices behind the rates:

```
                 same  different  kept-Y-1  not-found  rejected  error
A changed (18)      8          1         0          6         3      0
A kept    (93)     77          2         0          8         6      0
B changed           6          2         0          7         0      3
B kept             57          3         0         12        15      6
C changed           7          1         0          6         0      4
C kept             69          4         0         12         2      6
D changed           0          0         0          9         0      9
D kept              3          0         0         50         2     38
```

**Duration.** MiniMax is very slow, but it was served from OpenRouter, not the JRC.

**Cost.** OpenRouter billed **$17.59** for the smoke run and runs B, C and D
together. The key's spending endpoint does not break this down per run, and
run A's Azure cost was $22. MiniMax M2.7 lists at $0.21 / $0.84
per million input / output tokens, so a full LT run is a few dollars. It uses
about 1.5× GPT's prompt tokens, because it needs more retries and more `locate`
rounds.

## 4. The FR smoke run (5 cases)

The smoke run was a plumbing check before the long runs, too small to measure
anything:

- **Results.** 2 of 5 correct, no errors, all quotes verbatim.
- **One real error.** It answered `$tscerho_rate2` (FNAL contribution, firms of
  50 or more employees, 0,50 %) with 0,45 % quoted from CCH art. L313-1. That
  is the PEEC, a different employer levy. The MiniMax critique accepted it.
- **One sound abstention.** It abstained on `$tscsesi_rate13`, where GPT's
  8 Nov FR run had given a wrong value.

## 5. Why MiniMax loses ground

### 5.1 Crashes: provider limits, not model quality (14 of 19 errors in B+C)

Fourteen cases crashed with `400 … context window exceeds limit`, returned
by **GMICloud**. MiniMax M2.7 is listed at 196,608 tokens, yet the rejected
prompts were about 88k tokens, while prompts of 128k went through elsewhere.

- **The trigger.** OpenRouter routes MiniMax to Groq first. When Groq answered
  `429 rate-limited upstream`, OpenRouter fell back to GMICloud.
- **The limit.** GMICloud allows up to 176,947 output tokens, and the request
  set no `max_tokens`. The likely explanation is that GMICloud reserves that
  output budget inside the window, so the prompt only had about 20–90k tokens
  of room.
- **Runaway answers.** Without a cap, one MiniMax answer ran to 131,072
  output tokens (Groq's cap). 99 % of its calls stay under 7,740.

The other 5 errors are OpenRouter answers with no `choices` (a provider error
passed through as a 200 response), plus one structured-output validation
retry limit.

### 5.2 Quoting an old amending act instead of the law in force

The clearest reasoning error is on the income-disregard rates
`$bsa00_IncDisreg_rate2/4/5` (25 / 35 / 40 % in 2025). MiniMax answered 20 /
30 / 35 % in runs B and C:

- **What it quoted.** It quoted law **XIII-1733, art. 1**, a 2019 *amending*
  act: «1 straipsnis. 17 straipsnio pakeitimas … Pakeisti 17 straipsnio …
  išdėstyti taip: … 5) 35 procentai».
- **What GPT quoted.** The consolidated **PSPĮ art. 17**: «5) 40 procentų».
- **Why it happened.** In run C the consolidated article was not even among
  MiniMax's extracts. An amending act's article stays "in force" as an act
  forever, so retrieval returns it as current, while the article it rewrote
  was amended again later.
- **Why no check caught it.** The quote is verbatim, so the mechanical check
  passes. The MiniMax critique did not object, and in run B neither did
  gpt-6.1-sol.

The FR smoke run's FNAL/PEEC confusion (§4) is the same kind of error: a real
quote, from the wrong text.

### 5.3 A lenient critique

As critique, MiniMax rejected **2** proposals in run C. gpt-6.1-sol rejected
**15** of the same proposer's proposals in run B, and 9 of GPT's in run A.

- **Why C scores above B.** sol rejected many MiniMax proposals that had the
  right value but a citation it did not accept, while MiniMax accepted them.
- **The cost.** Errors like §5.2 get through.

The mechanical checks keep the overall precision at 93.8 %. Still, the
critique is the weaker of MiniMax's two roles.

### 5.4 Not specific to MiniMax

The following misses are shared by all models and are scoring or
ground-truth questions, not model failures:

- **Pension ages.** EUROMOD holds 64.66 and 64.83, while the law gives 64 years
  8 months = 64.667. Every model is scored wrong.
- **The `tin_schedule` / `tin_schedule_2` groups.** Every model mismatches
  them.

## 6. Why Mistral Small 3.2 fails

Phoenix shows that most of Mistral's 763 successful calls never produced a
usable answer:

- **No structured output.** It often wrote the JSON as plain text in a
  ```json block, or wrote Lithuanian prose, instead of calling the output
  tool.
- **Degenerate loops.** Some answers repeated one citation («sprendimas Nr.
  T3-65 … 5 punktas») until the 16,384-token limit. Others ended in a generic
  «I'm sorry, but I'm unable to assist with that… 😊».
- **Empty responses.** OpenRouter returned 144 empty responses (no `choices`).
  Some of its Mistral providers have 32k windows, against our 30–130k-token
  prompts.
- **Little reached the critique.** Only 32 proposals reached the MiniMax
  critique, and 59 cases ended as "not found".

A 24B instruction model does not cope with 100k-token prompts of foreign
legislation plus a strict output schema. **If JRC needs a Mistral model, test
a larger one** (Mistral Large / Medium). Small 3.2 is not worth tuning for
this pipeline.

## 7. Fixes made after the benchmark (in the code, not yet evaluated)

### 7.1 An output cap, and prompts trimmed to the model's window

`Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/llm.py`:

- **`ROUTED_MAX_TOKENS = 16_384`** is sent as `max_tokens` on every OpenRouter
  request (`model_settings`). Providers then budget the prompt against
  window − 16k instead of their own default reservation. The cap also stops
  runaway answers.
- **`CONTEXT_WINDOWS`** records the token windows of the models a full
  retrieval can outgrow: MiniMax M2.7 196,608, Mistral Small 3.2 128,000.
  `prompt_budget_chars(model)` converts window − output cap − 4,096 tokens of
  headroom into characters, at 2.0 characters per token. MiniMax measured
  about 2.4 on Lithuanian law, so 2.0 errs on the safe side. **A model not
  listed is never trimmed**, so the GPT runs are unchanged.
- **`propose_with_llm` and `critique_with_llm`** pass the retrieved chunks
  through `prompts.fit_hits` when the model has a budget, and log a warning
  whenever chunks are dropped. `fit_hits` works like this:
  - **Dropped first:** the ranked search hits, lowest rank-fusion score first.
    These are the tail of the k ranked hits, the least likely to state the
    value.
  - **Dropped only as a last resort:** hits added on purpose (citation fast
    path, located sources, cross-references, implementing acts, same-act
    articles, later-in-year versions, sibling chunks), from the end of the
    list.
  - **Never dropped:** in the critique, the chunks the proposal cites.
  - **Unchanged:** the order of the hits, and any prompt that already fits.

The mechanical checks still run against the full retrieval, so trimming only
changes what the model sees. Tests are in `tests/test_llm.py`.

### 7.2 The critique prefers the consolidated article over an amending act

`prompts.py` (prompt version **0.14.0**):

- **Proposer.** A new rule, *CONSOLIDATED TEXT OVER AMENDING ACTS*:
  - Quote the consolidated article when it is among the extracts.
  - Quote an amending provision only if it enters into force in the year
    before the reference date or later.
  - Otherwise return "not found" and name the consolidated article in
    `missing_sources`. The existing `locate` step then fetches it from the
    corpus, which would have retrieved PSPĮ art. 17 in §5.2.
- **Critique.** A new *SUPERSEDED AMENDMENT* clause in the dates check fails a
  proposal quoting an amending provision that entered into force before
  1 January of the year before the reference date, and names the consolidated
  article to cite. It also fails one that contradicts the consolidated version
  of the same article. The FR income-year rules for finance-act articles are
  explicitly left unaffected.
- **Detection.** Amending provisions are recognised by their wording, with
  examples in the four pilot languages («Pakeisti … išdėstyti taip», «est
  ainsi modifié», «wordt als volgt gewijzigd», «Se modifica»). This is
  prompt-level, not a mechanical check. A mechanical version would need the
  ingesters to mark amending acts (§8).

## 8. Recommendations and next steps

1. **Re-run C on LT** with the fixes (prompt 0.14.0) and compare with this
   run. Expected effect:
   - Most of the 10 crashes go away.
   - The income-disregard rates should be found through `locate`.
   - Run A should be repeated too, to check the new prompt rule does not cost
     GPT anything.
2. **Pin OpenRouter providers** for MiniMax (`provider.order` / `only`), so a
   benchmark does not silently mix providers with different limits and
   quantisations: GMICloud serves fp8.
3. **Try `minimax/minimax-m3`**: 1M-token context, still cheap ($0.30 / $1.20
   per million tokens), with `structured_outputs` support.
4. **Translate LT parameter texts** (`translate-params`, as done for FR), so
   the full-text leg of retrieval gets a Lithuanian query. This should help
   every model.
5. **Mark amending acts at ingest** (an instrument or unit flag), to turn the
   §7.2 rule into a mechanical check that does not depend on the critique
   model's strength.
6. **Then run FR** (345 cases) with the best configuration. FR is harder
   (income-year rules, guidance documents) and is where the critique's
   leniency would cost most. *Done on 16 Nov 2026 for A and C, see §9: it
   did cost most.*

For a JRC deployment without OpenAI, **all-MiniMax M2.7 is a viable
candidate today**: about 8 points behind GPT on LT, with comparable precision,
a few dollars per country run. Most of the remaining gap is the two
issues fixed in §7.

## 9. France, 2024→2025 (16 Nov 2026)

### 9.1 Runs

Only runs A and C were repeated on France: B and D were not, on purpose.
Both runs used commit `5ff0774`, agent 0.9.2 and prompt **0.14.0**, so they are
the first runs with the §7 fixes in place. They ran on the same day, one after
the other, on the same corpus.

| Run | Proposes | Critiques | Run id |
|---|---|---|---|
| **A** | `azure_openai/gpt-6-luna` | `azure_openai/gpt-6.1-sol` | `eval-20261116T063033Z-gpt-6-luna-65ced1` |
| **C** | `openrouter/minimax/minimax-m2.7` | `openrouter/minimax/minimax-m2.7` | `eval-20261116T121711Z-minimax-minimax-m2-7-04171d` |

```bash
EVAL_CRITIQUE_MODEL=<critique model> uv run nomokrisis-eval run-benchmark FR --year 2025 --model <proposer>
```

- **The task.** It is the same blind Y-1 → Y task as on LT (§2.1). FR
  has **345 cases**: 188 parameters EUROMOD changed, 152 it kept, and 5
  national-team or derived ones. The benchmark skipped 399 parameters: 361
  have no value on 1 July 2025, and 38 are scored inside a bracket schedule.
- **Model calls.** Phoenix shows that A called only gpt-6-luna (about 1 850
  calls) and gpt-6.1-sol (about 290). C made 2 364 MiniMax calls and nothing
  else.
- **Two incidents, both resumed.**
  - At `-j 4`, A hit the Azure rate limit on the gpt-6-luna deployment
    (`429 exceeded token rate limit`) on 54 cases, scattered through the run.
  - C ran out of OpenRouter credits (`402`) on its last 31 cases.
  - In both runs those error rows were deleted and the cases re-run with
    `nomokrisis-eval resume`: A at `-j 2`, C after a top-up. All 85 cases
    were scored on the re-run.
  - The figures below are the final ones.

### 9.2 Results

| FR 2024→2025, 345 parameters | A: GPT | C: all-MiniMax | *LT A* | *LT C* |
|---|---|---|---|---|
| **correct** | **65.2 %** (225) | 38.8 % (134) | *77.8 %* | *70.1 %* |
| findings (EUROMOD off the law) | **15** (9 stated, 6 derived) | 9 (9 stated) | *0* | *0* |
| success (correct + findings) | **69.6 %** (240) | 41.4 % (143) | *77.8 %* | *70.1 %* |
| coverage | 72.9 % (248/340) | 50.9 % (173/340) | *79.3 %* | *73.0 %* |
| **precision** | **88.7 %** (220/248) | 74.6 % (129/173) | *96.6 %* | *93.8 %* |
| change recall | **63.8 %** (120/188) | 31.4 % (59/188) | *44.4 %* | *38.9 %* |
| unchanged confirmed | 65.8 % (100/152) | 46.1 % (70/152) | *82.8 %* | *74.2 %* |
| different value + kept Y-1 | 13 | 35 | *3* | *5* |
| not found | 75 | 110 | *14* | *18* |
| rejected by the critique | 17 | 54 | *9* | *2* |
| **error (crash)** | **0** | **3** | *0* | *10* |
| LLM calls (eval.results) | 1 837 | 2 238 | | |
| prompt / completion tokens | 57.3 M / 0.95 M | 91.8 M / 2.72 M | | |
| wall time | ~6 h 25 | ~7 h 00 | | |

```
                 same  off-law  different  kept-Y-1  not-found  rejected  error
A changed (188)   120       14          8         0         32        14      0
A kept    (152)   100        1          5         0         43         3      0
C changed         59        9         24         3         56        36      1
C kept            70        0          8         0         54        18      2
```

- **Wall time.** Both runs ran 4 cases at a time (`-j 4`), and A's resume ran
  2 at a time. Wall time is therefore not comparable with the sequential LT
  runs. A's time also includes the waits on the rate limit.
- **Cost.** At list price, C's tokens cost about **$22**
  (91.8 M × $0.21 + 2.72 M × $0.84 per million). That fits the credit
  running out near the end of the run. A's Azure cost was not measured.

### 9.3 Reading the FR results

- **The gap is much wider than on LT.**
  - On correct answers, MiniMax trails GPT by 26 points, against 8 on LT.
  - On precision it trails by 14 points, against 3 on LT. A quarter of the
    values MiniMax commits to are wrong, and its own critique accepted them
    all.
  - OpenFisca has a value for 13 of C's disagreements with EUROMOD, and sides
    with EUROMOD on 12 of them.
  - Unlike LT, the gap is not crashes.
- **FR is the first real test of change detection.** LT had only 18 changed
  parameters, FR has 188. GPT finds 64 % of them, MiniMax 31 %.
- **FR produces findings, LT produced none.** GPT has 15 values where
  EUROMOD is exactly one unit off the figure the quoted law states:
  - 3 in each of `bch00_fr`, `bsa00_fr` and `tinkt_fr`;
  - 2 in `bchyc_fr`;
  - 1 in each of `bchba_fr`, `bchcc_fr`, `bched_fr` and `tinty_fr`.

  They are candidates for the EUROMOD team, **not yet checked by a
  person**.
- **GPT's misses are mostly abstentions.** Of 105 legislative misses, 75 are
  "not found" and 17 are rejections. The weakest policies are:
  - `bhoey_fr` (chèque énergie): 11 of 17 not found;
  - `tscer_fr`: 9 not found;
  - `tscse_fr`: 9 not found and 7 wrong rates;
  - `bsa00_fr` and `sickcomp_fr`: 7 not found each;
  - `bunmt_fr`: 5 of 6 not found.

  Most "not found" results are corpus problems rather than model problems
  (see the debug-phoenix-trace skill), so these policies are the next places
  to look for missing acts. 7 of GPT's 13 wrong values are self-employed
  contribution rates (`tscse_fr`).
- **MiniMax gives up on whole policies GPT answers.**

  | Policy | MiniMax | GPT |
  |---|---|---|
  | `trewl_fr` | 7 of 10 not found | 10 of 10 right |
  | `xcc_fr` | 9 of 16 rejected | 16 of 16 right |
  | `bsa00_fr` | 13 of 20 not found | 7 not found |
  | `bsawk_fr` | 8 of 14 not found, 5 rejected | 8 of 14 right |
  | `bunmt_fr` | 6 of 6 not found | 5 of 6 not found |

### 9.4 How MiniMax gets FR values wrong

The 35 wrong values MiniMax's critique accepted fall into three patterns.

- **The later revaluation instead of the 1 July amount.** EUROMOD holds the
  APL amounts as `(a*9 + b*3)/12`. The scorer accepts `a`, the amount in
  force on 1 July, and OpenFisca agrees with it. MiniMax proposed `b`, the
  1 October 2025 revaluation, on 6 `bhotn_fr` parameters. For example,
  `$bho_rentL_lim1` was proposed as 333.14 where the 1 July amount is 329.71.
  GPT gave the 1 July amounts.
- **The right article, the wrong figure in it.**
  - `$tin_decote_lim1` / `lim2` (décote thresholds 1 964 / 3 248) were
    answered with the décote amounts 889 / 1 470.
  - `$bsa00_hp_amt2` was answered with an APL rent ceiling (395.77), and
    `$bsa00_hp_amt4` with the APL charges amount (59.97).
  - `$tin_imaxdep_lim1` / `lim2` got wrong figures. OpenFisca agrees with
    EUROMOD on both.
- **Older figures on income-year parameters.**
  - These are `$tinty_dedpens_maxamt` (4 321 for 4 399), `$tscxc_thres4` /
    `thres6` and `$tintapv_lowlim`.
  - OpenFisca has a value for three of them, and agrees with EUROMOD on all
    three.
  - The income-year rule (`temporal_basis: income_year`) is the
    hardest FR rule, and a weak critique does not enforce it.

This is the §5.3 leniency at scale: the critique accepts the
proposer's choice of figure as long as the quote is verbatim. §8 point 6 had
predicted it.

### 9.5 What FR says about the §7 fixes

- **§7.1 (output cap, prompt trimming) works on long FR prompts.** C's 3
  errors are all the model's own: 2 `Exceeded maximum output retries` and 1
  `Model token limit (16384) exceeded before any response`. None is a
  provider refusing a long prompt, against 10 of 10 in LT run C.
- **§7.2 (consolidated text over amending acts) cannot be judged from FR.**
  It needs the LT re-run of §8 point 1.

### 9.6 Consequences

1. **For France, GPT stays the reference.** All-MiniMax M2.7 is not a
   replacement on a country this hard: it scores 41 % success against 70 %.
   The LT conclusion ("a viable candidate") holds for LT only.
2. **A stronger critique is the lever to test first for MiniMax.** Most of
   C's FR loss is wrong values its own critique accepted (§9.4). Run B
   (MiniMax proposing, a stronger critique) on FR would measure how much of
   that a stronger critique recovers.
3. **Run Azure full-country benchmarks at `-j 2`**, or raise the
   gpt-6-luna deployment's token-rate quota. At `-j 4`, 16 % of FR cases
   failed on the rate limit.
4. **Review the 15 GPT findings** with the EUROMOD team. They are what the
   project is for.
5. **Look for corpus gaps in `bhoey_fr`, `tscer_fr`, `tscse_fr`, `bsa00_fr`,
   `sickcomp_fr` and `bunmt_fr`**, where GPT abstains most. Start with the
   debug-phoenix-trace skill on their not_found traces.
