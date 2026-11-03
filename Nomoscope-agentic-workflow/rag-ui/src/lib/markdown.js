// A small, safe Markdown renderer for assistant answers.
//
// Everything is HTML-escaped first; only the constructs below are turned back
// into markup: headings, paragraphs, lists, block quotes, pipe tables, fenced
// and inline code, bold/italic, http(s) links (opened through the shell, never
// navigated in the webview) and citation markers — `[2]` or `[1, 3]` become
// buttons that select that quote in the source panel.

const ESCAPES = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };

export function escapeHtml(text) {
  return String(text ?? '').replace(/[&<>"']/g, (c) => ESCAPES[c]);
}

const CITE = /\[(\d{1,3}(?:\s*,\s*\d{1,3})*)\](?!\()/g;

// Inline markup over already-escaped text. Code spans are cut out first so
// nothing inside them is interpreted.
export function renderInline(escaped) {
  const codes = [];
  let text = escaped.replace(/`([^`]+)`/g, (_, code) => {
    codes.push(code);
    return `\u0000${codes.length - 1}\u0000`;
  });
  text = text
    .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, (_, label, href) => `<a class="ext" href="${href}" data-href="${href}">${label}</a>`)
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*\w])\*([^*\s][^*]*)\*(?!\w)/g, '$1<em>$2</em>')
    .replace(/(^|[^_\w])_([^_\s][^_]*)_(?!\w)/g, '$1<em>$2</em>')
    .replace(CITE, (_, list) =>
      list
        .split(',')
        .map((n) => n.trim())
        .map((n) => `<button type="button" class="cite" data-cite="${n}">${n}</button>`)
        .join(''),
    );
  return text.replace(/\u0000(\d+)\u0000/g, (_, i) => `<code>${codes[Number(i)]}</code>`);
}

function isTableSeparator(line) {
  return /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/.test(line);
}

function tableCells(line) {
  return line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map((c) => c.trim());
}

export function renderMarkdown(source) {
  const lines = String(source ?? '').replace(/\r\n?/g, '\n').split('\n');
  const out = [];
  let paragraph = [];
  let list = null; // { tag, items }

  const flushParagraph = () => {
    if (paragraph.length) out.push(`<p>${paragraph.map((l) => renderInline(escapeHtml(l))).join('<br>')}</p>`);
    paragraph = [];
  };
  const flushList = () => {
    if (list) out.push(`<${list.tag}>${list.items.map((i) => `<li>${renderInline(escapeHtml(i))}</li>`).join('')}</${list.tag}>`);
    list = null;
  };
  const flush = () => {
    flushParagraph();
    flushList();
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    const fence = line.match(/^\s*```\s*([\w-]*)\s*$/);
    if (fence) {
      flush();
      const body = [];
      for (i++; i < lines.length && !/^\s*```\s*$/.test(lines[i]); i++) body.push(lines[i]);
      out.push(`<pre><code>${escapeHtml(body.join('\n'))}</code></pre>`);
      continue;
    }
    if (!line.trim()) {
      flush();
      continue;
    }
    const heading = line.match(/^(#{1,4})\s+(.*)$/);
    if (heading) {
      flush();
      const level = Math.min(heading[1].length + 2, 6); // answers sit under the app's own headings
      out.push(`<h${level}>${renderInline(escapeHtml(heading[2]))}</h${level}>`);
      continue;
    }
    if (line.trim().startsWith('|') && i + 1 < lines.length && isTableSeparator(lines[i + 1])) {
      flush();
      const head = tableCells(line);
      const rows = [];
      for (i += 2; i < lines.length && lines[i].trim().startsWith('|'); i++) rows.push(tableCells(lines[i]));
      i--;
      const cell = (tag) => (c) => `<${tag}>${renderInline(escapeHtml(c))}</${tag}>`;
      out.push(
        `<table><thead><tr>${head.map(cell('th')).join('')}</tr></thead>` +
          `<tbody>${rows.map((r) => `<tr>${r.map(cell('td')).join('')}</tr>`).join('')}</tbody></table>`,
      );
      continue;
    }
    const quote = line.match(/^\s*>\s?(.*)$/);
    if (quote) {
      flush();
      const body = [quote[1]];
      while (i + 1 < lines.length && /^\s*>/.test(lines[i + 1])) body.push(lines[++i].replace(/^\s*>\s?/, ''));
      out.push(`<blockquote>${body.map((l) => renderInline(escapeHtml(l))).join('<br>')}</blockquote>`);
      continue;
    }
    const bullet = line.match(/^\s*[-*•]\s+(.*)$/);
    const numbered = line.match(/^\s*\d+[.)]\s+(.*)$/);
    if (bullet || numbered) {
      flushParagraph();
      const tag = bullet ? 'ul' : 'ol';
      if (list && list.tag !== tag) flushList();
      list ??= { tag, items: [] };
      list.items.push((bullet ?? numbered)[1]);
      continue;
    }
    if (list && /^\s{2,}\S/.test(line)) {
      list.items[list.items.length - 1] += ' ' + line.trim(); // wrapped list item
      continue;
    }
    flushList();
    paragraph.push(line);
  }
  flush();
  return out.join('\n');
}
