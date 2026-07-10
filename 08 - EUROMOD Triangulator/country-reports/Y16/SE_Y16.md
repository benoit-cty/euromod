Cover

Contents

[Abstract [4](#_Toc222502455)](#_Toc222502455)

[Acknowledgements [5](#_Toc222502456)](#_Toc222502456)

[Authors [5](#_Toc222502457)](#_Toc222502457)

[1. Introduction [6](#introduction)](#introduction)

[1.1. Basic information about the tax-benefit system
[6](#basic-information-about-the-tax-benefit-system)](#basic-information-about-the-tax-benefit-system)

[1.1.1. Policy changes for 2022
[7](#policy-changes-for-2022)](#policy-changes-for-2022)

[1.1.2. Policy changes for 2023
[7](#policy-changes-for-2023)](#policy-changes-for-2023)

[1.1.3. Policy changes for 2024
[8](#policy-changes-for-2024)](#policy-changes-for-2024)

[1.1.4. Policy changes for 2025
[8](#policy-changes-for-2025)](#policy-changes-for-2025)

[1.2. Social Benefits [8](#social-benefits)](#social-benefits)

[1.3. Social contributions
[13](#social-contributions)](#social-contributions)

[1.4. Taxes [13](#taxes)](#taxes)

[1.4.1. Simulated taxes [13](#simulated-taxes)](#simulated-taxes)

[1.4.2. Non simulated taxes
[14](#non-simulated-taxes)](#non-simulated-taxes)

[2. Simulation of taxes and benefits in EUROMOD
[15](#simulation-of-taxes-and-benefits-in-euromod)](#simulation-of-taxes-and-benefits-in-euromod)

[2.1. Scope of simulation
[15](#scope-of-simulation)](#scope-of-simulation)

[2.2. Order of simulation and interdependencies
[16](#order-of-simulation-and-interdependencies)](#order-of-simulation-and-interdependencies)

[2.3. Policy extensions [18](#policy-extensions)](#policy-extensions)

[2.4. Social benefits [19](#social-benefits-1)](#social-benefits-1)

[2.4.1. Unemployment insurance benefit (bunct_s)
[19](#unemployment-insurance-benefit-bunct_s)](#unemployment-insurance-benefit-bunct_s)

[2.4.2. Child benefit (bch_s)
[24](#child-benefit-bch_s)](#child-benefit-bch_s)

[2.4.3. Housing allowance (bho_s)
[25](#housing-allowance-bho_s)](#housing-allowance-bho_s)

[2.4.4. Housing allowance for pensioners (bhope_s)
[29](#housing-allowance-for-pensioners-bhope_s)](#housing-allowance-for-pensioners-bhope_s)

[2.4.5. Social assistance (bsamt_s)
[33](#social-assistance-bsamt_s)](#social-assistance-bsamt_s)

[2.4.6. Parental benefit (bfapl_s)
[35](#parental-benefit-bfapl_s)](#parental-benefit-bfapl_s)

[2.4.7. Special days for the other parent (bpa_s)
[36](#special-days-for-the-other-parent-bpa_s)](#special-days-for-the-other-parent-bpa_s)

[2.5. Social contributions
[37](#social-contributions-1)](#social-contributions-1)

[2.5.1. Employee social contributions(tscee_s)
[37](#employee-social-contributionstscee_s)](#employee-social-contributionstscee_s)

[2.5.2. Employer social contributions (ils_sicer)
[38](#employer-social-contributions-ils_sicer)](#employer-social-contributions-ils_sicer)

[2.6. Personal income tax
[41](#personal-income-tax)](#personal-income-tax)

[2.6.1. Tax unit [41](#tax-unit)](#tax-unit)

[2.6.2. Exemptions [41](#exemptions)](#exemptions)

[2.6.3. Taxable income [41](#taxable-income)](#taxable-income)

[2.6.4. Tax allowances [41](#tax-allowances)](#tax-allowances)

[2.6.5. Tax base [43](#tax-base)](#tax-base)

[2.6.6. Tax schedule [44](#tax-schedule)](#tax-schedule)

[2.6.7. Tax credits [44](#tax-credits)](#tax-credits)

[2.7. Other taxes [49](#other-taxes)](#other-taxes)

[2.7.1. Tax on capital income
[49](#tax-on-capital-income)](#tax-on-capital-income)

[2.7.2. Tax on real estate
[49](#tax-on-real-estate)](#tax-on-real-estate)

[2.8. Consumption taxes [50](#consumption-taxes)](#consumption-taxes)

[2.8.1. VAT (il_tva) [51](#vat-il_tva)](#vat-il_tva)

[2.8.2. Ad-valorem excises (il_txv)
[51](#ad-valorem-excises-il_txv)](#ad-valorem-excises-il_txv)

[2.8.3. Tax credits [52](#tax-credits-1)](#tax-credits-1)

[2.9. Extraordinary measures
[54](#extraordinary-measures)](#extraordinary-measures)

[2.9.1. COVID-19: Wage Compensation scheme COVID-19 (yemcomp_se)
[54](#covid-19-wage-compensation-scheme-covid-19-yemcomp_se)](#covid-19-wage-compensation-scheme-covid-19-yemcomp_se)

[3. Data [55](#data)](#data)

[3.1. General description
[55](#general-description)](#general-description)

[3.2. Data adjustment [56](#data-adjustment)](#data-adjustment)

[3.3. Imputations and assumptions
[56](#imputations-and-assumptions)](#imputations-and-assumptions)

[3.3.1. Time period [56](#time-period)](#time-period)

[3.3.2. Gross incomes [56](#gross-incomes)](#gross-incomes)

[3.3.3. Disaggregation of harmonized variables
[56](#disaggregation-of-harmonized-variables)](#disaggregation-of-harmonized-variables)

[3.4. Updating [57](#updating)](#updating)

[3.5. Extended input data (with household expenditures for the
simulation of consumption taxes)
[57](#extended-input-data-with-household-expenditures-for-the-simulation-of-consumption-taxes)](#extended-input-data-with-household-expenditures-for-the-simulation-of-consumption-taxes)

[4. Validation [60](#validation)](#validation)

[4.1. Aggregate Validation
[60](#aggregate-validation)](#aggregate-validation)

[4.1.1. Components of disposable income
[60](#components-of-disposable-income)](#components-of-disposable-income)

[4.1.2. Validation of incomes inputted into the simulation
[61](#validation-of-incomes-inputted-into-the-simulation)](#validation-of-incomes-inputted-into-the-simulation)

[4.1.3. Validation of tax and benefit instruments
[61](#validation-of-tax-and-benefit-instruments)](#validation-of-tax-and-benefit-instruments)

[4.2. Income distribution
[62](#income-distribution)](#income-distribution)

[4.2.1. Income inequality [62](#income-inequality)](#income-inequality)

[4.2.2. Poverty rates [62](#poverty-rates)](#poverty-rates)

[4.3. Validation of minimum wage
[63](#validation-of-minimum-wage)](#validation-of-minimum-wage)

[4.4. Summary of “health warnings”
[63](#summary-of-health-warnings)](#summary-of-health-warnings)

[4.5. Avenues for future improvements of the Swedish model in EUROMOD
[64](#avenues-for-future-improvements-of-the-swedish-model-in-euromod)](#avenues-for-future-improvements-of-the-swedish-model-in-euromod)

[References [65](#references)](#references)

[Sources for tax-benefit descriptions/rules
[65](#sources-for-tax-benefit-descriptionsrules)](#sources-for-tax-benefit-descriptionsrules)

[List of abbreviations and definitions
[66](#list-of-abbreviations-and-definitions)](#list-of-abbreviations-and-definitions)

[List of figures [69](#list-of-figures)](#list-of-figures)

[List of tables [70](#list-of-tables)](#list-of-tables)

[List of Annexes [72](#list-of-annexes)](#list-of-annexes)

[Annex 1. Uprating Factors
[72](#annex-1.-uprating-factors)](#annex-1.-uprating-factors)

[Annex 2. Policy Effects in 2024-2025
[74](#annex-2.-policy-effects-in-2024-2025)](#annex-2.-policy-effects-in-2024-2025)

[Annex 3. Validation Tables
[76](#annex-3.-validation-tables)](#annex-3.-validation-tables)

<span id="_Toc222502455" class="anchor"></span>Abstract

The EUROMOD Country Reports have the double function of describing the
scope of the EUROMOD simulations, including the underlying assumptions,
and providing the validation of these simulations against official
statistics. The Country Report for Sweden is prepared by the Swedish
EUROMOD National Team each year, and made available by the JRC on time
for the EUROMOD stable release of the model at the beginning of each
year.

<span id="_Toc222502456" class="anchor"></span>Acknowledgements

The work was carried out jointly by the EUROMOD core development team,
based at the JRC in Seville, and the Swedish national team.

<span id="_Toc222502457" class="anchor"></span>Authors

The key contributors to this update were:

Jonathan Stråle as member of the national team for Sweden

Hannes Serruys, as JRC developer responsible for Sweden

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
Sweden. It provides an overview of the Swedish tax-benefit system in
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

## Basic information about the tax-benefit system 

The tax-benefit system is largely a unified, national system.[^1] Income
tax is paid to the state, municipalities and county councils. Tax rates
for the municipalities and county councils vary.

The tax system generally changes in January each year. Main benefit
changes happen at the same time, but may also be implemented in July.
Both taxes and benefits can at rare occasions be changed at any month
during the year.

State pension age is flexible and varies from 63-69 years of age. 65 is
the most common retirement age.

Minimum school leaving age is 16; dependent children are defined as aged
under 16 or under 20 and in full-time upper secondary education.

The income tax system is an individual system, with the spouses being
assessed independently.

The means-tested benefit system assesses entitlement according to
benefit unit income. The benefit unit is the nuclear family - the couple
(cohabiting or married) or single adult plus any dependent children.

Social contributions and state benefits and pensions are usually
assessed and delivered on a monthly basis. Amounts are referred to in
monthly terms. The exception is income tax, where liability is based on
annual income and allowances and thresholds are referred to in annual
terms. Incomes related to means-tested systems are often defined in
annual terms.

Income tax withholdings are collected on a cumulative basis, i.e., the
system tries to ensure withholding the exact amount due in the financial
year. Most people however have to fill in an income tax return, which
however can be very simple when the amounts are known by the tax
authority. Wages and interests are normally pre-printed on the income
tax return.

Consumption taxes consist of (1) VAT with three rates (one standard of
25 percent, and two reduced, 12 and 6 percent respectively), (2)
harmonised excises on tobacco, alcohol, and energy.

### Policy changes for 2022

Besides general changes of already existing policies (i.e., increase or
decrease of benefit amounts, changed threshold amounts, and changes of
allocation/eligibility criteria), the only major change of whole
policies in 2022 was the abolishment of COVID-19 related benefits.
Following COVID-19 policies were changed:

**Constants** (ConstDef_se): The constant for COVID-19 wage compensation
schemes and policies (3.7) is switched off.

**Wage Compensation Scheme COVID-19** (yemcomp_se): The policy is
switched off as a whole.

**Employer Insurance Contribution** (tscer_se): All part of the
insurance that were changed due to COVID-19 are switched off.

**Self-employed Social Insurance Contribution** (tscse_se): All part of
the insurance that were changed due to COVID-19 are switched off.

### Policy changes for 2023

Besides general changes of already existing policies (i.e., increase or
decrease of benefit amounts, changed threshold amounts, and changes of
allocation/eligibility criteria), the only major change of whole
policies in 2023 stems from a change in the age threshold of the
earliest pensionable age, which in 2023 increased from 62 to 63. Since
the age thresholds in several benefit and tax systems are connected to
this threshold, a lot of age thresholds have been updated this year.
This includes the age threshold for disability pension, housing
allowance for seniors, maintenance support for elderly, old age pension,
guarantee pension, social contributions, basic allowance, the earned
income tax credit and the tax credit for persons with disability
pension.

### Policy changes for 2024 

There are no major policy changes in 2024, only changes of already
existing policies (i.e., increase or decrease of benefit amounts,
changed threshold amounts, and changes of allocation/eligibility
criteria).

### Policy changes for 2025 

Besides general changes of already existing (i.e., increase or decrease
of benefit amounts, changed threshold amounts, and changes of
allocation/eligibility criteria) in 2025, one larger change is that the
eligibility conditions and amounts of the unemployment benefit changed
as of October 1st.

The policy parameters saved as constants in the model and their values
for the most recent year are available at
[<u>https://euromod-web.jrc.ec.europa.eu/resources/parameters</u>](https://euromod-web.jrc.ec.europa.eu/resources/parameters). 

Additionally, the generosity of the tax credit has increased with the
aim of lowering the tax-wedge.

## Social Benefits

**1.2.1 Simulated Social Benefits.**

**Child benefit (Barnbidrag)** is received for each child until 16
years. Child 2, 3, etc. gets extra benefit. If the child is in primary
school, the child benefit is prolonged. If the child is in secondary
school, he/she can get financial help during 10 months/ a year until 20
years of age with the same amount as the child benefit. The benefit is
not taxable.

**Housing allowance (Bostadsbidrag**) can be given to families with
children and to single and married/cohabiting families where all family
members are 18-29 years old without children. The maximum allowance
depends on the number of children and the housing cost (within certain
limits). If the size of the dwelling exceeds a certain area, the
accepted housing cost is proportionally reduced to match the maximum
accepted area.

**Housing allowance for pensioners (Bostadstillägg, BT**) can be given
to old-age pensioners and persons with disability pension. It is
considered to be a part of the pension system. From the age of 66 you
can get age allowance and for younger persons you can get disability
allowance. The benefit is not taxable.

**Social assistance (Ekonomiskt bistånd)** is the ultimate and last part
of the social safety net. It can be paid out if the family has temporary
financial problems, or if the disposable income/month is too low. Two
important conditions to get social assistance are that the family
doesn’t have any wealth and is willing to take a job if this is offered.
The income limits for getting the benefit are based on the normative
costs for a basket of commodities needed to get a reasonable standard of
living. The income limits depend on the age of children, single or
cohabitant couple, and the number of individuals in the family. Housing
costs, and costs for health, dentist, furniture, local commuting,
insurance and child care costs are not included in the normative costs.
Actual costs are used instead. The benefit is not taxable.

**Maintenance support for elderly (Äldreförsörjningsstöd**) can be given
to old individuals (\>= 66 years) if their disposable income is below
the limits for reasonable level of living. Normative rules are used for
calculating the income. This benefit is valid for e.g. immigrants who
have not earned Swedish pension rights. The benefit is not taxable. The
rules are similar to Social assistance and hence the Maintenance support
will be simulated as part of the Social assistance.

**Unemployment insurance benefit (Arbetslöshetsförsäkring)** consists of
a mandatory part (basic insurance) and a voluntary income related
insurance. Membership of an unemployment insurance fund is voluntary.
Eligibility for unemployment insurance benefits requires membership for
12 months prior to the first day of unemployment. However, if the person
is not enrolled in the unemployment insurance fund but has worked for at
least 60 hours per month during at least 6 months in the past 12 months,
or at least a total of 420 hours for six consecutive months, with at
least 40 hours per month, in the past 12 months. Then the person is
entitled to between 5610 - 11,220 SEK per month.

From October 1st 2025, the basic insurance is simplified, focusing more
on earned income rather than amount of worked hours. Instead of a lower
threshold for work hours you need to have earned at least 120 000 SEK in
the past 12 months before unemployment and have a total of at least 4
(non-consecutive) months with an income above 11 000 SEK, or have at
least 4 consecutive months with an income above 11 000 SEK per month.
The above requirements on work hours to qualify for the benefit for
shorter memberships than a year is also abolished, but you get fewer
benefit days if you have been a member for less than 11 months. The
benefit is also lowered more sharply after the first 100 days as
compared to the previous insurance. The benefit is taxable.

**Parental leave insurance (Föräldraförsäkringen)** consists of parental
benefit (simulated for some years and switched off in the baseline),
temporary parental benefit (not simulated), pregnancy benefit (not
simulated), and special days for the other parent (simulated for some
years and switched off in the baseline). All parts are taxable benefits.

**Parental benefit** (**Föräldrapenning**) is the biggest part of the
parental leave insurance and which all parents are eligible to. For each
birth the parents receive 480 days with parental benefit. Of these days
the benefit for 390 days is based on the parent’s income and 90 days are
on a basic level. The days can be used from 60 days before the expected
birth. If the child was born in 2013 or earlier, the days can be used
until the day when the child is 8 years old, or has passed the first
year at school. If the child was born in 2014 or later, the days can be
used until the day when the child is 12 years old, or has passed the
fifth year at school, but 80 percent of the days must be used before the
child becomes four years old. Both parents have the right to half of the
days, but it is possible to transfer days to the other parent. However,
if the child is born in 2014 or 2015, 60 of the days on basic level
cannot be transferred, and if the child is born after 2015 none of the
days on the basic level (90 days) can be transferred to the other
parent. It is possible to get the benefit full time or part time. If the
parents get twins they receive 180 days extra, 90 days with benefit
based on their income and 90 days according to the basic level.

**Special days for the other parent (10-dagar vid barns födelse).** The
parent who is not pregnant has the right to temporary parental benefit
for 10 days when the baby is born or adopted. The days have to be used
within 60 days after the child’s arrival at home. The benefit rules are
the same as for the temporary parental benefit.

**1.2.2 Non-simulated social benefits**

**Sickness benefit (Sjukpenning)** Sickness insurance provides
compensation in the event of sickness that reduces work capacity by at
least one-quarter. Sickness benefit is based on the sickness benefit
qualifying annual income (SGI). In principle, the income is supposed to
correspond to the annual income before tax, non-monetary taxable
benefits should not be included. The SGI is determined by the Social
Insurance Agency. Sick pay is paid by the employer for the first 14 days
period and thereafter the Social Insurance Agency pays sickness benefit.
No compensation is paid on the first day (the qualifying day). If an
individual is unemployed the maximum benefit is the same as the
unemployment insurance. The benefit is taxable.

As of January 1 2020, the government gives a compensation with a maximum
daily amount of 1027 SEK. This was increased to 1116 SEK as of January 1
2023, to 1218 SEK on January 1 2024 and to 1250 SEK on January 1 2025.

**Temporary parental benefit (Vård av barn, VAB).** For children under
the age of 12 (and in certain cases under 16) temporary parental benefit
can be paid. The benefit can be paid for 120 working days per year, when
a parent needs to stay away from work due to a sick child. These days
can be divided between the caretakers of the child, and not exclusively
by the parents of the child. Parents of a seriously sick child can get
an unlimited number of days until the age of 18. It is possible to get
the benefit full time or part time.

**Pregnancy benefit (Graviditetspenning).** If the work conditions make
it impossible to work, a pregnant woman can apply for pregnancy benefit
during a period of maximum 60 days. The benefit rules are the same as
for the sickness benefit.

**Special housing allowance for pensioners** **(SBT, Särskilt
Bostadstillägg)** can be paid out if the disposable income is low and
the housing cost is high. The amounts vary with age, disability and
marital status (single/married). The benefit is not taxable.

**Old age pension (Ålderspensionen).** The mandatory parts of the
age-pension are under the process of changing from the old system (born
1937 or earlier) to the new system which started in 2003. Pensioners
born in 1938 or later are gradually subject to a new system. From age
class 1954 the new system is fully implemented. For age classes
1938-1953 the benefits are partly from the old system and partly from
the new system. If born in 1953, 1/20 comes from the old system and if
born in 1938 16/20 comes from the old system.

The old system consists of a supplementary pension and a guarantee
pension. The supplementary pension is based on the average of the 15
years with the highest work income. Only incomes up to 7.5 income base
amounts/year (7.5\*80 600 SEK in 2025) are included. The supplementary
pension is indexed with the average salary minus 1.6 percentage points.

If the supplementary pension is low, guarantee pension can be achieved.
For a single pensioner the maximum guarantee is 2.17 price basic
amounts/year and is reduced with increased supplementary pension. For a
married pensioner the maximum is 1.935 price basic amounts.

In the new system income related pension can be earned during the whole
lifetime. 18.5% of the earnings finance the earned pension rights (up to
7.5 income base amounts). 16% are going to public funds, which you
cannot handle yourself. 2.5% goes to private funds, where you can decide
how it should be composed. Over time the pension funds rise with the
average wage in the whole economy. The earliest pensionable age is 63
years, but there is no last pension age, even if traditionally many
retire at the age of 65. You also have legal right to work until the end
of the month of your 69th birthday. At the age for retirement the
pension is determined by the total pension rights divided with the
expected number of remaining years to live. After retirement the pension
is indexed with the average salary minus 1.6 percentage points.

If the related income is too low, guarantee pension can be achieved from
the age of 66. The maximum value is 2.13 price base amounts for
unmarried and 1.90 for married people.

Both in the old and new system, not only earnings but also insurance
benefits like sickness, unemployment and parental leave benefits give
pension rights.

In the new system you also get pension rights when studying, doing
military (duty) service or taking care of small children (up to 4 years
of age).

In addition to the mandatory pension most employees have occupational
pensions, with different rules for different sectors of the labour
market. Typically, the employers pay a fee between about 3,5% and 4.5%
of the salary. For all contracting parties, except private and
cooperative workers, the employers also give an extra compensation for
income shares above the income ceiling for the mandatory pensions.

All pensions are taxable. It is possible to retire full-time or
part-time.

**Disability pension (Sjukersättning/aktivitetsersättning)**. If
disabled or so sick or so injured, that you cannot work any longer, you
can get disability pension in the form of *sjukersättning* (if aged
30-65 ) or *aktivitetsersättning* (if aged 19- 29). The benefit is
taxable.

**Disability pension (Sjukersättning (aged 30-64 during 2016 and aged
19-64 from 2017, 19-65 from 2023).** The benefit can be income related
or a guarantee benefit. The income related benefit is 64.7 percent of an
expected income up to a certain level, as if the ability to work had not
decreased. The assumed forecasted income is based on the average of the
3 highest annual incomes within a number of years before the person
became sick. The number of years depends on the age of the person. The
guarantee benefit is age-dependent, ranging from 2.48 price base amounts
for those under 21 to 2.78 price base amounts for those aged 30 or above
in 2025.

**Disability pension (Aktivitetsersättning (aged 19-29 years)).** They
can only get time-limited benefit. The assumed income can be based on
the 2 highest annual incomes if that gives a higher assumed income. The
income related benefit is the same as for older persons but the
guarantee benefit is 2.48-2.78 price base amounts (2025) depending on
the age of the person.

**Introductory compensation to refugees and certain other foreign
nationals** (Etablerings-ersättning) is a compensation that a newly
arrived refugee can receive if an establishment plan is created. The
compensation is paid for a maximum of five days per week if the refugee
has an establishment plan. The compensation is 231 SEK per day during
the preparation of the plan, and 308 SEK per day when participating in
activities that are a part of the plan.

When participating in activities part time, the compensation is reduced
to the same extent.

**Supplementary introduction benefit** (Etableringstillägg) is a
supplementary benefit that a refugee that is already receiving
*introductory compensation to refugees and certain other foreign
nationals* can apply for if he or she has children living in the
household. The supplementary benefit is paid monthly, 800 SEK per child
that hasn’t turned 11 years old yet and 1500 SEK per child that has
turned 11 but is not yet 20 years old. The supplementary benefit is paid
for a maximum of three children. If there are more than three children
in the household the benefit is paid for the three oldest children.

If a refugee receives *maintenance support* for three children, then the
benefit is only paid for the two oldest children. If a refugee receives
*maintenance support* for four to five children, then the benefit is
only paid for the oldest child. If a refugee receives *maintenance
support* for six or more children, then the benefit is not paid at all.

**Housing allowance to refugees and certain other foreign nationals**
(Bostadsersättning) is an allowance that a refugee that is entitled to
*supplementary introduction benefit* and is single and without children
registered as living in the household. If the refugee has an
establishment plan according to law (2010:197), housing allowance can be
paid for the part of the living cost per month that is between 1800 SEK
and 5700 SEK. Depending on what ratio the establishment plan is
(full-time, part-time etc.) the housing allowance is paid in the same
extent.

**Activity and development grant** (Aktivitetsstöd och
utvecklingsersättning). If an individual is unemployed and participating
in a policy program one can receive an activity or a development grant.
If the individual is over 25 years old or meet the conditions for
unemployment benefits the individual get an activity grant. The grant is
at the minimum level of 510 SEK per day (365 after October 1st 2025),
and at the most 1200 SEK (1236 after October 1st), if the policy program
is full time. The number of days receiving the grant is contracted from
the days with unemployment benefit.

If the individual does not meet the requirements for unemployment
benefits and is at least 25 years old, the individual receives 223 SEK
per day.

If the individual is not yet 25 years old and doesn’t meet the
conditions for unemployment benefits the individual gets a development
grant. The grant is 205 SEK per day if the individual finished high
school.

If the individual did not finish high school the grant is 57 SEK per day
until the individual turns 20 years old, after that the grant is 183 SEK
per day. The development grant is non-taxable.

**Not strictly benefits**

**Maintenance support (Underhållsstöd).** When a child lives with only
one parent, the other parent must pay child support (underhållsbidrag).
If child support is not received, the child may be entitled to
maintenance support. This is a benefit for children whose parents do not
live together. The size of the maintenance support is depending of the
age of the child. It is at most SEK 1673-2223 (2023) per child and
month, and is paid to the parent with whom the child lives

**Childcare allowance (Omvårdnadsbidrag och merkostnadsersättning)**
Parents taking care of a sick child or a child with a disability can
obtain childcare allowance. The child must need special supervision and
care for at least six months. The childcare allowance can also be
obtained by families having large additional expenses due to the child’s
disability or illness. The childcare allowance can be obtained from the
time of the child’s birth until the month of June in the year the child
attains the age of 19.

**Student aid (studiemedel)** Students attending a college or university
can apply for student aid. Student aid includes both grants and loans.
The student can choose between applying only for the grant or applying
for both grant and loan. The loan has to be paid back during a number of
years after the studies are finished. The amount of student aid received
depends on the number of weeks of studying and if full-time or part-time
studies.

## Social contributions

Social contributions refer to health insurance, parental insurance,
occupational injuries, old age pension, survivors’ pension, labour
market, general wage fee and a special wage tax (for persons older than
65 years).

Employees pay a general old age pension contribution, approximately 7.0%
of the gross salary.

The employer pays social contributions as a proportion of the gross
salary. The total contribution is 31.42% of the gross salary.

Farmers and self-employed also pay social contributions but as
proportion of the net income. The proportion varies with age. Persons
below 66 years of age pay all social contributions, summing up at
28.97%. Persons aged 66 years or older age either pay special wage tax
for elderly (6.15%) if born 1937 or earlier or special wage tax for
elderly (6.15%) plus old age pensions contributions (10.21%). The
special wage tax for elderly was only paid up until 30 June 2019, after
which it was abolished.

For the period of 1 March 30 to 1 June 2020 the social security
contributions was reduced. For employers, the proportion of the gross
salary to be paid was reduced from 31.42% to 10.21% (thus only paying
only the old-age pension contribution). The reduction was valid for up
to 30 employees and for salaries up to SEK 25 000. For further employees
and for salaries above this amount no reduction was available. For
farmers and self-employed the proportion of net income to be paid was
reduced from 28.97% to 10.21% (thus only paying the old-age pension
contribution). The reduction was valid for net income up to SEK 100 000.

## Taxes

The Swedish system for direct taxes includes income taxes, capital tax
and tax on real estate. The sum of taxes cannot be negative.

**Indirect taxes** The VAT is 25 % as the normal level, but lower for
some goods (i.e. food at 12 %, books and newspapers at 6 %).

There are taxes on alcohol, tobacco, traffic, and a number of energy
related taxes.

### Simulated taxes

**Income tax (Inkomstskatt**) is assessed individually. Earnings,
insurance benefits like sickness benefit, pensions etc. are included in
the tax base. Costs for work to a limited amount and private premiums to
a limited amount for retirement are deducted from the tax base. The
result is called assessed income. From the assessed income the basic
allowance is deducted according to a rather complex formula. The result
is called taxable income, on which the tax schedule is applied. All
amounts are expressed in annual terms.

The national income tax is only paid on taxable incomes above a certain
amount (20 431 SEK for 2022, 22 208 SEK 2023, 24 238 SEK 2024 and 24 872
SEK in 2025, annually) and there are two tax rates. Local taxes are
assessed at municipality and county level. All municipalities (about
300) and county councils (about 25) have taxation rights. The tax is
proportional to the taxable income.

Everybody pays a funeral fee which is used for the care of cemeteries
and premises for funeral ceremonies. It is not connected to individual’s
funerals.

**Capital tax (Kapitalskatt**) is a national individual tax. The tax
base consists of capital income and is separate from the national income
tax. The general tax rate is 30%, but special rules in specific parts
lead to different (lower) tax rates than the general one. If the taxable
income is negative this leads to tax reduction on the final tax (sum of
local tax and national tax). It is especially common for loans on owned
houses.

The tax base consists of interests, cost of interest, interests on
bonds, shares, funds etc., capital gains and capital losses on shares,
funds, real estate.

**Consumption taxes**

The standard VAT rate is 25%. A lower rate of 12% exists for food and
repair of clothes and an even lower rate of 6% exists for public
transport, culture (e.g. museums, theatres, cinemas, books and
newspapers) and basic needs goods and services (rent, medical and dental
services, pharmaceuticals and education). Insurance and financial
services also have the lowest VAT rate of 6 %.

Excise duties are levied on several products, such as tobacco, various
alcoholic beverages, packaging. Tobacco is a EU-harmonized tax. All
Swedish excises are ad-quantum, with the exception of the excise on
cigarettes (which is a combination of an ad-quantum and ad-valorem
excise).

### Non simulated taxes

**Tax on real estate.** As from 2008 government property tax on
dwellings was abolished and replaced by a municipal property charge. Tax
on real estate is included in the SILC data (EUROMOD variable: tpr).

# Simulation of taxes and benefits in EUROMOD

## Scope of simulation

Table 2.1 and Table 2.2 show respectively the benefits and taxes and
contributions which are included (i.e. not simulated but included using
the value recorded in the survey) or simulated in EUROMOD.

<span id="_Toc222502814" class="anchor"></span>**Table 2.1** Simulation
of benefits in EUROMOD

<table style="width:58%;">
<colgroup>
<col style="width: 13%" />
<col style="width: 8%" />
<col style="width: 3%" />
<col style="width: 3%" />
<col style="width: 3%" />
<col style="width: 3%" />
<col style="width: 21%" />
</colgroup>
<thead>
<tr>
<th rowspan="2"></th>
<th rowspan="2"><strong>Variable name(s)</strong></th>
<th colspan="4"><strong>Treatment in EUROMOD</strong></th>
<th style="text-align: center;"><strong>Why not fully
simulated?</strong></th>
</tr>
<tr>
<th><strong>2022</strong></th>
<th><strong>2023</strong></th>
<th><strong>2024</strong></th>
<th><strong>2025</strong></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>Unemployment benefit</td>
<td>bunct</td>
<td>PS</td>
<td>PS</td>
<td>PS</td>
<td>PS</td>
<td>Unemployment benefit is not simulated in the baseline year and is
set to toggle as it is not possible to define contribution record and
past earnings.</td>
</tr>
<tr>
<td>Unemployment benefit</td>
<td>bunnc</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td rowspan="7">Lack of info in input data.</td>
</tr>
<tr>
<td>Parents' allowance</td>
<td>bpl</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
</tr>
<tr>
<td>Sickness benefit</td>
<td>bhl</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
</tr>
<tr>
<td>Education related allowance</td>
<td>bed</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
</tr>
<tr>
<td>Disability benefits</td>
<td>pdi</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
</tr>
<tr>
<td>Old age pensions</td>
<td>poa</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
</tr>
<tr>
<td>Survivors’ pensions</td>
<td>psu</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
</tr>
<tr>
<td>Child benefit</td>
<td>bch_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>Housing allowance</td>
<td>bho_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>Housing allowance for pensioners</td>
<td>bhope_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>Social Assistance</td>
<td>bsamt_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>Social Assistance</td>
<td>bsanm_s</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>Lack of info in input data.</td>
</tr>
<tr>
<td>Short-term work allowance (paid by state)</td>
<td>bwkmcee_s</td>
<td></td>
<td>S</td>
<td>S</td>
<td></td>
<td></td>
</tr>
<tr>
<td>Short-term work allowance (paid by firms)</td>
<td>yemmc_s</td>
<td></td>
<td>S</td>
<td>S</td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

Notes: “-”: policy did not exist in that year; “E”: *excluded* from the
model as it is neither included in the micro-data nor simulated; “I”:
*included* in the micro-data but not simulated; “PS” *partially
simulated* as some of its relevant rules are not simulated; “S”
*simulated* although some minor or very specific rules may not be
simulated.

Source: Own elaboration.

<span id="_Toc222502815" class="anchor"></span>**Table 2.2** Simulation
of taxes and social contributions in EUROMOD

<table style="width:59%;">
<colgroup>
<col style="width: 15%" />
<col style="width: 7%" />
<col style="width: 3%" />
<col style="width: 3%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 15%" />
</colgroup>
<thead>
<tr>
<th rowspan="2"></th>
<th rowspan="2"><strong>Variable name(s)</strong></th>
<th colspan="5" style="text-align: center;"><strong>Treatment in
EUROMOD</strong></th>
<th style="text-align: center;"><strong>Why not fully
simulated?</strong></th>
</tr>
<tr>
<th><strong>2021</strong></th>
<th><strong>2022</strong></th>
<th><strong>2023</strong></th>
<th><strong>2024</strong></th>
<th><strong>2025</strong></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>Employee social contributions</td>
<td>tscee_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>Employer social contributions</td>
<td>ils_sicer</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>Self-employed social contributions</td>
<td>ils_sicse</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>Personal income tax</td>
<td>tin_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>Tax on capital income</td>
<td>tinkt_s</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td></td>
</tr>
<tr>
<td>Tax on real estate</td>
<td>tpr</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>I</td>
<td>Lack of info in input data. This includes repayment of student
loan</td>
</tr>
<tr>
<td>VAT</td>
<td>-</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>Calculations based on extended input files with consumption
expenditures from HBS</td>
</tr>
<tr>
<td>Excise duties</td>
<td>-</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>S</td>
<td>Calculations based on extended input files with consumption
expenditures from HBS</td>
</tr>
</tbody>
</table>

Notes: “-” policy did not exist in that year; “E” policy is *excluded*
from the model’s scope as it is neither included in the microdata nor
simulated; “PS” policy is *partially simulated* as some of its relevant
rules are not simulated; “S” policy is *simulated* although some minor
or very specific rules may not be simulated

Source: Own elaboration.

## Order of simulation and interdependencies

Social contributions are simulated first, in order to allow the employee
social insurance contributions to be subtracted from the income tax.
Then, the income tax is simulated in all its components followed by the
tax on capital income. The simulation of the non-taxable benefits
follow: child benefit, housing allowance and housing allowance for
pensioners. The social assistance is the last benefit simulated because
it includes all previous simulated benefits and taxes in its means-test.

In the simulation of the tax benefit system, the price base amount is
used repeatedly and in one case also the income base amount. They are
defined as “constants” in the policy sheet ConstDef. The price base
amount (XBASM) is an amount established by the government for one year
at a time and adjusted annually. It is used for calculations of
pensions, sickness benefit and allowances for example. The income base
amount (XBASMI) is linked to the “income index” and was introduced in
connection with the pension reform. The income index measures the
average income change in Sweden.

<span id="_Toc222502816" class="anchor"></span>**Table 2.3** EUROMOD
Spine: order of simulation

| **Policy** | **SE_2021** | **SE_2022** | **SE_2023** | **SE_2024** | **SE_2025** | **Comment** |
|----|----|----|----|----|----|----|
| setdefault_se | on | on | on | on | on | DEF: SET DEFAULT |
| uprate_se | on | on | on | on | on | DEF: UPRATING FACTORS |
| ConstDef_se | on | on | on | on | on | DEF: CONSTANTS |
| ilsdef_se | on | on | on | on | on | DEF: INCOME CONCEPTS (standardized) |
| ilsUDBdef_se | on | on | on | on | on | DEF: INCOME CONCEPTS (UDB) |
| ildef_se | on | on | on | on | on | DEF: INCOME CONCEPTS (non-standardized) |
| random_se | on | on | on | on | on | DEF: Random assignment |
| transLMA_se | off | off | off | off | off | DEF: Simulation of labour market transitions |
| tudef_se | on | on | on | on | on | DEF: ASSESSMENT UNITS |
| yem_se | off | off | off | off | off | DEF: minimum wage |
| neg_se | on | on | on | on | on | DEF: recode negative self-employment income to zero |
| yemcomp_se | on | on | off | off | off | BEN: wage compensation scheme COVID-19 |
| bunct_se | off | off | off | off | off | BEN: Unemployment benefit |
| bfapl_se | switch | switch | switch | switch | switch | BEN: Parental leave benefit |
| bpa_se | switch | switch | switch | switch | switch | BEN: Paternity leave (10 days) |
| tscee_se | on | on | on | on | on | SIC: Employee Social Insurance contribution |
| tscer_se | on | on | on | on | on | SIC: Employer Social Insurance contribution |
| tscse_se | on | on | on | on | on | SIC: Self-employed Social Insurance contribution |
| tin_se | on | on | on | on | on | TAX: Personal Income tax |
| tinkt_se | on | on | on | on | on | TAX: Tax on Capital Income |
| bch_se | on | on | on | on | on | BEN: Child benefit |
| bho_se | on | on | on | on | on | BEN: Housing allowance |
| bhope_se | on | on | on | on | on | BEN: Housing allowance for pensioners |
| bsamt_se | on | on | on | on | on | BEN: Social Assistance |
| output_std_se | on | on | on | on | on | DEF: STANDARD OUTPUT INDIVIDUAL LEVEL |
| output_std_hh_se | off | off | off | off | off | DEF: STANDARD OUTPUT HOUSEHOLD LEVEL |
| tco_se | on | on | on | on | on | TAX: Commodities (consumption taxes) |

Source: Own elaboration.

The last policy included in the spine is tco_se (consumption taxes). It
is placed at the very end because consumption tax liabilities (VAT and
excises) depend on household consumption expenditures, and these are
estimated by the model based on the income shares (xs\_\* variables
included in the input data) and simulated disposable income (ils_dispy).
This is why before running any simulation of consumption tax policy it
is required to activate all the other policies intervening in the
simulation of disposable income.

<span id="_Toc222502817" class="anchor"></span>**Table 2.4** Annual Base
amounts

|        |  2022  |  2023  |  2024  |  2025  |
|--------|:------:|:------:|:------:|:------:|
| XBASM  | 48,300 | 52,500 | 57,300 | 58,800 |
| XBASMI | 71,000 | 74,300 | 76,200 | 80,600 |

Notes. XBASM: price base amount. XBASMI: income base amount

Source: The Swedish Government
(<https://www.regeringen.se/pressmeddelanden/2024/09/prisbasbelopp-for-2025-faststallt/>
and
<https://www.regeringen.se/artiklar/2024/11/inkomstbasbelopp-och-inkomstindex-for-ar-2025-faststallt/>)

## Policy extensions

There are seven extensions defined in the Swedish model: [^2]

**Parental Benefits Extension (PBE)** – to choose between observed
(extension *off*) and simulated (extension *on*) values of maternity
benefit and parental benefit

**Benefit Calibration Adjustments (BCA)-** allowing the user to
calibrate the receipt of benefits to match the simulated total
expenditure of a benefit to real expenditure from external statistics.
The extension is implemented for the simulation of means-tested social
assistance (*bsamt_se*). The default for the baseline is off. When the
extension is on, a subset of eligible of observations is selected
randomly as beneficiaries so that the real expenditure is reached,
removing the benefit from the rest of the eligible observations; when
off, all eligible observations are kept as beneficiaries. This extension
shares most of its functions with the BTA extension; as a general rule,
only one of the extensions should be on, but if both are, the lowest
rate between the take-up rate and the calibration rate will be applied.
More details on the specific implementation of BCA and BTA extensions
are provided in the subsections describing the corresponding benefit.

**Benefit Take-up Adjustments (BTA)** - allowing the user to apply
non-take-up corrections.  The extension is  used  for  the  simulation 
of  means tested social assistance benefits (*bsamt_se*). The default
for the baseline is off. When the extension is on, a share of (weighted)
eligible observations equal to the take-up rate is selected randomly as
beneficiaries, removing the benefit from the rest of the eligible
observations; when off, all eligible observations are kept as
beneficiaries. This extension shares most of its functions with the BCA
extension; as a general rule, only one of the extensions should be on,
but if both are, the lowest rate between the take-up rate and the
calibration rate will be applied. More details on the specific
implementation of BCA and BTA extensions are provided in the subsections
describing the corresponding benefit. 

**Minimum Wage Adjustment (MWA)** – This extension rescales the income
for incomes that fall below the minimum wage set for that given year.
Note that there is no minimum wage set and that hence the intended user
should choose a value for the constant \$MinWage in the spine.

**HHoT – Unemployment extension (HHoT_un) -** this extension improves
the simulation accuracy of the unemployment insurance benefit when
EUROMOD is run with hypothetical data. For instance, in most countries
the legislation of this benefit requires information on variables such
as individuals’ employment history, which are not available in SILC; we
can define these variables in HHoT and use them to simulate the policy’s
rules more precisely when running the model with hypothetical data. This
extension is set to on when the model is used with HHoT data.

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

## Social benefits

### Unemployment insurance benefit (bunct_s)

#### Definitions 

Unemployment insurance benefit consists of a mandatory part (*basic
insurance*) and a *voluntary income related insurance*. Membership to an
unemployment insurance (UI) fund is voluntary. The daily allowance, paid
five days a week, is based on the income received the 12 months before
the unemployment (the amount received is equal to the basic amount or
80% of previous gross earnings with a maximum limit).

#### Eligibility conditions

Up until October 1st 2025, eligibility for unemployment insurance
benefits requires membership to an unemployment insurance fund for 12
months prior to the first day of unemployment and having worked for at
least 60 hours per month during at least 6 months during the last 12
months, or at least 420 hours in 6 consecutive months with at least 40
hours each month.

From October 1st 2025, shorter membership is required to qualify, but
the length of the membership determines the maximum duration of the
benefit. For membership between 4-7 months, you will get 100 benefit
days. For membership between 8-10 months, you get 200 membership days
and for 11 months or longer you get 300 days (same the maximum benefit
days before the change). You must also have earned at least 120 000 SEK
in the last 12 months, 4 of which with a monthly income of at least
11 000 SEK, (alternatively, at least 4 consecutive months with an income
of at least 11 000 SEK), to qualify.

Up until October 1st 2025, if the person is not enrolled in the
unemployment insurance fund, but has worked for at least 60 hours per
month during at least 6 of the past 12 months. Or if the person has
worked at least 420 hours during a cohesive period of 6 months and
worked at least 40 hours during each one of these months, then is
entitled to receive between 255 and 510 SEK per day. From October 1st
2025, if the person is not enrolled in the unemployment insurance fund
they get between 255 and 773 SEK per day, if they have earned at least
120 000 SEK in the last 12 months, 4 of which with a monthly income of
at least 11 000 SEK, (alternatively, at least 4 consecutive months with
an income of at least 11 000 SEK).

It is possible to get the benefit full-time or part-time. From July 1st
2018 no compensation is paid for the first six days (the qualifying
days), but as a COVID-measure this was lowered to 2 days in 2020, and
this change was made permanent from January 1st 2024. The self-employed
are also eligible to the benefit in case their business closes. The
benefit is taxable.

In the recent past, most of the Swedes were members of an unemployment
insurance fund (in the simulation, we will assume that such an
eligibility condition is satisfied).

#### Income test

The daily allowance, paid five days a week, is based on the income
received the 12 months before unemployment. This is the case for all
years between 2021-2025.

#### Benefit amount 

The benefit is calculated according to the rules summarized in the table
below. Until October in 2025, 150 extra days for unemployed persons with
children was given. Starting October 2025 these extra days have however
been removed.

<span id="_Toc222502818" class="anchor"></span>**Table 2.5**
Unemployment benefits 2021-September 30th 2025

<table style="width:54%;">
<colgroup>
<col style="width: 16%" />
<col style="width: 8%" />
<col style="width: 15%" />
<col style="width: 13%" />
</colgroup>
<thead>
<tr>
<th><strong>Labour days</strong></th>
<th style="text-align: center;"><p><strong>Basic amount</strong></p>
<p><strong>SEK/day</strong></p></th>
<th style="text-align: center;"><p><strong>Compensation</strong></p>
<p><strong>(as a share of previous income)</strong></p></th>
<th style="text-align: center;"><p><strong>Upper limit</strong></p>
<p><strong>SEK/day</strong></p></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="3"><strong>2021 – 2025 (parent with child)</strong></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td>1-100</td>
<td style="text-align: center;">510</td>
<td style="text-align: center;">0.8</td>
<td style="text-align: center;">1200</td>
</tr>
<tr>
<td>101-200</td>
<td style="text-align: center;">510</td>
<td style="text-align: center;">0.8</td>
<td style="text-align: center;">1000</td>
</tr>
<tr>
<td>201-450</td>
<td style="text-align: center;">510</td>
<td style="text-align: center;">0.7</td>
<td style="text-align: center;">1000</td>
</tr>
<tr>
<td>450*-</td>
<td style="text-align: center;">510</td>
<td style="text-align: center;">0.65</td>
<td style="text-align: center;">1000</td>
</tr>
<tr>
<td><strong>2021 – 2025 (other)</strong></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td>1-100</td>
<td style="text-align: center;">510</td>
<td style="text-align: center;">0.8</td>
<td style="text-align: center;">1200</td>
</tr>
<tr>
<td>101-200</td>
<td style="text-align: center;">510</td>
<td style="text-align: center;">0.8</td>
<td style="text-align: center;">1000</td>
</tr>
<tr>
<td>201-300</td>
<td style="text-align: center;">510</td>
<td style="text-align: center;">0.7</td>
<td style="text-align: center;">1000</td>
</tr>
<tr>
<td>301*-</td>
<td style="text-align: center;">510</td>
<td style="text-align: center;">0.65</td>
<td style="text-align: center;">1000</td>
</tr>
</tbody>
</table>

Notes: \*Individuals participating in a public employment service
program receive support in the form of an activity grant, which they can
receive as long as they are taking part in the program, i.e. no more
than 450 days (parents with children) or no more than 300 days (if no
children).

Source: Akademikernas a-kassa
(<https://www.akademikernasakassa.se/gamla-ersattningen/ersattning-och-utbetalning/ersattningsniva>)

<span id="_Toc222502819" class="anchor"></span>**Table 2.6**
Unemployment benefits October 1st 2025 and onwards

<table style="width:54%;">
<colgroup>
<col style="width: 19%" />
<col style="width: 9%" />
<col style="width: 11%" />
<col style="width: 3%" />
<col style="width: 10%" />
</colgroup>
<thead>
<tr>
<th><strong>Labour days</strong></th>
<th style="text-align: center;"><p><strong>Basic amount</strong></p>
<p><strong>SEK/day</strong></p></th>
<th colspan="2"
style="text-align: center;"><p><strong>Compensation</strong></p>
<p><strong>(as a share of previous income)</strong></p></th>
<th style="text-align: center;"><p><strong>Upper limit</strong></p>
<p><strong>SEK/day</strong><a href="#fn1" class="footnote-ref"
id="fnref1" role="doc-noteref"><sup>1</sup></a></p></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>12 months membership</strong></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;"></td>
</tr>
<tr>
<td>1-100</td>
<td style="text-align: center;">365</td>
<td style="text-align: center;">0.8</td>
<td colspan="2" style="text-align: center;">1236</td>
</tr>
<tr>
<td>101-200</td>
<td style="text-align: center;">365</td>
<td style="text-align: center;">0.7</td>
<td colspan="2" style="text-align: center;">1082</td>
</tr>
<tr>
<td>201-300</td>
<td style="text-align: center;">365</td>
<td style="text-align: center;">0.65</td>
<td colspan="2" style="text-align: center;">1005</td>
</tr>
<tr>
<td><strong>6-11 months membership</strong></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;"></td>
</tr>
<tr>
<td>1-100</td>
<td style="text-align: center;">365</td>
<td style="text-align: center;">0.6</td>
<td colspan="2" style="text-align: center;">927</td>
</tr>
<tr>
<td>101-200</td>
<td style="text-align: center;">365</td>
<td style="text-align: center;">0.5</td>
<td colspan="2" style="text-align: center;">773</td>
</tr>
<tr>
<td>201-300</td>
<td style="text-align: center;">365</td>
<td style="text-align: center;">0.45</td>
<td colspan="2" style="text-align: center;">695</td>
</tr>
<tr>
<td><strong>1-5 months membership</strong></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;"></td>
</tr>
<tr>
<td>1-100</td>
<td style="text-align: center;">365</td>
<td style="text-align: center;">0.5</td>
<td colspan="2" style="text-align: center;">773</td>
</tr>
<tr>
<td>101-200</td>
<td style="text-align: center;">365</td>
<td style="text-align: center;">0.4</td>
<td colspan="2" style="text-align: center;">618</td>
</tr>
<tr>
<td>201-300</td>
<td style="text-align: center;">365</td>
<td style="text-align: center;">0.35</td>
<td colspan="2" style="text-align: center;">541</td>
</tr>
</tbody>
</table>
<section id="footnotes" class="footnotes footnotes-end-of-document"
role="doc-endnotes">
<hr />
<ol>
<li id="fn1"><p>Starting October 1<sup>st</sup>, the highest upper limit
is increased to 1236 SEK/day. This is not modelled in EUROMOD for
2025.<a href="#fnref1" class="footnote-back"
role="doc-backlink">↩︎</a></p></li>
</ol>
</section>

Notes: \*Individuals participating in a public employment service
program receive support in the form of an activity grant, which they can
receive as long as they are taking part in the program, which can be up
to 450 days at the basic amount level.

Source: Akademikernas a-kassa
(<https://www.akademikernasakassa.se/ersattningen/ersattning-och-utbetalning/ersattningsniva>)

The following table summarises the main characteristics of unemployment
insurance benefit in Sweden.

<span id="_Toc222502820" class="anchor"></span>**Table 2.7**
Characteristics of the unemployment benefit

<table style="width:70%;">
<colgroup>
<col style="width: 8%" />
<col style="width: 14%" />
<col style="width: 9%" />
<col style="width: 9%" />
<col style="width: 9%" />
<col style="width: 9%" />
<col style="width: 9%" />
</colgroup>
<thead>
<tr>
<th></th>
<th></th>
<th style="text-align: center;"><strong>2022</strong></th>
<th style="text-align: center;"><strong>2023</strong></th>
<th style="text-align: center;"><strong>2024</strong></th>
<th style="text-align: center;"><strong>2025, Jan-Sep</strong></th>
<th style="text-align: center;"><strong>2025, Oct-Dec</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Eligibility</strong></td>
<td>Contribution period</td>
<td style="text-align: center;">6 out of 12 last months</td>
<td style="text-align: center;">6 out of 12 last months</td>
<td style="text-align: center;">6 out of 12 last months</td>
<td style="text-align: center;">6 out of 12 last months</td>
<td style="text-align: center;"><p>Salary of at least</p>
<p>120 000 SEK last 12 months</p></td>
</tr>
<tr>
<td></td>
<td>Other conditions</td>
<td style="text-align: center;">Membership to UI fund</td>
<td style="text-align: center;">Membership to UI fund</td>
<td style="text-align: center;">Membership to UI fund</td>
<td style="text-align: center;">Membership to UI fund</td>
<td style="text-align: center;">Membership length affects basic
amount</td>
</tr>
<tr>
<td></td>
<td>Eligibility of self-employed</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">Yes</td>
</tr>
<tr>
<td><strong>Payment</strong></td>
<td>Contribution base</td>
<td style="text-align: center;">Gross earnings (12 months before)</td>
<td style="text-align: center;">Gross earnings (12 months before)</td>
<td style="text-align: center;">Gross earnings (12 months before)</td>
<td style="text-align: center;">Gross earnings (12 months before)</td>
<td style="text-align: center;">Gross earnings (12 months before)</td>
</tr>
<tr>
<td></td>
<td>Basic amount</td>
<td style="text-align: center;">510 SEK/day or 80% of previous earnings
(decreasing to 65%)</td>
<td style="text-align: center;">510 SEK/day or 80% of previous earnings
(decreasing to 65%)</td>
<td style="text-align: center;">510 SEK/day or 80% of previous earnings
(decreasing to 65%)</td>
<td style="text-align: center;">510<a href="#fn1" class="footnote-ref"
id="fnref1" role="doc-noteref"><sup>1</sup></a> SEK/day or 80% of
previous earnings (decreasing to 65%)</td>
<td style="text-align: center;">365<a href="#fn2" class="footnote-ref"
id="fnref2" role="doc-noteref"><sup>2</sup></a> SEK/day or 50-80% of
previous earnings (decreasing to 35-65%)</td>
</tr>
<tr>
<td></td>
<td>Additional amount</td>
<td style="text-align: center;">N/A</td>
<td style="text-align: center;">N/A</td>
<td style="text-align: center;">N/A</td>
<td style="text-align: center;">N/A</td>
<td style="text-align: center;">N/A</td>
</tr>
<tr>
<td></td>
<td>Floor<sup>a</sup></td>
<td style="text-align: center;">510 SEK/day</td>
<td style="text-align: center;">510 SEK/day</td>
<td style="text-align: center;">510 SEK/day</td>
<td style="text-align: center;">510 SEK/day</td>
<td style="text-align: center;">365 SEK/day</td>
</tr>
<tr>
<td></td>
<td>Ceiling<sup>a</sup></td>
<td style="text-align: center;">1200 SEK/day</td>
<td style="text-align: center;">1200 SEK/day</td>
<td style="text-align: center;">1200 SEK/day</td>
<td style="text-align: center;">1200 SEK/day</td>
<td style="text-align: center;">1236 SEK/day</td>
</tr>
<tr>
<td><strong>Duration</strong></td>
<td>Standard (in labour days)</td>
<td style="text-align: center;">300</td>
<td style="text-align: center;">300</td>
<td style="text-align: center;">300</td>
<td style="text-align: center;">300</td>
<td style="text-align: center;">300</td>
</tr>
<tr>
<td></td>
<td>Special cases (in labour days)</td>
<td style="text-align: center;">450 (parent with child)</td>
<td style="text-align: center;">450 (parent with child)</td>
<td style="text-align: center;">450 (parent with child)</td>
<td style="text-align: center;">450 (parent with child)</td>
<td style="text-align: center;">N/A</td>
</tr>
<tr>
<td><strong>Subject to</strong></td>
<td>Taxes</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">Yes</td>
</tr>
<tr>
<td></td>
<td>SIC</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">Yes</td>
</tr>
</tbody>
</table>
<section id="footnotes" class="footnotes footnotes-end-of-document"
role="doc-endnotes">
<hr />
<ol>
<li id="fn1"><p>510 SEK for 12 months of full-time employment, for
part-time employment a minimum of 255 SEK is applied, for all years in
the table.<a href="#fnref1" class="footnote-back"
role="doc-backlink">↩︎</a></p></li>
<li id="fn2"><p>365 SEK for 12 months of full-time employment, for
part-time employment a minimum of 255 SEK is applied, for all years in
the table.<a href="#fnref2" class="footnote-back"
role="doc-backlink">↩︎</a></p></li>
</ol>
</section>

Notes: a The floor and ceiling are defined for full-time workers. For
individuals working less than fulltime, the floor and ceiling are scaled
down in proportion to their working time.

Source: Akademikernas a-kassa
(<https://www.akademikernasakassa.se/gamla-ersattningen/ansokan-och-rapportering/grundregler>,
<https://www.akademikernasakassa.se/gamla-ersattningen/ersattning-och-utbetalning/ersattningsperiod>,
<https://www.akademikernasakassa.se/gamla-ersattningen/ersattning-och-utbetalning/ersattningsniva>,
<https://www.akademikernasakassa.se/ersattningen/ansokan-och-rapportering/grundregler>,
<https://www.akademikernasakassa.se/ersattningen/ersattning-och-utbetalning/ersattningsperiod>,
<https://www.akademikernasakassa.se/ersattningen/ersattning-och-utbetalning/ersattningsniva>)

#### EUROMOD modelling

The changes on October 1st is as of now not yet modelled in EUROMOD. The
full year of 2025 is modelled after the pre-October policy rules,
modelling details described below.

Effectively, this benefit is only partly simulated using the information
about actual receipt and it is switched off in the baseline. Rather than
only using the observed receipt as part of the eligibility criteria, all
eligibility rules in full detail are covered. However, as not all
required information (e.g. work history) is available several
assumptions are made, including considering some rules automatically
fulfilled for those observed in receipt of this benefit. This approach
is chosen so that the benefit can be also modelled for those currently
employed if needed (e.g. to simulate their entitlement if they become
unemployed, for replacement rates calculations).

Unemployment duration (lunmy_s) is set equal to the minimum between the
maximum duration according to the national rules and, the maximum of
observed unemployment duration (lunmy) and observed benefit receipt
(bunmy). If modelling unemployment benefit for those currently employed,
unemployment duration is set equal to the minimum between the maximum
duration according to the national rules or the reported number of
months in employment in the current year (liwmy), once contribution
history (see the next step) is modelled. It is effectively also assumed
that unemployment spells start in the reference year.

Modelled contribution history is based on the reported number of months
in employment (liwmy), controlling for the total number of months in
work (liwwh).

1.  For those currently employed (lnu\>0), this is used.

2.  For those currently unemployed (lunmy_s \> 0) and in receipt (bunct
    \> 0), this is set at least equal to the minimum qualifying period.

3.  For those currently unemployed (lunmy_s \> 0) and not in receipt
    (bunct = 0), this is set to zero.

At this point, people who are unemployed (lunmy_s \> 0), have not
reached retirement age yet and have sufficient contribution history are
considered eligible. In our simulations we assume that all employees
fulfil the eligibility condition of being a member of an unemployment
insurance fund for at least 12 months. On the contrary, it is assumed
that the self-employed are not members of an unemployment insurance fund
and are therefore entitled only to the daily allowance. Part-time
benefit is not simulated as no information about whether part-timers are
seeking for full-time work or not is available.

Benefit duration (bunmy_s) is simply set equal to the unemployment
duration (lunmy_s) as long as this is smaller than the maximum duration
according to the national rules. The standard maximum duration is 300
(labour) days but in case of parents with children it is 450 (labour)
days.

Benefit entitlement is calculated based on the variable previous
earnings, which is equal to current earnings for those in work and which
is obtained by reverse engineering starting from the unemployment
benefit amount for the unemployed.

The benefit is calculated as an average over the applicable parameters
over the year (assuming that all spells started at the beginning of the
year).

***COVID-19 Notes***

Due to the Covid-19 pandemic the government has temporarily changed the
eligibility conditions of the unemployment insurance benefit. From 13
April 2020 the eligibility conditions were temporarily eased and the six
qualifying days are temporarily removed. Individuals fulfilling the
requirements, but without membership of an unemployment insurance fund,
receive a daily allowance (5 days a week) equal to 510 SEK. Individuals
without a membership and without enough hours worked to be eligible for
unemployment insurance benefit, receive a daily allowance (5 days a
week) equal to 255 SEK.

From 31 March 2020 to 31 December 2022 the (non-simulated) requirement
for membership to an unemployment insurance fund are lowered to 3 months
and the number of hours worked has been lowered to 60 hours per month
during at least 6 months during the last 12 months. For 2023, most of
these temporary conditions have been prolonged. The six qualifying days,
that were previously completely removed, are now 2 days (as it also was
in 2021 and 2022). The higher levels of the unemployment insurance and
the lower work requirements are kept, but the membership requirements to
an unemployment insurance fund are changed back to the pre-pandemic
level of 12 months.

### Child benefit (bch_s)

#### Definitions 

The child benefit is a universal benefit received by legal guardians of
children aged 0-15 years or until 18 years if in upper secondary school.

#### Eligibility conditions

If having children aged 0-15 years or until 18 years if in upper
secondary school the family receives this benefit.

The assessment unit is the nuclear family (tu_bch_se), including
cohabiting partners and children aged below 16 years or until 18 years
if in upper secondary school.

Children, who are themselves parents, count as children as well.

#### Income test

Not applicable.

#### Benefit amount 

Child benefit’s basic amount is for each child until 16 years of age.
From the second child on, there is an extra benefit in addition to the
basic amount. If the child is a student in a lower secondary school (dec
=3), the child benefit is prolonged until he completes compulsory
education (grade 9). The child benefit is received 12 months a year.

Children aged 16-20 years and studying in upper secondary school (dec=
4) receive the basic amount of the child benefit (i.e. study allowance)
10 months a year. The extra amount is paid 12 months per year.

The extra amount is based on the number of children receiving child
benefit and study allowance.

The benefit is not taxable.

<span id="_Toc222502821" class="anchor"></span>**Table 2.8** Child
benefit monthly amounts – 2020-2025

| **Child number** | **Basic amount** | **Extra amount<sup>a</sup>** | **Total amount** |
|:--:|:--:|:--:|:--:|
| **1** | 1,250 | 0 | 1,250 |
| **2** | 1,250 | 150 | 2,650 |
| **3** | 1,250 | 580 | 4,480 |
| **4** | 1,250 | 1,010 | 6,740 |
| **5** | 1,250 | 1,250 | 9,240 |
| **Next child** | 1,250 | 1,250 | 9,240 + nr. of extra children \* 1,250 |

Note: <sup>a</sup> the extra amount is cumulative. E.g., a family with 6
kids get 1250\*6+150+580+1010+1250+1250=11740

Source: Swedish Social Insurance Agency
(<https://www.forsakringskassan.se/privatperson/foralder/barnbidrag-och-flerbarnstillagg>)

#### Allocation of the benefit within the family 

The benefit (basic and extra amount) for children until 18 years is by
default split evenly between the legal guardians if they have joint
custody and the child was born after 1 March 2014 otherwise it is paid
to the legal guardian with sole custody. For children born before 1
March 2014, the benefit is paid to one legal guardian by default. The
basic amount for children older than 18 years is paid directly to the
child. The extra amount (12 months per year) is always received by the
parents.

#### EUROMOD modelling 

The child benefit Allocate function (22.6) has been implemented
incorrectly from 2014 and onwards. Currently, the policy is implemented
as if the child benefit is split between parents with joint custody in
relation to all children, when this is only the case for children born
after 1 March 2014. It needs to be separated into two groups of children
– born before 2014 and born after 2014.

### Housing allowance (bho_s)

#### Definitions 

The unit of assessment is the family.

#### Eligibility conditions

Housing allowance can be given to families (tu_bho_se) with children (up
to 18 years old, or aged under 20 and receiving the basic amount of
child benefit (dec = 4)) and to single and married/cohabiting couples
without children where at least one family member is 18-29 years old.
The maximum allowance depends on the composition of the household, the
housing cost, the income of the household, and the size of the dwelling.
If the household exceeds certain income thresholds, the allowance is
reduced (see table 2.8 below). The eligibility criteria are active
regardless of whether the person owns or rents the residence.

In multi-family households, the housing allowance is given only to the
main family unit responsible for the house (i.e. xhc \>0).

Housing allowance below 100 SEK/month is not paid out. The benefit is
not taxable.

#### Income test

For higher incomes exceeding specific thresholds, the allowance is
reduced; 20% of annual income for parents and lone parents, and 33% of
annual income for lone youngsters and young couples with children.

<span id="_Toc222502822" class="anchor"></span>**Table 2.9** Housing
allowance – Thresholds 2020-2025

<table style="width:62%;">
<colgroup>
<col style="width: 6%" />
<col style="width: 7%" />
<col style="width: 5%" />
<col style="width: 8%" />
<col style="width: 5%" />
<col style="width: 7%" />
<col style="width: 5%" />
<col style="width: 7%" />
<col style="width: 5%" />
</colgroup>
<thead>
<tr>
<th rowspan="2" style="text-align: center;"><strong>Year</strong></th>
<th colspan="2" style="text-align: center;"><strong>Cohabiting
Parents</strong></th>
<th colspan="2" style="text-align: center;"><strong>Lone
Parents</strong></th>
<th colspan="2" style="text-align: center;"><strong>Young Couples
without Children</strong></th>
<th colspan="2" style="text-align: center;"><strong>Lone
Youth</strong></th>
</tr>
<tr>
<th style="text-align: center;"><strong>Threshold (for each
parent)</strong></th>
<th style="text-align: center;"><strong>Rate</strong></th>
<th style="text-align: center;"><strong>Threshold</strong></th>
<th style="text-align: center;"><strong>Rate</strong></th>
<th style="text-align: center;"><strong>Threshold</strong></th>
<th style="text-align: center;"><strong>Rate</strong></th>
<th style="text-align: center;"><strong>Threshold</strong></th>
<th style="text-align: center;"><strong>Rate</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><strong>2022</strong></td>
<td style="text-align: center;">75,000</td>
<td style="text-align: center;">20%</td>
<td style="text-align: center;">150,000</td>
<td style="text-align: center;">20%</td>
<td style="text-align: center;">58,000</td>
<td style="text-align: center;">33%</td>
<td style="text-align: center;">41,000</td>
<td style="text-align: center;">33%</td>
</tr>
<tr>
<td style="text-align: center;"><strong>2023</strong></td>
<td style="text-align: center;">75,000</td>
<td style="text-align: center;">20%</td>
<td style="text-align: center;">150,000</td>
<td style="text-align: center;">20%</td>
<td style="text-align: center;">58,000</td>
<td style="text-align: center;">33%</td>
<td style="text-align: center;">41,000</td>
<td style="text-align: center;">33%</td>
</tr>
<tr>
<td style="text-align: center;"><strong>2024</strong></td>
<td style="text-align: center;">75,000</td>
<td style="text-align: center;">20%</td>
<td style="text-align: center;">150,000</td>
<td style="text-align: center;">20%</td>
<td style="text-align: center;">58,000</td>
<td style="text-align: center;">33%</td>
<td style="text-align: center;">41,000</td>
<td style="text-align: center;">33%</td>
</tr>
<tr>
<td style="text-align: center;"><strong>2025</strong></td>
<td style="text-align: center;">75,000</td>
<td style="text-align: center;">20%</td>
<td style="text-align: center;">150,000</td>
<td style="text-align: center;">20%</td>
<td style="text-align: center;">58,000</td>
<td style="text-align: center;">33%</td>
<td style="text-align: center;">41,000</td>
<td style="text-align: center;">33%</td>
</tr>
</tbody>
</table>

Source: The Swedish Social Security Code (Socialförsäkringsbalken)
(<https://lagen.nu/2010:110#AGUII>)

The wealth of the family (property excluded) exceeding 100,000 SEK is
added to the income by 15 % (afc00_s).

For calculating the housing allowance, the following individual income
concept for each adult in the family is considered:

Income (il_means_bho) = (Employment income (yem) + fringe benefits
(kfb) + Private pensions (ypp) + Unemployment benefits (bunct + bunnc) +
Old age pension (poa) + Survivor’ pension (psu) + Sickness benefit
(bhl) + Disability benefit (pdi) + property income (ypr) + investment
income (yiy) + self-employment income (yse) + maintenance payments
received (ypt) + 80% of education allowances (bed) + parents’ allowance
(bpl) + 15% of wealth ((afc00_s, divided by two if there are two
partners) – 100 000)

Losses due to self-employment are set to 0.

#### EUROMOD modelling

For housing cost the variable xhc is used, which is a proxy of the
housing cost considered in the assessment of the allowance.

In the system there are limitations on size in m2 for the flat; those
limitations cannot be simulated.

Currently, the reduction for cohabiting parents is computed separately,
referring to these as dgn=0, ‘female partner’ and dgn=1, ‘male partner’.
This does not include same-sex parents.

#### Benefit amount 

<u>Families with children:</u>

The housing allowance is calculated as the sum of a *special component*
for families with children and a *rent component*:

The special component consists of a special component for children who
live permanently at the household (sin01_s) and a special component for
children with alternating households. It is assumed that all children
live permanently at households because there is no variable to
distinguish them from those with alternating household. Both components
are given by the table below.

If there are children with both permanent household and alternating
households in the same family, the special component for the permanent
children is paid out first and the alternating children is given a
special component according to the table below.

The rent component (sin02_s) is calculated as follows:

Rent component = (min(xhc , upper level) – lower level)\*0.5

according to the lower and upper values reported in the following table:

<span id="_Toc222502823" class="anchor"></span>**Table 2.10** Housing
allowance parameters – Families with children – 2021- 2025

<table style="width:65%;">
<colgroup>
<col style="width: 8%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 17%" />
<col style="width: 16%" />
</colgroup>
<thead>
<tr>
<th></th>
<th colspan="2" style="text-align: center;"><strong>Rent
component</strong></th>
<th style="text-align: center;"><strong>Special component, permanent
households</strong></th>
<th style="text-align: center;"><strong>Special component, alternating
households</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Number of children</strong></td>
<td style="text-align: center;"><strong>Lower level
SEK/month</strong></td>
<td style="text-align: center;"><strong>Upper level
SEK/month</strong></td>
<td style="text-align: center;"><strong>SEK/month</strong></td>
<td style="text-align: center;"><strong>SEK/month</strong></td>
</tr>
<tr>
<td>1</td>
<td style="text-align: center;">1,400</td>
<td style="text-align: center;">5,300</td>
<td style="text-align: center;">1,500</td>
<td style="text-align: center;">1,300</td>
</tr>
<tr>
<td>2</td>
<td style="text-align: center;">1,400</td>
<td style="text-align: center;">5,900</td>
<td style="text-align: center;">2,000</td>
<td style="text-align: center;">1,600</td>
</tr>
<tr>
<td>3 and more</td>
<td style="text-align: center;">1,400</td>
<td style="text-align: center;">6,600</td>
<td style="text-align: center;">2,650</td>
<td style="text-align: center;">2,100</td>
</tr>
</tbody>
</table>

Source: The Swedish Social Security Code (Socialförsäkringsbalken)
(<https://lagen.nu/2010:110#AGUII>)

<span id="_Toc222502824" class="anchor"></span>**Table 2.11** Housing
allowance parameters – Families with children with both permanent and
alternating housholds– 2021-2025

| **Number of permanent children** | **Number of alternating children** | **Special component for the children(s) SEK/month** |
|:--:|:--:|:--:|
| 1 | 1 | 300 |
| 2 | 1 | 500 |
| 1 | 2 | 800 |

Source: The Swedish Social Security Code (Socialförsäkringsbalken)
(<https://lagen.nu/2010:110#AGUII>)

The housing allowance is reduced following the equation below with the
parameters of the valid year (i.e., 2022 as in the equation below),
which vary according to the typology of the recipient. Thus, the
equation is similar for every year, but with the annual values from
table 2.8. added:

Married or cohabiting partner (the following applies to each partner
separately, yearly amounts – sin05_s):

Final Housing allowance = Housing allowance – 0.20(max((il_means_bho –
75,000), 0))

Lone parents (yearly incomes, sin06_s):

Final Housing allowance = Housing allowance – 0.20(max((il_means_bho –
150,000), 0))

***COVID-19 Notes***

During 2020, from July 1 until December 31, a temporary supplement to
housing allowance was introduced for families with children. The
temporary supplement amounted to a 25% increase in the allowance and was
granted without the need of application. This supplement was later on
extended to the period from the July 1 2021 to December 31 2021, July 1
2022 to December 31 2022 and January 1 2023 to June 30 2023 and July 1
to December 31 2023 and increased to 40% on January 1 2024. From January
1 2025, this supplement is once again lowered to 25% and on July 1 2025
it was removed. The plan is however to increase the housing allowance
permanently from Jan 1 2026.

<u>Young families below the age of 29 without children</u>

.

The rent component (sin07_s) is calculated as reported in the following
table:

<span id="_Toc222502825" class="anchor"></span>**Table 2.12** Housing
allowance parameters – Young couples without children – 2016- 2025

<table style="width:59%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 38%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><p><strong>Housing cost
(xhc)</strong></p>
<p><strong>SEK / month</strong></p></th>
<th style="text-align: center;"><strong>Rent component</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;">&lt; 1,800</td>
<td style="text-align: center;">0</td>
</tr>
<tr>
<td style="text-align: center;">1,800 – 2,600</td>
<td style="text-align: center;">(xhc - 1,800) * 0.90)</td>
</tr>
<tr>
<td style="text-align: center;">2,600 – 3,600</td>
<td style="text-align: center;">(2,600 - 1,800) * 0.90 + (3,600 - xhc) *
0.65</td>
</tr>
<tr>
<td style="text-align: center;">&gt;= 3,600</td>
<td style="text-align: center;">(2,600 - 1,800) * 0.90+(3,600 - 2,600) *
0.65</td>
</tr>
</tbody>
</table>

Source: The Swedish Social Security Code (Socialförsäkringsbalken) ()

The housing allowance is then reduced according to the typology of the
recipient:

singles (yearly incomes, sin08_s):

Final Housing allowance = Housing allowance – 0.33(max((il_means_bho–
41,000), 0))

married or cohabiting (the following applies to each partner separately,
yearly amount, sin12_s):

Final Housing allowance = Housing allowance – 0.33(max((il_means_bho –
58,000), 0))

### Housing allowance for pensioners (bhope_s)

#### Definitions 

The unit of analysis is the nuclear family (tu_bho_se), including the
cohabiting partners and children up to 18 years old, or aged under 20
and receiving the basic amount of child benefit (dec =4). In
multi-family households, the housing allowance is given only to the
family who is responsible for the house (xhc \> 0).

#### Eligibility conditions

Housing allowance for pensioners can be given to age pensioners or
disable pensioners (persons aged 19-65 who are permanently unable to
work due to a disability). It is considered to be part of the pension
system.

Families with persons older than 65 years or families with persons
receiving disability pension (pdi) can receive this allowance (age
allowance and disability allowance). The benefit is not taxable.

#### Income test

The allowance is diminished with the income over certain income limits,
which are dependent of the recipients being married/cohabitants (126,060
SEK) or single (139,239 SEK). Labour income is weighted less than
pension income. Additionally,15% of the wealth (afc) of the family
(divided by two if there are two partners) over 100,000 SEK for single
and 200,000 SEK for cohabiting partner is considered as income.

For calculating the housing allowance for pensioners the following
individual income concept (“reserved amount”) for each elderly or
disabled adult (if a child is living with his parents only the parents
can receive the allowance) in the family is calculated for all years
2009-2020 and deducted from the means:

<span id="_Toc222502826" class="anchor"></span>**Table 2.13** Housing
allowance for pensioners – Reserved amount – 2021-2025

<table style="width:64%;">
<colgroup>
<col style="width: 18%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Condition</strong></th>
<th style="text-align: center;"><p><strong>Reserved amount</strong></p>
<p><strong>2021</strong> (ydg01_s)</p></th>
<th style="text-align: center;"><p><strong>Reserved amount</strong></p>
<p><strong>2022</strong></p></th>
<th style="text-align: center;"><p><strong>Reserved amount</strong></p>
<p><strong>2023-2025</strong></p></th>
</tr>
</thead>
<tbody>
<tr>
<td>pdi&gt;0 and age&lt;= 20</td>
<td style="text-align: center;">2.23*XBASM</td>
<td style="text-align: center;">2.48*XBASM</td>
<td style="text-align: center;">2.48*XBASM</td>
</tr>
<tr>
<td>pdi&gt;0 and 20&lt; age &lt;= 22</td>
<td style="text-align: center;">2.28*XBASM</td>
<td style="text-align: center;">2.53*XBASM</td>
<td style="text-align: center;">2.53*XBASM</td>
</tr>
<tr>
<td>pdi&gt;0 and 22&lt; age &lt;= 24</td>
<td style="text-align: center;">2.33*XBASM</td>
<td style="text-align: center;">2.58*XBASM</td>
<td style="text-align: center;">2.58*XBASM</td>
</tr>
<tr>
<td>pdi&gt;0 and 24&lt; age &lt;= 26</td>
<td style="text-align: center;">2.38*XBASM</td>
<td style="text-align: center;">2.63*XBASM</td>
<td style="text-align: center;">2.63*XBASM</td>
</tr>
<tr>
<td>pdi&gt; 0 and 26&lt; age &lt;= 28</td>
<td style="text-align: center;">2.43*XBASM</td>
<td style="text-align: center;">2.68*XBASM</td>
<td style="text-align: center;">2.68*XBASM</td>
</tr>
<tr>
<td>pdi&gt; 0 and 28&lt; age &lt;= 29</td>
<td style="text-align: center;">2.48*XBASM</td>
<td style="text-align: center;">2.73*XBASM</td>
<td style="text-align: center;">2.73*XBASM</td>
</tr>
<tr>
<td>pdi&gt; 0 and age&gt;= 30</td>
<td style="text-align: center;">2.53*XBASM</td>
<td style="text-align: center;">2.78*XBASM</td>
<td style="text-align: center;">2.78*XBASM</td>
</tr>
<tr>
<td>Single, age&gt;65 and pdi=0</td>
<td style="text-align: center;">2.181*XBASM</td>
<td style="text-align: center;">2.181*XBASM</td>
<td style="text-align: center;">2.43*XBASM</td>
</tr>
<tr>
<td>Married or cohabiting, age &gt; 65 and pdi=0</td>
<td style="text-align: center;">1.951*XBASM</td>
<td style="text-align: center;">1.951*XBASM</td>
<td style="text-align: center;">2.2*XBASM</td>
</tr>
</tbody>
</table>

Source: The Swedish Social Security Code (Socialförsäkringsbalken)
(<https://lagen.nu/2010:110#K99>)

For person younger than 66 years

Income (il_means_bhope) = Old age pension (poa) + Disability benefit
(pdi) + investment income (yiy) + 0.8\*(Private pensions (ypp) + fringe
benefits (kfb) + Unemployment benefits (bunct + bunnc) + Sickness
benefit (bhl) + parents’ allowance (bpl)+ Survivor’ pension (psu)) +
property income (ypr) + 0.5 \* (Employment income (yem) +
self-employment income (yse)) + 0.15\*(wealth (afc00_s, divided by two
if there are two partners) – 100 000) – reserved amount (ydg01_s).

For persons older than 64 years from 2020 (65 from 2023) and onwards

Income (il_means_bhope) = 0.93 \* Income related pension (proxied by
poa) +

Guarantee pension (not included as already in poa) + Widow’s pension
(proxied by psu) + investment income (yiy) + property income (ypr) +
0.15\*(wealth (afc00_s, divided by two if there are two partners) – 100
000) + 0.93 \*max( (Employment income (yem)+ self-employment income
(yse))-24000,0) + 0.93 \*(Private pensions (ypp) + fringe benefits
(kfb) + Unemployment benefits (bunct + bunnc) + Sickness benefit (bhl) +
parents’ allowance (bpl) + other survivor pensions (not included as
already in psu)) – reserved amount (ydg01_s)

The proxies and omissions are used because it is not possible to
separate some benefits within variables in the data. We believe that the
misclassified benefits are smaller compared to the other benefits
included in those aggregated variables. With respect to Incomes related
pension, its components should only be Income pension, Supplementary
pension and Premium pension.

This Income is calculated independently for each partner. If married or
cohabiting then Income (sin02_s) = (Income_male + Income_female)/2

#### Benefit amount 

The maximum housing allowance (sin01_s) is calculated as follows per
each entitled individual:

For 2021

\- persons younger than 65 years and receiving disability pensions:
0.96\* min((xhc-bho_s), 5000)+0.7\*(MAX(MIN(xhc-bho_s,5600)-5000,0))

\- persons older than 64 years and married: 1.0\* min((xhc-bho_s),
3000)+0.9\*(MAX(MIN(xhc-bho_s,5000)-3000,0)+0.7\*(MAX(MIN(xhc-bho_s,7000)-5000,0))+12\*170

\- persons older than 64 years and single: 1.0\* min((xhc-bho_s),
3000)+0.90\*(MAX(MIN(xhc-bho_s,5000)-3000,0)+0.7\*(MAX(MIN(xhc-bho_s,7000)-5000,0))+12\*340

For 2022

\- persons younger than 65 years and receiving disability pensions:
0.96\* min((xhc-bho_s), 5000)+0.7\*(MAX(MIN(xhc-bho_s,7500)-5000,0))

\- persons older than 64 years and married: 1.0\* min((xhc-bho_s),
3000)+0.9\*(MAX(MIN(xhc-bho_s,5000)-3000,0)+0.7\*(MAX(MIN(xhc-bho_s,7000)-5000,0)+0.5\*(MAX(MIN(xhc-bho_s),7500)-7000,0))+)+12\*270

\- persons older than 64 years and single: 1.0\* min((xhc-bho_s),
3000)+0.9\*(MAX(MIN(xhc-bho_s,5000)-3000,0)+0.7\*(MAX(MIN(xhc-bho_s,7000)-5000,0)+0.5\*(MAX(MIN(xhc-bho_s),7500)-7000,0))+12\*540

For 2023-2025

\- persons younger than 66 years and receiving disability pensions:
0.96\* min((xhc-bho_s), 5000)+0.7\*(MAX(MIN(xhc-bho_s,7500)-5000,0))

\- persons older than 65 years and married: 1.0\* min((xhc-bho_s),
3000)+0.9\*(MAX(MIN(xhc-bho_s,5000)-3000,0)+0.7\*(MAX(MIN(xhc-bho_s,7000)-5000,0)+0.5\*(MAX(MIN(xhc-bho_s),7500)-7000,0))+)+420

\- persons older than 65 years and single: 1.0\* min((xhc-bho_s),
3000)+0.9\*(MAX(MIN(xhc-bho_s,5000)-3000,0)+0.7\*(MAX(MIN(xhc-bho_s,7000)-5000,0)+0.5\*(MAX(MIN(xhc-bho_s),7500)-7000,0))+840

Housing costs and Housing allowance are always considered at family
level. If it is a cohabiting couple then the maximum allowance is
divided by 2 (even in case only one partner is entitled to the allowance
because each partner is expected to pay their part of the housing cost).

The upper levels of housing costs are reported in the following table:

<span id="_Toc222502827" class="anchor"></span>**Table 2.14** Housing
allowance for pensioners – Maximum housing costs limits and total
coverage at maximum limit– 2021-2025

<table style="width:59%;">
<colgroup>
<col style="width: 5%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 13%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Year</strong></th>
<th style="text-align: center;"><p><strong>Upper level housing
cost</strong></p>
<p><strong>Disability pens.</strong></p>
<p><strong>SEK/month</strong></p></th>
<th style="text-align: center;"><p><strong>Per cent benefit</strong></p>
<p><strong>Disability pens.</strong></p></th>
<th style="text-align: center;"><p><strong>Upper level housing
cost</strong></p>
<p><strong>Age pensioners</strong></p>
<p><strong>SEK/month</strong></p></th>
<th style="text-align: center;"><p><strong>Per cent benefit</strong></p>
<p><strong>Age pensioners</strong></p></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>2021</strong></td>
<td style="text-align: center;">7,500</td>
<td style="text-align: center;">87.3</td>
<td style="text-align: center;">7,500</td>
<td style="text-align: center;">93.2</td>
</tr>
<tr>
<td><strong>2022</strong></td>
<td style="text-align: center;">7,500</td>
<td style="text-align: center;">87.3</td>
<td style="text-align: center;">7,500</td>
<td style="text-align: center;">97.2</td>
</tr>
<tr>
<td><strong>2023</strong></td>
<td style="text-align: center;">7,500</td>
<td style="text-align: center;">87.3</td>
<td style="text-align: center;">7,500</td>
<td style="text-align: center;">97.2</td>
</tr>
<tr>
<td><strong>2025</strong></td>
<td style="text-align: center;">7,500</td>
<td style="text-align: center;">87.3</td>
<td style="text-align: center;">7,500</td>
<td style="text-align: center;">97.2</td>
</tr>
</tbody>
</table>

Source: The Swedish Social Security Code (Socialförsäkringsbalken)
(<https://lagen.nu/2010:110#K99>)

<span id="_Toc222502828" class="anchor"></span>**Table 2.15** Housing
allowance for pensioners – Thresholds and marginal coverage – 2020-2025

<table style="width:63%;">
<colgroup>
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
<th colspan="4" style="text-align: center;"><strong>Disability
Pension</strong></th>
<th colspan="4" style="text-align: center;"><strong>Old-Age
Pension</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2"
style="text-align: center;"><strong>2020-2021</strong></td>
<td colspan="2"
style="text-align: center;"><strong>2022-2024</strong></td>
<td colspan="2"
style="text-align: center;"><strong>2020-2021</strong></td>
<td colspan="2"
style="text-align: center;"><strong>2022-2024</strong></td>
</tr>
<tr>
<td style="text-align: center;"><strong>Housing Cost
Threshold</strong></td>
<td style="text-align: center;"><strong>Benefit Coverage
(%-rate)</strong></td>
<td style="text-align: center;"><strong>Housing Cost
Threshold</strong></td>
<td style="text-align: center;"><strong>Benefit Coverage
(%-rate)</strong></td>
<td style="text-align: center;"><strong>Housing Cost
Threshold</strong></td>
<td style="text-align: center;"><strong>Benefit Coverage
(%-rate)</strong></td>
<td style="text-align: center;"><strong>Housing Cost
Threshold</strong></td>
<td style="text-align: center;"><strong>Benefit Coverage
(%-rate)</strong></td>
</tr>
<tr>
<td style="text-align: center;">5,000</td>
<td style="text-align: center;">96</td>
<td style="text-align: center;">5,000</td>
<td style="text-align: center;">96</td>
<td style="text-align: center;">3,000</td>
<td style="text-align: center;">100</td>
<td style="text-align: center;">3,000</td>
<td style="text-align: center;">100</td>
</tr>
<tr>
<td style="text-align: center;">5,600</td>
<td style="text-align: center;">70</td>
<td style="text-align: center;">7,500</td>
<td style="text-align: center;">70</td>
<td style="text-align: center;">5,000</td>
<td style="text-align: center;">96</td>
<td style="text-align: center;">5,000</td>
<td style="text-align: center;">90</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">7,000</td>
<td style="text-align: center;">70</td>
<td style="text-align: center;">7,000</td>
<td style="text-align: center;">70</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">7,500</td>
<td style="text-align: center;">50</td>
</tr>
</tbody>
</table>

Source: The Swedish Social Security Code (Socialförsäkringsbalken) (
<https://lagen.nu/2010:110#K99>)

The housing allowance for pensioners is then calculated for all persons
in the family who are entitled (older than 65 or receiving disability
benefit) according to the following rules:

<span id="_Toc222502829" class="anchor"></span>**Table 2.16** Housing
allowance for disable pensioners – Amounts – 2020-2025

<table style="width:65%;">
<colgroup>
<col style="width: 28%" />
<col style="width: 36%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Condition</strong></th>
<th style="text-align: center;"><strong>Amount</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>per capita income (sin02_s) &lt; XBASM</td>
<td>max((Indiv. maximum allowance - (sin02_s*0.62)), 0)</td>
</tr>
<tr>
<td>per capita income (sin02_s) &gt;= XBASM</td>
<td><p>max((Indiv. maximum allowance - (XBASM*0.62) –</p>
<p>((sin02_s - XBASM)*0.5)), 0)</p></td>
</tr>
</tbody>
</table>

Source: The Swedish Social Security Code (Socialförsäkringsbalken)
(<https://lagen.nu/2010:110#K99>)

<span id="_Toc222502830" class="anchor"></span>**Table 2.17** Housing
allowance for old-age pensioners – Amounts – 2020-2025

| **Condition** |                      **Amount**                      |
|:-------------:|:----------------------------------------------------:|
|      N/A      | max((Indiv. maximum allowance - (sin02_s\*0.62)), 0) |

Source: The Swedish Social Security Code (Socialförsäkringsbalken)
(<https://lagen.nu/2010:110#K99>)

The total housing allowance for pensioners is given by the sum received
by both partners (if entitled).

### Social assistance (bsamt_s)

#### Definitions 

The unit of analysis is the nuclear family (tu_bho_se), including the
cohabiting partners and children up to 18 years old, or aged under 20
and receiving the basic amount of child benefit (dec =4). In
multi-family households, the social assistance is given to the family
who is responsible for the hosing cost.

#### Eligibility conditions

Social assistance is the ultimate and last part of the social safety
net. It can be paid out if the family has temporary financial problems,
or if the disposable income/month is too low. Two conditions to get
social assistance are that the family doesn’t have any wealth (afc= 0)
and is willing to take a job if offered. The income limits for getting
the benefit are based on the normative costs for a basket of commodities
needed to get a reasonable standard of living. The income limits depend
on the age of children, single or cohabitant couple, and the number of
individuals in the family. Housing costs, and costs for health, dentist,
furniture, local commuting, insurance and child care costs are not
included in the normative costs. Actual costs (xhc) are used instead.
Income losses for self-employment income are not considered (i.e. set to
0). The benefit is not taxable.

#### Income test

The family’s needs are calculated as common needs plus personal needs
depending of the age of the children and if the head of the family is
single or not. For example, a married couple with 2 children aged 4 and
8 years old have the following needs in 2025:

2,700 (Child age 4) + 3,790 (child age 8) + 7,050 (Married couple) +
2,010 (family size=4)

The family’s consumption needs are calculated according to the rules
reported in the following tables:

<span id="_Toc222502831" class="anchor"></span>**Table 2.18** Personal
needs – Monthly amounts (SEK) – 2020-2024

<table style="width:68%;">
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
<col style="width: 6%" />
<col style="width: 8%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Year\Age</strong></th>
<th style="text-align: center;"><strong>0</strong></th>
<th style="text-align: center;"><strong>1-2</strong></th>
<th style="text-align: center;"><strong>3</strong></th>
<th style="text-align: center;"><strong>4-6</strong></th>
<th style="text-align: center;"><strong>7-10</strong></th>
<th style="text-align: center;"><strong>11-14</strong></th>
<th style="text-align: center;"><strong>15-18</strong></th>
<th style="text-align: center;"><strong>19-20</strong></th>
<th style="text-align: center;"><strong>Single</strong></th>
<th style="text-align: center;"><p><strong>Married/</strong></p>
<p><strong>cohabiting</strong></p></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>2022</strong></td>
<td>2090</td>
<td>2280</td>
<td>2030</td>
<td>2210</td>
<td>3110</td>
<td>3580</td>
<td>4040</td>
<td>4070</td>
<td>3210</td>
<td>5800</td>
</tr>
<tr>
<td><strong>2023</strong></td>
<td>2270</td>
<td>2480</td>
<td>2210</td>
<td>2410</td>
<td>3380</td>
<td>3890</td>
<td>4390</td>
<td>4430</td>
<td>3490</td>
<td>6300</td>
</tr>
<tr>
<td><strong>2024</strong></td>
<td>2470</td>
<td>2700</td>
<td>2410</td>
<td>2620</td>
<td>3680</td>
<td>4230</td>
<td>4780</td>
<td>4820</td>
<td>3800</td>
<td>6850</td>
</tr>
<tr>
<td><strong>2025</strong></td>
<td>2540</td>
<td>2780</td>
<td>2480</td>
<td>2700</td>
<td>3790</td>
<td>4350</td>
<td>4920</td>
<td>4960</td>
<td>3910</td>
<td>7050</td>
</tr>
</tbody>
</table>

Source: National Board of Health and Welfare (Socialstyrelsen)
(<https://www.socialstyrelsen.se/kunskapsstod-och-regler/omraden/ekonomiskt-bistand/riksnormen/>)

<span id="_Toc222502832" class="anchor"></span>**Table 2.19** Common
needs – Monthly amounts (SEK) – 2020-2024

| **Number of family members** | **1** | **2** | **3** | **4** | **5** | **6** | **7+** |
|------------------------------|-------|-------|-------|-------|-------|-------|--------|
| **2022**                     | 1040  | 1150  | 1450  | 1640  | 1890  | 2140  | 2310   |
| **2023**                     | 1130  | 1250  | 1580  | 1790  | 2060  | 2330  | 2510   |
| **2024**                     | 1230  | 1360  | 1720  | 1950  | 2240  | 2540  | 2730   |
| **2025**                     | 1270  | 1400  | 1770  | 2010  | 2310  | 2620  | 2810   |

Source: National Board of Health and Welfare (Socialstyrelsen)
<https://www.socialstyrelsen.se/kunskapsstod-och-regler/omraden/ekonomiskt-bistand/riksnormen/>

#### Benefit amount 

Final amount of social assistance is given by the following formula:

Personal needs + Common needs + housing cost (xhc) – net income
(il_means_bsa)

If the household has had social assistance for 6 months or more when
calculating net income, only 75% of the employment income (yem) is
deducted (i.e. the household can keep 25% of employment income).

#### Take up adjustment

BTA and BCA extensions are off, so the baseline model neither adjusts
for non-take-up of the benefit nor calibrates its receipt, but the user
can activate them if necessary. See section 2.3 for technical details on
both extensions and their interactions.

Users can enable the necessary extensions in Country Tools/Set Switches.
For proper functioning, the extensions require the following inputs:

BTA: The estimated take-up rate of the benefit should be set as the
value of the \$bsamt_BTA_rate constant in the model. Currently, the
value is set to 1, indicating no adjustment for non-take-up.

BCA: The aggregate expenditure of benefit recipients needs to be filled
out in the External Statistics table, so that the calibration rate
(\$bsamt_BCA_rate) is computed accordingly. Data are currently available
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

### Parental benefit (bfapl_s)

#### Definitions 

It is a benefit to all parents that provide care for children. The
benefit can be used from 60 days before the expected birth until the
child has finished their first year in compulsory school if the child is
born before 1 January 2014. For children born on or after 1 January
2014, the benefit can be used until the child’s 12th birthday/at the end
of the fifth year in compulsory school.

#### Eligibility conditions

A parent to the child or the person who has the custody of the child is
entitled to parental benefit. The child must be resident in Sweden or
within the EU / EEA or Switzerland.

#### Benefit duration

Parental benefit covers a total of 480 days, 240 days for each parent.
Twin and triplet parents receive an additional 180 and 360 days
respectively. In the case of two parents, if the child is born before
April 1st 2023 both can stay home at the same time for maximum 30 days
(this counts as 60 days of parental leave) during the child’s first 15
months. If the child is born after April 1st 2023, both can stay home at
the same time for a maximum of 60 days (which counts as 120 days of
parental leave) [^3]. A single parent is entitled to all days.

It is possible for the parents to divide the days by transferring days
to each other. But for parents to children born in 2016 or later, 90
days are personal and cannot be transferred to the other parent (60 days
for children born before 2016). The remaining 300 days, or 150 each, can
be transferred. It is thus possible for a parent couple to divide the
days so that one gets 90 and the other 390 days. In addition to
transferring days between parents, as of July 1st 2024, 45 days can also
be transferred to someone that is not the primary caretaker of the child
(such as a grandparent or close friend). The personal days cannot be
transferred to a non-parent.

The days can be used from 60 days before the expected birth until the
child has finished their first year in compulsory school, if the child
is born before 2014. If the child is born in 2014 or later, the
custodian may take out parental benefit until the child reaches the age
of 12 or when the child ends grade 5 of the compulsory school. However,
from the child's 4th birthday, only 96 days can be saved. If you have
twins, you can save 132 days in total.

#### Benefit amount 

For 390 of days, the remuneration is based on SGI (yearly income from
work without deductions from any absence, i.e. monthly income \* 12)
(for people with both employment and self-employment income, only the
former is considered in the simulation). For these days parents receive
80% of the income up to 10 price base amounts. The resulting amount is
reduced to 97%. The personal days that cannot be transferred to the
other parent are at this level. The minimum benefit (e.g. for parents
with low or missing SGI) during these 390 days is 250 SEK per day. For
the remaining 90 days the compensation is 180 SEK per day.

The first 180 days taken for the child must be based on SGI. This also
includes days of parental benefit taken before the birth of the child.

#### Subject to taxes/SIC

The benefit is taxable.

#### Take up 

In 2010, 12% of female parents did not use parental benefit days, while
this was 68% for male parents. In 2024, 30.7 percent of the parental
leave days were used by men. For children born in 2022, 21.2% of parents
chose to split the parental days equally (defined as at least a 40/60
split).

#### EUROMOD modelling 

This benefit and the following one are switched off in the baseline
(therefore, those observed in the data are used). We assume that
duration of the parental leave depends on the month of birth of a child.
The month of birth is assumed to be equal to the middle month of the
quarter of birth reported in SILC. If child’s month of birth is
unavailable, the assumption is that the child is born on June 30 (6th
month of the year). Mother is assumed to be the main carer. Where
mothers absent, fathers are assumed to receive the allowance for the
same duration as mothers.

We assume that all women with eligible child have taken 60 days of
parental leave before childbirth and all transferable days (390) right
after the childbirth. For single parents this is extended to 480 days
(including 60 days before childbirth). The families with twins get
additional 180 days on top of that. The partners of main carers thus are
eligible for 90 days. We assume that these 90 days are also taken in the
first year of a child’s life. We assume that the main carer gets max 300
days at the high replacement rate (80%), which means that the partner
gets his/her 90 days at this rate too.

Consider allocating the parental benefit to the mother instead of the
head of the tax unit.

### Special days for the other parent (bpa_s)

#### Definitions 

The parent who is not pregnant (mostly and assumed male) has the right
to temporary parental benefit for 10 days when the child is born.

#### Eligibility conditions

Parent to the child or the person who has the custody of the child is
entitled to the benefit. The child must be resident in Sweden or within
the EU / EEA or Switzerland

#### Income test

There is no income test

#### Benefit duration

The parent can receive the benefit for 10 days. These days must be taken
within 60 days after the child has returned home

#### Benefit amount 

The amount is based on SGI. The remuneration is 80% of the income. The
resulting amount is reduced to 97%. The maximum amount is 7.5 price base
amounts, i.e. no remuneration is given for salaries above 7.5 price base
amounts.

#### Subject to taxes/SIC

The benefit is taxable.

#### Take up 

N/A

## Social contributions

### Employee social contributions(tscee_s)

#### Liability to contributions

All individual residents in Sweden and born after 1937 with employment
income (yem), fringe benefits (kfb), sickness benefit (bhl) or
unemployment benefit (bunct + bunnc) larger than 1000 SEK per year have
to pay the general social security contributions.

#### Income base used to calculate contributions

The contribution base is calculated as follows:

Initial Contribution base = (yem+kfb+bhl+bunct+bunnc)\*12. This is
rounded down to the nearest hundred SEK.

Final Contribution base = min(Initial Contribution base , 8.07\*XBASMI).
This is rounded down to the nearest hundred SEK.

#### Contribution rates

If the Final Contribution base is larger than XBASM \* 0.423, then the
Social contribution is 7% of the Final Contribution base. Otherwise no
contribution is paid. The Social contribution is then rounded down to
the nearest hundred SEK (tscee_s).

### Employer social contributions (ils_sicer)

#### Liability to contributions

All employers are liable to pay social contributions based on employment
income (yem) and fringe benefits (kfb), if the annual amount is greater
than 1,000 SEK.

#### Income base used to calculate contributions

The employer social contributions are based on employment income (yem)
and fringe benefits (kfb), if the annual amount is greater than 1,000
SEK.

#### Contribution rates

There are 8 different employer social contributions: health insurance,
parental insurance, occupational injuries, old age pension, survivors
pension, labour market, general wage fee and a special wage tax (for
persons older than 65 years).The rates are specified in the following
tables.

In 2021, reduced social contributions rates were introduced for
employers hiring young workers. Two age cohorts are eligible for the
reduced rates; 15- to 18-year-olds and 19- to 23-year-olds. The reduced
rates are only applicable if the employee earns less than 25 000 SEK per
month. For the youngest age-cohort, the employer pays the old age
pension social contribution at 10.21% only, and for the older cohort,
the employer pays all types of social contributions but at a reduced
total rate of 19.73% (instead of 31.42%). During the 3 summer months
(June, July and August), the rate of the older age group is reduced to
the same rate as the younger group. As of 2023, the lower age limit
changed to 16. The exemption for summer salaries is further removed, and
as of April 1st the lower rates for 19 - to 23 year-olds is completely
removed, regardless of salary.

<span id="_Toc222502833" class="anchor"></span>**Table 2.20** Employer
social contributions – Persons younger than 66 years old

|                                       | **2022** | **2023** | **2024** | **2025** |
|---------------------------------------|:--------:|:--------:|:--------:|:--------:|
| **Health insurance (tscersi_s)**      |  0.0355  |  0.0355  |  0.0355  |  0.0355  |
| **Old age pension (tscerpi_s)**       |  0.1021  |  0.1021  |  0.1021  |  0.1021  |
| **Survivors pension (tscerci_s)**     |  0.0060  |  0.0060  |  0.0060  |  0.0060  |
| **Occupational injuries (tscerac_s)** |  0.0020  |  0.0020  |  0.0020  |  0.0020  |
| **Labour market (tscerir_s)**         |  0.0264  |  0.0264  |  0.0264  |  0.0264  |
| **General wage fee (tscerot_s)**      |  0.1162  |  0.1162  |  0.1162  |  0.1162  |
| **Parental insurance (tscerml_s)**    |  0.0260  |  0.0260  |  0.0260  |  0.0260  |

Source: The Swedish Tax Agency (Skatteverket)
(<https://skatteverket.se/privat/skatter/beloppochprocent/2025.4.262c54c219391f2e96342eb.html>)

<span id="_Toc222502834" class="anchor"></span>**Table 2.21** Employer
social contributions – Persons older than 65 and born after 1937

|            **Year**             | **2022** | **2023** | **2024** | **2025** |
|:-------------------------------:|:--------:|:--------:|:--------:|----------|
| **Old age pension (tscerpi_s)** |  0.1021  |  0.1021  |  0.1021  | 0.1021   |

Source: The Swedish Tax Agency (Skatteverket)
(<https://skatteverket.se/privat/skatter/beloppochprocent/2025.4.262c54c219391f2e96342eb.html>)

<span id="_Toc222502835" class="anchor"></span>**Table 2.22** Employer
social contributions – Persons aged between 15 and 23

| **Year** | **2022** | **2023** | **2024** | **2025** |
|:--:|:--:|:--:|:--:|:--:|
| **Social Contribution Rate for 15** <sup>a</sup> **-18 Year Olds** | 0.1021<sup>b</sup> | 0.1021<sup>b</sup> | 0.3142 <sup>d</sup> | 0.3142 <sup>d</sup> |
| **Social Contribution Rate for 19-23 Year Olds** | 0.1973<sup>b</sup> | 0.3142<sup>b</sup> | 0.3142 <sup>d</sup> | 0.3142 <sup>d</sup> |
| **Social Contribution Rate for 19-23 Year Olds (during summer)** | 0.1021<sup>b</sup> | 0.3142<sup>c</sup> | 0.3142 <sup>d</sup> | 0.3142 <sup>d</sup> |

Notes:

a increased to 16 in 2023\
b up to 25,000 SEK per month, 31.42 % for all salaries above this level\
c Changed as of April 1st, 0.1973 for incomes up to 25,000 SEK until
March 31.\
d Exemption for younger people removed as of Jan 1st 2024.

Source: The Swedish Tax Agency (Skatteverket)
(<https://skatteverket.se/privat/skatter/beloppochprocent/2025.4.262c54c219391f2e96342eb.html>)

***COVID-19 Notes***

A temporary reduction of employer's contributions and the general
payroll tax was introduced between March 1st to June 30th, 2020.
Employers could request a reduction of employer's contributions for a
maximum of 30 of their employees, so that only the old-age pension
contribution (10.21 percent) on compensation up to 25,000 kronor per
payee and per month was paid.

**Self-employed social contributions(ils_sicse)**

#### Liability to contributions

The self-employed (lse \> 0) pay social contributions.

#### Income base used to calculate contributions

The social contribution is based on total self-employment income (yse)
if the annual amount is greater than 1,000 SEK (if below no contribution
is paid).

#### Contribution rates

There are 8 different self-employed social contributions: health
insurance, parental insurance, occupational injuries, old age pension,
survivors pension, labour market, general wage fee and a special wage
tax (for persons older than 66 years). The rates are specified in the
following tables. If the self-employed business activity can be
categorized as a passive business (i.e., if the individual does not
spend any work hours in the business), a special wage tax of 24,26% is
paid instead of the social contributions.

<span id="_Toc222502836" class="anchor"></span>**Table 2.23**
Self-employed social contributions – Persons younger than 67 year old

| **Year** | **2022 <sup>a</sup>** | **2023<sup>a,b</sup>** | **2024<sup>a</sup>** | **2025<sup>a</sup>** |
|----|:--:|:--:|:--:|:--:|
| **Health insurance (tscsesi_s)** | 0.0364 | 0.0364 | 0.0364 | 0.0364 |
| **Old age pension (tscsepi_s)** | 0.1021 | 0.1021 | 0.1021 | 0.1021 |
| **Survivors pension (tscseci_s)** | 0.0060 | 0.0060 | 0.0060 | 0.0060 |
| **Occupational injuries (tscseac_s)** | 0.0020 | 0.0020 | 0.0020 | 0.0020 |
| **Labour market (tscseir_s)** | 0.0010 | 0.0010 | 0.0010 | 0.0010 |
| **General wage fee (tscseot_s)** | 0.1162 | 0.1162 | 0.1162 | 0.1162 |
| **Parental insurance (tscseml_s)** | 0.0260 | 0.0260 | 0.0260 | 0.0260 |

Notes:

<sup>a</sup> In 2022, 2023 and 2024, and 2025 individuals who have a
full age pension or sometime during the current year has received full
disability pension only pay the old age pension contribution, i.e.
10,21% **\
<sup>b</sup>** In 2023, the age was increased to younger than 67 (from
younger than 66)

Source: The Swedish Tax Agency (Skatteverket)
(<https://skatteverket.se/privat/skatter/beloppochprocent/2025.4.262c54c219391f2e96342eb.html>)

<span id="_Toc222502837" class="anchor"></span>**Table 2.24**
Self-employed contributions – Persons older than 65 and born after
1937<sup>a</sup>

|             **Year**             | **2022** | **2023** | **2024** | **2025** |
|:--------------------------------:|:--------:|:--------:|:--------:|:--------:|
|             **Age**              |  66-84   |  67-85   |  67-85   |  67-85   |
| **Special wage tax (tscseot_s)** |    0     |    0     |    0     |    0     |
| **Old age pension (tscsepi_s)**  |  0.1021  |  0.1021  |  0.1021  |  0.1021  |

Note: <sup>a</sup> Individuals born 1937 or earlier pay no contribution

Source: The Swedish Tax Agency (Skatteverket)
(<https://skatteverket.se/privat/skatter/beloppochprocent/2025.4.262c54c219391f2e96342eb.html>)

<span id="_Toc222502838" class="anchor"></span>**Table 2.25**
Self-employed contributions – Persons older than 65 years

| **Year**                         | **2021** | **2022** | **2023** | **2024** |
|----------------------------------|:--------:|:--------:|:--------:|:--------:|
| **Special wage tax for elderly** |   0.0    |   0.0    |   0.0    |   0.0    |

Source: The Swedish Tax Agency (Skatteverket)
(<https://skatteverket.se/privat/skatter/beloppochprocent/2025.4.262c54c219391f2e96342eb.html>)

#### EUROMOD modelling 

***COVID-19 Notes***

For farmers and self-employed the proportion of net income to be paid as
social contribution fee was reduced for 2020 from 28.97% to 10.21% (they
will only pay the old age pension contribution). The reduction is valid
for net income up to SEK 100 000. Thus, for net income up to SEK 100 000
the social contribution percentage will be 10.21% and for net income
above SEK 100 000 the full social contribution fee will be paid.

## Personal income tax

The main tax simulated for Sweden is the personal income tax which is
divided into four parts: a government tax, a county council tax, a
municipality tax and a funeral tax. All individuals earning above 20 430
SEK in 2022 and 20 207 SEK in 2023, 24 237 SEK in 2024 and 24 872 SEK in
2025 (annually) pay taxes.

### Tax unit 

Personal income tax is assessed at individual level.

### Exemptions

Child benefits, social assistance, housing allowance, housing allowance
for pensioners and social assistance for elderly are exempted from
income tax. Those who earn less than 20 431 SEK in 2022 and 20 208 SEK
in 2023, 24 238 SEK in 2024 and 24 873 SEK in 2025 (annually) are exempt
from paying income tax.

### Taxable income

The taxable income (il_taxabley) includes: employment income (yem),
fringe benefits (kfb), self-employment income (yse), parental leave
benefit (bpl – parent’s allowance at birth), income received by children
(yot), Private pensions (ypp), Unemployment benefits (bunct + bunnc),
Old age pension (poa), Disability benefit (pdi), Sickness benefit (bhl)
and Survivor’ pension (psu).

There exist, however, additional minor tax-related incomes not simulated
in Euromod. For example, emoluments (*arvoden*), taxable student aid,
annuity, and taxable car and housing benefits.

### Tax allowances

Two tax allowances are simulated.

**Allowance for voluntary Private Pension contributions (tintapv_s).**

From 2016 and onwards, the allowance for voluntary private pension
contributions are only for self-employed.

#### EUROMOD modelling 

Due to lack of data, we do not simulate those rules which anyway affect
only 3 percent of those claiming the allowance (i.e. having a higher
value).

**Basic allowance (tinta00_s)**

The basic allowance (tinta00_s) is based on taxable income minus the
allowance for voluntary Private Pension (il_taxabley_ppta).

<span id="_Toc222502839" class="anchor"></span>**Table 2.26** Basic
Allowance - 2020-2025

<table style="width:62%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 10%" />
<col style="width: 38%" />
</colgroup>
<thead>
<tr>
<th colspan="2" style="text-align: center;"><strong>Taxable income minus
allowance for Private pension</strong></th>
<th style="text-align: center;"><strong>Allowance</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Lower level</strong></td>
<td style="text-align: center;"><strong>Upper level</strong></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td>0</td>
<td style="text-align: center;">0.99*XBASM</td>
<td style="text-align: center;">min (il_taxabley_ppta, 0.423*XBASM)</td>
</tr>
<tr>
<td>0.99*XBASM</td>
<td style="text-align: center;">2.72*XBASM</td>
<td style="text-align: center;">0.423*XBASM+0.2*(il_taxabley_ppta
-0.99*XBASM)</td>
</tr>
<tr>
<td>2.72*XBASM</td>
<td style="text-align: center;">3.11*XBASM</td>
<td style="text-align: center;">0.77*XBASM</td>
</tr>
<tr>
<td>3.11*XBASM</td>
<td style="text-align: center;">7.88*XBASM</td>
<td style="text-align: center;">0.77*XBASM-0.1*(il_taxabley_ppta
-3.11*XBASM)</td>
</tr>
<tr>
<td>7.88*XBASM</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">0.293*XBASM</td>
</tr>
</tbody>
</table>

Source: The Income Tax Law (<https://lagen.nu/1999:1229#A11>)

There is also an additional basic allowance for pensioners (65 years or
older when the tax year started until Jan 1st 2023, when it increased to
66 years or older) (tintape_s):

<span id="_Toc222502840" class="anchor"></span>**Table 2.27** Additional
Basic Allowance for pensioners (over 65 years) – 2022-2025

<table style="width:61%;">
<colgroup>
<col style="width: 13%" />
<col style="width: 11%" />
<col style="width: 35%" />
</colgroup>
<thead>
<tr>
<th colspan="3" style="text-align: center;"><strong>2022-2023 (age limit
changed to 66 in 2023)</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>0</td>
<td style="text-align: center;">0.91*XBASM</td>
<td style="text-align: center;">min (il_taxabley_ppta, 0.687*XBASM)</td>
</tr>
<tr>
<td>0.91*XBASM</td>
<td style="text-align: center;">1.11*XBASM</td>
<td style="text-align: center;">0.885*XBASM-0.2* il_taxabley_ppta</td>
</tr>
<tr>
<td>1.11*XBASM</td>
<td style="text-align: center;">1.965*XBASM</td>
<td style="text-align: center;">0.600*XBASM+0.057* il_taxabley_ppta</td>
</tr>
<tr>
<td>1.965*XBASM</td>
<td style="text-align: center;">2.72*XBASM</td>
<td style="text-align: center;">0.333*XBASM+0.1949*
il_taxabley_ppta</td>
</tr>
<tr>
<td>2.72*XBASM</td>
<td style="text-align: center;">3.11*XBASM</td>
<td style="text-align: center;">-0.212*XBASM+0.3949*
il_taxabley_ppta</td>
</tr>
<tr>
<td>3.11*XBASM</td>
<td style="text-align: center;">3.24*XBASM</td>
<td style="text-align: center;">-0.523*XBASM+0.4949*
il_taxabley_ppta</td>
</tr>
<tr>
<td>3.24*XBASM</td>
<td style="text-align: center;">5.53*XBASM</td>
<td style="text-align: center;">0.325*XBASM+0.233* il_taxabley_ppta</td>
</tr>
<tr>
<td>5.53*XBASM</td>
<td style="text-align: center;">7.88*XBASM</td>
<td style="text-align: center;">0.441*XBASM+0.212* il_taxabley_ppta</td>
</tr>
<tr>
<td>7.88*XBASM</td>
<td style="text-align: center;">8.08*XBASM</td>
<td style="text-align: center;">1,104*XBASM+0.128* il_taxabley_ppta</td>
</tr>
<tr>
<td>8.08*XBASM</td>
<td style="text-align: center;">11.48*XBASM</td>
<td style="text-align: center;">2.139*XBASM</td>
</tr>
<tr>
<td>11.48*XBASM</td>
<td style="text-align: center;">12.8*XBASM</td>
<td style="text-align: center;">9.257*XBASM-0.62* il_taxabley_ppta</td>
</tr>
<tr>
<td>12.8*XBASM</td>
<td style="text-align: center;">13.54*XBASM</td>
<td style="text-align: center;">1.32*XBASM</td>
</tr>
<tr>
<td>13.54*XBASM</td>
<td style="text-align: center;">35.54*XBASM</td>
<td style="text-align: center;">2.097*XBASM-0.574* il_taxabley_ppta</td>
</tr>
<tr>
<td>35.54*XBASM</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">0</td>
</tr>
<tr>
<td colspan="3"><strong>2024 (66 and over)</strong></td>
</tr>
<tr>
<td>0</td>
<td style="text-align: center;">0.91*XBASM</td>
<td style="text-align: center;">min (il_taxabley_ppta, 0.687*XBASM)</td>
</tr>
<tr>
<td>0.91*XBASM</td>
<td style="text-align: center;">1.11*XBASM</td>
<td style="text-align: center;">0.885*XBASM-0.2* il_taxabley_ppta</td>
</tr>
<tr>
<td>1.11*XBASM</td>
<td style="text-align: center;">1.965*XBASM</td>
<td style="text-align: center;">0.600*XBASM+0.057* il_taxabley_ppta</td>
</tr>
<tr>
<td>1.965*XBASM</td>
<td style="text-align: center;">2.72*XBASM</td>
<td style="text-align: center;">0.333*XBASM+0.1949*
il_taxabley_ppta</td>
</tr>
<tr>
<td>2.72*XBASM</td>
<td style="text-align: center;">3.11*XBASM</td>
<td style="text-align: center;">-0.212*XBASM+0.3949*
il_taxabley_ppta</td>
</tr>
<tr>
<td>3.11*XBASM</td>
<td style="text-align: center;">3.24*XBASM</td>
<td style="text-align: center;">-0.523*XBASM+0.4949*
il_taxabley_ppta</td>
</tr>
<tr>
<td>3.24*XBASM</td>
<td style="text-align: center;">5*XBASM</td>
<td style="text-align: center;">0.208*XBASM+0.2693*
il_taxabley_ppta</td>
</tr>
<tr>
<td>5*XBASM</td>
<td style="text-align: center;">7.88*XBASM</td>
<td style="text-align: center;">0.3*XBASM+0.2513* il_taxabley_ppta</td>
</tr>
<tr>
<td>7.88*XBASM</td>
<td style="text-align: center;">8.08*XBASM</td>
<td style="text-align: center;">0.986*XBASM+0.1643*
il_taxabley_ppta</td>
</tr>
<tr>
<td>8.08*XBASM</td>
<td style="text-align: center;">10.74*XBASM</td>
<td style="text-align: center;">2.313*XBASM</td>
</tr>
<tr>
<td>10.74*XBASM</td>
<td style="text-align: center;">12.16*XBASM</td>
<td style="text-align: center;">8.972*XBASM-0.62* il_taxabley_ppta</td>
</tr>
<tr>
<td>12.16*XBASM</td>
<td style="text-align: center;">13.54*XBASM</td>
<td style="text-align: center;">1.430*XBASM</td>
</tr>
<tr>
<td>13.54*XBASM</td>
<td style="text-align: center;">38.42*XBASM</td>
<td style="text-align: center;">2.206*XBASM-0.574* il_taxabley_ppta</td>
</tr>
<tr>
<td>38.42*XBASM</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">0</td>
</tr>
<tr>
<td></td>
<td colspan="2" style="text-align: center;"><strong>2025 (66 and
over)</strong></td>
</tr>
<tr>
<td>0</td>
<td style="text-align: center;">0.91*XBASM</td>
<td style="text-align: center;">min (il_taxabley_ppta, 0.687*XBASM)</td>
</tr>
<tr>
<td>0.91*XBASM</td>
<td style="text-align: center;">1.11*XBASM</td>
<td style="text-align: center;">0.885*XBASM-0.2* il_taxabley_ppta</td>
</tr>
<tr>
<td>1.11*XBASM</td>
<td style="text-align: center;">1.965*XBASM</td>
<td style="text-align: center;">0.600*XBASM+0.057* il_taxabley_ppta</td>
</tr>
<tr>
<td>1.965*XBASM</td>
<td style="text-align: center;">2.72*XBASM</td>
<td style="text-align: center;">0.333*XBASM+0.1949*
il_taxabley_ppta</td>
</tr>
<tr>
<td>2.72*XBASM</td>
<td style="text-align: center;">3.11*XBASM</td>
<td style="text-align: center;">-0.212*XBASM+0.3949*
il_taxabley_ppta</td>
</tr>
<tr>
<td>3.11*XBASM</td>
<td style="text-align: center;">3.24*XBASM</td>
<td style="text-align: center;">-0.523*XBASM+0.4949*
il_taxabley_ppta</td>
</tr>
<tr>
<td>3.24*XBASM</td>
<td style="text-align: center;">5*XBASM</td>
<td style="text-align: center;">0.096*XBASM+0.304* il_taxabley_ppta</td>
</tr>
<tr>
<td>5*XBASM</td>
<td style="text-align: center;">7.88*XBASM</td>
<td style="text-align: center;">0.186*XBASM+0.286* il_taxabley_ppta</td>
</tr>
<tr>
<td>7.88*XBASM</td>
<td style="text-align: center;">8.08*XBASM</td>
<td style="text-align: center;">0.872*XBASM+0.199* il_taxabley_ppta</td>
</tr>
<tr>
<td>8.08*XBASM</td>
<td style="text-align: center;">10.94*XBASM</td>
<td style="text-align: center;">2.48*XBASM</td>
</tr>
<tr>
<td>10.94*XBASM</td>
<td style="text-align: center;">12.47*XBASM</td>
<td style="text-align: center;">9.263*XBASM-0.62* il_taxabley_ppta</td>
</tr>
<tr>
<td>12.47*XBASM</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">1.532*XBASM</td>
</tr>
</tbody>
</table>

Source: The Income Tax Law (<https://lagen.nu/1999:1229#A11>)

### Tax base

The tax base (il_taxbase) is defined as taxable income minus the
allowance for voluntary private pension and the basic allowance.

### Tax schedule

The tax schedule for government tax (tinna_s), county council tax
(tinrg_s), municipality tax (tinmu_s) and funeral tax (tinfu_s) applies
to the same tax base (il_taxbase).

Tax rates differ by region in Sweden. In 2025 the county council tax
rate varies between 10.83% and 12.38 % of the tax base, the municipality
tax rate varies between 16.60 % and 23.80 % of the tax base. The funeral
tax rate is common to all municipalities since 2017, except for
Stockholm and Tranås, which have 0.07 % and 0.275 % of the tax base in
2024, respectively.

Since information on the region persons are living in is not included in
EUROMOD, the taxes are simulated according to the average value for
Sweden, as reported in the following table.

<span id="_Toc222502841" class="anchor"></span>**Table 2.28** Income tax
rates – 2022-2025

| **Year** | **Municipality tax** | **County council tax** | **Funeral tax** |
|:--------:|:--------------------:|:----------------------:|:---------------:|
| **2022** |        20.67%        |         11.56%         |     0.261%      |
| **2023** |        20.67%        |         11.57%         |     0.258%      |
| **2024** |        20.7%         |         11.67%         |     0.277%      |
| **2025** |        20.71%        |         11.69%         |     0.293%      |

Source: The Swedish Tax Agency (Skatteverket)
(<https://skatteverket.se/privat/skatter/beloppochprocent/2025.4.262c54c219391f2e96342eb.html>)

The government income tax schedule is based on three income bands as
reported in the following table. From 2020 the government income tax
only has two income bands, as seen below.

<span id="_Toc222502842" class="anchor"></span>**Table 2.29** Government
income tax schedule (after basic allowance) – 2022-2025

|      **Band**      | **Tax rate** | **2022**  | **2023**  | **2024**  | **2025**  |
|:------------------:|:------------:|:---------:|:---------:|:---------:|:---------:|
| **1<sup>st</sup>** |     0 %      | 0-540,700 | 0-598,500 | 0-598,500 | 0-625,500 |
| **2<sup>nd</sup>** |     20 %     | 540,701-  | 598,501-  | 598,501-  | 625,501-  |
| **3<sup>rd</sup>** |     25 %     |    N/A    |    N/A    |    N/A    |           |

Source: The Swedish Tax Agency (Skatteverket)
(<https://skatteverket.se/privat/skatter/beloppochprocent/2025.4.262c54c219391f2e96342eb.html>)

### Tax credits 

There are eight different non-refundable tax credits in the Swedish tax
system (the final tax liability cannot be negative). Here we report on
those we are able to simulate or impute. Five of the tax credits cannot
be simulated due to lack of data but are also presented below.

**Tax credit for general social security contributions**

The general social security contribution (see 2.3.1 – tscee_s) is 100 %
deductible from income tax.

**Tax credit for negative capital income**

This can be simulated for those who have a negative capital income (i.e.
the interests paid minus the sum of income from rent and capital
incomes, if the difference is positive) because of mortgage on their
house. All negative capital income due to other forms of mortgage cannot
be simulated [^4]. The annual amount of the tax credit (tintcmi_s) is:

0.30\* negative capital income \*12 if negative capital income \*12 \<
100,000

0.30\*100,000 + 0.21\*(negative capital income \*12-100,000) if negative
capital income \*12 \>= 100 000

**Earned Income Tax credit**

Depending on the age there are two different scales for the tax credit.

In both cases it is based on the income (tintc00_s) defined as follows:\
tintc00_s = yem + yse + kfb .

<span id="_Toc222502843" class="anchor"></span>**Table 2.30** Earned
Income Tax credit – 2022

<table style="width:65%;">
<colgroup>
<col style="width: 11%" />
<col style="width: 1%" />
<col style="width: 11%" />
<col style="width: 0%" />
<col style="width: 40%" />
</colgroup>
<thead>
<tr>
<th colspan="5"><strong>Persons younger than 66 years</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4">Annual Income base for tax credit</td>
<td></td>
</tr>
<tr>
<td colspan="2"><strong>Lower level</strong></td>
<td colspan="2"><strong>Upper level</strong></td>
<td><strong>Tax credit</strong></td>
</tr>
<tr>
<td colspan="2">0</td>
<td colspan="2">0.91*XBASM</td>
<td>(tintc00_s –BA<sup>a</sup>)*MT</td>
</tr>
<tr>
<td colspan="2">0.91*XBASM</td>
<td colspan="2">3.24*XBASM</td>
<td>(0.91*XBASM+0.3874*( tintc00_s -0.91*XBASM)-BA)*MT<sup>b</sup></td>
</tr>
<tr>
<td colspan="2">3.24*XBASM</td>
<td colspan="2">8.08*XBASM</td>
<td>(1.812*XBASM+0.128*( tintc00_s -3.24*XBASM)-BA)*MT</td>
</tr>
<tr>
<td colspan="2">8.08*XBASM</td>
<td colspan="2">13.54*XBASM</td>
<td>((2.432*XBASM)-BA)*MT</td>
</tr>
<tr>
<td colspan="2">13.54*XBASM</td>
<td colspan="2"></td>
<td>(((2.432*XBASM)-BA)*MT)-0.03*( tintc00_s-13.54*XBASM)</td>
</tr>
<tr>
<td colspan="5"><strong>Persons 66 years and older</strong></td>
</tr>
<tr>
<td colspan="3">Annual Income base for tax credit</td>
<td colspan="2"></td>
</tr>
<tr>
<td><strong>Lower level</strong></td>
<td colspan="2"><strong>Upper level</strong></td>
<td colspan="2"><strong>Tax credit</strong></td>
</tr>
<tr>
<td>0</td>
<td colspan="2">100,000 SEK</td>
<td colspan="2">0.2* tintc00_s</td>
</tr>
<tr>
<td>100,000 SEK</td>
<td colspan="2">300,000 SEK</td>
<td colspan="2">15,000+0.05* tintc00_s</td>
</tr>
<tr>
<td>300,000 SEK</td>
<td colspan="2">600,000 SEK</td>
<td colspan="2">30,000</td>
</tr>
<tr>
<td>600,000 SEK</td>
<td colspan="2"></td>
<td colspan="2">30,000-0.03*(* tintc00_s-600,000)</td>
</tr>
</tbody>
</table>

Notes:

<sup>a</sup> BA = Basic Allowance, see chapter 2.6.4

<sup>b</sup>MT = Municipality tax rate and County council tax rate

Source: The Swedish Tax Agency (Skatteverket)
(<https://www4.skatteverket.se/rattsligvagledning/2940.html>)

<span id="_Toc222502844" class="anchor"></span>**Table 2.31** Earned
Income Tax credit – 2023

<table style="width:65%;">
<colgroup>
<col style="width: 11%" />
<col style="width: 1%" />
<col style="width: 11%" />
<col style="width: 0%" />
<col style="width: 40%" />
</colgroup>
<thead>
<tr>
<th colspan="5"><strong>Persons younger than 66 years</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4">Annual Income base for tax credit</td>
<td></td>
</tr>
<tr>
<td colspan="2"><strong>Lower level</strong></td>
<td colspan="2"><strong>Upper level</strong></td>
<td><strong>Tax credit</strong></td>
</tr>
<tr>
<td colspan="2">0</td>
<td colspan="2">0.91*XBASM</td>
<td>(tintc00_s –BA)*MT</td>
</tr>
<tr>
<td colspan="2">0.91*XBASM</td>
<td colspan="2">3.24*XBASM</td>
<td>(0.91*XBASM+0.3874*( tintc00_s -0.91*XBASM)-BA)*MT</td>
</tr>
<tr>
<td colspan="2">3.24*XBASM</td>
<td colspan="2">8.08*XBASM</td>
<td>(1.812*XBASM+0.128*( tintc00_s -3.24*XBASM)-BA)*MT</td>
</tr>
<tr>
<td colspan="2">8.08*XBASM</td>
<td colspan="2">13.54*XBASM</td>
<td>((2.432*XBASM)-BA)*MT</td>
</tr>
<tr>
<td colspan="2">13.54*XBASM</td>
<td colspan="2"></td>
<td>(((2.432*XBASM)-BA)*MT)-0.03*( tintc00_s-13.54*XBASM)</td>
</tr>
<tr>
<td colspan="5"><strong>Persons 66 years and older</strong></td>
</tr>
<tr>
<td colspan="3">Annual Income base for tax credit</td>
<td colspan="2"></td>
</tr>
<tr>
<td><strong>Lower level</strong></td>
<td colspan="2"><strong>Upper level</strong></td>
<td colspan="2"><strong>Tax credit</strong></td>
</tr>
<tr>
<td>0</td>
<td colspan="2">100,000 SEK</td>
<td colspan="2">0.22* tintc00_s</td>
</tr>
<tr>
<td>100,000 SEK</td>
<td colspan="2">300,000 SEK</td>
<td colspan="2">15,000+0.07* tintc00_s</td>
</tr>
<tr>
<td>300,000 SEK</td>
<td colspan="2">600,000 SEK</td>
<td colspan="2">36,000</td>
</tr>
<tr>
<td>600,000 SEK</td>
<td colspan="2"></td>
<td colspan="2">36,000-0.03*(* tintc00_s-600,000)</td>
</tr>
</tbody>
</table>

Notes:

<sup>a</sup> BA = Basic Allowance, see chapter 2.6.4

<sup>b</sup>MT = Municipality tax rate and County council tax rate

Source: The Swedish Tax Agency (Skatteverket)
(<https://www4.skatteverket.se/rattsligvagledning/2940.html>)

<span id="_Toc222502845" class="anchor"></span>**Table 2.32** Earned
Income Tax credit – 2024

<table style="width:65%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 40%" />
</colgroup>
<thead>
<tr>
<th colspan="3"><strong>Persons younger than 66 years</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2">Annual Income base for tax credit</td>
<td></td>
</tr>
<tr>
<td><strong>Lower level</strong></td>
<td><strong>Upper level</strong></td>
<td><strong>Tax credit</strong></td>
</tr>
<tr>
<td>0</td>
<td>0.91*XBASM</td>
<td>(tintc00_s –BA)*MT</td>
</tr>
<tr>
<td>0.91*XBASM</td>
<td>3.24*XBASM</td>
<td>(0.91*XBASM+0.3874*( tintc00_s -0.91*XBASM)-BA)*MT</td>
</tr>
<tr>
<td>3.24*XBASM</td>
<td>8.08*XBASM</td>
<td>(1.813*XBASM+0.1643*( tintc00_s -3.24*XBASM)-BA)*MT</td>
</tr>
<tr>
<td>8.08*XBASM</td>
<td>13.54*XBASM</td>
<td>((2.608*XBASM)-BA)*MT</td>
</tr>
<tr>
<td>13.54*XBASM</td>
<td></td>
<td>(((2.608*XBASM)-BA)*MT)-0.03*( tintc00_s-13.54*XBASM)</td>
</tr>
<tr>
<td colspan="3"><strong>Persons 66 years and older</strong></td>
</tr>
<tr>
<td colspan="2">Annual Income base for tax credit</td>
<td></td>
</tr>
<tr>
<td><strong>Lower level</strong></td>
<td><strong>Upper level</strong></td>
<td><strong>Tax credit</strong></td>
</tr>
<tr>
<td>0</td>
<td>1.75*XBASM</td>
<td>0.22* tintc00_s</td>
</tr>
<tr>
<td>1.75*XBASM</td>
<td>5.24*XBASM</td>
<td>0.2635*XBASM+0.07*tintc00_s</td>
</tr>
<tr>
<td>5.24*XBASM</td>
<td>10.48*XBASM</td>
<td>0.6293*XBASM</td>
</tr>
<tr>
<td>10.48*XBASM</td>
<td></td>
<td>0.6293*XBASM -0.03*(tintc00_s-10.48*XBASM)</td>
</tr>
</tbody>
</table>

Notes:

<sup>a</sup> BA = Basic Allowance, see chapter 2.6.4

<sup>b</sup> MT = Municipality tax rate and County council tax rate

Source: The Swedish Tax Agency (Skatteverket)
(<https://www4.skatteverket.se/rattsligvagledning/2940.html>)

<span id="_Toc222502846" class="anchor"></span>**Table 2.33** Earned
Income Tax credit – 2025

<table style="width:65%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 11%" />
<col style="width: 0%" />
<col style="width: 40%" />
</colgroup>
<thead>
<tr>
<th colspan="4"><strong>Persons younger than 66 years</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2">Annual Income base for tax credit</td>
<td colspan="2"></td>
</tr>
<tr>
<td><strong>Lower level</strong></td>
<td><strong>Upper level</strong></td>
<td colspan="2"><strong>Tax credit</strong></td>
</tr>
<tr>
<td>0</td>
<td>0.91*XBASM</td>
<td colspan="2">(tintc00_s –BA)*MT</td>
</tr>
<tr>
<td>0.91*XBASM</td>
<td>3.24*XBASM</td>
<td colspan="2">(0.91*XBASM+0.3874*( tintc00_s -0.91*XBASM)-BA)*MT</td>
</tr>
<tr>
<td>3.24*XBASM</td>
<td>8.08*XBASM</td>
<td colspan="2">(1.813*XBASM+0.199*( tintc00_s -3.24*XBASM)-BA)*MT</td>
</tr>
<tr>
<td>8.08*XBASM</td>
<td></td>
<td colspan="2">((2.776*XBASM)-BA)*MT</td>
</tr>
<tr>
<td colspan="4"><strong>Persons 66 years and older</strong></td>
</tr>
<tr>
<td colspan="3">Annual Income base for tax credit</td>
<td></td>
</tr>
<tr>
<td><strong>Lower level</strong></td>
<td colspan="2"><strong>Upper level</strong></td>
<td><strong>Tax credit</strong></td>
</tr>
<tr>
<td>0</td>
<td colspan="2">1.75*XBASM</td>
<td>0.22* tintc00_s</td>
</tr>
<tr>
<td>1.75*XBASM</td>
<td colspan="2">5.24*XBASM</td>
<td>0.2635*XBASM+0.07* tintc00_s</td>
</tr>
<tr>
<td>5.24*XBASM</td>
<td colspan="2"></td>
<td>0.6293*XBASM</td>
</tr>
</tbody>
</table>

Notes:

<sup>a</sup> BA = Basic Allowance, see chapter 2.6.4

<sup>b</sup> MT = Municipality tax rate and County council tax rate

Source: The Swedish Tax Agency (Skatteverket)
(<https://www4.skatteverket.se/rattsligvagledning/2940.html>)

**Tax credit for persons with Disability pension
(Sjukersättning/aktivitetsersättning) (2022-2025).**

Since 2018, a person receiving disability pension (pdi\>0) is entitled
to disability tax credit under the following rules. The tax base is the
total amount of disability pension that was paid out during the year
(tax free benefits excluded). The basic allowance is not considered in
2020 and 2021, but in 2022 and 2023 it is. Exact thresholds and
calculations for the respective years are given below:

<span id="_Toc222502847" class="anchor"></span>**Table 2.34** Tax credit
for persons with Disability pension, 2022-2025

<table style="width:65%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 39%" />
</colgroup>
<thead>
<tr>
<th colspan="3"><strong>Persons younger than 66 years (65 for
2022)</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2">Annual disability pension base for tax credit</td>
<td></td>
</tr>
<tr>
<td><strong>Lower level</strong></td>
<td><strong>Upper level</strong></td>
<td><strong>Tax credit</strong></td>
</tr>
<tr>
<td>0</td>
<td>0.91*XBASM</td>
<td>(pdi –BA)*MT</td>
</tr>
<tr>
<td>0.91*XBASM</td>
<td>3.24*XBASM</td>
<td>((0.91*XBASM+0.3405*( pdi -0.91*XBASM))-BA)*MT</td>
</tr>
<tr>
<td>3.24*XBASM</td>
<td></td>
<td>((1.703*XBASM+0.128*( pdi -3.24*XBASM))-BA)*MT</td>
</tr>
</tbody>
</table>

Notes:

<sup>a</sup> BA = Basic Allowance, see chapter 2.6.4

<sup>b</sup> MT = Municipality tax rate and County council tax rate

Source: The Swedish Tax Agency (Skatteverket)
(<https://www4.skatteverket.se/rattsligvagledning/edition/2025.2/364206.html>)

**Due to lack of data, five tax credits cannot be simulated. However,
they are presented below and an overview of their total amounts is
reported in the Table below.**

**Tax credit on seafarer’s income**

A tax reduction is given for persons with seafarer’s income. The amount
is from 9,000 SEK to 14,000 SEK per year depending on if the ship is
sailing abroad or in Sweden.

**Tax credit on domestic and reconstruction services (2007-)**

The tax reduction is 30 percent of the labour cost for reconstruction
services and 50 percent of the labour cost for domestic services. There
is an upper limit for this reduction. For reconstruction services the
reduction is maximum 50,000 SEK per year. For domestic services the
reduction is maximum 75 000 SEK per year (implemented in 2021). The
total reduction is maximum 75 000 SEK per year since 2021 (in 2020 it
was 50 000 SEK, which could be divided freely between domestic and
reconstruction services).

After July 1st 2024, the credit was temporarily increased to 75 000 for
reconstruction services as well, and the total possible reduction was
increased to 150 000. This only pertains for spending done after July
1st, for spending done before this date the old limits still apply. Due
to this, the old limits are still used in EUROMOD for the whole of 2024.

At January 1st 2025, it was reverted back to the previous limits (75 000
SEK total maximum, 50 000 SEK maximum for reconstruction services), but
for spending made after May 12th, the reduction for reconstruction
services will temporarily be increased to 50% as well. Since this covers
more than half of the year, these limits are used in EUROMOD for the
whole of 2025.

**Tax credit for installation of ‘green technology’ (2021-2025)**

The tax credit will reduce labour and material costs for the
installation of various kinds of green technology, with varying rates of
the reduction. For installation of solar cells, the reduction is 20%
(15% 2021-2022), for storing self-produced electricity, the reduction is
50 %, for installation of charging points for electric vehicles, the
reduction is 50 %. The maximum reduction is 50 000 SEK per year.

**Tax credit on real estate tax**

Pensioners (persons older than 65 years) can receive a tax credit on
real estate tax so that this tax not exceeds four percent of the income.
The tax credit only refers to the property where the person is living.

##  Other taxes 

### Tax on capital income

The tax on capital is 30 % of the positive capital income, defined as
income from capital and property income minus interests paid. This can
partly be simulated as 0.30\*max(((yiy+ypr) -xhcmomi), 0). Other
interests paid, in addition to the interests paid on mortgage (xhcmomi),
are not recorded in the data and they cannot be taken into account.

### Tax on real estate

As from 2008 government property tax on dwellings was abolished and
replaced by a municipal property charge. The tax is applicable for
persons owning a ready-built house or a block of ready-built flats in
Sweden. Newly built houses are exempt from charge. For houses built 2011
or earlier, the property is not charged the first five years,
thereafter, half the normal rate applies for the five additional years.
Accordingly, first after 10 years are the properties fully charged. For
houses built 2012 or later, the property is not charged the first 15
years.

The table below describes the types of property mainly concerning
private persons. Tax on real estate is included in the SILC data
(EUROMOD variable: tpr).

<span id="_Toc222502848" class="anchor"></span>**Table 2.35** Tax on
real estate

| **Type of property** | **Municipal property charge 2009-2025** |
|----|:--:|
| House/land, 0-5 years, built 2011 or earlier | 0 |
| House/land, 6-10 years, , built 2011 or earlier | min((0.00375\* assessed value), (0.00375\*800,000\*KPIyear<sup>a</sup>)) |
| House/land older than 10 years, built 2011 or earlier | min((0.0075\*assessed value), (0.0075\*800,000\*KPIyear)) |
| House/land, 0-15 years, built 2012 or later | 0 |

Notes: <sup>a</sup>KPIyear = XBASMI/XBASMI 2008

Source: The Swedish Tax Agency (Skatteverket)
(<https://skatteverket.se/privat/skatter/beloppochprocent/2025.4.262c54c219391f2e96342eb.html>)

##  Consumption taxes 

Consumption taxes simulated in EUROMOD can be divided in two groups: VAT
(value added tax) and excises (additional duties paid over consumption,
typically on energy, alcoholic beverages, and tobacco).

Simulated consumption tax liabilities paid by households depend on the
tax rules (e.g. the VAT rate) and on the tax base (consumption
expenditures or quantities). This is why, to simulate consumption taxes
in EUROMOD, the input data must contain information on household
expenditures. The expenditures matched in the EUROMOD input files based
on SILC are reported directly by households in the HBS surveys at
purchasing prices. Therefore, they already include the consumption taxes
paid.

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

Further information on methodology and specific calculations and the
independence of these consumption taxes is common across countries (this
is why they are placed in an add-on and not in the policy spine of each
country) and can be found in Akoğuz et al (2020). [^5]

### VAT (il_tva)

<span id="_Toc222502849" class="anchor"></span>**Table 2.36** VAT rates
\[2022-2025\]

|  | Products | 2022 | 2023 | 2024 | 2025 |
|----|---:|:--:|:--:|:--:|:--:|
| Standard[^6] |  | 25% | 25% | 25% | 25% |
| Reduced | Mainly applies to food (inc. restaurant meals) and repair of clothes. | 12% | 12% | 12% | 12% |
| Super reduced | Mainly applies to public transport, culture, rent, medical services/pharmaceuticals and education. | 6% | 6% | 6% | 6% |
| Zero | These goods all goes on the exemptions below. | 0% | 0% | 0% | 0% |
| Exempted[^7] | Artistic performances, art, libraries, rental of privately owned property, certain medical services, certain financial and insurance services. | \- | \- | \- | \- |

Source: The Swedish Tax Agency (Skatteverket)
(<https://skatteverket.se/foretag/moms/saljavarorochtjanster/momssatserochundantagfranmoms.4.58d555751259e4d66168000409.html>)

### Ad-valorem excises (il_txv)

Ad-valorem excises only cover cigarettes in Sweden.

<span id="_Toc222502850" class="anchor"></span>**Table 2.37** Ad-valorem
excise rates \[2022-2025\]

| Products   | 2022 | 2023 | 2024 | 2025 |
|------------|:----:|:----:|:----:|:----:|
| Cigarettes |  1%  |  1%  |  1%  |  1%  |

Source: The Swedish Tax Agency (Skatteverket)
(<https://skatteverket.se/foretag/skatterochavdrag/punktskatter/tobaksskatt/skattesatserfortobak.4.46ae6b26141980f1e2d4664.html>)
)

### Tax credits 

Specific excises (il_txa)

Specific excises apply to alcohol, tobacco and energy products. In this
case, we collect both tax parameters and consumer prices, to allow the
model to estimate the implicit quantities behind the reported household
consumption expenditure amounts.

<span id="_Toc222502851" class="anchor"></span>**Table 2.38** Specific
(ad-quantum) excise rates (in SEK)

| Products | 2022 | 2023 | 2024 | 2025 |
|----|---:|---:|---:|---:|
| Ethyl alcohol (pure alcohol) | \- | 521.76/ L | 526.97 / L | 526.97 / L |
| Wine | \- | 9.65-57.53 / L | 6.19-37.34 /L | 10.38-61.90 /L |
| Beer |  | 2.12 / L | 2.28 / L | 2.28 / L |
| Cigarettes | \- | 1.78 / piece | 1.84 / piece | 2.06 / piece |
| Cigars/other tobacco | \- | 1.56-1.78 / piece | 1.62-2.24 / piece | 1.82-2.51/ piece |
| Electricity | \- | 3.92 SEK/MWh | 4.28 SEK/MWh | 4.39/MWh |
| Natural Gas | \- | 71-98.6 / Gj | 77.6 -107.8 / Gj | 80.8-112.3/ Gj |
| LPG | \- | 3.991 – 5.278 / kg | 4.363- 5.770 / kg | 4.544-6.1 / kg |
| Gas Oil | \- | 4.072 – 4.616 / L | 4.192 -4.797 / L | 4.28-4.922 / L |
| Heavy fuel oil | \- | 4.2863 / kg | 4.4126 / kg | 4.505 / kg |
| Kerosene | \- | 4.072 – 4.616 / L | 4.192 – 4.591 / L | 4.281-4.922 / L |
| Coal and Coke | \- | 128.3908 / Gj | 140.3356 / Gj | 146.19 / Gj |
| Petrol | \- | 4.010 – 7.350 / L | 4.560 – 6.750 / L | 4.490-5.150 / L |

Sources: The Swedish Tax Agency (Skatteverket)
(<https://skatteverket.se/foretag/skatterochavdrag/punktskatter/tobaksskatt/skattesatserfortobak.4.46ae6b26141980f1e2d4664.html>,
<https://skatteverket.se/foretag/skatterochavdrag/punktskatter/alkoholskatt/skattesatserforalkohol.4.4a47257e143e26725aecb5.html>,\
<https://skatteverket.se/foretag/skatterochavdrag/punktskatter/energiskatter/skattpabransle.4.15532c7b1442f256bae5e56.html>,\
<https://skatteverket.se/foretag/skatterochavdrag/punktskatter/energiskatter/skattpael.4.15532c7b1442f256bae5e4c.html>)

<span id="_Toc222502852" class="anchor"></span>**Table 2.39** Average
Prices of Excise Products (in SEK)

| Prices                         |        2024         | 2025<sup>n</sup>  |
|--------------------------------|:-------------------:|:-----------------:|
| Ethyl alcohol                  |     357.10 / L      |    399.14 / L     |
| Wine                           | 130.89 – 312.97 / L | 140.26-349.80 / L |
| Beer                           |      34.86 / L      |     36.15 / L     |
| Cigarettes                     |    3.16 / piece     |   3.39 / piece    |
| Cigars                         |    2.43 / piece     |   2.67 / piece    |
| Other tobacco                  |      4.54 / kg      |     4.53 / kg     |
| Electricty                     |     3007 / MWh      |        N/A        |
| Natural Gas - Heating          |    812.45 / MWh     |        N/A        |
| LPG - Heating                  |     48.04 / kg      |     51.8 / kg     |
| Gas Oil - Heating              |      15.12 / L      |        N/A        |
| Heavy fuel oil - Heating       |     123.9 / kg      |        N/A        |
| Kerosene- Heating              |         N/A         |        N/A        |
| Coal and Coke - Heating        |     826.92 / Gj     |    881.01 / Gj    |
| Petrol                         |  20.13 -22.92 / L   |        N/A        |
| LPG - Propellant               |     26.52 / kg      |        N/A        |
| Gas oil, Class1 - Propellant   |  23.06 - 23.22 / L  |        N/A        |
| Kerosene, Class 1 - Propellant |         N/A         |        N/A        |
| Natural Gas - Propellant       |       626.84        |        N/A        |

Source: EUROSTAT, provided by JRC Seville

Consumer prices of goods subject to excise duties are nowcasted,
similarly to what the model does to update incomes from SILC. We combine
the latest available data from the following sources:

Prices per product, usually from last year, but for instance, fuel
prices have only 15 days delay.

Inflation: Harmonised Index of Consumer Prices (HICP, Eurostat) at
COICOP 5 digits, usually for the first quarter for beta release and up
to third quarter 3 for final release.

Inflation quarter-on-quarter forecasts (DG ECFIN, confidential) by HICP
main groups (Unprocessed food, Processed food including alcohol and
tobacco, Non-energy industrial goods, Energy, Services - overall index
excluding goods) of quarters 2, 3 and 4, as needed for each release.

For more details on the specific source of the price of each good, see
Akoğuz et al (2020).

The price of (<u>indicate product</u>) did not followed this general
sources/nowcasting strategy but was sourced from (<u>indicate
source</u>) because (<u>indicate reason</u>).

**<u>EUROMOD modelling</u>**

Consumption taxes (tco_se policy) require extended EUROMOD input data
(with imputed income shares of consumption expenditures at the household
level) and an add-on to run. The policy is set to off in the baseline.
To activate it, the ITT_xbase add-on must be run, and the extended EM
input files (see Section 3 for more information on the methodology and
features behind these extended input files) should be selected (as
defined in the database configuration of each country). The other
add-ons (ITT\_\*) are designed for reform simulations and assume
different behavioural responses: i) constant quantities (ITT_XCQ), ii)
constant income shares (ITT_XCIS), and iii) constant expenditure shares
(ITT_XCES). These reform-scenario add-ons require the auxiliary output
files are generated by running the first baseline simulation (as either
the quantities or expenditures and savings from the baseline are kept
constants and enter as inputs in the simulated reform scenarios).

## Extraordinary measures

### COVID-19: Wage Compensation scheme COVID-19 (yemcomp_se)

This scheme allowed employers to reduce their employees' working hours
while the government compensated a significant portion of the lost
wages. The goal was to help companies retain their employees and avoid
layoffs during periods of reduced business activity. The government
covered a substantial part of the wage costs for the reduced hours,
while the employer and employee shared the remaining cost.

# Data

## General description

The Swedish database is drawn from the UDB version of the European
Statistics on Income and Living Conditions (EU-SILC). Every year a
systematic sample is drawn from the register of total population (TPR).
The reference population is therefore the whole Swedish population,
except short-term migrants (i.e. those staying no longer than 3-12
months). The sample design follows a stratified sample with simple
random sampling; before 2021 within age strata and from the collection
year 2021 by NUTS2 region, age and sex. The table below illustrates the
main characteristic for the 2020 sample. Up until the collection year of
2020, the SILC sample in a given year (say year *t*) consists of four
rotating panels: one is included for the first time in the same year
*t*, while the other three panels were originally drawn in years *t-1*,
*t-2* and *t-3*. As of the collection year 2021, the number of rotating
panels increased to five [^8]. In addition, there is an additional
cross-sectional sample, only taking part in the survey for one year, to
reach the desired cross-sectional sample size of 20 000 selected
respondents.

<span id="_Toc222502853" class="anchor"></span>**Table 3.1** EUROMOD
database description

| EUROMOD database | SE_2024_b1 |
|----|----|
| Original name | UDB C24_release_25_06 |
| Provider | EUROSTAT |
| Year of collection | 2024 |
| Period of collection | 2024.01.01—<span class="comment-start" id="97" author="Jonathan Stråle" date="2026-01-23T15:40:00Z">Not entirely sure of the exact period of collection. Perhaps it’s changed now that we do the data task in the fall?</span>2024<span class="comment-end" id="97"></span>.06.31 |
| Income reference period | 2023 |
| Sample size | 9,764 households, 23,765 individuals |
| Response rate | 49.0% |

Source: EU-SILC

The cross-sectional weighting procedure uses auxiliary information
through a calibration approach. The use of auxiliary information is
aimed to reduce nonresponse bias and to provide better estimates of
indicators of poverty measures. The auxiliary variables are obtained
from the total population register (TPR), the register of income and
taxation (IoT) and the register of education; and include age\*sex,
civil status, education level, region, place of birth (Swedish
born/foreign born), income deciles, income (amount), receipt of
financial aid, housing allowance and sickness compensation.

This section briefly describes the weighting procedure. [^9] The sample
unit of interest in the Swedish EU SILC are the households of sampled
individuals. More precisely, individuals are sampled in order to reach
households. In collection made before 2021, the sample is stratified by
age in eight strata: 16-24 years, 25-34 years, 35-44 years, 45-54 years,
55-64 years, 65-74 years, 75-84 years and 85 years and older. The sample
allocation was proportional. From 2021 and onwards, the sampling design
for new panel samples is stratified systematic sampling, in which
stratification is with respect to NUTS2 regions and where the sampling
frame is ordered by sex and age. The sampling allocation is
non-proportional, in which small NUTS2 regions are overrepresented, and
large NUTS2 regions are underrepresented. The purpose of the new
sampling design is to increase compliance with the precision
requirements for SILC.

The design weights of the initial sample (DB080) are given by the ratio
of the total number of individuals in each stratum to the number of
individuals in the sample in each stratum multiplied with the proportion
of selected respondents from the current panel in the cross-sectional
sample. In order to get the household weights (DB090), the design
weights (DB080) are calibrated to the population totals of the auxiliary
variables. All individuals in a household get the same value of the
household weights (DB090) and personal weights RB050 and PB040 are set
equal to DB090. In addition, calibration for the personal weights,
PB060, is made separately using totals for the population of selected
respondents.

##  Data adjustment 

Adjustments to variables are kept to a minimum. Some minor data cleaning
has been done to make sure that the households and relationships of
individuals within households are coherent (for example, that young
children are not living alone or family relations are coherent).

In order to guarantee consistency between demographic variables and
income variables which refer to the previous year (and on which EUROMOD
simulation are based), all children born between the end of the income
reference period and the date of interview have been dropped from the
sample.

## Imputations and assumptions

### Time period

In the SILC user database, the income reference period is a 12-month
period. Information on all income sources refers to the last income year
(1 January 2023 – 31 December 2023). The variables are recorded at the
time the person receives it, i.e. when the payment is done. This means
that the income of a person for example unemployed during the last part
of December 2022 but receiving the payment in January 2023, will then be
part of the income for 2023.

The other variables refer to the time of the interview or a 12 months
period prior to the interview.

Children born after the end of the income reference period (i.e. 31
December 2023) have been dropped from the dataset.

### Gross incomes

The incomes used are gross incomes.

### Disaggregation of harmonized variables

EU-SILC variable HY050g (Family/children related allowances) has been
split into two components: child benefit (bch00, simulated in EUROMOD as
bch00_s) and parent’s allowance at birth (bpl, not simulated in EUROMOD)
according to the rules about child benefits.

EU-SILC variable PY140g (Education related allowances) has been split
into two components: education related allowances (bed, non-simulated in
EUROMOD) and extra supplement of child benefit for upper secondary
school students (bchot, simulated in EUROMOD as bch01_s) according to
the year of birth of the individual (i.e. after 1986 is considered as
extra supplement).

## Updating

To account for any time inconsistencies between the input dataset and
the policy year, updating factors are used. Each monetary variable (i.e.
each income component) is updated so as to account for changes in the
non-simulated variables that have taken place between the year of the
data and the year of the simulated tax-benefit system. Updating factors
are generally based on changes in the average value of an income
component between the year of the data and the policy year. For detailed
information about the construction of each uprating factor as well as
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

Table 3.2 summarizes the major features of the most recent database used
to be run with the policy systems of 2021-2024.

<span id="_Toc222502854" class="anchor"></span>**Table 3.2** Extended
EUROMOD database description

| Extended EUROMOD database for the simulation of consumption taxes | SILC 2024 – Income year 2024 – Expenditures from HBS 2015 |
|----|----|
| EUROMOD database | SE_2024_b1_2015_03_e2 |
| Year of collection (HBS) and source | HBS 2015 – EU |
| Year of collection (SILC) and source | SILC 2024 – EU |
| Coverage and sample size | Same as SE_2024_b1 |
| Share of households with negative incomes excluded from the matching procedure | 0.5<span class="comment-start" id="106" author="Jonathan Stråle" date="2026-01-23T18:25:00Z">This I’m not sure where to find either</span>1<span class="comment-end" id="106"></span>% |
|  |  |

Notes: z: source of expenditure shares data with u (EU-HBS), e (EMSD) n
(national HBS), a (admin data)

M: version of matching (correlative number), f: source of SILC dataset
(National, UDB, ESMD): a, b or c 

N: version of SILC processing (correlative number) 

Source: EU-SILC

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

For the case of Sweden, data SE_2024_b1, the number of variables
included (income shares of expenditures, xs_c\*) are 193, corresponding
to the harmonized consumption categories defined at COICOP 2013 level 4
(five digits)

This database is an extension of the core EUROMOD input database, and so
it is based on the same sample (i.e., same identifiers "idperson" and
"idhh" to identify persons and households, respectively) and contains
the same variables plus the income shares of expenditure (xs\_\*
variables).

In Table 3.3 we present the share of households' consumption
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
checks for Sweden.

<span id="_Toc222502855" class="anchor"></span>**Table 3.3** Expenditure
coverage of Extended EM Input files

<table style="width:39%;">
<colgroup>
<col style="width: 15%" />
<col style="width: 22%" />
<col style="width: 1%" />
</colgroup>
<thead>
<tr>
<th>COICOP group</th>
<th style="text-align: right;">HBS 2015 – Extended EM Input 2024</th>
<th style="text-align: right;"></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>1</p>
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
<td style="text-align: right;"><p>96.5%</p>
<p>65.8%</p>
<p>69.9%</p>
<p>109.7%</p>
<p>82.3%</p>
<p>106.2%</p>
<p>94.1%</p>
<p>110.4%</p>
<p>99.75%</p>
<p>100.7%</p>
<p>94.6%</p></td>
<td style="text-align: right;"></td>
</tr>
<tr>
<td>Total</td>
<td style="text-align: right;"><strong>89.8%</strong></td>
<td style="text-align: right;"></td>
</tr>
</tbody>
</table>

Source: HBS

The macro validation for the **Extended EM Input 2024** dataset reveals
a total expenditure coverage of **89.8%** relative to the HBS 2015
benchmark. While the original 2015 SILC-HBS match was remarkably precise
at 101%, the transition to SILC 2022 introduced an overall
overestimation of **18%**. Necessities such as food (Group 1) align
closely at 96.5%, yet the data reflects the usual survey modesty: "vice"
categories like alcohol and tobacco (Group 2) are under-reported at
65.8%, whereas communication and education (Groups 8 and 10) show
significant overestimation, exceeding 110% and 100% respectively.

# Validation

## Aggregate Validation 

EUROMOD results are validated against external benchmarks. Detailed
comparisons of the number of people receiving a given income component
and total yearly amounts are shown in Annex 3. Both market incomes and
non-simulated taxes and benefits in the input dataset as well as
simulated taxes and benefits are validated against external official
data. The main discrepancies between EUROMOD results and external
benchmarks are discussed in the following subsections. Some factors that
may explain the observed differences are also discussed.

The macro-validation takes place compared to publicly published
aggregate statistics. This means that macro-level benchmarks are not
available for all (reported or simulated) indicators from the EUROMOD
model. Furthermore, it should be noted that there can be differences in
for instance sample or income definitions that are used in EUROMOD
compared to what is used for national reporting of macro-level
statistics in Sweden.

### Components of disposable income

The definition of disposable income in EUROMOD follows closely EU-SILC
definition. The minor differences are outlined in the following table.
Note that disposable income in EUROMOD is constructed using simulated
components whenever possible and, hence, the values of two disposable
income concepts are not identical.

**Table 4.1 Components of disposable income**

<table style="width:54%;">
<colgroup>
<col style="width: 30%" />
<col style="width: 11%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr>
<th></th>
<th style="text-align: center;"><p>EUROMOD</p>
<p>2022-2025</p></th>
<th style="text-align: center;"><p>EU-SILC</p>
<p>2024</p></th>
</tr>
</thead>
<tbody>
<tr>
<td></td>
<td style="text-align: center;">ils_dispy</td>
<td style="text-align: center;">HY020</td>
</tr>
<tr>
<td>Employee cash or near cash income</td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td>Employer's social insurance contribution</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">0</td>
</tr>
<tr>
<td><blockquote>
<p>Company car</p>
</blockquote></td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td>Contributions to individual private pension plans</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">0</td>
</tr>
<tr>
<td>Cash benefits or losses from self-employment</td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td>Pension from individual private plans</td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td><em>Unemployment benefits</em></td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td><em>Old-age benefits</em></td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td><em>Survivor’ benefits</em></td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td>Sickness benefits</td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td>Disability benefits</td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td>Education-related allowances</td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td>Income from rental of a property or land</td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td><em>Family/children related allowances</em></td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td>Social exclusion not elsewhere classified</td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td>Housing allowances</td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td>Regular inter-household cash transfer received</td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td>Interests, dividends, etc.</td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td>Income received by people aged under 16</td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
<tr>
<td>Regular taxes on wealth</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><em>Regular inter-household cash transfer paid</em></td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><em>Tax on income and social contributions</em></td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td><em>Repayments/receipts for tax adjustment</em></td>
<td style="text-align: center;">+</td>
<td style="text-align: center;">+</td>
</tr>
</tbody>
</table>

Source: Own elaboration.

### Validation of incomes inputted into the simulation

Information about income components from the underlying EUROMOD data
(Swedish component of EU-SILC) are compared to information on income
components (wages and various benefits) from Statistics Sweden. The
comparison needs to be done with caution because the units of analysis
and the exact income concepts in the survey and in the statistics are
not always strictly comparable. Table A3.1 compares the number of
recipients of different income components. The number of external
statistics that could be gathered w.r.t the number of tax beneficiaries
was limited, only recipients of income from employment was available.
The model slightly overestimates the number of employed individuals, but
not by much. For the aggregate amount of employment income, found in
Table A3.2, the model almost perfectly matches the external statistics
however.

### Validation of tax and benefit instruments 

Tables A3.3 and A3.4 report the validation of tax instruments and social
security contributions simulated in EUROMOD. Table A3.5 and A3.6 report
numbers and amounts of benefits receipt. We generally observe an
over-estimation of the number of benefit recipients. In 2024, this is
most notable for the health benefit, the housing allowances for
pensioners and the general housing allowance. In 2024, the health
benefit and housing allowances for pensioners overestimates the number
of recipients by more than 100%. The over-estimation is in-line with the
expectations and is likely to be related to the non-take-up of benefits.
For the survivors pensions however, we see a severe under-estimation of
the number of recipients. This might be due to assumptions made in the
model due to data scarcity. The latest available year for the
unemployment benefit is also under-estimated, in contrast with previous
years. This might be due to an unexpected increase in Swedish
unemployment that is not yet captured in the data used for the
simulation. In terms of aggregate amounts, the simulated health benefit
is much more precise however. Similar over-estimations are however found
for the amounts of the means tested benefits, and the above mentioned
under-estimations are also seen for the amounts, likely for similar
reasons.

In terms of personal income tax, we simulate: Government Tax, County
Council Tax, Municipality Tax, funeral tax and Earned Income Tax Credit,
but can only validate a limited number of these because of data
availability. Other Swedish taxes, such as the funeral tax of the
distinction between municipal and government income taxes, is not
available in the EUROMOD simulations. We were unable to get any reliable
data for the number of payers of the different taxes, but the available
external statistics for the aggregate amounts have on the other hand
been improved. The amount of direct taxes paid are underestimated. The
underestimations represent 38% for income taxes, 17% for property tax
and 61% for capital taxes in 2024.Data quality w.r.t financial assets
held by the households is most likely to explain the poor performance
w.r.t capital taxes.

The social security contributions for employees and employers seems to
perform well overall, except for a few notable outliers. The
self-employed labour market contributions are heavily over-estimated,
and self-employed sickness SIC and employer special wage tax are also
notably overestimated. We have as of now no clear explanation for these
discrepancies.

## Income distribution 

All income distribution results presented are computed for individuals
according to their household disposable income (HDI) equivalised by the
“modified OECD” equivalence scale. HDI are calculated as the sum of all
income sources of all household members net of income tax and social
insurance contributions. The weights in the OECD equivalence are: first
adult=1; additional people aged 14+ = 0.5; additional people aged under
14 = 0.3

### Income inequality

Table A3.7 shows the main inequality indices from EUROMOD and SILC. Gini
coefficient for Disposable income is underestimated in EUROMOD by 8
percentage points for 2023. Similarly the S80/20 ratio is underestimated
as well. Looking at the different income deciles, we see that compared
to external statistics we are overestimating the income for low-income
households, and underestimating it for the highest deciles, which
explains the underestimation of the Gini coefficient and S80/20 index.

###  Poverty rates 

The overall relative poverty rate based on disposable income simulated
in EUROMOD somewhat underestimates the one based on disposable income
reported in EU-SILC (Table A3.8 in Annex 3). The differences are larger
with the lowest poverty line (underestimation with 39% of median
equivalised household income) and in the case of elderly poverty. The
latter can be affected by the over-simulation of the housing allowances
and social assistance resulting in lower poverty rates simulated by
EUROMOD. [^10]

## Validation of minimum wage

Baseline simulations in EUROMOD do not modify gross employment income in
any way. However, the user may switch on a policy that ‘corrects’
employment income by ensuring it is not below the gross minimum wage
corresponding to the number of hours the person has worked. In the case
of Sweden; however, because there is no statutory minimum wage, the
default censoring minimum wage is set at 0 and therefore it does not
affect results in any way. The user might choose to modify this.

## Summary of “health warnings”

This final section summarises the main findings in terms of particular
aspects of the Swedish part of EUROMOD that should be borne in mind when
planning appropriate uses of the model and in interpreting the results.
In particular:

Some aggregated variables available in the survey are very difficult to
split without having access to the original source of data (in
particular, parents’ allowance at birth, income from capital and
property income)

The lack of information related to negative capital income (with the
exception of the interests paid on the mortgage for the main house) and
other expenditures affects the simulation of some tax credits

The identification of those subject to self-employment social
contributions is problematic as well as the correct definition of the
tax base of the self-employment social contributions

The assumption of 100% take-up of means-test benefit overestimates both
recipients and amount of these benefits.

The simulation of parental benefits is switched off in the baseline
(therefore, those observed in the data are used).

The simulation of monetary compensation schemes (bwkmcee_s and yemmc_s)
is triggered by the simulation of labour market transitions defined in
policy TransLMA_se. This policy becomes operational if the model is run
in conjunction with the LMA add-on. The nature of these simulations is
still experimental and only partially validated. Users are encouraged to
refer to the “*Simulating labour market transitions in EUROMOD*”
document prior to their use.

Labour market transitions are switched OFF in EUROMOD baselines. As a
consequence, the simulation of monetary compensation schemes does not
produce any effect in baseline simulations. Since all policies not
linked to labour market transitions are fully functional, it is possible
for disposable income in 2020 to be higher than disposable income in
previous years.

## Avenues for future improvements of the Swedish model in EUROMOD

The current national team made a number of improvements to the Swedish
model in EUROMOD after taking over in 2022. They have further identified
a number of possible improvements to the policy model that will require
more resources than currently available. An evaluation of the
anticipated improvement of the simulation, feasibility in terms of
input-information, and priorities is required, in addition to extensive
testing and evaluation after implementation. We record these suggestions
here.

**Income concepts IlsDef_se**

Identify why *Maintenance Payment* (4.1.10) is subtracted from Original
Income and if this is how it should be. Our reasoning is that this
procedure results in an income concept (and, by extension, poverty and
inequality indicators) that mix income and consumption/expenditure.

**Unemployment benefit (contributory)** **bunct_se**

Identify why the unemployment benefit (14.3.1) max-function has been
turned off and if it should be turned back on again.

**Parental benefit bfapl_se**

Consider assigning parental leave benefit (15.20) to the mother instead
of to the head of the household. Assigning it to the mother will be more
in line with how parental leave is divided in practice (irrespective of
who’s heading the household).

**Housing allowance bho_se**

The simulation of this policy calculates housing allowance for families
with cohabiting parents. 23.6 concerns ‘female partners’ and 23.7
concerns ‘male partners’. Consider making this gender neutral, i.e.
partner 1 and partner 2, irrespective of their sex/gender.

Consider allocating housing allowance on a monthly basis as opposed to
on an annual basis, as the amount in 23.9.1 was a temporary covid-19
related add-on paid out for the later half of 2020, 2021 and 2022.

**Housing allowance for pensioners bhope_se:**

Old-age pensioners and disability pensioners are included in the same
calculations. Consider separating the calculations, as these are in fact
two separate policies. Housing allowance for old-age pensioners is
managed by the Swedish Pension Agency (*Pensionsmyndigheten*), and the
housing allowance for disability pensioners is managed by the Swedish
Social Insurance Agency (*Försäkringskassan*).

**Social assistance bsamt_se**

We have included the additional amount received by 19-20-year-olds for
the years 2016-20. Identify whether the variable needs to be updated
also for years prior to 2016.

# References

EUROSTAT Statistics Database (2020).
<http://epp.eurostat.ec.europa.eu/portal/page/portal/statistics/search_database>

Statistics Sweden (2020) "National Reference Metadata in ESS Standard
for Quality Reports Structure”.
<https://circabc.europa.eu/faces/jsp/extension/wai/navigation/container.jsp>

## Sources for tax-benefit descriptions/rules

Vår trygghet 2009, Vår trygghet 2010, Vår trygghet 2011, Vår trygghet
2012.

Handledning för beskattning av inkomst vid 2009 års taxering Del 1,
Del2, Del 3

Handledning för beskattning av inkomst vid 2010 års taxering Del 1,
Del2, Del 3

# List of abbreviations and definitions 

| **Abbreviations** | **Definitions** |
|----|----|
| BA | Barnibedrag (Child Benefit) |
| BCA | Benefit Calibration Adjustment |
| BT | Bostadstillägg (Housing Supplement/Allowance) |
| BTA | Benefit Take-up Adjustment |
| CIA | Consumption Inflation Adjustment |
| COICOP | Classification Of Individual COnsumption according to Purpose |
| CPI | Consumer Price Index |
| CT | Consumption Taxes |
| DG | Directorate-General |
| DG ECFIN | European Commission Directorate-General for Economic and Financial Affairs |
| EEA | European Economic Area |
| EM | EUROMOD |
| DG EMPL | Directorate-General for Employment, Social Affairs and Inclusion |
| EMSD | EUROMOD SILC Database |
| ESS | Employment Service of Slovenia |
| ESTAT | Eurostat |
| EU | European Union |
| FASIT | Fördelningsanalytiskt system för inkomster och transfereringar |
| HBS | Household Budget Survey |
| HDI | Household Disposable Income |
| HICP | Harmonised Index of Consumer Prices |
| ISER | Institute for Social and Economic Research |
| JRC | Joint Research Centre |
| LMA | Labour Market Adjustment |
| LPG | Liquefied Petroleum Gas |
| MAX | Maximum |
| MIN | Minimum |
| MWA | Minimum Wage Adjustment |
| NRR | Net Replacement Rate |
| OECD | Organisation for Economic Co-operation and Development |
| PBE | Parental Leave Benefits |
| REFORM | European Commission Reform and Investment Task Force |
| SBT | Särskilt Bostadstillägg (Special Housing Supplement) |
| SCB | Statistiska centralbyrån (Statistics Sweden) |
| SEK | Svensk krona (Swedish Krona) |
| SG | Secretariat-General |
| SGI | Sjukpenninggrundande inkomst (Sickness Benefit Qualifying Income) |
| SIC | Social Insurance Contributions |
| SILC | Statistics on Income and Living Conditions |
| DG TAXUD | European Commission Directorate-General for Taxation and Customs |
| TPR | Totalbefolkningsregistret (Total Population Register) |
| UDB | User Database |
| UI | Unemployment insurance |
| VAB | Vård av barn (Temporary benefit for care of a child) |
| VAT | Value Added Tax |
| XBASM | Price Base Amount |
| XBASMI | Income Base Amount |

# List of figures

[**Figure A2.1**: Policy effects in 2024-2025, using the CPI-indexation
[75](#_Toc222502807)](#_Toc222502807)

# List of tables

[**Table 2.1** Simulation of benefits in EUROMOD
[15](#_Toc222502814)](#_Toc222502814)

[**Table 2.2** Simulation of taxes and social contributions in EUROMOD
[15](#_Toc222502815)](#_Toc222502815)

[**Table 2.3** EUROMOD Spine: order of simulation
[16](#_Toc222502816)](#_Toc222502816)

[**Table 2.4** Annual Base amounts [17](#_Toc222502817)](#_Toc222502817)

[**Table 2.5** Unemployment benefits 2021-September 30th 2025
[20](#_Toc222502818)](#_Toc222502818)

[**Table 2.6** Unemployment benefits October 1st 2025 and onwards
[21](#_Toc222502819)](#_Toc222502819)

[**Table 2.7** Characteristics of the unemployment benefit
[21](#_Toc222502820)](#_Toc222502820)

[**Table 2.8** Child benefit monthly amounts – 2020-2025
[24](#_Toc222502821)](#_Toc222502821)

[**Table 2.9** Housing allowance – Thresholds 2020-2025
[26](#_Toc222502822)](#_Toc222502822)

[**Table 2.10** Housing allowance parameters – Families with children –
2021- 2025 [27](#_Toc222502823)](#_Toc222502823)

[**Table 2.11** Housing allowance parameters – Families with children
with both permanent and alternating housholds– 2021-2025
[27](#_Toc222502824)](#_Toc222502824)

[**Table 2.12** Housing allowance parameters – Young couples without
children – 2016- 2025 [28](#_Toc222502825)](#_Toc222502825)

[**Table 2.13** Housing allowance for pensioners – Reserved amount –
2021-2025 [29](#_Toc222502826)](#_Toc222502826)

[**Table 2.14** Housing allowance for pensioners – Maximum housing costs
limits and total coverage at maximum limit– 2021-2025
[31](#_Toc222502827)](#_Toc222502827)

[**Table 2.15** Housing allowance for pensioners – Thresholds and
marginal coverage – 2020-2025 [32](#_Toc222502828)](#_Toc222502828)

[**Table 2.16** Housing allowance for disable pensioners – Amounts –
2020-2025 [32](#_Toc222502829)](#_Toc222502829)

[**Table 2.17** Housing allowance for old-age pensioners – Amounts –
2020-2025 [32](#_Toc222502830)](#_Toc222502830)

[**Table 2.18** Personal needs – Monthly amounts (SEK) – 2020-2024
[33](#_Toc222502831)](#_Toc222502831)

[**Table 2.19** Common needs – Monthly amounts (SEK) – 2020-2024
[34](#_Toc222502832)](#_Toc222502832)

[**Table 2.20** Employer social contributions – Persons younger than 66
years old [38](#_Toc222502833)](#_Toc222502833)

[**Table 2.21** Employer social contributions – Persons older than 65
and born after 1937 [38](#_Toc222502834)](#_Toc222502834)

[**Table 2.22** Employer social contributions – Persons aged between 15
and 23 [39](#_Toc222502835)](#_Toc222502835)

[**Table 2.23** Self-employed social contributions – Persons younger
than 67 year old [40](#_Toc222502836)](#_Toc222502836)

[**Table 2.24** Self-employed contributions – Persons older than 65 and
born after 1937<sup>a</sup> [40](#_Toc222502837)](#_Toc222502837)

[**Table 2.25** Self-employed contributions – Persons older than 65
years [40](#_Toc222502838)](#_Toc222502838)

[**Table 2.26** Basic Allowance - 2020-2025
[42](#_Toc222502839)](#_Toc222502839)

[**Table 2.27** Additional Basic Allowance for pensioners (over 65
years) – 2022-2025 [42](#_Toc222502840)](#_Toc222502840)

[**Table 2.28** Income tax rates – 2022-2025
[44](#_Toc222502841)](#_Toc222502841)

[**Table 2.29** Government income tax schedule (after basic allowance) –
2022-2025 [44](#_Toc222502842)](#_Toc222502842)

[**Table 2.30** Earned Income Tax credit – 2022
[45](#_Toc222502843)](#_Toc222502843)

[**Table 2.31** Earned Income Tax credit – 2023
[46](#_Toc222502844)](#_Toc222502844)

[**Table 2.32** Earned Income Tax credit – 2024
[47](#_Toc222502845)](#_Toc222502845)

[**Table 2.33** Earned Income Tax credit – 2025
[47](#_Toc222502846)](#_Toc222502846)

[**Table 2.34** Tax credit for persons with Disability pension,
2022-2025 [48](#_Toc222502847)](#_Toc222502847)

[**Table 2.35** Tax on real estate [50](#_Toc222502848)](#_Toc222502848)

[**Table 2.36** VAT rates \[2022-2025\]
[51](#_Toc222502849)](#_Toc222502849)

[**Table 2.37** Ad-valorem excise rates \[2022-2025\]
[51](#_Toc222502850)](#_Toc222502850)

[**Table 2.38** Specific (ad-quantum) excise rates (in SEK)
[52](#_Toc222502851)](#_Toc222502851)

[**Table 2.39** Average Prices of Excise Products (in SEK)
[52](#_Toc222502852)](#_Toc222502852)

[**Table 3.1** EUROMOD database description
[55](#_Toc222502853)](#_Toc222502853)

[**Table 3.2** Extended EUROMOD database description
[57](#_Toc222502854)](#_Toc222502854)

[**Table 3.3** Expenditure coverage of Extended EM Input files
[58](#_Toc222502855)](#_Toc222502855)

[**Table A1.1** Uprating Factors [72](#_Toc222502856)](#_Toc222502856)

[**Table A2.1** Policy effects in 2024-2025
[74](#_Toc222502857)](#_Toc222502857)

[**Table A3.1** Validation Tables [76](#_Toc222502858)](#_Toc222502858)

# List of Annexes

## Annex 1. Uprating Factors 

<span id="_Toc222502856" class="anchor"></span>**Table A1.1** Uprating
Factors

<table>
<colgroup>
<col style="width: 6%" />
<col style="width: 5%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 61%" />
</colgroup>
<thead>
<tr>
<th><strong>Variable name</strong></th>
<th><strong>Factor reference name</strong></th>
<th style="text-align: center;"><strong>2020</strong></th>
<th style="text-align: center;"><strong>2021</strong></th>
<th style="text-align: center;"><strong>2022</strong></th>
<th style="text-align: center;"><strong>2023</strong></th>
<th style="text-align: center;"><strong>2024</strong></th>
<th style="text-align: center;"><strong>2025</strong></th>
<th><strong>Source and explanation</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Harmonized consumer price index (index 2015=100)</td>
<td>$HICP</td>
<td style="text-align: center;">107.63</td>
<td style="text-align: center;">110.49</td>
<td style="text-align: center;">119.39</td>
<td>126.44</td>
<td>128.76</td>
<td style="text-align: center;">131.96</td>
<td><p>EUROSTAT; the values of 2024 is based on values in September</p>
<p><a
href="https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_midx/default/table?lang=en&amp;category=prc.prc_hicp">https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_midx/default/table?lang=en&amp;category=prc.prc_hicp</a></p></td>
</tr>
<tr>
<td>Consumer price index</td>
<td>$f_cpi</td>
<td style="text-align: center;">335.92</td>
<td style="text-align: center;">343.19</td>
<td style="text-align: center;">371.91</td>
<td>403.70</td>
<td>416.71</td>
<td style="text-align: center;">419.35</td>
<td><p>SCB; The values of 2025 is based on values in October (1980 =
100)</p>
<p><a
href="https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__PR__PR0101__PR0101A/KPItotM/">https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__PR__PR0101__PR0101A/KPItotM/</a></p></td>
</tr>
<tr>
<td>HICP - actual rentals for housing (index 2015=100)</td>
<td>$f_house</td>
<td style="text-align: center;">104.69</td>
<td style="text-align: center;">106.61</td>
<td style="text-align: center;">108.16</td>
<td>113.80</td>
<td>119.18</td>
<td style="text-align: center;">126.01</td>
<td><p>Eurostat;</p>
<p><a
href="https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_aind__custom_13540745/default/table?lang=en">https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_aind__custom_13540745/default/table?lang=en</a>
(annual) <a
href="https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_midx__custom_13540822/default/table?lang=en">https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_midx__custom_13540822/default/table?lang=en</a>
(monthly, for 2025)</p></td>
</tr>
<tr>
<td>Average monthly salary, SEK</td>
<td>$f_wage</td>
<td style="text-align: center;">34700</td>
<td style="text-align: center;">35600</td>
<td style="text-align: center;">36800</td>
<td>38300</td>
<td>39900</td>
<td style="text-align: center;"></td>
<td><a
href="https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__AM__AM0110__AM0110C/LonSNIKonN/table/tableViewLayout1/">https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__AM__AM0110__AM0110C/LonSNIKonN/table/tableViewLayout1/</a>
(no figures for 2025 yet)</td>
</tr>
<tr>
<td>Hourly wage, SEK</td>
<td>$f_xlon</td>
<td style="text-align: center;">267.7</td>
<td style="text-align: center;">276.4</td>
<td style="text-align: center;">285.3</td>
<td>294.7</td>
<td>306.2</td>
<td style="text-align: center;">317.6</td>
<td><a
href="http://prognos.konj.se/PXWeb/pxweb/sv/SenastePrognosen/SenastePrognosen__f30_lonerochkonsumentpriser/F3004.px/table/tableViewLayout1/?rxid=265ee5d8-b549-41b2-81aa-5cecea3bf826">http://prognos.konj.se/PXWeb/pxweb/sv/SenastePrognosen/SenastePrognosen__f30_lonerochkonsumentpriser/F3004.px/table/tableViewLayout1/?rxid=265ee5d8-b549-41b2-81aa-5cecea3bf826</a>
(value for 2025 is a prediction).</td>
</tr>
<tr>
<td>5 amount</td>
<td>$f_xbasm</td>
<td style="text-align: center;">47300</td>
<td style="text-align: center;">47600</td>
<td style="text-align: center;">48300</td>
<td>52500</td>
<td style="text-align: center;">57300</td>
<td style="text-align: center;">58800</td>
<td><a
href="http://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__PR__PR0101__PR0101E/Basbeloppet/?rxid=1df81ffb-6943-4796-a5d5-4b5e900d58b3">http://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__PR__PR0101__PR0101E/Basbeloppet/?rxid=1df81ffb-6943-4796-a5d5-4b5e900d58b3</a></td>
</tr>
<tr>
<td>Income base amount</td>
<td>$f_xbasmi</td>
<td style="text-align: center;">66800</td>
<td style="text-align: center;">68200</td>
<td style="text-align: center;">71000</td>
<td>74300</td>
<td>76200</td>
<td style="text-align: center;">80600</td>
<td><a
href="https://www.regeringen.se/artiklar/2024/11/inkomstbasbelopp-och-inkomstindex-for-ar-2025-faststallt/">https://www.regeringen.se/artiklar/2024/11/inkomstbasbelopp-och-inkomstindex-for-ar-2025-faststallt/</a></td>
</tr>
<tr>
<td>Aggregate income from capital, millions of SEK</td>
<td>$f_yiy</td>
<td style="text-align: center;">141530</td>
<td style="text-align: center;">141052</td>
<td style="text-align: center;"></td>
<td style="text-align: center;">146600</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td>Forecast made by the FASIT model for 2020 and 2021. 2023 figure from
this source: <a
href="https://www.scb.se/hitta-statistik/statistik-efter-amne/hushallens-ekonomi/hushallens-inkomster-tillgangar-och-skulder/inkomster-och-skatter/#_Tabellerochdiagram">https://www.scb.se/hitta-statistik/statistik-efter-amne/hushallens-ekonomi/hushallens-inkomster-tillgangar-och-skulder/inkomster-och-skatter/#_Tabellerochdiagram</a></td>
</tr>
<tr>
<td>Aggregate income from property, millions of SEK</td>
<td>$f_ypr</td>
<td style="text-align: center;">2469</td>
<td style="text-align: center;">2515</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td>Forecast made by the FASIT model</td>
</tr>
<tr>
<td>Unit index</td>
<td>$f_unit</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">1</td>
<td>1</td>
<td>1</td>
<td style="text-align: center;">1</td>
<td></td>
</tr>
<tr>
<td>Pension Index (new)</td>
<td>$f_pen</td>
<td style="text-align: center;">182.58</td>
<td style="text-align: center;">186.52</td>
<td style="text-align: center;">194.19</td>
<td>203.13</td>
<td>208.41</td>
<td style="text-align: center;">220.23</td>
<td><a
href="https://www.regeringen.se/artiklar/2023/11/inkomstbasbelopp-och-inkomstindex-for-ar-2024-faststallt/">https://www.regeringen.se/artiklar/2023/11/inkomstbasbelopp-och-inkomstindex-for-ar-2024-faststallt/</a></td>
</tr>
</tbody>
</table>

Source: See last column of table for specific sources.

## Annex 2. Policy Effects in 2024-2025

*Preliminary: Indexation based on projected HICP for 2025*

Table A2.1 and Figure A2.1 show the effect of 2025 policies on mean
equivalised household disposable income by income component and income
decile group. The effect is estimated as a difference between simulated
household net income under the 2024 tax-benefit policies (deflating
monetary parameters by projected Harmonized Index of Consumer Prices,
HICP) and net incomes simulated under 2025 policies, as a percentage of
mean equivalised household disposable income in 2024.

In comparison to 2024 policies, (deflated) 2025 policies increase mean
household income by 1.72% in total. The increase is mostly regressive
with lower income deciles seeing a lower increase than the higher ones.
The main drivers of this impact are an increase in public pensions and a
decrease in direct taxes.

<span id="_Toc222502857" class="anchor"></span>**Table A2.1** Policy
effects in 2024-2025

| **Original income** | **Public pensions** | **Means-tested benefits** | **Non means- tested benefits** | **Employee SIC** | **Self-employed SIC** | **Other SIC** | **Direct taxes** | **Disposable income** |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 0.00 | 0.39 | -1.02 | -0.52 | 0.00 | 0.00 | 0.00 | 0.38 | -0.79 |
| 0.00 | 1.07 | -0.65 | -0.20 | 0.00 | 0.00 | 0.00 | 0.06 | 0.29 |
| 0.00 | 1.70 | -0.61 | -0.10 | -0.01 | 0.00 | 0.00 | 0.14 | 1.11 |
| 0.00 | 1.09 | -0.06 | -0.12 | -0.02 | 0.00 | 0.00 | 0.44 | 1.33 |
| 0.00 | 0.84 | -0.03 | -0.08 | -0.03 | 0.00 | 0.00 | 0.59 | 1.31 |
| 0.00 | 0.74 | -0.02 | -0.07 | -0.04 | 0.00 | 0.00 | 1.03 | 1.64 |
| 0.00 | 0.69 | -0.01 | -0.05 | -0.05 | 0.00 | 0.00 | 1.44 | 2.02 |
| 0.00 | 0.61 | -0.01 | -0.04 | -0.06 | 0.00 | 0.00 | 1.65 | 2.15 |
| 0.00 | 0.53 | -0.01 | -0.02 | -0.09 | 0.00 | 0.00 | 1.73 | 2.14 |
| 0.00 | 0.42 | 0.00 | -0.02 | -0.12 | 0.00 | 0.00 | 2.08 | 2.36 |
| **0.00** | **0.73** | **-0.12** | **-0.08** | **-0.06** | **0.00** | **0.00** | **1.25** | **1.72** |

Notes: shown as a percentage change in mean equivalised household
disposable income by income component and income decile group. Income
decile groups are based on equivalised household disposable income in
2023 using the modified OECD equivalence scale. Each policy system has
been applied to the same input data, deflating monetary parameters of
2024 policies by Eurostat’s Harmonized Index of Consumer Prices (HICP).

Source: Own elaboration.

<span id="_Toc222502807" class="anchor"></span>**Figure A2.1**: Policy
effects in 2024-2025, using the CPI-indexation

Source: Own elaboration.

## Annex 3. Validation Tables

<span id="_Toc222502858" class="anchor"></span>**Table A3.1** Validation
Tables

[^1]: The way it operates in practice may vary across regions and by
    other characteristics.

[^2]: Policy switches are denoted with ‘switch’ in the policy spine (for
    a given policy year), while their default values (*on* or *off*) are
    set in a separate dialogue box in the model.

[^3]: This change was implemented as of July 1<sup>st</sup> 2024, which
    also set the birth-date threshold to April 1<sup>st</sup> 2023 as
    the shared days must be used in the first 15 months since the
    child’s birth.

[^4]: Starting 2025, interest on loans without security is only
    deductible by 50% and in 2026 this type of interest that is paid
    will not be deductible at all.

[^5]: Akoğuz, Elif Cansu, Bart Capéau, André Decoster, Liebrecht De
    Sadeleer, Duygu Güner, Kostas Manios, Alari Paulus, and Toon
    Vanheukelom. A new indirect tax tool for EUROMOD: final report.
    Technical Report, https://euromod-web. jrc. ec. europa.
    eu/sites/default/files/2021-03/A% 20new% 20indirect% 20tax% 20tool%
    20for% 20EUROMOD% 20Final% 20Report. pdf, 2020.

[^6]: Reduced rates for specific territories in AT, EL, ES, FR and IT
    are not modelled yet.

[^7]: Only country specific exemptions

[^8]: As of collection year 2022, the number of panels will increase to
    6.

[^9]: For more information see the Quality Report EU-SILC Sweden,
    available from:
    <https://www.gesis.org/en/missy/materials/EU-SILC/documents/quality-reports>

[^10]: When self-reported Housing allowance and Social assistance are
    used instead of the simulated amounts, the difference between
    EUROMOD and SILC poverty rates for the elderly are considerably
    reduced.
