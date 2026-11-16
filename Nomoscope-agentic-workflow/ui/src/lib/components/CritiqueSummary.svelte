<script>
  // What the critique step's mechanical checks said about a proposal, in
  // plain words; "note: …" issues are the critique explaining a rule it
  // applied, not a problem.
  import Icon from '@shared/components/Icon.svelte';
  import { verdictLabel } from '@shared/lib/labels.js';

  let { item } = $props();
</script>

{#if item.critique && item.routing !== 'not_found'}
  {@const failed = [
    !item.critique.schema_valid && 'the proposal is not well-formed',
    !item.critique.citation_verified && 'the quote is not found word-for-word in the cited text',
    !item.critique.dates_consistent && 'the dates do not fit the year',
    !item.critique.values_sane && 'the value looks implausible',
  ].filter(Boolean)}
  <div
    class="checks-line"
    class:bad={item.critique.verdict !== 'pass'}
    title="{verdictLabel(item.critique.verdict).hint} ({item.critique.verdict})"
  >
    {#if item.critique.verdict === 'pass' && !failed.length}
      <Icon name="check" size={16} /> All automatic checks passed
    {:else}
      <Icon name="alert" size={16} />
      Automatic checks: {failed.length ? failed.join('; ') : 'see the issues below'}
    {/if}
  </div>
  {#if item.critique.issues.length}
    <!-- "note: …" lines are the critique explaining a rule it applied, not a problem -->
    <ul class="issues">
      {#each item.critique.issues as issue}
        {@const isNote = /^note:/i.test(issue)}
        <li class:note={isNote}>{isNote ? `Note: ${issue.replace(/^note:\s*/i, '')}` : issue}</li>
      {/each}
    </ul>
  {/if}
{/if}

<style>
  .checks-line { display: flex; align-items: center; gap: 0.45rem; color: var(--ok); font-weight: 600; font-size: 0.92rem; }
  .checks-line.bad { color: var(--warn); }
  .issues { color: var(--err); margin: -0.4rem 0 0; font-size: 0.9rem; }
  .issues li.note { color: var(--muted); }
</style>
