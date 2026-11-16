import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fromProgressEvent, fromWorkflowLine, percentDone } from './progress.js';

test('structured events with a total drive the bar', () => {
  let p = fromProgressEvent(null, { task: 'embed', done: 3, total: 12, detail: 'batch 1' });
  assert.deepEqual(p, { task: 'embed', done: 3, total: 12, detail: 'batch 1' });
  assert.equal(percentDone(p), 25);
  // a phase without a total keeps the counts and updates the detail only
  p = fromProgressEvent(p, { phase: 'waiting', detail: 'waiting for the GPU' });
  assert.equal(p.done, 3);
  assert.equal(p.detail, 'waiting for the GPU');
  // before any count, a total-less event does not invent one
  assert.equal(fromProgressEvent(null, { phase: 'starting' }), null);
  assert.equal(fromProgressEvent(p, null), p);
});

test('the workflow console is read parameter by parameter', () => {
  let p = fromWorkflowLine(null, 'readiness: FR ok');
  assert.equal(p, null, 'nothing before the first parameter');
  p = fromWorkflowLine(p, '[1/3] euromod://FR/x');
  assert.deepEqual(p, { done: 0, total: 3, current: 'euromod://FR/x', detail: '' });
  p = fromWorkflowLine(p, '  › retrieve');
  assert.equal(p.detail, 'retrieve');
  p = fromWorkflowLine(p, 'euromod://FR/x: routing=changed');
  assert.equal(p.done, 1);
  assert.equal(p.detail, 'changed');
  p = fromWorkflowLine(p, 'some other line');
  assert.equal(p.done, 1);
  assert.equal(percentDone(p), 33);
});

test('percentDone is null without a total and capped at 100', () => {
  assert.equal(percentDone(null), null);
  assert.equal(percentDone({ done: 1, total: 0 }), null);
  assert.equal(percentDone({ done: 7, total: 5 }), 100);
});
