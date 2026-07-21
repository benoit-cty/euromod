<script>
  import { api } from './lib/api.js';
  import QueueList from './lib/components/QueueList.svelte';
  import DetailPanel from './lib/components/DetailPanel.svelte';
  import AuditLog from './lib/components/AuditLog.svelte';
  import DatabaseTab from './lib/components/DatabaseTab.svelte';
  import IngestTab from './lib/components/IngestTab.svelte';
  import EvalTab from './lib/components/EvalTab.svelte';
  import ParamsTab from './lib/components/ParamsTab.svelte';

  let config = $state({ data_dir: null, reviewer: 'reviewer', db_url: '', phoenix_endpoint: '' });
  let items = $state([]);
  let facets = $state(null);
  let selectedId = $state(null);
  let decisions = $state([]);
  let tab = $state('review');
  let error = $state('');
  let statusMsg = $state('');
  let dark = $state(localStorage.getItem('theme') === 'dark');

  const selected = $derived(items.find((i) => i.id === selectedId) ?? null);

  $effect(() => {
    document.body.classList.toggle('dark', dark);
    localStorage.setItem('theme', dark ? 'dark' : 'light');
  });

  async function init() {
    try {
      config = await api.getEnvConfig();
      if (config.data_dir) await refresh();
    } catch (e) {
      error = String(e);
    }
  }

  async function refresh() {
    try {
      const res = await api.loadQueue(config.data_dir);
      items = res.items;
      facets = res.facets;
      error = '';
    } catch (e) {
      error = String(e);
    }
  }

  async function decide(action, note, editedValue) {
    try {
      const updated = await api.saveDecision({
        data_dir: config.data_dir,
        item_id: selected.id,
        action,
        reviewer: config.reviewer,
        note: note || null,
        edited_value: editedValue ?? null,
      });
      items = items.map((i) => (i.id === updated.id ? updated : i));
      statusMsg = `${updated.id}: ${action}`;
    } catch (e) {
      error = String(e);
    }
  }

  async function exportAccepted() {
    try {
      const res = await api.exportAccepted(config.data_dir);
      statusMsg = `${res.count} record(s) exported to ${config.data_dir}/export`;
    } catch (e) {
      error = String(e);
    }
  }

  async function pickDir() {
    const res = await api.pickDataDir();
    if (!res.canceled) {
      config.data_dir = res.path;
      await refresh();
    }
  }

  // Jump from the Parameters tab to a freshly created review-queue item.
  async function openReviewItem(id) {
    await refresh();
    selectedId = id;
    tab = 'review';
  }

  async function showAudit() {
    tab = 'audit';
    try {
      const res = await api.loadDecisions(config.data_dir);
      decisions = res.decisions;
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
      <button class:primary={tab === 'review'} onclick={() => (tab = 'review')}>Review queue</button>
      <button class:primary={tab === 'params'} onclick={() => (tab = 'params')}>Parameters</button>
      <button class:primary={tab === 'audit'} onclick={showAudit}>Audit log</button>
      <button class:primary={tab === 'database'} onclick={() => (tab = 'database')}>Database</button>
      <button class:primary={tab === 'ingest'} onclick={() => (tab = 'ingest')}>Ingest</button>
      <button class:primary={tab === 'eval'} onclick={() => (tab = 'eval')}>Evaluation</button>
    </nav>
    <div class="spacer"></div>
    <label class="inline">
      Reviewer
      <input size="10" bind:value={config.reviewer} />
    </label>
    <button onclick={pickDir} title={config.data_dir ?? 'no data directory'}>Data dir…</button>
    <button onclick={refresh}>Reload</button>
    <button onclick={exportAccepted}>Export accepted</button>
    <button onclick={() => (dark = !dark)}>{dark ? '☀' : '☾'}</button>
  </header>

  {#if error}<div class="banner error">{error}</div>{/if}
  {#if statusMsg}<div class="banner">{statusMsg}</div>{/if}

  {#if tab === 'review'}
    <main>
      <QueueList {items} {facets} {selectedId} onselect={(id) => (selectedId = id)} />
      <DetailPanel item={selected} ondecide={decide} />
    </main>
  {:else if tab === 'params'}
    <main class="single">
      <ParamsTab
        dbUrl={config.db_url}
        phoenixEndpoint={config.phoenix_endpoint || 'http://localhost:6006'}
        onopenitem={openReviewItem}
      />
    </main>
  {:else if tab === 'audit'}
    <main class="single">
      <AuditLog {decisions} />
    </main>
  {:else if tab === 'database'}
    <main class="single">
      <DatabaseTab dbUrl={config.db_url} />
    </main>
  {:else if tab === 'ingest'}
    <main class="single">
      <IngestTab dbUrl={config.db_url} />
    </main>
  {:else}
    <main class="single">
      <EvalTab dbUrl={config.db_url} />
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
</style>
