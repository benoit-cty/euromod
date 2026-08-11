<script>
  let { items, facets, selectedId, onselect } = $props();

  let search = $state('');
  let country = $state('');
  let routing = $state('');
  let status = $state('');
  // The same parameter is re-run for several system years / as-of dates, so the
  // raw queue shows near-duplicate rows. Collapsed (default) = one row per
  // parameter, the newest run; the older ones stay reachable from the detail
  // panel's run switcher.
  let collapse = $state(true);

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

  // `items` arrives newest-first, so the first run seen per parameter is the
  // latest. Grouping happens *after* filtering: a status filter narrows the runs
  // a group is made of, so the count never promises rows the filter hides.
  const rows = $derived.by(() => {
    if (!collapse) return filtered.map((item) => ({ key: item.id, runs: [item] }));
    const groups = new Map();
    for (const item of filtered) {
      const key = `${item.country}|${item.model_target}`;
      const group = groups.get(key);
      if (group) group.runs.push(item);
      else groups.set(key, { key, runs: [item] });
    }
    return [...groups.values()];
  });

  // Show the run the reviewer is actually looking at, so the row and the detail
  // panel never disagree; otherwise the newest one.
  function shown(row) {
    return row.runs.find((r) => r.id === selectedId) ?? row.runs[0];
  }

  function confidence(item) {
    const c = item.proposed_value?.lineage?.confidence;
    return c == null ? '—' : c.toFixed(2);
  }

  function year(item) {
    return item.system_year ?? item.as_of?.slice(0, 4) ?? '—';
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
  <div class="summary">
    <p class="muted">
      {rows.length}
      {collapse ? 'parameter(s)' : 'item(s)'} · {filtered.length} / {items.length} runs
    </p>
    <label class="inline muted">
      <input type="checkbox" bind:checked={collapse} />
      one row per parameter
    </label>
  </div>
  <div class="scroll">
    <table>
      <thead>
        <tr><th>Parameter</th><th>Year</th><th>Routing</th><th>Critique</th><th>Conf.</th><th>Status</th></tr>
      </thead>
      <tbody>
        {#each rows as row (row.key)}
          {@const item = shown(row)}
          <tr
            class="selectable"
            class:selected={item.id === selectedId}
            onclick={() => onselect(item.id)}
          >
            <td>
              <div>
                {item.label ?? item.model_target}
                {#if row.runs.length > 1}
                  <span class="runs" title="{row.runs.length} runs of this parameter — switch between them in the detail panel">
                    {row.runs.indexOf(item) + 1}/{row.runs.length} runs
                  </span>
                {/if}
              </div>
              <div class="muted mono">{item.country} · {item.model_target}</div>
            </td>
            <td>
              {year(item)}
              <div class="muted mono">{item.as_of}</div>
            </td>
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
  .summary { display: flex; align-items: center; justify-content: space-between; gap: 0.6rem; }
  .inline { display: flex; align-items: center; gap: 0.3rem; font-size: 0.85rem; white-space: nowrap; }
  .runs {
    margin-left: 0.35rem;
    padding: 0.05rem 0.35rem;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--panel-2);
    color: var(--muted);
    font-size: 0.7rem;
    white-space: nowrap;
  }
</style>
