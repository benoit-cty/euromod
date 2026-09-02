<script>
  let { items, facets, selectedId, onselect } = $props();

  let sectionEl = $state(null);
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

  // Move the selection by `delta` rows (the rows as displayed, so collapsed
  // groups count once). With nothing selected yet, enter the list from the end
  // the reviewer is arrowing towards.
  function move(delta) {
    if (!rows.length) return;
    const current = rows.findIndex((row) => row.runs.some((r) => r.id === selectedId));
    const next =
      current === -1
        ? delta > 0
          ? 0
          : rows.length - 1
        : Math.min(rows.length - 1, Math.max(0, current + delta));
    const id = shown(rows[next]).id;
    if (id !== selectedId) onselect(id);
  }

  // Arrow keys walk the queue. Bound on the window rather than on a focusable
  // row so the reviewer can key straight through the list without clicking one
  // first — but only while this list is on screen, and never when the focus is
  // somewhere that owns its arrow keys (a filter dropdown, the detail panel's
  // fields, a scrollable evidence pane).
  function onkeydown(event) {
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    if (!sectionEl || sectionEl.offsetParent === null) return;
    const active = document.activeElement;
    if (active && active !== document.body) {
      // Buttons ignore arrow keys anyway, so "Accept, then arrow to the next
      // item" keeps working with the focus left in the detail panel.
      const passive = active.tagName === 'BUTTON';
      if (!passive && !sectionEl.contains(active)) return;
      // The search box is fine (up/down do nothing there); a <select> is not.
      if (active.matches('select')) return;
    }
    if (event.key === 'ArrowDown') move(1);
    else if (event.key === 'ArrowUp') move(-1);
    else if (event.key === 'PageDown') move(10);
    else if (event.key === 'PageUp') move(-10);
    else if (event.key === 'Home') move(-rows.length);
    else if (event.key === 'End') move(rows.length);
    else return;
    event.preventDefault();
  }

  // Keep the selected row visible when the selection moved by key rather than
  // by click; 'nearest' is a no-op when the row is already in view.
  $effect(() => {
    selectedId;
    rows;
    sectionEl?.querySelector('tr.selected')?.scrollIntoView({ block: 'nearest' });
  });
</script>

<svelte:window {onkeydown} />

<section class="panel queue" bind:this={sectionEl}>
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
  /* The selected row doubles as the keyboard cursor, so it needs to read as
     more than the hover highlight it otherwise shares. */
  tbody tr.selected td:first-child { box-shadow: inset 2px 0 0 var(--accent); }
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
