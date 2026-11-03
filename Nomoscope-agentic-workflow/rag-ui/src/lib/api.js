// Single seam between the Svelte frontend and the Rust commands (ADR 0004:
// every call is a database round trip; anything needing a model or the
// internet is a job in ops.jobs that the worker runs).
import { invoke } from '@tauri-apps/api/core';
import { open } from '@tauri-apps/plugin-shell';

const db = (db_url, rest = {}) => ({ payload: { db_url, ...rest } });

export const api = {
  getEnvConfig: () => invoke('get_env_config'),
  // { workers: [{ alive, … }], models: [{ model, kind, is_default }] }
  workerStatus: (dbUrl) => invoke('worker_status', db(dbUrl)),
  submitJob: (dbUrl, jobType, payload, priority = 0) =>
    invoke('submit_job', db(dbUrl, { job_type: jobType, payload, priority })),
  jobStatus: (dbUrl, id) => invoke('job_status', db(dbUrl, { id })),
  jobEvents: (dbUrl, id, after = 0) => invoke('job_events', db(dbUrl, { id, after })),
  cancelJob: (dbUrl, id) => invoke('cancel_job', db(dbUrl, { id })),
  // Chat history = the caller's own `chat` jobs, grouped by conversation_id.
  listConversations: (dbUrl, limit = 40) => invoke('list_conversations', db(dbUrl, { limit })),
  conversationTurns: (dbUrl, conversationId) =>
    invoke('conversation_turns', db(dbUrl, { conversation_id: conversationId })),
  // Every language rendering of the version a chunk belongs to.
  chunkRenderings: (dbUrl, chunkId) => invoke('chunk_renderings', db(dbUrl, { chunk_id: chunkId })),
  // Direct search, no LLM: { results, notice } (notice = fell back to full text).
  searchArticles: (payload) => invoke('search_articles', { payload }),
  openExternal: (url) => open(url),
};
