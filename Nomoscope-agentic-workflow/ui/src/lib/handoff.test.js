// Run with: node --test src/lib
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildHandoffPrompt } from './handoff.js';

const notFound = {
  country: 'ES',
  model_target: 'euromod://ES/ConstDef_es/def_const/$UB_QperMin',
  label: '$UB_QperMin',
  system_year: 2025,
  as_of: '2025-07-01',
  value_type: 'scalar',
  unit: 'months',
  routing: 'not_found',
  current_value: { value: 12, valid_from: '2005-01-01', references: [] },
  proposed_value: null,
  critique: {
    issues: ['no value proposed', 'model: Article 269.1 states the scale in days and begins at 360 contribution days.'],
  },
  scout: {
    needs: ['artículo 266 del texto refundido de la Ley General de la Seguridad Social'],
    reasoning: 'The threshold is 360 days.',
  },
  retrieval_trace: [
    { citation: 'LGSS Artículo 266', validity: '[2016-01-02,)' },
    { citation: 'LGSS Artículo 266', validity: '[2016-01-02,)' },
    { citation: 'LGSS Artículo 269' },
  ],
};

const context = {
  parameters: [
    {
      model_target: notFound.model_target,
      name: '$UB_QperMin',
      unit: 'months',
      temporal_basis: 'in_force',
      texts: {
        label: { en: 'Qualifying period: min no of months in work' },
        description: { en: 'Minimum qualifying period (currently 12 months).' },
      },
      law_texts: [
        { lang: 'es', field: 'label', origin: 'machine_translation', content: 'Período de carencia' },
        { lang: 'fr', field: 'label', origin: 'machine_translation', content: 'Période d’affiliation' },
      ],
      history: [{ system_year: 2005, valid_from: '2005-01-01', value: 12, raw: '12' }],
    },
  ],
};

test('a not_found item carries the parameter, what was tried and the answer format', () => {
  const text = buildHandoffPrompt(notFound, context);
  assert.match(text, /Spain \(ES\), system year 2025/);
  assert.match(text, /Qualifying period: min no of months in work/);
  assert.match(text, /Período de carencia/);
  assert.doesNotMatch(text, /Période d’affiliation/); // not the law's language
  assert.match(text, /Values EUROMOD has held: 2005: 12/);
  assert.match(text, /in force during 2025/);
  assert.match(text, /Its reasoning: Article 269\.1/);
  assert.doesNotMatch(text, /no value proposed/);
  assert.match(text, /artículo 266/);
  assert.match(text, /Texts it read \(our corpus, 2\)/);
  assert.match(text, /boe\.es/);
  assert.match(text, /QUOTE: «/);
  assert.match(text, /SAME AS EUROMOD \(12\)/);
});

test('without context the prompt still stands on the queue item', () => {
  const text = buildHandoffPrompt(notFound);
  assert.match(text, /Value EUROMOD holds now: 12/);
  assert.match(text, /\$UB_QperMin/);
});

test('an income-year parameter is pointed at the previous income year', () => {
  const ctx = { parameters: [{ ...context.parameters[0], temporal_basis: 'income_year' }] };
  const text = buildHandoffPrompt({ ...notFound, country: 'FR' }, ctx);
  assert.match(text, /«income 2024»/);
  assert.match(text, /legifrance/);
});

test('a proposal is shown as something to check, with its quote', () => {
  const item = {
    ...notFound,
    routing: 'changed',
    proposed_value: {
      value: 360,
      valid_from: '2025-01-01',
      references: [{ title: 'LGSS art. 269', supporting_extract: '360 días' }],
    },
  };
  const text = buildHandoffPrompt(item, context);
  assert.match(text, /It proposed 360 from 2025-01-01, citing LGSS art\. 269/);
  assert.match(text, /Its quote: «360 días»/);
});

test('a schedule lists its members', () => {
  const member = (name, role) => ({ ...context.parameters[0], name, group_role: role });
  const text = buildHandoffPrompt(
    { ...notFound, model_target: 'group:FR:tinkt_fr:tin_schedule', country: 'FR' },
    { parameters: [member('$tin_rate1', 'rate 1'), member('$tin_upthres1', 'upper_threshold 1')] },
  );
  assert.match(text, /tax\/benefit schedule/);
  assert.match(text, /- \$tin_rate1 \(rate 1\)/);
  assert.match(text, /- \$tin_upthres1 \(upper_threshold 1\)/);
});
