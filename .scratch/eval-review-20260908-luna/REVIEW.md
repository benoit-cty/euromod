# Review of eval run `eval-20260908T143801Z-gpt-5-6-luna-120a86`

Status: ready-for-human (fixes applied 2026-09-08 — see 'Actions taken' at the end; 8 cases await re-verification)
Reviewed: 2026-09-08 (Claude, /review-eval). Run: 100 cases (FR 52, NL 15, ES 11, IE 11, LT 11), as_of 2025-06-01, dataset ef3208b827f8, git 3feaa30.

## Model identity (verified)

manifest: model `azure_openai/gpt-5.6-luna` -> resolved `gpt-5.6-luna`; judge `azure_openai/gpt-5.6-sol` -> resolved `gpt-5.6-sol`.
Phoenix LLM spans over the run's 100 traces: 140 x `gpt-5.6-luna`, 66 x `gpt-5.6-sol`. The judge is a different model, so `supportedness` is not self-graded. This is the first run where a Sol deployment actually answered.

## The split (lead with this, not the headline)

| pool | n | routing | value |
|---|---|---|---|
| headline, all cases | 100 | 50% | 48% (n=90) |
| ready cases (report's own split) | 77 | 60% | 58% (n=71) |
| ready minus corpus / retrieval / input / golden buckets | 43 | 95% | 95% (n=38) |

Of the 77 ready cases, 34 could not measure the model:

- **14 corpus gaps the readiness flag misses** (all scored 0%): act ingested but no version in force on 2025-06-01, or the value-bearing act not ingested.
  - CSS art. D242-4: versions end 2023-12-31, next starts 2026-01-01 -> `fr_tscee_tsceepi_rate2`, `fr_tscer_tscerpi_rate1`, `fr_tscer_tscerpi_rate2` (as-of filter can never return it).
  - CSS art. D633-3: last version ends 2024-07-07 -> `fr_tscse_tscsepi_rate5`.
  - SWCA 2005 s. 13: versions end 2022-01-01 -> `ie_tscee_prsia_rate1`.
  - LIRPF DA 61.ª: first version starts 2025-07-26, after as_of -> `es_tin_wkintc_amt` (the case's own `budget_act_window` hazard; either move as_of or accept it is unanswerable at 1 June).
  - Value-bearing second act not ingested: Orden PJC/178/2025 (`es_constdef_tscft_ee_rate5`, the note says so), the 2025 LT social-fund budget indicators law (`lt_tsceepi_rate`), Wet minimumloon (`nl_chall_b2`; `nl_minwage_m` is already `no_corpus`), Participatiewet art. 22a formula element dropped by the NL parser (`nl_bsa_single_nonret_amt`, note says IMPOSSIBLE today).
  - CSS art. L136-8 CSG thresholds x4 (`fr_tinty_tscxc_thres3..6`): the 2025 amounts (16 755 / 4 474 / 26 004 / 6 941) live in Lettre ministérielle D-24-019252, no Legifrance id (the case notes say "references not resolved in the legislation corpus"). The article states the 2020 base amounts and says they are revalued yearly. Same class as the bch00 circulaire cases. The model proposed the base amounts as a change on three of them (false alarms) and refused correctly on the fourth.
- **9 retrieval misses** (0%): golden article ingested, in force, embedded, absent from the run's k=15. Re-run of the frame query at k=80 (CPU encoder): LIRPF art. 66 rank 75 / absent / absent (`es_tin_capinc_natrate5`, `_ratrate5`, `_schedule`), LIRPF art. 57 rank 3 offline but absent in the run (`es_tin_perall_amt1`), Finance Act 2024 s. 3 rank 52 (`ie_tin_perstc_amt`), GPMĮ 20 rank 26 (`lt_tinta_basic_withdrate_higher`), Wet IB 2001 art. 2.10 rank 25 and 58 (`nl_tin_bandlim2`, `nl_tin_br1`), Social Welfare Act 2024 s. 8 holds "109.50" but was not retrieved (`ie_bunct_rate1`), PSS arrêté JORFTEXT000050854392 in corpus but not retrieved for the 4xPSS ceiling (`fr_tscse_tscsepi_uplim`). Pattern: the vector top-3 (score ~1.016) were wrong articles and the FTS leg was noise; the frame queries are still full of EUROMOD prose (SchedCalc, BenCalc, Country Report table refs).
- **6 input defects** (0% routing):
  - `es_tin_capinc_schedule` and `lt_tin_schedule`: the group record has `label: None, description: None`, so the frame query was literally `ES Tax schedule` and `LT`. FR's schedule only worked because CR headings filled in. `paramdb.load_group_record` should compose a label from the members.
  - `fr_setdefault_minwage_hourly`: unit `currency/month` on an hourly value (known; correct refusal, counts as abstained).
  - `lt_pensionagefemale`: unit `currency` on an age. The model derived 64 y 8 m = 64.6667 correctly from the step schedule (the note called it IMPOSSIBLE) and `values_sane` rejected it on the unit. Also golden 64.66 vs 64.6667 fails the 1e-6 tolerance and the diff's 1e-9 tolerance routes it `changed`.
  - `nl_tin_br3`: the store holds `null` for NL percent strings (`params.model_values.value_kind=expression, value_raw=null` for `$tin_br1`; IE's `4.1%` survives as a string). Correct value 0.495 proposed, routed `changed` because the stored value is null. Same store defect hits `nl_tin_br1`, `lt_tsceepi_rate`.
  - `nl_bfa_mult2`: unit `/1` on a 1.2143 multiplier -> `values_sane` range 0..1 fails. Model also dropped the word "is" from the extract (non-verbatim), so it fails on two legs.
- **5 golden/scoring artifacts** (routing was right, a leg scored wrong):
  - `lt_tinta_max_amt`: expected `747#m`, proposal is a bare float 8964.0 (proposals never carry a period, parameter unit is `currency`) -> `values_equal` cannot cross-period and scores False. The case as designed is unscorable.
  - `ie_tin_high_rate`: golden citation `TCA 1997, s. 15` is not in the corpus -> permanent citation miss. FIXED in golden_sources/ie.json (citation now `Finance Act 2024, s. 3`; TCA kept in the note). Rebuilt; the case is back to verified:false and needs re-verification.
  - `fr_tinkt_tin_imaxwd_amt`: golden lists only `JORFTEXT000051168007, art. 2`; the pipeline cited the consolidated `CGI, art. 197` (correct, the critique granted the in-force presumption). OpenFisca-generated case; the builder should also emit the consolidated article.
  - `nl_impr_band5`: golden `Wet IB 2001, artikel 3.112`; pipeline cited `artikel 3.19` (same table, business dwelling). Arguable near-miss.
  - `es_bsa00_amt`: golden `Ley IMV Artículo 13`; pipeline cited the 2025 revalorisation act `1/2025 Artículo 65`. Both defensible; add the RDL 1/2025 article to the golden citations.

## What the model actually got wrong (2 of 43)

- `nl_bfa_bchqtr_amt`: proposed the € 409,21 basiskinderbijslagbedrag (lid 1) for the under-6 amount € 286,45 (lid 3a). The trap the note describes; a real miss.
- `ie_txcin_upthres2`: right value 27 382, right extract, chunk id typed `4a56d7eb…` for the retrieved `4a56d5eb…` on both attempts -> mechanically rejected. Correct rejection; a pipeline could resolve the extract back to a retrieved chunk instead of trusting a 36-char id (`fr_tinty_tscxc_thres5` put a citation string in the id field the same way).

Everything else in the clean pool: 41/41 routing, 36/36 value, including all 20 FR income-year cases and all four barème thresholds.

Direction: every defect above pushed the score down. The eval is pessimistic, not broken.

## Actions taken (2026-09-08, after the review)

Corpus (Nomotheca):
- CSS art. D242-4 version 2023-12-31→2026-01-01 (LEGIARTI000048852488) and D633-3 version 2024-07-07→ (LEGIARTI000049904636) ingested; both were listed as siblings in the stored DILA JSON `VERSIONS` block.
- Orden PJC/178/2025 (BOE-A-2025-3780, 77 units) ingested; art. 4 states the 23,60/4,70 split the ES solidarity-contribution case needs.
- LT law XV-46 (2025 social-fund budget indicators, TAR 2024-22173, 13 units) ingested. TAR never consolidates a never-amended act, so the adapter gained a `<id>/orig` fallback that parses the Dokumentas row's own text as the single dated version (`countries/lt/{fetcher,parser}.py`, test added).
- Wet minimumloon (BWBR0002638) ingested, but its art. 8 carries the statutory base `€ 10,60 per uur` in every toestand: the indexed amounts live in the semi-annual Stcrt regelingen, so `nl_minwage_m` and `nl_chall_b2` stay unanswerable from the text.
- Participatiewet art. 22a: the kostendelersnorm formula is a PNG (`<plaatje><illustratie type="tekst">`), not MathML. The NL parser now renders `[formule als afbeelding: 256403.png]` in its place (NL has no `reparse` path; the act was refetched). `nl_bsa_single_nonret_amt` is now `corpus_available: false` with a corrected note.
- SWCA 2005 s. 13 post-2022 versions: the IE adapter only ingests enacted texts (irishstatutebook `/enacted/en/xml`), not Law Reform Commission revised acts — an adapter feature, not done here.
- Embeddings: rebuilt on CPU/OpenVINO for the new chunks (the GPU is held by a stray `query_embeddings` process, pid 500237). No machine translation was run for the new ES/LT/NL/FR texts (billed LLM step).

Parameter store (Nomoscope):
- FR, IE and LT had been ingested from the August export while the September export (d173e2a) changed units: all five countries re-ingested and curated. `$PensionAgeFemale` is `age_years` now, straight from the export.
- `paramdb.normalise_value` reads percent literals (`8.17%` → 0.0817); NL/LT rates were stored as null and could never route `unchanged`.
- `load_group_record` composes a label/description from the members; the ES and LT schedule cases had run with the queries `ES Tax schedule` and `LT`.
- Four FR and one IE `model_target` rows carried a trailing newline from the July export and collided with the clean key on re-ingest; trimmed in the DB and stripped at ingest.
- Curation: FR `$Minwage_hourly` → `currency/hour`; NL `$bfa_mult2`/`$bfa_mult3` → `ratio` (both units added to `KNOWN_UNITS`); IE: a `national_team` block for all 268 `tco_ie` constants.

Pipeline:
- Critique: a `citation_chunk_id` that is not a retrieved chunk is resolved to the ONE retrieved chunk containing the `supporting_extract` verbatim (one-hex-digit typos, citation strings in the id field); two candidates keep the failure.
- `_QUERY_NOISE` also strips EUROMOD function names and Country Report/Table pointers. Measured over the 15 frame queries of the missed cases at k=15: golden article in the top 15 for 2 instead of 1 (`nl_tin_bandlim2` rank 11). The dominant problem is the vector top-3 slots going to wrong articles, not the FTS noise.
- `retrieval.hybrid_search` / `citation_fast_path` bind `dict_row` on their own cursor.

Eval (Nomokrisis):
- `score_item` completes a bare proposed scalar with the stored value's `#period` suffix before `values_equal` (`lt_tinta_max_amt`: 8964 vs `747#m` now compares). Rescored the run with `--write`: LT value 25% → 38%, ready 33% → 50%; nothing else moved.
- `openfisca_golden`: a reference OpenFisca titles "(seuils avant revalorisation)" no longer makes a case `corpus_available`, and an entry-level `corpus_available` override is honoured. The four L136-8 CSG threshold cases are now `no_corpus` (verdicts kept).
- Golden citations now list every acceptable article (`citation_correct` is any-of): `ie_tin_high_rate` → Finance Act 2024 s. 3; `fr_tinkt_tin_imaxwd_amt` → + `CGI, art. 197` (explicit entry); `nl_impr_band5` → + art. 3.19; `es_bsa00_amt` → + RDL 1/2025 art. 65 (BOE-A-2025-1560); `es_constdef_tscft_ee_rate5` → + Orden PJC/178/2025 art. 4; `lt_tsceepi_rate` → + XV-46 art. 3.
- `lt_pensionagefemale`: expected is the law's 64.6667 and routing `changed` (EUROMOD's 64.66 is a truncation, reported like IE's 27 383); difficulty `derive`.

Needs a human (`nomokrisis-eval verify <id> --reviewer …`), all reset by the rebuild because the ground truth moved: ie_tin_high_rate, fr_tinkt_tin_imaxwd_amt, nl_impr_band5, es_bsa00_amt, es_constdef_tscft_ee_rate5, lt_tsceepi_rate, lt_pensionagefemale, plus the 2 pre-existing unverified FR drafts the rebuild reports. `nomokrisis-eval run` drops unverified cases silently.

Still open:
- IE revised-act ingestion (SWCA 2005 s. 13, Sch. 2 after 2022).
- NL indexed minimum-wage amounts (Stcrt regelingen) and the art. 22a formula text (OCR or curated alt text).
- Retrieval: the vector leg's guaranteed top-3 slots went to the wrong article on every miss; worth revisiting the +1.0 bonus (`retrieval.hybrid_search`) with the golden set as the yardstick.
- Machine translation of the newly ingested texts.
