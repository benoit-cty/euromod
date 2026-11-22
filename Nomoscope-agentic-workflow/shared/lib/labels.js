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
  provisional: {
    label: 'Needs newer law',
    hint: 'The evidence is probably last year’s value; this year’s act seems to be missing.',
  },
  national_team_source: {
    label: 'National team',
    hint: 'Supplied by the national team, not derived from legislation.',
  },
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

const AUTHENTICITY = {
  authentic: { label: 'Original', hint: 'The text as enacted, in its own language.' },
  official_translation: { label: 'Official translation', hint: 'A translation published by the authorities.' },
  machine_translation: {
    label: 'Machine translation',
    hint: 'Translated by a language model: never quoted as evidence.',
  },
};

const VERSION_STATUS = {
  in_force: { label: 'In force', hint: 'This version applies on the date searched.' },
  repealed: { label: 'Repealed', hint: 'No longer in force.' },
  not_yet_in_force: { label: 'Not yet in force', hint: 'Enacted, applies from a later date.' },
  suspended: { label: 'Suspended', hint: 'In force but suspended.' },
  unknown: { label: 'Status unknown', hint: 'The source does not say.' },
};

// How a passage reached the assistant (a review item's retrieval trace).
const RETRIEVAL_METHOD = {
  hybrid: { label: 'Search', hint: 'Found by the search over words and meaning.' },
  fts: { label: 'Word search', hint: 'Found by the full-text search.' },
  citation: { label: 'Cited', hint: 'Named by a citation the parameter carries.' },
  later_in_year: { label: 'Later this year', hint: 'A version entering into force after 1 July and by 31 December.' },
  located: { label: 'Looked up', hint: 'Fetched because the assistant named it as missing.' },
  sibling: { label: 'Same act', hint: 'Another article of an act already retrieved.' },
  country_report: { label: 'Country Report', hint: 'Background from the EUROMOD Country Report, never evidence.' },
  manual: { label: 'Added by hand', hint: 'Added by a person.' },
};

const JOB_TYPE = {
  workflow: { label: 'Parameter check', hint: 'The assistant checks parameters against the law.' },
  ingest: { label: 'Import', hint: 'A law or document fetched into the library.' },
  embed: { label: 'Make texts searchable', hint: 'Embeddings for texts that have none.' },
  translate: { label: 'Translation', hint: 'Machine translation of texts.' },
  'translate-params': { label: 'Parameter translation', hint: 'Machine translation of parameter texts.' },
  eval: { label: 'Evaluation', hint: 'A run over the golden set.' },
  encode: { label: 'Search', hint: 'A query encoded for the meaning search.' },
  impact: { label: 'Impact estimate', hint: 'Energy and carbon of the traced model calls.' },
  chat: { label: 'Chat question', hint: 'A question to the legislation chat.' },
  'draft-golden': { label: 'Golden-set draft', hint: 'Draft golden cases built for review.' },
};

const JOB_STATUS = {
  queued: { label: 'Waiting', hint: 'In the queue until a worker slot is free.' },
  running: { label: 'Running', hint: 'A worker is running it.' },
  waiting: { label: 'Waiting for the GPU', hint: 'Running, but another embeddings build holds the GPU.' },
  succeeded: { label: 'Done', hint: 'Finished successfully.' },
  failed: { label: 'Failed', hint: 'Stopped on an error.' },
  cancelled: { label: 'Cancelled', hint: 'Stopped on request.' },
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
export const authenticityLabel = (value) => lookup(AUTHENTICITY, value);
export const versionStatusLabel = (value) => lookup(VERSION_STATUS, value);
export const retrievalLabel = (value) => lookup(RETRIEVAL_METHOD, value);
export const jobTypeLabel = (value) => lookup(JOB_TYPE, value);
export const jobStatusLabel = (value) => lookup(JOB_STATUS, value);
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
