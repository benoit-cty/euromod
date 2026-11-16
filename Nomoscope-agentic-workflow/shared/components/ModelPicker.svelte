<script>
  // The language model a job runs with, picked from the list the worker
  // publishes (ops.worker_models) and nothing else. With `allowDefault` the
  // first option is the worker's own default ('' → the job carries
  // `model: null`); otherwise the published default is preselected. A choice
  // the worker stops publishing is replaced (models.js pickModel).
  import { pickModel } from '../lib/models.js';

  let {
    models = [],
    value = $bindable(''),
    allowDefault = false,
    // shown when the worker publishes no model (and there is no default option)
    emptyText = 'no model available',
    disabled = false,
    class: className = '',
  } = $props();

  $effect(() => {
    const next = pickModel(models, value, { allowDefault });
    if (next !== value) value = next;
  });
</script>

<select bind:value class={className} disabled={disabled || (!allowDefault && !models.length)}>
  {#if allowDefault}<option value="">Default</option>{/if}
  {#each models as m (m.model)}
    <option value={m.model}>{m.model}{m.is_default ? ' (default)' : ''}</option>
  {:else}
    {#if !allowDefault}<option value="">{emptyText}</option>{/if}
  {/each}
</select>
