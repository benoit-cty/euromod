<script>
  // Golden set review: the human gate on drafted evaluation ground truth.
  //
  // Cases are drafted from the OpenFisca corpus (`nomokrisis-eval
  // build-openfisca-dataset`) with verified=false. OpenFisca is curated and
  // occasionally wrong or lagging, so nothing here counts until a reviewer
  // compares the drafted value against the parameter EUROMOD holds and accepts
  // it. Accept sets verified=true; Reject records that a human said no, which
  // is not the same as nobody having looked yet.
  import { api } from '../api.js';

  let { datasetDir = '', reviewer = 'reviewer' } = $props();

  let dir = $state(''); // seeded from datasetDir once config loads
  let cases = $state(null);
  let error = $state('');
  let loading = $state(false);
  let selectedPath = $state(null);
  let note = $state('');
  let filter = $state('unreviewed');
  let saving = $state(false);
  let listEl = $state(null);
  let sectionEl = $state(null);

  const FILTERS = [
    { key: 'all', label: 'All' },
    { key: 'unreviewed', label: 'To review' },
    { key: 'verified', label: 'Accepted' },
    { key: 'rejected', label: 'Rejected' },
  ];

  function status(c) {
    if (c.verified) return 'verified';
    if (c.reviewed_by) return 'rejected';
    return 'unreviewed';
  }

  const visible = $derived(
    (cases ?? []).filter((c) => filter === 'all' || status(c) === filter),
  );
  const selected = $derived((cases ?? []).find((c) => c._path === selectedPath) ?? null);
  const counts = $derived({
    total: cases?.length ?? 0,
    verified: (cases ?? []).filter((c) => c.verified).length,
    rejected: (cases ?? []).filter((c) => status(c) === 'rejected').length,
  });

  $effect(() => {
    if (datasetDir && !dir) dir = datasetDir;
  });

  $effect(() => {
    if (dir && !cases && !loading && !error) load();
  });

  async function load() {
    loading = true;
    error = '';
    try {
      const res = await api.goldenCases(dir);
      cases = res.cases;
      if (selectedPath && !cases.some((c) => c._path === selectedPath)) selectedPath = null;
    } catch (e) {
      error = String(e);
      cases = null;
    } finally {
      loading = false;
    }
  }

  // Target of the shell's Reload button while this tab is showing.
  export async function reload() {
    await load();
  }

  function select(c) {
    selectedPath = c._path;
    note = c.review_note ?? '';
  }

  // Accept/Reject steps to the next case on its own, so the row it lands on can
  // be below the fold of a list that now scrolls independently. Same for the
  // arrow keys below.
  $effect(() => {
    selectedPath;
    visible;
    listEl?.querySelector('tr.selected')?.scrollIntoView({ block: 'nearest' });
  });

  // Move the selection by `delta` rows of the current filter. With nothing
  // selected yet, enter the list from the end the reviewer is arrowing towards.
  function move(delta) {
    if (!visible.length) return;
    const current = visible.findIndex((c) => c._path === selectedPath);
    const next =
      current === -1
        ? delta > 0
          ? 0
          : visible.length - 1
        : Math.min(visible.length - 1, Math.max(0, current + delta));
    if (visible[next]._path !== selectedPath) select(visible[next]);
  }

  // Arrow keys walk the worklist. Bound on the window rather than on a focusable
  // row so the reviewer can key straight through the cases without clicking one
  // first — but only while this tab is on screen, and never when the focus is
  // somewhere that owns its arrow keys. Text fields are excluded here (unlike
  // the review queue's search box): the note field is part of the verdict, and
  // stepping away from it would discard what is being typed.
  function onkeydown(event) {
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    if (!sectionEl || sectionEl.offsetParent === null) return;
    const active = document.activeElement;
    // Buttons ignore arrow keys anyway, so "Accept, then arrow on" keeps working
    // with the focus left on the verdict button.
    if (active && active !== document.body && active.tagName !== 'BUTTON') return;
    if (event.key === 'ArrowDown') move(1);
    else if (event.key === 'ArrowUp') move(-1);
    else if (event.key === 'PageDown') move(10);
    else if (event.key === 'PageUp') move(-10);
    else if (event.key === 'Home') move(-visible.length);
    else if (event.key === 'End') move(visible.length);
    else return;
    event.preventDefault();
  }

  async function decide(verified) {
    if (!selected) return;
    saving = true;
    try {
      const res = await api.setGoldenVerified({
        path: selected._path,
        verified,
        reviewer,
        note: note || null,
      });
      // Keep the enrichment the list was loaded with: the write path only
      // round-trips the case file itself.
      const updated = { ...selected, ...res.case };
      cases = cases.map((c) => (c._path === updated._path ? updated : c));
      error = '';
      // Reviewing runs down a filtered worklist; step to the next one still in it.
      const next = visible.find((c) => c._path !== updated._path);
      if (next && filter !== 'all') select(next);
    } catch (e) {
      error = String(e);
    } finally {
      saving = false;
    }
  }

  function fmt(value) {
    if (value == null) return '—';
    if (Array.isArray(value)) {
      return value
        .map((b) => `${b.threshold ?? 0} → ${b.rate ?? b.amount ?? '—'}`)
        .join('  |  ');
    }
    return String(value);
  }

  function currentValue(c) {
    return c._parameter?.current?.value ?? null;
  }

  function text(blob) {
    if (!blob) return '';
    if (typeof blob === 'string') return blob;
    return blob.fr ?? blob.en ?? Object.values(blob)[0] ?? '';
  }

  // Legifrance deep-links for every national id mentioned in the expected
  // citations — the reviewer's fastest route to the actual legal text.
  function legifrance(c) {
    const ids = new Set();
    for (const citation of c.expected?.citations ?? []) {
      for (const id of citation.match(/(?:JORF|LEGI)(?:TEXT|ARTI)\d+/g) ?? []) ids.add(id);
    }
    for (const id of (c.notes ?? '').match(/(?:JORF|LEGI)(?:TEXT|ARTI)\d+/g) ?? []) ids.add(id);
    return [...ids].map((id) => ({
      id,
      url: id.startsWith('LEGIARTI')
        ? `https://www.legifrance.gouv.fr/codes/article_lc/${id}`
        : `https://www.legifrance.gouv.fr/jorf/id/${id}`,
    }));
  }
</script>

<svelte:window {onkeydown} />

<section class="panel golden" bind:this={sectionEl}>
  <div class="row">
    <label class="grow">
      Golden dataset directory
      <input bind:value={dir} class="mono" />
    </label>
    <button onclick={load} disabled={loading}>{loading ? 'Loading…' : 'Reload cases'}</button>
  </div>

  {#if error}<p class="error">{error}</p>{/if}

  {#if cases}
    <div class="row between">
      <div class="filters">
        {#each FILTERS as f}
          <button class:primary={filter === f.key} onclick={() => (filter = f.key)}>{f.label}</button>
        {/each}
      </div>
      <span class="muted">
        {counts.verified} accepted · {counts.rejected} rejected ·
        {counts.total - counts.verified - counts.rejected} left of {counts.total}
      </span>
    </div>

    <div class="split">
      <div class="scroll" bind:this={listEl}>
        <table class="list">
          <thead>
            <tr><th></th><th>Case</th><th>Routing</th><th>Expected</th><th>From</th></tr>
          </thead>
          <tbody>
            {#each visible as c (c._path)}
              <tr class:selected={c._path === selectedPath} onclick={() => select(c)}>
                <td>
                  {#if c.verified}<span class="tick ok" title="accepted">✓</span>
                  {:else if c.reviewed_by}<span class="tick bad" title="rejected">✗</span>
                  {:else}<span class="muted" title="not reviewed">·</span>{/if}
                </td>
                <td class="mono">{c.id}</td>
                <td>{c.expected?.routing}</td>
                <td class="num">{fmt(c.expected?.value)}</td>
                <td class="muted">{c.expected?.valid_from ?? '—'}</td>
              </tr>
            {:else}
              <tr><td colspan="5" class="muted">No cases in this filter.</td></tr>
            {/each}
          </tbody>
        </table>
      </div>

      <div class="detail">
        {#if !selected}
          <p class="muted">Select a case to review its drafted ground truth.</p>
        {:else}
          <h2 class="mono">{selected.id}</h2>
          <p class="muted">
            {selected.country} · {selected.language} · as_of {selected.as_of}
            {#if selected.difficulty}· {selected.difficulty}{/if}
            {#if selected.source_class}· {selected.source_class}{/if}
            · drafted by <span class="mono">{selected.drafted_by}</span>
          </p>

          {#if selected._parameter}
            <h3>Parameter under test</h3>
            <p class="mono small">{selected._parameter.model_target}</p>
            <p>{text(selected._parameter.label) || text(selected._parameter.short_label)}</p>
            {#if text(selected._parameter.description)}
              <p class="muted small">{text(selected._parameter.description)}</p>
            {/if}
            <p class="muted small">
              unit {selected._parameter.unit ?? '—'} · temporal basis
              <strong>{selected._parameter.temporal_basis ?? 'in_force'}</strong>
              {#if selected._parameter.values}· {selected._parameter.values} value(s) on record{/if}
            </p>
          {/if}

          <h3>Drafted expectation</h3>
          <table class="compare">
            <tbody>
              <tr>
                <th>EUROMOD holds</th>
                <td class="num">{fmt(currentValue(selected))}</td>
                <td class="muted">from {selected._parameter?.current?.valid_from ?? '—'}</td>
              </tr>
              <tr>
                <th>OpenFisca says</th>
                <td class="num strong">{fmt(selected.expected?.value)}</td>
                <td class="muted">from {selected.expected?.valid_from ?? '—'}</td>
              </tr>
              <tr>
                <th>Routing</th>
                <td colspan="2"><strong>{selected.expected?.routing}</strong></td>
              </tr>
              <tr>
                <th>Citations</th>
                <td colspan="2">
                  {#each selected.expected?.citations ?? [] as citation}
                    <span class="badge">{citation}</span>
                  {:else}
                    <span class="muted">none — citation and retrieval KPIs stay unscored</span>
                  {/each}
                </td>
              </tr>
            </tbody>
          </table>

          {#if legifrance(selected).length}
            <p class="links">
              {#each legifrance(selected) as ref}
                <button class="link" onclick={() => api.openExternal(ref.url)}>{ref.id} ↗</button>
              {/each}
            </p>
          {/if}

          <h3>Provenance</h3>
          <ul class="notes">
            {#each (selected.notes ?? '').split(' | ') as part}
              {#if part.trim()}<li>{part}</li>{/if}
            {/each}
          </ul>

          <h3>Verdict</h3>
          {#if selected.reviewed_by}
            <p class="muted">
              last reviewed by <strong>{selected.reviewed_by}</strong> —
              {selected.verified ? 'accepted' : 'rejected'}
              {#if selected.review_note}: {selected.review_note}{/if}
            </p>
          {/if}
          <label>
            Note (optional — why you accepted, or what is wrong)
            <input bind:value={note} />
          </label>
          <div class="row">
            <button class="primary" disabled={saving} onclick={() => decide(true)}>
              Accept as ground truth
            </button>
            <button disabled={saving} onclick={() => decide(false)}>Reject</button>
          </div>
          <p class="muted small">
            Accepting sets <span class="mono">verified: true</span> in
            <span class="mono">{selected._path}</span> — commit the file to freeze it into the
            golden set.
          </p>
        {/if}
      </div>
    </div>
  {/if}
</section>

<style>
  /* The panel itself never scrolls: the list and the detail pane each own their
     own scrollbar, so running down a long worklist leaves the detail in place. */
  .golden { overflow: hidden; display: flex; flex-direction: column; gap: 0.8rem; min-height: 0; }
  .row { display: flex; gap: 0.5rem; align-items: end; flex-wrap: wrap; }
  .row.between { justify-content: space-between; align-items: center; }
  .grow { flex: 1; min-width: 16rem; }
  .filters { display: flex; gap: 0.3rem; }
  label { display: flex; flex-direction: column; gap: 0.25rem; color: var(--muted); }
  label input { width: 100%; }
  .error { color: var(--err); }
  .split {
    display: grid;
    grid-template-columns: minmax(24rem, 2fr) 3fr;
    gap: 0.8rem;
    flex: 1;
    min-height: 0;
  }
  .split > * { min-height: 0; }
  .scroll { overflow: auto; }
  .list tbody tr { cursor: pointer; }
  .list tbody tr:hover { background: var(--panel-2); }
  /* The selected row doubles as the keyboard cursor, so it gets a marker the
     hover highlight does not have. */
  .list tbody tr.selected { background: var(--accent-soft); }
  .list tbody tr.selected td:first-child { box-shadow: inset 2px 0 0 var(--accent); }
  .detail { border-left: 1px solid var(--border); padding-left: 0.8rem; overflow: auto; }
  .detail h2 { margin: 0; }
  .detail h3 { margin: 0.9rem 0 0.3rem; }
  .compare th { text-align: left; color: var(--muted); font-weight: 400; padding-right: 0.8rem; }
  .num { font-variant-numeric: tabular-nums; }
  .num.strong { font-weight: 700; }
  .small { font-size: 0.85em; }
  .tick.ok { color: var(--ok); }
  .tick.bad { color: var(--err); font-weight: 700; }
  .notes { margin: 0; padding-left: 1.1rem; color: var(--muted); font-size: 0.85em; }
  .notes li { overflow-wrap: anywhere; }
  .links { display: flex; gap: 0.4rem; flex-wrap: wrap; }
  button.link { background: none; border: none; color: var(--accent); cursor: pointer; padding: 0; }
</style>
