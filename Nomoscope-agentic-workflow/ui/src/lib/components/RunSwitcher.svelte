<script>
  // The other system years of the parameter on the review page. The queue
  // keeps one item per (parameter, year) run; the list shows only the newest,
  // so the other runs are reachable from here.
  import { routingLabel, statusLabel } from '@shared/lib/labels.js';

  // siblings: every queue run of the same parameter, newest first (item included)
  let { item, siblings = [], onselectrun = () => {} } = $props();

  const runIndex = $derived(siblings.findIndex((r) => r.id === item?.id));

  function runLabel(run) {
    return run.system_year ?? run.as_of?.slice(0, 4) ?? '—';
  }

  function stepRun(delta) {
    const next = siblings[runIndex + delta];
    if (next) onselectrun(next.id);
  }
</script>

{#if siblings.length > 1}
  <div class="runs">
    <span class="muted">Other years</span>
    <button class="step ghost" disabled={runIndex <= 0} title="Newer" onclick={() => stepRun(-1)}>‹</button>
    <div class="run-chips">
      {#each siblings as run (run.id)}
        <button
          class="chip"
          class:current={run.id === item.id}
          title="{routingLabel(run.routing).label} · {statusLabel(run.status).label}"
          onclick={() => onselectrun(run.id)}
        >
          <span class="year">{runLabel(run)}</span>
          {#if run.status !== 'pending'}<span class="badge {run.status}">{statusLabel(run.status).label}</span>{/if}
        </button>
      {/each}
    </div>
    <button
      class="step ghost"
      disabled={runIndex < 0 || runIndex >= siblings.length - 1}
      title="Older"
      onclick={() => stepRun(1)}>›</button
    >
  </div>
{/if}

<style>
  .runs { display: flex; align-items: center; gap: 0.4rem; font-size: 0.85rem; min-width: 0; }
  .run-chips { display: flex; gap: 0.3rem; overflow-x: auto; padding-bottom: 0.15rem; }
  .runs .chip {
    gap: 0.35rem;
    padding: 0.15rem 0.55rem;
    border-radius: 999px;
    background: var(--panel-2);
    border-color: transparent;
    color: var(--muted);
    white-space: nowrap;
  }
  .runs .chip.current { border-color: var(--accent); color: var(--text); background: var(--accent-soft); }
  .runs .chip .year { font-variant-numeric: tabular-nums; }
  .runs .step { padding: 0.05rem 0.45rem; }
</style>
