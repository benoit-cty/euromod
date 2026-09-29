---
status: accepted
date: 2026-09-29
---

# Analysts edit parameter metadata in the UI, and the EUROMOD export is a change set

A parameter's metadata can be wrong in the EUROMOD export. The FR export, for example, labels 146 rates `currency`. Until now the only fix was a line in the curation YAML, which a developer writes and re-applies with `curate-params`. The analyst who spots the error in the validation UI could not correct it there. The export back to EUROMOD also held the full Activity 1 record of every accepted item, history included, so EUROMOD had to diff it against what it already holds to find what had changed.

We decided that **an analyst can edit a parameter's metadata in the UI**: its `unit`, its `source_type`, and the language-keyed texts (`label`, `short_label`, `description`, `explanation`).

- **Identity is never editable, and neither are values.** Identity means `model_target` and `parameter_key`. A value changes only through a review decision.
- **One function makes every edit.** Each edit is one call to `params.edit_parameter()`. The function is `SECURITY DEFINER`, and `nomos_reviewer` holds EXECUTE on it but no UPDATE on `params.parameters`. It validates the unit and source-type vocabulary, applies the edit, and appends a row to `params.parameter_edits` that records `from`, `to`, the reviewer (the analyst's login, `session_user`) and a note.
- **Edits survive re-ingest.** The table has no foreign key, and `reapply_parameter_edits()` runs last in both `ingest-params` and `curate-params`. So a human edit wins over the export and over the YAML overlay.

**The export is a change set.** `params.euromod_change_set` has one entry per changed parameter, holding:

- `parameter_key` and `model_target`;
- `metadata`, as `{field: {from, to, reviewer, edited_at, note}}` — the net effect of the edits, so an edit that was reverted drops out;
- `values`: only the rows a human accepted as a change (routing `changed` / `new`) or edited, each with its system year and its decision.

Unchanged fields, the value history and accepted `unchanged` confirmations are left out. The UI export (`<CC>_changes_<date>.json`) and the CLI export (`<CC>_changes.json`) both read this one view, so they cannot drift apart.

## Considered options

- **Edit the columns in place, with a column grant to the reviewer.** Rejected: the next `ingest-params` would silently undo the edit, and there would be no audit trail.
- **Write the edits into the curation YAML.** Rejected: the workstation writes no file other than the export (ADR 0004), and the YAML is developer-owned and versioned in git.
- **Keep the full-record export and add a diff alongside it.** Rejected: EUROMOD asked for only the changes, and two formats for one handover invite confusion.

## Consequences

- The UI now writes four things: a decision, a metadata edit, a job and a golden verdict (`Nomergon-worker/db/roles.sql`).
- **`from` is the parameter store's value before the first edit**, which is not necessarily what EUROMOD holds. A field that the curation YAML already corrected reports the curated value as `from`. The YAML corrections themselves are not part of the change set.
- A UI edit outranks the YAML even when the YAML is changed afterwards. To hand a field back to the YAML, edit it to the YAML's value. The edit stays in force, but its net change then drops out of the change set.
- A `unit` or `source_type` edit changes pipeline behaviour on the next run. `unit` drives the proposer's percent normalisation and the critique's range check, and `national_team` routes the parameter around the pipeline. Queue items already produced are not re-run.
- While writing this, we found that `decide_review_item` stamped `current_user`. Inside a `SECURITY DEFINER` function that is the function's owner, so on a shared deployment every decision would have been attributed to the schema owner. Both functions now use `session_user`.
