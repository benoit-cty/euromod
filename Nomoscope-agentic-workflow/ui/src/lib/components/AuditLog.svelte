<script>
  // Every decision (params.review_decisions, append-only), newest first. The
  // log is also future training/validation data, so the technical columns
  // stay one tick away.
  import { statusLabel, routingLabel, relativeTime } from '../labels.js';

  let { decisions = [] } = $props();
  let search = $state('');
  let technical = $state(false);

  const shown = $derived(
    search.trim()
      ? decisions.filter((d) =>
          `${d.model_target} ${d.reviewer ?? ''} ${d.note ?? ''}`.toLowerCase().includes(search.trim().toLowerCase()),
        )
      : decisions,
  );
</script>

<section class="panel log">
  <div class="bar-row">
    <input class="search" placeholder="Search a parameter, reviewer or note…" bind:value={search} />
    <span class="muted small">{shown.length} decision{shown.length === 1 ? '' : 's'}</span>
    <label class="field check small">
      <input type="checkbox" bind:checked={technical} />
      Technical columns
    </label>
  </div>
  <div class="scroll">
    <table>
      <thead>
        <tr>
          <th>When</th><th>Parameter</th><th>Year</th><th>Decision</th><th>By</th>
          {#if technical}<th>Outcome</th><th>Confidence</th><th>Checks</th>{/if}
          <th>Note</th>
        </tr>
      </thead>
      <tbody>
        {#each shown as d}
          <tr>
            <td title={d.logged_at}>{relativeTime(d.logged_at)}</td>
            <td class="mono">{d.model_target}</td>
            <td>{d.as_of?.slice(0, 4) ?? '—'}</td>
            <td><span class="badge {d.action}">{statusLabel(d.action).label}</span></td>
            <td>{d.reviewer}</td>
            {#if technical}
              <td><span class="badge {d.routing}">{routingLabel(d.routing).label}</span></td>
              <td>{d.confidence ?? '—'}</td>
              <td>{d.critique_verdict ?? '—'}</td>
            {/if}
            <td>{d.note ?? ''}</td>
          </tr>
        {:else}
          <tr>
            <td colspan={technical ? 9 : 6}>
              <div class="empty-state">
                <span class="big">{decisions.length ? 'No match' : 'No decisions yet'}</span>
                <span>{decisions.length ? 'Try another search.' : 'Decisions you take in Review appear here.'}</span>
              </div>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</section>

<style>
  .log { display: flex; flex-direction: column; min-height: 0; gap: 0.8rem; }
  .bar-row { display: flex; gap: 0.8rem; align-items: center; flex-wrap: wrap; }
  .search { flex: 1; min-width: 14rem; }
  .scroll { overflow: auto; flex: 1; }
</style>
