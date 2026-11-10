<script>
  // Overview: the first screen. Three questions, answered in plain words —
  // what is waiting for me, can I export, is each country usable — and one
  // button per answer. Every number behind them is one click away on its page.
  import { api } from '../api.js';
  import Icon from './Icon.svelte';
  import { countryName, formatCount, relativeTime, humanize } from '../labels.js';
  import { countryReadiness } from '../readiness.js';

  let { dbUrl = '', items = [], reviewer = null, onnavigate, onexport } = $props();

  let stats = $state(null);
  let jobs = $state([]);
  let loadError = $state('');

  const pending = $derived(items.filter((i) => i.status === 'pending'));
  // Accepted value changes are what an export carries (metadata edits too,
  // which the queue does not show — the export reports the true count).
  const acceptedChanges = $derived(
    items.filter((i) => (i.status === 'accepted' || i.status === 'edited') && i.routing !== 'unchanged').length,
  );
  const decidedToday = $derived.by(() => {
    const today = new Date().toISOString().slice(0, 10);
    return items.filter((i) => i.status !== 'pending' && i.decision?.decided_at?.startsWith(today)).length;
  });
  const pendingByCountry = $derived.by(() => {
    const m = {};
    for (const i of pending) m[i.country] = (m[i.country] ?? 0) + 1;
    return m;
  });

  const countries = $derived.by(() => {
    if (!stats) return [];
    const inputs = new Map((stats.model_inputs?.by_country ?? []).map((r) => [r.code, r]));
    return stats.by_country.map((row) => {
      const input = inputs.get(row.code);
      return {
        code: row.code,
        laws: row.instruments,
        params: input?.parameters?.parameters ?? 0,
        ...countryReadiness(row, input),
      };
    });
  });

  const greeting = $derived.by(() => {
    const h = new Date().getHours();
    return h < 12 ? 'Good morning' : h < 18 ? 'Good afternoon' : 'Good evening';
  });

  async function load() {
    if (!dbUrl) return;
    try {
      const [s, j] = await Promise.all([api.dbStats(dbUrl), api.listJobs(dbUrl, 5).catch(() => ({ jobs: [] }))]);
      stats = s;
      jobs = j.jobs ?? [];
      loadError = '';
    } catch (e) {
      loadError = String(e);
    }
  }

  $effect(() => {
    if (dbUrl) load();
  });

  export function reload() {
    return load();
  }

  const JOB_NAMES = {
    workflow: 'Parameter check',
    ingest: 'Import',
    embed: 'Make texts searchable',
    translate: 'Translation',
    eval: 'Evaluation',
    encode: 'Search',
    impact: 'Impact estimate',
    chat: 'Chat question',
  };
  const JOB_STATUS = {
    queued: 'Waiting',
    running: 'Running',
    succeeded: 'Done',
    failed: 'Failed',
    cancelled: 'Cancelled',
  };
</script>

<div class="home">
  <section class="hero">
    <div>
      <h2>{greeting}{reviewer ? `, ${reviewer}` : ''}.</h2>
      {#if pending.length}
        <p class="lead">
          <strong>{pending.length}</strong> proposed value{pending.length === 1 ? '' : 's'} waiting for your review.
        </p>
      {:else if items.length}
        <p class="lead">You are all caught up: nothing is waiting for review.</p>
      {:else}
        <p class="lead">No proposals yet. Start by asking the assistant to check some parameters.</p>
      {/if}
    </div>
    {#if pending.length}
      <button class="primary big" onclick={() => onnavigate('review')}>
        Start reviewing <Icon name="arrow" size={18} />
      </button>
    {:else}
      <button class="primary big" onclick={() => onnavigate('params')}>
        Check parameters <Icon name="arrow" size={18} />
      </button>
    {/if}
  </section>

  <section class="tiles">
    <button class="tile" onclick={() => onnavigate('review')}>
      <span class="tile-icon warn"><Icon name="review" size={20} /></span>
      <span class="num">{formatCount(pending.length)}</span>
      <span class="label">To review</span>
    </button>
    <button class="tile" onclick={() => onnavigate('audit')}>
      <span class="tile-icon ok"><Icon name="check" size={20} /></span>
      <span class="num">{formatCount(decidedToday)}</span>
      <span class="label">Decided today</span>
    </button>
    <button class="tile" onclick={onexport} title="Export the accepted changes for EUROMOD">
      <span class="tile-icon accent"><Icon name="download" size={20} /></span>
      <span class="num">{formatCount(acceptedChanges)}</span>
      <span class="label">Accepted changes to export</span>
    </button>
    <button class="tile" onclick={() => onnavigate('database')}>
      <span class="tile-icon"><Icon name="book" size={20} /></span>
      <span class="num">{stats ? formatCount(stats.totals.instruments) : '…'}</span>
      <span class="label">Laws and texts in the library</span>
    </button>
  </section>

  <section class="panel">
    <h2>Countries</h2>
    {#if loadError}
      <p class="error">Could not load the library status: {loadError}</p>
    {:else if !stats}
      <p class="muted"><span class="spinner"></span> Loading…</p>
    {:else}
      <div class="countries">
        {#each countries as c (c.code)}
          <div class="country {c.level}">
            <div class="country-head">
              <span class="code">{c.code}</span>
              <strong>{countryName(c.code)}</strong>
              <span class="state {c.level}">
                {#if c.level === 'ready'}<Icon name="check" size={14} /> Ready
                {:else if c.level === 'partial'}<Icon name="alert" size={14} /> Usable
                {:else}<Icon name="x" size={14} /> Not set up{/if}
              </span>
            </div>
            <div class="muted small">
              {formatCount(c.laws)} law{c.laws === 1 ? '' : 's'} · {formatCount(c.params)} parameter{c.params === 1 ? '' : 's'}
              {#if pendingByCountry[c.code]}· <strong class="pend">{pendingByCountry[c.code]} to review</strong>{/if}
            </div>
            {#if c.problems.length}
              <ul class="problems">
                {#each c.problems as p}<li>{p}</li>{/each}
              </ul>
            {/if}
          </div>
        {/each}
      </div>
    {/if}
  </section>

  {#if jobs.length}
    <section class="panel">
      <h2>Recent activity</h2>
      <ul class="activity">
        {#each jobs as job (job.id)}
          <li>
            <span class="badge {job.status === 'succeeded' ? 'pass' : job.status === 'failed' ? 'fail' : 'pending'}">
              {JOB_STATUS[job.status] ?? humanize(job.status)}
            </span>
            <span>{JOB_NAMES[job.job_type] ?? humanize(job.job_type)}</span>
            <span class="muted small">{job.submitted_by ? `by ${job.submitted_by} · ` : ''}{relativeTime(job.submitted_at)}</span>
          </li>
        {/each}
      </ul>
    </section>
  {/if}
</div>

<style>
  .home { display: flex; flex-direction: column; gap: 1rem; overflow: auto; max-width: 72rem; }
  .hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
    padding: 1.4rem 1.6rem;
    border-radius: var(--radius);
    background: linear-gradient(120deg, var(--accent-soft), var(--panel));
    border: 1px solid var(--border);
  }
  .hero h2 { font-size: 1.3rem; margin: 0 0 0.25rem; }
  .lead { font-size: 1.05rem; margin: 0; }
  .tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr)); gap: 0.8rem; }
  .tile {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
    padding: 1rem 1.1rem;
    border-radius: var(--radius);
    border: 1px solid var(--border);
    background: var(--panel);
    box-shadow: var(--shadow);
    text-align: left;
  }
  .tile-icon {
    width: 2.2rem;
    height: 2.2rem;
    border-radius: 9px;
    display: grid;
    place-items: center;
    background: var(--panel-2);
    color: var(--muted);
    margin-bottom: 0.3rem;
  }
  .tile-icon.warn { background: var(--warn-soft); color: var(--warn); }
  .tile-icon.ok { background: var(--ok-soft); color: var(--ok); }
  .tile-icon.accent { background: var(--accent-soft); color: var(--accent); }
  .num { font-size: 1.6rem; font-weight: 700; line-height: 1.1; }
  .label { color: var(--muted); font-size: 0.9rem; }
  .countries { display: grid; grid-template-columns: repeat(auto-fill, minmax(17rem, 1fr)); gap: 0.7rem; }
  .country { border: 1px solid var(--border); border-radius: 10px; padding: 0.75rem 0.9rem; }
  .country-head { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.2rem; }
  .code {
    font-size: 0.72rem;
    font-weight: 700;
    background: var(--panel-2);
    border-radius: 5px;
    padding: 0.1rem 0.35rem;
    color: var(--muted);
  }
  .state { margin-left: auto; display: inline-flex; align-items: center; gap: 0.25rem; font-size: 0.8rem; font-weight: 600; }
  .state.ready { color: var(--ok); }
  .state.partial { color: var(--warn); }
  .state.missing { color: var(--muted); }
  .pend { color: var(--accent); }
  .problems { margin: 0.4rem 0 0; padding-left: 1.1rem; color: var(--muted); font-size: 0.82rem; }
  .activity { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; }
  .activity li { display: flex; align-items: center; gap: 0.7rem; padding: 0.45rem 0; border-bottom: 1px solid var(--border); }
  .activity li:last-child { border-bottom: 0; }
  .activity .small { margin-left: auto; }
</style>
