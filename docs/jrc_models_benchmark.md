# Benchmark of non-OpenAI models for the Nómos workflow (LT, 14–15 Nov 2026)

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
prompts. Two fixes followed from the analysis (§7). They are in the code but
not evaluated.

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
   leniency would cost most.

For a JRC deployment without OpenAI, **all-MiniMax M2.7 is a viable
candidate today**: about 8 points behind GPT on LT, with comparable precision,
a few dollars per country run. Most of the remaining gap is the two
issues fixed in §7.
