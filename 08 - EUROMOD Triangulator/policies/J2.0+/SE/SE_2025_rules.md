# EUROMOD Tax-Benefit Rules for SE_2025

## Policy: uprate_se
### 1. Function: Uprate
  - **dataset**: `*training_data`
  - **def_factor**: `1`
  - **WarnIfNoFactor**: `no`
  - **Dataset**: `*_hhot`

### 2. Function: SetDefault
  - **Dataset**: `*_hhot`
  - **xhc**: `2500`
  - **afc**: `0`
  - **bunct_s**: `0`
  - **bsa**: `0`
  - **liwmy**: `0`

### 3. Function: Uprate
  - **Dataset**: `se_20??_??_*`
  - **yse**: `$f_wage`
  - **ypt**: `$f_unit`
  - **ypp**: `$f_unit`
  - **yot**: `$f_unit`
  - **ypr**: `$f_house`
  - **yiy**: `$f_yiy`
  - **yem**: `1`
  - **xpp**: `$f_unit`
  - **xmp**: `$f_unit`
  - **xhcrt**: `$f_cpi`
  - **xhcot**: `$f_cpi`
  - **xhcmomi**: `$f_cpi`
  - **xhc**: `$f_cpi`
  - **tpr**: `$f_unit`
  - **psu**: `$f_pen`
  - **poa**: `$f_pen`
  - **pdi**: `$f_pen`
  - **kfb**: `$f_cpi`
  - **bun**: `$f_hourly_wage`
  - **bpl**: `$f_unit`
  - **bhl**: `$f_hourly_wage`
  - **bed**: `$f_unit`
  - **afc**: `$f_unit`
  - **bchot**: `$HICP`
  - **bch**: `$HICP`
  - **bho**: `$HICP`
  - **bsa**: `$HICP`
  - **kfbcc**: `$HICP`
  - **tis**: `$HICP`
  - **tin**: `$HICP`
  - **tad**: `$HICP`
  - **tscse**: `$HICP`
  - **tscer**: `$HICP`
  - **tscee**: `$HICP`
  - **ydses_o**: `$HICP`
  - **yds**: `$f_unit`
  - **yivwg**: `$f_hourly_wage`
  - **yem_a**: `$f_hourly_wage`
  - **yptmp**: `$f_unit`
  - **bfa**: `$HICP`
  - **ymwdt**: `$f_hourly_wage`
  - **bunct**: `$f_hourly_wage_lagged`
  - **bunnc**: `$f_unit`
  - **bsamt**: `$HICP`
  - **bsanm**: `$f_unit`
  - **bch00**: `$HICP`
  - **yem20_a**: `$f_hourly_wage`
  - **xed00**: `$f_cpi`
  - **xhl00**: `$f_cpi`
  - **Factor_Condition**: `lindi < 1`
  - **kivho**: `$f_cpi`


---

## Policy: ConstDef_se
### 1. Function: DefConst
  **Constants Defined:**
  - `$XBASM`: 58800#y
  - `$XBASMI`: 80600#y

### 2. Function: DefConst
  **Constants Defined:**
  - `$ImputedWage`: 0
  - `$fthw `: n/a

### 3. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$bunrate1`: 0.8
  - `$bunrate2`: 0.8
  - `$bunrate3`: 0.7
  - `$bunuplim`: 18700#m
  - `$siceethres`: 1000#y
  - `$siceebase1`: 8.07
  - `$siceebase2`: 0.423
  - `$siceerate`: 0.07
  - `$sicerthres`: 1000#y
  - `$scersirate`: 0.0355
  - `$scerrdrate`: 0.75
  - `$scermlrate`: 0.026
  - `$scerotrate3`: n/a
  - `$scerotrate2`: n/a
  - `$scerotrate1`: 0.1162
  - `$sceracrate`: 0.0020
  - `$scercirate`: 0.0060
  - `$scerpirate`: 0.1021
  - `$scerirrate`: 0.0264
  - `$bunrate4`: 0.65
  - `$ImputedWage`: n/a

### 4. Function: DefConst
  **Constants Defined:**
  - `$UB_QperMin`: 6
  - `$UB_QperTot`: 12
  - `$UB_UpLim1`: 910#l
  - `$UB_LowLim`: 510#l
  - `$UB_UpLim2`: 760#l
  - `$UB_LowLimB`: 510#l
  - `$UB_UpLim1B`: 1200#l
  - `$UB_UpLim2B`: 1000#l

### 5. Function: DefConst
  **Constants Defined:**
  - `$fthw `: 40
  - `$lhw`: n/a

### 6. Function: DefConst
  **Constants Defined:**
  - `$lhw`: 40
  - `$mc_my`: n/a
  - `$mc_rrate1`: n/a
  - `$mc_rrate2`: n/a
  - `$mc_rrate3`: n/a
  - `$mc_rrate4`: n/a
  - `$mc_share1`: n/a
  - `$mc_share2`: n/a
  - `$mc_share3`: n/a
  - `$mc_share4`: n/a
  - `$mc_max_yem`: n/a
  - `$tscer_thr`: n/a
  - `$tscse_thr`: n/a

### 7. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$mc_my`: 6
  - `$mc_rrate1`: 0.80
  - `$mc_rrate2`: 0.85
  - `$mc_rrate3`: 0.875
  - `$mc_rrate4`: 0.85
  - `$mc_share1`: 0.9375
  - `$mc_share2`: 0.8824
  - `$mc_share3`: 0.8571
  - `$mc_share4`: 0.8824
  - `$mc_amount`: n/a
  - `$mc_min`: n/a
  - `$mc_max`: n/a
  - `$mc_max_yem`: 44000#m
  - `$tscer_thr`: 25000#m
  - `$tscse_thr`: 100000#m
  - `$yemcomp_stdmy`: 12
  - `$yemcomp_thres1`: 1.00
  - `$yemcomp_thres2`: 0.75
  - `$yemcomp_thres3`: 0.50
  - `$yemcomp_thres4`: 0.25
  - `$yemcomp_thres5`: 0
  - `$yemcomp_rate1`: 0.80
  - `$yemcomp_rate2`: 0.6
  - `$yemcomp_rate3`: 0.40
  - `$yemcomp_rate4`: 0.2
  - `$yemcomp_minamt`: 0

### 8. Function: DefConst
  **Constants Defined:**
  - `$bunct_stdmy`: 12
  - `$bunct_my1`: 10
  - `$bunct_coef1`: 1/0.8
  - `$bunct_my2`: 9
  - `$bunct_my3`: 12
  - `$bunct_coef2`: 1/0.7
  - `$bunct_minage`: 16
  - `$bunct_maxage`: 65
  - `$bunct_coef3`: 52 / 12
  - `$bunct_thres1`: 30
  - `$bunct_rate1`: 0.8
  - `$bunct_rate2`: 0.7
  - `$bunct_rate3`: 0.65

### 9. Function: DefConst
  **Constants Defined:**
  - `$bfapl_stdmy`: 12
  - `$bfapl_child_age1`: 0
  - `$bfapl_child_age2`: 0
  - `$bfapl_coef1`: 30.5
  - `$bfapl_couple_amt1`: 390
  - `$bfapl_couple_amt2`: 60
  - `$bfapl_couple_amt3`: 180
  - `$bfapl_single_amt1`: 480
  - `$bfapl_single_amt2`: 60
  - `$bfapl_single_amt3`: 180
  - `$bfapl_couple_amt4`: 90
  - `$bfapl_couple_rate1`: 0.8
  - `$bfapl_couple_coef1`: 0.97
  - `$bfapl_couple_amt5`: 300
  - `$bfapl_couple_lim`: 10
  - `$bfapl_couple_amt6`: 250
  - `$bfapl_couple_amt7`: 180
  - `$bfapl_single_rate1`: 0.8
  - `$bfapl_single_coef1`: 0.97
  - `$bfapl_single_amt5`: 390
  - `$bfapl_single_lim`: 10
  - `$bfapl_single_amt6`: 250
  - `$bfapl_single_amt7`: 180

### 10. Function: DefConst
  **Constants Defined:**
  - `$bpa_coef1`: 0.97
  - `$bpa_rate`: 0.80
  - `$bpa_coef2`: 30.5
  - `$bpa_maxamt`: 10
  - `$bpa_maxlim`: 7.5
  - `$bpa_stdmy`: 12

### 11. Function: DefConst
  **Constants Defined:**
  - `$tscer_maxage `: 66
  - `$tscer_minamt1`: 1000#y
  - `$tscer_rate1`: 3.55%
  - `$tscer_rate2`: 10.21%
  - `$tscer_rate3`: 0.60%
  - `$tscer_rate4`: 0.20% 
  - `$tscer_rate5`: 2.64%
  - `$tscer_rate6`: 11.62%
  - `$tscer_rate7`: 2.60%
  - `$tscer_age1`: 23
  - `$tscer_minamt2`: 0#y
  - `$tscer_maxamt1`: 25000*.3142*0.4478
  - `$tscer_ret_minage`: 65
  - `$tscer_ret_maxage`: GetSystemYear - 1937 -1
  - `$tscer_minamt3`: 1000#y
  - `$tscer_rate8`: 10.21%

### 12. Function: DefConst
  **Constants Defined:**
  - `$tscee_maxage`: GetSystemYear - 1937 -1
  - `$tscee_minamt`: 1000#y
  - `$tscee_stdmy`: 12
  - `$tscee_coef1`: 8.07
  - `$tscee_coef2`: 0.423
  - `$tscee_rate`: 7%

### 13. Function: DefConst
  **Constants Defined:**
  - `$tscse_maxage1`: 65
  - `$tscse_minamt`: 1000#y
  - `$tscse_rate1`: 3.64%
  - `$tscse_rate2`: 10.21%
  - `$tscse_rate3`: 0.60%
  - `$tscse_rate4`: 0.20%
  - `$tscse_rate5`: 0.10%
  - `$tscse_rate6`: 11.62%
  - `$tscse_rate7`: 2.60%
  - `$tscse_ret_minage`: 65
  - `$tscse_ret_maxage`: GetSystemYear - 1937 -1
  - `$tscse_minamt2`: 1000#y
  - `$tscse_rate8`: 10.21%

### 14. Function: DefConst
  **Constants Defined:**
  - `$tin_amt1`: 0#y
  - `$tin_ee_thres1`: 0
  - `$tin_ee_thres2`: 0.99
  - `$tin_ee_thres3`: 2.72
  - `$tin_ee_thres4`: 3.11
  - `$tin_ee_thres5`: 7.88
  - `$tin_ee_coef1`: 0.423
  - `$tin_ee_coef2`: 0.2
  - `$tin_ee_coef3`: 0.99
  - `$tin_ee_coef4`: 0.77
  - `$tin_ee_coef5`: 0.1
  - `$tin_ee_coef6`: 3.11
  - `$tin_ee_coef7`: 0.293
  - `$tin_ret_minage`: 65
  - `$tin_ret_thres1`: 0
  - `$tin_ret_thres2`: 0.91
  - `$tin_ret_thres3`: 1.11
  - `$tin_ret_thres4`: 1.965
  - `$tin_ret_thres5`: 2.72
  - `$tin_ret_thres6`: 3.11
  - `$tin_ret_thres7`: 3.24
  - `$tin_ret_thres8`: 5
  - `$tin_ret_thres9`: 7.88
  - `$tin_ret_thres10`: 8.08
  - `$tin_ret_thres11`: 10.94
  - `$tin_ret_thres12`: 12.47
  - `$tin_ret_thres13`: n/a
  - `$tin_ret_thres14`: n/a
  - `$tin_ret_coef1`: 0.687
  - `$tin_ret_coef2`: 0.885
  - `$tin_ret_coef3`: 0.2
  - `$tin_ret_coef4`: 0.600
  - `$tin_ret_coef5`: 0.057
  - `$tin_ret_coef6`: 0.333
  - `$tin_ret_coef7`: 0.1949
  - `$tin_ret_coef8`: -0.212
  - `$tin_ret_coef9`: 0.3949
  - `$tin_ret_coef10`: -0.523
  - `$tin_ret_coef11`: 0.4949
  - `$tin_ret_coef12`: 0.096
  - `$tin_ret_coef13`: 0.304
  - `$tin_ret_coef14`: 0.186
  - `$tin_ret_coef15`: 0.286
  - `$tin_ret_coef16`: 0.872
  - `$tin_ret_coef17`: 0.199
  - `$tin_ret_coef18`: 2.48
  - `$tin_ret_coef25`: 0
  - `$tin_ret_coef19`: 9.263
  - `$tin_ret_coef20`: 0.62
  - `$tin_ret_coef21`: 1.532
  - `$tin_ret_coef26`: 0
  - `$tin_ret_coef22`: n/a
  - `$tin_ret_coef23`: n/a
  - `$tin_ret_coef24`: n/a
  - `$tin_ret_coef27`: 0
  - `$tin_amt2`: 1500#y
  - `$tin_amt3`: 0
  - `$tin_amt4`: 40000#y
  - `$tin_rate6`: 0.75%
  - `$tinna_upthres1`: 625500#y
  - `$tinpm_rate`: 0.01
  - `$tinpm_amt`: 1327#y
  - `$tintcmi_rate1`: 30%
  - `$tintcmi_amt`: 100000#y
  - `$tintcmi_rate2`: 21% 
  - `$tintc_ee_maxage`: 65
  - `$tintc_ee_addthres1`: 0
  - `$tintc_ee_addthres2`: 0.91
  - `$tintc_ee_addthres3`: 3.24
  - `$tintc_ee_addthres4`: 8.08
  - `$tintc_ee_addthres5`: 13.54
  - `$tin_ee_addcoef1`: 0.91
  - `$tin_ee_addcoef2`: 0.3874
  - `$tin_ee_addcoef3`: 1.813
  - `$tin_ee_addcoef4`: 0.199
  - `$tin_ee_addcoef5`: 3.24
  - `$tin_ee_addcoef6`: 2.776
  - `$tin_ee_addcoef7`: n/a
  - `$tin_ee_addcoef8`: n/a
  - `$tin_ret_addthres1`: 0
  - `$tin_ret_addthres2`: n/a
  - `$tin_ret_addthres3`: n/a
  - `$tin_ret_addthres4`: n/a
  - `$tin_ret_addcoef1`: 0.22
  - `$tin_ret_addcoef2`: 15000#y
  - `$tin_ret_addcoef3`: 0.07
  - `$tin_ret_addcoef4`: 36000#y
  - `$tin_ret_addcoef5`: 0.03
  - `$tin_disab_addthres1`: 0.91
  - `$tin_disab_addthres2`: 3.24
  - `$tin_disab_addcoef1`: 0.045
  - `$tin_disab_addcoef2`: 0.91
  - `$tin_disab_addcoef3`: 0.3405
  - `$tin_disab_addcoef4`: 1.703
  - `$tin_disab_addcoef5`: 0.128
  - `$tin_disab_addcoef6`: 3.24
  - `$tinna_rate3`: n/a
  - `$tinna_rate2`: 0.2
  - `$tinna_rate1`: 0
  - `$tinfu_rate`: 0.00293
  - `$tinrg_rate`: 0.1169
  - `$tinmu_rate`: 0.2071
  - `$tin_exempt_thres`: 24873#y

  - `$tin_ret_addthres5`: 1.75
  - `$tin_ret_addthres6`: 5.24
  - `$tin_ret_addthres7`: n/a
  - `$tin_ret_addcoef6`: 0.22
  - `$tin_ret_addcoef7`: 0.2635
  - `$tin_ret_addcoef8`: 0.07
  - `$tin_ret_addcoef9`: 0.6293
  - `$tin_ret_addcoef10`: n/a
  - `$tin_ret_addcoef11`: n/a

### 15. Function: DefConst
  **Constants Defined:**
  - `$bch_maxage1`: 16
  - `$bch_stdamt`: 1250#m
  - `$bch_addamt1`: 150#m
  - `$bch_addamt2`: 580#m
  - `$bch_addamt3`: 1010#m
  - `$bch_addamt4`: 1250#m
  - `$bch_maxage2`: 18
  - `$bch_addamt5`: 150#m
  - `$bch_addamt6`: 580#m
  - `$bch_addamt7`: 1010#m
  - `$bch_addamt8`: 1250#m
  - `$bch_maxage3`: 17
  - `$bch_redcoef`: 10/12

### 16. Function: DefConst
  **Constants Defined:**
  - `$bho_rate1`: 0.15
  - `$bho_thres1`: 100000#y
  - `$bho_stdmy`: 12
  - `$bho_child1_coef`: 1
  - `$bho_child2_coef`: 2
  - `$bho_child3_coef`: 3
  - `$bho_child1_stdamt`: 1500#m
  - `$bho_child2_stdamt`: 2000#m
  - `$bho_child3_stdamt`: 2650#m
  - `$bho_amt1`: 5300#m
  - `$bho_amt2`: 1400#m
  - `$bho_amt3`: 5900#m
  - `$bho_amt4`: 6600#m
  - `$bho_coef1`: 0.5
  - `$bho_redcoef1`: 20%
  - `$bho_amt5`: 75000#y
  - `$bho_supplcoef1`: 0.40
  - `$bho_redcoef2`: 0.2
  - `$bho_thres2`: 150000#y
  - `$bho_supplcoef2`: 0.25
  - `$bho_minage`: 18
  - `$bho_maxage`: 29
  - `$bho_amt6`: 1800#m
  - `$bho_amt7`: 2600#m
  - `$bho_amt8`: 3600#m
  - `$bho_coef2`: 0.9
  - `$bho_coef3`: 0.65
  - `$bho_coef4`: 0.33
  - `$bho_amt9`: 41000#y
  - `$bho_amt10`: 58000#y
  - `$bho_minamt`: 100#m
  - `$bho_coef5`: n/a
  - `$bho_my1`: 6/12

### 17. Function: DefConst
  **Constants Defined:**
  - `$bhope_rate1`: 0.15
  - `$bhope_thres1`: 200000#m
  - `$bhope_rate2`: 0.15
  - `$bhope_thres2`: 100000#y
  - `$bhope_stdmy`: 12
  - `$bhope_ret_minage`: 65
  - `$bhope_disab_age1`: 20
  - `$bhope_disab_age2`: 22
  - `$bhope_disab_age3`: 24
  - `$bhope_disab_age4`: 26
  - `$bhope_disab_age5`: 28
  - `$bhope_disab_age6`: 29
  - `$bhope_disab_age7`: 30
  - `$bhope_disab_age8`: 65
  - `$bhope_disab_coef1`: 2.48
  - `$bhope_disab_coef2`: 2.53
  - `$bhope_disab_coef3`: 2.58
  - `$bhope_disab_coef4`: 2.63
  - `$bhope_disab_coef5`: 2.68
  - `$bhope_disab_coef6`: 2.73
  - `$bhope_disab_coef7`: 2.78
  - `$bhope_disab_coef8`: 2.43
  - `$bhope_disab_coef9`: 2.2
  - `$bhope_ret_coef1`: 1
  - `$bhope_ret_coef2`: 0.90
  - `$bhope_ret_coef3`: 0.7
  - `$bhope_ret_coef4`: 0.5
  - `$bhope_ret_coef5`: 840
  - `$bhope_ret_coef6`: 1
  - `$bhope_ret_coef7`: 0.90
  - `$bhope_ret_coef8`: 0.7
  - `$bhope_ret_coef9`: 0.5
  - `$bhope_ret_coef10`: 540
  - `$bhope_disab_coef10`: 0.96

  - `$bhope_disab_coef11`: 0.7
  - `$bhope_amt1`: 3000#m
  - `$bhope_amt2`: 5000#m
  - `$bhope_amt3`: 7000#m
  - `$bhope_amt4`: 7500#m
  - `$bhope_ret_coef11`: 0.62
  - `$bhope_ret_coef12`: 0.5
  - `$bhope_minamt`: 25#m

### 18. Function: DefConst
  **Constants Defined:**
  - `$bsamt_child_age1`: 0
  - `$bsamt_child_age2`: 1
  - `$bsamt_child_age3`: 2
  - `$bsamt_child_age4`: 3
  - `$bsamt_child_age5`: 4
  - `$bsamt_child_age6`: 6
  - `$bsamt_child_age7`: 7
  - `$bsamt_child_age8`: 10
  - `$bsamt_child_age9`: 11
  - `$bsamt_child_age10`: 14
  - `$bsamt_child_age11`: 15
  - `$bsamt_child_age12`: 18
  - `$bsamt_child_age13`: 19
  - `$bsamt_child_amt1`: 2720#m
  - `$bsamt_child_amt2`: 3030#m
  - `$bsamt_child_amt3`: 2700#m
  - `$bsamt_child_amt4`: 3030#m
  - `$bsamt_child_amt5`: 3790#m
  - `$bsamt_child_amt6`: 4350#m
  - `$bsamt_child_amt7`: 4920#m
  - `$bsamt_child_amt8`: 4960#m
  - `$bsamt_ChildSingle_amt1`: 3910#m
  - `$bsamt_ChildCouple_amt1`: 7050#m
  - `$bsamt_coef1`: 1
  - `$bsamt_coef2`: 2
  - `$bsamt_coef3`: 3
  - `$bsamt_coef4`: 4
  - `$bsamt_coef5`: 5
  - `$bsamt_coef6`: 6
  - `$bsamt_coef7`: 7
  - `$bsamt_amt1`: 1270#m
  - `$bsamt_amt2`: 1400#m
  - `$bsamt_amt3`: 1770#m
  - `$bsamt_amt4`: 2010#m
  - `$bsamt_amt5`: 2310#m
  - `$bsamt_amt6`: 2620#m
  - `$bsamt_amt7`: 2810#m
  - `$bsamt_amt8`: 100#m

### 19. Function: DefConst *(Switch: off)*
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

### 20. Function: DefConst
  **Constants Defined:**
  - `$bsamt_BTA_rate`: 1
  - `$bsamt_BCA_rate`: 1


---

## Policy: ildef_se
### 1. Function: DefIl
  - **name**: `il_taxabley`
  - **yem**: `+`
  - **kfb**: `+`
  - **yse**: `+`
  - **yot**: `+`
  - **ypp**: `+`
  - **bunct_s**: `+`
  - **poa**: `+`
  - **pdi**: `+`
  - **psu**: `+`
  - **bhl**: `+`
  - **bpl**: `+`
  - **yselo_s**: `+`
  - **bunct**: `+`
  - **bpa_s**: `+`
  - **bfapl_s**: `+`
  - **bunnc**: `+`
  - **yemmc_s**: `+`
  - **bwkmcee_s**: `+`

### 2. Function: DefIl
  - **name**: `il_taxabley_ppta`
  - **il_taxabley**: `+`
  - **tintapv_s**: `-`

### 3. Function: DefIl
  - **name**: `il_sicee_base`
  - **yem**: `+`
  - **kfb**: `+`
  - **bhl**: `+`
  - **bunct_s**: `+`
  - **bunct**: `+`
  - **bunnc**: `+`
  - **yemmc_s**: `+`
  - **bwkmcee_s**: `+`

### 4. Function: DefIl
  - **name**: `il_sicer_base`
  - **yem**: `+`
  - **kfb**: `+`
  - **yemmc_s**: `+`
  - **bwkmcee_s**: `+`

### 5. Function: DefIl
  - **name**: `il_taxbase`
  - **il_taxabley**: `+`
  - **tintapv_s**: `-`
  - **tinta00_s**: `-`
  - **tintape_s**: `-`

### 6. Function: DefIl
  - **name**: `il_means_bho_prel`
  - **yem**: `+`
  - **kfb**: `+`
  - **ypp**: `+`
  - **bunct_s**: `+`
  - **poa**: `+`
  - **psu**: `+`
  - **bhl**: `+`
  - **pdi**: `+`
  - **ypr**: `+`
  - **yiy**: `+`
  - **yse**: `+`
  - **bed**: `+0.80`
  - **bpl**: `+`
  - **afc00_s**: `+`
  - **yselo_s**: `+`
  - **bunct**: `+`
  - **bpa_s**: `+`
  - **bfapl_s**: `+`
  - **bunnc**: `+`
  - **yemmc_s**: `+`
  - **bwkmcee_s**: `+`

### 7. Function: DefIl
  - **name**: `il_means_bho`
  - **il_means_bho_prel**: `+`
  - **ychot_s**: `-`

### 8. Function: DefIl *(Switch: off)*
  - **name**: `n/a`
  - **yem**: `n/a`
  - **kfb**: `n/a`
  - **bpl**: `n/a`
  - **ypp**: `n/a`
  - **bunct_s**: `n/a`
  - **poa**: `n/a`
  - **psu**: `n/a`
  - **bhl**: `n/a`
  - **pdi**: `n/a`
  - **ypr**: `n/a`
  - **yiy**: `n/a`
  - **yse**: `n/a`
  - **afc00_s**: `n/a`
  - **ydg01_s**: `n/a`
  - **yselo_s**: `n/a`
  - **bunct**: `n/a`
  - **bpa_s**: `n/a`
  - **bfapl_s**: `n/a`
  - **bunnc**: `n/a`

### 9. Function: DefIl
  - **name**: `il_means_bhope_prel`
  - **yem**: `+0.5`
  - **bpl**: `+0.8`
  - **kfb**: `+0.8`
  - **ypp**: `+0.8`
  - **bunct_s**: `+0.8`
  - **poa**: `+`
  - **psu**: `+0.8`
  - **bhl**: `+0.8`
  - **pdi**: `+`
  - **ypr**: `+`
  - **yiy**: `+`
  - **yse**: `+0.5`
  - **afc00_s**: `+`
  - **ydg01_s**: `-`
  - **yselo_s**: `+`
  - **bunct**: `+0.8`
  - **bpa_s**: `+0.8`
  - **bfapl_s**: `+0.8`
  - **bunnc**: `+0.8`
  - **yemmc_s**: `+0.5`
  - **bwkmcee_s**: `+0.5`

### 10. Function: DefIl *(Switch: off)*
  - **name**: `ils_sicct`

### 11. Function: DefIl
  - **name**: `il_means_bsa`
  - **ils_origy**: `+`
  - **ils_pen**: `+`
  - **ils_bennt**: `+`
  - **bho_s**: `+`
  - **bhope_s**: `+`
  - **ils_sicee**: `-`
  - **ils_sicse**: `-`
  - **ils_tax**: `-`
  - **yselo_s**: `+`

### 12. Function: DefIl
  - **Name**: `il_tu`
  - **ils_origy**: `+`
  - **bunct_s**: `+`
  - **bunct**: `+`
  - **bunnc**: `+`
  - **bhl**: `+`
  - **bpl**: `+`
  - **bfapl_s**: `+`
  - **bpa_s**: `+`
  - **bwkmcee_s**: `+`

### 13. Function: DefIl
  - **name**: `il_means_bhope_prel_64`
  - **poa**: `+0.93`
  - **pdi**: `n/a`
  - **yiy**: `+`
  - **ypp**: `+0.93`
  - **kfb**: `+0.93`
  - **bunct_s**: `+0.93`
  - **bunct**: `+0.93`
  - **bunnc**: `+0.93`
  - **bhl**: `+0.93`
  - **bpl**: `+0.93`
  - **bfapl_s**: `+0.93`
  - **bpa_s**: `+0.93`
  - **psu**: `+`
  - **yem**: `n/a`
  - **yemmc_s**: `n/a`
  - **yse**: `n/a`
  - **yselo_s**: `+`
  - **ypr**: `+`
  - **afc00_s**: `+`
  - **ydg01_s**: `-`
  - **bwkmcee_s**: `n/a`

### 14. Function: DefIl *(Switch: n/a)*
  - **name**: `n/a`
  - **poa**: `n/a`
  - **pdi**: `n/a`
  - **yiy**: `n/a`
  - **ypp**: `n/a`
  - **kfb**: `n/a`
  - **bunct_s**: `n/a`
  - **bunct**: `n/a`
  - **bunnc**: `n/a`
  - **bhl**: `n/a`
  - **bpl**: `n/a`
  - **bfapl_s**: `n/a`
  - **bpa_s**: `n/a`
  - **psu**: `n/a`
  - **yem**: `n/a`
  - **yemmc_s**: `n/a`
  - **yse**: `n/a`
  - **yselo_s**: `n/a`
  - **ypr**: `n/a`
  - **afc00_s**: `n/a`
  - **ydg01_s**: `n/a`
  - **bwkmcee_s**: `n/a`

### 15. Function: DefIl *(Switch: n/a)*
  - **name**: `n/a`
  - **poa**: `n/a`
  - **yiy**: `n/a`
  - **ypp**: `n/a`
  - **kfb**: `n/a`
  - **bunct_s**: `n/a`
  - **bunct**: `n/a`
  - **bunnc**: `n/a`
  - **bhl**: `n/a`
  - **bpl**: `n/a`
  - **bfapl_s**: `n/a`
  - **bpa_s**: `n/a`
  - **psu**: `n/a`
  - **yselo_s**: `n/a`
  - **ypr**: `n/a`
  - **afc00_s**: `n/a`
  - **ydg01_s**: `n/a`


---

## Policy: tudef_se
### 1. Function: DefTu
  - **Name**: `tu_hh_oecd_co`
  - **Type**: `HH`
  - **DepChildCond**: `dag<14`

### 2. Function: DefTu
  - **Name**: `tu_individual_se`
  - **Type**: `IND`
  - **LoneParentCond**: `Default`

### 3. Function: DefTu
  - **Name**: `tu_household_se`
  - **Type**: `HH`
  - **DepChildCond**: `Default & (dag < 16 | (dag < 20 & dec >= 4 & dms != 2))`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`
  - **NoChildIfHead**: `yes`
  - **LoneParentCond**: `Default`

### 4. Function: DefTu
  - **Name**: `tu_bch_se`
  - **Type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild & LooseDepChild`
  - **PartnerCond**: `default`
  - **DepChildCond**: `Default & (dag < 16 | (dag <= 18 & dec = 4))`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`
  - **NoChildIfHead**: `yes`
  - **LoneParentCond**: `Default`

### 5. Function: DefTu
  - **Name**: `tu_bho_se`
  - **Type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild & LooseDepChild`
  - **PartnerCond**: `default`
  - **DepChildCond**: `Default & (dag < 18 | (dag < 20 & dec = 4))`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`
  - **NoChildIfHead**: `yes`
  - **LoneParentCond**: `Default`


---

## Policy: neg_se
### 1. Function: ArithOp
  **Formula:** `0 - yse`
  **Output Variable:** `ysena`
  **Tax Unit:** `tu_individual_se`

### 2. Function: Max
  - **val**: `0`
  - **output_var**: `yse`
  - **TAX_UNIT**: `tu_individual_se`

### 3. Function: ArithOp
  **Formula:** `0 - yse`
  **Output Variable:** `yselo_s`
  **Tax Unit:** `tu_individual_se`

### 4. Function: SetDefault
  - **Dataset**: `*`
  - **ysena**: `0`


---

## Policy: yem_se *(Switch: switch)*
### 1. Function: DefConst
  **Constants Defined:**
  - `$Nwh`: 40
  - `const_monetary`: no
  - `$Minwage`: 0

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem > 0`
  - **Tax Unit:** `tu_individual_se`

### 3. Function: Max
  - **who_must_be_elig**: `one`
  - **val**: `$Minwage*min(lhw,$Nwh)/$Nwh*yemmy/12`
  - **output_var**: `yem`
  - **TAX_UNIT**: `tu_individual_se`

### 4. Function: ChangeParam
  - **Param_Id**: `d479250e-366d-4184-8d5e-6b52b9acf24b`
  - **Param_NewVal**: `se_2025_yem_std`


---

## Policy: tscee_se
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag <= $tscee_maxage & il_sicee_base > amount#1`
  - **Tax Unit:** `tu_individual_se`

### 2. Function: ArithOp
  **Formula:** `il_sicee_base*$tscee_stdmy`
  **Output Variable:** `sin01_s`
  **Tax Unit:** `tu_individual_se`

### 3. Function: ArithOp
  **Formula:** `min(sin01_s,$tscee_coef1*$XBASMI*$tscee_stdmy)`
  **Output Variable:** `sin02_s`
  **Tax Unit:** `tu_individual_se`

### 4. Function: BenCalc
  - **comp_cond**: `sin02_s > ($tscee_coef2*$XBASM*$tscee_stdmy)`
  - **comp_perTU**: `sin02_s*$tscee_rate`
  - **round_to**: `100`
  - **output_var**: `sin03_s`
  - **TAX_UNIT**: `tu_individual_se`

### 5. Function: ArithOp
  **Formula:** `sin03_s/$tscee_stdmy`
  **Output Variable:** `tscee_s`
  **Tax Unit:** `tu_individual_se`


---

## Policy: tscer_se
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag < $tscer_maxage & il_sicer_base > amount#1`
  - **Tax Unit:** `tu_individual_se`

### 2. Function: ArithOp
  **Formula:** `il_sicer_base* $tscer_rate1
`
  **Output Variable:** `tscersi_s`
  **Tax Unit:** `tu_individual_se`

### 3. Function: ArithOp
  **Formula:** `il_sicer_base * $tscer_rate2`
  **Output Variable:** `tscerpi_s`
  **Tax Unit:** `tu_individual_se`

### 4. Function: ArithOp
  **Formula:** `il_sicer_base * $tscer_rate3
`
  **Output Variable:** `tscerci_s`
  **Tax Unit:** `tu_individual_se`

### 5. Function: ArithOp
  **Formula:** `il_sicer_base * $tscer_rate4
`
  **Output Variable:** `tscerac_s`
  **Tax Unit:** `tu_individual_se`

### 6. Function: ArithOp
  **Formula:** `il_sicer_base * $tscer_rate5
`
  **Output Variable:** `tscerir_s`
  **Tax Unit:** `tu_individual_se`

### 7. Function: ArithOp
  **Formula:** `il_sicer_base * $tscer_rate6
`
  **Output Variable:** `tscerot_s`
  **Tax Unit:** `tu_individual_se`

### 8. Function: ArithOp
  **Formula:** `il_sicer_base * $tscer_rate7
`
  **Output Variable:** `tscerml_s`
  **Tax Unit:** `tu_individual_se`

### 9. Function: BenCalc
  - **comp_cond**: `dag <=$tscer_age1 & il_sicer_base  > amount#1`
  - **comp_perTU**: `(tscersi_s +  tscerci_s + tscerac_s + tscerir_s + tscerot_s + tscerml_s)*1`
  - **#_amount**: `$tscer_minamt2`
  - **output_var**: `tscerrd_s`
  - **TAX_UNIT**: `tu_individual_se`
  - **UpLim**: `$tscer_maxamt1`

### 10. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `n/a`
  - **#_amount**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 11. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag > $tscer_ret_minage & dag < $tscer_ret_maxage & il_sicer_base > amount#1`
  - **Tax Unit:** `tu_individual_se`

### 12. Function: ArithOp *(Switch: off)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 13. Function: ArithOp
  **Formula:** `il_sicer_base * $tscer_rate8
`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_se`

### 14. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 15. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 16. Function: BenCalc *(Switch: off)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Run_Cond**: `n/a`
  - **#_VariableName**: `n/a`

### 17. Function: BenCalc *(Switch: off)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Run_Cond**: `n/a`
  - **#_VariableName**: `n/a`

### 18. Function: BenCalc *(Switch: off)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Run_Cond**: `n/a`
  - **#_VariableName**: `n/a`

### 19. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Run_Cond**: `n/a`
  - **#_VariableName**: `n/a`

### 20. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Run_Cond**: `n/a`
  - **#_VariableName**: `n/a`

### 21. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Run_Cond**: `n/a`
  - **#_VariableName**: `n/a`


---

## Policy: tscse_se
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lse>0`
  - **Tax Unit:** `tu_individual_se`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yse>yem & yse>ils_pen`
  - **Tax Unit:** `tu_individual_se`

### 3. Function: ArithOp
  **Formula:** `yse`
  **Output Variable:** `sin01_s`
  **Tax Unit:** `tu_individual_se`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `sin01_s > amount#1 & dag <=$tscse_maxage1
`
  - **Tax Unit:** `tu_individual_se`

### 5. Function: ArithOp
  **Formula:** `sin01_s* $tscse_rate1
`
  **Output Variable:** `tscsesi_s`
  **Tax Unit:** `tu_individual_se`

### 6. Function: ArithOp
  **Formula:** `sin01_s * $tscse_rate2
`
  **Output Variable:** `tscsepi_s`
  **Tax Unit:** `tu_individual_se`

### 7. Function: ArithOp
  **Formula:** `sin01_s * $tscse_rate3
`
  **Output Variable:** `tscseci_s`
  **Tax Unit:** `tu_individual_se`

### 8. Function: ArithOp
  **Formula:** `sin01_s * $tscse_rate4
`
  **Output Variable:** `tscseac_s`
  **Tax Unit:** `tu_individual_se`

### 9. Function: ArithOp
  **Formula:** `sin01_s* $tscse_rate5
`
  **Output Variable:** `tscseir_s`
  **Tax Unit:** `tu_individual_se`

### 10. Function: ArithOp
  **Formula:** `sin01_s* $tscse_rate6
`
  **Output Variable:** `tscseot_s`
  **Tax Unit:** `tu_individual_se`

### 11. Function: ArithOp
  **Formula:** `sin01_s * $tscse_rate7`
  **Output Variable:** `tscseml_s`
  **Tax Unit:** `tu_individual_se`

### 12. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `n/a`
  - **#_amount**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 13. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag > $tscse_ret_minage & dag < $tscse_ret_maxage & sin01_s > amount#1`
  - **Tax Unit:** `tu_individual_se`

### 14. Function: ArithOp *(Switch: off)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 15. Function: ArithOp
  **Formula:** `sin01_s * $tscse_rate8
`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_se`

### 16. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag > $tscse_ret_minage & sin01_s > amount#1`
  - **Tax Unit:** `tu_individual_se`

### 17. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`


---

## Policy: tin_se
### 1. Function: ArithOp
  **Formula:** `min(xpp,amount#1)`
  **Output Variable:** `tintapv_s`
  **Tax Unit:** `tu_individual_se`

### 2. Function: BenCalc
  - **comp_cond**: `il_taxabley_ppta >  ($tin_ee_thres5*$XBASM)`
  - **comp_perTU**: `($tin_ee_coef7*$XBASM)`
  - **output_var**: `tinta00_s`
  - **TAX_UNIT**: `tu_individual_se`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag >$tin_ret_minage
`
  - **Tax Unit:** `tu_individual_se`

### 4. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `il_taxabley_ppta > ($tin_ret_thres11*$XBASM) & il_taxabley_ppta <= ($tin_ret_thres12*$XBASM)`
  - **comp_perTU**: `($tin_ret_coef19*$XBASM) -$tin_ret_coef20*(il_taxabley_ppta)`
  - **output_var**: `tintape_s`
  - **TAX_UNIT**: `tu_individual_se`
  - **Comp_perTU**: `n/a`
  - **Comp_Cond**: `n/a`

### 5. Function: ArithOp
  **Formula:** `il_taxbase*$tinmu_rate`
  **Output Variable:** `tinmu_s`
  **Tax Unit:** `tu_individual_se`

### 6. Function: ArithOp
  **Formula:** `il_taxbase*$tinrg_rate`
  **Output Variable:** `tinrg_s`
  **Tax Unit:** `tu_individual_se`

### 7. Function: ArithOp
  **Formula:** `il_taxbase*$tinfu_rate`
  **Output Variable:** `tinfu_s`
  **Tax Unit:** `tu_individual_se`

### 8. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_se`
  - **Output Variable:** `tinna_s`

### 9. Function: ArithOp
  **Formula:** `xhcmomi - yiy-ypr`
  **Output Variable:** `sin01_s`
  **Tax Unit:** `tu_individual_se`

### 10. Function: BenCalc
  - **comp_cond**: `sin01_s > 0 &(sin01_s)> amount#1`
  - **comp_perTU**: `(amount#1*$tintcmi_rate1)+$tintcmi_rate2*((sin01_s)-amount#1)`
  - **#_amount**: `$tintcmi_amt`
  - **output_var**: `tintcmi_s`
  - **TAX_UNIT**: `tu_individual_se`

### 11. Function: ArithOp
  **Formula:** `(yem + yse + kfb)`
  **Output Variable:** `tintc00_s`
  **Tax Unit:** `tu_individual_se`

### 12. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag <= $tintc_ee_maxage

`
  - **Tax Unit:** `tu_individual_se`

### 13. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `tintc00_s > ($tintc_ee_addthres4*$XBASM)`
  - **comp_perTU**: `(($tin_ee_addcoef6*$XBASM)-tinta00_s)*($tinmu_rate+$tinrg_rate)`
  - **lowlim**: `0`
  - **output_var**: `tintcly_s`
  - **TAX_UNIT**: `tu_individual_se`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`

### 14. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag > $tintc_ee_maxage
`
  - **Tax Unit:** `tu_individual_se`

### 15. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_amount**: `n/a`
  - **lowlim**: `0`
  - **output_add_var**: `tintcly_s`
  - **TAX_UNIT**: `tu_individual_se`
  - **#_Amount**: `n/a`

### 16. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_amount**: ``
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 17. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_amount**: ``
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 18. Function: ArithOp
  **Formula:** `tinmu_s + tinrg_s + tinfu_s + tinna_s - tscee_s - tintcmi_s - tintcly_s - tintcdb_s`
  **Output Variable:** `tin_s`
  **Tax Unit:** `tu_individual_se`

### 19. Function: BenCalc
  - **Comp_Cond**: `pdi>=$tin_disab_addthres2*$XBASM`
  - **Comp_perTU**: `(($tin_disab_addcoef4*$XBASM*$tin_disab_addcoef5*(pdi-$tin_disab_addcoef6*$XBASM))-tinta00_s)*($tinmu_rate+$tinrg_rate)`
  - **Output_Var**: `tintcdb_s`
  - **TAX_UNIT**: `tu_individual_se`
  - **Who_Must_Be_Elig**: `one`
  - **LowLim**: `0`

### 20. Function: Elig
  **Eligibility Check:**
  - **Condition:** `pdi>0`
  - **Tax Unit:** `tu_individual_se`

### 21. Function: Elig
  **Eligibility Check:**
  - **Condition:** `il_taxbase > $tin_exempt_thres`
  - **Tax Unit:** `tu_individual_se`

### 22. Function: ArithOp
  **Formula:** `-min($tin_amt2 , max($tin_amt3,(il_taxbase-$tin_amt4)*$tin_rate6))`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_se`

### 23. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_se`
  - **Output Variable:** `tinpm_s`
    - Band: Rate=`$tinpm_rate`, Limit=``

### 24. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: tinkt_se
### 1. Function: ArithOp
  **Formula:** `max((yiy+ypr)-xhcmomi,0)`
  **Output Variable:** `sin01_s`
  **Tax Unit:** `tu_individual_se`

### 2. Function: ArithOp
  **Formula:** `sin01_s * $tintcmi_rate1
`
  **Output Variable:** `tinkt_s`
  **Tax Unit:** `tu_individual_Se`


---

## Policy: bch_se
### 1. Function: BenCalc
  - **base**: `$bch_stdamt`
  - **comp_cond**: `isNtoMchild#5 & (dag < $bch_maxage1 | dec = 2)`
  - **comp_perElig**: `$base + $bch_addamt4
`
  - **#_N**: `5`
  - **#_M**: `99`
  - **output_var**: `sin01_s`
  - **TAX_UNIT**: `tu_bch_se`

### 2. Function: BenCalc
  - **comp_cond**: `isNtoMchild#5 & dag >=  $bch_maxage1 & dag <= $bch_maxage2 & dec = 4`
  - **comp_perElig**: `$bch_addamt8`
  - **#_N**: `5`
  - **#_M**: `99`
  - **output_var**: `sin02_s`
  - **TAX_UNIT**: `tu_bch_se`

### 3. Function: BenCalc
  - **comp_cond**: `dag >=  $bch_maxage1 & dag <= $bch_maxage3 & dec = 4 & IsDepChild  `
  - **comp_perElig**: `($bch_stdamt)*$bch_redcoef
`
  - **output_var**: `sin03_s`
  - **TAX_UNIT**: `tu_bch_se`

### 4. Function: BenCalc
  - **comp_cond**: `dag =  $bch_maxage2 & dec = 4 & IsDepChild  `
  - **comp_perElig**: `($bch_stdamt)*$bch_redcoef
`
  - **output_var**: `bch02_s`
  - **TAX_UNIT**: `tu_bch_se`

### 5. Function: Allocate *(Switch: off)*
  - **share**: `sin01_s`
  - **share_between**: `IsParentOfDepChild & (dgn = 0 | !IsWithPartner)`
  - **output_var**: `bch00_s`
  - **TAX_UNIT**: `tu_bch_se`

### 6. Function: Allocate *(Switch: off)*
  - **share**: `sin02_s + sin03_s + bch02_s`
  - **share_between**: `IsParentOfDepChild & (dgn = 0 | !IsWithPartner)`
  - **output_var**: `bch01_s`
  - **TAX_UNIT**: `tu_bch_se`

### 7. Function: ArithOp
  **Formula:** `bch00_s + bch01_s`
  **Output Variable:** `bch_s`
  **Tax Unit:** `tu_individual_se`

### 8. Function: Allocate
  - **share**: `sin01_s`
  - **share_between**: `IsParentOfDepChild`
  - **output_var**: `bch00_s`
  - **TAX_UNIT**: `tu_bch_se`

### 9. Function: Allocate
  - **share**: `sin02_s + sin03_s + bch02_s`
  - **share_between**: `IsParentOfDepChild`
  - **output_var**: `bch01_s`
  - **TAX_UNIT**: `tu_bch_se`


---

## Policy: bho_se
### 1. Function: ArithOp
  **Formula:** `$bho_rate1*max(afc-amount#1,0)`
  **Output Variable:** `afc00_s`
  **Tax Unit:** `tu_bho_se`

### 2. Function: Allocate
  - **share**: `(afc00_s / $bho_stdmy)`
  - **share_between**: `IsHead | IsPartner`
  - **output_var**: `afc00_s`
  - **TAX_UNIT**: `tu_bho_se`

### 3. Function: BenCalc
  - **comp_cond**: `IsDepChild#1`
  - **comp_perTU**: `il_means_bho_prel`
  - **#_level**: `tu_bho_se`
  - **output_var**: `ychot_s`
  - **TAX_UNIT**: `tu_individual_se`

### 4. Function: BenCalc
  - **comp_cond**: `nDepChildrenInTu >=$bho_child3_coef
`
  - **comp_perTU**: `$bho_child3_stdamt`
  - **output_var**: `sin01_s`
  - **TAX_UNIT**: `tu_bho_se`

### 5. Function: BenCalc
  - **comp_cond**: `nDepChildrenInTu >=$bho_child3_coef
`
  - **comp_perTU**: `(min(xhc,amount#4)-amount#2)*$bho_coef1
`
  - **#_amount**: `$bho_amt4`
  - **lowlim**: `0`
  - **output_var**: `sin02_s`
  - **TAX_UNIT**: `tu_bho_se`

### 6. Function: BenCalc
  - **comp_cond**: `nDepChildrenInTu#1 >= 1 & !IsLoneParentOfDepChild#1 & idpartner != 0 & IsparentOfDepChild#1 & dgn = 0`
  - **comp_perTU**: `(il_means_bho - amount#2)*$bho_redcoef1

`
  - **#_level**: `tu_bho_se`
  - **#_amount**: `$bho_amt5`
  - **lowlim**: `0`
  - **output_var**: `sin03_s`
  - **TAX_UNIT**: `tu_individual_se`

### 7. Function: BenCalc
  - **comp_cond**: `nDepChildrenInTu#1 >= 1 & !IsLoneParentOfDepChild#1 & idpartner != 0 & IsparentOfDepChild#1 & dgn = 1`
  - **comp_perTU**: `(il_means_bho - amount#2)*$bho_redcoef1
`
  - **#_level**: `tu_bho_se`
  - **#_amount**: `$bho_amt5`
  - **lowlim**: `0`
  - **output_var**: `sin04_s`
  - **TAX_UNIT**: `tu_individual_se`

### 8. Function: BenCalc
  - **comp_cond**: `nDepChildrenInTu >= 1 & !IsLoneParentOfDepChild & IsHead`
  - **comp_perTU**: `sin01_s + sin02_s - sin03_s - sin04_s`
  - **output_var**: `sin05_s`
  - **TAX_UNIT**: `tu_bho_se`

### 9. Function: BenCalc
  - **comp_cond**: `nDepChildrenInTu#1 >= 1 & IsLoneParentOfDepChild#1 & IsHead#1`
  - **comp_perTU**: `sin01_s + sin02_s`
  - **#_level**: `tu_bho_se`
  - **withdraw_base**: `il_means_bho`
  - **withdraw_rate**: `$bho_redcoef2`
  - **withdraw_start**: `$bho_thres2`
  - **lowlim**: `0`
  - **output_var**: `sin06_s`
  - **TAX_UNIT**: `tu_individual_se`

### 10. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag >= $bho_minage  & dag < $bho_maxage & nDepChildrenInTu = 0`
  - **Tax Unit:** `tu_bho_se`

### 11. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `xhc >= amount#3`
  - **comp_perTU**: `(amount#2-amount#1)*0.9 + (amount#3-amount#2)*$bho_coef3
`
  - **#_amount**: `$bho_amt8`
  - **output_var**: `sin07_s`
  - **TAX_UNIT**: `tu_bho_se`

### 12. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `!IsWithPartner & IsHead`
  - **comp_perTU**: `sin07_s`
  - **withdraw_base**: `il_means_bho`
  - **withdraw_rate**: `$bho_coef4`
  - **withdraw_start**: `$bho_amt9`
  - **output_var**: `sin08_s`
  - **TAX_UNIT**: `tu_bho_se`

### 13. Function: BenCalc
  - **comp_cond**: `sin09_s#1 >= 1 & IsWithPartner & dgn = 0`
  - **comp_perTU**: `(il_means_bho - amount#2)*33%`
  - **#_level**: `tu_bho_se`
  - **#_amount**: `$bho_amt10`
  - **lowlim**: `0`
  - **output_var**: `sin10_s`
  - **TAX_UNIT**: `tu_individual_se`

### 14. Function: BenCalc
  - **comp_cond**: `sin09_s#1 >= 1 & IsWithPartner & dgn = 1`
  - **comp_perTU**: `(il_means_bho - amount#2)*33%`
  - **#_level**: `tu_bho_se`
  - **#_amount**: `$bho_amt10`
  - **lowlim**: `0`
  - **output_var**: `sin11_s`
  - **TAX_UNIT**: `tu_individual_se`

### 15. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `IsWithPartner`
  - **comp_perTU**: `sin07_s - sin10_s - sin11_s`
  - **output_var**: `sin12_s`
  - **TAX_UNIT**: `tu_bho_se`

### 16. Function: BenCalc
  - **comp_cond**: `xhc = 0`
  - **comp_perTU**: `0`
  - **threshold**: `$bho_minamt`
  - **output_var**: `bho_s`
  - **TAX_UNIT**: `tu_bho_se`

### 17. Function: ArithOp
  **Formula:** `sin05_s + (sin05_s * $bho_supplcoef2*  $bho_my1)`
  **Output Variable:** `sin05_s`
  **Tax Unit:** `tu_bho_se`

### 18. Function: ArithOp
  **Formula:** `sin06_s + (sin06_s * $bho_supplcoef2 * $bho_my1)`
  **Output Variable:** `sin06_s`
  **Tax Unit:** `tu_bho_se`


---

## Policy: bhope_se
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsHead & IsWithPartner`
  - **Tax Unit:** `tu_bho_se`

### 2. Function: ArithOp
  **Formula:** `$bhope_rate1*max(afc#2-amount#1,0)`
  **Output Variable:** `afc00_s`
  **Tax Unit:** `tu_individual_se`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsHead & !IsWithPartner`
  - **Tax Unit:** `tu_bho_se`

### 4. Function: ArithOp
  **Formula:** `$bhope_rate2*max(afc#2-amount#1,0)`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_se`

### 5. Function: Allocate
  - **share**: `(afc00_s / $bhope_stdmy)`
  - **share_between**: `IsHead | IsPartner`
  - **output_var**: `afc00_s`
  - **TAX_UNIT**: `tu_bho_se`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(dag > $bhope_ret_minage | pdi > 0) & (IsHead#1 | IsPartner#1)`
  - **Tax Unit:** `tu_individual_se`

### 7. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `pdi = 0 & dag > $bhope_disab_age8 & IsWithPartner`
  - **comp_perTU**: `$bhope_disab_coef9*$XBASM`
  - **output_var**: `ydg01_s`
  - **TAX_UNIT**: `tu_individual_se`

### 8. Function: BenCalc
  - **comp_cond**: `IsDepChild#1`
  - **comp_perTU**: `i_means_bhope_prel`
  - **#_level**: `tu_bho_se`
  - **output_var**: `ychot_s`
  - **TAX_UNIT**: `tu_individual_se`

### 9. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `dag <=$bhope_ret_minage & pdi > 0`
  - **comp_perTU**: `$bhope_disab_coef10*min(xhc#1-bho_s#1,amount#3)+$bhope_disab_coef11*max(min(xhc#1-bho_s#1,amount#5)-amount#3,0)`
  - **#_level**: `tu_bho_se`
  - **#_amount**: `$bhope_amt2`
  - **lowlim**: `0`
  - **output_var**: `sin01_s`
  - **TAX_UNIT**: `tu_individual_se`
  - **Comp_Cond**: `dag >$bhope_ret_minage & !IsWithPartner`
  - **Comp_perTU**: `$bhope_ret_coef6*min(xhc#1-bho_s#1,amount#2)+$bhope_ret_coef7*max(min(xhc#1-bho_s#1,amount#3)-amount#2,0)+$bhope_ret_coef8*max(min(xhc#1-bho_s#1,amount#4)-amount#3,0)+$bhope_ret_coef9*max(min(xhc#1-bho_s#1,amount#5)-amount#4,0)+$bhope_ret_coef10
`
  - **#_Amount**: `$bhope_amt4`

### 10. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `sin01_s#1 > 0`
  - **comp_perElig**: `1`
  - **#_level**: `tu_individual_se`
  - **output_var**: `sin04_s`
  - **TAX_UNIT**: `tu_bho_se`

### 11. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `IsWithPartner & sin04_s#1 < 2`
  - **comp_perTU**: `sin01_s`
  - **#_level**: `tu_bho_se`
  - **output_var**: `sin01_s`
  - **TAX_UNIT**: `tu_individual_se`

### 12. Function: BenCalc
  - **comp_cond**: `!IsWithPartner`
  - **comp_perTU**: `sin01_s`
  - **output_var**: `sin01_s`
  - **TAX_UNIT**: `tu_individual_se`

### 13. Function: Allocate
  - **share**: `il_means_bhope`
  - **share_between**: `IsHead | IsPartner`
  - **output_var**: `sin02_s`
  - **TAX_UNIT**: `tu_bho_se`

### 14. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `(sin02_s >= $XBASM) & (pdi > 0)`
  - **comp_perTU**: `max(sin01_s-($XBASM *$bhope_ret_coef11)-((sin02_s-$XBASM )*$bhope_ret_coef12),0)`
  - **threshold**: `$bhope_minamt`
  - **output_var**: `bhope_s`
  - **TAX_UNIT**: `tu_individual_se`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`

### 15. Function: Allocate
  - **share**: `xhc`
  - **output_var**: `sin03_s`
  - **TAX_UNIT**: `tu_bho_se`

### 16. Function: BenCalc
  - **comp_cond**: `sin03_s = 0`
  - **comp_perTU**: `0`
  - **threshold**: `$bhope_minamt`
  - **output_var**: `bhope_s`
  - **TAX_UNIT**: `tu_individual_se`

### 17. Function: DefVar
  - **i_means_bhope_prel**: `0`

### 18. Function: BenCalc
  - **Comp_Cond**: `dag>$bhope_ret_minage
`
  - **Comp_perTU**: `il_means_bhope_prel_64+0.93*max(yem+yemmc_s+bwkmcee_s+yse-24000,0)`
  - **Output_Var**: `i_means_bhope_prel`
  - **TAX_UNIT**: `tu_individual_se`

### 19. Function: DefIl
  - **name**: `il_means_bhope`
  - **il_means_bhope_prel**: `n/a`
  - **ychot_s**: `-`
  - **i_means_bhope_prel**: `+`


---

## Policy: bsamt_se
### 1. Function: BenCalc
  - **comp_cond**: `IsHead & IsWithPartner`
  - **comp_perElig**: `$bsamt_ChildCouple_amt1`
  - **output_var**: `sin01_s`
  - **TAX_UNIT**: `tu_bho_se`
  - **Comp_Cond**: `IsDepChild & dag =$bsamt_child_age13 & dec=4`
  - **Comp_perElig**: `$bsamt_child_amt8`

### 2. Function: BenCalc
  - **comp_cond**: `NPersInUnit >= $bsamt_coef7`
  - **comp_perTU**: `$bsamt_amt7`
  - **output_var**: `sin02_s`
  - **TAX_UNIT**: `tu_bho_se`

### 3. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **threshold**: `n/a`
  - **lowlim**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 4. Function: Allocate
  - **share**: `bsamt_s`
  - **share_between**: `IsHead | IsPartner`
  - **output_var**: `bsamt_s`
  - **TAX_UNIT**: `tu_bho_se`

### 5. Function: BenCalc
  - **comp_cond**: `xhc = 0`
  - **comp_perTU**: `0`
  - **threshold**: `$bsamt_amt8`
  - **lowlim**: `0`
  - **output_var**: `i_bsa01`
  - **TAX_UNIT**: `tu_bho_se`

### 6. Function: BenCalc
  - **comp_cond**: `xhc = 0`
  - **comp_perTU**: `0`
  - **threshold**: `$bsamt_amt8`
  - **lowlim**: `0`
  - **output_var**: `i_bsa02`
  - **TAX_UNIT**: `tu_bho_se`

### 7. Function: DefVar
  - **i_bsa01**: `0`
  - **i_bsach**: `0`
  - **i_bsa02**: `0`

### 8. Function: ArithOp
  **Formula:** `i_bsa01*6/12 + i_bsa02*6/12`
  **Output Variable:** `bsamt_s`
  **Tax Unit:** `tu_bho_se`

### 9. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `(i_bsamt_cumpers > $bsamt_target_count & bsamtyn_a = -1)  | bsamtyn_a = 0`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bsamt_s`
  - **TAX_UNIT**: `tu_individual_se`

### 10. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsamt_elig`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsamt_sort`
  - **OutputVar**: `i_bsamt_cumpers`
  - **TAX_UNIT**: `tu_individual_se`

### 11. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsamt_target_count`: $sum_i_bsamt_elig * $bsamt_rate

### 12. Function: Totals *(Switch: off)*
  - **Agg**: `i_bsamt_elig`
  - **Use_Weights**: `yes`
  - **Varname_Sum**: `$sum`
  - **TAX_UNIT**: `tu_individual_se`

### 13. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsamt_rate`: min($bsamt_BCA_rate,$bsamt_BTA_rate)

### 14. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsamt_BCA_rate`: 0.3698

### 15. Function: Totals *(Switch: off)*
  - **Agg**: `n/a`
  - **Use_Weights**: `n/a`
  - **Varname_Sum**: `n/a`
  - **TAX_UNIT**: `n/a`

### 16. Function: DefVar *(Switch: off)*
  - **i_bsamt_bca_take**: `n/a`

### 17. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `n/a`
  - **SummingWeighted**: `n/a`
  - **SortingVar**: `n/a`
  - **OutputVar**: `n/a`
  - **TAX_UNIT**: `n/a`

### 18. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsamt_targetBCA_amt`: n/a

### 19. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `bsamt_s >= $bsamt_minamt`
  - **Comp_perTU**: `1`
  - **Comp_perElig**: `i_bsamt_sort`
  - **Output_Var**: `i_bsamt_sort`
  - **TAX_UNIT**: `tu_individual_se`

### 20. Function: DefVar *(Switch: off)*
  - **i_bsamt_sort**: `i_bsamt_rand`
  - **i_bsamt_amt**: `bsamt_s`
  - **i_bsamt_elig**: `bsamt_s > 0`
  - **i_bsamt_cumexp**: `0`
  - **i_bsamt_cumpers**: `0`

### 21. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsamt_minamt`: 0

### 22. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsamt_BTA_rate`: 1


---

## Policy: output_std_se
### 1. Function: DefOutput
  - **file**: `SE_2025_std`
  - **vargroup**: `x*`
  - **ilgroup**: `il_*`
  - **UnitInfo_TU**: `tu_bho_se`
  - **UnitInfo_id**: `IsPartner`
  - **nDecimals**: `2`
  - **TAX_UNIT**: `tu_individual_se`
  - **Var**: `liwmy`
  - **VarGroup**: `i*`


---

## Policy: output_std_hh_se *(Switch: off)*
### 1. Function: DefOutput
  - **file**: `SE_2025_std_hh`
  - **var**: `dwt`
  - **ilgroup**: `ils_*`
  - **TAX_UNIT**: `tu_household_se`


---

## Policy: setdefault_se
### 1. Function: SetDefault
  - **Dataset**: `se_20??_*`
  - **yempv_a**: `0`
  - **liwmy_a**: `0`
  - **lnu**: `0`
  - **bunct_s**: `0`
  - **yempv**: `0`
  - **ysepv_a**: `0`
  - **yptmp**: `0`
  - **lhwsr_a**: `0`
  - **bwkmcmy_a**: `0`
  - **lmc**: `0`
  - **yemmy_a**: `0`
  - **lhw_a**: `0`
  - **yem_a**: `0`
  - **lma**: `0`
  - **yem20_a**: `0`

### 2. Function: SetDefault
  - **Dataset**: `se_2007_*`
  - **ydses_o**: `0`
  - **kfbcc**: `0`
  - **ate**: `0`
  - **aco**: `0`
  - **aca**: `0`

### 3. Function: SetDefault
  - **Dataset**: `se_2008_*`
  - **ydses_o**: `0`
  - **kfbcc**: `0`
  - **ate**: `0`
  - **aco**: `0`
  - **aca**: `0`

### 4. Function: SetDefault
  - **Dataset**: `se_2010_*`
  - **ate**: `0`
  - **aco**: `0`
  - **aca**: `0`

### 5. Function: SetDefault
  - **Dataset**: `*training_data`
  - **bpa_s**: `0`
  - **bfapl_s**: `0`
  - **dmb**: `6`
  - **lcb_a**: `0`
  - **ltr**: `0`
  - **ymwdt**: `0`
  - **bfa**: `0`
  - **bsamt**: `bsa`
  - **bsanm**: `0`
  - **bunct**: `bun`
  - **bunnc**: `0`
  - **bch00**: `0`
  - **bunctmy**: `bunmy`
  - **xed00**: `0`
  - **xhl00**: `0`
  - **kivho**: `0`

### 6. Function: DefVar
  - **i_mc_rand_1**: `0`
  - **i_mc_rand_2**: `0`
  - **i_mc_rand_3**: `0`

### 7. Function: SetDefault
  - **Dataset**: `*training_data`
  - **yemmc_s**: `0`
  - **bwkmcee_s**: `0`
  - **lhwsr_s**: `0`
  - **bwkmceemy_s**: `0`
  - **yemmwmy_s**: `0`
  - **lhwsr02_s**: `0`
  - **yemmw_s**: `0`

### 8. Function: SetDefault *(Switch: n/a)*
  - **Dataset**: `n/a`
  - **Run_Cond**: `n/a`
  - **#_VariableName**: `n/a`
  - **tscerci_s**: `n/a`
  - **tscerot_s**: `n/a`
  - **tscerml_s**: `n/a`
  - **tscerac_s**: `n/a`
  - **tscersi_s**: `n/a`
  - **tscerir_s**: `n/a`

### 9. Function: SetDefault
  - **Dataset**: `se_20*`
  - **ydsyc_a**: `0`

### 10. Function: SetDefault
  - **Dataset**: `*`
  - **bsamtyn_a**: `-1`

### 11. Function: DefIl
  - **Run_Cond**: `IsUsedDatabase#1`
  - **#_DataBasename**: `se_20??_??_????_??_??`
  - **Name**: `il_xs_hl06`
  - **Warn_If_NonMonetary**: `no`
  - **RegExp_Def**: `xs06[0-9]+`
  - **RegExp_Factor**: `+`

### 12. Function: ArithOp
  **Formula:** `il_xs_hl06 * yds`
  **Output Variable:** `xhl00`
  **Tax Unit:** `tu_individual_se`
  **Run Condition:** `IsUsedDatabase#1`

### 13. Function: DefIl
  - **Run_Cond**: `IsUsedDatabase#1`
  - **#_DataBasename**: `se_20??_??_????_??_??`
  - **Name**: `il_xs_hl10`
  - **Warn_If_NonMonetary**: `no`
  - **RegExp_Def**: `xs10[0-9]+`
  - **RegExp_Factor**: `+`

### 14. Function: ArithOp
  **Formula:** `il_xs_hl10 * yds`
  **Output Variable:** `xed00`
  **Tax Unit:** `tu_individual_se`
  **Run Condition:** `IsUsedDatabase#1`


---

## Policy: bunct_se *(Switch: off)*
### 1. Function: ArithOp
  **Formula:** `max(lunmy,bunmy)`
  **Output Variable:** `lunmy_s`
  **Tax Unit:** `tu_individual_se`

### 2. Function: BenCalc
  - **comp_cond**: `lunmy_s > 0 & bunct = 0`
  - **comp_perElig**: `0`
  - **output_var**: `liwmy_s`
  - **TAX_UNIT**: `tu_individual_se`
  - **Who_Must_Be_Elig**: `one`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lunmy_s > 0 & liwmy_s >= $UB_QperMin & dag >= $bunct_minage
 & dag<$bunct_maxage
`
  - **Tax Unit:** `tu_individual_se`

### 4. Function: ArithOp
  **Formula:** `lunmy_s`
  **Output Variable:** `bunmy_s`
  **Tax Unit:** `tu_individual_se`

### 5. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `lunmy_s > 0 & bunct = 0`
  - **comp_perElig**: `0`
  - **output_var**: `yempv_s`
  - **TAX_UNIT**: `tu_individual_se`
  - **Comp_perElig**: `yivwg * $fthw  * $bunct_coef3
`
  - **Comp_Cond**: `lunmy_s > 0 & bunct> 0 & $ImputedWage=1`

### 6. Function: DefVar
  - **i_bun01**: `0`
  - **i_bun02**: `0`
  - **i_bun03**: `0`
  - **i_bun04**: `0`
  - **i_ftprop**: `0`

### 7. Function: ArithOp
  **Formula:** `yempv_s*$bunct_rate1
`
  **Output Variable:** `i_bun01`
  **Tax Unit:** `tu_individual_se`

### 8. Function: ArithOp
  **Formula:** `yempv_s*$bunct_rate1
`
  **Output Variable:** `i_bun02`
  **Tax Unit:** `tu_individual_se`

### 9. Function: BenCalc
  - **Comp_Cond**: `yempv>0`
  - **Comp_perElig**: `yempv`
  - **Output_Var**: `yempv`
  - **TAX_UNIT**: `tu_individual_se`

### 10. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lunmy_s > 0`
  - **Tax Unit:** `tu_individual_se`

### 11. Function: ArithOp
  **Formula:** `yempv_s*$bunct_rate2`
  **Output Variable:** `i_bun03`
  **Tax Unit:** `tu_individual_se`

### 12. Function: ArithOp
  **Formula:** `yempv_s*$bunct_rate3`
  **Output Variable:** `i_bun04`
  **Tax Unit:** `tu_individual_se`

### 13. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `bunct`
  **Tax Unit:** `tu_individual_se`

### 14. Function: BenCalc
  - **Comp_Cond**: `lnu > 0 & lhw_a > $bunct_thres1
`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_ftprop`
  - **TAX_UNIT**: `tu_individual_se`

### 15. Function: BenCalc
  - **Output_Var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_se`
  - **Comp_perTU**: `(i_bun01*min(bunmy_s,4)+i_bun02*min(max(bunmy_s-4,0),5)+i_bun03*min(max(bunmy_s-9,0),3))/$bunct_stdmy`
  - **Comp_Cond**: `!IsParent | IsParent`
  - **Who_Must_Be_Elig**: `one`

### 16. Function: BenCalc
  - **Comp_Cond**: `yempv_s=0  & ysepv_a=0`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_se`
  - **Who_Must_Be_Elig**: `one`

### 17. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bunmy>0 & liwwh12_h>=$UB_QperMin & dag>=$bunct_minage
 & dag<$bunct_maxage
`
  - **Tax Unit:** `tu_individual_se`

### 18. Function: ArithOp
  **Formula:** `yempv*$bunct_rate1
`
  **Output Variable:** `i_bun01`
  **Tax Unit:** `tu_individual_se`

### 19. Function: ArithOp
  **Formula:** `yempv*$bunct_rate1
`
  **Output Variable:** `i_bun02`
  **Tax Unit:** `tu_individual_se`

### 20. Function: ArithOp
  **Formula:** `yempv*$bunct_rate2`
  **Output Variable:** `i_bun03`
  **Tax Unit:** `tu_individual_se`

### 21. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `{lim_h =1}&{IsParent}`
  - **Comp_perTU**: `(i_bun01*min(bunmy,4)+i_bun02*min(max(bunmy-4,0),4)+i_bun03*min(max(bunmy-8,0),4))/$bunct_stdmy
`
  - **Output_Var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_se`

### 22. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `lim_h=1  & bunmy > 8`
  - **Comp_perTU**: `i_bun03`
  - **Output_Var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_se`


---

## Policy: IlsDef_se
### 1. Function: DefIl
  - **name**: `ils_origy`
  - **yem**: `+`
  - **yiy**: `+`
  - **yot**: `+`
  - **ypr**: `+`
  - **ypp**: `+`
  - **ypt**: `+`
  - **yse**: `+`
  - **xmp**: `-`
  - **yemmc_s**: `+`

### 2. Function: DefIl
  - **name**: `ils_pen`
  - **poa**: `+`
  - **pdi**: `+`
  - **psu**: `+`

### 3. Function: DefIl
  - **name**: `ils_origrepy`
  - **ils_origy**: `+`
  - **ils_pen**: `+`
  - **bunct_s**: `+`
  - **bhl**: `+`
  - **bpl**: `+`
  - **bunct**: `+`
  - **bunnc**: `+`
  - **bwkmcee_s**: `+`

### 4. Function: DefIl
  - **name**: `ils_earns`
  - **yem**: `+`
  - **yse**: `+`
  - **yemmc_s**: `+`

### 5. Function: DefIl
  - **name**: `ils_bennt`
  - **bunct_s**: `+`
  - **bhl**: `+`
  - **bed**: `+`
  - **bpl**: `+`
  - **bch_s**: `+`
  - **bunct**: `+`
  - **bpa_s**: `+`
  - **bfapl_s**: `+`
  - **bsanm**: `+`
  - **bunnc**: `+`
  - **bwkmcee_s**: `+`

### 6. Function: DefIl
  - **name**: `ils_tax`
  - **ils_taxin**: `+`
  - **ils_taxwl**: `+`

### 7. Function: DefIl
  - **name**: `ils_sicee`
  - **tscee_s**: `+`

### 8. Function: DefIl
  - **name**: `ils_sicse`
  - **tscsesi_s**: `+`
  - **tscsepi_s**: `+`
  - **tscseci_s**: `+`
  - **tscseac_s**: `+`
  - **tscseir_s**: `+`
  - **tscseot_s**: `+`
  - **tscseml_s**: `+`

### 9. Function: DefIl
  - **name**: `ils_sicer`
  - **tscersi_s**: `+`
  - **tscerpi_s**: `+`
  - **tscerci_s**: `+`
  - **tscerac_s**: `+`
  - **tscerir_s**: `+`
  - **tscerot_s**: `+`
  - **tscerml_s**: `+`
  - **tscerrd_s**: `-`

### 10. Function: DefIl
  - **name**: `ils_sicct`

### 11. Function: DefIl
  - **name**: `ils_benmt`
  - **bho_s**: `+`
  - **bhope_s**: `+`
  - **bsamt_s**: `+`

### 12. Function: DefIl
  - **name**: `ils_ben`
  - **ils_pen**: `+`
  - **ils_benmt**: `+`
  - **ils_bennt**: `+`

### 13. Function: DefIl
  - **name**: `ils_dispy`
  - **ils_origy**: `+`
  - **ils_ben**: `+`
  - **ils_tax**: `-`
  - **ils_sicdy**: `-`

### 14. Function: DefIl
  - **name**: `ils_bensim`
  - **bho_s**: `+`
  - **bhope_s**: `+`
  - **bsamt_s**: `+`
  - **bch_s**: `+`
  - **bunct_s**: `+`
  - **bwkmcee_s**: `+`

### 15. Function: DefIl
  - **name**: `ils_taxsim`
  - **tin_s**: `+`
  - **tinkt_s**: `+`

### 16. Function: DefIl
  - **Name**: `ils_b1_bho`
  - **bho_s**: `+`
  - **bhope_s**: `+`

### 17. Function: DefIl
  - **Name**: `ils_b1_bfa`
  - **ils_b1_bcb**: `+`
  - **bch_s**: `+`

### 18. Function: DefIl
  - **Name**: `ils_b1_bsa`
  - **bsamt_s**: `+`
  - **bsanm**: `+`

### 19. Function: DefIl
  - **Name**: `ils_b1_bed`
  - **bed**: `+`

### 20. Function: DefIl
  - **Name**: `ils_b1_bhl`
  - **bhl**: `+`

### 21. Function: DefIl
  - **Name**: `ils_b1_bun`
  - **bunct_s**: `+`
  - **bunct**: `+`
  - **bunnc**: `+`
  - **bwkmcee_s**: `+`

### 22. Function: DefIl
  - **Name**: `ils_b1_bdi`
  - **pdi**: `+`

### 23. Function: DefIl
  - **Name**: `ils_b1_bsu`
  - **psu**: `+`

### 24. Function: DefIl
  - **Name**: `ils_b1_boa`
  - **poa**: `+`

### 25. Function: DefIl
  - **Name**: `ils_b2_penhl`
  - **bhl**: `+`
  - **ils_pen**: `+`

### 26. Function: DefIl
  - **Name**: `ils_b2_bsaho`
  - **bsamt_s**: `+`
  - **bhope_s**: `+`
  - **bho_s**: `+`
  - **bsanm**: `+`

### 27. Function: DefIl
  - **Name**: `ils_b2_bfaed`
  - **ils_b1_bfa**: `+`
  - **bed**: `+`

### 28. Function: DefIl
  - **Name**: `ils_sicot`

### 29. Function: DefIl
  - **name**: `ils_sicdy`
  - **ils_sicee**: `+`
  - **ils_sicse**: `+`
  - **ils_sicot**: `+`

### 30. Function: DefIl
  - **name**: `ils_base_tin`
  - **yem**: `+`
  - **kfb**: `+`
  - **yse**: `+`
  - **yot**: `+`
  - **ypp**: `+`
  - **bunct_s**: `+`
  - **poa**: `+`
  - **pdi**: `+`
  - **psu**: `+`
  - **bhl**: `+`
  - **bpl**: `+`
  - **yselo_s**: `+`
  - **bunct**: `+`
  - **bunnc**: `+`
  - **yemmc_s**: `+`
  - **bfapl_s**: `+`
  - **bpa_s**: `+`
  - **bwkmcee_s**: `+`

### 31. Function: DefIl
  - **Name**: `ils_base_tinkt`
  - **ypr**: `+`
  - **yiy**: `+`

### 32. Function: DefIl
  - **Name**: `ils_b1_bcb`
  - **bpa_s**: `+`
  - **bfapl_s**: `+`
  - **bpl**: `+`

### 33. Function: DefIl
  - **Name**: `ils_b1_bwk`

### 34. Function: DefIl
  - **Name**: `ils_b2_bunwk`
  - **ils_b1_bwk**: `+`
  - **ils_b1_bun**: `+`

### 35. Function: DefIl
  - **Name**: `ils_taxin`
  - **tin_s**: `+`
  - **tinkt_s**: `+`

### 36. Function: DefIl
  - **Name**: `ils_taxwl`
  - **tpr**: `+`


---

## Policy: IlsUDBdef_se
### 1. Function: DefIl
  - **Name**: `ils_udb_boa`
  - **poa**: `+`

### 2. Function: DefIl
  - **Name**: `ils_udb_bsu`
  - **psu**: `+`

### 3. Function: DefIl
  - **Name**: `ils_udb_bdi`
  - **pdi**: `+`

### 4. Function: DefIl
  - **Name**: `ils_udb_bun`
  - **bunct_s**: `+`
  - **bunct**: `+`
  - **bunnc**: `+`
  - **bwkmcee_s**: `+`

### 5. Function: DefIl
  - **Name**: `ils_udb_bhl`
  - **bhl**: `+`

### 6. Function: DefIl
  - **Name**: `ils_udb_bed`
  - **bed**: `+`

### 7. Function: DefIl
  - **Name**: `ils_udb_bsa`
  - **bsamt_s**: `+`
  - **bsanm**: `+`

### 8. Function: DefIl
  - **Name**: `ils_udb_bfa`
  - **bpl**: `+`
  - **bch_s**: `+`
  - **bpa_s**: `+`
  - **bfapl_s**: `+`

### 9. Function: DefIl
  - **Name**: `ils_udb_bho`
  - **bho_s**: `+`
  - **bhope_s**: `+`

### 10. Function: DefIl
  - **Name**: `ils_udb_tis`
  - **tin_s**: `+`
  - **tinkt_s**: `+`
  - **tscee_s**: `+`
  - **tscsesi_s**: `+`
  - **tscsepi_s**: `+`
  - **tscseci_s**: `+`
  - **tscseac_s**: `+`
  - **tscseir_s**: `+`
  - **tscseot_s**: `+`
  - **tscseml_s**: `+`

### 11. Function: DefIl
  - **Name**: `ils_udb_tpr`
  - **tpr**: `+`

### 12. Function: DefIl
  - **Name**: `ils_udb_yem`
  - **yem**: `+`
  - **yemmc_s**: `+`

### 13. Function: DefIl
  - **Name**: `ils_udb_yse`
  - **yse**: `+`

### 14. Function: DefIl
  - **Name**: `ils_udb_yds`
  - **ils_udb_yem**: `+`
  - **ils_udb_yse**: `+`
  - **ils_udb_ypp**: `+`
  - **ils_udb_ypr**: `+`
  - **ils_udb_yiy**: `+`
  - **ils_udb_ypt**: `+`
  - **ils_udb_yot**: `+`
  - **ils_udb_kfbcc**: `+`
  - **ils_udb_boa**: `+`
  - **ils_udb_bsu**: `+`
  - **ils_udb_bdi**: `+`
  - **ils_udb_bun**: `+`
  - **ils_udb_bhl**: `+`
  - **ils_udb_bed**: `+`
  - **ils_udb_bsa**: `+`
  - **ils_udb_bfa**: `+`
  - **ils_udb_bho**: `+`
  - **ils_udb_tis**: `-`
  - **ils_udb_xmp**: `-`
  - **ils_udb_tpr**: `-`

### 15. Function: DefIl
  - **Name**: `ils_udb_ypp`
  - **ypp**: `+`

### 16. Function: DefIl
  - **Name**: `ils_udb_ypr`
  - **ypr**: `+`

### 17. Function: DefIl
  - **Name**: `ils_udb_yiy`
  - **yiy**: `+`

### 18. Function: DefIl
  - **Name**: `ils_udb_ypt`
  - **ypt**: `+`

### 19. Function: DefIl
  - **Name**: `ils_udb_yot`
  - **yot**: `+`

### 20. Function: DefIl
  - **Name**: `ils_udb_kfbcc`
  - **kfb**: `+`

### 21. Function: DefIl
  - **Name**: `ils_udb_xmp`
  - **xmp**: `+`


---

## Policy: bfapl_se *(Switch: switch)*
### 1. Function: DefVar
  - **i_elparent_bfapl**: `0`
  - **Var_Monetary**: `yes`
  - **i_elchild_bfapl**: `0`
  - **i_agedays_bfapl**: `0`
  - **i_nelchildren_bfapl**: `0`
  - **i_durdays_bfapl_head**: `0`
  - **i_bfapl_head**: `0`
  - **i_durdays_bfapl_partner**: `0`
  - **i_elpartner_bfapl**: `0`
  - **i_bfapl_partner**: `0`
  - **i_ils_earns_mx**: `0`

### 2. Function: DefTu
  - **Type**: `SUBGROUP`
  - **Name**: `tu_bfapl_se`
  - **Members**: `Partner & OwnDepChild & LooseDepChild`
  - **PartnerCond**: `Default`
  - **DepChildCond**: `Default & dag<1`
  - **ExtHeadCond**: `IsParentOfDepChild & (dgn = 0 | (dgn = 1 & idpartner = 0))`
  - **StopIfNoHeadFound**: `no`
  - **LoneParentCond**: `Default`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsHeadOfTu#1 & IsParentOfDepChild#1`
  - **Tax Unit:** `tu_individual_se`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsDepChild#1`
  - **Tax Unit:** `tu_individual_se`

### 5. Function: ArithOp
  **Formula:** `nDepChildrenInTu#1`
  **Output Variable:** `i_nelchildren_bfapl`
  **Tax Unit:** `tu_individual_se`

### 6. Function: BenCalc
  - **Comp_Cond**: `i_elchild_bfapl=1 & dag=$bfapl_child_age1
`
  - **Comp_perTU**: `($bfapl_stdmy-dmb)*$bfapl_coef1
`
  - **Output_Var**: `i_agedays_bfapl`
  - **TAX_UNIT**: `tu_individual_se`

### 7. Function: BenCalc
  - **Comp_Cond**: `i_elchild_bfapl=1 & i_agedays_bfapl>=$bfapl_child_age2
 & dag=$bfapl_child_age1
 & i_nelchildren_bfapl#1>1 & (GetMotherInfo#1=0 | GetFatherInfo#1=0)`
  - **Comp_perTU**: `$bfapl_single_amt1+$bfapl_single_amt3`
  - **Output_Var**: `i_durdays_bfapl_head`
  - **TAX_UNIT**: `tu_individual_se`
  - **Comp_UpLim**: `$bfapl_single_amt2+i_agedays_bfapl`
  - **Comp_LowLim**: `0`
  - **#_Level**: `tu_bfapl_se`
  - **#_Info**: `idpartner`

### 8. Function: BenCalc
  - **Comp_Cond**: `i_nelchildren_bfapl>0`
  - **Comp_perTU**: `i_durdays_bfapl_head/i_nelchildren_bfapl`
  - **Output_Var**: `i_durdays_bfapl_head`
  - **TAX_UNIT**: `tu_bfapl_se`

### 9. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bfapl=1 & idpartner>0`
  - **Comp_perTU**: `$bfapl_couple_rate1*(i_ils_earns_mx/$bfapl_coef1)*$bfapl_couple_coef1*min(i_durdays_bfapl_head,$bfapl_couple_amt5)`
  - **Output_Var**: `i_bfapl_head`
  - **TAX_UNIT**: `tu_individual_se`
  - **Comp_UpLim**: `$bfapl_couple_lim*$XBASM`
  - **#_Amount**: `$bfapl_couple_amt6`
  - **LowLim**: `Amount#1*min(i_durdays_bfapl_head,$bfapl_couple_amt5)`

### 10. Function: ArithOp
  **Formula:** `(i_bfapl_head + i_bfapl_partner)/$bfapl_stdmy`
  **Output Variable:** `bfapl_s`
  **Tax Unit:** `tu_individual_se`

### 11. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsPartner#1 & IsParentOfDepChild#1`
  - **Tax Unit:** `tu_individual_se`

### 12. Function: BenCalc
  - **Comp_Cond**: `i_elchild_bfapl=1 & i_agedays_bfapl>=$bfapl_child_age2 & dag=$bfapl_child_age1 & i_nelchildren_bfapl#1>=1 & GetMotherInfo#1>0 & GetFatherInfo#1>0`
  - **Comp_perTU**: `$bfapl_couple_amt4`
  - **Output_Var**: `i_durdays_bfapl_partner`
  - **TAX_UNIT**: `tu_individual_se`
  - **Comp_UpLim**: `i_agedays_bfapl`
  - **Comp_LowLim**: `0`
  - **#_Level**: `tu_bfapl_se`
  - **#_Info**: `idpartner`

### 13. Function: Allocate
  - **Share**: `i_durdays_bfapl_partner`
  - **Output_Var**: `i_durdays_bfapl_partner`
  - **TAX_UNIT**: `tu_bfapl_se`
  - **Share_Between**: `i_nelchildren_bfapl>0 & IsPartner & IsParentOfDepChild`

### 14. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bfapl=1 & idpartner>0 & i_durdays_bfapl_head>$bfapl_couple_amt5`
  - **Comp_perTU**: `Amount#1*(i_durdays_bfapl_head-$bfapl_couple_amt6)`
  - **Output_Add_Var**: `i_bfapl_head`
  - **TAX_UNIT**: `tu_individual_se`
  - **#_Amount**: `$bfapl_couple_amt7`

### 15. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `bpl`
  **Tax Unit:** `tu_individual_se`

### 16. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bfapl=1 & idpartner=0`
  - **Comp_perTU**: `$bfapl_single_rate1*(i_ils_earns_mx/$bfapl_coef1)*$bfapl_single_coef1*min(i_durdays_bfapl_head,$bfapl_single_amt5)`
  - **Output_Add_Var**: `i_bfapl_head`
  - **TAX_UNIT**: `tu_individual_se`
  - **Comp_UpLim**: `$bfapl_single_lim*$XBASM`
  - **#_Amount**: `$bfapl_single_amt6`
  - **LowLim**: `Amount#1*min(i_durdays_bfapl_head,$bfapl_single_amt5)`

### 17. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bfapl=1 & idpartner=0 & i_durdays_bfapl_head>$bfapl_single_amt5
`
  - **Comp_perTU**: `Amount#1*(i_durdays_bfapl_head-$bfapl_single_amt5)`
  - **Output_Add_Var**: `i_bfapl_head`
  - **TAX_UNIT**: `tu_individual_se`
  - **#_Amount**: `$bfapl_single_amt7`

### 18. Function: BenCalc
  - **Comp_Cond**: `i_nelchildren_bfapl>0`
  - **Comp_perTU**: `i_durdays_bfapl_partner/i_nelchildren_bfapl`
  - **Output_Var**: `i_durdays_bfapl_partner`
  - **TAX_UNIT**: `tu_bfapl_se`

### 19. Function: BenCalc
  - **Comp_Cond**: `i_elpartner_bfapl=1`
  - **Comp_perTU**: `$bfapl_single_rate1*(i_ils_earns_mx/$bfapl_coef1)*$bfapl_single_coef1*i_durdays_bfapl_partner`
  - **Output_Add_Var**: `i_bfapl_partner`
  - **TAX_UNIT**: `tu_individual_se`
  - **#_Amount**: `$bfapl_couple_amt6`
  - **Comp_UpLim**: `$bfapl_couple_lim*$XBASM`
  - **LowLim**: `Amount#1*i_durdays_bfapl_partner`

### 20. Function: BenCalc
  - **Comp_Cond**: `yemmy=0 & ysemy>0`
  - **Comp_perTU**: `(yse*$bfapl_stdmy)/ysemy`
  - **Output_Var**: `i_ils_earns_mx`
  - **TAX_UNIT**: `tu_individual_se`


---

## Policy: bpa_se *(Switch: switch)*
### 1. Function: DefVar
  - **i_elparent_bpa**: `0`
  - **i_amount_bpa**: `0`
  - **Var_Monetary**: `no`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsPartner#1 & IsParentOfDepChild#1`
  - **Tax Unit:** `tu_individual_se`

### 3. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bpa=1 & i_ils_earns_mx>0`
  - **Comp_perTU**: `$bpa_coef1* $bpa_rate*(i_ils_earns_mx/$bpa_coef2)*$bpa_maxamt
`
  - **Output_Var**: `i_amount_bpa`
  - **TAX_UNIT**: `tu_individual_se`
  - **Comp_UpLim**: `$bpa_maxlim*$XBASM`

### 4. Function: ArithOp
  **Formula:** `i_amount_bpa/$bpa_stdmy
`
  **Output Variable:** `bpa_s`
  **Tax Unit:** `tu_individual_se`


---

## Policy: random_se
### 1. Function: RandSeed
  - **Seed**: `19`

### 2. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_1`
  **Tax Unit:** `tu_individual_se`

### 3. Function: RandSeed
  - **Seed**: `20`

### 4. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_2`
  **Tax Unit:** `tu_individual_se`

### 5. Function: RandSeed
  - **Seed**: `21`

### 6. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_3`
  **Tax Unit:** `tu_individual_se`

### 7. Function: DefVar
  - **i_mc_rand_1**: `0`
  - **i_mc_rand_2**: `0`
  - **i_mc_rand_3**: `0`
  - **i_lmamy**: `0`
  - **i_lma2**: `0`
  - **i_lma1**: `0`
  - **Var_Monetary**: `no`
  - **i_bsamt_rand**: `0`

### 8. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lmamy`
  **Tax Unit:** `tu_individual_se`

### 9. Function: RandSeed
  - **Seed**: `25`

### 10. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lma2`
  **Tax Unit:** `tu_individual_se`

### 11. Function: RandSeed
  - **Seed**: `24`

### 12. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lma1`
  **Tax Unit:** `tu_individual_se`

### 13. Function: RandSeed
  - **Seed**: `23`

### 14. Function: RandSeed
  - **Seed**: `202402291642`

### 15. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_bsamt_rand`
  **Tax Unit:** `tu_individual_se`


---

## Policy: yemcomp_se *(Switch: off)*
### 1. Function: DefVar
  - **Var_Monetary**: `yes`
  - **i_yem_orig**: `yem`
  - **i_bwkmcee_s**: `0`
  - **i_yemmc_s**: `0`
  - **i_diff**: `0`
  - **i_yemmc02_s**: `0`
  - **i_bwkmcee02_s**: `0`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(bwkmceemy_s > $yemcomp_minamt)`
  - **Tax Unit:** `tu_individual_se`

### 3. Function: ArithOp
  **Formula:** `yem * $yemcomp_stdmy / yemmy`
  **Output Variable:** `yemmw_s`
  **Tax Unit:** `tu_individual_se`

### 4. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(bwkmceemy_s > $yemcomp_minamt) & (lhwsr_s=$yemcomp_rate4)`
  - **Comp_perTU**: `min(yemmw_s,$mc_max_yem) * (1- lhwsr_s) * $mc_rrate4 * $mc_share4`
  - **Output_Var**: `i_bwkmcee_s`
  - **TAX_UNIT**: `tu_individual_se`

### 5. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(bwkmceemy_s > $yemcomp_minamt) & (lhwsr_s=$yemcomp_rate4)`
  - **Comp_perTU**: `min(yemmw_s,$mc_max_yem) * (1- lhwsr_s) * $mc_rrate4 * (1-$mc_share4)`
  - **Output_Var**: `i_yemmc_s`
  - **TAX_UNIT**: `tu_individual_se`

### 6. Function: ArithOp
  **Formula:** `(i_bwkmcee_s * min(3,  bwkmceemy_s) + i_bwkmcee02_s * max(0,bwkmceemy_s - 3) ) / $yemcomp_stdmy
`
  **Output Variable:** `bwkmcee_s`
  **Tax Unit:** `tu_individual_se`

### 7. Function: ArithOp
  **Formula:** `(i_yemmc_s * min(3,bwkmceemy_s) + i_yemmc02_s * max(0,bwkmceemy_s - 3) ) / $yemcomp_stdmy
`
  **Output Variable:** `yemmc_s`
  **Tax Unit:** `tu_individual_se`

### 8. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(bwkmceemy_s > $yemcomp_minamt) & (lhwsr_s=$yemcomp_rate4)`
  - **Comp_perTU**: `min(yemmw_s,$mc_max_yem) * (1- lhwsr02_s) * $mc_rrate3 * $mc_share3`
  - **Output_Var**: `i_bwkmcee02_s`
  - **TAX_UNIT**: `tu_individual_se`

### 9. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(bwkmceemy_s > $yemcomp_minamt) & (lhwsr_s=$yemcomp_rate4)`
  - **Comp_perTU**: `min(yemmw_s,$mc_max_yem) * (1- lhwsr02_s) * $mc_rrate3 * (1-$mc_share3)`
  - **Output_Var**: `i_yemmc02_s`
  - **TAX_UNIT**: `tu_individual_se`

### 10. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `lhwsr_s > $yemcomp_thres5  & lhwsr_s < $yemcomp_thres4
`
  - **Comp_perTU**: `$yemcomp_rate4`
  - **Output_Var**: `lhwsr_s`
  - **TAX_UNIT**: `tu_individual_se`

### 11. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `lhwsr_s=$yemcomp_rate4
`
  - **Comp_perTU**: `$yemcomp_rate3
`
  - **Output_Var**: `lhwsr02_s`
  - **TAX_UNIT**: `tu_individual_se`


---

## Policy: tco_se *(Switch: off)*
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
  - `$tco_a_07221`: 0.50* (($tco_a_07221a1 +  (($tco_a_07221a21 +  $tco_a_07221a22+  $tco_a_07221a23)/3))/2) + 0.00*$tco_a_07221b + 0.50*(($tco_a_07221c1+$tco_a_07221c2+$tco_a_07221c3)/3) + 0.00*(($tco_a_07221d1+$tco_a_07221d2+$tco_a_07221d3)/3) + 0.00*$tco_a_07221e
  - `$tco_a_02122`: 0.95*$tco_a_02122a + 0.05*(($tco_a_02122b +$tco_a_02122c+$tco_a_02122d+$tco_a_02122e)/4)
  - `$tco_a_02121`: 0.95*$tco_a_02121a1 + 0.025*(($tco_a_02121a2 +$tco_a_02121a3+$tco_a_02121a4+$tco_a_02121a5)/4)+ 0.025*(($tco_a_02121b1+$tco_a_02121b2)/2)

### 3. Function: DefConst
  **Constants Defined:**
  - `$tco_base_a_04531`: 1.00*$tco_base_a_04531a + 0.00*$tco_base_a_04531b + 0.00*$tco_base_a_04531c
  - `$tco_base_a_07221`: 0.50* (($tco_base_a_07221a1 +  (($tco_base_a_07221a21 +  $tco_base_a_07221a22+  $tco_base_a_07221a23)/3))/2) + 0.00*$tco_base_a_07221b + 0.50*(($tco_base_a_07221c1+$tco_base_a_07221c2+$tco_base_a_07221c3)/3) + 0.00*(($tco_base_a_07221d1+$tco_base_a_07221d2+$tco_base_a_07221d3)/3) + 0.00*$tco_base_a_07221e
  - `$tco_base_q_02111`: $tco_base_q_02111t / 40% * 100
  - `$tco_base_q_02121`: (0.90*$tco_base_q_02121t1+ 0.05*$tco_base_q_02121t2 + 0.05*$tco_base_q_02121t3)* 100
  - `$tco_base_q_02122`: $tco_base_q_02122t * 100
  - `$tco_base_q_02131`: $tco_base_q_02131t * 100 / 5
  - `$tco_base_q_04531`: 1.00*$tco_base_q_04531a + 0.00*$tco_base_q_04531b + 0.00*$tco_base_q_04531c
  - `$tco_base_q_07221`: 0.50* (($tco_base_q_07221a1 +  (($tco_base_q_07221a21 +  $tco_base_q_07221a22+  $tco_base_q_07221a23)/3))/2) + 0.00*$tco_base_q_07221b + 0.50*(($tco_base_q_07221c1+$tco_base_q_07221c2+$tco_base_q_07221c3)/3) + 0.00*(($tco_base_q_07221d1+$tco_base_q_07221d2+$tco_base_q_07221d3)/3) + 0.00*$tco_base_q_07221e
  - `$tco_base_a_02122`: 0.95*$tco_base_a_02122a + 0.05*(($tco_base_a_02122b +$tco_base_a_02122c+$tco_base_a_02122d+$tco_base_a_02122e)/4)
  - `$tco_base_a_02121`: 0.95*$tco_base_a_02121a1 + 0.025*(($tco_base_a_02121a2 +$tco_base_a_02121a3+$tco_base_a_02121a4+$tco_base_a_02121a5)/4)+ 0.025*(($tco_base_a_02121b1+$tco_base_a_02121b2)/2)

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
  - `$tco_t_01111`: $tco_t_red1
  - `$tco_t_01112`: $tco_t_red1
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
  - `$tco_t_01141`: $tco_t_red1
  - `$tco_t_01142`: $tco_t_red1
  - `$tco_t_01143`: $tco_t_red1
  - `$tco_t_01144`: $tco_t_red1
  - `$tco_t_01145`: $tco_t_red1
  - `$tco_t_01146`: $tco_t_red1
  - `$tco_t_01147`: $tco_t_red1
  - `$tco_t_01151`: $tco_t_red1
  - `$tco_t_01152`: $tco_t_red1
  - `$tco_t_01153`: $tco_t_red1
  - `$tco_t_01154`: $tco_t_red1
  - `$tco_t_01155`: $tco_t_red1
  - `$tco_t_01161`: $tco_t_red1
  - `$tco_t_01162`: $tco_t_red1
  - `$tco_t_01163`: $tco_t_red1
  - `$tco_t_01164`: $tco_t_red1
  - `$tco_t_01165`: $tco_t_red1
  - `$tco_t_01166`: $tco_t_red1
  - `$tco_t_01167`: $tco_t_red1
  - `$tco_t_01168`: $tco_t_red1
  - `$tco_t_01169`: $tco_t_red1
  - `$tco_t_01171`: $tco_t_red1
  - `$tco_t_01172`: $tco_t_red1
  - `$tco_t_01173`: $tco_t_red1
  - `$tco_t_01174`: $tco_t_red1
  - `$tco_t_01175`: $tco_t_red1
  - `$tco_t_01176`: $tco_t_red1
  - `$tco_t_01177`: $tco_t_red1
  - `$tco_t_01178`: $tco_t_red1
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
  - `$tco_t_01222`: $tco_t_red1
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
  - `$tco_t_03141`: $tco_t_red1
  - `$tco_t_03211`: $tco_t_std
  - `$tco_t_03212`: $tco_t_std
  - `$tco_t_03213`: $tco_t_std
  - `$tco_t_03221`: $tco_t_red1
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
  - `$tco_t_06111`: $tco_t_std
  - `$tco_t_06121`: $tco_t_std
  - `$tco_t_06131`: $tco_t_std
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
  - `$tco_t_07311`: $tco_t_red2
  - `$tco_t_07321`: $tco_t_red2
  - `$tco_t_07331`: $tco_t_red2
  - `$tco_t_07341`: $tco_t_red2
  - `$tco_t_07351`: $tco_t_red2
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
  - `$tco_t_09411`: $tco_t_red2
  - `$tco_t_09421`: $tco_t_red2
  - `$tco_t_09422`: $tco_t_red2
  - `$tco_t_09423`: $tco_t_std
  - `$tco_t_09424`: $tco_t_std
  - `$tco_t_09511`: $tco_t_red2
  - `$tco_t_09521`: $tco_t_red2
  - `$tco_t_09531`: $tco_t_red2
  - `$tco_t_09541`: $tco_t_std
  - `$tco_t_09611`: $tco_t_std
  - `$tco_t_10111`: $tco_t_zero
  - `$tco_t_10211`: $tco_t_zero
  - `$tco_t_10311`: $tco_t_zero
  - `$tco_t_10411`: $tco_t_zero
  - `$tco_t_10511`: $tco_t_zero
  - `$tco_t_11111`: $tco_t_red1
  - `$tco_t_11112`: $tco_t_red1
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
  - `$tco_t_04111`: $tco_t_zero
  - `$tco_t_04121`: $tco_t_zero
  - `$tco_t_043`: $tco_t_std
  - `$tco_t_044`: $tco_t_std
  - `$tco_t_04511`: $tco_t_std
  - `$tco_t_04521`: $tco_t_std
  - `$tco_t_04522`: $tco_t_std
  - `$tco_t_04531`: $tco_t_std
  - `$tco_t_04541`: $tco_t_std
  - `$tco_t_04551`: $tco_t_std
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
  - `$tco_a_07221d3`: $tco_base_a_07221d3
  - `$tco_a_07221d2`: $tco_base_a_07221d2
  - `$tco_a_07221d1`: $tco_base_a_07221d1
  - `$tco_a_07221c3`: $tco_base_a_07221c3
  - `$tco_a_07221c2`: $tco_base_a_07221c2
  - `$tco_a_07221c1`: $tco_base_a_07221c1
  - `$tco_a_07221b`: $tco_base_a_07221b
  - `$tco_a_07221a23`: $tco_base_a_07221a23
  - `$tco_a_07221a22`: $tco_base_a_07221a22
  - `$tco_a_07221a21`: $tco_base_a_07221a21
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
  - `$tco_a_02121a1`: $tco_base_a_02121a1
  - `$tco_a_02121b1`: $tco_base_a_02121b1
  - `$tco_a_02111`: $tco_base_a_02111
  - `$tco_a_02121b2`: $tco_base_a_02121b2
  - `$tco_a_02121a5`: $tco_base_a_02121a5
  - `$tco_a_02121a4`: $tco_base_a_02121a4
  - `$tco_a_02121a3`: $tco_base_a_02121a3
  - `$tco_a_02121a2`: $tco_base_a_02121a2
  - `$tco_a_02122e`: $tco_base_a_02122e
  - `$tco_a_02122d`: $tco_base_a_02122d
  - `$tco_a_02122c`: $tco_base_a_02122c
  - `$tco_a_02122b`: $tco_base_a_02122b
  - `$tco_a_02122a`: $tco_base_a_02122a

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
  - **xs044**: `+`
  - **xs043**: `+`
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


---

## Policy: TransLMA_se *(Switch: off)*
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
  - `Run_Cond`: GetDataIncomeYear=2019

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy = 0) & (ysemy = 0)& (dag > 17) & (dag < 65) & ((les=5)| lowas=1) `
  - **Tax Unit:** `tu_individual_se`

### 3. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(deh = 5) & (dgn = 1) & (i_lma1 < $ur_dgn1_deh3_ee)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_se`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy > 0) `
  - **Tax Unit:** `tu_individual_se`

### 5. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(deh = 5) & (dgn = 1) & (i_lma1 < $er_dgn1_deh3_ee)`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_se`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ysemy > 0) & (yemmy = 0)`
  - **Tax Unit:** `tu_individual_se`

### 7. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dgn = 1 & (i_lma2 < $er_dgn1_se)`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_se`

### 8. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lma =1)`
  - **Tax Unit:** `tu_individual_se`

### 9. Function: ArithOp
  **Formula:** `(yivwg*$lhw*52/12)`
  **Output Variable:** `yem_a`
  **Tax Unit:** `tu_individual_se`

### 10. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lma=1)|(lma=5)`
  - **Tax Unit:** `tu_individual_se`

### 11. Function: ArithOp
  **Formula:** `$lhw`
  **Output Variable:** `lhw_a`
  **Tax Unit:** `tu_individual_se`

### 12. Function: BenCalc
  - **Comp_Cond**: `(lma=2) & (ysemy > 0) & (yemmy = 0)`
  - **Comp_perTU**: `0`
  - **Output_Var**: `yemmy_a`
  - **TAX_UNIT**: `tu_individual_se`

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
  - `Run_Cond`: GetDataIncomeYear=2019

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
  - `Run_Cond`: GetDataIncomeYear=2019

### 15. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy >0)  & (lma=0)`
  - **Tax Unit:** `tu_individual_se`

### 16. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(lindi = 5) & (dgn = 1) & (i_mc_rand_1 < $sh_mcee_l4_dgn1)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lmcee_s`
  - **TAX_UNIT**: `tu_individual_se`

### 17. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lmcee_s = 1)`
  - **Tax Unit:** `tu_individual_se`

### 18. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_2> $sh_mceemy_9)`
  - **Comp_perTU**: `min (10, yemmy)`
  - **Output_Var**: `bwkmceemy_s`
  - **TAX_UNIT**: `tu_individual_se`

### 19. Function: ArithOp
  **Formula:** `yemmy - bwkmceemy_s`
  **Output Variable:** `yemmwmy_s`
  **Tax Unit:** `tu_individual_se`

### 20. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(bwkmceemy_s > 0)`
  - **Tax Unit:** `tu_individual_se`

### 21. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_3 >$sh_45hours_ee)`
  - **Comp_perTU**: `0.70`
  - **Output_Var**: `lhwsr_s`
  - **TAX_UNIT**: `tu_individual_se`

### 22. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ysemy > 0)  & (lma=0) & (lmcee_s = 0) & (yse>0)`
  - **Tax Unit:** `tu_individual_se`

### 23. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(lindi = 5) & (dgn = 1) & (i_mc_rand_1 < $sh_mcse_l4_dgn1)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lmcse_s`
  - **TAX_UNIT**: `tu_individual_se`

### 24. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lmcse_s = 1)`
  - **Tax Unit:** `tu_individual_se`

### 25. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_2> $sh_mcsemy_9)`
  - **Comp_perTU**: `min (10, ysemy)`
  - **Output_Var**: `bwkmcsemy_s`
  - **TAX_UNIT**: `tu_individual_se`

### 26. Function: ArithOp
  **Formula:** `ysemy - bwkmcsemy_s`
  **Output Variable:** `ysemwmy_s`
  **Tax Unit:** `tu_individual_se`

### 27. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(bwkmcsemy_s > 0)`
  - **Tax Unit:** `tu_individual_se`

### 28. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_3 >$sh_45hours_se)`
  - **Comp_perTU**: `0.70`
  - **Output_Add_Var**: `lhwsr_s`
  - **TAX_UNIT**: `tu_individual_se`

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
  - `Run_Cond`: GetDataIncomeYear!=2019

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
  - `Run_Cond`: GetDataIncomeYear!=2019

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
  - `Run_Cond`: GetDataIncomeYear!=2019


---

## Policy: hhot_switch_se
### 1. Function: ChangeParam
  - **Param_Id**: `bunct_se`
  - **Param_NewVal**: `on`


---
