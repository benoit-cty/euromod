# 06 — Ingest published-but-unconsolidated acts from BOE's daily gazette

Status: ready-for-agent
Blocked by: 01 (done), 02 (done)

## Why

Issue 01 found where the regional **amounts** actually are: the annual budget
laws (Asturias Ley 8/2024 `BOE-A-2025-3124`, País Vasco Ley 8/2024
`BOE-A-2025-940`, Madrid Ley 9/2024 `BOE-A-2025-5524`, Aragón Decreto-ley
1/2025 `BOE-A-2025-12536`, Canarias Ley 7/2022 `BOE-A-2023-5961`). BOE
publishes them and never consolidates them (`estado_consolidacion codigo="0"`),
so `legislacion-consolidada/id/<ID>` answers 404 and `EsResolver` now refuses
their ELI with exactly that message. Without them, every `bsarg_es` regional
amount stays `not_found` even with the framework laws ingested — and the same
is true of the state budget law (Ley 31/2022, the IPREM case) and of every
state act the golden set marks `corpus_available: false`.

## What exists (verified 2026-09-08)

`https://www.boe.es/diario_boe/xml.php?id=BOE-A-2025-3124` → HTTP 200,
`application/xml`, 272 kB: `<documento fecha_actualizacion=…><metadatos>`
(`identificador`, `origen_legislativo codigo="2"` *Autonómico*, `departamento`,
`rango`, `fecha_disposicion`, `numero_oficial`, `titulo`, `fecha_publicacion`,
`fecha_vigencia`, `estatus_derogacion`, `estado_consolidacion codigo="0"`) then
`<analisis>` (materias, `<anterior>` references) and `<texto>` with
`<p class="articulo">` / `<p class="parrafo">` paragraphs and `<table>`s — the
same paragraph classes the consolidated `<version>` bodies use, without the
`<bloque>`/`<version>` wrapper.

## What to build

1. `countries/es/fetcher.py`: a second URL form, `diario_url(boe_id)`, chosen
   when the consolidated fetch 404s (or when the resolver already knows the act
   is unconsolidated); keep the `Accept: application/xml` header logic.
2. `countries/es/parser.py`: `parse_boe_diario_xml` — split `<texto>` at
   `<p class="articulo">` / disposición headings into units, one version each
   with `validity = [fecha_vigencia,)`, `version_status = 'as_published'` (or
   whatever the IR calls the eISB-style as-enacted text; IE already has this
   case). Reuse the paragraph/table renderer of `_parse_versions`.
3. Jurisdiction: `origen_legislativo` plays the role of `ambito`; the ELI in
   `<analisis>`/`<eli>` or `departamento` places the act through
   `regions.jurisdiction_for` unchanged.
4. Resolver: turn the "published but not consolidated" refusal into a
   `SourceRef` with `source_type="diario"`.
5. Tests: an inline fixture trimmed from `BOE-A-2025-3124` with one article
   and one table; a jurisdiction assertion (`ES-AS`).
6. Then ingest the five acts above, embed, and re-run issue 05's golden cases:
   Aragón's `$bsarg_rg24_basic_amt` should move from `not_found` to a proposal
   citing `DL 1/2025 Aragón`.

## Watch out

- Budget laws are superseded yearly: without consolidation nothing closes the
  previous year's version. Either close `validity` at the next vintage's
  `fecha_vigencia` on ingest of the successor, or accept overlapping open
  versions and let the critique's budget-act window (already built for FR)
  arbitrate. Decide before ingesting two vintages of the same region.
- `estado_consolidacion codigo="0"` acts also include state instruments the
  golden set needs (Ley 31/2022). Design the path country-neutral inside the
  ES adapter; do not special-case "regional".
