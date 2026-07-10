# Verification Checklist by Policy Type

Use this reference during Phase 5 (cross-check and report). For each field in the docx, confirm the value against at least one authoritative source (CR PDF or official website).

---

## Table of Contents
- [Taxes](#taxes)
- [Benefits](#benefits)
- [Contributions](#contributions)
- [Sickness Benefits](#sickness-benefits)
- [Childcare Costs](#childcare-costs)
- [General Checks](#general-checks-all-policies)
- [Issue Taxonomy](#issue-taxonomy)

---

## Taxes

- [ ] Year label in bracket tables matches the actual year (not copy-pasted from prior year)
- [ ] All income tax brackets: thresholds and rates correct
- [ ] Decimal/thousand separators consistent (period for decimals, comma for thousands in English)
- [ ] All covered income types listed (wages, self-employment, dividends, interest, capital gains, rental)
- [ ] Tax credits/deductions: amounts and eligibility conditions correct
- [ ] 2026 column: any changes to brackets, rates, or credits captured
- [ ] No missing spaces in formatted strings (e.g. "€5,000if income > X" → "€5,000 if income > X")

---

## Benefits

### Child/Family Benefits
- [ ] Birth grant amount correct for 2025 and 2026
- [ ] Child benefit amounts and income thresholds correct
- [ ] Large family allowance amounts correct
- [ ] Parental allowance: amount, duration, qualifying conditions

### Social Assistance
- [ ] Income support (varstveni dodatek): base amount, eligibility
- [ ] 2026 column: any changes to eligibility rules (e.g. adult children maintenance obligation)
- [ ] Financial social assistance: income test thresholds

### Scholarships
- [ ] State scholarship listed in Table of Contents if described in body
- [ ] Income thresholds for scholarship eligibility

### Formatting
- [ ] All monetary amounts use period as decimal separator
- [ ] Table of Contents matches all sections in document body

---

## Contributions

### Employee contributions
- [ ] Health insurance rate correct
- [ ] Pension insurance rate correct
- [ ] Long-term care (LTC) contribution: rate and applicable date (may be new)
- [ ] Unemployment insurance rate correct

### Employer contributions
- [ ] Health insurance: check if different rates apply for different worker categories
  - Regular employment / sick leave / maternity leave
  - Unemployment wage compensation
  - Disabled workers
- [ ] Pension insurance rate correct
- [ ] LTC contribution rate correct
- [ ] Occupational injury/disease insurance rate correct

### Self-employed contributions
- [ ] Total contribution rate correct; note if mid-year change applies
- [ ] LTC contribution documented separately if applicable
- [ ] Minimum contribution base (OZP) amount correct, including update date

---

## Sickness Benefits

- [ ] Replacement rates by cause listed completely for ≤90 days and >90 days:
  - Illness / regular sickness
  - Non-work-related injury
  - Care of family member
  - Isolation
  - Occupational accident / disease
  - Donation of tissue, organs, or blood
- [ ] "90 days" specified as **calendar** days (not working days)
- [ ] Employer period: 30 working days per absence, max 80 working days per calendar year
- [ ] Minimum benefit: 60% of minimum wage (verify formula)
- [ ] Maximum benefit: 2.5× average monthly gross salary (verify reference wage)
- [ ] Benefit base for ≤30 days: average of last 3 calendar months' gross wage
- [ ] Benefit base for >30 days: previous calendar year average
- [ ] Self-employed waiting period: 30 working days (cover themselves)
- [ ] 2026 column: check for any changes to rates, base, or entitlement rules
- [ ] Legal sources: includes all relevant laws (ZDR-1, ZZVZZ, any new interventional laws)

---

## Childcare Costs

### Gross fees
- [ ] Fee amounts correspond to national average (not a specific municipality)
- [ ] Two age groups covered: 1–2 years and 3–5 years
- [ ] Source of fee amounts stated (Ministry of Education annual publication)
- [ ] 2026 fees reflect updated annual publication

### Fee reductions (income brackets)
- [ ] All 9 income brackets listed with correct upper thresholds
- [ ] Payment percentages correct for each bracket
- [ ] 2026 thresholds updated (annual ZUPJS indexation — typically ~2–3%)
- [ ] Decimal separator: period throughout (comma is a formatting error)
- [ ] Second-child discount and third-child full exemption noted

### Tax treatment
- [ ] Confirmed: childcare costs are NOT tax-deductible in Slovenia (verify for other countries)

### Assumptions
- [ ] Full-day attendance assumed
- [ ] Public kindergarten assumed
- [ ] Municipal variation abstracted away — noted as limitation

---

## General Checks (All Policies)

- [ ] Document title matches country and year range
- [ ] All 2025 values verified against CR PDF or official source
- [ ] All 2026 changes verified (non-empty cells checked; empty cells confirmed correct)
- [ ] Sources section lists all laws and websites used
- [ ] No copy-paste artifacts from prior year (wrong year references, stale amounts)

---

## Issue Taxonomy

Use these types when recording findings in Phase 5 and when generating the issues JSON.

| Issue Type | Example |
|---|---|
| Wrong value | Rate is 5.96% but docx says 6.56% |
| Missing information | t change column empty but law changed |
| Formatting error | `€441,60` should be `€441.60` (comma vs period) |
| Wrong year label | Table header says "for t-1" but should say "for t" |
| Missing entry | Rate applies to category X but category X absent from table |
| Incomplete description | Change applies from July only, but no caveat stated |
| Missing source | New law in force but not listed in sources |
| Structural issue | Section in body text but missing from Table of Contents |
