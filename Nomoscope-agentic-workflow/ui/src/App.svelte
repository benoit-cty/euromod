<script>
  import { api } from './lib/api.js';
  import QueueList from './lib/components/QueueList.svelte';
  import DetailPanel from './lib/components/DetailPanel.svelte';
  import AuditLog from './lib/components/AuditLog.svelte';
  import DatabaseTab from './lib/components/DatabaseTab.svelte';
  import IngestTab from './lib/components/IngestTab.svelte';
  import EvalTab from './lib/components/EvalTab.svelte';
  import GoldenTab from './lib/components/GoldenTab.svelte';
  import ParamsTab from './lib/components/ParamsTab.svelte';
  import ImpactTab from './lib/components/ImpactTab.svelte';
  import JobsTab from './lib/components/JobsTab.svelte';

  // The UI is remote (ADR 0004): its one credential is the database login,
  // and `reviewer` is that login's current_user as the server sees it.
  let config = $state({
    reviewer: null,
    db_error: null,
    db_url: '',
    phoenix_endpoint: '',
    phoenix_project: '',
  });
  // GraphQL gid of the workflow's Phoenix project, for trace deep-links
  let phoenixGid = $state('');
  let items = $state([]);
  let facets = $state(null);
  let selectedId = $state(null);
  let decisions = $state([]);
  let tab = $state('review');
  // Tabs are kept alive once visited (hidden, not destroyed): switching away
  // must not lose a followed job's log or reset filters/selections.
  let visited = $state({ review: true });
  let paramsRunning = $state(false);
  let error = $state('');
  let statusMsg = $state('');
  let dark = $state(localStorage.getItem('theme') === 'dark');
  // Component instances, for the tab-aware Reload button below.
  let dbTab = $state(null);
  let paramsTab = $state(null);
  let evalTab = $state(null);
  let goldenTab = $state(null);
  let impactTab = $state(null);
  let jobsTab = $state(null);

  const selected = $derived(items.find((i) => i.id === selectedId) ?? null);
  // Every run of the selected parameter (newest first, as loadQueue sorts them):
  // the list collapses them to one row, the detail panel navigates between them.
  const siblings = $derived(
    selected
      ? items.filter(
          (i) => i.country === selected.country && i.model_target === selected.model_target,
        )
      : [],
  );

  $effect(() => {
    visited[tab] = true;
  });

  $effect(() => {
    document.body.classList.toggle('dark', dark);
    localStorage.setItem('theme', dark ? 'dark' : 'light');
  });

  async function init() {
    try {
      config = await api.getEnvConfig();
      if (config.db_error) error = `Database unreachable: ${config.db_error}`;
      else await refresh();
    } catch (e) {
      error = String(e);
    }
    try {
      const res = await api.phoenixProjects(config.db_url);
      const project =
        res.projects.find((p) => p.name === config.phoenix_project) ?? res.projects[0];
      phoenixGid = project?.gid ?? '';
    } catch {
      phoenixGid = ''; // Phoenix links degrade to the projects page
    }
  }

  async function refresh() {
    try {
      const res = await api.loadQueue(config.db_url);
      items = res.items;
      facets = res.facets;
      error = '';
    } catch (e) {
      error = String(e);
    }
  }

  // editedFields patches the non-value parts of the proposal (validity dates,
  // legal/source status, references); both are null on a plain accept.
  async function decide(action, note, editedValue, editedFields) {
    try {
      const res = await api.saveDecision({
        db_url: config.db_url,
        item_id: selected.id,
        action,
        reviewer: config.reviewer,
        note: note || null,
        edited_value: editedValue === undefined ? null : editedValue,
        edited_fields: editedFields ?? null,
      });
      // Throws if the database refused the decision, in which case nothing was
      // written and the item is still pending — the catch below shows why.
      const updated = res.item;
      items = items.map((i) => (i.id === updated.id ? updated : i));
      error = '';
      statusMsg = `${updated.id}: ${action}`;
    } catch (e) {
      error = String(e);
    }
  }

  async function exportAccepted() {
    try {
      const res = await api.exportAccepted(config.db_url);
      if (res.canceled) statusMsg = 'Export cancelled.';
      else if (res.count === 0) statusMsg = 'Nothing to export — no accepted or edited items.';
      else statusMsg = `${res.count} record(s) exported: ${res.paths.join(', ')}`;
    } catch (e) {
      error = String(e);
    }
  }

  // Jump from the Parameters tab to a freshly created review-queue item.
  async function openReviewItem(id) {
    await refresh();
    selectedId = id;
    tab = 'review';
  }

  async function loadDecisions() {
    const res = await api.loadDecisions(config.db_url);
    decisions = res.decisions;
  }

  async function showAudit() {
    tab = 'audit';
    try {
      await loadDecisions();
    } catch (e) {
      error = String(e);
    }
  }

  // Each tab owns its own data source, so Reload acts on the tab in view —
  // reloading the queue while the Database tab is up looks like a dead button.
  const reloaders = {
    review: refresh,
    audit: loadDecisions,
    database: () => dbTab?.reload(),
    params: () => paramsTab?.reload(),
    golden: () => goldenTab?.reload(),
    eval: () => evalTab?.reload(),
    impact: () => impactTab?.reload(),
    jobs: () => jobsTab?.reload(),
  };

  async function reloadActive() {
    try {
      await reloaders[tab]?.();
    } catch (e) {
      error = String(e);
    }
  }

  init();
</script>

<div class="shell">
  <header>
    <h1>EUROMOD Parameter Review</h1>
    <nav>
      <button class:primary={tab === 'ingest'} onclick={() => (tab = 'ingest')}>Ingest</button>
      <button class:primary={tab === 'database'} onclick={() => (tab = 'database')}>Database</button>
      <button class:primary={tab === 'params'} onclick={() => (tab = 'params')}>
        Parameters{#if paramsRunning}<span class="running-dot" title="agentic run in progress">●</span>{/if}
      </button>
      <button class:primary={tab === 'review'} onclick={() => (tab = 'review')}>Review queue</button>
      <button class:primary={tab === 'audit'} onclick={showAudit}>Audit log</button>
      <button class:primary={tab === 'golden'} onclick={() => (tab = 'golden')}>Golden set</button>
      <button class:primary={tab === 'eval'} onclick={() => (tab = 'eval')}>Evaluation</button>
      <button class:primary={tab === 'impact'} onclick={() => (tab = 'impact')}>Impact</button>
      <button class:primary={tab === 'jobs'} onclick={() => (tab = 'jobs')}>Jobs</button>
    </nav>
    <div class="spacer"></div>
    <span class="inline" title="your database login (current_user) — every decision, job and verdict is recorded under it">
      Reviewer <strong class="mono">{config.reviewer ?? '—'}</strong>
    </span>
    <button onclick={reloadActive} disabled={!reloaders[tab]} title="Reload the current tab">
      Reload
    </button>
    <button onclick={exportAccepted} title="One JSON file per country, into a folder you pick">Export accepted…</button>
    <button onclick={() => (dark = !dark)}>{dark ? '☀' : '☾'}</button>
  </header>

  {#if error}<div class="banner error">{error}</div>{/if}
  {#if statusMsg}<div class="banner">{statusMsg}</div>{/if}

  {#if visited.review}
    <main hidden={tab !== 'review'}>
      <QueueList {items} {facets} {selectedId} onselect={(id) => (selectedId = id)} />
      <DetailPanel
        item={selected}
        {siblings}
        onselectrun={(id) => (selectedId = id)}
        ondecide={decide}
        dbUrl={config.db_url}
        phoenixEndpoint={config.phoenix_endpoint || 'http://localhost:6006'}
        {phoenixGid}
      />
    </main>
  {/if}
  {#if visited.params}
    <main class="single" hidden={tab !== 'params'}>
      <ParamsTab
        bind:this={paramsTab}
        dbUrl={config.db_url}
        phoenixEndpoint={config.phoenix_endpoint || 'http://localhost:6006'}
        onopenitem={openReviewItem}
        active={tab === 'params'}
        onrunning={(v) => (paramsRunning = v)}
      />
    </main>
  {/if}
  {#if visited.audit}
    <main class="single" hidden={tab !== 'audit'}>
      <AuditLog {decisions} />
    </main>
  {/if}
  {#if visited.database}
    <main class="single" hidden={tab !== 'database'}>
      <DatabaseTab bind:this={dbTab} dbUrl={config.db_url} />
    </main>
  {/if}
  {#if visited.ingest}
    <main class="single" hidden={tab !== 'ingest'}>
      <IngestTab dbUrl={config.db_url} />
    </main>
  {/if}
  {#if visited.golden}
    <main class="single" hidden={tab !== 'golden'}>
      <GoldenTab bind:this={goldenTab} dbUrl={config.db_url} />
    </main>
  {/if}
  {#if visited.eval}
    <main class="single" hidden={tab !== 'eval'}>
      <EvalTab bind:this={evalTab} dbUrl={config.db_url} />
    </main>
  {/if}
  {#if visited.impact}
    <main class="single" hidden={tab !== 'impact'}>
      <ImpactTab bind:this={impactTab} dbUrl={config.db_url} />
    </main>
  {/if}
  {#if visited.jobs}
    <main class="single" hidden={tab !== 'jobs'}>
      <JobsTab bind:this={jobsTab} dbUrl={config.db_url} active={tab === 'jobs'} />
    </main>
  {/if}
</div>

<style>
  .shell {
    display: flex;
    flex-direction: column;
    height: 100vh;
    padding: 0.8rem;
    gap: 0.7rem;
  }
  header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  header h1 { margin: 0 0.8rem 0 0; }
  nav { display: flex; gap: 0.3rem; }
  .running-dot {
    margin-left: 0.35rem;
    color: var(--accent);
    animation: pulse 1.2s ease-in-out infinite;
  }
  @keyframes pulse {
    50% { opacity: 0.25; }
  }
  .spacer { flex: 1; }
  .inline { display: flex; align-items: center; gap: 0.35rem; color: var(--muted); }
  .banner {
    padding: 0.4rem 0.8rem;
    border-radius: 8px;
    background: var(--accent-soft);
    color: var(--accent);
  }
  .banner.error { background: var(--err-soft); color: var(--err); }
  main {
    flex: 1;
    display: grid;
    grid-template-columns: minmax(430px, 2fr) 3fr;
    gap: 0.7rem;
    min-height: 0;
  }
  main.single { grid-template-columns: 1fr; }
  /* display:grid above would override the hidden attribute's default */
  main[hidden] { display: none; }
</style>
