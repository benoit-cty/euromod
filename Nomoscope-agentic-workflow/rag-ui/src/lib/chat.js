// Pure helpers for the chat: what a turn sends, how a tool step reads, where
// an extract sits in its chunk. No Tauri imports, so `npm test` runs them.

export const COUNTRIES = ['FR', 'BE', 'NL', 'ES', 'IE', 'LT'];
export const CHAT_PRIORITY = 50; // ahead of batches, behind the encode lane

export function newConversationId() {
  const rand = globalThis.crypto?.randomUUID?.() ?? `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
  return `chat-${rand}`;
}

/**
 * The `messages` of a chat job: every earlier turn that got an answer, then
 * the new question. Failed or cancelled turns are left out — the model never
 * saw an answer to them. An assistant turn carries its verified quotes only,
 * so a follow-up ("more on [2]") resolves to a chunk the corpus really holds.
 */
export function buildMessages(turns, question) {
  const messages = [];
  for (const turn of turns) {
    if (turn.status !== 'succeeded' || !turn.result) continue;
    messages.push({ role: 'user', content: turn.question });
    messages.push({
      role: 'assistant',
      content: turn.result.answer ?? '',
      quotes: (turn.result.quotes ?? [])
        .filter((q) => q.verified)
        .map(({ chunk_id, citation, extract }) => ({ chunk_id, citation, extract })),
    });
  }
  messages.push({ role: 'user', content: question });
  return messages;
}

/** Fold one `@progress` tool event into a turn's step list (start, then done). */
export function applyStep(steps, event) {
  if (event?.event !== 'tool') return steps;
  if (event.status === 'start') {
    steps.push({ tool: event.tool, args: event.args ?? {}, done: false, summary: '' });
    return steps;
  }
  const open = [...steps].reverse().find((s) => s.tool === event.tool && !s.done);
  const step = open ?? { tool: event.tool, args: {}, done: false, summary: '' };
  if (!open) steps.push(step);
  step.done = true;
  step.summary = event.summary ?? '';
  step.chunk_ids = event.chunk_ids ?? [];
  step.urls = event.urls ?? [];
  return steps;
}

const TOOL_LABELS = {
  search_legislation: 'Searched the legislation',
  find_article: 'Looked up',
  read_article: 'Read article',
  web_search: 'Searched the web',
};

export function stepLabel(step) {
  const a = step.args ?? {};
  const where = a.countries?.length === 1 ? ` (${a.countries[0]}${a.region ? ' + ' + a.region : ''})` : a.country ? ` (${a.country})` : '';
  switch (step.tool) {
    case 'search_legislation':
      return `${TOOL_LABELS.search_legislation}${where}${a.language === 'en' ? ', English' : ''}: «${a.query ?? ''}»`;
    case 'find_article':
      return `${TOOL_LABELS.find_article}${where}: «${a.reference ?? ''}»`;
    case 'read_article':
      return TOOL_LABELS.read_article;
    case 'web_search':
      return `${TOOL_LABELS.web_search}${where}${a.domains?.length ? ' on ' + a.domains.join(', ') : ''}: «${a.query ?? ''}»`;
    default:
      return step.tool;
  }
}

/**
 * Where `extract` sits in `content`: exact first, then with any whitespace
 * run matching any other (the same tolerance as retrieval.verify_extract).
 * Returns { before, match, after } or null.
 */
export function locateExtract(content, extract) {
  if (!content || !extract?.trim()) return null;
  let start = content.indexOf(extract);
  let length = extract.length;
  if (start < 0) {
    const pattern = extract.trim().split(/\s+/).map(escapeRegExp).join('\\s+');
    const m = new RegExp(pattern).exec(content);
    if (!m) return null;
    start = m.index;
    length = m[0].length;
  }
  return { before: content.slice(0, start), match: content.slice(start, start + length), after: content.slice(start + length) };
}

function escapeRegExp(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/** Split a ts_headline with <<HL>>…<</HL>> markers into [{text, hit}] runs. */
export function headlineRuns(headline) {
  const runs = [];
  const re = /<<HL>>(.*?)<<\/HL>>/gs;
  let last = 0;
  for (let m; (m = re.exec(headline)); ) {
    if (m.index > last) runs.push({ text: headline.slice(last, m.index), hit: false });
    runs.push({ text: m[1], hit: true });
    last = m.index + m[0].length;
  }
  if (last < headline.length) runs.push({ text: headline.slice(last), hit: false });
  return runs;
}

/** The ingest job for an act found on the web (same form the scout uses). */
export function ingestPayload(discovery) {
  return {
    command: 'instrument',
    args: [discovery.country.toLowerCase(), discovery.ingest_id ?? discovery.instrument_id, '--max-items', '500'],
  };
}

export function todayIso() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}
