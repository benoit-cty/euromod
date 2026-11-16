Cover

Contents

[Abstract [4](#_Toc222163629)](#_Toc222163629)

[Acknowledgements [5](#_Toc222163630)](#_Toc222163630)

[Authors [5](#_Toc222163631)](#_Toc222163631)

[1. Introduction [6](#introduction)](#introduction)

[1.1. Basic information [6](#basic-information)](#basic-information)

[1.2. Social Benefits [7](#social-benefits)](#social-benefits)

[1.2.1. Not strictly benefits
[10](#not-strictly-benefits)](#not-strictly-benefits)

[1.3. Social contributions
[10](#social-contributions)](#social-contributions)

[1.4. Taxes [11](#taxes)](#taxes)

[2. Simulation of taxes, social insurance contributions and benefits in
EUROMOD
[13](#simulation-of-taxes-social-insurance-contributions-and-benefits-in-euromod)](#simulation-of-taxes-social-insurance-contributions-and-benefits-in-euromod)

[2.1. Scope of simulation
[13](#scope-of-simulation)](#scope-of-simulation)

[2.1.1. Part-simulated tax-benefit components
[15](#part-simulated-tax-benefit-components)](#part-simulated-tax-benefit-components)

[2.2. Main policy changes
[16](#main-policy-changes)](#main-policy-changes)

[2.3. Order of simulation and interdependencies
[17](#order-of-simulation-and-interdependencies)](#order-of-simulation-and-interdependencies)

[2.4. Policy Extensions [19](#policy-extensions)](#policy-extensions)

[2.5. Benefits [21](#benefits)](#benefits)

[2.5.1. Unemployment benefit (Arbejdsløshedsdagpenge og andre
A-kasse-ydelser, *bunct_s*)
[21](#unemployment-benefit-arbejdsløshedsdagpenge-og-andre-a-kasse-ydelser-bunct_s)](#unemployment-benefit-arbejdsløshedsdagpenge-og-andre-a-kasse-ydelser-bunct_s)

[2.5.2. Social assistance (Kontanthjælp; Aktivering af
kontanthjælpsmodtagere; Integrationsydelse, bsa_s)
[24](#social-assistance-kontanthjælp-aktivering-af-kontanthjælpsmodtagere-integrationsydelse-bsa_s)](#social-assistance-kontanthjælp-aktivering-af-kontanthjælpsmodtagere-integrationsydelse-bsa_s)

[2.5.3. Child family grant (Børne- og ungeydelse, *bfachnm_s*)
[28](#child-family-grant-børne--og-ungeydelse-bfachnm_s)](#child-family-grant-børne--og-ungeydelse-bfachnm_s)

[2.5.4. Ordinary child benefit and supplement (Ordinært børnetilskud and
ekstra børnetilskud, *bfach00_s*)
[29](#ordinary-child-benefit-and-supplement-ordinært-børnetilskud-and-ekstra-børnetilskud-bfach00_s)](#ordinary-child-benefit-and-supplement-ordinært-børnetilskud-and-ekstra-børnetilskud-bfach00_s)

[2.5.5. Child benefit for student parents (Særligt børnetilskud til
uddannelsessøgende forældre, *bfached_s*)
[30](#child-benefit-for-student-parents-særligt-børnetilskud-til-uddannelsessøgende-forældre-bfached_s)](#child-benefit-for-student-parents-særligt-børnetilskud-til-uddannelsessøgende-forældre-bfached_s)

[2.5.6. Maternity (Graviditets- og Barselsorlov, bma_s), paternity
(Fædreorlov, bpa_s) and Parental leave (Forældreorlov, bma_s and bpa_s)
[31](#maternity-graviditets--og-barselsorlov-bma_s-paternity-fædreorlov-bpa_s-and-parental-leave-forældreorlov-bma_s-and-bpa_s)](#maternity-graviditets--og-barselsorlov-bma_s-paternity-fædreorlov-bpa_s-and-parental-leave-forældreorlov-bma_s-and-bpa_s)

[2.5.7. *Green check (Grøn check, bhtuc_s)*
[33](#green-check-grøn-check-bhtuc_s)](#green-check-grøn-check-bhtuc_s)

[2.5.8. Housing Allowance [34](#housing-allowance)](#housing-allowance)

[2.5.9. Housing Benefit (Boligsikring, *bho01_s*)
[34](#housing-benefit-boligsikring-bho01_s)](#housing-benefit-boligsikring-bho01_s)

[2.5.10. Housing grant (Boligstøtte, *bho02_s*)
[36](#housing-grant-boligstøtte-bho02_s)](#housing-grant-boligstøtte-bho02_s)

[2.5.11. Basic old age pension (Folkepension, poa00_s)
[37](#basic-old-age-pension-folkepension-poa00_s)](#basic-old-age-pension-folkepension-poa00_s)

[2.5.12. Old-age pension supplement (Pensionstillæg, *poa01_s*)
[37](#old-age-pension-supplement-pensionstillæg-poa01_s)](#old-age-pension-supplement-pensionstillæg-poa01_s)

[2.5.13. Supplementary pension (ældrecheck/supplerende pensionsydelse,
*poa02_s*)
[39](#supplementary-pension-ældrechecksupplerende-pensionsydelse-poa02_s)](#supplementary-pension-ældrechecksupplerende-pensionsydelse-poa02_s)

[2.5.14. Personal Supplement rate (Tillægsprocent, *poa02_s*)
[40](#personal-supplement-rate-tillægsprocent-poa02_s)](#personal-supplement-rate-tillægsprocent-poa02_s)

[2.6. Social insurance contributions
[41](#social-insurance-contributions)](#social-insurance-contributions)

[2.6.1. Supplementary labour market pension (ATP-bidrag, *tscpier_s*,
*tscpiee_s*)
[41](#supplementary-labour-market-pension-atp-bidrag-tscpier_s-tscpiee_s)](#supplementary-labour-market-pension-atp-bidrag-tscpier_s-tscpiee_s)

[2.6.2. Contribution to unemployment insurance scheme and early
retirement scheme (A-kasse-bidrag and Efterlønsbidrag, *tyrui_s*)
[42](#contribution-to-unemployment-insurance-scheme-and-early-retirement-scheme-a-kasse-bidrag-and-efterlønsbidrag-tyrui_s)](#contribution-to-unemployment-insurance-scheme-and-early-retirement-scheme-a-kasse-bidrag-and-efterlønsbidrag-tyrui_s)

[2.7. Direct Taxes [42](#direct-taxes)](#direct-taxes)

[2.7.1. Earned Income Tax Credit (Beskæftigelsesfradrag, tintc_dk):
[44](#earned-income-tax-credit-beskæftigelsesfradrag-tintc_dk)](#earned-income-tax-credit-beskæftigelsesfradrag-tintc_dk)

[2.7.2. Labour Market Contributions (Arbejdsmarkedsbidrag, txc_dk)
[45](#labour-market-contributions-arbejdsmarkedsbidrag-txc_dk)](#labour-market-contributions-arbejdsmarkedsbidrag-txc_dk)

[2.7.3. Municipality Tax (Kommuneskat, tmu_dk):
[45](#municipality-tax-kommuneskat-tmu_dk)](#municipality-tax-kommuneskat-tmu_dk)

[2.7.4. Church Tax (Kirkeskat, tcr_dk):
[46](#church-tax-kirkeskat-tcr_dk)](#church-tax-kirkeskat-tcr_dk)

[2.7.5. Bottom Bracket Income Tax (Bundskat, tinbt_dk):
[46](#bottom-bracket-income-tax-bundskat-tinbt_dk)](#bottom-bracket-income-tax-bundskat-tinbt_dk)

[2.7.6. Top Bracket Tax (Topskat, tinto_dk):
[47](#top-bracket-tax-topskat-tinto_dk)](#top-bracket-tax-topskat-tinto_dk)

[2.7.7. Property tax (tpr_s)
[48](#property-tax-tpr_s)](#property-tax-tpr_s)

[2.8. Extraordinary measures
[49](#extraordinary-measures)](#extraordinary-measures)

[2.8.1. Extra temporary child benefit (midlertidig børnefamilieydelse,
*bfachxp_s*)
[49](#extra-temporary-child-benefit-midlertidig-børnefamilieydelse-bfachxp_s)](#extra-temporary-child-benefit-midlertidig-børnefamilieydelse-bfachxp_s)

[2.8.2. Wage Compensation Schemes (yemcomp_dk, ysecomp_dk)
[49](#wage-compensation-schemes-yemcomp_dk-ysecomp_dk)](#wage-compensation-schemes-yemcomp_dk-ysecomp_dk)

[2.9. Consumption taxes [51](#consumption-taxes)](#consumption-taxes)

[2.9.1. VAT (il_tva) [51](#vat-il_tva)](#vat-il_tva)

[2.9.2. Ad-valorem excises (il_txv)
[51](#ad-valorem-excises-il_txv)](#ad-valorem-excises-il_txv)

[2.9.3. Specific excises (il_txa)
[52](#specific-excises-il_txa)](#specific-excises-il_txa)

[3. Data [54](#data)](#data)

[3.1. General description
[54](#general-description)](#general-description)

[3.2. Sample quality and weights
[55](#sample-quality-and-weights)](#sample-quality-and-weights)

[3.2.1. Non-response [55](#non-response)](#non-response)

[3.2.2. Weights [55](#weights)](#weights)

[3.3. Data adjustment [56](#data-adjustment)](#data-adjustment)

[3.3.1. Labour market activities, months per year
[56](#labour-market-activities-months-per-year)](#labour-market-activities-months-per-year)

[3.4. Imputations and assumptions
[57](#imputations-and-assumptions)](#imputations-and-assumptions)

[3.4.1. Time period [57](#time-period)](#time-period)

[3.4.2. Gross incomes [57](#gross-incomes)](#gross-incomes)

[3.4.3. Disaggregation of harmonised variables
[57](#disaggregation-of-harmonised-variables)](#disaggregation-of-harmonised-variables)

[3.5. Break in series [57](#break-in-series)](#break-in-series)

[3.6. Updating factors [58](#updating-factors)](#updating-factors)

[3.7. Extended input data (with household expenditures for the
simulation of consumption taxes)
[58](#extended-input-data-with-household-expenditures-for-the-simulation-of-consumption-taxes)](#extended-input-data-with-household-expenditures-for-the-simulation-of-consumption-taxes)

[4. Validation [61](#validation)](#validation)

[4.1. Aggregate Validation
[61](#aggregate-validation)](#aggregate-validation)

[4.1.1. Components of disposable income
[61](#components-of-disposable-income)](#components-of-disposable-income)

[4.1.2. Validation of incomes inputted into the simulation
[62](#validation-of-incomes-inputted-into-the-simulation)](#validation-of-incomes-inputted-into-the-simulation)

[4.1.3. Validation of outputted (simulated) incomes
[62](#validation-of-outputted-simulated-incomes)](#validation-of-outputted-simulated-incomes)

[4.1.4. Validation of outputted (simulated) expenses
[63](#validation-of-outputted-simulated-expenses)](#validation-of-outputted-simulated-expenses)

[4.2. Income distribution
[64](#income-distribution)](#income-distribution)

[4.2.1. Income inequality [64](#income-inequality)](#income-inequality)

[4.2.2. Poverty rates [64](#poverty-rates)](#poverty-rates)

[4.3. Summary of “health warnings”
[64](#summary-of-health-warnings)](#summary-of-health-warnings)

[References [66](#references)](#references)

[Sources for tax-benefit descriptions/rules
[66](#sources-for-tax-benefit-descriptionsrules)](#sources-for-tax-benefit-descriptionsrules)

[List of abbreviations and definitions
[67](#list-of-abbreviations-and-definitions)](#list-of-abbreviations-and-definitions)

[List of boxes [69](#list-of-boxes)](#list-of-boxes)

[List of figures [70](#list-of-figures)](#list-of-figures)

[List of tables [71](#list-of-tables)](#list-of-tables)

[List of Annexes [73](#list-of-annexes)](#list-of-annexes)

[Annex 1. Uprating Factors
[73](#annex-1.-uprating-factors)](#annex-1.-uprating-factors)

[Annex 2. Policy effects in 2024-25
[74](#annex-2.-policy-effects-in-2024-25)](#annex-2.-policy-effects-in-2024-25)

[Annex 3. Validation Tables
[76](#annex-3.-validation-tables)](#annex-3.-validation-tables)

<span id="_Toc222163629" class="anchor"></span>Abstract

The EUROMOD Country Reports have the double function of describing the
scope of the EUROMOD simulations, including the underlying assumptions,
and providing the validation of these simulations against official
statistics. The Country Report for Denmark is prepared by the Danish
EUROMOD National Team each year, and made available by the JRC on time
for the EUROMOD stable release of the model at the beginning of each
year.

<span id="_Toc222163630" class="anchor"></span>Acknowledgements

The work was carried out jointly by the EUROMOD core development team,
based at the JRC in Seville, and the Danish national team.

<span id="_Toc222163631" class="anchor"></span>Authors

The key contributors to this update were:

Bent Greve, Martina Bazzoli, Carlo Fiorio and Sonia Marzadro, as members
of the national team for Denmark

Ilda Dreoni, as JRC developer responsible for Denmark

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
Slovenia. It provides an overview of the Slovenian tax-benefit system in
2022-2025 and of how these policies are implemented in EUROMOD. The
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

## Basic information

Overall policies are uniform across regions and municipalities, with a
few differences arising from some discretionary benefits within the
social assistance area. There can be differences in access to services,
but the user charges are in principle the same for all, except in the
case of day care for children where they can vary among municipalities.
Municipalities, but not regions, have a possibility of setting the local
income and property tax. Property taxes within boundaries set by the
state.

The Fiscal Year follows the calendar year, e.g. from the 1st of January
to the 31st of December.

The right to state pension is at the age of 66.5 for those born until
the 1.7.1955 and 67 for those born since the 1st of July 1955. It is
possible for individuals to postpone the age of retirement and then
acquire a higher level of state pension. It is possible from 2020 to get
a pension for seniors (senior pension) who has reduced physical capacity
and only or able to work up to 15 hours per week in their present type
of job. There is from 2022 an early pension (tidlig pension) for persons
who has worked at least 42 years between the age of 16 and 61.

There is no minimum school leaving age, however children are obliged to
10 years of schooling (at a public school or at an equivalent level at
home, private schools etc.), typically starting in August the (calendar)
year the child turns 6 years.

Both adults and children are taxed individually, as a starting point.
However, minor incomes for children from e.g. help at home or at
parents’ company are disregarded. Child benefits are paid to the person
having custody and if split custody, to the parent where the child is
staying the most, and if this is even, to the parent where the child has
the address

The tax system is mainly based on individual personal taxation, although
there are a few possibilities for married spouses to, for instance,
transfer redundant deductions in the different tax bases.

A lone parent is defined as a person living alone (neither with a spouse
nor with a partner) taking care of a child below the age of 18. The
definition of living alone is not always clear. Children are always
defined as being below the age of 18.

Denmark to some degree has a dual tax system, where private capital
incomes are taxed at a different rate than labour and transfer incomes.
Both labour, transfer and capital incomes however are part of a
comprehensive personal income tax system and enter alongside into
various tax bases. Share income is taxed fully separately.

Taxes on labour and transfer incomes are withheld at source, through
third-party reporting and payment by employers etc. The tax assessment
is based on a preliminary assessment of income, which can be changed by
the taxpayer. After the end of an income year a final tax return has to
be filled in and/or confirmed by all taxpayers using a web-based
solution, but most items are filled in already through the third-party
reporting system. Payment of taxes might be changed during the year in
order to increase the likelihood that people’s actual income tax
payments reflect what they should actually pay during the year.

Benefits and deductions are both indexed automatically through an
adjustment of rates signed into law, according to which the indexation
follows wage inflation. Means-tested benefits are typically held up
against incomes from the most recent tax annual statement. However,
there is an obligation to inform the authorities if there are
substantial changes in income in order to change the benefit level
during the year

Consumption taxes consist of (1) VAT with one rate of 25 % except for
goods and services according to the EU rules exempted from VAT, (2)
excises on tobacco, alcohol, energy and other consumer goods, and (3)
purchase of motor vehicles.

The policy parameters saved as constants in the model and their values
for the most recent year are available at
[<u>https://euromod-web.jrc.ec.europa.eu/resources/parameters</u>](https://euromod-web.jrc.ec.europa.eu/resources/parameters). 

## Social Benefits

**Social assistance (*Kontanthjælp*):** Social Assistance is the basic
income maintenance instrument in the event of unemployment, long-term
illness, etc. The benefit level varies with age, provider status, by
whether recipient is living with parents and whether or not having a
formal education. It is means-tested against both own and a spouse’s
income and wealth.

**Self- and home-travel benefit (Selvforsørgelse og hjemrejseydelse
eller overgangsydelse):** People who have not lived in Denmark in 9 out
of the last 10 years will be given a specific lower benefit compared to
social assistance. The amount is at the level of the educational benefit
with possible extra support for six months having taken a Danish course
at a specified level. However, in so far as EU-citizens have the rights
to benefits according to EU rules on free movement they will be given
social assistance.

**Unemployment benefits (*Arbejdsløshedsdagpenge*):** UB are
insurance-based, but subsidized by the state. Set at 90 % of previous
labour income, but with an upper threshold. This is restricted to 2 out
of 3 years in a running 3 years period. The full right can be
re-established by 52 weeks of full-time work within 3 years running
time. The employer pays the first two days of unemployment. Since 2017 a
new system was implemented especially with regard to how to re-establish
the right to benefit, but also including a possibility of three days
within a year without benefit for those not having any work during the
year, and, lowering of the benefits for newly graduated without
children, see further details in Section 2.3.1.

**Sickness benefits (*Sygedagpenge*):** After eigth weeks of illness the
municipality ascertains the ability to work and eligibility for sickness
benefits. Benefit levels vary by number of pre-illness working hours
(full time/part time), but also the option of working a reduced number
of hours and receiving sickness benefits for other remaining hours. The
maximum duration of sickness benefit is 22 weeks within a period of 9
months after which a benefit at the level of social assistance is paid.
However, in contrast to social assistance it does not depend on spouse
or cohabitant person’s income and wealth and an increased effort is made
to assess how the recipient may be reintegrated into the labour market.
Receiving the benefit can be prolonged in case of a life-threatening
disease and in a few other cases[^1].

**Maternity (*Graviditets- og Barselsorlov*) and paternity leave benefit
(*Fædreorlov*):** Mothers are entitled to a leave 4 weeks prior to the
expected time of birth and 14 weeks after giving birth. Fathers are
entitled to 2 weeks after the birth. Hereafter there is a parental leave
of 32 weeks, which can be shared among the parents. Between 8 to 13
weeks of this leave can be postponed until the child reaches the age of
9, although only one of the parents has the right to do it, the other
might go on leave too if the employer agrees to it. Wage-earner,
self-employed and students are entitled to the leave benefit, but the
size of the benefit differs between the three groups. No income test
applies. Since 1st of August 2022 there will be, beside the four weeks
before expected time of birth, and the two weeks after birth to both
father and mothers, 24 weeks to each parent, of which 9 weeks can’t be
shared among the parents.

**Education grant (*Statens Uddannelsesstøtte, SU*):** Given to students
in validated branches of study. Benefit levels vary by age, type of
education and by whether living with parents or by oneself. Furthermore,
students have to prove that they are active students by passing exams.
And they can be received for a maximum of one year longer than the study
is set to.

**Child family grant (*Børnefamilieydelse*):** Families with children
below 18 are paid a tax-free child family grant, with benefit level
varying with the age of the child. The grant is automatically paid and
it is split in half between the two parents, unless the child after a
divorce is living more than 9 days by one of the parents where it then
will be paid to this person.

**Child benefits (*Børnetilskud*):** A number of different tax-free
child benefits are paid to families/children in special circumstances,
such as single parents/providers, pensioners or student parents, twins
etc.

**Child support (*Børnebidrag*):** After divorce, separation or
out-of-wedlock birth, parents are obliged to pay child support/alimony
to the child (that is, in practice to the upbringing parent). The amount
depends on the income of the person who has to pay within certain
brackets.

**Housing benefit (*Boligsikring*):** Tax-free benefits for tenants who
are not old-age pensioners. Given as a function of the rent (excl. costs
for heating) and family composition, etc. Phased out, based on household
income and wealth.

**Housing grant (*Boligydelse*):** Tax-free benefits for tenants who are
old-age pensioners. Given as a function of the rent (excl. costs for
heating) and family composition, etc. Phased out, based on household
income and wealth.

**Disability pension (*Førtidspension*):** Given to persons below
retirement age with permanently reduced ability to work after all other
possibilities to be or become self-supporting have been discarded. The
benefit is taxable. Benefit level varies with marital status. Phased out
against own and spouse’s income.

**Early retirement pension (*Efterløn*):** Full or partial retirement by
choice from the age of 64 years. It can be received until the standard
retirement age for the age cohort. It is conditional upon previous
unemployment insurance and pension contributions. If retirement is
postponed 2 years the individual receives higher benefits according to
rules that have been in place until the 1st of July, 2022.[^2]

**Old-age pension (*Folkepension*):** Given from age 67. Benefit level
varies with marital status. The benefit is since 2023 no longer phased
out against own or spouses labour income.

**Old-age pension supplement (*Pensionstillæg*)**: Given from age of
eligibility for old-age pension. Benefit level varies with marital
status. The benefit is phased out against both own and a spouse’s
income, except wage income.

**Heating subsidy (*Varmetillæg*):** Old-age and disability pensioners
can apply for a heating subsidy to cover parts of their costs for
heating fuel. Phased-out against income and wealth.

**Survivors benefits (*Efterlevelsespension*):** Old-age or disability
pensioners can receive a survivors benefit when the partner dies for a
period of 3 months. The monthly benefit is equal to the couple’s
combined pension payment.

**Survivors help (*Efterlevelseshjælp*):** A person, whose partner
(married or cohabitant) dies, can receive a lump-sum taxable benefit
dependent on income and whether having received survivors benefit.

**Old-age supplementary benefit (*Ældrecheck*):** Annual taxable benefit
paid out to all old-age pensioners with liquid financial assets below a
certain threshold and low income.

**Green check (*Grøn check*):** A tax-free lump sum benefit to
compensate for the increase in environmental and energy taxes, with
rates varying between adults and children. It will gradually be reduced
and phased out. This started in 2018, and is now only available for
pensioners dependent on income, see 2.5.8.

**Resource activity benefit (*Ressourceforløbsydelse*):** it is a social
assistance benefit, but it is no means tested according to spouse income
and wealth. It aims to support individuals who do not have any
work-ability left who might be entitled to disability pension.

### Not strictly benefits

**Flex-job benefit (*Fleksjobsydelse*):** It may be granted to employees
with permanent lack of abilities to work an ordinary full-time job. The
recipient works an agreed number of hours which is paid by the employer.
This salary will be supplemented with an unemployment benefit for up to
37 hours per week. Unemployed and early retirees may also have access to
flex-job benefits – and it is referred to as *ledighedsydelse* for
unemployed and *fleksydelse* for early retirees.

## Social contributions

Denmark has a number of contributory payments for the accruement of
unemployment benefits and old-age pensions. However, the major part of
transfer benefits is financed through the general tax system.

**Supplementary labour market pension (*Arbejdsmarkedets tillægspension,
ATP*):** Mandatory old-age pension contribution, paid with a fixed rate
that varies with the length of employment contract (e.g. monthly) and
the extent of work (full-/part-time). Paid by employee (one-third of
rate) and employer (two-third of rate). There can be slightly different
levels among sectors.

**Unemployment benefit contribution (*A-kasse-bidrag*):** Required for
eligibility to unemployment benefits (see above). Rates vary across
unemployment insurance funds due to differences in the cost of
administration as the payment otherwise reflect the level of
unemployment benefit set by the state. Deductible in taxable income.

**Payment for membership of trade unions:** Deductible in taxable income
with a maximum of 7,000 DKK in 2025.

**Early retirement pension scheme contribution (*Efterlønsbidrag*):**
Required for eligibility for early retirement pension scheme (see
above). Conditional upon unemployment insurance membership in a number
of years. Deductible in taxable income.

## Taxes

**Labour market contribution (*Arbejdsmarkedsbidrag*):** A tax of 8 %
levied upon gross labour income, with deduction of the employee-paid
part of the supplementary labour market pension contributions.

**Earned income tax credit (*Beskæftigelsesfradrag*):** Negative
marginal tax rate on labour income of 12.3 % in 2025, with a maximum
allowance of 55.600 DKK in 2025. For single income earners there is a
supplementary of 11.5 % with a maximum allowance of 48.300 DKK. Finally,
there is a job tax-credit (*jobfradrag*) of 4.5 % above labour income of
224.500 with a maximum of 2,900 DKK in 2024.

**Municipality tax (*Kommuneskat*):** The tax rate is determined
individually by the 98 municipalities, but collected through the state’s
tax system and levied upon the taxable income base after a personal
allowance. However, overall the average municipality tax shall in
principle not increase.

**Church tax (*Kirkeskat*):** A voluntary contribution collected through
the tax system, if the individual tax payer does not opt out. The rate
is based upon budget from the church and is determined individually by
the 98 municipalities and is on average 0.87 per cent.

**Bottom-bracket tax (*Bundskat*):** The lowest of the three progressive
state taxes. Tax rate is 12.01 % in 2025. Levied upon the sum of the
personal income tax base and net capital income, with the general
personal allowance subtracted. Spouses can transfer negative net capital
income and any unused personal allowance between them for the
calculation of the bottom-bracket tax.

**Top-bracket tax (*Topskat*):** The highest-level of the three
progressive state taxes. Tax rate of 15%. Levied upon the sum of the
personal income tax base, positive net capital income and contribution
to capital pension schemes, with the top-bracket tax allowance of
611.800 DKK in 2025 subtracted. There is a yearly allowance in 2025 of
52,400 DKK for the inclusion of positive net capital income.

**Tax ceiling (*Skatteloft*):** A ceiling at the level of 52.01% in 2025
on the aggregate (nominal) tax rate is implemented by reducing the tax
rate on the top-bracket tax by the difference between the tax ceiling
and the sum of the municipal and state taxes, excluding the church tax.

**Free telephone tax (*Fri telefon-skat*):** All tax payers, who have an
employer-provided telephone at their disposal. In 2025 it is the
income-tax of an amount of 3,300 DKK per year.

**Shares tax (*Aktieskat*):** Net income from shares (share profits,
dividends and premiums, minus losses) is taxed progressively below/above
61,000 DKK in 2024 with 27/42 %.

**Property value tax (*Ejendomsværdiskat*):** A progressive state tax on
the overall value of property, based on the official property value
estimate. Both this tax base and the threshold for the progressivity
have been frozen nominally since 2002. In 2024 a new tax base has been
enacted.

**Land value tax *(Grundskyld)*:** A municipal tax on the land value of
residential property with tax rates set by the municipalities varying
between 0,4 % and 1,3 %. New evaluation of the value of residential
property will be used from 2024 and onwards.

**Value-added tax (*Moms*):** Tax rate of 25 %. It is levied uniformly
upon all transactions with only exceptions of those areas identified by
the EU directives and on newspapers.

**Excise duties (*Punktafgifter*):** Various excise taxes with varying
tax rates or duties are levied upon goods such as cigarettes, energy
use, environmentally hazardous goods, chocolate and perfume. There are
variations in criteria for levying the duties, such as the amount of
alcohol, the burning value of energy and the value of cars.

**Inheritance tax (*Boafgift*):** The estate is taxed with 0 %, 15 % or
25.0 % for a spouse, near relatives or more distant relatives as heirs
above a threshold of 346,000 DKK in 2024.

**Gift tax (*Gaveafgift*):** Gifts are taxed with 0 %, 15 % or 36.25 %
for a spouse, near relatives or more distant relatives as recipients.
With a threshold for near relatives of 76,900 DKK in 2024.

**Pension saving reduction (*Ekstra pensionsfradrag*):** More 15 years
before pension age it is 12 % of pension saving (with a maximum of
10,056 DKK) and with less than 15 years before it is 32 % (with a
maximum of 26,816 DKK) of savings for pension purposes.

# Simulation of taxes, social insurance contributions and benefits in EUROMOD

## Scope of simulation

Tables 2.1 and 2.2 present an overview over the simulated benefits and
taxes and social contributions, respectively.

<span id="Table2_1" class="anchor"></span>**Table 2.1** Simulation of
benefits in EUROMOD

<table style="width:65%;">
<colgroup>
<col style="width: 13%" />
<col style="width: 8%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 1%" />
<col style="width: 8%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th rowspan="2"></th>
<th rowspan="2">Variable name</th>
<th colspan="5"></th>
<th colspan="2">Why not fully simulated?</th>
</tr>
<tr>
<th>2021</th>
<th>2022</th>
<th>2023</th>
<th>2024</th>
<th colspan="2"></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>Unemployment benefits</td>
<td>bunct_s</td>
<td>PS</td>
<td>PS</td>
<td>PS</td>
<td>PS</td>
<td colspan="2"></td>
<td>No data on unemployment history; Previous earnings inferred from
unemployment benefit received.</td>
</tr>
<tr>
<td>Benefits for partially disabled waiting for subsidized work or after
flex job</td>
<td>bunot</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td colspan="2"></td>
<td>No data on disabled waiting for subsidized work or flexjob.</td>
</tr>
<tr>
<td>Sickness benefits</td>
<td>bhl</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td colspan="2"></td>
<td>No data on health status connected to use of sickness benefit and
further also occupational based topping up.</td>
</tr>
<tr>
<td>Social Assistance</td>
<td>bsa_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td colspan="2"></td>
<td></td>
</tr>
<tr>
<td>Integration benefit</td>
<td>-</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td colspan="2"></td>
<td>No data on length of stay in Denmark (part of bsa_s).</td>
</tr>
<tr>
<td>Resource activity benefit</td>
<td>Bsaot</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td colspan="2"></td>
<td>Includes also other social assistance benefits.</td>
</tr>
<tr>
<td>Education grant</td>
<td>Bed</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td colspan="2"></td>
<td></td>
</tr>
<tr>
<td>Maternity/paternity leave</td>
<td>-</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td colspan="2"></td>
<td>Benefit included in employment income (yem) for public servants,
students and self-employed incl. in other child benefits (bfachot).</td>
</tr>
<tr>
<td>Child Family Grant</td>
<td>bfachnm_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td colspan="2"></td>
<td></td>
</tr>
<tr>
<td>Ordinary Child Benefit &amp; supplement</td>
<td>bfach00_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td colspan="2"></td>
<td></td>
</tr>
<tr>
<td>Child benefit for student parents</td>
<td>bfached_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td colspan="2"></td>
<td></td>
</tr>
<tr>
<td>Child benefits for twins etc. &amp; adoptions</td>
<td>bfachot</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td colspan="2"></td>
<td>Rare benefit. No information on adoption.</td>
</tr>
<tr>
<td>Child support</td>
<td>bfachot</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td colspan="2"></td>
<td>No information on parents outside household.</td>
</tr>
<tr>
<td>Disability pension</td>
<td>pdi</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td colspan="2"></td>
<td>No impartial information on ability to work.</td>
</tr>
<tr>
<td>Housing benefit</td>
<td>bho01_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td colspan="2"></td>
<td></td>
</tr>
<tr>
<td>Housing grant</td>
<td>bho02_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td colspan="2"></td>
<td></td>
</tr>
<tr>
<td>Heating benefit</td>
<td>poaot</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td colspan="2"></td>
<td></td>
</tr>
<tr>
<td>Early retirement pension</td>
<td>-</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td colspan="2"></td>
<td></td>
</tr>
<tr>
<td>Old-age pension</td>
<td>poa00_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td colspan="2"></td>
<td></td>
</tr>
<tr>
<td>Old-age pension supplement</td>
<td>poa01_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td colspan="2"></td>
<td></td>
</tr>
<tr>
<td>Old-age supplementary benefit</td>
<td>poa02_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td colspan="2"></td>
<td></td>
</tr>
<tr>
<td>Survivors benefits</td>
<td>psu</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td colspan="2"></td>
<td>No information on death of partner.</td>
</tr>
<tr>
<td>Payment for membership of trade unions</td>
<td>-</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td>E</td>
<td colspan="2"></td>
<td></td>
</tr>
<tr>
<td>Green check</td>
<td>bhtuc_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td colspan="2"></td>
<td></td>
</tr>
<tr>
<td>Employee compensation scheme COVID-19</td>
<td>bwkmcee_s</td>
<td>PS</td>
<td>PS</td>
<td>-</td>
<td>-</td>
<td colspan="2"></td>
<td>No data on employees entering in compensation scheme</td>
</tr>
<tr>
<td>Self-employed compensation scheme COVID-19</td>
<td>bwkmcse_s</td>
<td>PS</td>
<td>PS</td>
<td>-</td>
<td>-</td>
<td colspan="2"></td>
<td>No data on self-employed entering in compensation scheme</td>
</tr>
</tbody>
</table>

Notes: “-”: policy did not exist in that year; “E”: *excluded* from the
model as it is neither included in the micro-data nor simulated; “I”:
*included* in the micro-data but not simulated; “PS” *partially
simulated* as some of its relevant rules are not simulated; “S”
*simulated* although some minor or very specific rules may not be
simulated.

Source: Own elaboration

**\**

<span id="_Toc222163714" class="anchor"></span>**Table 2.2** Simulation
of taxes and social contributions in EUROMOD

<table style="width:65%;">
<colgroup>
<col style="width: 18%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 22%" />
</colgroup>
<thead>
<tr>
<th rowspan="2"></th>
<th rowspan="2" style="text-align: center;"><strong>Variable
name</strong></th>
<th colspan="5" style="text-align: center;"><strong>Why not fully
simulated?</strong></th>
</tr>
<tr>
<th style="text-align: center;"><strong>2021</strong></th>
<th style="text-align: center;"><strong>2022</strong></th>
<th><strong>2023</strong></th>
<th><strong>2024</strong></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>Labour market contribution</td>
<td>txc_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>S</td>
<td>-</td>
</tr>
<tr>
<td>Supplementary labour market contribution</td>
<td>tscpi_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>S</td>
<td>-</td>
</tr>
<tr>
<td>Contributions to unemployment insurance scheme &amp; early
retirement pension scheme</td>
<td>tyrui_s</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td>PS</td>
<td>PS</td>
<td>No individual data on contribution =&gt; randomly assigned from
population data.</td>
</tr>
<tr>
<td>Earned Income Tax Credit</td>
<td>tintc_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>S</td>
<td>-</td>
</tr>
<tr>
<td>Municipality tax</td>
<td>tmu_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>S</td>
<td>-</td>
</tr>
<tr>
<td>Church tax</td>
<td>tcr_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>S</td>
<td>-</td>
</tr>
<tr>
<td>Bottom-bracket tax</td>
<td>tinbt_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>S</td>
<td>-</td>
</tr>
<tr>
<td>Top-bracket tax</td>
<td>tinto_s</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>S</td>
<td>-</td>
</tr>
<tr>
<td>Multimedia tax (now tax on free telephone)</td>
<td>-</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td>E</td>
<td>E</td>
<td>No information on the tax base.</td>
</tr>
<tr>
<td>Shares tax</td>
<td>-</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td>E</td>
<td>E</td>
<td>No isolated data on share income</td>
</tr>
<tr>
<td>Property value tax</td>
<td>tpr_s</td>
<td style="text-align: center;">PS</td>
<td style="text-align: center;">PS</td>
<td>PS</td>
<td>PS</td>
<td>Tax base derived from tax payment.</td>
</tr>
<tr>
<td>Land value tax</td>
<td>-</td>
<td style="text-align: center;">I</td>
<td style="text-align: center;">I</td>
<td>I</td>
<td>I</td>
<td>No isolated data on the tax payment or on the land value.</td>
</tr>
<tr>
<td>Inheritance tax</td>
<td>-</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td>E</td>
<td>E</td>
<td>No information on inheritance</td>
</tr>
<tr>
<td>Gift tax</td>
<td>-</td>
<td style="text-align: center;">E</td>
<td style="text-align: center;">E</td>
<td>E</td>
<td>E</td>
<td>No information on gifts</td>
</tr>
<tr>
<td>VAT</td>
<td>-</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>S</td>
<td>Calculations based on extended input files with consumption
expenditures from HBS</td>
</tr>
<tr>
<td>Excise Duties</td>
<td>-</td>
<td style="text-align: center;">S</td>
<td style="text-align: center;">S</td>
<td>S</td>
<td>S</td>
<td>Calculations based on extended input files with consumption
expenditures from HBS</td>
</tr>
</tbody>
</table>

Notes: “-”: policy did not exist in that year; “E”: *excluded* from the
model as it is neither included in the micro-data nor simulated; “I”:
*included* in the micro-data but not simulated; “PS” *partially
simulated* as some of its relevant rules are not simulated; “S”
*simulated* although some minor or very specific rules may not be
simulated.

Source: Euromod

### Part-simulated tax-benefit components 

Some benefits use eligibility information from the data due to lack of
information in the data to simulate all eligibility rules. This is the
case for the unemployment insurance benefit (bunct_s). The benefit is
only simulated for those who receives the benefit as indicated in the
data. A similar case is the property value tax (tpr_s) which is imputed
from the paid property tax. The imputed value of property is used to
simulate the property tax. Also the contribution to unemployment
insurance (tyrui_s) is part-simulated as information on the
participation to the unemployment insurance is not available. This
information (lrg) is simulated through a discrete model based on
national administrative register data.

## Main policy changes

This section shows the main changes in policy, whereas minor adjustments
of, for example, income brackets in line with the rules for adjustment
can be found in the sections of the individual changes. In 2023 change
in rules related to the impact of wage income on pensions has been
abolished related to the spouse income. This has further been changed
from the 1st of January 2024 (and with the rules also having an impact
from the 1st of January 2023) so that in general wage income does not
have an impact on the basic state pension, whereas other types of income
still can have.

<span id="_Toc222163715" class="anchor"></span>**Table 2.3** Key Changes
in Danish Social Policy and Taxation (2022-2025)

<table style="width:65%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 16%" />
<col style="width: 13%" />
<col style="width: 10%" />
<col style="width: 11%" />
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
<td>Benefits</td>
<td><p>Early pension (Tidlig pension) started from 1<sup>st</sup> of
January 2022 based upon having at least 42 years of work after the age
of 16 and until 61 years of age.</p>
<p>Unemployed insured taking a vocational training can get 10 % higher
level of benefit</p></td>
<td><p>Basic state pension for a person is not influenced by wage income
from a spouse.</p>
<p>Possibility of higher unemployment benefits for the first year after
the 1<sup>st</sup> of May 2023.</p></td>
<td>.</td>
<td>With impact from the 1<sup>st</sup> of July 2025 there will be
change in grouping of social assistance</td>
</tr>
<tr>
<td>Social insurance contributions</td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>Direct taxes</td>
<td></td>
<td></td>
<td></td>
<td><p>Personal allowances changes so it is the same for all age groups.
There has been decided increase for 2025 for the earned income
tax-credit</p>
<p>Higher earned income tax-credits.</p>
<p>A higher level of supplementary pension (decided in late 2024) has
been paid out.</p></td>
</tr>
<tr>
<td>Duties</td>
<td>A slight lower lever of duties on electricity in the second half of
the year</td>
<td>Abolished for the first 6 months of most duties on electricity.</td>
<td></td>
<td></td>
</tr>
<tr>
<td>Other</td>
<td><p>Child benefit is paid with half to each parent, with a few
exceptions in case of divorce.</p>
<p>A temporary support of up to 6000 kroner for those with high increase
in heating cost (using gas or other heating with an increase in cost of
more than 65 %) and an income below 706,000 Danish kroner before labour
market contribution.</p>
<p>There has further been cap on increase in rent and lump sum payment
to pensioners receiving the supplementary pension of 2.500 D.Kr., most
students and other outside the labour market 2000 D.Kr. as well as a
higher employment allowance.</p></td>
<td>A one-time payment of 5000 D.Kr. to old age pensioners if they have
a total amount of wealth below95.500 D. Kr.</td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

Note: Some changes enacted in a year might be decided in a previous year
as implementation of, for example, a change in the tax-structure often
takes time. When there is a gradual implementation of new rules, such as
often the case within the tax-system, it is only mentioned in the first
year it is having an impact.

Source: [www.fm.dk](http://www.fm.dk), [www.bm.dk](http://www.bm.dk),
[www.skm.dk](http://www.skm.dk)

## Order of simulation and interdependencies

The following table shows the order in which the main elements of the
Danish system in 2022-2025 are simulated. The labour market contribution
and the supplementary labour market pension contribution are the first
instruments to be simulated, as both are functions of only gross
employment incomes.

Taxable benefits such as the unemployment benefit and social assistance
are simulated before the simulation of taxes, as they enter the tax
bases. Likewise, for the earned income tax credit, which is a function
of gross employment income and both the labour market contribution and
the supplementary labour market pension contribution.

<span id="_Toc222163716" class="anchor"></span>**Table 2.4** EUROMOD
Spine: order of simulation, 2021-2024

| **Policy** | **Description** | **Main output** |
|----|----|----|
| xpp00_dk | Contribution to private pensions that can be deducted from personal income | xpp00_s |
| Ysecomp | Self-employed compensation scheme COVID-19 | bwkmcse_s |
| txc_dk | Labour Market Contribution, a gross tax on all employment income | txcee_s, txcse_s, txc_s |
| [tscpi_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#tscpi_dk!A1#tscpi_dk!A1) | Supplementary labour market pension contribution, a mandatory pension contribution | tscpiee_s, tscpier_s |
| tintaox_dk | Additional deduction | tintaox_s |
| [tyrui_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#tyrui_dk!A1#tyrui_dk!A1) | Unemployment benefit contribution and early retirement pension contribution, voluntary contribution to individual unemployment benefit insurance/early retirement accounts | tyrui_s |
| [bunct_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#bunct_dk!A1#bunct_dk!A1) | Unemployment benefits and similar benefits | bunct_s |
| bma_dk<sup>S</sup> | Mother’s component of maternity and parental leave | bma_s |
| bpa_dk<sup>S</sup> | Father’s component of paternity and parental leave | bpa_s |
| [tintc_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#tintc_dk!A1#tintc_dk!A1) | Earned Income Tax Credit | tintc_s |
| [poa_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#poa_dk!A1#poa_dk!A1) | Old age pension benefits (basic amount) supplement pension and old-age supplementary benefit | poa00_s, poa01_s, poa02_s |
| [bsa_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#bsa_dk!A1#bsa_dk!A1) | Social Assistance | bsa_s |
| [tmu_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#tmu_dk!A1#tmu_dk!A1) | Municipality Tax | tmu_s |
| [tcr_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#tcr_dk!A1#tcr_dk!A1) | Church Tax | tcr_s |
| [thl_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#thl_dk!A1#thl_dk!A1) | Health Contribution, a tax | thl_s |
| [tinbt_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#tinbt_dk!A1#tinbt_dk!A1) | Bottom Bracket Tax | tinbt_s |
| tinmd_dk | Medium Bracket Tax | tinmd_s |
| [tinto_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#tinto_dk!A1#tinto_dk!A1) | Top-bracket tax | tinto_s |
| [tpr_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#tpr_dk!A1#tpr_dk!A1) | Property Tax | tpr_s |
| [bfachnm_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#bfachnm_dk!A1#bfachnm_dk!A1) | Child Family Grant | bfachnm_s |
| [bfach00_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#bfach00_dk!A1#bfach00_dk!A1) | Ordinary child benefit & Supplementary child benefit | bfach00_s |
| [bfached_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#bfached_dk!A1#bfached_dk!A1) | Child benefit for student parents | bfached_s |
| [bho01_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#bho01_dk!A1#bho01_dk!A1) | Housing Benefit | bho1_s |
| [bho02_dk](file:///C:\Documents%20and%20Settings\atumino\EuromodFiles\Param\Denmark.xls#bho02_dk!A1#bho02_dk!A1) | Housing Grant | bho2_s |
| bhtuc_dk | Green check | bhtuc_s |
| bfachxp_dk | Extra child benefit | bfachxp_s |
| Yemcomp | Employee compensation scheme COVID-19 | bwkmcee_s |

Note: Switched off in the baseline

Source: Euromod

COVID-19 policies are not included in the baseline even if they are “on”
in the spine given that they only work when labour market transitions
(TransLMA) are switched on.

<span id="_Toc222163717" class="anchor"></span>**Table 2.5** EUROMOD –
Indirect Taxation spine: order of simulations \[2021 - 2024\]

<table style="width:67%;">
<colgroup>
<col style="width: 9%" />
<col style="width: 20%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
</colgroup>
<thead>
<tr>
<th rowspan="2"><strong>Policy</strong></th>
<th><strong>Description</strong></th>
<th><strong>Main output</strong></th>
<th colspan="5" style="text-align: center;"><strong>Year</strong></th>
</tr>
<tr>
<th></th>
<th></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"><strong>2021</strong></th>
<th style="text-align: center;"><strong>2022</strong></th>
<th style="text-align: center;"><strong>2023</strong></th>
<th style="text-align: center;"><strong>2024</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>SetDefault_cc</td>
<td>Default values</td>
<td></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
</tr>
<tr>
<td>Uprate_cc</td>
<td>Uprating factors</td>
<td></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
</tr>
<tr>
<td>ConstDef_cc</td>
<td>Constants</td>
<td></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
</tr>
<tr>
<td>ILsDef_cc</td>
<td>Standard income concepts</td>
<td></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
</tr>
<tr>
<td>TransLMA_cc</td>
<td>Modelling labour market transitions</td>
<td></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">off</td>
<td style="text-align: center;">off</td>
<td style="text-align: center;">off</td>
<td style="text-align: center;">off</td>
</tr>
<tr>
<td>tco_cc</td>
<td>Consumption taxes</td>
<td>il_tva, il_txa, il_txv</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
<td style="text-align: center;">on</td>
</tr>
</tbody>
</table>

Source: Euromod

## Policy Extensions

There is no minimum wage extension.

**HHoT – Non-compulsory payments (HHoT_ncp):** this extension permits to
switch on or off the simulation of non-compulsory payments (i.e. taxes
or social insurance contributions) when using EUROMO-HHoT. The default
choice is off, i.e. not to simulate non-compulsory payments when the
model is used with hypothetical data, in order to only reflect the parts
of the tax system that are mandatory. However, such elements could be
incorporated in the simulations, should it be of interest for the
hypothetical family-types under analysis.

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

**Benefit Calibration Adjustments (BCA),** allowing the user to
calibrate the receipt of benefits to match the simulated total
expenditure of a benefit to real expenditure from external statistics.
The extension is implemented for the simulation of the social assistance
benefit (bsa_cc). The default for the baseline is off. When the
extension is on, a subset of eligible of observations is selected
randomly as beneficiaries so that the real expenditure is reached,
removing the benefit from the rest of the eligible observations; when
off, all eligible observations are kept as beneficiaries. This extension
shares most of its functions with the BTA extension; as a general rule,
only one of the extensions should be on, but if both are, the lowest
rate between the take-up rate and the calibration rate will be applied.
More details on the specific implementation of BCA and BTA extensions
are provided in the subsections describing the corresponding benefit.  

**Benefit Take-up Adjustments (BTA)**, allowing the user to apply
non-take-up corrections.  The  extension  is  used  for  the 
simulation  of material need benefits (bsa_cc). The default for the
baseline is off. When the extension is on, a share of (weighted)
eligible observations equal to the take-up rate is selected randomly as
beneficiaries, removing the benefit from the rest of the eligible
observations; when off, all eligible observations are kept as
beneficiaries. This extension shares most of its functions with the BCA
extension; as a general rule, only one of the extensions should be on,
but if both are, the lowest rate between the take-up rate and the
calibration rate will be applied. More details on the specific
implementation of BCA and BTA extensions are provided in the subsections
describing the corresponding benefit. 

BTA and BCA extensions are off, so the baseline model neither adjusts
for non-take-up of the benefit nor calibrates its receipt, but the user
can activate them if necessary. See section 2.4 for technical details on
both extensions and their interactions. 

Users can enable the necessary extensions in Country Tools/Set Switches.
For proper functioning, the extensions require the following inputs: 

BTA: The estimated take-up rate of the benefit should be set as the
value of the \$bsa_BTA_rate constant in the model. Currently, the value
is set to 1, indicating no adjustment for non-take-up. 

BCA: The aggregate expenditure of benefit recipients needs to be filled
out in the External Statistics table, so that the calibration rate
(\$bsa_BCA_rate) is computed accordingly. Data are currently available
for the years 2018-2023; given the absence of information for 2024, the
calibration rate is not computed within the 2024 system, but the one
computed within the 2023 system is used instead. For the modelling of
reforms, the 2024 system should be used in order to allow for variation
in the number of beneficiaries (hence expenditure): beneficiaries will
change when the eligibility conditions change by applying the share of
2023 to the new pool of eligible units. If previous systems were used
for reforms, total expenditure would remain constant irrespective of the
reform applied, since the model would always stick to the existing
external statistics. 

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

### Unemployment benefit (Arbejdsløshedsdagpenge og andre A-kasse-ydelser, *bunct_s*)

<span id="_Toc222163718" class="anchor"></span>**Table 2.6**
Characteristics of the unemployment benefit

<table style="width:65%;">
<colgroup>
<col style="width: 7%" />
<col style="width: 10%" />
<col style="width: 13%" />
<col style="width: 12%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 8%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr>
<th></th>
<th></th>
<th><strong>2022</strong></th>
<th colspan="3"><strong>2023</strong></th>
<th><strong>2024</strong></th>
<th colspan="4"><strong>2025</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Eligibility</strong></td>
<td>Contribution period</td>
<td colspan="9">1,924 hours during the last 3 years</td>
</tr>
<tr>
<td></td>
<td>Other conditions</td>
<td colspan="9">Member of unemployment insurance fund for at least 12
months prior to unemployment unless having participated in education for
at least 18 months or served military service.</td>
</tr>
<tr>
<td></td>
<td>Eligibility of self-employed</td>
<td>Yes</td>
<td colspan="3">Yes</td>
<td colspan="2">Yes</td>
<td colspan="3">Yes</td>
</tr>
<tr>
<td><strong>Payment</strong></td>
<td>Contribution base</td>
<td colspan="9"><p>.</p>
<p>Average employment income of the 12 highest income months out of the
last 24 months prior to unemployment.</p></td>
</tr>
<tr>
<td></td>
<td>Basic amount</td>
<td colspan="9">90% of the contribution base (different for those in
education or military service, see below)</td>
</tr>
<tr>
<td></td>
<td>Additional amount</td>
<td colspan="9">No additional amount.</td>
</tr>
<tr>
<td></td>
<td>Floor</td>
<td colspan="9">No minimum amount.</td>
</tr>
<tr>
<td></td>
<td>The first three months after at least 4 months membership of
unemployment insurance fund</td>
<td>-</td>
<td>281,388</td>
<td colspan="6">290,388</td>
<td>300,840</td>
</tr>
<tr>
<td></td>
<td>Ceiling thereafter</td>
<td>232,212</td>
<td colspan="2">236,736</td>
<td colspan="5">244,308</td>
<td>253,104</td>
</tr>
<tr>
<td><strong>Duration</strong></td>
<td>Standard (in months)</td>
<td colspan="9">24 months</td>
</tr>
<tr>
<td></td>
<td>Special cases (in month)</td>
<td colspan="9"><p>Possibility to extend for another 12 months if
working a limited number of hours while unemployed. Every hour in
employment increases the duration by 2 hours (up to 1,924 hours). The
hourly wage must be above 136,81 DKK in 2024.</p>
<p>The duration may also be reduced by 1 day if the unemployed person
works less than 148 hours during 4 months of unemployment.</p>
<p>For students/conscripts without from the 1<sup>st</sup> of May 2023 a
maximum of 12 months of benefits is available.</p></td>
</tr>
<tr>
<td><strong>Subject to</strong></td>
<td>Taxes</td>
<td>Yes</td>
<td colspan="3">Yes</td>
<td colspan="3">Yes</td>
<td colspan="2">Yes</td>
</tr>
<tr>
<td></td>
<td>Social Insurance Contribution</td>
<td>No</td>
<td colspan="3">No</td>
<td colspan="3">No</td>
<td colspan="2">No</td>
</tr>
</tbody>
</table>

Source: [www.bm.dk](http://www.bm.dk) and
[www.borger.dk](http://www.borger.dk)

#### Definitions

The unit of analysis is the individual (tu_individual_dk).

#### Eligibility conditions 

For members of an unemployment insurance fund (member for at least one
year) experiencing unemployment. Benefit is paid for a maximum of 2
years within a three-year time-period. Beneficiaries need to be in work
for a minimum of 1,924 hours during the last three years. Having been
conscript as well as having had an education of at least 18 months also
gives right to be member of an unemployment insurance fund (and even
without a one-year membership have the right to receive benefits). The
duration benefit receipt can be prolonged from 2 to up to 3 years if the
unemployed person is working for a limited number of hours while
unemployed. This measure has been implemented in order to encourage
participation in the labour market even if the unemployed person cannot
find full-time employment. If a person, even if unemployed, can get work
for just a few hours, a week or so the rule is that for every hour
worked while actually unemployed, the unemployed person can prolong
receipt of the benefit for two more hours with a total maximum of 1,924
hours (which represents one full year of employment) of extra
unemployment benefits. This means that the unemployed person has to work
on average 9.3 hours per week for two years in order to receive the
unemployment benefit for an additional year. Only hours reported to the
central tax-system by the employer are counted as working hours and the
hourly wage may not be lower than 142.15 DKK in 2025. Unemployed persons
can gain extra hours of unemployment benefit but also face the risk of
losing benefit if they are not employed. Those who do not work 148 hours
(which is equivalent to 9.3 hours per week) during 4 months of
unemployment will lose one day of the benefit. This is repeated for
every four months a person is unemployed. Unemployment benefit is paid
per hour and not per day.

Since 2022 for unemployed insured person above the age of 30
participating in vocational training in areas on a list where there is
lack of manpower the benefit was raised to be10 percentages points
higher than normal unemployment benefit. There is a higher benefit for
the first three months of unemployment starting on the first of May
2023, thus first fully yearly impact from 2024. The policy is partially
simulated as we lack information on total number of years of membership
to the unemployment fund.

#### Income test

Upper limit on the received benefit, see below.

#### Benefit amount

90 per cent of the previous employment income (yempv), with an upper
limit of 253,104 DKK per year in 2025. For conscripts and those having
had education of at least 18 months the ceiling will be 82 % of the
maximum benefit for those being providers and 71.5 % for those not being
providers. Since 2017 the calculation of the 90 % with the upper limit
will be based upon the highest income in 12 months out of the last 24
months. The calculation used to be based on the wage of the last 3
months prior to unemployment in previous years. The upper limit varied
across years according to the table below:

<span id="_Toc222163719" class="anchor"></span>**Table 2.7** Upper
limits for unemployment benefits per year (DKK)

|                                        | **2022** | **2023** | **2024** | **2025** |
|----------------------------------------|----------|----------|----------|----------|
| Upper limit                            | 232,212  | 236,736  | 244,308  | 253,104  |
| Upper limit for the first three months | \-       | 281.388  | 290,388  | 300,840  |
| Students/Conscripts                    |          |          |          |          |
| With dependent child                   | 190,416  | 194,124  | 200.328  | 207,540  |
| Without dependent child                | 166,037  | 169,272  | 174.686  | 180,972  |
|                                        |          |          |          |          |

Note: A higher upper limit for the first three months of unemployment
has been introduced in 2023. In 2025 is 300,840 D.Kr.. For
students/conscripts with or without children below the age of 30 the
upper limit is always lower (in 2025 207,540 and 180,972 respectively).

Source: [www.borger.dk](http://www.borger.dk) and
[www.bm.dk/satser](http://www.bm.dk/satser)

**EUROMOD modelling:**

**1)** Membership of an unemployment fund (lrg=1) is simulated through a
discrete model based on national register data.

**2)** The maximum amount of benefit that can be received varies
according to the insurance status of the recipient, e.g. part-time
insured vs. full-time insured. Only full time insurance is assumed in
the EUROMOD simulation. The maximum amount for part-time insured people
is equal to 2/3 of the full time maximum. The upper limit for conscripts
and students is not taken into account due to missing information on the
previous labour market status.

**3)** Previous employment income is not recorded by EU-SILC. For this
reason, starting from the benefit amount, the previous employment income
is calculated for those receiving the benefit by reversing the benefit
rule. The unemployment benefit is then simulated using the simulated
previous earnings.

**4)** The new reform that requires unemployed to be employed is not
implemented given the availability of data.

**5)** The additional benefit for unemployed participating in vocational
training is not simulated due to data availability.

### Social assistance (Kontanthjælp; Aktivering af kontanthjælpsmodtagere; Integrationsydelse, bsa_s)

#### Definitions

The unit of analysis is the individual (tu_individual_dk), although
married partner’s income, wealth and the presence of dependent children
enter in the simulation (tu_bsa_dk). Children are defined as younger
than 18 years.

#### Eligibility conditions 

Eligibility is conditional upon:

The person has experienced a change in the living situation (e.g.
unemployment, divorce, etc.) and the person is not able to maintain a
living

Economic needs cannot be fulfilled by other means, including wealth

The person is an EU citizen or has stayed in Denmark for 9 out of the
last 10 years

No other income (il_bsa=0).

#### Income test

The income test is satisfied if the recipient does not have any income
and any financial wealth left. Financial assets less than 10,000 DKK
(20,000 DKK) for single (married) recipients are disregarded from the
income test.

Married persons are obliged to support each other. For this reason,
incomes of the married partner are withdrawn from the amount received by
the person entitled. The benefit withdrawal starts in principle from the
earned income albeit with a reduction in 2025 of 31,46 DKK per worked
hour.

<span id="_Toc222163574" class="anchor"></span>**Box 1.** Income
included in income test

Income included in the income test:

\+ (Self-)Employment income

\+ Pension related benefits

\+ Disability benefits

\+ Unemployment related benefits

\+ Net capital income

\+ Wealth (above the threshold)

#### Benefit amount

The tables below describe the benefit amount for entitled individuals.
Differences in amounts arise with respect to the age of the claimant,
her/his provider status, whether she/he lives with her parents. The
provider status is simulated in EUROMOD by controlling for the presence
of children in the family.

Since 2014 social assistance has in principle been abolished for those
below the age of 30 who do not provide for a child and whose highest
education is primary or lower. The benefit is substituted by an
education grant if they participate in vocational training and, under
certain conditions, by an activity grant. The table below illustrates
benefit entitlement.

<span id="_Toc222163720" class="anchor"></span>**Table 2.8** Social
assistance benefits, per month per person. DKK

|  | **2022** | **2023** | **2024** | **2025** |
|----|:--:|:--:|:--:|:--:|
| Provider (over 30 or under 30 and not married) | 15,570 | 15,874 | 16,382 | 16,972 |
| Provider (under 30 and married) | 10,412 | 10,615 | 10,955 | 11,349 |
| Non provider over 30 or over 25 with more than primary education | 11,716 | 11,944 | 12,316 | 12,770 |
| Non provider between 25 and 30 with primary education or less | 6,420 | 6,545 | 6,754 | 6,997 |
| Non-provider younger than 25 with more than primary education |  |  |  |  |
| \- living by oneself | 7,552 | 7,699 | 8,494 | 8,231 |
| \- living with parents | 3,644 | 3,715 | 4,382 | 3,972 |
| Non-provider younger than 25 with primary education or less (education grant) |  |  |  |  |
| \- living by oneself | 6,420 | 6,545 | 6,754 | 6,997 |
| \- living with parents | 2,766 | 2,820 | 2,910 | 3,015 |

Source: [www.bm.dk](http://www.bm.dk) and
[www.borger.dk](http://www.borger.dk)

Benefit amounts received by providers are subject to a reduction if the
child is not living in Denmark. This rule does not apply if the child
lives in an EU/EEA country or in other countries where specific
agreements are in place. Before making reduction in social assistance
when working, a certain amount of employment income is disregarded. In
2025, benefit recipients are allowed to earn 31,46 DKK per hour for a
maximum of 160 hours per month.

Social assistance inflation compensation (Kontanthjælp inflations
compensation, bsaxp_s). For families on social assistance and with
children under 18 years old there was an inflation compensation in 2023
with the following yearly amounts:

1 child 7500

2 children 11250

3 children and more 13500

The amount was tax free and did not have any impact on other benefits.

<span id="_Toc222163721" class="anchor"></span>**Table 2.9** Deduction
of employment income, amount per working hour (DKK)

|               | **2022** | **2023** | **2024** | **2025** |
|---------------|----------|----------|----------|----------|
| Hourly income | 28.46    | 29.43    | 30.37    | 31,46    |

Source: www.borger.dk

A benefit ceiling for receiving social assistance and other benefits, as
described in the next sentence, exists. It includes the following
benefits: social assistance, integration benefit, educational allowance
and specific means tested benefits, such as housing benefit, housing
grant, support for payment of day-care. It cannot be reduced to be below
the level of social assistance and not reduced with more than the sum of
specific support and housing benefits.

<span id="_Toc222163722" class="anchor"></span>**Table 2.10** Ceiling
per month and household before tax (Danish Kroner)

<table style="width:71%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
</colgroup>
<thead>
<tr>
<th></th>
<th colspan="2" style="text-align: center;"><strong>2022</strong></th>
<th colspan="2" style="text-align: center;"><strong>2023</strong></th>
<th colspan="2" style="text-align: center;"><strong>2024</strong></th>
<th colspan="2" style="text-align: center;"><strong>2025</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td></td>
<td><strong>Standard</strong></td>
<td><strong>Reduced</strong></td>
<td style="text-align: center;"><strong>Standard</strong></td>
<td style="text-align: center;"><strong>Reduced</strong></td>
<td style="text-align: center;"><strong>Standard</strong></td>
<td style="text-align: center;"><strong>Reduced</strong></td>
<td style="text-align: center;"><strong>Standard</strong></td>
<td style="text-align: center;"><strong>Reduced</strong></td>
</tr>
<tr>
<td>Single without children</td>
<td style="text-align: center;">14,171</td>
<td>5,616</td>
<td style="text-align: center;">14,447</td>
<td style="text-align: center;">5,726</td>
<td style="text-align: center;">14,909</td>
<td style="text-align: center;">5,909</td>
<td style="text-align: center;">15,446</td>
<td style="text-align: center;">6,122</td>
</tr>
<tr>
<td>Single provider with one child</td>
<td style="text-align: center;">16,233</td>
<td>7,675</td>
<td style="text-align: center;">16,550</td>
<td style="text-align: center;">7,752</td>
<td style="text-align: center;">16,742</td>
<td style="text-align: center;">8,000</td>
<td style="text-align: center;">17,695</td>
<td style="text-align: center;">8,288</td>
</tr>
<tr>
<td>Single provider with two or more children</td>
<td style="text-align: center;">16,617</td>
<td>7,675</td>
<td style="text-align: center;">16,941</td>
<td style="text-align: center;">7,825</td>
<td style="text-align: center;">17,146</td>
<td style="text-align: center;">8,075</td>
<td style="text-align: center;">18,112</td>
<td style="text-align: center;">8,366</td>
</tr>
<tr>
<td>Married/Cohabiting without children</td>
<td style="text-align: center;">11,716</td>
<td>5,6016</td>
<td style="text-align: center;">11,994</td>
<td style="text-align: center;">5,726</td>
<td style="text-align: center;">12,326</td>
<td style="text-align: center;">5,909</td>
<td style="text-align: center;">12,770</td>
<td style="text-align: center;">6,122</td>
</tr>
<tr>
<td>Married/Cohabiting with 1 child</td>
<td style="text-align: center;">15,570</td>
<td>7,675</td>
<td style="text-align: center;">15,874</td>
<td style="text-align: center;">7,752</td>
<td style="text-align: center;">16,382</td>
<td style="text-align: center;">8,000</td>
<td style="text-align: center;">16,972</td>
<td style="text-align: center;">8,288</td>
</tr>
<tr>
<td>Married/Cohabiting with 2 children or more</td>
<td style="text-align: center;">16,617</td>
<td>7,675</td>
<td style="text-align: center;">15,874</td>
<td style="text-align: center;">7,825</td>
<td style="text-align: center;">16,382</td>
<td style="text-align: center;">8,075</td>
<td style="text-align: center;">16,722</td>
<td style="text-align: center;">8,366</td>
</tr>
</tbody>
</table>

Source: [www.bm.dk](http://www.bm.dk) and www.borger.dk

The ceiling only applies to those who have not worked for at least 225
hours of ordinary unsupported work within a time period of 12 months
prior to receiving the benefit. Persons with disabilities living in
specific housing types (e.g. institutional homes) are not affected.
Social assistance recipients are furthermore expected to work for at
least 225 hours a year. If they do not fulfil this requirement, the
ceiling is reduced. It depends on whether the person is single or
married/co-habiting as well as on the number of children, see Table 2.5.

**EUROMOD modelling:**

**1)** The conditions regarding having experienced an exogenous shock
and citizenship are not simulated.

**2)** The income test is performed using the income list il_bsa. Its
components are: Earnings, Old age pensions, Disability Pensions,
Survivor Pensions, Early Retirement Pensions, Private Pensions, and
Unemployment Benefits. Plus, wealth above a certain threshold.

**3)** We assume that all the individuals below age 30 qualify for the
education grant if they have achieved primary education or less. We do
not simulate the activation grant because of a relatively small number
of recipients (around 6,000 people in the whole country).

**4)** We only take social assistance, housing benefit, housing grant
and educational allowance into account for the ceiling as information on
other specific means tested benefits as well as the integration benefit
is not available.

**5)** Information on the hours of ordinary unsupported work previous to
benefit receipt is not available. We assume that everyone with less than
1 working month in the current year is subject to the benefit ceiling.
(1 month refers to 225 divided by 37 weekly working hours divided by 4
weeks per month).

**6)** The reduced ceiling is not taken into account as it only affects
the ceiling after the first year of receiving social assistance benefit.

### Child family grant (Børne- og ungeydelse, *bfachnm_s*)

#### Definitions

The Child family grant is a benefit that is given to families with
child(ren) under 18 years old. The amount depends on the age of the
child (ren) and can be reduced if you exceed a certain income threshold.

#### Eligibility conditions 

The unit of analysis is a family formed by parents and dependent
children (tu_bfa_dk).

The eligibility condition is to have child (ren) aged 0-17 years.

For migrants from outside the EU there has been since 1st of September
2015 been a rule that they should have had lived in Denmark at least two
out of the last 10 years. After 6 months with permanent residence or
work they will have the right to 25 %, after 1 year 50 % and after 1½
year 75 %. This is still the rule for those who have received the
benefit before the 1st of January, 2018. Since then, the rule has been
six out of ten years. With an increase in benefit of 8.3 % for every six
months living in Denmark.

The grant is from 2022 automatically paid and shared with a half to each
parent, unless the child after a divorce is more than 9 days over a
total of 14 days by one of the parents where it then will be paid to
this person.

The amount of the benefit is reduced if the reference income is above a
specific threshold (in 2025 the threshold is 917.000). Up to 2022 the
reference income was at the household level, while from 2022 it is at
the individual level.

#### Income tested

The concept of income used for the test is the one used for the
calculation of the top-income tax (see section 2.5.8). Withdrawal rate
is 2% for parental income above a threshold of 917,000 DKK in 2025. The
income test follows the following rules:

If parents are unmarried, the mother’s income is used. In absence of the
mother, the father’s income is used.

If parents live together, and only one parent has income above the
threshold, then the income of this person is used for the income test
for that persons benefit. Thus, the income of the cohabiting partner is
not taken into account. His or her half of the benefit will not be
reduced.

If parents live together and both have income above the threshold, the
withdrawal rate is applied to the income of each partner which is above
the threshold.

The benefit varies for 0-2 year olds, 3-6 year olds and 7-17 years old
children, see table 2.9. The amount is paid out quarterly, although for
those between 15-17 years it is a monthly payment. In 2023 due to the
inflation an extra amount of 600 D.Kr. is paid out per child. This extra
amount is not subject to reduction even if the income is above the
threshold.

The total amount is split among parents unless the child lives mainly by
one parent.

<span id="_Toc222163723" class="anchor"></span>**Table 2.11** Child
family grant, per child per year, (Danish Kroner).

| Age of the child | 2022   | 2023   | Extra in 2023 | 2024   | 2025   |
|------------------|--------|--------|---------------|--------|--------|
| 0-2 years        | 18,612 | 18,984 | 600           | 20,496 | 21,168 |
| 3-6 years        | 14,724 | 15024  | 600           | 16,224 | 16,764 |
| 7-17 years       | 11,592 | 11,820 | 600           | 12,768 | 13,188 |

Source: [www.skm.dk](http://www.skm.dk),
[www.borger.dk](http://www.borger.dk),

**EUROMOD modelling:** In EUROMOD the benefit is assigned to the child.
We assume that children with migration background have lived at least
two/six out of the last 10 years in Denmark and thus, are eligible to
the full amount of the benefit.

### Ordinary child benefit and supplement (Ordinært børnetilskud and ekstra børnetilskud, *bfach00_s*)

#### Definitions

The unit of analysis is a family formed by parents and own dependent
children (tu_bfa_dk).

#### Eligibility conditions

Lone parent, or both parents are old-age pensioners, or both parents are
disability pensioners.

#### Income test

With an individual income (not household income) above 917,000 in 2025
the benefit (at the individual level) will be reduced with 2 % for the
part of income above the threshold.

<span id="_Toc222163575" class="anchor"></span>**Box 2.** Income
included in the income test:

\+ (Self-)Employment income and non-cash employee income

\+ Unemployment related benefits

\+ Social assistance related benefit

\+ Education related allowances

\+ Pension related benefits

\+ Sickness and disability related benefits

\+ Regular inter-household cash transfer

\+ Positive net capital income

\- Employee/self-employed/supplementary labour market contribution

#### Benefit amount

6,664 DKK per child in ordinary child benefit plus a supplement of 6,792
DKK per benefit unit for lone providers, see table 2.10.

<span id="_Toc222163724" class="anchor"></span>**Table 2.12** Ordinary
child benefit rates, per. year, (DKK)

|      | **Basic (per child)** | **Supplement (per unit)** |
|------|-----------------------|---------------------------|
| 2022 | 6,068                 | 6,184                     |
| 2023 | 6,232                 | 6,352                     |
| 2024 | 6,432                 | 6,556                     |
| 2025 | 6,664                 | 6,792                     |

Source: www.borger.dk

### Child benefit for student parents (Særligt børnetilskud til uddannelsessøgende forældre, *bfached_s*)

#### Definitions

The unit of analysis is a family formed by parent(s) and own dependent
children (tu_bfa_dk).

#### Eligibility conditions

Being in tertiary education and having child(ren) and being

lone parent not receiving education grant (benefit for all children), or

living with partner, but only one receives education grant (benefit for
all children), or

living with partner, and both receive education grant (benefit for
children beyond the first)

#### Income test 

If a single person has an income above 175,200 DKK in 2025 and a couple
above 262,700 DKK in 2025 then 10% of the income above the threshold is
subtracted from the benefit amount.

<span id="_Toc222163576" class="anchor"></span>**Box 3.** Income
included in the income test:

\+ (Self-)Employment income

\+ Disability related benefits

\+ Unemployment related benefits

\+ Net capital income

#### Benefit amount

8756 in 2025, 8452 in 2024, 8,188 DKK in 2023, 7,972 in 2022 per child
per year

### Maternity (Graviditets- og Barselsorlov, bma_s), paternity (Fædreorlov, bpa_s) and Parental leave (Forældreorlov, bma_s and bpa_s)

#### Definitions

This is a benefit for the period of maternity leave, available to
mothers, who have given birth, or the father of a child.

#### Eligibility conditions 

Leave benefits for parents in Denmark depends on whether they are wage
earners, students or self-employed. The difference is mainly related to
the size of the benefit and the way it is calculated.

The core conditions are:

Giving birth or being a father, and a “withmother” for women where there
has been insemination to get a child.

Having job, being working at least 18.5 hours per week in own company,
being in job besides education, being unemployed, including when newly
educated.

Daily physical contact with the child (implying that the child can’t be
in day-care while receiving leave benefits)

Permanent residence in Denmark, although if living in Denmark and
working in another EU-country it is the rule in this country deciding
the right to benefits.

#### Income test

None.

#### Benefit duration

The maternity leave for the mother starts 4 weeks before expected birth
and 14 weeks after birth, of which the first 2 weeks are compulsory. The
paternity leave for the father is 2 weeks within the 14 weeks following
birth.

In addition, mothers and fathers can share a parental leave of up to 32
weeks after the 14th week. This period of 32 weeks can be split up or
postponed, but must be taken before the 9th birthday of the child. It
can furthermore be extended proportionally if the parent returns to
part-time work.

Since the 2nd of August 2022 the rules have been that, besides the four
weeks before the expected time of birth maternity leave, and the two
weeks after birth to both father and mothers, there will in total be 24
weeks for each parent, of which 11 weeks can’t be shared among the
parents. Thus, the two weeks after birth are included in the 24 weeks.

#### Benefit amount

The benefit amount for wage-earners is calculated based on their hourly
wage and the number of hours worked, with a maximum of 4,865 DKK/week,
or 131,49 DKK/hour in 2025. Earnings after deducting the 8% contribution
are considered.

For the self-employed the yearly income should have been at least
252,980 DKK in 2025. The same maximum benefit levels apply as for wage
earners.

<span id="_Toc222163725" class="anchor"></span>**Table 2.13** Parental
leave rates, (Danish Kroner)

|                       |         |         |         |         |
|-----------------------|---------|---------|---------|---------|
|                       | 2022    | 2023    | 2024    | 2025    |
| Maximum/week          | 4,465   | 4,550   | 4,695   | 4,865   |
| Maximum/hour          | 120.68  | 122.97  | 126.29  | 131,49  |
| Self-employed income  | 232,212 | 236,736 | 244,140 | 252,980 |
| Students before birth | 3,195   | 3,255   | 3,360   | 3,480   |
| Students after birth  | 3,665   | 3,735   | 3,855   | 3,990   |

Note: In most collective agreements there is normal wage paid out for up
to 26 weeks of parental leave. Subject to taxes/SIC

Source: [www.borger.dk](http://www.borger.dk)

The benefit is subject to income tax.

#### Take up

**EUROMOD modelling:** We assume that duration of the maternity leave
depends on the month of birth of a child. The month of birth is assumed
to be equal to the middle month of the quarter of birth reported in
SILC. If child’s month of birth is unavailable, the assumption is that
the child is born on June 30 (6th month of the year). Where mothers are
absent, fathers are assumed to receive the allowance for the same number
of weeks as mothers, hence in those families we might be overestimating
the total amount of allowance.

Up to 2022, we assumed that all women with children aged less than 1
year have taken 4 weeks of maternity leave before childbirth and 18
weeks of maternity leave after childbirth; while all fathers with
children aged less than 1 year have taken 2 weeks of paternity leave.
The duration of shared parental leave (32 weeks) is split between the
mother and the father in proportion to their average shares for all
couples in the table above (90.5% for women and 9.5% for men). This adds
up to the maximum of 47 weeks of total paid leave for coupled women (or
50 weeks of paid leave for single parents) and 5 weeks of total paid
leave for coupled men that can be taken in a given year. We assume that
all the leave is spent in the first year after the childbirth.

The rules changed the 2nd August 2022 see description on the previous
page: we assume that fathers’ paternity leave is 13 weeks (bpa_s) while
mothers’ leave is 24+11 weeks post childbirth and 4 weeks before
childbirth.The total duration of leave pertaining to a mother is 39
weeks (bma_s). For a single mother (with full custody) the total
duration of leave is 41 weeks.

### *Green check (Grøn check, bhtuc_s)*

#### Definitions

The unit of analysis is the adult individual, but the number of
dependent children is relevant for the simulation (tu_bhtuc_dk). A child
is considered as dependant if younger than 18 years.

#### Eligibility conditions

All persons liable to pay taxes aged 18 or older, albeit from 2023 the
green check is only for pensioners

#### Income and wealth test

The green check is phased out with 7.5 percent against income above a
threshold of 475.300 DKK in 2025, where the relevant income is the tax
base for the top bracket tax (without taking into account the deduction
of contributions to capital pension schemes).

<span id="_Toc222163577" class="anchor"></span>**Box 4**. Income
included in the income test:

\+ (Self-)Employment income and non-cash employee income

\+ Unemployment related benefits

\+ Social assistance related benefit

\+ Education related allowances

\+ Pension related benefits

\+ Sickness and disability related benefits

\+ Regular inter-household cash transfer

\+ Positive net capital income

\- Employee/self-employed/supplementary labour market contribution

#### Benefit amount

The annual benefit amounts to 875 DKK for adults (only pensioners) in
2025 reduced by 7.5 % if income after labour market contribution exceeds
475.300 in 2025. Benefits for children are given to the mother, however
from 2022 will be split between the parents. There is an extra amount of
120 DKK per person for pensioners with children. Additionally there is
an extra amount of 280 DKK per person for low income earners that is
reduced by 7.5 % if the income exceeds 277,800 DKK in 2025.

<span id="_Toc222163726" class="anchor"></span>**Table 2.14** Green
check compensations scheme per year

|  | **2022** | **2023** | **2024** | **2025** |
|----|---:|---:|---:|---:|
| Per person | 263 | 0 | 0 | 0 |
| In case of pensioners | 875 | 875 | 1000 | 875 |
| Per child non-pensioners (max two) | 120 | 0 | 0 | 0 |
| Per child of pensioners | 200 | 120 | 120 | 0 |
| Extra amount (low-income earners) pensioner | 280 | 280 | 280 | 280 |
| Non-pensioners | 140 | 0 | 0 | 0 |

Source: [www.skm.dk](http://www.skm.dk)

### Housing Allowance

Housing allowance is the comprehensive term for the housing benefit for
tenants and the housing grant for pensioners. Both forms of housing
allowances are tax-free. The following only deals with the most
important rules, as the housing allowance even according to official
documentation is very complex.

A common term for the housing allowance is the housing cost, which is
defined as the pure rent for the tenancy, excluding costs for heating,
electricity etc. However, under some circumstances related both to
characteristics of the dwelling and of the tenancy, the housing cost is
augmented. The impossibility to fully simulate these circumstances
obliged us to derive the housing cost reversing the rule for the
calculation of the housing allowance. Then a regression analysis has
been performed at the household level to impute a value of housing cost
of households not receiving housing allowances. The derived variable is
called xivhc.

### Housing Benefit (Boligsikring, *bho01_s*)

#### Definitions

The unit of analysis is the household (tu_bho_dk).

#### Eligibility conditions

Tenants who are not pensioners (poa00=0 at the household level).

#### Income and wealth test

The benefit is phased-out against the total incomes of all household
members, and wealth, except income from children. Personal income base
(il_PersIncome) is taken into account.

<span id="_Toc222163578" class="anchor"></span>**Box 5.** Income of all
household members (except income from children (since 2019)) included in
the income test:

\+ (Self-)Employment income and non-cash employee income

\+ Unemployment related benefits

\+ Social assistance related benefit

\+ Education related allowances

\+ Pension related benefits

\+ Sickness und disability benefits

\- Contributions to private pension plans that can be deducted from
personal income

\- Employee/self-employed labour market contribution

\+ Wealth

The household income is augmented to take account of financial wealth
(see table below).

<span id="_Toc222163727" class="anchor"></span>**Table 2.15** Income
augmentation with wealth for calculation of housing benefit, (DKK).

| %   | 2022              | 2023              | 2024              | 2025              |
|-----|-------------------|-------------------|-------------------|-------------------|
| 0   | \< 779,800        | \< 793,100        | \< 855,800        | \<884,100         |
| 10  | 779,800-1,559,700 | 793,100-1,586,200 | 855,800-1,711,800 | 884,100-1,768,300 |
| 20  | \> 1,559,700      | \> 1,586,200      | \> 1,711,800      | 1,768,300         |

Source: www.borger.dk

The benefit amounts to ***60 per cent*** of the housing costs, which
maximum can be ***94,200 in*** 2025. From this, ***18 per cent*** of the
income that exceeds ***167,900*** DKK is subtracted. This income
threshold is augmented by ***44,200*** DKK for each child beyond the
first in the household, to a maximum of 4 children, see table 2.15
below. For households without children the housing benefit can at most
constitute ***15 per cent*** of the housing cost. Regardless of the
income correction etc. the recipient of the housing benefit always has
to pay a minimum of ***28,300 DKK*** in rents him/herself. Households
with children can at most receive a housing grant of ***49,716*** DKK
per year.

<span id="_Toc222163728" class="anchor"></span>**Table 2.16** Various
limits etc. for housing benefit, per year. DKK

|  | **2022** | **2023** | **2024** | **2025** |
|----|----|----|----|----|
| Lower income deduction | 148,100 | 150,600 | 162,600 | 167,900 |
| Deduction increase per child (2<sup>nd</sup>-4<sup>th</sup>) | 39,000 | 39,700 | 42,800 | 44,200 |
| Own minimum payment | 25,000 | 25,400 | 27,400 | 28,300 |
| Maximum benefit, households | 43,848 | 44,592 | 48,120 | 49,716 |
|  |  |  |  |  |
| Maximum yearly rent | 83,100 | 84,500 | 91,200 | 94,200 |

Source: [www.bm.dk](http://www.bm.dk)

###  Housing grant (Boligstøtte, *bho02_s*)

#### Definitions

The unit of analysis is the household (tu_bho_dk).

#### Eligibility conditions

Tenants who are pensioners (poa00\>0 at the household level).

#### Income and wealth test

The benefit is phased-out against total household income and wealth. The
relevant incomes are the same as the one defined in the housing benefit
section.

The household income for the calculation of the housing grant is
augmented to take account of financial wealth (see table below).

<span id="_Toc222163729" class="anchor"></span>**Table 2.17** Income
augmentation with wealth for calculation of housing grant,

| % | 2022 | 2023 | 2024 | 2025 |
|----|----|----|----|----|
| 0 | \< 913,400 | \< 940,800 | \< 973800 | \< 1,011,700 |
| 10 | 913,400 – 1,805,400 | 940,800 – 1,881,800 | 973,800 – 1,947,700 | 1,011,700 – 2,023,700 |
| 20 | \> 1,827,000 | \> 1,881,800 | \> 1,947,700 | \> 2,023,700 |

Source: [www.bm.dk](http://www.bm.dk)

The housing grant corresponds as a rule to 75 per cent of the housing
cost with a supplement of 8,100 DKK (in 2025). 22.5 per cent of the
income exceeding 192,200 DKK is subtracted from this. This income
threshold is augmented with 50,600 DKK from 2nd-4th child. The recipient
of the housing benefit has to pay a minimum 11 per cent of the income or
at least 20,300 DKK. Households can at most receive a housing grant of
56,892 DKK per year. The maximum benefit is defined independent from the
number of children in the household.

<span id="_Toc222163730" class="anchor"></span>**Table 2.18** Various
limits etc. for housing grant, per year, (DKK).

|  | **2022** | **2023** | **2024** | **2025** |
|----|----|----|----|----|
| Supplement | 7,300 | 7,500 | 7,800 | 8,100 |
| Lower income deduction | 173,500 | 178,700 | 185,000 | 192,200 |
| Deduction increase per 2<sup>nd</sup>-4<sup>th</sup> childchild | 45,700 | 47,100 | 48,700 | 50,600 |
| Own minimum payment | 18,300 | 18,900 | 19,600 | 20,300 |
| Maximum benefit | 51,360 | 52,908 | 54,756 | 56,892 |

Source: https://www.bm.dk/ydelser-satser, different years

### Basic old age pension (Folkepension, poa00_s)

#### Definitions

The unit of analysis is the individual (tu_individual_dk).

#### Eligibility conditions 

All persons from the age of 67 from 1st of July 2022 conditional on
citizenship and time of residence in Denmark or legal residence as
EU-citizens.

#### Income test

There is from 1st of January 2023 no longer income test for the basic
old age pension. Rules were decided in the autumn of 2023, implying that
those who have got their basic pension reduced due to the income test
will get this amount for 2023 paid out in May 2024.

Before 2023 the rule thus was that above a threshold in her/his own wage
earnings income, the benefit was withdrawn with 30 per cent, see table
below.

From 2023 there is no reduction in the basic old age pension. It is
still possible to wait to receive old-age pension and then get a higher
level or a lump sum later.

#### Benefit amount

86.376 DKK per year in 2025, see also table below.

<span id="_Toc222163731" class="anchor"></span>**Table 2.19** Income
threshold and benefit amount for basic old-age pension, per year (DKK)

|                  | **2022** | **2023** | **2024** | **2025** |
|------------------|----------|----------|----------|----------|
| Benefit amount   | 78,564   | 80,328   | 83,136   | 86,376   |
| Income threshold | 348,700  |          |          |          |

Source: [www.borger.dk](http://www.borger.dk): Folkepension,
[www.bm.dk](http://www.bm.dk)

**EUROMOD modelling:** The citizenship and length of residence rules are
not implemented in EUROMOD.

### Old-age pension supplement (Pensionstillæg, *poa01_s*)

#### Definitions

The unit of analysis is the individual (tu_individual_dk).

#### Eligibility conditions 

All persons from the age of 67 from 1st of July 2022 conditional on
citizenship and time of residence in Denmark or legal residence as
EU-citizen.

#### Income test

The rules for the income test have been changed from 1st of January
2023, and amended for 2025. Since first of January 2023 the income test
includes just positive capital income including income from shares
except the first 5000 and labour market pensions while the relevant
income until 1st of January 2023 used for the test includes also the
spouse’s earnings minus the labour market contribution in case the
recipient has a partner that is not a pensioner. The income from
self-employment do not influence under the condition that the person is
actively working in the company. From 2025 the relevant income for the
income test for a partner that is not a pensioner includes just income
from social assistance, early retirement benefits or sickness benefits

<span id="_Toc222163579" class="anchor"></span>**Box 6.** Income
included in the income test until 1<sup>st</sup> of January 2023:

\+ (Self-)Employment income of partner

- Employee/self-employed labour market contribution of partner

\+ Capital Income

From 1<sup>st</sup> of January 2023

\+ Capital Income

\+ Income from Shares except the first 5000

\+ Labour Market Pensions

\+ Married or cohabitants income from social assistance, early
retirement benefit or sickness benefit (from 2025)

The rules differentiate between singles and couples and for the latter
whether one or both partners are old-age pensioners. The rules do not
distinguish between married and cohabitating couples.

For a single pensioner since 2023 the pension supplement is phased out
against own income (capital income, income from shares and labour market
pensions) with 30.9 per cent, once the income surpasses a basic
deduction of 85,300 DKK in 2025. See also table below.

For couples, income above a combined basic deduction of 170,900 DKK
(2025) is set off against the pension supplement with 16 per cent for
two pensioner-couples and with 32 percent for one-pensioner couples.

<span id="_Toc222163732" class="anchor"></span>**Table 2.20** Income
dependence parameters for old-age pension supplement, per year.

|  | **2022** | **2023** | **2024** | **2025** |
|----|----|----|----|----|
| **Singles** |  |  |  |  |
| Deduction, own income (DKK) | 122,004 | 122,004 | 93,400 | 85,300 |
| Phase-out rate (%) | 30.9 | 30.9 | 30.9 | 30,9 |
| **Couples** |  |  |  |  |
| Limit for calc. of spouse-income (DKK) | 318,700 | \- | \- |  |
| Deduction, income (DKK) except partners wages income | 179,700 | 182,900 | 187,100 | 170,900 |
| Phase-out rate (%) |  |  |  |  |
| *Couples, 1 old-age pensioner* | 32 | 32 | 32 | 32 |
| *Couples, 2 old-age pensioners* | 16 | 16 | 16 | 16 |

Source: [www.bm.dk](http://www.bm.dk) and www.borger.dk

The amounts are shown in Table 2.19

<span id="_Toc222163733" class="anchor"></span>**Table 2.21** Benefits
for old-age pension supplement, per year (DKK).

|                     | **2022** | **2023** | **2024** | **2025** |
|---------------------|----------|----------|----------|----------|
| Married/cohabitants | 45,600   | 47,556   | 49,224   | 51,144   |
| Singles             | 89,664   | 92,940   | 96,192   | 99,948   |

Source: [www.borger.dk](http://www.borger.dk).

### Supplementary pension (ældrecheck/supplerende pensionsydelse, *poa02_s*)

#### Definitions

The unit of analysis is the individual (tu_individual_dk).

#### Eligibility conditions 

All reached the age limit for receiving old-age pensions.

#### Income and wealth test

The benefit is reserved for pensioners with liquid financial assets of
less than 103,100 DKK (see table below) and is phased-out against labour
income above a basic deduction based upon the calculated personal
supplement rate, see section 2.5.15. In 2022 and 2023 an extra amount of
5000 D. Kr. has been paid out. So, the first issue to look into is the
wealth, and if this is below the level then calculate the level of the
benefit based upon the personal supplement rate.

<span id="_Toc222163580" class="anchor"></span>**Box 7.** Income
included in the wealth test:

\+ Wealth

#### Benefit amount

25,700 DKK per year (see table below).

<span id="_Toc222163734" class="anchor"></span>**Table 2.22** Benefit
and asset test for supplementary pension, per year, (DKK).

|                 | **2022** | **2023** | **2024** | **2025** |
|-----------------|----------|----------|----------|----------|
| Benefit         | 18,600   | 19,200   | 19,900   | 25,700   |
| Asset threshold | 93,000   | 95,500   | 99,200   | 103,100  |
| Extra           | 5,000    | 5,000    |          |          |

Source: [www.borger.dk](http://www.borger.dk)

### Personal Supplement rate (Tillægsprocent, *poa02_s*)

The supplementary pension is also phased-out against incomes other than
old-age incomes, such as labour income, using the personal supplement
rate, which is calculated for all old-age pensioners based on their own
and a possible spouse’s income beyond the old-age pension.

<span id="_Toc222163581" class="anchor"></span>**Box 8.** Income
included in the income test:

\+ Employment income, as well as self-employment above the threshold and
non-cash employee income

\+ Pension from the labour market contribution scheme

\+ Early retirement, private, sickness and disability pension

\+ Net capital income

As a default the supplement rate is 100 per cent (e.g., 100% of the
benefit is paid), which is reduced for incomes above 35,200 DKK (in
2025) for singles and above 69,700 DKK for married cohabitant couples by
1 percentage point for every 606 DKK (1223 DKK for couples) of income
above the threshold. See also table below.

<span id="_Toc222163735" class="anchor"></span>**Table 2.23** Benefit
test for personal supplement rate, per year (DKK).

|                           | **2022** | **2023** | **2024** | **2025** |
|---------------------------|----------|----------|----------|----------|
| Basic deduction threshold |          |          |          |          |
| Singles                   | 35,000   | 35,000   | 35,100   | 35,200   |
| Couples                   | 69,300   | 69,200   | 69,400   | 69,700   |
| Phase-out                 |          |          |          |          |
| Singles                   | 547      | 563      | 583      | 606      |
| Couples                   | 1,091    | 1,137    | 1,177    | 1223     |

Source: [www.bm.dk](http://www.bm.dk),
[www.borger.dk](http://www.borger.dk)

## Social insurance contributions

Most Danish transfers are financed through either the tax system, or
through fully privately organized schemes. Below the three partly public
social security schemes are described.

### Supplementary labour market pension (ATP-bidrag, *tscpier_s*, *tscpiee_s*)

All employees and employers pay contributions to a supplementary labour
market pension scheme (ATP), with fixed contributions that vary by type
of employment contract – monthly, fortnightly, weekly or hourly – and
number of hours worked – full-time, part-time or less, see table below.
The income level is not taken into account. Employers pay two-thirds of
the contribution (tscpier_s), while employees pay one-third (tscpiee_s).
Self-employed can opt to pay the supplementary labour market pension as
well. There are also contributions with a monthly payment of 297 DKK for
self-employed.

<span id="_Toc222163736" class="anchor"></span>**Table 2.24**
Supplementary labour market pension contributions,

|                          | **2022 -2023** | **2024-2025** |
|--------------------------|----------------|---------------|
| **Monthly contract**     |                |               |
| Full time (117h-)        | 284            | 297           |
| Part time (78-116h)      | 189.35         | 198           |
| Part time (39-77h)       | 94.65          | 99.0          |
| \< 39 hours              | 0              |               |
| **Fortnightly contract** |                |               |
| Full time (54h-)         | 149.40         | 156.60        |
| Part time (36-53h)       | 99.60          | 104.40        |
| Part time (18-36h)       | 49.80          | 52.20         |
| \< 18hours               | 0              | 0             |
| **Weekly contract**      |                |               |
| Full time (27h-)         | 74.4           | 78.30         |
| Part time (18-26h)       | 49.8           | 52.20         |
| Part time (9-17h)        | 24.90          | 26.10         |
| \< 9 hours               | 0              | 0             |
| **Hourly paid**          |                |               |
| Per hour                 | 2.01           | 2.13          |

Source:
https://www.borger.dk/pension-og-efterloen/atp-livslang-pension-oversigt/historiske%20atp%20satser

**EUROMOD modelling:** Only monthly contracts are simulated in Euromod,
as the majority of contracts in Denmark are monthly. We only simulate
contribution for employed because information on voluntary contribution
of self-employed is not available.

### Contribution to unemployment insurance scheme and early retirement scheme (A-kasse-bidrag and Efterlønsbidrag, *tyrui_s*)

Unemployment insurance is voluntary and organised through typically
trade-specific insurance schemes with monthly contributions, see table
below. Early retirement is conditional upon long-term membership of an
unemployment insurance scheme, and contribution to early retirement is
therefore modelled alongside contributions to unemployment insurance
schemes with a total contribution (tyrui_s). It is possible only to be
member of unemployment insurance and thus not an early retirement
benefit scheme. This is increasingly the case.

<span id="_Toc222163737" class="anchor"></span>**Table 2.25** Voluntary
monthly contribution to unemployment insurance and early retirement
scheme, for full time insured. (DKK)

|                                         | **2022** | **2023** | **2024** | **2025** |
|-----------------------------------------|----------|----------|----------|----------|
| Contribution to unemployment insurance  | 357      | 364      | 376      | 389      |
| Contribution to early retirement scheme | 521      | 531      | 548      | 568      |
| Sum                                     | 878      | 895      | 924      | 957      |

Source: www.bm.dk

#### Random assignment

Participation in unemployment insurance scheme is imputed in the input
dataset using national register data.

**EUROMOD modelling:** The wage compensation for self-employed is not
taken into account when calculating the contribution to the unemployment
insurance scheme. If wage compensation policies are switched on, a
reduction of income (also in case this was replaced by a wage
compensation) can lead to a lower number of people paying this
contribution.

## Direct Taxes 

The Danish tax system contains a gross flat tax levied on all labour
income, municipal and county taxes levied on the taxable income base and
a progressive tax rate at the national level levied on the personal
income base. The tax system is mainly based on individual personal
taxation, although there are a few possibilities for married couples to
transfer redundant deductions in the different tax bases.

Two main income concepts used in this context are the Personal Income
and Taxable Income, which are calculated as shown in the table below.

<span id="_Toc222163582" class="anchor"></span>**Box 9.** Calculation of
the Personal Income and Taxable Income tax bases

<table style="width:70%;">
<colgroup>
<col style="width: 3%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 2%" />
<col style="width: 0%" />
<col style="width: 60%" />
<col style="width: 1%" />
</colgroup>
<thead>
<tr>
<th rowspan="2"><strong>(1)</strong></th>
<th colspan="5" rowspan="2"><strong>Gross labour income</strong></th>
<th></th>
</tr>
<tr>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong> </strong></td>
<td></td>
<td>-</td>
<td colspan="3">Contributions to occupational based agreed obligatory
supplementary pension scheme (<em>Arbejdsmarkedspension</em>)</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td>+</td>
<td colspan="3">All Transfers</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td></td>
<td></td>
<td colspan="2">Education grant (<em>Statens
Uddannelsesstøtte</em>)</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td></td>
<td></td>
<td colspan="2">Unemployment benefits (<em>A-Dagpenge</em>), Early
retirement pensions (<em>Efterløn</em> og <em>Engangsydelse</em>),
Social assistance (<em>Kontanthjælp</em> og
<em>integrationsydelse</em>), Severance pay
(<em>Fratrædelsesgodtgørelse</em>)</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td></td>
<td></td>
<td colspan="2">Sickness benefits (<em>Sygedagpenge mv.</em>)</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td></td>
<td></td>
<td colspan="2">Benefits to pensioners, including old-age pension
(<em>Folkepension</em>); pensions from the labour market contribution
scheme (<em>ATP-pensioner</em>); civil servant pensions, incl. pensions
to wife and children (<em>Tjenestemandspension</em>); pension payments
from privately held pension plans in pension funds, banks or insurance
companies with regular payments; capital pensions; pension payments from
previous employers; foreign pensions</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td></td>
<td></td>
<td colspan="2">Survivors benefits (<em>Efterladtepension</em>)</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td></td>
<td></td>
<td colspan="2">Disability pension (<em>Førtidspensione mv.</em>)</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td>+</td>
<td colspan="3">Other incomes</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td>+</td>
<td colspan="3">Gifts</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td>+</td>
<td colspan="3">Alimony received</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td>+</td>
<td colspan="3">Life insurance premiums, fringe benefits</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td>­-</td>
<td colspan="3">Labour market contribution (txc_s)</td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td>-</td>
<td colspan="3">Supplementary labour market contribution
(tscpiee_s)</td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td>-</td>
<td colspan="3">Contributions to private pension plans with a ceiling of
65.500, DKK in 2025 (xpp00_s)</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td>­-</td>
<td colspan="3">Additional deduction of 12% (if more than 15 years to
retirement) or 32% (if less than 15 years to retirement) of pension
contributions (public and private) of an amount up to 83,800 DKK in 2025
(tintaox_s)</td>
<td></td>
</tr>
<tr>
<td><strong>(2)</strong></td>
<td colspan="5"><strong>Personal income (il_PersIncome)</strong></td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td>+</td>
<td colspan="3">Net capital income</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td>­-</td>
<td colspan="3">Work-related deductions</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td></td>
<td colspan="2"></td>
<td>Earned income tax credit</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td></td>
<td colspan="2"></td>
<td>Transport allowance</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td></td>
<td colspan="2"></td>
<td>Payments to unemployment funds, unions &amp; early retirement
scheme</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td></td>
<td colspan="2"></td>
<td>Alimony/payments to divorcee’s children and ex-partner</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td></td>
<td colspan="2"></td>
<td>Special occupational deductions (fishermen, etc.)</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td></td>
<td colspan="2"></td>
<td>Deposit on (company) start-up account</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td></td>
<td></td>
<td colspan="2"></td>
<td>Gift deductions</td>
<td></td>
</tr>
<tr>
<td><strong> </strong></td>
<td style="text-align: right;"></td>
<td></td>
<td colspan="2"> </td>
<td>Other employee expenses (over 7300 DKK in 2025)</td>
<td></td>
</tr>
<tr>
<td><strong>(3)</strong></td>
<td colspan="5"><strong>Taxable income (il_tin)</strong></td>
<td></td>
</tr>
</tbody>
</table>

Another important feature of the tax system is the General Personal
Allowance (GenPersAllowance), used for the simulation of several of the
instruments described below. From 2023 the general personal allowance is
the same for all persons (decided in November 2023, but with impact for
the whole 2023).

<span id="_Toc222163738" class="anchor"></span>**Table 2.26** General
Personal Allowance, (DKK).

|                            | 2022   | 2023   | 2024   | 2025   |
|----------------------------|--------|--------|--------|--------|
| For persons below 18 years | 37,300 | 48,000 | 49,700 | 51,600 |
| For all other tax payers   | 46,600 | 48,000 | 49,700 | 51,600 |

Source: [www.skm.dk](http://www.skm.dk)

**EUROMOD modelling:**

**1)** It has not been possible to identify some of the components of
these income concepts. Please have a look at the component of the income
lists for more information.

**2)** The Danish tax system uses a concept of capital income, which
incorporates interest payments on loans, mortgages etc. No fully
comparable variable is found in the SILC-data, where the closest
variable – investment income *yiy* – also includes a long range of
positive incomes.

**3)** For commuting distances (forth and back) above 24 km, tax payers
can deduct standardized expenses (per km and work day). This is not
implemented.

### Earned Income Tax Credit (Beskæftigelsesfradrag, tintc_dk):

#### Tax unit 

Tax unit is the individual.

#### Tax Allowances

Contribution to private pension schemes and contribution to
supplementary labour market pension schemes needs to be deducted from
the tax base.

#### Tax Base

The tax base is the gross labour income after the deduction of the tax
allowances, albeit from 2018 changed so that it is gross-labour income.

#### Tax Schedule

In 2025 the earned income tax credit rate is 12.3 %. The maximum value
of tax credit is 55,600 DKK per year. There is an extra earned income
tax-credit for single providers with a percentage of 11,5 and a maximum
value of 48,300 DKK. The definition of single provider is the same as
the one used for the simulation of the child benefit supplement. Rate
and maximum amount for supplementary earned income tax credit is
reported in the table below. Finally, there is an additional credit for
incomes above 224,500 DKK with a maximum credit of 2,900 DKK.

<span id="_Toc222163739" class="anchor"></span>**Table 2.27** Earned
income tax-credit, per year, (*Beskæftigelsesfradrag*)

|                 |                     | **2022** | **2023** | **2024** | **2025** |
|-----------------|---------------------|----------|----------|----------|----------|
| General credit  | Rate (%)            | 10.65    | 10.65    | 10.65    | 12.3     |
|                 | Maximum value (DKK) | 43,500   | 45,600   | 45,100   | 55,600   |
| Single provider | Sup. Rate (%)       | 6.25     | 6.25     | 6.25     | 11,5     |
|                 | Sup. Max (%)        | 23,700   | 24,400   | 25,300   | 48,300   |
| Additional rate | Income above (DKK)  | 202,700  | 208,700  | 216,100  | 224,500  |
|                 | Rate (%)            | 4.5      | 4.5      | 4.5      | 4,5      |
|                 | Maximum value (DKK) | 2,700    | 2,700    | 2,800    | 2,900    |

Source: [www.borger.dk](http://www.borger.dk) and [Beskæftigelses- og
jobfradrag - Skat.dk](https://skat.dk/data.aspx?oid=2234762)

### Labour Market Contributions (Arbejdsmarkedsbidrag, txc_dk)

#### Tax unit 

The tax unit is the individual.

#### Tax Base

The tax base is the gross labour market income from employment and
self-employment.

#### Tax Schedule

The labour market contribution (LMC) is a gross tax of 8 per cent levied
upon gross labour income.

### Municipality Tax (Kommuneskat, tmu_dk):

#### Tax unit 

The tax unit is the individual.

#### Tax Base

The tax base is the taxable income base after the deduction of the
general personal allowance. Unused allowance can be transferred between
spouses.

#### Tax Schedule

Tax rates vary across municipalities, see table below.

<span id="_Toc222163740" class="anchor"></span>**Table 2.28**
Distribution of municipality tax rates (%), (kommuneskat)

|         | **2022** | **2023** | **2024** | **2025** |
|:-------:|:--------:|:--------:|:--------:|:--------:|
| Average |   25.0   |   25.0   |   25.1   |   25,1   |

Source: http://www.skm.dk

**EUROMOD modelling:** Since it is not possible to distinguish among
municipalities in the EU-SILC, the average tax rate is applied.

### Church Tax (Kirkeskat, tcr_dk):

#### Tax unit 

The tax unit is the individual.

#### Tax Base

The tax base is the taxable income base after the deduction of the
general personal allowance. Unused allowance can be transferred between
spouses.

#### Tax Schedule

Tax rates vary across municipalities, see table below.

<span id="_Toc222163741" class="anchor"></span>**Table 2.29** Municipal
average church tax rates, (%)

|              | **2022** | **2023** | **2024** | **2025** |
|--------------|----------|----------|----------|----------|
| Average rate | 0.87     | 0.87     | 0.87     | 0.87     |

Source: www.statistikbanken.dk/PSKAT

**EUROMOD modelling:** The church tax is a voluntary contribution. In
EUROMOD entitlement is randomly assigned to 75% of the population. Since
it is not possible to distinguish among municipalities in the EU-SILC,
the average tax rate is applied.

### Bottom Bracket Income Tax (Bundskat, tinbt_dk): 

#### Tax unit 

The tax unit is the individual.

#### Tax Base

The tax base is the personal income base and net capital income, with
the general personal allowance subtracted. Spouses can transfer negative
net capital income and any unused personal allowance between them for
the calculation of the bottom bracket tax.

#### Tax Schedule

The tax rate is 12.01 per cent in 2025.

<span id="_Toc222163742" class="anchor"></span>**Table 2.30** Bottom
bracket tax rates (%), (bundskat).

|                         | **2022** | **2023** | **2024** | **2025** |
|-------------------------|:--------:|:--------:|:--------:|:--------:|
| Bottom bracket tax rate |  12.09   |  12.06   |  12.06   |  12,01   |

Source: Danish Ministry of Taxation

### Top Bracket Tax (Topskat, tinto_dk):

#### Tax unit 

The tax unit is the individual.

#### Tax Base

The top-bracket tax is the highest-level of the progressive state taxes
and is levied upon the sum of the personal income tax base, positive net
capital income and contribution to capital pension schemes, with the
top-bracket tax allowance subtracted.

The positive net capital income for spouses for the calculation of the
top-bracket tax is computed jointly and taxed for the spouse with the
highest basis of calculation, i.e. the spouse with the highest sum of
the personal income base and the contributions to private capital
pensions.

<span id="_Toc222163583" class="anchor"></span>**Box 10.** Income
included in the income test:

\+ (Self-)Employment income and non-cash employee income

\+ Unemployment related benefits

\+ Social assistance related benefit

\+ Education related allowances

\+ Pension related benefits

\+ Sickness and disability related benefits

\+ Regular inter-household cash transfer

\+ Contributions to private pension plans

\+ Positive net capital income

\- Employee/self-employed/supplementary labour market contribution

There is a basic yearly allowance of 52,400 in 2025 for the inclusion of
positive net capital income in the tax base for the top-bracket tax. The
allowance can be transferred between spouses. This means that for two
spouses only positive capital incomes above 104,800 DKK (in 2025) are
taxed with the top-bracket tax rate.

#### Tax Schedule

<span id="_Toc222163743" class="anchor"></span>**Table 2.31** Top
bracket tax rates and allowances,

|  | **2022** | **2023** | **2024** | **2025** |
|----|:--:|:--:|:--:|:--:|
| Top bracket tax rate (%) | 15.0 | 15.0 | 15.0 | 15.0 |
| Top bracket tax allowance (DKK) | 552,500 | 568,900 | 588,900 | 611,800 |
| Allowance in positive net capital income (DKK)(((DKK(DKK) (DKK | 47,400 | 48,800 | 50,500 | 52,400 |

Source: Danish Ministry of Taxation (www.skm.dk). Allowance in positive
net income is for unmarried individuals (double for married couple).

The sum of municipal, health, bottom and top tax cannot exceed 52.01 %
tax ceiling in 2025 If the tax ceiling is reached, the top bracket
income tax is reduced accordingly.

<span id="_Toc222163744" class="anchor"></span>**Table 2.32** Tax
ceiling,

|             | **2022** | **2023** | **2024** | **2025** |
|-------------|----------|----------|----------|----------|
| Tax ceiling | 52.06    | 52.07    | 52.07    | 52.01    |

Source: www.skm.dk

### Property tax (tpr_s)

#### Tax unit 

The tax unit is the household.

#### Tax Base

The tax base is the property value.

#### Tax Schedule

From 2024 new values has been given to all property after a new IT
system has been used. The rules have further been changed. The tax rate
in 2025 is 0.51% on property value up to 9,2 million where it will be
1.4 % of the amount above 9.2. The estimated value of the property has
been reduced by 20 % as a safety measure. At the same time it is so that
in 2024 the tax will not be increased due to a so called tax-rebate.
From 2025 the property tax will change with changes in property value.

The description below is until and including 2023.

The tax rate is 0,92% on property value of up to 3,040,000 DKK and a tax
rate of 3 percent above that threshold. The threshold has been frozen
nominally since 2002. Pensioners can have the payment reduced with 0.37
% of the property value with a maximum of 6.000 D.Kr. This is reduced
with 5 % for single person with an income above 217.700 in 2023(206.200
in 2022) and for a couple 327.200 in 2023 (317.800 in 2022)

**EUROMOD modelling:** In order to simulate this instrument, the tax
rule has been reversed and the property value derived. This has then
been used in the simulation.

## Extraordinary measures

### Extra temporary child benefit (midlertidig børnefamilieydelse, *bfachxp_s*) 

From 2020-2022 there is an extra child benefit for those who receive
reduced benefits due to the ceiling of total benefits, such as housing
benefit. In 2023 the last payment was done in the month of February.

#### Definitions

The unit of analysis is a family formed by parent and own dependent
children (tu_bfa_dk).

#### Eligibility conditions

Receiving reduced benefits due to the ceiling on total benefits (see
table 2.8).

#### Benefit amount

The benefit is 616 DKK in 2023 per month for those single providers on
educational support or social assistance, 718 DKK in 2023 for single
providers with self- and home travel benefits, and 564 DKK in 2023 for a
parent who is married or co-habiting. There will be one supplementary
benefit of 666 DKK in 2023 independent on the number of children. In
total it cannot exceed the amount the benefit due to the ceiling has
been reduced with.

<span id="_Toc222163745" class="anchor"></span>**Table 2.33** Extra
temporary child benefit, (Danish Kroner)

|  | **2021** | **2022** | **2023 (only for two months)** |
|----|:--:|:--:|:--:|
| Single providers on educational support or social assistance | 615 | 616 | 616 |
| Single providers with self- and home travel benefits | 717 | 718 | 718 |
| Parent who is married or co-habiting | 563 | 564 | 564 |
| Supplementary benefit | 665 | 666 | 666 |

Source: www.borger.dk

**EUROMOD modelling:** The benefit for single providers with self and
home travel benefits is not simulated due to lack of information.
Abolished in February 2023.

### Wage Compensation Schemes (yemcomp_dk, ysecomp_dk)

In 2020 a number of schemes was introduced in order to compensate the
loss of income due to the period of the lock-down in Denmark. They were
for a limited time extended in 2021 and early 2022 until the 15th
February 2022. In line with traditions on the Danish labour market,
there was a tri-partite agreement. Thus for 2023 no longer relevant.

#### Eligibility conditions 

The agreement applies to employees of all private companies who are
affected exceptionally hard financially by COVID-19 and therefore have
to notify redundancies for at least 30 per cent of or for more than 50
employees. For self-employed and free-lance workers there has also been
decided a government compensation strategy.

#### Benefit amount

The company receives a state salary compensation of 75 per cent of the
salaries of the employees concerned, but with a maximum of DKK 23,000
per employee per month if they do not implement layoffs. For hourly wage
earners, state wage compensation amounts to 90 per cent, but with a
maximum of DKK 26,000 per month. From 11th of March 2021 the maximum has
been increased to DKK 30,000, which is also the case for 2022. In other
words, companies keeping labour employed instead of making them
redundant get an economic compensation since they will only have to pay
the remaining part of the wage costs, i.e. the wage earner will keep the
existing wage. The employed will have to give up 5 holidays/overtime
work, and if there are no days left then either from the next year’s
holidays or 5 days without wage-income. This agreement and the state
support will be in force, for the time being, from the 9th of March to
the 8th of August, and for a few within tourism further. It has later
from 1st of May, 2020 been extended to apprentices as well. In December
2020 it has been extended for those branches were there is lock-down.

For self-employed, state compensation is 75 per cent of the loss of
revenue, but with a maximum of DKK 23,000 per month corresponding to the
rates in the wage compensation scheme for salaried employees agreed with
the labour market partners in the tri-partite agreement. The
compensation can reach to up to DKK 46,000 per person per month if the
self-employed has a spouse as employee. [^3] The compensation has been
increased to 30,000 DKK and also prolonged. For self-employed where
there has been declared a close-down during these times to 100 % of the
loss of revenue. Free-lancers should have had an income as free-lancer
at a minimum of 180,000 DKK in 2019, and, so far in 2020 have not had an
income above 0.8 mill. DKK.

**EUROMOD modelling:**

**1)** Wage compensation schemes for hourly wage earners and free
lancers are not implemented in EUROMOD.

**2)** Both for employees and self-employed, we consider the maximum
compensation amount to be DKK 30,000 per month.

## Consumption taxes

Simulated consumption tax liabilities paid by households depend on the
tax rules (e.g. the VAT rate) and on the tax base (consumption
expenditures or quantities). This is why, to simulate consumption tax in
EUROMOD, the input data must contain information on household
expenditures. The expenditures matched in the EUROMOD input files based
on SILC are reported directly by households in the HBS surveys at
purchasing prices. Therefore, they already include the consumption taxes
paid.

In Denmark there is the following:

i\) **VAT** (il_tva variable in EUROMOD) is the value-added tax. The
model also simulates at high disaggregation level the VAT liabilities
paid for each consumption category (output variables are tva01111,
tva01112, and so on and so forth, corresponding to COICOP codes 01111
and 01112, etc.)

ii\) **Excises** (il_tx variable in EUROMOD) are additional duties paid
over consumption and can be classified in two groups: ad-valorem excises
(il_txv) that depend on producer prices, and of specific or ad-quantum
excises (il_txa) that depend on consumed quantities.

Since consumption data from HBS refers to expenditures (price times
quantity), for the simulation of specific excises information on
consumption prices are needed.

### VAT (il_tva)

To extract the baseline VAT embedded in the expenditure consumption
reported by households we only need the VAT rate of the policy system
year. VAT rates usually do not vary too much across product, and are
typically three rates (standard, reduced and zero). In Denmark, the
standard VAT rate is 25%. The zero rate applies to products exempted by
EU directives, as well as newspapers.

<span id="_Toc222163746" class="anchor"></span>**Table 2.34** VAT rates
\[2022-2025\]

|  | Products | 2022 | 2023 | 2024 | 2025 |
|----|----|----|----|----|----|
| Standard |  | 25 % | 25 % | 25 % | 25 % |
| Zero | Only applies to products exempted by EU directives, and newspaper | 0% | 0% | 0% | 0 % |

Source: www.skm.dk

Excises cover alcoholic beverages (such as beer, wine, liquor) as the
central duties, but also on coffee, different form of chocolate. There
are a number of variations in the way these are imposed, and, this also
implies that whether it is paid by the consumer or by the producer
depends theoretically on the elasticity of demand as well as supply.

### Ad-valorem excises (il_txv)

Cigarettes and cigars are subject to ad-valorem excises, see below.

<span id="_Toc222163747" class="anchor"></span>**Table 2.35** Excises on
tobacco in percentage of price

|                                   | **2022** | **2023** | **2024** | **2025** |
|-----------------------------------|:--------:|:--------:|:--------:|:--------:|
| Cigarettes                        |  0.3205  |  0.3205  |  0.3205  |  0.3205  |
| Cigars, cigarillos and cigarillos |  0.3205  |  0.3205  |  0.3205  |  0.3205  |

Source: [www.skat.dk](http://www.skat.dk) and Skatter og Afgifter,
Oversigt 2023

### Specific excises (il_txa)

Specific excises taxes apply to different kinds of alcohol, coffee,
chocolate etc. as shown in Table 2.35.

**Table 2.36** Specific excise rates

| Products | 2022 | 2023 | 2024 | 2025 |
|:--:|:--:|:--:|:--:|:--:|
| Ethyl alcohol (per 100 l of pure alcohol) | 15000 | 15000 | 15080 | 15080 |
| Wine (per 100 l) | 1126 | 1126 | 1126 | 1126 |
| Sparkling wine (per 100 l) | 1461 | 1461 | 1461 | 1461 |
| Beer (per 100 L per Alcohol of finished product) | 48.74 | 48.74 | 48.74 | 48,74 |
| Cigarettes (per 1000 pieces) | 1935.4 | 1935.4 | 1935.4 | 1935,4 |
| Cigars (per 1000 pieces) | 1185.1 | 1185.1 | 1185.1 | 1185,1 |
| Other tobacco (Fine cut, per kg) (per 1000 pieces) | 1550.9 | 1550.9 | 1550.9 | 1550,9 |
| Electricty (per MWh) in øre | 76,3 | 8 | 76,1 | 72 |
| Natural Gas - Heating (per gigajoule) | 111.94 | 113.48 | 121.98 | 193,9 |
| Liquefied hydrocarbons (per 1000 kg) | 4050 | 4108 | 3746 | 6386 |
| Gas Oil - Heating (per 1000L) | 2736 | 2775 | 2988 | 4725 |
| Coal and Coke - Heating (per gigajoule, 1 GJ = 0.0316 ton) | 63.0 | 63.9 | 68.8 | 149,7 |
| Petrol-Leaded (per 1000L) | 5230 | 5300 | 5710 | 6178 |
| Petrol-Unleaded (per 1000L) | 4440 | 4500 | 4850 | 5097 |
| Gas Oil- Propellant (per 1000L) | 3247 | 3293 | 3969 | 4916 |

Source: [www.skat.dk](http://www.skat.dk) and Skatter og Afgifter,
Oversigt 2023

**Table 2.37** Prices of Excise products

| Prices | 2022 | 2023 | 2024<sup>n</sup> | 2025<sup>n</sup> |
|----|---:|---:|---:|---:|
| Ethyl alcohol | 173.71 | 182.18 | 196.85 | 194.51 |
| Wine | 94.84 | 96.93 | 105.42 | 105.27 |
| Sparkling Wine | 234.21 | 239.40 | 262.12 | 261.74 |
| Beer | 26.21 | 28.21 | 29.46 | 29.65 |
| Other tobacco per kg | 2511.33 | 2639.04 | 2709.67 | 2792.05 |
| Cigarettes | 2718.64 | 2848.37 | 2931.59 | 3002.54 |
| Electricity per MWh | 3470.20 | 2550.87 | 2398.88 | 2277.86 |
| Natural Gas per gigajoule | 372.54 | 298.94 | 263.81 | 231.81 |
| Liquefied hydrocarbons per ton | 18352.92 | 19307.41 | 20459.47 | 20123.75 |
| Gas-oil-Heating 1000 l. | 15172.64 | 13631.50 | 13592.53 | 13457.82 |
| Petrol-unleaded 1000 L | 15538.11 | 14706.64 | 14899.61 | 14441.60 |
| Gas-Oil Propellant 1000 L. | 14612.00 | 12948.58 | 12711.27 | 13129.21 |

Note: n: nowcasted

Source: www.skm.dk

*Goods subject to excise duties are nowcasted, similarly to what the
model does to update incomes from SILC. We combine the latest available
data from the following sources:*

*Prices per product, usually from last year, but for instance, fuel
prices have only 15 days delay.*

*Inflation: Harmonised Index of Consumer Prices (HICP, Eurostat) at
COICOP 5 digits, usually for the first quarter for beta release and up
to third quarter 3 for final release.*

*Inflation quarter-on-quarter forecasts (DG ECFIN, confidential) by HICP
main groups (Unprocessed food, Processed food including alcohol and
tobacco, Non-energy industrial goods, Energy, Services - overall index
excluding goods) of quarters 2, 3 and 4, as needed for each release.*

# Data

## General description

From 2023 onwards, the database prepared by Eurostat - EUROMOD SILC
database (EMSD), has been enriched with several national SILC variables
provided by the National Statistical Office. In addition to these, the
archive also includes:

all UDB (User Database) variables;

EUROMOD variables created and imputed by Eurostat because of restricted
data access or knowledge in-house.

Based on the EMSD, the national team derives additional variables
requiring a deep understanding of country specificities (for instance
national tax-benefit rules). The final EUROMOD input dataset is
therefore made of variables created by both Eurostat and national team.

<span id="_Toc222163748" class="anchor"></span>**Table 3.1** EUROMOD
database description

| **EUROMOD database**    | **DK_2024_c1**                        |
|-------------------------|---------------------------------------|
| Original name           | DK_EMSD2_2024                         |
| Provider                | Statistics Denmark                    |
| Year of collection      | 2024                                  |
| Period of collection    | March-June (interview part)           |
| Income reference period | 2023 (calendar year)                  |
| Sampling                | Random probability sampling           |
| Unit of assessment      | Households                            |
| Coverage                | Private households                    |
| Sample size             | 6.010 households (11,200 individuals) |

Source:
https://ec.europa.eu/eurostat/web/microdata/european-union-statistics-on-income-and-living-conditions

The data sample is a representative sample of persons aged 16 years or
older. From this sample the households are defined as persons who share
expenses for daily living or share meals regularly. The data contains
information on both the households and its members.

The data are compiled by Statistics Denmark. While information on the
composition of the households, their living conditions, their view on
their economic stance, their labour market status and their health
status is collected through an interview survey (conducted between March
and June), further information on income, education and housing are
added from official registry data.

While incomes in the EU-SILC are recorded in EUR and yearly, the derived
EUROMOD data are stated in Danish kroner (DKK) in (mostly) monthly
terms.

## Sample quality and weights 

As EU-SILC is based on a sample of persons and household there are some
statistical uncertainty related to the data. This is partly due to the
presence of statistical uncertainty and partly due to the risk of
biases. A calibration of the survey is carried out in order to limit any
bias and make sure that the sample reflects the population on factors
such as demographics and incomes. For the published variables on making
ends meet and the burden of housing costs, the effect and risk of bias
is assumed to be negligible due to the strong correlation with incomes.

### Non-response

The household non-response rate is 51.27 per cent from the sampling of
private households to the final sample of 6,010 households in the Danish
part of the DK_EMSD2_2024 data. Statistics Denmark has not documented
the reasons for non-response explicitly. It is possible for citizen to
register for so-called ‘researcher protection’ with the registration
office. Nevertheless, the sample should be a good reflection of the
population in the demographics and incomes dimensions since a
calibration of the survey is carried out.

The non-response is counteracted through the modification of weights,
see first bullet in the next section.

### Weights

The household cross-sectional weights (variable **DB090** in EU-SILC)
form the background for the EUROMOD weight variable **dwt**. The weights
have been corrected for household non-response in order to calibrate the
sample to the population, taking account of the population distribution
in the following categories:

Sex

Age (5 classes 0-15, 16-24, 25-49, 50-64, 65+)

Family type

Income mass and income groups (12 intervals; 1, 5, 10, … 90, 95, 99th
percentile).

Risk of poverty

Equivalised disposable income

The size of the household

Education level of the person with the highest professional status in
the household

Socio-economic status of main income holder in the household.

<span id="_Toc222163749" class="anchor"></span>**Table 3.2** Descriptive
Statistics of weights

|                     | DB090<sup>1</sup> |
|---------------------|-------------------|
| Number              | 11200             |
| Mean                | 526.71            |
| Median              | 422.79            |
| Minimum             | 6.5               |
| Maximum             | 2430.1            |
| Max/Min             | 373.9             |
| Decile 1            | 184.9             |
| Decile 9            | 1019.3            |
| Decile 9 / Decile 1 | 5.5               |

Note: 1 The weight **dwt** in the EUROMOD data is equal to DB090.

Source: Own elaboration

## Data adjustment 

To accommodate the modelling of tax and benefit rules using the EU-SILC
data, a few variables had to be adjusted.

### Labour market activities, months per year

EU-SILC UDB does not provide information on the number of months that
different incomes are paid during the year. By default, it is imputed
based on the main economic status during the year. This affects the
following variables (variable unit is months per year):

yemmy Employment

kfbmy Fringe Benefits

ysemy Self Employment

bunmy Unemployment

pdimy Pension, disability

poamy Pension, old age

psumy Pension, survivors.

## Imputations and assumptions

### Time period

The used EU-SILC data for 2024 is based on survey data from interviews
conducted March-May 2024 combined with registry data from the calendar
year 2023 on incomes, dwellings, and educational information.

The input registry data on incomes are aggregated annual numbers, but
are for the use in EUROMOD converted into monthly figures, thus
implicitly assuming a regular flow of income throughout the year.
However, a number of variables in the data that record the number of
months with different income types, such as yemmy (“Months with
employment income”) or bunmy (“Months with unemployment benefit
income”), do not exist in EU-SILC and are therefore imputed see section
3.3.1.

### Gross incomes

The income variables in the Danish SILC-data only contain gross incomes.
Net-to-gross conversions have therefore not been necessary.

### Disaggregation of harmonised variables

Since the year 2021, many variables provided by the national statistical
office have been used. Specifically, these are the following variables:
pdi, poa00, poa01, poa02, poa03, poaot, pyr, ypp, bfa, bfachnm, bfach00,
bfached, bfachot, bho01, bho02, bunct, bhtuc, bsa, bsaot, bunot,
bcbplcs, aiv.

Variables are created by the national statistical office using both silc
and administrative data

Housing allowances are split by the age of the recipient into a housing
benefit (bho01) for recipient below the age of 67 and a housing grant
(bho02) for pensioners. The receipt of housing allowances is based on
the concept of housing costs, including rent, but not heating etc. Under
some circumstances related both to characteristics of the dwelling and
of the tenancy that cannot be simulated, the housing cost is augmented.
To establish this base for the computation of the housing allowances,
the housing costs in imputed hence by reversing the rules for the
housing allowances, creating the housing cost base for housing benefits
(xhc01) and for housing grants (xhc02). The variable xivhc is then
imputed for all the households in the sample using predictions of xhc01
on and xhc02 on the basis of household characteristics and SILC reported
housing cost.

The previous earnings (yempv) on which the level of unemployment benefit
is based is calculated by reversing the rules for the unemployment
benefit.

## Break in series

The quality of the Danish EUROMOD input data was improved due to the
availability of disaggregated benefits which simplified the
disaggregation of harmonised variables and improved the simulation of
unemployment benefit. This however reduces the comparability of results
using the 2016 dataset with results using earlier datasets.

Maternity and paternity leave benefits are included in the employment
income variable for private sector employees. Maternity and paternity
leave benefits for public sector employees and recipients of transfers
are now included in hy052g (while earlier in py122).

Some income types are reclassified from 2020 SILC, which is not
affecting disposable income or the main Eurostat indicators, while the
reclassification will affect the income levels of some income types.

As we wrote in the previous paragraph since the year 2021, many
variables have been provided by the national statistical office using
both silc and administrative data. This reduces the comparability of the
series.

## Updating factors

To account for any time lag between the input dataset and the policy
year, updating factors are used. Each monetary variable (i.e. each
income component) is updated so as to account for changes in the
non-simulated variables that have taken place between the year of the
data and the year of the simulated tax-benefit system. Updating factors
are generally based on changes in the average value of an income
component between the year of the data and the policy year. For detailed
information about the construction of each updating factor as well as
the sources that have been used, see Annex 1.

As a rule, updating factors are provided both for simulated and
non-simulated income components present in the input dataset. Note
however that in the case of simulated variables, the actual simulated
amounts are used in the baseline rather than the uprated original
variables in the dataset. Updating factors for simulated variables are
provided so as to facilitate the use of the model in cases when the user
wishes to turn off the simulation of a particular variable.

## Extended input data (with household expenditures for the simulation of consumption taxes)

For the simulation of consumption taxes, the model needs to be run with
extended EUROMOD input files. They consist of the core EUROMOD input
files based on EU-SILC or National SILC, extended with new variables
(household-level income shares of expenditures by product) imputed from
EU/National-HBS. The semi-parametric method implemented for the
imputation follows the methodology developed by Akoğuz et al (2020).

Table 3.3 summarizes the major features of the most recent database used
to be run with the policy systems of 2021-2024.

**\**

<span id="_Toc222163750" class="anchor"></span>**Table 3.3** Extended
EUROMOD database description

| Extended EUROMOD database for the simulation of consumption taxes | SILC 2024 – Income year 2023 – Expenditures from HBS 2015 |
|----|----|
| EUROMOD database | DK_2024_c1_2015_03_e1 |
| Year of collection (HBS) and source | HBS 2015 – EU |
| Year of collection (SILC) and source | SILC 2024 – EU |
| Coverage and sample size | 6.750 households (13,244 individuals) |
| Share of households with negative incomes excluded from the matching procedure | 0.13% |

Note: z: source of expenditure shares data with u (EU-HBS), e (EMSD) n
(national HBS), a (admin data)

M: version of matching (correlative number), f: source of SILC dataset
(National, UDB, ESMD): a, b or c 

N: version of SILC processing (correlative number) 

Source: own elaboration

These extended EUROMOD files contain all the variables included in the
standard EUROMOD input files plus the income shares of each consumption
category included in HBS. For example, for countries with consumption
disaggregation at 4 COICOP level (5 digits), there will be close to 200
additional variables, each one with the income shares of expenditure
(household level) for that particular consumption category (e.g.
starting from the income share of rice consumption: xs01111; bread:
xs01112, and so on and so forth). The number of additional variables
depends on the granularity available in HBS, and it varies across
countries).

For the case of Denmark, data DK_2024_c1_2015_03_e1, the number of
variables included (income shares of expenditures, xs_c\*) are 193,
corresponding to the harmonized consumption categories defined at COICOP
\[2003\] level 4 (five digits).

This database is an extension of the core EUROMOD input database, and so
it is based on the same sample (i.e., same identifiers "idperson" and
"idhh" to identify persons and households, respectively) and contains
the same variables plus the income shares of expenditure (xs\_\*
variables).

In Table 3.3 we present the share of households' consumption
expenditures by COICOP first level captured in our matched databases
(extended EM input files) with respect to the original reported
expenditures in HBS. The column that refers to the same year (in this
case, HBS 2015 with Extended EM Input 2015) directly depends on the
quality of the imputation procedure, while the comparison across
different years is influenced not only by the matching noise but also by
the changes in population characteristics and by the underlying
distribution of income. Therefore, the coverage displayed in the second
column is just informative but is not and should not be used to evaluate
nor validate the imputation procedure.

Information on the coverage of these simulated expenditures (coming from
the imputation of HBS 2015 to more recent SILC-based data) with respect
to the expenditures reported by National Accounts is included in section
4 of this report, together with the other macro-validation results.

Below we summarize the main findings from the imputation validation
checks for DK.

**\**

<span id="_Toc222163751" class="anchor"></span>**Table 3.4**.
Expenditure coverage of Extended EM Input files

| COICOP group | HBS 2015 – Extended EM Input 2015 | HBS 2015 – Extended EM Input 2024 |  |
|----|---:|---:|---:|
| 1 | 91.30% | 96.7% |  |
| 2 | 90.47% | 95.6% |  |
| 3 | 87.17% | 87.3% |  |
| 4 | 98.31% | 101.2% |  |
| 5 | 82.54% | 89.7% |  |
| 6 | 96.54% | 99.4% |  |
| 7 | 69.07% | 77.1% |  |
| 8 | 98.14% | 97.5% |  |
| 9 | 89.01% | 96.4% |  |
| 10 | 59.47% | 102.5% |  |
| 11 | 86.89% | 93.9% |  |
| 12 | 90.49% | 95.7% |  |

Source: own elaboration

The matched data do generally well and do not produce any big distortion
compared to original HBS (most of them are \<30%). There are few
exceptions to this which includes 3-digit level of CP063, CP071, CP081
and CP105 where the matching produces a more severe distortion. COICOP
02 expenditures (alcohol and tobacco) are fully under-reported in HBS
and as such results under-reported also in the matched dataset but that
does not depend on the matching procedure. Other problematic categories
to be signalled regard transport expenses (CP07) where expenditures for
CP071 are highly over-reported in HBS while results under-reported when
looking at the matched dataset, this is the result of both imprecise
starting data as well as distortions happening because of the matching
procedure. 

General issues related to HBS original data regards: over-reporting for
CP125, CP043 and under-reporting (more frequent) for CP022, CP063,
CP091, CP092, CP094, CP105, CP124, CP126. 

Please note that, due to the lack of information in the HBS files
distributed by Eurostat, there is no consumption reported at 5-digit
COICOP level for the following 3-digit codes: 

CP127, CP103. Positive consumption might exist for 3-digit or 4-digit
levels, but EUROMOD uses only 5-digit values.

 

# Validation

## Aggregate Validation 

EUROMOD results are validated against external benchmarks. Detailed
comparisons of the number of people receiving a given income component
and total yearly amounts are shown in Annex 3. Both market incomes and
non-simulated taxes and benefits in the input dataset as well as
simulated taxes and benefits are validated against external official
data. The main discrepancies between EUROMOD results and external
benchmarks are discussed in the following subsections. Factors that may
explain the observed differences are also discussed.

### Components of disposable income

<span id="_Toc222163752" class="anchor"></span>**Table 4.1** Components
of disposable income

|                                                   | **EUROMOD** | **EU-SILC** |
|---------------------------------------------------|-------------|-------------|
|                                                   | ils_dispy   | HY020       |
| Employee cash or near cash income                 | \+          | \+          |
| Employer's social insurance contribution          | 0           | 0           |
| Company car                                       | 0           | \+          |
| Contributions to individual private pension plans | 0           | 0           |
| Cash benefits or losses from self-employment      | \+          | \+          |
| Pension from individual private plans             | \+          | 0           |
| Unemployment benefits                             | \+          | \+          |
| Old-age benefits                                  | \+          | \+          |
| Survivor’ benefits                                | \+          | \+          |
| Sickness benefits                                 | \+          | \+          |
| Disability benefits                               | \+          | \+          |
| Education-related allowances                      | \+          | \+          |
| Income from rental of a property or land          | \+          | \+          |
| Family/children related allowances                | \+          | \+          |
| Social exclusion not elsewhere classified         | \+          | \+          |
| Housing allowances                                | \+          | \+          |
| Regular inter-household cash transfer received    | \+          | \+          |
| Interests, dividends, etc.                        | \+          | \+          |
| Income received by people aged under 16           | \+          | \+          |
| Regular taxes on wealth<sup>1</sup>               | \-          | \-          |
| Regular inter-household cash transfer paid        | \-          | \-          |
| Tax on income and social contributions            | \-          | \-          |
| Repayments/receipts for tax adjustment            | \+          | \+          |

Notes:1) Not applicable for Denmark; Contents of HY020 are based on
EUROSTAT (2010).

Source: Euromod, EU-SILC

### Validation of incomes inputted into the simulation

Tables A3.1 and A3.2 compare with external statistics the number of
people and the aggregated amount of a number of market income
components. Employment income is well captured by SILC data both in
terms of number of recipients and aggregated amount. The number of
people receiving income from self-employment is over-reported in SILC
when compared with external statistics, although the amount matches the
external statistics much better. A reason might be that people in
principle can have several types of income (wages, benefits,
self-employed income) and thus the numbers counting as self-employed
will vary more than the precise income as this comes from income in the
tax registers. Discrepancies arise also with respect to the investment
income, which is quite under-reported in SILC when compared to external
statistics. Both under-reporting of investment income as well as a
discrepancy in the concept of investment income used in SILC and in the
external statistics are likely to be the main causes of lacking
matching. It should be also noted, that Private pensions are
overestimated. As mentioned in section 3.4.3 information on private
pensions has been provided by the Danish Statistical Office.

Recipients and amounts of education-related allowances are
over-represented in EU-SILC (see Table A3.5 and A3.6 in Annex 3).
EUROMOD counts as a recipient all the individuals receiving this benefit
at least once during the year, while external statistics are based on
full time equivalents. Disability pensions are underestimated and early
retirement pension overestimated but both have been provided directly by
the Danish Statistical Office (see Section 3.4.3).

### Validation of outputted (simulated) incomes

For the benefits, taxes and social contributions that are simulated by
EUROMOD, cf. Table A3.3, A3.4, A3.5 and A3.6 in Annex 3, there are
generally reasonable fits. The most important exceptions are listed
below.

A change in the eligibility rules for housing benefit and grant may
accommodate for the divergence between the external statistics and the
EUROMOD simulations. The housing grant applies to old-age
pensioner-tenants, while the housing benefit applies to tenants under 67
years of age. However, in the external statistics the housing grant also
encompasses disability pensioners (i.e. non-pensioners) who are entitled
to it. This means that the external numbers for the housing grant are
inflated by these 'old' disability pensioners relative to the
simulations based on the new policy rules. Likewise, the external data
for the housing benefit are 'deflated' by these ‘old-rule’ disability
pensioners, compared to the simulations. The under-simulation of number
of people receiving unemployment benefit compared to external statistics
is probably based on the way of counting people. This is reflected also
in the aggregated simulated amount.

The overestimation of social assistance is likely to be driven both by
limitations in our simulation, which cannot control for the requirement
of experiencing particularly stressful (social) events, as well as by
issues such as benefit non take up.

The child benefit amount ('bfachnm_s') is underestimated in EUROMOD,
while the supplement is overestimated. This is due to the challenge of
distinguishing, in external statistics, between 'bfach00_s' and
'bfachnm_s' both of which represent child family grants addressed to
different types of households

### Validation of outputted (simulated) expenses

The validation of simulated expenditures used to model consumption taxes
includes two types of comparisons:  

1.  Simulated household consumption expenditures compared to
    expenditures collected by National Accounts (NA) of that same
    year.  

2.  Simulated consumption taxes (based on NA-adjusted simulated
    expenditures) compared to administrative data on consumption tax
    revenues.

Table A3.9 and A3.10 show the validation of consumption taxes related
amounts. The top part of table A3.9 compares expenditures aggregated
amount from EUROMOD simulations with National Account (NA) external
statistics as reported by EUROSTAT. Coicop level 1 categories perform
quite good when looking at “01 – food and non-alcoholic beverages”, “03
– Clothing and footwear”, “04 – housing, water and fuel (exc. Imputed
rent)” performs quite well and results in good coverage of relative NA
years. Coicop level 1 categories “05 - Furnishings, household
equipment”, “06 – health”, “08 – communications”, “09 – recreation and
culture” also performs relative good as they cover between 60 and 80% of
the NA expenses. The remaining categories instead are undersimulated and
this is probably due to under-reporting of those categories in original
data (e.g. tobacco and alcohol). To note that “08 – communications” is
quite oversimulated.

The second part of Table A3.9 compares aggregate revenues from
consumption taxes (i.e. VAT and excises) to external statistics from
EUROSTAT. The bottom part of the table shows simulated aggregate revenue
for some category of interest such as alcoholic drinks, tobacco and
energy products. In Denmark revenue from VAT and excises are
undersimulated. The simulation captures about 50 to 80% of the revenue
from consumption taxes. When looking at consumption taxes on specific
items, the simulation significantly underestimates the government
revenue on some product like tobacco and alcohol and this is probably
due to undersimulation of expenditures while excises on energy products
seem to do quite well, especially for the full energy category as well
as the natural gas category. The discrepancies are partly due to the
fact that the survey data underpinning the CT simulation are based on
consumers declared consumption that may differ from the actual
consumption (e.g. people misreport about how much they smoke and drink).
To correct for this problem, EUROMOD provides also adjusted consumption
aggregates, where the calibration/correcting factor is the ratio between
NA aggregated expenditures and EM aggregated simulated expenditures
level 1 at baseline. Effectively NA adjustment scales-up (or down)
consumption and tax liabilities of all individuals. Table A3.10 compares
annual Government revenue from consumption taxes after applying
calibration to NA. As a result about 60% of aggregate VAT revenues are
simulated in Euromod, while the model captures almost the whole revenue
from excises after calibration (98%). There might be various reasons for
these discrepancies. The major one being that several groups that pay
significant amounts of VAT are not covered in HBS. Among these groups
are government and third sector, hospitals and business enterprises such
as financial companies that are themselves exempt from VAT but have to
pay the input VAT from all previous production stages and private
households explicitly not covered by the HBS, such as people in
dormitories, jails, or retirement homes (although the latter are not
such big spenders). When looking at specific items at lower coicop
details, the calibration also improves the estimation of government
revenue although some differences w.r.t. official statistics remain
higher than 30-40%.

## Income distribution 

All income distribution results presented here are computed for
individuals according to their household disposable income (HDI)
equivalised by the “modified OECD” equivalence scale. HDI is calculated
as the sum of incomes from all sources of all household members net of
income tax and social insurance contributions. The weights in the OECD
equivalence are: first adult=1; additional people aged 14+ = 0.5;
additional people aged less than 14 = 0.3.

### Income inequality

A comparison of distributional indicators derived from EUROMOD-generated
household disposable income with external statistics shows that over all
the EUROMOD estimates fit well with the EUROSTAT income distribution
measures.

###  Poverty rates 

A computation of poverty rates by gender and age using EUROMOD shows
that EUROMOD estimates the incidence of poverty in Denmark according to
EUROSTAT database rather well with a few exceptions (table A3.8). There
are some discrepancies using the 60 %of median HDI: at risk of poverty
rate lower than expected below the age of 15 and above 64, and higher
for 25-64 years of age.

## Summary of “health warnings”

This final section summarises the main findings in terms of particular
aspects of the Danish part of EUROMOD or its database that should be
borne in mind when planning appropriate uses of the model and in
interpreting results.

Take-up rates in Denmark are generally high so that the level of take-up
should not have any specific impact on calculations. There is some
tax-evasion in Denmark, but this is at a low level compared to other
countries and should therefore only marginally impact the overall level
of calculation, however with a possible impact on distribution.

The land value tax is recorded as part of the total housing costs and
not simulated as there is no information on the land value or the tax
payment. The land value tax is recorded as a housing cost to make it
comparable to tenants, who (indirectly) pay the land value tax as a part
of their rent.

The only transferability and influence of income of a spouse is with
regard to dividend income, and this is not taken into account.

In contrast to other EU-SILC countries, Denmark includes a high number
of respondents with negative investment income. In Denmark, windfall
gains and losses on stocks are taxed in the same way as dividend when
stocks are traded, these are included in the investment income variable.
Losses are furthermore deductible from capital gains in the following
years and are very well recorded in the data. Negative investment
incomes are recoded to 0 in the neg_dk policy and only positive values
are used in the model. Two exceptions to this rule are the calculation
of the bottom and medium tax bracket where the transfer negative net
capital income can be used to reduce the tax burden.

Maternity and parental leave benefits are simulated but switched off for
policy years 2015-2025.

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

# References

EUROSTAT (2010): EU-SILC 065 (2008-operation) - Description of Target
Variables: Cross-sectional and Longitudinal. Version January 2010.

StatBank (2015). *www.dst.dk*. StatistikBanken is the Danish National
Statistical Office’s (Statistics Denmark) online statistical service.

## Sources for tax-benefit descriptions/rules

The description and the derived modelling of the Danish tax and benefit
system build on various sources, mostly only in the Danish language:

The Ministry of Taxation,
[www.skm.dk/foreign/](http://www.skm.dk/foreign/)

The central legal information: <https://www.retsinformation.dk/>

The Ministry for Employment: <http://bm.dk/>

The citizens’ entry point for information on public benefits etc.,
[www.borger.dk](http://www.borger.dk)

# List of abbreviations and definitions

| Abbreviations | Definitions |
|----|----|
| ATP | Arbejdsmarkedets tillægspension |
| BCA | Benefit Calibration Adjustment |
| BTA | Benefit Take-up Adjustment |
| CIA | Consumption Inflation Adjustment |
| COICOP | Classification Of Individual COnsumption according to Purpose |
| CT | Consumption Taxes |
| DG | Directorate-General |
| DK | Denmark |
| DKK | Danish Krone |
| DG ECFIN | European Commission Directorate-General for Economic and Financial Affairs |
| EEA | European Economic Area |
| EM | EUROMOD |
| DG EMPL | Directorate-General for Employment, Social Affairs and Inclusion |
| EMSD | EUROMOD SILC Database |
| ESTAT | Eurostat |
| EU | European Union |
| EUR | Euro |
| GJ | Gigajoule |
| HBS | Household Budget Survey |
| HDI | Household Disposable Income |
| HICP | Harmonised Index of Consumer Prices |
| ISER | Institute for Social and Economic Research |
| JRC | Joint Research Centre |
| LMC | Labour Market Contribution |
| NRR | Net Replacement Rate |
| OECD | Organisation for Economic Co-operation and Development |
| SG REFORM | European Commission Reform and Investment Task Force |
| SG | Secretariat-General |
| SIC | Social Insurance Contributions |
| SILC | Statistics on Income and Living Conditions |
| DG TAXUD | European Commission Directorate-General for Taxation and Customs |
| UB | Unemployment Benefits |
| UDB | User Database |
| VAT | Value Added Tax |

# List of boxes

[**Box 1.** Income included in income test
[24](#_Toc222163574)](#_Toc222163574)

[**Box 2.** Income included in the income test:
[29](#_Toc222163575)](#_Toc222163575)

[**Box 3.** Income included in the income test:
[30](#_Toc222163576)](#_Toc222163576)

[**Box 4**. Income included in the income test:
[33](#_Toc222163577)](#_Toc222163577)

[**Box 5.** Income of all household members (except income from children
(since 2019)) included in the income test:
[34](#_Toc222163578)](#_Toc222163578)

[**Box 6.** Income included in the income test until 1<sup>st</sup> of
January 2023: [38](#_Toc222163579)](#_Toc222163579)

[**Box 7.** Income included in the wealth test:
[39](#_Toc222163580)](#_Toc222163580)

[**Box 8.** Income included in the income test:
[40](#_Toc222163581)](#_Toc222163581)

[**Box 9.** Calculation of the Personal Income and Taxable Income tax
bases [43](#_Toc222163582)](#_Toc222163582)

[**Box 10.** Income included in the income test:
[47](#_Toc222163583)](#_Toc222163583)

# List of figures

[**Figure A1.** Policy effects in Denmark in 2024-2025
[75](#_Toc222163584)](#_Toc222163584)

# List of tables

[**Table 2.1** Simulation of benefits in EUROMOD
[13](#Table2_1)](#Table2_1)

[**Table 2.2** Simulation of taxes and social contributions in EUROMOD
[15](#_Toc222163714)](#_Toc222163714)

[**Table 2.3** Key Changes in Danish Social Policy and Taxation
(2022-2025) [16](#_Toc222163715)](#_Toc222163715)

[**Table 2.4** EUROMOD Spine: order of simulation, 2021-2024
[18](#_Toc222163716)](#_Toc222163716)

[**Table 2.5** EUROMOD – Indirect Taxation spine: order of simulations
\[2021 - 2024\] [18](#_Toc222163717)](#_Toc222163717)

[**Table 2.6** Characteristics of the unemployment benefit
[21](#_Toc222163718)](#_Toc222163718)

[**Table 2.7** Upper limits for unemployment benefits per year (DKK)
[23](#_Toc222163719)](#_Toc222163719)

[**Table 2.8** Social assistance benefits, per month per person. DKK
[26](#_Toc222163720)](#_Toc222163720)

[**Table 2.9** Deduction of employment income, amount per working hour
(DKK) [26](#_Toc222163721)](#_Toc222163721)

[**Table 2.10** Ceiling per month and household before tax (Danish
Kroner) [27](#_Toc222163722)](#_Toc222163722)

[**Table 2.11** Child family grant, per child per year, (Danish Kroner).
[29](#_Toc222163723)](#_Toc222163723)

[**Table 2.12** Ordinary child benefit rates, per. year, (DKK)
[30](#_Toc222163724)](#_Toc222163724)

[**Table 2.13** Parental leave rates, (Danish Kroner)
[32](#_Toc222163725)](#_Toc222163725)

[**Table 2.14** Green check compensations scheme per year
[34](#_Toc222163726)](#_Toc222163726)

[**Table 2.15** Income augmentation with wealth for calculation of
housing benefit, (DKK). [35](#_Toc222163727)](#_Toc222163727)

[**Table 2.16** Various limits etc. for housing benefit, per year. DKK
[35](#_Toc222163728)](#_Toc222163728)

[**Table 2.17** Income augmentation with wealth for calculation of
housing grant, [36](#_Toc222163729)](#_Toc222163729)

[**Table 2.18** Various limits etc. for housing grant, per year, (DKK).
[36](#_Toc222163730)](#_Toc222163730)

[**Table 2.19** Income threshold and benefit amount for basic old-age
pension, per year (DKK) [37](#_Toc222163731)](#_Toc222163731)

[**Table 2.20** Income dependence parameters for old-age pension
supplement, per year. [38](#_Toc222163732)](#_Toc222163732)

[**Table 2.21** Benefits for old-age pension supplement, per year (DKK).
[39](#_Toc222163733)](#_Toc222163733)

[**Table 2.22** Benefit and asset test for supplementary pension, per
year, (DKK). [40](#_Toc222163734)](#_Toc222163734)

[**Table 2.23** Benefit test for personal supplement rate, per year
(DKK). [40](#_Toc222163735)](#_Toc222163735)

[**Table 2.24** Supplementary labour market pension contributions,
[41](#_Toc222163736)](#_Toc222163736)

[**Table 2.25** Voluntary monthly contribution to unemployment insurance
and early retirement scheme, for full time insured. (DKK)
[42](#_Toc222163737)](#_Toc222163737)

[**Table 2.26** General Personal Allowance, (DKK).
[44](#_Toc222163738)](#_Toc222163738)

[**Table 2.27** Earned income tax-credit, per year,
(*Beskæftigelsesfradrag*) [45](#_Toc222163739)](#_Toc222163739)

[**Table 2.28** Distribution of municipality tax rates (%),
(kommuneskat) [46](#_Toc222163740)](#_Toc222163740)

[**Table 2.29** Municipal average church tax rates, (%)
[46](#_Toc222163741)](#_Toc222163741)

[**Table 2.30** Bottom bracket tax rates (%), (bundskat).
[47](#_Toc222163742)](#_Toc222163742)

[**Table 2.31** Top bracket tax rates and allowances,
[48](#_Toc222163743)](#_Toc222163743)

[**Table 2.32** Tax ceiling, [48](#_Toc222163744)](#_Toc222163744)

[**Table 2.33** Extra temporary child benefit, (Danish Kroner)
[49](#_Toc222163745)](#_Toc222163745)

[**Table 2.34** VAT rates \[2022-2025\]
[51](#_Toc222163746)](#_Toc222163746)

[**Table 2.35** Excises on tobacco in percentage of price
[52](#_Toc222163747)](#_Toc222163747)

[**Table 3.1** EUROMOD database description
[54](#_Toc222163748)](#_Toc222163748)

[**Table 3.2** Descriptive Statistics of weights
[56](#_Toc222163749)](#_Toc222163749)

[**Table 3.3** Extended EUROMOD database description
[59](#_Toc222163750)](#_Toc222163750)

[**Table 3.4**. Expenditure coverage of Extended EM Input files
[60](#_Toc222163751)](#_Toc222163751)

[**Table 4.1** Components of disposable income
[61](#_Toc222163752)](#_Toc222163752)

[**Table A1.1** Uprating factor values, 2014-2025
[73](#_Toc222163753)](#_Toc222163753)

[**Table A2.1** Policy effects including impact of inflation in Denmark
in 2024-2025 [74](#_Toc222163754)](#_Toc222163754)

[**Table A3.1** Validation Tables [76](#_Toc222163755)](#_Toc222163755)

# List of Annexes

## Annex 1. Uprating Factors

<span id="_Toc222163753" class="anchor"></span>**Table A1.1** Uprating
factor values, 2014-2025

|  |  | **2014** | **2015** | **2016** | **2017** | **2018** | **2019** | **2020** | **2021** | **2022** | **2023** | **2024** | **2025** |
|----|----|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Harmonised Index of Consumer Prices | \$HICP | 99.78 | 100.0 | 100.0 | 101.1 | 101.8 | 102.5 | 102.9 | 104.9 | 113.8 | 117.6 | 119.1 | 121.31 |
| Consumer Price Index (2015=100) | \$f_cpi | 99.6 | 100 | 100.3 | 101.4 | 102.3 | 103 | 103.4 | 105.4 | 113.6 | 116.4 | 118.5 | 120.7 |
| Indices of average earnings in Corporations and Organizations (2005=100) | \$f_earnings | 126.4 | 128.3 | 130.5 | 132.9 | 135.8 | 138.6 | 141 | 144.5 | 146.1 | 150.9 | 156.2 | 161.6 |
| Lagged indices of average earnings in Corporations and Organizations (2005=100) | \$f_earningsLag | 124.6 | 126.4 | 128.3 | 130.5 | 132.9 | 135.8 | 138.6 | 141 | 144.5 | 146.1 | 150.9 | 156.2 |
| Share index (at the end of period) | \$f_share | 608 | 786 | 723 | 836 | 752 | 946 | 1216 | 1481 | 1392 | 1626 | 1553 |  |
| No uprating | \$f_none | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

Source: www.statistikbanken.dk

## Annex 2. Policy effects in 2024-25

Table 1 and Figure 1 show the effect of 2025 policies on mean
equivalised household disposable income by income component and income
decile group. The effect is estimated as a difference between simulated
household net income under the 2025 tax-benefit policies (deflating
monetary parameters by Eurostat’s Harmonized Index of Consumer Prices,
HICP) and net incomes simulated under 2025 policies, as a percentage of
mean equivalised household disposable income in 2024.

The total effect of (deflated) 2024 policies on mean income is 1.16
which is higher than last year relatively -0.44 %. No major reforms have
taken place from 2024 to 2025, see Section 2.2., except a higher basic
allowance for those below the age of 18 so that the level now is the
same for all people. The higher income direct taxes in decile 2 is
difficult to explain, perhaps the large increase in public pensions can
be part of the reason therefore.

The core reason for the change can therefore be that the change in
consumer price inflation rate is the one single element best explaining
the changes in the distribution during the year, as witnessed by
comparing Table 1 and 2. Still, 2025 compared to 2024 has given lower
income groups a higher real income development compared to higher income
groups, mainly as a consequence of the higher indexation in 2025
compared to 2024 as social benefits indexation takes place with a delay.
The lack of wage incomes impact on receiving the basic public pension
can also help in explaining that higher income groups have increase in
the level of public pensions.

The increase in income for the lowest income groups without taken into
account changes in inflation as witnessed in Table 2 can also be
explained by the way benefits are indexed in the Danish welfare state,
however higher than for other income groups, albeit the impact of the
tax-system still favor’s the higher income groups development.

<span id="_Toc222163754" class="anchor"></span>**Table A2.1** Policy
effects including impact of inflation in Denmark in 2024-2025

<table style="width:65%;">
<colgroup>
<col style="width: 5%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 6%" />
<col style="width: 7%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 6%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Decile</strong></th>
<th>Original income</th>
<th>Public pensions</th>
<th>Means-tested benefits</th>
<th><p>Non means-</p>
<p>tested benefits</p></th>
<th>Employee SIC</th>
<th>Self-employed SIC</th>
<th>Other SIC</th>
<th>Direct taxes</th>
<th>Disposable income</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><strong>1</strong></td>
<td>0,00</td>
<td>0,72</td>
<td>0,39</td>
<td>0,44</td>
<td>-0,02</td>
<td>0,00</td>
<td>0,00</td>
<td>0,10</td>
<td>1,63</td>
</tr>
<tr>
<td style="text-align: center;"><strong>2</strong></td>
<td>0,00</td>
<td>1,68</td>
<td>0,18</td>
<td>0,24</td>
<td>-0,02</td>
<td>0,00</td>
<td>0,00</td>
<td>-0,23</td>
<td>1,84</td>
</tr>
<tr>
<td style="text-align: center;"><strong>3</strong></td>
<td>0,00</td>
<td>1,40</td>
<td>0,07</td>
<td>0,13</td>
<td>-0,02</td>
<td>0,00</td>
<td>0,00</td>
<td>0,02</td>
<td>1,61</td>
</tr>
<tr>
<td style="text-align: center;"><strong>4</strong></td>
<td>0,00</td>
<td>0,58</td>
<td>0,19</td>
<td>0,14</td>
<td>-0,03</td>
<td>0,00</td>
<td>0,00</td>
<td>0,47</td>
<td>1,35</td>
</tr>
<tr>
<td style="text-align: center;"><strong>5</strong></td>
<td>0,00</td>
<td>0,42</td>
<td>0,10</td>
<td>0,09</td>
<td>-0,04</td>
<td>0,00</td>
<td>0,00</td>
<td>0,62</td>
<td>1,20</td>
</tr>
<tr>
<td style="text-align: center;"><strong>6</strong></td>
<td>0,00</td>
<td>0,24</td>
<td>0,10</td>
<td>0,10</td>
<td>-0,04</td>
<td>0,00</td>
<td>0,00</td>
<td>0,74</td>
<td>1,14</td>
</tr>
<tr>
<td style="text-align: center;"><strong>7</strong></td>
<td>0,00</td>
<td>0,21</td>
<td>0,06</td>
<td>0,07</td>
<td>-0,04</td>
<td>0,00</td>
<td>0,00</td>
<td>0,79</td>
<td>1,08</td>
</tr>
<tr>
<td style="text-align: center;"><strong>8</strong></td>
<td>0,00</td>
<td>0,13</td>
<td>0,06</td>
<td>0,07</td>
<td>-0,04</td>
<td>0,00</td>
<td>0,00</td>
<td>0,84</td>
<td>1,05</td>
</tr>
<tr>
<td style="text-align: center;"><strong>9</strong></td>
<td>0,00</td>
<td>0,08</td>
<td>0,03</td>
<td>0,04</td>
<td>-0,04</td>
<td>0,00</td>
<td>0,00</td>
<td>0,92</td>
<td>1,03</td>
</tr>
<tr>
<td style="text-align: center;"><strong>10</strong></td>
<td>0,00</td>
<td>0,04</td>
<td>0,04</td>
<td>0,01</td>
<td>-0,03</td>
<td>0,00</td>
<td>0,00</td>
<td>0,72</td>
<td>0,79</td>
</tr>
<tr>
<td style="text-align: center;"><strong>Total</strong></td>
<td>0,00</td>
<td>0,20</td>
<td>0,10</td>
<td>0,05</td>
<td>0,00</td>
<td>0,00</td>
<td>0,00</td>
<td>0,80</td>
<td>1,16</td>
</tr>
</tbody>
</table>

Notes: shown as a percentage change in mean equivalised household
disposable income by income component and income decile group. Income
decile groups are based on equivalised household disposable income in
2024, using the modified OECD equivalence scale. Each policy system has
been applied to the same input data, deflating monetary parameters of
2024 policies by Eurostat’s Harmonized Index of Consumer Prices (HICP).

Source: Euromod

<span id="_Toc222163584" class="anchor"></span>**Figure A1.** Policy
effects in Denmark in 2024-2025

Source: Euromod

## Annex 3. Validation Tables

<span id="_Toc222163755" class="anchor"></span>**Table A3.1** Validation
Tables

[^1]: In the Danish welfare state model many will during sickness and
    leave have full wage income from the employer for up to 26 weeks due
    to the collective agreements. This is not modelled in Euromod.

[^2]: The increase in early retirement pension age is currently not
    taken into account in EUROMOD simulations, as a relatively small
    number of people were affected by the policy change in 2014 and
    2015. This is further due to a declining number of members of the
    early retirement scheme.

[^3]: The Ministry of Finance:
    https://fm.dk/nyheder/nyhedsarkiv/2020/marts/regeringen-og-alle-folketingets-partier-er-enige-om-omfattende-hjaelpepakke-til-dansk-oekonomi/accessed
    the 26<sup>th</sup> of March.
