<script>
  // Parameters tab: browse every EUROMOD parameter in the params DB, filter,
  // select some, launch the agentic workflow on them (run-targets), then jump
  // to the review-queue item or open the run's trace in Phoenix.
  import { onMount } from 'svelte';
  import { api } from '../api.js';

  // The component stays mounted (hidden) while other tabs are shown, so a
  // launched run keeps streaming; `active` re-triggers the log auto-scroll on
  // return and `onrunning` lets the shell show a run indicator on the tab.
  let {
    dbUrl = '',
    phoenixEndpoint = 'http://localhost:6006',
    onopenitem = null,
    active = true,
    onrunning = null,
  } = $props();

  let params = $state([]);
  let gids = $state({}); // phoenix project name -> GraphQL gid (for trace deep-links)
  let loading = $state(false);
  let error = $state('');

  // --- filters ---
  let country = $state('');
  let policy = $state('');
  let group = $state(''); // parameter-group id, e.g. 'FR:ConstDef_fr:tsc_schedule_2'
  let runState = $state(''); // '' | never | ran | changed | not_found | derived | pass | fail
  let search = $state('');

  // --- selection (model_target -> true) ---
  let selected = $state({});
  let expanded = $state(null);

  // --- run form ---
  let asOf = $state(new Date().toISOString().slice(0, 10));
  let model = $state('');
  let force = $state(false);

  // --- run state ---
  let running = $state(false);
  let runId = $state('');
  let logLines = $state([]);
  let summary = $state('');
  let logEl;
  // Liveness: when the run started, when the child last wrote a line, and a
  // 1 s clock so both ages tick while the pipeline is silent (model loads,
  // LLM calls) — a hang then looks different from a slow step.
  let startedAt = $state(0);
  let lastLogAt = $state(0);
  let now = $state(0);

  // --- progress state ---
  // Same bar as the Ingest tab, but fed from the workflow CLI's own console
  // output instead of `@progress` JSON: `run` prints "[i/N] file.json" per
  // parameter, tracing prints "  › step" / the final "…: routing=…" line.
  // Before the first parameter (readiness banner, model load) there is no
  // total yet, so the bar runs indeterminate like a no-total ingest run.
  const HEAD_RE = /^\[(\d+)\/(\d+)\]\s*(.*)$/;
  const STEP_RE = /^\s+›\s+(.+)$/;
  const ROUTED_RE = /\brouting=(\S+)/;
  let progress = $state(null); // { done, total, current, detail }
  let pct = $derived(
    progress ? (progress.total > 0 ? Math.min(100, Math.round((progress.done / progress.total) * 100)) : 100) : 0
  );

  function trackProgress(line) {
    const head = line.match(HEAD_RE);
    if (head) {
      // The parameter is starting: done counts the ones already finished.
      progress = { done: Number(head[1]) - 1, total: Number(head[2]), current: head[3], detail: '' };
      return;
    }
    if (!progress) return;
    const step = line.match(STEP_RE);
    if (step) {
      progress = { ...progress, detail: step[1] };
      return;
    }
    const routed = line.match(ROUTED_RE);
    if (routed) {
      progress = {
        ...progress,
        done: Math.min(progress.done + 1, progress.total),
        detail: routed[1],
      };
    }
  }

  const countries = $derived([...new Set(params.map((p) => p.country))].sort());
  const policies = $derived(
    [...new Set(params.filter((p) => !country || p.country === country).map((p) => p.policy).filter(Boolean))].sort()
  );
  // Parameter groups (bracket_schedule, rate_table, …) seen on the loaded rows.
  const groups = $derived.by(() => {
    const kinds = new Map();
    for (const p of params) {
      if (country && p.country !== country) continue;
      for (const g of p.groups ?? []) kinds.set(g.id, g.kind);
    }
    return [...kinds.entries()].map(([id, kind]) => ({ id, kind })).sort((a, b) => a.id.localeCompare(b.id));
  });

  function membership(p, gid) {
    return (p.groups ?? []).find((g) => g.id === gid);
  }

  const filtered = $derived.by(() => {
    const q = search.trim().toLowerCase();
    const rows = params.filter((p) => {
      if (country && p.country !== country) return false;
      if (policy && p.policy !== policy) return false;
      if (group && !membership(p, group)) return false;
      if (runState === 'never' && p.last_run_id) return false;
      if (runState === 'ran' && !p.last_run_id) return false;
      if (runState === 'changed' && p.last_routing !== 'changed') return false;
      if (runState === 'not_found' && p.last_routing !== 'not_found') return false;
      if (runState === 'provisional' && p.last_routing !== 'provisional') return false;
      if (runState === 'derived' && p.last_routing !== 'derived') return false;
      if (runState === 'pass' && p.last_verdict !== 'pass') return false;
      if (runState === 'fail' && p.last_verdict !== 'fail') return false;
      if (q) {
        const hay = `${p.model_target} ${p.name ?? ''} ${p.label ?? ''} ${p.description ?? ''}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });
    if (group) {
      // Band order: thresholds and rates of the same band next to each other.
      const roleRank = { lower_threshold: 0, upper_threshold: 1, rate: 2, amount: 3 };
      rows.sort((a, b) => {
        const ma = membership(a, group);
        const mb = membership(b, group);
        return (ma.index ?? 0) - (mb.index ?? 0) || (roleRank[ma.role] ?? 9) - (roleRank[mb.role] ?? 9);
      });
    }
    return rows;
  });

  const selectedTargets = $derived(Object.keys(selected).filter((t) => selected[t]));
  const allFilteredSelected = $derived(
    filtered.length > 0 && filtered.every((p) => selected[p.model_target])
  );

  async function refresh() {
    if (!dbUrl) return;
    loading = true;
    try {
      const res = await api.paramsList(dbUrl);
      params = res.parameters;
      error = '';
    } catch (e) {
      error = String(e);
    } finally {
      loading = false;
    }
    try {
      const res = await api.phoenixProjects(dbUrl);
      gids = Object.fromEntries(res.projects.map((p) => [p.name, p.gid]));
    } catch {
      gids = {}; // Phoenix links degrade to the projects page
    }
  }

  $effect(() => {
    if (dbUrl) refresh();
  });

  onMount(() => {
    const unlisten = api.onWorkflowLog((payload) => {
      if (payload.run_id !== runId) return;
      lastLogAt = Date.now();
      trackProgress(payload.line);
      logLines = [...logLines, payload];
    });
    return () => unlisten.then((un) => un());
  });

  // Auto-scroll the log as lines arrive — and when the tab is shown again
  // (while hidden the pane has no layout, so scrollHeight was 0).
  $effect(() => {
    logLines.length;
    if (active && logEl) logEl.scrollTop = logEl.scrollHeight;
  });

  $effect(() => {
    onrunning?.(running);
  });

  $effect(() => {
    if (!running) return;
    const timer = setInterval(() => (now = Date.now()), 1000);
    return () => clearInterval(timer);
  });

  function fmtDur(ms) {
    const s = Math.max(0, Math.round(ms / 1000));
    if (s < 60) return `${s}s`;
    const m = Math.floor(s / 60);
    if (m < 60) return `${m}m ${String(s % 60).padStart(2, '0')}s`;
    return `${Math.floor(m / 60)}h ${String(m % 60).padStart(2, '0')}m`;
  }

  function toggleAll() {
    const next = { ...selected };
    if (allFilteredSelected) filtered.forEach((p) => delete next[p.model_target]);
    else filtered.forEach((p) => (next[p.model_target] = true));
    selected = next;
  }

  function toggle(target) {
    selected = { ...selected, [target]: !selected[target] };
  }

  function traceUrl(p) {
    if (!p.last_trace_id) return null;
    const gid = gids[p.last_phoenix_project];
    return gid
      ? `${phoenixEndpoint}/projects/${gid}/traces/${p.last_trace_id}`
      : `${phoenixEndpoint}/projects`;
  }

  function fmtValue(p) {
    if (p.current_raw) return p.current_raw;
    const v = p.current_value;
    if (v === null || v === undefined) return '—';
    if (Array.isArray(v)) return `${v.length} brackets`;
    return String(v);
  }

  async function runSelected() {
    const targets = selectedTargets;
    if (!targets.length || running) return;
    const args = ['run-targets', ...targets, '--as-of', asOf];
    if (model.trim()) args.push('--model', model.trim());
    if (force) args.push('--force');
    runId = crypto.randomUUID();
    logLines = [];
    progress = null;
    summary = '';
    error = '';
    running = true;
    startedAt = lastLogAt = now = Date.now();
    try {
      const res = await api.runWorkflow({ run_id: runId, args, db_url: dbUrl || null });
      const took = fmtDur(Date.now() - startedAt);
      let line;
      if (res.canceled) {
        summary = `Canceled after ${took}.`;
        line = `✗ canceled after ${took}`;
      } else if (res.success) {
        summary = `Finished: ${targets.length} parameter(s) processed in ${took}.`;
        line = `✓ finished (exit 0, ${took})`;
        if (progress) progress = { ...progress, done: progress.total, current: '', detail: 'done' };
      } else {
        summary = `Exited with code ${res.code ?? '?'} after ${took}.`;
        line = `✗ exited with code ${res.code ?? '?'} after ${took}`;
      }
      logLines = [...logLines, { run_id: runId, stream: res.success ? 'system' : 'stderr', line }];
    } catch (e) {
      error = String(e);
    } finally {
      running = false;
      await refresh();
    }
  }

  async function stop() {
    if (runId) await api.stopWorkflow(runId);
  }
</script>

<section class="panel params">
  <div class="row filters">
    <label>
      Country
      <select bind:value={country} onchange={() => (policy = '')}>
        <option value="">all</option>
        {#each countries as c (c)}<option value={c}>{c}</option>{/each}
      </select>
    </label>
    <label>
      Policy
      <select bind:value={policy}>
        <option value="">all</option>
        {#each policies as p (p)}<option value={p}>{p}</option>{/each}
      </select>
    </label>
    <label>
      Group
      <select bind:value={group}>
        <option value="">all</option>
        {#each groups as g (g.id)}<option value={g.id}>{g.id} ({g.kind})</option>{/each}
      </select>
    </label>
    <label>
      Agent runs
      <select bind:value={runState}>
        <option value="">all</option>
        <option value="never">never run</option>
        <option value="ran">has a run</option>
        <option value="changed">routing: changed</option>
        <option value="not_found">routing: not found</option>
        <option value="provisional">routing: provisional</option>
        <option value="derived">routing: derived</option>
        <option value="pass">critique: pass</option>
        <option value="fail">critique: fail</option>
      </select>
    </label>
    <label class="grow">
      Search
      <input bind:value={search} placeholder="name, label, description, model_target…" />
    </label>
    <button onclick={refresh} disabled={loading}>{loading ? 'Loading…' : 'Reload'}</button>
  </div>

  <div class="row runbar">
    <span class="muted count">
      {filtered.length} of {params.length} shown · {selectedTargets.length} selected
    </span>
    <div class="spacer"></div>
    <label>
      As of
      <input type="date" bind:value={asOf} />
    </label>
    <label>
      Model
      <input bind:value={model} placeholder="default (WORKFLOW_MODEL)" class="mono" size="24" />
    </label>
    <label class="check">
      <input type="checkbox" bind:checked={force} />
      Force (overwrite reviewed)
    </label>
    <button class="primary" onclick={runSelected} disabled={running || !selectedTargets.length}>
      {running ? `Running… ${fmtDur(now - startedAt)}` : `Run agentic update (${selectedTargets.length})`}
    </button>
    <button onclick={stop} disabled={!running}>Stop</button>
  </div>

  {#if error}<p class="error">{error}</p>{/if}
  {#if summary}<p class="muted">{summary}</p>{/if}

  <div class="tablebox">
    <table>
      <thead>
        <tr>
          <th class="pick"><input class="bigcheck" type="checkbox" checked={allFilteredSelected} onchange={toggleAll} title="select all filtered" /></th>
          <th>CC</th>
          <th>Parameter</th>
          <th>Policy</th>
          <th>Type</th>
          <th>Current value</th>
          <th>Last agent run</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {#each filtered as p (p.model_target)}
          <tr
            class:expandedrow={expanded === p.model_target}
            onclick={() => (expanded = expanded === p.model_target ? null : p.model_target)}
          >
            <td class="pick" onclick={(e) => e.stopPropagation()}>
              <input
                class="bigcheck"
                type="checkbox"
                checked={!!selected[p.model_target]}
                onchange={() => toggle(p.model_target)}
              />
            </td>
            <td>{p.country}</td>
            <td>
              <span class="mono">{p.name ?? p.model_target}</span>
              {#if group}
                {@const m = membership(p, group)}
                <span class="badge">band {m.index}{m.role ? ` · ${m.role}` : ''}</span>
              {/if}
              {#if p.label}<div class="muted small">{p.label}</div>{/if}
            </td>
            <td class="mono">{p.policy ?? '—'}</td>
            <td>
              {p.value_type}
              {#if p.unit}<span class="muted small"> · {p.unit}</span>{/if}
            </td>
            <td>
              <span class="mono">{fmtValue(p)}</span>
              {#if p.current_valid_from}<div class="muted small">since {p.current_valid_from}</div>{/if}
            </td>
            <td>
              {#if p.last_run_id}
                <span class="badge {p.last_routing}">{p.last_routing ?? '?'}</span>
                {#if p.last_verdict}<span class="badge {p.last_verdict}">{p.last_verdict}</span>{/if}
                <div class="muted small">as of {p.last_as_of} · {p.last_model}</div>
              {:else}
                <span class="muted">never</span>
              {/if}
            </td>
            <td class="actions" onclick={(e) => e.stopPropagation()}>
              {#if p.last_trace_id}
                <button
                  class="link"
                  title="Open the agent trace in Phoenix"
                  onclick={() => api.openExternal(traceUrl(p))}
                >Trace ↗</button>
              {/if}
              {#if p.last_item_id && onopenitem}
                <button class="link" title="Open in the review queue" onclick={() => onopenitem(p.last_item_id)}>
                  Review →
                </button>
              {/if}
            </td>
          </tr>
          {#if expanded === p.model_target}
            <tr class="detail">
              <td></td>
              <td colspan="7">
                <div class="mono muted">{p.model_target}</div>
                {#if p.description}<p>{p.description}</p>{/if}
                {#if p.category}<div class="muted small">classification: {p.category}</div>{/if}
                {#if p.groups?.length}
                  <div class="muted small">
                    groups: {p.groups.map((g) => `${g.id} (${g.kind}, band ${g.index}${g.role ? ` · ${g.role}` : ''})`).join(', ')}
                  </div>
                {/if}
                {#if p.current_source_type === 'national_team'}
                  <div class="muted small">national-team source — routed around the pipeline</div>
                {/if}
                {#if p.last_run_id}
                  <div class="muted small">
                    run {p.last_run_id}
                    {#if p.last_finished_at}· finished {p.last_finished_at}{/if}
                    {#if p.last_trace_id}· trace <span class="mono">{p.last_trace_id}</span>{/if}
                  </div>
                {/if}
              </td>
            </tr>
          {/if}
        {:else}
          <tr>
            <td colspan="8" class="muted empty">
              {params.length
                ? 'No parameters match the filters.'
                : 'No parameters in the DB — run `nomoscope-workflow ingest-params` first.'}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>

  {#if running || progress}
    <div class="progressbox">
      {#if progress}
        <div class="bar"><div class="fill" style="width: {pct}%"></div></div>
      {:else}
        <div class="bar indeterminate"><div class="fill"></div></div>
      {/if}
      <div class="pstatus small" class:stale={running && now - lastLogAt > 60000}>
        {#if running}<span class="spinner"></span>{/if}
        {#if progress}
          {progress.done}/{progress.total} ({pct}%)
          {#if progress.current} · <span class="mono">{progress.current}</span>{/if}
          {#if progress.detail} · {progress.detail}{/if}
        {:else}
          Starting…
        {/if}
        {#if running} · {fmtDur(now - startedAt)} · last output {fmtDur(now - lastLogAt)} ago{/if}
      </div>
    </div>
  {/if}
  {#if logLines.length || running}
    <div class="log" bind:this={logEl}>
      {#each logLines as l, i (i)}
        <div class="line {l.stream}"><span class="mono">{l.line}</span></div>
      {/each}
    </div>
  {/if}
</section>

<style>
  .params { display: flex; flex-direction: column; gap: 0.7rem; min-height: 0; overflow: hidden; }
  .row { display: flex; gap: 0.6rem; align-items: end; flex-wrap: wrap; }
  .grow { flex: 1; min-width: 14rem; }
  .spacer { flex: 1; }
  label { display: flex; flex-direction: column; gap: 0.25rem; color: var(--muted); }
  label input, label select { width: 100%; }
  label.check { flex-direction: row; align-items: center; gap: 0.4rem; }
  label.check input { width: auto; }
  .runbar { align-items: end; }
  .count { align-self: center; white-space: nowrap; }
  .error { color: var(--err); margin: 0; }
  .tablebox { flex: 1; min-height: 10rem; overflow: auto; border: 1px solid var(--border); border-radius: 8px; }
  table { width: 100%; border-collapse: collapse; }
  thead th {
    position: sticky;
    top: 0;
    background: var(--panel-2);
    text-align: left;
    padding: 0.4rem 0.6rem;
    z-index: 1;
  }
  tbody td { padding: 0.35rem 0.6rem; border-top: 1px solid var(--border); vertical-align: top; }
  /* wide, easy-to-hit selection column */
  th.pick, td.pick { width: 2.6rem; text-align: center; padding-left: 0.3rem; padding-right: 0.3rem; }
  input.bigcheck {
    width: 1.6rem;
    height: 1.6rem;
    margin: 0;
    cursor: pointer;
    accent-color: var(--accent);
  }
  tbody tr { cursor: pointer; }
  tbody tr.detail, tbody tr.detail td { cursor: default; }
  tr.expandedrow td { border-bottom: none; }
  tr.detail td { border-top: none; padding-top: 0; }
  tr.detail p { margin: 0.3rem 0; }
  .small { font-size: 0.8rem; }
  .actions { white-space: nowrap; }
  button.link {
    background: none;
    border: none;
    color: var(--accent);
    cursor: pointer;
    padding: 0 0.2rem;
    font-size: 0.85rem;
  }
  .progressbox { display: flex; flex-direction: column; gap: 0.3rem; }
  .bar {
    height: 8px;
    background: var(--panel-2);
    border: 1px solid var(--border);
    border-radius: 999px;
    overflow: hidden;
  }
  .bar .fill { height: 100%; background: var(--accent); transition: width 0.3s ease; }
  .bar.indeterminate .fill { width: 30%; animation: bar-slide 1.2s ease-in-out infinite; }
  @keyframes bar-slide {
    from { margin-left: -30%; }
    to { margin-left: 100%; }
  }
  .pstatus { color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .pstatus.stale { color: var(--err); }
  .spinner {
    display: inline-block;
    vertical-align: middle;
    margin-right: 0.2rem;
    width: 0.7rem;
    height: 0.7rem;
    border: 2px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  .log {
    max-height: 11rem;
    min-height: 4rem;
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
