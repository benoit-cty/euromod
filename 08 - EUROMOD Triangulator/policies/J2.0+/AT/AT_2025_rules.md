# EUROMOD Tax-Benefit Rules for AT_2025

## Policy: ConstDef_at
### 1. Function: DefConst
  **Constants Defined:**
  - `$tsc_minThres1`: 551.10#m
  - `$tsc_maxThres1`: 6450#m
  - `$tscse_maxThres2`: 7525#m
  - `$tscse_minThres4`: 551.10#m
  - `$tscse_minThres3`: 551.10#m
  - `$tscse_minThres2`: 1016.97#m

### 2. Function: DefConst
  **Constants Defined:**
  - `$UB_QperMin1`: 12
  - `$UB_QperTot1`: 24
  - `$UB_QperMin2`: 6.5
  - `$UB_QperTot2`: 12
  - `$UB_QperMin3`: 6
  - `$UB_QperTot3`: 12

### 3. Function: DefConst
  **Constants Defined:**
  - `$PensionAgeMale`: 65
  - `$PensionAgeFemale`: 61
  - `$ImputedWage`: 0
  - `$bun_minAmt`: 42.47#d
  - `$bun_maxAmt`: 76.75#d

### 4. Function: DefConst
  **Constants Defined:**
  - `$lhwpt`: 25
  - `$lhw`: 42

### 5. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$tco_CIA_01`: 0
  - `$tco_CIA_12`: 0
  - `$tco_CIA_11`: 0
  - `$tco_CIA_10`: 0
  - `$tco_CIA_09`: 0
  - `$tco_CIA_08`: 0
  - `$tco_CIA_07`: 0
  - `$tco_CIA_06`: 0
  - `$tco_CIA_05`: 0
  - `$tco_CIA_04r`: 0
  - `$tco_CIA_03`: 0
  - `$tco_CIA_02`: 0
  - `$tco_CIA_045`: 0
  - `$tco_CIAon`: 1

### 6. Function: DefConst
  **Constants Defined:**
  - `$bsa_BTA_rate`: 1
  - `$bsa_BCA_rate`: 1


---

## Policy: random_at
### 1. Function: RandSeed
  - **seed**: `152331`

### 2. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `temp_rand`
  **Tax Unit:** `tu_bcc_at`
  **Run Condition:** `!IsUsedDatabase#1`

### 3. Function: DefVar
  - **temp_rand**: `0`
  - **i_mc_rand_se**: `0`
  - **i_mc_rand_1**: `0`
  - **i_mc_rand_3**: `0`
  - **i_lma_rand_1**: `0`
  - **i_lma_rand_2**: `0`
  - **i_lmamy**: `0`
  - **i_mc_rand_2**: `0`
  - **i_bsa_rand**: `0`

### 4. Function: ArithOp
  **Formula:** `bccdu`
  **Output Variable:** `temp_rand`
  **Tax Unit:** `tu_bcc_at`
  **Run Condition:** `IsUsedDatabase#1`

### 5. Function: RandSeed *(Switch: n/a)*
  - **Seed**: `17`

### 6. Function: ArithOp *(Switch: n/a)*
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_se`
  **Tax Unit:** `tu_individual_at`

### 7. Function: RandSeed *(Switch: n/a)*
  - **Seed**: `19`

### 8. Function: ArithOp *(Switch: n/a)*
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_ee`
  **Tax Unit:** `tu_individual_at`

### 9. Function: RandSeed *(Switch: n/a)*
  - **Seed**: `20`

### 10. Function: ArithOp *(Switch: n/a)*
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_2`
  **Tax Unit:** `tu_individual_at`

### 11. Function: RandSeed *(Switch: n/a)*
  - **Seed**: `21`

### 12. Function: ArithOp *(Switch: n/a)*
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_3`
  **Tax Unit:** `tu_individual_at`

### 13. Function: RandSeed *(Switch: n/a)*
  - **Seed**: `22`

### 14. Function: ArithOp *(Switch: n/a)*
  **Formula:** `rand`
  **Output Variable:** `i_lma_rand_1`
  **Tax Unit:** `tu_individual_at`

### 15. Function: RandSeed *(Switch: n/a)*
  - **Seed**: `23`

### 16. Function: ArithOp *(Switch: n/a)*
  **Formula:** `rand`
  **Output Variable:** `i_lma_rand_2`
  **Tax Unit:** `tu_individual_at`

### 17. Function: ArithOp *(Switch: n/a)*
  **Formula:** `rand`
  **Output Variable:** `i_lmamy`
  **Tax Unit:** `tu_individual_at`

### 18. Function: RandSeed *(Switch: n/a)*
  - **Seed**: `24`

### 19. Function: RandSeed *(Switch: n/a)*
  - **Seed**: `n/a`

### 20. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 21. Function: RandSeed
  - **Seed**: `202402291639`

### 22. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_bsa_rand`
  **Tax Unit:** `tu_individual_at`


---

## Policy: IlDef_at
### 1. Function: DefIl
  - **name**: `il_sicee01`
  - **tsceehl01_s**: `+`
  - **tsceepi01_s**: `+`
  - **tsceeui01_s**: `+`
  - **tsceeho_s**: `+`
  - **tsceeot_s**: `+`
  - **tscpehl01_s**: `+`
  - **tscpepi01_s**: `+`

### 2. Function: DefIl
  - **name**: `il_sicee02`
  - **tsceehl02_s**: `+`
  - **tsceepi02_s**: `+`
  - **tsceeui02_s**: `+`
  - **tscpehl02_s**: `+`
  - **tscpepi02_s**: `+`

### 3. Function: DefIl
  - **name**: `il_taxcredits`
  - **tintcch_s**: `+`

### 4. Function: DefIl
  - **name**: `il_mtpmmtu`
  - **ils_origy**: `+`
  - **ils_pen**: `+`
  - **bac00**: `+`
  - **bunct_s**: `+`
  - **bunnc_s**: `+`
  - **bhl00**: `+`
  - **bma**: `+`
  - **il_sicee01**: `-`
  - **ils_sicse**: `-`
  - **pxp00**: `-`
  - **yemxp**: `-`
  - **bhlxp**: `-`
  - **ils_tax**: `-`
  - **buntr**: `+`
  - **bunot**: `+`
  - **pxpot**: `-`
  - **bac01**: `+`
  - **bmact_s**: `+`

### 5. Function: DefIl
  - **name**: `il_progressionadj`
  - **bunct_s**: `+`
  - **bunnc_s**: `+`
  - **buntr**: `+`
  - **bunot**: `+`

### 6. Function: DefIl
  - **name**: `il_grosspartnery`
  - **yem**: `+`
  - **yse**: `+`
  - **yiy**: `+`
  - **bhl00**: `+`
  - **ypr**: `+`
  - **ils_pen**: `+`
  - **bma**: `+`
  - **ypp01**: `+`
  - **ypp02**: `+`
  - **bmact_s**: `+`
  - **yemmc_s**: `n/a`

### 7. Function: DefIl
  - **name**: `il_bunnc`
  - **yem**: `+`
  - **yse**: `+`
  - **ypp01**: `+`
  - **ypp02**: `+`
  - **ypr**: `+`
  - **ils_pen**: `+`
  - **bhl00**: `+`
  - **yemxp**: `-`
  - **pxp00**: `-`
  - **bhlxp**: `-`
  - **pxpot**: `-`
  - **ypt**: `+`
  - **bfaam**: `+`
  - **yemmc_s**: `n/a`

### 8. Function: DefIl
  - **name**: `il_child`
  - **ils_origy**: `+`
  - **bhl00**: `+`
  - **il_sicee01**: `-`
  - **tscpehl01_s**: `+`
  - **tscpepi01_s**: `+`
  - **ils_sicse**: `-`
  - **yemxp**: `-`
  - **bhlxp**: `-`
  - **temp_costearn
**: `-`
  - **temp_exdeduct**: `n/a`

### 9. Function: DefIl
  - **name**: `il_multiplech`
  - **ils_origy**: `+`
  - **ils_pen**: `+`
  - **bhl00**: `+`
  - **il_sicee01**: `-`
  - **ils_sicse**: `-`
  - **yemxp**: `-`
  - **bhlxp**: `-`
  - **pxp00**: `-`
  - **temp_costearn
**: `-`
  - **temp_exdeduct**: `n/a`
  - **pxpot**: `-`

### 10. Function: DefVar
  - **temp_yemxp**: `0`
  - **temp_pxp**: `0`
  - **temp_bhlxp**: `0`
  - **temp_pxpot**: `0`

### 11. Function: ArithOp
  **Formula:** `yemxp`
  **Output Variable:** `temp_yemxp`
  **Tax Unit:** `tu_individual_at`

### 12. Function: ArithOp
  **Formula:** `pxp00`
  **Output Variable:** `temp_pxp`
  **Tax Unit:** `tu_individual_at`

### 13. Function: ArithOp
  **Formula:** `bhlxp`
  **Output Variable:** `temp_bhlxp`
  **Tax Unit:** `tu_individual_at`

### 14. Function: ArithOp
  **Formula:** `pxpot`
  **Output Variable:** `temp_pxpot`
  **Tax Unit:** `tu_individual_at`

### 15. Function: DefIl
  - **name**: `il_taxablepartnery`
  - **yem**: `+`
  - **yse**: `+`
  - **ils_pen**: `+`
  - **ypp01**: `+`
  - **ypp02**: `+`
  - **bhl00**: `+`
  - **bma**: `+`
  - **ils_sicdy**: `-`
  - **temp_yemxp**: `-`
  - **temp_pxp**: `-`
  - **temp_bhlxp**: `-`
  - **temp_costearn
**: `-`
  - **temp_pxpot**: `-`
  - **ypr**: `+`
  - **bmact_s**: `+`
  - **yemmc_s**: `n/a`

### 16. Function: DefIl
  - **Name**: `il_taxableY`
  - **tintace_s**: `-`
  - **yemxp**: `-`
  - **ils_sicse**: `-`
  - **il_sicee01**: `-`
  - **ypp02**: `+`
  - **ypp01**: `+`
  - **bhl00**: `+`
  - **ils_pen**: `+`
  - **yse**: `+`
  - **yem**: `+`
  - **tintatb_s**: `-`
  - **tintaxp_s**: `n/a`
  - **tintach_s**: `n/a`
  - **pxp00**: `-`
  - **bhlxp**: `-`
  - **tintase_s**: `-`
  - **pxpot**: `-`
  - **ypr**: `+`
  - **yemmc_s**: `n/a`
  - **tintahl_s**: `-`
  - **bec02_s**: `n/a`
  - **bec04_s**: `n/a`
  - **i_bclmc_tax_s**: `n/a`
  - **yempv**: `+`

### 17. Function: DefIl
  - **name**: `il_bunncp`
  - **yem**: `+`
  - **yse**: `+`
  - **ypp01**: `+`
  - **ypp02**: `+`
  - **ypr**: `+`
  - **ils_pen**: `+`
  - **bhl00**: `+`
  - **il_sicee01**: `-`
  - **ils_sicse**: `-`
  - **yemxp**: `-`
  - **pxp00**: `-`
  - **bhlxp**: `-`
  - **tin_s**: `-`
  - **pxpot**: `-`
  - **bunct_s**: `+`
  - **ypt**: `+`
  - **bfaam**: `+`
  - **yemmc_s**: `n/a`

### 18. Function: DefIl
  - **Name**: `il_tins`
  - **tin_s**: `+`

### 19. Function: DefVar
  - **temp_costearn
**: `0`
  - **temp_exdeduct**: `n/a`

### 20. Function: DefIl
  - **Name**: `il_bma`
  - **bmact_s**: `+`
  - **bma**: `+`

### 21. Function: DefIl
  - **Name**: `il_tahealth`
  - **yem**: `+`
  - **yse**: `+`
  - **yemmc_s**: `n/a`
  - **ils_pen**: `+`
  - **bhl00**: `+`
  - **ypp01**: `+`
  - **ypp02**: `+`
  - **ypr**: `+`
  - **il_sicee01**: `-`
  - **ils_sicse**: `-`
  - **tintace_s**: `-`
  - **tintaxp_s**: `n/a`


---

## Policy: tudef_at
### 1. Function: DefTu
  - **Name**: `tu_hh_oecd_co`
  - **Type**: `HH`
  - **DepChildCond**: `dag<14`

### 2. Function: DefTu
  - **Name**: `tu_household_at`
  - **Type**: `HH`
  - **DepChildCond**: `dag<=15 | ((dag<=18 & (dec>=2 & dec<=4)) & !IsWithPartner & !IsMarried)`
  - **LoneParentCond**: `Default & !IsMarried & idpartner=0`

### 3. Function: DefTu
  - **Name**: `tu_individual_at`
  - **Type**: `IND`

### 4. Function: DefTu
  - **name**: `tu_partners_at`
  - **type**: `SUBGROUP`
  - **members**: `Partner`
  - **PartnerCond**: `Default`
  - **HeadDefInc**: `ils_pen`

### 5. Function: DefTu
  - **name**: `tu_pch_at`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild & LooseDepChild & DepParent`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`
  - **DepChildCond**: `default & (dag<=18 | (dag>18 & dag<27 & (IsInEducation | IsDisabled)))`

### 6. Function: DefTu
  - **name**: `tu_bcc_at`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild & LooseDepChild`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`
  - **DepChildCond**: `default & dag<=3`
  - **ExtHeadCond**: `!IsDepChild`

### 7. Function: DefTu
  - **name**: `tu_bfamt_at`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild & LooseDepChild`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`
  - **DepChildCond**: `default & dag>=1 & dag<3`
  - **ExtHeadCond**: `!IsDepChild`

### 8. Function: DefTu
  - **name**: `tu_bch00_at`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild & LooseDepChild & DepParent`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting) & ((nDepChildrenInTu=nLooseDepChildrenInTu & nDepChildrenInTu#1>0 & dag>=36) | (nDepChildrenInTu=nLooseDepChildrenInTu & nDepChildrenInTu#1=0)  | (nDepChildrenInTu!=nLooseDepChildrenInTu))`
  - **#_AgeMin**: `19`
  - **#_AgeMax**: `23`
  - **DepChildCond**: `default & (dag<=18 | (dag>18 & dag<24 & (dec>0 | IsDisabled)))`
  - **ExtHeadCond**: `!IsDepChild`
  - **NoChildIfHead**: `no`
  - **NoChildIfPartner**: `no`

### 9. Function: DefTu
  - **name**: `tu_bch01_at`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild & LooseDepChild & DepParent`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`
  - **DepChildCond**: `default & (dag<=18 | (dag>18 & (dec>0 | IsDisabled | bchditu>0)))`
  - **ExtHeadCond**: `!IsDepChild`
  - **NoChildIfHead**: `no`
  - **NoChildIfPartner**: `no`

### 10. Function: DefTu
  - **name**: `tu_unemplpartners_at`
  - **type**: `SUBGROUP`
  - **members**: `Partner`
  - **PartnerCond**: `Default`


---

## Policy: neg_at
### 1. Function: DefVar
  - **temp_yse0**: `0`

### 2. Function: ArithOp
  **Formula:** `yse`
  **Output Variable:** `temp_yse0`
  **Tax Unit:** `tu_individual_at`

### 3. Function: Max
  - **val**: `0`
  - **output_var**: `yse`
  - **TAX_UNIT**: `tu_individual_at`


---

## Policy: yem_at *(Switch: off)*
### 1. Function: DefConst
  **Constants Defined:**
  - `$Nwh`: 40
  - `$Minwage`: 1500#m

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem > 0`
  - **Tax Unit:** `tu_individual_at`

### 3. Function: ArithOp
  **Formula:** `yem`
  **Output Variable:** `temp_count`
  **Tax Unit:** `tu_individual_at`

### 4. Function: Max
  - **who_must_be_elig**: `one`
  - **val**: `$Minwage * (min(lhw, $Nwh)) / $Nwh * 14/12 * yemmy / 12`
  - **output_var**: `temp_overwrite`
  - **TAX_UNIT**: `tu_individual_at`

### 5. Function: Max
  - **who_must_be_elig**: `one`
  - **val**: `$Minwage * (min(lhw, $Nwh)) / $Nwh * 14/12 * yemmy / 12`
  - **output_var**: `yem`
  - **TAX_UNIT**: `tu_individual_at`

### 6. Function: ChangeParam
  - **Param_Id**: `99d0620a-80da-47e4-8224-c4060b391aaf`
  - **Param_NewVal**: `at_2025_yem_std`

### 7. Function: DefVar
  - **temp_count**: `0`
  - **temp_overwrite**: `0`


---

## Policy: tscer_at
### 1. Function: DefVar
  - **temp_basepenreg**: `0`
  - **temp_basepenspec**: `0`
  - **temp_basespec**: `0`
  - **temp_basereg**: `0`
  - **temp_maxpenmy**: `0`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yem-yemxp)>=$tsc_minThres1 * yemmy / 12`
  - **Tax Unit:** `tu_individual_at`

### 3. Function: ArithOp
  **Formula:** `yem-yemxp`
  **Output Variable:** `temp_basereg`
  **Tax Unit:** `tu_individual_at`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yemxp>=$tsc_minThres1 * 2/ 12 * yemmy/12`
  - **Tax Unit:** `tu_individual_at`

### 5. Function: ArithOp
  **Formula:** `yemxp`
  **Output Variable:** `temp_basespec`
  **Tax Unit:** `tu_individual_at`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=1`
  - **Tax Unit:** `tu_individual_at`

### 7. Function: ArithOp
  **Formula:** `yem*$tscerac_cs_rate`
  **Output Variable:** `tscerac_s`
  **Tax Unit:** `tu_individual_at`

### 8. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=0 & dag>=18 & dag<60`
  - **Tax Unit:** `tu_individual_at`

### 9. Function: ArithOp
  **Formula:** `(temp_basereg+temp_basespec)*$tscerac_ee_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 10. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=1`
  - **Tax Unit:** `tu_individual_at`

### 11. Function: ArithOp
  **Formula:** `(temp_basereg+temp_basespec)*$tscerhl_cs_rate`
  **Output Variable:** `tscerhl_s`
  **Tax Unit:** `tu_individual_at`

### 12. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `lsepf=1 & dag>=17`
  - **Tax Unit:** `tu_individual_at`

### 13. Function: ArithOp *(Switch: n/a)*
  **Formula:** `(temp_basereg+temp_basespec)*$tscerhl_pf_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 14. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `lcl=1 & lcs=0  & dag>=17`
  - **Tax Unit:** `tu_individual_at`

### 15. Function: ArithOp *(Switch: n/a)*
  **Formula:** `(temp_basereg+temp_basespec)*$tscerhl_bc_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 16. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `lcl=3 & dag>=17`
  - **Tax Unit:** `tu_individual_at`

### 17. Function: ArithOp *(Switch: n/a)*
  **Formula:** `(temp_basereg+temp_basespec)*$tscerhl_fa_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 18. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `(lcl=2 | lcl=0) & lcs=0 & lsepf=0 & dag>=17`
  - **Tax Unit:** `tu_individual_at`

### 19. Function: ArithOp *(Switch: n/a)*
  **Formula:** `(temp_basereg+temp_basespec)*$tscerhl_wc_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 20. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yem-yemxp)<$tsc_minThres1*yemmy/12 & dag>=18`
  - **Tax Unit:** `tu_individual_at`

### 21. Function: ArithOp
  **Formula:** `yem*$tscerhl_min_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 22. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=0 & (((dag<65 | dag>67) & dgn=1) | ((dag<61 | dag>63) & dgn=0))`
  - **Tax Unit:** `tu_individual_at`

### 23. Function: ArithOp
  **Formula:** `(temp_basereg+temp_basespec)*$tscerpi_ee_rate`
  **Output Variable:** `tscerpi_s`
  **Tax Unit:** `tu_individual_at`

### 24. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yem-yemxp)<$tsc_minThres1*yemmy/12 & lcs=0`
  - **Tax Unit:** `tu_individual_at`

### 25. Function: ArithOp
  **Formula:** `yem*$tscerpi_ee_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 26. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=0 & dag>=18 & ((dag<63 & dgn=1) | (dag<61 & dgn=0))`
  - **Tax Unit:** `tu_individual_at`

### 27. Function: ArithOp
  **Formula:** `(temp_basereg+temp_basespec)*$tscerui_rate`
  **Output Variable:** `tscerui_s`
  **Tax Unit:** `tu_individual_at`

### 28. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lsepf=0 & lcl!=3 & dag>=18`
  - **Tax Unit:** `tu_individual_at`

### 29. Function: ArithOp
  **Formula:** `temp_basereg*$tscerho_rate`
  **Output Variable:** `tscerho_s`
  **Tax Unit:** `tu_individual_at`

### 30. Function: Elig
  **Eligibility Check:**
  - **Condition:** `((dag<63 & dgn=1) | (dag<61 & dgn=0)) & lcs=0 & dag>=18`
  - **Tax Unit:** `tu_individual_at`

### 31. Function: ArithOp
  **Formula:** `(temp_basereg+temp_basespec)*$tscersf_rate`
  **Output Variable:** `tscersf_s`
  **Tax Unit:** `tu_individual_at`

### 32. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag<60 & lcs=0`
  - **Tax Unit:** `tu_individual_at`

### 33. Function: ArithOp
  **Formula:** `yem*$tscerfa_rate`
  **Output Variable:** `tscerfa_s`
  **Tax Unit:** `tu_individual_at`

### 34. Function: ArithOp
  **Formula:** `max(poamy,psumy)`
  **Output Variable:** `temp_maxpenmy`
  **Tax Unit:** `tu_individual_at`

### 35. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ils_pen-pxp00-pxpot)>=$tsc_minThres1 * temp_maxpenmy / 12`
  - **Tax Unit:** `tu_individual_at`

### 36. Function: ArithOp
  **Formula:** `ils_pen-pxp00-pxpot`
  **Output Variable:** `temp_basepenreg`
  **Tax Unit:** `tu_individual_at`

### 37. Function: Elig
  **Eligibility Check:**
  - **Condition:** `les=4 & poacs>0 & pxp00>=$tsc_minThres1 * 2/ 12 *  temp_maxpenmy/12`
  - **Tax Unit:** `tu_individual_at`

### 38. Function: ArithOp
  **Formula:** `pxp00`
  **Output Variable:** `temp_basepenspec`
  **Tax Unit:** `tu_individual_at`

### 39. Function: ArithOp
  **Formula:** `(temp_basepenreg+temp_basepenspec)*$tsccthl_cs_rate`
  **Output Variable:** `tsccthl_s`
  **Tax Unit:** `tu_individual_at`

### 40. Function: Elig
  **Eligibility Check:**
  - **Condition:** `les=4 & ils_pen>0 & poacs=0`
  - **Tax Unit:** `tu_individual_at`

### 41. Function: ArithOp
  **Formula:** `ils_pen*$tsccthl_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 42. Function: DefConst
  **Constants Defined:**
  - `$tscerac_cs_rate`: 0.0047
  - `$tscerac_ee_rate`: 0.011
  - `$tscerhl_cs_rate`: 0.03535
  - `$tscerhl_fa_rate`: n/a
  - `$tscerhl_bc_rate`: n/a
  - `$tscerhl_pf_rate`: n/a
  - `$tscerhl_wc_rate`: n/a
  - `$tscerhl_min_rate`: 0.0386
  - `$tscerui_rate`: 0.0295
  - `$tscerho_rate`: 0.005
  - `$tscersf_rate`: 0.001
  - `$tscerfa_rate`: 0.037
  - `$tsccthl_cs_rate`: 0.03535
  - `$tsccthl_rate`: 0.0468
  - `$tscerpi_ee_rate`: 0.1255
  - `$tscerpi_eeRed_rate`: 0.06275
  - `$tscerui_appr_rate`: 0.0115
  - `$tscerhl_ee_rate`: 0.0378
  - `$tscerhl_appr_rate`: 0.0168
  - `$tscerrg_rate`: 0.03
  - `$tsceruimin`: 0.0289

### 43. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=0 & (((dag>=65 & dag<=67) & dgn=1) | ((dag>=61 & dag<=63) & dgn=0))`
  - **Tax Unit:** `tu_individual_at`

### 44. Function: ArithOp
  **Formula:** `(temp_basereg+temp_basespec)*$tscerpi_eeRed_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 45. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yem-yemxp)<$tsc_minThres1*yemmy/12 & dag>=15 & dag<=17`
  - **Tax Unit:** `tu_individual_at`

### 46. Function: ArithOp
  **Formula:** `yem*$tscerhl_appr_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 47. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=0 & dag>=15 & dag<=17`
  - **Tax Unit:** `tu_individual_at`

### 48. Function: ArithOp
  **Formula:** `(temp_basereg+temp_basespec)*$tscerui_appr_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 49. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=0 & dag>=18`
  - **Tax Unit:** `tu_individual_at`

### 50. Function: ArithOp
  **Formula:** `(temp_basereg+temp_basespec)*$tscerhl_ee_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 51. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=0 & dag>=15 & dag<=17`
  - **Tax Unit:** `tu_individual_at`

### 52. Function: ArithOp
  **Formula:** `(temp_basereg+temp_basespec)*$tscerhl_appr_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 53. Function: ArithOp
  **Formula:** `yem*$tscerrg_rate`
  **Output Variable:** `tscerrg_s`
  **Tax Unit:** `tu_individual_at`

### 54. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yem-yemxp)<$tsc_minThres1*yemmy/12 & dag>=18`
  - **Tax Unit:** `tu_individual_at`

### 55. Function: ArithOp
  **Formula:** `yem * $tscerac_ee_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 56. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yem-yemxp)<$tsc_minThres1*yemmy/12 & dag>=18`
  - **Tax Unit:** `tu_individual_at`

### 57. Function: ArithOp
  **Formula:** `yem * $tsceruimin`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 58. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yem-yemxp)<$tsc_minThres1*yemmy/12 & dag>=18`
  - **Tax Unit:** `tu_individual_at`

### 59. Function: ArithOp
  **Formula:** `yem * $tscersf_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`


---

## Policy: tscee_at
### 1. Function: DefVar
  - **temp_basepenlow**: `0`
  - **temp_basepenhigh**: `0`
  - **temp_contributions1**: `0`
  - **temp_contributions2**: `0`
  - **temp_tsceepi**: `0`
  - **temp_basespec**: `0`
  - **temp_basereg**: `0`
  - **temp_basereg2**: `0`
  - **elig_tsceepi_reduc_pens**: `0`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yem-yemxp)>=$tsc_minThres1 * yemmy / 12`
  - **Tax Unit:** `tu_individual_at`

### 3. Function: ArithOp
  **Formula:** `yem-yemxp`
  **Output Variable:** `temp_basereg`
  **Tax Unit:** `tu_individual_at`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yemxp>=$tsc_minThres1 * 2/ 12 * yemmy/12`
  - **Tax Unit:** `tu_individual_at`

### 5. Function: ArithOp
  **Formula:** `yemxp`
  **Output Variable:** `temp_basespec`
  **Tax Unit:** `tu_individual_at`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=1`
  - **Tax Unit:** `tu_individual_at`

### 7. Function: ArithOp
  **Formula:** `temp_basereg*$tsceehl_cs_rate`
  **Output Variable:** `tsceehl01_s`
  **Tax Unit:** `tu_individual_at`

### 8. Function: ArithOp
  **Formula:** `temp_basespec*$tsceehl_cs_rate`
  **Output Variable:** `tsceehl02_s`
  **Tax Unit:** `tu_individual_at`

### 9. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 10. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 11. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 12. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 13. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 14. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 15. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 16. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 17. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 18. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 19. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 20. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 21. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem>0`
  - **Tax Unit:** `tu_individual_at`

### 22. Function: ArithOp
  **Formula:** `yem`
  **Output Variable:** `temp_basepenlow`
  **Tax Unit:** `tu_individual_at`

### 23. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yem)>$tscse_maxThres2 * yemmy / 12`
  - **Tax Unit:** `tu_individual_at`

### 24. Function: ArithOp
  **Formula:** `(yem-$tscse_maxThres2 * yemmy/12)`
  **Output Variable:** `temp_basepenhigh`
  **Tax Unit:** `tu_individual_at`

### 25. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2007
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2008*

### 26. Function: DefVar
  - **temp_birthyear**: `0`

### 27. Function: ArithOp
  **Formula:** `$PolicyYear-dag`
  **Output Variable:** `temp_birthyear`
  **Tax Unit:** `tu_individual_at`

### 28. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=1 & yem>0`
  - **Tax Unit:** `tu_individual_at`

### 29. Function: BenCalc
  - **comp_cond**: `temp_birthyear<=1954`
  - **comp_perTU**: `0.1255`
  - **output_var**: `temp_contributions1`
  - **TAX_UNIT**: `tu_individual_at`

### 30. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=1 & yem>0`
  - **Tax Unit:** `tu_individual_at`

### 31. Function: BenCalc
  - **comp_cond**: `temp_birthyear<=1954`
  - **comp_perTU**: `0.1255`
  - **output_var**: `temp_contributions2`
  - **TAX_UNIT**: `tu_individual_at`

### 32. Function: ArithOp
  **Formula:** `temp_basepenlow*temp_contributions1+temp_basepenhigh*temp_contributions2`
  **Output Variable:** `temp_tsceepi`
  **Tax Unit:** `tu_individual_at`

### 33. Function: ArithOp
  **Formula:** `temp_tsceepi*12/14`
  **Output Variable:** `tsceepi01_s`
  **Tax Unit:** `tu_individual_at`

### 34. Function: ArithOp
  **Formula:** `temp_tsceepi*2/14`
  **Output Variable:** `tsceepi02_s`
  **Tax Unit:** `tu_individual_at`

### 35. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=0 & (((dag<65 | dag>67) & dgn=1) | ((dag<61 | dag>63) & dgn=0))`
  - **Tax Unit:** `tu_individual_at`

### 36. Function: ArithOp
  **Formula:** `temp_basereg*$tsceepi_ee_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 37. Function: ArithOp
  **Formula:** `temp_basespec*$tsceepi_ee_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 38. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=0 & ((dag<63 & dgn=1) | (dag<61 & dgn=0))  & dag>=18`
  - **Tax Unit:** `tu_individual_at`

### 39. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `temp_basereg2`
  - **comp_cond**: `$base>$tsc_maxThres1*yemmy/12`
  - **comp_perTU**: `$tsc_maxThres1*yemmy/12*$tsceeui_rate4`
  - **#_amount**: `$tsceeui_upThres3`
  - **output_var**: `tsceeui01_s`
  - **TAX_UNIT**: `tu_individual_at`

### 40. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yemxp`
  - **comp_cond**: `$base>$tsc_maxThres1*2/12*yemmy/12`
  - **comp_perTU**: `$tsc_maxThres1*2/12*yemmy/12*$tsceeui_rate4`
  - **#_amount**: `$tsceeui_upThres3`
  - **output_var**: `tsceeui02_s`
  - **TAX_UNIT**: `tu_individual_at`

### 41. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lsepf=0 & lcl!=3 & dag>=18`
  - **Tax Unit:** `tu_individual_at`

### 42. Function: ArithOp
  **Formula:** `temp_basereg*$tsceeho_rate`
  **Output Variable:** `tsceeho_s`
  **Tax Unit:** `tu_individual_at`

### 43. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=0 & lcl!=3 & dag>=18`
  - **Tax Unit:** `tu_individual_at`

### 44. Function: ArithOp
  **Formula:** `temp_basereg*$tsceeot_rate`
  **Output Variable:** `tsceeot_s`
  **Tax Unit:** `tu_individual_at`

### 45. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcl=3 & dag>=18`
  - **Tax Unit:** `tu_individual_at`

### 46. Function: ArithOp
  **Formula:** `temp_basereg*$tsceeot_fa_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 47. Function: ArithOp
  **Formula:** `tsceehl01_s + tsceehl02_s`
  **Output Variable:** `tsceehl_s`
  **Tax Unit:** `tu_individual_at`

### 48. Function: ArithOp
  **Formula:** `tsceepi01_s + tsceepi02_s`
  **Output Variable:** `tsceepi_s`
  **Tax Unit:** `tu_individual_at`

### 49. Function: ArithOp
  **Formula:** `tsceeui01_s + tsceeui02_s`
  **Output Variable:** `tsceeui_s`
  **Tax Unit:** `tu_individual_at`

### 50. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2009
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2010*

### 51. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2010
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2011*

### 52. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2012
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2013*

### 53. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2011
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2012*

### 54. Function: DefConst
  **Constants Defined:**
  - `$tsceehl_cs_rate`: 0.041
  - `$tsceehl_pf_rate`: n/a
  - `$tsceehl_fa_rate`: n/a
  - `$tsceehl_bc_rate`: n/a
  - `$tsceehl_wc_rate`: n/a
  - `$tsceepi_ee_rate`: 0.1025
  - `$tsceeui_rate1`: 0
  - `$tsceeui_rate2`: 0.01
  - `$tsceeui_rate3`: 0.02
  - `$tsceeui_rate4`: 0.0295
  - `$tsceeho_rate`: 0.005
  - `$tsceeot_rate`: 0.005
  - `$tsceeot_fa_rate`: 0.0075
  - `$tsceeui_upThres1`: 2074#m
  - `$tsceeui_upThres2`: 2262#m
  - `$tsceeui_upThres3`: 2451#m
  - `$tsceehl_appr_rate`: 0.0167
  - `$tsceepi_eeRed_rate`: 0.05125
  - `$tsceeui_appr_rate`: 0.0115
  - `$tsceehl_ee_rate`: 0.0387

### 55. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2025
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: *training_data

### 56. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2013
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2014*

### 57. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=0 & (((dag>=65 & dag<=67) & dgn=1) | ((dag>=61 & dag<=63) & dgn=0))
`
  - **Tax Unit:** `tu_individual_at`

### 58. Function: ArithOp
  **Formula:** `temp_basereg*$tsceepi_eeRed_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 59. Function: ArithOp
  **Formula:** `temp_basespec*$tsceepi_eeRed_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 60. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2014
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2015*

### 61. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=0 & (dag>=15 & dag<=17)`
  - **Tax Unit:** `tu_individual_at`

### 62. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `temp_basereg2`
  - **comp_cond**: `$base>$tsc_maxThres1*yemmy/12`
  - **comp_perTU**: `$tsc_maxThres1*yemmy/12*$tsceeui_rate4`
  - **#_amount**: `$tsceeui_upThres3`
  - **Output_Add_Var**: `tsceeui01_s`
  - **TAX_UNIT**: `tu_individual_at`

### 63. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yemxp`
  - **comp_cond**: `$base>$tsc_maxThres1*2/12*yemmy/12`
  - **comp_perTU**: `$tsc_maxThres1*2/12*yemmy/12*$tsceeui_rate4`
  - **#_amount**: `$tsceeui_upThres3`
  - **Output_Add_Var**: `tsceeui02_s`
  - **TAX_UNIT**: `tu_individual_at`

### 64. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2025
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2025_hhot

### 65. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=0 &  dag>=18`
  - **Tax Unit:** `tu_individual_at`

### 66. Function: ArithOp
  **Formula:** `temp_basereg*$tsceehl_ee_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 67. Function: ArithOp
  **Formula:** `temp_basespec*$tsceehl_ee_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 68. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lcs=0 & dag>=15 & dag<=17`
  - **Tax Unit:** `tu_individual_at`

### 69. Function: ArithOp
  **Formula:** `temp_basereg*$tsceehl_appr_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 70. Function: ArithOp
  **Formula:** `temp_basespec*$tsceehl_appr_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 71. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2015
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2016*

### 72. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2016
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2017*

### 73. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2017
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2018*

### 74. Function: ArithOp
  **Formula:** `yem-yemxp`
  **Output Variable:** `temp_basereg2`
  **Tax Unit:** `tu_individual_at`

### 75. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2018
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2019*

### 76. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2019
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2020*

### 77. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2020
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2021*

### 78. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2021
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2022*

### 79. Function: Elig
  **Eligibility Check:**
  - **Condition:** `poa00 > 0 & (yem-yemxp)>=$tsc_minThres1 * yemmy / 12`
  - **Tax Unit:** `tu_individual_at`

### 80. Function: ArithOp
  **Formula:** `-1 * (temp_basereg*$tsceepi_ee_rate)`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 81. Function: Elig *(Switch: off)*
  **Eligibility Check:**
  - **Condition:** `(yempv)>=$tsc_minThres1 * yemmy / 12`
  - **Tax Unit:** `tu_individual_at`

### 82. Function: ArithOp *(Switch: off)*
  **Formula:** `yempv`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 83. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2022
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2023*

### 84. Function: DefConst
  **Constants Defined:**
  - `$PolicyYear`: 2023
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: AT_2024*


---

## Policy: tscse_at
### 1. Function: DefConst
  **Constants Defined:**
  - `$tscseac_fa_rate`: 0.019
  - `$tscseac_se_rate`: 12.07#m
  - `$tscsehl_se_rate`: 0.068
  - `$tscsepi_fa_rate`: 0.170
  - `$tscsepi_pf_rate`: 0.2
  - `$tscsepi_se_rate`: 0.185
  - `$tscseot_rate`: 0.0153
  - `$tscsehl_fa_rate`: 0.068
  - `$tscsepi_pf_redRate`: 0.1
  - `$tscsepi_se_redRate`: 0.0925
  - `$tscsepi_fa_redRate`: 0.085

### 2. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(les!=1 & lpf=0 & yse>0 & lse!=5)`
  - **Tax Unit:** `tu_individual_at`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(les!=1 & yem>0 & lpf=0 & yse>0 & lse!=5) & (((dag<65 | dag>67) & dgn=1) | ((dag<61 | dag>63) & dgn=0))`
  - **Tax Unit:** `tu_individual_at`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `les!=1 & lpf=1 & yse>0 & (((dag<65 | dag>67) & dgn=1) | ((dag<61 | dag>63) & dgn=0))`
  - **Tax Unit:** `tu_individual_at`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(les!=1 & yem=0 & lpf=0 & yse>0 & lse!=5) & (((dag<65 | dag>67) & dgn=1) | ((dag<61 | dag>63) & dgn=0))`
  - **Tax Unit:** `tu_individual_at`

### 7. Function: Elig
  **Eligibility Check:**
  - **Condition:** `les=1 & yse>0 & (((dag<65 | dag>67) & dgn=1) | ((dag<61 | dag>63) & dgn=0))`
  - **Tax Unit:** `tu_individual_at`

### 8. Function: ArithOp
  **Formula:** `tscsehl00_s + tscsehlpf_s`
  **Output Variable:** `tscsehl_s`
  **Tax Unit:** `tu_individual_at`

### 9. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(les!=1 & yem>0 & lpf=0 & yse>0 & lse!=5)`
  - **Tax Unit:** `tu_individual_at`

### 10. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(les!=1 & yem=0 & lpf=0 & yse>0 & lse!=5)`
  - **Tax Unit:** `tu_individual_at`

### 11. Function: Elig
  **Eligibility Check:**
  - **Condition:** `les=1 & yse>0`
  - **Tax Unit:** `tu_individual_at`

### 12. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base >($tscse_maxThres2*ysemy/12)`
  - **Comp_perTU**: `$tscseac_fa_rate*$tscse_minThres2*ysemy/12`
  - **Output_Add_Var**: `tscseac_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base<=($tscse_minThres2*ysemy/12)`

### 13. Function: Elig
  **Eligibility Check:**
  - **Condition:** `les=1 & yse>0`
  - **Tax Unit:** `tu_individual_at`

### 14. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **Output_Var**: `tscseac_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_perTU**: `$tscseac_se_rate*ysemy/12`
  - **Comp_Cond**: `$base > 0`

### 15. Function: Elig
  **Eligibility Check:**
  - **Condition:** `les!=1 & yse>0`
  - **Tax Unit:** `tu_individual_at`

### 16. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base >($tscse_maxThres2*ysemy/12) & temp_yse>($tscse_maxThres2*ysemy/12)`
  - **Comp_perTU**: `$tscsehl_fa_rate*temp_yse`
  - **Output_Var**: `tscsehl00_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base<=($tsc_minThres1*ysemy/12) & temp_yse>0 & tsceehl_s!=0`

### 17. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base >($tscse_maxThres2*ysemy/12)`
  - **Comp_perTU**: `$tscsehl_se_rate*$tsc_minThres1*ysemy/12`
  - **Output_Add_Var**: `tscsehl00_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base<=($tsc_minThres1*ysemy/12)`

### 18. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base >($tscse_maxThres2*ysemy/12)`
  - **Comp_perTU**: `$tscsehl_se_rate*$tsc_minThres1*ysemy/12`
  - **Output_Var**: `tscsehlpf_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base<=($tsc_minThres1*ysemy/12)`

### 19. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(les!=1 & lpf=1 & yse>0)`
  - **Tax Unit:** `tu_individual_at`

### 20. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base >($tscse_maxThres2*ysemy/12) & temp_yse>($tscse_maxThres2*ysemy/12)`
  - **Comp_perTU**: `$tscsehl_se_rate*temp_yse`
  - **Output_Add_Var**: `tscsehl00_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base<=($tsc_minThres1*ysemy/12) & temp_yse>0 & tsceehl_s!=0`

### 21. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base >($tscse_maxThres2*ysemy/12)`
  - **Comp_perTU**: `$tscsepi_se_rate*$tscse_minThres3*ysemy/12`
  - **Output_Add_Var**: `tscsepi_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base<=($tscse_minThres3*ysemy/12)`

### 22. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base >($tscse_maxThres2*ysemy/12)`
  - **Comp_perTU**: `$tscsepi_pf_rate*$tscse_minThres3*ysemy/12`
  - **Output_Add_Var**: `tscsepi_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base<=($tscse_minThres3*ysemy/12)`

### 23. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base<=($tsc_minThres1*ysemy/12) & temp_yse>0 & tsceepi_s!=0`
  - **Comp_perTU**: `$tscsepi_fa_rate*$tscse_maxThres2*ysemy/12`
  - **Output_Var**: `tscsepi_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base >($tscse_maxThres2*ysemy/12) & temp_yse>($tscse_maxThres2*ysemy/12)`

### 24. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base<=($tsc_minThres1*ysemy/12) & temp_yse>0 & tsceepi_s!=0`
  - **Comp_perTU**: `$tscsepi_se_rate*$tscse_maxThres2*ysemy/12`
  - **Output_Add_Var**: `tscsepi_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base >($tscse_maxThres2*ysemy/12) & temp_yse>($tscse_maxThres2*ysemy/12)`

### 25. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base >($tscse_maxThres2*ysemy/12)`
  - **Comp_perTU**: `$tscseot_rate*$tsc_minThres1*ysemy/12`
  - **Output_Var**: `tscseot_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base<=($tsc_minThres1*ysemy/12)`

### 26. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **base**: `n/a`
  - **comp_cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 27. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base >($tscse_maxThres2*ysemy/12) & temp_yse<($tscse_maxThres2*ysemy/12)`
  - **Comp_perTU**: `$tscsehl_se_rate*$tscse_maxThres2*ysemy/12`
  - **Output_Add_Var**: `tscsehl00_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base >($tscse_maxThres2*ysemy/12) & temp_yse>($tscse_maxThres2*ysemy/12)`

### 28. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(les!=1 & lpf=0 & yse>0 & lse=5)`
  - **Tax Unit:** `tu_individual_at`

### 29. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base >($tsc_minThres1*ysemy/12) & temp_yse<=($tscse_maxThres2*ysemy/12)`
  - **Comp_perTU**: `$tscsepi_se_rate*$tscse_maxThres2*ysemy/12`
  - **Output_Add_Var**: `tscsepi_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base >($tscse_maxThres2*ysemy/12) & temp_yse>($tscse_maxThres2*ysemy/12)`

### 30. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(les!=1 & lpf=0 & yse>0 & lse=5) & (((dag<65 | dag>67) & dgn=1) | ((dag<61 | dag>63) & dgn=0))`
  - **Tax Unit:** `tu_individual_at`

### 31. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base >($tscse_maxThres2*ysemy/12)`
  - **Comp_perTU**: `n/a`
  - **Output_Add_Var**: `tscseot_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `n/a`

### 32. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(les!=1 & lpf=0 & yse>0 & lse=5)`
  - **Tax Unit:** `tu_individual_at`

### 33. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem>= $tsc_minThres1 * 14/12 * yemmy/12`
  - **Tax Unit:** `tu_individual_at`

### 34. Function: ArithOp
  **Formula:** `yem`
  **Output Variable:** `temp_baseyem`
  **Tax Unit:** `tu_individual_at`

### 35. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yse>0 & yem>0`
  - **Tax Unit:** `tu_individual_at`

### 36. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yse>0`
  - **Tax Unit:** `tu_individual_at`

### 37. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `yem=0`
  - **Comp_perTU**: `0`
  - **Output_Var**: `temp_yse`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `temp_diff<=0 & yem>0`

### 38. Function: ArithOp
  **Formula:** `$tscse_maxThres2 - temp_baseyem`
  **Output Variable:** `temp_diff`
  **Tax Unit:** `tu_individual_at`

### 39. Function: DefVar
  - **temp_diff**: `0`
  - **temp_yse**: `0`
  - **temp_baseyem**: `0`
  - **temp_tscsehl00_bonus_s**: `0`

### 40. Function: Elig
  **Eligibility Check:**
  - **Condition:** `les=1 & yse>0 & (((dag>=65 & dag<=67) & dgn=1) | ((dag>=61 & dag<=63) & dgn=0))`
  - **Tax Unit:** `tu_individual_at`

### 41. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base<=($tsc_minThres1*ysemy/12) & temp_yse>0 & tsceepi_s!=0`
  - **Comp_perTU**: `$tscse_maxThres2*ysemy/12*$tscsepi_fa_redRate`
  - **Output_Add_Var**: `tscsepi_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base >($tscse_maxThres2*ysemy/12) & temp_yse>($tscse_maxThres2*ysemy/12)`

### 42. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(les!=1 & yem=0 & lpf=0 & yse>0 & lse!=5) & (((dag>=65 & dag<=67) & dgn=1) | ((dag>=61 & dag<=63) & dgn=0))`
  - **Tax Unit:** `tu_individual_at`

### 43. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base >($tscse_maxThres2*ysemy/12)`
  - **Comp_perTU**: `$tscse_minThres3*ysemy/12*$tscsepi_se_redRate`
  - **Output_Add_Var**: `tscsepi_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base<=($tscse_minThres3*ysemy/12)`

### 44. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(les!=1 & yem>0 & lpf=0 & yse>0 & lse!=5) & (((dag>=65 & dag<=67) & dgn=1) | ((dag>=61 & dag<=63) & dgn=0))`
  - **Tax Unit:** `tu_individual_at`

### 45. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base<=($tsc_minThres1*ysemy/12) & temp_yse>0 & tsceepi_s!=0`
  - **Comp_perTU**: `$tscse_maxThres2*ysemy/12*$tscsepi_se_redRate`
  - **Output_Add_Var**: `tscsepi_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base >($tscse_maxThres2*ysemy/12) & temp_yse>($tscse_maxThres2*ysemy/12)`

### 46. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(les!=1 & lpf=0 & yse>0 & lse=5) & (((dag>=65 & dag<=67) & dgn=1) | ((dag>=61 & dag<=63) & dgn=0))`
  - **Tax Unit:** `tu_individual_at`

### 47. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base >($tsc_minThres1*ysemy/12) & temp_yse<=($tscse_maxThres2*ysemy/12)`
  - **Comp_perTU**: `$tscse_maxThres2*ysemy/12*$tscsepi_se_redRate`
  - **Output_Add_Var**: `tscsepi_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base >($tscse_maxThres2*ysemy/12) & temp_yse>($tscse_maxThres2*ysemy/12)`

### 48. Function: Elig
  **Eligibility Check:**
  - **Condition:** `les!=1 & lpf=1 & yse>0 & (((dag>=65 & dag<=67) & dgn=1) | ((dag>=61 & dag<=63) & dgn=0))`
  - **Tax Unit:** `tu_individual_at`

### 49. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `yse`
  - **comp_cond**: `$base >($tscse_maxThres2*ysemy/12)`
  - **Comp_perTU**: `$tscse_minThres3*ysemy/12*$tscsepi_pf_redRate`
  - **Output_Add_Var**: `tscsepi_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `$base<=($tscse_minThres3*ysemy/12)`

### 50. Function: BenCalc
  - **Elig_Var**: `tscsehl00_s`
  - **Who_Must_Be_Elig**: `all`
  - **Base**: `tscsehl00_s / $tscsehl_se_rate`
  - **Comp_Cond**: `$base > 2400#m & $base <= 2900#m`
  - **Comp_perTU**: `60#y`
  - **Output_Var**: `temp_tscsehl00_bonus_s`
  - **TAX_UNIT**: `tu_individual_at`

### 51. Function: ArithOp
  **Formula:** `tscsehl00_s - temp_tscsehl00_bonus_s`
  **Output Variable:** `tscsehl00_s`
  **Tax Unit:** `tu_individual_at`


---

## Policy: bch00_at
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem>0`
  - **Tax Unit:** `tu_individual_at`

### 2. Function: ArithOp
  **Formula:** `132#y`
  **Output Variable:** `temp_costearn`
  **Tax Unit:** `tu_individual_at`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem>0 | yse>0 | ils_pen>0`
  - **Tax Unit:** `tu_individual_at`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag<18 | ((dag=18 | dag=19) & (dec>0 | IsDisabled)) | (dag>=20 & (dec>0 | IsDisabled) & il_child<$bch00_ilchild_thresh_yr)
`
  - **Tax Unit:** `tu_individual_at`

### 6. Function: DefVar
  - **temp_base**: `0`
  - **temp_supplement**: `0`
  - **temp_school**: `0`
  - **temp_above20educ**: `0`
  - **temp_costearn**: `n/a`
  - **temp_exdeduct**: `n/a`
  - **temp_eligchild19**: `0`
  - **temp_childbasicamount**: `0`
  - **temp_nochildrenbasicamount**: `0`
  - **temp_childbasicamount1**: `0`
  - **temp_childbasicamount2**: `0`
  - **temp_nochildrenbasicamount1**: `0`
  - **temp_nochildrenbasicamount2**: `0`
  - **temp_eligdisab**: `0`

### 7. Function: BenCalc
  - **comp_cond**: `dag>=$bch00_child_age4 & dag<$bch00_child_age5 & temp_eligchild19=1`
  - **comp_perElig**: `$bch00_basic_amt4`
  - **output_var**: `temp_base`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `temp_eligdisab=1 |  bchditu=2`
  - **Comp_perElig**: `$bch00_basic_amt4`

### 8. Function: Elig
  **Eligibility Check:**
  - **Condition:** `temp_base>0`
  - **Tax Unit:** `tu_individual_at`

### 9. Function: ArithOp
  **Formula:** `temp_childbasicamount`
  **Output Variable:** `temp_nochildrenbasicamount`
  **Tax Unit:** `tu_bch01_at`

### 10. Function: BenCalc
  - **comp_cond**: `temp_nochildrenbasicamount>=4`
  - **comp_perElig**: `$bch00_disab_amt`
  - **comp_perTU**: `$bch00_suppl_amt3 + $bch00_suppl_amt4*(temp_nochildrenbasicamount-3)`
  - **#_level**: `tu_bch01_at`
  - **output_var**: `temp_supplement`
  - **TAX_UNIT**: `tu_individual_at`

### 11. Function: ArithOp
  **Formula:** `temp_base+temp_supplement+temp_school`
  **Output Variable:** `bch00_s`
  **Tax Unit:** `tu_bch01_at`

### 12. Function: DefConst
  **Constants Defined:**
  - `$bch00_child_age1`: 0
  - `$bch00_child_age2`: 3
  - `$bch00_child_age3`: 10
  - `$bch00_child_age4`: 19
  - `$bch00_child_age5`: 24
  - `$bch00_basic_amt1`: 138.4#m
  - `$bch00_basic_amt2`: 148#m
  - `$bch00_basic_amt3`: 171.8#m
  - `$bch00_basic_amt4`: 200.4#m
  - `$bch00_suppl_amt2`: 17.2#m
  - `$bch00_suppl_amt3`: 63.3#m
  - `$bch00_suppl_amt4`: 65.3#m
  - `$bch00_disab_amt`: 189.2#m
  - `$bch00_multi_addAmt`: 24.4#m
  - `$bch00_school_amt`: 121.4#y
  - `$bch00_school_age`: 6
  - `$bch00_school_upAge`: 16
  - `$bch00_covid_amt`: n/a
  - `$bch00_ilchild_thresh_yr`: 17212#y
  - `$bch00_ilchild_thresh_nu`: 17212

### 13. Function: BenCalc
  - **Comp_perTU**: `bchasxc*($bch00_basic_amt1+$bch00_basic_amt2 + $bch00_basic_amt3 + $bch00_basic_amt4)/4`
  - **Comp_Cond**: `bchasxc>0`
  - **Output_Add_Var**: `temp_base`
  - **TAX_UNIT**: `tu_individual_at`
  - **Run_Cond**: `IsUsedDatabase#1  | IsUsedDatabase#2  | IsUsedDatabase#3`
  - **#_DataBasename**: `AT_2010_??_????_??_??`

### 14. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag>=20 & (dec>0 | IsDisabled) & il_child>=$bch00_ilchild_thresh_yr`
  - **Tax Unit:** `tu_individual_at`

### 15. Function: BenCalc
  - **comp_cond**: `dag>=$bch00_child_age4 & dag<$bch00_child_age5 & temp_above20educ=1`
  - **comp_perElig**: `(($bch00_ilchild_thresh_nu+$bch00_basic_amt4*12)/12)-il_child`
  - **Output_Add_Var**: `temp_base`
  - **TAX_UNIT**: `tu_individual_at`
  - **LowLim**: `0`

### 16. Function: BenCalc
  - **comp_cond**: `dag>=$bch00_school_age & dag<$bch00_school_upAge`
  - **comp_perElig**: `$bch00_school_amt`
  - **output_var**: `temp_school`
  - **TAX_UNIT**: `tu_bch01_at`

### 17. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag>=$bch00_child_age5 & IsDisabled & (idmother!=0 | idfather!=0) & il_child<$bch00_ilchild_thresh_yr & ils_pen=0 & dms!=1`
  - **Tax Unit:** `tu_individual_at`
  **Run Condition:** `IsUsedDatabase#1  | IsUsedDatabase#2  | IsUsedDatabase#3`

### 18. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 19. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`


---

## Policy: pch00_at *(Switch: off)*
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `nDepChildrenInTu#1>0 & ils_pen>0 & poacs=0`
  - **Tax Unit:** `tu_individual_at`

### 2. Function: ArithOp
  **Formula:** `$pch_child_amt*14/12*nDepChildrenInTu`
  **Output Variable:** `pch00_s`
  **Tax Unit:** `tu_pch_at`

### 3. Function: Allocate
  - **share**: `pch00_s`
  - **share_between**: `ils_pen#1>0`
  - **#_level**: `tu_individual_at`
  - **output_var**: `pch00_s`
  - **TAX_UNIT**: `tu_pch_at`

### 4. Function: DefConst
  **Constants Defined:**
  - `$pch_child_amt`: 29.07#m


---

## Policy: pchcs_at *(Switch: off)*
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsDepChild & ((ils_origy#1<=$tsc_minThres1*14/12 & dag>18) | dag<=18) & bch00_s>0 & ils_pen>0 & poacs>0`
  - **Tax Unit:** `tu_pch_at`

### 2. Function: ArithOp
  **Formula:** `$pch_csChild_amt*14/12*nDepChildrenInTu`
  **Output Variable:** `pchcs_s`
  **Tax Unit:** `tu_pch_at`

### 3. Function: Allocate
  - **share**: `pchcs_s`
  - **share_between**: `ils_pen#1>0 & poacs#1>0`
  - **#_level**: `tu_individual_at`
  - **output_var**: `pchcs_s`
  - **TAX_UNIT**: `tu_pch_at`

### 4. Function: DefConst
  **Constants Defined:**
  - `$pch_csChild_amt`: 15.6#m


---

## Policy: bunct_at
### 1. Function: ArithOp
  **Formula:** `max(lunmy,bunctmy)`
  **Output Variable:** `lunmy_s`
  **Tax Unit:** `tu_individual_at`

### 2. Function: BenCalc
  - **comp_cond**: `dag<=24`
  - **comp_perTU**: `min((liwmy*$UB_QperTot3/12), liwwh)`
  - **output_var**: `liwmy_s`
  - **TAX_UNIT**: `tu_individual_at`

### 3. Function: BenCalc
  - **comp_cond**: `lunmy_s > 0 & bunct = 0`
  - **comp_perElig**: `0`
  - **output_var**: `liwmy_s`
  - **TAX_UNIT**: `tu_individual_at`

### 4. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `ils_earns = 0 | bunct > 0`
  - **comp_perElig**: `lunmy_s`
  - **output_var**: `lunmy_s`
  - **TAX_UNIT**: `tu_individual_at`

### 5. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `dgn=0`
  - **comp_perElig**: `$PensionAgeFemale - dag`
  - **output_var**: `temp_eligret`
  - **TAX_UNIT**: `tu_individual_at`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lunmy_s > 0 & (liwmy_s >= $UB_QperMin1 | liwmy_s >= $UB_QperMin3) & dag >= 16 & poa00 = 0 & poacs=0 & (yem > 0 | (lse= 0 | yse=0))`
  - **Tax Unit:** `tu_individual_at`

### 7. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(liwwh>=107 & dag>=50)  & bunctmy=0`
  - **comp_perTU**: `12`
  - **output_var**: `bunctmy_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `bunctmy>0`
  - **Comp_perTU**: `bunctmy`

### 8. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `lunmy_s > 0 & bunct = 0`
  - **comp_perElig**: `0`
  - **output_var**: `yempv_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_perElig**: `yempv`
  - **Comp_Cond**: `bunctmy_s>0`

### 9. Function: ArithOp
  **Formula:** `0.55 * yempv_s`
  **Output Variable:** `temp_bunct`
  **Tax Unit:** `tu_individual_at`

### 10. Function: DefVar
  - **temp_bunct**: `0`
  - **temp_eligbch00earn**: `0`
  - **temp_eligbunct0**: `0`
  - **temp_eligret**: `0`
  - **i_bunct**: `0`

### 11. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bunct=0`
  - **Tax Unit:** `tu_individual_at`

### 12. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `temp_bunct<amount#1  & bunct=0`
  - **comp_perTU**: `(min(amount#1,(0.6*yempv_s)))*temp_eligbunct0`
  - **#_amount**: `$bun_minAmt`
  - **output_var**: `temp_bunct`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `temp_bunct<amount#1`
  - **Comp_perTU**: `min(amount#1,(0.6*yempv_s))`

### 13. Function: BenCalc
  - **comp_cond**: `nDepChildrenInTu#1>0 & temp_bunct>0`
  - **comp_perTU**: `(0.97#d*nDepChildrenInTU#1)*bunctmy_s / 12`
  - **#_level**: `tu_bch00_at`
  - **output_var**: `bunmt_s`
  - **TAX_UNIT**: `tu_individual_at`

### 14. Function: Elig
  **Eligibility Check:**
  - **Condition:** `nDepChildrenInTu#2>0 & temp_bunct>0 & GetPartnerIncome#1<=$tsc_minThres1*14/12`
  - **Tax Unit:** `tu_individual_at`

### 15. Function: BenCalc
  - **comp_cond**: `temp_eligbch00earn>0`
  - **comp_perTU**: `0.97#d*bunctmy_s / 12`
  - **output_add_var**: `bunmt_s`
  - **TAX_UNIT**: `tu_individual_at`

### 16. Function: Elig
  **Eligibility Check:**
  - **Condition:** `temp_bunct>0`
  - **Tax Unit:** `tu_individual_at`

### 17. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `temp_bunct<$bun_minAmt  & bunct=0 & bunmt_s>0`
  - **comp_perTU**: `(min($bun_minAmt,(0.8*yempv_s)))*temp_eligbunct0`
  - **output_var**: `temp_bunct`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `temp_bunct<$bun_minAmt & bunmt_s>0`
  - **Comp_perTU**: `min($bun_minAmt,(0.8*yempv_s))`

### 18. Function: ArithOp
  **Formula:** `temp_bunct * bunctmy_s  / 12`
  **Output Variable:** `bunct_s`
  **Tax Unit:** `tu_individual_at`

### 19. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 20. Function: BenCalc
  - **comp_cond**: `dag<=24 & liwwh12_h>=6`
  - **comp_perElig**: `1`
  - **output_var**: `liwmy_s`
  - **TAX_UNIT**: `tu_individual_at`

### 21. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lunmy_s>0 & yem<=$tsc_minThres1*14/12 & (liwmy_s!=0 & dag>=16 & poa00=0 & poacs=0 & (yem>0 | (lse=0 | yse=0)) )`
  - **Tax Unit:** `tu_individual_at`

### 22. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `liwwhny15_h>=108 & dag>=50`
  - **comp_perTU**: `3`
  - **Comp_Cond**: `liwwh>=36`
  - **Comp_perTU**: `7`
  - **UpLim**: `lunmy`
  - **output_var**: `bunctmy_s`
  - **TAX_UNIT**: `tu_individual_at`

### 23. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 24. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 25. Function: Elig *(Switch: off)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 26. Function: ArithOp *(Switch: off)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 27. Function: Elig *(Switch: off)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 28. Function: ArithOp *(Switch: off)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 29. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `bunctmy=0`
  - **Comp_perTU**: `min(lunmy_s, bunctmy_s)`
  - **Output_Var**: `bunctmy_s`
  - **TAX_UNIT**: `tu_individual_at`

### 30. Function: ArithOp *(Switch: off)*
  **Formula:** `0.55 * (yempv_s - i_tin - ils_sicee)`
  **Output Variable:** `temp_bunct`
  **Tax Unit:** `tu_individual_at`

### 31. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `lunmy_s>bunctmy_s`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_at`

### 32. Function: ArithOp *(Switch: off)*
  **Formula:** `temp_bunct * bunctmy_s  / 12`
  **Output Variable:** `i_bunct`
  **Tax Unit:** `tu_individual_at`


---

## Policy: pmmtu_at
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `ils_pen>0 & poacs=0 & bunct_s=0 & bunnc_s=0`
  - **Tax Unit:** `tu_individual_at`

### 2. Function: DefVar
  - **temp_il_mtpmmtu**: `0`
  - **temp_child**: `0`

### 3. Function: BenCalc
  - **comp_cond**: `dag>=18`
  - **comp_perTU**: `il_mtpmmtu`
  - **#_uplim**: `278.13#m`
  - **output_var**: `temp_il_mtpmmtu`
  - **TAX_UNIT**: `tu_individual_at`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsDepChild & (dag<=18 | (dag>18 & dag<27 & (ils_earns-ils_sicdy-ils_tax)#1<=amount#1 & (IsInEducation | IsDisabled))) & pch00_s#1>0`
  - **Tax Unit:** `tu_individual_at`

### 5. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `psu>0  & temp_il_mtpmmtu#4<amount#3 & dag<24 & (idmother=0 & idfather=0)`
  - **comp_perTU**: `(amount#3-temp_il_mtpmmtu#4)*14/12`
  - **#_amount**: `196.57#m`
  - **#_lowlim**: `0`
  - **#_Info**: `dms`
  - **output_var**: `pmmtu_s`
  - **TAX_UNIT**: `tu_individual_at`

### 6. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsWithPartner & poa00>0 & temp_il_mtpmmtu#2<amount#1`
  - **comp_perTU**: `(amount#1 + amount#3*temp_child -temp_il_mtpmmtu#2)*14/12`
  - **#_amount**: `196.57#m`
  - **#_lowlim**: `0`
  - **output_add_var**: `pmmtu_s`
  - **TAX_UNIT**: `tu_partners_at`


---

## Policy: pcstu_at
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `ils_pen>0 & poacs>0 & pmmtu_s#1=0 & bunct_s=0 & bunnc_s=0`
  - **Tax Unit:** `tu_individual_at`

### 2. Function: DefVar
  - **temp_childcs**: `0`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsDepChild & (dag<=18 | (dag>18 & dag<27 & ils_earns<=$tsc_minThres1 & (IsInEducation | IsDisabled))) & pchcs_s#1>0`
  - **Tax Unit:** `tu_individual_at`

### 4. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `!IsWithPartner & poacs>0 & il_mtpmmtu#2<amount#1`
  - **comp_perTU**: `(amount#1 +amount#3*temp_childcs -il_mtpmmtu#2)*14/12`
  - **#_amount**: `196.57#m`
  - **#_lowlim**: `0`
  - **output_var**: `pcstu_s`
  - **TAX_UNIT**: `tu_individual_at`

### 5. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsWithPartner & poacs>0 & il_mtpmmtu#2<amount#1`
  - **comp_perTU**: `(amount#1 +amount#3*temp_childcs -il_mtpmmtu#2)*14/12`
  - **#_amount**: `196.57#m`
  - **#_lowlim**: `0`
  - **output_add_var**: `pcstu_s`
  - **TAX_UNIT**: `tu_partners_at`


---

## Policy: tscpe_at
### 1. Function: DefConst
  **Constants Defined:**
  - `$tscpehl_cs_rate`: 0.06
  - `$tscpehl_rate`: 0.06
  - `$tscpepi_cs_rate`: 0.0219

### 2. Function: DefVar
  - **temp_basereg**: `0`
  - **temp_basespec**: `0`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(poacs-poacs*2/14)>=$tsc_minThres1 * poamy / 12`
  - **Tax Unit:** `tu_individual_at`

### 4. Function: ArithOp
  **Formula:** `poacs-(poacs*2/14)`
  **Output Variable:** `temp_basereg`
  **Tax Unit:** `tu_individual_at`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(poacs*2/14)>=$tsc_minThres1 * 2/12 * poamy / 12`
  - **Tax Unit:** `tu_individual_at`

### 6. Function: ArithOp
  **Formula:** `(poacs*2/14)`
  **Output Variable:** `temp_basespec`
  **Tax Unit:** `tu_individual_at`

### 7. Function: Elig
  **Eligibility Check:**
  - **Condition:** `poacs>0`
  - **Tax Unit:** `tu_individual_at`

### 8. Function: ArithOp
  **Formula:** `temp_basereg*$tscpehl_cs_rate`
  **Output Variable:** `tscpehl01_s`
  **Tax Unit:** `tu_individual_at`

### 9. Function: ArithOp
  **Formula:** `temp_basespec*$tscpehl_cs_rate`
  **Output Variable:** `tscpehl02_s`
  **Tax Unit:** `tu_individual_at`

### 10. Function: Elig
  **Eligibility Check:**
  - **Condition:** `poa00>0`
  - **Tax Unit:** `tu_individual_at`

### 11. Function: ArithOp
  **Formula:** `(poa00-(poa00*2/14))*$tscpehl_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 12. Function: ArithOp
  **Formula:** `(poa00*2/14)*$tscpehl_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 13. Function: Elig
  **Eligibility Check:**
  - **Condition:** `psu>0`
  - **Tax Unit:** `tu_individual_at`

### 14. Function: ArithOp
  **Formula:** `(psu-(psu*2/14))*$tscpehl_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 15. Function: ArithOp
  **Formula:** `(psu*2/14)*$tscpehl_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 16. Function: Elig
  **Eligibility Check:**
  - **Condition:** `poaot>0`
  - **Tax Unit:** `tu_individual_at`

### 17. Function: ArithOp
  **Formula:** `(poaot-(poaot*2/14))*$tscpehl_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 18. Function: ArithOp
  **Formula:** `(poaot*2/14)*$tscpehl_rate`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 19. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(les=4 & poacs>0)`
  - **Tax Unit:** `tu_individual_at`

### 20. Function: ArithOp
  **Formula:** `(poacs*12/14)*$tscpepi_cs_rate`
  **Output Variable:** `tscpepi01_s`
  **Tax Unit:** `tu_individual_at`

### 21. Function: ArithOp
  **Formula:** `(poacs*2/14)*$tscpepi_cs_rate`
  **Output Variable:** `tscpepi02_s`
  **Tax Unit:** `tu_individual_at`

### 22. Function: ArithOp
  **Formula:** `tscpehl01_s + tscpehl02_s`
  **Output Variable:** `tscpehl_s`
  **Tax Unit:** `tu_individual_at`

### 23. Function: ArithOp
  **Formula:** `tscpepi01_s + tscpepi02_s`
  **Output Variable:** `tscpepi_s`
  **Tax Unit:** `tu_individual_at`


---

## Policy: bch00_at

---

## Policy: tin_at
### 1. Function: DefConst
  **Constants Defined:**
  - `$tin_lowthres0`: 0#y
  - `$tin_basic_rate1`: 0
  - `$tin_upthres1`: 13308#y
  - `$tin_basic_rate2`: 0.20
  - `$tin_upthres2`: 21617#y
  - `$tin_basic_rate3`: 0.3
  - `$tin_upthres3`: 35836#y
  - `$tin_basic_rate4`: 0.4
  - `$tin_eeNeg_amt`: 487#y
  - `$tin_eeNeg_rate`: 0.55
  - `$tin_specialExempt_thres`: 2570#y
  - `$tin_special_rate1`: 0
  - `$tin_specialExempt_amt1`: 620#y
  - `$tin_special_rate2`: 0.06
  - `$tin_specialExempt_amt2`: 25000#y
  - `$tin_special_rate3`: 0.27
  - `$tin_specialExempt_amt3`: 50000#y
  - `$tin_special_rate4`: 0.3575
  - `$tin_specialExempt_amt4`: 83333#y
  - `$tin_special_rate5`: 0.5
  - `$tin_upthres4`: 69166#y
  - `$tin_basic_rate5`: 0.48
  - `$tin_upthres5`: 103072#y
  - `$tin_basic_rate6`: 0.5
  - `$tin_upthres6`: 1000000#y
  - `$tin_basic_rate7`: 0.55
  - `$tin_severance_rate`: 0.06
  - `$tin_special_rate6`: 0.55
  - `$tin_specialExempt_amt5`: 166667 #y
  - `$tin_penNeg_rate`: 0.80
  - `$tin_penNeg_amt`: 710#y
  - `$tin_eeNeg_addAmt`: 790#y

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bch00_s>0`
  - **Tax Unit:** `tu_bch00_at`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem>0`
  - **Tax Unit:** `tu_individual_at`

### 4. Function: ArithOp
  **Formula:** `$tintace_amt`
  **Output Variable:** `tintace_s`
  **Tax Unit:** `tu_individual_at`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem>0 | yse>0 | ils_pen>0`
  - **Tax Unit:** `tu_individual_at`

### 6. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 7. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `yse>$tintatb_amt`
  - **comp_perTU**: `$tintatb_amt - (yse - $tintatb_amt)`
  - **lowlim**: `0`
  - **output_var**: `tintatb_s`
  - **TAX_UNIT**: `tu_individual_at`

### 8. Function: BenCalc
  - **comp_cond**: `yse>0`
  - **comp_perTU**: `$tintase_rate*(yse-ils_sicse)`
  - **comp_uplim**: `$tintase_rate*$tintase_uplim`
  - **lowlim**: `0`
  - **output_var**: `tintase_s`
  - **TAX_UNIT**: `tu_individual_at`

### 9. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 10. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_income**: `n/a`
  - **#_level**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 11. Function: DefVar
  - **temp_tin1**: `0`
  - **temp_tin2**: `0`
  - **temp_tin3**: `0`
  - **temp_buncm**: `0`
  - **temp_threshold**: `0`
  - **temp_tin4**: `0`
  - **temp_tin5**: `0`
  - **temp_tinfa**: `0`
  - **tintachng_s**: `0`
  - **childreninTU**: `0`
  - **temp_tinfa_partner**: `0`
  - **temp_tintcfa00**: `0`
  - **temp_tin1fa**: `0`

### 12. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_at`
  - **Output Variable:** `temp_tin1`

### 13. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 14. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `tintcsw_s`
  **Tax Unit:** `tu_individual_at`

### 15. Function: Elig
  **Eligibility Check:**
  - **Condition:** `GetPartnerIncome#1<=$tintcsw_spouse_maxthres & nDepChildrenInTu#2>0 &  IsWithPartner &  (il_taxableY > GetPartnerIncome#1 | (il_taxableY = GetPartnerIncome#1 & bch00_s>0))`
  - **Tax Unit:** `tu_individual_at`

### 16. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChildrenInTu#1>=3`
  - **comp_perTU**: `($tintcsw_amt1+amount#2+amount#3*(nDepChildrenInTu#1-2))`
  - **#_level**: `tu_bch00_at`
  - **#_amount**: `$tintcsw_amt3`
  - **output_add_var**: `tintcsw_s`
  - **TAX_UNIT**: `tu_individual_at`

### 17. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChildrenInTu>=3 & IsLoneParentOfDepChild`
  - **comp_perTU**: `$tintclp_amt1+amount#1+amount#2*(nDepChildrenInTu-2)`
  - **#_amount**: `$tintclp_amt3`
  - **output_var**: `tintclp_s`
  - **TAX_UNIT**: `tu_bch00_at`

### 18. Function: Allocate
  - **share**: `tintclp_s`
  - **share_between**: `IsLoneParentOfDepChild`
  - **output_var**: `tintclp_s`
  - **TAX_UNIT**: `tu_bch00_at`

### 19. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem>0`
  - **Tax Unit:** `tu_individual_at`

### 20. Function: ArithOp
  **Formula:** `$tintcox_amt`
  **Output Variable:** `tintcox_s`
  **Tax Unit:** `tu_individual_at`

### 21. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 22. Function: ArithOp
  **Formula:** `ils_pen-tscpehl01_s-tscpepi01_s-pxp00-pxpot`
  **Output Variable:** `temp_threshold`
  **Tax Unit:** `tu_individual_at`

### 23. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(tintcox_s=0 & tintcsw_s=0) & GetPartnerIncome#1<=$tintcpe_spouse_maxthres & IsWithPartner & ils_pen>0`
  - **Tax Unit:** `tu_individual_at`

### 24. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 25. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `temp_threshold>=$tintcpe2_thres2`
  - **comp_perTU**: `0`
  - **output_var**: `tintcpe_s`
  - **TAX_UNIT**: `tu_individual_at`

### 26. Function: Elig
  **Eligibility Check:**
  - **Condition:** `tintcpe_s=0 & tintcox_s=0 & ils_pen>0`
  - **Tax Unit:** `tu_individual_at`

### 27. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `temp_threshold>=$tintcpe_thres2`
  - **comp_perTU**: `0`
  - **output_add_var**: `tintcpe_s`
  - **TAX_UNIT**: `tu_individual_at`

### 28. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 29. Function: BenCalc
  - **comp_cond**: `tintcsw_s=0 & tintclp_s=0`
  - **comp_perTU**: `temp_tin2`
  - **comp_lowlim**: `n/a`
  - **#_level**: `n/a`
  - **output_var**: `temp_tin3`
  - **TAX_UNIT**: `tu_individual_at`

### 30. Function: BenCalc
  - **comp_cond**: `temp_tin5<=0`
  - **comp_perTU**: `temp_tin3 - tintcoxne_s - tintcpene_s - tinng_s-tintcfang_s`
  - **output_var**: `tin01_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_perTU**: `0`
  - **Comp_Cond**: `temp_tin5=0`

### 31. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_at`
  - **Output Variable:** `tin02_s`

### 32. Function: ArithOp
  **Formula:** `yemxp+pxp00+pxpot+bhlxp`
  **Output Variable:** `stm01_s`
  **Tax Unit:** `tu_individual_at`

### 33. Function: Elig
  **Eligibility Check:**
  - **Condition:** `stm01_s>=$tin_specialExempt_thres`
  - **Tax Unit:** `tu_individual_at`

### 34. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** ``

### 35. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_at`
  - **Output Variable:** `tin02_s`

### 36. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_at`
  - **Output Variable:** ``

### 37. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_at`
  - **Output Variable:** ``

### 38. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_at`
  - **Output Variable:** ``

### 39. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_at`
  - **Output Variable:** ``

### 40. Function: ArithOp
  **Formula:** `tin02_s`
  **Output Variable:** `tin02_s`
  **Tax Unit:** `tu_individual_at`

### 41. Function: ArithOp
  **Formula:** `tin01_s+tin02_s+temp_buncm`
  **Output Variable:** `tin_s`
  **Tax Unit:** `tu_individual_at`

### 42. Function: Elig
  **Eligibility Check:**
  - **Condition:** `buncm>0`
  - **Tax Unit:** `tu_individual_at`

### 43. Function: ArithOp
  **Formula:** `buncm*$tin_severance_rate`
  **Output Variable:** `temp_buncm`
  **Tax Unit:** `tu_individual_at`

### 44. Function: ArithOp
  **Formula:** `temp_nochildrenbasicamount*$tintcch_amt`
  **Output Variable:** `tintcch_s`
  **Tax Unit:** `tu_bch00_at`

### 45. Function: DefConst
  **Constants Defined:**
  - `$tintcch_amt`: 70.9#m
  - `$tintcsw_amt1`: 601#y
  - `$tintcsw_amt2`: 212#y
  - `$tintcsw_amt3`: 268#y
  - `$tintclp_amt1`: 601#y
  - `$tintclp_amt2`: 212#y
  - `$tintclp_amt3`: 268#y
  - `$tintcox_amt`: 487#y
  - `$tintcee_amt`: n/a
  - `$tintcpe_amt`: 1002#y
  - `$tintcpe_addAmt`: 1476#y
  - `$tintcfa_basic_amt`: 2000#y
  - `$tintcfa_student_amt`: 700#y
  - `$tintcfa_neg_amt`: 700#y
  - `$tintcox_addAmt`: 790#y
  - `$tintcox_infl_amt`: n/a
  - `$tintcpe_infl_amt`: n/a
  - `$tintcsw_spouse_maxthres`: 7284#y
  - `$tintcox_thres1`: 19424#y
  - `$tintcox_thres2`: 29743#y
  - `$tintcpe_spouse_maxthres`: 2673#y
  - `$tintcpe2_thres1`: 24196#y
  - `$tintcpe2_thres2`: 30957#y
  - `$tintcpe_thres1`: 21245#y
  - `$tintcpe_thres2`: 30957#y

### 46. Function: DefConst
  **Constants Defined:**
  - `$tintace_amt`: 132#y
  - `$tintaxp_amt`: n/a
  - `$tintatb_amt`: 730#y
  - `$tintase_rate`: 0.15
  - `$tintach_single_amt`: n/a
  - `$tintach_couple_amt`: n/a
  - `$tintase_uplim`: 33000#y

### 47. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_at`
  - **Output Variable:** ``

### 48. Function: ArithOp
  **Formula:** `temp_tin3-tintcox_s-tintcpe_s`
  **Output Variable:** `temp_tin4`
  **Tax Unit:** `tu_individual_at`

### 49. Function: BenCalc
  - **Comp_Cond**: `temp_tin4<0 & tintcox_s>0 & temp_tin3<0`
  - **Comp_perTU**: `0`
  - **Output_Var**: `tintcoxne_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_LowLim**: `n/a`
  - **Comp_UpLim**: `tintcox_s`

### 50. Function: BenCalc
  - **Comp_Cond**: `temp_tin4<0 & tintcpe_s>0 & temp_tin3<0`
  - **Comp_perTU**: `0`
  - **Output_Var**: `tintcpene_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_LowLim**: `n/a`
  - **Comp_UpLim**: `tintcpe_s`

### 51. Function: BenCalc
  - **Comp_Cond**: `temp_tin5<=0 & yem>0 & tintcox_s>$tin_eeNeg_amt`
  - **Comp_perTU**: `temp_tin5* (-1)`
  - **Output_Var**: `tinng_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_UpLim**: `min(($tin_eeNeg_rate*ils_sicdy),($tin_eeNeg_amt + $tin_eeNeg_addAmt))`

### 52. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 53. Function: BenCalc
  - **comp_cond**: `((il_taxabley + tintase_s)-$tin_upthres1) >= tintase_s `
  - **comp_perTU**: `tintase_s`
  - **output_var**: `tintasene_s`
  - **TAX_UNIT**: `tu_individual_at`

### 54. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Comp_LowLim**: `n/a`

### 55. Function: BenCalc
  - **Comp_Cond**: `tintcpe_s=0`
  - **Comp_perTU**: `tinng_s`
  - **Output_Var**: `tinng_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_LowLim**: `0`

### 56. Function: BenCalc
  - **Comp_Cond**: `tintcsw_s =0 & tintclp_s =0 & temp_tinfa_partner<$tintcfa_neg_amt*temp_nochildrenbasicamount#2 & temp_tin1<$tintcfa_neg_amt*temp_nochildrenbasicamount#2`
  - **Comp_perElig**: `($tintcfa_neg_amt*temp_nochildrenbasicamount#2) - temp_tin1`
  - **Output_Var**: `tintcfang_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **LowLim**: `0`
  - **Who_Must_Be_Elig**: `all`
  - **#_Level**: `tu_bch00_at`
  - **UpLim**: `$tintcfa_neg_amt*temp_nochildrenbasicamount`

### 57. Function: BenCalc
  - **Comp_Cond**: `temp_tintcfa00 > temp_tin1fa`
  - **Comp_perTU**: `temp_tin1fa`
  - **Output_Var**: `tintcfa00_s`
  - **TAX_UNIT**: `tu_individual_at`

### 58. Function: ArithOp
  **Formula:** `temp_tin1-temp_tintcfa00`
  **Output Variable:** `temp_tin2`
  **Tax Unit:** `tu_individual_at`

### 59. Function: ArithOp
  **Formula:** `temp_tin1-tintcfa00_s`
  **Output Variable:** `temp_tin2`
  **Tax Unit:** `tu_individual_at`

### 60. Function: BenCalc
  - **Comp_Cond**: `temp_tinfa<= ($tintcfa_basic_amt/2) & temp_tinfa_partner<=($tintcfa_basic_amt/2)`
  - **Comp_perTU**: `($tintcfa_basic_amt/2)`
  - **Output_Add_Var**: `temp_tintcfa00`
  - **TAX_UNIT**: `tu_individual_at`
  - **Who_Must_Be_Elig**: `one`

### 61. Function: BenCalc
  - **Comp_Cond**: `temp_tinfa<= ($tintcfa_basic_amt/2) & temp_tinfa_partner<=($tintcfa_basic_amt/2)`
  - **Comp_perTU**: `($tintcfa_basic_amt/2)`
  - **Output_Add_Var**: `temp_tintcfa00`
  - **TAX_UNIT**: `tu_individual_at`
  - **Who_Must_Be_Elig**: `one`

### 62. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bch00_s#1>0 &temp_nochildrenbasicamount1#1>=2 & temp_tinfa>0 & IsParentOfDepChild#1`
  - **Tax Unit:** `tu_individual_at`

### 63. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bch00_s#1>0 &temp_nochildrenbasicamount1#1>=1 & temp_tinfa >0 & IsParentOfDepChild#1`
  - **Tax Unit:** `tu_individual_at`

### 64. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bch00_s#1>0 &temp_nochildrenbasicamount1#1>=3 & temp_tinfa>0 & IsParentOfDepChild#1`
  - **Tax Unit:** `tu_individual_at`

### 65. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bch00_s#1>0 &temp_nochildrenbasicamount1#1>=4 & temp_tinfa>0 & IsParentOfDepChild#1`
  - **Tax Unit:** `tu_individual_at`

### 66. Function: BenCalc
  - **Comp_Cond**: `temp_tinfa>temp_tinfa_partner | (temp_tinfa=temp_tinfa_partner & bch00_s>0)`
  - **Comp_perTU**: `$tintcfa_basic_amt*(temp_nochildrenbasicamount1#2-3)`
  - **Output_Add_Var**: `temp_tintcfa00`
  - **TAX_UNIT**: `tu_individual_at`
  - **#_Level**: `tu_bch00_at`
  - **Who_Must_Be_Elig**: `one`

### 67. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bch00_s#1>0 &temp_nochildrenbasicamount2#1>=3 & temp_tinfa >0 & IsParentOfDepChild#1`
  - **Tax Unit:** `tu_individual_at`

### 68. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bch00_s#1>0 &temp_nochildrenbasicamount2#1>=2 & temp_tinfa >0 & IsParentOfDepChild#1`
  - **Tax Unit:** `tu_individual_at`

### 69. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bch00_s#1>0 &temp_nochildrenbasicamount2#1>=1 & temp_tinfa >0 & IsParentOfDepChild#1`
  - **Tax Unit:** `tu_individual_at`

### 70. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bch00_s#1>0 &temp_nochildrenbasicamount2#1>=4 & temp_tinfa >0 & IsParentOfDepChild#1`
  - **Tax Unit:** `tu_individual_at`

### 71. Function: BenCalc
  - **Comp_Cond**: `temp_tinfa>temp_tinfa_partner | (temp_tinfa=temp_tinfa_partner & bch00_s>0)`
  - **Comp_perTU**: `$tintcfa_student_amt*(temp_nochildrenbasicamount2#2-3)`
  - **Output_Add_Var**: `temp_tintcfa00`
  - **TAX_UNIT**: `tu_individual_at`
  - **#_Level**: `tu_bch00_at`
  - **Who_Must_Be_Elig**: `one`

### 72. Function: BenCalc
  - **Comp_Cond**: `temp_tinfa<= ($tintcfa_basic_amt/2) & temp_tinfa_partner<=($tintcfa_basic_amt/2)`
  - **Comp_perTU**: `($tintcfa_basic_amt/2)`
  - **Output_Add_Var**: `temp_tintcfa00`
  - **TAX_UNIT**: `tu_individual_at`
  - **Who_Must_Be_Elig**: `one`

### 73. Function: BenCalc
  - **Comp_Cond**: `temp_tinfa<= ($tintcfa_student_amt/2) & temp_tinfa_partner<=($tintcfa_student_amt/2)`
  - **Comp_perTU**: `($tintcfa_student_amt/2)`
  - **Output_Add_Var**: `temp_tintcfa00`
  - **TAX_UNIT**: `tu_individual_at`
  - **Who_Must_Be_Elig**: `one`

### 74. Function: BenCalc
  - **Comp_Cond**: `temp_tinfa<= ($tintcfa_student_amt/2) & temp_tinfa_partner<=($tintcfa_student_amt/2)`
  - **Comp_perTU**: `($tintcfa_student_amt/2)`
  - **Output_Add_Var**: `temp_tintcfa00`
  - **TAX_UNIT**: `tu_individual_at`
  - **Who_Must_Be_Elig**: `one`

### 75. Function: BenCalc
  - **Comp_Cond**: `temp_tinfa<= ($tintcfa_student_amt/2) & temp_tinfa_partner<=($tintcfa_student_amt/2)`
  - **Comp_perTU**: `($tintcfa_student_amt/2)`
  - **Output_Add_Var**: `temp_tintcfa00`
  - **TAX_UNIT**: `tu_individual_at`
  - **Who_Must_Be_Elig**: `one`

### 76. Function: ArithOp
  **Formula:** `temp_tin1fa-temp_tintcfa00`
  **Output Variable:** `temp_tinfa`
  **Tax Unit:** `tu_individual_at`

### 77. Function: ArithOp
  **Formula:** `temp_tin1fa-temp_tintcfa00`
  **Output Variable:** `temp_tinfa`
  **Tax Unit:** `tu_individual_at`

### 78. Function: ArithOp
  **Formula:** `temp_tin1fa-temp_tintcfa00`
  **Output Variable:** `temp_tinfa`
  **Tax Unit:** `tu_individual_at`

### 79. Function: ArithOp
  **Formula:** `temp_tin1fa-temp_tintcfa00`
  **Output Variable:** `temp_tinfa`
  **Tax Unit:** `tu_individual_at`

### 80. Function: ArithOp
  **Formula:** `temp_tin1fa-temp_tintcfa00`
  **Output Variable:** `temp_tinfa`
  **Tax Unit:** `tu_individual_at`

### 81. Function: ArithOp
  **Formula:** `temp_tin1fa-temp_tintcfa00`
  **Output Variable:** `temp_tinfa`
  **Tax Unit:** `tu_individual_at`

### 82. Function: ArithOp
  **Formula:** `temp_tin1fa-temp_tintcfa00`
  **Output Variable:** `temp_tinfa`
  **Tax Unit:** `tu_individual_at`

### 83. Function: ArithOp
  **Formula:** `GetPartnerIncome#2 - GetPartnerIncome#3`
  **Output Variable:** `temp_tinfa_partner`
  **Tax Unit:** `tu_individual_at`

### 84. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `temp_tintcfa00`
  **Tax Unit:** `tu_individual_at`

### 85. Function: ArithOp
  **Formula:** `GetPartnerIncome#2 - GetPartnerIncome#3`
  **Output Variable:** `temp_tinfa_partner`
  **Tax Unit:** `tu_individual_at`

### 86. Function: ArithOp
  **Formula:** `GetPartnerIncome#2 - GetPartnerIncome#3`
  **Output Variable:** `temp_tinfa_partner`
  **Tax Unit:** `tu_individual_at`

### 87. Function: ArithOp
  **Formula:** `GetPartnerIncome#2 - GetPartnerIncome#3`
  **Output Variable:** `temp_tinfa_partner`
  **Tax Unit:** `tu_individual_at`

### 88. Function: ArithOp
  **Formula:** `GetPartnerIncome#2 - GetPartnerIncome#3`
  **Output Variable:** `temp_tinfa_partner`
  **Tax Unit:** `tu_individual_at`

### 89. Function: ArithOp
  **Formula:** `GetPartnerIncome#2 - GetPartnerIncome#3`
  **Output Variable:** `temp_tinfa_partner`
  **Tax Unit:** `tu_individual_at`

### 90. Function: ArithOp
  **Formula:** `GetPartnerIncome#2 - GetPartnerIncome#3`
  **Output Variable:** `temp_tinfa_partner`
  **Tax Unit:** `tu_individual_at`

### 91. Function: ArithOp
  **Formula:** `GetPartnerIncome#2 - GetPartnerIncome#3`
  **Output Variable:** `temp_tinfa_partner`
  **Tax Unit:** `tu_individual_at`

### 92. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yse>0 & yem>0`
  - **Tax Unit:** `tu_individual_at`

### 93. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bch00_s#1>0`
  - **Tax Unit:** `tu_bcc_at`

### 94. Function: ArithOp
  **Formula:** `tintcfa00_s + tintcfang_s`
  **Output Variable:** `tintcfa_s`
  **Tax Unit:** `tu_individual_at`

### 95. Function: ArithOp
  **Formula:** `temp_tin4 - tintcfang_s`
  **Output Variable:** `temp_tin5`
  **Tax Unit:** `tu_individual_at`

### 96. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yem >0 | yse>0)  | (bcc01my + bcc02my + bcc03my + bcc04my +bcc05my = 12)`
  - **Tax Unit:** `tu_bch00_at`

### 97. Function: ArithOp
  **Formula:** `temp_tin1fa-temp_tintcfa00`
  **Output Variable:** `temp_tinfa`
  **Tax Unit:** `tu_individual_at`

### 98. Function: BenCalc
  - **Comp_Cond**: `il_progressionadj<=0`
  - **Comp_perTU**: `temp_tin1`
  - **Output_Var**: `temp_tin1fa`
  - **TAX_UNIT**: `tu_individual_at`

### 99. Function: ArithOp
  **Formula:** `temp_childbasicamount2`
  **Output Variable:** `temp_nochildrenbasicamount2`
  **Tax Unit:** `tu_bch01_at`

### 100. Function: ArithOp
  **Formula:** `1`
  **Output Variable:** `temp_childbasicamount2`
  **Tax Unit:** `tu_individual_at`

### 101. Function: Elig
  **Eligibility Check:**
  - **Condition:** `temp_base>0&dag>=18`
  - **Tax Unit:** `tu_individual_at`

### 102. Function: ArithOp
  **Formula:** `temp_childbasicamount1`
  **Output Variable:** `temp_nochildrenbasicamount1`
  **Tax Unit:** `tu_bch01_at`

### 103. Function: ArithOp
  **Formula:** `1`
  **Output Variable:** `temp_childbasicamount1`
  **Tax Unit:** `tu_individual_at`

### 104. Function: Elig
  **Eligibility Check:**
  - **Condition:** `temp_base>0&dag<18`
  - **Tax Unit:** `tu_individual_at`

### 105. Function: BenCalc
  - **Comp_Cond**: `yem>0 & il_taxableY>$tintcox_thres2 & tintcox_s>0`
  - **Comp_perTU**: `0`
  - **Output_Add_Var**: `tintcox_s`
  - **TAX_UNIT**: `tu_individual_at`

### 106. Function: BenCalc
  - **Comp_Cond**: `il_tahealth > 36400#y`
  - **Comp_perTU**: `0.12`
  - **Output_Var**: `tinratahl_s`
  - **TAX_UNIT**: `tu_individual_at`

### 107. Function: BenCalc
  - **Comp_Cond**: `(GetPartnerIncome#1<=$tintcsw_spouse_maxthres &  IsWithPartner &  (il_taxableY > GetPartnerIncome#1 | (il_taxableY = GetPartnerIncome#1 & bch00_s>0))) | (nDepChildrenInTu>0 & IsLoneParentOfDepChild)`
  - **Comp_perTU**: `-0.01`
  - **#_Income**: `il_taxablepartnery`
  - **Output_Add_Var**: `tinratahl_s`
  - **TAX_UNIT**: `tu_individual_at`

### 108. Function: ArithOp
  **Formula:** `-0.01*(temp_nochildrenbasicamount1+temp_nochildrenbasicamount2)`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_at`

### 109. Function: ArithOp
  **Formula:** `tinratahl_s`
  **Output Variable:** `tinratahl_s`
  **Tax Unit:** `tu_individual_at`

### 110. Function: ArithOp
  **Formula:** `xhl00 - (il_tahealth * tinratahl_s)`
  **Output Variable:** `tintahl_s`
  **Tax Unit:** `tu_individual_at`

### 111. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **LowLim**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 112. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `il_taxableY>0`
  - **Comp_perTU**: `yempv/il_taxableY`
  - **Output_Var**: `i_share`
  - **TAX_UNIT**: `tu_individual_at`
  - **UpLim**: `1`
  - **LowLim**: `0`

### 113. Function: ArithOp *(Switch: off)*
  **Formula:** `tin_s-(tin_s*i_share)`
  **Output Variable:** `tin_s`
  **Tax Unit:** `tu_individual_at`


---

## Policy: bunnc_at
### 1. Function: DefConst
  **Constants Defined:**
  - `$bun_minAmt`: 42.47#d
  - `$bunnc_exemptChild_amt`: 0
  - `$bunnc_exemptPar_amt`: 0
  - `$bunnc_child_minAmt2`: 0
  - `$bunnc_child_minAmt1`: 0
  - `$bunnc_minAmt`: 0
  - `$bun_fa_amt`: 0.97#d

### 2. Function: BenCalc
  - **comp_cond**: `bunctmy_s=0 & bunnc>0`
  - **comp_perTU**: `bunncmy`
  - **comp_lowlim**: `0`
  - **round_to**: `1`
  - **output_var**: `bunncmy_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_perTU**: `12-bunctmy_s`
  - **Comp_Cond**: `lnu>0 & lunmy_s>0 & (liwmy02_a>=$UB_QperMin1 | liwmy02_a>= $UB_QperMin3) & dag>=16 & poa00=0 & poacs=0 & (yem>0 | (lse=0 | yse=0))`
  - **Comp_LowLim**: `0`

### 3. Function: DefVar
  - **temp_bunct**: `0`
  - **temp_thresholdbch00earn**: `0`
  - **i_bunnctumy**: `0`

### 4. Function: BenCalc
  - **comp_cond**: `bunct_s>0`
  - **comp_perTU**: `bunct_s*12/bunctmy_s`
  - **output_var**: `temp_bunct`
  - **TAX_UNIT**: `tu_individual_at`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `il_bunnc<$tsc_minThres1   & poa00=0 & poacs=0 & bunncmy_s>0`
  - **Tax Unit:** `tu_individual_at`

### 6. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `bunncmy_s>6 & bunctmy_s<=5 & temp_bunct>$bun_minAmt`
  - **comp_perTU**: `0.92*temp_bunct * bunncmy_s / 12`
  - **comp_lowlim**: `0.95*$bun_minAmt* bunncmy_s / 12`
  - **output_var**: `bunnc_s`
  - **TAX_UNIT**: `tu_individual_at`

### 7. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_income**: `n/a`
  - **#_level**: `n/a`
  - **lowlim**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **#_Level**: `n/a`

### 8. Function: BenCalc
  - **comp_cond**: `(sel01_s*nDepChildrenInTu>0)#1 & bunnc_s>0`
  - **comp_perTU**: `($bun_fa_amt*sel01_s*nDepChildrenInTU#1)*bunncmy_s / 12`
  - **#_level**: `tu_bch00_at`
  - **output_add_var**: `bunmt_s`
  - **TAX_UNIT**: `tu_individual_at`

### 9. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(sel01_s*nDepChildrenInTu>0)#2 & bunnc_s>0 & GetPartnerIncome#1<=$tsc_minThres1*14/12`
  - **Tax Unit:** `tu_individual_at`

### 10. Function: BenCalc
  - **comp_cond**: `temp_thresholdbch00earn>0`
  - **comp_perTU**: `$bun_fa_amt*bunncmy_s / 12`
  - **output_add_var**: `bunmt_s`
  - **TAX_UNIT**: `tu_individual_at`

### 11. Function: Elig
  **Eligibility Check:**
  - **Condition:** `nDepChildrenInTu#1>0 & bch00_s#1>0`
  - **Tax Unit:** `tu_individual_at`

### 12. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 13. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 14. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `bunctmy_s>0`
  - **Comp_perTU**: `i_bunct*12/bunctmy_s`
  - **Output_Var**: `temp_bunct`
  - **TAX_UNIT**: `tu_individual_at`

### 15. Function: BenCalc *(Switch: off)*
  - **who_must_be_elig**: `all`
  - **comp_cond**: `bunncmy_s>6 & bunctmy_s<=5 & temp_bunct>$bun_minAmt`
  - **comp_perTU**: `0.92*temp_bunct`
  - **comp_lowlim**: `0.95*$bun_minAmt`
  - **output_var**: `bunnc_s`
  - **TAX_UNIT**: `tu_individual_at`


---

## Policy: bunct_at

---

## Policy: bunnc_at

---

## Policy: pmmtu_at

---

## Policy: tscpe_at

---

## Policy: tin_at

---

## Policy: tiniy_at
### 1. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_at`
  - **Output Variable:** `tiniy_s`


---

## Policy: bcc00_at
### 1. Function: DefIl
  - **name**: `il_bcc`
  - **ils_pen**: `+`
  - **bhl00**: `+`
  - **bunct_s**: `+`
  - **bunnc_s**: `+`
  - **yem**: `+`
  - **ypr**: `+`
  - **yse**: `+`
  - **yiy**: `+`
  - **bhlot**: `+`
  - **buntr**: `+`
  - **bunot**: `+`

### 2. Function: DefVar
  - **temp_ilbcc**: `0`
  - **temp_model**: `0`
  - **temp_incdep**: `0`
  - **temp_suppl**: `0`
  - **temp_age3**: `0`
  - **temp_age2**: `0`
  - **temp_age1**: `0`
  - **temp_age0**: `0`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsParentOfDepChild | IsLoneParentOfDepChild`
  - **Tax Unit:** `tu_bcc_at`

### 4. Function: ArithOp
  **Formula:** `il_bcc`
  **Output Variable:** `temp_ilbcc`
  **Tax Unit:** `tu_individual_at`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bch00_s#1>0`
  - **Tax Unit:** `tu_bcc_at`

### 6. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMax**: `n/a`
  - **#_amount**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 7. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 8. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **#_amount**: `n/a`
  - **#_level**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 9. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **#_amount**: `n/a`
  - **#_level**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 10. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChildrenInTu#1>0 & il_bma>0 & temp_rand>$bcc731_y0_mo & temp_rand<=$bcc639_y0_mo`
  - **comp_perTU**: `$bcc639*10/12`
  - **#_AgeMax**: `0`
  - **#_amount**: `n/a`
  - **output_var**: `temp_age0`
  - **TAX_UNIT**: `tu_bcc_at`
  - **Comp_Cond**: `nDepChildrenInTu#1>0 & il_bma>0 & temp_rand>$bcc457_y0_mo & temp_rand<=$bcc365_y0_mo`
  - **Comp_perTU**: `$bcc365*10/12`
  - **#_Amount**: `n/a`

### 11. Function: BenCalc
  - **comp_cond**: `il_bma<temp_age0 & il_bma>0`
  - **comp_perTU**: `(temp_age0-il_bma)*2/12`
  - **output_add_var**: `temp_age0`
  - **TAX_UNIT**: `tu_bcc_at`

### 12. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChildrenInTu#1>0 & (temp_ilbcc#6<$bcc_y & IsParentOfDepChild & dgn=1 & !IsLoneParentOfDepChild) & temp_age0=0  & temp_rand>$bcc457_y1_fa & temp_rand<=$bcc365_y1_fa`
  - **comp_perTU**: `$bcc365*3/12`
  - **#_AgeMin**: `1`
  - **#_AgeMax**: `1`
  - **#_amount**: `n/a`
  - **#_level**: `tu_individual_at`
  - **output_var**: `temp_age1`
  - **TAX_UNIT**: `tu_bcc_at`
  - **#_Amount**: `n/a`
  - **Comp_Cond**: `nDepChildrenInTu#1>0 & (temp_ilbcc#6<$bcc_y & IsParentOfDepChild & dgn=1 & !IsLoneParentOfDepChild) & temp_age0=0  & temp_rand>$bcc639_y1_fa & temp_rand<=$bcc457_y1_fa`
  - **Comp_perTU**: `$bcc457*3.75/12`

### 13. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChildrenInTu#1>0 & (temp_ilbcc#4<$bcc_y & IsParentOfDepChild & dgn=1 & !IsLoneParentOfDepChild) & temp_age0=0 & temp_age1=0 & temp_rand<=$bcc851_y2_fa`
  - **comp_perTU**: `$bcc851*7/12`
  - **#_AgeMin**: `2`
  - **#_AgeMax**: `2`
  - **#_amount**: `n/a`
  - **#_level**: `tu_individual_at`
  - **output_var**: `temp_age2`
  - **TAX_UNIT**: `tu_bcc_at`
  - **Comp_Cond**: `nDepChildrenInTu#1>0 & (temp_ilbcc#4<$bcc_y & IsParentOfDepChild & dgn=1 & !IsLoneParentOfDepChild) & temp_age0=0 & temp_age1=0  & temp_rand>$bcc731_y2_fa & temp_rand<=$bcc639_y2_fa`
  - **Comp_perTU**: `$bcc639*2.25/12`

### 14. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChildrenInTu#3>1 & temp_age2>0`
  - **comp_perTU**: `temp_age2*$bcc_child_suppl_rate*(nDepChildrenInTu#3-1)`
  - **#_AgeMax**: `2`
  - **#_AgeMin**: `2`
  - **output_var**: `temp_suppl`
  - **TAX_UNIT**: `tu_bcc_at`

### 15. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsParentOfDepChild#2 & (dgn=0 | IsLoneParentOfDepChild) & nDepChildrenInTu#1>0 & il_bma>0  & bunct=0 & temp_ilbcc<$bccid_y & temp_rand#2>$bcc365_y0_mo & temp_rand#2<=$bccid_y0_mo`
  - **comp_perTU**: `min((il_bma*$bccid*10/12),$bccid_max)`
  - **#_AgeMax**: `0`
  - **#_level**: `tu_bcc_at`
  - **#_amount**: `n/a`
  - **output_var**: `temp_incdep`
  - **TAX_UNIT**: `tu_individual_at`
  - **#_Amount**: `n/a`

### 16. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChildrenInTu#1>0 & il_bma#2=0 & temp_ilbcc<$bccid_y & IsParentOfDepChild#2 & dgn=1 & !IsLoneParentOfDepChild &  temp_age0#2=0  & & temp_age1#2=0 & temp_incdep=0 & temp_rand#2>$bcc365_y1_fa & temp_rand#2<=$bccid_y1_fa`
  - **comp_perTU**: `min((il_bma*$bccid*2/12),$bccid_max)`
  - **#_level**: `tu_bcc_at`
  - **#_amount**: `n/a`
  - **output_add_var**: `temp_incdep`
  - **TAX_UNIT**: `tu_individual_at`
  - **#_AgeMin**: `1`
  - **#_AgeMax**: `1`

### 17. Function: ArithOp
  **Formula:** `temp_age0+temp_age1+temp_age2+temp_suppl+temp_incdep`
  **Output Variable:** `bcc00_s`
  **Tax Unit:** `tu_bcc_at`

### 18. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$bcc00_distr_coef1`: n/a
  - `$bcc00_distr_coef10`: n/a
  - `$bcc00_distr_coef9`: n/a
  - `$bcc00_distr_coef8`: n/a
  - `$bcc00_distr_coef7`: n/a
  - `$bcc00_distr_coef6`: n/a
  - `$bcc00_distr_coef5`: n/a
  - `$bcc00_distr_coef4`: n/a
  - `$bcc00_distr_coef3`: n/a
  - `$bcc00_distr_coef2`: n/a
  - `Run_Cond`: n/a
  - `#_DataBasename`: n/a
  - `$bcc00_distr_coef11`: n/a
  - `$bcc00_distr_coef12`: n/a
  - `$bcc00_distr_coef13`: n/a

### 19. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$bcc00_distr_coef1`: n/a
  - `$bcc00_distr_coef10`: n/a
  - `$bcc00_distr_coef9`: n/a
  - `$bcc00_distr_coef8`: n/a
  - `$bcc00_distr_coef7`: n/a
  - `$bcc00_distr_coef6`: n/a
  - `$bcc00_distr_coef5`: n/a
  - `$bcc00_distr_coef4`: n/a
  - `$bcc00_distr_coef3`: n/a
  - `$bcc00_distr_coef2`: n/a
  - `Run_Cond`: n/a
  - `#_DataBasename`: n/a
  - `$bcc00_distr_coef11`: n/a
  - `$bcc00_distr_coef12`: n/a
  - `$bcc00_distr_coef13`: n/a

### 20. Function: DefConst
  **Constants Defined:**
  - `Run_Cond`: !IsUsedDatabase#1
  - `#_DataBasename`: *_hhot
  - `$bcc851_y0_mo`: 0.163
  - `$bcc791_y0_mo`: 0.195
  - `$bcc731_y0_mo`: 0.296
  - `$bcc639_y0_mo`: 0.341
  - `$bcc457_y0_mo`: 0.388
  - `$bcc365_y0_mo`: 0.521
  - `$bccid_y0_mo`: 1.000
  - `$bcc851_y1_mo`: 0.477
  - `$bcc791_y1_mo`: 0.571
  - `$bcc731_y1_mo`: 0.866
  - `$bcc639_y1_mo`: 0.965
  - `$bcc457_y1_mo`: 1.000
  - `$bcc851_y2_mo`: 0.910
  - `$bcc791_y2_mo`: 1.000

### 21. Function: DefConst
  **Constants Defined:**
  - `Run_Cond`: !IsUsedDatabase#1
  - `#_DataBasename`: *_hhot
  - `$bcc639_y1_fa`: 0.081
  - `$bcc457_y1_fa`: 0.187
  - `$bcc365_y1_fa`: 0.426
  - `$bccid_y1_fa`: 1.000
  - `$bcc851_y2_fa`: 0.554
  - `$bcc791_y2_fa`: 0.657
  - `$bcc731_y2_fa`: 0.951
  - `$bcc639_y2_fa`: 1.000

### 22. Function: DefConst
  **Constants Defined:**
  - `$bcc851`: 17.65#d
  - `$bcc791`: 18.98#d
  - `$bcc731`: 20.56#d
  - `$bcc639`: 23.50#d
  - `$bcc457`: 32.86#d
  - `$bcc365`: 41.14#d
  - `$bccid`: 0.8
  - `$bccid_max`: 80.12#d
  - `$bcc_y`: 18000#y
  - `$bccid_y`: 8600#y
  - `$bcc_child_suppl_rate`: 0.5

### 23. Function: DefConst
  **Constants Defined:**
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: *_hhot
  - `$bcc851_y0_mo`: 1
  - `$bcc791_y0_mo`: 2
  - `$bcc731_y0_mo`: 3
  - `$bcc639_y0_mo`: 4
  - `$bcc457_y0_mo`: 5
  - `$bcc365_y0_mo`: 6
  - `$bccid_y0_mo`: 7
  - `$bcc851_y1_mo`: 1
  - `$bcc791_y1_mo`: 2
  - `$bcc731_y1_mo`: 3
  - `$bcc639_y1_mo`: 4
  - `$bcc457_y1_mo`: 5
  - `$bcc851_y2_mo`: 1
  - `$bcc791_y2_mo`: 2

### 24. Function: DefConst
  **Constants Defined:**
  - `Run_Cond`: IsUsedDatabase#1
  - `#_DataBasename`: *_hhot
  - `$bcc639_y1_fa`: 1
  - `$bcc457_y1_fa`: 2
  - `$bcc365_y1_fa`: 3
  - `$bccid_y1_fa`: 4
  - `$bcc851_y2_fa`: 1
  - `$bcc791_y2_fa`: 2
  - `$bcc731_y2_fa`: 3
  - `$bcc639_y2_fa`: 4


---

## Policy: bcctu_at
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `temp_age0>0`
  - **Tax Unit:** `tu_bcc_at`

### 2. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(IsParentOfDepChild & dgn=0 & IsWithPartner & temp_ilbcc#1<amount#7 & GetPartnerIncome#2<amount#8) & nDepChildrenInTu#9>0`
  - **comp_perTU**: `n/a`
  - **Comp_perTU**: `amount#3`
  - **#_level**: `tu_individual_at`
  - **#_income**: `temp_ilbcc`
  - **#_amount**: `$bcctu_thresh2`
  - **#_AgeMax**: `0`
  - **output_var**: `bcctu_s`
  - **TAX_UNIT**: `tu_bcc_at`

### 3. Function: DefConst
  **Constants Defined:**
  - `$bcctu_amt`: 6.06#d
  - `$bcctu_thresh1`: 8100#y
  - `$bcctu_thresh2`: 18000#y


---

## Policy: bfamt_at *(Switch: n/a)*
### 1. Function: DefVar *(Switch: n/a)*
  - **temp_equivscale**: `n/a`
  - **temp_incometest**: `n/a`
  - **temp_ben**: `n/a`

### 2. Function: DefIl *(Switch: n/a)*
  - **name**: `n/a`
  - **ils_origy**: `n/a`
  - **ils_pen**: `n/a`
  - **bunct_s**: `n/a`
  - **bho**: `n/a`
  - **bcc00_s**: `n/a`
  - **bunnc_s**: `n/a`
  - **bed**: `n/a`
  - **bma**: `n/a`
  - **bhl00**: `n/a`
  - **bcctu_s**: `n/a`
  - **ils_sicdy**: `n/a`
  - **ils_tax**: `n/a`
  - **xmp**: `n/a`
  - **bhlot**: `n/a`
  - **buntr**: `n/a`
  - **bunot**: `n/a`
  - **bmact_s**: `n/a`

### 3. Function: BenCalc *(Switch: n/a)*
  - **comp_Cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **comp_cond**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 5. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 6. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** `n/a`

### 7. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`


---

## Policy: output_std_at
### 1. Function: DefOutput
  - **file**: `AT_2025_std`
  - **vargroup**: `tsc*`
  - **ilgroup**: `il_*`
  - **nDecimals**: `2`
  - **TAX_UNIT**: `tu_individual_at`
  - **unitinfo_tu**: `tu_bcc_at`
  - **unitinfo_id**: `IsPartner`
  - **ILGroup**: `ils_*`
  - **VarGroup**: `i*`


---

## Policy: output_std_hh_at *(Switch: off)*
### 1. Function: DefOutput
  - **file**: `AT_2025_std_hh`
  - **var**: `dwt`
  - **TAX_UNIT**: `tu_household_at`
  - **ILGroup**: `ils_*`


---

## Policy: setdefault_at
### 1. Function: DefVar *(Switch: off)*
  - **temp_ptu1**: `n/a`
  - **temp_ptu2**: `n/a`
  - **temp_ptu**: `n/a`

### 2. Function: SetDefault
  - **Dataset**: `AT_20??_??_????_??_??`
  - **yempv_a**: `0`
  - **lnu**: `0`
  - **liwmy_a**: `0`
  - **liwmy02_a**: `0`
  - **yemmy_a**: `0`
  - **lma**: `0`
  - **lma18**: `0`
  - **lma19**: `0`
  - **lmc20**: `0`
  - **lmc**: `0`
  - **bwkmcmy_a**: `0`
  - **lhw_a**: `0`
  - **lhw19_a**: `0`
  - **lhw18_a**: `0`
  - **yem_a**: `0`
  - **yem19_a**: `0`
  - **yem18_a**: `0`
  - **yemmy19_a**: `0`
  - **yemmy18_a**: `0`
  - **lhwsr_a**: `0`
  - **lma20**: `0`
  - **yemmy20_a**: `0`
  - **yem20_a**: `0`
  - **lhw20_a**: `0`
  - **lhwsr_s**: `0`
  - **lmcee_s**: `0`
  - **bch00**: `0`
  - **bchditu**: `0`
  - **bsamy**: `0`
  - **pmmtu**: `0`
  - **pmmtuyn**: `0`
  - **poadi**: `0`
  - **yptmp**: `0`
  - ** tpr**: `0`
  - **kfbcc**: `0`
  - **yemot**: `0`
  - **yot01**: `0`
  - **yot02**: `0`
  - **drgn2**: `0`
  - **les01**: `0`
  - **lindi**: `0`
  - **lfs**: `0`
  - **lowas**: `0`
  - **kfbmy**: `0`
  - **dct**: `1`
  - **bunpvyn_h**: `0`

### 3. Function: SetDefault
  - **Dataset**: `AT_20??_??_????_??_??`
  - **bcc06**: `0`
  - **bchas01**: `-1`
  - **bchas02**: `-1`
  - **bchas03**: `-1`
  - **bchditu**: `0`
  - **bchdiyn**: `0`
  - **kfbcc**: `0`
  - **kfb**: `0`
  - **kfbmy**: `0`
  - **pdi**: `0`
  - **poaot**: `0`
  - **bsa00**: `0`
  - **bsaot**: `0`
  - **bsaoa**: `0`
  - **powpt**: `0`
  - **pxpot**: `0`
  - **tpr**: `0`
  - **ydses_o**: `0`
  - **yemot**: `0`
  - **yot01**: `0`
  - **yot02**: `0`
  - **ypp01**: `0`
  - **ymwdt**: `0`
  - **bac01**: `0`
  - **bcc00**: `0`
  - **bcc05**: `0`
  - **bccrd**: `0`
  - **bch00**: `0`
  - **bfaam**: `0`
  - **bfamt**: `0`
  - **bsamy**: `0`
  - **buncm**: `0`
  - **pmmtu**: `0`
  - **pmmtuyn**: `0`
  - **poadi**: `0`
  - **yptmp**: `0`
  - **xed00**: `0`
  - **xhl00**: `0`
  - **poa**: `0`
  - **bun**: `0`
  - **bhl**: `0`
  - **bedes**: `0`
  - **bedet**: `0`
  - **bedot**: `0`
  - **ypp**: `0`
  - **ypt00**: `0`
  - **yptot**: `0`
  - **tscer**: `0`
  - **lfs**: `0`
  - **afc**: `0`
  - **bec**: `0`
  - **lcb_a**: `0`

### 4. Function: InitVars
  - **bclmc_s**: `0`
  - **bec01_s**: `0`
  - **bec02_s**: `0`
  - **bec03_s**: `0`
  - **bec04_s**: `0`
  - **bedtu01_s**: `0`
  - **bedtu02_s**: `0`
  - **butmc01_s**: `0`
  - **butmc02_s**: `0`
  - **bhltu_s**: `0`
  - **bhotu_s**: `0`
  - **bmact_s**: `0`
  - **bsa_s**: `0`
  - **bsatu_s**: `0`
  - **bunmt_s**: `0`
  - **bunnc_s**: `0`
  - **bunnctu_s**: `0`
  - **buncttu_s**: `0`
  - **pch00_s**: `0`
  - **pchcs_s**: `0`
  - **pcstu_s**: `0`
  - **pmmtu_s**: `0`
  - **ptu_s**: `0`
  - **ptu01_s**: `0`
  - **tin_s**: `0`
  - **tiniy_s**: `0`
  - **tscerrg_s**: `0`
  - **tintach_s**: `0`
  - **tintase_s**: `0`
  - **tintcfa_s**: `0`
  - **tintcfang_s**: `0`
  - **tintcfa00_s**: `0`
  - **tscseot_s**: `n/a`
  - **tscpehl01_s**: `0`
  - **tscpehl02_s**: `0`
  - **tscpepi01_s**: `0`
  - **tscpepi02_s**: `0`
  - **tintatb_s**: `0`
  - **tintclp_s**: `0`
  - **tintace_s**: `0`
  - **tintahl_s**: `0`
  - **bec05_s**: `0`

### 5. Function: InitVars
  - **bwkmcee_s**: `0`
  - **bwkmcse_s**: `0`
  - **bwkmceemy_s**: `0`
  - **bwkmcsemy_s**: `0`
  - **yemmc_s**: `0`
  - **yemmwmy_s**: `0`
  - **lmcee_s**: `0`
  - **lmcse_s**: `0`
  - **lhwsr_s**: `0`

### 6. Function: InitVars
  - **tscpepi01_s**: `0`
  - **tscpehl01_s**: `0`
  - **tscpepi02_s**: `0`
  - **tscpehl02_s**: `0`
  - **bunnc_s**: `0`
  - **tin_s**: `0`
  - **tiniy_s**: `0`
  - **pch00_s**: `0`
  - **pchcs_s**: `0`
  - **tintach_s**: `0`
  - **bmact_s**: `0`
  - **tintase_s**: `0`
  - **ptu_s**: `0`

### 7. Function: SetDefault
  - **Dataset**: `AT_20??_??_????_??_??`
  - **drgru**: `0`
  - **drgmd**: `0`
  - **drgur**: `0`
  - **bcc05my**: `0`
  - **bcc04my**: `0`
  - **bcc03my**: `0`
  - **bcc02my**: `0`
  - **bcc01my**: `0`

### 8. Function: DefVar *(Switch: off)*
  - **i_tin**: `0`
  - **i_share**: `0`

### 9. Function: SetDefault
  - **Dataset**: `AT_20??_??_????_??_??`
  - **ydsyc_a**: `0`

### 10. Function: SetDefault
  - **Dataset**: `*`
  - **bsayn_a**: `-1`

### 11. Function: DefIl
  - **Run_Cond**: `IsUsedDatabase#1`
  - **#_DataBasename**: `AT_20??_??_????_??_??`
  - **Name**: `il_xs_hl06`
  - **Warn_If_NonMonetary**: `no`
  - **RegExp_Def**: `xs06[0-9]+`
  - **RegExp_Factor**: `+`

### 12. Function: ArithOp
  **Formula:** `il_xs_hl06 * yds`
  **Output Variable:** `xhl00`
  **Tax Unit:** `tu_individual_at`
  **Run Condition:** `IsUsedDatabase#1`

### 13. Function: DefIl
  - **Run_Cond**: `IsUsedDatabase#1`
  - **#_DataBasename**: `AT_20??_??_????_??_??`
  - **Name**: `il_xs_hl10`
  - **Warn_If_NonMonetary**: `no`
  - **RegExp_Def**: `xs10[0-9]+`
  - **RegExp_Factor**: `+`

### 14. Function: ArithOp
  **Formula:** `il_xs_hl10 * yds`
  **Output Variable:** `xed00`
  **Tax Unit:** `tu_individual_at`
  **Run Condition:** `IsUsedDatabase#1`


---

## Policy: uprate_at
### 1. Function: Uprate
  - **dataset**: `*training_data`
  - **def_factor**: `1`
  - **WarnIfNoFactor**: `no`
  - **Dataset**: `*_hhot`

### 2. Function: Uprate
  - **dataset**: `AT_20??_??`
  - **WarnIfNoFactor**: `yes`
  - **bac00**: `$f_bac`
  - **bfa**: `$f_bfa`
  - **bfaam**: `$f_bfaam`
  - **bunnc**: `$f_bunnc`
  - **xhcrt**: `$f_xhcrt`
  - **ydses_o**: `$f_ydses`
  - **yempv**: `$f_hourly_wage_pv`
  - **yiy**: `$f_yiy`
  - **yse**: `$f_yse`
  - **afc**: `$f_yiy`
  - **bacot**: `$f_poa`
  - **bed**: `$f_one`
  - **bhlot**: `$f_hourly_wage_pv`
  - **bho**: `$f_bac`
  - **bunot**: `$f_bunct`
  - **buntr**: `$f_bunct`
  - **kfb**: `$f_one`
  - **poaot**: `$f_poa`
  - **pxpot**: `$f_poa`
  - **tad**: `$f_cpi`
  - **tis**: `$f_hourly_wage`
  - **xhc**: `$f_cpi`
  - **xmp**: `$f_cpi`
  - **xmpam**: `$f_cpi`
  - **yds**: `$f_ydses`
  - **yivwg**: `$f_hourly_wage`
  - **poa00**: `$f_poa`
  - **ypp01**: `$f_poa`
  - **ypp02**: `$f_one`
  - **bcc05**: `$f_hourly_wage`
  - **bcc06**: `$f_one`
  - **bhl00**: `$f_hourly_wage_pv`
  - **bhlxp**: `$f_hourly_wage_pv`
  - **bma**: `$f_hourly_wage_pv`
  - **xpp**: `$f_hourly_wage`
  - **yemxp**: `$f_hourly_wage`
  - **yot**: `$f_hourly_wage`
  - **ypt**: `$f_hourly_wage`
  - **bsa**: `$f_bac`
  - **bac01**: `$f_bac`
  - **poacs**: `$f_poa`
  - **psu**: `$f_poa`
  - **pxp00**: `$f_bac`
  - **bcc00**: `$f_bfa`
  - **Factor_Condition**: `lindi < 1 | lindi > 12`
  - **bdi**: `$f_bdi5`
  - **bccrd**: `$f_bfa`
  - **ypr**: `$f_xhcrt`
  - **bfamt**: `$f_bfa`
  - **bch00**: `$f_bfa`
  - **xhcmomi**: `$f_yiy`
  - **powpt**: `$f_poa`
  - **bunct**: `$f_bunct`
  - **kivho**: `$f_cpi`
  - **xhcot**: `$f_cpi`
  - **buncm**: `$f_bunct`
  - **yemot**: `$f_hourly_wage`
  - **pdi**: `$f_poa`
  - **pmmtu**: `$f_bac`
  - **yem_a**: `$f_hourly_wage`
  - **yot02**: `$f_hourly_wage`
  - **yot01**: `$f_yot01`
  - **poadi**: `$f_poa`
  - **yptmp**: `$f_hourly_wage`
  - **ymwdt**: `$f_hourly_wage_dt`
  - **yem19_a**: `$f_hourly_wage`
  - **yem18_a**: `$f_hourly_wage`
  - **yem20_a**: `$f_hourly_wage`
  - **bsa00**: `$f_bac`
  - **bsaoa**: `$f_bac`
  - **bsaot**: `$f_bac`
  - **xed00**: `$f_cpi`
  - **xhl00**: `$f_cpi`
  - **yem**: `$f_hourly_wage`
  - **poa**: `$f_poa`
  - **bun**: `$f_bunct`
  - **bhl**: `$f_cpi`
  - **bedes**: `$f_one`
  - **bedet**: `$f_one`
  - **bedot**: `$f_one`
  - **ypp**: `$f_cpi`
  - **ypt00**: `$f_cpi`
  - **yptot**: `$f_cpi`
  - **tscer**: `$f_yem`
  - **Dataset**: `AT_20??_??_????_??_??`
  - **bec**: `$f_one`


---

## Policy: IlsDef_at
### 1. Function: DefIl
  - **name**: `ils_origy`
  - **yem**: `+`
  - **yse**: `+`
  - **yiy**: `+`
  - **yot01**: `+`
  - **ypp01**: `+`
  - **ypp02**: `+`
  - **ypt**: `+`
  - **ypr**: `+`
  - **xmp**: `-`
  - **yemot**: `+`
  - **yemmc_s**: `n/a`
  - **yot02**: `+`

### 2. Function: DefIl
  - **name**: `ils_pen`
  - **poa00**: `+`
  - **psu**: `+`
  - **poaot**: `+`
  - **poacs**: `+`
  - **powpt**: `+`
  - **ptu_s**: `n/a`
  - **ptu01_s**: `n/a`

### 3. Function: DefIl
  - **name**: `ils_origrepy`
  - **ils_origy**: `+`
  - **ils_pen**: `+`
  - **bunct_s**: `+`
  - **bhl00**: `+`
  - **bac00**: `+`
  - **bma**: `+`
  - **bdi**: `+`
  - **bacot**: `+`
  - **bhlot**: `+`
  - **buntr**: `+`
  - **bunot**: `+`
  - **bac01**: `+`
  - **bmact_s**: `+`
  - **bunnctu_s**: `n/a`
  - **buncttu_s**: `n/a`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`

### 4. Function: DefIl
  - **name**: `ils_earns`
  - **yem**: `+`
  - **yse**: `+`
  - **yemmc_s**: `n/a`

### 5. Function: DefIl
  - **name**: `ils_bensim`
  - **bch00_s**: `+`
  - **bcc00_s**: `+`
  - **bcctu_s**: `+`
  - **bsa_s**: `+`
  - **bfamt_s**: `n/a`
  - **bunnc_s**: `+`
  - **bunct_s**: `+`
  - **bunmt_s**: `+`
  - **tintcch_s**: `+`
  - **ptu_s**: `n/a`
  - **bmact_s**: `+`
  - **bunnctu_s**: `n/a`
  - **buncttu_s**: `n/a`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **ptu01_s**: `n/a`
  - **bclmc_s**: `+`
  - **bec01_s**: `n/a`
  - **bec02_s**: `n/a`
  - **bec03_s**: `n/a`
  - **bec04_s**: `n/a`
  - **butmc01_s**: `n/a`
  - **butmc02_s**: `n/a`
  - **bedtu01_s**: `n/a`
  - **bedtu02_s**: `+`
  - **bsatu_s**: `+`
  - **bhltu_s**: `n/a`
  - **bhotu_s**: `n/a`
  - **bec05_s**: `+`

### 6. Function: DefIl
  - **name**: `ils_benmt`
  - **bho**: `+`
  - **bed**: `+`
  - **bcc00_s**: `+`
  - **bcctu_s**: `+`
  - **bsa_s**: `+`
  - **bfamt_s**: `n/a`
  - **bunnc_s**: `+`
  - **bunmt_s**: `+`
  - **bunot**: `+`
  - **buntr**: `+`
  - **bunnctu_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **bhotu_s**: `n/a`
  - **bsatu_s**: `+`
  - **bedtu01_s**: `n/a`
  - **bedtu02_s**: `+`
  - **butmc01_s**: `n/a`
  - **butmc02_s**: `n/a`
  - **ptu01_s**: `n/a`
  - **ptu_s**: `n/a`

### 7. Function: DefIl
  - **name**: `ils_bennt`
  - **bhl00**: `+`
  - **bac00**: `+`
  - **bdi**: `+`
  - **bunct_s**: `+`
  - **bma**: `+`
  - **bch00_s**: `+`
  - **tintcch_s**: `+`
  - **bacot**: `+`
  - **bhlot**: `+`
  - **bac01**: `+`
  - **buncm**: `+`
  - **bfaam**: `+`
  - **bmact_s**: `+`
  - **buncttu_s**: `n/a`
  - **bwkmcee_s**: `n/a`
  - **bclmc_s**: `n/a`
  - **bec01_s**: `n/a`
  - **bec02_s**: `n/a`
  - **bec03_s**: `n/a`
  - **bec04_s**: `n/a`
  - **bhltu_s**: `n/a`
  - **bec05_s**: `n/a`

### 8. Function: DefIl
  - **name**: `ils_ben`
  - **ils_pen**: `+`
  - **ils_benmt**: `+`
  - **ils_bennt**: `+`

### 9. Function: DefIl
  - **name**: `ils_taxsim`
  - **tin_s**: `+`
  - **tiniy_s**: `+`

### 10. Function: DefIl
  - **name**: `ils_tax`
  - **ils_taxin**: `+`
  - **ils_taxwl**: `+`

### 11. Function: DefIl
  - **name**: `ils_sicee`
  - **tsceehl01_s**: `+`
  - **tsceepi01_s**: `+`
  - **tsceeui02_s**: `+`
  - **tsceepi02_s**: `+`
  - **tsceehl02_s**: `+`
  - **tsceeot_s**: `+`
  - **tsceeho_s**: `+`
  - **tsceeui01_s**: `+`

### 12. Function: DefIl
  - **name**: `ils_sicse`
  - **tscseac_s**: `+`
  - **tscsepi_s**: `+`
  - **tscsehl00_s**: `+`
  - **tscsehlpf_s**: `+`
  - **tscseot_s**: `+`

### 13. Function: DefIl
  - **name**: `ils_sicer`
  - **tscerac_s**: `+`
  - **tscerhl_s**: `+`
  - **tscerpi_s**: `+`
  - **tscerui_s**: `+`
  - **tscerho_s**: `+`
  - **tscersf_s**: `+`
  - **tscerfa_s**: `+`
  - **tscerrg_s**: `+`

### 14. Function: DefIl
  - **name**: `ils_sicct`
  - **tsccthl_s**: `+`

### 15. Function: DefIl
  - **name**: `ils_dispy`
  - **ils_origy**: `+`
  - **ils_ben**: `+`
  - **ils_tax**: `-`
  - **ils_sicdy**: `-`

### 16. Function: DefIl
  - **Name**: `ils_b1_bfa`
  - **bfaam**: `+`
  - **tintcch_s**: `+`
  - **bch00_s**: `+`
  - **bfamt_s**: `n/a`
  - **ils_b1_bcb**: `+`
  - **bsatu_s**: `+`

### 17. Function: DefIl
  - **Name**: `ils_b1_bhl`
  - **bhlot**: `+`
  - **bacot**: `+`
  - **bhl00**: `+`
  - **bac00**: `+`
  - **bhltu_s**: `n/a`

### 18. Function: DefIl
  - **Name**: `ils_b1_bun`
  - **buntr**: `+`
  - **bunot**: `+`
  - **bunmt_s**: `+`
  - **bunnc_s**: `+`
  - **bunct_s**: `+`
  - **buncm**: `+`
  - **bunnctu_s**: `n/a`
  - **buncttu_s**: `n/a`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`

### 19. Function: DefIl
  - **Name**: `ils_b1_bdi`
  - **bdi**: `+`

### 20. Function: DefIl
  - **Name**: `ils_b1_bsu`
  - **psu**: `+`
  - **bac01**: `+`
  - **temp_ptu2**: `n/a`

### 21. Function: DefIl
  - **Name**: `ils_b1_boa`
  - **powpt**: `+`
  - **poaot**: `+`
  - **poa00**: `+`
  - **poacs**: `+`
  - **temp_ptu1**: `n/a`
  - **ptu_s**: `n/a`
  - **ptu01_s**: `n/a`

### 22. Function: DefIl
  - **Name**: `ils_b1_bed`
  - **bed**: `+`
  - **bedtu01_s**: `n/a`
  - **bedtu02_s**: `+`

### 23. Function: DefIl
  - **Name**: `ils_b1_bho`
  - **bho**: `+`
  - **bhotu_s**: `n/a`
  - **butmc01_s**: `n/a`
  - **butmc02_s**: `n/a`
  - **bec01_s**: `n/a`
  - **bec02_s**: `n/a`
  - **bec03_s**: `n/a`
  - **bec04_s**: `n/a`
  - **bclmc_s**: `n/a`
  - **bec05_s**: `n/a`

### 24. Function: DefIl
  - **Name**: `ils_b1_bsa`
  - **bsa_s**: `+`
  - **bsatu_s**: `n/a`

### 25. Function: DefIl
  - **Name**: `ils_base_tiniy`
  - **yiy**: `+`

### 26. Function: DefIl
  - **Name**: `ils_b2_penhl`
  - **ils_b1_boa**: `+`
  - **ils_b1_bsu**: `+`
  - **ils_b1_bhl**: `+`
  - **ils_b1_bdi**: `+`

### 27. Function: DefIl
  - **Name**: `ils_b2_bfaed`
  - **ils_b1_bfa**: `+`
  - **ils_b1_bed**: `+`

### 28. Function: DefIl
  - **name**: `ils_sicot`
  - **tscpepi02_s**: `+`
  - **tscpehl02_s**: `+`
  - **tscpepi01_s**: `+`
  - **tscpehl01_s**: `+`

### 29. Function: DefIl
  - **Name**: `ils_b2_bsaho`
  - **ils_b1_bsa**: `+`
  - **ils_b1_bho**: `+`

### 30. Function: DefIl
  - **Name**: `ils_base_tin01`
  - **yem**: `+`
  - **yse**: `+`
  - **ypr**: `+`
  - **ypp02**: `+`
  - **ypp01**: `+`
  - **bhl00**: `+`
  - **ils_pen**: `+`
  - **pxpot**: `-`
  - **bhlxp**: `-`
  - **pxp00**: `-`
  - **yemxp**: `-`
  - **yemmc_s**: `n/a`

### 31. Function: DefIl
  - **Name**: `ils_base_temp_buncm`
  - **buncm**: `+`

### 32. Function: DefIl
  - **Name**: `ils_base_tin02`
  - **pxpot**: `+`
  - **bhlxp**: `+`
  - **pxp00**: `+`
  - **yemxp**: `+`

### 33. Function: DefIl
  - **name**: `ils_sicdy`
  - **ils_sicee**: `+`
  - **ils_sicot**: `+`
  - **ils_sicse**: `+`

### 34. Function: DefIl
  - **Name**: `ils_b1_bcb`
  - **bmact_s**: `+`
  - **bcctu_s**: `+`
  - **bma**: `+`
  - **bcc00_s**: `+`

### 35. Function: DefIl
  - **Name**: `ils_b1_bwk`

### 36. Function: DefIl
  - **Name**: `ils_b2_bunwk`
  - **ils_b1_bwk**: `+`
  - **ils_b1_bun**: `+`

### 37. Function: DefIl
  - **Name**: `ils_taxin`
  - **tin_s**: `+`
  - **tiniy_s**: `+`

### 38. Function: DefIl
  - **Name**: `ils_taxwl`
  - **tpr**: `+`


---

## Policy: bsa_at
### 1. Function: DefVar
  - **temp_hc**: `0`
  - **temp_hh**: `0`
  - **temp_std**: `0`
  - **TotalPensioner**: `0`
  - **Pensioner**: `0`
  - **TotalAdult**: `0`
  - **Adult**: `0`
  - **Young_edu_empl**: `0`
  - **TotalYoung_edu_empl**: `0`
  - **Young_not_edu_empl**: `0`
  - **TotalYoung_not_edu_empl**: `0`
  - **Young**: `0`
  - **TotalYoung**: `0`
  - **ChildRent**: `0`
  - **TotalChildRent**: `0`
  - **AdultRent**: `0`
  - **TotalAdultRent**: `0`

### 2. Function: BenCalc
  - **comp_cond**: `TotalAdultRent = 1 & TotalChildRent = 3`
  - **comp_perTU**: `$sa_a1c3 - temp_hh`
  - **output_var**: `temp_hc`
  - **TAX_UNIT**: `tu_household_at`
  - **UpLim**: `xhcrt - bho - temp_hh`
  - **LowLim**: `0`
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `TotalAdultRent >= 2 & TotalChildRent >= 10`
  - **Comp_perTU**: `$sa_a2c10 - temp_hh`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`

### 3. Function: DefConst
  **Constants Defined:**
  - `$bsa_rent_upLim1`: n/a
  - `$bsa_rent_upLim2`: n/a
  - `$bsa_rent_upLim3`: n/a
  - `$bsa_rent_upLim4`: n/a
  - `$bsa_child_amt`: 326.44#m
  - `$bsa_single_amt`: 1209.01#m
  - `$bsa_couple_amt`: 846.31#m
  - `$bsa_rentSingle_amt`: 302.25#m
  - `$bsa_rentCouple_amt`: 211.58#m
  - `$bsa_rentAdult3_amt`: n/a
  - `$bsa_rentRet_amt1`: 163.22#m
  - `$bsa_rentRet_amt3`: 81.61#m
  - `$bsa_rentRet_amt2`: 122.41#m
  - `$bsa_heat_amt`: n/a
  - `$bsa_rent_stsAmt`: n/a
  - `$bsa_Adult3_amt`: n/a
  - `$bsa_coupleRet_amt`: n/a
  - `$bsa_singleRet_amt`: n/a
  - `$sa_young_not_edu_empl`: 604.5#m
  - `$sa_young_edu_empl`: 906.76#m
  - `$sa_hhyoung_not_edu_empl
`: 151.13#m
  - `$sa_hhyoung_edu_empl`: 226.69#m
  - `$sa_a1c0`: 660.87#m
  - `$sa_a1c1`: 762.89#m
  - `$sa_a1c2`: 860.82#m
  - `$sa_a1c3`: 958.75#m
  - `$sa_a1c4`: 1056.68#m
  - `$sa_a1c5`: 1154.61#m
  - `$sa_a1c6`: 1252.55#m
  - `$sa_a1c7`: 1350.48#m
  - `$sa_a1c8`: 1448.41#m
  - `$sa_a1c9`: 1546.34#m
  - `$sa_a1c10`: 1644.27#m
  - `$sa_a2c0`: 880.67#m
  - `$sa_a2c1`: 977.37#m
  - `$sa_a2c2`: 1064.06#m
  - `$sa_a2c3`: 1150.76#m
  - `$sa_a2c4`: 1237.45#m
  - `$sa_a2c5`: 1324.15#m
  - `$sa_a2c6`: 1410.84#m
  - `$sa_a2c7`: 1497.54#m
  - `$sa_a2c8`: 1584.23#m
  - `$sa_a2c9`: 1670.93#m
  - `$sa_a2c10`: 1757.62#m
  - `$sa_chilld_suppl`: 54.41#m
  - `$sa_disability`: 217.62#m

### 4. Function: BenCalc
  - **comp_cond**: `(Adult = 1 & Pensioner = 0 & (TotalAdult#1 = 1)) |  (Young_edu_empl = 1 & Pensioner = 0 & (TotalYoung#1 = 1 & TotalAdult#1 = 0))`
  - **Comp_perTU**: `$sa_young_edu_empl*(14/12)`
  - **output_var**: `temp_std`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `(Adult = 1 & Pensioner = 1 & (TotalAdult#1 >= 2 | (TotalAdult#1 = 1 & TotalYoung#1 >= 1))) | (Young = 1 & Pensioner = 1 & (TotalYoung#1 >= 1 | (TotalYoung#1 = 1 & TotalAdult#1 >= 1)))`
  - **#_Level**: `tu_household_at`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(dgn=0 & dag>=61) | (dgn=1 & dag>=65) | (IsDisabled & dag>=18)`
  - **Tax Unit:** `tu_individual_at`

### 6. Function: ArithOp
  **Formula:** `Pensioner`
  **Output Variable:** `TotalPensioner`
  **Tax Unit:** `tu_household_at`

### 7. Function: BenCalc
  - **comp_cond**: `(Adult = 1 & Pensioner = 0 & (TotalAdult#1 = 1)) |  (Young_edu_empl = 1 & Pensioner = 0 & (TotalYoung#1 = 1 & TotalAdult#1 = 0))`
  - **Comp_perTU**: `$sa_hhyoung_edu_empl`
  - **output_var**: `temp_hh`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_Cond**: `(Young_edu_empl = 1 & Pensioner = 0 & ((TotalAdult#1 >= 1 & TotalYoung#1 >= 1) |  (TotalYoung#1 >= 2))) | (Young_not_edu_empl = 1 & Pensioner = 0 & (TotalYoung#1=1 & TotalAdult#1 = 0))`
  - **#_Level**: `tu_household_at`

### 8. Function: ArithOp
  **Formula:** `temp_std+temp_hc-il_bsa#1`
  **Output Variable:** `bsa_s`
  **Tax Unit:** `tu_household_at`

### 9. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag>24`
  - **Tax Unit:** `tu_individual_at`

### 10. Function: ArithOp
  **Formula:** `Adult`
  **Output Variable:** `TotalAdult`
  **Tax Unit:** `tu_household_at`

### 11. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **LowLim**: `n/a`

### 12. Function: Elig
  **Eligibility Check:**
  - **Condition:** `xhcrt>0 & xhcrt>(bho+temp_hh) & xhcrt>temp_hh`
  - **Tax Unit:** `tu_household_at`

### 13. Function: BenCalc
  - **comp_cond**: `xhcrt<(bho+temp_hh) & bho>0`
  - **Comp_perTU**: `temp_std`
  - **output_var**: `temp_std`
  - **TAX_UNIT**: `tu_household_at`
  - **Comp_Cond**: `bho=0`

### 14. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 15. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 16. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 17. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 18. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 19. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 20. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 21. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 22. Function: DefIl
  - **Name**: `il_bsa`
  - **ils_origy**: `+`
  - **yemxp**: `-`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **ils_pen**: `+`
  - **ils_sicdy**: `-`
  - **ils_tax**: `-`
  - **xmp**: `+`
  - **bac00**: `+`
  - **bac01**: `+`
  - **bacot**: `+`
  - **bunct_s**: `+`
  - **buntr**: `+`
  - **bunot**: `+`
  - **bunnc_s**: `+`
  - **bunmt_s**: `+`
  - **buncm**: `+`
  - **bhl00**: `+`
  - **bhlot**: `+`
  - **bma**: `+`
  - **bmact_s**: `+`
  - **bfaam**: `+`
  - **bcc00_s**: `+`
  - **bcctu_s**: `+`
  - **bed**: `+`
  - **bedtu02_s**: `+`
  - **bfamt_s **: `n/a`

### 23. Function: DefIl *(Switch: n/a)*
  - **Name**: `n/a`
  - **ils_origy**: `n/a`
  - **ils_pen**: `n/a`
  - **ils_bennt**: `n/a`
  - **bcc00_s**: `n/a`
  - **bcctu_s**: `n/a`
  - **bunnc_s**: `n/a`
  - **ils_sicdy**: `n/a`
  - **ils_tax**: `n/a`
  - **bdi**: `n/a`
  - **xmp**: `n/a`
  - **bch00_s**: `n/a`
  - **tintcch_s**: `n/a`
  - **bunot**: `n/a`
  - **buntr**: `n/a`

### 24. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(dag >= 18 & dag <= 24) & (les = 3 | les = 6)`
  - **Tax Unit:** `tu_individual_at`

### 25. Function: ArithOp
  **Formula:** `Young_edu_empl`
  **Output Variable:** `TotalYoung_edu_empl`
  **Tax Unit:** `tu_household_at`

### 26. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(dag >= 18 & dag <= 24) & (les != 3 & les != 6)`
  - **Tax Unit:** `tu_individual_at`

### 27. Function: ArithOp
  **Formula:** `Young_not_edu_empl`
  **Output Variable:** `TotalYoung_not_edu_empl`
  **Tax Unit:** `tu_household_at`

### 28. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(dag >= 18 & dag <= 24)`
  - **Tax Unit:** `tu_individual_at`

### 29. Function: ArithOp
  **Formula:** `Young`
  **Output Variable:** `TotalYoung`
  **Tax Unit:** `tu_household_at`

### 30. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag<18`
  - **Tax Unit:** `tu_individual_at`

### 31. Function: ArithOp
  **Formula:** `ChildRent`
  **Output Variable:** `TotalChildRent`
  **Tax Unit:** `tu_household_at`

### 32. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag>=18`
  - **Tax Unit:** `tu_individual_at`

### 33. Function: ArithOp
  **Formula:** `AdultRent`
  **Output Variable:** `TotalAdultRent`
  **Tax Unit:** `tu_household_at`

### 34. Function: BenCalc
  - **Comp_Cond**: `(Adult = 1 | Young = 1) & nDepChildrenInTu#1 >= 1`
  - **Comp_perTU**: `$sa_chilld_suppl`
  - **#_Level**: `tu_household_at`
  - **Output_Add_Var**: `temp_std`
  - **TAX_UNIT**: `tu_individual_at`

### 35. Function: BenCalc
  - **Comp_Cond**: `IsDisabled`
  - **Comp_perTU**: `$sa_disability`
  - **Output_Add_Var**: `temp_std`
  - **TAX_UNIT**: `tu_individual_at`

### 36. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `(i_bsa_cumpers > $bsa_target_count & bsayn_a = -1)  | bsayn_a = 0`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bsa_s`
  - **TAX_UNIT**: `tu_individual_at`

### 37. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsa_elig`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsa_sort`
  - **OutputVar**: `i_bsa_cumpers`
  - **TAX_UNIT**: `tu_individual_at`

### 38. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_target_count`: $sum_i_bsa_elig * $bsa_rate

### 39. Function: Totals *(Switch: off)*
  - **Agg**: `i_bsa_elig`
  - **Use_Weights**: `yes`
  - **Varname_Sum**: `$sum`
  - **TAX_UNIT**: `tu_individual_at`

### 40. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_rate`: min($bsa_BCA_rate,$bsa_BTA_rate)

### 41. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_BCA_rate`: 0.30733595

### 42. Function: Totals *(Switch: off)*
  - **Agg**: `n/a`
  - **Use_Weights**: `n/a`
  - **Varname_Sum**: `n/a`
  - **TAX_UNIT**: `n/a`

### 43. Function: DefVar *(Switch: off)*
  - **i_bsa_bca_take**: `n/a`

### 44. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `n/a`
  - **SummingWeighted**: `n/a`
  - **SortingVar**: `n/a`
  - **OutputVar**: `n/a`
  - **TAX_UNIT**: `n/a`

### 45. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_targetBCA_amt`: n/a

### 46. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `bsa_s >= $bsa_minamt`
  - **Comp_perTU**: `1`
  - **Comp_perElig**: `i_bsa_sort`
  - **Output_Var**: `i_bsa_sort`
  - **TAX_UNIT**: `tu_individual_at`

### 47. Function: DefVar *(Switch: off)*
  - **i_bsa_sort**: `i_bsa_rand`
  - **i_bsa_amt**: `bsa_s`
  - **i_bsa_elig**: `bsa_s > 0`
  - **i_bsa_cumexp**: `0`
  - **i_bsa_cumpers**: `0`

### 48. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_minamt`: 0

### 49. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_BTA_rate`: 0.67


---

## Policy: => pcstu_at

---

## Policy: ptu_at
### 1. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 2. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 3. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 5. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 6. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 7. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$ptu_lowlim`: n/a
  - `$ptu_bracket_lim1`: n/a
  - `$ptu_bracket_lim2`: n/a
  - `$ptu_bracket_lim3`: n/a
  - `$ptu_bracket_lim4`: n/a
  - `$ptu_rate1`: n/a
  - `$ptu_rate2`: n/a
  - `$ptu_bracket_amt1`: n/a
  - `$ptu_rate3`: n/a
  - `$ptu_amt2`: n/a

### 8. Function: DefVar *(Switch: n/a)*
  - **i_penbase**: `n/a`
  - **i_ptu_elig**: `n/a`

### 9. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 10. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 11. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **UpLim**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Elig_Var**: `n/a`


---

## Policy: IlsUDBDef_at
### 1. Function: DefIl
  - **Name**: `ils_udb_yem`
  - **yem**: `+`
  - **yot01**: `+`
  - **yemot**: `+`
  - **yemmc_s**: `n/a`

### 2. Function: DefIl
  - **Name**: `ils_udb_yse`
  - **yse**: `+`

### 3. Function: DefIl
  - **Name**: `ils_udb_ypp`
  - **ypp01**: `+`
  - **ypp02**: `+`

### 4. Function: DefIl
  - **Name**: `ils_udb_ypr`
  - **ypr**: `+`

### 5. Function: DefIl
  - **Name**: `ils_udb_yiy`
  - **yiy**: `+`

### 6. Function: DefIl
  - **Name**: `ils_udb_ypt`
  - **ypt**: `+`

### 7. Function: DefIl
  - **Name**: `ils_udb_yot`
  - **yot02**: `+`

### 8. Function: DefIl
  - **Name**: `ils_udb_xmp`
  - **xmp**: `+`

### 9. Function: DefIl
  - **Name**: `ils_udb_kfbcc`
  - **kfbcc**: `+`

### 10. Function: DefIl
  - **Name**: `ils_udb_tpr`
  - **tpr**: `+`

### 11. Function: DefIl
  - **Name**: `ils_udb_tis`
  - **tin_s**: `+`
  - **ils_sicdy**: `+`
  - **tiniy_s**: `+`

### 12. Function: DefIl
  - **Name**: `ils_udb_boa`
  - **powpt**: `+`
  - **poaot**: `+`
  - **temp_bdi**: `+`
  - **temp_bac**: `+`
  - **temp_poa**: `+`
  - **temp_ptu1**: `n/a`
  - **ptu_s**: `n/a`
  - **ptu01_s**: `n/a`

### 13. Function: DefIl
  - **Name**: `ils_udb_bsu`
  - **psu**: `+`
  - **bac01**: `+`
  - **temp_ptu2**: `n/a`

### 14. Function: DefIl
  - **Name**: `ils_udb_bdi`
  - **temp_bac2**: `+`
  - **temp_bdi2**: `+`
  - **poadi**: `+`

### 15. Function: DefIl
  - **Name**: `ils_udb_bun`
  - **buntr**: `+`
  - **bunot**: `+`
  - **bunmt_s**: `+`
  - **bunnc_s**: `+`
  - **bunct_s**: `+`
  - **buncm**: `+`
  - **bunnctu_s**: `n/a`
  - **buncttu_s**: `n/a`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`

### 16. Function: DefIl
  - **Name**: `ils_udb_bhl`
  - **bhlot**: `+`
  - **bacot**: `+`
  - **bhl00**: `+`
  - **bhltu_s**: `n/a`

### 17. Function: DefIl
  - **Name**: `ils_udb_bfa`
  - **bfaam**: `+`
  - **tintcch_s**: `+`
  - **bch00_s**: `+`
  - **bma**: `+`
  - **bfamt_s**: `n/a`
  - **bccrd**: `n/a`
  - **bcctu_s**: `+`
  - **bcc00_s**: `+`
  - **bmact_s**: `+`
  - **bsatu_s**: `+`

### 18. Function: DefIl
  - **Name**: `ils_udb_bsa`
  - **bsa_s**: `+`
  - **bsatu_s**: `n/a`

### 19. Function: DefIl
  - **Name**: `ils_udb_bho`
  - **bho**: `+`
  - **bhotu_s**: `n/a`
  - **butmc01_s**: `n/a`
  - **butmc02_s**: `n/a`
  - **bec01_s**: `n/a`
  - **bec02_s**: `n/a`
  - **bec03_s**: `n/a`
  - **bec04_s**: `n/a`
  - **bclmc_s**: `n/a`
  - **bec05_s**: `n/a`

### 20. Function: DefIl
  - **Name**: `ils_udb_bed`
  - **bed**: `+`
  - **bedtu01_s**: `n/a`
  - **bedtu02_s**: `+`

### 21. Function: DefIl
  - **Name**: `ils_udb_yds`
  - **ils_udb_yem**: `+`
  - **ils_udb_tis**: `-`
  - **ils_udb_tpr**: `-`
  - **ils_udb_bed**: `+`
  - **ils_udb_bho**: `+`
  - **ils_udb_bsa**: `+`
  - **ils_udb_bfa**: `+`
  - **ils_udb_bhl**: `+`
  - **ils_udb_bun**: `+`
  - **ils_udb_bdi**: `+`
  - **ils_udb_bsu**: `+`
  - **ils_udb_boa**: `+`
  - **ils_udb_kfbcc**: `+`
  - **ils_udb_xmp**: `-`
  - **ils_udb_yot**: `+`
  - **ils_udb_ypt**: `+`
  - **ils_udb_yiy**: `+`
  - **ils_udb_ypr**: `+`
  - **ils_udb_ypp**: `+`
  - **ils_udb_yse**: `+`

### 22. Function: DefVar
  - **temp_bac**: `0`
  - **temp_bdi**: `0`
  - **temp_bac2**: `0`
  - **temp_bdi2**: `0`
  - **temp_poa**: `0`

### 23. Function: BenCalc
  - **Comp_Cond**: `(dgn=0&dag>=61)|(dgn=1&dag>=65)`
  - **Comp_perElig**: `bac00`
  - **Output_Var**: `temp_bac`
  - **TAX_UNIT**: `tu_individual_at`

### 24. Function: BenCalc
  - **Comp_Cond**: `(dgn=0&dag>=61)|(dgn=1&dag>=65)`
  - **Comp_perElig**: `bdi`
  - **Output_Var**: `temp_bdi`
  - **TAX_UNIT**: `tu_individual_at`

### 25. Function: BenCalc
  - **Comp_Cond**: `(dgn=0&dag<61)|(dgn=1&dag<65)`
  - **Comp_perElig**: `bac00`
  - **Output_Var**: `temp_bac2`
  - **TAX_UNIT**: `tu_individual_at`

### 26. Function: BenCalc
  - **Comp_Cond**: `(dgn=0&dag<61)|(dgn=1&dag<65)`
  - **Comp_perElig**: `bdi`
  - **Output_Var**: `temp_bdi2`
  - **TAX_UNIT**: `tu_individual_at`

### 27. Function: ArithOp
  **Formula:** `poa00+poacs-poadi`
  **Output Variable:** `temp_poa`
  **Tax Unit:** `tu_individual_at`


---

## Policy: bmact_at *(Switch: switch)*
### 1. Function: DefVar
  - **i_elparent_bmact**: `0`
  - **Var_Monetary**: `yes`
  - **i_elchild_bmact**: `0`
  - **i_ageweeks_bmact**: `0`
  - **i_nelchildren_bmact**: `0`
  - **i_durweeks_bmact**: `0`
  - **i_yempv_bmact**: `0`

### 2. Function: DefTu
  - **Type**: `SUBGROUP`
  - **Name**: `tu_bmact_at`
  - **Members**: `Partner & OwnDepChild & LooseDepChild`
  - **PartnerCond**: `Default`
  - **DepChildCond**: `Default & dag <1`
  - **ExtHeadCond**: `nDepChOfCouple > 0 & dgn = 0`
  - **StopIfNoHeadFound**: `no`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dgn = 0 & IsParentOfDepChild#1`
  - **Tax Unit:** `tu_individual_at`

### 4. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bmact=1 & (yem > 0 | bunct_s > 0 | yse>0) & liwmy/12 >= 1/4`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_elparent_bmact`
  - **TAX_UNIT**: `tu_individual_at`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsDepChild#1`
  - **Tax Unit:** `tu_individual_at`

### 6. Function: ArithOp
  **Formula:** `nDepChildrenInTu#1`
  **Output Variable:** `i_nelchildren_bmact`
  **Tax Unit:** `tu_individual_at`

### 7. Function: BenCalc
  - **Comp_Cond**: `i_elchild_bmact=1`
  - **Comp_perTU**: `(12-dmb)*(30.5/7)`
  - **Output_Var**: `i_ageweeks_bmact`
  - **TAX_UNIT**: `tu_individual_at`

### 8. Function: BenCalc
  - **Comp_Cond**: `i_nelchildren_bmact>0`
  - **Comp_perTU**: `i_durweeks_bmact/i_nelchildren_bmact`
  - **Output_Var**: `i_durweeks_bmact`
  - **TAX_UNIT**: `tu_bmact_at`

### 9. Function: BenCalc
  - **Comp_Cond**: `(yivwg > 0 | yem > 0) & ils_base_tin01=0`
  - **Comp_perTU**: `max((yivwg*($lhw*52/12)),((yem-yemxp) - ils_sicee))`
  - **Output_Var**: `i_yempv_bmact`
  - **TAX_UNIT**: `tu_individual_at`

### 10. Function: BenCalc
  - **Comp_Cond**: `yse>0 & tscsehl_s>0 & yem=0`
  - **Comp_perTU**: `Amount#1 * ( i_durweeks_bmact*7)`
  - **Output_Var**: `bmact_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **#_Amount**: `70.28`

### 11. Function: ArithOp
  **Formula:** `bmact_s/12`
  **Output Variable:** `bmact_s`
  **Tax Unit:** `tu_individual_at`

### 12. Function: BenCalc
  - **Comp_Cond**: `i_elchild_bmact=1 & i_ageweeks_bmact>=0 & i_nelchildren_bmact#1>1`
  - **Comp_perTU**: `8+i_ageweeks_bmact`
  - **Output_Add_Var**: `i_durweeks_bmact`
  - **TAX_UNIT**: `tu_individual_at`
  - **Comp_UpLim**: `20`
  - **Comp_LowLim**: `0`
  - **#_Level**: `tu_bmact_at`

### 13. Function: BenCalc
  - **Comp_Cond**: `yem = 0 & lcb_a=1`
  - **Comp_perTU**: `i_yempv_bmact`
  - **Output_Var**: `i_yempv_bmact`
  - **TAX_UNIT**: `tu_individual_at`


---

## Policy: None *(Switch: switch)*

---

## Policy: TransLMA_at *(Switch: off)*
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy=0)  &  (ysemy=0) & (dag>17)  &  ((dag<$PensionAgeMale & dgn=1) | (dag<$PensionAgeFemale & dgn=0)) & (les=5)`
  - **Tax Unit:** `tu_individual_at`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy > 0) & (lcs = 0) `
  - **Tax Unit:** `tu_individual_at`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ysemy > 0) & (yemmy = 0)`
  - **Tax Unit:** `tu_individual_at`

### 4. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(dgn = 1) & (i_lma_rand_2 < $er_dgn1_se)`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_at`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lma=1)`
  - **Tax Unit:** `tu_individual_at`

### 6. Function: ArithOp
  **Formula:** `(yivwg*$lhw*52/12)`
  **Output Variable:** `yem_a`
  **Tax Unit:** `tu_individual_at`

### 7. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lma=1)|(lma=5)`
  - **Tax Unit:** `tu_individual_at`

### 8. Function: ArithOp
  **Formula:** `$lhw`
  **Output Variable:** `lhw_a`
  **Tax Unit:** `tu_individual_at`

### 9. Function: ArithOp
  **Formula:** `ysemy - bwkmcsemy_s`
  **Output Variable:** `ysemwmy_s`
  **Tax Unit:** `tu_individual_at`

### 10. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(ysemy <= $mc_my_se & i_mc_rand_2 > $mc_my_se/12)`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bwkmcsemy_s`
  - **TAX_UNIT**: `tu_individual_at`

### 11. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lmcse_s = 1)`
  - **Tax Unit:** `tu_individual_at`

### 12. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_se < $yseadj_sh)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lmcse_s`
  - **TAX_UNIT**: `tu_individual_at`

### 13. Function: Elig
  **Eligibility Check:**
  - **Condition:** `ysemy>= $mc_my_se & les01=2 & lma=0`
  - **Tax Unit:** `tu_individual_at`

### 14. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_3 >$sh_15hours_ee & i_mc_rand_3<= $sh_45hours_ee)`
  - **Comp_perTU**: `0.45`
  - **Output_Var**: `lhwsr_s`
  - **TAX_UNIT**: `tu_individual_at`

### 15. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(bwkmceemy_s > 0)`
  - **Tax Unit:** `tu_individual_at`

### 16. Function: ArithOp
  **Formula:** `yemmy -bwkmceemy_s`
  **Output Variable:** `yemmwmy_s`
  **Tax Unit:** `tu_individual_at`

### 17. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lmcee_s = 1`
  - **Tax Unit:** `tu_individual_at`

### 18. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy >0)  & (lma=0)`
  - **Tax Unit:** `tu_individual_at`

### 19. Function: DefConst
  **Constants Defined:**
  - `$er_dgn0_deh1_ee`: 0
  - `$er_dgn0_deh2_ee`: 0
  - `$er_dgn0_deh3_ee`: 0
  - `$er_dgn1_deh1_ee`: 0
  - `$er_dgn1_deh2_ee`: 0
  - `$er_dgn1_deh3_ee`: 0
  - `$ur_dgn0_deh1_ee`: 0
  - `$ur_dgn0_deh2_ee`: 0
  - `$ur_dgn0_deh3_ee`: 0
  - `$ur_dgn1_deh1_ee`: 0
  - `$ur_dgn1_deh2_ee`: 0
  - `$ur_dgn1_deh3_ee`: 0
  - `$er_dgn0_se`: 0
  - `$er_dgn1_se`: 0
  - `$er_yemmy2`: 0
  - `$er_yemmy5`: 0
  - `$er_yemmy8`: 0
  - `$ur_yemmy2`: 0
  - `$ur_yemmy5`: 0
  - `$ur_yemmy8`: 0
  - `Run_Cond`: n/a

### 20. Function: DefConst
  **Constants Defined:**
  - `$sh_mcee_l1_dgn0`: 0
  - `$sh_mcee_l2_dgn0`: 0
  - `$sh_mcee_l3_dgn0`: 0
  - `$sh_mcee_l4_dgn0`: 0
  - `$sh_mcee_l5_dgn0`: 0
  - `$sh_mcee_l1_dgn1`: 0
  - `$sh_mcee_l2_dgn1`: 0
  - `$sh_mcee_l3_dgn1`: 0
  - `$sh_mcee_l4_dgn1`: 0
  - `$sh_mcee_l5_dgn1`: 0
  - `$sh_mceemy_1`: 0
  - `$sh_mceemy_2`: 0
  - `$sh_mceemy_3`: 0
  - `$sh_mceemy_4`: 0
  - `$sh_mceemy_5`: 0
  - `$sh_mceemy_6`: 0
  - `$sh_mceemy_7`: 0
  - `$sh_mceemy_8`: 0
  - `$sh_mceemy_9`: 0
  - `$sh_0hours_ee`: 0
  - `$sh_15hours_ee`: 0
  - `$sh_45hours_ee`: 0
  - `Run_Cond`: GetDataIncomeYear = 2019
  - `$yseadj_sh`: 0
  - `$mc_my_se`: 0

### 21. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(deh = 5) & (dgn = 1) & (i_lma_rand_1 < $ur_dgn1_deh3_ee)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lma`
  - **TAX_UNIT**: `tu_household_at`

### 22. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(deh = 5) & (dgn = 1) & (i_lma_rand_1 < $er_dgn1_deh3_ee)`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_at`

### 23. Function: BenCalc
  - **Comp_Cond**: `(lma=2) & (ysemy > 0) & (yemmy = 0)`
  - **Comp_perTU**: `0`
  - **Output_Var**: `yemmy_a`
  - **TAX_UNIT**: `tu_individual_at`

### 24. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(lindi = 5) & (dgn = 1) & (i_mc_rand_1 < $sh_mcee_l4_dgn1)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lmcee_s`
  - **TAX_UNIT**: `tu_individual_at`

### 25. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_2> $sh_mceemy_9)`
  - **Comp_perTU**: `min (10, yemmy)`
  - **Output_Var**: `bwkmceemy_s`
  - **TAX_UNIT**: `tu_individual_at`

### 26. Function: DefConst
  **Constants Defined:**
  - `$er_dgn0_deh1_ee`: 0
  - `$er_dgn0_deh2_ee`: 0
  - `$er_dgn0_deh3_ee`: 0
  - `$er_dgn1_deh1_ee`: 0
  - `$er_dgn1_deh2_ee`: 0
  - `$er_dgn1_deh3_ee`: 0
  - `$ur_dgn0_deh1_ee`: 0
  - `$ur_dgn0_deh2_ee`: 0
  - `$ur_dgn0_deh3_ee`: 0
  - `$ur_dgn1_deh1_ee`: 0
  - `$ur_dgn1_deh2_ee`: 0
  - `$ur_dgn1_deh3_ee`: 0
  - `$er_dgn0_se`: 0
  - `$er_dgn1_se`: 0
  - `$er_yemmy2`: 0
  - `$er_yemmy5`: 0
  - `$er_yemmy8`: 0
  - `$ur_yemmy2`: 0
  - `$ur_yemmy5`: 0
  - `$ur_yemmy8`: 0
  - `Run_Cond`: GetDataIncomeYear != 2019

### 27. Function: DefConst
  **Constants Defined:**
  - `$sh_mcee_l1_dgn0`: 0
  - `$sh_mcee_l2_dgn0`: 0
  - `$sh_mcee_l3_dgn0`: 0
  - `$sh_mcee_l4_dgn0`: 0
  - `$sh_mcee_l5_dgn0`: 0
  - `$sh_mcee_l1_dgn1`: 0
  - `$sh_mcee_l2_dgn1`: 0
  - `$sh_mcee_l3_dgn1`: 0
  - `$sh_mcee_l4_dgn1`: 0
  - `$sh_mcee_l5_dgn1`: 0
  - `$sh_mceemy_1`: 0
  - `$sh_mceemy_2`: 0
  - `$sh_mceemy_3`: 0
  - `$sh_mceemy_4`: 0
  - `$sh_mceemy_5`: 0
  - `$sh_mceemy_6`: 0
  - `$sh_mceemy_7`: 0
  - `$sh_mceemy_8`: 0
  - `$sh_mceemy_9`: 0
  - `$sh_0hours_ee`: 0
  - `$sh_15hours_ee`: 0
  - `$sh_45hours_ee`: 0
  - `Run_Cond`: GetDataIncomeYear != 2019
  - `$yseadj_sh`: 0
  - `$mc_my_se`: 0


---

## Policy: ysecomp_at
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lmcse_s=1`
  - **Tax Unit:** `tu_individual_at`

### 2. Function: ArithOp *(Switch: n/a)*
  **Formula:** `1000#m * bwkmcsemy_s/12`
  **Output Variable:** `bwkmcse_s`
  **Tax Unit:** `tu_individual_at`


---

## Policy: yemcomp_at
### 1. Function: DefVar
  - **i_yem_orig**: `yem`
  - **Var_Monetary**: `yes`
  - **i_netincome**: `0`
  - **i_bwkmcee_s**: `0`
  - **i_yemmc_s**: `0`

### 2. Function: ArithOp
  **Formula:** `il_taxableY - ypr -yse - (ils_pen - pxp00) - ypp02 - ypp01- ils_tax + tin02_s`
  **Output Variable:** `i_netincome`
  **Tax Unit:** `tu_individual_at`

### 3. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `i_netincome*(1-lhwsr_s)*(($mc_rrate2-lhwsr_s)/(1-lhwsr_s))`
  - **Comp_perTU**: `i_netincome*(1-lhwsr_s)*(($mc_rrate3-lhwsr_s)/(1-lhwsr_s))`
  - **Output_Var**: `i_bwkmcee_s`
  - **TAX_UNIT**: `tu_individual_at`
  - **UpLim**: `3346.91#m*(1-lhwsr_s)*(($mc_rrate3-lhwsr_s)/(1-lhwsr_s))`

### 4. Function: ArithOp
  **Formula:** `i_bwkmcee_s*bwkmceemy_s/12`
  **Output Variable:** `bwkmcee_s`
  **Tax Unit:** `tu_individual_at`

### 5. Function: ArithOp
  **Formula:** `i_yemmc_s * bwkmceemy_s/12`
  **Output Variable:** `yemmc_s`
  **Tax Unit:** `tu_individual_at`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bwkmceemy_s > 0 & lhwsr_s != 0 & (yem-yemxp) > $tsc_minThres1`
  - **Tax Unit:** `tu_individual_at`

### 7. Function: DefConst
  **Constants Defined:**
  - `$mc_rrate1`: 0.928
  - `$mc_rrate2`: 0.9265
  - `$mc_rrate3`: 0.9

### 8. Function: ArithOp
  **Formula:** `i_netincome * lhwsr_s`
  **Output Variable:** `i_yemmc_s`
  **Tax Unit:** `tu_individual_at`


---

## Policy: None

---

## Policy: None

---

## Policy: tco_at *(Switch: off)*
### 1. Function: DefConst
  **Constants Defined:**
  - `$tco_v_02111`: $tco_base_v_02111
  - `$tco_v_02121`: $tco_base_v_02121
  - `$tco_v_02122`: $tco_base_v_02122
  - `$tco_v_02131`: $tco_base_v_02131
  - `$tco_v_02211`: $tco_base_v_02211
  - `$tco_v_02212`: $tco_base_v_02212
  - `$tco_v_02213a`: $tco_base_v_02213a
  - `$tco_v_04511`: $tco_base_v_04511
  - `$tco_v_04521`: $tco_base_v_04521
  - `$tco_v_04531`: $tco_base_v_04531
  - `$tco_v_04541`: $tco_base_v_04541
  - `$tco_v_04542`: $tco_base_v_04542
  - `$tco_v_07221`: $tco_base_v_07221
  - `$tco_v_02213b`: $tco_base_v_02213b
  - `$tco_v_07222`: $tco_base_v_07222
  - `$tco_v_02142`: $tco_base_v_02142
  - `$tco_v_02141`: $tco_base_v_02141

### 2. Function: DefConst
  **Constants Defined:**
  - `$tco_v_02213`: ($tco_v_02213a + $tco_v_02213b)/2
  - `$tco_a_04531`: 1.00*(($tco_a_04531a1+$tco_a_04531a2)/2) + 0.00*$tco_a_04531b + 0.00*$tco_a_04531c
  - `$tco_a_07221`: 0.0*(($tco_a_07221a +  $tco_a_07221b)/2) + 1.0*(($tco_a_07221c +  $tco_a_07221d)/2)
  - `$tco_a_07222`: ($tco_a_07222a +  $tco_a_07222b)/2
  - `$tco_a_02122`: 0.5*$tco_a_02122a + 0.5*($tco_a_02122b1 +  $tco_a_02122b2)/2
  - `$tco_a_02213`: $tco_a_02213a

### 3. Function: DefConst
  **Constants Defined:**
  - `$tco_base_q_04531`: 1.00*$tco_base_q_04531a + 0.00*$tco_base_q_04531b + 0.00*$tco_base_q_04531c
  - `$tco_base_q_02131`: ($tco_base_q_02131t)* 100 / 12
  - `$tco_base_q_02122`: (($tco_base_q_02122t1+$tco_base_q_02122t2)/2)* 100
  - `$tco_base_q_02121`: (0.9*$tco_base_q_02121t1+0.1*$tco_base_q_02121t2) * 100
  - `$tco_base_q_02111`: ($tco_base_q_02111t) / 40% * 100
  - `$tco_base_a_07221`: 0.00*(($tco_base_a_07221a + $tco_base_a_07221b)/2) +1.0*(($tco_base_a_07221c + $tco_base_a_07221d)/2)
  - `$tco_base_a_04531`: 1.00*(($tco_base_a_04531a1+$tco_base_a_04531a2)/2) + 0.00*$tco_base_a_04531b + 0.00*$tco_base_a_04531c
  - `$tco_base_v_02213`: ($tco_base_v_02213a + $tco_base_v_02213b)/2
  - `$tco_base_a_07222`: 0.50*$tco_base_a_07222a+ 0.50*$tco_base_a_07222b
  - `$tco_base_a_02122`: 0.5*$tco_base_a_02122a + 0.5*($tco_base_a_02122b1 +  $tco_base_a_02122b2)/2
  - `$tco_base_q_02142`: ($tco_base_q_02142t)* 100 / 12
  - `$tco_base_q_02141`: ($tco_base_q_02141t)* 100 / 12
  - `$tco_base_a_02213`: $tco_base_a_02213a

### 4. Function: DefIl
  - **Name**: `il_xs_exc`
  - **xs07221**: `+`
  - **xs04542**: `+`
  - **xs04541**: `+`
  - **xs04531**: `+`
  - **xs04521**: `+`
  - **xs04511**: `+`
  - **xs02213**: `+`
  - **xs02212**: `+`
  - **xs02211**: `+`
  - **xs02131**: `+`
  - **xs02122**: `+`
  - **xs02121**: `+`
  - **xs02111**: `+`
  - **Warn_If_NonMonetary**: `no`
  - **xs07222**: `+`
  - **xs02142**: `+`
  - **xs02141**: `+`

### 5. Function: DefConst
  **Constants Defined:**
  - `$tco_t_12714`: $tco_t_std
  - `$tco_t_12713`: $tco_t_zero
  - `$tco_t_12712`: $tco_t_zero
  - `$tco_t_12711`: $tco_t_std
  - `$tco_t_12621`: $tco_t_zero
  - `$tco_t_12551`: $tco_t_zero
  - `$tco_t_12542`: $tco_t_zero
  - `$tco_t_12541`: $tco_t_zero
  - `$tco_t_12531`: $tco_t_zero
  - `$tco_t_12521`: $tco_t_zero
  - `$tco_t_12421`: $tco_t_zero
  - `$tco_t_12411`: $tco_t_zero
  - `$tco_t_12324`: $tco_t_std
  - `$tco_t_12323`: $tco_t_std
  - `$tco_t_12322`: $tco_t_std
  - `$tco_t_12321`: $tco_t_std
  - `$tco_t_12312`: $tco_t_std
  - `$tco_t_12311`: $tco_t_std
  - `$tco_t_12139`: $tco_t_std
  - `$tco_t_12138`: $tco_t_std
  - `$tco_t_12137`: $tco_t_std
  - `$tco_t_12136`: $tco_t_std
  - `$tco_t_12135`: $tco_t_std
  - `$tco_t_12134`: $tco_t_std
  - `$tco_t_12133`: $tco_t_std
  - `$tco_t_12132`: $tco_t_std
  - `$tco_t_12131`: $tco_t_std
  - `$tco_t_12121`: $tco_t_std
  - `$tco_t_12113`: $tco_t_std
  - `$tco_t_12112`: $tco_t_std
  - `$tco_t_12111`: $tco_t_std
  - `$tco_t_11212`: $tco_t_red2
  - `$tco_t_11211`: $tco_t_red2
  - `$tco_t_11123`: $tco_t_red2
  - `$tco_t_11122`: $tco_t_red2
  - `$tco_t_11121`: $tco_t_red2
  - `$tco_t_11113`: $tco_t_red2
  - `$tco_t_11112`: $tco_t_red2
  - `$tco_t_11111`: $tco_t_red2
  - `$tco_t_10612`: $tco_t_zero
  - `$tco_t_10611`: $tco_t_zero
  - `$tco_t_10513`: $tco_t_zero
  - `$tco_t_10512`: $tco_t_zero
  - `$tco_t_10511`: $tco_t_zero
  - `$tco_t_10411`: $tco_t_zero
  - `$tco_t_10311`: $tco_t_zero
  - `$tco_t_10211`: $tco_t_zero
  - `$tco_t_10112`: $tco_t_zero
  - `$tco_t_10111`: $tco_t_zero
  - `$tco_t_09622`: $tco_t_std
  - `$tco_t_09621`: $tco_t_std
  - `$tco_t_09612`: $tco_t_std
  - `$tco_t_09611`: $tco_t_std
  - `$tco_t_09542`: $tco_t_std
  - `$tco_t_09541`: $tco_t_std
  - `$tco_t_09531`: $tco_t_red2
  - `$tco_t_09522`: $tco_t_red2
  - `$tco_t_09521`: $tco_t_red2
  - `$tco_t_09513`: $tco_t_red2
  - `$tco_t_09512`: $tco_t_red2
  - `$tco_t_09511`: $tco_t_red2
  - `$tco_t_09431`: $tco_t_zero
  - `$tco_t_09424`: $tco_t_std
  - `$tco_t_09423`: $tco_t_red2
  - `$tco_t_09422`: $tco_t_red1
  - `$tco_t_09421`: $tco_t_red1
  - `$tco_t_09412`: $tco_t_red1
  - `$tco_t_09411`: $tco_t_std
  - `$tco_t_09351`: $tco_t_std
  - `$tco_t_09343`: $tco_t_std
  - `$tco_t_09342`: $tco_t_std
  - `$tco_t_09341`: $tco_t_red1
  - `$tco_t_09332`: $tco_t_std
  - `$tco_t_09331`: $tco_t_red1
  - `$tco_t_09322`: $tco_t_std
  - `$tco_t_09321`: $tco_t_std
  - `$tco_t_09312`: $tco_t_std
  - `$tco_t_09311`: $tco_t_std
  - `$tco_t_09231`: $tco_t_std
  - `$tco_t_09222`: $tco_t_std
  - `$tco_t_09221`: $tco_t_std
  - `$tco_t_09212`: $tco_t_std
  - `$tco_t_09211`: $tco_t_std
  - `$tco_t_09151`: $tco_t_std
  - `$tco_t_09143`: $tco_t_std
  - `$tco_t_09142`: $tco_t_std
  - `$tco_t_09141`: $tco_t_std
  - `$tco_t_09136`: $tco_t_std
  - `$tco_t_09135`: $tco_t_std
  - `$tco_t_09134`: $tco_t_std
  - `$tco_t_09132`: $tco_t_std
  - `$tco_t_09131`: $tco_t_std
  - `$tco_t_09122`: $tco_t_std
  - `$tco_t_09121`: $tco_t_std
  - `$tco_t_09114`: $tco_t_std
  - `$tco_t_09113`: $tco_t_std
  - `$tco_t_09112`: $tco_t_std
  - `$tco_t_09111`: $tco_t_std
  - `$tco_t_08313`: $tco_t_std
  - `$tco_t_08312`: $tco_t_std
  - `$tco_t_08311`: $tco_t_std
  - `$tco_t_08211`: $tco_t_std
  - `$tco_t_08112`: $tco_t_zero
  - `$tco_t_08111`: $tco_t_zero
  - `$tco_t_07362`: $tco_t_std
  - `$tco_t_07361`: $tco_t_std
  - `$tco_t_07356`: $tco_t_red2
  - `$tco_t_07355`: $tco_t_red2
  - `$tco_t_07354`: $tco_t_red2
  - `$tco_t_07353`: $tco_t_red2
  - `$tco_t_07352`: $tco_t_red2
  - `$tco_t_07351`: $tco_t_red2
  - `$tco_t_07341`: $tco_t_red2
  - `$tco_t_07331`: $tco_t_zero
  - `$tco_t_07322`: $tco_t_red2
  - `$tco_t_07321`: $tco_t_red2
  - `$tco_t_07311`: $tco_t_red2
  - `$tco_t_07247`: $tco_t_std
  - `$tco_t_07246`: $tco_t_std
  - `$tco_t_07245`: $tco_t_zero
  - `$tco_t_07244`: $tco_t_std
  - `$tco_t_07243`: $tco_t_std
  - `$tco_t_07242`: $tco_t_std
  - `$tco_t_07241`: $tco_t_std
  - `$tco_t_07234`: $tco_t_std
  - `$tco_t_07233`: $tco_t_std
  - `$tco_t_07232`: $tco_t_std
  - `$tco_t_07231`: $tco_t_std
  - `$tco_t_07223`: $tco_t_std
  - `$tco_t_07222`: $tco_t_std
  - `$tco_t_07221`: $tco_t_std
  - `$tco_t_07213`: $tco_t_std
  - `$tco_t_07212`: $tco_t_std
  - `$tco_t_07211`: $tco_t_std
  - `$tco_t_07131`: $tco_t_std
  - `$tco_t_07122`: $tco_t_std
  - `$tco_t_07121`: $tco_t_std
  - `$tco_t_07113`: $tco_t_std
  - `$tco_t_07112`: $tco_t_std
  - `$tco_t_07111`: $tco_t_std
  - `$tco_t_06322`: $tco_t_zero
  - `$tco_t_06321`: $tco_t_zero
  - `$tco_t_06312`: $tco_t_zero
  - `$tco_t_06311`: $tco_t_zero
  - `$tco_t_06233`: $tco_t_zero
  - `$tco_t_06232`: $tco_t_zero
  - `$tco_t_06231`: $tco_t_zero
  - `$tco_t_06221`: $tco_t_zero
  - `$tco_t_06212`: $tco_t_zero
  - `$tco_t_06211`: $tco_t_zero
  - `$tco_t_06134`: $tco_t_std
  - `$tco_t_06133`: $tco_t_std
  - `$tco_t_06132`: $tco_t_std
  - `$tco_t_06131`: $tco_t_std
  - `$tco_t_06121`: $tco_t_red2
  - `$tco_t_06112`: $tco_t_std
  - `$tco_t_06111`: $tco_t_red2
  - `$tco_t_05622`: $tco_t_std
  - `$tco_t_05621`: $tco_t_std
  - `$tco_t_05612`: $tco_t_std
  - `$tco_t_05611`: $tco_t_std
  - `$tco_t_05522`: $tco_t_std
  - `$tco_t_05521`: $tco_t_std
  - `$tco_t_05512`: $tco_t_std
  - `$tco_t_05511`: $tco_t_std
  - `$tco_t_05412`: $tco_t_std
  - `$tco_t_05411`: $tco_t_std
  - `$tco_t_05331`: $tco_t_std
  - `$tco_t_05321`: $tco_t_std
  - `$tco_t_05316`: $tco_t_std
  - `$tco_t_05315`: $tco_t_std
  - `$tco_t_05314`: $tco_t_std
  - `$tco_t_05313`: $tco_t_std
  - `$tco_t_05312`: $tco_t_std
  - `$tco_t_05311`: $tco_t_std
  - `$tco_t_05213`: $tco_t_std
  - `$tco_t_05212`: $tco_t_std
  - `$tco_t_05211`: $tco_t_std
  - `$tco_t_05131`: $tco_t_std
  - `$tco_t_05121`: $tco_t_std
  - `$tco_t_05112`: $tco_t_std
  - `$tco_t_05111`: $tco_t_std
  - `$tco_t_04563`: $tco_t_std
  - `$tco_t_04562`: $tco_t_std
  - `$tco_t_04561`: $tco_t_std
  - `$tco_t_04551`: $tco_t_std
  - `$tco_t_04542`: $tco_t_std
  - `$tco_t_04541`: $tco_t_red1
  - `$tco_t_04531`: $tco_t_std
  - `$tco_t_04521`: $tco_t_std
  - `$tco_t_04511`: $tco_t_std
  - `$tco_t_04441`: $tco_t_red2
  - `$tco_t_04431`: $tco_t_zero
  - `$tco_t_04421`: $tco_t_red2
  - `$tco_t_04411`: $tco_t_red2
  - `$tco_t_04322`: $tco_t_std
  - `$tco_t_04321`: $tco_t_std
  - `$tco_t_04312`: $tco_t_std
  - `$tco_t_04311`: $tco_t_std
  - `$tco_t_04132`: $tco_t_std
  - `$tco_t_04131`: $tco_t_std
  - `$tco_t_04121`: $tco_t_red2
  - `$tco_t_04112`: $tco_t_red2
  - `$tco_t_04111`: $tco_t_red2
  - `$tco_t_03221`: $tco_t_red2
  - `$tco_t_03213`: $tco_t_std
  - `$tco_t_03212`: $tco_t_std
  - `$tco_t_03211`: $tco_t_std
  - `$tco_t_03143`: $tco_t_std
  - `$tco_t_03142`: $tco_t_red2
  - `$tco_t_03141`: $tco_t_std
  - `$tco_t_03133`: $tco_t_std
  - `$tco_t_03132`: $tco_t_std
  - `$tco_t_03131`: $tco_t_std
  - `$tco_t_03123`: $tco_t_std
  - `$tco_t_03122`: $tco_t_std
  - `$tco_t_03121`: $tco_t_std
  - `$tco_t_03111`: $tco_t_std
  - `$tco_t_02213`: $tco_t_std
  - `$tco_t_02212`: $tco_t_std
  - `$tco_t_02211`: $tco_t_std
  - `$tco_t_02142`: $tco_t_std
  - `$tco_t_02141`: $tco_t_std
  - `$tco_t_02131`: $tco_t_std
  - `$tco_t_02122`: $tco_t_std
  - `$tco_t_02121`: $tco_t_std
  - `$tco_t_02111`: $tco_t_std
  - `$tco_t_01232`: $tco_t_std
  - `$tco_t_01231`: $tco_t_std
  - `$tco_t_01224`: $tco_t_std
  - `$tco_t_01223`: $tco_t_std
  - `$tco_t_01222`: $tco_t_std
  - `$tco_t_01221`: $tco_t_std
  - `$tco_t_01213`: $tco_t_red2
  - `$tco_t_01212`: $tco_t_std
  - `$tco_t_01211`: $tco_t_std
  - `$tco_t_01194`: $tco_t_red2
  - `$tco_t_01193`: $tco_t_red2
  - `$tco_t_01192`: $tco_t_red2
  - `$tco_t_01191`: $tco_t_red2
  - `$tco_t_01186`: $tco_t_red2
  - `$tco_t_01185`: $tco_t_red2
  - `$tco_t_01184`: $tco_t_red2
  - `$tco_t_01183`: $tco_t_red2
  - `$tco_t_01182`: $tco_t_red2
  - `$tco_t_01181`: $tco_t_red2
  - `$tco_t_01177`: $tco_t_red2
  - `$tco_t_01176`: $tco_t_red2
  - `$tco_t_01175`: $tco_t_red2
  - `$tco_t_01174`: $tco_t_red2
  - `$tco_t_01173`: $tco_t_red2
  - `$tco_t_01172`: $tco_t_red2
  - `$tco_t_01171`: $tco_t_red2
  - `$tco_t_01168`: $tco_t_red2
  - `$tco_t_01167`: $tco_t_red2
  - `$tco_t_01166`: $tco_t_red2
  - `$tco_t_01165`: $tco_t_red2
  - `$tco_t_01164`: $tco_t_red2
  - `$tco_t_01163`: $tco_t_red2
  - `$tco_t_01162`: $tco_t_red2
  - `$tco_t_01161`: $tco_t_red2
  - `$tco_t_01155`: $tco_t_red2
  - `$tco_t_01154`: $tco_t_red2
  - `$tco_t_01153`: $tco_t_red2
  - `$tco_t_01152`: $tco_t_red2
  - `$tco_t_01151`: $tco_t_red2
  - `$tco_t_01147`: $tco_t_red2
  - `$tco_t_01146`: $tco_t_red2
  - `$tco_t_01145`: $tco_t_red2
  - `$tco_t_01144`: $tco_t_red2
  - `$tco_t_01143`: $tco_t_red2
  - `$tco_t_01141`: $tco_t_red2
  - `$tco_t_01134`: $tco_t_red2
  - `$tco_t_01133`: $tco_t_red2
  - `$tco_t_01132`: $tco_t_red2
  - `$tco_t_01131`: $tco_t_red2
  - `$tco_t_01129`: $tco_t_red2
  - `$tco_t_01128`: $tco_t_red2
  - `$tco_t_01127`: $tco_t_red2
  - `$tco_t_01126`: $tco_t_red2
  - `$tco_t_01125`: $tco_t_red2
  - `$tco_t_01124`: $tco_t_red2
  - `$tco_t_01123`: $tco_t_red2
  - `$tco_t_01122`: $tco_t_red2
  - `$tco_t_01121`: $tco_t_red2
  - `$tco_t_01116`: $tco_t_red2
  - `$tco_t_01115`: $tco_t_red2
  - `$tco_t_01114`: $tco_t_red2
  - `$tco_t_01113`: $tco_t_red2
  - `$tco_t_01112`: $tco_t_red2
  - `$tco_t_01111`: $tco_t_red2
  - `Run_Cond`: GetDataCOICOPVersion = 2003

### 6. Function: DefConst
  **Constants Defined:**
  - `$theta_01111`: $tco_theta0
  - `$theta_12714`: $tco_theta0
  - `$theta_12713`: $tco_theta0
  - `$theta_12712`: $tco_theta0
  - `$theta_12711`: $tco_theta0
  - `$theta_12621`: $tco_theta0
  - `$theta_12551`: $tco_theta0
  - `$theta_12542`: $tco_theta0
  - `$theta_12541`: $tco_theta0
  - `$theta_12531`: $tco_theta0
  - `$theta_12521`: $tco_theta0
  - `$theta_12421`: $tco_theta0
  - `$theta_12411`: $tco_theta0
  - `$theta_12324`: $tco_theta0
  - `$theta_12323`: $tco_theta0
  - `$theta_12322`: $tco_theta0
  - `$theta_12321`: $tco_theta0
  - `$theta_12312`: $tco_theta0
  - `$theta_12311`: $tco_theta0
  - `$theta_12139`: $tco_theta0
  - `$theta_12138`: $tco_theta0
  - `$theta_12137`: $tco_theta0
  - `$theta_12136`: $tco_theta0
  - `$theta_12135`: $tco_theta0
  - `$theta_12134`: $tco_theta0
  - `$theta_12133`: $tco_theta0
  - `$theta_12132`: $tco_theta0
  - `$theta_12131`: $tco_theta0
  - `$theta_12121`: $tco_theta0
  - `$theta_12113`: $tco_theta0
  - `$theta_12112`: $tco_theta0
  - `$theta_12111`: $tco_theta0
  - `$theta_11212`: $tco_theta0
  - `$theta_11211`: $tco_theta0
  - `$theta_11123`: $tco_theta0
  - `$theta_11122`: $tco_theta0
  - `$theta_11121`: $tco_theta0
  - `$theta_11113`: $tco_theta0
  - `$theta_11112`: $tco_theta0
  - `$theta_11111`: $tco_theta0
  - `$theta_10612`: $tco_theta0
  - `$theta_10611`: $tco_theta0
  - `$theta_10513`: $tco_theta0
  - `$theta_10512`: $tco_theta0
  - `$theta_10511`: $tco_theta0
  - `$theta_10411`: $tco_theta0
  - `$theta_10311`: $tco_theta0
  - `$theta_10211`: $tco_theta0
  - `$theta_10112`: $tco_theta0
  - `$theta_10111`: $tco_theta0
  - `$theta_09622`: $tco_theta0
  - `$theta_09621`: $tco_theta0
  - `$theta_09612`: $tco_theta0
  - `$theta_09611`: $tco_theta0
  - `$theta_09542`: $tco_theta0
  - `$theta_09541`: $tco_theta0
  - `$theta_09531`: $tco_theta0
  - `$theta_09522`: $tco_theta0
  - `$theta_09521`: $tco_theta0
  - `$theta_09513`: $tco_theta0
  - `$theta_09512`: $tco_theta0
  - `$theta_09511`: $tco_theta0
  - `$theta_09431`: $tco_theta0
  - `$theta_09424`: $tco_theta0
  - `$theta_09423`: $tco_theta0
  - `$theta_09422`: $tco_theta0
  - `$theta_09421`: $tco_theta0
  - `$theta_09412`: $tco_theta0
  - `$theta_09411`: $tco_theta0
  - `$theta_09351`: $tco_theta0
  - `$theta_09343`: $tco_theta0
  - `$theta_09342`: $tco_theta0
  - `$theta_09341`: $tco_theta0
  - `$theta_09332`: $tco_theta0
  - `$theta_09331`: $tco_theta0
  - `$theta_09322`: $tco_theta0
  - `$theta_09321`: $tco_theta0
  - `$theta_09312`: $tco_theta0
  - `$theta_09311`: $tco_theta0
  - `$theta_09231`: $tco_theta0
  - `$theta_09222`: $tco_theta0
  - `$theta_09221`: $tco_theta0
  - `$theta_09212`: $tco_theta0
  - `$theta_09211`: $tco_theta0
  - `$theta_09151`: $tco_theta0
  - `$theta_09143`: $tco_theta0
  - `$theta_09142`: $tco_theta0
  - `$theta_09141`: $tco_theta0
  - `$theta_09136`: $tco_theta0
  - `$theta_09135`: $tco_theta0
  - `$theta_09134`: $tco_theta0
  - `$theta_09132`: $tco_theta0
  - `$theta_09131`: $tco_theta0
  - `$theta_09122`: $tco_theta0
  - `$theta_09121`: $tco_theta0
  - `$theta_09114`: $tco_theta0
  - `$theta_09113`: $tco_theta0
  - `$theta_09112`: $tco_theta0
  - `$theta_09111`: $tco_theta0
  - `$theta_08313`: $tco_theta0
  - `$theta_08312`: $tco_theta0
  - `$theta_08311`: $tco_theta0
  - `$theta_08211`: $tco_theta0
  - `$theta_08112`: $tco_theta0
  - `$theta_08111`: $tco_theta0
  - `$theta_07362`: $tco_theta0
  - `$theta_07361`: $tco_theta0
  - `$theta_07356`: $tco_theta0
  - `$theta_07355`: $tco_theta0
  - `$theta_07354`: $tco_theta0
  - `$theta_07353`: $tco_theta0
  - `$theta_07352`: $tco_theta0
  - `$theta_07351`: $tco_theta0
  - `$theta_07341`: $tco_theta0
  - `$theta_07331`: $tco_theta0
  - `$theta_07322`: $tco_theta0
  - `$theta_07321`: $tco_theta0
  - `$theta_07311`: $tco_theta0
  - `$theta_07247`: $tco_theta0
  - `$theta_07246`: $tco_theta0
  - `$theta_07245`: $tco_theta0
  - `$theta_07244`: $tco_theta0
  - `$theta_07243`: $tco_theta0
  - `$theta_07242`: $tco_theta0
  - `$theta_07241`: $tco_theta0
  - `$theta_07234`: $tco_theta0
  - `$theta_07233`: $tco_theta0
  - `$theta_07232`: $tco_theta0
  - `$theta_07231`: $tco_theta0
  - `$theta_07223`: $tco_theta0
  - `$theta_07222`: $tco_theta0
  - `$theta_07221`: $tco_theta0
  - `$theta_07213`: $tco_theta0
  - `$theta_07212`: $tco_theta0
  - `$theta_07211`: $tco_theta0
  - `$theta_07131`: $tco_theta0
  - `$theta_07122`: $tco_theta0
  - `$theta_07121`: $tco_theta0
  - `$theta_07113`: $tco_theta0
  - `$theta_07112`: $tco_theta0
  - `$theta_07111`: $tco_theta0
  - `$theta_06322`: $tco_theta0
  - `$theta_06321`: $tco_theta0
  - `$theta_06312`: $tco_theta0
  - `$theta_06311`: $tco_theta0
  - `$theta_06233`: $tco_theta0
  - `$theta_06232`: $tco_theta0
  - `$theta_06231`: $tco_theta0
  - `$theta_06221`: $tco_theta0
  - `$theta_06212`: $tco_theta0
  - `$theta_06211`: $tco_theta0
  - `$theta_06134`: $tco_theta0
  - `$theta_06133`: $tco_theta0
  - `$theta_06132`: $tco_theta0
  - `$theta_06131`: $tco_theta0
  - `$theta_06121`: $tco_theta0
  - `$theta_06112`: $tco_theta0
  - `$theta_06111`: $tco_theta0
  - `$theta_05622`: $tco_theta0
  - `$theta_05621`: $tco_theta0
  - `$theta_05612`: $tco_theta0
  - `$theta_05611`: $tco_theta0
  - `$theta_05522`: $tco_theta0
  - `$theta_05521`: $tco_theta0
  - `$theta_05512`: $tco_theta0
  - `$theta_05511`: $tco_theta0
  - `$theta_05412`: $tco_theta0
  - `$theta_05411`: $tco_theta0
  - `$theta_05331`: $tco_theta0
  - `$theta_05321`: $tco_theta0
  - `$theta_05316`: $tco_theta0
  - `$theta_05315`: $tco_theta0
  - `$theta_05314`: $tco_theta0
  - `$theta_05313`: $tco_theta0
  - `$theta_05312`: $tco_theta0
  - `$theta_05311`: $tco_theta0
  - `$theta_05213`: $tco_theta0
  - `$theta_05212`: $tco_theta0
  - `$theta_05211`: $tco_theta0
  - `$theta_05131`: $tco_theta0
  - `$theta_05121`: $tco_theta0
  - `$theta_05112`: $tco_theta0
  - `$theta_05111`: $tco_theta0
  - `$theta_04563`: $tco_theta0
  - `$theta_04562`: $tco_theta0
  - `$theta_04561`: $tco_theta0
  - `$theta_04551`: $tco_theta0
  - `$theta_04542`: $tco_theta0
  - `$theta_04541`: $tco_theta0
  - `$theta_04531`: $tco_theta0
  - `$theta_04521`: $tco_theta0
  - `$theta_04511`: $tco_theta0
  - `$theta_04441`: $tco_theta0
  - `$theta_04431`: $tco_theta0
  - `$theta_04421`: $tco_theta0
  - `$theta_04411`: $tco_theta0
  - `$theta_04322`: $tco_theta0
  - `$theta_04321`: $tco_theta0
  - `$theta_04312`: $tco_theta0
  - `$theta_04311`: $tco_theta0
  - `$theta_04132`: $tco_theta0
  - `$theta_04131`: $tco_theta0
  - `$theta_04121`: $tco_theta0
  - `$theta_04112`: $tco_theta0
  - `$theta_04111`: $tco_theta0
  - `$theta_03221`: $tco_theta0
  - `$theta_03213`: $tco_theta0
  - `$theta_03212`: $tco_theta0
  - `$theta_03211`: $tco_theta0
  - `$theta_03143`: $tco_theta0
  - `$theta_03142`: $tco_theta0
  - `$theta_03141`: $tco_theta0
  - `$theta_03133`: $tco_theta0
  - `$theta_03132`: $tco_theta0
  - `$theta_03131`: $tco_theta0
  - `$theta_03123`: $tco_theta0
  - `$theta_03122`: $tco_theta0
  - `$theta_03121`: $tco_theta0
  - `$theta_03111`: $tco_theta0
  - `$theta_02213`: $tco_theta0
  - `$theta_02212`: $tco_theta0
  - `$theta_02211`: $tco_theta0
  - `$theta_02142`: $tco_theta0
  - `$theta_02141`: $tco_theta0
  - `$theta_02131`: $tco_theta0
  - `$theta_02122`: $tco_theta0
  - `$theta_02121`: $tco_theta0
  - `$theta_02111`: $tco_theta0
  - `$theta_01232`: $tco_theta0
  - `$theta_01231`: $tco_theta0
  - `$theta_01224`: $tco_theta0
  - `$theta_01223`: $tco_theta0
  - `$theta_01222`: $tco_theta0
  - `$theta_01221`: $tco_theta0
  - `$theta_01213`: $tco_theta0
  - `$theta_01212`: $tco_theta0
  - `$theta_01211`: $tco_theta0
  - `$theta_01194`: $tco_theta0
  - `$theta_01193`: $tco_theta0
  - `$theta_01192`: $tco_theta0
  - `$theta_01191`: $tco_theta0
  - `$theta_01186`: $tco_theta0
  - `$theta_01185`: $tco_theta0
  - `$theta_01184`: $tco_theta0
  - `$theta_01183`: $tco_theta0
  - `$theta_01182`: $tco_theta0
  - `$theta_01181`: $tco_theta0
  - `$theta_01177`: $tco_theta0
  - `$theta_01176`: $tco_theta0
  - `$theta_01175`: $tco_theta0
  - `$theta_01174`: $tco_theta0
  - `$theta_01173`: $tco_theta0
  - `$theta_01172`: $tco_theta0
  - `$theta_01171`: $tco_theta0
  - `$theta_01168`: $tco_theta0
  - `$theta_01167`: $tco_theta0
  - `$theta_01166`: $tco_theta0
  - `$theta_01165`: $tco_theta0
  - `$theta_01164`: $tco_theta0
  - `$theta_01163`: $tco_theta0
  - `$theta_01162`: $tco_theta0
  - `$theta_01161`: $tco_theta0
  - `$theta_01155`: $tco_theta0
  - `$theta_01154`: $tco_theta0
  - `$theta_01153`: $tco_theta0
  - `$theta_01152`: $tco_theta0
  - `$theta_01151`: $tco_theta0
  - `$theta_01147`: $tco_theta0
  - `$theta_01146`: $tco_theta0
  - `$theta_01145`: $tco_theta0
  - `$theta_01144`: $tco_theta0
  - `$theta_01143`: $tco_theta0
  - `$theta_01141`: $tco_theta0
  - `$theta_01134`: $tco_theta0
  - `$theta_01133`: $tco_theta0
  - `$theta_01132`: $tco_theta0
  - `$theta_01131`: $tco_theta0
  - `$theta_01129`: $tco_theta0
  - `$theta_01128`: $tco_theta0
  - `$theta_01127`: $tco_theta0
  - `$theta_01126`: $tco_theta0
  - `$theta_01125`: $tco_theta0
  - `$theta_01124`: $tco_theta0
  - `$theta_01123`: $tco_theta0
  - `$theta_01122`: $tco_theta0
  - `$theta_01121`: $tco_theta0
  - `$theta_01116`: $tco_theta0
  - `$theta_01115`: $tco_theta0
  - `$theta_01114`: $tco_theta0
  - `$theta_01113`: $tco_theta0
  - `$theta_01112`: $tco_theta0

### 7. Function: DefConst
  **Constants Defined:**
  - `$tco_t_std`: $tco_base_t_std
  - `$tco_t_red1`: $tco_base_t_red1
  - `$tco_t_red2`: $tco_base_t_red2
  - `$tco_t_zero`: $tco_base_t_zero
  - `$tco_theta1`: 20%
  - `$tco_theta2`: 50%
  - `$tco_theta3`: 80%
  - `$tco_theta0`: 100%
  - `$tco_theta_flag`: 0
  - `$tco_t_red3`: n/a

### 8. Function: DefConst
  **Constants Defined:**
  - `$tco_a_07222b`: $tco_base_a_07222b
  - `$tco_a_07222a`: $tco_base_a_07222a
  - `$tco_a_07221d`: $tco_base_a_07221d
  - `$tco_a_07221c`: $tco_base_a_07221c
  - `$tco_a_07221b`: $tco_base_a_07221b
  - `$tco_a_07221a`: $tco_base_a_07221a
  - `$tco_a_04542`: $tco_base_a_04542
  - `$tco_a_04541`: $tco_base_a_04541
  - `$tco_a_04531c`: $tco_base_a_04531c
  - `$tco_a_04531b`: $tco_base_a_04531b
  - `$tco_a_04531a2`: $tco_base_a_04531a2
  - `$tco_a_04531a1`: $tco_base_a_04531a1
  - `$tco_a_04521`: $tco_base_a_04521
  - `$tco_a_04511`: $tco_base_a_04511
  - `$tco_a_02213b`: n/a
  - `$tco_a_02213a`: $tco_base_a_02213a
  - `$tco_a_02212`: $tco_base_a_02212
  - `$tco_a_02122b1`: $tco_base_a_02122b1
  - `$tco_a_02131`: $tco_base_a_02131
  - `$tco_a_02122a`: $tco_base_a_02122a
  - `$tco_a_02121`: $tco_base_a_02121
  - `$tco_a_02111`: $tco_base_a_02111
  - `$tco_a_02122b2`: $tco_base_a_02122b2
  - `$tco_a_02142`: $tco_base_a_02142
  - `$tco_a_02141`: $tco_base_a_02141
  - `$tco_a_02211`: $tco_base_a_02211

### 9. Function: DefIl
  - **Name**: `il_xs_rest`
  - **xs01111**: `+`
  - **Warn_If_NonMonetary**: `no`
  - **xs12714**: `+`
  - **xs12713**: `+`
  - **xs12712**: `+`
  - **xs12711**: `+`
  - **xs12621**: `+`
  - **xs12551**: `+`
  - **xs12542**: `+`
  - **xs12541**: `+`
  - **xs12531**: `+`
  - **xs12521**: `+`
  - **xs12421**: `+`
  - **xs12411**: `+`
  - **xs12324**: `+`
  - **xs12323**: `+`
  - **xs12322**: `+`
  - **xs12321**: `+`
  - **xs12312**: `+`
  - **xs12311**: `+`
  - **xs12139**: `+`
  - **xs12138**: `+`
  - **xs12137**: `+`
  - **xs12136**: `+`
  - **xs12135**: `+`
  - **xs12134**: `+`
  - **xs12133**: `+`
  - **xs12132**: `+`
  - **xs12131**: `+`
  - **xs12121**: `+`
  - **xs12113**: `+`
  - **xs12112**: `+`
  - **xs12111**: `+`
  - **xs11212**: `+`
  - **xs11211**: `+`
  - **xs11123**: `+`
  - **xs11122**: `+`
  - **xs11121**: `+`
  - **xs11113**: `+`
  - **xs11112**: `+`
  - **xs11111**: `+`
  - **xs10612**: `+`
  - **xs10611**: `+`
  - **xs10513**: `+`
  - **xs10512**: `+`
  - **xs10511**: `+`
  - **xs10411**: `+`
  - **xs10311**: `+`
  - **xs10211**: `+`
  - **xs10112**: `+`
  - **xs10111**: `+`
  - **xs09622**: `+`
  - **xs09621**: `+`
  - **xs09612**: `+`
  - **xs09611**: `+`
  - **xs09542**: `+`
  - **xs09541**: `+`
  - **xs09531**: `+`
  - **xs09522**: `+`
  - **xs09521**: `+`
  - **xs09513**: `+`
  - **xs09512**: `+`
  - **xs09511**: `+`
  - **xs09431**: `+`
  - **xs09424**: `+`
  - **xs09423**: `+`
  - **xs09422**: `+`
  - **xs09421**: `+`
  - **xs09412**: `+`
  - **xs09411**: `+`
  - **xs09351**: `+`
  - **xs09343**: `+`
  - **xs09342**: `+`
  - **xs09341**: `+`
  - **xs09332**: `+`
  - **xs09331**: `+`
  - **xs09322**: `+`
  - **xs09321**: `+`
  - **xs09312**: `+`
  - **xs09311**: `+`
  - **xs09231**: `+`
  - **xs09222**: `+`
  - **xs09221**: `+`
  - **xs09212**: `+`
  - **xs09211**: `+`
  - **xs09151**: `+`
  - **xs09143**: `+`
  - **xs09142**: `+`
  - **xs09141**: `+`
  - **xs09136**: `+`
  - **xs09135**: `+`
  - **xs09134**: `+`
  - **xs09132**: `+`
  - **xs09131**: `+`
  - **xs09122**: `+`
  - **xs09121**: `+`
  - **xs09114**: `+`
  - **xs09113**: `+`
  - **xs09112**: `+`
  - **xs09111**: `+`
  - **xs08313**: `+`
  - **xs08312**: `+`
  - **xs08311**: `+`
  - **xs08211**: `+`
  - **xs08112**: `+`
  - **xs08111**: `+`
  - **xs07362**: `+`
  - **xs07361**: `+`
  - **xs07356**: `+`
  - **xs07355**: `+`
  - **xs07354**: `+`
  - **xs07353**: `+`
  - **xs07352**: `+`
  - **xs07351**: `+`
  - **xs07341**: `+`
  - **xs07331**: `+`
  - **xs07322**: `+`
  - **xs07321**: `+`
  - **xs07311**: `+`
  - **xs07247**: `+`
  - **xs07246**: `+`
  - **xs07245**: `+`
  - **xs07244**: `+`
  - **xs07243**: `+`
  - **xs07242**: `+`
  - **xs07241**: `+`
  - **xs07234**: `+`
  - **xs07233**: `+`
  - **xs07232**: `+`
  - **xs07231**: `+`
  - **xs07223**: `+`
  - **xs07213**: `+`
  - **xs07212**: `+`
  - **xs07211**: `+`
  - **xs07131**: `+`
  - **xs07122**: `+`
  - **xs07121**: `+`
  - **xs07113**: `+`
  - **xs07112**: `+`
  - **xs07111**: `+`
  - **xs06322**: `+`
  - **xs06321**: `+`
  - **xs06312**: `+`
  - **xs06311**: `+`
  - **xs06233**: `+`
  - **xs06232**: `+`
  - **xs06231**: `+`
  - **xs06221**: `+`
  - **xs06212**: `+`
  - **xs06211**: `+`
  - **xs06134**: `+`
  - **xs06133**: `+`
  - **xs06132**: `+`
  - **xs06131**: `+`
  - **xs06121**: `+`
  - **xs06112**: `+`
  - **xs06111**: `+`
  - **xs05622**: `+`
  - **xs05621**: `+`
  - **xs05612**: `+`
  - **xs05611**: `+`
  - **xs05522**: `+`
  - **xs05521**: `+`
  - **xs05512**: `+`
  - **xs05511**: `+`
  - **xs05412**: `+`
  - **xs05411**: `+`
  - **xs05331**: `+`
  - **xs05321**: `+`
  - **xs05316**: `+`
  - **xs05315**: `+`
  - **xs05314**: `+`
  - **xs05313**: `+`
  - **xs05312**: `+`
  - **xs05311**: `+`
  - **xs05213**: `+`
  - **xs05212**: `+`
  - **xs05211**: `+`
  - **xs05131**: `+`
  - **xs05121**: `+`
  - **xs05112**: `+`
  - **xs05111**: `+`
  - **xs04563**: `+`
  - **xs04562**: `+`
  - **xs04561**: `+`
  - **xs04551**: `+`
  - **xs04441**: `+`
  - **xs04431**: `+`
  - **xs04421**: `+`
  - **xs04411**: `+`
  - **xs04322**: `+`
  - **xs04321**: `+`
  - **xs04312**: `+`
  - **xs04311**: `+`
  - **xs04132**: `+`
  - **xs04131**: `+`
  - **xs04121**: `+`
  - **xs04112**: `+`
  - **xs04111**: `+`
  - **xs03221**: `+`
  - **xs03213**: `+`
  - **xs03212**: `+`
  - **xs03211**: `+`
  - **xs03143**: `+`
  - **xs03142**: `+`
  - **xs03141**: `+`
  - **xs03133**: `+`
  - **xs03132**: `+`
  - **xs03131**: `+`
  - **xs03123**: `+`
  - **xs03122**: `+`
  - **xs03121**: `+`
  - **xs03111**: `+`
  - **xs01232**: `+`
  - **xs01231**: `+`
  - **xs01224**: `+`
  - **xs01223**: `+`
  - **xs01222**: `+`
  - **xs01221**: `+`
  - **xs01213**: `+`
  - **xs01212**: `+`
  - **xs01211**: `+`
  - **xs01194**: `+`
  - **xs01193**: `+`
  - **xs01192**: `+`
  - **xs01191**: `+`
  - **xs01186**: `+`
  - **xs01185**: `+`
  - **xs01184**: `+`
  - **xs01183**: `+`
  - **xs01182**: `+`
  - **xs01181**: `+`
  - **xs01177**: `+`
  - **xs01176**: `+`
  - **xs01175**: `+`
  - **xs01174**: `+`
  - **xs01173**: `+`
  - **xs01172**: `+`
  - **xs01171**: `+`
  - **xs01168**: `+`
  - **xs01167**: `+`
  - **xs01166**: `+`
  - **xs01165**: `+`
  - **xs01164**: `+`
  - **xs01163**: `+`
  - **xs01162**: `+`
  - **xs01161**: `+`
  - **xs01155**: `+`
  - **xs01154**: `+`
  - **xs01153**: `+`
  - **xs01152**: `+`
  - **xs01151**: `+`
  - **xs01147**: `+`
  - **xs01146**: `+`
  - **xs01145**: `+`
  - **xs01144**: `+`
  - **xs01143**: `+`
  - **xs01141**: `+`
  - **xs01134**: `+`
  - **xs01133**: `+`
  - **xs01132**: `+`
  - **xs01131**: `+`
  - **xs01129**: `+`
  - **xs01128**: `+`
  - **xs01127**: `+`
  - **xs01126**: `+`
  - **xs01125**: `+`
  - **xs01124**: `+`
  - **xs01123**: `+`
  - **xs01122**: `+`
  - **xs01121**: `+`
  - **xs01116**: `+`
  - **xs01115**: `+`
  - **xs01114**: `+`
  - **xs01113**: `+`
  - **xs01112**: `+`

### 10. Function: DefIl
  - **Name**: `ils_extstat_ittcal`
  - **il_itt_revc**: `+`
  - **il_itt_excc**: `+`

### 11. Function: DefIl
  - **Name**: `il_itt_excc`
  - **il_tx0211_na**: `+`
  - **il_tx02121_na**: `+`
  - **il_tx02122_na**: `+`
  - **il_tx0213_na**: `+`
  - **il_tx022_na**: `+`
  - **il_tx045_na**: `+`
  - **il_tx0451_na**: `+`
  - **il_tx04521_na**: `+`
  - **il_tx045_072_na**: `+`

### 12. Function: DefIl
  - **Name**: `il_itt_revc`
  - **il_tva_na**: `+`
  - **il_tx_na**: `+`

### 13. Function: DefIl
  - **Name**: `ils_extstat_ittncal`
  - **il_itt_expnc**: `+`
  - **il_itt_revnc**: `+`
  - **il_itt_excnc**: `+`

### 14. Function: DefIl
  - **Name**: `il_itt_excnc`
  - **il_tx0211**: `+`
  - **il_tx02121**: `+`
  - **il_tx02122**: `+`
  - **il_tx0213**: `+`
  - **il_tx022**: `+`
  - **il_tx045**: `+`
  - **il_tx0451**: `+`
  - **il_tx04521**: `+`
  - **il_tx045_072**: `+`

### 15. Function: DefIl
  - **Name**: `il_itt_revnc`
  - **il_tva**: `+`
  - **il_tx**: `+`

### 16. Function: DefIl
  - **Name**: `il_itt_expnc`
  - **il_x01**: `+`
  - **il_x02**: `+`
  - **il_x03**: `+`
  - **il_x04**: `+`
  - **il_x05**: `+`
  - **il_x06**: `+`
  - **il_x07**: `+`
  - **il_x08**: `+`
  - **il_x09**: `+`
  - **il_x10**: `+`
  - **il_x11**: `+`
  - **il_x12**: `+`


---

## Policy: bec_at *(Switch: n/a)*
### 1. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 2. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 3. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 4. Function: DefVar *(Switch: n/a)*
  - **i_bec**: `n/a`

### 5. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 6. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$bec_inflationSe_minLim`: n/a
  - `$bec_inflationSe_lim1`: n/a
  - `$bec_inflationSe_lim2`: n/a
  - `$bec_inflationSe_lim3`: n/a
  - `$bec_inflationSe_lim4`: n/a
  - `$bec_inflationSe_lim5`: n/a
  - `$bec_inflationSe_lim6`: n/a
  - `$bec_inflationSe_lim7`: n/a
  - `$bec_inflationSe_lim8`: n/a
  - `$bec_inflationSe_lim9`: n/a
  - `$bec_inflationSe_lim10`: n/a
  - `$bec_inflationSe_lim11`: n/a
  - `$bec_inflationSe_lim12`: n/a
  - `$bec_inflationSe_lim13`: n/a
  - `$bec_inflationSe_lim14`: n/a
  - `$bec_inflationSe_lim15`: n/a
  - `$bec_inflationSe_maxLim`: n/a
  - `$bec_inflationSe_amt1`: n/a
  - `$bec_inflationSe_amt2`: n/a
  - `$bec_inflationSe_amt3`: n/a
  - `$bec_inflationSe_amt4`: n/a
  - `$bec_inflationSe_amt5`: n/a
  - `$bec_inflationSe_amt6`: n/a
  - `$bec_inflationSe_amt7`: n/a
  - `$bec_inflationSe_amt8`: n/a
  - `$bec_inflationSe_amt9`: n/a
  - `$bec_inflationSe_amt10`: n/a
  - `$bec_inflationSe_amt11`: n/a
  - `$bec_inflationSe_amt12`: n/a
  - `$bec_inflationSe_amt13`: n/a
  - `$bec_inflationSe_amt14`: n/a
  - `$bec_inflationSe_amt15`: n/a
  - `$bec_inflationSe_amt16`: n/a

### 7. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Base**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 8. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 9. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 10. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: None

---

## Policy: ptu01_at *(Switch: n/a)*
### 1. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 2. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 3. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 5. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 6. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`


---

## Policy: bedtu_at
### 1. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 2. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bed > 0`
  - **Tax Unit:** `tu_individual_at`

### 4. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dag <= 18`
  - **Comp_perTU**: `bed * $bedtu_rate
 * 4/12`
  - **Output_Var**: `bedtu02_s`
  - **TAX_UNIT**: `tu_individual_at`

### 5. Function: DefConst
  **Constants Defined:**
  - `$bedtu_amt`: n/a
  - `$bedtu_rate`: 0.046


---

## Policy: bhltu_at *(Switch: n/a)*
### 1. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 2. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 3. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`


---

## Policy: bhotu_at
### 1. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 2. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 3. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 5. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: bclmc_at *(Switch: n/a)*
### 1. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 2. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 3. Function: DefVar *(Switch: n/a)*
  - **temp_nDepChild_Disabled**: `n/a`
  - **temp_nDepChild_notDisabled**: `n/a`
  - **i_bclmc_tax_s**: `n/a`

### 4. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perElig**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 5. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perElig**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 6. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$bclim_basic_amt`: n/a
  - `$bclim_addAmt1`: n/a
  - `$bclim_addAmt2`: n/a
  - `$bclim_addAmt3`: n/a
  - `$bclim_addAmt4`: n/a
  - `$bclim_child_rate`: n/a
  - `$bclim_tax_thresh`: n/a

### 7. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 8. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`


---

## Policy: butmc01_at *(Switch: n/a)*
### 1. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 2. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`


---

## Policy: butmc02_at *(Switch: n/a)*
### 1. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 2. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`


---

## Policy: bsatu_at
### 1. Function: DefConst
  **Constants Defined:**
  - `$bsatu_child_amt`: 60#m
  - `$bsatu_child_eqCoef`: 1
  - `$bsatu_parent_lim`: 25725#y

### 2. Function: BenCalc
  - **Comp_Cond**: `tintclp_s#2 > 0 & dag < 18 & il_taxableY#1 <= $bsatu_parent_lim & IsDepChild#2`
  - **Comp_perTU**: `$bsatu_child_amt * $bsatu_child_eqCoef`
  - **Output_Var**: `bsatu_s`
  - **UpLim**: `$bsatu_child_amt * $bsatu_child_eqCoef`
  - **TAX_UNIT**: `tu_individual_at`
  - **#_Level**: `tu_bch00_at`

### 3. Function: ArithOp
  **Formula:** `bsatu_s`
  **Output Variable:** `bsatu_s`
  **Tax Unit:** `tu_household_at`


---
