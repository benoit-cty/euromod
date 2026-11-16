// What the worker status says, read the same way by every page: is a worker
// alive, which language models it publishes (ops.worker_models), and which
// one a picker should show. Pure functions; worker.svelte.js polls.

/** true / false once a status is in; null before (unknown). */
export function anyAlive(status) {
  if (!status) return null;
  return (status.workers ?? []).some((w) => w.alive);
}

/** The language models the worker publishes, default first as it lists them. */
export function llmModels(status) {
  return (status?.models ?? []).filter((m) => m.kind === 'llm');
}

/**
 * The model a picker should hold once the list is known. A model is never
 * typed (a free-text model string is how a wrong deployment went unnoticed
 * for a month): a value not in the list is replaced. With `allowDefault`, ''
 * stands for the worker's own default (the job then carries `model: null`)
 * and is what a vanished choice falls back to; without it, the published
 * default (else the first) is picked.
 */
export function pickModel(models, current, { allowDefault = false } = {}) {
  if (current && models.some((m) => m.model === current)) return current;
  if (allowDefault) return '';
  return (models.find((m) => m.is_default) ?? models[0])?.model ?? '';
}
