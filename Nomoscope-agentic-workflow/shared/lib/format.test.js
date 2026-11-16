import { test } from 'node:test';
import assert from 'node:assert/strict';
import { formatCount, formatDuration, formatFixed, formatNumber, formatPercent } from './format.js';

test('formatCount groups thousands with a space', () => {
  assert.equal(formatCount(34903), '34 903');
  assert.equal(formatCount(1234567), '1 234 567');
  assert.equal(formatCount(0), '0');
  assert.equal(formatCount(null), '—');
});

test('formatNumber caps decimals, formatFixed pads them', () => {
  assert.equal(formatNumber(1234.5678), '1,234.57');
  assert.equal(formatNumber(1234.5678, 0), '1,235');
  assert.equal(formatNumber(undefined), '—');
  assert.equal(formatFixed(0.1234, 5), '0.12340');
  assert.equal(formatFixed(null, 3), '—');
});

test('formatPercent reads a 0–100 value', () => {
  assert.equal(formatPercent(87.25), '87.3%');
  assert.equal(formatPercent(100), '100.0%');
  assert.equal(formatPercent(null), '—');
});

test('formatDuration: seconds, minutes, hours', () => {
  assert.equal(formatDuration(0), '0s');
  assert.equal(formatDuration(42_400), '42s');
  assert.equal(formatDuration(185_000), '3m 05s');
  assert.equal(formatDuration(7_620_000), '2h 07m');
  assert.equal(formatDuration(-5), '0s');
  assert.equal(formatDuration(NaN), '');
});
