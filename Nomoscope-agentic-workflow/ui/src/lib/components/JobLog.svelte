<script>
  // A job's log lines (ops.job_events: stdout, stderr, system), kept scrolled
  // to the newest. `folded` puts it behind a "Technical log" disclosure, as
  // pages show it to reviewers; the Jobs page shows it open, filling its pane.
  //
  // `active`: a page kept mounted while hidden has no layout, so the scroll
  // is redone when it is shown again.
  let { lines = [], jobId = null, active = true, folded = false, fill = false, empty = '' } = $props();

  let box = $state(null);

  $effect(() => {
    lines.length;
    if (active && box) box.scrollTop = box.scrollHeight;
  });
</script>

{#snippet logBox()}
  <div class="joblog" class:fill bind:this={box}>
    {#each lines as line, i (line.id ?? `i${i}`)}
      <div class="line {line.stream}"><span class="mono">{line.line}</span></div>
    {:else}
      {#if empty}<div class="muted">{empty}</div>{/if}
    {/each}
  </div>
{/snippet}

{#if folded}
  {#if lines.length}
    <details class="more">
      <summary>Technical log <span class="hint">{jobId != null ? `job #${jobId} · ` : ''}{lines.length} lines</span></summary>
      <div class="body">{@render logBox()}</div>
    </details>
  {/if}
{:else}
  {@render logBox()}
{/if}

<style>
  .joblog {
    max-height: 16rem;
    min-height: 4rem;
    overflow: auto;
    background: var(--panel-2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.6rem 0.8rem;
    font-size: 0.85rem;
    line-height: 1.4;
  }
  .joblog.fill { flex: 1; max-height: none; min-height: 8rem; }
  .line { white-space: pre-wrap; word-break: break-word; }
  .line.stderr .mono { color: var(--err); }
  .line.system .mono { color: var(--accent); }
</style>
