<script>
  // The progress of a job run (lib/jobRun.svelte.js): a bar — determinate
  // once the job reports a total, indeterminate before — and one status line.
  // A run that has printed nothing for a minute says so: a hang then looks
  // different from a slow step.
  import { formatDuration } from '@shared/lib/format.js';

  let { run } = $props();

  const STALE_MS = 60_000;
  const stale = $derived(run.running && run.silent > STALE_MS);
</script>

{#if run.running || run.progress}
  <div class="progress">
    {#if run.pct != null}
      <div class="bar"><div class="fill" style="width: {run.pct}%"></div></div>
    {:else}
      <div class="bar indeterminate"><div class="fill"></div></div>
    {/if}
    <div class="status small" class:stale>
      {#if run.progress?.total > 0}
        {run.progress.done} of {run.progress.total} done ({run.pct}%)
        {#if run.progress.failed}<span class="failed"> · {run.progress.failed} failed</span>{/if}
        {#if run.progress.current} · now: <span class="mono">{run.progress.current}</span>{/if}
        {#if run.progress.detail} · {run.progress.detail}{/if}
      {:else}
        {run.note || 'Starting…'}
      {/if}
      {#if stale} · no news for {formatDuration(run.silent)}{/if}
    </div>
  </div>
{/if}

<style>
  .progress { display: flex; flex-direction: column; gap: 0.3rem; }
  .bar { height: 8px; background: var(--panel-2); border-radius: 999px; overflow: hidden; }
  .fill { height: 100%; background: var(--focus); transition: width 0.3s ease; }
  .indeterminate .fill { width: 30%; animation: bar-slide 1.2s ease-in-out infinite; }
  @keyframes bar-slide { from { margin-left: -30%; } to { margin-left: 100%; } }
  .status { color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .status.stale { color: var(--err); }
  .failed { color: var(--err); }
</style>
