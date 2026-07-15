# EUROMOD-Assisted Parameter Update Format - Proposal for Validation

*Draft for discussion with the EUROMOD team.*

## 1. Purpose

The proof of concept assists a person updating EUROMOD parameters. For one existing parameter, it must:

1. receive the parameter and its history from the EUROMOD team;
2. select the relevant model value for a system year;
3. search authoritative sources for a candidate value;
4. show the candidate, exact supporting text, and citation;
5. let a person accept, reject, or request a revision.

The pipeline is **export-first and human-gated**. It never writes directly into EUROMOD.

The proposal is based on the files already received after a first draft format:

- `extracted_parameters/FR.policy.json` - the base parameter export;
- `extracted_parameters/enriched/FR.enriched.json` - the same export with existing enrichment.

The POC should preserve this work rather than introduce a completely different format.

## 2. What is already in the enriched French export

The large file was analysed with `jq`. It contains:

| Observation | Result |
|---|---:|
| Parameter records | 702 |
| Value-history rows | 3,886 |
| Top-level shape | 702 records with `information` and `values` |
| Unique `model_target` values | 702 |
| Exported target kind | 702 `def_const` constants |
| `value_type` | 702 `scalar` |
| Numeric value rows | 2,961 |
| String value rows | 925 |
| Rows whose value is `"n/a"` | 758 |
| Parameters with `coicop` | 227 |
| `usage.defined_in` entries | 705 |
| `usage.used_by` entries | 5,368 |

Every `information` object contains:

```text
country, model_target, spine_order, value_type, unit,
label, short_label, description, explanation,
last_confirmed_valid_on, classification,
usage, enrichment_lineage
```

`coicop` is additionally present for 227 consumption-tax parameters.

Every existing `values[]` row contains:

```text
value, valid_from, valid_to,
legal_status, source_type, official_journal_date,
references, lineage
```

This is already close to the needs of the assisted updater. The main requirement is therefore to identify who supplies or fills each field.

## 3. Data ownership and processing stages

The proposed exchange record keeps the existing `information + values[]` envelope and adds proposal and review blocks. Comments in [`parameter_sample.jsonc`](parameter_sample.jsonc) use the same four labels as this section.

### Stage A - received from the EUROMOD team

For the POC, `FR.enriched.json` is the received input contract. The POC treats its existing content as read-only source data.

The underlying base export already contains:

- `country`, `model_target`, `spine_order`, `value_type`, and `unit`;
- `label`, `description`, `explanation`, and `classification`;
- the complete `values[]` history;
- the raw EUROMOD representation in `values[].lineage.model_answer`;
- the source model identifier in `values[].lineage.model`.

The enriched file additionally contains or improves:

- `short_label` for all 702 parameters;
- `description` for all 702 parameters;
- `usage` for all 702 parameters;
- `enrichment_lineage` for all 702 parameters;
- `coicop` for 227 parameters;
- adjusted `unit` values for 211 parameters.

The comparison found the same 702 targets and no changes to any of the 3,886 value-history rows. This means the enrichment adds context while preserving model values.

The POC must not ask the value-search agent to regenerate labels, descriptions, classification, COICOP, or usage information that has already been supplied.

### Stage B - deterministic POC post-processing

This stage performs small, explainable transformations. It does not use an LLM and does not invent policy facts.

It may add:

- a structured `model_address`, parsed from `model_target`;
- `model_release`, parsed from `values[].lineage.model` when possible;
- `raw_euromod_value`, renamed from `lineage.model_answer` for clarity;
- a structured unit view while preserving the received `unit`;
- an optional `parameter_group`, based on an EUROMOD-team-approved mapping;
- a simple comparison between the current model value and a proposal.

The normalization rules for the POC are intentionally modest:

1. Preserve the received fields for traceability.
2. Convert a received model value of `"n/a"` to normalized `value: null`, but preserve `raw_euromod_value: "n/a"`.
3. Preserve formulas such as `$PSS * 4` or `0.6 * 6/12 + 0.4 * 6/12` as raw text. Formula parsing is not required.
4. Do not infer a legal effective date from a EUROMOD system year.
5. Do not silently correct questionable labels or units. Keep the received value and mark any normalized interpretation as post-processing.

### Stage C - agentic value search

The agent searches legislation or another permitted source and creates a new entry in `proposals[]`. It does not overwrite `values[]`.

The agent may supply:

- `proposed_value`;
- `effective_from` and `effective_to`, only when supported by the source;
- `source_class`;
- `legal_status`, when applicable;
- `official_journal_date`;
- one or more references;
- an exact `supporting_extract`;
- the cited RAG `chunks.id` as `jrc_database_id`;
- extraction lineage and confidence;
- a note explaining uncertainty or why the parameter should be routed to the national team.

The central anti-hallucination rule remains mechanical:

> For legislation-sourced proposals, `supporting_extract` must occur character-for-character in the cited RAG chunk before the proposal can be accepted.

The agent is allowed to say that it cannot determine the value. It must not manufacture a citation or explain a model/legal difference without evidence.

### Stage D - human review

The validation UI appends entries to `review_decisions[]`:

```text
accepted | rejected | needs_revision
```

A decision records the proposal id, reviewer, timestamp, and note. Previous decisions are retained. An empty list means that the proposal is pending.

## 4. Keep the existing parameter identity

The received export uses:

```text
euromod://FR/tinkt_fr/def_const/$tin_upthres1
```

`model_target` remains the canonical compatibility identifier for the POC. Post-processing may expose its parts for the UI and database:

```json
{
  "country": "FR",
  "policy": "tinkt_fr",
  "function": "def_const",
  "kind": "constant",
  "name": "$tin_upthres1"
}
```

This structured view is derived; it is not a request for the EUROMOD team to change the existing URI immediately. The team should confirm whether these parsed components are correct and sufficient for eventual write-back.

## 5. Keep model history separate from proposals

The received `values[]` rows describe the values found in the exported model. For `$tin_upthres1`, the enriched file contains:

| Model year derived from `valid_from` | Received value | Raw EUROMOD value |
|---:|---:|---|
| 2023 | 10,777 | `10777#y` |
| 2024 | 11,294 | `11294#y` |
| 2025 | 11,496 | `11496#y` |

The cited version of CGI article 197 states `11 497 EUR`. The POC should display both facts:

- **existing model value:** 11,496 for the 2025 system in release J2.19;
- **agent proposal:** 11,497, supported by the cited legal extract.

The agent must not replace the existing history. The reviewer decides whether a model update is appropriate and may ask the national team why the values differ.

### Model release and system year

The received lineage contains:

```text
euromod-connector:EUROMOD_MASTER_VERSION_J2.19
```

Post-processing can derive `model_release: "J2.19"`. For the latest annual row it can select `system_year: 2025` from the interval beginning at `valid_from: "2025-01-01"`.

Some received rows cover several years. In that case `valid_from` and `valid_to` remain the model interval, while `system_year` is the particular year being reviewed within that interval. It must not always be treated as a rename of the `valid_from` year.

Both are useful because a later release may revise the same system year. The original `valid_from`, `valid_to`, and lineage fields remain available until the EUROMOD team confirms that these derivations are reliable across countries.

### Model dates versus legal dates

All 3,886 received `valid_from` dates are 1 January, and every non-null `valid_to` is 31 December. For this POC, these dates are treated as model applicability intervals.

Legal dates belong in the proposal as `effective_from` and `effective_to`. They are filled only when the source establishes them. A legal date may therefore remain `null` even when the system year is known.

## 6. Values and units

### Literal, unavailable, and expression values

The received data uses the same `value` field for several representations:

```json
11496
"n/a"
"$PSS * 4"
"0.6 * 6/12 + 0.4 * 6/12"
```

The normalized POC view uses:

| Received value | Normalized value | Raw value retained |
|---|---|---|
| `11496` | `11496` | `"11496#y"` |
| `"n/a"` | `null` | `"n/a"` |
| `"$PSS * 4"` | `null` | `"$PSS * 4"` |
| weighted expression | `null` | complete expression |

Using `null` means “no normalized scalar is available”; it does not mean zero. Expressions remain visible to the reviewer, but the POC does not evaluate them.

### Units

The received `unit` remains authoritative input, for example `currency/year`. Post-processing may add:

```json
{
  "quantity": "money",
  "currency": "EUR",
  "period": "year",
  "euromod_suffix": "#y"
}
```

This structured unit is a convenience view. It is not allowed to hide the original value because the French data still contains questionable combinations, such as rates labelled `currency`.

## 7. Optional parameter groups

The received export correctly stores schedule components as separate scalar constants:

```text
$tin_upthres1 ... $tin_upthres5
$tin_rate1 ... $tin_rate6
```

The POC keeps every constant and `model_target` unchanged. Post-processing may optionally add:

```json
{
  "id": "FR:tinkt_fr:income_tax_schedule",
  "kind": "bracket_schedule",
  "role": "upper_threshold",
  "index": 1
}
```

This is only a display and retrieval hint. It does not combine values into an array and does not change write-back. Group mappings must be supplied or validated by the EUROMOD team; they should not be inferred from names alone for the POC.

## 8. Source class, legal status, and references

`source_class` answers “where did this candidate value come from?”:

```text
legislation | administrative_guidance | official_statistics | national_team | other
```

`legal_status` answers “what is the lifecycle state of this legal measure?”:

```text
enacted_in_force | enacted_not_yet_in_force | bill_proposed | announced
```

`legal_status` may be `null` for official statistics or national-team values. `national_team` is a source class, not a legal lifecycle status.

For legislation, references attach to the proposal that they support, not to the parameter in general. A reference may include title, article, URL, legal-unit identifier, exact extract, RAG chunk id, and offsets.

## 9. Usage and file size

The received `usage` block is valuable context: it shows where a constant is defined and its 5,368 uses in the model. It should not be discarded.

For the POC there are two acceptable options:

1. keep `usage` in each full exchange record, matching `FR.enriched.json`; or
2. place the unchanged usage graph in a sidecar file or table and keep a `usage_ref` in the compact review record.

Option 2 reduces repeated data sent to the agent and UI. It is an optimization, not a change to the information supplied by the EUROMOD team.

## 10. Minimal POC storage

PostgreSQL remains the proposed canonical store; JSON remains the exchange format.

The minimum tables are:

- `parameters` - received information plus deterministic normalized fields;
- `model_values` - received model history and raw EUROMOD representations;
- `parameter_usage` - received usage graph, optionally stored separately;
- `proposals` - agent-generated candidate values and source metadata;
- `proposal_references` - evidence attached to proposals;
- `extraction_runs` - agent, model, prompt, confidence, and retrieval trace;
- `review_decisions` - append-only human decisions.

This is intentionally smaller than a general fiscal-parameter database.

This schema is implemented as the `params` schema of the shared legislation
database: [agentic-workflow/pipeline/db/params_schema.sql](../agentic-workflow/pipeline/db/params_schema.sql)
(`references` is a reserved SQL word, so that table is named
`proposal_references`). It is applied and populated with:

```bash
cd agentic-workflow/pipeline
uv run euromod-workflow init-param-db
uv run euromod-workflow ingest-params ../../extracted_parameters/enriched/FR.enriched.json
```

Each `extraction_runs` row additionally carries `phoenix_trace_id`, the
OpenTelemetry trace id of that run's root span. A reviewer can open the full
agent process (frame, retrieve, propose, critique, diff) in Arize Phoenix at
`http://localhost:6006/projects/<project-id>/traces/<phoenix_trace_id>`.
This is a soft link for process transparency: the durable evidence remains the
verbatim `supporting_extract` and chunk id on `proposal_references`. The
`params.proposal_review` view joins a proposal, its current model value, and
the trace id as the read surface for the validation UI.

## 11. Required fields and gates

### Required POC input

- received `information.model_target` and `information.country`;
- received `values[]` history;
- received raw model value and connector/model identifier;
- enough received metadata to display the parameter to a reviewer.

### Required agent proposal

- `proposal_id`;
- `proposed_value`, which may be `null` when the agent abstains;
- `source_class`;
- run id and confidence;
- legal dates only when supported by evidence.

### Required before acceptance

- `legal_status` for legislation;
- at least one citation and exact supporting extract for legislation;
- otherwise, an appropriate source reference or explicit national-team note.

`parameter_group`, structured units, offsets, and legal end dates are optional.

## 13. Validation exercise

Validate 5-10 records already present in `FR.enriched.json`:

- one plain statutory amount;
- one rate;
- one `"n/a"` value;
- one raw expression;
- the `$tin_upthres1` model/legal discrepancy;
- optionally, two members of a validated parameter group;
- one parameter routed to the national team.

