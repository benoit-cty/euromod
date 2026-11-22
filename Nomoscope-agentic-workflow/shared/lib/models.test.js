import { test } from 'node:test';
import assert from 'node:assert/strict';
import { anyAlive, llmModels, pickModel } from './models.js';

const status = {
  workers: [{ alive: false }, { alive: true }],
  models: [
    { model: 'azure_openai/gpt-5.6-luna', kind: 'llm', is_default: true },
    { model: 'openrouter/minimax', kind: 'llm', is_default: false },
    { model: 'bge-m3', kind: 'embedding', is_default: true },
  ],
};

test('worker liveness is unknown until a status is in', () => {
  assert.equal(anyAlive(null), null);
  assert.equal(anyAlive(status), true);
  assert.equal(anyAlive({ workers: [{ alive: false }] }), false);
  assert.equal(anyAlive({}), false);
});

test('only language models are offered', () => {
  assert.deepEqual(
    llmModels(status).map((m) => m.model),
    ['azure_openai/gpt-5.6-luna', 'openrouter/minimax'],
  );
  assert.deepEqual(llmModels(null), []);
});

test('a picker keeps a listed model and replaces any other', () => {
  const models = llmModels(status);
  assert.equal(pickModel(models, 'openrouter/minimax'), 'openrouter/minimax');
  assert.equal(pickModel(models, 'gone/model'), 'azure_openai/gpt-5.6-luna');
  assert.equal(pickModel(models, ''), 'azure_openai/gpt-5.6-luna');
  assert.equal(pickModel([{ model: 'a', kind: 'llm' }], ''), 'a', 'no default published: the first');
  assert.equal(pickModel([], 'x'), '');
  // where '' means "the worker's default"
  assert.equal(pickModel(models, '', { allowDefault: true }), '');
  assert.equal(pickModel(models, 'gone/model', { allowDefault: true }), '');
  assert.equal(pickModel(models, 'openrouter/minimax', { allowDefault: true }), 'openrouter/minimax');
});
