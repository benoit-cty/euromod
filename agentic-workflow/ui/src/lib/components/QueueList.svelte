<script>
  let { items, facets, selectedId, onselect } = $props();

  let search = $state('');
  let country = $state('');
  let routing = $state('');
  let status = $state('');

  const filtered = $derived(
    items.filter((item) => {
      if (country && item.country !== country) return false;
      if (routing && item.routing !== routing) return false;
      if (status && item.status !== status) return false;
      if (search) {
        const needle = search.toLowerCase();
        const haystack = `${item.model_target} ${item.label ?? ''} ${item.id}`.toLowerCase();
        if (!haystack.includes(needle)) return false;
      }
      return true;
    })
  );

  function confidence(item) {
    const c = item.proposed_value?.lineage?.confidence;
    return c == null ? '—' : c.toFixed(2);
  }
</script>

<section class="panel queue">
  <div class="filters">
    <input placeholder="Search parameter…" bind:value={search} />
    <select bind:value={country}>
      <option value="">country</option>
      {#each facets?.countries ?? [] as c}<option value={c}>{c}</option>{/each}
    </select>
    <select bind:value={routing}>
      <option value="">routing</option>
      {#each facets?.routings ?? [] as r}<option value={r}>{r}</option>{/each}
    </select>
    <select bind:value={status}>
      <option value="">status</option>
      {#each facets?.statuses ?? [] as s}<option value={s}>{s}</option>{/each}
    </select>
  </div>
  <p class="muted">{filtered.length} / {items.length} items</p>
  <div class="scroll">
    <table>
      <thead>
        <tr><th>Parameter</th><th>as of</th><th>Routing</th><th>Critique</th><th>Conf.</th><th>Status</th></tr>
      </thead>
      <tbody>
        {#each filtered as item (item.id)}
          <tr
            class="selectable"
            class:selected={item.id === selectedId}
            onclick={() => onselect(item.id)}
          >
            <td>
              <div>{item.label ?? item.model_target}</div>
              <div class="muted mono">{item.country} · {item.model_target}</div>
            </td>
            <td>{item.as_of}</td>
            <td><span class="badge {item.routing}">{item.routing}</span></td>
            <td>
              {#if item.critique}
                <span class="badge {item.critique.verdict}">{item.critique.verdict}</span>
              {:else}—{/if}
            </td>
            <td>{confidence(item)}</td>
            <td><span class="badge {item.status}">{item.status}</span></td>
          </tr>
        {:else}
          <tr><td colspan="6" class="muted">Queue is empty — run the pipeline first.</td></tr>
        {/each}
      </tbody>
    </table>
  </div>
</section>

<style>
  .queue { display: flex; flex-direction: column; min-height: 0; }
  .filters { display: flex; gap: 0.4rem; flex-wrap: wrap; }
  .filters input { flex: 1; min-width: 10rem; }
  .scroll { overflow: auto; flex: 1; }
  p { margin: 0.4rem 0; }
</style>
