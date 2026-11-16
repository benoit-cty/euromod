import { test } from 'node:test';
import assert from 'node:assert/strict';
import { routingLabel, statusLabel, countryName, relativeTime, formatCount, humanize } from './labels.js';

test('known enum values get plain wording and keep the raw value', () => {
  assert.equal(routingLabel('not_found').label, 'Not found');
  assert.equal(routingLabel('not_found').raw, 'not_found');
  assert.equal(statusLabel('escalated').label, 'Sent to national team');
});

test('unknown enum values are humanized, never dropped', () => {
  const l = routingLabel('some_new_routing');
  assert.equal(l.label, 'Some new routing');
  assert.equal(l.raw, 'some_new_routing');
  assert.equal(humanize(null), '—');
});

test('country names fall back to the code', () => {
  assert.equal(countryName('FR'), 'France');
  assert.equal(countryName('XX'), 'XX');
});

test('relative time', () => {
  const now = Date.parse('2026-11-10T12:00:00Z');
  assert.equal(relativeTime('2026-11-10T11:59:50Z', now), 'just now');
  assert.equal(relativeTime('2026-11-10T11:30:00Z', now), '30 min ago');
  assert.equal(relativeTime('2026-11-09T11:00:00Z', now), 'yesterday');
  assert.equal(relativeTime('2026-10-01T00:00:00Z', now), '2026-10-01');
  assert.equal(relativeTime(null, now), '—');
  // Postgres timestamptz::text
  assert.equal(relativeTime('2026-11-10 11:30:00.123+00', now), '30 min ago');
});

test('counts use thin-space thousands', () => {
  assert.equal(formatCount(34903), '34 903');
  assert.equal(formatCount(null), '—');
});
