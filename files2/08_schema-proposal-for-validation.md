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

```json
{
  "parameter": {
    "country": "FR",
    "model_target": "euromod://FR/tin_fr/def_const/$tinrt_cdhr",
    "value_type": "scalar",
    "unit": "/1",
    "label": "Taux de la contribution différentielle sur les hauts revenus",
    "short_label": "Taux de la CDHR",
    "label_en": "Rate of the differential contribution on high incomes"
  },
  "values": [
    {
      "value": 0.20,
      "valid_from": "2025-01-01",
      "valid_to": null,
      "last_confirmed_valid_on": "2026-02-23",
      "legal_status": "enacted_in_force",
      "source_type": "legislation",
      "official_journal_date": "2025-02-15",
      "confidence": 0.95,
      "references": [
        {
          "title": "Loi de finances pour 2025, Article 10",
          "href": "https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000051168037"
        },
        {
          "title": "Code général des impôts, Article 224",
          "href": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051200465/2025-02-16",
          "supporting_extract": "Le montant résultant de l'application d'un taux de 20 %",
          "legal_unit_ref": "rag://FR/CGI/art224/v2025-02-16",
          "extract_offsets": [1042, 1096]
        }
      ],
      "lineage": {
        "proposed_by": "pipeline",
        "run_id": "2026-07-18T09:12Z#fr-042",
        "model": "…",
        "reviewed_by": null,
        "review_status": "pending"
      }
    }
  ]
}
```

What each block buys us:

- `model_target` — unambiguous write-back address in EUROMOD (system/policy/function/parameter). *Mandatory.*
- `values[]` — full history, one entry per effective date; `valid_to: null` = still in force. Point-in-time queries ("what was the rate on 2025-06-01?") are a filter, not an archaeology exercise. *Value + valid_from mandatory.*
- `supporting_extract` + `legal_unit_ref` — the exact sentence stating the value, linked to the chunk stored in our RAG. A reviewer verifies in seconds, and we can *automatically* check that the cited text really contains the value (our anti-hallucination KPI). *Required at acceptance for legislation-sourced values.*
- `legal_status` — the key extension beyond OpenFisca. OpenFisca stores only enacted law, which blocks work on next-year projections. Here a bill's parameter is a legitimate record with `legal_status: "bill_proposed"` — routed and displayed differently, never silently mixed with enacted values.
- `lineage` — filled automatically by the pipeline; no human ever types it. It's how we audit and evaluate the system (Activity 4).

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
| **Optional / auto-filled** | — | labels, `label_en`, `valid_to`, `official_journal_date`, signature date, `confidence`, notes, all of `lineage` (machine-filled) |

## 5. Storage: database canonical, JSON as the exchange format

We propose **PostgreSQL as the single source of truth**, in the same database as the RAG:

- Tables: `parameters`, `parameter_values`, `value_references`, `extraction_runs`, `review_decisions`.
- Why: the mandatory tier becomes real constraints (OpenFisca's flat files couldn't enforce anything); `legal_unit_ref` becomes a foreign key into the RAG's legal chunks (a citation can't point at nothing); temporal and cross-country queries are one `WHERE` clause; the review log lives next to the data it judges.
- The **JSON above is a generated view** — versioned JSON Schema (semver), round-trippable, and deliberately shaped like OpenFisca's YAML so it stays readable by economists. Pipeline and EUROMOD-side tooling consume/emit only this JSON; nothing outside the DB team touches SQL.

So "EUROMOD prefers JSON" and "the DB is better" are both satisfied: JSON is the *interface*, the database is the *truth*.

## 6. Decision points — what we need from you

1. **Addressing** (`model_target`): is `system/policy/function/parameter` sufficient and stable as a write-back address in EUROMOD? Edge cases (parameters shared across policies, spine reordering between system years)?
2. **Value types**: proposed set = `scalar | bracket_schedule | boolean | formula`. Enough for the pilot's parameter classes? How should we represent EUROMOD scale/band structures exactly?
3. **Mandatory tier**: do you confirm the minimal set in §4? Anything the *model* strictly needs that's missing (e.g., currency alongside unit)?
4. **Status enum**: are the six `legal_status` values right for how you work on projections and reforms? Should `national_team_estimate` be a status or only a `source_type`?
5. **Alignment with the Ireland JSON prototype** (Hannes): field-name mapping session — where do we diverge and why?
6. **One DB or two?** Parameters in the RAG's PostgreSQL (proposed) vs. a separate store. Any infra constraint against co-location? (Luis — does this fit the MCP integration you're exploring?)
7. **Uprating/indexation rules**: in scope as a `formula` value type in v1, or explicitly deferred?
8. **Who signs off** this schema, and does sign-off freeze v1.0?

## 7. What happens after validation

Schema v1.0 frozen → SQL DDL + JSON Schema committed to GitLab → agentic pipeline (Activity 3) and golden dataset (Activity 4) both expressed in this format → any later change goes through semver + decision log.
