// The worker's status, polled once per app and read by every page (the
// ribbon's Connection group, the model pickers, the "worker offline" badges,
// the Jobs page). Each app wires its fetch in its lib/api.js
// (`worker.use(api.workerStatus)`) and its shell polls (`worker.poll(ms)`);
// a page that needs it fresh now calls `worker.refresh()`.
import { anyAlive, llmModels } from './models.js';

function createWorker() {
  let status = $state(null); // { workers: [...], models: [...] }
  let error = $state('');
  let fetchStatus = null;
  let inFlight = null;

  return {
    /** The raw status row set, null until the first answer. */
    get status() { return status; },
    get error() { return error; },
    /** true / false, null while unknown. */
    get alive() { return anyAlive(status); },
    get workers() { return status?.workers ?? []; },
    get models() { return status?.models ?? []; },
    get llmModels() { return llmModels(status); },

    use(fetcher) {
      fetchStatus = fetcher;
    },

    /** Read the status now; concurrent callers share one round trip. */
    refresh() {
      if (!fetchStatus) return Promise.resolve(status);
      inFlight ??= fetchStatus()
        .then((next) => {
          status = next;
          error = '';
          return next;
        })
        .catch((e) => {
          // unknown, not "offline": the database did not answer
          status = null;
          error = String(e);
          return null;
        })
        .finally(() => (inFlight = null));
      return inFlight;
    },

    /** Poll every `ms` from now on; returns the stop function (an $effect cleanup). */
    poll(ms) {
      this.refresh();
      const timer = setInterval(() => this.refresh(), ms);
      return () => clearInterval(timer);
    },
  };
}

export const worker = createWorker();
