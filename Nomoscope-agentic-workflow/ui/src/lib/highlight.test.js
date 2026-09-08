// Run with: node --test src/lib
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { splitSentences, lexicalSpans, tintLevels, renderView, MARK_START, MARK_END } from './highlight.js';

const circular =
  'P\nar ailleurs, le Conseil a porté, à compter du 1er juillet 2025 :\n' +
  "l'allocation minimale à 32,13 euros,\n" +
  "l'allocation minimale versée aux demandeurs d'emploi en formation à 22,99 euros,\n" +
  'le plancher de l’alinéa 2 du §1 er de l’article 17 bis du règlement général\n' +
  'à l’application du coefficient de dégressivité à 64,80 euros.';

test('segments cover the whole text and glue fragments', () => {
  const segs = splitSentences(circular);
  assert.equal(segs[0].start, 0);
  assert.equal(segs[segs.length - 1].end, circular.length);
  for (let i = 1; i < segs.length; i += 1) assert.equal(segs[i].start, segs[i - 1].end);
  assert.ok(segs[0].text.startsWith('P\nar ailleurs'), 'stray "P" glued to its line');
  assert.ok(segs.some((s) => s.text.startsWith("l'allocation minimale versée")));
});

test('abbreviations and numbers do not split, sentence ends do', () => {
  const text = 'Voir art. 17 et n° 2025-07 du code. Le montant est fixé à 12,5 euros; Il est révisé.';
  assert.deepEqual(
    splitSentences(text).map((s) => s.text),
    ['Voir art. 17 et n° 2025-07 du code.', 'Le montant est fixé à 12,5 euros;', 'Il est révisé.'].filter(
      (s) => s.length >= 20 || true,
    ).reduce((acc, s) => {
      // "Il est révisé." is shorter than MIN_SENTENCE_CHARS and gets glued to the previous one.
      if (s === 'Il est révisé.') acc[acc.length - 1] += ' ' + s;
      else acc.push(s);
      return acc;
    }, []),
  );
});

test('lexical spans map headline markers back to content offsets', () => {
  const content = "l'allocation en faveur des demandeurs";
  const headline = `l'${MARK_START}allocation${MARK_END} en faveur des ${MARK_START}demandeurs${MARK_END}`;
  assert.deepEqual(lexicalSpans(headline, content), [[2, 12], [27, 37]]);
  assert.deepEqual(lexicalSpans(headline, content + ' x'), [], 'mismatch loses the marks');
  assert.deepEqual(lexicalSpans(null, content), []);
});

test('tint levels single out the best sentence', () => {
  assert.deepEqual(tintLevels([0.5, 0.62, 0.58, null, 0.3]), [null, 'best', 'near', null, null]);
  assert.deepEqual(tintLevels([0.61, 0.62]), ['best', 'best']);
  assert.deepEqual(tintLevels([0.3, 0.2]), [null, null], 'nothing close enough');
  assert.deepEqual(tintLevels([0.9]), [null], 'a single sentence has nothing to single out');
});

test('renderView cuts marks inside sentences', () => {
  const content = 'Alpha beta gamma delta. Epsilon zeta eta theta iota.';
  const headline = `Alpha ${MARK_START}beta${MARK_END} gamma delta. Epsilon zeta ${MARK_START}eta${MARK_END} theta iota.`;
  const view = renderView(content, headline, [0.3, 0.7]);
  assert.equal(view.length, 2);
  assert.equal(view[1].level, 'best');
  assert.deepEqual(view[0].parts.map((p) => [p.text, p.mark]), [['Alpha ', false], ['beta', true], [' gamma delta.', false]]);
  assert.equal(view.flatMap((s) => s.parts).map((p) => p.text).join(''), content);
});
