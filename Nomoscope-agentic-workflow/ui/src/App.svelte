<script>
  import { api } from './lib/api.js';
  import Icon from './lib/components/Icon.svelte';
  import Home from './lib/components/Home.svelte';
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
  let tab = $state('home');
  // Pages are kept alive once visited (hidden, not destroyed): switching away
  // must not lose a followed job's log or reset filters/selections.
  let visited = $state({ home: true });
  let paramsRunning = $state(false);
  let error = $state('');
  let statusMsg = $state('');
  let workerAlive = $state(null);
  const stored = (key) => {
    try {
      return localStorage.getItem(key);
    } catch {
      return null;
    }
  };
  let dark = $state(stored('theme') === 'dark');
  // Expert tools (golden set, evaluation, impact, jobs) are for the people
  // who build and measure the pipeline; a reviewer never needs them, so they
  // stay out of the sidebar until asked for.
  let expert = $state(stored('expert') === '1');
  // Component instances, for the page-aware Refresh button below.
  let homePage = $state(null);
  let dbTab = $state(null);
  let paramsTab = $state(null);
  let evalTab = $state(null);
  let goldenTab = $state(null);
  let impactTab = $state(null);
  let jobsTab = $state(null);

  const PAGES = [
    { id: 'home', icon: 'home', label: 'Overview', intro: 'Where things stand, and what to do next.' },
    { id: 'review', icon: 'review', label: 'Review', intro: 'Check each value the assistant proposes against the law, then accept, correct or reject it.' },
    { id: 'params', icon: 'list', label: 'Parameters', intro: 'Every EUROMOD parameter. Select some and ask the assistant to check them against this year’s law.' },
    { id: 'database', icon: 'search', label: 'Legislation', intro: 'Search the library of laws and official texts the assistant reads.' },
    { id: 'ingest', icon: 'plus', label: 'Add sources', intro: 'Add a law, circular or official document the library is missing.' },
    { id: 'audit', icon: 'history', label: 'History', intro: 'Every decision taken, newest first.' },
    { id: 'golden', icon: 'star', label: 'Golden set', expert: true, intro: 'Reference answers used to measure the assistant. Verify each drafted case.' },
    { id: 'eval', icon: 'chart', label: 'Evaluation', expert: true, intro: 'How well the assistant scores against the golden set, by model and language.' },
    { id: 'impact', icon: 'leaf', label: 'Impact', expert: true, intro: 'Estimated energy and carbon cost of the language-model calls.' },
    { id: 'jobs', icon: 'activity', label: 'Jobs', expert: true, intro: 'Everything the worker has run or is running, with its log.' },
  ];
  const page = $derived(PAGES.find((p) => p.id === tab) ?? PAGES[0]);
  const pendingCount = $derived(items.filter((i) => i.status === 'pending').length);

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
    try {
      localStorage.setItem('theme', dark ? 'dark' : 'light');
      localStorage.setItem('expert', expert ? '1' : '0');
    } catch {
      /* preferences are a convenience */
    }
  });

  // Leaving expert mode while on an expert page would leave a page with no
  // sidebar entry: go home instead.
  $effect(() => {
    if (!expert && page.expert) tab = 'home';
  });

  // The status line answers one action; it fades instead of piling up.
  $effect(() => {
    if (!statusMsg) return;
    const t = setTimeout(() => (statusMsg = ''), 8000);
    return () => clearTimeout(t);
  });

  async function init() {
    try {
      config = await api.getEnvConfig();
      if (config.db_error) error = `The database cannot be reached: ${config.db_error}`;
      else await refresh();
    } catch (e) {
      error = String(e);
    }
    pollWorker();
    try {
      const res = await api.phoenixProjects(config.db_url);
      const project =
        res.projects.find((p) => p.name === config.phoenix_project) ?? res.projects[0];
      phoenixGid = project?.gid ?? '';
    } catch {
      phoenixGid = ''; // Phoenix links degrade to the projects page
    }
  }

  async function pollWorker() {
    try {
      const status = await api.workerStatus(config.db_url);
      workerAlive = (status.workers ?? []).some((w) => w.alive);
    } catch {
      workerAlive = null;
    }
  }

  $effect(() => {
    const t = setInterval(pollWorker, 30000);
    return () => clearInterval(t);
  });

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
      const verb = { accepted: 'Accepted', edited: 'Accepted with your edits', rejected: 'Rejected', escalated: 'Sent to the national team' }[action] ?? action;
      statusMsg = `${verb}: ${updated.label ?? updated.model_target}`;
    } catch (e) {
      error = String(e);
    }
  }

  async function exportChanges() {
    try {
      const res = await api.exportChanges(config.db_url);
      if (res.canceled) statusMsg = 'Export cancelled.';
      else if (res.count === 0) statusMsg = 'Nothing to export yet: no accepted change and no corrected parameter.';
      else statusMsg = `${res.count} changed parameter(s) exported to ${res.paths.join(', ')}`;
    } catch (e) {
      error = String(e);
    }
  }

  function go(id) {
    tab = id;
    if (id === 'audit') loadDecisions().catch((e) => (error = String(e)));
  }

  // Jump from the Parameters page to a freshly created review item.
  async function openReviewItem(id) {
    await refresh();
    selectedId = id;
    tab = 'review';
  }

  async function loadDecisions() {
    const res = await api.loadDecisions(config.db_url);
    decisions = res.decisions;
  }

  // Each page owns its own data source, so Refresh acts on the page in view.
  const reloaders = {
    home: async () => {
      await refresh();
      await homePage?.reload();
    },
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
      pollWorker();
    } catch (e) {
      error = String(e);
    }
  }

  init();
</script>

{#snippet navItem(p)}
  <button
    class="nav-item"
    class:active={tab === p.id}
    aria-current={tab === p.id ? 'page' : undefined}
    onclick={() => go(p.id)}
  >
    <Icon name={p.icon} />
    <span class="nav-label">{p.label}</span>
    {#if p.id === 'review' && pendingCount}<span class="count">{pendingCount}</span>{/if}
    {#if p.id === 'params' && paramsRunning}<span class="running-dot" title="a check is running">●</span>{/if}
  </button>
{/snippet}

<div class="app">
  <aside class="sidebar">
    <div class="brand">
      <div class="logo">N</div>
      <div>
        <div class="brand-name">Nómos</div>
        <div class="brand-sub">EUROMOD parameter review</div>
      </div>
    </div>

    <nav>
      {#each PAGES.filter((p) => !p.expert) as p (p.id)}{@render navItem(p)}{/each}
      {#if expert}
        <div class="nav-section">Expert tools</div>
        {#each PAGES.filter((p) => p.expert) as p (p.id)}{@render navItem(p)}{/each}
      {/if}
    </nav>

    <div class="sidebar-foot">
      <div
        class="worker"
        title={workerAlive
          ? 'The worker that runs checks, searches and imports is online.'
          : workerAlive === false
            ? 'No worker is running: submitted work waits in the queue until one starts.'
            : 'Worker status unknown'}
      >
        <span class="dot" class:on={workerAlive} class:off={workerAlive === false}></span>
        {workerAlive ? 'Worker online' : workerAlive === false ? 'Worker offline' : 'Worker …'}
      </div>
      <div class="who" title="Your database login: every decision and job is recorded under it.">
        Signed in as <strong>{config.reviewer ?? '—'}</strong>
      </div>
      <label class="toggle">
        <input type="checkbox" bind:checked={expert} />
        <span>Show expert tools</span>
      </label>
      <button class="ghost theme" onclick={() => (dark = !dark)}>
        <Icon name={dark ? 'sun' : 'moon'} size={16} />
        {dark ? 'Light theme' : 'Dark theme'}
      </button>
    </div>
  </aside>

  <div class="content">
    <header class="topbar">
      <div class="title">
        <h1>{page.label}</h1>
        <p class="page-intro">{page.intro}</p>
      </div>
      <div class="actions">
        {#if reloaders[tab]}
          <button class="ghost" onclick={reloadActive} title="Reload this page’s data">
            <Icon name="refresh" size={16} /> Refresh
          </button>
        {/if}
        {#if tab === 'review' || tab === 'home'}
          <button
            onclick={exportChanges}
            title="Writes only what changed (accepted values and corrected parameters), one file per country, into a folder you pick."
          >
            <Icon name="download" size={16} /> Export for EUROMOD…
          </button>
        {/if}
      </div>
    </header>

    {#if error}
      <div class="callout err banner">
        <span>{error}</span>
        <button class="ghost" onclick={() => (error = '')} title="Dismiss"><Icon name="x" size={14} /></button>
      </div>
    {/if}
    {#if statusMsg}
      <div class="callout ok banner"><span>{statusMsg}</span></div>
    {/if}

    <main hidden={tab !== 'home'} class="single">
      <Home
        bind:this={homePage}
        dbUrl={config.db_url}
        {items}
        reviewer={config.reviewer}
        onnavigate={go}
        onexport={exportChanges}
      />
    </main>
    {#if visited.review}
      <main class="split" hidden={tab !== 'review'}>
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
</div>

<style>
  .app { display: flex; height: 100vh; }
  .sidebar {
    width: 228px;
    flex: none;
    background: var(--sidebar);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    padding: 1rem 0.7rem;
    gap: 1.2rem;
  }
  .brand { display: flex; align-items: center; gap: 0.6rem; padding: 0 0.4rem; }
  .logo {
    width: 2.1rem;
    height: 2.1rem;
    border-radius: 10px;
    background: var(--accent);
    color: #fff;
    display: grid;
    place-items: center;
    font-weight: 700;
    font-size: 1.1rem;
  }
  .brand-name { font-weight: 700; font-size: 1.05rem; }
  .brand-sub { color: var(--muted); font-size: 0.75rem; }
  nav { display: flex; flex-direction: column; gap: 2px; flex: 1; overflow: auto; }
  .nav-item {
    justify-content: flex-start;
    gap: 0.65rem;
    border: 0;
    background: transparent;
    color: var(--muted);
    padding: 0.55rem 0.7rem;
    border-radius: 8px;
    width: 100%;
    text-align: left;
  }
  .nav-item:hover:not(:disabled) { background: var(--panel-2); color: var(--text); }
  .nav-item.active { background: var(--accent-soft); color: var(--accent); font-weight: 600; }
  .nav-label { flex: 1; }
  .count {
    background: var(--accent);
    color: #fff;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.05rem 0.45rem;
    min-width: 1.4rem;
    text-align: center;
  }
  .nav-section {
    margin: 1rem 0.7rem 0.3rem;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--muted);
    font-weight: 600;
  }
  .running-dot { color: var(--accent); animation: pulse 1.2s ease-in-out infinite; }
  @keyframes pulse { 50% { opacity: 0.25; } }

  .sidebar-foot {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 0.8rem 0.4rem 0;
    border-top: 1px solid var(--border);
    font-size: 0.85rem;
    color: var(--muted);
  }
  .worker { display: flex; align-items: center; gap: 0.45rem; }
  .dot { width: 0.55rem; height: 0.55rem; border-radius: 50%; background: var(--border-strong); }
  .dot.on { background: var(--ok); }
  .dot.off { background: var(--err); }
  .who strong { color: var(--text); }
  .toggle { display: flex; align-items: center; gap: 0.45rem; cursor: pointer; }
  .theme { justify-content: flex-start; padding: 0.3rem 0; font-size: 0.85rem; }

  .content { flex: 1; display: flex; flex-direction: column; min-width: 0; padding: 1.1rem 1.4rem; gap: 0.9rem; }
  .topbar { display: flex; align-items: flex-start; gap: 1rem; }
  .title { flex: 1; min-width: 0; }
  .title h1 { margin-bottom: 0.15rem; }
  .actions { display: flex; gap: 0.5rem; flex: none; }
  .banner { display: flex; align-items: center; justify-content: space-between; gap: 0.6rem; padding: 0.5rem 0.9rem; }
  .banner button { padding: 0.2rem; }

  main { flex: 1; min-height: 0; display: flex; flex-direction: column; }
  main.single > :global(*) { flex: 1; min-height: 0; }
  main.split {
    display: grid;
    grid-template-columns: minmax(360px, 2fr) 3fr;
    gap: 1rem;
  }
  /* display:grid/flex above would override the hidden attribute's default */
  main[hidden] { display: none; }

  @media (max-width: 1000px) {
    .sidebar { width: 64px; padding: 1rem 0.4rem; }
    .brand > div:last-child, .nav-label, .nav-section, .sidebar-foot { display: none; }
    .nav-item { justify-content: center; position: relative; }
    .count { position: absolute; top: 2px; right: 2px; font-size: 0.65rem; }
    main.split { grid-template-columns: 1fr; overflow: auto; }
  }
</style>
