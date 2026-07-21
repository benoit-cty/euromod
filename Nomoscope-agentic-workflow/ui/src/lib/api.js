// Single seam between the Svelte frontend and the Rust commands.
import { invoke } from '@tauri-apps/api/core';
import { listen } from '@tauri-apps/api/event';
import { open } from '@tauri-apps/plugin-shell';

export const api = {
  getEnvConfig: () => invoke('get_env_config'),
  loadQueue: (dataDir) => invoke('load_queue', { payload: { data_dir: dataDir } }),
  saveDecision: (payload) => invoke('save_decision', { payload }),
  loadDecisions: (dataDir, limit = 200) =>
    invoke('load_decisions', { payload: { data_dir: dataDir, limit } }),
  exportAccepted: (dataDir) => invoke('export_accepted', { payload: { data_dir: dataDir } }),
  pickDataDir: () => invoke('pick_data_dir'),
  dbStats: (dbUrl) => invoke('db_stats', { payload: { db_url: dbUrl } }),
  searchArticles: (payload) => invoke('search_articles', { payload }),
  evalRuns: (dbUrl) => invoke('eval_runs', { payload: { db_url: dbUrl } }),
  evalRunDetail: (dbUrl, runPk) =>
    invoke('eval_run_detail', { payload: { db_url: dbUrl, run_pk: runPk } }),
  // Run an nomotheca_ingest CLI script; resolves with { canceled, success, code }
  // once the process exits. Live output arrives via onIngestLog events.
  runIngest: (payload) => invoke('run_ingest', { payload }),
  stopIngest: (runId) => invoke('stop_ingest', { runId }),
  // Subscribe to streamed log lines: handler({ run_id, stream, line }).
  // Returns a promise resolving to an unlisten function.
  onIngestLog: (handler) => listen('ingest-log', (event) => handler(event.payload)),
  openExternal: (url) => open(url),
};
