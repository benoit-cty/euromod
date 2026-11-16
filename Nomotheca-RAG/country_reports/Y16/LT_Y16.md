Cover

Contents

[Abstract [4](#_Toc222228277)](#_Toc222228277)

[Acknowledgements [5](#_Toc222228278)](#_Toc222228278)

[Authors [5](#_Toc222228279)](#_Toc222228279)

[1. Introduction [6](#introduction)](#introduction)

[1.1. Basic information about the tax-benefit system
[6](#basic-information-about-the-tax-benefit-system)](#basic-information-about-the-tax-benefit-system)

[1.2. Commonly used parameters and definitions
[8](#commonly-used-parameters-and-definitions)](#commonly-used-parameters-and-definitions)

[1.3. Social Benefits [11](#social-benefits)](#social-benefits)

[1.3.1. Non-contributory benefits
[11](#non-contributory-benefits)](#non-contributory-benefits)

[1.3.2. Contributory benefits
[15](#contributory-benefits)](#contributory-benefits)

[1.3.3. Not strictly benefits
[19](#not-strictly-benefits)](#not-strictly-benefits)

[1.4. Social contributions
[20](#social-contributions)](#social-contributions)

[1.5. Compulsory health insurance contributions
[21](#compulsory-health-insurance-contributions)](#compulsory-health-insurance-contributions)

[1.6. Taxes [21](#taxes)](#taxes)

[2. Simulation of taxes and benefits in EUROMOD
[24](#simulation-of-taxes-and-benefits-in-euromod)](#simulation-of-taxes-and-benefits-in-euromod)

[2.1. Scope of simulation
[24](#scope-of-simulation)](#scope-of-simulation)

[2.2. Main recent policy changes
[29](#main-recent-policy-changes)](#main-recent-policy-changes)

[2.2.1. Main policy changes between 2022 and 2023
[30](#main-policy-changes-between-2022-and-2023)](#main-policy-changes-between-2022-and-2023)

[2.2.2. Main policy changes between 2023 and 2024
[30](#main-policy-changes-between-2023-and-2024)](#main-policy-changes-between-2023-and-2024)

[2.2.3. Main policy changes between 2024 and 2025
[30](#main-policy-changes-between-2024-and-2025)](#main-policy-changes-between-2024-and-2025)

[2.3. Order of simulation and interdependencies
[31](#order-of-simulation-and-interdependencies)](#order-of-simulation-and-interdependencies)

[2.3.1. Order of simulation in 2022-2025
[31](#order-of-simulation-in-2022-2025)](#order-of-simulation-in-2022-2025)

[2.4. Policy switches [34](#policy-switches)](#policy-switches)

[2.5. Minimum wage [36](#minimum-wage)](#minimum-wage)

[2.5.1. Brief description [36](#brief-description)](#brief-description)

[2.5.2. Definitions and eligibility conditions
[36](#definitions-and-eligibility-conditions)](#definitions-and-eligibility-conditions)

[2.5.3. Amount [36](#amount)](#amount)

[2.6. Benefits [37](#benefits)](#benefits)

[2.6.1. Single person benefit (bsg_s)
[37](#single-person-benefit-bsg_s)](#single-person-benefit-bsg_s)

[2.6.2. Birth grant (bchba_s)
[37](#birth-grant-bchba_s)](#birth-grant-bchba_s)

[2.6.3. Universal child benefit (bchnm_s)
[38](#universal-child-benefit-bchnm_s)](#universal-child-benefit-bchnm_s)

[2.6.4. Additional child benefit (bch00_s)
[38](#additional-child-benefit-bch00_s)](#additional-child-benefit-bch00_s)

[2.6.5. Pregnancy grant (bmaprnc_s)
[40](#pregnancy-grant-bmaprnc_s)](#pregnancy-grant-bmaprnc_s)

[2.6.6. Maternity leave benefit (bmaprct_s)
[40](#maternity-leave-benefit-bmaprct_s)](#maternity-leave-benefit-bmaprct_s)

[2.6.7. Paternity leave benefit (bplct_s)
[42](#paternity-leave-benefit-bplct_s)](#paternity-leave-benefit-bplct_s)

[2.6.8. Childcare benefit (bmact_s)
[43](#childcare-benefit-bmact_s)](#childcare-benefit-bmact_s)

[2.6.9. Benefit for multiple-births (bchmp_s)
[46](#benefit-for-multiple-births-bchmp_s)](#benefit-for-multiple-births-bchmp_s)

[2.6.10. Childcare benefit for students (bmaed_s)
[46](#childcare-benefit-for-students-bmaed_s)](#childcare-benefit-for-students-bmaed_s)

[2.6.11. Social assistance benefit (bsa00_s)
[47](#social-assistance-benefit-bsa00_s)](#social-assistance-benefit-bsa00_s)

[2.6.12. Unemployment social insurance benefit (bunct_s)
[55](#unemployment-social-insurance-benefit-bunct_s)](#unemployment-social-insurance-benefit-bunct_s)

[2.6.13. Long-term work benefit (bunct01_s)
[57](#long-term-work-benefit-bunct01_s)](#long-term-work-benefit-bunct01_s)

[2.6.14. Compensation for heating costs (xhcht_s)
[58](#compensation-for-heating-costs-xhcht_s)](#compensation-for-heating-costs-xhcht_s)

[2.6.15. Compensation for water costs (xhcwt_s)
[59](#compensation-for-water-costs-xhcwt_s)](#compensation-for-water-costs-xhcwt_s)

[2.7. Social insurance contributions
[60](#social-insurance-contributions)](#social-insurance-contributions)

[2.7.1. Employee social insurance contributions (ils_sicee)
[60](#employee-social-insurance-contributions-ils_sicee)](#employee-social-insurance-contributions-ils_sicee)

[2.7.2. Employer social insurance contributions (ils_sicer)
[61](#employer-social-insurance-contributions-ils_sicer)](#employer-social-insurance-contributions-ils_sicer)

[2.7.3. Credited social contributions (ils_sicct)
[62](#credited-social-contributions-ils_sicct)](#credited-social-contributions-ils_sicct)

[2.7.4. Self-employed social contributions (ils_sicse)
[65](#self-employed-social-contributions-ils_sicse)](#self-employed-social-contributions-ils_sicse)

[2.7.5. Contributions to the funded pension scheme (tsceepi_s,
tscsepi_s)
[67](#contributions-to-the-funded-pension-scheme-tsceepi_s-tscsepi_s)](#contributions-to-the-funded-pension-scheme-tsceepi_s-tscsepi_s)

[2.7.6. Compulsory health insurance contributions for those not
otherwise insured (thl_s)
[68](#compulsory-health-insurance-contributions-for-those-not-otherwise-insured-thl_s)](#compulsory-health-insurance-contributions-for-those-not-otherwise-insured-thl_s)

[2.8. Taxes [68](#taxes-1)](#taxes-1)

[2.8.1. Personal income tax (tin_s)
[68](#personal-income-tax-tin_s)](#personal-income-tax-tin_s)

[2.8.2. Consumption taxes [74](#consumption-taxes)](#consumption-taxes)

[2.9. Extraordinary measures in Lithuania
[77](#extraordinary-measures-in-lithuania)](#extraordinary-measures-in-lithuania)

[3. Data [78](#data)](#data)

[3.1. General description
[78](#general-description)](#general-description)

[3.2. Sample quality and design
[79](#sample-quality-and-design)](#sample-quality-and-design)

[3.3. Non-response and item non-response
[79](#non-response-and-item-non-response)](#non-response-and-item-non-response)

[3.4. Weights [79](#weights)](#weights)

[3.5. Data adjustment [80](#data-adjustment)](#data-adjustment)

[3.6. Time period [80](#time-period)](#time-period)

[3.7. Gross incomes [81](#gross-incomes)](#gross-incomes)

[3.8. Merged and imputed variables
[81](#merged-and-imputed-variables)](#merged-and-imputed-variables)

[3.9. Uprating [82](#uprating)](#uprating)

[3.10. Input data extended with household expenditures
[83](#input-data-extended-with-household-expenditures)](#input-data-extended-with-household-expenditures)

[4. Validation [85](#validation)](#validation)

[4.1. Aggregate Validation
[85](#aggregate-validation)](#aggregate-validation)

[4.2. Components of disposable income
[85](#components-of-disposable-income)](#components-of-disposable-income)

[4.2.1. Validation of incomes inputted into the simulation
[86](#validation-of-incomes-inputted-into-the-simulation)](#validation-of-incomes-inputted-into-the-simulation)

[4.2.2. Validation of taxes, SIC and benefits
[87](#validation-of-taxes-sic-and-benefits)](#validation-of-taxes-sic-and-benefits)

[4.2.3. Validation of simulated consumption taxes
[91](#validation-of-simulated-consumption-taxes)](#validation-of-simulated-consumption-taxes)

[4.3. Income distribution
[92](#income-distribution)](#income-distribution)

[4.4. Income inequality [92](#income-inequality)](#income-inequality)

[4.5. Poverty rates [93](#poverty-rates)](#poverty-rates)

[4.6. Summary of “health warnings”
[93](#summary-of-health-warnings)](#summary-of-health-warnings)

[References [95](#references)](#references)

[List of abbreviations and definitions
[96](#list-of-abbreviations-and-definitions)](#list-of-abbreviations-and-definitions)

[List of figures [99](#list-of-figures)](#list-of-figures)

[List of tables [100](#list-of-tables)](#list-of-tables)

[List of Annexes [102](#list-of-annexes)](#list-of-annexes)

[Annex 1. Uprating Factors (2023 = 100)
[102](#annex-1.-uprating-factors-2023-100)](#annex-1.-uprating-factors-2023-100)

[Annex 2. Policy Effects in 2024-2025
[102](#annex-2.-policy-effects-in-2024-2025)](#annex-2.-policy-effects-in-2024-2025)

[Annex 3. Validation Tables
[105](#annex-3.-validation-tables)](#annex-3.-validation-tables)

[Annex 4. Recalculations and Compensations of Pensions
[105](#annex-4.-recalculations-and-compensations-of-pensions)](#annex-4.-recalculations-and-compensations-of-pensions)

[Statistical Annex 1. Validation Tables
[107](#statistical-annex-1.-validation-tables)](#statistical-annex-1.-validation-tables)

<span id="_Toc222228277" class="anchor"></span>Abstract

The EUROMOD Country Reports have the double function of describing the
scope of the EUROMOD simulations, including the underlying assumptions,
and providing the validation of these simulations against official
statistics. The Country Report for Lithuania is prepared by the
Lithuanian EUROMOD National Team each year, and made available by the
JRC on time for the EUROMOD stable release of the model at the beginning
of each year.

<span id="_Toc222228278" class="anchor"></span>Acknowledgements

The work was carried out jointly by the EUROMOD core development team,
based at the JRC in Seville, and the Lithuanian national team.

<span id="_Toc222228279" class="anchor"></span>Authors

The key contributors to this update were:

- Jekaterina Navickė, Aušra Čižauskaitė, Viginta Ivaškaitė-Tamošiūnė,
  Nerijus Černiauskas, as members of the national team for Lithuania

- Alberto Mazzon, as JRC developer responsible for Lithuania

# Introduction

EUROMOD is the tax-benefit microsimulation model for the European Union
(EU). It enables users to calculate in a comparable manner the effects
of taxes and benefits on household incomes and work incentives for the
population of each Member State and for the EU as a whole.

EUROMOD is yearly updated to cover the most recent changes in countries’
tax and benefit policies. It uses input databases which are also
regularly updated, derived from the European Union Statistics on Income
and Living Conditions (EU-SILC) and matched with Household Budget
Surveys (HBS). The model’s update is supported by the following
Directorate-Generals and Services of the European Commission: DG EMPL,
DG ECFIN, DG TAXUD, SG REFORM, DG JRC, DG ESTAT.

EUROMOD was originally maintained, developed and managed by the
Institute for Social and Economic Research (ISER). In 2021, these
responsibilities were taken over by the Joint Research Centre (JRC) of
the European Commission, in collaboration with Eurostat and 27 national
teams from the EU countries. Currently the EUROMOD governance structure
consists of a Steering Committee, allowing partner DGs to monitor the
process of the EUROMOD update, and a Scientific Advisory Board to
monitor and guide the scientific development of the model.

This report documents the work done in the most recent annual update for
Lithuania. It provides an overview of the Lithuanian tax-benefit system
in 2022-2025 and of how these policies are implemented in EUROMOD. The
results presented are derived using EUROMOD version J2.0+, and they may
not match those obtained using earlier or later versions of the model.

The EUROMOD model and software, together with extensive information and
documentation, are available online:

- EUROMOD homepage:
  [https://euromod-web.jrc.ec.europa.eu/resources/documentation](https://euromod-web.jrc.ec.europa.eu/resources/documentation\)

- Downloads: <https://euromod-web.jrc.ec.europa.eu/download-euromod>

- Documentation:
  <https://euromod-web.jrc.ec.europa.eu/resources/documentation>

- Glossary of EUROMOD terms:
  <https://euromod-web.jrc.ec.europa.eu/resources/glossary>

## Basic information about the tax-benefit system 

- The Lithuanian tax-benefit system is predominantly governed at the
  **national level**. Notable exceptions include the land tax, business
  certificates used by the self-employed and the commercial immovable
  property tax, which are fully or largely set by the municipalities.
  Also, municipalities provide a few local benefits based on local
  rules.

- The **fiscal year** runs from the 1st of January to 31st of December.
  Main benefit and tax changes most often come into effect either at the
  beginning of the fiscal year or mid-year, i.e. 1st of July.

- The **statutory retirement age** in Lithuania has been gradually
  increased to reach 65 years for both men and women by 2026 as
  indicated in the Table 1.1 below.

<span id="_Toc222228364" class="anchor"></span>**Table 1.1** Pension age
for women and men, 2022-2026

| **Year** | **Women**         | **Men**            |
|----------|-------------------|--------------------|
| 2022     | 63 years 8 months | 64 years 4 months  |
| 2023     | 64 years          | 64 years 6 months  |
| 2024     | 64 years 4 months | 64 years 8 months  |
| 2025     | 64 years 8 months | 64 years 10 months |
| 2026     | 65 years          | 65 years           |

Source: Sodra, URL: [Senatvės pensijos amžiaus lentelė –
„Sodra“](https://sodra.lt/senatves-pensijos-amziaus-lentele)

- The **minimum school leaving age** is 16 years old. Compulsory
  education is from the age 7 to 16. The age of majority is 18[^1].

- A **dependent child** is defined as an own or adopted child under 18
  years of age unless they have a partner (is married or officially
  cohabiting) or is a parent themself. For *benefit purposes* a
  dependent child can be under the age of 23 (under 24 in case of social
  assistance) if in full-time general or vocational education (or
  tertiary education in case of social assistance) [^2]. *For tax
  purposes*, dependent children are defined as children under the age of
  18 or older, if with disability or in education.

- **Single parent** is defined as a parent of a dependent child who is
  not legally married nor officially cohabiting.

- The **income tax system is an individual system**, with income of the
  spouses being assessed independently, although a few types of expenses
  can be deducted from the partner’s or parent’s tax dues.

- **Taxpayers can fill out an annual tax declaration** in order to
  return the unused annual tax allowance (also referred to as basic
  allowance) and/or to make certain deductions from the income tax dues.
  This is not obligatory unless a taxpayer is self-employed.

- Entitlement to the **means-tested social assistance** benefits
  typically depends on the assessment of the last three months’ average
  monthly income per person and an assets test. The assessment unit is
  typically a single adult or a couple plus any dependent children.

- Statutory indexation rules apply to pensions and social benefits in
  Lithuania on an annual basis.

- Consumption taxes consist of (1) VAT with four effective rates
  (standard 21%, 9%, 5% and 0%), (2) excises on tobacco, alcohol, and
  energy, and (3) import duties.

- Since 1 January 2015, the national currency is euro.

The policy parameters saved as constants in the model and their values
for the most recent year are available at
[<u>https://euromod-web.jrc.ec.europa.eu/resources/parameters</u>](https://euromod-web.jrc.ec.europa.eu/resources/parameters). 

## Commonly used parameters and definitions

Social benefits, pensions and compensations are often calculated in
relation to reference amounts, as indicated below (see
<span class="mark"></span>[**Table 1.2**](#Table_01_02) for the recent
levels).

**Basic Social Allowance** ***(bazinė socialinė išmoka**),* hereinafter
referred to as “**BSA**”, is the Government approved social indicator
mainly used for defining and calculating of different social protection
benefits and other statutory values.

**State Supported Income** ***(valstybės remiamos pajamos)*** level
(hereinafter referred to as “**SSI**”) is the Government approved
personal income level after taxes and contributions, but before
transfers of cash social assistance.

**Cost of Basic Needs (*minimalių vartojimo poreikių dydis*)**,
hereinafter referred to as “**CBN**”, is the Government approved social
indicator for estimating basic needs, which include both food and
non-food (other goods and services) components. Since 1st June 2022, BSA
and SSI have been increased as part of anti-inflation measure
package[^3].

<span id="Table_01_02" class="anchor"></span>**Table 1.2** Monthly BSA,
SSI and CBN levels effective on 30th June 2022-2025, EUR

<table style="width:58%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 4%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 4%" />
</colgroup>
<thead>
<tr>
<th></th>
<th style="text-align: center;"></th>
<th style="text-align: center;">2022 1<sup>st</sup> January</th>
<th style="text-align: center;">2022 1<sup>st</sup> June</th>
<th style="text-align: center;">2023</th>
<th style="text-align: center;">2024</th>
<th style="text-align: center;">2025</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Basic Social Allowance (BSA)</strong></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">42</td>
<td style="text-align: center;">46</td>
<td style="text-align: center;">49</td>
<td style="text-align: center;">55</td>
<td style="text-align: center;">70</td>
</tr>
<tr>
<td><strong>State Supported Income (SSI)</strong></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">129</td>
<td style="text-align: center;">147</td>
<td style="text-align: center;">157</td>
<td style="text-align: center;">176</td>
<td style="text-align: center;">221</td>
</tr>
<tr>
<td><strong>Cost of Basic Needs (CBN)</strong></td>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">267</td>
<td style="text-align: center;">354</td>
<td style="text-align: center;">446</td>
<td style="text-align: center;">450</td>
</tr>
</tbody>
</table>

Source: Based on the relevant version of Government of Lithuanian
Republic Resolution “Dėl bazinės socialinės išmokos dydžio
patvirtinimo”, “Dėl valstybės remiamų pajamų dydžio patvirtinimo” and
“Dėl minimalių vartojimo poreikių dydžio patvirtinimo”.

A number of other commonly used definitions for benefit calculations,
such as income lists, are presented here:

**Insured Income** ***(draudžiamosios pajamos)**,* hereinafter referred
to as “**II**”, defines the *<u>list</u>* of the person’s *insured
income* on the basis of which a number of contributory benefits, such as
maternity leave and paternity leave benefits, sickness benefit or
unemployment benefit, are paid.

*Insured income* includes all income of a person on which state social
insurance contributions were (or had to be) paid: earnings; income from
sports, incomes paid under authorship agreements, income of
self-employed persons and with some extent incomes received by some
groups of people that were previously not covered by social insurance
(solicitors, bailiffs, individual business owners, farmers and partners,
etc.); sickness benefit (including the first two days of sickness for
which the employer pays), vocational rehabilitation, maternity leave,
paternity leave, childcare benefits set by *the Law on Sickness and
Maternity Social Insurance*; sickness benefits due to occupational
accidents or occupational disease allowances payable in accordance with
*the Law on Social Insurance of Occupational Accidents and Occupational
Diseases*. There were no major changes made to the insured income list
during the period of 2022-2025.

The **average monthly insured income** **(AMII)** is the sum of the
insured incomes (**II)** averaged over the last several months before
the right to the relevant benefit has been granted. For example, the
right to maternity leave, paternity leave and childcare benefits relies
on AMII which is based on the averaged income calculated over the last
12 months period (excluding the month the benefit is claimed) [^4].
Other benefits, such as vocational rehabilitation allowance and
occupational disease allowance are based on insured income averaged over
3 months’ period. No major changes were made between 2022 and 2025.

**Pension indexation coefficient (*indeksavimo koeficientas*) and
reference points (*apskaitos vienetas*).** As of 2018 the formula for
estimating social insurance pension amounts was modified. All pension
entitlements were recalculated using a basic pension part and *reference
points (RP)*, which are to be automatically indexed each year using an
*indexation coefficient (IC)*. The RP refers to 12 average monthly
salaries earned during one year and is capped at 5 RP (60 average
monthly wages) per year. The IC is calculated based on the average
change of the total wage fund during the three previous, current and
three forthcoming years. Since January 1st 2022, individual indexation
coefficient (*ICC*) has been introduced to additionally index individual
pension part [^5]. Since 1st June 2022, RP and IIC have been increased
as part of anti-inflation measure package[^6].

<span id="_Toc222228366" class="anchor"></span>**Table 1.3** RP and IC
amounts, 30th June 2022-2025, EUR

<table style="width:66%;">
<colgroup>
<col style="width: 22%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 0%" />
<col style="width: 10%" />
<col style="width: 0%" />
<col style="width: 7%" />
<col style="width: 0%" />
<col style="width: 7%" />
<col style="width: 0%" />
<col style="width: 7%" />
<col style="width: 0%" />
<col style="width: 6%" />
<col style="width: 0%" />
</colgroup>
<thead>
<tr>
<th colspan="2" style="text-align: left;"></th>
<th colspan="2" style="text-align: left;"></th>
<th colspan="2">2022 1<sup>st</sup> January</th>
<th colspan="2">2022 1<sup>st</sup> June</th>
<th colspan="2">2023</th>
<th colspan="2">2024</th>
<th colspan="2">2025</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2"><strong>Reference Points (RP)</strong></td>
<td colspan="2" style="text-align: left;"></td>
<td colspan="2">4.70</td>
<td colspan="2">4.94</td>
<td colspan="2">5.70</td>
<td colspan="2">6.38</td>
<td colspan="2">7.16</td>
</tr>
<tr>
<td colspan="2"><strong>Indexation Coefficient (IC)</strong></td>
<td colspan="2" style="text-align: left;"></td>
<td colspan="4">1.0847</td>
<td colspan="2">1.0902</td>
<td colspan="2">1.0957</td>
<td colspan="2">1,1063</td>
</tr>
<tr>
<td><strong>Individual Indexation Coefficient (IIC)</strong></td>
<td colspan="2" style="text-align: left;"></td>
<td colspan="2" style="text-align: left;">1.0424</td>
<td colspan="2">1.05*</td>
<td colspan="2">1.0580</td>
<td colspan="2">1.02</td>
<td colspan="2">1,014</td>
<td></td>
</tr>
</tbody>
</table>

Notes: \* additional pension IIC since mid-year.

Source: SoDRA, URL:
<http://www.sodra.lt/lt/situacijos/statistika/pagrindiniai-socialiniai-rodikliai>

**Basic monthly pension (BMP) *(valstybinio socialinio draudimo bazinė
pensija*)** is the state approved amount, mainly used for the
calculation of social insurance benefits, such as old-age pension or
vocational rehabilitation allowance. Due to anti-inflation measures
package, the BMP has been increased twice in 2022.

**Assistance pension base (APB) (*šalpos pensijos bazė***) is the state
approved amount, introduced on January 1st 2017. The pension base is a
standard amount, used for the calculation of social assistance benefits
such as: social assistance disability pensions, social assistance
old-age pensions, social assistance orphans’ pensions[^7]. Due to
anti-inflation measures package, the APB has been increased twice in
2022[^8].

Most of the state pensions in Lithuania are calculated in relation to
the **state pension base (SPB) *(valstybinių pensijų bazė),***

<span id="_Toc222228367" class="anchor"></span>**Table 1.4** Basic
monthly pension, social assistance pension base and state pension base,
30th June 2022-2025, EUR

<table style="width:55%;">
<colgroup>
<col style="width: 24%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
</colgroup>
<thead>
<tr>
<th></th>
<th>2022 1<sup>st</sup> January</th>
<th><p>2022</p>
<p>1<sup>st</sup> June</p></th>
<th>2023</th>
<th>2024</th>
<th>2025</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Basic monthly pension (BMP)</strong></td>
<td>215.09</td>
<td>225.84</td>
<td>246.21</td>
<td>269.77</td>
<td>298.45</td>
</tr>
<tr>
<td><strong>Assistance pension base (APB)</strong></td>
<td>150</td>
<td>173</td>
<td>184</td>
<td>197</td>
<td>248</td>
</tr>
<tr>
<td><strong>State pension base (SPB)</strong></td>
<td>59.35</td>
<td>65.29</td>
<td>68.29</td>
<td>72.35</td>
<td>73,62</td>
</tr>
</tbody>
</table>

Source: Based on the Law “Dėl valstybinės socialinio draudimo bazinės
pensijos dydžio, valstybinės socialinio draudimo našlių pensijos bazinio
dydžio, maksimalios neperskaičiuotos pensijos dydžio ir valstybinių
pensijų bazės dydžio patvirtinimo“and its relevant amendments and
changes. The actual amounts are also published in Sodra’s page:
https://www.sodra.lt/lt/situacijos/statistika/pagrindiniai-socialiniai-rodikliai

**Minimum monthly salary** **(*minimali mėnesinė alga),*** hereinafter
referred to as “**MMS**” which amounts are listed in Table 1.5. This
reference amount is also used for defining (credited) social
contributions (see more details in section 2.7.3) and setting
non-taxable amount (section 2.8.1).

Average monthly salary (AMS) is used for estimating the base for some
personal income tax payments and estimating the base for social
insurance payments.[^9]

Average monthly salary of the previous quarter (AMSp) is used for
calculations of minimum and maximum amounts of maternity/paternity and
unemployment benefits.

<span id="Table_01_04" class="anchor"></span>**Table 1.5** State pension
base, minimum and average monthly salary, 30th June 2022-2025, EUR

<table style="width:65%;">
<colgroup>
<col style="width: 31%" />
<col style="width: 2%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;"></th>
<th style="text-align: left;"></th>
<th>2022 1<sup>st</sup> January</th>
<th>2022 1<sup>st</sup> June</th>
<th>2023</th>
<th>2024</th>
<th>2025</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Minimum monthly salary (MMS)</strong></td>
<td></td>
<td colspan="2">730</td>
<td>840</td>
<td>924</td>
<td>1038</td>
</tr>
<tr>
<td><strong>Average monthly salary (AMS)</strong></td>
<td></td>
<td colspan="2">1504.1</td>
<td>1684.9</td>
<td>1902.7</td>
<td>2108.88</td>
</tr>
<tr>
<td><strong>Average monthly salary of the previous quarter
(AMSp)</strong></td>
<td></td>
<td colspan="2">1666.9</td>
<td>1887.8</td>
<td>2097.3</td>
<td>2322.2</td>
</tr>
</tbody>
</table>

Source: Based on the Government of Lithuania Republic Resolution "Dėl
minimaliojo darbo užmokesčio dydžio didinimo" and their relevant
changes. AMS and AMSp amounts are published in the Sodra’s page
(<https://www.sodra.lt/lt/situacijos/pagrindiniai-socialiniai-rodikliai>).
The AMSpreflect the average gross earnings in the whole economy of the
previous quarter (QIV used in the model) published regularly here:
<https://osp.stat.gov.lt/en/statistiniu-rodikliu-analize?hash=6dca3982-d760-4b7f-bf48-ada2e5c0526f#/>.

## Social Benefits

### Non-contributory benefits

*All non-contributory benefits are non-taxable.*

**Birth grant** ***(vienkartinė išmoka gimus vaikui**)**:*** a lump-sum
cash benefit paid upon the birth (an adoption) of a child. The birth
grant amounts to 11 BSA per child, which equals to 770 EUR in 2025.[^10]

**Universal child benefit (*išmoka vaikui*):** each child up to 18 years
old receives a universal child benefit which is equal to 1.75 BSA. Since
January 1st, 2022, universal child benefit is also paid for families
with children below the age of 23 if in full-time general education,
including for those who are in vocational education, also while on leave
due sickness, pregnancy, or childbirth[^11]. In 2025 the child benefit
amount is 122.5 EUR. For children in families of social risk who have
compulsory early childhood education and care, pre-school, primary,
basic education programs, but do not attend educational institutions,
child benefit are provided in non-monetary form.

**Additional child benefit *(papildoma išmoka vaikui):*** a monthly cash
benefit paid for families with three or more children, for families
raising a child with a disability or families with up to two children
when household income is below a set income threshold. The benefit level
is calculated in relation to the BSA. Only one additional benefit can be
paid for the same child. Since January 1st, 2022, additional child
benefit is also paid for families with children below the age of 23 if
in full-time general education, including for those who are in
vocational education while on leave due sickness, pregnancy, or
childbirth[^12]. For children in families of social risk who have
compulsory early childhood education and care, pre-school, primary,
basic education programs, but do not attend educational institutions,
child benefit are provided in non-monetary form.

**Childcare benefit for students (*išmoka besimokančio ar studijuojančio
asmens vaiko priežiūrai*):** a monthly childcare benefit paid for one of
the parents (lone parent, guardian, foster) during study period or 12
months after finishing school of graduation[^13]. The benefit is paid to
one of the parents who studies (studied) in full time formal vocational
training or higher education programme, and doctoral/medical residency
studies [^14] and according to *the Law on Sickness and Maternity Social
Insurance* and is not entitled to a standard childcare benefit (a person
before the first day of childcare leave had less than 12 months over the
last 24 months of maternity (paternity) social insurance record). The
fixed benefit of 6 BSA is paid until the child reaches the age of 2
years. If two or more children are born (adopted) the amount of the
student’s childcare benefit does not increase. Since January 1st, 2022,
student’s childcare benefit is also paid for students who are in
full-time general education[^15]. To avoid double granting of the
benefit for a later born / adopted / foster child, the benefit is paid
for the care of the youngest child until they reach the age of 2.

**Benefit for multiple-births (*išmoka gimus vienu metu daugiau kaip
vienam vaikui*):** a monthly benefit paid for one of the parents (lone
parent) due to the birth of two or more children[^16]. The benefit level
is calculated in relation to BSA and varies based on the number of
children born at the same time: the benefit of 4 BSA is paid when two
children are born and it is increased by 4 BSA per child if more than
two children are born at the same time The benefit is paid from the
birth of the children until the children reach the age of 2 years.

**Benefit to a conscript’s child** ***(išmoka privalomosios tarnybos
kario vaikui***)***:*** a monthly benefit paid for each child in the
amount of 1.5 BSA during the military service of the father. According
to *Law on the Benefits to Children*, the benefit is paid to the mother
of the child of a conscript, unless she is not a permanent resident of
the Republic of Lithuania. In that case, the benefit is paid to the
child’s father. The recipient of this benefit is also entitled to a
child benefit as described above.

**Guardianship benefit** **and targeted guardianship subsidy**
***(globos (rūpybos) išmoka ir globos (rūpybos) išmokos tikslinis
priedas):*** **a** targeted guardianship subsidy is paid monthly to a
child’s guardian (curatorship) per child whom guardianship is
established for a family or a family-type institution.[^17] Since
January 1st, 2022, the guardian benefit amount is differentiated
according to the age and needs of the child under guardianship: 5.2 BSA
for children under 6 years of age, 6 BSA for children 6-12 years of age
and 6.5 BSA for children 12-8 years of age, children with disabilities.
The payment of the targeted guardianship subsidy to the former guardian
(caregiver) is extended when after the custody (care) of the children
due to age, emancipation, marriage or education, the former guardian
remains with the former caregiver and is dependent on them, but no
longer until they reach the age of 24.

**Temporary childcare allowance** (***vaiko laikinosios priežiūros
išmoka***): since January 2020, a newly introduced benefit of 6 BSA per
month for temporary childcare[^18]. Benefit is paid to a person
temporary taking care of a child as stipulated in *the Law on
Fundamentals of Protection of the Rights of the Child*. The temporary
childcare allowance is not granted if the request is made by child’s
parents or other legal representatives. The benefit is paid throughout
the period of temporary care.

**Grant for settlement** ***(vienkartinė išmoka įsikurti):*** a lump sum
of 75 BSA is given to a child upon the termination of a guardianship due
to reaching the legal age of 18, emancipation, or marriage. The grant
can be used for various purchases or expenses, including the purchase or
rental of a home, to cover housing costs, the purchase of furniture,
video or audio equipment, a computer, vehicles, to cover medical
expenses, etc. The grant cannot be paid in cash unless the unused part
of the grant is less than 2 BSA.

**Pregnancy grant *(vienkartinė išmoka nėščiai moteriai):*** a lump-sum
benefit to a pregnant woman who is not eligible to receive a maternity
leave benefit from the social insurance fund. The grant amounts to 6.43
BSA and is paid 70 days before the term of childbirth.

**Social assistance benefit (*socialinė pašalpa)*:** is the last resort
monthly benefit paid to families or single persons if they meet the
established eligibility, assets, and income tests (1.1 SSI per person).
The amount of the social assistance benefit depends on household
composition (equivalence scales are applied) and the benefit payment is
reduced with time. For people taking up a job with at least the MMS and
who comply with other required conditions, the in-work social assistance
benefit can be granted. This in-work social assistance benefit can be
paid up to 12 months and is reduced with time.

**Compensations for the heating of a dwelling, cold and hot water
expenses *(kompensacijos už būsto komunalines paslaugas)*** The heating
compensation is granted when the heating costs exceed 10% of the
difference between income and 2 SSI per each family member or 3 SSI for
single person (instead of 1.5 SSI), based on the notional defined sizes
of useful spaces [^19]. The drinking water compensation is granted when
the cots for cold water and wastewater exceed 2 % of income, while the
hot water compensation – when exceed 5% or income, taking into account
the notional standards (expressed in m3). Compensations are granted to
families and single persons if the value of family’s or person’s assets
does not exceed the established ratio of property value and if all
family members (single persons) meet the same eligibility criteria as
described for the receipt of the social assistance benefit.

**State social assistance benefits/pensions (*valstybinės šalpos
išmokos*)**: there are four types of social assistance
benefits/pensions: social assistance pensions; orphan’s social
assistance pensions; social assistance compensations pension
supplements. Social assistance benefits/pensions are varied and
calculated in relation to the *basic monthly pension (BMP)* (see
[**Table 1.4**](#Table_01_04)).

**Funeral allowance (*laidojimo pašalpa*):** a non-contributory lump-sum
benefit equal to 8 BSA is paid to the person burying the deceased.

**Repatriation benefit (*parama palaikams parvežti*):** is a
means-tested benefit for the repatriation of remains to Lithuania. The
benefit is equal to the actual costs of transporting, but not exceeding
54 BSA and is paid if mean monthly household’s income does not exceed 3
SSI.

*State pensions:*

**State pensions of degree one or two of the Republic of Lithuania
*(Lietuvos Respublikos pirmojo ir antrojo laipsnių valstybinės
pensijos)*** are awarded to citizens for distinguished achievements or
for individual or respective status (i.e., top-level state officials,
champions of Olympic Games, etc.), if these persons have reached a
**s**tatutory retirement age or have partially or fully lost their
capacity to work. A state pension of the first degree is equal to 4
*state pension bases (SPB)*. A state pension of the second-degree
amounts to 2 *state pension bases* (see [**Table 1.4**](#Table_01_04)).
The second-degree pension can also be awarded to a (step) mother or
(step)father who raised well 5 or more children and does not suffer from
addictions.

**State pensions for victims (*nukentėjusiųjų asmenų valstybinės
pensijos*)** are awarded to the persons recognised as incapable or
partially capable of work due to a number of state recognized
aggressions (i.e. 11-13 January 1991 events), political imprisonment,
deportations, participation in the resistance to the occupation, for
participants in elimination of the consequences of the accident at the
Chernobyl Nuclear Power Plant, or persons who became disabled due to
military service in the Soviet Army. These pensions are paid if persons
have reached the statutory retirement age or have partially or fully
lost their capacity to work. The pension amount is calculated in
relation to the *state pension base* (see [**Table 1.4**](#Table_01_04))
and varies for different victim groups.

**State pensions for officers and soldiers (*pareigūnų ir karių
valstybinės pensijos)*** are awarded to officers and soldiers or their
family members. There are three types of these pensions: for the
service; for lost capacity for work; for widows and orphans. The pension
amount is calculated based on the service record and former wage. The
exception is for compulsory or voluntary conscripts who lost their
capacity for work, the amount is calculated in relation to the state
pension base and varies depending on the level of the lost capacity for
work.

**State pensions for scientists *(mokslininkų valstybinės pensijos)***
are awarded to scientists on the basis of *the temporary Law on State
Pensions for Scientists*. These pensions are awarded to individuals with
an academic degree or title and at least a 10-year career of a doctor or
habilitated doctor **w**ho are either reached the statutory pension age
or lost 60–100% of their capacity for work. The pension is not paid if a
person continues pursuing scientific work. The amount of the pension is
calculated in relation to the *state pension base* (see [**Table
1.4**](#Table_01_04)) and depends on the insurance record.

**State** **pensions for judges *(teisėjų valstybinės pensijos)*** are
awarded to the retired persons, who worked as judges of the
Constitutional Court, the Supreme Court of Lithuania, the Court of
Appeal of Lithuania, the Supreme Administrative Court of Lithuania and
other Lithuanian general jurisdiction and specialized courts as well as
judges of any international court elected or delegated by Lithuania and
if they have at least five years of judicial service. The pension amount
depends on the service record and is calculated as a percentage of the
average salary over the last five years of the judicial work. Persons
entitled to receive state pension also have a right to receive state
social insurance pension, unless otherwise provided by the law..

**President of the Republic of Lithuania spouse’s state pension
(*Lietuvos Respublikos sutuoktinio valstybinė pensija)*** is awarded to
the spouse who carried out functions as defined by the official and (or)
diplomatic protocol for at least 3 years during the President’s term.
The pension amount is equal to 11.64% of the President’s monthly
salary[^20]. The pension is paid if the spouse has reached the statutory
retirement age or has lost at least 60% of capacity for work and does
not receive another state pension.

**President of the Republic of Lithuania orphan’s state pension
*(Lietuvos Respublikos sutuoktinio našlaičių valstybinė pensija*)** is
awarded to the President‘s orphan children, who either are: below the of
18; or above the age of 18 years old and is with disability; or below
the age of 24 if in full-time education. The amount per child is equal
to 30% of the President spouse’s pension, but for all children cannot
exceed 100% of the President spouse’s pension.

### Contributory benefits

*Taxable contributory benefits:*

**Maternity leave benefit (*motinystės išmoka*):** a lump sum benefit
paid to a pregnant woman who has contributed to the *Sickness and
Maternity Social Insurance.* The benefit is paid for a total of 126
calendar days, covering the period before and after the childbirth.
Maternity benefit is equal to 77.58% of the recipient’s compensatory
income but cannot be lower than 8 BSA. To qualify for the maternity
leave benefit it is required to have at least 12 months over the last 24
months of sickness and maternity social insurance contribution record.
Maternity benefit amount is not reduced if a person receives income from
self-employment during maternity benefit payment period.

**Paternity leave benefit (*tėvystės išmoka*):** a lump sum benefit,
which is granted on the basis of *the Law on Sickness and Maternity
Social Insurance*. The father can claim the benefit can from the birth
of his child until the child reaches 1 year of age. The paternity leave
duration is 30 days and can be split in two parts. The benefit is
granted if a person before the first day of paternity leave had no less
than 6 months over the last 24 months of sickness and maternity social
insurance record. The amount of paternity benefit is equal to 77.58% of
the recipient’s compensatory income, but cannot be lower than 8 BSA and
not higher than two national average monthly salaries of the previous
quarter (AMSp). The paternity benefit amount is not reduced if a person
receives income from self-employment during paternity benefit payment
period.

**Childcare benefit (*vaiko priežiūros išmoka*):** a monthly payment
granted on the basis of *the Law on Sickness and Maternity Social
Insurance* if a person before the first day of childcare leave had no
less than 12 months over the last 24 months of sickness and maternity
social insurance record. Since 1st of January 2023, the childcare
benefit is paid to one of the parents (adoptive parents), or guardians,
or grandparents (if satisfies the same contributory requirements and one
of the parents has the right to the benefit) until the child reaches
either 1.5 year (18 months) or 2 years (24 months), where parents can
choose between the two options. The compensation rate for
one-and-a-half-year period benefit is 60%, and for two years period the
compensation rate is 45% during the first year and 30% during the second
year. Additionally, during the childcare leave months each of the
parents (but not grandparents) has the right to use 2 non-transferable
months (or four months for a single parent) with higher compensatory
rate of 78%. The benefit is calculated in relation to AMII (see more
details in section 2.11.) with the minimum of 8 BSA and the maximum of
two country’s average monthly wages of the previous quarter. If one of
the parents receiving childcare benefit qualifies for another childcare
benefit for the other child, she or he is paid both benefits, but the
total amount of the benefits cannot exceed 78% of the previous earnings.

*Non-taxable contributory benefits:*

**Old-age pension *(senatvės pensija):*** monthly pension paid for
persons who attain the old-age retirement age as specified by *the*
*Pensions’* *law* and have the minimum or obligatory insurance period
specified for the old-age pension. Pensions consist of a basic pension
part and an individual pension part. The latter is calculated using
reference points (RP). Pensions are indexed on an annual basis.[^21].
Since January 1st, 2022, an additional indexation of the individual
pension component has been introduced [^22]. The supplementary index for
the individual part of the pension is calculated based on 75% of the
surplus of Sodra's pension contributions. The additional indexation
applies if the at-risk-of-poverty rate for people aged 65+ is higher
than 25% and (or) the ratio between the average old-age pension and the
average wage is less than 50%. Additionally, the procedure for
calculating the basic part of the pension has been changed for persons
who have minimum insurance period but do not have the obligatory length
of insurance, i.e., they are paid the basic pension part in full.

**Small pension bonus *(mažų pensijų priemoka):*** Since January 1st,
2019, bonuses on low pensions were introduced for the recipients of low
old-age or disability pensions, calculated as a difference between 95%
CBN and a sum of pensions, also taking into account contribution record
relative to full required [^23]. Since January 1st, 2020, the pension
bonus is paid as difference between 100% CBN and a sum of pensions.

**Single person benefit (*vienišo asmens išmoka*)** –is granted to
single adults with a working capacity level of up to 55% and persons who
have reached the statutory retirement age and do not receive any widow’s
or orphan’s benefits or these benefits are lower than the single person
benefit.[^24].

**Early retirement old-age pension (*išankstinė senatvės pensija*)** can
be claimed up to five years before the regular retirement age with 34
years of insurance contributory history in 2025[^25]. A reduction of
0.32% is applied for each month remaining until the retirement age[^26].
The amount of early retirement old-age pension is indexed on an annual
basis. As of January 1st, 2021, the amount of old-age pensions is not
reduced if the person has received the early retirement pension for less
than 3 years and has attained the period of insurance of 41 years before
receiving the early retirement pension in 2025[^27].

**Disability pension *(negalios pensija, before 2023.12.31 netekto
darbingumo pensija)***[^28]***:*** paid to a person for whom a certain
level of lost work capacity (level of participation since 2024) is
established. The pension varies according to the assessed degree of lost
work capacity (participation), as well as a person’s contribution
history. The amount of the disability pension depends on a level of lost
work capacity (participation), insurance period, the number of the
reference points (RF) and the amounts of the RF and basic pension. The
*minimum* and *obligatory* insurance periods are defined based on a
person’s age. Disability pensions are indexed in the same way as the
old-age pensions.

**Survivor's or orphan's pension *(našlių ir našlaičių pensija):*** is
paid monthly to the spouse and children of the deceased person if the
deceased person had been entitled or received the state disability (work
incapacity) pension or the old-age pension (see above). Survivor pension
is a lump-sum monthly amount. Survivor’s and orphan’s pensions is
indexed and recalculated in the same way as old-age pensions.

**Compensations for special working conditions (*kompensacijos už
ypatingas darbo sąlygas*)** are paid to people who have worked in
hazardous jobs until they reach statutory pension age. The monthly
compensation is equal to 136.4 % of the basic monthly pension (see
[**Table 1.4**](#Table_01_04))[^29].

**Unemployment social insurance benefit (*nedarbo draudimo išmoka*)** is
a monthly benefit paid to the unemployed people if they have at least 12
months of the unemployment social insurance record over the last 30
months (with the exception of those who were in the compulsory primary
military service or the alternative national defence service) and are
registered with the Public Unemployment Service. The benefit is
comprised of the constant (% of MMS) and variable (% of the previous
wage) components. The standard unemployment benefit can be paid for up
to 9 months with the decreasing replacement rate every three months. The
maximum amount of the benefit cannot be higher than 58.18% of the
national gross average wage.

**Long-term work benefit (ilgalaikio darbo išmoka).** Employees, who
have been continuously employed by the same employer for at least 5
years, in case of redundancy are eligible to receive the long-term work
benefits, except for those who have been working in budgetary
institutions and the Central Bank. The benefit is lump-sum and is equal
to 77.58% of one, two or three average earnings, depending on the length
of the contract with the same employer.

**Sickness benefit (*ligos išmoka*)**: granted on the basis of *the Law
on Sickness and Maternity Social Insurance* and is paid to people who
have been insured for at least 3 months over the last 12 months or 6
months over the 24 months (except for some groups). The benefit is
calculated on the basis of insured income with maximum (2 times the
national average monthly of the previous quarter salary (AMSp)) and
minimum (11.64% of the national average income) thresholds applied. The
benefit is partly paid by the employer (for first two days;) and partly
by the State Social Insurance Fund (from the third day
afterwards).[^30]. The sickness benefit, paid by the employer (for two
days), cannot by lower than 62.06% and higher than 100% of recipient’s
average wage. Employers are obliged to pay the sickness benefit from the
employer’s funds for the first 2 days of sickness regardless of the
employee’s social insurance record. The amount of sickness benefit, paid
by the State Social Insurance Fund is equal to 62.06% of compensatory
income, for donors for transplantation purposes - 77.58%, for parents
and grandparents taking care of sick child – 65.94% [^31]. The length of
the benefit varies (8 cases of varied duration are defined by law;
additionally, 11 specific cases for taking sickness leave to care of a
child).

**Vocational rehabilitation allowance (*profesinės reabilitacijos
išmoka*):** granted on the basis of *the Law on Sickness and Maternity
Social Insurance.* The allowance is paid monthly for the entire period
of the rehabilitation programme, but not for longer than 180 calendar
days. The benefit amount is equal to 65.94% of compensatory income[^32].
The amount of the benefit cannot be higher than 2 average monthly salary
of the previous quarter (AMSp) and lower than 2 BMP.

**Occupational disease allowance *(ligos dėl nelaimingo atsitikimo darbe
ar profesinės ligos išmoka):*** monthly allowance paid to people who
became temporary incapable to work and was covered by the social
insurance at the moment of the accident. The benefit is paid until the
person’s return to work or until the assignment of other benefit, i.e.
work incapacity pension. The benefit is equal to 77.58% of the average
monthly insured income AMII [^33].

**Disability grant *(netekto dalyvumo vienkartinė kompensacija*)**: a
lump-sum amount paid in case of the up to 30% loss of work capacity
(since 2024 – participation level): If up to 20% of work (participation)
capacity is (temporarily) lost, the grant is equal to 7.76% of persons’
24 months compensatory earnings; if 21% to 29%, of work (participation)
incapacity is (temporarily) lost, the grant is equal to 15.52% of
earnings[^34]. If the lost work (participation) incapacity is permanent,
then the grant is 3 times higher than the relevant grant amount,
indicated under different degrees of lost (temporary) work
(participation) incapacity.

**Periodical compensation for disability *(netekto dalyvumo periodinė
kompensacija)*** is a monthly compensation for insured persons who lost
30% or more of their work capacity because of an accident at work or
professional disease. If insured person lost 30-45% of work capacity
(since 2024 – participation level), monthly compensation is paid; if
insured person lost 45% or more work capacity (participation level),
compensation is paid if: the beneficiary is not entitled to the same
amount or higher lost incapacity (participation level) social insurance
pension; if the insured person receives disability social insurance
pension, which is lower than periodic compensation for disability
(compensation paid as difference)[^35].

**Periodical compensation in case of death of insured *(Periodinė
draudimo išmoka apdraustajam mirus)*:** is paid monthly to the family
members and the amount is equal to work incapacity periodical
compensation divided by the number of persons qualifying for the
compensation. The benefit is paid irrespective of other income (except
for the survivor’s or orphan’s pensions). This compensation is paid as
an entitlement due to the occupational accidents or occupational disease
insurance social insurance.

**Grant in case of death of insured** ***(Vienkartinė draudimo išmoka
apdraustajam mirus)*:** a lump-sum amount paid to the family members of
the deceased. The grant is equally divided between all family members.
This grant is paid as an entitlement due to the occupational accidents
or occupational disease insurance social insurance. The grant is equal
to 46.55 times the national average monthly wage[^36].

### Not strictly benefits

**Promotional education stipends** ***(skatinamosios stipendijos)***:
educational stipends given to students from all type of higher public
educational institutions. The stipends are paid from the institutional
scholarship funds based on specific institutional educational
performance criteria, while the government defines overarching maximum
stipend levels. Maximum levels also depend on the educational
institution type. The rate and criterion for receiving promotional
education stipends are determined by the schools themselves according to
the regulations on the provisions of stipends.

**Social stipends (*socialinės stipendijos*):** is a type of educational
stipend given to students from low-income families if they study at
public educational institutions. Social stipends are assigned to
educational establishment, as part of their institutional scholarship
fund. Social stipends are paid only for the students in higher
education, students have a right to get social stipends and promotional
stipends at the same time; students from vocational training
institutions can get lump sum payments from the school budget on
decision of appropriate administrative body. The State Studies
Foundation is responsible for the payment of the social stipends[^37],
which are equal to 6.5 BSA[^38]. Bachelor, masters, doctoral and
vocational training students are eligible to receive benefit if they
meet at least one of the following conditions: 1) is eligible to receive
the social assistance benefit; 2) has working capacity level of 45% or
less or is with severe/moderate disability; 3) is not older than 25
years of age and has been placed in custody (care) or parent(s) have
died.

**Municipal support *(vienkartinės pašalpos iš savivaldybių
biudžetų):*** municipalities have a right to grant a one-time social
support benefit for the families or single persons if they do not pass
the income test or the eligibility criteria to the social assistance.
The rules of granting a one-time municipal social support are set at the
local authorities’ level.

**Social assistance to pupils (*socialinė parama mokiniams*):** a
means-tested free meals to pupils (except for lunch for the first and
second grade pupils without means-test) and support for school’s
supplies (equal to 2 BSI) prior to the beginning of a new school year.
The threshold for the income test for both benefits is equal to 1.5
state supported income (SSI) per household member (or 2 SSI for some
groups). Free meals can be also offered during summer holidays at summer
camps organised by schools.

**Compensation for drugs and medical devices (*vaistų ir medicinos
pagalbos priemonių įsigijimo išlaidų kompensavimas*):** granted to
insured people based on *the Law of Health Insurance*. Children until
the age of 18 and people with severe disability have a right to 100%
compensation for approved drugs and medical devices. Pensioners, other
people with disabilities, or people ill with certain disease have a
right to partial compensation of the approved drugs and medical devices.
People get immediate discounts at pharmacies for approved drugs or
medical devices.

**Medical rehabilitation and compensation for sanatorium expenses
(*medicininės reabilitacijos ir sanatorinio gydymo išlaidų
kompensavimas)*:** granted to insured people based on *the Law of Health
Insurance*. 100% of medical rehabilitation expenses are compensated for
children until the age of 18, people with severe disability and people
ill with certain diseases. 90% of basic sanatorium expenses are
compensated for children until age 7 and people with disabilities until
age 18. Basic sanatorium prices are defined by the Ministry of Health.

**Severance pay/compensation (*Išeitinė kompensacija*):** paid if the
labour contract is terminated at the employer’s initiative and no fault
of the employee is identified. The severance pay/compensation is paid by
the employer in relation to the employment duration at the company. This
benefit is subject to the personal income tax.

## Social contributions

**Social insurance contributions (*socialinio draudimo įmokos*)** to the
State Social Insurance Fund (*Socialinio draudimo fondas,* *SoDra*) are
compulsorily paid by all employers and employees of private and public
sectors as well as main categories of self-employed people.
Contributions are flat-rate, but they differ for employees and
self-employed. Furthermore, contribution rates vary considerably among
different categories of self-employed people. Social insurance
contributions are paid for pensions, health care, sickness and
maternity, employment injuries, occupational diseases and unemployment
insurance. Social insurance contributions are subject to ceilings
(except for the healthcare contributions and for the funded pension
scheme) of 60 AMS (but only for the employees’ contributions)[^39] and
floors equal to the monthly minimum wage (applied to both employees and
employers’ contributions).

*Employee’s contributions*: All employees of private and public sector
pay the total contributions of 19.5%, divided between pension (8.72%),
sickness (1.99%), maternity (1.81%) and health (6.98%) social
insurance[^40]. Those who participate in the 2nd pension pillar, pay an
additional contribution of 3% of their salary with the state subsidy of
1.5% of the AMS.

*Employer’s contributions:* All employers of private and public sector
pay social insurance contributions on behalf of their employees (the
standard total rate being 1.77%, however, it can vary from 1.45% to
2.49% depending on the type of contract (open-ended or temporary) and if
it is a budget institution., etc.). Employers usually pay: unemployment
social insurance contributions (1.31%), to the employment injuries and
occupational diseases social insurance (0.14%), payments to the
long-term work benefit fund (0.16%), the guarantee fund (0.16%) and
[^41] . The last two types of insurances are not paid on behalf of
people working in bank of Lithuania and in government institutions,
while the payment to the guarantee fund is not made for people working
in political parties, trade unions, religious communities and foreign
companies. Employer contributions are subject to the floors of the
minimum monthly salary (MMS), meaning that employers have to pay social
insurance contributions not lower than for the MMS for those employees
whose monthly salaries are below the MMS.

*Contributions for self-employed*. Most self-employed are also covered
by the social insurance system for different social risks. The coverage
of different groups of the self-employed by social insurance has been
gradually expanded. Depending on the group of self-employed one belongs
to (currently 7 different groups are specified) they are covered by
different types of social insurance. For example, persons engaged in
individual activities are covered by the pension, sickness and maternity
social insurances, paying the total of 12.52% on 90% of their received
yearly income, while persons carrying out activities under a business
certificate pay only 8.72% of MMS to the pension insurance.

## Compulsory health insurance contributions 

Health insurance contributions are compulsory. All people receiving
taxable people pay health contributions of 6.98% or their gross salary.
People who do not have taxable income and who are not otherwise insured
for health social insurance by the government (see Section 2.7.3 for
details), nevertheless have to pay the compulsory monthly health
insurance contribution of 6.98% of the MMS.

## Taxes

**Personal Income Tax (*asmens pajamų mokestis)*** has a progressive
schedule and is applied on taxable individual income. This tax is paid
according to the *Law on Personal Income Tax (Lietuvos Respublikos
gyventojų pajamų mokesčio įstatymas*). Taxable income includes most
types of incomes, but over 50 categories are excluded (most importantly,
all state social assistance or social insurance benefits, paid from
state and municipal budgets or Social Insurance Fund, apart from
sickness, maternity leave, paternity leave, childcare and long-term work
benefits) as well as income from activities exercised under a business
certificate. In addition, various non-taxable amounts are deducted from
certain types of income (most notably from employment income, often
referred to as basic allowance) and certain expenditures (e.g., private
pension contributions) reduce taxable income. The main 20% PIT rate is
applied the annual taxable income below or equal to 60 AMS, and the
second 32% PIT rate if the annual taxable income exceeds 60 AMS. 15% tax
rate is applied to taxable benefits from the social insurance fund, as
well as to dividends and self-employment income.

**Corporate Income Tax (*pelno mokestis*)** is paid by Lithuanian and
foreign entities. For the purpose of calculating taxable profits of
Lithuanian entity non-taxable income and deductions can be deducted. The
tax rate on the taxable profits of Lithuanian entities and permanent
establishments is 15%. Since January 1st, 2021, entities with less than
10 employees and annual revenue below 300 thousand euros benefit from a
0% tax rate in the first year and 5% later [^42]. Since 1st July 2022,
an additional taxation of the profits of credit institutions is
implemented[^43]. The share of taxable profits of credit institutions
(e.g. banks) exceeding 2,000,000 EUR is subject to an additional tax
rate of 5%[^44].

**Inheritance tax (*paveldimo turto mokestis*)** is set according to the
*Inheritance Tax Law* (Lietuvos Respublikos paveldimo turto mokesčio
įstatymas). The taxable value of inherited property is taxed at either
5% (when the value is under 150 000 euros) or 10% otherwise. The tax is
applied on the 70% of the total value (see *Dėl Paveldimo turto
apmokestinamosios vertės apskaičiavimo taisyklių patvirtinimo*). No tax
is applied to property that is inherited by spouses, close kin and for
property of low value. Some allowances or deductions may be granted by
municipalities.

**Land taxes *(žemės mokestis)*** are set according to *Lietuvos
Respublikos žemės mokesčio įstatymas*. are based on the assessed value
of the land and paid by the landowner. The land tax calculation is based
on land value, which is estimated according to land assessment
methodology proven by the Government. [^45]Generally, a land tax value
is based on immovable property register data and it is calculated by the
local State Tax Inspectorate. Some people are exempt from land tax
liability, e.g. people with disabilities, pensioners. Some allowances or
deductions may be granted by municipalities. The rate of land tax ranges
from 0.01% to 4% of the assessed value of land and is defined
individually by each council of municipality [^46].

**Value Added Tax (*pridėtinės vertės mokestis*)** is set by the *Law on
Value Added Tax* (*Lietuvos Respublikos pridėtinės vertės mokesčio
įstatymas).* The standard rate is 21%. Reduced and super reduced rates
also exist for some goods and services: 9% (for, e.g., district heating,
books, certain transportation, hotel accommodation) and 5% (e.g.
pharmaceuticals and newspapers). Several services are exempt from VAT
(e.g., financial services), while other services and goods are exempt
depending on the provider and the recipient (e.g., non-profit
institution, state institution, political parties, trade unions and
other non-profit entities for their members).

**Excise Duties (*akcizai*)** are charged on alcohol and alcoholic
beverages, tobacco, and energy products according to *Law on Excise
Taxes* (*Lietuvos Respublikos akcizų įstatymas*).

**Immovable Property Tax (*nekilnojamo turto mokestis*)** is set
according to the Law on Immovable Property Tax (*Lietuvos Respublikos
nekilnojamojo turto mokesčio įstatymas)***.** This tax is paid by
natural and legal persons. The immovable property tax can range from
0.3% to 3% of the assessed value of property. The tax rate of commercial
immovable property is set by the municipality, while the residential
immovable property tax rate is set by the central government. The
residential immovable property tax rate is zero for the first 150 000
euro (200.000 EUR for families with three or more children or raising
children (under 18 or older) with disabilities) and rises to 0.5, 1 and
2%.

**Other taxes**

Other indirect taxes include Income Deductions according to Forest Law,
Tax on state natural resources, Tax on real estate - Leasing of
state-owned land, Lottery and Gambling Tax, Vehicle Tax, Environment
Pollution Taxes, Tolls and International Trade and Transaction Taxes.

# Simulation of taxes and benefits in EUROMOD

## Scope of simulation

Not all the taxes and benefits mentioned in the previous section are
simulated in EUROMOD. Some of the taxes or benefits are beyond the scope
of EUROMOD (i.e. indirect or business taxation) and are therefore
excluded from further simulations or imputations into the EUROMOD
underlying database. Their descriptions serve primarily as a tool for a
better understanding of the overall tax-benefit structure in Lithuania.
Some of the direct taxes and benefits are also not possible to simulate
based on the available data. If feasible, though, they are included (as
observed in the original data source) in the EUROMOD database either as
individual or/and aggregate income sources.

<span class="mark"></span>[**Table 2.1**](#Table_02_01) and
<span class="mark"></span>[**Table 2.2**](#Table_02_02) list the main
Lithuanian tax-benefit instruments, as discussed in Section 1, and
provide a brief explanation as to why the instrument is not (fully)
simulated or in which format it is included in the EUROMOD database.
Most of the benefits that are simulated in EUROMOD are family benefits
that depend on the number of children and their age. Furthermore,
simulations are possible for a number of contributory (social insurance
based) benefits, such as maternity leave or benefits assigned to
low-income households. A number of benefits, which entitlement rights
dependent on contribution history (i.e., pensions, sickness benefit,
disability benefits, etc.) are not simulated due to the lack of data on
previous employment history and salaries received, some event occurrence
(i.e., disability or accident at work).

Most of the direct income taxes and social insurance contributions are
simulated (except some minor ones), as they are calculated as
percentages of gross labour earnings, which are available in the EU-SILC
database. Nevertheless, some specific tax allowances or taxation of
specific income types cannot be simulated due to the lack of more
detailed information on a person’s disability degree, economic activity
type or other specific socio-economic information that is not collected
in the EU-SILC database. In such cases, the basic allowance level or
other general income taxation rules are applied.

<span id="Table_02_01" class="anchor"></span>**Table 2.1** Simulation of
benefits in EUROMOD, 2022-2025

<table style="width:65%;">
<colgroup>
<col style="width: 15%" />
<col style="width: 7%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 16%" />
</colgroup>
<thead>
<tr>
<th rowspan="2"><strong>Benefit</strong></th>
<th rowspan="2"><strong>Variable name(s)</strong></th>
<th colspan="4" style="text-align: center;"></th>
<th><strong>Main limitations/other remarks</strong></th>
</tr>
<tr>
<th style="text-align: center;"><strong>2022</strong></th>
<th style="text-align: center;"><strong>2023</strong></th>
<th style="text-align: center;"><strong>2024</strong></th>
<th><strong>2025</strong></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>Birth grant</td>
<td>bchba_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>Universal child benefit</td>
<td>bchnm_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>Introduced in 2018</td>
</tr>
<tr>
<td>Additional child benefit</td>
<td>bch00_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>Benefit to a conscript’s child</td>
<td>-</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td>E</td>
<td>No recipients could be observed due to the very limited scope of the
benefit.</td>
</tr>
<tr>
<td>Guardianship benefit</td>
<td>bchor</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td>I</td>
<td>No data on guardianship (curatorship); also included in the variable
bfa.</td>
</tr>
<tr>
<td>Grant for housing (settlement)</td>
<td>-</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td>E</td>
<td>Not identified in the data</td>
</tr>
<tr>
<td>Benefit for multiple birth families</td>
<td>bchmp_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>Introduced in 2017</td>
</tr>
<tr>
<td>S’udent's childcare benefit</td>
<td>bmaed_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>Introduced in 2017</td>
</tr>
<tr>
<td>Pregnancy grant</td>
<td>bmaprnc_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>No data on contribution history</td>
</tr>
<tr>
<td>Maternity leave benefit</td>
<td>bmaprct_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>No data on contribution history</td>
</tr>
<tr>
<td>Paternity leave benefit</td>
<td>bplct_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>No data on contribution history</td>
</tr>
<tr>
<td>Childcare benefit</td>
<td>bmact_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>No data on contribution history</td>
</tr>
<tr>
<td>Social assistance benefit</td>
<td>bsa00_s</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td>PS</td>
<td>No data on assets</td>
</tr>
<tr>
<td>Compensations for heating of a dwelling, cold and hot water
expenses, and sewage</td>
<td>bho</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td>I</td>
<td>No data on expenditures available</td>
</tr>
<tr>
<td>Unemployment social insurance benefit</td>
<td>bunct_s</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td>PS</td>
<td>No data on contribution history</td>
</tr>
<tr>
<td>Long-term work benefit</td>
<td>bunct01_s</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td>PS</td>
<td>Modelled with assumptions</td>
</tr>
<tr>
<td>Old-age pension</td>
<td>boa</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on contribution &amp; wage history;</td>
</tr>
<tr>
<td>Early retirement old-age pension</td>
<td>byr</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td>I</td>
<td>No data on contribution &amp; wage history or application for
early-retirement; also included within aggregate variable bun</td>
</tr>
<tr>
<td>Disability pension</td>
<td>bdi</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on disability occurrence.</td>
</tr>
<tr>
<td>Invalidity pension</td>
<td>bdi / boa</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td>-</td>
<td>No data on disability occurrence; information included in variables
bdi or boa (hereinafter referred to as bdi/boa), splitting by retirement
age</td>
</tr>
<tr>
<td>Survivor's or orphan's pension</td>
<td>boa/bsu</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on the loss of family members; included in variables boa or
bsu, based on recipient’s retirement age.</td>
</tr>
<tr>
<td>Sickness benefit</td>
<td>bhl</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on sickness duration</td>
</tr>
<tr>
<td>Vocational rehabilitation allowance</td>
<td>bdi</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on event occurrence</td>
</tr>
<tr>
<td>Occupational disease allowance</td>
<td>bdi</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on event occurrence</td>
</tr>
<tr>
<td>Disability grant</td>
<td>bdi/boa</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on incapacity occurrence</td>
</tr>
<tr>
<td>Work incapacity periodical compensation</td>
<td>bdi/boa</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on incapacity occurrence</td>
</tr>
<tr>
<td>State pensions of degree one or two</td>
<td>boa</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on occupational achievements</td>
</tr>
<tr>
<td>State pensions for victims</td>
<td>bdi</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on participation in recognized aggressions, political
imprisonment, deportations, etc.</td>
</tr>
<tr>
<td>State pensions for officers and soldiers</td>
<td>boa</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on occupation history</td>
</tr>
<tr>
<td>State pensions for scientists</td>
<td>boa</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on academic career length</td>
</tr>
<tr>
<td>State pensions for judges</td>
<td>boa</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on detailed occupational segregation and history</td>
</tr>
<tr>
<td>President of the Republic of Lithuania spouse state pension</td>
<td>-</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td>E</td>
<td>No recipients could be observed due to the very limited scope of the
benefit.</td>
</tr>
<tr>
<td>President of the Republic of Lithuania orphan state pension</td>
<td>-</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td>E</td>
<td>No recipients could be observed due to the very limited scope of the
benefit.</td>
</tr>
<tr>
<td>Temporary childcare allowance</td>
<td>-</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on the need for child protection.</td>
</tr>
<tr>
<td>Compensations for special working conditions</td>
<td>boa</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on hazardous jobs worked</td>
</tr>
<tr>
<td>State social assistance benefits/pensions</td>
<td>boa/bdi</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No information on relevant conditions, as disability occurrence,
nursing at home, etc.</td>
</tr>
<tr>
<td>Loss of breadwinner’s pension</td>
<td>bsu</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on previous rights to the benefit;</td>
</tr>
<tr>
<td>Retirement pension</td>
<td>boa</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on previous rights to the benefit</td>
</tr>
<tr>
<td>Single person benefit</td>
<td>bsg_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>Introduced in 2021</td>
</tr>
<tr>
<td>Educational stipends and other financial support for unemployed</td>
<td>bed</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on participation in non-formal education programmes;</td>
</tr>
<tr>
<td>Vocational training support</td>
<td>-</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td>E</td>
<td>No data on those receiving vocational education scholarships.</td>
</tr>
<tr>
<td>Apprenticeship</td>
<td>-</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td>E</td>
<td>No data on participation under an apprenticeship contracts.</td>
</tr>
<tr>
<td>Social stipends</td>
<td>bed</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No data on affiliation to different type of educational
establishments</td>
</tr>
<tr>
<td>Promotional education stipends</td>
<td>bed</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No information on grades</td>
</tr>
<tr>
<td>Municipal support</td>
<td>bsals</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td>I</td>
<td>No information on different benefit rules by municipalities;
inclusive of NGO support.</td>
</tr>
<tr>
<td>Free meals to pupils</td>
<td>-</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td>E</td>
<td>Value of the meal could only be based on the maximum subsidy amounts
to food providers.</td>
</tr>
<tr>
<td>Free school’s supplies prior to the beginning of a new school
year</td>
<td>-</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td>E</td>
<td>No rules for benefit distribution in 2005-2006. No information on
families being at “social-risk or special conditions set by education
institutions.</td>
</tr>
<tr>
<td>Compensation for drugs and medical devices</td>
<td>-</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td>E</td>
<td>No information on consumption of drugs</td>
</tr>
<tr>
<td>Funeral benefit</td>
<td>bsu</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td style="text-align: center;">IA</td>
<td>IA</td>
<td>No information on the loss of family members or benefit split among
the relatives</td>
</tr>
<tr>
<td>Severance pay</td>
<td>yunsv</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td>I</td>
<td>No information on circumstances upon termination of the job
contract.</td>
</tr>
<tr>
<td style="text-align: center;">Compensation for heating costs</td>
<td style="text-align: center;">xhcht_s</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td>PS</td>
<td>Modelled with assumptions on average monthly heating costs</td>
</tr>
<tr>
<td style="text-align: center;">Compensation for water costs</td>
<td style="text-align: center;">xhcwt_s</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td>PS</td>
<td>No data on cold/hot water usage and price, therefore average
cold/hot water usage in m3 per person is used.</td>
</tr>
</tbody>
</table>

Notes: \[a\] Variable extension *“\_s”* indicates variable that has been
simulated. Other variables are taken/ imputed from the used micro-data.
Notes: “-”: policy did not exist in that year; “E”: *excluded* from the
model as it is (neither included in the micro-data nor simulated); “I”:
*included* in the micro-data but not simulated; “IA”: included in the
micro-data in an aggregated variable but not simulated; “PS”: *partially
simulated* as some of its relevant rules are not simulated; “S”:
*simulated* although some minor or very specific rules may not be
simulated.

Source: Own elaboration.

<span id="Table_02_02" class="anchor"></span>**Table 2.2** Simulation of
taxes and social contributions in EUROMOD, 2022-2025

<table style="width:64%;">
<colgroup>
<col style="width: 16%" />
<col style="width: 8%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 17%" />
</colgroup>
<thead>
<tr>
<th><strong>Taxes and social contributions</strong></th>
<th><strong>Variable name(s)</strong></th>
<th colspan="5" style="text-align: center;"><strong>Main
limitations/other remarks</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td></td>
<td></td>
<td><strong>2022</strong></td>
<td><strong>2023</strong></td>
<td><strong>2024</strong></td>
<td><strong>2025</strong></td>
<td><strong> </strong></td>
</tr>
<tr>
<td>Personal Income Tax</td>
<td>tin_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>Certain income sources (e.g., from sale of financial assets) are
aggregated and then approximately simulated. Business licence tax is
imputed from the data.</td>
</tr>
<tr>
<td>Corporate Income Tax</td>
<td>-</td>
<td>n.a.</td>
<td>n.a.</td>
<td>n.a.</td>
<td>n.a.</td>
<td>Outside the scope of the model</td>
</tr>
<tr>
<td>Land Tax</td>
<td>-</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>Outside the scope of the model</td>
</tr>
<tr>
<td>Inheritance tax</td>
<td>-</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>No information available</td>
</tr>
<tr>
<td>Immovable property tax</td>
<td>-</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>Outside the scope of the model</td>
</tr>
<tr>
<td>VAT</td>
<td>tco_lt</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>Calculations based on extended input files with consumption
expenditures from HBS</td>
</tr>
<tr>
<td>Income Deductions according to Forest Law</td>
<td>-</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>Outside the scope of the model</td>
</tr>
<tr>
<td>Excise duties</td>
<td>tco_lt</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>Calculations based on extended input files with consumption
expenditures from HBS</td>
</tr>
<tr>
<td>Deferment and apportionment of tax payments due to Covid-19</td>
<td>-</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>Outside the scope of the model</td>
</tr>
<tr>
<td>Lottery and Gambling tax</td>
<td>-</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>Outside the scope of the model</td>
</tr>
<tr>
<td>Vehicle Tax</td>
<td>-</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>Outside the scope of the model</td>
</tr>
<tr>
<td>Environment Pollution Taxes</td>
<td>-</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>Outside the scope of the model</td>
</tr>
<tr>
<td>Tolls</td>
<td>-</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>Outside the scope of the model</td>
</tr>
<tr>
<td>International trade and transaction taxes</td>
<td>-</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>Outside the scope of the model</td>
</tr>
<tr>
<td>Credited social contributions</td>
<td>ils_sicct</td>
<td>PS</td>
<td>PS</td>
<td>PS</td>
<td>PS</td>
<td><p>Only some of the eligible</p>
<p>groups identified.</p></td>
</tr>
<tr>
<td>Credited contributions for health insurance</td>
<td>tsccthl_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>Employers’ social insurance contributions:</td>
<td>ils_sicer</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>- pension social insurance</td>
<td>tscerpi_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>- sickness and maternity social insurance</td>
<td>tscersi_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>- unemployment social insurance</td>
<td>tscerui_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>- health insurance</td>
<td>tscerhl_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>- employment injuries and occupational diseases social
insurance</td>
<td>tscerac_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>-payments to the guarantee fund</td>
<td>tscersf_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>-payment to the long-term unemployment fund</td>
<td>tscerot_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>Employees social insurance contribution:</td>
<td>ils_sicee</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>- pension social insurance</td>
<td>tsceepi_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>- sickness and maternity social insurance</td>
<td>tsceesi_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>- health insurance</td>
<td>tsceehl_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>- contributions to the second pillar pensions</td>
<td>tpceepi_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>Random allocation used for different rates.</td>
</tr>
<tr>
<td>Self-employed social insurance contributions:</td>
<td>ils_sicse</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>- for pensions</td>
<td>tscsepi_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>- for compulsory health insurance</td>
<td>tscehl_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>No data on income received from authorship contracts. No data on
land size.</td>
</tr>
<tr>
<td>- sickness and maternity social insurance</td>
<td>tscsesi_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>- contributions to the second pillar pensions</td>
<td>tpcsepi_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>Random allocation used for different rates.</td>
</tr>
</tbody>
</table>

Notes: “-” policy did not exist in that year; “E” policy is *excluded*
from the model’s scope as it is neither included in the microdata nor
simulated by EUROMOD; “PS” policy is *partially simulated* as some of
its relevant rules are not simulated; “S” policy is *simulated* although
some minor or very specific rules may not be simulated.

Source: Own elaboration.

There are several partially simulated components in the Lithuanian
policy spine, e.g. social assistance benefit, unemployment benefit and
credited social insurance contributions. The policy is marked in the
model as ‘PART SIMULATED’. When there are some elements in the policy,
which are part-simulated, those are marked as taken ‘FROM THE DATA’.
E.g. in case of unemployment benefit (bunct_s) we take the benefit
duration from the data. I.e. for the observed unemployed (bunct \> 0) we
limit the benefit duration by the actual receipt in the data
–max(lunmy,bunmy). This is done to reduce over-simulation of
unemployment benefit duration, as not all recipients use the maximum
possible duration. A considerable part of unemployment benefit
recipients discontinues its receipt earlier than their eligibility would
suggest due to finding a new job.

## Main recent policy changes

In addition to changes in the level of taxes and benefits, as well as
their related calculation parameters or income lists, the following are
the main recent structural changes in the LT system (simulated
policies):

<span id="_Toc222228371" class="anchor"></span>**Table 2.3** Main recent
policy changes

| **Policies** | **2022 → 2023** | **2023 → 2024** | **2024 → 2025** |
|----|:--:|:--:|:--:|
| **Benefits** | X | X | X |
| **Social insurance contributions** | X |  |  |
| **Direct taxes** | Basic allowance increased | Basic allowance increased | Minor changes in the basic allowance calculation formula |
| **Consumption taxes** | Standard VAT rates applied to performance and sports services; tobacco and alcohol excises increased | Standard VAT rates applied to restaurant services; various excises increased |  |
| **Other** |  |  |  |

Source: Own elaboration.

### Main policy changes between 2022 and 2023

Since 1st of January 2023, childcare benefit is paid until the child
reaches either 1.5 year (18 months) or 2 years (24 months), where parent
can choose between the two leave options. Since January 1st, 2023, the
compensation rate for one-and-a-half-year period benefit is 60%, and for
two years period the compensation rate is 45% during the first year and
30% during the second year. Additionally, during childcare leave months
each one of the parents has a right to use 2 non-transferable months
with higher compensatory rate (4 months for a single parent). The
compensation rate for the two non-transferable months for each parent
(or four months for a single parent) is 78%.

The mandatory social insurance record for paternity benefit has been
reduced to 6 months over the last 24 months. Regarding unemployment
benefit, the insured's average monthly insured income is calculated as
the average of the 30 months that have passed until the end of the
previous calendar month from the day of acquiring the unemployed status.
If there is no insured income in any month, it is equal to zero in that
month.

The assets test is not applied for social assistance benefits, heating
and water compensations.

Since January 1st, 2023, different income thresholds applied for the
basic allowance: basic allowance of 625 EUR is applied to income below
MMS (840 EUR); for income between MMS and 1926 EUR, withdraw rate has
been increased up to 0.42 and for those whose income is above 1926 EUR,
regular withdraw rate and basic allowance is applied.

Since July 1st, the standard VAT rate was applied to performance and
sports services instead of the 9% reduced rate. Excises taxes on cigars
increased by 20%, cigarettes by 7% and other tobacco by 8%. The majority
of excise on alcohol rose by 10%, while the excise of ethyl alcohol rose
by 7%.

### Main policy changes between 2023 and 2024

From May, the assets test is re-applied for social assistance benefits,
heating and water compensations. Increased BSA, SSI, SPB, APB amounts
affecting many contributory and non-contributory benefits. The lower
limit of the maternity, paternity and childcare benefits increased to 8
BSA (since mid July 2023).

The thresholds and amounts of the basic allowances are changed: the
monthly basic allowance of 747 EUR is applied to income below MMS (924
EUR); for income between MMS and 2167 EUR the withdrawal rate is
increased to 0.5, for those whose income is above 2167 EUR, the
withdrawal rate of 0.18 applied (as before). The allowance is not paid
for incomes equal or higher than the 2864.22 EUR threshold. The amount
of the basic allowance is also increased for people with reduced working
capacity (level of participation).

The standard VAT rate is applied to restaurant services instead of the
9% reduced rate. Excises taxes on cigars increased by 20%, cigarettes by
7% and other tobacco by 8%. The majority of excise on alcohol rose by
10%, while the excise of ethyl alcohol rose by 7%. Gas oil increased by
10%.

### Main policy changes between 2024 and 2025

There were no substantial changes to social benefits, pensions, taxes
and contributions simulated in the model. The changes were mainly due to
regular indexation rules. Worth noting, a substantial increase in BSA,
SSI, SPB, APB amounts (by around 25-27%), which affected many
contributory and non-contributory benefits.

The thresholds and amounts of the basic allowances were changed, which
also normally happens on an annual basis: the monthly basic allowance of
747 EUR (as before) is applied to income below MMS (1038 EUR); for
income between MMS and 2387.29 EUR the withdrawal rate is 0.49, for
those whose income is above 2387.29 EUR, the withdrawal rate of 0.18
applied (as before). The allowance is not paid for incomes equal or
higher than the 2387.29 EUR threshold. The amount of the basic allowance
is also increased for people with reduced working capacity (level of
participation).

## Order of simulation and interdependencies

### Order of simulation in 2022-2025

In 2022-2025 the order of simulation remains unchanged.

<span id="_Toc222228372" class="anchor"></span>**Table 2.4** EUROMOD
Spine: order of simulation, 2022-2025

<img src="media/image1.png" style="width:5.90903in;height:7.07847in" />

<img src="media/image2.png" style="width:5.90903in;height:7.27986in" />

<img src="media/image3.png" style="width:5.90903in;height:2.69792in" />

Source: EUROMOD model.

## Policy switches

There are several standard switches included into the spine (see above):

- **neg_lt**: switched ON by default

  - recodes negative income to zero; currently this policy only recodes
    negative self-employment income to zero, initial value stored in
    i_yse0

- **yem_lt**: switched OFF by default

  - if hourly wage is lower than hourly minimum wage recalculated in
    accordance to the minimum wage, leaving hours of work as recorded in
    the data; if switched ON by using MWA extension, it overwrites yem.

- **FYA_lt**: switched ON by default in 2020 and 2021 (see previous
  reports for detail).

- **boa00_lt**: switched OFF by default.

  - old-age pension indexation of boa, bdi and boact, where they can be
    calculated according to the pension formula. Since 2018, the
    conversion coefficient (0.78) is applied when recalculating former
    pension records into the point system.

- **TCA_lt:** switched OFF by default

  - tax compliance adjustment can be turned on since year 2017, where
    the data tax evasion corrections can be switched ON.

- **HHoT – Unemployment extension (HHoT_un)**: switched ON by default
  with HHoT data

  - this extension improves the simulation accuracy of the unemployment
    insurance benefit when EUROMOD is run with hypothetical data. For
    instance, in most countries the legislation of this benefit requires
    information on variables such as individuals’ employment history,
    which are not available in SILC; we can define these variables in
    HHoT and use them to simulate the policy’s rules more precisely when
    running the model with hypothetical data.

- The **HHoT Monthly Unemployment (HHoT_mu):** extension enables a
  monthly unemployment benefit simulation, similar to the approach used
  by the OECD TaxBEN for the calculation of monthly Net Replacement Rate
  (NRR) indicators. Those indicators measure to what extent a person's
  previous income from work is maintained after a certain number of
  months in unemployment. With this extension, unemployment benefit
  amounts are calculated with respect to a *specific month* of the
  unemployment spell and are then converted to annual amounts by
  multiplying by 12. By default, this extension is switched off; it is
  only set to on when the model is used for the calculation of the NRR
  indicators.

- **Benefit Calibration Adjustments (BCA):** switched OFF by default

  - this extension allows the user to calibrate the receipt of benefits
    to match the simulated total expenditure of a benefit to real
    expenditure from external statistics. The extension is implemented
    for the simulation of the social assistance benefit (bsa00_lt). The
    default for the baseline is off. When the extension is on, a subset
    of eligible of observations is selected randomly as beneficiaries so
    that the real expenditure is reached, removing the benefit from the
    rest of the eligible observations; when off, all eligible
    observations are kept as beneficiaries. This extension shares most
    of its functions with the BTA extension; as a general rule, only one
    of the extensions should be on, but if both are, the lowest rate
    between the take-up rate and the calibration rate will be applied.
    More details on the specific implementation of BCA and BTA
    extensions are provided in the subsections describing the
    corresponding benefit.

- **Benefit Take-Up Adjustments (BTA):** switched OFF by default

  - This extension allows the user to apply non-take-up corrections.
    The extension is used for the simulation of social assistance
    benefit (bsa00_lt). The default for the baseline is off. When the
    extension is on, a share of (weighted) eligible observations equal
    to the take-up rate is selected randomly as beneficiaries, removing
    the benefit from the rest of the eligible observations; when off,
    all eligible observations are kept as beneficiaries. This extension
    shares most of its functions with the BCA extension; as a general
    rule, only one of the extensions should be on, but if both are, the
    lowest rate between the take-up rate and the calibration rate will
    be applied. More details on the specific implementation of BCA and
    BTA extensions are provided in the subsections describing the
    corresponding benefit.

- The **Consumption Inflation Adjustment (CIA)** extension enables users
  to simulate price (inflation) shocks under the assumption that
  households do not immediately adjust their consumption patterns
  (constant quantities) in response to a sudden change. This extension
  can only be enabled if used together with Consumption Taxes add-ons
  CT_XBASE and CT_XCQ, respectively baseline and constant quantities. By
  default, this extension is switched OFF. Switching ON the inflation
  simulation (without changing parameters) allows users to apply
  [official annual inflation
  rates](https://euromod-web.jrc.ec.europa.eu/sites/default/files/Inflation_rates_by_product_category.xlsx)
  between two consecutive years (sourced from
  [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_manr/default/table?lang=en)
  and [DG ECFIN’s latest quarterly
  forecasts](https://economy-finance.ec.europa.eu/document/download/6e6837c1-e00c-42ed-9f10-8d1ad56f913a_en?filename=spring_forecast-2024_statisical%20annext_en.pdf))
  as stored in the Consumption Taxes (CT) table by
  *\$tco_base_upr\_\[COICOP\]*. Users can also simulate their own
  hypothetical price shock scenarios at COICOP level 1 (2-digits)
  categories, with the Housing & Utilities split between Energy and
  other. To do so users should modify constants *\$tco_CIA\_\** in
  *ConstDef_cc*. For example, what if annual inflation for food was 5%
  instead of the officially recorded? Changing *\$tco_CIA_01* to 5% for
  food and non-alcoholic beverages, multiplies the expenditures of foods
  and non-alcoholic beverages by 1.05. For the CIA extension to work
  properly, the users will need to add a new variable *ydsyc_a* to the
  input data recording for each household the disposable income growth
  between two consecutive years. \[HINT: Run systems *t* and *t+1*.
  Compute household disposable income for each year. For each household
  calculate *ydsyc_a* = *(hh_dpit+1 – hh_dpit)/hh_dpit*\]

## Minimum wage

### Brief description

Minimum wage is usually changed as of 1st of January.

### Definitions and eligibility conditions

The unit of analysis is individual. If the actual wage is less than
minimum wage, then wage is replaced with minimum hourly wage times
actual working hours.

### Amount

It is either defined in monthly or hourly terms.

<u>EUROMOD note:</u>

Monthly income from employment (taking into account the number of months
in work) is set equal to minimum wage (proportional to the hours worked)
if the income from employment is less than minimum wage and is positive,
and if working hours are less than or equal to 40 hours per week. We do
not apply the minimum wage correction when a person earns more than a
monthly minimum wage, but their hourly wage is still less than a minimum
wage.

By default, the simulation of minimum wage is set off, i.e., is not part
of the baseline.

## Benefits

### Single person benefit (bsg_s)

#### Brief description

single person benefit is granted to single adults with a working
capacity level of up to 55% and persons who have reached the statutory
retirement age and do not receive any widow’s or orphan’s benefit or
these benefits are lower than the single person benefit.

#### Eligibility conditions

Individuals are entitled to a single person benefit if their working
capacity (participation) level is up to 55% or they have reached the
statutory pension age and declared their place of residence in the
Republic of Lithuania or included in the records of individuals who have
not declared their place of residence. They have to be either not
married, their marriage has ceased to exist or are widows that receive
no social insurance suvivors’ pension, state suvivors’ pension, state
suvivors’ annuity and/or a periodic pension benefit from a foreign
state, or the amount of the benefit received (the total of these
benefits) is less than the single person benefit or do not receive the
social insurance widow’s pension and/or a state widow’s pension because
instead of these widows’ pensions they have chosen to receive the social
insurance orphan’s pension and/or the state’ orphan’s pension.

Before 2022, the receipt of the benefit was linked to the receipt of
certain types of pensions or was paid to people who lost up to 60% of
their working capacity. No major changes in 2025.

#### Income test

No income test applied.

#### Benefit amount

The amount of the benefit was 32 EUR in 2022, 34.89 EUR in 2023, 38.23
EUR in 2024 and is 42.29 EUR in 2025. The benefit is not taxable.

### Birth grant (bchba_s)

#### Brief description

This benefit is a non-contributory lump-sum cash benefit paid upon the
birth of a child.

#### Definitions

The primary unit of analysis is family.

#### Eligibility conditions

The benefit is paid to one of the parents (adoptive parents) or a
guardian of a child born that year.

#### Income test

No income test applied. As it is a one-off lump-sum benefit, it is not
included for income testing for the social assistance and the additional
child benefits.

#### Benefit amount

The benefit amounts to 11 BSA per eligible dependent child during the
entire 2022-2025 period, which is 770 EUR in 2025. The benefit is not
taxable.

### Universal child benefit (bchnm_s)

#### Brief description

It is a non-contributory monthly cash benefit for each dependent
(guarded) child until they reach the age of 18 or below 23 if in
full-time general education, including those in vocational education,
also while on leave due sickness, pregnancy, or childbirth

#### Definitions

The unit of analysis is the family.

#### Eligibility conditions

The benefit is paid to all families and care institutions (irrespective
of their care form: non-governmental guardianship institution,
family-type guardianship institution or childcare institution) having
one or more dependent (guarded) children up to the age of 18 or below
the age of 23 if in full-time general education (including those in
vocational education, also while on leave due sickness, pregnancy, or
childbirth).

#### Income test

No income test applied.

#### Benefit amount

The benefit level is calculated in relation to the BSA. Since January
1st, 2021, the child benefit is set to 1.75 BSA per child, which is
122.5 EUR in 2025 [^47]. The benefit is not taxable.

### Additional child benefit (bch00_s)

#### Brief description

It is a non-contributory monthly cash benefit paid to a family raising
one or more children up to the age of 18 or under 23 if in full-time
general education (including those in vocational education, also while
on leave due sickness, pregnancy, or childbirth) if satisfying one of
the three conditions: have three of more children, have a child with
disability, or have up to two children and family’s income is below the
certain income threshold. Until 2021, the lower age threshold was used
to define children (until 21 years of age).

#### Definitions

The unit of analysis is the family as defined in section 2.5.2.

#### Eligibility conditions

To receive this benefit, a family with child(ren) has to satisfy one of
the three conditions: must have three of more children, have a child
with disability, or have up to two children and family’s income is below
the certain income threshold.

#### Income test

The income test is applied only for families raising up to two children,
while the benefit is paid without any income testing for families with
three or more children or when raising a child with disability. To
receive the additional child benefit for families with up to two
children, an income test is applied based on the same income definition
as for the social assistance benefit - (monthly income per each family
member can’t exceed the threshold of 2 SSI [^48]).

#### Benefit amount

The benefit level is 1.03 BSA, which equals to 72.1 EUR in 2025
(<span class="mark"></span>[**Table 2.5**](#Table_02_05) ). Only one
additional benefit can be paid for the same child (e.g. if a child has
disability and is from a low-income family, child’s parents are eligible
only for one additional child benefit of 1.03 BSA per child per month).
The benefit is not taxable.

<span id="Table_02_05" class="anchor"></span>**Table 2.5** Additional
child benefit coefficients on January 1, 2022– 2025

<table style="width:53%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 14%" />
<col style="width: 17%" />
</colgroup>
<thead>
<tr>
<th rowspan="2" style="text-align: center;">Family type</th>
<th colspan="2"
style="text-align: center;"><strong>2022-2025</strong></th>
</tr>
<tr>
<th style="text-align: center;"><strong>Income test
applied</strong></th>
<th style="text-align: center;"><strong>Benefit amount per
child</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Families with 1-2 children</td>
<td style="text-align: center;">Yes</td>
<td rowspan="3" style="text-align: center;">1.03*BSA</td>
</tr>
<tr>
<td>Families with 3+ children</td>
<td style="text-align: center;">No</td>
</tr>
<tr>
<td>Families with a child with disability</td>
<td style="text-align: center;">No</td>
</tr>
</tbody>
</table>

Source: Based on Law of Benefits to Children and its relevant amendments
& Temporary Law on Recalculation and Payment of Social Benefits.

<u>EUROMOD note:</u>

Due to data limitations, it is not possible to distinguish guardians
(caregivers) from the data, thus cannot be simulated for them. There is
no information on disability level in the input database.

### Pregnancy grant (bmaprnc_s)

#### Brief description

This non-contributory benefit is a lump-sum cash benefit paid to a
pregnant woman upon the 28th week of the pregnancy when she is not
entitled to receive the maternity leave benefit from the social
insurance fund.

#### Definitions

In principle, the primary unit of analysis would be family as defined in
section 2.5.2. However, for technical reasons we define a separate
family unit, which consists of partners and their own dependent children
who are less than 3 years old.

#### Eligibility conditions

The benefit is paid to pregnant women who are not eligible to receive
the maternity leave benefit (See more benefit details in Section 2.5.6.)
and is paid 70 days before the term of childbirth.

#### Income test

No income test applied.

#### Benefit amount

The benefit is 6.43 BSA, which equal to 450.1 EUR in 2025. The benefit
is not taxable. No changes in 2022-2025.

<u>EUROMOD note</u>:

Instead of pregnant women, mothers with an own child aged 0 are
considered.

### Maternity leave benefit (bmaprct_s)

#### Brief description

This contributory benefit is a cash benefit paid to a pregnant woman who
have the required on the basis *Law on Sickness and Maternity Social
Insurance* contributory history. The maternity leave benefit is paid as
a lump sum amount for the number of working days in the *applicable
period (see below)*. If the applicable period stretches into a different
calendar year, the benefit could be paid in two lump-sum amounts.

*<u>Applicable period:</u>*

The benefit is paid to women for a total of 126 calendar days, which
covers the period before the childbirth (70 days) and after the delivery
(56 days). In the case of complicated childbirth or if more than one
child was born, the additional 14 days are added to the total period.

#### Definitions

The unit of analysis is the family as defined in section 2.5.2.

#### Eligibility conditions

The benefit is paid if women before the first day of the maternity
leave, had sickness and maternity social insurance record of no less
than 12 months over the last 24 months. The maternity leave benefit is
also paid for those mothers who had a qualifying period of no less than
12 months over the last 24 months but were not employed or insured
during pregnancy period.

#### Income test

No income test applied.

#### Benefit amount

The maternity benefit is equal to a set percentage of the recipient’s
average monthly insured income (AMII) (see chapter 1.1 for more
details), and is calculated as:

B = S\*X% \* D, *where:*

B is maternity benefit; and B\>= min B (minimum level)

S is a daily compensatory salary; S\<= (levels are not specified)

D is the number of working days in the applicable period.

The daily compensatory salary (“S”) is calculated by dividing the
beneficiary’s monthly income (using the month, when the beneficiary has
been granted a right to this entitlement) by the number of working days
in that month.

The maternity benefit is equal to 77.58% of the recipient’s compensatory
income, but cannot be lower than 8 BSA[^49]. The lower limit of the
maternity benefit increased from 6 BSA in 2022, to 7 BSA in 2023 and
since mid-July, 2023 it is 8 BSA.

Since January 1st, 2021, self-employed persons are eligible to receive
maternity benefit if they have paid social insurance contributions on at
least 1 MMS on a monthly basis and have required insurance period for
maternity benefit. If contribution amount is paid from less than 1 MMS,
the period o of the insured income is considered to be proportionally
shorter. The self-employed who are entitled to the maternity benefit,
the benefit are paid regardless of their income from self-employment,
i.e., the maternity benefit amount will not be reduced if the person
receives income from self-employment during the maternity benefit
payment period. However, the benefit is reduced if employment income or
other benefits (e.g., sickness benefit) are received. The amount of
state-funded insurance for a person with the status of an artist is also
not taken into account when paying maternity benefit. No changes in
2022-2025.

<u>EUROMOD note:</u>

The payment for additional 14 days is currently not simulated due to
data constraints.

As information on the social insurance contribution period is not
available, all mothers with an own child aged 0 in EUROMOD are
considered eligible if they have been in work for more than six months
in the current year [^50] (as suggested by observed patterns in the
underlying data).

The AMII is approximated in EUROMOD (thereby, also for other relevant
family benefits) using either estimated hourly wage rate multiplied by
work hours per month (i.e. 168 hours on average) or observed monthly
earnings.

Due to data limitations, it is not possible to distinguish whether a
woman, receiving maternity benefit, previously was unemployed or not
insured.

### Paternity leave benefit (bplct_s)

#### Brief description

The contributory benefit to fathers (adoptive fathers) of a new-born,
who have the required *Sickness and Maternity Social Insurance*
contributory history The benefit for 30 days in total can be claimed
from the birth of the child until the child reaches the age of 1 year.

#### Definitions

The unit of analysis is the family as defined in section 2.5.2. Insured
income (AMII) definition is presented in section 1.1.

#### Eligibility conditions

Before the first day of paternity leave (which is of 30 days), a father
(adoptive father) must have no less than 6 months over the last 24
months of contribution history. Before 2023, the required contribution
period was 12 months over the last 24 months of contribution history
[^51].

There is a statutory requirement to have a legal acknowledgement of the
fatherhood of the child in case child was born outside marriage. [^52]

#### Income test

No income test applied.

#### Benefit amount

The amount of paternity benefit is calculated as a percentage of the
benefit recipient’s AMII (see chapter 1.1 for more details). The
paternity benefit calculated for 30 days and is equal to 77.58% of the
recipient’s compensatory income[^53], but cannot be lower than 8 BSA and
not higher than 2 national average monthly salaries (AMS) The lower
limit of the paternity benefit increased from 6 BSA in 2022, to 7 BSA in
2023 and since mid-July, 2023 it is 8 BSA.

As of January 1st, 2021, self-employed persons [^54] who have acquired
the right to the paternity benefit, receive the benefit regardless of
their income from self-employment, i.e., the paternity benefit amount
will not be reduced if the person receives income from self-employment
during paternity benefit payment period [^55]. However, the benefit is
reduced if employment income or other benefits (e.g., sickness benefit)
are received. The amount of state-funded insurance for a person with the
status of an artist is also not considered when paying paternity
benefit. If contributions are paid on the incomes which are below 1
minimum monthly wage (MMS), the contributory period is proportionally
shortened.

<u>EUROMOD note:</u>

As information on social insurance record is not available in EUROMOD,
all fathers with an own child aged 0 are considered eligible. The
requirement of having a legal acknowledgement of fatherhood cannot be
simulated in the model.

### Childcare benefit (bmact_s)

#### Brief description

This contributory benefit is a monthly benefit to one of the parents
(adoptive parents) or a guardian or a grandparent to take care of a
child until they reach either 18 or 24 months, granted on the basis of
*the Law on Sickness and Maternity Social Insurance* each parent (but
not a grandparent) has a right to use 2 non-transferable months with the
higher compensatory rate. Single mothers / fathers have the right to use
4 months with the higher compensatory rate.

#### Definitions

The unit of analysis is the family as defined in section 2.5.2. Insured
income definition is presented in section 1.1.

#### Eligibility conditions

The benefit is granted if a person, before the first day of the
childcare leave, have no less than 12 months over the last 24 months of
contribution history. The childcare benefit is paid after the end of the
maternity leave or the paternity leave, however if a mother did not
receive maternity leave benefit, this benefit for other eligible person
can be calculated as of the birth of the child. The childcare benefit
can also be paid to one of the grandparents if he/she satisfies the same
contributory requirements and one of the child’s parents has the right
to the benefit.

Each of the parents has the right to use two non-transferable childcare
months (or four months for a single parent) with higher compensatory
rate. This right is not extended to grandparents. The contribution
history of the last 12 months is considered when calculating childcare
benefit during the non-transferable months.

In cases where a recipient of maternity leave and has given birth to
more than one child or is caring for two or more children at the same
time, childcare benefit for others those entitled to it may be granted
from the date of the birth of the child or from the first day after the
end of parental leave.

#### Income test

No income test applied.

#### Benefit amount

The amount of the childcare benefit is calculated as a percentage of the
recipient’s AMII (see more details in chapter 1.1) but cannot be lower
than 8 BSA or higher than two country’s average monthly wages. The lower
limit of the childcare benefit increased from 6 BSA in 2022, to 7 BSA in
2023 and since mid-July, 2023 it is 8 BSA. Duration and the compensation
rate of the childcare benefit can be chosen between two available
options – until child reaches 18 or 24 months of age. Since January 1st,
2023, the compensation rate for one-and-a-half-year period benefit is
60%, and for two years period the compensation rate is 45% during the
first year and 30% during the second year. The compensation rate for the
two non-transferable months for each parent is 78% (see [**Table
2.5**](#Table_02_05) ; rules until 2022 are presented in
<span class="mark"></span>[**Table 2.6**](#Table_02_06) ).

If one of the parents receiving childcare benefit qualifies for another
childcare benefit for other child, she or he receives both benefits, but
the total amount of the benefits cannot exceed 78% of the earnings on
which these benefits are calculated. This is, however, not modelled (see
EUROMOD note below).

Since 1st of January 2023, if a person receiving the childcare benefit
has insured income during the non-transferable months, the benefit is
reduced (this does not apply to single parents, i.e. their benefit is
not reduced). However, other types of insured income can be received
during the other childcare leave months, but the total amount of the
benefit and insured income combined cannot exceed 100% of the monthly
compensatory earnings of that person (based on which the childcare
benefit was calculated), but not higher than 5 national average monthly
salaries (since 2024). These conditions do not apply for self-employment
income, i.e., the person can have self-employment income throughout the
childcare leave and it will not affect the benefit amount.

<span id="Table_02_06" class="anchor"></span>**Table 2.6** The
compensation rate of childcare benefit, 2023- 2025 (as of 1st January)

|  | **2023 – 2025** |
|----|----|
| Duration | Optional, until child reaches 18 or 24 months of age (1.5 or 2 years) |
| The non-transferable months\* | 2+2 months for each parent (4 months for a single parent) |
| Compensation rate during non-transferable months, % | 78% |
| Compensation rate during the rest of the months | 60% for the 1.5-year option or 45% in 1<sup>st</sup> year/30% in 2<sup>nd</sup> year for the 2 years option |
| Benefit amount multiplied with \# of births | Yes, but cannot exceed 78% of the earnings on which the benefit is calculated |

Notes: \* For single parents, 2 additional non-transferrable months for
the absent parent are paid during the last two childcare leave months,
e.g., during 16-17 childcare leave months or 23-24 childcare leave
months.

Source: Based on the Law on Sickness and Maternity Social Insurance

<span id="_Toc222228375" class="anchor"></span>**Table 2.7** The
compensation rate of the childcare benefit, 2022 (as of 1st January)

|  |  | **2022** |
|----|----|----|
| Duration |  | Optional, until child reaches 1 or 2 years of age |
| Compensation rate 1<sup>st</sup> year, % |  | 77.58/54.31 |
| Max. benefit duration the 1<sup>st</sup> year, months\* |  | 12 |
| Compensation rate 2<sup>nd</sup> year, % |  | 0/31.03 |
| Max. benefit duration the 2<sup>nd</sup> year, months |  | 0/12 |
| Benefit size multiplied with \# of births |  | Yes, but cannot exceed 77.58% |

Notes: \* If a mother/father has received a maternity leave or paternity
leave benefit, the payment duration is reduced by the time (56 days and
1 month respectively) for which the relevant benefit has been paid.

Source: Based on the Law on Sickness and Maternity Social Insurance

<u>EUROMOD note:</u>

- As information on the social insurance contributions is not available,
  all mothers with an own child aged 2 or below are considered eligible
  if they have been in work for more than six months in the current year
  [^56] (as suggested by observed patterns in the underlying data).

- Two years of receipt for childcare benefit is modelled by default as
  the absolute majority of recipients choose this option (around 93%
  according to the latest available statistics provided on request by
  MoSSL).

- Alternatively, simulations of opting for different options of
  childcare benefit are integrated in EUROMOD through the constant
  \$MA_optDef.

- The recipient is always assumed to be the mother; father if there is
  no female partner in the household or mother is not eligible.

- In case there are several children eligible for the childcare benefit
  in the family, we model one parent to receive the benefit for both
  children.

- Non-transferable months are modelled with an assumption that the first
  parent (mother or father if no mother) takes those at the beginning of
  the childcare leave and the second parent (father) takes those at the
  end of the childcare leave period.

- The receipt of the childcare leave benefit with earnings (and
  potential benefit reduction) is not modelled due to data limitations.

### Benefit for multiple-births (bchmp_s)

#### Brief description

The non-contributory monthly benefit paid to one of the parents due to
the birth of two or more children at the same time. The benefit is paid
from the birth of the children until they reach the age of 2 years.

#### Definitions

The unit of analysis is the family as defined in section 2.5.2. Basic
social allowance definition is presented in section 1.1.

#### Eligibility conditions 

The benefit is granted due to the birth of two or more children at the
same time and is paid to one of the parents.

#### Income test

No income test is applied. As this is a regular payment for children, it
is included for the income test for the social assistance and child
benefits.

#### Benefit amount

The benefit level is calculated in relation to BSA and varies based on
the number of children born at the same time. The benefit amount is 4
BSA (EUR 280 in 2025) if twins are born. If more than two children are
born at the same time, the benefit amount increases by 4 BSA per child.
So, if three triplets are born, the benefit amount is 8 BSA. No changes
between 2022-2025.

###  Childcare benefit for students (bmaed_s)

#### Brief description

The non-contributory monthly benefit is granted to one of the child’s
parents (adoptive parents or guardians) during the period or training or
studies and 12 months after graduation, if they are not entitled to the
contributory childcare benefit.[^57] The benefit is paid until the child
reaches the age of 2 years.

#### Definitions

The unit of analysis is the family as defined in section 2.5.2. Basic
social allowance definition is presented in section 1.1.

#### Eligibility conditions 

The benefit is granted if a person studies (studied) in full-time
general education, formal vocational training or tertiary education
programme, or studies (studied) in doctoral studies or medical residency
and according to *the Law on Sickness and Maternity Social Insurance* is
not entitled to the contributory childcare benefit. The benefit is not
paid, if one of the parents is entitled to the childcare benefit for the
same child according to *the Law on Sickness and Maternity Social
Insurance.* To avoid double granting of the benefit for a later born /
adopted / foster child, the benefit is paid for the care of the youngest
child until they reach the age of 2. No changes in 2025.

#### Income test

No income test is applied.

#### Benefit amount

The benefit of 6 BSA (420 EUR in 2025) is paid until the child reaches
the age 2. If two or more children are born (adopted) the benefit’s
amount does not increase, but is paid until the youngest child reached
the age of 2 years.

###  Social assistance benefit (bsa00_s) 

#### Brief description

This means-tested monthly benefit is granted to families or single
persons as a last-resort financial assistance. The social assistance
benefit is granted for three months. The application must be
re-submitted upon the benefit expiration, unless local authorities have
granted the benefit for the period exceeding three months (i.e., if the
composition and income of the family has not changed).

BTA and BCA extensions are off, so the baseline model neither adjusts
for non-take-up of the benefit nor calibrates its receipt, but the user
can activate them if necessary. See section 2.4 for technical details on
both extensions and their interactions.

Users can enable the necessary extensions in Country Tools/Set Default.
For proper functioning, the extensions require the following inputs:

BTA: The estimated take-up rate of the benefit should be set as the
value of the \$bsa_BTA_rate constant in the model. Currently, the value
is set to 1, indicating no adjustment for non-take-up.

BCA: The aggregate expenditure needs to be filled out in the External
Statistics table, so that the calibration rate (\$bsa_BCA_rate) is
computed accordingly. Data are currently available for the years
2018-2023; given the absence of information for later years, the
calibration rate is not computed within the later systems, but the one
computed within the 2023 system is used instead. For the modelling of
reforms to allow for variation in the number of beneficiaries (hence
expenditure): beneficiaries will change when the eligibility conditions
change by applying the share of 2023 to the new pool of eligible units.
If previous systems were used for reforms, total expenditure would
remain constant irrespective of the reform applied, since the model
would always stick to the existing external statistics.

#### Definitions

The unit of analysis is family, which is either a single person (see
definitions below) or consists of partners (married of cohabiting) and
their own dependent children. Dependent children are children under 18
or under 24 if in general, higher or vocational education, including
periods of academic leave due to illness or pregnancy, until they reach
the age of 24 and between the date of completion of the general
education program and 1st of September (the beginning of the school or
study year) of the same year [^58]. Children cannot be married,
cohabiting with a partner nor parents themselves, but they can work and
receive income up to 1 SSI.

*Single person* is a person aged 18 and above and either is not married
and reside alone; or is married, but residing alone by the court’s
judgement; or is married with children, but residing alone, as their
children are staying with their spouse by the court’s judgement.

#### Eligibility conditions

1.  All family members or single persons are entitled to the social
    assistance benefit if they comply with all three requirements: The
    value the value of *family’s* or person’s assets does not exceed the
    *ratio of state established property value* (RP) (see Assets test).
    This requirement does not apply for the first three months.

2.  The average income used to calculate the benefit is less than 1.1
    SSI per person;

3.  Every person over the age of 18, single person or child (adoptee)
    between 16 and 18 years of age meets at least one of the conditions
    specified below (those in italic cannot be simulated):

    - if under 24 years of age, be in general, vocation or tertial
      education, including periods of academic leave due to illness or
      pregnancy, until they reach the age of 24 and between the date of
      completion of the general education program and 1st of September
      (the beginning of the school or study year) of the same year;

    - be employed for at least two thirds of the full-time equivalent or
      earning at least two thirds of the MMS;

    - self-employed with income of at least a monthly minimum salary;

    - reached the statutory retirement age;

    - receive pensions (except the state social insurance disability
      pension granted to a person with the lowest disability level or
      45-55% working capacity;

    - registered with the Public Employment office;

    - *officially nursing (providing assistance, care) another family
      member;*

    - *is undergoing treatment in an in-patient health care institution
      for at least a month;*

    - *is pregnant woman and less than 70 calendar days are left before
      a baby is due (28 or more weeks of pregnancy);*

      - is a mother or a father (a guardian or a curator) who raises at
        home a child under certain age and care conditions as prescribed
        in the same law:

      - if a family raises a child under three years old, who does not
        attend a pre-school educational establishment;

      - if a family raises three or more children under age of 14 and at
        least one of the children is under age 8 and does not attend a
        pre-school educational establishment or a school;

      - if a child under 8 years old does not attend a pre-school
        educational establishment due to medical recommendations or due
        to overcrowded schools**;**

    - *is a person from 16 and up to 18 years of age and either attends
      an institution of formal education; is with disability; is,
      registered with the Public Employment Office (i.e. unemployed) or
      is a pregnant woman.*

    - *one of the grandparents takes care of a child up to the age of 3,
      when childcare leave has been granted.*

    - *children under 16: included unconditionally.*

***Means test***

Assets and income tests are applied.

***Assets test:***

Family’s or person’s actual assets (AS) must be lower than the *ratio of
state established property value* (RP), which is calculated in the
following way: AS \<= RP = RE+RM, where

**AS** is the actual value of a family’s or person’s assets. AS is
established by calculating the value of the following family’s or
person’s assets:

- buildings, including those under construction;

- vehicles subject to registration;

- agricultural machinery subject to registration;

- land (including that occupied with forests and water bodies);

- livestock, poultry, animals, hives, if their total value exceeds EUR
  1,160;

- stocks, bonds, bills of exchange, and other securities, shares, if
  their total value exceeds EUR 580;

- works of art, gems, jewellery; precious metals, when the value of a
  unit exceeds EUR 580;

- cash resources if their total value exceeds EUR 580, except for child
  maintenance payments;

- received (unpaid) loans, if their total value exceeds EUR 580 except
  of state loans for the students studying at the higher education
  institutions, loans for modernization of housing and real estate
  mortgages;

- money lent to other individuals (and unpaid), if their total value
  exceeds EUR 580;

- *state compensations for real property purchased by the State,
  restored savings and other restored resources.*

In order to evaluate AS, applicants for social assistance benefit must
declare their assets. Then the declared number of properties is checked
with the registry data [^59]. If the value of the declared property is
extraordinarily low, officials have a right to establish property value
using *average market value*, as approved by the Commission for the
Assessment of Property Subject to Registration.

**RE** is the “ratio of real estate value” and is calculated as:

RE =

*Notional size of residence* (60m2 for the 1st person + 15m2 for each
additional family member) x *average market price of the residence*
(which is approved by the Commission for the Assessment of Property
Subject to Registration on 1st February 1st May, 1st August and 1st
November of each year).

\+

*Notional size of land area* per family or person x *average market
price of the land*.

The state requires application of the following notional sizes of land
per family:

- residential purpose land: in cities – 6 Ares,[^60] in towns and
  villages – 25 Ares;

- agricultural purpose land (if the plot does not exceed 1 hectare
  [^61]): in cities – 6 Ares, in towns and villages – 25 Ares;

- agricultural purpose land (if the plot exceeds 1 hectare): in cities –
  6 Ares, in towns 25 Ares and villages –6 hectares;

- other purpose land: in cities – 6 Ares, in towns and villages –25 Ares
  hectares.

if a person does not have land - the value of the notional size of the
land area is based on 1 hectare of agricultural purpose land.

RM is the “ratio of value of movables”, which is calculated per family
member:

- 35 SSI for the first or single person aged 18 or above;

- 25 SSI for each additional person aged 18 or above;

- 20 SSI for each person (child) under 18 years old.

The assets test will not be applied for at least 3 months for persons
either applying for the social assistance benefit for the first time, or
24 months after receiving the social assistance benefit [^62]. The
assets test was not applied until 30th of April, 2024[^63].

#### Income test 

For the purpose of means testing, the average family or person’s income
(IL) is calculated as: the average income of all family members during
the period of three months prior to the month when the family (single
resident) acquired the right to the social assistance benefit. All
income should be taken after the deduction of withholding income tax and
employee social insurance contributions. Incomes defined by the same
social assistance law, namely compensations for housing utilities and
the social assistance benefit itself, are not taken into account for
means testing.

The following incomes are included in the means-test [^64] unless
otherwise specified (***those in italic cannot be simulated***):

- income received under an employment contract or other legal
  relationship equivalent to an employment relationship, including per
  diems, subsistence allowances, food allowances and other income
  (except for persons under 18 years of age);

- income from the authorship contracts (royalties), income received from
  sports activities, artist activities;

- all types of pension benefits except the survivors’ pensions, the
  additional old-age or lost working capacity (invalidity) pension
  bonuses;

- dividends and interests;

- *income of an owner of an individual company, received from the
  taxable profit of such company;*

- *income received from the individual activity under a business
  certificate (except for persons under 18 years of age*)

- 70% of self-employment income (except from persons under the age of
  18)[^65];

- income from agricultural activities *(except of income from gardens of
  members of gardeners’ societies, the area of land plots of which does
  not exceed 3 hectare);a) in the absence of accounting documents,
  average monthly income should be calculated by applying the ratios of
  income from agricultural activities evaluated according to the state
  approved notional costs; b) if there is no possibility for determining
  income according to these ratios, average monthly agricultural income
  should be calculated by applying a state approved income rate per
  hectare of agricultural land; and payments for agricultural
  activities;*

- Alimony and benefits to children paid under the Law on Child
  Maintenance Payments

- all regular income of a social nature, i.e., state transfers, *with
  the exception of compensations of transport costs for the people with
  disabilities and compensations for donors, temporary childcare
  allowance* regular social benefits for children (including child
  benefits and all kinds of stipends) are included into the income test.
  Non-regular social benefits for children (e.g. birth grant) are not
  included into the income test;

- unemployment social insurance benefit, severance pay or compensation
  paid upon the termination of an employment contract or upon the
  dismissal of public servants, temporary jobseeker’s benefit;

- sickness, maternity, and childcare benefit and occupational
  rehabilitation benefits;

- compensation for property and non-pecuniary damage (including one-time
  compensation for lost working capacity);

- cash donations if their total amount exceeds the amount of 1\*SSI;

- cash received as a gift;

- inherited cash;

- cash resources received abroad or from a foreign state;

- income from property rent and income from property sale (unless it is
  included into assets);

- lottery and other cash winnings, prizes;

#### Income disregard 

When assessing the income, parts of income are disregarded, which
depends on family composition. A part of family’s (person’s) average
income from work included into income test is disregarded. As well as a
part of unemployment social insurance and the temporary jobseeker‘s
benefit are included into income disregards. No changes in 2022-2025.

<span id="_Toc222228376" class="anchor"></span>**Table 2.8** Levels of
income disregard based on household type, 2022-2025 (as of 1st January)

| **Household type** | **2022-2025** |
|----|:--:|
| For persons living together without children (adoptees) or for single person | 20% |
| For persons living together and raising one or two children (adoptees) | 25% |
| For persons living together and raising three or more children (adoptees) | 30% |
| For single parents, raising one or two children (adoptees) | 35% |
| For single parents, raising three or more children (adoptees) | 40% |

Source: Law on Social Assistance for Low-Income Residents

***Benefit amount***

The amount of the social assistance benefit is calculated:

- For a single person:

  - as the difference between 1.4\*SSI and income for the first 6
    months;

  - as the difference between 1.2\*SSI and income for subsequent 6
    months;

  - as the difference between 1.1\*SSI and income after 12 months.

- For households:

  - For the first person in a family, as the difference between 1.1\*SSI
    and income;

  - for the second person in a family, as the difference between
    1.1\*SSI and 90% of income;

  - for the third and a following person in a family, as the difference
    between 1.1\*SSI and 70% of income.

The benefit amount is reduced for a single person who is able to work
but not working or family having a person who is able to work but not
working and receiving benefit during the long period, excluding
children:

- by 20% after 12 months of payment;

- by 30% after 24 months of payment;

- by 40% after 36 months of payment;

- by 50% after 48 months of payment;

- after 60 months the benefit payment of 50% is provided in a
  non-monetary form.

The social assistance benefit (*in-work social assistance benefit*) can
be additionally paid when a person meets all these conditions:

- a single person or one of the family members starts working and
  receives not less than the MMS (or minimum hourly wage proportional to
  hours worked);

- prior employment the person was registered with the Employment Service
  for at least 6 consecutive months and during this period did not work
  or worked less than 2/3 of the full-time equivalent, earning less than
  the minimum wage, or worked in the jobs provided for in the employment
  promotion program;

- persons living together or one person living together were recipients
  of social assistance benefits for at least one month during the last 3
  months before employment;

- the application-application for granting an additional part of the
  social allowance upon employment is submitted no later than within 12
  months of employment.

The in-work social assistance benefit is granted and paid for each month
worked under an employment contract or a legal relationship equivalent
to an employment relationship, but no longer than 12 months. The benefit
amount decreases with time:

- for the 1st -3rd months - 100 % of the average amount of the social
  allowance paid during the previous 6 months before employment;

- for the 4th – 6th months – 80% of the average amount of the social
  allowance paid during the previous 6 months before employment;

- for the 7th to 12th months - 50% of the average amount of the social
  allowance paid during the previous 6 months before employment.

<u>EUROMOD note:</u>

The EU-SILC database does not contain information on assets value.
Therefore, most of the information on the assets listed above is not
available in EUROMOD. Proxy for the assets test is based on the notional
size of dwelling and land compared to reported and/or imputed actual
size of dwelling and land in the national SILC data. The following
imputations have been made (except for 2021):

- Residential property: actual size based on the EU-SILC variables on
  housing characteristics (area in m2); notional size as described above
  (60m2 for the 1st person + 15m2 for each additional family member).

- Actual land property size: reported values of residential and
  agricultural land (for datasets before 2012) and imputed values
  thereafter. Imputations based on reports on owning land; 0 ha of
  residential land for those living in flats, values for others imputed
  based on information on the area of the house, etc. Agricultural land
  imputed based on a dummy of owning land and information on earning
  from own agricultural activities.

- Notional land property size: according to the notional size of
  residential and agricultural land per family reported above.

- Financial assets: based on the EU-SILC information on investment
  income and external information on the average yield of LT government
  bonds.

*Other imputations and assumptions:*

- Benefit reduction for those able to work but not working is not
  simulated due to data limitation and lag in time until this rule
  effectively will be implemented.

###  Unemployment social insurance benefit (bunct_s)

#### Brief description

This contributory monthly benefit covers individuals previously
receiving remuneration for work.

#### Definitions

The unit of analysis is the individual.

#### Eligibility conditions

The right the unemployment insurance benefit is granted to a person who:

- is registered with the local Public Employment Service as unemployed,

- Employment Service has not offered a suitable job or active labour
  market policy measures and

- either has 12 months of the unemployment insurance over the last 30
  months,

- or has completed the compulsory primary military service or the
  alternative national defence service or has been released from the
  permanent compulsory initial military service during basic military
  training. In this case, the unemployed person must register with the
  Employment Service within 6 months of release from the compulsory
  primary military service or the alternative national defence service
  (in force since 2023).

#### Income test

No income test applied.

#### Benefit amount

The benefit amount comprises of the constant and variable components
(see Table 2.8 for details). Since 2023, the unemployment benefit is
started to be paid on the 8th day of unemployed status. For unemployed
persons, who were dismissed from work due to the employee’s fault, the
unemployment benefit begins to be paid 3 months after the registration
to the Public Employment Services, but no earlier than the day of
acquiring the unemployed status. If unemployed person is eligible to
receive sickness, professional rehabilitation, maternity, paternity,
childcare benefit before they get unemployed person status, the
unemployment benefit is paid after the end of other benefit payment
period.

<span id="_Toc222228377" class="anchor"></span>**Table 2.9**
Characteristics of the unemployment social insurance benefit, 2022-2025

<table style="width:68%;">
<colgroup>
<col style="width: 8%" />
<col style="width: 19%" />
<col style="width: 40%" />
</colgroup>
<thead>
<tr>
<th></th>
<th></th>
<th style="text-align: center;"><strong>2022-2025</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Eligibility</strong></td>
<td>Contribution period</td>
<td style="text-align: center;">12 months during the last 30 months</td>
</tr>
<tr>
<td></td>
<td>Other conditions</td>
<td style="text-align: center;">Registered with the Public Employment
Service as actively looking for a job</td>
</tr>
<tr>
<td></td>
<td>Eligibility for self-employed</td>
<td style="text-align: center;">Not eligible*</td>
</tr>
<tr>
<td><strong>Payment</strong></td>
<td>Contribution base</td>
<td style="text-align: center;">Gross earnings, no contribution
ceiling</td>
</tr>
<tr>
<td></td>
<td>Constant part amount</td>
<td style="text-align: center;">23.27% national minimum monthly
wage</td>
</tr>
<tr>
<td></td>
<td>Variable part amount</td>
<td style="text-align: center;"><p>% of former earnings decreasing with
time:</p>
<p>1-3 months – 38.79%</p>
<p>4-6 months – 31.03%</p>
<p>7-9 months – 23.27%</p></td>
</tr>
<tr>
<td></td>
<td>Floor</td>
<td style="text-align: center;">n/a</td>
</tr>
<tr>
<td></td>
<td>Ceiling</td>
<td style="text-align: center;">58.18% of the national gross average
wage</td>
</tr>
<tr>
<td><strong>Duration</strong></td>
<td>Standard</td>
<td style="text-align: center;">9 months</td>
</tr>
<tr>
<td></td>
<td>Special cases</td>
<td style="text-align: center;"><p>+2 months **</p>
<p>+up to 30 days***</p>
<p>+ for the period of the maternity leave</p></td>
</tr>
<tr>
<td><strong>Subject to</strong></td>
<td>Taxes</td>
<td style="text-align: center;">n/a</td>
</tr>
<tr>
<td></td>
<td>SIC</td>
<td style="text-align: center;">n/a</td>
</tr>
</tbody>
</table>

Note: \* Except members of general partnerships, members of small
partnerships, owners of individual enterprises. \*\* for those who have
5 or less years left to reach the statutory pension age and are not in
receipt of the early retirement pension; \*\*\* for those who, while
being unemployed, became temporary unable to tor due to illness or
injury or who voluntary undergo an addiction treatment in health care
institution providing addiction treatment services. The payment of the
unemployment benefit can be extended by this period, but not longer than
30 days.

Source: Law on Unemployment Social Insurance.

The insured's average monthly insured income is calculated as the
average of the 30 months that have passed until the end of the previous
calendar month from the day of acquiring the unemployed status. If there
is no insured income in any month, it is equated to zero. When the
payment of the unemployment insurance benefit has been terminated, the
unemployment insurance benefit can be re-assigned to the unemployed
person after 12 months from the date of the previous termination of the
unemployment insurance benefit payment.

If a person receives certain benefits (the old-age pension, rent for a
former athlete, allowance for the creative employee of professional
performing arts institutions or sickness allowance due to an accident at
work and occupational illness and occupational rehabilitation, illness,
maternity, paternity or child care benefit), only part of the
unemployment benefit that exceed the amount of all mentioned benefits,
pensions or allowances will be paid.

<u>EUROMOD note:</u>

Effectively, this benefit is only partly simulated using the information
about the actual benefit receipt. Rather than simply using the observed
receipt as part of the eligibility criteria, all eligibility rules are
covered in full detail. Since not all required information (e.g., work
history) is available, several assumptions are made, among else
considering some rules automatically being fulfilled for those in
receipt. This approach is chosen so that the benefit can also be
modelled for currently employed people if needed (e.g. to simulate their
entitlement if they become unemployed; for replacement rates
calculations).

The unemployment duration (lunmy_s) is set equal to the maximum of the
observed unemployment duration (lunmy) and the observed benefit receipt
(bunmy). When modelling the unemployment benefit for those who are
currently employed, the unemployment duration is set to the reported
number of months in employment in the current year (liwmy). After that
the contribution history (see the next step) is modelled. It is assumed
that the unemployment spells start in the reference year.

Modelled contribution history is based on the reported number of months
in employment (liwmy), controlling for the total number of months in
work (liwwh).

- For those currently employed (ils_earns != 0 & lunmy_s = 0 & bunct =
  0), this is used.

- For those currently unemployed (lunmy_s \> 0) and in receipt (bunct \>
  0), this is set to at least the minimum qualifying period.

- For those currently unemployed (lunmy_s \> 0) and not in receipt
  (bunct = 0), this is set to zero.

At this point, working age people who are unemployed (lunmy_s \> 0),
have sufficient contribution history, are not in education and not in
receipt of early retirement old-age pension are considered eligible. It
is assumed that all of them are involuntary unemployed and capable and
available for work (there is a variable in the SILC data identifying if
a person is available for work but only filled in for those currently
unemployed).

Benefit duration (bunmy_s) is calculated according to the rules above,
using modelled contribution history, while also controlling for the
unemployment duration (lunmy_s). The extended duration due to sickness
or maternity leave is not modelled. For currently employed, a further
cap is imposed corresponding roughly to the average duration observed in
administrative sources (and national SILC data).

The benefit entitlement is calculated based on previous earnings and
benefit duration, subject to the lower and upper thresholds. For those
currently employed, current earnings are used. For those currently
unemployed and in receipt, previous earnings are used which have been
imputed by reversing the unemployment social insurance benefit rules.
For those currently unemployed and not in receipt, the imputed wage is
used. Finally, the benefit amount is adjusted with the number of months
in receipt (bunmy_s).

Previous earnings by default are modelled based on the imputed wage
(yivwg), as the inverted wage (yempv) reflect the lower amount due to
applied ceilings on benefits. To switch from the calculations based on
the imputed wage to those based on the inverted wage, the constant
\$ImuputedWage should be set to zero.

Due to data limitations, it is not possible to distinguish whether a
person is partially employed as partial employment is mostly assigned by
the local Municipalities. Furthermore, due to limited data it is
impossible to distinguish if a person is working illegally in the shadow
economy and receives the unemployment benefit. Tax compliance
adjustments may be switched on to adjust simulations.

### Long-term work benefit (bunct01_s) 

#### Brief description

A contributory lump-sum benefit to paid employees in case of redundancy,
when they have been employed by the same employer for at least 5 years.

#### Definitions

The unit of analysis is the individual.

#### Eligibility conditions

In case of redundancy, employees must have been continuously employed by
the same employer for at least 5 years to be eligible to receive the
long-term work benefit. The benefits are paid to all employees who have
worked under employment contracts, except for those from budgetary
institutions and the Central Bank. The benefit is paid if within three
months the previous employee does not sign a new contract with the
previous employer.

#### Income test

No income test applied.

#### Benefit amount

For an employee who worked between 5 to 10 years, the benefit is equal
to 77.58% of 1 previous salary; from 10 to under 20 years – 77.58% of 2
previous salaries; 20 years or more - 77.58% of 3 previous salaries. I
The long-term work benefit amount is calculated on the person’s average
insured income over the last 12 months [^66]. No changes in 2022-2025.

<u>EUROMOD note:</u>

The following assumptions are made: the number of years worked with the
same employer is proxied by the total working history assuming 3 working
positions of an equal working duration (i.e. liwwh / 3). We assume that
those who were made redundant (but not quit the job) are not currently
employed or self-employed in the data and are eligible for unemployment
benefit. Working in the budgetary institution is proxied in the
following way: not working in defence /administration, education, health
or social services, not a public servant.

### Compensation for heating costs (xhcht_s)

#### Brief description

Compensations for the excessive heating costs for a dwelling. The
compensation is means-tested and depend on family income and assets.

#### Definitions

The unit of analysis is family.

#### Eligibility conditions

Compensation for the heating costs is granted regardless of the method
of heating (including central heating or other fuels such as firewood,
coal, gas, etc.).

#### Income test

To receive the compensation, income from the last 3 months period is
assessed. Child benefits and a part of the earnings and a part of the
unemployment benefit (20-40% depending on the composition of a family in
the number of children) are excluded from the income test. However, when
calculating income, income from movable and immovable property is
included e.g., income from the rental or sale of land, housing, car and
other property. The compensation granted to families and single persons
if the value of family’s or person’s assets does not exceed the
established ratio of property value (same as for the receipt of the
social assistance benefit). The assets test was not applied until 30th
of April 2024

#### Benefit amount

To calculate the amount of the compensation for the heating costs, the
notional standard of the useful floor space is used:

- when the place of residence is declared (rented) by one resident - 50
  m2;

- when the place of residence is declared (rented) by the family: 38 m2
  for the firs– household member; 12 m2 for the second; and –- 10 m2 for
  the third and each subsequent person.

The benefit covers 100% of the part of the bill for the heating
exceeding 10% of the difference between the income of a family or a
single person and 2\*SSI for each family member or 3\*SSI for single
persons, taking into account the notional standard useful floor space as
indicated above.

<u>EUROMOD note:</u>

Modelled with assumptions on average monthly heating costs.

###  Compensation for water costs (xhcwt_s)

#### Brief description

Compensations for water costs include compensations for drinking and hot
water costs.

#### Definitions

The unit of analysis is family.

#### Eligibility conditions

The drinking water compensation is granted when the costs for cold water
and wastewater exceed 2% of personal or family income.

The hot water compensations is granted when the costs for hot water and
its preparation exceed 5% of personal or family income.

#### Income test

To receive the compensation, income from the last 3 months period is
assessed. Child benefits and a part of the earnings and a part of the
unemployment benefit (20-40% depending on the composition of a family in
the number of children) are excluded from the income test. The
compensation granted to families and single persons if the value of
family’s or person’s assets does not exceed the established ratio of
property value (same as for the receipt of the social assistance
benefit). The assets test was not applied until 30th of April 2024.

#### Benefit amount

For the calculation of the compensations, the notional standards for
drinking water and hot water are applied.

For drinking water, it depends on the number of household members and
the way hot water is prepared:

When central heating is used to prepare hot water:

- 2 m3 for the first person or a single person per month.

- 1.5 m3 for a second person per month.

- 1 m3 for a third and each subsequent person per month.

When other forms of energy or fuel, such as electricity or firewood, are
used to prepare hot water:

- 33.5 m3 for the first person or a single person per month.

- 2.5 m3 for a second person per month.

- 1.5 m3 for a third and each subsequent person per month.

For hot water, the notional standard is

- 1.5 m3 for the first person or a single person per month.

- 1 m3 for a second person per month.

- 0.5 m3 for a third and each cohabiting person per month

The benefit covers 100% of the part of the expenses for drinking water
exceeding 2% of family’s or single person’s income and for hot water
exceeding 5% of family’s or single person’s income, taking into account
the notional standard per family members are indicated above.

<u>EUROMOD note:</u>

No data on cold/hot water usage and price, therefore the average
cold/hot water usage in m3 per person is used.

## Social insurance contributions

**Social insurance contributions (*socialinio draudimo įmokos*)** to
State Social Insurance Fund (*Socialinio draudimo fondas,* *SoDra*) are
compulsorily paid by all employers and employees of private and public
sectors as well as main categories of self-employed people.

Contributions are flat rate with floors and ceilings. Contributions
differ for employees and self-employed. Furthermore, contribution rates
vary considerably among different categories of self-employed people
(see below for more details). Social insurance contributions are paid
for pension, health care, sickness and maternity, employment injuries,
occupational diseases, and unemployment insurance. Paid contributions
determine eligibility and the amount of contributory benefits. All
social contributions are calculated on the individual tax unit basis.

### Employee social insurance contributions (ils_sicee)

All employees in private and public sectors must pay 19.5% of gross
wages and salaries as social insurance contributions (contribution rates
by insurance type are presented in <span class="mark"></span>[**Table
2.10**](#Table_02_10) ).

<span id="Table_02_10" class="anchor"></span>**Table 2.10** Employee’s
social contribution rates (% of gross salary), effective on 2022-2025

| **Employee’s social insurance contributions** | **2022-2025** |
|-----------------------------------------------|:-------------:|
| 1\. Pension social insurance                  |    8.72\*     |
| 2\. Sickness social insurance                 |     1.99      |
| 3\. Maternity social insurance                |     1.81      |
| 4\. Health insurance                          |     6.98      |
| **Total**                                     |   **19.5**    |

Note: \*if a person participates in the second pension pillar an
additional contribution of 2.7% or 3 % was applied in 2022 and 3% (with
the state subsidy of 1.5%) in 2023-2025.

Source: Sodra..

Since 2021, the ceilings of 60 AMS for the social security contributions
are applied only for the employee contributions (employers pay
contributions without a ceiling).[^67] For the annual income amounts
exceeding the AMS threshold, 0% contribution rate is applied. The
ceiling does not apply for the healthcare contributions nor to the
funded pension scheme. The floors are equal to the monthly minimum wage
and are applied to both employees and employers’ contributions. No
changes in 2025.

### Employer social insurance contributions (ils_sicer)

Public or private sector employers pay 1.77% social insurance
contributions (however, it can vary from 1.45% to 2.49% depending on the
type of contract (open-ended or temporary) and if it is a budget
institution, etc.) on, employees’ gross wages and salaries, which are
split into four components, as indicated in
<span class="mark"></span>[**Table 2.11**](#Table_02_11).

Social insurance contributions are subject to floors which is equal to
the MMS for those employees whose monthly salaries are below the MMS.
The floors are not applicable for certain groups: if an employee works
in more than one work position; if an employee receives the old-age or
work incapacity pension; if an employee is under 24; if an employee is
insured by the government; if an employee is on the childcare leave (in
the second or third year); if an employee takes care for a family member
with high disability level or with special need for permanent care.

<span id="Table_02_11" class="anchor"></span>**Table 2.11** Employers’
social insurance contributions (% of gross salary), 2022-2025

| Employer’s social insurance contributions |  | **2022-2025** |
|----|---:|---:|
| 1\. Unemployment social insurance |  | 1.31\* |
| 2\. Employment injuries and occupational diseases social insurance |  | 0.14\*\* |
| 3\. Contributions to the guarantee fund\*\*\* |  | 0.16 |
| 4\. Long-term work benefit fund\*\*\*\* |  | 0.16 |

Notes: \* 2.03 % for fixed-term contracts; \*\* this is the lowest and
most common rate that is applied for low-risk groups; however, the rate
can be higher for other groups (0.46%, 0.7% or 1.4%);\*\*\*not paid for
people working in bank of Lithuania, in government institutions, for
political parties, trade unions, religious communities and foreign
companies; \*\*\*\* not paid for people working in bank of Lithuania, in
government institutions.

Source: Sodra.

<u>EUROMOD note</u>*:*

Social insurance contribution floors are modelled and are ON by default.
It is recommended to treat simulations with caution. SIC floors should
best be interpreted when run in combination with the minimum wage
adjustments (yem_lt). Otherwise, this will severely over-estimate SIC
receipt. The following data limitations apply to the modelling of SIC
floors: we could not check if a person works in more than one position.
The condition if an employee is insured by the government is proxied by
an industry sector: those employed in defence, public administration,
health, social work, education.

### Credited social contributions (ils_sicct) 

*Credited social contributions* – social insurance contributions paid by
the government on behalf of certain individual groups (for all or
particular types of insurance). Credited social insurance contributions
can include unemployment, pension, sickness, maternity, employment
injuries and occupational diseases social insurance and/or health social
insurance contributions.

The contribution base for credited social insurance contributions is 1
MMS. The government pays contribution at the same rates as they are set
for employers and employee’s part. Most importantly, such contributions
are paid monthly for the following persons:

- If a mother or father (stepmother, stepfather) or guardian (curator)
  taking care of a child under age 3 has no taxable income, he/she is
  insured with the pension and for the unemployment social insurance.
  Only one of the parents can be insured.

- One of the non-pension age parents (stepparents) or guardian (curator)
  taking care after a person with disability has no taxable income,
  he/she is insured with the pension and the unemployment social
  insurance.

- Priests of accepted confessions and monks and nuns working in
  monasteries are compulsorily insured with the pension insurance.

- Conscripts are insured with the pension, unemployment, maternity,
  employment injuries and occupational diseases social insurances. 

- Vocational, tertiary school students and individuals who are directed
  by territorial job centre for vocational training are insured with the
  employment injuries and occupational diseases social insurance for the
  training period.

- Individuals in social or psychological rehabilitation institutions who
  get a salary are insured with the employment injuries and occupational
  diseases social insurance during labour hours.

- Artists, who are of working-age and have no insured income or less
  than 12 MMA per calendar year are covered by the pension, sickness,
  and maternity insurances.

- Unemployed spouses of public servants in an international service are
  insured with the pension, maternity, and unemployment insurances.

- Artists not receiving income are insured with the pension, sickness
  and maternity insurances.

- Cadets, carrying out military service while studying at a military
  training institution are insured with the employment injuries and
  occupational diseases social insurance.

- Interns are insured during their professional practice period at the
  institution of enterprise are insured with the employment injuries and
  occupational diseases social insurance.

- Vocational training students while at the penal institution are
  insured with the employment injuries and occupational diseases social
  insurance.

- Since January 1st, 2023, athletes who are paid a state scholarship in
  accordance with the procedure established by *the Sports Law of the
  Republic of Lithuania,* which does not exceed the amount of the MMS
  approved by the Government, are insured with the pension, sickness and
  maternity social insurances at the state's expense, calculating the
  social insurance contributions from the MMS approved by the Government
  in the event that they do not have insurance income.

Contribution rates for credited social insurance contributions in
2022-2025 are indicated in the [**Table 2.12**](#Table_02_12) .

<span id="Table_02_12" class="anchor"></span>**Table 2.12** Credited
contributions (% of MMS), 2022-2025

|  | **2022-2025** |
|----|---:|
| Contributions for pension social insurance | 8.72 |
| Sickness social insurance | 1.99 |
| Maternity social insurance | 1.81 |
| Unemployment insurance | 1.31 |
| Employment injuries and occupational diseases social insurance | 0.16\* |

Notes: \* can be different for some groups (0.14%, 0.46%, 0.7% or 1.4%).

Source: Sodra.

The contributions for the credited health social insurance are flat rate
and approved annually. It is calculated as 6.89% of MMS Annual amounts
of health social insurance contributions per person were as follows: EUR
611.4 per year (50.95 per month) in 2022, and EUR 703.6 (58.63 per
month) in 2023, EUR 774 (64.50 per month) in 2024 and EUR 869.4 per year
(72.45 per month) [^68].

Groups of persons who are insured for compulsory *health insurance* by
the state:

1.  Persons who receive any kind of pensions or assistance benefits/
    compensations;

2.  Officially unemployed persons (those unemployed who are registered
    with the local Labour Exchange office and are willing to take up a
    job and able to work);

3.  Unemployed persons of the working age who have compulsory
    contribution history for the state social old-age pension;

4.  Women on maternity leave and unemployed pregnant women 70 days
    before the childbirth and 56 days after the childbirth;

5.  One of (foster) parents looking for a child up to 8 years old and
    one of (foster) parents looking for two or more children;

6.  Persons up to 18 years old;

7.  Full-time students and pupils of Lithuanian secondary, vocational
    schools, colleges, universities and those who permanently live in
    Lithuania and study full-time in the EU high schools;

8.  Persons who receive the social assistance benefits;

9.  One of (foster) parents or guardians who nurse at home a person with
    or a person who requires permanent nursing;

10. Persons with disability;

11. Persons infected with communicable diseases that are dangerous for
    society and included into a special list;

12. Participants of the resistance;

13. Persons who helped to liquidate the outcomes of the Chernobyl
    accident;

14. Ex-prisoners of the ghetto and fascist’s prisons;

15. Priests, nuns and monks of the traditional religious communities and
    religious formation students;

16. Persons who participated in the Afghanistan war;

17. Unaccompanied underage foreign citizens;

18. Foreign citizens who are provided with additional and temporary
    shelter in Lithuania;

19. Unemployed spouse of an acting President of Lithuania who has no
    insured income;

20. Persons in traineeships as defined by the Activity law;

21. Displaced individuals;

22. Persons receiving any types of pensions under international
    agreements and when this is defined in the agreements;

23. Arrestees and convicts serving sentences of arrest, fixed-term
    imprisonment and life imprisonment;

24. Foreigners who have been granted temporary protection in Lithuania
    (under certain additional conditions).

Those who choose to participate in the 2nd pension pillar, additional
contributions are also made with state subsidies from the state budget
(3%, with the state subsidy of 1.5%).

<u>EUROMOD note:</u>

Pension and unemployment social insurance contributions are simulated in
EUROMOD only for mothers or fathers (stepmothers, stepfathers) or
guardians (curators) with no taxable income taking care of a child under
age 3 with the following assumptions:

- The recipient of this contribution is the parent, who does not have
  taxable income. If neither parent has income, then the recipient is
  the mother.

- A person should have no taxable income and should live in a family tax
  unit with a child under age 3.

Credited health social insurance contributions are simulated in EUROMOD
for groups 1, 2, 4-8 and 10, which make up the majority of eligible
persons. Compulsory health insurance contributions are not simulated for
other groups due to the lack of information on their status.

### Self-employed social contributions (ils_sicse)

*Self-employed* persons, with the exception of persons engaged in
individual activities under business certificates, have to pay social
insurance contributions. The total rate of the social insurance
contributions depends on the <span class="mark"></span>[**Table
2.13**](#Table_02_13). below show total social insurance contributions
rates for self-employed, which were effective on 1st January 2021-2025.

<span id="Table_02_13" class="anchor"></span>**Table 2.13** Social
insurance contribution rates (%) and bases for different groups of
self-employed, 2022-2025\*

<table style="width:64%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 19%" />
<col style="width: 12%" />
<col style="width: 10%" />
</colgroup>
<tbody>
<tr>
<td><em><strong>Group of self-employed</strong></em></td>
<td><em><strong>SIC contribution base</strong></em></td>
<td><em><strong>SIC types</strong></em></td>
<td><em><strong>SIC rate</strong></em></td>
</tr>
<tr>
<td>Persons engaged in individual activities</td>
<td>90% of income</td>
<td>Pension, sickness, maternity</td>
<td>12.52 (8.72, 1.99, 1.81)</td>
</tr>
<tr>
<td>Persons carrying out activities under a business certificate</td>
<td>MMS</td>
<td>Pension</td>
<td>8.72</td>
</tr>
<tr>
<td>Family-type guardianship institution</td>
<td>Depends on the number of members</td>
<td>Pension, sickness, maternity</td>
<td>12.52 (8.72, 1.99, 1.81)</td>
</tr>
<tr>
<td>Members of general partnerships/members of small partnerships/owners
of individual enterprises</td>
<td>50% of the amount of funds collected for personal needs</td>
<td><p>Pension, sickness, maternity,</p>
<p>unemployment</p></td>
<td>13.83 (8.72, 1.99, 1.81, 1.31)</td>
</tr>
<tr>
<td>Persons engaged in individual agricultural activities, when the
economic size of holding less than or equal to 2**</td>
<td>n.a.</td>
<td>n.a.</td>
<td>n.a.</td>
</tr>
<tr>
<td>Persons engaged in individual agricultural activities, when the
economic size of holding is greater than 2 and less than 4 + VAT
payers**</td>
<td>n.a.</td>
<td>n.a.</td>
<td>n.a.</td>
</tr>
<tr>
<td>Persons engaged in individual agricultural activities, when the
economic size of holding is greater than 4</td>
<td>90% of income</td>
<td>Pension, sickness, maternity</td>
<td>12.52 (8.72, 1.99, 1.81)</td>
</tr>
</tbody>
</table>

Note: SIC contributions are subject to the ceilings of 43 AMS. \* There
were slight differences in the separate social insurance contribution
rates in 2021 (for sickness and maternity insurance), however the total
SIC was the same. \*\* These groups nevertheless pay health
contributions (see below).

Source: SODRA,
<https://www.sodra.lt/lt/situacijos/imoku-tarifai/imoku-tarifai-savarankiskai-dirbantiems?lang=en>

The social insurance contributions for self-employed are subject to the
ceilings which is equal to 43 AMS. If self-employed participate in the
second pillar funded pension scheme, they additionally pay 3% of their
taxable base, plus receive the state subsidy of 1.5% of AMS.

Since January 1st, 2021, self-employed persons (except for family-type
guardianship institutions and receiving income from copyright or income
from sports or performance) may not pay social security and health
insurance contributions (that period is not accounted for the
contributory history) if they: 1) receive social insurance old-age
pension or lost working capacity (disability) pension; 2) receive state
social assistance pension or compensation (except orphan pensions); 3)
receive social insurance old-age, disability, lost capacity pension from
another country, 4) are in prison or mental health care institution; or
5) have reached the statutory retirement age.

Social insurance contributions may be not paid for the first year of the
activity if it is the first time that a person works as self-employed or
if at least 10 years have passed since the last day of their individual
activity.

As of January 1st, 2021, self-employed persons who pay social security
contributions for themselves, the payment of interest on arrears of
social security contributions may be deferred for up to one year if
their total indebtedness to the Fund is between 125-1500 EUR. If the
total indebtedness to the Fund is below 125 EUR, the payment of arrears
of interest on late payment of social security contributions cannot be
postponed.

As of January 1st, 2021, persons engaged in *individual activities under
business certificates* for a period shorter than 3 months must pay
social security contributions in advance for the entire period of
validity. Persons who have acquired business certificates for more 3
months or more must pay social insurance contributions once a quarter.

No major changes in 2022-2025.

<u>EUROMOD note</u>:

SIC “holidays” are modelled for those with the total working history not
exceeding 12 months in the data, i.e., only those with liwwh \> 12 are
eligible for paying social insurance contributions.

***Compulsory health insurance contributions for the self-employed:***

The standard health contribution rate of 6.98% is applied on 90% of
annual taxable income for people engaged in individual activities.
However, the compulsory minimum monthly contribution is 6.98% of the
MMS. If annual income is higher than the 12\*MMS, the self-employed have
to pay the health contribution difference when declaring their annual
income. For some groups of the self-employed the health contribution
rate or contribution base is different (Table 2.14).

<span id="_Toc222228382" class="anchor"></span>**Table 2.14** Health
insurance contribution rates (%) and bases for different groups of
self-employed, 2022-2025

<table style="width:65%;">
<colgroup>
<col style="width: 27%" />
<col style="width: 27%" />
<col style="width: 10%" />
</colgroup>
<tbody>
<tr>
<td><em><strong>Group of self-employed</strong></em></td>
<td><em><strong>Contribution base</strong></em></td>
<td><em><strong>HIC rate</strong></em></td>
</tr>
<tr>
<td>Persons engaged in individual activities</td>
<td><p>Monthly MMS</p>
<p>Yearly – 90% of income<br />
(but not less than 12*MMS)</p></td>
<td>6.98</td>
</tr>
<tr>
<td>Persons carrying out activities under a business certificate</td>
<td>MMS</td>
<td>6.98</td>
</tr>
<tr>
<td>Family-type guardianship institution</td>
<td>MMS</td>
<td>6.98</td>
</tr>
<tr>
<td>Members of general partnerships/members of small partnerships/owners
of individual enterprises</td>
<td>50% of the amount of funds collected for personal needs</td>
<td>6.98</td>
</tr>
<tr>
<td>Persons engaged in individual agricultural activities, when the
economic size of holding less than or equal to 2</td>
<td>MMS</td>
<td>2.33</td>
</tr>
<tr>
<td>Persons engaged in individual agricultural activities, when the
economic size of holding is greater than 2 and less than 4 + VAT
payers</td>
<td>MMS</td>
<td>6.98</td>
</tr>
<tr>
<td>Persons engaged in individual agricultural activities, when the
economic size of holding is greater than 4</td>
<td>MMS</td>
<td>6.98</td>
</tr>
</tbody>
</table>

Source: “LR valstybės biudžeto ir savivaldybių biudžetų finansinių
rodiklių patvirtinimo įstatymas“and Lietuvos Respublikos Sveikatos
draudimo įstatymas” and their relevant versions.

<u>EUROMOD note:</u>

Social insurance and health contributions paid by some groups of
self-employed are too specific and cannot be identified in the
underlying data to be simulated in EUROMOD.

### Contributions to the funded pension scheme (tsceepi_s, tscsepi_s)

Every working person below 40 is automatically included to the 2nd
pillar funded pension scheme with the possibility to opt out. If opted
out, the automatic inclusion is nevertheless repeated every 3 years
until person reaches 40 years of age. Older workers can participate if
they wish so. Once participating in the scheme, one cannot terminate the
contract, except important circumstances. The payment of the
contributions can be stopped only temporary for the total of 12 months
thorough the whole contributory period. The contributions since 2023 are
equal to 3% of the gross wage and the state contributes another 1.5% of
the AMS. In 2022 individuals could chose to pay lower contribution rates
(Table 2.15). Those who are on the childcare leave, do no pay the
contributions to the fund, but the state continues to contribute 1.5% of
the AMS until child reaches the age of 3.

<span id="_Toc222228383" class="anchor"></span>**Table 2.15** 2nd pillar
contribution rates to privately managed pension funds and state
subsidies (%), 2022-2025

|  **Year**   | **Rate and state subsidy (in brackets)** |
|:-----------:|:----------------------------------------:|
|    2022     |           2.7 (1.2) or 3 (1.5)           |
| 2023 - 2025 |                 3 (1.5)                  |

Note: state subsidy is capped at 1.5% of the AMS.

Source: Sodra.

<u>EUROMOD note:</u>

Based on the external statistics from State Social Insurance Fund
(Sodra) have shown, that participation rate among working age persons is
relatively high, however varies differently between the age groups. We
assume different participation rates with different contributions to the
2nd pillar for different age groups up to 2022 (see model). Different
participation rates were randomly distributed to each working age
employed or self-employed person. Since 2023 the contribution rate for
the 2nd pillar is 3% for all. It is important to note that those,
receiving childcare benefits or covered by the state, are not simulated
in the model. Extra contributions to the funded pension funds are not
modelled.

### Compulsory health insurance contributions for those not otherwise insured (thl_s)

Persons who do not receive any taxable income and who are not otherwise
insured for health social insurance (see Section 2.7.3 for details on
credited health insurance contributions), pay a compulsory health
insurance contribution of 6.98% of the MMS per month. No changes in
2022-2025.

## Taxes

### Personal income tax (tin_s)

#### Tax unit 

**Personal Income Tax (*asmens pajamų mokestis*):** Personal income tax
(PIT) is applied on individual’s taxable income in Lithuania.

#### Tax base 

*Tax base* is derived from declared income by deducting the following
components:

- non-taxable income (all state social assistance and some social
  insurance benefits e.g., pensions, disability benefits, etc.),

- income received from activities conducted under a business
  certificate,

- allowable deductions related to income from individual activities,

- tax credit for individual incomes,

- the acquisition price of property and expenses related to it,

- tax allowances

- deductible expenses incurred by a resident (only when calculating
  taxable income of fiscal year).

No deductions can be made to the income from distributed profit
(dividends).

#### Exemptions

We define exemptions as “income components (that) are part of pre-tax
income, but are not included in the concept of taxable income (e.g.
child benefits in most countries)”.

The list of tax-exempt incomes includes more than 50 categories (most
importantly, state social assistance or social insurance benefits, paid
from state and municipal budgets or *Social Insurance Fund*, except
sickness, maternity, paternity, childcare and long-term unemployment
benefits) that are not subject to personal income taxation.

A number of other non-taxable income include charity, scholarships,
interest from deposits, loans, compensations, lottery winnings, prizes
of sports competitions, pension annuities received from life insurance
companies, inherited income, alimonies, proceeds from the sale of
agricultural produce, which is produced, as well as produced and
processed on the land owned and some other types of incomes.

#### Tax allowances

Tax allowances are defined as amounts subtracted from pre-tax income.

The most significant tax allowance is the basic allowance applied to
employment-related income, consisting of:

- salary, bonuses and premiums (monthly, quarterly, annual),

- sickness allowance for the first two days of the illness (paid by the
  employer),

- compensation for unused vacation,

- payments for overtime work, working on holidays and weekends, at
  night, or for the idle time,

- holiday payments,

- per diem if exceeds the statutory rate,

- other additional earnings paid directly by an employer to an employee
  for the work performed.

Sickness, maternity, paternity, childcare benefits and long-term work
benefits are also included into the employment-related income (hence,
basic allowance is also subtracted), but are taxed at a lower rate.

***The rule for calculation of the basic allowance 2022-2025***

The general formula for calculating the monthly basic allowance for
residents without disability is:

**Equation 1** General formula for the calculation of monthly basic
allowance

<img src="media/image4.png" style="width:5.90625in;height:0.625in" />

where $`basic\ allowance_{0}`$ is the initial level of basic allowance
for a full-time working resident without disability, $`coef`$ is a
coefficient, $`income`$ is the monthly employment income of the resident
and ***MS*** is the monthly minimum salary (see
<span class="mark"></span>[**Table 1.5**](#Table_01_04) for minimum
salary and <span class="mark"></span>[**Table 2.16**](#Table_02_16) for
other values in the latest years). The basic allowance cannot fall below
0 and cannot exceed income.

The monthly basic allowance is calculated each month, but then is
recalculated at the end of the year using the yearly formula. In this
case, all parameters are multiplied by 12, while income is the total
taxable yearly income (not just employment income).

For the residents with 30-55% of working ability level, for those who
have reached retirement age and have a medium or low level of special
needs, or for the residents, who have a medium or mild level of
disability, the basic allowance is higher and does not change with
income (see <span class="mark"></span>[**Table 2.16**](#Table_02_16) ).

For the residents with 0-25% of working ability level, those who have
reached retirement age and have a high level of special needs, or for
the residents who have a severe level of disability, the basic allowance
is the highest of the three and does not change with income (see
<span class="mark"></span>[**Table 2.16**](#Table_02_16) ).

***The rules applied for calculation of the basic allowance for 2022 1st
of June (but applicable for the whole year)***

The monthly basic allowance is 540 EUR per month if the resident’s
monthly income does not exceed 730 EUR per month. If the resident’s
income is higher, the basic allowance is calculated using the following
formula if employment income:

1.  is between 730 EUR and between 1704 EUR:

    1)  The monthly basic allowance= 540 – 0.34 × (monthly employment
        income – 730)

    2)  The annual basic allowance = 6480 – 0.34 x (resident’s annual
        income – 8760)

<!-- -->

4.  exceeds 1704 EUR:

    1)  The monthly basic allowance= 400 – 0.18 x (monthly
        employment-related income – 642)

    2)  The annual basic allowance is 7704 EUR if the resident’s annual
        income does not exceed 4800 EUR. If the resident’s income is
        higher, the basic allowance is calculated using the following
        formula:

*The annual basic allowance = 4800 – 0.18 x (resident’s annual income –
7704)*

For the residents with 0-25% of working ability level, those who have
reached retirement age and have a high level of special needs, or for
the residents who have a severe level of disability, the basic allowance
of 870 EUR is applied.

For the residents with 30-55% of working ability level, for those who
have reached retirement age and have a medium or low level of special
needs, or for the residents, who have a medium or mild level of
disability, the basic allowance of 810 EUR is applied.

***The rules applied for calculation of the basic allowance for 2023***

The monthly basic allowance is 625 EUR per month if the resident’s
monthly income does not exceed 840 EUR per month. If the resident’s
income is higher, the basic allowance is calculated using the following
formula if employment income:

1.  is between 840 EUR and between 1926 EUR:

    1)  The monthly basic allowance= 625 – 0.42 × (monthly employment
        income – 840)

    2)  The annual basic allowance = 7500 – 0.42 x (resident’s annual
        income – 10080)

<!-- -->

1.   exceeds 1926 EUR:

    1)  The monthly basic allowance= 400 – 0.18 x (monthly
        employment-related income – 642)

    2)  The annual basic allowance is 7704 EUR if the resident’s annual
        income does not exceed 4800 EUR. If the resident’s income is
        higher, the basic allowance is calculated using the following
        formula:

        The annual basic allowance = 4800 – 0.18 x (resident’s annual
        income – 7704)

For the residents with 0-25% of working ability level, those who have
reached retirement age and have a high level of special needs, or for
the residents who have a severe level of disability, the basic allowance
of 1005 EUR is applied.

For the residents with 30-55% of working ability level, for those who
have reached retirement age and have a medium or low level of special
needs, or for the residents, who have a medium or mild level of
disability, the basic allowance of 935 EUR is applied.

***The rules applied for calculation of the basic allowance for 2024***

1.  The monthly basic allowance is 747 EUR per month (8964 per year) if
    the resident’s monthly income does not exceed 924 EUR (MMS) per
    month (11088 EUR per year).

<!-- -->

2.  If the resident’s monthly income is between 924 EUR (11088 EUR per
    year) and 2167 EUR (26004 EUR per year), the basic allowance is
    calculated using the following formula:

    1)  The monthly basic allowance= 747 – 0.5 × (monthly employment
        income – 924)

    2)  The annual basic allowance = 8964 – 0.5 x (resident’s annual
        income – 11088)

3.  If the resident’s monthly income exceeds 2167 EUR (26004 EUR per
    year), the allowance is calculated using the following formula:

    1)  The monthly basic allowance= 400 – 0.18 x (monthly
        employment-related income – 642)

    2)  The annual basic allowance = 4800 – 0.18 x (resident’s annual
        income – 7704)

The basic allowance decreases with income and is not applied when
monthly earnings reach 2864.22 EUR (yearly – 34370.67 EUR) threshold.

- For the residents with 0-25% of working ability level, and for those
  who have reached the retirement age and have a high level of special
  needs, and for the residents who have a severe disability, the monthly
  basic allowance is 1 127 EUR.

- For the residents with 30-55% of working ability level, and for those
  who have reached retirement age and have a medium or low level of
  special needs, or for the residents, who have a medium or mild level
  of disability, the monthly basic allowance is 1 057 EUR.

***The rules applied for calculation of the basic allowance for 2025***

1.  The monthly basic allowance is 747 EUR per month (8964 per year) if
    the resident’s monthly income **does not exceed 1038 EUR (MMS) per
    month** (12456 EUR per year).

2.  If the resident’s monthly income is **between 1038 EUR** (12456 EUR
    per year) **and 2387.29 EUR** (28647.48 EUR per year), the basic
    allowance is calculated using the following formula:

    1)  *The monthly basic allowance= 747 – 0.49 × (monthly employment
        income – 1038)*

    2)  *The annual basic allowance = 8964 – 0.49 × (resident’s annual
        income – 12456)*

3.  If the resident’s monthly income **exceeds 2387.29 EUR** (28647.48
    EUR per year), the allowance is calculated using the following
    formula:

    1)  The monthly basic allowance= 400 – 0.18 x (monthly
        employment-related income – 642)

    2)  The annual basic allowance = 4800 – 0.18 x (resident’s annual
        income – 7704)

        The basic allowance decreases with income and is not applied
        when monthly earnings reach 2864.22 EUR (yearly – 34370.67 EUR)
        threshold.

<!-- -->

1.  For the residents with 0-25% of working ability level, and for those
    who have reached the retirement age and have a high level of special
    needs, and for the residents who have a severe disability, the
    monthly basic allowance is 1 127 EUR.

2.  For the residents with 30-55% of working ability level, and for
    those who have reached retirement age and have a medium or low level
    of special needs, or for the residents, who have a medium or mild
    level of disability, the monthly basic allowance is 1 057 EUR.

<span id="Table_02_16" class="anchor"></span>**Table 2.16** Personal
income basic allowance (EUR per month) 2022-2025

|  |  |  |  |  |
|:--:|:--:|:--:|:--:|:--:|
| **Allowances** | **2022** | **2023** | **2024** | **2025** |
|  |  |  |  |  |
| \- General ($`basic\ allowance_{0}`$) | 540 | 625 | 747 | 747 |
| \- For the people with 0-25% work capacity | 870 | 1005 | 1127 | 1124 |
| \- For the people with 30-55% work capacity | 810 | 935 | 1057 | 1057 |
| 
``` math
coef
``` | 0.26 | 0.42 | 0.5 | 0.49 |
| 
``` math
threshold
``` | 1704 | 1926 | 2167 | 2387.29 |

Source: State Tax Inspectorate.

***Tax credit for self-employed income in 2022-2025:***

- when annual self-employment income is below or equal to 20 000 EUR,
  the tax credit is calculated using the following formula:

*Tax credit = annual self-employment income \* 0.1.*

- when annual self-employment income is above 20 000 EUR, the tax credit
  is calculated using the following formula:

*Tax credit = annual self-employment income \* (0.1-2/300 000 \* (annual
self-employment income – 20 000))*

***Tax schedule***

Employment income and several types of non-employment income are taxed
at 20% if this type of income does not exceed 60 AMS (average monthly
salary) and 32% thereafter. Taxable benefits (sickness, maternity,
paternity, childcare and long-term work), dividends, income from
individual activities (minus tax credit) and some other types of income
are taxed by 15% (see Table 2.17). On income derived from activities
conducted under a business certificate, a fixed amount set by municipal
councils is paid. Other income may be taxed at various tariffs ranging
5-20%.

<span id="_Toc222228385" class="anchor"></span>**Table 2.17** Personal
income tax rates and thresholds, 2022-2025

|  |  |  |  |  |
|:--:|:--:|:--:|:--:|:--:|
| **Allowances** | **2022** | **2023** | **2024** | **2025** |
|  |  |  |  |  |
| \- General ($`basic\ allowance_{0}`$) | 540 | 625 | 747 | 747 |
| \- For the people with 0-25% work capacity | 870 | 1005 | 1127 | 1124 |
| \- For the people with 30-55% work capacity | 810 | 935 | 1057 | 1057 |
| 
``` math
coef
``` | 0.26 | 0.42 | 0.5 | 0.49 |
| 
``` math
threshold
``` | 1704 | 1926 | 2167 | 2387.29 |

Source: based on “Lietuvos Respublikos gyventojų pajamų mokesčio
įstatymas” https://www.e-tar.lt/portal/lt/legalAct/TAR.C677663D2202/asr

***Deductible expenses***

The following expenses incurred by a resident of Lithuania during the
tax period may be deducted from his/her income:

1.  Life insurance contributions paid for own benefit or for the benefit
    of a spouse or minor children (adopted children) under 18 years of
    age or for children with disability (adopted children) under 18 and
    older who are considered in need for permanent care (with severe
    disability) under life insurance contracts, which provide an
    insurance benefit not only upon the occurrence of an insurance
    event, but also upon the expiry of the insurance contract.

2.  Voluntary pension contributions to pension funds paid for own
    benefit or for the benefit of a spouse or children (adopted
    children) with disability or who are considered in need for
    permanent care under 18 and older.

    1)  Voluntary pension contributions paid to pension funds operating
        in the EEA and OECD members to own behalf, when contributions
        are larger than 3% of his-her taxable base for social insurance
        contributions.

<!-- -->

1.  Fees for vocational training when qualification or specific
    competence is obtained upon graduation and for studies leading to a
    higher education qualification). If fees for vocational training or
    studies are made with borrowed funds (a loan is taken out from a
    credit institution for that purpose), the repaid amount of the loan
    during the tax period may be deducted from income. If a student is
    not a payer of the income tax or has no possibility to deduct fees
    for studies, those expenses may be deducted from the incomes of
    his/her parents (adoptive parents), guardians and (or) a spouse.

The total amount of the deducted expenses cannot exceed 25% of the total
tax base after deducting tax allowances. The total amount of the
expenses mentioned in parts 1, 2 and 2.1 cannot be higher than 1500 EUR

Expenses are deducted from income when calculating the final income tax
liability for the tax period when submitting the annual income tax
declaration.

***Withholding tax and final tax liability***

Almost on all income sources (except self-employed, farmers’ and income
from property sale and so called “other” incomes) income tax is already
withheld at the time of payment. Self-employment income and farmers’
income are subject to final tax, which is calculated when submitting the
annual tax declaration.

 

Generally, compared to the withheld income tax, the final income tax
takes into account several additional aspects:

1.  Income from self-employment;

2.  Income from property sale or another movable asset;

3.  Other received incomes

4.  The basic annual allowance if a person used not all annual
    amount (i.e. if a person worked not 12, but less months; if
    individual receives only incomes from authorship contracts; if an
    individual had multiple jobs, etc.).

5.  Deductible expenses.

<u>EUROMOD note:</u>

Since it is not possible to distinguish between different levels of
working capacity in the data, all self-reported people with disabilities
are assumed to have 0-25% working capacity.

Among deductible expenses only voluntary pension contributions could be
simulated given the data availability.

The fee for the business certificate is not simulated due to the data
constraints in EU-SILC. Taxes on the sale of wealth and various type of
other income are not modelled.

### Consumption taxes

Two types of consumption taxes are simulated in EUROMOD: VAT and
excises. Simulated consumption tax liabilities paid by households depend
on the tax rules (e.g. the VAT rate) and on the tax base (consumption
expenditures or quantities). The expenditures matched in the EUROMOD
input files based on SILC are reported directly by households in the HBS
surveys at purchasing prices. Therefore, they already include the
consumption taxes paid.

1.  VAT (il_tva variable in EUROMOD) is the value-added tax. The model
    also simulates at high disaggregation level the VAT liabilities paid
    for each consumption category (output variables are tva01111,
    tva01112, and so on and so forth, corresponding to COICOP codes
    01111 and 01112, etc.)

2.  Excises (il_tx variable in EUROMOD) are additional duties paid over
    consumption and can be classified in two groups: ad-valorem excises
    (il_txv) that depend on producer prices, and of specific or
    ad-quantum excises (il_txa) that depend on consumed quantities.

Since consumption data from HBS refers to expenditures (price times
quantity), for the simulation of specific excises information on
consumption prices are needed. Further information on methodology and
specific calculations and the independence of these consumption taxes is
common across countries (this is why they are placed in an add-on and
not in the policy spine of each country) and can be found in Akoğuz et
al (2020).[^69]

#### VAT (il_tva)

VAT embedded in the expenditure consumption reported by households is
extracted by applying the VAT rate of the policy system year.
<span class="mark"></span>[**Table 2.18**](#Table_02_18) contains the
rate structure for the latest four years. Although the rates did not
change, some goods and services were moved from one rate to another (see
main policy changes).

<span id="Table_02_18" class="anchor"></span>**Table 2.18** VAT rates
\[2022-2025\]

|  | Products and services | 2022 | 2023 | 2024 | 2025 |
|----|---:|:--:|:--:|:--:|:--:|
| Standard |  | 21% | 21% | 21% | 21% |
| Reduced | District heating, books, (largely public) transportation, hotel accommodation | 9% | 9% | 9% | 9% |
| Super reduced | Pharmaceuticals (except non-prescription non-compensated), disabled technical aids, newspapers | 5% | 5% | 5% | 5% |
| Zero or exempt | Financial and insurance services, health, education, social protection, and sports services when provided by official providers and non-profit institutions, especially if provided to its own members. | 0% | 0% | 0% | 0% |

Source: State Tax Inspectorate.

#### Ad-valorem excises (il_txv)

*Ad-valorem excises are applied to cigarettes.*

<span id="_Toc222228387" class="anchor"></span>**Table 2.19** Ad-valorem
excise rates \[2022-2025\]

|  Products  | 2022 | 2023 | 2024 | 2025 |
|:----------:|:----:|:----:|:----:|:----:|
| Cigarettes | 25%  | 25%  | 25%  | 25%  |

Source: State Tax Inspectorate.

#### Specific excises (il_txa)

*Specific excises apply to energy, alcohol and tobacco. Both tax
parameters and consumer prices are required to allow the model to
estimate the implicit quantities behind the reported household
consumption expenditure amounts. The main specific excise taxes are in
the table below.*

<span id="_Toc222228388" class="anchor"></span>**Table 2.20** Main
specific (ad-quantum) excise rates

|                 Products                  |  2022  |  2023  |  2024  |  2025  |
|:-----------------------------------------:|:------:|:------:|:------:|:------:|
| Ethyl alcohol (per 100 l of pure alcohol) |  2163  |  2310  |  2467  |  2778  |
|     Wine, \> 8,5% vo. (EUR per 100 l)     |        |        |  219   |  254   |
|     Wine, \< 8,5% vo. (EUR per 100 l)     |        |        |  109   |  127   |
|           Beer (EUR per 100 l)            |  7.82  |  8.60  |  9.46  | 10.97  |
|     Cigarettes (EUR per 1000 pieces)      | 74.30  | 79.60  | 85.30  | 92.60  |
|            Cigars (EUR per kg)            |   66   |   79   |   95   | 109.70 |
|   Other tobacco (Fine cut, EUR per kg)    |   97   | 104.60 | 112.80 | 106.45 |
|         Electricty (EUR per MWh)          |  1.01  |  1.01  |  1.01  |  1.01  |
| Natural Gas- Heating (EUR per gigajoule)  |  0.3   |  0.3   |  0.3   |  0.3   |
| Liquefied hydrocarbons (EUR per 1000 kg)  |   0    |   0    | 304.1  | 13.00  |
|      Petrol-Leaded (EUR per 1000 L)       | 579.24 | 579.24 | 579.24 | 626.24 |
|     Petrol-Unleaded (EUR per 1000 L)      |  466   |  466   |  466   |  513   |

Source: Eurostat, e-Seimas.

<span id="_Toc222228389" class="anchor"></span>**Table 2.21** Prices of
main excise products

| Prices | 2022 | 2023 | 2024 | 2025<sup>n</sup> |
|:--:|:--:|:--:|:--:|:--:|
| Ethyl alcohol (EUR per 1 l of spirits) | 43.0 | 46.9 | 48.4 | 52.5 |
| Wine (EUR per 1 l) | 7.8 | 8.3 | 8.7 | 9.2 |
| Sparkling wine (EUR per 1 l) | 7.3 | 7.8 | 8.7 | 9.2 |
| Beer (EUR per 1 l) | 2.3 | 2.6 | 2.8 | 3.1 |
| Cigarettes (EUR per 1000 pieces) | 205.8 | 209.6 | 238 | 252.56 |
| Cigars (EUR per 1000 pieces) | 264.1 | 284.9 | 384.9 | 305 |
| Other tobacco (Fine cut. EUR per kg) | 245.2 | 241.3 | 272 | 296.81 |
| Electricty (per MWh) | 212.3 | 264.4 | 230.40 | 197.61 |
| Natural Gas- Heating (EUR per gigajoule) | 26.04 | 45.86 | 20.14 | 19.38 |
| Liquefied hydrocarbons (propane - EUR per 1000 kg) | 1487.62 | 1113.33 | 1270.00 | 1229.00 |
| Gas Oil- Heating (EUR per 1000 l) | 1177.45 | 1081.84 | 922.02 | 907.61 |
| Coal and Coke - Heating (EUR per gigajoule) | 23.15 | 27.43 | 22.69 | 23.24 |
| Petrol-Unleaded (EUR per 1000 l) | 1710.00 | 1520.00 | 1453.79 | 1355.59 |
| Gas Oil- Propellant (EUR per 1000 l) | 1750.00 | 1500.00 | 1456.31 | 1459.38 |

Note: n: nowcasted.

Source: Eurostat, e-Seimas, own calculations.

Historical consumer prices are estimated using data on prices of the
goods or their close substitutes and the Harmonised Index of Consumer
Prices (HICP) or the Consumer Price Index (CPI).

Consumer prices of goods subject to excise duties are nowcasted
(following Akoğuz et al., 2020) similarly to what the model does to
update incomes from SILC. The latest available data comes from the
following sources:

- Prices per product, usually from last year, but for instance, fuel
  prices have only 15 days delay.

- Inflation: Harmonised Index of Consumer Prices (HICP, Eurostat) at
  COICOP 5 digits, usually for the first quarter for beta release and up
  to third quarter 3 for final release.

- Inflation quarter-on-quarter forecasts (DG ECFIN, confidential) by
  HICP main groups (Unprocessed food, Processed food including alcohol
  and tobacco, Non-energy industrial goods, Energy, Services - overall
  index excluding goods) of quarters 2, 3 and 4, as needed for each
  release.

- **<u>EUROMOD modelling</u>**

Consumption taxes (tco_cc policy) require extended EUROMOD input data
(with imputed income shares of consumption expenditures at the household
level) and an add-on to run. The policy is set to off in the baseline.
To activate it, the CT_xbase add-on must be run, and the extended EM
input files (see Section 3 for more information on the methodology and
features behind these extended input files) should be selected (as
defined in the database configuration of each country). The other
add-ons (CT\_\*) are designed for reform simulations and assume
different behavioural responses: i) constant quantities (CT_XCQ), ii)
constant income shares (CT_XCIS), and iii) constant expenditure shares
(CT_XCES). These reform-scenario add-ons require the auxiliary output
files are generated by running the first baseline simulation (as either
the quantities or expenditures and savings from the baseline are kept
constants and enter as inputs in the simulated reform scenarios).

## Extraordinary measures in Lithuania

Due to the coronavirus (Covid-19), a number discretionary tax and
benefit measures were implemented in Lithuania in order to cope with the
negative socio-economic impact of job and income loss due to the
pandemic. It includes newly introduced temporary benefits and existing
benefit changes, wage compensations and other measures that are outside
the scope of EUROMOD. Please refer to the earlier versions of the
Lithuanian country report for more details.

# Data

## General description

An overview of the established combinations of EUROMOD LT datasets and
policy years is given in Table 3.1. Our focus is on the EUROMOD LT-data
2024. The descriptions of the EUROMOD LT-data could be found in the
preceding EUROMOD Lithuania country reports.

<span id="_Toc222228390" class="anchor"></span>**Table 3.1** EUROMOD LT
2022-2025: data and policy years

|              | **2022** | **2023** | **2024** | **2025** |
|--------------|:--------:|:--------:|:--------:|:--------:|
| LT-data 2018 |    x     |    x     |    x     |    x     |
| LT-data 2019 |    x     |    x     |    x     |    x     |
| LT-data 2020 |    x     |    x     |    x     |    x     |
| LT-data 2021 |    x     |    x     |    x     |    x     |
| LT-data 2022 |   best   |    x     |    x     |    x     |
| LT-data 2024 |   n/a    |   best   |   best   |   best   |

Source: EUROMOD model.

EUROMOD LT-data 2024 is mainly derived from the EU-SILC EMSD (thereafter
also referred to as EMSD or EU-SILC data). In addition, the Lithuanian
(or National) SILC survey (i.e., *Pajamų ir gyvenimo sąlygų tyrimas*) is
used to include a few other variables and inform imputations. We
describe both datasets, as well as EUROMOD LT-data 2024, in more detail.

The EU-SILC EMSD survey has a 4-year rotational panel survey design. The
data is collected using a face-to-face interviewing of all respondents
aged 16 and over. In the Lithuanian part of the EU-SILC survey,
additional information on income and taxes paid is obtained from a few
administrative sources, such as the State Tax Inspectorate and the State
Social Insurance Fund Board. The National SILC survey is the underlying
micro-dataset on Lithuania for the EU-SILC. It contains additional
information, which is otherwise excluded in the EMSD version (e.g., on
national benefits). This information is highly useful for enlarging the
scope of EUROMOD Lithuanian policy simulations[^70]. As a result,
EUROMOD LT-data 2024 is constructed using both the EU-SILC EMSD and the
National Lithuanian SILC information. <span class="mark"></span>[**Table
3.2**](#Table_03_02) provides a short description of the database.

<span id="Table_03_02" class="anchor"></span>**Table 3.2** EUROMOD LT
database 2024 short description

<table style="width:66%;">
<colgroup>
<col style="width: 18%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"></th>
<th colspan="4">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>EUROMOD database</td>
<td>LT_2024_c1</td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>Original name</td>
<td colspan="4"><em>EU-SILC –</em> <em>Community Statistics on Income
and Living Conditions (Anonymised User Database EMSD) + merged variables
from “Pajamų ir gyvenimo sąlygų tyrimas”</em></td>
</tr>
<tr>
<td>Provider</td>
<td colspan="4">EUROSTAT (EU-SILC); Statistics Lithuania (<em>Pajamų ir
gyvenimo sąlygų tyrimas)</em></td>
</tr>
<tr>
<td>Year of collection</td>
<td>2024</td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>Period of collection</td>
<td>January-April</td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>Income reference period</td>
<td>2023</td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>Sampling</td>
<td colspan="4" style="text-align: left;">A stratified sampling design
was used. The entire Lithuanian territory was divided into 25
non-overlapping groups –strata. The population of the five largest
cities of Lithuania, towns of each county and rural areas of each county
was divided into separate strata. The size of the sample of households
in every stratum is proportional to the number of residents aged 16 and
older in them. From every stratum, a household sample with probabilities
proportional to the size of the household was selected</td>
</tr>
<tr>
<td>Unit of assessment</td>
<td colspan="4">Household and individual</td>
</tr>
<tr>
<td>Coverage</td>
<td colspan="4">Private households. Persons living in the institutional
households (e.g. in care or imprisonment institutions, etc.) are
excluded</td>
</tr>
<tr>
<td>Sample size</td>
<td colspan="4">households</td>
</tr>
<tr>
<td>Response rate</td>
<td colspan="4">Household response rate is 76.3% (6711 out of selected
8796)</td>
</tr>
</tbody>
</table>

Source: Statistics Lithuania (2024):
https://osp.stat.gov.lt/documents/10180/5118910/Gyvenimo+s%C4%85lygos+%5BLT%5D+721.html

## Sample quality and design

The target population of the SILC data is private households (Statistics
Lithuania, 2024). Persons living in the institutional households are
excluded. Households are selected from the *Residents’ Register* using a
stratified sampling design with a simple random sample in strata. For
this, the entire Lithuanian territory is divided into 7 non-overlapping
groups – strata (the 5 biggest cities of Lithuania Vilnius, Kaunas,
Klaipėda, Šiauliai and Panevėžys; other towns; rural areas). The sample
size of households in every stratum is proportional to the number of
population aged 16 and over in them.

## Non-response and item non-response

Based on Statistics Lithuania (2023) household response rate is 76.3%.
For the 2024 survey, 8796 households were selected, of which 6711
participated in the survey. No information is available on response
rates by area. Highest item non-response rates were on interest,
dividends, profit from capital investments in incorporated businesses
and regular inter-household cash transfers received. Item non-response
was lower for family/children related allowances, for social exclusion
payments, cash or near-cash employee income, unemployment benefits, old
age benefits, survivor benefits, disability benefits.

## Weights

The EU-SILC EMSD dataset uses a few types of cross-sectional survey
weights, such as:

- the household cross-sectional weight (variable db090) – the weight
  calibrated with the target population of private households and
  corrected for household non-response.

- the personal cross-sectional weight for all household members of all
  ages (variable rb050) is used to draw inference on individual basic
  demographic variables for the population of all individuals living in
  private households. Because all the current members of any selected
  household are surveyed, the personal weights rb050 are equal to the
  corresponding household cross-sectional weight db090.

- the personal cross-sectional weights for all household members aged 16
  and over (target variable pb040) is used to draw inference on the
  variables included in the personal questionnaire. These weights are
  corrected for individual non-response.

<span id="_Toc222228392" class="anchor"></span>**Table 3.3** Descriptive
statistics of the grossing-up weight rb050 (dwt)

|         | EU-SILC EMSD Lithuanian data |
|---------|------------------------------|
| Number  | 12,593                       |
| Mean    | 229.1                        |
| Maximum | 3200.9                       |
| Minimum | 6.9                          |
| Max/Min | 457.9                        |

Source: own calculations

Lithuanian EU-SILC sample statistics has been projected to a reference
population of **2.884.568** individuals in 1.5425.14 households. The
used weights are calibrated on the demographic data at the beginning of
the survey year. In addition to the major age groups (around 17
sub-groups) and gender, the survey is calibrated by the residence area:
the major 5 cities, other towns, and rural areas.

## Data adjustment

Adjustments to variables are kept to a minimum. Some minor data cleaning
is done to ensure that the relationships of individuals within
households are coherent. As we focus on the income reference year
(2023), children who are born in the year of the survey (until the
survey time, which is January-April in Lithuania) are dropped from the
final micro dataset - 4 observations.

## Time period

The EU-SILC information on demographic variables mainly refers to the
time of data collection (January-April, 2024). Some included demographic
information (e.g. age variables) also reflects the status quo at the end
of the income reference period (2023). Similar situation is observed for
socio-economic and labour variables. For example, variable rb210 (i.e.
basic activity status) refers to the data collection time, while
variable pl073 indicates a number of months in full time work during the
income reference period (the calendar year of 2024). For the
construction of EUROMOD LT data, the demographic, labour, and
socio-economic information is based – when possible - on the EU-SILC
variables referring to the income reference period.

The EU-SILC EMSD 2023 information on incomes refers to the calendar year
of 2024. Some additional information on the number of income payments
per year and monthly amounts has been obtained and imputed from the
National SILC information. This has been done for selected income
sources only. All monetary incomes in the EUROMOD database are converted
into monthly terms, based on a 12-month receipt period. In the EUROMOD
calculations, it is implicitly assumed that income is received at the
same rate throughout the year.

The EU-SILC does not contain information on how many times per year a
certain type of income is actually received. National SILC, on the other
hand, collects this information for some income variables. This
information is (partially) used to construct EUROMOD variables on how
many times a particular income type was paid over the year (e.g., bunmy
– number of months per year receiving an unemployment benefit). In
cases, where the National SILC does not carry the relevant information
on the frequency of income receipts, other types of
imputations/assumptions have been applied. For example, if the concerned
income variable is reported as an aggregate income type (e.g. old-age
pensions), a corresponding EUROMOD variable on the “months of benefit
receipt” is constructed by summing the number of different pensions’
receipts – to the extent that this information is available in National
SILC. The maximum number of months is set to 12. Also, if the
information on a number of months of receiving one or another benefit is
missing in National SILC, the relevant EUROMOD variable is constructed
based on the indication on how many months a person has spent in a
certain socio-economic activity type (i.e. the EU-SILC EMSD variables
pl\*).

## Gross incomes

The EU-SILC EMSD survey contains information on both gross and net
monetary incomes, if applicable. The survey also contains flag
variables, which indicate if the observation has been collected either
in gross or net form, imputation method and imputation factor
(collected/recorded).

## Merged and imputed variables

4 provides information on the variables that have been merged from the
National SILC into the EUROMOD LT-data 2024. No other major
modifications have been done for these variables.

<span id="_Toc222228393" class="anchor"></span>**Table 3.4** EUROMOD LT
database: variables merged from the National SILC

| LT-data 2024 variables | Description |
|:---|:---|
| Aldar | Area of own or rented land (hectares) |
| Aldagar | Area of own or rented agricultural use land (hectares) |

Source: EUROMOD model documentation: DRD.

A number of EUROMOD LT-2024 variables are constructed using (merged)
information both from the National SILC and EU-SILC EMSD surveys, plus –
when needed – a number of other imputations. The main reason for such a
construction of the variables is related to incomplete or missing
information in both surveys. The concerned variables are:

- Severance pay (yunsv variable);

- Early retirement old-age pension (byr variable);

- Unemployment insurance benefit (bunct variable);

- Employment earnings – a number of months received (yemmy variable);

- Unemployment benefits – a number of months received (bunmy variable);

- Disability pensions – a number of months received (bdimy variable);

- Work history – a length of time in months (liwwh variable);

- Work history – imputed work history based on recalculation of pensions
  recorded in SILC and recorded work history in line with applied
  pension formula (liwivwh variable);

- Income – hourly predicted wage (yivwg variable);

- Income - wage coefficient (ywgfj variable);

- Income - employment income previous year (yempv variable);

- Income – taxable employment income (yemtx variable);

- Income – taxable self-employment income (ysetx variable);

- Disability benefits - imputed for kids based on parents’ status (ddi
  variable).

Information from the National SILC is also used in some other EUROMOD
LT-2022 variables construction cases. For example, *les* variable on the
economic status is mainly derived from the EU-SILC EMSD reported income
variables. However, information from the National SILC is used to form
one of the *les* variable categories – a farmer status. The latter
information is not available in the EU-SILC EMSD survey. The National
SILC, on the other hand, reports on the “income received from the
agricultural activity”. This information - in comparison to the relative
importance of the other income sources - is used to make an assumption
on being engaged in the farmer economic activities.

Information from the National SILC is also used in the disaggregation of
the disability (*bdi*) and old age (*boa*) variables. The National SILC
is used for the disaggregation of old-age (*boact*), state benefit
(*boanc*), pensions for officials and soldiers (*boaml*), state pension
for victims (*boawr*), social assistance (social) pension and
compensation (*boamt*) and other pensions (*boaot*). The national SILC
is also used for the disaggregation of disability pensions, such as:
lost work capacity (*invalidity*) pension (*bdict*), compensation for
people with disability (*bdixp*) and other benefits for people with
disability (*bdiot*).

Some EUROMOD LT-2024 are constructed based on the external macro
statistics and selected EU-SILC information. For example, a variable
*afc* on the financial capital assets is constructed in relation to the
EU-SILC variable on investment income and in relation to the external
information of the arithmetic average between the central bank base
interest rate (EURIBOR rate) and a harmonised indices of consumer prices
provided by Eurostat (HICP) . Variables *xed00* and *xhl00* includes
expenditures for education and healthcare are imputed based on HBS data.
Expenditures for education (*xed00*) are allocated to the household
head, while expenditures to health care (*xhl00*) are allocated to each
adult in the household the same share of health care expenditure.

## Uprating

To account for time inconsistencies between the input dataset and the
policy year, uprating factors are used. Each monetary variable (i.e.,
each income component) is uprated so as to account for changes in the
non-simulated variables that have taken place between the year of the
data and the year of the simulated tax-benefit system. Uprating factors
are generally based on changes in the average value of an income
component between the year of the data and the policy year. For detailed
information about the construction of each uprating factor as well as
the sources that have been used, see Annex 1.

As a rule, uprating factors are provided both for simulated and
non-simulated income components present in the input dataset. Note
however that in the case of simulated variables, the actual simulated
amounts are used in the baseline rather than the uprated original
variables in the dataset. Uprating factors for simulated variables are
provided so as to facilitate the use of the model in cases when the user
wishes to turn off the simulation of a particular variable. The list of
uprating factors as well as the sources used to derive them can be found
in Annex 1.

No other uprating adjustments are employed; therefore, the distribution
of receipts of non-simulated incomes remains constant throughout the
period, while the level of amounts received changes in line with the
uprating factors. The variables included in EUROMOD on household and
personal characteristics, such as housing type, employment status or
demographic attributes, are constant in relation to the basis year (in
the baseline scenario).

Since 2020, the list of uprating factors was supplemented with average
gross earnings by 12 sectors of economic activity. It allows to improve
the scope of simulations by uprating the income of each sector. For more
information see Annex 1.

## Input data extended with household expenditures 

For the simulation of consumption taxes, the model is run with extended
EUROMOD input files. This file extends the EUROMOD LT-data with 193 new
variables (household-level income shares of expenditures by product)
imputed from EU/National-HBS (*corresponding to the harmonized
consumption categories defined at COICOP \[2003\] level 4 (five
digits))*. The semi-parametric method implemented for the imputation
follows the methodology developed by Akoğuz et al (2020).

Please note that, due to the lack of information in the HBS files
distributed by Eurostat, there is no consumption reported at 5-digit
COICOP level for the following 3-digit codes: CP102.

Positive consumption might exist for 3-digit or 4-digit levels, but
EUROMOD uses only 5-digit values. <span class="mark"></span>[**Table
3.5**](#Table_03_05) summarizes the major features of the most recent
database used to be run with the policy systems of 2023-2025.

<span id="Table_03_05" class="anchor"></span>**Table 3.5** Extended
EUROMOD database description

| Extended EUROMOD database for the simulation of consumption taxes | SILC 2024 – Income year 2023 – Expenditures from HBS 2015 |
|----|----|
| EUROMOD database | LT_2024_c1_2015_03_e2 |
| Year of collection (HBS) and source | HBS 2015 – EU |
| Year of collection (SILC) and source | SILC 2024 – EU/National |
| Coverage and sample size | Same as LT_2024_c1 |
| Share of households with negative incomes excluded from the matching procedure | 0.08% |

Source: EUROMOD model documentation: DRD.

In <span class="mark"></span>[**Table 3.6**](#Table_03_06) we present
the share of households' consumption expenditures by product (and total)
captured in our matched databases (extended EM input files) with respect
to the original reported expenditures in HBS. The column that refers to
the same year (in this case, HBS 2015 with Extended EM Input 2015)
directly depends on the quality of the imputation procedure, while the
comparison across different years is influenced not only by the matching
noise but also by the changes in population characteristics and in the
underlining distribution of income. Therefore, the coverage displayed in
the second column is just informative but is not and should not be used
to evaluate nor validate the imputation procedure.

Information on the coverage of these simulated expenditures (coming from
the imputation of HBS 2015 to more recent SILC-based data) with respect
to the expenditures reported by National Accounts is included in section
4 of this report, together with the other macro-validation results.

Below we summarize the main findings from the imputation validation
checks for Lithuania.

<span id="Table_03_06" class="anchor"></span>**Table 3.6** Expenditure
coverage of Extended EM Input files

| COICOP group | HBS 2015 – Extended EM Input 2015 | HBS 2015 – Extended EM Input 2022 & 2024 |  |
|----|---:|---:|---:|
| 1 | 103.7% | 120.8% |  |
| 2 | 98.2% | 126.9% |  |
| 3 | 122.5% | 154.0% |  |
| 4 | 108.3% | 122.6% |  |
| 5 | 131.5% | 153.8% |  |
| 6 | 126.4% | 136.1% |  |
| 7 | 116.0% | 133.4% |  |
| 8 | 118.6% | 129.1% |  |
| 9 | 97.7% | 126.8% |  |
| 10 | 236.3% | 162.2% |  |
| 11 | 96.2% | 128.6% |  |
| 12 | 105.7% | 136.8% |  |
| Total | **121.8%** | **135.9%** |  |

Source: Own calculations.

# Validation

## Aggregate Validation 

EUROMOD results are validated against external statistics. Detailed
comparisons of the number of people receiving a given income component
and total annual spending and revenues are shown in Annex I. Both market
incomes and non-simulated taxes and benefits in the input dataset as
well as simulated taxes and benefits are validated against external
official data. The main discrepancies between EUROMOD results and
external benchmarks are discussed in the following subsections. Factors
that may explain the observed differences are also discussed.

## Components of disposable income

Before commenting on how different income components in EUROMOD compare
against their external aggregates, this subsection outlines the
differences in the definition of disposable income in EUROMOD and
EU-SILC The major components of disposable income are the same in both
sources: original incomes (+); benefits (+), taxes (-), employee social
insurance contributions (-); and self-employed social insurance
contributions (-). However, at the level of individual components there
are two differences as can be seen from [**Table 4.1**](#Table_04_01) :

- EU-SILC includes (imputed) annual value of (using) a company car,
  while EUROMOD definition of disposable income excludes this type of
  income;

- Pension from individual private plans is included in the disposable
  income concept in EUROMOD, while it is excluded in EU-SILC.

Apart from differences in the definition, the size of disposable income
in EU-SILC and EUROMOD can differ for a given household as simulated
income components in EUROMOD can differ for a number of reasons from
their observed counterparts in EU-SILC dataset.

<span id="Table_04_01" class="anchor"></span>**Table 4.1** Components of
disposable income

<table style="width:65%;">
<colgroup>
<col style="width: 24%" />
<col style="width: 12%" />
<col style="width: 7%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr>
<th></th>
<th><strong>EUROMOD</strong></th>
<th><strong>EU-SILC</strong></th>
<th><strong>Notes</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td></td>
<td>ils_dispy</td>
<td>hy020</td>
<td></td>
</tr>
<tr>
<td>Employee cash or near cash income</td>
<td>yem</td>
<td>py010g</td>
<td>yem is derived from py010g</td>
</tr>
<tr>
<td>Company car</td>
<td>-</td>
<td>py021g</td>
<td></td>
</tr>
<tr>
<td>Cash benefits or losses from self-employment</td>
<td>Yse</td>
<td>py050g</td>
<td>yse is derived from py050g</td>
</tr>
<tr>
<td>Pension from individual private plans</td>
<td>ypp</td>
<td>-</td>
<td>ypp is derived from py080g</td>
</tr>
<tr>
<td>Investment income</td>
<td>Yiy</td>
<td>hy090g</td>
<td>yiy is derived from hy090g</td>
</tr>
<tr>
<td>Income from rental of a property or land</td>
<td>Yprrt</td>
<td>hy040g</td>
<td>yprrt is derived from hy040g</td>
</tr>
<tr>
<td>Income received by people aged under 16</td>
<td>Yot</td>
<td>hy110g</td>
<td>yot is derived from hy110g</td>
</tr>
<tr>
<td>Regular inter-household cash transfer received</td>
<td>ypt</td>
<td>hy080g</td>
<td>ypt is derived from hy080g</td>
</tr>
<tr>
<td>Regular inter-household cash transfer paid (-)</td>
<td>Xmp</td>
<td>hy130g</td>
<td>xmp is derived from hy130g</td>
</tr>
<tr>
<td>Old-age benefits</td>
<td>boa</td>
<td>py100g</td>
<td>boa is derived from py100g</td>
</tr>
<tr>
<td>Survivor’ benefits</td>
<td>Bsu</td>
<td>py110g</td>
<td>bsu is derived from py110g</td>
</tr>
<tr>
<td>Disability benefits</td>
<td>bdi</td>
<td>py130g</td>
<td>bdi is derived from py130g</td>
</tr>
<tr>
<td>Unemployment benefits</td>
<td>yunsv, byr, bunct_s</td>
<td>py090g</td>
<td><p>3 comp. in EUROMOD: byr (early retirement), yunsv (severance pay)
&amp; bunct_s (unempl. ben.); byr &amp; yunsv are derived using EU-SILC
(py090), Nat. SILC &amp; external admin. info; bunct_s is EUROMOD
simulated.</p>
<p>Long-term work payment (bunct01_s) is not yet part of 2016 SILC
data.</p></td>
</tr>
<tr>
<td>Housing allowances</td>
<td>Bho</td>
<td>hy070g</td>
<td>bho is derived from hy070g</td>
</tr>
<tr>
<td>Family/children related benefits</td>
<td><p>bchor ,</p>
<p>bch00_s, bchba_s, bplct_s bmaprnc_s, bmaprct_s, bmact_s</p>
<p>bmaed_s</p>
<p>bchmp_s</p></td>
<td>hy050g</td>
<td>all “_s” variables are EUROMOD simulated benefits; bchor is merged
from Nat. SILC</td>
</tr>
<tr>
<td>Benefit for a single person</td>
<td>bsg_s</td>
<td>-</td>
<td>Simulated benefit since 2021</td>
</tr>
<tr>
<td>Education related allowances</td>
<td>bed</td>
<td>py140g</td>
<td>bed is derived from py140g</td>
</tr>
<tr>
<td>Sickness benefits</td>
<td>bhl</td>
<td>py120g</td>
<td>bhl is derived from py120g</td>
</tr>
<tr>
<td>Social exclusion not elsewhere classified</td>
<td>bsa00_s, bsals</td>
<td>hy060g</td>
<td>bsa00_s is EUROMOD simulated benefit; bsals is derived using EU-SILC
(hy060g), Nat. SILC &amp; external admin. Info</td>
</tr>
<tr>
<td>Tax on income and social contributions (-)</td>
<td>tin_s, ils_sicee, ils_sicse</td>
<td>hy140g</td>
<td>EUROMOD data includes 3 simulated components; tin_s refers to final
tax liability. hy140g also refers to final tax liability; among other
components it includes any tax reimbursement received (also for income
received in previous years);</td>
</tr>
<tr>
<td>Regular taxes on wealth (-)</td>
<td>tpr</td>
<td>hy120g</td>
<td>tpr is derived from hy120g</td>
</tr>
</tbody>
</table>

Source: EUROMOD model, documentation and own elaboration.

### Validation of incomes inputted into the simulation

*Note: Please see Annex 3 for tables.*

Before discussing the results for original income in EUROMOD, it should
be noted that weights for the Lithuanian EU-SILC are calibrated only
towards demographical variables [^71]. No calibration is done towards
the external income aggregates. Hence, the discrepancies between the
aggregate amounts and recipiency of the major sources of income in the
survey compared to those shown by external statistics might occur. The
data on minor income sources, such as some small-scale benefits,
collected in the survey might not be representative. The standard
updating procedure applied in EUROMOD would not correct for this, but
instead should move the estimates in the parallel way relative to the
dynamics shown by external sources. We thus focus on validating the base
year (i.e., 2023) and checking the dynamics of income in the following
years. However, it is important to note that for the 2022 policy year,
we use EU-SILC 2022 data (2021 income year). Of note, there are numerous
gaps in external statistics on the number of recipients of market income
and aggregate amounts.

Table A3.1 shows that the number of people receiving employment income
is overestimated in EUROMOD by around 12%, 10% and 7% for 2022, 2023 and
2024 respectively, as compared to the LFS figures. This may be partially
explained by the fact that EU-SILC based data would pick up income
received for short periods of time and sum the recipients across the
year, while in LFS the average annual number of those receiving
employment or self-employment income is given. As in the period of 2022
the labour market and the economy were recovering from the COVID-19
pandemic in 2023-2024, the ratio between EUROMOD and LFS improved over
the years. Meanwhile, the number of recipients of self-employment income
is highly overestimated in EUROMOD for allyears (ratios 2.55 to 2.31
respectively). Supposedly, people tend not to report their self-employed
activities to the authorities, and some may have short self-employment
spells. Other factors for overestimation of the number of self-employed
are similar to those for employment income recipients.

The annual gross employment income in EUROMOD is underestimated compared
to external statistics (see Table A3.2). We, however, are using
information on aggregate wages and salaries from the national accounts
that is not strictly comparable with the survey estimates available in
EU-SILC. The total amount of employment income is underestimated in
EUROMOD by around 11-15% in 2022-2024. The respective statistics for
other types of market income are not available. The results from EUROMOD
show a steady increase in the amount of gross employment income between
2022-2025. Same is observed in the external statistics.

### Validation of taxes, SIC and benefits 

*Note: Please see Annex 3 for tables.*

Table A3.3 shows numbers of taxes and social insurance contributions
(SICs) payers. Regarding simulated tax and SIC components, the number of
taxpayers of the personal income tax (PIT) is slightly underestimated
compared to external administrative statistics in the baselines of 2022
and 2023 (ratio at 0.87) and less in -2024, by 15% respectively. The
underestimation could be related to the number of employed and
self-employed recorded in EUROMOD data, which does not capture the
latest labour market trends. However, the number of payers of SIC shows
a very good fit with the external statistics. It is equal to 1 in 2022
and is slightly under-simulated by 1% in 2023, is by 2% in 2024.
External statistics on the payers of the employer social insurance
contributions is not available. However it can be assumed to be
simulated with the same precision as employee contributions. There are
no proper administrative data on the number of property tax payers and
self-employed persons and who do not have business certificates, thus
the number will be validated against statistics on aggregated amounts
only.

The validation of aggregate amounts of the simulated taxes and SICs is
shown in Table A3.4. Aggregate amounts of PIT simulated by EUROMOD are
very close to the external data. PIT is matched at a ratio of 0.97 in
20221 in 2023 and 1.01 in 2024. The annual employee SIC are
over-simulated by 11-14% in 2022-2024 compared with the aggregates
derived from Eurostat. However, the latter also does not match the
administrative records on SIC receipts from the State Social Insurance
Fund (SSIF). If we validate our results towards SSIF data, the match for
employee SIC corresponds well to the external statistics, as well as the
number of the SIC payers (see Table 4.2). I.e. employee SIC is
over-simulated in 2022 by around 2%, is equal to 1 in 2023 and
under-estimated in 2024 by 1%. The employer SIC shows over-simulation of
8-30%, however, the SSIF data does not reflect contributions paid in
cases when SIC floors are applied. There were no changes to employer SIC
contributions between 2022-2023, hence the change in the validation
ratios between these years might reflect a break in the underlying data.
Worth noting, employer contributions do not affect disposable incomes
and related indicators.

<span id="_Toc222228397" class="anchor"></span>**Table 4.2** Employee
and employer SIC in EUROMOD and based on SSIF data

<table style="width:62%;">
<colgroup>
<col style="width: 7%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 4%" />
<col style="width: 4%" />
</colgroup>
<thead>
<tr>
<th> </th>
<th colspan="4"><strong>EUROMOD</strong></th>
<th colspan="3"><strong>External</strong></th>
<th colspan="3"><strong>Ratio</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td> </td>
<td><strong>2022</strong></td>
<td><strong>2023</strong></td>
<td><strong>2024</strong></td>
<td><strong>2025</strong></td>
<td><strong>2022</strong></td>
<td><strong>2023</strong></td>
<td><strong>2024</strong></td>
<td><strong>2022</strong></td>
<td><strong>2023</strong></td>
<td><strong>2024</strong></td>
</tr>
<tr>
<td><strong>Employee SIC, Health excl.</strong></td>
<td style="text-align: center;">3,169</td>
<td style="text-align: center;">3,734</td>
<td style="text-align: center;">4,161</td>
<td style="text-align: center;">4,517</td>
<td style="text-align: center;">3,245</td>
<td style="text-align: center;">3,700</td>
<td style="text-align: center;">4152</td>
<td style="text-align: center;">0.98</td>
<td style="text-align: center;">1.01</td>
<td style="text-align: center;">1.0</td>
</tr>
<tr>
<td><strong>Employee SIC, Health incl.*</strong></td>
<td style="text-align: center;">4,972</td>
<td style="text-align: center;">5,832</td>
<td style="text-align: center;">6,498</td>
<td style="text-align: center;">7,053</td>
<td style="text-align: center;">5,054</td>
<td style="text-align: center;">5,762</td>
<td style="text-align: center;">6467</td>
<td style="text-align: center;">0.98</td>
<td style="text-align: center;">1.01</td>
<td style="text-align: center;">1.0</td>
</tr>
<tr>
<td><strong>Employer SIC, floors excl.**</strong></td>
<td style="text-align: center;">464</td>
<td style="text-align: center;">631</td>
<td style="text-align: center;">701</td>
<td style="text-align: center;">770</td>
<td style="text-align: center;">431</td>
<td style="text-align: center;">491</td>
<td style="text-align: center;">538</td>
<td style="text-align: center;">1.08</td>
<td style="text-align: center;">1.29</td>
<td style="text-align: center;">1.3</td>
</tr>
</tbody>
</table>

Notes: Numbers do not include contributions to the II pillar funded
pension funds. \* Atvira Sodra does not include Health Insurance
receipts, which are imputed based on the tariffs applied. \*\* Employer
SIC in Atvira Sodra does not include extra contributions paid by the
employer when SIC contribution floors are applied.

Source: SSIF receipts based on Atvira Sodra, URL:
<https://atvira.sodra.lt/>

The annual SIC amounts of self-employed are highly overestimated (with
the ratios of 2.06-1.75). The result is not surprising as people might
be reluctant to report to the tax authorities that they are
self-employed. Given the high tax avoidance level in Lithuania and that
the self-employed are concentrated in the bottom income decile, we can
tentatively conclude that the problem is related to the high level of
under-reporting of self-employment income to the tax authorities, while
default EUROMOD simulates the statutory tax incidence based on the
assumption of full tax compliance (tax compliance adjustments can be
switched on). This issue, however, calls for further in-depth
investigation. Finally, the total property tax revenue is overestimated
by 11% in 2022 and underestimated in EUROMOD data by around 19-21% in
2023-2024 compared with the external statistics for 2023-2024, which
might be due to both the sampling and reporting errors in SILC. The
increase in the official property tax revenue in 2023-2024 might also be
due to the changes in property prices in the result of the new mass
evaluations.

*Note: Please see Annex 3 for tables.*

Table A3.5 shows the number of recipients of pensions, means-tested and
non-means-tested benefits. The number of recipients of old-age and
disability benefits in EUROMOD is computed by summing up non-overlapping
types of benefits before and after retirement age (and as such the
numbers may not be completely comparable). The data show that the number
of recipients of old-age benefits is underestimated in EUROMOD by only
4-5% in 2022-2024. When it comes to the number of recipients of
disability pensions there is an overestimation, with the ratio of 1.25
in 2022 and 1.44 in 2023-24. As for the number of early retirement
old-age pension recipients, the number is overestimated by 24% in 2022,
but under-estimated by 9-12% in 2023-2024. Survivor’s pension incidence
is overestimated just by 3% in 2022, but the ratio increased to 1.12 in
2023 and further to 1.14 in 2024. Discrepancies between the number of
pension recipients in EUROMOD and in the external statistics may also be
due to the benefit aggregation-related issues in the EMSD-SILC and
under-representation of the different groups of pensioners in the
survey.

The number of the recipients of means-tested benefits are also shown in
Table A3.5. The number of social assistance benefit recipients are
underestimated by 4-11%in 2022 –2023 and reached the ratio of 1.03 for
2024. These discrepancies might be due to several reasons: it may be
related to the undeclared work and under-reporting of income to tax
authorities which allow people to apply for social assistance; and can
indicate the modelling issues in EUROMOD. I.e, since EUROMOD uses yearly
income, it is not capable of calculating precisely the monthly
entitlements for the social assistance benefit, for which incomes of
only the last three months, as opposite to yearly income, are
considered. Similarly, the recipients of the housing allowance (which
cover compensations for heating and water costs) are underestimated by
even larger extent in EUROMOD. The ratios for the housing allowances
stood at 0.54 in 2022, but largely increased to 1.70 in 2023 and 2.12 in
2024. These discrepancies can be the result of the small sample size and
data weighting issues in the survey, as well as the modelling
peculiarities mentioned earlier. Please note that the numbers on the
housing allowances are taken from the data by default, but their
simulations can be switched on in the model.

The municipal and NGO support is highly overestimated in EUROMOD with
the ratios of 2.29 in 2022, 3.21 in 2023 and 3.98 in 2024. Please note
that this support is not simulated in EUROMOD and taken directly from
the data. Also, no precise external statistical information is
available, therefore these ratios should be considered with extreme
caution.

The number of families with children eligible for the additional child
benefit (allowance) is overestimated in EUROMOD with the ratio of
1.44-1.91 in 2022-2024. This discrepancy might be due to several
reasons. The main reason could be the assumption of 100% benefit take-up
in EUROMOD. In addition, it can be because of our simulation of the
means-test.

Further results in Table A3.5 cover recipients of simulated and
non-simulated non-means-tested benefits. The number of recipients of a
birth grant is underestimated by 6-12% between 2022-2024. As the receipt
of birth grant is only dependant on the fact of the childbirth, the
accuracy of the results strongly depends on the representativeness of
the survey sample and different reference periods for demographic and
income variables. Same is true for the pregnancy grant (non-contributory
maternity benefit), albeit there is much higher discrepancy (ratio up to
1.65- in 2024). This grant is quite uncommon in Lithuania and even less
so in the data. Hence the discrepancy is due to a small sample size.

EUROMOD simulates the number of families receiving the universal child
benefit well (overestimation of 3% in 2022 and underestimation by 7-8%
in 2023-2024). However, the recipients of other benefits, such as the
benefit for multiple birth families and the student’s childcare benefit
cannot be well validated due to small (or non–existent) coverage, i.e.
there were no recipients of the multiple birth families benefit observed
in the sample.

More widely spread contributory benefits are captured with the ratios of
the paternity leave benefit being 0.99 in 2022, but less well between
2023-2024, with the ratio of 0.76. The coverage of the maternity benefit
is underestimated with the ratio between 0.78-0.85. The biggest issue is
an overestimation by around 30-46% of the childcare benefit recipients
in 2022-2024. Like with birth and pregnancy grants, the larger number of
childcare benefit recipients simulated in EUROMOD most likely is related
with the representativeness of the survey sample.

The number of recipients of the unemployment social insurance benefit is
underestimated by 40% in 2022. However, the ratio significantly improves
in 2023-2024 with the ratios of 1.07 and 1.03, respectively. Please
note, that labour market adjustments can be additionally performed by
using the LMA add-on, which allows user to introduce labour market
transitions that are more in line with the changes in the labour market
and in this way improve simulations.

The recipients of the non-simulated guardianship benefit are
underestimated in EUROMOD. The ratios for guardianship benefits are at
0.72-0.73 in 2022-2024.These discrepancies can be the result of the
small sample size and data weighting issues in the survey. Sickness
social insurance benefits are widespread, yet there are no suitable
administrative data on the number of recipients, apart from the number
of cases of illness. If we use this information, the number of
recipients in EUROMOD appears to be underestimated by around half. This
is expected as one person may be sick for more than one time within a
year, especially during the pandemic years.

*Note: Please see Annex 3 for tables.*

Aggregate amounts of non-simulated benefits are provided in the Table
A3.6. Starting with pension section, the aggregate amount of disability
benefits before the retirement age is under-estimated by 4% in EUROMOD
in 2022, but overestimated by 10-29% in 2023-2024. Old-age benefits are
underestimated by 11-14% in 2022-2024. This is in part due to a slightly
underestimated number of old-age benefit recipients. Despite of the
overestimation of the recipients of the early retirement old-age
pensions, aggregate amounts are overestimated by 13% in 2022. However,
in 2023-2024 the amounts are underestimated by 15-18%, which is closer
to underestimation of the number of the recipients. The aggregate
variable for survival benefits consists of a few major components:
survivor and orphan pensions (before the retirement age), funeral
benefit and grant in case of death of an insured person. This aggregate
benefit is under-reported in the EU-SILC-based EUROMOD data by 14-30% in
2022-2024.

The validation of aggregate amounts of the means-tested benefits section
is also shown in Table A3.6. The total aggregate amount for the social
assistance benefit in EUROMOD is overestimated by 28-50% throughout
2022-2024. We have to take into account that there were important
changes implemented due to the response to the Covid-19 crisis, such as
loosened eligibility conditions, increased income disregard for the
means-test and more generous equivalence scales used for the calculation
of the social assistance benefit amount that altogether resulted in the
increased aggregate amounts. In simulating the social assistance
benefits, full take-up is assumed by default.

According to external statistics, expenditure on housing allowances
increased by 1.8 times in 2023 as compared to 2022 and then came back to
similar numbers to 2022 values in 2024. This is driven by the energy
crisis due to the Russia's war against Ukraine and increased inflation,
in addition to the doubled number of benefit recipients from 2022 to
2023. The expenditure on compensations was only 0.12 compared to the
external amounts in EUROMOD data in 2022. But for the 2023 increased up
to 0.52 and oversimulation in 2024 with the ratio of 1.15. Simulations
of the compensations for heating and water costs can be turned ON in the
model, which are OFF by default in the baseline model.

It should be noted that spending on the additional child benefits is
over-simulated in EUROMOD for 2022-2024 by 53-55%. The overestimation of
annual amounts is related to the oversimulated number of the recipients
of the benefits (see Table A3.5). This may be due to the non-take-up,
which is not accounted for in the model and other reason mentioned
above. As the benefit is means-tested, the non-take-up is likely.

For municipal and NGO support the annual amounts appear to be largely
over-estimated in EUROMOD, although precise administrative statistics
are not available both what concerns aggregate amounts and the number of
recipients.

Regarding the simulated and non-simulated non-means-tested benefits
listed in Table A3.6, the aggregate amounts of the universal child
benefit show a very good fit for 2022-2024, with the slight
overestimation of 3%-6%. The birth grand also shows a good fit,
especially for 2024 (with the ratio of 0.96), but is underestimated by
12% in 2023 and 7% in 2022, which is related to the underestimation of
benefit recipients. As there were no student’s childcare benefits
recipients observed in the sample and a very few recipients of benefit
for multiple birth families, we cannot properly validate annual amounts
of both types of benefit (we simulate only 20% of the expenditures on
the later benefit). The annual amounts of the non-contributory pregnancy
grant are highly overestimated in EUROMOD in 2022-2024 (ratios from 1.55
to 1.81), which is in line with the overestimated number of grant
recipients. This is likely due to a very small number of mothers who can
apply for the benefit. Additionally, the reliable external statistic
regarding non-contributory maternity grants is lacking. However, the
share of this benefit in total spending on non-contributory benefits is
small.

The precision of the simulation of the contributory benefits varies from
benefit to benefit. The closest match with external data is achieved for
the childcare leave benefit (0.83-1.06 in 2022-2024), despite the
overestimated number of the recipients. The aggregate amounts of the
maternity benefit are oversimulated by %-in2022 and underestimated by
14-18% in 2023-2024 and this is related to overestimation of the
recipients of this benefit. The paternity benefits are over-estimated in
EUROMOD (by around 14-29%), despite the number of recipients showing an
underestimation with the external statistics. This discrepancy might be
due to the higher previous wage recorded in the SILC data, which is used
for the calculation of the benefit amount. The aggregate amounts of
contributory unemployment social insurance benefits are undersimulated
in EUROMOD with ratio of 0.64 in 2022, but overestimated by 8-17% in
2023-2024, which is in line with the underestimated number of the
unemployment benefit recipients, which could be improved with the
simulated labour market transitions via LMA Add-on. It is important to
remember that two baseline databases have been used in the simulation
(2021- and 2023-income year data).

For the non-simulated benefits, the aggregate severance pay amount is
underestimated nearly half in 2022 compared with the external statistics
and even more in later years. The amounts of the sickness benefits, on
contrary, are overestimated in the baseline with the ratio of 1.36 in
2022 but slightly decreased to 1.20-1.26 in 2023-2024, despite showing
much lower incidence rates. As far as aggregate amounts of the
guardianship benefits are concerned, the EUROMOD results indicate
underestimation of 46-53% in 2022-2024since the amounts recorded in the
external statistics doubles in two years' time due to substantial
increases in the guardianship benefit payment and its differentiation
according to the child’s age and needs. Nevertheless, this benefit
constitutes only a minor part of disposable income.

### Validation of simulated consumption taxes 

Table A3.9 and A3.10 show the validation of consumption taxes related
amounts. The top part of table A3.9 compares expenditures aggregated
amount from EUROMOD simulations with National Account (NA) external
statistics as reported by EUROSTAT. For 2025 spending is over simulated
in EUROMOD for the following categories: Food and non-alcoholic
beverages, Housing water and fuel, Health, Communications. Spending is
under-simulated for Alcoholic beverages and tobacco, Furnishing and
household equipment, Transport, Recreation and culture, Hotels and
Restaurants, Education, and Miscellaneous goods and services.

The second part of Table A3.9 compares aggregate revenues from
consumption taxes (i.e. VAT and excises) to external statistics from
EUROSTAT. The bottom part of the table shows simulated aggregate revenue
for some category of interest such as alcoholic drinks, tobacco and
energy products. In Lithuania both revenue from VAT and excises are
under-simulated and capture only part of the revenue from consumption
taxes. When looking at consumption taxes on specific items, the
simulation significantly underestimates the government revenue on most
of these products. Exceptions are Energy and Electricity for which
simulated revenue is bigger than official statistics. These
discrepancies are partly due to the fact that the survey data
underpinning the CT simulation are based on consumers declared
consumption that may differ from the actual consumption (e.g. people
misreport about how much they smoke and drink). To correct for this
problem, EUROMOD provides also adjusted consumption aggregates, where
the calibration/correcting factor is the ratio between NA aggregated
expenditures and EM aggregated simulated expenditures level 1 at
baseline. Effectively NA adjustment scales-up (or down) consumption and
tax liabilities of all individuals. Table A3.10 compares annual
Government revenue from consumption taxes after applying calibration to
NA. In the top part of table 3.10 we show that consumption tax revenues
simulated in Lithuania for private households sum up to 5,888 million
EUR for VAT and 1,716 million EUR for excises in 2024. As a result about
92% of aggregate VAT revenues and 90% of aggregate excises revenues are
simulated in EUROMOD. When looking at specific items at lower COICOP
details, the calibration also improves the estimation of government
revenue for several categories.

## Income distribution 

All income distribution results presented here are computed for
individuals according to their household disposable income (HDI)
equalised by the “modified OECD” equivalence scale. HDI are calculated
as the sum of all income sources of all household members net of income
tax and social insurance contributions. The weights in the OECD
equivalence scale are: first adult=1; additional person aged 14 and over
= 0.5; additional person under 14 = 0.3.

Off note, better match between the simulated and external statistics can
be obtained by switching on add-ons (LMA) and extensions (MWA, EPS, TCA,
FYA) available for Lithuania.

## Income inequality

*Note: Please see Annex 3 for tables.*

This section estimates how well EUROMOD tracks the changes in income
distribution and inequality for 2022-2023 compared to Eurostat where
possible (at the time of writing, Eurostat figures referring to income
up to the year 2023 (2024 survey data) were available). Table A3.7
indicates the distribution of equivalised disposable income. Results
show that in 2022-2023 the income shares by decile predicted by EUROMOD
are relatively close to those reported by Eurostat. A notable exception
is the bottom income decile, for which incomes are overestimated by 16%
in 2022 and 18% in 2023. This may be due to several issues, including
the assumptions of full benefit take-up, limitations of simulated
means-testing rules, etc.

While the median shows a good fit, the mean is under simulated and by 8%
in 2022 and 2023. The assumption of full tax compliance may play a role
here. Tax compliance adjustments can be performed in EUROMOD but are
excluded in the baseline. All this leads to the S80/20 ratio being
underestimated in EUROMOD in 2022 (ratio 0.92) and in 2023 (ratio 0.85).
For the Gini coefficients we find a closer match for EUROMOD and
Eurostat statistics (ratio of 0.97 in 2022 and 0.94 in 2023).

## Poverty rates 

*Note: Please see Annex 3 for tables.*

Table A3.8 shows that the at-risk of poverty rates in the baseline year
of 2022 are somewhat lower compared with those reported by EUROSTAT
(2022 and 2024 EU-SILC data) The worst fit between EU-SILC and EUROMOD
is for the 40% median equivalised income poverty thresholds for 2022 and
2023 (ratios 0.84 and 0.73 respectively) is due to over-estimation of
disposable income for the first income decile shown in Table A3.7.
Better match is achieved for the at-risk-of poverty rates at the
threshold of 60% median equivalised income (ratio of 0.89 in 2022-2023)
and a very close fit at the threshold of 70% median equivalised income
(ratio 0.97 for both years).

The comparison with the external statistics for 2022 and 2023 shows that
statistics are rather well aligned throughout the age groups, with the
higher degree of underestimation for children (ratios 0.76-0.85 for 0-15
years old). At-risk-of-poverty rate for the remaining age groups (16 and
above) are generally up to 10% lower compared with external statistics.
The exception is the 25-49 years old group, for which the
at-risk-of-poverty level well aligned in 2022 but is underestimated by
17%. These trends might be due to demographic representation in the
model.

## Summary of “health warnings”

In conclusion, the following major “health warnings” should be taken
into account when using Lithuanian EUROMOD module and the underlying
micro-data:

- The EU-SILC (Lithuanian part) is calibrated on a limited number of
  dimensions: residence area (7 groups), age (17 groups) and gender. No
  calibration is done towards external income aggregates. Therefore,
  recipiency and aggregate amounts for the major income sources may not
  match between EU-SILC and external aggregates. Analysis on the
  benefits/taxes/contributions to/by smaller population groups should be
  done with care due to issues of representativeness.

- The default assumption in EUROMOD is full benefit take-up and full
  compliance with taxes and contributions. Baseline scenario does not
  include any employment adjustments.

- In the case of simulating a more recent policy year than the income
  reference period for the underlying input dataset, non-simulated
  monetary variables are uprated using income-specific uprating factors,
  whereas demographic and socio-economic status variables remain
  constant.

- Amounts of income taxes and social contributions of employees are well
  aligned with external statistics. Amounts of contributions paid by the
  self-employed are highly overestimated, which may be due to different
  reasons: changes in the number of the self-employed, the quality of
  reported self-employment income in EU-SILC, etc.

- Major aggregate benefit categories are difficult to validate as they
  consist of diverse individual components and are often constructed in
  line with the legal retirement age.

- Social assistance, a means-tested benefit, tends to be over-simulated
  in EUROMOD due to complexity of the means-test, difficulties in
  simulating the means-test using EMSD SILC and changes in
  administration of this social assistance benefit (municipalities have
  gotten more discretionary power).

- Labour market transitions are switched OFF in EUROMOD baselines. As a
  consequence, the simulation of monetary compensation schemes does not
  produce any effect in baseline simulations.

- Extensions available for Lithuania include tax compliance adjustments
  (TCA), extended policy simulations for pensions (EPS), minimum wage
  adjustments (MWA) and full-year adjustments (FYA). These may help
  improve simulations, but are switched OFF in the baseline model.

- EUROMOD LT- data 2021 should be used with caution. As the income
  reference year of this data is 2020, all Covid-19 payments are
  included into the main aggregated income variables with limited
  possibilities to distinguish them from the general social benefits and
  pensions. LMA add-on should not be used in combination with LT- data
  2021 to avoid double counting of Covid-19 benefits.

# References

- Lietuvos Respublikos gyventojų pajamų mokesčio įstatymas
  <https://www.e-tar.lt/portal/lt/legalAct/TAR.C677663D2202/asr>

- Lietuvos respublikos 2012 metų valstybės biudžeto ir savivaldybių
  biudžetų finansinių rodiklių patvirtinimo įstatymas 2011 m. gruodžio
  20 d. Nr. XI-1823 and relevant ammendments

- Lietuvos Respublikos 2014 metų valstybės biudžeto ir savivaldybių
  biudžetų finansinių rodiklių patvirtinimo įstatymas 2013 m. gruodžio
  12 d. Nr. XII-659 and relevant ammendments.

- SoDRA ,
  <http://www.sodra.lt/lt/situacijos/statistika/pagrindiniai-socialiniai-rodikliai>

- Statistics Lithuania
  https://osp.stat.gov.lt/documents/10180/5118910/Gyvenimo+s%C4%85lygos+%5BLT%5D+721.html

# List of abbreviations and definitions

| Abbreviations | Definitions |
|----|----|
| AMII | Average Monthly Insured Income |
| AMS | Average Monthly Salary |
| APB | Assistance Pension Base |
| AS | Actual assets of a person |
| BCA | Benefit Calibration Adjustment |
| BMP | Basic Monthly Pension |
| BSA | Basic Social Allowance |
| BTA | Benefit Take-up Adjustment |
| CBN | Cost of Basic Needs |
| CIA | Consumption Inflation Adjustment |
| COICOP | Classification Of Individual COnsumption according to Purpose |
| CPI | Consumer Price Index |
| CT | Consumption Taxes |
| DG | Directorate-General |
| DRD | Data Requirement Document |
| DG ECFIN | European Commission Directorate-General for Economic and Financial Affairs |
| EEA | European Economic Area |
| EM | EUROMOD |
| DG EMPL | Directorate-General for Employment, Social Affairs and Inclusion |
| EMSD | EUROMOD SILC Database |
| EPS | Extended policy simulation |
| ESTAT | Eurostat |
| EU | European Union |
| EUR | Euro |
| FYA | Full Year Adjustments |
| HBS | Household Budget Survey |
| HDI | Household Disposable Income |
| HICP | Harmonised Index of Consumer Prices |
| IC | Indexation Coefficient |
| IIC | Individual Indexation Coefficient |
| IL | Income List |
| ISER | Institute for Social and Economic Research |
| JRC | Joint Research Centre |
| LFS | Labour Force Survey |
| LMA | Labour Market Adjustment |
| LT | Lithuania |
| MMS | Minimum Monthly Salary |
| MWA | Minimum Wage Adjustment |
| NA | National Account |
| NGO | Non-Governmental Organisation |
| NRR | Net Replacement Rate |
| OECD | Organisation for Economic Co-operation and Development |
| PIT | Personal Income Tax |
| RE | Ratio of Real Estate value |
| REFORM | European Commission Reform and Investment Task Force |
| RM | Ratio of value of movables |
| RP | Reference Points |
| SG | Secretariat-General |
| SIC | Social Insurance Contributions |
| SILC | Statistics on Income and Living Conditions |
| SODRA | Valstybinio socialinio draudimo fondo valdyba |
| SPB | State Pension Base |
| SSI | State Supported Income |
| SSIF | State Social Insurance Fund |
| DG TAXUD | European Commission Directorate-General for Taxation and Customs |
| TCA | Tax Compliance Adjustment |
| VAT | Value Added Tax |

# List of figures

[**Figure A2.3** Policy effects in 2024-2025, using the CPI-indexation
(1.6 %) [105](#_Toc222228363)](#_Toc222228363)

# List of tables

[**Table 1.1** Pension age for women and men, 2022-2026
[7](#_Toc222228364)](#_Toc222228364)

[**Table 1.2** Monthly BSA, SSI and CBN levels effective on 30th June
2022-2025, EUR [8](#Table_01_02)](#Table_01_02)

[**Table 1.3** RP and IC amounts, 30th June 2022-2025, EUR
[9](#_Toc222228366)](#_Toc222228366)

[**Table 1.4** Basic monthly pension, social assistance pension base and
state pension base, 30th June 2022-2025, EUR
[10](#_Toc222228367)](#_Toc222228367)

[**Table 1.5** State pension base, minimum and average monthly salary,
30th June 2022-2025, EUR [10](#Table_01_04)](#Table_01_04)

[**Table 2.1** Simulation of benefits in EUROMOD, 2022-2025
[24](#Table_02_01)](#Table_02_01)

[**Table 2.2** Simulation of taxes and social contributions in EUROMOD,
2022-2025 [27](#Table_02_02)](#Table_02_02)

[**Table 2.3** Main recent policy changes
[29](#_Toc222228371)](#_Toc222228371)

[**Table 2.4** EUROMOD Spine: order of simulation, 2022-2025
[32](#_Toc222228372)](#_Toc222228372)

[**Table 2.5** Additional child benefit coefficients on January 1, 2022–
2025 [39](#Table_02_05)](#Table_02_05)

[**Table 2.6** The compensation rate of childcare benefit, 2023- 2025
(as of 1st January) [45](#Table_02_06)](#Table_02_06)

[**Table 2.7** The compensation rate of the childcare benefit, 2022 (as
of 1st January) [45](#_Toc222228375)](#_Toc222228375)

[**Table 2.8** Levels of income disregard based on household type,
2022-2025 (as of 1st January) [53](#_Toc222228376)](#_Toc222228376)

[**Table 2.9** Characteristics of the unemployment social insurance
benefit, 2022-2025 [55](#_Toc222228377)](#_Toc222228377)

[**Table 2.10** Employee’s social contribution rates (% of gross
salary), effective on 2022-2025 [61](#Table_02_10)](#Table_02_10)

[**Table 2.11** Employers’ social insurance contributions (% of gross
salary), 2022-2025 [62](#Table_02_11)](#Table_02_11)

[**Table 2.12** Credited contributions (% of MMS), 2022-2025
[63](#Table_02_12)](#Table_02_12)

[**Table 2.13** Social insurance contribution rates (%) and bases for
different groups of self-employed, 2022-2025\*
[65](#Table_02_13)](#Table_02_13)

[**Table 2.14** Health insurance contribution rates (%) and bases for
different groups of self-employed, 2022-2025
[67](#_Toc222228382)](#_Toc222228382)

[**Table 2.15** 2nd pillar contribution rates to privately managed
pension funds and state subsidies (%), 2022-2025
[67](#_Toc222228383)](#_Toc222228383)

[**Table 2.16** Personal income basic allowance (EUR per month)
2022-2025 [72](#Table_02_16)](#Table_02_16)

[**Table 2.17** Personal income tax rates and thresholds, 2022-2025
[73](#_Toc222228385)](#_Toc222228385)

[**Table 2.18** VAT rates \[2022-2025\]
[75](#Table_02_18)](#Table_02_18)

[**Table 2.19** Ad-valorem excise rates \[2022-2025\]
[75](#_Toc222228387)](#_Toc222228387)

[**Table 2.20** Main specific (ad-quantum) excise rates
[76](#_Toc222228388)](#_Toc222228388)

[**Table 2.21** Prices of main excise products
[76](#_Toc222228389)](#_Toc222228389)

[**Table 3.1** EUROMOD LT 2022-2025: data and policy years
[78](#_Toc222228390)](#_Toc222228390)

[**Table 3.2** EUROMOD LT database 2024 short description
[78](#Table_03_02)](#Table_03_02)

[**Table 3.3** Descriptive statistics of the grossing-up weight rb050
(dwt) [80](#_Toc222228392)](#_Toc222228392)

[**Table 3.4** EUROMOD LT database: variables merged from the National
SILC [81](#_Toc222228393)](#_Toc222228393)

[**Table 3.5** Extended EUROMOD database description
[83](#Table_03_05)](#Table_03_05)

[**Table 3.6** Expenditure coverage of Extended EM Input files
[83](#Table_03_06)](#Table_03_06)

[**Table 4.1** Components of disposable income
[85](#Table_04_01)](#Table_04_01)

[**Table 4.2** Employee and employer SIC in EUROMOD and based on SSIF
data [88](#_Toc222228397)](#_Toc222228397)

[**Table A1.1** Uprating Factors [102](#_Toc222228398)](#_Toc222228398)

[**Table A2.1** Policy effects in 2024-2025, using the CPI-indexation, %
[104](#_Toc222228399)](#_Toc222228399)

[**Table A2.2** Policy effects in 2024-2025, in nominal values, %
[104](#_Toc222228400)](#_Toc222228400)

[**Table S.A.1** Validation Tables
[107](#_Toc221717387)](#_Toc221717387)

# List of Annexes

## Annex 1. Uprating Factors (2023 = 100)

<span id="_Toc222228398" class="anchor"></span>**Table A1.1** Uprating
Factors

<img src="media/image5.png" style="width:5.90625in;height:4.78125in" />

Source: EUROMOD model.

## Annex 2. Policy Effects in 2024-2025 

Indexation based on projected HICP for 2025[^72] (HICP = 1.6%)

Table A2.1 shows the effect of policy changes implemented in 2025 on
mean equalised household disposable income by income component and
income decile group, as a percentage of mean equalised household
disposable income in 2024. The effect is estimated as a difference
between simulated household net income under the 2025 tax-benefit
policies (deflating monetary parameters by Eurostat’s Harmonized Index
of Consumer Prices, HICP) and net incomes simulated under 2024 policies.

In general, we observe a progressive and positive effect to income in
all income deciles despite the inflation (of 1.6%) and due to the
measures implemented in 2025. The positive effects on disposable income
between 2024-2025 ranges from 0.69% in the 10th income decile to 8.87%
in the 1st decile. The real disposable incomes increased the most for
the second decile (by 9.3%). The implemented policy reforms resulted in
the progressive tax-benefit policy effect. The largest positive
contributions to incomes of the lowest income deciles are driven by the
changes in public pensions, and by the means-tested and non-means-tested
benefits. The positive impact of the direct taxes, on the other hand,
has an inverted U-shape, affecting incomes from the 3rd until the 7th
deciles (peaking at the 5th) more than at the tails of income
distribution. All deciles are affected by the small but negative real
changes in the self-employed SIC (mostly affecting the tenth decile),
and other SIC (mostly affecting the first decile). Meanwhile the
negative change in the employee SIC affects only the 10th decile.

The largest increase in disposable income is due to changes in public
pensions due to further pension indexation in 2025. On average, the
average old-age pensions increased by around 11%. State pensions (for
judges, officials, soldiers) have been indexed by 1.75%. State pensions
for victims and scientists have been increased in relation to state
pension base (SPB). Because of the increased SPB, higher pensions were
received by survivors and orphans, children and adults with
disabilities, the increased assistance pension base affected persons who
have not accumulated the required contributory history to receive the
old-age pension.

The positive changes in both the means-tested and non-means-tested
benefits between 2024 and 2025 are mainly related to the increased BSA
(from 55 to 70 EUR) and SSI (from 176 to 221 EUR) amounts, i.e. an
impressive increase by around one forth. The increase in the BSA
positively affects many benefits, such as birth grant, pregnancy grant,
multiple births grant, universal and additional child benefits. BSA is
also used to determine the floor for some contributory benefits, such as
maternity, paternity and parental benefits, thus affecting people with
low incomes. SSI, on the other hand, is important for the calculation of
social assistance benefit and compensations for heating and water.
Therefore, the overall impact off aforementioned changed is progressive,
affecting the affecting the first two income deciles more than the
others.

The positive impact of the direct taxes affected people mostly from the
3nr until the 7th deciles (peaking at the 5th) more than from the top
and bottom deciles. This is related to the changes in the thresholds and
amounts of the basic tax allowances: 747 EUR is applied to income below
MMS (1038 EUR); for income between MMS and 2387.29 EUR the withdrawal
rate is 0.49, while for those whose income is above 2387.29 EUR, the
withdrawal rate of 0.18 applied (as before). The allowance is not paid
for incomes equal or higher than the 2387.29 EUR. The amount of the
basic allowance was also increased for people with reduced working
capacity (level of participation). The higher negative impact of
employee SIC on income in the 10th decile is due to the automatic
indexation of the upper threshold of SIC payment (fixed at 5 average
wages per month), which increases effective SIC for high earners. The
stronger impact of other SIC on the first decile is related to the
increased minimum compulsory health insurance contributions which are
calculated as a share of the MMS, which was increased.

Overall, the changes between 2024 and 2025 had a positive progressive
impact, especially benefiting the bottom income deciles. Real disposable
income of the first and second deciles grew by about 9%. Overall policy
changes were pro-poor and with the orientation towards pensioners, who
are usually situated at the bottom of income distribution. Table A2.1
presents results in real terms, accounting for the CPI, and for
comparison purposes, Table A2.2 complements the report by showing
results in nominal terms. Due to low inflation (1.6%), the results in
both tables do not differ much and the later table (without inflation)
also convey the same message that the policy changes had a progressive
impact on income in 2025.

<span id="_Toc222228399" class="anchor"></span>**Table A2.1** Policy
effects in 2024-2025, using the CPI-indexation, %

<table style="width:68%;">
<colgroup>
<col style="width: 4%" />
<col style="width: 2%" />
<col style="width: 5%" />
<col style="width: 0%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 7%" />
<col style="width: 8%" />
<col style="width: 5%" />
<col style="width: 6%" />
<col style="width: 6%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"></th>
<th colspan="10" style="text-align: center;"><strong>Results for
Lithuania with alpha: CPI [1.016] on dataset LT_2024_c1</strong></th>
<th style="text-align: center;"></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: center;"><strong>Decile</strong></td>
<td colspan="2" style="text-align: center;"><strong>Orig.
income</strong></td>
<td style="text-align: center;"><strong>Public pensions</strong></td>
<td style="text-align: center;"><strong>Means-tested
benefits</strong></td>
<td style="text-align: center;"><strong>Non means- tested
benefits</strong></td>
<td style="text-align: center;"><strong>Employee SIC</strong></td>
<td style="text-align: center;"><strong>Self-employed SIC</strong></td>
<td style="text-align: center;"><strong>Other SIC</strong></td>
<td style="text-align: center;"><strong>Direct taxes</strong></td>
<td style="text-align: center;"><p><strong>Disp.</strong></p>
<p><strong>income</strong></p></td>
</tr>
<tr>
<td style="text-align: center;">1</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">2.23</td>
<td style="text-align: center;">4.09</td>
<td style="text-align: center;">2.95</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.11</td>
<td style="text-align: center;">-0.34</td>
<td style="text-align: center;">0.05</td>
<td style="text-align: center;">8.87</td>
</tr>
<tr>
<td style="text-align: center;">2</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">3.47</td>
<td style="text-align: center;">3.08</td>
<td style="text-align: center;">2.75</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.02</td>
<td style="text-align: center;">-0.07</td>
<td style="text-align: center;">0.11</td>
<td style="text-align: center;">9.31</td>
</tr>
<tr>
<td style="text-align: center;">3</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">3.40</td>
<td style="text-align: center;">1.89</td>
<td style="text-align: center;">2.19</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">-0.04</td>
<td style="text-align: center;">0.21</td>
<td style="text-align: center;">7.63</td>
</tr>
<tr>
<td style="text-align: center;">4</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">2.66</td>
<td style="text-align: center;">1.59</td>
<td style="text-align: center;">1.70</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">-0.04</td>
<td style="text-align: center;">0.27</td>
<td style="text-align: center;">6.17</td>
</tr>
<tr>
<td style="text-align: center;">5</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">1.87</td>
<td style="text-align: center;">1.00</td>
<td style="text-align: center;">1.43</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">-0.03</td>
<td style="text-align: center;">0.32</td>
<td style="text-align: center;">4.58</td>
</tr>
<tr>
<td style="text-align: center;">6</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">1.28</td>
<td style="text-align: center;">0.26</td>
<td style="text-align: center;">1.30</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">-0.04</td>
<td style="text-align: center;">0.30</td>
<td style="text-align: center;">3.09</td>
</tr>
<tr>
<td style="text-align: center;">7</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">1.02</td>
<td style="text-align: center;">0.09</td>
<td style="text-align: center;">0.92</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">-0.02</td>
<td style="text-align: center;">0.19</td>
<td style="text-align: center;">2.17</td>
</tr>
<tr>
<td style="text-align: center;">8</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">0.89</td>
<td style="text-align: center;">0.07</td>
<td style="text-align: center;">0.91</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">0.11</td>
<td style="text-align: center;">1.96</td>
</tr>
<tr>
<td style="text-align: center;">9</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">0.66</td>
<td style="text-align: center;">0.06</td>
<td style="text-align: center;">0.74</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.02</td>
<td style="text-align: center;">-0.02</td>
<td style="text-align: center;">0.04</td>
<td style="text-align: center;">1.47</td>
</tr>
<tr>
<td style="text-align: center;">10</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">0.33</td>
<td style="text-align: center;">0.01</td>
<td style="text-align: center;">0.46</td>
<td style="text-align: center;">-0.11</td>
<td style="text-align: center;">-0.06</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">0.06</td>
<td style="text-align: center;">0.69</td>
</tr>
<tr>
<td style="text-align: center;"><strong>Total</strong></td>
<td colspan="2" style="text-align: center;"><strong>0.00</strong></td>
<td colspan="2" style="text-align: center;"><strong>1.26</strong></td>
<td style="text-align: center;"><strong>0.60</strong></td>
<td style="text-align: center;"><strong>1.12</strong></td>
<td style="text-align: center;"><strong>-0.03</strong></td>
<td style="text-align: center;"><strong>-0.03</strong></td>
<td style="text-align: center;"><strong>-0.03</strong></td>
<td style="text-align: center;"><strong>0.14</strong></td>
<td style="text-align: center;"><strong>3.04</strong></td>
</tr>
</tbody>
</table>

Source: own calculations.

<span id="_Toc222228400" class="anchor"></span>**Table A2.2** Policy
effects in 2024-2025, in nominal values, %

<table style="width:66%;">
<colgroup>
<col style="width: 5%" />
<col style="width: 1%" />
<col style="width: 5%" />
<col style="width: 0%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 7%" />
</colgroup>
<thead>
<tr>
<th colspan="12" style="text-align: center;"><strong>Results for
Lithuania with alpha: custom [1] on dataset LT_2024_c1</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: center;"><strong>Decile</strong></td>
<td colspan="2" style="text-align: center;"><strong>Orig.
income</strong></td>
<td style="text-align: center;"><strong>Public pensions</strong></td>
<td style="text-align: center;"><strong>Means-tested
benefits</strong></td>
<td style="text-align: center;"><strong>Non means- tested
benefits</strong></td>
<td style="text-align: center;"><strong>Employee SIC</strong></td>
<td style="text-align: center;"><strong>Self-employed SIC</strong></td>
<td style="text-align: center;"><strong>Other SIC</strong></td>
<td style="text-align: center;"><strong>Direct taxes</strong></td>
<td style="text-align: center;"><p><strong>Disp.</strong></p>
<p><strong>income</strong></p></td>
</tr>
<tr>
<td style="text-align: center;">1</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">3.09</td>
<td style="text-align: center;">4.45</td>
<td style="text-align: center;">3.16</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.13</td>
<td style="text-align: center;">-0.40</td>
<td style="text-align: center;">0.07</td>
<td style="text-align: center;">10.25</td>
</tr>
<tr>
<td style="text-align: center;">2</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">4.37</td>
<td style="text-align: center;">3.34</td>
<td style="text-align: center;">2.92</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.03</td>
<td style="text-align: center;">-0.08</td>
<td style="text-align: center;">0.18</td>
<td style="text-align: center;">10.70</td>
</tr>
<tr>
<td style="text-align: center;">3</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">4.14</td>
<td style="text-align: center;">2.03</td>
<td style="text-align: center;">2.37</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">-0.05</td>
<td style="text-align: center;">0.33</td>
<td style="text-align: center;">8.81</td>
</tr>
<tr>
<td style="text-align: center;">4</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">3.21</td>
<td style="text-align: center;">1.72</td>
<td style="text-align: center;">1.85</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">-0.05</td>
<td style="text-align: center;">0.44</td>
<td style="text-align: center;">7.16</td>
</tr>
<tr>
<td style="text-align: center;">5</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">2.26</td>
<td style="text-align: center;">1.16</td>
<td style="text-align: center;">1.57</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.02</td>
<td style="text-align: center;">-0.03</td>
<td style="text-align: center;">0.51</td>
<td style="text-align: center;">5.46</td>
</tr>
<tr>
<td style="text-align: center;">6</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">1.54</td>
<td style="text-align: center;">0.30</td>
<td style="text-align: center;">1.43</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">-0.04</td>
<td style="text-align: center;">0.49</td>
<td style="text-align: center;">3.71</td>
</tr>
<tr>
<td style="text-align: center;">7</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">1.21</td>
<td style="text-align: center;">0.10</td>
<td style="text-align: center;">1.04</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">-0.03</td>
<td style="text-align: center;">0.35</td>
<td style="text-align: center;">2.66</td>
</tr>
<tr>
<td style="text-align: center;">8</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">1.06</td>
<td style="text-align: center;">0.08</td>
<td style="text-align: center;">1.03</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">0.24</td>
<td style="text-align: center;">2.38</td>
</tr>
<tr>
<td style="text-align: center;">9</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">0.79</td>
<td style="text-align: center;">0.07</td>
<td style="text-align: center;">0.84</td>
<td style="text-align: center;">0.00</td>
<td style="text-align: center;">-0.02</td>
<td style="text-align: center;">-0.02</td>
<td style="text-align: center;">0.12</td>
<td style="text-align: center;">1.77</td>
</tr>
<tr>
<td style="text-align: center;">10</td>
<td colspan="2" style="text-align: center;">0.00</td>
<td colspan="2" style="text-align: center;">0.40</td>
<td style="text-align: center;">0.01</td>
<td style="text-align: center;">0.53</td>
<td style="text-align: center;">-0.12</td>
<td style="text-align: center;">-0.07</td>
<td style="text-align: center;">-0.01</td>
<td style="text-align: center;">0.10</td>
<td style="text-align: center;">0.84</td>
</tr>
<tr>
<td style="text-align: center;"><strong>Total</strong></td>
<td colspan="2" style="text-align: center;"><strong>0.00</strong></td>
<td colspan="2" style="text-align: center;"><strong>1.54</strong></td>
<td style="text-align: center;"><strong>0.66</strong></td>
<td style="text-align: center;"><strong>1.23</strong></td>
<td style="text-align: center;"><strong>-0.03</strong></td>
<td style="text-align: center;"><strong>-0.03</strong></td>
<td style="text-align: center;"><strong>-0.04</strong></td>
<td style="text-align: center;"><strong>0.25</strong></td>
<td style="text-align: center;"><strong>3.59</strong></td>
</tr>
</tbody>
</table>

Source: own calculations.

<span id="_Toc222228363" class="anchor"></span>**Figure A2.3** Policy
effects in 2024-2025, using the CPI-indexation (1.6 %)

<img src="media/image6.png" style="width:5.90625in;height:3.35417in" />

Source: own calculations.

## Annex 3. Validation Tables

See [statistical annex](#statistical-annex-1.-validation-tables) for
details and tables.

## Annex 4. Recalculations and Compensations of Pensions

While pensions are not directly simulated in EUROMOD, we include the
following components into the model related to pension indexation, cuts,
compensations, and bonuses. Extended policy simulations for pensions are
off by default and can be switched ON using EPS extension.

First, due to fiscal consolidation during the period of economic crisis
social insurance and state pensions were progressively cut in Lithuania
in 2010. Cuts lasted until 2012 and since 2014 compensations for the
losses have been initialised. All these recalculations of pensions were
of progressive nature and had different effect on the different groups
of pensioners. Therefore, we opted for simulating them directly in the
model instead of applying the regular updating procedure for
non-simulated benefits. The structural cuts for the following categories
of pensions were simulated in EUROMOD for 2010-2011 and included into
the baseline (policy sheet *boa_lt*). Up to 2009 these benefits were
updated using regular updating procedure. In 2010-2011 the pension cuts
were implemented directly in the model; these simulations are linked to
2010 SILC (2009 income reference). For more information see previous
EUROMOD country reports for Lithuania.

The old-age pension indexation is also introduced and implemented in the
model (policy sheet *boa00_lt*). It is implemented based on the previous
employment history (liwivwh) and the number of reference points (ywgfj)
which are imputed in the data. Since 2018 policy system, the conversion
coefficient (0.78) is applied when recalculating former pension records
into the point system. Changes to the basic part of social insurance
pensions since 2022 are also modelled.

From 2019 onwards, small pension bonuses we implemented in EUROMOD based
on the Law on Social Assistance Pensions of the Republic of
Lithuania[^73]. If a person is eligible for the pension, he is paid a
full difference of 95% of cost of basic needs (CBN) and the received
pension. If a person has a minimum length of service but is not eligible
to receive the pension, the proportion of the bonus is reduced
proportionately. As of January 1st, 2020, an eligible person is paid a
full difference of 100% of cost of basic needs (CBN)[^74]. The bonus is
modelled in an intermediate variable (int_bonus) and added to boa01_s.

## Statistical Annex 1. Validation Tables

<span id="_Toc221717387" class="anchor"></span>**Table S.A.1**
Validation Tables

[^1]: Majority is an age threshold, recognized by the
    [law](http://en.wikipedia.org/wiki/Law), as a moment when a child
    assumes control over his/her actions, thereby terminating the legal
    control and legal responsibilities of parents or guardians.

[^2]: The precise dependent child definition is usually a benefit
    specific and could cover different conditions.

[^3]: Based on the following law “Dėl Lietuvos Respublikos Vyriausybės
    2014 m. lapkričio 5 d. nutarimo Nr. 1206 „Dėl socialinės paramos
    išmokų atskaitos rodiklių dydžių patvirtinimo“ pakeitimo” 2022-05-23
    Nr. 10912.

[^4]: Based on the following law “Lietuvos Respublikos Ligos ir
    motinystės socialinio draudimo įstatymo 3, 4, 5, 6, 8, 9, 16, 18, 19
    straipsnių pakeitimo ir papildymo Įstatymas”. 2008.12.18 Nr. XI-71.
    <http://www3.lrs.lt/pls/inter2/dokpaieska.showdoc_l?p_id=334539>http://www3.lrs.lt/pls/inter2/dokpaieska.showdoc_l?p_id=334539

[^5]: Based on the following law “Lietuvos Respublikos Valstybinio
    socialinio draudimo fondo biudžeto 2022 metų rodiklių patvirtinimo
    įstatymas”. 2021-12-14 Nr. XIV-749.

[^6]: Based on the following law “Lietuvos Respublikos Valstybinio
    socialinio draudimo fondo biudžeto 2022 metų rodiklių patvirtinimo
    įstatymas”. 2021-12-14 Nr. XIV-749.

[^7]: Based on the following law “ Lietuvos Respublikos valstybinių
    šalpos išmokų įstatymo Nr. I-675 pakeitimo įstatymas“. 2016-06-29,
    Nr. XII-2506.
    <https://www.e-tar.lt/portal/lt/legalAct/f5ee93504a6e11e6b5d09300a16a686c>

[^8]: Based on the following law “CloseDėl Lietuvos Respublikos
    Vyriausybės 2014 m. lapkričio 5 d. nutarimo Nr. 1206 „Dėl socialinės
    paramos išmokų atskaitos rodiklių dydžių patvirtinimo“ pakeitimo”.
    2022-05-23 Nr. 10912

[^9]: As set in the following Laws: “[Lietuvos Respublikos valstybinio
    socialinio draudimo fondo biudžeto rodiklių patvirtinimo
    įstatymas](https://www.e-tar.lt/portal/lt/legalAct/5fc0c06002b311e9a5eaf2cd290f1944)”
    and “[Lietuvos Respublikos valstybės socialinių fondų biudžetų
    rodiklių patvirtinimo
    įstatymas](https://www.e-tar.lt/portal/lt/legalAct/5fc0c06002b311e9a5eaf2cd290f1944)”

[^10]: Based on the following law “Lietuvos Respublikos Išmokų vaikams
    įstatymo 1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 13, 14, 18, 20, 22
    straipsnių ir antrojo, trečiojo skirsnių pavadinimų pakeitimo
    įstatymas”. 2008.07.01. Nr. X-1664:
    <http://www3.lrs.lt/pls/inter2/dokpaieska.showdoc_l?p_id=324329>

[^11]: Based on the following law “Lietuvos Respublikos išmokų vaikams
    įstatymo Nr. I-621 6, 9, 11, 12, 13, 14, 15, 17, 18, 19, 21
    straipsnių ir priedo pakeitimo įstatymas”. 2021-12-07, Nr. XIV-720.
    <https://www.e-tar.lt/portal/legalAct.html?documentId=964f55405d9311eca9ac839>
    120d251c4

[^12]: Based on the following law “Lietuvos Respublikos išmokų vaikams
    įstatymo Nr. I-621 6, 9, 11, 12, 13, 14, 15, 17, 18, 19, 21
    straipsnių ir priedo pakeitimo įstatymas”. 2021-12-07, Nr. XIV-720.
    <https://www.e-tar.lt/portal/legalAct.html?documentId=964f55405d9311eca9ac839>
    120d251c4

[^13]: Based on the following law “ Lietuvos Respublikos išmokų vaikams
    įstatymo Nr. I-621 1, 3, 10, 12, 13 straipsnių, ketvirtojo skirsnio
    pavadinimo pakeitimo ir Įstatymo papildymo 10-1 ir 10-2 straipsniais
    įstatymo Nr. XII-2500 5 straipsnio pakeitimo įstatymas“. 2016-06-28.
    Nr. XII-2500:
    <https://www.e-tar.lt/portal/legalAct.html?documentId=250ebe404a6e11e6b5d09300a16a686c>

[^14]: Based on the following law “Lietuvos Respublikos išmokų vaikams
    įstatymo Nr. I-621 9 straipsnio pakeitimo įstatymas”. Nr. XIV-83:
    <https://www.e-tar.lt/portal/legalAct.html?documentId=95e6c310450a11eb8d9fe110e148c770>

[^15]: Based on the following law: “Lietuvos Respublikos išmokų vaikams
    įstatymo Nr. I-621 6, 9, 11, 12, 13, 14, 15, 17, 18, 19,
    21 straipsnių ir priedo pakeitimo įstatymas”. 2021-12-07, Nr.
    XIV-720.
    <https://www.e-tar.lt/portal/legalAct.html?documentId=964f55405d9311eca9ac839120d251c4>

[^16]: Based on the following law „Lietuvos Respublikos išmokų vaikams
    įstatymo Nr. I-621 1, 3, 10, 12, 13 straipsnių, ketvirtojo skirsnio
    pavadinimo pakeitimo ir Įstatymo papildymo 10-1 ir 10-2 straipsniais
    įstatymas“. 2016-06-28. Nr. XII-2500:
    <https://www.e-tar.lt/portal/legalAct.html?documentId=250ebe404a6e11e6b5d09300a16a686c>

[^17]: Based on the following law ,, Lietuvos Respublikos išmokų vaikams
    įstatymo Nr. I-621 8 straipsnio pakeitimo įstatymas“. 2015-12-15.
    Nr. XII-2191:
    <https://www.e-tar.lt/portal/legalAct.html?documentId=8e886460a8ad11e5be7fbe3f919a1ebe>

[^18]: Based on the following law „Lietuvos Respublikos išmokų vaikams
    įstatymo Nr. I-621 3, 16, 17, 19, 21 straipsnių, trečiojo skyriaus
    pavadinimo pakeitimo ir Įstatymo papildymo 12-1 straipsniu
    įstatymas“. 2019-05-07, Nr. 7400.

[^19]: Based on the following law: “Lietuvos Respublikos piniginės
    socialinės paramos nepasiturintiems gyventojams įstatymo Nr. IX-1675
    7 ir 11 straipsnių pakeitimo įstatymas”. No. XIV-721, 2021-12-07.

[^20]: Based on the following law “Lietuvos Respublikos valstybinių
    pensijų įstatymo Nr. I-730 15-1 straipsnio pakeitimo įstatymas”

[^21]: Based on the following law: 2016-07-15, No. XII-2512 „Lietuvos
    Respublikos valstybinių socialinio draudimo pensijų įstatymo Nr.
    I-549 pakeitimo įstatymas“. 2016. No. 20649.

[^22]: Based on the following law “Lietuvos Respublikos socialinio
    draudimo pensijų įstatymo Nr. I-549 2, 8, 17, 29, 33, 45 ir
    49 straipsnių pakeitimo įstatymas”. 2021-11-23, Nr. XIV-678.

[^23]: Based on the following law: 2019-04-19,,Lietuvos Respublikos
    šalpos pensijų įstatymas”. 2019. No. 96-1873

[^24]: Based on the following law “Lietuvos Respublikos vienišo asmens
    išmokos įstatymo Nr. XIV-352 2, 3, 5 ir 8 straipsnių pakeitimo
    įstatymas”. 2021-11-23, Nr. XIV-679.

[^25]: 34.5 in 2026 and starting 2027, the contributory requirement is
    set to 35 years.

[^26]: Based on the following law: ‘Lietuvos Respublikos socialinio
    draudimo pensijų įstatymo Nr. I-549 22 straipsnio pakeitimo
    įstatymas‘. No. XIII-3394, 2020-11-10.
    <https://www.e-tar.lt/portal/legalAct.html?documentId=6ac80c5029a511eb932eb1ed7f923910>

[^27]: <sup>R</sup>equired period of insurance is being increased by 3
    months every year until reaches 42 years and 6 months in 2031. Based
    on the following law: ‘Lietuvos Respublikos socialinio draudimo
    pensijų įstatymo Nr. I-549 23 and 54 straipsnių pakeitimo įstatymo
    Nr. XIII-3203 pakeitimo įstatymas’. No. XIII-3395, 2020-11-10.

[^28]: Until 1st July 1, 2005 defined as invalidity (invalidumo)
    pension.

[^29]: Based on the following law: 2017-12-12, No. XIII-881 “Lietuvos
    Respublikos valstybinių socialinio draudimo pensijų įstatymo Nr.
    I-549 pakeitimo įstatymo Nr. XII-2512 1 ir 3 straipsnių pakeitimo
    įstatymas”. 2017, No. 20433.

[^30]: Based on the following law: 2018-12-20, No. XIII-1827 “Lietuvos
    Respublikos ligos ir motinystės socialinio draudimo įstatymo Nr.
    IX-110 6 straipsnio pakeitimo įstatymas”. 2018, Nr. 21847.

[^31]: Based on the following law: 2018-06-28, No. XIII-1338 “Lietuvos
    Respublikos ligos ir motinystės socialinio draudimo įstatymo Nr.
    IX-110 6, 14, 18, 21, 22, 24 ir 27 straipsnių pakeitimo įstatymas”.
    2018, No. Nr. 11433.

[^32]: Based on the following law: 2018-06-28, No. XIII-1338 “Lietuvos
    Respublikos ligos ir motinystės socialinio draudimo įstatymo Nr.
    IX-110 6, 14, 18, 21, 22, 24 ir 27 straipsnių pakeitimo įstatymas”.
    2018, No. 11433.

[^33]: Based on the following law: 2018-06-28, No. XIII-1339 “Lietuvos
    Respublikos nelaimingų atsitikimų darbe ir profesinių ligų
    socialinio draudimo įstatymo Nr. VIII-1509 3, 15, 19, 26 ir 27
    straipsnių pakeitimo įstatymas”. 2018, No. 11434.

[^34]: Based on the following law: 2018-06-28, No. XIII-1339 “Lietuvos
    Respublikos nelaimingų atsitikimų darbe ir profesinių ligų
    socialinio draudimo įstatymo Nr. VIII-1509 3, 15, 19, 26 ir 27
    straipsnių pakeitimo įstatymas”. 2018, No. 11434.

[^35]: Based on the following law: 2018-12-11, No. XIII-1722 “Lietuvos
    Respublikos nelaimingų atsitikimų darbe ir profesinių ligų
    socialinio draudimo įstatymo Nr. VIII-1509 20 straipsnio pakeitimo
    įstatymas”. 2018, No. 20976.

[^36]: Based on the followng law: 2018-06-28, No. XIII-1339 “Lietuvos
    Respublikos nelaimingų atsitikimų darbe ir profesinių ligų
    socialinio draudimo įstatymo Nr. VIII-1509 3, 15, 19, 26 ir 27
    straipsnių pakeitimo įstatymas”. 2018, No. 11434.

[^37]: Based on the following resolution “Socialinių stipendijų aukštųjų
    mokyklų studentams skyrimo ir administravimo tvarkos aprašas”.
    Patvirtinta Lietuvos Respublikos Vyriausybės 2009 m. gruodžio 23 d.
    nutarimu Nr. 1801.
    <http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=390234>.

[^38]: Based on the following law: ‘Lietuvos Respublikos mokslo ir
    studijų įstatymo Nr. XI-242 82 straipsnio pakeitimo ir Įstatymo
    papildymo 82-1 straipsniu įstatymas’. 2020-06-09, Nr. 12613.
    <https://www.e-tar.lt/portal/legalAct.html?documentId=09329240aa5611eab9d9cd0c85e0b745>

[^39]: Based on the following law; ‘Lietuvos Respublikos valstybinio
    socialinio draudimo įstatymo Nr. I-1336 10, 15, 16, 32 ir 34
    straipsnių pakeitimo ir Įstatymo papildymo 34-1 straipsniu
    įstatymas’. No. XIII-1720, 2018-12-11.
    <https://www.e-tar.lt/portal/legalAct.html?documentId=be79ae40044911e9a5eaf2cd290f1944>

[^40]: Based on the following law: 2018-12-11, No. XIII-1719 “Lietuvos
    Respublikos valstybinio socialinio draudimo fondo biudžeto 2019 metų
    rodiklių patvirtinimo įstatymas”. 2018, No. 20701.

[^41]: Based on the following law: 2018-12-11, No. XIII-1719 “Lietuvos
    Respublikos valstybinio socialinio draudimo fondo biudžeto 2019 metų
    rodiklių patvirtinimo įstatymas”. 2018, No. 20701.

[^42]: Based on the following law: ‘Lietuvos Respublikos pelno mokesčio
    įstatymo Nr. IX-675 5 ir 30 straipsnių pakeitimo įstatymas‘. No.
    XIV-39, 2020-12-15.
    <https://www.e-tar.lt/portal/legalAct.html?documentId=c176eaf03ede11eb8d9fe110e148c770>

[^43]:

[^44]: Based on the following law: „Lietuvos Respublikos pelno mokesčio
    įstatymo Nr. IX-675 2, 4, 12, 14, 30, 31, 55, 56-1 straipsnių, 3
    priedėlio pakeitimo ir Įstatymo papildymo 38-3, 40-2, 56-2
    straipsniais įstatymas“. 2019-12-30. Nr. 21550.

[^45]: Based on the following resolution “LR Vyriausybės 1993 m.
    rugpjūčio 3 d. nutarimas [Nr.
    603](http://www3.lrs.lt/cgi-bin/preps2?Condition1=11340&Condition2=)
    „Dėl žemės mokesčio“.

[^46]: Based on the following law “Lietuvos Respublikos Žemės mokesčio
    įstatymo pakeitimo įstatymas“. Žin., 2011, Nr. 163-7743.
    <http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=415667&p_query=&p_tr2=2>

[^47]: Based on the following law: ‘Lietuvos Respublikos išmokų vaikams
    įstatymo Nr. I-621 2, 6, 10, 15, 17, 18, 20 ir 21 straipsnių
    pakeitimo įstatymo Nr. XIII-2693 2 straipsnio pakeitimo įstatymas’.
    No. Nr. XIV-129, 2020-12-23.

[^48]: Based on the following law “Lietuvos Respublikos išmokų vaikams
    įstatymo Nr. I-621 2, 6, 10, 15, 17, 18, 20 ir 21 straipsnių
    pakeitimo įstatymas”. 2019-12-30. No. 21548

[^49]: Based on the following law: 2018-06-28, No. XIII-1338 ,, Lietuvos
    Respublikos ligos ir motinystės socialinio draudimo įstatymo Nr.
    IX-110 6, 14, 18, 21, 22, 24 ir 27 straipsnių pakeitimo įstatymas“,
    2018, No. 11433

[^50]: Note that being on maternity leave is considered as in work in
    the underlying data source, i.e. EU-SILC.

[^51]: Based on the following law ‘Lietuvos Respublikos ligos ir
    motinystės socialinio draudimo įstatymo Nr. IX-110 4, 5, 6, 8, 9,
    10, 11, 12, 13, 14, 16, 18, 19, 21, 23, 24, 25, 27 ir 33 straipsnių
    pakeitimo įstatymas’. No. 20050.

[^52]: According to the following law: Lietuvos Respublikos Ligos ir
    motinystės socialinio draudimo įstatymo 3, 5, 6, 8, 10, 15, 16, 17,
    18, 181, 183, 19, 20, 21 straipsnių pakeitimo ir papildymo
    įstatymas. 2007 m. Gruodžio 4 d. Nr. X-1338:
    <http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=310952>

[^53]: Based on the following law: 2018-06-28, No. XIII-1338 ,, Lietuvos
    Respublikos ligos ir motinystės socialinio draudimo įstatymo Nr.
    IX-110 6, 14, 18, 21, 22, 24 ir 27 straipsnių pakeitimo įstatymas“,
    2018, No. 11433

[^54]: Self-employed persons: engaged in individual activities, persons
    engaged in individual agricultural activity, family-type
    guardianship institution, the owners of individuals enterprises,
    ‘real members’ of agricultural communities.

[^55]: Based on the following law: ‘Lietuvos Respublikos ligos ir
    motinystės socialinio draudimo įstatymo Nr. IX-110 2, 4, 5, 11-1,
    14, 18, 21 ir 24 straipsnių pakeitimo įstatymas‘. 2020-12-29, No.
    28981

[^56]: Note that being on maternity leave is considered as in work in
    the underlying data source, i.e. EU-SILC.

[^57]: On the basis of *the Law of Child Benefits*

[^58]: Based on the following Law: ‘Lietuvos Respublikos piniginės
    socialinės paramos nepasiturintiems gyventojams įstatymo Nr. IX-1675
    2 ir 8 straipsnių pakeitimo įstatymas’. No. XIII-3375, 2020-11-05.
    <https://www.e-tar.lt/portal/legalAct.html?documentId=732a064025be11eb932eb1ed7f923910>

[^59]: Based on Methodology of Asset Evaluation (*Turto vertinimo
    metodika*),

[^60]: 1 Are = 100 square meters

[^61]: 1 Hectare = 10000 sq. meters or 100 Ares

[^62]: Based on the following Law: ‘Lietuvos Respublikos piniginės
    socialinės paramos nepasiturintiems gyventojams įstatymas’. No.
    XIII-2883, 2020-05-07.

[^63]: Based on the following law: ‘Lietuvos Respublikos piniginės
    socialinės paramos nepasiturintiems gyventojams įstatymo Nr. IX-1675
    3, 6, 7, 9, 10, 11, 15, 17, 21 ir 23 straipsnių pakeitimo įstatymo
    Nr. XIII-2883 11 straipsnio pakeitimo įstatymas’. No. 11866.

[^64]: Changes effective on the 30th June, 2009 indicated according to
    the following law: “Lietuvos Respublikos Piniginės socialinės
    paramos nepasiturinčioms šeimoms ir vieniems gyvenantiems asmenims
    įstatymo 15 ir 22 straipsnių pakeitimo įstatymas“. 2008.06.17 Nr.
    X-1611:
    <http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=323463>

[^65]: Based on the following law: „Lietuvos Respublikos piniginės
    socialinės paramos nepasiturintiems gyventojams įstatymo Nr. IX-1675
    17 straipsnio pakeitimo įstatymas“. 2019-07-03, Nr. 10931

[^66]: Based on the following law „Lietuvos Respublikos garantijų
    darbuotojams jų darbdaviui tapus nemokiam ir ilgalaikio darbo išmokų
    įstatymo Nr. XII-2604 2, 3, 5, 6, 7, 8, 10 ir 19 straipsnių
    pakeitimo įstatymas“. 2019-06-27, Nr. 10341

[^67]: Based on the following law: ‘Lietuvos Respublikos valstybinio
    socialinio draudimo įstatymo Nr. I-1336 6, 10, 11, 12, 14, 15, 16,
    19, 19-1, 21, 29, 30, 32, 36, 40 ir 41 straipsnių pakeitimo
    įstatymas’. Nr. XIV-123, 2020-12-23.
    <https://www.e-tar.lt/portal/legalAct.html?documentId=a235e98049e611eb8d9fe110e148c770>.

[^68]: Source: “Lietuvos respublikos 2012 metų valstybės biudžeto ir
    savivaldybių biudžetų finansinių rodiklių patvirtinimo įstatymas“
    2011 m. gruodžio 20 d. Nr. XI-1823 and relevant ammendments.

    “Lietuvos Respublikos 2014 metų valstybės biudžeto ir savivaldybių
    biudžetų finansinių rodiklių patvirtinimo įstatymas” 2013 m.
    gruodžio 12 d. Nr. XII-659 and relevant ammendments.

[^69]: Akoğuz, Elif Cansu, Bart Capéau, André Decoster, Liebrecht De
    Sadeleer, Duygu Güner, Kostas Manios, Alari Paulus, and Toon
    Vanheukelom. A new indirect tax tool for EUROMOD: final report.
    Technical Report, https://euromod-web. jrc. ec. europa.
    eu/sites/default/files/2021-03/A% 20new% 20indirect% 20tax% 20tool%
    20for% 20EUROMOD% 20Final% 20Report. pdf, 2020.

[^70]: The list of variables which are merged into the EUROMOD LT-data
    from the National SILC is provided in Table 3.4.

[^71]: See EU-SILC quality reports available at:
    <http://epp.eurostat.ec.europa.eu/portal/page/portal/income_social_inclusion_living_conditions/quality/national_quality_reports>

[^72]: Results based on the final HICP will appear in the annual EUROMOD
    report <u>Effects of tax-benefit policy changes across the income
    distributions of the EU-28 countries: 2019-22 (updated)</u>.

[^73]: Based on the following law: Lietuvos Respublikos šalpos pensijų
    įstatymas, No. I-675.
    <https://www.e-tar.lt/portal/lt/legalAct/TAR.2CE6CFE9E2EE>

[^74]: Based on the following law „Lietuvos Respublikos šalpos pensijų
    įstatymo Nr. I-675 8, 20, 22-1, 22-2 ir 24 straipsnių pakeitimo
    įstatymas“. 2019-12-19, Nr. 20564.
