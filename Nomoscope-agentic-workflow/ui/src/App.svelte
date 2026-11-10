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
  import brandBackground from './assets/brand_background_EUROMOD.jpg';

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
  // stay out of the tab strip until asked for.
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
  // tab: go home instead.
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
    class="tab"
    class:active={tab === p.id}
    class:expert={p.expert}
    role="tab"
    aria-selected={tab === p.id}
    title={p.intro}
    onclick={() => go(p.id)}
  >
    {p.label}
    {#if p.id === 'review' && pendingCount}<span class="count">{pendingCount}</span>{/if}
    {#if p.id === 'params' && paramsRunning}<span class="running-dot" title="a check is running">●</span>{/if}
  </button>
{/snippet}

<div class="app">
  <!-- EUROMOD's own layout: a tab strip under the logo, a ribbon of grouped
       commands, the brand star behind the pages, a status bar at the foot. -->
  <header class="tabstrip">
    <div class="logo" title="Nómos: EUROMOD parameter review">N</div>
    <nav role="tablist">
      {#each PAGES.filter((p) => !p.expert) as p (p.id)}{@render navItem(p)}{/each}
      {#if expert}
        {#each PAGES.filter((p) => p.expert) as p (p.id)}{@render navItem(p)}{/each}
      {/if}
    </nav>
  </header>

  <div class="ribbon">
    <div class="group">
      <div class="cmds">
        <button
          class="big-cmd"
          onclick={exportChanges}
          title="Writes only what changed (accepted values and corrected parameters), one file per country, into a folder you pick."
        >
          <Icon name="download" size={24} />
          <span>Export</span>
        </button>
        <button
          class="big-cmd"
          onclick={reloadActive}
          disabled={!reloaders[tab]}
          title="Reload this page’s data"
        >
          <Icon name="refresh" size={24} />
          <span>Refresh</span>
        </button>
      </div>
      <div class="group-label">General</div>
    </div>
    <div class="group page-group">
      <div class="cmds col">
        <strong>{page.label}</strong>
        <span class="page-intro">{page.intro}</span>
      </div>
      <div class="group-label">Page</div>
    </div>
    <div class="group">
      <div class="cmds col">
        <label class="inline">
          Theme:
          <select value={dark ? 'dark' : 'light'} onchange={(e) => (dark = e.currentTarget.value === 'dark')}>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </label>
        <label class="inline toggle">
          <input type="checkbox" bind:checked={expert} />
          <Icon name="tools" size={15} /> Show expert tools
        </label>
      </div>
      <div class="group-label">Display</div>
    </div>
    <div class="group">
      <div class="cmds col">
        <div
          class="inline"
          title={workerAlive
            ? 'The worker that runs checks, searches and imports is online.'
            : workerAlive === false
              ? 'No worker is running: submitted work waits in the queue until one starts.'
              : 'Worker status unknown'}
        >
          <span class="dot" class:on={workerAlive} class:off={workerAlive === false}></span>
          {workerAlive ? 'Worker online' : workerAlive === false ? 'Worker offline' : 'Worker …'}
        </div>
        <div class="inline" title="Your database login: every decision and job is recorded under it.">
          Signed in as <strong>{config.reviewer ?? '—'}</strong>
        </div>
      </div>
      <div class="group-label">Connection</div>
    </div>
  </div>

  <div class="content" style:--brand-bg={`url(${brandBackground})`}>
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

  <footer class="statusbar">
    <span>{pendingCount ? `${pendingCount} proposal(s) waiting for review` : 'Ready'}</span>
    <span class="muted">{config.reviewer ? `Signed in as ${config.reviewer}` : 'Not connected'}</span>
  </footer>
</div>

<style>
  .app { display: flex; flex-direction: column; height: 100vh; }

  /* --- Tab strip (EUROMOD: logo disc, then light-blue tabs) --- */
  .tabstrip {
    display: flex;
    align-items: flex-end;
    gap: 0.6rem;
    background: var(--strip);
    padding: 0.35rem 0.5rem 0;
    flex: none;
  }
  .logo {
    width: 2.6rem;
    height: 2.6rem;
    margin-bottom: 0.25rem;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, #4f72c9, #1f3d8f);
    border: 2px solid #fff;
    box-shadow: 0 0 0 1px var(--border-strong);
    color: #fff;
    display: grid;
    place-items: center;
    font-size: 1.35rem;
    font-weight: 700;
    flex: none;
  }
  nav { display: flex; gap: 3px; overflow-x: auto; min-width: 0; }
  .tab {
    border: 1px solid var(--border-strong);
    border-bottom: 0;
    border-radius: 10px 10px 0 0;
    background: var(--tab);
    color: var(--text);
    padding: 0.5rem 1rem;
    box-shadow: none;
    white-space: nowrap;
    flex: none;
  }
  .tab:hover:not(:disabled) { background: var(--tab-hover); border-color: var(--border-strong); box-shadow: none; }
  .tab.active { background: var(--panel); position: relative; top: 1px; padding-bottom: calc(0.5rem + 1px); }
  .tab.expert { font-style: italic; }
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
  .running-dot { color: var(--accent); animation: pulse 1.2s ease-in-out infinite; }
  @keyframes pulse { 50% { opacity: 0.25; } }

  /* --- Ribbon: groups of commands, each captioned underneath --- */
  .ribbon {
    display: flex;
    flex: none;
    background: var(--panel);
    border-top: 1px solid var(--border-strong);
    border-bottom: 1px solid var(--border-strong);
    overflow-x: auto;
    font-size: 0.9rem;
  }
  .group {
    display: flex;
    flex-direction: column;
    border-right: 1px solid var(--border-strong);
    flex: none;
  }
  .group.page-group { flex: 1 1 18rem; min-width: 14rem; }
  .cmds { flex: 1; display: flex; gap: 0.3rem; padding: 0.4rem 0.6rem; align-items: stretch; }
  .cmds.col { flex-direction: column; gap: 0.35rem; justify-content: center; }
  .group-label {
    text-align: center;
    font-size: 12px;
    color: var(--text);
    border-top: 1px solid var(--border-strong);
    padding: 0.05rem 0.5rem 0.1rem;
  }
  .big-cmd {
    flex-direction: column;
    gap: 0.25rem;
    padding: 0.4rem 0.7rem;
    border-radius: 5px;
    min-width: 4rem;
    background: transparent;
    border-color: transparent;
  }
  /* EUROMOD ribbon buttons: flat until hovered, then a border and a 1px shadow. */
  .big-cmd:hover:not(:disabled) { border-color: var(--border-strong); }
  .page-intro { color: var(--muted); font-size: 0.85rem; }
  .inline { display: flex; align-items: center; gap: 0.4rem; white-space: nowrap; color: var(--muted); }
  .inline strong { color: var(--text); }
  .inline select { padding: 0.2rem 0.4rem; }
  .toggle { cursor: pointer; }
  .dot { width: 0.55rem; height: 0.55rem; border-radius: 50%; background: var(--border-strong); }
  .dot.on { background: var(--ok); }
  .dot.off { background: var(--err); }

  /* --- Content over the brand star --- */
  .content {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;
    padding: 1rem 1.2rem;
    gap: 0.9rem;
    position: relative;
    isolation: isolate;
    background: var(--bg);
  }
  .content::before {
    content: '';
    position: absolute;
    inset: 0;
    z-index: -1;
    background: var(--brand-bg) right center / auto 100% no-repeat;
    opacity: var(--brand-opacity);
    pointer-events: none;
  }
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

  /* --- Status bar --- */
  .statusbar {
    flex: none;
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.15rem 0.6rem;
    font-size: 0.78rem;
    background: var(--panel);
    border-top: 1px solid var(--border-strong);
  }

  @media (max-width: 1000px) {
    .page-group { display: none; }
    main.split { grid-template-columns: 1fr; overflow: auto; }
  }
</style>
