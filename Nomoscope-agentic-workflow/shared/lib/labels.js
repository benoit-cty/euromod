// Plain-language wording for the pipeline's machine vocabulary.
//
// The database and the pipeline speak in enum values (`not_found`,
// `national_team_source`, `escalated`…). Reviewers should not have to learn
// them to use the UI: every badge goes through here, and the raw value stays
// in the badge's tooltip for whoever needs it. The CSS class keeps the raw
// value too, so colours do not depend on the wording.

const ROUTING = {
  changed: { label: 'Change proposed', hint: 'The law states a different value from the one EUROMOD holds.' },
  new: { label: 'New value', hint: 'EUROMOD holds no value for this year; the law states one.' },
  unchanged: { label: 'No change', hint: 'The law confirms the value EUROMOD already holds.' },
  derived: { label: 'Calculated', hint: 'The value is computed from figures quoted from the law.' },
  not_found: { label: 'Not found', hint: 'No text in the library states this value.' },
  provisional: { label: 'Needs newer law', hint: 'The evidence is probably last year’s value; this year’s act seems to be missing.' },
  national_team_source: { label: 'National team', hint: 'Supplied by the national team, not derived from legislation.' },
};

const STATUS = {
  pending: { label: 'To review', hint: 'Waiting for a decision.' },
  accepted: { label: 'Accepted', hint: 'Accepted as proposed.' },
  edited: { label: 'Accepted (edited)', hint: 'Accepted after the reviewer corrected it.' },
  rejected: { label: 'Rejected', hint: 'Rejected by the reviewer.' },
  escalated: { label: 'Sent to national team', hint: 'Escalated to the national team.' },
};

const VERDICT = {
  pass: { label: 'Checks passed', hint: 'The automatic checks found no problem.' },
  fail: { label: 'Checks failed', hint: 'The automatic checks found at least one problem.' },
};

const TRUST = {
  evidence: { label: 'Legislation', hint: 'A statute-level text.' },
  guidance: { label: 'Guidance', hint: 'A circular or doctrine: citable, but not legislation.' },
  context: { label: 'Background', hint: 'Context only, never cited as evidence.' },
};

const COUNTRIES = {
  BE: 'Belgium',
  ES: 'Spain',
  FR: 'France',
  IE: 'Ireland',
  LT: 'Lithuania',
  NL: 'Netherlands',
};

function humanize(value) {
  if (value == null || value === '') return '—';
  const text = String(value).replaceAll('_', ' ');
  return text.charAt(0).toUpperCase() + text.slice(1);
}

function lookup(table, value) {
  const entry = table[value];
  return entry ? { ...entry, raw: value } : { label: humanize(value), hint: '', raw: value };
}

export const routingLabel = (value) => lookup(ROUTING, value);
export const statusLabel = (value) => lookup(STATUS, value);
export const verdictLabel = (value) => lookup(VERDICT, value);
export const trustLabel = (value) => lookup(TRUST, value);
export const countryName = (code) => COUNTRIES[code] ?? code ?? '—';
export { humanize };

/** Postgres `timestamptz::text` ("2026-11-10 12:00:00.12+00") as epoch ms;
 *  WebKit's Date.parse refuses the space and the bare "+00" offset. */
export function parseTimestamp(text) {
  if (!text) return NaN;
  const iso = String(text)
    .trim()
    .replace(' ', 'T')
    .replace(/([+-]\d{2})$/, '$1:00');
  return Date.parse(iso);
}

/** "3 minutes ago", "yesterday", or a date: for timestamps a person reads. */
export function relativeTime(iso, now = Date.now()) {
  if (!iso) return '—';
  const then = parseTimestamp(iso);
  if (Number.isNaN(then)) return String(iso);
  const s = Math.round((now - then) / 1000);
  if (s < 45) return 'just now';
  const m = Math.round(s / 60);
  if (m < 60) return `${m} min ago`;
  const h = Math.round(m / 60);
  if (h < 24) return `${h} h ago`;
  const d = Math.round(h / 24);
  if (d === 1) return 'yesterday';
  if (d < 7) return `${d} days ago`;
  return new Date(then).toISOString().slice(0, 10);
}

/** 34903 -> "34 903": thin-space thousands, as the reviewers' legal texts write them. */
export function formatCount(n) {
  if (n == null) return '—';
  return Number(n).toLocaleString('en-US').replaceAll(',', ' ');
}
