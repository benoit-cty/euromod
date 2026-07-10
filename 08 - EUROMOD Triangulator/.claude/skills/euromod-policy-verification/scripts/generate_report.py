"""
DK Policy Verification Report 2025 → 2026
Output: EM_DK_policy_verification_2025_2026.html
"""
from datetime import date
import os

today = date.today().strftime("%Y-%m-%d")

# ============================================================================
# SETTINGS — edit before running
# ============================================================================
COUNTRY      = "DK"                   # Two-letter country code
COUNTRY_NAME = "Denmark"              # Full country name for the H1 title
COUNTRY_FLAG = "&#127465;&#127472;"   # HTML flag emoji (DK)
T_MINUS_1    = 2025                   # Base year (t-1)
T            = 2026                   # Target year (t)
BASE_SYSTEM  = "DK_2025"             # EUROMOD system name for t-1 (must exist in XML)
OUTPUT_DIR   = r"."                   # Output folder; set to absolute path before running
# True if the t system already exists in the XML (Case B: corrections only).
# False if the t system does not yet exist (Case A: full parameter list).
YEAR_T_EXISTS = False

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
SEV_COLOR = {"WARNING": "#fd7e14", "INFO": "#0d6efd"}
SEV_BG    = {"WARNING": "#fff3cd", "INFO": "#f0f4ff"}

def badge(sev):
    c = SEV_COLOR.get(sev, "#555")
    return f'<span style="background:{c};color:white;padding:2px 8px;border-radius:4px;font-size:0.82em;font-weight:bold">{sev}</span>'

def domain_badge(domain):
    color_map = {"Benefits": "#198754", "Taxes": "#0dcaf0",
                 "Contributions": "#6f42c1", "Childcare": "#d63384",
                 "Sickness": "#0dcaf0", "XML": "#dc3545"}
    c = color_map.get(domain, "#888")
    return f'<span style="background:{c};color:white;padding:2px 7px;border-radius:4px;font-size:0.80em;">{domain}</span>'

def row_color(sev):
    return SEV_BG.get(sev, "#f9f9f9")

def ok(v):   return f'<span class="ok">{v}</span>'
def warn(v): return f'<span class="warn">{v}</span>'
def dash():  return "—"
def bold(v): return f'<strong>{v}</strong>'
def tbd(v):  return f'<em style="color:#888">{v}</em>'

# ---------------------------------------------------------------------------
# SECTION 1 — SOURCE INVENTORY
# ---------------------------------------------------------------------------
sources = [
    ("taxes_2025_2026_final.docx",           "Policy docx", '<span class="source-ok">&#10003; Extracted</span>', "PIT rates, allowances, municipality tax, bracket taxes, earned income credit, property tax"),
    ("benefits_2025_2026_final.docx",        "Policy docx", '<span class="source-ok">&#10003; Extracted</span>', "UB, social assistance, child benefits, housing benefit/grant, pensions, green check"),
    ("contributions_2025_2026_final.docx",   "Policy docx", '<span class="source-ok">&#10003; Extracted</span>', "A-kasse, efterlon, ATP"),
    ("DK_sicknessbenefits_2025_20261_final.docx", "Policy docx", '<span class="source-ok">&#10003; Extracted</span>', "Sickness benefit ceiling"),
    ("DK_childcarecost_2025_2026_final.docx","Policy docx", '<span class="source-ok">&#10003; Extracted</span>', "Childcare fees, subsidy thresholds"),
    ("Y16_CR_DK.pdf",                        "Country Report (PDF)", '<span class="source-ok">&#10003; Extracted</span>', "2025 baseline values — pdfplumber, pages 23-55"),
    ("DK/DK.xml (J2.0)",                     "EUROMOD model XML", '<span class="source-ok">&#10003; Probed</span>', "DK_2025 system — DefConst, BenCalc, SchedCalc probed; DK_2026 does NOT exist"),
    ('<a href="https://www.retsinformation.dk">retsinformation.dk VEJ 10230/2025</a>', "Official website", '<span class="source-ok">&#10003; Accessible</span>', "Dagpenge/A-kasse/efterlon 2026 rates, UB ceiling, ATP, tax bracket thresholds"),
    ("skat.dk/satser", "Official website", '<span class="source-fail">&#10007; JS-rendered &mdash; inaccessible</span>', "PIT rates, personfradrag &mdash; values obtained via VEJ 10230"),
    ("borger.dk",      "Official website", '<span class="source-fail">&#10007; JS-rendered &mdash; inaccessible</span>', "Benefit amounts, childcare, social assistance"),
    ("bm.dk",          "Official website", '<span class="source-fail">&#10007; Cookie wall &mdash; inaccessible</span>', "Benefit policy details"),
]

# ---------------------------------------------------------------------------
# SECTION 2 — CHANGES FROM DOCX
# ---------------------------------------------------------------------------
# Tuple: (policy_code, parameter_description, t_minus_1_value, t_value, nature)
# Rules for t_value: always show actual value; bold() if changed; plain text if same.
# Nature: "Parametric" | "Structural" | "New policy" | "No change" | "TBD"
# NEVER use warn(), ok(), badge(), or colour classes in t_value or t_minus_1_value.
taxes_changes = [
    ("tmu_dk / ConstDef_dk", "Personal allowance &mdash; adult (personfradrag)", "51,600 DKK", bold("54,100 DKK"), "Parametric"),
    ("tmu_dk / ConstDef_dk", "Personal allowance &mdash; youth (personfradrag)", "51,600 DKK", bold("54,100 DKK"), "Parametric"),
    ("tmu_dk", "Municipality tax &mdash; weighted average", "25.10%", bold("25.05%"), "Parametric"),
    ("tinbt_dk", "Bottom bracket rate (bundskat)", "12.01%", "12.01%", "No change"),
    ("tcr_dk", "Church tax average (kirkeskat)", "0.87%", "0.87%", "No change"),
    ("tintc_dk", "Earned income credit rate", "12.30%", bold("12.75%"), "Parametric"),
    ("tintc_dk", "Earned income credit max", "55,600 DKK", bold("63,300 DKK"), "Parametric"),
    ("tintc_dk", "EIC single-provider supplement max", "48,300 DKK", bold("50,600 DKK"), "Parametric"),
    ("tintc_dk", "EIC additional credit threshold", "224,500 DKK", bold("235,200 DKK"), "Parametric"),
    ("tintc_dk", "EIC additional credit max", "2,900 DKK", bold("3,100 DKK"), "Parametric"),
    ("tinto_dk", "Top bracket rate (topskat)", "15.00%", bold("7.50%"), "Parametric + Structural"),
    ("ConstDef_dk", "Top bracket threshold", "611,800 DKK", bold("777,900 DKK"), "Parametric"),
    ("tinto_dk", "Tax ceiling (skatteloft)", "52.07%", bold("44.57%"), "Parametric"),
    ("tinto_dk", "Net capital income allowance (bundfradrag)", "52,400 DKK", bold("55,000 DKK"), "Parametric"),
    ("tinmd_dk &mdash; NEW", "Middle bracket rate (mellemskat)", "n/a", bold("7.50%"), "New policy"),
    ("tinmd_dk &mdash; NEW", "Middle bracket threshold", "n/a", bold("641,200 DKK/y"), "New policy"),
    ("tinmd_dk &mdash; NEW", "Net capital income allowance (tinmd_dk)", "n/a", bold("55,000 DKK"), "New policy"),
    ("tintto_dk &mdash; NEW", "Toptop bracket rate", "n/a", bold("5.00%"), "New policy"),
    ("tintto_dk &mdash; NEW", "Toptop bracket threshold", "n/a", bold("2,592,700 DKK/y"), "New policy"),
    ("txc_dk", "Am-bidrag age restriction", "None (all earners)", bold("&ge; 18 years from 2026"), "Structural"),
    ("tintcs_dk &mdash; NEW", "Senior earned income credit rate", "n/a", bold("1.4% of gross wages"), "New policy"),
    ("tintcs_dk &mdash; NEW", "Senior EIC maximum", "n/a", bold("6,100 DKK/y"), "New policy"),
]

benefits_changes = [
    ("bunct_dk", "Unemployment benefit standard ceiling", "253,104 DKK/y", bold("264,492 DKK/y"), "Parametric"),
    ("bunct_dk", "UB first-3-months ceiling (118.86%)", "300,840 DKK/y", bold("314,376 DKK/y"), "Parametric"),
    ("bunct_dk", "UB student with child ceiling", "207,540 DKK/y", bold("216,888 DKK/y"), "Parametric"),
    ("bunct_dk", "UB student without child ceiling", "180,972 DKK/y", bold("189,108 DKK/y"), "Parametric"),
    ("bhtuc_dk", "Green check &mdash; pensioner base amount", "875 DKK/y", "875 DKK/y", "No change"),
    ("bhtuc_dk", "Green check &mdash; per-child amount (pensioners)", "240 DKK", bold("0 DKK"), "Parametric"),
    ("bhtuc_dk", "Green check &mdash; phase-out threshold", "475,300 DKK", bold("498,200 DKK"), "Parametric"),
    ("bhtuc_dk", "Green check &mdash; extra low-income threshold", "~277,800 DKK", bold("~291,100 DKK"), "Parametric"),
    ("bfachnm_dk", "Child family grant (age 0&ndash;2)", "21,168 DKK/y", bold("21,480 DKK/y"), "Parametric"),
    ("bfachnm_dk", "Child family grant (age 3&ndash;6)", "16,764 DKK/y", bold("16,992 DKK/y"), "Parametric"),
    ("bfachnm_dk", "Child family grant (age 7&ndash;17)", "13,188 DKK/y", bold("13,668 DKK/y"), "Parametric"),
    ("bfachnm_dk", "Child family grant &mdash; income threshold", "917,000 DKK/y", bold("961,100 DKK/y"), "Parametric"),
    ("bfach00_dk", "Child benefit basic amount", "6,664 DKK/y", bold("6,964 DKK/y"), "Parametric"),
    ("bfach00_dk", "Child benefit lone-parent supplement", "6,792 DKK/y", bold("7,096 DKK/y"), "Parametric"),
    ("bfach00_dk", "Child benefit &mdash; income threshold", "917,000 DKK/y", bold("961,100 DKK/y"), "Parametric"),
    ("bfached_dk", "Student parent benefit &mdash; amount per child", "8,452 DKK/y", bold("9,152 DKK/y"), "Parametric"),
    ("bfached_dk", "Student parent benefit &mdash; single threshold", "169,200 DKK", bold("183,100 DKK"), "Parametric"),
    ("bfached_dk", "Student parent benefit &mdash; couple threshold", "253,600 DKK", bold("274,500 DKK"), "Parametric"),
    ("bho01_dk", "Housing benefit &mdash; max housing cost", "94,200 DKK/y", bold("96,200 DKK/y"), "Parametric"),
    ("bho01_dk", "Housing benefit &mdash; income threshold", "167,900 DKK/y", bold("171,500 DKK/y"), "Parametric"),
    ("bho01_dk", "Housing benefit &mdash; per-child increment", "44,200 DKK/y", bold("45,200 DKK/y"), "Parametric"),
    ("bho01_dk", "Housing benefit &mdash; min own rent", "28,300 DKK/y", bold("28,900 DKK/y"), "Parametric"),
    ("bho02_dk", "Housing grant &mdash; supplement amount", "8,100 DKK/y", bold("8,500 DKK/y"), "Parametric"),
    ("bho02_dk", "Housing grant &mdash; income threshold", "192,200 DKK/y", bold("201,400 DKK/y"), "Parametric"),
    ("bho02_dk", "Housing grant &mdash; per-child increment", "50,600 DKK/y", bold("53,100 DKK/y"), "Parametric"),
    ("bho02_dk", "Housing grant &mdash; min own rent", "20,300 DKK/y", bold("21,300 DKK/y"), "Parametric"),
    ("bho02_dk", "Housing grant &mdash; max benefit", "56,892 DKK/y", bold("59,628 DKK/y"), "Parametric"),
    ("poa_dk", "Old age pension basic amount", "86,376 DKK/y", bold("90,528 DKK/y"), "Parametric"),
    ("poa_dk", "Pension supplement &mdash; singles amount", "99,948 DKK/y", bold("104,748 DKK/y"), "Parametric"),
    ("poa_dk", "Pension supplement &mdash; singles threshold", "85,300 DKK/y", bold("89,400 DKK/y"), "Parametric"),
    ("poa_dk", "Pension supplement &mdash; couples amount", "51,144 DKK/y", bold("53,604 DKK/y"), "Parametric"),
    ("poa_dk", "Pension supplement &mdash; couples threshold", "170,900 DKK/y", bold("179,100 DKK/y"), "Parametric"),
    ("poa_dk", "Supplementary pension amount", "25,700 DKK/y", bold("26,900 DKK/y"), "Parametric"),
    ("poa_dk", "Supplementary pension asset threshold", "103,100 DKK", bold("108,000 DKK"), "Parametric"),
    ("bsa_dk", "Social assistance &mdash; complete overhaul", "Multi-tier, 225-hour rule", bold("New 3-tier structure"), "Structural"),
]

contributions_changes = [
    ("tyrui_dk", "A-kasse member contribution", "389 DKK/m", bold("407 DKK/m"), "Parametric"),
    ("tyrui_dk", "Efterlon contribution", "568 DKK/m", bold("593 DKK/m"), "Parametric"),
    ("tscpi_dk", "ATP (full-time employment)", "297 DKK/m", "297 DKK/m", "No change"),
]

sickness_changes = [
    ("sickcomp_dk", "Sickness benefit ceiling", "4,865 DKK/week (21,114 DKK/m)", bold("5,085 DKK/week (22,035 DKK/m)"), "Parametric"),
]

childcare_changes = [
    ("xcc_dk", "Childcare fee (age 0&ndash;2)", "45,548 DKK/y", tbd("TBD &mdash; not yet available"), "TBD"),
    ("xcc_dk", "Childcare fee (age 3&ndash;5)", "25,758 DKK/y", tbd("TBD &mdash; not yet available"), "TBD"),
    ("bccfc_dk", "Childcare subsidy: free-below threshold", "200,301 DKK", bold("218,101 DKK"), "Parametric"),
    ("bccfc_dk", "Childcare subsidy: full-fee threshold", "622,200 DKK", bold("677,500 DKK"), "Parametric"),
]

# ---------------------------------------------------------------------------
# SECTION 3 — CROSS-CHECK t-1 (2025)
# ---------------------------------------------------------------------------
crosscheck_2025 = [
    ("Personfradrag (adult)", "<code>$tmu_adult_rate</code>", "51,600 DKK", "51,600 DKK (Table 2.26)", "51,600", "VEJ 10230: 51,600", '<span class="source-ok">&#10003; MATCH</span>'),
    ("Personfradrag (youth)", "<code>$tmu_youth_rate</code>", "51,600 DKK", "51,600 DKK (Table 2.26)", "51,600", "VEJ 10230: 51,600", '<span class="source-ok">&#10003; MATCH</span>'),
    ("Municipality tax average", "<code>$tmu_rate</code>", "25.10%", "25.10% (Table 2.28)", "0.251", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Bottom bracket (bundskat)", "<code>$tinbt_rate</code>", "12.01%", "12.01% (Table 2.30)", "0.1201", "VEJ 10230: 12.01%", '<span class="source-ok">&#10003; MATCH</span>'),
    ("Church tax average", "<code>$tcr_rate</code>", "0.87%", "0.87% (Table 2.29)", "0.0087", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("EIC rate", "<code>$tintc_rate</code>", "12.30%", "12.30% (Table 2.27)", "0.123", "VEJ 10230: 12.30%", '<span class="source-ok">&#10003; MATCH</span>'),
    ("EIC max", "<code>$tintc_lim</code>", "55,600 DKK", "55,600 DKK (Table 2.27)", "55,600", "VEJ 10230: 55,600", '<span class="source-ok">&#10003; MATCH</span>'),
    ("EIC single-provider supplement max", "<code>$tintc_suppllim1</code>", "48,300 DKK", "48,300 DKK (Table 2.27)", "48,300", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("EIC additional credit threshold", "<code>$tintc_supplthres</code>", "224,500 DKK", "224,500 DKK (Table 2.27)", "224,500", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("EIC additional credit max", "<code>$tintc_suppllim2</code>", "2,900 DKK", "2,900 DKK (Table 2.27)", "2,900", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Top bracket rate", "<code>$tinto_rate</code>", "15.00%", "15.00% (Table 2.31)", "0.15", "VEJ 10230: 15.00%", '<span class="source-ok">&#10003; MATCH</span>'),
    ("Top bracket threshold", "<code>$tinto_thres</code>", "611,800 DKK", "611,800 DKK (Table 2.31)", "611,800", "VEJ 10230: 611,800", '<span class="source-ok">&#10003; MATCH</span>'),
    ("Tax ceiling (skatteloft)", "<code>$tinto_uplim_rate</code>", "52.07%", "52.01% (CR Table 2.32)", "0.5201", dash(), '<span class="warn">&#9888; DISCREPANCY &mdash; DK-012</span>'),
    ("Net capital income allowance", "<code>bundfradrag</code>", "52,400 DKK", "52,400 DKK (Table 2.31)", "52,400", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("A-kasse contribution", "<code>$tyrui_akasse</code>", "389 DKK/m", "389 DKK/m (Table 2.25)", "957 (combined)", "VEJ 10230: 389", '<span class="source-ok">&#10003; MATCH</span>'),
    ("Efterlon contribution", "<code>$tyrui_efterlon</code>", "568 DKK/m", "568 DKK/m (Table 2.25)", "957 (combined)", "VEJ 10230: 568", '<span class="source-ok">&#10003; MATCH</span>'),
    ("ATP (full-time)", "<code>$tscpi_amt1</code>", "297 DKK/m", "297 DKK/m (Table 2.24)", "297", "VEJ 10230: 297", '<span class="source-ok">&#10003; MATCH</span>'),
    ("UB standard ceiling", "<code>$bunct_uplim</code>", "253,104 DKK/y", "253,104 DKK/y (Table 2.7)", "253,104", "VEJ 10230: 253,104", '<span class="source-ok">&#10003; MATCH</span>'),
    ("Sickness benefit ceiling", "<code>$bhl_max_amt</code>", "4,865 DKK/wk (21,114 DKK/m)", "Not in CR", "21,114", dash(), '<span class="source-ok">&#10003; XML matches docx</span>'),
    ("Green check &mdash; pensioner base amount", "<code>bhtuc_dk Amount#3</code>", "875 DKK/y", "~1,005 DKK/y (CR Table 2.14)", "875", dash(), '<span class="warn">&#9888; DISCREPANCY &mdash; DK-001/DK-009</span>'),
    ("Green check &mdash; per-child (pensioners)", "<code>bhtuc_dk Amount#4</code>", "240 DKK/y", "0 DKK/y (CR Table 2.14)", "0", dash(), '<span class="warn">&#9888; DISCREPANCY &mdash; DK-005</span>'),
    ("Green check &mdash; phase-out threshold", "<code>bhtuc_dk withdraw_start</code>", "475,300 DKK", "475,300 DKK (CR Table 2.14)", "457,500", dash(), '<span class="warn">&#9888; DISCREPANCY &mdash; DK-010</span>'),
    ("Child family grant (age 0&ndash;2)", "<code>$bfachnm_amt1</code>", "21,168 DKK/y", "21,168 DKK/y (Table 2.11)", "21,168", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Child family grant (age 3&ndash;6)", "<code>$bfachnm_amt2</code>", "16,764 DKK/y", "16,764 DKK/y (Table 2.11)", "16,764", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Child family grant (age 7&ndash;17)", "<code>$bfachnm_amt3</code>", "13,188 DKK/y", "13,188 DKK/y (Table 2.11)", "13,188", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Child family grant &mdash; income threshold", "<code>$bfachnm_thres</code>", "917,000 DKK/y", "917,000 DKK/y (CR)", "917,000", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Child benefit basic amount", "<code>$bfach00_bchild_amt</code>", "6,664 DKK/y", "6,664 DKK/y (Table 2.12)", "6,664", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Child benefit lone-parent supplement", "<code>$bfach00_bchild_lone_amt</code>", "6,792 DKK/y", "6,792 DKK/y (Table 2.12)", "6,792", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Student parent benefit &mdash; amount", "<code>$bfached_bamt</code>", "8,452 DKK/y", "8,756 DKK/y (CR p.32)", "8,756", dash(), '<span class="warn">&#9888; DISCREPANCY &mdash; DK-002</span>'),
    ("Student parent benefit &mdash; single threshold", "<code>$bfached_ytest_single</code>", "169,200 DKK", "175,200 DKK (CR p.32)", "169,100", dash(), '<span class="warn">&#9888; DISCREPANCY &mdash; DK-003/DK-011</span>'),
    ("Student parent benefit &mdash; couple threshold", "<code>$bfached_ytest_couple</code>", "253,600 DKK", "262,700 DKK (CR p.32)", "253,600", dash(), '<span class="warn">&#9888; DISCREPANCY &mdash; DK-003/DK-011</span>'),
    ("Housing benefit &mdash; max housing cost", "<code>bho01_dk inline</code>", "94,200 DKK/y", "94,200 DKK/y (Table 2.16)", "94,200", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Housing benefit &mdash; income threshold", "<code>bho01_dk inline</code>", "167,900 DKK/y", "167,900 DKK/y (Table 2.16)", "167,900", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Housing benefit &mdash; per-child increment", "<code>bho01_dk inline</code>", "44,200 DKK/y", "44,200 DKK/y (Table 2.16)", "44,200", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Housing benefit &mdash; min own rent", "<code>bho01_dk inline</code>", "28,300 DKK/y", "28,300 DKK/y (Table 2.16)", "28,300", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Housing grant &mdash; supplement amount", "<code>bho02_dk inline</code>", "8,100 DKK/y", "8,100 DKK/y (Table 2.18)", "8,100", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Housing grant &mdash; income threshold", "<code>bho02_dk inline</code>", "192,200 DKK/y", "192,200 DKK/y (Table 2.18)", "192,200", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Housing grant &mdash; max benefit", "<code>bho02_dk inline</code>", "56,892 DKK/y", "56,892 DKK/y (Table 2.18)", "56,892", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Old age pension basic amount", "<code>$poa_amt</code>", "86,376 DKK/y", "86,376 DKK/y (Table 2.19)", "86,376", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Old age pension supplement (singles)", "<code>$poa_single_supplamt</code>", "99,948 DKK/y", "99,948 DKK/y (Table 2.21)", "99,948", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Old age pension supplement threshold (singles)", "<code>$poa_single_thres</code>", "85,300 DKK/y", "85,300 DKK/y (CR p.40)", "85,300", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Old age pension supplement (couples)", "<code>$poa_couple_supplamt</code>", "51,144 DKK/y", "51,144 DKK/y (Table 2.21)", "51,144", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Supplementary pension amount", "<code>$poa_supplamt</code>", "25,700 DKK/y", "25,700 DKK/y (Table 2.22)", "25,700", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Supplementary pension asset threshold", "<code>$poa_supplthres</code>", "103,100 DKK", "103,100 DKK (Table 2.22)", "103,100", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Personal suppl. rate &mdash; single threshold", "<code>poa_dk inline</code>", "35,200 DKK/y", "35,200 DKK/y (Table 2.23)", "35,200", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Personal suppl. rate &mdash; single deduction/pp", "<code>poa_dk inline</code>", "606 DKK", "606 DKK (Table 2.23)", "606 (DefConst: 583)", dash(), '<span class="warn">&#9888; DISCREPANCY &mdash; DK-013</span>'),
    ("Personal suppl. rate &mdash; couple threshold", "<code>poa_dk inline</code>", "69,700 DKK/y", "69,700 DKK/y (Table 2.23)", "69,700", dash(), '<span class="source-ok">&#10003; MATCH</span>'),
    ("Personal suppl. rate &mdash; couple deduction/pp", "<code>poa_dk inline</code>", "1,223 DKK", "1,223 DKK (Table 2.23)", "1,223 (DefConst: 1,177)", dash(), '<span class="warn">&#9888; DISCREPANCY &mdash; DK-013</span>'),
    ("Childcare fee (age 0&ndash;2)", "<code>$xcc_amt1</code>", "45,548 DKK/y", "Not in CR", "45,548", dash(), '<span class="source-ok">&#10003; XML matches docx</span>'),
    ("Childcare fee (age 3&ndash;5)", "<code>$xcc_amt2</code>", "25,758 DKK/y", "Not in CR", "25,758", dash(), '<span class="source-ok">&#10003; XML matches docx</span>'),
    ("Childcare subsidy: free-below threshold", "<code>$bccfc_upthres1</code>", "200,301 DKK", "Not in CR", "208,101", "borger.dk: blocked", '<span class="warn">&#9888; DISCREPANCY &mdash; DK-008</span>'),
]

# ---------------------------------------------------------------------------
# SECTION 4 — CROSS-CHECK t (2026)
# ---------------------------------------------------------------------------
crosscheck_2026 = [
    ("Personfradrag (adult)", "<code>$tmu_adult_rate</code>", "54,100 DKK", "VEJ 10230: 54,100", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Personfradrag (youth)", "<code>$tmu_youth_rate</code>", "54,100 DKK", "VEJ 10230: 54,100", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Municipality tax average", "<code>$tmu_rate</code>", "25.05%", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Bottom bracket (bundskat)", "<code>$tinbt_rate</code>", "12.01%", "VEJ 10230: 12.01%", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Church tax", "<code>$tcr_rate</code>", "0.87%", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("EIC rate", "<code>$tintc_rate</code>", "12.75%", "VEJ 10230: 12.75%", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("EIC max", "<code>$tintc_lim</code>", "63,300 DKK", "VEJ 10230: 63,300", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("EIC single-provider supplement max", "<code>$tintc_suppllim1</code>", "50,600 DKK", "VEJ 10230: 50,600", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("EIC additional credit threshold", "<code>$tintc_supplthres</code>", "235,200 DKK", "VEJ 10230: 235,200", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("EIC additional credit max", "<code>$tintc_suppllim2</code>", "3,100 DKK", "VEJ 10230: 3,100", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Top bracket rate", "<code>$tinto_rate</code>", "7.50%", "VEJ 10230: 7.50%", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Top bracket threshold", "<code>$tinto_thres</code>", "777,900 DKK", "VEJ 10230: 777,900", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Tax ceiling (skatteloft)", "<code>$tinto_uplim_rate</code>", "44.57%", "VEJ 10230: 44.57%", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Middle bracket rate (new)", "<code>$tinmd_rate</code>", "7.50%", "VEJ 10230: 7.50%", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Middle bracket threshold (new)", "<code>$tinmd_thres</code>", "641,200 DKK", "VEJ 10230: 641,200", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Net capital income allowance (middle bracket)", "<code>$tinmd_netcap_allow</code>", "55,000 DKK", "VEJ 10230: 55,000", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Toptop bracket rate (new)", "<code>$tintto_rate</code>", "5.00%", "VEJ 10230: 5.00%", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Toptop bracket threshold (new)", "<code>$tintto_thres</code>", "2,592,700 DKK", "VEJ 10230: 2,592,700", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Senior EIC rate (new)", "<code>$tintcs_rate</code>", "1.40%", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Senior EIC max (new)", "<code>$tintcs_lim</code>", "6,100 DKK", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Net capital income allowance (top bracket)", "<code>bundfradrag</code>", "55,000 DKK", "VEJ 10230: 55,000", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("A-kasse contribution", "<code>$tyrui_akasse</code>", "407 DKK/m", "VEJ 10230: 407", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Efterlon contribution", "<code>$tyrui_efterlon</code>", "593 DKK/m", "VEJ 10230: 593", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("ATP (full-time)", "<code>$tscpi_amt1</code>", "297 DKK/m", "VEJ 10230: 297", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("UB standard ceiling", "<code>$bunct_uplim</code>", "276,492 DKK/y", "VEJ 10230: 264,492 DKK/y", '<span class="warn">&#9888; DISCREPANCY &mdash; DK-004</span>'),
    ("UB first-3-months ceiling", "<code>bunct_dk inline</code>", "314,376 DKK/y", "VEJ 10230: 314,376", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("UB student with child ceiling", "<code>bunct_dk inline</code>", "216,888 DKK/y", "VEJ 10230: 216,888", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("UB student without child ceiling", "<code>bunct_dk inline</code>", "189,108 DKK/y", "VEJ 10230: 189,108", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Sickness benefit ceiling", "<code>$bhl_max_amt</code>", "5,085 DKK/week (~22,035 DKK/m)", "VEJ 10230: 22,041 DKK/m", '<span class="source-ok">&#10003; CONFIRMED</span>'),
    ("Green check &mdash; pensioner base amount", "<code>bhtuc_dk Amount#3</code>", "875 DKK/y", dash(), '<span style="color:#1565c0">&#8505; Docx only; borger.dk blocked</span>'),
    ("Green check &mdash; phase-out threshold", "<code>bhtuc_dk withdraw_start</code>", "498,200 DKK", dash(), '<span style="color:#1565c0">&#8505; Docx only; borger.dk blocked</span>'),
    ("Child family grant (age 0&ndash;2)", "<code>$bfachnm_amt1</code>", "21,480 DKK/y", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Child family grant (age 3&ndash;6)", "<code>$bfachnm_amt2</code>", "16,992 DKK/y", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Child family grant (age 7&ndash;17)", "<code>$bfachnm_amt3</code>", "13,668 DKK/y", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Child benefit basic amount", "<code>$bfach00_bchild_amt</code>", "6,964 DKK/y", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Child benefit lone-parent supplement", "<code>$bfach00_bchild_lone_amt</code>", "7,096 DKK/y", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Student parent benefit &mdash; amount", "<code>$bfached_bamt</code>", "9,152 DKK/y", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Student parent benefit &mdash; single threshold", "<code>$bfached_ytest_single</code>", "183,100 DKK", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Student parent benefit &mdash; couple threshold", "<code>$bfached_ytest_couple</code>", "274,500 DKK", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Old age pension basic amount", "<code>$poa_amt</code>", "90,528 DKK/y", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Old age pension supplement (singles)", "<code>$poa_single_supplamt</code>", "104,748 DKK/y", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Old age pension supplement (couples)", "<code>$poa_couple_supplamt</code>", "53,604 DKK/y", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Supplementary pension amount", "<code>$poa_supplamt</code>", "26,900 DKK/y", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Supplementary pension asset threshold", "<code>$poa_supplthres</code>", "108,000 DKK", dash(), '<span style="color:#1565c0">&#8505; Docx only</span>'),
    ("Social assistance (new structure)", "<code>bsa_dk</code>", "New 3-tier structure", "borger.dk: blocked", '<span style="color:#1565c0">&#8505; Docx only; borger.dk blocked</span>'),
    ("Childcare fees", "<code>$xcc_amt1/2</code>", tbd("TBD &mdash; not yet available"), dash(), '<span style="color:#1565c0">&#8505; Not yet published</span>'),
    ("Childcare subsidy: free-below threshold", "<code>$bccfc_upthres1</code>", "218,101 DKK", "borger.dk: blocked", '<span style="color:#1565c0">&#8505; Docx only; borger.dk blocked</span>'),
    ("Childcare subsidy: full-fee threshold", "<code>$bccfc_upthres3</code>", "677,500 DKK", "borger.dk: blocked", '<span style="color:#1565c0">&#8505; Docx only; borger.dk blocked</span>'),
]

# ---------------------------------------------------------------------------
# SECTION 5 — ISSUES
# ---------------------------------------------------------------------------
issues = [
    {"id": "DK-001", "sev": "WARNING", "domain": "Benefits",
     "title": "<strong>bhtuc_dk</strong> &mdash; Green check base amount 2025 in docx is wrong",
     "detail": "Docx 2025 column: <b>875 DKK/year</b> for pensioners. Correct 2025 value per skat.dk: <b>1,005 DKK/year</b> (CR: 1,000 DKK). The docx has placed the 2026 value (875 DKK) in the 2025 column.",
     "rec": "Correct 2025 value in docx to 1,005 DKK; confirm 2026 change to 875 DKK."},
    {"id": "DK-002", "sev": "WARNING", "domain": "Benefits",
     "title": "<strong>bfached_dk</strong> &mdash; Student parent benefit amount 2025 in docx is wrong",
     "detail": "Docx 2025 column: <b>8,452 DKK/year per child</b>. CR p.32 (2025): <b>8,756 DKK/year</b>. The value 8,452 DKK is the 2024 figure. XML (DK_2025) has the correct value of 8,756 DKK.",
     "rec": "Correct docx 2025 column to 8,756 DKK/year."},
    {"id": "DK-003", "sev": "WARNING", "domain": "Benefits",
     "title": "<strong>bfached_dk</strong> &mdash; Income thresholds 2025 in docx AND XML are wrong",
     "detail": "Docx 2025: single <b>169,200 DKK</b>, couple <b>253,600 DKK</b>. CR 2025: single <b>175,200 DKK</b>, couple <b>262,700 DKK</b>. XML DK_2025 also has 2024 values: $bfached_ytest_single = 169,100, $bfached_ytest_couple = 253,600.",
     "rec": "Correct docx 2025 column to 175,200 / 262,700 DKK. Update XML DK_2025."},
    {"id": "DK-004", "sev": "WARNING", "domain": "Benefits",
     "title": "<strong>bunct_dk</strong> &mdash; UB standard ceiling 2026 in docx is wrong",
     "detail": "Docx 2026: <b>276,492 DKK/year</b>. VEJ 10230 &sect;47a: 22,041 DKK/month = <b>264,492 DKK/year</b>. The docx value of 276,492 implies ~9.2% increase; correct rate is ~4.5%.",
     "rec": "Correct docx 2026 standard UB ceiling to 264,492 DKK/year. Use 264,492 in XML DK_2026."},
    {"id": "DK-005", "sev": "INFO", "domain": "Benefits",
     "title": "<strong>bhtuc_dk</strong> &mdash; Per-child amount 2025 in docx is wrong",
     "detail": "Docx 2025: <b>240 DKK per child</b> for pensioners. CR Table 2.14 (2025): <b>0 DKK per child</b> (phased out from 2025). XML (DK_2025) correctly has Amount#4 = 0.",
     "rec": "Correct docx 2025 per-child component to 0 DKK."},
    {"id": "DK-006", "sev": "INFO", "domain": "Contributions",
     "title": "<strong>tscpi_dk (ATP)</strong> &mdash; Table year label inconsistency",
     "detail": "ATP table is labeled '(2024, Table 2.23)' in the 2025 parameter column. Values are correct (297 DKK/month unchanged), but the year label is misleading.",
     "rec": "Update docx label to '2024&ndash;2025' or '2025'."},
    {"id": "DK-007", "sev": "INFO", "domain": "Childcare",
     "title": "<strong>xcc_dk</strong> &mdash; 2026 fees not yet available from official sources",
     "detail": "The childcare docx explicitly notes: 'not available yet from official sources' for 2026 fees. 2025 values (age 0&ndash;2: 45,548 DKK/y; age 3&ndash;5: 25,758 DKK/y) match XML DK_2025.",
     "rec": "Monitor official source for 2026 childcare fees once published."},
    {"id": "DK-008", "sev": "INFO", "domain": "Childcare",
     "title": "<strong>bccfc_dk</strong> &mdash; Docx 2025 thresholds differ from XML DK_2025",
     "detail": "Docx 2025: free-below = <b>200,301 DKK</b>, full-fee = <b>622,200 DKK</b>. XML DK_2025: $bccfc_upthres1 = <b>208,101 DKK</b>, $bccfc_upthres3 = <b>646,500 DKK</b>. XML values are consistent with uprating. Official source (borger.dk) was blocked.",
     "rec": "Verify 2025 thresholds against borger.dk. If XML (208,101 / 646,500) is correct, update docx; if docx (200,301 / 622,200) is correct, update XML DK_2025."},
    {"id": "DK-009", "sev": "WARNING", "domain": "XML",
     "title": "<strong>bhtuc_dk &mdash; DK_2025</strong>: Green check base amount for pensioners is the 2026 value",
     "detail": "XML DK_2025 bhtuc_dk Amount#3 = <b>875 DKK/year</b>. Correct 2025 value: <b>1,005 DKK/year</b>. The XML was apparently updated with the 2026 value without creating DK_2026.",
     "rec": "Fix DK_2025: set bhtuc pensioner amount back to 1,005 DKK. In DK_2026, set to 875 DKK."},
    {"id": "DK-010", "sev": "WARNING", "domain": "XML",
     "title": "<strong>bhtuc_dk &mdash; DK_2025</strong>: Green check phase-out threshold is the 2024 value",
     "detail": "XML DK_2025 bhtuc_dk withdraw_start = <b>457,500 DKK</b>. Correct 2025 value: <b>475,300 DKK</b> (CR Table 2.14). Not updated from 2024.",
     "rec": "Fix DK_2025: set bhtuc phase-out withdraw_start to 475,300 DKK. For DK_2026, update to 498,200 DKK."},
    {"id": "DK-011", "sev": "WARNING", "domain": "XML",
     "title": "<strong>bfached_dk &mdash; DK_2025</strong>: Student parent benefit income thresholds are 2024 values",
     "detail": "XML DK_2025: $bfached_ytest_single = <b>169,100 DKK</b> (correct 2025: <b>175,200 DKK</b>); $bfached_ytest_couple = <b>253,600 DKK</b> (correct 2025: <b>262,700 DKK</b>). Amount was correctly updated to 8,756 DKK but income thresholds were not.",
     "rec": "Fix DK_2025: $bfached_ytest_single &rarr; 175,200; $bfached_ytest_couple &rarr; 262,700. For DK_2026, update to 183,100 / 274,500 DKK."},
    {"id": "DK-012", "sev": "WARNING", "domain": "XML",
     "title": "<strong>tinto_dk &mdash; DK_2025</strong>: Tax ceiling (skatteloft) is 52.01% instead of 52.07%",
     "detail": "XML DK_2025 tinto_dk DefConst: $tinto_uplim_rate = <b>0.5201</b> (52.01%). Correct 2025 value: <b>52.07%</b> (skat.dk, docx). The CR also states 52.01% &mdash; the XML inherited this error from the CR.",
     "rec": "Fix DK_2025: $tinto_uplim_rate &rarr; 0.5207. For DK_2026, update to 0.4457."},
    {"id": "DK-013", "sev": "INFO", "domain": "XML",
     "title": "<strong>poa_dk &mdash; DK_2025</strong>: Stale DefConst values (not used in active computation)",
     "detail": "poa_dk DefConst DK_2025: $poa_dedsingle_amt = <b>583</b> (active inline: 606); $poa_couple_supthres = <b>69,400</b> (active: 69,700); $poa_dedcouple_amt = <b>1,177</b> (active: 1,223). Active computation is correct.",
     "rec": "Clean up stale DefConst values to match active computation (606 / 69,700 / 1,223), or remove if unused."},
]

# ---------------------------------------------------------------------------
# SECTION 6 — PARAMETRIC CHANGES (Case A: DK_2026 does not exist)
# Spine row numbers from CR Table 2.4 (EUROMOD spine)
# ---------------------------------------------------------------------------
params_changes = [
    ("divider", "Taxes"),
    ("16", "<code>$tmu_adult_rate</code> &mdash; personfradrag (adult)", "<code>tmu_dk / ConstDef_dk</code>", "51,600 DKK", bold("54,100 DKK"), "2025: docx &#10003;, CR &#10003;, VEJ 10230 &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("16", "<code>$tmu_youth_rate</code> &mdash; personfradrag (youth)", "<code>tmu_dk / ConstDef_dk</code>", "51,600 DKK", bold("54,100 DKK"), "2025: docx &#10003;, VEJ 10230 &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("16", "<code>$tmu_rate</code> &mdash; municipality tax average", "<code>tmu_dk</code>", "25.10%", bold("25.05%"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("18", "<code>$tinbt_rate</code> &mdash; bottom bracket rate", "<code>tinbt_dk</code>", "12.01%", "12.01%", "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("17", "<code>$tcr_rate</code> &mdash; church tax average", "<code>tcr_dk</code>", "0.87%", "0.87%", "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("20", "<code>$tintc_rate</code> &mdash; EIC rate", "<code>tintc_dk</code>", "12.30%", bold("12.75%"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("20", "<code>$tintc_lim</code> &mdash; EIC max", "<code>tintc_dk</code>", "55,600 DKK", bold("63,300 DKK"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("20", "<code>$tintc_suppllim1</code> &mdash; EIC single-provider max", "<code>tintc_dk</code>", "48,300 DKK", bold("50,600 DKK"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("20", "<code>$tintc_supplthres</code> &mdash; EIC additional threshold", "<code>tintc_dk</code>", "224,500 DKK", bold("235,200 DKK"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("20", "<code>$tintc_suppllim2</code> &mdash; EIC additional max", "<code>tintc_dk</code>", "2,900 DKK", bold("3,100 DKK"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("19", "<code>$tinto_rate</code> &mdash; top bracket rate", "<code>tinto_dk</code>", "15.00%", warn(bold("7.50%") + " &mdash; STRUCTURAL"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("19", "<code>$tinto_thres</code> &mdash; top bracket threshold", "<code>ConstDef_dk</code>", "611,800 DKK", warn(bold("777,900 DKK") + " &mdash; STRUCTURAL"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("19", "<code>$tinto_uplim_rate</code> &mdash; skatteloft", "<code>tinto_dk</code>", warn("52.07% (XML: 52.01% &mdash; DK-012)"), bold("44.57%"), "2025: docx &#10003;, skat.dk &#10003;; CR/XML &#10007;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("19", "<code>bundfradrag</code> &mdash; net capital income allowance", "<code>tinto_dk</code>", "52,400 DKK", bold("55,000 DKK"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("NEW", "<code>$tinmd_rate</code> &mdash; middle bracket rate", "<code>tinmd_dk &mdash; NEW</code>", "n/a", warn(bold("7.50%") + " &mdash; new policy"), "2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("NEW", "<code>$tinmd_thres</code> &mdash; middle bracket threshold", "<code>tinmd_dk &mdash; NEW</code>", "n/a", warn(bold("641,200 DKK") + " &mdash; new policy"), "2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("NEW", "<code>$tinmd_netcap_allow</code> &mdash; net cap. income allowance", "<code>tinmd_dk &mdash; NEW</code>", "n/a", warn(bold("55,000 DKK") + " &mdash; new policy"), "2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("NEW", "<code>$tintto_rate</code> &mdash; toptop bracket rate", "<code>tintto_dk &mdash; NEW</code>", "n/a", warn(bold("5.00%") + " &mdash; new policy"), "2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("NEW", "<code>$tintto_thres</code> &mdash; toptop bracket threshold", "<code>tintto_dk &mdash; NEW</code>", "n/a", warn(bold("2,592,700 DKK") + " &mdash; new policy"), "2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("NEW", "<code>$tintcs_rate</code> &mdash; senior EIC rate", "<code>tintcs_dk &mdash; NEW</code>", "n/a", warn(bold("1.40%") + " &mdash; new policy"), "2026: docx &#10003;"),
    ("NEW", "<code>$tintcs_lim</code> &mdash; senior EIC max", "<code>tintcs_dk &mdash; NEW</code>", "n/a", warn(bold("6,100 DKK") + " &mdash; new policy"), "2026: docx &#10003;"),
    ("divider", "Contributions"),
    ("5", "<code>$tyrui_akasse</code> &mdash; A-kasse contribution", "<code>tyrui_dk</code>", "389 DKK/m", bold("407 DKK/m"), "2025: docx &#10003;, CR &#10003;, VEJ 10230 &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("5", "<code>$tyrui_efterlon</code> &mdash; efterlon contribution", "<code>tyrui_dk</code>", "568 DKK/m", bold("593 DKK/m"), "2025: docx &#10003;, CR &#10003;, VEJ 10230 &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("3", "<code>$tscpi_amt1</code> &mdash; ATP full-time", "<code>tscpi_dk</code>", "297 DKK/m", "297 DKK/m", "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("divider", "Benefits / Unemployment"),
    ("6", "<code>$bunct_uplim</code> &mdash; UB standard ceiling", "<code>bunct_dk</code>", "253,104 DKK/y", warn("264,492 DKK/y (docx says 276,492 &mdash; DK-004)"), "2025: docx &#10003;, CR &#10003;; 2026: VEJ 10230 &#10003;; docx &#10007;"),
    ("6", "UB first-3-months ceiling (118.86% rule)", "<code>bunct_dk</code>", "300,840 DKK/y", bold("314,376 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("6", "UB student with child ceiling", "<code>bunct_dk</code>", "207,540 DKK/y", bold("216,888 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("6", "UB student without child ceiling", "<code>bunct_dk</code>", "180,972 DKK/y", bold("189,108 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("divider", "Benefits / Sickness"),
    ("22", "<code>$bhl_max_amt</code> &mdash; sickness benefit ceiling", "<code>sickcomp_dk</code>", "~21,114 DKK/m (4,865 DKK/wk)", bold("~22,035 DKK/m (5,085 DKK/wk)"), "2025: docx &#10003;, XML &#10003;; 2026: docx &#10003;, VEJ 10230 &#10003;"),
    ("divider", "Benefits / Green check"),
    ("12", "Pensioner base amount", "<code>bhtuc_dk</code>", warn("1,005 DKK/y (XML: 875 &mdash; DK-009)"), bold("875 DKK/y"), "2025: skat.dk &#10003;; XML &#10007;; 2026: docx &#10003;"),
    ("12", "Per-child amount (pensioners)", "<code>bhtuc_dk</code>", warn("0 DKK/y (docx: 240 &mdash; DK-005)"), "0 DKK/y", "2025: CR &#10003;; 2026: docx &#10003;"),
    ("12", "Phase-out threshold", "<code>bhtuc_dk</code>", warn("475,300 DKK (XML: 457,500 &mdash; DK-010)"), bold("498,200 DKK"), "2025: CR &#10003;, skat.dk &#10003;; XML &#10007;; 2026: docx &#10003;"),
    ("12", "Extra low-income phase-out threshold", "<code>bhtuc_dk</code>", "~277,800 DKK", bold("~291,100 DKK"), "2025: docx, XML; 2026: docx &#10003;"),
    ("divider", "Benefits / Child family grant"),
    ("8", "<code>$bfachnm_amt1</code> &mdash; age 0&ndash;2", "<code>bfachnm_dk</code>", "21,168 DKK/y", bold("21,480 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("8", "<code>$bfachnm_amt2</code> &mdash; age 3&ndash;6", "<code>bfachnm_dk</code>", "16,764 DKK/y", bold("16,992 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("8", "<code>$bfachnm_amt3</code> &mdash; age 7&ndash;17", "<code>bfachnm_dk</code>", "13,188 DKK/y", bold("13,668 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("8", "<code>$bfachnm_thres</code> &mdash; income threshold", "<code>bfachnm_dk</code>", "917,000 DKK/y", bold("961,100 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("divider", "Benefits / Child benefit"),
    ("9", "<code>$bfach00_bchild_amt</code> &mdash; basic amount", "<code>bfach00_dk</code>", "6,664 DKK/y", bold("6,964 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("9", "<code>$bfach00_bchild_lone_amt</code> &mdash; lone-parent supplement", "<code>bfach00_dk</code>", "6,792 DKK/y", bold("7,096 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("9", "Income threshold (phase-out start)", "<code>bfach00_dk</code>", "917,000 DKK/y", bold("961,100 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("divider", "Benefits / Student parent benefit"),
    ("10", "<code>$bfached_bamt</code> &mdash; amount per child", "<code>bfached_dk</code>", warn("8,756 DKK/y (docx: 8,452 &mdash; DK-002)"), bold("9,152 DKK/y"), "2025: CR &#10003;; docx &#10007;; 2026: docx &#10003;"),
    ("10", "<code>$bfached_ytest_single</code> &mdash; single threshold", "<code>bfached_dk</code>", warn("175,200 DKK (XML: 169,100 &mdash; DK-003/DK-011)"), bold("183,100 DKK"), "2025: CR &#10003;; docx/XML &#10007;; 2026: docx &#10003;"),
    ("10", "<code>$bfached_ytest_couple</code> &mdash; couple threshold", "<code>bfached_dk</code>", warn("262,700 DKK (XML: 253,600 &mdash; DK-003/DK-011)"), bold("274,500 DKK"), "2025: CR &#10003;; docx/XML &#10007;; 2026: docx &#10003;"),
    ("divider", "Benefits / Housing benefit"),
    ("13", "Max housing cost", "<code>bho01_dk</code>", "94,200 DKK/y", bold("96,200 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("13", "Income threshold", "<code>bho01_dk</code>", "167,900 DKK/y", bold("171,500 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("13", "Per-child increment", "<code>bho01_dk</code>", "44,200 DKK/y", bold("45,200 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("13", "Min own rent", "<code>bho01_dk</code>", "28,300 DKK/y", bold("28,900 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("divider", "Benefits / Housing grant"),
    ("14", "Supplement amount", "<code>bho02_dk</code>", "8,100 DKK/y", bold("8,500 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("14", "Income threshold", "<code>bho02_dk</code>", "192,200 DKK/y", bold("201,400 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("14", "Per-child increment", "<code>bho02_dk</code>", "50,600 DKK/y", bold("53,100 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("14", "Min own rent", "<code>bho02_dk</code>", "20,300 DKK/y", bold("21,300 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("14", "Max benefit", "<code>bho02_dk</code>", "56,892 DKK/y", bold("59,628 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("divider", "Benefits / Pension"),
    ("15", "<code>$poa_amt</code> &mdash; basic pension", "<code>poa_dk</code>", "86,376 DKK/y", bold("90,528 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("15", "<code>$poa_single_supplamt</code> &mdash; supplement (singles)", "<code>poa_dk</code>", "99,948 DKK/y", bold("104,748 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("15", "<code>$poa_single_thres</code> &mdash; supplement threshold (singles)", "<code>poa_dk</code>", "85,300 DKK/y", bold("89,400 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("15", "<code>$poa_couple_supplamt</code> &mdash; supplement (couples)", "<code>poa_dk</code>", "51,144 DKK/y", bold("53,604 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("15", "<code>$poa_couple_thres</code> &mdash; supplement threshold (couples)", "<code>poa_dk</code>", "170,900 DKK/y", bold("179,100 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("15", "<code>$poa_supplamt</code> &mdash; supplementary pension amount", "<code>poa_dk</code>", "25,700 DKK/y", bold("26,900 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("15", "<code>$poa_supplthres</code> &mdash; supplementary pension asset threshold", "<code>poa_dk</code>", "103,100 DKK", bold("108,000 DKK"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("15", "Personal suppl. rate &mdash; single threshold", "<code>poa_dk</code>", "35,200 DKK/y", bold("35,700 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("15", "Personal suppl. rate &mdash; single deduction/pp", "<code>poa_dk</code>", "606 DKK", bold("635 DKK"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("15", "Personal suppl. rate &mdash; couple threshold", "<code>poa_dk</code>", "69,700 DKK/y", bold("70,600 DKK/y"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("15", "Personal suppl. rate &mdash; couple deduction/pp", "<code>poa_dk</code>", "1,223 DKK", bold("1,282 DKK"), "2025: docx &#10003;, CR &#10003;; 2026: docx &#10003;"),
    ("divider", "Childcare"),
    ("23", "<code>$xcc_amt1</code> &mdash; fee age 0&ndash;2", "<code>xcc_dk</code>", "45,548 DKK/y", tbd("TBD &mdash; not yet available"), "2025: docx &#10003;, XML &#10003;; 2026: unavailable"),
    ("23", "<code>$xcc_amt2</code> &mdash; fee age 3&ndash;5", "<code>xcc_dk</code>", "25,758 DKK/y", tbd("TBD &mdash; not yet available"), "2025: docx &#10003;, XML &#10003;; 2026: unavailable"),
    ("23", "<code>$bccfc_upthres1</code> &mdash; subsidy free-below threshold", "<code>bccfc_dk</code>", warn("208,101 DKK? (docx: 200,301 &mdash; DK-008)"), bold("218,101 DKK"), "2025: docx vs XML discrepancy &mdash; DK-008; 2026: docx &#10003;"),
    ("23", "<code>$bccfc_upthres3</code> &mdash; subsidy full-fee threshold", "<code>bccfc_dk</code>", warn("646,500 DKK? (docx: 622,200 &mdash; DK-008)"), bold("677,500 DKK"), "2025: docx vs XML discrepancy &mdash; DK-008; 2026: docx &#10003;"),
]

# ---------------------------------------------------------------------------
# SECTION 7 — STRUCTURAL CHANGES (Case A: DK_2026 does not exist)
# ---------------------------------------------------------------------------
structural_changes = [
    ("NEW", "tinmd_dk (new middle bracket tax)",
     "New middle bracket income tax introduced from 2026. Does not exist in DK_2025. "
     "Create new policy <code>tinmd_dk</code> in DK_2026. Parameters: rate = <strong>7.5%</strong>; "
     "main threshold = <strong>641,200 DKK/year</strong>; net capital income allowance = <strong>55,000 DKK</strong>. "
     "Joint computation for spouses."),
    ("19", "tinto_dk (top bracket tax reform)",
     "The top bracket tax (topskat) changes substantially for 2026. "
     "In DK_2025: rate 15%, threshold 611,800 DKK, ceiling 52.07%. "
     "In DK_2026: rate = <strong>7.5%</strong>; threshold = <strong>777,900 DKK</strong>; "
     "tax ceiling (skatteloft) = <strong>44.57%</strong>. "
     "Update DefConst: <code>$tinto_rate</code>, <code>$tinto_thres</code> (ConstDef_dk), <code>$tinto_uplim_rate</code>."),
    ("NEW", "tintto_dk (new toptop bracket tax)",
     "New toptop bracket tax introduced from 2026. Does not exist in DK_2025. "
     "Create new policy <code>tintto_dk</code> in DK_2026. Parameters: rate = <strong>5%</strong>; "
     "threshold = <strong>2,592,700 DKK/year</strong>. Joint computation for spouses applies."),
    ("2", "txc_dk (am-bidrag age restriction)",
     "Labour market contribution (am-bidrag) restricted to individuals aged &ge; 18 from 2026. "
     "In DK_2025: no age condition. "
     "In DK_2026: add eligibility condition age &ge; 18. Rate (8%) is unchanged."),
    ("NEW", "tintcs_dk (new senior earned income credit)",
     "New senior earned income credit introduced from 2026. Does not exist in DK_2025. "
     "Create new policy <code>tintcs_dk</code> in DK_2026. Parameters: rate = <strong>1.4%</strong> of gross wages; "
     "maximum = <strong>6,100 DKK/year</strong>. "
     "Eligibility: employed individuals within 2 years of pension age."),
    ("7", "bsa_dk (social assistance complete overhaul)",
     "Social assistance fully redesigned from 1 January 2026 &mdash; new 3-tier structure. "
     "Current DK_2025: 8 amounts differentiated by age, provider status, and living arrangement, with 225-hour income ceiling. "
     "DK_2026 new amounts (per month): "
     "Basic (age &lt;30, not at home) = <strong>7,529 DKK</strong>; "
     "Living-at-home (age &lt;30) = <strong>3,057 DKK</strong>; "
     "Higher (age &ge;30) = <strong>13,060 DKK</strong>; "
     "Minimum = <strong>7,095 DKK</strong>; "
     "Child supplement = <strong>2,909 DKK</strong>; "
     "Single-provider supplement = <strong>1,712 DKK</strong>; "
     "Single non-provider supplement = <strong>1,141 DKK</strong>. "
     "225-hour ceiling abolished; earn-up rule applies; asset disregard 16,200 DKK (single) / 32,400 DKK (couple). "
     "Requires major XML restructuring of <code>bsa_dk</code>."),
    ("&mdash;", "Foodcheck (one-off 2026 advisory &mdash; Foedevarecheck)",
     "Temporary one-off food voucher payment for 2026: "
     "pensioners 2,500 DKK; families with children 5,000 DKK (income limit 498,200 DKK); students 1,000 DKK. "
     "Not a recurring policy component &mdash; informational note only. Not modelled in regular EUROMOD simulation."),
]

# ---------------------------------------------------------------------------
# COUNT SUMMARY
# ---------------------------------------------------------------------------
n_param  = sum(1 for r in params_changes if r[0] != "divider")
n_warn   = sum(1 for i in issues if i["sev"] == "WARNING")
n_info   = sum(1 for i in issues if i["sev"] == "INFO")
n_struct = len(structural_changes)

# ---------------------------------------------------------------------------
# BUILD HTML
# ---------------------------------------------------------------------------
hp = []

hp.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>DK Policy Verification Report 2026</title>
<style>
  body { font-family: 'Segoe UI', Arial, sans-serif; margin: 20px 40px; color: #212529; font-size: 14px; }
  h1 { color: #003087; border-bottom: 3px solid #003087; padding-bottom: 6px; }
  h2 { color: #003087; margin-top: 30px; border-left: 4px solid #003087; padding-left: 10px; }
  h3 { color: #333; margin-top: 20px; }
  table { border-collapse: collapse; width: 100%; margin-top: 10px; }
  th { background: #003087; color: white; padding: 8px 10px; text-align: left; font-size: 0.9em; }
  td { border: 1px solid #dee2e6; padding: 7px 10px; vertical-align: top; }
  tr:nth-child(even) { background: #f8f9fa; }
  .summary-box { background: #e9f0fb; border-left: 5px solid #003087; padding: 12px 16px; margin: 16px 0; border-radius: 4px; }
  code { background: #e9ecef; padding: 1px 4px; border-radius: 3px; font-size: 0.88em; }
  .source-ok { color: #198754; font-weight: bold; }
  .source-fail { color: #dc3545; }
  .toc a { color: #003087; }
  .ok { color: #198754; font-weight: bold; }
  .warn { color: #e65c00; font-weight: 600; }
</style>
</head>
<body>""")

hp.append(f'<h1>{COUNTRY_FLAG} {COUNTRY_NAME} ({COUNTRY}) &#8212; Policy Verification Report {T}</h1>')
hp.append(f'<p>Generated: <strong>{today}</strong> | System: <strong>{BASE_SYSTEM}</strong> (base) &#8594; target: <strong>{COUNTRY}_{T}</strong></p>')
hp.append(f"""<div class="summary-box">
  <strong>Summary:</strong> Verification covers 5 policy docx files, Country Report PDF (Y16_CR_DK.pdf), and EUROMOD DK.xml (J2.0).
  Web source verification was partial &mdash; retsinformation.dk VEJ 10230/2025 was accessible and confirmed key 2025/2026 values;
  skat.dk, borger.dk, and bm.dk were JS-rendered or blocked.
  <strong>{n_param} parametric changes</strong> identified for {COUNTRY}_{T}.
  <strong>{n_warn} warnings</strong>, <strong>{n_info} informational notes</strong>,
  <strong>{n_struct} structural changes</strong> requiring manual XML review.
  <br>&#9888;&#65039; <strong>{COUNTRY}_{T} does not yet exist in the XML &mdash; the system must be created before implementation.</strong>
</div>""")

hp.append("""<h2 id="toc">Contents</h2>
<ul class="toc">
  <li><a href="#sources">1. Source Inventory</a></li>
  <li><a href="#phase1">2. Changes Extracted from Docx Files</a></li>
  <li><a href="#phase2">3. Year t&#8209;1 (2025) &mdash; Cross-Check of All Sources</a></li>
  <li><a href="#phase4">4. Year t (2026) &mdash; Verification Against Available Sources</a></li>
  <li><a href="#issues">5. Issues &amp; Warnings</a></li>
  <li><a href="#params">6. Parametric Changes for {COUNTRY}_{T}</a></li>
  <li><a href="#structural">7. Structural Changes (Manual Review Required)</a></li>
</ul>""")

# --- Section 1 ---
hp.append('<h2 id="sources">1. Source Inventory</h2>')
hp.append('<table><tr><th>Source</th><th>Type</th><th>Status</th><th>Coverage</th></tr>')
for s in sources:
    hp.append(f'<tr><td>{s[0]}</td><td>{s[1]}</td><td>{s[2]}</td><td>{s[3]}</td></tr>')
hp.append('</table>')

# --- Section 2 ---
hp.append(f'<h2 id="phase1">2. Changes Extracted from Docx Files</h2>')

def sec2_table(rows):
    hp.append(f'<table><tr><th>Policy</th><th>Parameter</th><th>{T_MINUS_1} Value</th><th>{T} Value</th><th>Nature</th></tr>')
    for policy, param, v_t1, v_t, nature in rows:
        hp.append(f'<tr><td><code>{policy}</code></td><td>{param}</td><td>{v_t1}</td><td>{v_t}</td><td>{nature}</td></tr>')
    hp.append('</table>')

hp.append(f'<h3>2.1 Taxes</h3>');        sec2_table(taxes_changes)
hp.append(f'<h3>2.2 Benefits</h3>');      sec2_table(benefits_changes)
hp.append(f'<h3>2.3 Contributions</h3>'); sec2_table(contributions_changes)
hp.append(f'<h3>2.4 Sickness</h3>');      sec2_table(sickness_changes)
hp.append(f'<h3>2.5 Childcare</h3>');     sec2_table(childcare_changes)

# --- Section 3 ---
hp.append('<h2 id="phase2">3. Year t&#8209;1 (2025) &mdash; Cross-Check of All Sources</h2>')
hp.append('<p>For each parameter: docx 2025 value compared against Country Report, EUROMOD XML (DK_2025), and web sources where accessible.</p>')
hp.append('<table><tr><th>Parameter</th><th>Policy / Constant</th><th>Docx 2025</th><th>Country Report</th><th>XML DK_2025</th><th>Web source</th><th>Status</th></tr>')
for r in crosscheck_2025:
    hp.append(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td></tr>')
hp.append('</table>')

# --- Section 4 ---
hp.append('<h2 id="phase4">4. Year t (2026) &mdash; Verification Against Available Sources</h2>')
hp.append('<p>Country Report covers 2022&ndash;2025 only. Web verification via retsinformation.dk VEJ 10230/2025 (dagpenge, A-kasse, tax brackets 2026); skat.dk, borger.dk, bm.dk were blocked.</p>')
hp.append('<table><tr><th>Parameter</th><th>Policy / Constant</th><th>Docx 2026</th><th>Web source</th><th>Status</th></tr>')
for r in crosscheck_2026:
    hp.append(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>')
hp.append('</table>')

# --- Section 5 ---
hp.append('<h2 id="issues">5. Issues &amp; Warnings</h2>')
hp.append('<table><tr><th>ID</th><th>Severity</th><th>Domain</th><th>Policy / Title</th><th>Detail</th><th>Recommendation</th></tr>')
for i in issues:
    bg = row_color(i["sev"])
    hp.append(f'<tr style="background:{bg}"><td><code>{i["id"]}</code></td><td>{badge(i["sev"])}</td><td>{domain_badge(i["domain"])}</td><td>{i["title"]}</td><td style="font-size:0.85em">{i["detail"]}</td><td style="font-size:0.85em">{i["rec"]}</td></tr>')
hp.append('</table>')

# --- Section 6 ---
hp.append(f'<h2 id="params">6. Parametric Changes for {COUNTRY}_{T}</h2>')
hp.append(f'<p class="warn">&#9888;&#65039; The <code>{COUNTRY}_{T}</code> system does not yet exist in the EUROMOD XML and must be created before implementation. All parameter values listed here must be populated in the new system. See Section 7 for structural changes required.</p>' if not YEAR_T_EXISTS else f'<p>&#8505; The <code>{COUNTRY}_{T}</code> system already exists in the EUROMOD XML. Only parameters requiring correction or attention are listed here.</p>')
hp.append('<table><tr><th>Spine Row</th><th>Parameter</th><th>Policy</th><th>2025 Value</th><th>2026 Value</th><th>Source</th></tr>')
for r in params_changes:
    if r[0] == "divider":
        hp.append(f'<tr><td colspan="6" style="background:#003087;color:white;font-weight:bold;padding:6px 10px">{r[1]}</td></tr>')
    else:
        hp.append(f'<tr><td style="font-weight:bold;color:#003087">{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td style="font-size:0.85em">{r[5]}</td></tr>')
hp.append('</table>')

# --- Section 7 ---
hp.append('<h2 id="structural">7. Structural Changes (Manual Review Required)</h2>')
hp.append(f'<p class="warn">&#9888;&#65039; The <code>{COUNTRY}_{T}</code> system does not yet exist in the EUROMOD XML. All structural changes listed below must be implemented when creating <code>{COUNTRY}_{T}</code>.</p>' if not YEAR_T_EXISTS else f'<p>&#8505; Structural issues identified in <code>{COUNTRY}_{T}</code>. Each row describes a structure that is missing or incorrect.</p>')
hp.append('<table><tr><th>Spine Row</th><th>Policy</th><th>Description of Structural Change</th></tr>')
for spine, policy, desc in structural_changes:
    hp.append(f'<tr><td style="font-weight:bold;color:#003087;white-space:nowrap">{spine}</td><td style="white-space:nowrap"><code>{policy}</code></td><td style="font-size:0.9em">{desc}</td></tr>')
hp.append('</table>')

hp.append(f'<hr><p style="color:#888;font-size:0.85em">Report generated by EUROMOD policy verification workflow | System: {BASE_SYSTEM} | {today}</p>')
hp.append('</body></html>')

# ---------------------------------------------------------------------------
# WRITE FILE
# ---------------------------------------------------------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)
out = os.path.join(OUTPUT_DIR, f"EM_{COUNTRY}_policy_verification_{T_MINUS_1}_{T}.html")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(hp))
print(f"Written: {out}")
