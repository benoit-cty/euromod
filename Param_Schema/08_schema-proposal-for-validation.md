# Policy Parameter Format — Schema Proposal for Validation

*Draft for review by JRC.B.2 (Hannes, Luis, Kosta, Hugo) before any implementation. Please read §2 (the example) and §6 (decision points) even if you skip the rest.*

---

## 1. What problem this format solves

Our fiscal models (EUROMOD first) contain thousands of policy parameters — tax rates, thresholds, benefit amounts. Today, updating them means a person reads the law and edits the model. The AI pipeline we're building must **propose** such updates, and a human must be able to **verify** each proposal quickly. That requires every parameter value to carry, in one structured record:

1. **What** the value is, and **where in the model** it goes *(needed by the model)*
2. **Since when** it applies, and until when *(needed by the model)*
3. **Where it comes from** — the legal text, down to the exact sentence *(needed by the reviewer)*
4. **How solid it is** — enacted law, or a bill still in parliament? extracted by an LLM, or confirmed by the national team? *(needed by the reviewer and for projections)*

Design principle, learned the hard way in OpenFisca-France (issue #1672, where optional metadata ended up filled 19–60% of the time): **only fields in group 1–2 are mandatory.** Groups 3–4 are enforced when a human *accepts* a proposal into the model — not when data enters the database. A parameter without a legal reference is valid data: it tells us it's national-team-sourced or not yet traced.

## 2. A real example, end to end

France's *Contribution différentielle sur les hauts revenus* (CDHR), rate 20%, created by the 2025 budget law. As one record (JSON view):

See [parameter_sample](Param_Schema\parameter_sample.jsonc)

What each block buys us:

- `model_target` — unambiguous write-back address in EUROMOD (system/policy/function/parameter). *Mandatory.*
- `values[]` — full history, one entry per effective date; `valid_to: null` = still in force. Point-in-time queries ("what was the rate on 2025-06-01?") are a filter, not an archaeology exercise. *Value + valid_from mandatory.*
- `supporting_extract` + `legal_unit_ref` — the exact sentence stating the value, linked to the chunk stored in our RAG. A reviewer verifies in seconds, and we can *automatically* check that the cited text really contains the value (our anti-hallucination KPI). *Required at acceptance for legislation-sourced values.*
- `legal_status` — the key extension beyond OpenFisca. OpenFisca stores only enacted law, which blocks work on next-year projections. Here a bill's parameter is a legitimate record with `legal_status: "bill_proposed"` — routed and displayed differently, never silently mixed with enacted values.
- `label`, `short_label`, `description` — language-keyed dictionaries, not separate one-off translation fields. This keeps the EU-facing interface ready for original-language review and multilingual display without changing the schema each time we add a language.
- `lineage` — filled automatically by the pipeline; no human ever types it. It's how we audit and evaluate the system (Activity 4).

### 2.1 A bracketed value (progressive schedule)

Most fiscal parameters aren't scalars — they're **scales**: income-tax bands, contribution ceilings, tapered benefits. These use `value_type: "bracket_schedule"`, and the only thing that changes is the shape of `value` (an ordered array of bands instead of a number). The whole envelope — `references`, `legal_status`, `confidence`, `lineage` — is identical to §2, so we show just the `parameter` header and one `values[]` entry:

```json
{
  "information": {
    "country": "FR",
    "model_target": "euromod://FR/tin_fr/def_const/$tinsc_bareme",
    "value_type": "bracket_schedule",
    "unit": "/1",
    "threshold_unit": "EUR",
    "label": {
      "fr": "Barème de l'impôt sur le revenu (par part de quotient familial)",
      "en": "Income tax rate schedule (per family-quotient share)"
    },
    "short_label": {
      "fr": "Barème IR",
      "en": "Income tax schedule"
    },
    "description": {
      "fr": "Barème progressif de l'impôt sur le revenu, avec un seuil inférieur et un taux pour chaque tranche.",
      "en": "Progressive income-tax schedule, with a lower threshold and rate for each band."
    },
    "explanation" : {
      "en": "Enforced by President following a strike."
    },
    "last_confirmed_valid_on": "2026-02-23",
  },
  "values": [
    {
      "value": [
        { "threshold": 0,      "rate": 0.00 },
        { "threshold": 11294,  "rate": 0.11 },
        { "threshold": 28797,  "rate": 0.30 },
        { "threshold": 82341,  "rate": 0.41 },
        { "threshold": 177106, "rate": 0.45 }
      ],
      "valid_from": "2024-01-01",
      "valid_to": "2024-12-31",
      "legal_status": "enacted_in_force",
      "source_type": "legislation",
      "official_journal_date": "2025-02-15",
      "confidence": 0.93,
      "references": [
        {
          "title": "Code général des impôts, Article 197",
          "href": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047850595",
          "jrc_database_id": "cb64e73f-a350-47b5-803c-7e37584c5e49",
          "supporting_extract": "… le taux de : … 11 % pour la fraction supérieure à 11 294 € …",
          "reviewer_note": "Refer to another document on specific notes."
        }
      ],
      "lineage": {
        "proposed_by": "pipeline",
        "review_status": "accepted"
      }
    },
    {
      "value": [
        { "threshold": 0,      "rate": 0.00 },
        { "threshold": 11497,  "rate": 0.11 },
        { "threshold": 29315,  "rate": 0.30 },
        { "threshold": 83823,  "rate": 0.41 },
        { "threshold": 180294, "rate": 0.45 }
      ],
      "valid_from": "2025-01-01",
      "valid_to": null,
      "legal_status": "enacted_in_force",
      "source_type": "legislation",
      "confidence": 0.93,
      "references": [
        {
          "title": "Code général des impôts, Article 197",
          "href": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051200000",
          "jrc_database_id": "cb64e73f-a350-47b5-803c-7e37584c5e49",
          "supporting_extract": "… le taux de : … 11 % pour la fraction supérieure à 11 497 € …"
        }
      ],
      "lineage": {
        "proposed_by": "pipeline",
        "review_status": "pending"
      }
    }
  ]
}
```

Notes on the bracket shape:

- Each band carries only its **lower** `threshold` and its `rate`; the upper edge is implicitly the next band's threshold, and the last band runs to infinity. This matches EUROMOD's band tables and OpenFisca's `brackets`/`rates` pairs, so round-tripping stays lossless.
- Thresholds and rates have **different units** — thresholds are amounts (`threshold_unit: "EUR"`), rates are dimensionless (`unit: "/1"`). This is exactly why decision point 2 (scale representation) and 3 (currency alongside unit) need your confirmation.
- Amount-only scales (e.g. flat band ceilings with no rate) or amount-per-band scales would use the same array with an `amount` key instead of `rate`. We'd like JRC.B.2 to tell us which band variants EUROMOD actually needs so we don't over- or under-model this.

## 3. The lifecycle statuses

| `legal_status` | Meaning | Typical use |
|---|---|---|
| `enacted_in_force` | Published, effective | Normal updates |
| `enacted_not_yet_in_force` | Published, future effective date | Next-year systems |
| `adopted_pending_publication` | Voted, not yet in the official journal | Fast-track updates |
| `bill_proposed` | In parliamentary procedure | Reform simulations |
| `announced` | Government announcement only | Early scenario work |
| `national_team_estimate` | No legal source; national team is the authority | Non-codified parameters |

`legal_status` (where the *law* is in its life) is deliberately separate from `confidence` (how sure we are the *extraction* is right). An enacted law badly read by the LLM is high status / low confidence; a precise reading of a bill is low status / high confidence.

## 4. Mandatory vs. optional — the complete picture

| Requirement level | Enforced by | Fields |
|---|---|---|
| **Mandatory** | database (`NOT NULL`) | `country`, `model_target`, `value_type`, `unit`, `value`, `valid_from` |
| **Acceptance-gated** | validation UI (can't click *Accept* without it) | `legal_status`; at least one `reference` **or** `source_type: national_team`; `supporting_extract` if legislation-sourced |
| **Optional / auto-filled** | — | `label`, `short_label`, and `description` as language-keyed dictionaries, `valid_to`, `official_journal_date`, signature date, `confidence`, notes, all of `lineage` (machine-filled), `metadata` (free-form, see §5.1) |

## 5. Storage: database canonical, JSON as the exchange format

We propose **PostgreSQL as the single source of truth**, in the same database as the RAG:

- Tables: `parameters`, `parameter_values`, `value_references`, `extraction_runs`, `review_decisions`.
- Why: the mandatory tier becomes real constraints (OpenFisca's flat files couldn't enforce anything); `legal_unit_ref` becomes a foreign key into the RAG's legal chunks (a citation can't point at nothing); temporal and cross-country queries are one `WHERE` clause; the review log lives next to the data it judges.
- The **JSON above is a generated view** — versioned JSON Schema (semver), round-trippable, and deliberately shaped like OpenFisca's YAML so it stays readable by economists. Pipeline and EUROMOD-side tooling consume/emit only this JSON; nothing outside the DB team touches SQL.

So "EUROMOD prefers JSON" and "the DB is better" are both satisfied: JSON is the *interface*, the database is the *truth*.

### 5.1 Keeping the schema open — a `metadata` escape hatch

A hard constraint has a cost: the first time reality doesn't fit, you need a migration, a schema-version bump, and coordination with everyone who consumes the JSON. To avoid freezing v1.0 into a corner, we propose that **both the `parameters` and `parameter_values` tables carry a `metadata JSONB` column** (defaulting to `{}`), surfaced in the JSON view as an optional `metadata` object.

The rule of thumb:

- Anything the **model needs** or the **reviewer gates on** is a *first-class, typed column* — never buried in `metadata`. The mandatory and acceptance-gated tiers (§4) stay strict.
- Anything **experimental, country-specific, or not-yet-standardised** goes in `metadata` first. Examples we already anticipate: a national team's internal parameter id, EUROMOD spine-ordering hints, indexation notes before uprating is formalised (decision point 7), or a flag for a value type we haven't blessed yet.
- When a `metadata` key proves it's used widely and reliably (the opposite of OpenFisca-France #1672), we **promote it to a real column** with a constraint, in a normal semver minor release. So `metadata` is a *staging area*, not a dumping ground — it lets us learn what's genuinely needed before committing the schema to it.

This gives us forward-compatibility without weakening the constraints that matter: `NOT NULL` still guards the model's inputs, foreign keys still guard citations, and the JSON Schema can still validate the typed fields strictly while allowing `metadata` to be any object.

## 6. Decision points — what we need from you

1. **Addressing** (`model_target`): is `system/policy/function/parameter` sufficient and stable as a write-back address in EUROMOD? Edge cases (parameters shared across policies, spine reordering between system years)?
2. **Value types**: proposed set = `scalar | bracket_schedule | boolean | formula`. Enough for the pilot's parameter classes? How should we represent EUROMOD scale/band structures exactly?
3. **Mandatory tier**: do you confirm the minimal set in §4? Anything the *model* strictly needs that's missing (e.g., currency alongside unit)?
4. **Status enum**: are the six `legal_status` values right for how you work on projections and reforms? Should `national_team_estimate` be a status or only a `source_type`?
5. **Alignment with the Ireland JSON prototype** (Hannes): field-name mapping session — where do we diverge and why?
6. **One DB or two?** Parameters in the RAG's PostgreSQL (proposed) vs. a separate store. Any infra constraint against co-location? (Luis — does this fit the MCP integration you're exploring?)
7. **Uprating/indexation rules**: in scope as a `formula` value type in v1, or explicitly deferred?
8. **Language fields**: should `label`, `short_label`, and `description` be language-keyed dictionaries using ISO/BCP 47 language codes (`fr`, `en`, `ga`, `de-AT`, ...)? Which languages are required at acceptance: original legal language only, English, or both?
9. **Forward-compatibility** (`metadata`, §5.1): do you agree with a free-form `metadata JSONB` escape hatch on both tables, with the discipline that model-critical / review-gated fields are never allowed to live there? Any field you'd want promoted to a real column from day one rather than staged in `metadata`?
10. **Who signs off** this schema, and does sign-off freeze v1.0?

## 7. What happens after validation

Schema v1.0 frozen → SQL DDL + JSON Schema committed to GitLab → agentic pipeline (Activity 3) and golden dataset (Activity 4) both expressed in this format → any later change goes through semver + decision log.
