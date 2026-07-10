# EUROMOD Tax-Benefit Rules for HU_2025

## Policy: uprate_hu
### 1. Function: Uprate
  - **Dataset**: `*_hhot`
  - **WarnIfNoFactor**: `no`
  - **Def_Factor**: `1`

### 2. Function: Uprate *(Switch: off)*
  - **Dataset**: `hu_20??_??_*`
  - **yem**: `$f_hourly_wage`
  - **yse**: `$f_hourly_wage`
  - **poa**: `$f_poa`
  - **poa01**: `$f_poa`
  - **poa02**: `$f_poa`
  - **psu**: `$f_psu`
  - **bfa**: `$f_bfa`
  - **bfaot**: `$f_bfa`
  - **bfant01**: `$f_bfa`
  - **bfant02**: `$f_bfa`
  - **bfamt**: `$f_bfa`
  - **bun**: `$f_bun`
  - **bunmt**: `$f_bun`
  - **bunct**: `$f_bun`
  - **bhl**: `$f_bhl`
  - **phl**: `$f_bhl`
  - **pdi**: `$f_pdi`
  - **afc**: `$f_afc`
  - **bed**: `$f_bed`
  - **bho**: `$f_bsa`
  - **botre**: `$f_cpi`
  - **bsa**: `$f_bsa`
  - **bsamt**: `$f_bsa`
  - **bsant**: `$f_bsa`
  - **kfb**: `$f_afc`
  - **kivho**: `$f_afc`
  - **tad**: `$f_cpi`
  - **tin**: `$f_const`
  - **tis**: `$f_cpi`
  - **tpr**: `$f_cpi`
  - **tscee**: `$f_const`
  - **tscer**: `$f_const`
  - **tscse**: `$f_const`
  - **xhc**: `$f_cpi`
  - **xhcmomi**: `$f_cpi`
  - **xhcot**: `$f_cpi`
  - **xhcrt**: `$f_cpi`
  - **xmp**: `$f_cpi`
  - **xpp**: `$f_cpi`
  - **yds**: `$f_const`
  - **yivwg**: `$f_hourly_wage`
  - **yiy**: `$f_cpi`
  - **yot**: `$f_cpi`
  - **ypp**: `$f_cpi`
  - **yprrt**: `$f_cpi`
  - **AggVar_Name**: `ypr`
  - **AggVar_Part**: `yprrt`
  - **ypt**: `$f_hourly_wage`
  - **yptmp**: `$f_hourly_wage`
  - **yempv**: `$f_hourly_wage`
  - **yempv_a**: `$f_hourly_wage`
  - **yem_a**: `$f_hourly_wage`
  - **yem18_a**: `$f_hourly_wage`
  - **yem19_a**: `$f_hourly_wage`
  - **yem20_a**: `$f_hourly_wage`
  - **ydses_o**: `$f_const`
  - **kfbcc**: `$f_afc`
  - **yemdt**: `$f_hourly_wage`
  - **xed00**: `$f_cpi`
  - **xhl00**: `$f_cpi`

### 3. Function: Uprate
  - **Dataset**: `hu_20??_??_*`
  - **Factor_Condition**: `lindi <= 0 `
  - **yem**: `$f_hourly_wage`
  - **yse**: `$f_hourly_wage`
  - **poa**: `$f_poa`
  - **poa01**: `$f_poa`
  - **poa02**: `$f_poa`
  - **psu**: `$f_psu`
  - **bfa**: `$f_bfa`
  - **bfaot**: `$f_bfa`
  - **bfant01**: `$f_bfa`
  - **bfant02**: `$f_bfa`
  - **bfamt**: `$f_bfa`
  - **bun**: `$f_bun`
  - **bunmt**: `$f_bun`
  - **bunct**: `$f_bun`
  - **bhl**: `$f_bhl`
  - **phl**: `n/a`
  - **pdi**: `$f_pdi`
  - **afc**: `$f_afc`
  - **bed**: `$f_bed`
  - **bho**: `$f_bsa`
  - **botre**: `$f_cpi`
  - **bsa**: `$f_bsa`
  - **bsamt**: `$f_bsa`
  - **bsant**: `$f_bsa`
  - **kfb**: `$f_afc`
  - **kivho**: `$f_afc`
  - **tad**: `$f_cpi`
  - **tin**: `$f_const`
  - **tis**: `$f_cpi`
  - **tpr**: `$f_cpi`
  - **tscee**: `$f_const`
  - **tscer**: `$f_const`
  - **tscse**: `$f_const`
  - **xhc**: `$f_cpi`
  - **xhcmomi**: `$f_cpi`
  - **xhcot**: `$f_cpi`
  - **xhcrt**: `$f_cpi`
  - **xmp**: `$f_cpi`
  - **xpp**: `$f_cpi`
  - **yds**: `$f_const`
  - **yivwg**: `$f_hourly_wage`
  - **yiy**: `$f_cpi`
  - **yot**: `$f_cpi`
  - **ypp**: `$f_cpi`
  - **yprrt**: `$f_cpi`
  - **AggVar_Name**: `ypr`
  - **AggVar_Part**: `yprrt`
  - **ypt**: `$f_hourly_wage`
  - **yptmp**: `$f_hourly_wage`
  - **yempv**: `$f_hourly_wage`
  - **yempv_a**: `$f_hourly_wage`
  - **yem_a**: `$f_hourly_wage`
  - **yem18_a**: `$f_hourly_wage`
  - **yem19_a**: `$f_hourly_wage`
  - **yem20_a**: `$f_hourly_wage`
  - **ydses_o**: `$f_const`
  - **kfbcc**: `$f_afc`
  - **yemdt**: `$f_yemLead`
  - **xed00**: `$f_cpi`
  - **xhl00**: `$f_cpi`

### 4. Function: Uprate
  - **Dataset**: `hu_20??_??_*`
  - **xhl01**: `$f_cpi`


---

## Policy: Ildef_hu
### 1. Function: DefIl
  - **name**: `il_taxprogY`
  - **bed**: `+`
  - **bcclt_s**: `+`
  - **bccnc_s**: `+`
  - **poa**: `+`
  - **bmanc_s**: `+`
  - **bchnm_s**: `+`

### 2. Function: DefIl
  - **name**: `il_totalY`
  - **bcclt_s**: `+`
  - **bccnc_s**: `+`
  - **bed**: `+`
  - **phl**: `n/a`
  - **bunct_s**: `+`
  - **yem**: `+`
  - **yiy**: `+`
  - **ypr**: `+`
  - **yse**: `+`
  - **bhl**: `+`
  - **bunnc_s**: `+`
  - **bwkmcee_s**: `+`
  - **yemmc_s**: `+`

### 3. Function: DefIl
  - **name**: `il_wageY`
  - **phl**: `n/a`
  - **bunct_s**: `+`
  - **yem**: `+`
  - **bhl**: `+`
  - **bunnc_s**: `+`
  - **yemmc_s**: `+`

### 4. Function: DefIl
  - **name**: `il_meanstestY`
  - **bcclt_s**: `+`
  - **bccnc_s**: `+`
  - **bchnm_s**: `+`
  - **bmanc_s**: `+`
  - **tscee_s**: `-`
  - **tin_s**: `-`
  - **tbs_s**: `n/a`
  - **tscse_s**: `-`
  - **pdi**: `+`
  - **bed**: `+`
  - **phl**: `n/a`
  - **bunct_s**: `+`
  - **yem**: `+`
  - **yiy**: `+`
  - **yot**: `+`
  - **poa**: `+`
  - **ypr**: `+`
  - **ypp**: `+`
  - **ypt**: `+`
  - **psu**: `+`
  - **botre**: `+`
  - **yse**: `+`
  - **bhl**: `+`
  - **yselo_s**: `n/a`
  - **bunnc_s**: `+`
  - **tis_s**: `-`
  - **bwkmcee_s**: `+`
  - **yemmc_s**: `+`

### 5. Function: DefIl
  - **name**: `il_meanstestY1`
  - **bcclt_s**: `+`
  - **bccnc_s**: `+`
  - **bchnm_s**: `+`
  - **bchmt_s**: `+`
  - **bmanc_s**: `+`
  - **tscee_s**: `-`
  - **tin_s**: `-`
  - **tbs_s**: `n/a`
  - **tscse_s**: `-`
  - **pdi**: `+`
  - **bed**: `+`
  - **phl**: `n/a`
  - **bunct_s**: `+`
  - **yem**: `+`
  - **yiy**: `+`
  - **yot**: `+`
  - **poa**: `+`
  - **ypr**: `+`
  - **ypp**: `+`
  - **ypt**: `+`
  - **psu**: `+`
  - **botre**: `+`
  - **yse**: `+`
  - **bhl**: `+`
  - **yselo_s**: `n/a`
  - **bunnc_s**: `+`
  - **bfaot_s**: `n/a`
  - **bfaot**: `+`
  - **tis_s**: `-`
  - **yemmc_s**: `+`
  - **bwkmcee_s**: `+`

### 6. Function: DefIl
  - **name**: `il_sareexclY`
  - **bcclt_s**: `+`
  - **bccnc_s**: `+`
  - **poamt_s**: `+`
  - **pdi**: `+`
  - **phl**: `n/a`
  - **bunct_S**: `+`
  - **yem**: `+`
  - **poa**: `+`
  - **psu**: `+`
  - **yse**: `+`
  - **bhl**: `+`
  - **bunnc_s**: `+`
  - **bwkmcee_s**: `+`
  - **yemmc_s**: `+`

### 7. Function: DefIl
  - **name**: `il_taxableY`
  - **il_tinty**: `+`
  - **tinta_s**: `-`

### 8. Function: DefIl
  - **Name**: `il_tinty`
  - **il_taxprogY**: `n/a`
  - **bhl**: `+`
  - **phl**: `n/a`
  - **bunct_s**: `+`
  - **ypr**: `+`
  - **yse**: `+`
  - **yem**: `+`
  - **bunnc_s**: `n/a`
  - **yemmc_s**: `+`
  - **bwkmcee_s**: `+`

### 9. Function: DefIl
  - **Name**: `il_pencontr`
  - **bunct_s**: `+`
  - **yem**: `+`


---

## Policy: TUDef_hu
### 1. Function: DefTu
  - **Name**: `tu_hh_oecd_co`
  - **Type**: `HH`
  - **DepChildCond**: `(dag<14)`

### 2. Function: DefTu
  - **Name**: `tu_household_hu`
  - **Type**: `HH`
  - **DepChildCond**: `(dag<=15) | (((dag<=24) & (dec>=3) & (dec<=4)) & !(IsWithPartner) & !(IsMarried))`
  - **LoneParentCond**: `(Default) & !(IsMarried)`

### 3. Function: DefTu
  - **Name**: `tu_individual_hu`
  - **Type**: `IND`
  - **DepChildCond**: `(dag<=15) | (((dag<=24) & (dec>=3) & (dec<=4)) & !(IsWithPartner) & !(IsMarried))`
  - **LoneParentCond**: `(Default) & !(IsMarried)`

### 4. Function: DefTu
  - **Name**: `tu_cbfam_hu`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `!(IsParent) & ((dag<=15) | (((dag<=24) & (dec>=3) & (dec<=4)) & !(IsWithPartner) & !(IsMarried)))`
  - **LoneParentCond**: `(Default) & !(IsMarried)`

### 5. Function: DefTu
  - **Name**: `tu_ccfam_hu`
  - **type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild & DepParent`
  - **DepChildCond**: `!(IsParent) & ((dag<=2) | ((dag<=9) & (IsDisabled)))`
  - **LoneParentCond**: `(Default) & !(IsMarried)`
  - **AssignDepChOfDependents**: `yes`

### 6. Function: DefTu
  - **Name**: `tu_cpfam_hu`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild`
  - **DepChildCond**: `!(IsParent) & ((dag<=17) | ((dag<=25) & (dec=6)) | ((dag<=23) & (dec>=3) & (dec<=4))) & !(IsWithPartner) & !(IsMarried)`
  - **AssignDepChOfDependents**: `yes`

### 7. Function: DefTu
  - **Name**: `tu_couple_hu`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner`

### 8. Function: DefTu
  - **Name**: `tu_asfam1_hu`
  - **Type**: `SUBGROUP`
  - **Members**: `Partner & OwnDepChild & DepParent`
  - **DepChildCond**: `!(IsParent) & !(IsWithPartner) & !(IsMarried) & ((dag<16) |  ((dag<=20) & (dec>0) & ((yem#1=0)  | (yse#1=0))) | ((dag<24) & (dec>=3) & ((yem#1=0)  | (yse#1=0)) ) )`
  - **#_level**: `tu_individual_hu`
  - **AssignDepChOfDependents**: `yes`
  - **LoneParentCond**: `(Default) & !(IsMarried)`
  - **NoChildIfHead**: `yes`


---

## Policy: ConstDef_hu
### 1. Function: DefConst
  **Constants Defined:**
  - `$MinPension_m`: 28500#m
  - `$MinWage_m`: 290800#m
  - `$MinWage_net`: n/a
  - `$PenAge`: 65
  - `$PenAgeFem`: 65
  - `$HBTUWAWork`: 1
  - `$HBTUWANowork`: 1
  - `$HBTUPen`: 1

### 2. Function: DefConst
  **Constants Defined:**
  - `$UB_QperMin`: 12
  - `$UB_QperTot`: 36
  - `$Imputedwage`: 0
  - `$Nwh`: 40

### 3. Function: DefConst
  **Constants Defined:**
  - `$lhw`: 40

### 4. Function: DefConst
  **Constants Defined:**
  - `$mc_rrate`: 0.7
  - `$mc_share`: 1
  - `$mc_amount`: n/a
  - `$mc_min`: n/a
  - `$mc_max`: n/a

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

## Policy: neg_hu
### 1. Function: DefVar
  - **i_yse0**: `0`

### 2. Function: ArithOp
  **Formula:** `yse`
  **Output Variable:** `i_yse0`
  **Tax Unit:** `tu_individual_hu`

### 3. Function: Max
  - **val**: `0`
  - **output_var**: `yse`
  - **TAX_UNIT**: `tu_individual_hu`

### 4. Function: BenCalc
  - **Comp_Cond**: `(yse<5000#m)`
  - **Comp_perTU**: `(-yse)`
  - **Output_Add_Var**: `yse`
  - **TAX_UNIT**: `tu_individual_hu`
  - **#_DataBasename**: `HU_2017_a?`
  - **Run_Cond**: `(IsUsedDatabase#1)`


---

## Policy: yem_hu *(Switch: off)*
### 1. Function: DefConst
  **Constants Defined:**
  - `$Nwh`: 40
  - `const_monetary`: no

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yem > 0)`
  - **Tax Unit:** `tu_individual_hu`

### 3. Function: Max
  - **who_must_be_elig**: `one`
  - **val**: `$MinWage_m*min(lhw,$Nwh)/$Nwh*yemmy/12`
  - **output_var**: `yem`
  - **TAX_UNIT**: `tu_individual_hu`

### 4. Function: ChangeParam
  - **Param_Id**: `0083b801-b870-4c7f-abcb-cbb75819def7`
  - **Param_NewVal**: `hu_2025_yem_std`


---

## Policy: bun_hu
### 1. Function: DefVar
  - **maxbunmy_s**: `0`
  - **var_monetary**: `no`
  - **bunct03_s**: `0`
  - **bunct01_s**: `0`

### 2. Function: ArithOp
  **Formula:** `3`
  **Output Variable:** `maxbunmy_s`
  **Tax Unit:** `tu_individual_hu`

### 3. Function: ArithOp
  **Formula:** `min(maxbunmy_s,lunmy_s)`
  **Output Variable:** `bunmy_s`
  **Tax Unit:** `tu_individual_hu`

### 4. Function: BenCalc
  - **comp_cond**: `(lunmy_s > 0) & (bun = 0)`
  - **comp_perElig**: `0`
  - **output_var**: `yempv_s`
  - **TAX_UNIT**: `tu_individual_hu`
  - **Comp_Cond**: `(lunmy_s > 0) & (bun > 0) & ($ImputedWage = 1)`
  - **Comp_perElig**: `yivwg * $Nwh * 52/12`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lunmy_s > 0) & (liwmy_s >= $UB_QperMin) & (poa = 0) & (bhl=0) & (pdi=0)`
  - **Tax Unit:** `tu_individual_hu`

### 6. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 7. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `(bunmy_s > 3)`
  - **comp_perTU**: `(60% * yempv_s * 3)`
  - **comp_lowlim**: `100% * $MinWage_m * bunmy_s`
  - **comp_uplim**: `$MinWage_m * 3`
  - **output_var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_hu`
  - **Comp_LowLim**: `100% * $MinWage_m * 3`

### 8. Function: ArithOp
  **Formula:** `bunct_s / 12`
  **Output Variable:** `bunct_s`
  **Tax Unit:** `tu_individual_hu`

### 9. Function: BenCalc
  - **comp_cond**: `(dgn=0)`
  - **comp_perElig**: `$PenAge - dag`
  - **output_var**: `sin05_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 10. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 11. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 12. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 13. Function: BenCalc *(Switch: n/a)*
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`
  - **Result_Var**: `n/a`
  - **LowLim**: `n/a`

### 14. Function: BenCalc
  - **comp_cond**: `(yempv_s>=$MinWage_m) & (lunmy_s>0) & (bunct_s>0) & (bunmy_s >= 1.5) & (lunmy_s > maxbunmy_s) & (les = 5) & (sin05_s<=5)`
  - **comp_perTU**: `(40%*$MinWage_m)*min(lunmy_s-1.5,12)/12`
  - **output_var**: `bunnc_s`
  - **TAX_UNIT**: `tu_individual_hu`
  - **Comp_perTU**: `(40%*yempv_s)*min(lunmy_s-1.5,12)/12`
  - **Comp_Cond**: `(yempv_s<$MinWage_m) & (lunmy_s>0) & (bunct_s>0) & (bunmy_s >= 1.5) & (lunmy_s > maxbunmy_s) & (les = 5) & (sin05_s<=5)`
  - **LowLim**: `0`

### 15. Function: ArithOp
  **Formula:** `max(lunmy,bunmy)`
  **Output Variable:** `lunmy_s`
  **Tax Unit:** `tu_individual_hu`

### 16. Function: ArithOp
  **Formula:** `min(liwmy*$UB_QperTot/12,liwwh)`
  **Output Variable:** `liwmy_s`
  **Tax Unit:** `tu_individual_hu`

### 17. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `(ils_earns = 0) | (bun > 0)`
  - **comp_perElig**: `lunmy_s`
  - **output_var**: `lunmy_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 18. Function: Elig
  **Eligibility Check:**
  - **Condition:** `lunmy_s>0 & liwwh36_h>=$UB_QperMin & poa=0 & bhl=0 & pdi=0`
  - **Tax Unit:** `tu_individual_hu`

### 19. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `bunmy_s>3`
  - **comp_perTU**: `(60% * yempv * 3)`
  - **comp_lowlim**: `60% * $MinWage_m * bunmy_s`
  - **comp_uplim**: `$MinWage_m * 3`
  - **Comp_LowLim**: `60% * $MinWage_m * 3`
  - **output_var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 20. Function: BenCalc
  - **Comp_Cond**: `(lunmy_s > 0) & (bun = 0)`
  - **Comp_perElig**: `0`
  - **Output_Var**: `liwmy_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 21. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **comp_cond**: `bunmy_s>3 & bunmy_s <=6`
  - **comp_perTU**: `60% * yempv`
  - **comp_lowlim**: `60% * $MinWage_m`
  - **comp_uplim**: `$MinWage_m`
  - **Comp_LowLim**: `60% * $MinWage_m`
  - **Comp_Cond**: `bunmy_s > 6`
  - **Comp_perTU**: `0`
  - **output_var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 22. Function: BenCalc
  - **Comp_Cond**: `bunmy_s<lunmy_s`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bunct_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 23. Function: BenCalc
  - **Comp_Cond**: `(lunmy_s>0) & (bunct_s>0) & (bunmy_s >= 1.5) & (lunmy_s > maxbunmy_s) & (les = 5) & (sin05_s<=5)`
  - **Comp_perTU**: `40%*$MinWage_m`
  - **Output_Var**: `bunnc_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 24. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `(yempv>=$MinWage_m) & (lunmy_s>0) & (bunct_s>0) & (bunmy_s >= 1.5) & (lunmy_s > maxbunmy_s) & (les = 5) & (sin05_s<=5)`
  - **comp_perTU**: `(40%*$MinWage_m)*min(lunmy_s-1.5,12)/12`
  - **output_var**: `bunnc_s`
  - **TAX_UNIT**: `tu_individual_hu`
  - **LowLim**: `0`
  - **Comp_perTU**: `(40%*yempv)*min(lunmy_s-1.5,12)/12`
  - **Comp_Cond**: `(yempv<$MinWage_m) & (lunmy_s>0) & (bunct_s>0) & (bunmy_s >= 1.5) & (lunmy_s > maxbunmy_s) & (les = 5) & (sin05_s<=5)`


---

## Policy: bmanc_hu
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(dag=0)`
  - **Tax Unit:** `tu_cbfam_hu`

### 2. Function: ArithOp
  **Formula:** `$MinPension_m/12 * 2.25`
  **Output Variable:** `bmanc_s`
  **Tax Unit:** `tu_cbfam_hu`


---

## Policy: bccnc_hu
### 1. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `( !(IsDepChild) & (bun=0)) & (((nDepChInTu#1>0) & (IsParentOfDepChild) & (dgn=0) & (lhw=0)) | ((nDepChInTu#2>0) & (IsParentOfDepChild) & (dgn=0)))`
  - **Tax Unit:** `tu_ccfam_hu`

### 3. Function: ArithOp
  **Formula:** `$MinPension_m`
  **Output Variable:** `bccnc_s`
  **Tax Unit:** `tu_ccfam_hu`


---

## Policy: bcclt_hu
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `!(IsDepChild) & ((nDepChInTu>=3) & (nDepChInTu#1>0) & (nDepChInTu#2=0))`
  - **Tax Unit:** `tu_cbfam_hu`

### 2. Function: ArithOp
  **Formula:** `$MinPension_m`
  **Output Variable:** `bcclt_s`
  **Tax Unit:** `tu_cbfam_hu`


---

## Policy: bchnm_hu
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(IsLoneParentOfDepChild)`
  - **Tax Unit:** `tu_cbfam_hu`

### 2. Function: BenCalc
  - **who_must_be_elig**: `one_member`
  - **comp_cond**: `(IsDisabled) & (IsDepChild)`
  - **comp_perElig**: `25900#m`
  - **output_var**: `bchnm_s`
  - **TAX_UNIT**: `tu_cbfam_hu`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(bchnm_s = 0)`
  - **Tax Unit:** `tu_cbfam_hu`

### 4. Function: BenCalc
  - **who_must_be_elig**: `all_members`
  - **comp_cond**: `(IsDisabled) & (IsDepChild)`
  - **comp_perElig**: `23300#m`
  - **output_add_var**: `bchnm_s`
  - **TAX_UNIT**: `tu_cbfam_hu`


---

## Policy: tscee_hu
### 1. Function: DefVar
  - **tscee00_s**: `0`
  - **i_tinta01_s**: `0`
  - **i_sicred**: `n/a`

### 2. Function: BenCalc
  - **comp_cond**: `(poa>0) & (yem>0)`
  - **comp_perElig**: `0`
  - **result_var**: `n/a`
  - **Output_Var**: `tsceehl_s`
  - **TAX_UNIT**: `tu_individual_hu`
  - **LowLim**: `0`

### 3. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `(poa>0) & (yem>0)`
  - **comp_perElig**: `0`
  - **TAX_UNIT**: `tu_individual_hu`
  - **Output_Var**: `tscee00_s`
  - **LowLim**: `n/a`

### 4. Function: BenCalc
  - **Comp_Cond**: `(i_tinta00_s>0) & (yem=0)`
  - **Comp_perTU**: `i_tinta00_s`
  - **Output_Var**: `i_tinta01_s`
  - **TAX_UNIT**: `tu_individual_hu`
  - **LowLim**: `0`

### 5. Function: BenCalc
  - **Comp_Cond**: `(poa>0) & (yem>0)`
  - **TAX_UNIT**: `tu_individual_hu`
  - **LowLim**: `0`
  - **Comp_perTU**: `0`
  - **UpLim**: `n/a`
  - **Output_Var**: `tsceepi_s`

### 6. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `(poa>0) & (yem>0)`
  - **comp_perElig**: `(yem * 0.04) - i_tinta00_s`
  - **LowLim**: `0`
  - **Comp_Cond**: `(yem>0) & (lindi=5) | (lindi=6)`
  - **Comp_perElig**: `((yem * 0.07) - i_tinta00_s)*8/12+7710*4/12`
  - **Output_Var**: `tsceehl_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 7. Function: BenCalc *(Switch: n/a)*
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Comp_perElig**: `n/a`
  - **LowLim**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 8. Function: BenCalc
  - **comp_cond**: `(poa>0) & (yem>0)`
  - **comp_perElig**: `0`
  - **Comp_Cond**: `(poa=0) & (yem>0) & (lindi=5) | (lindi=6)`
  - **Comp_perElig**: `yem * 0.015 *8/12`
  - **Output_Var**: `tscee00_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 9. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 10. Function: ArithOp
  **Formula:** `tsceepi_s+tsceehl_s+tscee00_s`
  **Output Variable:** `tscee_s`
  **Tax Unit:** `tu_individual_hu`

### 11. Function: DefConst
  **Constants Defined:**
  - `$tscee_hlt_rt1`: 7%
  - `$tscee_hlt_rt2`: 0
  - `$tscee_pen_rt1`: 10%
  - `$tscee_unemp_rt1`: 1.5%


---

## Policy: tscer_hu
### 1. Function: DefVar *(Switch: off)*
  - **tscerge_s**: `0`

### 2. Function: ArithOp *(Switch: off)*
  **Formula:** `yem * 0.24`
  **Output Variable:** `tscer_s`
  **Tax Unit:** `tu_individual_hu`

### 3. Function: ArithOp *(Switch: off)*
  **Formula:** `yem * 0.02`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_hu`

### 4. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **result_var**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 5. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `n/a`
  - **Tax Unit:** `n/a`

### 6. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** ``
  **Tax Unit:** `n/a`

### 7. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 8. Function: ArithOp *(Switch: off)*
  **Formula:** `yem * 0.01`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_hu`

### 9. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **Output_Add_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 10. Function: ArithOp
  **Formula:** `yem * 0.13`
  **Output Variable:** `tscer_s`
  **Tax Unit:** `tu_individual_hu`

### 11. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `(yem>0) & (lindi=6)`
  - **Comp_perTU**: `yem * 0.175`
  - **Comp_perElig**: `yem * 0.175*8/12`
  - **Output_Var**: `tscer_s`
  - **TAX_UNIT**: `tu_individual_hu`


---

## Policy: tscse_hu
### 1. Function: DefVar
  - **tscsege_s**: `0`
  - **i_contbase**: `0`
  - **tscsehlfx_s**: `0`
  - **tscsehl00_s**: `0`
  - **semp_sel**: `0`
  - **tscsepiee_s**: `0`
  - **tscsepier_s**: `0`
  - **tscsest_s**: `0`
  - **i_tinta03_s**: `0`
  - **i_tinta02_s**: `0`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `!(yse=0) & (lse=2)`
  - **Tax Unit:** `tu_individual_hu`

### 3. Function: BenCalc
  - **elig_var**: `semp_sel`
  - **who_must_be_elig**: `one_member`
  - **comp_cond**: `(poa=0) & (tscee_s>0) & (lse00=0)`
  - **comp_perElig**: `yse`
  - **comp_lowlim**: `$MinWage_m`
  - **lowlim**: `0`
  - **output_var**: `i_contbase`
  - **TAX_UNIT**: `tu_individual_hu`

### 4. Function: BenCalc *(Switch: n/a)*
  - **elig_var**: `n/a`
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **comp_uplim**: `n/a`
  - **result_var**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 5. Function: BenCalc *(Switch: off)*
  - **elig_var**: `semp_sel`
  - **who_must_be_elig**: `one_member`
  - **comp_cond**: `(poa=0) & (tscee_s>0) & (lse00=0)`
  - **comp_perElig**: `0`
  - **result_var**: `tscsepier_s`
  - **output_add_var**: `tscse_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 6. Function: BenCalc
  - **elig_var**: `semp_sel`
  - **who_must_be_elig**: `one_member`
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **result_var**: `tscsege_s`
  - **output_add_var**: `tscse_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 7. Function: BenCalc *(Switch: off)*
  - **elig_var**: `semp_sel`
  - **who_must_be_elig**: `one_member`
  - **comp_cond**: `(poa=0) & (tscee_s>0) & (lse00=0)`
  - **comp_perElig**: `0`
  - **result_var**: `tscsehl00_s`
  - **output_add_var**: `tscse_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 8. Function: BenCalc *(Switch: n/a)*
  - **elig_var**: `n/a`
  - **who_must_be_elig**: `n/a`
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **result_var**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

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
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 12. Function: ArithOp
  **Formula:** `i_contbase * 0.13`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_hu`

### 13. Function: BenCalc
  - **elig_var**: `semp_sel`
  - **who_must_be_elig**: `one_member`
  - **comp_cond**: `(poa=0) & (lse00=0)`
  - **comp_perElig**: `0`
  - **result_var**: `tscsehl00_s`
  - **Output_Var**: `tscse_s`
  - **TAX_UNIT**: `tu_individual_hu`
  - **LowLim**: `0`

### 14. Function: BenCalc
  - **Comp_Cond**: `(i_tinta02_s>0) & (semp_sel>0) & (poa>0)`
  - **Comp_perTU**: `i_tinta02_s`
  - **Output_Var**: `i_tinta03_s`
  - **TAX_UNIT**: `tu_individual_hu`
  - **LowLim**: `0`

### 15. Function: BenCalc
  - **Comp_Cond**: `(i_tinta01_s>0) & (yem =0)`
  - **Comp_perTU**: `i_tinta01_s`
  - **Output_Var**: `i_tinta02_s`
  - **TAX_UNIT**: `tu_individual_hu`
  - **LowLim**: `0`

### 16. Function: BenCalc
  - **elig_var**: `semp_sel`
  - **who_must_be_elig**: `one_member`
  - **comp_cond**: `(poa=0) & (tscee_s>0) & (lse00=0)`
  - **comp_perElig**: `0`
  - **comp_uplim**: `21700#d`
  - **result_var**: `tscsepiee_s`
  - **Output_Add_Var**: `tscse_s`
  - **TAX_UNIT**: `tu_individual_hu`
  - **LowLim**: `0`


---

## Policy: tin_hu
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lse00=1)`
  - **Tax Unit:** `tu_individual_hu`

### 2. Function: ArithOp
  **Formula:** `il_taxableY - yse*sel_s`
  **Output Variable:** `sin01_s`
  **Tax Unit:** `tu_individual_hu`

### 3. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 4. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** `n/a`

### 5. Function: ArithOp
  **Formula:** `sin01_s * $tin_rate`
  **Output Variable:** `tin_s`
  **Tax Unit:** `tu_individual_hu`

### 6. Function: SchedCalc *(Switch: n/a)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `n/a`
  - **Output Variable:** `n/a`

### 7. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 8. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **lowlim**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 9. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 10. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 11. Function: DefVar *(Switch: off)*
  - **tintcee01_s**: `0`

### 12. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **uplim**: `n/a`
  - **lowlim**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 13. Function: BenCalc
  - **comp_cond**: `(ddi=1)`
  - **comp_perElig**: `$MinWage_m*0.05`
  - **output_var**: `tintchl_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 14. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perTU**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 15. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 16. Function: ArithOp *(Switch: off)*
  **Formula:** `tintchl_s`
  **Output Variable:** `tintc_s`
  **Tax Unit:** `tu_individual_hu`

### 17. Function: ArithOp *(Switch: off)*
  **Formula:** `tin_s-tintc_s`
  **Output Variable:** `sin03_s`
  **Tax Unit:** `tu_individual_hu`

### 18. Function: Allocate *(Switch: off)*
  - **share**: `sin02_s`
  - **share_prop**: `sin03_s`
  - **share_equ_ifzero**: `yes`
  - **output_var**: `tintcch_s`
  - **TAX_UNIT**: `tu_couple_hu`

### 19. Function: ArithOp
  **Formula:** `tintchl_s + i_tintcfam_s`
  **Output Variable:** `tintc_s`
  **Tax Unit:** `tu_individual_hu`

### 20. Function: ArithOp
  **Formula:** `tin_s-tintc_s`
  **Output Variable:** `tin_s`
  **Tax Unit:** `tu_individual_hu`

### 21. Function: ArithOp *(Switch: off)*
  **Formula:** `yiydv * 0.2`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_hu`

### 22. Function: BenCalc
  - **comp_cond**: `(nDepChInTU>=3)`
  - **comp_perTU**: `nDepChInTU*220000#m`
  - **output_var**: `sin04_s`
  - **TAX_UNIT**: `tu_cbfam_hu`
  - **Result_Var**: `n/a`

### 23. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 24. Function: Allocate
  - **Share**: `sin04_s`
  - **Output_Var**: `tinta_s`
  - **TAX_UNIT**: `tu_cbfam_hu`
  - **Share_All_IfNoElig**: `yes`
  - **Share_Between**: `il_tinty#1>0 & !IsDepChild`
  - **Result_Var**: `i_tintafam_s`
  - **#_Level**: `tu_individual_hu`

### 25. Function: DefVar
  - **tintcfa_s**: `0`

### 26. Function: BenCalc
  - **Comp_Cond**: `(nDepChildrenInTu#1>3) & (dgn=0)`
  - **#_Level**: `tu_cbfam_hu`
  - **Comp_perTU**: `tin_s`
  - **Output_Var**: `tintcfa_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 27. Function: ArithOp
  **Formula:** `tin_s-tintcfa_s`
  **Output Variable:** `tin_s`
  **Tax Unit:** `tu_individual_hu`

### 28. Function: Allocate *(Switch: off)*
  - **Share**: `sin04_s`
  - **Output_Add_Var**: `tinta_s`
  - **TAX_UNIT**: `tu_cbfam_hu`
  - **#_UpLim**: `809000#m`
  - **#_LowLim**: `0`
  - **Share_Between**: `(il_tinty>0)`

### 29. Function: SchedCalc *(Switch: off)*
  **Schedule Calculation:**
  - **Income Variable:** ``
  - **Tax Unit:** `tu_individual_hu`
  - **Output Variable:** ``
    - Band: Rate=`0.15`, Limit=``

### 30. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(dag< 25) & (il_tinty>0)`
  - **Tax Unit:** `tu_individual_hu`

### 31. Function: ArithOp
  **Formula:** `656785#m`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_hu`

### 32. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(i_tintafam_s>0) & (il_tinty>0)`
  - **Tax Unit:** `tu_individual_hu`

### 33. Function: DefVar
  - **Var_Monetary**: `no`
  - **i_tintafam_s**: `0`
  - **i_tintayp_s**: `0`
  - **i_tintcfam_s**: `0`
  - **i_famall**: `n/a`
  - **i_taxb**: `n/a`
  - **i_tintam_s**: `0`
  - **i_yngmth**: `0`
  - **i_hhnewborn**: `0`

### 34. Function: ArithOp
  **Formula:** `0#y`
  **Output Variable:** `i_tintcfam_s`
  **Tax Unit:** `tu_individual_hu`

### 35. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsParentOfDepChild & dgn=0 & (dag>= 25 & dag<30) & (il_tinty>0)`
  - **Tax Unit:** `tu_individual_hu`

### 36. Function: Elig
  **Eligibility Check:**
  - **Condition:** `nDepChildrenInTu#1>0`
  - **Tax Unit:** `tu_cbfam_hu`

### 37. Function: ArithOp
  **Formula:** `656785#m * i_yngmth * i_hhnewborn`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_hu`

### 38. Function: DefConst
  **Constants Defined:**
  - `$tin_rt`: 15%


---

## Policy: tbs_hu *(Switch: n/a)*
### 1. Function: DefVar *(Switch: n/a)*
  - **i_basetbs**: `0`

### 2. Function: Elig *(Switch: n/a)*
  **Eligibility Check:**
  - **Condition:** `(lse00=1)`
  - **Tax Unit:** `tu_individual_hu`

### 3. Function: ArithOp *(Switch: n/a)*
  **Formula:** `max(yse,$MinWage_m)`
  **Output Variable:** `i_basetbs`
  **Tax Unit:** `tu_individual_hu`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `i_basetbs * 0.37`
  **Output Variable:** `tbs_s`
  **Tax Unit:** `tu_individual_hu`


---

## Policy: bchmt_hu
### 1. Function: DefVar
  - **i_pcy**: `0`
  - **i_selbchmt**: `0`
  - **var_monetary**: `no`

### 2. Function: ArithOp
  **Formula:** `il_meanstestY / nPersInUnit`
  **Output Variable:** `sin01_s`
  **Tax Unit:** `tu_cpfam_hu`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(sin01_s < $MinPension_m*1.30) & (nDepChInTu>0)`
  - **Tax Unit:** `tu_cpfam_hu`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 5. Function: ArithOp
  **Formula:** `12000#y*nDepChildrenInTu`
  **Output Variable:** `bchmt_s`
  **Tax Unit:** `tu_cpfam_hu`


---

## Policy: bsa_hu
### 1. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **#_AgeMin**: `n/a`
  - **comp_perTU**: `n/a`
  - **#_AgeMax**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **result_var**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 2. Function: Allocate *(Switch: n/a)*
  - **share**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 3. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 4. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 5. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **comp_perElig**: `n/a`
  - **lowlim**: `n/a`
  - **uplim**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **result_var**: `n/a`
  - **output_add_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 6. Function: Elig *(Switch: off)*
  **Eligibility Check:**
  - **Condition:** `(dag >= 18) & (dag < 65) & (bunct_s = 0) & (bunnc_s = 0) & (yem = 0) & (yse <= 0) & (i_hhpercapitaY1#1 < $MinPension_m*0.9)`
  - **Tax Unit:** `tu_individual_hu`

### 7. Function: BenCalc *(Switch: off)*
  - **who_must_be_elig**: `one`
  - **base**: `$MinPension_m*0.95`
  - **comp_cond**: `(IsDepChild)`
  - **comp_perElig**: `$base*0.7`
  - **lowlim**: `0`
  - **uplim**: `69426#m`
  - **withdraw_base**: `il_meanstestY1`
  - **withdraw_rate**: `1`
  - **Output_Var**: `bsa00_s`
  - **TAX_UNIT**: `tu_asfam1_hu`

### 8. Function: BenCalc *(Switch: n/a)*
  - **comp_cond**: `n/a`
  - **#_level**: `n/a`
  - **#_AgeMax**: `n/a`
  - **comp_perElig**: `n/a`
  - **lowlim**: `n/a`
  - **uplim**: `n/a`
  - **withdraw_base**: `n/a`
  - **withdraw_rate**: `n/a`
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 9. Function: Elig
  **Eligibility Check:**
  - **Condition:** `((IsParentOfDepChild#1=1 & dag>=18 & dag<=55 & nDepChildrenInTu#1>0 & i_famwdisk!=0) | (dag>=18 & dag<$PenAge & ((ddi=1 | pdi>0) & (bunct_s=0 & bunnc_s=0)) )) & (yem=0 & yse<=0) & (il_sareexclY#1<=0)`
  - **Tax Unit:** `tu_individual_hu`

### 10. Function: Allocate *(Switch: n/a)*
  - **share**: `n/a`
  - **output_var**: `n/a`
  - **TAX_UNIT**: `n/a`

### 11. Function: ArithOp
  **Formula:** `il_meanstestY1/i_hhUscale`
  **Output Variable:** `i_hhpercapitaY1`
  **Tax Unit:** `tu_household_hu`

### 12. Function: Allocate *(Switch: off)*
  - **share**: `i_hhpercapitaY1 * nPersInTu`
  - **output_var**: `i_hhpercapitaY`
  - **TAX_UNIT**: `tu_household_hu`

### 13. Function: ArithOp *(Switch: n/a)*
  **Formula:** `n/a`
  **Output Variable:** `n/a`
  **Tax Unit:** `n/a`

### 14. Function: Elig *(Switch: off)*
  **Eligibility Check:**
  - **Condition:** `(i_hhpercapitaY <= ($MinPension_m*250%))`
  - **Tax Unit:** `tu_individual_hu`

### 15. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `(IsHead) & (i_hhpercapitaY1 > ($MinPension_m*50%)) & (i_hhpercapitaY1 <= ($MinPension_m*250%))`
  - **comp_perTU**: `min(xhc,sin06_s)*sin04_s`
  - **output_var**: `bsaho_s`
  - **TAX_UNIT**: `tu_household_hu`
  - **Who_Must_Be_Elig**: `one`

### 16. Function: ArithOp *(Switch: off)*
  **Formula:** `bsaho_s`
  **Output Variable:** ``
  **Tax Unit:** `tu_individual_hu`

### 17. Function: ArithOp
  **Formula:** `1+0.9*min(nAdultsInTu-1,1)+0.8*max(nAdultsInTu-2,0)+0.8*min(nDepChildrenInTu,2)+0.7*max(nDepChildrenInTu-2,0)`
  **Output Variable:** `i_hhUscale`
  **Tax Unit:** `tu_household_hu`

### 18. Function: BenCalc
  - **Comp_perTU**: `0.2`
  - **Comp_Cond**: `(IsLoneParent)`
  - **Output_Add_Var**: `i_hhUscale`
  - **TAX_UNIT**: `tu_household_hu`

### 19. Function: BenCalc *(Switch: off)*
  - **Comp_perTU**: `(65 + 5*(nPersInUnit-4)) * 450#m`
  - **Comp_Cond**: `(nPersInUnit > 4)`
  - **Output_Var**: `sin06_s`
  - **TAX_UNIT**: `tu_household_hu`

### 20. Function: BenCalc *(Switch: off)*
  - **Comp_perTU**: `0.3-(((i_hhpercapitaY1 - $MinPension_m*50%)/$MinPension_m)*0.15)`
  - **Comp_Cond**: `(i_hhpercapitaY1>($MinPension_m*50%)) & (i_hhpercapitaY1<=(250%*$MinPension_m))`
  - **Output_Var**: `sin04_s`
  - **TAX_UNIT**: `tu_household_hu`

### 21. Function: BenCalc *(Switch: off)*
  - **Comp_perTU**: `bsaho_s`
  - **Comp_Cond**: `(bsaho_s >= 2500#m)`
  - **Output_Var**: `bsaho_s`
  - **TAX_UNIT**: `tu_household_hu`

### 22. Function: BenCalc
  - **Comp_perTU**: `max(($MinPension_m*0.8)-(sin31_s),0)`
  - **Comp_Cond**: `(IsWithPartner) & (dag>=$PenAge)`
  - **Output_Var**: `sin32_s`
  - **TAX_UNIT**: `tu_individual_hu`
  - **UpLim**: `$MinPension_m*0.80`

### 23. Function: BenCalc
  - **Comp_perTU**: `max(($MinPension_m*0.95)-sin31_s,0)`
  - **Comp_Cond**: `!(IsWithPartner) & (dag>=$PenAge) & (dag<75)`
  - **Output_Var**: `sin33_s`
  - **TAX_UNIT**: `tu_individual_hu`
  - **UpLim**: `$MinPension_m*0.95`

### 24. Function: BenCalc
  - **Comp_perTU**: `max(($MinPension_m*1.3)-sin31_s,0)`
  - **Comp_Cond**: `!(IsWithPartner) & (dag>=75)`
  - **Output_Var**: `sin34_s`
  - **TAX_UNIT**: `tu_individual_hu`
  - **UpLim**: `$MinPension_m*1.30`

### 25. Function: ArithOp
  **Formula:** `sin32_s+sin33_s+sin34_s`
  **Output Variable:** `poamt_s`
  **Tax Unit:** `tu_couple_hu`

### 26. Function: Allocate
  - **Share**: `il_meanstestY1`
  - **Output_Var**: `sin31_s`
  - **TAX_UNIT**: `tu_couple_hu`

### 27. Function: BenCalc
  - **Comp_perTU**: `0`
  - **Comp_Cond**: `(il_meanstestY1<0)`
  - **Output_Var**: `sin30_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 28. Function: BenCalc *(Switch: off)*
  - **comp_cond**: `(IsHead) & (((dag >= $PenAge) & (dgn =1)) | ((dag >= $PenAgeFem) & (dgn =0))) & (bsa_s = 0)  & (($use_nontakeup = 0) | (i_rand_ind#1 <= $HBTUPen))`
  - **comp_perTU**: `bsaho_s`
  - **#_level**: `tu_individual_hu`
  - **output_var**: `bsaho_s`
  - **result_var**: `stm02_s`
  - **TAX_UNIT**: `tu_household_hu`

### 29. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `(bsa01_s>=0)`
  - **Comp_perElig**: `bsa00_s -  bsa01_s`
  - **Output_Var**: `bsa00_s`
  - **TAX_UNIT**: `tu_asfam1_hu`
  - **LowLim**: `0`

### 30. Function: DefVar
  - **bsa01_s**: `0`
  - **i_hhpercapitaY1**: `0`
  - **i_hhnumpercapitaY**: `0`
  - **i_hhpercapitaY**: `0`
  - **i_percapitaY**: `0`
  - **bsa03_s**: `0`
  - **bsa02_s**: `0`
  - **sel2_s**: `0`
  - **sel1_s**: `0`
  - **i_hhUscale**: `0`
  - **i_Uscale**: `0`
  - **Var_Monetary**: `no`
  - **i_diskid**: `0`
  - **i_famwdisk**: `0`
  - **i_sel_SAlowinc**: `0`

### 31. Function: ArithOp *(Switch: off)*
  **Formula:** `80% * $MinPension_m`
  **Output Variable:** `bsa01_s`
  **Tax Unit:** `tu_asfam1_hu`

### 32. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `(i_bsa_cumpers > $bsa_target_count & bsayn_a = -1)  | bsayn_a = 0`
  - **Comp_perTU**: `0`
  - **Output_Var**: `bsa_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 33. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `i_bsa_elig`
  - **SummingWeighted**: `yes`
  - **SortingVar**: `i_bsa_sort`
  - **OutputVar**: `i_bsa_cumpers`
  - **TAX_UNIT**: `tu_individual_hu`

### 34. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_target_count`: $sum_i_bsa_elig * $bsa_rate

### 35. Function: Totals *(Switch: off)*
  - **Agg**: `i_bsa_elig`
  - **Use_Weights**: `yes`
  - **Varname_Sum**: `$sum`
  - **TAX_UNIT**: `tu_individual_hu`

### 36. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_rate`: min($bsa_BCA_rate,$bsa_BTA_rate)

### 37. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_BCA_rate`: 0.759114473

### 38. Function: Totals *(Switch: off)*
  - **Agg**: `n/a`
  - **Use_Weights**: `n/a`
  - **Varname_Sum**: `n/a`
  - **TAX_UNIT**: `n/a`

### 39. Function: DefVar *(Switch: off)*
  - **i_bsa_bca_take**: `n/a`

### 40. Function: CumulativeSum *(Switch: off)*
  - **SummingVar**: `n/a`
  - **SummingWeighted**: `n/a`
  - **SortingVar**: `n/a`
  - **OutputVar**: `n/a`
  - **TAX_UNIT**: `n/a`

### 41. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_targetBCA_amt`: n/a

### 42. Function: BenCalc *(Switch: off)*
  - **Comp_Cond**: `bsa_s >= $bsa_minamt`
  - **Comp_perTU**: `1`
  - **Comp_perElig**: `i_bsa_sort`
  - **Output_Var**: `i_bsa_sort`
  - **TAX_UNIT**: `tu_individual_hu`

### 43. Function: DefVar *(Switch: off)*
  - **i_bsa_sort**: `i_bsa_rand`
  - **i_bsa_amt**: `bsa_s`
  - **i_bsa_elig**: `bsa_s > 0`
  - **i_bsa_cumexp**: `0`
  - **i_bsa_cumpers**: `0`

### 44. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_minamt`: 0

### 45. Function: DefConst *(Switch: off)*
  **Constants Defined:**
  - `$bsa_BTA_rate`: 1

### 46. Function: Elig
  **Eligibility Check:**
  - **Condition:** `IsDepChild#1 & (ddi=1 | pdi>0)`
  - **Tax Unit:** `tu_individual_hu`

### 47. Function: Allocate
  - **Share**: `i_diskid`
  - **Output_Var**: `i_famwdisk`
  - **TAX_UNIT**: `tu_asfam1_hu`

### 48. Function: ArithOp
  **Formula:** `bsa00_s + bsa01_s + poamt_s`
  **Output Variable:** `bsa_s`
  **Tax Unit:** `tu_asfam1_hu`

### 49. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(dag >= 18) & (dag < 65) & (bunct_s = 0) & (bunnc_s = 0) & (yem = 0) & (yse <= 0) & (i_hhpercapitaY1#1 < $MinPension_m*0.9) &(bsa01_s#2=0)`
  - **Tax Unit:** `tu_individual_hu`

### 50. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `$MinPension_m*0.95`
  - **comp_cond**: `(IsDepChild)`
  - **comp_perElig**: `$base*0.8`
  - **lowlim**: `0`
  - **uplim**: `69426#m`
  - **withdraw_base**: `il_meanstestY1`
  - **withdraw_rate**: `1`
  - **Output_Var**: `sin02_s`
  - **TAX_UNIT**: `tu_asfam1_hu`

### 51. Function: Elig
  **Eligibility Check:**
  - **Condition:** `i_hhpercapitaY1#1 < $MinPension_m*0.9`
  - **Tax Unit:** `tu_individual_hu`

### 52. Function: BenCalc
  - **who_must_be_elig**: `one`
  - **base**: `$MinPension_m*0.95`
  - **comp_cond**: `(IsDepChild)`
  - **comp_perElig**: `$base*0.8`
  - **lowlim**: `0`
  - **uplim**: `69426#m`
  - **withdraw_base**: `il_meanstestY1`
  - **withdraw_rate**: `1`
  - **Output_Var**: `bsa01_s`
  - **TAX_UNIT**: `tu_asfam1_hu`

### 53. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `nDepChildrenInTu=0`
  - **Comp_perTU**: `$MinPension_m*0.80`
  - **Output_Var**: `sin01_s`
  - **TAX_UNIT**: `tu_asfam1_hu`

### 54. Function: Elig
  **Eligibility Check:**
  - **Condition:** `nDepChildrenInTu>0`
  - **Tax Unit:** `tu_asfam1_hu`

### 55. Function: ArithOp
  **Formula:** `sin01_s + sin02_s`
  **Output Variable:** `bsa00_s`
  **Tax Unit:** `tu_asfam1_hu`


---

## Policy: output_std_hu
### 1. Function: DefOutput
  - **vargroup**: `a*`
  - **defil**: `ils_dispy`
  - **ILGroup**: `il_*`
  - **nDecimals**: `2`
  - **TAX_UNIT**: `tu_individual_hu`
  - **file**: `HU_2025_std`
  - **VarGroup**: `n/a`
  - **UnitInfo_Id**: `n/a`
  - **UnitInfo_TU**: `tu_cbfam_hu`


---

## Policy: output_std_hh_hu *(Switch: off)*
### 1. Function: DefOutput
  - **file**: `HU_2025_std_hh`
  - **var**: `dwt`
  - **TAX_UNIT**: `tu_hh_oecd_co`
  - **ILGroup**: `ils*`
  - **DefIL**: `ils_dispy`


---

## Policy: bfa_hu *(Switch: off)*
### 1. Function: ArithOp
  **Formula:** `bfa-bmanc_s-bccnc_s-bcclt_s-bchnm_s-bchmt_s`
  **Output Variable:** `bfaot_s`
  **Tax Unit:** `tu_household_hu`


---

## Policy: BTA_hu *(Switch: off)*
### 1. Function: DefVar
  - **i_rand**: `0`

### 2. Function: RandSeed
  - **seed**: `2`

### 3. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_rand`
  **Tax Unit:** `tu_household_hu`

### 4. Function: ArithOp
  **Formula:** `i_rand#1`
  **Output Variable:** `i_rand_ind`
  **Tax Unit:** `tu_individual_hu`

### 5. Function: DefConst
  **Constants Defined:**
  - `$use_nontakeup`: 1


---

## Policy: InitVars_hu
### 1. Function: ArithOp *(Switch: off)*
  **Formula:** `0 - yse`
  **Output Variable:** `yselo_s`
  **Tax Unit:** `tu_individual_hu`

### 2. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_rand_ind`
  **Tax Unit:** `tu_individual_hu`

### 3. Function: DefVar
  - **i_rand_ind**: `0`

### 4. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `lse00`
  **Tax Unit:** `tu_individual_hu`

### 5. Function: DefConst
  **Constants Defined:**
  - `$use_nontakeup`: 0


---

## Policy: setdefault_hu
### 1. Function: SetDefault
  - **Dataset**: `*training_data`
  - **yempv_a**: `0`
  - **liwmy_a**: `0`
  - **lnu**: `0`
  - **lhw_a**: `0`
  - **lhwsr_a**: `0`
  - **bwkmcmy_a**: `0`
  - **lmc20**: `0`
  - **lmc**: `0`
  - **yemmy_a**: `0`
  - **yemmy20_a**: `0`
  - **yemmy19_a**: `0`
  - **yemmy18_a**: `0`
  - **lhw20_a**: `0`
  - **lhw19_a**: `0`
  - **lhw18_a**: `0`
  - **yem_a**: `0`
  - **yem20_a**: `0`
  - **yem19_a**: `0`
  - **yem18_a**: `0`
  - **lma20**: `0`
  - **lma19**: `0`
  - **lma18**: `0`
  - **lma**: `0`

### 2. Function: SetDefault
  - **Dataset**: `*training_data`
  - **poa01**: `0`
  - **bunct**: `0`
  - **bunmt**: `0`
  - **bsamt**: `0`
  - **bsant**: `0`
  - **bfamt**: `0`
  - **bfant02**: `0`
  - **bfant01**: `0`
  - **bfaot**: `0`
  - **aca**: `0`
  - **aco**: `0`
  - **ate**: `0`
  - **poa02**: `0`
  - **yptmp**: `0`
  - **xhcot**: `0`
  - **kfbcc**: `0`
  - **ydses_o**: `0`
  - **tscer**: `0`
  - **tscse**: `0`
  - **tscee**: `0`
  - **tin**: `0`
  - **yprrt**: `ypr`
  - **botre**: `0`
  - **bplct_s**: `0`
  - **bmact_s**: `0`
  - **yemdt**: `0`
  - **ltr**: `0`
  - **kivho**: `0`

### 3. Function: SetDefault
  - **bhl**: `phl`
  - **dataset**: `hu_2007_a7`

### 4. Function: SetDefault *(Switch: off)*
  - **Dataset**: `hu_20*`
  - **phl**: `bhl`
  - **yemmy**: `0`

### 5. Function: SetDefault
  - **Dataset**: `*training_data`
  - **yemmc_s**: `0`
  - **lhwsr_s**: `0`
  - **bwkmceemy_s**: `0`
  - **yemmwmy_s**: `0`

### 6. Function: SetDefault
  - **Dataset**: `hu_20*`
  - **xhl00**: `0`
  - **xed00**: `0`

### 7. Function: SetDefault
  - **Dataset**: `hu_2021_??_*`
  - **kivho**: `0`

### 8. Function: SetDefault
  - **Dataset**: `hu_20*`
  - **ydsyc_a**: `0`

### 9. Function: SetDefault
  - **Dataset**: `*`
  - **bsayn_a**: `-1`

### 10. Function: DefIl
  - **Name**: `il_xs_hl06`
  - **#_DataBasename**: `hu_20??_??_????_??_??`
  - **Run_Cond**: `IsUsedDatabase#1`
  - **RegExp_Factor**: `+`
  - **RegExp_Def**: `xs06[0-9]+`
  - **Warn_If_NonMonetary**: `no`

### 11. Function: ArithOp
  **Formula:** `il_xs_hl06 * yds`
  **Output Variable:** `xhl00`
  **Tax Unit:** `tu_individual_hu`
  **Run Condition:** `IsUsedDatabase#1`

### 12. Function: SetDefault
  - **Dataset**: `hu_20??_??_????_??_??`
  - **xhl01**: `0`

### 13. Function: ArithOp
  **Formula:** `yds * (xs06111 + xs06121)`
  **Output Variable:** `xhl01`
  **Tax Unit:** `tu_individual_hu`
  **Run Condition:** `GetDataCOICOPVersion != 0`

### 14. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `tis`
  **Tax Unit:** `tu_individual_hu`
  **Run Condition:** `!IsUsedDatabase#1`


---

## Policy: tscfa_hu
### 1. Function: BenCalc
  - **Comp_Cond**: `(tinta_s>0) & (il_tinty>0) &(tinta_s > il_tinty)`
  - **Comp_perTU**: `tinta_s - il_tinty`
  - **Output_Var**: `sin01_s`
  - **TAX_UNIT**: `tu_cbfam_hu`

### 2. Function: DefVar
  - **i_tinta00_s**: `0`

### 3. Function: Allocate
  - **Share**: `sin01_s`
  - **Output_Var**: `i_tinta00_s`
  - **TAX_UNIT**: `tu_cbfam_hu`
  - **Share_All_IfNoElig**: `yes`
  - **Share_Between**: `ils_earns#1>0 & !IsDepChild`
  - **#_Level**: `tu_individual_hu`

### 4. Function: ArithOp
  **Formula:** `min(sin01_s*15%, i_tinta00_s)`
  **Output Variable:** `i_tinta00_s`
  **Tax Unit:** `tu_individual_hu`

### 5. Function: Min *(Switch: n/a)*
  - **Output_Var**: `n/a`
  - **TAX_UNIT**: `n/a`


---

## Policy: IlsDef_hu
### 1. Function: DefIl
  - **name**: `ils_earns`
  - **yem**: `+`
  - **yse**: `+`
  - **yemmc_s**: `+`

### 2. Function: DefIl
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

### 3. Function: DefIl
  - **name**: `ils_bensim`
  - **bcclt_s**: `+`
  - **bccnc_s**: `+`
  - **bchmt_s**: `+`
  - **bchnm_s**: `+`
  - **bmanc_s**: `+`
  - **bsa_s**: `+`
  - **bfaot_s**: `n/a`
  - **bwkmcee_s**: `+`

### 4. Function: DefIl
  - **name**: `ils_pen`
  - **poa**: `+`
  - **pdi**: `+`
  - **phl**: `n/a`
  - **psu**: `+`
  - **bhl**: `+`
  - **poa_s**: `+`

### 5. Function: DefIl
  - **name**: `ils_origrepy`
  - **ils_origy**: `+`
  - **ils_pen**: `+`
  - **bmanc_s**: `+`
  - **bunct_s**: `+`
  - **bunnc_s**: `+`
  - **bwkmcee_s**: `+`

### 6. Function: DefIl
  - **name**: `ils_benmt`
  - **bchmt_s**: `+`
  - **bed**: `+`
  - **bsa_s**: `+`
  - **bho**: `+`

### 7. Function: DefIl
  - **name**: `ils_bennt`
  - **bmanc_s**: `+`
  - **bccnc_s**: `+`
  - **bcclt_s**: `+`
  - **bchnm_s**: `+`
  - **bunct_s**: `+`
  - **botre**: `+`
  - **bfaot_s**: `n/a`
  - **bunnc_s**: `+`
  - **bfaot**: `+`
  - **bwkmcee_s**: `+`

### 8. Function: DefIl
  - **name**: `ils_ben`
  - **ils_pen**: `+`
  - **ils_bennt**: `+`
  - **ils_benmt**: `+`

### 9. Function: DefIl
  - **name**: `ils_taxsim`
  - **tin_s**: `+`
  - **tbs_s**: `n/a`
  - **tis_s**: `+`

### 10. Function: DefIl
  - **name**: `ils_tax`
  - **ils_taxin**: `+`
  - **ils_taxwl**: `+`

### 11. Function: DefIl
  - **name**: `ils_sicee`
  - **tscee_s**: `+`

### 12. Function: DefIl
  - **name**: `ils_sicse`
  - **tscse_s**: `+`

### 13. Function: DefIl
  - **name**: `ils_sicer`
  - **tscer_s**: `+`

### 14. Function: DefIl
  - **name**: `ils_dispy`
  - **ils_origy**: `+`
  - **ils_ben**: `+`
  - **ils_tax**: `-`
  - **ils_sicdy**: `-`

### 15. Function: DefIl
  - **Name**: `ils_sicot`

### 16. Function: DefIl
  - **Name**: `ils_base_tin`
  - **bchnm_s**: `+`
  - **bmanc_s**: `+`
  - **poa**: `+`
  - **bccnc_s**: `+`
  - **bcclt_s**: `+`
  - **bed**: `+`
  - **bhl**: `+`
  - **phl**: `n/a`
  - **bunnc_s**: `n/a`
  - **bunct_s**: `+`
  - **ypr**: `+`
  - **yse**: `+`
  - **yem**: `+`

### 17. Function: DefIl
  - **Name**: `ils_base_tbs`
  - **yse**: `+`

### 18. Function: DefIl
  - **Name**: `ils_sicdy`
  - **ils_sicot**: `+`
  - **ils_sicse**: `+`
  - **ils_sicee**: `+`

### 19. Function: DefIl
  - **Name**: `ils_b2_bsaho`
  - **ils_b1_bsa**: `+`
  - **ils_b1_bho**: `+`

### 20. Function: DefIl
  - **Name**: `ils_b2_penhl`
  - **ils_b1_boa**: `+`
  - **ils_b1_bsu**: `+`
  - **ils_b1_bhl**: `+`
  - **ils_b1_bdi**: `+`

### 21. Function: DefIl
  - **Name**: `ils_b2_bfaed`
  - **ils_b1_bfa**: `+`
  - **ils_b1_bed**: `+`

### 22. Function: DefIl
  - **Name**: `ils_b1_bsa`
  - **bsa_s**: `+`
  - **bsaho_s**: `n/a`

### 23. Function: DefIl
  - **Name**: `ils_b1_bho`
  - **bsaho_s**: `n/a`
  - **bho**: `+`

### 24. Function: DefIl
  - **Name**: `ils_b1_bhl`
  - **phl**: `n/a`
  - **bhl**: `+`

### 25. Function: DefIl
  - **Name**: `ils_b1_bun`
  - **bunct_s**: `+`
  - **bunnc_s**: `+`
  - **bwkmcee_s**: `+`

### 26. Function: DefIl
  - **Name**: `ils_b1_bdi`
  - **pdi**: `+`

### 27. Function: DefIl
  - **Name**: `ils_b1_bsu`
  - **psu**: `+`

### 28. Function: DefIl
  - **Name**: `ils_b1_boa`
  - **poa**: `+`
  - **poa_s**: `+`

### 29. Function: DefIl
  - **Name**: `ils_b1_bed`
  - **bed**: `+`

### 30. Function: DefIl
  - **Name**: `ils_b1_bfa`
  - **bcclt_s**: `+`
  - **bchmt_s**: `+`
  - **bchnm_s**: `+`
  - **botre**: `+`
  - **ils_b1_bcb**: `+`

### 31. Function: DefIl
  - **Name**: `ils_b1_bcb`
  - **bfaot**: `+`
  - **bfaot_s**: `n/a`
  - **bccnc_s**: `+`
  - **bmanc_s**: `+`

### 32. Function: DefIl
  - **Name**: `ils_b1_bwk`

### 33. Function: DefIl
  - **Name**: `ils_b2_bunwk`
  - **ils_b1_bwk**: `+`
  - **ils_b1_bun**: `+`

### 34. Function: DefIl
  - **Name**: `ils_taxin`
  - **tin_s**: `+`
  - **tbs_s**: `n/a`
  - **tis_s**: `+`

### 35. Function: DefIl
  - **Name**: `ils_taxwl`
  - **tpr**: `+`

### 36. Function: DefIl
  - **Name**: `ils_sicct`


---

## Policy: tis_hu
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yse>0) & (yse <= 12000000#y) & (i_rand_ind<0.258) & !IsUsedDatabase#1`
  - **Tax Unit:** `tu_individual_hu`

### 2. Function: BenCalc
  - **comp_cond**: `(lhw<=36)`
  - **comp_perElig**: `25000#m`
  - **Output_Var**: `tis_s`
  - **TAX_UNIT**: `tu_individual_hu`
  - **LowLim**: `0`
  - **Who_Must_Be_Elig**: `one`

### 3. Function: DefVar
  - **i_rand_ind**: `0`
  - **i_rand**: `0`

### 4. Function: ArithOp
  **Formula:** `0`
  **Output Variable:** `i_rand_ind`
  **Tax Unit:** `tu_individual_hu`

### 5. Function: ArithOp
  **Formula:** `i_rand#1`
  **Output Variable:** `i_rand_ind`
  **Tax Unit:** `tu_individual_hu`

### 6. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_rand`
  **Tax Unit:** `tu_household_hu`

### 7. Function: RandSeed
  - **seed**: `2`


---

## Policy: IlsUDBDef_hu
### 1. Function: DefIl
  - **Name**: `ils_udb_boa`
  - **poa**: `+`
  - **poa_s**: `+`

### 2. Function: DefIl
  - **Name**: `ils_udb_bsu`
  - **psu**: `+`

### 3. Function: DefIl
  - **Name**: `ils_udb_bdi`
  - **pdi**: `+`

### 4. Function: DefIl
  - **Name**: `ils_udb_bun`
  - **bunct_s**: `+`
  - **bunnc_s**: `+`
  - **bwkmcee_s**: `+`

### 5. Function: DefIl
  - **Name**: `ils_udb_bhl`
  - **phl**: `n/a`
  - **bhl**: `+`

### 6. Function: DefIl
  - **Name**: `ils_udb_bed`
  - **bed**: `+`

### 7. Function: DefIl
  - **Name**: `ils_udb_bsa`
  - **bsa_s**: `+`
  - **bsaho_s**: `n/a`

### 8. Function: DefIl
  - **Name**: `ils_udb_bfa`
  - **bcclt_s**: `+`
  - **bccnc_s**: `+`
  - **bchmt_s**: `+`
  - **bchnm_s**: `+`
  - **bmanc_s**: `+`
  - **bfaot_s**: `n/a`
  - **botre**: `+`
  - **bfaot**: `+`

### 9. Function: DefIl
  - **Name**: `ils_udb_bho`
  - **bsaho_s**: `n/a`
  - **bho**: `+`

### 10. Function: DefIl
  - **Name**: `ils_udb_yem`
  - **yem**: `+`
  - **yemmc_s**: `+`

### 11. Function: DefIl
  - **Name**: `ils_udb_yse`
  - **yse**: `+`

### 12. Function: DefIl
  - **Name**: `ils_udb_ypp`
  - **ypp**: `+`

### 13. Function: DefIl
  - **Name**: `ils_udb_ypr`
  - **ypr**: `+`

### 14. Function: DefIl
  - **Name**: `ils_udb_yiy`
  - **yiy**: `+`

### 15. Function: DefIl
  - **Name**: `ils_udb_ypt`
  - **ypt**: `+`

### 16. Function: DefIl
  - **Name**: `ils_udb_yot`
  - **yot**: `+`

### 17. Function: DefIl
  - **Name**: `ils_udb_xmp`
  - **xmp**: `+`

### 18. Function: DefIl
  - **Name**: `ils_udb_kfbcc`
  - **kfbcc**: `+`

### 19. Function: DefIl
  - **Name**: `ils_udb_tpr`
  - **tpr**: `+`

### 20. Function: DefIl
  - **Name**: `ils_udb_tis`
  - **tin_s**: `+`
  - **tbs_s**: `n/a`
  - **tscee_s**: `+`
  - **tscse_s**: `+`
  - **tis_s**: `+`

### 21. Function: DefIl
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
  - **ils_udb_xmp**: `-`
  - **ils_udb_tis**: `-`
  - **ils_udb_tpr**: `-`


---

## Policy: bmact_hu *(Switch: off)*
### 1. Function: DefVar
  - **i_elparent_bmact**: `0`
  - **Var_Monetary**: `no`
  - **i_elchild_bmact**: `0`
  - **i_ageweeks_bmact**: `0`
  - **i_nelchildren_bmact**: `0`
  - **i_durweeks_bmact**: `0`
  - **i_yempv_bmact**: `0`
  - **i_bmact**: `0`

### 2. Function: DefTu
  - **Type**: `SUBGROUP`
  - **Name**: `tu_bmact_hu`
  - **Members**: `Partner & OwnDepChild & LooseDepChild`
  - **PartnerCond**: `(Default)`
  - **DepChildCond**: `(Default) & (dag <1)`
  - **ExtHeadCond**: `(nDepChOfCouple > 0) & (dgn = 0)`
  - **StopIfNoHeadFound**: `no`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(dgn = 0) & (IsParentOfDepChild#1)`
  - **Tax Unit:** `tu_individual_hu`

### 4. Function: BenCalc
  - **Comp_Cond**: `(i_elparent_bmact=1) & (liwmy/12 >= 1/2)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_elparent_bmact`
  - **TAX_UNIT**: `tu_individual_hu`

### 5. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(IsDepChild#1)`
  - **Tax Unit:** `tu_individual_hu`

### 6. Function: ArithOp
  **Formula:** `nDepChildrenInTu#1`
  **Output Variable:** `i_nelchildren_bmact`
  **Tax Unit:** `tu_individual_hu`

### 7. Function: BenCalc
  - **Comp_Cond**: `(i_elchild_bmact=1)`
  - **Comp_perTU**: `(12-dmb)*(30.5/7)`
  - **Output_Var**: `i_ageweeks_bmact`
  - **TAX_UNIT**: `tu_individual_hu`

### 8. Function: BenCalc
  - **Comp_Cond**: `(i_nelchildren_bmact>0)`
  - **Comp_perTU**: `i_durweeks_bmact/i_nelchildren_bmact`
  - **Output_Var**: `i_durweeks_bmact`
  - **TAX_UNIT**: `tu_bmact_hu`

### 9. Function: BenCalc
  - **Comp_Cond**: `(i_elparent_bmact=1) & ((yivwg > 0) | (yem > 0) | (yse>0))`
  - **Comp_perTU**: `max(yivwg*$lhw*(52/12),yem+yse)`
  - **Output_Var**: `i_yempv_bmact`
  - **TAX_UNIT**: `tu_individual_hu`

### 10. Function: BenCalc
  - **Comp_Cond**: `(i_yempv_bmact>0)`
  - **Comp_perTU**: `(i_yempv_bmact/30) * (i_durweeks_bmact*7)`
  - **Output_Var**: `i_bmact`
  - **TAX_UNIT**: `tu_individual_hu`

### 11. Function: ArithOp
  **Formula:** `i_bmact/12`
  **Output Variable:** `bmact_s`
  **Tax Unit:** `tu_individual_hu`

### 12. Function: BenCalc
  - **Comp_Cond**: `(i_elchild_bmact=1) & (i_ageweeks_bmact>=0) & (i_nelchildren_bmact#1>=1)`
  - **Comp_perTU**: `24`
  - **Output_Var**: `i_durweeks_bmact`
  - **TAX_UNIT**: `tu_individual_hu`
  - **Comp_UpLim**: `4+i_ageweeks_bmact`
  - **Comp_LowLim**: `0`
  - **#_Level**: `tu_bmact_hu`


---

## Policy: parben_output_std_hu *(Switch: off)*
### 1. Function: DefOutput
  - **file**: `HU_2025_std_parben`
  - **vargroup**: `a*`
  - **defil**: `ils_dispy`
  - **ILGroup**: `il_*`
  - **nDecimals**: `2`
  - **TAX_UNIT**: `tu_individual_hu`
  - **VarGroup**: `i_*`
  - **UnitInfo_TU**: `tu_bplct_hu`
  - **UnitInfo_Id**: `IsDepChild`


---

## Policy: bplct_hu *(Switch: off)*
### 1. Function: BenCalc
  - **Comp_Cond**: `(i_nelchildren_bplct_year1>0)`
  - **Comp_perTU**: `0.7*i_yempv_bplct`
  - **Output_Var**: `i_bplct_1`
  - **TAX_UNIT**: `tu_bplct_hu`
  - **Comp_UpLim**: `0.7*($MinWage_m*2)`

### 2. Function: BenCalc
  - **Comp_Cond**: `(i_elparent_bplct=1) & (liwmy/12 >= 1/2)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `i_elparent_bplct`
  - **TAX_UNIT**: `tu_individual_hu`

### 3. Function: BenCalc
  - **Comp_Cond**: `(i_elparent_bplct=1) & ((yivwg > 0) | (yem > 0) | (yse>0))`
  - **Comp_perTU**: `max(yivwg*($lhw*52/12),yem+yse)`
  - **Output_Var**: `i_yempv_bplct`
  - **TAX_UNIT**: `tu_individual_hu`

### 4. Function: DefVar
  - **i_elparent_bplct**: `0`
  - **Var_Monetary**: `no`
  - **i_elchild_bplct_year0**: `0`
  - **i_ageweeks_bplct_year0**: `0`
  - **i_nelchildren_bplct_year0**: `0`
  - **i_durweeks_bplct_year0**: `0`
  - **i_yempv_bplct**: `0`
  - **i_nelchildren_bplct_year1**: `0`
  - **i_bplct**: `0`
  - **i_elchild_bplct_year1**: `0`
  - **i_bplct_0**: `0`
  - **i_bplct_1**: `0`

### 5. Function: DefTu
  - **Type**: `SUBGROUP`
  - **Name**: `tu_bplct_hu`
  - **Members**: `Partner & OwnDepChild & LooseDepChild`
  - **PartnerCond**: `(Default)`
  - **DepChildCond**: `(Default) & (dag<2)`
  - **ExtHeadCond**: `(IsParentOfDepChild) & ((dgn = 0) | ((dgn = 1) & (idpartner = 0)))`
  - **StopIfNoHeadFound**: `no`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(IsHeadOfTu#1) & (IsParentOfDepChild#1)`
  - **Tax Unit:** `tu_individual_hu`

### 7. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(IsDepChild#1) & (dag=0)`
  - **Tax Unit:** `tu_individual_hu`

### 8. Function: BenCalc
  - **Comp_Cond**: `i_elchild_bplct_year0=1`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_nelchildren_bplct_year0`
  - **TAX_UNIT**: `tu_bplct_hu`

### 9. Function: BenCalc
  - **Comp_Cond**: `(i_elchild_bplct_year0=1)`
  - **Comp_perTU**: `(12-dmb)*30.5/7`
  - **Output_Var**: `i_ageweeks_bplct_year0`
  - **TAX_UNIT**: `tu_individual_hu`

### 10. Function: BenCalc
  - **Comp_Cond**: `(i_elchild_bplct_year0#1>0)`
  - **Comp_perTU**: `i_ageweeks_bplct_year0-i_durweeks_bmact`
  - **Output_Var**: `i_durweeks_bplct_year0`
  - **TAX_UNIT**: `tu_individual_hu`
  - **Comp_UpLim**: `i_ageweeks_bplct_year0`
  - **Comp_LowLim**: `0`
  - **#_Level**: `tu_bplct_hu`

### 11. Function: BenCalc
  - **Comp_Cond**: `(i_nelchildren_bplct_year0>0)`
  - **Comp_perTU**: `i_durweeks_bplct_year0/i_nelchildren_bplct_year0`
  - **Output_Var**: `i_durweeks_bplct_year0`
  - **TAX_UNIT**: `tu_bplct_hu`

### 12. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(IsDepChild#1) & (dag=1)`
  - **Tax Unit:** `tu_individual_hu`

### 13. Function: BenCalc
  - **Comp_Cond**: `i_elchild_bplct_year1=1`
  - **Comp_perElig**: `1`
  - **Output_Var**: `i_nelchildren_bplct_year1`
  - **TAX_UNIT**: `tu_bplct_hu`

### 14. Function: BenCalc
  - **Comp_Cond**: `(i_elparent_bplct=1) & (i_yempv_bplct>0) & (i_durweeks_bplct_year0>0)`
  - **Comp_perTU**: `0.7*i_yempv_bplct* (i_durweeks_bplct_year0*7/30.5)`
  - **Output_Var**: `i_bplct_0`
  - **TAX_UNIT**: `tu_individual_hu`
  - **Comp_UpLim**: `0.7*($MinWage_m*2)* (i_durweeks_bplct_year0*7/30.5)`

### 15. Function: ArithOp
  **Formula:** `i_bplct_0 + i_bplct_1`
  **Output Variable:** `bplct_s`
  **Tax Unit:** `tu_bplct_hu`

### 16. Function: ArithOp
  **Formula:** `i_bplct_0/12`
  **Output Variable:** `i_bplct_0`
  **Tax Unit:** `tu_individual_hu`


---

## Policy: random_HU
### 1. Function: DefVar
  - **i_mc_rand_1**: `0`
  - **i_mc_rand_2**: `0`
  - **i_mc_rand_3**: `0`
  - **i_lmamy**: `0`
  - **i_lma2**: `0`
  - **i_lma1**: `0`
  - **Var_Monetary**: `no`
  - **i_bsa_bta_rand**: `0`

### 2. Function: RandSeed
  - **Seed**: `19`

### 3. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_1`
  **Tax Unit:** `tu_individual_hu`

### 4. Function: RandSeed
  - **Seed**: `20`

### 5. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_2`
  **Tax Unit:** `tu_individual_hu`

### 6. Function: RandSeed
  - **Seed**: `21`

### 7. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_mc_rand_3`
  **Tax Unit:** `tu_individual_hu`

### 8. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lmamy`
  **Tax Unit:** `tu_individual_hu`

### 9. Function: RandSeed
  - **Seed**: `25`

### 10. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lma2`
  **Tax Unit:** `tu_individual_hu`

### 11. Function: RandSeed
  - **Seed**: `24`

### 12. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_lma1`
  **Tax Unit:** `tu_individual_hu`

### 13. Function: RandSeed
  - **Seed**: `23`

### 14. Function: ArithOp
  **Formula:** `rand`
  **Output Variable:** `i_bsa_rand`
  **Tax Unit:** `tu_individual_hu`

### 15. Function: RandSeed
  - **Seed**: `734515`


---

## Policy: yemcomp_hu
### 1. Function: DefVar
  - **i_yem_orig**: `yem`
  - **Var_Monetary**: `yes`
  - **i_bwkmcee_s**: `0`
  - **i_yemmc_s**: `0`
  - **i_diff**: `0`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(bwkmceemy_s > 0)`
  - **Tax Unit:** `tu_individual_hu`

### 3. Function: ArithOp
  **Formula:** `yem * 12 / yemmy`
  **Output Variable:** `yemmw_s`
  **Tax Unit:** `tu_individual_hu`

### 4. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Comp_LowLim**: `n/a`
  - **Comp_UpLim**: `n/a`
  - **LowLim**: `n/a`
  - **UpLim**: `n/a`
  - **Output_Var**: `i_bwkmcee_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 5. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `n/a`
  - **Comp_perTU**: `n/a`
  - **Comp_LowLim**: `n/a`
  - **Comp_UpLim**: `n/a`
  - **LowLim**: `n/a`
  - **UpLim**: `n/a`
  - **Output_Var**: `i_yemmc_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 6. Function: BenCalc *(Switch: n/a)*
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_bwkmcee_s + i_yemmc_s > (1-lhwsr_s) * $mc_max * min(lhw/$lhw,1))`
  - **Comp_perTU**: `(1-lhwsr_s) * $mc_max * min(lhw/$lhw,1) - (i_bwkmcee_s + i_yemmc_s)`
  - **Output_Var**: `i_diff`
  - **TAX_UNIT**: `tu_individual_hu`

### 7. Function: ArithOp
  **Formula:** `i_bwkmcee_s + $mc_share * i_diff`
  **Output Variable:** `i_bwkmcee_s`
  **Tax Unit:** `tu_individual_hu`

### 8. Function: ArithOp
  **Formula:** `i_yemmc_s + (1 - $mc_share) * i_diff`
  **Output Variable:** `i_yemmc_s`
  **Tax Unit:** `tu_individual_hu`

### 9. Function: ArithOp
  **Formula:** `i_bwkmcee_s * bwkmceemy_s / 12`
  **Output Variable:** `bwkmcee_s`
  **Tax Unit:** `tu_individual_hu`

### 10. Function: ArithOp
  **Formula:** `i_yemmc_s * bwkmceemy_s / 12`
  **Output Variable:** `yemmc_s`
  **Tax Unit:** `tu_individual_hu`


---

## Policy: TransLMA_hu *(Switch: off)*
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy = 0) & (ysemy = 0)& (dag > 17) & (dag < 65) & (les=5)`
  - **Tax Unit:** `tu_individual_hu`

### 2. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy > 0) `
  - **Tax Unit:** `tu_individual_hu`

### 3. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ysemy > 0) & (yemmy = 0)`
  - **Tax Unit:** `tu_individual_hu`

### 4. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lma =1)`
  - **Tax Unit:** `tu_individual_hu`

### 5. Function: ArithOp
  **Formula:** `(yivwg*$Nwh*52/12)`
  **Output Variable:** `yem_a`
  **Tax Unit:** `tu_individual_hu`

### 6. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lma=1)|(lma=5)`
  - **Tax Unit:** `tu_individual_hu`

### 7. Function: ArithOp
  **Formula:** `$Nwh`
  **Output Variable:** `lhw_a`
  **Tax Unit:** `tu_individual_hu`

### 8. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `dgn = 1 & (i_lma2 < $er_dgn1_se)`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_hu`

### 9. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(bwkmceemy_s > 0)`
  - **Tax Unit:** `tu_individual_hu`

### 10. Function: ArithOp
  **Formula:** `yemmy - bwkmceemy_s`
  **Output Variable:** `yemmwmy_s`
  **Tax Unit:** `tu_individual_hu`

### 11. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lmcee_s = 1)`
  - **Tax Unit:** `tu_individual_hu`

### 12. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(lindi>=9 & lindi<=12) & (dgn = 1) &  (i_mc_rand_1 < $sh_mcee_l5_dgn1)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lmcee_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 13. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(yemmy > 0) & (lcs = 0) & (lma=0)`
  - **Tax Unit:** `tu_individual_hu`

### 14. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(ysemy > 0)  & (lma=0) & (lmcee_s = 0) & (yse>0)`
  - **Tax Unit:** `tu_individual_hu`

### 15. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_1 < $sh_mcse)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lmcse_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 16. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(lmcse_s = 1)`
  - **Tax Unit:** `tu_individual_hu`

### 17. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(ysemy <= $avg_mcsemy)`
  - **Comp_perTU**: `ysemy`
  - **Output_Var**: `bwkmcsemy_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 18. Function: DefConst
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

### 19. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(deh = 5) & (dgn = 1) & (i_lma1 < $ur_dgn1_deh3_ee)`
  - **Comp_perTU**: `1`
  - **Output_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_hu`

### 20. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(deh = 5) & (dgn = 1) & (i_lma1 < $er_dgn1_deh3_ee)`
  - **Comp_perTU**: `2`
  - **Output_Add_Var**: `lma`
  - **TAX_UNIT**: `tu_individual_hu`

### 21. Function: BenCalc
  - **Comp_Cond**: `(lma=2) & (ysemy > 0) & (yemmy = 0)`
  - **Comp_perTU**: `0`
  - **Output_Var**: `yemmy_a`
  - **TAX_UNIT**: `tu_individual_hu`

### 22. Function: DefConst
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
  - `$sh_hours_ee`: n/a
  - `Run_Cond`: GetDataIncomeYear=2019

### 23. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_2> $sh_mceemy_9)`
  - **Comp_perTU**: `min (10, yemmy)`
  - **Output_Var**: `bwkmceemy_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 24. Function: BenCalc
  - **Who_Must_Be_Elig**: `one`
  - **Comp_Cond**: `(i_mc_rand_3 >$sh_45hours_ee)`
  - **Comp_perTU**: `0.70`
  - **Output_Var**: `lhwsr_s`
  - **TAX_UNIT**: `tu_individual_hu`

### 25. Function: DefConst
  **Constants Defined:**
  - `$sh_mcse`: 0
  - `$avg_mcsemy`: 0
  - `$sh_mcse_l5_dgn1`: n/a
  - `$sh_mcse_l4_dgn1`: n/a
  - `$sh_mcse_l3_dgn1`: n/a
  - `$sh_mcse_l2_dgn1`: n/a
  - `$sh_mcse_l1_dgn1`: n/a
  - `$sh_mcse_l5_dgn0`: n/a
  - `$sh_mcse_l4_dgn0`: n/a
  - `$sh_mcse_l3_dgn0`: n/a
  - `$sh_mcse_l1_dgn0`: n/a
  - `$sh_mcsemy_7`: n/a
  - `$sh_mcsemy_6`: n/a
  - `$sh_mcsemy_5`: n/a
  - `$sh_mcsemy_4`: n/a
  - `$sh_mcsemy_3`: n/a
  - `$sh_mcsemy_2`: n/a
  - `$sh_mcsemy_1`: n/a
  - `$sh_hours_se`: n/a
  - `$sh_45hours_se`: n/a
  - `$sh_15hours_se`: n/a
  - `$sh_0hours_se`: n/a
  - `Run_Cond`: GetDataIncomeYear=2019

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
  - `Run_Cond`: GetDataIncomeYear!=2019

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
  - `$sh_hours_ee`: n/a
  - `Run_Cond`: GetDataIncomeYear!=2019

### 28. Function: DefConst
  **Constants Defined:**
  - `$sh_mcse`: 0
  - `$avg_mcsemy`: 0
  - `$sh_mcse_l5_dgn1`: n/a
  - `$sh_mcse_l4_dgn1`: n/a
  - `$sh_mcse_l3_dgn1`: n/a
  - `$sh_mcse_l2_dgn1`: n/a
  - `$sh_mcse_l1_dgn1`: n/a
  - `$sh_mcse_l5_dgn0`: n/a
  - `$sh_mcse_l4_dgn0`: n/a
  - `$sh_mcse_l3_dgn0`: n/a
  - `$sh_mcse_l1_dgn0`: n/a
  - `$sh_mcsemy_7`: n/a
  - `$sh_mcsemy_6`: n/a
  - `$sh_mcsemy_5`: n/a
  - `$sh_mcsemy_4`: n/a
  - `$sh_mcsemy_3`: n/a
  - `$sh_mcsemy_2`: n/a
  - `$sh_mcsemy_1`: n/a
  - `$sh_hours_se`: n/a
  - `$sh_45hours_se`: n/a
  - `$sh_15hours_se`: n/a
  - `$sh_0hours_se`: n/a
  - `Run_Cond`: GetDataIncomeYear!=2019


---

## Policy: poa_hu
### 1. Function: Elig
  **Eligibility Check:**
  - **Condition:** `(poa>0)`
  - **Tax Unit:** `tu_individual_hu`

### 2. Function: ArithOp
  **Formula:** `poa/12`
  **Output Variable:** `poa_s`
  **Tax Unit:** `tu_individual_hu`

### 3. Function: DefVar
  - **Var_Monetary**: `yes`
  - **poa_s**: `0`


---

## Policy: tco_hu *(Switch: off)*
### 1. Function: DefConst
  **Constants Defined:**
  - `$tco_t_std`: $tco_base_t_std
  - `$tco_t_red1`: $tco_base_t_red1
  - `$tco_t_red2`: $tco_base_t_red2
  - `$tco_t_zero`: $tco_base_t_zero

### 2. Function: DefConst
  **Constants Defined:**
  - `$tco_t_01111`: $tco_t_std
  - `$tco_t_01112`: $tco_t_std
  - `$tco_t_01113`: $tco_t_std
  - `$tco_t_01114`: $tco_t_std
  - `$tco_t_01115`: $tco_t_red1
  - `$tco_t_01116`: $tco_t_std
  - `$tco_t_01121`: $tco_t_red2
  - `$tco_t_01122`: $tco_t_red2
  - `$tco_t_01123`: $tco_t_red2
  - `$tco_t_01124`: $tco_t_red2
  - `$tco_t_01125`: $tco_t_std
  - `$tco_t_01126`: $tco_t_std
  - `$tco_t_01127`: $tco_t_std
  - `$tco_t_01131`: $tco_t_red2
  - `$tco_t_01132`: $tco_t_std
  - `$tco_t_01133`: $tco_t_std
  - `$tco_t_01134`: $tco_t_std
  - `$tco_t_01141`: $tco_t_red2
  - `$tco_t_01142`: $tco_t_red2
  - `$tco_t_01143`: $tco_t_red2
  - `$tco_t_01144`: $tco_t_red1
  - `$tco_t_01145`: $tco_t_red1
  - `$tco_t_01146`: $tco_t_red1
  - `$tco_t_01147`: $tco_t_red2
  - `$tco_t_01151`: $tco_t_red1
  - `$tco_t_01152`: $tco_t_std
  - `$tco_t_01153`: $tco_t_std
  - `$tco_t_01154`: $tco_t_std
  - `$tco_t_01155`: $tco_t_std
  - `$tco_t_01161`: $tco_t_std
  - `$tco_t_01162`: $tco_t_std
  - `$tco_t_01163`: $tco_t_std
  - `$tco_t_01164`: $tco_t_std
  - `$tco_t_01165`: $tco_t_std
  - `$tco_t_01166`: $tco_t_std
  - `$tco_t_01167`: $tco_t_std
  - `$tco_t_01168`: $tco_t_std
  - `$tco_t_01169`: $tco_t_std
  - `$tco_t_01171`: $tco_t_std
  - `$tco_t_01172`: $tco_t_std
  - `$tco_t_01173`: $tco_t_std
  - `$tco_t_01174`: $tco_t_std
  - `$tco_t_01175`: $tco_t_std
  - `$tco_t_01176`: $tco_t_std
  - `$tco_t_01177`: $tco_t_std
  - `$tco_t_01178`: $tco_t_std
  - `$tco_t_01181`: $tco_t_std
  - `$tco_t_01182`: $tco_t_std
  - `$tco_t_01183`: $tco_t_red1
  - `$tco_t_01184`: $tco_t_std
  - `$tco_t_01185`: $tco_t_std
  - `$tco_t_01186`: $tco_t_std
  - `$tco_t_01191`: $tco_t_std
  - `$tco_t_01192`: $tco_t_std
  - `$tco_t_01193`: $tco_t_std
  - `$tco_t_01194`: $tco_t_std
  - `$tco_t_01211`: $tco_t_std
  - `$tco_t_01212`: $tco_t_std
  - `$tco_t_01213`: $tco_t_red1
  - `$tco_t_01221`: $tco_t_std
  - `$tco_t_01222`: $tco_t_red1
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
  - `$tco_t_06121`: $tco_t_red2
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
  - `$tco_t_07321`: $tco_t_red2
  - `$tco_t_07331`: $tco_t_red2
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
  - `$tco_t_09411`: $tco_t_zero
  - `$tco_t_09421`: $tco_t_std
  - `$tco_t_09422`: $tco_t_std
  - `$tco_t_09423`: $tco_t_std
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
  - `$tco_t_11111`: $tco_t_red2
  - `$tco_t_11112`: $tco_t_red2
  - `$tco_t_11121`: $tco_t_std
  - `$tco_t_11211`: $tco_t_red2
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

### 3. Function: DefConst
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
  - `$tco_a_04531a`: $tco_base_a_04531a
  - `$tco_a_04531b`: $tco_base_a_04531b
  - `$tco_a_04541`: $tco_base_a_04541
  - `$tco_a_07221a`: $tco_base_a_07221a
  - `$tco_a_07221b`: $tco_base_a_07221b
  - `$tco_a_07221c`: $tco_base_a_07221c
  - `$tco_a_07221d`: $tco_base_a_07221d

### 4. Function: DefConst
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

### 5. Function: DefConst
  **Constants Defined:**
  - `$tco_a_04531`: ($tco_a_04531a +$tco_a_04531b)/2
  - `$tco_a_07221`: ($tco_a_07221b +$tco_a_07221c +$tco_a_07221d)/3

### 6. Function: DefConst
  **Constants Defined:**
  - `$tco_base_a_04531`: ($tco_base_a_04531a +$tco_base_a_04531b)/2
  - `$tco_base_a_07221`: ($tco_base_a_07221a +$tco_base_a_07221b +$tco_base_a_07221c +$tco_base_a_07221d)/4
  - `$tco_base_q_02111`: $tco_base_q_02111t / 40% * 100
  - `$tco_base_q_02121`: $tco_base_q_02121t * 100
  - `$tco_base_q_02122`: $tco_base_q_02122t * 100
  - `$tco_base_q_02131`: $tco_base_q_02131t * 100 / 5
  - `$tco_base_q_07221`: ($tco_base_q_07221a + $tco_base_q_07221b)/2

### 7. Function: DefIl
  - **Name**: `il_xs_exc`
  - **Warn_If_NonMonetary**: `no`
  - **xs02111**: `+`
  - **xs02121**: `+`
  - **xs02122**: `+`
  - **xs02131**: `+`
  - **xs02211**: `+`
  - **xs02212**: `+`
  - **xs02213**: `+`
  - **xs04511**: `+`
  - **xs04521**: `+`
  - **xs04522**: `+`
  - **xs04531**: `+`
  - **xs04541**: `+`
  - **xs07221**: `+`

### 8. Function: DefIl
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
