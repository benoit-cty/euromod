# EUROMOD Tax-Benefit Rules for LV_2025

## Policy: uprate_lv
### 1. Function: Uprate
  - **def_factor**: `1`
  - **WarnIfNoFactor**: `no`
  - **dataset**: `*training_data`
  - **Dataset**: `*_hhot`

### 2. Function: Uprate
  - **WarnIfNoFactor**: `yes`
  - **pdint**: `$f_wageoffic_1`
  - **bhl**: `$f_wageoffic_1`
  - **bsafu**: `$f_wageoffic_1`
  - **yivwg**: `$f_wagena`
  - **yivwg01**: `$f_wagena_1`
  - **yivwg02**: `$f_wagena_1`
  - **tpr**: `$f_tpr`
  - **yds**: `$f_one`
  - **ydses_o**: `$f_one`
  - **Factor_Condition**: `lcs != 1 & (lindi < 1  | lindi > 12)`
  - **yem**: `$f_one`
  - **afc**: `$f_one`
  - **bed**: `$f_one`
  - **kfb**: `$f_wageoffic`
  - **kfbcc**: `$f_wageoffic`
  - **xmp**: `$f_cpi`
  - **xpp**: `$f_cpi`
  - **yiynt**: `$f_one`
  - **yiytx**: `$f_one`
  - **yot**: `$f_wageoffic`
  - **ypp**: `$f_one`
  - **ypt**: `$f_wageoffic`
  - **bfaot**: `$f_bfa`
  - **bsaot**: `$f_bsa`
  - **tad**: `$f_one`
  - **tis**: `$f_one`
  - **tscer**: `$f_one`
  - **yse**: `$f_wagena_pr`
  - **bho**: `$f_house`
  - **kivho**: `$f_house`
  - **xhc**: `$f_house`
  - **xhcmomi**: `$f_house`
  - **xhcot**: `$f_house`
  - **xhcrt**: `$f_house`
  - **ypr**: `$f_house`
  - **bunot**: `$f_bun`
  - **yempv**: `$f_wageoffic_1`
  - **aggvar_name**: `bsa`
  - **aggvar_part**: `bpeecdi_01`
  - **yem_a**: `$f_wagena`
  - **poatx**: `$f_poatx_av`
  - **pditx**: `$f_pditx_av`
  - **psutx**: `$f_pditx_av`
  - **Dataset**: `lv_20??_??_????_??_??`
  - **bfaba**: `$f_one`
  - **bfacc**: `$f_one`
  - **bfama**: `$f_one`
  - **bfana**: `$f_one`
  - **bfapl**: `$f_one`
  - **bfawk**: `$f_one`
  - **bsamm**: `$f_one`
  - **bun00**: `$f_one`
  - **pdiss01**: `$f_one`
  - **pdiss02**: `$f_one`
  - **poass**: `$f_one`
  - **psuss**: `$f_one`
  - **yempv01**: `$f_wagena_1`
  - **yempv_a**: `$f_wagena`
  - **yptmp**: `$f_wageoffic`
  - **ymwdt**: `$f_wageofficLead`
  - **yem20_a**: `$f_wagena`
  - **yem19_a**: `$f_wagena`
  - **yem18_a**: `$f_wagena`
  - **bfaam**: `$f_one`
  - **xed00**: `$f_cpi`
  - **xhl00**: `$f_cpi`
  - **AggVar_Part**: `bpeecsu_01`
  - **bfa00**: `$f_one`
  - **bfaec**: `$f_one`
  - **bpeecoa**: `$f_one`
  - **bpeecdi**: `$f_one`
  - **bpeecsu**: `$f_one`
  - **AggVar_Tolerance**: `4`
  - **bpeec02**: `$f_one`
  - **bpeec**: `$f_one`
  - **tbs**: `$f_one`
  - **bpeecoa_01**: `$f_one`
  - **bpeecsu_01**: `$f_one`
  - **bpeecdi_01**: `$f_one`
  - **bhoht**: `$f_one`
  - **bpeec01**: `$f_one`


---

## Policy: ConstDef_lv
### 1. Function: DefConst
  **Constants Defined:**
  - `$MinWage`: 740#m
  - `$pss_amt`: 166#m
  - `$tscse_se_lim`: 740#m
  - `$tscse_se_uplim1`: 105300#y
  - `$tscse_se_uplim0`: 78100#y
  - `$bun00_daylim`: n/a
  - `$bfawk_daylim`: n/a
  - `$tscse_se_minthres`: 0#y

### 2. Function: DefConst
  **Constants Defined:**
  - `$PensAgeMale`: 65
  - `$PensAgeFem`: 65
  - `$Nwh`: 40
  - `$ImputedWage`: 0
  - `$MajorityAge`: 18

### 3. Function: DefConst
  **Constants Defined:**
  - `$bun00_QperMin`: 12
  - `$bun00_QperTot`: 16

### 4. Function: DefConst
  **Constants Defined:**
  - `$mc_my_3`: n/a
  - `$mc_my_2`: n/a
  - `$mc_my_1`: n/a
  - `$mc_rrate`: n/a
  - `$mc_min`: n/a
  - `$mc_max`: n/a
  - `$mc_sicmin`: n/a
  - `$mc_dep`: n/a
  - `$mc_depallow`: n/a
  - `$mc_my_4`: n/a
  - `$mc_my_6`: n/a
  - `$mc_my_5`: n/a

### 5. Function: DefConst
  **Constants Defined:**
  - `$tscse_rate1`: 0.3107
  - `$tscse_rate2`: 0.2936
  - `$tscse_rate3`: 0.1

### 6. Function: DefConst *(Switch: off)*
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

### 7. Function: DefConst
  **Constants Defined:**
  - `$bsamm_BTA_rate`: 1
  - `$bsamm_BCA_rate`: 1
  - `$bho_BTA_rate`: 1
  - `$bho_BCA_rate`: 1

### 8. Function: DefConst
  **Constants Defined:**
  - `$bfawk_age1`: 0.09
  - `$bfawk_age2`: 0.17
  - `$bfawk_age3`: 0.25
  - `$bfawk_age4`: 0.34
  - `$bfawk_age5`: 0.42
  - `$bfawk_age6`: 0.5
  - `$bfawk_age7`: 0.59
  - `$bfawk_age8`: 0.67
  - `$bfawk_age9`: 0.75
  - `$bfawk_age10`: 0.84
  - `$bfawk_age11`: 0.92
  - `$bfawk_age12`: 1
  - `$bfawk_age13`: 1.09
  - `$bfawk_age14`: 1.17
  - `$bfawk_age15`: 1.25
  - `$bfawk_age16`: 1.34
  - `$bfawk_age17`: 1.42
  - `$bfawk_age18`: 1.5
  - `$bfawk_age19`: 1.59
  - `$bfawk_age20`: 1.67
  - `$bfawk_age21`: 1.75
  - `$bfawk_age22`: 1.84
  - `$bfawk_age23`: 1.92
  - `$bfawk_age24`: 2
  - `$bfawk_age25`: 2.09
  - `$bfawk_age26`: 2.17
  - `$bfawk_age27`: 2.25
  - `$bfawk_age28`: 2.34
  - `$bfawk_age29`: 2.42
  - `$bfawk_age30`: 2.5
  - `$bfawk_age31`: 2.59
  - `$bfawk_age32`: 2.67
  - `$bfawk_age33`: 2.75
  - `$bfawk_age34`: 2.84
  - `$bfawk_age35`: 2.92
  - `$bfawk_age36`: 3


---

## Policy: IlsDef_lv
### 1. Function: DefIl
  - **name**: `ils_earns`
  - **yem**: `+`
  - **yse**: `+`

### 2. Function: DefIl
  - **name**: `ils_origy`
  - **ils_earns**: `+`
  - **yiy**: `+`
  - **ypp**: `+`
  - **ypr**: `+`
  - **yot**: `+`
  - **ypt**: `+`
  - **xmp**: `-`

### 3. Function: DefIl
  - **name**: `ils_origrepy`
  - **ils_origy**: `+`
  - **poatx**: `+`
  - **poass_s**: `+`
  - **bfama_s**: `+`
  - **bfacc_s**: `+`
  - **bfawk_s**: `+`
  - **bfapl_s**: `+`
  - **bun00_s**: `+`
  - **pditx**: `+`
  - **pdint**: `+`
  - **pdiss_s**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **bwkmcch_s**: `n/a`
  - **bfaec_s**: `n/a`
  - **bpeec_s**: `n/a`
  - **bpeec02_s**: `n/a`
  - **bpeec01_s
**: `n/a`

### 4. Function: DefIl
  - **name**: `ils_pen`
  - **poatx**: `+`
  - **poass_s**: `+`
  - **psutx**: `+`
  - **psuss_s**: `+`
  - **pditx**: `+`
  - **pdiss_s**: `+`

### 5. Function: DefIl
  - **name**: `ils_bennt`
  - **bun00_s**: `+`
  - **bhl**: `+`
  - **bed**: `+`
  - **bfacc_s**: `+`
  - **bfama_s**: `+`
  - **bfapl_s**: `+`
  - **bfawk_s**: `+`
  - **bfana_s**: `+`
  - **bfaba_s**: `+`
  - **bfaot**: `+`
  - **pdint**: `+`
  - **bsafu**: `+`
  - **bsaot**: `+`
  - **bunot**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **bwkmcch_s**: `n/a`
  - **bfaec_s**: `n/a`
  - **bpeec_s**: `n/a`
  - **bpeec02_s**: `n/a`
  - **bfaam**: `+`
  - **bpeec01_s**: `n/a`
  - **bhoht**: `n/a`

### 6. Function: DefIl
  - **name**: `ils_benmt`
  - **bsamm_s**: `+`
  - **bho_s**: `+`

### 7. Function: DefIl
  - **name**: `ils_ben`
  - **ils_pen**: `+`
  - **ils_benmt**: `+`
  - **ils_bennt**: `+`

### 8. Function: DefIl
  - **name**: `ils_tax`
  - **ils_taxin**: `+`
  - **ils_taxwl**: `+`

### 9. Function: DefIl
  - **name**: `ils_sicee`
  - **tscee_s**: `+`

### 10. Function: DefIl
  - **name**: `ils_sicse`
  - **tscse_s**: `+`

### 11. Function: DefIl
  - **name**: `ils_sicer`
  - **tscer_s**: `+`
  - **txcer_s**: `+`
  - **tscmm_s**: `+`

### 12. Function: DefIl
  - **name**: `ils_dispy`
  - **ils_origy**: `+`
  - **ils_ben**: `+`
  - **ils_tax**: `-`
  - **ils_sicdy**: `-`

### 13. Function: DefIl
  - **name**: `ils_taxin`
  - **tin_s**: `+`
  - **txcee_s**: `+`
  - **txcse_s**: `+`
  - **tbs**: `+`

### 14. Function: DefIl
  - **name**: `ils_bensim`
  - **pss_s**: `+`
  - **bun00_s**: `+`
  - **bfama_s**: `+`
  - **bfana_s**: `+`
  - **bfaba_s**: `+`
  - **bfapl_s**: `+`
  - **bsamm_s**: `+`
  - **bho_s**: `+`
  - **bfacc_s**: `+`
  - **bfawk_s**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **bwkmcch_s**: `n/a`
  - **bfaec_s**: `n/a`
  - **bpeec_s**: `n/a`
  - **bpeec02_s**: `n/a`
  - **bpeec01_s
**: `n/a`

### 15. Function: DefIl
  - **Name**: `ils_b1_bfa`
  - **bfana_s**: `+`
  - **bfacc_s**: `+`
  - **bfaba_s**: `+`
  - **bfapl_s**: `+`
  - **bfama_s**: `+`
  - **bfawk_s**: `+`
  - **bfaot**: `+`
  - **bfaec_s**: `n/a`
  - **bfaam**: `+`

### 16. Function: DefIl
  - **Name**: `ils_b1_bed`
  - **bed**: `+`

### 17. Function: DefIl
  - **Name**: `ils_b1_boa`
  - **poatx**: `+`
  - **poass_s**: `+`
  - **bpeec_s**: `n/a`
  - **bpeec02_s**: `n/a`
  - **bpeec01_s**: `n/a`

### 18. Function: DefIl
  - **Name**: `ils_b1_bsu`
  - **psutx**: `+`
  - **psuss_s**: `+`

### 19. Function: DefIl
  - **Name**: `ils_b1_bdi`
  - **pditx**: `+`
  - **pdiss_s**: `+`
  - **pdint**: `+`

### 20. Function: DefIl
  - **Name**: `ils_b1_bun`
  - **bun00_s**: `+`
  - **bunot**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **bwkmcch_s**: `n/a`

### 21. Function: DefIl
  - **Name**: `ils_b1_bhl`
  - **bhl**: `+`

### 22. Function: DefIl
  - **Name**: `ils_b1_bho`
  - **bho_s**: `+`
  - **bhoht**: `n/a`

### 23. Function: DefIl
  - **Name**: `ils_b1_bsa`
  - **bsamm_s**: `+`
  - **bsafu**: `+`
  - **bsaot**: `+`

### 24. Function: DefIl
  - **Name**: `ils_b2_bfaed`
  - **ils_b1_bed**: `+`
  - **ils_b1_bfa**: `+`

### 25. Function: DefIl
  - **Name**: `ils_b2_penhl`
  - **ils_b1_bsu**: `+`
  - **ils_b1_boa**: `+`
  - **ils_b1_bdi**: `+`
  - **ils_b1_bhl**: `+`

### 26. Function: DefIl
  - **Name**: `ils_sicot`

### 27. Function: DefIl
  - **Name**: `ils_sicct`

### 28. Function: DefIl
  - **Name**: `ils_b2_bsaho`
  - **ils_b1_bho**: `+`
  - **ils_b1_bsa**: `+`

### 29. Function: DefIl
  - **Name**: `ils_base_txcee`
  - **yem**: `+`

### 30. Function: DefIl
  - **Name**: `ils_base_txcse`
  - **yse**: `+`

### 31. Function: DefIl
  - **Name**: `ils_base_tin`
  - **yiy**: `n/a`
  - **yem**: `+`
  - **yiytx**: `+`
  - **pditx**: `+`
  - **psutx**: `+`
  - **poatx**: `+`
  - **ypr**: `+`
  - **yse**: `+`
  - **yot**: `+`
  - **bhl**: `+`

### 32. Function: DefIl
  - **Name**: `ils_base_txcer`
  - **yem**: `+`

### 33. Function: DefIl
  - **Name**: `ils_sicdy`
  - **ils_sicot**: `+`
  - **ils_sicse**: `+`
  - **ils_sicee**: `+`

### 34. Function: DefIl
  - **Name**: `ils_b1_bwk`

### 35. Function: DefIl
  - **Name**: `ils_b2_bunwk`
  - **ils_b1_bwk**: `+`
  - **ils_b1_bun**: `+`

### 36. Function: DefIl
  - **name**: `ils_taxwl`
  - **tpr**: `+`

### 37. Function: DefIl
  - **Name**: `ils_taxsim`
  - **txcse_s**: `+`
  - **txcee_s**: `+`
  - **tin_s**: `+`


---

## Policy: tudef_lv
### 1. Function: DefTu
  - **Name**: `tu_hh_oecd_co`
  - **Type**: `HH`
  - **DepChildCond**: `dag<14`

### 2. Function: DefTu
  - **Name**: `tu_individual_lv`
  - **Type**: `IND`

### 3. Function: DefTu
  - **Name**: `tu_household_lv`
  - **Type**: `HH`
  - **DepChildCond**: `(dag<=15 | (dag<=19 & (dec>=2 & dec<=4))) & !IsMarried & bed#1=0`
  - **#_level**: `tu_individual_lv`
  - **LoneParentCond**: `Default & !IsMarried`

### 4. Function: DefTu
  - **Name**: `tu_hhdep_lv`
  - **Type**: `HH`
  - **DepChildCond**: `default & (dag<18 | (dag<24 & dec>2))`


---

## Policy: neg_lv
### 1. Function: ArithOp
  **Formula:** `max(0,yse)`
  **Output Variable:** `yse`
  **Tax Unit:** `tu_individual_lv`


---

## Policy: yem_lv *(Switch: switch)*
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem>0 & lhw>0`
  - **Tax Unit:** `tu_individual_lv`

### 2. Function: Max
  - **who_must_be_elig**: `one`
  - **val**: `$MinWage*min(lhw,$Nwh)/$Nwh*yemmy/12`
  - **output_var**: `yem`
  - **TAX_UNIT**: `tu_individual_lv`

### 3. Function: ChangeParam
  - **Param_Id**: `d3af70a0-65a7-44f7-b786-b19b62b8069c`
  - **Param_NewVal**: `lv_2025_yem_std`


---

## Policy: tscee_lv
### 1. Function: DefConst
  **Constants Defined:**
  - `$tscee_rate1`: 0.105
  - `$tscee_rate2`: 0.0925

### 2. Function: BenCalc
  - **comp_cond**: `(dag00>=$PensAgeMale & dgn=1) | (dag00>=$PensAgeFem & dgn=0)`
  - **comp_perTU**: `yem#1*$tscee_rate2`
  - **#_uplim**: `$tscse_se_uplim1`
  - **output_var**: `tscee_s`
  - **TAX_UNIT**: `tu_individual_lv`


---

## Policy: tscer_lv
### 1. Function: DefConst
  **Constants Defined:**
  - `$tscer_rate1`: 0.2359
  - `$tscer_rate2`: 0.2077

### 2. Function: BenCalc
  - **comp_cond**: `(dag00>=$PensAgeMale & dgn=1) | (dag00>=$PensAgeFem & dgn=0)`
  - **comp_perTU**: `yem#1*$tscer_rate2`
  - **#_uplim**: `$tscse_se_uplim1`
  - **output_var**: `tscer_s`
  - **TAX_UNIT**: `tu_individual_lv`


---

## Policy: tscse_lv
### 1. Function: DefVar
  - **i_yse**: `0`
  - **i_tscse**: `0`

### 2. Function: BenCalc
  - **comp_cond**: `ysemy>0`
  - **comp_perTU**: `yse*12/ysemy`
  - **uplim**: `$tscse_se_uplim1`
  - **output_var**: `i_yse`
  - **TAX_UNIT**: `tu_individual_lv`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_yse>=$tscse_se_lim`
  - **Tax Unit:** `tu_individual_lv`

### 4. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(dag00>=$PensAgeMale & dgn=1) | (dag00>=$PensAgeFem & dgn=0)`
  - **comp_perTU**: `$tscse_se_lim*$tscse_rate2`
  - **output_var**: `i_tscse`
  - **TAX_UNIT**: `tu_individual_lv`

### 5. Function: ArithOp
  **Formula:** `i_tscse*ysemy/12`
  **Output Variable:** `tscse_s`
  **Tax Unit:** `tu_individual_lv`

### 6. Function: BenCalc
  - **Comp_Cond**: `i_yse<$tscse_se_lim`
  - **Comp_perTU**: `(i_yse-$tscse_se_minthres*12/ysemy)*$tscse_rate3`
  - **Output_Add_Var**: `i_tscse`
  - **TAX_UNIT**: `tu_individual_lv`
  - **LowLim**: `0`
  - **Who_Must_Be_Elig**: `one`

### 7. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yse>=$tscse_se_minthres & ysemy>0`
  - **Tax Unit:** `tu_individual_lv`


---

## Policy: pss_lv
### 1. Function: BenCalc
  - **comp_cond**: `poass>0`
  - **comp_perTU**: `$pss_amt`
  - **output_var**: `poass_s`
  - **TAX_UNIT**: `tu_individual_lv`

### 2. Function: BenCalc
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `psuss_s`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Comp_perTU**: `$pss_amt`
  - **Comp_Cond**: `psuss>0 & nDepChildrenInTu#1 = 0 & nDepChildrenInTu#2 = 0 `
  - **#_Level**: `tu_household_lv`
  - **#_AgeMin**: `7`
  - **#_AgeMax**: `6`

### 3. Function: BenCalc
  - **comp_cond**: `pdiss02>0  & yem = 0 & yse = 0`
  - **comp_perTU**: `($pss_disab_coef1+$pss_disab_coef2 +$pss_disab_coef3)/3 *($pss_disab1_amt + $pss_disab2_amt + $pss_disab3_amt)/3`
  - **output_var**: `pdiss_s`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Comp_Cond**: `pdiss02>0   & (yem >0 | yse > 0)`
  - **Comp_perTU**: `($pss_disab1_amt + $pss_disab2_amt + $pss_disab3_amt)/3`

### 4. Function: ArithOp
  **Formula:** `poass_s+pdiss_s+psuss_s`
  **Output Variable:** `pss_s`
  **Tax Unit:** `tu_individual_lv`

### 5. Function: DefConst
  **Constants Defined:**
  - `$pss_disabchild3_amt`: 189#m
  - `$pss_disab1_amt`: 232.4#m
  - `$pss_disabchild2_amt`: 226.8#m
  - `$pss_disabchild1_amt`: 264.6#m
  - `$pss_disab3_amt`: 166#m
  - `$pss_disab2_amt`: 199.2#m
  - `$pss_disabchild_amt`: n/a
  - `$pss_child_age6`: 189#m
  - `$pss_child_age7`: 226#m
  - `$pss_disab_coef1`: 1.3
  - `$pss_disab_coef2`: 1.2
  - `$pss_disab_coef3`: 1

### 6. Function: DefVar
  - **i_psuss_n1**: `0`
  - **i_psuss_n2**: `0`


---

## Policy: bun00_lv
### 1. Function: DefVar
  - **i_bun01**: `0`
  - **i_bun02**: `0`
  - **i_bun03**: `0`
  - **i_bunrt**: `0`
  - **i_bun**: `0`
  - **i_bun04**: `0`

### 2. Function: ArithOp
  **Formula:** `max(lunmy,bunmy)`
  **Output Variable:** `lunmy_s`
  **Tax Unit:** `tu_individual_lv`

### 3. Function: BenCalc
  - **comp_cond**: `lunmy_s > 0 & bun00 = 0`
  - **comp_perElig**: `0`
  - **output_var**: `liwmy_s`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Comp_LowLim**: `$bun00_QperMin`
  - **Comp_Cond**: `lnu > 0`
  - **Comp_perElig**: `liwmy_a`

### 4. Function: BenCalc
  - **comp_cond**: `liwwh>=$bun00_totthres4`
  - **comp_perTU**: `$bun00_rate4`
  - **output_var**: `i_bunrt`
  - **TAX_UNIT**: `tu_individual_lv`

### 5. Function: BenCalc
  - **comp_cond**: `lunmy_s > 0 & bun00 = 0 `
  - **comp_perElig**: `0`
  - **uplim**: `$tscse_se_uplim0`
  - **output_var**: `yempv_s`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Comp_Cond**: `lunmy_s>0`
  - **Comp_perElig**: `yempv`

### 6. Function: ArithOp
  **Formula:** `i_bunrt*yempv_s`
  **Output Variable:** `i_bun01`
  **Tax Unit:** `tu_individual_lv`

### 7. Function: ArithOp
  **Formula:** `i_bunrt*yempv_s*$bun00_redamt1`
  **Output Variable:** `i_bun02`
  **Tax Unit:** `tu_individual_lv`

### 8. Function: ArithOp
  **Formula:** `i_bunrt*yempv_s*$bun00_redamt2`
  **Output Variable:** `i_bun03`
  **Tax Unit:** `tu_individual_lv`

### 9. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 10. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 11. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 12. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 13. Function: BenCalc
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `bunmy_s>4`
  - **comp_perTU**: `(bunmy_s#3 - 4)*i_bun03`
  - **#_uplim**: `6`
  - **output_var**: `i_bun`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Comp_Cond**: `bunmy_s>6`
  - **Comp_perTU**: `(bunmy_s#4 - 6)*i_bun04`
  - **#_UpLim**: `8`

### 14. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 15. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_uplim**: `n/a`
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
  - **#_uplim**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 18. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag>15 & ( (dgn=1 & dag00<=$PensAgeMale) | (dgn=0 & dag00<=$PensAgeFem )) & (dec=0 | dec>2) & poamy<12`
  - **Tax Unit:** `tu_individual_lv`

### 19. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `liwwh>=$bun00_totthres1 & liwmy_s >= $bun00_QperMin & lunmy_s > 0`
  - **comp_perTU**: `i_bun/12`
  - **output_var**: `bun00_s`
  - **TAX_UNIT**: `tu_individual_lv`

### 20. Function: BenCalc
  - **Comp_perTU**: `lunmy_s`
  - **Comp_Cond**: `lunmy_s > 0 & bun00 = 0`
  - **Output_Var**: `bunmy_s`
  - **TAX_UNIT**: `tu_individual_lv`

### 21. Function: DefConst
  **Constants Defined:**
  - `$bun00_rate1`: 0.5
  - `$bun00_rate2`: 0.55
  - `$bun00_rate3`: 0.6
  - `$bun00_rate4`: 0.65
  - `$bun00_unemp_amt`: n/a
  - `$bun00_totthres1`: 12
  - `$bun00_totthres2`: 120
  - `$bun00_totthres3`: 240
  - `$bun00_totthres4`: 360
  - `$bun00_redamt1`: 0.75
  - `$bun00_redamt2`: 0.5
  - `$bun00_redamt3`: 0.45

### 22. Function: ArithOp
  **Formula:** `i_bunrt*yempv_s*$bun00_redamt3`
  **Output Variable:** `i_bun04`
  **Tax Unit:** `tu_individual_lv`

### 23. Function: BenCalc *(Switch: switch)*
  - **comp_cond**: `liwwh16_h>=$bun00_totthres1 & liwwh>=$bun00_totthres4`
  - **comp_perTU**: `$bun00_rate4`
  - **output_var**: `i_bunrt`
  - **TAX_UNIT**: `tu_individual_lv`

### 24. Function: BenCalc *(Switch: switch)*
  - **comp_cond**: `(bunmy_s>4)&(bunmy_s <=6)`
  - **comp_perTU**: `(2 * i_bun01) + (2 * i_bun02) + (bunmy_s - 4)*i_bun03`
  - **Comp_Cond**: `(bunmy_s>8)`
  - **Comp_perTU**: `(2 * i_bun01) + (2 * i_bun02) + (2* i_bun03) + (2* i_bun04)`
  - **output_var**: `i_bun`
  - **TAX_UNIT**: `tu_individual_lv`

### 25. Function: BenCalc *(Switch: switch)*
  - **who_must_be_elig**: `one`
  - **comp_cond**: `les=5 & liwwh16_h>=$bun00_totthres1 & liwwh>=$bun00_QperMin`
  - **comp_perTU**: `i_bun/12`
  - **output_var**: `bun00_s`
  - **TAX_UNIT**: `tu_individual_lv`

### 26. Function: BenCalc
  - **comp_cond**: `(bunmy_s>4)&(bunmy_s <=6)`
  - **comp_perTU**: `i_bun03`
  - **Comp_Cond**: `(bunmy_s>8)`
  - **Comp_perTU**: `0`
  - **output_var**: `i_bun`
  - **TAX_UNIT**: `tu_individual_lv`

### 27. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `les=5 & liwwh16_h>=$bun00_totthres1 & liwwh>=$bun00_QperMin`
  - **comp_perTU**: `i_bun`
  - **output_var**: `bun00_s`
  - **TAX_UNIT**: `tu_individual_lv`

### 28. Function: BenCalc
  - **Comp_Cond**: `bunmy_s<lunmy_s`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bun00_s`
  - **TAX_UNIT**: `tu_individual_lv`


---

## Policy: bfana_lv
### 1. Function: DefConst
  **Constants Defined:**
  - `$bfana_stdamt`: 25#m
  - `$bfana_coef1`: n/a
  - `$bfana_coef2`: n/a
  - `$bfana_coef3`: n/a
  - `$bfana_extraamt2`: n/a
  - `$bfana_extraamt3`: n/a
  - `$bfana_extraamt4`: n/a
  - `$bfana_amt2`: 50#m
  - `$bfana_amt3`: 75#m
  - `$bfana_amt4`: 100#m

### 2. Function: DefTu
  - **name**: `tu_bfana_lv`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild & LooseDepChild`
  - **DepChildCond**: `default & dag>=1 & (dag<16 | (dag<20 & dec>2 & dms=1))`
  - **#_level**: `n/a`
  - **NoChildIfHead**: `yes`
  - **NoChildIfPartner**: `yes`
  - **ExtHeadCond**: `dgn=0 & !IsDepChild`
  - **StopIfNoHeadFound**: `no`

### 3. Function: DefTu
  - **Type**: `SUBGROUP`
  - **Name**: `tu_bfana2_lv`
  - **NoChildIfPartner**: `no`
  - **NoChildIfHead**: `no`
  - **StopIfNoHeadFound**: `no`
  - **ExtHeadCond**: `dgn=0 & !IsDepChild`
  - **Members**: `Partner & OwnDepChild & LooseDepChild `
  - **DepChildCond**: `default`

### 4. Function: BenCalc
  - **output_var**: `bfana_s`
  - **TAX_UNIT**: `tu_bfana_lv`
  - **#_Level**: `n/a`
  - **Comp_Cond**: `nDepChildrenInTu#1>=4`
  - **Comp_perTU**: `(nDepChildrenInTu#1)*$bfana_amt4`


---

## Policy: bfapl_lv
### 1. Function: DefVar
  - **i_yempl**: `0`
  - **i_bfapl**: `0`

### 2. Function: DefTu
  - **name**: `tu_bfapl_lv`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild & LooseDepChild`
  - **DepChildCond**: `dag00<=1`
  - **NoChildIfHead**: `yes`
  - **NoChildIfPartner**: `yes`
  - **ExtHeadCond**: `default & dgn=1`
  - **StopIfNoHeadFound**: `no`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dgn=1 & (yemmy>0 | ysemy > 0) & liwwh >=3 & IsParentOfDepChild#1 & nDepChInTu#1 > 0`
  - **Tax Unit:** `tu_individual_lv`

### 4. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `yempv01>0 & tscse_s>0`
  - **comp_perTU**: `yempv01`
  - **uplim**: `$tscse_se_uplim0`
  - **output_var**: `i_yempl`
  - **TAX_UNIT**: `tu_individual_lv`

### 5. Function: ArithOp
  **Formula:** `i_yempl*$bfapl_rate`
  **Output Variable:** `i_bfapl`
  **Tax Unit:** `tu_individual_lv`

### 6. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 7. Function: ArithOp
  **Formula:** `i_bfapl*$bfapl_dy*$bfapl_coef`
  **Output Variable:** `bfapl_s`
  **Tax Unit:** `tu_individual_lv`

### 8. Function: BenCalc
  - **comp_cond**: `bfapl>0`
  - **comp_perTU**: `bfapl_s`
  - **output_var**: `bfapl_s`
  - **TAX_UNIT**: `tu_individual_lv`

### 9. Function: DefConst
  **Constants Defined:**
  - `$bfapl_rate`: 0.8
  - `$bfapl_coef`: 1.46
  - `$bfapl_dy`: 10/365


---

## Policy: bfama_lv
### 1. Function: DefVar
  - **i_yemma**: `0`
  - **i_bfama**: `0`
  - **i_bfamamy2**: `0`
  - **i_bfamamy1**: `0`

### 2. Function: DefTu
  - **name**: `tu_bfama_lv`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild & LooseDepChild`
  - **DepChildCond**: `dag00<= 1`
  - **NoChildIfHead**: `yes`
  - **NoChildIfPartner**: `yes`
  - **ExtHeadCond**: `default & dgn=0`
  - **StopIfNoHeadFound**: `no`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsHeadOfTu#1 & liwwh>=3 & IsParentOfDepChild#1 & nDepChInTu#1 > 0`
  - **Tax Unit:** `tu_individual_lv`

### 4. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `yempv01>0 & tscse_s>0`
  - **comp_perTU**: `yempv01`
  - **uplim**: `$tscse_se_uplim0`
  - **output_var**: `i_yemma`
  - **TAX_UNIT**: `tu_individual_lv`

### 5. Function: ArithOp
  **Formula:** `i_yemma*$bfama_rate`
  **Output Variable:** `i_bfama`
  **Tax Unit:** `tu_individual_lv`

### 6. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 7. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `nDepChInTu#1>1`
  - **comp_perTU**: `70/30.5`
  - **#_level**: `tu_bfama_lv`
  - **output_var**: `i_bfamamy2`
  - **TAX_UNIT**: `tu_individual_lv`

### 8. Function: DefConst
  **Constants Defined:**
  - `$bfama_rate`: 0.8

### 9. Function: ArithOp
  **Formula:** `i_bfama * (i_bfamamy1 + i_bfamamy2)/12`
  **Output Variable:** `bfama_s`
  **Tax Unit:** `tu_individual_lv`

### 10. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `dgn=0`
  - **comp_perTU**: `70/30.5`
  - **output_var**: `i_bfamamy1`
  - **TAX_UNIT**: `tu_individual_lv`

### 11. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_bfama > 0`
  - **Tax Unit:** `tu_individual_lv`


---

## Policy: bfaba_lv
### 1. Function: DefConst
  **Constants Defined:**
  - `$bfaba_stdamt`: 421.17#y
  - `$bfaba_extraamt1`: 0#y
  - `$bfaba_extraamt2`: 0#y
  - `$bfaba_extraamt3`: 0#y

### 2. Function: DefTu
  - **name**: `tu_bfaba_lv`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild & LooseDepChild`
  - **DepChildCond**: `!IsParent & dag<99`
  - **ExtHeadCond**: `default & dgn=0`
  - **NoChildIfPartner**: `yes`
  - **NoChildIfHead**: `yes`
  - **StopIfNoHeadFound**: `no`

### 3. Function: BenCalc
  - **base**: `$bfaba_stdamt`
  - **comp_cond**: `dag00<=1 & isNtoMchild#3`
  - **comp_perElig**: `$base + $bfaba_extraamt3`
  - **#_N**: `3`
  - **#_M**: `99`
  - **output_var**: `bfaba_s`
  - **TAX_UNIT**: `tu_bfaba_lv`


---

## Policy: bfacc_lv
### 1. Function: DefVar
  - **i_yemcc**: `0`
  - **i_bfacc1**: `0`
  - **i_bfacc2**: `0`
  - **i_bfacc1_adj**: `0`
  - **i_bfaccmy2**: `0`
  - **i_bfaccmy1**: `0`
  - **i_bfacc2_adj**: `0`

### 2. Function: DefTu
  - **name**: `tu_bfacc1_lv`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild  & LooseDepChild`
  - **DepChildCond**: `dag00 <= $bfawk_age29`
  - **NoChildIfHead**: `yes`
  - **NoChildIfPartner**: `yes`
  - **ExtHeadCond**: `default & dgn=0`
  - **StopIfNoHeadFound**: `no`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsHeadOfTu &IsParentOfDepChild`
  - **Tax Unit:** `tu_bfacc1_lv`

### 4. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **uplim**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 5. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_lowlim**: `n/a`
  - **comp_uplim**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 6. Function: BenCalc
  - **comp_cond**: `IsHeadOfTu &  IsParentOfDepChild`
  - **comp_perTU**: `$bfacc_amt2`
  - **output_var**: `i_bfacc2`
  - **TAX_UNIT**: `tu_bfacc2_lv`

### 7. Function: ArithOp
  **Formula:** `i_bfacc1_adj + i_bfacc2_adj`
  **Output Variable:** `bfacc_s`
  **Tax Unit:** `tu_individual_lv`

### 8. Function: ArithOp
  **Formula:** `$bfacc_amt1`
  **Output Variable:** `i_bfacc1`
  **Tax Unit:** `tu_individual_lv`

### 9. Function: DefConst
  **Constants Defined:**
  - `$bfacc_rate`: n/a
  - `$bfacc_minamt`: n/a
  - `$bfacc_maxamt`: n/a
  - `$bfacc_amt1`: 171#m
  - `$bfacc_amt2`: 42.69#m

### 10. Function: DefTu
  - **name**: `tu_bfacc2_lv`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild  & LooseDepChild`
  - **DepChildCond**: `dag00 > $bfawk_age18 & dag00 < $bfawk_age36`
  - **NoChildIfHead**: `yes`
  - **NoChildIfPartner**: `yes`
  - **ExtHeadCond**: `default & dgn=0`
  - **StopIfNoHeadFound**: `no`

### 11. Function: BenCalc
  - **Comp_Cond**: `dag00 > $bfawk_age3 & dag00 <= $bfawk_age6`
  - **Comp_perTU**: `6`
  - **Output_Var**: `i_bfaccmy1`
  - **TAX_UNIT**: `tu_bfacc1_lv`
  - **UpLim**: `n/a`
  - **Run_Cond**: `GetDataIncomeYear < 2019`

### 12. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 13. Function: ArithOp
  **Formula:** `i_bfacc1 * (i_bfaccmy1 - i_bfamamy2)/12`
  **Output Variable:** `i_bfacc1_adj`
  **Tax Unit:** `tu_bfacc1_lv`

### 14. Function: BenCalc
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `i_bfaccmy2`
  - **TAX_UNIT**: `tu_bfacc2_lv`
  - **UpLim**: `n/a`
  - **Run_Cond**: `GetDataIncomeYear < 2019`

### 15. Function: ArithOp
  **Formula:** `i_bfacc2 * i_bfaccmy2/12`
  **Output Variable:** `i_bfacc2_adj`
  **Tax Unit:** `tu_bfacc2_lv`

### 16. Function: BenCalc
  - **Run_Cond**: `GetDataIncomeYear >= 2019`
  - **Comp_Cond**: `dag00 > $bfawk_age28 & dag00 <=$bfawk_age29`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_bfaccmy1`
  - **TAX_UNIT**: `tu_bfacc1_lv`

### 17. Function: BenCalc
  - **Run_Cond**: `GetDataIncomeYear >= 2019`
  - **Comp_Cond**: `dag00 > $bfawk_age34 & dag00 <= $bfawk_age35`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_bfaccmy2`
  - **TAX_UNIT**: `tu_bfacc2_lv`


---

## Policy: tin_lv
### 1. Function: DefConst
  **Constants Defined:**
  - `$tin_lv_rate`: n/a
  - `$tin_se_rate`: n/a
  - `$tin_kt_rate`: 0.255
  - `$tin_se_minamt`: 50#y
  - `$tin_rate1`: 0.255
  - `$tin_rate2`: 0.33
  - `$tin_rate3`: n/a
  - `$tin_addrate`: 0.03

### 2. Function: DefConst
  **Constants Defined:**
  - `$tintamm_stdamt`: 510#m
  - `$tintach_amt`: 250#m
  - `$tintamm_minamt`: n/a
  - `$tintamm_maxamt`: n/a
  - `$tintamm_lim1`: n/a
  - `$tintamm_lim2`: n/a

### 3. Function: DefConst
  **Constants Defined:**
  - `$PensAgeMale96`: 90
  - `$PensAgeFem96`: 85
  - `$tintape_penamt`: 1000#m

### 4. Function: DefVar
  - **i_tintb1**: `0`
  - **i_tintb2**: `0`
  - **i_tintb3**: `0`
  - **i_tintarm1**: `0`
  - **i_tintarm2**: `0`
  - **i_tintadiff**: `0`
  - **i_tin**: `0`
  - **i_tintyiy**: `0`
  - **i_tintlp**: `0`
  - **i_tintap**: `0`
  - **i_tintp**: `0`
  - **i_ded_xed_xhl**: `0`

### 5. Function: DefIl
  - **name**: `il_tintyee`
  - **yem**: `+`
  - **bhl**: `+`
  - **yot**: `+`

### 6. Function: DefIl
  - **name**: `il_tintyse`
  - **yse**: `+`
  - **ypr**: `+`

### 7. Function: DefIl
  - **name**: `il_tintype`
  - **poatx**: `+`
  - **psutx**: `+`
  - **pditx**: `+`

### 8. Function: DefIl
  - **name**: `il_tintyiy`
  - **yiytx**: `n/a`
  - **yiy**: `+`

### 9. Function: DefIl
  - **name**: `il_tinty`
  - **il_tintyee**: `+`
  - **il_tintyse**: `+`
  - **il_tintype**: `+`
  - **il_tintyiy**: `n/a`
  - **il_tintyiytx**: `+`

### 10. Function: DefTu
  - **name**: `tu_tin_lv`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild & Loose DepChild & DepParent`
  - **PartnerCond**: `Default & IsMarried & il_tinty#7< ($tintach_amt) & bun00_s#7=0 & poatx#7=0 & pditx#7=0 & yemmy=0 & ysemy=0`
  - **DepChildCond**: `default & (dag<18 | (dag<24 & dec>2)) & il_tinty#7< $tintach_amt & bun00_s#7=0 & poatx#7=0 & pditx#7=0`
  - **DepParentCond**: `default & il_tinty#7< $tintach_amt & bun00_s#7=0 & poatx#7=0 & pditx#7=0 & yemmy=0 & ysemy=0 & ( GetPartnerIncome#1<$tintach_amt & GetPartnerIncome#2=0 & GetPartnerIncome#3=0 & GetPartnerIncome#4=0 &  GetPartnerInfo#5=0 &  GetPartnerInfo#6=0)`
  - **#_income**: `pditx`
  - **#_info**: `ysemy`
  - **#_level**: `tu_individual_lv`
  - **HeadDefInc**: `il_tinty`
  - **NoChildIfHead**: `yes`
  - **NoChildIfPartner**: `yes`
  - **AssignDepChOfDependents**: `yes`
  - **AssignPartnerOfDependents**: `yes`

### 11. Function: BenCalc
  - **comp_cond**: `IsDepChild`
  - **comp_perElig**: `$tintach_amt`
  - **output_var**: `tintach_s`
  - **TAX_UNIT**: `tu_tin_lv`

### 12. Function: BenCalc
  - **comp_cond**: `IsDepParent & ddi > 0`
  - **comp_perElig**: `$tintach_amt`
  - **output_var**: `tintadp_s`
  - **TAX_UNIT**: `tu_tin_lv`

### 13. Function: BenCalc
  - **comp_cond**: `IsPartner & (ddi > 0| nDepChildrenOfCouple#1>=1 | (nChildrenOfCouple#2>=3 & nDepChildrenOfCouple#3>=1) |nChildrenOfCouple>=5 )`
  - **comp_perElig**: `$tintach_amt`
  - **output_var**: `tintasp_s`
  - **TAX_UNIT**: `tu_tin_lv`
  - **#_AgeMax**: `6`

### 14. Function: ArithOp
  **Formula:** `tscee_s`
  **Output Variable:** `tintaee_s`
  **Tax Unit:** `tu_individual_lv`

### 15. Function: ArithOp
  **Formula:** `tscse_s`
  **Output Variable:** `tintase_s`
  **Tax Unit:** `tu_individual_lv`

### 16. Function: ArithOp
  **Formula:** `xpp`
  **Output Variable:** `tintapv_s`
  **Tax Unit:** `tu_individual_lv`

### 17. Function: BenCalc
  - **comp_cond**: `IsHead#1 & il_tintype=0`
  - **Comp_perTU**: `$tintamm_stdamt`
  - **#_level**: `tu_tin_lv`
  - **output_var**: `tintamm_s`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Withdraw_Start**: `n/a`
  - **Withdraw_Rate**: `n/a`
  - **Withdraw_Base**: `n/a`

### 18. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `IsHead#1 & il_tintype>0 & ((dag<$PensAgeMale96 & dgn=1) | (dag< $PensAgeFem96 & dgn=0) | (liwwh<120))`
  - **comp_perElig**: `$tintape_penamt`
  - **#_level**: `tu_tin_lv`
  - **output_var**: `tintape_s`
  - **TAX_UNIT**: `tu_individual_lv`

### 19. Function: DefIl
  - **name**: `il_tinta`
  - **tintach_s**: `+`
  - **tintadp_s**: `+`
  - **tintasp_s**: `+`
  - **tintaee_s**: `+`
  - **tintapv_s**: `+`
  - **tintamm_s**: `+`
  - **tintape_s**: `+`
  - **tinxctaee_s**: `+`
  - **tintahl_s**: `+`
  - **tintaed_s**: `+`

### 20. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 21. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 22. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 23. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 24. Function: ArithOp
  **Formula:** `il_tintyiy`
  **Output Variable:** `i_tintb3`
  **Tax Unit:** `tu_tin_lv`
  **Run Condition:** `GetDataIncomeYear < 2018`

### 25. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 26. Function: BenCalc
  - **comp_cond**: `IsHead#1 & il_tintype>0 `
  - **comp_perElig**: `$tintape_penamt`
  - **#_level**: `tu_tin_lv`
  - **output_var**: `tintape_s`
  - **TAX_UNIT**: `tu_individual_lv`

### 27. Function: BenCalc
  - **Comp_Cond**: `!(yse != 0 & tscse_s = 0 & tscee_s = 0 & i_tintb1 = 0)`
  - **Comp_perTU**: `i_tin`
  - **Output_Var**: `tin_s`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Comp_LowLim**: `$tin_se_minamt`

### 28. Function: ArithOp
  **Formula:** `txcee_s`
  **Output Variable:** `tinxctaee_s`
  **Tax Unit:** `tu_individual_lv`

### 29. Function: ArithOp
  **Formula:** `txcse_s`
  **Output Variable:** `tinxctase_s`
  **Tax Unit:** `tu_individual_lv`

### 30. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 31. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **#_Level**: `n/a`

### 32. Function: DefIl
  - **Name**: `il_tintase`
  - **tintase_s**: `+`
  - **tinxctase_s**: `+`

### 33. Function: DefConst
  **Constants Defined:**
  - `$tin_upthres1`: $tscse_se_uplim1
  - `$tin_upthres2`: $tscse_se_uplim1
  - `$tin_share`: 1
  - `$tin_addthres`: 200000#y

### 34. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_lv`
  - **Output Variable:** `i_tintlp`
    - Band: Rate=`n/a`, Limit=``

### 35. Function: ArithOp
  **Formula:** `i_tintlp-i_tintap`
  **Output Variable:** `i_tintp`
  **Tax Unit:** `tu_individual_lv`

### 36. Function: ArithOp
  **Formula:** `(i_tintp+i_tintyiy)`
  **Output Variable:** `i_tin`
  **Tax Unit:** `tu_individual_lv`

### 37. Function: BenCalc
  - **Comp_Cond**: `i_tintb3>0`
  - **Comp_perTU**: `i_tintb3*$tin_kt_rate`
  - **Output_Var**: `i_tintyiy`
  - **TAX_UNIT**: `tu_individual_lv`

### 38. Function: BenCalc
  - **Comp_Cond**: `{xed00>0} | {xhl00>0}`
  - **Comp_perTU**: `min((xed00 + xhl00), (nPersInUnit * $tin_ded_uplimit))`
  - **Output_Var**: `i_ded_xed_xhl`
  - **TAX_UNIT**: `tu_tin_lv`

### 39. Function: BenCalc
  - **Comp_Cond**: `{xed00>0}`
  - **Comp_perTU**: `i_ded_xed_xhl* (xed00 /(xed00 + xhl00))`
  - **Output_Var**: `tintaed_s`
  - **TAX_UNIT**: `tu_tin_lv`

### 40. Function: Allocate
  - **Share**: `tintaed_s`
  - **Share_Between**: `{IsParent}`
  - **Output_Var**: `tintaed_s`
  - **TAX_UNIT**: `tu_tin_lv`

### 41. Function: BenCalc
  - **Comp_Cond**: `{xhl00>0}`
  - **Comp_perTU**: `i_ded_xed_xhl* (xhl00/(xed00 + xhl00))`
  - **Output_Var**: `tintahl_s`
  - **TAX_UNIT**: `tu_tin_lv`

### 42. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_lv`
  - **Output Variable:** `i_tintap`
    - Band: Rate=`n/a`, Limit=``

### 43. Function: DefIl
  - **Name**: `il_tintyiytx`
  - **yiytx**: `+`

### 44. Function: ArithOp
  **Formula:** `il_tintyiytx`
  **Output Variable:** `i_tintb3`
  **Tax Unit:** `tu_tin_lv`
  **Run Condition:** `GetDataIncomeYear >= 2018`

### 45. Function: DefConst
  **Constants Defined:**
  - `$tin_ded_uplimit`: 600#y

### 46. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_lv`
  - **Output Variable:** ``
    - Band: Rate=`$tin_addrate`, Limit=``


---

## Policy: bsamm_lv
### 1. Function: DefConst
  **Constants Defined:**
  - `$bsamm_ded_amt`: 0#m
  - `$bsamm_ret_amt`: n/a
  - `$bsamm_child_amt`: n/a
  - `$bsamm_couple_amt`: n/a
  - `$bsamm_child_addamt`: n/a
  - `$bsamm_stdamt1`: 166#m
  - `$bsamm_riga_amt`: n/a
  - `$bsamm_my`: 12
  - `$bsamm_thres1`: 377#m
  - `$bsamm_stdamt2`: 116#m
  - `$bsamm_thres2`: 264#m
  - `$yptmp_minrate1`: n/a
  - `$yptmp_minrate2`: n/a

### 2. Function: DefVar
  - **i_bsail**: `0`
  - **i_gmipe**: `0`
  - **i_gmich**: `0`
  - **i_gmi**: `0`
  - **i_bsamm**: `0`
  - **i_yptmp**: `0`

### 3. Function: DefIl
  - **name**: `il_bsamm`
  - **yem**: `+`
  - **yse**: `+`
  - **ypr**: `+`
  - **ypt**: `+`
  - **ypp**: `+`
  - **yiy**: `+`
  - **yot**: `+`
  - **poatx**: `+`
  - **poass_s**: `+`
  - **pditx**: `+`
  - **pdiss_s**: `+`
  - **pdint**: `+`
  - **psutx**: `+`
  - **psuss_s**: `+`
  - **bun00_s**: `+`
  - **bhl**: `+`
  - **bed**: `+`
  - **bfana_s**: `n/a`
  - **bfaba_s**: `n/a`
  - **bfama_s**: `+`
  - **bfapl_s**: `+`
  - **bfacc_s**: `+`
  - **bfawk_s**: `+`
  - **bsafu**: `n/a`
  - **ils_sicee**: `-`
  - **ils_sicse**: `-`
  - **tin_s**: `-`
  - **txcee_s**: `-`
  - **txcse_s**: `-`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **bwkmcch_s**: `n/a`
  - **bfaam**: `+`

### 4. Function: BenCalc
  - **comp_cond**: `bfawk_s<=$bsamm_ded_amt`
  - **comp_perTU**: `il_bsamm-bfawk_s`
  - **output_var**: `i_bsail`
  - **TAX_UNIT**: `tu_individual_lv`

### 5. Function: DefTu
  - **name**: `tu_bsamm_lv`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild  & LooseDepChild`
  - **DepChildCond**: `default & dag<18`
  - **NoChildIfHead**: `yes`
  - **NoChildIfPartner**: `yes`

### 6. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 7. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **uplim**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 8. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 9. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_level**: `n/a`
  - **#_income**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 10. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 11. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 12. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 13. Function: BenCalc
  - **comp_cond**: `i_bsail < ($bsamm_stdamt1 + $bsamm_stdamt2 * (nPersonsInTu - 1))  & afc <= $bsamm_thres1`
  - **comp_perTU**: `($bsamm_stdamt1 + $bsamm_stdamt2 * (nPersonsInTu - 1)) - i_bsail`
  - **uplim**: `n/a`
  - **output_var**: `i_bsamm`
  - **TAX_UNIT**: `tu_household_lv`

### 14. Function: ArithOp
  **Formula:** `i_bsamm*$bsamm_my/12`
  **Output Variable:** `bsamm_s`
  **Tax Unit:** `tu_household_lv`

### 15. Function: Allocate
  - **share**: `bsamm_s`
  - **output_var**: `bsamm_s`
  - **TAX_UNIT**: `tu_household_lv`

### 16. Function: BenCalc *(Switch: n/a)*
  - **Comp_perTU**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Comp_LowLim**: `n/a`

### 17. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yptmp>0`
  - **Tax Unit:** `tu_individual_lv`

### 18. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 19. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 20. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `(i_bsamm_cumpers > $bsamm_target_count & bsammyn_a = -1)  | bsammyn_a = 0`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bsamm_s`
  - **TAX_UNIT**: `tu_individual_lv`

### 21. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsamm_elig`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsamm_sort`
  - **OutputVar**: `i_bsamm_cumpers`
  - **TAX_UNIT**: `tu_individual_lv`

### 22. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsamm_target_count`: $sum_i_bsamm_elig * $bsamm_rate

### 23. Function: Totals *(Switch: off)*
  - **Agg**: `i_bsamm_elig`
  - **Use_Weights**: `yes`
  - **Varname_Sum**: `$sum`
  - **TAX_UNIT**: `tu_individual_lv`

### 24. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsamm_rate`: min($bsamm_BCA_rate,$bsamm_BTA_rate)

### 25. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsamm_BCA_rate`: 0.682

### 26. Function: Totals *(Switch: off)*
  - **Agg**: `n/a`
  - **Use_Weights**: `n/a`
  - **Varname_Sum**: `n/a`
  - **TAX_UNIT**: `n/a`

### 27. Function: DefVar *(Switch: off)*
  - **i_bsamm_bca_take**: `n/a`

### 28. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `n/a`
  - **SummingWeighted**: `n/a`
  - **SortingVar**: `n/a`
  - **OutputVar**: `n/a`
  - **TAX_UNIT**: `n/a`

### 29. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsamm_targetBCA_count`: n/a

### 30. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `bsamm_s >= $bsamm_minamt`
  - **Comp_perTU**: `1`
  - **Comp_perElig**: `i_bsamm_sort`
  - **Output_Var**: `i_bsamm_sort`
  - **TAX_UNIT**: `tu_individual_lv`

### 31. Function: DefVar *(Switch: off)*
  - **i_bsamm_sort**: `i_bsamm_rand`
  - **i_bsamm_amt**: `bsamm_s`
  - **i_bsamm_elig**: `bsamm_s > 0`
  - **i_bsamm_cumexp**: `0`
  - **i_bsamm_cumpers**: `0`

### 32. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsamm_minamt`: 0

### 33. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsamm_BTA_rate`: 1


---

## Policy: bho_lv
### 1. Function: DefVar
  - **i_xhcmax**: `0`
  - **i_amrarmax**: `0`

### 2. Function: DefIl
  - **name**: `il_bho`
  - **i_bsail**: `+`
  - **bsamm_s**: `+`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgur=1`
  - **Tax Unit:** `tu_individual_lv`

### 4. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `nPersInUnit>=4`
  - **comp_perElig**: `$xhcmax_urb_amt4`
  - **output_var**: `i_xhcmax`
  - **TAX_UNIT**: `tu_household_lv`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `drgur00=3`
  - **Tax Unit:** `tu_individual_lv`

### 6. Function: BenCalc
  - **who_must_be_elig**: `all`
  - **comp_cond**: `nPersInUnit>=4`
  - **comp_perElig**: `$xhcmax_rur_amt4`
  - **output_add_var**: `i_xhcmax`
  - **TAX_UNIT**: `tu_household_lv`

### 7. Function: Elig
  **Eligibility Check:**
  - **Condition:** `afc <= $bsamm_thres1 & ((dgn=1 & (dag00 >= $MajorityAge & dag00<$PensAgeMale &  pdiss_s#1=0 &  pditx#1=0)) | (dgn=0 & (dag00 >= $MajorityAge & dag00<$PensAgeFem &  pdiss_s#1=0 & pditx#1=0 )))`
  - **Tax Unit:** `tu_household_lv`
  **Run Condition:** `n/a`

### 8. Function: ArithOp
  **Formula:** `$bho_coef1*($bsamm_stdamt1 + $bsamm_stdamt2 * (nPersonsInTu - 1)) + xhc#1 - il_bho`
  **Output Variable:** `bho_s`
  **Tax Unit:** `tu_household_lv`
  **Run Condition:** `n/a`

### 9. Function: Allocate
  - **share**: `bho_s`
  - **output_var**: `bho_s`
  - **TAX_UNIT**: `tu_household_lv`

### 10. Function: BenCalc *(Switch: off)*
  - **run_cond**: `IsUsedDatabase#1`
  - **#_DatabaseName**: `lv_2010_a?.txt`
  - **comp_cond**: `bho>0`
  - **comp_perTU**: `bho_s`
  - **output_var**: `bho_s`
  - **TAX_UNIT**: `tu_individual_lv`

### 11. Function: DefConst
  **Constants Defined:**
  - `$xhcmax_urb_amt1`: 128.75#m
  - `$xhcmax_urb_amt2`: 86.09#m
  - `$xhcmax_urb_amt3`: 57.16#m
  - `$xhcmax_urb_amt4`: 48.85#m
  - `$xhcmax_rur_amt1`: 90.02#m
  - `$xhcmax_rur_amt2`: 61.32#m
  - `$xhcmax_rur_amt3`: 43.85#m
  - `$xhcmax_rur_amt4`: 36.11#m

### 12. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$bho_thres1`: n/a
  - `$bho_thres2`: n/a
  - `$bho_dmc2_thr1`: n/a
  - `$bho_dmc3_thr1`: n/a
  - `$bho_dmc3_thr2`: n/a
  - `$bho_dmc4_thr1`: n/a
  - `$bho_dmc4_thr2`: n/a
  - `$bho_dmc5_thr1`: n/a
  - `$bho_dmc5_thr2`: n/a
  - `$bho_dmc6_thr1`: n/a
  - `$bho_dmc6_thr2`: n/a
  - `$bho_dmc6_thr3`: n/a
  - `$bho_dmc6_thr4`: n/a
  - `$bho_dmc6_thr5`: n/a
  - `$bho_dmc7_thr1`: n/a
  - `$bho_dmc7_thr2`: n/a
  - `$bho_dmc7_thr3`: n/a
  - `$bho_dmc8_thr1`: n/a
  - `$bho_dmc8_thr2`: n/a
  - `$bho_dmc9_thr1`: n/a
  - `$bho_dmc9_thr2`: n/a
  - `$bho_dmc9_thr3`: n/a

### 13. Function: DefConst
  **Constants Defined:**
  - `$bho_coef1`: 1.3
  - `$bho_coef2`: 2.1
  - `$bho_coef3`: 1.7
  - `$bho_coef4`: 1.7

### 14. Function: Elig
  **Eligibility Check:**
  - **Condition:** `afc <= $bsamm_thres1 & ((dgn=1 & (dag00>=$PensAgeMale | pdiss_s#1>0 | pditx#1>0)) | (dgn=0 & ( dag00>=$PensAgeFem | pdiss_s#1>0 | pditx#1>0 )))`
  - **Tax Unit:** `tu_household_lv`

### 15. Function: BenCalc
  - **Who_Must_Be_Elig**: `all`
  - **Comp_Cond**: `NPersInTu>1`
  - **Comp_perTU**: `$bho_coef3*($bsamm_stdamt1 + $bsamm_stdamt2 * (nPersonsInTu - 1)) + xhc#1 - il_bho`
  - **LowLim**: `0`
  - **#_UpLim**: `i_xhcmax`
  - **Output_Add_Var**: `bho_s`
  - **TAX_UNIT**: `tu_household_lv`
  - **UpLim**: `min(xhc,i_xhcmax)`

### 16. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 17. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 18. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 19. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 20. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 21. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 22. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 23. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 24. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 25. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 26. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 27. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 28. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 29. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 30. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 31. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 32. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 33. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 34. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 35. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 36. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 37. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 38. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 39. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 40. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 41. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`
  **Run Condition:** `n/a`

### 42. Function: ArithOp
  **Formula:** `min(amrar , 32+18 * (nPersInUnit-1))`
  **Output Variable:** `i_amrarmax`
  **Tax Unit:** `tu_household_lv`

### 43. Function: BenCalc
  - **Who_Must_Be_Elig**: `all`
  - **Comp_Cond**: `i_amrarmax > 45`
  - **Comp_perTU**: `max(45*7, i_amrarmax * 5)`
  - **Output_Var**: `i_xhcmax`
  - **TAX_UNIT**: `tu_household_lv`

### 44. Function: BenCalc
  - **Who_Must_Be_Elig**: `all`
  - **Comp_Cond**: `i_amrarmax > 0`
  - **Comp_perTU**: `i_amrarmax * 5`
  - **Output_Add_Var**: `i_xhcmax`
  - **TAX_UNIT**: `tu_household_lv`

### 45. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `(i_bho_cumpers > $bho_target_count & bhoyn_a = -1)  | bhoyn_a = 0`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bho_s`
  - **TAX_UNIT**: `tu_individual_lv`

### 46. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bho_elig`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bho_sort`
  - **OutputVar**: `i_bho_cumpers`
  - **TAX_UNIT**: `tu_individual_lv`

### 47. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bho_target_count`: $sum_i_bho_elig * $bho_rate

### 48. Function: Totals *(Switch: off)*
  - **Agg**: `i_bho_elig`
  - **Use_Weights**: `yes`
  - **Varname_Sum**: `$sum`
  - **TAX_UNIT**: `tu_individual_lv`

### 49. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bho_rate`: min($bho_BCA_rate,$bho_BTA_rate)

### 50. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bho_BCA_rate`: 0.541

### 51. Function: Totals *(Switch: off)*
  - **Agg**: `n/a`
  - **Use_Weights**: `n/a`
  - **Varname_Sum**: `n/a`
  - **TAX_UNIT**: `n/a`

### 52. Function: DefVar *(Switch: off)*
  - **i_bho_bca_take**: `n/a`

### 53. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `n/a`
  - **SummingWeighted**: `n/a`
  - **SortingVar**: `n/a`
  - **OutputVar**: `n/a`
  - **TAX_UNIT**: `n/a`

### 54. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bho_targetBCA_count`: n/a

### 55. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `bho_s >= $bho_minamt`
  - **Comp_perTU**: `1`
  - **Comp_perElig**: `i_bho_sort`
  - **Output_Var**: `i_bho_sort`
  - **TAX_UNIT**: `tu_individual_lv`

### 56. Function: DefVar *(Switch: off)*
  - **i_bho_sort**: `i_bho_rand`
  - **i_bho_amt**: `bho_s`
  - **i_bho_elig**: `bho_s > 0`
  - **i_bho_cumexp**: `0`
  - **i_bho_cumpers**: `0`

### 57. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bho_minamt`: 0

### 58. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bho_BTA_rate`: 1

### 59. Function: Elig
  **Eligibility Check:**
  - **Condition:** `afc <= $bsamm_thres1 & nDepChildrenInTu#2 > 0 & ((dgn=1 & (dag00>=$PensAgeMale | pdiss_s#1>0 | pditx#1>0)) | (dgn=0 & ( dag00>=$PensAgeFem | pdiss_s#1>0 | pditx#1>0 )) | dag00 < $MajorityAge)`
  - **Tax Unit:** `tu_household_lv`

### 60. Function: ArithOp
  **Formula:** `$bho_coef4*($bsamm_stdamt1 + $bsamm_stdamt2 * (nPersonsInTu - 1)) + xhc#1 - il_bho`
  **Output Variable:** ``
  **Tax Unit:** `tu_household_lv`


---

## Policy: output_std_lv
### 1. Function: DefOutput
  - **file**: `LV_2025_std`
  - **vargroup**: `e*`
  - **ilgroup**: `il_*`
  - **unitinfo_tu**: `n/a`
  - **unitinfo_id**: `n/a`
  - **nDecimals**: `2`
  - **TAX_UNIT**: `tu_individual_lv`
  - **VarGroup**: `i_*`
  - **UnitInfo_TU**: `n/a`
  - **UnitInfo_Id**: `n/a`


---

## Policy: output_std_hh_lv *(Switch: off)*
### 1. Function: DefOutput
  - **file**: `LV_2025_std_hh`
  - **var**: `dwt`
  - **TAX_UNIT**: `tu_hh_oecd_co`
  - **ILGroup**: `ils*`


---

## Policy: bfawk_lv
### 1. Function: DefVar
  - **i_yemwk**: `0`
  - **i_bfawk**: `0`
  - **i_bfawk_n1**: `0`
  - **i_bfawk_n2**: `0`
  - **Var_Monetary**: `no`
  - **i_bfawkmy**: `0`
  - **i_yemwk01**: `0`
  - **i_bfawk01**: `0`
  - **i_bfawkmy01**: `0`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsHeadOfTu#1 & liwwh>3 & IsParentOfDepChild#1 & nDepChInTu#1 > 0`
  - **Tax Unit:** `tu_individual_lv`

### 3. Function: BenCalc
  - **comp_cond**: `yempv01>0 & tscse_s>0`
  - **comp_perTU**: `yempv01`
  - **uplim**: `$tscse_se_uplim0`
  - **output_var**: `i_yemwk01`
  - **TAX_UNIT**: `tu_individual_lv`

### 4. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_yemwk>0`
  - **comp_perTU**: `i_yemwk*$bfawk_rate2`
  - **comp_lowlim**: `n/a`
  - **output_var**: `i_bfawk`
  - **TAX_UNIT**: `tu_individual_lv`

### 5. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 6. Function: DefConst
  **Constants Defined:**
  - `$bfawk_rate1`: 0.6
  - `$bfawk_minamt`: n/a
  - `$bfawk_rate2`: 0.4375
  - `$bfawk_lv_rate`: 0.75

### 7. Function: DefTu
  - **name**: `tu_bfawk_lv`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild  & LooseDepChild`
  - **DepChildCond**: `dag00<= $bfawk_age29`
  - **NoChildIfHead**: `yes`
  - **NoChildIfPartner**: `yes`
  - **HeadDefInc**: `i_yemwk`
  - **StopIfNoHeadFound**: `no`
  - **ExtHeadCond**: `n/a`
  - **LoneParentCond**: `default`

### 8. Function: BenCalc
  - **Comp_Cond**: `dgn = 1 & i_yemwk01 > 0 & !IsLoneParent`
  - **Comp_perTU**: `i_yemwk01*$bfawk_lv_rate`
  - **Output_Var**: `i_yemwk`
  - **TAX_UNIT**: `tu_individual_lv`

### 9. Function: BenCalc
  - **Comp_Cond**: `dag00 > $bfawk_age3 & dag00 <= $bfawk_age6`
  - **Comp_perTU**: `6`
  - **Output_Var**: `i_bfawkmy`
  - **TAX_UNIT**: `tu_bfawk_lv`
  - **Who_Must_Be_Elig**: `one`
  - **Run_Cond**: `GetDataIncomeYear < 2019`
  - **UpLim**: `12`

### 10. Function: ArithOp
  **Formula:** `i_bfawk * (i_bfawkmy - i_bfamamy2)/12`
  **Output Variable:** `bfawk_s`
  **Tax Unit:** `tu_bfawk_lv`

### 11. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_bfawk > 0 `
  - **Tax Unit:** `tu_bfawk_lv`

### 12. Function: BenCalc
  - **Run_Cond**: `GetDataIncomeYear >= 2019`
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dag00 > $bfawk_age17 & dag00 <= $bfawk_age18`
  - **Comp_perTU**: `9`
  - **UpLim**: `12`
  - **Output_Var**: `i_bfawkmy`
  - **TAX_UNIT**: `tu_bfawk_lv`

### 13. Function: DefTu
  - **name**: `tu_bfawk01_lv`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild  & LooseDepChild`
  - **DepChildCond**: `dag00 > $bfawk_age15 & dag00 <= $bfawk_age24`
  - **LoneParentCond**: `default`
  - **NoChildIfHead**: `yes`
  - **NoChildIfPartner**: `yes`
  - **ExtHeadCond**: `dgn = 0`
  - **StopIfNoHeadFound**: `no`

### 14. Function: DefTu
  - **name**: `tu_bfawk02_lv`
  - **type**: `SUBGROUP`
  - **members**: `Partner & OwnDepChild  & LooseDepChild`
  - **DepChildCond**: `dag00 > $bfawk_age15 & dag00 <= $bfawk_age24`
  - **LoneParentCond**: `default`
  - **NoChildIfHead**: `yes`
  - **NoChildIfPartner**: `yes`
  - **ExtHeadCond**: `dgn = 1`
  - **StopIfNoHeadFound**: `no`

### 15. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(IsHeadOfTu#1 | IsPartner#1) & liwwh>3 & IsParentOfDepChild#1 & nDepChInTu#1 > 0`
  - **Tax Unit:** `tu_individual_lv`

### 16. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `i_yemwk01>0`
  - **comp_perTU**: `i_yemwk01*$bfawk_rate2`
  - **output_var**: `i_bfawk01`
  - **TAX_UNIT**: `tu_individual_lv`

### 17. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsHeadOfTu#1 & !(IsLoneParentOfDepChild#1) &  liwwh>3 & IsParentOfDepChild#1 & nDepChInTu#1 > 0`
  - **Tax Unit:** `tu_individual_lv`

### 18. Function: BenCalc
  - **Run_Cond**: `GetDataIncomeYear < 2019`
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dag00 > $bfawk_age15 & dag00 <= $bfawk_age24`
  - **Comp_perTU**: `2`
  - **Output_Var**: `i_bfawkmy01`
  - **UpLim**: `2`
  - **TAX_UNIT**: `tu_bfawk01_lv`

### 19. Function: BenCalc
  - **Run_Cond**: `GetDataIncomeYear >= 2019`
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dag00 > $bfawk_age16 & dag00 <= $bfawk_age24`
  - **Comp_perTU**: `2`
  - **Output_Var**: `i_bfawkmy01`
  - **UpLim**: `2`
  - **TAX_UNIT**: `tu_bfawk01_lv`

### 20. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsHeadOfTu#1 & !(IsLoneParentOfDepChild#1) &  liwwh>3 & IsParentOfDepChild#1 & nDepChInTu#1 > 0`
  - **Tax Unit:** `tu_individual_lv`

### 21. Function: BenCalc
  - **Run_Cond**: `GetDataIncomeYear < 2019`
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dag00 > $bfawk_age18 & dag00 <= $bfawk_age24`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `i_bfawkmy01`
  - **UpLim**: `2`
  - **TAX_UNIT**: `tu_bfawk02_lv`

### 22. Function: BenCalc
  - **Run_Cond**: `GetDataIncomeYear >= 2019`
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dag00 > $bfawk_age18 & dag00 <= $bfawk_age24`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `i_bfawkmy01`
  - **UpLim**: `2`
  - **TAX_UNIT**: `tu_bfawk02_lv`

### 23. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsLoneParentOfDepChild#1 & liwwh>3 & IsParentOfDepChild#1 & nDepChInTu#1 > 0`
  - **Tax Unit:** `tu_individual_lv`

### 24. Function: BenCalc
  - **Run_Cond**: `GetDataIncomeYear < 2019`
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dag00 > $bfawk_age18 & dag00 <= $bfawk_age24`
  - **Comp_perTU**: `4`
  - **Output_Add_Var**: `i_bfawkmy01`
  - **UpLim**: `4`
  - **TAX_UNIT**: `tu_bfawk_lv`

### 25. Function: BenCalc
  - **Run_Cond**: `GetDataIncomeYear >= 2019`
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dag00 > $bfawk_age18 & dag00 <= $bfawk_age24`
  - **Comp_perTU**: `4`
  - **Output_Add_Var**: `i_bfawkmy01`
  - **UpLim**: `4`
  - **TAX_UNIT**: `tu_bfawk_lv`

### 26. Function: ArithOp
  **Formula:** `i_bfawk01*i_bfawkmy01/12`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_lv`


---

## Policy: SetDefault_lv
### 1. Function: SetDefault
  - **Dataset**: `lv_20*`
  - **lhw_a**: `0`
  - **yempv_a**: `0`
  - **liwmy_a**: `0`
  - **lnu**: `0`
  - **lhwsr_a**: `0`
  - **bwkmcmy_a**: `0`
  - **lmc20**: `0`
  - **lmc**: `0`
  - **yemmy20_a**: `0`
  - **yemmy19_a**: `0`
  - **yemmy18_a**: `0`
  - **lhw20_a**: `0`
  - **lhw19_a**: `0`
  - **lhw18_a**: `0`
  - **yem20_a**: `0`
  - **yem19_a**: `0`
  - **yem18_a**: `0`
  - **lma20**: `0`
  - **lma19**: `0`
  - **lma18**: `0`
  - **lma**: `0`
  - **yem_a**: `0`
  - **yemmy_a**: `0`
  - **bpeecsu**: `0`
  - **bpeecdi**: `0`
  - **bpeecoa**: `0`
  - **bpeec02**: `0`
  - **bpeec**: `0`
  - **bfaec**: `0`
  - **bhoht**: `0`
  - **bpeec01**: `0`
  - **bpeecoa_01**: `0`
  - **bpeecdi_01**: `0`
  - **bpeecsu
_01**: `0`

### 2. Function: SetDefault
  - **dataset**: `lv_2008_a?`
  - **bsafu**: `bsa`
  - **bsaot**: `0`
  - **bun00**: `bun`
  - **bunot**: `0`
  - **bfaot**: `0`
  - **yempv01**: `yivwg01`
  - **bfaba**: `0`
  - **bfacc**: `0`
  - **bfana**: `bfa`
  - **bfapl**: `0`
  - **bfawk**: `0`
  - **ydses_o**: `0`
  - **kfbcc**: `0`
  - **bsamm**: `0`
  - **yivwg02**: `0`
  - **tscer**: `0`
  - **bfama**: `0`
  - **dag00**: `dag`
  - **yptmp**: `0`
  - **ymwdt**: `0`
  - **bfa00**: `0`
  - **xed00**: `0`
  - **xhl00**: `0`
  - **bfaam**: `0`
  - **tbs**: `0`
  - **bhoht**: `0`
  - **bpeec01**: `0`
  - **bpeecoa_01**: `0`
  - **bpeecdi_01**: `0`
  - **bpeecsu_01**: `0`
  - **bfaec**: `0`
  - **bpeec02**: `0`
  - **bpeec**: `0`
  - **bpeecoa**: `0`
  - **bpeecdi**: `0`
  - **bpeecsu**: `0`

### 3. Function: SetDefault
  - **yempv01**: `yivwg02`
  - **liwftmy**: `liwmy`
  - **dag00**: `dag`
  - **ymwdt**: `0`
  - **xed00**: `0`
  - **xhl00**: `0`
  - **bfaam**: `0`
  - **dmc**: `1`
  - **kivho**: `0`
  - **tbs**: `0`
  - **bhoht**: `0`
  - **bpeec01**: `0`
  - **bpeecoa_01**: `0`
  - **bpeecdi_01**: `0`
  - **bpeecsu_01**: `0`
  - **Dataset**: `lv_202?_?*`
  - **bfaec**: `0`
  - **bpeec02**: `0`
  - **bpeec**: `0`
  - **bpeecoa**: `0`
  - **bpeecdi**: `0`
  - **bpeecsu**: `0`

### 4. Function: SetDefault
  - **dataset**: `*training_data`
  - **yemmy**: `12`
  - **poatx**: `poa`
  - **psutx**: `psu`
  - **pditx**: `pdi`
  - **dag00**: `dag`
  - **ysemy**: `12`
  - **bwkmceemy_s**: `n/a`
  - **bwkmcsemy_s**: `n/a`
  - **yemmwmy_s**: `n/a`
  - **ysemwmy_s**: `n/a`
  - **ysemw_s**: `n/a`
  - **dmc**: `1`

### 5. Function: DefConst
  **Constants Defined:**
  - `$uaa`: 0

### 6. Function: SetDefault
  - **Dataset**: `lv_2012_a*`
  - **yptmp**: `0`

### 7. Function: SetDefault
  - **Dataset**: `lv_20*`
  - **bwkmceemy_s**: `0`
  - **bwkmcsemy_s**: `0`
  - **yemmwmy_s**: `0`
  - **ysemwmy_s**: `0`
  - **ysemw_s**: `0`
  - **bwkmcch_s**: `0`

### 8. Function: SetDefault
  - **Dataset**: `lv_20*`
  - **ydsyc_a**: `0`

### 9. Function: SetDefault
  - **Dataset**: `*`
  - **bsammyn_a**: `-1`
  - **bhoyn_a**: `-1`

### 10. Function: SetDefault
  - **dataset**: `*hhot`
  - **bhoht**: `n/a`

### 11. Function: DefIl
  - **Run_Cond**: `IsUsedDatabase#1`
  - **#_DataBasename**: `lv_20??_??_????_??_??`
  - **Name**: `il_xs_hl06`
  - **Warn_If_NonMonetary**: `no`
  - **RegExp_Def**: `xs06[0-9]+`
  - **RegExp_Factor**: `+`

### 12. Function: ArithOp
  **Formula:** `il_xs_hl06 * yds`
  **Output Variable:** `xhl00`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `IsUsedDatabase#1`

### 13. Function: DefIl
  - **Run_Cond**: `IsUsedDatabase#1`
  - **#_DataBasename**: `lv_20??_??_????_??_??`
  - **Name**: `il_xs_hl10`
  - **Warn_If_NonMonetary**: `no`
  - **RegExp_Def**: `xs10[0-9]+`
  - **RegExp_Factor**: `+`

### 14. Function: ArithOp
  **Formula:** `il_xs_hl10 * yds`
  **Output Variable:** `xed00`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `IsUsedDatabase#1`


---

## Policy: uprate_bands_lv
### 1. Function: DefConst
  **Constants Defined:**
  - `$Index2013`: 1.0400
  - `$Index2014`: 1.0274
  - `$IndexA_2008`: 1.1068
  - `$Limit2_2007`: 5 * $pss_amt
  - `$Limit1_2007`: 3 * $pss_amt
  - `$IndexD_2007`: 1.0542
  - `$IndexC_2007`: 1.1011
  - `$IndexB_2007`: 1.1566
  - `$IndexA_2007`: 1.0445
  - `$Limit2014`: 285#m
  - `$Limit2013`: 284.57#m
  - `$Limit2_2008`: 5 * $pss_amt
  - `$Limit1_2008`: 213.43#m
  - `$IndexD_2008`: 1.0457
  - `$IndexC_2008`: 1.1574
  - `$IndexB_2008`: 1.1731
  - `$Index2015`: 1.0158
  - `$Limit2015`: 311#m
  - `$Index2016`: 1.0186
  - `$Limit2016`: 332#m
  - `$Index2017`: 1.0439
  - `$Limit2017`: 349#m
  - `$Index2018_1`: 1.0590
  - `$Index2018_2`: 1.0655
  - `$Index2018_3`: 1.0720
  - `$Limit2018`: 382#m
  - `$Index2019_3`: 1.0891
  - `$Index2019_2`: 1.0805
  - `$Index2019_1`: 1.0719
  - `$Limit2019`: 420#m
  - `$Index2019_4`: 1.0977
  - `$Index2020_1`: 1.038
  - `$Index2020_2`: 1.0446
  - `$Index2020_3`: 1.0512
  - `$Index2020_4`: 1.0578
  - `$Limit2020`: 454#m
  - `$Index2021_1`: 1.0423
  - `$Index2021_2`: 1.0451
  - `$Index2021_3`: 1.0479
  - `$Index2021_4
`: 1.0507
  - `$Limit2021`: 470#m
  - `$Index2022_1`: 1.2287
  - `$Index2022_2`: 1.2314
  - `$Index2022_3`: 1.2341
  - `$Index2022_4`: 1.2369
  - `$Limit2022`: 534#m
  - `$Index2023_1`: 1.0640
  - `$Index2023_2`: 1.0640
  - `$Index2023_3`: 1.0640
  - `$Index2023_4`: 1.0640
  - `$Limit2023`: 609#m
  - `$Index2024_1`: 1.0654
  - `$Index2024_2`: 1.0771
  - `$Index2024_3`: 1.0887
  - `$Index2024_4`: 1.1004
  - `$Limit2024`: 683#m
  - `$Index2025_1`: 1.0635
  - `$Index2025_2`: 1.0686
  - `$Index2025_3`: 1.0737
  - `$Index2025_4`: 1.0787
  - `$Limit2025`: 1488#m

### 2. Function: DefVar
  - **i_pen2013_01**: `0`
  - **i_pen2013_12**: `0`
  - **i_pen2013_av**: `0`
  - **i_pen2014_01**: `0`
  - **i_pen2014_12**: `0`
  - **i_pen2008_12**: `0`
  - **i_pen2008_04**: `0`
  - **i_pen2008_01**: `0`
  - **i_pen2007_04**: `0`
  - **i_pen2006_av**: `0`
  - **i_pen2007_12**: `0`
  - **i_pen2007_01**: `0`
  - **i_pen2014_av**: `0`
  - **i_pen2008_av**: `0`
  - **i_pen2009_av**: `0`
  - **i_pen2009_01**: `0`
  - **i_pen2012_av**: `0`
  - **i_pen2011_av**: `0`
  - **i_pen2010_av**: `0`
  - **i_pen2007_av**: `0`
  - **i_pen2015_av**: `0`
  - **i_pen2015_01**: `0`
  - **i_pen2015_12**: `0`
  - **i_pen2016_01**: `0`
  - **i_pen2016_12**: `0`
  - **i_pen2016_av**: `0`
  - **i_pen2017_01**: `0`
  - **i_pen2017_12**: `0`
  - **i_pen2017_av**: `0`
  - **i_pen2018_01**: `0`
  - **i_pen2018_12**: `0`
  - **i_pen2018_av**: `0`
  - **i_pen2019_01**: `0`
  - **i_pen2019_12**: `0`
  - **i_pen2019_av**: `0`
  - **i_pen2020_01**: `0`
  - **i_pen2020_12**: `0`
  - **i_pen2020_av**: `0`
  - **i_pen2021_01**: `0`
  - **i_pen2021_12**: `0`
  - **i_pen2022_01**: `0`
  - **i_pen2022_12**: `0`
  - **i_pen2021_av**: `0`
  - **i_pen2022_av**: `0`
  - **i_pen2023_01**: `0`
  - **i_pen2023_12**: `0`
  - **i_pen2023_av**: `0`
  - **i_pen2024_01**: `0`
  - **i_pen2024_12**: `0`
  - **i_pen2024_av**: `0`
  - **i_pen2025_01**: `0`
  - **i_pen2025_12**: `0`
  - **i_pen2025_av**: `0`

### 3. Function: BenCalc
  - **Comp_Cond**: `i_pen2013_01 > $Limit2013`
  - **Comp_perTU**: `i_pen2013_01`
  - **Output_Var**: `i_pen2013_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 4. Function: ArithOp
  **Formula:** `(9 * i_pen2025_01 + 3 * i_pen2025_12)/12`
  **Output Variable:** `i_pen2025_av`
  **Tax Unit:** `tu_individual_lv`

### 5. Function: ArithOp
  **Formula:** `i_pen2013_12`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2014 & GetDataIncomeYear <= 2012`

### 6. Function: BenCalc
  - **Comp_Cond**: `i_pen2014_01 > $Limit2014`
  - **Comp_perTU**: `i_pen2014_01 + $Limit2014 * ($Index2014 - 1)`
  - **Output_Var**: `i_pen2014_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 7. Function: ArithOp
  **Formula:** `i_pens`
  **Output Variable:** `i_pen2007_01`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2007 & GetDataIncomeYear <= 2006`

### 8. Function: BenCalc
  - **Comp_Cond**: `i_pen2007_01 > $Limit1_2007`
  - **Comp_perTU**: `i_pen2007_01`
  - **Output_Var**: `i_pen2007_04`
  - **TAX_UNIT**: `tu_individual_lv`

### 9. Function: BenCalc
  - **Comp_Cond**: `i_pen2007_04 >$Limit2_2007`
  - **Comp_perTU**: `i_pen2007_04`
  - **Output_Var**: `i_pen2007_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 10. Function: BenCalc
  - **Comp_Cond**: `i_pen2008_01 > $Limit1_2008`
  - **Comp_perTU**: `i_pen2008_01`
  - **Output_Var**: `i_pen2008_04`
  - **TAX_UNIT**: `tu_individual_lv`

### 11. Function: BenCalc
  - **Comp_Cond**: `i_pen2008_04 >$Limit2_2008`
  - **Comp_perTU**: `i_pen2008_04`
  - **Output_Var**: `i_pen2008_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 12. Function: DefVar
  - **i_pens**: `0`
  - **i_psutx**: `psutx`
  - **i_pditx**: `pditx`
  - **i_poatx**: `poatx`

### 13. Function: Loop
  - **Last_Func**: `0ad174dc-d04f-44ad-8026-e5313b907a2b`
  - **First_Func**: `eb3971fe-dc00-4eca-9311-bc55ccb947a8`
  - **Loop_Id**: `pens`
  - **Num_Iterations**: `3`

### 14. Function: ArithOp
  **Formula:** `poatx`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `loopcount_pens = 1`

### 15. Function: ArithOp
  **Formula:** `pditx`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `loopcount_pens = 2`

### 16. Function: ArithOp
  **Formula:** `psutx`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `loopcount_pens = 3`

### 17. Function: ArithOp
  **Formula:** `i_pens`
  **Output Variable:** `poatx`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `loopcount_pens = 1`

### 18. Function: ArithOp
  **Formula:** `i_pens`
  **Output Variable:** `pditx`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `loopcount_pens = 2`

### 19. Function: ArithOp
  **Formula:** `i_pens`
  **Output Variable:** `psutx`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `loopcount_pens = 3`

### 20. Function: ArithOp
  **Formula:** `poatx + poass`
  **Output Variable:** `poa`
  **Tax Unit:** `tu_individual_lv`

### 21. Function: ArithOp
  **Formula:** `pditx + pdiss + pdint`
  **Output Variable:** `pdi`
  **Tax Unit:** `tu_individual_lv`

### 22. Function: ArithOp
  **Formula:** `psutx + psuss`
  **Output Variable:** `psu`
  **Tax Unit:** `tu_individual_lv`

### 23. Function: ArithOp
  **Formula:** `i_pen2007_12`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2008 & GetDataIncomeYear <= 2006`

### 24. Function: ArithOp
  **Formula:** `i_pen2008_12`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2009 & GetDataIncomeYear <= 2007`

### 25. Function: ArithOp
  **Formula:** `i_pens`
  **Output Variable:** `i_pen2013_01`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2013 & GetDataIncomeYear <= 2012`

### 26. Function: ArithOp
  **Formula:** `i_pen2025_av`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear > GetDataIncomeYear`

### 27. Function: BenCalc
  - **Comp_Cond**: `i_pens > $Limit2_2007 * $IndexC_2007`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pens`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Run_Cond**: `GetSystemYear = 2006 & GetDataIncomeYear >= 2007`

### 28. Function: BenCalc
  - **Comp_Cond**: `i_pens > $Limit2_2008 * $IndexC_2008`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pens`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Run_Cond**: `GetSystemYear <= 2007 & GetDataIncomeYear >= 2008`

### 29. Function: BenCalc
  - **Comp_Cond**: `i_pen2015_01 > $Limit2015`
  - **Comp_perTU**: `i_pen2015_01 + $Limit2015 * ($Index2015 - 1)`
  - **Output_Var**: `i_pen2015_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 30. Function: ArithOp
  **Formula:** `i_pen2015_12`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2016 &  GetDataIncomeYear <= 2014`

### 31. Function: BenCalc
  - **Comp_Cond**: `i_pen2016_01 > $Limit2016`
  - **Comp_perTU**: `i_pen2016_01 + $Limit2016 * ($Index2016 - 1)`
  - **Output_Var**: `i_pen2016_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 32. Function: ArithOp
  **Formula:** `i_pen2014_12`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2015 & GetDataIncomeYear <= 2013`

### 33. Function: BenCalc
  - **Comp_Cond**: `i_pens > $Limit2013 * $Index2013`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pens`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Run_Cond**: `GetSystemYear <= 2012 & GetDataIncomeYear >= 2013`

### 34. Function: BenCalc
  - **Comp_Cond**: `i_pens > $Limit2014 * $Index2014`
  - **Comp_perTU**: `i_pens - $Limit2014 * ($Index2014 - 1)`
  - **Output_Var**: `i_pens`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Run_Cond**: `GetSystemYear <= 2013 & GetDataIncomeYear >= 2014`

### 35. Function: BenCalc
  - **Comp_Cond**: `i_pen2017_01 > $Limit2017`
  - **Comp_perTU**: `i_pen2017_01 + $Limit2017 * ($Index2017 - 1)`
  - **Output_Var**: `i_pen2017_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 36. Function: BenCalc
  - **Comp_Cond**: `i_pen2018_01<=$Limit2018 & liwwh >= 360 & liwwh < 480`
  - **Comp_perTU**: `i_pen2018_01 * $Index2018_2`
  - **Output_Var**: `i_pen2018_12`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Run_Cond**: `loopcount_pens = 1`

### 37. Function: BenCalc
  - **Comp_Cond**: `i_pen2019_01 > $Limit2019 & liwwh >= 540`
  - **Comp_perTU**: `$Limit2019*$Index2019_4 + (i_pen2019_01 - $Limit2019)`
  - **Output_Var**: `i_pen2019_12`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Run_Cond**: `loopcount_pens = 1`

### 38. Function: ArithOp
  **Formula:** `i_pen2016_12`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2017 &  GetDataIncomeYear <= 2015`

### 39. Function: ArithOp
  **Formula:** `i_pen2017_12`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2018 & GetDataIncomeYear <= 2016`

### 40. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `i_pen2018_01 > $Limit2018`
  - **Output_Var**: `i_pen2018_12`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Comp_perTU**: `$Limit2018*$Index2018_1 + (i_pen2018_01 - $Limit2018)`

### 41. Function: ArithOp
  **Formula:** `i_pen2018_12`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2019 & GetDataIncomeYear <= 2017`

### 42. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `i_pen2019_01 > $Limit2019`
  - **Comp_perTU**: `i_pen2019_01 * $Index2019_1`
  - **Output_Var**: `i_pen2019_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 43. Function: ArithOp
  **Formula:** `i_pen2019_12`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2020 & GetDataIncomeYear <= 2018`

### 44. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 1`
  - **Comp_Cond**: `i_pen2020_01 > $Limit2020 & liwwh < 360`
  - **Comp_perTU**: `i_pen2020_01 * $Index2020_4`
  - **Output_Var**: `i_pen2020_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 45. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `i_pen2020_01 > $Limit2020`
  - **Comp_perTU**: `i_pen2020_01 * $Index2020_1`
  - **Output_Var**: `i_pen2020_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 46. Function: BenCalc
  - **Comp_Cond**: `GetSystemYear >= 2008 & GetDataIncomeYear < 2007`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2008_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 47. Function: BenCalc
  - **Comp_Cond**: `GetSystemYear >= 2014 & GetDataIncomeYear < 2013`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2014_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 48. Function: BenCalc
  - **Comp_Cond**: `GetSystemYear >= 2015 & GetDataIncomeYear < 2014`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2015_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 49. Function: BenCalc
  - **Comp_Cond**: `GetSystemYear >= 2016 & GetDataIncomeYear < 2015`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2016_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 50. Function: BenCalc
  - **Comp_Cond**: `GetSystemYear >= 2017 & GetDataIncomeYear < 2016`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2017_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 51. Function: BenCalc
  - **Comp_Cond**: `GetSystemYear >= 2018 & GetDataIncomeYear < 2017`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2018_01
`
  - **TAX_UNIT**: `tu_individual_lv`

### 52. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 1`
  - **Comp_Cond**: `GetSystemYear >= 2019 & GetDataIncomeYear < 2018`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2019_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 53. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `GetSystemYear >= 2019 & GetDataIncomeYear < 2018`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2019_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 54. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 1`
  - **Comp_Cond**: `GetSystemYear >= 2020 & GetDataIncomeYear < 2019`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2020_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 55. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `GetSystemYear >= 2020 & GetDataIncomeYear < 2019`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2020_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 56. Function: ArithOp
  **Formula:** `i_pen2020_12`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2021 & GetDataIncomeYear <= 2019`

### 57. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 1`
  - **Comp_Cond**: `GetSystemYear >= 2021 & GetDataIncomeYear < 2020`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2021_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 58. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `GetSystemYear >= 2021 & GetDataIncomeYear < 2020`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2021_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 59. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 1`
  - **Comp_Cond**: `i_pen2021_01 > $Limit2021 & liwwh >= 540`
  - **Comp_perTU**: `$Limit2021*$Index2021_4 + (i_pen2021_01 - $Limit2021)`
  - **Output_Var**: `i_pen2021_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 60. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `i_pen2021_01 > $Limit2021`
  - **Comp_perTU**: `$Limit2021*$Index2021_1 + (i_pen2021_01 - $Limit2021)`
  - **Output_Var**: `i_pen2021_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 61. Function: ArithOp
  **Formula:** `i_pen2021_12`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2022 & GetDataIncomeYear <= 2020`

### 62. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 1`
  - **Comp_Cond**: `GetSystemYear >= 2022 & GetDataIncomeYear < 2021`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2022_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 63. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `GetSystemYear >= 2022 & GetDataIncomeYear < 2021`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2022_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 64. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 1`
  - **Comp_Cond**: `i_pen2022_01 > $Limit2022 & liwwh >= 540`
  - **Comp_perTU**: `$Limit2022*$Index2022_4 + (i_pen2022_01 - $Limit2022)`
  - **Output_Var**: `i_pen2022_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 65. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `i_pen2022_01 > $Limit2022`
  - **Comp_perTU**: `$Limit2022*$Index2022_1 + (i_pen2022_01 - $Limit2022)`
  - **Output_Var**: `i_pen2022_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 66. Function: ArithOp
  **Formula:** `i_pen2022_12`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2023 & GetDataIncomeYear <= 2021`

### 67. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 1`
  - **Comp_Cond**: `GetSystemYear >= 2023 & GetDataIncomeYear < 2022`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2023_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 68. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `GetSystemYear >= 2023 & GetDataIncomeYear < 2022`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2023_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 69. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 1`
  - **Comp_Cond**: `i_pen2023_01 > $Limit2023 & liwwh >= 540`
  - **Comp_perTU**: `$Limit2023*$Index2023_4 + (i_pen2023_01 - $Limit2023)`
  - **Output_Var**: `i_pen2023_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 70. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `i_pen2023_01 > $Limit2023`
  - **Comp_perTU**: `$Limit2023*$Index2023_1 + (i_pen2023_01 - $Limit2023)`
  - **Output_Var**: `i_pen2023_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 71. Function: ArithOp
  **Formula:** `i_pen2023_12`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2024 & GetDataIncomeYear <= 2022`

### 72. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 1`
  - **Comp_Cond**: `GetSystemYear >= 2024 & GetDataIncomeYear < 2023`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2024_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 73. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `GetSystemYear >= 2024 & GetDataIncomeYear < 2023`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2024_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 74. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 1`
  - **Comp_Cond**: `i_pen2024_01 > $Limit2024 & liwwh >= 540`
  - **Comp_perTU**: `$Limit2024*$Index2024_4 + (i_pen2024_01 - $Limit2024)`
  - **Output_Var**: `i_pen2024_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 75. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `i_pen2024_01 > $Limit2024`
  - **Comp_perTU**: `$Limit2024*$Index2024_1 + (i_pen2024_01 - $Limit2024)`
  - **Output_Var**: `i_pen2024_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 76. Function: ArithOp
  **Formula:** `i_pen2024_12`
  **Output Variable:** `i_pens`
  **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetSystemYear >= 2025 & GetDataIncomeYear <= 2023`

### 77. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 1`
  - **Comp_Cond**: `GetSystemYear >= 2025 & GetDataIncomeYear < 2024`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2025_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 78. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `GetSystemYear >= 2025 & GetDataIncomeYear < 2024`
  - **Comp_perTU**: `i_pens`
  - **Output_Var**: `i_pen2025_01`
  - **TAX_UNIT**: `tu_individual_lv`

### 79. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 1`
  - **Comp_Cond**: `i_pen2025_01 > $Limit2025 & liwwh >= 540`
  - **Comp_perTU**: `$Limit2025*$Index2025_4 + (i_pen2025_01 - $Limit2025)`
  - **Output_Var**: `i_pen2025_12`
  - **TAX_UNIT**: `tu_individual_lv`

### 80. Function: BenCalc
  - **Run_Cond**: `loopcount_pens = 2 | loopcount_pens = 3`
  - **Comp_Cond**: `i_pen2025_01 > $Limit2025`
  - **Comp_perTU**: `$Limit2025*$Index2025_1 + (i_pen2025_01 - $Limit2025)`
  - **Output_Var**: `i_pen2025_12`
  - **TAX_UNIT**: `tu_individual_lv`


---

## Policy: txcee_lv
### 1. Function: DefConst
  **Constants Defined:**
  - `$txcee_rate1`: 0.105
  - `$txcee_rate2`: 0.0925

### 2. Function: BenCalc
  - **Comp_Cond**: `(dag00>=$PensAgeMale & dgn=1) | (dag00>=$PensAgeFem & dgn=0)`
  - **Comp_perTU**: `(yem - $tscse_se_uplim1)*$txcee_rate2`
  - **Output_Var**: `txcee_s`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Who_Must_Be_Elig**: `one`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem > $tscse_se_uplim1`
  - **Tax Unit:** `tu_individual_lv`

### 4. Function: ArithOp
  **Formula:** `txcee_s*yemmy/12`
  **Output Variable:** `txcee_s`
  **Tax Unit:** `tu_individual_lv`


---

## Policy: txcer_lv
### 1. Function: DefConst
  **Constants Defined:**
  - `$txcer_rate1`: n/a
  - `$txcer_rate2`: n/a
  - `$txcer_rate3`: 0.25

### 2. Function: BenCalc
  - **Comp_Cond**: `(dag00>=$PensAgeMale & dgn=1) | (dag00>=$PensAgeFem & dgn=0) `
  - **Comp_perTU**: `(yem - $tscse_se_uplim1)*($txcer_rate3-$txcee_rate2)`
  - **Output_Var**: `txcer_s`
  - **TAX_UNIT**: `tu_individual_lv`
  - **Who_Must_Be_Elig**: `one`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem > $tscse_se_uplim1`
  - **Tax Unit:** `tu_individual_lv`

### 4. Function: ArithOp
  **Formula:** `txcer_s*yemmy/12`
  **Output Variable:** `txcer_s`
  **Tax Unit:** `tu_individual_lv`


---

## Policy: txcse_lv
### 1. Function: DefConst
  **Constants Defined:**
  - `$txcse_rate1`: n/a
  - `$txcse_rate2`: n/a
  - `$txcse_rate3`: 0.25

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yse > $tscse_se_uplim1`
  - **Tax Unit:** `tu_individual_lv`

### 3. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Who_Must_Be_Elig**: `n/a`

### 4. Function: ArithOp
  **Formula:** `txcse_s*ysemy/12`
  **Output Variable:** `txcse_s`
  **Tax Unit:** `tu_individual_lv`

### 5. Function: ArithOp
  **Formula:** `(yse - $tscse_se_uplim1)*$txcse_rate3`
  **Output Variable:** `txcse_s`
  **Tax Unit:** `tu_individual_lv`


---

## Policy: IlsUDBDef_lv
### 1. Function: DefIl
  - **Name**: `ils_udb_ypr`
  - **ypr**: `+`

### 2. Function: DefIl
  - **Name**: `ils_udb_ypp`
  - **ypp**: `+`

### 3. Function: DefIl
  - **Name**: `ils_udb_yse`
  - **yse**: `+`

### 4. Function: DefIl
  - **Name**: `ils_udb_yem`
  - **yem**: `+`

### 5. Function: DefIl
  - **Name**: `ils_udb_xmp`
  - **xmp**: `+`

### 6. Function: DefIl
  - **Name**: `ils_udb_yot`
  - **yot**: `+`

### 7. Function: DefIl
  - **Name**: `ils_udb_ypt`
  - **ypt**: `+`

### 8. Function: DefIl
  - **Name**: `ils_udb_yiy`
  - **yiynt**: `+`
  - **yiytx**: `+`

### 9. Function: DefIl
  - **Name**: `ils_udb_bdi`
  - **pdint**: `+`
  - **pdiss_s**: `+`
  - **pditx**: `+`

### 10. Function: DefIl
  - **Name**: `ils_udb_bsu`
  - **psuss_s**: `+`
  - **psutx**: `+`

### 11. Function: DefIl
  - **Name**: `ils_udb_boa`
  - **poass_s**: `+`
  - **poatx**: `+`
  - **bpeec_s**: `n/a`
  - **bpeec02_s**: `n/a`
  - **bpeec01_s**: `n/a`

### 12. Function: DefIl
  - **Name**: `ils_udb_kfbcc`
  - **kfbcc**: `+`

### 13. Function: DefIl
  - **Name**: `ils_udb_bfa`
  - **bfaot**: `+`
  - **bfana_s**: `+`
  - **bfacc_s**: `+`
  - **bfawk_s**: `+`
  - **bfapl_s**: `+`
  - **bfama_s**: `+`
  - **bfaba_s**: `+`
  - **bfaec_s**: `n/a`
  - **bfaam**: `+`

### 14. Function: DefIl
  - **Name**: `ils_udb_bed`
  - **bed**: `+`

### 15. Function: DefIl
  - **Name**: `ils_udb_bhl`
  - **bhl**: `+`

### 16. Function: DefIl
  - **Name**: `ils_udb_bun`
  - **bunot**: `+`
  - **bun00_s**: `+`
  - **bwkmcee_s**: `n/a`
  - **bwkmcse_s**: `n/a`
  - **bwkmcch_s**: `n/a`

### 17. Function: DefIl
  - **Name**: `ils_udb_yds`
  - **ils_udb_tis**: `-`
  - **ils_udb_tpr**: `-`
  - **ils_udb_xmp**: `-`
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
  - **ils_udb_yot**: `+`
  - **ils_udb_ypt**: `+`
  - **ils_udb_yiy**: `+`
  - **ils_udb_ypr**: `+`
  - **ils_udb_ypp**: `+`
  - **ils_udb_yse**: `+`
  - **ils_udb_yem**: `+`

### 18. Function: DefIl
  - **Name**: `ils_udb_tis`
  - **txcse_s**: `+`
  - **txcee_s**: `+`
  - **tscse_s**: `+`
  - **tscee_s**: `+`
  - **tin_s**: `+`

### 19. Function: DefIl
  - **Name**: `ils_udb_tpr`
  - **tpr**: `+`

### 20. Function: DefIl
  - **Name**: `ils_udb_bho`
  - **bho_s**: `+`
  - **bhoht**: `n/a`

### 21. Function: DefIl
  - **Name**: `ils_udb_bsa`
  - **bsaot**: `+`
  - **bsafu**: `+`
  - **bsamm_s**: `+`


---

## Policy: random_lv
### 1. Function: DefVar
  - **i_mc_rand_1**: `n/a`
  - **i_mc_rand_2**: `n/a`
  - **i_mc_rand_3**: `n/a`
  - **i_mc_rand_4**: `n/a`
  - **i_lmamy**: `0`
  - **i_lma2**: `0`
  - **i_lma1**: `0`
  - **Var_Monetary**: `no`
  - **i_bsamm_bta_rand**: `0`
  - **i_bsamm_bca_rand**: `0`
  - **i_bho_bta_rand**: `0`
  - **i_bho_bca_rand**: `0`
  - **i_bsamm_rand**: `0`
  - **i_bho_rand**: `0`

### 2. Function: RandSeed *(Switch: n/a)*
  - **Seed**: `n/a`

### 3. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 4. Function: RandSeed *(Switch: n/a)*
  - **Seed**: `n/a`

### 5. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 6. Function: RandSeed *(Switch: n/a)*
  - **Seed**: `n/a`

### 7. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 8. Function: RandSeed *(Switch: n/a)*
  - **Seed**: `n/a`

### 9. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 10. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lmamy`
  **Tax Unit:** `tu_individual_lv`

### 11. Function: RandSeed
  - **Seed**: `25`

### 12. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lma2`
  **Tax Unit:** `tu_individual_lv`

### 13. Function: RandSeed
  - **Seed**: `24`

### 14. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lma1`
  **Tax Unit:** `tu_individual_lv`

### 15. Function: RandSeed
  - **Seed**: `23`

### 16. Function: RandSeed
  - **Seed**: `202402291639`

### 17. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_bsamm_rand`
  **Tax Unit:** `tu_household_lv`

### 18. Function: RandSeed
  - **Seed**: `202402291639`

### 19. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_bho_rand`
  **Tax Unit:** `tu_household_lv`

### 20. Function: ArithOp
  **Formula:** `i_bsamm_rand#1`
  **Output Variable:** `i_bsamm_rand`
  **Tax Unit:** `tu_individual_lv`

### 21. Function: ArithOp
  **Formula:** `i_bho_rand#1`
  **Output Variable:** `i_bho_rand`
  **Tax Unit:** `tu_individual_lv`


---

## Policy: yemcomp_lv *(Switch: off)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_yem_orig**: `n/a`
  - **Var_Monetary**: `n/a`
  - **i_yemmy_orig**: `n/a`
  - **i_bwkmcee_s**: `n/a`

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

### 5. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`


---

## Policy: ysecomp_lv *(Switch: off)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_yse_orig**: `n/a`
  - **Var_Monetary**: `n/a`
  - **i_ysemy_orig**: `n/a`
  - **i_bwkmcse_s**: `n/a`

### 2. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 3. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **LowLim**: `n/a`
  - **UpLim**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 5. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 6. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`


---

## Policy: ycompdep_lv *(Switch: off)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_bwkmcch_s**: `n/a`
  - **Var_Monetary**: `n/a`

### 2. Function: DefTu *(Switch: n/a)*
  - **name**: `n/a`
  - **type**: `n/a`
  - **members**: `n/a`
  - **PartnerCond**: `n/a`
  - **DepChildCond**: `n/a`
  - **DepParentCond**: `n/a`
  - **#_Income**: `n/a`
  - **#_Info**: `n/a`
  - **#_level**: `n/a`
  - **HeadDefInc**: `n/a`
  - **NoChildIfHead**: `n/a`
  - **NoChildIfPartner**: `n/a`
  - **AssignDepChOfDependents**: `n/a`
  - **AssignPartnerOfDependents**: `n/a`

### 3. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 4. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perElig**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 5. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: TransLMA_lv *(Switch: off)*
### 1. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 2. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 3. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 4. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 5. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 6. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 7. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 8. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Output_Var**: `n/a`

### 9. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 10. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 11. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 12. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 13. Function: DefVar *(Switch: n/a)*
  - **i_yemmw**: `n/a`

### 14. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 15. Function: DefConst
  **Constants Defined:**
  - `$er_dgn0_deh1_lv`: 0
  - `$er_dgn0_deh2_lv`: 0
  - `$er_dgn0_deh3_lv`: 0
  - `$er_dgn1_deh1_lv`: 0
  - `$er_dgn1_deh2_lv`: 0
  - `$er_dgn1_deh3_lv`: 0
  - `$ur_dgn0_deh1_lv`: 0
  - `$ur_dgn0_deh2_lv`: 0
  - `$ur_dgn0_deh3_lv`: 0
  - `$ur_dgn1_deh1_lv`: 0
  - `$ur_dgn1_deh2_lv`: 0
  - `$ur_dgn1_deh3_lv`: 0
  - `$er_dgn0_se`: 0
  - `$er_dgn1_se`: 0
  - `$er_yemmy2`: 0
  - `$er_yemmy5`: 0
  - `$er_yemmy8`: 0
  - `$ur_yemmy2`: 0
  - `$ur_yemmy5`: 0
  - `$ur_yemmy8`: 0
  - `Run_Cond`: GetDataIncomeYear=2019

### 16. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy = 0) & (ysemy = 0)& (dag > 17) & (dag < 65) & ((les=5) | lowas=1)`
  - **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetDataIncomeYear <= 2020`

### 17. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(deh = 5) & (dgn = 1) & (i_lma1 < $ur_dgn1_deh3_lv)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_lv`

### 18. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy > 0) `
  - **Tax Unit:** `tu_individual_lv`

### 19. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(deh = 5) & (dgn = 1) & (i_lma1 < $er_dgn1_deh3_lv)`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_lv`

### 20. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ysemy > 0) & (yemmy = 0)`
  - **Tax Unit:** `tu_individual_lv`

### 21. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dgn = 1 & (i_lma2 < $er_dgn1_se)`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_lv`

### 22. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lma =1)`
  - **Tax Unit:** `tu_individual_lv`

### 23. Function: ArithOp
  **Formula:** `(yivwg*$Nwh*52/12)`
  **Output Variable:** `yem_a`
  **Tax Unit:** `tu_individual_lv`

### 24. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lma=1)|(lma=5)`
  - **Tax Unit:** `tu_individual_lv`

### 25. Function: ArithOp
  **Formula:** `$Nwh`
  **Output Variable:** `lhw_a`
  **Tax Unit:** `tu_individual_lv`

### 26. Function: BenCalc
  - **Comp_Cond**: `(lma=2) & (ysemy > 0) & (yemmy = 0)`
  - **Comp_perTU**: `0`
  - **Output_Var**: `yemmy_a`
  - **TAX_UNIT**: `tu_individual_lv`

### 27. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$sh_mcee_l1`: n/a
  - `$sh_mcee_l2`: n/a
  - `$sh_mcee_l3`: n/a
  - `$sh_mcee_l4`: n/a
  - `$sh_mcee_l5`: n/a
  - `$sh_mcee_l6`: n/a
  - `$sh_mcee_l7`: n/a
  - `$sh_mcee_l8`: n/a
  - `$sh_mcee_l9`: n/a
  - `$sh_mcee_l10`: n/a
  - `$sh_mcee_l11`: n/a
  - `$sh_mcee_l12`: n/a
  - `$sh_mcee_l1_fem`: n/a
  - `$sh_mcee_l2_fem`: n/a
  - `$sh_mcee_l3_fem`: n/a
  - `$sh_mcee_l4_fem`: n/a
  - `$sh_mcee_l5_fem`: n/a
  - `$sh_mcee_l6_fem`: n/a
  - `$sh_mcee_l7_fem`: n/a
  - `$sh_mcee_l8_fem`: n/a
  - `$sh_mcee_l9_fem`: n/a
  - `$sh_mcee_l10_fem`: n/a
  - `$sh_mcee_l11_fem`: n/a
  - `$sh_mcee_l12_fem`: n/a
  - `$sh_mceemy_1`: n/a
  - `$sh_mceemy_2`: n/a
  - `$sh_mceemy_3`: n/a
  - `$sh_mceemy_4`: n/a
  - `$sh_mceemy_5`: n/a
  - `$sh_mceemy_6`: n/a
  - `Run_Cond`: GetDataIncomeYear=2019

### 28. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$sh_mcse`: n/a
  - `$sh_mcsemy_1`: n/a
  - `$sh_mcsemy_2`: n/a
  - `$sh_mcsemy_3`: n/a
  - `$sh_mcsemy_4`: n/a
  - `$sh_mcsemy_5`: n/a
  - `$sh_mcsemy_6`: n/a
  - `Run_Cond`: GetDataIncomeYear=2019

### 29. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy = 0) & (ysemy = 0)& (dag > 17) & (dag < 65) & (les=5)`
  - **Tax Unit:** `tu_individual_lv`
  **Run Condition:** `GetDataIncomeYear > 2020`

### 30. Function: DefConst
  **Constants Defined:**
  - `$er_dgn0_deh1_lv`: 0
  - `$er_dgn0_deh2_lv`: 0
  - `$er_dgn0_deh3_lv`: 0
  - `$er_dgn1_deh1_lv`: 0
  - `$er_dgn1_deh2_lv`: 0
  - `$er_dgn1_deh3_lv`: 0
  - `$ur_dgn0_deh1_lv`: 0
  - `$ur_dgn0_deh2_lv`: 0
  - `$ur_dgn0_deh3_lv`: 0
  - `$ur_dgn1_deh1_lv`: 0
  - `$ur_dgn1_deh2_lv`: 0
  - `$ur_dgn1_deh3_lv`: 0
  - `$er_dgn0_se`: 0
  - `$er_dgn1_se`: 0
  - `$er_yemmy2`: 0
  - `$er_yemmy5`: 0
  - `$er_yemmy8`: 0
  - `$ur_yemmy2`: 0
  - `$ur_yemmy5`: 0
  - `$ur_yemmy8`: 0
  - `Run_Cond`: GetDataIncomeYear!=2019

### 31. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$sh_mcee_l1`: n/a
  - `$sh_mcee_l2`: n/a
  - `$sh_mcee_l3`: n/a
  - `$sh_mcee_l4`: n/a
  - `$sh_mcee_l5`: n/a
  - `$sh_mcee_l6`: n/a
  - `$sh_mcee_l7`: n/a
  - `$sh_mcee_l8`: n/a
  - `$sh_mcee_l9`: n/a
  - `$sh_mcee_l10`: n/a
  - `$sh_mcee_l11`: n/a
  - `$sh_mcee_l12`: n/a
  - `$sh_mcee_l1_fem`: n/a
  - `$sh_mcee_l2_fem`: n/a
  - `$sh_mcee_l3_fem`: n/a
  - `$sh_mcee_l4_fem`: n/a
  - `$sh_mcee_l5_fem`: n/a
  - `$sh_mcee_l6_fem`: n/a
  - `$sh_mcee_l7_fem`: n/a
  - `$sh_mcee_l8_fem`: n/a
  - `$sh_mcee_l9_fem`: n/a
  - `$sh_mcee_l10_fem`: n/a
  - `$sh_mcee_l11_fem`: n/a
  - `$sh_mcee_l12_fem`: n/a
  - `$sh_mceemy_1`: n/a
  - `$sh_mceemy_2`: n/a
  - `$sh_mceemy_3`: n/a
  - `$sh_mceemy_4`: n/a
  - `$sh_mceemy_5`: n/a
  - `$sh_mceemy_6`: n/a
  - `Run_Cond`: n/a

### 32. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$sh_mcse`: n/a
  - `$sh_mcsemy_1`: n/a
  - `$sh_mcsemy_2`: n/a
  - `$sh_mcsemy_3`: n/a
  - `$sh_mcsemy_4`: n/a
  - `$sh_mcsemy_5`: n/a
  - `$sh_mcsemy_6`: n/a
  - `Run_Cond`: n/a


---

## Policy: tco_lv *(Switch: off)*
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
  - `$tco_v_04541`: n/a
  - `$tco_v_07221`: $tco_base_v_07221
  - `$tco_v_01211`: $tco_base_v_01211
  - `$tco_v_01222`: $tco_base_v_01222

### 2. Function: DefConst
  **Constants Defined:**
  - `$tco_a_02121`: 0.95*$tco_a_02121a + 0.025*$tco_a_02121b1+ 0.025*$tco_a_02121b2
  - `$tco_a_02122`: ($tco_a_02122a + $tco_a_02122b)/2
  - `$tco_a_04531`: 1.00*$tco_a_04531a1 + 0.00*$tco_a_04531b
  - `$tco_a_07221`: 0.50*$tco_a_07221a21+0.50*$tco_a_07221c1
  - `$tco_a_01222`: (($tco_a_01222a+$tco_a_01222b)/2)/100

### 3. Function: DefConst
  **Constants Defined:**
  - `$tco_base_q_07221`: 0.50*$tco_base_q_07221a +  0.50*$tco_base_q_07221c
  - `$tco_base_q_04531`: 1.00*$tco_base_q_04531a + 0.00*$tco_base_q_04531b
  - `$tco_base_q_02131`: $tco_base_q_02131t * 100 / 5
  - `$tco_base_q_02122`: $tco_base_q_02122t * 100
  - `$tco_base_q_02121`: (0.90*$tco_base_q_02121t1+ 0.05*$tco_base_q_02121t2 + 0.05*$tco_base_q_02121t3)* 100
  - `$tco_base_q_02111`: $tco_base_q_02111t / 40% * 100
  - `$tco_base_a_07221`: 0.50*$tco_base_a_07221a21+0.50*$tco_base_a_07221c1
  - `$tco_base_a_04531`: 1.00*$tco_base_a_04531a1 + 0.00*$tco_base_a_04531b
  - `$tco_base_a_02122`: ($tco_base_a_02122a + $tco_base_a_02122b)/2
  - `$tco_base_a_02121`: 0.95*$tco_base_a_02121a + 0.025*$tco_base_a_02121b1+ 0.025*$tco_base_a_02121b2
  - `$tco_base_a_01222`: (($tco_base_a_01222a+$tco_base_a_01222b)/2)/100

### 4. Function: DefIl
  - **Name**: `il_xs_exc`
  - **xs07221**: `+`
  - **xs04541**: `n/a`
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
  - **xs01211**: `+`
  - **xs01222**: `+`

### 5. Function: DefConst
  **Constants Defined:**
  - `$tco_t_01111`: $tco_t_std
  - `$tco_t_01112`: $tco_t_std
  - `$tco_t_01113`: $tco_t_std
  - `$tco_t_01114`: $tco_t_std
  - `$tco_t_01115`: $tco_t_std
  - `$tco_t_01116`: $tco_t_std
  - `$tco_t_01121`: $tco_t_std
  - `$tco_t_01122`: $tco_t_std
  - `$tco_t_01123`: $tco_t_std
  - `$tco_t_01124`: $tco_t_std
  - `$tco_t_01125`: $tco_t_std
  - `$tco_t_01126`: $tco_t_std
  - `$tco_t_01127`: $tco_t_std
  - `$tco_t_01131`: $tco_t_std
  - `$tco_t_01132`: $tco_t_std
  - `$tco_t_01133`: $tco_t_std
  - `$tco_t_01134`: $tco_t_std
  - `$tco_t_01141`: $tco_t_std
  - `$tco_t_01142`: $tco_t_std
  - `$tco_t_01143`: $tco_t_std
  - `$tco_t_01144`: $tco_t_std
  - `$tco_t_01145`: $tco_t_std
  - `$tco_t_01146`: $tco_t_std
  - `$tco_t_01147`: $tco_t_std
  - `$tco_t_01151`: $tco_t_std
  - `$tco_t_01152`: $tco_t_std
  - `$tco_t_01153`: $tco_t_std
  - `$tco_t_01154`: $tco_t_std
  - `$tco_t_01155`: $tco_t_std
  - `$tco_t_01161`: $tco_t_red1
  - `$tco_t_01162`: $tco_t_red1
  - `$tco_t_01163`: $tco_t_red1
  - `$tco_t_01164`: $tco_t_red1
  - `$tco_t_01165`: $tco_t_red1
  - `$tco_t_01166`: $tco_t_red1
  - `$tco_t_01167`: $tco_t_red1
  - `$tco_t_01168`: $tco_t_std
  - `$tco_t_01169`: $tco_t_std
  - `$tco_t_01171`: $tco_t_red1
  - `$tco_t_01172`: $tco_t_red1
  - `$tco_t_01173`: $tco_t_red1
  - `$tco_t_01174`: $tco_t_red1
  - `$tco_t_01175`: $tco_t_std
  - `$tco_t_01176`: $tco_t_std
  - `$tco_t_01177`: $tco_t_red1
  - `$tco_t_01178`: $tco_t_red1
  - `$tco_t_01181`: $tco_t_std
  - `$tco_t_01182`: $tco_t_std
  - `$tco_t_01183`: $tco_t_std
  - `$tco_t_01184`: $tco_t_std
  - `$tco_t_01185`: $tco_t_std
  - `$tco_t_01186`: $tco_t_std
  - `$tco_t_01191`: $tco_t_std
  - `$tco_t_01192`: $tco_t_std
  - `$tco_t_01193`: $tco_t_red1
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
  - `$tco_t_04411`: $tco_t_std
  - `$tco_t_04421`: $tco_t_std
  - `$tco_t_04431`: $tco_t_std
  - `$tco_t_04441`: $tco_t_std
  - `$tco_t_04511`: $tco_t_std
  - `$tco_t_04521`: $tco_t_std
  - `$tco_t_04522`: $tco_t_std
  - `$tco_t_04531`: $tco_t_std
  - `$tco_t_04541`: $tco_t_red1
  - `$tco_t_04551`: $tco_t_red1
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
  - `$tco_t_06111`: $tco_t_red1
  - `$tco_t_06121`: $tco_t_red1
  - `$tco_t_06131`: $tco_t_red1
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
  - `$tco_t_07311`: $tco_t_red1
  - `$tco_t_07321`: $tco_t_red1
  - `$tco_t_07331`: $tco_t_zero
  - `$tco_t_07341`: $tco_t_red1
  - `$tco_t_07351`: $tco_t_red1
  - `$tco_t_07361`: $tco_t_red1
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
  - `$tco_t_09421`: $tco_t_zero
  - `$tco_t_09422`: $tco_t_zero
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
  - `$tco_t_11111`: $tco_t_std
  - `$tco_t_11112`: $tco_t_std
  - `$tco_t_11121`: $tco_t_std
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
  - `$tco_a_02211`: $tco_base_a_02211
  - `$tco_a_02131`: $tco_base_a_02131
  - `$tco_a_02122b`: $tco_base_a_02122b
  - `$tco_a_02122a`: $tco_base_a_02122a
  - `$tco_a_02121b2`: $tco_base_a_02121b2
  - `$tco_a_02121b1`: $tco_base_a_02121b1
  - `$tco_a_02121a`: $tco_base_a_02121a
  - `$tco_a_02111`: $tco_base_a_02111
  - `$tco_a_07221c1`: $tco_base_a_07221c1
  - `$tco_a_04531c2`: n/a
  - `$tco_a_07221e`: n/a
  - `$tco_a_07221d`: n/a
  - `$tco_a_07221c4`: n/a
  - `$tco_a_07221c3`: n/a
  - `$tco_a_07221c2`: n/a
  - `$tco_a_07221b`: n/a
  - `$tco_a_07221a23`: n/a
  - `$tco_a_07221a22`: n/a
  - `$tco_a_07221a21`: $tco_base_a_07221a21
  - `$tco_a_07221a1`: n/a
  - `$tco_a_04541`: n/a
  - `$tco_a_04531c1`: n/a
  - `$tco_a_04531b`: $tco_base_a_04531b
  - `$tco_a_04531a2`: n/a
  - `$tco_a_04531a1`: $tco_base_a_04531a1
  - `$tco_a_04522`: $tco_base_a_04522
  - `$tco_a_04521`: $tco_base_a_04521
  - `$tco_a_04511`: $tco_base_a_04511
  - `$tco_a_02213`: $tco_base_a_02213
  - `$tco_a_02212`: $tco_base_a_02212
  - `$tco_a_01211`: $tco_base_a_01211
  - `$tco_a_01222a`: $tco_base_a_01222a
  - `$tco_a_01222b`: $tco_base_a_01222b

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
  - **xs01222**: `n/a`
  - **xs01221**: `+`
  - **xs01213**: `+`
  - **xs01212**: `+`
  - **xs01211**: `n/a`
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
  - **xs04541**: `+`

### 9. Function: DefIl
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
  - **txa01211_na**: `+`
  - **txa01222_na**: `+`

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
  - **txa01211**: `+`
  - **txa01222**: `+`

### 15. Function: DefIl
  - **Name**: `il_itt_revnc`
  - **il_tva**: `+`
  - **il_tx**: `+`

### 16. Function: DefConst
  **Constants Defined:**
  - `$tco_a_01211`: $tco_base_a_01211
  - `$tco_a_01222a`: $tco_base_a_01222a
  - `$tco_a_01222b`: $tco_base_a_01222b
  - `$tco_a_02111`: 1939.50
  - `$tco_a_02121a`: 132.00
  - `$tco_a_02121b1`: 253.83
  - `$tco_a_02121b2`: 152.83
  - `$tco_a_02122a`: 132.00
  - `$tco_a_02122b`: 75.83
  - `$tco_a_02131`: 9.67
  - `$tco_a_02211`: $tco_base_a_02211
  - `$tco_a_02212`: $tco_base_a_02212
  - `$tco_a_02213`: $tco_base_a_02213
  - `$tco_a_04511`: $tco_base_a_04511
  - `$tco_a_04521`: $tco_base_a_04521
  - `$tco_a_04522`: $tco_base_a_04522
  - `$tco_a_04531a1`: $tco_base_a_04531a1
  - `$tco_a_04531a2`: n/a
  - `$tco_a_04531b`: $tco_base_a_04531b
  - `$tco_a_04531c1`: n/a
  - `$tco_a_04531c2`: n/a
  - `$tco_a_04541`: n/a
  - `$tco_a_07221a1`: n/a
  - `$tco_a_07221a21`: $tco_base_a_07221a21
  - `$tco_a_07221a22`: n/a
  - `$tco_a_07221a23`: n/a
  - `$tco_a_07221b`: n/a
  - `$tco_a_07221c1`: $tco_base_a_07221c1
  - `$tco_a_07221c2`: n/a
  - `$tco_a_07221c3`: n/a
  - `$tco_a_07221c4`: n/a
  - `$tco_a_07221d`: n/a
  - `$tco_a_07221e`: n/a


---

## Policy: tscmm_lv
### 1. Function: DefVar
  - **i_tscmm**: `0`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `!(dag<24 & dec>2) &  !(nDepChildrenOfCouple#1>=1) & !(nChildrenOfCouple#2>=3 & nDepChildrenOfCouple#3>=1)
 & ((poatx=0 & dag00<$PensAgeMale & dgn=1) | (poatx=0& dag00<$PensAgeFem & dgn=0)) & yem>0 & yemmy>0 & (yemmy+ysemy)<=12 & (yem*12/yemmy)<$MinWage`
  - **Tax Unit:** `tu_individual_lv`

### 3. Function: ArithOp
  **Formula:** `($MinWage-yem*12/yemmy)*($tscee_rate1+$tscer_rate1)`
  **Output Variable:** `i_tscmm`
  **Tax Unit:** `tu_individual_lv`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `!(dag<24 & dec>2) &  !(nDepChildrenOfCouple#1>=1) & !(nChildrenOfCouple#2>=3 & nDepChildrenOfCouple#3>=1)
 & ((poatx=0 & dag00<$PensAgeMale & dgn=1) | (poatx=0 & dag00<$PensAgeFem & dgn=0))  & yem>0 & yemmy>0 & ysemy>0 & (yem*12/yemmy)<$MinWage & (yemmy+ysemy)>12`
  - **Tax Unit:** `tu_individual_lv`

### 5. Function: BenCalc
  - **Who_Must_Be_Elig**: `all`
  - **Comp_Cond**: `($MinWage-yem*12/yemmy-yse*12/ysemy)<0`
  - **Comp_perTU**: `($MinWage-yem*12/yemmy)*($tscee_rate1+$tscer_rate1)*(12-ysemy)/yemmy`
  - **Output_Add_Var**: `i_tscmm`
  - **TAX_UNIT**: `tu_individual_lv`

### 6. Function: ArithOp
  **Formula:** `i_tscmm*yemmy#1/12`
  **Output Variable:** `tscmm_s`
  **Tax Unit:** `tu_individual_lv`


---

## Policy: bec_lv *(Switch: n/a)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_bec_rand**: `n/a`
  - **Var_Monetary**: `n/a`

### 2. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$bfaec_amt`: n/a
  - `$bpeec_amt`: n/a
  - `$bpeec02_amt1`: n/a
  - `$bpeec02_amt2`: n/a
  - `$bpeec02_amt3`: n/a
  - `$bpeec02_rate1`: n/a
  - `$bpeec02_rate2`: n/a
  - `$bpeec02_rate3`: n/a
  - `$bpeec01_amt1`: n/a
  - `$bpeec01_amt2`: n/a
  - `$bpeec01_amt3`: n/a
  - `$bpeec01_lim1`: n/a
  - `$bpeec01_lim2`: n/a

### 3. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 5. Function: DefTu *(Switch: n/a)*
  - **Name**: `n/a`
  - **Type**: `n/a`
  - **Members**: `n/a`
  - **DepChildCond**: `n/a`
  - **NoChildIfHead**: `n/a`
  - **NoChildIfPartner**: `n/a`
  - **ExtHeadCond**: `n/a`
  - **StopIfNoHeadFound**: `n/a`

### 6. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 7. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 8. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 9. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 10. Function: RandSeed *(Switch: n/a)*
  - **Seed**: `n/a`

### 11. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 12. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 13. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 14. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 15. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
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

### 19. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `n/a`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`


---
