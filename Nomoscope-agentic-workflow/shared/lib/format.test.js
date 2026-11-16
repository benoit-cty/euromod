import { test } from 'node:test';
import assert from 'node:assert/strict';
import { formatDuration } from './format.js';

test('formatDuration: seconds, minutes, hours', () => {
  assert.equal(formatDuration(0), '0s');
  assert.equal(formatDuration(42_400), '42s');
  assert.equal(formatDuration(185_000), '3m 05s');
  assert.equal(formatDuration(7_620_000), '2h 07m');
  assert.equal(formatDuration(-5), '0s');
  assert.equal(formatDuration(NaN), '');
});
