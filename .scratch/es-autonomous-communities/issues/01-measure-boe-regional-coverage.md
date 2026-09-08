# 01 — Measure how much regional social law BOE actually consolidates

Status: resolved
Blocks: 02, 03, 04

## Question

Feasibility is proven for exactly one regional act (Galicia's Decreto
Legislativo 1/2011, fetches 200). Before designing anything, find out how many
of the 14 regions in `bsarg_es`/`bchrg_es` have their minimum-income and child-
benefit legislation in BOE's *consolidated* database, as opposed to only in
their own diario oficial.

## Method

1. Extract the `**Legal sources**` block from each region's subsection of the
   Country Report (`08 - EUROMOD Triangulator/country-reports/Y16/ES_Y16.md`,
   `bsarg_es` starts line 9191, `bchrg_es` line 6497). These name the acts.
2. For each named act, find its BOE id. The open-data `query=` endpoint is
   dead (HTTP 500), so use the boe.es web search over legislación consolidada
   and record the id; note where no consolidated entry exists at all.
3. Verify each candidate id fetches:
   `curl -H 'Accept: application/xml' https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/<ID>`
4. Record `ambito`, `ambito_codigo` and `departamento` from the payload
   metadata for each — these are what issue 02 keys the region off.

## Deliverable

A table, one row per (region, act): CCAA, NUTS-2 code, act name from the CR,
BOE id or "not consolidated", HTTP status, `departamento` string. Attach it to
this issue under `## Answer`. It decides whether this effort covers 14 regions,
3, or none — and issue 02's design depends on the answer.

## Notes

Do not ingest anything yet. Issue 03 decides the jurisdiction model first, and
ingesting under the wrong one means re-ingesting.

## Answer (2026-09-08)

Method actually used: BOE's search API is dead, but **BOE resolves ELI URLs for
autonomous-community acts** — `https://www.boe.es/eli/es-cn/l/2022/12/19/5/con`
returns the consolidated act as HTML with the BOE id in `<title>` (an unknown
ELI returns an HTTP 200 "Error 404" page, so the title is the signal). The
`/con` form resolves only when BOE *consolidates* the act; the plain form
resolves when BOE merely *published* it. Every act below was probed both ways
and every id then fetched from `legislacion-consolidada/id/<ID>` with
`Accept: application/xml` (script: scratchpad `probe_boe.py`).

| Family | Region (NUTS-2, code) | Act as the Country Report names it | BOE id | Consolidated API | `departamento` |
|---|---|---|---|---|---|
| bsarg | Asturias (ES12, ES-AS) | Ley del Principado de Asturias 8/2024, de 27 de diciembre, de Presupuestos Generales para 2025 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Asturias (ES12, ES-AS) | Ley 4/2023, de 29 de diciembre, de Presupuestos Generales para 2024 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Asturias (ES12, ES-AS) | Ley 3/2021, de 30 de junio, de Garantía de Derechos y Prestaciones Vitales | `BOE-A-2021-13685` | 200 — Ley, Finalizado, 143 blocks / 143 versions | Comunidad Autónoma del Principado de Asturias |
| bsarg | Asturias (ES12, ES-AS) | Decreto 29/2011, de 13 de abril, Reglamento General de la Ley 4/2005 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | País Vasco (ES21, ES-PV) | Ley 8/2024, de 20 de diciembre, Presupuestos Generales de Euskadi 2025 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | País Vasco (ES21, ES-PV) | Ley 21/2023, de 22 de diciembre, Presupuestos Generales de Euskadi 2024 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | País Vasco (ES21, ES-PV) | Ley 14/2022, de 22 de diciembre, del Sistema Vasco de Garantía de Ingresos y para la Inclusión | `BOE-A-2023-1405` | 200 — Ley, Finalizado, 210 blocks / 225 versions | Comunidad Autónoma del País Vasco |
| bsarg | País Vasco (ES21, ES-PV) | Ley 18/2008, de 23 de diciembre, para la Garantía de Ingresos y para la Inclusión Social | `BOE-A-2011-15732` | 200 — Ley, Finalizado, 149 blocks / 187 versions | Comunidad Autónoma del País Vasco |
| bsarg | País Vasco (ES21, ES-PV) | Decreto 173/2023, de 21 de noviembre, Reglamento de la Renta de Garantía de Ingresos | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Navarra (ES22, ES-NC) | Ley Foral 15/2016, de 11 de noviembre, derechos a la Inclusión Social y a la Renta Garantizada | `BOE-A-2016-11671` | 200 — Ley Foral, Finalizado, 62 blocks / 73 versions | Comunidad Foral de Navarra |
| bsarg | Navarra (ES22, ES-NC) | Orden Foral 10/2025, de 30 de enero, cuantía de la renta garantizada 2025 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Navarra (ES22, ES-NC) | Decreto Foral 26/2018, de 25 de abril | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Aragón (ES24, ES-AR) | Decreto-Ley 1/2025, de 9 de abril, del Gobierno de Aragón (prestaciones 2025) | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Aragón (ES24, ES-AR) | Ley 17/2023, de 22 de diciembre, de Presupuestos de Aragón 2024 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Aragón (ES24, ES-AR) | Ley 8/2022, de 29 de diciembre, de Presupuestos de Aragón 2023 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Aragón (ES24, ES-AR) | Ley 3/2021, de 20 de mayo (Prestación Aragonesa Complementaria del IMV) | `BOE-A-2021-10673` | 200 — Ley, Finalizado, 37 blocks / 38 versions | Comunidad Autónoma de Aragón |
| bsarg | Aragón (ES24, ES-AR) | Decreto-Ley 5/2020, de 29 de junio, Prestación Aragonesa Complementaria del IMV | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Aragón (ES24, ES-AR) | Decreto 161/2021, de 13 de octubre (reglamento PACIMV) | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Madrid (ES30, ES-MD) | Ley 9/2024, de 26 de diciembre, de Presupuestos Generales de la Comunidad de Madrid 2025 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Madrid (ES30, ES-MD) | Ley 15/2023, de 27 de diciembre, de Presupuestos Generales de la Comunidad de Madrid 2024 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Madrid (ES30, ES-MD) | Ley 4/2021, de 23 de diciembre, de Presupuestos Generales de la Comunidad de Madrid 2022 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Madrid (ES30, ES-MD) | Ley 15/2001, de 27 de diciembre, de Renta Mínima de Inserción (framework, not in the CR list) | `BOE-A-2002-4378` | 200 — Ley, Finalizado, 68 blocks / 87 versions | Comunidad de Madrid |
| bsarg | Madrid (ES30, ES-MD) | Decreto 126/2014, de 20 de noviembre, Reglamento RMI | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Castilla-La Mancha (ES42, ES-CM) | Ley 5/1995, de 23 de marzo, de Solidaridad en Castilla-La Mancha (IMS framework) | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Castilla-La Mancha (ES42, ES-CM) | Decreto 179/2002, de 17 de diciembre, Ingreso Mínimo de Solidaridad | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Cataluña (ES51, ES-CT) | Llei 14/2017, del 20 de juliol, de la renda garantida de ciutadania | `BOE-A-2017-9799` | 200 — Ley, Desactualizado, 53 blocks / 66 versions | Comunidad Autónoma de Cataluña |
| bsarg | Cataluña (ES51, ES-CT) | Decreto 55/2020, de 28 de abril, Reglamento de la Ley 14/2017 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Illes Balears (ES53, ES-IB) | Ley 4/2023, de 27 de febrero, de prestaciones sociales de carácter económico | `BOE-A-2023-13761` | 200 — Ley, Finalizado, 133 blocks / 154 versions | Comunidad Autónoma de las Illes Balears |
| bsarg | Illes Balears (ES53, ES-IB) | Ley 5/2021, de 28 de diciembre, de Presupuestos Generales Illes Balears 2022 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Illes Balears (ES53, ES-IB) | Decreto ley 10/2020, de 12 de junio, de prestaciones sociales de carácter económico | `BOE-A-2020-8013` | 200 — Decreto-ley, Finalizado, 119 blocks / 127 versions | Comunidad Autónoma de las Illes Balears |
| bsarg | Illes Balears (ES53, ES-IB) | Ley 5/2016, de 13 de abril, de la renta social garantizada | `BOE-A-2016-4178` | 200 — Ley, Finalizado, 52 blocks / 56 versions | Comunidad Autónoma de las Illes Balears |
| bsarg | Ceuta (ES63, ES-CE) | Reglamento del Ingreso Mínimo de Inserción Social (BOCCE 4793, 21-11-2008; mod. BOCCE 4996, 2-11-2010) | — | no BOE form at all (city/regional bulletin only) |  |
| bsarg | Melilla (ES64, ES-ML) | Reglamento regulador de las ayudas económicas y servicios (Resolución 696, BOME extr. 4, 9-2-2018) | — | no BOE form at all (city/regional bulletin only) |  |
| bsarg | Canarias (ES70, ES-CN) | Ley 5/2022, de 19 de diciembre, de la renta canaria de ciudadanía | `BOE-A-2023-2940` | 200 — Ley, Finalizado, 93 blocks / 96 versions | Comunidad Autónoma de Canarias |
| bsarg | Canarias (ES70, ES-CN) | Ley 7/2022, de 28 de diciembre, de Presupuestos Generales de Canarias 2023 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Canarias (ES70, ES-CN) | Ley 6/2021, de 28 de diciembre, de Presupuestos Generales de Canarias 2022 | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Canarias (ES70, ES-CN) | Decreto-ley 3/2021, de 18 de marzo (modifica Ley 1/2007 PCI) | `BOE-A-2021-9007` | 200 — Decreto-ley, Finalizado, 9 blocks / 9 versions | Comunidad Autónoma de Canarias |
| bsarg | Canarias (ES70, ES-CN) | Decreto-ley 16/2020, de 24 de septiembre (PCI / IMV compatibility) | not consolidated | ELI `/con` → 404 page |  |
| bsarg | Canarias (ES70, ES-CN) | Ley 1/2007, de 17 de enero, Prestación Canaria de Inserción | `BOE-A-2007-4066` | 200 — Ley, Finalizado, 67 blocks / 111 versions | Comunidad Autónoma de Canarias |
| bchrg | Galicia (ES11, ES-GA) | Orden de 30 de diciembre de 2024 (Tarjeta Benvida 2025, DOG) | not consolidated | ELI `/con` → 404 page |  |
| bchrg | Galicia (ES11, ES-GA) | Ley 3/2011, de 30 de junio, de apoyo a la familia y a la convivencia de Galicia (framework, not in the CR list) | `BOE-A-2011-13120` | 200 — Ley, Finalizado, 183 blocks / 188 versions | Comunidad Autónoma de Galicia |
| bchrg | Asturias (ES12, ES-AS) | Resolución de 3 de abril de 2023, Consejería de Derechos Sociales y Bienestar (BOPA) | — | no BOE form at all (city/regional bulletin only) |  |
| bchrg | Cantabria (ES13, ES-CB) | Decreto 23/2015, de 23 de abril (natalidad), mod. Decreto 26/2016 y Decreto 66/2020 (BOC) | not consolidated | ELI `/con` → 404 page |  |
| bchrg | País Vasco (ES21, ES-PV) | Decreto 27/2023, de 21 de febrero, de ayudas a las familias con hijas o hijos (BOPV) | not consolidated | ELI `/con` → 404 page |  |
| bchrg | Aragón (ES24, ES-AR) | Orden BSF/1325/2024, de 23 de octubre (partos múltiples 2024, BOA) | not consolidated | ELI `/con` → 404 page |  |
| bchrg | Madrid (ES30, ES-MD) | Acuerdo de 9 de diciembre de 2021, del Consejo de Gobierno (BOCM) | — | no BOE form at all (city/regional bulletin only) |  |
| bchrg | Castilla-La Mancha (ES42, ES-CM) | Decreto 80/2012, de 26 de abril (familias numerosas), mod. Decreto 108/2014 (DOCM) | not consolidated | ELI `/con` → 404 page |  |
| bchrg | Cataluña (ES51, ES-CT) | Orden TSF/251/2016, de 19 de septiembre (DOGC) | not consolidated | ELI `/con` → 404 page |  |
| bchrg | Andalucía (ES61, ES-AN) | Decreto-Ley 7/2013, de 30 de abril, medidas contra la exclusión social en Andalucía | not consolidated | ELI `/con` → 404 page |  |
| bchrg | Andalucía (ES61, ES-AN) | Orden de 6 de mayo de 2002 (ayudas por menores y partos múltiples, BOJA) | — | no BOE form at all (city/regional bulletin only) |  |

Departamento strings of the other communities, read off consolidated acts BOE
does hold (their framework social laws): ES-AN `BOE-A-2017-657` «Comunidad Autónoma de Andalucía», ES-CB `BOE-A-2007-8186` «Comunidad Autónoma de Cantabria», ES-CM `BOE-A-2011-2752` «Comunidad Autónoma de Castilla-La Mancha», ES-EX `BOE-A-2019-3491` «Comunidad Autónoma de Extremadura», ES-RI `BOE-A-2017-5627` «Comunidad Autónoma de La Rioja», ES-MC `BOE-A-2008-12493` «Comunidad Autónoma de la Región de Murcia».
Castilla y León's DLeg 1/2019 and Comunitat Valenciana's Ley 19/2017 are not
consolidated.

### What it means

1. **BOE consolidates the communities' *framework* laws** — rank of law only
   (Ley, Ley Foral, Decreto-ley, Decreto Legislativo). Present for 12 of the 14
   regions in `bsarg_es`/`bchrg_es`; Ceuta and Melilla legislate by city
   *reglamento* in the BOCCE/BOME, which BOE never carries.
2. **BOE consolidates no annual budget law.** Asturias's Ley 8/2024, País
   Vasco's Ley 8/2024, Madrid's Ley 9/2024, Canarias's Ley 7/2022 and Aragón's
   Decreto-ley 1/2025 are all *published* (`BOE-A-2025-3124`, `-940`, `-5524`,
   `BOE-A-2023-5961`, `BOE-A-2025-12536`) and none is consolidated
   (`estado_consolidacion codigo="0"`; the API 404s on the id). Those are the
   acts that carry the **2025 amounts**. They are reachable through a different
   endpoint, `https://www.boe.es/diario_boe/xml.php?id=<ID>` (verified: 200,
   `<documento><metadatos>…<texto>` with `<p class="articulo">` headings and
   tables, one version) — a second fetch/parse path, tracked as issue 06.
3. **No regional decreto, orden, resolución or acuerdo is in BOE** — which is
   every `bchrg_es` source and the amount-setting instruments of Navarra
   (Orden Foral), Castilla-La Mancha (Resolución), Galicia (Orden), Madrid's
   reglamento. Those need the regional diario, a separate source per region.
4. The consolidated framework laws almost never state the EUROMOD amounts
   (grep of all 14 payloads for the 2025 values: none; Ley 5/2016 Balears states
   2016 amounts, Ley 15/2001 Madrid 2002 amounts in pesetas, Ley 1/2007 Canarias
   a 130,41 floor). They are still the right corpus for eligibility rules and
   for the *state ↔ region* scoping proof, and they are what the ELI/ALIAS
   resolver now covers.

Ingested (2026-09-08, under their child jurisdictions): the 14 consolidated
acts above plus Cantabria's Ley 2/2007 (`BOE-A-2007-8186`).
