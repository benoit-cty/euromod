import { test } from 'node:test';
import assert from 'node:assert/strict';
import { countryReadiness } from './readiness.js';

const row = { instruments: 10, chunks: 100, embedded_chunks: 100, text_versions: 10, en_versions: 3 };
const inputs = { parameters: { parameters: 500 }, country_report: { reports: 1 } };

test('a fully embedded country with parameters and a report is ready', () => {
  const r = countryReadiness(row, inputs);
  assert.equal(r.level, 'ready');
  assert.deepEqual(r.problems, []);
  assert.equal(r.englishPct, 30);
});

test('missing embeddings or report make it partial', () => {
  const r = countryReadiness({ ...row, embedded_chunks: 80 }, { ...inputs, country_report: null });
  assert.equal(r.level, 'partial');
  assert.equal(r.problems.length, 2);
});

test('no parameters or no legislation means not usable', () => {
  assert.equal(countryReadiness(row, { country_report: { reports: 1 } }).level, 'missing');
  // BE in the dev database: one instrument, nothing else
  assert.equal(countryReadiness({ ...row, instruments: 0 }, inputs).level, 'missing');
});
