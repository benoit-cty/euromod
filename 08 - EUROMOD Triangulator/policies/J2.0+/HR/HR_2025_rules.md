# EUROMOD Tax-Benefit Rules for HR_2025

## Policy: SetDefault_hr
### 1. Function: SetDefault
  - **yemmy00**: `12`
  - **Dataset**: `training*`
  - **ysebsre**: `yse`
  - **lemhw00**: `lhw`

### 2. Function: SetDefault
  - **Dataset**: `*_hhot`
  - **lhw_a**: `0`
  - **yem_a**: `0`
  - **liwmy_a**: `0`
  - **lnu**: `0`
  - **yempv_a**: `0`
  - **yemmy_a**: `0`
  - **lma**: `0`
  - **lma18**: `0`
  - **lma19**: `0`
  - **lma20**: `0`
  - **lmc**: `0`
  - **yem18_a**: `0`
  - **yem19_a**: `0`
  - **yem20_a**: `0`
  - **lowas**: `0`
  - **ysemy**: `0`
  - **kfbmy**: `0`
  - **yemmy20_a**: `0`
  - **yemmy19_a**: `0`
  - **yemmy18_a**: `0`
  - **lhw20_a**: `0`
  - **lhw19_a**: `0`
  - **lhw18_a**: `0`
  - **lmc20**: `0`

### 3. Function: SetDefault
  - **Dataset**: `hr_20*`
  - **bsu**: `0`
  - **boa**: `0`
  - **bfamh**: `0`
  - **bfaba**: `0`
  - **bch**: `0`
  - **yptmp**: `0`
  - **ypt00**: `ypt`
  - **aca**: `0`
  - **yst**: `0`
  - **ymwdt**: `0`
  - **bfaot**: `0`
  - **yemtx**: `yem`
  - **yemnt**: `0`
  - **kfbtx**: `kfb`
  - **kfbnt**: `0`
  - **ysecwre00**: `ysecwre`
  - **ysecwre01**: `0`
  - **ysecwre02**: `0`
  - **ymc**: `0`
  - **ymc00**: `0`
  - **ymc01**: `0`
  - **xed00**: `0`
  - **xhl00**: `0`
  - **yiytx**: `yiy`
  - **yiynt**: `0`
  - **pditx**: `pdi`
  - **pdint**: `0`
  - **poatx**: `poa`
  - **poant**: `0`
  - **psutx**: `psu`
  - **psunt**: `0`

### 4. Function: SetDefault
  - **Dataset**: `*_training_data`
  - **yemmy00**: `yemmy`
  - **lemhw00**: `lhw`
  - **ysebsre**: `yse`
  - **xmp00**: `0`
  - **xmpam**: `0`

### 5. Function: SetDefault
  - **Dataset**: `*training*`
  - **bwkmceemy_s**: `0`
  - **bwkmcsemy_s**: `0`
  - **bwkmcmy_s**: `0`
  - **yemmwmy_s**: `0`
  - **ysemwmy_s**: `0`
  - **lmcee_s**: `0`
  - **lmcse_s**: `0`

### 6. Function: SetDefault *(Switch: off)*
  - **Dataset**: `hr_20*`
  - **ydsyc_a**: `0`

### 7. Function: SetDefault *(Switch: off)*
  - **Dataset**: `*`
  - **bsayn_a**: `-1`


---

## Policy: Uprate_hr
### 1. Function: Uprate
  - **Dataset**: `*training_data.txt`
  - **WarnIfNoFactor**: `no`
  - **Def_Factor**: `1`

### 2. Function: Uprate
  - **Dataset**: `HR_20??_??_????_??_??`
  - **kivho**: `$f_monthly_wage`
  - **kfbcc**: `$f_monthly_wage`
  - **tis**: `$f_one`
  - **tscer**: `$f_one`
  - **tscee**: `$f_one`
  - **tad**: `$f_one`
  - **tpr**: `$f_one`
  - **bunot**: `$f_monthly_wage`
  - **bunct**: `$f_monthly_wage`
  - **bsaot**: `$f_sab2`
  - **bsa00**: `$f_sab1`
  - **bho**: `$f_sab2`
  - **bhl**: `$f_monthly_wage`
  - **bed**: `$f_gdp`
  - **afc**: `$f_hicp_nat`
  - **xhcmomi**: `$f_hicp_nat`
  - **xhcrt**: `$f_gdp`
  - **ydses_o**: `$f_one`
  - **ypp**: `$f_monthly_wage`
  - **yds**: `$f_one`
  - **yem_a**: `$f_monthly_wage`
  - **yivwg**: `$f_monthly_wage`
  - **ysv**: `$f_gdp`
  - **ypr**: `$f_gdp`
  - **yot**: `$f_monthly_wage`
  - **ysebsnr**: `$f_monthly_wage`
  - **yemtx**: `$f_monthly_wage_tax`
  - **xpp**: `$f_hicp_nat`
  - **xhcot**: `$f_hicp_nat`
  - **ysecwre00**: `$f_monthly_wage`
  - **ysebsre**: `$f_monthly_wage`
  - **ysecwnr**: `$f_monthly_wage`
  - **tscse**: `$f_one`
  - **AggVar_Part**: `psunt`
  - **AggVar_Name**: `psu`
  - **tin**: `$f_one`
  - **yempv**: `$f_monthly_wage`
  - **bdi**: `$f_sab2`
  - **yse**: `$f_monthly_wage`
  - **tmu**: `$f_one`
  - **boa**: `$f_pens`
  - **bsu**: `$f_bub`
  - **bch**: `$f_bub`
  - **bfaba**: `$f_bub`
  - **bfamh**: `$f_monthly_wage`
  - **ypt00**: `$f_monthly_wage`
  - **yptmp**: `$f_monthly_wage`
  - **xmp00**: `$f_hicp_nat`
  - **xmpam**: `$f_hicp_nat`
  - **bfa**: `$f_bub`
  - **kfbtx**: `$f_monthly_wage`
  - **yst**: `$f_monthly_wage`
  - **ymwdt**: `$f_yemLead`
  - **bfaot**: `$f_bub`
  - **kfbnt**: `$f_monthly_wage`
  - **xed00**: `$f_gdp`
  - **xhl00**: `$f_gdp`
  - **yemnt**: `$f_monthly_wage_nontax`
  - **ysecwre01**: `$f_monthly_wage`
  - **ysecwre02**: `$f_monthly_wage`
  - **ymc00**: `$f_monthly_wage`
  - **ymc01**: `$f_monthly_wage`
  - **pditx**: `$f_pdi_av`
  - **pdint**: `$f_pdi_av`
  - **poatx**: `$f_poa_av`
  - **poant**: `$f_poa_av`
  - **psutx**: `$f_psu_av`
  - **psunt**: `$f_psu_av`
  - **yiytx**: `$f_one`
  - **yiynt**: `$f_one`
  - **Factor_Condition**: `lindi = 0`


---

## Policy: ConstDef_hr
### 1. Function: DefConst
  **Constants Defined:**
  - `$ANWPY`: 1302#m
  - `$ANWPY2`: 1317#m
  - `$GMW`: 970#m
  - `$PSMW`: 800.75#m
  - `$BUB`: 441.44#m
  - `$Nwh`: 40
  - `$tsceepi02_rate`: 0.05
  - `$tsceepi01_rate`: 0.15
  - `$tsceepi00_rate`: 0.2
  - `$tscsebusi01_rate`: n/a
  - `$tscersi00_rate`: 0.165
  - `$tscerui_rate`: n/a
  - `$AGWPY`: 1798#m
  - `$PensionAgeWomen`: 63.75
  - `$PensionAgeMen`: 65
  - `$tscbesi_rate1`: 0
  - `$tscbesi_rate2`: 0
  - `$tscsecwsi00_rate`: 0.075
  - `$tscsecwpi01_rate`: 0.075
  - `$tscsecwpi00_rate`: 0.1
  - `$tscsecwpi02_rate`: 0.025
  - `$tscseui_rate`: n/a
  - `$tscsebusi00_rate`: 0.075
  - `$tscsebupi00_farmC_rate`: 0.1
  - `$tscsebupi01_farmC_rate`: 0.05
  - `$PAB`: 600#m
  - `$SAB1`: 160#m
  - `$SAB2`: 75#m

### 2. Function: DefConst
  **Constants Defined:**
  - `$UB_QperMin`: 9
  - `$UB_QperTot`: 24

### 3. Function: DefConst
  **Constants Defined:**
  - `$mc_am1`: 0
  - `$mc_am2`: 0
  - `$lhw`: 0

### 4. Function: DefConst *(Switch: off)*
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

### 5. Function: DefConst
  **Constants Defined:**
  - `$bsa_BTA_rate`: 1
  - `$bsa_BCA_rate`: 1


---

## Policy: ilsdef_hr
### 1. Function: DefIl
  - **Name**: `ils_earns`
  - **ysebsnr**: `+`
  - **yemtx**: `+`
  - **ysecwre**: `+`
  - **ysebsre**: `+`
  - **ysecwnr**: `+`
  - **yst**: `+`
  - **yemnt**: `+`

### 2. Function: DefIl
  - **Name**: `ils_origy`
  - **ypt**: `+`
  - **yiy**: `+`
  - **ypr**: `+`
  - **ypp**: `+`
  - **yot**: `+`
  - **ysebsnr**: `+`
  - **yemtx**: `+`
  - **ysecwre**: `+`
  - **ysebsre**: `+`
  - **ysecwnr**: `+`
  - **xmp00**: `-`
  - **xmpam**: `-`
  - **yst**: `+`
  - **yemnt**: `+`
  - **ymc**: `+`

### 3. Function: DefIl
  - **Name**: `ils_origrepy`
  - **bunct_s**: `+`
  - **ils_pen**: `+`
  - **ils_origy**: `+`
  - **bfapl_s**: `+`
  - **bfama_s**: `+`
  - **bhl**: `+`
  - **bwkmc_s**: `n/a`

### 4. Function: DefIl
  - **Name**: `ils_pen`
  - **psu**: `+`
  - **poa**: `+`
  - **pdi**: `+`

### 5. Function: DefIl
  - **Name**: `ils_benmt`
  - **bsa_s**: `+`
  - **bho**: `+`
  - **bch_s**: `+`
  - **bsaot**: `+`
  - **bhout_s**: `+`
  - **boamt_s**: `+`
  - **boatu00_s**: `+`
  - **boatu01_s**: `+`
  - **bsatu_s**: `n/a`
  - **bchtu_s**: `n/a`

### 6. Function: DefIl
  - **Name**: `ils_bennt`
  - **bhl**: `+`
  - **bfaba_s**: `+`
  - **bmanc_s**: `+`
  - **bed**: `+`
  - **bfapl_s**: `+`
  - **bfama_s**: `+`
  - **bunct_s**: `+`
  - **bdi**: `+`
  - **bunot**: `+`
  - **boa**: `+`
  - **bsu**: `+`
  - **bfaot**: `+`
  - **bwkmc_s**: `n/a`
  - **ymc**: `n/a`
  - **buntu_s**: `n/a`
  - **bditu_s**: `n/a`
  - **bfafh_s**: `+`

### 7. Function: DefIl
  - **Name**: `ils_ben`
  - **ils_benmt**: `+`
  - **ils_pen**: `+`
  - **ils_bennt**: `+`

### 8. Function: DefIl
  - **Name**: `ils_bensim`
  - **bunct_s**: `+`
  - **bsa_s**: `+`
  - **bfaba_s**: `+`
  - **bmanc_s**: `+`
  - **bfapl_s**: `+`
  - **bfama_s**: `+`
  - **bch_s**: `+`
  - **bhout_s**: `+`
  - **bwkmc_s**: `n/a`
  - **boamt_s**: `+`
  - **boatu00_s**: `+`
  - **buntu_s**: `n/a`
  - **bchtu_s**: `n/a`
  - **bsatu_s**: `n/a`
  - **bditu_s**: `n/a`
  - **bfafh_s**: `+`
  - **boatu01_s**: `+`

### 9. Function: DefIl
  - **Name**: `ils_taxsim`
  - **tin_s**: `+`
  - **tmu_s**: `n/a`

### 10. Function: DefIl
  - **Name**: `ils_tax`
  - **ils_taxwl**: `+`
  - **ils_taxin**: `+`

### 11. Function: DefIl
  - **Name**: `ils_sicer`
  - **tscerui_s**: `n/a`
  - **tscersi01_s**: `n/a`
  - **tscersi00_s**: `+`
  - **tscsecwsi00_s**: `+`

### 12. Function: DefIl
  - **Name**: `ils_sicse`
  - **tscsebupi02_s**: `+`
  - **tscsebupi01_s**: `+`
  - **tscsebupi00_s**: `+`
  - **tscsebusi01_s**: `n/a`
  - **tscsebusi00_s**: `+`
  - **tscsecwpi02_s**: `+`
  - **tscsecwpi01_s**: `+`
  - **tscsecwpi00_s**: `+`
  - **tscseui_s**: `n/a`

### 13. Function: DefIl
  - **Name**: `ils_sicee`
  - **tsceepi02_s**: `+`
  - **tsceepi01_s**: `+`
  - **tsceepi00_s**: `+`

### 14. Function: DefIl
  - **Name**: `ils_dispy`
  - **ils_sicdy**: `-`
  - **ils_tax**: `-`
  - **ils_ben**: `+`
  - **ils_origy**: `+`

### 15. Function: DefIl
  - **Name**: `ils_b1_bed`
  - **bed**: `+`

### 16. Function: DefIl
  - **Name**: `ils_b1_bun`
  - **bunct_s**: `+`
  - **bunot**: `+`
  - **bwkmc_s**: `n/a`

### 17. Function: DefIl
  - **Name**: `ils_b1_bdi`
  - **pdi**: `+`
  - **bdi**: `+`

### 18. Function: DefIl
  - **Name**: `ils_b1_bsu`
  - **psu**: `+`
  - **bsu**: `+`

### 19. Function: DefIl
  - **Name**: `ils_b1_bho`
  - **bho**: `+`

### 20. Function: DefIl
  - **Name**: `ils_b1_bsa`
  - **bsa_s**: `+`
  - **bsaot**: `+`
  - **bhout_s**: `+`
  - **boamt_s**: `+`
  - **boatu00_s**: `+`
  - **buntu_s**: `n/a`
  - **bchtu_s**: `n/a`
  - **bsatu_s**: `n/a`
  - **bditu_s**: `n/a`
  - **boatu01_s**: `+`

### 21. Function: DefIl
  - **Name**: `ils_b1_bhl`
  - **bhl**: `+`

### 22. Function: DefIl
  - **Name**: `ils_b1_boa`
  - **poa**: `+`
  - **boa**: `+`

### 23. Function: DefIl
  - **Name**: `ils_b1_bfa`
  - **bch_s**: `+`
  - **ils_b1_bcb**: `+`
  - **bfaot**: `+`
  - **ymc**: `n/a`

### 24. Function: DefIl
  - **Name**: `ils_b2_bfaed`
  - **ils_b1_bfa**: `+`
  - **ils_b1_bed**: `+`

### 25. Function: DefIl
  - **Name**: `ils_b2_bsaho`
  - **ils_b1_bsa**: `+`
  - **ils_b1_bho**: `+`

### 26. Function: DefIl
  - **Name**: `ils_b2_penhl`
  - **ils_b1_boa**: `+`
  - **ils_b1_bdi**: `+`
  - **ils_b1_bhl**: `+`
  - **ils_b1_bsu**: `+`

### 27. Function: DefIl
  - **Name**: `ils_sicct`
  - **tscct_s**: `+`

### 28. Function: DefIl
  - **Name**: `ils_sicot`
  - **tscbesi_s**: `n/a`

### 29. Function: DefIl
  - **Name**: `ils_sicdy`
  - **ils_sicot**: `+`
  - **ils_sicse**: `+`
  - **ils_sicee**: `+`

### 30. Function: DefIl
  - **Name**: `ils_base_tin`
  - **yiy**: `+`
  - **ypr**: `+`
  - **ysecwre**: `+`
  - **ysebsre**: `+`
  - **kfbtx**: `+`
  - **yemtx**: `+`
  - **psutx**: `+`
  - **pditx**: `+`
  - **poatx**: `+`

### 31. Function: DefIl *(Switch: n/a)*
  - **Name**: `n/a`
  - **yiy**: `n/a`
  - **ypr**: `n/a`
  - **ysecwre**: `n/a`
  - **ysebsre**: `n/a`
  - **kfb**: `n/a`
  - **yem**: `n/a`
  - **psu**: `n/a`
  - **pdi**: `n/a`
  - **poa**: `n/a`

### 32. Function: DefIl
  - **Name**: `ils_b1_bcb`
  - **bfama_s**: `+`
  - **bfapl_s**: `+`
  - **bmanc_s**: `+`
  - **bfaba_s**: `+`
  - **bfafh_s**: `+`

### 33. Function: DefIl
  - **Name**: `ils_extstat_other`
  - **i_yemkfbtx**: `+`
  - **i_yemkfbnt**: `+`
  - **i_sicerrelam1**: `+`
  - **i_sicerrelam3**: `+`

### 34. Function: DefIl
  - **Name**: `ils_b1_bwk`

### 35. Function: DefIl
  - **Name**: `ils_b2_bunwk`
  - **ils_b1_bwk**: `+`
  - **ils_b1_bun**: `+`

### 36. Function: DefIl
  - **Name**: `ils_taxin`
  - **tin_s**: `+`
  - **tmu_s**: `n/a`

### 37. Function: DefIl
  - **Name**: `ils_taxwl`
  - **tpr**: `+`


---

## Policy: tudef_hr
### 1. Function: DefTu
  - **Type**: `IND`
  - **Name**: `tu_individual_hr`

### 2. Function: DefTu
  - **Type**: `HH`
  - **Name**: `tu_hh_oecd_co`
  - **DepChildCond**: `(dag<14)`

### 3. Function: DefTu
  - **Type**: `HH`
  - **Name**: `tu_household_hr`
  - **HeadDefInc**: `ils_origy`
  - **DepChildCond**: `(dag<14)`

### 4. Function: DefTu
  - **Type**: `SUBGROUP`
  - **Name**: `tu_mar_couple_hr`
  - **Members**: `Partner`
  - **PartnerCond**: `(Default) & (IsMarried)`

### 5. Function: DefTu
  - **Type**: `SUBGROUP`
  - **Name**: `tu_bfama_hr`
  - **DepChildCond**: `(dag = 0) | (dag = 1)`
  - **Members**: `Partner & OwnDepChild & LooseDepChild`
  - **NoChildIfPartner**: `yes`
  - **NoChildIfHead**: `yes`
  - **ExtHeadCond**: `(default) & (dgn = 0)`
  - **StopIfNoHeadFound**: `no`

### 6. Function: DefTu
  - **Type**: `SUBGROUP`
  - **Name**: `tu_bfapl_broad_hr`
  - **DepChildCond**: `(dag <= 40) & !(IsParent)`
  - **Members**: `Partner & OwnDepChild & LooseDepChild & DepParent`
  - **NoChildIfPartner**: `yes`
  - **NoChildIfHead**: `yes`
  - **ExtHeadCond**: `(default) & (dgn=0)`
  - **StopIfNoHeadFound**: `no`
  - **DepParentCond**: `(Default)`

### 7. Function: DefTu
  - **Type**: `SUBGROUP`
  - **Name**: `tu_bfapl_hr`
  - **DepChildCond**: `(dag <= 3) `
  - **Members**: `Partner & OwnDepChild & LooseDepChild`
  - **NoChildIfPartner**: `yes`
  - **NoChildIfHead**: `yes`
  - **ExtHeadCond**: `(default) & (dgn=0)`
  - **StopIfNoHeadFound**: `no`

### 8. Function: DefTu
  - **Type**: `SUBGROUP`
  - **Name**: `tu_bfaba_hr`
  - **DepChildCond**: `(dag = 0)`
  - **Members**: `Partner & OwnDepChild & LooseDepChild`
  - **NoChildIfPartner**: `yes`
  - **NoChildIfHead**: `yes`
  - **ExtHeadCond**: `(default)`
  - **StopIfNoHeadFound**: `no`

### 9. Function: DefTu
  - **Name**: `tu_tin_broad_hr`
  - **Type**: `HH`
  - **DepChildCond**: `(IsOwnChild)`
  - **AssignPartnerOfDependents**: `no`
  - **HeadDefInc**: `ils_origy`

### 10. Function: DefTu
  - **Name**: `tu_bfafh_hr`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild & LooseDepChild`
  - **DepChildCond**: `(dag = 0)`
  - **NoChildIfHead**: `yes`
  - **NoChildIfPartner**: `yes`
  - **ExtHeadCond**: `(default) & (dgn = 1)`
  - **StopIfNoHeadFound**: `no`


---

## Policy: yem_hr *(Switch: toggle)*
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yem > 0)`
  - **Tax Unit:** `tu_individual_hr`

### 2. Function: Max
  - **Val**: `$GMW * min(lhw, $Nwh) / $Nwh * yemmy / 12`
  - **Output_Var**: `yem`
  - **TAX_UNIT**: `tu_individual_hr`
  - **Who_Must_Be_Elig**: `one`

### 3. Function: ChangeParam
  - **Param_Id**: `dd4bf183-2937-4ffc-b61f-c07421db4ef3`
  - **Param_NewVal**: `HR_2025_yem_std`


---

## Policy: neg_hr
### 1. Function: DefVar
  - **i_ysebsnr**: `0`
  - **i_ysecwre**: `0`
  - **i_ysebsre**: `0`
  - **i_ysecwnr**: `0`

### 2. Function: ArithOp
  **Formula:** `ysebsnr`
  **Output Variable:** `i_ysebsnr`
  **Tax Unit:** `tu_individual_hr`

### 3. Function: Max
  - **Val**: `0`
  - **Output_Var**: `ysebsnr`
  - **TAX_UNIT**: `tu_individual_hr`

### 4. Function: ArithOp
  **Formula:** `ysecwre`
  **Output Variable:** `i_ysecwre`
  **Tax Unit:** `tu_individual_hr`

### 5. Function: ArithOp
  **Formula:** `ysebsre`
  **Output Variable:** `i_ysebsre`
  **Tax Unit:** `tu_individual_hr`

### 6. Function: ArithOp
  **Formula:** `ysecwnr`
  **Output Variable:** `i_ysecwnr`
  **Tax Unit:** `tu_individual_hr`

### 7. Function: Max
  - **Val**: `0`
  - **Output_Var**: `ysecwre`
  - **TAX_UNIT**: `tu_individual_hr`

### 8. Function: Max
  - **Val**: `0`
  - **Output_Var**: `ysebsre`
  - **TAX_UNIT**: `tu_individual_hr`

### 9. Function: Max
  - **Val**: `0`
  - **Output_Var**: `ysecwnr`
  - **TAX_UNIT**: `tu_individual_hr`

### 10. Function: ArithOp
  **Formula:** `ysebsnr + ysecwnr + ysebsre + ysecwre`
  **Output Variable:** `yse`
  **Tax Unit:** `tu_individual_hr`


---

## Policy: tscer_hr
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(i_yemkfbtx > 0) & (i_yemhwy > 0)`
  - **Tax Unit:** `tu_individual_hr`

### 2. Function: DefVar
  - **i_sicerbft0**: `0`
  - **i_yemfteq**: `0`
  - **i_sicerdcft**: `0`
  - **i_yemaj**: `0`
  - **i_yempt**: `0`
  - **i_yemft**: `0`
  - **i_yemhwy**: `0`
  - **i_yemkfbtx**: `0`
  - **i_yempteq**: `0`
  - **i_sicerdcpt**: `0`
  - **i_sicerbpt0**: `0`
  - **i_sicerbaj**: `0`
  - **i_sicerb**: `0`
  - **i_sicerrel1**: `0`
  - **i_sicerrel3**: `0`
  - **i_yemkfbnt**: `0`
  - **i_sicerrelam1**: `0`
  - **i_sicerrelam3**: `0`

### 3. Function: ArithOp
  **Formula:** `$tscersi00_rate * i_sicerb * (1 - i_sicerrel1 - i_sicerrel3)`
  **Output Variable:** `tscersi00_s`
  **Tax Unit:** `tu_individual_hr`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 5. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 6. Function: ArithOp
  **Formula:** `i_yemft`
  **Output Variable:** `i_sicerbft0`
  **Tax Unit:** `tu_individual_hr`

### 7. Function: ArithOp
  **Formula:** `i_yemft/min(lemhw00,$Nwh)*$Nwh/(yemmy00/12)`
  **Output Variable:** `i_yemfteq`
  **Tax Unit:** `tu_individual_hr`

### 8. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 9. Function: ArithOp
  **Formula:** `i_yemkfbtx *  (yemmy00 * lemhw00 * 52/12) / i_yemhwy`
  **Output Variable:** `i_yemft`
  **Tax Unit:** `tu_individual_hr`

### 10. Function: ArithOp
  **Formula:** `(52 / 12) * (yemmy00 * lemhw00 + yemmy01 * lemhw01 + yemajmy * lemhw02)`
  **Output Variable:** `i_yemhwy`
  **Tax Unit:** `tu_individual_hr`

### 11. Function: ArithOp
  **Formula:** `i_yemkfbtx *  (yemmy01 * lemhw01 * 52/12) / i_yemhwy`
  **Output Variable:** `i_yempt`
  **Tax Unit:** `tu_individual_hr`

### 12. Function: ArithOp
  **Formula:** `i_yemkfbtx *  (yemajmy * lemhw02 * 52/12) / i_yemhwy`
  **Output Variable:** `i_yemaj`
  **Tax Unit:** `tu_individual_hr`

### 13. Function: ArithOp
  **Formula:** `i_yempt / min(lemhw01, $Nwh) * $Nwh / (yemmy01 / 12)`
  **Output Variable:** `i_yempteq`
  **Tax Unit:** `tu_individual_hr`

### 14. Function: ArithOp
  **Formula:** `yemtx + kfbtx`
  **Output Variable:** `i_yemkfbtx`
  **Tax Unit:** `tu_individual_hr`

### 15. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(i_yemft > 0) & (i_yemhwy > 0)`
  - **Tax Unit:** `tu_individual_hr`

### 16. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(i_yempt > 0) & (i_yemhwy > 0)`
  - **Tax Unit:** `tu_individual_hr`

### 17. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 18. Function: ArithOp
  **Formula:** `i_yempt`
  **Output Variable:** `i_sicerbpt0`
  **Tax Unit:** `tu_individual_hr`

### 19. Function: ArithOp
  **Formula:** `i_yemaj`
  **Output Variable:** `i_sicerbaj`
  **Tax Unit:** `tu_individual_hr`

### 20. Function: ArithOp
  **Formula:** `i_sicerbft0  + i_sicerbpt0 + i_sicerbaj`
  **Output Variable:** `i_sicerb`
  **Tax Unit:** `tu_individual_hr`

### 21. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(i_yemaj > 0) & (i_yemhwy > 0)`
  - **Tax Unit:** `tu_individual_hr`

### 22. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(i_sicerb > 0) & (i_yemhwy > 0)`
  - **Tax Unit:** `tu_individual_hr`

### 23. Function: DefConst
  **Constants Defined:**
  - `$tscersi00_randthres1`: 0.55
  - `$tscersi00_randthres3`: 0.77
  - `$tscersi00_minbase`: 0.38

### 24. Function: BenCalc
  - **Comp_Cond**: `(i_sicerrel1 = 0) & (dag < 35) & (yemmy > 0) & (liwwh <= 60)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_sicerrel3`
  - **TAX_UNIT**: `tu_individual_hr`

### 25. Function: BenCalc
  - **Comp_Cond**: `(yemmy > 0) & (liwwh <= yemmy)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_sicerrel1`
  - **TAX_UNIT**: `tu_individual_hr`

### 26. Function: ArithOp
  **Formula:** `yemnt + kfbnt`
  **Output Variable:** `i_yemkfbnt`
  **Tax Unit:** `tu_individual_hr`

### 27. Function: BenCalc
  - **Comp_Cond**: `(i_sicerrel3 > 0)`
  - **Comp_perTU**: `i_sicerrel3`
  - **Output_Var**: `i_sicerrel3`
  - **TAX_UNIT**: `tu_individual_hr`

### 28. Function: BenCalc
  - **Comp_Cond**: `(i_sicerrel1 > 0)`
  - **Comp_perTU**: `i_sicerrel1`
  - **Output_Var**: `i_sicerrel1`
  - **TAX_UNIT**: `tu_individual_hr`

### 29. Function: ArithOp
  **Formula:** `$tscersi00_rate * i_sicerb * i_sicerrel1`
  **Output Variable:** `i_sicerrelam1`
  **Tax Unit:** `tu_individual_hr`

### 30. Function: ArithOp
  **Formula:** `$tscersi00_rate * i_sicerb * i_sicerrel3`
  **Output Variable:** `i_sicerrelam3`
  **Tax Unit:** `tu_individual_hr`


---

## Policy: tscee_hr
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(i_siceeb > 0) & (i_dag >= 40)`
  - **Tax Unit:** `tu_individual_hr`

### 2. Function: ArithOp
  **Formula:** `$tsceepi00_rate * i_siceeb1`
  **Output Variable:** `tsceepi00_s`
  **Tax Unit:** `tu_individual_hr`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(i_siceeb > 0) & (i_dag < 40)`
  - **Tax Unit:** `tu_individual_hr`

### 4. Function: ArithOp
  **Formula:** `$tsceepi01_rate * i_siceeb1`
  **Output Variable:** `tsceepi01_s`
  **Tax Unit:** `tu_individual_hr`

### 5. Function: ArithOp
  **Formula:** `$tsceepi02_rate * i_siceeb`
  **Output Variable:** `tsceepi02_s`
  **Tax Unit:** `tu_individual_hr`

### 6. Function: DefVar
  - **i_dag**: `0`
  - **i_siceebft**: `0`
  - **i_siceebaj**: `0`
  - **i_siceebpt**: `0`
  - **i_siceeb**: `0`
  - **i_siceeb1**: `0`
  - **i_sceepided**: `0`

### 7. Function: ArithOp
  **Formula:** `dag - 24`
  **Output Variable:** `i_dag`
  **Tax Unit:** `tu_individual_hr`

### 8. Function: ArithOp
  **Formula:** `i_yemft`
  **Output Variable:** `i_siceebft`
  **Tax Unit:** `tu_individual_hr`

### 9. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(i_yemft > 0) & (i_yemhwy > 0)`
  - **Tax Unit:** `tu_individual_hr`

### 10. Function: ArithOp
  **Formula:** `i_yempt`
  **Output Variable:** `i_siceebpt`
  **Tax Unit:** `tu_individual_hr`

### 11. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(i_yempt > 0) & (i_yemhwy > 0)`
  - **Tax Unit:** `tu_individual_hr`

### 12. Function: ArithOp
  **Formula:** `i_yemaj`
  **Output Variable:** `i_siceebaj`
  **Tax Unit:** `tu_individual_hr`

### 13. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(i_yemaj > 0) & (i_yemhwy > 0)`
  - **Tax Unit:** `tu_individual_hr`

### 14. Function: ArithOp
  **Formula:** `i_siceebft + i_siceebpt + i_siceebaj`
  **Output Variable:** `i_siceeb`
  **Tax Unit:** `tu_individual_hr`

### 15. Function: DefConst
  **Constants Defined:**
  - `$tsceepi00_ded_thres1`: 700#m
  - `$tsceepi00_ded_rate`: 0.5
  - `$tsceepi00_ded_thres2`: 1300#m
  - `$tsceepi00_ded_amt`: 300#m

### 16. Function: BenCalc
  - **Comp_Cond**: `(yemmy > 0) & (i_siceeb < $tsceepi00_ded_thres1)`
  - **Comp_perTU**: `$tsceepi00_ded_amt * (yemmy / 12)`
  - **Output_Var**: `i_sceepided`
  - **TAX_UNIT**: `tu_individual_hr`

### 17. Function: ArithOp
  **Formula:** `i_siceeb - i_sceepided`
  **Output Variable:** `i_siceeb1`
  **Tax Unit:** `tu_individual_hr`


---

## Policy: tscsebu_hr
### 1. Function: DefConst
  **Constants Defined:**
  - `$tscsebusi00_pro1A_base`: 1.10
  - `$tscsebusi00_pro2A_base`: 0.65
  - `$tscsebusi00_tradA_base`: 0.65
  - `$tscsebusi00_farm2A_base`: 0.55
  - `$tscsebusi00_farmC_base`: 0.38
  - `$tscsebusi00_farmD_base`: 0.38
  - `$tscsebusi00_tradB_base`: 0.40

### 2. Function: BenCalc
  - **Comp_Cond**: `(i_tradB = 1)`
  - **Comp_perTU**: `(ysemy / 12) * $AGWPY * $tscsebusi00_tradB_base * $tscersi00_rate`
  - **Output_Var**: `tscsebusi00_s`
  - **TAX_UNIT**: `tu_individual_hr`

### 3. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 4. Function: BenCalc
  - **Comp_Cond**: `(i_tradB = 1) & (i_dag >= 40)`
  - **Comp_perTU**: `(ysemy / 12) * $AGWPY * $tscsebusi00_tradB_base * $tsceepi00_rate`
  - **Output_Var**: `tscsebupi00_s`
  - **TAX_UNIT**: `tu_individual_hr`

### 5. Function: BenCalc
  - **Comp_Cond**: `(i_tradB = 1) & (i_dag < 40)`
  - **Comp_perTU**: `(ysemy / 12) * $AGWPY * $tscsebusi00_tradB_base * $tsceepi01_rate`
  - **Output_Var**: `tscsebupi01_s`
  - **TAX_UNIT**: `tu_individual_hr`

### 6. Function: BenCalc
  - **Comp_Cond**: `(i_tradB = 1) & (i_dag < 40)`
  - **Comp_perTU**: `(ysemy / 12) * $AGWPY * $tscsebusi00_tradB_base * $tsceepi02_rate`
  - **Output_Var**: `tscsebupi02_s`
  - **TAX_UNIT**: `tu_individual_hr`

### 7. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: tscbesi_hr *(Switch: n/a)*
### 1. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** `n/a`
    - Band: Rate=`n/a`, Limit=``

### 2. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$tscbesi_randthres`: n/a

### 3. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: bunct_hr
### 1. Function: ArithOp
  **Formula:** `max(lunmy,bunctmy)`
  **Output Variable:** `lunmy_s`
  **Tax Unit:** `tu_individual_hr`

### 2. Function: BenCalc
  - **Comp_Cond**: `(lunmy_s > 0) & (bunct = 0)`
  - **Comp_perElig**: `0`
  - **Output_Var**: `liwmy_s`
  - **TAX_UNIT**: `tu_individual_hr`
  - **Comp_LowLim**: `$UB_QperMin`

### 3. Function: BenCalc
  - **Comp_Cond**: `(bunct > 0)`
  - **Comp_perElig**: `yempv`
  - **Output_Var**: `yempv_s`
  - **TAX_UNIT**: `tu_individual_hr`

### 4. Function: BenCalc
  - **Comp_Cond**: `(dgn=0)`
  - **Comp_perElig**: `$PensionAgeWomen - dag`
  - **Output_Var**: `i_yearsleft`
  - **TAX_UNIT**: `tu_individual_hr`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lunmy_s > 0) & (liwmy_s >= $UB_QperMin) & (dag > 15) & (i_yearsleft >= 0)`
  - **Tax Unit:** `tu_individual_hr`

### 6. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_hr`
  - **Output Variable:** `bunmy_s`
    - Band: Rate=``, Limit=``

### 7. Function: BenCalc
  - **Comp_Cond**: `(liwwh <= 384) | (i_yearsleft >= 5)`
  - **Comp_perElig**: `bunmy_s`
  - **Output_Var**: `bunmy_s`
  - **TAX_UNIT**: `tu_individual_hr`

### 8. Function: BenCalc
  - **Comp_Cond**: `(bunct = 0) & (lunmy_s > 0)`
  - **Comp_perElig**: `bunmy_s`
  - **Output_Var**: `bunmy_s`
  - **TAX_UNIT**: `tu_individual_hr`
  - **Who_Must_Be_Elig**: `one`
  - **UpLim**: `lunmy_s`

### 9. Function: ArithOp
  **Formula:** `$UB_rate_period1 * yempv_s`
  **Output Variable:** `sin01_s`
  **Tax Unit:** `tu_individual_hr`

### 10. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 11. Function: ArithOp
  **Formula:** `(sin01_s * min(bunmy_s, 3) + sin02_s * min(max(bunmy_s - 3, 0), 3) + sin03_s * max(bunmy_s - 6, 0)) / 12`
  **Output Variable:** `bunct_s`
  **Tax Unit:** `tu_individual_hr`

### 12. Function: DefVar
  - **i_yearsleft**: `0`

### 13. Function: ArithOp
  **Formula:** `bunmy_s`
  **Output Variable:** `bunmy_s`
  **Tax Unit:** `tu_individual_hr`

### 14. Function: ArithOp *(Switch: off)*
  **Formula:** `liwwh24_h`
  **Output Variable:** `liwmy_s`
  **Tax Unit:** `tu_individual_hr`

### 15. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `bunmy_s>6`
  - **Comp_perTU**: `sin03_s`
  - **Output_Var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_hr`

### 16. Function: BenCalc
  - **Comp_Cond**: `bunmy_s<lunmy_s`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_hr`

### 17. Function: ArithOp
  **Formula:** `$UB_rate_period2 * yempv_s`
  **Output Variable:** `sin02_s`
  **Tax Unit:** `tu_individual_hr`

### 18. Function: ArithOp
  **Formula:** `$UB_rate_period3 * yempv_s`
  **Output Variable:** `sin03_s`
  **Tax Unit:** `tu_individual_hr`

### 19. Function: DefConst
  **Constants Defined:**
  - `$UB_rate_period1`: 0.6
  - `$UB_minamt_period1`: 0.5 * $PSMW
  - `$UB_maxamt_period1`: 0.7 * $ANWPY2
  - `$UB_rate_period2`: 0.35
  - `$UB_minamt_period2`: 0.5 * $PSMW
  - `$UB_maxamt_period2`: 0.4 * $ANWPY2
  - `$UB_rate_period3`: 0.3
  - `$UB_minamt_period3`: 0.5 * $PSMW
  - `$UB_maxamt_period3`: 0.35 * $ANWPY2


---

## Policy: tscsecw_hr
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ysecwre > 0) & (i_dag >= 40)`
  - **Tax Unit:** `tu_individual_hr`

### 2. Function: ArithOp
  **Formula:** `$tscsecwpi00_rate * ysecwre`
  **Output Variable:** `tscsecwpi00_s`
  **Tax Unit:** `tu_individual_hr`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ysecwre > 0) & (i_dag < 40)`
  - **Tax Unit:** `tu_individual_hr`

### 4. Function: ArithOp
  **Formula:** `$tscsecwpi01_rate * ysecwre`
  **Output Variable:** `tscsecwpi01_s`
  **Tax Unit:** `tu_individual_hr`

### 5. Function: ArithOp
  **Formula:** `$tscsecwpi02_rate * ysecwre`
  **Output Variable:** `tscsecwpi02_s`
  **Tax Unit:** `tu_individual_hr`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ysecwre > 0)`
  - **Tax Unit:** `tu_individual_hr`

### 7. Function: ArithOp
  **Formula:** `$tscsecwsi00_rate * ysecwre`
  **Output Variable:** `tscsecwsi00_s`
  **Tax Unit:** `tu_individual_hr`


---

## Policy: bsa_hr
### 1. Function: DefConst
  **Constants Defined:**
  - `$bsa_SingleAdult_amt`: $SAB1 * 1
  - `$bsa_SingleAdultDisab_amt`: $SAB1 * 1.3
  - `$bsa_FamAdult_amt`: $SAB1 * 0.7
  - `$bsa_Child18to25_amt`: n/a
  - `$bsa_Child15to17_amt`: n/a
  - `$bsa_Child7to14_amt`: n/a
  - `$bsa_Child0to6_amt`: n/a
  - `$bsa_FamAdultDisab_amt`: $SAB1 * 0.95
  - `$bsa_LonePar_amt`: $SAB1 * 1.45
  - `$bsa_LoneParDisab_amt`: $SAB1 * 1.60
  - `$bsa_ChildSingleLone0to6_amt`: n/a
  - `$bsa_ChildSingleLone7to14_amt`: n/a
  - `$bsa_ChildSingleLone15to17_amt`: n/a
  - `$bsa_ChildSingleLone18to25_amt`: n/a
  - `$bsa_Alim13to18_thres`: 0.110 * $ANWPY2
  - `$bsa_Alim7to12_thres`: 0.100 * $ANWPY2
  - `$bsa_Alim0to6_thres`: 0.085 * $ANWPY2
  - `$bsa_bta_thres`: 0.03 * $ANWPY
  - `$bsa_Child2Par_amt`: $SAB1 * 0.95
  - `$bsa_ChildSinglePar_amt`: $SAB1 * 1.05
  - `$bsa_ChildLonePar_amt`: $SAB1 * 1.15
  - `$bsa_BTA_rate`: 1
  - `$bsa_minamt`: 0.03 * $ANWPY

### 2. Function: DefVar
  - **i_MoS**: `0`
  - **i_carcond**: `0`
  - **i_npadisbsa**: `0`
  - **i_bsapot**: `0`
  - **i_alim**: `0`
  - **i_alimthres**: `0`
  - **i_finasset**: `0`
  - **i_MoSind**: `0`
  - **i_psuexA_bsa**: `0`
  - **i_npatin_bsa**: `0`

### 3. Function: BenCalc
  - **Comp_Cond**: `(IsDepChild) & (nAdultsInTu = 1) & (yptmp = 0)`
  - **Comp_perElig**: `$bsa_ChildLonePar_amt`
  - **Output_Var**: `i_MoS`
  - **TAX_UNIT**: `tu_bsa_hr`

### 4. Function: DefTu
  - **Type**: `HH`
  - **Name**: `tu_bsa_hr`
  - **DepChildCond**: `(dag < 18)`

### 5. Function: DefIl
  - **Name**: `il_bsa`
  - **bfapl_s**: `+`
  - **bhl**: `+`
  - **yiy**: `+`
  - **ypp**: `+`
  - **ypr**: `+`
  - **ysecwre**: `+`
  - **ysebsre**: `+`
  - **yemtx**: `+`
  - **bunct_s**: `+`
  - **bmanc_s**: `n/a`
  - **bfama_s**: `+`
  - **ils_pen**: `+`
  - **ils_sicse**: `-`
  - **ils_sicee**: `-`
  - **tmu_s**: `n/a`
  - **tin_s**: `-`
  - **i_alim**: `+`
  - **ysv**: `+`
  - **xmpam**: `-`
  - **ysebsnr**: `+`
  - **ysecwnr**: `+`
  - **ils_sicot**: `-`
  - **bwkmc_s**: `n/a`
  - **kfbtx**: `+`
  - **ymc**: `+`
  - **i_psuexA_bsa**: `-`

### 6. Function: ArithOp
  **Formula:** `i_mos - il_bsa`
  **Output Variable:** `i_bsapot`
  **Tax Unit:** `tu_bsa_hr`

### 7. Function: BenCalc
  - **Comp_Cond**: `(aca != 1) | ((aca = 1) & (i_npadisbsa > 0)) | ((aca = 1) & (nPersInUnit > 5))`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_carcond`
  - **TAX_UNIT**: `tu_bsa_hr`

### 8. Function: BenCalc
  - **Comp_Cond**: `(IsDisabled) | (bdi > 0)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_npadisbsa`
  - **TAX_UNIT**: `tu_bsa_hr`

### 9. Function: ArithOp
  **Formula:** `i_bsapot * i_carcond`
  **Output Variable:** `bsa_s`
  **Tax Unit:** `tu_bsa_hr`

### 10. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `(yptmp > 0) & (dag > 6) & (dag <= 12)`
  - **Comp_perElig**: `$bsa_Alim7to12_thres`
  - **Output_Var**: `i_alimthres`
  - **TAX_UNIT**: `tu_bsa_hr`

### 11. Function: ArithOp
  **Formula:** `yptmp - $GMW`
  **Output Variable:** `i_alim`
  **Tax Unit:** `tu_bsa_hr`

### 12. Function: BenCalc *(Switch: off)*
  - **Comp_perTU**: `bsa_s`
  - **Output_Var**: `bsa_s`
  - **TAX_UNIT**: `tu_bsa_hr`
  - **Comp_Cond**: `(bsa_s > 0)`

### 13. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `(IsDepChild#1) & (nAdultsInTu#1 = 1) & (yptmp#1 = 0)`
  - **Comp_perElig**: `$bsa_ChildLonePar_amt`
  - **Output_Var**: `i_MoSind`
  - **#_Level**: `tu_bsa_hr`
  - **TAX_UNIT**: `tu_individual_hr`

### 14. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `(i_bsa_cumpers > $bsa_target_count & bsayn_a = -1)  | bsayn_a = 0`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bsa_s`
  - **TAX_UNIT**: `tu_individual_hr`

### 15. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsa_elig`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsa_sort`
  - **OutputVar**: `i_bsa_cumpers`
  - **TAX_UNIT**: `tu_individual_hr`

### 16. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_target_count`: $sum_i_bsa_elig * $bsa_rate

### 17. Function: Totals *(Switch: off)*
  - **Agg**: `i_bsa_elig`
  - **Use_Weights**: `yes`
  - **Varname_Sum**: `$sum`
  - **TAX_UNIT**: `tu_individual_hr`

### 18. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_rate`: min($bsa_BCA_rate,$bsa_BTA_rate)

### 19. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_BCA_rate`: 0.786

### 20. Function: Totals *(Switch: off)*
  - **Agg**: `n/a`
  - **Use_Weights**: `n/a`
  - **Varname_Sum**: `n/a`
  - **TAX_UNIT**: `n/a`

### 21. Function: DefVar *(Switch: off)*
  - **i_bsa_bca_take**: `n/a`

### 22. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `n/a`
  - **SummingWeighted**: `n/a`
  - **SortingVar**: `n/a`
  - **OutputVar**: `n/a`
  - **TAX_UNIT**: `n/a`

### 23. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_targetBCA_amt`: n/a

### 24. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `bsa_s >= $bsa_minamt`
  - **Comp_perTU**: `1`
  - **Comp_perElig**: `i_bsa_sort`
  - **Output_Var**: `i_bsa_sort`
  - **TAX_UNIT**: `tu_individual_hr`

### 25. Function: DefVar *(Switch: off)*
  - **i_bsa_sort**: `i_bsa_rand`
  - **i_bsa_amt**: `bsa_s`
  - **i_bsa_elig**: `bsa_s > 0`
  - **i_bsa_cumexp**: `0`
  - **i_bsa_cumpers**: `0`

### 26. Function: BenCalc
  - **Comp_Cond**: `(IsParentOfDepChild)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_npatin_bsa`
  - **TAX_UNIT**: `tu_bsa_hr`

### 27. Function: BenCalc
  - **Comp_Cond**: `(i_npatin_bsa#2 < 2) & (i_psuexE#1 = 1) & (psu#1 > 0)`
  - **Comp_perTU**: `psu`
  - **#_Level**: `tu_bsa_hr`
  - **UpLim**: `$GMW`
  - **Output_Var**: `i_psuexA_bsa`
  - **TAX_UNIT**: `tu_bsa_hr`


---

## Policy: tin_hr
### 1. Function: DefConst
  **Constants Defined:**
  - `$tin_secw_rate`: 0.2
  - `$tin_rent_rate`: 0.12
  - `$tin_div_rate`: 0.12
  - `$tinta_pen_amt1`: n/a
  - `$tinta_basic_amt`: $PAB * 1
  - `$tintach_child6_amt`: $PAB * 8
  - `$tintach_child5_amt`: $PAB * 5.5
  - `$tintach_child4_amt`: $PAB * 3.6
  - `$tintach_child3_amt`: $PAB * 2.2
  - `$tintach_child2_amt`: $PAB * 1.2
  - `$tintach_child1_amt`: $PAB * 0.5
  - `$tinta_pen_amt2`: n/a
  - `$tinta_dep_thres`: $PAB * 6 / 12
  - `$tintach_child10_amt`: $PAB * 26
  - `$tintach_child9_amt`: $PAB * 20.1
  - `$tintach_child8_amt`: $PAB * 15.2
  - `$tintach_child7_amt`: $PAB * 11.2
  - `$tin_stdupthres2`: n/a
  - `$tin_stdupthres1`: $PAB * (50 / 6)
  - `$tin_stdrate3`: n/a
  - `$tin_stdrate2`: n/a
  - `$tin_stdrate1`: n/a
  - `$tin_div_thres`: n/a
  - `$tinta_dep_amt`: $PAB * 0.5
  - `$tinta_disab_amt1`: $PAB * 0.3
  - `$tin_secw_thres`: n/a
  - `$tin_lumpsum_base`: 1695#y
  - `$tin_lumpsum_rate`: 0.12
  - `$tinta_disab_amt2`: $PAB * 1
  - `$tin_rent_ded`: 0.3
  - `$tin_stdrate4`: n/a
  - `$tin_stdupthres3`: n/a

### 2. Function: DefTu
  - **Type**: `SUBGROUP`
  - **Name**: `tu_tin_hr`
  - **NoChildIfHead**: `yes`
  - **DepChildCond**: `(Default) & ((dag<=14) | (IsInEducation) | ((liwwh = 0) & (liwmy = 0))) & (il_taxableYDC#1 < $tinta_dep_thres)`
  - **Members**: `Partner & OwnDepChild & LooseDepChild & DepRelative`
  - **PartnerCond**: `(Default) & (IsMarried)`
  - **HeadDefInc**: `il_taxableY`
  - **NoChildIfPartner**: `yes`
  - **DepRelativeCond**: `!(IsHeadOfTu) & !(IsDepChild) & ((IsPartner) | (IsParent) | (IsDepChild#2)) & (il_taxableYDR#1 < $tinta_dep_thres)`
  - **#_Level**: `tu_tin_broad_hr`

### 3. Function: BenCalc
  - **Comp_Cond**: `(nDepChildrenInTu#1 = 8)`
  - **Comp_perTU**: `$tintach_child8_amt`
  - **Output_Var**: `i_tintacha`
  - **TAX_UNIT**: `tu_individual_hr`
  - **#_Level**: `tu_tin_hr`

### 4. Function: BenCalc
  - **Comp_Cond**: `(IsDepRelative) & (nPersInUnit > 1)`
  - **Comp_perElig**: `$tinta_dep_amt`
  - **Output_Var**: `tintadp_s`
  - **TAX_UNIT**: `tu_tin_hr`

### 5. Function: BenCalc
  - **Comp_Cond**: `(IsDisabled) | (bdi > 0)`
  - **Comp_perTU**: `$tinta_disab_amt1`
  - **Output_Var**: `tintadb_s`
  - **TAX_UNIT**: `tu_tin_hr`

### 6. Function: ArithOp
  **Formula:** `i_gtstotinc - (i_gtsbasall + tintach_s + tintadp_s + tintadb_s)`
  **Output Variable:** `i_gtsbase`
  **Tax Unit:** `tu_individual_hr`

### 7. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_hr`
  - **Output Variable:** `i_gtstax`
    - Band: Rate=`i_pitrat2`, Limit=``

### 8. Function: BenCalc
  - **TAX_UNIT**: `tu_individual_hr`
  - **Comp_perElig**: `i_ysecwps * i_pitrat1`
  - **Comp_Cond**: `(i_ysecwps > 0)`
  - **Output_Var**: `i_tinysecw`

### 9. Function: DefVar
  - **i_gtsmss**: `0`
  - **i_tinISS**: `0`
  - **i_pemy**: `0`
  - **i_penps**: `0`
  - **i_yemps**: `0`
  - **i_ysebsps**: `0`
  - **i_ysecwps**: `0`
  - **i_penpsav**: `0`
  - **i_yempsav**: `0`
  - **i_tintaPE**: `0`
  - **i_tintbPE**: `0`
  - **i_tinPE0**: `0`
  - **i_tinPE**: `0`
  - **i_tintaEM**: `0`
  - **i_tintbEM**: `0`
  - **i_tinEM**: `0`
  - **i_gtsbasall**: `0`
  - **i_gtsbase**: `0`
  - **i_gtstax**: `0`
  - **i_tinMSS**: `0`
  - **i_gtstotinc**: `0`
  - **i_icwext**: `0`
  - **i_tinypr**: `0`
  - **i_tinyiy**: `0`
  - **i_tinysecw**: `0`
  - **i_psuexmy**: `0`
  - **i_psuexA**: `0`
  - **i_psuexE**: `0`
  - **i_npatin**: `0`
  - **i_tinY050**: `0`
  - **i_tinY075**: `0`
  - **i_tinY100**: `0`
  - **i_tintbY050**: `0`
  - **i_tintbY075**: `0`
  - **i_tintbY100**: `0`
  - **i_tintach050**: `0`
  - **i_tintach075**: `0`
  - **i_tintach100**: `0`
  - **i_tintacha**: `0`
  - **i_gtstcp**: `0`
  - **i_gtstce**: `0`
  - **i_ysels**: `0`
  - **i_tinsels**: `0`
  - **i_surtrat**: `0`
  - **i_pitrat1**: `0`
  - **i_pitrat2**: `0`
  - **i_tinsebs**: `0`
  - **i_tinse**: `0`

### 10. Function: ArithOp
  **Formula:** `ysecwre - il_tscsecwpi`
  **Output Variable:** `i_ysecwps`
  **Tax Unit:** `tu_individual_hr`

### 11. Function: ArithOp
  **Formula:** `i_yemkfbtx - il_tsceepi`
  **Output Variable:** `i_yemps`
  **Tax Unit:** `tu_individual_hr`

### 12. Function: ArithOp
  **Formula:** `(il_pentx - i_psuexA)`
  **Output Variable:** `i_penps`
  **Tax Unit:** `tu_individual_hr`

### 13. Function: ArithOp
  **Formula:** `pdimy + poamy + i_psuexmy`
  **Output Variable:** `i_pemy`
  **Tax Unit:** `tu_individual_hr`

### 14. Function: BenCalc
  - **Comp_Cond**: `(i_pemy > 0)`
  - **Comp_perTU**: `12 * i_penps / i_pemy`
  - **Output_Var**: `i_penpsav`
  - **TAX_UNIT**: `tu_individual_hr`

### 15. Function: BenCalc
  - **Comp_Cond**: `(yemmy > 0)`
  - **Comp_perTU**: `12 * i_yemps / yemmy`
  - **Output_Var**: `i_yempsav`
  - **TAX_UNIT**: `tu_individual_hr`

### 16. Function: BenCalc
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `i_tintaPE`
  - **TAX_UNIT**: `tu_individual_hr`

### 17. Function: ArithOp
  **Formula:** `i_penpsav - (i_tintaPE + tintach_s + tintadp_s + tintadb_s)`
  **Output Variable:** `i_tintbPE`
  **Tax Unit:** `tu_individual_hr`

### 18. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_hr`
  - **Output Variable:** `i_tinPE0`
    - Band: Rate=`i_pitrat2`, Limit=``

### 19. Function: ArithOp
  **Formula:** `0.5 * i_tinPE0`
  **Output Variable:** `i_tinPE`
  **Tax Unit:** `tu_individual_hr`

### 20. Function: ArithOp
  **Formula:** `i_yempsav - (tinta00_s + tintach_s + tintadp_s + tintadb_s)`
  **Output Variable:** `i_tintbEM`
  **Tax Unit:** `tu_individual_hr`

### 21. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_hr`
  - **Output Variable:** `i_tinEM`
    - Band: Rate=`i_pitrat2`, Limit=``

### 22. Function: ArithOp
  **Formula:** `tinta00_s`
  **Output Variable:** `i_gtsbasall`
  **Tax Unit:** `tu_individual_hr`

### 23. Function: ArithOp
  **Formula:** `i_penps +  i_yemps + i_ysebsps + i_ysecwps`
  **Output Variable:** `i_gtstotinc`
  **Tax Unit:** `tu_individual_hr`

### 24. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 25. Function: ArithOp
  **Formula:** `(i_tinPE * i_pemy / 12) + (i_tinEM * yemmy / 12) + i_tinypr + i_tinyiy + i_tinysecw`
  **Output Variable:** `i_tinMSS`
  **Tax Unit:** `tu_individual_hr`

### 26. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 27. Function: ArithOp
  **Formula:** `(i_gtstax - i_gtstcp - i_gtstce) + i_tinypr + i_tinyiy`
  **Output Variable:** `i_gtsmss`
  **Tax Unit:** `tu_individual_hr`

### 28. Function: BenCalc
  - **Comp_Cond**: `(ypr > 0)`
  - **Comp_perElig**: `(1 - $tin_rent_ded) * ypr * $tin_rent_rate`
  - **TAX_UNIT**: `tu_individual_hr`
  - **Output_Var**: `i_tinypr`

### 29. Function: BenCalc
  - **TAX_UNIT**: `tu_individual_hr`
  - **Comp_perElig**: `yiytx * $tin_div_rate`
  - **Comp_Cond**: `(yiy > 0)`
  - **Output_Var**: `i_tinyiy`

### 30. Function: BenCalc
  - **Comp_Cond**: `(IsParentOfDepChild)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_npatin`
  - **TAX_UNIT**: `tu_tin_hr`

### 31. Function: BenCalc
  - **Comp_Cond**: `(dag <= 18) | ((dag > 18) & (dag < 26) & (dec > 0))`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_psuexE`
  - **TAX_UNIT**: `tu_individual_hr`

### 32. Function: BenCalc
  - **Comp_Cond**: `(i_npatin#1 < 2) & (i_psuexE = 1) & (psu > 0)`
  - **Comp_perTU**: `psu`
  - **Output_Var**: `i_psuexA`
  - **TAX_UNIT**: `tu_individual_hr`
  - **#_Level**: `tu_tin_hr`

### 33. Function: BenCalc
  - **Comp_Cond**: `(i_psuexA > 0)`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_psuexmy`
  - **TAX_UNIT**: `tu_individual_hr`

### 34. Function: BenCalc
  - **Comp_Cond**: `!(IsHeadOfTu#1) & !(IsPartner#1)`
  - **Comp_perTU**: `0 * i_tintacha`
  - **Output_Var**: `i_tintach100`
  - **TAX_UNIT**: `tu_individual_hr`
  - **#_Level**: `tu_tin_hr`

### 35. Function: BenCalc
  - **Comp_Cond**: `(i_tinY050#1 < i_tinY100#1) &  (i_tinY050#1 < i_tinY075#1)`
  - **Comp_perTU**: `i_tintach050`
  - **Output_Var**: `tintach_s`
  - **TAX_UNIT**: `tu_individual_hr`
  - **#_Level**: `tu_tin_hr`

### 36. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_hr`
  - **Output Variable:** `i_tinY050`
    - Band: Rate=`i_pitrat2`, Limit=``

### 37. Function: ArithOp
  **Formula:** `il_taxableY - (tinta00_s + i_tintach050 + tintadp_s + tintadb_s)`
  **Output Variable:** `i_tintbY050`
  **Tax Unit:** `tu_individual_hr`

### 38. Function: BenCalc
  - **Comp_Cond**: `!(IsHeadOfTu#1) & !(IsPartner#1)`
  - **Comp_perTU**: `0 * i_tintacha`
  - **Output_Var**: `i_tintach050`
  - **TAX_UNIT**: `tu_individual_hr`
  - **#_Level**: `tu_tin_hr`

### 39. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_hr`
  - **Output Variable:** `i_tinY075`
    - Band: Rate=`i_pitrat2`, Limit=``

### 40. Function: ArithOp
  **Formula:** `il_taxableY - (tinta00_s + i_tintach075 + tintadp_s + tintadb_s)`
  **Output Variable:** `i_tintbY075`
  **Tax Unit:** `tu_individual_hr`

### 41. Function: BenCalc
  - **Comp_Cond**: `!(IsHeadOfTu#1) & !(IsPartner#1)`
  - **Comp_perTU**: `0 * i_tintacha`
  - **Output_Var**: `i_tintach075`
  - **TAX_UNIT**: `tu_individual_hr`
  - **#_Level**: `tu_tin_hr`

### 42. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_hr`
  - **Output Variable:** `i_tinY100`
    - Band: Rate=`i_pitrat2`, Limit=``

### 43. Function: ArithOp
  **Formula:** `il_taxableY - (tinta00_s + i_tintach100 + tintadp_s + tintadb_s)`
  **Output Variable:** `i_tintbY100`
  **Tax Unit:** `tu_individual_hr`

### 44. Function: BenCalc
  - **Comp_Cond**: `(i_penps > 0) & (i_gtstotinc > 0)`
  - **Comp_perTU**: `0.5 * (i_penps / i_gtstotinc) * i_gtstax`
  - **Output_Var**: `i_gtstcp`
  - **TAX_UNIT**: `tu_individual_hr`

### 45. Function: BenCalc
  - **Comp_Cond**: `(i_yemps > 0) & (i_gtstotinc > 0) & (dag >= 26) & (dag <= 30)`
  - **Comp_perTU**: `0.5*(i_yemps/i_gtstotinc)*min(i_gtstax,i_pitrat1*($tin_stdupthres1+i_icwext))`
  - **Output_Var**: `i_gtstce`
  - **TAX_UNIT**: `tu_individual_hr`

### 46. Function: BenCalc
  - **Comp_Cond**: `(i_sepA = 1) & (ysebsre > 0)`
  - **Comp_perTU**: `ysebsre - il_sicsebs`
  - **Output_Var**: `i_ysebsps`
  - **LowLim**: `0`
  - **TAX_UNIT**: `tu_individual_hr`

### 47. Function: BenCalc
  - **Comp_Cond**: `(i_tradB = 1)`
  - **Comp_perTU**: `$tin_lumpsum_base`
  - **Output_Var**: `i_ysels`
  - **TAX_UNIT**: `tu_individual_hr`

### 48. Function: ArithOp
  **Formula:** `i_ysels * $tin_lumpsum_rate`
  **Output Variable:** `i_tinsels`
  **Tax Unit:** `tu_individual_hr`

### 49. Function: ArithOp
  **Formula:** `i_gtsmss + i_tinsels`
  **Output Variable:** `tin_s`
  **Tax Unit:** `tu_individual_hr`

### 50. Function: DefConst
  **Constants Defined:**
  - `$tmu_rate1`: n/a
  - `$tmu_rate2`: n/a
  - `$tmu_rate3`: n/a
  - `$tin_stdrate11`: 0.224
  - `$tin_stdrate12`: 0.199
  - `$tin_stdrate13`: 0.200
  - `$tin_stdrate21`: 0.324
  - `$tin_stdrate22`: 0.299
  - `$tin_stdrate23`: 0.299

### 51. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 52. Function: ArithOp
  **Formula:** `$tinta_basic_amt`
  **Output Variable:** `tinta00_s`
  **Tax Unit:** `tu_individual_hr`

### 53. Function: BenCalc
  - **Comp_Cond**: `(drgru = 1)`
  - **Comp_perTU**: `$tin_stdrate13`
  - **Output_Var**: `i_pitrat1`
  - **TAX_UNIT**: `tu_individual_hr`

### 54. Function: BenCalc
  - **Comp_Cond**: `(drgru = 1)`
  - **Comp_perTU**: `$tin_stdrate23`
  - **Output_Var**: `i_pitrat2`
  - **TAX_UNIT**: `tu_individual_hr`

### 55. Function: BenCalc
  - **Comp_Cond**: `(i_gtstotinc > 0)`
  - **Comp_perTU**: `i_gtstax * i_ysebsps / i_gtstotinc`
  - **Output_Var**: `i_tinsebs`
  - **TAX_UNIT**: `tu_individual_hr`

### 56. Function: ArithOp
  **Formula:** `i_tinsels + i_tinsebs`
  **Output Variable:** `i_tinse`
  **Tax Unit:** `tu_individual_hr`


---

## Policy: tscct_hr
### 1. Function: ArithOp
  **Formula:** `i_csic1 + i_csic2a + i_csic2b + i_csic3 + i_csic5`
  **Output Variable:** `tscct_s`
  **Tax Unit:** `tu_individual_hr`

### 2. Function: DefVar
  - **i_csic1**: `0`
  - **i_csic2a**: `0`
  - **i_csic2b**: `0`
  - **i_csic3**: `0`
  - **i_csic5**: `0`

### 3. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** `n/a`
    - Band: Rate=`n/a`, Limit=``

### 4. Function: BenCalc
  - **Comp_Cond**: `((i_bfamamy > 0) | (i_bfaplmy > 0)) & (i_dag < 40)`
  - **Comp_perTU**: `(0.38 * $AGWPY) * $tscct00_rate * (i_bfamamy + i_bfaplmy) / 12`
  - **Output_Var**: `i_csic1`
  - **TAX_UNIT**: `tu_individual_hr`

### 5. Function: DefConst
  **Constants Defined:**
  - `$tscct00_rate`: 0.05
  - `$tscct01_rate`: 0.05
  - `$tscct02_rate`: 0.01

### 6. Function: BenCalc
  - **Comp_Cond**: `(lunmy > 0) & (lowas = 1)`
  - **Comp_perTU**: `(0.38 * $AGWPY) * $tscct01_rate * lunmy / 12`
  - **Output_Var**: `i_csic2b`
  - **TAX_UNIT**: `tu_individual_hr`

### 7. Function: BenCalc
  - **Comp_Cond**: `(lunmy > 0) & (lowas = 1) & (i_dag < 40)`
  - **Comp_perTU**: `(0.38 * $AGWPY) * $tscct00_rate * lunmy / 12`
  - **Output_Var**: `i_csic2a`
  - **TAX_UNIT**: `tu_individual_hr`

### 8. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: bmanc_hr
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(IsHeadOfTu#1) & (dgn = 0) & (IsParentOfDepChild#1) & (nDepChInTu#1 > 0) & (lemmy = 0) & (i_bmelse = 0) & (bfama_s + bfapl_s = 0)`
  - **Tax Unit:** `tu_individual_hr`

### 2. Function: BenCalc
  - **Comp_Cond**: `(i_thirdch = 0) & (i_twins = 0) & (i_minage = 1)`
  - **Comp_perElig**: `i_mindmb - 1`
  - **Output_Var**: `i_bmancmy`
  - **TAX_UNIT**: `tu_individual_hr`
  - **Who_Must_Be_Elig**: `one`

### 3. Function: DefVar
  - **i_bmancmy**: `0`

### 4. Function: ArithOp
  **Formula:** `$bmanc_amt * i_bmancmy / 12`
  **Output Variable:** `bmanc_s`
  **Tax Unit:** `tu_individual_hr`


---

## Policy: bfaba_hr
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(IsHeadOfTu#1) & (IsParentOfDepChild#1) & (nDepChInTu#1 > 0)`
  - **Tax Unit:** `tu_individual_hr`

### 2. Function: ArithOp
  **Formula:** `$bfaba_rate * nDepChildrenInTu#1`
  **Output Variable:** `bfaba_s`
  **Tax Unit:** `tu_individual_hr`

### 3. Function: DefConst
  **Constants Defined:**
  - `$bfaba_rate`: $BUB * 1.4 / 12


---

## Policy: bch_hr
### 1. Function: DefTu
  - **Type**: `HH`
  - **Name**: `tu_bch_hr`
  - **DepChildCond**: `(dms = 1) & (((dag <= 14) | (dag = 15) & (dec = 2)) | ((dag >= 15) & (dag <= 19) & ((dec = 3) | (dec = 4))) | ((dag <= 21) & ((IsDisabled) | (bdi > 0))))`

### 2. Function: DefConst
  **Constants Defined:**
  - `$bch_thres1`: $BUB * 0.2
  - `$bch_thres2`: $BUB * 0.4
  - `$bch_thres3`: $BUB * 0.6
  - `$bch_rate3`: $BUB * 0.11
  - `$bch_rate2`: $BUB * 0.125
  - `$bch_rate1`: $BUB * 0.14
  - `$bch_suppl_amt2`: 132.72#m
  - `$bch_suppl_amt1`: 66.36#m
  - `$bch_thres4`: $BUB * 1.0
  - `$bch_thres5`: $BUB * 1.4
  - `$bch_rate4`: $BUB * 0.09
  - `$bch_rate5`: $BUB * 0.07
  - `$empnr`: 0.917
  - `$bch_suppl_rate2`: 0.25
  - `$bch_suppl_rate1`: 0.15

### 3. Function: DefIl
  - **Name**: `il_bch`
  - **bfapl_s**: `+`
  - **ysebsre**: `+`
  - **yemtx**: `+`
  - **ils_pen**: `+`
  - **bfama_s**: `+`
  - **bhl**: `+`
  - **yiy**: `+`
  - **ysecwre**: `+`
  - **ypp**: `+`
  - **ypr**: `+`
  - **bmanc_s**: `+`
  - **ils_sicee**: `-`
  - **tmu_s**: `n/a`
  - **tin_s**: `-`
  - **ils_sicse**: `-`
  - **ysv**: `+`
  - **bunct_s**: `+`
  - **ils_sicot**: `-`
  - **bwkmc_s**: `n/a`
  - **kfbtx**: `+`
  - **ymc**: `+`

### 4. Function: ArithOp
  **Formula:** `(il_bch * $empnr) / nPersInUnit`
  **Output Variable:** `i_bchYpHM`
  **Tax Unit:** `tu_bch_hr`

### 5. Function: DefVar
  - **i_bchYpHM**: `0`
  - **i_npadis**: `0`
  - **i_nchdis**: `0`
  - **i_bchbasic**: `0`
  - **i_bchprons**: `0`
  - **i_bchothers**: `0`

### 6. Function: BenCalc
  - **Comp_Cond**: `(i_bchYpHM > $bch_thres4) & (i_bchYpHM <= $bch_thres5)`
  - **Comp_perTU**: `$bch_rate5 * nDepChildrenInTu`
  - **Output_Var**: `bch_s`
  - **TAX_UNIT**: `tu_bch_hr`
  - **Result_Var**: `i_bchbasic`

### 7. Function: BenCalc
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Add_Var**: `bch_s`
  - **TAX_UNIT**: `tu_bch_hr`
  - **Result_Var**: `i_bchothers`

### 8. Function: BenCalc
  - **Comp_Cond**: `(IsParentOfDepChild) & ((IsDisabled) | (bdi#1 > 0))`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_npadis`
  - **TAX_UNIT**: `tu_bch_hr`
  - **#_Level**: `tu_individual_hr`

### 9. Function: BenCalc
  - **Comp_Cond**: `(IsDepChild) & ((IsDisabled) | (bdi#1 > 0))`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_nchdis`
  - **TAX_UNIT**: `tu_bch_hr`
  - **#_Level**: `tu_individual_hr`

### 10. Function: BenCalc
  - **Output_Add_Var**: `bch_s`
  - **TAX_UNIT**: `tu_bch_hr`
  - **Comp_perTU**: `$bch_suppl_amt1`
  - **Comp_Cond**: `(nDepChildrenInTu = 3) & (i_bchbasic > 0)`
  - **Result_Var**: `i_bchprons`


---

## Policy: output_std_hr
### 1. Function: DefOutput
  - **TAX_UNIT**: `tu_individual_hr`
  - **VarGroup**: `id*`
  - **ILGroup**: `ils_*`
  - **UnitInfo_TU**: `n/a`
  - **UnitInfo_Id**: `n/a`
  - **File**: `HR_2025_std`


---

## Policy: output_std_hh_hr *(Switch: off)*
### 1. Function: DefOutput
  - **File**: `HR_2025_std_hh`
  - **TAX_UNIT**: `tu_hh_oecd_co`
  - **Var**: `idhh`
  - **ILGroup**: `ils_*`


---

## Policy: InitVars_hr
### 1. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `bfama_s`
  **Tax Unit:** `tu_individual_hr`

### 2. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `bfapl_s`
  **Tax Unit:** `tu_individual_hr`

### 3. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `bmanc_s`
  **Tax Unit:** `tu_individual_hr`

### 4. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `bunct_s`
  **Tax Unit:** `tu_individual_hr`


---

## Policy: tmu_hr *(Switch: n/a)*
### 1. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 2. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 3. Function: DefVar *(Switch: n/a)*
  - **i_tmuMSS**: `n/a`
  - **i_tmuse**: `n/a`
  - **i_tmuPE**: `n/a`

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


---

## Policy: tin_hr

---

## Policy: ildef_hr
### 1. Function: DefIl
  - **Name**: `il_tsceepi`
  - **tsceepi02_s**: `+`
  - **tsceepi01_s**: `+`
  - **tsceepi00_s**: `+`

### 2. Function: DefIl
  - **Name**: `il_tscsebupi`
  - **tscsebupi02_s**: `+`
  - **tscsebupi01_s**: `+`
  - **tscsebupi00_s**: `+`

### 3. Function: DefIl
  - **Name**: `il_tscsecwpi`
  - **tscsecwpi02_s**: `+`
  - **tscsecwpi01_s**: `+`
  - **tscsecwpi00_s**: `+`

### 4. Function: DefIl
  - **Name**: `il_sicsebs`
  - **tscsebusi00_s**: `+`
  - **tscsebusi01_s**: `n/a`
  - **tscsebupi00_s**: `+`
  - **tscsebupi01_s**: `+`
  - **tscsebupi02_s**: `+`
  - **tscseui_s**: `n/a`

### 5. Function: DefIl
  - **Name**: `il_sicsecw`
  - **tscsecwpi00_s**: `+`
  - **tscsecwpi01_s**: `+`
  - **tscsecwpi02_s**: `+`
  - **tscsecwsi00_s**: `+`

### 6. Function: DefIl
  - **Name**: `il_taxableY`
  - **ils_pen**: `+`
  - **ysebsre**: `+`
  - **yem**: `+`
  - **ysecwre**: `+`
  - **ypr**: `n/a`
  - **yiy**: `n/a`
  - **il_tscsecwpi**: `-`
  - **il_sicsebs**: `-`
  - **il_tsceepi**: `-`
  - **tscbesi_s**: `n/a`

### 7. Function: DefIl
  - **Name**: `il_taxableYDR`
  - **il_taxableY**: `+`
  - **bhl**: `+`
  - **bed**: `n/a`
  - **ypp**: `+`
  - **bmanc_s**: `+`
  - **bfapl_s**: `+`
  - **bfama_s**: `+`
  - **bunct_s**: `+`
  - **yiy**: `+`
  - **ypr**: `+`

### 8. Function: DefIl
  - **Name**: `il_taxableYDC`
  - **il_taxableYDR**: `+`
  - **psu**: `-`

### 9. Function: DefIl
  - **Name**: `il_pentx`
  - **poatx**: `+`
  - **pditx**: `+`
  - **psutx**: `+`


---

## Policy: Def_hr
### 1. Function: UpdateTu
  - **Name**: `tu_tin_hr`


---

## Policy: bhout_hr
### 1. Function: DefConst
  **Constants Defined:**
  - `$bhout_max_amt`: 70#m

### 2. Function: DefVar
  - **i_ambdi**: `0`
  - **i_bdipda**: `0`

### 3. Function: BenCalc
  - **Comp_Cond**: `(bdimy > 0)`
  - **Comp_perTU**: `12 * bdi / bdimy`
  - **Output_Var**: `i_ambdi`
  - **TAX_UNIT**: `tu_individual_hr`

### 4. Function: BenCalc
  - **Comp_Cond**: `(i_ambdi >= 200#m)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_bdipda`
  - **TAX_UNIT**: `tu_individual_hr`

### 5. Function: BenCalc
  - **Comp_Cond**: `(bsa_s > 0) | (i_bdipda > 0) | (boamt_s > 0)`
  - **Comp_perTU**: `min($bhout_max_amt, xhcot)`
  - **Output_Var**: `bhout_s`
  - **TAX_UNIT**: `tu_household_hr`


---

## Policy: bfama_hr
### 1. Function: DefVar
  - **i_child3**: `0`
  - **i_minage**: `0`
  - **i_minagechild**: `0`
  - **i_IncBaseSE**: `0`
  - **i_BfmBeeR**: `0`
  - **i_tinSE**: `0`
  - **i_sicSE**: `0`
  - **i_BfmBse**: `0`
  - **i_BfmBeeN**: `0`
  - **i_yempr**: `0`
  - **i_tscempr**: `0`
  - **i_tinempr**: `0`
  - **i_bmelse**: `0`
  - **i_BfmBee**: `0`
  - **i_bfanch01**: `0`
  - **i_bfanch**: `0`
  - **i_bfanch21**: `0`
  - **i_bfanch11**: `0`
  - **i_mindmbchild**: `0`
  - **i_bfanch31**: `0`
  - **i_twins**: `0`
  - **i_thirdch**: `0`
  - **i_mindmb**: `0`
  - **i_triplets**: `0`
  - **i_bfamamy0**: `0`
  - **i_bfama**: `0`
  - **i_bfamamy**: `0`
  - **i_bfanch32**: `0`
  - **i_bfanch22**: `0`
  - **i_bfanch12**: `0`
  - **i_bfanch02**: `0`
  - **i_bfanch34**: `0`
  - **i_bfanch33**: `0`
  - **i_bfanch24**: `0`
  - **i_bfanch23**: `0`
  - **i_bfanch14**: `0`
  - **i_bfanch13**: `0`
  - **i_bfanch04**: `0`
  - **i_bfanch03**: `0`
  - **i_dagalt**: `0`
  - **i_dmb0**: `0`
  - **i_yemre**: `0`
  - **i_tscemre**: `0`
  - **i_tinemre**: `0`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(HasMinValInTu#1) & (IsDepChild)`
  - **Tax Unit:** `tu_bfapl_hr`

### 3. Function: ArithOp
  **Formula:** `dag`
  **Output Variable:** `i_minagechild`
  **Tax Unit:** `tu_individual_hr`

### 4. Function: BenCalc
  - **Comp_Cond**: `(i_twins = 0) & (i_triplets = 1)`
  - **Comp_perTU**: `i_minagechild / 3`
  - **Output_Var**: `i_minage`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 5. Function: ArithOp
  **Formula:** `i_IncBaseSE - i_sicSE - i_tinSE`
  **Output Variable:** `i_BfmBse`
  **Tax Unit:** `tu_individual_hr`

### 6. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_hr`
  - **Output Variable:** `i_tinSE`
    - Band: Rate=`i_pitrat2`, Limit=``

### 7. Function: ArithOp
  **Formula:** `($tsceepi00_rate + $tscersi00_rate) * i_IncBaseSE`
  **Output Variable:** `i_sicSE`
  **Tax Unit:** `tu_individual_hr`

### 8. Function: BenCalc
  - **Comp_Cond**: `(i_pro1A = 1)`
  - **Comp_perTU**: `$AGWPY * $tscsebusi00_pro1A_base`
  - **Output_Var**: `i_IncBaseSE`
  - **TAX_UNIT**: `tu_individual_hr`

### 9. Function: ArithOp
  **Formula:** `i_yemre - i_tscemre - i_tinemre`
  **Output Variable:** `i_BfmBeeR`
  **Tax Unit:** `tu_individual_hr`

### 10. Function: ArithOp
  **Formula:** `yivwg * 174`
  **Output Variable:** `i_yempr`
  **Tax Unit:** `tu_individual_hr`

### 11. Function: ArithOp
  **Formula:** `$tsceepi00_rate * i_yempr`
  **Output Variable:** `i_tscempr`
  **Tax Unit:** `tu_individual_hr`

### 12. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_hr`
  - **Output Variable:** `i_tinempr`
    - Band: Rate=`i_pitrat2`, Limit=``

### 13. Function: ArithOp
  **Formula:** `i_yempr - i_tscempr - i_tinempr`
  **Output Variable:** `i_BfmBeeN`
  **Tax Unit:** `tu_individual_hr`

### 14. Function: BenCalc
  - **Comp_Cond**: `(i_farmA = 1) | (i_pro1A = 1) | (i_pro2A = 1) | (i_tradA = 1) | (i_tradB = 1)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_bmelse`
  - **TAX_UNIT**: `tu_individual_hr`

### 15. Function: BenCalc
  - **Comp_Cond**: `(yemmy = 0)`
  - **Comp_perTU**: `i_BfmBeeN`
  - **Output_Var**: `i_BfmBee`
  - **TAX_UNIT**: `tu_individual_hr`

### 16. Function: BenCalc
  - **Comp_Cond**: `(IsOwnChild) | (IsLooseDepChild)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch`
  - **TAX_UNIT**: `tu_bfapl_broad_hr`

### 17. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag<=0) & (dmb >= 1) & (dmb <= 3)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch01`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 18. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag = 1) & (dmb >= 1) & (dmb <= 3)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch11`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 19. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag = 2) & (dmb >= 1) & (dmb <= 3)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch21`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 20. Function: ArithOp
  **Formula:** `dmb`
  **Output Variable:** `i_mindmbchild`
  **Tax Unit:** `tu_individual_hr`

### 21. Function: BenCalc
  - **Comp_Cond**: `(i_bfanch01 = 2) | (i_bfanch02 = 2) | (i_bfanch03 = 2) | (i_bfanch04 = 2) | (i_bfanch11 = 2) | (i_bfanch12 = 2) | (i_bfanch13 = 2) | (i_bfanch14 = 2) | (i_bfanch21 = 2) | (i_bfanch22 = 2) | (i_bfanch23 = 2) | (i_bfanch24 = 2) | (i_bfanch31 = 2) | (i_bfanch32 = 2) | (i_bfanch33 = 2) | (i_bfanch34 = 2)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_twins`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 22. Function: BenCalc
  - **Comp_Cond**: `(i_bfanch > 2)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_thirdch`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 23. Function: BenCalc
  - **Comp_Cond**: `(i_twins = 0) & (i_triplets = 1)`
  - **Comp_perTU**: `i_mindmbchild / 3`
  - **Output_Var**: `i_mindmb`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 24. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag = 3) & (dmb >= 1) & (dmb <= 3)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch31`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 25. Function: BenCalc
  - **Comp_Cond**: `(i_bfanch01 = 3) | (i_bfanch02 = 3) | (i_bfanch03 = 3) | (i_bfanch04 = 3) | (i_bfanch11 = 3) | (i_bfanch12 = 3) | (i_bfanch13 = 3) | (i_bfanch14 = 3) | (i_bfanch21 = 3) | (i_bfanch22 = 3) | (i_bfanch23 = 3) | (i_bfanch24 = 3) | (i_bfanch31 = 3) | (i_bfanch32 = 3) | (i_bfanch33 = 3) | (i_bfanch34 = 3)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_triplets`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 26. Function: ArithOp
  **Formula:** `i_bfama * i_bfamamy / 12`
  **Output Variable:** `bfama_s`
  **Tax Unit:** `tu_individual_hr`

### 27. Function: ArithOp
  **Formula:** `i_bfamamy0`
  **Output Variable:** `i_bfamamy`
  **Tax Unit:** `tu_individual_hr`

### 28. Function: BenCalc
  - **Comp_Cond**: `((lemmy > 0) | (les = 3)) & (liwwh >= 12)`
  - **Comp_perElig**: `i_BfmBee`
  - **Output_Var**: `i_bfama`
  - **TAX_UNIT**: `tu_individual_hr`
  - **Who_Must_Be_Elig**: `one`
  - **LowLim**: `$bfama_min_amt`

### 29. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(IsHeadOfTu#1) & (dgn = 0) & (IsParentOfDepChild#1) & (nDepChInTu#1 > 0) & ((lemmy > 0) | (les = 3) | (i_bmelse = 1))`
  - **Tax Unit:** `tu_individual_hr`

### 30. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag<=0) & (dmb >= 4) & (dmb <= 6)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch02`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 31. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag = 1) & (dmb >= 4) & (dmb <= 6)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch12`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 32. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag = 2) & (dmb >= 4) & (dmb <= 6)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch22`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 33. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag = 3) & (dmb >= 4) & (dmb <= 6)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch32`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 34. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag<=0) & (dmb >= 7) & (dmb <= 9)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch03`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 35. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag<=0) & (dmb >= 10) & (dmb <= 12)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch04`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 36. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag = 1) & (dmb >= 10) & (dmb <= 12)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch14`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 37. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag = 1) & (dmb >= 7) & (dmb <= 9)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch13`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 38. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag = 2) & (dmb >= 10) & (dmb <= 12)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch24`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 39. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag = 2) & (dmb >= 7) & (dmb <= 9)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch23`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 40. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag = 3) & (dmb >= 10) & (dmb <= 12)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch34`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 41. Function: BenCalc
  - **Comp_Cond**: `((IsOwnDepChild) | (IsLooseDepChild)) & (dag = 3) & (dmb >= 7) & (dmb <= 9)`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_bfanch33`
  - **TAX_UNIT**: `tu_bfapl_hr`

### 42. Function: ArithOp
  **Formula:** `100 * dag + dmb`
  **Output Variable:** `i_dagalt`
  **Tax Unit:** `tu_individual_hr`

### 43. Function: DefConst
  **Constants Defined:**
  - `$bfapl_min_amt`: $BUB * 1.59
  - `$bfapl_max_amt`: $BUB * 6.8
  - `$bfama_min_amt`: $BUB * 1.59
  - `$bfafh_min_amt`: $BUB * 1.59
  - `$bmanc_amt`: $BUB * 1.14

### 44. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 45. Function: BenCalc
  - **Comp_Cond**: `(yemmy > 0)`
  - **Comp_perTU**: `12 * (yemtx + kfbtx) / yemmy`
  - **Output_Var**: `i_yemre`
  - **TAX_UNIT**: `tu_individual_hr`

### 46. Function: ArithOp
  **Formula:** `$tsceepi00_rate * i_yemre`
  **Output Variable:** `i_tscemre`
  **Tax Unit:** `tu_individual_hr`

### 47. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_hr`
  - **Output Variable:** `i_tinemre`
    - Band: Rate=`n/a`, Limit=``

### 48. Function: BenCalc
  - **Comp_Cond**: `(i_bfama > 0) & (i_minage = 0) & ((i_mindmb >= 1) & (i_mindmb <= 7))`
  - **Comp_perElig**: `0`
  - **Output_Var**: `i_bfamamy0`
  - **TAX_UNIT**: `tu_individual_hr`


---

## Policy: bfapl_hr
### 1. Function: DefVar
  - **i_bfapl**: `0`
  - **i_bfaplmy0**: `n/a`
  - **i_bfaplmy**: `0`
  - **i_bfaplmo**: `0`
  - **i_bfaplfh**: `0`
  - **i_bfaplmyA0**: `0`
  - **i_bfaplmyA**: `0`
  - **i_bfaplmomyA0**: `0`
  - **i_bfaplmomyA**: `0`
  - **i_bfaplfhmyA0**: `0`
  - **i_bfaplfhmyA**: `0`
  - **i_bfaplmomyB0**: `0`
  - **i_bfaplmomyB**: `0`
  - **i_bfaplA**: `0`
  - **i_bfaplmoA**: `0`
  - **i_bfaplfhA**: `0`
  - **i_bfaplmoB**: `0`
  - **i_bfapl_fhm**: `0`
  - **i_bfapl_fhp**: `0`
  - **i_bfaplfhA2**: `0`
  - **i_bfaplfhA4**: `0`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(IsHeadOfTu#1) & (dgn = 0) & (IsParentOfDepChild#1) & (nDepChInTu#1 > 0) & ((lemmy > 0) | (les = 3) | (i_bmelse = 1))`
  - **Tax Unit:** `tu_individual_hr`

### 3. Function: DefConst
  **Constants Defined:**
  - `$bfapl_randthres1`: 0.06
  - `$bfapl_randthres2`: 0.15

### 4. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(liwwh < 12)`
  - **Comp_perElig**: `$bfapl_min_amt`
  - **LowLim**: `$bfapl_min_amt`
  - **UpLim**: `$bfapl_max_amt`
  - **Output_Var**: `i_bfaplmo`
  - **TAX_UNIT**: `tu_individual_hr`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(IsPartnerOfHeadOfTu#1) & (dgn = 1) & (IsParentOfDepChild#1) & (nDepChInTu#1 > 0) & ((lemmy > 0) | (les = 3) | (i_bmelse = 1)) & (i_bfaplmo#1 > 0)`
  - **Tax Unit:** `tu_individual_hr`

### 6. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(liwwh < 12)`
  - **Comp_perElig**: `$bfapl_min_amt`
  - **LowLim**: `$bfapl_min_amt`
  - **UpLim**: `$bfapl_max_amt`
  - **Output_Var**: `i_bfaplfh`
  - **TAX_UNIT**: `tu_individual_hr`

### 7. Function: BenCalc
  - **Comp_Cond**: `(i_bfaplfh > 0)`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bfapl_fhm`
  - **TAX_UNIT**: `tu_individual_hr`

### 8. Function: BenCalc
  - **Comp_Cond**: `(i_bfapl_fhm > 0)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_bfapl_fhp`
  - **TAX_UNIT**: `tu_individual_hr`

### 9. Function: BenCalc
  - **Comp_Cond**: `(i_bfaplmo > 0) & (i_minage = 1) & (i_mindmb >= 7)`
  - **Comp_perElig**: `6 + 2 * i_bfapl_fhp#1`
  - **#_Level**: `tu_bfapl_hr`
  - **Output_Var**: `i_bfaplmyA0`
  - **TAX_UNIT**: `tu_individual_hr`

### 10. Function: ArithOp
  **Formula:** `round((1 - i_bfapl_fhm#1 / 8) * i_bfaplmyA0)`
  **Output Variable:** `i_bfaplmomyA0`
  **Tax Unit:** `tu_individual_hr`

### 11. Function: ArithOp
  **Formula:** `min(i_bfaplmomyA0, 12 - i_bfamamy)`
  **Output Variable:** `i_bfaplmomyA`
  **Tax Unit:** `tu_individual_hr`

### 12. Function: BenCalc
  - **Comp_Cond**: `(i_bfapl_fhp = 1)`
  - **Comp_perElig**: `i_bfaplmyA0#1 - i_bfaplmomyA0#1`
  - **#_Level**: `tu_bfapl_hr`
  - **Output_Var**: `i_bfaplfhmyA0`
  - **TAX_UNIT**: `tu_individual_hr`

### 13. Function: ArithOp
  **Formula:** `i_bfaplfhmyA0`
  **Output Variable:** `i_bfaplfhmyA`
  **Tax Unit:** `tu_individual_hr`

### 14. Function: BenCalc
  - **Comp_Cond**: `(i_bfaplmo > 0) & ((i_thirdch = 1) | (i_twins = 1)) & (i_minage = 3)`
  - **Comp_perElig**: `i_mindmb - 1`
  - **#_Level**: `tu_bfapl_hr`
  - **Output_Var**: `i_bfaplmomyB0`
  - **TAX_UNIT**: `tu_individual_hr`

### 15. Function: ArithOp
  **Formula:** `min(i_bfaplmomyB0, 12  - i_bfamamy - i_bfaplmomyA)`
  **Output Variable:** `i_bfaplmomyB`
  **Tax Unit:** `tu_individual_hr`

### 16. Function: BenCalc
  - **Comp_Cond**: `(i_bfaplmo > 0) & (i_bfaplmomyA > 0)`
  - **Comp_perElig**: `i_bfaplmo * i_bfaplmomyA`
  - **Output_Var**: `i_bfaplmoA`
  - **TAX_UNIT**: `tu_individual_hr`

### 17. Function: BenCalc
  - **Comp_Cond**: `(i_bfaplfh > 0) & (i_bfaplfhmyA > 0)`
  - **Comp_perElig**: `i_bfaplfh * i_bfaplfhmyA`
  - **Output_Var**: `i_bfaplfhA`
  - **TAX_UNIT**: `tu_individual_hr`

### 18. Function: BenCalc
  - **Comp_Cond**: `(i_bfaplmo > 0) & (i_bfaplmomyB > 0)`
  - **Comp_perElig**: `$bfapl_min_amt * i_bfaplmomyB`
  - **Output_Var**: `i_bfaplmoB`
  - **TAX_UNIT**: `tu_individual_hr`

### 19. Function: ArithOp
  **Formula:** `(i_bfaplmoA + i_bfaplfhA + i_bfaplmoB) / 12`
  **Output Variable:** `bfapl_s`
  **Tax Unit:** `tu_individual_hr`

### 20. Function: ArithOp
  **Formula:** `i_bfaplmomyA + i_bfaplfhmyA + i_bfaplmomyB`
  **Output Variable:** `i_bfaplmy`
  **Tax Unit:** `tu_individual_hr`

### 21. Function: ArithOp
  **Formula:** `(i_bfaplmoA + i_bfaplfhA) / 12`
  **Output Variable:** `i_bfaplA`
  **Tax Unit:** `tu_individual_hr`

### 22. Function: BenCalc
  - **Comp_Cond**: `(i_bfaplfhA > 0) & (i_bfapl_fhm = 2)`
  - **Comp_perTU**: `i_bfaplfhA`
  - **Output_Var**: `i_bfaplfhA2`
  - **TAX_UNIT**: `tu_individual_hr`

### 23. Function: BenCalc
  - **Comp_Cond**: `(i_bfaplfhA > 0) & (i_bfapl_fhm = 4)`
  - **Comp_perTU**: `i_bfaplfhA`
  - **Output_Var**: `i_bfaplfhA4`
  - **TAX_UNIT**: `tu_individual_hr`


---

## Policy: ilsUDBdef_hr
### 1. Function: DefIl
  - **Name**: `ils_udb_boa`
  - **poa**: `+`
  - **boa**: `+`

### 2. Function: DefIl
  - **Name**: `ils_udb_bsu`
  - **psu**: `+`
  - **bsu**: `+`

### 3. Function: DefIl
  - **Name**: `ils_udb_bdi`
  - **pdi**: `+`
  - **bdi**: `+`

### 4. Function: DefIl
  - **Name**: `ils_udb_bun`
  - **bunct_s**: `+`
  - **bunot**: `+`
  - **bwkmc_s**: `n/a`

### 5. Function: DefIl
  - **Name**: `ils_udb_bhl`
  - **bhl**: `+`

### 6. Function: DefIl
  - **Name**: `ils_udb_bed`
  - **bed**: `+`

### 7. Function: DefIl
  - **Name**: `ils_udb_bsa`
  - **bsa_s**: `+`
  - **bsaot**: `+`
  - **bhout_s**: `+`
  - **boamt_s**: `+`
  - **boatu00_s**: `+`
  - **buntu_s**: `n/a`
  - **bchtu_s**: `n/a`
  - **bsatu_s**: `n/a`
  - **bditu_s**: `n/a`
  - **boatu01_s**: `+`

### 8. Function: DefIl
  - **Name**: `ils_udb_bfa`
  - **bch_s**: `+`
  - **bfama_s**: `+`
  - **bmanc_s**: `+`
  - **bfapl_s**: `+`
  - **bfaba_s**: `+`
  - **bfaot**: `+`
  - **bfafh_s**: `+`

### 9. Function: DefIl
  - **Name**: `ils_udb_bho`
  - **bho**: `+`

### 10. Function: DefIl
  - **Name**: `ils_udb_yem`
  - **yemtx**: `+`
  - **yst**: `+`
  - **yemnt**: `+`
  - **ymc**: `+`

### 11. Function: DefIl
  - **Name**: `ils_udb_yse`
  - **ysebsnr**: `+`
  - **ysecwre**: `+`
  - **ysebsre**: `+`
  - **ysecwnr**: `+`

### 12. Function: DefIl
  - **Name**: `ils_udb_yiy`
  - **yiy**: `+`

### 13. Function: DefIl
  - **Name**: `ils_udb_ypp`
  - **ypp**: `+`

### 14. Function: DefIl
  - **Name**: `ils_udb_ypr`
  - **ypr**: `+`

### 15. Function: DefIl
  - **Name**: `ils_udb_yot`
  - **yot**: `+`

### 16. Function: DefIl
  - **Name**: `ils_udb_ypt`
  - **ypt**: `+`

### 17. Function: DefIl
  - **Name**: `ils_udb_xmp`
  - **xmp00**: `+`
  - **xmpam**: `+`

### 18. Function: DefIl
  - **Name**: `ils_udb_kfbcc`
  - **kfbcc**: `+`

### 19. Function: DefIl
  - **Name**: `ils_udb_tpr`
  - **tpr**: `+`

### 20. Function: DefIl
  - **Name**: `ils_udb_tis`
  - **tin_s**: `+`
  - **ils_sicse**: `+`
  - **ils_sicee**: `+`
  - **tmu_s**: `n/a`
  - **ils_sicot**: `+`

### 21. Function: DefIl
  - **Name**: `ils_udb_yds`
  - **ils_udb_yem**: `+`
  - **ils_udb_tis**: `-`
  - **ils_udb_tpr**: `-`
  - **ils_udb_xmp**: `-`
  - **ils_udb_yiy**: `+`
  - **ils_udb_kfbcc**: `+`
  - **ils_udb_yot**: `+`
  - **ils_udb_ypt**: `+`
  - **ils_udb_ypr**: `+`
  - **ils_udb_ypp**: `+`
  - **ils_udb_boa**: `+`
  - **ils_udb_bsu**: `+`
  - **ils_udb_bdi**: `+`
  - **ils_udb_bun**: `+`
  - **ils_udb_bhl**: `+`
  - **ils_udb_bed**: `+`
  - **ils_udb_bsa**: `+`
  - **ils_udb_bfa**: `+`
  - **ils_udb_bho**: `+`
  - **ils_udb_yse**: `+`


---

## Policy: random_hr
### 1. Function: RandSeed
  - **Seed**: `32156`

### 2. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_rn_sic1`
  **Tax Unit:** `tu_individual_hr`

### 3. Function: RandSeed
  - **Seed**: `25832`

### 4. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_rn_sic2`
  **Tax Unit:** `tu_individual_hr`

### 5. Function: RandSeed
  - **Seed**: `34685`

### 6. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_1`
  **Tax Unit:** `tu_individual_hr`

### 7. Function: RandSeed
  - **Seed**: `18903`

### 8. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_2`
  **Tax Unit:** `tu_individual_hr`

### 9. Function: RandSeed
  - **Seed**: `13453`

### 10. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lma1`
  **Tax Unit:** `tu_individual_hr`

### 11. Function: RandSeed
  - **Seed**: `16576`

### 12. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lma2`
  **Tax Unit:** `tu_individual_hr`

### 13. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lmamy`
  **Tax Unit:** `tu_individual_hr`

### 14. Function: RandSeed
  - **Seed**: `20345`

### 15. Function: DefVar
  - **i_mc_rand_1**: `0`
  - **i_mc_rand_2**: `0`
  - **i_mc_rand_3**: `0`
  - **i_rn_sic1**: `0`
  - **i_rn_sic2**: `0`
  - **i_lma1**: `0`
  - **i_lma2**: `0`
  - **i_lmamy**: `0`
  - **i_rn_sic3**: `0`
  - **i_rn_bfapl**: `0`
  - **i_bsa_rand**: `0`

### 16. Function: RandSeed
  - **Seed**: `18904`

### 17. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_3`
  **Tax Unit:** `tu_individual_hr`

### 18. Function: RandSeed
  - **Seed**: `82354`

### 19. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_rn_sic3`
  **Tax Unit:** `tu_individual_hr`

### 20. Function: RandSeed
  - **Seed**: `734512`

### 21. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_rn_bfapl`
  **Tax Unit:** `tu_individual_hr`

### 22. Function: RandSeed
  - **Seed**: `734515`

### 23. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_bsa_rand`
  **Tax Unit:** `tu_individual_hr`


---

## Policy: TransLMA_hr *(Switch: off)*
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy = 0) & (ysemy = 0) & (dag > 17) & (dag < 65) & (les = 5)`
  - **Tax Unit:** `tu_individual_hr`

### 2. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(deh = 5) & (dgn = 1) & (i_lma1 < $ur_dgn1_deh3_ee)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_hr`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy > 0)`
  - **Tax Unit:** `tu_individual_hr`

### 4. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(deh = 5) & (dgn = 1) & (i_lma1 < $er_dgn1_deh3_ee)`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_hr`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ysemy > 0) & (yemmy = 0)`
  - **Tax Unit:** `tu_individual_hr`

### 6. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dgn = 1 & (i_lma2 < $er_dgn1_se)`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_hr`

### 7. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lma = 1)`
  - **Tax Unit:** `tu_individual_hr`

### 8. Function: ArithOp
  **Formula:** `(yivwg * $lhw * 52/12)`
  **Output Variable:** `yem_a`
  **Tax Unit:** `tu_individual_hr`

### 9. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lma = 1) | (lma = 5)`
  - **Tax Unit:** `tu_individual_hr`

### 10. Function: ArithOp
  **Formula:** `$lhw`
  **Output Variable:** `lhw_a`
  **Tax Unit:** `tu_individual_hr`

### 11. Function: BenCalc
  - **Comp_Cond**: `(lma=2) & (ysemy > 0) & (yemmy = 0)`
  - **Comp_perTU**: `0`
  - **Output_Var**: `yemmy_a`
  - **TAX_UNIT**: `tu_individual_hr`

### 12. Function: DefConst
  **Constants Defined:**
  - `$er_dgn0_deh1_ee`: 0.00
  - `$er_dgn0_deh2_ee`: 0.00
  - `$er_dgn0_deh3_ee`: 0.00
  - `$er_dgn1_deh1_ee`: 0.00
  - `$er_dgn1_deh2_ee`: 0.00
  - `$er_dgn1_deh3_ee`: 0.00
  - `$ur_yemmy8`: 0.00
  - `$ur_dgn0_deh1_ee`: 0.00
  - `$ur_dgn0_deh2_ee`: 0.00
  - `$ur_dgn0_deh3_ee`: 0.00
  - `$ur_dgn1_deh1_ee`: 0.00
  - `$ur_dgn1_deh2_ee`: 0.00
  - `$ur_dgn1_deh3_ee`: 0.00
  - `$er_dgn0_se`: 0.00
  - `$er_dgn1_se`: 0.00
  - `$er_yemmy2`: 0.00
  - `$er_yemmy5`: 0.00
  - `$er_yemmy8`: 0.00
  - `$ur_yemmy2`: 0.00
  - `$ur_yemmy5`: 0.00
  - `Run_Cond`: GetDataIncomeYear = 2019

### 13. Function: DefVar
  - **i_lmc**: `0`

### 14. Function: DefConst
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

### 15. Function: DefConst
  **Constants Defined:**
  - `$sh_mcse_l1_dgn0`: 0
  - `$sh_mcse_l2_dgn0`: 0
  - `$sh_mcse_l3_dgn0`: 0
  - `$sh_mcse_l4_dgn0`: 0
  - `$sh_mcse_l5_dgn0`: 0
  - `$sh_mcse_l1_dgn1`: 0
  - `$sh_mcse_l2_dgn1`: 0
  - `$sh_mcse_l3_dgn1`: 0
  - `$sh_mcse_l4_dgn1`: 0
  - `$sh_mcse_l5_dgn1`: 0
  - `$sh_mcsemy_1`: 0
  - `$sh_mcsemy_2`: 0
  - `$sh_mcsemy_3`: 0
  - `$sh_mcsemy_4`: 0
  - `$sh_mcsemy_5`: 0
  - `$sh_mcsemy_6`: 0
  - `$sh_mcsemy_7`: 0
  - `$sh_mcsemy_8`: 0
  - `$sh_mcsemy_9`: 0
  - `$sh_0hours_se`: 0
  - `$sh_15hours_se`: 0
  - `$sh_45hours_se`: 0
  - `Run_Cond`: GetDataIncomeYear = 2019

### 16. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 17. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 18. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 19. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 20. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 21. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 22. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 23. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 24. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 25. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 26. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 27. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 28. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 29. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 30. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 31. Function: DefConst
  **Constants Defined:**
  - `$er_dgn0_deh1_ee`: 0.00
  - `$er_dgn0_deh2_ee`: 0.00
  - `$er_dgn0_deh3_ee`: 0.00
  - `$er_dgn1_deh1_ee`: 0.00
  - `$er_dgn1_deh2_ee`: 0.00
  - `$er_dgn1_deh3_ee`: 0.00
  - `$ur_yemmy8`: 0.00
  - `$ur_dgn0_deh1_ee`: 0.00
  - `$ur_dgn0_deh2_ee`: 0.00
  - `$ur_dgn0_deh3_ee`: 0.00
  - `$ur_dgn1_deh1_ee`: 0.00
  - `$ur_dgn1_deh2_ee`: 0.00
  - `$ur_dgn1_deh3_ee`: 0.00
  - `$er_dgn0_se`: 0.00
  - `$er_dgn1_se`: 0.00
  - `$er_yemmy2`: 0.00
  - `$er_yemmy5`: 0.00
  - `$er_yemmy8`: 0.00
  - `$ur_yemmy2`: 0.00
  - `$ur_yemmy5`: 0.00
  - `Run_Cond`: GetDataIncomeYear != 2019

### 32. Function: DefConst
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

### 33. Function: DefConst
  **Constants Defined:**
  - `$sh_mcse_l1_dgn0`: 0
  - `$sh_mcse_l2_dgn0`: 0
  - `$sh_mcse_l3_dgn0`: 0
  - `$sh_mcse_l4_dgn0`: 0
  - `$sh_mcse_l5_dgn0`: 0
  - `$sh_mcse_l1_dgn1`: 0
  - `$sh_mcse_l2_dgn1`: 0
  - `$sh_mcse_l3_dgn1`: 0
  - `$sh_mcse_l4_dgn1`: 0
  - `$sh_mcse_l5_dgn1`: 0
  - `$sh_mcsemy_1`: 0
  - `$sh_mcsemy_2`: 0
  - `$sh_mcsemy_3`: 0
  - `$sh_mcsemy_4`: 0
  - `$sh_mcsemy_5`: 0
  - `$sh_mcsemy_6`: 0
  - `$sh_mcsemy_7`: 0
  - `$sh_mcsemy_8`: 0
  - `$sh_mcsemy_9`: 0
  - `$sh_0hours_se`: 0
  - `$sh_15hours_se`: 0
  - `$sh_45hours_se`: 0
  - `Run_Cond`: GetDataIncomeYear != 2019


---

## Policy: selfemp_hr
### 1. Function: DefVar
  - **i_fawo**: `0`
  - **i_farmA**: `0`
  - **i_farmC**: `0`
  - **i_farmD**: `0`
  - **i_pro1A**: `0`
  - **i_pro2A**: `0`
  - **i_tradA**: `0`
  - **i_septx**: `0`
  - **i_tradB**: `0`
  - **i_tradE**: `0`
  - **i_sepA**: `0`

### 2. Function: BenCalc
  - **Comp_Cond**: `(ysebsre > 0) & (lsemy > 0) & (lesse = 1)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_farmA`
  - **TAX_UNIT**: `tu_individual_hr`

### 3. Function: BenCalc
  - **Comp_Cond**: `(ysebsre > 0) & (lsemy > 0) & (lesse = 2)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_farmC`
  - **TAX_UNIT**: `tu_individual_hr`

### 4. Function: BenCalc
  - **Comp_Cond**: `(ysebsre > 0) & (lsemy > 0) & (lesse = 3)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_farmD`
  - **TAX_UNIT**: `tu_individual_hr`

### 5. Function: BenCalc
  - **Comp_Cond**: `(ysebsre > 0) & (lsemy > 0) & (lesse = 4)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_pro1A`
  - **TAX_UNIT**: `tu_individual_hr`

### 6. Function: BenCalc
  - **Comp_Cond**: `(ysebsre > 0) & (lsemy > 0) & (lesse = 5)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_pro2A`
  - **TAX_UNIT**: `tu_individual_hr`

### 7. Function: BenCalc
  - **Comp_Cond**: `(ysebsre > 0) & (lsemy > 0) & (lesse = 6)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_tradA`
  - **TAX_UNIT**: `tu_individual_hr`

### 8. Function: ArithOp
  **Formula:** `i_farmA + i_farmC + i_farmD + i_pro1A + i_pro2A + i_tradA + i_tradB`
  **Output Variable:** `i_septx`
  **Tax Unit:** `tu_individual_hr`

### 9. Function: BenCalc
  - **Comp_Cond**: `(ysebsre > 0) & (lsemy > 0) & (lesse = 7)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_tradB`
  - **TAX_UNIT**: `tu_individual_hr`

### 10. Function: BenCalc
  - **Comp_Cond**: `(lsemy > 0) & (lesse = 8)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_tradE`
  - **TAX_UNIT**: `tu_individual_hr`

### 11. Function: ArithOp
  **Formula:** `i_farmA + i_pro1A + i_pro2A + i_tradA`
  **Output Variable:** `i_sepA`
  **Tax Unit:** `tu_individual_hr`


---

## Policy: covidcomp_hr *(Switch: off)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_yem_orig**: `n/a`
  - **Var_Monetary**: `n/a`
  - **i_kfb_orig**: `n/a`
  - **i_ysebsre_orig**: `n/a`
  - **i_bwkmcee_s**: `n/a`
  - **i_bwkmcse_s**: `n/a`
  - **i_yemmy_orig**: `n/a`
  - **i_ysemy_orig**: `n/a`

### 2. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 3. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 5. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 6. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 7. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 8. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 9. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 10. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 11. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`


---

## Policy: tco_hr *(Switch: off)*
### 1. Function: DefConst
  **Constants Defined:**
  - `$tco_v_02111`: $tco_base_v_02111
  - `$tco_v_02121`: $tco_base_v_02121
  - `$tco_v_02122`: $tco_base_v_02122
  - `$tco_v_02131`: $tco_base_v_02131
  - `$tco_v_02211`: $tco_base_v_02211
  - `$tco_v_02212`: $tco_base_v_02212
  - `$tco_v_02213`: $tco_base_v_02213
  - `$tco_v_04511`: $tco_base_v_04511
  - `$tco_v_04521`: $tco_base_v_04521
  - `$tco_v_04522`: $tco_base_v_04522
  - `$tco_v_04531`: $tco_base_v_04531
  - `$tco_v_04541`: $tco_base_v_04541
  - `$tco_v_07221`: $tco_base_v_07221

### 2. Function: DefConst
  **Constants Defined:**
  - `$tco_a_04531`: 1.00*$tco_a_04531a + 0.00*$tco_a_04531b + 0.00*$tco_a_04531c
  - `$tco_a_07221`: 0.50*(0*$tco_a_07221a1+$tco_a_07221a2) + 0.00*$tco_a_07221b + 0.50*$tco_a_07221c + 0.00*$tco_a_07221d + 0.00*$tco_a_07221e
  - `$tco_a_02121`: 0.95*$tco_a_02121a +0.025*$tco_a_02121b +0.025*$tco_a_02121c

### 3. Function: DefConst
  **Constants Defined:**
  - `$tco_base_q_07221`: 0.50*$tco_base_q_07221a + 0.00*$tco_base_q_07221b + 0.50*$tco_base_q_07221c + 0.00*$tco_base_q_07221d + 0.00*$tco_base_q_07221e
  - `$tco_base_q_04531`: 1.00*$tco_base_q_04531a + 0.00*$tco_base_q_04531b + 0.00*$tco_base_q_04531c
  - `$tco_base_q_02131`: ($tco_base_q_02131t)* 100 / 5
  - `$tco_base_q_02122`: $tco_base_q_02122t * 100
  - `$tco_base_q_02121`: (0.90*$tco_base_q_02121t1+ 0.05*$tco_base_q_02121t2 + 0.05*$tco_base_q_02121t3)* 100
  - `$tco_base_q_02111`: $tco_base_q_02111t / 40% * 100
  - `$tco_base_a_07221`: 0.50*(0*$tco_base_a_07221a1+$tco_base_a_07221a2) + 0.00*$tco_base_a_07221b + 0.50*$tco_base_a_07221c + 0.00*$tco_base_a_07221d + 0.00*$tco_base_a_07221e
  - `$tco_base_a_04531`: 1.00*$tco_base_a_04531a + 0.00*$tco_base_a_04531b + 0.00*$tco_base_a_04531c
  - `$tco_base_a_02121`: 0.95*$tco_base_a_02121a + 0.025*$tco_base_a_02121b + 0.025*$tco_base_a_02121c

### 4. Function: DefIl
  - **Name**: `il_xs_exc`
  - **xs07221**: `+`
  - **xs04541**: `+`
  - **xs04531**: `+`
  - **xs04522**: `+`
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

### 5. Function: DefConst
  **Constants Defined:**
  - `$tco_t_01111`: $tco_t_std
  - `$tco_t_01112`: $tco_t_red2
  - `$tco_t_01113`: $tco_t_std
  - `$tco_t_01114`: $tco_t_std
  - `$tco_t_01115`: $tco_t_std
  - `$tco_t_01116`: $tco_t_std
  - `$tco_t_01121`: $tco_t_red2
  - `$tco_t_01122`: $tco_t_red2
  - `$tco_t_01123`: $tco_t_red2
  - `$tco_t_01124`: $tco_t_red2
  - `$tco_t_01125`: $tco_t_red2
  - `$tco_t_01126`: $tco_t_std
  - `$tco_t_01127`: $tco_t_red2
  - `$tco_t_01131`: $tco_t_red2
  - `$tco_t_01132`: $tco_t_red2
  - `$tco_t_01133`: $tco_t_std
  - `$tco_t_01134`: $tco_t_std
  - `$tco_t_01141`: $tco_t_red2
  - `$tco_t_01142`: $tco_t_red2
  - `$tco_t_01143`: $tco_t_red2
  - `$tco_t_01144`: $tco_t_std
  - `$tco_t_01145`: $tco_t_std
  - `$tco_t_01146`: $tco_t_std
  - `$tco_t_01147`: $tco_t_red2
  - `$tco_t_01151`: $tco_t_red2
  - `$tco_t_01152`: $tco_t_red2
  - `$tco_t_01153`: $tco_t_red2
  - `$tco_t_01154`: $tco_t_red2
  - `$tco_t_01155`: $tco_t_red2
  - `$tco_t_01161`: $tco_t_red2
  - `$tco_t_01162`: $tco_t_red2
  - `$tco_t_01163`: $tco_t_red2
  - `$tco_t_01164`: $tco_t_red2
  - `$tco_t_01165`: $tco_t_red2
  - `$tco_t_01166`: $tco_t_red2
  - `$tco_t_01167`: $tco_t_red2
  - `$tco_t_01168`: $tco_t_red2
  - `$tco_t_01169`: $tco_t_red2
  - `$tco_t_01171`: $tco_t_red2
  - `$tco_t_01172`: $tco_t_red2
  - `$tco_t_01173`: $tco_t_red2
  - `$tco_t_01174`: $tco_t_red2
  - `$tco_t_01175`: $tco_t_red2
  - `$tco_t_01176`: $tco_t_red2
  - `$tco_t_01177`: $tco_t_red2
  - `$tco_t_01178`: $tco_t_red2
  - `$tco_t_01181`: $tco_t_std
  - `$tco_t_01182`: $tco_t_std
  - `$tco_t_01183`: $tco_t_std
  - `$tco_t_01184`: $tco_t_std
  - `$tco_t_01185`: $tco_t_std
  - `$tco_t_01186`: $tco_t_std
  - `$tco_t_01191`: $tco_t_std
  - `$tco_t_01192`: $tco_t_std
  - `$tco_t_01193`: $tco_t_red2
  - `$tco_t_01194`: $tco_t_std
  - `$tco_t_01211`: $tco_t_std
  - `$tco_t_01212`: $tco_t_std
  - `$tco_t_01213`: $tco_t_std
  - `$tco_t_01221`: $tco_t_std
  - `$tco_t_01222`: $tco_t_std
  - `$tco_t_01223`: $tco_t_std
  - `$tco_t_01224`: $tco_t_std
  - `$tco_t_02111`: $tco_t_std
  - `$tco_t_02121`: $tco_t_std
  - `$tco_t_02122`: $tco_t_std
  - `$tco_t_02131`: $tco_t_std
  - `$tco_t_02211`: $tco_t_std
  - `$tco_t_02212`: $tco_t_std
  - `$tco_t_02213`: $tco_t_std
  - `$tco_t_03111`: $tco_t_std
  - `$tco_t_03121`: $tco_t_std
  - `$tco_t_03122`: $tco_t_std
  - `$tco_t_03123`: $tco_t_std
  - `$tco_t_03131`: $tco_t_std
  - `$tco_t_03141`: $tco_t_std
  - `$tco_t_03211`: $tco_t_std
  - `$tco_t_03212`: $tco_t_std
  - `$tco_t_03213`: $tco_t_std
  - `$tco_t_03221`: $tco_t_std
  - `$tco_t_04111`: $tco_t_zero
  - `$tco_t_04121`: $tco_t_zero
  - `$tco_t_04311`: $tco_t_std
  - `$tco_t_04321`: $tco_t_std
  - `$tco_t_04411`: $tco_t_red1
  - `$tco_t_04421`: $tco_t_red1
  - `$tco_t_04431`: $tco_t_red1
  - `$tco_t_04441`: $tco_t_std
  - `$tco_t_04511`: $tco_t_red1
  - `$tco_t_04521`: $tco_t_red2
  - `$tco_t_04522`: $tco_t_std
  - `$tco_t_04531`: $tco_t_std
  - `$tco_t_04541`: $tco_t_std
  - `$tco_t_04551`: $tco_t_red2
  - `$tco_t_05111`: $tco_t_std
  - `$tco_t_05121`: $tco_t_std
  - `$tco_t_05131`: $tco_t_std
  - `$tco_t_05211`: $tco_t_std
  - `$tco_t_05311`: $tco_t_std
  - `$tco_t_05312`: $tco_t_std
  - `$tco_t_05313`: $tco_t_std
  - `$tco_t_05314`: $tco_t_std
  - `$tco_t_05315`: $tco_t_std
  - `$tco_t_05316`: $tco_t_std
  - `$tco_t_05317`: $tco_t_std
  - `$tco_t_05321`: $tco_t_std
  - `$tco_t_05331`: $tco_t_std
  - `$tco_t_05411`: $tco_t_std
  - `$tco_t_05412`: $tco_t_std
  - `$tco_t_05413`: $tco_t_std
  - `$tco_t_05414`: $tco_t_std
  - `$tco_t_05511`: $tco_t_std
  - `$tco_t_05521`: $tco_t_std
  - `$tco_t_05611`: $tco_t_std
  - `$tco_t_05612`: $tco_t_std
  - `$tco_t_05621`: $tco_t_std
  - `$tco_t_05622`: $tco_t_std
  - `$tco_t_06111`: $tco_t_red2
  - `$tco_t_06121`: $tco_t_std
  - `$tco_t_06131`: $tco_t_red2
  - `$tco_t_06211`: $tco_t_zero
  - `$tco_t_06221`: $tco_t_zero
  - `$tco_t_06231`: $tco_t_zero
  - `$tco_t_06232`: $tco_t_zero
  - `$tco_t_06233`: $tco_t_zero
  - `$tco_t_06311`: $tco_t_zero
  - `$tco_t_07111`: $tco_t_std
  - `$tco_t_07112`: $tco_t_std
  - `$tco_t_07121`: $tco_t_std
  - `$tco_t_07131`: $tco_t_std
  - `$tco_t_07141`: $tco_t_std
  - `$tco_t_07211`: $tco_t_std
  - `$tco_t_07221`: $tco_t_std
  - `$tco_t_07231`: $tco_t_std
  - `$tco_t_07241`: $tco_t_std
  - `$tco_t_07311`: $tco_t_std
  - `$tco_t_07321`: $tco_t_std
  - `$tco_t_07331`: $tco_t_zero
  - `$tco_t_07341`: $tco_t_std
  - `$tco_t_07351`: $tco_t_std
  - `$tco_t_07361`: $tco_t_std
  - `$tco_t_08111`: $tco_t_zero
  - `$tco_t_08211`: $tco_t_std
  - `$tco_t_08311`: $tco_t_std
  - `$tco_t_09111`: $tco_t_std
  - `$tco_t_09112`: $tco_t_std
  - `$tco_t_09121`: $tco_t_std
  - `$tco_t_09122`: $tco_t_std
  - `$tco_t_09131`: $tco_t_std
  - `$tco_t_09141`: $tco_t_std
  - `$tco_t_09151`: $tco_t_std
  - `$tco_t_09211`: $tco_t_std
  - `$tco_t_09221`: $tco_t_std
  - `$tco_t_09222`: $tco_t_std
  - `$tco_t_09231`: $tco_t_std
  - `$tco_t_09311`: $tco_t_std
  - `$tco_t_09321`: $tco_t_std
  - `$tco_t_09331`: $tco_t_std
  - `$tco_t_09341`: $tco_t_std
  - `$tco_t_09351`: $tco_t_std
  - `$tco_t_09411`: $tco_t_std
  - `$tco_t_09421`: $tco_t_red2
  - `$tco_t_09422`: $tco_t_std
  - `$tco_t_09423`: $tco_t_zero
  - `$tco_t_09424`: $tco_t_std
  - `$tco_t_09511`: $tco_t_red2
  - `$tco_t_09521`: $tco_t_red2
  - `$tco_t_09531`: $tco_t_std
  - `$tco_t_09541`: $tco_t_std
  - `$tco_t_09611`: $tco_t_std
  - `$tco_t_10111`: $tco_t_zero
  - `$tco_t_10211`: $tco_t_zero
  - `$tco_t_10311`: $tco_t_zero
  - `$tco_t_10411`: $tco_t_zero
  - `$tco_t_10511`: $tco_t_zero
  - `$tco_t_11111`: $tco_t_red1
  - `$tco_t_11112`: $tco_t_std
  - `$tco_t_11121`: $tco_t_red1
  - `$tco_t_11211`: $tco_t_red1
  - `$tco_t_12111`: $tco_t_std
  - `$tco_t_12121`: $tco_t_std
  - `$tco_t_12131`: $tco_t_std
  - `$tco_t_12311`: $tco_t_std
  - `$tco_t_12321`: $tco_t_std
  - `$tco_t_12322`: $tco_t_std
  - `$tco_t_12411`: $tco_t_zero
  - `$tco_t_12412`: $tco_t_zero
  - `$tco_t_12521`: $tco_t_zero
  - `$tco_t_12531`: $tco_t_zero
  - `$tco_t_12541`: $tco_t_zero
  - `$tco_t_12551`: $tco_t_zero
  - `$tco_t_12621`: $tco_t_zero
  - `$tco_t_12711`: $tco_t_std
  - `Run_Cond`: GetDataCOICOPVersion=2003

### 6. Function: DefConst
  **Constants Defined:**
  - `$tco_t_std`: $tco_base_t_std
  - `$tco_t_red1`: $tco_base_t_red1
  - `$tco_t_red2`: $tco_base_t_red2
  - `$tco_t_zero`: $tco_base_t_zero

### 7. Function: DefConst
  **Constants Defined:**
  - `$tco_a_07221e`: $tco_base_a_07221e
  - `$tco_a_07221d`: $tco_base_a_07221d
  - `$tco_a_07221c`: $tco_base_a_07221c
  - `$tco_a_07221b`: $tco_base_a_07221b
  - `$tco_a_07221a1`: $tco_base_a_07221a1
  - `$tco_a_04541`: $tco_base_a_04541
  - `$tco_a_04531c`: $tco_base_a_04531c
  - `$tco_a_04531b`: $tco_base_a_04531b
  - `$tco_a_04531a`: $tco_base_a_04531a
  - `$tco_a_04522`: $tco_base_a_04522
  - `$tco_a_04521`: $tco_base_a_04521
  - `$tco_a_04511`: $tco_base_a_04511
  - `$tco_a_02213`: $tco_base_a_02213
  - `$tco_a_02212`: $tco_base_a_02212
  - `$tco_a_02211`: $tco_base_a_02211
  - `$tco_a_02131`: $tco_base_a_02131
  - `$tco_a_02122`: $tco_base_a_02122
  - `$tco_a_02121a`: $tco_base_a_02121a
  - `$tco_a_02111`: $tco_base_a_02111
  - `$tco_a_07221a2`: $tco_base_a_07221a2
  - `$tco_a_02121c`: $tco_base_a_02121c
  - `$tco_a_02121b`: $tco_base_a_02121b

### 8. Function: DefIl
  - **Name**: `il_xs_rest`
  - **xs01111**: `+`
  - **Warn_If_NonMonetary**: `no`
  - **xs12621**: `+`
  - **xs12551**: `+`
  - **xs12541**: `+`
  - **xs12531**: `+`
  - **xs12521**: `+`
  - **xs12412**: `+`
  - **xs12411**: `+`
  - **xs12322**: `+`
  - **xs12321**: `+`
  - **xs12311**: `+`
  - **xs12131**: `+`
  - **xs12121**: `+`
  - **xs12111**: `+`
  - **xs11211**: `+`
  - **xs11121**: `+`
  - **xs11112**: `+`
  - **xs11111**: `+`
  - **xs10511**: `+`
  - **xs10411**: `+`
  - **xs10311**: `+`
  - **xs10211**: `+`
  - **xs10111**: `+`
  - **xs09611**: `+`
  - **xs09541**: `+`
  - **xs09531**: `+`
  - **xs09521**: `+`
  - **xs09511**: `+`
  - **xs09424**: `+`
  - **xs09423**: `+`
  - **xs09422**: `+`
  - **xs09421**: `+`
  - **xs09411**: `+`
  - **xs09351**: `+`
  - **xs09341**: `+`
  - **xs09331**: `+`
  - **xs09321**: `+`
  - **xs09311**: `+`
  - **xs09231**: `+`
  - **xs09222**: `+`
  - **xs09221**: `+`
  - **xs09211**: `+`
  - **xs09151**: `+`
  - **xs09141**: `+`
  - **xs09131**: `+`
  - **xs09122**: `+`
  - **xs09121**: `+`
  - **xs09112**: `+`
  - **xs09111**: `+`
  - **xs08311**: `+`
  - **xs08211**: `+`
  - **xs08111**: `+`
  - **xs07361**: `+`
  - **xs07351**: `+`
  - **xs07341**: `+`
  - **xs07331**: `+`
  - **xs07321**: `+`
  - **xs07311**: `+`
  - **xs07241**: `+`
  - **xs07231**: `+`
  - **xs07211**: `+`
  - **xs07141**: `+`
  - **xs07131**: `+`
  - **xs07121**: `+`
  - **xs07112**: `+`
  - **xs07111**: `+`
  - **xs06311**: `+`
  - **xs06233**: `+`
  - **xs06232**: `+`
  - **xs06231**: `+`
  - **xs06221**: `+`
  - **xs06211**: `+`
  - **xs06131**: `+`
  - **xs06121**: `+`
  - **xs06111**: `+`
  - **xs05622**: `+`
  - **xs05621**: `+`
  - **xs05612**: `+`
  - **xs05611**: `+`
  - **xs05521**: `+`
  - **xs05511**: `+`
  - **xs05414**: `+`
  - **xs05413**: `+`
  - **xs05412**: `+`
  - **xs05411**: `+`
  - **xs05331**: `+`
  - **xs05321**: `+`
  - **xs05317**: `+`
  - **xs05316**: `+`
  - **xs05315**: `+`
  - **xs05314**: `+`
  - **xs05313**: `+`
  - **xs05312**: `+`
  - **xs05311**: `+`
  - **xs05211**: `+`
  - **xs05131**: `+`
  - **xs05121**: `+`
  - **xs05111**: `+`
  - **xs04551**: `+`
  - **xs04441**: `+`
  - **xs04431**: `+`
  - **xs04421**: `+`
  - **xs04411**: `+`
  - **xs04321**: `+`
  - **xs04311**: `+`
  - **xs04121**: `+`
  - **xs04111**: `+`
  - **xs03221**: `+`
  - **xs03213**: `+`
  - **xs03212**: `+`
  - **xs03211**: `+`
  - **xs03141**: `+`
  - **xs03131**: `+`
  - **xs03123**: `+`
  - **xs03122**: `+`
  - **xs03121**: `+`
  - **xs03111**: `+`
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
  - **xs01178**: `+`
  - **xs01177**: `+`
  - **xs01176**: `+`
  - **xs01175**: `+`
  - **xs01174**: `+`
  - **xs01173**: `+`
  - **xs01172**: `+`
  - **xs01171**: `+`
  - **xs01169**: `+`
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
  - **xs01142**: `+`
  - **xs01141**: `+`
  - **xs01134**: `+`
  - **xs01133**: `+`
  - **xs01132**: `+`
  - **xs01131**: `+`
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
  - **xs12711**: `+`

### 9. Function: DefIl
  - **Name**: `ils_extstat_ittcal`
  - **il_itt_revc**: `+`
  - **il_itt_excc**: `+`

### 10. Function: DefIl
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

### 11. Function: DefIl
  - **Name**: `il_itt_revc`
  - **il_tva_na**: `+`
  - **il_tx_na**: `+`

### 12. Function: DefIl
  - **Name**: `ils_extstat_ittncal`
  - **il_itt_expnc**: `+`
  - **il_itt_revnc**: `+`
  - **il_itt_excnc**: `+`

### 13. Function: DefIl
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

### 14. Function: DefIl
  - **Name**: `il_itt_revnc`
  - **il_tva**: `+`
  - **il_tx**: `+`

### 15. Function: DefIl
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

### 16. Function: DefConst
  **Constants Defined:**
  - `$tco_a_02211`: (53.10 * 6 + 56.10 * 6)/12
  - `$tco_a_02212`: (114.15 * 6 + 120.50 * 6)/12
  - `$tco_a_02213`: (114.15 * 6 + 120.50 * 6)/12


---

## Policy: boamt_hr
### 1. Function: DefVar
  - **i_boamtYpHM**: `0`

### 2. Function: DefConst
  **Constants Defined:**
  - `$boamt`: 154.50#m

### 3. Function: DefIl
  - **Name**: `il_boamt`
  - **ils_pen**: `+`
  - **yemtx**: `+`
  - **kfbtx**: `+`
  - **ysv**: `+`
  - **ysebsre**: `+`
  - **ysecwre**: `+`
  - **ypp**: `+`
  - **ypr**: `+`
  - **yiy**: `+`
  - **bhl**: `+`
  - **bfapl_s**: `+`
  - **bfama_s**: `+`
  - **bmanc_s**: `+`
  - **bunct_s**: `+`
  - **bwkmc_s**: `n/a`
  - **ymc**: `+`
  - **ils_sicot**: `-`
  - **ils_sicee**: `-`
  - **ils_sicse**: `-`
  - **tin_s**: `-`
  - **tmu_s**: `n/a`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(dag >= 65) & (ils_pen = 0) & (bsa_s#1 = 0)`
  - **Tax Unit:** `tu_individual_hr`

### 5. Function: ArithOp
  **Formula:** `il_boamt / nPersInUnit`
  **Output Variable:** `i_boamtYpHM`
  **Tax Unit:** `tu_household_hr`

### 6. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_boamtYpHM#1 <= 2 * $boamt)`
  - **Comp_perElig**: `$boamt`
  - **Output_Var**: `boamt_s`
  - **#_Level**: `tu_household_hr`
  - **TAX_UNIT**: `tu_individual_hr`


---

## Policy: bfafh_hr
### 1. Function: DefVar
  - **i_bfafh**: `0`
  - **i_bfafhmc**: `0`

### 2. Function: DefConst
  **Constants Defined:**
  - `$bfafhd1`: 10
  - `$bfafhd2`: 15

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(IsHeadOfTu#1) & (dgn = 1) & (IsParentOfDepChild#1) & (nDepChInTu#1 > 0) & ((lemmy > 0) | (les = 3) | (i_bmelse = 1))`
  - **Tax Unit:** `tu_individual_hr`

### 4. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(liwwh < 12)`
  - **Comp_perTU**: `$bfafh_min_amt`
  - **LowLim**: `$bfafh_min_amt`
  - **Output_Var**: `i_bfafh`
  - **TAX_UNIT**: `tu_individual_hr`

### 5. Function: BenCalc
  - **Comp_Cond**: `(i_twins = 1) | (i_triplets = 1)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_bfafhmc`
  - **TAX_UNIT**: `tu_bfafh_hr`

### 6. Function: BenCalc
  - **Comp_Cond**: `(i_bfafh > 0) & (i_bfafhmc = 1)`
  - **Comp_perTU**: `i_bfafh * $bfafhd2 * 8 / 2080`
  - **Output_Var**: `bfafh_s`
  - **TAX_UNIT**: `tu_individual_hr`


---

## Policy: boatu00_hr
### 1. Function: DefIl
  - **Name**: `il_boatu`
  - **i_penpsav**: `+`
  - **i_tinPE**: `-`
  - **i_tmuPE**: `n/a`

### 2. Function: DefVar *(Switch: n/a)*
  - **i_boatu00_1**: `n/a`
  - **i_boatu00_2**: `n/a`
  - **i_boatu00_3**: `n/a`

### 3. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** `n/a`
    - Band: Rate=``, Limit=``

### 4. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** `n/a`
    - Band: Rate=``, Limit=``

### 5. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** `n/a`
    - Band: Rate=``, Limit=``

### 6. Function: BenCalc
  - **Comp_Cond**: `(il_boatu > 0) & (ils_sicee = 0) & (ils_sicse = 0)`
  - **Comp_perTU**: `0`
  - **Output_Var**: `boatu00_s`
  - **TAX_UNIT**: `tu_individual_hr`


---

## Policy: bchtu_hr *(Switch: n/a)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_bchtu**: `n/a`

### 2. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: buntu_hr *(Switch: n/a)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_buntu**: `n/a`

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


---

## Policy: bditu_hr *(Switch: n/a)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_bditu**: `n/a`

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


---

## Policy: bsatu_hr *(Switch: n/a)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_bsatu**: `n/a`

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


---

## Policy: boatu01_hr
### 1. Function: DefVar
  - **i_boatu01_1**: `0`

### 2. Function: ArithOp
  **Formula:** `50#y`
  **Output Variable:** `i_boatu01_1`
  **Tax Unit:** `tu_individual_hr`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `((poamy > 0) | (boamt_s > 0)) & (ils_sicee = 0) & (ils_sicse = 0)`
  - **Tax Unit:** `tu_individual_hr`

### 4. Function: ArithOp
  **Formula:** `i_boatu01_1`
  **Output Variable:** `boatu01_s`
  **Tax Unit:** `tu_household_hr`

### 5. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`


---
