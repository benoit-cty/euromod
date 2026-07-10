Cover

Contents

[Abstract [4](#_Toc222328587)](#_Toc222328587)

[Acknowledgements [5](#_Toc222328588)](#_Toc222328588)

[Authors [5](#_Toc222328589)](#_Toc222328589)

[1. Introduction [6](#introduction)](#introduction)

[1.1. Basic information regarding the tax-benefit system
[6](#basic-information-regarding-the-tax-benefit-system)](#basic-information-regarding-the-tax-benefit-system)

[1.2. Social benefits [7](#social-benefits)](#social-benefits)

[1.3. Social contributions
[9](#social-contributions)](#social-contributions)

[1.4. Taxes [9](#taxes)](#taxes)

[1.5. Extraordinary measures
[10](#extraordinary-measures)](#extraordinary-measures)

[2. Simulation of taxes, social insurance contributions and benefits in
EUROMOD
[11](#simulation-of-taxes-social-insurance-contributions-and-benefits-in-euromod)](#simulation-of-taxes-social-insurance-contributions-and-benefits-in-euromod)

[2.1. Scope of simulation
[11](#scope-of-simulation)](#scope-of-simulation)

[2.2. Main policy changes
[14](#main-policy-changes)](#main-policy-changes)

[2.2.1. In 2022 [16](#in-2022)](#in-2022)

[2.2.2. In 2023 [17](#in-2023)](#in-2023)

[2.2.3. In 2024 [19](#in-2024)](#in-2024)

[2.2.4. In 2025 [27](#in-2025)](#in-2025)

[2.3. Order of simulations and interdependence
[34](#order-of-simulations-and-interdependence)](#order-of-simulations-and-interdependence)

[2.4. Policy extensions [37](#policy-extensions)](#policy-extensions)

[2.5. Benefits [39](#benefits)](#benefits)

[2.5.1. Unemployment benefit – insurance (*bunct_pt*)
[39](#unemployment-benefit-insurance-bunct_pt)](#unemployment-benefit-insurance-bunct_pt)

[2.5.2. Unemployment Benefit – Assistance (*bunnc_pt*)
[41](#unemployment-benefit-assistance-bunnc_pt)](#unemployment-benefit-assistance-bunnc_pt)

[2.5.3. Minimum pension (*poacm_pt*)
[43](#minimum-pension-poacm_pt)](#minimum-pension-poacm_pt)

[2.5.4. Old age social pension (*poanc_pt*)
[44](#old-age-social-pension-poanc_pt)](#old-age-social-pension-poanc_pt)

[2.5.5. Solidarity supplement for the elderly (*bsaoa_pt*)
[46](#solidarity-supplement-for-the-elderly-bsaoa_pt)](#solidarity-supplement-for-the-elderly-bsaoa_pt)

[2.5.6. Social integration income (*bsa00_pt*)
[50](#social-integration-income-bsa00_pt)](#social-integration-income-bsa00_pt)

[2.5.7. Child benefit (*bch_pt*)
[52](#child-benefit-bch_pt)](#child-benefit-bch_pt)

[2.5.8. Prenatal family allowance (*bmapr_pt*)
[57](#prenatal-family-allowance-bmapr_pt)](#prenatal-family-allowance-bmapr_pt)

[2.5.9. Parental allowance (*bplct_pt*)
[59](#parental-allowance-bplct_pt)](#parental-allowance-bplct_pt)

[2.5.10. Parental social allowance (*bplnc_pt*)
[62](#parental-social-allowance-bplnc_pt)](#parental-social-allowance-bplnc_pt)

[2.5.11. Extraordinary Housing Support (*bhotn_pt*)
[64](#extraordinary-housing-support-bhotn_pt)](#extraordinary-housing-support-bhotn_pt)

[2.6. Social insurance contributions
[65](#social-insurance-contributions)](#social-insurance-contributions)

[2.6.1. Employee social contributions *(tscee_pt)*
[65](#employee-social-contributions-tscee_pt)](#employee-social-contributions-tscee_pt)

[2.6.2. Employer social contributions *(tscer_pt)*
[65](#employer-social-contributions-tscer_pt)](#employer-social-contributions-tscer_pt)

[2.6.3. Self-employed social contributions *(tscse_pt)*
[65](#self-employed-social-contributions-tscse_pt)](#self-employed-social-contributions-tscse_pt)

[2.7. Direct taxes [66](#direct-taxes)](#direct-taxes)

[2.7.1. Personal income tax (*tin00_pt*)
[66](#personal-income-tax-tin00_pt)](#personal-income-tax-tin00_pt)

[2.8. Consumption taxes [77](#consumption-taxes)](#consumption-taxes)

[2.8.1. VAT (il_tva) [77](#vat-il_tva)](#vat-il_tva)

[2.8.2. Excise Duties: Ad-valorem (il_txv) and Specific (il_txa)
[81](#excise-duties-ad-valorem-il_txv-and-specific-il_txa)](#excise-duties-ad-valorem-il_txv-and-specific-il_txa)

[2.9. Extraordinary measures
[85](#extraordinary-measures-1)](#extraordinary-measures-1)

[2.9.1. COST-OF-LIVING Crisis: Family income support (bfaxp_pt)
[85](#cost-of-living-crisis-family-income-support-bfaxp_pt)](#cost-of-living-crisis-family-income-support-bfaxp_pt)

[2.9.2. COST-OF-LIVING Crisis: Extraordinary supplement for vulnerable
families (*bfaxp01_pt*)
[86](#cost-of-living-crisis-extraordinary-supplement-for-vulnerable-families-bfaxp01_pt)](#cost-of-living-crisis-extraordinary-supplement-for-vulnerable-families-bfaxp01_pt)

[3. Data [88](#data)](#data)

[3.1. General description
[88](#general-description)](#general-description)

[3.2. Sample quality and weights
[88](#sample-quality-and-weights)](#sample-quality-and-weights)

[3.2.1. Weights [88](#weights)](#weights)

[3.3. Data adjustment [89](#data-adjustment)](#data-adjustment)

[3.4. Imputations and assumptions
[89](#imputations-and-assumptions)](#imputations-and-assumptions)

[3.4.1. Time period [89](#time-period)](#time-period)

[3.4.2. Gross incomes [90](#gross-incomes)](#gross-incomes)

[3.4.3. Disaggregation of harmonized variables and other imputations
[90](#disaggregation-of-harmonized-variables-and-other-imputations)](#disaggregation-of-harmonized-variables-and-other-imputations)

[3.5. Extended input data (with household expenditures for the
simulation of consumption taxes)
[91](#extended-input-data-with-household-expenditures-for-the-simulation-of-consumption-taxes)](#extended-input-data-with-household-expenditures-for-the-simulation-of-consumption-taxes)

[3.6. Uprating factors [92](#uprating-factors)](#uprating-factors)

[4. Validation [94](#validation)](#validation)

[4.1. Aggregate Validation
[94](#aggregate-validation)](#aggregate-validation)

[4.1.1. Components of disposable income
[94](#components-of-disposable-income)](#components-of-disposable-income)

[4.1.2. Validation of market incomes
[96](#validation-of-market-incomes)](#validation-of-market-incomes)

[4.1.3. Validation of taxes and social insurance contributions
[97](#validation-of-taxes-and-social-insurance-contributions)](#validation-of-taxes-and-social-insurance-contributions)

[4.1.4. Validation of benefits
[98](#validation-of-benefits)](#validation-of-benefits)

[4.1.5. Validation of outputted (simulated) expenses
[102](#validation-of-outputted-simulated-expenses)](#validation-of-outputted-simulated-expenses)

[4.2. Income distribution
[104](#income-distribution)](#income-distribution)

[4.2.1. Income inequality [105](#income-inequality)](#income-inequality)

[4.2.2. Poverty rates [105](#poverty-rates)](#poverty-rates)

[4.3. Health warnings [106](#health-warnings)](#health-warnings)

[References [109](#references)](#references)

[Sources for tax-benefit descriptions/rules
[109](#sources-for-tax-benefit-descriptionsrules)](#sources-for-tax-benefit-descriptionsrules)

[List of abbreviations and definitions
[110](#list-of-abbreviations-and-definitions)](#list-of-abbreviations-and-definitions)

[List of figures [113](#list-of-figures)](#list-of-figures)

[List of tables [114](#list-of-tables)](#list-of-tables)

[List of Annexes [117](#list-of-annexes)](#list-of-annexes)

[Annex 1. Uprating Factors
[117](#annex-1.-uprating-factors)](#annex-1.-uprating-factors)

[Annex 2. Policy Effects in 2024-2025
[123](#annex-2.-policy-effects-in-2024-2025)](#annex-2.-policy-effects-in-2024-2025)

[Annex 3. Validation Tables
[125](#annex-3.-validation-tables)](#annex-3.-validation-tables)

<span id="_Toc222328587" class="anchor"></span>Abstract

The EUROMOD Country Reports have the double function of describing the
scope of the EUROMOD simulations, including the underlying assumptions,
and providing the validation of these simulations against official
statistics. The Country Report for Portugal is prepared by the
Portuguese EUROMOD National Team each year and made available by the JRC
on time for the EUROMOD stable release of the model at the beginning of
each year.

<span id="_Toc222328588" class="anchor"></span>Acknowledgements

The work was carried out jointly by the EUROMOD core development team,
based at the JRC in Seville, and the Portuguese national team.

<span id="_Toc222328589" class="anchor"></span>Authors

The key contributors to this update were:

Carlos Farinha Rodrigues, Amílcar Moreira, Sara Riscado, Paulo Renato
Costa, Rui Nicola, David Leite Neves and Joana Andrade Vicente, as
members of the national team for Portugal

Silvia Navarro, as JRC developer responsible for Portugal

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
Portugal. It provides an overview of the Portuguese tax-benefit system
in 2022-2025 and of how these policies are implemented in EUROMOD. The
results presented are derived using EUROMOD version J2.0+, and they may
not match those obtained using earlier or later versions of the model.

The EUROMOD model and software, together with extensive information and
documentation, are available online:

EUROMOD homepage:
<https://euromod-web.jrc.ec.europa.eu/resources/documentation>

Downloads: <https://euromod-web.jrc.ec.europa.eu/download-euromod>

Documentation:
<https://euromod-web.jrc.ec.europa.eu/resources/documentation>

Glossary of EUROMOD terms:
<https://euromod-web.jrc.ec.europa.eu/resources/glossary>

## Basic information regarding the tax-benefit system 

The Portuguese tax-benefit system is a **single national system**.
However, the autonomous regions (Azores and Madeira) have lower income
tax rates.

**Fiscal year** matches the calendar year (*i.e.*, January 1st to
December 31st). Changes to the tax system generally take place in
January, whereas changes in benefits can occur throughout the year.

To compute the **income tax base**, the tax rate is applied to the half
of the aggregate income, and then the resulting tax liability is
multiplied by two to obtain couple’s total tax liability. Some income
components, like capital income, are taxed at source and may be left out
of the final tax calculations.

Taxpayers need to fill an **annual tax return**, since some differences
between the withholdings at source and the exact tax liability can
exist.

**Consumption taxes** consist of (1) VAT with three rates (standard,
intermediate and reduced), (2) harmonised excises on tobacco, petroleum
and energy products, alcohol, alcoholic beverages and beverages
containing added sugar or other sweetening matter, and (3) taxes on the
purchase and ownership of motor vehicles. Special rates apply in the
autonomous regions of Azores and Madeira. Although it applies on credit
to consumption, stamp duty (as it is mostly targeted on financial and
property transactions) is not treated as a consumption tax.

Since 2016, the **legal retirement age** started to vary according to
the evolution of life expectancy at the age of 65, during the 2nd and
3rd years prior to the date of the pension. It is given the option of
retiring later with a pension bonus to workers that are already in the
legal retirement age or have already exceeded it.

For tax purposes, **dependent children** are children with 18 years old
or less, or those under 25 years old that have a monthly income below
the national minimum wage.

For benefits and tax credit purposes, **single parents** are parents of
resident dependent children who are not cohabiting with a partner.

The **means-tested component** relies on different time scales to assess
income: entitlement to a means-tested benefit can depend on the income
of the previous year, the previous month or even the current income,
depending on the specific benefit.

Most benefits and pensions are indexed to the **Social Support Index**
(SSI), which is updated every year according to the real GDP growth and
CPI variation..

The policy parameters saved as constants in the model and their values
for the most recent year are available at
[<u>https://euromod-web.jrc.ec.europa.eu/resources/parameters</u>](https://euromod-web.jrc.ec.europa.eu/resources/parameters)

## Social benefits

**National minimum wage** **(‘*retribuição mínima mensal garantida’*):**
although not truly a social benefit, minimum wage guarantees, by law, a
minimum remuneration to full-time workers.

**Unemployment benefits (‘*subsídio de desemprego’*)**:
insurance/contributory unemployment benefit and
assistance/social/non-contributory unemployment benefit are the two main
policies that provide financial compensation to the unemployed. The
assistance benefit acts as an extension of the first one or as the only
benefit for shorter warranty periods (both modalities are means-tested
and restricted to participants in the employees’ social insurance
scheme). The insurance benefit is related to earnings. A new benefit for
long-term unemployed was implemented in 2016.

**Old age contributory pension (‘*pensão de velhice’*)**: pension to all
the elderly (people at and over the legal age of retirement) that
contributed to the compulsory social insurance scheme (both employees
and self-employed workers). The amount is a function of the average
monthly earnings adjusted over the person’s entire insurance life, up to
a maximum of 40 years.

**Minimum pension** **(‘*pensão mínima’*)**: new pensioners entitled to
an old age or disability pension who have contributed to the compulsory
social insurance scheme are entitled to a minimum pension, of different
amounts according to the career length. In the case of old age pensions,
this safety net is only provided for those who retire at the legal age
of retirement or later.

**Old age social pension (‘*pensão social de velhice’*)**:
non-contributory means-tested pension that provides a minimum pension to
low-income elderly individuals at the legal age of retirement.

**Survivors’ pension (‘*pensão de sobrevivência’*)**: granted to the
surviving spouse (with at least 35 years old) of a deceased insured
person, or to the divorced surviving spouse if the latter was receiving
alimony payments. It can also be granted to children until they have 18
years old (25 or 27 if they are studying – higher education) or, when
there are no surviving children or spouses, to the dependent parents.
There is also a non-earnings-related survivors’ pension (‘*pensão de
viuvez’* for widows and ‘*pensão de orfandade’* for orphans).

**Disability benefit/pension (‘*pensão de invalidez’*)**: any worker
under the legal retirement age who becomes unable to earn more than one
third of his standard wage due to illness or a work-related accident not
covered by health and safety legislation is entitled to this benefit.

**Social benefit for the inclusion (‘*prestação social para a
inclusão’*):** benefit created in October 2017 for disabled and
handicapped people. Replaced the non-earnings-related disability benefit
(for pensioners who were not able to fulfil the minimum career for the
main benefit) and ‘*subsídio mensal vitalício’* (another
handicapped/disability related benefit). Covers recipients with at least
a 60% of disability. Since October 2018, it includes a supplement
(means-tested) for poor handicapped people, and since 2019 includes a
bonus to support certain expenses.

**Sickness cash benefit (‘*subsídio de doença’*)**: available to all
insured employees as part of the compulsory social insurance scheme.
Benefits are earnings-related.

**Solidarity supplement for the elderly (‘*complemento solidário para
idosos’*)**: non-contributory means-tested benefit to help pensioners
who have reached the legal age of retirement and live on low incomes. It
considers a wide range of income sources which are not usually
considered in this kind of schemes, like the monetary income of the
recipients’ or residence at an old age care institution funded by the
Social Security.

**Social integration income (‘*rendimento social de inserção’*)**: cash
benefit granted together with an integration contract. Aims to ensure
that individuals and their family members have sufficient resources to
cover their basic needs, while promoting their gradual social and
professional integration.

**Child benefit (‘*abono de família para crianças e jovens’*)**: social
policy targeted to families with children and young people, as a
compensation for their expenditure on educating. Belongs to the same
group as funeral expenses allowances or special benefits paid to
disabled and dependent people, essentially children. Even though it is
means-tested, child benefit has a more universal nature than the other
policies that rely on income testing.

**Prenatal family allowance (‘*abono de família pré-natal’*):**
allowance assigned for 6 months to pregnant women starting from the 13th
week of gestation, to encourage motherhood by compensating the costs
increase during this period.

**Parental allowance (‘*subsídio parental’*)**: allowance paid to the
mother and/or father to replace the ‘lost’ work income during the period
of childbirth leave. Parents need to have a record of remunerations in
Social Security. This allowance comprises several modalities (which have
different concession periods): initial parental allowance, mother’s
initial parental allowance, parent’s original parental allowance, and
initial parental allowance of one parent in the event of the
impossibility of the other. The daily amount of the allowance is
calculated by applying a percentage to the value of the beneficiary’s
reference remuneration. It is available an extended parental allowance.

**Parental social allowance (‘*subsídio social parental’*)**: alongside
the parental allowance, this is the main policy that provides financial
compensation to the parents of a born child. This allowance is paid to
the parents who are not qualified for the parental allowance.

Besides the ones previously mentioned, there are other less important
benefits (or specific bonus or complements to the main benefits) in the
Portuguese Social Security system, which provide protection in areas
like disability, death, or social inclusion. Especially during 2022 and
2023, other temporary and extraordinary benefits were also introduced,
to compensate for the increase in prices and consequent cost of living.

**Extraordinary Housing Support (‘*Apoio Extraordinário à
Habitação’*)**: Introduced in 2023, the scheme provides a benefit of up
to €200, renewable for up to 5 years, aimed at tenants with effort rates
above 35%, with income up to the maximum limit of the sixth bracket of
personal income tax (IRS) and with contracts concluded up to March 15,
2023.

## Social contributions

**Employee and employer Social Security contributions (‘*contribuições
do trabalhador por conta de outrem e da entidade patronal’*)**:
contributions are shared between employees (23.75%) and employers (11%).
There are several different regimes reflecting specific occupations such
as non-profit organizations, rural workers, football players, clergy,
domestic services, young people in their first job, or disabled people.

**Self-employed Social Security contributions (‘*contribuições dos
trabalhadores independentes’*)**: since 2019, self-employed workers pay
a flat rate of 21.4% over the actual income.

**Civil servants’ contributions**: workers that entered the Civil
Service before 2006 belong to a separate Social Security scheme. From
January 1st of 2006, new civil servants (and their employer
institutions) contribute to the regular Social Security scheme and
follow the general regime rules.

## Taxes

**Personal income tax (‘*Imposto sobre o Rendimento das Pessoas
Singulares’, IRS*)**: paid by residents in Portugal and by non-residents
receiving income in Portugal. If the resident is part of a family unit
composed by spouse and dependents, the tax may be applied to all the
family members. Capital income is taxed at source (withholdings) and may
be left out of the final tax calculations, meaning that a different tax
rate can be applied. Property income may be left out of the final tax
calculations, meaning that a different tax rate can be applied. Labour
income is also taxed at source, but it is re-evaluated at the annual tax
calculations stage.

**Corporate income tax (‘*Imposto sobre o Rendimento das Pessoas
Coletivas’, IRC*):** paid by companies on their profits at a flat rate
of 20%. There is also a local government levy (‘*Derrama*’).

**Property transfer municipal tax (‘*Imposto Municipal sobre as
Transmissões Onerosas de Imóveis’, IMT*)**: local government tax on real
estate transactions.

**Property municipal tax (‘*Imposto Municipal sobre Imóveis’, IMI*)**:
local government tax on rural and urban properties. In 2017, a new
extension (*AIMI*) was created for highly valued real estates, which
provides funding for the Social Security Financial Stabilisation Fund.

**Value Added Tax (‘*Imposto sobre o Valor Acrescentado’, IVA*)**:
general rate of 23%, with intermediate (13%) and reduced (6%) rates
applying to specific goods. Lower rates apply to specific classes of
goods and in the autonomous regions of Azores and Madeira.

Special taxes on consumption include **alcohol duty/tax** (‘***Imposto
sobre o Álcool e as Bebidas Alcoólicas’, IABA***), **fuel duty/tax**
(‘***Imposto sobre Produtos Petrolíferos e Energéticos’, ISP***),
**tobacco duty/tax** (**‘*Imposto sobre o Tabaco’, IT***).

Taxes on vehicles include the sales tax on new cars (**‘*Imposto Sobre
Veículos’, ISV***) and the annual **vehicles tax** (‘***Imposto Único de
Circulação’, IUC***).

Besides the ones previously mentioned, there are other less important
taxes in the Portuguese tax system.

## Extraordinary measures

Following the COVID-19 pandemic, Portugal experienced a significant
increase in prices (see Moreira et al (2024). In 2022, and the
subsequent year, Portuguese authorities have introduced a number of
measures to deal with the impact of the Cost-Of-Living Crisis, namely:

**Family Income Support:** Introduced (in 2022) as part of the
‘*Families First*’ program, this scheme grants €125 per adult and €50
per child and young people, to residents with an income up to €2,700 per
month and who benefit from social benefits. Those receiving an
exceptional supplement for pensioners of less than €125 will receive the
difference.

**Extraordinary Supplement for Vulnerable Families**: Introduced in
2023, this scheme grants families that benefit from the social energy
tariff or minimum social benefits a €120 benefit, paid four times
throughout the year. For families receiving the Child Benefit, up to the
4th income bracket, this also includes an add on of €60, per child -
also paid quarterly.

**Supplement to Child Benefit**: Families with children and young people
up to the fourth income bracket of the child benefit also receive an
extraordinary supplement of €15 per month for each child, also paid on a
quarterly basis. Introduced in 2023.

**Extraordinary Housing Support:** Introduced in 2023, this scheme
provided extraordinary and temporary rental support and interest bonus
for families experiencing a high burden with housing costs. As part of
this scheme, families in rented accommodation, with a burden rate
exceeding 35% and income up to the maximum limit of the sixth PIT income
bracket, are entitled to a monthly benefit of up to €200. Families with
mortgages on their house, and that are subject to an effort rate of 50%
(or more, depending on the income bracket), are e entitled to a benefit
of up to €720.65 on the interest of their mortgage. The bonus covers the
difference between the present value of the indexer and the value of the
indexer at the start of the loan plus 3 p.p.. As the programme extends
for a period of up to 5 years, we decided to consider it as a permanent
feature of the Portuguese Tax-Benefit system (see Section 2.5.11)

# Simulation of taxes, social insurance contributions and benefits in EUROMOD

## Scope of simulation

<span id="_Toc222328520" class="anchor"></span>**Table 2.1** Simulation
of benefits in EUROMOD \[2022-2025\]

<table style="width:63%;">
<colgroup>
<col style="width: 13%" />
<col style="width: 7%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 21%" />
</colgroup>
<thead>
<tr>
<th><strong>Benefit</strong></th>
<th style="text-align: center;"><strong>Variable</strong></th>
<th style="text-align: center;"><strong>2022</strong></th>
<th style="text-align: center;"><strong>2023</strong></th>
<th style="text-align: center;"><strong>2024</strong></th>
<th style="text-align: center;"><strong>2025</strong></th>
<th style="text-align: center;"><strong>Comments</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Survivors’ pension</td>
<td style="text-align: center;">psu</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td>No data on the loss of family members. 2022 Extraordinary Pension
Supplement modelled.</td>
</tr>
<tr>
<td>Disability benefit</td>
<td style="text-align: center;">pdi</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td>No data on disability incidence. 2022 Extraordinary Pension
Supplement modelled.</td>
</tr>
<tr>
<td>Sickness cash benefit</td>
<td style="text-align: center;">bhl</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td>No data on sick leave incidence</td>
</tr>
<tr>
<td>Other family benefits</td>
<td style="text-align: center;">bfa</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td rowspan="4">Composed of several benefits impossible to split and
simulate.</td>
</tr>
<tr>
<td>Other social assistance benefits</td>
<td style="text-align: center;">bsaot</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
</tr>
<tr>
<td>Education benefit</td>
<td style="text-align: center;">bed</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
</tr>
<tr>
<td>Housing benefit</td>
<td style="text-align: center;">bho</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
</tr>
<tr>
<td>Child benefit</td>
<td style="text-align: center;">bch_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td></td>
</tr>
<tr>
<td>Prenatal family allowance</td>
<td style="text-align: center;">bmapr_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td rowspan="3">However, the simulation is switched off in the baseline,
i.e., non-simulated components (bfa) are used.</td>
</tr>
<tr>
<td>Parental allowance</td>
<td style="text-align: center;">bplct_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
</tr>
<tr>
<td>Parental social allowance</td>
<td style="text-align: center;">bplnc_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
</tr>
<tr>
<td>Old age contributory pension</td>
<td style="text-align: center;">poact_s</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td>No data on contributory career (years, number of contributions).
Simulation of the minimum pension only. 2022 and 2024 Extraordinary
Pension Supplement modelled.</td>
</tr>
<tr>
<td>Old age social pension</td>
<td style="text-align: center;">poanc_s</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td>No data on contributory career (years, number of contributions).
Split of the original microdata aggregated variable related to old age
pensions only. 2022 Extraordinary Pension Supplement modelled</td>
</tr>
<tr>
<td>Solidarity supplement for the elderly</td>
<td style="text-align: center;">bsaoa_s</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td>No data on the descendants of beneficiaries that do not live in the
same household. No data on residence in Social Security funded
institutions. Difficulty in dealing with non-take up issue.</td>
</tr>
<tr>
<td>Social integration income</td>
<td style="text-align: center;">bsa00_s</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td>Difficulty in matching the simulated family unit with the actual
one. Difficulty in dealing with non-take up issue.</td>
</tr>
<tr>
<td>Unemployment insurance</td>
<td style="text-align: center;">bunct_s</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td rowspan="2">No data on the reason for becoming unemployed. No data
on the contribution history of unemployed individuals, nor on the
previous earnings before unemployment. Split of the original aggregated
variable only. Benefit recipients are imputed using information of the
reported receipt of the respective benefit in SILC data (i.e.,
simulations are conditional on the report of the benefit receipt in the
microdata).</td>
</tr>
<tr>
<td>Unemployment assistance</td>
<td style="text-align: center;">bunnc_s</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
</tr>
<tr>
<td>Extraordinary Housing Support</td>
<td style="text-align: center;">bhotn_s</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td>The Mortgage Interest Bonus component cannot be modelled due to a
lack of data on several elements such as spread, contract date, and loan
maturity date.</td>
</tr>
</tbody>
</table>

Source: Own elaboration.

<span id="_Toc222328521" class="anchor"></span>**Table 2.2** Simulation
of Extraordinary benefits in EUROMOD \[2022-2025\] (Cont.)

| **Benefit** | **Variable** | **2022** | **2023** | **2024** | **2025** | **Comments** |
|----|:--:|:--:|:--:|:--:|----|----|
| COST-OF LIVING: Family income support | bfaxp_s | S | \- | \- | \- |  |
| COST-OF LIVING: Extraordinary supplement for vulnerable families | bfaxp01_s | \- | S | \- | \- |  |

Note: “**I**” *included* in the micro-data but not simulated; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated. “**E**” *excluded* from the model’s scope, as it is
neither included in the microdata nor simulated by EUROMOD; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated.

Source: Own elaboration.

<span id="_Toc222328522" class="anchor"></span>**Table 2.3** Simulation
of taxes and social insurance contributions in EUROMOD \[2022-2024\]

| **Benefit** | **Variable** | **2022** | **2023** | **2024** | **2025** | **Comments** |
|----|:--:|:--:|:--:|:--:|:--:|----|
| Personal income tax | tin_s | PS | PS | PS | PS | Influenced by individual choices. No data available on some of the tax allowances (particularly health, one of the most important). |
| Employee social insurance contribution | tscee_s | S | S | S | S | General rules assumed. |
| Employer social insurance contribution | tscer_s | S | S | S | S | General rules assumed. |
| Self-employed social insurance contribution | tscse_s | PS | PS | PS | PS | General rules assumed. Significantly influenced by individual choices. |
| Value added tax | \- | S | S | S | S | Calculations based on extended input files with consumption expenditures from HBS |
| Excise duties | \- | S | S | S | S | Calculations based on extended input files with consumption expenditures from HBS |
| Tax on the purchase of new vehicles (IMV) | \- | E | E | E | E | No data on purchases of new vehicles |
| Vehicle Circulation Tax (IUC) | \- | E | E | E | E | No data on characteristics of vehicle(s) owned by household. |
| Property transfers municipal tax | \- | E | E | E | E | No data on purchases of propery(ies) |
| Property municipal tax | \- | E | E | E | E | No data on wealth |

Note: “**I**” *included* in the micro-data but not simulated; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated. “**E**” *excluded* from the model’s scope, as it is
neither included in the microdata nor simulated by EUROMOD; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated.

Source: Own elaboration.

Not all the taxes and benefits mentioned in the previous section are
simulated in EUROMOD. Some are beyond its scope entirely and are neither
included in the EUROMOD database nor in its output income variables.
Others are not possible to simulate accurately with the available data.
They are included in the database and may be chosen as components of
output variables, but the rules governing them may not be changed by the
model. Table 2.1 to Table 2.3 classify each of the main tax-benefit
instruments (and some minor ones introduced above) into one of these
three groups and provide a brief explanation as to why the instrument is
not fully simulated if this is the case. In the following tables we
present information on EUROMOD using the most recent dataset of combined
EU-SILC and national SILC data. Information on earlier input datasets
for the Portuguese model can be found in earlier country reports.

## Main policy changes

<span id="_Toc222328523" class="anchor"></span>**Table 2.4** Main policy
changes \[2022-2025\] a, b, c

<table style="width:98%;">
<colgroup>
<col style="width: 11%" />
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 21%" />
</colgroup>
<thead>
<tr>
<th><strong>Policies</strong></th>
<th><strong>2022</strong></th>
<th><strong>2023</strong></th>
<th><strong>2024</strong></th>
<th><strong>2025</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Upgrading of Wages &amp; Benefits</strong></td>
<td><p>NMW: €705</p>
<p>SSI: €443.20</p></td>
<td><p>NMW: €760</p>
<p>SSI: € 480.43</p></td>
<td><p>NMW: €820</p>
<p>SSI: €509.26</p></td>
<td><p>NMW: €870</p>
<p>SSI: €522.50</p></td>
</tr>
<tr>
<td><strong>Social Security Benefits</strong></td>
<td>Ret. Age: 66 years and 7 months</td>
<td>Ret. Age: 66 years and 4 months</td>
<td></td>
<td>Ret. Age: 66 years and 7 months</td>
</tr>
<tr>
<td></td>
<td><p>Old Age, Survivors and Disability Pensions are upgraded, but not
in line with Updating Formula.</p>
<p>Extraordinary Pension Increase</p>
<p>Exceptional Supplement for Pensioners</p></td>
<td>Old Age, Survivors and Disability Pensions are upgraded, but not in
line with Updating Formula.</td>
<td>Old Age, Survivors and Disability Pensions are upgraded, in line
with Updating Formula.</td>
<td><p>Old Age, Survivors and Disability Pensions are upgraded, in line
with Updating Formula.</p>
<p>Exceptional Supplement for Pensioners</p></td>
</tr>
<tr>
<td></td>
<td>Child Benefit: Increase for children in 1<sup>st</sup> and
2<sup>nd</sup> income brackets</td>
<td>Child Benefit: Increase of Reference Amounts</td>
<td>Child Benefit: Increase of Reference Amounts</td>
<td>Child Benefit: Increase of Reference Amounts</td>
</tr>
<tr>
<td></td>
<td>Introduction of ‘Child Guarantee’</td>
<td>Child Guarantee: Reference amount upgraded to €100/month.</td>
<td>Child Guarantee: Reference amount upgraded to €122/month.</td>
<td>Child Guarantee: Reference amount upgraded to €124.56/month.</td>
</tr>
<tr>
<td></td>
<td></td>
<td>CSI: Annual reference amount upgraded to €5,858.63/year</td>
<td><p>CSI: Annual Reference amount upgraded to €6,608.00/year (€7,208,
July onwards).</p>
<p>CSI: Earnings from children no longer considered in
means-test</p></td>
<td>CSI: Annual reference amount upgraded to €7,568.00/year.</td>
</tr>
<tr>
<td></td>
<td></td>
<td>RSI: Reference amount upgraded to €209.11/month.</td>
<td>RSI: Reference amount upgraded to €237.25/month.</td>
<td>RSI: Reference amount upgraded to €242.23/month.</td>
</tr>
<tr>
<td><strong>Direct Taxes (PIT &amp; SIC)</strong></td>
<td><p>PIT: Two new income brackets</p>
<p>PIT: Reduction of marginal rate of the 3 and 5<sup>th</sup> income
brackets.</p>
<p>PIT: Increase in Tax Credits for families with dependent children</p>
<p>PIT: Partial exemption for young people.</p></td>
<td><p>PIT: Income brackets updated by 5.1%</p>
<p>PIT: Marginal rate of the 2nd income bracket reduced from 23% to
21%.</p>
<p>PIT: Expansion of partial exemption for young people.</p>
<p>PIT: Reduction of Work-Disincentives in ‘Minimum Existence’.</p></td>
<td><p>PIT: Income brackets updated by 3%</p>
<p>PIT: Reduction of marginal rates for the income brackets 1 to 6.</p>
<p>PIT: Expansion of partial exemption for young people.</p>
<p>PIT: Reduction of Work-Disincentives in ‘Minimum Existence’.</p></td>
<td><p>PIT: Income brackets updated by 4.6%.</p>
<p>PIT: Increase in tax allowance for incomes from work and
pensions.</p>
<p>PIT: Expansion of Partial Allowance for Young People to people up to
35, and overall increase in exemptions.</p>
<p>PIT: Increase in Housing Tax Credit, concerning expenditure with
rents.</p>
<p>PIT: Upgrade of PIT minimum income guarantee</p></td>
</tr>
<tr>
<td><strong>Consumption Taxes</strong></td>
<td><p>VAT: Extension of Reduced Rate to: electricity consumption (first
100 kWh of monthly consumption), and products for people with
disabilities.</p>
<p>VAT: COVID-19 related exemptions</p></td>
<td>VAT: Reduced Rate to electricity consumption (first 100 kWh of
monthly consumption) extended.</td>
<td>VAT: Reduced Rate to electricity consumption (first 100 kWh of
monthly consumption) extended.</td>
<td><p>VAT: VAT rate applied to baby and children food is reduced to 6%,
and to 5% and 4% in Madeira and Azores, respectively.</p>
<p>ISP: Increase of rate on gasoline and diesel.</p>
<p>ISP: Decrease in Carbon Tax to 67,395 euros/ton of
CO<sub>2.</sub> </p></td>
</tr>
<tr>
<td><strong>Extraordinary Measures</strong></td>
<td><p>COVID-19: Termination of key measures.</p>
<p>COST-OF-LIVING: ‘Families First’</p></td>
<td><p>COST-OF-LIVING: Extraordinary €15 Supplement per child.</p>
<p>COST-OF-LIVING: Extraordinary supplement for vulnerable families</p>
<p>COST-OF-LIVING: Extraordinary Housing Support</p></td>
<td>COST-OF-LIVING: Extraordinary Housing Support extended and
upgraded</td>
<td></td>
</tr>
</tbody>
</table>

Note: <sup>a</sup> This table only mentions measures that are modelled
in EUROMOD. <sup>a</sup> Measures that reflect the influence of
automatic indexation mechanisms are not included. c Measures are
identified by the date they come into force, not the date they have been
approved.

### In 2022

**National minimum wage:** NMW updated to €705.

**Social Support Index:** SSI updated to €443.20.

**Pensions:**

Change in the legal retirement age to 66 years and 7 months.

**Contributory pensions:**

Increase in the amounts of the minimum pension.

Change in the remaining minimum amounts (regular annual update in
pensions): pensions ≤ 2 x SSI are updated by 1.0%; pensions \> 2 x SSI
and ≤ 6 x SSI are updated by 0.49%; and pensions \> 6 x SSI and ≤ 12 x
SSI are updated by 0.24%.

Extraordinary update in pensions: in January, sixth extraordinary
increase for pensions earned by people who have a total pension income
up to 2.5 x SSI up to €10. The amount of the increase equals the
difference between €10 and the amount received as part of the regular
update of pensions.

Exceptional supplement for pensioners: disability, old age and survival
pensioners (with pensions \<= 12 x SSI) are entitled, in October 2022,
to an additional amount of pensions. The value corresponds to 50% of the
total amount earned in October 2022.

**Old age social pension:** change in the base amount to €213.91 and in
the extraordinary solidarity supplement to €18.62 and €37.23 (depending
on age).

**Child benefit:**

Update in the amounts of the 1st and 2nd income brackets for children in
the age brackets above 36 months.

Complement for lower income families: new supplement (‘*Child*
*Guarantee’*) that guarantees the payment of a total amount of €70
(including the child benefit amount) for children under the age of 18,
recipients of the child benefit and belonging to households that are in
extreme poverty.

**Personal Income Tax:**

Income brackets were segmented (and limits updated), creating two
additional intermediate ones.

Tax credits regarding taxpayers and their dependent children: families
with two or more children between 3 and 6 years old will have a tax
credit increase from €600 to €750, starting from the second child and
regardless of the age of the first child. Each child older than 3 years
old continues to enable an automatic tax credit of €600 (and of €726 if
the child is under 3 years old); and for families with two or more
children aged up to 3 years old, the tax credit is €900 for the second
and subsequent children, regardless of the age of the first child.

Partial exemption for young people: young people between 18 and 26 years
old (or 30 years old, if completed a PhD programme), who earn dependent
or independent income (previously it did not include self-employed),
will benefit from a partial exemption of PIT in the first five years of
work (previously was three), according to the following amounts per year
of work:

1st and 2nd years: 30% with a limit of 7.5 x SSI,

3rd and 4th year: 20% with a limit of 5 x SSI,

5th year: 10% with a limit of 2.5 x SSI.

**Consumption Taxes:**

VAT: The VAT reduced rate is extended to the purchase (and repair) of
products targeted at people with disabilities and chronic diseases;

VAT: Exemption for all purchases related to delivery of COVID-19
vaccines and tests;

VAT: As part of response to the COVID-19 crisis the government
introduced the IVAucher Scheme allows the final consumer to accumulate
the value corresponding to the total VAT incurred on consumption in the
accommodation, culture and catering sectors, during a quarter, and use
this value, during the following quarter, on consumption in these same
sectors.

VAT: As part of response to the Cost-of-Living Crisis the VAT
intermediate rate is extended to the electricity for consumptions
(excluding its fixed components) of up to 100 kWh per period of 30 days,
or 150 kWh for families of five or more people; in households with
contracted power up to 6.90 kVA. This scheme entered in force in October
2021;

**COVID-19 temporary measures:** the main measures to support the
COVID-19 effects ceased in the first quarter of 2022.

**COST-OF-LIVING - Family income support:** extraordinary support of
€125 per adult and €50 per child and young people, to compensate for the
increase in prices. The ‘*Families First*’ program assigns this support
to residents with an income up to €2,700 per month and who benefit from
social benefits. Those receiving an exceptional supplement for
pensioners of less than €125 will receive the difference.

### In 2023

**National minimum wage:** NMW updated to €760.

**Civil servants’ wages**: the following update by bands of the civil
servants salaries was applied:

The base remuneration increased to €761.58;

All wages between €709.48 and €2,612.03 increased €52.11;

Wages above €2,612.03 increased 2%.

Additionally, all civil servants in Portugal received an additional 1%
salary increase.

**Social Support Index:** SSI updated to €480.43.

**Pensions:** change in the legal retirement age to 66 years and 4
months.

**Contributory pensions:**

Increase in the amounts of the minimum pension.

Change in the remaining minimum amounts (regular annual update in
pensions). From January to June, pensions are updated (respecting to
December 2022) by 4.83% for pensions ≤ 2 x SSI; 4.49% for pensions \> 2
x SSI and ≤ 6 x SSI; and 3.89% for pensions \> 6 x SSI and ≤ 12 x SSI.

From July to December, pensions are updated (respecting to December
2022) by 8.4% for pensions ≤ 2 x SSI; 8.06% for pensions \> 2 x SSI and
≤ 6 x SSI; and 7.46% for pensions \> 6 x SSI and ≤ 12 x SSI

**Old age social pension:** change in the base amount to €224.24 and in
the extraordinary solidarity supplement to €19.53 and €39.03 (depending
on age).

**Solidarity supplement for the elderly**: increase in the reference
value to €5,858.63/year.

**Social integration income:** increase in the reference amount to
€209.11.

**Child benefit:**

Update of the amounts (including the complement for lower income
families, the supplement for large families and the bonus for lone
parent families).

Extraordinary support: to mitigate the effects of inflation, in 2023
there is an extraordinary support of €15 per month for each child
receiving the child benefit (for all income brackets).

Complement for lower income families: the ‘*Child* *Guarantee’*
supplement now intends to guarantee the payment of a total amount of
€100 (including the child benefit amount) for children under the age of
18, recipients of the child benefit and belonging to households that are
in extreme poverty.

**Personal income tax:**

Income brackets limits are updated by 5.1% and the applicable marginal
rate of the 2nd income bracket is reduced from 23% to 21%.

Tax credits regarding taxpayers and their dependent children: for
families with two or more children, the tax credit is €900 for the
second and subsequent children now aged up to 6 years old (previously it
was 3 years old), regardless of the age of the first child.

Partial exemption for young people reinforced according to the following
amounts per year of work (with upper limits again):

1st year: 50%, with a limit of 12.5 x SSI.

2nd year: 40%, with a limit of 10 x SSI.

3rd and 4th year: 30%, with a limit of 7.5 x SSI.

5th year: 20%, with a limit of 5 x SSI.

Structural changes to the net income guarantee (“mínimo de existência”).

Earnings from the rental of property are taxed at 25% (part of the
‘+Housing’ package)

**COST-OF-LIVING - Extraordinary supplement for vulnerable families:**
extraordinary support for the most vulnerable families of €30 per month
per household, paid three times along the year, to compensate for the
increase in prices. The definition of vulnerable families is of those
that benefit from the social energy tariff or minimum social benefits.
In addition, families with children and young people up to the fourth
income bracket of the child benefit also receive an extraordinary
supplement of €15 per month for each child, also paid on a quarterly
basis.

**COST-OF-LIVING - Housing benefit:** extraordinary and temporary rental
support and interest bonus for families in the context of housing.

The rental support is aimed at tenants with a burden rate exceeding 35%
and income up to the maximum limit of the sixth PIT income bracket. The
support translates to a monthly amount up to €200 (and corresponds to
the difference between the value of the rent and the amount that would
be paid if the effort rate was 35 % of the average monthly value of
income).

As for the interest bonus, the support translates to a yearly bonus up
to €720.65. The bonus shall cover the difference between the present
value of the indexer and the value of the indexer at the start of the
loan plus 3 p.p., in the case of an effort rate of 50% (or more,
depending on the income bracket). It cannot be implemented in EUROMOD
due to a lack of data on several elements such as spread, contract date,
and loan maturity date.

### In 2024

In this section, we identify the policy measures that have come in force
in 2024, until the 31st of October. Changes to the Portuguese
tax-benefit system, are structured as follows:

Upgrading of Wages;

Changes to Pension Benefits;

Changes to Other Social Security Benefits;

Changes to Direct Taxes;

Changes to Consumption Taxes.

Tables 2-5 to 2.10 identify the key changes made, the supporting
legislation (where applicable), and whether those changes are simulated
in the model (or not).

#### Upgrading of Wages 

The Portuguese government approved a set of wage increases well above
the projected inflation for 2024 (3.3%) (Ministério das Finanças, 2024:
37) - see Table 2-5. Thus, the **National Minimum Wage (NMW)** for
private sector workers was increased by 7.9%, to €820.

In the same way, the **Base Remuneration for Public Sector Workers** was
increased by 6.8%, to €821,83. This was not the case, however, for
public sector workers with wages over €1754,49 - which were only
increased by 3%. Public sector wages between €821,83 and €1754,49 were
increased by €52.63.

<span id="_Toc222328524" class="anchor"></span>**Table 2.5** Changes to
National Minimum Wage and Public Sector Wages \[2024\]

<table style="width:65%;">
<colgroup>
<col style="width: 10%" />
<col style="width: 26%" />
<col style="width: 9%" />
<col style="width: 19%" />
</colgroup>
<thead>
<tr>
<th><strong>Policy</strong></th>
<th><p><strong>Measure</strong></p>
<p><strong>(<em>Legal Basis</em>)</strong></p></th>
<th style="text-align: center;"><strong>Impact on EUROMOD</strong></th>
<th style="text-align: center;"><strong>Comments</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>National Minimum Wage (Private Sector)</strong></td>
<td><p>NMW updated to €820</p>
<p><em>Decree-Law 107/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Public Sector Wages</strong></td>
<td><p>Updating of Public Sector workers’ wages:</p>
<ul>
<li><p>The Base Remuneration is increased to €821,83;</p></li>
<li><p>Wages between €821,83 and €1754,49 are increased by
€52.63;</p></li>
<li><p>Wages over € 1754,49 are increased by 3%.</p></li>
</ul>
<p><em>Decree-Law 108/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Source: Decreto-Lei n.º 107/2023, de 11 de novembro (Private Sector
NMW); Decreto-Lei n.º 108/2023, de 12 de novembro (Public Sector wages)
— Diário da República, www.dre.pt

#### Changes to Pension Benefits 

In 2024, there were some significant changes made to pension benefits
(see Table 2-6):

1.  Portuguese authorities have resumed the use of the ‘Pension
    Upgrading Formula’ to update the value of **Old Age, Survivors and
    Disability Pensions** (see Table 2-6)**.** As result of this, a
    significant share of pensioners received increases above the
    projected rate of inflation for 2024. Pensioners with pensions over
    €1085,52, received smaller increases, between 5% and 5.65% - but
    still above the projected rate of inflation for 2024.

2.  The **Minimum Pension** reference amounts were increased by 9.6%
    (see Table 2-20, Section 2.5.3);

3.  The **Old Age Social Pension** was also increased by 9.6%, to
    €245.79. The **Extraordinary Solidarity Supplement** (CES) was also
    upgraded to €21.39, for those aged 65 to 69, and to €42.78, for
    those aged 70 or over (see Table 2-22, Section 2.5.4).

<span id="_Toc222328525" class="anchor"></span>**Table 2.6** Changes to
Pension Benefits \[2024\]

<table style="width:65%;">
<colgroup>
<col style="width: 10%" />
<col style="width: 26%" />
<col style="width: 9%" />
<col style="width: 19%" />
</colgroup>
<thead>
<tr>
<th><strong>Policy</strong></th>
<th><p><strong>Measure</strong></p>
<p><strong>(<em>Legal Basis</em>)</strong></p></th>
<th style="text-align: center;"><strong>Impact on EUROMOD</strong></th>
<th style="text-align: center;"><strong>Comments</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Legal Age of Retirement</strong></td>
<td><p>66 years and 4 months (no change)</p>
<p><em>Order 292/2022</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Pension Update Formula</strong></td>
<td><p>Updating of Old Age, Survivors and Incapacity Pensions:</p>
<ul>
<li><p>Up to €301,41 updated by 6%;</p></li>
<li><p>Between €301,41 and €1018,52: updated by 6%, subject to a minimum
increase of €18.08;</p></li>
<li><p>Between €1018,52 and €3055,56: updated by 5.65%, subject to a
minimum increase of €61,11;</p></li>
<li><p>Pensions over €3055,56 : updated by 5%, subject to a minimum
increase of €172,64.</p></li>
</ul>
<p>Pensions equal or above to 12xSSI, subject to exceptions, do not
receive any increase.</p>
<p><em>Order 424/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Minimum Pensions</strong></td>
<td><p>Increased by 9.6%</p>
<p><em>Order 424/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Social Old Age Pension</strong></td>
<td><p>Increased by 9.6%, to €245.79. The Extraordinary Solidarity
Supplement (CES) was also upgraded</p>
<p><em>Order 424/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Note: “**I**” *included* in the micro-data but not simulated; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated. “**E**” *excluded* from the model’s scope, as it is
neither included in the microdata nor simulated by EUROMOD; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated.

Source: Despacho n.º 424/2023 (pension valorisation); Order 424/2023 —
Diário da República, www.dre.pt

In contrast with previous years, there was no change to the Legal Age of
Retirement, which remained at 66 years and 4 months (see Table 2-6).

#### Changes Other Social Security Benefits

In this section, we cover:

Changes to the indexation mechanism (SSI) that secures the regular
uprating of Social Security benefits;

Changes to non-means-tested benefits;

Changes to means-tested benefits.

As can be seen in Table 2-7, the **Social Support Index**, which is used
as a reference to determine the eligibility and generosity of Social
Security benefits (and certain aspects of the Personal Income Tax) was
upgraded above the projected rate of inflation for 2024 (6%), to €509.26
– still, below the national minimum wage increase (see Table 2-5).

<span id="_Toc222328526" class="anchor"></span>**Table 2.7** Indexation
of Social Security Benefits \[2024\]

<table style="width:65%;">
<colgroup>
<col style="width: 10%" />
<col style="width: 26%" />
<col style="width: 9%" />
<col style="width: 19%" />
</colgroup>
<thead>
<tr>
<th><strong>Policy</strong></th>
<th><p><strong>Measure</strong></p>
<p><strong>(<em>Legal Basis</em>)</strong></p></th>
<th style="text-align: center;"><strong>Impact on EUROMOD</strong></th>
<th style="text-align: center;"><strong>Comments</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Social Support Index</strong></td>
<td><p>Social Support Index updated to €509.26</p>
<p><em>Order 13288-E/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Note: “**I**” *included* in the micro-data but not simulated; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated. “**E**” *excluded* from the model’s scope, as it is
neither included in the microdata nor simulated by EUROMOD; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated.

*Source: Portaria n.º 13288-E/2023 (SSI update) — Diário da República,
www.dre.pt*

The changes introduced, during 2024, to non means-tested benefits are
relatively minor and refer mostly to by products of the increase in the
SSI (see Sections 2.5.1 and 2.5.2). By contrast, we identify a number of
substantive changes to a number of means-tested Social Security benefits
in 2024 (see Table 2-9):

The value of Child Benefits was significantly upgraded.

Taking the case of a child aged under 36 months, in the first income
bracket, the Child Benefit was increased by 14%. Part of this increase
involved the incorporation of the Extraordinary Support for Children - a
temporary benefit worth (€15 per child) introduced in 2023 to compensate
families for the increase in the cost of living – into the value of the
Child Benefit (see Table 2-33, Section 2.5.7);

The **Child Benefit’s Supplement for Lone Parent Families**, for
families in the 2nd to 4th income brackets was increased from 42.5% to
50% (Section 2.5.7);

The **Child Guarantee** reference value has also been increased from
€100 to €122, per month. However, when one considers the increases in
the Child Benefit, this means the actual value of the Child Guarantee
(differential) benefit has not increased (see Table 2-38, Section
2.5.7);

Reflecting (an increasing) cross-party consensus about the need to
improve the effectiveness of the **Solidarity Supplement for the
Elderly** (**CSI)** in fighting elderly poverty, this benefit was
increased – not once, but twice. As part of the 2024 Budget Law, the
annual reference amount was increased by 12.8%, to €6,608. Then, from
the 1st of June 2024, the CSI annual reference amount was increased
(again) by (approximately) 9.1% - to €7,208 (see Table 2-23, Section
2.5.5);

In what can be seen as an effort to expand the eligibility to **CSI**,
earnings from applicants’ children/descendants are no longer considered
in the means-test that determines the eligibility to the scheme (see
Section 2.5.5);

The **Extraordinary Housing Support** scheme, introduced in 2023 as part
of the response to the Cost-of-Living crisis, was extended to 2024 and
the value of the payment was increased by 4.6% (see Section 2.5.11).

<span id="_Toc222328527" class="anchor"></span>**Table 2.8** Changes to
Non-Means Tested Social Security Benefits \[2024\]

<table style="width:65%;">
<colgroup>
<col style="width: 10%" />
<col style="width: 26%" />
<col style="width: 9%" />
<col style="width: 19%" />
</colgroup>
<thead>
<tr>
<th><strong>Policy</strong></th>
<th><p><strong>Measure</strong></p>
<p><strong>(<em>Legal Basis</em>)</strong></p></th>
<th style="text-align: center;"><strong>Impact on EUROMOD</strong></th>
<th style="text-align: center;"><strong>Comments</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Child Benefit</strong></td>
<td><p>Updating of Reference Amounts</p>
<p><em>Order 422/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Supplement for Lone Parent Families for families in the 2nd to
4th income brackets was increased from 42.5% to 50%</p>
<p><em>Order 422/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Child Guarantee (Annual) Reference Amount increased to €1464
(€122, per month)</p>
<p><em>Order 422/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td>Updating of Supplement for Families with 2 or More Children, by
reference to Child Benefit Amounts</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Prenatal Family Allowance</strong></td>
<td><p>Updating Income Brackets, in line with Child Benefit</p>
<p><em>Order 422/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Updating of Reference Amounts, in line with Child Benefit</p>
<p><em>Order 422/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Parental Social Allowance</strong></td>
<td><p>Updating Income Brackets, in line with Child Benefit</p>
<p><em>Order 422/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Solidarity Supplement for the Elderly (CSI)</strong></td>
<td><p>Annual Reference Amount updated to €6,608.00.</p>
<p><em>Order 419/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Annual Reference Amount updated to €7,208.</p>
<p><em>Order 154-A/2024</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Earnings from children are no longer considered in the CSI
means-test.</p>
<p><em>Order 154-A/2024</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Social Integration Income (RSI)</strong></td>
<td><p>RSI Monthly Reference Amount updated to €237.25 month</p>
<p><em>Order 420/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Extraordinary Housing Support</strong></td>
<td><p>The scheme is extended to 2024. Payment is increased by 4.96%</p>
<p><em>Law 82/2023,</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Note: “**I**” *included* in the micro-data but not simulated; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated. “**E**” *excluded* from the model’s scope, as it is
neither included in the microdata nor simulated by EUROMOD; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated.

*Source: Lei n.º 82/2023, de 29 de dezembro (OE 2024); Portaria n.º
154-A/2024; Portaria n.º 420/2023 — Diário da República, www.dre.pt*

#### Changes to Direct Taxes (SSC & PIT)

In 2024, there were no significant changes to **Social Security
Contributions** (SSC) (see Section 2.6). The only changes are the
product of automatic indexation mechanisms in the tax-benefit system. In
contrast, several substantive changes to the **Personal Income Tax**
were introduced (see Table 2-9):

**PIT** income brackets were upgraded by 3%, very much in line with the
projected inflation for 2024 (see Table 2-49, Section 2.7.1);

**PIT** marginal tax rates for individuals/households in the first five
income brackets were reduced by (see Table 2-49, Section 2.7.1):

\- 1.25 percentage points in the 1st income bracket;

\- 3.0 percentage points in the 2nd income bracket;

\- 3.50 percentage points in the 3rd income bracket;

\- 2.50 percentage points in the 4th income bracket

\- 2.25 percentage points in the 5th income bracket.

Tax allowance for income from work increased to €4350.25, and to be
updated annually, in line with SSI (see Table 2-47, Section 2.7.1);

Tax allowance for income from pensions increased to €4350.25, and to be
updated annually, in line with SSI (see Table 2-47, Section 2.7.1);

The partial **PIT** tax allowance for young persons between 18 and 25
was also significantly expanded both in terms of the level of the
exemption, both in terms of the limits on the amount covered by those
exemptions (see Table 2-48, Section 2.7.1);

The **PIT** **Housing Tax Credit, concerning expenses with rents** was
increased (see Table 2-54, Section 2.7.1):

1)  To €900, for individuals with incomes in the first income bracket;

2)  To a varying degree, for individuals with incomes equal or above 1st
    Income Bracket of PIT and under €30,000.

3)  To €600, for individuals with incomes above €30,000;

    In line with the increase in the value of the National Minimum Wage,
    the reference amount of the **PIT** Net Income Guarantee reference
    value was also significantly increased to €11,480 (14\*NMW) (see
    Table 2-48, Section 2.7.1);

    In line with transition rules set in 2023 State Budget, the rules
    for determining application of the **PIT** Net Income Guarantee were
    also altered, (see Table 2-52, Section 2.7.1).\
    **Table 2.9** Changes to Personal Income Tax \[2024, Continent\]

<table style="width:65%;">
<colgroup>
<col style="width: 10%" />
<col style="width: 30%" />
<col style="width: 9%" />
<col style="width: 15%" />
</colgroup>
<thead>
<tr>
<th><strong>Policy</strong></th>
<th><p><strong>Measure</strong></p>
<p><strong>(<em>Legal Basis</em>)</strong></p></th>
<th style="text-align: center;"><strong>Impact on EUROMOD</strong></th>
<th style="text-align: center;"><strong>Comments</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>PIT: Income Brackets</strong></td>
<td><p>PIT Income Brackets were increased by 3%</p>
<p><em>Law 82/2023, Article 230º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>PIT: Rates</strong></td>
<td><p>Reduction in marginal rates of the first 5 Income brackets:</p>
<ul>
<li><p>- 1.25 p.p in the 1<sup>st</sup> income bracket;</p></li>
<li><p>- 3.0 p.p in the 2<sup>nd</sup> income bracket;</p></li>
<li><p>- 3.50 p.p in the 3<sup>rd</sup> income bracket;</p></li>
<li><p>- 2.50 p.p in the 4<sup>th</sup> income bracket;</p></li>
<li><p>- 2.25 p.p in the 5<sup>th</sup> income bracket.</p></li>
</ul>
<p><em>Law 82/2023, Article 230º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>PIT: Tax Allowances</strong></td>
<td><p>Increase in tax exemptions for people aged between 18 and 26:</p>
<ul>
<li><p>1st year: 100%, with a limit of 40 x SSI.</p></li>
<li><p>2nd year: 75%, with a limit of 30 x SSI.</p></li>
<li><p>3rd and 4th year: 50%, with a limit of 20x SSI.</p></li>
<li><p>5th year: 25%, with a limit of 10 x SSI.</p></li>
</ul>
<p><em>Law 82/2023, Article 230º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Tax allowance for income from work to €4350.25and from now to be
updated annually, in line with SSI</p>
<p><em>Law 32/2024, Article 2º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Tax allowance for income from pensions to €4350.25and from now to
be updated annually, in line with SSI</p>
<p><em>Law 32/2024, Article 2º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>PIT: Tax Credits</strong></td>
<td><p>The upper limit of the Housing Tax Credit, concerning rent
expenses, for individuals in the 1st Income Bracket of PIT, is raised to
€600 (from €502);</p>
<p><em>Law 82/2023, Article 230º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>The formula for computing the upper limit of the Housing Tax
Credit, concerning rent expenses, for individuals with incomes equal or
above 1st Income Bracket of PIT and under €30,000, now varies between
€600 and €900 (previously between €502 and €800),</p>
<p><em>Law 82/2023, Article 230º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>The upper limit of the Housing Tax Credit, concerning rent
expenses, for individuals with income above €30,000 is raised to €600
(from €502);</p>
<p><em>Law 82/2023, Article 230º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>PIT: Minimum Income Guarantee</strong></td>
<td><p>The (Annual) Reference Value of the Minimum Income Guarantee was
increased to the highest value between €11,480 (i.e., 14* NMW), and 1,5
x 14 x IAS,</p>
<p><em>Law 82/2023, Article 230º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Changes to Minimum Income Guarantee in the computation of the
Income Limit (L) Formula: Reference Value of the Minimum Income
Guarantee – General Deductions Limit / (1st bracket Rate*3.60) + 1st
bracket Limit/3.60</p>
<p><em>Law 82/2023, Article 230º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;"><del>-</del></td>
</tr>
<tr>
<td></td>
<td><p>Changes to Minimum Income Guarantee formula for income between
the Reference Value and the Income Limit (L): Reference Value –
2.6*(Income – Reference Value) - (Tax Allowances +General Deductions
Limit/ 1st bracket Rate)</p>
<ul>
<li><p><em>Law 82/2023, Article 230º</em></p></li>
</ul></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;"><del>-</del></td>
</tr>
<tr>
<td></td>
<td><p>Changes to Minimum Income Guarantee formula for income above the
Income Limit (L): L - 1st bracket Limit – 1.35*(Income – L) – Tax
Allowances</p>
<ul>
<li><p><em>Law 34/2024, Article 2º</em></p></li>
</ul></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;"><del>-</del></td>
</tr>
</tbody>
</table>

Source: Lei n.º 82/2023, de 29 de dezembro (OE 2024), art. 230.º; Lei
n.º 34/2024, art. 2.º — Autoridade Tributária e Aduaneira,
www.portaldasfinancas.gov.pt

<span id="_Toc222328528" class="anchor"></span>**Table 2.10** Changes to
Personal Income Tax \[2024, Azores & Madeira\]

<table style="width:65%;">
<colgroup>
<col style="width: 10%" />
<col style="width: 31%" />
<col style="width: 9%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th><strong>Policy</strong></th>
<th><p><strong>Measure</strong></p>
<p><strong>(Legal Basis)</strong></p></th>
<th style="text-align: center;"><strong>Impact on EUROMOD</strong></th>
<th style="text-align: center;"><strong>Comments</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Personal Income tax</strong></td>
<td><p>Azores: Updating Income Brackets, by 3%</p>
<p><em>Law 82/2023, Article 230º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Azores: Reduction in marginal rates of the first 5 Income
brackets:</p>
<ul>
<li><p>- 0.875 p.p in the 1st income bracket;</p></li>
<li><p>- 2.1 p.p in the 2nd income bracket;</p></li>
<li><p>- 2.45 p.p in the 3rd income bracket;</p></li>
<li><p>- 1.75 p.p in the 4th income bracket;</p></li>
<li><p>- 6.83 p.p in the 5th income bracket.</p></li>
</ul>
<p><em>Law 82/2023, Article 230º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Madeira: Updating Income Brackets, by 3%</p>
<p><em>Regional Decree-Law 7/2024/M, Article 2º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td></td>
<td><p>Madeira: Reduction in marginal rates of the first 5 Income
brackets:</p>
<ul>
<li><p>- 1.05 p.p in the 1st income bracket;</p></li>
<li><p>- 3.2 p.p in the 2nd income bracket;</p></li>
<li><p>- 3.15 p.p in the 3rd income bracket;</p></li>
<li><p>- 2.45 p.p in the 4th income bracket;</p></li>
<li><p>- 1.36 p.p in the 5th income bracket.</p></li>
</ul>
<p><em>Regional Decree-Law 7/2024/M, Article 2º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Source: Decreto Legislativo Regional n.º 7/2024/M, art. 2.º (Madeira) —
Diário da República, www.dre.pt

Changes were also introduced in Personal Income Tax in the Autonomous
Region of Azores:

**PIT** income brackets were upgraded by 3%, very much in line with the
projected inflation for 2024 (see Table 2-51, Section 2.7.1);

**PIT** marginal tax rates for individuals/households in the first five
income brackets were reduced by (see Table 2-51, Section 2.7.1):

\- 0.875 percentage points in the 1st income bracket;

\- 2.1 percentage points in the 2nd income bracket;

\- 2.45 percentage points in the 3rd income bracket;

\- 1.75 percentage points in the 4th income bracket;

\- 6.83 percentage points in the 5th income bracket.

Changes were also introduced in Personal Income Tax in the Autonomous
Region of Madeira:

**PIT** income brackets were upgraded by 3%, very much in line with the
projected inflation for 2024 (see Table 2-51, Section 2.7.1);

**PIT** marginal tax rates for individuals/households in the first five
income brackets were reduced by (see Table 2-51, Section 2.7.1):

\- 1.05 percentage points in the 1st income bracket;

\- 3.2 percentage points in the 2nd income bracket;

\- 3.15 percentage points in the 3rd income bracket;

\- 2.45 percentage points in the 4th income bracket;

\- 1.36 percentage points in the 5th income bracket.

#### Changes to Consumption Taxes

There were also some changes to **Consumption Taxes,** namely**:**

The **VAT** intermediate rate is extended to the following products (see
Table 2-57, Section 2.8.1):

Edible vegetable oils;

‘Alheiras’ (bread sausages);

Juices, nectars and carbonated waters or added with carbon dioxide or
other substances, provided they are purchase in a context specific to
the provision of food and beverage services;

The **VAT** reduced rate is extended to the All purchases related with
the production of renewable energy (see Table 2-57, Section 2.8.1);

The **VAT** Exemption on tutoring services now applies whether the
lessons are taught only personally or in a group (see Table 2-57,
Section 2.8.1).

###  In 2025

In this section, we identify the policy measures that have come in force
in 2025. For the sake of consistency (see Chapter 4), changes to the
Portuguese tax-benefit system, are structured as follows:

Upgrading of Wages;

Changes to Pension Benefits

Changes to Other Social Security Benefits

Changes to Direct Taxes

Changes to Consumption Taxes

Tables 2-5 to 2.13 identify the key changes made, the supporting
legislation (where applicable), and whether those changes are simulated
in the model (or not). Changes that result from indexation (e.g.,
changes in the income brackets thresholds that are indexed to the SSI)
are not reported here.

#### Upgrading of Wages 

The Portuguese government approved a set of wage increases well above
the projected inflation for 2025, 2.3% (Ministério das Finanças, 2025:
6, 10). The **National Minimum Wage (NMW)** for private sector workers
was increased by 6.1%, to €870 (see Table 2-11).

The **Base Remuneration for Public Sector Workers** was increased by 6.9
%, to €878.41 (see Table 2-11). Public sector wages between €878.42 and
€2,631.62 were increased by €56.58, while public sector workers with
wages equal or over €2,631.63 were increased by 2.15%.

<span id="_Toc222328529" class="anchor"></span>**Table 2.11** Changes to
National Minimum Wage and Public Sector Wages \[2025\]

<table style="width:65%;">
<colgroup>
<col style="width: 10%" />
<col style="width: 26%" />
<col style="width: 9%" />
<col style="width: 19%" />
</colgroup>
<thead>
<tr>
<th><strong>Policy</strong></th>
<th><p><strong>Measure</strong></p>
<p><strong>(<em>Legal Basis</em>)</strong></p></th>
<th style="text-align: center;"><strong>Impact on EUROMOD</strong></th>
<th style="text-align: center;"><strong>Comments</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>National Minimum Wage (Private Sector)</strong></td>
<td><p>NMW updated to €870</p>
<p><em>Decree-Law 112/2024</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Public Sector Wages</strong></td>
<td><p>Updating of Public Sector workers’ wages:</p>
<ul>
<li><p>The Base Remuneration is increased to €878.41;</p></li>
<li><p>Wages between €878.42 and €2,631.62 are increased by
€56.58;</p></li>
<li><p>Wages equal or over €2,631.62 are increased by 2.15%.</p></li>
</ul>
<p><em>Decree-Law 1/2025</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Source: Decreto-Lei n.º 112/2024 (Private Sector NMW); Decreto-Lei n.º
1/2025 (Public Sector wages) — Diário da República, www.dre.pt

<span id="_Toc222328530" class="anchor"></span>**Table 2.12** Changes to
Pension Benefits \[2025\]

<table style="width:65%;">
<colgroup>
<col style="width: 10%" />
<col style="width: 26%" />
<col style="width: 9%" />
<col style="width: 19%" />
</colgroup>
<thead>
<tr>
<th><strong>Policy</strong></th>
<th><p><strong>Measure</strong></p>
<p><strong>(<em>Legal Basis</em>)</strong></p></th>
<th style="text-align: center;"><strong>Impact on EUROMOD</strong></th>
<th style="text-align: center;"><strong>Comments</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Legal Age of Retirement</strong></td>
<td><p>66 years and 7 months</p>
<p><em>Order 414/2023</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Pension Update Formula</strong></td>
<td><p>Updating of Old Age, Survivors and Incapacity Pensions:</p>
<ul>
<li><p>Up to €319.49 updated by 3.85%;</p></li>
<li><p>Between €319.49 and €1045: updated by 3.85%, subject to a minimum
increase of €12.30;</p></li>
<li><p>Between €1045 and €1567.50: updated by 3.35%, subject to a
minimum increase of €40.23;</p></li>
<li><p>Between €1567.50 and €3135: updated by 2.10%, subject to a
minimum increase of €52.51;</p></li>
<li><p>Between €3135 and €6270: updated by 1.85%, subject to a minimum
increase of €65.84;</p></li>
</ul>
<p>Pensions equal or above to 12xSSI (€6270), subject to exceptions, do
not suffereceive any increase.</p>
<p><em>Order 372-B/2024</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Minimum Pensions</strong></td>
<td><p>Increased by 3.8%</p>
<p><em>Order 372-B/2024</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Social Old Age Pension</strong></td>
<td><p>Increased by 3.8%, to €255.25.</p>
<p><em>Order 372-B/2024</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Extraordinary Solidarity Supplement
(<em>CSI</em>)</strong></td>
<td><p>Increased by:</p>
<ul>
<li><p>€22.21, if aged under 70</p></li>
<li><p>€44.43, if aged 70 or over</p></li>
</ul></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
</tbody>
</table>

Note: “**I**” *included* in the micro-data but not simulated; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated. “**E**” *excluded* from the model’s scope, as it is
neither included in the microdata nor simulated by EUROMOD; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated.

Source: Portaria n.º 372-B/2024 (pension valorisation and extraordinary
supplement) — Diário da República, www.dre.pt

#### Changes to Pension Benefits 

As the impact of the COVID-19 pandemic on mortality faded, the long-term
increase in life expectancy resumed. This meant that in 2025, the Legal
Age of Retirement increases to 66 years and 7 months (see Table 2-12).

In 2025, pensioners receiving the **Minimum Pension** and the **Social
Old Age Pension** benefited from increases (3.8%) above the projected
rate of inflation (see Table 2-12). Furthermore, pensioners with Old
Age, Survivors and Disability Pensions up to 3\*SSI also benefited from
an extraordinary increase of 1.25% - which resulted in further
contributed to real income gains for this particular group of
individuals (see Table 2-12).

#### Changes Other Social Security Benefits

In this section, we cover:

Changes to the indexation mechanism (SSI) of the regular uprating of
Social Security benefits;

Changes to non means-tested benefits;

Changes to means-tested benefits.

As can be seen in Table 2-13, the **Social Support Index**, was upgraded
to €522.5 - i.e. 2.6%, just above the projected rate of inflation for
2025.

<span id="_Toc222328531" class="anchor"></span>**Table 2.13** Indexation
of Social Security Benefits \[2025\]

<table style="width:65%;">
<colgroup>
<col style="width: 10%" />
<col style="width: 26%" />
<col style="width: 9%" />
<col style="width: 19%" />
</colgroup>
<thead>
<tr>
<th><strong>Policy</strong></th>
<th><p><strong>Measure</strong></p>
<p><strong>(<em>Legal Basis</em>)</strong></p></th>
<th style="text-align: center;"><strong>Impact on EUROMOD</strong></th>
<th style="text-align: center;"><strong>Comments</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Social Support Index</strong></td>
<td><p>Social Support Index updated to €522.5</p>
<p><em>Order 6-B/2025</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Note: “**I**” *included* in the micro-data but not simulated; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated. “**E**” *excluded* from the model’s scope, as it is
neither included in the microdata nor simulated by EUROMOD; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated.

Source: Portaria n.º 6-B/2025 (SSI update) — Diário da República,
www.dre.pt

The changes introduced, in 2025, to non means-tested benefits are
relatively minor and refer mostly to byproducts of the increase in the
SSI (see Sections 2.5.1 and 2.5.2). By contrast, we identify a number of
substantive changes to a number of means-tested Social Security benefits
in 2025 (see Table 2-14):

The **Social Insertion Income** benefit (*RSI*) for the head beneficiary
was increased by 2.1% (see Table 2-14 and Section 2.5.4)

The value of the **Child Benefit** was upgraded by 2.1%, with the
exception of benefits for children under 36 months in the 3rd Income
Bracket – who saw their benefit increase by 2.7% (see Table 2-34,
Section 2.5.7);

In the same way, the **Child Benefit’s Supplement for Large Families**
was uprated by 2.1%, with the exception of benefits for large families
in the 4th Income Bracket – who saw their benefit increase by 2.5% (see
Table 2-35, Section 2.5.7);

The **Child Guarantee** reference value has also been increased from
€122 to €124.56, per month. This means that, discounting the increase in
the Child Benefit, the value of the Child Guarantee (differential)
benefit was effectively raised by 2.1% (see Table 2-39, Section 2.5.7).

<span id="_Toc222328532" class="anchor"></span>**Table 2.14** Changes to
Means Tested Social Security Benefits \[2025\]

<table style="width:65%;">
<colgroup>
<col style="width: 10%" />
<col style="width: 26%" />
<col style="width: 9%" />
<col style="width: 19%" />
</colgroup>
<thead>
<tr>
<th><strong>Policy</strong></th>
<th><p><strong>Measure</strong></p>
<p><strong>(<em>Legal Basis</em>)</strong></p></th>
<th style="text-align: center;"><strong>Impact on EUROMOD</strong></th>
<th style="text-align: center;"><strong>Comments</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Child Benefit</strong></td>
<td><p>Updating of Reference Amounts by 2.1%</p>
<p><em>Order 112/2025</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Child Guarantee (Annual) Reference Amount increased to €1495
(€124.56, per month)</p>
<p><em>Order 112/2025</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Solidarity Supplement for the Elderly
(<em>CSI</em>)</strong></td>
<td><p>Annual Reference Amount updated to €7,568.</p>
<p><em>Order 311/2024</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>Social Integration Income (<em>RSI</em>)</strong></td>
<td><p>RSI Monthly Reference Amount updated to €242.23 month</p>
<p><em>Order 39/2025</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Note: “**I**” *included* in the micro-data but not simulated; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated. “**E**” *excluded* from the model’s scope, as it is
neither included in the microdata nor simulated by EUROMOD; “**PS**”
*partially simulated* as some of its applicable rules are not simulated;
“**S**” *simulated,* although some minor or very specific rules may not
be simulated.

Source: Portaria n.º 311/2024 (CSI reference value update); Portaria n.º
39/2025 (RSI update) — Diário da República, www.dre.pt

The only exception to this across-the-board approach, was the
**Solidarity Supplement for the Elderly (*CSI*)**, which was increased
by 5%, to €7,568 - almost twice the projected rate of inflation (see
Table 2-23, Section 2.5.5). The other exception, although in an opposite
direction, is the **Extraordinary Housing Support** scheme, which was
not updated (see Section 2.5.11).

#### Changes to Direct Taxes (SSC & PIT)

In 2025, there were no significant changes to Social Security
Contributions (SSC).

As can be seen Table 2-11, changes to the PIT were meant to reduce the
tax burden, particularly on the young:

The **limit on the allowance for incomes from work** (Cat. A) was
increased by 2.6% - in line with the SSI, to which it is now indexed
(see Table 2-47, Section 2.7.1);

The **limit on the allowance for incomes from pensions** (Cat. H) was
increased by 2.6% - in line with the SSI, to which it is now indexed
(see Table 2-47, Section 2.7.1);

The allowance for Young Persons was significantly expanded, yet again:

1)  The age of eligibility was expanded for up to 35 (see Table 2-48,
    Section 2.7.1);

<!-- -->

1)  Education-related eligibility requirements were eliminated was
    expanded for up to 35 (see Table 2-48, Section 2.7.1);

2)  The maximum duration of the allowance was also expanded to 10 years
    (see Table 2-52, Section 2.7.1);

3)  Both the level and limits of the allowance were significantly
    increased (see Table 2-52, Section 2.7.1);

    **PIT Net Income Guarantee** was also upgraded to the annual amount
    of NMW, €12,180 (see Table 2-52, Section 2.7.1);

    **PIT income brackets** were upgraded by 4.6%, very much above the
    projected inflation for 2026 (see Table 2-49, Section 2.7.1);

    **PIT marginal tax rates** were reduced by (see Table 2-50, Section
    2.7.1):

<!-- -->

1)  \- 0.50 percentage points in the 1st, 2nd and 3rd income bracket;

<!-- -->

4)  \- 0.60 percentage points in the 4th, 5th and 6th income bracket;

5)  \- 0.40 percentage points in the 7th and 8th income brackets.

    The **PIT** **Housing Tax Credit, concerning expenses with rents**
    was increased (see Table 2-53, Section 2.7.1):

<!-- -->

1)  To €1000, for individuals with incomes falling in the first income
    bracket;

<!-- -->

6)  To a varying degree, for individuals with incomes equal or above the
    1st income bracket of PIT and under €30,000.

7)  To €800, for individuals with incomes above €30,000;

<span id="_Toc222328533" class="anchor"></span>**Table 2.15** Changes to
Personal Income Tax \[2025, Continent\]

<table style="width:65%;">
<colgroup>
<col style="width: 10%" />
<col style="width: 30%" />
<col style="width: 9%" />
<col style="width: 15%" />
</colgroup>
<thead>
<tr>
<th><strong>Policy</strong></th>
<th><p><strong>Measure</strong></p>
<p><strong>(<em>Legal Basis</em>)</strong></p></th>
<th style="text-align: center;"><strong>Impact on EUROMOD</strong></th>
<th style="text-align: center;"><strong>Comments</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>PIT: Tax Allowances</strong></td>
<td><p>Increases in level and upper limits of the Partial Tax Exemption
for Youngsters (individuals until 35 years old):</p>
<ul>
<li><p>1st year - 100%, with a limit of 55 x SSI;</p></li>
<li><p>2nd to the 4th year - 75%, with a limit of 55 x SSI;</p></li>
<li><p>5th to the 7th year - 50%, with a limit of 55 x SSI;</p></li>
<li><p>From the 8th to the 10th year - 25%, with a limit of 55 x
SSI;</p></li>
</ul>
<p><em>Law 45-A/2024, Art. 89.º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Tax allowance for income from work is now determined by reference
to 8.54*SSI, and thus increased to €4,462.15.</p>
<p><em>Law 45-A/2024, Art. 89.º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Tax allowance for income from pensions is now determined by
reference to 8.54*SSI and thus increased to €4,462.15.</p>
<p><em>Law 45-A/2024, Art. 89.º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>PIT: Minimum Income Guarantee</strong></td>
<td><p>The (Annual) Reference Value of the Minimum Income Guarantee was
increased to €12,180 (i.e., 14* NMW),</p>
<p><em>Law 45-A/2024, Art. 89.º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>PIT: Income Brackets</strong></td>
<td><p>PIT Income Brackets were increased by 4.6%</p>
<p><em>Law 45-A/2024, Art. 89.º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>PIT: Rates</strong></td>
<td><p>Reduction in marginal rates :</p>
<ul>
<li><p>- 0.5 p.p in the 1<sup>st</sup>, 2<sup>nd</sup> and
3<sup>rd</sup> income brackets;</p></li>
<li><p>- 0.6 p.p in the 4<sup>th</sup>, 5<sup>th</sup> and
6<sup>th</sup> income brackets;</p></li>
<li><p>- 0.4 p.p in the 7<sup>th</sup> and 8<sup>th</sup> income
brackets;</p></li>
</ul>
<p><em>Law 55-A/2025, Article 2º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><strong>PIT: Tax Credits</strong></td>
<td><p>The upper limit of the Housing Tax Credit, concerning rent
expenses, for individuals in the 1<sup>st</sup> income bracket of PIT,
is raised to €1000 (from €900);</p>
<p><em>Law 36/2024, Article 2º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>The formula for computing the upper limit of the Housing Tax
Credit, concerning rent expenses, for individuals with incomes equal or
above 1st Income Bracket of PIT and under €30,000, now varies between
€700 and €1000 (previously between €600 and €900),</p>
<p><em>Law 36/2024, Article 2º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>The upper limit of the Housing Tax Credit, concerning rent
expenses, for individuals with income above €30,000 is raised to €700
(from €600);</p>
<p><em>Law 36/2024, Article 2º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Source: Lei n.º 36/2024, de 30 de julho (OE 2025), art. 2.º — Autoridade
Tributária e Aduaneira, www.portaldasfinancas.gov.

<span id="_Toc222328534" class="anchor"></span>**Table 2.16** Changes to
Personal Income Tax \[2025, Azores & Madeira\]

<table style="width:65%;">
<colgroup>
<col style="width: 10%" />
<col style="width: 31%" />
<col style="width: 9%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th><strong>Policy</strong></th>
<th><p><strong>Measure</strong></p>
<p><strong>(Legal Basis)</strong></p></th>
<th style="text-align: center;"><strong>Impact on EUROMOD</strong></th>
<th style="text-align: center;"><strong>Comments</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Personal Income tax</strong></td>
<td><p>Azores: Updating Income Brackets, by 4.6%</p>
<p><em>Law 45-A/2024, Art. 89.º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Azores: Reduction in marginal rates - 0.35 p.p in the
1<sup>st</sup>, 2<sup>nd</sup> and 3<sup>rd</sup> income brackets;</p>
<ul>
<li><p>- 0.42 p.p in the 4<sup>th</sup>, 5<sup>th</sup> and
6<sup>th</sup> income brackets;</p></li>
<li><p>- 0.28 p.p. in the 7<sup>th</sup> and 8<sup>th</sup> income
brackets;</p></li>
</ul>
<p><em>Law 55-A/2025, Article 2º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td></td>
<td><p>Madeira: Updating Income Brackets, by 4.6%</p>
<p><em>Regional Decree-Law 3/2025/M, Article 2º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td></td>
<td><p>Madeira: Reduction in marginal rates:</p>
<ul>
<li><p>- 0.35 p.p in the 1<sup>st</sup>, 2<sup>nd</sup> and
3<sup>rd</sup> income brackets;</p></li>
<li><p>- 0.42 p.p in the 4<sup>th</sup>and 5<sup>th</sup> income
brackets;</p></li>
<li><p>- 7.88 p.p. in the 6<sup>th</sup> income bracket;</p></li>
<li><p>- 5.56 p.p. in the 7<sup>th</sup> income bracket;</p></li>
<li><p>- 3.06 p.p in the 8<sup>th</sup> income bracket;</p></li>
</ul>
<p><em>Regional Decree-Law Law 3/2025/M, Article 2º</em></p></td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Source: Decreto Legislativo Regional n.º 3/2025/M, art. 2.º (Madeira) —
Diário da República, www.dre.pt

#### Changes to Consumption Taxes

There were also changes to **Consumption Taxes,** namely**:**

The **VAT** reduced rate (6%) extended to baby and children food, both
in the Continent and in Azores and Madeira (see Table 2-56, Section
2.8.1);

Increase of ISP applicable to fuels (see Table 2-59, Section 2.8.2):

1)  Gasoline: to €481,26/1000 liters (from €460,36 /1000 liters);

<!-- -->

1)  Diesel: €337.21/1000 liters of diesel (from €323,54 /1000 liters).

    Decrease in Carbon Tax to 67,395 euros/ton of CO2 (see Section
    2.8.2).

## Order of simulations and interdependence

The following table shows the benefits and taxes simulated by EUROMOD
for the years of 2022-2025. As there were only a few structural changes
in the Portuguese tax-benefit system during this period, the order by
which the policies are simulated remains mainly unchanged.

Essentially, the simulation order results from policies’
interdependence, as the income simulated by some policies is then taken
as an input by others. For example, the minimum wage and minimum pension
policies are simulated first, as their outcomes are employment and
pension’s income, which will be used by subsequent policies.

The simulation of social contributions comes next, as employment income
is subject to social contributions.

Unemployment benefits should be simulated next, as all inputs required
are now available (either from the original data or simulated) and its
output (unemployment benefit income) will be used after.

Then parental leave benefits are simulated[^1] as their income tests
include unemployment benefits and pensions.

All necessary inputs are now available to simulate the personal income
tax and the tax on capital income.

The minimum means-tested schemes and social integration income comes
next, as they are part of the assessed income to determine child benefit
eligibility. Finally, after simulating the child benefit, the remaining
temporary and extraordinary benefits are also simulated.

<span id="_Toc222328535" class="anchor"></span>**Table 2.17** EUROMOD
spine: order of simulation \[2022-2025\]

| **Policy** | **2022** | **2023** | **2024** | **2025** |  |
|----|----|----|----|----|----|
| SetDefault_pt | **on** | **on** | **on** | **on** | DEF: DEFAULT VALUES FOR VARIABLES |
| uprate_pt | **on** | **on** | **on** | **on** | DEF: UPRATING FACTORS |
| Uprate_bands_pt | **on** | **on** | **on** | **on** | DEF: UPRATING IN BANDS: PENSIONS |
| Uprate_yempb_pt | **n/a** | **n/a** | **on** | **on** | DEF\_ UPRATING IN BANDS: CIVIL SERVANTS WAGES 2023 & 2024 |
| ConstDef_pt | **on** | **on** | **on** | **on** | DEF: CONSTANTS |
| ilsdef_pt | **on** | **on** | **on** | **on** | DEF: STANDARDISED INCOME LISTS |
| ilsUDBdef_pt | **on** | **on** | **on** | **on** | DEF: UDB-RELATED STANDARDISED INCOME LISTS |
| Ildef_pt | **on** | **on** | **on** | **on** | DEF: NON-STANDARD INCOME CONCEPTS |
| random_pt | **on** | **on** | **on** | **on** | DEF: Random assignment for bsaoa_s |
| TransLMA_pt | **off** | **off** | **off** | **off** | DEF: Modelling labour market transitions |
| tudef_pt | **on** | **on** | **on** | **on** | DEF: ASSESSMENT UNITS |
| InitVars_pt | **on** | **on** | **on** | **on** | DEF: Initialise variables |
| pxp00_pt | **a n/** | **on** | **n/a** | **n/a** | BEN: Pensions: 2022 Extraordinary (10 euros) increase in pensions |
| pxp01_pt | **n/a** | **on** | **n/a** | **n/a** | BEN: Cost of Living: Extraordinary Pension Supplement (2022) |
| pxp02_pt | **n/a** | **n/a** | **n/a** | **on** | BEN: Extraordinary Pension Supplement (2024) |
| yem_pt | **switch** | **switch** | **switch** | **switch** | INC: Minimum wage (salario mínimo) |
| yempb_pt | **off** | **off** | **off** | **off** | INC: Public wages cuts |
| poacm_pt | **off** | **off** | **off** | **off** | BEN: Minimum pension (Pensoes mínimas) |
| pcuts_pt | **n/a** | **n/a** | **n/a** | **n/a** | INC: Pensions cuts and solidarity contributions |
| neg_pt | **on** | **on** | **on** | **on** | DEF: recode negative self-employment income to zero |
| yemcomp_pt | **on** | **off** | **off** | **off** | BEN: Wage compensation scheme Covid-19 |
| tscee_pt | **on** | **on** | **on** | **on** | SIC: Employee social insurance contributions |
| tscer_pt | **on** | **on** | **on** | **on** | SIC: Employer social insurance contribution |
| tscse_pt | **on** | **on** | **on** | **on** | SIC: Self-employed social insurance contribution |
| ysecomp_pt | **on** | **off** | **off** | **off** | BEN: Self-employment income compensation scheme Covid-19 |
| tscse_pt | **on** | **on** | **on** | **on** | SIC: Self-employed social insurance contribution (repetition of policy with order 20) |
| bunct_pt | **on** | **on** | **on** | **on** | BEN: Unemployment insurance (Subsídio de desemprego) PART- SIMULATED |
| bunnc_pt | **on** | **on** | **on** | **on** | BEN: Unemployment assistance (subsidio social de desemprego) PARTILLY SIMULATED |
| buncm_pt | **on** | **on** | **on** | **on** | BEN: Unemployment benefit bonus |
| poanc_pt | **on** | **on** | **on** | **on** | BEN: Social Pension (Pensão social de velhice) |
| bmapr_pt | **switch** | **switch** | **switch** | **switch** | BEN: Prenatal family allowance (Abono de família pré-natal) |
| bplct_pt | **switch** | **switch** | **switch** | **switch** | BEN: Parental allowance (Subsídio parental) |
| bplnc_pt | **switch** | **switch** | **switch** | **switch** | BEN: Parental social allowance (Subsídio social parental) |
| tin00_pt | **on** | **on** | **on** | **on** | TAX: Progressive personal income tax |
| tiniy_pt | **on** | **on** | **on** | **On** | TAX: Income tax on capital income |
| bsaoa_pt | **on** | **on** | **on** | **On** | BEN: Solidarity supplement for older persons (Complemento Solidário para Idosos - CSI) |
| bsa00_pt | **on** | **on** | **on** | **on** | BEN: Social insertion income (Rendimento social de inserção ou mínimo garantido) |
| bfaxp_pt | **n/a** | **on** | **n/a** | **n/a** | BEN: Cost of Living: Family income support 2022 (Apoio excecional aos rendimentos e apoio excecional a crianças e jovens) |
| bch_pt | **on** | **on** | **on** | **on** | BEN: Family benefit (Abono de família para crianças e jovens) |
| bfaxp01_pt | **n/a** | **n/a** | **on** | **n/a** | BEN: COST-OF-LIVING: Extraordinary Supplement for Vulnerable Families 2023 (Apoio extraordinário a famílias mais vulneráveis) |
| bhotn_pt | **n/a** | **n/a** | **on** | **on** | BEN: Extraordinary Housing Support (Apoio extraordinário à habitação) |
| tco_pt | **on** | **on** | **on** | **on** | TAX: Commodities |
| spp_pt | **off** | **off** | **off** | **off** | TAX/BEN: Special Price Policies |
| output_std_pt | **on** | **on** | **on** | **on** | DEF: STANDARD OUTPUT INDIVIDUAL LEVEL |
| parben_output_std_pt | **switch** | **switch** | **switch** | **switch** | DEF: STANDARD OUTUT INDIVIDUAL LEVEL |
| output_std_hh_pt | **off** | **off** | **off** | **off** | DEF: STANDARD OUTPUT HOUSEHOLD LEVEL |

Source: Own elaboration.

The last policy included in the spine is the tco_pt (consumption taxes).
It is placed at the very end because consumption tax liabilities (VAT
and excises) depend on household consumption expenditures, and these are
estimated by the model based on the disposable income shares (xs\_\*
variables included in the input data) and simulated disposable income
(ils_dispy). This is why before running any simulation of consumption
tax policy it is required to activate all the other policies intervening
in the simulation of disposable income.

## Policy extensions

There are several policies / extensions that can be turned on/off in the
Portuguese model:

**Uprating by Average Adjustment (UAA),** allowing the user to choose
between uprating (non-simulated) public pensions based on the growth in
average amounts (if extension is on) or by using statutory indexation
rules (if extension is off). The default for the baselines is off.

**Minimum Wage Adjustment (MWA)**, allowing the user to switch on/off
the minimum wage simulation. The default for the baselines is off.

**Full Year Adjustments (FYA).** While EUROMOD usually simulates
policies as of June 30th of the respective year, it is also possible to
simulate within-year policy changes. It is now switched off in the
baseline scenario.

**Parental Benefits Extension (PBE),** allowing the user to choose
between the observed (non-simulated) parental leave benefits (extension
off) or the simulated ones (extension on). The default for the baselines
is off.

**HHoT – Unemployment extension (HHoT_un),** improves the simulation
accuracy of the unemployment insurance benefit when EUROMOD is run with
hypothetical data. For instance, in most countries the legislation of
this benefit requires information on variables such as individuals’
employment history, which are not available in SILC; we can define these
variables in HHoT and use them to simulate the policy’s rules more
precisely when running the model with hypothetical data. This extension
is set to on when the model is used with HHoT data.

The **HHoT Monthly Unemployment (HHoT_mu)** extension enables a monthly
unemployment benefit simulation, similar to the approach used by the
OECD TaxBEN for the calculation of monthly Net Replacement Rate (NRR)
indicators. Those indicators measure to what extent a person's previous
income from work is maintained after a certain number of months in
unemployment. With this extension, unemployment benefit amounts are
calculated with respect to a *specific month* of the unemployment spell
and are then converted to annual amounts by multiplying by 12. By
default, this extension is switched off; it is only set to on when the
model is used for the calculation of the NRR indicators.

‘**Minimum pensions**’ (*poacm_pt*). This policy is switched off in the
baseline due to its underestimating effect on elderly poverty.

‘**Labour market transitions**’ (*TransLMA_pt**)*****.** This policy
defines the individuals that are selected to undergo transitions to
monetary compensation schemes and/or unemployment. The transitions are
only enabled if used together with the Labour Market Adjustments (LMA)
add-on (i.e., the LMA add-on switches on this policy automatically). The
transitions are based on a random allocation of individuals and they
might be triggered by feeding the parameters of this policy with
official or hypothetical information[^2]. This policy, in combination
with the LMA add-on, enables the simulation of the wage compensation
scheme (*yemcomp_pt*) and the self-employment compensation scheme
(*ysecomp_pt*).

**Benefit Calibration Adjustments (BCA)**, allowing the user to
calibrate the receipt of benefits to match the simulated total
expenditure of a benefit to real expenditure from external statistics.
The extension is implemented for the simulation of the social assistance
benefit (*bsa00_pt*) and Solidarity supplement for older persons
(*bsaoa_pt*). The default for the baseline is off. When the extension is
on, a subset of eligible of observations is selected randomly as
beneficiaries so that the real expenditure is reached, removing the
benefit from the rest of the eligible observations; when off, all
eligible observations are kept as beneficiaries. This extension shares
most of its functions with the BTA extension; as a general rule, only
one of the extensions should be on, but if both are, the lowest rate
between the take-up rate and the calibration rate will be applied. More
details on the specific implementation of BCA and BTA extensions are
provided in the subsections describing the corresponding benefits.

**Benefit Take-up Adjustments (BTA),** allowing the user to apply
non-take-up corrections.  The extension is used for  the  simulation 
of  the social assistance benefit (*bsa00_pt*) and Solidarity supplement
for older persons (*bsaoa_pt*). The default for the baseline is off.
When the extension is on, a share of (weighted) eligible observations
equal to the take-up rate is selected randomly as beneficiaries,
removing the benefit from the rest of the eligible observations; when
off, all eligible observations are kept as beneficiaries. This extension
shares most of its functions with the BCA extension; as a general rule,
only one of the extensions should be on, but if both are, the lowest
rate between the take-up rate and the calibration rate will be applied.
More details on the specific implementation of BCA and BTA extensions
are provided in the subsections describing the corresponding
benefit(s). 

The **Consumption Inflation Adjustment (CIA)** extension enables users
to simulate price (inflation) shocks under the assumption that
households do not immediately adjust their consumption patterns
(constant quantities) in response to a sudden change. This extension can
only be enabled if used together with Consumption Taxes add-ons CT_XBASE
and CT_XCQ, respectively baseline and constant quantities. By default,
this extension is switched OFF. Switching ON the inflation simulation
(without changing parameters) allows users to apply [official annual
inflation
rates](https://euromod-web.jrc.ec.europa.eu/sites/default/files/Inflation_rates_by_product_category.xlsx)
between two consecutive years (sourced from
[Eurostat](https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_manr/default/table?lang=en)
and [DG ECFIN’s latest quarterly
forecasts](https://economy-finance.ec.europa.eu/document/download/6e6837c1-e00c-42ed-9f10-8d1ad56f913a_en?filename=spring_forecast-2024_statisical%20annext_en.pdf))
as stored in the Consumption Taxes (CT) table by
*\$tco_base_upr\_\[COICOP\]*. Users can also simulate their own
hypothetical price shock scenarios at COICOP level 1 (2-digits)
categories, with the Housing & Utilities split between Energy and other.
To do so users should modify constants *\$tco_CIA\_\** in *ConstDef_cc*.
For example, what if annual inflation for food was 5% instead of the
officially recorded? Changing *\$tco_CIA_01* to 5% for food and
non-alcoholic beverages, multiplies the expenditures of foods and
non-alcoholic beverages by 1.05. For the CIA extension to work properly,
the users will need to add a new variable *ydsyc_a* to the input data
recording for each household the disposable income growth between two
consecutive years. \[HINT: Run systems *t* and *t+1*. Compute household
disposable income for each year. For each household calculate *ydsyc_a*
= *(hh_dpit+1 – hh_dpit)/hh_dpit*\]

## Benefits

### Unemployment benefit – insurance (*bunct_pt*)

#### Definition

The unit of analysis is the individual. There are no benefit units
(*i.e.,* the units are single), and no income test.

#### Eligibility conditions

Have been fired (exclusively by decision of the employer) after working
for at least 360 days over the previous 24 months (insurance period). It
excludes self-employment.

Actively looking for work.

#### Benefit amount

Reference remuneration: wages’ average of the first 12 of the 14 months
before the firing date.

Amount: 65% of the reference remuneration. Lower bound: 1.15 x SSI (if
the reference remuneration corresponds, at least, to the NMW) since
2021. Upper bound: 2.5 x SSI.

Bonus of 10% for couples with children if both parents claim insurance
unemployment benefit. The increase is attributed to each of the
beneficiaries and if one of them no longer receives the insurance
unemployment benefit and starts receiving the assistance unemployment
benefit or, remaining unemployed, does not receive any benefit for it,
the other beneficiary continues to receive the bonus.

#### Unemployment benefit for chairmen and self-employed

Chairmen and self-employed may also be entitled to an unemployment
benefit, under specific rules. (NOT SIMULATED)

#### EUROMOD modelling

The unemployment benefits cannot be fully simulated in EUROMOD, as there
is no information on the reason why people became unemployed (voluntary
or compulsory), nor on the duration of the most recent jobs. These
constraints apply to the main unemployment benefit – called contributory
or insurance unemployment benefit – and to the social unemployment
benefit (see next section), also referred to as non-contributory benefit
(although there was some limited contribution) or assistance
unemployment benefit.

Nonetheless, a split of the original variable in the database (*bun*)
can be simulated by observing some of the occurrences more easily
associated with the latter kind of benefit (see next section for a more
detailed description of the splitting process).

<span id="_Toc222328536" class="anchor"></span>**Table 2.18**
Characteristics of the Unemployment Benefit – Insurance (*bunct_pt*)
\[2022-2025\]

<table style="width:65%;">
<colgroup>
<col style="width: 7%" />
<col style="width: 12%" />
<col style="width: 11%" />
<col style="width: 26%" />
<col style="width: 8%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"><strong>2022</strong></th>
<th style="text-align: center;"><strong>2023-2025</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="3"
style="text-align: center;"><strong>Eligibility</strong></td>
<td style="text-align: center;">Contribution period</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">1 year out of the last 2</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">Other conditions</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">Have been fired &amp; listed on the
unemployment register (actively looking for work)</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">Eligibility of self-employed (NOT
SIMULATED)</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">Yes (under specific rules)</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td rowspan="5"
style="text-align: center;"><strong>Payment</strong></td>
<td style="text-align: center;">Contribution base</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">Wages’ average of the first 12 of the 14
months before the firing date</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">Basic amount</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">65% of the contribution base</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">Additional amount</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">10% bonus for couples with children if
both partners claim insurance unemployment benefit</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">Floor</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">SSI</td>
<td style="text-align: center;">Or 1.15xSSI</td>
</tr>
<tr>
<td style="text-align: center;">Ceiling</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">2.5 x SSI</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td rowspan="16" style="text-align: center;"><strong>Duration in
months</strong></td>
<td rowspan="4" style="text-align: center;">Up to 29 years old</td>
<td style="text-align: center;">Up to 14 months</td>
<td style="text-align: center;">5 months</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">15-23 months</td>
<td style="text-align: center;">7 months</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">24+ months</td>
<td style="text-align: center;">11 months</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">Bonus</td>
<td style="text-align: center;">30 days for every 5 years employed</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td rowspan="4" style="text-align: center;">30-39 years old</td>
<td style="text-align: center;">Up to 14 months</td>
<td style="text-align: center;">6 months</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">15-23 months</td>
<td style="text-align: center;">11 months</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">24+ months</td>
<td style="text-align: center;">14 months</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">Bonus</td>
<td style="text-align: center;">30 days for every 5 years employed</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td rowspan="4" style="text-align: center;">40-49 years old</td>
<td style="text-align: center;">Up to 14 months</td>
<td style="text-align: center;">7 months</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">15-23 months</td>
<td style="text-align: center;">12 months</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">24+ months</td>
<td style="text-align: center;">18 months</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">Bonus</td>
<td style="text-align: center;">45 days for every 5 years employed</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td rowspan="4" style="text-align: center;">50+ years old</td>
<td style="text-align: center;">Up to 14 months</td>
<td style="text-align: center;">9 months</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">15-23 months</td>
<td style="text-align: center;">16 months</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">24+ months</td>
<td style="text-align: center;">18 months</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">Bonus</td>
<td style="text-align: center;">60 days for every 5 years employed</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td rowspan="2" style="text-align: center;"><strong>Subject
to</strong></td>
<td style="text-align: center;">Taxes</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">No</td>
<td style="text-align: center;">No changes</td>
</tr>
<tr>
<td style="text-align: center;">SIC</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">No</td>
<td style="text-align: center;">No changes</td>
</tr>
</tbody>
</table>

Source: Decreto-Lei n.º 220/2006, de 3 de novembro, as amended;
Instituto da Segurança Social (www.seg-social.pt)

### Unemployment Benefit – Assistance (*bunnc_pt*)

#### Definition

Either this benefit is granted as an initial benefit to claimants who
have not worked long enough to claim the main unemployment benefit, or
as an extension to those who cease to be entitled to the main
unemployment benefit (as long as they meet the additional conditions
listed below).

Unlike the main benefit, the social benefit considers both individual
and family units. Family units are defined as:

The individual;

His/her partner;

Any dependent children (those below 18 years old).

#### Eligibility conditions

For the ‘initial benefit modality’: Have been fired (exclusively by
decision of the employer) after working for at least 180 days over the
previous 12 months (insurance period). It excludes self-employment.

For the ‘extended modality’: Having ended the main unemployment benefit.

For the long-term unemployed: Previous recipients of the means-tested
social unemployment benefit who are still unemployed six months after
the end of the benefit and still fulfil the remaining conditions.

Actively looking for work.

#### Income test

The family unit equivalent income must be less than 80% of the SSI. The
equivalent income is defined by total income after applying the
following equivalence scale:

Recipient – 1

Every other adult (18+) – 0.7

Every under-18 – 0.5

There are specific rules regarding investment income (NOT SIMULATED):
family’s total financial assets amount must be lower than 240 x SSI.

<span id="_Toc222328537" class="anchor"></span>**Table 2.19**
Unemployment benefit – assistance (*bunnc_pt*): assessed income

| **Variable** | **Label** |
|----|----|
| yem | INCOME: Employment |
| yse | INCOME: Self-employment |
| poact_s | BENEFIT/PENSION: Old age: contributory |
| poanc_s | BENEFIT/PENSION: Old age: non-contributory (simulated) |
| psu | BENEFIT/PENSION: Survivors |
| pdi | BENEFIT/PENSION: Disability |
| bed | BENEFIT/PENSION: Education |
| ypp | INCOME: Private pension |
| ypr | INCOME: Property |
| ypt | INCOME: Private transfers received |
| yiy | INCOME: Investment |
| bho | BENEFIT/PENSION: Housing (new from August 2010)<sup>(1)</sup> |

Note: <sup>(1)</sup> For non-monetary housing benefits (benefits in
kind), the maximum amount of rent subsidy is considered, in progressive
terms along the duration of the unemployment benefit. (NOT SIMULATED)

Source: Own elaboration

#### Benefit amount

Amount: 80% of the SSI for individuals in a single benefit unit and 100%
of the SSI if the benefit unit size is larger than one.

Bonus of 10% x NMW per child in the household.

Amount of the long-term unemployed benefit: 80% of the previous one.

#### Benefit’s length

‘Initial modality’: Same as for the insurance unemployment benefit.

‘Extended modality’: if age at the end of the insurance benefit is below
40 years old, the length is half of that benefit’s length. Otherwise, it
is the same as the ‘initial modality’.

#### EUROMOD modelling

As mentioned above, the unemployment benefits cannot be fully simulated,
but it is possible to simulate a split of the original unemployment
benefit variable (*bun*) into assistance/social and
insurance/contributory related variables (*bunnc_s* and *bunct_s*,
respectively).

The original splitting of the unemployment benefit variable (*bun*) into
two variables, namely the ones respecting to the contributory
unemployment benefit (*bunct*) and the non-contributory unemployment
benefit (*bunnc*), was made through the EU-SILC variables py092g and
py09g, respectively.

<span id="_Toc222328538" class="anchor"></span>**Table 2.20**
Characteristics of the Unemployment Benefit – Assistance (*bunnc_pt*)
\[2022-2025\]

<table style="width:61%;">
<colgroup>
<col style="width: 7%" />
<col style="width: 16%" />
<col style="width: 37%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"><strong>2022-2025</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="3"
style="text-align: center;"><strong>Eligibility</strong></td>
<td style="text-align: center;">Contribution period</td>
<td style="text-align: center;"><p>180 days over the last year
<em>(“initial modality”)</em> <strong>OR</strong></p>
<p>having ended the main unemployment benefit <em>(“extended
modality”)</em></p></td>
</tr>
<tr>
<td style="text-align: center;">Other conditions</td>
<td style="text-align: center;"><p>Family unit equivalent income &lt;
80% of the SSI <strong>&amp;</strong></p>
<p>actively looking for work)</p></td>
</tr>
<tr>
<td style="text-align: center;">Eligibility of self-employed</td>
<td style="text-align: center;">No</td>
</tr>
<tr>
<td rowspan="5"
style="text-align: center;"><strong>Payment</strong></td>
<td style="text-align: center;">Contribution base</td>
<td style="text-align: center;">n/a</td>
</tr>
<tr>
<td style="text-align: center;">Basic amount</td>
<td style="text-align: center;"><p>80% of the SSI for single benefit
units</p>
<p><strong>OR</strong></p>
<p>100% of the SSI for larger benefit units</p></td>
</tr>
<tr>
<td style="text-align: center;">Additional amount</td>
<td style="text-align: center;">Bonus of 10% x NMW per child in the
household.</td>
</tr>
<tr>
<td style="text-align: center;">Floor</td>
<td style="text-align: center;">No</td>
</tr>
<tr>
<td style="text-align: center;">Ceiling</td>
<td style="text-align: center;">No</td>
</tr>
<tr>
<td rowspan="2" style="text-align: center;"><strong>Duration in
months</strong></td>
<td style="text-align: center;">Standard</td>
<td style="text-align: center;"><em>Initial modality</em>: same as for
the insurance unemployment benefit</td>
</tr>
<tr>
<td style="text-align: center;">Special cases</td>
<td style="text-align: center;"><em>Extended modality:</em> if &lt; 40
years old, the length is half of that benefit’s length. Otherwise, it is
the same as the “initial modality”</td>
</tr>
<tr>
<td rowspan="2" style="text-align: center;"><strong>Subject
to</strong></td>
<td style="text-align: center;">Taxes</td>
<td style="text-align: center;">No</td>
</tr>
<tr>
<td style="text-align: center;">SIC</td>
<td style="text-align: center;">No</td>
</tr>
</tbody>
</table>

Source: Decreto-Lei n.º 220/2006, de 3 de novembro, as amended;
Instituto da Segurança Social (www.seg-social.pt)

### Minimum pension (*poacm_pt*)

#### Definition

The unit of analysis is the individual.

#### Eligibility conditions

Minimum pensions are guaranteed to individuals with past contributions
that retire at legal age or later and have a statutory pension amount
lower than the minimum that the pensioner is entitled.

#### Benefit amount

Minimum pensions are composed by two parts: the statutory pension and
the ‘social supplement’ (difference between the statutory and the
minimum amount). The former is financed by the Social Security budget,
while the latter is financed by the state budget. The minimum value is
fixed each year and varies with the pensioners’ working career length.
In the simulation, the variable *liwwh* (work history, in months) is
used as a proxy to the working career length. Thus, every old age
contributory pension (*poact*) in the database is ‘corrected’
accordingly to the following grid:

<span id="_Toc222328539" class="anchor"></span>**Table 2.21** Old age
contributory pension: minimum amounts \[2022-2025\] (monthly, in €)

| **Career length**  | **2022** | **2023** | **2024** | **2025** |
|--------------------|:--------:|:--------:|:--------:|:--------:|
| Less than 15 years |  278.05  |  291.48  |  319.49  |  331.79  |
| 15 to 20 years     |  291.68  |  305.77  |  335.15  |  348.05  |
| 21 to 30 years     |  321.86  |  337.41  |  369.83  |  384.07  |
| More than 30 years |  402.32  |  421.75  |  462.28  |  480.08  |

Source: Annual valorisation Orders (Portaria n.º 38/2022; Portaria n.º
97/2023; Portaria n.º 424/2023; Portaria n.º 372-B/2024) — Instituto da
Segurança Social (www.seg-social.pt)

#### EUROMOD modelling

The simulation of the old age contributory pensions is not achievable
using the available microdata, due to the lack of information on several
attributes. However, it is possible to simulate the non-contributory
pensions and, with some degree of simplification, the level of minimum
pensions. Furthermore, this methodology offers the possibility of
‘correcting’ the original data regarding the low declared old age
pension income.

This policy is switched off (*i.e.*, not executed) in the baseline, due
to its underestimating effect on elderly poverty.

### Old age social pension (*poanc_pt*)

#### Definition

The recipient is the individual, although if living with a partner, the
income of the couple is considered in the income test.

#### Eligibility conditions

Minimum age:

2022: 66 years and 7 months;

2023: 66 years and 5 months;

2024: 66 years and 5 months;

2025: 66 years and 7 months;

#### Income test

Single recipient: monthly gross income up to 40% of the SSI.

Couple: monthly gross income up to 60% of the SSI.

The framework of the old age social pension is unclear regarding which
types of income should be included in the means-test evaluation, but
they should include, at least:

<span id="_Toc222328540" class="anchor"></span>**Table 2.22** Old age
social pension (*poanc_pt*) assessed income

| **Variable** | **Label**                              |
|--------------|----------------------------------------|
| yem          | INCOME: Employment                     |
| yse          | INCOME: Self-employment                |
| bun          | BENEFIT/PENSION: Unemployment          |
| poact_s      | BENEFIT/PENSION: Old age: contributory |
| psu          | BENEFIT/PENSION: Survivors             |
| pdi          | BENEFIT/PENSION: Disability            |
| bed          | BENEFIT/PENSION: Education             |
| ypp          | INCOME: Private pension                |
| ypr          | INCOME: Property                       |
| bsaot        | Other social assistance benefits       |
| bho          | BENEFIT/PENSION: Housing               |
| yiy          | INCOME: Investment                     |
| yot          | INCOME: Other                          |

Source: Own elaboration

Important rule to consider while simulating the old age social pension
(especially when testing couples): although the social pension itself
(of the partner, in this case) amounts to the total couple income, it
should be considered only its base value. So, for example, Extraordinary
Solidarity Supplement should not be included.

#### Benefit amount

The monthly amount of the old age social pension is €255.25 in 2025.
Notwithstanding, besides that amount, every recipient receives an
Extraordinary Solidarity Supplement (‘*Complemento Extraordinário de
Solidariedade’*), that differs according to their age (€22.21 for those
aged up to 70 years old, and €44.43 for those with more than 70 years
old).

<span id="_Toc222328541" class="anchor"></span>**Table 2.23** Old age
social pension (*poanc_pt*) amounts \[2022-2025\] (monthly, in €)

<table style="width:62%;">
<colgroup>
<col style="width: 19%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"></th>
<th colspan="2" style="text-align: center;"><strong>2022</strong></th>
<th colspan="2" style="text-align: center;"><strong>2023</strong></th>
<th colspan="2" style="text-align: center;"><strong>2024</strong></th>
<th colspan="2" style="text-align: center;"><strong>2025</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"><strong>65-69</strong></td>
<td style="text-align: center;"><strong>70+</strong></td>
<td style="text-align: center;"><strong>65-69</strong></td>
<td style="text-align: center;"><strong>70+</strong></td>
<td style="text-align: center;"><strong>65-69</strong></td>
<td style="text-align: center;"><strong>70+</strong></td>
<td style="text-align: center;"><strong>65-69</strong></td>
<td style="text-align: center;"><strong>70+</strong></td>
</tr>
<tr>
<td style="text-align: center;">Old age social pension base amount</td>
<td colspan="2" style="text-align: center;">213.91</td>
<td colspan="2" style="text-align: center;">224.24</td>
<td colspan="2" style="text-align: center;">245.79</td>
<td colspan="2" style="text-align: center;">255.25</td>
</tr>
<tr>
<td style="text-align: center;">Extraordinary solidarity supplement</td>
<td style="text-align: center;">18.62</td>
<td style="text-align: center;">37.23</td>
<td style="text-align: center;">19.52</td>
<td style="text-align: center;">39.03</td>
<td style="text-align: center;">21.39</td>
<td style="text-align: center;">42.78</td>
<td style="text-align: center;">22.21</td>
<td style="text-align: center;">44.43</td>
</tr>
<tr>
<td style="text-align: center;"><strong>Sum</strong></td>
<td style="text-align: center;"><strong>232.53</strong></td>
<td style="text-align: center;"><strong>251.14</strong></td>
<td style="text-align: center;"><strong>243.76</strong></td>
<td style="text-align: center;"><strong>263.27</strong></td>
<td style="text-align: center;"><strong>267.18</strong></td>
<td style="text-align: center;"><strong>288,57</strong></td>
<td style="text-align: center;"><strong>277.46</strong></td>
<td style="text-align: center;"><strong>299.68</strong></td>
</tr>
</tbody>
</table>

Source: Annual valorisation Orders (Portaria n.º 97/2023; Portaria n.º
372-B/2024) — Instituto da Segurança Social (www.seg-social.pt)

These amounts are paid monthly and there is a 13th (in July) and 14th
(in December) extra payment in the same amounts.

#### EUROMOD modelling

The original EU-SILC py102g, py103g and py104g variables are used to
split old age benefits into old age contributory pension (*poact*) and
old age social pension (*poanc*). The values of this initial splitting
are checked to assure that the value of *poanc* cannot be higher than
the maximum value of the old age social pension.

This disaggregation should be done according to the policy rules
described before and if the original value of the variable *poa* is
within the band \[-3.5%, +3.5%\] of the individual income.

### Solidarity supplement for the elderly (*bsaoa_pt*)

#### Definition

The recipient is the individual, although if living with a partner, the
income of the couple is observed. Thus, the family unit is the
individual, if living alone, or the couple otherwise.

Equivalence scale for the recipient's ‘family unit’: 1 for the single
recipient and 1.75 for the couple. This benefit also considers a second
family unit: the household of the recipient’s children.

#### Eligibility conditions

Minimum age:

2022: 66 years and 7 months;

2023: 66 years and 5 months;

2024: 66 years and 5 months;

2025: 66 years and 7 months;

Since 2018, to compensate the penalties in early pensions since 2014, an
exception to the minimum age is granted in cases where the pensioner had
an early pension starting since January 2014 (NOT SIMULATED).
Additionally, from October 2018, invalidity pensioners who are not
recipients of the new benefit for handicapped people (‘*Prestação Social
para a Inclusão*’), may also be entitled to the solidarity supplement.

#### Income test

Single recipient: annual gross income up to the reference amount.

Couple: annual gross income up to 1.75 x reference amount. However, the
single recipient means-test must also be met.

<span id="_Toc222328542" class="anchor"></span>**Table 2.24** Solidarity
supplement for the elderly (*bsaoa_pt*): reference value (RV)
\[2022-2025\] (annual, in €)

<table style="width:64%;">
<colgroup>
<col style="width: 15%" />
<col style="width: 8%" />
<col style="width: 8%" />
<col style="width: 8%" />
<col style="width: 8%" />
<col style="width: 13%" />
</colgroup>
<thead>
<tr>
<th></th>
<th rowspan="2" style="text-align: center;"><strong>2022</strong></th>
<th rowspan="2" style="text-align: center;"><strong>2023</strong></th>
<th colspan="2" rowspan="2"
style="text-align: center;"><strong>2024</strong></th>
<th style="text-align: center;"></th>
</tr>
<tr>
<th></th>
<th style="text-align: center;"><strong>2025</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Single</td>
<td style="text-align: center;">5,258.63</td>
<td style="text-align: center;">5,858.63</td>
<td style="text-align: center;">6,608.00*</td>
<td style="text-align: center;">7.208.00**</td>
<td style="text-align: center;">7,568.00</td>
</tr>
<tr>
<td>Couple (1.75 x Single)</td>
<td style="text-align: center;">9,202.60</td>
<td style="text-align: center;">10,252.60</td>
<td style="text-align: center;">11,564.00*</td>
<td style="text-align: center;">12,614.00**</td>
<td style="text-align: center;">1,3244-00</td>
</tr>
</tbody>
</table>

Note: (\*) From 1st of January to 31st of May 2024. (\*) From 1st of
June 2024.

Source: Portaria n.º 311/2024 (2025 update); previous annual Orders —
Instituto da Segurança Social (www.seg-social.pt)

The income of both elements of the family unit (Y1 and Y2 in the formula
in Table 2-28 below) include a wide range of income variables in
EUROMOD, as listed below (although some types of income are impossible
or difficult to simulate).

<span id="_Toc222328543" class="anchor"></span>**Table 2.25** Solidarity
supplement for the elderly (*bsaoa_pt*): assessed income ‘Family
Solidarity’

| **Variable** | **Label** |
|----|----|
| Yem | INCOME: Employment |
| Yse | INCOME: Self-employment (only 65% of the amount) |
| bunct_s | BENEFIT/PENSION: Unemployment: insurance |
| bunnc_s | BENEFIT/PENSION: Unemployment: assistance |
| poact_s | BENEFIT/PENSION: Old age: contributory |
| poanc_s | BENEFIT/PENSION: Old age: non-contributory (simulated) |
| Psu | BENEFIT/PENSION: Survivors |
| Pdi | BENEFIT/PENSION: Disability |
| Bed | BENEFIT/PENSION: Education |
| Ypp | INCOME: Private pension |
| Ypr | INCOME: Property |
| bsaot | Other social assistance benefits |
| bho | BENEFIT/PENSION: Housing |
| yiy | INCOME: Investment |
| yot | INCOME: Other |
| ypt | INCOME: Private transfers |
| \- | Family solidarity (not fully simulated – see below) |
| \- | Institution attendance: annual subsidy paid by Social Security to social institutions. Impossible to simulate. |
| \- | Income imputation from wealth: 5% of the value of financial assets (when this value is higher than the investment income declared) and 5% of real estate (when this value is higher than the property income declared). Impossible to simulate. |

Source: Own elaboration

**‘Family Solidarity’**

Before 2024, this benefit also considered the income of the recipients’
children/descendants. They were evaluated within their own households
and comprise their own partners and any dependent children[^3]. However,
in 2024, this was excluded from the means test to assess the eligibility
to CSI.

Previous to 2024, the assessment of children/descendants’ income was
done as follows:

1.  The types of income of the recipients’ descendants that are
    evaluated are:

<!-- -->

4.  Then, the household’s total income is equivalised through an ‘OECD
    modified’ resembling scale of equivalence (1 for the first adult,
    0.5 for other adults with more than 18 years old, and 0.3 for every
    child aged 0-17). The computed equivalent income is then used to
    position the descendant on a scale.

5.  If the income level of each recipients’ descendants is high enough –
    if it is included in the 4th rank (above 5 x reference value) –, the
    parent/recipient is automatically excluded from the Solidarity
    Supplement for the elderly. If the income of the recipients’
    children/descendants is included up to the 3rd rank (\< 5 x
    reference value), the FS is 0%.

6.  One important remark: the FS only happens when a parent is a
    recipient. For example, if an elderly couple have a daughter
    together, but only the wife is a recipient, then she will only
    “generate” the FS to her mother.

<span id="_Toc222328544" class="anchor"></span>**Table 2.26** Solidarity
supplement for the elderly (*bsaoa_pt*): assessed income (Family
Solidarity)

| **Variable** | **Label**                        |
|--------------|----------------------------------|
| yem          | INCOME: Employment               |
| yse          | INCOME: Self-employment          |
| poa          | BENEFIT/PENSION: Old age         |
| psu          | BENEFIT/PENSION: Survivors       |
| pdi          | BENEFIT/PENSION: Disability      |
| bed          | BENEFIT/PENSION: Education       |
| ypp          | INCOME: Private pension          |
| ypt          | INCOME: Private transfers        |
| ypr          | INCOME: Property                 |
| bsaot        | Other social assistance benefits |
| bho          | BENEFIT/PENSION: Housing         |

Source: Own elaboration

#### Benefit amount

The amount paid is the difference between the reference value (see Table
2-20) and the annual income of the recipient. Calculations are simple
when the recipient lives alone, but complicated when living in couples:

When there is only one recipient in the couple, the amount paid is the
minimum of two values: the difference between the reference value and
the actual individual income of the recipient (or half of the actual
income of the couple), and the difference between the ‘total equivalent
reference value’ (€7,568.00 x 1.75 in 2025) and the couple's total
income.

When both are recipients, the amount paid is given by the difference
between the ‘total equivalent reference value’ and the couple's total
income. This amount is then divided between the two recipients according
to specific rules.

<span id="_Toc222328545" class="anchor"></span>**Table 2.27** Solidarity
supplement for the elderly (*bsaoa_pt*): Family Solidarity scale
\[2022-2025\]

<table style="width:63%;">
<colgroup>
<col style="width: 53%" />
<col style="width: 9%" />
</colgroup>
<thead>
<tr>
<th></th>
<th rowspan="2" style="text-align: center;"><strong>Rank</strong></th>
</tr>
<tr>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>Below or equal to 2.5 x reference value (RV)</td>
<td style="text-align: center;">1<sup>st</sup></td>
</tr>
<tr>
<td>Between 2.5 and 3.5 x RV</td>
<td style="text-align: center;">2<sup>nd</sup></td>
</tr>
<tr>
<td>Between 3.5 and 5 x RV</td>
<td style="text-align: center;">3<sup>rd</sup></td>
</tr>
<tr>
<td>Above 5 x RV</td>
<td style="text-align: center;">4<sup>th</sup></td>
</tr>
</tbody>
</table>

Source: Decreto-Lei n.º 232/2005, de 29 de dezembro, as amended —
Instituto da Segurança Social (www.seg-social.pt)

<span id="_Toc222328546" class="anchor"></span>**Table 2.28**
Calculation of the solidarity supplement for the elderly (*bsaoa_pt*)

| Single recipient:       |                                         
                           ``` math                                 
                           amount = RV - Y_{1}                      
                           ```                                      |
|-------------------------|-----------------------------------------|
| Couple, one recipient:  |                                         
                           ``` math                                 
                           amount = \min\left\{ \begin{matrix}      
                           RV - Y_{1} \\                            
                           RV \times 1.75 - Y_{1} - Y_{2}           
                           \end{matrix} \right.\                    
                           ```                                      |
| Couple, two recipients: |                                         
                           ``` math                                 
                           amount = RV \times 1.75 - Y_{1} - Y_{2}  
                           ```                                      |

Note: Y1 is the total individual income of the sole recipient or of the
first recipient in a couple where both are recipients, while Y2 is the
total individual income of the partner or second recipient in the
couple. RV is the reference value. Y1 and Y2 include the FS, but only in
the case of the recipients.

Source: Decreto-Lei n.º 232/2005, de 29 de dezembro, as amended; EUROMOD
Y16, authors' calculations

The solidarity supplement for the elderly is paid monthly, twelve times
a year.

#### EUROMOD modelling

The EU-SILC hy060g variable (*social exclusion not elsewhere
classified*) contains information about several benefits: solidarity
supplement for the elderly, social integration income and others.

In EU-SILC UDB hy06g, hy062g and hy064g are missing and have the
flag=-2. This implies that hy060g = hy063g and all the hy060g amount is
non-contributive and means-tested. The option is to split *bsa* into
*bsaoa* and *bsa00* and make *bsaot*=0 for all cases.

The solidarity supplement for the elderly is the first variable to get
from the split, considering the rules of this policy. Basically, for
households with a positive amount of this variable (*bsa* \> 0) and with
at least one person within the legal retirement age or more, the
expected amount of solidarity supplement for the elderly is calculated.
If the original value (*bsa*) is greater or equal to that expected
amount, then the solidarity supplement is equal to that amount,
otherwise it is equal to the original value of *bsa*.

Given the impossibility of simulating all means-tested conditions of the
non-resident descendants, the simulation overestimates the number of
recipients and the benefit amounts. Thus, we have introduced a
calibration and take up adjustment. BTA and BCA extensions are off, so
the baseline model neither adjusts for non-take-up of the benefit nor
calibrates its receipt, but the user can activate them if necessary. See
section 2.4 for technical details on both extensions and their
interactions. 

Users can enable the necessary extensions in Country Tools/Set Switches.
For proper functioning, the extensions require the following inputs: 

BTA: The estimated take-up rate of the benefit should be set as the
value of the \$bsaoa_BTA_rate constant in the model. Currently, the
value is set to 1, indicating no adjustment for non-take-up. 

BCA: The aggregate expenditure to be filled out in the External
Statistics table, so that the calibration rate (\$bsaoa_BCA_rate) is
computed accordingly. Data are currently available for the years
2016-2023; given the absence of information for 2024, the calibration
rate is not computed within the 2024 system, but the one computed within
the 2023 system is used instead. For the modelling of reforms, the 2024
system should be used in order to allow for variation in the number of
beneficiaries (hence expenditure): beneficiaries will change when the
eligibility conditions change by applying the share of 2023 to the new
pool of eligible units. If previous systems were used for reforms, total
expenditure would remain constant irrespective of the reform applied,
since the model would always stick to the existing external statistics. 

### Social integration income (*bsa00_pt*)

#### Definition

The unit of analysis is the family. This unit comprises:

The head of the family;

His/her partner;

All his/her under-18 relatives;

Other direct descendants of the head aged 18+ that are his dependents.
Dependency is defined by having an income level up to 70% of the social
pension.

Equivalence scale for income evaluation: 1 for the first adult (aged
18+); 0.7 for each additional adult; 0.5 for each child.

#### Eligibility conditions

Individuals of all ages. However, the head of the family must be an
adult (aged 18 or older).

#### Income test

The family’s total income must be lower than their ‘Social Integration
Income (SII) value’, which is equal to the scale of equivalence
multiplied by the SII reference amount (€242.23in 2025).

There is also a specific test on financial assets, which must be less
than 60 x SSI (NOT SIMULATED).

<span id="_Toc222328547" class="anchor"></span>**Table 2.29** Social
integration income (*bsa00_pt*): assessed income

| **Variable** | **Label**                                              |
|--------------|--------------------------------------------------------|
| yem          | INCOME: Employment (only 80% of the amount)            |
| yse          | INCOME: Self-employment (only 80% of the amount)       |
| bunct_s      | BENEFIT/PENSION: Unemployment: insurance               |
| bunnc_s      | BENEFIT/PENSION: Unemployment: assistance              |
| poact_s      | BENEFIT/PENSION: Old age: contributory                 |
| poanc_s      | BENEFIT/PENSION: Old age: non-contributory (simulated) |
| psu          | BENEFIT/PENSION: Survivors                             |
| pdi          | BENEFIT/PENSION: Disability                            |
| bed          | BENEFIT/PENSION: Education                             |
| ypp          | INCOME: Private pension                                |
| ypt          | INCOME: Private transfers                              |
| ypr          | INCOME: Property                                       |
| yiy          | INCOME: Investment                                     |
| yot          | INCOME: Other                                          |

Source: Own elaboration

#### Benefit amount

The amount paid results from the difference between the ‘SII value’ and
the family’s total income. The SII is paid in a monthly basis, twelve
times a year.

Other modifications (beyond the equivalence scale and threshold) not
documented here, can affect the benefits claiming, renewal and
administrative processes, and may have a negative impact on the number
of recipients, such as:

New rules for new claims and renewals of the SII may increase the
bureaucratic process and create additional difficulties to families,
leading to an increase in non-take-up and exit issues.

Increased emphasis in inspection checks to combat fraudulent claims.

Individuals must now follow stricter rules concerning their integration
programs. If an individual fails to attend a Social Security services
meeting without reasonable motive, the benefit is cancelled.

Individuals who live in institutions funded by the state (including
jail) are no longer eligible.

#### EUROMOD modelling

SII is just one of the possible benefits included in the original
variable hy060g. Previously, solidarity supplement for the elderly has
been extracted by estimation from hy060g. The difference between *bsa*
and *bsaoa* is attributed to *bsa00*.

BTA and BCA extensions are off, so the baseline model neither adjusts
for non-take-up of the benefit nor calibrates its receipt, but the user
can activate them if necessary. See section 2.4 for technical details on
both extensions and their interactions. 

Users can enable the necessary extensions in Country Tools/Set Switches.
For proper functioning, the extensions require the following inputs: 

BTA: The estimated take-up rate of the benefit should be set as the
value of the \$bsa00_BTA_rate constant in the model. Currently, the
value is set to 1, indicating no adjustment for non-take-up. 

BCA: The aggregate expenditure to be filled out in the External
Statistics table, so that the calibration rate (\$bsa00_BCA_rate) is
computed accordingly. Data are currently available for the years
2016-2023; given the absence of information for 2024, the calibration
rate is not computed within the 2024 system, but the one computed within
the 2023 system is used instead. For the modelling of reforms, the 2024
system should be used in order to allow for variation in the number of
beneficiaries (hence expenditure): beneficiaries will change when the
eligibility conditions change by applying the share of 2023 to the new
pool of eligible units. If previous systems were used for reforms, total
expenditure would remain constant irrespective of the reform applied,
since the model would always stick to the existing external statistics. 

### Child benefit (*bch_pt*)

#### Definition

The unit of analysis is the family. The recipients are the children. The
number of recipients is the only data needed for the equivalence scale
calculations, although the family income is also observed.

It assumes a wider concept of benefit unit than the one that is
generally used. The *de facto benefit* unit is a tax unit including the
recipient child (or children), siblings, parents, tutors, and
stepparents.

Equivalence scale for income evaluation: 1 for each recipient plus one
(e.g., the income of a family with 2 recipient children is divided by
3).

#### Eligibility conditions

Children up to 16 years old. It can be extended to individuals up to 24
years under certain conditions:

Aged between 16 and 18: if attending primary education (1st to 6th
grade) or higher.

Aged between 18 and 21: if attending secondary education (7th to 12th
grade) or higher.

Aged between 21 and 24: if attending higher/superior education.

Also until 24 years old: if disabled children and receiving disability
allowance (not simulated), and children not working.

#### Income test

The annual ‘reference income’ cannot exceed 2.5 x 14 x SSI. It results
from the total annual family unit income divided by the total number of
recipients plus one. According to the ‘reference income’, families are
ranked along four income brackets:

<span id="_Toc222328548" class="anchor"></span>**Table 2.30** Child
benefit (*bch_pt*) income brackets upper bounds (1) \[2022-2025\]

<table style="width:64%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 11%" />
<col style="width: 9%" />
<col style="width: 9%" />
<col style="width: 9%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"></th>
<th colspan="4"
style="text-align: center;"><strong>Formula</strong></th>
<th style="text-align: center;"><strong>Value</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><strong>Income bracket</strong></td>
<td style="text-align: center;"><strong>2022</strong></td>
<td style="text-align: center;"><strong>2023</strong></td>
<td style="text-align: center;"><strong>2024</strong></td>
<td style="text-align: center;"><strong>2025</strong></td>
<td style="text-align: center;"><strong>2025
<sup>(1)</sup></strong></td>
</tr>
<tr>
<td style="text-align: center;">1<sup>st</sup></td>
<td colspan="4" style="text-align: center;">0.5 x 14 x SSI</td>
<td style="text-align: center;">€3,363.01</td>
</tr>
<tr>
<td style="text-align: center;">2<sup>nd</sup></td>
<td colspan="4" style="text-align: center;">1.0 x 14 x SSI</td>
<td style="text-align: center;">€6,726.02</td>
</tr>
<tr>
<td style="text-align: center;">3<sup>rd</sup></td>
<td style="text-align: center;"></td>
<td colspan="3" style="text-align: center;">1.7 x 14 x SSI</td>
<td style="text-align: center;">€11,434.23</td>
</tr>
<tr>
<td style="text-align: center;">4<sup>th</sup></td>
<td colspan="4" style="text-align: center;">2.5 x 14 x SSI</td>
<td style="text-align: center;">€16,815.05</td>
</tr>
</tbody>
</table>

Note: (1) The Income Brackets are based on the value of the SSI in the
reference year which is used to assess the eligibility to the benefit.
This means that, in 2025 the values of the Child Benefit’s Income
Brackets are based on the value of the SSI in 2024.

Source: Decreto-Lei n.º 176/2003, de 2 de agosto, as amended — Instituto
da Segurança Social (www.seg-social.pt)

<span id="_Toc222328549" class="anchor"></span>**Table 2.31** Child
benefit (*bch_pt*): assessed income

| **Variable** | **Label**                                               |
|--------------|---------------------------------------------------------|
| Yem          | INCOME: Employment                                      |
| yse          | INCOME: Self-employment (70% of earnings, 20% of sales) |
| bunct_s      | BENEFIT/PENSION: Unemployment: insurance                |
| bunnc_s      | BENEFIT/PENSION: Unemployment: assistance               |
| poact_s      | BENEFIT/PENSION: Old age: contributory                  |
| poanc_s      | BENEFIT/PENSION: Old age: non-contributory (simulated)  |
| bsaoa_s      | BENEFIT/PENSION: Solidarity supplement for the elderly  |
| bsa00_s      | BENEFIT/PENSION: Social integration income              |
| psu          | BENEFIT/PENSION: Survivors                              |
| pdi          | BENEFIT/PENSION: Disability                             |
| bed          | BENEFIT/PENSION: Education                              |
| ypp          | INCOME: Private pension                                 |
| ypr          | INCOME: Property                                        |
| yiy          | INCOME: Investment                                      |
| yot          | INCOME: Other                                           |

Source: Own elaboration

#### Benefit amount

The amount paid every month depends on the child’s age and on the income
bracket of the child’s family.

<span id="_Toc222328550" class="anchor"></span>**Table 2.32** Child
benefit (*bch_pt*) amounts \[2022\] (monthly, in €)

<table style="width:62%;">
<colgroup>
<col style="width: 9%" />
<col style="width: 7%" />
<col style="width: 10%" />
<col style="width: 8%" />
<col style="width: 8%" />
<col style="width: 11%" />
<col style="width: 8%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"></th>
<th colspan="3" style="text-align: center;"><strong>From January to
June</strong></th>
<th colspan="3" style="text-align: center;"><strong>From July to
December</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><strong>Income bracket</strong></td>
<td style="text-align: center;"><strong>&lt;=36 months</strong></td>
<td style="text-align: center;"><strong>&gt;36 and &lt;=72
months</strong></td>
<td style="text-align: center;"><strong>&gt;72 months</strong></td>
<td style="text-align: center;"><strong>&lt;=36 months</strong></td>
<td style="text-align: center;"><strong>&gt;36 and &lt;=72
months</strong></td>
<td style="text-align: center;"><strong>&gt;72 months</strong></td>
</tr>
<tr>
<td style="text-align: center;">1<sup>st</sup></td>
<td style="text-align: center;">149.85</td>
<td style="text-align: center;">49.95</td>
<td style="text-align: center;">37.46</td>
<td style="text-align: center;">149.85</td>
<td style="text-align: center;">50.00</td>
<td style="text-align: center;">41.00</td>
</tr>
<tr>
<td style="text-align: center;">2<sup>nd</sup></td>
<td style="text-align: center;">123.69</td>
<td style="text-align: center;">41.23</td>
<td style="text-align: center;">30.93</td>
<td style="text-align: center;">123.69</td>
<td style="text-align: center;">50.00</td>
<td style="text-align: center;">41.00</td>
</tr>
<tr>
<td style="text-align: center;">3<sup>rd</sup></td>
<td style="text-align: center;">97.31</td>
<td style="text-align: center;">32.44</td>
<td style="text-align: center;">28.00</td>
<td style="text-align: center;">97.31</td>
<td style="text-align: center;">32.44</td>
<td style="text-align: center;">28.00</td>
</tr>
<tr>
<td style="text-align: center;">4<sup>th</sup></td>
<td style="text-align: center;">58.39</td>
<td style="text-align: center;">19.46</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">58.39</td>
<td style="text-align: center;">19.46</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Note: in EUROMOD it is used the average amounts referring to the two
semesters.

Source: Portaria n.º 76/2022 (Jan–Jun); Portaria n.º 268/2022 (Jul–Dec)
— Instituto da Segurança Social (www.seg-social.pt)

<span id="_Toc222328551" class="anchor"></span>**Table 2.33** Child
benefit (*bch_pt*) amounts \[2023\] (monthly, in €)

| **Income bracket** | **\<=36 months** | **\>36 and \<=72 months** | **\>72 months** |
|:--:|:--:|:--:|:--:|
| 1<sup>st</sup> | 161.03 | 50.00 | 50.00 |
| 2<sup>nd</sup> | 132.92 | 50.00 | 50.00 |
| 3<sup>rd</sup> | 104.57 | 34.86 | 30.09 |
| 4<sup>th</sup> | 62.75 | 20.91 | \- |

Source: Annual amounts Order for 2023 — Instituto da Segurança Social
(www.seg-social.pt)

<span id="_Toc222328552" class="anchor"></span>**Table 2.34** Child
benefit (*bch_pt*) amounts \[2024\] (monthly, in €)

| **Income bracket** | **\<=36 months** | **\>36 and \<=72 months** | **\>72 months** |
|:--:|:--:|:--:|:--:|
| 1<sup>st</sup> | 183.03 | 72.00 | 72.00 |
| 2<sup>nd</sup> | 154.92 | 72.00 | 72.00 |
| 3<sup>rd</sup> | 126.57 | 56.86 | 52.09 |
| 4<sup>th</sup> | 84.75 | 42.91 | \- |

Source: Annual amounts Order for 2024 (OE 2024 update) — Instituto da
Segurança Social (www.seg-social.pt)

<span id="_Toc222328553" class="anchor"></span>**Table 2.35** Child
benefit (*bch_pt*) amounts \[2025\] (monthly, in €)

| **Income bracket** | **\<=36 months** | **\>36 and \<=72 months** | **\>72 months** |
|:--:|:--:|:--:|:--:|
| 1<sup>st</sup> | 186.87 | 73.51 | 73.51 |
| 2<sup>nd</sup> | 158.17 | 73.51 | 73.51 |
| 3<sup>rd</sup> | 129.23 | 58.05 | 53.18 |
| 4<sup>th</sup> | 86.53 | 43.81 | \- |

Source: Annual amounts Order for 2025 — Instituto da Segurança Social
(www.seg-social.pt)

**Supplement for large families:** In 2022, every child up to 36 months
entitled to the benefit with one other sibling, received an additional
amount equal to what a child aged 36+ receive in the same income
bracket, and if the child had two or more other siblings, the additional
amount was equal to two times what a child aged 36+ receive in the same
income bracket. As of 2023, the following supplements apply:

<span id="_Toc222328554" class="anchor"></span>**Table 2.36** Child
benefit (*bch_pt*): supplement for large families \[2025\] (monthly, in
€)

| **Income bracket** | **2 children** | **2+ children** |
|:------------------:|:--------------:|:---------------:|
|   1<sup>st</sup>   |     63.56      |     104.66      |
|   2<sup>nd</sup>   |      56.4      |      90.33      |
|   3<sup>rd</sup>   |     53.18      |      83.91      |
|   4<sup>th</sup>   |     38.43      |      54.5       |

Source: Decreto-Lei n.º 176/2003, as amended — Instituto da Segurança
Social (www.seg-social.pt)

**Bonus for lone parent families:** 35% increase in the above amounts in
2022. For 2023 and, the increase is of 50% for the 1st income bracket
and 42.5% for the 2nd, 3rd and 4th income brackets. For 2024 and 2025,
the increase is of 50% for all income brackets.

**Number of payments:** the child benefit is paid in a monthly basis,
twelve times a year. There is an extra payment (of the same amount) in
September, for children that fulfil the following conditions:

The child’s heir family is in the 1st income bracket.

The child is between 6 and 16 years old (age attained during the civil
year);

The child attends school.

**Education allowance:** twice the amount of the benefit that the child
is receiving. Conditions that must be fully observed:

The family income bracket is the 1st or the 2nd.

The child is attending the 10-12th grade.

The child’s age is less than 18 years (can be 18 if that age is attained
during the school year).

The child has school success. (NOT SIMULATED)

**Child Guarantee:** since July 2022, a new supplement is in place, the
Child Guarantee (‘*Garantia para a Infância*’), aimed at children under
the age of 18, recipients of the child benefit and belonging to
households that are in extreme poverty (*i.e.*, placed in the 1st income
bracket). This support consists of a benefit that complements the child
benefit in order to guarantee the payment of a total amount (including
the child benefit amount) of €70 in 2022, €100 in 2023, €122 in 2024 and
€124.56 in 2024.

<span id="_Toc222328555" class="anchor"></span>**Table 2.37** Child
Benefit (*bch_pt*): Child Guarantee \[2022\] (Reference Amount, and
Differential Payment, in €)

<table style="width:64%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Income bracket</strong></th>
<th style="text-align: center;"><strong>Age</strong></th>
<th style="text-align: center;"><p><strong>Child</strong></p>
<p><strong>Benefit</strong></p></th>
<th colspan="2" style="text-align: center;"><strong>Child
Guarantee</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p><strong>Reference Amount</strong></p>
<p><strong>(Monthly)</strong></p></td>
<td style="text-align: center;"><strong>Differential
Payment</strong></td>
</tr>
<tr>
<td style="text-align: center;">1st</td>
<td style="text-align: center;">≤ 32 months</td>
<td style="text-align: center;">149.85</td>
<td style="text-align: center;">70*</td>
<td style="text-align: center;">0</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt; 32 months &amp;≤ 32 months</td>
<td style="text-align: center;">50.00</td>
<td style="text-align: center;">70*</td>
<td style="text-align: center;">20</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;72 months</td>
<td style="text-align: center;">41.00</td>
<td style="text-align: center;">70*</td>
<td style="text-align: center;">29</td>
</tr>
<tr>
<td style="text-align: center;">2nd</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td style="text-align: center;">3rd</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td style="text-align: center;">4th</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Note: (\*) Based on an annual reference amount of €840, for 6 months.

Source: Resolução do Conselho de Ministros n.º 110-A/2022 (Garantia para
a Infância) — Instituto da Segurança Social (www.seg-social.pt)

<span id="_Toc222328556" class="anchor"></span>**Table 2.38** Child
Benefit (*bch_pt*): Child Guarantee \[2023\] (Reference Amount, and
Differential Payment, in €)

<table style="width:64%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Income bracket</strong></th>
<th style="text-align: center;"><strong>Age</strong></th>
<th style="text-align: center;"><p><strong>Child</strong></p>
<p><strong>Benefit</strong></p></th>
<th colspan="2" style="text-align: center;"><strong>Child
Guarantee</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p><strong>Reference Amount</strong></p>
<p><strong>(Monthly)</strong></p></td>
<td style="text-align: center;"><strong>Differential
Payment</strong></td>
</tr>
<tr>
<td style="text-align: center;">1st</td>
<td style="text-align: center;">≤ 32 months</td>
<td style="text-align: center;">161.03</td>
<td style="text-align: center;">100</td>
<td style="text-align: center;">0</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt; 32 months &amp;≤ 32 months</td>
<td style="text-align: center;">50.00</td>
<td style="text-align: center;">100</td>
<td style="text-align: center;">50</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;72 months</td>
<td style="text-align: center;">41.00</td>
<td style="text-align: center;">100</td>
<td style="text-align: center;">59</td>
</tr>
<tr>
<td style="text-align: center;">2nd</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td style="text-align: center;">3rd</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td style="text-align: center;">4th</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Note: (\*) Based on an annual reference amount of €1200.

Source: Resolução do Conselho de Ministros n.º 110-A/2022, as extended
for 2023 — Instituto da Segurança Social (www.seg-social.pt)

<span id="_Toc222328557" class="anchor"></span>**Table 2.39** Child
Benefit (*bch_pt*): Child Guarantee \[2024\] (Reference Amount, and
Differential Payment, in €)

<table style="width:64%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Income bracket</strong></th>
<th style="text-align: center;"><strong>Age</strong></th>
<th style="text-align: center;"><p><strong>Child</strong></p>
<p><strong>Benefit</strong></p></th>
<th colspan="2" style="text-align: center;"><strong>Child
Guarantee</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p><strong>Reference Amount</strong></p>
<p><strong>(Monthly)</strong></p></td>
<td style="text-align: center;"><strong>Differential
Payment</strong></td>
</tr>
<tr>
<td style="text-align: center;">1st</td>
<td style="text-align: center;">≤ 32 months</td>
<td style="text-align: center;">183.03</td>
<td style="text-align: center;">122*</td>
<td style="text-align: center;">0</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt; 32 months &amp;≤ 32 months</td>
<td style="text-align: center;">72.00</td>
<td style="text-align: center;">122*</td>
<td style="text-align: center;">50</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;72 months</td>
<td style="text-align: center;">72.00</td>
<td style="text-align: center;">122*</td>
<td style="text-align: center;">50</td>
</tr>
<tr>
<td style="text-align: center;">2nd</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td style="text-align: center;">3rd</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td style="text-align: center;">4th</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Note: (\*) Based on an annual reference amount of €1464.

Source: Child Guarantee extension for 2024 (OE 2024) — Instituto da
Segurança Social (www.seg-social.pt)

<span id="_Toc222328558" class="anchor"></span>**Table 2.40** Child
Benefit (*bch_pt*): Child Guarantee \[2025\] (Reference Amount, and
Differential Payment, in €)

<table style="width:64%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Income bracket</strong></th>
<th style="text-align: center;"><strong>Age</strong></th>
<th style="text-align: center;"><p><strong>Child</strong></p>
<p><strong>Benefit</strong></p></th>
<th colspan="2" style="text-align: center;"><strong>Child
Guarantee</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p><strong>Reference Amount</strong></p>
<p><strong>(Monthly)</strong></p></td>
<td style="text-align: center;"><strong>Differential
Payment</strong></td>
</tr>
<tr>
<td style="text-align: center;">1st</td>
<td style="text-align: center;">≤ 32 months</td>
<td style="text-align: center;">186.87</td>
<td style="text-align: center;">124.60*</td>
<td style="text-align: center;">0</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt; 32 months &amp;≤ 32 months</td>
<td style="text-align: center;">73.51</td>
<td style="text-align: center;">124.60*</td>
<td style="text-align: center;">51.09</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;72 months</td>
<td style="text-align: center;">73.51</td>
<td style="text-align: center;">124.60*</td>
<td style="text-align: center;">51.09</td>
</tr>
<tr>
<td style="text-align: center;">2nd</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td style="text-align: center;">3rd</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td style="text-align: center;">4th</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Note: (\*) Based on an annual reference amount of €1495.

Source: Child Guarantee extension for 2025 (OE 2025) — Instituto da
Segurança Social (www.seg-social.pt)

#### EUROMOD modelling

The EU-SILC variable hy050g (family/children related allowances)
contains information regarding two benefits: child benefit (*bch*) and
other family/children related allowances (*bfa*). The identification of
the *bch* variable was done using the information of the EU-SILC
variable hy053g (family/children-related allowances non-contributory and
means-tested). The remains components of the variable hy050g were
affected to *bfa*.

### Prenatal family allowance (*bmapr_pt*)

#### Brief description

A pregnant woman receives the benefit. It is an allowance attributed to
the pregnant woman from the 13th week of gestation, which aims to
encourage motherhood by compensating for the increased costs during the
period of pregnancy. The applicant cannot have a reference income higher
than 1.7 x SSI x 14.

#### Definition

The unit of analysis is the family.

#### Eligibility conditions

Have reached the 13th week of gestation.

Be resident in Portugal or equivalent to a resident.

Have the reference income equal to or less than the value established
for the 5th income bracket (equal to or less than 2.5 x SSI x 14).

Do not have financial capital more than 240 x SSI.

#### Income test

The assessment of eligibility is based on the households’ reference
income. The reference income is calculated by summing the total income
of all family members in the year previous to the application to the
Prenatal Family Allowance, divided by the number of children and young
people entitled to the family allowance in that same household plus one
and the number of unborn children.

The decision on eligibility is made by reference to income brackets,
computed by reference to the value of the SSI in the year of the
reference income.

<span id="_Toc222328559" class="anchor"></span>**Table 2.41** Prenatal
family allowance (*bmapr_pt*) income brackets \[2022-2025\]

<table style="width:64%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 8%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"></th>
<th colspan="4"
style="text-align: center;"><strong>Formula</strong></th>
<th style="text-align: center;"><strong>Value</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><strong>Income bracket</strong></td>
<td style="text-align: center;"><strong>2022</strong></td>
<td style="text-align: center;"><strong>2023</strong></td>
<td style="text-align: center;"><strong>2024</strong></td>
<td style="text-align: center;"><strong>2025</strong></td>
<td style="text-align: center;"><strong>2025
<sup>(1)</sup></strong></td>
</tr>
<tr>
<td style="text-align: center;">1<sup>st</sup></td>
<td colspan="4" style="text-align: center;">0.5 x 14 x SSI</td>
<td style="text-align: center;">€3564.8</td>
</tr>
<tr>
<td style="text-align: center;">2<sup>nd</sup></td>
<td colspan="4" style="text-align: center;">1.0 x 14 x SSI</td>
<td style="text-align: center;">€7129.6</td>
</tr>
<tr>
<td style="text-align: center;">3<sup>rd</sup></td>
<td style="text-align: center;"></td>
<td colspan="3" style="text-align: center;">1.75 x 14 x SSI</td>
<td style="text-align: center;">€12120.4</td>
</tr>
<tr>
<td style="text-align: center;">4<sup>th</sup></td>
<td colspan="4" style="text-align: center;">2.5 x 14 x SSI</td>
<td style="text-align: center;">€17,824.1</td>
</tr>
</tbody>
</table>

Note: <sup>(1)</sup> The Income Brackets are based on the value of the
SSI in the reference year which is used to assess the eligibility to the
benefit. This means that, in 2025 the values of the Child Benefit’s
Income Brackets are based on the value of the SSI in 2024.

Source: Decreto-Lei n.º 176/2003, de 2 de agosto, as amended — Instituto
da Segurança Social (www.seg-social.pt)

<span id="_Toc222328560" class="anchor"></span>**Table 2.42** Prenatal
family allowance (*bmapr_pt*): assessed income

| **Variable** | **Label**                                              |
|--------------|--------------------------------------------------------|
| yem          | INCOME: Employment                                     |
| yse          | INCOME: Self-employment                                |
| bunct_s      | BENEFIT/PENSION: Unemployment: insurance               |
| bunnc_s      | BENEFIT/PENSION: Unemployment: assistance              |
| poact_s      | BENEFIT/PENSION: Old age: contributory                 |
| poanc_s      | BENEFIT/PENSION: Old age: non-contributory             |
| psu          | BENEFIT/PENSION: Survivors                             |
| bsaoa_s      | BENEFIT/PENSION: Solidarity supplement for the elderly |
| bsa00_s      | BENEFIT/PENSION: Social integration income             |
| bsaot        | BENEFIT/PENSION: Other social assistance benefits      |
| bho          | BENEFIT/PENSION: Housing benefits                      |
| bed          | BENEFIT/PENSION: Education                             |
| ypp          | INCOME: Private pension                                |
| ypt          | INCOME: Private transfers                              |
| ypr          | INCOME: Property                                       |
| yiy          | INCOME: Investment                                     |
| yot          | INCOME: Other                                          |

Source: Own elaboration

#### Benefit amount

The prenatal family allowance is assigned for 6 months, from the month
following that in which the 13th week of pregnancy is reached.

If the period of pregnancy is:

Over 40 weeks, it is attributed for 6 months or until the month of
birth, inclusive.

Less than 40 weeks, it is attributed for 6 months, and can be
accumulated with the child benefit after birth.

If an interruption of pregnancy occurs, it is attributed until the month
of termination of pregnancy.

The amount of prenatal family allowance is variable based on the
reference income of the household and corresponds to the amount of child
benefit in the first year of life. It is increased by 35% in single
parenting situations.

<span id="_Toc222328561" class="anchor"></span>**Table 2.43** Prenatal
family allowance (*bmapr_pt*) amounts \[2022-2025\] (monthly, in €)\*

| **Income bracket** | **2022** | **2023** | **2024** | **2025** |
|:------------------:|:--------:|:--------:|:--------:|:--------:|
|   1<sup>st</sup>   |  149.85  |  161.03  |  183.03  |  186.87  |
|   2<sup>nd</sup>   |  123.69  |  132.92  |  154.92  |  158.17  |
|   3<sup>rd</sup>   |  97.31   |  104.57  |  126.57  |  129.23  |
|   4<sup>th</sup>   |  58.39   |  62.75   |  84.75   |  86.53   |

Note: \* The amounts in case of twins are doubled (tripled if triplets).

Source: Instituto da Segurança Social (www.seg-social.pt) \[amounts
equal to bch_pt 1st-year amounts by income bracket\]

#### Subject to taxes/SIC

Not taxable. Not subject to SICs.

#### EUROMOD modelling

This benefit will only be simulated since 2015. The simulation is,
however, switched off as part of the baselines, i.e., non-simulated
components (*bfa*) are being used.

The benefit can only be simulated for those women who already gave birth
and therefore could be eligible for the allowance for up to 6 months
before the childbirth during each policy year. The duration of this
allowance depends on the month of birth of the child.

### Parental allowance (*bplct_pt*)

#### Brief description

This benefit is intended for citizens’ beneficiaries of the Social
Security system and is intended to replace the lost work income (of the
mother and/or the father) during the period of childbirth leave. It is
not compatible with work income and unemployment benefits (that will be
suspended while receiving the parental allowance). There are different
concession periods considering the different modalities that this
allowance comprises.

#### Definition

This benefit is intended for citizens:

Beneficiaries of the Social Security system covered by the
employees/self-employed/voluntary social insurance scheme;

Beneficiaries in pre-retirement status who carry out an activity under
any of the aforementioned schemes;

Beneficiaries receiving unemployment benefits (insurance and
assistance);

Beneficiaries who receive a relative disability pension or survivor’s
pension and that are working and with records of remuneration in the
Social Security.

This allowance comprises several modalities (which have different
concession periods):

**Initial parental allowance:** attributed for a period up to 120 or 150
consecutive days, according to the parents’ option. This period can be
extended by 30 days in cases of shared license or birth of twins (for
each twin, in addition to the first).

**Mother’s exclusive initial parental allowance:** assigned to the
mother for a period up to 72 days (30 days, at most, before childbirth
and 42 mandatory days immediately after delivery). This period is
included in period corresponding to the initial parental allowance.

**Father’s exclusive initial parental allowance:** assigned to the
father for a period of 20 mandatory working days (of which 5 immediately
after the birth and 15 within 6 weeks of the birth) and 5 optional
working days (consecutive or not) which must be taken after the 20
mandatory days and within the period of the mother’s maternity leave.
This period is additional to the initial parental allowance.

**Initial parental allowance of one parent in the event of impossibility
of the other:** assigned to the father or mother in the event of
physical or mental incapacity, or death of one of them, for the period
of the initial parental allowance which the other parent lacked.

#### Eligibility conditions

Have a minimum period of contributions of at least 6 months.

Enjoy the respective licenses, absences and unpaid waivers under the
Labour Code or equivalent periods.

Have Social Security contributions paid by the end of the third month
immediately preceding the month in which the parents leave work for the
birth child (if self-employed person or if covered by the voluntary
social insurance scheme).

#### Income test

This is not a means-tested benefit.

#### Benefit amount

The daily amount of the allowance is calculated by applying a percentage
to the amount of the beneficiary’s reference remuneration (RR), defined
by:

RR = R/180, where R is equal to the total of the salaries registered in
Social Security in the first six calendar months immediately preceding
the second month preceding the beginning of the incapacity for work; or

RR = R/(30 x n) if there is no remuneration record in that six-month
period because there has been a totalization of taxable periods, and
where R is equal to the total remuneration recorded in Social Security
since the beginning of the reference to the day before the impediment to
work, and n is the number of months to which they report.

<span id="_Toc222328562" class="anchor"></span>**Table 2.44** Parental
allowance (*bplct_pt*) amounts \[2022-2025\]

<table style="width:51%;">
<colgroup>
<col style="width: 32%" />
<col style="width: 18%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Periods of
concession</strong></th>
<th style="text-align: center;"><strong>Monthly amounts</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>120 days of leave</p>
<p>150 days of shared leave (120 + 30)</p>
<p>30 additional days for each twin (plus the first)</p>
<p>Days of father’s exclusive license</p></td>
<td style="text-align: center;">100% of RR</td>
</tr>
<tr>
<td>180 days of shared leave (150 + 30)</td>
<td style="text-align: center;">83% of RR</td>
</tr>
<tr>
<td>150 days of leave</td>
<td style="text-align: center;">80% of RR</td>
</tr>
</tbody>
</table>

Source: Decreto-Lei n.º 91/2009, de 9 de abril

**Minimum daily amount:** the amount of the allowance cannot be less
than 80% of 1/30 of the SSI, which corresponded to €13.93 in 2024,
€13.58 in 2024, €12.81 in 2023, and €11.82 in 2022.

#### Extended parental allowance

Allowance paid to the mother or the father or both, alternatively aiming
to replace the lost work income during the period of childbirth leave,
provided that the leave is taken immediately after the end of the period
of the parental allowance or the extended parental allowance of the
other parent.

It is assigned for a period up to 3 months.

The daily amount of the allowance is calculated by applying 25% to the
value of the beneficiary’s reference remuneration.

**Minimum daily amount:** the amount of the allowance cannot be less
than 40% of 1/30 of the SSI, which corresponded to €6.97 in 2023, €6.79
in 2024, €6.41 in 2023 and €5.91 in 2022.

#### Subject to taxes/SIC

Not taxable. Not subject to SICs.

#### EUROMOD modelling

In the next EUROMOD Public Release this benefit will only be simulated
from 2015 to 2023. The simulation is, however, switched off as part of
the baselines, i.e., non-simulated components (*bfa*) are being used.

We assume that the mother takes the whole duration of leave and chooses
to take a shorter leave at higher replacement rate (120 days including
30 days before the childbirth, extended to 150 days in total in case of
multiple births)[^4]. For the partner we assume that they take the
maximum duration (25 working days given the 6 working days week or 29
calendar days). We also assume that parents do not decide to make use of
the extended parental allowance.

Besides, as the benefit amount depends on the previous earnings, we
assume those to be equal to the imputed wage (*yivwg*) or the current
wage, whichever is higher. The imputed wage is recorded in hourly terms;
hence we assume a country-specific standard number of hours worked per
week (40 hours) and we recalculate *yivwg* in monthly terms (yivwg\*40
\*(52/12)).

###  Parental social allowance (*bplnc_pt*)

#### Brief description

This benefit is intended for citizens that are not covered by any
compulsory social protection scheme or by the voluntary social insurance
scheme. This allowance is paid to the father and/or mother who do not
work and do not have Social Security contributions, or who do not
qualify for parental allowance. It is not compatible with work income
and unemployment benefits (that will be suspended while receiving the
parental social allowance).

#### Definition

This benefit is intended for citizens:

Not beneficiaries of any compulsory social protection scheme or by the
voluntary social insure scheme;

Beneficiaries receiving unemployment benefits (insurance and
assistance).

This allowance comprises several modalities (which have different
concession periods): initial parental social allowance, mother’s
exclusive initial parental social allowance, parent’s exclusive initial
parental social allowance, and initial parental social allowance of one
parent in the event of the impossibility of the other. The concession
periods are the ones equal to the contributory parental allowance.

#### Eligibility conditions

Be resident in Portugal or equivalent to a resident.

Have a monthly income, per person, of the household, equal or less than
80% of the SSI.

Do not have financial capital more than 240 x SSI.

#### Income test

The reference income is the sum of all the monthly income of the
household of the applicant divided by the elements of his household,
considering the following weighting for each element of the household:

Recipient: 1

Every other adult (18+): 0.7

Every under 18: 0.5

<span id="_Toc222328563" class="anchor"></span>**Table 2.45** Parental
social allowance (*bplnc_pt*): assessed income

| **Variable** | **Label**                                              |
|--------------|--------------------------------------------------------|
| yem          | INCOME: Employment                                     |
| yse          | INCOME: Self-employment                                |
| bunct_s      | BENEFIT/PENSION: Unemployment: insurance               |
| bunnc_s      | BENEFIT/PENSION: Unemployment: assistance              |
| poact_s      | BENEFIT/PENSION: Old age: contributory                 |
| poanc_s      | BENEFIT/PENSION: Old age: non-contributory             |
| psu          | BENEFIT/PENSION: Survivors                             |
| bsaoa_s      | BENEFIT/PENSION: Solidarity supplement for the elderly |
| bsa00_s      | BENEFIT/PENSION: Social integration income             |
| bsaot        | BENEFIT/PENSION: Other social assistance benefits      |
| bho          | BENEFIT/PENSION: Housing benefits                      |
| bed          | BENEFIT/PENSION: Education                             |
| ypp          | INCOME: Private pension                                |
| ypt          | INCOME: Private transfers                              |
| ypr          | INCOME: Property                                       |
| yiy          | INCOME: Investment                                     |
| Yot          | INCOME: Other                                          |

Source: Own elaboration

#### Benefit amount

The amount of the allowance corresponds to a percentage of the SSI, as
indicated below:

<span id="_Toc222328564" class="anchor"></span>**Table 2.46** Parental
social allowance (*bplnc_pt*) amounts \[2022-2025\]

<table style="width:56%;">
<colgroup>
<col style="width: 27%" />
<col style="width: 14%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Periods of
concession</strong></th>
<th style="text-align: center;"><strong>Monthly amounts</strong></th>
<th style="text-align: center;"><strong>In 2024</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>120 days of leave</p>
<p>150 days of shared leave (120 + 30)</p>
<p>30 additional days for each twin (plus the first)</p>
<p>10 days of father’s exclusive license</p></td>
<td style="text-align: center;">80% x SSI</td>
<td style="text-align: center;">€418.00</td>
</tr>
<tr>
<td>180 days of shared leave (150 + 30)</td>
<td style="text-align: center;">66% x SSI</td>
<td style="text-align: center;">€344,85</td>
</tr>
<tr>
<td>150 days of leave</td>
<td style="text-align: center;">64% x SSI</td>
<td style="text-align: center;">€334.40</td>
</tr>
</tbody>
</table>

Source: Decreto-Lei n.º 91/2009, de 9 de abril, as amended — Instituto
da Segurança Social (www.seg-social.pt)

#### Subject to taxes/SIC

Not taxable. Not subject to SICs.

#### EUROMOD modelling

This benefit is simulated from 2015. The simulation is, however,
switched off as part of the baselines, i.e., non-simulated components
(*bfa*) are being used.

The duration of this allowance is modelled for both parents the same way
as for the contributory parental allowance.

###  Extraordinary Housing Support (*bhotn_pt*)

#### Brief description

The Extraordinary Housing Support was introduced in 2023 as an
extraordinary support for families in the context of housing,
encompassing two different measures: a rental support, to support for
the payment of rent from a lease or sublease of first dwellings; and an
interest bonus, to support for the payment of the provision of a credit
agreement for own and permanent housing. Although initially planned as a
temporary measure, it has been kept and now constitute a definitive
feature of the Portuguese welfare-state architecture.

#### Definition

The unit of analysis is the individual.

#### Eligibility conditions

The rental support is aimed at resident tenants with a rent burden rate
exceeding 35% and an income up to the maximum limit of the sixth PIT
income bracket. This benefit, which is automatically assigned by the
Social Security with no need to request it, is also intended for
individuals who, although not obligated to submit an annual PIT
declaration, have monthly work incomes declared to social security or
are recipients of social benefits, up to a monthly amount corresponding
to 1/14 of the maximum limit of the sixth bracket of the PIT.

The interest bonus presents the same eligibility conditions, and it
comprises contracts concluded by 15 March 2023. The request has to be
made by the beneficiary from the financial institution.

#### Benefit amount

As for the rental support, it translates to a monthly amount up to €200
(and corresponds to the difference between the value of the rent and the
amount that would be paid if the effort rate was 35 % of the average
monthly value of income). This income support is intended for a maximum
period of five years.

As for the interest bonus, it translates to a yearly amount up to
€720.65 (and corresponds to the difference between the present value of
the indexer and the value of the indexer at the start of the loan plus 3
p.p., in the case of an effort rate of 50% (or more, depending on the
income bracket)). In addition to this support, credit institutions are
required to allow consumers to choose between variable, fixed or mixed
interest rates.

#### EUROMOD modelling

The interest bonification cannot be implemented in EUROMOD due to a lack
of data on several elements such as spread, contract date and loan
maturity date.

The simulation of the Extraordinary Housing Support benefit makes uses
of some interpretation room of [Decreto-Lei n.º
20-B/2023](https://urldefense.com/v3/__https:/files.dre.pt/1s/2023/03/05801/0003200040.pdf__;!!DOxrgLBm!FMqnvERNkKnSVYi1Cb9YmiYEGdVLf5bG490DYSG5L4gsK_o-GYEyzAS2MelYZeTZBifwfKqTo-Mw5Omoz7wI5U_ONf5D1KOeyHI5TlgW$)
to adjust the income lists used to compute the household rate of effort,
to avoid unequal situations in the access to the benefit between
taxpayers and non-taxpayers

## Social insurance contributions

### Employee social contributions *(tscee_pt)*

Generally, employees pay contributions on their gross employment income
at an 11% flat rate. Civil servants that started working before 2006
contribute to a separate scheme with multiple rates, but their average
rate is like the private sector general regime rate.

#### EUROMOD modelling

There are several regimes, according to specific activities/situations
(non-profit organizations, rural workers, football players, clergy,
domestic services, young people in their first job, handicapped). Due to
the lack of detailed information in the available data, EUROMOD can only
simulate the general rule.

### Employer social contributions *(tscer_pt)*

Employers pay contributions on their employees’ gross income according
to a flat rate of 23.75%.

#### EUROMOD modelling

The policy can be fully/perfectly simulated in EUROMOD, without any
particular data or modelling limitations.

###  Self-employed social contributions *(tscse_pt)*

**Self-employed social contributions since 2019:**

**Contribution rates** (applied to the monthly average income): 21.4%
(25.2% for rural workers).

**Contribution base:** actual income, rather than a conventional income
based on brackets. Still, not all the gross income is considered.
Relevant income: 70% of services or 20% of sales, according to the
nature of the business. In the income declaration, the self-employed has
the option to change the total income used for the calculation of
contributions, increasing, or lowering it by up to 25%.

Maximum base: 12 x SSI.

Minimum base: a base of incidence resulting in a contribution amount
lower than €5 is considered null.

**Quarterly reporting:** every quarter (end of January, April, July,
October) the self-employed are obliged to communicate their income from
the previous quarter. The quarterly income is then divided by three to
get the monthly average income. Quarterly update: every quarter,
contribution amounts are updated according to the updated monthly
average income derived from the quarterly income declaration.

**Minimum contribution:** €20/month.

**Exemptions:** the self-employed workers are exempt of paying social
contributions if they receive old age/disability pensions, or if they
simultaneously have received as employees an income above 12 x SSI and a
monthly average income from self-employment below 4 x SSI (the exceeding
amount is relevant and is considered in the contribution base).

**Self-employed ‘employers’ contribution:** if the self-employed
individual works on a regular basis for one institution, i.e., more than
50% (or 80%) of the self-employment income is paid by this institution
and the individual has no other source of employment income, then the
institution must pay a contribution of 7% (or 10%, respectively) of the
total amount paid for the services.

## Direct taxes

### Personal income tax (*tin00_pt*)

#### Tax unit

Personal income tax (‘*Imposto sobre o Rendimento Singular*’ – IRS) is
due by individuals residing in Portugal and by non-residents receiving
income in Portugal. When the individual residing in Portugal is part of
a family unit, the income tax may be applied jointly to all its members.
The basic tax unit is composed by the individual (or both partners, if
joint taxation is chosen) and their dependent children who are defined
as:

Children, adopted children and stepchildren younger than 18 years old
and not emancipated.

Children, adopted children and stepchildren aged between 18 and 25
(adults), with a monthly income below the national minimum wage.

Children, adopted children and stepchildren aged 18+ that have been
declared unfit for work and have a monthly income below the national
minimum wage (the model assumes that all disabled individuals are unfit
to work);

Minors (less than 18) living with a guardian and earning no income.

The age assessment’s date is December 31st.

Dependent parents do not belong to the tax unit. They constitute a
different tax unit of their own, that is only accounted in the
deductions phase. However, if they fulfil the conditions required to be
considered dependent parents (*i.e.*, income below the minimum pension)
they are exempt from tax obligations.

#### Taxable income

Methods for income determination and tax collection may vary between
different income sources. Nevertheless, the taxable income is always the
total income resulting from the aggregation of gross incomes of
different sources minus income specific deductions applied to each
income category, and specific reductions/allowances.

<span id="_Toc222328565" class="anchor"></span>**Table 2.47** Personal
income tax (*tin00_pt*): assessed income (before allowances deduction)

| **Variable** | **Label** |
|----|----|
| yem | INCOME: Employment |
| yse | INCOME: Self-employment |
| poact_s | BENEFIT/PENSION: Old age: contributory |
| poanc_s | BENEFIT/PENSION: Old age: non-contributory |
| psu | BENEFIT/PENSION: Survivors |
| pdi | BENEFIT/PENSION: Disability |
| ypp | INCOME: Private pension |
| ypr | INCOME: Property |
| yiy | INCOME: Investment (Although interest is subject to personal income tax, it is generally taxed at source, through the banking system, at a flat rate of 28%. Thus, in EUROMOD, it is simulated separately and not added to the families’ assessed income) |

Source: Own elaboration

#### Tax allowances

Deductions are applied at the individual level, even on joint taxation.
For instance, if both partners work, the deductions of the first income
category (see next table) are applied separately to their individual
incomes, with zero as limit for the outcome for each of them. Hence, if
only one of the partners received employment income, only one deduction
is applied. The same rule applies to pensions.

<span id="_Toc222328566" class="anchor"></span>**Table 2.48** Personal
income tax (*tin00_pt*) allowances \[2025\]

<table style="width:64%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 51%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Income category</strong></th>
<th style="text-align: center;"><strong>Deductions</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>A – Employment income <sup>(1) (2) (3)</sup></td>
<td>Deduction limit: €4,462.15 (8.54 X SSI) (or Social Security
contributions, if higher), with the upper limit of the yearly employment
income (if lower).</td>
</tr>
<tr>
<td>B – Business and professional income <sup>(1) (2) (3)</sup></td>
<td><p>Simplified regime: taxable income is 15% of sales or 75% of
liberal job earnings or 35% of other services provision earnings.</p>
<p>For the simulation, we assume a 25% tax allowance on self-employment
income.</p></td>
</tr>
<tr>
<td>E – Investment income</td>
<td>No deduction, but only 50% of the yearly gain is taxable. (NOT
SIMULATED)</td>
</tr>
<tr>
<td>F – Rental income</td>
<td>Repairs and maintenance expenses effectively incurred, municipal tax
and expenses with building administration. (NOT SIMULATED)</td>
</tr>
<tr>
<td>G – Net worth increases</td>
<td>50% of the net yearly gain is taxable. This rule does not apply to
realized gains from the sale of financial assets, where a 10% special
rate is applied. (NOT SIMULATED)</td>
</tr>
<tr>
<td>H – Pensions <sup>(1)</sup></td>
<td>Deduction limit: €4,462.15 (8.54 X SSI) (or Social Security
contributions, if higher), with the upper limit of the yearly pension
(if lower).</td>
</tr>
</tbody>
</table>

Notes:

<sup>(1)</sup> Specific considerations regarding income in A, B and H
categories from disabled people (90% incapacity): only 85% of income
from categories A and B, and 90% of income from category H, is
considered as taxable (upper limit per income category: €2,500).

<sup>(2)</sup> In 2021, a partial deduction for younger persons in
dependent employment was introduced. For further details see Table 2-48.

<sup>(3)</sup> Since 2020, there is a deduction for dependent students,
who earn employment and self-employment income, up to 5 x SSI.

Source: Código do IRS (CIRS), arts. 25.º–78.º — Autoridade Tributária e
Aduaneira (www.portaldasfinancas.gov.pt)

<span id="_Toc222328567" class="anchor"></span>**Table 2.49** Youth Tax
Allowance (IRS Jovem) \[2022-2025\]

<table style="width:62%;">
<colgroup>
<col style="width: 15%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"></th>
<th style="text-align: center;"><strong>2022</strong></th>
<th style="text-align: center;"><strong>2023</strong></th>
<th style="text-align: center;"><strong>2024</strong></th>
<th style="text-align: center;"><strong>2025</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Eligibility Conditions</strong></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td><blockquote>
<p><strong>Age</strong></p>
</blockquote></td>
<td style="text-align: center;">18-30</td>
<td style="text-align: center;">18-30</td>
<td style="text-align: center;">18-30</td>
<td style="text-align: center;">18-35</td>
</tr>
<tr>
<td><blockquote>
<p><strong>Education</strong></p>
</blockquote></td>
<td style="text-align: center;">Concluded mandatory education (12th
year) if under 26, or PhD if under 30.</td>
<td style="text-align: center;">Concluded mandatory education (12th
year) if under 26, or PhD if under 30.</td>
<td style="text-align: center;">Concluded mandatory education (12th
year) if under 26, or PhD if under 30.</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><blockquote>
<p><strong>Other</strong></p>
</blockquote></td>
<td style="text-align: center;">In dependent and independent
employment</td>
<td style="text-align: center;">In dependent and independent
employment</td>
<td style="text-align: center;">In dependent and independent
employment</td>
<td style="text-align: center;">In dependent and independent
employment</td>
</tr>
<tr>
<td><strong>Duration (Max.)</strong></td>
<td style="text-align: center;">3 Years</td>
<td style="text-align: center;">5 Years</td>
<td style="text-align: center;">5 Years</td>
<td style="text-align: center;">10 Years</td>
</tr>
<tr>
<td><strong>Allowance</strong></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td><blockquote>
<p><strong>1st Year</strong></p>
</blockquote></td>
<td style="text-align: center;">30% (up to 7.5 SSI)</td>
<td style="text-align: center;"><p>50%</p>
<p>up to 12.5 SSI)</p></td>
<td style="text-align: center;">100% (up to 40 SSI)</td>
<td style="text-align: center;">100% (up to 55 SSI)</td>
</tr>
<tr>
<td><blockquote>
<p><strong>2nd Year</strong></p>
</blockquote></td>
<td style="text-align: center;">20% (up to 5 SSI)</td>
<td style="text-align: center;"><p>40%</p>
<p>up to 10 SSI)</p></td>
<td style="text-align: center;">75% (up to 30 SSI)</td>
<td rowspan="3" style="text-align: center;">75% (up to 55 SSI)</td>
</tr>
<tr>
<td><blockquote>
<p><strong>3rd Year</strong></p>
</blockquote></td>
<td style="text-align: center;">10% (up to 2.5 SSI)</td>
<td style="text-align: center;"><p>30%</p>
<p>up to 7.5 SSI)</p></td>
<td rowspan="2" style="text-align: center;">50% (up to 20 SSI)</td>
</tr>
<tr>
<td><blockquote>
<p><strong>4th Year</strong></p>
</blockquote></td>
<td style="text-align: center;">-</td>
<td style="text-align: center;"><p>30%</p>
<p>up to 7.5 SSI)</p></td>
</tr>
<tr>
<td><blockquote>
<p><strong>5th Year</strong></p>
</blockquote></td>
<td style="text-align: center;">-</td>
<td style="text-align: center;"><p>20%</p>
<p>up to 5 SSI)</p></td>
<td style="text-align: center;">25% (up to 10 SSI)</td>
<td rowspan="3" style="text-align: center;">50% (up to 55 SSI)</td>
</tr>
<tr>
<td><blockquote>
<p><strong>6th Year</strong></p>
</blockquote></td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><blockquote>
<p><strong>7th Year</strong></p>
</blockquote></td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><blockquote>
<p><strong>8th Year</strong></p>
</blockquote></td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td rowspan="3" style="text-align: center;">25% (up to 55 SSI)</td>
</tr>
<tr>
<td><blockquote>
<p><strong>9th Year</strong></p>
</blockquote></td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><blockquote>
<p><strong>10th Year</strong></p>
</blockquote></td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Source: Lei n.º 82/2023 (OE 2024); Lei n.º 36/2024 (OE 2025) —
Autoridade Tributária e Aduaneira (www.portaldasfinancas.gov.pt)

<span id="_Toc222328568" class="anchor"></span>**Table 2.50** Net income
guarantee (‘*mínimo de existência*’) \[2022-2025\] (€/year)

<table style="width:60%;">
<colgroup>
<col style="width: 15%" />
<col style="width: 10%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 10%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"></th>
<th style="text-align: center;"><strong>2022</strong></th>
<th style="text-align: center;"><strong>2023</strong></th>
<th style="text-align: center;"><strong>2024</strong></th>
<th style="text-align: center;"><strong>2025</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Reference Value: a) In 2022, tax rates cannot reduce net income
below X euros if income originates mainly from employment and pensions;
b) From 2023 onwards, taxable incomes originated mainly from employment
income below X euros are entitled to the allowance amount of the Minimum
Income Guarantee <sup>(4)</sup></td>
<td style="text-align: center;"><p>14 x 1.5 x SSI</p>
<p>(or 14 x NMW, if higher) <sup>(2)</sup></p></td>
<td style="text-align: center;">The higher between 14 x 1.5 x SSI or
€10,640</td>
<td style="text-align: center;">The higher between 14 x 1.5 x SSI or
€11,480</td>
<td style="text-align: center;">The higher between 14 x 1.5 x SSI or
€12,180</td>
</tr>
<tr>
<td>Households with 3 or 4 dependent children and a taxable income less
or equal to X euros/year are exempt <sup>(1)</sup></td>
<td style="text-align: center;">11,320</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td>Households with 5+ dependent children and a taxable income less or
equal to X euros/year are exempt <sup>(1)</sup></td>
<td style="text-align: center;">15,560</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td>Income Limit (L) <sup>(3)</sup></td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">Reference Value- <span
class="math inline">$- \frac{limit\ for\ household\ general\
expenses}{1st\ tax\ rate\ x\ 3.3} + + \frac{1st\ income\
bracket}{3.3}$</span></td>
<td style="text-align: center;">Reference Value- <span
class="math inline">$- \frac{limit\ for\ household\ general\
expenses}{1st\ tax\ rate\ x\ 3.6} + + \frac{1st\ income\
bracket}{3.6}$</span></td>
<td style="text-align: center;">Reference Value- <span
class="math inline">$- \frac{limit\ for\ household\ general\
expenses}{1st\ tax\ rate\ x\ 3.6} + + \frac{1st\ income\
bracket}{3.6}$</span></td>
</tr>
</tbody>
</table>

Notes:

<sup>(1)</sup> Or half the amount in couples choosing individual
taxation.

<sup>(2)</sup> In the period covered, it is the case for 2022.

<sup>(3)</sup> Parameter employed to compute the taxpayers' deductions
in the 2023 Reform.

<sup>(4)</sup> The 2023 reform was applied retroactively to 2022 income,
with a safeguard clause stipulating that the rule resulting in lower tax
would apply. In general, the 2023 reform results in lower tax.

Source: Código do IRS (CIRS), art. 70.º — Autoridade Tributária e
Aduaneira (www.portaldasfinancas.gov.pt)

Since 2019, self-employed start being covered by the PIT net income
guarantee. This means that now these workers also have part of their
income tax-free, similarly to what already happened in previous years
with dependent employees. Net income guarantee should then also include
self-employment income (*yse*).

In 2023, there have been several changes in how the Net Income Guarantee
deduction is implemented. It now applies to taxable income to determine
the tax base before the tax schedule is applied, instead of being
adjusted after tax credits. Under this reform, the deduction is
applicable when the total of all taxpayers' gross incomes is less than
2.2 times the SSI multiplied by the number of taxpayers in the tax unit.
This reform was applied retroactively to 2022 income, with a safeguard
clause stipulating that the rule resulting in lower tax would apply.

To calculate the deduction for taxpayers, two different scenarios were
defined for 2022:

a\) For those whose total gross taxable income equal to or less than the
reference value, the deduction is the positive difference between the
reference value and specific allowances plus the
$`\frac{limit\ for\ household\ general\ deductions}{1st\ tax\ rate}`$,

b\) For those whose total gross taxable income is higher than the
reference value, the deduction is the positive difference between the
reference value and 3 x (gross taxable income - reference value), and
specific deductions plus
$`\frac{limit\ for\ household\ general\ deductions}{1st\ tax\ rate}`$,

To calculate the deduction for taxpayers in 2023, three different
scenarios were defined:

a\) For those whose total gross taxable income equal to or less than the
reference value, the deduction is the positive difference between the
reference value and specific allowances plus the
$`\frac{limit\ for\ household\ general\ deductions}{1st\ tax\ rate}`$,

b\) For those whose total gross taxable income is higher than the
reference value but equal to or less than the income limit L, the
deduction is the positive difference between the reference value and 2.3
x (gross taxable income - reference value), and specific deductions plus
$`\frac{limit\ for\ household\ general\ deductions}{1st\ tax\ rate}`$,

c\) For those with total gross taxable income higher than the income
limit, L, the deduction is the positive difference between L – 1st
bracket limit – 1.3 x (gross taxable income - L) and the sum of specific
allowances.

Since 2024, the intervals are the following:

a\) For those whose total gross taxable income equal to or less than the
reference value, the deduction is the positive difference between the
reference value and specific allowances plus the
$`\frac{limit\ for\ household\ general\ deductions}{1st\ tax\ rate}`$,

b\) For those whose total gross taxable income is higher than the
reference value but equal to or less than the income limit L, the
deduction is the positive difference between the reference value and 2.6
x (gross income - reference value), and specific deductions plus
$`\frac{limit\ for\ household\ general\ deductions}{1st\ tax\ rate}`$,

c\) For those with total gross taxable income higher than the income
limit, L, the deduction is the positive difference between L – 1st
bracket limit – 1.35 x (gross taxable income - L) and the sum of
specific allowances.

#### Tax base

**Personal Income Tax =** Tax base \* Rate – Tax credits,

Where **Tax base = Gross income – Income specific deductions –
Allowances**

According to the splitting system, income from married couples is
divided by 2 before applying the tax rate. In the case of married
couples, the resulting tax is multiplied by two to obtain the tax
liability (before tax credits).

#### Tax schedule 

The taxable income is subjected to tax rates according to income
brackets. In Azores and Madeira, the marginal tax rates are lower than
in the mainland[^5].

<span id="_Toc222328569" class="anchor"></span>**Table 2.51** Personal
income tax (*tin00_pt*) marginal rates \[2022-2025, Continent\]

|       **Year**        | **Income bracket** | **Marginal Rate** | **Deduct** |
|:---------------------:|:------------------:|:-----------------:|:----------:|
| **2022<sup>a</sup>**  |                    |                   |            |
|                       |    Up to 7,116     |      14.50%       |     0      |
|                       |  \>7,116 – 10,736  |      23.00%       |   604,86   |
|                       | \>10,736 – 15,216  |      26.50%       |   980,63   |
|                       | \>15,216 – 19,696  |      28.50%       |  1,284.99  |
|                       | \>19,696 – 25,076  |      35,00%       |  2,565.21  |
|                       | \>25,076 – 36,757  |      37.00%       |  3,066.79  |
|                       | \>36,757 – 48,033  |      43.50%       |  5,455.84  |
|                       | \>48,033 – 75,009  |      45.00%       |  6,176.56  |
|                       |    Above 75,009    |      48.00%       |  8,426.51  |
| **2023 <sup>a</sup>** |                    |                   |            |
|                       |    Up to 7,479     |      14.50%       |     0      |
|                       |  \>7,479 – 11,284  |      21.00%       |   486,14   |
|                       | \>11,284 – 15,992  |      26.50%       |  1,106.73  |
|                       | \>15,992 – 20,700  |      28.50%       |  1,426.65  |
|                       | \>20,700 – 26,355  |      35.00%       |  2,772.14  |
|                       | \>26,355 – 38,632  |      37.00%       |  3,299.12  |
|                       | \>38,632 – 50,483  |      43.50%       |  5,810.25  |
|                       | \>50,483 – 78,834  |      45.00%       |  6,567.33  |
|                       |    Above 78,834    |      48.00%       |  8,932.68  |
| **2024 <sup>a</sup>** |                    |                   |            |
|                       |    Up to 7,703     |      13.00%       |     0      |
|                       |  \>7,703 – 11,623  |      16.50%       |   269,61   |
|                       | \>11,623 – 16,472  |      22.00%       |   908.92   |
|                       | \>16,472 – 21,321  |      25.00%       |  1,403.08  |
|                       | \>21,321 – 27,146  |      32.00%       |  2,895.61  |
|                       | \>27,146 – 39,791  |      35.50%       |  3,845.50  |
|                       | \>39,791 – 43,000  |      43.50%       |  7,029.08  |
|                       | \>43,000 – 80,000  |      45.00%       |  7,673.78  |
|                       |    Above 80,000    |      48.00%       | 10,073.60  |
| **2025 <sup>a</sup>** |                    |                   |            |
|                       |    Up to 8,059     |      12.50%       |     0      |
|                       |  \>8,059 - 12,160  |      16.00%       |   282.07   |
|                       | \>12,160 - 17,233  |      21.50%       |   950.91   |
|                       | \>17,233 - 22,306  |      24.40%       |  1,450.67  |
|                       | \>22,306 - 28,400  |      31.40%       |  3,011.98  |
|                       | \>28,400 - 41,629  |      34.90%       |  4,006.10  |
|                       | \>41,629 - 44,987  |      43.10%       |  7,419.54  |
|                       | \>44,987 – 83,696  |      44.60%       |  8,094.51  |
|                       |    Above 83,696    |      48.00%       | 10,939.90  |

Notes**:** <sup>a</sup> Plus **“additional solidarity tax”:** income
above 80,000 and below 250,000 is additionally taxed in 2.5%; income
above 250,000 is additionally taxed in 5%.

Source: Código do IRS (CIRS), art. 68.º-A, as amended annually (OE laws)
— Autoridade Tributária e Aduaneira (www.portaldasfinancas.gov.pt)

<span id="_Toc222328570" class="anchor"></span>**Table 2.52** Personal
income tax (*tin00_pt*) marginal rates \[2022-2025, Azores\]

<table style="width:57%;">
<colgroup>
<col style="width: 6%" />
<col style="width: 24%" />
<col style="width: 0%" />
<col style="width: 13%" />
<col style="width: 13%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Year</strong></th>
<th colspan="2" style="text-align: center;"><strong>Income
bracket</strong></th>
<th style="text-align: center;"><strong>Marginal Rate</strong></th>
<th style="text-align: center;"><strong>Deduct</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><strong>2022<sup>a</sup></strong></td>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">Up to 7,116</td>
<td colspan="2" style="text-align: center;">10.15%</td>
<td style="text-align: center;">0</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;7,116 – 10,736</td>
<td colspan="2" style="text-align: center;">16.10%</td>
<td style="text-align: center;">423.40</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;10,736 – 15,216</td>
<td colspan="2" style="text-align: center;">18.55%</td>
<td style="text-align: center;">686.46</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;15,216 – 19,696</td>
<td colspan="2" style="text-align: center;">19.95%</td>
<td style="text-align: center;">899.42</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;19,696 – 25,076</td>
<td colspan="2" style="text-align: center;">24.50%</td>
<td style="text-align: center;">1,795.68</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;25,076 – 36,757</td>
<td colspan="2" style="text-align: center;">25.90%</td>
<td style="text-align: center;">2,146.76</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;36,757 – 48,033</td>
<td colspan="2" style="text-align: center;">30.45%</td>
<td style="text-align: center;">3,819.05</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;48,033 – 75,009</td>
<td colspan="2" style="text-align: center;">31.50%</td>
<td style="text-align: center;">4,323.45</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">Above 75,009</td>
<td colspan="2" style="text-align: center;">33.60%</td>
<td style="text-align: center;">5,898.71</td>
</tr>
<tr>
<td style="text-align: center;"><strong>2023 <sup>a</sup></strong></td>
<td colspan="2" style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">Up to 7,479</td>
<td style="text-align: center;">10.15%</td>
<td style="text-align: center;">0</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;7,479 – 11,284</td>
<td style="text-align: center;">14.70%</td>
<td style="text-align: center;">340.29</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;11,284 – 15,992</td>
<td style="text-align: center;">18.55%</td>
<td style="text-align: center;">774.76</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;15,992 – 20,700</td>
<td style="text-align: center;">19.95%</td>
<td style="text-align: center;">998.54</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;20,700 – 26,355</td>
<td style="text-align: center;">24.50%</td>
<td style="text-align: center;">1,940.42</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;26,355 – 38,632</td>
<td style="text-align: center;">25.90%</td>
<td style="text-align: center;">2,309.49</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;38,632 – 50,483</td>
<td style="text-align: center;">30.45%</td>
<td style="text-align: center;">4,067.18</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;50,483 – 78,834</td>
<td style="text-align: center;">31.50%</td>
<td style="text-align: center;">4,597.49</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">Above 78,834</td>
<td style="text-align: center;">33.60%</td>
<td style="text-align: center;">6,253.11</td>
</tr>
<tr>
<td style="text-align: center;"><strong>2024 <sup>a</sup></strong></td>
<td colspan="2" style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">Up to 7,703</td>
<td style="text-align: center;">9.10%</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;7,703 – 11,623</td>
<td style="text-align: center;">11.55%</td>
<td style="text-align: center;">188.72</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;11,623 – 16,472</td>
<td style="text-align: center;">15.40%</td>
<td style="text-align: center;">636.24</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;16,472 – 21,321</td>
<td style="text-align: center;">17.50%</td>
<td style="text-align: center;">982.06</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;21,321– 27,146</td>
<td style="text-align: center;">22.40%</td>
<td style="text-align: center;">2,026.77</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;27,146 – 39,791</td>
<td style="text-align: center;">24.85%</td>
<td style="text-align: center;">2,691.80</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;39,791– 51,997</td>
<td style="text-align: center;">30.45%</td>
<td style="text-align: center;">4,920.16</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;51,997 – 81,199</td>
<td style="text-align: center;">31.50%</td>
<td style="text-align: center;">5,464.44</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">Above 81,199</td>
<td style="text-align: center;">33.60%</td>
<td style="text-align: center;">7,171,50</td>
</tr>
<tr>
<td style="text-align: center;"><strong>2025 <sup>a</sup></strong></td>
<td colspan="2" style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">Up to 8,059</td>
<td style="text-align: center;">8.75%</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;8,059 - 12,160</td>
<td style="text-align: center;">11.20%</td>
<td style="text-align: center;">197.45</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;12,160 - 17,233</td>
<td style="text-align: center;">15.05%</td>
<td style="text-align: center;">665.64</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;17,233 - 22,306</td>
<td style="text-align: center;">17.08%</td>
<td style="text-align: center;">1,015.37</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;22,306 - 28,400</td>
<td style="text-align: center;">21.98%</td>
<td style="text-align: center;">2,108.36</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;28,400 - 41,629</td>
<td style="text-align: center;">24.43%</td>
<td style="text-align: center;">2,804.22</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;41,629 - 44,987</td>
<td style="text-align: center;">30.17%</td>
<td style="text-align: center;">5,193.63</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;44,987 – 83,696</td>
<td style="text-align: center;">31.22%</td>
<td style="text-align: center;">5,666.11</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">Above 83,696</td>
<td style="text-align: center;">33.60%</td>
<td style="text-align: center;">7,658.18</td>
</tr>
</tbody>
</table>

**Notes:** <sup>a</sup> Plus **“additional solidarity tax”:** income
above 80,000 and below 250,000 is additionally taxed in 1,75%; income
above 250,000 is additionally taxed in 3.5%.

Source: Decretos Legislativos Regionais da Madeira (annual) — Autoridade
Tributária e Aduaneira (www.portaldasfinancas.gov.pt)

<span id="_Toc222328571" class="anchor"></span>**Table 2.53** Personal
income tax (*tin00_pt*) marginal rates \[2022-2025, Madeira\]

<table style="width:57%;">
<colgroup>
<col style="width: 6%" />
<col style="width: 24%" />
<col style="width: 0%" />
<col style="width: 13%" />
<col style="width: 13%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Year</strong></th>
<th colspan="2" style="text-align: center;"><strong>Income
bracket</strong></th>
<th style="text-align: center;"><strong>Marginal Rate</strong></th>
<th style="text-align: center;"><strong>Deduct</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><strong>2022<sup>a</sup></strong></td>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">Up to 7,116</td>
<td colspan="2" style="text-align: center;">10.15%</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;7,116 – 10,736</td>
<td colspan="2" style="text-align: center;">16.10%</td>
<td style="text-align: center;">423.40</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;10,736 – 15,216</td>
<td colspan="2" style="text-align: center;">21.20%</td>
<td style="text-align: center;">970.96</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;15,216 – 19,696</td>
<td colspan="2" style="text-align: center;">22.80%</td>
<td style="text-align: center;">1,214,39</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;19,696 – 25,076</td>
<td colspan="2" style="text-align: center;">29.75%</td>
<td style="text-align: center;">2,583,33</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;25,076 – 36,757</td>
<td colspan="2" style="text-align: center;">33.67%</td>
<td style="text-align: center;">3,566,31</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;36,757 – 48,033</td>
<td colspan="2" style="text-align: center;">42.20%</td>
<td style="text-align: center;">6,701,54</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">&gt;48,033 – 75,009</td>
<td colspan="2" style="text-align: center;">43.65%</td>
<td style="text-align: center;">7,398,04</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;">Above 75,009</td>
<td colspan="2" style="text-align: center;">47.52%</td>
<td style="text-align: center;">10,300,99</td>
</tr>
<tr>
<td style="text-align: center;"><strong>2023 <sup>a</sup></strong></td>
<td colspan="2" style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">Up to 7,479</td>
<td style="text-align: center;">10.15%</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;7,479 – 11,284</td>
<td style="text-align: center;">14.70%</td>
<td style="text-align: center;">340.29</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;11,284 – 15,992</td>
<td style="text-align: center;">18.55%</td>
<td style="text-align: center;">774.76</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;15,992 – 20,700</td>
<td style="text-align: center;">19.95%</td>
<td style="text-align: center;">998.54</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;20,700 – 26,355</td>
<td style="text-align: center;">29.75%</td>
<td style="text-align: center;">3,027.17</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;26,355 – 38,632</td>
<td style="text-align: center;">33.67%</td>
<td style="text-align: center;">4,060.25</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;38,632 – 50,483</td>
<td style="text-align: center;">42.20%</td>
<td style="text-align: center;">7,355.53</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;50,483 – 78,834</td>
<td style="text-align: center;">43.65%</td>
<td style="text-align: center;">8,087.88</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">Above 78,834</td>
<td style="text-align: center;">47.52%</td>
<td style="text-align: center;">1,1138.46</td>
</tr>
<tr>
<td style="text-align: center;"><strong>2024 <sup>a</sup></strong></td>
<td colspan="2" style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">Up to 7,703</td>
<td style="text-align: center;">9.10%</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;7,703 – 11,623</td>
<td style="text-align: center;">11.55%</td>
<td style="text-align: center;">188.72</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;11,623 – 16,472</td>
<td style="text-align: center;">15.40%</td>
<td style="text-align: center;">636.24</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;16,472 – 21,321</td>
<td style="text-align: center;">17.50%</td>
<td style="text-align: center;">982.06</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;21,321– 27,146</td>
<td style="text-align: center;">22.40%</td>
<td style="text-align: center;">2,026.7</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;27,146 – 39,791</td>
<td style="text-align: center;">32.31%</td>
<td style="text-align: center;">4,716.89</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;39,791– 51,997</td>
<td style="text-align: center;">42.20%</td>
<td style="text-align: center;">8,652.16</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;51,997 – 81,199</td>
<td style="text-align: center;">43.65%</td>
<td style="text-align: center;">9,406.26</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">Above 81,199</td>
<td style="text-align: center;">47.52%</td>
<td style="text-align: center;">1,2548.49</td>
</tr>
<tr>
<td style="text-align: center;"><strong>2025 <sup>a</sup></strong></td>
<td colspan="2" style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">Up to 7,703</td>
<td style="text-align: center;">8.75%</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;7,703 – 11,623</td>
<td style="text-align: center;">11.20%</td>
<td style="text-align: center;">197.45</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;11,623 – 16,472</td>
<td style="text-align: center;">15.05%</td>
<td style="text-align: center;">665.64</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;16,472 – 21,321</td>
<td style="text-align: center;">17.08%</td>
<td style="text-align: center;">1,015.37</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;21,321– 27,146</td>
<td style="text-align: center;">21.98%</td>
<td style="text-align: center;">2,108.36</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;27,146 – 39,791</td>
<td style="text-align: center;">24.43%</td>
<td style="text-align: center;">2,804.22</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;39,791– 51,997</td>
<td style="text-align: center;">36.64%</td>
<td style="text-align: center;">7,887.03</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">&gt;51,997 – 81,199</td>
<td style="text-align: center;">40.59%</td>
<td style="text-align: center;">9,664.11</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">Above 81,199</td>
<td style="text-align: center;">46.56%</td>
<td style="text-align: center;">14,661.03</td>
</tr>
</tbody>
</table>

Notes: a Plus **“additional solidarity tax”:** income above 80,000 and
below 250,000 is additionally taxed in 2.5%; income above 250,000 is
additionally taxed in 5%.

Source: Decretos Legislativos Regionais dos Açores (annual) — Autoridade
Tributária e Aduaneira (www.portaldasfinancas.gov.pt

#### Tax credits

Certain expenses related to health, education, old age-care, housing,
insurance premiums, and disability can be deducted from the taxable
income, reducing the total tax liability. Table 2.53 below lists all
personal tax credits and other deductions.

Besides the ones presented, there are also other tax credits associated
with private retirement plans, stocks, shares savings plans, mortgage
savings accounts, acquisition of computers, acquisition of renewable
energy equipment, legal counselling fees, among others. (NOT SIMULATED)

<span id="_Toc222328572" class="anchor"></span>**Table 2.54** Personal
income tax (*tin00_pt*) credits \[2022-2025\]

<table style="width:64%;">
<colgroup>
<col style="width: 16%" />
<col style="width: 47%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Tax credit group</strong></th>
<th style="text-align: center;"><strong>Maximum limit</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Dependent children</td>
<td><ul>
<li><p>2022: €600 (or €726 if aged &lt;3) per dependent child. Increased
amounts for families with 2+: €900 per child aged &lt;3 and €750 per
child aged between 3 and 6;</p></li>
<li><p>2023: €600 (or €726 if aged &lt;3) per dependent child. Increased
amounts for families with 2+: €900 per child aged &lt;6;</p></li>
<li><p>2024: €600 (or €726 if aged &lt;3) per dependent child. Increased
amounts for families with 2+: €900 per child aged &lt;6;</p></li>
<li><p>2025: €600 (or €726 if aged &lt;3) per dependent child. Increased
amounts for families with 2+: €900 per child aged &lt;6.</p></li>
</ul></td>
</tr>
<tr>
<td>Dependent parents / grandparents</td>
<td style="text-align: center;">€525 per dependent parent (€635 if only
one)</td>
</tr>
<tr>
<td>Health</td>
<td style="text-align: center;">15% of expenses (up to €1,000)</td>
</tr>
<tr>
<td>Education and training</td>
<td style="text-align: center;"><p>30% of general education expenses (up
to €800)</p>
<p>30% of rent costs with accommodation of child in higher education (up
to €400) (NOT SIMULATED)</p></td>
</tr>
<tr>
<td>Retirement homes residency <sup>(1)</sup></td>
<td style="text-align: center;">25% of expenses (up to €403.75)</td>
</tr>
<tr>
<td>Housing (for mortgages – only interest – and rents)</td>
<td style="text-align: center;"><p>2022 and 2023: 15% of expenses (up to
€296 for mortgages or up to €502 for renters in the official renting
regime and other specific limits – see below)</p>
<p>2024: 15% of expenses (up to €296 for mortgages or up to €600 for
renters in the official renting regime and other specific limits – see
below)</p>
<p>2025: 15% of expenses (up to €296 for mortgages or up to €700 for
renters in the official renting regime and other specific limits – see
below)</p></td>
</tr>
<tr>
<td>Paid alimonies <sup>(1)</sup></td>
<td style="text-align: center;">20% of the alimonies annual amount</td>
</tr>
<tr>
<td>Disability</td>
<td style="text-align: center;">4 x IAS per individual disabled + 2.5 x
SSI per disabled dependent or dependent parent + 30% of expenses on
special education + 25% of expenses on life insurance of covering
exclusively the risks of death, disability, or old age</td>
</tr>
<tr>
<td>Invoice claiming <sup>(1)</sup></td>
<td style="text-align: center;">15% of the VAT paid in products and
services from specific sectors (restaurants, hotels, car repair, …) up
to €250</td>
</tr>
<tr>
<td>Household general expenses <sup>(2)</sup></td>
<td style="text-align: center;">35% of expenses (up to €250) supported
by each partner in the couple or by each single taxpayer or 45% of
expenses (up to €335) in the case of lone parents – see below.</td>
</tr>
</tbody>
</table>

Notes:

<sup>(1)</sup> EU-SILC contains no data on these expenses, so the
simulated tax credits are equal to zero.

<sup>(2)</sup> From 2015 on, a new tax credit is given according to
documented general expenses. Data may not yield information on
consumption, but the limit should prove to be easily attainable for
every non-exempt taxpayer, thus providing strong arguments to simulate
the full limit to every household without the need to regard
consumption.

Source: Código do IRS (CIRS), arts. 78.º et seq. — Autoridade Tributária
e Aduaneira (www.portaldasfinancas.gov.pt)

<span id="_Toc222328573" class="anchor"></span>**Table 2.55** Specific
limits for housing tax credit \[2022-2025\]

<table style="width:87%;">
<colgroup>
<col style="width: 8%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 26%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"></th>
<th style="text-align: center;"><strong>2022-2023</strong></th>
<th style="text-align: center;"><strong>2024</strong></th>
<th style="text-align: center;">2025</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="3">For renters paying rent</td>
<td>For individual tax bases up to the 1<sup>st</sup> income bracket,
the limit is €800</td>
<td style="text-align: center;">For individual tax bases up to the
1<sup>st</sup> income bracket, the limit is €900</td>
<td style="text-align: center;">For individual tax bases up to the 1st
income bracket, the limit is €1000</td>
</tr>
<tr>
<td><p>For individual tax bases between the 1<sup>st</sup> income
bracket and €30,000:</p>
<p><span class="math display">$$Limit = 502 + (800 - 502) \times
\frac{30,000 - Ind.Tax\ Base}{30,000 - \ 1st\ income\ bracket\ amount}\
$$</span></p></td>
<td style="text-align: center;"><p>For individual tax bases between the
1st income bracket and €30,000:</p>
<p><span class="math display">$$Limit = 600 + (900 - 600) \times
\frac{30,000 - Ind.Tax\ Base}{30,000 - \ 1st\ income\ bracket\
amount}$$</span></p></td>
<td style="text-align: center;"><p>For individual tax bases between the
1st income bracket and €30,000:</p>
<p><span class="math display">$$Limit = 700 + (1000 - 700) \times
\frac{30,000 - Ind.Tax\ Base}{30,000 - \ 1st\ income\ bracket\
amount}$$</span></p></td>
</tr>
<tr>
<td>For individual tax bases above €30,000, the limit is €502</td>
<td style="text-align: center;">For individual tax bases above €30,000,
the limit is €600</td>
<td style="text-align: center;">For individual tax bases above €30,000,
the limit is €700</td>
</tr>
<tr>
<td rowspan="3">For owners paying mortgage</td>
<td>For individual tax bases up to the 1<sup>st</sup> income bracket,
the limit is €450</td>
<td style="text-align: center;">For individual tax bases up to the
1<sup>st</sup> income bracket, the limit is €450</td>
<td style="text-align: center;">For individual tax bases up to the
1<sup>st</sup> income bracket, the limit is €450</td>
</tr>
<tr>
<td><p>For individual tax bases between the 1<sup>st</sup> income
bracket and €30,000:</p>
<p><span class="math display">$$Limit = 296 + (450 - 296) \times
\frac{30,000 - Ind.Tax\ Base}{30,000 - \ 1st\ income\ bracket\ amount}\
$$</span></p></td>
<td style="text-align: center;"><p>For individual tax bases between the
1<sup>st</sup> income bracket and €30,000:</p>
<p><span class="math display">$$Limit = 296 + (450 - 296) \times
\frac{30,000 - Ind.Tax\ Base}{30,000 - \ 1st\ income\ bracket\ amount}\
$$</span></p></td>
<td style="text-align: center;"><p>For individual tax bases between the
1<sup>st</sup> income bracket and €30,000:</p>
<p><span class="math display">$$Limit = 296 + (450 - 296) \times
\frac{30,000 - Ind.Tax\ Base}{30,000 - \ 1st\ income\ bracket\ amount}\
$$</span></p></td>
</tr>
<tr>
<td>For individual tax bases above €30,000, the limit is €296</td>
<td style="text-align: center;">For individual tax bases above €30,000,
the limit is €296</td>
<td style="text-align: center;">For individual tax bases above €30,000,
the limit is €296</td>
</tr>
</tbody>
</table>

Source: Código do IRS (CIRS), art. 78.º-E; Lei n.º 36/2024, art. 2.º —
Autoridade Tributária e Aduaneira (www.portaldasfinancas.gov.pt)

**Limits for tax credits:** the tax credits total amount (only on
health, education, housing, alimonies, invoice claiming, residential
homes and fiscal benefits) is restricted accordingly to the table below.
Note: the limits refer to the sum of the tax credits due to expenses on
health, education, housing, alimonies, invoice claiming, residential
homes and other fiscal benefits. Fixed tax credits regarding the number
of taxpayers or other elements in the tax units, disability or tax
credits regarding general expenses are not considered for these limits.

<span id="_Toc222328574" class="anchor"></span>**Table 2.56** Limits for
tax credit \[2022-2025\]

<table style="width:64%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 42%" />
<col style="width: 0%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"></th>
<th colspan="2" style="text-align: center;">2022-2025</th>
</tr>
</thead>
<tbody>
<tr>
<td>For individual tax bases up to the 1<sup>st</sup> income bracket,
there is</td>
<td colspan="2" style="text-align: center;">No limit</td>
</tr>
<tr>
<td>For individual tax bases between the 1<sup>st</sup> and last income
brackets:</td>
<td style="text-align: center;"><span class="math display">$$Limit =
1,000 + (2,500 - 1,500) \times \frac{first\ income\ bracket\ amount\
(art.\ 68 - A) - Ind.Tax\ Base}{first\ income\ bracket\ amount\ (art.\
68 - A) - 1st\ income\ bracket\ amounts}$$</span></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td>For individual tax bases above the last income bracket</td>
<td colspan="2" style="text-align: center;">€1,000</td>
</tr>
</tbody>
</table>

Note: In tax units with 3+ dependent children, all the above limits are
further increased in 5% for each one.

Source: Código do IRS (CIRS), art. 78.º-F — Autoridade Tributária e
Aduaneira (www.portaldasfinancas.gov.pt)

#### EUROMOD modelling

Joint taxation for unmarried couples is optional. Since it is by far the
most frequent option EUROMOD considers that from 2015, two adult
individuals that share the same fiscal dwelling during at least two
years – as well as in the period of the income tax – are entitled to
joint taxation (under civil union, ‘*união de facto*’, without need for
additional proof or declaring they are married in the input data). This
change contributed to a better validation of the PIT liability.
Comparing the percentage of individuals in EUROMOD/SILC eligible for
joint taxation with administrative microdata from the income tax, the
share of adult individuals that fills the declaration in joint taxation
is now only slightly higher (difference of 1 p.p.).

## Consumption taxes

As mentioned above (see section 1.4). the Portuguese tax system
encompasses a variety of consumption taxes. In this section we depict
the implementation (and modelling) of the Value Added Tax (‘Imposto
sobre o Valor Acrescentado’, IVA) and the various excise taxes that levy
upon the consumption of tobacco, alcohol, alcoholic and non-alcoholic
drinks and energy products.

### VAT (il_tva)

The Portuguese VAT Tax Code (Decree-Law n.º 102/2008) contemplates three
rates: A ‘Standard Rate’, and ‘Intermediate Rate’ and a Reduced Rate.
Since 2011 (Decree-Law n.º 134/2010), these rates are set as follows:

Standard Rate, is set at 23%;

Intermediate Rate is set at 13%;

‘Reduced Rate’ is set at 6%.

Portuguese legislation allows for the application of lower VAT rates in
the regions of Azores (16%, 9% and 4%, respectively) Madeira (22%, 12%
and 5%, respectively).

The Portuguese VAT Tax Code does, however, consider a number of
exemptions namely on goods medical and education supplies, transfer and
leasing of immovable property or goods (and services) provided by public
bodies or social solidarity private organizations. There are also VAT
exemptions for companies or self-employed persons with low turnover
(€14,500 in 2024), and a Special Scheme that provides a VAT exemption
for small retailers.

In 2023 (see Section 2.2.3), in response to the Cost-of-Living crisis,
Portuguese authorities have introduced a ‘Zero Rate’ (Law n.º 17/2023),
that applied to a variety of primary consumption goods (see Table 2.40),
below. This special rate was terminated in 2024.

<span id="_Toc222328575" class="anchor"></span>**Table 2.57** VAT rates
\[2022-2025\]

<table style="width:99%;">
<colgroup>
<col style="width: 9%" />
<col style="width: 0%" />
<col style="width: 65%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
</colgroup>
<thead>
<tr>
<th colspan="2">Rate</th>
<th>Products</th>
<th style="text-align: center;">2022</th>
<th style="text-align: center;">2023</th>
<th style="text-align: center;">2024</th>
<th style="text-align: center;">2025</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2">Standard</td>
<td></td>
<td style="text-align: center;">23%</td>
<td style="text-align: center;">23%</td>
<td style="text-align: center;">23%</td>
<td style="text-align: center;">23%</td>
</tr>
<tr>
<td colspan="2"></td>
<td></td>
<td style="text-align: center;"><p>(22%) <sup>a</sup></p>
<p>(16%) <sup>b</sup></p></td>
<td style="text-align: center;"><p>(22%) <sup>a</sup></p>
<p>(16%) <sup>b</sup></p></td>
<td style="text-align: center;"><p>(22%) <sup>a</sup></p>
<p>(16%) <sup>b</sup></p></td>
<td style="text-align: center;"><p>(22%)<sup>a</sup></p>
<p>(16%)<sup>b</sup></p></td>
</tr>
<tr>
<td colspan="2">Intermediate</td>
<td><p>Applies to:</p>
<p>a) Meat, fish and seafood preserves; b) Fruit and vegetable
preserves; c) Edible and vegetable oils, margarine; d) Vegetable
aperitives, corn based snacks; e) Cereals, without added sugar; f)
Cofee; g) Bottled water, common wines; h) Ready made meals (eat in or
take-out); i) Muscal instruments; j) Eletricity, for consumptions under
100 kWH /150kWH per months (in contracts with power equal or under 6.90
kVA)</p>
<p>k) Equipment for agriculture or environmental purposes.</p></td>
<td style="text-align: center;"><p>13%</p>
<p>(12%) <sup>a</sup></p>
<p>(9%) <sup>b</sup></p></td>
<td style="text-align: center;"><p>13%</p>
<p>(12%) <sup>a</sup></p>
<p>(9%) <sup>b</sup></p></td>
<td style="text-align: center;"><p>13%</p>
<p>(12%) <sup>a</sup></p>
<p>(9%) <sup>b</sup></p></td>
<td style="text-align: center;"><p>13%</p>
<p>(12%)<sup>a</sup></p>
<p>(9%)<sup>b</sup></p></td>
</tr>
<tr>
<td>Reduced</td>
<td colspan="2"><p>Applies to:</p>
<p>a) Bread, rice and other products from cereals; b) Meats, fish and
seafood (fresh or frozen); c) Dairy products (milk, cheese, yogurts),
eggs and honey; d) Salt, Olive oils, pig fat; e) Fruits, vegetables; f)
Water, except bottled and gasified water; g) Pharmaceutical products and
dietary products made from fruits or cereals; h) Books, magazines and
newspapers; i) Diesel, passenger transport, fire-fighting equipment; j)
Hotel accommodation and rental of areas reserved for camping sites; k)
Entries into singing, dancing, music, theater, cinema, circus shows.
exhibitions, zoos, botanical gardens and public aquariums; l)
Construction contracts for economic or cost-controlled housing
properties, as well as for local authorities and associations or fire
brigades; J) Food products for infants and young children, including
follow-on formulas, as well as foods for special medical purposes (2025
onwads).</p></td>
<td style="text-align: center;"><p>6%</p>
<p>(5%) <sup>a</sup></p>
<p>(4%) <sup>b</sup></p></td>
<td style="text-align: center;"><p>6%</p>
<p>(5%) <sup>a</sup></p>
<p>(4%) <sup>b</sup></p></td>
<td style="text-align: center;"><p>6%</p>
<p>(5%) <sup>a</sup></p>
<p>(4%) <sup>b</sup></p></td>
<td style="text-align: center;"><p>6%</p>
<p>(5%) <sup>a</sup></p>
<p>(4%) <sup>b</sup></p></td>
</tr>
<tr>
<td>Super reduced</td>
<td colspan="2">n.a.</td>
<td style="text-align: center;">n.a.</td>
<td style="text-align: center;">n.a.</td>
<td style="text-align: center;">n.a.</td>
<td style="text-align: center;">n.a.</td>
</tr>
</tbody>
</table>

Note: <sup>a</sup> *Rates applied in Madeira region. b Rates applied in
Azores region.\*

*Source: Código do IVA (CIVA), Listas I, II, and III annexed; annual OE
amendments — Autoridade Tributária e Aduaneira
(www.portaldasfinancas.gov.pt)*

<table style="width:99%;">
<colgroup>
<col style="width: 9%" />
<col style="width: 0%" />
<col style="width: 65%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
</colgroup>
<thead>
<tr>
<th colspan="2">Rate</th>
<th>Products</th>
<th style="text-align: center;">2022</th>
<th style="text-align: center;">2023</th>
<th style="text-align: center;">2024</th>
<th style="text-align: center;">2025</th>
</tr>
</thead>
<tbody>
<tr>
<td>Zero</td>
<td colspan="2"><p>Applies to:</p>
<p>a) Bread, rice, and pastas (except filled pastas); b) Fresh
vegetables, specifically potatoes, onions, tomatoes, cauliflower,
lettuce, broccoli, carrots, courgettis, leek, pumpkins, greens,
Portuguese cabbage, spinach, turnip, peas.</p>
<p>b) Dried vegetables, specifically red beans, black-eye peas,
chickpeas;</p>
<p>c) Fruits, specifically banana, oranges, pears, and melon;</p>
<p>d) Dairy, specifically cow milk, yogurt or fermented milk and
cheeses.</p>
<p>e) Meat (pork, chicken, turkey and veal) and fish (cod, sardines,
hake, mackerel, horse mackerel);</p>
<p>f) Oil, vegetable oil and edible oils, butter;</p>
<p>g) Other products, specifically canned tuna, chicken eggs,
vegetable-based drinks and yogurts, dietary and gluten-free
products.</p></td>
<td style="text-align: center;">n.a.</td>
<td style="text-align: center;">0%</td>
<td style="text-align: center;">n.a.</td>
<td style="text-align: center;">n.a.</td>
</tr>
<tr>
<td>Exempted</td>
<td colspan="2"><p>Applies to:</p>
<p>a) Medical care and education supplies;</p>
<p>b) Food and beverages supplied by employers to its staff;</p>
<p>c) Transfer and leasing of immovable property;</p>
<p>d) Insurance and reinsurance operations;</p>
<p>e) Certain financial operations;</p>
<p>f) Certain services rendered by non-profit making organisations;</p>
<p>g) Subscription fees of non-profit organisations;</p>
<p>h) Services related with the interpretation of Portuguese sign
language;</p>
<p>i) Tutoring services.</p></td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
</tbody>
</table>

Note: <sup>a</sup> Rates applied in Madeira region. <sup>b</sup> Rates
applied in Azores region.

Source: Decreto Legislativo Regional n.º 26/2016/M (Madeira CIVA);
Decreto Legislativo Regional n.º 1/2020/A (Azores CIVA) — Autoridade
Tributária e Aduaneira (www.portaldasfinancas.gov.pt)

### Excise Duties: Ad-valorem (il_txv) and Specific (il_txa)

As mentioned above, Excise Duties in Portugal cover five groups of
products: alcohol, alcoholic drinks, non-alcoholic drinks, tobacco
products and energy products.

<span id="_Toc222328576" class="anchor"></span>**Table 2.58**
*Ad-valorem* excise rates \[2022-2025\]

<table style="width:65%;">
<colgroup>
<col style="width: 34%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 9%" />
<col style="width: 8%" />
</colgroup>
<thead>
<tr>
<th>Products</th>
<th style="text-align: center;">2022</th>
<th style="text-align: center;">2023</th>
<th style="text-align: center;">2024</th>
<th style="text-align: center;">2025</th>
</tr>
</thead>
<tbody>
<tr>
<td>Tobacco</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td><blockquote>
<p>Cigarettes</p>
</blockquote></td>
<td style="text-align: center;">14%</td>
<td style="text-align: center;">12%</td>
<td style="text-align: center;">1%</td>
<td style="text-align: center;">1%</td>
</tr>
<tr>
<td><blockquote>
<p>Fine cut smoking tobacco (for rolling of cigarettes)</p>
</blockquote></td>
<td style="text-align: center;">15%</td>
<td style="text-align: center;">15%</td>
<td style="text-align: center;">15%</td>
<td style="text-align: center;">15%</td>
</tr>
<tr>
<td><blockquote>
<p>Cigars</p>
</blockquote></td>
<td style="text-align: center;">25%</td>
<td style="text-align: center;">25%</td>
<td style="text-align: center;">25%</td>
<td style="text-align: center;">25%</td>
</tr>
<tr>
<td><blockquote>
<p>Cigarillos</p>
</blockquote></td>
<td style="text-align: center;">25%</td>
<td style="text-align: center;">25%</td>
<td style="text-align: center;">25%</td>
<td style="text-align: center;">25%</td>
</tr>
<tr>
<td><blockquote>
<p>Other smoking tobacco (Smoking tobacco, snuff, chewing tobacco)</p>
</blockquote></td>
<td style="text-align: center;">15%</td>
<td style="text-align: center;">15%</td>
<td style="text-align: center;">15%</td>
<td style="text-align: center;">15%</td>
</tr>
<tr>
<td><blockquote>
<p>Other smoking tobacco (Hookah tobacco)</p>
</blockquote></td>
<td style="text-align: center;">50%</td>
<td style="text-align: center;">50%</td>
<td style="text-align: center;">75%</td>
<td style="text-align: center;">75%</td>
</tr>
<tr>
<td><blockquote>
<p>Other smoking tobacco (Liquid tobacco, with nicotine)</p>
</blockquote></td>
<td style="text-align: center;">n.a.</td>
<td style="text-align: center;">n.a.</td>
<td style="text-align: center;">n.a.</td>
<td style="text-align: center;">n.a.</td>
</tr>
<tr>
<td><blockquote>
<p>Other smoking tobacco (Liquid tobacco, without nicotine)</p>
</blockquote></td>
<td style="text-align: center;">n.a.</td>
<td style="text-align: center;">n.a.</td>
<td style="text-align: center;">n.a.</td>
<td style="text-align: center;">n.a.</td>
</tr>
</tbody>
</table>

Source: TEDB ([Taxes in Europe Database v4 - Homepage
(europa.eu)](https://ec.europa.eu/taxation_customs/tedb/#/home))

<span id="_Toc222328577" class="anchor"></span>**Table 2.59** Specific
(*ad-quantum*) excise rates \[2022-2025\]

<table style="width:74%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th>Products</th>
<th>2022</th>
<th>2023</th>
<th>2024</th>
<th>2025</th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>Ethyl alcohol (pure alcohol)</td>
<td>€1386.93/Hl</td>
<td>€1456.83/Hl</td>
<td>€1602.51/Hl</td>
<td>€1602.51/Hl</td>
<td></td>
</tr>
<tr>
<td>Alcoholic Drinks</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Low Alcohol Beer</p>
</blockquote></td>
<td>€8.42/Hl</td>
<td>€8.76/Hl</td>
<td>€9.64/Hl</td>
<td>€9.64/Hl</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Beer, per Plato of finished product</p>
</blockquote></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Plato &lt;=7º</p>
</blockquote></td>
<td>€10.54/Hl</td>
<td>€10.96/Hl</td>
<td><p>€12.06/Hl</p>
<p><sup>(€12.06/Hl)</sup></p></td>
<td><p>€12.06/Hl</p>
<p><sup>(€12.06/Hl)</sup></p></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Plato &gt;7º &amp; &lt;= 11º</p>
</blockquote></td>
<td>€16.87/Hl</td>
<td>€17.54/Hl</td>
<td><p>€19.29/Hl</p>
<p><sup>(€19.29/Hl)</sup></p></td>
<td><p>€19.29/Hl</p>
<p><sup>(€19.29/Hl)</sup></p></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Plato &gt;11º &amp; &lt;= 13º</p>
</blockquote></td>
<td>€21.10/Hl</td>
<td><p>€21.94/Hl</p>
<p><sup>(€21.94/Hl)</sup></p></td>
<td><p>€24.13/Hl</p>
<p><sup>(€24.13/Hl)</sup></p></td>
<td><p>€24.13/Hl</p>
<p><sup>(€24.13/Hl)</sup></p></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Plato &gt;13º &amp; &lt;= 15º</p>
</blockquote></td>
<td>€25.31/Hl</td>
<td>€26.32/Hl</td>
<td><p>€28.95/Hl</p>
<p><sup>(€28.95/Hl)</sup></p></td>
<td><p>€28.95/Hl</p>
<p><sup>(€28.95/Hl)</sup></p></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Plato &gt;15º</p>
</blockquote></td>
<td>€29.59/Hl</td>
<td>€30.77/Hl</td>
<td><p>€33.85/Hl</p>
<p><sup>(€33.85/Hl)</sup></p></td>
<td><p>€33.85/Hl</p>
<p><sup>(€33.85/Hl)</sup></p></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Wine</p>
</blockquote></td>
<td>€0</td>
<td><p>€0</p>
<p><sup>(€0)</sup></p></td>
<td><p>€0</p>
<p><sup>(€0)</sup></p></td>
<td><p>€0</p>
<p>(€0)</p></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Fermented</p>
</blockquote></td>
<td>€10.54/Hl</td>
<td>€10.96/Hl</td>
<td><p>€12.06/Hl</p>
<p><sup>(€12.06/Hl)</sup></p></td>
<td><p>€12.06/Hl</p>
<p><sup>(€12.06/Hl)</sup></p></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Intermediate</p>
</blockquote></td>
<td>€76.86/Hl</td>
<td>€79.93/Hl</td>
<td><p>€87.92/Hl</p>
<p><sup>(€87.92/Hl)</sup></p></td>
<td><p>€87.92/Hl</p>
<p><sup>(€87.92/Hl)</sup></p></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Spirits</p>
</blockquote></td>
<td>€1400.80/Hl</td>
<td>€1456.83/Hl</td>
<td>€1602.51/Hl</td>
<td>€1602.51/Hl</td>
<td></td>
</tr>
<tr>
<td>Non-alcoholic beverages</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>With added sugar or sweetening</p>
</blockquote></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&lt; 25 grams</p>
</blockquote></td>
<td>€1.01/l</td>
<td>€1.05/l</td>
<td>€1.16/l</td>
<td>€1.16/l</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&gt;=25 to &lt; 50 grams</p>
</blockquote></td>
<td>€6.08/l</td>
<td>€6.32/l</td>
<td>€6.95/l</td>
<td>€6.95/l</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&gt;=50 to &lt; 80 grams</p>
</blockquote></td>
<td>€8.10/l</td>
<td>€8.42/l</td>
<td>€9.26/l</td>
<td>€9.26/l</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&gt;80 grams</p>
</blockquote></td>
<td>€20.26/l</td>
<td>€21.07/l</td>
<td>€23.18/l</td>
<td>€23.18/l</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Low alcohol</p>
<p>(&gt; 0,5% vol. &amp; &lt;= 1,2% vol.)</p>
</blockquote></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&lt; 25 grams</p>
</blockquote></td>
<td>€1.01/l</td>
<td>€1.05/l</td>
<td>€1.16/l</td>
<td>€1.16/l</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&gt;=25 to &lt; 50 grams</p>
</blockquote></td>
<td>€6.08/l</td>
<td>€6.32/l</td>
<td>€6.95/l</td>
<td>€6.95/l</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&gt;=50 to &lt; 80 grams</p>
</blockquote></td>
<td>€8.10/l</td>
<td>€8.42/l</td>
<td>€9.26/l</td>
<td>€9.26/l</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&gt;80 grams</p>
</blockquote></td>
<td>€20.26/l</td>
<td>€21.07/l</td>
<td>€23.18/l</td>
<td>€23.18/l</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Concentrates (Liquid Form)</p>
</blockquote></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&lt; 25 grams</p>
</blockquote></td>
<td>€6.08/l</td>
<td>€6.32/l</td>
<td>€6.95/l</td>
<td>€6.95/l</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&gt;=25 to &lt; 50 grams</p>
</blockquote></td>
<td>€36,47/l</td>
<td>€37,93/l</td>
<td>€41,72/l</td>
<td>€41,72/l</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&gt;=50 to &lt; 80 grams</p>
</blockquote></td>
<td>€48.62/l</td>
<td>€50.56/l</td>
<td>€55.62/l</td>
<td>€55.62/l</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&gt;80 grams</p>
</blockquote></td>
<td>€121.56/l</td>
<td>€126.42/l</td>
<td>€139.06/l</td>
<td>€139.06/l</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Concentrates (Solids)</p>
</blockquote></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&lt; 25 grams</p>
</blockquote></td>
<td>€10.13/l00 Kg</td>
<td>€10.54/l00 Kg</td>
<td>€11.59/l00 Kg</td>
<td>€11.59/l00 Kg</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&gt;=25 to &lt; 50 grams</p>
</blockquote></td>
<td>€60.78/ l00 Kg</td>
<td>€63.21/ l00 Kg</td>
<td>€69.53/ l00 Kg</td>
<td>€63.53/ l00 Kg</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&gt;=50 to &lt; 80 grams</p>
</blockquote></td>
<td>€81.04/ l00 Kg</td>
<td>€84.28/ l00 Kg</td>
<td>€92.71/ l00 Kg</td>
<td>€92.71/ l00 Kg</td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>&gt;80 grams</p>
</blockquote></td>
<td>€202.61/ l00 Kg</td>
<td>€210.71/ l00 Kg</td>
<td>€231.78/ l00 Kg</td>
<td>€231.78/ l00 Kg</td>
<td></td>
</tr>
</tbody>
</table>

Note: **g** - Gramm; **l** - Liter; **ml** - Milliliter; **Hl** –
Hectoliter (100 Liters); **MGW** – Megawatt; **T** – Ton (1000 Kg);
**KT** – Kiloton (1000 Tons); GJ - Gigajoule (1,000,000,000 Joules).

Source: Código dos Impostos Especiais de Consumo (CIEC), as amended
annually — Autoridade Tributária e Aduaneira
(www.portaldasfinancas.gov.pt)

<span id="_Toc222328578" class="anchor"></span>**Table 2.60** Specific
(*ad-quantum*) excise rates \[2022-2025\] (cont.)

<table style="width:63%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th>Products</th>
<th>2022</th>
<th>2023</th>
<th>2024</th>
<th>2025</th>
</tr>
</thead>
<tbody>
<tr>
<td>Tobacco</td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Cigarettes</p>
</blockquote></td>
<td><p>€102.01/</p>
<p>1000 units</p></td>
<td><p>€112.50/</p>
<p>1000 units</p></td>
<td><p>€151.88/</p>
<p>1000 units</p></td>
<td><p>€151.88/</p>
<p>1000 units</p></td>
</tr>
<tr>
<td><blockquote>
<p>Fine cut smoking tobacco (for rolling of cigarettes)</p>
</blockquote></td>
<td>0.082/g</td>
<td>0.087/g</td>
<td>0.091/g</td>
<td>0.091/g</td>
</tr>
<tr>
<td><blockquote>
<p>Cigars <sup>a</sup></p>
</blockquote></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Cigarillos <sup>a</sup></p>
</blockquote></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Other smoking tobacco (Smoking tobacco, snuff, chewing tobacco)</p>
</blockquote></td>
<td>€0.0845/g</td>
<td>€0.0896/g</td>
<td>€0.0935/g</td>
<td>€0.0935/g</td>
</tr>
<tr>
<td><blockquote>
<p>Other smoking tobacco (Hookah tobacco)</p>
</blockquote></td>
<td>n.a.</td>
<td>n.a.</td>
<td>n.a.</td>
<td>n.a.</td>
</tr>
<tr>
<td><blockquote>
<p>Other smoking tobacco (Liquid tobacco, with nicotine)</p>
</blockquote></td>
<td>€0.323/ml</td>
<td>€0.336/ml</td>
<td>€0.351/ml</td>
<td>€0.351/ml</td>
</tr>
<tr>
<td><blockquote>
<p>Other smoking tobacco (Liquid tobacco, without nicotine)</p>
</blockquote></td>
<td style="text-align: center;">n.a.</td>
<td style="text-align: center;">n.a.</td>
<td>€0.175/ml</td>
<td>€0.175/ml</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>Energy Products <sup>a</sup></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Electricity</p>
</blockquote></td>
<td>1/MGW</td>
<td>1/MGW</td>
<td>1/MGW</td>
<td>1/MGW</td>
</tr>
<tr>
<td><blockquote>
<p>Coal (heating fuel for non-business use)</p>
</blockquote></td>
<td>€4.26/T</td>
<td>€4.26/T</td>
<td>€4.26/T</td>
<td>€4.26/T</td>
</tr>
<tr>
<td><blockquote>
<p>Petroleum Coke (heating fuel for non-business use)</p>
</blockquote></td>
<td>€4.26/T</td>
<td>€4.26/T</td>
<td>€4.26/T</td>
<td>€4.26/T</td>
</tr>
<tr>
<td><blockquote>
<p>Petrol</p>
</blockquote></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Leaded</p>
</blockquote></td>
<td>n.a.</td>
<td>n.a.</td>
<td>n.a.</td>
<td>n.a.</td>
</tr>
<tr>
<td><blockquote>
<p>Unleaded</p>
</blockquote></td>
<td>€444.90/KT</td>
<td>€552.26/KT</td>
<td>€629.88/KT</td>
<td>€634.36/KT</td>
</tr>
<tr>
<td><blockquote>
<p>Diesel</p>
</blockquote></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Regular (Propellant)</p>
</blockquote></td>
<td>€286.06/KT</td>
<td>€418.22/KT</td>
<td>€465.45/KT</td>
<td>€504/KT</td>
</tr>
<tr>
<td><blockquote>
<p>Regular (Heating fuel for non-business use)</p>
</blockquote></td>
<td>€330.00/KT</td>
<td>€330.00/KT</td>
<td>€330.00/KT</td>
<td>€330.00/KT</td>
</tr>
<tr>
<td><blockquote>
<p>Colored (Propellant)</p>
</blockquote></td>
<td>€67.51/KT</td>
<td>€47.19/KT</td>
<td>€21/KT</td>
<td>€21/KT</td>
</tr>
<tr>
<td><blockquote>
<p>Natural Gas</p>
</blockquote></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Propellant</p>
</blockquote></td>
<td>€0.307/GJ</td>
<td>€0.307/GJ</td>
<td>€0.307/GJ</td>
<td>€0.307/GJ</td>
</tr>
<tr>
<td><blockquote>
<p>Heating fuel for non-business use</p>
</blockquote></td>
<td>€1.65/GJ</td>
<td>€1.65/GJ</td>
<td>€3.467/GJ</td>
<td>€3.467/GJ</td>
</tr>
<tr>
<td><blockquote>
<p>Heavy Fuel Oil</p>
</blockquote></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>If Sulphur content =&lt;0.5%</p>
</blockquote></td>
<td>€15.65/T</td>
<td>€15.65/T</td>
<td>€15.65/T</td>
<td>€15.65/T</td>
</tr>
<tr>
<td><blockquote>
<p>If Sulphur content &gt;0.5%</p>
</blockquote></td>
<td>€29.92/T</td>
<td>€29.92/T</td>
<td>€29.92/T</td>
<td>€29.92/T</td>
</tr>
<tr>
<td><blockquote>
<p>LPG</p>
</blockquote></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Propellant</p>
</blockquote></td>
<td>€136.56/T</td>
<td>€136.56/T</td>
<td>€136.56/T</td>
<td>€136.56/T</td>
</tr>
<tr>
<td><blockquote>
<p>Heating fuel for non-business use</p>
</blockquote></td>
<td>€7.99/T</td>
<td>€7.99/T</td>
<td>€7.99/T</td>
<td>€7.99/T</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

Notes: g - Gramm; l - Liter; ml - Milliliter; Hl – Hectoliter (100
Liters); MGW – Megawatt; T – Ton (1000 Kg); KT – Kiloton (1000 Tons);
GJ - Gigajoule (1,000,000,000 Joules). a This product is not subjected
to a specific rate. The values refer to the minimum tax applicable per
1000 units, under the Portuguese legislation. a An additional carbon
related-tax is applied in these products.

Source: Código dos Impostos Especiais de Consumo (CIEC), as amended
annually — Autoridade Tributária e Aduaneira
(www.portaldasfinancas.gov.pt)

<span id="_Toc222328579" class="anchor"></span>**Table 2.61** Prices of
Excise products \[2022-2025\]

<table style="width:63%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th>Products</th>
<th>2022</th>
<th>2023</th>
<th>2024</th>
<th>2025</th>
</tr>
</thead>
<tbody>
<tr>
<td>Alcohol</td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Ethyl Alcohol</p>
</blockquote></td>
<td>25.49 EUR/l</td>
<td>27.48 EUR/l</td>
<td>29.19 EUR/l</td>
<td>29.19 EUR/l</td>
</tr>
<tr>
<td><blockquote>
<p>Wine</p>
</blockquote></td>
<td>7.41 EUR/l</td>
<td>6.84 EUR/l</td>
<td>6.79 EUR/l</td>
<td>6.79 EUR/l</td>
</tr>
<tr>
<td><blockquote>
<p>Sparkling Wine</p>
</blockquote></td>
<td>36.00 EUR/l</td>
<td>37.46 EUR/l</td>
<td>37.19 EUR/l</td>
<td>37.19 EUR/l</td>
</tr>
<tr>
<td><blockquote>
<p>Beer</p>
</blockquote></td>
<td>2.92 EUR/l</td>
<td>3.27 EUR/l</td>
<td>3.25 EUR/l</td>
<td>3.25 EUR/l</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>Tobacco</td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Cigarettes</p>
</blockquote></td>
<td>235.00 EUR/ 1000 pieces</td>
<td>239.00 EUR/ 1000 pieces</td>
<td>246.50 EUR/ 1000 pieces</td>
<td>246.50 EUR/ 1000 pieces</td>
</tr>
<tr>
<td><blockquote>
<p>Cigars</p>
</blockquote></td>
<td>273.04 EUR/ 1000 pieces</td>
<td>277.45 EUR/ 1000 pieces</td>
<td>286.45 EUR/ 1000 pieces</td>
<td>286.45 EUR/ 1000 pieces</td>
</tr>
<tr>
<td><blockquote>
<p>Other Tobacco</p>
</blockquote></td>
<td>256.71 EUR/kg</td>
<td>263.56 EUR/kg</td>
<td>271.96 EUR/kg</td>
<td>271.96 EUR/kg</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>Energy Products</td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><blockquote>
<p>Electricity</p>
</blockquote></td>
<td>233.40 EUR /MWh</td>
<td>229.40 EUR /MWh</td>
<td>254.26 EUR /MWh</td>
<td>254.26 EUR /MWh</td>
</tr>
<tr>
<td><blockquote>
<p>Natural – Gas (Heating)</p>
</blockquote></td>
<td>33.21 EUR/GJ</td>
<td>47.05 EUR/GJ</td>
<td>38.59 EUR/GJ</td>
<td>38.59 EUR/GJ</td>
</tr>
<tr>
<td><blockquote>
<p>Liquefied hydrocarbons (LPG)</p>
</blockquote></td>
<td>2534.47 EUR /1000kg</td>
<td>2647.88 EUR /1000kg</td>
<td>2744.99 EUR /1000L</td>
<td>2744.99 EUR /1000L</td>
</tr>
<tr>
<td><blockquote>
<p>Gas Oil (Heating)</p>
</blockquote></td>
<td>1736.41 EUR /1000l</td>
<td>1592.65 EUR /1000l</td>
<td>1641.80 EUR /1000l</td>
<td>1641.80 EUR /1000l</td>
</tr>
<tr>
<td><blockquote>
<p>Coal and Coke (Heating)</p>
</blockquote></td>
<td>23.77 EUR/GJ</td>
<td>26.73 EUR/GJ</td>
<td>27.05 EUR/GJ</td>
<td>27.05 EUR/GJ</td>
</tr>
<tr>
<td><blockquote>
<p>Petrol (Unleaded)</p>
</blockquote></td>
<td>1847.29 EUR /1000l</td>
<td>1719.10 EUR /1000l</td>
<td>1735.08 EUR /1000lt</td>
<td>1735.08 EUR /1000lt</td>
</tr>
<tr>
<td><blockquote>
<p>Gas Oil (Propellant)</p>
</blockquote></td>
<td>1795.96 EUR /1000l</td>
<td>1589.38 EUR /1000l</td>
<td>1597.42 EUR /1000l</td>
<td>1597.42 EUR /1000l</td>
</tr>
</tbody>
</table>

Notes: n: nowcasted

Source: Direção-Geral de Energia e Geologia (DGEG) — www.dgeg.gov.pt;
INE / Eurostat consumer price statistics

Consumer prices of goods subject to excise duties are nowcasted,
similarly to what the model does to update incomes from SILC. We combine
the latest available data from the following sources:

Inflation: Harmonised Index of Consumer Prices (HICP, Eurostat) at
COICOP 5 digits, usually for the first quarter for beta release and up
to third quarter 3 for final release.

Inflation quarter-on-quarter forecasts (DG ECFIN, confidential) by HICP
main groups (Unprocessed food, Processed food including alcohol and
tobacco, Non-energy industrial goods, Energy, Services - overall index
excluding goods) of quarters 2, 3 and 4, as needed for each release.

For more details on the specific source of the price of each good, see
Akoğuz et al (2020).

The price of Cigarettes and Fuels (Petrol and Gas Oil) did not follow
this general sources/nowcasting strategy but were sourced from “Taxes in
Europe” Database (DG-TAXUD) and the Weekly Oil Bulletin, respectively.
While the “Taxes in Europe” database seems to report more accurately the
prices of this particular excise item, the Weekly Oil Bulletin registers
fuels’ weekly prices, allowing for estimating a more updated evolution
of fuel prices.

***<u>EUROMOD modelling</u>***

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

When modelling the implementation of VAT, we take in consideration four
orders of factors:

1)  The type and level of VAT tax rates;

2)  The products covered by each type of VAT rate;

3)  The possibility of exemptions to VAT;

4)  The existence of relevant regional variations, applicable to the
    autonomous regions of Azores and Madeira.

When modelling the implementation of Excise Duties, we take in
consideration four orders of factors:

1)  Differences in approach, i.e. whether products are taxed by
    reference to their value (*ad-valorem* excise rates), or by
    reference to the quantity consumed (*ad-quantum* or specific excise
    rates);

<!-- -->

5)  The types of products covered by reference to the type of taxation
    approach adopted;

6)  The existence of relevant regional variations, applicable to the
    autonomous regions of Azores and Madeira.

In cases where no specific rate is specified in the legislation, we use
the minimum tax applicable as the functional equivalent for the specific
rate.

Further information on methodology and specific calculations and the
independence of these consumption taxes is common across countries (this
is why they are placed in an add-on and not in the policy spine of each
country) and can be found in Akoğuz et al (2020).

## Extraordinary measures

### COST-OF-LIVING Crisis: Family income support (bfaxp_pt)

#### Brief description

This extraordinary benefit was was introduced in 2022 and intended to
partially compensate families for the increase in prices and cost of
living faced during that year, within the ‘*Families First*’ program
scope. It was a one-off payment done in October 2022.

#### Definition

The unit of analysis is the individual.

#### Eligibility conditions

This extraordinary income support is granted to residents with a gross
income of up to €2,700 gross per month (€37,800 annually), equivalent to
twice the average monthly earnings in Portugal.

Recipients of the measure are also beneficiaries of certain social
benefits (such as unemployment benefit, sickness benefit, social
insertion income or child benefit, among others) and scholarship holders
who pay voluntary social insurance.

#### Benefit amount

Exceptional income support of €125 per adult and €50 per child or young
people up to 24 years old (inclusive), or with no age limit in the case
of dependents due to disability.

Those receiving an exceptional supplement for pensioners of less than
€125 will received the difference.

### COST-OF-LIVING Crisis: Extraordinary supplement for vulnerable families (*bfaxp01_pt*)

#### Brief description

This extraordinary supplement for vulnerable families was introduced in
2023 and intended to partially compensate families for the increase in
prices and cost of living faced during that year.

#### Definition

The unit of analysis is the family.

#### Eligibility conditions

This support is granted to residents who are beneficiaries of the Social
Electricity Tariff, in reference to the month of March 2023.

Families that are not beneficiaries of the Social Electricity Tariff,
but in which at least one member of the household is a beneficiary of
one of the minimum social benefits (such as unemployment benefit,
sickness benefit or social insertion income, among others) or in which
one of the children is entitled to the 1st or 2nd income bracket of the
child family, are also entitled to this support.

#### Benefit amount

This extraordinary supplement for vulnerable families is of €30 per
month per household, paid quarterly. Families with children and young
people, receiving Child Benefit (up to the fourth income bracket) are
also receive an extraordinary supplement of €15 per month for each
child, which is also paid on a quarterly basis.

#### EUROMOD modelling

EU-SILC does not include information on recipients of the Social
Electricity Tariff. Therefore, in the model, families eligible for the
benefit are those in which at least one household member receives one of
the minimum social benefits.

# Data

## General description

EUROMOD database results from EU-SILC, (the latest dataset is based on
EU-SILC containing 2024 cross-sectional and 2023 longitudinal Version
24-250530). The Portuguese EU-SILC survey is an annual survey with a
four-year rotational panel. Fieldwork was carried out in 2024, between
March and September, and contains data regarding the incomes of 2023.
The database is provided by Eurostat.

The EU-SILC sample is composed of four independent sub-samples, where
each one follows a stratified two-stage cluster sampling design. The
2022 sampling frame was selected from the National Dwellings Register
(NDR). It is constituted by private dwellings of usual residence and
excludes collective households and institutions. Its size is
approximately 1,4 million dwellings of usual residence.

The selection of the sample followed a stratified (NUTS II
stratification) and multistage sampling design. The primary sampling
units, consisting of cells of the INSPIRE grid of 1km2, were selected
with probability proportional to the number of dwellings of usual
residence. And the secondary sampling units (dwellings) were
systematically selected in each primary sampling unit. Information is
collected on all households and individuals living in the selected
dwelling.

<span id="_Toc222328580" class="anchor"></span>**Table 3.1** EUROMOD
database description

| EUROMOD database | PT_2024_b1_2015_03_e2 |
|----|----|
| Original name | EU-SILC |
| Provider | Eurostat |
| Year of collection | 2024 |
| Period of collection | Fieldwork executed between March and September |
| Income reference period | 2023 |
| Sampling | Stratified, multi-stage, clustered |
| Unit of assessment | Household and personal |
| Coverage | Private households (households living at private residential addresses). Individuals living in institutional households (e.g., in care or imprisonment institutions, etc.) are excluded. |
| Original sample size | 15,777 households (of which 37,524 individuals) |

Source: Eurostat EU-SILC (User Database, UDB), 2024 wave; Statistics
Portugal / INE ([www.ine.pt](http://www.ine.pt)). EUROMOD DRD codebook

## Sample quality and weights 

The Portuguese EU-SILC information regularly collected on an annual
basis through computer-assisted face-to-face interviews (CAPI) in the
second quarter of each year.

### Weights

Adjustments to the sample weights are made for the whole sample
(combining the four sub-samples) at household and individual level using
the SAS macro CALMAR. An integrative calibration is applied to ensure
consistency between households and individuals, because all household
members receive the same cross-sectional weight as the household they
belong to.

The estimated results are obtained using household and individual
weights, calibrated by region, household size, age, and sex.

The following table shows the descriptive statistics for the grossing-up
weights used.

<span id="_Toc222328581" class="anchor"></span>**Table 3.2** Descriptive
statistics of the grossing-up weight *rb050*

|                | EU-SILC UDB Portuguese data |
|----------------|----------------------------:|
| Number         |                      37,464 |
| Mean           |                      283.33 |
| Median         |                      184.43 |
| Maximum        |                    4160.074 |
| Minimum        |                       4.785 |
| Decile 1 (P10) |                       27.17 |
| Decile 9 (P90) |                      640.02 |

Source: Eurostat EU-SILC UDB, Portuguese data, 2024 wave

## Data adjustment 

Adjustments to the variables are kept to a minimum. Some minor data
cleaning is done to ensure that the relationships of individuals within
households are consistent. In order to guarantee consistency between
demographic and income variables which refer to the previous year (and
on which EUROMOD simulation are based), all children born between the
end of the income reference period and the data of the interview (60
cases) were dropped from the sample.

However, the weights were not readjusted to consider the drop of these
individuals. EUROMOD final sample contains 17,305 households and 37,524
individuals.

## Imputations and assumptions

### Time period

In the EU-SILC dataset, the income reference period is the previous year
of the survey. All monetary amounts are expressed in annual terms.
Dividing them by 12, these are converted into monthly amounts for the
EUROMOD database.

There are two age variables in the EU-SILC dataset: one relates to the
age of the individual at the moment of the survey, and the other to the
age at the end of the income reference period. EUROMOD uses the first
one to characterise all individuals in the dataset.

### Gross incomes

The EU-SILC survey contains information on both gross and net monetary
incomes, if applicable, and flag variables, which indicate if the
observation has been collected in a gross or net form.

Income data can be provided by respondents in either gross or net
values. Hence, the net series is obtained by Statistics Portugal using a
specific gross-to-net micro simulation model (see more information
regarding the model in Rodrigues, 2007).

### Disaggregation of harmonized variables and other imputations

Some variables required for the simulation of the tax-benefit system in
Portugal are not available in the EU-SILC UDB. However, the Euromod team
has also access to EMSD file provided by Eurostat that that contains
some national variables not included in the EU-SILC UDB. The use of the
EMSD file provided by Eurostat contains imputations in some variables
and a disaggregation of other variables.

The use of EMSD allows the split of the following variables:

1.  **Old age pension** splits into contributory pensions (*poac*) and
    means-tested non-contributory benefit for the elderly (*poanc* – old
    age social pension). The EMSD provides two variables obtained from
    the national EU-SILC PDB: *poact_nsilc* and *poanc_nsilc*. Each of
    those national variables are divided by 12, these are converted into
    monthly amounts for the EUROMOD database.

2.  **Unemployment benefit** in the UDB split into contributory
    unemployment benefit (*bunct*) and the means-tested unemployment
    benefit (*bunnc*). The splitting is based on the variables PY09g
    (Unemployment benefits – Contributory and means-tested) and PY092G
    (Unemployment benefits – Contributory and non-means-tested).

3.  **The aggregate family benefits** variable in the UDB splits into
    two components: child benefit (*bch*) and Other family benefits
    (*bfa*). The EMSD provides two variables obtained from the national
    EU-SILC PDB: *bch_nsilc*, *bcpn_nsilc*. Those variables are added
    and divided by 12 to obtain the monthly amount of *bch*. The
    difference between *bch* and *hy050*/12 are included in *bfa*.

4.  **Social exclusion benefits** split into three components:
    Solidarity supplement for the elderly (*bsaoa*), minimum income
    benefit (*bsa00*) and Other social assistance benefits (*bsaot*).
    The EMSD provides three variables obtained from the national EU-SILC
    PDB: *bsa00_nsilc*, *bsaoa_nsilc* and *bsaot_nsilc*. Each of those
    national variables are divided by 12, these are converted into
    monthly amounts for the EUROMOD database.

Education level is imputed to children aged under 16 according to their
age and the rules of the Portuguese education system.

Incomes reported at household level are assigned to the relevant member
of the household or to the first member closer to 45 years old.

## Extended input data (with household expenditures for the simulation of consumption taxes)

For the simulation of consumption taxes, the model needs to be run with
extended EUROMOD input files. They consist of the core EUROMOD input
files based on EU-SILC or National SILC, extended with new variables
(household-level income shares of expenditures by product) imputed from
EU/National-HBS. The semi-parametric method implemented for the
imputation follows the methodology developed by Akoğuz et al (2020).

Table 3.3 summarizes the major features of the most recent database used
to be run with the policy systems of 2022-2025.

<span id="_Toc222328582" class="anchor"></span>**Table 3.3** Extended
EUROMOD database description

| Extended EUROMOD database for the simulation of consumption taxes | SILC 2024 – Income year 2023 – Expenditures from HBS 2015 |
|----|----|
| EUROMOD database | PT_2024_b1_2015_03_e2 |
| Year of collection (HBS) and source | HBS 2015 – EU |
| Year of collection (SILC) and source | SILC 2024 – EU |
| Coverage and sample size | 15,777 households (37,524 individuals) |
| Share of households with negative incomes excluded from the matching procedure | 0% |
|  |  |

Notes:

z: source of expenditure shares data with u (EU-HBS), e (EMSD) n
(national HBS), a (admin data)

M: version of matching (correlative number), f: source of SILC dataset
(National, UDB, ESMD): a, b or c 

N: version of SILC processing (correlative number) 

Source: EU Household Budget Survey (EU-HBS)

These extended EUROMOD files contain all the variables included in the
standard EUROMOD input files plus the income shares of each consumption
category included in HBS. For example, for countries with consumption
disaggregation at 4 COICOP level (5 digits), there will be close to 200
additional variables, each one with the income shares of expenditure
(household level) for that particular consumption category (e.g.
starting from the income share of rice consumption: xs_01111; bread:
xs_01112, and so on and so forth). The number of additional variables
depends on the granularity available in HBS, and it varies across
countries).

For the case of Portugal, data PT_2024_b1_2015_03_e2, the number of
variables included (income shares of expenditures, xs_c\*) are 193,
corresponding to the harmonized consumption categories defined at COICOP
2003 level 4 (five digits)

This database is an extension of the core EUROMOD input database, and so
it is based on the same sample (i.e., same identifiers "idperson" and
"idhh" to identify persons and households, respectively) and contains
the same variables plus the income shares of expenditure (xs\_\*
variables).

In Table 3-4 we present the share of households' consumption
expenditures by product (and total) captured in our matched databases
(extended EM input files) with respect to the original reported
expenditures in HBS. The column that refers to the same year (in this
case, HBS 2015 with Extended EM Input 2015) directly depends on the
quality of the imputation procedure, while the comparison across
different years is influenced not only by the matching noise but also by
the changes in population characteristics and in the underlining
distribution of income. Therefore, the coverage displayed in the second
column is just informative but is not and should not be used to evaluate
nor validate the imputation procedure.

Information on the coverage of these simulated expenditures (coming from
the imputation of HBS 2015 to more recent SILC-based data) with respect
to the expenditures reported by National Accounts is included in section
4 of this report, together with the other macro-validation results.

Below we summarize the main findings from the imputation validation
checks for Portugal.

<span id="_Toc222328583" class="anchor"></span>**Table 3.4** Expenditure
coverage of Extended EM Input files

<table style="width:33%;">
<colgroup>
<col style="width: 5%" />
<col style="width: 13%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th>COICOP group</th>
<th style="text-align: right;">HBS 2015 – Extended EM Input 2015
(%)</th>
<th style="text-align: right;">HBS 2015 – Extended EM Input 2022
(%)</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="2"><p>1</p>
<p>2</p>
<p>3</p>
<p>4</p>
<p>5</p>
<p>6</p>
<p>7</p>
<p>8</p>
<p>9</p>
<p>10</p>
<p>11</p>
<p>12</p></td>
<td rowspan="2" style="text-align: right;"><p>103.7</p>
<p>116.4<br />
<br />
92.09</p>
<p>102.7</p>
<p>976</p>
<p>110.9</p>
<p>93.6</p>
<p>106.4</p>
<p>89.9</p>
<p>74.1</p>
<p>91.8</p>
<p>104.5</p></td>
<td rowspan="2" style="text-align: right;"><p>94.9</p>
<p>101.6</p>
<p>84.1</p>
<p>94.8</p>
<p>90.2</p>
<p>103.9</p>
<p>90.0</p>
<p>99.8</p>
<p>86.2</p>
<p>68.8</p>
<p>87.0</p>
<p>95.6</p></td>
</tr>
<tr>
</tr>
</tbody>
</table>

Source: EU HBS 2015, EU SILC 2015, EU SILC 2024

The original HBS data seems to be generally underestimating consumption
figures over National Accounts (NA) for Portugal, with a weighted
average of aggregate expenses shares equal to 64.4%. The only first
level COICOP groups that are within the 30% range are CP04, CP06, CP07,
CP08, and CP10.

The matching process generally worsen the coverage of NA consumption
(58.5%) respect to the performance of original HBS, specifically for the
COICOP groups CP03, CP04, CP05, CP07, CP09, CP10, CP11 and CP12. 

The matched SILC/HBS rates are in the acceptable range of 84.1%-103.9%
for all COICOP level 1 categories. On the 3-digit COICOP level, the
matching performs good, where we do not have deviations larger than 30%,
except for CP081(188.8%), and CP102 (55.4%).

## Uprating factors

Uprating factors are used to account for any time inconsistencies
between the input dataset and the policy year. Each monetary variable
(*i.e*., each income component) is updated to account for changes in the
non-simulated variables that have taken place between the year the data
was collected and the simulation year of the tax-benefit system.
Uprating factors are generally based on the changes in the average value
of the relevant income component between the two years. For detailed
information on the construction of each uprating factor and
corresponding sources, see Annex 1.

As a rule, uprating factors are given in Annex 1 for both simulated and
non-simulated income components included in the input dataset. Note,
however, that in the case of simulated variables, the actual simulated
amounts are used in the baseline rather than the uprated original
variables in the dataset. Uprating factors for simulated variables are
given to enable the user to turn off the simulation of a particular
variable if and when required.

# Validation

## Aggregate Validation 

In this section we assess the accuracy of EUROMOD based estimates by
reference to the following categories of groups of indicators:

(Non-Simulated) Market Incomes in the input dataset;

Simulated Taxes and Social Security contributions;

Simulated Benefits;

Simulated indicators of Income Distribution.

For each of these categories, we confront EUROMOD baseline estimates
with readily available official statistics, for the period between 2022
and 2025. It is important to remark that unlike in the previous Country
Report (‘PORTUGAL (PT) 2021-2024’), EUROMOD baseline simulations for the
2022-2025 system years are produced using two different datasets: 2024
dataset for the 2023-2025 policy systems, and 2023 dataset for the 2022
policy system.[^6] Hence, in some cases, the results presented here
might not be consistent with the assessment made in the previous Country
Report.

It is also important to remark that, since labour market transitions are
switched OFF in EUROMOD baselines, COVID-19 temporary measures (policies
*wage compensation scheme COVID-19* and *self-employed compensation due
to COVID-19*) do not produce any effect in baseline simulations, i.e.,
the EUROMOD results do not consider the effect of the pandemic in the
Portuguese economy.

### Components of disposable income

This subsection outlines the differences in the disposable income
definition in EUROMOD and EU-SILC 2024. The major components of
disposable income are the same in both sources: original incomes (+);
benefits (+), taxes (-), employee social insurance contributions (-);
and self-employed social insurance contributions (-). However, there are
two differences at the individual level components:

1.  The EU-SILC 2024 definition includes the (imputed) annual value of
    (using) a company car, while EUROMOD excludes it; and

2.  Pensions from individual private plans are included in the EUROMOD
    definition used in EUROMOD, while EU-SILC 2024 excludes it.

Besides these differences, the amount of the disposable income of the
same household can be different because the simulated income components
in EUROMOD can differ from their observed counterparts in EU-SILC
dataset.

**Table 4.1 Components of disposable income**

<table style="width:66%;">
<colgroup>
<col style="width: 22%" />
<col style="width: 9%" />
<col style="width: 7%" />
<col style="width: 22%" />
<col style="width: 3%" />
</colgroup>
<thead>
<tr>
<th rowspan="2" style="text-align: center;"></th>
<th rowspan="2"
style="text-align: center;"><strong>EUROMOD</strong></th>
<th rowspan="2" style="text-align: center;"><strong>EU-SILC
2024</strong></th>
<th rowspan="2" style="text-align: center;"><strong>Notes</strong></th>
<th></th>
</tr>
<tr>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>Household disposable income</td>
<td>ils_dispy</td>
<td>hy020</td>
<td></td>
<td></td>
</tr>
<tr>
<td>Employee cash or near cash income</td>
<td>yem</td>
<td>py010g</td>
<td>yem derived from py010g</td>
<td></td>
</tr>
<tr>
<td>Company car</td>
<td>-</td>
<td>py02g</td>
<td></td>
<td></td>
</tr>
<tr>
<td>Cash benefits or losses from self- employment</td>
<td>Yse</td>
<td>py050g</td>
<td>yse derived from py050g</td>
<td></td>
</tr>
<tr>
<td>Pension from individual private plans</td>
<td>ypp</td>
<td>-</td>
<td>ypp derived from py080g</td>
<td></td>
</tr>
<tr>
<td>Investment income</td>
<td>Yiy</td>
<td>hy090g</td>
<td>yiy derived from hy090g</td>
<td></td>
</tr>
<tr>
<td>Income from rental of a property or land</td>
<td>yprrt</td>
<td>hy040g</td>
<td>yprrt derived from hy040g</td>
<td></td>
</tr>
<tr>
<td>Income received by people aged under 16</td>
<td>yot</td>
<td>hy110g</td>
<td>yot derived from hy110g</td>
<td></td>
</tr>
<tr>
<td>Regular inter-household cash transfer received</td>
<td>ypt</td>
<td>hy080g</td>
<td>ypt derived from hy080g</td>
<td></td>
</tr>
<tr>
<td>Regular inter-household cash transfer paid (-)</td>
<td>xmp</td>
<td>hy130g</td>
<td>xmp derived from hy130g</td>
<td></td>
</tr>
<tr>
<td rowspan="2">Old age benefits</td>
<td>poact_s</td>
<td rowspan="2"><p>py100g</p>
<p>py102g</p>
<p>py103g</p>
<p>py104g</p></td>
<td rowspan="2">poact_s and poanc_s derived from the split of py100g
into contributory and non-contributory old age pensions</td>
<td></td>
</tr>
<tr>
<td>poanc_s</td>
<td></td>
</tr>
<tr>
<td>Survivors benefits</td>
<td>Bsu</td>
<td>py110g</td>
<td>bsu derived from py110g</td>
<td></td>
</tr>
<tr>
<td>Disability benefits</td>
<td>bdi</td>
<td>py130g</td>
<td>bdi derived from py130g</td>
<td></td>
</tr>
<tr>
<td rowspan="2">Unemployment benefits</td>
<td>bunct_s</td>
<td rowspan="2"><p>py090g</p>
<p>py09g</p>
<p>py092g</p></td>
<td>bunct_s derived from py092g</td>
<td></td>
</tr>
<tr>
<td>bunnc_s</td>
<td>bunnc_s derived from py09g</td>
<td></td>
</tr>
<tr>
<td>Housing allowances</td>
<td>bho</td>
<td>hy070g</td>
<td>bho derived from hy070g</td>
<td></td>
</tr>
<tr>
<td rowspan="2">Family/children related allowances</td>
<td>Bfa</td>
<td rowspan="2"><p>hy050g</p>
<p>hy053g</p></td>
<td>bfa derived from the difference between hy050 and hy053</td>
<td></td>
</tr>
<tr>
<td>bch_s</td>
<td>bch_s derived from hy053g</td>
<td></td>
</tr>
<tr>
<td>Education related allowances</td>
<td>bed</td>
<td>py140g</td>
<td>bed derived from py140g</td>
<td></td>
</tr>
<tr>
<td>Sickness benefits</td>
<td>bhl</td>
<td>py120g</td>
<td>bhl derived from py120g</td>
<td></td>
</tr>
<tr>
<td rowspan="3">Social exclusion not elsewhere classified</td>
<td>bsaot</td>
<td rowspan="3">hy060g</td>
<td rowspan="3">hy060g split into social integration income (bsa00_s),
solidarity supplement for the elderly (bsaoa_s) and other social
assistance benefits (bsaot)</td>
<td></td>
</tr>
<tr>
<td>bsaoa_s</td>
<td></td>
</tr>
<tr>
<td>bsa00_s</td>
<td></td>
</tr>
<tr>
<td rowspan="3">Tax on income and social contributions (-)</td>
<td>tin_s</td>
<td rowspan="3">hy140g</td>
<td rowspan="3">EUROMOD data includes three simulated components: tin_s
(simulated income tax); tscee_s (simulated SIC employee) and tscse_s
(simulated SIC self-employee).</td>
<td></td>
</tr>
<tr>
<td>tscee_s</td>
<td></td>
</tr>
<tr>
<td>tscse_s</td>
<td></td>
</tr>
<tr>
<td>Regular taxes on wealth (-)</td>
<td>Tpr</td>
<td>hy120g</td>
<td>tpr derived from hy120g</td>
<td></td>
</tr>
<tr>
<td colspan="4"><p>Note: all “_s” variables are EUROMOD simulated
benefits or taxes.</p>
<p>Source: Own elaboration</p></td>
<td></td>
</tr>
</tbody>
</table>

### Validation of market incomes

In this section, we assess (non-simulated) market incomes in EUROMOD’s
input dataset. As can be seen in Tables A3.1 and A3.2, there is no
readily available public statistics on the number of recipients and
annual amounts for the following income sources:

Income from private pensions (ypp);

Private transfers (ypt);

Maintenance payments (xmp);

Incomes from children under 16 (yot);

\[Covid-19\] Wage Compensation (paid by firms) (yemmc_s).

That being said, our analysis focuses on the following types of incomes,
as reported in input dataset:

Income from employment (yem);

Income from self-emplyment (yse);

Income from property (ypr);

Income from investments (yiy), amounts only;

Our analysis shows that:

The **number of individuals** reporting **receiving incomes from
employment** (yem) in EUROMOD’s input dataset is very much in line with
Bank of Portugal’s (quarterly) estimates on dependent employment (see
Table A3.1). The accuracy EUROMOD input dataset estimates is relatively
constant in the period for which there is external benchmark data
(2022-2024);

The total **amount of** **income from employment** (yem) in EUROMOD’s
input dataset is very much in line with data from the Portuguese Tax
Authority (see Table A3.2), on the amount of income from employment
reported on income tax assessments. The accuracy EUROMOD input dataset
estimates is relatively constant in the period for which there is
external benchmark data (2022-2023);

The **number of individuals** reporting **receiving incomes from
self-employment** (yse) in EUROMOD’s input dataset is very much in line
with Bank of Portugal’s (quarterly) estimates on self-employment (see
Table A3.1). Notheless, the accuracy EUROMOD input dataset estimates has
varied during the period for which there is external benchmark data
(2022-2024);

When compared with statistics from the Portuguese Tax Authority (see
Table A3.2) the total **amount of income from self-employment** (yse) in
EUROMOD’s input dataset is significantly overestimated – 55%, for the
latest available year (2023). There are two possible explanations, for
this. First, this could be the product of the wide range of exemptions
for self-employed in income tax and social security contributions rules,
which means that significant amounts of income from self-employment does
not have to be reported, and therefore is not captured in official
statistics. Second, given the significance of informal economy and tax
evasion in Portugal (see CEAFGEA, 2008) this might very well be related
with significant levels of under-reporting of income from
self-employment, for tax and social security purposes;

When compared with public statistics from the Portuguese Tax Authority
(see Table A3.1) the **number of individuals** reporting **receiving
income from property** (ypr) in EUROMOD’s input dataset is significantly
underestimated – by 23%, for the latest available year (2023). This
could, yet again, be a reflex of the size of informal economy and tax
evasion in the Portuguese economy, and in particular in the housing
sector – for which there is some evidence[^7];

When compared with public statistics from the Portuguese Tax Authority
(see Table A3.2), EUROMOD’s input dataset overestimates the total
**amount of income from property** (ypr) fairly substantially – 36% in
the latest year for which external data is available (2023).

When compared with public statistics from the Portuguese Tax Authority
(see Table A3.2) the total **amount of income from investments** (yiy)
in EUROMOD’s input dataset is significantly overestimated – 99%, for the
latest available year (2023). One possible explanation for this is that
EU-SILC is capturing undeclared or tax-exempt capital income.
Alternatively, this might be down to the fact that EU-SILC is capturing
capital income below tax filing thresholds that does not appear in
administrative tax data.

### Validation of taxes and social insurance contributions

In this section, we assess EUROMOD’s ability to simulate the taxes and
social security contributions paid in Portugal. As can be seen in Tables
A3.3 and A3.4, there is no readily available public statistics on the
number of recipients and annual amounts for the following taxes and
social security contributions:

Property tax (tpr);

Income tax on capital income (tiniy_s);

Extraordinary solidarity contribution on pensions (txcpe_s).

Hence, our analysis will focus on the following types of taxes/social
security contributions:

Personal Income Tax (tin_s);

Employee’s Social Security Contributions (tscee_s);

Employer’s Social Security Contributions (tscer_s);

Self-Employed Social Security Contributions (tscse_s).

Our analysis reveals that:

When compared with public statistics from the Portuguese Tax Authority
(see Table A3.3) the **number of individuals paying Personal Income**
Tax (tin_s) in EUROMOD’s input dataset is underestimated – by 14%, for
the latest available year (2023);

When compared with public statistics from the Portuguese Tax Authority
(see Table A3.4) the total **amount paid** in **Personal Income Tax**
(tin_s) simulated by EUROMOD is (slightly) overestimated – by 21%, in
2022, and by 7% in 2023. This might be explained by the fact that
EUROMOD does not simulate some of the full range of tax credits in the
legislation – such as tax credits for expenditures on private retirement
plans or investments in stocks, shares savings plans, etc.;

The **number of individuals paying** **Employee’s Social Security
Contributions** (tscee_s) simulated by EUROMOD is very much in line with
public statistics from the Social Security (see Table A3.3).
Unsurprisingly, as it refers to the same data, the **number of
individuals** for which **Employer’s Social Security Contributions**
(tscer_s) have been paid in EUROMOD’s input dataset is also very in line
with public statistics from the Social Security on this topic (see Table
A3.3);

When compared with public statistics from Social Security (see Table
A3.4) the **amount paid** in **Employee’s Social Security
Contributions** (tscee_s) and **Employer’s Social Security
Contributions** (tscer_s) simulated by EUROMOD is overestimated – by 26%
and 30%, respectively, for the latest available year (2023). This might
be explained by the fact EUROMOD does not simulate the large range of
reduced rates that apply to a number of occupations/sectors;.

When compared with public statistics from Social Security (see Table
A3.3) the **number of individuals paying** **Self-Employed Social
Security Contributions** (tscse_s) simulated by EUROMOD is significantly
underestimated – by 33%, for the latest available year (2023).

In contrast, the **amount of paid** in **Self-Employed Social Security
Contributions** (tscse_s) simulated by EUROMOD is significantly
overestimated – by 64%, for the latest available year (2023). This might
be explained by the fact EUROMOD does not simulate the full variety of
exemptions/ reduced rates that apply to self-employed workers

### Validation of benefits

In this section, we assess the simulated benefits in EUROMOD’s input
dataset. In order to provide a more systematic assessment, our analysis
will be structured in three stages:

Validation of Pension Benefits;

Validation of Non Means-Tested Benefits;

Validation of Means-Tested Benefits,

#### Validation of Pension Benefits

As can be seen in Tables A3.5 and A3.6, there is no readily available
public statistics on the number of recipients and annual amounts for the
Social Pension (poanc_s), hence our analysis here covers the following
pension benefits:

Contributory Old-Age Pension (poact_s);

Disability Pension (pdi);

Survivor Pension (psu);

Our analysis reveals that:

When compared with public statistics from the National Statistics Office
(INE) (see Table A3.5) the **number of individuals** receiving a
**Contributory Old-Age Pension** (poact_s) simulated by EUROMOD are
overestimated – by 31%, for the latest available year (2024);

The total **amount** of **Contributory Old-Age Pension** (poact_s)
**payments** simulated by EUROMOD is very much in line with public
statistics from the National Statistics Office (INE), (see Table A3.6);

The **number of individuals** receiving a **Disability Pension** (pdi)
in EUROMOD’s input dataset is broadly in line with public statistics
from the National Statistics Office (INE) (see Table A3.5). The accuracy
EUROMOD dataset estimates varies during the period for which there is
external benchmark data (2022-2024);

However, when compared with public statistics from the National
Statistics Office (INE) (see Table A3.6) the total **amount** of
**Disability Pension** (pdi) **payments** in EUROMOD’s input dataset
significantly underestimated – by 59%, for the latest available year
(2023).This might be a sign of severe under-reporting of the value of
Disability Pensions in EU-SILC;

When compared with public statistics from the National Statistics Office
(INE) (see Table A3.5) the **number of individuals** receiving a
**Survivor Pension** (psu) in EUROMOD’s input dataset is significantly
underestimated – by 36%, for the latest available year (2024).

In the same way When compared with public statistics from the National
Statistics Office (INE) (see Table A3.6) the total **amount** of
**Survivor Pension** (psu) **payments** in EUROMOD’s input dataset is
underestimated – by 25%, for the latest available year (2023). This
might be a sign of under-reporting of receipt and the value of Survivor
Pensions in EU-SILC.

#### Validation of Non Means-Tested Benefits 

As can be seen in Tables A3.5 and A3.6, there is no readily available
public statistics on the number of recipients and annual amounts for the
following benefits:

Parental Allowance (bplct_s)

Family Benefits (other than Child Benefit) (bfa)

Scholarships (bed);

\[Covid-19\] Wage Compensation (bwkmcee_s)

\[Covid-19\] Self-Employment Compensation (bwkmcse_s)

Hence, our analysis focuses on the following benefits:

Unemployment Insurance (bunct_s);

Sickness Benefit (bhl).

Our analysis reveals that:

When compared with public statistics from Social Security (see Table
A3.5) the **number of individuals** receiving **Unemployment Insurance**
[^8] (bunct_s) simulated by EUROMOD is underestimated – by 44%, for the
latest available year (2024). This may be explained by the fact that
unemployment insurance benefits cannot be fully simulated in EUROMOD, as
there is no information on the reason why people became unemployed
(voluntary or compulsory), nor on the duration of the most recent jobs.
Not only that, EUROMOD does not simulate the entitlement of (out of
work) self-employed persons.

When compared with public statistics from Social Security (see Table
A3.6) the total **amount** of **Unemployment Insurance** (bunct_s)
**payments** simulated by EUROMOD is underestimated – by 18%, for the
latest available year (2022).

When compared with public statistics from the National Statistics Office
(INE) (see Table A3.5) the **number of individuals** receiving
**Sickness Benefit** (bhl) in EUROMOD’s input dataset is significantly
underestimated – by 69%, for the latest available year (2023). One
possible explanation is that external data is constructed using sickness
episodes along the year and there is no information on the EU-SILC data
about the number of individuals experiencing various episodes along the
year (e.g., counting of a same individual experiencing various episodes
along the year). The accuracy EUROMOD dataset estimates is relatively
constant in the period for which there is external benchmark data
(2022-2023);

The total **amount** of **Sickness Benefit** (bhl) **payments** in
EUROMOD’s input dataset is broadly in line with public statistics from
the National Statistics Office (INE) (see Table A3.6). The accuracy
EUROMOD dataset estimates has improved in the period for which there is
external benchmark data (2022-2024).

#### Validation of Means-Tested Benefits 

As can be seen in Tables A3.5 and A3.6, there is no readily available
public statistics on the number of recipients and annual amounts for the
following benefits:

Housing Benefit (bho);

COST-of-LIVING: Housing Benefit (bhotn_s)

Prenatal Family Allowance (bmapr_s)

Parental Social Allowance (bplnc_s)

Other Social Assistance benefits (bsaot).

Family Income Support (2022) (bfaxp_s)

Extraordinary Supplement for Vulnerable Families (2023) (bfaxp01_s)

Therefore, our analysis focuses on the following types of simulated
means-tested benefits:

Child Benefit (bch_s)

Unemployment Assistance Benefit (bunnc_s)

Solidarity Supplement for Older Persons (bsaoa_s)

Social Insertion Income (bsa00_s).

Our analysis reveals that:

The **number of individuals** receiving **Child Benefit** (**bch_s**) in
EUROMOD’s input dataset is broadly in line with public statistics from
the National Statistics Office (INE) (see Table A3.5). The accuracy
EUROMOD dataset estimates has improved in the period for which there is
external benchmark data (2022-2024);

The **total amounts** paid concerning **Child Benefit** (**bch_s**)
simulated by EUROMOD is very much in line with public statistics from
the National Statistics Office (see Table A3.6). In fact, the accuracy
EUROMOD dataset estimates has significantly improved in last year of the
period for which there is external benchmark data (2022-2024);

When compared with public statistics from Social Security (see Table
A3.5) the **number of individuals** receiving **Unemployment
Assistance** (**bunct_s**) simulated by EUROMOD is significantly
underestimated – by 67%%, for the latest available year (2023). This
might be down to the fact that EUROMOD does not simulate the entitlement
to certain categories of entitlement to Unemployment Assistance;

When compared with public statistics from Social Security (see Table
A3.6) the **total amounts** of **Unemployment Assistance** (**bunct_s**)
payments simulated by EUROMOD are significantly underestimated – by 69%,
for the latest available year (2022). Again, this might be down to the
fact that EUROMOD does not simulate the entitlement to certain
categories of entitlement to Unemployment Assistance;

When compared with public statistics from the National Statistics Office
(see Table A3.5) the **number of individuals** receiving the
**Solidarity Supplement for Older Persons** (**bsaoa_s**) simulated by
EUROMOD is significantly overestimated – by 101%, for the latest
available year (2023). This might be explained by the fact that these
estimates are produced without the use of take-up adjustments.

The **total amounts** paid concerning **Solidarity Supplement for Older
Persons**[^9] (**bsaoa_s**) simulated by EUROMOD is very much in line
with public statistics from Social Security (see Table A3.6).

When compared with public statistics from the National Statistics Office
(see Table A3.5) the **number of individuals** receiving **Social
Insertion Income** (**bsa00_s**) simulated by EUROMOD is significantly
underestimated – by 47%, for the latest available year (2023).

The **total amounts** paid concerning **Social Insertion Income**
(**bsa00_s**) simulated by EUROMOD is very much in line with public
statistics from the National Statistics Office (see Table A3.6). The
accuracy EUROMOD dataset estimates has significantly improved in the
period for which there is external benchmark data (2022-2024).

### Validation of outputted (simulated) expenses

In this section, we assess the accuracy of EUROMOD estimates on:

1)  Household consumption expenditures (see Table A3.9);

2)  Revenues from consumption taxes (see Table A3.9 and Table A3.10)

The validation of simulated expenditures used to model consumption taxes
includes two types of comparisons:  

1.  Simulated household consumption expenditures compared to
    expenditures collected by National Accounts (NA) of that same
    year.  

<!-- -->

7.  Simulated consumption taxes (based on NA-adjusted simulated
    expenditures) compared to administrative data on consumption tax
    revenues. 

In what concerns the accuracy of EUROMOD’s **household consumption
estimates**, our analysis shows that:

As discussed in Section 3.5, if we take data on consumption National
Accounts as a benchmark, HBS data tends to underestimate the how much
Portuguese households spend on daily expenses. It is therefore not
surprising that the EUROMOD dataset significantly underestimates the
amount spent on a variety of goods, notably:

**Clothing and footwear**, by 58%, in the last year for which
information is available (2025);

**Alcoholic beverages, tobacco, etc**., by 58%, in the last year for
which information is available (2025);

**Hotels and restaurants**, by 54%, in the last year for which
information is available (2025);

**Furnishings, household equipment**, etc., by 54%, in the last year for
which information is available (2025);

**Recreation and culture**, by 46%, in the last year for which
information is available (2025).

Still, although the level expenditure is underestimated, EUROMOD
estimates are closer to the consumption figures in the National
Accounts. This is the case of **Health, Transport and Education
expenses** - which are underestimated by approximately 20%, in the last
year for which information is available (2025);

In contrast with this, household expenditures for **Housing, water and
fuel, and Communications** seem to be overestimated – by 30% and 15%,
respectively, in the last year for which information is available
(2025);

Bearing in mind that EUROMOD’s dataset underestimates household
expenses, it is not surprising that **estimates of consumption taxes
(VAT and Excises) revenues** are also generally underestimated,
regardless of how this is assessed.

As can be seen in Table A3.9, when compared with external data from
EUROSTAT, EUROMOD tends to underestimate the revenues from VAT and
excises:

**Revenues from VAT** are underestimated by 51%, in the last year for
which information is available (2024);

**Revenues from Excises** are also underestimated by 24%, in the last
year for which information is available (2023);

There are, however, significant variations in EUROMOD’s estimates of
revenues from excises:

Taking by reference the last year for which information is available
(2023), excise revenues from **Spirits** (88%), **Beer** (83%),
**Tobacco** (49%) and **Electricity** (31%) are (in some cases,
substantially) underestimated;

On the other hand, excise revenues from Energy (electricity, natural
gas, coal-coke) and Natural Gas are very significantly overestimated -
by over 4 and 2 times, respectively, in the last year for which
information is available (2023);

There might be various reasons for these discrepancies. Frist of all,
the afore mentioned underestimation of consumption in HBS. Another
possible reason lies in the fact that several organisations/sectors –
such as government and third sector, hospitals and business enterprises
such as financial companies - are themselves exempt from VAT but have to
pay the input VAT from all previous production stages. Moreover, there
are also private households - such as people in dormitories, jails, or
retirement homes – which are not covered by the HBS.

Acknowledging this, Table A3.10 shows adjusted consumption
estimates[^10], which provide an alternative benchmark to assess the
robustness of EUROMOD’s consumption tax revenues. Using this alternative
benchmark, our analysis shows that:

The accuracy of the **VAT** revenues’ estimates improves significantly.
Still, they remain underestimated - by 21%, in the last year for which
information is available (2024);

The accuracy of the **Excises** revenues’ estimates also improve
significantly. In fact, using this approach, Excises revenues are
significantly overestimated by 22% in the last year for which
information is available (2023);

However, the changes in the accuracy of Excises revenues are not linear
across the types of products being considered:

The Excise revenue estimates for **Tobacco** are the ones that benefit
the most from this approach. In fact, with this EUROMOD overestimates
(by 28%) Excise revenues for this product;

In some cases, such as **Spirits** and **Beer**, the accuracy of EUROMOD
increases significantly – even if Excise revenue estimates remain bellow
the eternal benchmark;

In contrast with this, the accuracy of Excise revenue estimates on
**Energy (electricity, natural gas, coal-coke)** actually worsens –
remaining largely overestimated.

## Income distribution 

In this section we assess the accuracy of EUROMOD estimates concerning
how disposable income is distributed in Portuguese society. Our analysis
focuses on two types of indicators:

Estimates on the level of inequality in the distribution of income;

Estimates on the level of poverty.

It should be noticed that the equivalised disposable income simulated in
EUROMOD is slightly different from the original EU-SILC data, namely
with regards:

The inclusion of different sources of income in the definition of
household income as mentioned earlier. For example, the EU-SILC includes
in disposable income (variable hy020) the company car (py021), which is
not included in EUROMOD; and EUROMOD includes pensions received from
individual private plans (py080) and repayments/receipts for tax
adjustment, not included EU-SILC;

Changes in the sample and weighting of the observations;

Changes in the amounts of some income sources due to their simulation in
EUROMOD:

In general, simulated social benefits rely on full take up, which should
generate significant differences in disposable income when compared to
EU-SILC;

The social supplement for the elderly constitutes an exception, as it is
adjusted so that simulated take up is coherent with actual take up. But
as EU-SILC underestimates the total amount received, there are again
differences between simulated and actual disposable income.

All income distribution results presented here are computed for
individuals according to their household disposable income (HDI)
equivalised by the “modified OECD” equivalence scale. HDI is calculated
as the sum of all income sources of all household members, net of income
tax and social insurance contributions. The weights in the OECD
equivalence are: first adult = 1; additional individuals aged 14+ = 0.5;
additional individuals aged under 14 = 0.3.

External benchmarks are based on income distribution statistics produced
by EUROSTAT, which are also based on EU-SILC. This means that the
‘income reference period, i.e. the year for which data on incomes is
collected, lags by one year the ‘period of collection of data’. Given
that the latest available EU-SILC data refer to the 2023 round, this
means that we only have external benchmarks for 2021 and 2022 (see
Tables A3.7 and A3.8).

### Income inequality

In this section we assess the accuracy of a set of estimates (produced
by EUROMOD) concerning the inequality in the distribution of income in
Portuguese society, namely:

Mean equivalised disposable income;

Median equivalised disposable income;

Share of national equivalised income, by decile;

Income quintile share ratio (S80/S20) for disposable income;

GINI coefficient of equivalised disposable income;

Our analysis shows that:

The estimates of **mean and median equivalised disposable income**
produced by EUROMOD are very much in line with external benchmarks
produced by EUROSTAT. The accuracy EUROMOD’s estimates has remained
relatively stable during the period for which there is external
benchmark data (2022-2023).

As can be seen in Table A3.7, EUROMOD’s estimates of how the **shares of
national equivalised income** are distributed across income deciles are
very much in line with EUROSTAT estimates. The only exception concerns
the share of national equivalised income of individuals in the first
income decile, which EUROMOD seems to overestimate - by 26%, for the
latest available year (2023);

This pattern is reflected in the accuracy of the measures of income
distribution produced by EUROMOD.

Reflecting the fact that it is more sensitive to what happens at the
extremes of the distribution of income, we observe that EUROMOD’s
estimates of **income quintile share ratio (S80/S20)** are
underestimated - by 14%, for the latest available year (2023). The
accuracy EUROMOD’s estimates has worsened during the period for which
there is external benchmark data (2022-2023);

Reflecting the fact that it is less sensitive to what happens at the
extremes of the distribution of income, we observe that the **GINI
coefficient** estimate generated by EUROMOD is very much in line with
external benchmarks produced by EUROSTAT. Still, the accuracy EUROMOD
dataset estimates has worsened in the period for which there is external
benchmark data (2022-2023).

### Poverty rates

In this section we assess the accuracy of EUROMOD-based estimates of
income poverty in Portuguese society. We start by looking at a
head-count index which measures the percentage of individuals with
incomes below 60% of the median equivalent disposable income. With the
aim of further assessing EUROMOD’s ability to produce accurate estimates
on the level and nature of income poverty, we complement this assessment
by looking at (see Table A3.8):

Poverty rate, 60% of the median disposable income, by gender;

Poverty rate, 60% of the median disposable income, by age group;

Poverty rate, using different poverty thresholds:

70% of the median disposable income;

50% of the median disposable income;

40% of the median disposable income.

Our analysis shows that:

The **poverty rate, at 60% of the median disposable income**, estimate
produced by EUROMOD is very much in line with external benchmarks
produced by the EUROSTAT. The accuracy EUROMOD’s estimates has remained
relatively stable during the period for which there is external
benchmark data (2022-2023).

EUROMOD-based **poverty rates, at 60% of the median disposable income,
by gender** are also very much in line with external benchmarks produced
by the EUROSTAT. Again, the accuracy of EUROMOD’s estimates has remained
relatively stable during the period for which there is external
benchmark data (2022-2023).

EUROMOD seems to underestimate the **percentage of young persons at risk
of income poverty (at 60% of the median disposable income)** - by 25%,
in the case of children up to 15 years; and, by 11% for persons between
16 and 25, and by 16% for persons between 25 and 49. The accuracy of
EUROMOD estimates for these age-groups has worsened in the period for
which there is external benchmark data (2022-2023).

In contrast , , EUROMOD tends to overestimate , by about 10%, the
percentage of individuals aged 65 and over, at risk of poverty (see
Table A3.8).

The accuracy EUROMOD poverty-related estimates decreases when more
strict poverty thresholds (in the sense that they capture a smaller
universe of people at risk of poverty) are used. Thus, EUROMOD seems to
underestimate the **percentage of people at risk of income poverty, at
50% of the median disposable income** - by 18%, for the latest available
year (2023). The **percentage of people at risk of income poverty, at
40% of the median disposable income** is also underestimated - by 29%,
for the latest available year (2023). In both cases, the accuracy
EUROMOD dataset estimates has worsened in the period for which there is
external benchmark data (2022-2023).

On the other hand, the **poverty rate, at 70% of the median disposable
income**, estimate produced by EUROMOD is very much in line with
external benchmarks produced by the EUROSTAT. The accuracy EUROMOD’s
estimates has remained stable during the period for which there is
external benchmark data (2021-2022).

## Health warnings

This final section summarises the main findings in terms of particular
aspects of the Portuguese part of EUROMOD or its database that should be
considered while using the model and interpreting its results.

Care should be taken in interpreting results for small sub-groups due to
small sample sizes.

The weights do not control for the variations of unemployment in
Portugal over the period under consideration.

No adjustments are made for structural changes in the characteristics of
the population between the data income collection year (2020) and the
simulation years.

The Portuguese version of the EU-SILC clearly underestimates some social
benefits, and this is not corrected by EUROMOD unless these benefits are
simulated.

The simulation of some benefits in EUROMOD is conditioned by the
difficulty of splitting some income variables from the EU-SILC user
database and by the difficulty some of the recipients have in clearly
identifying the source of their incomes.

Non-take-up of benefits is not modelled in most policies (the exception
being the Social Supplement for the Elderly). This has the effect of
inflating the simulated incomes of households who do not actually take
up these benefits. This is particularly relevant in the simulation of
child benefits and social integration income. And although the Social
Supplement for the Elderly simulation adjusts the number of recipients
to match the actual benefit’s take-up, as EU-SILC underestimates the
same number (and amounts), this has an impact on the comparison between
EUROMOD results and other indicators based on disposable income obtained
from EU-SILC (poverty rate, inequality indices, etc.).

Comparisons between EUROMOD and administrative figures on personal
income tax must take into consideration the existence of tax evasion, as
well as the lack of adequate information for the simulation of several
tax allowances and deductions.

Parental leave benefits are only simulated since 2015. They are defined
in an extension (Parental Benefits Extension) that is switched off in
the baselines, i.e., the non-simulated component (*bfa*) is being used.
When the extension is switched on, the non-simulated component is
reduced by subtracting the value of the simulated components (*bmapr_s,
bplct_s, bplnc_s*). The simulated numbers might differ significantly
from external statistics as some policy rules cannot be simulated
accurately due to lack of information in the underlying data.

The simulation of monetary compensation schemes (*yemcomp_pt* &
*ysecomp_pt*) is triggered by the simulation of labour market
transitions defined in policy *TransLMA_pt*. This policy becomes
operational if the model is run in conjunction with the LMA add-on. The
nature of these simulations is still experimental and only partially
validated. Users are encouraged to refer to the “Simulating labour
market transitions in EUROMOD” document prior to their use.

The simulation of consumption taxes sensitively depends on the quality
of the match of the extended EUROMOD files, as well as on the frequency
of this data and the gaps between the input data files and the policy
systems. At this point, the most recent HBS data available for all
countries (EU-HBS) is 2015.

When the user runs a policy system year (e.g., 2024) that does not
coincide with the incomes reported in the SILC-data used (e.g., 2022,
with reported incomes from 2021), expenditures in EUROMOD are simulated
under the constant income shares assumption (by default). This is
because the income shares of expenditure included in the extended input
files are not updated and remain constant regardless of the policy
system that is used for the simulation. This means that a household that
spends 10% of its income in food (e.g. the sum of all the xs_1\*
variables, i.e. xs01111, xs01112, and so on and so forth, is 0.10) will
still spend 10% of their income in 2024, regardless of the change in
incomes driven by the uprating factors and tax-benefit changes. This
implicitly assumes an income elasticity of one.

Labour market transitions are switched OFF in EUROMOD baselines. As a
consequence, the simulation of monetary compensation schemes does not
produce any effect in baseline simulations. Since all policies not
linked to labour market transitions are fully functional, it is possible
for disposable income in 2023 to be higher than disposable income in
previous years.

# References

CEAFGEA (2008). *Economia Informal em Portugal*. Centro de Estudos de
Gestão e Economia Aplicada, UCP, Porto.

INE (2019). *Inquérito às Condições de Vida e Rendimento – Documento
Metodológico (versão 3.7)*, Statistics Portugal, March 2019.

INE (2021) *Income and Living Conditions 2020 (Provisional Data)*,
Statistics Portugal Press Release of 7 February 2021.

INE (2023). Website database available at
[www.ine.pt](http://www.ine.pt)

RODRIGUES, C.F. (2007). *Income in EU-SILC - Net/Gross Conversion
Techniques for Building and Using EU-SILC Databases*, in Eurostat(ed),
*Comparative EU Statistics on Income and Living Conditions: Issues and
Challenges*. Eurostat, Luxembourg, pp 159-172.

Eurostat (2023). Website database available at
[www.ec.europa.eu/eurostat](http://www.ec.europa.eu/eurostat)

## Sources for tax-benefit descriptions/rules

Portuguese Fiscal System (in Portuguese):
<https://info.portaldasfinancas.gov.pt/pt/apoio_contribuinte/Folhetos_informativos/Pages/default.aspx>

Social benefits descriptions and rules (in Portuguese):
[www.seg-social.pt](http://www.seg-social.pt)

Online legislation (in Portuguese): [www.dre.pt](http://www.dre.pt)

# List of abbreviations and definitions

| Abbreviations | Definitions |
|----|----|
| BCA | Benefit Calibration Adjustment |
| BTA | Benefit Take-up Adjustment |
| CALMAR | Calibration macro in SAS for survey weight adjustment |
| CIA | Consumption Inflation Adjustment |
| COICOP | Classification Of Individual COnsumption according to Purpose |
| CPI | Consumer Price Index |
| CSI | Code on Social Insurance |
| CT | Consumption Taxes |
| DG | Directorate-General |
| DRD | Data Requirement Document |
| DG ECFIN | European Commission Directorate-General for Economic and Financial Affairs |
| EM | EUROMOD |
| DG EMPL | Directorate-General for Employment, Social Affairs and Inclusion |
| EMSD | EUROMOD SILC Database |
| ESTAT | Eurostat |
| EU | European Union |
| EUR | Euro |
| FYA | Full Year Adjustments |
| GDP | Gross Domestic Product |
| GJ | Gigajoule |
| HBS | Household Budget Survey |
| HDI | Household Disposable Income |
| HICP | Harmonised Index of Consumer Prices |
| INE | Instituto Nacional de Estatística |
| IRS | Imposto sobre o Rendimento das Pessoas Singulares |
| ISER | Institute for Social and Economic Research |
| ISP | Imposto sobre os Produtos Petrolíferos e Energéticos |
| IVA | Imposto sobre o Valor Acrescentado |
| JRC | Joint Research Centre |
| LMA | Labour Market Adjustment |
| LPG | Liquefied Petroleum Gas |
| MWA | Minimum Wage Adjustment |
| NA | National Account |
| NMW | National Minimum Wage |
| NRR | Net Replacement Rate |
| OECD | Organisation for Economic Co-operation and Development |
| PBE | Parental Leave Benefits |
| PDB | Production Database |
| PIT | Personal Income Tax |
| PT | Portugal |
| REFORM | European Commission Reform and Investment Task Force |
| RSI | Rendimento Social de Inserção |
| SAS | Statistical Analysis System (statistical software package) |
| SG | Secretariat-General |
| SIC | Social Insurance Contributions |
| SILC | Statistics on Income and Living Conditions |
| SSC | Social Security Contributions |
| SSI | Social Security Index |
| DG TAXUD | European Commission Directorate-General for Taxation and Customs |
| TEDB | Taxes in Europe Database |
| UAA | Uprating by Average Adjustment |
| UDB | User Database |
| VAT | Value Added Tax |

# List of figures

[**Figure A2** Policy effects in Portugal in 2024-2025, using the
HICP-indexation (HICP growth = 2.15%)
[124](#_Toc222328513)](#_Toc222328513)

# List of tables

[**Table 2.1** Simulation of benefits in EUROMOD \[2022-2025\]
[11](#_Toc222328520)](#_Toc222328520)

[**Table 2.2** Simulation of Extraordinary benefits in EUROMOD
\[2022-2025\] (Cont.) [12](#_Toc222328521)](#_Toc222328521)

[**Table 2.3** Simulation of taxes and social insurance contributions in
EUROMOD \[2022-2024\] [13](#_Toc222328522)](#_Toc222328522)

[**Table 2.4** Main policy changes \[2022-2025\] a, b, c
[14](#_Toc222328523)](#_Toc222328523)

[**Table 2.5** Changes to National Minimum Wage and Public Sector Wages
\[2024\] [20](#_Toc222328524)](#_Toc222328524)

[**Table 2.6** Changes to Pension Benefits \[2024\]
[21](#_Toc222328525)](#_Toc222328525)

[**Table 2.7** Indexation of Social Security Benefits \[2024\]
[22](#_Toc222328526)](#_Toc222328526)

[**Table 2.8** Changes to Non-Means Tested Social Security Benefits
\[2024\] [23](#_Toc222328527)](#_Toc222328527)

[**Table 2.10** Changes to Personal Income Tax \[2024, Azores &
Madeira\] [26](#_Toc222328528)](#_Toc222328528)

[**Table 2.11** Changes to National Minimum Wage and Public Sector Wages
\[2025\] [28](#_Toc222328529)](#_Toc222328529)

[**Table 2.12** Changes to Pension Benefits \[2025\]
[29](#_Toc222328530)](#_Toc222328530)

[**Table 2.13** Indexation of Social Security Benefits \[2025\]
[30](#_Toc222328531)](#_Toc222328531)

[**Table 2.14** Changes to Means Tested Social Security Benefits
\[2025\] [31](#_Toc222328532)](#_Toc222328532)

[**Table 2.15** Changes to Personal Income Tax \[2025, Continent\]
[33](#_Toc222328533)](#_Toc222328533)

[**Table 2.16** Changes to Personal Income Tax \[2025, Azores &
Madeira\] [34](#_Toc222328534)](#_Toc222328534)

[**Table 2.17** EUROMOD spine: order of simulation \[2022-2025\]
[35](#_Toc222328535)](#_Toc222328535)

[**Table 2.18** Characteristics of the Unemployment Benefit – Insurance
(*bunct_pt*) \[2022-2025\] [40](#_Toc222328536)](#_Toc222328536)

[**Table 2.19** Unemployment benefit – assistance (*bunnc_pt*): assessed
income [42](#_Toc222328537)](#_Toc222328537)

[**Table 2.20** Characteristics of the Unemployment Benefit – Assistance
(*bunnc_pt*) \[2022-2025\] [43](#_Toc222328538)](#_Toc222328538)

[**Table 2.21** Old age contributory pension: minimum amounts
\[2022-2025\] (monthly, in €) [43](#_Toc222328539)](#_Toc222328539)

[**Table 2.22** Old age social pension (*poanc_pt*) assessed income
[45](#_Toc222328540)](#_Toc222328540)

[**Table 2.23** Old age social pension (*poanc_pt*) amounts
\[2022-2025\] (monthly, in €) [45](#_Toc222328541)](#_Toc222328541)

[**Table 2.24** Solidarity supplement for the elderly (*bsaoa_pt*):
reference value (RV) \[2022-2025\] (annual, in €)
[46](#_Toc222328542)](#_Toc222328542)

[**Table 2.25** Solidarity supplement for the elderly (*bsaoa_pt*):
assessed income ‘Family Solidarity’
[47](#_Toc222328543)](#_Toc222328543)

[**Table 2.26** Solidarity supplement for the elderly (*bsaoa_pt*):
assessed income (Family Solidarity)
[48](#_Toc222328544)](#_Toc222328544)

[**Table 2.27** Solidarity supplement for the elderly (*bsaoa_pt*):
Family Solidarity scale \[2022-2025\]
[49](#_Toc222328545)](#_Toc222328545)

[**Table 2.28** Calculation of the solidarity supplement for the elderly
(*bsaoa_pt*) [49](#_Toc222328546)](#_Toc222328546)

[**Table 2.29** Social integration income (*bsa00_pt*): assessed income
[51](#_Toc222328547)](#_Toc222328547)

[**Table 2.30** Child benefit (*bch_pt*) income brackets upper bounds
(1) \[2022-2025\] [52](#_Toc222328548)](#_Toc222328548)

[**Table 2.31** Child benefit (*bch_pt*): assessed income
[53](#_Toc222328549)](#_Toc222328549)

[**Table 2.32** Child benefit (*bch_pt*) amounts \[2022\] (monthly, in
€) [53](#_Toc222328550)](#_Toc222328550)

[**Table 2.33** Child benefit (*bch_pt*) amounts \[2023\] (monthly, in
€) [54](#_Toc222328551)](#_Toc222328551)

[**Table 2.34** Child benefit (*bch_pt*) amounts \[2024\] (monthly, in
€) [54](#_Toc222328552)](#_Toc222328552)

[**Table 2.35** Child benefit (*bch_pt*) amounts \[2025\] (monthly, in
€) [54](#_Toc222328553)](#_Toc222328553)

[**Table 2.36** Child benefit (*bch_pt*): supplement for large families
\[2025\] (monthly, in €) [54](#_Toc222328554)](#_Toc222328554)

[**Table 2.37** Child Benefit (*bch_pt*): Child Guarantee \[2022\]
(Reference Amount, and Differential Payment, in €)
[55](#_Toc222328555)](#_Toc222328555)

[**Table 2.38** Child Benefit (*bch_pt*): Child Guarantee \[2023\]
(Reference Amount, and Differential Payment, in €)
[56](#_Toc222328556)](#_Toc222328556)

[**Table 2.39** Child Benefit (*bch_pt*): Child Guarantee \[2024\]
(Reference Amount, and Differential Payment, in €)
[56](#_Toc222328557)](#_Toc222328557)

[**Table 2.40** Child Benefit (*bch_pt*): Child Guarantee \[2025\]
(Reference Amount, and Differential Payment, in €)
[56](#_Toc222328558)](#_Toc222328558)

[**Table 2.41** Prenatal family allowance (*bmapr_pt*) income brackets
\[2022-2025\] [57](#_Toc222328559)](#_Toc222328559)

[**Table 2.42** Prenatal family allowance (*bmapr_pt*): assessed income
[58](#_Toc222328560)](#_Toc222328560)

[**Table 2.43** Prenatal family allowance (*bmapr_pt*) amounts
\[2022-2025\] (monthly, in €)\* [59](#_Toc222328561)](#_Toc222328561)

[**Table 2.44** Parental allowance (*bplct_pt*) amounts \[2022-2025\]
[60](#_Toc222328562)](#_Toc222328562)

[**Table 2.45** Parental social allowance (*bplnc_pt*): assessed income
[63](#_Toc222328563)](#_Toc222328563)

[**Table 2.46** Parental social allowance (*bplnc_pt*) amounts
\[2022-2025\] [63](#_Toc222328564)](#_Toc222328564)

[**Table 2.47** Personal income tax (*tin00_pt*): assessed income
(before allowances deduction) [67](#_Toc222328565)](#_Toc222328565)

[**Table 2.48** Personal income tax (*tin00_pt*) allowances \[2025\]
[67](#_Toc222328566)](#_Toc222328566)

[**Table 2.49** Youth Tax Allowance (IRS Jovem) \[2022-2025\]
[68](#_Toc222328567)](#_Toc222328567)

[**Table 2.50** Net income guarantee (‘*mínimo de existência*’)
\[2022-2025\] (€/year) [69](#_Toc222328568)](#_Toc222328568)

[**Table 2.51** Personal income tax (*tin00_pt*) marginal rates
\[2022-2025, Continent\] [71](#_Toc222328569)](#_Toc222328569)

[**Table 2.52** Personal income tax (*tin00_pt*) marginal rates
\[2022-2025, Azores\] [72](#_Toc222328570)](#_Toc222328570)

[**Table 2.53** Personal income tax (*tin00_pt*) marginal rates
\[2022-2025, Madeira\] [73](#_Toc222328571)](#_Toc222328571)

[**Table 2.54** Personal income tax (*tin00_pt*) credits \[2022-2025\]
[75](#_Toc222328572)](#_Toc222328572)

[**Table 2.55** Specific limits for housing tax credit \[2022-2025\]
[76](#_Toc222328573)](#_Toc222328573)

[**Table 2.56** Limits for tax credit \[2022-2025\]
[77](#_Toc222328574)](#_Toc222328574)

[**Table 2.57** VAT rates \[2022-2025\]
[79](#_Toc222328575)](#_Toc222328575)

[**Table 2.58** *Ad-valorem* excise rates \[2022-2025\]
[81](#_Toc222328576)](#_Toc222328576)

[**Table 2.59** Specific (*ad-quantum*) excise rates \[2022-2025\]
[81](#_Toc222328577)](#_Toc222328577)

[**Table 2.60** Specific (*ad-quantum*) excise rates \[2022-2025\]
(cont.) [82](#_Toc222328578)](#_Toc222328578)

[**Table 2.61** Prices of Excise products \[2022-2025\]
[83](#_Toc222328579)](#_Toc222328579)

[**Table 3.1** EUROMOD database description
[88](#_Toc222328580)](#_Toc222328580)

[**Table 3.2** Descriptive statistics of the grossing-up weight *rb050*
[89](#_Toc222328581)](#_Toc222328581)

[**Table 3.3** Extended EUROMOD database description
[91](#_Toc222328582)](#_Toc222328582)

[**Table 3.4** Expenditure coverage of Extended EM Input files
[92](#_Toc222328583)](#_Toc222328583)

[**Table AI.1** Monetary updating raw indices (in relation to 2006)
[117](#_Toc222328584)](#_Toc222328584)

[**Table A2.** Policy effects in Portugal in 2024-2025, using the
HICP-indexation (HICP growth = 2.15%)
[124](#_Toc222328585)](#_Toc222328585)

[**Table A3.** Validation Tables [126](#_Toc222328586)](#_Toc222328586)

# List of Annexes

## Annex 1. Uprating Factors

<span id="_Toc222328584" class="anchor"></span>**Table AI.1** Monetary
updating raw indices (in relation to 2006)

| **Indicator** | **Variable** | **2022** | **2023** | **2024** | **2025** | **Source/Comments** |
|----|:--:|:--:|:--:|:--:|----|:--:|
| Harmonised Index of Consumer Prices | \$HICP | 113.03 | 118.98 | 122.15 | 124.78 | EUROSTAT; AMECO 2025 spring forecasts for 2025 values |
| Consumer Price Index | \$f_cpi | 124.91 | 129.22 | 131.64 | 135.24 | CPI (Inflation Rate) - Year on Year Rate (Annual, 2006=100); Source: Bank of Portugal (Var. ID: 12704650) Latest year: 2026 Budget Report, Table 2.3, p. 29; Average gross monthly earnings per employee, private sector (Annual, 2006=100) - based on Social Security's Monthly Statement of Earnings (DMR) and Contributive Relation of the Caixa Geral de Aposentações (CGA), 2006-2013; NA: 2014-2024; INE (Var. ID: 0011137) Latest year: Estimate based on 2025 Budget Report, Table 1.2, p. 6; |
| Wages growth: private sector | \$f_wage1 | 145.6882 | 156.2064 | 165.9414 | 174.9022 | Average gross monthly earnings per employee, private sector (Annual, 2006=100) - based on Social Security's Monthly Statement of Earnings (DMR) and Contributive Relation of the Caixa Geral de Aposentações (CGA), 2006-2013; Source: INE (Var. ID: 0013137) Latest year: Decree 1/2005; Estimate base on increase for wages above remuneration level (TRU) 39, as this coincides with the average montly earnings per public sector worker (DGAEP) |
| Wages growth: civil servants | \$f_wage2 | 125.4174 | 133.1718 | 143.7461 | 146.9021 | Average gross monthly earnings per employee, private sector (Annual, 2006=100) - based on Social Security's Monthly Statement of Earnings (DMR) and Contributive Relation of the Caixa Geral de Aposentações (CGA); Source: INE (Var. ID: 0013137) Latest year: Decree 1/2005; Estimate base on increase for wages above remuneration level (TRU) 39, as this coincides with the average montly earnings per public sector worker (DGAEP) |
| Social Pension (poanc) | \$f_ben1 | 213.91 | 224.24 | 245.79 | 255.25 | Social Security website (base amount) |
| Social Insertion Income (bsa00) | \$f_ben2 | 189.66 | 209.11 | 237.25 | 242.23 | Social Security website (reference amount) |
| Solidarity Supplement for Older Persons (bsaoa) | \$f_ben3 | 5258.63 | 5858.63 | 7208.04 | 7668 | Social Security website (reference amount) |
| GDP | \$f_gdp | 243.96 | 270.35 | 289.43 | 295.2186 | Gross Domestic Product, at current prices, in nacional currency (Annual); Source: AMECO (Var. ID: UVGD); Latest year: 2025 Budget Report, Table 1.2, p. 6; Statistics Portugal: Average value of social security pensions, by Type of pension, Annual (Total divided by 12) |
| Average contributive old age pension | \$f_poact | 581.5 | 605.6667 | 642.0067 | 666.7239 | https://www.ine.pt/xportal/xmain/?xpid=INE&xpgid=ine_indicadores&indOcorrCod=0004347&contexto=bd&selTab=tab2&xlang=en Statistics Portugal: Average value of social security pensions, by Type of pension, Annual (Total divided by 12) |
| Average contributive disability pension | \$f_pdi | 480.8333 | 495.75 | 525.495 | 545.7266 | https://www.ine.pt/xportal/xmain/?xpid=INE&xpgid=ine_indicadores&indOcorrCod=0004347&contexto=bd&selTab=tab2&xlang=en |
| Social Support Index | \$f_ssi | 443.2 | 480.43 | 509.26 | 522.5 | Fixed by law: Ordinance nº 298/2022; https://files.dre.pt/1s/2022/12/24100/0001700017.pdf |
| Avg Mortgage Cost | \$f_mg | 267.6667 | 352.0833 | 403.75 | 395.7 | Average Loans (Annual, based on monthly values) Interest rates implicit in housing loans; Source: INE (Var. ID: 0008869); Latest year: Average Loan Repayments on Housing Loans; Estimate based on the values of the first 9 months; |
| Lead index of employment income | \$f_wage1lead | 149.19 | 156.8 | 164.17 | 173.0352 | CPI (Inflation Rate) - Year on Year Rate (Annual, 2006=100); Statistics Portugal: Average value of social security pensions, by Type of pension, Annual (Total divided by 12) |
| Average survivor pension | \$f_psu | 257.2143 | 268.1429 | 284.2314 | 295.1743 | https://www.ine.pt/xportal/xmain/?xpid=INE&xpgid=ine_indicadores&indOcorrCod=0004347&contexto=bd&selTab=tab2&xlang=en |
| Average hourly wage, Agriculture and Fishing (lindi = 1) | \$f_hourly_wage_lindi_1 | 6.3111 | 6.786 | 7.8995 | 8.2828 | Computed from ESTAT tables nama_10_a64 (wages) and nama_10_a64_e (hours worked) up to 2019 and for 2023 onwards. The values by sector for 2020-2022 are computed by non-linear interpolation between 2019 and 2023, following the trend for all sectors. Due to unavailability of 2025 data, values for this year are computed by multiplying the value of 2024 by the forecasted yearly increase of nominal compensation per employee, total economy, from AMECO. |
| Average hourly wage, Mining, Manufact. and Utilities (lindi = 2) | \$f_hourly_wage_lindi_2 | 10.1145 | 10.8537 | 11.4623 | 12.0184 | same as above |
| Average hourly wage, Construction (lindi = 3) | \$f_hourly_wage_lindi_3 | 8.9436 | 9.5421 | 10.0578 | 10.5458 | same as above |
| Average hourly wage, Wholesale and retail (lindi = 4) | \$f_hourly_wage_lindi_4 | 10.0236 | 10.6723 | 11.2807 | 11.828 | same as above |
| Average hourly wage, Hotels and restaurants (lindi = 5) | \$f_hourly_wage_lindi_5 | 8.6218 | 9.4475 | 9.9823 | 10.4666 | same as above |
| Average hourly wage, Transport and communication (lindi = 6) | \$f_hourly_wage_lindi_6 | 15.2282 | 16.379 | 17.4795 | 18.3275 | same as above |
| Average hourly wage, Financial intermediation (lindi = 7) | \$f_hourly_wage_lindi_7 | 21.034 | 22.2429 | 23.398 | 24.5331 | same as above |
| Average hourly wage, Real estate and business (lindi = 8) | \$f_hourly_wage_lindi_8 | 9.81 | 10.5858 | 11.2404 | 11.7857 | same as above |
| Average hourly wage, Public administ. and defence (lindi = 9) | \$f_hourly_wage_lindi_9 | 14.5297 | 15.3331 | 16.6449 | 17.4524 | same as above |
| Average hourly wage, Education (lindi = 10) | \$f_hourly_wage_lindi_10 | 12.3556 | 12.8199 | 13.9061 | 14.5807 | same as above |
| Average hourly wage, Health and social work (lindi = 11) | \$f_hourly_wage_lindi_11 | 11.2542 | 11.9365 | 12.9039 | 13.5299 | same as above |
| Average hourly wage, Other (lindi = 12) | \$f_hourly_wage_lindi_12 | 8.9411 | 9.533 | 10.1329 | 10.6245 | same as above |
| Average hourly wages (total wages / total hours)- All activity sectors | \$f_hourly_wage | 10.8268 | 11.5668 | 12.3367 | 12.9352 | same as above |
| Average hourly wages in the Previous year (total wages / total hours)- All activity sectors | \$f_hourly_wage_py | 10.3924 | 10.8268 | 11.6942 | 12.6299 | same as above |
| Average hourly wages in the Following year (total wages / total hours)- All activity sectors | \$f_hourly_wage_qt | 11.6942 | 12.6299 | 13.2427 | 13.8851 | same as above |

Source: Mentioned in the table

## Annex 2. Policy Effects in 2024-2025[^11]

Figure A.2 and Table A.2 show the effect that 2025 policies have on
disposable income by income component and income decile group on
average. The effect is estimated as the difference between simulated
household income under 2025 tax-benefit policies (deflating monetary
parameters by Eurostat’s Harmonized Index of Consumer Prices, HICP) and
net incomes simulated under the year 2024 policies, as a percentage of
mean equivalised household disposable income in 2024.

It’s important to note that the results presented here are in real
terms, which already incorporates how inflation eroded the real value of
the increases in social benefits and pensions between 2024 and 2025. The
HICP growth was milder in 2025 regarding the previous years, and, in
this way, the policy changes occurring in 2025 more than compensated the
inflation income erosion impact, leading to an increase of 1.52% of
households’ disposable income. While positive, this increase nonetheless
falls short of the values for 2024 – when disposable income grew by
2,87%.

Much of the (policy-related) increase in disposable income in 2025 is
largely explained by changes to Personal Income Tax, namely the broad
range reduction in tax rates (see Table 2-12, Section 2.24). In fact,
the changes to Personal Income Tax account for 3 quarters of overall
increase in disposable income. Other than that, the overall increase in
disposable income is explained by changes to public pensions (by just
over 13%), and to means-tested benefits (by about 7%). Unsurprisingly,
as there were no changes to this domain of public policy, social
insurance contributions (SICs) – both paid by employees and
self-employed – had no effect on the disposable income distribution.

The changes in disposable income across income groups reflect the
differentiated impact of the set of policies introduced during 2025.
Increases in disposable income have been stronger at the extremes of the
income distribution, particularly in the 9th and 10th deciles – where
disposable income grew by 1,87% and 2,09%, respectively. On the other
hand, disposable income in the 1st and 2nd deciles grew by 1,47% and
1,7%. Changes to Personal Income Tax have mostly benefited families in
the upper part of the income distribution. In fact, for the 9th and 10th
deciles, the (policy-related) increase in disposable income is almost
exclusively down to the changes in Personal Income Tax. Changes to
public pensions, on the other hand, have benefited those on the lower
echelons of the income distribution, particularly those in the 1st and
2nd deciles. This is consistent with the measures taken in this field,
namely the extraordinary pension increase of 1.25% and the Extraordinary
Pension Supplement – both targeted at pensioners with pensions up to
3\*SSI (see Table 2-12, Section 2.24). Reflecting the design of the
pension updating formula, which assigns below inflation pension
increases to individuals with higher pensions (see Table, 2-12, Section
2.24), public pensions contributed to marginally decrease the real
evolution of disposable income of households in the 10th decile.
Families in the lower income strata have also benefited from changes in
means-tested benefits, namely the 5% increase in the Solidarity
Supplement for the Elderly (CSI) (see Table, 2-14, Section 2.24).

<span id="_Toc222328513" class="anchor"></span>**Figure A2** Policy
effects in Portugal in 2024-2025, using the HICP-indexation (HICP growth
= 2.15%)

<img src="media/image2.svg" style="width:6.16597in;height:3.44861in" />

Source: Own elaboration

<span id="_Toc222328585" class="anchor"></span>**Table A2.** Policy
effects in Portugal in 2024-2025, using the HICP-indexation (HICP growth
= 2.15%)

| **Decile** | **Original income** | **Public pensions** | **Means-tested benefits** | **Non means- tested benefits** | **Employee SIC** | **Self-employed SIC** | **Other SIC** | **Direct taxes** | **Disposable income** |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | 0,00 | 0,47 | 0,71 | 0,11 | 0,00 | 0,00 | 0,00 | 0,17 | 1,47 |
| 2 | 0,00 | 0,64 | 0,84 | 0,08 | 0,00 | 0,00 | 0,00 | 0,14 | 1,70 |
| 3 | 0,00 | 0,42 | 0,06 | 0,08 | 0,00 | 0,00 | 0,00 | 0,22 | 0,77 |
| 4 | 0,00 | 0,39 | 0,08 | 0,07 | 0,00 | 0,00 | 0,00 | 0,44 | 0,97 |
| 5 | 0,00 | 0,31 | 0,00 | 0,07 | 0,00 | 0,00 | 0,00 | 0,54 | 0,91 |
| 6 | 0,00 | 0,26 | 0,04 | 0,06 | 0,00 | 0,00 | 0,00 | 0,79 | 1,15 |
| 7 | 0,00 | 0,22 | 0,06 | 0,06 | 0,00 | 0,00 | 0,00 | 0,97 | 1,31 |
| 8 | 0,00 | 0,19 | 0,03 | 0,04 | 0,00 | 0,00 | 0,00 | 1,18 | 1,44 |
| 9 | 0,00 | 0,10 | 0,05 | 0,04 | 0,00 | 0,00 | 0,00 | 1,69 | 1,87 |
| 10 | 0,00 | -0,03 | 0,02 | 0,03 | 0,00 | 0,00 | 0,00 | 2,06 | 2,09 |
| **Total** | 0,00 | 0,20 | 0,10 | 0,05 | 0,00 | 0,00 | 0,00 | 1,16 | 1,52 |

Note: shown as a percentage change in mean equivalised household
disposable income by income component and income decile group. Income
decile groups are based on equivalised household disposable income in
2022, using the modified OECD equivalence scale. Each policy system has
been applied to the same input data, deflating monetary parameters of
2024 policies by Eurostat’s Harmonized Index of Consumer Prices (HICP).

Source: Own elaboration

## Annex 3. Validation Tables

<span id="_Toc222328586" class="anchor"></span>**Table A3.** Validation
Tables

[^1]: Even though their simulation is switched off in the baseline. See
    section 2.3 and the corresponding policies’ descriptions for more
    information.

[^2]: For more information about the modelling of labour market
    transitions, please consult the “*Simulating labour market
    transitions in EUROMOD*” document.

[^3]: However, it is only possible to simulate the Family Solidarity
    component when both the recipient and descendants lived in the same
    household

[^4]: However, external statistics shows that it exists a clear
    preference on choosing 150 days (for the mothers, in the initial
    parent allowance). The same does not happen when one considers the
    initial parental social allowance.

[^5]: Since 2018 EU-SILC, the EUROMOD input data contains regional
    information at NUTS2 level, allowing to simulate the different
    existing tax schedules in Azores and Madeira.

[^6]: In the previous Country Report, we used the 2020 dataset for the
    2021 system year, and the 2021 dataset for the 2020, 2022, and 2023
    system years. As explained in the CR, this decision was made due to
    the significant impact of COVID on income in the 2021 dataset, which
    would have distorted the results. Consequently, by using the 2020
    dataset for the 2021 system year, we aimed to better replicate the
    decrease in the AROP rate in Portugal in 2021, as identified by
    ESTAT.

[^7]: For evidence of informal economy practices in the housing sector,
    see
    <https://www.publico.pt/2022/11/29/p3/noticia/metade-estudantes-mercado-arrendamento-estao-contrato-2029550>.

[^8]: External statistics source employed for Unemployment Benefits in
    the validation tables is no longer publicly available as of 2025.

[^9]: External statistics source employed for Solidarity Supplement for
    Older Persons and Social Insertion Income in the validation tables
    is no longer publicly available as of 2025.

[^10]: The original estimates are adjusted by reference to a ratio
    between (original) non-adjusted expenditures and EM simulated
    expenditures (aggregated at level 1) at the baseline.

[^11]: Consistent with the underlying methodology outlined in Bargain &
    Callan (2010) and applied to other EUROMOD countries, our analysis
    excludes simulations affecting public sector pay. Specifically, in
    the Portuguese context, this means that the wage growth for Public
    Servants in 2024 and 2025 is not factored into our results. To
    achieve this, the Uprate_yempb_pt policy was set to off in order to
    produce the PET results.
