# EUROMOD Country Report — France Y16 (policy years 2022–2025): extraction for RAG & evaluation

Source: `Y16_CR_FR.pdf` (189 pages, EUROMOD master J2.19 era, EU-SILC 2024 input data). This markdown condenses everything relevant to the JRC parameter-update project: instrument definitions, EUROMOD variable names, parameter values per year, modelling caveats, validation sources and uprating factors. Parameter-level matching against `extracted_parameters/FR.policy.json` is in [FR_parameter_matching.md](FR_parameter_matching.md).

Contents (CR page references in each section heading):

1. Introduction & scope of simulation (p8–27) — system basics, instrument catalogue, policy changes 2022→2025, simulation spine, extensions
2. Family & disability benefits (p27–46) — AF, PAJE, ARS, ASF, CF, AAH
3. Social minima & activity benefits (p46–65) — AV, RSA, Prime d'activité, chèque énergie, ASPA, housing (start)
4. Housing benefit, unemployment & leave benefits (p65–84) — APL/AL, ARE, ASS, sickness/maternity/paternity
5. Social insurance contributions (p84–98) — employee/employer/self-employed SIC, Fillon, CSG, CRDS, capital levies
6. Personal income tax (p98–111) — IRPP base, quotient familial, schedule, décote, PFU, CEHR/CDHR, tax credits
7. Extraordinary measures & consumption taxes (p111–131) — Covid schemes, inflation lump sums, VAT, excises
8. Data & validation (p131–146) — EMSD/SILC vintage, imputations, external validation sources, health warnings
9. Annexes (p157–166) — uprating factors table, policy effects 2024–2025

---

## 1. Introduction & scope of simulation (CR pages 8-27)

Source: EUROMOD Country Report France Y16 (`Y16_CR_FR.pdf`), pages 8-27. Covers the French tax-benefit system 2022-2025 as implemented in EUROMOD version **J2.0+**. Authors: Laurence Bouvard, Alain Trannoy (national team), Silvia Navarro (JRC developer for France).

---

### 1.1 Basic information about the tax-benefit system

- **National system**: people are taxed the same way regardless of region. Exceptions: local taxes — land tax ("taxe foncière") and tax on occupied housing ("taxe d'habitation") — defined at regional level; rates set every year by local authorities.
- **Fiscal year**: 1 January to 31 December. Tax rules are usually determined in November each year, defining tax policy for the next year.
- **State pension age**:
  - 60 up to 30/06/2011; 2011 reforms increased state pension age to between 62 and 67 for full pension; reversed June 2012.
  - Pension amount depends on number of quarters worked. Minimum age was 62 when the retiree has the necessary number of contribution quarters for a full pension (otherwise: can leave at 62 with penalties, or work beyond 62 — but less than 67 — until reaching the required quarters).
  - **From 1 September 2023, a reform introduces a minimum retirement age of 64**, applied progressively by year of birth (63 years and 3 months in 2027 to 64 years in 2030, with 43 years of contribution).

**Table 1.1 — Retirement age by year of birth under the 2023 pension reform** (Source: CLEISS 2025, https://www.cleiss.fr/docs/regimes/regime_france/an_3.html)

| Year of birth | Retirement age |
|---|---|
| 1962 | 62 years and 6 months |
| 1963 | 62 years and 9 months |
| 1964 | 63 years |
| 1965 | 63 years and 3 months |
| 1966 | 63 years and 6 months |
| 1967 | 63 years and 9 months |
| From 1 January 1968 | 64 years |

- **School**: minimum leaving age 16; school obligation starts at 3 (since September 2019; before it was 6).
- **Dependent child for family benefits**: aged under 20 AND earning less than **55% of the minimum wage** (based on 169 hours/month employment, gross wage), or disabled and under 20. Used for calculation of social benefits.
- **Lone parents** (benefit and tax purposes): parents of resident dependent children under 18 who (a) do not cohabit with other adults who are not dependent (disabled), and (b) cohabit only with adults they cannot marry (mother, brother, cousin...).
- **Income tax unit**: joint system based on the tax group "**foyer fiscal**". Spouses assessed together; married or PACS (civil partnership) partners count as spouses. The tax group = one taxpayer + fiscally dependent persons (dependent children, dependent parents).
- **Fiscally dependent children**:
  - Under 18 (automatically)
  - Under 21 (if they choose to be declared with parents)
  - Under 25 and students (if they choose to be declared with parents)
  - Disabled (automatically, whatever their age)
  - Other adults can be dependent if disabled.
- **Quotient familial (family ratio)**: all incomes of the tax group are combined; a weight (number of shares) is given to each person; the family ratio is applied to total income before applying the tax schedule.
- **Tax return**: filed April-May with total revenue of the previous year.
- **Payment of income tax**:
  - Until 2018: (1) monthly withholding based on previous year's amount, adjusted in September; or (2) 3 payments per year ("tiers provisionnel"), third payment reassessed in September.
  - **From 2019: withholding income tax (prélèvement à la source)** — deducted by the employer directly from wages, by pension funds for pensioners, by the employment office ("pôle emploi") for the unemployed. Self-employed pay monthly or quarterly at their choice. The withholding rate is proposed by the administration based on previous years' income tax; the taxpayer may increase/decrease it; rates are automatically revised after the spring income return.
- **Indexation/uprating**: most benefits are indexed every year to inflation (particularly social minima). Tax brackets and amounts involved in tax computation are likewise re-evaluated for inflation.
- **Benefit assessment periods**: most benefits assessed yearly based on past income (previous year or the year before), or assessed for 3 months based on the past 12 months' income.
- **Legal working week**: 35 hours for full-time employees since 2000 (or 2002 depending on firm size); 39 hours before. Threshold for calculating overtime (with exceptions).
- **Consumption taxes**: (1) VAT with several rates, (2) harmonised excises on tobacco, alcohol and energy, (3) purchase of motor vehicles. See https://ec.europa.eu/taxation_customs/tedb/taxSearch.html
- Policy parameters saved as constants in the model (most recent year values): https://euromod-web.jrc.ec.europa.eu/resources/parameters

---

### 1.2 Social benefits

Three broad types: family benefits (means and non-means tested), replacement incomes, social assistance.

| Benefit (English) | French name | Acronym | Key rules |
|---|---|---|---|
| Family benefit | Allocations Familiales | AF | Main child benefit; households with 2+ dependent children; amount varies with number and age of children; income threshold since July 2015 |
| Means-tested benefit for young children | Prestation d'accueil du jeune enfant | PAJE | Families with children under 3 |
| Means-tested family complement | Complément familial | CF | Families with at least 3 dependent children aged 3 and over |
| Means-tested education grant | Allocation de rentrée scolaire | ARS | Annual lump sum paid in September for each dependent child aged 6-18; income threshold |
| Family support allowance | Allocation de soutien familial | ASF | NOT means-tested; paid for children under 20 not raised by both parents |
| Education allowance for handicapped children | Allocation d'Education de l'Enfant Handicapé | AEEH | Child under 20 with at least 79% disability, or 50-80% disability attending special school, or condition requiring special education; increased for lone parents |
| Disabled benefit | Allocation aux adultes handicapés | AAH | Working-age adults over 20 and under 62 who cannot work due to disability; permanent disability of at least 80%, or 50-79% with difficulties finding substantial and sustainable employment; income threshold |
| Solidarity labour income | Revenu de solidarité active | RSA | Guaranteed minimum income and low-earnings top-up; tested in 34 counties from May 2007, generalized from 1 June 2009; replaced RMI, single parent allowance (API — RSA increased in that case), and lump-sum aids like the grant of temporary return to work |
| Activity allowance | Prime d'activité | — | Created 1 January 2016; replaces the RSA activity component and the PPE tax credit; income threshold |
| Back-to-work allowance | Prime de retour à l'emploi | — | Until 31 December 2022: financial aid to RSA beneficiaries who find a job |
| Solidarity allowance for the elderly | Allocation de solidarité aux personnes âgées | ASPA | Minimum pension for persons aged 65+ with limited resources; varies with household income. Since 1 January 2006 replaces the minimum pension for elderly ("Minimum vieillesse", MV), merging a dozen benefits into one |
| Survivor minimum pension (widows/widowers) | Allocation veuvage | AV | Means-tested; limited in time (2 years); for spouses of a previously insured person, widowed at less than 55 years old, resources under a threshold |
| Personalized housing benefit | Aide personnalisée au logement | APL | Only tenants in subsidized housing or owners repaying state-subsidized loans; amount depends on resources and rent/loan repayment |
| Housing benefit | Allocation logement | AL | For those not eligible for APL; split into ALF (Allocation de logement familiale — tenants and owners eligible for other benefits like AF, ASF) and ALS (Allocation de logement sociale — tenants only, varies with resources and number of dependents) |
| Contributory pensions | — | — | PAYG system; basic + supplementary pension; managed by pension funds; proportional to career contributions |
| Unemployment benefit | Régime d'assurance chômage / Régime de solidarité nationale | RAC / RSN | RAC funded by employee+employer contributions; RSN compensates unemployed who exhausted RAC rights. The insurance agreement in force at unemployment start defines maximum duration and amount based on past wages |
| Sickness benefit | l'Assurance Maladie | AM | One of four branches of Sécurité Sociale; general, agricultural and independent schemes; covers sickness, maternity, disability, death, accidents/illnesses; funded by contributions on wages and CSG; CMU universal health coverage (income threshold) |
| Parental leave | congé maternité / congé paternité / congé d'adoption | — | Replacement income via l'Assurance Maladie under sickness-benefit conditions |

**Not strictly benefits — Student grants ("Bourse étudiante")**: non-taxable, means-tested on parental income; student must be under 28 on 1 October of the academic year and in qualifying training; awarded based on household income tax, number of children in the family's tax burden, and remoteness of place of study.

---

### 1.3 Social contributions

- **CSG (Contribution sociale généralisée)** — General social security contribution: levy with a social purpose allocated to the social security budget (national family fund, old-age solidarity fund, compulsory health insurance schemes). Paid on income of French residents and individuals subject to a French compulsory health insurance scheme.
- **CRDS (Contribution au remboursement de la dette sociale)** — clears social security deficits; paid by individuals domiciled in France for tax purposes who contribute to French compulsory health insurance.
- **Social contributions on capital income**:
  - "Prélèvement social" (introduced 1998) on personal assets and investment income — allocated to old-age solidarity fund, national retirement pension fund, pension reserve fund.
  - "Contribution additionnelle au prélèvement social" (2004) — allocated to CNSA (national solidarity fund for autonomy).
  - "Contribution additionnelle RSA" (2009) — funded the RSA; removed in 2013 and replaced by the "Prélèvement de solidarité" on the same incomes.
  - **Since 2018: total social contributions on capital income = 17.2%** (to which a **flat tax of 12.8%** is added). Not deductible from the income tax base; collected like the CSG on the same income.
- **Employee social contributions**: finance the Social Security System (illness, accident, disability, unemployment; old age, widowhood). Levied on the whole gross wage and related incomes. Several regimes for different types of workers.
- **Self-employed social contributions**: on gross profit; three types of self-employed (farmers, artisans, industry/trader workers) with quite different contribution rates.
- **Employer social contributions**: cover old-age, illness, unemployment etc., plus contributions financing family, housing, professional training and apprenticeship.
- Financing note: family benefits, sickness (since 2018), unemployment insurance (since 2019) and housing are financed **only by employer contributions**.

---

### 1.4 Taxes

- **Personal Income Tax ("Impôt sur le revenu des personnes physiques", IRPP)**: comprehensive annual tax on total income of the foyer fiscal in a calendar year; all incomes aggregated (net of social contributions for the wage part); single progressive scale; family quotient: sum of household incomes divided by number of shares before the tax schedule.
- **VAT ("Taxe sur la valeur ajoutée", TVA)** — 4 main rates:
  - **Standard 20%** since 01/01/2014 (19.6% before): all taxable transactions with no other rate.
  - **Intermediate/reduced 10%** since 01/01/2014 (7% before, since 01/01/2012): restaurants/catering, hotels, transport, firewood, agricultural unprocessed products, museum/zoo entrance fees, passenger transport.
  - **Reduced 5.5%** from 01/01/2012: food, utilities, basic-needs goods and services (books, sanitary products, gas and electricity subscriptions, canteen meals, cinema/live performance tickets, social housing).
  - **Special 2.1%**: certain medications (only those reimbursable by social security), certain cultural products, sales of live animals for slaughter.
- **Excise duty ("Droit d'accises")**: alcohol and alcoholic beverages, tobacco, fuel (TIPP), mineral oils, packaging. Alcohol, tobacco, energy are EU-harmonized; the first two ad-valorem, energy typically ad-quantum.
- **Wealth tax ("Impôt de solidarité sur la fortune", ISF)**: annual progressive tax on personal assets above **EUR 1,300,000** (since 1 January 2012); assessed by household (spouses, cohabiting partners, minor children). **Removed in 2018**, replaced by IFI.
- **Real estate wealth tax ("Impôt sur la fortune immobilière", IFI)**: annual progressive tax on net real estate (except professional real estate) above **EUR 1,300,000**; assessed by household; **30% abatement on the principal residence value**.
- **Exceptional contribution on high incomes ("Taxe exceptionnelle sur les hauts revenus")**: annual tax on the same income base as personal income tax (revenu fiscal de référence, RFR) above **EUR 250,000 for singles / EUR 500,000 for couples**.
- **Inheritance tax ("Droits de succession")**: progressive schedule; many exemptions/deductions depending on relationship and nature of donation/bequest.
- **Housing tax ("Taxe d'habitation", TH)**: paid by whoever has taxable residential premises at their disposal on 1 January (owner, tenant, free occupier; one tax per premises). Base = authority-assessed value × locally voted rates. **2018 reform**: phase-out for main residences — for eligible households (income/RFR condition, ~80% of households): reduction of 30% in 2018, 65% in 2019, 100% exoneration in 2020 and after; for the remaining 20% wealthiest households: 30% in 2021, 65% in 2022, 100% in 2023 and after.

**Table 1.2 — Applicable RFR thresholds for housing tax exoneration [2021-2022]** (Source: impots.gouv.fr chatbot fiche 2022-07-08)

| Family quotient (number of shares) | Maximum RFR 2021 | Maximum RFR 2022 |
|---|---|---|
| 1 | 27 761 € | 28 150 € |
| 1.5 | 35 986 € | 36 490 € |
| 2 | 44 211 € | 44 830 € |
| 2.5 | 50 380 € | 51 085 € |
| 3 | 56 549 € | 57 340 € |
| 3.5 | 62 718 € | 63 595 € |
| Each additional 0.5 | 6 169 | 6 255 |

- **Land tax ("Taxe Foncière", TF)**: annual, on land/permanent constructions in France; tax base = **50% of the value** (regularly updated by authorities) × locally voted rates; paid by owner at 1 January.
- **Waste tax ("Taxe sur les ordures ménagères")**: optional communal household waste collection tax, assessed on the cadastral income used as the base for property tax on developed land.
- **Motor vehicles**: tax on individuals and corporations owning motor vehicles; amount depends on type, cylinder capacity, horsepower, fuel type.

---

### 1.5 Temporary Covid-19 support measures

**2021** (renewals of 2020 measures):
- Exceptional solidarity fund compensating firms and self-employed for turnover losses (eligibility loss rate depends on sector; amount depends on sector and previous turnover).
- Financial assistance to self-employed (artisans-commerçants and micro-entrepreneurs), **maximum EUR 1,250 once a year**, amount based on previous contributions paid; postponement of social and tax contributions (exoneration for micro companies with fewer than 10 employees during lockdown).
- Government-guaranteed loans / loan rescheduling for struggling companies.
- Sickness benefit for workers who cannot telework or must care for children while schools are closed.
- Partial unemployment facilitated: firm pays **70% of gross wages (100% for SMIC and less)**, reimbursed by administration; from June 2020 reimbursement decreased to **60% of the 70%**, decreasing further in June, July, August 2021 (see sections 2.8 and 2.9).
- November 2020 - May 2021: exceptional monthly allowance for precarious workers combining short contracts and unemployment, guaranteeing a **minimum income of EUR 900/month**.

**2022**: following the Covid resumption (Dec 2021 - Jan 2022), previous measures renewed and reinforced in the most affected sectors (culture, tourism, events, nightclubs, hotels and restaurants, caterers, indoor entertainment) subject to public-access bans or gauging (details in sections 2.8 and 2.9).

---

### 2.1 Scope of simulation

Not the entire French tax-benefit system is simulated: gaps in data (e.g. no contribution history for pensions, no wealth information for property taxes) mean some instruments are taken directly from the microdata.

**Legend**: “E” = excluded (neither in micro-data nor simulated); “I” = included in micro-data but not simulated; “IA” = not simulated but included in an aggregate variable from the microdata; “PS” = partially simulated (some relevant rules not simulated); “S” = simulated (minor/very specific rules may not be); “-” = policy did not exist that year.

**Table 2.1 — Simulation of benefits in EUROMOD [2022-2025]**

| Benefit | Variable | 2022 | 2023 | 2024 | 2025 | Comments |
|---|---|---|---|---|---|---|
| Family benefit (AF) | bch00_s | S | S | S | S | |
| Means-tested allowances for young children (PAJE) | bchyc_s | S | S | S | S | |
| Free choice of activity - PreParE (PAJE) | bchcc_s | S | S | S | S | |
| Large family benefit (CF) | bchlg_s | S | S | S | S | |
| Means-tested education benefit (ARS) | bched_s | S | S | S | S | |
| Family support allowance (ASF) | bchor_s | S | S | S | S | Only simulated for widows/widowers with underage children; deserted/orphaned children cannot be identified in the data |
| Special education allowance (AEEH) | bchot | IA | IA | IA | IA | No information on disability status of children; included in other benefits for children |
| Disability benefit (AAH) | bdi_s | S | S | S | S | |
| Solidarity labour income (RSA) | bsa00_s | S | S | S | S | |
| Activity bonus | bsawk_s | S | S | S | S | |
| Return to work allowance | bsaot | IA | IA | IA | IA | No information about previous status before work; no information about continuous employment |
| Solidarity allowance for the elderly (ASPA) | bsaoa_s | PS | PS | PS | PS | Eligibility based on observed receipt in the data; full simulation possible but non-take-up leads to severe overestimation |
| Survivor minimum pension (AV) | bsuwd | I | I | I | I | Simulated but turned off in the baseline; no information about when a person became widowed |
| Housing benefit (APL) | bhoot | IA | IA | IA | IA | No information on subsidized loans, eligible subsidized tenancies, or asset values |
| Housing benefit (AL) | bhotn_s | S | S | S | S | Simulated for rent-paying tenants only; owner benefits included in bhoot; no asset value information |
| Housing benefit (AL, owners) | bhoot | IA | IA | IA | IA | Homeowner benefits cannot be simulated; included alongside other housing benefits; no asset value information |
| Contributory unemployment insurance benefit (ARE) | bunct_s | PS | PS | PS | PS | No contribution history; eligibility approximated by receipt in the data |
| Means-tested unemployment assistance benefit (ASS) | bunmt_s | PS | PS | PS | PS | Eligibility based on observed receipt; conditions only approximately simulated (no previous contributions / previous ARE receipt information) |
| Contributory pensions | poa | I | I | I | I | No contribution history or past wages |
| Sickness benefits (AM) | bhl | I | I | I | I | No information on days of sickness or previous contribution history |
| Disability pension | pdi00 | I | I | I | I | No degree of disability, no contribution history |
| Survivor pensions | psu | I | I | I | I | No contribution history |
| Partial unemployment linked to Covid-19 | bwkmcee_s | PS | - | - | - | Eligibility rules not simulated (firm-level); workers allocated randomly |
| Self-employment compensation linked to Covid-19 | bwkmcse_s | PS | - | - | - | Eligibility partially simulated; allocation among eligible done randomly |
| Exceptional support for self-employed linked to Covid-19 (Aide CPSTI RCI COVID-19) | bseec_s | S | - | - | - | Uses current self-employed SICs as proxy of previous contributions (not in dataset) |
| Social assistance linked to Covid-19 | bsaeccm_s | - | - | - | - | |
| Energy Bonus | bhoey_s | S | S | S | S | |
| Inflation compensation | binxp_s | S | S | - | - | Exceptional 2021-2022 lump-sum to compensate inflation increase |
| Purchasing power public servants | binps_s | - | S | - | - | Exceptional 2023 lump sum for purchasing power of some public servants |

**Table 2.2 — Simulation of taxes and social insurance contributions in EUROMOD [2022-2025]**

| Tax/SIC | Variable | 2022 | 2023 | 2024 | 2025 | Comments |
|---|---|---|---|---|---|---|
| Personal income tax (IRPP) | tin_s | S | S | S | S | Some tax allowances and tax credits cannot be simulated (missing data) |
| VAT | - | S | S | S | S | Based on extended input files with consumption expenditures from HBS |
| Excise duties | - | S | S | S | S | Based on extended input files with consumption expenditures from HBS |
| Exceptional contribution on high incomes | tinto_s | S | S | S | S | Based on current year only; no account of averaging with previous 2 years |
| Differential contribution on high incomes | tinto01_s | - | - | - | S | Based on current year only |
| Generalised social insurance contributions (CSG) | tscxc_s | S | S | S | S | |
| Insurance contributions for deficit repayment (CRDS) | tscdf_s | S | S | S | S | |
| SICs paid on capital income | tsckt_s | S | S | S | S | |
| SICs paid by employees | tscee_s | S | S | S | S | Only the general "regime" simulated; regimes cannot be identified |
| SICs paid by employers | tscer_s | S | S | S | S | Only the general "regime" simulated; regimes cannot be identified |
| SICs paid by the self-employed | tscse_s | S | S | S | S | |
| Wealth tax (ISF) | twl | - | - | - | - | Asset values not available in input dataset |
| Real estate wealth tax (IFI) | tpr | I | I | I | I | Asset values not available in input dataset |
| Housing tax (TH) | tmu | E | E | E | E | Housing values and municipality of residence not available |

Note: EUROMOD input data based on EU-SILC does not include the land tax; input data based on national SRCV (e.g. 2012) does include the land tax.

#### 2.1.1 Partially simulated tax-benefit components
Benefits using eligibility from observed receipt in the data (only partially simulated): **Solidarity allowance for the elderly (bsoa_s [sic — bsaoa_s in Table 2.1])**, **Contributory unemployment insurance benefit (bunct_s)** and **Means-tested unemployment assistance benefit (bunmt_s)** — simulated only for those observed receiving the benefit. Covid-19-related monetary compensations for employees (**bwkmcee_s**) and self-employed (**bwkmcse_s**) are also partially simulated: some eligibility conditions cannot be simulated and individuals are randomly allocated using external statistics.

---

### 2.2 Main policy changes

**Table 2.3 — Main policy changes [2022-2025]**

| Policies | 2022 → 2023 | 2023 → 2024 | 2024 → 2025 |
|---|---|---|---|
| SMIC | +4.03% | +5.4% | +2% |
| PSS (social security ceiling) | +6.9% | +1.13% | +1.6% |
| Social benefits | +1.6% | +4.6% | +1.7% |
| Pensions | +0.8% | +5.3% | +2.2% |
| Social insurance contributions | No change | Few changes for employers | No change for employees and little changes for employers |
| Direct taxes (income tax brackets) | +5.4% | +4.8% | +1.8% |
| Consumption taxes | No change | No change | No change |
| Other | Exceptional allowance on petrol expenses; change in income conditions for AAH; increase in public servants salary +1.5% | | |

*(Note: the SMIC/PSS percentages in Table 2.3 vs the narrative below are slightly inconsistent in the source PDF — the narrative says PSS +6.9% "in 2023" and +5.4% "in 2024", SMIC +1.13% in January 2024; recorded verbatim in both places.)*

#### 2.2.1 Main policy changes 2022 → 2023
- **PSS revalued by 6.9% in 2023**; social contributions unchanged for employees, employers and self-employed.
- **SMIC**: first increase of **1.81% in January 2023**; due to high inflation a second increase of **2.22% in May 2023** — increasing the general reduction in employers' contributions ("réduction Fillon") for eligible employees.
- **Unemployment benefit**: exceptional increase of **1.9% in April 2023** (inflation compensation). From **February 2023**, a reform **reduced the duration of the ARE by 25%** in case of good labour-market conditions.
- **Old-age pensions**: **+0.8% from January 2023** (after two 2022 rises: +1.1% January and +4% July 2022).
- **Social benefits**: **+1.6% in April 2023** to compensate inflation from higher energy prices. One-year inflation from April 2022 estimated at +5.6%; after the anticipated +4% increase of July 2022, the government added +1.6%.
- **2023 energy voucher**: between **EUR 48 and EUR 277**, given to the poorest 20% of households with **RFR/CU < EUR 11,000**. New in 2023: an energy voucher conditionally allocated to poor households heating with wood.
- **Exceptional petrol allowance**: **EUR 100** on petrol expenses for poor workers, under income conditions and on request.
- **AAH**: from **1 October 2023**, income conditions changed — **only the recipient's income counts, independently of the spouse's income** (deconjugalisation).
- **Housing benefits**: **+3.5% from 1 October 2023**.
- **Income tax brackets**: raised by **+5.4%**.
- **Public servants**: basic salary **+1.5% from 1 July 2023** (after +3.5% in July 2022); exceptional purchasing-power bonus for certain public servants, subject to income conditions, paid in a single lump sum in the last quarter of the year.

#### 2.2.2 Main policy changes 2023 → 2024
- **PSS revalued by 5.4% in 2024**; contributions unchanged for employees, changed a little for employers and self-employed.
- **SMIC**: increase of about **1.13% in January 2024**, increasing the general reduction in employers' contributions ("réduction Fillon").
- **Old-age pensions**: **+5.3% from January 2024**.
- **Social benefits**: **+4.6% in April 2024** to compensate inflation (one-year 2023 inflation estimated +4.9%).
- **2024 energy voucher**: between **EUR 48 and EUR 277**, poorest 20% of households with **RFR/CU < EUR 11,000**.
- **Petrol allowance**: **EUR 100** renewed in 2024 for poor workers on request, subject to income conditions and if petrol price exceeds the set alert threshold.
- **Housing benefits**: **+3.26% from 1 October 2024**.
- **Income tax brackets**: raised by **+4.8%**.
- No change in VAT since 2014.

#### 2.2.3 Main policy changes 2024 → 2025
- **PSS revalued by 1.6% in 2025**. Employee social contributions unchanged; **employer contributions increased**: for **sickness and family contributions, the ceilings have been decreased**, leading to an increase in the amount of these contributions.
- **SMIC**: **no increase at the beginning of 2025**; the previous increase of about **2% occurred in November 2024**, increasing the general reduction in employers' contributions ("réduction générale de cotisation").
- **Old-age pensions**: **+2.2% from January 2025**.
- **Social benefits**: **+1.7% in April 2025** (one-year 2024 inflation estimated +2%).
- **Daily sickness benefit**: ceiling reduced from **1.8 SMIC to 1.4 SMIC** in 2025 — reduces remuneration taken into account in the daily-allowance calculation for those with income above 1.4 SMIC.
- **Unemployment benefit duration**: changed for jobseekers aged **53 and over**, with a reduction in the number of days compensated.
- **Energy voucher**: 2024 voucher (EUR 48-277, poorest 20%, RFR/CU < EUR 11,000) renewed.
- **Housing benefits**: +3.26% from 1 October 2024 (**+1.04% in October 2025**).
- **Income tax brackets**: raised by **+1.8%**.
- **New in 2025**: an **exceptional differential tax on high incomes (CDHR)** ensuring the minimum total amount of tax equals **20% of income**.
- No change in VAT since 2014.

---

### 2.3 Order of simulation and interdependencies

The order is largely determined by interactions within the system: e.g. net taxable income (which determines eligibility for many means-tested benefits) is simulated before those benefits; contributory unemployment benefits (liable to income tax) are simulated before income tax.

**Table 2.4 — EUROMOD spine: order of simulation [2022-2025]**

| Policy | 2022 | 2023 | 2024 | 2025 | Description | Main output |
|---|---|---|---|---|---|---|
| Setdefault_fr | on | on | on | on | Default values for variables not in input dataset | |
| uprate_fr | on | on | on | on | Uprating of input data | |
| ConstDef_fr | on | on | on | on | Definition of constants used in the model | |
| IlsDef_fr | on | on | on | on | Standardized income concepts | |
| Ilsudbdef_fr | on | on | on | on | Standard UDB income concepts | |
| ildef_fr | on | on | on | on | Non-standardized income lists | |
| TUdef_fr | on | on | on | on | Definition of assessment units | |
| random_fr | on | on | on | on | Random numbers for take-up of RMI/RSA | i_takeup & i_takeup2 |
| transLMA_fr | off | off | off | off | Modelling labour market transitions | |
| yem_fr | switch | switch | switch | switch | Minimum wage | yem |
| neg_fr | on | on | on | on | Recoding of negative self-employment income | yse |
| yemcomp_fr (1) | on | on | on | on | Wage compensation scheme Covid-19 | bwkmcee_s |
| ysecomp_fr (1) | on | on | on | on | Self-employment compensation scheme Covid-19 | bwkmcse_s |
| bmact_fr | switch | switch | switch | switch | Maternity leave benefit | bmact_s |
| bpact_fr | switch | switch | switch | switch | Paternity leave benefit | bpact_s |
| bunct_fr | on | on | on | on | Unemployment insurance benefit (Allocation de retour à l'emploi, ARE) | bunct_s |
| bchor_fr | on | on | on | on | Family Support Allowance (Allocation de soutien familial, ASF) | bchor_s |
| tscee_fr | on | on | on | on | Employee social insurance contributions | tscee_s |
| bch00_fr | on | on | on | on | Universal child benefit (Allocation Familiale, AF) | bch00_s |
| tscer_fr | on | on | on | on | Employer social insurance contributions | tscer_s |
| tscse_fr | on | on | on | on | Self-employed social insurance contributions | tscse_s |
| bseec_fr | on | on | on | on | Exceptional support for self-employed linked to Covid-19 | bseec_s |
| tsckt_fr | on | on | on | on | SICs paid on capital income | tsckt_s |
| bsuwd_fr | off | off | off | off | Minimum survivor pension (Allocation veuvage, AV) | bsuwd_s |
| tinty_fr | on | on | on | on | Net taxable income | il_rniy |
| tscxc_fr | on | on | on | on | Generalized SICs (Contribution Sociale Généralisée, CSG) | tscxc_s |
| tinkt_s | on | on | on | on | Personal income tax with flat-rate taxation of capital income (Prélèvement forfaitaire non libératoire, PFL) | temp_tingt1 |
| tin_fr | on | on | on | on | Personal income tax using the progressive tax schedule only, and optimization of gross tax | temp_tingt2; tingt_s |
| tincot_fr | on | on | on | on | Tax credits other than PPE | tintcch_s; tintcmi_s; tintced_s |
| tintcee_fr | n/a | n/a | n/a | n/a | Low earner refundable tax credit (Prime Pour L'Emploi, PPE) & net tax | tintcee_s; tin_s |
| tinto01_fr | n/a | n/a | n/a | on | Differential contribution on high income (CDHR) | tinto01_s |
| bdi_fr | on | on | on | on | Means-tested disability benefit (Allocation aux adultes handicapés, AAH) | bdi_s |
| bunmt_fr | on | on | on | on | Unemployment assistance benefit (Allocation de solidarité spécifique, ASS) | bunmt_s |
| bchyc_fr | on | on | on | on | Means-tested benefit for young children (Prestation d'Accueil du Jeune Enfant, PAJE) | bchyc_s |
| bchba_fr | on | on | on | on | Means-tested birth grant (Prime de naissance, PN) | bchba_s |
| bchcc_fr | on | on | on | on | Parental leave supplement (Complément de libre choix d'activité, PreParE) | bchcc_s |
| bched_fr | on | on | on | on | Means-tested education grant (Allocation de rentrée scolaire, ARS) | bched_s |
| bchlg_fr | on | on | on | on | Means-tested benefit for large families (Complément familial, CF) | bchlg_s |
| bhotn_fr | on | on | on | on | Means-tested housing benefits (Allocation Logement, AL) | bhotn_s |
| bsaoa_fr | on | on | on | on | Means-tested solidarity allowance for the elderly (Allocation de solidarité aux personnes âgées, ASPA) | bsaoa_s |
| tscdf_fr | on | on | on | on | Contribution for the deficit repayment (Contribution pour le Remboursement de la Dette Sociale, CRDS) | tscdf_s |
| bsa00_fr | on | on | on | on | Minimum guaranteed income (Revenu minimum d'insertion RMI / Revenu de solidarité active RSA) | bsa00_s |
| bsawk_fr | on | on | on | on | Activity allowance (Prime d'activité) | bsawk_s |
| bsaeccm_fr | n/a | n/a | n/a | n/a | Social assistance linked to Covid-19 | bsaeccm_s |
| bhoey_fr | on | on | on | on | Energy bonus | bhoey_s |
| binxp_fr | on | n/a | n/a | n/a | Exceptional 2021-2022 inflation compensation | binxp_s |
| binps_fr | n/a | on | n/a | n/a | Exceptional 2023 purchasing power premium | binps_s |
| tco_fr | on | on | on | on | Consumption taxes | il_tva; il_txa; il_txv |
| output_std_fr | on | on | on | on | Standard output file at the individual level | |
| output_std_hh_fr | off | off | off | off | Standard output file at the household level | |

Note (1): Covid-19 policies are not included in the baseline even if "on" in the spine, since they only work when labour market transitions (transLMA) are switched on.

---

### 2.4 Policy extensions (switchable from the Run dialogue box)

- **Uprating by Average Adjustment (UAA)** — default **off**. When on, pension income is uprated by changes in the average pension rather than indexation rules.
- **Minimum wage (yem_fr)** — default **off** in the baseline. Individual earnings checked against the minimum wage in force at **30 June** of the policy year; wages below the minimum (adjusted for hours worked and time in employment) are raised to the minimum wage threshold.
- **Parental leave benefits** (maternity **bmact_fr**, paternity **bpact_fr**) — implemented for policy years **2015-2025**; turned **off** in the baseline due to validation/consistency issues; can be switched on.
- **Full Year Adjustments (FYA)** — default **on** for 2022-2025. EUROMOD normally simulates policies as of **June 30th**; FYA simulates within-year policy changes via a weighted average of amounts before/after the change (weighted by number of months each amount applies).
- **Benefit Take-up Adjustments (BTA)** — default **on**. Applies non-take-up corrections for material-need benefits (**bsa00_fr, bsawk_fr**): a share of (weighted) eligible observations equal to the take-up rate is randomly selected as beneficiaries; the rest lose the benefit. Shares functions with BCA; as a rule only one should be on — if both are on, the **lowest** of take-up rate and calibration rate applies.
- **HHoT – Unemployment extension (HHoT_un)** — improves unemployment insurance simulation with hypothetical data (employment-history variables not in SILC can be defined in HHoT). On when using HHoT data.
- **HHoT Monthly Unemployment (HHoT_mu)** — monthly unemployment benefit simulation (OECD TaxBEN-style NRR indicators); amounts computed for a specific month of the unemployment spell, then annualized (×12). Default **off**; on only for NRR indicator calculations.
- **LMA transitions** — triggers transitions to wage unemployment, for use with the LMA add-on. Default **off** (no transitions in baseline).
- **Months and hours in wage compensation scheme (yemcomptime_fr)** — triggers transitions to Covid-19 wage compensation schemes in 2020, 2021, 2022. Default **off** (no eligible individuals for yemcomp_fr in baseline).
- **Months and hours in self-employment compensation scheme (ysecomptime_fr)** — same for Covid-19 self-employment compensation (ysecomp_fr) in 2020, 2021, 2022. Default **off**.
- **Survivors pension for widowhood ("Allocation Veuvage", AV) (bsuwd_fr)** — simulated with assumptions due to lack of micro-data information (see sections 2.5.7 and 2.5.11); results do not match administrative statistics well, so **off** in the baseline.
- **Benefit Calibration Adjustments (BCA)** — default **off**. Calibrates receipt of **bsa00_fr** and **bsawk_fr** so simulated total expenditure matches real expenditure from external statistics; a random subset of eligible observations is selected until real expenditure is reached. If both BCA and BTA are on, the lowest of the take-up and calibration rates applies.

---

## 2. Family & disability benefits (CR pages 27-46)

Source: EUROMOD Country Report France (Y16_CR_FR.pdf), section 2.5 "Benefits", pages 27-46 (plus page 47 for the end of the AAH section). All monetary values in EUR. "Gross from CRDS" means amounts before the CRDS levy is deducted.

---

### 2.5.1. Universal child benefit: Family benefit — bch00_s — (Allocation Familiale, AF)

#### Definitions
Children are considered dependent persons if they are aged under 20 and earning less than 55% of the minimum wage (based on SMIC for 169 hours/month).

#### Eligibility conditions
- Paid in arrears to households with **two or more dependent children**.
- Household resources must not exceed the amount determined based on the applicant's family situation.
- In cases of legal separation or divorce of the parents, the beneficiary is the parent who maintains the children.

#### Income test
The benefit was **not means-tested until 1st July 2015**. Since then, both the family benefit and the increased amount for children over 14 are subject to income testing.

The households' resources (**Revenu Net Catégoriel**) determine the benefit amount. This income concept should not be confused with the Reference Fiscal Income (Revenu Fiscal de Référence, RFR): the Revenu Net Catégoriel is used as the means test for Family Benefits, while the RFR is used as the means test for Housing Benefit and as the tax base to calculate income tax. The income concepts are built as follows:

1. **Revenu Brut Global (Total Gross Income):**
   - (a) C1 income (net after 10% deduction or actual expenses): employment income (excluding overtime > 5,000 EUR from 2019) + overtime pay > 5,000 EUR (if applicable) + sickness benefits + unemployment benefits + contributory pensions + private pensions + survivor minimum pension
   - (b) C2 income: self-employment (net after business expenses)
   - (c) C3 income: capital income — investment income (dividends, interest, etc.) + property/rental income (net after expenses or 30% micro-foncier deduction)
   - (d) C4 income: capital gains (plus-values)
2. **Revenu Net Global (Total Net Income)** — deductible charges from global income: alimony payments; retirement savings contributions (PERP, etc.); deductible CSG on activity income (6.8% of base); deductible CSG on replacement income (varies by rate); deductible CSG on capital income; costs for dependent elderly persons (75+)
3. **Revenu net imposable (Net Taxable Income)** — special tax allowances/abattements: for elderly persons (65+); for disabled persons; for dependent children over 18
4. **Revenu Fiscal de Référence, RFR (Reference Fiscal Income)** — deductions on C1, C2 and C3 incomes

Families may receive the **full rate, 50% or 25%** of the benefit amount depending on their **n-2 income (RFR)**, i.e. 2023 income for benefit in 2025.

**Table 2.5 Family benefit income thresholds [2022-2025]** (maximum annual family RFR amount, for basic benefit and for over-14-years-old increase)

Thresholds 2022:

| Benefit rate | 2 dependent children | 3 dependent children | Income increase per child after the 3rd |
|---|---|---|---|
| Full rate | ≤ 70,074 | ≤ 75,913 | + 5,839 |
| Rate at 50% | 70,074 < RFR ≤ 93,399 | 75,913 < RFR ≤ 99,238 | + 5,839 |
| Rate at 25% | > 93,399 | > 99,238 | + 5,839 |

Thresholds 2023:

| Benefit rate | 2 dependent children | 3 dependent children | Income increase per child after the 3rd |
|---|---|---|---|
| Full rate | ≤ 71,194 | ≤ 77,126 | + 5,932 |
| Rate at 50% | 71,194 < RFR ≤ 94,893 | 77,126 < RFR ≤ 100,825 | + 5,932 |
| Rate at 25% | > 94,893 | > 100,825 | + 5,932 |

Thresholds 2024:

| Benefit rate | 2 dependent children | 3 dependent children | Income increase per child after the 3rd |
|---|---|---|---|
| Full rate | ≤ 74,966 | ≤ 81,212 | + 6,246 |
| Rate at 50% | 74,996 < RFR ≤ 99,922 (as printed in the CR; full-rate row says 74,966) | 81,212 < RFR ≤ 106,168 | + 6,246 |
| Rate at 25% | > 99,922 | > 106,168 | + 6,246 |

Thresholds 2025:

| Benefit rate | 2 dependent children | 3 dependent children | Income increase per child after the 3rd |
|---|---|---|---|
| Full rate | ≤ 78,565 | ≤ 85,111 | + 6,546 |
| Rate at 50% | 78,596 < RFR ≤ 104,719 (as printed in the CR; full-rate row says 78,565) | 85,111 < RFR ≤ 111,265 | + 6,546 |
| Rate at 25% | > 104,719 | > 111,265 | + 6,546 |

Source: https://www.caf.fr/allocataires/aides-et-demarches/droits-et-prestations/vie-personnelle/les-allocations-familiales-af

#### Benefit amount
The benefit amount is the amount below multiplied by the percentage (rate) above. The monthly amount depends on the number and age of dependent children in the household (gross from CRDS) and on the household income.

**Table 2.6 Family benefit amount in gross from CRDS [2022-2025]** (monthly amounts, EUR)

| | 2022 | 2022 (from 1 July)¹ | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| 2 dependent children | 135.14 | 140.53 | 142.70 | 149.27 | 151.81 |
| 3 dependent children | 308.26 | 320.59 | 325.54 | 340.50 | 346.29 |
| Each child after the 3rd | 173.14 | 180.06 | 182.83 | 191.25 | 194.49 |
| Increment for child over 14 | 67.57 | 70.27 | 71.36 | 74.63 | 75.91 |
| Fixed amount paid to families of 3+ children with eldest of 20-21 | 85.45 | 88.86 | 90.24 | 94.38 | 95.99 |

Notes: Indexation — the amounts change each 1st of April. ¹ On July 1st 2022, the amounts increased by 4%.

- For families with only 2 dependent children, the increased amount for children over 14 concerns **only the second child** — it is not paid for the first child.
- The **fixed amount paid to families of 3+ children** (forfait) is paid under two conditions:
  1. One of the children is 20 years old, lives at home, and does not work, or has remuneration less than 55% of the minimum wage calculated on 169 hours/month in gross (or 78% of net SMIC based on 151.67 hours/month), i.e. **982.48 EUR in 2022 / 1,028.96 EUR from July 2022 / 1,047.55 EUR from April 2023 / 1,082.87 EUR from April 2024 / 1,104.25 EUR from April 2025**.
  2. The family has received benefits for at least three children in the month before the 20th birthday.
- Qualifying families receive the monthly lump sum until the month before the child turns 21. Like the AF, this lump sum is paid at full rate, 50% or 25% depending on net taxable income (RFR).

#### Compatibilities
Compatible with national or regional lump-sum child benefits. If one of the children receives APL (housing benefit), it means he has his own home; the household is then no longer eligible for AF.

#### Taxation and income testing
Not taxable and not included in the income test of other benefits (**except for activity allowance and RSA**), but subject to **CRDS**.

#### EUROMOD modelling
- Simulated based on the **age of children at the end of the income reference period**. No benefit is simulated for children who reach the age threshold during the income reference period (month of birth unknown).
- The age-based increase is simulated for the entire year for children who turn 14 in the income reference period.
- The supplement for children aged 20 is simulated for the entire year whenever a person aged 20 (who is not head or partner) lives with at least two dependent children.
- The 1 July 2022 increment is introduced with the **FYA** (full-year adjustment), calculated as a weighted average of the amounts before and after 1 July.

---

### 2.5.2. Means-tested benefit for young children — Prestation d'accueil du jeune enfant (PAJE)

PAJE contains:
- **PAJE base amount ("allocation de base")**: means-tested benefit for children under 3 (bchyc_s).
- **Baby bonus ("prime de naissance")**: means-tested bonus for childbirth (bchba_s).
- **Supplement for free choice of custody ("complément de libre choix du mode de garde")**: for families with children born after 2004 and aged under 6, where parents work, are under the income threshold and employ a certified carer. **Not simulated in EUROMOD** due to the lack of information about child minding.
- **Supplement for free choice of activity ("complément de libre choix d'activité", CLCA)**: replaced the Parent education allowance ("allocation parentale d'éducation", APE) for children born after 2004. Since 1st January 2015 it was modified and replaced by **"Prestation partagée d'éducation de l'enfant, PreParE"** (bchcc_s).

---

### 2.5.2.1. Basic Allowance for young children — bchyc_s — (Allocation de base de la PAJE)

#### Eligibility conditions
Means-tested allowance received by households with **children under 3**. From **April 1st 2014** the benefit was reformed: children born after April 1st are subject to new rules; entitlement of children born before that date is unaffected (old rules apply).

The income test depends on the number of parents who work. For two-earner couples, a minimum threshold applies to the earnings of **each** parent to be considered a two-earner couple; if each member earns less than the threshold, they are treated as a one-earner couple and the one-earner threshold applies.

**Table 2.7 Annual individual income threshold to be considered an earner for PAJE base, income n-2 [2022-2025]**

| | 2022 (income 2020) | 2023 (income 2021) | 2024 (income 2022) | 2025 (income 2023) |
|---|---|---|---|---|
| Each member of the couple should earn more than | 5,594 | 5,594 | 5,594 | 5,983 |

Source: https://caf.fr/professionnels/offres-et-services/accompagnement-des-allocataires/bareme-prime-la-naissance-et-allocation-de-base

#### Definitions
Children are dependent persons if aged under 20 and earning less than 55% of the minimum wage (169 h/month basis). The assessment unit includes parents (married or cohabiting) and their dependent children.

#### Income test
Entitlement is subject to an income test: household resources in **year n-2** must be below the threshold. Ceilings depend on the child's date of birth. For children born after 1st April 2014 there are new ceilings and the benefit is no longer flat-rate but depends on income.

**Table 2.8 PAJE base, Ceilings C1: ceilings granting access to the benefit (partial rate), children born or adopted after April 2018 [2022-2025]** (yearly amounts, EUR)

| Yearly amount | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| **One earner couples** | | | | |
| One dependent child | 32,520 | 33,040 | 34,791 | 36,461 |
| Two dependent children | 39,024 | 39,648 | 41,749 | 43,753 |
| Three dependent children | 46,829 | 47,578 | 50,099 | 52,504 |
| Each child after the third | 7,805 | 7,930 | 8,350 | 8,751 |
| **Two earner couples or lone parent** | | | | |
| One dependent child | 42,978 | 43,665 | 45,979 | 48,186 |
| Two dependent children | 49,482 | 50,273 | 52,937 | 55,478 |
| Three dependent children | 57,287 | 58,203 | 61,287 | 64,229 |
| Each child after the third | 7,805 | 7,930 | 8,350 | 8,751 |

#### Benefit amount
Since 1st April 2014 the monthly amount depends on parents' income:
- Income **below ceiling 2** → **100%** of the benefit amount (full rate).
- Income **above ceiling 2 but below ceiling 1** → benefit reduced to **50%** of the full amount (partial rate).

**Table 2.9 PAJE base, Ceilings C2 for full rate after 1st of April 2018 [2022-2025]** (yearly amounts for full benefit, EUR)

| Yearly amount for full benefit | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| **One earner couples** | | | | |
| One dependent child | 27,219 | 27,654 | 29,120 | 30,518 |
| Two dependent children | 32,663 | 33,185 | 34,944 | 36,621 |
| Three dependent children | 39,196 | 39,822 | 41,933 | 43,946 |
| Each child after the third | 6,533 | 6,637 | 6,989 | 7,324 |
| **Two earner couples or lone parent** | | | | |
| One dependent child | 35,971 | 36,546 | 38,483 | 40,330 |
| Two dependent children | 41,415 | 42,077 | 44,307 | 46,434 |
| Three dependent children | 47,948 | 48,714 | 51,296 | 53,758 |
| Each child after the third | 6,533 | 6,637 | 6,989 | 7,324 |

The monthly amount is **per family** (not per child, except for multiple births), gross from CRDS:

**Table 2.10 PAJE base, monthly amount per family in gross from CRDS [2022-2025]** (EUR)

| | 2022 | 2022 (from 1 July)¹ | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Monthly amount (full rate) | 175.89 | 182.91 | 185.74 | 194.28 | 197.59 |
| Monthly amount (half rate) | 87.95 | 91.47 | 92.86 | 97.13 | 98.79 |

Note: ¹ On July 1st 2022 the amount increased by 4%.

#### Compatibilities
Compatible with national or regional lump-sum child benefits, **except** the Family Complement (CF) and Family Support allowance (ASF).

#### Taxation and income testing
Not taxable and not included in the income test of other benefits (**except for activity allowance and RSA**), but subject to **CRDS**.

#### EUROMOD modelling
- Income test is calculated on **yearly net taxable income during the income reference period** (rather than past taxable income).
- Simulation based on the age of children at the end of the income reference period: no benefit for children turning 3 during the period; benefit simulated for the entire year for children born during the period.
- For the transition to the new ceilings/amounts of 31 March 2018, the assumption is that all kids were born after March 31st; consequently, from 2020 onwards, kids born before 2018 (old ceilings) are already 3+ and no longer eligible.
- Adoption of children over 3 cannot be simulated (no data on adopted children over 3), although in law they may receive the benefit for 3 years before their 20th birthday.
- New rules simulated for all children born in 2014 or 2018 irrespective of month of birth.
- Variable **bchyc_s contains only the PAJE base amount**; the baby bonus and PreParE are stored in **bchba_s** and **bchcc_s**. The supplement for free choice of custody is not simulated (no child-minding information).
- The 1 July 2022 increment is introduced with the FYA, weighted average of amounts before and after 1 July.

---

### 2.5.2.2. Means-tested birth grant: Baby bonus — bchba_s — (Prime de naissance, PAJE)

#### Definitions
Children are dependent persons if aged under 20 and earning less than 55% of the minimum wage (169 h/month basis).

#### Eligibility conditions
Have a child born in the year, or have adopted a child under 20 years of age; comply with the eligibility conditions of the PAJE allocation de base.

#### Income test
For children born after 1st April 2018, the annual family net taxable income must be below the following thresholds (**same as PAJE Ceilings C1**):

**Table 2.11 PAJE baby bonus, income thresholds for child born after 1st of April 2018 [2022-2025]** (EUR)

| | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| **One earner couples** | | | | |
| One dependent child | 32,520 | 33,040 | 34,791 | 36,461 |
| Two dependent children | 39,024 | 39,648 | 41,749 | 43,753 |
| Three dependent children | 46,829 | 47,578 | 50,099 | 52,504 |
| Each child after the third | 7,805 | 7,930 | 8,350 | 8,751 |
| **Two earner couples or lone parent** | | | | |
| One dependent child | 42,978 | 43,665 | 45,979 | 48,186 |
| Two dependent children | 49,482 | 50,273 | 52,937 | 55,478 |
| Three dependent children | 57,287 | 58,203 | 61,287 | 64,229 |
| Each child after the third | 7,805 | 7,930 | 8,350 | 8,751 |

#### Benefit amount
Lump sum for each child born in the year (gross from CRDS):

**Table 2.12 PAJE baby bonus amount in gross from CRDS [2022-2025]** (EUR)

| | 2022 | 2022 (from 1 July)¹ | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Childbirth | 970.19 | 1,008.99 | 1,024.55 | 1,071.67 | 1,089.88 |
| Adoption | 1,940.38 | 2,018 | 2,049.09 | 2,143.35 | 2,179.74 |

Note: ¹ On July 1st 2022 the bonus amount increased by 4%.

#### Compatibilities
Compatible with national or regional lump-sum child benefits.

#### Taxation and income testing
Not taxable and not included in the income test of other benefits, but subject to **CRDS**.

#### EUROMOD modelling
- No information on adoptions in the data → **only the childbirth benefit is simulated**.
- Income test based on **current** yearly net taxable income rather than previous taxable income.
- The 1 July 2022 increment introduced with the FYA (weighted average before/after 1 July).

---

### 2.5.2.3. Supplement for free choice of activity — bchcc_s — (PreParE, PAJE)

#### Definitions
Children are dependent persons if aged under 20 and earning less than 55% of the minimum wage (169 h/month basis).

#### Eligibility conditions
- Have at least one child under 3 years of age.
- Stop or partially stop working to take care of the child. The beneficiary must have made social security contributions for **8 quarters** out of: the previous **2 years** (1st child), the previous **4 years** (2nd child), or the previous **5 years** (3rd+ child).

#### Income test
The benefit is **not means-tested**.

#### Benefit amount (duration rules)
- **First child, couple**: each parent can receive the benefit for at most **6 months** from birth/end of maternity leave, within the child's first birthday. **Lone parents**: paid at most **12 months** within the child's first birthday.
- **Two or more children**: paid from birth/end of maternity leave until the month before the 3rd birthday of the youngest, but claimable (by either parent) for a maximum of **24 months** (within the limit of the youngest child's third birthday). Lone parents: paid until the month before the 3rd birthday of the youngest.
- **Triplets**: paid from birth/end of maternity leave until the month before the **6th** birthday, but each parent at most **48 months**. Lone parents: paid until the month before the 6th birthday.
- **Adoptions**: one child in the family — each parent at most 12 months; other children present — each parent at most 12 months; if after this period the child is under 3, parents can receive the benefit until the 3rd birthday. If an adoption concerns at least 3 children, parents can receive the benefit for the first 36 months after adoption.

**Table 2.13 PAJE-PreParE amount in gross from CRDS [2022-2025]** (monthly, EUR)

| Gross amount from CRDS | 2022 | 2022 (from 1 July)¹ | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Full rate (stop working completely) | 408.01 | 424.33 | 430.86 | 450.68 | 458.34 |
| Reduce work to < 50% | 263.77 | 274.31 | 278.53 | 291.35 | 296.29 |
| Reduce work to 50-80% | 152.15 | 158.23 | 160.67 | 168.06 | 170.92 |

Note: ¹ On July 1st 2022 the amount increased by 4%.

**PreParE Majorée**: families with three children can opt for it. Each parent can receive it for at most **8 months** from birth/end of maternity leave until the child's first birthday; lone parents at most **12 months** until the first birthday. Same contribution requirements as PreParE, at the following rate (gross from CRDS):

**Table 2.14 PAJE-PreParE majorée amount in gross from CRDS [2022-2025]** (monthly, EUR)

| PreParE Majorée | 2022 | 2022 (from 1 July)¹ | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Amount | 666.91 | 693.59 | 704.27 | 736.65 | 749.18 |

Note: ¹ On July 1st 2022 the amount increased by 4%.

#### Compatibilities
**Not compatible** with paid holidays, maternity/paternity/adoption leave, sick leave or unemployment benefit.

#### Taxation and income testing
Not taxable and not included in the income test of other benefits (**except for activity allowance and RSA**), but subject to **CRDS**.

#### EUROMOD modelling
- Detailed contribution history not available: eligibility is based on fulfilling a contributory requirement of **2 years of contributions during the entire work history**; the differing requirements by birth order are not simulated.
- Amounts simulated based on earnings and current working hours. Entitlement to the out-of-work amount is based on absence of earnings during the entire income reference period. Reduced amounts (reduced working time) are based on **current** (rather than contemporaneous) working hours.
- Only one child present: benefit simulated for **6 months** during the income reference period conditional on the child being aged 0 (assumed paid in the first year after birth); no entitlement simulated for children aged 1 & 2 when only one child is present.
- It is assumed a parent always takes up the **PreParE Majorée** if entitled: simulated for all entitled parents (fulfilling contribution requirements and stopping work) whose **third child is aged 0**; assumed not paid for children aged 1 and 2.
- Simulation based on ages at the end of the income reference period, i.e. benefits received for only part of the year (before a child turns 3 or 1) are not simulated.
- Only the incompatibility with **unemployment benefits and sickness benefits** is simulated (other benefits are short-term with no within-year receipt information). Other incompatibilities are not simulated.
- Higher benefits for adoption and longer benefits for triplets are **not simulated**.
- The 1 July 2022 increment introduced with the FYA (weighted average before/after 1 July).

---

### 2.5.3. Means-tested education grant — bched_s — (Allocation de rentrée scolaire, ARS)

#### Definitions
Children are dependent persons if aged under 20 and earning less than 55% of the minimum wage (169 h/month basis).

#### Eligibility conditions
Have at least one child **aged 6 to 18 attending school**. The child must not earn more than 55% of the minimum wage (169 h/month basis).

#### Income test
Depends on the number of dependent children:

**Table 2.15 ARS, income test [2022-2025]** (EUR per year)

| Euros per year | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| One dependent child | 25,370 | 25,775 | 27,141 | 28,444 |
| Two dependent children | 31,225 | 31,537 | 33,404 | 35,008 |
| Three dependent children | 37,080 | 37,392 | 39,667 | 41,572 |
| Each child after the third | 5,855 | 5,948 | 6,263 | 6,564 |

Source: https://www.caf.fr/allocataires/aides-et-demarches/droits-et-prestations/vie-personnelle/l-allocation-de-rentree-scolaire-ars

**ARS différentielle (AD)** — since 2012, households slightly exceeding the income threshold are eligible for a residual amount if their revenue is less than the threshold plus the relevant benefit amount, where N is the number of children:

AD = (income threshold + (ARS6-10 × N6-10) + (ARS11-14 × N11-14) + (ARS15-18 × N15-18) − income) / N

with a **minimum payment of €15**. The income used is the net taxable income.

#### Benefit amount
Paid **per child**; yearly amount depends on the child's age (gross from CRDS):

**Table 2.16 ARS, amounts in gross from CRDS [2022-2025]** (EUR per child per year)

| Benefit amount per child | 2022 | 2022 (from 1 July)¹ | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| 6-10 years | 378.87 | 394.02 | 400.09 | 418.50 | 425.61 |
| 11-14 years | 399.78 | 415.77 | 422.14 | 441.59 | 449.09 |
| 15-18 years | 413.63 | 430.17 | 436.78 | 456.87 | 464.65 |

Note: ¹ On July 1st 2022 the amount increased by 4%.

#### Compatibilities
Compatible with national or regional lump-sum child benefits.

#### Taxation and income testing
Not taxable and not included in the income test of other benefits, but subject to **CRDS**.

#### EUROMOD modelling
- Simulation based on **current rather than previous taxable income**.
- Uses ages of children **at the end of the income reference period** rather than at the start of the school year.

---

### 2.5.4. Family support allowance — bchor_s — (Allocation de soutien familial, ASF)

#### Definitions
Children are dependent persons if aged under 20 and earning less than 55% of the minimum wage (169 h/month basis).

#### Eligibility conditions
Must be a **lone parent or other carer** (e.g. grandparent) where the other parent (or both parents) is deceased, has abandoned the child, or does not pay alimony.

#### Income test
This benefit is **not means-tested**.

#### Benefit amount
Monthly amount per child (gross from CRDS):

**Table 2.17 ASF, amount gross from CRDS [2022-2025]** (EUR per child per month)

| Benefit amount | 2022 | 2022 (from 1 July)¹ | 2022 (from 1 Nov)² | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| Child living with lone parent | 118.79 | 123.55 | 185.34 | 188.18 | 196.83 | 200.18 |
| Child living with no parents | 158.36 | 164.69 | 247.03 | 250.84 | 262.38 | 266.83 |

Notes: ¹ On July 1st 2022 the amount increased by 4%. ² On November 1st 2022, support for single-parent families being one of the government's priority policies, the amount was **increased by 50%**.

Source: https://www.caf.fr/allocataires/aides-et-demarches/droits-et-prestations/vie-personnelle/l-allocation-de-soutien-familial-asf

#### Compatibilities
Compatible with national or regional lump-sum child benefits.

#### Taxation and income testing
Not taxable and not included in the income test of other benefits (**except for social assistance (RSA) and Activity allowance**), but subject to **CRDS**.

#### EUROMOD modelling
- Simulated **only for children of widows/widowers**: it is not possible to identify children abandoned by parents, nor children whose both parents are deceased.
- The increments of July 1st and November 1st 2022 are introduced with the FYA, calculated with a weighted average of the amounts before and after each change.

---

### 2.5.5. Means-tested family complement — bchlg_s — (Complément familial, CF)

#### Definitions
Children are dependent persons if aged **under 21** and earning less than 55% of the minimum wage (169 h/month basis). Children under 21 who are themselves parents may be considered dependent if not receiving family benefits.

#### Eligibility conditions
- Have at least **3 children, all aged 3 years or more**.
- The amount is the same for all families regardless of the number of dependent children, but since 1st April 2014 the monthly amount depends on parents' income and on the number of dependent children.
- The child must not earn more than 55% of the minimum wage (169 h/month basis).

#### Income test
Depends on the number of earners. For two-earner couples, a minimum threshold applies to the earnings of each parent (same mechanism as PAJE): if each member earns less than the threshold, the one-earner threshold applies.

**Table 2.18 CF, annual individual income threshold to be considered an earner [2022-2025]**

| | 2022 (income 2020) | 2023 (income 2021) | 2024 (income 2022) | 2025 (income 2023) |
|---|---|---|---|---|
| Each member of the couple should earn more than | 5,594 | 5,594 | 5,594 | 5,983 |

**Table 2.19 CF, income Ceiling 1 granting access to the benefit [2022-2025]** (yearly income for family with 3 children, EUR)

| Yearly income for family with 3 children | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| One earner couples | 39,196 | 39,822 | 41,933 | 43,946 |
| Two earner couples or lone parent | 47,948 | 48,714 | 51,296 | 53,758 |
| Increase for each dependent child after 3rd | 6,533 | 6,637 | 6,989 | 7,324 |

Note: the income used is the **net taxable income**.

**Table 2.20 CF, income Ceiling 2 for receiving the increased amount [2022-2025]** (EUR)

| Yearly income for family with 3 children | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| One earner couples | 19,603 | 19,915 | 20,971 | 21,978 |
| Two earner couples or lone parent | 23,979 | 24,362 | 25,653 | 26,884 |
| Increase for each dependent child after 3rd | 3,267 | 3,319 | 3,495 | 3,663 |

Source: https://www.caf.fr/allocataires/aides-et-demarches/droits-et-prestations/vie-personnelle/le-complement-familial-cf

#### Benefit amount
Before 2014 the amount was flat-rate for all qualifying families. Since 1st April 2014:
- Income **below ceiling 2** → **increased amount**.
- Income **between ceiling 1 and ceiling 2** → **standard amount**.

**Table 2.21 CF monthly amount per household in gross from CRDS [2022-2025]** (EUR)

| | 2022 | 2022 (from 1 July)² | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Basic monthly amount | 175.89 | 182.92 | 185.74 | 194.28 | 197.58 |
| Increased monthly amount¹ | 263.85 | 274.39 | 278.62 | 291.44 | 296.39 |

Notes: ¹ Increased monthly amount (after 1st April 2014, for parents whose income is below ceiling 2). ² On 1st July 2022 this amount was increased by 4%.

#### Compatibilities
Compatible with national or regional lump-sum child benefits **except the PAJE** (basic allowance and supplement for free choice of activity): if the household is eligible for PAJE, the CF is not paid. If one of the children receives APL, he has his own home and the household is no longer eligible for CF.

#### Taxation and income testing
Not taxable and not included in the income test of other benefits (**except for activity allowance and RSA**), but subject to **CRDS**.

#### EUROMOD modelling
- Income test based on **current** rather than previous net taxable income.
- Age condition uses the age at the end of the income reference period: children turning 21 during the year are not considered dependent, so partial-year entitlements on account of such children are not simulated.
- The 1 July 2022 increment introduced with the FYA (weighted average before/after 1 July).

---

### 2.5.6. Means-tested disabled benefit — bdi_s — (Allocation aux adultes handicapés, AAH)

#### Definitions
Dependent children: aged under 20 and earning less than 55% of the minimum wage.

#### Eligibility conditions
- Disabled with a permanent disability of **at least 80%**, or a disability **between 50 and 80%** and unemployable (for medical reasons).
- Aged **over 20 and less than 62** (64 for those born from 1st January 1968).
- The income test is carried out using total couple income, including any income of dependent children. **From 1st October 2023, the partner's income is no longer taken into account** in the eligibility conditions ("déconjugalisation") — except if it is less advantageous financially, in which case the resources of the other person are still taken into account when calculating AAH ("conjugalisation"). This reform increases the benefit by an average of about **350 EUR per month** for concerned people.

#### Income test

**Table 2.22 AAH, income threshold [2022-2025]** (annual income, EUR)

| Annual income | 2022 | 2023¹ | 2024 | 2025 |
|---|---|---|---|---|
| Single | 11,038 | 11,656 | 12,193 | 12,399.84 |
| Couple | 19,979 | 21,098 | 22,069 | — |
| For each child | 5,519 | 5,829 | 6,096 | 6,199.92 |

Note: ¹ From 1st October 2023, only the single income threshold is taken into account.

Source: https://caf.fr/allocataires/aides-et-demarches/droits-et-prestations/handicap/l-allocation-aux-adultes-handicapes-aah

- There is a **100% withdrawal rate** if (threshold − benefit) < income < threshold.
- Since **January 2022 and until September 2023**, for AAH recipients living in a couple, a flat-rate deduction applies to the partner's income if the partner is not an AAH recipient: the partner's annual income counted in the income test is reduced by **5,000 EUR**, plus a further **1,400 EUR per dependent child** (deductions applied only to earned income, not to capital income).

**Table 2.23 AAH, income deduction for recipient living in couple [2022-2023]** (yearly amounts, EUR)

| Deduction on partner income (if not AAH recipient) | 2022-2023 |
|---|---|
| For AAH recipient living in couple | 5,000 |
| For each child | 1,400 |

Until September 2023 the partner's income is taken into account; after that, only the beneficiary's income counts for the income threshold.

#### Benefit amount
The benefit is **differential**; the monthly benefit is:

**AAH = (Threshold − Income) / 12**

Income is the monthly net taxable income used for the establishment of the income tax.

**Table 2.24 AAH, monthly maximum benefit amount [2022-2025]** (EUR)

| | 2022 | 2022 (from 1 July)² | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Maximum monthly benefit | 919.86 | 956.65 | 971.37 | 1,016.05 | 1,033.32 |
| Supplement for those disabled for at least one year¹ (with a minimum of 80% incapacity) | 179.31 | 179.31 | 179.31 | 179.31 | 179.31 |

Notes: ¹ This supplement was removed for new requests since **December 1, 2019**; those receiving it before that date continue to receive it for 10 years if they fulfil the conditions (80% incapacity, disabled for at least one year, under 62, receive AAH at full rate, live in independent accommodation). It cannot be implemented in EUROMOD as there is no information on the degree of disability in the data. ² On 1st July 2022 this amount was increased by 4%.

There are additional amounts allowed with an increasing level of disability; all cannot be simulated. The **increase for independent living ("Majoration pour la vie autonome")** is awarded to disabled people receiving AAH at full rate or AAH as a complement to old age or invalidity (i.e. who do not work). Monthly lump sum:

**Table 2.25 AAH, increased amount [2022-2025]** (EUR per month)

| | 2022-2025 |
|---|---|
| Increase for independent living | 104.77 |

Those eligible for both the supplement and the increase for independent living must choose between the two.

#### Compatibilities
Compatible with national or regional lump-sum child benefits **except AEEH** (allowance for disabled children).

#### Taxation and income testing
Not taxable and not included in the income test of other benefits (**except for activity allowance and social assistance (RSA)**). **Not subject to CRDS.**

#### EUROMOD modelling
- No information on the degree of disability exists in the data, so the supplement for those with at least 80% disability is **not modelled**.
- The benefit is simulated for all individuals who fulfil the income criterion and **report themselves as disabled (pl031 = 8)**.
- The income test is simulated on **current** rather than previous taxable income.
- The increase for independent living is simulated for individuals receiving AAH at the full rate, as well as for individuals reporting zero earnings. No other additional amounts are simulated.
- The 1 July 2022 increment is introduced with the FYA: the 2022 benefit amount is a weighted average of the amounts before and after 1 July.

---

## 3. Social minima & activity benefits (CR pages 46-65)

Source: EUROMOD Country Report France (Y16_CR_FR.pdf), PDF pages 46-65 (printed pages 44-63). Covers the tail end of AAH (section 2.5.6), Allocation veuvage AV (2.5.7, bsuwd_s), RSA (2.5.8, bsa00_s), Prime d'activité (2.5.9, bsawk_s), Chèque énergie (2.5.10, bhoey_s), ASPA (2.5.11, bsaoa_s) and the start of Housing Benefits APL/AL (2.5.12, bhotn_s).

---

### 3.0 End of AAH section (Allocation aux Adultes Handicapés — bdidi_s context, printed pp. 44-45)

*(These pages conclude section 2.5.6 on AAH, which starts before page 46.)*

A reduction of 1,400 EUR per dependent child is applied to the partner's annual income (these reductions are applied only to earned income, not to capital income).

**Table 2.23 — AAH, income deduction for recipient living in couple [2022-2023]** (yearly amounts)

| Deduction on partner income (if not AAH recipient) | 2022-2023 |
|---|---|
| For AAH recipient living in couple | 5,000 |
| For each child | 1,400 |

Source: https://caf.fr/allocataires/aides-et-demarches/droits-et-prestations/handicap/l-allocation-aux-adultes-handicapes-aah

Until September 2023, the partner's income is taken into account; it will no longer be the case after — only the beneficiary's income will be taken into account for the income threshold.

**Benefit amount (2.5.6.4).** The benefit is differential; the monthly benefit is:

> AAH = (Threshold − Income) / 12

Income is defined as the monthly net taxable income, used for the establishment of the income tax.

**Table 2.24 — AAH, monthly maximum benefit amount [2022-2025]**

| | 2022 | 2022 (from 1 July)² | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Maximum monthly benefit | 919.86 | 956.65 | 971.37 | 1016.05 | 1033.32 |
| Supplement for those disabled at least 1 year¹ (min. 80% incapacity) | 179.31 | 179.31 | 179.31 | 179.31 | 179.31 |

Notes: ¹ The supplement was removed for new requests since 1 December 2019; prior recipients continue to receive it for 10 years if they fulfil the conditions (80% incapacity, disabled at least one year, under 62, receive AAH at full rate, live in independent accommodation). It cannot be implemented in EUROMOD as there is no information on the degree of disability in the data. ² On 1 July 2022 this amount is increased by 4%.

**Table 2.25 — AAH, increased amount [2022-2025]** ("Majoration pour la vie autonome", monthly lump-sum, awarded to disabled who receive AAH at full rate or AAH as a complement to old age or invalidity, i.e. who do not work)

| | 2022-2025 |
|---|---|
| Increase for independent living | 104.77 |

Those eligible for both the supplement and the increase for independent living must choose between the two benefits.

**Compatibilities (2.5.6.5):** compatible with national or regional lump-sum child benefits except AEEH.

**Taxation and income testing (2.5.6.6):** not taxable and not included in the income test of other benefits (except for activity allowance and social assistance RSA). Not subject to CRDS.

**EUROMOD modelling (2.5.6.7):**
- No information on degree of disability in the data → the supplement for ≥80% disability is not modelled.
- The benefit is simulated for all individuals who fulfil the income criterion and report themselves as being disabled (pl031=8).
- The income test is simulated on current rather than previous taxable income.
- The increase for independent living is simulated for individuals receiving AAH at the full rate, as well as for individuals reporting zero earnings. No other additional amounts are simulated.
- The increment of the benefit from 1 July 2022 is introduced with the FYA extension; the 2022 benefit amount is calculated with a weighted average of amounts before and after 1 July.

---

### 3.1 Allocation veuvage (AV) — Survivor Minimum Pension — bsuwd_s (section 2.5.7)

Means-tested benefit for widows/widowers.

**Eligibility conditions (2.5.7.1):**
- Widow/er not remarried, aged under 55.
- The deceased spouse must have contributed to the old-age insurance at least 3 months during the year preceding the death.
- The pension is paid for 2 years.

**Income test (2.5.7.2):** the monthly widow/er's income for the last 3 months must be below the following ceiling.

**Table 2.26 — AV, monthly widow/er's income ceiling (last 3 months) [2022-2025]**

| | 2022 | 2022 (from 1 Aug)¹ | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Monthly income ceiling | 790.24 | 821.812 | 828.37 | 872.275 | 891.4625 |

Note: ¹ From 1st August. Source: https://www.service-public.gouv.fr/particuliers/vosdroits/F744

Income taken into account: net taxable income of the widow/er (earned income, pensions, unemployment benefit, self-employment and capital income, all in gross terms), excluding family benefits and AAH.

**Benefit amount (2.5.7.3):**

**Table 2.27 — AV, monthly benefit [2022-2025]**

| | 2022 | 2022 (from 1 July)¹ | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Monthly benefit | 632.19 | 657.45 | 662.70 | 697.82 | 713.17 |

Note: ¹ From 1st July. Source: https://www.service-public.gouv.fr/particuliers/vosdroits/F744

**Compatibilities (2.5.7.4):** compatible with national or regional benefits.

**Taxation and income testing (2.5.7.5):** taxable like pension income for personal income tax, but not subject to CRDS and CSG.

**EUROMOD modelling (2.5.7.6):**
- The simulation of this benefit is turned off; the original variable in the dataset is used instead in the baseline.
- No information in the input dataset about the year a person became widowed → if simulated, the benefit is simulated for all widows/widowers who pass the income test.
- The income test is simulated using current rather than past taxable income.
- The 1 July 2022 increment is introduced with the FYA; the 2022 amount is a weighted average of amounts before and after 1 July.

---

### 3.2 RSA — Revenu de Solidarité Active (Solidarity Labour Income) — bsa00_s (section 2.5.8)

Main means-tested social assistance benefit. The RSA aims to ensure a minimum income per month. The benefit amount is the difference between the maximum RSA (lump sum + 62% of net household income from work until 2016, and only lump sum after) and other household resources (including the housing benefit package). Since 2016, this benefit is given only to those out of work or with very low incomes (below the benefit amount). For low-paid workers, the Prime d'activité was introduced. The lump-sum is determined by household composition and the number of dependent children. The RSA is increased for those who meet the previous conditions for means-tested lone parents benefits (API).

**Definitions (2.5.8.1):**
- Dependent children: children under 20. Children over 20 and under 25 living at home may be considered dependent in the RSA sense provided their own income is very low (< 55% of SMIC).
- Since 1 January 2024, the "net social amount" of income has to be declared by those in work to claim the RSA or Activity allowance. The net social amount takes into account income from work and related advantages (lunch vouchers, housing facilities provided by employers, company participations, etc.), which were previously not included in the income declaration.
- RSA is calculated on the basis of the average of the last 3 months' family income.

**Eligibility conditions (2.5.8.2):**
- Be over 25, or under 25 with a dependent child or pregnant, and be aged under 65 (or not entitled to the Minimum Pension for the Elderly).
- Youths 18-25 without children are eligible if they have worked at least two years out of the last three years.
- Income of entitled beneficiaries should not exceed the current benefit limits (implied by the benefit amount calculation).
- From 2023, several regional departments enhanced the support system for RSA recipients (registration with "France Travail", commitment contract with an action plan, condition of "working" at least 15 hours a week — training and integration, not mini-jobs — with certain exemptions). From 2025, this measure has been extended to the whole of France. This is not reflected in EUROMOD (regional coverage, many exemptions, impossible to know which individuals are impacted).

**Benefit amount (2.5.8.3):**

> RSA = (Maximum minimum income based on family characteristics) − (family quarterly income/3 + housing package)

The housing package is a lump-sum subtracted only for people who received the AL.

Family quarterly income (household's quarterly resources) includes:
- the quarterly net taxable income: all working income and related advantages, replacement income (unemployment, ARE, sickness, maternity, invalidity pensions), alimonies, other pensions and income from capital (investment income, savings income and property income), extraordinary income (sale of property, inheritance, gambling winnings);
- all quarterly social minima (AAH), and family benefits (AF, ASF, PAJE and CF only).

**Table 2.28 — RSA, Maximum minimum incomes (MI) and Housing package (HP) lump-sums [2022-2025]** (monthly EUR)

*2022 (until end of June¹) and 2022 from 1 July² (+4%):*

| Family situation | 2022 MI¹ | 2022 HP¹ | 2022 MI² (from 1 July) | 2022 HP² (from 1 July) |
|---|---|---|---|---|
| **Lone parent with children under 3** | | | | |
| Pregnant without child | 739.03 | 69.06 | 768.60 | 71.82 |
| One dependent child | 985.38 | 138.12 | 1024.80 | 143.65 |
| Two dependent children | 1231.72 | 170.93 | 1281.00 | 177.77 |
| Each child after the 2nd | 246.34 | — | 256.19 | — |
| **Single** | | | | |
| Without dependent child | 575.52 | 69.06 | 598.54 | 71.82 |
| One dependent child | 863.28 | 138.12 | 897.81 | 143.65 |
| Two dependent children | 1035.94 | 170.93 | 1077.37 | 177.77 |
| Each child after 2nd | 230.21 | — | 239.42 | — |
| **Couple** | | | | |
| Without dependent child | 863.28 | 138.12 | 897.81 | 143.65 |
| One dependent child | 1035.94 | 170.93 | 1077.37 | 177.77 |
| Two dependent children | 1208.6 | 170.93 | *(not shown in table)* | *(not shown)* |
| Each child after 2nd | 230.21 | — | *(not shown)* | — |

Notes: ¹ Until end of June. ² From July 1st 2022 the value is increased by 4%.

*2023:*

| Family situation | 2023 MI | 2023 HP |
|---|---|---|
| **Lone parent with children under 3** | | |
| Pregnant without child | 780.42 | 72.93 |
| One dependent child | 1040.56 | 145.86 |
| Two dependent children | 1300.70 | 180.50 |
| Each child after the 2nd | 260.14 | — |
| **Single** | | |
| Without dependent child | 607.75 | 72.93 |
| One dependent child | 911.62 | 145.86 |
| Two dependent children | 1093.95 | 180.50 |
| Each child after 2nd | 243.10 | — |
| **Couple** | | |
| Without dependent child | 911.62 | 145.86 |
| One dependent child | 1093.95 | 180.50 |
| Two dependent children | 1276.27 | 180.50 |
| Each child after 2nd | 243.10 | — |

*2024 and 2025:*

| Family situation | 2024 MI | 2024 HP | 2025 MI | 2025 HP |
|---|---|---|---|---|
| **Lone parent with children under 3** | | | | |
| Pregnant without child | 816.32 | 76.28 | 830.21 | 77.58 |
| One dependent child | 1088.43 | 152.57 | 1106.94 | 155.16 |
| Two dependent children | 1360.54 | 188.80 | 1383.68 | 192.02 |
| Each child after the 2nd | 272.10 | — | 276.73 | — |
| **Single** | | | | |
| Without dependent child | 635.70 | 76.28 (12% of RSA MI) | 646.52 | 77.58 (12% of RSA MI) |
| One dependent child | 953.56 | 152.57 (16%) | 969.78 | 155.16 (16%) |
| Two dependent children | 1144.27 | 188.80 (16.5%) | 1163.74 | 192.02 (16.5%) |
| Each child after 2nd | 254.28 | — | 258.61 | — |
| **Couple** | | | | |
| Without dependent child | 953.56 | 152.57 (16%) | 969.78 | 155.16 (16%) |
| One dependent child | 1144.27 | 188.80 (16.5%) | 1163.74 | 192.02 (16.5%) |
| Two dependent children | 1334.98 | 188.80 | 1357.70 | 192.02 |
| Each child after 2nd | 254.28 | — | 258.61 | — |

Source: https://caf.fr/allocataires/aides-et-demarches/droits-et-prestations/vie-professionnelle/le-revenu-de-solidarite-active-rsa

**Table 2.29 — RSA, End of year bonus ("Prime de Noël") [2022-2025]**

| Family situation | 2022-2025 |
|---|---|
| **Single** | |
| Without dependent child or pregnant | 152.45 |
| One dependent child | 228.67 |
| Two dependent children | 274.41 |
| Each child after 2nd | 60.98 |
| **Couple** | |
| Without dependent child | 228.67 |
| One dependent child | 274.41 |
| Two dependent children | 320.14 |
| Each child after 2nd | 60.98 |

Source: https://www.caf.fr/allocataires/caf-du-nord/actualites-departementales/le-versement-de-la-prime-de-noel

The end of year bonus is given once in December to RSA (and ASS) beneficiaries entitled to the RSA (or ASS) in November or December of the current year. Only one bonus is paid per household.

**Compatibilities (2.5.8.4):** compatible with national or regional lump-sum child benefits. It is possible to combine RSA with ASS, but the RSA amount has to be deducted from ASS.

**Taxation and income testing (2.5.8.5):** RSA is not taxable, not included in the income test of other benefits, and not subject to CRDS.

**EUROMOD modelling (2.5.8.6):**
- No benefit is simulated for pregnant women due to lack of information in the data.
- Age at the end of the income reference period is used.
- Lone parents are identified as parents of dependent children without a partner in the dataset.
- Children aged less than 25, earning less than 55% of SMIC and living with other adults are always considered dependent.
- The income test is simulated using current yearly income rather than previous quarterly income; shorter periods of eligibility may be missed.
- When a household receives housing benefits, the lower between the actual benefits and the housing package is deducted.
- The Benefit Take-Up adjustment (BTA) for the RSA is applied to all years and set to "on" as default in the baseline. The non-take-up rate from 2016 to 2024 is 20% (DREES Report 2022: https://drees.solidarites-sante.gouv.fr/sites/default/files/2022-07/Regularly%20measuring%20the%20non-take-up%20of%20the%20RSA%20and%20the%20employment%20bonus%20method%20and%20results.pdf).
- Employment is established based on the presence of yearly earnings: individuals with no earnings throughout the year are considered not working; otherwise in work.
- Starting in 2016, only individuals not in work (or with incomes lower than the benefit amount) are simulated to receive RSA; individuals in work are assumed to receive Prime d'activité.
- Entitlement to the end-of-year bonus is calculated based on annual average incomes and then assigned to approx. 16% of those eligible, to mimic the fact that only families receiving the benefit in November and December would be entitled.
- The 1 July 2022 increment is introduced with the FYA extension; the 2022 benefit amount is a weighted average of amounts before and after 1 July.
- From 2023, the counterpart of 15-20 hours/week of training and integration for RSA recipients is not modelled (regional only, many exemptions, impacted individuals unidentifiable).
- BTA extension is on (baseline adjusts for non-take-up); BCA extension is off (no calibration to external statistics, but the user can activate it). Extensions are toggled in Country Tools/Set Switches. Required inputs:
  - **BTA:** estimated take-up rate set as `$bsa00_BTA_rate` constant; values incorporated for 2006-2024 (DREES Report).
  - **BCA:** aggregate expenditure/benefit recipients filled in the External Statistics table so the calibration rate `$bsa00_BCA_rate` is computed. Data available 2006-2023; for 2024 the 2023 rate is used. For reform modelling, the 2024 system should be used to allow variation in beneficiaries/expenditure (the 2023 share is applied to the new pool of eligible units); with previous systems, totals would stay constant regardless of the reform.

---

### 3.3 Prime d'activité — Activity allowance — bsawk_s (section 2.5.9)

Since 1 January 2016, the Prime d'activité replaced the "RSA activité" and "PPE". It addresses low-income workers (employed or self-employed), is given to families (or single people) with at least one person in work, calculated every 3 months and paid monthly. In January 2019, after large social discontent movements, the bonus amount increased by 90 EUR and earnings limits were increased by between 222€ and 854€ depending on family composition.

**Definitions (2.5.9.1):**
- Children under 20 are dependent children. Children over 20 and under 25 living at home may be considered dependent provided their own income is below 55% of SMIC (for 169 hours/month).
- Since 1 January 2024, the "net social amount" of income must be declared by those in work (income from work plus related advantages previously not declared).

**Eligibility conditions (2.5.9.2):** concerns both employees and self-employed. For the self-employed, turnover is used to determine access; turnover ceilings depend on the type of self-employment.

**Benefit amount (2.5.9.3):**

> Allowance amount = (Maximum minimum income based on family circumstances + 61% family work income + Bonus) − (max(Household's resources; Maximum minimum income) + Housing package)

Important comments:
- Household's resources are disregarded if they exceed the Maximum minimum income lump sums; otherwise the Maximum minimum income lump sums are disregarded.
- If amount < 0, the allowance is set to 0.
- The percentage of income changed in October 2018 (previously 62%). From 1 April 2025, the percentage changed from 61% to 59.85%.

The maximum minimum income is based on the lump sum (gross of CRDS):

**Table 2.30 — Activity allowance, lump sum [2022-2025]**

| | 2022 | 2022 (from 1 July)¹ | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Lump sum | 566.51 | 589.17 | 598.24 | 625.76 | 633.21 |

Note: ¹ On 1 July 2022, updated by 4%. Source: https://www.service-public.gouv.fr/particuliers/vosdroits/F2882

Lump sum increases by household composition:
- +50% for the first additional person;
- +30% for the second additional person;
- +40% per additional person beyond the 3rd person if the household has more than 2 dependent children or persons under 25, except for the person living in couple with the beneficiary.

For lone persons with children or pregnant: the increased amount is 128.412% of the maximum minimum income, plus 42.804% of the maximum minimum income for every child.

Family working income: income from work (wages, bonuses, overtime pay, unemployment benefits and sickness benefits) net of social security contributions (employment and self-employment income before taxes and transfers).

Household's resources are defined as for RSA: all work income, replacement income (unemployment, ARE, sickness, maternity, invalidity pensions), alimonies, other pensions, capital income (investment, savings, property income), extraordinary income (sale of property, inheritance, gambling winnings) and social minima or family benefits (AAH, APL, ALS, AF, CLCA/PreParE, PAJE base and CF are included). PAJE PN, CMG and ARS are NOT taken into account. Since 2018, disability pensions, pensions for accident at work and pensions for occupational diseases are not taken into account either. The last 3 months are used to calculate the activity allowance.

**Table 2.31 — Activity allowance, housing package [2022-2025]** (monthly EUR)

| | 2022 | 2022 (from 1 July)¹ | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Single person | 69.06 | 70.35 | 71.43 | 74.72 | 75.99 |
| Lone parent with 1 child | 138.12 | 140.69 | 142.86 | 149.43 | 151.97 |
| Lone parent with 2+ children | 170.93 | 174.11 | 176.79 | 184.92 | 188.06 |
| Couple with no children | 138.12 | 140.69 | 142.86 | 149.43 | 151.97 |
| Couple with 1 or more children | 170.93 | 174.11 | 176.79 | 184.92 | 188.06 |

Note: ¹ On 1 July 2022, this value is increased. Source: https://www.caf.fr/professionnels/offres-et-services/accompagnement-des-allocataires/bareme-prime-d-activite

The housing package is a percentage of the activity allowance lump sum net of CRDS: 12% for single, 16% for lone parent with a child, 16.5% for lone parent with 2+ children. Example for 2025 (gross lump sum 633.21€):
- single: HP = 12% × 633.21 = 75.99€
- lone parent with 1 child: HP = 16% × (633.21 × (1 + 50%)) = 151.97€
- lone parent with 2+ children: HP = 16.5% × (633.21 × (1 + 80%)) = 188.06€

**Bonus for activity allowance:**
- Each family member who works can benefit from the bonus; the amount is capped for each worker. The individual bonus depends on individual work income; paid if individual work income is between 0.5 and 1.4 SMIC in 2018, 0.5 to 1.5 SMIC since 2019 (based on net SMIC).
- Monthly work income < 0.5 SMIC (= 59 × hourly gross SMIC): bonus = 0.
- Monthly work income over 120 × hourly gross SMIC: bonus fixed and capped at:
  - 12.782% of the lump sum (net of CRDS) until 2018;
  - 29.101% of the lump sum (net of CRDS) since 2019 — 2022: 164.04€ net / 164.86€ gross; 2023: 173.22€ net / 174.09€ gross; 2024: 181.19€ net / 182.10€ gross; "2024: 183.35€ net/" *(as printed in the report — the second "2024" is evidently a typo for 2025; gross value left blank in the PDF)*.
- Bonus variable but below the cap for monthly work income between 59 and 120 × hourly gross SMIC (income bounds: 2022: 623.63€/1268.40€; 2023: 664.93€/1352.40€; 2024: 687.38€/1398€; 2025: 696.20€/1416€), or between 59 and 95 gross hourly SMIC before 2019.
- Since 2019 the bonus formula is:

> Bonus = (0.29101 × lump sum) × (1 − ((120 × hourly gross SMIC) − work income) / (120 × hourly gross SMIC − 59 × hourly gross SMIC))

- The allowance is paid from age 18. For students, interns and apprentices, income from work must be over 1104.25€ in 2025 (78% of net SMIC for 35 hours).
- The allowance is not taken into account in income for the calculation of income tax and is not paid for amounts below 15€.

**Taxation and income testing (2.5.9.4):** not taxable and not included in the income test of other benefits, but subject to CRDS.

**EUROMOD modelling (2.5.9.5):**
- Simulated for all individuals who fulfil the income test and are observed to have positive earnings.
- Earnings are calculated over the year → the model may overestimate PA receipt and underestimate RSA receipt. The earnings limit to qualify is likewise calculated using annual earnings.
- No information about self-employed turnover in the dataset → specific self-employed eligibility conditions are not simulated; the self-employed are assumed eligible if their net profit satisfies the same conditionality as employees.
- The bonus amount is calculated using annual work income.
- The variable is not disaggregated in the UDB but simulated since 2019 in EUROMOD. From 2020, the variable is disaggregated in EMSD.
- The 1 July 2022 lump-sum increment is introduced with the FYA extension (weighted average of amounts before/after 1 July).
- References cited: https://drees.solidarites-sante.gouv.fr/publications/les-dossiers-de-la-drees/le-non-recours-aux-prestations-sociales-mise-en-perspective and https://www.senat.fr/rap/a19-143-7/a19-143-77.html
- BTA extension is on (baseline adjusts for non-take-up); BCA extension is off. Required inputs:
  - **BTA:** take-up rate set as `$bsawk_BTA_rate`; 73% at the end of 2016, 57% in 2017, 80% since 2018 onwards (source: https://www.caf.fr/nous-connaitre/l-e-ssentiel).
  - **BCA:** aggregate expenditure in the External Statistics table for the calibration rate `$bsawk_BCA_rate`; data available 2016-2023; for 2024 the 2023 rate is used. For reforms, use the 2024 system to allow variation in beneficiaries/expenditure.

---

### 3.4 Chèque énergie — Energy bonus — bhoey_s (section 2.5.10)

From 2018, this bonus replaces the gas and electricity social prices granted to low-income households. It is a voucher sent directly to beneficiaries without any administrative action, used to pay part of the energy bill (given to the energy supplier). The bonus is given once in March-April each year; in 2025 the bonus will be given in the autumn.

**Eligibility conditions (2.5.10.1):** persons with limited resources who filed an income tax return. The bonus is granted according to household composition and the "Revenu Fiscal de Référence" (RFR, see section 2.6 Personal income tax). Household members are counted as consumption units (CU).

**Table 2.32 — Energy bonus, Consumption unit [2022-2025]**

| | 2022-2025 |
|---|---|
| First person of the household | 1 |
| Second person of the household | + 0.5 |
| Each supplementary person | + 0.3 |

**Table 2.33 — Energy bonus, income ceilings [2022-2025]**

| | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Maximum RFR by consumption unit | 10,800 | 11,000 | 11,000 | 11,000 |

Source: https://www.economie.gouv.fr/particuliers/gerer-mon-argent/comment-beneficier-du-cheque-energie#

Example: a couple with 2 children must not exceed an RFR of 23,100€ in 2024 (2.1 × 11,000 = 23,100).

**Benefit amount (2.5.10.2):** based on household composition and RFR.

**Table 2.34 — Energy bonus amounts [2022-2025]** (EUR per year)

*2022:*

| | (RFR/CU) < 5600€ | 5600€ ≤ (RFR/CU) < 6700€ | 6700€ ≤ (RFR/CU) < 7700€ | 7700€ ≤ (RFR/CU) < 10700€ (10800€ in 2021-2022) |
|---|---|---|---|---|
| 1 CU (1 person) | 194 | 146 | 98 | 48 |
| 1 < CU < 2 (2 or 3 people) | 240 | 176 | 113 | 63 |
| ≥ 2 CU (4 people or more) | 277 | 202 | 126 | 76 |

*2023-2025:*

| | (RFR/CU) < 5700€ | 5700€ ≤ (RFR/CU) < 6800€ | 6800€ ≤ (RFR/CU) < 7850€ | 7850€ ≤ (RFR/CU) < 11000€ |
|---|---|---|---|---|
| 1 CU (1 person) | 194 | 146 | 98 | 48 |
| 1 < CU < 2 (2 or 3 people) | 240 | 176 | 113 | 63 |
| ≥ 2 CU (4 people or more) | 277 | 202 | 126 | 76 |

Note: CU = Consumption Unit. Source: https://www.economie.gouv.fr/particuliers/gerer-mon-argent/comment-beneficier-du-cheque-energie#

**Additional Energy Voucher:**
- In 2022, an exceptional energy voucher of 100€ to 200€ paid to 40% of the most modest households from December 2022:
  - 200€ for households whose reference tax income per consumption unit is strictly less than 10,800€;
  - 100€ for households whose reference tax income per consumption unit is between 10,800€ and 17,400€.
- In 2023, several exceptional vouchers given to eligible households only upon application:
  - Wood-energy voucher for households with RFR < 27,500€, on presentation of an invoice for wood or pellet purchase: for pellets 200€ if RFR < 14,400, 100€ if 14,400 < RFR < 27,500; for logs 100€ if RFR < 14,400, 50€ if 14,400 < RFR < 27,500.
  - A petrol allowance of 100€ for the most modest households under resource conditions (RFR < 14,700€ for 1 part of RFR), only upon application.
- The Additional Energy Voucher has not been renewed in 2024 and 2025.

**Compatibilities (2.5.10.3):** compatible with national or regional benefits.

**Taxation and income testing (2.5.10.4):** not taxable, not included in the income test of other benefits, not subject to CRDS.

**EUROMOD modelling (2.5.10.5):**
- Simulated in EUROMOD since 2018; no information on actual use of the voucher, but all eligible beneficiaries are assumed to use it.
- Additional energy vouchers are simulated in 2021 and 2022 but not in 2023 because of lack of information on wood consumption and kind of transport used. The 2023 Additional Energy vouchers cannot be implemented because EU-SILC has no data on wood consumption or transport used by eligible low-income earners to commute to work.

---

### 3.5 ASPA — Allocation de solidarité aux personnes âgées (Solidarity allowance for the elderly) — bsaoa_s (section 2.5.11)

**Eligibility conditions (2.5.11.1):** persons aged 65 and over with limited resources and retired (not working).

**Benefit amount (2.5.11.2):** the benefit is differential at the level of the couple:

> ASPA = Monthly Maximum amount − Quarterly Family income / 3

If the amount calculated is < 0, the amount is set to 0.

Family quarterly income does not include family benefits or housing benefits (i.e. quarterly net taxable income + AAH) and concerns only the beneficiary's and his/her partner's income.

**Table 2.35 — ASPA, monthly maximum income [2022-2025]**

| | 2022 | 2022 (from 1 July)² | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Single | 916.78 | 953.45 | 961.08 | 1012.02 | 1034.28 |
| Couple¹ | 1423.31 | 1480.24 | 1492.08 | 1571.16 | 1605.73 |

Notes: ¹ The couple amount is applied if at least one person is aged 65 or over. ² On 1 July 2022 this value is updated by 4%. Source: https://www.economie.gouv.fr/particuliers/preparer-ma-retraite-et-ma-succession/comment-fonctionne-le-minimum-vieillesse-ou#

**Compatibilities (2.5.11.3):** compatible with national or regional benefits.

**Taxation and income testing (2.5.11.4):** not taxable, not included in the income test of other benefits, not subject to CRDS.

**EUROMOD modelling (2.5.11.5):**
- Eligibility is restricted to individuals reporting receipt in the data. While full simulation is technically possible, it results in substantial overestimation of both the number of recipients and the amounts.
- The income test uses current yearly income rather than previous quarterly income.
- The age condition uses age at the end of the income reference period → a full year of benefits is simulated for individuals turning 65 during the reference period who in reality would have been entitled only during part of the year.
- The 1 July 2022 increment is introduced with the FYA (weighted average of amounts before/after 1 July).

---

### 3.6 Housing Benefits — bhotn_s — (Allocation Logement, APL and AL) (section 2.5.12, start)

**Definitions (2.5.12.1):**
- Children are dependent persons if aged under 20 and earning less than 55% of the minimum wage (based on 169h/month).
- Dependent persons: all dependent children and disabled close family members (parents, grandparents, sisters, brothers…) or parents and grandparents over 65 living in the household who earn less than 55% of the minimum wage.
- Unit of assessment: the entire household.

**Eligibility conditions (2.5.12.2):**
- Be a renter of subsidized housing, sub-renter or first-time buyer.
- Since July 2016, if the real rent paid is over a threshold, the benefit is suppressed; if the rent is over a determined ceiling but under a maximum threshold, the benefit is decreased.
- Since October 2016, the value of assets is taken into account in the allowance calculation when higher than 30,000 EUR: real estate assets (excluding the main residence and properties for occupational use), financial assets and movable assets.
- Beneficiaries dependent on a household subject to wealth tax or tax on real estate wealth are not entitled.
- A reform, initially planned for 2019 but taking place on 1 January 2021 due to covid-19, changed the income reference period to the previous 12 months, with eligibility conditions checked every 3 months.

**Benefit amount (2.5.12.3):** the general formula (same for APL and AL):

> **Equation 1:** AL or APL = L + C − Pp − Mfo

- L: real rent up to the limit of a certain ceiling
- C: lump-sum charge
- Pp: minimal personal participation
- Mfo: lump sum voted each year

The system presented is the general system for the rental sector (specificities for residential homes "Logement-foyer", roommates or specific loans are not covered).

**1. Real Rent (L):** taken into account up to a monthly ceiling depending on the number of dependent persons and geographical zone. Children older than 20 are not dependent persons but their incomes are included in assessed household income.

**Table 2.36 — Housing benefits, rent taken into account in calculation [2022-2025]** (monthly EUR)

*October 2021 to June 2022:*

| | Zone I | Zone II | Zone III |
|---|---|---|---|
| Single | 298.07 | 259.78 | 243.48 |
| Couple without dependent person | 359.49 | 317.97 | 295.15 |
| Lone parent/couple with one dependent person | 406.30 | 357.80 | 330.94 |
| Lone parent/couple with two dependent people | 465.25 | 409.88 | 378.37 |
| Increase for each dependent person | 58.95 | 52.08 | 47.43 |

Note: on 1 July 2022, these values are updated in advance to compensate inflation by 3.5%. The usual annual increase occurs from October 2023, +3.5%.

*July 2022 to September 2023, and October 2023 to September 2024:*

| | Jul 2022-Sep 2023 Zone I | Zone II | Zone III | Oct 2023-Sep 2024 Zone I | Zone II | Zone III |
|---|---|---|---|---|---|---|
| Single | 308.50 | 268.87 | 252.00 | 319.30 | 278.28 | 260.82 |
| Couple without dependent person | 372.07 | 329.10 | 305.48 | 385.09 | 340.60 | 316.17 |
| Lone parent/couple with one dependent person | 420.52 | 370.32 | 342.52 | 435.24 | 383.28 | 354.51 |
| Lone parent/couple with two dependent people | 481.54 | 424.22 | 391.61 | 498.39 | 439.07 | 405.32 |
| Increase for each dependent person | 61.01 | 53.90 | 49.09 | 63.15 | 55.79 | 50.81 |

Source: https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000046206217

Geographical zones:
- Zone I: Paris and region "Ile de France"
- Zone II: cities with more than 100,000 inhabitants and Corsica
- Zone III: all other cities

Since July 2016, real rent paid is used to determine if the benefit is abolished. It depends on the geographic zone and the previous L amount which integrates family composition. If the rent actually paid is above C1 but under C2, the allowance is decreased; if rent paid is above C2, the benefit is abolished.

**Table 2.37 — Housing benefits, decrease parameters [2022-2025]**

| Zone | C1 | C2 | E.g. in July 2025 for Single |
|---|---|---|---|
| Zone I | > 3.4 L | ≥ 4 L | (between 1132.676€ and 1332.56€) |
| Zone II | > 2.5 L | ≥ 3.1 L | (between 725.85€ and 900.054€) |
| Zone III | > 2.5 L | ≥ 3.1 L | (between 680.3€ and 843.572€) |

Note: the increases for each dependent person are also multiplied by the corresponding coefficient. Source: https://www.legifrance.gouv.fr/loda/id/LEGISCTA000039160679

If the rent actually paid is between C1 and C2, the decreasing rate applied to the allowance amount is:

> **Equation 2:** α = (rent paid − C1) / (C2 − C1)

with α = 0 when rent paid ≥ C2 (then APL = 0); α = 1 when rent paid = C1; 0 < α < 1 when rent paid is between C1 and C2.

*(Note: as printed in the report; given Equation 3 below, α acts as the reduction factor with new APL = APL × (1 − α).)*

If and only if the rent actually paid is between C1 and C2, the allowance amount is:

> **Equation 3:** new APL = APL × (1 − α)

**2. Lump-sum charge (C):** monthly amount depending on the number of dependent persons.

**Table 2.38 — Housing benefits, lump-sum charge [2022-2025]** (monthly EUR)

| | 2022 | 2022¹-2023 | 2023²-2024 | 2024²-2025 | 2025² |
|---|---|---|---|---|---|
| Single person/couple without dependent person | 54.22 | 56.12 | 58.08 | 59.97 | 60.59 |
| Single person/couple with one dependent person | 66.51 | 68.84 | 71.25 | 73.57 | 74.33 |
| Increase for each dependent person | 12.29 | 12.72 | 13.17 | 13.60 | 13.74 |

Notes: ¹ From July 2022, increase by 3.5%. ² From October. Source: https://www.legifrance.gouv.fr/loda/id/JORFTEXT000039160329

**3. Minimal personal participation (Pp):**

> **Equation 4:** Pp = P0 + Tp × Rp

- P0: minimal participation
- Tp: personal participation rate
- Rp: resources

P0 minimal participation:

> **Equation 5:** P0 = Max(P0forf, [8.5% × (L + C)])

**Table 2.39 — Housing benefits, minimal participation [2022-2025]**

| | 2022 | 2022¹-2023 | 2023²-2024 | 2024²-2025 | 2025² |
|---|---|---|---|---|---|
| P0forf (€ per month) | 35.39 | 36.63 | 37.91 | 39.15 | 39.56 |

Notes: ¹ From July 2022, increase by 3.5%. ² From October.

*(Section 2.5.12 continues beyond PDF page 65 with the personal participation rate Tp, resources Rp and the Mfo lump sum.)*

---

# EUROMOD Country Report France (Y16, 2022-2025)

## 4. Housing benefit, unemployment & leave benefits (CR pages 65-84)

---

### 4.1 Housing benefits APL/AL — bhotn_s (continued: formula parameters) [CR section 2.5.12, pages 65-69]

Continuation of the housing benefit (Aide personnalisée au logement, APL / Allocation logement, AL — EUROMOD variable `bhotn_s`) formula components. The benefit formula uses eligible rent (L), a lump-sum charge (C) and a minimal personal participation (Pp).

#### 2. Lump-sum charge (C)

Monthly amount depends on the number of dependent persons.

**Table 2.38 Housing benefits, lump-sum charge [2022-2025]** (EUR/month)

| | 2022 | 2022¹-2023 | 2023²-2024 | 2024²-2025 | 2025² |
|---|---|---|---|---|---|
| Single person/couple without dependent person | 54.22 | 56.12 | 58.08 | 59.97 | 60.59 |
| Single person/couple with one dependent person | 66.51 | 68.84 | 71.25 | 73.57 | 74.33 |
| Increase for each dependent person | 12.29 | 12.72 | 13.17 | 13.60 | 13.74 |

Notes: ¹ From July 2022, increase by 3.5 %. ² From October.
Source: https://www.legifrance.gouv.fr/loda/id/JORFTEXT000039160329

#### 3. Minimal personal participation (Pp)

**Equation 4 — Minimal personal participation:**

```
Pp = P0 + Tp * Rp
```

- P0: minimal participation
- Tp: personal participation rate
- Rp: resources

**P0 — minimal participation floor (Equation 5):**

```
P0 = Max(P0forf, 8.5 % * (L + C))
```

**Table 2.39 Housing benefits, minimal participation [2022-2025]**

| | 2022 | 2022¹-2023 | 2023²-2024 | 2024²-2025 | 2025² |
|---|---|---|---|---|---|
| P0forf (EUR per month) | 35.39 | 36.63 | 37.91 | 39.15 | 39.56 |

Notes: ¹ From July 2022, increase by 3.5 %. ² From October.
Source: https://www.legifrance.gouv.fr/loda/id/LEGISCTA000039160679

**Tp — personal participation rate:**

```
Tp = Tf + Tl
```

**Table 2.40 Housing benefits, parameter Tf [2022-2025]**

| Family situation | 2022-2025 |
|---|---|
| Single | 2.83 % |
| Couple without dependents | 3.15 % |
| Lone parent/couple with one dependent person | 2.70 % |
| Lone parent/couple with two dependent persons | 2.38 % |
| Lone parent/couple with three dependent persons | 2.01 % |
| Lone parent/couple with four dependent persons | 1.85 % |
| Lone parent/couple with five dependent persons | 1.79 % |
| Increase for each dependent person | -0.06 % |

Source: https://www.legifrance.gouv.fr/loda/id/LEGISCTA000039160679

**Tl — rent component (Equation 6, rent-to-baseline ratio RL):**

```
RL = L / Rent Baseline
```

**Table 2.41 Housing benefits, Rent Baseline [2022-2025]** (EUR/month)

| | 2022 | 2022¹-2023 | 2023²-2024 | 2024²-2025 | 2025² |
|---|---|---|---|---|---|
| Single | 259.78 | 268.87 | 278.28 | 287.35 | 290.34 |
| Couple without dependent | 317.97 | 329.10 | 340.62 | 351.72 | 355.38 |
| Lone parent/couple with one dependent | 357.80 | 370.32 | 383.28 | 395.77 | 399.89 |
| Lone parent/couple with two dependents | 409.88 | 424.22 | 439.07 | 453.38 | 458.10 |
| Increase for each dependent | 52.08 | 53.90 | 55.79 | 57.61 | 58.21 |

Notes: ¹ From July 2022, increase by 3.5 %. ² From October.
Source: https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000046206217

**Table 2.42 Housing benefits, Tl as function of RL [2022-2025]**

| RL | Tl |
|---|---|
| 0-45 % | 0 % |
| 45-75 % | 0.45 % * (RL - 45 %) |
| > 75 % | 0.45 % * 30 % + 0.68 % * (RL - 75 %) |

Source: https://www.legifrance.gouv.fr/loda/id/LEGISCTA000039160679

**Rp — Resources:**

Rp is the difference between the household's resources (income of 2 years before until 2020; the 12 previous months since January 2021, incorporating assets values) and a lump-sum R0. Household resources = the "Revenu Brut global" used in the income tax.

**Table 2.43 Housing benefits, R0 parameter [2022-2025]** (yearly amounts, EUR)

| | 2022 | 2022¹ | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Single | 4683 | 4870 | 4949 | 5186 | 5235 |
| Couple without dependent person | 6709 | 6977 | 7090 | 7430 | 7501 |
| Lone parent/couple with one dependent person | 8002 | 8322 | 8456 | 8862 | 8947 |
| Lone parent/couple with two dependent persons | 8182 | 8509 | 8646 | 9061 | 9148 |
| Increase for each dependent child | 311 | 323 | 328 | 343 | 346 |

Note: ¹ From July 2022, increase by 4 %.
Source: https://www.service-public.gouv.fr/particuliers/actualites/A17979

#### 4. Lump sum reduction (Mfo)

Since October 2017, the AL amount is reduced by a lump sum voted each year; since October (2017) this amount is 5 euros. Also since October 2017, the minimum payment goes from EUR 15 to EUR 10 for AL, and 0 for APL.

#### RLS — «Réduction du loyer de solidarité» (NOT computed in EUROMOD)

Introduced February 2018: a decrease of housing benefit APL for tenants with low incomes living in social housing, fully compensated by an equivalent reduction in the monthly rent. Only people eligible for RLS are entitled to a decrease in housing benefit; the rent reduction is linked to the APL decrease.

Eligibility:
- must rent social housing (except sheltered house and overseas housing);
- must respect the following resource ceilings.

**Table 2.44 Housing benefits, monthly resources ceilings for RLS [2022-2025]** (EUR/month)

| | 2022-2023 Zone I | Zone II | Zone III | 2024-25 Zone I | Zone II | Zone III |
|---|---|---|---|---|---|---|
| Single | 915 | 854 | 828 | 959 | 895 | 868 |
| Couple without dependent person | 1102 | 1042 | 1008 | 1155 | 1092 | 1056 |
| Lone parent/couple with one dependent person | 1403 | 1329 | 1289 | 1470 | 1393 | 1351 |
| Lone parent/couple with two dependent people | 1669 | 1583 | 1536 | 1749 | 1659 | 1610 |
| Lone parent/couple with three dependent people | 2043 | 1943 | 1877 | 2141 | 2036 | 1967 |
| Lone parent/couple with four dependent people | 2357 | 2243 | 2169 | 2470 | 2351 | 2273 |
| Lone parent/couple with five dependent people | 2624 | 2497 | 2411 | 2750 | 2617 | 2527 |
| Lone parent/couple with six dependent people | 2905 | 2764 | 2671 | 3045 | 2897 | 2799 |
| Increase for each dependent person | 283 | 266 | 247 | 297 | 279 | 259 |

Sources: https://www.anil.org/aj-reduction-loyer-solidarite-rls-apl/ ; https://www.legifrance.gouv.fr/loda/id/JORFTEXT000044560604/2023-05-17/

The RLS amount is updated each January; the maximum ceiling is indexed to the rent reference index (IRL).

**Table 2.45 Housing benefits, RLS monthly rent decreases for social housing [2022-2023]** (EUR/month, by geographical zone)

| | 01/2022-09/2022 I | II | III | 10/2022-12/2022 I | II | III | 2023 I | II | III | Oct 2023 I | II | III |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Single | 50.95 | 44.60 | 41.76 | 52.97 | 46.59 | 43.56 | 52.16 | 45.66 | 42.76 | 54.51 | 48.22 | 45.08 |
| Couple without dependent person | 61.53 | 54.49 | 50.59 | 63.82 | 56.71 | 52.67 | 63 | 55.79 | 51.80 | 66.05 | 58.71 | 54.51 |
| Lone parent/couple with one dependent person | 69.48 | 61.04 | 56.64 | 71.92 | 62.81 | 58.75 | 71.14 | 62.50 | 57.99 | 74.43 | 65.00 | 60.80 |
| Increase for each dependent person | 10.00 | 8.88 | 8.03 | 10.13 | 9.12 | 8.11 | 10.24 | 9.09 | 8.22 | 10.48 | 9.44 | 8.39 |

**RLS monthly rent decreases, gross of CRDS [2024-2025]** (EUR/month, by geographical zone)

| | 2024 I | II | III | Oct 2024 I | II | III | 2025¹ I | II | III | 2025² I | II | III |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Single | 55.2 | 48.45 | 45.36 | 59.14 | 52.31 | 48.91 | 55.48 | 48.69 | 45.59 | 36.89 | 35 | 32.77 |
| Couple without dependent person | 66.73 | 59.15 | 54.92 | 71.66 | 63.69 | 59.14 | 67.06 | 59.45 | 55.20 | 48.22 | 42.74 | 39.68 |
| Lone parent/couple with one dependent person | 75.31 | 66.06 | 61.42 | 80.75 | 70.52 | 65.96 | 75.79 | 66.39 | 61.73 | 54.41 | 47.73 | 44.38 |
| Increase for each dependent person | 10.78 | 9.60 | 8.65 | 11.37 | 10.24 | 9.10 | 10.52 | 9.65 | 8.69 | 7.79 | 6.93 | 6.25 |

Notes: ¹ From 2025 onwards it was planned that the amount would be revalued each 1 January in line with the IRL (official rent index, https://www.insee.fr/fr/statistiques/serie/001515333). ² But in June 2025 a new modification was made.
Source: https://www.service-public.gouv.fr/particuliers/actualites/A15236

Additional RLS rules:
- Persons living at the same address but not part of the household can each benefit from the rent reduction if their income does not exceed the ceilings, but within the limit of 75 % of the reduction.
- The amount of the APL decrease for eligible beneficiaries is set to 98 % of RLS since 2018 (rate fixed each year, varies from 90 % to 98 %).
- The rent reduction only applies to the poorest families benefiting from APL; the decrease in APL is fully offset by the reduction in rent, so gains generated are minimal.

#### 2.5.12.4 Compatibilities
Compatible with national or regional benefits.

#### 2.5.12.5 Taxation and income testing
Not taxable and not included in the income test of other benefits (except for activity allowance and RSA), but subjected to CRDS.

#### 2.5.12.6 EUROMOD modelling (housing benefit)
- Only the general benefit for tenants paying rent is simulated.
- Benefits for home owners/tenants in free accommodation are not simulated (absence of required information in the dataset). Due to lack of information on social housing, the February 2018 RLS reform is not simulated in EUROMOD.
- The three zones on which the benefit depends are imputed based on geographical region (db040) and population density (db100).
- The income used in the income test is yearly rather than quarterly. Rent paid is calculated using a monthly average of rent paid throughout the entire year.
- The 2019 change in the income reference period has no impact on EUROMOD simulations because EUROMOD uses the income of the same year when simulating entitlement.
- The 1 July 2022 amount increment is introduced with the FYA (full-year adjustment): a weighted average considering the benefit amounts before and after 1 July.

---

### 4.2 Unemployment insurance benefit — bunct_s (Allocation de retour à l'emploi, ARE) [CR section 2.5.13, pages 68-73]

#### 2.5.13.1 Eligibility conditions
- Since November 2019: at least 6 months worked over the previous 24 months (36 months for employees aged 53+) at termination of the employment contract; must not have left the job voluntarily; must be actively looking for work. Due to the Covid-19 crisis, the 6-month period was exceptionally reduced to 4 months from August 2020 to November 2021.
- Under conditions, voluntary quitters can benefit (approved professional project + 5 years worked during the last 60 months).
- Self-employed: separate benefit ATI (Allocation des Travailleurs Indépendants) — EUR 800/month during 6 months if previous income of the last 2 years exceeds EUR 10 000/year and the company is in legal redress. Voluntary quitters and self-employed are NOT simulated in EUROMOD (no information on beneficiaries in EU-SILC).
- Before November 2019: at least 4 months worked over the previous 28 months (or 36 months for employees 53+); no benefit for voluntary quitters or self-employed.

**October/December 2021 reform (SJR calculation):** From 1 October 2021, the daily reference wage (SJR) takes into account non-worked days: no longer based on days worked in the last 12 months, but on average monthly income including days worked AND periods of inactivity — i.e. total calendar days between the first day of the first work contract and the last day of the last work contract, excluding days of illness, maternity/paternity and work accident, during the last 24 months for under-53s (36 months otherwise). Jobseekers with split work patterns are more likely to see a benefit reduction. An Unédic impact study (April 2021) estimated a 17 % average drop in daily benefit in the first year for 1.15 million recipients, with longer compensation time (14 months average vs 11). A decree of 30 March 2021 introduced a floor: the benefit cannot decrease more than 43 % relative to the old calculation (obtained by capping non-worked days counted at 75 % of days worked); 365 000 of the 1.15 million recipients benefit from this floor.

**Dégressivité (regressivity) trigger:** For jobseekers under 57 (reform not applied at 57+) with gross income above EUR 4500/month (4518 in 2022, 4766 in 2023, 4857.81 in 2024, 4915.33 in 2025), the benefit is reduced by 30 % from the 7th month of unemployment; this started 1 December 2021 after several postponements. From 1 April 2025, the 30 % reduction from the 7th month no longer applies to jobseekers aged 55 and over (instead of 57 previously).

#### 2.5.13.2 Income test
No income test. The benefit amount depends on the salary earned during the last 12 months.

#### 2.5.13.3 Benefit amount

Based on the gross daily reference wage (Salaire journalier de référence, SJR):

- **Until September 2021:** `SJR = sum of gross earned income during the last 12 months before the last day worked / (365 - days of absence or without a contract (= number of worked days (capped at 261) * 1.4))`
- **From October 2021:** `SJR = sum of gross earned income during the last 24 months (36 for 53+) before the last day worked / (731 - days of illness, paternity/maternity or work accident)` — or 1096 for 53+. If the new method reduces the SJR, the reduction is capped at 43 % of the SJR under the previous method.

Amount rules:
- Benefit = 40.4 % of SJR + fixed allocation (EUR 13.11 per day in 2025).
- Floor: minimum benefit (31.97 * RF euros/day in 2025); ceiling: 75 % of SJR.
- Since 1 July 2014, the benefit is the higher of (40.4 % SJR + fixed allocation) and (57 % of SJR); overall the amount lies between 57 % and 75 % of SJR.
- Part-time workers: reduction factor `RF = (number of hours worked in part-time work) / (legal number of hours)`.
- Dégressivité: since 1 November 2019 (effectively applied from 1 December 2021, so the first 30 % reduction appears in benefit amounts of July 2022), people under 57 with gross wage above EUR 4500/month (4545 in 2022, 4766 in 2023, 4857.81 in 2024, 4915.33 in 2025) get a 30 % reduction from the 7th month of unemployment, with a minimum threshold of EUR 2261 net/month (2679 in 2023, 2730 in 2024, 2763 in 2025).

**Table 2.46 ARE parameters [2022-2025]** (EUR/day; amounts at 30 June — increased each 1 July since July 2011)

| Parameters | 2022 | 2022¹ | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Fixed allocation | 12.12*RF | 12.47*RF | 12.71*RF | 12.95*RF | 13.11*RF |
| Minimum benefit | 29.56*RF | 30.42*RF | 31*RF | 31.59*RF | 31.97*RF |

Note: ¹ From July 2022, increase by 2.9 %.
Source: https://travail-emploi.gouv.fr/lallocation-daide-au-retour-lemploi-are

Monthly benefit = daily benefit * number of days in the month (since April 2025, fixed at 30 days each month).

#### Duration rules
- Base rule: "one day worked, one day of compensation"; duration = days worked * 1.4 (converts days worked, 5/week, into days of allowance, 7/week).
- 2009 to October 2019: eligibility 4 months worked in the last 28 months (88 days or 610 hours) for under-53s, last 36 months for over-53s; registered at the employment office. Maximum duration depended on age (at end of work contract) and days worked, from 4 to 36 months.
- Since November 2019: 130 days (6 months) or 910 hours worked during the last 24 months for under-53s (36 months for 53+). Maximum duration: 24 months for <53; 30 months for 53-54; 36 months for 55+.
- August 2020 to November 2021: eligibility exceptionally reduced to 4 months (Covid-19); back to 6 months from December 2021.
- Since February 2023: duration reduced by 25 %, except those with only 6 months of duration before the reform (6 months = minimum duration threshold). At the end of the benefit period, jobseekers may be entitled to an end-of-right supplement extending the benefit period (by the same duration as the 25 % deducted) if the labour market deteriorates: unemployment rate above 9 %, or increase of the unemployment rate by 0.8 % in one quarter.
- Since 1 April 2025: maximum duration changed for 53-54 year olds (548 calendar days instead of 685, i.e. 18 months instead of 22.5) and for 55-56 (685 calendar days instead of 822, i.e. 22.5 months instead of 27). With the 25 % end-of-right supplement in bad labour-market circumstances: 53-54 → total max 24 months (18 + 6, i.e. 730 days = 548 + 182); 55-56 → total max 30 months (22.5 + 7.5, i.e. 913 days = 685 + 228); 57+ → total max 36 months (27 + 9, i.e. 1095 days = 822 + 273).

#### 2.5.13.4 Taxation and income testing
Taxable and included in the income test of other benefits; subjected to CRDS and CSG.

**Table 2.47 Characteristics of the unemployment insurance benefit [2019-2025]**

| | November 2019 - January 2023 | February 2023 - March 2025 | From April 2025 |
|---|---|---|---|
| Eligibility - contribution period | <53: 6 months in the last 24; ≥53: 6 months in the last 36 months immediately preceding unemployment | Same rules | Same rules |
| Other conditions | Reduced to 4 months from August 2020 to November 2021 (Covid crisis) | - | - |
| Self-employed | 800 EUR/month during 6 months under conditions¹ | Same rules | Same rules |
| Workers who quit | Resignation deemed legitimate by administration² | Same rules | Same rules |
| Contribution base | Gross earning | Gross earning | Gross earning |
| Basic amount | 40.4 % of gross daily reference wage + fixed allocation | Same rules | Same rules |
| Floor | 29.56/day³ (2022) | 31/day (2023), 31.59/day (2024) | 31.97/day (2025) |
| Ceiling | Maximum 75 % of the gross daily reference wage | idem | idem |
| Regressivity | Gross wages >4766 EUR in 2023 (4545 until June 2022, 4677 until end of 2022), and under 57: up to 30 % less than the initial allocation from the 7th month of unemployment (after 182 days = 6 months; 8 months from July 2021 except if unemployment situation is better at that date)⁴ | Gross wages >4766 EUR in 2023 (4857.81 in 2024); same rules | Gross wages >4915.33 and under 55 |
| Duration (standard) | days worked * 1.4, min 182 calendar days, max 730 calendar days for <53 (913 for 53-54, 1095 for 55+) | Demands after 1 February 2023: duration reduced by 25 % with minimum threshold of 6 months (182 calendar days). Max 548 calendar days (685 for 53-54, 822 for ≥55) | Same conditions for demands after 1 April 2025 except max duration: 548 calendar days for 53-54, 685 for 55-56, 822 for 57+ |
| Special cases | Part-time: part-time rate applied (rate = nb hours/35, applied to the 31.59 EUR in 2024, 31.97 EUR in 2025, and to the fixed allocation); the maximum depends on the same full-time calculation | idem | idem |
| Subject to taxes | Yes | Yes | Yes |
| Subject to SIC | Yes (3 % for retirement) | Yes (3 % for retirement) | Yes (3 % for retirement) |

Notes:
1. Self-employed: must have been in the same company for 2 years; the company must be in reorganization or liquidation; the 2 previous years' annual turnover must be at least EUR 10 000; the applicant's income must be less than RSA at the time of the request; must prove serious job search.
2. Resignation legitimate if objective reasons justify it (follow partner or parents to another region, after a marriage, in case of domestic violence, or if the applicant left for another job and lost it within 65 days of recruitment). In other resignation cases, the benefit can be obtained after 4 months (121 days) of unemployment (4 months not compensated) if eligibility conditions are fulfilled and there is serious, active job search. Since November 2019, resigners may also access the benefit to build another professional project (project must be accepted by administration before resignation).
3. Amount increased to 30.42 in July 2022.
4. This part of the reform was temporarily suspended until December 2021; for eligible people the degressivity starts in fact from July 2022, after 182 days of unemployment.

**Dégressivité thresholds (from page 73 note 4):**
- From June 2022, those whose daily allowance is higher than EUR 149.5/day (156.70 in 2023, 159.68 in 2024, 161.6 in 2025) are eligible for degressivity.
- After application of the 30 % degressivity, the minimum daily allocation cannot be less than EUR 87.65/day (89.32 in 2023, 91.02 in 2024, 92.11 in 2025), i.e. EUR 2666 of allowance per month (2679 in 2023, 2730 in 2024, 2763 in 2025).
- From June 2022, for gross wages > EUR 4677 (4518 in 2020, 4545 until June 2022, 4677 from August 2022, 4766 in 2023, 4857.1 in 2024, 4915.33 in 2025) and under 57 (55 from April 2025): up to 30 % less than the initial allocation from the 7th month of unemployment (after 182 days = 6 months; 8 months from July 2021 except if the unemployment situation in France is better at that date).

Source: https://www.unedic.org/l-assurance-chomage-et-vous/demandeur-d-emploi-ou-salarie/mon-indemnisation/pendant-combien-de-temps-vais-je-toucher-mes-allocations-chomage

#### 2.5.13.5 EUROMOD modelling (ARE)
- No information in the dataset on contribution history; simulated eligibility approximates to a large extent observed receipt in the data.
- Age condition simulated using age at the end of the income reference period; individuals who turned 65 during the period (possibly entitled for part of the year) are considered ineligible.
- Previous earnings imputed from the observed amount of the received benefit by inverting the benefit rules.
- Full-time vs part-time difference not simulated (hours worked in the previous year not observable); all entitled individuals assumed to have worked full time.
- If the upper limit (75 % of SJR) is lower than the minimum benefit, the upper limit is enforced (assumption: such a situation may arise only for part-time workers for whom the minimum benefit is over-simulated).
- Duration simulated assuming the same number of months worked each year as in the current year; duration of receipt simulated to be at least the number of months in receipt observed in the data.
- New rules on the computation period (in force since October 2021) cannot be implemented due to lack of relevant information in the input data.
- The 1 July 2022 increment is introduced with the FYA (weighted average of amounts before and after 1 July).

---

### 4.3 Unemployment assistance — bunmt_s (Allocation de solidarité spécifique, ASS) [CR section 2.5.14, pages 73-76]

#### 2.5.14.1 Eligibility conditions
People who have exhausted their rights to unemployment insurance, employed at least 5 years during the last 10 years, aged under 62 (from 2023, depending on whether the applicant has a sufficient number of quarters to claim a full-rate pension but has not reached the minimum age), able to work and actively looking for a job.

#### 2.5.14.2 Income test
Income taken into account: the couple's net taxable income (RNI), excluding the unemployment benefit previously earned, family allowance and housing benefits, but including the ASS itself. Monthly income = sum of eligible income of the 12 months before the month of the demand, divided by 12.

**Table 2.48 ASS income limit**

| Monthly income | Differential rate |
|---|---|
| Single | 70 times the daily amount |
| Couple | 110 times the daily amount |

**Table 2.49 ASS, threshold for full rate**

| Monthly income | Full rate |
|---|---|
| Single | Under 40 times the daily amount |
| Couple | Under 80 times the daily amount |

Source: https://www.francetravail.fr/candidat/mes-droits-aux-aides-et-allocati/aides-financieres-et-autres-allo/autres-allocations/lallocation-de-solidarite-specif.html

#### 2.5.14.3 Benefit amount

**Table 2.50 ASS daily benefit amount [2022-2025]** (EUR/day)

| | 2022 | 2022* | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Daily amount | 17.21 | 17.90 | 18.17 | 19 | 19.33 |

(* from July 2022)

- Monthly amount = daily amount * 30.
- If the couple's income is below the full rate threshold (40 * daily amount for a single, 80 * for a couple): monthly benefit = daily amount * 30 (full rate).
- If the couple's income is above the full-rate threshold: `benefit = 30 * daily amount - (couple's income - full rate threshold)` (differential rate).

#### 2.5.14.4 Compatibilities
Not compatible with unemployment insurance benefit ARE and RSA; compatible with AAH before 2017 (not after, for new requests; those who received both allowances before January 2017 may, under eligibility conditions, combine the two allowances for 10 years).

#### 2.5.14.5 Taxation and income testing
Taxable, but NOT subjected to CRDS and CSG. Included in the income test of other benefits.

Simulation assumption (footnote 2): ASS is taxable and at the same time its income test depends on taxes. To deal with this circularity, taxes (including income tax and CRDS) are calculated using the data variable and not the simulated variable; the simulated variable is calculated after taxes are computed.

**Table 2.51 ASS, characteristics of the unemployment assistance [2022-2025]**

| | 2022-2025 |
|---|---|
| Contribution period | n/a |
| Other conditions | Employed at least 5 years in the last 10 years; under 62 years old (for those who have all the quarters to receive a full pension); looking for a job; exhausted unemployment insurance |
| Eligibility of self-employed | No |
| Contribution base | Net taxable income (couple) |
| Basic amount | 16.91/day in 2021; 17.21/day in 2022; 18.17/day in 2023; 19/day in 2024; 19.33/day in 2025 |
| Additional amount | - |
| Floor | n/a |
| Ceiling | Below full-rate threshold (40x daily amount single / 80x couple): daily amount * 30. Above the threshold: 30 * daily amount - (household's income - full rate threshold) |
| Duration (standard) | 6 months, renewable as long as the beneficiary fulfils the eligibility conditions |
| Subject to taxes | Yes |
| Subject to SIC | No |

(Note: the PDF prints "16.91/day in 20021" — i.e. 2021.)
Sources: francetravail.fr (see above); https://www.service-public.gouv.fr/particuliers/vosdroits/F12484

#### ASS — End of year bonus
Given once in December to ASS beneficiaries entitled to ASS in November or December of the current year. In 2023, single parents with one or more children who receive ASS receive a 35 % bonus on their allowance. The increased amount for dependent children is available only on request from "France Travail".

**Table 2.52 ASS — End of year bonus [2022-2025]** (EUR)

| End of year bonus | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Fixed amount | 152.45 | 152.45 | 152.45 | 152.45 |
| On request only in 2023 — lone parents: | | | | |
| - One dependent child | | 205.81 | | |
| - Two dependent children | | 232.49 | | |
| - Three dependent children | | 248.49 | | |
| - Four dependent children | | 269.84 | | |
| - Each child after 2nd | | 21.34 | | |

Source: https://www.francetravail.fr/candidat/mes-droits-aux-aides-et-allocati/aides-financieres-et-autres-allo/aide-exceptionnelle-de-fin-danne.html

#### 2.5.14.6 EUROMOD modelling (ASS)
- No detailed contribution history in the data: the "5 years worked in the last 10" condition is approximated by checking that the individual has worked at least 5 years throughout his entire work career.
- All potential recipients assumed to be actively looking for work.
- Exhaustion of ARE checked by comparing months in unemployment with the imputed/simulated number of months receiving ARE.
- Income test simulated based on current yearly income; due to time-period mismatch, the simulated benefit does not approximate well observed receipt in the data.
- Incompatibilities with RSA are not simulated; instead, ASS is included in the income test of RSA.
- The 1 July 2022 increment is introduced with the FYA (weighted average of amounts before and after 1 July).

---

### 4.4 Sickness benefit and parental leave [CR section 2.5.15, pages 76-84]

#### 2.5.15.1 Definitions
The parental leave ("congé maternité", "congé paternité", "congé adoption") and the sickness benefit ("congé maladie") are replacement income provided by the Primary Health Insurance (CPAM) for employees. In case of sick leave, maternity, paternity or adoption leave, the employee receives daily social security benefits. The parental leave and the sickness benefit are subject to almost the same conditions of grant. For the three types of parental leave, the duration changes depending on the number of children in the household and the number of children expected or adopted. The benefit is paid fortnightly in arrears; it depends on previous salaries and the number of days of leave; the first payment is received after 14 days.

#### 2.5.15.2 Sickness benefit (bhl)

##### Eligibility
Employees receive daily social security allowances if they fulfil conditions varying with duration of inactivity and contributions.

If out of work for **less than 6 months**:
- have worked at least 150 hours in the 3 calendar months or 90 days prior to the inactivity; OR have contributed on a salary equal to at least 1015 times the hourly SMIC during the 6 calendar months preceding the inactivity;
- or, failing that (seasonal or intermittent activity): at least 600 hours worked or contributions on a salary of at least 2030 times the hourly SMIC, during the 12 calendar months or 365 days before the beginning of the inactivity.

If inactivity is **longer than 6 months** (long-term inactivity): registered at least 12 months as socially insured at the date of the beginning of the inactivity; AND at least 600 hours worked in the 12 calendar months or 365 days prior to the inactivity, or contributions on a salary of at least 2030 times the hourly SMIC during the 12 calendar months preceding the inactivity.

##### Benefit amount
- Daily allowance = half of the daily wage of the last 3 months (last 12 months for seasonal or intermittent activity). Daily wage = total of the last 3 gross wages / 91.25 (accounts for Sundays and holidays in paid benefits).
- Remunerations counted only up to a ceiling of **1.8 times the SMIC**: maximum amount in January 2022 was EUR 47.43 = (1603.15 * 1.8 * 50 %) / 30.42; 50.58 in 2023; 52.28 in 2024. **From April 2025 the ceiling changed to 1.4 SMIC**, so the maximum amount is EUR 41.47 = (1801.80 * 1.4 * 50 %) / 30.42.
- From July 2020, the advantage from the 31st day of absence from work for employees with at least 3 dependent children is cancelled.
- The employee may also be entitled to additional compensation paid by the employer or maintenance of the salary (collective agreements).
- Jobseekers: daily allowance calculated using the last 3 wages received, rather than the unemployment benefits.
- Covid-19 measures: workers who could not telework or who had to take care of children under 16 during lockdowns could get sickness benefit from 1 to 21 days (until 1 May), then had to resort to partial unemployment.

**Table 2.53 SMIC amounts [2022-2025]** (EUR, gross)

| Year | Gross hourly SMIC | Gross monthly SMIC (151.67 h¹) | Gross monthly SMIC (169 h) | Gross annual SMIC (151.67 h¹) | Gross annual SMIC (169 h) | Date of entry in force |
|---|---|---|---|---|---|---|
| 2022 | 10.57 | 1603.15 | 1786.33 | 19237.82 | 21435.96 | 01/01/2022 |
| 2022 | 10.85 | 1645.58 | 1833.67 | 19746.96 | 22004.04 | 01/05/2022 |
| 2022 | 11.07 | 1678.95 | 1870.83 | 20147.40 | 22449.96 | 01/08/2022 |
| 2023 | 11.27 | 1709.28 | 1904.63 | 20511.85 | 22855.56 | 01/01/2023 |
| 2023 | 11.52 | 1747.20 | 1946.88 | 20966.40 | 23362.56 | 01/05/2023 |
| 2024 | 11.65 | 1766.92 | 1968.85 | 21203.04 | 23626.20 | 01/01/2024 |
| 2024 | 11.88 | 1801.80 | 2007.72 | 21621.60 | 24092.64 | 01/11/2024 |

Note: ¹ Legal working time.
Source: https://www.insee.fr/fr/statistiques/1375188 and own elaboration for 169 hours of work.

**Table 2.54 Sickness benefit, amounts [2022-2025]** (EUR)

| | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Minimum monthly amount of disability pension, sickness/maternity/paternity benefit | 292.89 (9.66/day) | 310.47 (10.24/day) | 310.47 (10.24/day) | 334.12 (11.02/day) |
| Maximum daily amount for sickness benefit | 47.43 | 50.58 | 52.28 | 41.47 |
| Maximum amount for sickness benefit for employees with at least 3 children, from the 31st day of sickness | 63.23 | 67.47 | | |
| Maximum amount for maternity/paternity/adoption leave | 89.03 | 95.22 | 100.36 | 101.94 |

Source: https://www.service-public.gouv.fr/particuliers/vosdroits/F3053

##### Duration
- Waiting period of three days: daily allowances paid from the 4th day of sick leave in the private sector, from the 2nd day in the public sector. The waiting period applies to each period of inactivity, except recognized long-term illness.
- Except in recognized cases of long-term illness, no more than 360 daily allowances over a period of three years. Maximum payment duration increased to three years for long-term/chronic illnesses. Any resumption of work of one year or more restarts a new maximum three-year compensation period. Beyond three years, employees may be eligible for a disability pension.

##### EUROMOD modelling (sickness benefit)
Due to lack of information on sickness (number of days of sickness) and on previous contribution history, the sickness benefit is NOT simulated in EUROMOD but included in the microdata (variable bhl taken from data).

#### 2.5.15.3 Maternity leave (bmact_s)

##### Eligibility
Not subject to any conditions on seniority in the company or nature of the contract. Being pregnant confers entitlement if the employee has been insured for 10 months on the presumed date of delivery. Must also satisfy the two conditions mentioned for sickness benefit for being out of work less than 6 months (the date taken into account is the beginning of pregnancy or prenatal leave). Footnote: the pregnant woman must inform her employer generally at the beginning of the second trimester (medical certificate + letter with presumed delivery date and leave dates); an employee cannot be dismissed during maternity leave (breach of contract possible only for serious misconduct or impossibility to maintain the contract for reasons unrelated to maternity, and even then not notified during the leave).

##### Duration
Minimum duration calculated in weeks; breaks down into a prenatal and a postnatal period:
- First pregnancy or birth of a second child: 16 weeks total — 6 weeks before delivery, 10 weeks after.
- From the third child: 26 weeks total — 8 weeks before delivery, 18 weeks after.
- Twins: 34 weeks — 12 weeks before, 22 weeks after.
- Triplets or more: 46 weeks — 24 weeks before, 22 weeks after.

Extensions: in case of premature birth, untaken prenatal leave days extend postnatal leave accordingly. Illness related to pregnancy/childbirth: up to +2 weeks prenatal and up to +4 weeks postnatal. If the mother dies while on maternity leave (e.g. during delivery), the father's employment contract may be suspended for 10 weeks from the child's birth.

##### Benefit amount
Same rules as sick leave except for the maximum amount (see Table 2.54): calculation of the ceiling is **(PSS * 79 %) / 30.42** (PSS = social security ceiling / plafond de la sécurité sociale). Daily social security benefits paid; the company's collective agreement may provide full maintenance of salary.

#### 2.5.15.4 Paternity leave (bpact_s)

##### Eligibility
Applies not only to employees but also to jobseekers, trainees in vocational training, non-salaried workers (agricultural or non-agricultural), and the liberal professions. Footnote: from the birth of the child, the salaried father benefits from a protection period of 10 weeks from birth (whether or not he takes the leave): he can only be dismissed for serious misconduct independent of the birth or for economic reasons.

##### Duration
- 11 consecutive calendar days (including non-worked days: Saturdays, Sundays, holidays); optional for the father. **Since 1 July 2021: increased to 25 days.**
- Twins or triplets: 18 days instead of 11 (**32 days since 1 July 2021**).
- Must be taken within four months after the birth (the departure date counts; the leave can end after the 4-month period).
- Employee must notify the employer at least one month in advance of departure and return dates (can be before the birth). The employer cannot refuse unless the one-month notice was not respected. After the birth, the employee must send a complete copy of the birth certificate or a copy of the family record book to his health insurance to receive the daily allowances. The employment contract is suspended during the leave.
- In addition, the father is entitled to a birth holiday of three days — a new father can take 14 consecutive days of absence combining both leaves (or 21 days for twins); the paternity leave need not follow the 3-day birth holiday.

##### Amount
Employees on paternity leave are paid by social security, not the employer. Conditions of payment of daily allowances by CPAM are the same as for maternity leave (max daily amount per Table 2.54: 89.03 in 2022, 95.22 in 2023, 100.36 in 2024, 101.94 in 2025).

#### 2.5.15.5 Adoption leave

##### Eligibility
An employee who adopts a child is entitled to a compensated adoption leave of varying duration (depending on number of children adopted and number of children already dependent). It can be taken by one parent or divided between the two employed parents. Open to any employee entrusted with a child by: the child welfare service (ASE); the French Agency for Adoption (AFA); a French agency authorized for adoption; or by decision of the competent foreign authority, provided the child has been authorized to enter France. (Footnote: adoption in France requires a certificate from the departmental adoption services indicating the beginning of the adaptation period or a certificate of placement; adoption abroad requires a photocopy of the child's passport or other official document with the visa issued by the Intercountry Adoption Mission (IAM).)

##### Duration

**Table 2.55 Adoption leave, duration**

| Number of adopted children | Number of already dependent children in the household | Before July 2021 — one parent takes the leave | Before July 2021 — both parents take the leave | After July 2021 — one parent takes the leave | After July 2021 — both parents take the leave |
|---|---|---|---|---|---|
| 1 | 0 or 1 | 10 weeks | 10 weeks + 11 days | 16 weeks | 16 weeks + 25 days |
| 1 | 2 or more | 18 weeks | 18 weeks + 11 days | 18 weeks | 18 weeks + 25 days |
| 2 or more | Whatever | 22 weeks | 22 weeks + 18 days | 22 weeks | 22 weeks + 32 days |

Source: https://travail-emploi.gouv.fr/le-conge-dadoption#anchor-navigation-566

- When divided between the two parents, the leave can only be divided into two periods, the shortest of which is at least 11 days (25 since July 2021) — or 18/32 days (in 2023) in the case of multiple adoptions. The two periods can follow each other or be taken simultaneously.
- The leave begins on the date of arrival of the child in the home; it can start earlier, within the limit of 7 consecutive days preceding the arrival. Notification by registered letter with acknowledgment of receipt (or delivery against receipt), stating the reason for absence and the end date of the contract suspension. The employer cannot refuse. Unless a contractual/collective agreement provides otherwise, no time limit is imposed on the employee to warn the employer.

##### Amount
During adoption leave, any adoptive parent is entitled to daily rest allowances if he/she complies with the 3 previous conditions of the maternity leave (the date taken into account is the date of arrival of the child in the home).

##### Taxation and income testing (parental leave benefits)
- Note: bchcc_s (supplement for free choice of activity) is not compatible with paid holidays, maternity/paternity/adoption leave, sick leave or unemployment benefit — this must be accounted for when modelling bchcc_s.
- Taxable and included in the income test of other benefits; subjected to CRDS and CSG.

##### EUROMOD modelling (adoption leave)
This benefit (adoption leave) is not simulated in EUROMOD due to lack of information about adoption in the data.

---

# EUROMOD Country Report France (Y16, systems 2022-2025)

## 5. Social insurance contributions (CR pages 84-98)

Source: EUROMOD Country Report FR, section 2.6 "Social insurance contributions" (document pages 83-97, PDF pages 85-99).

### 5.0 Overview of French social security regimes

Discrepancies exist in regimes of social security depending on the employment status of individuals and sometimes on the sector they work in. There are 4 main social systems in France:

- The general regime ("régime général") for employees
- The regime for the self-employed (travailleur non salarié, TNS) run by independent groups (RAM)
- The agricultural system managed by Mutuelle Sociale Agricole (MSA)
- The local Alsace-Moselle plan
- Some more specific schemes (SNCF, EDF…)

The "régime général" covers employees against the financial consequences of different risks (illness, accident) or situations (family, old age, widowhood). These systems are financed by contributions from both employees and employers (sometimes either one or the other) on wages and related income.

---

### 5.1 Employee social contributions — **tscee_s**

Employee social contributions mainly finance the Social Security system (Sécurité Sociale). Types of contributions paid by employees on their whole gross income:

- Employee contributions for health insurance and widowhood
- Employee contributions for old age
- Employee contributions for unemployment insurance

#### Liability to contributions

All employees pay social contributions, but there are exemptions or rate reductions for certain contributions to help employment:

- For entrepreneurship when they invest in disadvantaged areas or were unemployed or were employed and create or take over a business.
- For hiring an employee with low income or in a disadvantaged area, or for young innovative enterprises.
- For the employment of young people or unemployed people who have particular employment contracts like "Contrat d'apprentissage", "Contrat de professionnalisation" or "Contrat d'accompagnement dans l'emploi".
- For the employment of home help for the elderly or disabled, or child custody.
- Since 2019, overtime pay is exempted from income tax (up to 5,000 € before 2022, 7,500 € after) and from employee SIC contributions (but limited to 11.31% on old age, complementary pension and CEG, which corresponds to the rate for income group 1/A).

#### Income base

The tax base depends on the gross income and on the type of contribution. Some contributions are taxed on whole income, others are capped (only part of the income is taxed). The ceiling depends on the **monthly social security ceiling (PMSS)**; depending on the contribution, the ceiling is multiplied by 1, 3, 4 or 8. The income considered is gross income on the payroll for all jobs, part-time or full-time, occasional or not.

**Table 2.56 — Employee social contribution, monthly ceilings (EUR/month) [2022-2025]**

| Income group | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Income group A | 0 to 3,428 | 0 to 3,666 | 0 to 3,864 | 0 to 3,925 |
| Income group B | 3,428 to 13,712 | 3,666 to 14,664 | 3,864 to 15,456 | 3,925 to 15,700 |
| Income group C | 13,712 to 27,424 | 14,664 to 29,328 | 15,456 to 30,912 | 15,700 to 31,400 |
| Income group 1 | 0 to 3,428 | 0 to 3,666 | 0 to 3,864 | 0 to 3,925 |
| Income group 2 | 3,428 to 10,284 | 3,666 to 10,998 | 3,864 to 11,592 | 3,925 to 11,775 |

Source: https://www.cci.fr/actualites/les-charges-sociales-au-1er-janvier-2025

Remark (2025 values): 3,925 = 1 × monthly PSS; 15,700 = 4 × monthly PSS; 31,400 = 8 × monthly PSS; 11,775 = 3 × monthly PSS.
(Implied monthly PSS/PMSS: 2022 = 3,428 €; 2023 = 3,666 €; 2024 = 3,864 €; 2025 = 3,925 €.)

Since 2019, income groups were renamed: group A became Tranche 1 (less than 1 × PSS), Groups B and C became Tranche 2 (between 1 and 8 × PSS) and Tranche 3 (> 8 × PSS).

#### Contribution rates

**Table 2.57 — Employee social contribution, rates [2022-2025]**

| Contribution | Base | Rate 2022-2025 |
|---|---|---|
| Sickness | Whole income | 0 % |
| Old age | Income group A | 6.90 % |
| Old age | Whole income | 0.40 % |
| Complementary pension for non-white collars | Income group 1 | 3.15 % |
| Complementary pension for non-white collars | Income group 2 | 8.64 % |
| Complementary pension for white collars | Income group A | 3.15 % |
| Complementary pension for white collars | Income group B | 8.64 % |
| Complementary pension for white collars | Income group C | 8.64 % |
| AGFF (Old age), CEG (general equilibrium contribution) | Income group 1/A | 0.86 % |
| AGFF (Old age), CEG (general equilibrium contribution) | Income group 2/B | 1.08 % |
| Unemployment insurance | Income group A/B | 0 % |
| White collar (APEC) | Income group A+B | 0.024 % |
| Outstanding contribution (CET) | Income group A/B/C | 0.14 % |

Source: https://www.cci.fr/actualites/les-charges-sociales-au-1er-janvier-2025

#### EUROMOD modelling (tscee_s)

There is not enough information in the dataset to identify to which specific contribution regime an individual contributes; only the "régime général" is simulated for all employees. The simulation takes into account the number of months an individual worked during the income reference period, but not variation in earnings throughout the year. White collar workers are approximated based on occupation (senior officials and managers, and professionals). No exemption from contributions, with the exception of overtime pay, or entitlement to lower rates is simulated due to absence of information in the micro-data. Complementary pensions for white-collar employees are simulated assuming the employer/employee split of contributions on Income Group C is similar to that on Income Group B (in practice, part of this split is subject to firm-level negotiations).

---

### 5.2 Employer social contributions — **tscer_s**

Like employees, employers are liable for social contributions on medical insurance, pensions, unemployment insurance and additional contributions such as family contributions and housing. Since 1 January 2016, employers must provide a mutual company insurance ("mutuelle d'entreprise") to their employees; the employer pays half of the contributions and the employee the other half, to provide all employees a minimal social coverage in addition to social security.

#### Liability and income base

Definitions (liability, income groups) are the same as for employee social contributions. The income base refers to gross employment income.

#### Contribution rates

**Table 2.58 — Employer social contributions, rates [2022-2025]**

| Contribution | Base | 2022-2023 | 2024 | 2025 |
|---|---|---|---|---|
| Sickness ¹ | Income > 2.5 SMIC | 13 % | 13 % | — |
| Sickness ¹ | Income > 2.25 SMIC | — | — | 13 % |
| Sickness ¹ | Income ≤ 2.5 SMIC | 7 % | 7 % | — |
| Sickness ¹ | Income ≤ 2.25 SMIC | — | — | 7 % |
| Family benefits ¹ | Whole income for income > 3.5 SMIC | 5.25 % | 5.25 % | — |
| Family benefits ¹ | Whole income for income > 3.3 SMIC | — | — | 5.25 % |
| Family benefits ¹ | Income ≤ 3.5 SMIC | 3.45 % | 3.45 % | — |
| Family benefits ¹ | Income ≤ 3.3 SMIC | — | — | 3.45 % |
| Housing — FNAL, firms with less than 50 employees ² | Income group A | 0.10 % | 0.10 % | 0.10 % |
| Housing — FNAL, firms with more than 50 employees ² | Whole income | 0.50 % | 0.50 % | 0.50 % |
| Old age ¹ | Income group A | 8.55 % | 8.55 % | 8.55 % |
| Old age ¹ | Whole income | 1.90 % | 2.02 % | 2.02 % |
| CSA (autonomy solidarity) ² | Whole income | 0.30 % | 0.30 % | 0.30 % |
| Complementary pension non-white collars (AGIRC-ARRCO) ³ | Income group 1 | 4.72 % | 4.72 % | 4.72 % |
| Complementary pension non-white collars (AGIRC-ARRCO) ³ | Income group 2 | 12.95 % | 12.95 % | 12.95 % |
| Complementary pension white collars (AGIRC-ARRCO) ³ | Income group A | 4.72 % | 4.72 % | 4.72 % |
| Complementary pension white collars (AGIRC-ARRCO) ³ | Income group B | 12.95 % | 12.95 % | 12.95 % |
| Complementary pension white collars (AGIRC-ARRCO) ³ | Income group C | 12.95 % | 12.95 % | 12.95 % |
| AGFF (old age) (CEG) ³ | Income group A/1 | 1.29 % | 1.29 % | 1.29 % |
| AGFF (old age) (CEG) ³ | Income group B/2 | 1.62 % | 1.62 % | 1.62 % |
| White collars contingency | Income group A | 1.50 % | 1.50 % | 1.50 % |
| Unemployment insurance ³ | Income group A+B | 4.05 % | 4.05 % | 4.05 % (4.00 % from May) |
| Wage guarantee fund (AGS) | Income group A+B | 0.15 % | 0.20 % | 0.25 % |
| Agency for management employment (APEC) | Income group A+B | 0.036 % | 0.036 % | 0.036 % |
| Outstanding contribution (CET), white collars only | Income group A/B/C | 0.21 % | 0.21 % | 0.21 % |
| Professional training — less than 10 employees | Whole income | 0.55 % | 0.55 % | 0.55 % |
| Professional training — 10-19 employees | Whole income | 1 % | 1 % | 1 % |
| Professional training — more than 19 employees | Whole income | 1 % | 1 % | 1 % |
| Apprenticeship tax | Whole income | 0.68 % | 0.68 % | 0.68 % |
| Participation in the construction effort (more than 20 employees in 2019, 50 after) | Whole income | 0.45 % | 0.45 % | 0.45 % |
| Contribution to professional and unions organizations | Whole income | 0.016 % | 0.016 % | 0.016 % |

Notes:
- ¹ subject to "Réduction Fillon"
- ² subject to "Réduction Fillon" since 2015
- ³ since 2019
- For family benefits, 5.25 % is the standard rate. Since 2015, for incomes below 3.5 SMIC, the reduced rate of 3.45 % is applied, but for those with incomes above 3.5 SMIC, 5.25 % is applied on the whole income (and not 3.45 % up to 3.5 SMIC and 5.25 % above); the same method is applied for sickness. From January 2025, the income ceiling has been reduced to 3.3 SMIC for family benefits and to 2.25 SMIC for sickness.

Source: https://www.cci.fr/actualites/les-charges-sociales-au-1er-janvier-2025

#### Reductions in employers' social security contributions ("Réduction générale des cotisations patronales" since 2020, called "Réduction Fillon" before)

Since 2003, a general reduction on employer contributions paid for low-income employees exists ("Réduction Fillon"). The reduction is decreasing and varies with the level of the employee's income; the coefficient is maximum at the minimum wage (SMIC). It applies to all employees whose income is less than **1.6 SMIC**, whatever the form or nature of the employment contract and working hours, the amount being maximum for employees paid at the minimum wage. It applies for each calendar year, for each employee.

History and scope:

- The reduction was amended in 2015. Since 2011, the reduction is calculated on the **yearly** income (before, on monthly income); annual income includes bonuses such as the 13th month (before, bonuses were not included). In 2012, overtime was included in the yearly income (excluded before). From 2015, there are, under certain conditions, no employer contributions for sickness, maternity, pension, invalidity and death for employees with low earnings.
- Contributions affected by the "Réduction Fillon": sickness, family benefits, and old age. Since 1 January 2015: also housing (FNAL), solidarity autonomy (CSA), and occupational diseases and work accident (rate varies by company).
- Since 2019, the tax credit for competitiveness and employment ("Crédit d'impôt pour la compétitivité et l'emploi", CICE) was removed and replaced by a reduction in employer social contribution rates. Since January 2019, complementary pension (AGIRC-ARRCO only up to 4.72 %) and AGFF-CEG (only up to 1.29 %) contributions are also included in the general reduction (6.01 pts for 1 SMIC). Since October 2019, the unemployment contribution is included too (at the rate 4.05 %).
- The reduction concerns private companies who pay unemployment insurance and must hold salary negotiations each year (for companies with more than 50 employees where there are trade-union representatives). It only concerns work contracts that do not qualify for other social security exemptions (cumulating exemptions is generally not possible: e.g. standard deduction of employer contributions for overtime, exemption for employees of home help).
- The reduction amount is the product of the yearly gross income by a coefficient that changes with the number of company employees at 31 December.
- The reduction is calculated on an annual basis, but applied in advance: each month on contributions paid (based on the monthly SMIC and monthly remuneration) and regularized if necessary (e.g. if monthly pay varies during the year, when there are bonuses). Regularization is made in December for monthly employers, in the 4th quarter for quarterly employers; if the contract ends during the year, the regularization applies to the last month or quarter due.
- The reduction is calculated per employee, and its amount cannot be superior to contributions due.
- Since 2020, the amount of the reduction calculated after application of the specific deduction for professional expenses ("déduction forfaitaire spécifique") is capped at **130 %** of the amount of the reduction calculated without application of the deduction.
- Since 2022, the general reduction also concerns contributions due for accidents at work and occupational diseases up to a limit of **0.59 %** of remuneration (0.55 % in 2023 and 2025, 0.49 % in 2024). The rate of this employer contribution is not indicated in the rates table because it depends on the work done and on the activity sector; due to lack of information in SILC, this contribution is not implemented.

**Table 2.59 — Reduction applied on employer contributions [2022-2025]**

| Contribution | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Sickness | yes | yes | yes | yes |
| Housing/FNAL | yes | yes | yes | yes |
| Family benefits | yes | yes | yes | yes |
| CSA | yes | yes | yes | yes |
| Pension | yes | yes | yes | yes |
| Complementary pension | yes | yes | yes | yes |
| Unemployment | yes | yes | yes | yes |
| Accident at work/occupational diseases | yes (up to 0.59 %) | yes (up to 0.55 %) | yes (up to 0.49 %) | yes (up to 0.59 %) |

Source: own elaboration (CR).
(Note: the accident-at-work caps in Table 2.59 read 0.59 % in 2022 and 2025, 0.55 % in 2023, 0.49 % in 2024; the body text says 0.59 % in 2022, 0.55 % in 2023 and 2025, 0.49 % in 2024.)

**Table 2.60 — Fillon coefficient, companies with less than 50 employees (Income ≤ 1.6 SMIC)**

| Year | Coefficient formula | Cap on coefficient (T) |
|---|---|---|
| 2022 | = (0.3195/0.6) × [(1.6 × (SMIC gross annual amount / gross annual income subject to social security contributions)) − 1] | 0.3195 |
| 2023 | = (0.3191/0.6) × [(1.6 × (SMIC gross annual amount / gross annual income subject to social security contributions)) − 1] | 0.3191 |
| 2024 | = (0.3194/0.6) × [(1.6 × (SMIC gross annual amount / gross annual income subject to social security contributions)) − 1] | 0.3194 |
| 2025 | = (0.3193/0.6) × [(1.6 × (SMIC gross annual amount / gross annual income subject to social security contributions)) − 1] | 0.3193 |

**Table 2.61 — Fillon coefficient, companies with 50 employees and more (Income ≤ 1.6 SMIC)**

| Year | Coefficient formula | Cap on coefficient (T) |
|---|---|---|
| 2022 | = (0.3235/0.6) × [(1.6 × (SMIC gross annual amount / gross annual income subject to social security contributions)) − 1] | 0.3235 |
| 2023 | = (0.3231/0.6) × [(1.6 × (SMIC gross annual amount / gross annual income subject to social security contributions)) − 1] | 0.3231 |
| 2024 | = (0.3234/0.6) × [(1.6 × (SMIC gross annual amount / gross annual income subject to social security contributions)) − 1] | 0.3234 |
| 2025 | = (0.3233/0.6) × [(1.6 × (SMIC gross annual amount / gross annual income subject to social security contributions)) − 1] | 0.3233 |

Source (both tables): https://www.economie.gouv.fr/entreprises/gerer-ses-ressources-humaines-et-ses-salaries/comment-fonctionne-la-reduction-generale#

SMIC annual amount used in the formula:
- Full-time job: SMIC gross annual amount = 1820 × gross hourly SMIC, or the sum of 12 identical fractions corresponding to its value multiplied by 52/12 of the legal weekly working hours.
- Part-time job: SMIC gross annual amount is calculated prorata temporis, depending on work duration (e.g. for 50 %, gross hourly SMIC × 1820/2).
- The gross annual income taken into account includes all cash or in-kind compensation elements.

**Table 2.62 — SMIC amounts [2022-2025]**

| Year | Gross hourly SMIC | Gross monthly SMIC (151.67 h ¹) | Gross monthly SMIC (169 h) | Gross annual SMIC (151.67 h ¹) | Gross annual SMIC (169 h) | Date of entry in force |
|---|---|---|---|---|---|---|
| 2022 | 10.57 | 1,603.15 | 1,786.33 | 19,237.82 | 21,435.96 | 01/01/2022 |
| 2022 | 10.85 | 1,645.58 | 1,833.67 | 19,746.96 | 22,004.04 | 01/05/2022 |
| 2022 | 11.07 | 1,678.95 | 1,870.83 | 20,147.40 | 22,449.96 | 01/08/2022 |
| 2023 | 11.27 | 1,709.28 | 1,904.63 | 20,511.85 | 22,855.56 | 01/01/2023 |
| 2023 | 11.52 | 1,747.20 | 1,946.88 | 20,966.40 | 23,362.56 | 01/05/2023 |
| 2024 | 11.65 | 1,766.92 | 1,968.85 | 21,203.04 | 23,626.20 | 01/01/2024 |
| 2024 | 11.88 | 1,801.80 | 2,007.72 | 21,621.60 | 24,092.64 | 01/11/2024 |

Notes: ¹ legal working time.
Source: https://www.insee.fr/fr/statistiques/1375188 and own elaboration for 169 hours of work.

#### EUROMOD modelling (tscer_s)

Only the "régime général" is simulated for all employees (no information on specific regimes). The simulation takes into account the number of months worked during the income reference period, not earnings variation through the year. White collar workers approximated by occupation (senior officials and managers, and professionals). No exemption from contributions, except for entitlement to reduced rates, is simulated. The reduction related to contributions for accidents at work and occupational diseases has not been simulated (rates depend on the sector of activity, not observed). Although companies need to file a declaration and apply for the reduction with Urssaf, in EUROMOD the reduction in employer social contributions is simulated for all employers. The 130 % cap for the "réduction générale des cotisations patronales" since 2020 is not simulated due to lack of data.

Note: the `lfs` variable (Firm size) was discontinued in EU-SILC from 2022 onwards, so it can no longer be used to model Employer SIC for systems using datasets from 2022 and later. The spine was adjusted to model Employer SIC based on assumptions on firm size informed by Eurostat statistics.

---

### 5.3 Self-employed social contributions — **tscse_s**

#### Liability to contributions

All self-employed in activity must pay social contributions, but there are exemptions or rate reductions for certain contributions to help employment:

- For entrepreneurship when investing in disadvantaged areas, or when previously unemployed/employed and creating or taking over a business.
- For hiring an employee with low income or in a disadvantaged area, or for young innovative enterprises.
- For the employment of young/unemployed people with particular contracts ("Contrat d'apprentissage", "Contrat de professionnalisation", "Contrat d'accompagnement dans l'emploi").
- For the employment of home help for the elderly or disabled, or child custody.
- For the self-employed when starting their activity.

#### Income base

The tax base depends on the gross self-employment activity income (i.e. gross profit) and on the type of contribution. Some contributions are taxed on whole income, others are capped. The ceiling depends on the **annual social security ceiling (PSS)**, increased by a multiplicative factor depending on the contribution.

**Table 2.63 — PSS ("plafond de la sécurité sociale") annual amounts (EUR) [2022-2025]**

| | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Annual PSS | 41,136 | 43,992 | 46,368 | 47,100 |

Source: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000050854392

#### Contribution rates

Rates depend on the type of self-employment: "Artisan", "Industry and traders" and "Farmers".

**Table 2.64 — Self-employed social contributions, rates [2022-2025]** (r = gross self-employment income)

| Contribution | Artisan / Industry and trader | Farmers |
|---|---|---|
| Family benefits | 0 % if r ≤ 1.1 PSS; 3.1 % if r > 1.4 PSS; if 1.1 PSS < r ≤ 1.4 PSS: rate = [(3.1 / 0.3 PSS) × (r − 1.1 PSS)] | if r ≤ 1.1 PSS: 0 %; if r > 1.4 PSS: 3.1 %; if r between 1.1 and 1.4 PSS: 0 % ≤ rate ≤ 3.1 %, rate = [(3.1 %)/(0.3 PSS)] × (r − 1.1 PSS) |
| Sickness | 0.5 % if r ≤ 0.4 PSS; if 0.4 PSS < r ≤ 0.6 PSS: 0.5 % ≤ rate < 4.5 %, rate = {[(4.5 % − 0.5 %)/(0.2 PSS)] × [r − (0.4 PSS)]} + 0.5 %; if 0.6 PSS < r ≤ 1.1 PSS: 4.5 % ≤ rate < 7.2 %, rate = {[(7.2 % − 4.5 %)/(0.5 PSS)] × [r − (0.6 PSS)]} + 4.5 %; if 1.1 PSS < r ≤ 5 PSS: rate = 7.20 %; if r > 5 PSS: rate = 6.50 % | 0 % if r ≤ 0.4 PSS; if 0.4 PSS < r ≤ 0.6 PSS: 0 % ≤ rate < 4 %, rate = [(4 %)/(0.2 PSS)] × r + [0 % − [(4 %/0.2 PSS)] × 0.4 PSS]; if 0.6 PSS < r ≤ 1.1 PSS: 4 % ≤ rate < 6.5 %, rate = [(2.5 %)/(0.5 PSS)] × r + [4 % − [(2.5 %/0.5 PSS)] × 0.6 PSS]; if r ≥ 1.1 PSS: 6.50 % |
| Supplementary sickness | 0.85 % of r < 5 × PSS; minimum payment calculated on 0.4 × PSS (140 € in 2022) | — |
| Pension | 17.75 % of r < PSS and 0.60 % of r > PSS (min contribution calculated on 11.5 % × PSS = 949 € in 2025) | 14.87 % of r < PSS and 2.24 % of r > PSS |
| Complementary pension | 7 % of r < PSS; 8 % of PSS < r < 4 × PSS | 4 % |
| Professional training contribution | Artisan: 0.29 % of PSS; Industry and trader: 0.25 % of PSS | — |
| Invalidity + death insurance | 1.3 % of r < PSS (min contribution based on 11.5 % × PSS; 70 € in 2025) | 1.1 % (min 11.5 % PSS) + IJ Amexa = 250 euros in 2025 and invalidity pension = 40 euros in 2025 |

Note: r = gross self-employment income.
Sources: https://www.urssaf.fr/accueil/outils-documentation/taux-baremes/taux-cotisations-ac-plnr.html and https://www.msa.fr/lfp/exploitant/cotisations-et-contributions

The rates for (liberal) professionals are not reported because there are many professional categories not subjected to the same system. It can be assumed to be the same system as Industry and Trader (the only difference is the pension and complementary pension, which is a lump sum depending on the professional class).

#### EUROMOD modelling (tscse_s)

The three types of self-employment are approximated based on industry (Agriculture vs. non-agriculture) and occupation (non-agricultural craft and trade workers are assumed to be artisans; the rest are assumed to contribute to the industry & trade regime). Contributions are simulated based on the current yearly self-employment income.

---

### 5.4 General Social contribution — **tscxc_s** ("Contribution Sociale Généralisée", CSG)

CSG applies to:

- Employment income
- Self-employment income
- Pension income and survivor pension
- Unemployment insurance benefit (ARE)
- Capital income
- Sickness benefit (only the daily allowances, not the reimbursement for medical procedures)

**Tax base:** gross income after a reduction of **1.75 %** (3 % before 2012) for professional expenses (on employment income and unemployment benefit, but **not** on capital income and sickness benefits): i.e. **98.25 % of gross income up to four times the annual PSS, 100 % above, or for pensions**.

Benefits like ASPA or RSA and, more generally, minimum incomes (AAH and AV), all the family benefits and housing benefits are **excluded** from the tax base.

**Table 2.65 — CSG rates [2022-2025]**

| Income category | Full CSG | Reduced rate | Median rate | Deductible CSG |
|---|---|---|---|---|
| Employment income | 9.2 % | — | — | 6.8 % |
| Pension income ¹ | 8.3 % | 3.8 % | 6.6 % | 5.9 % or 4.2 % |
| Unemployment benefit | 6.2 % | 3.8 % | — | 3.8 % |
| Sickness benefit | 6.2 % | 3.8 % | — | 3.8 % |
| Capital income | 9.2 % | — | — | 6.8 % |

Notes: ¹ For pension income, the rate of 8.3 % was introduced for all pensioners in 2018 (except those on the 3.8 % rate). In 2019, the government abolished the increase in this rate but only for pensioners earning less than 2,000 € per month: these pensioners pay a rate of 6.6 % from January 2019. Moreover, since 2013, an additional contribution for solidarity and autonomy (**CASA**) of **0.3 %** applies to pension income, for pensioners subject to CSG rate 6.6 % and more.

Source: https://www.economie.gouv.fr/particuliers/impots-et-fiscalite/gerer-mes-autres-impots-et-taxes/csg-et-crds-comment-ca-fonctionne#csg-et-crds-quels-sont-les-taux-_2

A fraction of the CSG can be removed from the tax base before income tax (deductible CSG).

**Exemption (CSG rate 0 %):** Pensioners with low incomes are exempted from CSG and CRDS. The income threshold depends on the tax unit ("Quotient Familial"). The income considered is the household net taxable income in n-2.

**Table 2.66 — CSG, income limit for exoneration (EUR/year) [2022-2025]**

| Annual tax base | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| 1 share | 11,431 | 11,614 | 12,230 | 12,817 |
| Each additional 0.5 share | 3,052 | 3,101 | 3,265 | 3,422 |

If pensioners exceed the ceiling above but income tax is less than 61 euros, the CSG rate is decreased to 3.8 % and is totally deductible from income for the tax calculation. Otherwise CSG is paid at a rate of 8.3 % or 6.6 %. If a pensioner has several types of income, only the pension incomes are exempted from CSG, but the income threshold takes into account all types of income. The reference income (RFR) is the n-2 income.

Since 2015, ceilings have changed and a ceiling threshold was introduced for pensioners: the income tax amount is no longer considered for application of the reduced rate of 3.8 %; only the reference income (RFR, "Revenu fiscal de référence") is taken into account. If pensioners' RFR in n-2 exceeds the lower threshold but is under the ceiling, the rate is decreased to 3.8 % and is totally deductible from income for the tax calculation.

**Table 2.67 — CSG, income limit for 3.80 % reduced rate (RFR, EUR/year) [2022-2025]**

| RFR | 2022 lower | 2022 ceiling | 2023 lower | 2023 ceiling | 2024 lower | 2024 ceiling | 2025 lower | 2025 ceiling |
|---|---|---|---|---|---|---|---|---|
| 1 share | 11,432 | 14,944 | 11,615 | 15,183 | 12,231 | 15,988 | 12,818 | 16,755 |
| Each 0.5 share | 3,052 | 3,990 | 3,101 | 4,054 | 3,265 | 4,269 | 3,422 | 4,474 |

In 2019, new ceilings were introduced for modest pensioners with a median rate of CSG of 6.6 %:

**Table 2.68 — CSG, income limit for 6.60 % median rate (RFR, EUR/year) [2022-2025]**

| RFR | 2022 lower | 2022 ceiling | 2023 lower | 2023 ceiling | 2024 lower | 2024 ceiling | 2025 lower | 2025 ceiling |
|---|---|---|---|---|---|---|---|---|
| 1 share | 14,944 | 23,193 | 15,183 | 23,564 | 15,989 | 24,813 | 16,756 | 26,004 |
| Each 0.5 share | 3,990 | 6,191 | 4,054 | 6,290 | 4,269 | 6,623 | 4,474 | 6,941 |

Above this ceiling threshold, pensions are subjected to the full CSG rate of 8.30 %.

Source (Tables 2.66-2.68): https://www.economie.gouv.fr/particuliers/impots-et-fiscalite/gerer-mes-autres-impots-et-taxes/csg-et-crds-comment-ca-fonctionne#csg-et-crds-quels-sont-les-taux-_2

#### EUROMOD modelling (tscxc_s)

CSG is simulated on current yearly incomes. The full exemption from CSG for pensioners with low incomes is simulated.

---

### 5.5 Social security debt repayment contribution — **tscdf_s** (CRDS)

Like CSG, CRDS is levied on different income categories:

- Employment income
- Self-employment income
- Pension income
- Unemployment income and activity allowance
- Family benefits (AF, ASF, ARS, CF, PAJE)
- Capital income
- Housing benefits
- Sickness benefits (only the daily allowances, not the reimbursement for medical procedures)

Unlike CSG, family benefits are subjected to CRDS. The rate is the same for all these income categories: **0.5 %**. CRDS applies globally on the same basis as CSG: paid on gross income after a reduction of **1.75 %** (3 % until 2011), except for capital income, pensions and sickness benefits (98.25 % on gross income up to four times the annual PSS, 100 % above).

The CRDS is **not deductible** for tax purposes.

#### EUROMOD modelling (tscdf_s)

CRDS is simulated using observed incomes (where they are not simulated in the model) and simulated benefits. The simulation uses current yearly incomes.

---

### 5.6 Social contribution on capital income — **tsckt_s**

In addition to CSG and CRDS, other additional social contributions apply on capital (investment & property) incomes.

**Table 2.69 — Social contribution on capital income, rates**

| Contribution | 2017 | 2018 | 2019-2025 |
|---|---|---|---|
| Social contribution | 4.50 % | 4.50 % | — |
| Additional contribution | 0.30 % | 0.30 % | — |
| Solidarity contribution | 2.00 % | 2.00 % | — |
| Solidarity levy ("prélèvement de solidarité") | — | — | 7.5 % |
| **Total (excl. CSG/CRDS)** | 6.80 % | 6.80 % | 7.5 % |
| **Total with CSG and CRDS** | 15.5 % | 17.2 % | 17.2 % |

Source: https://www.service-public.gouv.fr/particuliers/vosdroits/F2329/personnalisation/resultat?lang=&quest0=0&quest=

These contributions are **not deductible** for tax purposes.

#### EUROMOD modelling (tsckt_s)

These contributions are simulated using observed investment and property income. Current yearly income is used.

---

## 6. Personal income tax (CR pages 98-111)

Source: EUROMOD Country Report France (Y16_CR_FR.pdf), PDF pages 98–111 (printed pages 96–109). Covers end of section 2.6 (CRDS, social contributions on capital) and section 2.7 Direct taxes — Personal income tax `tin_s` (Impôt sur le Revenu des Personnes Physiques, IRPP), including CEHR (`tinto_s`) and CDHR (`tinto01_s`).

---

### 2.6.5 Social security debt repayment contribution — tscdf_s — (CRDS) [p. 98]

Like CSG, CRDS is levied on: employment income, self-employment income, pension income, unemployment income and activity allowance, family benefits (AF, ASF, ARS, CF, PAJE), capital income, housing benefits, sickness benefits (only daily allowances, not reimbursement of medical procedures).

- Unlike CSG, **family benefits ARE subject to CRDS**.
- Rate: **0.5 %** for all income categories.
- Base: same as CSG — gross income after a reduction of **1.75 %** (3 % until 2011), except for capital income, pensions and sickness benefits (base = 98.25 % of gross income up to four times the annual PSS, 100 % above).
- CRDS is **not deductible** for tax purposes.

**EUROMOD modelling:** simulated using observed incomes (where not simulated in the model) and simulated benefits; uses current yearly incomes.

### 2.6.6 Social contribution on capital income (tsckt_s) [p. 98]

Additional social contributions on capital (investment & property) income:

**Table 2.69 — Social contribution on capital income, rates [2022-2025]**

| | 2017 | 2018 | 2019–2025 |
|---|---|---|---|
| Social contribution | 4.50 % | 4.50 % | — |
| Additional contribution | 0.30 % | 0.30 % | — |
| Solidarity contribution | 2.00 % | 2.00 % | — |
| Solidarity levy | — | — | 7.5 % |
| **Total** | 6.80 % | 6.80 % | 7.5 % |
| **Total with CSG and CRDS** | 15.5 % | 17.2 % | 17.2 % |

Not deductible for tax purposes. **EUROMOD modelling:** simulated using observed investment and property income (current yearly income).

---

# 2.7 Direct taxes

### 2.7.1 Personal income tax — tin_s — (Impôt sur le Revenu des Personnes Physiques, IRPP) [p. 99]

- Tax unit: neither individual nor household — the **"Foyer fiscal"**, a sub-group of the household: one taxpayer plus persons fiscally dependent on him. Also applies to taxation of capital income (tinkt_s).
- Spouses (married or PACS civil partnership) and all dependent children/persons are grouped in the same unit.
- Dependent children are:
  - Children under 18 (automatically)
  - Children strictly under 21 (if they agree to be declared with their parents)
  - Children strictly under 25 who are students (if they agree to be declared with their parents)
  - Disabled children (automatically, whatever their age)
  - Other adults can be dependent if they are disabled.

### 2.7.2 Exemptions [p. 99]

- All family benefits, social minima (RSA) and social assistance benefits (AAH) are **exempted** from taxation.
- The only taxable allowance is the survivor's pension (AV), treated as a pension.
- A share of the CSG can be deducted from income before taxation (see social contributions section).
- Sickness benefits: only the **daily allowances** (sick leave, injury on duty leave, maternity leave) are taxable — added to earned income — except in the case of workplace accidents and benefits paid to people with a disease with prolonged treatment and particularly costly therapy. Reimbursements of medical/surgical/maternity procedures are not taxable.
- **Overtime payments**: since 2019, exempt from income tax up to **EUR 5 000** (excess taxed normally) until 2021, **EUR 7 500 from 2022**. For employee social contributions, the reduction rate on contributions is at most **11.31 %** (sum of old-age insurance contributions, only for overtime worked).

### 2.7.3 Tax allowance (abattement) [p. 100]

Deduction of **10 %** for category C1 income (earned income, pension, unemployment), with min/max ceilings per earner / pensioner / UB recipient:

**Table 2.70 — IRPP, 10 % deduction ceilings, yearly amounts (min and max) [2022-2025]**

| Income year (taxation year) | Income 2022 (Tax. 2022) | Income 2023 (Tax. 2023) | Income 2024 (Tax. 2024) | Income 2025 (Tax. 2025) |
|---|---|---|---|---|
| Earned income — min | 448 | 472 | 495 | 504 |
| Earned income — max | 12 829 | 13 522 | 14 171 | 14 426 |
| Pension¹ — min | 400 | 422 | 442 | 450 |
| Pension¹ — max | 3 912 | 4 123 | 4 321 | 4 399 |

Note ¹: for pensions, the minimum is per person and the maximum is for all people in the same tax declaration.

- Category C3 (capital income): **property income (rent) can be deducted by 30 %** if annual property income **< EUR 15 000** (income limit unchanged 2006–2023). More complicated deductions exist for property income > EUR 15 000/year (not simulated).
- Deduction for **private retirement savings ("épargne retraite")** per person = 10 % of earned income from the previous years (less the deduction for professional expenses), within these limits:

**Table 2.71 — IRPP, deduction ceilings for private retirement saving [2022-2025]**

| | Income 2022 (Tax. 2022) | Income 2023 (Tax. 2023) | Income 2024 (Tax. 2024) | Income 2025 (Tax. 2025) |
|---|---|---|---|---|
| Maximum | 32 909 | 32 909 | 35 194 | 37 094 |
| Minimum | 4 114 | 4 114 | 4 399 | 4 637 |

### 2.7.4 Tax base [pp. 100-102]

Net taxable income ("Revenu net imposable") is computed via intermediate incomes.

### 2.7.4.1 « Revenu Brut Global »

Income classes:
- **C1**: Earned income, pensions (except ASPA, AAH) and unemployment benefit
- **C2**: Self-employment
- **C3**: Capital income

For each class, the non-deductible CSG is added to gross income minus the social insurance contributions.

**Revenu Brut Global** = SUM over all persons of the tax unit of:
(C1 − deduction) + C2 + C3 + non-deductible CSG and CRDS (on C1, C2 and C3)

### 2.7.4.2 « Revenu Net Global (RNG) »

**Revenu Net Global = Revenu Brut Global − particular charges** (alimony, investments in particular sectors, hospitality expenditures for people over 75, etc. — these particular charges cannot be simulated in EUROMOD).

- Alimony paid for minor children or ascendants: **fully deductible, not limited**.
- Alimony paid for each **adult child** (declared with their parent, separate home) — deduction capped at:

**Table 2.72 — IRPP, capped amount deducted as alimony for adult child [2022-2025]**

| Income taxation year | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Cap | 6 042 | 6 368 | 6 674 | 6 794 |

- Fixed amount deductible as **payment in kind for ascendants or major children living in the household** (tax unit):

**Table 2.73 — IRPP, amount deducted for ascendants or major children [2022-2025]**

| Income taxation year | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Amount | 3 592 | 3 786 | 3 968 | 4 039 |

- Deduction for each **person 65 and over or disabled** in the tax unit, conditional on RNG thresholds:

**Table 2.74 — IRPP, amount deducted for person over 65 or disabled [2022-2025]**

| Year | Deduction (full) | RNG condition (full) | Deduction (half) | RNG condition (half) |
|---|---|---|---|---|
| 2022 | 2 476 | RNG < 15 514 | 1 238 | 15 514 < r < 24 985 |
| 2023 | 2 484 | RNG < 15 560 | 1 242 | 15 560 < r < 25 040 |
| 2024 | 2 620 | RNG < 16 410 | 1 310 | 16 410 < r < 26 400 |
| 2025 | 2 796 | RNG < 17 510 | 1 398 | 17 510 < r < 28 170 |

Source: BOFiP BOI-IR-BASE-40 (bofip.impots.gouv.fr, identifiant BOI-IR-BASE-40-20250414).

### 2.7.4.3 Net taxable income ("Revenu net imposable")

**Net taxable income = Revenu Net Global − special deductions** (disabled people, …).

### 2.7.4.4 Family ratio (Quotient Familial, QF)

Each family member gets a weight; weights are summed to compute the QF:

**Table 2.75 — IRPP, weights for family ratio**

| Person in the tax unit | Weight |
|---|---|
| Taxpayer | 1 |
| Partner (if married) | 1 |
| First child | 0.5 |
| Second child | 0.5 |
| Each child after the second | 1 |

Supplementary weights in specific cases:
- Widow/er with at least one dependent child: **+1** (from 2008 onwards)
- Each disabled adult / child: **+0.5**
- Lone parent: **+0.5** (if not a widow/er)

### 2.7.4.5 Tax base

**Tax Base = Net Taxable Income / QF** — this amount is submitted to the tax schedule.

### 2.7.4.6 Capital income [pp. 103-104]

- **2014–2017**: "prélèvement forfaitaire non libératoire" (PFNL) — an advance levy paid in year n at a rate determined by type of investment (not by total income). In year n+1, all income is declared and capital income is subject to the progressive income tax; the advance is refunded or topped up as needed.
- Since 2014, **low-income taxpayers may ask to be exempted from the levy** if their RFR in year n−1 is below a threshold: **EUR 75 000 for a couple, EUR 50 000 for a single person**. In this case a **40 % deduction** applies on the gross amount of dividend income (in 2018 this deduction only applies if progressive taxation is chosen). Interest income is treated the same way but with income limits of **EUR 25 000 for a single and EUR 50 000 for a couple**.
- **Since 2018: unique flat tax (PFU) of 30 %** — **12.8 %** flat rate for income tax + **17.2 %** social contributions. No more progressive tax unless the taxpayer opts for it when more advantageous.
- Adding the CEHR (see below), the flat tax can reach **33 to 34 %** depending on income. In 2025, with the introduction of the CDHR (see below), the flat tax can reach **37.2 %** (20 % income tax + 17.2 % social contributions).

**Table 2.76 — IRPP, capital income taxation rates [2022-2025]**

| All capital income | Flat rate¹ | Social contributions |
|---|---|---|
| Fixed-rate investment income | 12.8 % | 17.2 % |
| Interest and dividends | 12.8 % | 17.2 % |

Note ¹: social contributions must be added to the flat rate paid at the source.

### 2.7.5 Tax schedule [p. 105]

Progressive schedule; income brackets apply to annual income (per QF share).

**Table 2.77 — IRPP, marginal income tax rates [2022-2025]**

| Taxation 2022 (income 2022) — bracket | Rate | Taxation 2023 (income 2023) — bracket | Rate | Taxation 2024 (income 2024) — bracket | Rate | Taxation 2025 (income 2025) — bracket | Rate |
|---|---|---|---|---|---|---|---|
| 0 to 10 225 | 0 % | 0 to 10 777 | 0 % | 0 to 11 294 | 0 % | 0 to 11 496 | 0 % |
| 10 226 to 26 070 | 11 % | 10 778 to 27 478 | 11 % | 11 295 to 28 797 | 11 % | 11 497 to 29 314 | 11 % |
| 26 071 to 74 545 | 30 % | 27 479 to 78 570 | 30 % | 28 798 to 82 341 | 30 % | 29 315 to 83 822 | 30 % |
| 74 546 to 160 336 | 41 % | 78 571 to 168 994 | 41 % | 82 342 to 177 106 | 41 % | 83 823 to 180 293 | 41 % |
| > 160 336 | 45 % | > 168 994 | 45 % | > 177 106 | 45 % | > 180 294 | 45 % |

The tax amount obtained (on Tax Base = NTI/QF) is then **multiplied by QF** to give the total tax for the tax unit.

### Limit on tax reduction due to Family Ratio ("Plafonnement du quotient familial") [p. 106]

Corrections limit the benefit of dependent children's (or dependent adults') weights. Tax cuts for these additional weights are capped at:

**Table 2.78 — IRPP, capping of the family ratio [2022-2025]**

| | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| The two first 0.5 for lone parent | 3 756 | 3 959 | 4 149 | 4 224 |
| Each 0.5 after the second for lone parent | 1 592 | 1 678 | 1 759 | 1 791 |
| Each 0.5 | 1 592 | 1 678 | 1 759 | 1 791 |

Source: Legifrance LEGIARTI000046860759; economie.gouv.fr (plafonnement du quotient familial).

Procedure: recalculate the tax with a new QF of **1 for single, 2 for couples** (married or PACS), then subtract the caps above:
**Imax = "new tax" calculated − ceiling**. The tax to pay is the **maximum** between the "normal" tax liability and Imax.

### Complementary reduction ("réduction complémentaire") [pp. 106-107]

If the tax was corrected by the QF ceiling, income tax is reduced for disabled people, by the following amounts per disabled person:

**Table 2.79 — IRPP, complementary reduction, yearly amounts [2022-2025]**

| | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Disabled | 1 587 | 1 673 | 1 753 | 1 785 |
| Widower with dependent child | 1 772 | 1 868 | 1 958 | 1 993 |

### Tax rebate ("Décote") [p. 107]

A **non-refundable** tax rebate is given to any tax unit whose gross tax liability is under:

**Table 2.80 — IRPP, tax rebate ceilings [2022-2025]**

| Tax rebate ceiling | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Single | 1 746 | 1 840 | 1 929 | 1 964 |
| Couple | 2 889 | 3 045 | 3 191 | 3 248 |

Amounts used for the calculation of the rebate:

**Table 2.81 — IRPP, tax rebate parameters for calculation [2022-2025]**

| Tax rebate parameter | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Single | 790 | 833 | 873 | 889 |
| Couple | 1 307 | 1 378 | 1 444 | 1 470 |

The rebate = the parameter amount above **minus**:
- From 2017 to 2019: **¾** of the gross tax liability previously calculated.
- Since 2020: **45.25 %** of the gross tax liability previously calculated.

### 2.7.6 Tax credits [pp. 107-109]

Final tax payable = gross tax − tax reductions − tax credits − Employment Bonus (Prime pour l'emploi, PPE).

### Tax reductions

- Allowed for **charitable spending (donations)**, school fees for dependent children, specific investments.
- **School fees reduction** (unchanged between 2009 and 2025):
  - **61 EUR/year** per child in junior high school (ages 11–14)
  - **153 EUR/year** per child in upper high school (ages 15–18)
  - **183 EUR/year** per child in third-level education
- **Supplementary tax reduction 2017–2019**: additional flat-rate reduction on income tax for low income earners, applied after the tax rebate.
- **2020**: the new décote calculation method incorporates the tax rebate and the supplementary **20 %** tax reduction for low income; this tax reduction is deleted in its previous form.

### Tax credits

- **Green investments** (purchase of a clean vehicle, solar panels, etc.).
- **Childcare fees**: households employing people for the custody of their child can deduct **50 %** of the amount paid up to a ceiling of **EUR 3 500 per child per year**.
- **Home service employment** (tutoring, homemaker, …).
- **Energy transition, CITE** (« crédit d'impôt transition énergétique »): covers energy-efficiency work in the main house. **30 %** of expenses, capped at **EUR 8 000 (16 000 for a couple, plus 400 euros per dependent)** over a period of five years. In 2018 and 2019: rates of **15 % or 30 %** depending on the restoration work, only available until 30 June. Replaced in January 2020 by **"Ma Prime Rénov"** for modest households (extended to all households in 2021 except wealthier households). Amount depends on energy efficiency, region and household composition/income; capped at **EUR 2 400 for a single and 4 800 for a couple, plus EUR 120 per dependent person**; the aid cannot exceed **75 % of the bill**. In 2020, for intermediary or wealthier households the aid became lump sum: intermediary — **EUR 40 per window replacement, EUR 15/m² for insulation, EUR 2 000 for installation of a heat pump**; wealthier — **EUR 10/m² inside insulation, EUR 25/m² exterior insulation**. Renewed in 2021, 2022 and 2023.
- **CICE** (« crédit d'impôt pour la compétitivité et l'emploi »), 2013–2019; removed in 2019 and replaced by a reduction of certain employers' social contributions. Concerns only workers whose wage is below **2.5 SMIC**. Rates over the years: **4 %** of the wage bill of concerned workers in 2013, **6 %** in 2014, 2015 and 2016, **7 %** in 2017, **6 %** in 2018. In EUROMOD, the employer social-contribution reduction is simulated for all employers.
- **Rental property investment reductions** (conditions on tenant and rent): successive schemes — Robien, Duflot, Pinel, etc. Rates and duration of the reduction vary by scheme.
- **PPE** (individual tax credit encouraging return to employment): abolished at **31 December 2015**, integrated into the Activity Allowance (RSA/Prime d'activité) from **1 January 2016**.

### Exceptional contribution on high income — tinto_s ("Contribution exceptionnelle sur les hauts revenus", CEHR) [pp. 109-110]

- Introduced **since 2013**. Annual tax based on the **"revenu fiscal de référence" (RFR)** = RNI plus taxable capital income.
- Concerns people whose incomes exceed **EUR 250 000 for singles** and **EUR 500 000 for couples**. The fraction of income above the threshold is taxed as:

**Table 2.82 — Exceptional contribution on high income, rates [2022-2025]**

| Tax rates | Single | Couple |
|---|---|---|
| RFR ≤ 250 000 | 0 % | 0 % |
| 250 000 < RFR ≤ 500 000 | 3 % | 0 % |
| 500 000 < RFR ≤ 1 000 000 | 4 % | 3 % |
| RFR > 1 000 000 | 4 % | 4 % |

**Smoothing mechanism** for exceptional income (sale of property, etc.), under two conditions:
1. The RFR of the taxation year must be ≥ 1.5 times the average of the previous two years' RFR.
2. The RFR of the previous two years must be ≤ the release threshold for the exceptional tax on high incomes.

**Equation 7 — Smoothed tax base for CEHR:**
Tax base = M + [(RFRn − M)/2], with M = (RFRn−2 + RFRn−1)/2 (average of the last two years' RFR) and RFRn = RFR of the taxation year.
The 3 % and 4 % rates are applied on this tax base, and **the tax amount is twice this result**.

### Differential contribution on high income — tinto01_s ("Contribution différentielle sur les hauts revenus", CDHR) [pp. 110-111]

- **In 2025**, an exceptional **one-year** differential contribution on high incomes was introduced, concerning only taxpayers who are tax residents in France. Aim: ensure that **at least 20 %** of the income of the highest earners is taxed.
- Based on the **adjusted RFR** (a variant of the income used to calculate personal income tax after adjustments). Concerns people whose adjusted RFR exceeds **EUR 250 000 for singles** and **EUR 500 000 for couples**.
- Calculated as the difference (when positive) between **20 % of the adjusted RFR** and the sum of income tax, CEHR and the flat-rate levies due on 2025 income. It does not apply to taxpayers whose 2025 effective tax rate (income tax + CEHR + withholding tax) exceeds 20 % of adjusted RFR.
- Items removed from the adjusted RFR base (hence out of CDHR scope), including:
  - A fixed allowance of **EUR 500 000** on gains from share sales by retiring executives; a **40 %** allowance on distributed income under the progressive tax scale; a **50 %** allowance on gains from bonus shares worth under **EUR 300 000**.
  - Income exempt through bilateral tax treaties and under **article 155 B of the CGI** (impatriate regime).
  - Income not regularly collected exceeding the average net income taxed over the last three years: included at only **25 %** of its amount.

**Equation 8 — CDHR:**
CDHR = (Adjusted RFR × 20 %) − [(Income tax + CEHR + flat rate) + (EUR 1 500 for each dependant person and EUR 12 500 for a couple subject to joint taxation)]

The income tax, CEHR and flat rate used in this calculation are also adjusted:
- Increased by **EUR 1 500 per dependant** and by **EUR 12 500** for taxpayers subject to joint taxation;
- Increased by the benefit provided by a limited number of tax credits and reductions (e.g. tax credits under international tax treaties, Duflot and Pinel reductions, reduction for cash subscriptions to company capital, property restoration in protected areas, etc.). Only **25 %** of the tax paid on exceptional income (itself taken into account for 25 % of its amount) is taken into account.

**Tapering mechanism** when the adjusted RFR is:
- between **EUR 250 000 and EUR 330 000** for single, widowed, separated or divorced taxpayers; or
- between **EUR 500 000 and EUR 660 000** for taxpayers subject to joint taxation.

In this case, the amount corresponding to 20 % of the adjusted RFR is reduced by:

**Equation 9 — Tapering formula for CDHR** (adjusted RFR between EUR 250 000–330 000 single / EUR 500 000–660 000 couple):
(Adjusted RFR × 20 %) − [(Adjusted RFR × 82.5 %) − (EUR 250 000 or EUR 500 000, depending on the composition of the tax household)]

- Social security contributions are **not** taken into account in the calculation: e.g. on capital gains or income from transferable securities subject to the 30 % flat tax, only the **12.8 %** flat-tax component counts (the flat tax = 12.8 % income tax + 17.2 % social security contributions).
- Due to the difference between the adjusted RFR and the RFR: all CDHR payers must pay CEHR (if their imposition rate is less than 20 % of the adjusted RFR), but not all CEHR payers are concerned by CDHR.

### 2.7.6.1 EUROMOD modelling [p. 111, continues beyond p. 111]

- All children under 21 and all students under 25 co-residing with their parents are assumed to be declared on their parents' tax return. Children under 21 / students under 25 not co-residing with their parents cannot be accounted for (not observed in the data).
- All alimonies paid are assumed to be paid for underage children, and thus fully deductible from the tax base.
- All children aged 18+ and dependent adults are assumed to entitle the taxpayer to the specific allowance claimable on their behalf.
- Disability is based on observed status in the data (**pl031 = 8**).
- Capital income: an **optimization** is simulated — both flat-rate taxation (PFU) and inclusion into total income under progressive taxation are simulated, and the option yielding the lower tax liability is chosen. No information exists on the source of investment income, so the tax deduction for dividends when not applying the PFNL regime is simulated for all types of investment income.
- Simulated tax credits: tax credit for childcare fees, tax credit for mortgage interest expenditure, tax credit for children of school age, and the refundable employment credit (PPE until 2015; since 2016 the activity allowance replaces the PPE). Tax credits for childcare expenses are simulated for all families where both parents are in work and there is a child younger [text continues on p. 112 of the PDF].

---

# EUROMOD Country Report France (Y16_CR_FR) — Extraction

## 7. Extraordinary measures & consumption taxes (CR pages 111-131)

> Source: EUROMOD Country Report France, PDF pages 111-131 (printed pages 109-129). Covers end of section 2.7.6 (CDHR modelling), section 2.8 Extraordinary measures and section 2.9 Consumption taxes.

---

### 7.0 Carry-over from 2.7.6 — CDHR (Contribution différentielle sur les hauts revenus), end of section (p. 111-112)

The adjusted reference tax income (adjusted RFR) used for the CDHR is:

- Increased by €1,500 per dependant and by €12,500 for taxpayers subject to joint taxation;
- Increased by the benefit provided only by a limited number of tax credits and reductions (tax credits provided by international tax treaties, tax reductions under the Duflot and Pinel schemes, tax reduction for cash subscriptions to company capital, reduction for property restoration expenditure in protected areas, etc.). Only 25% of the tax paid on exceptional income (itself taken into account for 25% of its amount) is taken into account.

Tapering mechanism when the adjusted reference tax income is:
- between €250,000 and €330,000 for single, widowed, separated or divorced taxpayers; or
- between €500,000 and €660,000 for taxpayers subject to joint taxation.

In this case the amount corresponding to 20% of the adjusted RFR is reduced by:

**Equation 9. Tapering formula for CDHR** (adjusted RFR between €250,000–€330,000 single / €500,000–€660,000 couple):

```
(Adjusted RFR * 20%) - [(adjusted RFR * 82.5%) – (€250,000 or €500,000 depending on the composition of the tax household)]
```

Social security contributions are NOT taken into account in the calculation: e.g. on capital gains or income from transferable securities subject to the 30% flat tax (PFU), only the 12.8% flat tax component counts (the flat tax = 12.8% tax + 17.2% social security contributions).

Note: due to the difference between adjusted RFR and RFR, all CDHR payers must pay CEHR (if their imposition rate is less than 20% of the adjusted RFR), but not all CEHR payers are concerned by CDHR.

#### 2.7.6.1 EUROMOD modelling (income tax, p. 111-112)
- All children under 21 and students under 25 co-residing with parents assumed declared on parents' tax return (non-coresiding ones not observed in data).
- All alimonies paid assumed paid for underage children → fully deductible from tax base.
- All children aged 18+ and dependent adults assumed to entitle taxpayer to the specific allowance on their behalf.
- Disability based on observed status (pl031=8).
- Capital income: optimization simulated — both flat rate taxation (PFU) and inclusion into progressive taxation are simulated and the lower-tax option chosen. No information on the source of investment income, so the tax deduction for dividends (when not applying the PNFL regime) is simulated for all types of investment income.
- Simulated tax credits: child care fees, mortgage interest expenditure, children of school age, refundable employment credit (PPE until 2015; since 2016 the activity allowance replaces the PPE). Child care credit simulated for all families where both parents work and there is a child younger than 6; maximum yearly deduction simulated in all cases. Mortgage interest credit approximated based on age of head: households paying mortgage interest with head under 45 assumed eligible (more accurate rules can be run only with national SILC data).
- PPE simulated on current rather than previous year's income; conversion factor sums partial income-source-specific factors; only months worked (not hours) used; married persons with missing partner treated as two-earner couple.
- Smoothening mechanism of the exceptional contribution on high incomes (CEHR) not simulated (no RFR income of previous years).
- Cap on direct taxes not simulated.
- Since SILC 2022, bsuwd (Survivors' benefits) reported as zero (no py110n recipients in recent French samples), affecting the computation of tax deductions for pension income (Table 2.66) and potentially accuracy of related calculations.
- CDHR: adjusted RFR cannot be computed from SILC (no info on type/source of income or type of tax reduction), so adjusted RFR is assumed equal to RFR.

---

### 7.1 (CR 2.8) Extraordinary measures

#### 7.1.1 (CR 2.8.1) Wage compensation scheme in response to Covid-19 — `bwkmcee_s` (p. 112-116)

Context: during the Covid-19 crisis, access to partial unemployment (activité partielle) was facilitated to avoid massive dismissal. Lockdowns: 2020: March 17–May 10 and October 30–December 15; 2021: April 3–May 3.

Measures:
- Chronic illness or childcare (children under 16 whose school is closed): workers could apply for sickness benefit without the usual waiting period until 1 May. Afterwards, to avoid the benefit decrease from the 31st day (from 90% to 66% of net wage), they go into partial unemployment (84% of net wage for wages > SMIC, 100% for wages up to SMIC). From 1 June, parents wishing to keep children home while schools reopened were no longer eligible.
- Workers who cannot telework or whose activity decreased/stopped can be assigned to partial unemployment (including working zero hours).

**Table 2.83 — Covid-19 partial unemployment, cost and beneficiaries [2020-2021]**

| Month | Partial unemployment — beneficiaries | Full-time equivalent | Cost (EUR) | Sickness benefit (lack of activity / childcare due to Covid) — beneficiaries | Cost (EUR) |
|---|---|---|---|---|---|
| March 2020 | 6.7 million employees (866,000 firms) | 2.2 million | 3.2 billion | | |
| April 2020 | 8.4 million employees (974,000 firms) | 4.6 | 8.98 billion | 2 million employees | 1.1 billion |
| May 2020 | 7 million employees (886,000 firms) | 3.1 | 4.7 billion | | |
| June 2020 | 3.2 million employees (408,000 firms) | 1.4 | 2.1 billion | | |
| July 2020 | 1.8 million employees (237,000 firms) | 0.6 | 1.2 billion | | |
| August 2020 | 1.1 million employees (157,000 firms) | 0.4 | 0.7 (billion) | | |
| September 2020 | 1.2 million employees (152,000 firms) | 0.5 | 0.8 | | |
| October 2020 | 1.8 million employees (261,000 firms) | 0.5 | 0.9 | | |
| November 2020 | 3.1 million employees (456,000 firms) | 1.7 | 2.3 | | |
| December 2020 | 2.5 million employees (335,000 firms) | 1.1 | 1.9 | | |
| January 2021 | 2.2 million employees (300,000 firms) | 1.1 | 1.6 | | |
| February 2021 | 2.2 million employees (294,000 firms) | 1.2 | 1.7 | | |
| March 2021 | 2.4 million employees (301,000 firms) | 1.1 | 2 | | |
| April 2021 | 2.7 (251,000 firms) | 1.5 | 2 | | |

Source: DARES tableaux de bord marché du travail crise sanitaire (dares.travail-emploi.gouv.fr).

Precarious workers (short contracts + unemployment periods): an exceptional allowance guarantees a minimum income of €900 from November 2020 to May 2021; the amount is the difference between their income/allowance and €900. Eligibility: having worked at least 138 days in short contracts in 2019 and being unable to work sufficiently in 2020. **Not implemented in EUROMOD** (no info on cumulation of short contracts).

##### Definitions (2.8.1.1)
Firms can request a partial activity authorisation if they encounter difficulties or must stop activity due to the Covid-19 pandemic, allowing them to allocate employees to partial unemployment.

##### Eligibility conditions (2.8.1.2)
- Employees of private firms whose activity is affected by Covid-19, where the firm requested partial activity authorisation to temporarily lay off (fully or partially) employees. Employers pay wages and are partially reimbursed retrospectively by the administration. Administration must answer within 15 days; authorisation granted for a renewable period up to 12 months.
- Since 1 September: in case of school closure or isolation of children due to Covid-19, if neither parent can telework, one of them can claim partial unemployment.

EUROMOD identification: a random variable from a uniform distribution allocates individuals to the scheme.

**Table 2.84 — Share of wage compensation by sector (EUROMOD variable `lindi`)**

| Sector | Share of workers |
|---|---|
| 1: Agriculture & fishing | 11% |
| 2: Mining, Manufacturing and Utilities | 36% |
| 3: Construction | 62% |
| 4: Wholesale and retail | 18% |
| 5: Hotels and restaurants | 100% |
| 6: Transport and communication | 40% |
| 7: Financial intermediation | 17% |
| 8: Real estate and business | 71% |
| 9: Public administration and defence | 8% |
| 10: Education | 8% |
| 11: Health and social work | 8% |
| 12: Others | 62% |

Source: own elaboration.

**Table 2.85 — Number of months in wage compensation (assumed distribution)**

| Number of months in wage compensation | Share of beneficiaries |
|---|---|
| 2 months | 10% |
| 3 months | 39% |
| 4 months | 24% |
| 5 months | 27% |

Note: months in wage compensation cannot exceed the number of months worked in the dataset (`yemmy`). Source: own elaboration.

Workers transiting to compensation schemes are assumed to work a share of their normal hours between 49% and 58%. Figures computed from Ministry of Labour official statistics as of 15 September (DARES).

##### Income test (2.8.1.3)
No income test; the benefit amount depends on the salary earned.

##### Benefit amount (2.8.1.4)
- Employee receives 70% of gross hourly wage for each hour not worked (= 84% of net hourly wage); 100% up to SMIC is reimbursed by the state (no remaining cost for companies), with a minimum of €8.59 (€8.11 in 2021) and a maximum of €33.30 (€32.29 in 2021) per hour not worked.
- From 1 July 2021, for companies not administratively closed nor in specific protected sectors (hotels and restaurants, tourism, culture, sport, events), the rate decreases to 60% of gross (72% of net hourly wage) — the usual rate — with a minimum of €8.11 (€8.59 in 2022) and a maximum of €27.68 (€28.54 in 2022) per hour not worked, with 40% remaining to be paid by employers.
- Facilitated access until summer 2021; relaxed administrative procedures. For childcare in case of school closure, the employee must provide a certificate. Up to 4.5 SMIC (€6,927 in 2021; €7,152.75 in 2022), the amount remaining to be paid by the employer is compensated or partially compensated; administration answer time reduced to 2 days (instead of the usual 15).

Progressive decrease introduced in 2021:
- March–May 2020: the 70% of gross salary (84% of net) is fully paid by the administration.
- 1 June 2020 – May 2021: administration pays 60% of gross salary, firm pays the remainder. Protected sectors (hotels and restaurants, tourism, culture, sport, events, passenger transport): administration pays the full 70% of gross.
- June 2021: administration pays 52% of gross, firm pays remainder. Protected sectors: administration pays the full 70%.
- July 2021: allowance rate decreases to 60% of gross wage; administration pays 36% of gross, firm the remainder. Protected sectors: administration pays the full 60%.
- August 2021: administration pays 36% of gross, firm the remainder. Protected sectors: administration pays 52% of gross.

**Table 2.86 — Rates of employees' allowance [2020-2022]**

| Date | All other sectors (% gross hourly wage) | Protected sectors (tourism, hotels/restaurants, sports, culture, events, passenger transport) (% gross) | Related sectors with decrease in turnover (% gross) | Closed / partially closed firms (sanitary measures) (% gross) | All other sectors (% net) | Protected sectors (% net) | Related sectors (% net) | Closed firms (% net) |
|---|---|---|---|---|---|---|---|---|
| March–May 2020 | 70% | 70% | 70% | 70% | 84% | 84% | 84% | 84% |
| June 2020 – May 2021 | 70% | 70% | 70% | 70% | 84% | 84% | 84% | 84% |
| June 2021 | 70% | 70% | 70% | 70% | 84% | 84% | 84% | 84% |
| July 2021 | 60% | 70% | 70% | 70% | 72% | 84% | 84% | 84% |
| August 2021 | 60% | 70% | 70% | 70% | 72% | 84% | 84% | 84% |
| September – 30 October 2021 | 60% | 60% | 70% | 70% | 72% | 72% | 84% | 84% |
| December 2021 – February 2022 | 70% | 70% | 70% | 70% | 84% | 84% | 84% | 84% |

(Layout of the PDF table is merged across columns; the reliable reading: allowance is 70% gross / 84% net for everyone until June 2021; from July 2021 it is 60% gross / 72% net for "all other sectors" while protected/related/closed sectors stay at 70% gross / 84% net; from September to 30 October 2021 protected sectors also fall to 60%/72%, related and closed firms keep 70%/84%; December 2021 – February 2022 back to 70% / 84%.)
Source: securite-sociale.fr (Covid-19 — dispositif exceptionnel press release).

**Table 2.87 — Rates reimbursed to firms and amount remaining to pay for firms [2020-2022]**

| Date | Administration reimbursement — all other sectors (% of gross hourly wage normally paid) | Reimbursement — protected sectors | Reimbursement — related sectors with turnover decrease | Reimbursement — closed / partially closed firms | Remaining to pay — all other sectors (% of gross hourly wage really paid) | Remaining — protected sectors | Remaining — related sectors | Remaining — closed firms |
|---|---|---|---|---|---|---|---|---|
| March–May 2020 | 70% | 70% | 70% | 70% | 0% | 0% | 0% | 0% |
| June 2020 – March 2021 | 63% | 70% | 70% | 70% | 10% | 0% | 0% | 0% |
| April–May 2021 | 60% | 70% | 70% | 70% | 15% | 0% | 0% | 0% |
| June 2021 | 52% | 70% | 70% | 70% | 25% | 0% | 0% | 0% |
| July 2021 | 36% | 60% | 60% | 70% | 40% | 15% | 15% | 0% |
| August 2021 | 36% | 52% | 52% | 70% | 40% | 25% | 25% | 0% |
| September – 30 November 2021 | 36% | 36% | 60% | 70% | 40% | 40% | 15% | 0% |
| December 2021 – February 2022 | 70% | 70% | 70% | 70% | 0% | 0% | 0% | 0% |

(The PDF table cells are merged; percentages above are the best faithful reconstruction of the printed values: 70%/0% Mar-May 2020; 63%/10% others vs 70%/0% protected Jun 2020–Mar 2021; 60%/15% Apr-May 2021; 52%/25% vs 70%/0% June 2021; 36%/40%, 60%/15%, 70%/0% July 2021; 36%/40%, 52%/25%, 70%/0% August 2021; 36%/40% with 0%…15% for protected/related and 70%/0% for closed firms September–30 November 2021; 70%/0% for all December 2021–February 2022.)
Source: securite-sociale.fr.

With the Covid crisis and the war in Ukraine, until end of 2022, in addition to protected-sector companies, other companies can claim a 10% remaining-to-pay long-term partial unemployment (70% of gross for employees, with 60% of gross reimbursed to employers):
- companies affected by mandatory closure due to sanitary conditions;
- companies facing a drop in activity and/or supply difficulties;
- companies unable to implement Covid preventive health measures;
- employees who must look after their children due to class closures linked to Covid (or childcare facilities) or introduction of gauges (capacity limits).

##### Compatibilities (2.8.1.5)
Not compatible with any inactivity benefit (ARE, ASS, RSA).

##### Taxation and income testing (2.8.1.6)
The amount paid by the employer is exonerated from social contributions (both employee and employer parts) but subject to CSG (rate 6.2%) and CRDS (0.5%) on the basis of 98.25% of the compensation paid; these deductions are not applied if they would bring remuneration below gross SMIC (€1,539.42). The amount paid by the employer is included in the income test for other benefits.

##### EUROMOD modelling (2.8.1.7)
- Simulated with the general rules in place on 30 June: in 2020, 70% of the wage compensation paid by the administration (rest by the firm); in 2021, 60%. Applied to all workers (data limitations prevent sector differentiation).
- Produces results only when run with the LMA add-on. Individuals selected for transitions are defined in the `TransLMA_xx` policy (switched on automatically by the add-on; off in the baseline). See 'Simulating labour market transitions in EUROMOD'.
- 2020: labour transition data produced by Eurostat from LFS distributional information plus administrative data; durations and % hours worked modelled against EU-LFS longitudinal and quarterly transitions.
- 2021: not enough information available — all parameters set to zero.

#### 7.1.2 (CR 2.8.2) Self-employed and firm compensation scheme in response to Covid-19 — `bwkmcse_s`, `bseec_s` (p. 118-121)

##### Definitions (2.8.2.1)
Solidarity fund (fonds de solidarité) compensating firms and self-employed for turnover losses above 50% comparing March/April/May 2020 to the same months of the previous year. Eligible: fewer than 10 employees, turnover below €1 million, taxable profits below €60,000. Maximum compensation €1,500 per month (max €4,500 for the three months). Firms/self-employed fulfilling certain conditions can get an additional amount between €2,000 and €10,000 in 2021 (between €2,000 and €5,000 in 2020).

Two stages:
- "Volet 1": losses during the lockdown for March, April and May (max €1,500/month).
- "Volet 2": for beneficiaries of volet 1, an additional allowance between €2,000 and €10,000 (only for firms/self-employed in sectors strongly affected by the crisis with losses ≥ 80%).

One-off financial assistance of €1,250 for self-employed in 2020 and 2021 (except liberal professions), limited by previous contributions paid. Also: deferral of social and tax contributions; government-guaranteed loans (PGE) or loan rescheduling for firms with financial problems. In 2022, exceptional support renewed only for self-employed in hotels, restaurant, nightlife, events and travel agency sectors.

##### Eligibility conditions (2.8.2.2)

**In 2020:**
- Until 31 May 2020: self-employed with fewer than 10 employees, previous-year turnover below €1 million, previous-year taxable profits below €60,000.
- From 1 June 2020: only some sectors (restaurants, tourism, culture, sport and events), with increased limits: 20 employees and €2 million turnover.
- Additional conditions: activity started before 01/02/2020; not in suspension of payments at 01/03/2020.
- From 1 June to September: only sectors strongly affected (restaurants, tourism, culture, sport, events, passenger transport), doubled limits (20 workers, €2 million turnover).
- October and November: applied to all sectors (fewer than 50 workers), no turnover condition.
- From December 2020: all firms mentioned before; firms receiving the public but closed for administrative Covid reasons without size criteria; firms of protected sectors durably affected losing at least 50% of turnover (no size criteria); other sectors: firms under 50 employees impacted by lockdown with turnover losses of at least 50%.

**In 2021** — can benefit from the solidarity fund:
- firms subject to an administrative ban on receiving the public with turnover losses from 50% (no condition on employees or taxable profit);
- firms partially closed with turnover losses of 20% (no condition on employees or taxable profit);
- firms of protected sectors with turnover losses from 50% (no condition on employees or taxable profit);
- firms of other sectors with turnover losses from 50% (firms with fewer than 50 employees, no condition on taxable profit).
- Summer (from June): fund adapted to reopening/sanitary conditions; only firms administratively closed during the period and firms from protected sectors strongly impacted.
- October 2021: creation of the "dispositif loyer" for retail and service businesses with several shops, some closed between February and May 2021 (commercial areas subject to ban on public access). Aid assessed month-by-month, relative to other aid granted; amount = sum of rent and charges per shop in proportion to days closed.

**In 2022** (epidemic rebound end-2021 / early-2022; sectors: event industry, hotel and restaurant industry, caterers, travel agencies, indoor leisure, culture, sport, companies subject to bans on receiving the public or gauges):
- Micro-enterprises and self-employed: exceptional financial assistance (AFE) and assistance for contributors in difficulty may be requested.
- Reactivation of exemption/reduction of social contributions for November–December 2021 and January 2022: 100% reduction if activity drop > 65%; 50% reduction for a drop between 30% and 65%.
- December 2021: "aide renfort" to compensate certain charges for companies forbidden to receive the public (if turnover loss ≥ 50%).
- Reinforcement of the "coûts fixes" provision for December 2021 and January 2022 following administrative closure of nightclubs: compensates 100% of operating losses (previously 90% for companies < 50 employees and 70% for those > 50 employees, for all companies banned from receiving the public in the sectors above).
- Reinforcement of partial activity until end of January 2022 with zero cost to employers who lost 65% of turnover or are subject to health restrictions.
- Extension of state-guaranteed loans (PGE) until end of June 2022, repayment period extended from 6 to 10 years.
- Extension of the solidarity fund in January and February 2022 with these conditions:
  - firms subject to a total administrative ban on receiving the public with turnover loss of 20% (no employee/profit condition): aid = 20% of reference turnover, capped at €200,000;
  - firms partially closed (minimum 21 days of closure) with turnover loss of 50% (no employee/profit condition): aid = 20% of reference turnover, capped at €200,000;
  - firms in other sectors subject to a total administrative ban, domiciled in an area under confinement for at least 8 days in the month, with turnover loss of 20% (no profit condition): aid = turnover loss up to €1,500;
  - firms in protected sectors with turnover losses from 10% (no employee/profit condition) — must have benefited from the solidarity fund at least one month between January and May 2021, achieved 15% of reference turnover, be domiciled in a territory under state of health emergency, and have been under confinement or curfew at least 19 days in the month: aid = 40% of turnover loss (up to 20% of reference turnover, capped at €200,000);
  - firms in other sectors domiciled in an area under confinement at least 8 days in the month with turnover losses from 50% (firms < 50 employees, no profit condition): aid = turnover loss up to €1,500.
- Total aid may not exceed €2.3 million over the period March 2020 – June 2022.
- War in Ukraine: partial activity with zero remaining cost for employers extended for affected companies until end of 2022.

##### Income test (2.8.2.3)
Conditions on turnover, turnover losses and taxable profit (see above).

##### Benefit amount (2.8.2.4)
- Turnover loss with a maximum of €1,500 per month (first stage of the solidarity fund).
- €2,000 to €5,000 for the second stage in 2020 (€2,000 to €10,000 in 2021).
- €1,250 for the extraordinary financial assistance.
- From December 2020, firms subject to a ban on receiving the public choose between: amount of losses capped at €10,000, or 20% of turnover up to €200,000.
- Partial closure: €1,500 for turnover losses between 20% and 50%; €10,000 or 20% of turnover up to €200,000 for losses from 50%.
- Protected sectors: up to €10,000 from 50% losses; 15% of turnover for losses from 50% to 70%; amount can reach 20% of turnover within the €200,000 limit.
- Other firms: €1,500 with turnover losses from 50%.
- Summer 2021 (only administratively closed firms, 20% of turnover up to €200,000 per month of closure, and protected-sector firms):
  - June 2021: 40% of turnover losses (within the limit of 20% of turnover or €200,000), from 50% of losses;
  - July 2021: 30% of turnover losses, from 50% of losses;
  - August 2021: 20% of turnover losses, from 10% of turnover losses;
  - September–December 2021: 20% of turnover losses from 10% of turnover losses; protected firms or firms in specific areas under confinement: 40% of turnover losses (within the limit of 20% of turnover or €200,000);
  - January–February 2022: fund only available for nightclubs and overseas territories confined or under curfew.

##### Taxation and income testing (2.8.2.5)
Not taxable.

##### EUROMOD modelling (2.8.2.6)
- Only the first stage of the solidarity fund is simulated (data limitations for the second). Only eligibility conditions on profits in 2020 (< €60,000) and number of employees in 2020 (≤ 20) and 2021-2022 (≤ 50) can be simulated. No information on turnover losses, so all eligible self-employed are assumed to receive the actual average benefit: **€1,278 in 2020** (as of 1 October 2020) and **€2,272 for 2021 and 2022** (as of 1 October 2021).
- Produces results only with the LMA add-on; individuals selected in `TransLMA_xx` (on automatically with the add-on, off in the baseline).
- The one-off financial assistance is simulated using current self-employed social insurance contributions as a proxy for previous contributions (not in the dataset).
- 2020: Eurostat labour transition model data (LFS + administrative data). For 2021 and 2022, not enough information — all parameters set to zero.

#### 7.1.3 (CR 2.8.3) Exceptional 2021-2022 lump sum to compensate inflation increase — `binxp_s` (Indemnité inflation) (p. 123)

**2021:**
- Lump sum of €100 paid in one go to people over 16 years old earning on average less than €2,000 net per month.
- Net monthly income = average of salaries received January–October 2021 for employees; amounts received in October 2021 for other cases.
- Individualised: if both members of a household earn less than €2,000 net/month, both receive it.
- Not subject to any tax or social contributions; not counted for income tax nor when qualifying for social assistance.
- Potential beneficiaries: people in activity (employees and self-employed), retired, unemployed, ill or in maternity/paternity leave, recipients of minimum social benefits (RSA, AAH, invalidity beneficiaries…), apprentices, students on scholarship or students receiving housing benefits.
- Payment date: between December 2021 and February 2022 depending on status.

**2022 (exceptional solidarity lump sum):**
- Given to recipients of social minima (RSA, AAH, ASPA, AV, ASS, housing benefits or invalidity), apprentices and scholarship students.
- Paid in November and December: €100 one-off per household, plus €50 for each dependant in the household.
- Recipients of the activity allowance (prime d'activité): exceptional lump sum of €28, increased by €14 for each dependent child.
- The two allowances cannot be combined (activity allowance recipients cannot claim the exceptional solidarity allowance for another social minimum).

#### 7.1.4 (CR 2.8.4) Exceptional 2023 purchasing power bonus for public servants — `binps_s` (p. 123-124)

In 2023, an exceptional purchasing power bonus for certain public servants, subject to income conditions, paid in a single lump sum in the last quarter of the year.

##### Eligibility conditions (2.8.4.1)
- Recruited or appointed by a public employer before 1 January 2023;
- Still in place as of 30 June 2023;
- Received, between 1 July 2022 and 30 June 2023, remuneration of up to €39,000 gross for 12 months, or €3,250 gross per month maximum.
- If not employed for the whole period 1 July 2022 – 30 June 2023: eligibility verified by dividing total gross remuneration by the number of paid months, then multiplying by 12. With more than one employer, consider the total remuneration paid by the last employer, then apply the same calculation.

##### Benefit amount (2.8.4.2)
Staggered between €300 and €800, prorated for part-time work or if the period of work is less than 12 months. Calculated on gross remuneration received 1 July 2022 – 30 June 2023.

**Table 2.88 — Benefit amount dependent on gross income**

| Gross remuneration (GR) | Lump sum amount |
|---|---|
| GR ≤ €23,700 | €800 |
| €23,700 < GR ≤ €27,300 | €700 |
| €27,300 < GR ≤ €29,160 | €600 |
| €29,160 < GR ≤ €30,840 | €500 |
| €30,840 < GR ≤ €32,280 | €400 |
| €32,280 < GR ≤ €33,600 | €350 |
| €33,600 < GR ≤ €39,000 | €300 |

Source: Décret n° 2023-702 du 31 juillet 2023.

This lump sum is subject to social contributions and income tax.

---

### 7.2 (CR 2.9) Consumption taxes

#### 7.2.1 (CR 2.9.1) Definitions (p. 124-125)
- Consumption taxes simulated in EUROMOD: VAT and excises (additional duties on consumption, typically energy, alcoholic beverages, tobacco).
- Simulated liabilities depend on tax rules (e.g. VAT rate) and the tax base (consumption expenditures or quantities). Input data must contain household expenditures; expenditures matched into EUROMOD input files (based on SILC) come from HBS surveys at purchasing prices, so they already include the consumption taxes paid.
- **VAT** = `il_tva` variable. The model also simulates VAT liabilities at high disaggregation per consumption category (output variables tva01111, tva01112, … corresponding to COICOP codes 01111, 01112, etc.).
- **Excises** = `il_tx` variables, split into: ad-valorem excises (`il_txv`) depending on producer prices, and specific / ad-quantum excises (`il_txa`) depending on consumed quantities. Since HBS data are expenditures (price × quantity), consumption prices are needed to simulate specific excises.
- Methodology common across countries (placed in an add-on, not in each country's policy spine): see Akoğuz et al. (2020), "A new indirect tax tool for EUROMOD: final report".

#### 7.2.2 (CR 2.9.2) VAT — `il_tva` (Taxe sur la valeur ajoutée, TVA) (p. 125)

**Table 2.89 — VAT rates [2022-2025]**

| Rate category | Products | Rate 2022-2025 |
|---|---|---|
| Standard | The majority of sales of goods and services | 20% |
| Intermediate | Unprocessed agricultural products, firewood, passenger transport, museums, zoos, exhibitions… | 10% |
| Reduced | Most food products, sanitary products, books, gas and electricity subscription… | 5.5% |
| Super reduced | Medicinal products reimbursable by social security, sales of live butchery animals… | 2.1% |
| Exempted | Export, education, activities of general interest, medical activities, most rentals for main residence | — |

Notes: reduced rates for specific territories in AT, EL, ES, FR and IT are not modelled yet. Source: economie.gouv.fr (CEDEF, "Quels sont les taux de TVA en vigueur en France et dans l'Union").

Additional VAT rules stated in the section (p. 128-129):
- All alcoholic products are subject to 20% VAT.
- Waters and soft drinks: 10% VAT if taken away for immediate consumption, 5.5% VAT otherwise.
- Electricity: VAT depends on subscribed power — if > 36 kVA, VAT = 20%; for < 36 kVA, 5.5% on the subscription and 20% on the electricity price.
- Gas and fuel: 20%.

#### 7.2.3 (CR 2.9.3) Ad-valorem excises — `il_txv` (Droits d'accise ad-valorem) (p. 125-127)

Ad-valorem excises cover all tobacco products.

**Table 2.90 — Ad-valorem excise rates [2022-2025]: excise parameters**

2022 and 2023:

| Product | 2022 rate | 2022 price per 1000 units or per kg | 2022 minimum levy (per 1000 units) | 2023 rate | 2023 price per 1000 units or 1000 g | 2023 minimum levy (per 1000 units or 1000 g) |
|---|---|---|---|---|---|---|
| Cigarettes | 60% | — | 90€ | 55% | 68.1€ | 360.6€ |
| Cigars and cigarillos | 5% | 12€ | — | 36.3% | 52.2€ | 288€ |
| Rolling tobacco | 50% | 60€ | — | 49.1% | 91.7€ | 335.3€ |
| Other tobacco for smoking or inhaling after heating | 20% | 22€ | — | 51.4% | 33.6€ | 145.1€ |
| Tobacco sticks for heating | 20% | 22€ | — | 51.4% | 19.3€ | 232€ |
| Other heating tobaccos | 20% | 22€ | — | 51.4% | 72.7€ | 875.5€ |
| Tabacs à priser (snuff) | 20% | 22€ | — | 58.1% | — | — |
| Chewing tobacco | 20% | 22€ | — | 40.7% | — | — |

2024 and 2025:

| Product | 2024 rate | 2024 price per 1000 units or 1000 g | 2024 minimum levy (per 1000 units or 1000 g) | 2025 rate | 2025 price per 1000 units or 1000 g | 2025 minimum levy (per 1000 units or 1000 g) |
|---|---|---|---|---|---|---|
| Cigarettes | 55% | 71.3€ | 371.4€ | 55% | 72.7€ (printed "72.7.1€") | 378.8€ |
| Cigars and cigarillos | 36.3% | 54.7€ | 296.6€ | 36.3% | 55.7€ | 302.6€ |
| Rolling tobacco | 49.1% | 99.7€ | 345.4€ | 49.1% | 104.2€ | 335.8€ |
| Other tobacco for smoking or inhaling after heating | 51.4% | 35.2€ | 149.5€ | 51.4% | 35.9€ | 152.4€ |
| Tobacco sticks for heating | 51.4% | 30.2€ | 268€ | 51.4% | 41.1€ | 303.8€ |
| Other heating tobaccos | 51.4% | 113.9€ | 1011.3€ | 51.4% | 155.2€ | 1146.4€ |
| Tabacs à priser (snuff) | 58.1% | — | — | 58.1% | — | — |
| Chewing tobacco | 40.7% | — | — | 40.7% | — | — |

Source: douane.gouv.fr, "La fiscalité appliquée aux tabacs manufacturés et la composition du prix de vente au détail".

**Table 2.91 — Structure of cigarettes price in 2025** (pack of 20 cigarettes at €11.50 "low market" and €13 "premium", 1 January 2025, mainland France)

| Price structure in 2025 | Rate / Price | Cigarettes "low market" (€11.50 pack) | Cigarettes "premium" (€13 pack) |
|---|---|---|---|
| Retail price (pack of 20 cigarettes) | | 11.50€ | 13€ |
| Excise — rate component | 55% | 6.325€ | 7.15€ |
| Excise — price component (per 1000 units) | 72.7€ | 1.45€ | 1.45€ |
| Minimum levy (per 1000 units) | 378.8€ | (7.58€)¹ | (7.58€)¹ |
| VAT "inside"² on the retail price | 16.6667% | 1.92€ | 2.17€ |
| Tobacco retailer's gross discount | 10.29% | 1.183€ | 1.338€ |
| Manufacturers' margin | | 0.62€ | 0.89€ |

Notes: ¹ If the sum of (excise rate × retail selling price) + excise price exceeds the minimum charge, that sum applies. ² Included in the price.
Source: douane.gouv.fr (same page as Table 2.90).

#### 7.2.4 (CR 2.9.4) Specific excises — `il_txa` (Droits d'accise ad-quantum) (p. 127-130)

Specific excises apply to energy products and alcoholic products.

**Table 2.92 — Specific (ad-quantum) excise rates**

| Product | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| **Alcoholic products** | | | | |
| Wine | 3.92 EUR/hl | 3.98 EUR/hl | 4.05 EUR/hl | 4.12 EUR/hl |
| Sparkling wine | 9.7 EUR/hl | 9.85 EUR/hl | 10.02 EUR/hl | 10.20 EUR/hl |
| Cider, hydromel (mead) | 1.37 EUR/hl | 1.39 EUR/hl | 1.41 EUR/hl | 1.43 EUR/hl |
| Liquor wine, sweet wine | 48.97 EUR/hl | 49.73 EUR/hl | 50.6 EUR/hl | 51.49 EUR/hl |
| Other intermediate products: Porto, Pineau, Pommeau | 195.86 EUR/hl | 198.91 EUR/hl | 202.39 EUR/hl | 205.93 EUR/hl |
| Beer ≤ 2.8% degree of alcohol | 3.85 EUR/hl | 3.91 EUR/hl | 3.98 EUR/degree/hl | 4.05 EUR/degree/hl |
| Beer > 2.8% degree of alcohol | 7.7 EUR/hl | 7.82 EUR/hl | 7.96 EUR/degree/hl | 8.10 EUR/degree/hl |
| Rum | 903.64 EUR/hl | 917.72 EUR/hl | 933.78 EUR/hl | 950.12 EUR/hl |
| Other alcohol | 1806.28 EUR/hlap | 1834.42 EUR/hlap | 1866.52 EUR/hlap | 1899.18 EUR/hlap |
| **Other products** | | | | |
| Waters | 0.54 EUR/hl | 0.54 EUR/hl | 0.54 EUR/hl | 0.54 EUR/hl |
| Soft drinks — with sugar | 3.34 to 26.09 EUR/hl depending on quantity of sugar/hl ¹ | 3.34 to 26.09 EUR/hl depending on quantity of sugar/hl ¹ | 3.34 to 26.09 EUR/hl depending on quantity of sugar/hl ¹ | 4 to 35 EUR/hl depending on quantity of sugar/hl ¹ |
| Soft drinks — with sweetener | 3.34 EUR/hl | 3.34 EUR/hl | 3.34 EUR/hl | 3.50 EUR/hl |
| **Energy products ²** | | | | |
| TICPE (fuel) | From 59.4€/l to 76.826€/l depending on area and type of fuel | From 59.4€/l to 76.826€/l depending on area and type of fuel | From 59.4€/l to 76.826€/l depending on area and type of fuel | From 59.4€/l to 76.826€/l depending on area and type of fuel |
| TICFE (electricity) | 0.5€/MWh for power > 36 kVA; 1€/MWh otherwise ³ | 0.5€/MWh for power > 36 kVA; 1€/MWh otherwise ³ | 20.5€/MWh for power > 36 kVA; 21€/MWh otherwise ⁴ | 25.6875€/MWh for power ≤ 36 kVA; 22.5€/MWh for power > 250 kVA; 22.5625€/MWh otherwise |
| TICGN (gas) | 0.54€ or 1.52€, 1.6€ or 8.41€/MWh depending on consumer profile | 0.54€ or 1.52€, 1.6€ or 8.37€/MWh depending on consumer profile | 0.54€ or 1.52€, 1.6€ or 16.37€/MWh depending on consumer profile | 0.54€ or 1.52€, 1.6€ or 17.16€/MWh depending on consumer profile |
| TICC (coal) | 1.19€, 2.29€ or 14.62€/MWh depending on consumer profile | 1.19€, 2.29€ or 14.62€/MWh depending on consumer profile | 1.19€, 2.29€ or 14.62€/MWh depending on consumer profile | 1.19€, 2.29€ or 14.62€/MWh depending on consumer profile |

Notes:
1. See https://entreprendre.service-public.fr/vosdroits/F32101 (sugar-content scale).
2. For 2025, the figures for energy products are only valid until end of July 2025.
3. Special reduction due to high inflation, called "bouclier tarifaire" (tariff shield).
4. Prices still reduced; the normal price should be 25.6875€ or 32.0625€.
(The PDF prints "kWA"; the intended unit is kVA subscribed power. TICPE printed as "€/l" in the PDF — the national TICPE scale is per hectolitre; values reproduced exactly as printed.)
Source: ecologie.gouv.fr, "Guide 2025 sur la fiscalité des énergies".

Remark: a part of the carbon tax is included in the excises for energy products; another part is the SEQE-EU / EU ETS (not included in EUROMOD). See ecologie.gouv.fr "tarification effective du carbone".

The domestic consumption tax on energy products (Taxe intérieure de consommation sur les produits énergétiques, TICPE) applies to petroleum products intended for use as motor fuel or heating fuel. TICFE concerns electricity products.

**Table 2.93 — Additional taxes**

| Item | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| **Taxes for social security contributions** | | | | |
| Alcohol > 18% vol. (full rate) | 579.96 EUR/hl | 589 EUR/hlap | 599.31 EUR/hlap | 609.80 EUR/hlap |
| Intermediate products > 18% vol. (full rate) | 48.97 EUR/hl | 49.73 EUR/hl | 50.6 EUR/hl | 51.49 EUR/hl |
| Intermediate products > 18% vol. (reduced rate at 40%) | 19.6 EUR/hl | 19.91 EUR/hl | 20.26 EUR/hl | 20.61 EUR/hl |
| Beer > 18% vol. | 48.97 EUR/hl | 49.73 EUR/hl | 50.6 EUR/hl | 51.49 EUR/hl |
| Rums and spirits made from local alcohol | 325 EUR/hl | 403 EUR/hl | 482 EUR/hlap | 609.8 EUR/hlap ¹ |
| **Taxes called "Premix" (> 1% alcohol)** | | | | |
| Wine or other fermented beverage | 3 EUR/dlap | 3 EUR/dlap | 3 EUR/dlap | 3 EUR/dlap |
| Other products | 11 (EUR)/dlap | 11/dlap | 11/dlap | 11/dlap |
| **Other taxes** | | | | |
| Air transport passengers | 4.69€ or 8.43€ per passenger depending on destination | 4.83€ or 8.69€ per passenger depending on destination | 4.93€ or 8.87€ per passenger depending on destination | 5.05€ or 9.09€ (5.14€/9.25€ from 1 April) per passenger depending on destination |
| Air ticket solidarity tax (TSBA) | Economy class: 2.63€ (flights to EU), 7.51€ (other countries); Business class: 20.27€ (EU), 63.07€ (other countries) | same structure as 2022 (printed as a merged cell) | same structure (merged cell) | 7.4€/15€/40€ per ticket depending on distance for economy class (30€/80€/120€ for business class; 210€ to 2100€ for jets depending on type of jet and distance) |
| Ecotaxe: Malus on the purchase of polluting vehicles | From 50€ to 40,000€ (max 50% of the selling price), from 128 g to 225 g CO2/km | From 50€ to 50,000€ (max 50% of the selling price), from 123 g to 225 g CO2/km | From 50€ to 60,000€ and more, from 118 g to 193 g CO2/km, without cap | From 50€ to 60,000€ and more, from 118 g to 193 g CO2/km, without cap |

Note: ¹ End of the reduced rate in January 2025.
Sources: entreprendre.service-public.gouv.fr/vosdroits/F32101; legifrance.gouv.fr (LEGITEXT000044595989 / LEGISCTA000044599467); economie.gouv.fr (taxe malus véhicules polluants); service-public.gouv.fr actualité A18080 (TSBA, 1 March 2025).

##### Price nowcasting for excisable goods (p. 130)
Consumer prices of goods subject to excise duties are nowcasted (similarly to income updating from SILC), combining:
- Prices per product, usually from last year (fuel prices have only a 15-day delay);
- Inflation: Harmonised Index of Consumer Prices (HICP, Eurostat) at COICOP 5 digits — usually first quarter for beta release, up to third quarter for final release;
- Inflation quarter-on-quarter forecasts (DG ECFIN, confidential) by HICP main groups (unprocessed food; processed food including alcohol and tobacco; non-energy industrial goods; energy; services — overall index excluding goods) for quarters 2, 3 and 4 as needed per release.
- For details on the specific price source per good, see Akoğuz et al. (2020).
- Exception: the price of "Other tobacco" was sourced from douane.gouv.fr because the correct category is "Tabacs fine coupe destinés à rouler les cigarettes /kg" and not "Autres tabacs à fumer ou à inhaler après avoir été chauffés (narguilé, blunts, etc.)".

##### EUROMOD modelling (consumption taxes)
- Consumption taxes are in the `tco_fr` policy. They require extended EUROMOD input data (with imputed income shares of consumption expenditures at household level) and an add-on to run; the policy is off in the baseline.
- To activate: run the `ITT_xbase` add-on and select the extended EM input files (see Section 3 of the CR for methodology of the extended input files, as defined in each country's database configuration).
- Other add-ons (`ITT_*`) are for reform simulations with different behavioural responses: i) constant quantities (`ITT_XCQ`), ii) constant income shares (`ITT_XCIS`), iii) constant expenditure shares (`ITT_XCES`). These require auxiliary output files generated by first running the baseline simulation (quantities or expenditures and savings from the baseline are kept constant and enter as inputs into the reform scenarios).

*(PDF page 131 is blank apart from the page number 129.)*

---

# EUROMOD Country Report France (Y16) — extraction

## 8. Data & validation (CR pages 131-146)

*(PDF page 131 is blank; content starts on PDF page 132.)*

### 3. Data

#### 3.1 General description

- The French database is the French part of **EU-SILC** provided by Eurostat: a rotating panel survey (9 rotational groups until 2019, 4 since 2020), representative of the French population in private households (all persons aged 16 and over within the household are eligible), **excluding French Overseas Departments and territories (DOM)**.
- The underlying French survey is conducted by **INSEE** and is named **"Statistiques sur les ressources et les conditions de vie" (SRCV)**.
- Sampling frame history:
  - Before 2010: reference population estimated from the 1999 population census plus dwellings built since then.
  - 2010–2019: reference population estimated from **Octopusse** ("Organisation coordonnée de tirages optimisés pour une utilisation statistique des échantillons"), updated each year based on dwellings enumerated the previous year (only principal residences in metropolitan France).
  - Since 2020: sample drawn from the new sampling frame **"Fideli-Nautile"** based on tax sources (income tax, tax sources on built-up properties and housing tax).
- Around **14,000 households** are surveyed each year; the sample is stratified to be representative at the national level. Data collection is annual: over six weeks in May–June until 2019; since 2020, collection runs **29 January to 13 April** (to deliver data early to Eurostat, in March N+1).
- **French EU-SILC 2024 sample statistics project to a reference population of 66,167,451 individuals.**
- Since 2008, **statistical matching with tax sources**: the amount of (taxable) income and social benefits actually received over the reference year is collected directly from the public finance body, the **DGFIP**, and the three main benefit funds: the national family benefits fund (**CNAF**), the national old-age insurance fund (**CNAV**) and the central agricultural social insurance fund (**CCMSA**).
- Technical references:
  - https://www.insee.fr/en/metadonnees/source/serie/s1220
  - https://data.progedo.fr/studies/doi/10.13144/lil-1738?tab=documents

#### 3.2 EUROMOD SILC Database (EMSD)

- Before 2021 only the EU-SILC UDB was used. **From 2021 onward, the EUROMOD SILC database (EMSD)** prepared by Eurostat is used to derive the EUROMOD input dataset.
- The EMSD includes:
  - All UDB variables (each described in **DocSILC0658 (2025 operation)**; footnote 8 gives the CIRCABC link: https://circabc.europa.eu/ui/group/853b48e6-a00f-4d22-87db-c40bafd0161d/library/334d943f-6f71-4f4b-9c7e-a6767a3fe164?p=1&n=10&sort=name_ASC%22);
  - National data supplied by the National Statistical Institute (NSI), described in a national codebook;
  - EUROMOD variables created and imputed by Eurostat because of restricted data access or in-house knowledge (generation explained in the DRD).
- The national team derives additional variables requiring deep understanding of country specificities (e.g. national tax-benefit rules). The final EUROMOD input dataset combines variables from Eurostat, National Teams (NTs) and JRC.
- Some Eurostat-produced EUROMOD variables use **PDB (Production Database)** variables, which are more detailed than UDB (or not top-coded). By NSI–Eurostat agreement the national team could use this detail. **Users recomputing input data from the DRD formulas may find differences because PDB variables are not available to them.**

**Table 3.1 EUROMOD database description** (source: EU SILC 2024 and EUROMOD DRD codebook):

| Item | Value |
|---|---|
| EUROMOD database | FR_2024_c1 |
| Original name | FR_EMSD2_2024 |
| Provider | Eurostat |
| Year of collection | 2024 |
| Period of collection | January to April 2024 |
| Income reference period | 2023 |
| Sample size | 38.319 IND / 17.305 HH |

- **The income reference period of SILC 2024 is year 2023** (2023 incomes are used).
- **SILC 2021 peculiarity (Covid)**: SILC 2021 uses 2020 incomes. In 2020, Covid mitigation measures (particularly for the poorest) resulted in an unusually low number of people in poverty in the 2021 database, artificially reducing poverty in 2021. Using the `fr_2021_c2` dataset for policy year 2021 yielded a poverty rate that was too low, attributable to the increase in 2020 income from Covid benefits. The team therefore considers the most suitable match for policy year 2021 to be the **`fr_2020_c2` dataset (SILC 2020 with incomes from 2019)**.

#### 3.3 Data adjustment

- Adjustments to variables are kept to a minimum; minor cleaning ensures household composition and family relationships are coherent (e.g. young children not living alone).
- To guarantee consistency between demographic variables and income variables (referring to the previous year, on which EUROMOD simulations are based), **all children born between the end of the income reference period and the date of interview were dropped (48 observations deleted in 2024)**.
- Item non-response is treated by **re-weighting** for the first period and **re-interrogation** for following periods in the original SRCV data. Variables used to compute the new weight: age, population density of home, household type, number of men and women by age category, reference person's education, profession of reference person.

#### 3.4 Imputations and assumptions

##### 3.4.1 Time period

- Demographic information refers to time of data collection (January–April 2024); some information indicates the status quo at the end of the income reference period (2023) — e.g. two age variables (at survey time and at end-2023); similarly for some socio-economic and labour variables (rb211 basic main activity status refers to collection time; pl073 gives months in full-time work during the income reference calendar year 2023). Where possible, EUROMOD dataset information is based on variables referring to the **income reference period**.
- Income information refers to **calendar year 2023, 12-month receipt period**. All monetary incomes in the EUROMOD database are converted to **monthly** terms; EUROMOD implicitly assumes income is received at the same rate throughout the year.
- Legal framework change since 2021: **Regulation (EU) 2019/1700** (IESS regulation, 10 October 2019). Consequences:
  1. Some EU-SILC variables renamed (e.g. pe020 is now pe021);
  2. Some moved to a 3-year module (pe030 used in dew; pl020 used in lowas; pl130 used in lfs; pl160 used in ltr; hy030g used for kivho);
  3. Others totally excluded from EU-SILC (rb070 used in dmb; py200g used in ymwdt).
- See "Methodological guidelines and description of EU-SILC target variables – 2023 operation".

##### 3.4.2 Gross incomes

- EU-SILC contains both gross and net monetary incomes with flag variables indicating collection form. In most cases incomes are collected **net** (except work income, collected net of CSG and non-deductible CRDS).
- **Gross incomes were recalculated by INSEE** by adding social contributions **CSG, CRDS and employee social contributions** (if applicable for work income), estimated by **inversion of the tax rules**. More detail in the Country Quality Report: https://www.insee.fr/fr/metadonnees/source/serie/s1220

##### 3.4.3 Disaggregation of harmonized variables

Variables needed for simulating the French tax-benefit system but not available in EU-SILC were fully imputed:

1. **Unemployment benefit** disaggregated into contributory unemployment insurance (**ARE**) and means-tested unemployment assistance (**ASS**), based on benefit rules and average daily benefit amounts.
2. **Aggregate family benefits** split into components: universal child benefit (**AF**) separated using benefit rules; means-tested child benefits (**CF, ARS, PAJE**) disaggregated based on benefit rules and the relationship between gross incomes and net taxable incomes; residual amounts placed in "other child benefits". Since EU-SILC 2020 the disaggregation is based on national SILC variables **"prest_fam_autres"** (for AL, CF, ARS) and **"prest_fam_petite_enfance"** (for PAJE components / PreParE).
3. **Means-tested survivor minimum pension (AV)** separated from contributory survivor benefits by applying benefit rules.
4. **Employment income during the previous year** for recipients of unemployment insurance benefits imputed by inverting benefit rules.
5. **Geographical zone variable** for housing benefit (AL) imputed from region (NUTS 2 level db040) and urbanization (DB100). In 2024, DB040 is not disseminated in the UDB nor the EMSD; the NSI allowed Eurostat to use **PDB-DB040** to compute **drg01** for housing benefit. The Metropolitan France / Overseas distinction is given in **drgn1/drgn2** (SILC scope extended to Overseas territories since 2022): drgn1/drgn2 have two modalities each — 11 and 30 for Metropole, 9 and 29 for Overseas territories — instead of the detailed modalities of past years.
6. **Housing benefit** disaggregated into benefits received by tenants vs the rest, based on tenure status.
7. **Employment income** split into regular-hours pay and **overtime pay**, based on current hours paid reported in SILC. Regular hours assumed 35 h/week for every employee (including part-time). Average hourly pay from yearly employment pay, months in employment and weekly hours. Statutory overtime rules applied (extra 25 % pay for the first 8 hours per week, 50 % thereafter). Overtime pay assumed zero for employees working <35 h/week and for those working <12 months in the income reference period (hours information too unreliable there).

Since 2021, some previously-disaggregated variables are available directly in the national SRCV survey and are now used:

- Means-tested disability benefit (**AAH**), previously separated from contributory disability pensions (BDI), now from SRCV variable **"prest_precarite_hand"**.
- Invalidity pension (**pdi00**), also previously from BDI, now from SRCV variable **"prest_precarite_invalidite"**.
- Old-age pensions (POA) previously split into contributory pensions (poa00) and the means-tested elderly benefit **ASPA** (variable **bsaoa**) using eligibility rules on age/income and observed amounts; ASPA (bsaoa) is now from SRCV variable **"prest_precarite_vieil"**.
- Social exclusion benefits (BSA) previously split into the main social assistance benefit (**RSA**, variable **bsa00**), the activity allowance (**bsawk**) and the rest by simulating benefit rules (residual in "other social assistance benefits"). RSA (bsa00) is now based on SRCV variable **"RSA_soc_i"** in SILC 2019 (renamed **"rsa_men_nsilc"** since SILC 2020); activity allowance on **"RSA_pa_i"** in SILC 2019 (**"ppa_men_nsilc"** since SILC 2020), without change for the rest.
- Since SILC 2019, **personal income tax (tin)** is based on national variable **"IRPP"**; **property tax (tpr)** on national variable **"TF"** (called **"taxfon"** in SILC 2020). In SILC 2021 "taxfon" was not collected so **HY120** was used; in 2022 the national variable was collected and used in EMSD.
- In SILC 2020: SIC employee based on national variable **"cots_sal"**, SIC self-employed on **"contindep"**, SIC employer on **"cotp_sal"**. In SILC 2021 these SIC variables were not available. Since SILC 2022, "cots_sal" is available, "cotp_sal" is not.

#### 3.5 Updating (uprating)

- EUROMOD currently permits simulation of **20 policy years, 2006–2025**.
- Simulations use datasets (as listed in the report): FR-SILC 2007, FR-SILC 2010, FR-SRCV2012, FR-SILC2015, FR-SILC2016, FR-SILC2017, FR-SILC2018, FR-EMSD2-2019, FR-EMSD2-2020, FR-EMSD2-2021, FR-EMSD2-2022, and FR-EMSD2-2023, containing 2006, 2009, 2011, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022 and 2023 incomes. (The report says "eigth datasets" but lists twelve names / thirteen income years.) Data year and policy year are aligned only in 2006, 2009, 2011, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022 and 2023.
- **Uprating factors** correct for time inconsistencies between input dataset and policy year — typically changes in average incomes between data year and policy year, or indexation rules. **Separate factors are used for most income components. No attempt is made to correct for demographic or other population changes.**
- The list of updating factors for the 2021 dataset and their sources is in **Annex 1**.
- For simulated variables, the actual simulated amounts are used in the baseline rather than uprated original variables; uprating factors for simulated variables are still provided so users can turn off simulation of a particular variable.

#### 3.6 Extended input data (household expenditures for consumption taxes)

- Consumption-tax simulation requires **extended EUROMOD input files**: core input files (EU-SILC / National SILC) extended with household-level income shares of expenditures by product, imputed from **EU/National-HBS**, using the **semi-parametric method of Akoğuz et al (2020)**.

**Table 3.2 Extended EUROMOD database for the simulation of consumption taxes** (SILC 202[4] – Income year 2023 – Expenditures from HBS 2015; source: own elaboration):

| Item | Value |
|---|---|
| EUROMOD database | FR_2024_c1_2024_03_e2 |
| Year of collection (HBS) and source | HBS 2015 |
| Year of collection (SILC) and source | SILC 2024 |
| Coverage and sample size | 17.305 Households (38.271 individuals) |
| Share of households with negative incomes excluded from the matching procedure | 0.0020% |

- The extended files contain all standard variables plus income shares of each HBS consumption category. For France (data FR_2024_c1_2015_03_e2), there are **193 xs_c\* variables** (income shares of expenditures) corresponding to harmonized consumption categories at **COICOP 2003 level 4 (five digits)** (e.g. rice: xs_01111; bread: xs_01112). Due to lack of information in Eurostat-distributed HBS files, there is **no consumption reported at 5-digit COICOP level for 3-digit codes CP022, CP054, CP096, CP103, CP124** (positive consumption may exist at 3- or 4-digit level, but EUROMOD uses only 5-digit values).
- Same sample and identifiers ("idperson", "idhh") as the core database.

**Validation HBS 2015 – Extended EM Input.** The same-year column (HBS 2015 vs Extended EM Input 2015) reflects imputation quality; the cross-year column is influenced by matching noise plus changes in population characteristics and income distribution, so it is informative only and should not be used to validate the imputation.

**Table 3.3 Expenditure coverage of Extended EUROMOD Input files** (source: own elaboration using HBS 2015, 2015 SILC-based data, 2024 SILC-based data):

| COICOP group | HBS 2015 – Extended EUROMOD Input 2015 (%) | HBS 2015 – Extended EUROMOD Input 2024 (%) |
|---|---|---|
| 1 | 86.7 | 95.3 |
| 2 | 49.1 | 51.5 |
| 3 | 97.4 | 103.9 |
| 4 | 101.9 | 101.8 |
| 5 | 96.7 | 104.0 |
| 6 | 92.6 | 101.8 |
| 7 | 96.2 | 113.0 |
| 8 | 103.2 | 120.3 |
| 9 | 80.3 | 83.1 |
| 10 | 62.9 | 89.4 |
| 11 | 90.9 | 93.7 |
| 12 | 83.0 | 89.9 |
| **Average** | **86.7** | **93.2** |

- Original HBS data generally underestimates consumption vs **National Accounts (NA)** for France: weighted average of aggregate expense shares = **74.8%**. Only COICOP level-1 groups deemed severely underreported (>30%): **CP02, CP06 and CP11**.
- The matching process adds further underestimation of NA coverage vs original HBS (**72.1%**). Severe underreporting persists for the three categories (worsening for CP02, similar for CP06 and CP11), plus **CP09**, when comparing HBS-matched-to-SILC vs NA.
- Matched SILC/HBS rates are in the acceptable range **83.1%–120.3%** for all COICOP level-1 categories except CP02. At 3-digit COICOP level the matching performs well, with no deviations larger than 30%.

### 4. Validation

Accuracy of EUROMOD estimates is assessed for four categories of indicators, against readily available official statistics for **2022–2025**:

1. (Non-simulated) market incomes in the input dataset;
2. Simulated taxes and social security contributions;
3. Simulated benefits;
4. Simulated indicators of income distribution.

Unlike the previous Country Report ("France 2021-2024"), baseline simulations for 2022–2025 system years use **two datasets: the 2024 dataset for the 2023–2025 policy systems, and the 2023 dataset for the 2022 policy system**.

#### 4.1 Aggregate validation

EUROMOD's disposable income differs slightly from SILC's: EUROMOD **adds income from private pension plans**, **disregards tax adjustment repayments** (taxes/benefits are computed "exactly" via simulation), and **does not add the value of the company car**.

##### 4.1.1 Components of disposable income

**Table 4.1 Definitions of disposable income in EU-SILC and EUROMOD** (EUROMOD = ils_dispy; EU-SILC = HY020; 0 = the income concept does not enter the calculation; source: own elaboration):

| Income component | EUROMOD (ils_dispy) | EU-SILC (HY020) |
|---|---|---|
| Employee cash or near cash income | + | + |
| Employer's social insurance contribution | 0 | 0 |
| Contributions to individual private pension plans | 0 | 0 |
| Cash benefits or losses from self-employment | + | + |
| Pension from individual private plans | + | 0 |
| Unemployment benefits | + | + |
| Old-age benefits | + | + |
| Survivor' benefits | + | + |
| Sickness benefits | + | + |
| Disability benefits | + | + |
| Education-related allowances | + | + |
| Income from rental of a property or land | + | + |
| Family/children related allowances | + | + |
| Social exclusion not elsewhere classified | + | + |
| Housing benefits | + | + |
| Regular inter-household cash transfer received | + | + |
| Interests, dividends, etc. | + | + |
| Income received by people aged under 16 | + | + |
| Regular taxes on wealth | - | - |
| Regular inter-household cash transfer paid | - | - |
| Tax on income and social contributions | - | - |
| Repayments/receipts for tax adjustment | 0 | + |
| Company car | 0 | + |

##### 4.1.2 Validation of incomes (vs external administrative data — Annex 3 tables)

**Recipients of original incomes (Table A3.1):** EUROMOD counts anyone with some employment/self-employment income over the year, while external data record numbers at a point in time (31 December), so EUROMOD figures should be slightly higher. Indeed:
- Number of **employment income** recipients ~**12% higher** in EUROMOD than the external benchmark in 2024.
- **Self-employment income** recipients **underestimated by ~15%** in EUROMOD in 2023 (year of the last available external values).

**Amounts of original incomes (Table A3.2, EU-SILC 2024, income reference 2023):**
- **Total employment income underestimated in SILC** vs external statistics — possibly SILC's inability to capture high earners.
- **Total self-employment income underestimated**, as are **investment income** and **income from public pensions** — possibly also a mismatch between external statistics and EU-SILC concepts.
- Note: the contribution on investment income changed in France — a significant portion of investment income from productive investments was removed from taxation; taxation is now largely focused on real estate assets and moved to **IFI (Impôt sur la fortune immobilière)**.

Not all benefits and taxes are simulated; where reliable simulation is not possible, components are taken directly from the micro-data.

**Taxes and SIC — number of payers (Table A3.3):**
- Number of tax households slightly **underestimated by ~4% in 2022**, possibly because external values cover whole France (with overseas) while EUROMOD covers metropolitan France.

**Taxes and SIC — amounts (Table A3.4):**
- **Income tax underestimated by 6% in 2022 and by 2% in 2023** (no external values yet for 2024).
- **CSG and CRDS** (the two taxes specific to the French system) **underestimated by 5% in 2024** in EUROMOD.
- Simulated personal income tax revenues are generally more or less in line with external statistics, but France has a range of complex tax deductions/credits that cannot all be simulated — the most important ones simulated relate to **rental income, dividends, overtime pay and childcare**; deductions particularly important for high incomes are likely missed. Also, some market income components (earnings, investment & property) are underreported in the data vs external statistics.

**Benefits — number of recipients (Table A3.5, EUROMOD baseline and EU-SILC vs external administrative information):**
- **Old-age pensioners**: accurately captured, minor **underestimation of 4% in 2023**.
- **Survivor and disability pensioners**: **significantly overestimated** — probably because external data use an overly restrictive definition of disability and miss a significant share of individuals eligible in EUROMOD.
- **Universal child benefit**: number of recipients accurately estimated.
- **Means-tested educational allowance, family support allowance, means-tested benefit for young children, means-tested birth grant**: **underestimated**. Family support underestimation likely due to the low number of recipients in the original SILC database (possibly also for other low-beneficiary benefits); lack of information on alimony payments may also contribute.
- **RSA (guaranteed minimum income)**: quite well estimated, considering the applied **non-take-up adjustment**; EUROMOD slightly **overestimates recipients by 8% in 2024** — due to external statistics covering all French territories vs metropolitan France in EUROMOD.
- **Activity allowance**: well estimated in 2023, **overestimated by 12% in 2024**.
- **Contributory unemployment benefit**: number of recipients **overestimated** — entirely due to observed receipt in SILC (EUROMOD eligibility is constructed to reproduce observed receipt; simulated numbers and data-derived numbers are very close). Since SILC aggregates contributory and means-tested unemployment benefits, disaggregation errors may drive the overestimation.

**Benefits — amounts (Table A3.6):**
- **Survivor benefits clearly overestimated** in EUROMOD.
- **Old-age pensions, disability pensions and universal child benefits: quite well estimated.**
- **Sickness benefits significantly underestimated** — note the EUROMOD variable contains more benefits than the external benchmarks (child disability, adoption, parental care etc.); it was not possible to reconstitute the EUROMOD variable exactly from external administrative data.
- **RSA amounts (including non-take-up adjustment) underestimated by 14% in 2024** — households entitled to small amounts are less likely to claim.
- **Total spending on contributory unemployment benefits overestimated by 13% in 2023**, as is the activity allowance, which is clearly overestimated.

##### 4.1.3 Validation of outputted (simulated) expenses

Two comparison types: (1) simulated household consumption expenditures vs **National Accounts (NA)** of the same year; (2) simulated consumption taxes (based on NA-adjusted simulated expenditures) vs administrative data on consumption tax revenues.

- **Table A3.9** (top): expenditures aggregated from EUROMOD vs NA external statistics as reported by **EUROSTAT**. COICOP level-1 categories are under-reported already in the French HBS, especially **02 Alcoholic beverages, tobacco, etc.** and **06 Health**, so aggregated simulated values are also under-simulated w.r.t. NA. **There is a break in the Excises series from NA in 2024**, hence external values are not included that year.
- Table A3.9 (second part): aggregate revenues from consumption taxes (VAT and excises) vs EUROSTAT external statistics; bottom part shows simulated aggregate revenue for categories of interest (alcoholic drinks, tobacco, energy products). **In France both VAT and excise revenues are undersimulated; the simulation captures less than half of the revenue from consumption taxes** (before calibration). Consumption taxes on specific items are significantly underestimated. Partly because survey data rely on declared consumption which may differ from actual consumption (people misreport how much they smoke and drink).
- To correct this, EUROMOD provides **NA-adjusted consumption aggregates**: the calibration factor is the ratio between NA aggregated expenditures and EM aggregated simulated expenditures at COICOP level 1 at baseline; NA adjustment scales up (or down) consumption and tax liabilities of all individuals.
- **Table A3.10** (after NA calibration): consumption tax revenues simulated for private households in **2024 sum to 134,337 million euros for VAT and 27,576 million euros for excises**. About **65% of aggregate VAT revenues** are captured in 2024; **58% of excise revenue** after calibration in 2023 (2024 external values not mentioned due to the series break). Main reason for remaining gaps: several groups paying significant VAT are not covered in HBS — government and third sector, hospitals, business enterprises such as financial companies (VAT-exempt but paying input VAT), and private households not covered by HBS (people in dormitories, jails, or retirement homes). At lower COICOP details, calibration improves estimates but some differences vs official statistics remain higher than 50%.

#### 4.2 Income distribution

All income distribution results are computed for individuals according to household disposable income (HDI) equivalised by the **"modified OECD" equivalence scale** (first adult = 1; additional people aged 14+ = 0.5; additional people aged under 14 = 0.3). HDI = sum of all income sources of all household members net of income tax and social insurance contributions.

##### 4.2.1 Income inequality (Table A3.7, external figures from EUROSTAT's statistics database)

- **Median and mean disposable incomes** rather well aligned in 2022 and 2023, with a very slight underestimation (**2 or 3%**).
- **Gini coefficient and S80/S20 ratio**: overall inequality **slightly underestimated** in EUROMOD where information is available.
- **Decile shares**: well aligned for **D3 to D10**; the bottom of the distribution is **overestimated ~18% for D1 and 4% for D2 in 2023 (respectively 20 and 4% in 2022)**.
- Possible explanations: (1) no adjustments to socio-demographic variables when policy year ≠ data year (no adjustment for employment/unemployment changes); (2) uprating factors based on changes in *average* income components may not capture distributional change — if incomes rise faster at the top, inequality increases without being captured in averages.

##### 4.2.2 Poverty rates (Table A3.8)

- At-risk-of-poverty rates shown for various thresholds, in total and by gender, and by age group for the **60% of median** threshold.
- **Poverty is underestimated in EUROMOD, for men and women, at lower poverty thresholds**; with higher thresholds EUROMOD rates are closer to external benchmarks.
- Interpretation: non-take-up of some means-tested benefits, or administrative errors in their implementation, may play a role EUROMOD cannot capture. Only non-take-up of general social assistance (**RSA, Activity allowance**) is simulated, and it is simulated to be **random**. If marginalized, peripheral groups are less likely to claim benefits to which they are theoretically entitled, incomes at the bottom will be inflated in EUROMOD.

#### 4.3 Summary of "health warnings"

Things to keep in mind when interpreting EUROMOD results (full list):

- **Employment income appears to be underreported in SILC** compared to external benchmarks.
- Similarly, some other income types — **sickness benefits, investment and property incomes** — are lower in SILC than external information.
- **Accurate simulation of the parental leave benefit (CLCA) was not possible** given available information in SILC; however, both amounts and recipient numbers appear close to external statistics.
- **Non-take-up of the main social assistance benefits (RSA, activity allowance) is simulated to be random**; non-take-up is most likely non-random — comparisons with external benchmarks suggest households entitled to lower amounts are less likely to claim.
- **Simulation of eligibility for the contributory unemployment insurance benefit (ARE) is inaccurate** due to the quality of data in SILC.
- **Eligibility for ASPA (means-tested solidarity allowance for the elderly) and ASS (means-tested unemployment assistance) is simulated based on observed receipt in the data.**
- Overall, **inequality based on EUROMOD simulated incomes is lower**; **poverty rates, especially at low poverty thresholds, are underestimated**.
- The simulation of **monetary compensation schemes** is triggered by simulated labour market transitions defined in policy **TransLMA_cc**, operational only with the **LMA add-on**; these simulations are only partially validated — users should consult "Simulating labour market transitions in EUROMOD" before use.
- **Labour market transitions are switched OFF in EUROMOD baselines**, so monetary compensation schemes have no effect in baseline simulations. Since all policies not linked to labour market transitions are fully functional, disposable income in 2020 can be higher than in previous years.
- The simulation of **consumption taxes** sensitively depends on the quality of the match of the extended EUROMOD files, the frequency of the data, and the gaps between input data files and policy systems. The most recent HBS data available for all countries (EU-HBS) is **2015**.
- When the user runs a policy system year (e.g. 2025) that does not coincide with the incomes in the SILC data used (e.g. 2024 data with 2023 incomes), expenditures are simulated under the **constant income shares assumption** (by default): income shares of expenditure in the extended input files are not updated and remain constant regardless of the policy system. A household spending 10% of its income on food (sum of all xs_1* variables = 0.10) will still spend 10% in 2025, regardless of income changes driven by uprating factors and tax-benefit changes. **This implicitly assumes an income elasticity of one.**

---

## 9. Annex: uprating factors & policy effects (CR pages 157-166)

Source: EUROMOD Country Report France (Y16_CR_FR.pdf), Annex 1 (Uprating Factors, PDF pages 158-163, printed pages 156-161) and Annex 2 (Policy Effects in 2024-2025, PDF pages 164-167, printed pages 162-165). Annex 3 (Validation Tables) begins on PDF page 168.

### Annex 1. Uprating Factors (Table A1.1)

Uprating factors are the non-legislative indices EUROMOD uses to update monetary variables from the data year to each simulated policy year (2022-2025). Each row gives the income component uprated, the EUROMOD factor name (`$f_...`), the index values for 2022-2025, and the exact statistical source.

#### Price and macroeconomic indices

| Income component | Factor name | 2022 | 2023 | 2024 | 2025 | Source |
|---|---|---|---|---|---|---|
| Harmonized Indices of Consumer Prices (HICP) | `$f_hicp` | 114.04 | 120.5 | 123.29 | 124.40 | Eurostat / HICP (2015=100), monthly data (prc_hicp_midx), http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=prc_hicp_midx&lang=en ; EUROSTAT; AMECO Autumn forecast for 2022 values |
| Harmonized Indices of Consumer Prices (HICP) | `$f_hicp` | 131.89 | 139.35 | 142.58 | 143.92 | Eurostat / HICP (2005=100), monthly data (prc_hicp_midx), same Eurostat dataset link |
| Inflation rate (from INSEE) | `$f_cpi` | 112.09 | 117.60 | 119.93 | 119.84 | INSEE IdBank 0001765178, http://www.bdm.insee.fr/bdm2/affichageSeries?idbank=001765178&bouton=OK&codeGroupe=1743 |
| Annual national accounts - GDP current price | `$f_gdp` | 2 545 145 | 2 581 775 | 2 612 510 | 2 628 185 | INSEE IdBank 001690355; 2016 & 2017 GDP based on forecasted GDP growth (https://ec.europa.eu/info/sites/info/files/wf2017_statistical_annex_0.pdf) |

#### Earnings indices

| Income component | Factor name | 2022 | 2023 | 2024 | 2025 | Source |
|---|---|---|---|---|---|---|
| Average annual net full-time equivalent salary - All salaried workers | `$f_yem` | 30 718 | 31 902 | 32 885 | 33 743 | INSEE IdBank 001665118 (bdm.insee.fr series, codeGroupe=1475) |
| Average annual net FTE salary - First quartile | `$f_yem_q1` | 19 422 | 20 368 | 20 996 | 21 543 | INSEE IdBank (bdm.insee.fr series, codeGroupe=1476, idbanks 001665118-001665148) |
| Average annual net FTE salary - Second quartile | `$f_yem_q2` | 24 515 | 25 569 | 26 357 | 27 044 | INSEE IdBank 001665127 (bdm.insee.fr series, codeGroupe=1476) |
| Average annual net FTE salary - Third quartile | `$f_yem_q3` | 33 797 | 35 147 | 36 230 | 37 175 | INSEE IdBank 001665130 (bdm.insee.fr series, codeGroupe=1476) |
| Gross wages and salaries (totals from AMECO) | `$f_yem_Ameco` | 1061.3 | 1116.1 | 1150.5 | 1180.50 | DG ECFIN/AMECO, household and NPISH / revenue / gross wages and salaries (Mrd euros), http://ec.europa.eu/economy_finance/ameco/user/serie/ResultSerie.cfm |
| Average net full-time salary in the PREVIOUS year | `$f_yempv` | 29 569 | 30 718 | 31 902 | 32 885 | INSEE IdBank 001665118 |
| Average disposable income (per hh) | `$f_yds` | 44 718 | 47 027 | 48 477 | 49 741 | INSEE, https://www.insee.fr/fr/statistiques/2412465#tableau-Donnes |
| Change in average investment and property income (2006=base) | `$f_yiy` | 1.173 | 1.190 | 1.204 | 1.211 | "Revenu de la propriété reçus diminués des revenus versés", http://www.insee.fr/fr/ffc/docs_ffc/ref/revpmen11h.pdf |

#### Pensions and housing indices

| Income component | Factor name | 2022 | 2023 | 2024 | 2025 | Source |
|---|---|---|---|---|---|---|
| Rent reference index (RRI), base 100 on the 4th quarter of 1998 | `$f_rri` | 135.82 | 140.57 | 144.45 | 145.98 | INSEE IdBank 001515333, http://www.insee.fr/en/bases-de-donnees/bsweb/serie.asp?idbank=001515333 |
| Monthly average amount per retired person | `$f_poa` | 1626 | 1666 | 1754.30 | 1792.89 | INSEE (http://www.insee.fr/fr/themes/tableau.asp?reg_id=0&ref_id=NATTEF04571) and DREES "Les retraités et les retraites" édition 2017 |
| Pension indexation rules | `$f_poa_index` | 105.92 (see note) | 106.77 | 112.42 | 114.9 | INSEE IdBank 0001765178 |

Footnote to `$f_poa_index` 2022 value: "Reflects the increase on pensions on July 1st by 4% on July 1: (103.8419448*1.04+103.8419448)/2=105.9188".

#### Benefit base amounts (used to uprate specific benefits)

| Income component | Factor name | 2022 | 2023 | 2024 | 2025 | Source |
|---|---|---|---|---|---|---|
| Monthly base for family benefits (BMAF) | `$f_bfa` | 428.86 | 444.24 | 466.44 | 474.37 | http://www.dalloz-actualite.fr/indice/base-mensuelle-de-calcul-des-prestations-familiales.VSfD45PK-AB |
| Basic AF amount | `$f_bch00` | 136.55 | 141.45 | 146.89 | 151.05 | https://www.caf.fr/allocataires/aides-et-demarches/droits-et-prestations |
| Basic CF amount | `$f_bchlg` | 177.73 | 183.41 | 190.95 | 196.59 | caf.fr (same page) |
| Basic PAJE amount | `$f_bchyc` | 184.62 | 184.62 | 184.62 | 184.62 | caf.fr (same page) |
| Basic ARS amount | `$f_bched` | 382.85 | 396.58 | 416.4 | 423.46 | caf.fr (same page) |
| Basic Baby Bonus amount | `$f_bchba` | 985.30 | 1020.66 | 1066.31 | 1084.44 | caf.fr (same page) |
| Basic BMAF amount | `$f_bchot` | 428.86 | 444.24 | 466.44 | 474.37 | caf.fr (same page) |
| Maximum amount of AAH | `$f_bdi` | 934.19 | 967.69 | 1016.05 | 1033.32 | caf.fr (same page) |
| Basic AV amount (widow/er allowance) | `$f_bsuwd` | 644.80 | 662.7 | 697.82 | 713.17 | caf.fr (same page) |
| Basic RSA amount | `$f_bsa00` | 584.48 | 605.45 | 628.71 | 646.52 | caf.fr (same page) |
| Basic Activity allowance | `$f_bsawk` | 575.33 | 595.97 | 622.63 | 633.21 | caf.fr (same page) |
| Basic ASPA amount | `$f_bsaoa` | 935.11 | 961.08 | 1012.02 | 1034.28 | caf.fr (same page) |
| Rent reference level for AL (housing benefits) | `$f_bho` | 264.05 | 268.87 | 278.28 | 290.34 | caf.fr (same page) |
| Basic daily rate for ASS | `$f_bunmt` | 17.55 | 18.17 | 19 | 19.33 | Based on the ASS daily amount |

#### Tax aggregates (totals collected, used to uprate/calibrate taxes)

| Income component | Factor name | 2022 | 2023 | 2024 | 2025 | Source |
|---|---|---|---|---|---|---|
| Total amount of ISF collected (billions) | `$f_twl` | 2.3 | 2.3 | 2.7 | 2.73 | Based on total ISF (Impôt de solidarité sur la fortune) collected: https://www.insee.fr/fr/statistiques/2381408#tableau-Donnes |
| Total amount of TF collected (billions) | `$f_tpr` | 37.3 | 41.1 | 42.90 | 43.30 | Based on total TF (taxe foncière) collected, same INSEE page |
| Total amount of TH collected (billions) | `$f_tmu` | 5.5 | 2.80 | 3.30 | 3.33 | Based on total TH (taxe d'habitation) collected, same INSEE page |
| Total amount of IRPP collected (billions) | `$f_tin` | 95.99 | 96.89 | 96.16 | 97.06 | Based on total amount of IRPP, https://www.insee.fr/fr/statistiques/2381408#tableau-Donnes |

#### Average hourly wages by industry (lindi), units of national currency

All rows sourced identically: "Computed from ESTAT tables nama_10_a64 (wages) and nama_10_a64_e (hours worked) up to 2019. The values for 2020-2024 are computed by multiplying the value of the previous year by the yearly increase of nominal compensation per employee, total economy, from AMECO." (The lindi=11 row says "values for 2020-2022" in the PDF.)

| Industry (lindi code) | Factor name | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Agriculture and Fishing (lindi = 1) | `$f_hourly_wage_lindi_1` | 16.8367 | 17.1645 | 17.2893 | 17.7228 |
| Mining, Manufacturing and Utilities (lindi = 2) | `$f_hourly_wage_lindi_2` | 28.6321 | 29.6895 | 30.5480 | 31.3140 |
| Construction (lindi = 3) | `$f_hourly_wage_lindi_3` | 26.8433 | 27.6572 | 28.2679 | 28.9768 |
| Wholesale and retail (lindi = 4) | `$f_hourly_wage_lindi_4` | 24.6772 | 25.6197 | 26.0859 | 26.7400 |
| Hotels and restaurants (lindi = 5) | `$f_hourly_wage_lindi_5` | 20.5063 | 21.2506 | 21.6856 | 22.2293 |
| Transport and communication (lindi = 6) | `$f_hourly_wage_lindi_6` | 31.8097 | 32.9733 | 33.7552 | 34.6017 |
| Financial intermediation (lindi = 7) | `$f_hourly_wage_lindi_7` | 37.4448 | 39.1927 | 40.0965 | 41.1019 |
| Real estate and business (lindi = 8) | `$f_hourly_wage_lindi_8` | 29.0849 | 30.0963 | 30.7867 | 31.5587 |
| Public administration and defence (lindi = 9) | `$f_hourly_wage_lindi_9` | 26.3975 | 27.3379 | 27.9863 | 28.688 |
| Education (lindi = 10) | `$f_hourly_wage_lindi_10` | 31.6877 | 33.1393 | 33.7568 | 34.6032 |
| Health and social work (lindi = 11) | `$f_hourly_wage_lindi_11` | 24.758 | 26.1189 | 26.753 | 27.4239 |
| Other (lindi = 12) | `$f_hourly_wage_lindi_12` | 22.6167 | 23.4225 | 23.6789 | 24.2726 |
| Average hourly wages (total wages / total hours) | `$f_hourly_wage` | 27.3475 | 28.413 | 29.0428 | 29.7711 |

### Annex 2. Policy Effects in 2024-2025

#### Methodology

- Table A2.1 and Figure A2.1 show changes in mean equivalised household disposable income induced by policy changes between 2024 and 2025, by income component and income decile group.
- The effect is the difference between equivalised household disposable income under 2025 tax-benefit policies (deflating monetary parameters by projected Eurostat's Harmonized Index of Consumer Prices, HICP, available in autumn 2025) and that simulated under 2024 policies, as a percentage of mean equivalised household disposable income in 2024.
- Results are interpreted in real terms (CPI-indexation with CPI = 1.0091, i.e. HICP growth of about 1% in 2025); Table A2.2 gives the same effects in nominal terms.
- Income decile groups are based on equivalised household disposable income in 2023, using the modified OECD equivalence scale. Each policy system is applied to the same input data.
- Source: Own elaboration using the Policy Effects tool embedded in EUROMOD.

#### Main findings (real terms)

- HICP growth was milder in 2025 (equal to 1%) than in previous years, so the 2025 policy changes more than compensated the inflation erosion, leading to an increase of 0.44% of households' disposable income; the bottom income deciles recorded the greatest increases (0.78% in the first two deciles and 0.81% for the third).
- Largest contributions: increase in public pensions (+0.31% of total disposable income), means-tested benefits (+0.09%), and non-means-tested benefits (+0.03%). The increase in income tax brackets (+1.8%) led to a slight reduction in direct taxes and added +0.02% to disposable income.
- Compensating measures for inflation: minimum wage +2%, PSS +1.6%, social benefits +1.7% (April increase), pensions +2.2%, housing benefits +1.04%, unemployment benefit +0.5%.
- Distribution: gains for all deciles, larger at the bottom (+0.78% D1-D2, +0.81% D3); smallest for D9 (+0.35%) and D10 (+0.16%).
- Public pensions: revalued by 2.2% from January 2025, above inflation. Contribution to disposable income ranges from +0.18% (D1) to +0.16% (D10); D2-D7 most affected (+0.35 to +0.44%, maximum +0.44% for D3); +0.31% for D8 and +0.30% for D9.
- Means-tested benefits: strongest for the poorest (+0.52% D1, +0.27% D2, +0.20% D3, +0.18% D4), declining to +0.08% (D5-D6), +0.06% (D7), +0.03% (D8), +0.02% (D9), +0.01% (D10).
- Non-means-tested benefits: greater positive impact on the lowest deciles (+0.07% D1 vs +0.01% D10). The low inflation indexation of unemployment benefit (+0.5% in 2025) and the reduced duration of indemnisation for jobseekers aged 53 and over may explain the modest gains at the bottom.
- SIC: stability of employee SIC and self-employed SIC has no impact on disposable income. The reduction of the ceiling for daily sickness benefits (which reduces the remuneration used to calculate the sickness daily allowance) appears to have a low impact or to be absorbed by other measures.
- Direct taxes: reduced for all deciles except D10 (about -0.01% of disposable income): +0.01 for D1, +0.10 for D2, +0.14 for D3. Unlike 2024 (when direct-tax gains concentrated in higher deciles), the exceptional differential tax on high incomes removes most of the advantage for top deciles (roughly +0.01% for D7-D9, slightly negative for D10).

#### Table A2.1 Policy effects in France in 2024-2025, using the CPI-indexation (CPI = 1.0091), %

| Decile | Original income | Public pensions | Means-tested benefits | Non means-tested benefits | Employee SIC | Self-employed SIC | Other SIC | Direct taxes | Disposable income |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00 | 0.18 | 0.52 | 0.07 | 0.00 | 0.00 | 0.00 | 0.01 | 0.78 |
| 2 | 0.00 | 0.35 | 0.27 | 0.06 | 0.00 | 0.00 | 0.00 | 0.10 | 0.78 |
| 3 | 0.00 | 0.44 | 0.20 | 0.03 | 0.00 | 0.00 | 0.00 | 0.14 | 0.81 |
| 4 | 0.00 | 0.40 | 0.18 | 0.02 | 0.00 | 0.00 | 0.00 | 0.00 | 0.59 |
| 5 | 0.00 | 0.42 | 0.08 | 0.02 | 0.00 | 0.00 | 0.00 | 0.03 | 0.55 |
| 6 | 0.00 | 0.40 | 0.08 | 0.02 | 0.00 | 0.00 | 0.00 | 0.06 | 0.55 |
| 7 | 0.00 | 0.35 | 0.06 | 0.03 | 0.00 | 0.00 | 0.00 | 0.01 | 0.44 |
| 8 | 0.00 | 0.31 | 0.03 | 0.06 | 0.00 | 0.00 | 0.00 | 0.00 | 0.40 |
| 9 | 0.00 | 0.30 | 0.02 | 0.03 | 0.00 | 0.00 | 0.00 | 0.01 | 0.35 |
| 10 | 0.00 | 0.16 | 0.01 | 0.01 | 0.00 | 0.00 | 0.00 | -0.01 | 0.16 |
| Total | 0.00 | 0.31 | 0.09 | 0.03 | 0.00 | 0.00 | 0.00 | 0.02 | 0.44 |

Notes: Shown as a percentage change in mean equivalised household disposable income by income component and income decile group. Income decile groups are based on equivalised household disposable income in 2023, using the modified OECD equivalence scale. Each policy system has been applied to the same input data, deflating monetary parameters of 2024 policies by Eurostat's Harmonized Index of Consumer Prices (HICP). Source: Own elaboration using the Policy Effects tool embedded in EUROMOD.

#### Table A2.2 Policy effects in France in 2024-2025 (Nominal terms)

| Decile | Original income | Public pensions | Means-tested benefits | Non means-tested benefits | Employee SIC | Self-employed SIC | Other SIC | Direct taxes | Disposable income |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00 | 0.31 | 0.98 | 0.16 | 0.00 | -0.01 | 0.00 | -0.03 | 1.41 |
| 2 | 0.00 | 0.61 | 0.58 | 0.12 | 0.00 | 0.00 | 0.00 | 0.07 | 1.38 |
| 3 | 0.00 | 0.76 | 0.45 | 0.07 | 0.00 | 0.00 | 0.00 | 0.10 | 1.38 |
| 4 | 0.00 | 0.69 | 0.38 | 0.05 | 0.00 | 0.00 | 0.00 | -0.04 | 1.08 |
| 5 | 0.00 | 0.73 | 0.19 | 0.04 | 0.00 | 0.00 | 0.00 | 0.00 | 0.96 |
| 6 | 0.00 | 0.69 | 0.13 | 0.04 | 0.00 | 0.00 | 0.00 | 0.04 | 0.89 |
| 7 | 0.00 | 0.60 | 0.11 | 0.04 | 0.00 | 0.00 | 0.00 | 0.01 | 0.76 |
| 8 | 0.00 | 0.54 | 0.06 | 0.07 | 0.00 | 0.00 | 0.00 | 0.01 | 0.67 |
| 9 | 0.00 | 0.52 | 0.03 | 0.04 | 0.00 | -0.01 | 0.00 | 0.04 | 0.62 |
| 10 | 0.00 | 0.28 | 0.01 | 0.01 | -0.01 | -0.01 | 0.00 | 0.09 | 0.37 |
| Total | 0.00 | 0.53 | 0.18 | 0.05 | 0.00 | 0.00 | 0.00 | 0.04 | 0.79 |

Source: Own elaboration using the Policy Effects tool embedded in EUROMOD.

Figures A2.1 (CPI-indexed) and A2.2 (nominal) plot the same decomposition by decile (change in mean disposable income, %, y-axis range roughly -0.1 to 1.5) with series for public pensions, means-tested benefits, non means-tested benefits and employee SIC.

The erosion of inflation on the real value of the increase in social benefits is verified by comparing Table A2.1 (real terms) and Table A2.2 (nominal terms): e.g. total effect 0.44% real vs 0.79% nominal.

---

