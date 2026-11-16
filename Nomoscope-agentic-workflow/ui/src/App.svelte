<script>
  import { api, worker } from './lib/api.js';
  import { library } from './lib/library.svelte.js';
  import AppShell from '@shared/components/AppShell.svelte';
  import Icon from '@shared/components/Icon.svelte';
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
  // and `reviewer` is that login's current_user as the server sees it. The
  // URL stays in Rust; `db_url` here is for display (password masked).
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
  // True until the first queue load answers (931 items take a few seconds):
  // the Overview and the review list show a loader instead of "nothing yet".
  let queueLoading = $state(true);
  let facets = $state(null);
  let selectedId = $state(null);
  let decisions = $state([]);
  let tab = $state('home');
  // Pages are kept alive once visited (hidden, not destroyed): switching away
  // must not lose a followed job's log or reset filters/selections.
  let visited = $state({ home: true });
  let paramsRunning = $state(false);
  // Bumped when the app is pointed at another database: every page is
  // remounted, so none keeps rows read from the previous one.
  let dbGeneration = $state(0);
  let error = $state('');
  let statusMsg = $state('');
  const stored = (key) => {
    try {
      return localStorage.getItem(key);
    } catch {
      return null;
    }
  };
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
    try {
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
    queueLoading = false;
    try {
      const res = await api.phoenixProjects();
      const project =
        res.projects.find((p) => p.name === config.phoenix_project) ?? res.projects[0];
      phoenixGid = project?.gid ?? '';
    } catch {
      phoenixGid = ''; // Phoenix links degrade to the projects page
    }
  }

  // One worker status for the whole app (ribbon, pickers, badges).
  $effect(() => worker.poll(15000));

  async function refresh() {
    try {
      const res = await api.loadQueue();
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
        item_id: selected.id,
        // The run on screen: a decision on an item re-run since is refused.
        run_id: selected.run_id ?? null,
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
      const res = await api.exportChanges();
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

  // The one way to change database (Legislation and Evaluation pages offer
  // it): checked by the backend first, then the whole app is reloaded on it.
  async function changeDb(url) {
    const res = await api.setDbUrl(url);
    config.db_url = res.db_url;
    config.reviewer = res.reviewer;
    config.db_error = null;
    error = '';
    items = [];
    decisions = [];
    selectedId = null;
    visited = { home: true, [tab]: true };
    library.reset();
    dbGeneration += 1;
    queueLoading = true;
    await refresh();
    queueLoading = false;
    worker.refresh();
    statusMsg = `Connected to ${res.db_url} as ${res.reviewer}.`;
  }

  async function loadDecisions() {
    const res = await api.loadDecisions();
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
      worker.refresh();
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

<AppShell
  logoTitle="Nómos: EUROMOD parameter review"
  themeKey="theme"
  workerAlive={worker.alive}
  workerHint={{
    online: 'The worker that runs checks, searches and imports is online.',
    offline: 'No worker is running: submitted work waits in the queue until one starts.',
  }}
  user={config.reviewer}
  userHint="Your database login: every decision and job is recorded under it."
  bind:error
  status={pendingCount ? `${pendingCount} proposal(s) waiting for review` : 'Ready'}
>
  {#snippet tabs()}
    {#each PAGES.filter((p) => !p.expert) as p (p.id)}{@render navItem(p)}{/each}
    {#if expert}
      {#each PAGES.filter((p) => p.expert) as p (p.id)}{@render navItem(p)}{/each}
    {/if}
  {/snippet}

  {#snippet ribbon()}
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
  {/snippet}

  {#snippet display()}
    <label class="inline toggle">
      <input type="checkbox" bind:checked={expert} />
      <Icon name="tools" size={15} /> Show expert tools
    </label>
  {/snippet}

  {#if statusMsg}
    <div class="callout ok banner"><span>{statusMsg}</span></div>
  {/if}

  {#key dbGeneration}
  <main hidden={tab !== 'home'} class="single">
    <Home
      bind:this={homePage}
      {items}
      loading={queueLoading}
      reviewer={config.reviewer}
      onnavigate={go}
      onexport={exportChanges}
    />
  </main>
  {#if visited.review}
    <main class="split" hidden={tab !== 'review'}>
      <QueueList {items} {facets} loading={queueLoading} {selectedId} onselect={(id) => (selectedId = id)} />
      <DetailPanel
        item={selected}
        {siblings}
        onselectrun={(id) => (selectedId = id)}
        ondecide={decide}
        phoenixEndpoint={config.phoenix_endpoint || 'http://localhost:6006'}
        {phoenixGid}
      />
    </main>
  {/if}
  {#if visited.params}
    <main class="single" hidden={tab !== 'params'}>
      <ParamsTab
        bind:this={paramsTab}
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
      <DatabaseTab bind:this={dbTab} dbUrl={config.db_url} onchangedb={changeDb} />
    </main>
  {/if}
  {#if visited.ingest}
    <main class="single" hidden={tab !== 'ingest'}>
      <IngestTab />
    </main>
  {/if}
  {#if visited.golden}
    <main class="single" hidden={tab !== 'golden'}>
      <GoldenTab bind:this={goldenTab} />
    </main>
  {/if}
  {#if visited.eval}
    <main class="single" hidden={tab !== 'eval'}>
      <EvalTab bind:this={evalTab} dbUrl={config.db_url} onchangedb={changeDb} />
    </main>
  {/if}
  {#if visited.impact}
    <main class="single" hidden={tab !== 'impact'}>
      <ImpactTab bind:this={impactTab} />
    </main>
  {/if}
  {#if visited.jobs}
    <main class="single" hidden={tab !== 'jobs'}>
      <JobsTab bind:this={jobsTab} active={tab === 'jobs'} />
    </main>
  {/if}
  {/key}
</AppShell>

<style>
  /* What the review UI adds to the shared shell (@shared/shell.css). */
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
  .group.page-group { flex: 1 1 18rem; min-width: 14rem; }
  .page-intro { color: var(--muted); font-size: 0.85rem; }

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
    .group.page-group { display: none; }
    main.split { grid-template-columns: 1fr; overflow: auto; }
  }
</style>
