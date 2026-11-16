// Single seam between the RAG chat's Svelte frontend and its Rust commands:
// the commands both apps share (@shared/lib/api.js) plus the chat's own
// (ADR 0004: every call is a database round trip; anything needing a model
// or the internet is a job in ops.jobs that the worker runs). The database
// URL lives on the Rust side: no call carries it.
import { invoke } from '@tauri-apps/api/core';
import { open } from '@tauri-apps/plugin-shell';
import { createApi } from '@shared/lib/api.js';
import { bindJobs } from '@shared/lib/jobs.js';
import { worker } from '@shared/lib/worker.svelte.js';

const shared = createApi(invoke, open);
const { call } = shared;

export const api = {
  ...shared,
  // Chat history = the caller's own `chat` jobs, grouped by conversation_id.
  listConversations: (limit = 40) => call('list_conversations', { limit }),
  conversationTurns: (conversationId) => call('conversation_turns', { conversation_id: conversationId }),
};

// A chat turn is short: poll a little faster than the review UI's batches.
export const { followJob, submitAndFollow } = bindJobs(api, 800);

// The one worker status the chat reads (polled by the shell).
worker.use(api.workerStatus);
export { worker };
