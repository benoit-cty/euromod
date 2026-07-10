ESRI working papers represent un-refereed work-in-progress by researchers who are solely responsible for the 
content and any views expressed therein. Any comments on these papers will be welcome and should be sent to the 
author(s) by email. Papers may be downloaded for personal use only. 
ESRI Working Paper No. 750
May 2023
The trouble with take-up
Karina Doorleya,b,c* & Theano Kakoulidoua,b
a) Economic and Social Research Institute, Dublin, Ireland
b) Department of Economics, Trinity College Dublin, Dublin, Ireland
c) Institute of Labor Economics, Bonn, Germany
*Corresponding Author:
Dr Karina Doorley
Economic and Social Research Institute,
Whitaker Square, Sir John Rogerson’s Quay,
Dublin, Ireland
Email: Karina.Doorley@esri.ie
Acknowledgements:
We would like to thank Sharon Farrell and Seamus O’Malley for excellent research assistance. This work was carried out 
with funding from the ESRI’s Tax, Welfare and Pensions Research Programme (supported by the Department of Public 
Expenditure and Reform, the Department of Social Protection, the Department of Health, the Department of Children and 
Youth Affairs and the Department of Finance), which is gratefully acknowledged. The results presented here are based on 
the ESRI’s tax-benefit model, SWITCH version 5.3 which makes use of the EUROMOD platform, as well as EUROMOD 
version I4.109+. Originally maintained, developed and managed by the Institute for Social and Economic Research (ISER), 
since 2021 EUROMOD is maintained, developed and managed by the Joint Research Centre (JRC) of the European 
Commission, in collaboration with EUROSTAT and national teams from the EU countries. We are indebted to the many 
people who have contributed to the development of EUROMOD. The results and their interpretation are the authors’ 
responsibility. 


Take-up of social welfare is key to its success in alleviating poverty. For a variety 
of reasons, including stigma, transaction costs and information asymmetry, take-
up of welfare benefits is imperfect. This research note discusses the issue of 
take-up of social welfare and its measurement. We explore the 
difficulties of estimating welfare take-up, using the example of the Irish 
Working Family Payment (WFP) and two microsimulation models. We show 
how estimates of take-up can vary depending on the dataset used for 
simulation. We then estimate take-up of the WFP, updating the most recent 
estimate from 2005. Lastly, we discuss policy lessons.


Introduction 
Take-up of social welfare is key to its success in alleviating poverty. For a variety of reasons, 
including stigma, transaction costs and information asymmetry, take-up of welfare benefits is 
imperfect. The level of take-up is strongly correlated with how universal the payment is. Age-
related benefits or universal child related benefits tend to have relatively high take-up rates. 
Benefits with complicated eligibility criteria and which are means tested tend to have much 
lower take-up rates.  
In-work benefits such as the Earned Income Tax Credit in the US, the former Working Tax 
Credit in the U.K. and the Working Family Payment in Ireland are important anti-poverty tools. 
They both encourage work and increase the incomes of those at work on low pay. These 
payments tend to suffer from a high rate of non-take-up which is linked both to their complexity 
and to their expected value to recipient households (Bruckmeier & Wiemers, 2012; Bhargava 
& Manoli, 2015; Tempelman & Houkes-Hommes, 2016).2 Understanding the reasons for and 
patterns of non-take-up is important if policy-makers wish to fully exploit these instruments to 
encourage work and reduce in-work poverty. 
Estimating non-take-up of in-work (and other) benefits is often carried out using a tax and 
benefit microsimulation model which simulates the entire income distribution based on survey 
data linked to tax-benefit rules. Comparing simulated eligibility, as estimated by a 
microsimulation model, to actual receipt of the benefit, reported in the underlying survey or 
administrative data, allows researchers to estimate the take-up rate.  
This analysis is often complicated by the limitations of the data underlying widely used 
microsimulation models, such as EUROMOD, the harmonised EU tax-benefit model. In this 
note, we explore the difficulties of estimating welfare take-up, using the example of the Irish 
Working Family Payment (WFP) and two microsimulation models. We show how estimates 
of take-up can vary depending on the dataset used for simulation. We then estimate take-up of 
the WFP, updating the most recent estimate from 2005. Lastly, we discuss policy lessons.  
2 Recent research by Martin et al (2022) indicates that the administrative burden associated with government 
benefits is particularly high compared to other forms of administrative burdens. 


1. Modelling take-up of the Working Family Payment 
The WFP was first introduced as the Family Income Supplement in 1984 in a bid to alleviate 
financial strain on the working poor and increase the incentive to work. It has evolved since 
then, increasing in generosity and undergoing a name change that sought to increase its 
visibility as a payment for working families in 2018. The application process recently moved 
from paper to online and employers no longer need to countersign applications. It is available 
to families with at least one child where the parent or parents are working as employees at least 
38 hours per fortnight. In 2022, the income limit for a family with one child was €551 per week 
(for reference, average weekly earnings for 2022 are €874)3 and the taper rate of the payment 
is 60%. The income limit increases for each subsequent child. Denoting 𝐵𝐵 the income limit and 
𝑌𝑌 the families’ weekly reckonable income:4 
𝑊𝑊𝑊𝑊𝑊𝑊= max {0, 60%(𝐵𝐵−𝑌𝑌)} 
A minimum rate of €20 per week is paid to eligible families. Early estimates of take-up of the 
WFP ranged from 20-40% with the most recent estimate of 20-30% (depending on the 
calculation method) dating from 2005 (Callan and Keane, 2008). While the definition of low 
take-up is debatable, Hernandez et al (2004) considered take-up rates of as low as 68% in the 
UK, a “significant problem” and estimated take-up rates of means-tested social assistance in 
the Netherlands, Germany, France, the UK and US at between 40% and 80%. This puts the 
most recent estimate of WFP take-up at the very bottom of those recently estimated in other 
OECD countries. 
Estimating take-up rates of means-tested social assistance requires comparing receipt to 
entitlement. This typically requires the use of a microsimulation model to estimate eligibility, 
based on household level information from a survey dataset linked to the rules of the tax-benefit 
system. This simulated eligibility must then be compared to receipt, as reported in the survey 
dataset. This process is complicated by two main methodological problems. First, receipt of 
 
3 CSO Table EHQ03 https://data.cso.ie/table/EHQ03 
4 The family’s weekly reckonable income includes the employment and self-employment income of the couple 
(excluding income tax, social security contribution, and pension savings), as well as income from occupational 
pensions, social welfare payments, student grants, carer’s payments, and rental income. A number of social 
welfare payments are not included in reckonable income the most important of them being: child benefit, 
guardian’s payment, supplementary welfare allowance, domiciliary care allowance, foster child allowance, rent 
allowance and supplement, fuel allowance and children’s income. A more detailed list of what counts as 
reckonable 
income 
can 
be 
found 
https://www.citizensinformation.ie/en/social_welfare/social_welfare_payments/social_welfare_payments_to
_families_and_children/family_income_supplement.html.  


social welfare payments in survey data is often self-reported. There is a well-documented 
under-reporting of social welfare receipt in survey data, which tends to be at least partly 
attributed to associated stigma (Moffit, 2003; Bargain et al, 2012; Ko and Moffit, 2022). 
Second, receipt of social welfare is often reported for an income reference period (such as the 
preceding tax or calendar year) which does not correspond to the period in which other relevant 
information for the simulation process – such as hours of work, number of children, etc – is 
collected.  
EUROMOD and SWITCH are microsimulation models for Ireland which use the same 
platform and interface, but which are linked to different datasets.5 EUROMOD is linked to EU-
SILC data which contains information on income and welfare receipt from the calendar year 
preceding the survey. SWITCH is linked to the SILC Research Microdata File (RMF) which 
is matched to administrative information from the Department of Social Protection and 
Revenue Commissioners on welfare receipt and income for the current month, i.e. the month 
in which the survey took place. This makes SWITCH more suitable to estimating take-up as 
(i) it does not rely on self-reported receipt of social welfare and (ii) the welfare payment and 
other income information relates to the same period as the demographic information needed to 
simulate eligibility. 
Table 1 compares simulations of WFP eligibility - using the two models - to reported receipt 
in the datasets underlying the models. We report two sets of results for the EUROMOD 
simulations, the first links the 2019 policy to 2019 EU-SILC data while the second links the 
2018 policy to the 2019 EU-SILC data (thus aligning the policy rules with the income reference 
period, but not with the other survey variables). The number of households in receipt of and 
eligible for the WFP in both underlying datasets are small. For this reason, a detailed 
econometric analysis of the characteristics of those who take-up the payment is not appropriate. 
The administrative data underlying SWITCH contains 100 recipient households of WFP. 
Weighted, this equates to 53k households, which is similar to administrative figures thanks to 
the reweighting procedure used to prepare the SILC data to be used with the SWITCH model.6 
SWITCH simulates that 210 (unweighted) or over 100k households are eligible for the WFP, 
giving a take-up rate of almost 53%.  
 
5 See Sutherland and Figari (2013) for an overview of the EUROMOD model and Keane et al (2022) for an 
overview of the SWITCH model. 
6 Without this reweighting procedure, we have 47,315 recipient households compared to 100,275 eligible 
households.  


The EU-SILC dataset underlying EUROMOD contains just 27, or 12k weighted self-declared 
recipient households. EUROMOD simulates that between 80 and 90k households are eligible 
(depending on which policy system is linked to the underlying 2019 data). This gives a much 
lower take-up rate of 13-15%. The self-reported nature of WFP receipt in the EUROMOD 
dataset is likely to be driving down the number of recipient households.7 This coupled with the 
mismatch between the income reference period and the survey year in EUROMOD leads us to 
consider the SWITCH simulation to be much more accurate. The magnitude of the discrepancy 
between the two simulations indicates the importance of these two factors in estimating take-
up robustly. 
Table 1: Benefit Recipient Numbers Comparison, 2019 
Receipt 
Eligible  
  
unweighted weighted unweighted weighted 
Take-
up 
Admin. 
Data 
SWITCH 
100 
52,733  
210 
100,365  
53% 
53,104 
EUROMOD 
27 
11,707 
159 
80,085 
15% 
EUROMOD: 1 year 
lag 
27 
11,707 
175 
88,501 
13% 
Note: Authors calculations using the SWITCH v5.3 tax-benefit system for 2019 linked to SILC 2019 and EUROMOD 
vI4.109+ tax-benefit system for 2019 and 2018 (1 year lag) linked to EU-SILC 2019. Administrative figures taken from 2019 
SISWS file: gov.ie - Annual SWS Statistical Information Report (www.gov.ie) 
In Table 2, we calculate take-up based on the amount of WFP received by households rather 
than the number of households in receipt. Using SWITCH, take-up is estimated at 73%, 20 
points higher than take-up based on recipient numbers. This is consistent with the wider 
literature on take-up, which suggests that households that do not take up welfare are 
systematically more likely to be eligible for lower levels of welfare. 
Table 2: Annual Expenditure on Working Family Payment, 2019 (€, million) 
 
Receipt 
Eligible 
Take-up 
Annual amount of WFP 
 
 
 
SWITCH 
343.69  
472.99  
72.7% 
 
7 This is not unusual in survey data. Meyer & Mittag (2019) recently showed that self-reported receipt of welfare 
in the American Current Population Survey was between 40-65% of actual receipt. For Ireland, Bargain & Doorley 
(2011) estimate that 17% of those eligible for the Family Income Supplement in the 2001 Living in Ireland Survey 
report receiving it.  


EUROMOD 
46.33 
370.81 
12.5% 
EUROMOD 1 year lag 
45.94 
413.33 
11.1% 
Admin data 
397.20 
 
 
Note: Authors calculations using the SWITCH v5.3 tax-benefit system for 2019 linked to SILC 2019 and EUROMOD 
vI4.109+ tax-benefit system for 2019 and 2018 (1 year lag) linked to EU-SILC 2019. Administrative figures taken from 2019 
SISWS file: gov.ie - Annual SWS Statistical Information Report (www.gov.ie) 
2. Income poverty and inequality 
We next simulate income poverty and inequality in 2019 using SWITCH under the assumption 
of (i) full-take up of the WFP and (ii) simulated partial take-up of the WFP. In scenario (ii), we 
assign 53% of those households eligible for the WFP to actually take it up.  Figure 1 illustrates 
that much of the estimated non-take-up is concentrated among households who are eligible for 
a relatively low level of payment (< €300 per month). We therefore assign a higher probability 
of take-up to households who are eligible for a greater amount of WFP and our distribution of 
adjusted take-up (patterned bar in Figure 1) closely matches receipt in the underlying data 
(black bar).  
Figure 1: Distribution of WFP amount for receiving and eligible households with full and 
adjusted take-up 
 
Note: Authors calculations using the SWITCH v5.3 tax-benefit system for 2019 linked to SILC 2019. The adjusted take-up 
scenarios assume a take-up rate of 53% and a higher probability of take-up to households who are eligible for higher amount 
of WFP. 
Table 3 shows that income inequality is largely unchanged in the two take-up scenarios. 
However, income poverty increases between the full take-up and adjusted take-up scenarios, 
0%
10%
20%
30%
40%
50%
60%
0-300
301-600
601-900
>900
Percent of eligible households
Amount of WFP
Receiving
Eligible
Eligible - adjusted take-up


increasing by half a percentage point for the whole population and almost one percentage point 
for children.  
Table 3: Income inequality and poverty 
 
SWITCH full take up SWITCH adjusted take-up Difference 
 
 
 
 
Gini 
0.2657 
0.2668 
0.0011 pp 
Poverty - whole population 11.80% 
12.26% 
0.46 pp 
Poverty - adult population 
11.47% 
11.84% 
0.37 pp 
Elderly poverty 
9.12% 
9.12% 
0.00 pp 
Child poverty 
14.11% 
15.03% 
0.92 pp 
Note: Authors calculations using the SWITCH v5.3 tax-benefit system for 2019 linked to SILC 2019. The adjusted take-up 
scenario assumes a take-up rate of 53% and a higher probability of take-up for households who are eligible for higher WFP. 
Assessment units are defined as being at risk of poverty (poor) if their equivalised disposable income is below the poverty 
line. The poverty line is defined as 60% of the median equivalised disposable income. The CSO equivalence scale is used, 
which attributes a weight of 1 to the head of the unit, a weight of 0.66 to every person above the age of 13 and a weight of 
0.33 to every child aged 0-13. Income poverty rates for the adjusted take-up are reported using a poverty line fixed to the 
SWITCH full take-up level scenario.  
3. Discussion 
Take-up of welfare in general is important as the welfare system is typically designed to reduce 
poverty and income inequality, while maintaining incentives to work. Take-up of the WFP in 
Ireland is of particular policy importance as Doorley et al (2022) showed that, euro-for-euro, it 
has a greater poverty reducing potential that other instruments in the Irish system. This note 
reinforces that importance, showing that improving take-up could materially affect poverty. 
Even if most households who do not take up the payment are eligible for a relatively small 
amount, it would still improve the living standards of a portion of households currently living 
below the poverty line.  
Imperfect take-up reduces the effectiveness of welfare and in-work transfers and renders it 
difficult to design and cost reforms. In this respect, measuring take-up is an important function 
of researchers. This note has illustrated the difficulties inherent to the estimation of take-up and 
shown the discrepancies involved in estimates derived from self-declared sources compared to 
more reliable administrative sources. The SWITCH microsimulation model, which is based on 
survey data linked to administrative data from the Irish Department of Social Protection, is a 
good working example of how collaboration between statistical agencies who collect and 


administer survey data and government ministries who hold administrative information on 
welfare payments can be used to obtain robust estimates of welfare take-up which can be used 
for policy purposes.  
4. Bibliography 
Bargain, O., Immervoll, H. & Viitamäki, H. (2012). No claim, no pain. Measuring the non-
take-up of social assistance using register data. The Journal of Economic 
Inequality, 10(3), 375–395. 
Bargain, O. & Doorley, K. (2011). In-Work Transfers in Good Times and Bad: Simulations for 
Ireland, Solomon W. Polachek, Konstantinos Tatsiramos (eds.), 2011, Research in 
Labor Economics (Research in Labor Economics, Volume 33), Emerald Group 
Publishing Limited, 307-339 
Bhargava, S., & Manoli, D. (2015). Psychological Frictions and the Incomplete Take-Up of 
Social Benefits: Evidence from an IRS Field Experiment. American Economic 
Review, 105 (11): 3489-3529. 
Bruckmeier, K., & Wiemers, J. (2012). A new targeting: a new take-up?. Empirical 
Economics, 43(2), 565–580. 
Callan, T., & Keane, C. (2008). Non-take-up of means-tested benefits: National Report for 
Ireland. AIM-AP Project: Accurate Income Measurement for the Assessment of 
National Priorities. 
Doorley, K., Kakoulidou, T., O'Malley, S., Russell, H. & Maître, B. (2022). Headline Poverty 
Target Reduction in Ireland and the Role of Work and Social Welfare. Economic and 
Social Research Institute (ESRI) Research Series. 
Hernanz, V., Malherbet, F., & Pellizzari, M. (2004). Take-Up of Welfare Benefits in OECD 
Countries: A Review of the Evidence.  
Keane, C., Doorley, K., Kakoulidou, T., & O’Malley, S. (2023). SWITCH: A Tax-Benefit 
Model for Ireland Linked to Survey and Register Data. International Journal of 
Microsimulation, 16(1), 65-88. 
Ko, W., & Moffitt, R. A. (2022). Take-up of social benefits (No. w30148). National Bureau of 
Economic Research. 


Martin, L., Delaney, L., & Doyle, O. (2022). Everyday Administrative Burdens and Inequality 
(No.WP22/05). UCS Centre for Economic Research Working Paper Series. 
Meyer, B. D., & Mittag, N.(2019). Using Linked Survey and Administrative Data to Better 
Measure Income: Implications for Poverty, Program Effectiveness, and Holes in the 
Safety Net. American Economic Journal: Applied Economics, 11 (2): 176-204. 
Moffitt, R. A. (Ed.). (2007). Means-tested transfer programs in the United States. University 
of Chicago Press. 
Sutherland, H., & Figari, F. (2013). EUROMOD: the European Union tax-benefit 
microsimulation model. International Journal of Microsimulation, 6(1), 4–26. 
Tempelman, C. & Houkes-Hommes, A., (2016), What Stops Dutch Households from Taking 
Up Much Needed Benefits?. Review of Income and Wealth, 62(4), 685-705. 
 


