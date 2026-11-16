Cover

Contents

[Abstract [4](#_Toc222326495)](#_Toc222326495)

[Acknowledgements [5](#_Toc222326496)](#_Toc222326496)

[Authors [5](#_Toc222326497)](#_Toc222326497)

[1. Introduction [6](#introduction)](#introduction)

[1.1. Basic information about the tax-benefit system
[6](#basic-information-about-the-tax-benefit-system)](#basic-information-about-the-tax-benefit-system)

[1.2. Minimum Wage [7](#minimum-wage)](#minimum-wage)

[1.3. Social Benefits [8](#social-benefits)](#social-benefits)

[1.3.1. Contributory insurance-based benefits
[8](#contributory-insurance-based-benefits)](#contributory-insurance-based-benefits)

[1.3.2. Non-contributory social benefits
[10](#non-contributory-social-benefits)](#non-contributory-social-benefits)

[1.4. Social insurance contributions
[11](#social-insurance-contributions)](#social-insurance-contributions)

[1.5. Taxes [13](#taxes)](#taxes)

[2. Simulation of taxes, Social Insurance Contributions and benefits in
Euromod
[14](#simulation-of-taxes-social-insurance-contributions-and-benefits-in-euromod)](#simulation-of-taxes-social-insurance-contributions-and-benefits-in-euromod)

[2.1. Scope of simulation
[14](#scope-of-simulation)](#scope-of-simulation)

[2.2. Partially simulated tax-benefit components
[14](#partially-simulated-tax-benefit-components)](#partially-simulated-tax-benefit-components)

[2.3. Main policy changes
[19](#main-policy-changes)](#main-policy-changes)

[2.4. Order of simulations and interdependence
[19](#order-of-simulations-and-interdependence)](#order-of-simulations-and-interdependence)

[2.5. Policy extensions [21](#policy-extensions)](#policy-extensions)

[2.6. Benefits [23](#benefits)](#benefits)

[2.6.1. Unemployment benefit/Επίδομα ανεργίας (bunct_cy)
[23](#unemployment-benefitεπίδομα-ανεργίας-bunct_cy)](#unemployment-benefitεπίδομα-ανεργίας-bunct_cy)

[2.6.2. Child benefit/Επίδομα Τέκνου (bch_cy)
[26](#child-benefitεπίδομα-τέκνου-bch_cy)](#child-benefitεπίδομα-τέκνου-bch_cy)

[2.6.3. Single-parent benefit/Επίδομα μονογονεϊκής οικογένειας
(bchlp_cy)
[27](#single-parent-benefitεπίδομα-μονογονεϊκής-οικογένειας-bchlp_cy)](#single-parent-benefitεπίδομα-μονογονεϊκής-οικογένειας-bchlp_cy)

[2.6.4. Student grant/Φοιτητική χορηγία (bedet_cy)
[28](#student-grantφοιτητική-χορηγία-bedet_cy)](#student-grantφοιτητική-χορηγία-bedet_cy)

[2.6.5. Standard birth grant/Βοήθημα Τοκετού (bchba_cy)
[31](#standard-birth-grantβοήθημα-τοκετού-bchba_cy)](#standard-birth-grantβοήθημα-τοκετού-bchba_cy)

[2.6.6. Special birth grant for unmarried mothers/Ειδικό βοήθημα τοκετού
σε άγαμες μητέρες (bchba_cy)
[32](#special-birth-grant-for-unmarried-mothersειδικό-βοήθημα-τοκετού-σε-άγαμες-μητέρες-bchba_cy)](#special-birth-grant-for-unmarried-mothersειδικό-βοήθημα-τοκετού-σε-άγαμες-μητέρες-bchba_cy)

[2.6.7. Maternity allowance /Επίδομα μητρότητας, (bmact_cy)
[32](#maternity-allowance-επίδομα-μητρότητας-bmact_cy)](#maternity-allowance-επίδομα-μητρότητας-bmact_cy)

[2.6.8. Paternity allowance /Επίδομα πατρότητας (bpact_cy)
[33](#paternity-allowance-επίδομα-πατρότητας-bpact_cy)](#paternity-allowance-επίδομα-πατρότητας-bpact_cy)

[2.6.9. Guaranteed Minimum Income/Ελάχιστο Εγγυημένο Εισόδημα (bsamm_cy)
[34](#guaranteed-minimum-incomeελάχιστο-εγγυημένο-εισόδημα-bsamm_cy)](#guaranteed-minimum-incomeελάχιστο-εγγυημένο-εισόδημα-bsamm_cy)

[2.6.10. Low pension benefit/ Επίδομα χαμηλοσυνταξιούχου (bsaoa_cy)
[38](#low-pension-benefit-επίδομα-χαμηλοσυνταξιούχου-bsaoa_cy)](#low-pension-benefit-επίδομα-χαμηλοσυνταξιούχου-bsaoa_cy)

[2.6.11. Easter Benefit/Πασχαλινό Επίδομα (bsals_cy)
[41](#easter-benefitπασχαλινό-επίδομα-bsals_cy)](#easter-benefitπασχαλινό-επίδομα-bsals_cy)

[2.7. Social insurance contributions
[42](#social-insurance-contributions-1)](#social-insurance-contributions-1)

[2.7.1. Employee social insurance contributions (tscee_cy)
[42](#employee-social-insurance-contributions-tscee_cy)](#employee-social-insurance-contributions-tscee_cy)

[2.7.2. Employer social insurance contributions (tscer_cy)
[45](#employer-social-insurance-contributions-tscer_cy)](#employer-social-insurance-contributions-tscer_cy)

[2.7.3. Self-employed social contributions (tscse_cy)
[47](#self-employed-social-contributions-tscse_cy)](#self-employed-social-contributions-tscse_cy)

[2.7.4. Government social insurance contributions (tscgv_cy)
[48](#government-social-insurance-contributions-tscgv_cy)](#government-social-insurance-contributions-tscgv_cy)

[2.7.5. Contributions to the General Healthcare System/Γενικό Σύστημα
Υγείας (tsc\*\*\_cy)
[48](#contributions-to-the-general-healthcare-systemγενικό-σύστημα-υγείας-tsc_cy)](#contributions-to-the-general-healthcare-systemγενικό-σύστημα-υγείας-tsc_cy)

[2.8. Direct taxes (tin_cy)
[50](#direct-taxes-tin_cy)](#direct-taxes-tin_cy)

[2.8.1. Tax unit [50](#tax-unit)](#tax-unit)

[2.8.2. Tax base [51](#tax-base)](#tax-base)

[2.8.3. Tax schedule [53](#tax-schedule)](#tax-schedule)

[2.8.4. Tax credits [53](#tax-credits)](#tax-credits)

[2.9. Other taxes [53](#other-taxes)](#other-taxes)

[2.9.1. Special Contribution for Defence/Έκτακτη Εισφορά για την Άμυνα
(txc_cy)
[53](#special-contribution-for-defenceέκτακτη-εισφορά-για-την-άμυνα-txc_cy)](#special-contribution-for-defenceέκτακτη-εισφορά-για-την-άμυνα-txc_cy)

[2.9.2. Contribution of broader public sector employees to the
Government Employees' Pension Scheme/Εισφορές στο Επαγγελματικό Σχέδιο
Συνταξιοδοτικών Ωφελημάτων των υπαλλήλων της κρατικής υπηρεσίας και του
ευρύτερου δημόσιου τομέα (tpipb_cy)
[54](#contribution-of-broader-public-sector-employees-to-the-government-employees-pension-schemeεισφορές-στο-επαγγελματικό-σχέδιο-συνταξιοδοτικών-ωφελημάτων-των-υπαλλήλων-της-κρατικής-υπηρεσίας-και-του-ευρύτερου-δημόσιου-τομέα-tpipb_cy)](#contribution-of-broader-public-sector-employees-to-the-government-employees-pension-schemeεισφορές-στο-επαγγελματικό-σχέδιο-συνταξιοδοτικών-ωφελημάτων-των-υπαλλήλων-της-κρατικής-υπηρεσίας-και-του-ευρύτερου-δημόσιου-τομέα-tpipb_cy)

[2.9.3. Contributions of public employees to the Widows and Orphans
Government Fund/Εισφορές στο Ταμείο Χηρών και Ορφανών (tscee_cy)
[56](#contributions-of-public-employees-to-the-widows-and-orphans-government-fundεισφορές-στο-ταμείο-χηρών-και-ορφανών-tscee_cy)](#contributions-of-public-employees-to-the-widows-and-orphans-government-fundεισφορές-στο-ταμείο-χηρών-και-ορφανών-tscee_cy)

[2.9.4. Scaled reduction in emoluments of public and broader public
sector pensioners and employees/Μείωση Απολαβών και Συντάξεων του
Ευρύτερου Δημόσιου Τομέα (paycut_cy)
[56](#scaled-reduction-in-emoluments-of-public-and-broader-public-sector-pensioners-and-employeesμείωση-απολαβών-και-συντάξεων-του-ευρύτερου-δημόσιου-τομέα-paycut_cy)](#scaled-reduction-in-emoluments-of-public-and-broader-public-sector-pensioners-and-employeesμείωση-απολαβών-και-συντάξεων-του-ευρύτερου-δημόσιου-τομέα-paycut_cy)

[2.10. Consumption taxes [57](#consumption-taxes)](#consumption-taxes)

[2.10.1. VAT (il_tva) [57](#vat-il_tva)](#vat-il_tva)

[2.10.2. Ad-valorem excises (il_txv)
[60](#ad-valorem-excises-il_txv)](#ad-valorem-excises-il_txv)

[2.10.3. Specific excises (il_txa)
[60](#specific-excises-il_txa)](#specific-excises-il_txa)

[3. Data [63](#data)](#data)

[3.1. General description
[63](#general-description)](#general-description)

[3.2. Data adjustments [64](#data-adjustments)](#data-adjustments)

[3.3. Imputations and assumptions
[64](#imputations-and-assumptions)](#imputations-and-assumptions)

[3.4. Time period [66](#time-period)](#time-period)

[3.5. Gross incomes [66](#gross-incomes)](#gross-incomes)

[3.6. Disaggregation of harmonised variables
[67](#disaggregation-of-harmonised-variables)](#disaggregation-of-harmonised-variables)

[3.7. Uprating [67](#uprating)](#uprating)

[3.8. Extended input data (with household expenditures for the
simulation of consumption taxes)
[67](#extended-input-data-with-household-expenditures-for-the-simulation-of-consumption-taxes)](#extended-input-data-with-household-expenditures-for-the-simulation-of-consumption-taxes)

[4. Validation [70](#validation)](#validation)

[4.1. Aggregate Validation
[70](#aggregate-validation)](#aggregate-validation)

[4.1.1. Components of disposable income
[71](#components-of-disposable-income)](#components-of-disposable-income)

[4.1.2. Validation of market income
[71](#validation-of-market-income)](#validation-of-market-income)

[4.1.3. Validation of taxes and social insurance contributions
[72](#validation-of-taxes-and-social-insurance-contributions)](#validation-of-taxes-and-social-insurance-contributions)

[4.1.4. Validation of benefits
[73](#validation-of-benefits)](#validation-of-benefits)

[4.2. Income distribution
[74](#income-distribution)](#income-distribution)

[4.2.1. Income inequality [74](#income-inequality)](#income-inequality)

[4.2.2. Poverty rates [74](#poverty-rates)](#poverty-rates)

[4.3. Consumption Taxes
[75](#consumption-taxes-1)](#consumption-taxes-1)

[4.4. Summary of “health warnings”
[76](#summary-of-health-warnings)](#summary-of-health-warnings)

[References [77](#references)](#references)

[Sources for tax-benefit descriptions/rules
[77](#sources-for-tax-benefit-descriptionsrules)](#sources-for-tax-benefit-descriptionsrules)

[List of abbreviations and definitions
[78](#list-of-abbreviations-and-definitions)](#list-of-abbreviations-and-definitions)

[List of figures [81](#list-of-figures)](#list-of-figures)

[List of tables [82](#list-of-tables)](#list-of-tables)

[List of Annexes [84](#list-of-annexes)](#list-of-annexes)

[Annex 1. Uprating Factors
[84](#annex-1.-uprating-factors)](#annex-1.-uprating-factors)

[Annex 2. Policy Effects in 2024-2025
[88](#annex-2.-policy-effects-in-2024-2025)](#annex-2.-policy-effects-in-2024-2025)

[Annex 3: Validation Tables
[90](#annex-3-validation-tables)](#annex-3-validation-tables)

[Annex 4. Data Based On EMSD 2023
[90](#annex-4.-data-based-on-emsd-2023)](#annex-4.-data-based-on-emsd-2023)

[Statistical Annex 1. Validation Tables
[93](#statistical-annex-1.-validation-tables)](#statistical-annex-1.-validation-tables)

<span id="_Toc222326495" class="anchor"></span>Abstract

The EUROMOD Country Reports have the double function of describing the
scope of the EUROMOD simulations, including the underlying assumptions,
and providing the validation of these simulations against official
statistics. The Country Report for Cyprus is prepared by the Cypriot
EUROMOD National Team each year, and made available by the JRC on time
for the EUROMOD stable release of the model at the beginning of each
year.

<span id="_Toc222326496" class="anchor"></span>Acknowledgements

The work was carried out jointly by the EUROMOD core development team,
based at the JRC in Seville, and the Cypriot national team.

<span id="_Toc222326497" class="anchor"></span>Authors

The key contributors to this update were:

Elena Andreou, Emmanouil Daousis, Christopher Markides, Paris Nearchou
and Dimitris Smyrnakis, as members of the national team for Cyprus

Klaus Grünberger and Chrysa Leventi, as JRC developers responsible for
Cyprus

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
Cyprus. It provides an overview of the Cypriot tax-benefit system in
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
https://euromod-web.jrc.ec.europa.eu/resources/glossary

## Basic information about the tax-benefit system

The Cyprus tax-benefit system features a unified national framework in
which policy rules are consistent across regions and local authorities.

The “tax year” runs from 1 January to 31 December.

The statutory pensionable age under the General Social Insurance Scheme
(the “GSIS”) is 65 for both men and women, regardless of worker category
(employed or self-employed) or occupation. Accessing a GSIS statutory
pension at age 63 is possible under certain conditions, but it entails
financial disincentives, such as actuarial reductions in pension
benefits.

The normal retirement age for the Government Employee Pension Scheme is
65 for both men and women. However, it is possible to retire at 63 under
certain conditions, subject to financial disincentives (actuarial
reductions in pensions). For specific occupations, such as police and
military officers and those in educational services, the normal
retirement age is lower; for example, it is 62 for officers in
educational services.

Definitions of benefit units can vary slightly between policies. A key
definition in social policy concerns dependent children. Typically,
children are regarded as dependent if they are under 18, or between 18
and 23 if they are in military service or undertaking full-time
education. Children unable to support themselves, for example, due to a
disability, are considered dependent regardless of age.

Income tax is calculated individually, with spouses assessed separately.

Individual taxable income is taxed progressively, whereas corporate
profits, dividends, and interest are taxed at a flat rate.

The levels of benefits, pensions, and wages in the public sector are
periodically reviewed through statutory indexing schemes that take
account of inflation and/or the cost of living.

For means-testing purposes, income is assessed either annually or
monthly, depending on the policy context. Means-testing relies on income
earned in prior periods. The definition of income may vary by policy
context.

Consumption taxes include (1) VAT with three rate categories (standard,
reduced, and zero), (2) harmonised excises on tobacco, alcohol, and
energy, and (3) Vehicle Registration Tax on the purchase of motor
vehicles.

The policy parameters are stored as constants in the model, and their
values for the most recent year are available at
<https://euromod-web.jrc.ec.europa.eu/resources/parameters>.

## Minimum Wage

As of 1 January 2023, Cyprus introduced a National Minimum Wage. This
amount was set at €885 upon recruitment for full-time work, with the
provision to increase to €940 per month after six months of employment
with the same employer. Since 1 January 2024, the National Minimum Wage
has risen to €900 upon recruitment, increasing to €1000 per month after
six months of employment with the same employer.

For individuals under 18 who are temporarily employed, the full-time
amount may be reduced by 25% for up to 2 months.

The minimum wage does not apply to household workers (οικιακούς
εργαζομένους), employees in the hotel industry who are subject to
different legislation, those in the agricultural or forestry
(γεωργοκτηνοτροφία) sectors, or in shipping (ναυτιλία). It also excludes
workers in education or training who are undertaking mandatory work
placements. Additionally, it does not apply to workers covered by more
favourable arrangements established by legislation, contract, custom, or
tradition.

Before 1 January 2023, Cyprus lacked a national minimum wage, as the
relevant legislation applied only to specific occupations. These
included shop assistants, clerks, childcare workers (including assistant
baby and child minders), personal care workers (such as nursing
assistants), security guards, and cleaners. The starting monthly wage
was €870, increasing to €924 after six months with the same employer.
The minimum wage for security guards was set at €4.90 per hour, rising
to €5.20 after six months. The corresponding hourly rates for cleaners
were €4.55 and €4.84, respectively.

## Social Benefits

This section offers a brief overview of basic social benefits under the
GSIS, both simulated and non-simulated, excluding minor benefits that
affect small population groups and have limited importance. Section 2
provides detailed information on policy parameters (e.g., benefit
rates).

### Contributory insurance-based benefits

#### Short-term benefits

**Unemployment benefit (*Ανεργιακό Επίδομα*)**: Unemployment benefits
are available to individuals aged 16 to 63 who are involuntarily
unemployed. The payment period is 156 days per spell of unemployment.
The benefit rate is calculated as a proportion of insurable earnings and
is increased for dependent spouses and children. Eligibility is subject
to specific contribution conditions. Specifically, a person should (i)
have been insured for at least 26 weeks and have paid, up to the date of
unemployment, contributions not lower than 26 times the weekly amount of
the basic insurable earnings; and (ii) have paid contributions in the
previous contribution year on insurable earnings no less than 20 times
the weekly amount of basic insurable earnings. These contribution
conditions also apply to other insurance-based benefits.

**Maternity benefit (Επίδομα Μητρότητας**). The maternity benefit is a
contributory benefit payable to employed and self-employed mothers of
newborns during maternity leave. The benefit lasts for 18 weeks, with an
increase for multiple births (by 4 weeks for twins and by 8 weeks for
triplets and more). An amendment to the social insurance law, enacted on
5 November 2021, extends maternity leave and the benefit to 22 weeks for
a second child and 26 weeks for a third child and beyond. The scheme
also covers adoptive mothers. To be eligible, the recipient must be on
maternity leave and not receive a full salary from her employer.
Additionally, certain contribution-related conditions must be met. The
benefit amount is calculated based on the recipient's insurable
earnings. However, the sum of the reduced wage (if any) and the benefit
cannot exceed the full wage.

**Paternity benefit (Επίδομα Πατρότητας):** The paternity benefit is a
contributory benefit available to employed and self-employed fathers of
newborns during their parental leave period.[^1] The benefit lasts for 2
weeks. The same qualifying conditions that apply to maternity benefits
also apply here. This benefit was introduced in August 2017. As of 16
December 2022, a new law (No. 214 (I)/2022) was enacted, extending this
benefit to fathers regardless of their marital status. From that date,
paternity leave and benefit receipt can be extended in cases where the
mother dies during childbirth or maternity leave.

**Birth grant (Βοήθημα Τοκετού):** The birth grant is a one-off,
flat-rate benefit based on contributions and available to mothers of
newborns. The social insurance record of either the mother or the father
determines eligibility.

**Special birth grant for unmarried mothers (Ειδικό Βοήθημα Τοκετού σε
Άγαμες Μητέρες):** The special birth grant, a non-contributory,
tax-funded benefit, is available to unmarried mothers who do not qualify
for the birth grant. It is equal in amount to the birth grant.

**Parental leave benefit (Γονική Άδεια):** In December 2022, the Social
Insurance Law was amended to grant parental leave benefits to insured
employees (and self-employed individuals from May 2024 onwards) on
parental leave. This benefit is paid for up to 6 weeks (8 weeks after
August 2024) to each parent for each child, from the 18 weeks of
parental leave provided by the Leaves (Paternity, Parental, Caring,
Force Majeure) and Flexible Work Arrangements for Work-Life Balance Law
of 2022 (216(I)/2022). For single parents, the leave is extended to 23
weeks. In cases involving a child with a severe disability or moderate
mental disability, the benefit is extended by 4 weeks, and by 6 weeks
for a child with a total disability. The benefit is paid from the end of
maternity/paternity leave until the child turns 8 years old, or until
they reach 18 if disabled. Additionally, for the unpaid part of parental
leave, the GSIS provides equivalent insurance credits.

**Other benefits for parents:** These include the honorary allowance for
mothers, the allowance for caring for disabled children or older
relatives, and grants for the care of children placed with foster
families. There is also a funeral grant. In October 2022, Law
150(I)/2022 was enacted, providing sickness benefits to insured persons
aged 63 to 65 who continue working and do not receive the state pension.

**Sickness Benefit (Επίδομα Ασθενείας):** Under GSIS, the sickness
benefit is payable to individuals unable to work. The payment period
cannot exceed 156 days. Eligibility is based on standard contribution
conditions (see above). The benefit rate is calculated as a proportion
of insurable earnings and increases with the number of dependants.

**Orphan Benefit *(Επίδομα Ορφάνιας)***: An orphan benefit is payable to
dependent children[^2] whose parents have both died, or whose one parent
has died and the other is not entitled to a widow’s pension. Eligibility
requires at least one parent to be insured. The benefit is calculated as
a proportion of insurable earnings, subject to certain ceilings. It is
paid until the child reaches the maximum qualifying age, unless the
beneficiary is permanently unable to work.

**Employment injury benefit (Επίδομα Σωματικής Βλάβης):** This GSIS
benefit is available to any employed person (and from April 2024, to any
self-employed individual) who is unable to work due to an employment
accident or an occupational-related disease. The benefit can be received
for up to 12 months from the date of the accident or the onset of the
disease. The recipient must have been employed on the day of the
accident or disease and, due to the injury, be unable to work and not
receive a full wage during this period. The injury benefit rate is the
same as the sickness benefit rate.

**Disablement grant (Βοήθημα Αναπηρίας):** The disablement grant is
payable to employed individuals who, as a result of an employment
injury, have suffered a loss of physical or mental capacity amounting to
a disability of 10% to 19%. The benefit is paid as a lump sum.

#### Pensions

**Statutory pension (Θεσμοθετημένη Σύνταξη):** The statutory pension is
payable to insured individuals who have reached the pensionable age (65
years for all categories of employees) and meet all the required
insurance conditions. These conditions require that the claimant have
been insured for at least 780 weeks up to the pensionable age, and that
the insurance points accrued during that period be at least 30% of the
years included. The statutory pension can be received at age 63, with a
12% actuarial reduction, provided that the insurance points accumulated
in the relevant period are at least 70% of the years included. The
statutory pension comprises two components: the basic and the
supplementary. The basic pension is calculated as 60% of the average
insurable earnings in the lower band, with increases of one-third,
one-half, and two-thirds for one, two, or three or more dependants,
respectively. The supplementary pension amounts to 1/52 of 1.5% of the
total insurable earnings (of the beneficiary in the upper band).

**Invalidity pension (Σύνταξη Ανικανότητας):** The invalidity pension is
payable to individuals who have been unable to work for at least 156
days and are expected to remain permanently unable to work. In addition
to the standard insurance conditions (see other benefits), the claimant
must have been insured for a minimum of 156 weeks up to the date of
invalidity, and the number of insurance points accumulated during that
period must be at least 25% of the years in that period. The calculation
of the invalidity pension is similar to that of a statutory pension.

**Widow/widower pension (Σύνταξη Χηρείας):** The widows’ pension is
payable to the widow of a person who, until the date of their death, met
the relevant insurance conditions. The widows’ pension comprises a basic
part and a supplementary part. The basic part equals the basic component
of the statutory pension, while the supplementary part is 60% of the
statutory or invalidity pension. An amendment to the social insurance
law, enacted on 5 August 2019 with retrospective effect from 1 January
2018, mandates the payment of widowers’ pensions to men under the same
conditions as those for women who lose their husbands.

**Honorary benefit for war veterans (Τιμητικό επίδομα βετεράνων
πολεμιστών του 1974):** This means-tested, tax-funded benefit,
established in June 2018, is for individuals who receive a statutory
pension and are war veterans. These veterans include those who served in
the National Guard during the Turkish invasion in 1974 and, as a result,
completed at least one month of additional service, and/or were
prisoners of war and/or are disabled. Additionally, a Special Lump Sum
is paid biannually to individuals registered by the Ministry of Defence
or the Ministry of Interior as military or non-military (civilian)
prisoners of war during the Turkish invasion of 1974, as well as to
individuals who are war invalids and receive a monthly benefit from the
Patients' Relief Fund. (NB: Since December 2022, the lump sum for those
who are war invalids is paid from the Patients' Relief Fund. With a
supplementary decision from the Council of Ministers, beneficiaries of
the Special Lump Sum may also include those who do not qualify for the
monthly honorary benefit. The lump sum was implemented in July 2022).

### Non-contributory social benefits

**Guaranteed Minimum Income (Ελάχιστο Eγγυημένο Eισόδημα):** The
Guaranteed Minimum Income scheme is a means-tested benefit for families
whose income is insufficient to meet basic needs. It provides the
difference between the basic income and the family’s actual income. This
amount is topped up with a housing allowance. The recipient unit is the
“family unit”, comprising couples or single individuals living with
unmarried children up to age 28, or children in full-time education or
military service. Both movable and immovable property are considered
when assessing eligibility.

**Disablement pension (*Σύνταξη Αναπηρίας*):** All employed individuals
who have suffered a work-related injury resulting in a loss of physical
or mental capacity, with a disability degree of 20% or more, are
entitled to a disablement pension. There are no insurance requirements
for eligibility. Recipients of the disablement pension may continue to
work while receiving it.

**Child Benefit (Επίδομα Τέκνου):** Child Benefit is a non-contributory,
means-tested benefit available to all families with children who live
permanently in Cyprus. The amount of the benefit is proportional to the
number of children in the family and inversely proportional to its
income.

**Student Grant (Φοιτητική Χορηγία):** The Student Grant is a
non-contributory, means-tested benefit paid to the person covering the
tuition fees of a student at either private or public tertiary
institutions. It comprises a basic component and a supplementary
component. The basic component is a fixed amount, while the
supplementary component depends on income and other criteria.

**Social Pension (Κοινωνική Σύνταξη):** The Social Pension provides a
minimum pension to elderly individuals residing in Cyprus who are not
eligible for a contributory pension or other forms of retirement income.
Beneficiaries must meet one of the following residence requirements:
they must have legally resided in Cyprus for at least 20 years from the
date they turned 40, or have lawfully lived in Cyprus for at least 35
years from the age of 18. The Social Pension is paid at a flat rate to
all eligible beneficiaries. The pension amount for 2025 is €415.13.

**Single Parent Benefit (Επίδομα Μονογονιού):** The Single Parent
Benefit is a non-contributory, means-tested scheme that provides
financial support to single parents who are Cypriot nationals, EU
citizens, or have lived in Cyprus for the past three years. Single
parents may be unmarried, divorced, or widowed, and live with their
dependent children without a spouse or partner.

**Low Pension Benefit (Επίδομα Χαμηλοσυνταξιούχου):** The Low Pension
Benefit is a means-tested, non-contributory support for families with
incomes below the poverty line, where at least one family member
receives a pension. It was introduced on 1 December 2009 and came into
effect on 1 March 2010.

**Easter Benefit (Πασχαλινό Επίδομα):** The Easter Benefit is a
means-tested allowance provided to low-income pensioners just before
Easter. Introduced in 2010, it is voted on annually by the Council of
Ministers.

**Benefit for nursery expenses for children under 4 (Σχέδιο Επιδότησης
Διδάκτρων και Σίτισης Παιδιών ηλικίας μέχρι 4ων ετών):** Introduced in
2023, this benefit supports families with young children who are
eligible for child benefits. It partially subsidises daycare services
for dependent children (up to 4 years old) by making direct monthly
payments to nurseries or daycare centres. The subsidy covers 80% of the
monthly fees for each child, with a maximum amount determined by family
income, composition, and the duration of daycare attendance.

## Social insurance contributions

**Employee social insurance contributions (Ασφαλιστικές εισφορές
εργαζομένων):** The mandatory employee contribution rate is 22.8%,
comprising 8.8% paid by the employee, 8.8% by the employer, and 5.2%
from the Consolidated Fund of the Republic (Πάγιο Ταμείο της
Δημοκρατίας).

**Self-employed social insurance contributions (Ασφαλιστικές εισφορές
αυτοτελώς εργαζομένων):** The contribution rate for self-employed
individuals is 21.8%, with 16.6% paid by the self-employed and 5.2%
contributed by the state. The insured person chooses the amount of
insured earnings on which social insurance contributions are based;
however, a mandatory minimum amount (notional income) applies for each
occupational category. There is also a single upper limit on insured
earnings that applies to all occupational categories. If a self-employed
person's actual income falls below the minimum amount for their
occupational category, they may request to pay contributions based on
their actual income.

**Voluntary insured person social insurance contributions (Προαιρετικές
ασφαλιστικές εισφορές):** Voluntary Insurance is available for persons
wishing to supplement their contributions in order to reach the
requirements for the state pension (or increase the amount of the
pension they will be given), as well as for those working abroad for
Cypriot employers. For voluntarily insured individuals working in
Cyprus, the contribution rate is 20%, with 15.2% paid by the insured
person and 4.8% by the state. For those working abroad for Cypriot
employers, the rate is 23.1%, comprising 17.8% paid by the insured
person and 5.3% by the government. The insured person chooses the amount
of insured earnings on which social insurance contributions are based,
but this amount cannot exceed the weekly total of their past insured
earnings.

**Employer social insurance contributions (Ασφαλιστικές εισφορές
εργοδοτών):** Employers must contribute to the following funds for all
employees whose earnings exceed €2 per week or €7 per month: the Social
Insurance Fund, the Annual Holidays Fund, the Redundancy Fund, the Human
Resource Development Authority Fund, and the Social Cohesion Fund. For
trainees and apprentices, each employer must contribute to the Social
Insurance Fund, even if the employee has no earnings. The employer's
obligation to pay contributions to the Social Insurance Fund ends on the
day the employee reaches pensionable age.

**Credited social insurance contributions (Πιστωμένες ασφαλιστικές
εισφορές):** Contributions may be credited to insured persons in the
following cases: 1) for any period after the age of 16 when they are
studying full-time or attending training courses; 2) for any period
during which they receive sickness, unemployment, maternity, physical
injury benefits, or incapacity pensions from the Social Insurance Fund;
3) for any period of declared unemployment or illness when the
individual is not eligible to receive a benefit. In these cases, the
credit period cannot exceed six months.

**Provident fund contributions (Ασφαλιστικές εισφορές ταμείων
πρόνοιας):** Provident funds provide cash benefits to employees upon
termination of employment, permanent incapacity to work, retirement, or
death, and are financed through regular contributions from both
employers and employees. The Law of the Establishment, Activities and
Supervision of Institutions of Occupational Retirement Benefits sets out
the general legislative framework. However, it does not specify
contribution or benefit rates, which are established through collective
agreements between employees and employers.

**General Healthcare System (Γενικό Σύστημα Υγείας):** The General
Healthcare System is a comprehensive, contributory healthcare framework
that provides equal access to healthcare services to all covered
individuals. Participation is mandatory for all income-earning residents
of Cyprus. The GHS has been fully implemented since 1 June 2020, while
contributions for the first phase of its implementation began on 1 March
2019.

## Taxes

**Personal Income Tax (Φόρος Εισοδήματος):** The Personal Income Tax
applies to all tax residents of Cyprus on income earned or received from
any source, whether within Cyprus or abroad. Taxable income includes
wages and salaries, income from self-employment and business activities,
and rental income and pensions. Social benefits paid as a lump sum or
for a short period (for example, sickness benefit) are not included in
the tax base.

**Special Contributions for Defence (Ειδική Εισφορά για την Άμυνα):**
The Special Contribution for Defence is levied on income from dividends,
interest, and rental income of Cyprus tax residents, including both
individuals and legal entities. Dividends are taxed at 17%, as are
“passive” interest income, except for interest from corporate bonds,
Cyprus government savings and development bonds, and interest earned by
a provident fund, which are taxed at 3%. Other minor exemptions also
apply. Finally, rental income is taxed at 3%, but only 75% of it is
subject to the contribution.

**Real Property Tax (Φόρος Ακίνητης Περιουσίας):** Property owners,
whether residing in Cyprus or not, are responsible for paying an annual
tax based on the total value of their immovable property. The real
property tax was abolished on 1 January 2017.

**Value Added Tax (Φόρος Προστιθέμενης Αξίας):** VAT is levied on the
supply of goods and services in Cyprus, on the purchase of goods from
the European Union, and on the importation of goods into Cyprus. The
standard VAT rate is 19%, with reduced rates of 9%, 5%, and 3% applying
to several essential goods.

**Capital Gains Tax (Φόρος Κεφαλαιακών Κερδών):** Capital gains, such as
those from selling immovable property, are taxed at 20%. Individuals can
claim various deductions.

**Special Contribution (Ειδική Εισφορά):** The Special Contribution was
part of the fiscal consolidation measures introduced after 2011. It was
levied on the monthly earnings of private- and public-sector employees,
self-employed individuals, and pensioners. The contribution rate began
at zero below a certain threshold and increased progressively with
earnings. The Special Contribution was abolished from 1 January 2017.

**Excise duties (Καταναλωτικοί Φόροι):** Excise duties are levied on
various products, including energy (electricity and mineral oils),
tobacco, and a range of alcoholic beverages. Alcohol, tobacco, and
energy are subject to EU-harmonised taxes. Some tobacco products are
taxed both ad valorem and ad quantum, whereas all other products are
taxed ad quantum only.

**Motor Vehicle Registration Tax (Εγγραφή μηχανοκίνητου οχήματος):** A
tax is levied on individuals and corporations when a motor vehicle is
registered. The amount payable depends on the vehicle type, engine
capacity, horsepower, and the type of fuel used.

# Simulation of taxes, Social Insurance Contributions and benefits in Euromod

## Scope of simulation

EUROMOD simulates a range of policy instruments, including taxes, social
benefits, and social insurance contributions.

The decision to simulate a specific instrument is based on the
information available in the input data. For example, simulating
eligibility rules is not always feasible because some policies entail
substantial information requirements. A notable example is pensions, for
which a meaningful simulation requires access to the individual's
contribution record up to pensionable age.

Other benefits are governed by complex rules that the model only
partially simulates. A characteristic example is the GMI benefit, which,
in addition to a basic monetary benefit and a housing allowance,
provides recipients with a range of minor cash and non-cash benefits
tailored to their individual needs (such as long-term care cash benefits
for households with dependent elderly persons, childcare benefits, and
others), which the model cannot capture. In these instances, the policy
simulation is partial and should be interpreted accordingly.

[**Table 2.1**](#Table_02_01) lists the benefits, and [**Table
2.2**](#Table_02_02) the tax and social insurance contribution policies
simulated for the policy years 2022 to 2025.

## Partially simulated tax-benefit components

Some benefits use eligibility information from the input data to
determine eligibility status, as the data does not contain sufficient
information to simulate all relevant eligibility rules. For example, the
unemployment benefit is simulated only for those recorded in the input
data as recipients.

<span id="Table_02_01" class="anchor"></span>**Table 2.1** Simulation of
benefits in EUROMOD \[2022-2025\]

<table>
<colgroup>
<col style="width: 26%" />
<col style="width: 9%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 38%" />
</colgroup>
<thead>
<tr>
<th><strong>Benefit</strong></th>
<th><blockquote>
<p><strong>Variable</strong></p>
</blockquote></th>
<th><strong>2022</strong></th>
<th><strong>2023</strong></th>
<th><blockquote>
<p><strong>2024</strong></p>
</blockquote></th>
<th><blockquote>
<p><strong>2025</strong></p>
</blockquote></th>
<th><blockquote>
<p><strong>Comments</strong></p>
</blockquote></th>
</tr>
</thead>
<tbody>
<tr>
<td>GMI</td>
<td><blockquote>
<p>bsamm_s</p>
</blockquote></td>
<td>S</td>
<td>S</td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>Lack of information on the particular needs of the recipient</p>
</blockquote></td>
</tr>
<tr>
<td>Low pension benefit</td>
<td><blockquote>
<p>bsaoa_s</p>
</blockquote></td>
<td>S</td>
<td>S</td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>-</p>
</blockquote></td>
</tr>
<tr>
<td>Easter benefit</td>
<td><blockquote>
<p>bsals_s</p>
</blockquote></td>
<td>S</td>
<td>S</td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>-</p>
</blockquote></td>
</tr>
<tr>
<td>Unemployment benefit: From SIF</td>
<td><blockquote>
<p>bunct_s</p>
</blockquote></td>
<td>PS</td>
<td>PS</td>
<td><blockquote>
<p>PS</p>
</blockquote></td>
<td><blockquote>
<p>PS</p>
</blockquote></td>
<td><blockquote>
<p>Not possible to define the contribution record and past earnings</p>
</blockquote></td>
</tr>
<tr>
<td>Unemployment: other</td>
<td><blockquote>
<p>bunot</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>No information to define eligibility</p>
</blockquote></td>
</tr>
<tr>
<td>Maternity benefit</td>
<td><blockquote>
<p>bma</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Paid SICs cannot be defined perfectly, as there is no available
information</p>
</blockquote></td>
</tr>
<tr>
<td>Paternity benefit</td>
<td><blockquote>
<p>-</p>
</blockquote></td>
<td>-</td>
<td>-</td>
<td><blockquote>
<p>-</p>
</blockquote></td>
<td><blockquote>
<p>-</p>
</blockquote></td>
<td><blockquote>
<p>Implemented as the Maternity benefit</p>
</blockquote></td>
</tr>
<tr>
<td>Child benefit</td>
<td><blockquote>
<p>bch_s</p>
</blockquote></td>
<td>S</td>
<td>S</td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>Relevant income may not be defined exactly</p>
</blockquote></td>
</tr>
<tr>
<td>Military service grant</td>
<td><blockquote>
<p>bml</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Not enough information to define the exact amount of the grant</p>
</blockquote></td>
</tr>
<tr>
<td>Students grant</td>
<td><blockquote>
<p>bedet_s</p>
</blockquote></td>
<td>S</td>
<td>S</td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>-</p>
</blockquote></td>
</tr>
<tr>
<td>Special unemployment scheme: Employees</td>
<td><blockquote>
<p>bwkmcee_s</p>
</blockquote></td>
<td>S</td>
<td>S</td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>Introduced during the COVID-related lockdown in 2020.</p>
</blockquote></td>
</tr>
<tr>
<td>Special unemployment scheme: Self-employed</td>
<td><blockquote>
<p>bwkmcse_s</p>
</blockquote></td>
<td>S</td>
<td>S</td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>Introduced during the COVID-related lockdown in 2020.</p>
</blockquote></td>
</tr>
<tr>
<td>Special grant to blind persons</td>
<td><blockquote>
<p>pdi</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Eligibility cannot be defined</p>
</blockquote></td>
</tr>
<tr>
<td>Sickness benefit</td>
<td><blockquote>
<p>bhl</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Eligibility cannot be defined</p>
</blockquote></td>
</tr>
<tr>
<td>Physical injury benefit</td>
<td><blockquote>
<p>bhl</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Eligibility cannot be defined</p>
</blockquote></td>
</tr>
<tr>
<td>Disability pension</td>
<td><blockquote>
<p>pdi</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Eligibility cannot be defined</p>
</blockquote></td>
</tr>
<tr>
<td>Disability benefit</td>
<td><blockquote>
<p>pdi</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Eligibility cannot be defined</p>
</blockquote></td>
</tr>
<tr>
<td>Widow/widower pension</td>
<td><blockquote>
<p>psuwd</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Depends on the SICs of the deceased</p>
</blockquote></td>
</tr>
<tr>
<td>Orphan benefit</td>
<td><blockquote>
<p>psuor</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Eligibility cannot be defined</p>
</blockquote></td>
</tr>
<tr>
<td>Parent pension</td>
<td><blockquote>
<p>psuot</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Eligibility cannot be defined</p>
</blockquote></td>
</tr>
<tr>
<td>Honorary benefit</td>
<td><blockquote>
<p>-</p>
</blockquote></td>
<td>E</td>
<td>E</td>
<td><blockquote>
<p>E</p>
</blockquote></td>
<td><blockquote>
<p>E</p>
</blockquote></td>
<td><blockquote>
<p>Introduced in 2019, not yet part of the input data. Eligibility
cannot be defined</p>
</blockquote></td>
</tr>
<tr>
<td>Birth grant</td>
<td><blockquote>
<p>bchba_s</p>
</blockquote></td>
<td>S</td>
<td>S</td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>-</p>
</blockquote></td>
</tr>
<tr>
<td>Maternity benefit</td>
<td><blockquote>
<p>bmact_s</p>
</blockquote></td>
<td>S</td>
<td>S</td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>Eligibility: difficult to define work history</p>
</blockquote></td>
</tr>
<tr>
<td>Paternity benefit</td>
<td><blockquote>
<p>bpact_s</p>
</blockquote></td>
<td>S</td>
<td>S</td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>Eligibility: difficult to define work history</p>
</blockquote></td>
</tr>
<tr>
<td>Other benefits for parents</td>
<td><blockquote>
<p>bfamh</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Eligibility cannot be defined</p>
</blockquote></td>
</tr>
<tr>
<td>Widow's pension for public employees</td>
<td><blockquote>
<p>psuwd</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Eligibility cannot be defined</p>
</blockquote></td>
</tr>
<tr>
<td>Orphan pension for public employees</td>
<td><blockquote>
<p>psuor</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Eligibility cannot be defined</p>
</blockquote></td>
</tr>
<tr>
<td>Statutory pension</td>
<td><blockquote>
<p>poa</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>The pension’s level depends on the SICs which are not known</p>
</blockquote></td>
</tr>
<tr>
<td>Social pension</td>
<td><blockquote>
<p>poasp</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Eligibility cannot be simulated</p>
</blockquote></td>
</tr>
<tr>
<td>Incapacity pension</td>
<td><blockquote>
<p>pdi</p>
</blockquote></td>
<td>I</td>
<td>I</td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>I</p>
</blockquote></td>
<td><blockquote>
<p>Eligibility cannot be defined.</p>
</blockquote></td>
</tr>
<tr>
<td>Single-parent benefit</td>
<td><blockquote>
<p>bchlp_s</p>
</blockquote></td>
<td>S</td>
<td>S</td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>S</p>
</blockquote></td>
<td><blockquote>
<p>-</p>
</blockquote></td>
</tr>
<tr>
<td>Benefit for nursery expenses for children aged under 4</td>
<td><blockquote>
<p>-</p>
</blockquote></td>
<td>E</td>
<td>E</td>
<td><blockquote>
<p>E</p>
</blockquote></td>
<td><blockquote>
<p>E</p>
</blockquote></td>
<td><blockquote>
<p>Introduced in September 2023, not yet part of the input data.
Eligibility cannot be defined</p>
</blockquote></td>
</tr>
<tr>
<td colspan="7"><strong>Notes</strong>: “-”: policy did not exist in
that year; “E”: excluded from the model as it is neither included in the
micro-data nor simulated; “I”: included in the micro-data but not
simulated; “PS” partially simulated as some of its relevant rules are
not simulated; “S” simulated although some minor or very specific rules
may not be simulated.</td>
</tr>
<tr>
<td colspan="7">Source: Own elaboration, based on information from the
EUROMOD Cyprus model (V0.60).</td>
</tr>
</tbody>
</table>

<span id="Table_02_02" class="anchor"></span>**Table 2.2** Simulation of
taxes and Social Insurance contributions (SICs) in EUROMOD \[2022-2025\]

<table style="width:100%;">
<colgroup>
<col style="width: 25%" />
<col style="width: 9%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 38%" />
</colgroup>
<thead>
<tr>
<th><strong>Taxes/SICs</strong></th>
<th><strong>Variable</strong></th>
<th><strong>2022</strong></th>
<th><strong>2023</strong></th>
<th><strong>2024</strong></th>
<th><strong>2025</strong></th>
<th><blockquote>
<p><strong>Comments</strong></p>
</blockquote></th>
</tr>
</thead>
<tbody>
<tr>
<td>Employee SICs: General</td>
<td>tscee00_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>Employee SICs: Widow and pension fund</td>
<td>tsceepi_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>Employee SICs: General Healthcare System</td>
<td>tsceehl_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>Employer SICs: General</td>
<td>tscer00_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>Employer SICs: Annual Holidays Fund</td>
<td>tscerhe_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><blockquote>
<p>Contributors randomly chosen</p>
</blockquote></td>
</tr>
<tr>
<td>Employer SICs: Redundancy Fund</td>
<td>tscersv_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>Employer SICs: Human Resources Fund</td>
<td>tscerot_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>Employer SICs: Social Cohesion</td>
<td>tscerir_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>Employer SICs: General Healthcare System</td>
<td>tscerhl_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>Self-employed SICs:</td>
<td>tscse00_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>Self-employed SICs: General Healthcare System</td>
<td>tscsehl_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>Pensioner SICs: General Healthcare System</td>
<td>tscpehl_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>Other Income SICSs: General Healthcare System</td>
<td>tscothl_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>State SICSs: General</td>
<td>tscgv00_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>State SICSs: General Healthcare System</td>
<td>tscgvhl_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>Optionally insured person SICs</td>
<td><blockquote>
<p>-</p>
</blockquote></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><blockquote>
<p>No sufficient information is available from the data</p>
</blockquote></td>
</tr>
<tr>
<td>Credited SICs</td>
<td><blockquote>
<p>-</p>
</blockquote></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><blockquote>
<p>No sufficient information is available from the data</p>
</blockquote></td>
</tr>
<tr>
<td>Provident-fund contributions</td>
<td><blockquote>
<p>-</p>
</blockquote></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><blockquote>
<p>No sufficient information is available from the data</p>
</blockquote></td>
</tr>
<tr>
<td>Contribution for public pensions</td>
<td>tpipb_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>Personal Income Tax</td>
<td>tin_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td></td>
</tr>
<tr>
<td>Corporate income tax</td>
<td></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><blockquote>
<p>Out of the scope of the model</p>
</blockquote></td>
</tr>
<tr>
<td>Property tax</td>
<td><blockquote>
<p>-</p>
</blockquote></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><blockquote>
<p>No information about the value of the property</p>
</blockquote></td>
</tr>
<tr>
<td>Special contribution for defence</td>
<td>txc_s</td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><blockquote>
<p>No information on legal entities</p>
</blockquote></td>
</tr>
<tr>
<td>Value Added Tax (VAT)</td>
<td><blockquote>
<p>-</p>
</blockquote></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><blockquote>
<p>Calculations based on extended input files with consumption
expenditures from HBS</p>
</blockquote></td>
</tr>
<tr>
<td>Excise duties</td>
<td><blockquote>
<p>-</p>
</blockquote></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><strong>S</strong></td>
<td><blockquote>
<p>Calculations based on extended input files with consumption
expenditures from HBS</p>
</blockquote></td>
</tr>
<tr>
<td>Motor vehicle tax</td>
<td><blockquote>
<p>-</p>
</blockquote></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><strong>E</strong></td>
<td><blockquote>
<p>No information available</p>
</blockquote></td>
</tr>
<tr>
<td colspan="7">Notes: “-” policy did not exist in that year; “E” policy
is excluded from the model’s scope as it is neither included in the
microdata nor simulated by EUROMOD; “PS” policy is partially simulated
as some of its relevant rules are not simulated; “S” policy is simulated
although some minor or very specific rules may not be simulated.</td>
</tr>
<tr>
<td colspan="7">Source: Own elaboration, based on information from the
EUROMOD Cyprus model (V0.60).</td>
</tr>
</tbody>
</table>

## Main policy changes

[**Table 2.3**](#Table_02_03) records the primary policy changes that
took place throughout the simulation period.

<span id="Table_02_03" class="anchor"></span>**Table 2.3** Main policy
changes over 2022-2025

<table style="width:65%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 14%" />
<col style="width: 13%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr>
<th><strong>Policies</strong></th>
<th><strong>2021 → 2022</strong></th>
<th><strong>2022 → 2023</strong></th>
<th><strong>2023 → 2024</strong></th>
<th><strong>2024 → 2025</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Benefits</strong></td>
<td><em><strong>Maternity allowance:</strong></em> The duration of the
maternity benefit has been extended according to the number of children
in the family.</td>
<td><em><strong>Minimum Wage:</strong> Introduction of the National
Minimum Wage</em></td>
<td><em><strong>Benefit for nursery expenses for children aged under
4:</strong> Introduction of the scheme</em></td>
<td></td>
</tr>
<tr>
<td><strong>Social Insurance Contributions</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><strong>Direct Taxes</strong></td>
<td></td>
<td><em>The <strong>Scaled reduction in emoluments of public and broader
public sector pensioners and employees</strong> was abolished</em></td>
<td></td>
<td></td>
</tr>
<tr>
<td rowspan="2"><strong>Consumption Taxes</strong></td>
<td rowspan="2"></td>
<td colspan="2"><em><strong>VAT:</strong> The rate for basic foodstuffs
(e.g., bread, milk, eggs, baby food, etc.) was temporarily reduced to 0%
for several months in 2023 and 2024, as a measure to mitigate the impact
of high inflation.</em></td>
<td></td>
</tr>
<tr>
<td><em><strong>VAT:</strong> A new reduced rate at 3% was introduced in
July</em></td>
<td></td>
<td></td>
</tr>
<tr>
<td><strong>Other</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

Source: Own elaboration.

## Order of simulations and interdependence

The structure of the model spine has remained stable from 2022 to 2025.

The simulation order is as follows: initially, the model simulates
social insurance contributions (with reductions in public-sector
employees’ wages and pensions simulated before SICs). Subsequently,
income tax and the special contribution to defence are deducted from
income. Thereafter, cash benefits are simulated in the following order:
birth grant, child benefit, single parent benefit, student grant, and
GMI.

The final policy included in the spine is tco_cy (consumption taxes). It
is placed at the very end because consumption tax liabilities (VAT and
excise duties) depend on household consumption expenditure, which the
model estimates from income shares (xs\_\* variables in the input data)
and simulated disposable income (ils_dispy). Therefore, before running
any simulation of consumption tax policy, it is necessary to activate
all other policies that affect the simulation of disposable income.
Lastly, we note that the unemployment benefit is switched off (in the
baseline scenario) for all years. [**Table 2.4**](#Table_02_04) outlines
the order in which the main instruments of the Cypriot tax-benefit
system are simulated.

<span id="Table_02_04" class="anchor"></span>**Table 2.4** EUROMOD
Spine: order of simulation

| **Policy** | **Position in spine** | **Section in CR** | **2022** | **2023** | **2024** | **2025** | **Description of the instrument and main output** |
|:---|:---|:---|:---|:---|:---|:---|:---|
| *yemcomp_cy* | 13 | \- | Off | Off | Off | Off | Special unemployment benefit scheme for employees (only produces results with the LMA add-on) |
| *ysecomp_cy* | 14 | \- | Off | Off | Off | Off | Special unemployment benefit scheme for self-employed (only produces results with the LMA add-on) |
| *paycut_cy* | 15 | 2.9.4 | On | Off | Off | Off | Cuts in broader public sector wages and pensions |
| *tscee_cy* | 16 | 2.7.1, 2.7.5, 2.9.3 | On | On | On | On | Employee contributions: Social Insurance, GHS, Widows and Orphans Government Fund |
| *tscer_cy* | 17 | 2.7.2, 2.7.5 | On | On | On | On | Employer contributions: Social Insurance, GHS |
| *tscse_cy* | 18 | 2.7.3, 2.7.5 | On | On | On | On | Self-employed contributions: Social Insurance, GHS |
| *tscpe_cy* | 19 | 2.7.5 | On | On | On | On | Pensioner contributions: GHS |
| *tscot_cy* | 20 | 2.7.5 | On | On | On | On | Other income earners' contributions: GHS |
| *tscgv_cy* | 21 | 2.7.4, 2.7.5 | On | On | On | On | Government contributions: Social Insurance, GHS |
| *txcbp_cy* | 22 | \- | n/a | n/a | n/a | n/a | Special contribution of public sector employees |
| *txcps_cy* | 23 | \- | n/a | n/a | n/a | n/a | Special contribution of private sector employees |
| *txcpe_cy* | 24 | \- | n/a | n/a | n/a | n/a | Special contribution on pensioners |
| *tpipb_cy* | 25 | 2.9.2 | On | On | On | On | Contribution of broader public sector employees to the Government Pension Scheme |
| *tin_cy* | 26 | 2.8 | On | On | On | On | Income Tax |
| *txc_cy* | 27 | 2.9.1 | On | On | On | On | Special contribution for defence |
| *bchba_cy* | 28 | 2.6.5, 2.6.6 | On | On | On | On | Birth grant (standard, for unmarried mothers) |
| *bmact_cy* | 29 | 2.6.7 | switch | switch | switch | switch | Maternity allowance |
| *bpact_cy* | 30 | 2.6.8 | switch | switch | switch | switch | Paternity allowance |
| *bunct_cy* | 32 | 2.6.1 | Off | Off | Off | Off | Unemployment benefit |
| *bch_cy* | 33 | 2.6.2 | On | On | On | On | Child benefit |
| *bchlp_cy* | 34 | 2.6.3 | On | On | On | On | Single-parent benefit |
| *bsamm_cy* | 35 | 2.6.9 | On | On | On | On | Guaranteed Minimum Income |
| *bfamh_cy* | 36 | n/a | On | On | On | On | Correct double-counting of family benefits |
| *bedet_cy* | 37 | 2.6.4 | On | On | On | On | Student grant |
| *bsa_cy* | 38 | \- | n/a | n/a | n/a | n/a | Social assistance benefit |
| *bsaoa_cy* | 39 | 2.6.10 | On | On | On | On | Low Pension benefit |
| *bsals_cy* | 40 | 2.6.11 | On | On | On | On | Easter benefit |
| *tco_cc* | 41 | 2.10 | Off | Off | Off | Off | Consumption taxes |

Source: Own elaboration, based on information from EUROMOD.

## Policy extensions

**FYA (Full Year Adjustments):** The baseline simulation refers to the
policy rules that are applicable as of 30 June of the relevant year. The
FYA switch allows for the consideration of policy changes that occurred
during the year. Currently, this switch is applied to account for the
increase in the General Healthcare System-related social insurance
contribution rates that took effect on 1 June 2020, from the previous
level set on 1 March 2019. By default, the switch is turned on.

**HHoT – Unemployment extension (HHoT_un):** This extension enhances the
simulation accuracy of unemployment insurance benefits when EUROMOD is
run with hypothetical data. Specifically, in most countries, the
legislation governing this benefit necessitates information on variables
such as individuals’ employment history, which are not available in
SILC. We can define these variables in HHoT and use them to simulate the
policy’s rules more accurately when running the model with hypothetical
data. This extension is activated when the model is used with HHoT data.

**HHoT Monthly Unemployment (HHoT_mu):** this extension enables a
monthly unemployment benefit simulation, similar to the approach used by
the OECD TaxBEN for the calculation of monthly Net Replacement Rate
(NRR) indicators. Those indicators measure to what extent a person's
previous income from work is maintained after a certain number of months
in unemployment. With this extension, unemployment benefit amounts are
calculated with respect to a specific month of the unemployment spell
and are then converted to annual amounts by multiplying by 12. By
default, this extension is switched off; it is only set to on when the
model is used for the calculation of the NRR indicators. 

**MWA (Minimum Wage Adjustment):** This switch enables the simulation of
hypothetical minimum wage models in policy yem_cy. It is set to off by
default.

**PBE (Parental Leave Benefits):** This switch enables you to activate
parental leave-related policies not simulated in the baseline: bmact_cy
and bpact_cy. It is set to off by default.

**Benefit Calibration Adjustments (BCA):** This extension allows users
to calibrate the receipt of benefits to align the simulated total number
of beneficiaries with actual expenditure from external statistics.

It is utilised in the simulation of the Guaranteed Minimum Income
(bsamm_cy). The default baseline setting is off.

When the extension is on, a subset of eligible observations is selected
randomly as beneficiaries so that the actual number of beneficiaries is
reached, removing the benefit from the remaining eligible observations;
when off, all eligible observations are kept as beneficiaries.

This extension shares most of its functions with the BTA extension. As a
general rule, only one extension should be active; however, if both are
enabled, the lower of the two rates – between the take-up rate and the
calibration rate – will be applied. Further details regarding the
specific implementation of the BCA and BTA extensions are provided in
the subsections describing the corresponding benefit.

**Benefit Take-up Adjustments (BTA):** This extension enables users to
implement non-take-up corrections.

It is utilised in the simulation of the Guaranteed Minimum Income
(bsamm_cy). The default baseline setting is off.

When the extension is on, a share of (weighted) eligible observations
equal to the take-up rate is selected randomly as beneficiaries,
removing the benefit from the remaining eligible observations; when off,
all eligible observations are kept as beneficiaries.

This extension shares most of its functions with the BCA extension. As a
general rule, only one extension should be active; however, if both are
enabled, the lower of the two rates – between the take-up rate and the
calibration rate – will be applied. Further details on the specific
implementation of the BCA and BTA extensions are provided in the
subsections describing the corresponding benefit.

- **Consumption Inflation Adjustment (CIA):** this extension enables
  users to simulate price (inflation) shocks under the assumption that
  households do not immediately adjust their consumption patterns
  (constant quantities) in response to a sudden change. This extension
  can only be enabled if used together with Consumption Taxes add-ons
  CT_XBASE and CT_XCQ, respectively baseline and constant quantities. By
  default, the extension is switched off. Switching on the inflation
  simulation (without changing parameters) allows users to apply
  [official annual inflation
  rates](https://euromod-web.jrc.ec.europa.eu/sites/default/files/Inflation_rates_by_product_category.xlsx)
  between two consecutive years (sourced from
  [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_manr/default/table?lang=en)
  and [DG ECFIN’s latest quarterly
  forecasts](https://economy-finance.ec.europa.eu/document/download/6e6837c1-e00c-42ed-9f10-8d1ad56f913a_en?filename=spring_forecast-2024_statisical%20annext_en.pdf))
  as stored in the Consumption Taxes (CT) table by
  *\$tco_base_upr\_\[COICOP\].* Users can also simulate their own
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
  calculate *ydsyc_a = (hh_dpit+1 – hh_dpit)/hh_dpit*\]

## Benefits

### Unemployment benefit/Επίδομα ανεργίας (bunct_cy)

<span id="_Toc222326619" class="anchor"></span>**Table 2.5** Key
features of the unemployment benefit

<table style="width:66%;">
<colgroup>
<col style="width: 8%" />
<col style="width: 13%" />
<col style="width: 7%" />
<col style="width: 1%" />
<col style="width: 7%" />
<col style="width: 0%" />
<col style="width: 1%" />
<col style="width: 5%" />
<col style="width: 3%" />
<col style="width: 2%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;"></th>
<th style="text-align: left;"></th>
<th colspan="2" style="text-align: left;"><strong>2022</strong></th>
<th colspan="2" style="text-align: left;"><strong>2023</strong></th>
<th colspan="3" style="text-align: left;"><strong>2024</strong></th>
<th colspan="2" style="text-align: left;"><strong>2025</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Eligibility</strong></td>
<td style="text-align: left;">Contribution period</td>
<td colspan="9" style="text-align: left;">26 contribution weeks with
employment income subject to SIC.</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Contributed amount</td>
<td colspan="9" style="text-align: left;">Twenty times the weekly amount
of basic insurable earnings (see below).</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Other conditions</td>
<td colspan="9" style="text-align: left;">Age ranges from 16 to 63 (65
if not eligible for a statutory pension), not unable to work, not on
leave, and no other employment income.</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Self-employed</td>
<td colspan="9" style="text-align: left;">No.</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Payment</strong></td>
<td style="text-align: left;">Contribution base</td>
<td colspan="9" style="text-align: left;">Average weekly paid and
credited insured earnings (employment income) for the previous
contribution year.</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Basic amount</td>
<td colspan="9" style="text-align: left;">60% of the contribution
base</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Additional amounts</td>
<td colspan="9" style="text-align: left;"><p>Supplementary amounts in
the case of:</p>
<ul>
<li><p>dependent spouse: 20%</p></li>
<li><p>dependent children/other dependants (up to 2): 10%</p></li>
<li><p>50% of the contribution base exceeding the basic insured earnings
up to the level of the basic insured earnings.</p></li>
</ul></td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Floor</td>
<td colspan="9" style="text-align: left;">No minimum amount.</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Ceiling of the basic amount (€):</td>
<td colspan="9" style="text-align: left;">60% of <em>basic insurable
earnings</em> of:</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;"><em>in weekly terms:<br />
in annual terms:</em></td>
<td colspan="2" style="text-align: left;">183.96<br />
9,682</td>
<td colspan="3" style="text-align: left;">186.20<br />
10,008</td>
<td colspan="3" style="text-align: left;">192.47<br />
10,482</td>
<td style="text-align: left;">201.57<br />
11,104</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Duration</strong></td>
<td style="text-align: left;">Standard</td>
<td colspan="9" style="text-align: left;">156 working days (Sundays
excluded, 6 months)</td>
</tr>
<tr>
<td rowspan="2" style="text-align: left;"><strong>Subject
to:</strong></td>
<td style="text-align: left;">Taxes</td>
<td style="text-align: left;">No.</td>
<td colspan="2" style="text-align: left;"></td>
<td colspan="3" style="text-align: left;"></td>
<td colspan="3" style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;">SIC</td>
<td style="text-align: left;">No.</td>
<td colspan="2" style="text-align: left;"></td>
<td colspan="3" style="text-align: left;"></td>
<td colspan="3" style="text-align: left;"></td>
</tr>
</tbody>
</table>

Source: [Insurable Earnings 1981-2025, Ministry of Labour, Welfare and
Social Insurance, Social Insurance
Services.](https://www.mlsi.gov.cy/mlsi/sid/sidv2.nsf/All/109C23F9B530F193C2257DB700288564?OpenDocument)

#### Definitions

The unemployment benefit is available to insured employees working in
Cyprus or to voluntary contributors employed abroad by a Cypriot
employer. Insured individuals must be between 16 and 63 years old to
qualify for the benefit. The upper age limit of 63 can be extended to 65
if the applicant is not eligible for an old-age pension. Any insured
person may apply for unemployment benefits for the days they are
unemployed, provided they are able and willing to accept employment.
Conversely, they are not considered unemployed:

When they are incapable of work due to sickness;

When they are on leave;

On Sundays;

On days they engage in any occupation alongside their usual work, from
which they earn a salary that is at least equal to 1/12 of the basic
insurable earnings.

On any day for which their employer pays contributions for them.

The following categories of individuals are regarded as dependants of
the insured person: their spouse, any children under the age of 15, an
unmarried daughter aged 15 to 23 if she is a student, an unmarried son
aged 15 to 25 if he is a student or serving in the military, an
unmarried child who is permanently incapable of self-support regardless
of age, a disabled spouse if they are supported by the insured
individual, the father or mother of the insured person if they are
unable to work and financially dependent on them, and a younger brother
or sister if the insured person provides financial support for them.

#### Eligibility conditions

The eligibility requirements for receiving unemployment benefits are:

1.  A minimum of 26 weeks must have elapsed between the individual
    becoming insured and the day they became unemployed. Throughout that
    period, the total insured earnings must be at least 26 times the
    weekly basic insurable earnings.

2.  The applicant has either paid [^3] or been credited[^4] with
    contributions in the previous contribution year [^5]. Insured
    earnings must total at least 20 times the weekly amount of basic
    insurable earnings during this period.

Regarding the requirements mentioned above, the contributions of
self-employed individuals are not considered. By contrast, the
contributions of optionally insured persons are taken into account only
if they relate to work abroad with a Cypriot employer.

***EUROMOD modelling:** The model controls for the first condition using
a variable on working history. As for the second, it utilises employment
income.*

The benefit is payable for 156 working days for each period of
employment interruption.

An unemployed person who has exhausted his or her entitlement to
unemployment benefits may be allowed to receive them again if he or she
works and pays contributions on earnings that total at least 26 times
the weekly amount of basic insured earnings, provided that at least 26
weeks have passed since the last day the person received the benefit.

If an unemployed individual is over 60 and is not entitled to a pension
from any professional scheme, they are eligible for unemployment
benefits, provided they have worked and paid contributions on earnings
amounting to no less than 26 times the weekly rate of basic insured
earnings, and at least 13 weeks have passed since the last day they
received unemployment benefits.

***EUROMOD modelling:** The rules described above are not simulated in
the model.*

The applicant loses entitlement to the unemployment benefit for up to
six weeks if he/she:

1.  loses his/her employment by his/her own fault or abandons it without
    excuse,

<!-- -->

3.  refuses or omits to apply for proper employment or to accept proper
    employment offered to him/her,

4.  fails or neglects to be employed in a suitable job and

5.  refuses, or omits without excuse, to attend professional training
    lessons.

***EUROMOD modelling:** EUROMOD does not control for these conditions.*

#### Income test

There is no income test.

#### Benefit amount

The level of the unemployment benefit is based on the insured person's
mean weekly paid and credited insured earnings during the previous
contribution year.

The unemployment benefit includes a basic and a supplementary amount.
The weekly basic amount equals 60% of the mean weekly insured earnings
(up to the weekly basic insurable amount) during the previous
contribution year. This increases by a further 20% if there is a
dependent spouse and by 10% for every child [^6] or other dependent[^7]
(NB: The maximum number of dependent children/other dependents is two).
If both spouses are eligible to receive unemployment benefits, the
increase for dependents is paid only to the spouse entitled to the
highest increase.

The weekly supplementary amount equals 50% of the amount by which the
beneficiary's mean weekly insured earnings in the previous contribution
year exceed the weekly basic insurable earnings. However, this
supplementary amount must not exceed the weekly basic insurable
earnings.

If, in addition to the unemployment benefit, the insured person is
entitled to other provisions of the Social Insurance Fund, only the
benefit with the highest rate is paid. This rule does not apply if the
beneficiaries are entitled to unemployment benefits and a widow's
pension or a missing person's allowance. In that case, both provisions
are paid to the person, and the increase for dependants is paid on
whichever benefit is higher.

***Note on EUROMOD implementation:** Dependants other than the spouse's
and the recipient's children are not taken into account in the
calculations. However, such cases are very rare in practice.*

### Child benefit/Επίδομα Τέκνου (bch_cy)

#### Definitions

Child benefit is a non-contributory benefit offered to families with
dependent children. This benefit is means-tested and available to
families residing in Cyprus for at least 3 consecutive years. As of 1
January 2018, the residence requirement increased from 3 to 5 years of
living in Cyprus. The relevant law defines “dependent children” as
individuals who are: 1) up to 18 years old; 2) up to 20 years old if
they continue to attend secondary education; 3) up to 21 years old if
they serve in the National Guard; and 4) regardless of age, if they are
permanently unable to support themselves (e.g., children with
disabilities).

The benefit amount is determined by the number of children and the gross
annual family income. It consists of a basic component and a
supplementary component. The benefit is paid to the mother or, in her
absence, to the father or the guardian responsible for the children if
both parents are deceased. Finally, the child benefit is not subject to
tax.

#### Eligibility conditions

A family is entitled to the benefit only if their *annual family income*
(before taxes) does not exceed:

€49,000 for families with one dependent child,

€59,000 for families with two dependent children,

Effective from 1 January 2018, the threshold increases by €5,000 for
each additional child in families with three or more children (for
instance, the threshold is €64,000 for a family with three dependent
children and €69,000 for four dependent children).

Moreover, a family is not eligible for the benefit if its total property
value (including real estate, shares, bonds, securities, and deposits)
exceeds €1.2 million.

#### Income test

Family income is defined as the total annual gross income received in
the year preceding the benefit application. This includes wages and
salaries of all family members, pensions, capital income, rents, and
social benefits (including GMI). The child benefit is paid annually and
is non-taxable.

#### Benefit amount

The benefit amount is determined by the number of dependent children and
the family income, as illustrated in the table below.

<span id="_Toc222326620" class="anchor"></span>**Table 2.6** Benefit
levels for 2022-2025 (annual amounts per child, in EUR)

<table style="width:65%;">
<colgroup>
<col style="width: 16%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;"></th>
<th colspan="4" style="text-align: left;"><strong>Benefit amounts for
families with income:</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"></td>
<td><strong>up to 19,500</strong></td>
<td><strong>19,500.01 -39,000</strong></td>
<td><strong>39,000.01 - 49,000</strong></td>
<td><strong>49,000.01 - 59,000*</strong></td>
</tr>
<tr>
<td colspan="5" style="text-align: center;"><strong>2022</strong></td>
</tr>
<tr>
<td style="text-align: left;">Family with 1 child</td>
<td>496.42</td>
<td>444.17</td>
<td>397.14</td>
<td>0.00</td>
</tr>
<tr>
<td style="text-align: left;">with 2 children</td>
<td>595.71</td>
<td>543.45</td>
<td>397.14</td>
<td>360.56</td>
</tr>
<tr>
<td style="text-align: left;">with 3 children</td>
<td>1,092.13</td>
<td>1,039.87</td>
<td>794.28</td>
<td>721.12</td>
</tr>
<tr>
<td style="text-align: left;">with 4+ children</td>
<td>1,750.54</td>
<td>1,593.78</td>
<td>1,316.83</td>
<td>1,186.19</td>
</tr>
<tr>
<td colspan="5" style="text-align: center;"><strong>2023</strong></td>
</tr>
<tr>
<td style="text-align: left;">Family with 1 child</td>
<td>539.98</td>
<td>483.14</td>
<td>431.98</td>
<td>0.00</td>
</tr>
<tr>
<td style="text-align: left;">with 2 children</td>
<td>647.98</td>
<td>591.14</td>
<td>431.98</td>
<td>392.20</td>
</tr>
<tr>
<td style="text-align: left;">with 3 children</td>
<td>1,187.96</td>
<td>1,131.12</td>
<td>863.97</td>
<td>784.39</td>
</tr>
<tr>
<td style="text-align: left;">with 4+ children</td>
<td>1,904.14</td>
<td>1,733.62</td>
<td>1,432.37</td>
<td>1,290.27</td>
</tr>
<tr>
<td colspan="5" style="text-align: center;"><strong>2024</strong></td>
</tr>
<tr>
<td style="text-align: left;">Family with 1 child</td>
<td>559.74</td>
<td>500.82</td>
<td>447.79</td>
<td>0.00</td>
</tr>
<tr>
<td style="text-align: left;">with 2 children</td>
<td>671.69</td>
<td>612.77</td>
<td>447.79</td>
<td>406.55</td>
</tr>
<tr>
<td style="text-align: left;">with 3 children</td>
<td>1,231.43</td>
<td>1,172.51</td>
<td>895.58</td>
<td>813.10</td>
</tr>
<tr>
<td style="text-align: left;">with 4+ children</td>
<td>1,973.82</td>
<td>1,797.06</td>
<td>1,484.78</td>
<td>1,337.48</td>
</tr>
<tr>
<td colspan="5" style="text-align: center;"><strong>2025</strong></td>
</tr>
<tr>
<td style="text-align: left;">Family with 1 child</td>
<td>599.00</td>
<td>535.84</td>
<td>478.79</td>
<td>0.00</td>
</tr>
<tr>
<td style="text-align: left;">with 2 children</td>
<td>718.18</td>
<td>655.02</td>
<td>478.79</td>
<td>434.98</td>
</tr>
<tr>
<td style="text-align: left;">with 3 children</td>
<td>1,317.18</td>
<td>1,254.02</td>
<td>957.58</td>
<td>869.97</td>
</tr>
<tr>
<td style="text-align: left;">with 4+ children</td>
<td>2,111.77</td>
<td>1,922.29</td>
<td>1,588.15</td>
<td>1,430.25</td>
</tr>
</tbody>
</table>

**Note:** \* Since 2018, this income threshold increases by €5,000 for
each additional child for families with three or more children.

Source: [Welfare Benefit Services, Deputy Ministry of Social
Welfare](https://www.wbas.dmsw.gov.cy/dmsw/ydep.nsf/All/67BC9C0D98FA34B4C22587D5003E83C1?OpenDocument)

***EUROMOD modelling:** The income test uses current income rather than
the previous year's income. The benefit is allocated to the head of the
tax unit. Furthermore, the student grant is included in the
means-testing of the benefit, whereas the reverse does not apply. Social
assistance is excluded from the income list. Due to data limitations,
the period of residency in Cyprus is not considered in the model.*

### Single-parent benefit/Επίδομα μονογονεϊκής οικογένειας (bchlp_cy)

#### Definitions

The single-parent benefit is a non-contributory, means-tested allowance
for single parents with dependent children. Single-parent families
consist of one parent living with at least one dependent child. The
single parent may be unmarried, widowed, or divorced. Eligible
recipients must have already applied for the Child Benefit (which
indicates that the exact definition of dependent children applies to
both benefits). This benefit is not taxable.

#### Eligibility conditions

The recipients should be eligible for the Child Benefit. The definition
of a single-parent family is as outlined above. The recipients may be
either Cypriots or EU citizens who have lived in Cyprus for at least
three years. On January 1, 2018, the residence requirement changed from
3 to 5 years.

#### Income test

The benefit is subject to means testing. The income test considers the
gross family income earned in the year preceding the application. Family
income is defined in the same way as for the child benefit.

#### Benefit amount

The benefit amount is based on the gross family income:

<span id="_Toc222326621" class="anchor"></span>**Table 2.7** Benefit
levels for 2022-2025 (monthly amounts per child, in EUR)

| **Family income** | **2022** | **2023** | **2024** | **2025** |
|-------------------|----------|----------|----------|----------|
| 0 – 39,000        | 188.12   | 204.62   | 212.11   | 215.96   |
| 39,000 – 49,000   | 167.22   | 181.89   | 188.54   | 192.53   |

*Source: [Grants and Benefits Services, Ministry of
Finance](https://www.gov.cy/mof/ypiresia-chorigion-kai-epidomaton/)*

***EUROMOD modelling:** The model does not take into account the period
of residency in Cyprus.*

### Student grant/Φοιτητική χορηγία (bedet_cy)

#### Definitions

The student grant is a means-tested, non-contributory benefit designed
to provide income support to families with members studying in higher
education in institution located either in Cyprus or abroad. [^8]

The law recognises the following family units:

couples with children,

lone parents (divorced, widowed, or unmarried) and their children,

students whose parents are deceased, missing, or have abandoned them,

married students, along with their spouses and children.

students who are divorced or widowed, along with their children.

Furthermore, the law defines children as follows:

children up to 18 years old,

children up to 19 years old if they attend secondary education,

children up to 21 years old if they are serving in the National Guard,

children of any age who are students eligible to receive the student
grant,

children of any age who are disabled or permanently unable to maintain
themselves.

The student grant is awarded either to the student’s parents or to any
individual responsible for covering the student’s expenses. In the first
case, students must either reside in the same household as their parents
or, if they live separately, be financially supported by them.

#### Eligibility conditions

Eligible students must be either Cypriot citizens or EU citizens who
hold permanent residency in Cyprus (permanent residents are defined as
individuals who have lived in Cyprus for at least 30 months during the
three years preceding the start of their studies). If a student is a
non-EU citizen, they may be eligible for the grant if at least one of
their parents has Cyprus or EU citizenship. Furthermore, recipients must
have graduated from a secondary school in Cyprus. Students should be
enrolled in a recognised higher education institution. The grant is
disbursed only for the standard duration of studies, which may vary
across faculties. The payment period may be extended in exceptional
circumstances, such as due to health issues.

The student grant is not available for students who:

are enrolled in language learning programmes that serve as prerequisites
for admission to educational institutions,

are pursuing foundation certificates in higher education or similar
courses,

are studying distance-learning or open university courses,

are enrolled in courses as external students instead of as full-time
students,

are undertaking vocational education or specialisation courses,

are enrolled in PhD programmes.

Finally, the recipients must fulfil specific asset criteria. In
particular, the total value of the family’s immovable and movable
property must not exceed €1.2 million.

#### Income test

Eligibility for the student grant is determined by the recipient's total
gross family income. Total gross family income (accrued in the year
preceding 1 January of the relevant academic year) comprises the
following components: employment income, pensions, rental income, income
from interest or dividends, alimony, the GMI benefit, public assistance,
child benefit[^9], the single-parent benefit, and other benefits or
grants.

The following sources of income are excluded: income derived from the
employment of children who are full-time students, scholarships or other
student benefits, as well as any disability or chronic illness benefits
and grants received by any family member. Income thresholds are
presented in the subsequent tables.

#### Benefit amount

The level of the student grant is determined by the family’s gross
income and comprises a basic amount and a supplementary amount. The
supplementary amount is provided to families that either cover tuition
fees when they exist or have more than three dependent children
(multi-child families).

If the student completes her studies in the first semester of an
academic year, the family is eligible to receive half of the annual
grant.

For part-time studies, the grant is paid when the duration of study
equals one year of full-time study.

[**Table 2.8**](#Table_02_08) indicates the amount of the student grant
allocated to each income group for 2022-2025.

<span id="Table_02_08" class="anchor"></span>**Table 2.8** Student grant
amounts for 2022-2025 (in EUR) [^10]

| **Total Gross Family Income** | **Annual amount per student** | **Additional amount for families paying tuition fees or with more than three dependent children** |
|:---|:---|:---|
| 0 – 39,000 | 1,710 | 855 |
| 39,000.01 – 49,000 | 1,580 | 790 |
| 49,000.01 – 59,000\* | 1,450 | 725 |

Notes: \* Since 2019, the maximum income threshold has increased by
€5,000 for each additional child beyond the second child. For instance,
the maximum income threshold for a family with three children is
€64,000.

Source: [**Grants and Benefits Services, Ministry of
Finance**](https://www.gov.cy/mof/ypiresia-chorigion-kai-epidomaton/)

***Note on EUROMOD implementation:** The model cannot fully account for
all provisions of the law. Under the current implementation, the grant
is allocated to families with dependent children enrolled in an
educational programme corresponding to ISCED levels 5 or 6. As it is not
feasible to account for fee payments, the only additional amount
simulated is for families with multiple children. It is also important
to note that social assistance is not included in the calculation of
family income. Eligibility for students aged 19 and older is further
restricted to those without their own original income, based on the
assumption that their parents will provide support.*

### Standard birth grant/Βοήθημα Τοκετού (bchba_cy)

#### Definitions

The standard birth grant is a contributory benefit paid to the mother of
a newborn child, provided that either she or her spouse is insured,
regardless of whether they are employed, self-employed, or voluntarily
insured.

#### Eligibility conditions

The conditions for qualifying for the maternity grant are:

1.  The birth of a live child or a stillborn child after at least 28
    weeks of pregnancy.

<!-- -->

6.  The applicant or their spouse must have been insured for a minimum
    of 26 weeks. The total insured earnings must be at least 26 times
    the weekly basic insurable earnings.

7.  The applicant or spouse has paid or been credited with contributions
    in the previous contribution year. During this period, the insured
    earnings must be at least 20 times the weekly basic insurable
    earnings.

#### Income test

No income test applies.

#### Benefit amount

The maternity grant is paid as a lump sum upon the birth of a child. The
amount payable for each child was:

€580.92 for 2022

€600.48 for 2023

€600.48 for 2024

€628.92 for 2025

***EUROMOD modelling:** This benefit is granted to all heads of families
with children aged 0, where at least one parent has a work history of at
least 6 months (26 weeks) and annual earnings of at least 20 times the
weekly amount of basic insured earnings.*

### Special birth grant for unmarried mothers/Ειδικό βοήθημα τοκετού σε άγαμες μητέρες (bchba_cy)

#### Eligibility conditions

Women who give birth and have resided in Cyprus continuously for 12
months prior to giving birth are eligible for the special maternity
grant, provided they are not already receiving the maternity grant from
the Social Insurance Services.

#### Benefit amount

The special birth grant is the same amount as the maternity grant for
that year (e.g., €628.92 in 2025) and is paid as a lump sum on
childbirth.

***EUROMOD modelling**: The period of residency in Cyprus is not
accounted for in the model.*

### Maternity allowance /Επίδομα μητρότητας, (bmact_cy)

#### Definitions

Maternity allowance is a contributory benefit that compensates mothers
(including adoptive mothers) for the income they lose during their
maternity leave. It covers women who are employees or self-employed
working in Cyprus. It also extends to women who opt to be voluntarily
insured while employed by a Cypriot employer with operations abroad.

#### Eligibility conditions 

Eligible recipients must:

be on maternity leave and not receive a full wage from their employer.
In cases where wages are reduced (as permitted under certain collective
agreements), the combined total of the reduced wage and the benefit must
not exceed the full wage.

have paid social insurance contributions for at least 26 weeks by the
start of the week in which their maternity leave begins,

have paid contributions of at least 26 times the weekly amount of basic
insurable earnings of the previous year [^11] by the start of their
maternity leave (0.5 insurance points), [^12]

have paid and/or accumulated contributions amounting to at least 20
times the weekly basic insurable earnings (0.39 insurance points) in the
previous contribution year.

NB: The last three conditions are similar to the eligibility
requirements for unemployment insurance benefits.

#### Income test

There is no income test.

#### Benefit duration

The benefit duration is 18 weeks for the first child. This can be
extended to 21 weeks under certain conditions, such as prolonged
hospitalisation of the newborn due to premature delivery or health
issues. For twins, the period is extended by 4 weeks, and for triplets,
by 8 weeks. In all cases, maternity leave must start at least two weeks
before the expected due date.

An amendment to the social insurance law, enacted on 5 November 2021,
extends maternity benefits to 22 weeks for the second child and to 26
weeks for the third and subsequent children.

#### Benefit amount

The maternity benefit is calculated on a weekly basis and consists of a
basic part and a supplementary part:

The weekly rate of the basic part is equal to 72% of the employee's
weekly basic insurable earnings for the previous year. This rate
increases to 80%, 90%, and 100% for one, two, or three dependants,
respectively (with a maximum of three dependants), if the mother is a
lone parent or the father is considered a dependant spouse. For the
latter, the father must be neither working nor receiving any other
contributory benefit.

The weekly rate of the supplementary part is 72% of the portion of the
average weekly insurable earnings that exceeds last year's basic
insurable earnings, up to a maximum amount (of €1,209 per week in 2025).

#### Subject to taxes/SIC

The benefit is not subject to taxes or SICs.

#### Take up

There are no data on take-up. However, the take-up rate is expected to
be very high.

### Paternity allowance /Επίδομα πατρότητας (bpact_cy) 

#### Definitions

Paternity allowance is a contributory benefit that compensates fathers
(including adoptive fathers) for the income they lose during their
parental leave. It covers fathers of newborns who are employees or
self-employed and working in Cyprus. It also extends to men who choose
to be voluntarily insured while employed by a Cypriot employer with
operations abroad.

The benefit was introduced in August 2017 and initially covered only
married fathers. By December 2022, it had been extended to include all
fathers, regardless of marital status. However, it does not include
those without custody rights.

#### Eligibility conditions

The same eligibility criteria as for maternity benefits must be
satisfied.

#### Income test

There is no income test.

#### Benefit duration 

The benefit duration is 2 weeks. This can be extended in cases where the
mother dies during labour or maternity leave.

#### Benefit amount 

The paternity benefit is calculated in the same way as the maternity
benefit.

#### Subject to taxes/SIC

The benefit is not subject to taxes or SICs.

#### Take up

There are no available data on take-up.

### Guaranteed Minimum Income/Ελάχιστο Εγγυημένο Εισόδημα (bsamm_cy)

#### Definitions

The Guaranteed Minimum Income (GMI) scheme is a means-tested,
non-contributory top-up benefit designed for individuals or families
whose incomes are insufficient to meet their basic needs. Basic needs
are assessed using a minimum consumption basket that defines the
essential goods and services required for a standard level of living.
The GMI scheme replaced Social Assistance in 2014.

The unit of assessment is the family, consisting of:

The claimant,

His/her spouse,

Children under the age of 18,

Unmarried children under 28 years of age, regardless of whether they
live with their parents or not (except for those who reside abroad).

#### Eligibility conditions

The following categories of individuals may apply for the benefit,
provided they have lived in the country for the past five years:

Every citizen of the Republic,

EU citizens,

Third-country nationals, if they have received the status of long-term
resident or are refugees (excluding asylum seekers),

Victims of human trafficking.

Additionally, the claimant must fall into one of the following
categories:

At least 28 years old

Married, irrespective of age

A single parent, irrespective of age

An orphan, irrespective of age

A disabled adult, irrespective of age, who, before reaching 18 years
old, was under the care of Social Welfare Services.

Finally, several special categories are not eligible for the benefit,
including monks, individuals serving in the National Guard, and students
(excluding those under the care of Social Welfare Services, orphans, the
disabled, and those voluntarily unemployed).

#### Income test

GMI is a top-up benefit. Social welfare services calculate the cost to
cover the recipients’ basic needs and their family income. The
difference is then given to the eligible recipients as a top-up to their
current income. Family income is the sum of the monetary incomes of all
family members (the recipient unit). A portion of any employment income
earned is exempted from the definition of family income according to the
following schedule:

<span id="_Toc222326623" class="anchor"></span>**Table 2.9** Exempted
labour income (in EUR)

<table style="width:65%;">
<colgroup>
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 19%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th colspan="2" style="text-align: left;">Labour income earned by the
claimant and/or his/her spouse</th>
<th colspan="2" style="text-align: left;">Labour income earned by a
family child</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">Earnings brackets</td>
<td style="text-align: left;">Exemption rate</td>
<td style="text-align: left;">Earnings brackets</td>
<td style="text-align: left;">Exemption rate</td>
</tr>
<tr>
<td style="text-align: left;">Up to 50</td>
<td style="text-align: left;">100%</td>
<td style="text-align: left;">Up to 480</td>
<td style="text-align: left;">50%</td>
</tr>
<tr>
<td style="text-align: left;">50.01 – 200</td>
<td style="text-align: left;">40%</td>
<td style="text-align: left;">480.01 – 1,000</td>
<td style="text-align: left;">90%</td>
</tr>
<tr>
<td style="text-align: left;">200.01 – 500</td>
<td style="text-align: left;">20%</td>
<td style="text-align: left;">1,000.01 – 2,000</td>
<td style="text-align: left;">85%</td>
</tr>
<tr>
<td style="text-align: left;">500.01 and above</td>
<td style="text-align: left;">0%</td>
<td style="text-align: left;">2,000.01 and above</td>
<td style="text-align: left;">80%</td>
</tr>
<tr>
<td colspan="4" style="text-align: left;"></td>
</tr>
</tbody>
</table>

**Notes**: The exemption rate increases to 100% for the first 512 euros
of income earned by a family member who is disabled or by a family
member whose spouse is disabled.

Source: [Welfare Benefit Services, Deputy Ministry of Social
Welfare](https://www.wbas.dmsw.gov.cy/dmsw/ydep.nsf/All/D61276624117BB62C22587C30035D819?OpenDocument#9)

The following examples examine straightforward cases of exemption
calculations:

<u>Example 1</u>: If the claimant is the sole earner in the family,
earning €200, then €110 (i.e., the first €50, plus 40% of the remaining
€150 up to the total earnings amount of €200) is exempt. Consequently,
only €90 (=€200-€110) is used to calculate the GMI.

<u>Example 2</u>: If the claimant has a child under the age of 28
(regardless of whether they live with them) who is also the sole earner
in the family, earning €1,000, then €708 (i.e., 50% of €480, plus 90% of
the remaining €520 to the total earnings amount of €1000) is exempt.
Therefore, only €292 (€1000 - €708) will be used to calculate GMI.

Furthermore, the following benefits/pensions are not considered in the
calculation of family income:

Funeral grant

Birth grant

Student grant

Military grant

Financial aid to low-income pensioners

Donations to philanthropic institutions

Alimony (only in case the claimant can prove that they are not paid to
him/her)

Benefits to disabled persons

Income from participation in employment or training schemes.

Assistance through the Welfare Lottery Fund or from the Ministry of
Labour and Social Insurance, provided as ad hoc financial aid upon the
Minister's approval.

#### Asset test

The total value of family immovable property should not exceed €100,000.
In the case of a mortgage, €100,000 is exempt from the calculation.
Additionally, if the family resides in a family-owned house, it is
exempt from the calculations if the house is under 300 square metres.

The movable property should be below €5,000, with this amount increasing
by €1,000 for each additional family member. However, deposits of up to
€20,000 are excluded, provided the following conditions are met:

are for mortgage (which occurred before the law implementation in 2014)

belong to minors of the family (which occurred before the law
implementation in 2014)

belong to minors of the family and acquired after a fundraiser or other
special conditions

are used for student loans

are in the same account with an old-age parent (which occurred before
the law implementation in 2014).

are necessary for health reasons, rehabilitation, treatments, or for
people with disabilities.

#### Benefit amount

Basic income is the minimum monetary amount required to ensure
recipients have access to a comprehensive basket of goods and services
that meets the minimum standard of living established by society.
Currently, the value of this basket is €480 for a single individual and
increases proportionally with the size of the recipient unit, according
to OECD equivalence scales. The OECD scales assign a value of 0.5 for
each additional adult and 0.3 for each additional child, with children
defined as persons under 14 years old. For instance, for a couple with a
13-year-old child, the total basic amount is calculated as 480 + 0.5 x
480 + 0.3 x 480 = 864 euros.

If the basic amount exceeds the family income, the difference is paid to
the eligible recipient. Furthermore, the benefit amount is supplemented
with a housing allowance (see details in Table 2-10). Renters and
homeowners who are unable to repay their mortgage loans qualify for the
housing allowance.

<span id="_Toc222326624" class="anchor"></span>**Table 2.10** Housing
Allowance (in EUR)

<table style="width:65%;">
<colgroup>
<col style="width: 19%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 7%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;"><strong>Family Unit type</strong></th>
<th style="text-align: left;"><p><strong>Nicosia</strong></p>
<p><strong>(4.06/m<sup>2</sup>)</strong></p></th>
<th style="text-align: left;"><p><strong>Limassol</strong></p>
<p><strong>(4.41/m<sup>2</sup>)</strong></p></th>
<th style="text-align: left;"><p><strong>Famagusta</strong></p>
<p><strong>(2.94/m<sup>2</sup>)</strong></p></th>
<th style="text-align: left;"><p><strong>Larnaca</strong></p>
<p><strong>(3.50/m<sup>2</sup>)</strong></p></th>
<th style="text-align: left;"><p><strong>Paphos</strong></p>
<p><strong>(2.94/m<sup>2</sup>)</strong></p></th>
<th style="text-align: left;"><p><strong>Average</strong></p>
<p><strong>(3.88/m<sup>2</sup>)</strong></p></th>
</tr>
</thead>
<tbody>
<tr>
<td>Couple or single parent with no children</td>
<td>223.30</td>
<td>242.55</td>
<td>161.70</td>
<td>192.50</td>
<td>161.70</td>
<td>213.48</td>
</tr>
<tr>
<td>Couple or single parent with 1 child</td>
<td>324.80</td>
<td>352.80</td>
<td>235.20</td>
<td>280.00</td>
<td>235.20</td>
<td>310.48</td>
</tr>
<tr>
<td>Couple or single parent with two minor children of the same sex</td>
<td>324.80</td>
<td>352.80</td>
<td>235.20</td>
<td>280.00</td>
<td>235.20</td>
<td>310.48</td>
</tr>
<tr>
<td>Couple or single parent with 2 adult children</td>
<td>406.00</td>
<td>441.00</td>
<td>294.00</td>
<td>350.00</td>
<td>294.00</td>
<td>388.13</td>
</tr>
<tr>
<td>Couple or single parent, one adult child and one minor child</td>
<td>406.00</td>
<td>441.00</td>
<td>294.00</td>
<td>350.00</td>
<td>294.00</td>
<td>388.13</td>
</tr>
<tr>
<td>Couple or single parent with three minor children</td>
<td>406.00</td>
<td>441.00</td>
<td>294.00</td>
<td>350.00</td>
<td>294.00</td>
<td>388.13</td>
</tr>
<tr>
<td>-&gt; larger families (for each additional child or two additional
minor children of the same sex)</td>
<td>81.20</td>
<td>88.20</td>
<td>58.80</td>
<td>70.00</td>
<td>58.80</td>
<td>77.66</td>
</tr>
<tr>
<td>-&gt; for each person with a disability</td>
<td>101.50</td>
<td>110.25</td>
<td>73.50</td>
<td>87.50</td>
<td>73.50</td>
<td>97.00</td>
</tr>
</tbody>
</table>

**Note:** Minor child if aged \< 18, adult child if aged ≥ 18.

Source: [Welfare Benefit Services, Deputy Ministry of Social
Welfare](https://www.wbas.dmsw.gov.cy/dmsw/ydep.nsf/All/D61276624117BB62C22587C30035D819?OpenDocument#13)

***EUROMOD modelling (Policy rules):***

*Due to data limitations, the asset test is not implemented in the
model. Furthermore, in the calculation of the housing allowance,
regional differences cannot be taken into account, and the weighted
average (rightmost column of Table 2-10) is applied instead.*

*The adjustment of earnings exemptions due to disability is currently
not taken into account.*

*Some special categories of recipients (e.g., orphans, persons with
disabilities, individuals under the care of Social Welfare Services)
cannot be identified by the model.*

*Furthermore, according to the model's premises, claimants cannot be
students, and all unemployed persons are considered involuntarily
unemployed.*

*For the simulation, we adopted the following income list: original
income (without excluding alimony paid), statutory pensions, survivor
pensions, health benefits, unemployment benefits, scholarships, housing
benefits, child benefits and family-related benefits.*

*Finally, all families eligible for the basic benefit and paying
mortgage interest are considered eligible for the housing allowance.*

***EUROMOD modelling (Take-up adjustments)**:*

*BTA and BCA extensions are disabled, so the baseline model neither
adjusts for non-take-up of the benefit nor calibrates its receipt;
however, the user can activate them if necessary. See section 2.4 for
technical details on both extensions and their interactions.*

*Users can enable the necessary extensions in Country Tools/Set
Switches. For proper functioning, the extensions require the following
inputs:*

*BTA: The estimated take-up rate of the benefit should be set as the
value of the \$bsamm_BTA_rate constant in the model. Currently, the
value is set to 1, indicating no adjustment for non-take-up.*

*BCA: The total number of benefit recipients needs to be filled out in
the External Statistics table so that the calibration rate
(\$bsamm_BCA_rate) is computed accordingly. Data are currently available
for the years 2019-2024. Given the absence of information for 2025, the
calibration rate is not calculated within the 2025 system; instead, the
one computed within the 2024 system is used. For the modelling of
reforms, the 2025 system should be used to allow for variation in the
number of beneficiaries (hence expenditure): beneficiaries will change
when eligibility conditions change, by applying the 2024 share to the
new pool of eligible units. If previous systems were used for reforms,
the total number of beneficiaries would remain constant irrespective of
the reform applied, since the model would always stick to the existing
external statistics.*

### Low pension benefit/ Επίδομα χαμηλοσυνταξιούχου (bsaoa_cy)

#### Definitions

The low pension benefit is a non-contributory support aimed at families
with incomes below a poverty threshold. It is a means-tested benefit
provided to families with at least one member receiving a pension. This
policy was introduced on 1 December 2009 and came into effect on 1 March
2010. With the introduction of the GMI in 2014, an individual can apply
for either the GMI or the low pension benefit and receives the higher of
the two if eligible for both. Previously, people eligible for both
benefits would receive the low pension benefit plus the difference
between this and the public assistance benefit, which was the precursor
to GMI.

The unit of assessment is the family consisting of:

The claimant

His/her spouse

Children under the age of 18

Female children up to 23 years old, provided that they attend secondary
or tertiary education

Male children up to 25 years old, provided that they attend secondary or
tertiary education, or are serving in the National Guard

Children, irrespective of their age, who are eligible to receive the
student grant

Children, irrespective of their age, who are disabled or permanently
deprived of the ability to maintain themselves

#### Eligibility conditions

An individual is deemed eligible if he or she receives any pension from
the following three categories:

Pension from the Social Insurance Services

Social pension

Pension from an occupational pension scheme as it applies in Cyprus

Once the above conditions are met, any individual may apply for the
benefit, provided they are Cypriot residents and have maintained their
legal and continuous residence in areas under the effective control of
the Republic of Cyprus for at least one year before applying. They must
also maintain continuous residence in the Republic for as long as they
receive the benefit, with no absence exceeding 3 months in any calendar
year.

Since 1 January 2021, an additional eligibility condition (“asset test”)
has been introduced regarding household deposits, which must be below
€100,000. The calculation of household deposits includes any alienations
of deposits made in the two years preceding the year of application,
unless such alienations are justified as imperative and necessary. From
1 January 2023, the alienation period has been extended to three years.

#### Income test

Eligibility for and the amount of the low pension benefit depend on the
family's total income in the previous year and the total pension in the
current year at the time of assessment. These assessments occur when
applying for the benefit and during subsequent re-evaluations.

The total family income must be below the poverty threshold set by the
Council of Ministers. This is currently €10,324 for single-person
households and is further adjusted (scaled up) based on household
composition. Specifically, this amount is multiplied by a scaling factor
of 1, plus 0.5 for each additional person aged 14 or over and 0.3 for
each child under 14.[^13]

The total family income includes any pension received in Cyprus or
abroad, income from employment, rents, interest, dividends, and other
benefits such as orphan's benefit, unemployment benefit, sickness
benefit, child benefit, and single parent benefit. However, it does not
include any disability benefits, student grants, maternity and
employment injury benefits, the GMI, Easter, or low pension benefits.

#### Benefit amount

[**Table 2.11**](#Table_02_11) and [**Table 2.12**](#Table_02_12)
provide details on the base monthly amount of the low pension benefit
for households with one or two pensioners, which depends on the family's
annual income. The total family income *after* receiving the benefit
must not exceed 120% of the poverty threshold, adjusted for household
composition; the benefit level in the highest income bracket is
therefore lowered accordingly.

Once the base monthly amount is calculated, it is adjusted according to
family composition to determine the total family benefit. Specifically,
the base amount is multiplied by a scaling factor that is calculated by
adding 1 for each pensioner, 0.5 for a non-pensioner spouse, and 0.3 for
each additional member. The scaling factor must not exceed 3.

The resulting benefit is paid twelve times a year, divided equally
between the two pensioners in households with two pensioners.

<span id="Table_02_11" class="anchor"></span>**Table 2.11** Monthly low
pension benefit amounts, 1/1/2021 to 31/5/2023

<table style="width:76%;">
<colgroup>
<col style="width: 7%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 8%" />
<col style="width: 10%" />
<col style="width: 7%" />
<col style="width: 8%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 9%" />
</colgroup>
<thead>
<tr>
<th colspan="5" style="text-align: center;"><strong>One-pensioner
household</strong></th>
<th colspan="5" style="text-align: center;"><strong>Two-pensioner
household</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: center;"><strong>Total monthly income
before the benefit</strong></td>
<td colspan="2" style="text-align: center;"><strong>Monthly
Benefit</strong></td>
<td style="text-align: center;"><strong>Total monthly income after the
benefit</strong></td>
<td colspan="2" style="text-align: center;"><strong>Total monthly income
before the benefit</strong></td>
<td colspan="2" style="text-align: center;"><strong>Monthly
Benefit</strong></td>
<td style="text-align: center;"><strong>Total monthly income after the
benefit</strong></td>
</tr>
<tr>
<td style="text-align: center;"><strong>from (€)</strong></td>
<td style="text-align: center;"><strong>to (€)</strong></td>
<td style="text-align: center;"><strong>from (€)</strong></td>
<td style="text-align: center;"><strong>to (€)</strong></td>
<td style="text-align: center;"><strong>€</strong></td>
<td style="text-align: center;"><strong>from (€)</strong></td>
<td style="text-align: center;"><strong>to (€)</strong></td>
<td style="text-align: center;"><strong>from (€)</strong></td>
<td style="text-align: center;"><strong>to (€)</strong></td>
<td style="text-align: center;"><strong>€</strong></td>
</tr>
<tr>
<td style="text-align: center;">0</td>
<td style="text-align: center;">341</td>
<td colspan="2" style="text-align: center;">369</td>
<td style="text-align: center;">710</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">700</td>
<td colspan="2" style="text-align: center;">510</td>
<td style="text-align: center;">1,210</td>
</tr>
<tr>
<td style="text-align: center;">342</td>
<td style="text-align: center;">360</td>
<td style="text-align: center;">350</td>
<td style="text-align: center;">368</td>
<td style="text-align: center;">710</td>
<td style="text-align: center;">701</td>
<td style="text-align: center;">750</td>
<td colspan="2" style="text-align: center;">510</td>
<td style="text-align: center;">1,260</td>
</tr>
<tr>
<td style="text-align: center;">361</td>
<td style="text-align: center;">400</td>
<td style="text-align: center;">310</td>
<td style="text-align: center;">350</td>
<td style="text-align: center;">710</td>
<td style="text-align: center;">751</td>
<td style="text-align: center;">800</td>
<td style="text-align: center;">476</td>
<td style="text-align: center;">510</td>
<td style="text-align: center;">1,271</td>
</tr>
<tr>
<td style="text-align: center;">401</td>
<td style="text-align: center;">450</td>
<td style="text-align: center;">271</td>
<td style="text-align: center;">310</td>
<td style="text-align: center;">710 – 721</td>
<td style="text-align: center;">801</td>
<td style="text-align: center;">850</td>
<td style="text-align: center;">421</td>
<td style="text-align: center;">476</td>
<td style="text-align: center;">1,271</td>
</tr>
<tr>
<td style="text-align: center;">451</td>
<td style="text-align: center;">500</td>
<td style="text-align: center;">244</td>
<td style="text-align: center;">271</td>
<td style="text-align: center;">721 – 744</td>
<td style="text-align: center;">851</td>
<td style="text-align: center;">900</td>
<td style="text-align: center;">371</td>
<td style="text-align: center;">421</td>
<td style="text-align: center;">1,271</td>
</tr>
<tr>
<td style="text-align: center;">501</td>
<td style="text-align: center;">550</td>
<td style="text-align: center;">216</td>
<td style="text-align: center;">244</td>
<td style="text-align: center;">744 – 766</td>
<td style="text-align: center;">901</td>
<td style="text-align: center;">1,000</td>
<td style="text-align: center;">271</td>
<td style="text-align: center;">371</td>
<td style="text-align: center;">1,271</td>
</tr>
<tr>
<td style="text-align: center;">551</td>
<td style="text-align: center;">600</td>
<td style="text-align: center;">189</td>
<td style="text-align: center;">216</td>
<td style="text-align: center;">766 – 789</td>
<td style="text-align: center;">1,001</td>
<td style="text-align: center;">1,100</td>
<td style="text-align: center;">171</td>
<td style="text-align: center;">271</td>
<td style="text-align: center;">1,271</td>
</tr>
<tr>
<td style="text-align: center;">601</td>
<td style="text-align: center;">794</td>
<td style="text-align: center;">40</td>
<td style="text-align: center;">189</td>
<td style="text-align: center;">789 - 834</td>
<td style="text-align: center;">1,101</td>
<td style="text-align: center;">1,191</td>
<td style="text-align: center;">81</td>
<td style="text-align: center;">171</td>
<td style="text-align: center;">1,271</td>
</tr>
</tbody>
</table>

*Source:* [*Welfare Benefit
Services*](https://www.wbas.dmsw.gov.cy/dmsw/ydep.nsf/All/B337EE5D4B327A13C22587D500403FE8?OpenDocument)

<span id="Table_02_12" class="anchor"></span>**Table 2.12** Monthly low
pension benefit amounts since 1/6/2023

<table style="width:77%;">
<colgroup>
<col style="width: 7%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 8%" />
<col style="width: 9%" />
<col style="width: 7%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 9%" />
</colgroup>
<thead>
<tr>
<th colspan="5" style="text-align: center;"><strong>One-pensioner
household</strong></th>
<th colspan="5" style="text-align: center;"><strong>Two-pensioner
household</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: center;"><strong>Total monthly income
before the benefit</strong></td>
<td colspan="2" style="text-align: center;"><strong>Monthly
Benefit</strong></td>
<td style="text-align: center;"><strong>Total monthly income after the
benefit</strong></td>
<td colspan="2" style="text-align: center;"><strong>Total monthly income
before the benefit</strong></td>
<td colspan="2" style="text-align: center;"><strong>Monthly
Benefit</strong></td>
<td style="text-align: center;"><strong>Total monthly income after the
benefit</strong></td>
</tr>
<tr>
<td style="text-align: center;"><strong>from (€)</strong></td>
<td style="text-align: center;"><strong>to (€)</strong></td>
<td style="text-align: center;"><strong>from (€)</strong></td>
<td style="text-align: center;"><strong>to (€)</strong></td>
<td style="text-align: center;"><strong>€</strong></td>
<td style="text-align: center;"><strong>from (€)</strong></td>
<td style="text-align: center;"><strong>to (€)</strong></td>
<td style="text-align: center;"><strong>from (€)</strong></td>
<td style="text-align: center;"><strong>to (€)</strong></td>
<td style="text-align: center;"><strong>€</strong></td>
</tr>
<tr>
<td style="text-align: center;">0</td>
<td style="text-align: center;">341</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">387</td>
<td style="text-align: center;">728</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">700</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">536</td>
<td style="text-align: center;">1,236</td>
</tr>
<tr>
<td style="text-align: center;">342</td>
<td style="text-align: center;">360</td>
<td style="text-align: center;">368</td>
<td style="text-align: center;">386</td>
<td style="text-align: center;">728</td>
<td style="text-align: center;">701</td>
<td style="text-align: center;">750</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">536</td>
<td style="text-align: center;">1,236</td>
</tr>
<tr>
<td style="text-align: center;">361</td>
<td style="text-align: center;">400</td>
<td style="text-align: center;">328</td>
<td style="text-align: center;">367</td>
<td style="text-align: center;">728</td>
<td style="text-align: center;">751</td>
<td style="text-align: center;">800</td>
<td style="text-align: center;">490</td>
<td style="text-align: center;">536</td>
<td style="text-align: center;">1,290</td>
</tr>
<tr>
<td style="text-align: center;">401</td>
<td style="text-align: center;">450</td>
<td style="text-align: center;">285</td>
<td style="text-align: center;">327</td>
<td style="text-align: center;">728 – 735</td>
<td style="text-align: center;">801</td>
<td style="text-align: center;">850</td>
<td style="text-align: center;">440</td>
<td style="text-align: center;">489</td>
<td style="text-align: center;">1,290</td>
</tr>
<tr>
<td style="text-align: center;">451</td>
<td style="text-align: center;">500</td>
<td style="text-align: center;">256</td>
<td style="text-align: center;">284</td>
<td style="text-align: center;">735 – 756</td>
<td style="text-align: center;">851</td>
<td style="text-align: center;">900</td>
<td style="text-align: center;">390</td>
<td style="text-align: center;">439</td>
<td style="text-align: center;">1,290</td>
</tr>
<tr>
<td style="text-align: center;">501</td>
<td style="text-align: center;">550</td>
<td style="text-align: center;">227</td>
<td style="text-align: center;">255</td>
<td style="text-align: center;">756 – 777</td>
<td style="text-align: center;">901</td>
<td style="text-align: center;">1,000</td>
<td style="text-align: center;">290</td>
<td style="text-align: center;">389</td>
<td style="text-align: center;">1,290</td>
</tr>
<tr>
<td style="text-align: center;">551</td>
<td style="text-align: center;">600</td>
<td style="text-align: center;">198</td>
<td style="text-align: center;">226</td>
<td style="text-align: center;">777 – 798</td>
<td style="text-align: center;">1,001</td>
<td style="text-align: center;">1,100</td>
<td style="text-align: center;">190</td>
<td style="text-align: center;">289</td>
<td style="text-align: center;">1,290</td>
</tr>
<tr>
<td style="text-align: center;">601</td>
<td style="text-align: center;">794</td>
<td style="text-align: center;">86</td>
<td style="text-align: center;">197</td>
<td style="text-align: center;">798 - 880</td>
<td style="text-align: center;">1,101</td>
<td style="text-align: center;">1,191</td>
<td style="text-align: center;">99</td>
<td style="text-align: center;">189</td>
<td style="text-align: center;">1,290</td>
</tr>
</tbody>
</table>

*Source:* [*Welfare Benefit
Services*](https://www.wbas.dmsw.gov.cy/dmsw/ydep.nsf/All/B337EE5D4B327A13C22587D500403FE8?OpenDocument)

***EUROMOD modelling:** The resident status of migrants is not
considered in the simulation.*

### Easter Benefit/Πασχαλινό Επίδομα (bsals_cy)

#### Definitions

Besides the Low Pension Benefit, there is also the Easter benefit, which
is given to pensioners with low incomes just before Easter, following a
decision by the Council of Ministers. Like the Low Pension Benefit, it
was first introduced in 2010.

#### Eligibility conditions

Eligible persons are those who already receive the Low Pension Benefit
or are entitled to it under the GMI law.

#### Income test

Recipients of the Low Pension Benefit qualify if their family income
from the previous year is below €7,000 for single-person households and
€12,000 for two-person households, provided all household members are
pensioners. As with the Low Pension Benefit, these thresholds are
adjusted according to the number of additional household members.
Specifically, they are multiplied by a scaling factor of 1, plus 0.5 for
each dependent under 14 and 0.3 for each family member over 14. The
definitions of family income and the family unit remain the same as
those used for the Low Pension Benefit.

#### Benefit amount

The annual benefit amount is decided on an ad hoc basis following a
relevant decision by the Council of Ministers. The one-off benefit for
2022-2023 was €190 per pensioner. For 2024 and 2025, the benefit was set
at €250 per pensioner.

## Social insurance contributions

Participation in the Social Insurance Scheme is compulsory for the
entire working population up to age 65.[^14] Those covered are
classified as employees or self-employed individuals. Voluntary
insurance is also available to those who wish to extend coverage after
completing a period of mandatory insurance. Social insurance
contributions are calculated as a percentage of insurable earnings,
defined as earnings subject to contributions. These include any
remuneration from employment and payments to the Central Holiday Fund.
The insured person, the employer, and the state each contribute a share
of the total contribution.

### Employee social insurance contributions (tscee_cy)

The level of the basic insurable earnings is calculated each year, based
on the amounts of earnings reported to the Social Insurance Services by
employers in that year:

€9,682 in annual terms (or €186.20 weekly) for 2021,

€10,008 in annual terms (or €192.47 weekly) for 2022,

€10,482 in annual terms (or €201.57 weekly) for 2023.

€11,104 in annual terms (or €213.54 weekly) for 2024.

These amounts are then used in the following year to establish
eligibility and the basic and earnings-related components of several
social insurance benefits. Accordingly:

€9,682 is the annual amount used for 2022,

€10,008 is the annual amount for 2023. However, following an amendment
to the law in July 2022, the amount used for 2023 was adjusted to
€10,089 to compensate for an increase in the price index,

€10,482 is the annual amount used for 2024,

€11,104 is the annual amount used for 2025.

#### Liability to contributions

Contributions to the Social Insurance Fund (SIF) are mandatory for all
employers, employees, and self-employed individuals across both the
private and public sectors.[^15]

Moreover, employees in the broader public sector are also covered by the
Government Employees Pension Scheme (GEPS).[^16] Between 1 October 2011
and 31 December 2022, coverage applied only to those permanently
employed before 1 October 2011. Changes enacted on 1 January 2023 extend
coverage to all permanently employed employees in the broader public
sector, although different provisions apply to those who became
permanent from 1 October 2011 onwards.

#### Income base used to calculate contributions

The insurable earnings of the employee include any amount paid to the
employee for their labour, i.e., basic salary, cost of living allowance,
overtime, commissions, 13th salary, 53rd/56th week, the employer's
contribution to the Central Holiday Fund, and holiday unions’ funds.
Only ex gratia payments are not included. Also, the Law sets a maximum
amount of earnings for contribution purposes, which is revised annually:

€4,840 per month or €1,117 per week for 2022,

€5,005 per month or €1,155 per week for 2023,

€5,239 per month or €1,209 per week for 2024,

€5,551 per month or €1,281 per week for 2025.

If an employee’s earnings exceed the maximum amount, no contributions
are paid on the excess.

#### Contribution rates

The Social Insurance Scheme is financed by contributions from employees,
employers, and the State (through the Consolidated Fund of the Republic,
“Πάγιο Ταμείο της Δημοκρατίας”). As of 1 January 2024, the total
contribution rate is 22.8% of insurable earnings, comprising 8.8% from
the employer, 8.8% from the employee, and 5.2% from the State. Employees
additionally covered by an occupational scheme also contribute 22.8% of
their insurable earnings, with 13.15% paid by the employer, 4.45% by the
employee, and 5.2% by the State. Notably, since 2009, contribution rates
have gradually increased to ensure the long-term fiscal sustainability
of the social insurance scheme. The contribution rates are summarised in
the following tables:

<span id="Table_02_13" class="anchor"></span>**Table 2.13** Social
Insurance Contribution standard rates

|  | After 1 April 2009 | After 1 January 2014 | After 1 January 2019 | After 1 January 2024 | After 1 January 2029 |
|:---|:---|:---|:---|:---|:---|
| Employee | 6.80% | 7.80% | 8.30% | 8.80% | 9.30% |
| Employer | 6.80% | 7.80% | 8.30% | 8.80% | 9.30% |
| Government | <u>4.30%</u> | <u>4.60%</u> | <u>4.90%</u> | <u>5.20%</u> | <u>5.50%</u> |
| **Total** | **17.90%** | **20.20%** | **21.50%** | **22.80%** | **24.10%** |

Source: [Law
59(I)/2010](https://www.cylaw.org/nomoi/enop/non-ind/2010_1_59/full.html)

<span id="Table_02_14" class="anchor"></span>**Table 2.14** Social
Insurance Contribution special rates, applicable when employees are
covered by a supplementary occupational scheme

|  | After 1 April 2009 | After 1 January 2014 | After 1 January 2019 | After 1 January 2024 | After 1 January 2029 |
|:---|:---|:---|:---|:---|:---|
| Employee | 3.45% | 3.95% | 4.20% | 4.45% | 4.70% |
| Employer | 10.15% | 11.65% | 12.40% | 13.15% | 13.90% |
| Government | <u>4.30%</u> | <u>4.60%</u> | <u>4.90%</u> | <u>5.20%</u> | <u>5.50%</u> |
| **Total** | **17.90%** | **20.20%** | **21.50%** | **22.80%** | **24.10%** |

Source: [Law
59(I)/2010](https://www.cylaw.org/nomoi/enop/non-ind/2010_1_59/full.html)

Voluntary Insurance is also available to those wishing to supplement
their contributions to meet the requirements for the state pension (or
increase the amount of the pension they will receive), as well as to
those working abroad for Cypriot employers. For voluntarily insured
individuals working in Cyprus, the contribution rate is currently 20%,
with 15.2% paid by the insured person and 4.8% by the state. For those
working abroad for Cypriot employers, the current rate is 23.1%,
comprising 17.8% paid by the insured person and 5.3% by the government.
The insured person chooses the amount of insured earnings on which
social insurance contributions are based, but this amount cannot exceed
the weekly total of their past insured earnings. Tables 2-15 and Table
2-16 summarise the voluntary contribution rates in recent years.

<span id="Table_02_15" class="anchor"></span>**Table 2.15** Social
Insurance Voluntary Contribution rates, applicable to persons residing
in Cyprus

|  | After 1 April 2009 | After 1 January 2014 | After 1 January 2019 | After 1 January 2024 | After 1 January 2029 |
|:---|:---|:---|:---|:---|:---|
| Employee | 11.00% | 13.00% | 14.00% | 15.20% | 16.40% |
| Government | <u>3.80%</u> | <u>4.10%</u> | <u>4.40%</u> | <u>4.80%</u> | <u>5.20%</u> |
| **Total** | **14.80%** | **17.10%** | **18.40%** | **20.00%** | **21.60%** |

Source: [Law
59(I)/2010](https://www.cylaw.org/nomoi/enop/non-ind/2010_1_59/full.html)

<span id="_Toc222326630" class="anchor"></span>**Table 2.16** Social
Insurance Voluntary Contribution rates, applicable to persons working
abroad for Cypriot employers

<table style="width:61%;">
<colgroup>
<col style="width: 12%" />
<col style="width: 9%" />
<col style="width: 9%" />
<col style="width: 9%" />
<col style="width: 10%" />
<col style="width: 9%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;"></th>
<th style="text-align: left;">After 1 April 2009</th>
<th style="text-align: left;">After 1 January 2014</th>
<th style="text-align: left;">After 1 January 2019</th>
<th style="text-align: left;">After 1 January 2024</th>
<th style="text-align: left;">After 1 January 2029</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">Employee</td>
<td style="text-align: left;">13.60%</td>
<td style="text-align: left;">15.60%</td>
<td style="text-align: left;">16.60%</td>
<td style="text-align: left;">17.80%</td>
<td style="text-align: left;">19,00%</td>
</tr>
<tr>
<td style="text-align: left;">Government</td>
<td style="text-align: left;"><u>4.30%</u></td>
<td style="text-align: left;"><u>4.60%</u></td>
<td style="text-align: left;"><u>4.90%</u></td>
<td style="text-align: left;"><u>5.30%</u></td>
<td style="text-align: left;"><u>5.70%</u></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Total</strong></td>
<td style="text-align: left;"><strong>17.90%</strong></td>
<td style="text-align: left;"><strong>20.20%</strong></td>
<td style="text-align: left;"><strong>21.50%</strong></td>
<td style="text-align: left;"><strong>23.10%</strong></td>
<td style="text-align: left;"><strong>24.70%</strong></td>
</tr>
<tr>
<td colspan="6" style="text-align: left;"></td>
</tr>
</tbody>
</table>

Source: [Law
59(I)/2010](https://www.cylaw.org/nomoi/enop/non-ind/2010_1_59/full.html)

***EUROMOD modelling:** Due to data limitations, it is not possible to
determine whether an employee is covered by their employer's pension
scheme (or whether such a scheme is available to them). As a result, the
reduced contribution of 4.2% applies only to civil servants. No
voluntary contributions are modelled, also because of data limitations.*

### Employer social insurance contributions (tscer_cy)

#### Liability to contributions

Employers are required to pay contributions to the funds (Social
Insurance, Annual Holidays with Pay, Redundancy, Human Resource
Development, and Social Cohesion) for each of their employees who earn
at least €2 per week if paid weekly or €7 per month if paid monthly.
[^17]

The employer's liability for paying contributions ends on the day
employees reach pensionable age. An employer is not required to pay
contributions to the Central Holiday Fund if they obtain an exemption
from the Minister of Labour and Social Insurance. Exemptions are granted
in cases where the employer provides annual holidays to their employees
on terms more favourable than those specified in the Annual Holidays
with Pay legislation.

#### Income base used to calculate contributions

Insurable earnings are subject to an annual cap that is reviewed
annually. Contributions to the Social Cohesion Fund are calculated on
total earnings with no upper limits. Earnings include basic salary,
cost-of-living allowance, commissions, 13th and 14th salaries, 53rd/56th
week, overtime, and other benefits. The gross amount of earnings (i.e.,
before deducting taxes and contributions) is taken into consideration.
The employer's contribution to the Central Holiday Fund is included in
insurable earnings. Earnings payable to the employee for periods
exceeding one week or one month, such as the 13th salary, earnings of
the 54th week, commissions, etc., are taken into consideration up to the
amount that, when added to the employee's earnings for the period in
question, does not exceed the maximum amount for that period.

#### Contribution rates

Contributions payable by employers to the Funds mentioned above are
calculated as a percentage of the employee's earnings, as explained
below. Contributions under (a), (b), (c) and (d) are computed on
insurable earnings up to the maximum amount specified above. In
contrast, contributions under (e) are calculated based on actual
earnings, with no upper limit. The rates under (c), (d), and (e) apply
to trainees with low earnings and are applied to their actual earnings.

**(a) Social Insurance Fund**

As shown in Table 2-13, as of 1 January 2024, the employee contribution
rate was 22.8%, comprising 8.8% paid by the employee, 8.8% by the
employer, and 5.2% from the Consolidated Fund of the Republic. As shown
further in Table 2-14, if an employer establishes an occupational
pension scheme, the employer contributes 13.15% and the employee 4.45%.

**(b) Central Holiday Fund**

The contribution rate to the Central Holiday Fund varies based on the
length of annual leave that the employee is entitled to, as illustrated
in the following table:

<span id="_Toc222326631" class="anchor"></span>**Table 2.17** Rate of
contribution to the Central Holiday Fund for employees with a
5-day/6-day working week

<table style="width:65%;">
<colgroup>
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 16%" />
</colgroup>
<thead>
<tr>
<th colspan="4" style="text-align: left;"><strong>Rate of contribution
to the Central Holiday Fund for employees with a 5-day working
week</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">Duration of annual leave (days)</td>
<td style="text-align: left;">Rate of contribution (%)</td>
<td style="text-align: left;">Duration of annual leave (days)</td>
<td style="text-align: left;">Rate of contribution (%)</td>
</tr>
<tr>
<td style="text-align: left;">20</td>
<td style="text-align: left;">8.0</td>
<td style="text-align: left;">31</td>
<td style="text-align: left;">12.5</td>
</tr>
<tr>
<td style="text-align: left;">21</td>
<td style="text-align: left;">8.5</td>
<td style="text-align: left;">32-33</td>
<td style="text-align: left;">13.0</td>
</tr>
<tr>
<td style="text-align: left;">22-23</td>
<td style="text-align: left;">9.0</td>
<td style="text-align: left;">34</td>
<td style="text-align: left;">13.5</td>
</tr>
<tr>
<td style="text-align: left;">24</td>
<td style="text-align: left;">9.5</td>
<td style="text-align: left;">35</td>
<td style="text-align: left;">14.0</td>
</tr>
<tr>
<td style="text-align: left;">25</td>
<td style="text-align: left;">10.0</td>
<td style="text-align: left;">36</td>
<td style="text-align: left;">14.5</td>
</tr>
<tr>
<td style="text-align: left;">26</td>
<td style="text-align: left;">10.5</td>
<td style="text-align: left;">37-38</td>
<td style="text-align: left;">15.0</td>
</tr>
<tr>
<td style="text-align: left;">27-28</td>
<td style="text-align: left;">11.0</td>
<td style="text-align: left;">39</td>
<td style="text-align: left;">15.5</td>
</tr>
<tr>
<td style="text-align: left;">29</td>
<td style="text-align: left;">11.5</td>
<td style="text-align: left;">40</td>
<td style="text-align: left;">16.0</td>
</tr>
<tr>
<td style="text-align: left;">30</td>
<td style="text-align: left;">12.0</td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td colspan="4" style="text-align: left;"><strong>Rate of contribution
to the Central Holiday Fund for employees with a 6-day working
week</strong></td>
</tr>
<tr>
<td style="text-align: left;">Duration of annual leave (days)</td>
<td style="text-align: left;">Rate of contribution (%)</td>
<td style="text-align: left;">Duration of annual leave (days)</td>
<td style="text-align: left;">Rate of contribution (%)</td>
</tr>
<tr>
<td style="text-align: left;">24</td>
<td style="text-align: left;">8.0</td>
<td style="text-align: left;">37-38</td>
<td style="text-align: left;">12.5</td>
</tr>
<tr>
<td style="text-align: left;">25-26</td>
<td style="text-align: left;">8.5</td>
<td style="text-align: left;">39</td>
<td style="text-align: left;">13.0</td>
</tr>
<tr>
<td style="text-align: left;">27</td>
<td style="text-align: left;">9.0</td>
<td style="text-align: left;">40-41</td>
<td style="text-align: left;">13.5</td>
</tr>
<tr>
<td style="text-align: left;">28-29</td>
<td style="text-align: left;">9.5</td>
<td style="text-align: left;">42</td>
<td style="text-align: left;">14.0</td>
</tr>
<tr>
<td style="text-align: left;">30</td>
<td style="text-align: left;">10.0</td>
<td style="text-align: left;">43-44</td>
<td style="text-align: left;">14.5</td>
</tr>
<tr>
<td style="text-align: left;">31-32</td>
<td style="text-align: left;">10.5</td>
<td style="text-align: left;">45</td>
<td style="text-align: left;">15.0</td>
</tr>
<tr>
<td style="text-align: left;">33</td>
<td style="text-align: left;">11.0</td>
<td style="text-align: left;">46-47</td>
<td style="text-align: left;">15.5</td>
</tr>
<tr>
<td style="text-align: left;">34-35</td>
<td style="text-align: left;">11.5</td>
<td style="text-align: left;">48</td>
<td style="text-align: left;">16.0</td>
</tr>
<tr>
<td style="text-align: left;">36</td>
<td style="text-align: left;">12.0</td>
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td colspan="4" style="text-align: left;"></td>
</tr>
</tbody>
</table>

Source: [Social Security
Services](https://www.gov.cy/app/uploads/2024/03/%CE%9F%CE%B4%CE%B7%CE%B3%CF%8C%CF%82-%CE%B3%CE%B9%CE%B1-%CF%84%CE%B7-%CE%9D%CE%BF%CE%BC%CE%BF%CE%B8%CE%B5%CF%83%CE%AF%CE%B1-%CE%95%CF%84%CE%AE%CF%83%CE%B9%CF%89%CE%BD-%CE%91%CE%B4%CE%B5%CE%B9%CF%8E%CE%BD.pdf)

The contribution rate for leave longer than 40 days in a 5-day working
week and 48 days in a 6-day working week is increased accordingly.

The contribution to the Central Holiday Fund is paid in full by the
employer.

**(c) Redundancy Fund**

The contribution to the Redundancy Fund (at a rate of 1.2%) is wholly
payable by the employer.

**(d) Human Resource Development Fund**

The contribution to the Human Resource Development Fund (at a rate of
0.5%) is payable in full by the employer.

**(e) Social Cohesion Fund**

The Social Cohesion Fund was introduced on 1 January 2003. The
contribution to the Fund (at a rate of 2%) is payable entirely by the
employer.

***EUROMOD modelling:** Central Holiday Fund - The same contribution
rate (8%) was applied across all employers. The data do not indicate
whether an employer-sponsored pension plan covers an employee.
Therefore, the reduced contribution of 12.4% applies only to civil
servants. Trainees cannot be identified in the dataset; therefore, the
special rules that apply to them are not simulated.*

#### Random assignment

Eligibility to pay contributions to the Central Holiday Fund is randomly
simulated among non-civil servants based on the ratios presented in the
table below. Note that the 2023 value is also used for 2024 and 2025, as
no information is currently available for the latter.

<span id="_Toc222326632" class="anchor"></span>**Table 2.18** Number of
Employees covered by the Central Holiday Fund

| Year | Number of Employees covered by the Central Holiday Fund | Employees in the private and semi-public sectors | Ratio |
|:---|---:|---:|---:|
| 2012 | 98,845 | 356,704 | 0.277 |
| 2013 | n.a. | n.a. | \- |
| 2014 | 80,187 | 332,266 | 0.241 |
| 2015 | 76,829 | 338,799 | 0.227 |
| 2016 | 74,462 | 356,786 | 0.209 |
| 2017 | 80,556 | 385,805 | 0.209 |
| 2018 | 88,437 | 413,625 | 0.214 |
| 2019 | 94,816 | 431,307 | 0.224 |
| 2020 | 99,248 | 408,292 | 0.244 |
| 2021 | 95,863 | 429,389 | 0.223 |
| 2022 | 97,935 | 468,325 | 0.210 |
| 2023 | 101,174 | 492,886 | 0.206 |
| 2024 | \- | \- | 0.206 |
| 2025 | \- | \- | 0.206 |

Source: [Social Insurance Services, Ministry of Labour and Social
Insurance](https://www.mlsi.gov.cy/mlsi/sid/sidv2.nsf/page21_gr/page21_gr?OpenDocument)

### Self-employed social contributions (tscse_cy)

#### Liability to contributions

Self-employed individuals are liable for social insurance contributions.
Their minimum insurable earnings are determined by their profession and
workplace.

#### Income base used to calculate contributions

For each professional category, an annual minimum amount of insurable
earnings is set. Self-employed individuals may pay contributions on
earnings above this minimum, but there is also an annual upper limit
that applies equally across all professional categories. If a
self-employed person's actual income falls below the minimum income for
their professional category, they may request to pay contributions based
on their actual income.

#### Contribution rates

As of January 2014, the total contribution of self-employed persons was
19.2% of their insured earnings. Of this percentage, 14.6% was paid by
the self-employed and 4.6% by the government. By January 2019, the total
contribution for the self-employed increased to 20.5% of their insured
earnings; the self-employed paid 15.6%, while the government paid the
remaining 4.9%. As of 1 January 2024, the total contribution rose
further to 21.8%; the self-employed paid 16.6%, and the government
contributed the remaining 5.2%.

An insured individual has the right to pay contributions towards
retirement until the age of 65. However, if the insured individual does
not qualify for the statutory pension by that age due to specific
requirements, they may continue to pay contributions until those
requirements are met. This period cannot extend beyond the age of 68.

The contribution rate for the self-employed is set to change as follows:

23.7% as of January 2029, with 18% paid by the self-employed and 5.7%
from the Republic's Consolidated Fund.

25.4% as of January 2034, with 19.4% paid by the self-employed and 6%
from the Republic's Consolidated Fund.

26.7% as of January 2039, with 20.4% paid by the self-employed and 6.3%
from the Consolidated Fund of the Republic.

The maximum contribution base for self-employed individuals is uniform
across all professional categories, such as doctors, managers, teachers,
and farmers. The following limits are applied:

€1,117 per week in 2022,

€1,155 per week in 2023,

€1,209 per week in 2024,

€1,281 per week in 2025.

### Government social insurance contributions (tscgv_cy)

The State also contributes to the Social Insurance Scheme. As previously
mentioned in Sections
[2.7.1](#employee-social-insurance-contributions-tscee_cy) (see [**Table
2.13**](#Table_02_13) and [**Table 2.14**](#Table_02_14) ) and
[2.7.3](#self-employed-social-contributions-tscse_cy), the government
contribution rate for employed and self-employed persons was 4.9% from 1
January 2019 to 31 December 2023. Since 1 January 2024, this rate has
increased to 5.2%. Central Holiday Fund contributions are included in
the earnings used to calculate the government contributions.

### Contributions to the General Healthcare System/Γενικό Σύστημα Υγείας (tsc\*\*\_cy)

The General Healthcare System (GHS) is a comprehensive, financially
sustainable healthcare system that aims to meet the expectations of
Cypriot citizens for equal access to treatment and high-quality
healthcare by utilising all available resources as effectively as
possible. To implement the GHS, a special fund was established to
collect relevant contributions, from which all payments to healthcare
service providers will be made. The GHS fund will be administered by the
Health Insurance Organisation (Οργανισμός Ασφάλισης Υγείας - ΟΑΥ). The
Health Insurance Organisation was established in Cyprus pursuant to the
General Healthcare System Law (N. 89 (I)/2001). Participation in the GHS
is mandatory for all residents of Cyprus with income in Cyprus.

Under the provisions of the General Healthcare System (Amending) Law of
2017, the GHS was implemented in two stages.

The first stage, which began on 1 June 2019, provided only outpatient
healthcare, i.e., services delivered by personal doctors, outpatient
specialists, pharmacists, and laboratories.

The second and final stage of GHS implementation, which began on 1 June
2020, includes all remaining healthcare services, i.e., services offered
by allied health professionals (clinical dieticians, occupational
therapists, speech pathologists, physiotherapists, and clinical
psychologists), nurses and midwives, accident and emergency departments,
ambulance services, dentists, palliative healthcare services, and
medical rehabilitation services.

Contributions to the first implementation stage of the GHS began on 1
March 2019. Full implementation was initially scheduled for 1 March 2020
but was postponed to 1 June 2020 due to COVID-19-related events.

The beneficiaries of the GHS are as follows:

Every citizen of the Republic

EU citizens who work or have the right of permanent residence

Third-country nationals who have acquired a legal right of permanent
residence or the right to equal treatment

Refugees and people with subsidiary protection status

#### Liability to contributions

The primary source of financing for the GHS is contributions. These are
paid by those with income. Those who do not contribute, such as the
unemployed, are also beneficiaries.

The Contributors’ Categories are (see table below for more information):

Employees

Employers

Self-employed

Pensioners (excl. pensioners who only receive the social pension)

Income-earners (incomes from rent, assets, investments)

Civil servants

In addition to these groups, the state is paying additional
contributions for specific categories.

#### Income base used to calculate contributions

Gross incomes.

#### Contribution rates

The contribution rates for each contributor category, as set by the
General Healthcare System (Amending) Law of 2017, are shown in Table
2-19.

<span id="_Toc222326633" class="anchor"></span>**Table 2.19**
Contribution rates to the General Healthcare System

<table style="width:65%;">
<colgroup>
<col style="width: 17%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr>
<th><p><strong>Contributor</strong></p>
<p><strong>Categories</strong></p></th>
<th><p><strong>First Phase</strong></p>
<p><strong>(1/3/2019-31/5/2020)</strong></p></th>
<th><p><strong>Full Implementation</strong></p>
<p><strong>(since 1/7/2020)</strong></p></th>
<th><strong>Explanation</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Employee</td>
<td>1.70%</td>
<td>2.65%</td>
<td>Earnings</td>
</tr>
<tr>
<td>Employer</td>
<td>1.85%</td>
<td>2.90%</td>
<td>Earnings of employees</td>
</tr>
<tr>
<td>State</td>
<td>1.65%</td>
<td>4.70%</td>
<td>On earnings, self-employment income, and pensions</td>
</tr>
<tr>
<td>Self-employed</td>
<td>2.55%</td>
<td>4.00%</td>
<td>Self-employment income</td>
</tr>
<tr>
<td>Pensioners</td>
<td>1.70%</td>
<td>2.65%</td>
<td>Pensions</td>
</tr>
<tr>
<td>Income earners</td>
<td>1.70%</td>
<td>2.65%</td>
<td>Incomes from various sources</td>
</tr>
<tr>
<td>Government Officials</td>
<td>1.70%</td>
<td>2.65%</td>
<td>On their remuneration</td>
</tr>
<tr>
<td>Employer of Government Officials</td>
<td>1.85%</td>
<td>2.90%</td>
<td>On the remuneration of the Government Official</td>
</tr>
</tbody>
</table>

Source: [General Health
System](https://www.gesy.org.cy/sites/Sites?d=Desktop&locale=en_US&lookuphost=/en-us/&lookuppage=hiofinancing)

**<u>Example</u>:** An employee with a gross salary of €1,000 will
contribute €17.00 to GHS (€1,000 x 1.7%); their employer will contribute
€18.50 (€1,000 x 1.85%).

For every natural person, if the total annual amount received exceeds
€180,000, contributions will be required only for €180,000 (using the
income-source-specific contribution rate, starting with employment
income, then self-employment income, pensions, and other sources).

If the natural person is not a tax resident of Cyprus, they will pay
contributions only on income, earnings, and pensions derived from the
Republic of Cyprus, excluding dividends and interest. 

Furthermore, every natural person has the right to deduct from their
taxable income the amount they contribute to the GHS (only the amount
they pay themselves). The maximum deductible income is set at €180,000,
which means a maximum deduction of €3,060 can be claimed.

***EUROMOD modelling:** The introduction of GHS occurred on 1 March
2019, and the GHS-related SIC rates were further increased on 1 June
2020. As a rule, EUROMOD baseline models refer to policy rules on 30
June of the respective year. An FYA (Full Year Adjustment) switch is
available to account for the fact that GHS-related SIC increases in 2019
and 2020 are effective only for parts of the year (see section 2.5). The
switch is set to on by default.*

## Direct taxes (tin_cy)

### Tax unit 

A personal income tax is levied on the income of individuals who are tax
residents in Cyprus. The taxed income may originate from sources within
or outside Cyprus. Tax residents include every citizen of the Republic
of Cyprus, as well as non-citizens who are permanently settled in the
Republic and have elected to be taxed as citizens for income tax
purposes. Individuals who are not tax residents of Cyprus are taxed only
on specific types of income earned or derived from sources within
Cyprus.

***EUROMOD modelling:** Currently, the model classifies all individuals
in the input data as tax residents.*

### Tax base

The calculation of the tax base (or taxable income) begins with
determining the Gross Total Income. This includes individuals' worldwide
income, subject to certain exemptions. Several deductions are then
applied to the Total Income to arrive at the Net Total Income. This
amount is further reduced by deducting various tax allowances, resulting
in the tax base.

The employer's contributions to the Annual Holiday Fund are part of the
Gross Total Income.

#### Tax exemptions

The entire amount of the following types of income is excluded from the
calculation of Gross Total Income (as detailed in Law 201(I)/2022
art.8):

1.  Interest, except for interest derived from an individual's usual
    business activities or closely related activities. The amount may be
    liable for the Special Contribution for Defence.

<!-- -->

8.  Dividends. The amount might be subject to the Special Contribution
    for Defence.

9.  Profits arising from a foreign permanent establishment under
    specific conditions. [^18]

10. A lump sum received as retirement gratuity, pension commutation, or
    compensation for death or injury.

11. Lump sums received by individuals from payments made to approved
    funds (e.g., provident funds).

12. Profits earned from the sale of securities.[^19]

13. Remuneration for salaried services performed outside Cyprus for more
    than 90 days in a tax year, either for a non-Cyprus resident
    employer or for a foreign permanent establishment of a Cyprus
    resident employer.

Furthermore, the following types of income are only partially excluded:

1.  Profits from the production of films, series, and other related
    audiovisual programmes. The exempt amount is the lower of 35% of
    eligible expenditure or 50% of taxable income. Any unused exemption
    may be carried forward for up to five (5) years.

<!-- -->

14. Remuneration for first employment in Cyprus. The duration of this
    exemption, the percentage of remuneration exempted, and the maximum
    amount exempted depend on when the employment in Cyprus began, the
    number of years before that date during which the individual was not
    a Cyprus resident, and the amount of remuneration.

***EUROMOD modelling:** The Gross Total Income is calculated as the sum
of employment income, self-employment income, pensions, and rental
income for all individuals in the input data.*

#### Tax deductions

The deductions listed below are applied to the Gross Total Income to
calculate the Net Total Income:

1.  Contributions to trade unions or professional bodies (full amount),

2.  Losses incurred in the current and several previous years (total
    amount),

3.  Donations to approved charities (full amount),

4.  Expenses related to maintaining a building under an active
    Preservation Order (up to €1,200, €1,100 or €700 per sq. m.,
    depending on the building’s size).

5.  One-fifth of the expenditure on infrastructure and technological
    equipment in the audiovisual industry

6.  Revenue expenditure for scientific research and R&D – subject to
    conditions (whole amount plus an additional 20% for expenditure
    incurred in 2022, 2023, and 2024).

7.  Tax amortisation on capital expenditure for scientific research and
    R&D – subject to conditions (whole amount, plus an additional 20%
    for expenditures incurred in 2022, 2023, and 2024 – allocated over
    the asset’s lifetime, up to a maximum of 20 years), and

8.  One fifth of gross rental income.

Additionally, for investments made from 1 January 2017 in approved
innovative small and medium-sized enterprises, either directly or
indirectly, part of the invested amount (20%, 35%, or 50%, based on
investment characteristics) may be deducted, up to 50% of total income
for the investment year, calculated before this deduction. The deduction
is capped at €150,000 per tax year.

***EUROMOD modelling:** Due to data limitations, only the rental income
deduction (5) is included in the model.*

#### Tax allowances

The following amounts are deducted from the Net Total Income to
determine the tax base amount. The total amount of allowances deducted
is limited to one-fifth of the Total Net Income.

1.  Social Insurance Contributions (SIC),

2.  Contributions to the General Healthcare System (GHS/ΓεΣΥ),

3.  Contributions to private medical funds, up to a maximum equal to 2%
    of remuneration,

4.  Contributions to pension and provident funds, up to a maximum equal
    to 10% of remuneration, and

5.  Life Insurance premiums, up to a maximum equal to 7% of the insured
    amount.

***EUROMOD modelling:*** Due to limited data availability, life
insurance premiums are excluded from the calculations. Furthermore,
contributions to private medical funds, pensions, and provident funds
are modelled only in part, as remuneration data is unavailable.

### Tax schedule

The amount of personal income tax is calculated by applying a
progressive tax rate schedule to the tax base. The income brackets and
their corresponding tax rates have remained unchanged from 2022 to 2025.

<span id="_Toc222326634" class="anchor"></span>**Table 2.20** Tax rates
and income brackets for 2022-2025 (in EUR)

| **Income Bracket** | **Tax Rate** |
|:------------------:|:------------:|
|     0 – 19,500     |      0%      |
|  19,501 – 28,000   |     20%      |
|  28,001 – 36,300   |     25%      |
|  36,301 – 60,000   |     30%      |
|      60,001 +      |     35%      |

Source: [Tax Department, Ministry of
Finance](https://www.mof.gov.cy/mof/tax/taxdep.nsf/index_en/index_en?opendocument)

### Tax credits 

Tax credits are available in cases of double taxation (see Footnote 18).

***EUROMOD modelling:*** Tax credits are not considered.

## Other taxes

### Special Contribution for Defence/Έκτακτη Εισφορά για την Άμυνα (txc_cy)

The Special Contribution for Defence, as detailed in Law 198(I)/2022, is
imposed on income earned by individuals and legal entities based in
Cyprus. Non-tax residents are generally exempt. It is charged at the
following rates:

1.  On dividend income (from Cyprus and non-Cyprus tax-resident
    companies): 17%

<!-- -->

15. On interest income arising from the ordinary activities or closely
    related to the ordinary activities of the business: 0% (NB: This
    type of income is instead liable to personal income tax).

16. On other interest income (“passive”), received or credited: A
    standard rate of 30% in 2022 and 2023, and 17% in 2024 and
    2025[^20], except for the following cases:

    1)  Other interest income received by or credited to individuals
        with an annual income (including interest) not exceeding
        €12,000: 3% (reduced rate)

    2)  Interest from corporate bonds (as of 26 June 2019), Cyprus
        government savings and development bonds, local or national
        administration bonds, or debt securities traded on recognised
        stock exchanges (as of 8 June 2022): 3% (reduced rate)

    3)  Interest earned on a provident fund: 3% (reduced rate)

17. On gross rents (reduced by 25%): 3%

Money paid as a Special Contribution to Defence is subject to tax.

***EUROMOD modelling:** Only individual contributions are modelled, as
contributions by legal entities are outside the model's scope.
Furthermore, contributions under points 1 and 3.b are not simulated;
therefore, the Special Contribution for Defence is only partially
simulated.*

### Contribution of broader public sector employees to the Government Employees' Pension Scheme/Εισφορές στο Επαγγελματικό Σχέδιο Συνταξιοδοτικών Ωφελημάτων των υπαλλήλων της κρατικής υπηρεσίας και του ευρύτερου δημόσιου τομέα (tpipb_cy)

Before 1 October 2011, all permanent employees in the broader public
sector, which includes the central government, semi-governmental
organisations, government agencies, and local administration
organisations, were covered by the Government Employees’ Pension Scheme.
This scheme provided them with a supplementary pension upon retirement,
in addition to the pension earned through participation in the Social
Insurance pension scheme. A key feature was that those covered were not
required to contribute. Furthermore, as this was a supplementary
employer-provided scheme, special rates applied to the calculation of
their and their employer’s social insurance contributions (see Table
2-21). For employees, the special rate is lower than the corresponding
standard rate, whereas for employers, it is higher (NB: These rates are
reported in [**Table 2.13**](#Table_02_13) and [**Table
2.14**](#Table_02_14) ).

As of 1 October 2011 (Law 216(I)/2012), participation in this scheme has
been limited to those who were permanently employed in the broader
public sector before that date. These individuals are now required to
pay 3% of their gross employment income to the government for their
participation, unless they have made more than 400 monthly social
insurance contributions. Their social insurance contributions, along
with those of their employers, remain unchanged (i.e. at the special
rate). Despite the introduction of the obligation to contribute to the
scheme, the level of pension benefits they receive does not depend on
these payments. Therefore, these payments are not officially considered
contributions but rather a form of taxation that applies only to this
group of employees. For those who would become permanently employed from
1 October 2011 onwards, the law did not give them the option to
participate in the scheme. Instead, it required them to pay social
insurance contributions at the standard rate, as their employers would
(see [**Table 2.21**](#Table_02_21)).

As of 1 January 2023 (Law 210(I)/2022), a new Government Employees'
Pension Scheme was established for those permanently employed from that
date onwards, providing the same pension benefits as the original
scheme. Participants must contribute 5% of their insurable earnings,
with their employer matching this amount. Additionally, their social
insurance contributions and their employer's contributions are
calculated at the special rate, as this is a supplementary
employer-provided pension scheme (see [**Table 2.21**](#Table_02_21)).

Individuals who were permanently employed between the establishment of
the two government pension schemes, i.e., from 1 October 2011 to 31
December 2022, are also eligible to participate in this scheme. To
receive the same benefits as others covered, those who choose to do so
must make retrospective payments to cover the period without
contributions from 1 October 2011 to 31 December 2022. The total amount
payable is based on the difference between the social insurance
contributions they actually paid during their period of permanent
employment until 31 December 2022, and the combined amount of social
insurance contributions and contributions to the new pension scheme they
would have paid if the scheme had been active and they had participated
during the same period. This amount can be paid either as a lump sum or
in 36 equal monthly instalments from 1 January 2025 to 31 December 2027.

<span id="Table_02_21" class="anchor"></span>**Table 2.21** Contribution
rates to government pension schemes by the broader public sector
employees and their employers

<table style="width:62%;">
<colgroup>
<col style="width: 10%" />
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
<th rowspan="2"><strong>Group of broader public sector
employees</strong></th>
<th rowspan="2" style="text-align: center;"><strong>Pension
Fund</strong></th>
<th colspan="2" style="text-align: center;"><strong>Before
1/10/2011</strong></th>
<th colspan="2" style="text-align: center;"><strong>From 1/10/2011 to
31/12/2022</strong></th>
<th colspan="2" style="text-align: center;"><strong>From
1/1/2023</strong></th>
</tr>
<tr>
<th style="text-align: center;"><strong>Employee</strong></th>
<th style="text-align: center;"><strong>Employer</strong></th>
<th style="text-align: center;"><strong>Employee</strong></th>
<th style="text-align: center;"><strong>Employer</strong></th>
<th style="text-align: center;"><strong>Employee</strong></th>
<th style="text-align: center;"><strong>Employer</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="2">Permanently employed before 1/10/2011</td>
<td style="text-align: center;">Original gov't scheme</td>
<td style="text-align: center;">no provision</td>
<td style="text-align: center;">no provision</td>
<td style="text-align: center;">3%</td>
<td style="text-align: center;">no provision</td>
<td style="text-align: center;">3%</td>
<td style="text-align: center;">no provision</td>
</tr>
<tr>
<td style="text-align: center;">Social Insurance</td>
<td style="text-align: center;">special rate</td>
<td style="text-align: center;">special rate</td>
<td style="text-align: center;">special rate</td>
<td style="text-align: center;">special rate</td>
<td style="text-align: center;">special rate</td>
<td style="text-align: center;">special rate</td>
</tr>
<tr>
<td rowspan="2">Permanently employed between 1/10/2011 and
31/12/2022</td>
<td style="text-align: center;">New gov't scheme</td>
<td style="text-align: center;">n/a</td>
<td style="text-align: center;">n/a</td>
<td style="text-align: center;">n/a</td>
<td style="text-align: center;">n/a</td>
<td style="text-align: center;">5%</td>
<td style="text-align: center;">5%</td>
</tr>
<tr>
<td style="text-align: center;">Social Insurance</td>
<td style="text-align: center;">n/a</td>
<td style="text-align: center;">n/a</td>
<td style="text-align: center;">standard rate</td>
<td style="text-align: center;">standard rate</td>
<td style="text-align: center;">special rate</td>
<td style="text-align: center;">special rate</td>
</tr>
<tr>
<td rowspan="2">Permanently employed from 1/1/2023</td>
<td style="text-align: center;">New gov't scheme</td>
<td style="text-align: center;">n/a</td>
<td style="text-align: center;">n/a</td>
<td style="text-align: center;">n/a</td>
<td style="text-align: center;">n/a</td>
<td style="text-align: center;">5%</td>
<td style="text-align: center;">5%</td>
</tr>
<tr>
<td style="text-align: center;">Social Insurance</td>
<td style="text-align: center;">n/a</td>
<td style="text-align: center;">n/a</td>
<td style="text-align: center;">n/a</td>
<td style="text-align: center;">n/a</td>
<td style="text-align: center;">special rate</td>
<td style="text-align: center;">special rate</td>
</tr>
</tbody>
</table>

**Notes: NB:** The special SIC rates apply when an employer provides a
supplementary pension scheme. For employees, the special rate is lower
than the corresponding standard rate, whereas the opposite is true for
their employers. These rates are reported in [Table
2‑13](#_Ref218340323) (standard rates) and [Table 2‑14](#_Ref218340333)
(special rates).

Source: [Law
210(I)/2022](https://www.cylaw.org/nomoi/arith/2022_1_210.pdf)

***EUROMOD modelling:** The distinction between public sector employees
who started before or after 1 October 2011 is captured by the variable
lcs10; see the Data section for more information. The exemption for
those who contributed for more than 400 months is simulated using the
person's employment history.*

### Contributions of public employees to the Widows and Orphans Government Fund/Εισφορές στο Ταμείο Χηρών και Ορφανών (tscee_cy)

All broad public sector employees contribute to the Widows and Orphans
Government Fund. Before 1 October 2011, the contribution rate was 0.75%
of the gross salary. If the gross salary exceeded the maximum insurable
earnings, a rate of 1.75% applied to the excess. A brief example
demonstrates how the contribution is calculated: Let the gross wage be
€6,000; then the contribution is:

C = 0.75% \* 5,005 (this is the maximum amount of insurable earnings in
2023) + 1.75% \* (6,000-5,005).

As of 1 October 2011, the rules were simplified. The contribution rose
to 2% of gross wages, with no minimum or maximum limits. Furthermore, if
the employee has made more than 400 monthly social insurance
contributions, they are exempt from the contribution.

***Note on EUROMOD Implementation:** This instrument is implemented
within the policy tscee_cy and included in the variable tscee_s
(employees’ social insurance contributions). The exemption for those who
contributed for more than 400 months is simulated by using the person's
employment history.*

### Scaled reduction in emoluments of public and broader public sector pensioners and employees/Μείωση Απολαβών και Συντάξεων του Ευρύτερου Δημόσιου Τομέα (paycut_cy)

Since 1 December 2012, the government has implemented a scaled reduction
in the emoluments of public sector employees and pensioners. The
reduction is applied to gross salaries and pensions. The term "gross"
refers to income before all taxes and contributions. On 30 April 2013,
the House of Representatives voted to modify the law, changing the
reduction rates. After 1 June 2013, the scaled reduction appearing in
the third column of the following table replaced the one voted in 2012.
As of 1 January 2014, emoluments in the public sector, including
pensions, decreased by an additional 3 per cent; the total reduction is
shown in the fourth column. From July 2018, the scaled reduction began
to decrease, and by 1 January 2023, it was abolished.

<span id="_Toc222326636" class="anchor"></span>**Table 2.22** Scaled
reductions

<table style="width:65%;">
<colgroup>
<col style="width: 7%" />
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
<th style="text-align: left;">Monthly Income brackets</th>
<th style="text-align: left;"><p>12/2012</p>
<p>-</p>
<p>05/2013</p></th>
<th style="text-align: left;"><p>06/2013</p>
<p>-</p>
<p>12/2013</p></th>
<th style="text-align: left;"><p>01/2014</p>
<p>-</p>
<p>06/2018</p></th>
<th style="text-align: left;"><p>07/2018</p>
<p>-</p>
<p>12/2018</p></th>
<th style="text-align: left;"><p>01/2019</p>
<p>-</p>
<p>12/2019</p></th>
<th style="text-align: left;"><p>01/2020</p>
<p>-</p>
<p>12/2020</p></th>
<th style="text-align: left;"><p>01/2021</p>
<p>-</p>
<p>12/2021</p></th>
<th style="text-align: left;"><p>01/2022</p>
<p>-</p>
<p>12/2022</p></th>
</tr>
</thead>
<tbody>
<tr>
<td>0-1,000</td>
<td>0%</td>
<td>0.8%</td>
<td>3.8%</td>
<td>1.8%</td>
<td>0%</td>
<td>0%</td>
<td>0%</td>
<td>0%</td>
</tr>
<tr>
<td>1,001-1,500</td>
<td>6.5%</td>
<td>7.3%</td>
<td>10.3%</td>
<td>8.3%</td>
<td>5.8%</td>
<td>3.3%</td>
<td>0.8%</td>
<td>0%</td>
</tr>
<tr>
<td>1,501-2,000</td>
<td>8.5%</td>
<td>9.3%</td>
<td>12.3%</td>
<td>10.3%</td>
<td>7.8%</td>
<td>5.3%</td>
<td>2.8%</td>
<td>0%</td>
</tr>
<tr>
<td>2,001- 3,000</td>
<td>9.5%</td>
<td>10.5%</td>
<td>13.5%</td>
<td>13.5%</td>
<td>13.5%</td>
<td>11%</td>
<td>8.5%</td>
<td>5%</td>
</tr>
<tr>
<td>3,001-4,000</td>
<td>11.5%</td>
<td>13%</td>
<td>16%</td>
<td>16%</td>
<td>16%</td>
<td>13.5%</td>
<td>11%</td>
<td>7.5%</td>
</tr>
<tr>
<td>4,001-above</td>
<td>12.5%</td>
<td>14.5%</td>
<td>17.5%</td>
<td>17.5%</td>
<td>17.5%</td>
<td>15%</td>
<td>12.5%</td>
<td>9%</td>
</tr>
</tbody>
</table>

Source: [Law
168(I)/2012](https://www.cylaw.org/nomoi/enop/non-ind/2012_1_168/full.html)

***Note on EUROMOD Implementation:*** *This instrument is implemented
within the policy paycut_cy.*

## Consumption taxes

Consumption taxes simulated in EUROMOD can be divided into two groups:
VAT (value-added tax) and excises (additional duties paid over
consumption, typically on energy, alcoholic beverages, and tobacco).

Simulated consumption tax liabilities paid by households depend on the
tax rules (e.g., the VAT rate) and the tax base (consumption
expenditures or quantities). This is why, to simulate consumption taxes
in EUROMOD, the input data must contain information on household
expenditures. The expenditures matched in the EUROMOD input files based
on SILC are reported directly by households in the HBS surveys at
purchasing prices. Therefore, they already include the consumption taxes
paid.

**VAT** (*il_tva* variable in EUROMOD) is the value-added tax. The model
also simulates, at a high disaggregation level, the VAT liabilities paid
for each consumption category (output variables are tva01111, tva01112,
and so on, corresponding to COICOP codes 01111 and 01112, etc.).

**Excises** (*il_tx* variable in EUROMOD) are additional duties paid
over consumption. These can be classified into two groups: ad-valorem
excises (il_txv) that depend on producer prices, and specific or
ad-quantum excises (il_txa) that depend on consumed quantities.

Since consumption data from HBS refers to expenditures (price times
quantity), information on consumption prices is also needed to simulate
specific excises.

Note that the structure of these consumption taxes is common across
countries, and this is why they are placed in an add-on and not in the
policy spine of each country. Further information on methodology and
specific calculations can be found in Akoğuz et al. (2020).

### VAT (il_tva)

Value Added Tax (VAT) in Cyprus is defined and implemented as described
in Law 95(I)/2000, as well as subsequent legislation that amends it. VAT
is imposed on the supply of all goods and services in Cyprus, on the
acquisition of goods from other Member States and on the importation of
goods from third countries.

<span id="_Toc222326637" class="anchor"></span>**Table 2.23** VAT rates
\[2022-2025\]

<table style="width:65%;">
<colgroup>
<col style="width: 15%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th>Type</th>
<th style="text-align: right;">2022</th>
<th style="text-align: right;">2023</th>
<th style="text-align: right;">2024</th>
<th style="text-align: right;">2025</th>
</tr>
</thead>
<tbody>
<tr>
<td>Standard</td>
<td style="text-align: right;">19%</td>
<td style="text-align: right;">19%</td>
<td style="text-align: right;">19%</td>
<td style="text-align: right;">19%</td>
</tr>
<tr>
<td>Reduced-1</td>
<td style="text-align: right;">9%</td>
<td style="text-align: right;">9%</td>
<td style="text-align: right;">9%</td>
<td style="text-align: right;">9%</td>
</tr>
<tr>
<td>Reduced-2</td>
<td style="text-align: right;">5%</td>
<td style="text-align: right;">5%</td>
<td style="text-align: right;">5%</td>
<td style="text-align: right;">5%</td>
</tr>
<tr>
<td>Reduced-3</td>
<td style="text-align: right;">-</td>
<td style="text-align: right;">-</td>
<td style="text-align: right;">3%</td>
<td style="text-align: right;">3%</td>
</tr>
<tr>
<td>Zero</td>
<td style="text-align: right;">0%</td>
<td style="text-align: right;">0%</td>
<td style="text-align: right;">0%</td>
<td style="text-align: right;">0%</td>
</tr>
<tr>
<td>Exempted</td>
<td style="text-align: right;">-</td>
<td style="text-align: right;">-</td>
<td style="text-align: right;">-</td>
<td style="text-align: right;">-</td>
</tr>
<tr>
<td colspan="5"></td>
</tr>
</tbody>
</table>

Source: [Tax Department, Ministry of
Finance](https://www.mof.gov.cy/mof/tax/taxdep.nsf/index/index?opendocument)

Standard rate:

The standard rate applies to the supply of all goods and services in
Cyprus that are not subject to the zero rate, reduced rates, or any
exemptions.

The reduced rate of 9% applies to:

All restaurant and catering services, including the supply of alcoholic
drinks, beer, wine and soft drinks.

Accommodation in hotels, tourist lodgings, and any other similar
lodgings, including the provision of holiday lodgings.

Transportation of passengers and their accompanying luggage within the
Republic by urban, intercity and rural taxis and tourist and intercity
buses.

Movement of passengers in inland waters and their accompanying luggage.

Provision of services and supply of goods by nursing homes, which are
not exempt transactions.

The reduced rate of 5% applies to:

The supply of foodstuffs.

The supply of prepared or unprepared foodstuffs and/or beverages
(excluding alcoholic drinks, beer, wine and soft drinks), whether the
goods are delivered from the supplier to the customer or taken away by
the customer.

The supply of pharmaceutical products and vaccines used for healthcare,
the prevention of illnesses, and the treatment of medical or veterinary
conditions.

The supply of live animals for the preparation of food.

Entry fees to circuses, festivals, theme parks, museums, etc.

Entry fees at sports events and fees for using sports centres.

Hairdressing services.

Renovation and repair of private households after three years of first
occupancy.

Supply of catering services from school canteens.

Acquisition or construction of residence (subject to conditions).

The reduced rate of 3% was introduced on 21 July 2023 and applies to the
following supplies:

Books, newspapers, and periodicals (including those in electronic
formats).

Audiobooks for disabled persons.

Special lifting appliances, wheelchair-type buggies and other vehicles
for disabled persons.

Certain orthopaedic items and appliances; splints, supports, and other
fracture-related items and devices; certain prosthetic items; and
specific devices to facilitate hearing, other medical devices, or
implants.

Street cleaning, refuse collection, and waste treatment services, other
than the supply of such services by public authorities, local
authorities, and bodies governed by public law.

Disposal and treatment of wastewater and evacuation of septic and
industrial tanks.

Admission to theatrical, musical, or dance performances, or classical
works.

The zero rate applies to:

The exportation of goods.

Supply, modification, repair, maintenance, chartering and hiring of
sea-going vessels used for navigation on the high seas and for carrying
passengers for reward or for commercial, industrial, or other
activities.

Supply, modification, repair, maintenance, chartering, and hiring of
aircraft used by airlines operating for reward, mainly on international
routes.

Supply of services to meet the direct needs of seagoing vessels and
aircraft.

Transportation of passengers from the Republic to a place outside the
Republic and vice versa by sea or by air.

Supplies of gold to the Central Bank of the Republic.

International passenger transport to the extent it takes place within
the territory of Cyprus.

Braille typewriters and special electronic typewriters for disabled
persons.

Wheelchairs and other vehicles intended solely for personal use by
disabled persons.

Exempt supplies include:

Rental of immovable property for residential purposes

Financial services (with certain exceptions).

Hospital and medical care services.

Postal services.

Insurance services.

Disposal of immovable property where the application for building
permission was submitted before 1 May 2004.

Educational services at all levels of education, under certain
conditions.

### Ad-valorem excises (il_txv)

Ad-valorem excises cover only cigarettes.

<span id="_Toc222326638" class="anchor"></span>**Table 2.24** Ad-valorem
excise rates \[2022-2025\]

| Products   | 2022 | 2023 | 2024 | 2025 |
|------------|-----:|-----:|-----:|-----:|
| Cigarettes |  34% |  34% |  34% |  34% |

Source: [Tax Department, Ministry of
Finance](https://www.mof.gov.cy/mof/tax/taxdep.nsf/index/index?opendocument)

### Specific excises (il_txa)

Specific excises apply to energy products, tobacco, and various
alcoholic beverages. In this case, we collect both tax parameters and
consumer prices to allow the model to estimate the implicit quantities
behind the reported household consumption expenditure amounts.

<span id="_Toc222326639" class="anchor"></span>**Table 2.25** Specific
(ad-quantum) excise rates

| Products | 2022 | 2023 | 2024 | 2025 |
|----|---:|---:|---:|---:|
| Ethyl alcohol (Euro per 100 l of pure alcohol) | 956.82 | 956.82 | 956.82 | 956.82 |
| Wine (Euro per 100 l) | 0 | 0 | 0 | 0 |
| Sparkling wine (Euro per 100 l) | 0 | 0 | 0 | 0 |
| Beer (Euro per 100 L per Alcohol of finished product) | 6 | 6 | 6 | 6 |
| Cigarettes (Euro per 1000 pieces) | 55 | 55 | 55 | 55 |
| Cigars (Euro per kg) | 90 | 90 | 90 | 90 |
| Other tobacco (Euro per 1000 pieces) | 150 | 150 | 150 | 150 |
| Electricity (Euro per MWh) | 5 | 5 | 0 | 5 |
| Natural Gas (Euro per gigajoule) | 2.6 | 2.6 | 2.6 | 2.6 |
| Liquefied hydrocarbons (Euro per 1000 kg) | 0 | 0 | 0 | 0 |
| Gas Oil (Euro per 1000L) | 21 | 21 | 74.73 | 74.73 |
| Coal and Coke (Euro per gigajoule, 1 GJ = 0.0316 ton) | 0.31 | 0.31 | 0.31 | 0.31 |
| Petrol-Leaded (Euro per 1000L) | 421 | 421 | 421 | 421 |
| Petrol-Unleaded (Euro per 1000L) | 429 | 359 | 429 | 429 |
| Gas Oil (Euro per 1000L) | 330 | 330 | 400 | 400 |

Source: [Tax Department, Ministry of
Finance](https://www.mof.gov.cy/mof/tax/taxdep.nsf/index/index?opendocument)

<span id="_Toc222326640" class="anchor"></span>**Table 2.26** Prices of
excise products

| Products                                     |    2022 |    2023 |    2024 |    2025 |
|----------------------------------------------|--------:|--------:|--------:|--------:|
| Ethyl alcohol (Euro per 1 unit of spirits)   |   19.47 |   20.41 |   22.08 |   21.91 |
| Wine (Euro per 1 l)                          |    8.97 |    9.58 |   11.84 |   11.81 |
| Sparkling wine (Euro per 1 l)                |   25.34 |   27.08 |   32.32 |   32.24 |
| Beer (Euro per 1 l of lager)                 |    2.67 |    2.81 |    2.69 |    2.64 |
| Cigarettes (Euro per 1000 units)             |  218.00 |  218.00 |  221.50 |  227.14 |
| Cigars (Euro per 1000 units)                 |  396.76 |  411.59 |  423.94 |  439.94 |
| Other tobacco (Euro per kg)                  |  230.91 |  235.27 |  228.70 |  239.33 |
| Electricity (Euro per MWh)                   |  294.40 |  363.50 |  330.50 |  315.24 |
| Natural Gas- Heating (Euro per gigajoule)    |   26.55 |   25.40 |   26.85 |   29.45 |
| Liquefied hydrocarbons (Euro per 1000 kg)    | 1811.46 | 1775.14 | 1766.00 | 1897.23 |
| Gas Oil- Heating (Euro per 1000 l)           | 1283.45 | 1103.51 | 1068.86 | 1043.04 |
| Coal and Coke - Heating (Euro per gigajoule) |   23.16 |   25.62 |   25.15 |   24.72 |
| Petrol-Unleaded (Euro per 1000 l)            | 1536.81 | 1447.85 | 1439.76 | 1409.86 |
| Gas Oil- Propellant (Euro per 1000 l)        | 1743.02 | 1546.84 | 1506.15 | 1503.72 |

Source: [Tax Department, Ministry of
Finance](https://www.mof.gov.cy/mof/tax/taxdep.nsf/index/index?opendocument)

Consumer prices of goods subject to excise duties are nowcasted, as the
model does for updating incomes from SILC. We combine the latest
available data from the following sources:

Prices per product: Usually from last year, but, for instance, fuel
prices have only a 15-day delay.

Inflation: Harmonised Index of Consumer Prices (HICP, Eurostat) at
COICOP 5 digits, usually for the first quarter in the beta release and
up to the third quarter in the final release.

Inflation quarter-on-quarter forecasts (DG ECFIN, confidential) by HICP
main groups (Unprocessed Food, Processed Food including alcohol and
tobacco, Non-Energy industrial goods, Energy, Services - overall index
excluding goods) for quarters 2, 3 and 4, as needed for each release.

For more details on the specific source of the price of each good, see
Akoğuz et al. (2020).

***EUROMOD modelling:** Consumption taxes (tco_cc policy) require
extended EUROMOD input data (with imputed income shares of consumption
expenditures at the household level) and an add-on to run. The policy is
set to off in the baseline. To activate it, the CT_XBASE add-on must be
run, and the extended EM input files (see Section 3 for more information
on the methodology and features behind these extended input files)
should be selected (as defined in the database configuration of each
country). The other add-ons (CT\_\*) are designed for reform simulations
and assume different behavioural responses: i) constant quantities
(CT_XCQ), ii) constant income shares (CT_XCIS), and iii) constant
expenditure shares (CT_XCES). These reform-scenario add-ons require that
the auxiliary output files be generated by running the first baseline
simulation (as either the quantities or expenditures and savings from
the baseline are kept constant and entered as inputs in the simulated
reform scenarios).*

# Data

## General description

The Cyprus EUROMOD 2022-2025 simulations are based on the recently
introduced EUROMOD SILC database (EMSD), prepared by Eurostat. The EMSD
includes:

all EU-SILC UDB (User Database) variables

national SILC data supplied by the National Statistical Institute (NSI)

EUROMOD variables created and imputed by Eurostat because of restricted
data access or knowledge in-house.

Based on the EMSD, the national team derives additional variables
requiring a deep understanding of country-specificities (for instance,
national tax-benefit rules). Therefore, the final EUROMOD input dataset
comprises variables from Eurostat and those created by the national
team.

Some of the EUROMOD variables produced by Eurostat are created and/or
imputed using PDB (Production Database) variables. This is because the
modalities of the PDB variables are more detailed than those of the UDB.
According to the NSI-Eurostat agreement, the national team could use the
more detailed information from the PDB to derive EUROMOD variables or to
impute values for other EUROMOD variables.

At the same time, the same disclosure rules as in the UDB are applied to
the final EUROMOD input dataset. However, disclosure rules are not
applied when imputing variables, so the values may still differ from
those a user would obtain when replicating the imputation using the UDB
dataset.

In this section, we provide details of the production of the EUROMOD
input data based on EMSD 2024, i.e., the EMSD derived from EU-SILC 2024
and used for the simulation of 2023-2025 policies. In Annex 3, we also
provide details of the production of the input data based on EMSD 2023,
i.e., the EMSD derived from EU-SILC 2023 and used for the simulation of
2022 policies.

[**Table 3.1**](#Table_03_01) reports information on the data collection
period, the income reference period, the sample size, and the response
rate for the EMSD 2024:

<span id="Table_03_01" class="anchor"></span>**Table 3.1** EUROMOD
database description

<table style="width:49%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 28%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">EUROMOD database</th>
<th style="text-align: left;">CY_2024_b1</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">Original name</td>
<td style="text-align: left;">CY_EMSD2_2024</td>
</tr>
<tr>
<td style="text-align: left;">Provider</td>
<td style="text-align: left;">Eurostat</td>
</tr>
<tr>
<td style="text-align: left;">Year of collection</td>
<td style="text-align: left;">2024</td>
</tr>
<tr>
<td style="text-align: left;">Income reference period</td>
<td style="text-align: left;">2023</td>
</tr>
<tr>
<td style="text-align: left;">Sample size</td>
<td style="text-align: left;">10,717 IND, 4,301 HH</td>
</tr>
<tr>
<td colspan="2" style="text-align: left;">Source: Eurostat Metadata for
EMSD 2024.</td>
</tr>
</tbody>
</table>

## Data adjustments 

Data adjustments were kept to a minimum. All monetary values in the EMSD
database are expressed in annual terms, whereas in the EUROMOD database,
they were converted to monthly terms.

## Imputations and assumptions

[**Table 3.2**](#Table_03_02) shows the variables that were imputed
using other EMSD variables. Below, we provide details of the imputation
process for each case.

The soldier’s allowance (bml) is considered as employee cash or
near-cash income. This type of income is recorded in the EMSD by the
variable py010g. Accordingly, we set bml equal to py010g/12 if the
individual (a) has never worked as an employee, (b) has spent a positive
number of months in compulsory military service during the Income
Reference Period, and (c) declares employee (cash or near-cash) income.
If the individual has served a positive number of months in compulsory
military service and has also worked as an employee, then bml is set
equal to the basic monthly soldier’s allowance (around 162 euros in
2023) multiplied by the number of months served in the army, divided by
12.

Since the 2016 release, the benefit-related monetary variables in
EU-SILC are disaggregated into four categories based on income
eligibility conditions (means-tested or not) and whether they are
contributory or not. For example, the variable py111g records
contributory and means-tested survivor’s benefits, py112g contributory
and non-means-tested survivor’s benefits, py113g non-contributory and
means-tested survivor’s benefits, and py114g non-contributory and
non-means-tested survivor’s benefits. We use these to impute the values
of the survivor’s benefit to a widow (psuwd), the survivor’s benefit to
an orphan (psuor), and other survivor’s benefits (psuot) as follows:

psuwd is set equal to py112g/12 + py113g/12 if (a) py112g and/or py113g
are positive, and (b) the marital status (pb190) is widow(er) or the
individual is married, but no partner id (rb240) is recorded in the
data.

psuor is set equal to py112g/12 + py113g/12 if (a) py112g and/or py113g
is positive, (b) the individual is not a widow(er), and (c) is aged less
than 25.

psuot is equal to py110g/12 - psuwd - psuor if py110g is positive.[^21]

The total amount of child and family-related benefits is recorded in the
harmonised variable hy050g and disaggregated in variables hy051g,
hy052g, hy053g, and hy054g, which adhere to the exact notation rules as
described above for the disaggregated survivor’s benefits. We combine
these variables with the child benefit (bch) and the single parent
benefit (bchlp), which are set equal to the NSI-type variables included
in the EMSD, to impute the values for the birth grant (bchba), the
maternity allowance (bma), and the variable recording all other
family-related allowances (bfamh). Specifically, we impute the received
family birth grant (bchba) by multiplying the birth grant amount for the
Income Reference Period (around 600.48 euros per year in 2023)[^22] by
the number of children under 1 year old in the family. If the imputed
birth grant is lower than or equal to hy052g, we set bchba to be equal
to the imputed birth grant. If the imputed birth grant is higher than
hy052g, we set bchba equal to hy052g. The maternity allowance (bma) is
calculated as the difference between hy052g and the birth grant.
Finally, we calculate the total amount of all other family-related
allowances (bfamh) as hy050g minus bch, bchlp, bchba, and bma.

The total amount of old-age benefits is recorded in the variable py100g
and further disaggregated into the variables py101g, py102g, py103g, and
py104g. We use these variables to impute values for three
old-age-related benefits: the social pension (poasp), the taxable
old-age pension (poatx), and the non-taxable old-age pension (poant). In
particular, poasp is set equal to py104g/12 if the individual is over 64
years of age and py104g/12 is less than the maximum amount of social
pension for the year. For poatx, we start by comparing the net (py100n)
and gross (py100g) amounts of total old-age benefits, with the
difference equal to the tax paid on the sum of all taxable pensions
received. By reversing the income tax policy, we can then calculate
poatx. In the final step, poant is calculated as the residual, i.e.,
poant=py100g-poatx-poasp.

In the EMSD data, the total amount of unemployment benefits is recorded
in the variable py090g and disaggregated across the variables py091g,
py092g, py093g, and py094g. We use these to impute the values of the
unemployment benefit paid by the Social Insurance Fund (bunct) and the
unemployment benefit paid from all other sources (bunot). First, we
identify the maximum monthly amount an individual with positive py092g
can receive in unemployment benefits under current policy provisions. We
compare this maximum unemployment benefit with the monthly unemployment
benefits reported in the data (i.e., py092g), divided by the reported
number of months in unemployment, but we constrain the duration to up to
six months (unemployed individuals can receive unemployment benefits for
up to six months). If the maximum monthly unemployment benefit is lower
than the reported monthly unemployment benefit, we set bunot equal to
the difference between the two amounts (multiplied by the duration of
unemployment and divided by 12), and bunct equal to the maximum monthly
unemployment benefit amount (multiplied by the duration of unemployment
and divided by 12). If the maximum monthly unemployment benefit is equal
to or higher than the reported monthly unemployment benefit, we set
bunot equal to zero and bunct equal to the reported monthly unemployment
benefit (multiplied by the duration of unemployment and divided by 12).
We also add the amounts recorded in py093g and py094g, divided by 12, to
bunot. We then use bunct to obtain the monthly wage before unemployment
(yempv) by reversing the unemployment benefit policy.[^23]

Since 2024, EMSD has included information on whether someone works in
the public or private sector. This information is provided by the NSI
and recorded in the variable pl230_nsilc. Accordingly, the variable lcs,
which records the private/public sector status in the input data, is set
equal to pl230_nsilc rather than having its values imputed, as was done
in previous years.

Based on the available information, we also construct a variable
indicating whether a civil servant was hired in the public sector in the
previous 12 months (variable lcs10). For this imputation, we use
information on whether someone is a civil servant (lcs=1) and their
number of months of employment (liwwh). Specifically, if someone is a
civil servant with less than 12 months of work history, we assume that
they were hired in the public sector within the last 12 months. The
indicator variable for military conscripts (young men enlisted in the
army) (l01) is created based on the information provided by individuals
about their current economic status (variable pl032) and the months
spent in compulsory military service during the income reference period
(variable pl088): when pl032=9 and pl088\>0, then the individual is in
mandatory military service. Finally, variable l02 indicates whether
someone is a public-sector pensioner. Pensioners who are former civil
servants usually receive higher pension incomes than other pensioners
because they receive pensions from the SIF (Social Insurance Fund) and
pensions from the Government Employees Pension Scheme. Using this
information, we define as former civil servants those who (a) are
pensioners (les=4), and (b) their monthly statutory pension is higher
than the sum of the minimum full pension from the SIF plus the minimum
full pension from the Government Employees Pension Scheme.

<span id="Table_03_02" class="anchor"></span>**Table 3.2** List of
imputed variables

<table style="width:63%;">
<colgroup>
<col style="width: 14%" />
<col style="width: 48%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Variable name</th>
<th style="text-align: left;">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">bml</td>
<td style="text-align: left;">BENEFIT/PENSION: Soldier allowance</td>
</tr>
<tr>
<td style="text-align: left;">psuwd</td>
<td style="text-align: left;">BENEFIT/PENSION: Survivors: widow</td>
</tr>
<tr>
<td style="text-align: left;">psuor</td>
<td style="text-align: left;">BENEFIT/PENSION: Survivors: orphan</td>
</tr>
<tr>
<td style="text-align: left;">psuot</td>
<td style="text-align: left;">BENEFIT/PENSION: Survivors: other</td>
</tr>
<tr>
<td style="text-align: left;">bchba</td>
<td style="text-align: left;">BENEFIT/PENSION: Maternity: birth
grant</td>
</tr>
<tr>
<td style="text-align: left;">bma</td>
<td style="text-align: left;">BENEFIT/PENSION: Maternity allowance</td>
</tr>
<tr>
<td style="text-align: left;">bfamh</td>
<td style="text-align: left;">BENEFIT/PENSION: Family: Family-related
allowances</td>
</tr>
<tr>
<td style="text-align: left;">poasp</td>
<td style="text-align: left;">BENEFIT/PENSION: Social Pension - Old
Age</td>
</tr>
<tr>
<td style="text-align: left;">poatx</td>
<td style="text-align: left;">BENEFIT/PENSION: Taxable Old Age</td>
</tr>
<tr>
<td style="text-align: left;">poant</td>
<td style="text-align: left;">BENEFIT/PENSION: Non-taxable Old Age</td>
</tr>
<tr>
<td style="text-align: left;">bunct</td>
<td style="text-align: left;">BENEFIT/ SIC: unemployment benefit</td>
</tr>
<tr>
<td style="text-align: left;">bunot</td>
<td style="text-align: left;">BENEFIT: Other unemployment benefits</td>
</tr>
<tr>
<td style="text-align: left;">yempv</td>
<td style="text-align: left;">INCOME: monthly wage from previous
work</td>
</tr>
<tr>
<td style="text-align: left;">lcs10</td>
<td style="text-align: left;">LABOUR MARKET: Newly hired (in the last 12
months) Civil servant</td>
</tr>
<tr>
<td style="text-align: left;">l01</td>
<td style="text-align: left;">LABOUR MARKET: Military</td>
</tr>
<tr>
<td style="text-align: left;">l02</td>
<td style="text-align: left;">LABOUR MARKET: Pensioner – former civil
servant</td>
</tr>
<tr>
<td colspan="2" style="text-align: left;">Source: STATA code that
generates the input data from the EMSD.</td>
</tr>
</tbody>
</table>

## Time period

The EMSD information on demographic variables refers to the time of data
collection, while the income reference period is 2023. Accordingly, the
same reference period applies to income taxes, social insurance
contributions, and wealth taxes.

## Gross incomes

The EMSD survey contains information on gross and net monetary income.
In the few cases where gross income could not be collected, net income
was recorded and converted to gross using the tax and social insurance
contributions rules.

## Disaggregation of harmonised variables

As discussed earlier, several harmonised EMSD variables were
disaggregated into their constituent components. These are:

Survivor’s benefits are recorded in the harmonised variable py110g and
the disaggregated variables py111g, py112g, py113g and py114g. The
information in these variables is decomposed into three parts: the
survivor’s benefit to the widow, the survivor’s benefit to the orphan,
and other survivor’s benefits.

Child- and family-related variables are recorded in the harmonised
variable hy050g and in the disaggregated variables hy051g, hy052g,
hy053g and hy054g. We decompose these variables into the child benefit,
birth grant, maternity allowance, single-parent benefit, and other
family-related allowances.

Old-age benefits are included in the harmonised variable py100g and in
the disaggregated variables py101g, py102g, py103g and py104g. The total
amount is split between the taxable old-age pension, the non-taxable
old-age pension, and the social pension.

Unemployment benefits are included in the harmonised variable py090g and
in the disaggregated variables py091g, py092g, py093g and py094g. The
total amount is split into two parts: unemployment benefits from the
Social Insurance Fund and those from other sources.

## Uprating

As noted above, the income variables in the EMSD record information for
2023 (the Income Reference Period). When running tax-benefit simulations
for a subsequent policy year using this data, the income information is
uprated to reflect changes between the Income Reference Period (i.e.,
2023) and the simulation year. Uprating indices are generally based on
changes in the average value of an income component between the data
year and the policy year. Annex 1 provides detailed information on each
uprating index.

## Extended input data (with household expenditures for the simulation of consumption taxes)

To simulate consumption taxes, the model must be run using extended
EUROMOD input files. These files consist of the core EUROMOD input files
based on EU-SILC or National SILC, extended with new variables
(household-level income shares of expenditures by product) imputed from
EU/National-HBS. The semi-parametric imputation method implemented
follows the methodology developed by Akoğuz et al. (2020).

[**Table 3.3**](#Table_03_03) summarises some key characteristics of the
most recent database used to run the policy systems for 2023-2025.

<span id="Table_03_03" class="anchor"></span>**Table 3.3** Extended
EUROMOD database description

| Extended EUROMOD database for the simulation of consumption taxes | SILC 2024 – Income year 2023 – Expenditures from HBS 2015 |
|----|----|
| EUROMOD database | CY_2024_b1_2015_03_e2 |
| Year of collection (HBS) and source | HBS 2015 – EU |
| Year of collection (SILC) and source | SILC 2024 – EU |
| Coverage and sample size | Same as CY_2024_b1 |
| Share of households with negative incomes excluded from the matching procedure | 0% |

Source: Own elaboration.

These extended EUROMOD files contain all the variables from the standard
EUROMOD input files, plus the income shares for each consumption
category included in the HBS. For example, for countries with
consumption disaggregation at the 4th COICOP level (5 digits), there
will be close to 200 additional variables, each one with the income
shares of expenditure (household level) for that consumption category
(e.g. starting from the income share of rice consumption: xs_01111;
bread: xs_01112, and so on). The number of additional variables depends
on the granularity available in HBS, which varies across countries.

For Cyprus, in data CY_2024_b1_2015_03_e2, the number of variables
included (income shares of expenditures, xs_c\*) is 193, corresponding
to the harmonised consumption categories defined at the COICOP \[2003\]
level 4 (five digits).

This database extends the core EUROMOD input database. It is based on
the same sample (i.e., the same identifiers "idperson" and "idhh" for
persons and households, respectively). It also includes the same
variables, plus the income shares of expenditure (xs\_\* variables).

In [**Table 3.4**](#Table_03_04) we present the share of households'
consumption expenditures by product (and total) captured in our matched
databases (extended EM input files) with respect to the original
reported expenditures in HBS. The column that refers to the same year
(in this case, HBS 2015 with Extended EM Input 2015) directly depends on
the quality of the imputation procedure, while the comparison across
different years is influenced not only by the matching noise but also by
the changes in population characteristics and in the underlying
distribution of income. Therefore, the coverage displayed in the second
column is merely informative and should not be used to evaluate or
validate the imputation procedure.

Information on the coverage of these simulated expenditures (coming from
the imputation of HBS 2015 to more recent SILC-based data) with respect
to the expenditures reported by National Accounts is included in Section
4 of this report, together with the other macro-validation results.

Below, we summarise the main findings from the imputation validation
checks for Cyprus.

<span id="Table_03_04" class="anchor"></span>**Table 3.4** Expenditure
coverage of Extended EM Input files

| COICOP group | HBS 2015 – Extended EM Input 2015 | HBS 2015 – Extended EM Input 2022 |  |
|----|---:|---:|---:|
| 1 | 107.1% | 108.2% |  |
| 2 | 106.1% | 55.4% |  |
| 3 | 110.1% | 111.4% |  |
| 4 | 105.1% | 139.1% |  |
| 5 | 110.5% | 109.2% |  |
| 6 | 128.0% | 117.8% |  |
| 7 | 113.2% | 89.6% |  |
| 8 | 107.6% | 120.4% |  |
| 9 | 110.3% | 76.2% |  |
| 10 | 93.1% | 113.1% |  |
| 11 | 106.5% | 72.5% |  |
| 12 | 114.9% | 90.0% |  |

Source: Own elaboration.

# Validation

## Aggregate Validation 

In this section, we validate the EUROMOD output data against external
benchmarks. Specifically, we compare the number of individuals receiving
or earning a given income component, or paying a given tax or social
insurance contribution, with the values reported in official external
statistics. We also compare the corresponding annual amounts with the
relevant external statistics. In both cases, we provide possible
explanations for any observed discrepancies.

External statistics are collected from various administrative sources,
including the Ministry of Labour and Social Insurance, the Deputy
Ministry of Social Welfare, the Statistical Service of Cyprus, the
Ministry of Finance, and the Tax Department. It should be stressed from
the outset that the scope of macrovalidation is considerably reduced by
the limited supply of such data, [^24] the timeliness of official data
publications and, in some cases, differences in statistical definitions
across data sources. Furthermore, a macrovalidation exercise may also be
challenging for the following reasons:

a\) Using a sample to calculate totals requires caution. Grossing
factors (weights) are necessary to compute a population total from a
sample. The basic statistical purpose of grossing factors is to adjust
the proportions of different groups (i.e., to account for unequal
selection probabilities or non-response). By default, the grossing
factors sum to the total population, but several subgroups may be under-
or overrepresented. This could lead to differences between the simulated
and official data, regardless of the microsimulation's precision.[^25]

b\) Administrative data are collected using accounting procedures that
meet the needs of public authorities. This may mean that the underlying
statistical definitions are not suitable for the macrovalidation of a
given microsimulation model. For example, in Cyprus, statistics on
annual public spending on various benefits refer to the total value of
payments made for each benefit in a particular year. However, many of
these payments relate to entitlements from previous years. For example,
a family is entitled to a birth grant in 2022, but the amount is
credited to the family’s bank account in 2023.

Based on the above, the comparison between EUROMOD totals and
administrative data is meaningful only in terms of order of magnitude.
Where large differences exist, this suggests that the simulation of the
corresponding quantities may not be perfect, and that some adjustments
may be necessary (for example, the benefit in question is characterised
by considerable non-take-up, and more detailed data are needed). Bearing
these points in mind, the model provides relatively good estimates of
the simulated instruments despite several discrepancies. Our long-term
goal is to gradually improve the model, leveraging our deeper
understanding of the social protection system and incorporating new
advances in microsimulation techniques.

### Components of disposable income

**[Table 4.1](#Table_04_01)** shows the components of disposable income
in EUROMOD and EU-SILC, the latter based on EMSD2024.

<span id="Table_04_01" class="anchor"></span>**Table 4.1** Components of
disposable income

|  | **EUROMOD** | **EU-SILC** |
|:---|:--:|:--:|
|  | **ils_dispy** | **HY020** |
| Employee cash or near-cash income | \+ | \+ |
| Employer's social insurance contribution | 0 | 0 |
| Company car | 0 | \+ |
| Contributions to individual private pension plans | 0 | 0 |
| Cash benefits or losses from self-employment | \+ | \+ |
| Pension from individual private plans | 0 | 0 |
| Unemployment benefits | \+ | \+ |
| Old-age benefits | \+ | \+ |
| Survivor’s benefits | \+ | \+ |
| Sickness benefits | \+ | \+ |
| Disability benefits | \+ | \+ |
| Education-related allowances | \+ | \+ |
| Income from the rental of a property or land | \+ | \+ |
| Family/children-related allowances | \+ | \+ |
| Social exclusion not elsewhere classified | \+ | \+ |
| Housing allowances | \+ | \+ |
| Regular inter-household cash transfers received | \+ | \+ |
| Interests, dividends, etc. | \+ | \+ |
| Income received by people aged under 16 | \+ | \+ |
| Regular taxes on wealth | \- | \- |
| Regular inter-household cash transfers paid | \- | \- |
| Tax on income and social contributions | \- | \- |
| Repayments/receipts for tax adjustment | \+ | \+ |

Notes: NB: “+” indicates that the component amount is added to the
disposable income, “-” that is subtracted, and “0” means that it is not
included.

Source: EUROMOD and STATA code generating the input data based on EMSD
2024.

### Validation of market income

Tables A4.1 and A4.2 (in Annex 4) present the number of
earners/recipients and the corresponding total annual amounts for
various types of market income used in the model, along with available
external statistics. As shown in column 2 of each table, neither
quantity is simulated for any income type and is therefore derived from
the input data, which are based on EMSD 2023 for 2022 and on EMSD 2024
for 2023-2025.

Specifically, the number of income earners/recipients for 2022, reported
in column 3 (“Baseline values”) of Table A4.1, is based on the number of
earners/recipients of the given income type recorded in EMSD 2023, which
refers to 2022 (the corresponding ‘base year’). The original value is
appropriately weighted to reflect the entire population in that year.
The number of income earners/recipients for 2023-2025, reported in
columns 4-6, is based on the number of earners/recipients of the given
income type recorded in EMSD 2024, which refers to 2023 (the
corresponding ‘base year’). This number is also appropriately weighted
to reflect the entire population in that year and is also used for 2024
and 2025.

As shown in columns 11-13 (“Baseline/External ratio”), the number of
employment-income earners (i.e., employees) calculated in this way is
close to the external statistics from the Social Security Services. By
contrast, the number of recipients of self-employment income is well
above the corresponding external statistics, which likely reflects the
well-known high incidence of underreporting of self-employment status to
the Social Security Services in Cyprus.

The total annual amounts of various types of earned/received income for
2022, reported in column 3 (“Baseline values”) of Table A4.2, are based
on the corresponding quantities recorded in EMSD 2023, which refer to
2022. The corresponding amounts for 2023-2025, reported in columns 4-6,
are based on the amounts recorded in EMSD 2024, which refer to 2023. To
obtain the 2024 and 2025 amounts, the 2023 amounts from EMSD 2024 are
adjusted (i.e., uprated) to reflect changes in income over time, e.g.,
due to price inflation, income growth, etc. As a result, although based
on the same raw data, the statistics reported in columns 5 and 6 (for
2024 and 2025, respectively) differ slightly from those in column 4 (for
2023).

The comparison results in columns 11-13 show that the total annual
employee income calculated this way is very close to the external
statistics. In contrast, self-employment income exceeds the relevant
external statistics by more than three times for all years. As discussed
above, this may be due to underreporting of self-employment status to
Social Security Services. It could also be due to underreporting of
self-employment income by those who have actually reported their
self-employment status to the Social Insurance Services.

### Validation of taxes and social insurance contributions

Tables A4.3 and A4.4 present the number of payers and the corresponding
total annual amounts paid for (mainly) simulated taxes and social
insurance contributions, as reported in the EUROMOD output data and in
external statistics.

Table A4.4 shows that the total annual amounts of General Social
Insurance Contributions by employees and employers, and the employer
contribution to the Redundancy Fund, all based on employee income, are
simulated with very high accuracy. Specifically, the discrepancy between
the simulated and actual amounts for 2022-2024 is no more than 10%. In
contrast, the simulated amounts for contributions paid by the
self-employed are approximately 2.5 times higher than the corresponding
external statistics for the same years. Similarly, the simulated total
annual amounts of the Government contribution, which include the
Government's matching contributions to employees' and the
self-employed’s contributions, are approximately 2 times higher than the
corresponding external statistics.[^26] Both results can be explained by
the large underreporting of self-employment income to the Social
Insurance Services, as discussed in the previous section.

Finally, the simulated total annual employer contributions to the Annual
Holiday Fund exceed the corresponding external statistics for 2022-2024
by 31% to 41%. By contrast, the number of employees whose employers
contribute to the Annual Holiday Fund, as reported in Table A4.3, is
very close to the corresponding external statistics.

### Validation of benefits

Table A4.5 reports the number of recipients of various simulated and
non-simulated benefits in the EUROMOD output data. Table A4.6 shows the
corresponding total annual amounts.

First, focusing on the simulated benefits, we note that the number of
Child Benefit recipients for 2022-2024 is moderately overestimated by
20% to 27%. The corresponding total annual amount is slightly
overestimated for 2022 and 2023 by 5% and 7%, respectively, and somewhat
underestimated for 2024 by 4%. Compared with the values recorded in the
input data, the simulated number of recipients is lower by 9% to 14% in
2023-2025 and very close in 2022. The simulated total benefit amount is
lower than the input data amount for all four years, by 4% to 13%.

The number of recipients of the Guaranteed Minimum Income for 2022-2024
is overestimated by 29% to 69%, whereas the corresponding total annual
amounts are underestimated by 35% to 41%. By contrast, the number of
recipients of the Low Pension Benefit for 2023 is very close to the
external statistic, and is understated for 2021 and 2023 by 8% and 22%,
respectively. The corresponding total annual amounts are understated by
about 20% to 37%.

The number of recipients and the total annual amount of the Easter
Benefit are underestimated by around 30% for 2022, around 10% for 2024,
and no more than 4% for 2023.

Conversely, the number of recipients and the total annual amount of the
Single Parent Benefit are overestimated by 50% to 71% and 29% to 48%,
respectively. The simulated number of recipients also exceeds the values
recorded in the input data: by 140% in 2022 and 70% in 2023-2025.
Similarly, the simulated total benefit amount exceeds the amount derived
from the input data by around 21 times in 2023-2025 and 30 times in
2022. This deviation can be attributed to the very few recipient
observations found in the input data.

The number of recipients and the total annual amount of the Birth Grant
for 2022-2024 are overestimated by 6% to 15% and 8% to 19%,
respectively. The simulated number of recipients also exceeds the values
recorded in the input data for 2022-2025 by 17% to 24%. Similarly, the
simulated total benefit amount exceeds the amount derived from the input
data for the same years by 11% to 23%.

Finally, the simulated number of recipients of the Student Grant for
2022-2025 is 14% to 25% lower than the value recorded in the input data.
Similarly, the simulated total benefit amount exceeds the amount derived
from the input data by 21% to 30%.

Next, we turn to the non-simulated benefits. Because these figures are
not simulated, the baseline values for the number of benefit recipients
are taken from the input data for each policy year: EMSD 2023 for 2022,
and EMSD 2024 for 2023-2025. The total benefit amount for 2022 is
derived from EMSD 2023 (whose Income Reference Period is also 2022), and
similarly, for 2023, from EMSD 2024 (whose Income Reference Period is
also 2023). The total benefit amounts for 2024 and 2025 are also derived
from EMSD 2024 but are uprated to account for differences between each
of these years and 2023, so they differ slightly from the amount
reported for 2023.

The number of recipients of the Old Age Social Pension for 2022-2024 is
slightly overestimated, by 9% to 17%. The corresponding total annual
amount is also slightly above the external statistics, by no more than
8%.

The number of recipients of the Taxable Old Age Pension and Widow
Pension for the same years is relatively close to the corresponding
values of the external statistic. In the first case, these differ from
the external statistic by no more than 7% in absolute terms; in the
second, by no more than 5%. However, in both cases, the total annual
amounts are overstated by 44% to 59% for the Taxable Old Age Pension and
by 37% to 53% for the Widow Pension.

The number of recipients and the total annual amounts for the Orphan
Pension in 2022-2024 are substantially understated, by about 60% and
80%, respectively. In contrast, the number of recipients for the
Maternity Benefit is substantially overstated by 64% to 135%. At the
same time, the corresponding total annual amount is also overstated, but
to a lesser degree, between 17% and 38%.

The number of recipients of the Social Insurance Unemployment Benefit is
very close to the external statistic in 2021, and slightly overstated in
2023 and 2024, by around 18%. The corresponding total annual amount is
moderately overstated by 40% to 56% over the three years.

Finally, the number of Sickness Benefit recipients is understated by 17%
to 33% for 2022-2024. In contrast, the corresponding total annual amount
is moderately overstated by 26% to 59%.

## Income distribution 

All income distribution results, including income inequality and poverty
statistics, are based on the distribution of equivalised household
disposable income. This is the weighted sum of all household members'
incomes, net of income tax and social insurance contributions. The
weights are derived from the modified OECD equivalence scale. They are 1
for the first adult, 0.5 for each additional household member aged 14 or
above, and 0.3 for each additional household member under 14.

### Income inequality

EUROMOD estimates of income inequality, as reflected in decile shares,
the Gini index, and the S80/S20 Income Quintile Share ratio reported in
Table A4.7, are very close to the EUROSTAT estimates, with deviations of
less than 7 percentage points (p.p.).

### Poverty rates 

Table A4.8 presents several poverty rates derived from the simulated
distribution of equivalised household disposable income and calculated
under various poverty-line specifications. The 2022 simulation results
are based on EMSD 2023, whose income reference period is 2022, and the
2023 results are based on EMSD 2024, whose income reference period is
2023. Accordingly, the income and expenditure data used in the
simulations for each year refer to that year.

When the poverty line is set at either 60% or, more so, 70% of the
median of the simulated income distribution, the resulting poverty rates
for the entire population and those calculated separately for men and
women are very close to the corresponding rates reported by EUROSTAT.
The most significant deviation in 2022 is no more than eight p.p., and
in 2023, no more than four p.p.

The corresponding poverty rates obtained under the more restrictive
poverty line specifications, i.e., when the poverty line is set at 40%
or 50% of the median of the simulated income distribution, are lower
than the corresponding EUROSTAT rates, specifically by 14 to 30 p.p. for
the 40% specification and 4 to 23 p.p. for the 50% specification. This
suggests that the leftmost part of the simulated income distribution's
left tail is substantially thinner than the corresponding part of the
income distribution used by EUROSTAT for its poverty rate calculations.

With very few exceptions, poverty rates for age groups, with the poverty
line set at 60% of the median of the simulated income distribution, are
also very close to those reported by EUROSTAT. In 2022, the most
significant deviation is observed in the 50-64 age group, where the
simulated rate is 20 p.p. lower than the EUROSTAT rate. Similarly, in
2023, the most significant deviation is observed in the 0-15 age group,
where the simulated rate is 13 p.p. lower than the EUROSTAT rate.

In general, distributional discrepancies (underestimating or
overestimating incomes at specific points in the income distribution)
may arise because the current model version does not account for tax
evasion and non-take-up. Regarding tax evasion, Pashardes and Polycarpou
(2008) estimate the size of the black economy in Cyprus in the early
2000’s at around 6.7% to 8.1% of GDP, with income from self-employment
underreported by 44.8% and capital income by 40.3% (NB: the highest
underreporting rate – of 59.9% – was estimated for agricultural income).
To our knowledge, no official results on the extent of benefit
non-take-up in Cyprus are currently available.

## Consumption Taxes

Table A4.9 compares simulated (non-calibrated) expenditure and
consumption tax statistics with statistics from external sources.

The comparison of the simulated expenditures to the expenditures from
the National accounts for 2022-2025 gives mixed results, which may be
classified into three categories:

1.  Simulated expenses relatively close to the external statistics
    (i.e., with less than 20% deviation between them). These include the
    expenditure on Housing, Water and Fuel (excluding imputed rent) and
    Education, which are overestimated, and on Furniture and Household
    Equipment, Transport, Clothing and footwear and Food and
    non-alcoholic beverages, which are underestimated.

<!-- -->

18. Simulated expenses that are underestimated. These include
    expenditures on Recreation and Culture and Miscellaneous Expenses on
    Goods and Services, which are underestimated by no more than 50%.
    Also, the expenditure on Alcoholic Beverages, and Hotels and
    Restaurants, which are underestimated by more than 50%.

19. Simulated expenses that are overestimated. These include the
    expenditure on Communications, which is overestimated by no more
    than 50%, and on Health, which is overestimated by more than 50%.

The simulated revenue from the value-added tax for 2022 is
underestimated by 57%, and the simulated excise revenues are also
underestimated by 30%. These deviations are to be expected, as the
external statistics include all taxes, not only the amount households
pay.

The simulated revenue for excise taxes on various classifications of
alcoholic beverages and tobacco for 2022 is also heavily underestimated,
which reflects the earlier comments about the accuracy of the simulated
expenditure on these goods.

Table A4.10 compares the calibrated simulated consumption taxes to the
same external statistics used above, where consumption is calibrated to
match households' final consumption expenditure recorded in the National
accounts. In general, the calibrated simulated revenues from consumption
taxes better match external statistics than the non-calibrated amounts.
Notably, the revenue from the value-added tax is now underestimated for
2022 by 42% as opposed to 57%. The primary reason for under-simulated
consumption taxes is that several groups that pay significant amounts of
VAT are not covered in the HBS. Among these groups are the government
and third sector, hospitals, business enterprises, and private
households that are explicitly not covered by the HBS, such as people in
dormitories, jails, or retirement homes.

## Summary of “health warnings”

The model simulates several policy instruments within Cyprus's tax and
benefit system. It is a valuable tool that enables the user to estimate
the first-round distributional and fiscal effects of potential policy
reforms. Nevertheless, to interpret the results meaningfully, the
following caveats should be taken into account:

Issues of data comparability

Model validation requires comparing microsimulation results (e.g., the
total number of recipients and total annual spending per benefit) with
external data, typically from administrative sources. Due to limited
data availability and difficulties in systematically collecting
administrative data, the macrovalidation process is imperfect.

Partly simulated instruments

Several instruments were not fully simulated due to data limitations.
For example, the GMI benefit is only partially simulated because
information on the specific needs of recipients (which are nevertheless
covered by the GMI Law) cannot be obtained. Another example concerns the
eligibility conditions for several contributory benefits, which depend
on knowledge of the potential recipient's contributory record.
Regrettably, such information is not included in the underlying
database.

Imperfect targeting and tax evasion

The model does not account for imperfect non-take-up, income
underreporting, and tax evasion. This may cause differences between
simulated and actual values. In practice, welfare programmes are subject
to Type I and Type II errors. Type I errors arise from “false
negatives", meaning the benefit is not attributed to an eligible
recipient. By contrast, Type II errors arise from “false positives”;
that is, the benefit is attributed to non-eligible persons. Lastly, tax
evasion may introduce biases into distributional statistics.

# References

Akoğuz, Elif Cansu, Bart Capéau, André Decoster, Liebrecht De Sadeleer,
Duygu Güner, Kostas Manios, Alari Paulus, and Toon Vanheukelom (2020) A
new indirect tax tool for EUROMOD: final report. Technical Report, JRC
Project No. JRC/SVQ/2018/B.2/0021/OC
\[[LINK](https://euromod-web.jrc.ec.europa.eu/sites/default/files/2021-03/A%20new%20indirect%20tax%20tool%20for%20EUROMOD%20Final%20Report.pdf)\]

Pashardes, P. & Polycarpou, A. (2008) “Income Tax Evasion, Inequality
and Poverty”, Cyprus Economic Policy Review, Economics Research Centre,
University of Cyprus, 2(2): 37-49.
\[[LINK](https://www.ucy.ac.cy/erc2/wp-content/uploads/sites/125/2023/08/CyEPR_Vol2_No2_A2_12_2008.pdf)\]

## Sources for tax-benefit descriptions/rules

Social Insurance Services, Ministry of Labour and Social Insurance:

<https://www.mlsi.gov.cy/mlsi/sid/sidv2.nsf/index_gr/index_gr?OpenDocument>

Welfare Benefit Services, Deputy Ministry of Social Welfare

<https://www.wbas.dmsw.gov.cy/dmsw/ydep.nsf/home/home?openform>

Ministry of Finance, Grants and Benefits Services:

<https://www.gov.cy/mof/ypiresia-chorigion-kai-epidomaton/>

Legal acts in English:

<http://www.mlsi.gov.cy/mlsi/sws/sws.nsf/dmlindex_en/dmlindex_en?OpenDocument>

# List of abbreviations and definitions

| Abbreviations | Definitions |
|----|----|
| BCA | Benefit Calibration Adjustment |
| BTA | Benefit Take-up Adjustment |
| CIA | Consumption Inflation Adjustment |
| COICOP | Classification Of Individual COnsumption according to Purpose |
| CPI | Consumer Price Index |
| CR | County Report |
| CT | Consumption Taxes |
| DG | Directorate-General |
| DG ECFIN | European Commission Directorate-General for Economic and Financial Affairs |
| EM | EUROMOD |
| DG EMPL | Directorate-General for Employment, Social Affairs and Inclusion |
| EMSD | EUROMOD SILC Database |
| ESTAT | Eurostat |
| EU | European Union |
| EUR | Euro |
| FYA | Full Year Adjustments |
| GDP | Gross Domestic Product |
| GEPS | Government Employees Pension Scheme |
| GHS | General Healthcare System |
| GJ | Gigajoule |
| GMI | Guaranteed Minimum Income |
| GSIS | General Social Insurance Scheme |
| HBS | Household Budget Survey |
| HH | Households |
| HICP | Harmonised Index of Consumer Prices |
| IND | Individuals |
| ISCED | International Standard Classification of Education |
| ISER | Institute for Social and Economic Research |
| JRC | Joint Research Centre |
| LMA | Labour Market Adjustment |
| MWA | Minimum Wage Adjustment |
| NB | Nota bene |
| NRR | Net Replacement Rate |
| NSI | National Statistical Institute |
| OECD | Organisation for Economic Co-operation and Development |
| PBE | Parental Leave Benefits |
| PDB | Production Database |
| REFORM | European Commission Reform and Investment Task Force |
| SG | Secretariat-General |
| SIC | Social Insurance Contributions |
| SIF | Social Insurance Fund |
| SILC | Statistics on Income and Living Conditions |
| DG TAXUD | European Commission Directorate-General for Taxation and Customs |
| UDB | User Database |
| VAT | Value Added Tax |
| HHoT | Hypothetical Household Tool |

# List of figures

[**Figure A2.1** Policy effects in 2024-2025, using the CPI-indexation,
% [89](#_Toc222326652)](#_Toc222326652)

# List of tables

[**Table 2.1** Simulation of benefits in EUROMOD \[2022-2025\]
[15](#Table_02_01)](#Table_02_01)

[**Table 2.2** Simulation of taxes and Social Insurance contributions
(SICs) in EUROMOD \[2022-2025\] [16](#Table_02_02)](#Table_02_02)

[**Table 2.3** Main policy changes over 2022-2025
[19](#Table_02_03)](#Table_02_03)

[**Table 2.4** EUROMOD Spine: order of simulation
[20](#Table_02_04)](#Table_02_04)

[**Table 2.5** Key features of the unemployment benefit
[23](#_Toc222326619)](#_Toc222326619)

[**Table 2.6** Benefit levels for 2022-2025 (annual amounts per child,
in EUR) [27](#_Toc222326620)](#_Toc222326620)

[**Table 2.7** Benefit levels for 2022-2025 (monthly amounts per child,
in EUR) [28](#_Toc222326621)](#_Toc222326621)

[**Table 2.8** Student grant amounts for 2022-2025 (in EUR)
[30](#Table_02_08)](#Table_02_08)

[**Table 2.9** Exempted labour income (in EUR)
[35](#_Toc222326623)](#_Toc222326623)

[**Table 2.10** Housing Allowance (in EUR)
[37](#_Toc222326624)](#_Toc222326624)

[**Table 2.11** Monthly low pension benefit amounts, 1/1/2021 to
31/5/2023 [40](#Table_02_11)](#Table_02_11)

[**Table 2.12** Monthly low pension benefit amounts since 1/6/2023
[41](#Table_02_12)](#Table_02_12)

[**Table 2.13** Social Insurance Contribution standard rates
[44](#Table_02_13)](#Table_02_13)

[**Table 2.14** Social Insurance Contribution special rates, applicable
when employees are covered by a supplementary occupational scheme
[44](#Table_02_14)](#Table_02_14)

[**Table 2.15** Social Insurance Voluntary Contribution rates,
applicable to persons residing in Cyprus
[44](#Table_02_15)](#Table_02_15)

[**Table 2.16** Social Insurance Voluntary Contribution rates,
applicable to persons working abroad for Cypriot employers
[44](#_Toc222326630)](#_Toc222326630)

[**Table 2.17** Rate of contribution to the Central Holiday Fund for
employees with a 5-day/6-day working week
[46](#_Toc222326631)](#_Toc222326631)

[**Table 2.18** Number of Employees covered by the Central Holiday Fund
[47](#_Toc222326632)](#_Toc222326632)

[**Table 2.19** Contribution rates to the General Healthcare System
[50](#_Toc222326633)](#_Toc222326633)

[**Table 2.20** Tax rates and income brackets for 2022-2025 (in EUR)
[53](#_Toc222326634)](#_Toc222326634)

[**Table 2.21** Contribution rates to government pension schemes by the
broader public sector employees and their employers
[55](#Table_02_21)](#Table_02_21)

[**Table 2.22** Scaled reductions [56](#_Toc222326636)](#_Toc222326636)

[**Table 2.23** VAT rates \[2022-2025\]
[57](#_Toc222326637)](#_Toc222326637)

[**Table 2.24** Ad-valorem excise rates \[2022-2025\]
[60](#_Toc222326638)](#_Toc222326638)

[**Table 2.25** Specific (ad-quantum) excise rates
[60](#_Toc222326639)](#_Toc222326639)

[**Table 2.26** Prices of excise products
[61](#_Toc222326640)](#_Toc222326640)

[**Table 3.1** EUROMOD database description
[63](#Table_03_01)](#Table_03_01)

[**Table 3.2** List of imputed variables
[66](#Table_03_02)](#Table_03_02)

[**Table 3.3** Extended EUROMOD database description
[67](#Table_03_03)](#Table_03_03)

[**Table 3.4** Expenditure coverage of Extended EM Input files
[68](#Table_03_04)](#Table_03_04)

[**Table 4.1** Components of disposable income
[71](#Table_04_01)](#Table_04_01)

[**Table A1.1** Uprating factor values and sources, 2022-2025
[84](#_Toc222326646)](#_Toc222326646)

[**Table A2.1** Policy effects in 2024-2025, using the CPI-indexation, %
[89](#_Toc222326647)](#_Toc222326647)

[**Table A3.1** EUROMOD database description
[90](#Table_A3_01)](#Table_A3_01)

[**Table A3.2** List of imputed variables
[90](#Table_A3_02)](#Table_A3_02)

[**Table A3.3** Extended EUROMOD database description
[91](#Table_A3_03)](#Table_A3_03)

[**Table S.A.1** Validation Tables [93](#_Toc221717387)](#_Toc221717387)

# List of Annexes

## Annex 1. Uprating Factors

<span id="_Toc222326646" class="anchor"></span>**Table A1.1** Uprating
factor values and sources, 2022-2025

| Index | Reference | 2022 | 2023 | 2024 | 2025 | Source |
|----|----|---:|---:|---:|---:|----|
| Harmonised Index of Consumer Prices | \$HICP | 110.17 | 114.50 | 117.09 | 119.49 | EUROSTAT; AMECO 2025 spring forecasts for 2025 values |
| CPI (2005=100) | \$f_CPI | 127.65 | 132.18 | 134.55 | 134.66 | Republic of Cyprus, Statistical Service, Economy & Finance, Consumer Price Index \> CONSUMER PRICE INDEX – TIMESERIES (BASE 1992, 2005, 2015) \[https://www.mof.gov.cy/mof/cystat/statistics.nsf/economy_finance_14main_en/economy_finance_14main_en?OpenForm&sub=4&sel=2\] |
| Basic annual child benefit for one child | \$f_childben | 397.14 | 431.98 | 447.79 | 478.79 | Ministry of Labour, Welfare and Social Insurance |
| Average annual amount of the student grant | \$f_studgrant | 1710.00 | 1710.00 | 1710.00 | 1710.00 | Ministry of Education \[http://www.moec.gov.cy/ypiresia_foititikis_merimnas/foititiki_chorigia.html\] |
| Monthly public assistance benefit amount for the head of household | \$f_bsa | 0.00 | 0.00 | 0.00 | 0.00 | Ministry of Labour and Social Insurance, Department of Social Insurance Services, Statistical data, archived statistical data |
| Basic amount of a number of benefits | \$f_ben | 446.88 | 465.65 | 483.77 | 512.50 | Ministry of Labour and Social Insurance, Department of Social Insurance Services, Statistical data \[http://www.mlsi.gov.cy/mlsi/sid/sidv2.nsf/page21_gr/page21_gr?OpenDocument\] |
| Basic monthly amount of the orphan grant | \$f_psuor | 297.92 | 310.43 | 322.51 | 341.66 | Ministry of Labour and Social Insurance, Department of Social Insurance Services, Statistical data \[http://www.mlsi.gov.cy/mlsi/sid/sidv2.nsf/page21_gr/page21_gr?OpenDocument\] |
| Basic  amount of birth grant | \$f_bchba | 580.92 | 600.48 | 628.92 | 666.24 | Ministry of Labour and Social Insurance, Department of Social Insurance Services, Statistical data \[http://www.mlsi.gov.cy/mlsi/sid/sidv2.nsf/page21_gr/page21_gr?OpenDocument\] |
| Basic monthly amount of social pension | \$f_poasp | 361.97 | 377.18 | 391.85 | 415.12 | Ministry of Labour and Social Insurance, Department of Social Insurance Services, Statistical data \[http://www.mlsi.gov.cy/mlsi/sid/sidv2.nsf/page21_gr/page21_gr?OpenDocument\] |
| Average yearly income from employment, previous year | \$f_yempv | 12.79 | 13.68 | 14.31 | 14.96 | Lagged value of \$f_hourly_wage |
| Basic amount of military grant | \$f_bml | 157.23 | 162.32 | 162.32 | 162.32 | Ministry of Defence (Χορήγημα οπλιτών ΕΦ) |
| Employment Income, civil servants | \$f_EmplInc_Publ | 18.94 | 20.13 | 20.13 | 20.13 | Value of "Average hourly wage, Public administration and defence (lindi = 9), units of national currency" |
| Taxable public pensions | \$f_poatx_publ | 446.88 | 465.65 | 483.77 | 512.50 | Ministry of Labour and Social Insurance, Department of Social Insurance Services, Statistical data \[http://www.mlsi.gov.cy/mlsi/sid/sidv2.nsf/page21_gr/page21_gr?OpenDocument\] |
| GDP at market values | \$f_GDP | 7224.50 | 7729.00 | 8362.00 | 9046.90 | Republic of Cyprus, Statistical Service, Economy & Finance, National Accounts \[https://www.mof.gov.cy/mof/cystat/statistics.nsf/economy_finance_11main_en/economy_finance_11main_en?OpenForm&sub=1&sel=2\] |
| Average pension from SIF | \$f_avgpen | 10473.99 | 11046.36 | 11466.13 | 11901.85 | Ministry of Labour and Social Insurance, Department of Social Insurance Services, Statistical data \[http://www.mlsi.gov.cy/mlsi/sid/sidv2.nsf/page21_gr/page21_gr?OpenDocument\] |
| Monthly Guaranteed Minimum Income benefit amount for the head of the household | \$f_bsamm | 480.00 | 480.00 | 480.00 | 480.00 | Ministry of Labour and Social Insurance, Department of Social Insurance Services, Statistical data \[http://www.mlsi.gov.cy/mlsi/sid/sidv2.nsf/page21_gr/page21_gr?OpenDocument\] |
| Single-parent benefit | \$f_bchlp | 188.12 | 204.62 | 212.11 | 215.96 | Ministry of Labour, Welfare and Social Insurance |
| Maternity allowance | \$f_bma | 13.68 | 14.31 | 14.95 | 14.95 | Value of \$f_hourly_wage |
| Average yearly income from employment, lead value | \$f_yemdt | 14.31 | 14.96 | 15.50 | 15.50 | Lead value of \$f_hourly_wage |
| Average hourly wage, Agriculture and Fishing (lindi = 1), units of national currency | \$f_hourly_wage_lindi_1 | 5.93 | 6.45 | 6.46 | 6.69 | Computed from ESTAT tables nama_10_a64 (wages) and nama_10_a64_e (hours worked) up to 2019 and for 2023 onwards. The values by sector for 2020-2022 are computed by non-linear interpolation between 2019 and 2023, following the trend for all sectors. Due to the unavailability of 2025 data, values for this year are computed by multiplying the value of 2024 by the forecasted yearly increase of nominal compensation per employee, total economy, from AMECO. |
| Average hourly wage, Mining, Manufact. and Utilities (lindi = 2), units of national currency | \$f_hourly_wage_lindi_2 | 11.14 | 12.14 | 12.61 | 13.06 | Same as above. |
| Average hourly wage, Construction (lindi = 3), units of national currency | \$f_hourly_wage_lindi_3 | 9.79 | 10.74 | 11.25 | 11.65 | Same as above. |
| Average hourly wage, Wholesale and retail (lindi = 4), units of national currency | \$f_hourly_wage_lindi_4 | 9.33 | 10.13 | 10.51 | 10.89 | Same as above. |
| Average hourly wage, Hotels and restaurants (lindi = 5), units of national currency | \$f_hourly_wage_lindi_5 | 8.22 | 9.16 | 9.42 | 9.76 | Same as above. |
| Average hourly wage, Transport and communication (lindi = 6), units of national currency | \$f_hourly_wage_lindi_6 | 19.33 | 22.04 | 22.81 | 23.63 | Same as above. |
| Average hourly wage, Financial intermediation (lindi = 7), units of national currency | \$f_hourly_wage_lindi_7 | 29.87 | 33.39 | 33.24 | 34.43 | Same as above. |
| Average hourly wage, Real estate and business (lindi = 8), units of national currency | \$f_hourly_wage_lindi_8 | 12.49 | 13.62 | 14.14 | 14.64 | Same as above. |
| Average hourly wage, Public administ. and defence (lindi = 9), units of national currency | \$f_hourly_wage_lindi_9 | 20.30 | 22.89 | 24.76 | 25.65 | Same as above. |
| Average hourly wage, Education (lindi = 10), units of national currency | \$f_hourly_wage_lindi_10 | 21.73 | 23.88 | 23.42 | 24.26 | Same as above. |
| Average hourly wage, Health and social work (lindi = 11), units of national currency | \$f_hourly_wage_lindi_11 | 16.15 | 18.12 | 18.19 | 18.84 | Same as above. |
| Average hourly wage, Other (lindi = 12), units of national currency | \$f_hourly_wage_lindi_12 | 5.42 | 5.85 | 6.05 | 6.27 | Same as above. |
| Average hourly wage, All activity sectors, units of national currency | \$f_hourly_wage | 13.03 | 14.47 | 14.94 | 15.48 | Same as above. |
|  |  |  |  |  |  |  |

Notes: NB: Some of the figures for the latter two years are either
provided by the source as “preliminary” or are projected.

Source: EUROMOD, External Statistics table

## Annex 2. Policy Effects in 2024-2025

Table A2.1 and Figure A2.1 present the ceteris paribus impact of the
2025 policies on mean equivalised household disposable income, by income
component and income decile group. The impact is quantified as the
difference between simulated household disposable income under the 2025
tax-benefit policies (with all monetary parameters deflated using
Eurostat’s Harmonised Index of Consumer Prices, HICP)[^27] and simulated
household disposable income under the 2024 policies, with both policy
systems applied to the 2024 input data. This difference is then
expressed as a percentage of the 2024 mean equivalised household
disposable income (the “base amount”).

As reported in Table A2.1 (see bottom-right cell), the overall policy
impact is a positive 0.28% – relative to the base amount – between 2024
and 2025. This effect is small, reflecting minimal policy changes over
the two years.

Regardless of size, this result is primarily attributable to the
positive impact of increased public pensions, which offset the negative
impact of direct taxes (i.e., personal income tax) and, to a lesser
extent, reduced means-tested benefits. As shown in the bottom row, the
cumulative effect of these three items was 0.31%. The total impact of
the remaining income components, i.e., non-means-tested benefits and
individual types of Social Insurance Contributions, was less than 0.03%
in absolute terms.

The overall impact on disposable income by income (decile) group, shown
in the rightmost column of the same table, is also small and positive,
ranging from 0.04% (Decile 8) to 0.95% (Decile 2).

The overall impact for Decile 1 at 0.34% stands out as an outlier,
primarily due to the significant negative impact of reduced means-tested
benefits (-1.24%), which offsets the significant positive impact from
increased public pensions (1.64%).

By contrast, in Decile 2, the negative impact of reduced means-tested
benefits is smaller, at -0.22%[^28]. The overall impact, of 0.95%, is
thus driven by the positive impact of public pensions, which is 1.28%.

From that point on, the overall positive impact gradually declines until
Decile 8, reaching 0.04%. This is primarily driven by a rising negative
impact from direct taxes and a falling positive impact from public
pensions.[^29]

This trend reverses for the remaining two deciles, with the overall
impact rising to 0.14% for Decile 9 and then to 0.34% for Decile 10.
This is because the positive impact of public pensions increases,
offsetting the rising negative impact of direct taxes. This corroborates
results from previous years, which indicate that many in the latter
group receive public pensions. As a result, Decile 10 experiences the
third-highest positive impact, after Decile 2.

<span id="_Toc222326647" class="anchor"></span>**Table A2.1** Policy
effects in 2024-2025, using the CPI-indexation, %

| **Decile** | **Original income** | **Public pensions** | **Means-tested benefits** | **Non-means- tested benefits** | **Employee SIC** | **Self-employed SIC** | **Other SIC** | **Direct taxes** | **Disposable income** |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **(1)** | **(2)** | **(3)** | **(4)** | **(5)** | **(6)** | **(7)** | **(8)** | **(9)** | **(10)** |
| 1 | 0.00 | 1.64 | -1.24 | 0.00 | 0.00 | 0.00 | -0.04 | -0.01 | 0.34 |
| 2 | 0.00 | 1.28 | -0.22 | -0.01 | 0.00 | 0.00 | -0.03 | -0.07 | 0.95 |
| 3 | 0.00 | 0.73 | -0.04 | -0.02 | 0.00 | 0.00 | -0.02 | -0.10 | 0.56 |
| 4 | 0.00 | 0.58 | -0.04 | 0.00 | 0.00 | 0.00 | -0.02 | -0.16 | 0.36 |
| 5 | 0.00 | 0.51 | -0.03 | -0.01 | 0.00 | 0.00 | -0.01 | -0.19 | 0.27 |
| 6 | 0.00 | 0.48 | -0.06 | 0.00 | 0.00 | 0.00 | -0.01 | -0.27 | 0.13 |
| 7 | 0.00 | 0.44 | -0.05 | 0.00 | -0.01 | 0.00 | -0.01 | -0.32 | 0.05 |
| 8 | 0.00 | 0.53 | -0.07 | 0.00 | -0.02 | 0.00 | -0.01 | -0.38 | 0.04 |
| 9 | 0.00 | 0.62 | -0.01 | 0.02 | -0.03 | 0.00 | -0.02 | -0.43 | 0.14 |
| 10 | 0.00 | 0.88 | -0.02 | 0.05 | -0.07 | -0.01 | -0.02 | -0.45 | 0.37 |
| **Total** | 0.00 | 0.71 | -0.09 | 0.01 | -0.03 | 0.00 | -0.02 | -0.31 | 0.28 |

Notes: Policy effects are reported as percentage changes in the mean
equivalised household disposable income in 2024, by income component and
income decile group. Income decile groups are based on equivalised
household disposable income in 2024, calculated using weights from the
modified OECD equivalence scale. Each policy system has been applied to
the same input data, with monetary parameters for 2025 policies deflated
using Eurostat’s Harmonised Index of Consumer Prices (HICP).

Source: EUROMOD software calculations (Policy Effects tool) based on
EUROMOD.

<span id="_Toc222326652" class="anchor"></span>**Figure A2.1** Policy
effects in 2024-2025, using the CPI-indexation, %

<img src="media/image1.png" style="width:5.5125in;height:2.45278in" />

Source: Own elaboration, based on the figures reported in Table A2.1.

## Annex 3: Validation Tables

See [statistical annex 1](#statistical-annex-1.-validation-tables) for
details and tables.

## Annex 4. Data Based On EMSD 2023

General description

[**Table A3.1**](#Table_A3_01) reports information on the data
collection period, the income reference period, the sample size, and the
response rate for the EMSD based on EU-SILC 2023.

<span id="Table_A3_01" class="anchor"></span>**Table A3.1** EUROMOD
database description

| EUROMOD database        | CY_2023_b1           |
|:------------------------|:---------------------|
| Original name           | CY_EMSD2_2023        |
| Provider                | Eurostat             |
| Year of collection      | 2023                 |
| Income reference period | 2022                 |
| Sample size             | 10,726 IND, 4,281 HH |

Source: Eurostat Metadata for EMSD 2023

Data adjustments

Data adjustments were kept to a minimum. All monetary values in the EMSD
database are expressed in annual terms, whereas in the EUROMOD database,
they were converted to monthly terms.

Imputations and assumptions

[**Table A3.2**](#Table_A3_02) shows the variables that were imputed
using other EMSD variables, following the same imputation process as the
one described in Section [3.3](#imputations-and-assumptions) for the
case of EMSD 2023.

<span id="Table_A3_02" class="anchor"></span>**Table A3.2** List of
imputed variables

| Variable name | Description |
|:---|:---|
| Bml | BENEFIT/PENSION: Soldier allowance |
| Psuwd | BENEFIT/PENSION: Survivors: widow |
| Psuor | BENEFIT/PENSION: Survivors: orphan |
| Psuot | BENEFIT/PENSION: Survivors: other |
| Bchba | BENEFIT/PENSION: Maternity: birth grant |
| Bma | BENEFIT/PENSION: Maternity allowance |
| Bfamh | BENEFIT/PENSION: Family: Family-related allowances |
| Poasp | BENEFIT/PENSION: Social Pension - Old Age |
| Poatx | BENEFIT/PENSION: Taxable Old Age |
| Poant | BENEFIT/PENSION: Non-taxable Old Age |
| Bunct | BENEFIT/ SIC: unemployment benefit |
| Bunot | BENEFIT: Other unemployment benefits |
| Yempv | INCOME: monthly wage from previous work |
| lcs10 | LABOUR MARKET: Newly hired (in the last 12 months) Civil servant |
| l01 | LABOUR MARKET: Military |
| l02 | LABOUR MARKET: Pensioner – former civil servant |

Source: STATA code that generates the input data from the EMSD.

Time period

The EMSD information on demographic variables refers to the time of data
collection, while the income reference period is 2022. Accordingly, the
same reference period applies to income taxes, social insurance
contributions, and wealth taxes.

Gross incomes

The EMSD survey contains information on gross and net monetary income.
In the few cases where gross income could not be collected, net income
was recorded and converted to gross using the tax and social insurance
contributions rules.

Disaggregation of harmonised variables

As discussed earlier, several harmonised EMSD variables were
disaggregated into their constituent components. The information
provided in Section [3.6](#disaggregation-of-harmonised-variables) also
applies here.

Uprating

As noted above, the income variables in the EMSD record information for
2022 (the Income Reference Period). When running tax-benefit simulations
for a subsequent policy year using this data, the income information is
uprated to reflect changes between the Income Reference Period (i.e.,
2022) and the simulation year. Uprating indices are generally based on
changes in the average value of an income component between the data
year and the policy year. Annex 1 provides detailed information on each
uprating index.

Extended input data (with household expenditures for the simulation of
consumption taxes)

To simulate consumption taxes, the model must be run using extended
EUROMOD input files. These files consist of the core EUROMOD input files
based on EU-SILC or National SILC, extended with new variables
(household-level income shares of expenditures by product) imputed from
EU/National-HBS. The semi-parametric imputation method implemented
follows the methodology developed by Akoğuz et al. (2020).

[**Table A3.3**](#Table_A3_03) summarises some key characteristics of
the most recent database used to run the policy system for 2022.

<span id="Table_A3_03" class="anchor"></span>**Table A3.3** Extended
EUROMOD database description

| Extended EUROMOD database for the simulation of consumption taxes | SILC 2023 – Income year 2022 – Expenditures from HBS 2015 |
|----|----|
| EUROMOD database | CY_2023_b1_2015_03_e2 |
| Year of collection (HBS) and source | HBS 2015 – EU |
| Year of collection (SILC) and source | SILC 2023 – EU |
| Coverage and sample size | Same as CY_2023_b1 |
| Share of households with negative incomes excluded from the matching procedure | 0% |

*Source: Own elaboration.*

These extended EUROMOD files contain all the variables from the standard
EUROMOD input files, plus the income shares for each consumption
category included in the HBS. For example, for countries with
consumption disaggregation at the 4th COICOP level (5 digits), there
will be close to 200 additional variables, each one with the income
shares of expenditure (household level) for that consumption category
(e.g. starting from the income share of rice consumption: xs_01111;
bread: xs_01112, and so on). The number of additional variables depends
on the granularity available in HBS, which varies across countries.

For Cyprus, in data CY_2023_b1_2015_03_e2, the number of variables
included (income shares of expenditures, xs_c\*) is 193, corresponding
to the harmonised consumption categories defined at the COICOP \[2003\]
level 4 (five digits).

This database extends the core EUROMOD input database. It is based on
the same sample (i.e., the same identifiers "idperson" and "idhh" for
persons and households, respectively). It also includes the same
variables, plus the income shares of expenditure (xs\_\* variables).

## Statistical Annex 1. Validation Tables

<span id="_Toc221717387" class="anchor"></span>**Table S.A.1**
Validation Tables

## 

[^1]: Divorced fathers who have lost their custody rights are not
    entitled to parental leave, and thus to parental benefits.

[^2]: <sup>3</sup> The definition of a dependent child includes a child
    under 15 years old, an unmarried son between 15 and 25 who is in
    full-time education or serving in the military, an unmarried
    daughter between 15 and 23 who is in full-time education, and an
    unmarried person of any age who is permanently unable to support
    themselves.

[^3]: The paid insured earnings denote the earnings for which
    contributions have been made.

[^4]: Every insured individual is entitled to receive insured earnings
    credit for each period of full-time education after the age of 16,
    during military service, and for the duration they are receiving
    sickness benefit, unemployment benefit, maternity benefit, physical
    injury benefit, or incapacity pension from the Social Insurance
    Fund. This also encompasses periods of absence from employment due
    to parental leave or leave for exceptional circumstances (force
    majeure).

[^5]: For the first semester of each year, the previous contributions
    year is the penultimate calendar year, and for the second semester,
    it is the most recent calendar year. For example, in the first
    semester of 2023, the previous contributions year is 2022, whereas
    in the second semester of 2023, it is 2022.

[^6]: The usual definition of dependent child applies.

[^7]: Other dependants refer to cases involving a) the recipient’s
    younger brothers, and b) the recipient’s parent(s) if he/she or they
    are unable to work. In both cases, a) and b), the dependants must
    demonstrate that the recipient financially supports them.

[^8]: The Ministry of Education and Culture oversees the administration
    of this policy, which is set out in the Provision of Student Grant
    (modifying) Law of 2012 (περί Παροχής Φοιτητικής Χορηγίας
    (Τροποποιητικός) Νόμο του 2012 (N. 181(I)/2012)) and the State
    Student Care Law of 2015 (περί Κρατικής Φοιτητικής Μέριμνας Νόμος
    του 2015 (N. 203(I)/2015)).

[^9]: Note that the child benefit was excluded in the definition of
    family income according to the 2011 Law. The 2015 Law added the
    child benefit in the definition of family income.

[^10]: One *insurance point* equals 52 times the weekly basic amount
    (for 2024: €10,482).

[^11]: The basic weekly insurable earnings were €192.47 in 2024 (see
    [Table 2‑5](#_Ref207301574)).

[^12]: One insurance point equals 52 times the basic weekly insurable
    earnings, for example, €10,482 in 2024 (see [Table
    2‑5](#_Ref207301574)).

[^13]: For example, for a three-member family with two adults and one
    child below 14, the scaling factor is equal to 1.8 (=1+0.5+0.3). NB:
    The scaling coefficients used here correspond to the modified OECD
    equivalence scale.

[^14]: Insured persons who reach the pensionable age of 65 but do not
    meet the relevant insurance conditions for an old-age pension
    continue to pay contributions until those conditions are fulfilled.
    In no case are contributions paid beyond the age of 68.

[^15]: The employer is liable to pay contributions to the Social
    Insurance, Annual Holidays with Pay, Redundancy, Human Resource
    Development and Social Cohesion Funds for each of his/her employees,
    whose remuneration is not less than €2 per week, or not less than €7
    per month if he/she is a salaried employee (Social Insurance in
    Cyprus, Ministry of Labour and Social Insurance).

[^16]: See description in Section
    [2.9.2](#contribution-of-broader-public-sector-employees-to-the-government-employees-pension-schemeεισφορές-στο-επαγγελματικό-σχέδιο-συνταξιοδοτικών-ωφελημάτων-των-υπαλλήλων-της-κρατικής-υπηρεσίας-και-του-ευρύτερου-δημόσιου-τομέα-tpipb_cy).

[^17]: For trainees and apprentices, the employer must pay contributions
    to the Social Insurance Fund even if the employee has no earnings.

[^18]: Effective from 1 July 2016, taxpayers may choose to tax the
    profits earned by a foreign permanent establishment, with a tax
    credit available for foreign taxes incurred on those profits.
    Transitional rules apply in some instances.

[^19]: The term *securities* is defined as shares, bonds, debentures,
    founders’ shares, and other securities of companies or other legal
    entities incorporated in Cyprus or abroad, including options on
    these securities. Circulars issued by the Tax Authorities provide
    further clarification of what qualifies as Securities.

[^20]: The 17% rate has been in place since 1 January 2024. The earlier
    rate of 30% was introduced on 19 April 2013.

[^21]: No contributory and means-tested (py111g) survivor benefits exist
    in Cyprus.

[^22]: See the policy parameters reported in Section
    [2.6.5](#standard-birth-grantβοήθημα-τοκετού-bchba_cy).

[^23]: No means-tested unemployment benefits exist in Cyprus, either
    contributory and means-tested (py091g), or non-contributory and
    means-tested (py093g).

[^24]: In some cases, EUROMOD variables represent groups of benefits
    (e.g., housing allowances, pensions, and family-related allowances).
    Meaningful macrovalidation of these variables requires the timely
    collection of official data from various public services – an
    endeavour severely constrained by practical limitations.

[^25]: <sup>41</sup> For example, the sample may understate the number
    of people with disabilities. If so, the number of recipients of
    disability benefits will be understated, even if the microsimulation
    procedure is exact.

[^26]: NB: These calculations of government contributions do not account
    for underreporting of self-employment income to social insurance
    services that may occur in practice.

[^27]: The annual average of HCPI was retrieved from the Eurostat
    website, AMECO forecast for 2024 data.

[^28]: This follows from the fact that means-tested benefits are a much
    smaller component of the disposable income of households in Decile 2
    than in Decile 1.

[^29]: The adult members of households in these deciles are primarily
    working-age individuals whose employment income is their primary
    source of income.
