// Single seam between the Svelte frontend and the Rust commands.
//
// The UI is remote (ADR 0004): every call here is a database round trip. Work
// that needs a model or the internet is a job (submitJob → ops.jobs) the
// worker runs; lib/jobs.js follows one to completion. The database URL lives
// on the Rust side (Tauri state): no call carries it, and setDbUrl is the one
// way to point the whole app at another database.
import { invoke } from '@tauri-apps/api/core';
import { open } from '@tauri-apps/plugin-shell';

export const api = {
  // { reviewer, db_error, db_url (password masked), phoenix_endpoint, phoenix_project }
  getEnvConfig: () => invoke('get_env_config'),
  // Checked before it is taken: resolves { db_url, reviewer } or rejects and
  // changes nothing. A masked password (as getEnvConfig shows it) keeps the current one.
  setDbUrl: (dbUrl) => invoke('set_db_url', { payload: { db_url: dbUrl } }),
  // Review queue (params.review_queue) and decisions (params.decide_review_item).
  loadQueue: () => invoke('load_queue'),
  saveDecision: (payload) => invoke('save_decision', { payload }),
  loadDecisions: (limit = 200) => invoke('load_decisions', { payload: { limit } }),
  // The EUROMOD change set — metadata edits and accepted value changes only —
  // one file per country, into a folder the reviewer picks: { count, paths, canceled }.
  exportChanges: () => invoke('export_changes'),
  // Metadata edits (params.edit_parameter, ADR 0005): unit, source_type or a
  // {lang: text} field. Resolves { id } (null = already the store's value).
  editParameter: (modelTarget, field, value, note = null) =>
    invoke('edit_parameter', { payload: { model_target: modelTarget, field, value, note } }),
  parameterEdits: (modelTarget) => invoke('parameter_edits', { payload: { model_target: modelTarget } }),
  // A parameter's EUROMOD texts, law-language texts and value history (every
  // member for a `group:` target), for the review page's hand-off prompt.
  parameterContext: (modelTarget) => invoke('parameter_context', { payload: { model_target: modelTarget } }),
  dbStats: () => invoke('db_stats'),
  // Vector/hybrid modes encode the query on the worker; `notice` is set when
  // no worker was alive and the search fell back to full text.
  searchArticles: (payload) => invoke('search_articles', { payload }),
  // Cosine of each sentence against the query (one BGE-M3 batch on the
  // worker), so the Database tab can tint the sentence of a hit that most
  // likely answers.
  scoreSentences: (query, sentences) => invoke('score_sentences', { payload: { query, sentences } }),
  // Contributed documents: the instruments a document can be said to implement
  // (title or national-id fragment, `context` instruments excluded).
  searchInstruments: (country, query, limit = 20) =>
    invoke('search_instruments', { payload: { country, query, limit } }),
  // Every language rendering (authentic / official / machine translation) of the
  // legal-unit version a cited chunk belongs to.
  chunkRenderings: (chunkId) => invoke('chunk_renderings', { payload: { chunk_id: chunkId } }),
  // Golden set: drafted evaluation cases (eval.golden_cases) and the reviewer's verdict.
  goldenCases: () => invoke('golden_cases'),
  setGoldenVerified: ({ id, verified, note }) => invoke('set_golden_verified', { payload: { id, verified, note } }),
  evalRuns: () => invoke('eval_runs'),
  evalRunDetail: (runPk) => invoke('eval_run_detail', { payload: { run_pk: runPk } }),
  // Parameters tab: params-schema listing and Phoenix trace-link resolution.
  paramsList: () => invoke('params_list'),
  phoenixProjects: () => invoke('phoenix_projects'),

  // --- jobs (ops.jobs): the only way the UI makes anything run ---
  submitJob: (jobType, payload, priority = 0) =>
    invoke('submit_job', { payload: { job_type: jobType, payload, priority } }),
  jobStatus: (id) => invoke('job_status', { payload: { id } }),
  jobEvents: (id, after = 0) => invoke('job_events', { payload: { id, after } }),
  cancelJob: (id) => invoke('cancel_job', { payload: { id } }),
  listJobs: (limit = 100) => invoke('list_jobs', { payload: { limit } }),
  // { workers: [{ alive, device, … }], models: [{ model, kind, is_default }] }
  workerStatus: () => invoke('worker_status'),
  openExternal: (url) => open(url),
};
