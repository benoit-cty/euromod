// What a running job's progress bar shows, from its events. Pure functions:
// jobRun.svelte.js feeds them, `npm test` checks them.
//
// Most jobs print structured `@progress {json}` lines (the ingest, embed and
// translate CLIs: {done, total, detail, …}; a build waiting for the GPU lock:
// {phase: "waiting", detail}). The workflow CLI (`run-targets`, a Parameters
// tab check) prints none: it is read off its console instead — "[i/N] target"
// when a parameter starts, "  › step" per step, a "…: routing=…" line when
// one is routed.

/** Fold one structured progress event into the bar's state. */
export function fromProgressEvent(progress, data) {
  if (!data) return progress;
  if (data.total > 0) return { ...(progress ?? {}), ...data };
  // no total (a phase, a waiting build): keep the counts, show what it says
  return progress ? { ...progress, detail: data.detail ?? progress.detail } : progress;
}

const HEAD_RE = /^\[(\d+)\/(\d+)\]\s*(.*)$/;
const STEP_RE = /^\s+›\s+(.+)$/;
const ROUTED_RE = /\brouting=(\S+)/;

/** Fold one console line of the workflow CLI into the bar's state. */
export function fromWorkflowLine(progress, line) {
  const head = String(line ?? '').match(HEAD_RE);
  if (head) {
    // The parameter is starting: done counts the ones already finished.
    return { done: Number(head[1]) - 1, total: Number(head[2]), current: head[3], detail: '' };
  }
  if (!progress) return progress;
  const step = line.match(STEP_RE);
  if (step) return { ...progress, detail: step[1] };
  const routed = line.match(ROUTED_RE);
  if (routed) return { ...progress, done: Math.min(progress.done + 1, progress.total), detail: routed[1] };
  return progress;
}

/** Percentage done, 0–100; null without a total (the bar runs indeterminate). */
export function percentDone(progress) {
  if (!(progress?.total > 0)) return null;
  return Math.min(100, Math.round((progress.done / progress.total) * 100));
}
