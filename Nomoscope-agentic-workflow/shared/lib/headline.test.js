import { test } from 'node:test';
import assert from 'node:assert/strict';
import { headlineRuns, lexicalSpans, parseHeadline } from './headline.js';

test('a headline parses into its plain text and the marked spans', () => {
  assert.deepEqual(parseHeadline('le <<HL>>taux<</HL>> du <<HL>>barème<</HL>>'), {
    plain: 'le taux du barème',
    spans: [
      [3, 7],
      [11, 17],
    ],
  });
  // an unclosed or empty mark is not a span
  assert.deepEqual(parseHeadline('a <<HL>>b').spans, []);
  assert.deepEqual(parseHeadline('a <<HL>><</HL>>b').spans, []);
  assert.deepEqual(parseHeadline(null), { plain: '', spans: [] });
});

test('headlineRuns splits ts_headline markers into runs', () => {
  assert.deepEqual(headlineRuns('a <<HL>>b<</HL>> c'), [
    { text: 'a ', hit: false },
    { text: 'b', hit: true },
    { text: ' c', hit: false },
  ]);
  assert.deepEqual(headlineRuns('<<HL>>x<</HL>>'), [{ text: 'x', hit: true }]);
  assert.deepEqual(headlineRuns(''), []);
});

test('lexicalSpans keeps the marks only when the headline is the content', () => {
  assert.deepEqual(lexicalSpans('a <<HL>>b<</HL>>', 'a b'), [[2, 3]]);
  assert.deepEqual(lexicalSpans('a <<HL>>b<</HL>>', 'a b and more'), []);
  assert.deepEqual(lexicalSpans(null, 'a b'), []);
});
