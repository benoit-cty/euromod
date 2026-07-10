<script>
  import { api } from '../api.js';

  let { dbUrl = '' } = $props();

  let url = $state(''); // seeded from dbUrl by the $effect below once config loads
  let runs = $state(null);
  let error = $state('');
  let loading = $state(false);

  let selectedPk = $state(null);
  let detail = $state(null);
  let detailError = $state('');
  let detailLoading = $state(false);
  let failuresOnly = $state(false);

  const selectedRun = $derived(runs?.find((r) => r.id === selectedPk) ?? null);

  const KPIS = [
    { key: 'routing_pct', label: 'routing' },
    { key: 'value_pct', label: 'value' },
    { key: 'date_pct', label: 'date' },
    { key: 'citation_pct', label: 'citation' },
    { key: 'supportedness_pct', label: 'supportedness' },
    { key: 'hallucination_pct', label: 'hallucination', invert: true },
    { key: 'retrieval_recall_pct', label: 'retrieval recall' },
  ];

  $effect(() => {
    if (dbUrl && !url) url = dbUrl;
  });

  $effect(() => {
    if (url && !runs && !loading && !error) loadRuns();
  });

  async function loadRuns() {
    loading = true;
    error = '';
    try {
      runs = (await api.evalRuns(url)).runs;
      if (selectedPk && !runs.some((r) => r.id === selectedPk)) {
        selectedPk = null;
        detail = null;
      }
    } catch (e) {
      error = String(e);
      runs = null;
    } finally {
      loading = false;
    }
  }

  async function selectRun(pk) {
    selectedPk = pk;
    detail = null;
    detailError = '';
    detailLoading = true;
    try {
      detail = await api.evalRunDetail(url, pk);
    } catch (e) {
      detailError = String(e);
    } finally {
      detailLoading = false;
    }
  }

  function pct(v) {
    return v == null ? '—' : `${v.toFixed(1)}%`;
  }

  function ms(v) {
    return v == null ? '—' : `${Math.round(v)} ms`;
  }

  function caseFailed(c) {
    return (
      c.error != null ||
      c.hallucination ||
      [c.routing_correct, c.value_correct, c.date_correct, c.citation_correct, c.supportedness, c.retrieval_hit].some(
        (v) => v === false
      )
    );
  }

  const visibleCases = $derived(
    (detail?.cases ?? []).filter((c) => !failuresOnly || caseFailed(c))
  );
</script>

{#snippet mark(v)}
  {#if v === true}<span class="tick ok">✓</span>
  {:else if v === false}<span class="tick bad">✗</span>
  {:else}<span class="muted">—</span>{/if}
{/snippet}

<section class="panel eval">
  <div class="row">
    <label class="grow">
      Database URL
      <input bind:value={url} class="mono" />
    </label>
    <button onclick={loadRuns} disabled={loading}>{loading ? 'Loading…' : 'Refresh runs'}</button>
  </div>

  {#if error}<p class="error">{error}</p>{/if}

  {#if runs}
    <h2>Evaluation runs</h2>
    {#if runs.length === 0}
      <p class="muted">No evaluation runs yet — run <span class="mono">euromod-eval run</span> first.</p>
    {:else}
      <table class="runs">
        <thead>
          <tr>
            <th>Run</th><th>Created</th><th>As of</th><th>Model</th><th>Prompt</th><th>Agent</th>
            <th>Countries</th><th>Cases</th><th>Err</th>
            {#each KPIS as k}<th>{k.label}</th>{/each}
            <th>Latency</th>
          </tr>
        </thead>
        <tbody>
          {#each runs as run (run.id)}
            <tr class:selected={run.id === selectedPk} onclick={() => selectRun(run.id)}>
              <td class="mono" title={run.notes ?? run.run_id}>{run.run_id}</td>
              <td class="muted">{run.created_at.slice(0, 16)}</td>
              <td>{run.as_of}</td>
              <td><strong>{run.model_provider}/{run.model_name}</strong></td>
              <td class="mono">{run.prompt_version}</td>
              <td class="mono">{run.agent_version}</td>
              <td>{run.countries.join(' ')}</td>
              <td>{run.cases}</td>
              <td>{#if run.errors > 0}<span class="badge fail">{run.errors}</span>{:else}0{/if}</td>
              {#each KPIS as k}<td>{pct(run[k.key])}</td>{/each}
              <td>{ms(run.avg_latency_ms)}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  {/if}

  {#if selectedRun}
    <h2>
      Run <span class="mono">{selectedRun.run_id}</span>
      <span class="muted">
        {selectedRun.model_provider}/{selectedRun.model_name} · prompt {selectedRun.prompt_version} ·
        agent {selectedRun.agent_version} · dataset {selectedRun.dataset_version}
        {#if selectedRun.git_commit}· {selectedRun.git_commit.slice(0, 8)}{/if}
      </span>
    </h2>
    {#if selectedRun.notes}<p class="muted">{selectedRun.notes}</p>{/if}

    {#if detailError}<p class="error">{detailError}</p>{/if}
    {#if detailLoading}<p class="muted">Loading run detail…</p>{/if}

    {#if detail}
      <div class="cards">
        {#each KPIS as k}
          {@const v = selectedRun[k.key]}
          <div class="card" class:bad={v != null && (k.invert ? v > 0 : v < 100)}>
            <div class="num">{pct(v)}</div>
            <div class="muted">{k.label}{k.invert ? ' (want 0)' : ''}</div>
          </div>
        {/each}
        <div class="card">
          <div class="num">{ms(selectedRun.avg_latency_ms)}</div>
          <div class="muted">avg latency</div>
        </div>
      </div>

      <h3>By language / country</h3>
      <table>
        <thead>
          <tr>
            <th>Lang</th><th>Country</th><th>Cases</th><th>Err</th>
            {#each KPIS as k}<th>{k.label}</th>{/each}
            <th>Latency</th>
          </tr>
        </thead>
        <tbody>
          {#each detail.summary as row}
            <tr>
              <td><strong>{row.language}</strong></td>
              <td>{row.country}</td>
              <td>{row.cases}</td>
              <td>{row.errors}</td>
              {#each KPIS as k}<td>{pct(row[k.key])}</td>{/each}
              <td>{ms(row.avg_latency_ms)}</td>
            </tr>
          {/each}
        </tbody>
      </table>

      <h3>
        Cases
        <label class="inline">
          <input type="checkbox" bind:checked={failuresOnly} />
          failures only ({detail.cases.filter(caseFailed).length}/{detail.cases.length})
        </label>
      </h3>
      {#each visibleCases as c (c.case_id)}
        <details>
          <summary>
            <strong class="mono">{c.case_id}</strong>
            <span class="badge {caseFailed(c) ? 'fail' : 'pass'}">{caseFailed(c) ? 'fail' : 'pass'}</span>
            <span class="muted">
              {c.country} · {c.language}
              {#if c.difficulty}· {c.difficulty}{/if}
              {#if c.source_class}· {c.source_class}{/if}
            </span>
            <span class="kpi-marks">
              routing {@render mark(c.routing_correct)}
              value {@render mark(c.value_correct)}
              date {@render mark(c.date_correct)}
              citation {@render mark(c.citation_correct)}
              supported {@render mark(c.supportedness)}
              retrieval {@render mark(c.retrieval_hit)}
              {#if c.hallucination}<span class="badge fail">hallucination</span>{/if}
            </span>
          </summary>
          <div class="case-body">
            <p class="muted">
              routing: expected <strong>{c.routing_expected}</strong> →
              actual <strong>{c.routing_actual ?? '—'}</strong>
              {#if c.model_target}· target <span class="mono">{c.model_target}</span>{/if}
              {#if c.confidence != null}· confidence {c.confidence.toFixed(2)}{/if}
              {#if c.latency_ms != null}· {c.latency_ms} ms{/if}
            </p>
            {#if c.error}<p class="error mono">{c.error}</p>{/if}
            {#if c.details}<pre class="mono">{JSON.stringify(c.details, null, 2)}</pre>{/if}
          </div>
        </details>
      {:else}
        <p class="muted">No {failuresOnly ? 'failing ' : ''}cases.</p>
      {/each}
    {/if}
  {/if}
</section>

<style>
  .eval { overflow: auto; display: flex; flex-direction: column; gap: 0.8rem; min-height: 0; }
  .row { display: flex; gap: 0.5rem; align-items: end; flex-wrap: wrap; }
  .grow { flex: 1; min-width: 16rem; }
  label { display: flex; flex-direction: column; gap: 0.25rem; color: var(--muted); }
  label input { width: 100%; }
  label.inline { display: inline-flex; flex-direction: row; align-items: center; gap: 0.35rem;
    font-size: 0.8rem; font-weight: 400; margin-left: 0.8rem; }
  label.inline input { width: auto; }
  .error { color: var(--err); }
  .runs tbody tr { cursor: pointer; }
  .runs tbody tr:hover { background: var(--panel-2); }
  .runs tbody tr.selected { background: var(--accent-soft); }
  .cards { display: flex; gap: 0.6rem; flex-wrap: wrap; }
  .card {
    background: var(--panel-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    min-width: 7.5rem;
  }
  .card.bad { border-color: var(--err); }
  .num { font-size: 1.4rem; font-weight: 700; }
  .tick.ok { color: var(--ok); }
  .tick.bad { color: var(--err); font-weight: 700; }
  .kpi-marks { display: inline-flex; gap: 0.5rem; align-items: baseline; color: var(--muted); font-size: 0.85em; }
  details { border-top: 1px solid var(--border); padding: 0.5rem 0; }
  summary { cursor: pointer; display: flex; gap: 0.5rem; align-items: baseline; flex-wrap: wrap; }
  .case-body { padding: 0.4rem 0 0 1rem; }
  pre { background: var(--panel-2); border: 1px solid var(--border); border-radius: 8px;
    padding: 0.6rem; overflow: auto; max-height: 24rem; white-space: pre-wrap; }
</style>
