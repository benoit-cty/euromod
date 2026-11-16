// The legislation library's statistics (`db_stats`: two 7-table
// count(DISTINCT) joins), read once and shared by the pages that show them —
// the Overview, the Legislation page's status, the Add-sources pickers —
// instead of once per page. A page's Refresh reloads it for all of them.
import { api } from './api.js';

function createLibrary() {
  let stats = $state(null);
  let error = $state('');
  let loading = $state(false);
  let inFlight = null;

  return {
    get stats() { return stats; },
    get error() { return error; },
    get loading() { return loading; },

    /** The statistics; read from the database the first time, or when `force`d. */
    load(force = false) {
      if (stats && !force) return Promise.resolve(stats);
      inFlight ??= (async () => {
        loading = true;
        try {
          stats = await api.dbStats();
          error = '';
        } catch (e) {
          error = String(e);
        } finally {
          loading = false;
          inFlight = null;
        }
        return stats;
      })();
      return inFlight;
    },

    /** Forget what was read (the app was pointed at another database). */
    reset() {
      stats = null;
      error = '';
    },
  };
}

export const library = createLibrary();
