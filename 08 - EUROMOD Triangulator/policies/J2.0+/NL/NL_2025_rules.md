# EUROMOD Tax-Benefit Rules for NL_2025

## Policy: uprate_nl
### 1. Function: Uprate
  - **dataset**: `*training_data`
  - **def_factor**: `1`
  - **WarnIfNoFactor**: `no`
  - **Dataset**: `*_hhot`

### 2. Function: SetDefault
  - **dataset**: `nl_2007_a4`
  - **bunct_s**: `bunct`
  - **Dataset**: `nl_20??_??_*`

### 3. Function: SetDefault
  - **Dataset**: `nl_20??_??_*`
  - **ydses_o**: `0`
  - **kfbcc**: `0`
  - **bch**: `0`
  - **yemmy00**: `0`
  - **tscer**: `0`
  - **tscse**: `0`
  - **tscee**: `0`
  - **tin**: `0`
  - **yemmy**: `0`
  - **bcbma02**: `0`
  - **bcbma01**: `0`
  - **yptmp**: `0`
  - **yprrt**: `ypr`
  - **ypr**: `yprrt`
  - **ymwdt**: `0`
  - **kivho**: `0`

### 4. Function: Uprate
  - **dataset**: `nl_20??_??`
  - **WarnIfNoFactor**: `yes`
  - **yivwg**: `$f_hourly_wage`
  - **yse**: `$f_hourly_wage`
  - **Factor_Condition**: `lindi <1 | lindi > 12`
  - **yem**: `n/a`
  - **bcbma01**: `$f_hourly_wage`
  - **bcbma02**: `$f_hourly_wage`
  - **yem_a**: `$f_hourly_wage`
  - **yem18_a**: `$f_hourly_wage`
  - **yem19_a**: `$f_hourly_wage`
  - **yem20_a**: `$f_hourly_wage`
  - **yiy**: `$f_hourly_wage`
  - **ypt**: `$f_ypt`
  - **bed**: `$f_bed`
  - **pdi**: `$f_minw`
  - **afc**: `$f_hourly_wage`
  - **bched**: `$f_bed`
  - **bfa**: `$f_bfa`
  - **bch**: `$f_cpi`
  - **bhl**: `$f_hourly_wage`
  - **bho**: `$f_cpi`
  - **bsa00**: `$f_cpi`
  - **bsaot**: `$f_minw`
  - **aggvar_name**: `poa`
  - **aggvar_part**: `poacm`
  - **aggvar_tolerance**: `1`
  - **bunct**: `$f_minw`
  - **bunst**: `$f_minw`
  - **kfb**: `$f_hourly_wage`
  - **kivho**: `$f_cpi`
  - **poa00**: `$f_poa00`
  - **poacm**: `$f_poacm`
  - **psu**: `$f_psu`
  - **tad**: `$f_const`
  - **tis**: `$f_const`
  - **tin**: `$f_const`
  - **tscee**: `$f_const`
  - **tscse**: `$f_const`
  - **tscer**: `$f_const`
  - **tpcpe**: `$f_hourly_wage`
  - **tpr**: `$f_cpi`
  - **xhc**: `$f_cpi`
  - **xhcmomi**: `$f_cpi`
  - **xhcot**: `$f_cpi`
  - **xhcrt**: `$f_cpi`
  - **xmp**: `$f_cpi`
  - **xmp00**: `$f_cpi`
  - **xmp01**: `$f_cpi`
  - **xpp**: `$f_cpi`
  - **yds**: `$f_const`
  - **yot**: `$f_hourly_wage`
  - **ypp**: `$f_poacm`
  - **yprrt**: `$f_hourly_wage`
  - **AggVar_Name**: `ypr`
  - **AggVar_Part**: `yprrt`
  - **yptmpnt**: `$f_ypt`
  - **yptmptx**: `$f_ypt`
  - **yptmp**: `$f_ypt`
  - **kfbcc**: `$f_const`
  - **ydses_o**: `$f_const`
  - **ymwdt**: `$f_wgLead`
  - **amriv**: `$f_amriv`
  - **xed00**: `$f_cpi`
  - **xhl00**: `$f_cpi`
  - **Dataset**: `nl_20??_??_*`


---

## Policy: ildef_nl
### 1. Function: DefIl
  - **name**: `il_taxabley_work`
  - **yem**: `+`
  - **yse**: `+`
  - **bhl**: `+`
  - **kfb**: `+`
  - **tpcpe**: `-`
  - **tschl00_s**: `n/a`
  - **bcbma01**: `+`
  - **bcbma02**: `+`
  - **bma_s**: `+`

### 2. Function: DefIl
  - **name**: `il_taxabley_work4pen`
  - **yem**: `+`
  - **yse**: `+`
  - **bhl**: `+`
  - **kfb**: `+`
  - **tpcpe**: `-`
  - **bcbma01**: `+`
  - **bcbma02**: `+`
  - **bma_s**: `+`

### 3. Function: DefIl
  - **name**: `il_sic`
  - **yem**: `+`
  - **bunct_s**: `+`
  - **bunst**: `+`
  - **pdi**: `+`
  - **tpcpe**: `-`
  - **bcbma01**: `+`
  - **bcbma02**: `+`
  - **bma_s**: `+`

### 4. Function: DefIl
  - **name**: `il_pns_linkedwork`
  - **bunct_s**: `+`
  - **bunst**: `+`
  - **pdi**: `+`
  - **bed**: `+`
  - **bsaot**: `+`
  - **ypp**: `+`

### 5. Function: DefIl
  - **Name**: `il_sf`
  - **bmcer_s**: `n/a`

### 6. Function: DefIl
  - **Name**: `ils_extstat_other`
  - **tschl_s**: `+`


---

## Policy: tudef_nl
### 1. Function: DefTu
  - **Name**: `tu_hh_oecd_co`
  - **Type**: `HH`
  - **DepChildCond**: `dag<14`

### 2. Function: DefTu
  - **Name**: `tu_individual_nl`
  - **Type**: `IND`
  - **DepChildCond**: `dag<=17`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`

### 3. Function: DefTu
  - **Name**: `tu_household_nl`
  - **Type**: `HH`
  - **DepChildCond**: `dag<=15 | ((dag=16 |dag=17) &  ((les=6|dec>0) | les=5 | IsDisabled))`
  - **#_level**: `n/a`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`

### 4. Function: DefTu
  - **Name**: `tu_couple_nl`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner`
  - **LoneParentCond**: `Default &! (IsMarried | IsCohabiting)`

### 5. Function: DefTu
  - **Name**: `tu_sben_family_nl`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild & LooseDepChild`
  - **DepChildCond**: `dag<=15 | (dag<=17  & ((les=6|dec>0) | les=5 | IsDisabled))`
  - **#_level**: `n/a`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`

### 6. Function: DefTu
  - **name**: `tu_Childunder18_nl`
  - **type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `dag<18`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`

### 7. Function: DefTu
  - **name**: `tu_Child16_17_nl`
  - **type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `dag=16|dag =17`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`

### 8. Function: DefTu
  - **name**: `tu_Child12_15_nl`
  - **type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `dag>11&dag <16`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`

### 9. Function: DefTu
  - **name**: `tu_Childunder16_nl`
  - **type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `dag<=16`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`

### 10. Function: DefTu
  - **name**: `tu_Childunder5_nl`
  - **type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `dag<5`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`

### 11. Function: DefTu
  - **name**: `tu_Childunder7_nl`
  - **type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `dag<7`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`

### 12. Function: DefTu
  - **name**: `tu_SingleParent_nl`
  - **type**: `SUBGROUP`
  - **members**: `OwnDepChild`
  - **DepChildCond**: `dag<=27`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`

### 13. Function: DefTu
  - **name**: `tu_Childunder12_nl`
  - **type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `dag<=12`
  - **LoneParentCond**: `Default & !(IsMarried | IsCohabiting)`


---

## Policy: constdef_nl
### 1. Function: DefConst
  **Constants Defined:**
  - `$PenAge`: 67
  - `const_monetary`: no

### 2. Function: DefConst
  **Constants Defined:**
  - `$gUB_QperMin`: 26
  - `$gUB_QperTot`: 36
  - `$Nwh`: 37
  - `$ImputedWage`: 0
  - `$eUB_QperTot`: 48
  - `$eUB_QperMinDd`: 52
  - `$mc_my`: 10

### 3. Function: InitVars
  - **kivhooo_s**: `kivho`

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
  - `$bsa00_BTA_rate`: 1
  - `$bsa00_BCA_rate`: 1

### 6. Function: DefConst
  **Constants Defined:**
  - `$MinWage_m`: 2191.80#m
  - `$Nwh`: 38
  - `const_monetary`: no

### 7. Function: DefConst
  **Constants Defined:**
  - `$tin_bandlim1`: 38441#y
  - `$tin_bandlim1a`: 40502#y
  - `$tin_bandlim2`: 76817#y
  - `$tin_birthyear`: 1946
  - `$tin_taxyear`: 2025

### 8. Function: DefConst
  **Constants Defined:**
  - `$EI_maxdwag`: 290.67#d


---

## Policy: InitVar_nl
### 1. Function: DefVar
  - **i_tinyse**: `0`
  - **var_monetary**: `no`
  - **i_band2**: `0`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yse >= 0.6 * ils_earns & yse > 0 & lhw >  23`
  - **Tax Unit:** `tu_individual_nl`

### 3. Function: BenCalc
  - **comp_cond**: `dag > 79`
  - **comp_perTU**: `40502#y`
  - **output_var**: `i_band2`
  - **TAX_UNIT**: `tu_individual_nl`

### 4. Function: BenCalc
  - **Comp_Cond**: `bcbma01=0 & bcbma02=0`
  - **Comp_perTU**: `yemmy`
  - **Output_Var**: `yemmy`
  - **TAX_UNIT**: `tu_individual_nl`

### 5. Function: DefVar *(Switch: n/a)*
  - **i_loss_turnover**: `n/a`
  - **Var_Monetary**: `n/a`


---

## Policy: yem_nl
### 1. Function: DefVar
  - **i_minwage_m**: `0`
  - **i_mwrt**: `0`
  - **i_yem**: `0`

### 2. Function: DefConst
  **Constants Defined:**
  - `$MinWage_m`: 2191.80#m
  - `$Nwh`: 38
  - `const_monetary`: no

### 3. Function: BenCalc
  - **comp_cond**: `dag = 15`
  - **comp_perTU**: `0.3`
  - **output_var**: `i_mwrt`
  - **TAX_UNIT**: `tu_individual_nl`

### 4. Function: ArithOp
  **Formula:** `($MinWage_m * i_mwrt) + ($MinWage_m * i_mwrt)*0.08`
  **Output Variable:** `i_minwage_m`
  **Tax Unit:** `tu_individual_nl`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem > 0`
  - **Tax Unit:** `tu_individual_nl`

### 6. Function: Max
  - **who_must_be_elig**: `one`
  - **val**: `i_minwage_m*min(lhw,$Nwh)/$Nwh*yemmy/12`
  - **output_var**: `i_yem`
  - **TAX_UNIT**: `tu_individual_nl`

### 7. Function: Max
  - **val**: `i_yem`
  - **output_var**: `yem`
  - **TAX_UNIT**: `tu_individual_nl`

### 8. Function: ChangeParam
  - **Param_Id**: `8344a9ee-afd4-4b04-b06f-788dd354db08`
  - **Param_NewVal**: `nl_2025_yem_std`


---

## Policy: neg_nl
### 1. Function: DefVar
  - **i_yse0**: `0`

### 2. Function: ArithOp
  **Formula:** `yse`
  **Output Variable:** `i_yse0`
  **Tax Unit:** `tu_individual_nl`

### 3. Function: Max
  - **val**: `0`
  - **output_var**: `yse`
  - **TAX_UNIT**: `tu_individual_nl`


---

## Policy: bfa_nl
### 1. Function: DefConst
  **Constants Defined:**
  - `$bfa_bchqtr_amt`: 286.45#q
  - `$bfa_mult1`: 1
  - `$bfa_mult2`: 1.2143
  - `$bfa_mult3`: 1.4286

### 2. Function: DefVar
  - **i_chbrt**: `0`

### 3. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 4. Function: BenCalc
  - **comp_cond**: `IsDepChild & (dag>=12 & dag<=17)`
  - **comp_perElig**: `$bfa_mult3`
  - **output_var**: `i_chbrt`
  - **TAX_UNIT**: `tu_sben_family_nl`

### 5. Function: ArithOp
  **Formula:** `i_chbrt * $bfa_bchqtr_amt`
  **Output Variable:** `bfa_s`
  **Tax Unit:** `tu_sben_family_nl`


---

## Policy: bunct_nl
### 1. Function: DefVar
  - **i_gubelig**: `0`
  - **var_monetary**: `no`
  - **i_eubelig**: `0`
  - **i_liwdy**: `0`
  - **maxbunctmy01_s**: `0`
  - **bunctmy01_s**: `0`
  - **i_bunct01**: `0`
  - **i_bunct02**: `0`

### 2. Function: BenCalc
  - **comp_cond**: `bunct > 0`
  - **comp_perElig**: `if(bunmy=0, 0, 1/0.7*bunct*12/bunmy)`
  - **output_var**: `yempv`
  - **TAX_UNIT**: `tu_individual_nl`
  - **Run_Cond**: `!IsUsedDatabase#1`
  - **#_DataBasename**: `*hhot`

### 3. Function: ArithOp
  **Formula:** `max(lunmy,bunmy)`
  **Output Variable:** `lunmy_s`
  **Tax Unit:** `tu_individual_nl`

### 4. Function: ArithOp
  **Formula:** `min(liwmy*52/12,liwwh*52/12)`
  **Output Variable:** `liwmy_s`
  **Tax Unit:** `tu_individual_nl`

### 5. Function: ArithOp
  **Formula:** `min(liwmy_s*$gUB_QperTot / max(52,1),max(liwwh*52/12,0)+liwmy_s)`
  **Output Variable:** `sin02_s`
  **Tax Unit:** `tu_individual_nl`

### 6. Function: BenCalc
  - **comp_cond**: `lunmy_s > 0 & bunct = 0`
  - **comp_perElig**: `0`
  - **output_var**: `sin02_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 7. Function: ArithOp
  **Formula:** `sin02_s *12/52`
  **Output Variable:** `liwmy_s`
  **Tax Unit:** `tu_individual_nl`

### 8. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `yem = 0 | bunct > 0`
  - **comp_perElig**: `lunmy_s`
  - **output_var**: `lunmy_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 9. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lunmy_s > 0 & sin02_s >= $gUB_QperMin & dag >= 15 & dag<=$PenAge & (yem >=0 | i_tinyse=0)`
  - **Tax Unit:** `tu_individual_nl`

### 10. Function: ArithOp
  **Formula:** `min(lunmy_s,3)`
  **Output Variable:** `bunctmy_s`
  **Tax Unit:** `tu_individual_nl`

### 11. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **elig_var**: `i_gubelig`
  - **comp_cond**: `lunmy_s > 0 & bunct = 0`
  - **comp_perElig**: `0`
  - **output_var**: `yempv_s`
  - **TAX_UNIT**: `tu_individual_nl`
  - **Comp_perElig**: `yivwg * $Nwh * 52/12`
  - **Comp_Cond**: `lunmy_s>0`
  - **Comp_perTU**: `yempv`

### 12. Function: ArithOp *(Switch: off)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 13. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **elig_var**: `i_gubelig`
  - **comp_cond**: `bunctmy_s>2`
  - **comp_perElig**: `(75%*min(yempv_s,290.67#d)*2+70%*min(yempv_s,290.67#d))/12`
  - **output_var**: `sin04_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 14. Function: ArithOp
  **Formula:** `lhw/8`
  **Output Variable:** `i_liwdy`
  **Tax Unit:** `tu_individual_nl`

### 15. Function: ArithOp
  **Formula:** `sin02_s * i_liwdy`
  **Output Variable:** `sin05_s`
  **Tax Unit:** `tu_individual_nl`

### 16. Function: ArithOp
  **Formula:** `max(sin05_s*$eUB_QperTot /12,max(liwwh*52/12*max(i_liwdy,5),0))`
  **Output Variable:** `sin06_s`
  **Tax Unit:** `tu_individual_nl`

### 17. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_gubelig=1 & sin06_s > ($eUB_QperMinDd * $eUB_QperTot /12)`
  - **Tax Unit:** `tu_individual_nl`

### 18. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **elig_var**: `i_eubelig`
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **lowlim**: `3`
  - **uplim**: `24`
  - **output_var**: `maxbunctmy01_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 19. Function: ArithOp
  **Formula:** `min(lunmy_s,maxbunctmy01_s)`
  **Output Variable:** `bunctmy01_s`
  **Tax Unit:** `tu_individual_nl`

### 20. Function: ArithOp *(Switch: off)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 21. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **elig_var**: `i_eubelig`
  - **comp_cond**: `bunctmy01_s>2`
  - **comp_perElig**: `((75%*min(yempv_s,290.67#d)*2)+(70%*min(yempv_s,290.67#d)*min((bunctmy01_s-2),10)))/12`
  - **output_var**: `sin07_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 22. Function: BenCalc
  - **comp_cond**: `i_eubelig=0 & i_gubelig=1`
  - **comp_perElig**: `sin04_s`
  - **output_var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 23. Function: SetDefault
  - **Dataset**: `*`
  - **yempv**: `0`

### 24. Function: Elig *(Switch: off)*
  **Eligibility Check:**
  - **Condition:** `lunmy_s>0 & liwwh09_h>6.5 & dag>=15 & dag<=$PenAge & (yem>=0 | i_tinyse=0)`
  - **Tax Unit:** `tu_individual_nl`

### 25. Function: Elig *(Switch: off)*
  **Eligibility Check:**
  - **Condition:** `i_gubelig=1 & liwwhnd_h>=(52*4/5)`
  - **Tax Unit:** `tu_individual_nl`

### 26. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **elig_var**: `i_gubelig`
  - **comp_cond**: `(bunctmy_s>2) & (bunctmy_s<=12)`
  - **comp_perElig**: `(70%*min(yempv_s,290.67#d))`
  - **output_var**: `i_bunct01`
  - **TAX_UNIT**: `tu_individual_nl`

### 27. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **elig_var**: `i_eubelig`
  - **comp_cond**: `(bunctmy01_s>2) & (bunctmy01_s<=12)`
  - **comp_perElig**: `(70%*min(yempv_s,290.67#d))`
  - **output_var**: `i_bunct02`
  - **TAX_UNIT**: `tu_individual_nl`

### 28. Function: BenCalc
  - **comp_cond**: `i_eubelig=0 & i_gubelig=1`
  - **comp_perElig**: `i_bunct01`
  - **output_var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 29. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `bunmy <lunmy_s`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_nl`


---

## Policy: psu_nl
### 1. Function: DefVar
  - **i_eligpsu**: `0`
  - **var_monetary**: `no`
  - **i_psu01**: `0`
  - **i_psu02**: `0`

### 2. Function: DefIl
  - **name**: `il_psu_fromwork_60`
  - **il_taxabley_work4pen**: `+`
  - **ypp**: `+`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag<$PenAge & dms=5 & idpartner=0 & (nDepChInTu>0 | ddi=1 )`
  - **Tax Unit:** `tu_Childunder18_nl`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_eligpsu=1 & dgn=1 & dag>=60`
  - **Tax Unit:** `tu_Childunder18_nl`

### 5. Function: ArithOp
  **Formula:** `$psu_base-il_pns_linkedwork-max(0,il_psu_fromwork_60-(0.5*$MinWage_m+0.333*max(0,il_psu_fromwork_60-0.5*$MinWage_m)))`
  **Output Variable:** `i_psu01`
  **Tax Unit:** `tu_Childunder18_nl`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_eligpsu=1 &  ( (dag<60 & dgn=1) | (dgn=0))`
  - **Tax Unit:** `tu_Childunder18_nl`

### 7. Function: ArithOp
  **Formula:** `$psu_base-il_pns_linkedwork-max(0,il_taxabley_work4pen-(0.5*$MinWage_m+0.333*max(0,il_taxabley_work4pen-0.5*$MinWage_m)))`
  **Output Variable:** ``
  **Tax Unit:** `tu_Childunder18_nl`

### 8. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **#_info**: `n/a`
  - **comp_perElig**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 9. Function: ArithOp
  **Formula:** `i_psu01`
  **Output Variable:** `psu_s`
  **Tax Unit:** `tu_Childunder18_nl`

### 10. Function: DefConst
  **Constants Defined:**
  - `$psu_base`: 1717.38#m


---

## Policy: poa_nl
### 1. Function: DefVar
  - **i_POAmeans**: `0`

### 2. Function: BenCalc
  - **comp_cond**: `(dag>=$PenAge | GetPartnerInfo#1>=76) & IsWithPartner`
  - **comp_perElig**: `$poa_couple`
  - **#_info**: `dag`
  - **output_var**: `poa00_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 3. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag<$PenAge & poa00_s>0`
  - **Tax Unit:** `tu_individual_nl`

### 5. Function: ArithOp
  **Formula:** `il_pns_linkedwork+2/3*max(0,il_taxabley_work4pen-0.15*$MinWage_m)`
  **Output Variable:** `i_POAmeans`
  **Tax Unit:** `tu_individual_nl`

### 6. Function: ArithOp
  **Formula:** `poa00_s - i_POAmeans`
  **Output Variable:** `poa00_s`
  **Tax Unit:** `tu_individual_nl`

### 7. Function: Allocate
  - **share**: `poa00_s`
  - **share_between**: `dag >= $PenAge`
  - **share_all_ifnoelig**: `no`
  - **output_var**: `poa00_s`
  - **TAX_UNIT**: `tu_couple_nl`

### 8. Function: ArithOp
  **Formula:** `il_taxabley_work4pen`
  **Output Variable:** `sin40_s`
  **Tax Unit:** `tu_individual_nl`

### 9. Function: DefConst
  **Constants Defined:**
  - `$poa_single`: 1683.38#m
  - `$poa_couple`: 1154.68#m


---

## Policy: eesic_nl
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem>0&dag<$PenAge &poa00_s=0`
  - **Tax Unit:** `tu_individual_nl`

### 2. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_nl`
  - **Output Variable:** `tsceeui_s`

### 3. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$sic_rate`: n/a


---

## Policy: tschl_nl
### 1. Function: DefIl
  - **name**: `il_tschl1_yem`
  - **yem**: `+`
  - **bhl**: `+`
  - **tpcpe**: `-`
  - **bcbma01**: `+`
  - **bcbma02**: `+`
  - **bma_s**: `+`

### 2. Function: DefIl
  - **name**: `il_tschl1_nl`
  - **il_tschl1_yem**: `+`
  - **bunct_s**: `+`
  - **bunst**: `+`
  - **bsaot**: `+`
  - **pdi**: `+`
  - **psu_s**: `+`

### 3. Function: DefIl
  - **name**: `il_tschl2_nl`
  - **poa00_s**: `+`

### 4. Function: DefIl
  - **name**: `il_tschl3_nl`
  - **poacm**: `+`
  - **yse**: `+`

### 5. Function: BenCalc
  - **comp_cond**: `dag>=18`
  - **comp_perTU**: `$tschl_prem_av`
  - **output_var**: `tschlfx_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 6. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_nl`
  - **Output Variable:** `tschl01_s`

### 7. Function: Elig
  **Eligibility Check:**
  - **Condition:** `tschl01_s > 0`
  - **Tax Unit:** `tu_individual_nl`

### 8. Function: ArithOp
  **Formula:** `il_tschl1_yem / il_tschl1_nl * tschl01_s`
  **Output Variable:** `tschl00_s`
  **Tax Unit:** `tu_individual_nl`

### 9. Function: BenCalc
  - **comp_cond**: `il_tschl2_nl>0`
  - **comp_perTU**: `$tschl_rate_se*min($tschl_uplim-il_tschl1_nl,il_tschl2_nl)`
  - **lowlim**: `0`
  - **output_var**: `tschl02_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 10. Function: BenCalc
  - **comp_cond**: `il_tschl3_nl>0`
  - **comp_perTU**: `$tschl_rate_se*min($tschl_uplim-il_tschl1_nl-il_tschl2_nl,il_tschl3_nl)`
  - **lowlim**: `0`
  - **output_var**: `tschl03_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 11. Function: ArithOp
  **Formula:** `tschl01_s + tschl02_s + tschl03_s + tschlfx_s`
  **Output Variable:** `tschl_s`
  **Tax Unit:** `tu_individual_nl`

### 12. Function: DefConst
  **Constants Defined:**
  - `$tschl_prem_av`: 1905#y
  - `$tschl_rate_emp`: 6.51%
  - `$tschl_rate_se`: 5.26%
  - `$tschl_uplim`: 75860#y


---

## Policy: tin_nl
### 1. Function: DefVar
  - **i_netIR**: `0`
  - **i_elig**: `0`
  - **var_monetary**: `no`
  - **i_minIRMI**: `0`
  - **i_mkb**: `0`
  - **i_IR**: `0`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_tinyse = 1`
  - **Tax Unit:** `tu_individual_nl`

### 3. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_nl`
  - **Output Variable:** `tinta00_s`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_tinyse = 1 & dag >= $PenAge`
  - **Tax Unit:** `tu_individual_nl`

### 5. Function: ArithOp
  **Formula:** `tinta00_s * (100% - 50%)`
  **Output Variable:** `tinta01_s`
  **Tax Unit:** `tu_individual_nl`

### 6. Function: ArithOp
  **Formula:** `tinta01_s * (-1)`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_nl`

### 7. Function: DefIl
  - **name**: `il_taxabley_box1_exclIR`
  - **yem**: `+`
  - **yse**: `+`
  - **tinta00_s**: `-`
  - **yptmptx**: `+`
  - **ypp**: `+`
  - **yot**: `+`
  - **bunct_s**: `+`
  - **bunst**: `+`
  - **tschl01_s**: `n/a`
  - **poa00_s**: `+`
  - **poacm**: `+`
  - **psu_s**: `+`
  - **kfb**: `+`
  - **pdi**: `+`
  - **bhl**: `+`
  - **bsaot**: `+`
  - **tsceeui_s**: `-`
  - **tpcpe**: `-`
  - **xmp00**: `-`
  - **bcbma01**: `+`
  - **bcbma02**: `+`
  - **bma_s**: `+`

### 8. Function: ArithOp
  **Formula:** `min(kivhooo_s,xhcmomi)`
  **Output Variable:** `i_minIRMI`
  **Tax Unit:** `tu_individual_nl`

### 9. Function: DefIl
  - **name**: `il_taxabley_box1`
  - **il_taxabley_box1_exclIR**: `+`
  - **xhcmomi**: `-`
  - **i_minIRMI**: `+`
  - **i_IR**: `+`

### 10. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_nl`
  - **Output Variable:** `tingt_s`

### 11. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_nl`
  - **Output Variable:** ``
    - Band: Rate=`$tin_br3_red`, Limit=``

### 12. Function: ArithOp
  **Formula:** `$tin_profexempt_se* (yse- tinta00_s)`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_nl`

### 13. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_tinyse = 1`
  - **Tax Unit:** `tu_individual_nl`

### 14. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_tinyse = 1`
  - **Tax Unit:** `tu_individual_nl`

### 15. Function: ArithOp
  **Formula:** `$tin_profexempt_se* (yse- tinta00_s)`
  **Output Variable:** `i_mkb`
  **Tax Unit:** `tu_individual_nl`

### 16. Function: DefIl
  - **name**: `il_taxabley_box1_exclIR_exclSE`
  - **il_taxabley_box1_exclIR**: `+`
  - **i_mkb**: `+`

### 17. Function: BenCalc
  - **Run_Cond**: `IsUsedDatabase#1 | IsUsedDatabase#2`
  - **#_DataBasename**: `nl_2020_b*`
  - **Comp_Cond**: `amriv > $impr_band5`
  - **Comp_perTU**: `($impr_perc_5*$impr_band5 + $impr_perc_6*(amriv - $impr_band5))/12`
  - **Output_Var**: `kivhooo_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 18. Function: Allocate
  - **Run_Cond**: `IsUsedDatabase#1 | IsUsedDatabase#2`
  - **#_DataBasename**: `nl_2020_b*`
  - **Share**: `kivhooo_s`
  - **Share_Between**: `dhr =1`
  - **Output_Var**: `kivhooo_s`
  - **TAX_UNIT**: `tu_household_nl`

### 19. Function: ArithOp
  **Formula:** `$impr_perc_y*max(kivhooo_s-xhcmomi,0)`
  **Output Variable:** `i_IR`
  **Tax Unit:** `tu_individual_nl`

### 20. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_nl`
  - **Output Variable:** ``
    - Band: Rate=`$tin_br3_red`, Limit=``

### 21. Function: DefConst
  **Constants Defined:**
  - `$tin_br1`: 8.17%
  - `$tin_br2`: 37.48%
  - `$tin_br3`: 49.50%
  - `$tin_br3_red`: 12.02%

### 22. Function: DefConst
  **Constants Defined:**
  - `$tin_deduc_se`: 2470#y
  - `$tin_profexempt_se`: 12.7%

### 23. Function: DefConst
  **Constants Defined:**
  - `$impr_band1`: 12500#c
  - `$impr_band2`: 25000#c
  - `$impr_band3`: 50000#c
  - `$impr_band4`: 75000#c
  - `$impr_band5`: 1330000#c
  - `$impr_perc_1`: 0%
  - `$impr_perc_2`: 0.1%
  - `$impr_perc_3`: 0.2%
  - `$impr_perc_4`: 0.25%
  - `$impr_perc_5`: 0.35%
  - `$impr_perc_6`: 2.35%
  - `$impr_perc_y`: 23.33%


---

## Policy: tinkt_nl
### 1. Function: DefVar
  - **i_GenAsset**: `0`
  - **i_OldAgeAsset**: `0`
  - **i_taxbase_box3**: `0`
  - **i_ChildAsset**: `0`

### 2. Function: BenCalc
  - **comp_cond**: `!IsDepChild`
  - **comp_perElig**: `$tinkt_assetlim_ch`
  - **output_var**: `i_GenAsset`
  - **TAX_UNIT**: `tu_individual_nl`

### 3. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 4. Function: Elig *(Switch: off)*
  **Eligibility Check:**
  - **Condition:** `dag > =$PenAge & afc < ($tinkt_assetlim* nPersInTu)`
  - **Tax Unit:** `tu_couple_nl`

### 5. Function: BenCalc *(Switch: off)*
  - **who_must_be_elig**: `one`
  - **comp_cond**: `il_taxabley_box1<=$tinkt_inclim_l`
  - **comp_perTU**: `0`
  - **output_var**: `i_OldAgeAsset`
  - **TAX_UNIT**: `tu_individual_nl`

### 6. Function: ArithOp *(Switch: off)*
  **Formula:** `((afc -i_GenAsset - i_ChildAsset - i_OldAgeAsset)/12 )* 4%`
  **Output Variable:** `i_taxbase_box3`
  **Tax Unit:** `tu_couple_nl`

### 7. Function: ArithOp
  **Formula:** `i_taxbase_box3 * 36%`
  **Output Variable:** `tinkt_s`
  **Tax Unit:** `tu_couple_nl`

### 8. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_couple_nl`
  - **Output Variable:** `i_taxbase_box3`
    - Band: Rate=`6.17%`, Limit=``

### 9. Function: DefConst
  **Constants Defined:**
  - `$tinkt_assetlim_ch`: 57684#c
  - `$tinkt_assetlim`: 282226#c
  - `$tinkt_inclim_l`: 14431#y
  - `$tinkt_inclim_u`: 20075#y


---

## Policy: peoplesic_nl
### 1. Function: DefVar
  - **i_Pisurvivor**: `0`
  - **i_Pihealth**: `0`
  - **i_PIpension**: `0`

### 2. Function: DefConst
  **Constants Defined:**
  - `$peoplesic_aow_rate`: 17.9%
  - `const_monetary`: no
  - `$peoplesic_anw_rate`: 0.1%
  - `$peoplesic_awbz_rate`: 9.65%
  - `$peoplesic_maxbase`: n/a

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `il_taxabley_box1>0`
  - **Tax Unit:** `tu_individual_nl`

### 4. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_nl`
  - **Output Variable:** `tsceepigr_s`

### 5. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_nl`
  - **Output Variable:** ``

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag<$PenAge & il_taxabley_box1>0`
  - **Tax Unit:** `tu_individual_nl`

### 7. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_nl`
  - **Output Variable:** ``


---

## Policy: tintc_nl
### 1. Function: DefIl
  - **name**: `il_taxabley_worktc`
  - **il_taxabley_work**: `+`
  - **tsceeui_s**: `-`

### 2. Function: BenCalc
  - **comp_cond**: `dag>=$PenAge`
  - **comp_perTU**: `$tin_gtc_spa`
  - **output_var**: `tintc00_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `il_taxabley_worktc>0 & dag<$PenAge`
  - **Tax Unit:** `tu_individual_nl`

### 4. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_nl`
  - **Output Variable:** `tintcee_s`
    - Band: Rate=`$tin_wtc_p3`, Limit=``

### 5. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 6. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** ``

### 7. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 8. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** ``

### 9. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 10. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** ``

### 11. Function: Elig
  **Eligibility Check:**
  - **Condition:** `il_taxabley_worktc>0 & dag>=$PenAge`
  - **Tax Unit:** `tu_individual_nl`

### 12. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_nl`
  - **Output Variable:** ``
    - Band: Rate=`$tin_wtc_p3_spa`, Limit=``

### 13. Function: DefVar
  - **i_hiTC**: `0`
  - **i_OATCbonus**: `0`
  - **i_ERtc**: `0`

### 14. Function: BenCalc
  - **comp_cond**: `il_taxabley_worktc>$tin_wtc_inclim & dag >= $PenAge`
  - **comp_perElig**: `(il_taxabley_worktc-$tin_wtc_inclim)*$tin_wtc_pred_spa *(-1)`
  - **result_var**: `i_hiTC`
  - **output_add_var**: `tintcee_s`
  - **TAX_UNIT**: `tu_individual_nl`
  - **Comp_LowLim**: `-$tin_wtc_spa`

### 15. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **comp_uplim**: `n/a`
  - **result_var**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 16. Function: DefVar
  - **i_eligchtc**: `0`
  - **var_monetary**: `no`
  - **i_CombCredit**: `0`
  - **i_eligscctc**: `0`
  - **i_SuppCombCredit**: `0`
  - **i_tcOA**: `0`
  - **i_SuppOA**: `0`
  - **i_GrossTotalTax**: `0`
  - **i_NetTotalTax**: `0`
  - **i_NetTotalTaxNonRef**: `0`
  - **i_ratioPC**: `0`
  - **i_unusedTaxCredit**: `0`
  - **i_unusedTaxRefund**: `0`
  - **i_TotalTaxableIncome**: `0`

### 17. Function: ArithOp
  **Formula:** `il_taxabley_box1+i_taxbase_box3`
  **Output Variable:** `i_TotalTaxableIncome`
  **Tax Unit:** `tu_individual_nl`

### 18. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 19. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 20. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_level**: `n/a`
  - **lowlim**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 21. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **#_level**: `n/a`
  - **comp_perElig**: `n/a`
  - **result_var**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 22. Function: Elig
  **Eligibility Check:**
  - **Condition:** `HasMinValInTu#1`
  - **Tax Unit:** `tu_couple_nl`

### 23. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_eligscctc = 1 & (GetPartnerInfo#1 = 0 | dag >GetPartnerInfo#2 | (dag = GetPartnerInfo#2 & idperson < GetPartnerInfo#3))`
  - **Tax Unit:** `tu_couple_nl`

### 24. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **result_var**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 25. Function: BenCalc
  - **comp_cond**: `i_eligscctc = 1 & (il_taxabley_worktc > $tin_irc_lowlim | tinta00_s > 0) & nDepChildrenInTU#1>0 & dag >= $PenAge`
  - **#_level**: `tu_Childunder12_nl`
  - **comp_perElig**: `$tin_irc_perc_spa*max(il_taxabley_worktc-$tin_irc_lowlim,0)`
  - **comp_lowlim**: `0`
  - **comp_uplim**: `($tin_irc_uplim- $tin_irc_lowlim)* $tin_irc_perc_spa`
  - **result_var**: `i_CombCredit`
  - **output_var**: `tintcch00_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 26. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 27. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **comp_uplim**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 28. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(IsWithPartner & GetPartnerInfo#1 >=$PenAge) | !IsWithPartner`
  - **Tax Unit:** `tu_individual_nl`

### 29. Function: BenCalc
  - **comp_cond**: `dag>=$PenAge& (il_taxabley_box1+i_taxbase_box3 * sel_s)<$tin_oac_inclow`
  - **comp_perTU**: `$tin_oac`
  - **result_var**: `i_tcOA`
  - **output_var**: `tintcpe_s`
  - **TAX_UNIT**: `tu_individual_nl`
  - **Comp_Cond**: `dag>=$PenAge& (il_taxabley_box1+i_taxbase_box3 * sel_s)>=$tin_oac_inclow`
  - **Comp_perTU**: `max($tin_oac-$tin_oac_pred*((il_taxabley_box1+i_taxbase_box3*sel_s)-$tin_oac_inclow),0)`

### 30. Function: BenCalc
  - **comp_cond**: `dag>=$PenAge & !IsWithPartner & poa00_s>0 &tintcpe_s>0`
  - **comp_perTU**: `$tin_oac_sp`
  - **result_var**: `i_SuppOA`
  - **output_add_var**: `tintcpe_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 31. Function: DefIl
  - **name**: `il_tintc_refund`
  - **tintc00_s**: `+`
  - **tintcee_s**: `+`
  - **tintcch_s**: `n/a`
  - **tintcch00_s**: `+`

### 32. Function: DefIl
  - **name**: `il_tintc_total`
  - **il_tintc_refund**: `+`
  - **tintclp_s**: `n/a`
  - **tintclp00_s**: `n/a`
  - **tintcpe_s**: `+`

### 33. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 34. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **comp_uplim**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Comp_LowLim**: `n/a`
  - **Who_Must_Be_Elig**: `n/a`

### 35. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **UpLim**: `n/a`

### 36. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 37. Function: BenCalc
  - **comp_cond**: `il_taxabley_box1>$tin_gtc_inclim & dag >= $PenAge`
  - **comp_perElig**: `(il_taxabley_box1-$tin_gtc_inclim)*$tin_gtc_pred_spa *(-1)`
  - **output_add_var**: `tintc00_s`
  - **TAX_UNIT**: `tu_individual_nl`
  - **Comp_LowLim**: `-$tin_gtc_spa`

### 38. Function: DefConst
  **Constants Defined:**
  - `$tin_gtc`: 3068#y
  - `$tin_gtc_spa`: 1536#y
  - `$tin_gtc_inclim`: 28406#y
  - `$tin_gtc_pred`: 6.337%
  - `$tin_gtc_pred_spa`: 3.170%

### 39. Function: DefConst
  **Constants Defined:**
  - `$tin_wtc`: 5599#y
  - `$tin_wtc_p1`: 8.053%
  - `$tin_wtc_b1_l`: 12169#y
  - `$tin_wtc_p2`: 30.030%
  - `$tin_wtc_b2_l`: 26288#y
  - `$tin_wtc_p3`: 2.258%
  - `$tin_wtc_spa`: 2802#y
  - `$tin_wtc_p1_spa`: 4.029%
  - `$tin_wtc_p2_spa`: 15.023%
  - `$tin_wtc_p3_spa`: 1.130%
  - `$tin_wtc_inclim`: 43071#y
  - `$tin_wtc_pred`: 6.51%
  - `$tin_wtc_pred_spa`: 3.257%

### 40. Function: DefConst
  **Constants Defined:**
  - `$tin_irc_lowlim`: 6145#y
  - `$tin_irc_uplim`: 32223#y
  - `$tin_irc_perc`: 11.45%
  - `$tin_irc_perc_spa`: 5.73%

### 41. Function: DefConst
  **Constants Defined:**
  - `$tin_oac`: 2035#y
  - `$tin_oac_inclow`: 45308#y
  - `$tin_oac_incupp`: 58875#y
  - `$tin_oac_pred`: 15%
  - `$tin_oac_sp`: 531#y


---

## Policy: chall_nl
### 1. Function: DefVar
  - **i_eligchtc**: `0`
  - **var_monetary**: `no`
  - **i_TotalTaxableIncome**: `0`

### 2. Function: ArithOp
  **Formula:** `il_taxabley_box1+i_taxbase_box3`
  **Output Variable:** `i_TotalTaxableIncome`
  **Tax Unit:** `tu_individual_nl`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `nDepChildrenInTU > 0 & !IsDepChild & HasMaxValInTu#1`
  - **Tax Unit:** `tu_Childunder18_nl`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_eligchtc = 1 & (GetPartnerInfo#1 = 0 | dag > GetPartnerInfo#2 | (dag = GetPartnerInfo#2 & dgn=1))`
  - **Tax Unit:** `tu_Childunder18_nl`

### 5. Function: BenCalc
  - **comp_cond**: `sel_s = 1 & nDepChildrenInTU#2 >=5`
  - **comp_perTU**: `$chall_C4 - $chall_D *max(0,il_taxabley_box1#1+i_taxbase_box3#1- $chall_B2 + (2-nPersInUnit#1)*( $chall_B2  -  $chall_B1 ))+ $chall_C5 *(nDepChildrenInTU#2-4)+nDepChildrenInTU#3* $chall_I1 +nDepChildrenInTU#4* $chall_I2 +(2-nPersInUnit#1)* $chall_S1`
  - **#_level**: `tu_Child16_17_nl`
  - **lowlim**: `0`
  - **output_var**: `bch_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 6. Function: BenCalc
  - **Comp_Cond**: `i_taxbase_box3>$chall_asslim`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bch_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 7. Function: DefConst
  **Constants Defined:**
  - `$chall_B1`: 28406#y
  - `$chall_B2`: 37545#y
  - `$chall_C1`: 2511#y
  - `$chall_C2`: 5022#y
  - `$chall_C3`: 7533#y
  - `$chall_C4`: 10044#y
  - `$chall_C5`: 2511#y
  - `$chall_D`: 7.10%
  - `$chall_I1`: 703#y
  - `$chall_I2`: 936#y
  - `$chall_S1`: 3389#y
  - `$chall_asslim`: 252.759#m


---

## Policy: bsanet_nl
### 1. Function: DefVar
  - **i_taxcredits**: `0`
  - **i_bsa1**: `0`
  - **i_netbsa**: `0`
  - **i_eligbsa**: `0`
  - **var_monetary**: `no`
  - **i_bsa2**: `0`
  - **i_bsa3**: `0`
  - **i_bsa4**: `0`
  - **i_owner**: `0`
  - **i_sben_means**: `0`
  - **i_tinyse1**: `0`
  - **i_bsanorm**: `0`
  - **i_netbsa_r1**: `0`
  - **Var_Monetary**: `no`
  - **n_nstuds**: `0`
  - **n_nstud**: `0`
  - **i_bsanormc**: `0`
  - **n_nstuds_ind**: `0`
  - **i_bsafactor**: `0`
  - **i_taxcreditss**: `n/a`
  - **i_unusedtc**: `0`

### 2. Function: DefIl
  - **name**: `il_meansTClp`
  - **tintc00_s**: `+`
  - **tintcee_s**: `+`
  - **tintclp_s**: `n/a`
  - **tintcpe_s**: `+`
  - **tintcch00_s**: `+`

### 3. Function: DefIl
  - **name**: `il_meansTCother`
  - **il_meansTClp**: `+`
  - **tintcch00_s**: `n/a`
  - **tintclp00_s**: `n/a`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsLoneParentOfDepChild`
  - **Tax Unit:** `tu_Childunder5_nl`

### 5. Function: BenCalc
  - **comp_cond**: `sel_s = 0`
  - **comp_perTU**: `il_meansTCother`
  - **output_var**: `i_taxcredits`
  - **TAX_UNIT**: `tu_individual_nl`

### 6. Function: DefIl
  - **name**: `il_sben_means`
  - **yem**: `+`
  - **yse**: `+`
  - **yot**: `+`
  - **ypp**: `+`
  - **ypr**: `+`
  - **ypt**: `+`
  - **bed**: `+`
  - **bhl**: `+`
  - **bunct_s**: `+`
  - **bunst**: `+`
  - **bsaot**: `+`
  - **kfb**: `+`
  - **pdi**: `+`
  - **psu_s**: `+`
  - **poa00_s**: `+`
  - **poacm**: `+`
  - **tpcpe**: `-`
  - **tsceeui_s**: `-`
  - **tsceepigr_s**: `-`
  - **tingt_s**: `-`
  - **tschl03_s**: `-`
  - **i_taxcredits**: `+`
  - **bcbma01**: `+`
  - **bcbma02**: `+`
  - **bma_s**: `+`
  - **i_unusedtc**: `-`

### 7. Function: ArithOp
  **Formula:** `il_sben_means`
  **Output Variable:** `i_sben_means`
  **Tax Unit:** `tu_couple_nl`

### 8. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(amrtn = 1 | amrtn = 2) & dag>=18 & (idfather =0 & idmother =0)`
  - **Tax Unit:** `tu_individual_nl`

### 9. Function: ArithOp
  **Formula:** `max(i_tinyse,GetPartnerInfo#1)`
  **Output Variable:** `i_tinyse1`
  **Tax Unit:** `tu_individual_nl`

### 10. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dec=0 & dag>=18 & i_tinyse1=0& !(i_owner = 1) & !(bed > 0)`
  - **Tax Unit:** `tu_sben_family_nl`

### 11. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_eligbsa=1 & idpartner>0 & NDepChInTU>0 & afc < $bsa_couple_asset_thres`
  - **Tax Unit:** `tu_sben_family_nl`

### 12. Function: BenCalc
  - **who_must_be_elig**: `one_member`
  - **comp_cond**: `nPersonsInTU#3=1 & ( nPersonsInTU#1=1 | nPersonsInTU#2=1)`
  - **#_AgeMin**: `18`
  - **#_AgeMax**: `20`
  - **comp_perTU**: `$bsa_couple_youth1_amt`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **result_var**: `i_bsa1`
  - **output_var**: `i_bsanorm`
  - **TAX_UNIT**: `tu_sben_family_nl`

### 13. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_eligbsa=1 & idpartner>0   & NDepChInTU=0 & afc < $bsa_couple_noch_asset_thres`
  - **Tax Unit:** `tu_sben_family_nl`

### 14. Function: BenCalc
  - **who_must_be_elig**: `one_member`
  - **comp_cond**: `nPersonsInTU#3=1 & ( nPersonsInTU#1=1 | nPersonsInTU#2=1)`
  - **#_AgeMin**: `18`
  - **#_AgeMax**: `20`
  - **comp_perTU**: `$bsa_couple_noch_youth1_amt`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **result_var**: `i_bsa2`
  - **output_add_var**: `i_bsanorm`
  - **TAX_UNIT**: `tu_sben_family_nl`

### 15. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_eligbsa=1 &  IsLoneParentOfDepChild & NDepChInTU>0 & afc < $bsa_loneparent_asset_thres
`
  - **Tax Unit:** `tu_sben_family_nl`

### 16. Function: BenCalc
  - **who_must_be_elig**: `one_member`
  - **comp_cond**: `nPersonsInTU#3=1`
  - **comp_perTU**: `$bsa_loneparent_youth_amt`
  - **#_AgeMin**: `18`
  - **#_AgeMax**: `20`
  - **#_level**: `tu_household_nl`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **result_var**: `i_bsa3`
  - **output_add_var**: `i_bsanorm`
  - **TAX_UNIT**: `tu_sben_family_nl`

### 17. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_eligbsa=1 & nPersonsInTU=1 & afc < $bsa_single_asset_thres
`
  - **Tax Unit:** `tu_sben_family_nl`

### 18. Function: BenCalc
  - **who_must_be_elig**: `one_member`
  - **comp_cond**: `nPersonsInTU#3=1`
  - **comp_perTU**: `$bsa_single_youth_amt`
  - **#_AgeMin**: `18`
  - **#_AgeMax**: `20`
  - **#_level**: `tu_household_nl`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **result_var**: `i_bsa4`
  - **output_add_var**: `i_bsanorm`
  - **TAX_UNIT**: `tu_sben_family_nl`

### 19. Function: BenCalc
  - **comp_cond**: `il_sben_means <= 0`
  - **comp_perTU**: `i_bsanorm`
  - **output_var**: `i_netbsa`
  - **TAX_UNIT**: `tu_couple_nl`

### 20. Function: Allocate
  - **share**: `i_netbsa`
  - **output_var**: `i_netbsa`
  - **TAX_UNIT**: `tu_couple_nl`

### 21. Function: DefIl
  - **name**: `il_sben_means_r`
  - **yem**: `+`
  - **yse**: `+`
  - **yot**: `+`
  - **ypp**: `+`
  - **ypr**: `+`
  - **ypt**: `+`
  - **bed**: `+`
  - **bhl**: `+`
  - **bunct_s**: `+`
  - **bunst**: `+`
  - **bsaot**: `+`
  - **kfb**: `+`
  - **pdi**: `+`
  - **psu_s**: `+`
  - **poa00_s**: `+`
  - **poacm**: `+`
  - **tpcpe**: `-`
  - **tsceeui_s**: `-`
  - **tschl03_s**: `-`
  - **bcbma01**: `+`
  - **bcbma02**: `+`
  - **bma_s**: `+`

### 22. Function: BenCalc
  - **comp_cond**: `il_sben_means_r <= 0`
  - **comp_perTU**: `i_bsanorm`
  - **output_var**: `i_netbsa_r1`
  - **TAX_UNIT**: `tu_couple_nl`

### 23. Function: Allocate
  - **share**: `i_netbsa_r1`
  - **output_var**: `i_netbsa_r1`
  - **TAX_UNIT**: `tu_couple_nl`

### 24. Function: ArithOp *(Switch: off)*
  **Formula:** `nAdultsInTu#3`
  **Output Variable:** `n_nstuds`
  **Tax Unit:** `tu_household_nl`

### 25. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dec = 0  & !(bed> 0) & dag> 27`
  - **Tax Unit:** `tu_individual_nl`

### 26. Function: ArithOp
  **Formula:** `1`
  **Output Variable:** `n_nstud`
  **Tax Unit:** `tu_individual_nl`

### 27. Function: ArithOp
  **Formula:** `n_nstuds#1`
  **Output Variable:** `n_nstuds_ind`
  **Tax Unit:** `tu_individual_nl`

### 28. Function: BenCalc
  - **Comp_Cond**: `n_nstuds_ind = 8`
  - **Comp_perTU**: `0.7`
  - **TAX_UNIT**: `tu_individual_nl`
  - **Output_Var**: `i_bsafactor`

### 29. Function: BenCalc
  - **Comp_Cond**: `nPersInUnit#1 =1&nDepChInTu > 0 &nPersInUnit#2 = 0`
  - **Comp_perTU**: `i_bsanorm`
  - **Output_Var**: `i_bsanormc`
  - **TAX_UNIT**: `tu_sben_family_nl`
  - **#_AgeMin**: `21`
  - **#_AgeMax**: `20`

### 30. Function: ArithOp
  **Formula:** `i_bsanormc`
  **Output Variable:** `i_bsanorm`
  **Tax Unit:** `tu_sben_family_nl`

### 31. Function: BenCalc
  - **Comp_Cond**: `n_nstud =1`
  - **Comp_perElig**: `1`
  - **Output_Var**: `n_nstuds`
  - **TAX_UNIT**: `tu_household_nl`

### 32. Function: ArithOp *(Switch: off)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 33. Function: ArithOp *(Switch: off)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 34. Function: ArithOp
  **Formula:** `max(i_taxcredits-tsceepigr_s - tingt_s, 0)`
  **Output Variable:** `i_unusedtc`
  **Tax Unit:** `tu_individual_nl`

### 35. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `(i_bsa00_cumpers > $bsa00_target_count & bsa00yn_a = -1)  | bsa00yn_a = 0`
  - **Comp_perTU**: `0`
  - **Output_Var**: `i_netbsa`
  - **TAX_UNIT**: `tu_individual_nl`

### 36. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsa00_elig`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsa00_sort`
  - **OutputVar**: `i_bsa00_cumpers`
  - **TAX_UNIT**: `tu_individual_nl`

### 37. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa00_target_count`: $sum_i_bsa00_elig * $bsa00_rate

### 38. Function: Totals *(Switch: off)*
  - **Agg**: `i_bsa00_elig`
  - **Use_Weights**: `yes`
  - **Varname_Sum**: `$sum`
  - **TAX_UNIT**: `tu_individual_nl`

### 39. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa00_rate`: min($bsa00_BCA_rate,$bsa00_BTA_rate)

### 40. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa00_BCA_rate`: 0.741143

### 41. Function: Totals *(Switch: off)*
  - **Agg**: `n/a`
  - **Use_Weights**: `n/a`
  - **Varname_Sum**: `n/a`
  - **TAX_UNIT**: `n/a`

### 42. Function: DefVar *(Switch: off)*
  - **i_bsa00_bca_take**: `n/a`

### 43. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `n/a`
  - **SummingWeighted**: `n/a`
  - **SortingVar**: `n/a`
  - **OutputVar**: `n/a`
  - **TAX_UNIT**: `n/a`

### 44. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa00_targetBCA_count`: n/a

### 45. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_netbsa>=
$bsa00_minamt`
  - **Comp_perTU**: `1`
  - **Comp_perElig**: `i_bsa00_sort`
  - **Output_Var**: `i_bsa00_sort`
  - **TAX_UNIT**: `tu_individual_nl`

### 46. Function: DefVar *(Switch: off)*
  - **i_bsa00_sort**: `i_bsa00_rand`
  - **i_bsa00_amt**: `i_netbsa`
  - **i_bsa00_elig**: `i_netbsa
 > 0`
  - **i_bsa00_cumexp**: `0`
  - **i_bsa00_cumpers**: `0`

### 47. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa00_minamt`: 0

### 48. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `i_netbsa>0`
  - **Comp_perTU**: `i_netbsa_r1`
  - **Output_Var**: `i_netbsa_r1`
  - **TAX_UNIT**: `tu_individual_nl`

### 49. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa00_BTA_rate`: 65%

### 50. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa00_BTA_rate`: 1

### 51. Function: DefConst
  **Constants Defined:**
  - `$bsa_couple_asset_thres`: 15540#c
  - `$bsa_couple_nonret_amt`: 1922.07#m
  - `$bsa_couple_ret_amt`: 2053.48#m
  - `$bsa_couple_youth_amt`: 1048.75#m
  - `$bsa_couple_youth1_amt`: 1672.66#m
  - `$bsa_couple_noch_asset_thres`: 15540#c
  - `$bsa_couple_noch_nonret_amt`: 1922.07#m
  - `$bsa_couple_noch_ret_amt`: 2053.48#m
  - `$bsa_couple_noch_youth_amt`: 664.34#m
  - `$bsa_couple_noch_youth1_amt`: 1293. 21#m
  - `$bsa_loneparent_asset_thres`: 15540#c
  - `$bsa_loneparent_nonret_amt`: 1345. 45#m
  - `$bsa_loneparent_ret_amt`: 1501.07#m
  - `$bsa_loneparent_youth_amt`: 332.17#m
  - `$bsa_single_asset_thres`: 7770#c
  - `$bsa_single_nonret_amt`: 961.04#m
  - `$bsa_single_lone_nonret_amt`: 1345. 45#m
  - `$bsa_single_ret_amt`: 1501.07#m
  - `$bsa_single_youth_amt`: 332.17#m
  - `$bsa_loneparent_lone_nonret_amt`: 1345. 45#m
  - `$bsa_norm_amt_1`: 332.17#m
  - `$bsa_norm_amt_2`: 384.41#m


---

## Policy: bsagross_nl
### 1. Function: DefVar
  - **i_rf**: `0`
  - **i_rfmax**: `0`
  - **i_bsadiff**: `0`
  - **i_taxpos**: `0`
  - **i_netbsa2**: `0`
  - **i_netbsa3**: `0`
  - **i_unusedtcr**: `0`
  - **i_rfn**: `0`
  - **i_bsa01_s**: `0`
  - **i_number**: `0`

### 2. Function: BenCalc
  - **comp_cond**: `dag>=$PenAge`
  - **comp_perTU**: `max((i_netbsa-i_unusedtc)*$bsag_fact_old, i_netbsa)`
  - **output_var**: `bsa00_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 3. Function: BenCalc
  - **comp_cond**: `dag>=$PenAge`
  - **comp_perTU**: `tsceepigr_s`
  - **output_var**: `tsceepigr_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 4. Function: BenCalc
  - **comp_cond**: `dag>=$PenAge`
  - **comp_perTU**: `tschl_s+bsa00_s*$tschl_rate_se`
  - **output_var**: `tschl_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 5. Function: BenCalc
  - **comp_cond**: `dag>=$PenAge`
  - **comp_perTU**: `tingt_s`
  - **output_var**: `tingt_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 6. Function: ArithOp
  **Formula:** `tsceepigr_s + tingt_s + tinkt_s`
  **Output Variable:** `i_GrossTotalTax`
  **Tax Unit:** `tu_individual_nl`

### 7. Function: ArithOp
  **Formula:** `i_GrossTotalTax - il_tintc_total`
  **Output Variable:** `i_NetTotalTax`
  **Tax Unit:** `tu_individual_nl`

### 8. Function: ArithOp
  **Formula:** `il_tintc_total`
  **Output Variable:** `tintc_s`
  **Tax Unit:** `tu_individual_nl`

### 9. Function: ArithOp
  **Formula:** `i_GrossTotalTax - (il_tintc_total - il_tintc_refund)`
  **Output Variable:** `i_NetTotalTaxNonRef`
  **Tax Unit:** `tu_individual_nl`

### 10. Function: ArithOp
  **Formula:** `il_tintc_refund - i_NetTotalTaxNonRef`
  **Output Variable:** `i_rf`
  **Tax Unit:** `tu_individual_nl`

### 11. Function: BenCalc
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_level**: `n/a`
  - **output_var**: `tinrf_s`
  - **TAX_UNIT**: `tu_individual_nl`
  - **#_Income**: `n/a`
  - **LowLim**: `n/a`

### 12. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **#_income**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 13. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 14. Function: ArithOp
  **Formula:** `($peoplesic_aow_rate+$peoplesic_anw_rate+$peoplesic_awbz_rate)*i_bsadiff`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_nl`

### 15. Function: ArithOp
  **Formula:** `i_bsadiff*$tin_br1`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_nl`

### 16. Function: ArithOp
  **Formula:** `i_bsadiff*$tschl_rate_emp`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_nl`

### 17. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `i_bsadiff > 0 & i_rf > 0 & (tingt_s + tsceepigr_s) > (tintc_s + tinrf_s)`
  - **comp_perTU**: `tingt_s + tsceepigr_s  -tintc_s`
  - **output_add_var**: `tintc_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 18. Function: BenCalc
  - **comp_cond**: `dag>=$PenAge`
  - **comp_perElig**: `($peoplesic_anw_rate+$peoplesic_awbz_rate)/($tin_br1+$peoplesic_anw_rate+$peoplesic_awbz_rate)`
  - **output_var**: `i_ratioPC`
  - **TAX_UNIT**: `tu_individual_nl`

### 19. Function: Elig
  **Eligibility Check:**
  - **Condition:** `tinrf_s = 0`
  - **Tax Unit:** `tu_individual_nl`

### 20. Function: ArithOp
  **Formula:** `tintc_s * i_ratioPC - tsceepigr_s`
  **Output Variable:** `i_unusedTaxCredit`
  **Tax Unit:** `tu_individual_nl`

### 21. Function: ArithOp
  **Formula:** `tsceepigr_s - tintc_s * i_ratioPC`
  **Output Variable:** `tsceepi_s`
  **Tax Unit:** `tu_individual_nl`

### 22. Function: Elig
  **Eligibility Check:**
  - **Condition:** `tinrf_s > 0`
  - **Tax Unit:** `tu_individual_nl`

### 23. Function: ArithOp
  **Formula:** `min(tinrf_s*i_ratioPC,GetPartnerIncome#1)*(-1)`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_nl`

### 24. Function: ArithOp
  **Formula:** `max(tinrf_s*i_ratioPC-GetPartnerIncome#1,0)`
  **Output Variable:** `i_unusedTaxRefund`
  **Tax Unit:** `tu_individual_nl`

### 25. Function: ArithOp
  **Formula:** `tingt_s + tinkt_s - tintc_s * (1 - i_ratioPC) - i_unusedTaxCredit`
  **Output Variable:** `tin_s`
  **Tax Unit:** `tu_individual_nl`

### 26. Function: Elig
  **Eligibility Check:**
  - **Condition:** `tinrf_s > 0`
  - **Tax Unit:** `tu_individual_nl`

### 27. Function: ArithOp
  **Formula:** `(tinrf_s * (1 - i_ratioPC) + i_unusedTaxRefund) * (-1)`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_nl`

### 28. Function: DefVar
  - **i_rev**: `0`
  - **var_monetary**: `yes`
  - **i_diff**: `0`
  - **i_sben_means_r**: `0`
  - **i_netbsa_r**: `0`
  - **i_bsa00_s**: `0`

### 29. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bsa00_s > 0`
  - **Tax Unit:** `tu_sben_family_nl`

### 30. Function: ArithOp
  **Formula:** `i_NetTotalTax`
  **Output Variable:** `i_rev`
  **Tax Unit:** `tu_couple_nl`

### 31. Function: Allocate
  - **share**: `i_rev`
  - **output_var**: `i_rev`
  - **TAX_UNIT**: `tu_couple_nl`

### 32. Function: ArithOp
  **Formula:** `il_sben_means_r`
  **Output Variable:** `i_sben_means_r`
  **Tax Unit:** `tu_couple_nl`

### 33. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bsa00_s > 0 & i_rev > -0.1 & i_rev < 0.1`
  - **Tax Unit:** `tu_individual_nl`

### 34. Function: ArithOp
  **Formula:** `i_bsanorm - il_sben_means_r`
  **Output Variable:** `i_diff`
  **Tax Unit:** `tu_individual_nl`

### 35. Function: Allocate
  - **share**: `i_diff`
  - **output_var**: `i_diff`
  - **TAX_UNIT**: `tu_couple_nl`

### 36. Function: Elig
  **Eligibility Check:**
  - **Condition:** `bsa00_s > 0 & i_rev < 0.1& i_rev > -0.1`
  - **Tax Unit:** `tu_individual_nl`

### 37. Function: ArithOp
  **Formula:** `i_diff`
  **Output Variable:** `i_netbsa_r`
  **Tax Unit:** `tu_sben_family_nl`

### 38. Function: Allocate
  - **share**: `i_netbsa_r`
  - **output_var**: `i_netbsa_r`
  - **TAX_UNIT**: `tu_couple_nl`

### 39. Function: ArithOp
  **Formula:** `bsa00_s`
  **Output Variable:** `i_bsa00_s`
  **Tax Unit:** `tu_individual_nl`

### 40. Function: BenCalc
  - **comp_cond**: `i_netbsa_r = 0&i_netbsa_r1 > 0&i_bsa00_s = 0`
  - **comp_perTU**: `i_netbsa_r1`
  - **output_var**: `bsa00_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 41. Function: BenCalc
  - **comp_cond**: `dag>=$PenAge|bsa00_s = i_bsa00_s`
  - **comp_perTU**: `tsceepigr_s`
  - **output_var**: `tsceepigr_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 42. Function: BenCalc
  - **comp_cond**: `dag>=$PenAge|bsa00_s = i_bsa00_s`
  - **comp_perTU**: `tschl_s`
  - **output_var**: `tschl_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 43. Function: BenCalc
  - **comp_cond**: `dag>=$PenAge|bsa00_s = i_bsa00_s`
  - **comp_perTU**: `tingt_s`
  - **output_var**: `tingt_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 44. Function: ArithOp
  **Formula:** `tsceepigr_s + tingt_s + tinkt_s`
  **Output Variable:** `i_GrossTotalTax`
  **Tax Unit:** `tu_individual_nl`

### 45. Function: ArithOp
  **Formula:** `tschl_s - tschlfx_s - tschl02_s - tschl03_s`
  **Output Variable:** `tschl01_s`
  **Tax Unit:** `tu_individual_nl`

### 46. Function: Elig
  **Eligibility Check:**
  - **Condition:** `tinrf_s = 0`
  - **Tax Unit:** `tu_individual_nl`

### 47. Function: ArithOp
  **Formula:** `bsa00_s`
  **Output Variable:** `i_bsa01_s`
  **Tax Unit:** `tu_individual_nl`

### 48. Function: BenCalc
  - **Comp_Cond**: `i_unusedtc > GetPartnerIncome#1`
  - **Comp_perTU**: `i_unusedtc`
  - **#_Income**: `i_unusedtc`
  - **Output_Var**: `i_unusedtcr`
  - **TAX_UNIT**: `tu_individual_nl`

### 49. Function: BenCalc
  - **Comp_Cond**: `(i_rf > 0 & dag > 62)|(GetPartnerInfo#1 > 62 & GetPartnerIncome#2 > 0)`
  - **Comp_perTU**: `max(i_number*(i_bsanorm-i_sben_means-i_unusedtcr),0)`
  - **Output_Var**: `i_netbsa2`
  - **#_Info**: `dag`
  - **#_Income**: `i_rf`
  - **TAX_UNIT**: `tu_couple_nl`

### 50. Function: Allocate
  - **Share**: `i_netbsa2`
  - **Output_Var**: `i_netbsa3`
  - **TAX_UNIT**: `tu_couple_nl`

### 51. Function: BenCalc
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **#_Income**: `i_sben_means`
  - **Output_Var**: `i_rfn`
  - **TAX_UNIT**: `tu_individual_nl`

### 52. Function: BenCalc
  - **Comp_Cond**: `(tinrf_ s > 0 & dag < 63)|(GetPartnerInfo#1 < 63 & GetPartnerIncome#2 > 0)`
  - **Comp_perTU**: `max((i_bsanorm-i_sben_means-tinrf_s),0)`
  - **#_Info**: `dag`
  - **#_Income**: `tinrf_s`
  - **Output_Add_Var**: `i_netbsa2`
  - **TAX_UNIT**: `tu_couple_nl`

### 53. Function: Allocate
  - **Share**: `i_netbsa2`
  - **Output_Var**: `i_netbsa3`
  - **TAX_UNIT**: `tu_couple_nl`

### 54. Function: BenCalc
  - **Comp_Cond**: `tinrf_s = 0 & GetPartnerIncome#1 = 0`
  - **Comp_perTU**: `bsa00_s`
  - **#_Income**: `tinrf_s`
  - **Output_Var**: `bsa00_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 55. Function: ArithOp
  **Formula:** `bsa00_s - i_bsa01_s`
  **Output Variable:** `i_bsadiff`
  **Tax Unit:** `tu_individual_nl`

### 56. Function: ArithOp
  **Formula:** `tsceepigr_s + tingt_s + tinkt_s`
  **Output Variable:** `i_GrossTotalTax`
  **Tax Unit:** `tu_individual_nl`

### 57. Function: ArithOp
  **Formula:** `i_GrossTotalTax - il_tintc_total`
  **Output Variable:** `i_NetTotalTax`
  **Tax Unit:** `tu_individual_nl`

### 58. Function: BenCalc
  - **Comp_Cond**: `tsceepi_s + tin_s + GetPartnerIncome#1 + GetPartnerIncome#2 >= -0.01 | tsceepi_s  + tin_s > =0`
  - **#_Income**: `tin_s`
  - **Comp_perTU**: `tin_s`
  - **Output_Var**: `tin_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 59. Function: BenCalc
  - **Comp_Cond**: `tsceepi_s + tin_s + GetPartnerIncome#1 + GetPartnerIncome#2 >= -0.01 | tsceepi_s  + tin_s > =0`
  - **#_Income**: `tin_s`
  - **Comp_perTU**: `tsceepi_s`
  - **Output_Var**: `tsceepi_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 60. Function: Elig
  **Eligibility Check:**
  - **Condition:** `dag < 63 & i_NetTotalTax < 0`
  - **Tax Unit:** `tu_individual_nl`

### 61. Function: ArithOp
  **Formula:** `1`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_nl`

### 62. Function: Allocate
  - **Share**: `i_rev`
  - **Output_Var**: `i_rev`
  - **TAX_UNIT**: `tu_couple_nl`

### 63. Function: DefConst
  **Constants Defined:**
  - `$bsag_fact`: 1.558118
  - `$bsag_fact_old`: 1.05552

### 64. Function: ArithOp
  **Formula:** `1/(1 - 0.5*($tin_br1+$peoplesic_aow_rate+$peoplesic_anw_rate+$peoplesic_awbz_rate))`
  **Output Variable:** `i_number`
  **Tax Unit:** `tu_couple_nl`


---

## Policy: bhlmt_nl
### 1. Function: DefVar
  - **i_nprm**: `0`

### 2. Function: DefIl
  - **name**: `il_taxabley1`
  - **il_taxabley_box1**: `+`
  - **i_taxbase_box3**: `+`
  - **bsa00_s**: `+`
  - **bsase00_s**: `n/a`

### 3. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 4. Function: DefIl
  - **name**: `il_taxabley2`
  - **il_taxabley1**: `+`
  - **sin44_s**: `n/a`

### 5. Function: DefIl
  - **name**: `il_taxabley`
  - **il_taxabley2**: `+`

### 6. Function: DefConst
  **Constants Defined:**
  - `$bhlmt_A_rt`: .1370
  - `$bhlmt_B_amt`: 28406#y
  - `$bhlmt_C_amt`: 1213.79#y
  - `$bhlmt_D_amt`: 538.57#y
  - `$bhlmt_E_amt`: 4224#y
  - `$bhlmt_F_amt`: 2112#y
  - `$bhlmt_inclim_single`: 39719#y
  - `$bhlmt_inclim_couple`: 50206#y
  - `$bhlmt_assetlim_single`: 141896#y
  - `$bhlmt_assetlim_couple`: 179429#y
  - `$bhlmt_asslim_m`: 252.76#m

### 7. Function: BenCalc
  - **comp_cond**: `!IsDepChild#1 & dag < $PenAge`
  - **comp_perElig**: `il_taxabley2`
  - **#_level**: `tu_Childunder18_nl`
  - **output_var**: `sin20_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 8. Function: BenCalc
  - **comp_cond**: `dag>=18 & IsHead & IsWithPartner & sin20_s < $bhlmt_inclim_couple`
  - **comp_perTU**: `$bhlmt_A_rt*max(0,sin20_s-$bhlmt_B_amt)+$bhlmt_C_amt`
  - **output_var**: `i_nprm`
  - **TAX_UNIT**: `tu_Childunder18_nl`

### 9. Function: BenCalc
  - **comp_cond**: `dag>=18 & IsHead & IsWithPartner & sin20_s < $bhlmt_inclim_couple`
  - **comp_perTU**: `$bhlmt_E_amt-i_nprm`
  - **comp_lowlim**: `0`
  - **output_var**: `bhlmt_s`
  - **TAX_UNIT**: `tu_Childunder18_nl`

### 10. Function: BenCalc
  - **comp_cond**: `i_taxbase_box3>$bhlmt_asslim_m`
  - **comp_perTU**: `0`
  - **comp_lowlim**: `0`
  - **output_var**: `bhlmt_s`
  - **TAX_UNIT**: `tu_Childunder18_nl`


---

## Policy: ersic_NL
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `yem>0 & dag<$PenAge`
  - **Tax Unit:** `tu_individual_nl`

### 2. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_nl`
  - **Output Variable:** `tscerui_s`

### 3. Function: SchedCalc
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_nl`
  - **Output Variable:** `tscerdi_s`

### 4. Function: ArithOp
  **Formula:** `tscerui_s + tscerdi_s`
  **Output Variable:** `tscer_s`
  **Tax Unit:** `tu_individual_nl`

### 5. Function: DefConst
  **Constants Defined:**
  - `$ersic_disab_r`: 7.545%
  - `$ersic_unemp_r`: 3.29%
  - `$ersic_uplim`: 6322#m


---

## Policy: bho_nl
### 1. Function: DefVar
  - **i_normrentA**: `0`
  - **i_normrentC**: `0`
  - **i_normrentE**: `0`
  - **i_normrentG**: `0`
  - **i_eligbho**: `0`
  - **var_monetary**: `no`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `xhcrt < $hbo_maxrent  & tinkt_s = 0`
  - **Tax Unit:** `tu_household_nl`

### 3. Function: DefConst
  **Constants Defined:**
  - `$bho_aA_rt`: 0.000000438698
  - `$bho_bA_rt`: 0.000446392665
  - `$bho_cA_amt`: -37.14#m
  - `$bho_incomeA_amt`: 22700#y
  - `$hbo_quallim`: 477.20#m
  - `$hbo_maxrent`: 900.07#m
  - `$hbo_uplim_1`: 682.96#m
  - `$hbo_uplim_3`: 731.92#m
  - `$hbo_minnormA`: 236.19#m
  - `$hbo_minbasA`: 199.05#m

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_eligbho = 1 & nPersInUnit = 1 & $hbo_minbasA < xhcrt`
  - **Tax Unit:** `tu_household_nl`

### 5. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** `n/a`

### 6. Function: ArithOp
  **Formula:** `$bho_aA_rt*(il_taxabley*12)^2 + $bho_bA_rt*il_taxabley*12 + $bho_cA_amt`
  **Output Variable:** `i_normrentA`
  **Tax Unit:** `tu_household_nl`

### 7. Function: BenCalc
  - **who_must_be_elig**: `one_member`
  - **comp_cond**: `i_normrentA<xhcrt & xhcrt>$hbo_uplim_1`
  - **#_amount**: `n/a`
  - **comp_perTU**: `0.4*(xhcrt-max($hbo_uplim_1,i_normrentA))+0.65*max(0,$hbo_uplim_1-max(i_normrentA,$hbo_quallim))+max(0,$hbo_quallim-i_normrentA)`
  - **output_var**: `bho_s`
  - **TAX_UNIT**: `tu_household_nl`

### 8. Function: DefConst
  **Constants Defined:**
  - `$bho_aC_rt`: 0.000000298184
  - `$bho_bC_rt`: -0.001382497146
  - `$bho_cC_amt`: -37.14#m
  - `$bho_incomeC_amt`: 30450#y
  - `$hbo_minnormC`: 234.38#m
  - `$hbo_minbasC`: 197.24#m

### 9. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_eligbho = 1 & IsHead & nPersInUnit > 1 & $hbo_minbasC < xhcrt`
  - **Tax Unit:** `tu_household_nl`

### 10. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** `n/a`

### 11. Function: ArithOp
  **Formula:** `$bho_aC_rt*(il_taxabley*12)^2 + $bho_bC_rt*il_taxabley*12 + $bho_cC_amt`
  **Output Variable:** `i_normrentC`
  **Tax Unit:** `tu_household_nl`

### 12. Function: BenCalc
  - **who_must_be_elig**: `one_member`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_amount**: `n/a`
  - **#_AgeMin**: `n/a`
  - **output_add_var**: `bho_s`
  - **TAX_UNIT**: `tu_household_nl`

### 13. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$bho_aE_rt`: n/a
  - `$bho_bE_rt`: n/a
  - `$bho_cE_amt`: n/a
  - `$bho_incomeE_amt`: n/a

### 14. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 15. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** `n/a`

### 16. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 17. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **#_amount**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 18. Function: DefConst *(Switch: n/a)*
  **Constants Defined:**
  - `$bho_aG_rt`: n/a
  - `$bho_bG_rt`: n/a
  - `$bho_cG_amt`: n/a
  - `$bho_incomeG_amt`: n/a

### 19. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 20. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** `n/a`

### 21. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 22. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_amount**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: output_std_nl
### 1. Function: DefOutput
  - **file**: `NL_2025_std`
  - **VarGroup**: `x*`
  - **defil**: `ils_dispy`
  - **ILGroup**: `il*`
  - **nDecimals**: `2`
  - **TAX_UNIT**: `tu_individual_nl`
  - **unitinfo_tu**: `tu_couple_nl`
  - **unitinfo_id**: `IsPartner`


---

## Policy: output_std_hh_nl *(Switch: off)*
### 1. Function: DefOutput
  - **file**: `NL_2025_std_hh`
  - **var**: `dwt`
  - **TAX_UNIT**: `tu_hh_oecd_co`
  - **ILGroup**: `ils*`


---

## Policy: setdefault_nl
### 1. Function: SetDefault
  - **Dataset**: `nl_20*`
  - **yempv_a**: `0`
  - **liwmy_a**: `0`
  - **lnu**: `0`
  - **lhw_a**: `0`
  - **yem_a**: `0`
  - **dmb**: `6`
  - **lcb_a**: `0`
  - **yemmy20_a**: `0`
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
  - **amriv**: `0`

### 2. Function: SetDefault
  - **Dataset**: `*`
  - **bma_s**: `0`
  - **bwkmceemy_s**: `0`
  - **lhwsr_s**: `0`

### 3. Function: SetDefault
  - **Dataset**: `nl_20??_??_*`
  - **xed00**: `0`
  - **xhl00**: `0`

### 4. Function: SetDefault
  - **Dataset**: `nl_20??_??_*`
  - **ydsyc_a**: `0`

### 5. Function: SetDefault
  - **Dataset**: `*`
  - **bsa00yn_a**: `-1`

### 6. Function: DefIl
  - **Run_Cond**: `IsUsedDatabase#1`
  - **#_DataBasename**: `nl_20??_??_????_??_??`
  - **Name**: `il_xs_hl06`
  - **Warn_If_NonMonetary**: `no`
  - **RegExp_Def**: `xs06[0-9]+`
  - **RegExp_Factor**: `+`

### 7. Function: ArithOp
  **Formula:** `il_xs_hl06 * yds`
  **Output Variable:** `xhl00`
  **Tax Unit:** `tu_individual_nl`
  **Run Condition:** `IsUsedDatabase#1`

### 8. Function: DefIl
  - **Run_Cond**: `IsUsedDatabase#1`
  - **#_DataBasename**: `nl_20??_??_????_??_??`
  - **Name**: `il_xs_hl10`
  - **Warn_If_NonMonetary**: `no`
  - **RegExp_Def**: `xs10[0-9]+`
  - **RegExp_Factor**: `+`

### 9. Function: ArithOp
  **Formula:** `il_xs_hl10 * yds`
  **Output Variable:** `xed00`
  **Tax Unit:** `tu_individual_nl`
  **Run Condition:** `IsUsedDatabase#1`


---

## Policy: ilsdef_nl
### 1. Function: DefIl
  - **name**: `ils_origy`
  - **yem**: `+`
  - **yse**: `+`
  - **yiy**: `+`
  - **ypp**: `+`
  - **ypr**: `+`
  - **ypt**: `+`
  - **yot**: `+`
  - **poacm**: `+`
  - **xmp**: `-`

### 2. Function: DefIl
  - **name**: `ils_earns`
  - **yem**: `+`
  - **yse**: `+`

### 3. Function: DefIl
  - **name**: `ils_origrepy`
  - **ils_origy**: `+`
  - **bunct_s**: `+`
  - **bunst**: `+`
  - **poa00_s**: `+`
  - **psu_s**: `+`
  - **pdi**: `+`
  - **bhl**: `+`
  - **bcbma01**: `+`
  - **bcbma02**: `+`
  - **bma_s**: `+`

### 4. Function: DefIl
  - **name**: `ils_pen`
  - **poa00_s**: `+`

### 5. Function: DefIl
  - **name**: `ils_benmt`
  - **bhlmt_s**: `+`
  - **bho_s**: `+`
  - **bsa00_s**: `+`
  - **bed**: `+`
  - **bched**: `+`
  - **bsaot**: `+`
  - **psu_s**: `+`
  - **bch_s**: `+`
  - **bsase00_s**: `n/a`

### 6. Function: DefIl
  - **name**: `ils_bennt`
  - **bfa_s**: `+`
  - **bunct_s**: `+`
  - **bunst**: `+`
  - **pdi**: `+`
  - **bhl**: `+`
  - **bcbma01**: `+`
  - **bcbma02**: `+`
  - **bma_s**: `+`

### 7. Function: DefIl
  - **name**: `ils_ben`
  - **ils_pen**: `+`
  - **ils_benmt**: `+`
  - **ils_bennt**: `+`

### 8. Function: DefIl
  - **name**: `ils_bensim`
  - **bfa_s**: `+`
  - **psu_s**: `+`
  - **bhlmt_s**: `+`
  - **bho_s**: `+`
  - **bsa00_s**: `+`
  - **bch_s**: `+`
  - **bunct_s**: `+`
  - **bma_s**: `+`
  - **bsase00_s**: `n/a`

### 9. Function: DefIl
  - **name**: `ils_taxsim`
  - **tin_s**: `+`

### 10. Function: DefIl
  - **name**: `ils_tax`
  - **ils_taxin**: `+`
  - **ils_taxwl**: `+`

### 11. Function: DefIl
  - **name**: `ils_sicer`
  - **tscerui_s**: `+`
  - **tscerdi_s**: `+`
  - **tschl00_s**: `+`

### 12. Function: DefIl
  - **name**: `ils_sicct`
  - **tschl01_s**: `+`
  - **tschl00_s**: `-`

### 13. Function: DefIl
  - **name**: `ils_sicee`
  - **tpcpe**: `+`
  - **tsceeui_s**: `+`
  - **tsceepi_s**: `+`

### 14. Function: DefIl
  - **name**: `ils_sicse`

### 15. Function: DefIl
  - **name**: `ils_dispy`
  - **ils_origy**: `+`
  - **ils_ben**: `+`
  - **ils_sicdy**: `-`
  - **ils_tax**: `-`

### 16. Function: DefIl
  - **Name**: `ils_sicot`
  - **tschl03_s**: `+`
  - **tschl02_s**: `+`
  - **tschlfx_s**: `+`

### 17. Function: DefIl
  - **Name**: `ils_sicdy`
  - **ils_sicse**: `+`
  - **ils_sicot**: `+`
  - **ils_sicee**: `+`

### 18. Function: DefIl
  - **Name**: `ils_base_tingt`
  - **bsa00_s**: `+`
  - **kivho**: `n/a`
  - **bsaot**: `+`
  - **bhl**: `+`
  - **pdi**: `+`
  - **kfb**: `+`
  - **psu_s**: `+`
  - **poacm**: `+`
  - **poa00_s**: `+`
  - **bunst**: `+`
  - **bunct_s**: `+`
  - **yot**: `+`
  - **ypp**: `+`
  - **yptmptx**: `+`
  - **yse**: `+`
  - **bcbma02**: `+`
  - **bcbma01**: `+`
  - **yem**: `+`
  - **bma_s**: `+`
  - **bsase00_s**: `n/a`
  - **kivhooo_s**: `+`

### 19. Function: DefIl
  - **Name**: `ils_base_tinkt`
  - **afc**: `+`

### 20. Function: DefIl
  - **Name**: `ils_b2_bsaho`
  - **ils_b1_bsa**: `+`
  - **ils_b1_bho**: `+`

### 21. Function: DefIl
  - **Name**: `ils_b2_penhl`
  - **ils_b1_boa**: `+`
  - **ils_b1_bsu**: `+`
  - **ils_b1_bhl**: `+`
  - **ils_b1_bdi**: `+`

### 22. Function: DefIl
  - **Name**: `ils_b2_bfaed`
  - **ils_b1_bfa**: `+`
  - **ils_b1_bed**: `+`

### 23. Function: DefIl
  - **Name**: `ils_b1_bcb`
  - **bcbma01**: `+`
  - **bcbma02**: `+`
  - **bma_s**: `+`

### 24. Function: DefIl
  - **Name**: `ils_b1_bsa`
  - **bsaot**: `+`
  - **bsa00_s**: `+`
  - **bsase00_s**: `n/a`

### 25. Function: DefIl
  - **Name**: `ils_b1_bho`
  - **bho_s**: `+`

### 26. Function: DefIl
  - **Name**: `ils_b1_bhl`
  - **bhl**: `+`
  - **bhlmt_s**: `+`

### 27. Function: DefIl
  - **Name**: `ils_b1_bun`
  - **bunst**: `+`
  - **bunct_s**: `+`

### 28. Function: DefIl
  - **Name**: `ils_b1_bdi`
  - **pdi**: `+`

### 29. Function: DefIl
  - **Name**: `ils_b1_bsu`
  - **psu_s**: `+`

### 30. Function: DefIl
  - **Name**: `ils_b1_boa`
  - **poa00_s**: `+`

### 31. Function: DefIl
  - **Name**: `ils_b1_bed`
  - **bched**: `+`
  - **bed**: `+`

### 32. Function: DefIl
  - **Name**: `ils_b1_bfa`
  - **bch_s**: `+`
  - **bfa_s**: `+`
  - **ils_b1_bcb**: `+`

### 33. Function: DefIl
  - **Name**: `ils_b1_bwk`

### 34. Function: DefIl
  - **Name**: `ils_b2_bunwk`
  - **ils_b1_bwk**: `+`
  - **ils_b1_bun**: `+`

### 35. Function: DefIl
  - **Name**: `ils_taxin`
  - **tin_s**: `+`

### 36. Function: DefIl
  - **Name**: `ils_taxwl`
  - **tpr**: `+`


---

## Policy: ilsudbdef_nl
### 1. Function: DefIl
  - **Name**: `ils_udb_yem`
  - **yem**: `+`
  - **bcbma01**: `+`
  - **bcbma02**: `+`

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
  - **Name**: `ils_udb_boa`
  - **poa00_s**: `+`
  - **poacm**: `+`

### 11. Function: DefIl
  - **Name**: `ils_udb_bsu`
  - **psu_s**: `+`

### 12. Function: DefIl
  - **Name**: `ils_udb_bdi`
  - **pdi**: `+`

### 13. Function: DefIl
  - **Name**: `ils_udb_bun`
  - **bunst**: `+`
  - **bunct_s**: `+`

### 14. Function: DefIl
  - **Name**: `ils_udb_bhl`
  - **bhl**: `+`
  - **bhlmt_s**: `+`

### 15. Function: DefIl
  - **Name**: `ils_udb_bed`
  - **bched**: `+`
  - **bed**: `+`

### 16. Function: DefIl
  - **Name**: `ils_udb_bsa`
  - **bsaot**: `+`
  - **bsa00_s**: `+`
  - **bsase00_s**: `n/a`

### 17. Function: DefIl
  - **Name**: `ils_udb_bfa`
  - **bch_s**: `+`
  - **bfa_s**: `+`
  - **bma_s**: `+`

### 18. Function: DefIl
  - **Name**: `ils_udb_bho`
  - **bho_s**: `+`

### 19. Function: DefIl
  - **Name**: `ils_udb_tpr`
  - **tpr**: `+`

### 20. Function: DefIl
  - **Name**: `ils_udb_tis`
  - **tin_s**: `+`
  - **tschl03_s**: `+`
  - **tpcpe**: `+`
  - **tschl02_s**: `+`
  - **tschlfx_s**: `+`
  - **tsceepi_s**: `+`
  - **tsceeui_s**: `+`

### 21. Function: DefIl
  - **Name**: `ils_udb_yds`
  - **ils_udb_yem**: `+`
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


---

## Policy: bma_nl *(Switch: off)*
### 1. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bma=1 & ( yem > 0 | yse>0 | bun>0 | bunct_s>0 |  pdi>0 | liwmy>0)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_elparent_bma`
  - **TAX_UNIT**: `tu_individual_nl`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsHeadOfTu#1 & IsParentOfDepChild#1`
  - **Tax Unit:** `tu_individual_nl`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsDepChild#1`
  - **Tax Unit:** `tu_individual_nl`

### 4. Function: BenCalc
  - **Comp_Cond**: `i_elchild_bma=1`
  - **Comp_perTU**: `(12-dmb)*(30.5/7)`
  - **Output_Var**: `i_ageweeks_bma`
  - **TAX_UNIT**: `tu_individual_nl`

### 5. Function: BenCalc
  - **Comp_Cond**: `i_elchild_bma=1 & i_ageweeks_bma>=0 & i_nelchildren_bma#1>1`
  - **Comp_perTU**: `20`
  - **Output_Var**: `i_durweeks_bma`
  - **TAX_UNIT**: `tu_individual_nl`
  - **Comp_UpLim**: `4+i_ageweeks_bma`
  - **Comp_LowLim**: `0`
  - **#_Level**: `tu_bma_nl`

### 6. Function: DefVar
  - **i_elparent_bma**: `0`
  - **Var_Monetary**: `no`
  - **i_elchild_bma**: `0`
  - **i_ageweeks_bma**: `0`
  - **i_nelchildren_bma**: `0`
  - **i_durweeks_bma**: `0`
  - **i_yempv_bma**: `0`
  - **i_bma**: `0`

### 7. Function: ArithOp
  **Formula:** `nDepChildrenInTu#1`
  **Output Variable:** `i_nelchildren_bma`
  **Tax Unit:** `tu_individual_nl`

### 8. Function: BenCalc
  - **Comp_Cond**: `i_nelchildren_bma>0`
  - **Comp_perTU**: `i_durweeks_bma/i_nelchildren_bma`
  - **Output_Var**: `i_durweeks_bma`
  - **TAX_UNIT**: `tu_bma_nl`

### 9. Function: DefTu
  - **Type**: `SUBGROUP`
  - **Name**: `tu_bma_nl`
  - **Members**: `Partner & OwnDepChild & LooseDepChild`
  - **PartnerCond**: `Default`
  - **DepChildCond**: `Default & dag <1`
  - **ExtHeadCond**: `nDepChOfCouple > 0 & (dgn = 0 | ( dgn =1 & idpartner = 0))`
  - **StopIfNoHeadFound**: `no`

### 10. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bma=1 & yemmy > 0`
  - **Comp_perTU**: `yem*12/yemmy`
  - **Output_Var**: `i_yempv_bma`
  - **TAX_UNIT**: `tu_individual_nl`
  - **Comp_UpLim**: `290.67#d`

### 11. Function: BenCalc
  - **Comp_Cond**: `i_elparent_bma=1 & yse > 0 & i_yempv_bma = 0`
  - **Comp_perTU**: `($MinWage_m/30.5*7)*i_durweeks_bma`
  - **Output_Var**: `i_bma`
  - **TAX_UNIT**: `tu_individual_nl`

### 12. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `bcbma01`
  **Tax Unit:** `tu_individual_nl`

### 13. Function: BenCalc
  - **Comp_Cond**: `yem>0 | bcbma01>0 | lcb_a=1`
  - **Comp_perTU**: `i_bma/12`
  - **Output_Var**: `bma_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 14. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `bcbma02`
  **Tax Unit:** `tu_individual_nl`


---

## Policy: random_nl
### 1. Function: DefVar
  - **i_mc_rand_1**: `0`
  - **i_mc_rand_2**: `0`
  - **i_lmamy**: `0`
  - **i_lma2**: `0`
  - **i_lma1**: `0`
  - **i_mc_rand_3**: `0`
  - **Var_Monetary**: `no`
  - **i_bsa00_rand**: `0`

### 2. Function: RandSeed
  - **Seed**: `19`

### 3. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_1`
  **Tax Unit:** `tu_individual_nl`

### 4. Function: RandSeed
  - **Seed**: `20`

### 5. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_2`
  **Tax Unit:** `tu_individual_nl`

### 6. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lmamy`
  **Tax Unit:** `tu_individual_nl`

### 7. Function: RandSeed
  - **Seed**: `24`

### 8. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lma2`
  **Tax Unit:** `tu_individual_nl`

### 9. Function: RandSeed
  - **Seed**: `23`

### 10. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lma1`
  **Tax Unit:** `tu_individual_nl`

### 11. Function: RandSeed
  - **Seed**: `22`

### 12. Function: RandSeed
  - **Seed**: `21`

### 13. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_3`
  **Tax Unit:** `tu_individual_nl`

### 14. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_bsa00_rand`
  **Tax Unit:** `tu_individual_nl`

### 15. Function: RandSeed
  - **Seed**: `734519`


---

## Policy: bsasenet_nl *(Switch: n/a)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_taxcredits**: `n/a`
  - **i_bsa1**: `n/a`
  - **i_netbsase**: `n/a`
  - **i_eligbsase**: `n/a`
  - **var_monetary**: `n/a`
  - **i_bsa2**: `n/a`
  - **i_bsa3**: `n/a`
  - **i_bsa4**: `n/a`
  - **i_owner**: `n/a`
  - **i_sben_means_se**: `n/a`
  - **i_ysemt1**: `n/a`
  - **i_tinyse1**: `n/a`
  - **i_bsanorm**: `n/a`
  - **i_netbsa_r1**: `n/a`
  - **n_nstuds**: `n/a`
  - **Var_Monetary**: `n/a`
  - **n_nstud**: `n/a`
  - **i_bsanormc**: `n/a`
  - **n_nstuds_ind**: `n/a`
  - **i_bsafactor**: `n/a`

### 2. Function: DefIl *(Switch: n/a)*
  - **name**: `n/a`
  - **tintc00_s**: `n/a`
  - **tintcee_s**: `n/a`
  - **tintclp_s**: `n/a`
  - **tintcpe_s**: `n/a`

### 3. Function: DefIl *(Switch: n/a)*
  - **name**: `n/a`
  - **il_meansTClp**: `n/a`
  - **tintcch00_s**: `n/a`
  - **tintclp00_s**: `n/a`

### 4. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 5. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 6. Function: DefIl *(Switch: n/a)*
  - **name**: `n/a`
  - **yem**: `n/a`
  - **bcbma01**: `n/a`
  - **bcbma02**: `n/a`
  - **bma_s**: `n/a`
  - **yot**: `n/a`
  - **ypp**: `n/a`
  - **ypr**: `n/a`
  - **ypt**: `n/a`
  - **bed**: `n/a`
  - **bhl**: `n/a`
  - **bunct_s**: `n/a`
  - **bunst**: `n/a`
  - **bsaot**: `n/a`
  - **kfb**: `n/a`
  - **pdi**: `n/a`
  - **psu_s**: `n/a`
  - **poa00_s**: `n/a`
  - **poacm**: `n/a`
  - **tpcpe**: `n/a`
  - **tsceeui_s**: `n/a`
  - **tsceepigr_s**: `n/a`
  - **tingt_s**: `n/a`
  - **tschl03_s**: `n/a`
  - **i_taxcredits**: `n/a`
  - **yse**: `n/a`

### 7. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 8. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 9. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 10. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 11. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 12. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **comp_perTU**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **result_var**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 13. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 14. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **comp_perTU**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **result_var**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 15. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 16. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **#_level**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **result_var**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 17. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 18. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMin**: `n/a`
  - **#_AgeMax**: `n/a`
  - **#_level**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **result_var**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 19. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 20. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 21. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perElig**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 22. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 23. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 24. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 25. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **#_AgeMax**: `n/a`
  - **#_AgeMin**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 26. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 27. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 28. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 29. Function: Allocate *(Switch: n/a)*
  - **share**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 30. Function: DefIl *(Switch: n/a)*
  - **name**: `n/a`
  - **yem**: `n/a`
  - **bcbma01**: `n/a`
  - **bcbma02**: `n/a`
  - **bma_s**: `n/a`
  - **yse**: `n/a`
  - **yot**: `n/a`
  - **ypp**: `n/a`
  - **ypr**: `n/a`
  - **ypt**: `n/a`
  - **bed**: `n/a`
  - **bhl**: `n/a`
  - **bunct_s**: `n/a`
  - **bunst**: `n/a`
  - **bsaot**: `n/a`
  - **kfb**: `n/a`
  - **pdi**: `n/a`
  - **psu_s**: `n/a`
  - **poa00_s**: `n/a`
  - **poacm**: `n/a`
  - **tpcpe**: `n/a`
  - **tsceeui_s**: `n/a`
  - **tschl03_s**: `n/a`

### 31. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 32. Function: Allocate *(Switch: n/a)*
  - **share**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: bsasegross_nl *(Switch: n/a)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_rf**: `n/a`
  - **i_rfmax**: `n/a`
  - **i_bsadiff**: `n/a`
  - **i_taxpos**: `n/a`
  - **i_tsceepi_s**: `n/a`
  - **i_tin_s**: `n/a`

### 2. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 3. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 4. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 5. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 6. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 7. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

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

### 11. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_info**: `n/a`
  - **#_level**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 12. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **#_income**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 13. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 14. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 15. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 16. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 17. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 18. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 19. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 20. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 21. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 22. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 23. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 24. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 25. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 26. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 27. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 28. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 29. Function: DefVar *(Switch: n/a)*
  - **i_rev**: `n/a`
  - **var_monetary**: `n/a`
  - **i_diff**: `n/a`
  - **i_sben_means_r**: `n/a`
  - **i_netbsa_r**: `n/a`
  - **i_bsa00_s**: `n/a`

### 30. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 31. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 32. Function: Allocate *(Switch: n/a)*
  - **share**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 33. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 34. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 35. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 36. Function: Allocate *(Switch: n/a)*
  - **share**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 37. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 38. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 39. Function: Allocate *(Switch: n/a)*
  - **share**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 40. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 41. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 42. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 43. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 44. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 45. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 46. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 47. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 48. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: chall2_nl *(Switch: n/a)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_eligchtc**: `n/a`
  - **var_monetary**: `n/a`
  - **i_TotalTaxableIncome**: `n/a`

### 2. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 3. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 4. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 5. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_level**: `n/a`
  - **lowlim**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 6. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: yemcomp_nl *(Switch: n/a)*
### 1. Function: DefVar *(Switch: n/a)*
  - **Var_Monetary**: `n/a`
  - ** i_bwkmcee_s**: `n/a`
  - **i_yemmc_s**: `n/a`

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

## Policy: tco_nl *(Switch: off)*
### 1. Function: DefConst
  **Constants Defined:**
  - `$tco_v_07223`: $tco_base_v_07223
  - `$tco_v_07222`: $tco_base_v_07222
  - `$tco_v_07221`: $tco_base_v_07221
  - `$tco_v_04541`: n/a
  - `$tco_v_04531`: $tco_base_v_04531
  - `$tco_v_04522`: n/a
  - `$tco_v_04521`: $tco_base_v_04521
  - `$tco_v_04511`: $tco_base_v_04511
  - `$tco_v_02213`: $tco_base_v_02213
  - `$tco_v_02212`: $tco_base_v_02212
  - `$tco_v_02211`: $tco_base_v_02211
  - `$tco_v_02134`: $tco_base_v_02134
  - `$tco_v_02133`: $tco_base_v_02133
  - `$tco_v_02132`: $tco_base_v_02132
  - `$tco_v_02131`: $tco_base_v_02131
  - `$tco_v_02124`: $tco_base_v_02124
  - `$tco_v_02123`: $tco_base_v_02123
  - `$tco_v_02122`: $tco_base_v_02122
  - `$tco_v_02121`: $tco_base_v_02121
  - `$tco_v_02112`: $tco_base_v_02112
  - `$tco_v_02111`: $tco_base_v_02111

### 2. Function: DefConst
  **Constants Defined:**
  - `$tco_a_07223`: 0.70*$tco_a_07223a + 0.00*(($tco_a_07223b1+$tco_a_07223b2)/2) + 0.30*$tco_a_07223c
  - `$tco_a_07222`: 1.00*$tco_a_07222a +0.00*$tco_a_07222b
  - `$tco_a_07221`: 0.50*$tco_a_07221a +0.50*$tco_a_07221b
  - `$tco_a_04531`: 1.00*$tco_a_04531a + 0.00*$tco_a_04531b + 0.00*$tco_a_04531c
  - `$tco_a_02131`: 0.50*$tco_a_02131a +0.50*$tco_a_02131b
  - `$tco_a_02121`: 0.90*$tco_a_02121a +0.05*$tco_a_02121b+0.025*$tco_a_02121c+0.025*$tco_a_02121d
  - `$tco_a_02123`: 0.90*$tco_a_02123a +0.05*$tco_a_02123b+0.05*$tco_a_02123c
  - `$tco_a_02122`: 0.90*$tco_a_02122a +0.05*$tco_a_02122b+0.025*$tco_a_02122c+0.025*$tco_a_02122d

### 3. Function: DefConst
  **Constants Defined:**
  - `$tco_base_a_04531`: 1.00*$tco_base_a_04531a + 0.00*$tco_base_a_04531b + 0.00*$tco_base_a_04531c
  - `$tco_base_a_07223`: 1.00*$tco_base_a_07223a + 0.00*(($tco_base_a_07223b1+$tco_base_a_07223b2)/2) + 0.00*$tco_base_a_07223c
  - `$tco_base_q_02111`: ($tco_base_q_02111t) / 40% * 100
  - `$tco_base_q_02121`: (0.95*$tco_base_q_02121at+0.05*$tco_base_q_02121bt) * 100
  - `$tco_base_q_02122`: $tco_base_q_02122t* 100
  - `$tco_base_q_02123`: $tco_base_q_02123t* 100
  - `$tco_base_q_02124`: $tco_base_q_02124t* 100
  - `$tco_base_q_02131`: $tco_base_q_02131t* 100
  - `$tco_base_q_07223`: 1.00*$tco_base_q_07223a + 0.00*$tco_base_q_07223b + 0.00*$tco_base_q_07223c
  - `$tco_base_q_04531`: 1.00*$tco_base_q_04531a + 0.00*$tco_base_q_04531b + 0.00*$tco_base_q_04531c
  - `$tco_base_q_02134`: $tco_base_q_02134t * 100
  - `$tco_base_q_02133`: $tco_base_q_02133t * 100
  - `$tco_base_q_02132`: $tco_base_q_02132t * 100
  - `$tco_base_q_02112`: ($tco_base_q_02112t) / 5% * 100
  - `$tco_base_a_07221`: 0.50*$tco_base_a_07221a +0.50*$tco_base_a_07221b
  - `$tco_base_a_02131`: 0.50*$tco_base_a_02131a +0.50*$tco_base_a_02131b
  - `$tco_base_a_07222`: 1.00*$tco_base_a_07222a +0.00*$tco_base_a_07222b
  - `$tco_base_a_02123`: 0.90*$tco_base_a_02123a +0.05*$tco_base_a_02123b+0.05*$tco_base_a_02123c
  - `$tco_base_a_02122`: 0.90*$tco_base_a_02122a +0.05*$tco_base_a_02122b+0.025*$tco_base_a_02122c+0.025*$tco_base_a_02122d
  - `$tco_base_a_02121`: 0.90*$tco_base_a_02121a +0.05*$tco_base_a_02121b+0.025*$tco_base_a_02121c+0.025*$tco_base_a_02121d

### 4. Function: DefIl
  - **Name**: `il_xs_exc`
  - **Warn_If_NonMonetary**: `no`
  - **xs07223**: `+`
  - **xs07222**: `+`
  - **xs07221**: `+`
  - **xs04541**: `n/a`
  - **xs04531**: `+`
  - **xs04522**: `n/a`
  - **xs04521**: `+`
  - **xs04511**: `+`
  - **xs02213**: `+`
  - **xs02212**: `+`
  - **xs02211**: `+`
  - **xs02134**: `+`
  - **xs02133**: `+`
  - **xs02132**: `+`
  - **xs02131**: `+`
  - **xs02124**: `+`
  - **xs02123**: `+`
  - **xs02122**: `+`
  - **xs02121**: `+`
  - **xs02112**: `+`
  - **xs02111**: `+`

### 5. Function: DefConst
  **Constants Defined:**
  - `$tco_t_12714`: $tco_t_std
  - `$tco_t_12713`: $tco_t_zero
  - `$tco_t_12712`: $tco_t_std
  - `$tco_t_12711`: $tco_t_std
  - `$tco_t_12622`: $tco_t_zero
  - `$tco_t_12621`: $tco_t_zero
  - `$tco_t_12551`: $tco_t_zero
  - `$tco_t_12542`: $tco_t_zero
  - `$tco_t_12541`: $tco_t_zero
  - `$tco_t_12532`: $tco_t_zero
  - `$tco_t_12531`: $tco_t_zero
  - `$tco_t_12521`: $tco_t_zero
  - `$tco_t_12414`: $tco_t_zero
  - `$tco_t_12413`: $tco_t_zero
  - `$tco_t_12412`: $tco_t_zero
  - `$tco_t_12411`: $tco_t_zero
  - `$tco_t_12329`: $tco_t_std
  - `$tco_t_12323`: $tco_t_red1
  - `$tco_t_12322`: $tco_t_std
  - `$tco_t_12321`: $tco_t_std
  - `$tco_t_12313`: $tco_t_std
  - `$tco_t_12312`: $tco_t_std
  - `$tco_t_12311`: $tco_t_std
  - `$tco_t_12132`: $tco_t_std
  - `$tco_t_12131`: $tco_t_std
  - `$tco_t_12122`: $tco_t_std
  - `$tco_t_12121`: $tco_t_std
  - `$tco_t_12113`: $tco_t_red1
  - `$tco_t_12112`: $tco_t_red1
  - `$tco_t_12111`: $tco_t_red1
  - `$tco_t_11213`: $tco_t_red1
  - `$tco_t_11212`: $tco_t_red1
  - `$tco_t_11211`: $tco_t_red1
  - `$tco_t_11121`: $tco_t_red1
  - `$tco_t_11112`: $tco_t_red1
  - `$tco_t_11111`: $tco_t_red1
  - `$tco_t_10511`: $tco_t_zero
  - `$tco_t_10411`: $tco_t_zero
  - `$tco_t_10311`: $tco_t_zero
  - `$tco_t_10211`: $tco_t_zero
  - `$tco_t_10112`: $tco_t_zero
  - `$tco_t_10111`: $tco_t_zero
  - `$tco_t_09612`: $tco_t_std
  - `$tco_t_09611`: $tco_t_std
  - `$tco_t_09549`: $tco_t_std
  - `$tco_t_09541`: $tco_t_std
  - `$tco_t_09531`: $tco_t_std
  - `$tco_t_09522`: $tco_t_red1
  - `$tco_t_09521`: $tco_t_red1
  - `$tco_t_09514`: $tco_t_red1
  - `$tco_t_09513`: $tco_t_red1
  - `$tco_t_09512`: $tco_t_red1
  - `$tco_t_09511`: $tco_t_red1
  - `$tco_t_09429`: $tco_t_std
  - `$tco_t_09425`: $tco_t_std
  - `$tco_t_09424`: $tco_t_std
  - `$tco_t_09423`: $tco_t_std
  - `$tco_t_09422`: $tco_t_red1
  - `$tco_t_09421`: $tco_t_red1
  - `$tco_t_09412`: $tco_t_red1
  - `$tco_t_09411`: $tco_t_red1
  - `$tco_t_09351`: $tco_t_std
  - `$tco_t_09342`: $tco_t_std
  - `$tco_t_09341`: $tco_t_std
  - `$tco_t_09332`: $tco_t_red1
  - `$tco_t_09331`: $tco_t_std
  - `$tco_t_09323`: $tco_t_std
  - `$tco_t_09322`: $tco_t_std
  - `$tco_t_09321`: $tco_t_std
  - `$tco_t_09312`: $tco_t_std
  - `$tco_t_09311`: $tco_t_std
  - `$tco_t_09231`: $tco_t_std
  - `$tco_t_09222`: $tco_t_std
  - `$tco_t_09221`: $tco_t_std
  - `$tco_t_09215`: $tco_t_std
  - `$tco_t_09214`: $tco_t_std
  - `$tco_t_09213`: $tco_t_std
  - `$tco_t_09212`: $tco_t_std
  - `$tco_t_09211`: $tco_t_std
  - `$tco_t_09151`: $tco_t_std
  - `$tco_t_09149`: $tco_t_std
  - `$tco_t_09142`: $tco_t_std
  - `$tco_t_09141`: $tco_t_std
  - `$tco_t_09134`: $tco_t_std
  - `$tco_t_09133`: $tco_t_std
  - `$tco_t_09132`: $tco_t_std
  - `$tco_t_09131`: $tco_t_std
  - `$tco_t_09123`: $tco_t_std
  - `$tco_t_09122`: $tco_t_std
  - `$tco_t_09121`: $tco_t_std
  - `$tco_t_09119`: $tco_t_std
  - `$tco_t_09113`: $tco_t_std
  - `$tco_t_09112`: $tco_t_std
  - `$tco_t_09111`: $tco_t_std
  - `$tco_t_08315`: $tco_t_std
  - `$tco_t_08314`: $tco_t_std
  - `$tco_t_08313`: $tco_t_std
  - `$tco_t_08312`: $tco_t_std
  - `$tco_t_08311`: $tco_t_std
  - `$tco_t_08214`: $tco_t_std
  - `$tco_t_08213`: $tco_t_std
  - `$tco_t_08212`: $tco_t_std
  - `$tco_t_08211`: $tco_t_std
  - `$tco_t_08119`: $tco_t_std
  - `$tco_t_08111`: $tco_t_zero
  - `$tco_t_07369`: $tco_t_std
  - `$tco_t_07362`: $tco_t_std
  - `$tco_t_07361`: $tco_t_std
  - `$tco_t_07351`: $tco_t_red1
  - `$tco_t_07342`: $tco_t_red1
  - `$tco_t_07341`: $tco_t_red1
  - `$tco_t_07332`: $tco_t_zero
  - `$tco_t_07331`: $tco_t_zero
  - `$tco_t_07322`: $tco_t_red1
  - `$tco_t_07321`: $tco_t_red1
  - `$tco_t_07312`: $tco_t_red1
  - `$tco_t_07311`: $tco_t_red1
  - `$tco_t_07243`: $tco_t_std
  - `$tco_t_07242`: $tco_t_std
  - `$tco_t_07241`: $tco_t_std
  - `$tco_t_07231`: $tco_t_std
  - `$tco_t_07224`: $tco_t_std
  - `$tco_t_07223`: $tco_t_std
  - `$tco_t_07222`: $tco_t_std
  - `$tco_t_07221`: $tco_t_std
  - `$tco_t_07213`: $tco_t_std
  - `$tco_t_07212`: $tco_t_std
  - `$tco_t_07211`: $tco_t_std
  - `$tco_t_07141`: $tco_t_std
  - `$tco_t_07131`: $tco_t_std
  - `$tco_t_07121`: $tco_t_std
  - `$tco_t_07112`: $tco_t_std
  - `$tco_t_07111`: $tco_t_std
  - `$tco_t_06311`: $tco_t_zero
  - `$tco_t_06239`: $tco_t_zero
  - `$tco_t_06232`: $tco_t_zero
  - `$tco_t_06231`: $tco_t_zero
  - `$tco_t_06221`: $tco_t_zero
  - `$tco_t_06212`: $tco_t_zero
  - `$tco_t_06211`: $tco_t_zero
  - `$tco_t_06139`: $tco_t_red1
  - `$tco_t_06133`: $tco_t_zero
  - `$tco_t_06132`: $tco_t_red1
  - `$tco_t_06131`: $tco_t_std
  - `$tco_t_06129`: $tco_t_red1
  - `$tco_t_06121`: $tco_t_red1
  - `$tco_t_06111`: $tco_t_red1
  - `$tco_t_05629`: $tco_t_std
  - `$tco_t_05623`: $tco_t_std
  - `$tco_t_05622`: $tco_t_red1
  - `$tco_t_05621`: $tco_t_std
  - `$tco_t_05612`: $tco_t_std
  - `$tco_t_05611`: $tco_t_std
  - `$tco_t_05523`: $tco_t_std
  - `$tco_t_05522`: $tco_t_std
  - `$tco_t_05521`: $tco_t_std
  - `$tco_t_05512`: $tco_t_std
  - `$tco_t_05511`: $tco_t_std
  - `$tco_t_05414`: $tco_t_std
  - `$tco_t_05413`: $tco_t_std
  - `$tco_t_05412`: $tco_t_std
  - `$tco_t_05411`: $tco_t_std
  - `$tco_t_05331`: $tco_t_std
  - `$tco_t_05329`: $tco_t_std
  - `$tco_t_05324`: $tco_t_std
  - `$tco_t_05323`: $tco_t_std
  - `$tco_t_05322`: $tco_t_std
  - `$tco_t_05321`: $tco_t_std
  - `$tco_t_05319`: $tco_t_std
  - `$tco_t_05315`: $tco_t_std
  - `$tco_t_05314`: $tco_t_std
  - `$tco_t_05313`: $tco_t_std
  - `$tco_t_05312`: $tco_t_std
  - `$tco_t_05311`: $tco_t_std
  - `$tco_t_05219`: $tco_t_std
  - `$tco_t_05214`: $tco_t_red1
  - `$tco_t_05213`: $tco_t_std
  - `$tco_t_05212`: $tco_t_std
  - `$tco_t_05211`: $tco_t_std
  - `$tco_t_05131`: $tco_t_std
  - `$tco_t_05123`: $tco_t_std
  - `$tco_t_05122`: $tco_t_std
  - `$tco_t_05121`: $tco_t_std
  - `$tco_t_05119`: $tco_t_std
  - `$tco_t_05113`: $tco_t_std
  - `$tco_t_05112`: $tco_t_std
  - `$tco_t_05111`: $tco_t_std
  - `$tco_t_04551`: $tco_t_std
  - `$tco_t_04549`: $tco_t_std
  - `$tco_t_04541`: n/a
  - `$tco_t_04531`: $tco_t_std
  - `$tco_t_04522`: n/a
  - `$tco_t_04521`: $tco_t_std
  - `$tco_t_04511`: $tco_t_std
  - `$tco_t_04449`: $tco_t_std
  - `$tco_t_04442`: $tco_t_std
  - `$tco_t_04441`: $tco_t_std
  - `$tco_t_04431`: $tco_t_std
  - `$tco_t_04421`: $tco_t_std
  - `$tco_t_04411`: $tco_t_red1
  - `$tco_t_04329`: $tco_t_std
  - `$tco_t_04325`: $tco_t_std
  - `$tco_t_04324`: $tco_t_red1
  - `$tco_t_04323`: $tco_t_std
  - `$tco_t_04322`: $tco_t_std
  - `$tco_t_04321`: $tco_t_std
  - `$tco_t_04311`: $tco_t_std
  - `$tco_t_04122`: $tco_t_std
  - `$tco_t_04121`: $tco_t_zero
  - `$tco_t_04111`: $tco_t_zero
  - `$tco_t_03221`: $tco_t_red1
  - `$tco_t_03213`: $tco_t_std
  - `$tco_t_03212`: $tco_t_std
  - `$tco_t_03211`: $tco_t_std
  - `$tco_t_03142`: $tco_t_red1
  - `$tco_t_03141`: $tco_t_std
  - `$tco_t_03132`: $tco_t_std
  - `$tco_t_03131`: $tco_t_std
  - `$tco_t_03123`: $tco_t_std
  - `$tco_t_03122`: $tco_t_std
  - `$tco_t_03121`: $tco_t_std
  - `$tco_t_03111`: $tco_t_std
  - `$tco_t_02213`: $tco_t_std
  - `$tco_t_02212`: $tco_t_std
  - `$tco_t_02211`: $tco_t_std
  - `$tco_t_02134`: $tco_t_std
  - `$tco_t_02133`: $tco_t_red1
  - `$tco_t_02132`: $tco_t_std
  - `$tco_t_02131`: $tco_t_std
  - `$tco_t_02124`: $tco_t_std
  - `$tco_t_02123`: $tco_t_std
  - `$tco_t_02122`: $tco_t_std
  - `$tco_t_02121`: $tco_t_std
  - `$tco_t_02112`: $tco_t_std
  - `$tco_t_02111`: $tco_t_std
  - `$tco_t_01223`: $tco_t_red1
  - `$tco_t_01222`: $tco_t_red1
  - `$tco_t_01221`: $tco_t_red1
  - `$tco_t_01213`: $tco_t_red1
  - `$tco_t_01212`: $tco_t_red1
  - `$tco_t_01211`: $tco_t_red1
  - `$tco_t_01199`: $tco_t_red1
  - `$tco_t_01194`: $tco_t_red1
  - `$tco_t_01193`: $tco_t_red1
  - `$tco_t_01192`: $tco_t_red1
  - `$tco_t_01191`: $tco_t_red1
  - `$tco_t_01186`: $tco_t_red1
  - `$tco_t_01185`: $tco_t_red1
  - `$tco_t_01184`: $tco_t_red1
  - `$tco_t_01183`: $tco_t_red1
  - `$tco_t_01182`: $tco_t_red1
  - `$tco_t_01181`: $tco_t_red1
  - `$tco_t_01176`: $tco_t_red1
  - `$tco_t_01175`: $tco_t_red1
  - `$tco_t_01174`: $tco_t_red1
  - `$tco_t_01173`: $tco_t_red1
  - `$tco_t_01172`: $tco_t_red1
  - `$tco_t_01171`: $tco_t_red1
  - `$tco_t_01164`: $tco_t_red1
  - `$tco_t_01163`: $tco_t_red1
  - `$tco_t_01162`: $tco_t_red1
  - `$tco_t_01161`: $tco_t_red1
  - `$tco_t_01155`: $tco_t_red1
  - `$tco_t_01154`: $tco_t_red1
  - `$tco_t_01153`: $tco_t_red1
  - `$tco_t_01152`: $tco_t_red1
  - `$tco_t_01151`: $tco_t_red1
  - `$tco_t_01147`: $tco_t_red1
  - `$tco_t_01146`: $tco_t_red1
  - `$tco_t_01145`: $tco_t_red1
  - `$tco_t_01144`: $tco_t_red1
  - `$tco_t_01143`: $tco_t_red1
  - `$tco_t_01142`: $tco_t_red1
  - `$tco_t_01141`: $tco_t_red1
  - `$tco_t_01136`: $tco_t_red1
  - `$tco_t_01135`: $tco_t_red1
  - `$tco_t_01134`: $tco_t_red1
  - `$tco_t_01133`: $tco_t_red1
  - `$tco_t_01132`: $tco_t_red1
  - `$tco_t_01131`: $tco_t_red1
  - `$tco_t_01128`: $tco_t_red1
  - `$tco_t_01127`: $tco_t_red1
  - `$tco_t_01126`: $tco_t_red1
  - `$tco_t_01125`: $tco_t_red1
  - `$tco_t_01124`: $tco_t_red1
  - `$tco_t_01123`: $tco_t_red1
  - `$tco_t_01122`: $tco_t_red1
  - `$tco_t_01121`: $tco_t_red1
  - `$tco_t_01118`: $tco_t_red1
  - `$tco_t_01117`: $tco_t_red1
  - `$tco_t_01116`: $tco_t_red1
  - `$tco_t_01115`: $tco_t_red1
  - `$tco_t_01114`: $tco_t_red1
  - `$tco_t_01113`: $tco_t_red1
  - `$tco_t_01112`: $tco_t_red1
  - `$tco_t_01111`: $tco_t_red1
  - `Run_Cond`: GetDataCOICOPVersion = 2003

### 6. Function: DefConst
  **Constants Defined:**
  - `$tco_t_std`: $tco_base_t_std
  - `$tco_t_red1`: $tco_base_t_red1
  - `$tco_t_zero`: $tco_base_t_zero

### 7. Function: DefConst
  **Constants Defined:**
  - `$tco_a_07223c`: $tco_base_a_07223c
  - `$tco_a_07223b2`: $tco_base_a_07223b2
  - `$tco_a_07223b1`: $tco_base_a_07223b1
  - `$tco_a_07223a`: $tco_base_a_07223a
  - `$tco_a_07222b`: $tco_base_a_07222b
  - `$tco_a_07222a`: $tco_base_a_07222a
  - `$tco_a_07221b`: $tco_base_a_07221b
  - `$tco_a_07221a`: $tco_base_a_07221a
  - `$tco_a_04541`: n/a
  - `$tco_a_04531c`: $tco_base_a_04531c
  - `$tco_a_04531b`: $tco_base_a_04531b
  - `$tco_a_04531a`: $tco_base_a_04531a
  - `$tco_a_04522`: n/a
  - `$tco_a_04521`: $tco_base_a_04521
  - `$tco_a_04511`: $tco_base_a_04511
  - `$tco_a_02213`: $tco_base_a_02213
  - `$tco_a_02212`: $tco_base_a_02212
  - `$tco_a_02211`: $tco_base_a_02211
  - `$tco_a_02134`: $tco_base_a_02134
  - `$tco_a_02133`: $tco_base_a_02133
  - `$tco_a_02132`: $tco_base_a_02132
  - `$tco_a_02131b`: $tco_base_a_02131b
  - `$tco_a_02131a`: $tco_base_a_02131a
  - `$tco_a_02124`: $tco_base_a_02124
  - `$tco_a_02123a`: $tco_base_a_02123a
  - `$tco_a_02122a`: $tco_base_a_02122a
  - `$tco_a_02121b`: $tco_base_a_02121b
  - `$tco_a_02121a`: $tco_base_a_02121a
  - `$tco_a_02112`: $tco_base_a_02112
  - `$tco_a_02111`: $tco_base_a_02111
  - `$tco_a_02123c`: $tco_base_a_02123c
  - `$tco_a_02123b`: $tco_base_a_02123b
  - `$tco_a_02122d`: $tco_base_a_02122d
  - `$tco_a_02122c`: $tco_base_a_02122c
  - `$tco_a_02122b`: $tco_base_a_02122b
  - `$tco_a_02121d`: $tco_base_a_02121d
  - `$tco_a_02121c`: $tco_base_a_02121c

### 8. Function: DefIl
  - **Name**: `il_xs_rest`
  - **Warn_If_NonMonetary**: `no`
  - **xs12714**: `+`
  - **xs12713**: `+`
  - **xs12712**: `+`
  - **xs12711**: `+`
  - **xs12622**: `+`
  - **xs12621**: `+`
  - **xs12551**: `+`
  - **xs12542**: `+`
  - **xs12541**: `+`
  - **xs12532**: `+`
  - **xs12531**: `+`
  - **xs12521**: `+`
  - **xs12414**: `+`
  - **xs12413**: `+`
  - **xs12412**: `+`
  - **xs12411**: `+`
  - **xs12329**: `+`
  - **xs12323**: `+`
  - **xs12322**: `+`
  - **xs12321**: `+`
  - **xs12313**: `+`
  - **xs12312**: `+`
  - **xs12311**: `+`
  - **xs12132**: `+`
  - **xs12131**: `+`
  - **xs12122**: `+`
  - **xs12121**: `+`
  - **xs12113**: `+`
  - **xs12112**: `+`
  - **xs12111**: `+`
  - **xs11213**: `+`
  - **xs11212**: `+`
  - **xs11211**: `+`
  - **xs11121**: `+`
  - **xs11112**: `+`
  - **xs11111**: `+`
  - **xs10511**: `+`
  - **xs10411**: `+`
  - **xs10311**: `+`
  - **xs10211**: `+`
  - **xs10112**: `+`
  - **xs10111**: `+`
  - **xs09612**: `+`
  - **xs09611**: `+`
  - **xs09549**: `+`
  - **xs09541**: `+`
  - **xs09531**: `+`
  - **xs09522**: `+`
  - **xs09521**: `+`
  - **xs09514**: `+`
  - **xs09513**: `+`
  - **xs09512**: `+`
  - **xs09511**: `+`
  - **xs09429**: `+`
  - **xs09425**: `+`
  - **xs09424**: `+`
  - **xs09423**: `+`
  - **xs09422**: `+`
  - **xs09421**: `+`
  - **xs09412**: `+`
  - **xs09411**: `+`
  - **xs09351**: `+`
  - **xs09342**: `+`
  - **xs09341**: `+`
  - **xs09332**: `+`
  - **xs09331**: `+`
  - **xs09323**: `+`
  - **xs09322**: `+`
  - **xs09321**: `+`
  - **xs09312**: `+`
  - **xs09311**: `+`
  - **xs09231**: `+`
  - **xs09222**: `+`
  - **xs09221**: `+`
  - **xs09215**: `+`
  - **xs09214**: `+`
  - **xs09213**: `+`
  - **xs09212**: `+`
  - **xs09211**: `+`
  - **xs09151**: `+`
  - **xs09149**: `+`
  - **xs09142**: `+`
  - **xs09141**: `+`
  - **xs09134**: `+`
  - **xs09133**: `+`
  - **xs09132**: `+`
  - **xs09131**: `+`
  - **xs09123**: `+`
  - **xs09122**: `+`
  - **xs09121**: `+`
  - **xs09119**: `+`
  - **xs09113**: `+`
  - **xs09112**: `+`
  - **xs09111**: `+`
  - **xs08315**: `+`
  - **xs08314**: `+`
  - **xs08313**: `+`
  - **xs08312**: `+`
  - **xs08311**: `+`
  - **xs08214**: `+`
  - **xs08213**: `+`
  - **xs08212**: `+`
  - **xs08211**: `+`
  - **xs08119**: `+`
  - **xs08111**: `+`
  - **xs07369**: `+`
  - **xs07362**: `+`
  - **xs07361**: `+`
  - **xs07351**: `+`
  - **xs07342**: `+`
  - **xs07341**: `+`
  - **xs07332**: `+`
  - **xs07331**: `+`
  - **xs07322**: `+`
  - **xs07321**: `+`
  - **xs07312**: `+`
  - **xs07311**: `+`
  - **xs07243**: `+`
  - **xs07242**: `+`
  - **xs07241**: `+`
  - **xs07231**: `+`
  - **xs07224**: `+`
  - **xs07213**: `+`
  - **xs07212**: `+`
  - **xs07211**: `+`
  - **xs07141**: `+`
  - **xs07131**: `+`
  - **xs07121**: `+`
  - **xs07112**: `+`
  - **xs07111**: `+`
  - **xs06311**: `+`
  - **xs06239**: `+`
  - **xs06232**: `+`
  - **xs06231**: `+`
  - **xs06221**: `+`
  - **xs06212**: `+`
  - **xs06211**: `+`
  - **xs06139**: `+`
  - **xs06133**: `+`
  - **xs06132**: `+`
  - **xs06131**: `+`
  - **xs06129**: `+`
  - **xs06121**: `+`
  - **xs06111**: `+`
  - **xs05629**: `+`
  - **xs05623**: `+`
  - **xs05622**: `+`
  - **xs05621**: `+`
  - **xs05612**: `+`
  - **xs05611**: `+`
  - **xs05523**: `+`
  - **xs05522**: `+`
  - **xs05521**: `+`
  - **xs05512**: `+`
  - **xs05511**: `+`
  - **xs05414**: `+`
  - **xs05413**: `+`
  - **xs05412**: `+`
  - **xs05411**: `+`
  - **xs05331**: `+`
  - **xs05329**: `+`
  - **xs05324**: `+`
  - **xs05323**: `+`
  - **xs05322**: `+`
  - **xs05321**: `+`
  - **xs05319**: `+`
  - **xs05315**: `+`
  - **xs05314**: `+`
  - **xs05313**: `+`
  - **xs05312**: `+`
  - **xs05311**: `+`
  - **xs05219**: `+`
  - **xs05214**: `+`
  - **xs05213**: `+`
  - **xs05212**: `+`
  - **xs05211**: `+`
  - **xs05131**: `+`
  - **xs05123**: `+`
  - **xs05122**: `+`
  - **xs05121**: `+`
  - **xs05119**: `+`
  - **xs05113**: `+`
  - **xs05112**: `+`
  - **xs05111**: `+`
  - **xs04551**: `+`
  - **xs04549**: `+`
  - **xs04449**: `+`
  - **xs04442**: `+`
  - **xs04441**: `+`
  - **xs04431**: `+`
  - **xs04421**: `+`
  - **xs04411**: `+`
  - **xs04329**: `+`
  - **xs04325**: `+`
  - **xs04324**: `+`
  - **xs04323**: `+`
  - **xs04322**: `+`
  - **xs04321**: `+`
  - **xs04311**: `+`
  - **xs04122**: `+`
  - **xs04121**: `+`
  - **xs04111**: `+`
  - **xs03221**: `+`
  - **xs03213**: `+`
  - **xs03212**: `+`
  - **xs03211**: `+`
  - **xs03142**: `+`
  - **xs03141**: `+`
  - **xs03132**: `+`
  - **xs03131**: `+`
  - **xs03123**: `+`
  - **xs03122**: `+`
  - **xs03121**: `+`
  - **xs03111**: `+`
  - **xs01223**: `+`
  - **xs01222**: `+`
  - **xs01221**: `+`
  - **xs01213**: `+`
  - **xs01212**: `+`
  - **xs01211**: `+`
  - **xs01199**: `+`
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
  - **xs01176**: `+`
  - **xs01175**: `+`
  - **xs01174**: `+`
  - **xs01173**: `+`
  - **xs01172**: `+`
  - **xs01171**: `+`
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
  - **xs01136**: `+`
  - **xs01135**: `+`
  - **xs01134**: `+`
  - **xs01133**: `+`
  - **xs01132**: `+`
  - **xs01131**: `+`
  - **xs01128**: `+`
  - **xs01127**: `+`
  - **xs01126**: `+`
  - **xs01125**: `+`
  - **xs01124**: `+`
  - **xs01123**: `+`
  - **xs01122**: `+`
  - **xs01121**: `+`
  - **xs01118**: `+`
  - **xs01117**: `+`
  - **xs01116**: `+`
  - **xs01115**: `+`
  - **xs01114**: `+`
  - **xs01113**: `+`
  - **xs01112**: `+`
  - **xs01111**: `+`

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

## Policy: TransLMA_nl *(Switch: off)*
### 1. Function: DefConst
  **Constants Defined:**
  - `$er_dgn0_deh1_nl`: 0
  - `$er_dgn0_deh2_nl`: 0
  - `$er_dgn0_deh3_nl`: 0
  - `$er_dgn1_deh1_nl`: 0
  - `$er_dgn1_deh2_nl`: 0
  - `$er_dgn1_deh3_nl`: 0
  - `$ur_dgn0_deh1_nl`: 0
  - `$ur_dgn0_deh2_nl`: 0
  - `$ur_dgn0_deh3_nl`: 0
  - `$ur_dgn1_deh1_nl`: 0
  - `$ur_dgn1_deh2_nl`: 0
  - `$ur_dgn1_deh3_nl`: 0
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
  - **Condition:** `(yemmy = 0) & (ysemy = 0) & (liwmy=0) & (lpemy=0) & (dag > 17) & (dag < $PenAge) & ((les=5) | lowas=1)`
  - **Tax Unit:** `tu_individual_nl`

### 3. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(deh = 5) & (dgn = 1) & (i_lma1 < $ur_dgn1_deh3_nl)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_nl`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy > 0) `
  - **Tax Unit:** `tu_individual_nl`

### 5. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(deh = 5) & (dgn = 1) & (i_lma1 < $er_dgn1_deh3_nl)`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_nl`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ysemy > 0) & (yemmy = 0)`
  - **Tax Unit:** `tu_individual_nl`

### 7. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dgn = 1 & (i_lma2 < $er_dgn1_se)`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_nl`

### 8. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lma =1)`
  - **Tax Unit:** `tu_individual_nl`

### 9. Function: ArithOp
  **Formula:** `(yivwg*$Nwh *52/12)`
  **Output Variable:** `yem_a`
  **Tax Unit:** `tu_individual_nl`

### 10. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lma=1)|(lma=5)`
  - **Tax Unit:** `tu_individual_nl`

### 11. Function: ArithOp
  **Formula:** `$Nwh`
  **Output Variable:** `lhw_a`
  **Tax Unit:** `tu_individual_nl`

### 12. Function: BenCalc
  - **Comp_Cond**: `(lma=2) & (ysemy > 0) & (yemmy = 0)`
  - **Comp_perTU**: `0`
  - **Output_Var**: `yemmy_a`
  - **TAX_UNIT**: `tu_individual_nl`

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
  - `$sh_0hours_nl`: 0
  - `$sh_15hours_nl`: 0
  - `$sh_45hours_nl`: 0
  - `$sh_hours_nl`: n/a
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
  - `Run_Cond`: n/a

### 15. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy >0 & bcbma01 = 0 & bcbma02 = 0)  & (lma=0)`
  - **Tax Unit:** `tu_individual_nl`

### 16. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(lindi = 5) & (dgn = 1) & (i_mc_rand_1 < $sh_mcee_l4_dgn1)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lmcee_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 17. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lmcee_s = 1)`
  - **Tax Unit:** `tu_individual_nl`

### 18. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_2> $sh_mceemy_9)`
  - **Comp_perTU**: `min (10, yemmy)`
  - **Output_Var**: `bwkmceemy_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 19. Function: ArithOp
  **Formula:** `yemmy - bwkmceemy_s`
  **Output Variable:** `yemmwmy_s`
  **Tax Unit:** `tu_individual_nl`

### 20. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(bwkmceemy_s > 0)`
  - **Tax Unit:** `tu_individual_nl`

### 21. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_3 >$sh_45hours_nl)`
  - **Comp_perTU**: `0.70`
  - **Output_Var**: `lhwsr_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 22. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ysemy > 0)  & (lma=0) & (lmcee_s = 0) & (yse>0)`
  - **Tax Unit:** `tu_individual_nl`

### 23. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(lindi = 5) & (dgn = 1) & (i_mc_rand_1 < $sh_mcse_l4_dgn1)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lmcse_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 24. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lmcse_s = 1)`
  - **Tax Unit:** `tu_individual_nl`

### 25. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_2> $sh_mcsemy_9)`
  - **Comp_perTU**: `min (10, ysemy)`
  - **Output_Var**: `bwkmcsemy_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 26. Function: ArithOp
  **Formula:** `ysemy - bwkmcsemy_s`
  **Output Variable:** `ysemwmy_s`
  **Tax Unit:** `tu_individual_nl`

### 27. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(bwkmcsemy_s > 0)`
  - **Tax Unit:** `tu_individual_nl`

### 28. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_3 >$sh_45hours_se)`
  - **Comp_perTU**: `0.70`
  - **Output_Add_Var**: `lhwsr_s`
  - **TAX_UNIT**: `tu_individual_nl`

### 29. Function: DefConst
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
  - `Run_Cond`: n/a

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
  - `$sh_0hours_nl`: 0
  - `$sh_15hours_nl`: 0
  - `$sh_45hours_nl`: 0
  - `$sh_hours_nl`: n/a
  - `Run_Cond`: GetDataIncomeYear!=2019

### 31. Function: DefConst
  **Constants Defined:**
  - `$er_dgn0_deh1_nl`: 0
  - `$er_dgn0_deh2_nl`: 0
  - `$er_dgn0_deh3_nl`: 0
  - `$er_dgn1_deh1_nl`: 0
  - `$er_dgn1_deh2_nl`: 0
  - `$er_dgn1_deh3_nl`: 0
  - `$ur_dgn0_deh1_nl`: 0
  - `$ur_dgn0_deh2_nl`: 0
  - `$ur_dgn0_deh3_nl`: 0
  - `$ur_dgn1_deh1_nl`: 0
  - `$ur_dgn1_deh2_nl`: 0
  - `$ur_dgn1_deh3_nl`: 0
  - `$er_dgn0_se`: 0
  - `$er_dgn1_se`: 0
  - `$er_yemmy2`: 0
  - `$er_yemmy5`: 0
  - `$er_yemmy8`: 0
  - `$ur_yemmy2`: 0
  - `$ur_yemmy5`: 0
  - `$ur_yemmy8`: 0
  - `Run_Cond`: GetDataIncomeYear!=2019


---
