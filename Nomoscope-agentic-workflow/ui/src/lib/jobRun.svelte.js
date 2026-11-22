// "Run a job and show its progress", once: the state a page keeps while it
// submits work to the worker and follows it (ADR 0004 — a job is a row, its
// log is rows). Pages render it with <JobProgress> and <JobLog>.
//
//   const job = createJobRun({ fromLine: fromWorkflowLine });
//   await job.session(async () => {
//     const final = await job.follow('workflow', payload);
//     job.summary = …;
//   });
//
// A session spans one or more jobs (an ingest followed by an embeddings
// build) and owns `running`, the clock and the error; each `follow` resets
// the progress bar and appends to the same log. Create it during component
// initialisation: the clock is an $effect.
import { api, submitAndFollow } from './api.js';
import { summarize } from '@shared/lib/jobs.js';
import { fromProgressEvent, percentDone } from './progress.js';
import { formatDuration } from '@shared/lib/format.js';

/**
 * @param {object} [options]
 * @param {(progress, line: string) => object} [options.fromLine] progress read
 *   off console lines, for a CLI that prints no `@progress` (the workflow).
 * @param {boolean | null} [options.workerAlive] getter: false = say up front that
 *   the job will wait in the queue.
 */
export function createJobRun({ fromLine = null, workerAlive = () => null } = {}) {
  let running = $state(false);
  let jobId = $state(null);
  let lines = $state([]);
  let progress = $state(null);
  // the latest `detail` of any progress event, shown before there is a count
  let note = $state('');
  let summary = $state('');
  let error = $state('');
  let startedAt = $state(0);
  let lastEventAt = $state(0);
  let now = $state(0);

  // Tick a 1 s clock while a session runs, so the elapsed time and the
  // "no news for …" warning move while the job is silent.
  $effect(() => {
    if (!running) return;
    const timer = setInterval(() => (now = Date.now()), 1000);
    return () => clearInterval(timer);
  });

  const log = (line, stream = 'system') => {
    lines = [...lines, { stream, line }];
  };

  const handlers = {
    onSubmit: (id) => {
      jobId = id;
      log(`job #${id} submitted`);
    },
    onLine: (event) => {
      lastEventAt = Date.now();
      if (fromLine) progress = fromLine(progress, event.line);
      lines = [...lines, event];
    },
    onProgress: (data) => {
      lastEventAt = Date.now();
      if (data?.detail) note = data.detail;
      progress = fromProgressEvent(progress, data);
    },
  };

  return {
    get running() {
      return running;
    },
    get jobId() {
      return jobId;
    },
    get lines() {
      return lines;
    },
    get progress() {
      return progress;
    },
    set progress(value) {
      progress = value;
    },
    get note() {
      return note;
    },
    get pct() {
      return percentDone(progress);
    },
    get summary() {
      return summary;
    },
    set summary(value) {
      summary = value;
    },
    get error() {
      return error;
    },
    set error(value) {
      error = value;
    },
    /** Milliseconds since the session started. */
    get elapsed() {
      return running ? now - startedAt : 0;
    },
    /** Milliseconds since the job last printed anything. */
    get silent() {
      return running ? now - lastEventAt : 0;
    },
    /** "3m 05s" since the session started. */
    get took() {
      return formatDuration(Date.now() - startedAt);
    },
    log,

    /**
     * Run `body` as one session: state reset, `running` while it runs, any
     * error it throws shown as `error`. Resolves with what `body` returns
     * (undefined when it threw).
     */
    async session(body) {
      if (running) return undefined;
      jobId = null;
      lines = [];
      progress = null;
      note = '';
      summary = '';
      error = '';
      startedAt = lastEventAt = now = Date.now();
      running = true;
      if (workerAlive() === false) log('no worker alive — the job waits in the queue until one starts');
      try {
        return await body();
      } catch (e) {
        error = String(e?.message ?? e);
        return undefined;
      } finally {
        running = false;
      }
    },

    /** Submit a job inside a session and follow it to the end; resolves with its final row. */
    follow(jobType, payload) {
      progress = null;
      note = '';
      return submitAndFollow(jobType, payload, handlers);
    },

    /** Ask the worker to stop the job being followed; a refusal is shown, not thrown. */
    async cancel() {
      if (jobId == null) return;
      try {
        await api.cancelJob(jobId);
      } catch (e) {
        error = `Could not cancel job #${jobId}: ${e}`;
      }
    },

    /** The default one-line outcome of a finished job. */
    summarize: (final, took = '') => summarize(final, took),
  };
}
