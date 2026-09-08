// Answer highlighting for Database-tab search hits. Pure text functions, no
// Svelte: the component renders what these return.
//
// Two layers, answering two different questions:
//   - lexical marks: which words of the chunk the full-text half matched
//     (Postgres ts_headline, language-aware stemming), exact and cheap;
//   - sentence tint: which sentence of the chunk is closest to the query
//     for BGE-M3, the "this is probably the answer" hint, which also works in
//     Embeddings mode where the lexical layer has nothing to show.

export const MARK_START = '<<HL>>';
export const MARK_END = '<</HL>>';

/** Sentences shorter than this are glued to their neighbour (a stray "P" before "ar ailleurs…"). */
export const MIN_SENTENCE_CHARS = 20;
/**
 * The best sentence is only tinted when it is at least this close to the query.
 * Calibrated on a Unédic circular: matching FR/EN queries peak at 0.67–0.86,
 * an unrelated query (VAT on books) at 0.53.
 */
export const MIN_SIMILARITY = 0.55;
/** Sentences within this margin of the best one share its tint … */
export const BEST_MARGIN = 0.02;
/** … and sentences within this margin get the lighter tint. */
export const NEAR_MARGIN = 0.05;

const OPENERS = new Set(['«', '"', '“', '(', '[']);

function startsSentence(text, i) {
  // Skip whitespace, then require an uppercase letter, a digit, or an opener:
  // "art. 17" and "n° 2025-07" must not split, "… euros, le plancher" neither.
  let j = i;
  while (j < text.length && /\s/.test(text[j])) j += 1;
  if (j === i || j >= text.length) return false;
  const ch = text[j];
  return OPENERS.has(ch) || /\p{Lu}/u.test(ch) || /\d/.test(ch);
}

/**
 * Split a chunk into contiguous sentence segments covering the whole string.
 * Returns [{ start, end, text, scorable }]; `text` is the trimmed sentence sent
 * to the encoder, `scorable` false for fragments too short to mean anything.
 */
export function splitSentences(content) {
  const cuts = [];
  for (let i = 0; i < content.length; i += 1) {
    const ch = content[i];
    if (ch === '\n') {
      cuts.push(i + 1);
    } else if ('.;!?'.includes(ch) && startsSentence(content, i + 1)) {
      cuts.push(i + 1);
    }
  }
  let segments = [];
  let start = 0;
  for (const cut of [...cuts, content.length]) {
    if (cut > start) segments.push({ start, end: cut });
    start = cut;
  }
  // Glue fragments to their neighbour so a broken line does not become a sentence.
  const merged = [];
  for (const seg of segments) {
    const previous = merged[merged.length - 1];
    if (previous && trimmed(content, previous).length < MIN_SENTENCE_CHARS) {
      previous.end = seg.end;
    } else {
      merged.push({ ...seg });
    }
  }
  const last = merged[merged.length - 1];
  if (merged.length > 1 && trimmed(content, last).length < MIN_SENTENCE_CHARS) {
    merged[merged.length - 2].end = last.end;
    merged.pop();
  }
  return merged.map((seg) => {
    const text = trimmed(content, seg);
    return { ...seg, text, scorable: text.length >= MIN_SENTENCE_CHARS && /\p{L}/u.test(text) };
  });
}

function trimmed(content, seg) {
  return content.slice(seg.start, seg.end).trim();
}

/**
 * Offsets of the lexical marks in `content`, read off a ts_headline rendering
 * of the same text. Returns [] when the headline does not reproduce the content
 * verbatim once the markers are removed, so a mismatch loses the marks rather
 * than shifting them onto the wrong words.
 */
export function lexicalSpans(headline, content) {
  if (!headline) return [];
  const spans = [];
  let plain = '';
  let open = null;
  let i = 0;
  while (i < headline.length) {
    if (headline.startsWith(MARK_START, i)) {
      open = plain.length;
      i += MARK_START.length;
    } else if (headline.startsWith(MARK_END, i)) {
      if (open != null && plain.length > open) spans.push([open, plain.length]);
      open = null;
      i += MARK_END.length;
    } else {
      plain += headline[i];
      i += 1;
    }
  }
  return plain === content ? spans : [];
}

/**
 * Tint level per sentence from its similarity: 'best', 'near' or null.
 * Nothing is tinted when fewer than two sentences were scored (a one-sentence
 * chunk has nothing to single out) or when even the best is far from the query.
 */
export function tintLevels(similarities) {
  const scored = similarities.filter((s) => s != null);
  if (scored.length < 2) return similarities.map(() => null);
  const best = Math.max(...scored);
  if (best < MIN_SIMILARITY) return similarities.map(() => null);
  return similarities.map((s) => {
    if (s == null) return null;
    if (s >= best - BEST_MARGIN) return 'best';
    if (s >= best - NEAR_MARGIN) return 'near';
    return null;
  });
}

/**
 * Everything the template needs to paint one hit: sentence segments carrying
 * their tint level and similarity, each cut into { text, mark } parts along
 * the lexical spans.
 */
export function renderView(content, headline, similarities) {
  const sentences = splitSentences(content);
  const spans = lexicalSpans(headline, content);
  const sims = sentences.map((s, i) => (s.scorable && similarities ? similarities[i] ?? null : null));
  const levels = tintLevels(sims);
  return sentences.map((seg, i) => ({
    level: levels[i],
    similarity: sims[i],
    parts: cutParts(content, seg.start, seg.end, spans),
  }));
}

function cutParts(content, start, end, spans) {
  const parts = [];
  let pos = start;
  for (const [a, b] of spans) {
    const from = Math.max(a, start);
    const to = Math.min(b, end);
    if (to <= from) continue;
    if (from > pos) parts.push({ text: content.slice(pos, from), mark: false });
    parts.push({ text: content.slice(from, to), mark: true });
    pos = to;
  }
  if (pos < end) parts.push({ text: content.slice(pos, end), mark: false });
  return parts;
}
