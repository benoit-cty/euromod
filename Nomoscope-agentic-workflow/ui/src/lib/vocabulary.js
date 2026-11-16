// The parameter vocabularies the review UI offers in its editors. They mirror
// the pipeline's (Param_Schema doc 01, schema.py LegalStatus / SourceType,
// paramdb.KNOWN_UNITS); the database refuses anything else in a metadata edit
// (params.edit_parameter — a pytest keeps the SQL lists in step with Python).

export const LEGAL_STATUSES = [
  'enacted_in_force',
  'enacted_not_yet_in_force',
  'adopted_pending_publication',
  'bill_proposed',
  'announced',
  'national_team_estimate',
];

export const SOURCE_TYPES = [
  'legislation',
  'national_team',
  'administrative_guidance',
  'official_statistics',
  'parliamentary_bill',
  'government_announcement',
  'other',
];

export const UNITS = [
  '/1',
  '/100',
  'ratio',
  'currency',
  'currency/hour',
  'currency/day',
  'currency/week',
  'currency/month',
  'currency/year',
];
