// Single seam between the Svelte frontend and the Rust commands.
import { invoke } from '@tauri-apps/api/core';
import { listen } from '@tauri-apps/api/event';
import { open } from '@tauri-apps/plugin-shell';

export const api = {
  getEnvConfig: () => invoke('get_env_config'),
  loadQueue: (dataDir) => invoke('load_queue', { payload: { data_dir: dataDir } }),
  saveDecision: (payload) => invoke('save_decision', { payload }),
  loadDecisions: (dataDir, dbUrl, limit = 200) =>
    invoke('load_decisions', { payload: { data_dir: dataDir, db_url: dbUrl, limit } }),
  exportAccepted: (dataDir) => invoke('export_accepted', { payload: { data_dir: dataDir } }),
  pickDataDir: () => invoke('pick_data_dir'),
  dbStats: (dbUrl) => invoke('db_stats', { payload: { db_url: dbUrl } }),
  searchArticles: (payload) => invoke('search_articles', { payload }),
  // Every language rendering (authentic / official / machine translation) of the
  // legal-unit version a cited chunk belongs to.
  chunkRenderings: (dbUrl, chunkId) =>
    invoke('chunk_renderings', { payload: { db_url: dbUrl, chunk_id: chunkId } }),
  // Golden set: drafted evaluation cases on disk, and the reviewer's verdict.
  goldenCases: (datasetDir) => invoke('golden_cases', { payload: { dataset_dir: datasetDir } }),
  setGoldenVerified: (payload) => invoke('set_golden_verified', { payload }),
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
  // Parameters tab: params-schema listing, Phoenix trace-link resolution, and
  // launching the agentic workflow CLI (same contract as runIngest/onIngestLog).
  paramsList: (dbUrl) => invoke('params_list', { payload: { db_url: dbUrl } }),
  phoenixProjects: (dbUrl) => invoke('phoenix_projects', { payload: { db_url: dbUrl } }),
  runWorkflow: (payload) => invoke('run_workflow', { payload }),
  // Impact tab: EcoLogits report over Phoenix LLM spans, computed by the
  // pipeline CLI (`nomoscope-workflow impact --json`).
  impactReport: (dbUrl, project = '', zone = '') =>
    invoke('impact_report', { payload: { db_url: dbUrl, project, zone } }),
  stopWorkflow: (runId) => invoke('stop_workflow', { runId }),
  onWorkflowLog: (handler) => listen('workflow-log', (event) => handler(event.payload)),
  openExternal: (url) => open(url),
};
