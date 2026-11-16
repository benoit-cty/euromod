// Single seam between the review UI's Svelte frontend and its Rust commands:
// the commands both apps share (@shared/lib/api.js) plus the review UI's own.
//
// The UI is remote (ADR 0004): every call here is a database round trip. Work
// that needs a model or the internet is a job (submitJob → ops.jobs) the
// worker runs; submitAndFollow / followJob follow one to completion. The
// database URL lives on the Rust side (Tauri state): no call carries it, and
// setDbUrl is the one way to point the whole app at another database.
import { invoke } from '@tauri-apps/api/core';
import { open } from '@tauri-apps/plugin-shell';
import { createApi } from '@shared/lib/api.js';
import { bindJobs } from '@shared/lib/jobs.js';
import { worker } from '@shared/lib/worker.svelte.js';

const shared = createApi(invoke, open);
const { call } = shared;

export const api = {
  ...shared,
  // Checked before it is taken: resolves { db_url, reviewer } or rejects and
  // changes nothing. A masked password (as getEnvConfig shows it) keeps the current one.
  setDbUrl: (dbUrl) => call('set_db_url', { db_url: dbUrl }),
  // Review queue (params.review_queue) and decisions (params.decide_review_item).
  loadQueue: () => call('load_queue'),
  saveDecision: (payload) => call('save_decision', payload),
  loadDecisions: (limit = 200) => call('load_decisions', { limit }),
  // The EUROMOD change set — metadata edits and accepted value changes only —
  // one file per country, into a folder the reviewer picks: { count, paths, canceled }.
  exportChanges: () => call('export_changes'),
  // Metadata edits (params.edit_parameter, ADR 0005): unit, source_type or a
  // {lang: text} field. Resolves { id } (null = already the store's value).
  editParameter: (modelTarget, field, value, note = null) =>
    call('edit_parameter', { model_target: modelTarget, field, value, note }),
  parameterEdits: (modelTarget) => call('parameter_edits', { model_target: modelTarget }),
  // A parameter's EUROMOD texts, law-language texts and value history (every
  // member for a `group:` target), for the review page's hand-off prompt.
  parameterContext: (modelTarget) => call('parameter_context', { model_target: modelTarget }),
  dbStats: () => call('db_stats'),
  // Cosine of each sentence against the query (one BGE-M3 batch on the
  // worker), so the Database tab can tint the sentence of a hit that most
  // likely answers.
  scoreSentences: (query, sentences) => call('score_sentences', { query, sentences }),
  // Contributed documents: the instruments a document can be said to implement
  // (title or national-id fragment, `context` instruments excluded).
  searchInstruments: (country, query, limit = 20) => call('search_instruments', { country, query, limit }),
  // Golden set: drafted evaluation cases (eval.golden_cases) and the reviewer's verdict.
  goldenCases: () => call('golden_cases'),
  setGoldenVerified: ({ id, verified, note }) => call('set_golden_verified', { id, verified, note }),
  evalRuns: () => call('eval_runs'),
  evalRunDetail: (runPk) => call('eval_run_detail', { run_pk: runPk }),
  // Parameters tab: params-schema listing and Phoenix trace-link resolution.
  paramsList: () => call('params_list'),
  phoenixProjects: () => call('phoenix_projects'),
  listJobs: (limit = 100) => call('list_jobs', { limit }),
};

export const { followJob, submitAndFollow } = bindJobs(api);

// The one worker status every page reads (polled by the shell).
worker.use(api.workerStatus);
export { worker };
