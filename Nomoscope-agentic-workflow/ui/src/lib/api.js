// Single seam between the Svelte frontend and the Rust commands.
//
// The UI is remote (ADR 0004): every call here is a database round trip. Work
// that needs a model or the internet is a job (submitJob → ops.jobs) the
// worker runs; lib/jobs.js follows one to completion.
import { invoke } from '@tauri-apps/api/core';
import { open } from '@tauri-apps/plugin-shell';

export const api = {
  getEnvConfig: () => invoke('get_env_config'),
  // Review queue (params.review_queue) and decisions (params.decide_review_item).
  loadQueue: (dbUrl) => invoke('load_queue', { payload: { db_url: dbUrl } }),
  saveDecision: (payload) => invoke('save_decision', { payload }),
  loadDecisions: (dbUrl, limit = 200) =>
    invoke('load_decisions', { payload: { db_url: dbUrl, limit } }),
  // One file per country, into a folder the reviewer picks: { count, paths, canceled }.
  exportAccepted: (dbUrl) => invoke('export_accepted', { payload: { db_url: dbUrl } }),
  dbStats: (dbUrl) => invoke('db_stats', { payload: { db_url: dbUrl } }),
  // Vector/hybrid modes encode the query on the worker; `notice` is set when
  // no worker was alive and the search fell back to full text.
  searchArticles: (payload) => invoke('search_articles', { payload }),
  // Cosine of each sentence against the query (one BGE-M3 batch on the
  // worker), so the Database tab can tint the sentence of a hit that most
  // likely answers.
  scoreSentences: (dbUrl, query, sentences) =>
    invoke('score_sentences', { payload: { db_url: dbUrl, query, sentences } }),
  // Contributed documents: the instruments a document can be said to implement
  // (title or national-id fragment, `context` instruments excluded).
  searchInstruments: (dbUrl, country, query, limit = 20) =>
    invoke('search_instruments', { payload: { db_url: dbUrl, country, query, limit } }),
  // Every language rendering (authentic / official / machine translation) of the
  // legal-unit version a cited chunk belongs to.
  chunkRenderings: (dbUrl, chunkId) =>
    invoke('chunk_renderings', { payload: { db_url: dbUrl, chunk_id: chunkId } }),
  // Golden set: drafted evaluation cases (eval.golden_cases) and the reviewer's verdict.
  goldenCases: (dbUrl) => invoke('golden_cases', { payload: { db_url: dbUrl } }),
  setGoldenVerified: ({ db_url, id, verified, note }) =>
    invoke('set_golden_verified', { payload: { db_url, id, verified, note } }),
  evalRuns: (dbUrl) => invoke('eval_runs', { payload: { db_url: dbUrl } }),
  evalRunDetail: (dbUrl, runPk) =>
    invoke('eval_run_detail', { payload: { db_url: dbUrl, run_pk: runPk } }),
  // Parameters tab: params-schema listing and Phoenix trace-link resolution.
  paramsList: (dbUrl) => invoke('params_list', { payload: { db_url: dbUrl } }),
  phoenixProjects: (dbUrl) => invoke('phoenix_projects', { payload: { db_url: dbUrl } }),

  // --- jobs (ops.jobs): the only way the UI makes anything run ---
  submitJob: (dbUrl, jobType, payload, priority = 0) =>
    invoke('submit_job', { payload: { db_url: dbUrl, job_type: jobType, payload, priority } }),
  jobStatus: (dbUrl, id) => invoke('job_status', { payload: { db_url: dbUrl, id } }),
  jobEvents: (dbUrl, id, after = 0) =>
    invoke('job_events', { payload: { db_url: dbUrl, id, after } }),
  cancelJob: (dbUrl, id) => invoke('cancel_job', { payload: { db_url: dbUrl, id } }),
  listJobs: (dbUrl, limit = 100) => invoke('list_jobs', { payload: { db_url: dbUrl, limit } }),
  // { workers: [{ alive, device, … }], models: [{ model, kind, is_default }] }
  workerStatus: (dbUrl) => invoke('worker_status', { payload: { db_url: dbUrl } }),
  // Synchronous encode on the worker's priority lane: { halfvec } or { similarities }.
  encodeQuery: (dbUrl, query, sentences = null) =>
    invoke('encode_query', { payload: { db_url: dbUrl, query, sentences } }),

  openExternal: (url) => open(url),
};
