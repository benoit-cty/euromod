import { test } from 'node:test';
import assert from 'node:assert/strict';

import { applyStep, buildMessages, headlineRuns, ingestPayload, locateExtract, stepLabel } from './chat.js';
import { renderMarkdown, renderInline, escapeHtml } from './markdown.js';

test('buildMessages keeps answered turns and their verified quotes only', () => {
  const turns = [
    {
      question: 'Barème 2025 ?',
      status: 'succeeded',
      result: {
        answer: 'Voir [1].',
        quotes: [
          { chunk_id: 'a', citation: 'CGI art. 197', extract: '11 %', verified: true, char_start: 3 },
          { chunk_id: 'b', citation: 'x', extract: 'paraphrase', verified: false },
        ],
      },
    },
    { question: 'lost', status: 'failed', result: null },
  ];
  assert.deepEqual(buildMessages(turns, 'Et 2026 ?'), [
    { role: 'user', content: 'Barème 2025 ?' },
    { role: 'assistant', content: 'Voir [1].', quotes: [{ chunk_id: 'a', citation: 'CGI art. 197', extract: '11 %' }] },
    { role: 'user', content: 'Et 2026 ?' },
  ]);
});

test('applyStep pairs a done event with its open start', () => {
  const steps = [];
  applyStep(steps, { event: 'tool', status: 'start', tool: 'search_legislation', args: { query: 'q', countries: ['FR'] } });
  applyStep(steps, { event: 'tool', status: 'start', tool: 'web_search', args: { query: 'w' } });
  applyStep(steps, { event: 'tool', status: 'done', tool: 'search_legislation', summary: '8 passage(s)', chunk_ids: ['c'] });
  assert.equal(steps.length, 2);
  assert.equal(steps[0].done, true);
  assert.equal(steps[0].summary, '8 passage(s)');
  assert.equal(steps[1].done, false);
  applyStep(steps, { event: 'other' });
  assert.equal(steps.length, 2);
  assert.match(stepLabel(steps[0]), /legislation \(FR\): «q»/);
});

test('locateExtract tolerates whitespace runs like verify_extract', () => {
  const content = 'Le taux est fixé à 11 %\npour la fraction supérieure à 11 497 €.';
  assert.deepEqual(locateExtract(content, '11 % pour la fraction'), {
    before: 'Le taux est fixé à ',
    match: '11 %\npour la fraction',
    after: ' supérieure à 11 497 €.',
  });
  assert.equal(locateExtract(content, 'absent'), null);
  assert.equal(locateExtract(content, ''), null);
  assert.equal(locateExtract(content, 'a (b'), null); // regex metacharacters are literal
});

test('headlineRuns splits ts_headline markers', () => {
  assert.deepEqual(headlineRuns('a <<HL>>b<</HL>> c'), [
    { text: 'a ', hit: false },
    { text: 'b', hit: true },
    { text: ' c', hit: false },
  ]);
});

test('ingestPayload mirrors the scout: lower-case country, suffixed id', () => {
  assert.deepEqual(ingestPayload({ country: 'LT', instrument_id: 'abc', ingest_id: 'abc/asr' }).args.slice(0, 2), ['lt', 'abc/asr']);
});

test('markdown escapes HTML before adding any markup', () => {
  const html = renderMarkdown('<img src=x onerror=alert(1)> **bold**');
  assert.ok(!html.includes('<img'));
  assert.ok(html.includes('&lt;img'));
  assert.ok(html.includes('<strong>bold</strong>'));
  assert.equal(escapeHtml(`"'&`), '&quot;&#39;&amp;');
});

test('citation markers become buttons, links stay links, code stays literal', () => {
  const html = renderInline(escapeHtml('rate [1] and [2, 3], see [Légifrance](https://www.legifrance.gouv.fr/x) `[4]`'));
  assert.equal((html.match(/class="cite"/g) ?? []).length, 3);
  assert.ok(html.includes('data-href="https://www.legifrance.gouv.fr/x"'));
  assert.ok(html.includes('<code>[4]</code>'));
  assert.ok(!renderInline(escapeHtml('[x](javascript:alert(1))')).includes('<a'));
});

test('markdown tables, lists and fences', () => {
  const html = renderMarkdown(
    ['| Tranche | Taux |', '|---|---|', '| 0 – 11 497 | 0 % [1] |', '', '- one', '- two', '', '```', '<b>', '```'].join('\n'),
  );
  assert.ok(html.includes('<th>Tranche</th>'));
  assert.ok(html.includes('<td>0 % <button type="button" class="cite" data-cite="1">1</button></td>'));
  assert.ok(html.includes('<ul><li>one</li><li>two</li></ul>'));
  assert.ok(html.includes('<pre><code>&lt;b&gt;</code></pre>'));
});
