# FR 2025 benchmark: improvements of 3–7 Nov 2026

Status: ready-for-human
Last full run: `eval-20261107T132321Z-gpt-6-luna-1e30cd` (agent 0.9.2, model `azure_openai/gpt-6-luna`, critique `gpt-6.1-sol`), 7 Nov, after all 130 FR contributed documents were reparsed with the footnote rule and re-embedded.
Previous full run: `eval-20261106T111405Z-gpt-6-luna-5565d9` (agent 0.9.1). Batches between the two: `eval-20261106T161223Z-…-2e6f83` (13 contribution cases) and `eval-20261107T093927Z-…-93cdcd` (0.9.2, 30 cases).
Benchmark: blind EUROMOD 2024 → 2025 over every FR parameter with a value in force on 1 July 2025. That is 345 cases.

On Tuesday the success rate was 34%, we are now above 80%.

## Headline

**Success 285 / 345 = 82.6 %** on the 0.9.2 full run, past the 80 % goal. That is 270 values equal to EUROMOD's (or routed around as expected) plus **15 findings** where EUROMOD is off the law. The findings are counted as successes and reported separately, with no tolerance (see below).

The batches had projected about 279 (80.9 %); the full run did better by 6. Against 0.9.1 it gained 23 cases and lost 8, a net of +15. The runs vary by about ±5 cases, so the gain is larger than run-to-run variance.

| run | agent | correct | findings | success |
|---|---|---|---|---|
| `…e1ed27` (3 Nov) | 0.3.0 | 136 | — | 39.4 % |
| `…5c7ac3` (4 Nov) | 0.5.0 | 177 | — | 51.3 % |
| `…0ca32d` (5 Nov) | 0.8.0 | 218 | — | 63.2 % |
| `…c79352` (6 Nov) | 0.8.3 | 248 | not scored | 71.9 % |
| `…5565d9` (6 Nov) | 0.9.1 | 252 | 18 | 78.3 % |
| **`…1e30cd` (7 Nov)** | **0.9.2** | **270** | **15** | **82.6 %** |

Runs before 0.9.0 were scored before the findings rule existed and were not re-scored, so their score is the "correct" column alone.

| metric | 0.9.1 | 0.9.2 |
|---|---|---|
| coverage (a value was proposed) | 83.5 % | 88.2 % |
| precision (proposed values that are right) | 87.0 % | 88.3 % |
| change recall | 66.5 % | 70.2 % |
| unchanged values confirmed | 80.3 % | 87.5 % |
| hallucination (non-verbatim quote, caught by the extract check, scored as rejected) | 3 | 1 |
| errors | 1 (Azure 429) | 0 |

Verbatim extracts are 100 % in what reaches the queue.

### 0.9.2 against 0.9.1, case by case

| | cases |
|---|---|
| **gained (23)** | RSA `amt9`, `hp_amt5`; prime d'activité `bsawk_hp_amt5`; AL `bchlg_lim4/6`, `bchlg_thres1`; AAH `bdi_lim3`; ASS `bunmt_bonus2`; `UB_QperMin`; IJ `bhl_day_thres_pf`, `bhl_std_rate3`; IR `tin_decote_lim2`, `tinkt_rate`, `tpr_threshold3`; `trewl_rate1`; APEC `tsceeui_rate2`, `tscerui_rate2`; FNAL `tscerho_rate1/2`; `tscerpi_rate7`; `tscsepi_farmers_rate3`; schedules `tscee:tsc_schedule`, `tsceesi_rate_schedule` |
| **lost (8)** | `bchyc_lim23`, `bchyc_lim31`, `bdi_lim1`, `bsa00_bonus_amt5`, `bsawk_hp_amt2`, `bhl_max_amt2`, `bhl_std_rate2b`, `casa_rate` |

Most of the losses are model variance: a not_found with the same evidence that passed in 0.9.1 (`bdi_lim1`, `bonus_amt5`, `hp_amt2`), an operand quote that misses its figure (`bhl_max_amt2`), and a CASA rate cited from the wrong article (`casa_rate`). Two of them come from the derived-result rule and deserve a note: on `bchyc_lim23` and `lim31` the model chose the wrong operands (43 946 × 1,1947 instead of the PAJE rule) and typed the right figure (52 504) next to a derivation that evaluates to 52 502,3. In 0.9.1 the 0,1 % tolerance kept the typed figure. Now the arithmetic decides, as it must: a figure the derivation doesn't produce is not supported.

### Findings: EUROMOD off the law
When the proposal passed the critique on a verbatim extract, and every figure where it parts from EUROMOD is exactly one unit of the held precision, the case is a **finding**. That means 0,01 on a cents amount or 1 on a whole one, never a rate. A finding is either stated in the extract or derived by a verified derivation.

`value_correct` stays False and there is no tolerance. The report gives findings their own column, and the `success` line adds them to the correct answers.

The findings (18 in 0.9.1, 15 in 0.9.2) include:
- AF 151,81 against the law's 151,80;
- the barème's 11 496 against 11 497;
- PAJE ceilings one euro off;
- RSA amounts one cent off (`amt7`, `amt10`);
- prime de Noël amounts (`bonus_amt5`).

They are for the EUROMOD economists team.

## What changed in 0.9.x (6–7 Nov)

### Corpus: sources the contribution cases needed
- **ANI APEC du 12 juillet 2011:** the signed PDF is a scan, and there is no OCR, so a Markdown transcription was contributed as a collective agreement (evidence). Art. 14 states 0,036 / 0,024 pour 100. The APEC cases (`tsceeui_rate2`, `tscerui_rate2`) went from not_found to correct.
- **Agirc-Arrco circulars «Paramètres 2025» (2024-18-DRJ) and «Paramètres 2026» (2025-16-SG-DRJ)**, as guidance. They state the tranche rates, CEG, CET and APEC.
- **AGS brève of 17 Dec 2025** (guidance). It states only the 2026 rate, so `tscerwgf_rate` correctly stays not_found: it needs an AGS source dated 2025.
- **A `.pdf` URL that no browser can fetch is refused** instead of ingesting the HTML page in its place. The AGS 2025 PDF had been ingested as the press-release listing.

### 0.9.2 (measured on the 30-case batch)
- **Derivations: the arithmetic decides the value** (`pipeline._round_like_held`). The check accepted a result within 0.1 % of the typed figure, and RSA 646,52 × (1,28412 + 2 × 0,42804) = 1 383,68 was typed and kept as 1 383,28. The verified result is now rounded like the held value. → `bsa00_amt9` is correct.
- **One more attempt when the only objection is a misquote** (`pipeline._misquoted_only`). The attempt after `locate` was the last one, and «calculé pour trois personnes ou plus lorsque» was refused with the exact passage in hand. → RSA forfait logement `hp_amt2`, `hp_amt4`, `hp_amt5` and prime d'activité `bsawk_hp_amt5` are correct. The verbatim check is unchanged.
- **Schedules are searched in the law's language** (`paramdb._group_texts`). A group now composes a French label and description from its members' French texts. In English, the AGIRC-ARRCO schedule never reached the circular. → `tscee:tsc_schedule` (7,30 % / 0,40 %) and `tsceesi_rate_schedule` are correct.
- **Footnotes are no longer sections** (`documents.drop_table_rows`). Bare numbers that start over are footnotes. Circular 2024-18 reads 1 | 1 2 3 | 1, and its 2025 rate table was a "section" headed by a footnote. All 130 FR documents were reparsed on 7 Nov before the full run.
- **Scoring: a band with no rate equals a 0 % band.** EUROMOD's CEHR first band has no rate member, and a proposal stating 0 % for it scored as a wrong schedule. Re-scoring the full run changes nothing; the batch gains `tinto_schedule`.

### Measured on the full run
- **Articles of the same act that name a retrieved one** (`retrieval._same_act_citing`). ANI AGIRC-ARRCO art. 36, «un pourcentage d'appel, fixé à 127 %, est appliqué aux taux visés à l'article 35», now comes with art. 35. The employee schedules `tscee:tsc_schedule` and `_2` pass in the full run, and `tscerpi_rate4` derives 6,20 % × 127 % × 60 % from art. 35/36. `ConstDef:tsc_schedule` and `_2` are still not_found. In `_2` the model's own refusal names arts. 35, 36 and 38, so the articles are in view now; it ran out of attempts before writing the 6-figure schedule.
- **All FR contributed documents reparsed with the footnote rule** (130 documents, embed job 480). No case that passed in 0.9.1 was lost to it.

### 0.9.2 batch, case by case (30 cases that failed or were findings in the full run)

| outcome | cases |
|---|---|
| gained (7, +1 after re-scoring) | `bsa00_amt9`, `bsa00_hp_amt2/4/5`, `bsawk_hp_amt5`, `tscee:tsc_schedule`, `tsceesi_rate_schedule`, `tinto_schedule` (re-score) |
| kept | `amt7`, `amt10`, `bonus_amt5` (findings), `bonus_amt2` (now exact), `tin_schedule` (finding), `tinto_schedule_2`, `tscee:tsc_schedule_2` |
| lost (1) | `ConstDef:tsc_schedule_3` (CET employee 0,14 %): the model would not derive it from the overall 0,35 % and the circular was not retrieved. Variance on a fragile case; the not-yet-measured art. 36 change targets it |
| still failing | prime d'activité `bsawk_hp_amt3/4`, `bsawk_minamt1/3/5` (not found, see below); `bsa00_amt8` (wrong composition); `bsa00_hp_amt3` (operand quote again); AGIRC-ARRCO `tsc_schedule/_2`; self-employed and farmers' schedules |

## What changed up to 0.8.3 (3–6 Nov)

### Retrieval: getting the act that states this year's figure into view
- **Implementing acts, with references followed backwards** (`retrieval.implementing_acts`). A code article that says «fixé par décret» brings the recent non-code acts that name it:
  - CASF L. 262-2 → the décret du 28 mars 2025 (RSA 646,52 €);
  - CSS L. 842-3 → the prime d'activité decree (633,21 €);
  - R. 522-2 → instruction DSS/2B/2024/181.
  
  This includes acts that name the article in a list closed by the code's name. The 20 best-ranked code articles are looked at, the acts are ranked by distance to the query, and each act also brings its two chunks nearest to the query.
- **Recent texts for a named need** (`locate_named_units`): after a not_found, the need's words are also searched over texts that entered into force in the last year.
- **Code lists** («Articles L. 381-1, …, R. 522-2 … du code de la sécurité sociale») are read as references to each article.

### Corpus
- **Guidance:** DSS/2B/2025/38 (BMAF and the April 2025 revaluations), DSS/2B/2024/181 (family-benefit ceilings for 2025), the CAF EAJE barème 2025, and the CSG instruction of 4 Dec 2024.
- **Evidence:** CSS D. 843-1.
- **PDF splitting:** table rows and dates are no longer turned into headings.
- **Bulletin officiel:** a `.pdf` URL that answers a script with HTML is retried once in headless Firefox.

### Verification: fewer right values refused, same anti-hallucination guarantee
- **A quote that sits in another retrieved chunk** is re-pointed to the one retrieved chunk that holds it. A citation string or a corrupted UUID in the id field is resolved by the extract.
- **PDF artefacts are tolerated:** whitespace runs, a split ligature between letters, and punctuation at a quote's ends.
- **Derivations:**
  - numbers the law spells out are accepted;
  - «majoré de 50 %» states 1.5;
  - the months 3, 6 and 9 are allowed constants;
  - rates are rounded like the value held;
  - a PDF table row states each of its amounts;
  - the retry is shown the sentence stating a missed figure.
- **Confirming the held value:** a start-date objection becomes a note.
- **"FYA" amounts** are proposed as the amount in force, never averaged.

## What still fails (60 cases in the 0.9.2 full run)

| bucket | cases | what it is | lever |
|---|---|---|---|
| EUROMOD conventions or stale values | ~23 | Unchanged from the 0.8.3 review: `tpr_threshold*` lag a year, `bho_rl_rate2/3` are held in points, `tscsesi_*` are aggregates, `bsawk_income_rate`, `UB_dayfixamt`, `tinty_dedub_uplim` (switched off). New: the **2025 self-employed reform is not modelled**. D633-3 says 0,72 % (EUROMOD 0,60 % until 2026). D635-7 says 8,1 / 9,1 % up to 1 / 4 PSS, where EUROMOD keeps 7 / 8 % up to an RCI ceiling of 43 891 (`sched_schedule_3`, `tscsepi_schedule`, `tscsepi_uplim`). These are findings bigger than one unit, so they don't count | report to the EUROMOD team; or a curation decision |
| Prime d'activité scale | 5 | The model refuses to apply the D843-1 uplifts (+50 %, +30 %, +40 %) to the 633,21 € base. It wrongly reads them as RSA-only, or lacks the 633,21 € decree in its hits. `minamt4` and `hp_amt5` succeed with the same evidence | prompt: say that D843-1 is the prime d'activité scale; make sure the décret naming L. 842-3 is always retrieved with D843-1 |
| AGIRC-ARRCO schedules | 2 | `ConstDef:tsc_schedule`, `_2`: arts. 35/36/38 are now retrieved, but the model refuses or runs out of attempts before writing the full schedule | a schedule-derivation example in the prompt; the circular's table chunk still ranks low in the vector leg |
| Contributions with no source | ~6 | AGS for 2025 (`tscerwgf_rate`); employee rates of 0 % that no text states (`tsceeui_rate1`); FNAL `tscerho_*`; farmers' vieillesse `sched_schedule` | corpus: an AGS release dated 2025, Urssaf barèmes as a guidance publisher |
| Model reasoning errors | ~12 | `bsa00_amt8` (lone-parent coefficients for a couple), `bched_amt2`, `bchlg_thres1`, `tscer_red_coef2`, … | variance; two proposals per case |
| Other not found | ~17 | prime de fin d'année variants, ASF, `bhl_max_amt1/2`, … | as in the 0.8.3 review |

## Decisions and steps for you

1. **The 0.9.2 full run is done**: 82.6 % success (see the headline). The goal is reached. A second full run would show how much of the margin over 80 % is variance; it's billed and needs the GPU for about 5½ h.
2. **The other contributed documents were reparsed with the footnote rule** (7 Nov, approved by you): all 130 FR documents (`cli reparse-documents -j FR`), then embed job 480 (2 739 chunks). Some Cnav circulars lost their footnote sections (2026/29: 109 → 101 units, 2025/08: 33 → 32, 2024/44: 17 → 16). The full run above measures the effect.
3. **AGS rate for 2025:** save the AGS release that followed the board of 2 Dec 2024 or of 18 June 2025. ags-garantie-salaires.org does not serve it to a script; I'll ingest it.
4. **The golden set (separate from the benchmark)** was reviewed on 7 Nov with what the benchmark taught us: 59 FR cases now, 40 of them reset to `verified: false`. See `Nomokrisis-evaluation_pipeline/golden_set_FR.md`.
   - It added citations to 18 cases that are now answerable.
   - It corrected two wrong expectations: `tinty_dedub_uplim` (national team) and `tscsepi_uplim` (47 100, not 43 891).
   - It added seven curated cases: a collective agreement, AGIRC-ARRCO arithmetic, the first ready derivations, a later-in-year act, `start_of_year`, and a one-cent finding.
   - The builder now takes `exclude: true` per entry and `fill_from_links: false` in the header.
   - Re-verify the reset cases in the UI's Golden set tab.

## Housekeeping

- **Nothing is committed.** The working tree holds all changes: pipeline, ingest, eval, tests, CLAUDE.md and `golden_set_FR.md`.
- **Tests:**
  - Pipeline: 162 passed. `test_encode_client.py::test_no_worker_is_a_timeout` fails whenever the worker is up, as before.
  - Ingest: 260 passed.
  - Eval: 96 passed.
- **Agent version** is 0.9.2. The 30-case batch started before the bump, so `eval.runs` records it as 0.9.1. It did run the four 0.9.2 changes listed under "0.9.2 (measured on the 30-case batch)". The full run `…1e30cd` is recorded as 0.9.2 and was re-scored with `--write` (no change).
