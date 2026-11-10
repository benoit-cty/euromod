<script>
  // Parameters tab: browse every EUROMOD parameter in the params DB, filter,
  // select some, submit a `workflow` job for them (the worker runs
  // run-targets), then jump to the review-queue item or open the run's trace
  // in Phoenix. The expanded row edits the parameter's metadata (ParameterEditor).
  import { api } from '../api.js';
  import ParameterEditor from './ParameterEditor.svelte';
  import { submitAndFollow, summarize } from '../jobs.js';
  import { countryName, routingLabel, humanize } from '../labels.js';
  import Icon from './Icon.svelte';

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
  // One run verifies ONE EUROMOD system year, and only the years the export
  // actually defines (FR J2.19: 2006-2025). Never default to today's date: a
  // run anchored on a year EUROMOD has no system for compares the proposal
  // against the newest value on file, so every parameter comes back `changed`
  // on no evidence. Null until the params list loads and supplies the years.
  let systemYears = $state({}); // country -> [year, …] ascending
  let systemYear = $state(null);
  // The model is picked from the list the worker publishes; '' = the worker's
  // default (the job carries `model: null`). Never free text (see llm.py).
  let models = $state([]);
  let model = $state('');
  let workerAlive = $state(null);
  let force = $state(false);

  // --- run state ---
  let running = $state(false);
  let jobId = $state(null);
  let logLines = $state([]);
  let summary = $state('');
  let logEl = $state(null);
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

  // Years offered = those defined for every country in the run. Selecting
  // across countries intersects them, so the run can never be anchored on a
  // year one of those countries has no system for.
  const runCountries = $derived.by(() => {
    const byTarget = new Map(params.map((p) => [p.model_target, p.country]));
    const picked = selectedTargets.map((t) => byTarget.get(t)).filter(Boolean);
    return [...new Set(picked.length ? picked : filtered.map((p) => p.country))];
  });

  const availableYears = $derived.by(() => {
    const lists = runCountries.map((c) => systemYears[c]).filter(Boolean);
    if (!lists.length) return [];
    const common = lists.reduce((acc, years) => acc.filter((y) => years.includes(y)));
    return [...common].sort((a, b) => b - a); // newest first
  });

  // Keep the choice valid as the selection changes: fall back to the newest
  // year the current countries share rather than silently keeping a stale one.
  $effect(() => {
    if (availableYears.length && !availableYears.includes(systemYear)) {
      systemYear = availableYears[0];
    }
  });

  async function refresh() {
    if (!dbUrl) return;
    loading = true;
    try {
      const res = await api.paramsList(dbUrl);
      params = res.parameters;
      systemYears = res.system_years ?? {};
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
    try {
      const status = await api.workerStatus(dbUrl);
      workerAlive = (status.workers ?? []).some((w) => w.alive);
      models = (status.models ?? []).filter((m) => m.kind === 'llm');
      if (model && !models.some((m) => m.model === model)) model = '';
    } catch {
      models = [];
    }
  }

  $effect(() => {
    if (dbUrl) refresh();
  });

  // Target of the shell's Reload button while this tab is showing.
  export function reload() {
    return refresh();
  }

  const handlers = {
    onSubmit: (id) => {
      jobId = id;
      logLines = [...logLines, { stream: 'system', line: `job #${id} submitted` }];
    },
    onLine: (e) => {
      lastLogAt = Date.now();
      trackProgress(e.line);
      logLines = [...logLines, e];
    },
    onProgress: (data) => {
      lastLogAt = Date.now();
      if (data && data.total > 0) progress = { ...(progress ?? {}), ...data };
    },
  };

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
    if (!targets.length || running || !systemYear) return;
    const payload = { targets, year: Number(systemYear), model: model || null, force: Boolean(force) };
    jobId = null;
    logLines = workerAlive === false
      ? [{ stream: 'system', line: 'no worker alive — the job waits in the queue until one starts' }]
      : [];
    progress = null;
    summary = '';
    error = '';
    running = true;
    startedAt = lastLogAt = now = Date.now();
    try {
      const final = await submitAndFollow(dbUrl, 'workflow', payload, handlers);
      const took = fmtDur(Date.now() - startedAt);
      let line;
      if (final.status === 'succeeded') {
        const n = final.result?.item_ids?.length ?? targets.length;
        summary = `Finished: ${n} parameter(s) processed in ${took}.`;
        line = `✓ finished (${took})`;
        if (progress) progress = { ...progress, done: progress.total, current: '', detail: 'done' };
      } else {
        summary = summarize(final, took);
        line = `✗ ${summary}`;
      }
      logLines = [...logLines, { stream: final.status === 'succeeded' ? 'system' : 'stderr', line }];
    } catch (e) {
      error = String(e.message ?? e);
    } finally {
      running = false;
      await refresh();
    }
  }

  async function stop() {
    if (jobId != null) await api.cancelJob(dbUrl, jobId);
  }
</script>
<section class="panel params">
  <div class="row filters">
    <input class="grow search" bind:value={search} placeholder="Search by name, label or description…" />
    <select bind:value={country} onchange={() => (policy = '')} title="Country">
      <option value="">All countries</option>
      {#each countries as c (c)}<option value={c}>{countryName(c)}</option>{/each}
    </select>
    <select bind:value={runState} title="Last check by the assistant">
      <option value="">Any check status</option>
      <option value="never">Never checked</option>
      <option value="ran">Checked at least once</option>
      <option value="changed">Change proposed</option>
      <option value="not_found">Not found</option>
      <option value="provisional">Needs newer law</option>
      <option value="derived">Calculated</option>
      <option value="pass">Checks passed</option>
      <option value="fail">Checks failed</option>
    </select>
    <details class="morefilters">
      <summary>More filters{policy || group ? ' •' : ''}</summary>
      <div class="morefilters-body">
        <label class="field">
          Policy
          <select bind:value={policy}>
            <option value="">all</option>
            {#each policies as p (p)}<option value={p}>{p}</option>{/each}
          </select>
        </label>
        <label class="field">
          Schedule / group
          <select bind:value={group}>
            <option value="">all</option>
            {#each groups as g (g.id)}<option value={g.id}>{g.id} ({g.kind})</option>{/each}
          </select>
        </label>
      </div>
    </details>
  </div>

  {#if error}<p class="callout err">{error}</p>{/if}

  <div class="tablebox">
    <table>
      <thead>
        <tr>
          <th class="pick"><input class="bigcheck" type="checkbox" checked={allFilteredSelected} onchange={toggleAll} title="Select all shown" /></th>
          <th>Parameter</th>
          <th>Value in EUROMOD</th>
          <th>Last check</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {#each filtered as p (p.model_target)}
          <tr
            class:expandedrow={expanded === p.model_target}
            class:picked={!!selected[p.model_target]}
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
            <td>
              <div class="pname">
                {p.label ?? p.name ?? p.model_target}
                {#if p.edit_count}<span class="badge new" title="Corrected in this app: part of the next EUROMOD export">corrected</span>{/if}
                {#if group}
                  {@const m = membership(p, group)}
                  <span class="badge">band {m.index}{m.role ? ` · ${humanize(m.role)}` : ''}</span>
                {/if}
              </div>
              <div class="muted small">
                {countryName(p.country)}{#if p.label}{' · '}<span class="mono">{p.name ?? p.model_target}</span>{/if}
              </div>
            </td>
            <td>
              <span class="mono">{fmtValue(p)}</span>
              {#if p.unit}<span class="muted small"> {p.unit}</span>{/if}
              {#if p.current_valid_from}<div class="muted small">since {p.current_valid_from}</div>{/if}
            </td>
            <td>
              {#if p.last_run_id}
                {@const r = routingLabel(p.last_routing)}
                <span class="badge {p.last_routing}" title={r.hint}>{r.label}</span>
                {#if p.last_verdict === 'fail'}<span class="flag" title="The automatic checks found a problem">⚠</span>{/if}
                <div class="muted small">for {p.last_as_of?.slice(0, 4) ?? '—'}</div>
              {:else}
                <span class="muted">Never checked</span>
              {/if}
            </td>
            <td class="actions" onclick={(e) => e.stopPropagation()}>
              {#if p.last_item_id && onopenitem}
                <button class="link" title="Open in Review" onclick={() => onopenitem(p.last_item_id)}>
                  Review →
                </button>
              {/if}
            </td>
          </tr>
          {#if expanded === p.model_target}
            <tr class="detail">
              <td></td>
              <td colspan="4">
                {#if p.description}<p>{p.description}</p>{/if}
                <dl class="facts">
                  <dt>Identifier</dt><dd class="mono">{p.model_target}</dd>
                  {#if p.policy}<dt>Policy</dt><dd class="mono">{p.policy}</dd>{/if}
                  <dt>Type</dt><dd>{p.value_type}{p.unit ? ` · ${p.unit}` : ''}</dd>
                  {#if p.category}<dt>Classification</dt><dd>{p.category}</dd>{/if}
                  {#if p.groups?.length}
                    <dt>Groups</dt>
                    <dd>{p.groups.map((g) => `${g.id} (${g.kind}, band ${g.index}${g.role ? ` · ${g.role}` : ''})`).join(', ')}</dd>
                  {/if}
                  {#if p.current_source_type === 'national_team'}
                    <dt>Source</dt><dd>National team: not checked against legislation</dd>
                  {/if}
                  {#if p.last_run_id}
                    <dt>Last check</dt>
                    <dd>
                      {p.last_model}{#if p.last_finished_at} · {p.last_finished_at}{/if}
                      {#if p.last_trace_id}
                        · <button class="link" title="Open the agent trace in Phoenix" onclick={() => api.openExternal(traceUrl(p))}>trace ↗</button>
                      {/if}
                    </dd>
                  {/if}
                </dl>
                <ParameterEditor {dbUrl} param={p} onsaved={refresh} />
              </td>
            </tr>
          {/if}
        {:else}
          <tr>
            <td colspan="5">
              <div class="empty-state">
                {#if loading}
                  <span><span class="spinner"></span> Loading parameters…</span>
                {:else if params.length}
                  <span class="big">No parameter matches</span>
                  <span>Try clearing the search or filters.</span>
                {:else}
                  <span class="big">No parameters loaded</span>
                  <span>Run <code>nomoscope-workflow ingest-params</code> first.</span>
                {/if}
              </div>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>

  <div class="runbar" class:active={selectedTargets.length || running}>
    <span class="count">
      {#if selectedTargets.length}
        <strong>{selectedTargets.length}</strong> selected
        <button class="link" onclick={() => (selected = {})} disabled={running}>clear</button>
      {:else}
        <span class="muted">{filtered.length} of {params.length} shown. Tick parameters to check them.</span>
      {/if}
    </span>
    <div class="spacer"></div>
    {#if workerAlive === false}
      <span class="badge fail" title="No worker heartbeat: the check will wait until one starts">worker offline</span>
    {/if}
    <label class="field inline">
      Year
      <select bind:value={systemYear} disabled={!availableYears.length}>
        {#each availableYears as year}
          <option value={year}>{year}</option>
        {/each}
      </select>
    </label>
    <details class="runopts">
      <summary title="Model and overwrite options">Options</summary>
      <div class="runopts-body">
        <label class="field">
          Language model
          <select bind:value={model} class="mono">
            <option value="">Default</option>
            {#each models as m (m.model)}
              <option value={m.model}>{m.model}{m.is_default ? ' (default)' : ''}</option>
            {/each}
          </select>
        </label>
        <label class="field check">
          <input type="checkbox" bind:checked={force} />
          Re-check items already reviewed
        </label>
      </div>
    </details>
    {#if running}
      <button onclick={stop} disabled={jobId == null}>Cancel</button>
    {/if}
    <button class="primary" onclick={runSelected} disabled={running || !selectedTargets.length || !systemYear}>
      {#if running}<span class="spinner light"></span> Checking… {fmtDur(now - startedAt)}
      {:else}<Icon name="sparkle" size={16} /> Check with the assistant{/if}
    </button>
  </div>

  {#if running || progress || summary}
    <div class="progressbox">
      {#if running || progress}
        {#if progress}
          <div class="bar"><div class="fill" style="width: {pct}%"></div></div>
        {:else}
          <div class="bar indeterminate"><div class="fill"></div></div>
        {/if}
        <div class="pstatus small" class:stale={running && now - lastLogAt > 60000}>
          {#if progress}
            {progress.done} of {progress.total} done
            {#if progress.current} · now: <span class="mono">{progress.current}</span>{/if}
          {:else}
            Starting…
          {/if}
          {#if running && now - lastLogAt > 60000} · no news for {fmtDur(now - lastLogAt)}{/if}
        </div>
      {/if}
      {#if summary}
        <p class="small">{summary} {#if !running}Results are in <button class="link" onclick={() => onopenitem?.(null)}>Review</button>.{/if}</p>
      {/if}
      {#if logLines.length}
        <details class="more">
          <summary>Technical log <span class="hint">{jobId != null ? `job #${jobId} · ` : ''}{logLines.length} lines</span></summary>
          <div class="body">
            <div class="joblog" bind:this={logEl}>
              {#each logLines as l, i (i)}
                <div class="line {l.stream}"><span class="mono">{l.line}</span></div>
              {/each}
            </div>
          </div>
        </details>
      {/if}
    </div>
  {/if}
</section>

<style>
  .params { display: flex; flex-direction: column; gap: 0.8rem; min-height: 0; overflow: hidden; }
  .row { display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; }
  .grow { flex: 1; min-width: 14rem; }
  .spacer { flex: 1; }
  .morefilters > summary, .runopts > summary { cursor: pointer; color: var(--accent); font-size: 0.9rem; white-space: nowrap; }
  .morefilters { position: relative; }
  .morefilters-body, .runopts-body {
    position: absolute;
    z-index: 5;
    margin-top: 0.4rem;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    box-shadow: 0 8px 24px rgba(16, 24, 40, 0.12);
    padding: 0.8rem;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    min-width: 18rem;
  }
  .morefilters-body { right: 0; }
  .runopts { position: relative; }
  .runopts-body { bottom: 2.2rem; right: 0; }
  .tablebox { flex: 1; min-height: 10rem; overflow: auto; border: 1px solid var(--border); border-radius: 10px; }
  thead th { background: var(--panel-2); z-index: 1; }
  tbody td { vertical-align: top; }
  /* wide, easy-to-hit selection column */
  th.pick, td.pick { width: 2.8rem; text-align: center; padding-left: 0.3rem; padding-right: 0.3rem; }
  input.bigcheck { width: 1.25rem; height: 1.25rem; margin: 0; cursor: pointer; accent-color: var(--accent); }
  tbody tr { cursor: pointer; }
  tbody tr:hover td { background: var(--panel-2); }
  tbody tr.picked td { background: var(--accent-soft); }
  tbody tr.detail, tbody tr.detail td, tbody tr.detail:hover td { cursor: default; background: var(--panel); }
  tr.expandedrow td { border-bottom: none; }
  tr.detail td { padding-top: 0; }
  tr.detail p { margin: 0.2rem 0 0.5rem; }
  .pname { font-weight: 600; display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap; }
  .flag { color: var(--warn); margin-left: 0.2rem; }
  .facts { display: grid; grid-template-columns: auto 1fr; gap: 0.2rem 0.9rem; margin: 0 0 0.6rem; font-size: 0.88rem; }
  .facts dt { color: var(--muted); }
  .facts dd { margin: 0; }
  .actions { white-space: nowrap; text-align: right; }
  .runbar {
    display: flex;
    gap: 0.7rem;
    align-items: center;
    flex-wrap: wrap;
    padding: 0.6rem 0.8rem;
    border-radius: 10px;
    background: var(--panel-2);
  }
  .runbar.active { background: var(--accent-soft); }
  .inline { flex-direction: row; align-items: center; gap: 0.4rem; }
  .inline select { width: auto; }
  .count { display: inline-flex; gap: 0.5rem; align-items: center; }
  .progressbox { display: flex; flex-direction: column; gap: 0.4rem; }
  .pstatus { color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .pstatus.stale { color: var(--err); }
  .spinner.light { border-color: var(--border-strong); border-top-color: var(--text-bright); }
</style>
