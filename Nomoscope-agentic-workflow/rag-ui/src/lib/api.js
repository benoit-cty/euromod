// Single seam between the Svelte frontend and the Rust commands (ADR 0004:
// every call is a database round trip; anything needing a model or the
// internet is a job in ops.jobs that the worker runs). The database URL lives
// on the Rust side: no call carries it.
import { invoke } from '@tauri-apps/api/core';
import { open } from '@tauri-apps/plugin-shell';

const payload = (fields) => ({ payload: fields });

export const api = {
  getEnvConfig: () => invoke('get_env_config'),
  // { workers: [{ alive, … }], models: [{ model, kind, is_default }] }
  workerStatus: () => invoke('worker_status'),
  submitJob: (jobType, body, priority = 0) => invoke('submit_job', payload({ job_type: jobType, payload: body, priority })),
  jobStatus: (id) => invoke('job_status', payload({ id })),
  jobEvents: (id, after = 0) => invoke('job_events', payload({ id, after })),
  cancelJob: (id) => invoke('cancel_job', payload({ id })),
  // Chat history = the caller's own `chat` jobs, grouped by conversation_id.
  listConversations: (limit = 40) => invoke('list_conversations', payload({ limit })),
  conversationTurns: (conversationId) => invoke('conversation_turns', payload({ conversation_id: conversationId })),
  // Every language rendering of the version a chunk belongs to.
  chunkRenderings: (chunkId) => invoke('chunk_renderings', payload({ chunk_id: chunkId })),
  // Direct search, no LLM: { results, notice } (notice = fell back to full text).
  searchArticles: (payload) => invoke('search_articles', { payload }),
  openExternal: (url) => open(url),
};
