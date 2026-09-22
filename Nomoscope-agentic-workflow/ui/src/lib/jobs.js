// Following a worker job from the UI: poll its events by last-seen id and its
// status row until it reaches a terminal state (ADR 0004 — no NOTIFY, no
// process, a row is the API).
//
// The transport is injectable so the cursor logic is testable under plain
// node (the default one is the Tauri `api` module, imported lazily so this
// file has no static dependency on @tauri-apps).

export const TERMINAL = new Set(['succeeded', 'failed', 'cancelled']);

const defaultTransport = {
  submitJob: async (...args) => (await import('./api.js')).api.submitJob(...args),
  jobStatus: async (...args) => (await import('./api.js')).api.jobStatus(...args),
  jobEvents: async (...args) => (await import('./api.js')).api.jobEvents(...args),
  sleep: (ms) => new Promise((resolve) => setTimeout(resolve, ms)),
};

/**
 * Follow job `id` until it finishes. Handlers:
 *   onLine({ id, at, stream, line })  every stdout/stderr/system event, in order, once
 *   onProgress(data, event)           every progress event (`data` is the parsed JSON)
 *   onStatus(row)                     every status poll (running/queued/… with progress)
 * Resolves with the final status row (`status` ∈ succeeded|failed|cancelled).
 * Events that land between the last event poll and the terminal status are
 * drained before resolving, so nothing printed at exit is lost.
 */
export async function followJob(dbUrl, id, handlers = {}, pollMs = 1000, transport = defaultTransport) {
  const { onLine, onProgress, onStatus } = handlers;
  let after = 0;

  const drain = async () => {
    const res = await transport.jobEvents(dbUrl, id, after);
    for (const event of res.events ?? []) {
      if (event.id <= after) continue; // never deliver twice
      after = event.id;
      if (event.stream === 'progress') onProgress?.(event.data ?? parseProgress(event.line), event);
      else onLine?.(event);
    }
  };

  for (;;) {
    await drain();
    const status = await transport.jobStatus(dbUrl, id);
    onStatus?.(status);
    if (TERMINAL.has(status.status)) {
      await drain();
      return status;
    }
    await transport.sleep(pollMs);
  }
}

/** Submit a job and follow it. Resolves with the final status row; `onSubmit(id)` fires first. */
export async function submitAndFollow(dbUrl, jobType, payload, handlers = {}, pollMs = 1000, transport = defaultTransport) {
  const { id } = await transport.submitJob(dbUrl, jobType, payload, handlers.priority ?? 0);
  handlers.onSubmit?.(id);
  return followJob(dbUrl, id, handlers, pollMs, transport);
}

const PROGRESS_PREFIX = '@progress ';

// A progress event whose `data` the worker did not parse: read the raw line.
export function parseProgress(line) {
  const text = line?.startsWith(PROGRESS_PREFIX) ? line.slice(PROGRESS_PREFIX.length) : line;
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

/** One-line summary of a finished job for a status bar. */
export function summarize(status, took = '') {
  const suffix = took ? ` after ${took}` : '';
  switch (status?.status) {
    case 'succeeded':
      return `Finished successfully${suffix}.`;
    case 'cancelled':
      return `Cancelled${suffix}.`;
    case 'failed':
      return `Failed${suffix}: ${lastLine(status.error) ?? 'no error recorded'}`;
    default:
      return status?.status ?? '';
  }
}

function lastLine(text) {
  if (!text) return null;
  const lines = String(text).trim().split('\n');
  return lines[lines.length - 1];
}
