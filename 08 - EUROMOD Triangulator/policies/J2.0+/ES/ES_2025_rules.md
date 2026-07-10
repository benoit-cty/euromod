# EUROMOD Tax-Benefit Rules for ES_2025

## Policy: uprate_es
### 1. Function: Uprate
  - **dataset**: `*training_data`
  - **def_factor**: `1`
  - **WarnIfNoFactor**: `no`
  - **Dataset**: `*_hhot`

### 2. Function: Uprate
  - **dataset**: `ES_20??_a?`
  - **def_factor**: `$f_1`
  - **afc**: `$f_afc_av`
  - **bch00**: `$f_bch00`
  - **bchdi**: `$f_bchdi`
  - **bchot**: `$f_mw`
  - **bed**: `$f_bed_av`
  - **bho**: `$f_cpi_bho`
  - **bma**: `$f_wagelag1`
  - **bsa**: `$f_iprem`
  - **bunct**: `$f_wagelag1`
  - **bunctpc**: `$f_wage`
  - **bunnc**: `$f_iprem`
  - **bunot**: `$f_iprem`
  - **kfb**: `$f_labor`
  - **kivho**: `$f_1`
  - **pdi00**: `$f_pdi00_av`
  - **poa00**: `$f_poa_av`
  - **poacm**: `$f_mpenold`
  - **poanc**: `$f_poanc`
  - **poaot**: `$f_mpenold`
  - **psuot**: `$f_mpenw`
  - **psuwd00**: `$f_psu_av`
  - **psuwdcm**: `$f_mpenw`
  - **tad**: `$f_1`
  - **tin**: `$f_1`
  - **tis**: `$f_1`
  - **twl**: `$f_tpr`
  - **tscee**: `$f_1`
  - **tscer**: `$f_1`
  - **tscse**: `$f_1`
  - **xhc**: `$f_cpi`
  - **xhcmomc**: `$f_cpi`
  - **xhcmomi**: `$f_cpi`
  - **xhcot**: `$f_cpi`
  - **xhcrt**: `$f_cpi`
  - **xhcmo**: `$f_cpi`
  - **xmp**: `$f_cpi`
  - **xpp**: `$f_cpi`
  - **yds**: `$f_1`
  - **yivwg**: `$f_wage`
  - **yiy**: `$f_k`
  - **yot**: `$f_1`
  - **ypt**: `$f_wage`
  - **yse**: `$f_wage`
  - **ysv**: `$f_wage`
  - **aggvar_name**: `psu`
  - **aggvar_tolerance**: `1`
  - **aggvar_part**: `psuwdcm`
  - **Factor_Condition**: `lcs = 1`
  - **yem**: `$f_wagepub`
  - **kfbcc**: `$f_labor`
  - **ydses_o**: `$f_1`
  - **yem_a**: `$f_wage`
  - **AggVar_Part**: `pdiot`
  - **ypr**: `$f_1`
  - **WarnIfNoFactor**: `yes`
  - **bhlot**: `$f_wage`
  - **AggVar_Tolerance**: `1`
  - **AggVar_Name**: `bfa`
  - **bhl00**: `$f_wage`
  - **pdicm**: `$f_pdicm_av`
  - **pdinc**: `$f_pdinc_av`
  - **ypp**: `$f_ypp_av`
  - **yptmp**: `$f_wage`
  - **ymwdt**: `$f_wageLead`
  - **tintrch**: `$f_tintrch`
  - **yem20_a**: `$f_wage`
  - **yem19_a**: `$f_wage`
  - **yem18_a**: `$f_wage`
  - **Dataset**: `ES_20??_??_????_??_??`
  - **pdiot**: `$f_pdi00_av`
  - **tpr**: `$f_1`
  - **xed00**: `$f_cpi`
  - **xhl00**: `$f_cpi`
  - **yprrt**: `$f_1`


---

## Policy: ilsdef_es
### 1. Function: DefIl
  - **name**: `ils_earns`
  - **yem**: `+`
  - **yse**: `+`
  - **yemmc_s**: `n/a`

### 2. Function: DefIl
  - **name**: `ils_origy`
  - **ils_earns**: `+`
  - **yiy**: `+`
  - **yot**: `+`
  - **ypr**: `+`
  - **ypt**: `+`
  - **ypp**: `+`
  - **xmp**: `-`

### 3. Function: DefIl
  - **name**: `ils_pen`
  - **pdi00**: `+`
  - **poa00**: `+`
  - **poaot**: `+`
  - **psuwd00**: `+`
  - **psuot**: `+`
  - **pdiot**: `+`

### 4. Function: DefIl
  - **name**: `ils_origrepy`
  - **ils_origy**: `+`
  - **ils_pen**: `+`
  - **bunnc_s**: `+`
  - **bunct_s**: `+`
  - **bhl**: `+`
  - **bma**: `+`
  - **bmact_s**: `+`
  - **bpact_s**: `+`
  - **bmanc_s**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`

### 5. Function: DefIl
  - **name**: `ils_bensim`
  - **bch00_s**: `+`
  - **bchbamtna_s**: `+`
  - **bchmtrg_s**: `+`
  - **bchbamtrg_s**: `+`
  - **bchlgmtrg_s**: `+`
  - **bunnc_s**: `+`
  - **bunmt_s**: `+`
  - **poacm_s**: `+`
  - **poanc_s**: `+`
  - **psuwdcm_s**: `+`
  - **bchbaucna_s**: `n/a`
  - **bchdi_s**: `+`
  - **bunct_s**: `+`
  - **bchucrg_s**: `+`
  - **bchbaucrg_s**: `+`
  - **bchlgucrg_s**: `+`
  - **tintrch_s**: `+`
  - **tintrchlg_s**: `+`
  - **tintrchlp_s**: `+`
  - **bchbaucna02_s**: `+`
  - **bunct02_s**: `+`
  - **bmact_s**: `+`
  - **bpact_s**: `+`
  - **bmanc_s**: `+`
  - **bsarg_s**: `+`
  - **bsa00_s**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **bwrls_s**: `+`
  - **bunnc02_s**: `+`

### 6. Function: DefIl
  - **name**: `ils_benmt`
  - **bch00_s**: `+`
  - **bchbamtna_s**: `+`
  - **bchmtrg_s**: `+`
  - **bchbamtrg_s**: `+`
  - **bchlgmtrg_s**: `+`
  - **bunnc_s**: `+`
  - **bunmt_s**: `+`
  - **poacm_s**: `+`
  - **poanc_s**: `+`
  - **psuwdcm_s**: `+`
  - **bsa_s**: `n/a`
  - **bed**: `+`
  - **bho**: `+`
  - **bunot**: `+`
  - **pdicm**: `+`
  - **pdinc**: `+`
  - **bsarg_s**: `+`
  - **bsa00_s**: `+`
  - **bwrls_s**: `+`

### 7. Function: DefIl
  - **name**: `ils_bennt`
  - **bma**: `+`
  - **bchbaucna_s**: `n/a`
  - **bchdi_s**: `+`
  - **bunct_s**: `+`
  - **bchucrg_s**: `+`
  - **bchbaucrg_s**: `+`
  - **bchlgucrg_s**: `+`
  - **tintrch_s**: `+`
  - **ysv**: `+`
  - **bhl**: `+`
  - **tintrchlg_s**: `+`
  - **tintrchlp_s**: `+`
  - **bchbaucna02_s**: `+`
  - **bunct02_s**: `+`
  - **bmact_s**: `+`
  - **bpact_s**: `+`
  - **bmanc_s**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`

### 8. Function: DefIl
  - **name**: `ils_ben`
  - **ils_pen**: `+`
  - **ils_benmt**: `+`
  - **ils_bennt**: `+`

### 9. Function: DefIl
  - **name**: `ils_taxsim`
  - **tin_s**: `+`

### 10. Function: DefIl
  - **name**: `ils_tax`
  - **ils_taxin**: `+`
  - **ils_taxwl**: `+`

### 11. Function: DefIl
  - **name**: `ils_sicee`
  - **tsceepi_s**: `+`
  - **tsceeui_s**: `+`
  - **tsceeot_s**: `+`
  - **tsceeie_s**: `+`
  - **tsceeas_s**: `+`

### 12. Function: DefIl
  - **name**: `ils_sicer`
  - **tscerpi_s**: `+`
  - **tscerui_s**: `+`
  - **tscerot_s**: `+`
  - **tscerie_s**: `+`
  - **tsceras_s**: `+`

### 13. Function: DefIl
  - **name**: `ils_sicct`
  - **tscuner_s**: `+`
  - **tsccterpi_s**: `n/a`
  - **tsccterui_s**: `n/a`
  - **tsccterot_s**: `n/a`
  - **tscctsepi_s**: `n/a`
  - **tscctsehl_s**: `n/a`
  - **tscctseot_s**: `n/a`

### 14. Function: DefIl
  - **name**: `ils_sicse`
  - **tscsepi_s**: `+`
  - **tscsehl_s**: `+`
  - **tscseot_s**: `+`
  - **tscseie_s**: `+`

### 15. Function: DefIl
  - **name**: `ils_dispy`
  - **ils_origy**: `+`
  - **ils_ben**: `+`
  - **ils_tax**: `-`
  - **ils_sicdy**: `-`

### 16. Function: DefIl
  - **name**: `ils_b1_bho`
  - **bho**: `+`

### 17. Function: DefIl
  - **name**: `ils_b1_bfa`
  - **bchbaucna_s**: `n/a`
  - **ils_b1_bcb**: `+`
  - **bch00_s**: `+`
  - **bchdi_s**: `+`
  - **bchlgucrg_s**: `+`
  - **bchbaucrg_s**: `+`
  - **bchucrg_s**: `+`
  - **bchbamtna_s**: `+`
  - **bchbaucna02_s**: `+`
  - **bchlgmtrg_s**: `+`
  - **bchbamtrg_s**: `+`
  - **bchmtrg_s**: `+`
  - **tintrch_s**: `+`
  - **tintrchlp_s**: `+`
  - **tintrchlg_s**: `+`

### 18. Function: DefIl
  - **name**: `ils_b1_bsa`
  - **bsa_s**: `n/a`
  - **bsarg_s**: `+`
  - **bsa00_s**: `+`
  - **bwrls_s**: `+`

### 19. Function: DefIl
  - **name**: `ils_b1_bed`
  - **bed**: `+`

### 20. Function: DefIl
  - **name**: `ils_b1_bun`
  - **bunot**: `+`
  - **bunmt_s**: `+`
  - **bunnc_s**: `+`
  - **bunct_s**: `+`
  - **bunct02_s**: `+`
  - **ysv**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`

### 21. Function: DefIl
  - **name**: `ils_b1_bdi`
  - **pdi00**: `+`
  - **pdinc**: `+`
  - **pdicm**: `+`
  - **pdiot**: `+`

### 22. Function: DefIl
  - **name**: `ils_b1_bsu`
  - **psuwd00**: `+`
  - **psuwdcm_s**: `+`
  - **psuot**: `+`

### 23. Function: DefIl
  - **name**: `ils_b1_boa`
  - **poacm_s**: `+`
  - **poanc_s**: `+`
  - **poa00**: `+`
  - **poaot**: `+`

### 24. Function: DefIl
  - **name**: `ils_b1_bhl`
  - **bhl**: `+`

### 25. Function: DefIl
  - **Name**: `ils_b2_bfaed`
  - **ils_b1_bfa**: `+`
  - **ils_b1_bed**: `+`

### 26. Function: DefIl
  - **Name**: `ils_b2_penhl`
  - **ils_b1_bdi**: `+`
  - **ils_b1_bhl**: `+`
  - **ils_b1_bsu**: `+`
  - **ils_b1_boa**: `+`

### 27. Function: DefIl
  - **Name**: `ils_b2_bsaho`
  - **ils_b1_bsa**: `+`
  - **ils_b1_bho**: `+`

### 28. Function: DefIl
  - **Name**: `ils_sicot`
  - **tscunee_s**: `+`
  - **tscbeeepi_s**: `n/a`
  - **tscbeeeui_s**: `n/a`
  - **tscbeeeot_s**: `n/a`

### 29. Function: DefIl
  - **Name**: `ils_sicdy`
  - **ils_sicse**: `+`
  - **ils_sicot**: `+`
  - **ils_sicee**: `+`

### 30. Function: DefIl
  - **Name**: `ils_base_tin`
  - **ypp**: `+`
  - **yse**: `+`
  - **ypr**: `+`
  - **psuot**: `+`
  - **psuwd00**: `+`
  - **poaot**: `+`
  - **poa00**: `+`
  - **pdi00**: `+`
  - **bma**: `n/a`
  - **bunnc_s**: `+`
  - **bunct_s**: `+`
  - **bhl**: `+`
  - **psuwdcm_s**: `+`
  - **poanc_s**: `+`
  - **poacm_s**: `+`
  - **yem**: `+`
  - **yiy**: `+`
  - **bmact_s**: `n/a`
  - **bpact_s**: `n/a`
  - **bmanc_s**: `n/a`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **pdiot**: `+`
  - **pec_s**: `n/a`

### 31. Function: DefIl
  - **Name**: `ils_b1_bcb`
  - **bmanc_s**: `+`
  - **bpact_s**: `+`
  - **bmact_s**: `+`
  - **bma**: `+`

### 32. Function: DefIl
  - **Name**: `ils_b1_bwk`

### 33. Function: DefIl
  - **Name**: `ils_b2_bunwk`
  - **ils_b1_bwk**: `+`
  - **ils_b1_bun**: `+`

### 34. Function: DefIl
  - **Name**: `ils_taxin`
  - **tin_s**: `+`

### 35. Function: DefIl
  - **Name**: `ils_taxwl`
  - **twl**: `+`

### 36. Function: DefIl
  - **Name**: `ils_extstat_other`
  - **i_bsarg_11**: `+`
  - **i_bsarg_12**: `+`
  - **i_bsarg_13**: `+`
  - **i_bsarg_21**: `+`
  - **i_bsarg_22**: `+`
  - **i_bsarg_23**: `+`
  - **i_bsarg_24**: `+`
  - **i_bsarg_30**: `+`
  - **i_bsarg_41**: `+`
  - **i_bsarg_42**: `+`
  - **i_bsarg_43**: `+`
  - **i_bsarg_51**: `+`
  - **i_bsarg_52**: `+`
  - **i_bsarg_53**: `+`
  - **i_bsarg_61**: `+`
  - **i_bsarg_62**: `+`
  - **i_bsarg_63**: `+`
  - **i_bsarg_64**: `+`
  - **i_bsarg_70**: `+`


---

## Policy: tudef_es
### 1. Function: DefTu
  - **Name**: `tu_hh_oecd_co`
  - **Type**: `HH`
  - **DepChildCond**: `dag<14`

### 2. Function: DefTu
  - **Name**: `tu_household_es`
  - **Type**: `HH`
  - **DepChildCond**: `Default`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`

### 3. Function: DefTu
  - **name**: `tu_couple_es`
  - **type**: `SUBGROUP`
  - **Members**: `Partner`

### 4. Function: DefTu
  - **Name**: `tu_individual_es`
  - **Type**: `IND`
  - **DepChildCond**: `Default`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`
  - **LoneParentCond**: `Default & !IsMarried`

### 5. Function: DefTu
  - **Name**: `tu_large_es`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `default & (dag < 21 | (dag < 26 & dec > 0) | ddi > 0 & (idfather>0 | idmother>0)) & ((ils_origy#1 <= $SMI) | (ddi> 0 & pdi00 <=$IPREM))`
  - **#_level**: `tu_individual_es`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`

### 6. Function: DefTu
  - **Name**: `tu_nucfam`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `default & dag < 18`
  - **LoneParentCond**: `Default`

### 7. Function: DefTu
  - **Name**: `tu_bunct`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **OwnDepChildCond**: `default`
  - **DepChildCond**: `(dag < 26 | ddi > 0) & ils_origrepy#1 <= $SMI`
  - **#_level**: `tu_individual_es`


---

## Policy: ConstDef_es
### 1. Function: DefConst
  **Constants Defined:**
  - `$IPREM`: 600#m
  - `$SMI`: 1184  #m
  - `$IRSC`:  778.49 #m
  - `$SMI2`: 735.90 #m

### 2. Function: DefConst
  **Constants Defined:**
  - `$UB_QperMin`: 12
  - `$UB_QperTot`: 72
  - `$UBSE_QperTot`: 24
  - `$UBSE_QperMin`: 12

### 3. Function: DefConst
  **Constants Defined:**
  - `$ImputedWage`: 0
  - `$lhw`: 40

### 4. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$mc_rrate`: n/a
  - `$mc_share`: n/a
  - `$mc_rrate_se`: n/a
  - `$mc_rrate_se_2`: n/a

### 5. Function: DefConst
  **Constants Defined:**
  - `$tscft_ftbs_minamt1`: 1929.00#m
  - `$tscft_ftbs_minamt2`: 1599.60#m
  - `$tscft_ftbs_minamt3`: 1391.70#m
  - `$tscft_ftbs_minamt4`: 1381.20#m
  - `$tscft_ftbs_minamt5`: 1381.20#m
  - `$tscft_ftbs_maxamt`: 4909.50#m
  - `$tscft_ee_rate1`: 0.047
  - `$tscft_ee_rate2`: 0.0155
  - `$tscft_ee_rate3`: 0.001
  - `$tscft_er_rate1`: 0.236
  - `$tscft_er_rate2`: 0.055
  - `$tscft_er_rate3`: 0.008
  - `$tscft_ee_rate4`: 0.0013
  - `$tscft_er_rate4`: 0.0067
  - `$tscft_ee_rate5`: 0.0015
  - `$tscft_ee_rate6`: 0.0017
  - `$tscft_ee_rate7`: 0.0019
  - `$tscft_ee_lim1`: 4909.50
  - `$tscft_ee_lim2`: 5400.45
  - `$tscft_ee_lim3`: 7364.25
  - `$tscft_er_rate5`: 0.0077
  - `$tscft_er_rate6`: 0.0083
  - `$tscft_er_rate7`: 0.0098
  - `$tscft_er_lim1`: 4909.50
  - `$tscft_er_lim2`: 5400.45
  - `$tscft_er_lim3`: 7364.25

### 6. Function: DefConst
  **Constants Defined:**
  - `$tscpt_ptbs_minamt1`: 11.62
  - `$tscpt_ptbs_minamt2`: 9.64
  - `$tscpt_ptbs_minamt3`: 8.38
  - `$tscpt_ptbs_minamt4`: 8.32
  - `$tscpt_ptbs_minamt5`: 8.32
  - `$tscpt_ptbs_maxamt`: 4909.50#m
  - `$tscpt_ee_rate1`: 0.047
  - `$tscpt_ee_rate2`: 0.0155
  - `$tscpt_ee_rate3`: 0.001
  - `$tscpt_er_rate1`: 0.236
  - `$tscpt_er_rate2`: 0.055
  - `$tscpt_er_rate3`: 0.008
  - `$tscpt_ee_rate4`: 0.0013
  - `$tscpt_er_rate4`: 0.0067
  - `$tscpt_ee_rate5`: $tscft_ee_rate5
  - `$tscpt_ee_rate6`: $tscft_ee_rate6
  - `$tscpt_ee_rate7`: $tscft_ee_rate7
  - `$tscpt_ee_lim1`: $tscft_ee_lim1
  - `$tscpt_ee_lim2`: $tscft_ee_lim2
  - `$tscpt_ee_lim3`: $tscft_ee_lim3
  - `$tscpt_er_rate5`: $tscft_er_rate5
  - `$tscpt_er_rate6`: $tscft_er_rate6
  - `$tscpt_er_rate7`: $tscft_er_rate7
  - `$tscpt_er_lim1`: $tscft_er_lim1
  - `$tscpt_er_lim2`: $tscft_er_lim2
  - `$tscpt_er_lim3`: $tscft_er_lim3

### 7. Function: DefConst
  **Constants Defined:**
  - `$tscag_bs_minamt1`: 1929.00#m
  - `$tscag_bs_minamt2`: 1599.60#m
  - `$tscag_bs_minamt3`: 1391.70#m
  - `$tscag_bs_minamt4`: 1381.20#m
  - `$tscag_bs_minamt5`: 1381.20#m
  - `$tscag_bs_maxamt`: 4909.50#m
  - `$tscag_ee_rate1`: 0.047
  - `$tscag_ee_rate2`: 0.0155
  - `$tscag_ee_rate3`: 0.0003
  - `$tscag_er_rate1`: 0.2096
  - `$tscag_er_rate2`: 0.055
  - `$tscag_er_rate3`: 0.0025
  - `$tscag_ee_rate4`: 0.0013
  - `$tscag_er_rate4`: 0.0067
  - `$tscag_ee_rate5`: $tscft_ee_rate5
  - `$tscag_ee_rate6`: $tscft_ee_rate6
  - `$tscag_ee_rate7`: $tscft_ee_rate7
  - `$tscag_ee_lim1`: $tscft_ee_lim1
  - `$tscag_ee_lim2`: $tscft_ee_lim2
  - `$tscag_ee_lim3`: $tscft_ee_lim3
  - `$tscag_er_rate5`: $tscft_er_rate5
  - `$tscag_er_rate6`: $tscft_er_rate6
  - `$tscag_er_rate7`: $tscft_er_rate7
  - `$tscag_er_lim1`: $tscft_er_lim1
  - `$tscag_er_lim2`: $tscft_er_lim2
  - `$tscag_er_lim3`: $tscft_er_lim3

### 8. Function: DefConst *(Switch: off)*
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

### 9. Function: DefConst
  **Constants Defined:**
  - `$bsa00_BTA_rate`: 1
  - `$bsa00_BCA_rate`: 1


---

## Policy: neg_es
### 1. Function: DefVar
  - **i_yse0**: `0`

### 2. Function: ArithOp
  **Formula:** `yse`
  **Output Variable:** `i_yse0`
  **Tax Unit:** `tu_individual_es`

### 3. Function: Max
  - **val**: `0`
  - **output_var**: `yse`
  - **TAX_UNIT**: `tu_individual_es`


---

## Policy: prelim_es
### 1. Function: BenCalc
  - **comp_cond**: `lhw > 30`
  - **comp_perTU**: `1`
  - **output_var**: `liwft_s`
  - **TAX_UNIT**: `tu_individual_es`

### 2. Function: BenCalc
  - **comp_cond**: `dag <= 17`
  - **comp_perTU**: `5`
  - **output_var**: `sin27_s`
  - **TAX_UNIT**: `tu_individual_es`

### 3. Function: ArithOp *(Switch: off)*
  **Formula:** `bsa`
  **Output Variable:** `bsa_s`
  **Tax Unit:** `tu_individual_es`

### 4. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `bsarg_s`
  **Tax Unit:** `tu_individual_es`

### 5. Function: DefVar
  - **i_reg_61**: `0`
  - **i_reg_24**: `0`
  - **i_reg_12**: `0`
  - **i_reg_53**: `0`
  - **i_reg_70**: `0`
  - **i_reg_13**: `0`
  - **i_reg_42**: `0`
  - **i_reg_41**: `0`
  - **i_reg_51**: `0`
  - **i_reg_43**: `0`
  - **i_reg_11**: `0`
  - **i_reg_23**: `0`
  - **i_reg_30**: `0`
  - **i_reg_62**: `0`
  - **i_reg_22**: `0`
  - **i_reg_52**: `0`
  - **i_reg_21**: `0`
  - **i_reg_63**: `0`
  - **i_reg_64**: `0`
  - **Var_Monetary**: `no`

### 6. Function: BenCalc
  - **comp_cond**: `drgn2 = 61`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_61`
  - **TAX_UNIT**: `tu_individual_es`

### 7. Function: BenCalc
  - **comp_cond**: `drgn2 = 24`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_24`
  - **TAX_UNIT**: `tu_individual_es`

### 8. Function: BenCalc
  - **comp_cond**: `drgn2 = 12`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_12`
  - **TAX_UNIT**: `tu_individual_es`

### 9. Function: BenCalc
  - **comp_cond**: `drgn2 = 53`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_53`
  - **TAX_UNIT**: `tu_individual_es`

### 10. Function: BenCalc
  - **comp_cond**: `drgn2 = 70`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_70`
  - **TAX_UNIT**: `tu_individual_es`

### 11. Function: BenCalc
  - **comp_cond**: `drgn2 = 13`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_13`
  - **TAX_UNIT**: `tu_individual_es`

### 12. Function: BenCalc
  - **comp_cond**: `drgn2 = 42`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_42`
  - **TAX_UNIT**: `tu_individual_es`

### 13. Function: BenCalc
  - **comp_cond**: `drgn2 = 41`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_41`
  - **TAX_UNIT**: `tu_individual_es`

### 14. Function: BenCalc
  - **comp_cond**: `drgn2 = 51`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_51`
  - **TAX_UNIT**: `tu_individual_es`

### 15. Function: BenCalc
  - **comp_cond**: `drgn2 = 43`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_43`
  - **TAX_UNIT**: `tu_individual_es`

### 16. Function: BenCalc
  - **comp_cond**: `drgn2 = 11`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_11`
  - **TAX_UNIT**: `tu_individual_es`

### 17. Function: BenCalc
  - **comp_cond**: `drgn2 = 23`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_23`
  - **TAX_UNIT**: `tu_individual_es`

### 18. Function: BenCalc
  - **comp_cond**: `drgn2 = 30`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_30`
  - **TAX_UNIT**: `tu_individual_es`

### 19. Function: BenCalc
  - **comp_cond**: `drgn2 = 62`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_62`
  - **TAX_UNIT**: `tu_individual_es`

### 20. Function: BenCalc
  - **comp_cond**: `drgn2 = 22`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_22`
  - **TAX_UNIT**: `tu_individual_es`

### 21. Function: BenCalc
  - **comp_cond**: `drgn2 = 52`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_52`
  - **TAX_UNIT**: `tu_individual_es`

### 22. Function: BenCalc
  - **comp_cond**: `drgn2 = 21`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_21`
  - **TAX_UNIT**: `tu_individual_es`

### 23. Function: BenCalc
  - **comp_cond**: `drgn2 = 63`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_63`
  - **TAX_UNIT**: `tu_individual_es`

### 24. Function: BenCalc
  - **comp_cond**: `drgn2 = 64`
  - **comp_perElig**: `1`
  - **output_var**: `i_reg_64`
  - **TAX_UNIT**: `tu_individual_es`

### 25. Function: DefVar
  - **i_apr**: `0`

### 26. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `bsa00_s`
  **Tax Unit:** `tu_individual_es`

### 27. Function: ArithOp
  **Formula:** `(ypr*12)/$prelim_ry_rate`
  **Output Variable:** `i_apr`
  **Tax Unit:** `tu_bsa00`

### 28. Function: DefConst
  **Constants Defined:**
  - `$prelim_ry_rate`: 0.045


---

## Policy: yem_es *(Switch: switch)*
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem > 0`
  - **Tax Unit:** `tu_individual_es`

### 2. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **Comp_Cond**: `(yem * 12 / yemmy) / lhw >= $SMI * (14/12) / $lhw`
  - **Comp_perElig**: `yem`
  - **output_var**: `yem_s`
  - **TAX_UNIT**: `tu_individual_es`

### 3. Function: ArithOp
  **Formula:** `yem_s`
  **Output Variable:** `yem`
  **Tax Unit:** `tu_individual_es`

### 4. Function: ChangeParam
  - **Param_Id**: `c3701adf-b354-4434-9e74-741bdab12f24`
  - **Param_NewVal**: `es_2025_yem_std`


---

## Policy: tscft_es
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lindi != 1 & liwft_s =1 & yemxm_s > 0`
  - **Tax Unit:** `tu_individual_es`

### 2. Function: ArithOp
  **Formula:** `1`
  **Output Variable:** `sin01_s`
  **Tax Unit:** `tu_individual_es`

### 3. Function: ArithOp
  **Formula:** `(yemmy / 12)`
  **Output Variable:** `tsceemy_s`
  **Tax Unit:** `tu_individual_es`

### 4. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `sin27_s = 5`
  - **comp_perTU**: `max($tscft_ftbs_minamt5,yemxm_s)`
  - **uplim**: `$tscft_ftbs_maxamt`
  - **output_var**: `tsctbee_s`
  - **TAX_UNIT**: `tu_individual_es`

### 5. Function: ArithOp
  **Formula:** `tsctbee_s * $tscft_ee_rate1 * tsceemy_s`
  **Output Variable:** `tsceepi_s`
  **Tax Unit:** `tu_individual_es`

### 6. Function: ArithOp
  **Formula:** `tsctbee_s * $tscft_ee_rate2 * tsceemy_s`
  **Output Variable:** `tsceeui_s`
  **Tax Unit:** `tu_individual_es`

### 7. Function: ArithOp
  **Formula:** `tsctbee_s * $tscft_ee_rate3 * tsceemy_s`
  **Output Variable:** `tsceeot_s`
  **Tax Unit:** `tu_individual_es`

### 8. Function: ArithOp
  **Formula:** `tsceepi_s + tsceeui_s + tsceeot_s + tsceeie_s + tsceeas_s`
  **Output Variable:** `tscee_s`
  **Tax Unit:** `tu_individual_es`

### 9. Function: ArithOp
  **Formula:** `tsctbee_s * $tscft_er_rate1 * tsceemy_s`
  **Output Variable:** `tscerpi_s`
  **Tax Unit:** `tu_individual_es`

### 10. Function: ArithOp
  **Formula:** `tsctbee_s * $tscft_er_rate2 * tsceemy_s`
  **Output Variable:** `tscerui_s`
  **Tax Unit:** `tu_individual_es`

### 11. Function: ArithOp
  **Formula:** `tsctbee_s * $tscft_er_rate3 * tsceemy_s`
  **Output Variable:** `tscerot_s`
  **Tax Unit:** `tu_individual_es`

### 12. Function: ArithOp
  **Formula:** `tscerpi_s + tscerui_s + tscerot_s + tscerie_s + tsceras_s`
  **Output Variable:** `tscer_s`
  **Tax Unit:** `tu_individual_es`

### 13. Function: BenCalc
  - **comp_cond**: `yem > 0`
  - **comp_perTU**: `yem * (12 / yemmy)`
  - **output_var**: `yemxm_s`
  - **TAX_UNIT**: `tu_individual_es`

### 14. Function: ArithOp
  **Formula:** `tsctbee_s * $tscft_ee_rate4 * tsceemy_s`
  **Output Variable:** `tsceeie_s`
  **Tax Unit:** `tu_individual_es`

### 15. Function: ArithOp
  **Formula:** `tsctbee_s * $tscft_er_rate4 * tsceemy_s`
  **Output Variable:** `tscerie_s`
  **Tax Unit:** `tu_individual_es`

### 16. Function: BenCalc
  - **Comp_Cond**: `yemxm_s > $tscft_ee_lim3`
  - **Comp_perElig**: `((($tscft_ee_lim2 - $tscft_ee_lim1) * $tscft_ee_rate5) + (($tscft_ee_lim3 - $tscft_ee_lim2) * $tscft_ee_rate6) + ((yemxm_s - $tscft_ee_lim3) * $tscft_ee_rate7)) * tsceemy_s`
  - **Output_Var**: `tsceeas_s`
  - **TAX_UNIT**: `tu_individual_es`

### 17. Function: BenCalc
  - **Comp_Cond**: `yemxm_s > $tscft_er_lim3`
  - **Comp_perTU**: `((($tscft_er_lim2 - $tscft_er_lim1) * $tscft_er_rate5) + (($tscft_er_lim3 - $tscft_er_lim2) * $tscft_er_rate6) + ((yemxm_s - $tscft_er_lim3) * $tscft_er_rate7)) * tsceemy_s`
  - **Output_Var**: `tsceras_s`
  - **TAX_UNIT**: `tu_individual_es`


---

## Policy: tscpt_es
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lindi != 1 & liwft_s !=1 & yemxm_s > 0`
  - **Tax Unit:** `tu_individual_es`

### 2. Function: ArithOp
  **Formula:** `2`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 3. Function: ArithOp
  **Formula:** `(yemmy / 12)`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 4. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `sin27_s = 5`
  - **comp_perTU**: `max($tscpt_ptbs_minamt5*lhw*52/12,yemxm_s)`
  - **uplim**: `$tscpt_ptbs_maxamt`
  - **output_add_var**: `tsctbee_s`
  - **TAX_UNIT**: `tu_individual_es`

### 5. Function: ArithOp
  **Formula:** `tsctbee_s * $tscpt_ee_rate1 * tsceemy_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 6. Function: ArithOp
  **Formula:** `tsctbee_s * $tscpt_ee_rate2 * tsceemy_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 7. Function: ArithOp
  **Formula:** `tsctbee_s * $tscpt_ee_rate3 * tsceemy_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 8. Function: ArithOp
  **Formula:** `tsceepi_s + tsceeui_s + tsceeot_s + tsceeie_s + tsceeas_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 9. Function: ArithOp
  **Formula:** `tsctbee_s * $tscpt_er_rate1 * tsceemy_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 10. Function: ArithOp
  **Formula:** `tsctbee_s * $tscpt_er_rate2 * tsceemy_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 11. Function: ArithOp
  **Formula:** `tsctbee_s * $tscpt_er_rate3 * tsceemy_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 12. Function: ArithOp
  **Formula:** `tscerpi_s + tscerui_s + tscerot_s + tscerie_s + tsceras_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 13. Function: ArithOp
  **Formula:** `tsctbee_s * $tscpt_ee_rate4 * tsceemy_s`
  **Output Variable:** `tsceeie_s`
  **Tax Unit:** `tu_individual_es`

### 14. Function: ArithOp
  **Formula:** `tsctbee_s * $tscpt_er_rate4 * tsceemy_s`
  **Output Variable:** `tscerie_s`
  **Tax Unit:** `tu_individual_es`

### 15. Function: BenCalc
  - **Comp_Cond**: `yemxm_s > $tscpt_ee_lim3`
  - **Comp_perTU**: `((($tscpt_ee_lim2 - $tscpt_ee_lim1) * $tscpt_ee_rate5) + (($tscpt_ee_lim3 - $tscpt_ee_lim2) * $tscpt_ee_rate6) + ((yemxm_s - $tscpt_ee_lim3) * $tscpt_ee_rate7)) * tsceemy_s`
  - **Output_Var**: `tsceeas_s`
  - **TAX_UNIT**: `tu_individual_es`

### 16. Function: BenCalc
  - **Comp_Cond**: `yemxm_s > $tscpt_er_lim3`
  - **Comp_perTU**: `((($tscpt_er_lim2 - $tscpt_er_lim1) * $tscpt_er_rate5) + (($tscpt_er_lim3 - $tscpt_er_lim2) * $tscpt_er_rate6) + ((yemxm_s - $tscpt_er_lim3) * $tscpt_er_rate7)) * tsceemy_s`
  - **Output_Var**: `tsceras_s`
  - **TAX_UNIT**: `tu_individual_es`


---

## Policy: tscag_es
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lindi = 1 & yemxm_s > 0`
  - **Tax Unit:** `tu_individual_es`

### 2. Function: ArithOp
  **Formula:** `3`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 3. Function: ArithOp
  **Formula:** `(yemmy / 12)`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 4. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `sin27_s = 5`
  - **comp_perTU**: `$tscag_bs_minamt5`
  - **uplim**: `$tscag_bs_maxamt`
  - **output_add_var**: `tsctbee_s`
  - **TAX_UNIT**: `tu_individual_es`

### 5. Function: ArithOp
  **Formula:** `tsctbee_s * $tscag_ee_rate1 * tsceemy_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 6. Function: ArithOp
  **Formula:** `tsctbee_s * $tscag_ee_rate2 * tsceemy_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 7. Function: ArithOp
  **Formula:** `tsctbee_s * $tscag_ee_rate3 * tsceemy_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 8. Function: ArithOp
  **Formula:** `tsceepi_s + tsceeui_s + tsceeot_s + tsceeie_s + tsceeas_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 9. Function: ArithOp
  **Formula:** `tsctbee_s * $tscag_er_rate1 * tsceemy_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 10. Function: ArithOp
  **Formula:** `tsctbee_s * $tscag_er_rate2 * tsceemy_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 11. Function: ArithOp
  **Formula:** `tsctbee_s * $tscag_er_rate3 * tsceemy_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 12. Function: ArithOp
  **Formula:** `tscerpi_s + tscerui_s + tscerot_s + tscerie_s + tsceras_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 13. Function: ArithOp
  **Formula:** `tsctbee_s * $tscag_ee_rate4 * tsceemy_s`
  **Output Variable:** `tsceeie_s`
  **Tax Unit:** `tu_individual_es`

### 14. Function: ArithOp
  **Formula:** `tsctbee_s * $tscag_er_rate4 * tsceemy_s`
  **Output Variable:** `tscerie_s`
  **Tax Unit:** `tu_individual_es`

### 15. Function: BenCalc
  - **Comp_Cond**: `yemxm_s > $tscag_ee_lim3`
  - **Comp_perTU**: `((($tscag_ee_lim2 - $tscag_ee_lim1) * $tscag_ee_rate5) + (($tscag_ee_lim3 - $tscag_ee_lim2) * $tscag_ee_rate6) + ((yemxm_s - $tscag_ee_lim3) * $tscag_ee_rate7)) * tsceemy_s`
  - **Output_Var**: `tsceeas_s`
  - **TAX_UNIT**: `tu_individual_es`

### 16. Function: BenCalc
  - **Comp_Cond**: `yemxm_s > $tscag_er_lim3`
  - **Comp_perTU**: `((($tscag_er_lim2 - $tscag_er_lim1) * $tscag_er_rate5) + (($tscag_er_lim3 - $tscag_er_lim2) * $tscag_er_rate6) + ((yemxm_s - $tscag_er_lim3) * $tscag_er_rate7)) * tsceemy_s`
  - **Output_Var**: `tsceras_s`
  - **TAX_UNIT**: `tu_individual_es`


---

## Policy: tscse_es
### 1. Function: DefConst
  **Constants Defined:**
  - `$tscse_agebs_minamt1`: n/a
  - `$tscse_agebs_maxamt1`: n/a
  - `$tscse_se_rate1`: 0.283
  - `$tscse_se_rate2`: n/a
  - `$tscse_agebs_minamt2`: n/a
  - `$tscse_agebs_maxamt2`: n/a
  - `$tscse_agebs2018_minamt1`: n/a
  - `$tscse_agebs2018_minamt2`: n/a
  - `$tscse_se_redcoef`: 0.055
  - `$tscse_se_rate3`: 0.013
  - `$tscse_se_rate4`: 0.01
  - `$tscse_bs_minamt1`: 653.59#m
  - `$tscse_bs_minamt2`: 718.95#m
  - `$tscse_bs_minamt3`: 849.67#m
  - `$tscse_bs_minamt4`: 950.98#m
  - `$tscse_bs_minamt5`: 960.78#m
  - `$tscse_bs_minamt6`: 960.78#m
  - `$tscse_bs_minamt7`: 1143.79#m
  - `$tscse_bs_minamt8`: 1209.15#m
  - `$tscse_bs_minamt9`: 1274.51#m
  - `$tscse_bs_minamt10`: 1356.21#m
  - `$tscse_bs_minamt11`: 1437.91#m
  - `$tscse_bs_minamt12`: 1519.61#m
  - `$tscse_bs_minamt13`: 1601.31#m
  - `$tscse_bs_minamt14`: 1732.03#m
  - `$tscse_bs_minamt15`: 1928.10#m
  - `$tscse_se_rate5`: 0.008
  - `$tscse_yse_lim1`: 670
  - `$tscse_yse_lim2`: 900
  - `$tscse_yse_lim3`: 1166.7
  - `$tscse_yse_lim4`: 1300
  - `$tscse_yse_lim5`: 1500
  - `$tscse_yse_lim6`: 1700
  - `$tscse_yse_lim7`: 1850
  - `$tscse_yse_lim8`: 2030
  - `$tscse_yse_lim9`: 2330
  - `$tscse_yse_lim10`: 2760
  - `$tscse_yse_lim11`: 3190
  - `$tscse_yse_lim12`: 3620
  - `$tscse_yse_lim13`: 4050
  - `$tscse_yse_lim14`: 6000

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yse > 0 & lindi != 1`
  - **Tax Unit:** `tu_individual_es`

### 3. Function: ArithOp
  **Formula:** `1`
  **Output Variable:** `sin02_s`
  **Tax Unit:** `tu_individual_es`

### 4. Function: ArithOp
  **Formula:** `ysemy / 12`
  **Output Variable:** `tscsemy_s`
  **Tax Unit:** `tu_individual_es`

### 5. Function: ArithOp
  **Formula:** `sin42_s`
  **Output Variable:** `tsctbse_s`
  **Tax Unit:** `tu_individual_es`

### 6. Function: ArithOp
  **Formula:** `tscsepi_s + tscsehl_s + tscseot_s + tscseie_s`
  **Output Variable:** `tscse_s`
  **Tax Unit:** `tu_individual_es`

### 7. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 8. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 9. Function: BenCalc
  - **Comp_Cond**: `yse>0 & yemxm_s > 0`
  - **Comp_perTU**: `((tsctbse_s * $tscse_se_rate1) - (tsctbse_s * $tscse_se_rate1 *$tscse_se_redcoef)) * tscsemy_s`
  - **Output_Var**: `tscsepi_s`
  - **TAX_UNIT**: `tu_individual_es`
  - **Who_Must_Be_Elig**: `all`

### 10. Function: ArithOp
  **Formula:** `tsctbse_s*$tscse_se_rate3*tscsemy_s`
  **Output Variable:** `tscsehl_s`
  **Tax Unit:** `tu_individual_es`

### 11. Function: ArithOp
  **Formula:** `tsctbse_s*$tscse_se_rate4*tscsemy_s`
  **Output Variable:** `tscseot_s`
  **Tax Unit:** `tu_individual_es`

### 12. Function: BenCalc
  - **Comp_Cond**: `yse>$tscse_yse_lim14`
  - **Comp_perTU**: `$tscse_bs_minamt15`
  - **Output_Var**: `sin42_s`
  - **TAX_UNIT**: `tu_individual_es`

### 13. Function: ArithOp
  **Formula:** `tsctbse_s*$tscse_se_rate5*tscsemy_s`
  **Output Variable:** `tscseie_s`
  **Tax Unit:** `tu_individual_es`


---

## Policy: tscseag_es
### 1. Function: DefConst
  **Constants Defined:**
  - `$tscseag_agebs_minamt1`: n/a
  - `$tscseag_agebs_maxamt1`: n/a
  - `$tscseag_seag_rate1`: 0.1875
  - `$tscseag_seag_rate2`: 0.033
  - `$tscseag_seag_rate3`: 0.01
  - `$tscseag_bs_minamt1`: 653.59#m
  - `$tscseag_bs_minamt2`: 718.95#m
  - `$tscseag_bs_minamt3`: 849.67#m
  - `$tscseag_bs_minamt4`: 950.98#m
  - `$tscseag_bs_minamt5`: 960.78#m
  - `$tscseag_bs_minamt6`: 960.78#m
  - `$tscseag_bs_minamt7`: 1143.79#m
  - `$tscseag_bs_minamt8`: 1209.15#m
  - `$tscseag_bs_minamt9`: 1274.51#m
  - `$tscseag_bs_minamt10`: 1356.21#m
  - `$tscseag_bs_minamt11`: 1437.91#m
  - `$tscseag_bs_minamt12`: 1519.61#m
  - `$tscseag_bs_minamt13`: 1601.31
  - `$tscseag_bs_minamt14`: 1732.03#m
  - `$tscseag_bs_minamt15`: 1928.10#m
  - `$tscseag_seag_rate4`: 0.008
  - `$tscseag_seag_rate5`: 0.265
  - `$tscseag_seag_lim`: 1141.18#m

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yse > 0 & lindi = 1`
  - **Tax Unit:** `tu_individual_es`

### 3. Function: ArithOp
  **Formula:** `2`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 4. Function: ArithOp
  **Formula:** `ysemy / 12`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 5. Function: ArithOp
  **Formula:** `sin42_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 6. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 7. Function: ArithOp
  **Formula:** `tsctbse_s * $tscseag_seag_rate3 * tscsemy_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 8. Function: ArithOp
  **Formula:** `tsctbse_s * $tscseag_seag_rate2 * tscsemy_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 9. Function: ArithOp
  **Formula:** `tscsepi_s + tscsehl_s + tscseie_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 10. Function: BenCalc
  - **Comp_Cond**: `yse>$tscse_yse_lim14`
  - **Comp_perTU**: `$tscseag_bs_minamt15`
  - **Output_Var**: `sin42_s`
  - **TAX_UNIT**: `tu_individual_es`

### 11. Function: ArithOp
  **Formula:** `tsctbse_s * $tscseag_seag_rate4 * tscsemy_s`
  **Output Variable:** `tscseie_s`
  **Tax Unit:** `tu_individual_es`

### 12. Function: BenCalc
  - **Comp_Cond**: `tsctbse_s>$tscseag_seag_lim`
  - **Comp_perTU**: `$tscseag_seag_lim * $tscseag_seag_rate1 * tscsemy_s+(tsctbse_s -$tscseag_seag_lim) * $tscseag_seag_rate5 * tscsemy_s`
  - **Output_Add_Var**: `tscsepi_s`
  - **TAX_UNIT**: `tu_individual_es`


---

## Policy: bunct_es
### 1. Function: BenCalc
  - **comp_cond**: `lunmy > 0 & bunct = 0`
  - **comp_perElig**: `lunmy`
  - **output_var**: `lunmy_s`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_Cond**: `lunmy>0`
  - **Comp_perElig**: `lunmy`

### 2. Function: BenCalc
  - **comp_cond**: `bunct > 0`
  - **comp_perElig**: `max(min(yemmy*$UB_QperTot/12,liwwh),$UB_QperMin)`
  - **uplim**: `$UB_QperTot`
  - **output_var**: `liwmy_s`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_perElig**: `liwmy_a`
  - **Comp_Cond**: `lnu>0`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(bunct > 0 | lnu > 0 ) & liwmy_s >= $UB_QperMin & dag > 16 & dag < 65`
  - **Tax Unit:** `tu_individual_es`

### 4. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_es`
  - **Output Variable:** `bunctmy_s`

### 5. Function: ArithOp
  **Formula:** `min(bunctmy_s,lunmy_s)`
  **Output Variable:** `bunctmy_s`
  **Tax Unit:** `tu_individual_es`

### 6. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `bunctmy > 0`
  - **comp_perElig**: `min(bunctmy_s,bunctmy)`
  - **output_var**: `bunctmy_s`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_perTU**: `bunctmy_s`
  - **Comp_Cond**: `lnu>0 & bunctmy = 0`

### 7. Function: BenCalc
  - **comp_cond**: `nDepChInTu > 0`
  - **comp_perTU**: `(1+1/6) * (1.07 * $IPREM)`
  - **output_var**: `i_bunctmin`
  - **TAX_UNIT**: `tu_bunct`

### 8. Function: BenCalc
  - **comp_cond**: `nDepChInTu > 1`
  - **comp_perTU**: `(1+1/6) * (2.25 * $IPREM)`
  - **output_var**: `i_bunctmax`
  - **TAX_UNIT**: `tu_bunct`

### 9. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `bunctmy_s > 6`
  - **comp_perElig**: `yempv_s  * (6 * $bunct_rep_rate1 + (bunctmy_s - 6) * $bunct_rep_rate2) / bunctmy_s`
  - **lowlim**: `i_bunctmin#1 * i_ftprop`
  - **uplim**: `i_bunctmax#1 * i_ftprop`
  - **#_level**: `tu_bunct`
  - **output_var**: `i_bunct`
  - **TAX_UNIT**: `tu_individual_es`

### 10. Function: ArithOp
  **Formula:** `i_bunct * bunctmy_s / 12`
  **Output Variable:** `bunct_s`
  **Tax Unit:** `tu_individual_es`

### 11. Function: BenCalc
  - **Comp_Cond**: `liwwh>0`
  - **Comp_perTU**: `liwwh72_h * 30`
  - **Output_Var**: `i_liwwh`
  - **TAX_UNIT**: `tu_individual_es`
  - **Who_Must_Be_Elig**: `one`
  - **#_UpLim**: `$UB_QperTot`

### 12. Function: DefVar
  - **i_liwwh**: `0`
  - **i_bunctmax**: `0`
  - **i_bunctmin**: `0`
  - **i_bunct**: `0`
  - **i_ftprop**: `0`

### 13. Function: DefConst
  **Constants Defined:**
  - `$bunct_minlim1`: 360
  - `$bunct_my1`: 4
  - `$bunct_minlim2`: 540
  - `$bunct_my2`: 6
  - `$bunct_minlim3`: 720
  - `$bunct_my3`: 8
  - `$bunct_minlim4`: 900
  - `$bunct_my4`: 10
  - `$bunct_minlim5`: 1080
  - `$bunct_my5`: 12
  - `$bunct_minlim6`: 1260
  - `$bunct_my6`: 14
  - `$bunct_minlim7`: 1440
  - `$bunct_my7`: 16
  - `$bunct_minlim8`: 1620
  - `$bunct_my8`: 18
  - `$bunct_minlim9`: 1800
  - `$bunct_my9`: 20
  - `$bunct_minlim10`: 1980
  - `$bunct_my10`: 22
  - `$bunct_minlim11`: 2160
  - `$bunct_my11`: 24
  - `$bunct_rep_rate1`: 0.7
  - `$bunct_rep_rate2`: 0.6

### 14. Function: BenCalc
  - **Comp_Cond**: `bunctmy_s>0`
  - **Comp_perTU**: `lhwpv_h/$lhw`
  - **Output_Var**: `i_ftprop`
  - **TAX_UNIT**: `tu_individual_es`

### 15. Function: BenCalc
  - **Comp_Cond**: `bunctmy_s>0`
  - **Comp_perTU**: `bunctpc`
  - **Output_Var**: `yempv_s`
  - **TAX_UNIT**: `tu_individual_es`
  - **#_UpLim**: `$tscft_ftbs_maxamt`

### 16. Function: Elig *(Switch: toggle)*
  **Eligibility Check:**
  - **Condition:** `les=5 & liwwh72_h>=$UB_QperMin & dag>16 & dag<65`
  - **Tax Unit:** `tu_individual_es`

### 17. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `bunctmy_s > 6`
  - **comp_perElig**: `yempv_s * $bunct_rep_rate2`
  - **lowlim**: `i_bunctmin#1 * i_ftprop`
  - **uplim**: `i_bunctmax#1 * i_ftprop`
  - **#_level**: `tu_bunct`
  - **output_var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_es`

### 18. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `bunctmy_s < lunmy_s`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_es`


---

## Policy: bunnc_es
### 1. Function: DefIl
  - **name**: `il_bunnc`
  - **ils_origy**: `+`
  - **ils_pen**: `+`
  - **bhl**: `+`
  - **bed**: `+`
  - **bunct_s**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`

### 2. Function: DefTu
  - **Name**: `tu_bunnc`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `default & (dag < 26 | ddi > 0) & il_bunnc#1 <= $SMI * 0.75`
  - **#_level**: `tu_individual_es`

### 3. Function: BenCalc
  - **comp_cond**: `bunct_s = 0 & bunnc = 0 & lunmy > 0`
  - **comp_perElig**: `0`
  - **lowlim**: `0`
  - **output_var**: `i_bunncmy`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_Cond**: `bunct_s = 0 & (liwmy >= 3 | liwmy02_a >= 3) & lunmy > 0`
  - **Comp_perElig**: `liwmy`

### 4. Function: BenCalc
  - **comp_cond**: `idpartner > 0 & GetPartnerIncome#2 < $SMI * 0.75 `
  - **comp_perTU**: `1`
  - **#_level**: `tu_bunnc`
  - **#_income**: `il_bunnc`
  - **output_var**: `i_bunncnumdep`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_perTU**: `nDepChOfCouple#1`
  - **Comp_Cond**: `nDepChOfCouple#1 > 0`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(il_bunnc <= $SMI * 0.75 & il_bunnc#1 / nPersInUnit#1 < $SMI * 0.75) & i_bunncmy > 0 & ((dag > 45 & bunctmy00 >= 4) | (dag <= 45 & bunctmy00 >= 12) | (i_bunncnumdep > 0 & bunctmy00 >= 4) | ((liwmy >= 3 | liwmy02_a >= 3) & bunctmy00 = 0))`
  - **Tax Unit:** `tu_individual_es`

### 6. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 7. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `bunnc_s`
  - **TAX_UNIT**: `tu_individual_es`

### 8. Function: DefVar
  - **i_bunncmy**: `0`
  - **i_bunncnumdep**: `0`

### 9. Function: BenCalc *(Switch: toggle)*
  - **comp_cond**: `les=5 & bunct_s=0`
  - **comp_perElig**: `12`
  - **lowlim**: `0`
  - **output_var**: `i_bunncmy`
  - **TAX_UNIT**: `tu_individual_es`

### 10. Function: Elig *(Switch: toggle)*
  **Eligibility Check:**
  - **Condition:** `il_bunnc<=$SMI* 0.75 & il_bunnc#1 / nPersInUnit#1<$SMI*0.75 & i_bunncmy>0 & (dag>=45 | (i_bunncnumdep>0 | liwwh72_h>= 6))`
  - **Tax Unit:** `tu_individual_es`

### 11. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `bunnc_s`
  - **TAX_UNIT**: `tu_individual_es`

### 12. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `i_bunncmy > 0 & bunctmy00 = 0 & i_bunncnumdep > 0 & (liwmy >= 6 | liwmy02_a >= 6)`
  - **Comp_perElig**: `max(21,i_bunncmy)`
  - **Comp_UpLim**: `max(liwmy,liwmy02_a)`
  - **LowLim**: `0`
  - **UpLim**: `12`
  - **Output_Var**: `bunncmy_s`
  - **TAX_UNIT**: `tu_individual_es`


---

## Policy: bunmt_es
### 1. Function: DefConst
  **Constants Defined:**
  - `$bunmt_inc_lim`: 0.75
  - `$bunmt_amt`: 0.75

### 2. Function: DefTu
  - **Name**: `tu_bunmt`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild & DepParent`
  - **DepChildCond**: `default & (dag < 26 | ddi > 0)`
  - **DepParentCond**: `Default`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lunmy > (bunctmy_s + bunncmy_s) & il_bunnc <= ($SMI * $bunmt_inc_lim) & (il_bunnc#1 / nPersInUnit#1) < ($SMI * $bunmt_inc_lim) &  dag < 65 & bsa = 0 & (i_bunncnumdep > 0 | lunmy>=12)`
  - **Tax Unit:** `tu_individual_es`

### 4. Function: ArithOp
  **Formula:** `min(6,lunmy-(bunctmy_s+bunncmy_s))`
  **Output Variable:** `bunmtmy_s`
  **Tax Unit:** `tu_individual_es`

### 5. Function: ArithOp
  **Formula:** `($IPREM * $bunmt_amt) * bunmtmy_s / 12`
  **Output Variable:** `bunmt_s`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `IsUsedDatabase#1 | IsUsedDatabase#2`


---

## Policy: tscct_es
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bunct_s > 0`
  - **Tax Unit:** `tu_individual_es`

### 2. Function: ArithOp
  **Formula:** `bunctpc`
  **Output Variable:** `tsctbun_s`
  **Tax Unit:** `tu_individual_es`

### 3. Function: ArithOp
  **Formula:** `tsctbun_s * ($tscft_er_rate1) * bunctmy_s / 12`
  **Output Variable:** `tscuner_s`
  **Tax Unit:** `tu_individual_es`

### 4. Function: ArithOp
  **Formula:** `tsctbun_s * ($tscft_ee_rate1) * bunctmy_s / 12`
  **Output Variable:** `tscunee_s`
  **Tax Unit:** `tu_individual_es`

### 5. Function: DefVar
  - **i_tscer_cv19_rt**: `0`
  - **i_tscse_cv19_rt**: `0`
  - **Var_Monetary**: `no`

### 6. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `(bwkmceemy_s > 0)`
  - **Tax Unit:** `tu_individual_es`

### 7. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(lfs >= 50)`
  - **Comp_perTU**: `0.25`
  - **Output_Var**: `i_tscer_cv19_rt`
  - **TAX_UNIT**: `tu_individual_es`

### 8. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `all`
  - **Comp_Cond**: `(lindi=1)`
  - **Comp_perTU**: `(tsctbee_s * $tscag_er_rate1 * (1 - i_tscer_cv19_rt) * (bwkmceemy_s / 12)) * (1- lhwsr_s)`
  - **Output_Var**: `tsccterpi_s`
  - **TAX_UNIT**: `tu_individual_es`

### 9. Function: ArithOp *(Switch: n/a)*
  **Formula:** `-tsccterpi_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 10. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `all`
  - **Comp_Cond**: `(lindi=1)`
  - **Comp_perTU**: `tsctbee_s * $tscag_er_rate2
* (1-i_tscer_cv19_rt) * (bwkmceemy_s / 12) * (1- lhwsr_s)`
  - **Output_Var**: `tsccterui_s`
  - **TAX_UNIT**: `tu_individual_es`

### 11. Function: ArithOp *(Switch: n/a)*
  **Formula:** `-tsccterui_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 12. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `all`
  - **Comp_Cond**: `(lindi=1)`
  - **Comp_perTU**: `tsctbee_s * $tscag_er_rate3* (1-i_tscer_cv19_rt) * (bwkmceemy_s / 12) * (1- lhwsr_s)`
  - **Output_Var**: `tsccterot_s`
  - **TAX_UNIT**: `tu_individual_es`

### 13. Function: ArithOp *(Switch: n/a)*
  **Formula:** `-tsccterot_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 14. Function: ArithOp *(Switch: n/a)*
  **Formula:** `tsccterpi_s 
+ tsccterui_s + tsccterot_s`
  **Output Variable:** `tsccter_s`
  **Tax Unit:** `tu_individual_es`

### 15. Function: ArithOp *(Switch: n/a)*
  **Formula:** `tscerpi_s + tscerui_s + tscerot_s`
  **Output Variable:** `tscer_s`
  **Tax Unit:** `tu_individual_es`

### 16. Function: ArithOp *(Switch: n/a)*
  **Formula:** `tsctbee_s * $tscft_ee_rate1 * (bwkmceemy_s / 12) * (1- lhwsr_s)`
  **Output Variable:** `tscbeeepi_s`
  **Tax Unit:** `tu_individual_es`

### 17. Function: ArithOp *(Switch: n/a)*
  **Formula:** `-tscbeeepi_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 18. Function: ArithOp *(Switch: n/a)*
  **Formula:** `tsctbee_s * $tscft_ee_rate2 * (bwkmceemy_s / 12) * (1- lhwsr_s)`
  **Output Variable:** `tscbeeeui_s`
  **Tax Unit:** `tu_individual_es`

### 19. Function: ArithOp *(Switch: n/a)*
  **Formula:** `-tscbeeeui_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 20. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `all`
  - **Comp_Cond**: `(lindi=1)`
  - **Comp_perTU**: `tsctbee_s * $tscag_ee_rate3 * (bwkmceemy_s / 12) * (1- lhwsr_s)`
  - **Output_Var**: `tscbeeeot_s`
  - **TAX_UNIT**: `tu_individual_es`

### 21. Function: ArithOp *(Switch: n/a)*
  **Formula:** `-tscbeeeot_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 22. Function: ArithOp *(Switch: n/a)*
  **Formula:** `tsceepi_s + tsceeui_s + tsceeot_s`
  **Output Variable:** `tscee_s`
  **Tax Unit:** `tu_individual_es`

### 23. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `(bwkmcse_s > 0)`
  - **Tax Unit:** `tu_individual_es`

### 24. Function: ArithOp *(Switch: n/a)*
  **Formula:** `0`
  **Output Variable:** `i_tscse_cv19_rt`
  **Tax Unit:** `tu_individual_es`

### 25. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `all`
  - **Comp_Cond**: `i_yse_orig>0 & yemxm_s > 0`
  - **Comp_perTU**: `((tsctbse_s * $tscse_se_rate1) - (tsctbse_s * $tscse_se_rate1 *$tscse_se_redcoef)) * (1-i_tscse_cv19_rt) * (bwkmcsemy_s / 12) * (1- lhwsr_s)`
  - **Output_Var**: `tscctsepi_s`
  - **TAX_UNIT**: `tu_individual_es`

### 26. Function: ArithOp *(Switch: n/a)*
  **Formula:** `-tscctsepi_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_es`

### 27. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 28. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 29. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 30. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 31. Function: ArithOp *(Switch: n/a)*
  **Formula:** `tscsepi_s + tscsehl_s + tscseot_s`
  **Output Variable:** `tscse_s`
  **Tax Unit:** `tu_individual_es`

### 32. Function: ArithOp
  **Formula:** `tsctbun_s * ($tscft_ee_rate1)`
  **Output Variable:** `tscunee_s`
  **Tax Unit:** `tu_individual_es`


---

## Policy: poanc_es
### 1. Function: DefConst
  **Constants Defined:**
  - `$poanc_amt`: 7905.80#y
  - `$poanc_rent_amt`: 525#y

### 2. Function: DefConst
  **Constants Defined:**
  - `$poanc_rg61_amt1`: 186.45#y
  - `$poanc_rg24_amt1`: 700#y
  - `$poanc_rg12_amt1`: 0
  - `$poanc_rg53_amt1`: 0
  - `$poanc_rg70_amt1`: 0#y
  - `$poanc_rg13_amt1`: 0
  - `$poanc_rg42_amt1`: 0
  - `$poanc_rg41_amt1`: 0
  - `$poanc_rg51_amt1`: 0
  - `$poanc_rg43_amt1`: 265#y
  - `$poanc_rg11_amt1`: 220.50#y
  - `$poanc_rg23_amt1`: 0
  - `$poanc_rg30_amt1`: 0
  - `$poanc_rg62_amt1`: 0
  - `$poanc_rg22_amt1`: 0
  - `$poanc_rg52_amt1`: 0
  - `$poanc_rg21_amt1`: 0

### 3. Function: DefConst
  **Constants Defined:**
  - `$poanc_rg61_amt2`: 0
  - `$poanc_rg24_amt2`: 0
  - `$poanc_rg12_amt2`: 0
  - `$poanc_rg53_amt2`: 0
  - `$poanc_rg70_amt2`: 0
  - `$poanc_rg13_amt2`: 0
  - `$poanc_rg42_amt2`: 0
  - `$poanc_rg41_amt2`: 0
  - `$poanc_rg51_amt2`: 0
  - `$poanc_rg43_amt2`: 0
  - `$poanc_rg11_amt2`: 0
  - `$poanc_rg23_amt2`: 0
  - `$poanc_rg30_amt2`: 0
  - `$poanc_rg62_amt2`: 0
  - `$poanc_rg22_amt2`: 0
  - `$poanc_rg52_amt2`: 0
  - `$poanc_rg21_amt2`: 0

### 4. Function: DefVar
  - **i_poanc_reg_cm**: `0`
  - **i_poanc_reg_tu**: `0`
  - **i_poanc**: `0`
  - **i_poanc_test**: `0`

### 5. Function: ArithOp
  **Formula:** `$poanc_rg61_amt1 * i_reg_61 + $poanc_rg24_amt1 * i_reg_24 + $poanc_rg12_amt1 * i_reg_12 + $poanc_rg53_amt1 * i_reg_53 + $poanc_rg70_amt1 * i_reg_70 + $poanc_rg13_amt1 * i_reg_13 + $poanc_rg42_amt1 * i_reg_42 + $poanc_rg41_amt1 * i_reg_41 + $poanc_rg51_amt1 * i_reg_51 + $poanc_rg43_amt1 * i_reg_43 + $poanc_rg11_amt1 * i_reg_11 + $poanc_rg23_amt1 * i_reg_23 + $poanc_rg30_amt1 * i_reg_30 + $poanc_rg62_amt1 * i_reg_62 + $poanc_rg22_amt1 * i_reg_22 + $poanc_rg52_amt1 * i_reg_52 + $poanc_rg21_amt1 * i_reg_21`
  **Output Variable:** `i_poanc_reg_cm`
  **Tax Unit:** `tu_individual_es`

### 6. Function: ArithOp
  **Formula:** `$poanc_rg61_amt2 * i_reg_61 + $poanc_rg24_amt2 * i_reg_24 + $poanc_rg12_amt2 * i_reg_12 + $poanc_rg53_amt2 * i_reg_53 + $poanc_rg70_amt2 * i_reg_70 + $poanc_rg13_amt2 * i_reg_13 + $poanc_rg42_amt2 * i_reg_42 + $poanc_rg41_amt2 * i_reg_41 + $poanc_rg51_amt2 * i_reg_51 + $poanc_rg43_amt2 * i_reg_43 + $poanc_rg11_amt2 * i_reg_11 + $poanc_rg23_amt2 * i_reg_23 + $poanc_rg30_amt2 * i_reg_30 + $poanc_rg62_amt2 * i_reg_62 + $poanc_rg22_amt2 * i_reg_22 + $poanc_rg52_amt2 * i_reg_52 + $poanc_rg21_amt2 * i_reg_21`
  **Output Variable:** `i_poanc_reg_tu`
  **Tax Unit:** `tu_individual_es`

### 7. Function: DefIl
  - **name**: `il_poanc`
  - **ils_origy**: `+`
  - **ils_pen**: `+`
  - **bhl**: `+`
  - **bunnc_s**: `+`
  - **bunct_s**: `+`
  - **bma**: `+`
  - **bpact_s**: `+`
  - **bmanc_s**: `+`
  - **bmact_s**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`

### 8. Function: DefTu
  - **Name**: `tu_poanc`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & DepParent & OwnDepChild`
  - **DepChildCond**: `default & dag>=0`
  - **DepParentCond**: `default & dag>=65 & il_poanc < $poanc_amt`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`

### 9. Function: Elig *(Switch: off)*
  **Eligibility Check:**
  - **Condition:** `dag >= 65 & il_poanc#1 < i_poanc_test#1 & poa00 = 0`
  - **Tax Unit:** `tu_individual_es`

### 10. Function: Elig
  **Eligibility Check:**
  - **Condition:** `poanc > 0 & il_poanc#1 < i_poanc_test#1`
  - **Tax Unit:** `tu_individual_es`

### 11. Function: BenCalc
  - **comp_cond**: `nChOfCouple > 0`
  - **comp_perTU**: `$poanc_amt * (1 + (nPersInUnit - 1) * 0.7)`
  - **comp_perTu**: `$poanc_amt * (1 + (nPersInUnit - 1) * 0.7) * 2.5`
  - **output_var**: `i_poanc_test`
  - **TAX_UNIT**: `tu_poanc`

### 12. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `sel_s = 1`
  - **comp_perElig**: `$poanc_amt * 0.7`
  - **comp_perTu**: `$poanc_amt * 0.3`
  - **output_var**: `i_poanc`
  - **TAX_UNIT**: `tu_poanc`

### 13. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_poanc`
  - **share_between**: `sel_s = 1`
  - **share_equ_ifzero**: `no`
  - **share_all_ifnoelig**: `no`
  - **output_var**: `i_poanc`
  - **TAX_UNIT**: `tu_poanc`

### 14. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `il_poanc >= $poanc_amt * 0.35`
  - **comp_perElig**: `i_poanc`
  - **comp_perTu**: `i_poanc - (il_poanc - $poanc_amt * 0.35)`
  - **lowlim**: `0.25 * $poanc_amt`
  - **output_var**: `poanc00_s`
  - **TAX_UNIT**: `tu_individual_es`

### 15. Function: Elig
  **Eligibility Check:**
  - **Condition:** `poanc00_s > 0`
  - **Tax Unit:** `tu_individual_es`

### 16. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `amrtn = 3 | amrtn = 4 | amrtn = 5`
  - **comp_perElig**: `$poanc_rent_amt`
  - **output_var**: `poancna_s`
  - **TAX_UNIT**: `tu_individual_es`

### 17. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_poanc_reg_tu > poanc00_s`
  - **comp_perElig**: `i_poanc_reg_tu - poanc00_s`
  - **output_var**: `poancrg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 18. Function: ArithOp
  **Formula:** `poanc00_s + poancna_s + poancrg_s`
  **Output Variable:** `poanc_s`
  **Tax Unit:** `tu_individual_es`


---

## Policy: poacm_es
### 1. Function: DefConst
  **Constants Defined:**
  - `$poacm_minamt1`: 15786.40#y
  - `$poacm_minamt2`: 10824.80#y
  - `$poacm_minamt3`: 15786.40#y
  - `$poacm_minamt4`: 11620.00#y
  - `$poacm_inc_lim1`: 9193.00  #y
  - `$poacm_inc_lim2`: 10723.00 #y
  - `$poacm_minamt5`: 11452.00#y
  - `$poacm_minamt6`: 12241.60#y

### 2. Function: DefIl
  - **name**: `il_poacm`
  - **ils_origy**: `+`
  - **pdi**: `+`
  - **psu**: `+`
  - **bhl**: `+`
  - **bunnc_s**: `+`
  - **bunct_s**: `+`
  - **bed**: `+`
  - **poanc_s**: `+`
  - **bma**: `+`
  - **ils_sicee**: `-`
  - **bmact_s**: `+`
  - **bpact_s**: `+`
  - **bmanc_s**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`

### 3. Function: DefIl
  - **name**: `il_poacmds`
  - **ils_pen**: `+`
  - **poanc_s**: `+`

### 4. Function: Elig *(Switch: off)*
  **Eligibility Check:**
  - **Condition:** `poa00 > 0`
  - **Tax Unit:** `tu_individual_es`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `poa00 > 0 & poacm > 0`
  - **Tax Unit:** `tu_individual_es`

### 6. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dag >= 65 & i_partner = 3`
  - **comp_perElig**: `$poacm_minamt6`
  - **output_var**: `i_poacm`
  - **TAX_UNIT**: `tu_individual_es`

### 7. Function: DefVar
  - **i_poacm**: `0`
  - **i_partner**: `0`
  - **i_limit**: `0`

### 8. Function: BenCalc
  - **Comp_Cond**: `!IsWithPartner`
  - **Comp_perElig**: `3`
  - **#_Income**: `il_poacm`
  - **Output_Var**: `i_partner`
  - **TAX_UNIT**: `tu_individual_es`

### 9. Function: BenCalc
  - **Comp_Cond**: `i_partner = 2 | i_partner = 3`
  - **Comp_perTU**: `$poacm_inc_lim2`
  - **Output_Var**: `i_limit`
  - **TAX_UNIT**: `tu_individual_es`

### 10. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `il_poacm > i_limit & il_poacm + poa00 < i_limit + i_poacm`
  - **Comp_perTU**: `i_limit + i_poacm - (il_poacm + poa00)`
  - **LowLim**: `0`
  - **Output_Var**: `poacm_s`
  - **TAX_UNIT**: `tu_individual_es`

### 11. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `i_partner = 2 | i_partner = 3`
  - **Comp_perTU**: `poacm_s`
  - **Comp_UpLim**: `$poanc_amt`
  - **Output_Var**: `poacm_s`
  - **TAX_UNIT**: `tu_individual_es`


---

## Policy: psuwdcm_es
### 1. Function: DefConst
  **Constants Defined:**
  - `$psuwdcm_minamt1`: 0
  - `$psuwdcm_minamt2`: 9275.00#y
  - `$psuwdcm_minamt3`: 11452.00#y
  - `$psuwdcm_minamt4`: 12241.60#y
  - `$psuwdcm_minamt5`: 15786.40#y
  - `$psuwdcm_inc_lim`: 9193.00 #y

### 2. Function: DefIl
  - **name**: `il_psuwdcm`
  - **ils_origy**: `+`
  - **pdi**: `+`
  - **poa00**: `+`
  - **bhl**: `+`
  - **bunnc_s**: `+`
  - **bunct_s**: `+`
  - **bed**: `+`
  - **poanc_s**: `+`
  - **bma**: `+`
  - **ils_sicee**: `-`
  - **bmact_s**: `+`
  - **bpact_s**: `+`
  - **bmanc_s**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`

### 3. Function: DefTu
  - **Name**: `tu_psuwdcm`
  - **Type**: `SUBGROUP`
  - **Members**: `OwnDepChild`
  - **DepChildCond**: `default & (dag < 26 | ddi > 0) & il_psuwdcm#1 <= $SMI * 0.75`
  - **#_level**: `tu_individual_es`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`

### 4. Function: Elig *(Switch: off)*
  **Eligibility Check:**
  - **Condition:** `psuwd00 > 0`
  - **Tax Unit:** `tu_individual_es`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `psuwd00 > 0 & psuwdcm > 0`
  - **Tax Unit:** `tu_individual_es`

### 6. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu#1 > 0 & il_psuwdcm#1 < $SMI * 0.75 * nPersInTu#1`
  - **comp_perElig**: `$psuwdcm_minamt5`
  - **#_level**: `tu_psuwdcm`
  - **output_var**: `sin22_s`
  - **TAX_UNIT**: `tu_individual_es`

### 7. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `il_psuwdcm > $psuwdcm_inc_lim & il_psuwdcm + psuwd00 < $psuwdcm_inc_lim + sin22_s`
  - **comp_perTU**: `sin22_s - psuwd00`
  - **comp_perTu**: `$psuwdcm_inc_lim + sin22_s - (il_psuwdcm + psuwd00)`
  - **lowlim**: `0`
  - **output_var**: `psuwdcm_s`
  - **TAX_UNIT**: `tu_individual_es`
  - **UpLim**: `$poanc_amt`


---

## Policy: bch00_es
### 1. Function: DefConst
  **Constants Defined:**
  - `$bch00_inc_lim1`: 14952.00#y
  - `$bch00_inc_lim2`: 22501.00 #y
  - `$bch00_inc_lim3`: 3646.00 #y
  - `$bch00_amt1`: 0
  - `$bch00_amt2`: 0
  - `$bch00_amt3`: 0
  - `$bch00_amt4`: 1000.00#y
  - `$bch00_amt5`: 5805.60#Y
  - `$bch00_amt6`: 637.92#y
  - `$bch00_inc_lim4`: 4373 #y
  - `$bch00_nc_minamt`: 49#m

### 2. Function: DefTu
  - **Name**: `tu_bch00`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild & loosedepchild`
  - **DepChildCond**: `default & (dag < 18 | dag>18 & ddi>0) & il_bch00#1<=$SMI`
  - **#_level**: `tu_individual_es`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`
  - **LoneParentCond**: `Default`

### 3. Function: DefTu
  - **Name**: `tu_largefam`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `default & (dag < 21 | (dag < 26 & dec > 0) | ddi > 0) & il_bch00#1 <= $IPREM`
  - **#_level**: `tu_individual_es`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`

### 4. Function: ArithOp
  **Formula:** `ddi`
  **Output Variable:** `sin15_s`
  **Tax Unit:** `tu_individual_es`

### 5. Function: BenCalc
  - **comp_cond**: `sin15_s#1 > 0 & nDepChInTu#1 >= 2`
  - **comp_perTU**: `1`
  - **#_level**: `tu_largefam`
  - **output_var**: `dlg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 6. Function: BenCalc
  - **comp_cond**: `IsHead & dlg_s = 1 & nDepChInTu > 3`
  - **comp_perTU**: `$bch00_inc_lim3 * (nDepChInTu - 3)`
  - **output_var**: `sin03_s`
  - **TAX_UNIT**: `tu_bch00`

### 7. Function: BenCalc
  - **comp_cond**: `il_bch00 > sin03_s & nDepChildrenInTu>0 & ((sin03_s + ($bch00_amt3*nDepChildrenInTu#3) - il_bch00)) > ($bch00_amt3/12*nDepChildrenInTu#3)`
  - **comp_perTU**: `(sin03_s+$bch00_amt3*nDepChildrenInTu#3)-il_bch00`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `17`
  - **lowlim**: `0`
  - **output_var**: `bch00_s`
  - **TAX_UNIT**: `tu_bch00`

### 8. Function: DefTu
  - **Name**: `tu_bchdi`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `default & ddi > 0 & il_bch00#1<=$SMI`
  - **#_level**: `tu_individual_es`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`

### 9. Function: BenCalc
  - **comp_cond**: `IsParentOfDepChild > 0`
  - **comp_perTU**: `$bch00_amt5 * nDepChInTu#2`
  - **#_AgeMin**: `18`
  - **#_AgeMax**: `999`
  - **output_var**: `bchdi_s`
  - **TAX_UNIT**: `tu_bchdi`

### 10. Function: BenCalc
  - **Comp_Cond**: `!IsDepChild & !IsDepParent`
  - **Comp_perTU**: `il_bch00`
  - **Output_Var**: `i_il_bch00`
  - **TAX_UNIT**: `tu_bch00`

### 11. Function: DefVar
  - **i_il_bch00**: `0`

### 12. Function: BenCalc
  - **Comp_Cond**: `nDepChInTu > 0 & sin03_s > il_bch00 & i_il_bch00<$bch00_inc_lim4 + (($bch00_inc_lim4*0.5*(nPersInUnit#3-1)) + ($bch00_inc_lim4*0.3*nPersInUnit#4))`
  - **Comp_perTU**: `($bch00_amt6-$bch00_amt2)*nDepChildrenInTu#5`
  - **Output_Add_Var**: `bch00_s`
  - **TAX_UNIT**: `tu_bch00`
  - **#_AgeMax**: `17`
  - **#_AgeMin**: `0`
  - **LowLim**: `0`

### 13. Function: BenCalc
  - **Comp_Cond**: `bch00_s<$bch00_nc_minamt`
  - **Comp_perTU**: `-bch00_s`
  - **Output_Add_Var**: `bch00_s`
  - **TAX_UNIT**: `tu_bch00`


---

## Policy: bchbamtna_es
### 1. Function: DefConst
  **Constants Defined:**
  - `$bchbamtna_amt`: 1000.00#y
  - `$bchbamtna_minamt`: 10#y

### 2. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **lowlim**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 3. Function: BenCalc
  - **comp_cond**: `il_bch00 > sin03_s & nDepChildrenInTu#2>2 & ((sin03_s + $bchbamtna_amt - il_bch00)) > ($bchbamtna_minamt*nDepChildrenInTu#2)`
  - **comp_perTU**: `((sin03_s+$bchbamtna_amt)-il_bch00)* (nDepChInTu#1>0)`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `17`
  - **lowlim**: `0`
  - **output_var**: `bchbamtna_s`
  - **TAX_UNIT**: `tu_bch00`


---

## Policy: bchbaucna_es *(Switch: n/a)*
### 1. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$bchbaucna_newborn_amt`: n/a

### 2. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **lowlim**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: tin_cons_es
### 1. Function: DefConst
  **Constants Defined:**
  - `$tin_capinc_totrate1`: 0.19
  - `$tin_capinc_totrate2`: 0.21
  - `$tin_capinc_totrate3`: 0.23
  - `$tin_capinc_lim1`: 6000#y
  - `$tin_capinc_lim2`: 50000#y
  - `$tin_capinc_regrate3`: 0.115
  - `$tin_capinc_regrate2`: 0.105
  - `$tin_capinc_regrate1`: 0.095
  - `$tin_capinc_natrate3`: 0.115
  - `$tin_capinc_natrate2`: 0.105
  - `$tin_capinc_natrate1`: 0.095
  - `$tin_capinc_ratrate4`: 0.27
  - `$tin_capinc_natrate4`: 0.135
  - `$tin_capinc_regrate4`: 0.135
  - `$tin_capinc_lim3`: 200000#y
  - `$tin_capinc_ratrate5`: 0.30
  - `$tin_capinc_natrate5`: 0.14
  - `$tin_capinc_regrate5`: 0.14
  - `$tin_capinc_lim4`: 300000#y

### 2. Function: DefConst
  **Constants Defined:**
  - `$tin_perall_amt1`: 5550#y
  - `$tin_perall_amt2`: 1150#y
  - `$tin_perall_amt3`: 1400#y
  - `$tin_jointall_amt1`: 2150#y
  - `$tin_jointall_amt2`: 3400#y
  - `$tin_childall_amt1`: 2400#y
  - `$tin_childall_amt2`: 2700#y
  - `$tin_childall_amt3`: 4000#y
  - `$tin_childall_amt4`: 4500#y
  - `$tin_childall_amt5`: 2800#y
  - `$tin_childallrg30_amt3`: 4400#y
  - `$tin_childallrg30_amt4`: 4950#y
  - `$tin_depall_lim`: 8000#y
  - `$tin_depall_amt1`: 1150#y
  - `$tin_depall_amt2`: 1400#y
  - `$tin_empall_lim1`: 14852#y
  - `$tin_empall_lim2`: 17673.52#y
  - `$tin_empall_lim3`: 6500#y
  - `$tin_empall_maxamt`: 7302#y
  - `$tin_empall_minamt`: n/a
  - `$tin_empall_rate`: 1.14
  - `$tin_childallrg13_amt1`: n/a
  - `$tin_childallrg13_amt2`: n/a
  - `$tin_childallrg13_amt3`: n/a
  - `$tin_childallrg13_amt4`: n/a
  - `$tin_childallrg13_amt5`: n/a
  - `$tin_depallrg13_amt1`: 1150#y
  - `$tin_depallrg13_amt2`: 1400#y
  - `$tin_childallrg53_amt1`: 4400#y
  - `$tin_childallrg53_amt2`: 4950#y
  - `$tin_childallrg42_amt1`: n/a
  - `$tin_childallrg42_amt2`: n/a
  - `$tin_childallrg42_amt3`: n/a
  - `$tin_childallrg42_amt4`: n/a
  - `$tin_childallrg42_amt5`: n/a
  - `$tin_perallrg53_amt2`: 1265#y
  - `$tin_perallrg53_amt3`: 1540#y
  - `$tin_empded_amt`: 2000#y
  - `$tin_perallrg53_amt1`: 6105#y
  - `$tin_perallrg51_amt`: 6105#y
  - `$tin_perallrg51_lim`: 12450#y
  - `$tin_perallrg61_amt2`: 1200#y
  - `$tin_perallrg61_amt3`: 1460#y
  - `$tin_perallrg61_amt1`: 5790#y
  - `$tin_perallrg11_amt2`: 1199#y
  - `$tin_perallrg11_amt3`: 1460#y
  - `$tin_perallrg11_amt1`: 5789#y
  - `$tin_childallrg30_amt1`: 2575.85#y
  - `$tin_childallrg30_amt2`: 2897.83#y
  - `$tin_childallrg61_amt1`: 2510#y
  - `$tin_childallrg61_amt2`: 2820#y
  - `$tin_childallrg61_amt3`: 4170#y
  - `$tin_childallrg61_amt4`: 4700#y
  - `$tin_childallrg61_amt5`: 2920#y
  - `$tin_childallrg11_amt1`: 2503#y
  - `$tin_childallrg11_amt2`: 2816#y
  - `$tin_childallrg11_amt3`: 4172#y
  - `$tin_childallrg11_amt4`: 4694#y
  - `$tin_childallrg11_amt5`: 2920#y
  - `$tin_childallrg30_amt5`: 3005.16#y
  - `$tin_childallrg52_amt1`: 2640#y
  - `$tin_childallrg52_amt2`: 2970#y
  - `$tin_childallrg52_amt3`: 4400#y
  - `$tin_childallrg52_amt4`: 4950#y
  - `$tin_childallrg52_amt5`: 3080#y
  - `$tin_depallrg61_amt1`: 1200#y
  - `$tin_depallrg61_amt2`: 1460#y
  - `$tin_depallrg11_amt1`: 1199#y
  - `$tin_depallrg11_amt2`: 1460#y
  - `$tin_depallrg30_amt1`: 1234.26#y
  - `$tin_depallrg30_amt2`: 1502.58#y
  - `$tin_depallrg52_amt1`: 1265#y
  - `$tin_depallrg52_amt2`: 1540#y
  - `$tin_depallrg30_amt3`: 1234.26#y
  - `$tin_depallrg30_amt4`: 1502.58#y
  - `$tin_depallrg30_amt5`: 5956.65#y
  - `$tin_perallrg70_amt1`: 5606#y
  - `$tin_perallrg70_amt2`: 1162#y
  - `$tin_perallrg70_amt3`: 1414#y
  - `$tin_childallrg70_amt1`: 2424#y
  - `$tin_childallrg70_amt2`: 2727#y
  - `$tin_childallrg70_amt3`: 4040#y
  - `$tin_childallrg70_amt4`: 4545#y
  - `$tin_childallrg70_amt5`: 2828#y
  - `$tin_depallrg70_amt1`: 1162#y
  - `$tin_depallrg70_amt2`: 1414#y
  - `$tin_pen_amt1`: 1500#y
  - `$tin_pen_amt2`: n/a
  - `$tin_empall_lim4`: 19747.5#y
  - `$tin_empall_maxamt2`: 2364.34#y
  - `$tin_empall_rate2`: 1.75

### 3. Function: DefConst
  **Constants Defined:**
  - `$tin_upthres1`: 12450.00#y
  - `$tin_upthres2`: 20200.00#y
  - `$tin_upthres3`: 35200.00#y
  - `$tin_upthres4`: 60000.00#y
  - `$tin_upthres5`: 300000.00#y
  - `$tin_upthres6`: 99999999999
  - `$tin_rate1`: 0.095
  - `$tin_rate2`: 0.12
  - `$tin_rate3`: 0.15
  - `$tin_rate4`: 0.185
  - `$tin_rate5`: 0.225
  - `$tin_rate6`: 0.245
  - `$tin_rate7`: 0

### 4. Function: DefConst
  **Constants Defined:**
  - `$tin_rg61_upthres1`: 13000#y
  - `$tin_rg61_upthres3`: 21100#y
  - `$tin_rg61_upthres5`: 35200#y
  - `$tin_rg61_upthres6`: 60000#y
  - `$tin_rg61_upthres7`: 99999999999
  - `$tin_rg61_upthres8`: 99999999999
  - `$tin_rg61_upthres9`: 99999999999
  - `$tin_ts_lt10_rg_61`: 99999999999
  - `$tin_ts_lt11_rg_61`: 99999999999
  - `$tin_rg61_rate1`: 0.0950
  - `$tin_rg61_rate3`: 0.12
  - `$tin_rg61_rate4`: 0.15
  - `$tin_rg61_rate6`: 0.185
  - `$tin_rg61_rate7`: 0.225
  - `$tin_rg61_rate8`: 0
  - `$tin_rg61_rate9`: 0
  - `$tin_rg61_rate10`: 0
  - `$tin_ts_rt11_rg_61`: 0

### 5. Function: DefConst
  **Constants Defined:**
  - `$tin_rg24_upthres1`: 13072.00#y
  - `$tin_rg24_upthres2`: 21210.00#y
  - `$tin_rg24_upthres3`: 36960.00#y
  - `$tin_rg24_upthres5`: 52500.00#y
  - `$tin_rg24_upthres6`: 60000.00#y
  - `$tin_rg24_upthres8`: 80000#y
  - `$tin_rg24_upthres9`: 90000.00#y
  - `$tin_ts_lt10_rg_24`: 130000.00#y
  - `$tin_ts_lt11_rg_24`: 99999999999
  - `$tin_rg24_rate1`: 0.095
  - `$tin_rg24_rate2`: 0.12
  - `$tin_rg24_rate3`: 0.15
  - `$tin_rg24_rate4`: 0.185
  - `$tin_rg24_rate5`: 0.205
  - `$tin_rg24_rate6`: 0.23
  - `$tin_rg24_rate7`: 0.24
  - `$tin_rg24_rate8`: 0.25
  - `$tin_rg24_rate9`: 0.255
  - `$tin_rg24_rate10`: 0

### 6. Function: DefConst
  **Constants Defined:**
  - `$tin_rg12_upthres1`: 12450.00#y
  - `$tin_rg12_upthres2`: 17707.20#y
  - `$tin_rg12_upthres4`: 33007.20#y
  - `$tin_rg12_upthres6`: 53407.20#y
  - `$tin_rg12_upthres8`: 70000.00#y
  - `$tin_rg12_upthres9`: 90000.00#y
  - `$tin_ts_lt10_rg_12`: 175000.00#y
  - `$tin_ts_lt11_rg_12`: 99999999999
  - `$tin_ts_lt12_rg_12`: 99999999999
  - `$tin_rg12_rate1`: 0.10
  - `$tin_rg12_rate2`: 0.12
  - `$tin_rg12_rate4`: 0.14
  - `$tin_rg12_rate5`: 0.185
  - `$tin_rg12_rate6`: 0.215
  - `$tin_rg12_rate7`: 0.225
  - `$tin_rg12_rate8`: 0.25
  - `$tin_rg12_rate9`: 0.255
  - `$tin_rg12_rate10`: 0
  - `$tin_ts_rt11_rg_12`: 0

### 7. Function: DefConst
  **Constants Defined:**
  - `$tin_rg53_upthres1`: 10000.00#y
  - `$tin_rg53_upthres3`: 18000.00#y
  - `$tin_rg53_upthres5`: 30000.00#y
  - `$tin_rg53_upthres7`: 48000.00#y
  - `$tin_rg53_upthres9`: 70000.00#y
  - `$tin_ts_lt10_rg_53`: 90000.00#y
  - `$tin_ts_lt11_rg_53`: 120000.00#y
  - `$tin_ts_lt12_rg_53`: 175000.00#y
  - `$tin_ts_lt14_rg_53`: 99999999999
  - `$tin_rg53_rate1`: 0.09
  - `$tin_rg53_rate3`: 0.1125
  - `$tin_rg53_rate5`: 0.1425
  - `$tin_rg53_rate7`: 0.1750
  - `$tin_rg53_rate9`: 0.19
  - `$tin_rg53_rate10`: 0.2175
  - `$tin_ts_rt11_rg_53`: 0.2275
  - `$tin_ts_rt12_rg_53`: 0.2375
  - `$tin_ts_rt14_rg_53`: 0.2475
  - `$tin_ts_rt15_rg_53`: 0

### 8. Function: DefConst
  **Constants Defined:**
  - `$tin_rg70_upthres1`: 13465.00#y
  - `$tin_rg70_upthres3`: 19022.00#y
  - `$tin_rg70_upthres6`: 35185.00#y
  - `$tin_ts_lt10_rg_70`: 56382.00#y
  - `$tin_ts_lt13_rg_70`: 91350.00#y
  - `$tin_ts_lt14_rg_70`: 121200.00#y
  - `$tin_ts_lt15_rg_70`: 99999999999
  - `$tin_ts_lt16_rg_70`: 99999999999
  - `$tin_ts_lt17_rg_70`: 99999999999
  - `$tin_rg70_rate1`: 0.09
  - `$tin_rg70_rate3`: 0.115
  - `$tin_rg70_rate6`: 0.14
  - `$tin_rg70_rate10`: 0.185
  - `$tin_ts_rt13_rg_70`: 0.235
  - `$tin_ts_rt14_rg_70`: 0.25
  - `$tin_ts_rt15_rg_70`: 0.26
  - `$tin_ts_rt16_rg_70`: 0
  - `$tin_ts_rt17_rg_70`: 0
  - `$tin_ts_rt18_rg_70`: 0

### 9. Function: DefConst
  **Constants Defined:**
  - `$tin_rg13_upthres1`: 13000#y
  - `$tin_rg13_upthres2`: 21000#y
  - `$tin_rg13_upthres3`: 35200#y
  - `$tin_rg13_upthres5`: 60000#y
  - `$tin_rg13_upthres6`: 90000#y
  - `$tin_rg13_upthres7`: 99999999999
  - `$tin_rg13_upthres9`: 99999999999
  - `$tin_ts_lt10_rg_13`: 99999999999
  - `$tin_ts_lt11_rg_13`: 99999999999
  - `$tin_rg13_rate1`: 0.085
  - `$tin_rg13_rate2`: 0.11
  - `$tin_rg13_rate3`: 0.145
  - `$tin_rg13_rate5`: 0.18
  - `$tin_rg13_rate6`: 0.225
  - `$tin_rg13_rate7`: 0.245
  - `$tin_rg13_rate8`: 0
  - `$tin_rg13_rate9`: 0
  - `$tin_rg13_rate10`: 0
  - `$tin_ts_rt11_rg_13`: 0

### 10. Function: DefConst
  **Constants Defined:**
  - `$tin_rg42_upthres1`: 12450.00#y
  - `$tin_rg42_upthres2`: 20200.00#y
  - `$tin_rg42_upthres3`: 35200.00#y
  - `$tin_rg42_upthres4`: 60000.00#y
  - `$tin_rg42_upthres6`: 99999999999
  - `$tin_rg42_upthres7`: 99999999999
  - `$tin_rg42_upthres8`: 99999999999
  - `$tin_rg42_upthres9`: 99999999999
  - `$tin_ts_lt10_rg_42`: 99999999999
  - `$tin_rg42_rate1`: 0.095
  - `$tin_rg42_rate2`: 0.12
  - `$tin_rg42_rate3`: 0.15
  - `$tin_rg42_rate4`: 0.185
  - `$tin_rg42_rate6`: 0.225
  - `$tin_rg42_rate7`: 0
  - `$tin_rg42_rate8`: 0
  - `$tin_rg42_rate9`: 0
  - `$tin_rg42_rate10`: 0
  - `$tin_ts_rt11_rg_42`: 0

### 11. Function: DefConst
  **Constants Defined:**
  - `$tin_rg41_upthres1`: 12450.00#y
  - `$tin_rg41_upthres2`: 20200.00#y
  - `$tin_rg41_upthres3`: 35200.00#y
  - `$tin_rg41_upthres4`: 53407.20#y
  - `$tin_rg41_upthres7`: 99999999999
  - `$tin_rg41_upthres8`: 99999999999
  - `$tin_rg41_upthres9`: 99999999999
  - `$tin_ts_lt10_rg_41`: 99999999999
  - `$tin_ts_lt11_rg_41`: 99999999999
  - `$tin_rg41_rate1`: 0.09
  - `$tin_rg41_rate2`: 0.12
  - `$tin_rg41_rate3`: 0.14
  - `$tin_rg41_rate4`: 0.185
  - `$tin_rg41_rate7`: 0.215
  - `$tin_rg41_rate8`: 0
  - `$tin_rg41_rate9`: 0
  - `$tin_rg41_rate10`: 0
  - `$tin_ts_rt11_rg_41`: 0
  - `$tin_ts_rt12_rg_41`: 0

### 12. Function: DefConst
  **Constants Defined:**
  - `$tin_rg51_upthres1`: 12450.00#y
  - `$tin_rg51_upthres5`: 17707.2#y
  - `$tin_rg51_upthres7`: 21000.00#y
  - `$tin_ts_lt10_rg_51`: 33007.2#y
  - `$tin_ts_lt11_rg_51`: 53407.2#y
  - `$tin_ts_lt12_rg_51`: 90000.00#y
  - `$tin_ts_lt13_rg_51`: 120000.00#y
  - `$tin_ts_lt14_rg_51`: 175000.00#y
  - `$tin_ts_lt15_rg_51`: 99999999999
  - `$tin_rg51_rate2`: 0.105
  - `$tin_rg51_rate5`: 0.12
  - `$tin_rg51_rate7`: 0.14
  - `$tin_rg51_rate10`: 0.15
  - `$tin_ts_rt11_rg_51`: 0.188
  - `$tin_ts_rt12_rg_51`: 0.215
  - `$tin_ts_rt13_rg_51`: 0.235
  - `$tin_ts_rt14_rg_51`: 0.245
  - `$tin_ts_rt15_rg_51`: 0.255
  - `$tin_ts_rt16_rg_51`: 0

### 13. Function: DefConst
  **Constants Defined:**
  - `$tin_rg43_upthres3`: 24200.0#y
  - `$tin_rg43_upthres4`: 35200.0#y
  - `$tin_rg43_upthres5`: 60000.0#y
  - `$tin_rg43_upthres6`: 80200.0#y
  - `$tin_rg43_upthres7`: 99200.0#y
  - `$tin_rg43_upthres8`: 120200.0#y
  - `$tin_ts_lt10_rg_43`: 99999999999
  - `$tin_rg43_rate3`: 0.16
  - `$tin_rg43_rate4`: 0.175
  - `$tin_rg43_rate5`: 0.21
  - `$tin_rg43_rate6`: 0.235
  - `$tin_rg43_rate7`: 0.24
  - `$tin_rg43_rate8`: 0.245
  - `$tin_rg43_rate10`: 0.25
  - `$tin_rg43_upthres2`: 20200.0#y
  - `$tin_rg43_upthres1`: 12450.0#y
  - `$tin_rg43_rate2`: 0.10
  - `$tin_rg43_rate1`: 0.08
  - `$tin_ts_rt11_rg_43`: 0

### 14. Function: DefConst
  **Constants Defined:**
  - `$tin_rg11_upthres1`: 12985.35#y
  - `$tin_rg11_upthres3`: 21068.60#y
  - `$tin_rg11_upthres5`: 35200#y
  - `$tin_rg11_upthres6`: 60000.00#y
  - `$tin_rg11_upthres7`: 99999999999
  - `$tin_rg11_upthres8`: 99999999999
  - `$tin_ts_lt10_rg_11`: 99999999999
  - `$tin_ts_lt11_rg_11`: 99999999999
  - `$tin_ts_lt12_rg_11`: 99999999999
  - `$tin_rg11_rate1`: 0.09
  - `$tin_rg11_rate3`: 0.1165
  - `$tin_rg11_rate5`: 0.149
  - `$tin_rg11_rate6`: 0.184
  - `$tin_rg11_rate7`: 0.225
  - `$tin_rg11_rate8`: 0
  - `$tin_rg11_rate10`: 0
  - `$tin_ts_rt11_rg_11`: 0
  - `$tin_ts_rt12_rg_11`: 0
  - `$tin_ts_rt13_rg_11`: 0

### 15. Function: DefConst
  **Constants Defined:**
  - `$tin_rg23_upthres1`: 12450.0#y
  - `$tin_rg23_upthres2`: 20200.0#y
  - `$tin_rg23_upthres3`: 35200.0#y
  - `$tin_rg23_upthres4`: 40000#y
  - `$tin_rg23_upthres5`: 50000#y
  - `$tin_rg23_upthres6`: 60000#y
  - `$tin_rg23_upthres8`: 120000#y
  - `$tin_rg23_upthres9`: 99999999999
  - `$tin_ts_lt10_rg_23`: 99999999999
  - `$tin_rg23_rate1`: 0.08
  - `$tin_rg23_rate2`: 0.106
  - `$tin_rg23_rate3`: 0.136
  - `$tin_rg23_rate4`: 0.178
  - `$tin_rg23_rate5`: 0.183
  - `$tin_rg23_rate6`: 0.19
  - `$tin_rg23_rate8`: 0.245
  - `$tin_rg23_rate9`: 0.27
  - `$tin_rg23_rate10`: 0
  - `$tin_ts_rt11_rg_23`: 0

### 16. Function: DefConst
  **Constants Defined:**
  - `$tin_rg30_upthres1`: 13362.22#y
  - `$tin_rg30_upthres3`: 19004.63#y
  - `$tin_rg30_upthres6`: 35425.68#y
  - `$tin_rg30_upthres9`: 57320.40#y
  - `$tin_ts_lt13_rg_30`: 99999999999
  - `$tin_ts_lt14_rg_30`: 99999999999
  - `$tin_ts_lt15_rg_30`: 99999999999
  - `$tin_ts_lt16_rg_30`: 99999999999
  - `$tin_ts_lt17_rg_30`: 99999999999
  - `$tin_rg30_rate1`: 0.085
  - `$tin_rg30_rate3`: 0.107
  - `$tin_rg30_rate6`: 0.128
  - `$tin_rg30_rate9`: 0.174
  - `$tin_ts_rt13_rg_30`: 0.205
  - `$tin_ts_rt14_rg_30`: 0
  - `$tin_ts_rt15_rg_30`: 0
  - `$tin_ts_rt16_rg_30`: 0
  - `$tin_ts_rt17_rg_30`: 0
  - `$tin_ts_rt18_rg_30`: 0

### 17. Function: DefConst
  **Constants Defined:**
  - `$tin_rg62_upthres1`: 12450.00#y
  - `$tin_rg62_upthres3`: 20200.00#y
  - `$tin_rg62_upthres5`: 34000.00#y
  - `$tin_rg62_upthres8`: 60000.00#y
  - `$tin_ts_lt10_rg_62`: 99999999999
  - `$tin_ts_lt11_rg_62`: 99999999999
  - `$tin_ts_lt12_rg_62`: 99999999999
  - `$tin_ts_lt13_rg_62`: 99999999999
  - `$tin_ts_lt14_rg_62`: 99999999999
  - `$tin_rg62_rate1`: 0.095
  - `$tin_rg62_rate3`: 0.112
  - `$tin_rg62_rate5`: 0.133
  - `$tin_rg62_rate8`: 0.179
  - `$tin_rg62_rate10`: 0.225
  - `$tin_ts_rt11_rg_62`: 0
  - `$tin_ts_r12_rg_62`: 0
  - `$tin_ts_rt13_rg_62`: 0
  - `$tin_ts_rt14_rg_62`: 0
  - `$tin_ts_rt15_rg_62`: 0

### 18. Function: DefConst
  **Constants Defined:**
  - `$tin_rg22_upthres1`: 12450.00#y
  - `$tin_rg22_upthres2`: 20200.00#y
  - `$tin_rg22_upthres3`: 35200.00#y
  - `$tin_rg22_upthres4`: 60000.00#y
  - `$tin_rg22_upthres6`: 300000#y
  - `$tin_rg22_upthres7`: 99999999999
  - `$tin_rg22_upthres8`: 99999999999
  - `$tin_rg22_upthres9`: 99999999999
  - `$tin_ts_lt10_rg_22`: 99999999999
  - `$tin_rg22_rate1`: 0.095
  - `$tin_rg22_rate2`: 0.12
  - `$tin_rg22_rate3`: 0.15
  - `$tin_rg22_rate4`: 0.185
  - `$tin_rg22_rate6`: 0.225
  - `$tin_rg22_rate7`: 0.245
  - `$tin_rg22_rate8`: 0
  - `$tin_rg22_rate9`: 0
  - `$tin_rg22_rate10`: 0
  - `$tin_ts_rt11_rg_22`: 0

### 19. Function: DefConst
  **Constants Defined:**
  - `$tin_rg52_upthres1`: 12000.00#y
  - `$tin_rg52_upthres3`: 22000.00#y
  - `$tin_rg52_upthres6`: 32000.00#y
  - `$tin_rg52_lim10`: 200000.00#y
  - `$tin_ts_lt14_rg_52`: 52000.00#y
  - `$tin_ts_lt16_rg_52`: 62000.00#y
  - `$tin_ts_lt18_rg_52`: 72000.00#y
  - `$tin_ts_lt24_rg_52`: 100000.00#y
  - `$tin_ts_lt25_rg_52`: 150000.00#y
  - `$tin_rg52_rate2`: 0.09
  - `$tin_rg52_rate3`: 0.12
  - `$tin_rg52_rate6`: 0.15
  - `$tin_rg52_rate10`: 0.175
  - `$tin_ts_rt14_rg_52`: 0.2
  - `$tin_ts_rt16_rg_52`: 0.225
  - `$tin_ts_rt18_rg_52`: 0.25
  - `$tin_ts_rt24_rg_52`: 0.265
  - `$tin_ts_rt25_rg_52`: 0.275
  - `$tin_ts_rt26_rg_52`: 0.285
  - `$tin_rg52_lim11`: 99999999999
  - `$tin_rg52_rate11`: 0.295
  - `$tin_rg52_rate12`: 0

### 20. Function: DefConst
  **Constants Defined:**
  - `$tin_rg21_upthres1`: 12450.00#y
  - `$tin_rg21_upthres2`: 20200.00#y
  - `$tin_rg21_upthres3`: 35200.00#y
  - `$tin_rg21_upthres4`: 60000.00#y
  - `$tin_rg21_upthres6`: 300000#y
  - `$tin_rg21_upthres7`: 99999999999
  - `$tin_rg21_upthres8`: 99999999999
  - `$tin_rg21_upthres9`: 99999999999
  - `$tin_ts_lt10_rg_21`: 99999999999
  - `$tin_rg21_rate1`: 0.095
  - `$tin_rg21_rate2`: 0.12
  - `$tin_rg21_rate3`: 0.15
  - `$tin_rg21_rate4`: 0.185
  - `$tin_rg21_rate6`: 0.225
  - `$tin_rg21_rate7`: 0.245
  - `$tin_rg21_rate8`: 0
  - `$tin_rg21_rate9`: 0
  - `$tin_rg21_rate10`: 0
  - `$tin_ts_rt11_rg_21`: 0

### 21. Function: DefConst
  **Constants Defined:**
  - `$tin_rg63_upthres1`: 12450.00#y
  - `$tin_rg63_upthres2`: 20200.00#y
  - `$tin_rg63_upthres4`: 34000.00#y
  - `$tin_rg63_upthres5`: 60000.00#y
  - `$tin_rg63_upthres7`: 99999999999
  - `$tin_rg63_upthres8`: 99999999999
  - `$tin_rg63_upthres9`: 99999999999
  - `$tin_ts_lt10_rg_63`: 99999999999
  - `$tin_ts_lt11_rg_63`: 99999999999
  - `$tin_rg63_rate1`: 0.095
  - `$tin_rg63_rate2`: 0.120
  - `$tin_rg63_rate4`: 0.150
  - `$tin_rg63_rate5`: 0.185
  - `$tin_rg63_rate7`: 0.225
  - `$tin_rg63_rate8`: 0
  - `$tin_rg63_rate9`: 0
  - `$tin_rg63_rate10`: 0
  - `$tin_ts_rt11_rg_63`: 0
  - `$tin_ts_rt12_rg_63`: 0

### 22. Function: DefConst
  **Constants Defined:**
  - `$tin_rg64_upthres1`: 12450.00#y
  - `$tin_rg64_upthres2`: 20200.00#y
  - `$tin_rg64_upthres4`: 34000.00#y
  - `$tin_rg64_upthres5`: 60000.00#y
  - `$tin_rg64_upthres7`: 99999999999
  - `$tin_rg64_upthres8`: 99999999999
  - `$tin_rg64_upthres9`: 99999999999
  - `$tin_ts_lt10_rg_64`: 99999999999
  - `$tin_ts_lt11_rg_64`: 99999999999
  - `$tin_rg64_rate1`: 0.095
  - `$tin_rg64_rate2`: 0.120
  - `$tin_rg64_rate4`: 0.150
  - `$tin_rg64_rate5`: 0.185
  - `$tin_rg64_rate7`: 0.225
  - `$tin_rg64_rate8`: 0
  - `$tin_rg64_rate9`: 0
  - `$tin_rg64_rate10`: 0
  - `$tin_ts_rt11_rg_64`: 0
  - `$tin_ts_rt12_rg_64`: 0

### 23. Function: DefVar
  - **v_tin_ts_lt1_rg**: `0`
  - **v_tin_ts_lt2_rg**: `0`
  - **v_tin_ts_lt3_rg**: `0`
  - **v_tin_ts_lt4_rg**: `0`
  - **v_tin_ts_lt5_rg**: `0`
  - **v_tin_ts_lt6_rg**: `0`
  - **v_tin_ts_lt7_rg**: `0`
  - **v_tin_ts_lt8_rg**: `0`
  - **v_tin_ts_lt9_rg**: `0`
  - **v_tin_ts_rt1_rg**: `0`
  - **v_tin_ts_rt2_rg**: `0`
  - **v_tin_ts_rt3_rg**: `0`
  - **v_tin_ts_rt4_rg**: `0`
  - **v_tin_ts_rt5_rg**: `0`
  - **v_tin_ts_rt6_rg**: `0`
  - **v_tin_ts_rt7_rg**: `0`
  - **v_tin_ts_rt8_rg**: `0`
  - **v_tin_ts_rt9_rg**: `0`
  - **v_tin_ts_rt10_rg**: `0`
  - **var_monetary**: `no`

### 24. Function: ArithOp
  **Formula:** `$tin_rg61_upthres1 * i_reg_61 + $tin_rg24_upthres1 * i_reg_24 + $tin_rg12_upthres1 * i_reg_12 + $tin_rg53_upthres1 * i_reg_53 + $tin_rg70_upthres1 * i_reg_70 + $tin_rg13_upthres1 * i_reg_13 + $tin_rg42_upthres1 * i_reg_42 + $tin_rg41_upthres1 * i_reg_41 + $tin_rg51_upthres1 * i_reg_51 + $tin_rg43_upthres1 * i_reg_43 + $tin_rg11_upthres1 * i_reg_11 + $tin_rg23_upthres1 * i_reg_23 + $tin_rg30_upthres1 * i_reg_30 + $tin_rg62_upthres1 * i_reg_62 + $tin_rg22_upthres1 * i_reg_22 + $tin_rg52_upthres1 * i_reg_52 + $tin_rg21_upthres1 * i_reg_21 + $tin_rg63_upthres1 * i_reg_63 + $tin_rg64_upthres1 * i_reg_64`
  **Output Variable:** `v_tin_ts_lt1_rg`
  **Tax Unit:** `tu_individual_es`

### 25. Function: ArithOp
  **Formula:** `$tin_rg61_upthres2 * i_reg_61 + $tin_rg24_upthres2 * i_reg_24 + $tin_rg12_upthres2 * i_reg_12 + $tin_rg53_upthres2 * i_reg_53 + $tin_rg70_upthres2 * i_reg_70 + $tin_rg13_upthres2 * i_reg_13 + $tin_rg42_upthres2 * i_reg_42 + $tin_rg41_upthres2 * i_reg_41 + $tin_rg51_upthres2 * i_reg_51 + $tin_rg43_upthres2 * i_reg_43 + $tin_rg11_upthres2 * i_reg_11 + $tin_rg23_upthres2 * i_reg_23 + $tin_rg30_upthres2 * i_reg_30 + $tin_rg62_upthres2 * i_reg_62 + $tin_rg22_upthres2 * i_reg_22 + $tin_rg52_upthres2 * i_reg_52 + $tin_rg21_upthres2 * i_reg_21 + $tin_rg63_upthres2 * i_reg_63 + $tin_rg64_upthres2 * i_reg_64`
  **Output Variable:** `v_tin_ts_lt2_rg`
  **Tax Unit:** `tu_individual_es`

### 26. Function: ArithOp
  **Formula:** `$tin_rg61_upthres3 * i_reg_61 + $tin_rg24_upthres3 * i_reg_24 + $tin_rg12_upthres3 * i_reg_12 + $tin_rg53_upthres3 * i_reg_53 + $tin_rg70_upthres3 * i_reg_70 + $tin_rg13_upthres3 * i_reg_13 + $tin_rg42_upthres3 * i_reg_42 + $tin_rg41_upthres3 * i_reg_41 + $tin_rg51_upthres3 * i_reg_51 + $tin_rg43_upthres3 * i_reg_43 + $tin_rg11_upthres3 * i_reg_11 + $tin_rg23_upthres3 * i_reg_23 + $tin_rg30_upthres3 * i_reg_30 + $tin_rg62_upthres3 * i_reg_62 + $tin_rg22_upthres3 * i_reg_22 + $tin_rg52_upthres3 * i_reg_52 + $tin_rg21_upthres3 * i_reg_21 + $tin_rg63_upthres3 * i_reg_63 + $tin_rg64_upthres3 * i_reg_64`
  **Output Variable:** `v_tin_ts_lt3_rg`
  **Tax Unit:** `tu_individual_es`

### 27. Function: ArithOp
  **Formula:** `$tin_rg61_upthres4 * i_reg_61 + $tin_rg24_upthres4 * i_reg_24 + $tin_rg12_upthres4 * i_reg_12 + $tin_rg53_upthres4 * i_reg_53 + $tin_rg70_upthres4 * i_reg_70 + $tin_rg13_upthres4 * i_reg_13 + $tin_rg42_upthres4 * i_reg_42 + $tin_rg41_upthres4 * i_reg_41 + $tin_rg51_upthres4 * i_reg_51 + $tin_rg43_upthres4 * i_reg_43 + $tin_rg11_upthres4 * i_reg_11 + $tin_rg23_upthres4 * i_reg_23 + $tin_rg30_upthres4 * i_reg_30 + $tin_rg62_upthres4 * i_reg_62 + $tin_rg22_upthres4 * i_reg_22 + $tin_rg52_upthres4 * i_reg_52 + $tin_rg21_upthres4 * i_reg_21 + $tin_rg63_upthres4 * i_reg_63 + $tin_rg64_upthres4 * i_reg_64`
  **Output Variable:** `v_tin_ts_lt4_rg`
  **Tax Unit:** `tu_individual_es`

### 28. Function: ArithOp
  **Formula:** `$tin_rg61_upthres5 * i_reg_61 + $tin_rg24_upthres5 * i_reg_24 + $tin_rg12_upthres5 * i_reg_12 + $tin_rg53_upthres5 * i_reg_53 + $tin_rg70_upthres5 * i_reg_70 + $tin_rg13_upthres5 * i_reg_13 + $tin_rg42_upthres5 * i_reg_42 + $tin_rg41_upthres5 * i_reg_41 + $tin_rg51_upthres5 * i_reg_51 + $tin_rg43_upthres5 * i_reg_43 + $tin_rg11_upthres5 * i_reg_11 + $tin_rg23_upthres5 * i_reg_23 + $tin_rg30_upthres5 * i_reg_30 + $tin_rg62_upthres5 * i_reg_62 + $tin_rg22_upthres5 * i_reg_22 + $tin_rg52_upthres5 * i_reg_52 + $tin_rg21_upthres5 * i_reg_21 + $tin_rg63_upthres5 * i_reg_63 + $tin_rg64_upthres5 * i_reg_64`
  **Output Variable:** `v_tin_ts_lt5_rg`
  **Tax Unit:** `tu_individual_es`

### 29. Function: ArithOp
  **Formula:** `$tin_rg61_upthres6 * i_reg_61 + $tin_rg24_upthres6 * i_reg_24 + $tin_rg12_upthres6 * i_reg_12 + $tin_rg53_upthres6 * i_reg_53 + $tin_rg70_upthres6 * i_reg_70 + $tin_rg13_upthres6 * i_reg_13 + $tin_rg42_upthres6 * i_reg_42 + $tin_rg41_upthres6 * i_reg_41 + $tin_rg51_upthres6 * i_reg_51 + $tin_rg43_upthres6 * i_reg_43 + $tin_rg11_upthres6 * i_reg_11 + $tin_rg23_upthres6 * i_reg_23 + $tin_rg30_upthres6 * i_reg_30 + $tin_rg62_upthres6 * i_reg_62 + $tin_rg22_upthres6 * i_reg_22 + $tin_rg52_upthres6 * i_reg_52 + $tin_rg21_upthres6 * i_reg_21 + $tin_rg63_upthres6 * i_reg_63 + $tin_rg64_upthres6 * i_reg_64`
  **Output Variable:** `v_tin_ts_lt6_rg`
  **Tax Unit:** `tu_individual_es`

### 30. Function: ArithOp
  **Formula:** `$tin_rg61_upthres7 * i_reg_61 + $tin_rg24_upthres7 * i_reg_24 + $tin_rg12_upthres7 * i_reg_12 + $tin_rg53_upthres7 * i_reg_53 + $tin_rg70_upthres7 * i_reg_70 + $tin_rg13_upthres7 * i_reg_13 + $tin_rg42_upthres7 * i_reg_42 + $tin_rg41_upthres7 * i_reg_41 + $tin_rg51_upthres7 * i_reg_51 + $tin_rg43_upthres7 * i_reg_43 + $tin_rg11_upthres7 * i_reg_11 + $tin_rg23_upthres7 * i_reg_23 + $tin_rg30_upthres7 * i_reg_30 + $tin_rg62_upthres7 * i_reg_62 + $tin_rg22_upthres7 * i_reg_22 + $tin_rg52_upthres7 * i_reg_52 + $tin_rg21_upthres7 * i_reg_21 + $tin_rg63_upthres7 * i_reg_63 + $tin_rg64_upthres7 * i_reg_64`
  **Output Variable:** `v_tin_ts_lt7_rg`
  **Tax Unit:** `tu_individual_es`

### 31. Function: ArithOp
  **Formula:** `$tin_rg61_upthres8 * i_reg_61 + $tin_rg24_upthres8 * i_reg_24 + $tin_rg12_upthres8 * i_reg_12 + $tin_rg53_upthres8 * i_reg_53 + $tin_rg70_upthres8 * i_reg_70 + $tin_rg13_upthres8 * i_reg_13 + $tin_rg42_upthres8 * i_reg_42 + $tin_rg41_upthres8 * i_reg_41 + $tin_rg51_upthres8 * i_reg_51 + $tin_rg43_upthres8 * i_reg_43 + $tin_rg11_upthres8 * i_reg_11 + $tin_rg23_upthres8 * i_reg_23 + $tin_rg30_upthres8 * i_reg_30 + $tin_rg62_upthres8 * i_reg_62 + $tin_rg22_upthres8 * i_reg_22 + $tin_rg52_upthres8 * i_reg_52 + $tin_rg21_upthres8 * i_reg_21 + $tin_rg63_upthres8 * i_reg_63 + $tin_rg64_upthres8 * i_reg_64`
  **Output Variable:** `v_tin_ts_lt8_rg`
  **Tax Unit:** `tu_individual_es`

### 32. Function: ArithOp
  **Formula:** `$tin_rg61_upthres9 * i_reg_61 + $tin_rg24_upthres9 * i_reg_24 + $tin_rg12_upthres9 * i_reg_12 + $tin_rg53_upthres9 * i_reg_53 + $tin_rg70_upthres9 * i_reg_70 + $tin_rg13_upthres9 * i_reg_13 + $tin_rg42_upthres9 * i_reg_42 + $tin_rg41_upthres9 * i_reg_41 + $tin_rg51_upthres9 * i_reg_51 + $tin_rg43_upthres9 * i_reg_43 + $tin_rg11_upthres9 * i_reg_11 + $tin_rg23_upthres9 * i_reg_23 + $tin_rg30_upthres9 * i_reg_30 + $tin_rg62_upthres9 * i_reg_62 + $tin_rg22_upthres9 * i_reg_22 + $tin_rg52_upthres9 * i_reg_52 + $tin_rg21_upthres9 * i_reg_21 + $tin_rg63_upthres9 * i_reg_63 + $tin_rg64_upthres9 * i_reg_64`
  **Output Variable:** `v_tin_ts_lt9_rg`
  **Tax Unit:** `tu_individual_es`

### 33. Function: ArithOp
  **Formula:** `$tin_rg61_rate1 * i_reg_61 + $tin_rg24_rate1 * i_reg_24 + $tin_rg12_rate1 * i_reg_12 + $tin_rg53_rate1 * i_reg_53 + $tin_rg70_rate1 * i_reg_70 + $tin_rg13_rate1 * i_reg_13 + $tin_rg42_rate1 * i_reg_42 + $tin_rg41_rate1 * i_reg_41 + $tin_rg51_rate1 * i_reg_51 + $tin_rg43_rate1 * i_reg_43 + $tin_rg11_rate1 * i_reg_11 + $tin_rg23_rate1 * i_reg_23 + $tin_rg30_rate1 * i_reg_30 + $tin_rg62_rate1 * i_reg_62 + $tin_rg22_rate1 * i_reg_22 + $tin_rg52_rate1 * i_reg_52 + $tin_rg21_rate1 * i_reg_21 + $tin_rg63_rate1 * i_reg_63 + $tin_rg64_rate1 * i_reg_64`
  **Output Variable:** `v_tin_ts_rt1_rg`
  **Tax Unit:** `tu_individual_es`

### 34. Function: ArithOp
  **Formula:** `$tin_rg61_rate2 * i_reg_61 + $tin_rg24_rate2 * i_reg_24 + $tin_rg12_rate2 * i_reg_12 + $tin_rg53_rate2 * i_reg_53 + $tin_rg70_rate2 * i_reg_70 + $tin_rg13_rate2 * i_reg_13 + $tin_rg42_rate2 * i_reg_42 + $tin_rg41_rate2 * i_reg_41 + $tin_rg51_rate2 * i_reg_51 + $tin_rg43_rate2 * i_reg_43 + $tin_rg11_rate2 * i_reg_11 + $tin_rg23_rate2 * i_reg_23 + $tin_rg30_rate2 * i_reg_30 + $tin_rg62_rate2 * i_reg_62 + $tin_rg22_rate2 * i_reg_22 + $tin_rg52_rate2 * i_reg_52 + $tin_rg21_rate2 * i_reg_21 + $tin_rg63_rate2 * i_reg_63 + $tin_rg64_rate2 * i_reg_64`
  **Output Variable:** `v_tin_ts_rt2_rg`
  **Tax Unit:** `tu_individual_es`

### 35. Function: ArithOp
  **Formula:** `$tin_rg61_rate3 * i_reg_61 + $tin_rg24_rate3 * i_reg_24 + $tin_rg12_rate3 * i_reg_12 + $tin_rg53_rate3 * i_reg_53 + $tin_rg70_rate3 * i_reg_70 + $tin_rg13_rate3 * i_reg_13 + $tin_rg42_rate3 * i_reg_42 + $tin_rg41_rate3 * i_reg_41 + $tin_rg51_rate3 * i_reg_51 + $tin_rg43_rate3 * i_reg_43 + $tin_rg11_rate3 * i_reg_11 + $tin_rg23_rate3 * i_reg_23 + $tin_rg30_rate3 * i_reg_30 + $tin_rg62_rate3 * i_reg_62 + $tin_rg22_rate3 * i_reg_22 + $tin_rg52_rate3 * i_reg_52 + $tin_rg21_rate3 * i_reg_21 + $tin_rg63_rate3 * i_reg_63 + $tin_rg64_rate3 * i_reg_64`
  **Output Variable:** `v_tin_ts_rt3_rg`
  **Tax Unit:** `tu_individual_es`

### 36. Function: ArithOp
  **Formula:** `$tin_rg61_rate4 * i_reg_61 + $tin_rg24_rate4 * i_reg_24 + $tin_rg12_rate4 * i_reg_12 + $tin_rg53_rate4 * i_reg_53 + $tin_rg70_rate4 * i_reg_70 + $tin_rg13_rate4 * i_reg_13 + $tin_rg42_rate4 * i_reg_42 + $tin_rg41_rate4 * i_reg_41 + $tin_rg51_rate4 * i_reg_51 + $tin_rg43_rate4 * i_reg_43 + $tin_rg11_rate4 * i_reg_11 + $tin_rg23_rate4 * i_reg_23 + $tin_rg30_rate4 * i_reg_30 + $tin_rg62_rate4 * i_reg_62 + $tin_rg22_rate4 * i_reg_22 + $tin_rg52_rate4 * i_reg_52 + $tin_rg21_rate4 * i_reg_21 + $tin_rg63_rate4 * i_reg_63 + $tin_rg64_rate4 * i_reg_64`
  **Output Variable:** `v_tin_ts_rt4_rg`
  **Tax Unit:** `tu_individual_es`

### 37. Function: ArithOp
  **Formula:** `$tin_rg61_rate5 * i_reg_61 + $tin_rg24_rate5 * i_reg_24 + $tin_rg12_rate5 * i_reg_12 + $tin_rg53_rate5 * i_reg_53 + $tin_rg70_rate5 * i_reg_70 + $tin_rg13_rate5 * i_reg_13 + $tin_rg42_rate5 * i_reg_42 + $tin_rg41_rate5 * i_reg_41 + $tin_rg51_rate5 * i_reg_51 + $tin_rg43_rate5 * i_reg_43 + $tin_rg11_rate5 * i_reg_11 + $tin_rg23_rate5 * i_reg_23 + $tin_rg30_rate5 * i_reg_30 + $tin_rg62_rate5 * i_reg_62 + $tin_rg22_rate5 * i_reg_22 + $tin_rg52_rate5 * i_reg_52 + $tin_rg21_rate5 * i_reg_21 + $tin_rg63_rate5 * i_reg_63 + $tin_rg64_rate5 * i_reg_64`
  **Output Variable:** `v_tin_ts_rt5_rg`
  **Tax Unit:** `tu_individual_es`

### 38. Function: ArithOp
  **Formula:** `$tin_rg61_rate6 * i_reg_61 + $tin_rg24_rate6 * i_reg_24 + $tin_rg12_rate6 * i_reg_12 + $tin_rg53_rate6 * i_reg_53 + $tin_rg70_rate6 * i_reg_70 + $tin_rg13_rate6 * i_reg_13 + $tin_rg42_rate6 * i_reg_42 + $tin_rg41_rate6 * i_reg_41 + $tin_rg51_rate6 * i_reg_51 + $tin_rg43_rate6 * i_reg_43 + $tin_rg11_rate6 * i_reg_11 + $tin_rg23_rate6 * i_reg_23 + $tin_rg30_rate6 * i_reg_30 + $tin_rg62_rate6 * i_reg_62 + $tin_rg22_rate6 * i_reg_22 + $tin_rg52_rate6 * i_reg_52 + $tin_rg21_rate6 * i_reg_21 + $tin_rg63_rate6 * i_reg_63 + $tin_rg64_rate6 * i_reg_64`
  **Output Variable:** `v_tin_ts_rt6_rg`
  **Tax Unit:** `tu_individual_es`

### 39. Function: ArithOp
  **Formula:** `$tin_rg61_rate7 * i_reg_61 + $tin_rg24_rate7 * i_reg_24 + $tin_rg12_rate7 * i_reg_12 + $tin_rg53_rate7 * i_reg_53 + $tin_rg70_rate7 * i_reg_70 + $tin_rg13_rate7 * i_reg_13 + $tin_rg42_rate7 * i_reg_42 + $tin_rg41_rate7 * i_reg_41 + $tin_rg51_rate7 * i_reg_51 + $tin_rg43_rate7 * i_reg_43 + $tin_rg11_rate7 * i_reg_11 + $tin_rg23_rate7 * i_reg_23 + $tin_rg30_rate7 * i_reg_30 + $tin_rg62_rate7 * i_reg_62 + $tin_rg22_rate7 * i_reg_22 + $tin_rg52_rate7 * i_reg_52 + $tin_rg21_rate7 * i_reg_21 + $tin_rg63_rate7 * i_reg_63 + $tin_rg64_rate7 * i_reg_64`
  **Output Variable:** `v_tin_ts_rt7_rg`
  **Tax Unit:** `tu_individual_es`

### 40. Function: ArithOp
  **Formula:** `$tin_rg61_rate8 * i_reg_61 + $tin_rg24_rate8 * i_reg_24 + $tin_rg12_rate8 * i_reg_12 + $tin_rg53_rate8 * i_reg_53 + $tin_rg70_rate8 * i_reg_70 + $tin_rg13_rate8 * i_reg_13 + $tin_rg42_rate8 * i_reg_42 + $tin_rg41_rate8 * i_reg_41 + $tin_rg51_rate8 * i_reg_51 + $tin_rg43_rate8 * i_reg_43 + $tin_rg11_rate8 * i_reg_11 + $tin_rg23_rate8 * i_reg_23 + $tin_rg30_rate8 * i_reg_30 + $tin_rg62_rate8 * i_reg_62 + $tin_rg22_rate8 * i_reg_22 + $tin_rg52_rate8 * i_reg_52 + $tin_rg21_rate8 * i_reg_21 + $tin_rg63_rate8 * i_reg_63 + $tin_rg64_rate8 * i_reg_64`
  **Output Variable:** `v_tin_ts_rt8_rg`
  **Tax Unit:** `tu_individual_es`

### 41. Function: ArithOp
  **Formula:** `$tin_rg61_rate9 * i_reg_61 + $tin_rg24_rate9 * i_reg_24 + $tin_rg12_rate9 * i_reg_12 + $tin_rg53_rate9 * i_reg_53 + $tin_rg70_rate9 * i_reg_70 + $tin_rg13_rate9 * i_reg_13 + $tin_rg42_rate9 * i_reg_42 + $tin_rg41_rate9 * i_reg_41 + $tin_rg51_rate9 * i_reg_51 + $tin_rg43_rate9 * i_reg_43 + $tin_rg11_rate9 * i_reg_11 + $tin_rg23_rate9 * i_reg_23 + $tin_rg30_rate9 * i_reg_30 + $tin_rg62_rate9 * i_reg_62 + $tin_rg22_rate9 * i_reg_22 + $tin_rg52_rate9 * i_reg_52 + $tin_rg21_rate9 * i_reg_21 + $tin_rg63_rate9 * i_reg_63 + $tin_rg64_rate9 * i_reg_64`
  **Output Variable:** `v_tin_ts_rt9_rg`
  **Tax Unit:** `tu_individual_es`

### 42. Function: ArithOp
  **Formula:** `$tin_rg61_rate10 * i_reg_61 + $tin_rg24_rate10 * i_reg_24 + $tin_rg12_rate10 * i_reg_12 + $tin_rg53_rate10 * i_reg_53 + $tin_rg70_rate10 * i_reg_70 + $tin_rg13_rate10 * i_reg_13 + $tin_rg42_rate10 * i_reg_42 + $tin_rg41_rate10 * i_reg_41 + $tin_rg51_rate10 * i_reg_51 + $tin_rg43_rate10 * i_reg_43 + $tin_rg11_rate10 * i_reg_11 + $tin_rg23_rate10 * i_reg_23 + $tin_rg30_rate10 * i_reg_30 + $tin_rg62_rate10 * i_reg_62 + $tin_rg22_rate10 * i_reg_22 + $tin_rg52_rate10 * i_reg_52 + $tin_rg21_rate10 * i_reg_21 + $tin_rg63_rate10 * i_reg_63 + $tin_rg64_rate10 * i_reg_64`
  **Output Variable:** `v_tin_ts_rt10_rg`
  **Tax Unit:** `tu_individual_es`

### 43. Function: DefConst
  **Constants Defined:**
  - `$tin_mortgtc_amt1`: 9040#y
  - `$tin_mortgtc_amt2`: 9040#y
  - `$tin_mortgtc_rate1`: 0.075
  - `$tin_mortgtc_rate2`: 0
  - `$tin_renttc_lim1`: 17707.20#y
  - `$tin_renttc_lim2`: 24107.20#y
  - `$tin_renttc_maxamt`: 9040#y
  - `$tin_renttc_rate1`: 0.105
  - `$tin_renttc_rate2`: 1.4125
  - `$tin_untc_amt`: 0
  - `$tin_untc_lim1`: 0
  - `$tin_untc_lim2`: 0
  - `$tin_untc_rate`: 0
  - `$tin_mortgtc_regrate1`: 0.075
  - `$tin_mortgtc_regrate2`: 0
  - `$tin_wkintc_amt`: 340#y
  - `$tin_wkintc_lim1`: 16576#y
  - `$tin_wkintc_lim2`: 18276#y
  - `$tin_wkintc_rate`: 0.2

### 44. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$tin_rate1`: n/a
  - `$tin_rate2`: n/a
  - `$tin_rate3`: n/a
  - `$tin_rate4`: n/a
  - `$tin_rate5`: n/a
  - `$tin_rate6`: n/a
  - `$tin_rate7`: n/a


---

## Policy: tinit_es
### 1. Function: DefTu
  - **Name**: `tu_tinfait`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild & DepParent`
  - **PartnerCond**: `Default`
  - **DepChildCond**: `Default & dag<25 & il_tinty#1<=$tin_depall_lim`
  - **DepParentCond**: `Default & dag>65 & il_tinty#1<=$tin_depall_lim`
  - **#_level**: `tu_individual_es`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`

### 2. Function: ArithOp
  **Formula:** `max(il_tinty,0)`
  **Output Variable:** `tinty_s`
  **Tax Unit:** `tu_individual_es`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `il_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 4. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dag > 75`
  - **comp_perElig**: `$tin_perall_amt1`
  - **comp_perTu**: `$tin_perall_amt3`
  - **output_var**: `sin04_s`
  - **TAX_UNIT**: `tu_individual_es`

### 5. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu#1 > 0`
  - **comp_perTu**: `$tin_childall_amt5 * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `2`
  - **output_var**: `sin05_s`
  - **TAX_UNIT**: `tu_tinfait`

### 6. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsDepParent & dag > 75`
  - **comp_perElig**: `$tin_depall_amt2`
  - **output_var**: `sin06_s`
  - **TAX_UNIT**: `tu_tinfait`

### 7. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsParentOfDepChild`
  - **Tax Unit:** `tu_tinfait`

### 8. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `sin05_s`
  - **share_between**: `IsParentOfDepChild`
  - **share_equ_ifzero**: `no`
  - **share_all_ifnoelig**: `no`
  - **output_var**: `sin05_s`
  - **TAX_UNIT**: `tu_tinfait`

### 9. Function: DefIl
  - **name**: `il_tintcit`
  - **sin04_s**: `+`
  - **sin05_s**: `+`
  - **sin06_s**: `+`

### 10. Function: BenCalc
  - **comp_cond**: `i_tinwk01 > $tin_empall_lim2 & i_tinwk01 <= $tin_empall_lim4 & il_tinot <= $tin_empall_lim3`
  - **comp_perTu**: `$tin_empall_maxamt2 - $tin_empall_rate * (i_tinwk01 - $tin_empall_lim2)`
  - **output_var**: `sin07_s`
  - **TAX_UNIT**: `tu_individual_es`
  - **UpLim**: `i_tinwk01`

### 11. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTu**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **UpLim**: `n/a`

### 12. Function: DefIl
  - **name**: `il_tintbit`
  - **sin04_s**: `n/a`
  - **sin05_s**: `n/a`
  - **sin06_s**: `n/a`
  - **tintaxp_s**: `-`
  - **i_tintibg**: `+`

### 13. Function: ArithOp
  **Formula:** `max(il_tintbit,0)`
  **Output Variable:** `tintbit_s`
  **Tax Unit:** `tu_individual_es`

### 14. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_es`
  - **Output Variable:** `i_tiningt`

### 15. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_es`
  - **Output Variable:** `i_tiningc`

### 16. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_es`
  - **Output Variable:** ``

### 17. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_es`
  - **Output Variable:** ``

### 18. Function: DefIl
  - **name**: `il_tintcmo`
  - **xhcmomi**: `+`
  - **xhcmomc**: `+`

### 19. Function: Allocate
  - **share**: `il_tintcmo`
  - **share_between**: `IsHead | IsPartner`
  - **share_equ_ifzero**: `no`
  - **share_all_ifnoelig**: `no`
  - **output_var**: `xhcmo`
  - **TAX_UNIT**: `tu_tinfait`

### 20. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 != 51`
  - **Tax Unit:** `tu_individual_es`

### 21. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `i_tingtint> 0`
  - **comp_perTu**: `min(xhcmo,$tin_mortgtc_amt1)*$tin_mortgtc_rate1`
  - **output_var**: `i_tintincmt`
  - **TAX_UNIT**: `tu_individual_es`

### 22. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTu**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 23. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTu**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 24. Function: ArithOp *(Switch: off)*
  **Formula:** `sin35_s + sin09_s + sin29_s `
  **Output Variable:** `tintcit_s`
  **Tax Unit:** `tu_individual_es`

### 25. Function: ArithOp *(Switch: off)*
  **Formula:** `tingtit_s - tintcit_s`
  **Output Variable:** `tinit_s`
  **Tax Unit:** `tu_individual_es`

### 26. Function: BenCalc
  - **comp_cond**: `dag >=50`
  - **comp_perElig**: `min($tin_pen_amt1,0.3*(yse+i_tinwk))`
  - **comp_perTu**: `min($tin_pen_amt1,0.3*(yse+i_tinwk))`
  - **output_var**: `i_tintaxp`
  - **TAX_UNIT**: `tu_individual_es`
  - **UpLim**: `n/a`

### 27. Function: ArithOp
  **Formula:** `xpp`
  **Output Variable:** `tintaxp_s`
  **Tax Unit:** `tu_individual_es`

### 28. Function: DefVar
  - **i_tintaxp**: `0`

### 29. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_reg_53=1  & nDepChInTu > 3`
  - **comp_perTu**: `$tin_childallrg53_amt2*max(nDepChInTu-3,0)`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `2`
  - **output_var**: `sin45_s`
  - **TAX_UNIT**: `tu_tinfait`
  - **Comp_perTU**: `$tin_childallrg70_amt5 * nDepChInTu#1`
  - **Comp_Cond**: `i_reg_70=1  & nDepChInTu#1 > 0`

### 30. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_reg_13=1 & IsDepParent & dag>75`
  - **Comp_perTU**: `$tin_depallrg70_amt2`
  - **output_var**: `sin46_s`
  - **TAX_UNIT**: `tu_tinfait`
  - **Comp_Cond**: `i_reg_70=1 & IsDepParent & dag>75`

### 31. Function: BenCalc
  - **Comp_Cond**: `tintbit_s-il_tintcit < 0`
  - **Comp_perTU**: `il_tintcit-tintbit_s`
  - **Output_Var**: `i_tinexticn`
  - **TAX_UNIT**: `tu_individual_es`

### 32. Function: BenCalc
  - **Comp_Cond**: `tintbit_s-il_tintcitrg< 0`
  - **Comp_perTU**: `il_tintcitrg-tintbit_s`
  - **Output_Var**: `i_tinexticr`
  - **TAX_UNIT**: `tu_individual_es`

### 33. Function: Elig
  **Eligibility Check:**
  - **Condition:** `tintbit_s-il_tintcit> 0`
  - **Tax Unit:** `tu_individual_es`

### 34. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_tintikb-i_tinexticn> 0`
  - **Tax Unit:** `tu_individual_es`

### 35. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_es`
  - **Output Variable:** `i_tininkt`
    - Band: Rate=`$tin_capinc_natrate4`, Limit=``

### 36. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_es`
  - **Output Variable:** `i_tininkc`
    - Band: Rate=`$tin_capinc_natrate4`, Limit=``

### 37. Function: Elig
  **Eligibility Check:**
  - **Condition:** `tintbit_s-il_tintcitrg> 0`
  - **Tax Unit:** `tu_individual_es`

### 38. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_tintikb-i_tinexticr> 0`
  - **Tax Unit:** `tu_individual_es`

### 39. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_es`
  - **Output Variable:** `i_tinirkt`
    - Band: Rate=`$tin_capinc_natrate4`, Limit=``

### 40. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_es`
  - **Output Variable:** `i_tinirkc`
    - Band: Rate=`$tin_capinc_natrate4`, Limit=``

### 41. Function: ArithOp
  **Formula:** `i_tiningt-i_tiningc+ i_tininkt-i_tininkc`
  **Output Variable:** `i_tingtint`
  **Tax Unit:** `tu_individual_es`

### 42. Function: ArithOp
  **Formula:** `i_tinirgt-i_tinirgc+ i_tinirkt- i_tinirkc`
  **Output Variable:** `i_tingtirg`
  **Tax Unit:** `tu_individual_es`

### 43. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `i_tingtirg> 0`
  - **comp_perTu**: `min(xhcmo,$tin_mortgtc_amt1)*$tin_mortgtc_regrate1`
  - **output_var**: `i_tintircmt`
  - **TAX_UNIT**: `tu_individual_es`

### 44. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTu**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 45. Function: ArithOp
  **Formula:** `i_tingtint -  i_tintincmt -  i_tintincrt - i_tiniwkintc`
  **Output Variable:** `i_tintint`
  **Tax Unit:** `tu_individual_es`

### 46. Function: DefIl
  - **Name**: `il_tintbiit`
  - **il_tinty**: `+`
  - **sin07_s**: `-`

### 47. Function: ArithOp
  **Formula:** `max(il_tintbiit,0)`
  **Output Variable:** `i_tintibg`
  **Tax Unit:** `tu_individual_es`

### 48. Function: Elig
  **Eligibility Check:**
  - **Condition:** `il_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 49. Function: DefVar
  - **i_tinexticn**: `0`
  - **i_tinexticr**: `0`
  - **i_tininkt**: `0`
  - **i_tininkc**: `0`
  - **i_tinirkt**: `0`
  - **i_tinirkc**: `0`
  - **i_tingtint**: `0`
  - **i_tintircmt**: `0`
  - **i_tingtirg**: `0`
  - **i_tintircrt**: `0`
  - **i_tintint**: `0`
  - **i_tintirg**: `0`
  - **i_tintibg**: `0`
  - **i_tintikb**: `0`
  - **i_tintincrt**: `0`
  - **i_tinirgc**: `0`
  - **i_tiningc**: `0`
  - **i_tinirgt**: `0`
  - **i_tiningt**: `0`
  - **i_tintincmt**: `0`
  - **i_tinticee**: `n/a`
  - **i_tinwkex**: `0`
  - **i_tinwk**: `0`
  - **i_tinwk01**: `0`
  - **i_tiniwkintc**: `0`

### 50. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `sin45_s`
  - **share_between**: `IsParentOfDepChild`
  - **share_equ_ifzero**: `no`
  - **share_all_ifnoelig**: `no`
  - **output_var**: `sin45_s`
  - **TAX_UNIT**: `tu_tinfait`

### 51. Function: DefIl
  - **name**: `il_tinwkgr`
  - **yem**: `+`
  - **ils_pen**: `+`
  - **poacm_s**: `+`
  - **poanc_s**: `+`
  - **psuwdcm_s**: `+`
  - **bhl**: `+`
  - **bunct_s**: `+`
  - **bunnc_s**: `+`
  - **bma**: `n/a`
  - **bmact_s**: `n/a`
  - **bpact_s**: `n/a`
  - **bmanc_s**: `n/a`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **pec_s**: `n/a`

### 52. Function: BenCalc
  - **Comp_Cond**: `il_tinwkgr > 0`
  - **Comp_perTU**: `$tin_empded_amt`
  - **UpLim**: `il_tinwkgr`
  - **Output_Var**: `i_tinwkex`
  - **TAX_UNIT**: `tu_individual_es`

### 53. Function: DefIl
  - **name**: `il_tinwk`
  - **yem**: `+`
  - **ils_pen**: `+`
  - **poacm_s**: `+`
  - **poanc_s**: `+`
  - **psuwdcm_s**: `+`
  - **bhl**: `+`
  - **bunct_s**: `+`
  - **bunnc_s**: `+`
  - **bma**: `n/a`
  - **bmact_s**: `n/a`
  - **bpact_s**: `n/a`
  - **bmanc_s**: `n/a`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **ils_sicee**: `-`
  - **i_tinwkex**: `-`
  - **pec_s**: `n/a`

### 54. Function: DefIl
  - **name**: `il_tinot`
  - **ypr**: `+`
  - **yse**: `+`
  - **ypp**: `+`
  - **ils_sicse**: `-`
  - **yiy**: `n/a`

### 55. Function: DefIl
  - **name**: `il_tinty`
  - **il_tinwk**: `n/a`
  - **il_tinot**: `+`
  - **i_tinwk**: `+`

### 56. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `i_reg_70=1 & dag > 75`
  - **Comp_perTU**: `$tin_perallrg70_amt3`
  - **Output_Var**: `sin51_s`
  - **TAX_UNIT**: `tu_individual_es`

### 57. Function: DefIl
  - **Name**: `il_tintsit`
  - **yiy**: `+`

### 58. Function: ArithOp
  **Formula:** `max(il_tintsit,0)`
  **Output Variable:** `i_tintikb`
  **Tax Unit:** `tu_individual_es`

### 59. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `i_reg_51 = 1 & ((tintbit_s + i_tintikb) < $tin_perallrg51_lim)`
  - **Comp_perTU**: `$tin_perallrg51_amt - $tin_perall_amt1`
  - **Output_Add_Var**: `sin04_s`
  - **TAX_UNIT**: `tu_individual_es`

### 60. Function: DefIl
  - **name**: `il_tintcitrg`
  - **sin51_s**: `+`
  - **sin45_s**: `+`
  - **sin46_s**: `+`

### 61. Function: DefIl
  - **name**: `il_tinwk01`
  - **yem**: `+`
  - **ils_pen**: `+`
  - **poacm_s**: `+`
  - **poanc_s**: `+`
  - **psuwdcm_s**: `+`
  - **bhl**: `+`
  - **bunct_s**: `+`
  - **bunnc_s**: `+`
  - **bma**: `n/a`
  - **bmact_s**: `n/a`
  - **bpact_s**: `n/a`
  - **bmanc_s**: `n/a`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **pec_s**: `n/a`
  - **ils_sicee**: `-`

### 62. Function: ArithOp
  **Formula:** `il_tinwk`
  **Output Variable:** `i_tinwk`
  **Tax Unit:** `tu_individual_es`

### 63. Function: ArithOp
  **Formula:** `il_tinwk01`
  **Output Variable:** `i_tinwk01`
  **Tax Unit:** `tu_individual_es`

### 64. Function: BenCalc
  - **Comp_Cond**: `ils_earns >0 & il_tinwkgr > $tin_wkintc_lim1 & il_tinwkgr<= $tin_wkintc_lim2 & il_tinot <= $tin_empall_lim3`
  - **Comp_perTU**: `min(i_tiningt-i_tiningc+i_tinirgt-i_tinirgc, $tin_wkintc_amt-$tin_wkintc_rate*(il_tinwkgr - $tin_wkintc_lim1))`
  - **Output_Var**: `i_tiniwkintc`
  - **TAX_UNIT**: `tu_individual_es`


---

## Policy: tintcrgit_es
### 1. Function: DefTu
  - **Name**: `tu_tintcrg01`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild & DepParent`
  - **PartnerCond**: `Default`
  - **DepChildCond**: `Default & dag<25 & il_tinty#1<=8000#y & dec >= 2 & dec <= 4`
  - **DepParentCond**: `Default & dag>65 & il_tinty#1<=8000#y`
  - **#_level**: `tu_individual_es`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`

### 2. Function: DefVar
  - **i_tbbefpfa_i**: `0`
  - **i_tbaftpfa_i**: `0`
  - **i_gtbaftpfa_i**: `0`
  - **i_tinty**: `0`
  - **i_bchbamt_i**: `0`
  - **i_nospinwrk**: `0`
  - **i_nodepprt**: `0`
  - **i_tcrg_i**: `0`
  - **i_tcrgba_i**: `0`
  - **i_tcrgdb_i**: `0`
  - **i_tcrglp_i**: `0`
  - **i_tcrgdp_i**: `0`
  - **i_tcrgoa_i**: `0`
  - **i_tcrgfa_i**: `0`
  - **i_tcrglg_i**: `0`
  - **i_tcrgch_i**: `0`
  - **i_tcrgcc_i**: `0`
  - **i_tcrgrt_i**: `0`
  - **i_tcrgee_i**: `0`
  - **i_tcrghk_i**: `0`
  - **i_tcrgwm_i**: `0`
  - **i_tcrgmo_i**: `0`
  - **i_tcrgmocond51**: `0`
  - **i_tcrgun_i**: `0`
  - **i_tcrgse_i**: `0`
  - **i_tingtrg_i**: `0`
  - **i_tcrgli_i**: `0`
  - **i_temp**: `0`
  - **i_tcrgw_i**: `0`

### 3. Function: ArithOp
  **Formula:** `tintbit_s + yiy`
  **Output Variable:** `i_tbbefpfa_i`
  **Tax Unit:** `tu_individual_es`

### 4. Function: ArithOp
  **Formula:** `tintbit_s +yiy - sin04_s - sin05_s - sin06_s`
  **Output Variable:** `i_tbaftpfa_i`
  **Tax Unit:** `tu_individual_es`

### 5. Function: ArithOp
  **Formula:** `tintbit_s - sin04_s - sin05_s - sin06_s`
  **Output Variable:** `i_gtbaftpfa_i`
  **Tax Unit:** `tu_individual_es`

### 6. Function: ArithOp
  **Formula:** `il_tinty`
  **Output Variable:** `i_tinty`
  **Tax Unit:** `tu_individual_es`

### 7. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 61 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 8. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nPersInUnit > 5`
  - **comp_perTU**: `(8 + (nPersInUnit - 5) ) * $SMI`
  - **output_var**: `sin31_s`
  - **TAX_UNIT**: `tu_bch00`

### 9. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `il_bch00 < sin31_s & IsParentOfDepChild & nDepChInTu#2 >= 2`
  - **comp_perTU**: `12000 + (1200 * (nDepChInTu#2 - 2) )`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `i_bchbamt_i`
  - **TAX_UNIT**: `tu_bch00`

### 10. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`

### 11. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `i_tinty#1 > 0`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgba_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_couple_es`

### 12. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsLoneParentOfDepChild & i_tbbefpfa_i <= 80000#y`
  - **comp_perTU**: `100#y`
  - **output_add_var**: `i_tcrglp_i`
  - **TAX_UNIT**: `tu_tinfait`

### 13. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsDepParent & dag > 75 & i_tbbefpfa_i <= 80000#y`
  - **comp_perTU**: `100#y`
  - **output_add_var**: `i_tcrgdp_i`
  - **TAX_UNIT**: `tu_tinfait`

### 14. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1  = 0& ddi#1 > 0 & i_tbbefpfa_i#1 <= 80000#y`
  - **comp_perElig**: `100#y`
  - **output_var**: `i_temp`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfait`

### 15. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `i_tinty#1 > 0`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgdb_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_couple_es`

### 16. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & ddi > 0 & i_tbbefpfa_i <= 19000#y`
  - **comp_perTU**: `100#y`
  - **output_add_var**: `i_tcrgdb_i`
  - **TAX_UNIT**: `tu_individual_es`

### 17. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1  > 0 & dag#1 < 35 & i_tbbefpfa_i#1 <=$tintc_rg61_rent_lim_it`
  - **comp_perTU**: `min(0.15*xhcrt,$tintc_rg61_rent_amt)`
  - **output_var**: `i_temp`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfait`

### 18. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `i_tinty#1 > 0 & dag#1 < 35 & i_tbbefpfa_i#1 <= $tintc_rg61_rent_lim_it`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgrt_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_couple_es`

### 19. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 24 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 20. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu >= 3 & i_tbaftpfa_i <= 21000#y`
  - **comp_perTU**: `100#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`

### 21. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `i_tinty#1 > 0`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgba_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_couple_es`

### 22. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsDepParent & dag#1 > 75 & i_tinty > 0 & i_tbaftpfa_i < 21000#y`
  - **comp_perElig**: `150#y`
  - **output_var**: `i_temp`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfait`

### 23. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `i_tinty#1 > 0`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgdb_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_couple_es`

### 24. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 12 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 25. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `i_temp`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfait`

### 26. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `i_tinty#1 > 0`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgrt_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_couple_es`

### 27. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tbbefpfa_i#1<35000#y & dlg_s=1 &nDepChInTu>=5`
  - **comp_perTU**: `2000#y`
  - **output_add_var**: `i_temp`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfait`

### 28. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `i_tinty#1 > 0`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrglg_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_couple_es`

### 29. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsLoneParentOfDepChild & i_tbbefpfa_i<45000#y`
  - **comp_perTU**: `500#y`
  - **output_add_var**: `i_tcrglp_i`
  - **TAX_UNIT**: `tu_tinfait`

### 30. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Who_Must_Be_Elig**: `n/a`

### 31. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 53 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 32. Function: BenCalc *(Switch: off)*
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & dag > 65 & i_tbaftpfa_i <= 12500#y`
  - **comp_perElig**: `50#y`
  - **output_add_var**: `i_tcrgoa_i`
  - **TAX_UNIT**: `tu_individual_es`

### 33. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `ddi > 0 & i_tinty > 0 & i_tbaftpfa_i <= 33000#y`
  - **comp_perElig**: `88#y`
  - **output_add_var**: `i_tcrgdb_i`
  - **TAX_UNIT**: `tu_individual_es`

### 34. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **output_var**: `i_temp`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tintcrg01`

### 35. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `i_tinty#1 > 0`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgch_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_couple_es`

### 36. Function: BenCalc *(Switch: off)*
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & dag < 36 & ( (i_tbaftpfa_i <= 18000#y) | ( i_tbaftpfa_i <= 24000#y  & dlg_s = 1) )`
  - **comp_perTU**: `min(0.065*xhcrt,200#y)`
  - **output_add_var**: `i_tcrgrt_i`
  - **TAX_UNIT**: `tu_individual_es`

### 37. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 70 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 38. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu >= 5 & i_tbbefpfa_i<= 42900#y`
  - **comp_perTU**: `840#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`

### 39. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `i_tinty#1 > 0`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgba_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_couple_es`

### 40. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#2 > 0 & tintbit_s#2 <= 42900#y`
  - **comp_perTU**: `min(400#y*nDepChInTu#1,xcc*0.15)`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `2`
  - **#_level**: `tu_individual_es`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`

### 41. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `i_tinty#1 > 0`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgcc_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_couple_es`

### 42. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & dag > 65 & i_tbaftpfa_i <= 39000#y  `
  - **comp_perElig**: `120#y`
  - **output_add_var**: `i_tcrgdb_i`
  - **TAX_UNIT**: `tu_individual_es`

### 43. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dlg_s = 1 & nDepChInTu >= 5`
  - **comp_perTU**: `600#y`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`

### 44. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `i_tinty#1 > 0`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrglg_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_couple_es`

### 45. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & tintbit_s <=$tintc_rg70_rent_lim_it`
  - **comp_perTU**: `min(0.20*xhcrt,$tintc_rg70_rent_minamt)`
  - **output_add_var**: `i_tcrgrt_i`
  - **TAX_UNIT**: `tu_individual_es`

### 46. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(bunct_s>0 |bunnc_s>0) & lunmy_s>=6 & 11200#y<i_tinwk & i_tinwk<22000#y & il_tinot<1600#y`
  - **comp_perTU**: `100#y`
  - **output_add_var**: `i_tcrgun_i`
  - **TAX_UNIT**: `tu_individual_es`

### 47. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 13 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 48. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `ddi#2 > 0 & i_tinty#2 <= 6000#y`
  - **comp_perTU**: `100#y * nDepChInTu#1`
  - **comp_perElig**: `100#y`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `2`
  - **output_var**: `i_temp`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfait`

### 49. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `i_tinty#1 > 0`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgfa_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_couple_es`

### 50. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & i_tbbefpfa_i <= 22000#y & (dag < 35 | dag > 65 | ddi > 0)`
  - **comp_perTU**: `min(0.10*xhcrt,300#y)`
  - **output_add_var**: `i_tcrgrt_i`
  - **TAX_UNIT**: `tu_individual_es`

### 51. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 42 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 52. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsParentOfDepChild & i_tbbefpfa_i#2 <27000#y`
  - **comp_perTU**: `100#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **#_level**: `tu_individual_es`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`

### 53. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `IsParentOfDepChild & i_tbbefpfa_i#1 < 36000#y`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgba_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfait`

### 54. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsDepParent & dag#1 > 75 & i_tbbefpfa_i < 27000#y`
  - **comp_perElig**: `150#y`
  - **#_level**: `tu_individual_es`
  - **output_add_var**: `i_tcrgfa_i`
  - **TAX_UNIT**: `tu_tinfait`

### 55. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & dag > 75 & i_tbbefpfa_i < 27000#y`
  - **comp_perElig**: `150#y`
  - **output_add_var**: `i_tcrgoa_i`
  - **TAX_UNIT**: `tu_individual_es`

### 56. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 41 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 57. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu > 2  & i_tbaftpfa_i <= 18900#y`
  - **comp_perTU**: `2351#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`
  - **Comp_perTU**: `n/a`
  - **Comp_Cond**: `n/a`

### 58. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `IsParentOfDepChild`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgba_i`
  - **TAX_UNIT**: `tu_tinfait`

### 59. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu > 3 & i_tbaftpfa_i <= 18900#y`
  - **comp_perTU**: `450#y * (nDepChInTu - 3)`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`

### 60. Function: Allocate *(Switch: off)*
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `IsHead | IsPartner`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrglg_i`
  - **TAX_UNIT**: `tu_tinfait`

### 61. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(( IsParentOfDepChild & ils_earns#1 & GetPartnerIncome#2 > 0 ) | ( IsLoneParentOfDepChild & ils_earns#1 )) & i_tbaftpfa_i#1 <= 18900#y & nDepChInTu#3 > 0`
  - **comp_perTU**: `min(322#y,xcc*0.3)`
  - **#_level**: `tu_individual_es`
  - **#_income**: `ils_earns`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `3`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`

### 62. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `IsHead | IsPartner`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgcc_i`
  - **TAX_UNIT**: `tu_tinfait`

### 63. Function: BenCalc *(Switch: off)*
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & dag < 36 & drgur = 0 & i_tbaftpfa_i <= 18900#y`
  - **comp_perTU**: `min(0.20*xhcrt,612#y)`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_individual_es`

### 64. Function: Allocate *(Switch: off)*
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `dag < 36 & i_tbaftpfa_i <= 18900#y`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgrt_i`
  - **TAX_UNIT**: `tu_tinfait`

### 65. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 51 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 66. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsParentOfDepChild & nDepChInTu#1 >= 1`
  - **comp_perElig**: `150#y`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`

### 67. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `IsParentOfDepChild & nDepChInTu#1 >= 1`
  - **share_all_ifnoelig**: `yes`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `i_tcrgba_i`
  - **TAX_UNIT**: `tu_tinfait`

### 68. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 > 0 & i_tbbefpfa_i#1 <= $tintc_rg51_rent_lim_it & dlg_s = 1 & (dag#1 < 32 | lunmy#1 > 6 | ( dag#1 > 65 & dms#1 = 5) )`
  - **comp_perElig**: `min(0.10*xhcrt,$tintc_rg51_rent_minamt)`
  - **comp_perTU**: `min(0.10*xhcrt,$tintc_rg51_rent_minamt2)`
  - **uplim**: `min(0.10*xhcrt,$tintc_rg51_rent_minamt2)`
  - **output_var**: `i_temp`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfait`

### 69. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `i_tinty#1  > 0 & i_tbbefpfa_i#1 <= 20000#y & (dag#1 < 32 | lunmy#1 > 6 | ( dag#1 > 65 & dms#1 = 5) )`
  - **share_all_ifnoelig**: `yes`
  - **#_level**: `tu_individual_es`
  - **output_add_var**: `i_tcrgrt_i`
  - **TAX_UNIT**: `tu_tinfait`

### 70. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(dag <= 32 & i_tbaftpfa_i <= $tintc_rg51_mortg_lim_it) | lunmy >= 6 | ddi = 1 | nDepChildrenOfCouple >= 1`
  - **Tax Unit:** `tu_individual_es`

### 71. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tingtirg> 0 & i_tcrgmocond51 = 1`
  - **comp_perTu**: `min(il_tintcmo,$tin_mortgtc_amt2)*$tintcrgit_mortgtcrg51_totrate2`
  - **output_add_var**: `i_tcrgmo_i`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_Cond**: `(i_tcrgmocond51 != 1) & (i_tingtirg> 0)`
  - **Comp_perTU**: `min(il_tintcmo,$tin_mortgtc_amt2)*$tintcrgit_mortgtcrg51_totrate1`

### 72. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 43 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 73. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & i_tbbefpfa_i <= 45600#y & (dag < 36 | dlg_s = 1 | IsDisabled)`
  - **comp_perTU**: `min(0.3*xhcrt,750#y)`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_individual_es`

### 74. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `i_tinty#1  > 0 & i_tbbefpfa_i#1 <= 45600#y & (dag#1 < 36| dlg_s = 1)`
  - **share_all_ifnoelig**: `yes`
  - **#_level**: `tu_individual_es`
  - **output_add_var**: `i_tcrgrt_i`
  - **TAX_UNIT**: `tu_tinfait`

### 75. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & i_tinwk > 0 & i_tinwk <= 12000#y & il_tinot <= 300#y`
  - **comp_perTU**: `75#y`
  - **output_add_var**: `i_tcrgee_i`
  - **TAX_UNIT**: `tu_individual_es`

### 76. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 11 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 77. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu#2 > 0 & i_tbaftpfa_i > 22000#y & i_tbaftpfa_i <= 31000#y`
  - **comp_perTU**: `300#y * nDepChInTu#2`
  - **#_AgeMin**: `1`
  - **#_AgeMax**: `2`
  - **output_add_var**: `i_tcrgba_i`
  - **TAX_UNIT**: `tu_individual_es`

### 78. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `idpartner = 0`
  - **comp_perTU**: `0`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_individual_es`

### 79. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `IsParentOfDepChild & nDepChInTu#1 >= 1`
  - **share_all_ifnoelig**: `yes`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `2`
  - **output_add_var**: `i_tcrgba_i`
  - **TAX_UNIT**: `tu_tinfait`

### 80. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu > 4`
  - **comp_perTU**: `150#y`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`

### 81. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `(IsHead | IsPartner) & i_tinty#1 > 0`
  - **share_all_ifnoelig**: `yes`
  - **#_level**: `tu_individual_es`
  - **output_add_var**: `i_tcrglg_i`
  - **TAX_UNIT**: `tu_tinfait`

### 82. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(( IsParentOfDepChild & ils_earns#1 & GetPartnerIncome#2 > 0 ) | ( IsLoneParentOfDepChild & ils_earns#1 )) & i_tbaftpfa_i#1 <= 22000#y & nDepChInTu#3 > 0`
  - **comp_perTU**: `min(400#y,xcc*0.3)`
  - **#_level**: `tu_individual_es`
  - **#_income**: `ils_earns`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `3`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`

### 83. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `(IsHead | IsPartner) & i_tinty#1 > 0 & i_tbaftpfa_i#1 <= 22000#y`
  - **share_all_ifnoelig**: `yes`
  - **#_level**: `tu_individual_es`
  - **output_add_var**: `i_tcrgcc_i`
  - **TAX_UNIT**: `tu_tinfait`

### 84. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & dag < 36 & i_tbbefpfa_i <= 22000#y & NChildrenofCouple < 2`
  - **comp_perTU**: `min(0.10*xhcrt,300#y)`
  - **output_add_var**: `i_tcrgrt_i`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_perTU**: `min(0.10*xhcrt,600#y)`
  - **Comp_Cond**: `i_tinty > 0 & dag < 36 & i_tbbefpfa_i <= 22000#y & NChildrenofCouple >= 2`

### 85. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 30 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 86. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsParentOfDepChild & nDepChInTu#1 > 1 & i_tbbefpfa_i#2 <= 30930#y`
  - **comp_perTU**: `721.70#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **#_level**: `tu_individual_es`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`

### 87. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `IsParentOfDepChild & i_tinty#1 > 0 & i_tbbefpfa_i#1 <= 25620#y`
  - **share_all_ifnoelig**: `yes`
  - **#_level**: `tu_individual_es`
  - **output_add_var**: `i_tcrgba_i`
  - **TAX_UNIT**: `tu_tinfait`

### 88. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & dag < 35 & i_tbbefpfa_i <= $tintc_rg30_rent_lim_it`
  - **comp_perTU**: `min(0.30*xhcrt,$tintc_rg30_rent_amt)`
  - **output_add_var**: `i_tcrgrt_i`
  - **TAX_UNIT**: `tu_individual_es`

### 89. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_es`
  - **Output Variable:** ``

### 90. Function: BenCalc
  - **comp_cond**: `i_tinty > 0 & i_tbbefpfa_i <= 24000#y & IsParentOfDepChild & nDepChInTu>=2`
  - **comp_perTU**: `0.10 * (i_tingtirg - i_tintircmt - i_tintircrt-i_tcrgba_i-i_tcrgrt_i)`
  - **lowlim**: `0`
  - **output_add_var**: `i_tcrgli_i`
  - **TAX_UNIT**: `tu_tinfait`
  - **Who_Must_Be_Elig**: `one`

### 91. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 62 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 92. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(IsParentOfDepChild & ils_earns#1)  &  i_tbbefpfa_i <= 30000#y & nDepChInTu#3 > 0`
  - **comp_perTU**: `min(1000#y*nDepChInTu#3,xcc*0.20)`
  - **#_level**: `tu_individual_es`
  - **#_income**: `n/a`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `2`
  - **output_add_var**: `i_tcrgcc_i`
  - **TAX_UNIT**: `tu_tinfait`

### 93. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 23 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 94. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu#1 =3`
  - **comp_perTU**: `900#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`

### 95. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `IsParentOfDepChild & i_tinty#1 > 0`
  - **share_all_ifnoelig**: `yes`
  - **#_level**: `tu_individual_es`
  - **output_add_var**: `i_tcrgba_i`
  - **TAX_UNIT**: `tu_tinfait`

### 96. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 22 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 97. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 52 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 98. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#2 > 0 & IsParentOfDepChild & nDepChInTu > 0 & i_tbbefpfa_i <= 23000#y`
  - **comp_perTU**: `270#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`
  - **Comp_perTU**: `270#y  * (1-((i_tbbefpfa_i-23000)/2000)) * nDepChInTu#1`
  - **Comp_Cond**: `i_tinty#2 > 0 & IsParentOfDepChild & nDepChInTu > 0 & (i_tbbefpfa_i > 23000#y  & i_tbbefpfa_i#2 < 25000#y)`
  - **#_Level**: `tu_individual_es`

### 99. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `IsParentOfDepChild & i_tinty#1 > 0 & i_tbbefpfa_i#1 <= 23000#y`
  - **share_all_ifnoelig**: `yes`
  - **#_level**: `tu_individual_es`
  - **output_add_var**: `i_tcrgba_i`
  - **TAX_UNIT**: `tu_tinfait`

### 100. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu#1 > 1 & i_tbbefpfa_i <= 23000#y`
  - **comp_perTU**: `224#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `i_tcrgba_i`
  - **TAX_UNIT**: `tu_tinfait`
  - **Comp_perTU**: `224#y  * (1-((i_tbbefpfa_i-23000)/2000)) * nDepChInTu#1`
  - **Comp_Cond**: `nDepChInTu#1 > 1 & ( i_tbbefpfa_i > 23000#y & i_tbbefpfa_i <= 25000#y)`

### 101. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dlg_s = 1 & nDepChInTu >= 5 & i_tbbefpfa_i <= 26000#y`
  - **comp_perTU**: `600#y`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`
  - **Comp_perTU**: `600#y  * (1-((i_tbbefpfa_i-26000)/4000))`
  - **Comp_Cond**: `dlg_s = 1 & nDepChInTu >= 5 & ( i_tbbefpfa_i > 26000#y & i_tbbefpfa_i <= 30000#y)`

### 102. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `IsParentOfDepChild & i_tinty#1 > 0`
  - **share_all_ifnoelig**: `yes`
  - **#_level**: `tu_individual_es`
  - **output_add_var**: `i_tcrglg_i`
  - **TAX_UNIT**: `tu_tinfait`

### 103. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & ddi > 0 & dag > 65 & i_tbbefpfa_i <= 23000#y`
  - **comp_perTU**: `179#y`
  - **output_add_var**: `i_tcrgdb_i`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_perTU**: `179#y  * (1-((i_tbbefpfa_i-23000)/2000))`
  - **Comp_Cond**: `i_tinty > 0 & ddi > 0 & dag > 65 &  ( i_tbbefpfa_i > 23000#y & i_tbbefpfa_i <= 25000#y)`

### 104. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dms#1 = 2 & idpartner#1 > 0 & (i_tinwk#1 > 0 | yse#1 > 0)`
  - **comp_perElig**: `1`
  - **output_var**: `i_nospinwrk`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfait`

### 105. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dms#1 = 2 & idpartner#1 > 0 & i_tinwk#1 = 0 & yse#1 = 0 & nDepChOfCouple > 1 & i_nospinwrk = 1 & i_tbbefpfa_i <= 23000#y`
  - **comp_perTU**: `153#y`
  - **output_add_var**: `i_tcrghk_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfait`
  - **Comp_perTU**: `153#y  * (1-((i_tbbefpfa_i-23000)/2000))`
  - **Comp_Cond**: `dms#1 = 2 & idpartner#1 > 0 & i_tinwk#1 = 0 & yse#1 = 0 & nDepChOfCouple > 1 & i_nospinwrk = 1 & ( i_tbbefpfa_i > 23000#y & i_tbbefpfa_i <= 25000#y)`

### 106. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsParentOfDepChild & ils_earns#1 > 0 & (GetPartnerIncome#2 > 0 | IsLoneParentOfDepChild) & i_tbbefpfa_i#1 <= 24000#y`
  - **comp_perTU**: `270#y * nDepChInTu#3`
  - **#_level**: `tu_individual_es`
  - **#_income**: `ils_earns`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `2`
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`
  - **Comp_perTU**: `270#y  * (1-((i_tbbefpfa_i-23000)/2000))* nDepChInTu#3`
  - **Comp_Cond**: `IsParentOfDepChild & ils_earns#1 > 0 & (GetPartnerIncome#2 > 0 | IsLoneParentOfDepChild) & ( i_tbbefpfa_i > 23000#y & i_tbbefpfa_i <= 25000#y)`

### 107. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `IsParentOfDepChild & ils_earns#1 > 0 & (GetPartnerIncome#2 > 0 | IsLoneParentOfDepChild) & i_tbbefpfa_i#1 <= 27245#y`
  - **share_all_ifnoelig**: `yes`
  - **#_level**: `tu_individual_es`
  - **#_income**: `ils_earns`
  - **output_add_var**: `i_tcrgcc_i`
  - **TAX_UNIT**: `tu_tinfait`

### 108. Function: DefTu
  - **Name**: `tu_tintcrg03`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild & DepParent`
  - **DepParentCond**: `Default & dag>75 & i_tinty#1<=8000#y`
  - **#_level**: `tu_individual_es`
  - **DepChildCond**: `Default`

### 109. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsDepParent`
  - **comp_perElig**: `1`
  - **output_var**: `i_nodepprt`
  - **TAX_UNIT**: `tu_tintcrg03`

### 110. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & i_tbbefpfa_i <= 23000#y`
  - **comp_perTU**: `179#y * i_nodepprt`
  - **output_add_var**: `i_tcrgdp_i`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_perTU**: `179#y  * (1-((i_tbbefpfa_i-23000)/2000)) * i_nodepprt`
  - **Comp_Cond**: `i_tinty > 0 & ( i_tbbefpfa_i > 23000#y & i_tbbefpfa_i <= 25000#y)`

### 111. Function: DefTu
  - **Name**: `tu_tintcrg02`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **PartnerCond**: `Default`
  - **DepChildCond**: `Default & dag = 4`

### 112. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChOfCouple#1 > 0 & (dgn=0 | (dgn=1 & idpartner=0))& il_sic > 0 & i_tbbefpfa_i <= 23000#y`
  - **comp_perTU**: `min(418#y,il_sic)*nDepChOfCouple#1`
  - **#_level**: `tu_tintcrg02`
  - **output_add_var**: `i_tcrgwm_i`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_perTU**: `min(418#y,il_sic)*(1-((i_tbbefpfa_i-23000)/2000))*nDepChOfCouple#1`
  - **Comp_Cond**: `nDepChOfCouple#1 > 0 & (dgn=0 | (dgn=1 & idpartner=0))& il_sic > 0 & (i_tbbefpfa_i > 23000#y & i_tbbefpfa_i <= 25000#y)`

### 113. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & i_tbbefpfa_i <= 23000#y & (dag < 35 | ddi > 0)`
  - **comp_perElig**: `min(0.20*xhcrt,612#y)`
  - **output_add_var**: `i_tcrgrt_i`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_perTU**: `min(0.20*xhcrt,612#y*(i_tbbefpfa_i-23000#y)/2000#y)`
  - **Comp_Cond**: `i_tinty > 0 & (i_tbbefpfa_i > 23000#y & i_tbbefpfa_i <= 25000#y)  & (dag < 35 | ddi > 0)`

### 114. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_es`
  - **Output Variable:** ``

### 115. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 21 & i_tinty > 0`
  - **Tax Unit:** `tu_individual_es`

### 116. Function: ArithOp
  **Formula:** `i_tcrgba_i + i_tcrgdb_i + i_tcrglp_i + i_tcrgdp_i + i_tcrgoa_i + i_tcrgfa_i + i_tcrglg_i + i_tcrgch_i + i_tcrgcc_i + i_tcrgrt_i + i_tcrgee_i + i_tcrghk_i + i_tcrgwm_i + i_tcrgmo_i + i_tcrgun_i + i_tcrgse_i + i_tcrgli_i`
  **Output Variable:** `i_tcrg_i`
  **Tax Unit:** `tu_individual_es`

### 117. Function: ArithOp
  **Formula:** `i_tingtirg - i_tintircmt - i_tintircrt - i_tcrg_i`
  **Output Variable:** `i_tintirg`
  **Tax Unit:** `tu_individual_es`

### 118. Function: BenCalc
  - **Comp_perTU**: `1000#y *nDepChInTu#1`
  - **Comp_Cond**: `nDepChInTu#1>1`
  - **Output_Add_Var**: `i_tcrgrt_i`
  - **TAX_UNIT**: `tu_tinfait`
  - **Who_Must_Be_Elig**: `one`
  - **#_AgeMax**: `0`
  - **#_AgeMin**: `0`

### 119. Function: BenCalc
  - **Comp_perTU**: `900#y*nDepChInTu#1`
  - **Comp_Cond**: `nDepChildrenInTu#1>2 `
  - **Output_Var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`
  - **Who_Must_Be_Elig**: `one`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **#_Level**: `n/a`

### 120. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu > =5 `
  - **comp_perTU**: `400#y `
  - **output_var**: `i_temp`
  - **TAX_UNIT**: `tu_tinfait`

### 121. Function: BenCalc
  - **comp_cond**: `i_tinty > 0 & i_tbbefpfa_i <= 24000#y & IsParentOfDepChild & nDepChInTu>=2`
  - **comp_perTU**: `0.10 * ( i_tingtrg_i-i_tinirgc- i_tinirkc- i_tcrgba_i-i_tcrgrt_i)`
  - **lowlim**: `0`
  - **output_add_var**: `i_tcrgli_i`
  - **TAX_UNIT**: `tu_tinfait`
  - **Who_Must_Be_Elig**: `one`

### 122. Function: Allocate
  - **who_must_be_elig**: `one`
  - **share**: `i_temp`
  - **share_between**: `IsParentOfDepChild & i_tbbefpfa_i#1 < 36000#y`
  - **share_all_ifnoelig**: `yes`
  - **output_add_var**: `i_tcrgba_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfait`

### 123. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dms=1 & i_tbbefpfa_i < 19000#y`
  - **comp_perTU**: `100#y`
  - **output_add_var**: `i_tcrgw_i`
  - **TAX_UNIT**: `tu_individual_es`

### 124. Function: BenCalc
  - **Comp_perTU**: `300#y *nDepChInTu#1`
  - **Comp_Cond**: `nDepChInTu#1>1 & i_tbbefpfa_i#1<19000#y`
  - **Output_Add_Var**: `i_tcrgrt_i`
  - **TAX_UNIT**: `tu_tinfait`
  - **Who_Must_Be_Elig**: `one`
  - **#_AgeMax**: `0`
  - **#_AgeMin**: `0`
  - **#_Level**: `tu_individual_es`

### 125. Function: ArithOp
  **Formula:** `i_tintirg+i_tintint`
  **Output Variable:** `tinit_s`
  **Tax Unit:** `tu_individual_es`

### 126. Function: DefConst
  **Constants Defined:**
  - `$tintcrgit_mortgtcrg51_totrate1`: 0.075 + 0.075
  - `$tintcrgit_mortgtcrg51_totrate2`: 0.075 + 0.09

### 127. Function: DefConst
  **Constants Defined:**
  - `$tintc_rg61_rent_amt`: 500#y
  - `$tintc_rg61_rent_lim_it`: 19000#y
  - `$tintc_rg61_rent_lim_jt`: 24000#y
  - `$tintc_rg12_rent_lim_amt`: 500#y
  - `$tintc_rg12_rent_lim_it`: 26000#y
  - `$tintc_rg12_rent_lim_jt`: 37000#y
  - `$tintc_rg53_books_amt`: 110#y
  - `$tintc_rg53_books_lim_it`: 33000#y
  - `$tintc_rg53_books_lim_jt`: 52000#y
  - `$tintc_rg70_disabold_amt1`: 120#y
  - `$tintc_rg70_disabold_amt2`: 39000#y
  - `$tintc_rg70_disabold_lim_it`: 52000#y
  - `$tintc_rg70_disabold_lim_jt`: 300#y
  - `$tintc_rg70_rent_minamt`: 600#y
  - `$tintc_rg70_rent_lim_it`: 20000#y
  - `$tintc_rg70_rent_lim_jt`: 30000#y
  - `$tintc_rg51_rent_minamt`: 300#y
  - `$tintc_rg51_rent_minamt2`: 600#y
  - `$tintc_rg51_rent_lim_it`: 20000#y
  - `$tintc_rg51_rent_lim_jt`: 30000#y
  - `$tintc_rg51_mortg_lim_it`: 30000#y
  - `$tintc_rg30_birth_amt`: 721.70#y
  - `$tintc_rg30_birth_lim_it`: 30930#y
  - `$tintc_rg30_birth_lim_jt`: 37322.20#y
  - `$tintc_rg30_rent_amt`: 1237.20#y
  - `$tintc_rg30_rent_lim_it`: 26414.22#y
  - `$tintc_rg30_rent_lim_jt`: 37322.20#y


---

## Policy: tinjt_es
### 1. Function: DefTu
  - **Name**: `tu_tinfajt`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild & DepParent`
  - **PartnerCond**: `Default & IsMarried`
  - **DepChildCond**: `Default & dag<25 & il_tinty#1<=$tin_depall_lim`
  - **DepParentCond**: `Default & dag>65 & il_tinty#1<=$tin_depall_lim`
  - **#_level**: `tu_individual_es`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`
  - **LoneParentCond**: `default & !IsMarried & nDepChOfCouple > 0`

### 2. Function: DefTu
  - **Name**: `tu_tinfajt02`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **PartnerCond**: `Default & IsMarried`
  - **DepChildCond**: `Default & dag<18 & il_tinty#1<=$tin_depall_lim`
  - **#_level**: `tu_individual_es`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`
  - **LoneParentCond**: `default & !IsMarried & nDepChOfCouple > 0`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `il_tinty > 0 & (IsMarried | IsParentOfDepChild)`
  - **Tax Unit:** `tu_tinfajt02`

### 4. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dag > 75`
  - **comp_perElig**: `$tin_perall_amt3`
  - **comp_perTu**: `n/a`
  - **output_var**: `sin11_s`
  - **TAX_UNIT**: `tu_tinfajt02`
  - **Comp_perTU**: `$tin_perall_amt1`

### 5. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsDepParent & dag > 75`
  - **comp_perElig**: `$tin_depall_amt2`
  - **output_var**: `sin13_s`
  - **TAX_UNIT**: `tu_tinfajt`

### 6. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `!IsMarried & !IsWithPartner & IsParentOfDepChild`
  - **comp_perTu**: `$tin_jointall_amt1`
  - **output_var**: `sin28_s`
  - **TAX_UNIT**: `tu_tinfajt02`

### 7. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `n/a`
  - **comp_perTu**: `n/a`
  - **output_var**: `sin14_s`
  - **TAX_UNIT**: `tu_tinfajt02`
  - **UpLim**: `i_tinwk01`

### 8. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTu**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **UpLim**: `n/a`

### 9. Function: DefIl
  - **name**: `il_tintbjt`
  - **i_tintjbg**: `+`
  - **sin11_s**: `n/a`
  - **sin12_s**: `n/a`
  - **sin13_s**: `n/a`
  - **sin28_s**: `-`
  - **i_tintajtxp_s**: `-`

### 10. Function: ArithOp
  **Formula:** `max(il_tintbjt,0)`
  **Output Variable:** `tintbjt_s`
  **Tax Unit:** `tu_tinfajt02`

### 11. Function: Elig
  **Eligibility Check:**
  - **Condition:** `sin17_s & tintbjt_s > il_tintcjt`
  - **Tax Unit:** `tu_tinfajt02`

### 12. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_tinfajt02`
  - **Output Variable:** `i_tinjngt`

### 13. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_tinfajt02`
  - **Output Variable:** `i_tinjngc`

### 14. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_tinfajt02`
  - **Output Variable:** ``

### 15. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_tinfajt02`
  - **Output Variable:** ``

### 16. Function: Elig
  **Eligibility Check:**
  - **Condition:** `il_tinty > 0 & (IsMarried | IsParentOfDepChild) & drgn2 != 51`
  - **Tax Unit:** `tu_tinfajt02`

### 17. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tingtjnt > 0`
  - **comp_perTu**: `min(il_tintcmo,$tin_mortgtc_amt1)*$tin_mortgtc_rate1`
  - **output_var**: `i_tintjncmt`
  - **TAX_UNIT**: `tu_tinfajt02`

### 18. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTu**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Who_Must_Be_Elig**: `n/a`

### 19. Function: ArithOp *(Switch: off)*
  **Formula:** `sin36_s + sin16_s + sin30_s `
  **Output Variable:** `tintcjt_s`
  **Tax Unit:** `tu_tinfajt02`

### 20. Function: ArithOp *(Switch: off)*
  **Formula:** `tingtjt_s - tintcjt_s`
  **Output Variable:** `tinjt_s`
  **Tax Unit:** `tu_tinfajt02`

### 21. Function: BenCalc
  - **comp_cond**: `dag >=50`
  - **comp_perElig**: `min($tin_pen_amt1,0.3*(yse+i_tinwk))`
  - **comp_perTu**: `min($tin_pen_amt1,0.3*(yse+i_tinwk))`
  - **output_var**: `i_tintajtxplt`
  - **TAX_UNIT**: `tu_individual_es`
  - **UpLim**: `n/a`

### 22. Function: ArithOp
  **Formula:** `xpp`
  **Output Variable:** `i_tintajtxpi`
  **Tax Unit:** `tu_individual_es`

### 23. Function: ArithOp
  **Formula:** `i_tintajtxpi`
  **Output Variable:** `i_tintajtxp_s`
  **Tax Unit:** `tu_tinfajt02`

### 24. Function: DefVar
  - **i_tintajtxplt**: `0`
  - **i_tintajtxpi**: `0`
  - **i_tintajtxp_s**: `0`

### 25. Function: DefIl
  - **name**: `il_tintcjt`
  - **sin11_s**: `+`
  - **sin12_s**: `+`
  - **sin13_s**: `+`

### 26. Function: BenCalc
  - **Comp_Cond**: `i_tintjbg-sin28_s<0`
  - **Comp_perTU**: `sin28_s-i_tintjbg`
  - **Output_Var**: `i_tinextjta
`
  - **TAX_UNIT**: `tu_tinfajt02`
  - **Who_Must_Be_Elig**: `one`

### 27. Function: DefIl
  - **Name**: `il_tintsjt`
  - **i_tinextjta**: `-`
  - **yiy**: `+`

### 28. Function: ArithOp
  **Formula:** `max(il_tintsjt,0)`
  **Output Variable:** `i_tintjkb`
  **Tax Unit:** `tu_tinfajt02`

### 29. Function: BenCalc
  - **Comp_Cond**: `tintbjt_s-il_tintcjtrg< 0`
  - **Comp_perTU**: `il_tintcjtrg-tintbjt_s`
  - **Output_Var**: `i_tinextjcr`
  - **TAX_UNIT**: `tu_tinfajt02`
  - **Who_Must_Be_Elig**: `one`

### 30. Function: BenCalc
  - **Comp_Cond**: `tintbjt_s-il_tintcjt < 0`
  - **Comp_perTU**: `il_tintcjt-tintbjt_s`
  - **Output_Var**: `i_tinextjcn`
  - **TAX_UNIT**: `tu_tinfajt02`
  - **Who_Must_Be_Elig**: `one`

### 31. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_tinfajt02`
  - **Output Variable:** `i_tinjnkt`
    - Band: Rate=`$tin_capinc_natrate4`, Limit=``

### 32. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_tinfajt02`
  - **Output Variable:** `i_tinjnkc`
    - Band: Rate=`$tin_capinc_natrate4`, Limit=``

### 33. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_tinfajt02`
  - **Output Variable:** `i_tinjrkc`
    - Band: Rate=`$tin_capinc_natrate4`, Limit=``

### 34. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_tinfajt02`
  - **Output Variable:** `i_tinjrkt`
    - Band: Rate=`$tin_capinc_natrate4`, Limit=``

### 35. Function: ArithOp
  **Formula:** `i_tinjngt - i_tinjngc +  i_tinjnkt-i_tinjnkc`
  **Output Variable:** `i_tingtjnt`
  **Tax Unit:** `tu_tinfajt02`

### 36. Function: ArithOp
  **Formula:** `i_tinjrgt - i_tinjrgc +  i_tinjrkt - i_tinjrkc`
  **Output Variable:** `i_tingtjrg`
  **Tax Unit:** `tu_tinfajt02`

### 37. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tingtjrg > 0`
  - **comp_perTu**: `min(il_tintcmo,$tin_mortgtc_amt1)*$tin_mortgtc_regrate1`
  - **output_var**: `i_tintircmt`
  - **TAX_UNIT**: `tu_tinfajt02`

### 38. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTu**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Who_Must_Be_Elig**: `n/a`

### 39. Function: Elig
  **Eligibility Check:**
  - **Condition:** `il_tinty > 0 & (IsMarried | IsParentOfDepChild) `
  - **Tax Unit:** `tu_tinfajt02`

### 40. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTu**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Who_Must_Be_Elig**: `n/a`

### 41. Function: ArithOp
  **Formula:** `i_tingtjnt -  i_tintjncmt -  i_tintjncrt - i_tinjwkintc`
  **Output Variable:** `i_tintjnt`
  **Tax Unit:** `tu_tinfajt02`

### 42. Function: DefIl
  - **Name**: `il_tintbijt`
  - **il_tinty**: `+`
  - **sin14_s**: `-`

### 43. Function: ArithOp
  **Formula:** `max(il_tintbijt,0)`
  **Output Variable:** `i_tintjbg`
  **Tax Unit:** `tu_tinfajt02`

### 44. Function: Elig
  **Eligibility Check:**
  - **Condition:** `sin17_s & yiy-i_tinextjcn> 0`
  - **Tax Unit:** `tu_tinfajt02`

### 45. Function: Elig
  **Eligibility Check:**
  - **Condition:** `sin17_s & yiy-i_tinextjcr> 0`
  - **Tax Unit:** `tu_tinfajt02`

### 46. Function: Elig
  **Eligibility Check:**
  - **Condition:** `sin17_s`
  - **Tax Unit:** `tu_tinfajt02`

### 47. Function: DefVar
  - **i_tinextjcr**: `0`
  - **i_tinextjcn**: `0`
  - **i_tinjnkt**: `0`
  - **i_tintjncmt**: `0`
  - **i_tintjrg**: `0`
  - **i_tintjnt**: `0`
  - **i_tintjrcrt**: `0`
  - **i_tingtjrg**: `0`
  - **i_tintjrcmt**: `0`
  - **i_tingtjnt**: `0`
  - **i_tinjrkc**: `0`
  - **i_tinjrkt**: `0`
  - **i_tinjnkc**: `0`
  - **i_tintjbg**: `0`
  - **i_tintjkb**: `0`
  - **i_tinextjta**: `0`
  - **i_tintjncrt**: `0`
  - **i_tinjrgc**: `0`
  - **i_tinjngc**: `0`
  - **i_tinjrgt**: `0`
  - **i_tinjngt**: `0`
  - **i_tintjcee**: `n/a`
  - **i_tinjwkintc**: `0`

### 48. Function: Elig
  **Eligibility Check:**
  - **Condition:** `sin17_s & tintbjt_s > il_tintcjtrg`
  - **Tax Unit:** `tu_tinfajt02`

### 49. Function: ArithOp
  **Formula:** `sin05_s`
  **Output Variable:** `sin12_s`
  **Tax Unit:** `tu_tinfajt`

### 50. Function: ArithOp
  **Formula:** `sin45_s`
  **Output Variable:** `sin47_s`
  **Tax Unit:** `tu_tinfajt`

### 51. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `i_reg_70=1 & dag > 75`
  - **Comp_perTU**: `$tin_perallrg70_amt3`
  - **Comp_perElig**: `$tin_perallrg53_amt3`
  - **Output_Var**: `sin52_s`
  - **TAX_UNIT**: `tu_tinfajt02`

### 52. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `i_reg_51 = 1 & ((tintbit_s + i_tintikb) < $tin_perallrg51_lim)`
  - **Comp_perTU**: `$tin_perallrg51_amt - $tin_perall_amt1`
  - **Output_Add_Var**: `sin11_s`
  - **TAX_UNIT**: `tu_tinfajt02`

### 53. Function: DefIl
  - **name**: `il_tintcjtrg`
  - **sin52_s**: `+`
  - **sin47_s**: `+`
  - **sin48_s**: `+`

### 54. Function: ArithOp
  **Formula:** `sin46_s`
  **Output Variable:** `sin48_s`
  **Tax Unit:** `tu_tinfajt`

### 55. Function: BenCalc
  - **Comp_Cond**: `ils_earns >0 & il_tinwkgr > $tin_wkintc_lim1 & il_tinwkgr<= $tin_wkintc_lim2 & il_tinot <= $tin_empall_lim3`
  - **Comp_perTU**: `min(i_tiningt-i_tiningc+i_tinirgt-i_tinirgc, $tin_wkintc_amt-$tin_wkintc_rate*(il_tinwkgr - $tin_wkintc_lim1))`
  - **Output_Var**: `i_tinjwkintc`
  - **TAX_UNIT**: `tu_individual_es`


---

## Policy: tintcrgjt_es
### 1. Function: DefVar
  - **i_tbbefpfa_j**: `0`
  - **i_tbaftpfa_j**: `0`
  - **i_gtbaftpfa_j**: `0`
  - **i_tcrgba_j**: `0`
  - **i_tcrgdb_j**: `0`
  - **i_tcrglp_j**: `0`
  - **i_tcrgdp_j**: `0`
  - **i_tcrgoa_j**: `0`
  - **i_tcrgfa_j**: `0`
  - **i_tcrglg_j**: `0`
  - **i_tcrgch_j**: `0`
  - **i_tcrgcc_j**: `0`
  - **i_tcrgrt_j**: `0`
  - **i_tcrgee_j**: `0`
  - **i_bchbamt_j**: `0`
  - **i_tcrghk_j**: `0`
  - **i_tcrgwm_j**: `0`
  - **i_tcrg_j**: `0`
  - **i_tcrgmo_j**: `0`
  - **i_tcrgun_j**: `0`
  - **i_tcrgse_j**: `0`
  - **i_tinitrg_j**: `0`
  - **i_tcrgli_j**: `0`
  - **i_tcrgw_j**: `0`

### 2. Function: ArithOp
  **Formula:** `tintbjt_s + yiy`
  **Output Variable:** `i_tbbefpfa_j`
  **Tax Unit:** `tu_tinfajt02`

### 3. Function: ArithOp
  **Formula:** `tintbjt_s +yiy - sin04_s - sin05_s - sin06_s`
  **Output Variable:** `i_tbaftpfa_j`
  **Tax Unit:** `tu_individual_es`

### 4. Function: ArithOp
  **Formula:** `tintbjt_s - sin04_s - sin05_s - sin06_s`
  **Output Variable:** `i_gtbaftpfa_j`
  **Tax Unit:** `tu_individual_es`

### 5. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrgba_j`
  **Tax Unit:** `tu_individual_es`

### 6. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_bchbamt_j`
  **Tax Unit:** `tu_individual_es`

### 7. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrgdb_j`
  **Tax Unit:** `tu_individual_es`

### 8. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrglp_j`
  **Tax Unit:** `tu_individual_es`

### 9. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrgdp_j`
  **Tax Unit:** `tu_individual_es`

### 10. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrgoa_j`
  **Tax Unit:** `tu_individual_es`

### 11. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrgfa_j`
  **Tax Unit:** `tu_individual_es`

### 12. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrglg_j`
  **Tax Unit:** `tu_individual_es`

### 13. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrgch_j`
  **Tax Unit:** `tu_individual_es`

### 14. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrgcc_j`
  **Tax Unit:** `tu_individual_es`

### 15. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrgrt_j`
  **Tax Unit:** `tu_individual_es`

### 16. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrgee_j`
  **Tax Unit:** `tu_individual_es`

### 17. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrghk_j`
  **Tax Unit:** `tu_individual_es`

### 18. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrgwm_j`
  **Tax Unit:** `tu_individual_es`

### 19. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrgmo_j`
  **Tax Unit:** `tu_individual_es`

### 20. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrgun_j`
  **Tax Unit:** `tu_individual_es`

### 21. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrgse_j`
  **Tax Unit:** `tu_individual_es`

### 22. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tinitrg_j`
  **Tax Unit:** `tu_individual_es`

### 23. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_tcrgli_j`
  **Tax Unit:** `tu_individual_es`

### 24. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 61 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 25. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nPersInUnit > 5`
  - **comp_perTU**: `(8 + (nPersInUnit - 5) ) * $SMI`
  - **output_var**: `sin31_s`
  - **TAX_UNIT**: `tu_bch00`

### 26. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `il_bch00 < sin31_s & IsParentOfDepChild & nDepChInTu#2 >= 2`
  - **comp_perTU**: `12000 + (1200 * (nDepChInTu#2 - 2) )`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `i_bchbamt_j`
  - **TAX_UNIT**: `tu_bch00`

### 27. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu > 0 & i_tbbefpfa_j<= 25000#y`
  - **comp_perTU**: `200#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `i_tcrgba_j`
  - **TAX_UNIT**: `tu_tinfajt02`

### 28. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsLoneParentOfDepChild & i_tbbefpfa_j < 100000#y`
  - **comp_perTU**: `100#y`
  - **output_add_var**: `i_tcrglp_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 29. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsDepParent & dag > 75 & i_tbbefpfa_j < 100000#y`
  - **comp_perTU**: `100#y`
  - **output_add_var**: `i_tcrgdp_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 30. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 = 0 & ddi#1 > 0 & i_tbbefpfa_j < 100000#y`
  - **comp_perElig**: `100#y`
  - **output_add_var**: `i_tcrgdb_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`

### 31. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 > 0 & ddi#1 > 0 & i_tbbefpfa_j < 24000#y`
  - **comp_perTU**: `100#y`
  - **#_level**: `tu_individual_es`
  - **output_add_var**: `i_tcrgdb_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 32. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 > 0 & dag#1 < 35 & i_tbbefpfa_j < $tintc_rg61_rent_lim_jt`
  - **comp_perTU**: `min(0.15*xhcrt,$tintc_rg61_rent_amt)`
  - **output_add_var**: `i_tcrgrt_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`

### 33. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 24 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 34. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu >= 3 & i_tbaftpfa_j < 35000#y`
  - **comp_perTU**: `100#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `i_tcrgba_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 35. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsDepParent & dag#1 > 75 & i_tinty > 0 & i_tbaftpfa_j < 35000#y`
  - **comp_perElig**: `150#y`
  - **output_add_var**: `i_tcrgdb_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`

### 36. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 12 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 37. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & i_tbbefpfa_j < $tintc_rg12_rent_lim_jt`
  - **comp_perTU**: `min(0.10*xhcrt,$tintc_rg12_rent_lim_amt)`
  - **output_add_var**: `i_tcrgrt_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 38. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tbbefpfa_j<45000#y & dlg_s=1 &nDepChInTu>=5`
  - **comp_perTU**: `2000#y`
  - **output_add_var**: `i_tcrglg_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 39. Function: BenCalc
  - **comp_cond**: `IsLoneParentOfDepChild & i_tbbefpfa_i<45000#y`
  - **comp_perTU**: `500#y`
  - **output_add_var**: `i_tcrglp_j`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Who_Must_Be_Elig**: `one`

### 40. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 41. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 53 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 42. Function: BenCalc *(Switch: off)*
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 > 0 & dag#1 > 65 & i_tbaftpfa_j#1 <= 25000#y`
  - **comp_perElig**: `50#y`
  - **output_add_var**: `i_tcrgoa_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`

### 43. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `ddi#1 > 0 & i_tbaftpfa_j <= 52800#y`
  - **comp_perElig**: `88#y`
  - **output_add_var**: `i_tcrgdb_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`

### 44. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_add_var**: `i_tcrgch_j`
  - **TAX_UNIT**: `tu_tintcrg01`

### 45. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_add_var**: `n/a`
  - **#_level**: `n/a`
  - **TAX_UNIT**: `n/a`

### 46. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 70 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 47. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu >= 5  &i_tbaftpfa_j <= 57200#y`
  - **comp_perTU**: `840#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `i_tcrgba_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 48. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#2 > 0 & tintbjt_s <= 57200#y`
  - **comp_perTU**: `min(400#y*nDepChInTu#1,xcc*0.15)`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `2`
  - **#_level**: `tu_individual_es`
  - **output_add_var**: `i_tcrgcc_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 49. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 > 0 & dag#1 > 65 & tintbjt_s <= 52000#y`
  - **comp_perElig**: `120#y`
  - **#_level**: `tu_individual_es`
  - **output_add_var**: `i_tcrgdb_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 50. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dlg_s = 1 & nDepChInTu >= 5`
  - **comp_perTU**: `600#y`
  - **output_add_var**: `i_tcrglg_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 51. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(bunct_s>0 |bunnc_s>0) & lunmy_s>=6 & 11200#y<i_tinwk#1 & i_tinwk#1<22000#y & il_tinot#1<1600#y`
  - **comp_perTU**: `100#y`
  - **#_level**: `tu_individual_es`
  - **output_add_var**: `i_tcrgun_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 52. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `tintbjt_s <=$tintc_rg70_rent_lim_jt`
  - **comp_perTU**: `min(0.20*xhcrt,$tintc_rg70_rent_minamt)`
  - **output_add_var**: `i_tcrgrt_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 53. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 13 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 54. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `ddi#2 > 0 & i_tinty#2 <= 6000#y`
  - **comp_perTU**: `100#y * nDepChInTu#1`
  - **comp_perElig**: `100#y`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `2`
  - **output_add_var**: `i_tcrgfa_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`

### 55. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 > 0 & i_tbbefpfa_j <= 31000#y & (dag#1 < 35 | dag#1 > 65 | ddi#1 > 0)`
  - **comp_perTU**: `min(0.10*xhcrt,600#y)`
  - **output_add_var**: `i_tcrgrt_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`

### 56. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 42 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 57. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsParentOfDepChild & i_tbbefpfa_j < 36000#y`
  - **comp_perTU**: `100#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `i_tcrgba_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 58. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsDepParent & dag#1 > 75 & i_tbbefpfa_j < 36000#y`
  - **comp_perElig**: `150#y`
  - **output_add_var**: `i_tcrgfa_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`

### 59. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 > 0 & dag#1 > 75 & i_tbbefpfa_j < 36000#y`
  - **comp_perElig**: `150#y`
  - **output_add_var**: `i_tcrgoa_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`

### 60. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 41 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 61. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu > 3 & i_tbaftpfa_j<= 31500#y`
  - **comp_perTU**: `450#y * (nDepChInTu - 3)`
  - **output_add_var**: `i_tcrglg_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 62. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(( IsParentOfDepChild & ils_earns#1 & GetPartnerIncome#2 > 0 ) | ( IsLoneParentOfDepChild & ils_earns#1 )) & i_tbaftpfa_j <= 31500#y & nDepChInTu#3 > 0`
  - **comp_perTU**: `min(322#y,xcc*0.3)`
  - **#_level**: `tu_individual_es`
  - **#_income**: `ils_earns`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `3`
  - **output_add_var**: `i_tcrgcc_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 63. Function: BenCalc *(Switch: off)*
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 > 0 & dag#1 < 36 & drgur = 0 & i_tbaftpfa_j <= 31500#y`
  - **comp_perTU**: `min(0.20*xhcrt,612#y)`
  - **output_add_var**: `i_tcrgrt_i`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfait`

### 64. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 51 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 65. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsParentOfDepChild & nDepChInTu#1 >= 1`
  - **comp_perTU**: `300#y`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `i_tcrgba_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 66. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 > 0 & i_tbbefpfa_j <=$tintc_rg51_rent_lim_jt & (dag#1 < 32 | lunmy#1 > 6 | ( dag#1 > 65 & dms#1 = 5) )`
  - **comp_perTU**: `min(0.10*xhcrt,$tintc_rg51_rent_minamt2)`
  - **output_add_var**: `i_tcrgrt_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`

### 67. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tingtjnt > 0 & i_tcrgmocond51=1`
  - **comp_perTu**: `min(il_tintcmo,$tin_mortgtc_amt2)*$tintcrgit_mortgtcrg51_totrate2`
  - **output_add_var**: `i_tcrgmo_j`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Comp_Cond**: `i_tingtjnt > 0 & i_tcrgmocond51!=1`
  - **Comp_perTU**: `min(il_tintcmo,$tin_mortgtc_amt2)*$tintcrgit_mortgtcrg51_totrate1`

### 68. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 43 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 69. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tbbefpfa_j <= 60100#y & (dag < 36  | dlg_s = 1 | IsDisabled)`
  - **comp_perTU**: `min(0.3*xhcrt, 1500#y)`
  - **output_add_var**: `i_tcrgrt_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 70. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 > 0 & i_tinwk#1 > 0 & i_tinwk#1 <= 12000#y & il_tinot#1 <= 300#y`
  - **comp_perElig**: `75#y`
  - **output_add_var**: `i_tcrgee_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`

### 71. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 11 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 72. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu#2 > 0 & i_tbaftpfa_j > 22000#y & i_tbaftpfa_j <= 31000#y`
  - **comp_perTU**: `300#y * nDepChInTu#2`
  - **#_AgeMin**: `1`
  - **#_AgeMax**: `2`
  - **output_add_var**: `i_tcrgba_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 73. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu > 4`
  - **comp_perTU**: `150#y`
  - **output_add_var**: `i_tcrglg_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 74. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(( IsParentOfDepChild & ils_earns#1 & GetPartnerIncome#2 > 0 ) | ( IsLoneParentOfDepChild & ils_earns#1 )) & i_tbaftpfa_j <= 31000#y & nDepChInTu#3 > 0`
  - **comp_perTU**: `min(200#y,xcc*0.3)`
  - **#_level**: `tu_individual_es`
  - **#_income**: `ils_earns`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `3`
  - **output_add_var**: `i_tcrgcc_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 75. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty > 0 & dag < 36 & i_tbbefpfa_j <= 22000#y & NChildrenOfCouple < 2`
  - **comp_perTU**: `min(0.10*xhcrt,300#y)`
  - **output_add_var**: `i_tcrgrt_j`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Comp_perTU**: `min(0.10*xhcrt,600#y)`
  - **Comp_Cond**: `i_tinty > 0 & dag < 36 & i_tbbefpfa_j <= 22000#y & NChildrenOfCouple >= 2`

### 76. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 30 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 77. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu#1 > 1 & i_tbbefpfa_i#2 <= 25620#y & i_tbbefpfa_j <= 37322.20#y`
  - **comp_perTU**: `721.70#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **#_level**: `tu_individual_es`
  - **output_add_var**: `i_tcrgba_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 78. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 > 0 & dag#1 < 35 & i_tbbefpfa_j <= $tintc_rg30_rent_lim_jt`
  - **comp_perTU**: `min(0.30*xhcrt,$tintc_rg30_rent_amt)`
  - **output_add_var**: `i_tcrgrt_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`

### 79. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_tinfajt02`
  - **Output Variable:** `i_tinitrg_j`

### 80. Function: BenCalc
  - **comp_cond**: `i_tinty > 0 & i_tbbefpfa_j <= 24000#y & IsParentOfDepChild & nDepChInTu>=2`
  - **comp_perTU**: `0.10 * (i_tingtjrg - i_tintircmt - i_tintjrcrt-i_tcrgba_j-i_tcrgrt_j)`
  - **lowlim**: `0`
  - **output_add_var**: `i_tcrgli_j`
  - **TAX_UNIT**: `tu_tinfajt02`
  - **Who_Must_Be_Elig**: `one`

### 81. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 62 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 82. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(IsParentOfDepChild & ils_earns#1)  &  i_tbbefpfa_i <= 50000#y & nDepChInTu#3 > 0`
  - **comp_perTU**: `min(1000#y*nDepChInTu#3,xcc*0.20)`
  - **#_level**: `tu_individual_es`
  - **#_income**: `n/a`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `2`
  - **output_add_var**: `i_tcrgcc_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 83. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 23 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 84. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu#1 =3`
  - **comp_perTU**: `900#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `i_tcrgba_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 85. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 22 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 86. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 52 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 87. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu > 0 & i_tbbefpfa_j <= 37000#y`
  - **comp_perTU**: `270#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `i_tcrgba_j`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Comp_perTU**: `270#y  * (1-((i_tbbefpfa_j-37000)/3000)) * nDepChInTu#1`
  - **Comp_Cond**: `nDepChInTu > 0 & (i_tbbefpfa_j >37000#y & i_tbbefpfa_j <=40000#y)`

### 88. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu#1 > 1 & i_tbbefpfa_j <= 37000#y`
  - **comp_perTU**: `224#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `i_tcrgba_j`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Comp_perTU**: `224#y  * (1-((i_tbbefpfa_j-37000)/3000)) * nDepChInTu#1`
  - **Comp_Cond**: `nDepChInTu > 1 & (i_tbbefpfa_j >37000#y & i_tbbefpfa_j <=40000#y)`

### 89. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dlg_s = 1 & nDepChInTu >= 5 & i_tbbefpfa_j <=46000#y`
  - **comp_perTU**: `600#y`
  - **output_add_var**: `i_tcrglg_j`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Comp_perTU**: `600#y  * (1-((i_tbbefpfa_j-46000)/3000))`
  - **Comp_Cond**: `dlg_s = 1 & nDepChInTu >= 5 & (i_tbbefpfa_j >46000#y & i_tbbefpfa_j <=50000#y)`

### 90. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 > 0 & ddi#1 > 0 & dag#1 > 65  & i_tbbefpfa_j <= 37000#y`
  - **comp_perTU**: `179#y`
  - **output_add_var**: `i_tcrgdb_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Comp_perTU**: `179#y  * (1-((i_tbbefpfa_j-37000)/3000))`
  - **Comp_Cond**: `i_tinty#1 > 0 & ddi#1 > 0 & dag#1 > 65  & (i_tbbefpfa_j >37000#y & i_tbbefpfa_j <=40000#y)`

### 91. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dms#1 = 2 & idpartner#1 > 0 & (i_tinwk#1 > 0 | yse#1 > 0)`
  - **comp_perElig**: `1`
  - **output_var**: `i_nospinwrk`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`

### 92. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dms#1 = 2 & idpartner#1 > 0 & i_tinwk#1 = 0 & yse#1 = 0 & nDepChOfCouple > 1 & i_nospinwrk = 1 & i_tbbefpfa_j <= 23000#y`
  - **comp_perTU**: `153#y`
  - **output_add_var**: `i_tcrghk_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Comp_perTU**: `153#y  * (1-((i_tbbefpfa_j-23000)/2000))`
  - **Comp_Cond**: `dms#1 = 2 & idpartner#1 > 0 & i_tinwk#1 = 0 & yse#1 = 0 & nDepChOfCouple > 1 & i_nospinwrk = 1 & (i_tbbefpfa_j >23000#y & i_tbbefpfa_j <=25000#y)`

### 93. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsParentOfDepChild & ils_earns#1 > 0 & (GetPartnerIncome#2 > 0 | IsLoneParentOfDepChild) & i_tbbefpfa_j <= 37000#y`
  - **comp_perTU**: `265#y * nDepChInTu#3`
  - **#_level**: `tu_individual_es`
  - **#_income**: `ils_earns`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `2`
  - **output_add_var**: `i_tcrgcc_j`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Comp_perTU**: `265#y  * (1-((i_tbbefpfa_j-37000)/3000))`
  - **Comp_Cond**: `IsParentOfDepChild & ils_earns#1 > 0 & (GetPartnerIncome#2 > 0 | IsLoneParentOfDepChild) & (i_tbbefpfa_j >37000#y & i_tbbefpfa_j <=40000#y)`

### 94. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 > 0 & i_tbbefpfa_j <= 37000#y`
  - **comp_perTU**: `179#y * i_nodepprt`
  - **output_add_var**: `i_tcrgdp_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Comp_perTU**: `179#y * (1-((i_tbbefpfa_j-37000)/3000))* i_nodepprt
`
  - **Comp_Cond**: `i_tinty#1 > 0 & (i_tbbefpfa_j >37000#y & i_tbbefpfa_j <=40000#y)`

### 95. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChOfCouple#1 > 0 & (dgn=0 | (dgn=1 & idpartner=0))& il_sic > 0 & i_tbbefpfa_j <= 37000#y`
  - **comp_perTU**: `min(418#y,il_sic)*nDepChOfCouple#1`
  - **#_level**: `tu_tintcrg02`
  - **output_add_var**: `i_tcrgwm_j`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_perTU**: `min(418#y,il_sic)*(1-((i_tbbefpfa_j-37000)/3000))*nDepChOfCouple#1`
  - **Comp_Cond**: `nDepChOfCouple#1 > 0 & (dgn=0 | (dgn=1 & idpartner=0))& il_sic > 0 &(i_tbbefpfa_j >37000#y & i_tbbefpfa_j <=40000#y)`

### 96. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_tinty#1 > 0 & !IsDepChild & i_tbbefpfa_j <= 37000#y & (dag#1 < 35 | ddi#1 > 0)`
  - **comp_perTU**: `min(0.20*xhcrt,612#y*2)`
  - **output_add_var**: `i_tcrgrt_j`
  - **#_level**: `tu_individual_es`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Comp_perTU**: `min(0.20*xhcrt,612#y*2*(1-((i_tbbefpfa_j-37000#y)/3000#y)))`
  - **Comp_Cond**: `i_tinty#1 > 0 & !IsDepChild & (i_tbbefpfa_j >37000#y & i_tbbefpfa_j <=40000#y) & (dag#1 < 35 | ddi#1 > 0)`

### 97. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_tinfajt02`
  - **Output Variable:** `i_tinitrg_j`

### 98. Function: BenCalc
  - **comp_cond**: `i_tinty > 0 & i_tbbefpfa_j <= 24000#y & IsParentOfDepChild & nDepChInTu>=2`
  - **comp_perTU**: `0.10 * (i_tingtjrg - i_tintircmt - i_tintjrcrt-i_tcrgba_j-i_tcrgrt_j)`
  - **lowlim**: `0`
  - **output_add_var**: `i_tcrgli_j`
  - **TAX_UNIT**: `tu_tinfajt02`
  - **Who_Must_Be_Elig**: `one`

### 99. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 21 & sin17_s = 1`
  - **Tax Unit:** `tu_individual_es`

### 100. Function: ArithOp
  **Formula:** `i_tcrgba_j + i_tcrgdb_j + i_tcrglp_j + i_tcrgdp_j + i_tcrgoa_j + i_tcrgfa_j + i_tcrglg_j + i_tcrgch_j + i_tcrgcc_j + i_tcrgrt_j + i_tcrgee_j + i_tcrghk_j +  i_tcrgwm_j +  i_tcrgmo_j +i_tcrgun_j+i_tcrgse_j + i_tcrgli_j`
  **Output Variable:** `i_tcrg_j`
  **Tax Unit:** `tu_individual_es`

### 101. Function: ArithOp
  **Formula:** `i_tingtjrg - i_tintircmt - i_tintjrcrt - i_tcrg_j`
  **Output Variable:** `i_tintjrg
`
  **Tax Unit:** `tu_tinfajt02`

### 102. Function: BenCalc
  - **Comp_perTU**: `1000#y *nDepChInTu#1`
  - **Comp_Cond**: `nDepChInTu#1>1`
  - **Output_Add_Var**: `i_tcrgrt_j`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Who_Must_Be_Elig**: `one`
  - **#_AgeMax**: `0`
  - **#_AgeMin**: `0`

### 103. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu > 2  & i_tbaftpfa_j<= 31500#y`
  - **comp_perTU**: `2351#y * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_var**: `i_tcrgba_j`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Comp_perTU**: `n/a`
  - **Comp_Cond**: `n/a`

### 104. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dlg_s >0 & nDepChInTu >= 5`
  - **comp_perTU**: `400#y`
  - **output_add_var**: `i_tcrglg_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 105. Function: BenCalc
  - **Comp_perTU**: `900#y*nDepChInTu#1`
  - **Comp_Cond**: `nDepChildrenInTu#1>2`
  - **Output_Add_Var**: `i_tcrgba_j`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Who_Must_Be_Elig**: `one`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`

### 106. Function: BenCalc
  - **Comp_perTU**: `300#y*nDepChInTu#1`
  - **Comp_Cond**: `nDepChildrenInTu#1=2`
  - **Output_Add_Var**: `i_tcrgba_j`
  - **TAX_UNIT**: `tu_tinfajt`
  - **Who_Must_Be_Elig**: `one`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`

### 107. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dms=1 & i_tbbefpfa_i < 24000#y`
  - **comp_perTU**: `100#y`
  - **output_add_var**: `i_tcrgw_j`
  - **TAX_UNIT**: `tu_tinfajt`

### 108. Function: ArithOp
  **Formula:** `i_tintjrg+i_tintjnt`
  **Output Variable:** `tinjt_s`
  **Tax Unit:** `tu_tinfajt02`


---

## Policy: tinopt_es
### 1. Function: BenCalc
  - **comp_cond**: `sin17_s = 1 & tinit_s#1 > tinjt_s#1`
  - **comp_perTu**: `22`
  - **#_level**: `tu_tinfajt02`
  - **output_var**: `tintp_s`
  - **TAX_UNIT**: `tu_individual_es`

### 2. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `tinjt_s`
  - **output_var**: `tin_s`
  - **TAX_UNIT**: `tu_individual_es`

### 3. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tingtjnt + i_tingtjrg`
  - **output_var**: `tingt_s`
  - **TAX_UNIT**: `tu_individual_es`

### 4. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `sin11_s`
  - **output_var**: `tinta00_s`
  - **TAX_UNIT**: `tu_individual_es`

### 5. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `sin12_s`
  - **output_var**: `tintach_s`
  - **TAX_UNIT**: `tu_individual_es`

### 6. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `sin13_s`
  - **output_var**: `tintadp_s`
  - **TAX_UNIT**: `tu_individual_es`

### 7. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `sin14_s`
  - **output_var**: `tintaee_s`
  - **TAX_UNIT**: `tu_individual_es`

### 8. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `tintbjt_s`
  - **output_var**: `tintb_s`
  - **TAX_UNIT**: `tu_individual_es`

### 9. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tinjrgc+i_tinjngc+i_tinjnkc+i_tinjrkc`
  - **output_var**: `tintc00_s`
  - **TAX_UNIT**: `tu_individual_es`

### 10. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tintjncmt+i_tintircmt`
  - **output_var**: `tintcmg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 11. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tintjncrt+i_tintjrcrt`
  - **output_var**: `tintcrt_s`
  - **TAX_UNIT**: `tu_individual_es`

### 12. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTu**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 13. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tintjncmt+i_tintircmt+i_tintjncrt+i_tintjrcrt+i_tinjngc+i_tinjrgc+i_tinjwkintc`
  - **output_var**: `tintc_s`
  - **TAX_UNIT**: `tu_individual_es`

### 14. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tintjrg`
  - **output_var**: `tinrg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 15. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tintjnt`
  - **output_var**: `tinna_s`
  - **TAX_UNIT**: `tu_individual_es`

### 16. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tintjkb`
  - **output_var**: `tintbiy_s`
  - **TAX_UNIT**: `tu_individual_es`

### 17. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tingtjnt`
  - **output_var**: `tingtna_s`
  - **TAX_UNIT**: `tu_individual_es`

### 18. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tingtjrg`
  - **output_var**: `tingtrg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 19. Function: BenCalc
  - **Comp_Cond**: `tintp_s = 22`
  - **Comp_perTU**: `i_tinjwkintc`
  - **Output_Var**: `tintcot_s`
  - **TAX_UNIT**: `tu_individual_es`


---

## Policy: tinoptrg_es
### 1. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tcrg_j`
  - **output_var**: `tintcrg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 2. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tcrgba_j`
  - **output_var**: `tintcbarg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 3. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tcrgdb_j`
  - **output_var**: `tintcdbrg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 4. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tcrglp_j`
  - **output_var**: `tintclprg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 5. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tcrgdp_j`
  - **output_var**: `tintcdprg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 6. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tcrgoa_j`
  - **output_var**: `tintcoarg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 7. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tcrgfa_j`
  - **output_var**: `tintcfarg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 8. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tcrglg_j`
  - **output_var**: `tintclgrg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 9. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tcrgch_j`
  - **output_var**: `tintcchrg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 10. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tcrgcc_j`
  - **output_var**: `tintcccrg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 11. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tcrgrt_j`
  - **output_var**: `tintcrtrg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 12. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tcrgee_j`
  - **output_var**: `tintceerg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 13. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tcrghk_j`
  - **output_var**: `tintchkrg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 14. Function: BenCalc
  - **comp_cond**: `tintp_s = 22`
  - **comp_perTu**: `i_tcrgwm_j`
  - **output_var**: `tintcwmrg_s`
  - **TAX_UNIT**: `tu_individual_es`

### 15. Function: Allocate
  - **Share**: `tin_s`
  - **Output_Var**: `tin_s`
  - **TAX_UNIT**: `tu_tinfajt02`
  - **Share_Prop**: `ils_base_tin`
  - **Who_Must_Be_Elig**: `one`
  - **Share_Equ_IfZero**: `yes`

### 16. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(tintp_s = 22)`
  - **Tax Unit:** `tu_individual_es`


---

## Policy: tintrch_es
### 1. Function: DefConst
  **Constants Defined:**
  - `$tintrch_amt`: 1200#y

### 2. Function: DefTu
  - **Name**: `tu_tintrch`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `Default & dag < 3`

### 3. Function: BenCalc
  - **comp_cond**: `nDepChOfCouple#1 > 0 & (dgn=0 | (dgn=1 & idpartner=0))& (il_sic > 0 | il_tintrch> 0)`
  - **comp_perElig**: `min($tintrch_amt,il_sic)*nDepChOfCouple#1`
  - **#_level**: `tu_tintrch`
  - **output_var**: `tintrch_s`
  - **TAX_UNIT**: `tu_individual_es`

### 4. Function: DefIl
  - **Name**: `il_tintrch`
  - **bunct_s**: `+`
  - **bunct02_s**: `+`
  - **bunnc_s**: `+`
  - **bunmt_s**: `+`
  - **bunot**: `+`


---

## Policy: bchrg_es
### 1. Function: SetDefault
  - **dataset**: `*`
  - **bchrg_s**: `0`
  - **bchucrg_s**: `0`
  - **bchmtrg_s**: `0`
  - **bchbarg_s**: `0`
  - **bchbaucrg_s**: `0`
  - **bchbamtrg_s**: `0`
  - **bchlgrg_s**: `0`
  - **bchlgucrg_s**: `0`
  - **bchlgmtrg_s**: `0`

### 2. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `sin31_s`
  **Tax Unit:** `tu_individual_es`

### 3. Function: ArithOp
  **Formula:** `tintb_s-tinta00_s-tintach_s-tintadp_s`
  **Output Variable:** `sin32_s`
  **Tax Unit:** `tu_bch00`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 61`
  - **Tax Unit:** `tu_individual_es`

### 5. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 24`
  - **Tax Unit:** `tu_individual_es`

### 7. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 12`
  - **Tax Unit:** `tu_individual_es`

### 8. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 9. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 53`
  - **Tax Unit:** `tu_individual_es`

### 10. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 70`
  - **Tax Unit:** `tu_individual_es`

### 11. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 13`
  - **Tax Unit:** `tu_individual_es`

### 12. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `tintp_s = 22 & IsParentOfDepChild & IsHead`
  - **comp_perTU**: `$bchrg_reg13_lim3`
  - **Output_Var**: `sin31_s`
  - **TAX_UNIT**: `tu_bch00`

### 13. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 14. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 42`
  - **Tax Unit:** `tu_individual_es`

### 15. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `nDepChInTu > 2 & nDepChInTu < 7  `
  - **comp_perTU**: `($IPREM) * (1+ (nDepChInTu) )`
  - **Output_Var**: `sin31_s`
  - **TAX_UNIT**: `tu_largefam`
  - **Comp_Cond**: `nDepChInTu > 6 `
  - **Comp_perTU**: `$IPREM*8`

### 16. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 17. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 18. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 41`
  - **Tax Unit:** `tu_individual_es`

### 19. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 20. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 21. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 22. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 51`
  - **Tax Unit:** `tu_individual_es`

### 23. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 24. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 25. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **Output_Var**: `sin31_s`
  - **TAX_UNIT**: `tu_bch00`

### 26. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `IsParentOfDepChild & nDepChInTu#1 >0 & tintb_s <=sin31_s & ( dlg_s=1 | IsLoneParentOfDepChild)`
  - **comp_perTU**: `$bchrg_reg51_amt2*nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **Output_Add_Var**: `bchbamtrg_s`
  - **TAX_UNIT**: `tu_bch00`

### 27. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 43`
  - **Tax Unit:** `tu_individual_es`

### 28. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 29. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 30. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 31. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 11`
  - **Tax Unit:** `tu_individual_es`

### 32. Function: ArithOp
  **Formula:** `$bchrg_reg11_lim1`
  **Output Variable:** `sin31_s`
  **Tax Unit:** `tu_bch00`

### 33. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `sin32_s <= sin31_s & IsParentOfDepChild & nDepChInTu#1=1`
  - **comp_perTU**: `$bchrg_reg11_amt1`
  - **#_AgeMin**: `1`
  - **#_AgeMax**: `2`
  - **output_add_var**: `bchmtrg_s`
  - **TAX_UNIT**: `tu_bch00`
  - **Comp_perTU**: `$bchrg_reg11_amt1+$bchrg_reg11_amt2+$bchrg_reg11_amt3*(nDepChildrenInTu#1 -2)`
  - **Comp_Cond**: `sin32_s <= sin31_s & IsParentOfDepChild & nDepChInTu#1>=3`

### 34. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 23`
  - **Tax Unit:** `tu_individual_es`

### 35. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 30`
  - **Tax Unit:** `tu_individual_es`

### 36. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 37. Function: Allocate *(Switch: n/a)*
  - **share**: `n/a`
  - **share_between**: `n/a`
  - **share_all_ifnoelig**: `n/a`
  - **output_var**: `n/a`
  - **tax_unit**: `n/a`

### 38. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 62`
  - **Tax Unit:** `tu_individual_es`

### 39. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 22`
  - **Tax Unit:** `tu_individual_es`

### 40. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 41. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 42. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 43. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 44. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 52`
  - **Tax Unit:** `tu_individual_es`

### 45. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgn2 = 21`
  - **Tax Unit:** `tu_individual_es`

### 46. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`

### 47. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `bchbamtrg_s`
  - **TAX_UNIT**: `tu_bchrg21`

### 48. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 49. Function: ArithOp
  **Formula:** `bchmtrg_s + bchucrg_s + bchbamtrg_s + bchbaucrg_s + bchlgmtrg_s + bchlgucrg_s`
  **Output Variable:** `bchrg_s`
  **Tax Unit:** `tu_individual_es`

### 50. Function: BenCalc
  - **Comp_perTU**: `(0.25)*$bchrg_reg24_basic_amt*nDepChildrenInTu#1`
  - **Comp_Cond**: `sin32_s>$bchrg_reg24_lim5 & sin32_s<=$bchrg_reg24_lim6 & IsParentOfDepChild & nDepChInTu#1>=3`
  - **Output_Var**: `bchbaucrg_s`
  - **TAX_UNIT**: `tu_bch00`
  - **Who_Must_Be_Elig**: `all`
  - **#_AgeMax**: `0`
  - **#_AgeMin**: `0`

### 51. Function: BenCalc *(Switch: n/a)*
  - **Comp_perTU**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Who_Must_Be_Elig**: `n/a`
  - **#_AgeMax**: `n/a`
  - **#_AgeMin**: `n/a`

### 52. Function: BenCalc *(Switch: n/a)*
  - **Comp_perTU**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Who_Must_Be_Elig**: `n/a`

### 53. Function: BenCalc *(Switch: n/a)*
  - **Comp_perTU**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Who_Must_Be_Elig**: `n/a`
  - **#_AgeMax**: `n/a`
  - **#_AgeMin**: `n/a`

### 54. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `il_bch00 < $IPREM & IsParentOfDepChild & nDepChInTu#1 >= 2`
  - **comp_perTU**: `($bchrg_reg61_amt2 + ($bchrg_reg61_amt2 * (nDepChInTu#1 - 2)))*1.2`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `bchbamtrg_s`
  - **TAX_UNIT**: `tu_bch00`
  - **Comp_Cond**: `$IPREM*4<=il_bch00  & il_bch00< $IPREM *6  & IsParentOfDepChild & nDepChInTu#1 >= 2`
  - **Comp_perTU**: `($bchrg_reg61_amt2 + ($bchrg_reg61_amt2 * (nDepChInTu#1 - 2)))*0.5`

### 55. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `17`
  - **output_add_var**: `bchlgmtrg_s`
  - **TAX_UNIT**: `tu_largefam`
  - **Comp_Cond**: `sin32_s <= sin31_s & IsParentOfDepChild & dlg_s = 1 & nDepChildrenInTu#1=7`
  - **Comp_perTU**: `$bchrg_reg42_amt5* nDepChInTu#1`

### 56. Function: BenCalc *(Switch: off)*
  - **who_must_be_elig**: `all`
  - **comp_cond**: `IsParentOfDepChild & nDepChInTu#1 = 2 & sin32_s > 39838#y & sin32_s <= 55773.9#y`
  - **comp_perTU**: `2448#y`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `bchbamtrg_s`
  - **TAX_UNIT**: `tu_bch00`

### 57. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `nDepChInTu#1>1 & sin32_s <= sin31_s`
  - **Comp_perTU**: `$bchrg_reg13_amt4*nDepChInTu#1`
  - **Output_Add_Var**: `bchmtrg_s`
  - **TAX_UNIT**: `tu_bch00`
  - **Who_Must_Be_Elig**: `all`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`

### 58. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 59. Function: DefConst
  **Constants Defined:**
  - `$bchrg_reg61_amt1`: 600#y
  - `$bchrg_reg61_amt2`: 1200#y

### 60. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `il_bch00 < $IPREM & IsParentOfDepChild & nDepChInTu >= 3 & nDepChInTu#1 >= 2 & nDepChildrenInTu#3 >= 1`
  - **comp_perTU**: `$bchrg_reg61_amt1 * 1.2 * nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_add_var**: `bchbamtrg_s`
  - **TAX_UNIT**: `tu_bch00`
  - **Comp_Cond**: `$IPREM*4 <= il_bch00  & il_bch00 < $IPREM*6 & IsParentOfDepChild & nDepChInTu >= 3 & nDepChInTu#1 >= 2 & nDepChildrenInTu#3 >= 1`
  - **Comp_perElig**: `$bchrg_reg61_amt1 * 1.1 * nDepChInTu#1`
  - **Comp_perTU**: `$bchrg_reg61_amt1 * 0.5 * nDepChInTu#1`

### 61. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$bchrg_reg12_amt1`: n/a
  - `$bchrg_reg12_lim1`: n/a

### 62. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$bchrg_reg70_amt1`: n/a

### 63. Function: BenCalc
  - **Comp_perTU**: `$bchrg_reg13_amt7`
  - **Comp_Cond**: `nDepChInTu#1>2 & sin32_s <= sin31_s`
  - **Output_Var**: `bchmtrg_s`
  - **TAX_UNIT**: `tu_bch00`
  - **Who_Must_Be_Elig**: `all`
  - **#_AgeMax**: `0`
  - **#_AgeMin**: `0`

### 64. Function: ArithOp
  **Formula:** `$bchrg_reg11_lim2`
  **Output Variable:** `sin31_s`
  **Tax Unit:** `tu_bch00`

### 65. Function: BenCalc
  - **Who_Must_Be_Elig**: `all`
  - **Comp_Cond**: `sin32_s <= sin31_s & IsParentOfDepChild & nDepChInTu >= 3`
  - **Comp_perTU**: `$bchrg_reg11_amt3*nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **Output_Add_Var**: `bchmtrg_s`
  - **TAX_UNIT**: `tu_bch00`

### 66. Function: BenCalc
  - **Who_Must_Be_Elig**: `all`
  - **Comp_Cond**: `IsParentOfDepChild & nDepChInTu#1>=6`
  - **Comp_perTU**: `bchbaucrg_s + 0.65 *bchbaucrg_s`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **Output_Var**: `bchbaucrg_s`
  - **TAX_UNIT**: `tu_bch00`

### 67. Function: DefVar
  - **i_eq**: `0`

### 68. Function: DefTu
  - **Name**: `tu_bchrg21`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild & loosedepchild`
  - **DepChildCond**: `default & (dag < 25) & il_bch00#1<=$SMI`
  - **#_level**: `tu_individual_es`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`
  - **LoneParentCond**: `Default`

### 69. Function: BenCalc
  - **Who_Must_Be_Elig**: `all`
  - **Comp_Cond**: `IsHeadOfTu`
  - **Comp_perTU**: `1 + 0.3*IsLoneParentOfDepChild + 0.5*IsWithPartner+0.3*nDepChildrenInTu#1 + 0.3*IsDisabled`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `25`
  - **Output_Add_Var**: `i_eq`
  - **TAX_UNIT**: `tu_bchrg21`

### 70. Function: BenCalc
  - **Who_Must_Be_Elig**: `all`
  - **Comp_Cond**: `tintp_s=22`
  - **Comp_perTU**: `$bchrg_reg30_lim2`
  - **Output_Var**: `sin31_s`
  - **TAX_UNIT**: `tu_bch00`

### 71. Function: BenCalc
  - **Comp_Cond**: `tintb_s <= sin31_s & IsParentOfDepChild & dag<=30 &  nDepChInTu#1>=1`
  - **Comp_perTU**: `$bchrg_reg30_amt1*nDepChInTu#1`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `1`
  - **Output_Add_Var**: `bchbamtrg_s`
  - **TAX_UNIT**: `tu_bch00`
  - **Who_Must_Be_Elig**: `all`

### 72. Function: DefConst
  **Constants Defined:**
  - `$bchrg_reg24_basic_amt`: 1200#y
  - `$bchrg_reg24_lim1`: 4570#y
  - `$bchrg_reg24_lim2`: 6280#y
  - `$bchrg_reg24_lim3`: 7425#y
  - `$bchrg_reg24_lim4`: 9140#y
  - `$bchrg_reg24_lim5`: 10280#y
  - `$bchrg_reg24_lim6`: 11400#y

### 73. Function: DefConst
  **Constants Defined:**
  - `$bchrg_reg13_amt1`: 400#y
  - `$bchrg_reg13_amt2`: 600#y
  - `$bchrg_reg13_amt3`: 900#y
  - `$bchrg_reg13_amt4`: 1000#y
  - `$bchrg_reg13_amt5`: 1500#y
  - `$bchrg_reg13_amt6`: 2000#y
  - `$bchrg_reg13_amt7`: 3000#y
  - `$bchrg_reg13_lim1`: 18001#y
  - `$bchrg_reg13_lim2`: 30000#y
  - `$bchrg_reg13_lim3`: 42000#y

### 74. Function: DefConst
  **Constants Defined:**
  - `$bchrg_reg42_amt1`: 41.22#m
  - `$bchrg_reg42_amt2`: 54.96#m
  - `$bchrg_reg42_amt3`: 68.70#m
  - `$bchrg_reg42_amt4`: 82.44#m
  - `$bchrg_reg42_amt5`: 96.18#m
  - `$bchrg_reg42_amt6`: 109.92#m
  - `$bchrg_reg42_amt7
`: 123.66#m
  - `$bchrg_reg42_amt8`: 137.40#m

### 75. Function: DefConst
  **Constants Defined:**
  - `$bchrg_reg51_amt1`: 650#y
  - `$bchrg_reg51_amt2`: 750#y
  - `$bchrg_reg51_amt3`: 2448#y
  - `$bchrg_reg51_amt4`: 3264#y
  - `$bchrg_reg51_lim1`: 16000#y
  - `$bchrg_reg51_lim2`: 39838.5#y
  - `$bchrg_reg51_lim3`: 55773.9#y

### 76. Function: DefConst
  **Constants Defined:**
  - `$bchrg_reg11_amt1`: 600#y
  - `$bchrg_reg11_amt2`: 1200#y
  - `$bchrg_reg11_amt3`: 2400#y
  - `$bchrg_reg11_lim1`: 22000#y
  - `$bchrg_reg11_lim2`: 45000#y

### 77. Function: DefConst
  **Constants Defined:**
  - `$bchrg_reg30_amt1`: 6000#y
  - `$bchrg_reg30_lim1`: 30000#y
  - `$bchrg_reg30_lim2`: 36200#y

### 78. Function: DefConst
  **Constants Defined:**
  - `$bchrg_reg21_amt1`: 1200#y
  - `$bchrg_reg21_amt2`: 2400#y
  - `$bchrg_reg21_amt3`: n/a
  - `$bchrg_reg21_amt4`: 2000#y
  - `$bchrg_reg21_lim1`: 20000#y
  - `$bchrg_reg21_lim2`: 30000#y

### 79. Function: BenCalc
  - **Who_Must_Be_Elig**: `all`
  - **Comp_Cond**: `IsParentOfDepChild & nDepChInTu#3>=3`
  - **Comp_perTU**: `$bchrg_reg21_amt1*nDepChInTu#2`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `25`
  - **Output_Add_Var**: `bchucrg_s`
  - **TAX_UNIT**: `tu_bchrg21`


---

## Policy: bsarg_es
### 1. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 2. Function: DefIl *(Switch: n/a)*
  - **name**: `n/a`
  - **ils_origy**: `n/a`
  - **ils_pen**: `n/a`
  - **bhl**: `n/a`
  - **bunnc_s**: `n/a`
  - **bunct_s**: `n/a`
  - **bed**: `n/a`
  - **poacm_s**: `n/a`
  - **psuwdcm_s**: `n/a`
  - **bma**: `n/a`
  - **ils_sicee**: `n/a`
  - **ils_sicse**: `n/a`
  - **bmact_s**: `n/a`
  - **bpact_s**: `n/a`
  - **bmanc_s**: `n/a`

### 3. Function: DefTu *(Switch: n/a)*
  - **Name**: `n/a`
  - **Type**: `n/a`
  - **Members**: `n/a`
  - **DepChildCond**: `n/a`
  - **DepParentCond**: `n/a`
  - **AssignDepChOfDependents**: `n/a`
  - **AssignPartnerOfDependents**: `n/a`
  - **LoneParentCond**: `n/a`

### 4. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 5. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **uplim**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 6. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 7. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 8. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 9. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 10. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 11. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 12. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 13. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 14. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 15. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 16. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 17. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 18. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 19. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`

### 20. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 21. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **comp_perElig**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 22. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 23. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 24. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 25. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 26. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 27. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 28. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 29. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 30. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 31. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 32. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 33. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 34. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 35. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 36. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 37. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 38. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 39. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 40. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 41. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 42. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 43. Function: DefTu
  - **Name**: `tu_bsarg`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & DepParent & DepChild`
  - **DepChildCond**: `(default)`
  - **DepParentCond**: `(default)`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`
  - **LoneParentCond**: `(Default)`

### 44. Function: DefVar
  - **i_bsarg_potential**: `0`
  - **i_bsarg_11**: `0`
  - **i_bsarg_12**: `0`
  - **i_bsarg_13**: `0`
  - **i_bsarg_21**: `0`
  - **i_bsarg_22**: `0`
  - **i_bsarg_23**: `0`
  - **i_bsarg_24**: `0`
  - **i_bsarg_30**: `0`
  - **i_bsarg_41**: `0`
  - **i_bsarg_42**: `0`
  - **i_bsarg_43**: `0`
  - **i_bsarg_51**: `0`
  - **i_bsarg_52**: `0`
  - **i_bsarg_53**: `0`
  - **i_bsarg_61**: `0`
  - **i_bsarg_62**: `0`
  - **i_bsarg_63**: `0`
  - **i_bsarg_64**: `0`
  - **i_bsarg_70**: `0`
  - **i_gmi_11**: `0`
  - **i_gmi_12**: `0`
  - **i_gmi_13**: `0`
  - **i_gmi_21**: `0`
  - **i_gmi_22**: `0`
  - **i_gmi_23**: `0`
  - **i_gmi_24**: `0`
  - **i_gmi_30**: `0`
  - **i_gmi_41**: `0`
  - **i_gmi_42**: `0`
  - **i_gmi_43**: `0`
  - **i_gmi_51**: `0`
  - **i_gmi_52**: `0`
  - **i_gmi_53**: `0`
  - **i_gmi_61**: `0`
  - **i_gmi_62**: `0`
  - **i_gmi_63**: `0`
  - **i_gmi_64**: `0`
  - **i_gmi_70**: `0`
  - **i_gmi**: `0`
  - **i_red_24**: `0`
  - **i_test_21**: `0`
  - **i_test_ded_21**: `0`
  - **i_test_42**: `0`
  - **i_test_ded_42**: `0`
  - **i_wth_61**: `0`
  - **i_il_bsa_global**: `0`

### 45. Function: DefIl
  - **Name**: `il_bsarg_global`
  - **bsa00_s**: `+`
  - **i_il_bsa_global**: `+`

### 46. Function: DefIl
  - **Name**: `il_bsarg_11`
  - **il_bsarg_global**: `+`
  - **bch00_s**: `-`
  - **bchbamtna_s**: `-`
  - **bchdi_s**: `-`
  - **bchucrg_s**: `-`
  - **bed**: `-`

### 47. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 11) & ((dag > 25) | ((dag>18) & ((ddi>0) | (IsParentOfDepChild#1)))) & (dag < 66) & ((poanc_s=0) & (pdinc=0))`
  - **Tax Unit:** `tu_individual_es`

### 48. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit >= 4)`
  - **comp_perTU**: `$IPREM*0.75`
  - **comp_perTu**: `$IPREM*0.75 + $IPREM*0.14 + $IPREM*0.12 + $IPREM*0.10*(nPersInUnit-3)`
  - **output_add_var**: `i_gmi_11`
  - **TAX_UNIT**: `tu_bsarg`

### 49. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_gmi_11>=$IPREM*1.20) & (nPersInUnit = nAdultsInTu)`
  - **Comp_perTU**: `$IPREM*1.20 - i_gmi_11`
  - **Output_Add_Var**: `i_gmi_11`
  - **TAX_UNIT**: `tu_bsarg`

### 50. Function: ArithOp
  **Formula:** `i_gmi_11 - max(il_bsarg_11, 0)`
  **Output Variable:** `i_bsarg_11`
  **Tax Unit:** `tu_bsarg`

### 51. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_bsarg_11 > 0) & (i_bsarg_11 < $IPREM*0.25)`
  - **Comp_perTU**: `$IPREM*0.25 - i_bsarg_11`
  - **Output_Add_Var**: `i_bsarg_11`
  - **TAX_UNIT**: `tu_bsarg`

### 52. Function: ArithOp
  **Formula:** `i_bsarg_11*(12/12)`
  **Output Variable:** `i_bsarg_11`
  **Tax Unit:** `tu_bsarg`

### 53. Function: DefIl
  - **Name**: `il_bsarg_12`
  - **il_bsarg_global**: `+`
  - **tin_s**: `-`
  - **bch00_s**: `-`
  - **bchbamtna_s**: `-`
  - **bchmtrg_s**: `-`
  - **bchbamtrg_s**: `-`
  - **bchbaucna02_s**: `-`
  - **bchucrg_s**: `-`
  - **bchbaucrg_s**: `-`
  - **bchdi_s**: `-`

### 54. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 12) & ((dag > 25) | ((dag>18) & ((ddi>0) | (IsWithPartner) | (IsParentOfDepChild#1))))`
  - **Tax Unit:** `tu_individual_es`

### 55. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit >= 6)`
  - **comp_perTU**: `$bsarg_rg12_amt1`
  - **comp_perTu**: `$bsarg_rg12_amt6`
  - **Output_Var**: `i_gmi_12`
  - **TAX_UNIT**: `tu_bsarg`

### 56. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(ddi = 1)`
  - **comp_perTU**: `0.05*i_gmi_12`
  - **output_add_var**: `i_gmi_12`
  - **TAX_UNIT**: `tu_bsarg`

### 57. Function: ArithOp
  **Formula:** `i_gmi_12`
  **Output Variable:** `i_gmi_12`
  **Tax Unit:** `tu_bsarg`

### 58. Function: ArithOp
  **Formula:** `i_gmi_12 - max(il_bsarg_12, 0)`
  **Output Variable:** `i_bsarg_12`
  **Tax Unit:** `tu_bsarg`

### 59. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_bsarg_12>0) & (i_bsarg_12<0.10*$bsarg_rg12_amt1)`
  - **Comp_perTU**: `0.10*$bsarg_rg12_amt1- i_bsarg_12`
  - **Output_Add_Var**: `i_bsarg_12`
  - **TAX_UNIT**: `tu_bsarg`

### 60. Function: ArithOp
  **Formula:** `i_bsarg_12*(12/12)`
  **Output Variable:** `i_bsarg_12`
  **Tax Unit:** `tu_bsarg`

### 61. Function: DefIl
  - **Name**: `il_bsarg_13`
  - **il_bsarg_global**: `+`
  - **bch00_s**: `-`
  - **bchbamtna_s**: `-`
  - **bchmtrg_s**: `-`
  - **bchbamtrg_s**: `-`
  - **bchbaucna02_s**: `-`
  - **bchucrg_s**: `-`
  - **bchbaucrg_s**: `-`
  - **bchdi_s**: `-`
  - **bed**: `-`
  - **bho**: `-`

### 62. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 13) & (((dag > 23) & (dag < 65)) | (IsParentOfDepChild#1))`
  - **Tax Unit:** `tu_individual_es`

### 63. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit >= 3)`
  - **comp_perTU**: `$IPREM * 0.80`
  - **comp_perTu**: `$IPREM * (0.80 + 0.25 + 0.10*(nPersInUnit-2))`
  - **Output_Var**: `i_gmi_13`
  - **UpLim**: `$IPREM * 1.25`
  - **TAX_UNIT**: `tu_bsarg`

### 64. Function: ArithOp
  **Formula:** `i_gmi_13-max(il_bsarg_13,0)`
  **Output Variable:** `i_bsarg_13`
  **Tax Unit:** `tu_bsarg`

### 65. Function: BenCalc
  - **Comp_Cond**: `(i_bsarg_13 < $IPREM * 0.01)`
  - **Comp_perTU**: `- i_bsarg_13`
  - **Output_Add_Var**: `i_bsarg_13`
  - **TAX_UNIT**: `tu_bsarg`

### 66. Function: DefIl
  - **Name**: `il_bsarg_21`
  - **il_bsarg_global**: `+`
  - **bch00_s**: `-`
  - **bchbamtna_s**: `-`
  - **bchdi_s**: `-`
  - **bchucrg_s**: `-`
  - **bed**: `-`
  - **bho**: `-`
  - **tin_s**: `-`

### 67. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 21) & (dag >= 18) `
  - **Tax Unit:** `tu_individual_es`

### 68. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **comp_perTu**: `n/a`
  - **UpLim**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 69. Function: ArithOp
  **Formula:** `i_gmi_21-max(il_bsarg_21,0)`
  **Output Variable:** `i_bsarg_21`
  **Tax Unit:** `tu_bsargpv`

### 70. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 71. Function: DefIl
  - **Name**: `il_bsarg_22`
  - **il_bsarg_global**: `+`
  - **bch00_s**: `-`
  - **bchbamtna_s**: `-`
  - **bchmtrg_s**: `-`
  - **bchbamtrg_s**: `-`
  - **bchbaucna02_s**: `-`
  - **bchucrg_s**: `-`
  - **bchbaucrg_s**: `-`
  - **bchdi_s**: `-`
  - **bed**: `-`
  - **bho**: `-`

### 72. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 22) & ((dag > 24) | ((dag > 18)  & (!(IsDepChild#1) | (IsParentOfDepChild#1))))`
  - **Tax Unit:** `tu_individual_es`

### 73. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit >= 4)`
  - **comp_perTU**: `$bsarg_rg22_basic_amt`
  - **comp_perTu**: `$bsarg_rg22_basic_amt * (1 + 0.35 + 0.25 + 0.15*(nPersInUnit-3))`
  - **Output_Var**: `i_gmi_22`
  - **TAX_UNIT**: `tu_bsarg`

### 74. Function: ArithOp
  **Formula:** `i_gmi_22-max(il_bsarg_22,0)`
  **Output Variable:** `i_bsarg_22`
  **Tax Unit:** `tu_bsarg`

### 75. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_bsarg_22>$bsarg_rg22_basic_amt*2)`
  - **Comp_perTU**: `$bsarg_rg22_basic_amt*2 - i_bsarg_22`
  - **Output_Add_Var**: `i_bsarg_22`
  - **TAX_UNIT**: `tu_bsarg`

### 76. Function: BenCalc
  - **Comp_Cond**: `(afc > 12 * $bsarg_rg22_basic_amt * 0.65) | (i_apr > 12 * $bsarg_rg22_basic_amt *10)`
  - **Comp_perTU**: `-i_bsarg_22`
  - **Output_Add_Var**: `i_bsarg_22`
  - **TAX_UNIT**: `tu_bsarg`

### 77. Function: DefIl
  - **Name**: `il_bsarg_23`
  - **il_bsarg_global**: `+`
  - **bch00_s**: `-`
  - **bchbamtna_s**: `-`
  - **bchmtrg_s**: `-`
  - **bchbamtrg_s**: `-`
  - **bchbaucna02_s**: `-`
  - **bchucrg_s**: `-`
  - **bchbaucrg_s**: `-`
  - **bchdi_s**: `-`
  - **bed**: `-`
  - **bho**: `-`
  - **tin_s**: `-`

### 78. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 23) & ((dag > 25) | ((dag > 16) & IsParent)) & (poa00 + poanc_s + poacm_s = 0) & (pdi < $IPREM*0.8) & (psuwd00 < $IPREM*0.8) & (bunct_s < $IPREM*0.8) & (bunnc_s < $IPREM*0.8) & (yse < $IPREM*0.8) & (ypr = 0) & (yse = 0)`
  - **Tax Unit:** `tu_individual_es`

### 79. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit = 1)`
  - **comp_perTU**: `$IPREM * 0.80`
  - **Comp_Cond**: `(nPersInUnit > 3)`
  - **Comp_perTU**: `$IPREM * (0.80 + 0.20 + 0.15 + 0.10*(nPersInUnit-3))`
  - **UpLim**: `$IPREM * 1.25`
  - **output_add_var**: `i_gmi_23`
  - **TAX_UNIT**: `tu_bsarg`

### 80. Function: BenCalc
  - **Comp_Cond**: `(afc + i_apr > 12 * i_gmi_23  * 4) | (afc > 12 * $IPREM * 2.30)`
  - **Comp_perTU**: `-i_bsarg_23`
  - **Output_Add_Var**: `i_bsarg_23`
  - **TAX_UNIT**: `tu_bsarg`

### 81. Function: ArithOp
  **Formula:** `i_gmi_23-max(il_bsarg_23,0)`
  **Output Variable:** `i_bsarg_23`
  **Tax Unit:** `tu_bsarg`

### 82. Function: DefIl
  - **Name**: `il_bsarg_24`
  - **il_bsarg_global**: `+`
  - **bed**: `-`

### 83. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 24) & ((dag >= 23 & dag < 65) | (dag >= 18 & IsParent))`
  - **Tax Unit:** `tu_individual_es`

### 84. Function: BenCalc
  - **Comp_Cond**: `(dag < 25) | (dag > 65)`
  - **Comp_perTU**: `il_bsarg_24 * 0.75`
  - **Output_Var**: `i_red_24`
  - **TAX_UNIT**: `tu_individual_es`

### 85. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit = 4)`
  - **comp_perTU**: `$bsarg_rg24_basic_amt`
  - **comp_perTu**: `$bsarg_rg24_basic_amt * (1 + 0.3 + 0.3*2)`
  - **output_add_var**: `i_gmi_24`
  - **TAX_UNIT**: `tu_bsarg`
  - **Comp_Cond**: `(nPersInUnit > 4)`
  - **Comp_perTU**: `$bsarg_rg24_basic_amt * (1 + 0.3*4)`
  - **#_AgeMin**: `18`

### 86. Function: ArithOp
  **Formula:** `i_gmi_24 - (il_bsarg_24 )`
  **Output Variable:** `i_bsarg_24`
  **Tax Unit:** `tu_bsarg`

### 87. Function: DefIl
  - **Name**: `il_bsarg_30`
  - **il_bsarg_global**: `+`
  - **bch00_s**: `-`
  - **bchdi_s**: `-`
  - **bchmtrg_s**: `-`
  - **bchucrg_s**: `-`
  - **bed**: `-`
  - **bho**: `-`
  - **tin_s**: `-`

### 88. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 30) & (((dag > 25) & (dag < 65)) | (((dag<=25) | (dag>=65)) & (IsParentOfDepChild#1)) | ((dag>=65) & (nPersInUnit#1=1)))`
  - **Tax Unit:** `tu_individual_es`

### 89. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit >= 3)`
  - **comp_perTU**: `$bsarg_rg30_basic_amt`
  - **comp_perTu**: `$bsarg_rg30_basic_amt+$bsarg_rg30_extra_amt2 + ($bsarg_rg30_extra_amt3*(nPersInUnit-2))`
  - **UpLim**: `$bsarg_rg30_up_lim`
  - **output_add_var**: `i_gmi_30`
  - **TAX_UNIT**: `tu_bsarg`

### 90. Function: ArithOp
  **Formula:** `i_gmi_30-max(il_bsarg_30,0)`
  **Output Variable:** `i_bsarg_30`
  **Tax Unit:** `tu_bsarg`

### 91. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(afc + i_apr >= 12 * i_gmi_30 * 3)`
  - **Comp_perTU**: `-i_bsarg_30`
  - **Output_Add_Var**: `i_bsarg_30`
  - **TAX_UNIT**: `tu_bsarg`

### 92. Function: DefIl
  - **Name**: `il_bsarg_41`
  - **il_bsarg_global**: `+`
  - **bch00_s**: `-`
  - **bchbamtna_s**: `-`
  - **bchmtrg_s**: `-`
  - **bchbamtrg_s**: `-`
  - **bchbaucna02_s**: `-`
  - **bchucrg_s**: `-`
  - **bchbaucrg_s**: `-`
  - **bchdi_s**: `-`
  - **bed**: `-`

### 93. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 41) & (((dag > 25) & (dag < 65)) | (IsParent) | ((dag >= 65) & (ils_pen=0)))`
  - **Tax Unit:** `tu_individual_es`

### 94. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit >= 4)`
  - **comp_perTU**: `$IPREM * 0.80`
  - **comp_perTu**: `$IPREM * (0.80 + 0.25 + 0.10* (nPersInUnit - 3))`
  - **Output_Var**: `i_gmi_41`
  - **TAX_UNIT**: `tu_bsarg`

### 95. Function: ArithOp
  **Formula:** `i_gmi_41 -max(il_bsarg_41,0)`
  **Output Variable:** `i_bsarg_41`
  **Tax Unit:** `tu_bsarg`

### 96. Function: BenCalc
  - **Comp_Cond**: `(drgn2 = 42)  & ((amrtn = 1) | (amrtn = 3) | (amrtn = 4) | (amrtn = 5))`
  - **Comp_perTU**: `0.35*$IPREM`
  - **Output_Add_Var**: `i_test_ded_42`
  - **TAX_UNIT**: `tu_bsarg`

### 97. Function: DefIl
  - **Name**: `il_bsarg_42`
  - **il_bsarg_global**: `+`
  - **i_test_ded_42**: `-`
  - **bch00_s**: `-`
  - **bchdi_s**: `-`
  - **bchmtrg_s**: `-`
  - **bchucrg_s**: `-`
  - **bchbamtna_s**: `-`
  - **bchbaucna02_s**: `-`
  - **bchbamtrg_s**: `-`
  - **bchlgmtrg_s**: `-`
  - **bchbaucrg_s**: `-`
  - **bchlgucrg_s**: `-`
  - **bed**: `-`

### 98. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 42) & (((dag > 24) & (dag <65)) | ((dag>18) & (IsParentOfDepChild#1)))`
  - **Tax Unit:** `tu_individual_es`

### 99. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `i_gmi_42`
  - **TAX_UNIT**: `tu_bsarg`

### 100. Function: ArithOp
  **Formula:** `i_gmi_42-max(il_bsarg_42,0)`
  **Output Variable:** `i_bsarg_42`
  **Tax Unit:** `tu_bsarg`

### 101. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_bsarg_42>0) & (i_bsarg_42<50#m)`
  - **Comp_perTU**: `50#m - i_bsarg_42`
  - **Output_Add_Var**: `i_bsarg_42`
  - **TAX_UNIT**: `tu_bsarg`

### 102. Function: ArithOp
  **Formula:** `i_bsarg_42*(12/12)`
  **Output Variable:** `i_bsarg_42`
  **Tax Unit:** `tu_bsarg`

### 103. Function: DefIl
  - **Name**: `il_bsarg_43`
  - **ils_sicee**: `n/a`
  - **il_bsarg_global**: `+`
  - **bch00_s**: `-`
  - **bchbamtna_s**: `-`
  - **bchmtrg_s**: `-`
  - **bchbamtrg_s**: `-`
  - **bchbaucna02_s**: `-`
  - **bchucrg_s**: `-`
  - **bchbaucrg_s**: `-`
  - **bchdi_s**: `-`
  - **bed**: `-`

### 104. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 43) & ((dag > 25) | ((dag > 18) & (IsParent)))`
  - **Tax Unit:** `tu_individual_es`

### 105. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `$IPREM`
  - **comp_perTu**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **output_add_var**: `i_gmi_43`
  - **TAX_UNIT**: `tu_bsarg`

### 106. Function: ArithOp
  **Formula:** `i_gmi_43 - max(il_bsarg_43,0)`
  **Output Variable:** `i_bsarg_43`
  **Tax Unit:** `tu_bsarg`

### 107. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_bsarg_43 > 0) & (i_bsarg_43 < $IPREM * 0.10)`
  - **Comp_perTU**: `$IPREM * 0.10 - i_bsarg_43`
  - **Output_Add_Var**: `i_bsarg_43`
  - **TAX_UNIT**: `tu_bsarg`

### 108. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 109. Function: DefIl
  - **Name**: `il_bsarg_51`
  - **il_bsarg_global**: `+`

### 110. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 51) & ((dag > 23) | ((dag>18) & (IsParentOfDepChild#1)))`
  - **Tax Unit:** `tu_individual_es`

### 111. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit = 3)`
  - **comp_perTU**: `$IRSC`
  - **comp_perTu**: `$IRSC * 1.65`
  - **UpLim**: `$IRSC * 1.82`
  - **output_add_var**: `i_gmi_51`
  - **TAX_UNIT**: `tu_bsarg`
  - **Comp_Cond**: `(nPersInUnit >4)`
  - **Comp_perTU**: `$IRSC * 1.82`

### 112. Function: ArithOp
  **Formula:** `i_gmi_51 - max(il_bsarg_51,0)`
  **Output Variable:** `i_bsarg_51`
  **Tax Unit:** `tu_bsarg`

### 113. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_bsarg_51 > 0) & (i_bsarg_51 < $IRSC * 0.10)`
  - **Comp_perTU**: `$IRSC * 0.10 - i_bsarg_51`
  - **Output_Add_Var**: `i_bsarg_51`
  - **TAX_UNIT**: `tu_bsarg`

### 114. Function: DefIl
  - **Name**: `il_bsarg_52`
  - **il_bsarg_global**: `+`
  - **bch00_s**: `-`
  - **bchdi_s**: `-`
  - **bchmtrg_s**: `-`
  - **bed**: `-`
  - **bho**: `-`

### 115. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 52) & ((dag > 25) | ((dag>16) &  (IsParentOfDepChild#1))) & (bunct_s#1 + bunnc#1 = 0)`
  - **Tax Unit:** `tu_individual_es`

### 116. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(yem + yse > 0) & (nPersInUnit >= 6)`
  - **comp_perTU**: `$SMI * 0.70`
  - **comp_perTu**: `$SMI * 1.1`
  - **Output_Var**: `i_gmi_52`
  - **TAX_UNIT**: `tu_bsarg`

### 117. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(yem + yse = 0) & (ils_ben > 0) & (nPersInUnit >= 6)`
  - **comp_perTU**: `$SMI2 * 0.70`
  - **comp_perTu**: `$SMI2 * 1.10`
  - **Output_Add_Var**: `i_gmi_52`
  - **TAX_UNIT**: `tu_bsarg`

### 118. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **Comp_Cond**: `(yem + yse + ils_ben = 0) & (nPersInUnit >= 6)`
  - **Comp_perTU**: `$SMI2 * 1.10`
  - **Output_Add_Var**: `i_gmi_52`
  - **TAX_UNIT**: `tu_bsarg`

### 119. Function: ArithOp
  **Formula:** `i_gmi_52 - max(il_bsarg_52,0)`
  **Output Variable:** `i_bsarg_52`
  **Tax Unit:** `tu_bsarg`

### 120. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(afc + i_apr > 12 * i_gmi_52 * 7)`
  - **Comp_perTU**: `-i_bsarg_52`
  - **Output_Add_Var**: `i_bsarg_52`
  - **TAX_UNIT**: `tu_bsarg`

### 121. Function: DefIl
  - **Name**: `il_bsarg_53`
  - **il_bsarg_global**: `+`
  - **bch00_s**: `-`
  - **bchdi_s**: `-`
  - **bchmtrg_s**: `-`
  - **bchucrg_s**: `-`
  - **bed**: `-`
  - **bho**: `-`

### 122. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 53) & ((dag > 25) | ((dag>18) & (IsParentOfDepChild#1))) & bsa00_s=0`
  - **Tax Unit:** `tu_individual_es`

### 123. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit = 4)`
  - **comp_perTU**: `$bsarg_rg53_amt1`
  - **comp_perTu**: `$bsarg_rg53_amt4`
  - **UpLim**: `$bsarg_rg53_uplim`
  - **output_add_var**: `i_gmi_53`
  - **TAX_UNIT**: `tu_bsarg`
  - **Comp_Cond**: `(nPersInUnit >= 5)`
  - **Comp_perTU**: `$bsarg_rg53_uplim`

### 124. Function: ArithOp
  **Formula:** `i_gmi_53-max(il_bsarg_53,0)`
  **Output Variable:** `i_bsarg_53`
  **Tax Unit:** `tu_bsarg`

### 125. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_bsarg_53>0) & (i_bsarg_53<0.25*$bsarg_rg53_amt1)`
  - **Comp_perTU**: `0.25*$bsarg_rg53_amt1- i_bsarg_53`
  - **Output_Add_Var**: `i_bsarg_53`
  - **TAX_UNIT**: `tu_bsarg`

### 126. Function: ArithOp
  **Formula:** `0.011*(i_apr/12)`
  **Output Variable:** `i_wth_61`
  **Tax Unit:** `tu_individual_es`

### 127. Function: DefIl
  - **Name**: `il_bsarg_61`
  - **il_bsarg_global**: `+`
  - **ypt**: `-`
  - **bch00_s**: `-`
  - **bchdi_s**: `-`
  - **bchmtrg_s**: `-`
  - **bchucrg_s**: `-`
  - **bho**: `-`
  - **bed**: `-`
  - **psuot**: `-`
  - **i_wth_61**: `+`

### 128. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 61) & (((dag > 24) & (dag < 65)) | ((dag>17) & (dag<25) & ((IsParentOfDepChild) | (IsDisabled))))`
  - **Tax Unit:** `tu_bsarg`

### 129. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(sel_s = 1) | ((sel_s=0) & (drgn2 = 61) & (dag > 64) & (IsParentOfDepChild))`
  - **Tax Unit:** `tu_bsarg`

### 130. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit > 1)`
  - **comp_perTU**: `$poanc_amt / 12`
  - **comp_perTu**: `($poanc_amt / 12) + (($poanc_amt / 12) * ((nPersInUnit - 1) * 0.3))`
  - **Comp_Cond**: `(ddi>0)`
  - **Comp_perTU**: `($poanc_amt / 12)*0.22`
  - **Output_Var**: `i_gmi_61`
  - **TAX_UNIT**: `tu_bsarg`

### 131. Function: ArithOp
  **Formula:** `i_gmi_61 - max(il_bsarg_61,0)`
  **Output Variable:** `i_bsarg_61`
  **Tax Unit:** `tu_bsarg`

### 132. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_bsarg_61 > (($poanc_amt / 12) * 0.24)) & (drgn2 = 61)`
  - **Comp_perTU**: `i_bsarg_61`
  - **Output_Var**: `i_bsarg_61`
  - **TAX_UNIT**: `tu_bsarg`

### 133. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `i_bsarg_61`
  - **TAX_UNIT**: `tu_bsarg`

### 134. Function: ArithOp
  **Formula:** `i_bsarg_61*(12/12)`
  **Output Variable:** `i_bsarg_61`
  **Tax Unit:** `tu_bsarg`

### 135. Function: DefIl
  - **Name**: `il_bsarg_62`
  - **il_bsarg_global**: `+`
  - **bch00_s**: `-`
  - **bchdi_s**: `-`
  - **bchmtrg_s**: `-`
  - **bed**: `-`
  - **tin_s**: `-`

### 136. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 62) & (((dag > 25) & (dag < 65)) | (IsParent) | ((dag >= 65) & (ils_pen=0)))`
  - **Tax Unit:** `tu_individual_es`

### 137. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit >= 5)`
  - **comp_perTU**: `$IPREM * 0.80`
  - **comp_perTu**: `$IPREM * (0.80 + 0.20 + 0.10*2 + 0.08*(nPersInUnit - 4))`
  - **UpLim**: `$IPREM * 1.50`
  - **Output_Var**: `i_gmi_62`
  - **TAX_UNIT**: `tu_bsarg`

### 138. Function: ArithOp
  **Formula:** `i_gmi_62 - max(il_bsarg_62,0)`
  **Output Variable:** `i_bsarg_62`
  **Tax Unit:** `tu_bsarg`

### 139. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(afc + i_apr > 12 * $IPREM * 4) | (afc > i_bsarg_62 * 6)`
  - **Comp_perTU**: `-i_bsarg_62`
  - **Output_Add_Var**: `i_bsarg_62`
  - **TAX_UNIT**: `tu_bsarg`

### 140. Function: DefIl
  - **Name**: `il_bsarg_63`
  - **il_bsarg_global**: `+`
  - **ypt**: `-`
  - **bch00_s**: `-`
  - **bchdi_s**: `-`
  - **bchmtrg_s**: `-`
  - **bchucrg_s**: `-`
  - **bho**: `-`
  - **bed**: `-`

### 141. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 63) & ((dag > 25) & (dag< 65) | ((dag < 25) & (dag>65) & (IsParentOfDepChild)))`
  - **Tax Unit:** `tu_bsarg`

### 142. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit >= 2)`
  - **comp_perTU**: `$bsarg_rg63_basic_amt`
  - **comp_perTu**: `$bsarg_rg63_basic_amt+ $bsarg_rg63_basic_amt * (nPersInUnit - 1) * 0.10`
  - **UpLim**: `$bsarg_rg63_up_lim`
  - **Output_Var**: `i_gmi_63`
  - **TAX_UNIT**: `tu_bsarg`

### 143. Function: ArithOp
  **Formula:** `i_gmi_63-max(il_bsarg_63,0)`
  **Output Variable:** `i_bsarg_63`
  **Tax Unit:** `tu_bsarg`

### 144. Function: BenCalc
  - **Comp_Cond**: `((afc + i_apr) > 12 * i_gmi_63 * 3)`
  - **Comp_perTU**: `-i_bsarg_63`
  - **Output_Add_Var**: `i_bsarg_63`
  - **TAX_UNIT**: `tu_bsarg`

### 145. Function: DefIl
  - **Name**: `il_bsarg_64`
  - **il_bsarg_global**: `+`

### 146. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 64) & ((dag > 25) & (dag< 65) | (IsLoneParentOfDepChild#1) | ((dag>18 & ddi >0)) & ((il_bsarg_64<$poanc_amt) | ((il_bsarg_64<($poanc_amt*1.20)) & (nPersInUnit#1=2)) | ((nPersInUnit#1>=3) & (il_bsarg_64<(1.20*$poanc_amt + 0.15*(nPersInUnit#1 -2)*$poanc_amt)))))`
  - **Tax Unit:** `tu_individual_es`

### 147. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit >= 2)`
  - **comp_perTU**: `0.5*$bsarg_rg64_basic_amt`
  - **comp_perTu**: `(0.5*$bsarg_rg64_basic_amt) + ((0.5*$bsarg_rg64_basic_amt)*(nPersInUnit - 1) * 0.10)`
  - **UpLim**: `$bsarg_rg64_basic_amt`
  - **Output_Var**: `i_gmi_64`
  - **TAX_UNIT**: `tu_bsarg`

### 148. Function: ArithOp
  **Formula:** `i_gmi_64-max(il_bsarg_64,0)`
  **Output Variable:** `i_bsarg_64`
  **Tax Unit:** `tu_bsarg`

### 149. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `((afc + i_apr) >= 12 * i_gmi_64 *4)`
  - **Comp_perTU**: `-i_bsarg_64`
  - **Output_Add_Var**: `i_bsarg_64`
  - **TAX_UNIT**: `tu_bsarg`

### 150. Function: DefIl
  - **Name**: `il_bsarg_70`
  - **il_bsarg_global**: `+`
  - **bch00_s**: `-`
  - **bchdi_s**: `-`
  - **bchmtrg_s**: `-`
  - **bchucrg_s**: `-`
  - **bed**: `-`
  - **bho**: `-`
  - **pdi00**: `-`
  - **pdinc**: `-`
  - **pdicm**: `-`

### 151. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(drgn2 = 70) & (((dag > 25) & (dag < 65)) | ((dag<=25) & (IsParentOfDepChild#1)) | ((dag>=65) & (poa00 + poanc_s + poacm_s = 0)) | ((dag>=18) & (IsDisabled) & (pdi00 + pdicm + pdinc = 0)))`
  - **Tax Unit:** `tu_individual_es`

### 152. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(nPersInUnit = 4)`
  - **comp_perTU**: `$bsarg_rg70_amt1`
  - **comp_perTu**: `$bsarg_rg70_amt4`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **output_add_var**: `i_gmi_70`
  - **TAX_UNIT**: `tu_bsarg`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`

### 153. Function: ArithOp
  **Formula:** `i_gmi_70-max(il_bsarg_70,0)`
  **Output Variable:** `i_bsarg_70`
  **Tax Unit:** `tu_bsarg`

### 154. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 155. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(afc + i_apr >= 12 * i_gmi_70 * 3)`
  - **Comp_perTU**: `-i_bsarg_70`
  - **Output_Add_Var**: `i_bsarg_70`
  - **TAX_UNIT**: `tu_bsarg`

### 156. Function: ArithOp
  **Formula:** `i_gmi_11 + i_gmi_12 + i_gmi_13 + i_gmi_21 + i_gmi_22 + i_gmi_23 + i_gmi_24 + i_gmi_30 + i_gmi_41 + i_gmi_42 + i_gmi_43 + i_gmi_51 + i_gmi_52 + i_gmi_53 + i_gmi_61 + i_gmi_62 + i_gmi_63 + i_gmi_64 + i_gmi_70`
  **Output Variable:** `i_gmi`
  **Tax Unit:** `tu_individual_es`

### 157. Function: ArithOp
  **Formula:** `i_bsarg_11 + i_bsarg_12 + i_bsarg_13 + i_bsarg_21 + i_bsarg_22 + i_bsarg_23 + i_bsarg_24 + i_bsarg_30 + i_bsarg_41 + i_bsarg_42 + i_bsarg_43 + i_bsarg_51 + i_bsarg_52 + i_bsarg_53 + i_bsarg_61 + i_bsarg_62 + i_bsarg_63 + i_bsarg_64 + i_bsarg_70`
  **Output Variable:** `bsarg_s`
  **Tax Unit:** `tu_individual_es`

### 158. Function: ArithOp
  **Formula:** `bsarg_s + bsa00_s`
  **Output Variable:** `bsa_s`
  **Tax Unit:** `tu_individual_es`

### 159. Function: ArithOp
  **Formula:** `il_bsa_global`
  **Output Variable:** `i_il_bsa_global`
  **Tax Unit:** `tu_individual_es`

### 160. Function: DefTu
  - **Name**: `tu_bsargpv`
  - **Type**: `HH`
  - **DepChildCond**: `idmother>0 | idfather>0`
  - **DepParentCond**: `(default)`
  - **LoneParentCond**: `(default)`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`

### 161. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(nAdultsInTu#2+nDepChildrenInTu#1)>1
`
  - **#_AgeMin**: `18`
  - **Comp_perTU**: `((nPersInUnit-2)*0.3+0.5+0.5+1)*$bsarg_rg21_basic_amt`
  - **Output_Var**: `i_gmi_21`
  - **TAX_UNIT**: `tu_bsargpv`

### 162. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `((poa00>0) | (poanc_s>0) | (psuwd00>0))`
  - **Comp_perTU**: `$bsarg_rg21_basic_amt*0.40`
  - **Output_Add_Var**: `i_gmi_21`
  - **TAX_UNIT**: `tu_bsargpv`

### 163. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_11* 1000000/12

### 164. Function: DefVar *(Switch: off)*
  - **i_bsarg_11_bca_sort**: `i_bsarg_11_bca_rand`
  - **i_bsarg_11_2**: `i_bsarg_11`
  - **i_bsarg_11_2_cumexp**: `0`

### 165. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_11`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_11_bca_sort`
  - **OutputVar**: `i_bsarg_11_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 166. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_11_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_11`
  - **TAX_UNIT**: `tu_individual_es`

### 167. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_12* 1000000/12

### 168. Function: DefVar *(Switch: off)*
  - **i_bsarg_12_bca_sort**: `i_bsarg_12_bca_rand`
  - **i_bsarg_12_2**: `i_bsarg_12`
  - **i_bsarg_12_2_cumexp**: `0`

### 169. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_12`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_12_bca_sort`
  - **OutputVar**: `i_bsarg_12_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 170. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_12_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_12`
  - **TAX_UNIT**: `tu_individual_es`

### 171. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_13* 1000000/12

### 172. Function: DefVar *(Switch: off)*
  - **i_bsarg_13_bca_sort**: `i_bsarg_13_bca_rand`
  - **i_bsarg_13_2**: `i_bsarg_13`
  - **i_bsarg_13_2_cumexp**: `0`

### 173. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_13`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_13_bca_sort`
  - **OutputVar**: `i_bsarg_13_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 174. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_13_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_13`
  - **TAX_UNIT**: `tu_individual_es`

### 175. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_21* 1000000/12

### 176. Function: DefVar *(Switch: off)*
  - **i_bsarg_21_bca_sort**: `i_bsarg_21_bca_rand`
  - **i_bsarg_21_2**: `i_bsarg_21`
  - **i_bsarg_21_2_cumexp**: `0`

### 177. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_21`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_21_bca_sort`
  - **OutputVar**: `i_bsarg_21_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 178. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_21_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_21`
  - **TAX_UNIT**: `tu_individual_es`

### 179. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_22* 1000000/12

### 180. Function: DefVar *(Switch: off)*
  - **i_bsarg_22_bca_sort**: `i_bsarg_22_bca_rand`
  - **i_bsarg_22_2**: `i_bsarg_22`
  - **i_bsarg_22_2_cumexp**: `0`

### 181. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_22`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_22_bca_sort`
  - **OutputVar**: `i_bsarg_22_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 182. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_22_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_22`
  - **TAX_UNIT**: `tu_individual_es`

### 183. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_23* 1000000/12

### 184. Function: DefVar *(Switch: off)*
  - **i_bsarg_23_bca_sort**: `dwt`
  - **i_bsarg_23_2**: `i_bsarg_23`
  - **i_bsarg_23_2_cumexp**: `0`

### 185. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_23`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_23_bca_sort`
  - **OutputVar**: `i_bsarg_23_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 186. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_23`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_23`
  - **TAX_UNIT**: `tu_individual_es`

### 187. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_24* 1000000/12

### 188. Function: DefVar *(Switch: off)*
  - **i_bsarg_24_bca_sort**: `dwt`
  - **i_bsarg_24_2**: `i_bsarg_24`
  - **i_bsarg_24_2_cumexp**: `0`

### 189. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_24`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_24_bca_sort`
  - **OutputVar**: `i_bsarg_24_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 190. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_24`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_24`
  - **TAX_UNIT**: `tu_individual_es`

### 191. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_30* 1000000/12

### 192. Function: DefVar *(Switch: off)*
  - **i_bsarg_30_bca_sort**: `dwt`
  - **i_bsarg_30_2**: `i_bsarg_30`
  - **i_bsarg_30_2_cumexp**: `0`

### 193. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_30`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_30_bca_sort`
  - **OutputVar**: `i_bsarg_30_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 194. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_30_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_30`
  - **TAX_UNIT**: `tu_individual_es`

### 195. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_41* 1000000/12

### 196. Function: DefVar *(Switch: off)*
  - **i_bsarg_41_bca_sort**: `i_bsarg_41_bca_rand`
  - **i_bsarg_41_2**: `i_bsarg_41`
  - **i_bsarg_41_2_cumexp**: `0`

### 197. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_41`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_41_bca_sort`
  - **OutputVar**: `i_bsarg_41_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 198. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_41_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_41`
  - **TAX_UNIT**: `tu_individual_es`

### 199. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_42* 1000000/12

### 200. Function: DefVar *(Switch: off)*
  - **i_bsarg_42_bca_sort**: `dwt`
  - **i_bsarg_42_2**: `i_bsarg_42`
  - **i_bsarg_42_2_cumexp**: `0`

### 201. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_42`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_42_bca_sort`
  - **OutputVar**: `i_bsarg_42_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 202. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_42_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_42`
  - **TAX_UNIT**: `tu_individual_es`

### 203. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_43* 1000000/12

### 204. Function: DefVar *(Switch: off)*
  - **i_bsarg_43_bca_sort**: `i_bsarg_43_bca_rand`
  - **i_bsarg_43_2**: `i_bsarg_43`
  - **i_bsarg_43_2_cumexp**: `0`

### 205. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_43`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_43_bca_sort`
  - **OutputVar**: `i_bsarg_43_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 206. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_43_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_43`
  - **TAX_UNIT**: `tu_individual_es`

### 207. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_51* 1000000/12

### 208. Function: DefVar *(Switch: off)*
  - **i_bsarg_51_bca_sort**: `i_bsarg_51_bca_rand`
  - **i_bsarg_51_2**: `i_bsarg_51`
  - **i_bsarg_51_2_cumexp**: `0`

### 209. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_51`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_51_bca_sort`
  - **OutputVar**: `i_bsarg_51_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 210. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_51_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_51`
  - **TAX_UNIT**: `tu_individual_es`

### 211. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_52* 1000000/12

### 212. Function: DefVar *(Switch: off)*
  - **i_bsarg_52_bca_sort**: `i_bsarg_52_bca_rand`
  - **i_bsarg_52_2**: `i_bsarg_52`
  - **i_bsarg_52_2_cumexp**: `0`

### 213. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_52`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_52_bca_sort`
  - **OutputVar**: `i_bsarg_52_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 214. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_52_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_52`
  - **TAX_UNIT**: `tu_individual_es`

### 215. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_53* 1000000/12

### 216. Function: DefVar *(Switch: off)*
  - **i_bsarg_53_bca_sort**: `i_bsarg_53_bca_rand`
  - **i_bsarg_53_2**: `i_bsarg_53`
  - **i_bsarg_53_2_cumexp**: `0`

### 217. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_53`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_53_bca_sort`
  - **OutputVar**: `i_bsarg_53_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 218. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_53_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_53`
  - **TAX_UNIT**: `tu_individual_es`

### 219. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA
`: $extstat_amount_i_bsarg_61* 1000000/12

### 220. Function: DefVar *(Switch: off)*
  - **i_bsarg_61_bca_sort**: `i_bsarg_61_bca_rand`
  - **i_bsarg_61_2**: `i_bsarg_61`
  - **i_bsarg_61_2_cumexp**: `0`

### 221. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_61`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_61_bca_sort`
  - **OutputVar**: `i_bsarg_61_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 222. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_61_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_61`
  - **TAX_UNIT**: `tu_individual_es`

### 223. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_62* 1000000/12

### 224. Function: DefVar *(Switch: off)*
  - **i_bsarg_62_bca_sort**: `i_bsarg_62_bca_rand`
  - **i_bsarg_62_2**: `i_bsarg_62`
  - **i_bsarg_62_2_cumexp**: `0`

### 225. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_62`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_62_bca_sort`
  - **OutputVar**: `i_bsarg_62_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 226. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_62_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_62`
  - **TAX_UNIT**: `tu_individual_es`

### 227. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_63* 1000000/12

### 228. Function: DefVar *(Switch: off)*
  - **i_bsarg_63_bca_sort**: `i_bsarg_63_bca_rand`
  - **i_bsarg_63_2**: `i_bsarg_63`
  - **i_bsarg_63_2_cumexp**: `0`

### 229. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_63`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_63_bca_sort`
  - **OutputVar**: `i_bsarg_63_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 230. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_63_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_63`
  - **TAX_UNIT**: `tu_individual_es`

### 231. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_64* 1000000/12

### 232. Function: DefVar *(Switch: off)*
  - **i_bsarg_64_bca_sort**: `dwt`
  - **i_bsarg_64_2**: `i_bsarg_64`
  - **i_bsarg_64_2_cumexp**: `0`

### 233. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_64`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_64_bca_sort`
  - **OutputVar**: `i_bsarg_64_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 234. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_64_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_64`
  - **TAX_UNIT**: `tu_individual_es`

### 235. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$target_exp_BCA`: $extstat_amount_i_bsarg_70* 1000000/12

### 236. Function: DefVar *(Switch: off)*
  - **i_bsarg_70_bca_sort**: `dwt`
  - **i_bsarg_70_2**: `i_bsarg_70`
  - **i_bsarg_70_2_cumexp**: `0`

### 237. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsarg_70`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsarg_70_bca_sort`
  - **OutputVar**: `i_bsarg_70_2_cumexp`
  - **TAX_UNIT**: `tu_individual_es`

### 238. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_bsarg_70_2_cumexp > $target_exp_BCA`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_bsarg_70`
  - **TAX_UNIT**: `tu_individual_es`

### 239. Function: DefConst
  **Constants Defined:**
  - `$bsarg_rg12_amt1`: 501.67#m
  - `$bsarg_rg12_amt2`: 612.02#m
  - `$bsarg_rg12_amt3`: 692.29#m
  - `$bsarg_rg12_amt4`: 772.54#m
  - `$bsarg_rg12_amt5`: 807.67#m
  - `$bsarg_rg12_amt6`: 827.74#m
  - `$bsarg_rg21_basic_amt`: 568.85#m
  - `$bsarg_rg22_basic_amt`: 790.28#m
  - `$bsarg_rg24_basic_amt`: 700#y
  - `$bsarg_rg30_basic_amt`: 469.93 #m
  - `$bsarg_rg30_extra_amt2`: 117.48#m
  - `$bsarg_rg30_extra_amt3`: 75.11#m
  - `$bsarg_rg30_up_lim`: $SMI
  - `$bsarg_rg42_basic_amt`: 525#m
  - `$bsarg_rg42_add_amt`: n/a
  - `$bsarg_rg53_amt1`: 658.81#m
  - `$bsarg_rg53_amt2`: 856.46#m
  - `$bsarg_rg53_amt3`: 1199.04#m
  - `$bsarg_rg53_amt4`: 1251.75#m
  - `$bsarg_rg63_basic_amt`: 300#m
  - `$bsarg_rg63_up_lim`: 420#m
  - `$bsarg_rg64_basic_amt`: 656#m
  - `$bsarg_rg70_amt1`: 658.81#m
  - `$bsarg_rg70_amt2`: 856.46#m
  - `$bsarg_rg70_amt3`: 1054.10#m
  - `$bsarg_rg70_amt4`: 1251.75#m
  - `$bsarg_rg70_amt5`: 1449.39#m
  - `$bsarg_rg70_amt6`: 1449.39#m
  - `$bsarg_rg70_child_suppl`: n/a
  - `$bsarg_rg70_min_amt`: n/a
  - `$bsarg_rg51_extra_amt`: 100#m
  - `$bsarg_rg53_uplim`: 1449.39#m


---

## Policy: output_std_es
### 1. Function: DefOutput
  - **file**: `ES_2025_std`
  - **nDecimals**: `2`
  - **VarGroup**: `a*`
  - **ILGroup**: `il_*`
  - **TAX_UNIT**: `tu_individual_es`


---

## Policy: output_std_hh_es *(Switch: off)*
### 1. Function: DefOutput
  - **file**: `ES_2025_std_hh`
  - **var**: `dwt`
  - **ILGroup**: `ils*`
  - **nDecimals**: `2`
  - **TAX_UNIT**: `tu_household_es`


---

## Policy: bunct02_es *(Switch: off)*
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lnu > 0  & liwmy02_s >= $UBSE_QperMin & dag > 16 & dag < 65`
  - **Tax Unit:** `tu_individual_es`

### 2. Function: ArithOp
  **Formula:** `min(bunctmy02_s,lunmy_s)`
  **Output Variable:** `bunctmy02_s`
  **Tax Unit:** `tu_individual_es`

### 3. Function: BenCalc
  - **comp_cond**: `nDepChInTu > 0`
  - **comp_perTU**: `(1+1/6) * (1.07 * $IPREM)`
  - **output_var**: `i_bunctmin02`
  - **TAX_UNIT**: `tu_bunct`

### 4. Function: BenCalc
  - **comp_cond**: `nDepChInTu > 1`
  - **comp_perTU**: `(2.25 * $IPREM)`
  - **output_var**: `i_bunctmax02`
  - **TAX_UNIT**: `tu_bunct`

### 5. Function: ArithOp
  **Formula:** `i_bunct02 * bunctmy02_s / 12`
  **Output Variable:** `bunct02_s`
  **Tax Unit:** `tu_individual_es`

### 6. Function: DefVar
  - **i_liwwh02**: `0`
  - **i_bunctmax02**: `0`
  - **i_bunct02**: `0`
  - **i_ftprop02**: `0`
  - **i_bunctmin02**: `0`

### 7. Function: DefConst
  **Constants Defined:**
  - `$bunct02_minlim1`: 360
  - `$bunct02_my1`: 4
  - `$bunct02_minlim2`: 540
  - `$bunct02_my2`: 6
  - `$bunct02_minlim3`: 720
  - `$bunct02_my3`: 8
  - `$bunct02_minlim4`: 900
  - `$bunct02_my4`: 10
  - `$bunct02_minlim5`: 1080
  - `$bunct02_my5`: 12
  - `$bunct02_minlim6`: 1290
  - `$bunct02_my6`: 16
  - `$bunct02_minlim7`: 1440
  - `$bunct02_my7`: 24
  - `$bucnt02_rep_rate1`: 0.7
  - `$bunct02_my2b`: 6
  - `$bunct02_my3b`: 8
  - `$bunct02_my4b`: 10
  - `$bunct02_my5b`: 12
  - `$bunct02_my6b`: 16

### 8. Function: BenCalc
  - **Comp_Cond**: `i_liwwh02>=$bunct02_minlim7`
  - **Comp_perTU**: `$bunct02_my7`
  - **Output_Var**: `bunctmy02_s`
  - **TAX_UNIT**: `tu_individual_es`
  - **Who_Must_Be_Elig**: `one`

### 9. Function: BenCalc
  - **comp_cond**: `lnu > 0`
  - **comp_perElig**: `lunmy`
  - **output_var**: `lunmy02_s`
  - **TAX_UNIT**: `tu_individual_es`

### 10. Function: BenCalc
  - **uplim**: `$UBSE_QperTot`
  - **output_var**: `liwmy02_s`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_perElig**: `liwmy02_a`
  - **Comp_Cond**: `lnu>0`

### 11. Function: BenCalc
  - **Output_Var**: `i_liwwh02`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_Cond**: `lnu > 0`
  - **Comp_perTU**: `liwmy02_a * 30`
  - **Who_Must_Be_Elig**: `one`

### 12. Function: ArithOp
  **Formula:** `ysepv_a * $bucnt02_rep_rate1`
  **Output Variable:** `i_bunct02`
  **Tax Unit:** `tu_individual_es`


---

## Policy: setdefault_es
### 1. Function: SetDefault
  - **bchbamtrg_s**: `0`
  - **bchbaucna_s**: `0`
  - **bchbarg_s**: `0`
  - **bchbaucrg_s**: `0`
  - **bchlgmtrg_s**: `0`
  - **bchlgrg_s**: `0`
  - **bchlgucrg_s**: `0`
  - **bchmtrg_s**: `0`
  - **bchrg_s**: `0`
  - **bchucrg_s**: `0`
  - **bma**: `0`
  - **bunct_s**: `0`
  - **bunnc_s**: `0`
  - **bunmt_s**: `0`
  - **poaot**: `0`
  - **sin31_s**: `0`
  - **sin32_s**: `0`
  - **tintcbarg_s**: `0`
  - **tintcccrg_s**: `0`
  - **tintcchrg_s**: `0`
  - **tintcdbrg_s**: `0`
  - **tintcdprg_s**: `0`
  - **tintceerg_s**: `0`
  - **tintcfarg_s**: `0`
  - **tintchkrg_s**: `0`
  - **tintclgrg_s**: `0`
  - **tintclprg_s**: `0`
  - **tintcoarg_s**: `0`
  - **tintcrg_s**: `0`
  - **tintcrtrg_s**: `0`
  - **tintcwmrg_s**: `0`
  - **xcc**: `0`
  - **yemmy**: `12`
  - **bunctpc**: `0`
  - **bunot**: `0`
  - **xhcmo**: `0`
  - **dataset**: `ES_20??_a?`
  - **yem_a**: `0`
  - **kfbcc**: `0`
  - **ydses_o**: `0`
  - **lnu**: `0`
  - **lhw_a**: `0`
  - **lhwpv_a**: `0`
  - **liwmy02_a**: `0`
  - **bunotmy**: `0`
  - **bchbaucna02_s**: `0`
  - **poanc_s**: `0`
  - **bunct02_s**: `0`
  - **Dataset**: `ES_20??_??_????_??_??`
  - **bhlot**: `0`
  - **bhl00**: `bhl`
  - **pdinc**: `0`
  - **pdicm**: `0`
  - **pdi00**: `pdi`
  - **yptmp**: `0`
  - **liwmy_a**: `0`
  - **yempv_a**: `0`
  - **bmact_s**: `0`
  - **bpact_s**: `0`
  - **bmanc_s**: `0`
  - **lcb_a**: `0`
  - **dmb**: `2`
  - **ymwdt**: `0`
  - **ysepv_a**: `0`
  - **tintrchlp_s**: `0`
  - **tintrchlg_s**: `0`
  - **dsu01**: `0`
  - **yemmy19_a**: `0`
  - **yemmy18_a**: `0`
  - **lhwsr_a**: `0`
  - **bwkmcmy_a**: `0`
  - **lmc20**: `0`
  - **lhw20_a**: `0`
  - **lhw19_a**: `0`
  - **lhw18_a**: `0`
  - **lma20**: `0`
  - **lma19**: `0`
  - **lma18**: `0`
  - **lma**: `0`
  - **lmc**: `0`
  - **yemmy_a**: `0`
  - **yem20_a**: `0`
  - **yem19_a**: `0`
  - **yem18_a**: `0`
  - **yemmy20_a**: `0`
  - **pdiot**: `0`
  - **twl**: `tpr`
  - **xed00**: `0`
  - **xhl00**: `0`
  - **bwrls_s**: `0`
  - **sin51_s**: `0`
  - **sin52_s**: `0`
  - **kivho**: `0`
  - **tin**: `0`
  - **tscee**: `0`
  - **tscse**: `0`
  - **tpr**: `0`
  - **lfs**: `5`
  - **yprrt**: `ypr`
  - **tintrch**: `0`
  - **bunnc02_s**: `0`
  - **bunctmy00**: `0`

### 2. Function: SetDefault *(Switch: n/a)*
  - **Dataset**: `n/a`
  - **yemmc_s**: `n/a`
  - **lhwsr_s**: `n/a`
  - **bwkmceemy_s**: `n/a`
  - **yemmwmy_s**: `n/a`
  - **bwkmcee_s**: `n/a`
  - **lhwsesr_s**: `n/a`
  - **bwkmcsemy_s**: `n/a`
  - **ysemwmy_s**: `n/a`
  - **bwkmcse_s**: `n/a`

### 3. Function: ArithOp
  **Formula:** `bch00 + bchdi + bchot + bma + tintrch`
  **Output Variable:** `bfa`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `IsUsedDatabase#1 | IsUsedDatabase#2 | IsUsedDatabase#3 | IsUsedDatabase#4 | IsUsedDatabase#5`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `0`
  **Output Variable:** `tpr`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `!(IsUsedDatabase#1 | IsUsedDatabase#2)`

### 5. Function: SetDefault
  - **Dataset**: `es_20*`
  - **ydsyc_a**: `0`

### 6. Function: SetDefault
  - **Dataset**: `*`
  - **bsa00yn_a**: `-1`
  - **bwrlsyn_a**: `-1`

### 7. Function: DefIl
  - **Run_Cond**: `IsUsedDatabase#1`
  - **#_DataBasename**: `es_20??_??_????_??_??`
  - **Name**: `il_xs_hl06`
  - **Warn_If_NonMonetary**: `no`
  - **RegExp_Def**: `xs06[0-9]+`
  - **RegExp_Factor**: `+`

### 8. Function: ArithOp
  **Formula:** `il_xs_hl06 * yds`
  **Output Variable:** `xhl00`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `IsUsedDatabase#1`

### 9. Function: DefIl
  - **Run_Cond**: `IsUsedDatabase#1`
  - **#_DataBasename**: `es_20??_??_????_??_??`
  - **Name**: `il_xs_hl10`
  - **Warn_If_NonMonetary**: `no`
  - **RegExp_Def**: `xs10[0-9]+`
  - **RegExp_Factor**: `+`

### 10. Function: ArithOp
  **Formula:** `il_xs_hl10 * yds`
  **Output Variable:** `xed00`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `IsUsedDatabase#1`


---

## Policy: uprate_bands_es
### 1. Function: DefConst
  **Constants Defined:**
  - `$uprate_bands_2013A_index`: 1.02
  - `$uprate_bands_2013_lim`: 1000#m
  - `$uprate_bands_2010_index`: 1.023
  - `$uprate_bands_2012_index`: 1.01
  - `$uprate_bands_2013B_index`: 1.01
  - `$uprate_bands_2011_index`: 1
  - `$uprate_bands_2009_index`: 1.003
  - `$uprate_bands_2008_index`: 1.024
  - `$uprate_bands_2007_index`: 1.041
  - `$uprate_bands_2006_index`: 1.026
  - `$uprate_bands_2014_index`: 1.0025
  - `$uprate_bands_2015_index`: 1.0025
  - `$uprate_bands_2016_index`: 1.0025
  - `$uprate_bands_2017_index`: 1.0025
  - `$uprate_bands_2018_index`: 1.016
  - `$uprate_bands_2019_index`: 1.016
  - `$uprate_bands_2020_index`: 1.009
  - `$uprate_bands_2021_index`: 1.009
  - `$uprate_bands_2022_index`: 1.025
  - `$uprate_bands_2023_index`: 1.085
  - `$Index2024`: 1.038
  - `$Index2025`: 1.028

### 2. Function: DefVar
  - **i_pens**: `0`
  - **i_psuwd00**: `psuwd00`
  - **i_pdi00**: `pdi00`
  - **i_poa00**: `poa00`
  - **i_pdinc**: `pdinc`
  - **i_pdicm**: `pdicm`

### 3. Function: Loop
  - **Last_Func**: `1c2880f8-32a4-48c7-bb7c-b548af0fdc7c`
  - **First_Func**: `601fbec3-dce9-49a9-a7f9-44dbd078aab7`
  - **Loop_Id**: `pens`
  - **Num_Iterations**: `5`

### 4. Function: BenCalc
  - **Comp_Cond**: `loopcount_pens = 3`
  - **Comp_perTU**: `pdicm`
  - **Output_Var**: `i_pens`
  - **TAX_UNIT**: `tu_individual_es`

### 5. Function: ArithOp
  **Formula:** `i_pens`
  **Output Variable:** `poa00`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `loopcount_pens = 1`

### 6. Function: ArithOp
  **Formula:** `i_pens`
  **Output Variable:** `pdi00`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `loopcount_pens = 2`

### 7. Function: ArithOp
  **Formula:** `i_pens`
  **Output Variable:** `psuwd00`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `loopcount_pens = 5`

### 8. Function: ArithOp
  **Formula:** `poa00 + poacm + poanc+ poaot`
  **Output Variable:** `poa`
  **Tax Unit:** `tu_individual_es`

### 9. Function: ArithOp
  **Formula:** `psuwd00 + psuwdcm + psuot`
  **Output Variable:** `psu`
  **Tax Unit:** `tu_individual_es`

### 10. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2006_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2006 & GetDataIncomeYear <= 2005`

### 11. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2007_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2007 & GetDataIncomeYear <= 2006`

### 12. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2008_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2008 & GetDataIncomeYear <= 2007`

### 13. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2009_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2009 & GetDataIncomeYear <= 2008`

### 14. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2010_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2010 & GetDataIncomeYear <= 2009`

### 15. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2011_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2011 & GetDataIncomeYear <= 2010`

### 16. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2012_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2012 & GetDataIncomeYear <= 2011`

### 17. Function: BenCalc
  - **Comp_Cond**: `i_pens > $uprate_bands_2013_lim`
  - **Comp_perTU**: `i_pens * $uprate_bands_2013B_index`
  - **Output_Var**: `i_pens`
  - **TAX_UNIT**: `tu_individual_es`
  - **Run_Cond**: `GetSystemYear >= 2013 & GetDataIncomeYear <= 2012`

### 18. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2014_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2014 & GetDataIncomeYear <= 2013`

### 19. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2011_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2010 & GetDataIncomeYear >= 2011`

### 20. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2010_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2009 & GetDataIncomeYear >= 2010`

### 21. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2009_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2008 & GetDataIncomeYear >= 2009`

### 22. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2008_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2007 & GetDataIncomeYear >= 2008`

### 23. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2007_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2006 & GetDataIncomeYear >= 2007`

### 24. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2006_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2005 & GetDataIncomeYear >= 2006`

### 25. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2015_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2015 & GetDataIncomeYear <= 2014`

### 26. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2016_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2016 & GetDataIncomeYear <= 2015`

### 27. Function: ArithOp
  **Formula:** `pdi00 + pdicm + pdinc + pdiot`
  **Output Variable:** `pdi`
  **Tax Unit:** `tu_individual_es`

### 28. Function: BenCalc
  - **Comp_Cond**: `i_pens > $uprate_bands_2013_lim * $uprate_bands_2013A_index`
  - **Comp_perTU**: `i_pens / $uprate_bands_2013B_index`
  - **Output_Var**: `i_pens`
  - **TAX_UNIT**: `tu_individual_es`
  - **Run_Cond**: `GetSystemYear <= 2012 & GetDataIncomeYear >= 2013`

### 29. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2012_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2011 & GetDataIncomeYear >= 2012`

### 30. Function: ArithOp
  **Formula:** `i_pens`
  **Output Variable:** `pdicm`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `loopcount_pens = 3`

### 31. Function: ArithOp
  **Formula:** `i_pens`
  **Output Variable:** `pdinc`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `loopcount_pens = 4`

### 32. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2017_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2017 & GetDataIncomeYear <= 2016`

### 33. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2018_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2018 & GetDataIncomeYear <= 2017`

### 34. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2019_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2019 & GetDataIncomeYear <= 2018`

### 35. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2014_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2013 & GetDataIncomeYear >= 2014`

### 36. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2015_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2014 & GetDataIncomeYear >= 2015`

### 37. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2016_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2015 & GetDataIncomeYear >= 2016`

### 38. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2017_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2016 & GetDataIncomeYear >= 2017`

### 39. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2018_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2017 & GetDataIncomeYear >= 2018`

### 40. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2019_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2018 & GetDataIncomeYear >= 2019`

### 41. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2020_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2020 & GetDataIncomeYear <= 2019`

### 42. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2020_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2019 & GetDataIncomeYear >= 2020`

### 43. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2021_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2021 & GetDataIncomeYear <= 2020`

### 44. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2021_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2020 & GetDataIncomeYear >= 2021`

### 45. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2022_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2022 & GetDataIncomeYear <= 2021`

### 46. Function: ArithOp
  **Formula:** `i_pens * $uprate_bands_2023_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2023 & GetDataIncomeYear <= 2022`

### 47. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2023_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2022 & GetDataIncomeYear >= 2023`

### 48. Function: ArithOp
  **Formula:** `i_pens / $uprate_bands_2022_index`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2021 & GetDataIncomeYear >= 2022`

### 49. Function: ArithOp
  **Formula:** `i_pens * $Index2024`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2024 & GetDataIncomeYear <= 2023`

### 50. Function: ArithOp
  **Formula:** `i_pens / $Index2024`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2023 & GetDataIncomeYear >= 2024`

### 51. Function: ArithOp
  **Formula:** `i_pens * $Index2025`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear >= 2025 & GetDataIncomeYear <= 2024`

### 52. Function: ArithOp
  **Formula:** `i_pens / $Index2025`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_es`
  **Run Condition:** `GetSystemYear <= 2024 & GetDataIncomeYear >= 2025`


---

## Policy: bchbaucna02_es
### 1. Function: BenCalc
  - **comp_cond**: `nDepChInTu#1=2`
  - **comp_perTU**: `4*$SMI/12`
  - **#_AgeMin**: `0`
  - **#_AgeMax**: `0`
  - **output_var**: `bchbaucna02_s`
  - **TAX_UNIT**: `tu_bch00`
  - **Comp_perTU**: `12*$SMI/12`
  - **Comp_Cond**: `nDepChInTu#1>3`


---

## Policy: tintrchlg_es
### 1. Function: DefConst
  **Constants Defined:**
  - `$tintrchlg_ded_amt1`: 600#y
  - `$tintrchlg_ded_amt2`: 1200#y
  - `$tintrchlg_ded_amt3`: 2400#y

### 2. Function: DefTu
  - **Name**: `tu_tintrchlg`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `Default`

### 3. Function: BenCalc
  - **comp_cond**: `3<=nDepChOfCouple#1 & nDepChOfCouple#1<5 & idpartner!=0& il_sic > 0 & GetPartnerIncome#1>0`
  - **Comp_perTU**: `min($tintrchlg_ded_amt3,il_sic)`
  - **#_level**: `tu_tintrchlg`
  - **output_var**: `tintrchlg_s`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_Cond**: `(nDepChOfCouple#1 >=5 & idpartner!=0& il_sic > 0 & GetPartnerIncome#1=0)|(nDepChOfCouple#1 >=5 & idpartner=0 & il_sic > 0)`
  - **#_Income**: `il_sic`


---

## Policy: tintrchlp_es
### 1. Function: DefConst
  **Constants Defined:**
  - `$tintrchlp_ded_amt`: 1200#y

### 2. Function: BenCalc
  - **comp_cond**: `i_dpl=1 &nDepChildrenInTu#1>=2 & (il_sic > 0 & (yem>0 |  yse>0))`
  - **Comp_perTU**: `$tintrchlp_ded_amt`
  - **output_var**: `tintrchlp_s`
  - **TAX_UNIT**: `tu_individual_es`
  - **#_Level**: `tu_defvar`
  - **Comp_Cond**: `i_dpl=1 &nDepChildrenInTu#1>=2 & yem=0 &  yse=0 & (bunct_s>0 |bunnc_s>0 | poa00>0)`

### 3. Function: DefTu
  - **Name**: `tu_defvar`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `Default & dag<18`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`

### 4. Function: BenCalc
  - **Comp_Cond**: `IsParentOfDepChild#1 & idpartner<=0 &  !(IsMarried | isCohabiting)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_dpl`
  - **TAX_UNIT**: `tu_individual_es`
  - **#_Level**: `tu_defvar`

### 5. Function: DefVar
  - **i_dpl**: `0`


---

## Policy: ildef_es
### 1. Function: DefIl
  - **name**: `il_sic`
  - **ils_sicee**: `+`
  - **ils_sicer**: `+`
  - **ils_sicse**: `+`

### 2. Function: DefIl
  - **Name**: `il_tsctbeese`
  - **tsctbee_s**: `+`
  - **tsctbse_s**: `+`

### 3. Function: DefIl
  - **name**: `il_bch00`
  - **ils_origy**: `+`
  - **ils_pen**: `+`
  - **bhl**: `+`
  - **bunnc_s**: `+`
  - **bunct_s**: `+`
  - **bed**: `+`
  - **poacm_s**: `+`
  - **psuwdcm_s**: `+`
  - **bma**: `+`
  - **bmact_s**: `+`
  - **bpact_s**: `+`
  - **bmanc_s**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`

### 4. Function: DefIl
  - **Name**: `il_bsa_global`
  - **yem**: `+`
  - **yse**: `+`
  - **yiy**: `+`
  - **ypr**: `+`
  - **ypt**: `+`
  - **ypp**: `+`
  - **yot**: `+`
  - **xmp**: `-`
  - **pdi00**: `+`
  - **poa00**: `+`
  - **poaot**: `+`
  - **psuwd00**: `+`
  - **psuot**: `+`
  - **bch00_s**: `+`
  - **bchbamtna_s**: `+`
  - **bchmtrg_s**: `+`
  - **bchbamtrg_s**: `+`
  - **bchlgmtrg_s**: `+`
  - **bunnc_s**: `+`
  - **bunmt_s**: `+`
  - **bunot**: `+`
  - **pdicm**: `+`
  - **pdinc**: `+`
  - **poacm_s**: `+`
  - **poanc_s**: `+`
  - **psuwdcm_s**: `+`
  - **bed**: `+`
  - **bho**: `+`
  - **bhl**: `+`
  - **bma**: `+`
  - **bmact_s**: `+`
  - **bpact_s**: `+`
  - **bmanc_s**: `+`
  - **bchbaucna02_s**: `+`
  - **bchucrg_s**: `+`
  - **bchbaucrg_s**: `+`
  - **bchlgucrg_s**: `+`
  - **bchdi_s**: `+`
  - **bunct_s**: `+`
  - **bunct02_s**: `+`
  - **ysv**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **tsceepi_s**: `-`
  - **tsceeui_s**: `-`
  - **tsceeot_s**: `-`
  - **tscunee_s**: `-`
  - **tscsepi_s**: `-`
  - **tscsehl_s**: `-`
  - **tscseot_s**: `-`
  - **tscbeeepi_s**: `n/a`
  - **tscbeeeui_s**: `n/a`
  - **tscbeeeot_s**: `n/a`
  - **pdiot**: `+`
  - **tsceeie_s**: `-`
  - **tscseie_s**: `-`

### 5. Function: DefIl
  - **Name**: `il_bsawr`
  - **yem**: `+`
  - **yse**: `+`
  - **yiy**: `+`
  - **ypr**: `+`
  - **ypt**: `+`
  - **ypp**: `+`
  - **yot**: `+`
  - **xmp**: `-`
  - **pdi00**: `+`
  - **pdiot**: `+`
  - **poa00**: `+`
  - **poaot**: `+`
  - **psuwd00**: `+`
  - **psuot**: `+`
  - **bch00_s**: `+`
  - **bchbamtna_s**: `+`
  - **bchmtrg_s**: `+`
  - **bchbamtrg_s**: `+`
  - **bchlgmtrg_s**: `+`
  - **bunnc_s**: `+`
  - **bunmt_s**: `+`
  - **bunot**: `+`
  - **pdicm**: `+`
  - **pdinc**: `+`
  - **poacm_s**: `+`
  - **psuwdcm_s**: `+`
  - **bed**: `+`
  - **bho**: `+`
  - **bhl**: `+`
  - **bma**: `+`
  - **bmact_s**: `+`
  - **bpact_s**: `+`
  - **bmanc_s**: `+`
  - **bchbaucna02_s**: `+`
  - **bchucrg_s**: `+`
  - **bchbaucrg_s**: `+`
  - **bchlgucrg_s**: `+`
  - **bchdi_s**: `+`
  - **bunct_s**: `+`
  - **bunct02_s**: `+`
  - **ysv**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`


---

## Policy: ilsUDBDef_es
### 1. Function: DefIl
  - **Name**: `ils_udb_yem`
  - **yem**: `+`
  - **yemmc_s**: `n/a`

### 2. Function: DefIl
  - **Name**: `ils_udb_yse`
  - **yse**: `+`

### 3. Function: DefIl
  - **Name**: `ils_udb_ypp`
  - **ypp**: `+`

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
  - **yot**: `+`

### 8. Function: DefIl
  - **Name**: `ils_udb_xmp`
  - **xmp**: `+`

### 9. Function: DefIl
  - **Name**: `ils_udb_kfbcc`
  - **kfbcc**: `+`

### 10. Function: DefIl
  - **name**: `ils_udb_boa`
  - **poacm_s**: `+`
  - **poanc_s**: `+`
  - **poa00**: `+`
  - **poaot**: `+`

### 11. Function: DefIl
  - **name**: `ils_udb_bsu`
  - **psuwd00**: `+`
  - **psuwdcm_s**: `+`
  - **psuot**: `+`

### 12. Function: DefIl
  - **name**: `ils_udb_bdi`
  - **pdi00**: `+`
  - **pdinc**: `+`
  - **pdicm**: `+`
  - **pdiot**: `+`

### 13. Function: DefIl
  - **name**: `ils_udb_bun`
  - **bunot**: `+`
  - **bunmt_s**: `+`
  - **bunnc_s**: `+`
  - **bunct_s**: `+`
  - **bunct02_s**: `+`
  - **ysv**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`

### 14. Function: DefIl
  - **name**: `ils_udb_bhl`
  - **bhl**: `+`

### 15. Function: DefIl
  - **name**: `ils_udb_bed`
  - **bed**: `+`

### 16. Function: DefIl
  - **name**: `ils_udb_bsa`
  - **bsa_s**: `n/a`
  - **bsarg_s**: `+`
  - **bsa00_s**: `+`
  - **bwrls_s**: `+`

### 17. Function: DefIl
  - **name**: `ils_udb_bfa`
  - **bchbaucna_s**: `n/a`
  - **bma**: `+`
  - **bch00_s**: `+`
  - **bchdi_s**: `+`
  - **bchlgucrg_s**: `+`
  - **bchbaucrg_s**: `+`
  - **bchucrg_s**: `+`
  - **bchbamtna_s**: `+`
  - **bchbaucna02_s**: `+`
  - **bchlgmtrg_s**: `+`
  - **bchbamtrg_s**: `+`
  - **bchmtrg_s**: `+`
  - **tintrch_s**: `+`
  - **tintrchlp_s**: `+`
  - **tintrchlg_s**: `+`
  - **bmact_s**: `+`
  - **bpact_s**: `+`
  - **bmanc_s**: `+`

### 18. Function: DefIl
  - **name**: `ils_udb_bho`
  - **bho**: `+`

### 19. Function: DefIl
  - **Name**: `ils_udb_tpr`
  - **twl**: `+`

### 20. Function: DefIl
  - **Name**: `ils_udb_tis`
  - **tin_s**: `+`
  - **tsceeot_s**: `+`
  - **tsceeui_s**: `+`
  - **tsceepi_s**: `+`
  - **tscsehl_s**: `+`
  - **tscsepi_s**: `+`
  - **tscunee_s**: `+`
  - **tscseot_s**: `+`
  - **tscbeeepi_s**: `n/a`
  - **tscbeeeui_s**: `n/a`
  - **tscbeeeot_s**: `n/a`
  - **tsceeie_s**: `+`
  - **tscseie_s**: `+`
  - **tsceeas_s**: `+`

### 21. Function: DefIl
  - **Name**: `ils_udb_yds`
  - **ils_udb_tis**: `-`
  - **ils_udb_bho**: `+`
  - **ils_udb_bsa**: `+`
  - **ils_udb_bfa**: `+`
  - **ils_udb_bed**: `+`
  - **ils_udb_bdi**: `+`
  - **ils_udb_bhl**: `+`
  - **ils_udb_bsu**: `+`
  - **ils_udb_boa**: `+`
  - **ils_udb_bun**: `+`
  - **ils_udb_kfbcc**: `+`
  - **ils_udb_xmp**: `-`
  - **ils_udb_yot**: `+`
  - **ils_udb_ypt**: `+`
  - **ils_udb_yiy**: `+`
  - **ils_udb_ypr**: `+`
  - **ils_udb_ypp**: `+`
  - **ils_udb_yse**: `+`
  - **ils_udb_yem**: `+`
  - **ils_udb_tpr**: `-`


---

## Policy: bmact_es *(Switch: switch)*
### 1. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bmact=1 & yemmy >0`
  - **Comp_perTU**: `max((yivwg * $lhw * 52 / 12), (tsctbee_s))`
  - **Output_Var**: `i_yempv_bmact`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_UpLim**: `$tscft_ftbs_maxamt`

### 2. Function: DefTu
  - **Type**: `SUBGROUP`
  - **Name**: `tu_bma_es`
  - **Members**: `Partner & OwnDepChild & LooseDepChild`
  - **PartnerCond**: `Default`
  - **DepChildCond**: `Default & dag <1`
  - **ExtHeadCond**: `nDepChOfCouple > 0 & dgn = 0`
  - **StopIfNoHeadFound**: `no`
  - **LoneParentCond**: `Default & !IsMarried`

### 3. Function: DefVar
  - **i_elparent_bmact**: `0`
  - **Var_Monetary**: `no`
  - **i_elchild_bmact**: `0`
  - **i_ageweeks_bmact**: `0`
  - **i_nelchildren_bmact**: `0`
  - **i_durweeks_bmact**: `0`
  - **i_bmact**: `0`
  - **i_yempv_bmact**: `0`
  - **i_ysepv_bmact**: `0`
  - **i_ageweeks_bma**: `0`
  - **i_nelchildren_bma**: `0`
  - **i_elchild_bma**: `0`
  - **i_elparent_bma**: `0`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsHeadOfTu & IsParentOfDepChild`
  - **Tax Unit:** `tu_bma_es`

### 5. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bma=1 & dag<21 & (((ysemy + yemmy)/12) >0 | liwwh>0)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_elparent_bmact`
  - **TAX_UNIT**: `tu_individual_es`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsDepChild`
  - **Tax Unit:** `tu_bma_es`

### 7. Function: ArithOp
  **Formula:** `nDepChildrenInTu#1`
  **Output Variable:** `i_nelchildren_bma`
  **Tax Unit:** `tu_individual_es`

### 8. Function: BenCalc
  - **Comp_Cond**: `i_elchild_bma=1`
  - **Comp_perTU**: `(12-dmb)*(30.5/7)`
  - **Output_Var**: `i_ageweeks_bma`
  - **TAX_UNIT**: `tu_individual_es`

### 9. Function: BenCalc
  - **Comp_Cond**: `i_elchild_bma=1 & i_ageweeks_bma>=0 & i_nelchildren_bma#1>2`
  - **Comp_perTU**: `16+4`
  - **Output_Var**: `i_durweeks_bmact`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_UpLim**: `1+i_ageweeks_bma`
  - **Comp_LowLim**: `0`
  - **#_Level**: `tu_bma_es`

### 10. Function: BenCalc
  - **Comp_Cond**: `i_nelchildren_bma>0`
  - **Comp_perTU**: `i_durweeks_bmact/i_nelchildren_bma`
  - **Output_Var**: `i_durweeks_bmact`
  - **TAX_UNIT**: `tu_bma_es`

### 11. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bmact=1 & i_ysepv_bmact>0`
  - **Comp_perTU**: `(i_ysepv_bmact/30.5*7)*i_durweeks_bmact`
  - **Output_Var**: `i_bmact`
  - **TAX_UNIT**: `tu_individual_es`

### 12. Function: ArithOp
  **Formula:** `i_bmact/12`
  **Output Variable:** `bmact_s`
  **Tax Unit:** `tu_individual_es`

### 13. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bmact=1 & ysemy >0`
  - **Comp_perTU**: `max((yivwg * $lhw * 52 / 12), (tsctbse_s))`
  - **Output_Var**: `i_ysepv_bmact`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_UpLim**: `$tscft_ftbs_maxamt`

### 14. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bmact=1 & i_ysepv_bmact>0 & & i_nelchildren_bma#1>1`
  - **Comp_perTU**: `(i_ysepv_bmact/30.5)*6`
  - **#_Level**: `tu_bma_es`
  - **Output_Add_Var**: `i_bmact`
  - **TAX_UNIT**: `tu_individual_es`

### 15. Function: BenCalc
  - **Comp_Cond**: `bmact_s > 0`
  - **Comp_perTU**: `bma-bmact_s`
  - **LowLim**: `0`
  - **Output_Var**: `bma`
  - **TAX_UNIT**: `tu_household_es`


---

## Policy: bmanc_es *(Switch: switch)*
### 1. Function: DefVar
  - **i_elparent_bmanc**: `0`
  - **Var_Monetary**: `no`
  - **i_elchild_bmanc**: `0`
  - **i_ageweeks_bmanc**: `0`
  - **i_nelchildren_bmanc**: `0`
  - **i_durweeks_bmanc**: `0`
  - **i_bmanc**: `0`

### 2. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bma=1 & ((ysemy + yemmy)/12 >0 | liwwh>0) & bmact_s=0`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_elparent_bmanc`
  - **TAX_UNIT**: `tu_individual_es`

### 3. Function: BenCalc
  - **Comp_Cond**: `i_elchild_bma=1 & i_ageweeks_bma>=0 & i_nelchildren_bma#1>1`
  - **Comp_perTU**: `6+2`
  - **Output_Var**: `i_durweeks_bmanc`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_UpLim**: `1+i_ageweeks_bma`
  - **Comp_LowLim**: `0`
  - **#_Level**: `tu_bma_es`

### 4. Function: BenCalc
  - **Comp_Cond**: `i_nelchildren_bma>0`
  - **Comp_perTU**: `i_durweeks_bmanc/i_nelchildren_bma`
  - **Output_Var**: `i_durweeks_bmanc`
  - **TAX_UNIT**: `tu_bma_es`

### 5. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bmanc=1`
  - **Comp_perTU**: `($IPREM/30.5*7)*i_durweeks_bmanc`
  - **Output_Var**: `i_bmanc`
  - **TAX_UNIT**: `tu_individual_es`

### 6. Function: ArithOp
  **Formula:** `i_bmanc/12`
  **Output Variable:** `bmanc_s`
  **Tax Unit:** `tu_individual_es`

### 7. Function: BenCalc
  - **Comp_Cond**: `bmanc_s > 0`
  - **Comp_perTU**: `bma-bmanc_s`
  - **LowLim**: `0`
  - **Output_Var**: `bma`
  - **TAX_UNIT**: `tu_household_es`

### 8. Function: BenCalc
  - **#_Level**: `tu_large_es`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_Cond**: `i_elchild_bma=1 & i_ageweeks_bma>=0 & i_nelchildren_bma#1>0 & (IsHeadOfTu#1 & ddi>0)`
  - **Comp_perTU**: `2`
  - **UpLim**: `max(1+i_ageweeks_bma, 8)`
  - **Output_Add_Var**: `i_durweeks_bmanc`


---

## Policy: bpact_es *(Switch: switch)*
### 1. Function: DefVar
  - **i_elparent_bpact**: `0`
  - **Var_Monetary**: `no`
  - **i_bpact**: `0`
  - **i_yempv_bpact**: `0`
  - **i_ysepv_bpact**: `0`
  - **i_durweeks_bpact**: `0`

### 2. Function: DefTu
  - **Type**: `SUBGROUP`
  - **Name**: `tu_bpact_es`
  - **Members**: `Partner & OwnDepChild & LooseDepChild`
  - **PartnerCond**: `Default & dgn=1`
  - **DepChildCond**: `Default & dag <1`
  - **ExtHeadCond**: `nDepChOfCouple > 0 & dgn = 0`
  - **StopIfNoHeadFound**: `no`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsPartner & IsParentOfDepChild`
  - **Tax Unit:** `tu_bpact_es`

### 4. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bpact=1 & ((ysemy + yemmy)/12 >= 180/2555 | (liwwh*30.5)>360)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_elparent_bpact`
  - **TAX_UNIT**: `tu_individual_es`

### 5. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bpact=1 & yemmy >0`
  - **Comp_perTU**: `max((yivwg * $lhw * 52 / 12), (tsctbee_s))`
  - **Output_Var**: `i_yempv_bpact`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_UpLim**: `$tscft_ftbs_maxamt`

### 6. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bpact=1 & ysemy >0`
  - **Comp_perTU**: `max((yivwg * $lhw * 52 / 12), (tsctbse_s))`
  - **Output_Var**: `i_ysepv_bpact`
  - **TAX_UNIT**: `tu_individual_es`
  - **Comp_UpLim**: `$tscft_ftbs_maxamt`

### 7. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bpact=1 & i_ysepv_bpact>0`
  - **Comp_perTU**: `(i_ysepv_bpact/30.5*7)*i_durweeks_bpact`
  - **Output_Var**: `i_bpact`
  - **TAX_UNIT**: `tu_individual_es`

### 8. Function: ArithOp
  **Formula:** `i_bpact/12`
  **Output Variable:** `bpact_s`
  **Tax Unit:** `tu_individual_es`

### 9. Function: BenCalc
  - **Comp_Cond**: `bpact_s > 0`
  - **Comp_perTU**: `bma-bpact_s`
  - **LowLim**: `0`
  - **Output_Var**: `bma`
  - **TAX_UNIT**: `tu_household_es`

### 10. Function: BenCalc
  - **#_Level**: `tu_bma_es`
  - **Comp_Cond**: `i_elchild_bma=1 & i_ageweeks_bma>=0 & i_nelchildren_bma#1>2`
  - **Comp_perTU**: `16+2`
  - **Comp_LowLim**: `0`
  - **Comp_UpLim**: `i_ageweeks_bma`
  - **Output_Var**: `i_durweeks_bpact`
  - **TAX_UNIT**: `tu_individual_es`

### 11. Function: BenCalc
  - **Comp_Cond**: `i_nelchildren_bma>0`
  - **Comp_perTU**: `i_durweeks_bpact/i_nelchildren_bma`
  - **Output_Var**: `i_durweeks_bpact`
  - **TAX_UNIT**: `tu_bpact_es`

### 12. Function: Allocate
  - **Share_Between**: `i_nelchildren_bma>0 & IsPartner & IsParentOfDepChild`
  - **Share_All_IfNoElig**: `no`
  - **Share**: `i_durweeks_bpact`
  - **Output_Var**: `i_durweeks_bpact`
  - **TAX_UNIT**: `tu_bpact_es`


---

## Policy: random_es
### 1. Function: DefVar
  - **i_mc_rand_1**: `0`
  - **i_mc_rand_2**: `0`
  - **i_mc_rand_3**: `0`
  - **i_lmamy**: `0`
  - **i_lma2**: `0`
  - **i_lma1**: `0`
  - **i_bsa00_rand**: `0`
  - **i_bwrls_rand**: `n/a`
  - ** i_bsarg_11_bca_rand**: `0`
  - ** i_bsarg_12_bca_rand**: `0`
  - ** i_bsarg_13_bca_rand**: `0`
  - **i_bsarg_21_bca_rand**: `0`
  - **i_bsarg_22_bca_rand**: `0`
  - **i_bsarg_23_bca_rand**: `0`
  - **i_bsarg_24_bca_rand**: `0`
  - **i_bsarg_30_bca_rand**: `0`
  - **i_bsarg_41_bca_rand**: `0`
  - **i_bsarg_42_bca_rand**: `0`
  - **i_bsarg_43_bca_rand
**: `0`
  - **i_bsarg_51_bca_rand
**: `0`
  - **i_bsarg_52_bca_rand**: `0`
  - **i_bsarg_53_bca_rand**: `0`
  - **None**: `0`
  - **i_bsarg_61_bca_rand**: `0`
  - **i_bsarg_62_bca_rand**: `0`
  - **i_bsarg_63_bca_rand**: `0`
  - **i_bsarg_64_bca_rand**: `0`
  - **i_bsarg_70_bca_rand
**: `0`

### 2. Function: RandSeed
  - **Seed**: `19`

### 3. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_1`
  **Tax Unit:** `tu_individual_es`

### 4. Function: RandSeed
  - **Seed**: `20`

### 5. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_2`
  **Tax Unit:** `tu_individual_es`

### 6. Function: RandSeed
  - **Seed**: `21`

### 7. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_3`
  **Tax Unit:** `tu_individual_es`

### 8. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lmamy`
  **Tax Unit:** `tu_individual_es`

### 9. Function: RandSeed
  - **Seed**: `24`

### 10. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lma2`
  **Tax Unit:** `tu_individual_es`

### 11. Function: RandSeed
  - **Seed**: `23`

### 12. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lma1`
  **Tax Unit:** `tu_individual_es`

### 13. Function: RandSeed
  - **Seed**: `22`

### 14. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_bsa00_rand`
  **Tax Unit:** `tu_individual_es`

### 15. Function: RandSeed *(Switch: n/a)*
  - **Seed**: `n/a`

### 16. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 17. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 18. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_11_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 19. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 20. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_12_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 21. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 22. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_13_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 23. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 24. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_21_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 25. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 26. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_22_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 27. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 28. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_23_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 29. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 30. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_24_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 31. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 32. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_30_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 33. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 34. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_41_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 35. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 36. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_42_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 37. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 38. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_43_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 39. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 40. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_51_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 41. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 42. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_52_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 43. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 44. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_53_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 45. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 46. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_61_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 47. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 48. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_62_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 49. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 50. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_63_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 51. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 52. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_64_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 53. Function: RandSeed *(Switch: off)*
  - **Seed**: `202422100925`

### 54. Function: ArithOp *(Switch: off)*
  **Formula:** `rand`
  **Output Variable:** `i_bsarg_70_bca_rand`
  **Tax Unit:** `tu_individual_es`

### 55. Function: RandSeed
  - **Seed**: `202402291642`


---

## Policy: yemcomp_es *(Switch: off)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_yem_orig**: `n/a`
  - **i_bwkmcee_s**: `n/a`
  - **i_yemmc_s**: `n/a`
  - **i_diff**: `n/a`
  - **i_bwkmcee_min**: `n/a`
  - **i_bwkmcee_max**: `n/a`
  - **Var_Monetary**: `n/a`

### 2. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 3. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 4. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 5. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 6. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **LowLim**: `n/a`
  - **UpLim**: `n/a`
  - **#_Level**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

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


---

## Policy: ysecomp_es *(Switch: off)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_yse_orig**: `n/a`
  - **i_bwkmcse_s**: `n/a`
  - **i_ysemc_s**: `n/a`
  - **i_bwkmcse_min**: `n/a`
  - **i_bwkmcse_max**: `n/a`
  - **Var_Monetary**: `n/a`
  - **i_n_ben**: `n/a`

### 2. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 3. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 4. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 5. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 6. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **LowLim**: `n/a`
  - **UpLim**: `n/a`
  - **#_Level**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

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

### 10. Function: DefIl *(Switch: n/a)*
  - **Name**: `n/a`
  - **yse**: `n/a`
  - **tscse_s**: `n/a`

### 11. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **#_Level**: `n/a`
  - **Comp_perElig**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 12. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **#_Level**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: bsa00_es
### 1. Function: DefTu
  - **Name**: `tu_bsa00`
  - **Type**: `HH`
  - **DepChildCond**: `Default`

### 2. Function: DefVar
  - **i_gmi_00**: `0`
  - **i_wealth_00**: `0`
  - **i_bsa_00**: `0`
  - **bsaec00_s**: `n/a`

### 3. Function: DefIl
  - **Name**: `il_bsa00`
  - **il_bsa_global**: `+`
  - **bed**: `-`
  - **bho**: `-`
  - **bch00_s**: `-`
  - **bchdi_s**: `-`
  - **tin_s**: `-`
  - **tintrch_s**: `+`
  - **tintrchlg_s**: `+`
  - **tintrchlp_s**: `+`

### 4. Function: DefConst
  **Constants Defined:**
  - `$bsa00_amt`: 7905.72#y
  - `$bsa00_extraamt1`: 0.3
  - `$bsa00_extraamt2`: 0.22
  - `$bsa00_maxamt`: 2.20
  - `$bsa00_lim`: 7905.72#y*3
  - `$bsa00_extralim`: 0.4
  - `$bsa00_maxlim`: 2.6
  - `$bsa00_takeup_ratio`: 0.234
  - `$bsa00_2022refund_amt`: n/a

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(dag >= 23 & dag < 65) | (dag >= 18 & IsParent#1)`
  - **Tax Unit:** `tu_individual_es`

### 6. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(nPersInUnit>1) & (nAdultsInTu#1 = 1)`
  - **Comp_perTU**: `$bsa00_amt * $bsa00_extraamt2`
  - **UpLim**: `$bsa00_amt*$bsa00_maxamt`
  - **Output_Var**: `i_gmi_00`
  - **TAX_UNIT**: `tu_bsa00`
  - **#_AgeMin**: `18`

### 7. Function: ArithOp
  **Formula:** `i_gmi_00 - max(il_bsa00, 0)`
  **Output Variable:** `i_bsa_00`
  **Tax Unit:** `tu_bsa00`

### 8. Function: ArithOp
  **Formula:** `i_bsa_00*(12/12)`
  **Output Variable:** `i_bsa_00`
  **Tax Unit:** `tu_bsa00`

### 9. Function: BenCalc
  - **Comp_Cond**: `i_apr + afc > i_wealth_00`
  - **Comp_perTU**: `-i_bsa_00`
  - **Output_Add_Var**: `i_bsa_00`
  - **TAX_UNIT**: `tu_bsa00`

### 10. Function: BenCalc
  - **Comp_Cond**: `i_bsa_00 < 10#m`
  - **Comp_perTU**: `-i_bsa_00`
  - **Output_Add_Var**: `i_bsa_00`
  - **TAX_UNIT**: `tu_bsa00`

### 11. Function: ArithOp
  **Formula:** `i_bsa_00`
  **Output Variable:** `bsa00_s`
  **Tax Unit:** `tu_bsa00`

### 12. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 13. Function: BenCalc
  - **Comp_Cond**: `bsa00_s > 0`
  - **Comp_perTU**: `-bch00_s`
  - **Output_Add_Var**: `bch00_s`
  - **TAX_UNIT**: `tu_bch00`

### 14. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(nPersInUnit>1)`
  - **Comp_perTU**: `$bsa00_lim * $bsa00_extralim * (nPersInUnit - 1)`
  - **Output_Var**: `i_wealth_00`
  - **UpLim**: `$bsa00_lim * $bsa00_maxlim`
  - **TAX_UNIT**: `tu_bsa00`

### 15. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(il_bsa00 <(i_gmi_00*3)) & ((i_apr+afc) < (i_wealth_00*1.5))`
  - **Tax Unit:** `tu_bsa00`

### 16. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dag >= 6 & dag < 18`
  - **Comp_perElig**: `57.50`
  - **Output_Add_Var**: `i_bsa_00`
  - **TAX_UNIT**: `tu_bsa00`

### 17. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bsa00_s>0`
  - **Tax Unit:** `tu_bsa00`

### 18. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **UpLim**: `n/a`
  - **#_AgeMin**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 19. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 20. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa00_minamt`: 0

### 21. Function: DefVar *(Switch: off)*
  - **i_bsa00_sort**: `i_bsa00_rand`
  - **i_bsa00_amt**: `bsa00_s`
  - **i_bsa00_elig**: `bsa00_s > 0`
  - **i_bsa00_cumexp**: `0`
  - **i_bsa00_cumpers**: `0`

### 22. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `bsa00_s >= $bsa00_minamt`
  - **Comp_perTU**: `1`
  - **Comp_perElig**: `i_bsa00_sort`
  - **Output_Var**: `i_bsa00_sort`
  - **TAX_UNIT**: `tu_individual_es`

### 23. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa00_targetBCA_amt`: n/a

### 24. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `n/a`
  - **SummingWeighted**: `n/a`
  - **SortingVar**: `n/a`
  - **OutputVar**: `n/a`
  - **TAX_UNIT**: `n/a`

### 25. Function: DefVar *(Switch: off)*
  - **i_bsa00_bca_take**: `n/a`

### 26. Function: Totals *(Switch: off)*
  - **Agg**: `n/a`
  - **Use_Weights**: `n/a`
  - **Varname_Sum**: `n/a`
  - **TAX_UNIT**: `n/a`

### 27. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa00_BCA_rate`: 0.3380962

### 28. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa00_rate`: min($bsa00_BCA_rate,$bsa00_BTA_rate)

### 29. Function: Totals *(Switch: off)*
  - **Agg**: `i_bsa00_elig`
  - **Use_Weights**: `yes`
  - **Varname_Sum**: `$sum`
  - **TAX_UNIT**: `tu_individual_es`

### 30. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa00_target_count`: $sum_i_bsa00_elig * $bsa00_rate

### 31. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsa00_elig`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsa00_sort`
  - **OutputVar**: `i_bsa00_cumpers`
  - **TAX_UNIT**: `tu_individual_es`

### 32. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `(i_bsa00_cumpers > $bsa00_target_count & bsa00yn_a = -1)  | bsa00yn_a = 0`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bsa00_s`
  - **TAX_UNIT**: `tu_individual_es`

### 33. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa00_BTA_rate`: 0.45


---

## Policy: TransLMA_es *(Switch: off)*
### 1. Function: DefConst
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
  - `Run_Cond`: GetDataIncomeYear = 2019

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy = 0) & (ysemy = 0)& (dag > 17) & (dag < 65) & ((les=5) | lowas=1)`
  - **Tax Unit:** `tu_individual_es`

### 3. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(deh = 5) & (dgn = 1) & (i_lma1 < $ur_dgn1_deh3_ee)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_es`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy > 0) `
  - **Tax Unit:** `tu_individual_es`

### 5. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(deh = 5) & (dgn = 1) & (i_lma1 < $er_dgn1_deh3_ee)`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_es`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ysemy > 0) & (yemmy = 0)`
  - **Tax Unit:** `tu_individual_es`

### 7. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dgn = 1 & (i_lma2 < $er_dgn1_se)`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_es`

### 8. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lma =1)`
  - **Tax Unit:** `tu_individual_es`

### 9. Function: ArithOp
  **Formula:** `(yivwg*$lhw*52/12)`
  **Output Variable:** `yem_a`
  **Tax Unit:** `tu_individual_es`

### 10. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lma=1)|(lma=5)`
  - **Tax Unit:** `tu_individual_es`

### 11. Function: ArithOp
  **Formula:** `$lhw`
  **Output Variable:** `lhw_a`
  **Tax Unit:** `tu_individual_es`

### 12. Function: BenCalc
  - **Comp_Cond**: `(lma=2) & (ysemy > 0) & (yemmy = 0)`
  - **Comp_perTU**: `0`
  - **Output_Var**: `yemmy_a`
  - **TAX_UNIT**: `tu_individual_es`

### 13. Function: DefConst
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

### 14. Function: DefConst
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

### 15. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy >0)  & (lma=0)`
  - **Tax Unit:** `tu_individual_es`

### 16. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(lindi = 5) & (dgn = 1) & (i_mc_rand_1 < $sh_mcee_l4_dgn1)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lmcee_s`
  - **TAX_UNIT**: `tu_individual_es`

### 17. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lmcee_s = 1)`
  - **Tax Unit:** `tu_individual_es`

### 18. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_2> $sh_mceemy_9)`
  - **Comp_perTU**: `min (10, yemmy)`
  - **Output_Var**: `bwkmceemy_s`
  - **TAX_UNIT**: `tu_individual_es`

### 19. Function: ArithOp
  **Formula:** `yemmy - bwkmceemy_s`
  **Output Variable:** `yemmwmy_s`
  **Tax Unit:** `tu_individual_es`

### 20. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(bwkmceemy_s > 0)`
  - **Tax Unit:** `tu_individual_es`

### 21. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_3 >$sh_45hours_ee)`
  - **Comp_perTU**: `0.70`
  - **Output_Var**: `lhwsr_s`
  - **TAX_UNIT**: `tu_individual_es`

### 22. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ysemy > 0)  & (lma=0) & (lmcee_s = 0) & (yse>0)`
  - **Tax Unit:** `tu_individual_es`

### 23. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(lindi = 5) & (dgn = 1) & (i_mc_rand_1 < $sh_mcse_l4_dgn1)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lmcse_s`
  - **TAX_UNIT**: `tu_individual_es`

### 24. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lmcse_s = 1)`
  - **Tax Unit:** `tu_individual_es`

### 25. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_2> $sh_mcsemy_9)`
  - **Comp_perTU**: `min (10, ysemy)`
  - **Output_Var**: `bwkmcsemy_s`
  - **TAX_UNIT**: `tu_individual_es`

### 26. Function: ArithOp
  **Formula:** `ysemy - bwkmcsemy_s`
  **Output Variable:** `ysemwmy_s`
  **Tax Unit:** `tu_individual_es`

### 27. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(bwkmcsemy_s > 0)`
  - **Tax Unit:** `tu_individual_es`

### 28. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_3 >$sh_45hours_se)`
  - **Comp_perTU**: `0.70`
  - **Output_Add_Var**: `lhwsr_s`
  - **TAX_UNIT**: `tu_individual_es`

### 29. Function: DefConst
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

### 30. Function: DefConst
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

### 31. Function: DefConst
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

## Policy: pec00_es *(Switch: n/a)*
### 1. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$pec00_ncpen_amt`: n/a
  - `$pec00_child_amt`: n/a
  - `$pec00_pen_minamt1`: n/a
  - `$pec00_pen_minamt2`: n/a
  - `$pec00_pen_minamt3`: n/a
  - `$pec00_pen_minamt4`: n/a
  - `$pec00_pen_minamt5`: n/a
  - `$pec00_pen_minamt6`: n/a
  - `$pec00_wdpen_minamt1`: n/a
  - `$pec00_wdpen_minamt2`: n/a
  - `$pec00_wdpen_minamt3`: n/a
  - `$pec00_wdpen_minamt4`: n/a
  - `$pec00_wdpen_minamt5`: n/a
  - `$pec00_wdpen_minamt6`: n/a

### 2. Function: DefVar *(Switch: n/a)*
  - **i_poancec**: `n/a`

### 3. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 4. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **comp_perTu**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 5. Function: Allocate *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **share**: `n/a`
  - **share_between**: `n/a`
  - **share_equ_ifzero**: `n/a`
  - **share_all_ifnoelig**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 6. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **comp_perTu**: `n/a`
  - **lowlim**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 7. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 8. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 9. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 10. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 11. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 12. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **#_level**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 13. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`


---

## Policy: bwr_es *(Switch: n/a)*
### 1. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$bwr_amt`: n/a
  - `$bwr_inc_limit`: n/a
  - `$bwr_wlth_limit`: n/a

### 2. Function: DefVar *(Switch: n/a)*
  - **i_poancwr**: `n/a`
  - **i_bsawr**: `n/a`

### 3. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 4. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 5. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 6. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 7. Function: BenCalc *(Switch: n/a)*
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

### 10. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 11. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 12. Function: DefTu *(Switch: n/a)*
  - **Name**: `n/a`
  - **Type**: `n/a`
  - **Members**: `n/a`
  - **PartnerCond**: `n/a`
  - **DepChildCond**: `n/a`
  - **#_level**: `n/a`
  - **DepParentCond**: `n/a`

### 13. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 14. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `n/a`
  - **SummingWeighted**: `n/a`
  - **SortingVar**: `n/a`
  - **OutputVar**: `n/a`
  - **TAX_UNIT**: `n/a`

### 15. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bwrls_target_count`: n/a

### 16. Function: Totals *(Switch: off)*
  - **Agg**: `n/a`
  - **Use_Weights**: `n/a`
  - **Varname_Sum**: `n/a`
  - **TAX_UNIT**: `n/a`

### 17. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bwrls_rate`: n/a

### 18. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bwrls_BCA_rate`: n/a

### 19. Function: Totals *(Switch: off)*
  - **Agg**: `n/a`
  - **Use_Weights**: `n/a`
  - **Varname_Sum**: `n/a`
  - **TAX_UNIT**: `n/a`

### 20. Function: DefVar *(Switch: off)*
  - **i_bwrls_bca_take**: `n/a`

### 21. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `n/a`
  - **SummingWeighted**: `n/a`
  - **SortingVar**: `n/a`
  - **OutputVar**: `n/a`
  - **TAX_UNIT**: `n/a`

### 22. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bwrls_targetBCA_amt`: n/a

### 23. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Comp_perElig**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 24. Function: DefVar *(Switch: off)*
  - **i_bwrls_sort**: `n/a`
  - **i_bwrls_amt**: `n/a`
  - **i_bwrls_elig**: `n/a`
  - **i_bwrls_cumexp**: `n/a`
  - **i_bwrls_cumpers**: `n/a`

### 25. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bwrls_BTA_rate`: n/a
  - `$bwrls_BCA_rate`: n/a
  - `$bwrls_minamt`: n/a


---

## Policy: pec01_es *(Switch: n/a)*
### 1. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 2. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 3. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`


---

## Policy: tco_es *(Switch: off)*
### 1. Function: DefConst
  **Constants Defined:**
  - `$tco_t_std`: $tco_base_t_std
  - `$tco_t_red1`: $tco_base_t_red1
  - `$tco_t_red2`: $tco_base_t_red2
  - `$tco_t_red3`: $tco_base_t_red3
  - `$tco_t_zero`: $tco_base_t_zero

### 2. Function: DefConst
  **Constants Defined:**
  - `$tco_a_02111`: $tco_base_a_02111
  - `$tco_a_02121`: $tco_base_a_02121
  - `$tco_a_02122`: $tco_base_a_02122
  - `$tco_a_02131`: $tco_base_a_02131
  - `$tco_a_02211`: $tco_base_a_02211
  - `$tco_a_02212`: $tco_base_a_02212
  - `$tco_a_02213`: $tco_base_a_02213
  - `$tco_a_04511`: $tco_base_a_04511
  - `$tco_a_04521`: $tco_base_a_04521
  - `$tco_a_04522`: $tco_base_a_04522
  - `$tco_a_04531`: $tco_base_a_04531
  - `$tco_a_04541`: $tco_base_a_04541
  - `$tco_a_07221a`: $tco_base_a_07221a
  - `$tco_a_07221b`: $tco_base_a_07221b
  - `$tco_a_07221c`: $tco_base_a_07221c
  - `$tco_a_07221d`: $tco_base_a_07221d

### 3. Function: DefConst
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

### 4. Function: DefConst
  **Constants Defined:**
  - `$tco_a_07221`: ($tco_a_07221a +$tco_a_07221b +$tco_a_07221c +$tco_a_07221d)/4

### 5. Function: DefConst
  **Constants Defined:**
  - `$tco_base_a_07221`: ($tco_base_a_07221a +$tco_base_a_07221b +$tco_base_a_07221c +$tco_base_a_07221d)/4
  - `$tco_base_q_02111`: $tco_base_q_02111t / 40% * 100
  - `$tco_base_q_02121`: $tco_base_q_02121t * 100
  - `$tco_base_q_02122`: $tco_base_q_02122t * 100
  - `$tco_base_q_02131`: $tco_base_q_02131t * 100
  - `$tco_base_q_07221`: ($tco_base_q_07221b + $tco_base_q_07221c)/2

### 6. Function: DefIl
  - **Name**: `il_xs_exconly`
  - **Warn_If_NonMonetary**: `no`
  - **xs02111**: `+`
  - **xs02121**: `+`
  - **xs02122**: `+`
  - **xs02131**: `+`
  - **xs02211**: `+`
  - **xs02212**: `+`
  - **xs02213**: `+`
  - **xs04511**: `n/a`
  - **xs04521**: `+`
  - **xs04522**: `+`
  - **xs04531**: `+`
  - **xs04541**: `+`
  - **xs07221**: `+`

### 7. Function: DefIl
  - **Name**: `il_xs_rest`
  - **Warn_If_NonMonetary**: `no`
  - **xs01111**: `+`
  - **xs01112**: `+`
  - **xs01113**: `+`
  - **xs01114**: `+`
  - **xs01115**: `+`
  - **xs01116**: `+`
  - **xs01121**: `+`
  - **xs01122**: `+`
  - **xs01123**: `+`
  - **xs01124**: `+`
  - **xs01125**: `+`
  - **xs01126**: `+`
  - **xs01127**: `+`
  - **xs01131**: `+`
  - **xs01132**: `+`
  - **xs01133**: `+`
  - **xs01134**: `+`
  - **xs01141**: `+`
  - **xs01142**: `+`
  - **xs01143**: `+`
  - **xs01144**: `+`
  - **xs01145**: `+`
  - **xs01146**: `+`
  - **xs01147**: `+`
  - **xs01151**: `+`
  - **xs01152**: `+`
  - **xs01153**: `+`
  - **xs01154**: `+`
  - **xs01155**: `+`
  - **xs01161**: `+`
  - **xs01162**: `+`
  - **xs01163**: `+`
  - **xs01164**: `+`
  - **xs01165**: `+`
  - **xs01166**: `+`
  - **xs01167**: `+`
  - **xs01168**: `+`
  - **xs01169**: `+`
  - **xs01171**: `+`
  - **xs01172**: `+`
  - **xs01173**: `+`
  - **xs01174**: `+`
  - **xs01175**: `+`
  - **xs01176**: `+`
  - **xs01177**: `+`
  - **xs01178**: `+`
  - **xs01181**: `+`
  - **xs01182**: `+`
  - **xs01183**: `+`
  - **xs01184**: `+`
  - **xs01185**: `+`
  - **xs01186**: `+`
  - **xs01191**: `+`
  - **xs01192**: `+`
  - **xs01193**: `+`
  - **xs01194**: `+`
  - **xs01211**: `+`
  - **xs01212**: `+`
  - **xs01213**: `+`
  - **xs01221**: `+`
  - **xs01222**: `+`
  - **xs01223**: `+`
  - **xs01224**: `+`
  - **xs03111**: `+`
  - **xs03121**: `+`
  - **xs03122**: `+`
  - **xs03123**: `+`
  - **xs03131**: `+`
  - **xs03141**: `+`
  - **xs03211**: `+`
  - **xs03212**: `+`
  - **xs03213**: `+`
  - **xs03221**: `+`
  - **xs04111**: `+`
  - **xs04121**: `+`
  - **xs04311**: `+`
  - **xs04321**: `+`
  - **xs04411**: `+`
  - **xs04421**: `+`
  - **xs04431**: `+`
  - **xs04441**: `+`
  - **xs04551**: `+`
  - **xs05111**: `+`
  - **xs05121**: `+`
  - **xs05131**: `+`
  - **xs05211**: `+`
  - **xs05311**: `+`
  - **xs05312**: `+`
  - **xs05313**: `+`
  - **xs05314**: `+`
  - **xs05315**: `+`
  - **xs05316**: `+`
  - **xs05317**: `+`
  - **xs05321**: `+`
  - **xs05331**: `+`
  - **xs05411**: `+`
  - **xs05412**: `+`
  - **xs05413**: `+`
  - **xs05414**: `+`
  - **xs05511**: `+`
  - **xs05521**: `+`
  - **xs05611**: `+`
  - **xs05612**: `+`
  - **xs05621**: `+`
  - **xs05622**: `+`
  - **xs06111**: `+`
  - **xs06121**: `+`
  - **xs06131**: `+`
  - **xs06211**: `+`
  - **xs06221**: `+`
  - **xs06231**: `+`
  - **xs06232**: `+`
  - **xs06233**: `+`
  - **xs06311**: `+`
  - **xs07111**: `+`
  - **xs07112**: `+`
  - **xs07121**: `+`
  - **xs07131**: `+`
  - **xs07141**: `+`
  - **xs07211**: `+`
  - **xs07231**: `+`
  - **xs07241**: `+`
  - **xs07311**: `+`
  - **xs07321**: `+`
  - **xs07331**: `+`
  - **xs07341**: `+`
  - **xs07351**: `+`
  - **xs07361**: `+`
  - **xs08111**: `+`
  - **xs08211**: `+`
  - **xs08311**: `+`
  - **xs09111**: `+`
  - **xs09112**: `+`
  - **xs09121**: `+`
  - **xs09122**: `+`
  - **xs09131**: `+`
  - **xs09141**: `+`
  - **xs09151**: `+`
  - **xs09211**: `+`
  - **xs09221**: `+`
  - **xs09222**: `+`
  - **xs09231**: `+`
  - **xs09311**: `+`
  - **xs09321**: `+`
  - **xs09331**: `+`
  - **xs09341**: `+`
  - **xs09351**: `+`
  - **xs09411**: `+`
  - **xs09421**: `+`
  - **xs09422**: `+`
  - **xs09423**: `+`
  - **xs09424**: `+`
  - **xs09511**: `+`
  - **xs09521**: `+`
  - **xs09531**: `+`
  - **xs09541**: `+`
  - **xs09611**: `+`
  - **xs10111**: `+`
  - **xs10211**: `+`
  - **xs10311**: `+`
  - **xs10411**: `+`
  - **xs10511**: `+`
  - **xs11111**: `+`
  - **xs11112**: `+`
  - **xs11121**: `+`
  - **xs11211**: `+`
  - **xs12111**: `+`
  - **xs12121**: `+`
  - **xs12131**: `+`
  - **xs12311**: `+`
  - **xs12321**: `+`
  - **xs12322**: `+`
  - **xs12411**: `+`
  - **xs12412**: `+`
  - **xs12521**: `+`
  - **xs12531**: `+`
  - **xs12541**: `+`
  - **xs12551**: `+`
  - **xs12621**: `+`
  - **xs12711**: `+`

### 8. Function: DefConst
  **Constants Defined:**
  - `$tco_t_01111`: $tco_t_red3
  - `$tco_t_01112`: $tco_t_red3
  - `$tco_t_01113`: $tco_t_red1
  - `$tco_t_01114`: $tco_t_red1
  - `$tco_t_01115`: $tco_t_red1
  - `$tco_t_01116`: $tco_t_red1
  - `$tco_t_01121`: $tco_t_red1
  - `$tco_t_01122`: $tco_t_red1
  - `$tco_t_01123`: $tco_t_red1
  - `$tco_t_01124`: $tco_t_red1
  - `$tco_t_01125`: $tco_t_red1
  - `$tco_t_01126`: $tco_t_red1
  - `$tco_t_01127`: $tco_t_red1
  - `$tco_t_01131`: $tco_t_red1
  - `$tco_t_01132`: $tco_t_red1
  - `$tco_t_01133`: $tco_t_red1
  - `$tco_t_01134`: $tco_t_red1
  - `$tco_t_01141`: $tco_t_red3
  - `$tco_t_01142`: $tco_t_red3
  - `$tco_t_01143`: $tco_t_red3
  - `$tco_t_01144`: $tco_t_red1
  - `$tco_t_01145`: $tco_t_red3
  - `$tco_t_01146`: $tco_t_red1
  - `$tco_t_01147`: $tco_t_red3
  - `$tco_t_01151`: $tco_t_red1
  - `$tco_t_01152`: $tco_t_red1
  - `$tco_t_01153`: $tco_t_red3
  - `$tco_t_01154`: $tco_t_red1
  - `$tco_t_01155`: $tco_t_red1
  - `$tco_t_01161`: $tco_t_red3
  - `$tco_t_01162`: $tco_t_red3
  - `$tco_t_01163`: $tco_t_red3
  - `$tco_t_01164`: $tco_t_red3
  - `$tco_t_01165`: $tco_t_red3
  - `$tco_t_01166`: $tco_t_red3
  - `$tco_t_01167`: $tco_t_red3
  - `$tco_t_01168`: $tco_t_red3
  - `$tco_t_01169`: $tco_t_red3
  - `$tco_t_01171`: $tco_t_red3
  - `$tco_t_01172`: $tco_t_red3
  - `$tco_t_01173`: $tco_t_red3
  - `$tco_t_01174`: $tco_t_red3
  - `$tco_t_01175`: $tco_t_red3
  - `$tco_t_01176`: $tco_t_red3
  - `$tco_t_01177`: $tco_t_red3
  - `$tco_t_01178`: $tco_t_red3
  - `$tco_t_01181`: $tco_t_red1
  - `$tco_t_01182`: $tco_t_red1
  - `$tco_t_01183`: $tco_t_red1
  - `$tco_t_01184`: $tco_t_red1
  - `$tco_t_01185`: $tco_t_red1
  - `$tco_t_01186`: $tco_t_red1
  - `$tco_t_01191`: $tco_t_red1
  - `$tco_t_01192`: $tco_t_red1
  - `$tco_t_01193`: $tco_t_red1
  - `$tco_t_01194`: $tco_t_red1
  - `$tco_t_01211`: $tco_t_red1
  - `$tco_t_01212`: $tco_t_red1
  - `$tco_t_01213`: $tco_t_red1
  - `$tco_t_01221`: $tco_t_red1
  - `$tco_t_01222`: $tco_t_std
  - `$tco_t_01223`: $tco_t_red1
  - `$tco_t_01224`: $tco_t_red1
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
  - `$tco_t_04321`: $tco_t_red1
  - `$tco_t_04411`: $tco_t_red1
  - `$tco_t_04421`: $tco_t_red1
  - `$tco_t_04431`: $tco_t_red1
  - `$tco_t_04441`: $tco_t_std
  - `$tco_t_04511`: $tco_t_std
  - `$tco_t_04521`: $tco_t_std
  - `$tco_t_04522`: $tco_t_std
  - `$tco_t_04531`: $tco_t_std
  - `$tco_t_04541`: $tco_t_std
  - `$tco_t_04551`: $tco_t_std
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
  - `$tco_t_06111`: $tco_t_red3
  - `$tco_t_06121`: $tco_t_red1
  - `$tco_t_06131`: $tco_t_red1
  - `$tco_t_06211`: $tco_t_zero
  - `Run_Cond`: GetDataCOICOPVersion = 2003
  - `$tco_t_12711`: $tco_t_std
  - `$tco_t_12621`: $tco_t_zero
  - `$tco_t_12551`: $tco_t_zero
  - `$tco_t_12541`: $tco_t_zero
  - `$tco_t_12531`: $tco_t_zero
  - `$tco_t_12521`: $tco_t_zero
  - `$tco_t_12412`: $tco_t_zero
  - `$tco_t_12411`: $tco_t_zero
  - `$tco_t_12322`: $tco_t_std
  - `$tco_t_12321`: $tco_t_std
  - `$tco_t_12311`: $tco_t_std
  - `$tco_t_12131`: $tco_t_std
  - `$tco_t_12121`: $tco_t_std
  - `$tco_t_12111`: $tco_t_std
  - `$tco_t_11211`: $tco_t_red1
  - `$tco_t_11121`: $tco_t_red1
  - `$tco_t_11112`: $tco_t_red1
  - `$tco_t_11111`: $tco_t_red1
  - `$tco_t_10511`: $tco_t_zero
  - `$tco_t_10411`: $tco_t_zero
  - `$tco_t_10311`: $tco_t_zero
  - `$tco_t_10211`: $tco_t_zero
  - `$tco_t_10111`: $tco_t_zero
  - `$tco_t_09611`: $tco_t_std
  - `$tco_t_09541`: $tco_t_std
  - `$tco_t_09531`: $tco_t_red3
  - `$tco_t_09521`: $tco_t_red3
  - `$tco_t_09511`: $tco_t_red3
  - `$tco_t_09424`: $tco_t_std
  - `$tco_t_09423`: $tco_t_std
  - `$tco_t_09422`: $tco_t_red1
  - `$tco_t_09421`: $tco_t_red1
  - `$tco_t_09411`: $tco_t_zero
  - `$tco_t_09351`: $tco_t_std
  - `$tco_t_09341`: $tco_t_std
  - `$tco_t_09331`: $tco_t_std
  - `$tco_t_09321`: $tco_t_std
  - `$tco_t_09311`: $tco_t_std
  - `$tco_t_09231`: $tco_t_std
  - `$tco_t_09222`: $tco_t_std
  - `$tco_t_09221`: $tco_t_std
  - `$tco_t_09211`: $tco_t_std
  - `$tco_t_09151`: $tco_t_std
  - `$tco_t_09141`: $tco_t_std
  - `$tco_t_09131`: $tco_t_std
  - `$tco_t_09122`: $tco_t_std
  - `$tco_t_09121`: $tco_t_std
  - `$tco_t_09112`: $tco_t_std
  - `$tco_t_09111`: $tco_t_std
  - `$tco_t_08311`: $tco_t_std
  - `$tco_t_08211`: $tco_t_std
  - `$tco_t_08111`: $tco_t_zero
  - `$tco_t_07361`: $tco_t_std
  - `$tco_t_07351`: $tco_t_red1
  - `$tco_t_07341`: $tco_t_red1
  - `$tco_t_07331`: $tco_t_red1
  - `$tco_t_07321`: $tco_t_red1
  - `$tco_t_07311`: $tco_t_red1
  - `$tco_t_07241`: $tco_t_std
  - `$tco_t_07231`: $tco_t_std
  - `$tco_t_07221`: $tco_t_std
  - `$tco_t_07211`: $tco_t_std
  - `$tco_t_07141`: $tco_t_std
  - `$tco_t_07131`: $tco_t_std
  - `$tco_t_07121`: $tco_t_std
  - `$tco_t_07112`: $tco_t_std
  - `$tco_t_07111`: $tco_t_std
  - `$tco_t_06311`: $tco_t_zero
  - `$tco_t_06233`: $tco_t_zero
  - `$tco_t_06232`: $tco_t_zero
  - `$tco_t_06231`: $tco_t_zero
  - `$tco_t_06221`: $tco_t_zero

### 9. Function: DefIl
  - **Name**: `ils_extstat_ittcal`
  - **il_itt_excc**: `+`
  - **il_itt_revc**: `+`

### 10. Function: DefIl
  - **Name**: `il_itt_excc`
  - **il_tx045_072_na**: `+`
  - **il_tx04521_na**: `+`
  - **il_tx0451_na**: `+`
  - **il_tx045_na**: `+`
  - **il_tx022_na**: `+`
  - **il_tx0213_na**: `+`
  - **il_tx02122_na**: `+`
  - **il_tx02121_na**: `+`
  - **il_tx0211_na**: `+`

### 11. Function: DefIl
  - **Name**: `il_itt_revc`
  - **il_tx_na**: `+`
  - **il_tva_na**: `+`

### 12. Function: DefIl
  - **Name**: `ils_extstat_ittncal`
  - **il_itt_expnc**: `+`
  - **il_itt_revnc**: `+`
  - **il_itt_excnc**: `+`

### 13. Function: DefIl
  - **Name**: `il_itt_excnc`
  - **il_tx045_072**: `+`
  - **il_tx04521**: `+`
  - **il_tx0451**: `+`
  - **il_tx045**: `+`
  - **il_tx022**: `+`
  - **il_tx0213**: `+`
  - **il_tx02122**: `+`
  - **il_tx02121**: `+`
  - **il_tx0211**: `+`

### 14. Function: DefIl
  - **Name**: `il_itt_revnc`
  - **il_tx**: `+`
  - **il_tva**: `+`

### 15. Function: DefIl
  - **Name**: `il_itt_expnc`
  - **il_x12**: `+`
  - **il_x11**: `+`
  - **il_x10**: `+`
  - **il_x09**: `+`
  - **il_x08**: `+`
  - **il_x07**: `+`
  - **il_x06**: `+`
  - **il_x05**: `+`
  - **il_x04**: `+`
  - **il_x03**: `+`
  - **il_x02**: `+`
  - **il_x01**: `+`

### 16. Function: DefConst
  **Constants Defined:**
  - `$tco_ov_04511`: $tco_base_ov_04511

### 17. Function: DefIl
  - **Name**: `il_xs_othct`
  - **xs04511**: `+`
  - **Warn_If_NonMonetary**: `no`


---
