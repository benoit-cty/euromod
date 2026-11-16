// Following a worker job from either desktop app: poll its events by
// last-seen id and its status row until it reaches a terminal state (ADR 0004
// — no NOTIFY, no process, a row is the API).
//
// The transport is the app's `api` (submitJob, jobStatus, jobEvents) and is
// passed in, so this file has no dependency on @tauri-apps and its cursor
// logic runs under plain node. Each app binds it once (`bindJobs(api)` in its
// lib/api.js) and its components call the bound functions.

export const TERMINAL = new Set(['succeeded', 'failed', 'cancelled']);

/**
 * The status to show for a job row. A claimed job is `running` in ops.jobs
 * from the moment its subprocess starts, but an `embeddings build` (an embed
 * job, or a workflow/eval job's scout) may then sit behind another build's GPU
 * lock; it reports that as a `phase: "waiting"` progress line, and a running
 * job whose latest progress says so is shown as `waiting`.
 */
export function displayStatus(job) {
  if (job?.status === 'running' && job.progress?.phase === 'waiting') return 'waiting';
  return job?.status ?? '';
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Follow job `id` until it finishes. Handlers:
 *   onLine({ id, at, stream, line })  every stdout/stderr/system event, in order, once
 *   onProgress(data, event)           every progress event (`data` is the parsed JSON)
 *   onStatus(row)                     every status poll (running/queued/… with progress)
 * Resolves with the final status row (`status` ∈ succeeded|failed|cancelled).
 * Events that land between the last event poll and the terminal status are
 * drained before resolving, so nothing printed at exit is lost.
 */
export async function followJob(id, handlers, pollMs, transport) {
  const { onLine, onProgress, onStatus } = handlers ?? {};
  const wait = transport.sleep ?? sleep;
  let after = 0;

  const drain = async () => {
    const res = await transport.jobEvents(id, after);
    for (const event of res.events ?? []) {
      if (event.id <= after) continue; // never deliver twice
      after = event.id;
      if (event.stream === 'progress') onProgress?.(event.data ?? parseProgress(event.line), event);
      else onLine?.(event);
    }
  };

  for (;;) {
    await drain();
    const status = await transport.jobStatus(id);
    onStatus?.(status);
    if (TERMINAL.has(status.status)) {
      await drain();
      return status;
    }
    await wait(pollMs);
  }
}

/** Submit a job and follow it. Resolves with the final status row; `onSubmit(id)` fires first. */
export async function submitAndFollow(jobType, payload, handlers, pollMs, transport) {
  const { id } = await transport.submitJob(jobType, payload, handlers?.priority ?? 0);
  handlers?.onSubmit?.(id);
  return followJob(id, handlers, pollMs, transport);
}

/** followJob / submitAndFollow bound to an app's transport (its `api`). */
export function bindJobs(transport, pollMs = 1000) {
  return {
    followJob: (id, handlers = {}) => followJob(id, handlers, pollMs, transport),
    submitAndFollow: (jobType, payload, handlers = {}) => submitAndFollow(jobType, payload, handlers, pollMs, transport),
  };
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
      return `Failed${suffix}: ${lastLine(status.error)}`;
    default:
      return status?.status ?? '';
  }
}

/** The last line of a job's error text, for an inline message. */
export function lastLine(text) {
  const lines = String(text ?? '').trim().split('\n');
  return lines[lines.length - 1] || 'no error recorded';
}
