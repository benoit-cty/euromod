// The article search's lexical marks, read once for both apps. The search SQL
// (db/search.rs) returns a hit's `content` as a `headline` too: Postgres
// ts_headline with every matched lexeme wrapped in <<HL>>…<</HL>>.

export const MARK_START = '<<HL>>';
export const MARK_END = '<</HL>>';

/**
 * Parse a headline into its plain text and the [start, end) offsets of the
 * marked spans in that text. A start marker never closed marks to the end of
 * nothing (it is dropped), an empty span is not a span.
 */
export function parseHeadline(headline) {
  const text = String(headline ?? '');
  const spans = [];
  let plain = '';
  let open = null;
  let i = 0;
  while (i < text.length) {
    if (text.startsWith(MARK_START, i)) {
      open = plain.length;
      i += MARK_START.length;
    } else if (text.startsWith(MARK_END, i)) {
      if (open != null && plain.length > open) spans.push([open, plain.length]);
      open = null;
      i += MARK_END.length;
    } else {
      plain += text[i];
      i += 1;
    }
  }
  return { plain, spans };
}

/** The headline as [{ text, hit }] runs, for a template to paint marks. */
export function headlineRuns(headline) {
  const { plain, spans } = parseHeadline(headline);
  const runs = [];
  let at = 0;
  for (const [start, end] of spans) {
    if (start > at) runs.push({ text: plain.slice(at, start), hit: false });
    runs.push({ text: plain.slice(start, end), hit: true });
    at = end;
  }
  if (at < plain.length) runs.push({ text: plain.slice(at), hit: false });
  return runs;
}

/**
 * Offsets of the lexical marks in `content`, read off a headline of the same
 * text. Returns [] when the headline does not reproduce the content verbatim
 * once the markers are removed, so a mismatch loses the marks rather than
 * shifting them onto the wrong words.
 */
export function lexicalSpans(headline, content) {
  if (!headline) return [];
  const { plain, spans } = parseHeadline(headline);
  return plain === content ? spans : [];
}
