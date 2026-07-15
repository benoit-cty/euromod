# Parameter Database Schema

This diagram documents the `params` schema created by
[`agentic-workflow/pipeline/db/params_schema.sql`](../agentic-workflow/pipeline/db/params_schema.sql).
It follows the four-stage ownership model: received EUROMOD data, deterministic
normalization, agent proposals, and append-only human review.

```mermaid
erDiagram
    PARAMETERS {
        bigint id PK
        text country
        text model_target UK
        text policy
        text function
        text name
        text spine_order
        text value_type
        text unit
        jsonb unit_structured
        jsonb label
        jsonb short_label
        jsonb description
        jsonb explanation
        jsonb classification
        jsonb coicop
        date last_confirmed_valid_on
        jsonb enrichment_lineage
        jsonb parameter_group
        text source_file
        timestamptz ingested_at
    }

    MODEL_VALUES {
        bigint id PK
        bigint parameter_id FK
        integer seq
        jsonb value_raw
        float8 value_numeric
        text value_kind
        text raw_euromod_value
        text model_release
        integer system_year
        date valid_from
        date valid_to
        text legal_status
        text source_type
        date official_journal_date
        jsonb received_references
        jsonb lineage
    }

    PARAMETER_USAGE {
        bigint id PK
        bigint parameter_id FK
        text relation
        text policy
        text function
        text function_comment
        text group_name
        text used_in_parameter
        text_array systems
        text source
    }

    EXTRACTION_RUNS {
        bigint id PK
        text run_id UK
        bigint parameter_id FK
        text country
        text model_target
        date as_of
        text model
        text critique_model
        text prompt_version
        text agent_version
        text phoenix_project
        text phoenix_trace_id
        text routing
        text critique_verdict
        text item_id
        jsonb retrieval_trace
        timestamptz started_at
        timestamptz finished_at
    }

    PROPOSALS {
        bigint id PK
        text proposal_id UK
        bigint run_pk FK
        bigint parameter_id FK
        text model_target
        jsonb proposed_value
        float8 proposed_value_numeric
        date effective_from
        date effective_to
        text legal_status
        text source_class
        date official_journal_date
        real confidence
        text reasoning
        timestamptz created_at
    }

    PROPOSAL_REFERENCES {
        bigint id PK
        bigint proposal_pk FK
        text title
        text href
        text legal_unit_ref
        uuid jrc_chunk_id
        text supporting_extract
        integer extract_start
        integer extract_end
        text reviewer_note
    }

    REVIEW_DECISIONS {
        bigint id PK
        bigint proposal_pk FK
        text item_id
        text action
        text reviewer
        text note
        timestamptz decided_at
        timestamptz logged_at
    }

    PUBLIC_CHUNKS {
        uuid id PK
    }

    PARAMETERS ||--o{ MODEL_VALUES : "has received history"
    PARAMETERS ||--o{ PARAMETER_USAGE : "has usage edges"
    PARAMETERS o|--o{ EXTRACTION_RUNS : "optionally targets"
    EXTRACTION_RUNS ||--o{ PROPOSALS : "produces"
    PARAMETERS o|--o{ PROPOSALS : "optionally identifies"
    PROPOSALS ||--o{ PROPOSAL_REFERENCES : "is supported by"
    PROPOSALS o|--o{ REVIEW_DECISIONS : "may receive"
    PUBLIC_CHUNKS o|--o{ PROPOSAL_REFERENCES : "soft reference only"
```

## Relationship Notes

- `parameters.model_target`, `extraction_runs.run_id`, and
  `proposals.proposal_id` are unique business identifiers.
- `model_values` is unique on `(parameter_id, seq)`; proposals never overwrite
  this received value history.
- `extraction_runs.parameter_id` and `proposals.parameter_id` are nullable so a
  run can represent a target that has not been ingested.
- `proposal_references.jrc_chunk_id` is deliberately not a foreign key. It is a
  soft reference to `public.chunks.id`; cited-chunk retention is enforced by
  `public.citation_registry`.
- `review_decisions` is append-only. A row must have either `proposal_pk` or
  `item_id`; `item_id` supports decisions on abstained or `not_found` queue
  items that have no proposal row.
- Phoenix trace IDs are also soft links because Phoenix data can be reset while
  proposal evidence remains durable.

## Review View

`params.proposal_review` is the validation UI read surface. It combines each
proposal with its run, parameter metadata, the model value applicable on the
run's `as_of` date, and a count of review decisions.

```mermaid
flowchart LR
    P[(parameters)] --> V{{proposal_review}}
    MV[(model_values)] -->|latest interval containing as_of| V
    ER[(extraction_runs)] --> V
    PR[(proposals)] --> V
    RD[(review_decisions)] -->|count by proposal| V
    V --> UI[Validation UI]
```

The view does not include `proposal_references`; evidence is loaded separately
from the proposal relationship when the reviewer opens citation details.