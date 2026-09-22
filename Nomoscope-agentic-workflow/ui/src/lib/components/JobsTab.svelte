<script>
  // Jobs: what the worker is doing and has done (ops.jobs), the worker's own
  // heartbeat and the models it serves. Everything the UI triggers is a row
  // here, so this is also where an analyst sees why their run is waiting
  // (one worker, one job at a time — a translation batch ahead of it).
  import { api } from '../api.js';
  import { TERMINAL } from '../jobs.js';

  let { dbUrl = '', active = true } = $props();

  let jobs = $state([]);
  let currentUser = $state('');
  let worker = $state(null); // { workers: [...], models: [...] }
  let error = $state('');
  let selectedId = $state(null);
  let events = $state([]);
  let lastEventId = $state(0);
  let logEl = $state(null);

  const selected = $derived(jobs.find((j) => j.id === selectedId) ?? null);
  const alive = $derived((worker?.workers ?? []).filter((w) => w.alive));
  const llmModels = $derived((worker?.models ?? []).filter((m) => m.kind === 'llm'));

  async function refresh() {
    if (!dbUrl) return;
    try {
      const [list, status] = await Promise.all([api.listJobs(dbUrl, 200), api.workerStatus(dbUrl)]);
      jobs = list.jobs;
      currentUser = list.current_user;
      worker = status;
      error = '';
    } catch (e) {
      error = String(e);
    }
    if (selectedId != null) await tail();
  }

  // Poll while the tab is on screen; a hidden tab costs nothing.
  $effect(() => {
    if (!active || !dbUrl) return;
    refresh();
    const timer = setInterval(refresh, 5000);
    return () => clearInterval(timer);
  });

  export function reload() {
    return refresh();
  }

  async function select(job) {
    if (selectedId === job.id) return;
    selectedId = job.id;
    events = [];
    lastEventId = 0;
    await tail();
  }

  // Tail the selected job's events by last-seen id (same cursor as jobs.js).
  async function tail() {
    if (selectedId == null) return;
    try {
      const res = await api.jobEvents(dbUrl, selectedId, lastEventId);
      const fresh = (res.events ?? []).filter((e) => e.id > lastEventId);
      if (fresh.length) {
        events = [...events, ...fresh];
        lastEventId = fresh[fresh.length - 1].id;
      }
    } catch (e) {
      error = String(e);
    }
  }

  $effect(() => {
    events.length;
    if (active && logEl) logEl.scrollTop = logEl.scrollHeight;
  });

  async function cancel(job) {
    try {
      await api.cancelJob(dbUrl, job.id);
      await refresh();
    } catch (e) {
      error = String(e);
    }
  }

  const canCancel = (job) => !TERMINAL.has(job.status) && !job.cancel_requested && job.submitted_by === currentUser;

  function fmtTime(t) {
    return t ? t.replace('T', ' ').slice(0, 19) : '—';
  }

  function duration(job) {
    if (!job.started_at) return '';
    const end = job.finished_at ? Date.parse(job.finished_at) : Date.now();
    const s = Math.max(0, Math.round((end - Date.parse(job.started_at)) / 1000));
    if (s < 60) return `${s}s`;
    const m = Math.floor(s / 60);
    return m < 60 ? `${m}m ${String(s % 60).padStart(2, '0')}s` : `${Math.floor(m / 60)}h ${String(m % 60).padStart(2, '0')}m`;
  }

  function progressText(job) {
    const p = job.progress;
    if (!p) return '';
    if (p.total > 0) return `${p.done}/${p.total}`;
    return p.detail ?? '';
  }

  function payloadSummary(job) {
    const p = job.payload ?? {};
    switch (job.job_type) {
      case 'workflow':
        return `${(p.targets ?? []).length} target(s) · ${p.year ?? '?'}${p.model ? ` · ${p.model}` : ''}${p.force ? ' · force' : ''}`;
      case 'ingest':
        return `${p.command} ${(p.args ?? []).slice(0, 2).join(' ')}`;
      case 'embed':
        return `model ${p.model_id} · batch ${p.batch_size}${p.limit ? ` · limit ${p.limit}` : ''}${p.dry_run ? ' · dry run' : ''}`;
      case 'translate':
        return `${p.model} → ${p.target_lang}${p.limit ? ` · limit ${p.limit}` : ''}${p.dry_run ? ' · dry run' : ''}`;
      case 'encode':
        return `"${String(p.query ?? '').slice(0, 40)}"${p.sentences ? ` · ${p.sentences.length} sentences` : ''}`;
      case 'eval':
        return p.resume ? `resume ${p.resume}` : `${p.as_of} · ${p.model}`;
      case 'impact':
        return `${p.project || 'all projects'} · ${p.zone || 'EEE'}`;
      default:
        return JSON.stringify(p).slice(0, 60);
    }
  }
</script>

<section class="panel jobs">
  <div class="worker">
    {#if !worker}
      <span class="muted">Reading worker status…</span>
    {:else if alive.length === 0}
      <span class="badge fail">no worker alive</span>
      <span class="muted">
        Jobs will wait in the queue until a worker starts
        {#if worker.workers.length}(last heartbeat {fmtTime(worker.workers[0].heartbeat_at)}){/if}.
      </span>
    {:else}
      {#each alive as w (w.worker_id)}
        <span class="badge pass">worker alive</span>
        <span class="mono">{w.hostname}</span>
        <span class="muted">· {w.device ?? 'device ?'} · {w.version ?? ''}</span>
        {#if w.current_job_id}<span class="muted">· running job #{w.current_job_id}</span>{/if}
      {/each}
    {/if}
    {#if llmModels.length}
      <span class="muted">· models: {llmModels.map((m) => m.model + (m.is_default ? ' (default)' : '')).join(', ')}</span>
    {/if}
    <div class="spacer"></div>
    <button onclick={refresh}>Refresh</button>
  </div>

  {#if error}<p class="error">{error}</p>{/if}

  <div class="split">
    <div class="tablebox">
      <table>
        <thead>
          <tr><th>#</th><th>Type</th><th>Status</th><th>What</th><th>By</th><th>Submitted</th><th>Took</th><th>Progress</th><th></th></tr>
        </thead>
        <tbody>
          {#each jobs as job (job.id)}
            <tr class:selected={job.id === selectedId} onclick={() => select(job)}>
              <td class="mono">{job.id}</td>
              <td>{job.job_type}</td>
              <td>
                <span class="badge {job.status}">{job.status}</span>
                {#if job.cancel_requested && !TERMINAL.has(job.status)}<span class="muted small">cancelling…</span>{/if}
              </td>
              <td class="small">{payloadSummary(job)}</td>
              <td class="mono small">{job.submitted_by}</td>
              <td class="mono small">{fmtTime(job.submitted_at)}</td>
              <td class="small">{duration(job)}</td>
              <td class="small">{progressText(job)}</td>
              <td onclick={(e) => e.stopPropagation()}>
                {#if canCancel(job)}
                  <button class="link" onclick={() => cancel(job)}>Cancel</button>
                {/if}
              </td>
            </tr>
          {:else}
            <tr><td colspan="9" class="muted">No jobs yet — every run from the Ingest and Parameters tabs shows up here.</td></tr>
          {/each}
        </tbody>
      </table>
    </div>

    <div class="detail">
      {#if !selected}
        <p class="muted">Select a job to tail its output.</p>
      {:else}
        <p>
          <strong>#{selected.id} {selected.job_type}</strong>
          <span class="badge {selected.status}">{selected.status}</span>
          <span class="muted small">{payloadSummary(selected)}</span>
        </p>
        {#if selected.error}<pre class="err">{selected.error}</pre>{/if}
        {#if selected.result}
          <details>
            <summary>result</summary>
            <pre>{JSON.stringify(selected.result, null, 2)}</pre>
          </details>
        {/if}
        <div class="log" bind:this={logEl}>
          {#each events as e (e.id)}
            <div class="line {e.stream}"><span class="mono">{e.line}</span></div>
          {:else}
            <div class="muted">No output yet.</div>
          {/each}
        </div>
      {/if}
    </div>
  </div>
</section>

<style>
  .jobs { display: flex; flex-direction: column; gap: 0.6rem; min-height: 0; overflow: hidden; }
  .worker { display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap; }
  .spacer { flex: 1; }
  .error { color: var(--err); margin: 0; }
  .split { display: grid; grid-template-columns: 3fr 2fr; gap: 0.7rem; flex: 1; min-height: 0; }
  .split > * { min-height: 0; }
  .tablebox { overflow: auto; border: 1px solid var(--border); border-radius: 8px; }
  table { width: 100%; border-collapse: collapse; }
  thead th { position: sticky; top: 0; background: var(--panel-2); text-align: left; padding: 0.4rem 0.6rem; z-index: 1; }
  tbody td { padding: 0.3rem 0.6rem; border-top: 1px solid var(--border); vertical-align: top; }
  tbody tr { cursor: pointer; }
  tbody tr:hover { background: var(--panel-2); }
  tbody tr.selected { background: var(--accent-soft); }
  .small { font-size: 0.8rem; }
  .badge.queued { background: var(--panel-2); color: var(--muted); }
  .badge.running { background: var(--accent-soft); color: var(--accent); }
  .badge.succeeded { background: var(--ok-soft); color: var(--ok); }
  .badge.failed, .badge.cancelled { background: var(--err-soft); color: var(--err); }
  button.link { background: none; border: none; color: var(--accent); cursor: pointer; padding: 0; font-size: 0.85rem; }
  .detail { display: flex; flex-direction: column; gap: 0.4rem; overflow: hidden; }
  .detail p { margin: 0; display: flex; gap: 0.5rem; align-items: baseline; flex-wrap: wrap; }
  pre { margin: 0; white-space: pre-wrap; word-break: break-word; font-size: 0.8rem; max-height: 10rem; overflow: auto; }
  pre.err { color: var(--err); }
  .log {
    flex: 1;
    min-height: 8rem;
    overflow: auto;
    background: var(--panel-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.5rem 0.7rem;
    font-size: 0.85rem;
    line-height: 1.4;
  }
  .log .line { white-space: pre-wrap; word-break: break-word; }
  .log .line.stderr .mono { color: var(--err); }
  .log .line.system .mono { color: var(--accent); }
</style>
