import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createApi } from './api.js';

test('commands go out as Tauri invokes, with a payload only where they take one', async () => {
  const calls = [];
  const opened = [];
  const api = createApi(
    async (command, args) => {
      calls.push([command, args]);
      return { ok: true };
    },
    (url) => opened.push(url),
  );

  await api.getEnvConfig();
  await api.workerStatus();
  await api.submitJob('embed', { limit: 5 });
  await api.jobEvents(7);
  await api.cancelJob(7);
  await api.chunkRenderings('abc');
  await api.call('load_decisions', { limit: 3 });
  api.openExternal('https://example.org');

  assert.deepEqual(calls, [
    ['get_env_config', undefined],
    ['worker_status', undefined],
    ['submit_job', { payload: { job_type: 'embed', payload: { limit: 5 }, priority: 0 } }],
    ['job_events', { payload: { id: 7, after: 0 } }],
    ['cancel_job', { payload: { id: 7 } }],
    ['chunk_renderings', { payload: { chunk_id: 'abc' } }],
    ['load_decisions', { payload: { limit: 3 } }],
  ]);
  assert.deepEqual(opened, ['https://example.org']);
  // the database URL stays in Rust: no call carries one
  assert.ok(calls.every(([, args]) => !JSON.stringify(args ?? {}).includes('db_url')));
});
