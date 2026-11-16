import { test } from 'node:test';
import assert from 'node:assert/strict';
import { navDelta, plainKey, stepIndex } from './keynav.js';

test('navigation keys move by one, by ten, or to an end', () => {
  assert.equal(navDelta('ArrowDown', 40), 1);
  assert.equal(navDelta('ArrowUp', 40), -1);
  assert.equal(navDelta('PageDown', 40), 10);
  assert.equal(navDelta('PageUp', 40), -10);
  assert.equal(navDelta('Home', 40), -40);
  assert.equal(navDelta('End', 40), 40);
  assert.equal(navDelta('Enter', 40), null);
});

test('stepping clamps, and enters an unselected list from the end arrowed towards', () => {
  assert.equal(stepIndex(3, 1, 10), 4);
  assert.equal(stepIndex(9, 10, 10), 9);
  assert.equal(stepIndex(2, -10, 10), 0);
  assert.equal(stepIndex(-1, 1, 10), 0);
  assert.equal(stepIndex(-1, -1, 10), 9);
  assert.equal(stepIndex(-1, 1, 0), -1);
});

test('a key with a modifier is not navigation', () => {
  assert.equal(plainKey({ key: 'ArrowDown' }), true);
  assert.equal(plainKey({ key: 'ArrowDown', ctrlKey: true }), false);
  assert.equal(plainKey({ key: 'ArrowDown', shiftKey: true }), false);
});
