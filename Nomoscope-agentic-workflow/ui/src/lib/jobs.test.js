// Run with: npm test (node --test src/lib)
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { followJob, submitAndFollow, parseProgress, summarize } from './jobs.js';

// A fake worker: the job's event log grows between polls, its status flips
// after a number of polls. `after` seen by each events call is recorded so the
// cursor logic is observable.
function fakeTransport({ pages, statuses }) {
  const seenAfter = [];
  const submitted = [];
  let statusCalls = 0;
  let eventCalls = 0;
  return {
    seenAfter,
    submitted,
    submitJob: async (dbUrl, jobType, payload, priority) => {
      submitted.push({ dbUrl, jobType, payload, priority });
      return { id: 42 };
    },
    jobEvents: async (dbUrl, id, after) => {
      seenAfter.push(after);
      const page = pages[Math.min(eventCalls, pages.length - 1)];
      eventCalls += 1;
      return { events: page.filter((e) => e.id > after) };
    },
    jobStatus: async () => {
      const s = statuses[Math.min(statusCalls, statuses.length - 1)];
      statusCalls += 1;
      return s;
    },
    sleep: async () => {},
  };
}
const ev = (id, stream, line, data) => ({ id, at: 't', stream, line, data: data ?? null });

test('events are delivered once, in order, and the cursor advances past the last id', async () => {
  const log = [ev(1, 'system', 'started'), ev(2, 'stdout', 'one')];
  const later = [...log, ev(3, 'stderr', 'warn'), ev(4, 'progress', '@progress {"done":1,"total":2}', { done: 1, total: 2 })];
  const final = [...later, ev(5, 'stdout', 'bye')];
  const fake = fakeTransport({
    pages: [log, later, final, final],
    statuses: [{ id: 42, status: 'running' }, { id: 42, status: 'succeeded', result: { ok: true } }],
  });
  const lines = [];
  const progress = [];
  const statuses = [];
  const result = await followJob('db', 42, {
    onLine: (e) => lines.push(`${e.stream}:${e.line}`),
    onProgress: (d) => progress.push(d),
    onStatus: (s) => statuses.push(s.status),
  }, 0, fake);

  assert.equal(result.status, 'succeeded');
  assert.deepEqual(result.result, { ok: true });
  assert.deepEqual(lines, ['system:started', 'stdout:one', 'stderr:warn', 'stdout:bye'], 'trailing event drained after the terminal status');
  assert.deepEqual(progress, [{ done: 1, total: 2 }]);
  assert.deepEqual(statuses, ['running', 'succeeded']);
  // poll 1 from 0, poll 2 after id 2, final drain after id 4
  assert.deepEqual(fake.seenAfter, [0, 2, 4]);
});

test('a progress event without parsed data falls back to the raw line', async () => {
  const fake = fakeTransport({
    pages: [[ev(1, 'progress', '@progress {"done":3,"total":3}')], [ev(1, 'progress', '@progress {"done":3,"total":3}')]],
    statuses: [{ id: 7, status: 'succeeded' }],
  });
  const progress = [];
  await followJob('db', 7, { onProgress: (d) => progress.push(d) }, 0, fake);
  assert.deepEqual(progress, [{ done: 3, total: 3 }]);
  assert.equal(parseProgress('not json'), null);
});

test('submitAndFollow submits with the priority and reports the id before following', async () => {
  const fake = fakeTransport({ pages: [[]], statuses: [{ id: 42, status: 'failed', error: 'a\nb\nlast line' }] });
  let seenId = null;
  const result = await submitAndFollow('db', 'impact', { zone: 'EEE' }, { onSubmit: (id) => (seenId = id) }, 0, fake);
  assert.equal(seenId, 42);
  assert.deepEqual(fake.submitted, [{ dbUrl: 'db', jobType: 'impact', payload: { zone: 'EEE' }, priority: 0 }]);
  assert.equal(result.status, 'failed');
  assert.equal(summarize(result, '3s'), 'Failed after 3s: last line');
  assert.equal(summarize({ status: 'cancelled' }), 'Cancelled.');
});
