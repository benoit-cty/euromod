<script>
  // Parameters tab: browse every EUROMOD parameter in the params DB, filter,
  // select some, launch the agentic workflow on them (run-targets), then jump
  // to the review-queue item or open the run's trace in Phoenix.
  import { onMount } from 'svelte';
  import { api } from '../api.js';

  let { dbUrl = '', phoenixEndpoint = 'http://localhost:6006', onopenitem = null } = $props();

  let params = $state([]);
  let gids = $state({}); // phoenix project name -> GraphQL gid (for trace deep-links)
  let loading = $state(false);
  let error = $state('');

  // --- filters ---
  let country = $state('');
  let policy = $state('');
  let group = $state(''); // parameter-group id, e.g. 'FR:ConstDef_fr:tsc_schedule_2'
  let runState = $state(''); // '' | never | ran | changed | not_found | pass | fail
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
      logLines = [...logLines, payload];
    });
    return () => unlisten.then((un) => un());
  });

  // Auto-scroll the log as lines arrive.
  $effect(() => {
    logLines.length;
    if (logEl) logEl.scrollTop = logEl.scrollHeight;
  });

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
    summary = '';
    error = '';
    running = true;
    try {
      const res = await api.runWorkflow({ run_id: runId, args, db_url: dbUrl || null });
      if (res.canceled) summary = 'Canceled.';
      else if (res.success) summary = `Finished: ${targets.length} parameter(s) processed.`;
      else summary = `Exited with code ${res.code ?? '?'}.`;
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
      {running ? 'Running…' : `Run agentic update (${selectedTargets.length})`}
    </button>
    <button onclick={stop} disabled={!running}>Stop</button>
  </div>

  {#if error}<p class="error">{error}</p>{/if}
  {#if summary}<p class="muted">{summary}</p>{/if}

  <div class="tablebox">
    <table>
      <thead>
        <tr>
          <th><input type="checkbox" checked={allFilteredSelected} onchange={toggleAll} title="select all filtered" /></th>
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
            <td onclick={(e) => e.stopPropagation()}>
              <input
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
