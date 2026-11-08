# LT 2025 benchmark: first full run, 8 Nov 2026

Status: ready-for-human
Run: `eval-20261108T100417Z-gpt-6-luna-a265f6` (agent 0.9.2, model `azure_openai/gpt-6-luna`, critique `gpt-6.1-sol`), same setup as the FR run `…1e30cd`.
Benchmark: blind EUROMOD 2024 → 2025 over every LT parameter with a value in force on 1 July 2025. That is 117 cases (18 changed, 93 unchanged, 2 derived, 4 national team); 38 parameters skipped, 4 of them scored inside their bracket schedule.

## Headline

**Success 86 / 117 = 73.5 %**, no findings. 0 errors, 100 % verbatim extracts, 0 hallucinations.

| metric | LT 0.9.2 | FR 0.9.2 |
|---|---|---|
| success | 73.5 % | 82.6 % |
| coverage | 75.7 % | 88.2 % |
| precision | 95.2 % | 88.3 % |
| change recall | **22.2 % (4/18)** | 70.2 % |
| unchanged confirmed | 81.7 % | 87.5 % |

The headline is carried by unchanged values. Of the 18 values that changed in 2025, only 4 were found. The cause is one ingest bug (below), not the model.

## What failed (31 cases)

| bucket | cases | what it is | status |
|---|---|---|---|
| **Resolutions and orders loaded empty** | 7: `MMS`, `NMMS`, `tscerhi_ratec`, `BSA`, `SSI`, `AssisPens`, `CBN` | The LT parser split acts on `N straipsnis` only. A Government resolution or a ministerial order has numbered points instead, so it loaded as an `istatymas` shell with no unit. The scout "ingested" the right act (minimum-wage resolution Nr. 709, Nr. 1206 on the social-assistance reference amounts, MVPD order A1-823), and the corpus still had no text. 10 such shells were created today alone | **fixed** (parser), acts re-ingested and embedded, not re-run |
| Unit curation | 7: six `xhcht_*_m3`, `bmact_MaxLim` | The model found the right values; the critique refused them for the unit. The water norms (m³/month) are labelled `currency`; `bmact_MaxLim` (2 × AMS) failed the `/1` range check | `bmact_MaxLim` → `ratio`, **fixed**; the m³ volumes need a decision (below) |
| In the corpus, not used | 4: `BasicPens`, `tsceepi_private_CredAmount2`, `bsg_amt`, `RP` | XV-46 art. 6 states the basic pension 298,45 € and is embedded, but the located step brought arts. 13 and 9 of the same act. XV-89 art. 9 states 30,33 €; art. 18 was retrieved instead. `bsg_amt` = 42,29 € is the widow's-pension base by reference, and the single-person benefit law is not ingested. The 2025 point value (`RP` 7,16) was not found in the corpus | retrieval: within-act article ranking for Lithuanian (no LT stemmer in FTS: «dydis» ≠ «dydį») |
| Convention mismatches | 4: `PensionAgeFemale/Male`, `tin_schedule`, `tin_schedule_2` | Pension age: proposed 64.6667 (64 y 8 m), EUROMOD holds 64.66 (truncated). Income-tax schedule: the model puts the 60 VDU threshold in the band, EUROMOD keeps 0 and applies 60 × VDU elsewhere | scorer or curation decision; the proposals are right in law |
| EUROMOD legacy parameters | 3: `tinta_basic_amt`, `tinta_basic_WithdRate`, `tinta_children_amt` | Pre-2022 basic-allowance method; the model correctly says the current law has no such parameter | candidates for `national_team_source` / exclusion |
| Other not found | 6: `AMSp` (a statistic, not law), `tin_LowRate`, `bplct_duration_m`, `bsa00_scale_coef2`, `tsceemi_rate`, `tsceesi_rate` | mixed | as for FR |

The scout also burned attempts on e-seimas `TAP/TAD` ids (Seimas drafts). TAR's open data does not serve them (`TAR returned no Suvestine row`), so every one fails.

## Fixes applied (not committed)

- `Nomotheca-RAG/ingest/src/nomotheca_ingest/countries/lt/parser.py`:
  - An act with no articles is split into its top-level points, with its preamble as its own unit, or into one whole-text unit.
  - Such an act is cited «2024 m. rugpjūčio 28 d. nutarimas Nr. 709 1 punktas».
  - Its type comes from `rusis` or the header.
  - It is keyed by `dokumento_id` on both the Dokumentas path and the consolidation path. «Nr. 709» or «V-524» is not unique, and the two paths disagreeing tripped `instruments_eli`.
  - Its title is the «Dėl …» line, not the issuer.
  - 3 tests; ingest suite 263 passed.
- Re-ingested 9 acts into the shells. The 2025 figures are now units:
  - MMA 1 038 € (Nr. 709 p. 1);
  - BSI 70 €, assistance-pension base 248 € and VRP 221 € (Nr. 1206, 2025 version);
  - MVPD 450 € (A1-823 p. 1).
  
  Embed job done: 2 508 chunks; LT 14 268 / 14 268 embedded.
- `curation/LT.curation.yaml`: `bmact_MaxLim` → `ratio`, applied with `curate-params`.
- CLAUDE.md: one line on LT resolutions next to the TAR `/orig` quirk.

## Re-run of the 31 failed cases (`eval-20261108T143048Z-gpt-6-luna-83add2`)

**9 recovered → 95 / 117 = 81.2 %** (full run's 86 + 9), change recall 9 / 18 = 50 % (was 22 %).

| outcome | cases |
|---|---|
| recovered by the parser fix | `MMS` 1 038, `BSA` 70, `SSI` 221, `CBN` 450 |
| recovered by the `ratio` curation | `bmact_MaxLim` |
| recovered, same corpus (variance) | `tsceepi_private_CredAmount2` 30,33, `bplct_duration_m`, `bsa00_scale_coef2`, `tsceesi_rate` |
| fix in the corpus, missed by retrieval | `AssisPens`: Nr. 1206 p. 4 retrieved, p. 2 (248 €) not; `tscerhi_ratec` = 6,98 % × 1 038 needs Nr. 709, not retrieved this time |
| not law | `NMMS` (EUROMOD's net-MMS approximation), `AMSp` (a statistic) |
| unchanged | the m³ volumes (unit), pension ages and `tin_schedule` (conventions), `tinta_*` (legacy), `BasicPens`, `RP`, `bsg_amt`, `tin_LowRate`, `tsceemi_rate` |

The 81.2 % combines two runs and assumes the 86 cases that passed in the full run still pass. Only a new full run (about 1½ h, billed) measures it in one go.

## Decisions and steps for you

1. Re-run of the 31 failed cases: done, see above.
2. **Two empty shells remain:** `V-1224` and `V-524`, two education-ministry orders the scout found, which are not EUROMOD-relevant. The cleanup `DELETE` was blocked in this session. Delete them, or leave them; nothing references them. The 8 other shells now hold their text but keep `instrument_type = 'istatymas'`, because the loader never updates a type. Retrieval filters on trust class, so this is cosmetic.
3. **A unit for volumes and durations** (`xhcht_*_m3`, `bplct_duration_m`): `KNOWN_UNITS` has none. This would mean a new unit in `paramdb.KNOWN_UNITS` and in the SQL check, with no range check, or reporting it to the economists with the `/1` batch.
4. **Convention cases:** say whether a pension age in years-and-months should be compared after truncation to EUROMOD's two decimals, and whether `tin_schedule`'s VDU-multiple threshold should be curated.
