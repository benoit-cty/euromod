// The commands both desktop apps share, as one seam between Svelte and Rust.
//
// Every call is a database round trip (ADR 0004): anything that needs a model
// or the internet is a job in ops.jobs that the worker runs. The database URL
// lives on the Rust side (Tauri state), so no call carries it. `invoke` and
// `open` are passed in (Tauri's core invoke and the shell plugin's open) so
// this module imports nothing from @tauri-apps and runs under plain node.
// Each app's lib/api.js spreads this and adds its own commands.

export function createApi(invoke, open) {
  const call = (command, payload) => (payload === undefined ? invoke(command) : invoke(command, { payload }));
  return {
    call,
    // Connection settings (URL with its password masked) and the login.
    getEnvConfig: () => call('get_env_config'),
    // { workers: [{ alive, device, … }], models: [{ model, kind, is_default }] }
    workerStatus: () => call('worker_status'),
    submitJob: (jobType, payload, priority = 0) => call('submit_job', { job_type: jobType, payload, priority }),
    jobStatus: (id) => call('job_status', { id }),
    jobEvents: (id, after = 0) => call('job_events', { id, after }),
    cancelJob: (id) => call('cancel_job', { id }),
    // Direct article search, no LLM: { results, notice } (notice = no worker
    // was alive to encode the query, so the search fell back to full text).
    searchArticles: (payload) => call('search_articles', payload),
    // Every language rendering (authentic / official / machine translation)
    // of the legal-unit version a chunk belongs to.
    chunkRenderings: (chunkId) => call('chunk_renderings', { chunk_id: chunkId }),
    openExternal: (url) => open(url),
  };
}
