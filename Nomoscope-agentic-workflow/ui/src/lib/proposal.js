// The review page's correction form for one proposal, and the gate on its
// Accept button. Pure functions: DetailPanel holds the form as state,
// ProposalEditor edits it, `npm test` checks the rules.

import { humanize } from '../../../shared/lib/labels.js';

const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;

/** An empty reference row. */
export function newReference() {
  return {
    title: '',
    href: '',
    jrc_database_id: '',
    source_trust_class: null,
    legal_unit_ref: '',
    supporting_extract: '',
    _extract_orig: '',
    extract_offsets: null,
    reviewer_note: '',
  };
}

/** The editable form of a proposed value envelope; null when nothing was proposed. */
export function buildForm(pv) {
  if (!pv) return null;
  const brackets = Array.isArray(pv.value);
  return {
    brackets,
    valueText: brackets ? JSON.stringify(pv.value, null, 2) : pv.value == null ? '' : String(pv.value),
    valid_from: pv.valid_from ?? '',
    valid_to: pv.valid_to ?? '',
    legal_status: pv.legal_status ?? '',
    source_type: pv.source_type ?? '',
    official_journal_date: pv.official_journal_date ?? '',
    references: (pv.references ?? []).map((r) => ({
      ...newReference(),
      title: r.title ?? '',
      href: r.href ?? '',
      jrc_database_id: r.jrc_database_id ?? '',
      // Read-only: the class of the instrument this citation came from
      // (ADR 0001). Carried through the form so a hand-edited reference does
      // not silently lose what the value rests on.
      source_trust_class: r.source_trust_class ?? null,
      legal_unit_ref: r.legal_unit_ref ?? '',
      supporting_extract: r.supporting_extract ?? '',
      // kept so an untouched extract keeps its verified offsets
      _extract_orig: r.supporting_extract ?? '',
      extract_offsets: r.extract_offsets ?? null,
      reviewer_note: r.reviewer_note ?? '',
    })),
  };
}

/**
 * Acceptance-gated tier (Param_Schema doc 08 §4): Accept enforces valid_from,
 * legal_status and at least one reference with a supporting extract — checked
 * against the *edited* form, so filling a gap in the form unblocks Accept. A
 * provisional proposal is never accepted: its act is likely missing.
 * Returns { ok, reason }.
 */
export function acceptGate(form, routing) {
  if (!form) return { ok: false, reason: 'there is no proposed value to accept' };
  if (routing === 'provisional') {
    return {
      ok: false,
      reason:
        "provisional: the evidence is likely the previous year's value — " +
        'ingest the missing finance act and re-run instead of accepting',
    };
  }
  if (!form.valid_from) return { ok: false, reason: 'the “valid from” date is missing' };
  // dates are hand-editable text, so they are checked before they can be saved
  for (const field of ['valid_from', 'valid_to', 'official_journal_date']) {
    const value = form[field];
    if (value && !ISO_DATE.test(value)) {
      return { ok: false, reason: `${humanize(field)} must be a date (YYYY-MM-DD)` };
    }
  }
  if (!form.legal_status) return { ok: false, reason: 'the legal status is missing' };
  const hasSource =
    form.source_type === 'national_team' || form.references.some((r) => r.supporting_extract.trim());
  if (!hasSource) return { ok: false, reason: 'no reference quotes the law' };
  return { ok: true, reason: '' };
}

/**
 * The value the form holds: bracket JSON parsed (throws when it is not JSON),
 * a scalar parsed when it is a JSON number/bool, formulas ($PSS * 4) and other
 * free text kept as strings, empty = null.
 */
export function parsedValue(form) {
  const text = form.valueText.trim();
  if (form.brackets) return JSON.parse(text);
  if (text === '') return null;
  try {
    const parsed = JSON.parse(text);
    return typeof parsed === 'object' ? text : parsed;
  } catch {
    return text;
  }
}

/** The non-value fields of an edited proposal, as `save_decision` takes them. */
export function editedFields(form, value) {
  return {
    // also carried here so an intentional null ("n/a" row) survives the wire,
    // where a null edited_value would read as "unchanged"
    value,
    valid_from: form.valid_from || null,
    valid_to: form.valid_to || null,
    legal_status: form.legal_status || null,
    source_type: form.source_type || null,
    official_journal_date: form.official_journal_date || null,
    references: form.references.map((r) => ({
      title: r.title || null,
      href: r.href || null,
      jrc_database_id: r.jrc_database_id || null,
      source_trust_class: r.source_trust_class || null,
      legal_unit_ref: r.legal_unit_ref || null,
      supporting_extract: r.supporting_extract || null,
      // a hand-edited extract no longer matches the verified offsets
      extract_offsets: r.supporting_extract === r._extract_orig ? r.extract_offsets : null,
      reviewer_note: r.reviewer_note || null,
    })),
  };
}
