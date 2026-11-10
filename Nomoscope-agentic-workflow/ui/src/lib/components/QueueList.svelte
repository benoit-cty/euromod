<script>
  import { routingLabel, statusLabel, countryName } from '../labels.js';

  let { items, facets, selectedId, onselect } = $props();

  let sectionEl = $state(null);
  let search = $state('');
  let country = $state('');
  let routing = $state('');
  // What the list shows: the work left to do by default, so the first screen
  // is a to-do list rather than the whole history of the queue.
  let view = $state('pending'); // pending | decided | all
  // The same parameter is re-run for several system years / as-of dates, so the
  // raw queue shows near-duplicate rows. Collapsed (default) = one row per
  // parameter, the newest run; the older ones stay reachable from the detail
  // panel's run switcher.
  let collapse = $state(true);

  const counts = $derived({
    pending: items.filter((i) => i.status === 'pending').length,
    decided: items.filter((i) => i.status !== 'pending').length,
    all: items.length,
  });

  const filtered = $derived(
    items.filter((item) => {
      if (view === 'pending' && item.status !== 'pending') return false;
      if (view === 'decided' && item.status === 'pending') return false;
      if (country && item.country !== country) return false;
      if (routing && item.routing !== routing) return false;
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

  function year(item) {
    return item.system_year ?? item.as_of?.slice(0, 4) ?? '—';
  }

  // Move the selection by `delta` rows (the rows as displayed, so collapsed
  // groups count once). With nothing selected yet — or the selected item just
  // left the "To review" view because it was decided — enter the list from the
  // end the reviewer is arrowing towards.
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
    sectionEl?.querySelector('.item.selected')?.scrollIntoView({ block: 'nearest' });
  });
</script>

<svelte:window {onkeydown} />

<section class="panel queue" bind:this={sectionEl}>
  <div class="segmented views" role="tablist">
    <button class:active={view === 'pending'} onclick={() => (view = 'pending')}>
      To review <span class="count">{counts.pending}</span>
    </button>
    <button class:active={view === 'decided'} onclick={() => (view = 'decided')}>
      Decided <span class="count">{counts.decided}</span>
    </button>
    <button class:active={view === 'all'} onclick={() => (view = 'all')}>
      All <span class="count">{counts.all}</span>
    </button>
  </div>

  <div class="filters">
    <input class="search" placeholder="Search a parameter…" bind:value={search} />
    <select bind:value={country} title="Country">
      <option value="">All countries</option>
      {#each facets?.countries ?? [] as c}<option value={c}>{countryName(c)}</option>{/each}
    </select>
    <select bind:value={routing} title="What the assistant found">
      <option value="">Any outcome</option>
      {#each facets?.routings ?? [] as r}<option value={r}>{routingLabel(r).label}</option>{/each}
    </select>
  </div>

  <div class="list" role="listbox" aria-label="Review queue">
    {#each rows as row (row.key)}
      {@const item = shown(row)}
      {@const outcome = routingLabel(item.routing)}
      <button
        class="item"
        class:selected={item.id === selectedId}
        role="option"
        aria-selected={item.id === selectedId}
        onclick={() => onselect(item.id)}
      >
        <div class="item-main">
          <div class="item-title">{item.label ?? item.model_target}</div>
          <div class="item-sub muted">
            {countryName(item.country)} · {year(item)}
            {#if row.runs.length > 1}
              <span class="runs" title="This parameter was checked for {row.runs.length} years — switch between them on the right">
                +{row.runs.length - 1} more year{row.runs.length > 2 ? 's' : ''}
              </span>
            {/if}
          </div>
        </div>
        <div class="item-side">
          <span class="badge {item.routing}" title={outcome.hint}>{outcome.label}</span>
          {#if item.status !== 'pending'}
            <span class="badge {item.status}">{statusLabel(item.status).label}</span>
          {:else if item.critique?.verdict === 'fail'}
            <span class="flag" title="The automatic checks found a problem with this proposal">⚠ check failed</span>
          {/if}
        </div>
      </button>
    {:else}
      <div class="empty-state">
        {#if view === 'pending' && items.length}
          <span class="big">All caught up</span>
          <span>Nothing left to review{country || routing || search ? ' with these filters' : ''}.</span>
          <button class="link" onclick={() => (view = 'all')}>Show everything</button>
        {:else if items.length}
          <span class="big">No match</span>
          <span>Try clearing the search or filters.</span>
        {:else}
          <span class="big">Nothing to review yet</span>
          <span>Go to Parameters and ask the assistant to check some.</span>
        {/if}
      </div>
    {/each}
  </div>

  <div class="foot muted">
    <span>{rows.length} shown · use ↑ ↓ to move</span>
    <label class="inline" title="A parameter checked for several years appears once, with its newest year">
      <input type="checkbox" bind:checked={collapse} />
      group years
    </label>
  </div>
</section>

<style>
  .queue { display: flex; flex-direction: column; min-height: 0; gap: 0.7rem; padding: 0.9rem; }
  .views { align-self: flex-start; }
  .filters { display: flex; gap: 0.4rem; flex-wrap: wrap; }
  .search { flex: 1; min-width: 9rem; }
  .filters select { max-width: 11rem; }
  .list { overflow: auto; flex: 1; display: flex; flex-direction: column; gap: 2px; margin: 0 -0.3rem; padding: 0 0.3rem; }
  .item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.7rem;
    width: 100%;
    text-align: left;
    border: 1px solid transparent;
    background: transparent;
    border-radius: 9px;
    padding: 0.6rem 0.7rem;
  }
  .item:hover:not(:disabled) { background: var(--panel-2); border-color: transparent; }
  /* The selected row doubles as the keyboard cursor, so it needs to read as
     more than the hover highlight. */
  .item.selected, .item.selected:hover:not(:disabled) {
    background: var(--accent-soft);
    border-color: var(--accent);
  }
  .item-main { min-width: 0; flex: 1; }
  .item-title { font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .item-sub { font-size: 0.85rem; }
  .item-side { display: flex; flex-direction: column; align-items: flex-end; gap: 0.2rem; flex: none; }
  .flag { color: var(--warn); font-size: 0.75rem; font-weight: 600; }
  .runs { margin-left: 0.3rem; font-size: 0.78rem; }
  .foot { display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; }
  .inline { display: flex; align-items: center; gap: 0.3rem; white-space: nowrap; cursor: pointer; }
</style>
