// Following a worker job: poll its events by last-seen id and its status row
// until it is terminal (the review UI's ui/src/lib/jobs.js, trimmed: a row is
// the API, no NOTIFY, no process).
import { api } from './api.js';

export const TERMINAL = new Set(['succeeded', 'failed', 'cancelled']);

/**
 * Submit a job and follow it. Handlers: onSubmit(id), onProgress(data),
 * onLine(event), onStatus(row). Resolves with the final status row; events
 * printed just before exit are drained before resolving.
 */
export async function submitAndFollow(dbUrl, jobType, payload, handlers = {}, pollMs = 800) {
  const { id } = await api.submitJob(dbUrl, jobType, payload, handlers.priority ?? 0);
  handlers.onSubmit?.(id);
  let after = 0;
  const drain = async () => {
    const res = await api.jobEvents(dbUrl, id, after);
    for (const event of res.events ?? []) {
      if (event.id <= after) continue;
      after = event.id;
      if (event.stream === 'progress') handlers.onProgress?.(event.data ?? parseProgress(event.line), event);
      else handlers.onLine?.(event);
    }
  };
  for (;;) {
    await drain();
    const status = await api.jobStatus(dbUrl, id);
    handlers.onStatus?.(status);
    if (TERMINAL.has(status.status)) {
      await drain();
      return status;
    }
    await new Promise((resolve) => setTimeout(resolve, pollMs));
  }
}

function parseProgress(line) {
  try {
    return JSON.parse(String(line).replace(/^@progress /, ''));
  } catch {
    return null;
  }
}

/** The last line of a job's error text, for an inline message. */
export function lastLine(text) {
  const lines = String(text ?? '').trim().split('\n');
  return lines[lines.length - 1] || 'no error recorded';
}
