<script>
  // Nomoscope RAG chat. Each question is one `chat` job: the worker runs an
  // agent with legislation search, article read and official-portal web
  // search, and returns the answer with its quotes checked verbatim against
  // the corpus. The app itself only reads the database and submits jobs
  // (ADR 0004); conversations are those jobs, reopened from ops.jobs.
  import { onMount, tick } from 'svelte';
  import { api } from './lib/api.js';
  import { applyStep, buildMessages, CHAT_PRIORITY, COUNTRIES, newConversationId, todayIso } from './lib/chat.js';
  import { submitAndFollow } from './lib/jobs.js';
  import ChunkCard from './lib/components/ChunkCard.svelte';
  import SearchPanel from './lib/components/SearchPanel.svelte';
  import Turn from './lib/components/Turn.svelte';
  import WebPanel from './lib/components/WebPanel.svelte';

  let config = $state({ db_url: '', user: null, db_error: null });
  let worker = $state({ alive: null, models: [] });
  let error = $state('');

  // Settings of the next question (each turn records its own).
  let country = $state('FR');
  let asOf = $state(todayIso());
  let model = $state('');
  let web = $state(true);

  let conversationId = $state(newConversationId());
  let turns = $state([]);
  let input = $state('');
  let conversations = $state([]);
  let showHistory = $state(false);

  // Source panel: which turn, which quote, which tab.
  let selectedTurn = $state(null);
  let selectedQuote = $state(null);
  let tab = $state('sources');
  let thread = $state(null);

  let dark = $state(readTheme());

  const busy = $derived(turns.some((t) => t.status === 'queued' || t.status === 'running'));
  const llmModels = $derived(worker.models.filter((m) => m.kind === 'llm'));
  const panelTurn = $derived(selectedTurn !== null ? turns[selectedTurn] : null);
  const panelResult = $derived(panelTurn?.status === 'succeeded' ? panelTurn.result : null);
  const quotedIds = $derived(new Set((panelResult?.quotes ?? []).map((q) => q.chunk_id)));
  const otherSources = $derived((panelResult?.sources ?? []).filter((s) => !quotedIds.has(s.chunk_id)));
  const sourceById = $derived(Object.fromEntries((panelResult?.sources ?? []).map((s) => [s.chunk_id, s])));

  function readTheme() {
    try {
      return localStorage.getItem('rag-theme') === 'dark';
    } catch {
      return false;
    }
  }

  $effect(() => {
    document.body.classList.toggle('dark', dark);
    try {
      localStorage.setItem('rag-theme', dark ? 'dark' : 'light');
    } catch {
      /* private window: the theme just isn't remembered */
    }
  });

  onMount(() => {
    init();
    const timer = setInterval(refreshWorker, 15000);
    return () => clearInterval(timer);
  });

  async function init() {
    try {
      config = await api.getEnvConfig();
      if (config.db_error) {
        error = `Database unreachable: ${config.db_error}`;
        return;
      }
      await refreshWorker();
      await loadConversations();
    } catch (e) {
      error = String(e);
    }
  }

  async function refreshWorker() {
    if (!config.db_url || config.db_error) return;
    try {
      const res = await api.workerStatus(config.db_url);
      worker = { alive: res.workers.some((w) => w.alive), models: res.models };
      if (!model || !worker.models.some((m) => m.model === model)) {
        model = (llmModels.find((m) => m.is_default) ?? llmModels[0])?.model ?? '';
      }
    } catch (e) {
      worker = { alive: null, models: [] };
    }
  }

  async function loadConversations() {
    try {
      conversations = (await api.listConversations(config.db_url)).conversations;
    } catch {
      conversations = [];
    }
  }

  async function send(event) {
    event?.preventDefault();
    const question = input.trim();
    if (!question || busy || !config.db_url) return;
    const payload = {
      conversation_id: conversationId,
      messages: buildMessages(turns, question),
      country: country || null,
      as_of: asOf || null,
      model: model || null,
      web,
    };
    turns.push({ question, status: 'queued', steps: [], result: null, error: null, jobId: null });
    const index = turns.length - 1;
    input = '';
    await scrollDown();
    try {
      const final = await submitAndFollow(config.db_url, 'chat', payload, {
        priority: CHAT_PRIORITY,
        onSubmit: (id) => (turns[index].jobId = id),
        onProgress: (data) => {
          applyStep(turns[index].steps, data);
          scrollDown();
        },
        onStatus: (row) => (turns[index].status = row.status),
      });
      turns[index].result = final.result;
      turns[index].error = final.error;
      turns[index].status = final.status === 'succeeded' && !final.result ? 'failed' : final.status;
      if (turns[index].status === 'succeeded') select(index, (final.result.quotes ?? []).length ? 0 : null);
    } catch (e) {
      turns[index].status = 'failed';
      turns[index].error = String(e);
    }
    await scrollDown();
    loadConversations();
  }

  async function cancel(index) {
    const id = turns[index].jobId;
    if (id) await api.cancelJob(config.db_url, id).catch((e) => (error = String(e)));
  }

  function select(index, quote = null) {
    selectedTurn = index;
    selectedQuote = quote;
    tab = 'sources';
  }

  async function scrollDown() {
    await tick();
    thread?.scrollTo({ top: thread.scrollHeight, behavior: 'smooth' });
  }

  function newChat() {
    if (busy) return;
    conversationId = newConversationId();
    turns = [];
    selectedTurn = null;
    selectedQuote = null;
    showHistory = false;
  }

  async function openConversation(id) {
    if (busy) return;
    try {
      const res = await api.conversationTurns(config.db_url, id);
      conversationId = id;
      turns = res.turns.map((t) => ({
        question: t.question,
        status: t.status === 'succeeded' && !t.result ? 'failed' : t.status,
        steps: [],
        result: t.result,
        error: t.error,
        jobId: t.job_id,
      }));
      const last = res.turns.at(-1)?.settings;
      if (last) {
        country = last.country ?? '';
        if (last.as_of) asOf = last.as_of;
        web = last.web ?? true;
      }
      const lastOk = turns.findLastIndex((t) => t.status === 'succeeded');
      selectedTurn = lastOk >= 0 ? lastOk : null;
      selectedQuote = null;
      showHistory = false;
      await scrollDown();
    } catch (e) {
      error = String(e);
    }
  }

  function onKeydown(event) {
    if (event.key === 'Enter' && !event.shiftKey) send(event);
  }
</script>

<div class="app">
  <header class="top">
    <h1>Nomoscope <span class="muted">RAG chat</span></h1>
    <label>Country
      <select bind:value={country}>
        <option value="">all</option>
        {#each COUNTRIES as c}<option value={c}>{c}</option>{/each}
      </select>
    </label>
    <label>In force on <input type="date" bind:value={asOf} /></label>
    <label>Model
      <select bind:value={model} disabled={!llmModels.length}>
        {#if !llmModels.length}<option value="">worker default</option>{/if}
        {#each llmModels as m (m.model)}<option value={m.model}>{m.model}{m.is_default ? ' (default)' : ''}</option>{/each}
      </select>
    </label>
    <label class="check"><input type="checkbox" bind:checked={web} /> Web search</label>
    <span class="spacer"></span>
    <span class="badge {worker.alive ? 'ok' : worker.alive === false ? 'err' : ''}" title="ops.workers heartbeat">
      worker {worker.alive ? 'online' : worker.alive === false ? 'offline' : '…'}
    </span>
    {#if config.user}<span class="muted small">{config.user}</span>{/if}
    <button onclick={() => (showHistory = !showHistory)}>History</button>
    <button onclick={newChat} disabled={busy}>New chat</button>
    <button onclick={() => (dark = !dark)} title="Toggle theme">{dark ? '☀' : '☾'}</button>
  </header>

  {#if error}<div class="banner err">{error}</div>{/if}
  {#if worker.alive === false}
    <div class="banner warn">No worker is running — questions wait in the queue until one starts (<span class="mono">docker compose --profile gpu up -d</span>).</div>
  {/if}

  <main>
    {#if showHistory}
      <aside class="history">
        <h2>Conversations</h2>
        {#if !conversations.length}<p class="muted small">None yet.</p>{/if}
        {#each conversations as c (c.conversation_id)}
          <button class="conv" class:on={c.conversation_id === conversationId} onclick={() => openConversation(c.conversation_id)}>
            <span class="title">{c.title ?? '(untitled)'}</span>
            <span class="muted small">{c.country ?? 'all'} · {c.turns} turn(s) · {c.last_at.slice(0, 16)}</span>
          </button>
        {/each}
      </aside>
    {/if}

    <section class="chat">
      <div class="thread" bind:this={thread}>
        {#if !turns.length}
          <div class="empty">
            <h2>Ask the legislation</h2>
            <p class="muted">
              Answers are grounded in the Nomotheca corpus: every quote is checked character-for-character
              against the cited article. When the corpus lacks a source, the assistant searches the official
              portals and lists the act so you can ingest it.
            </p>
            <ul class="muted small">
              <li>Quel est le barème de l'impôt sur le revenu applicable aux revenus 2024 ?</li>
              <li>What is the Irish standard rate cut-off point for a single person in 2025?</li>
              <li>¿Qué escala autonómica del IRPF aplica Aragón en 2025?</li>
            </ul>
          </div>
        {/if}
        {#each turns as turn, i (i)}
          <Turn
            {turn}
            selected={selectedTurn === i}
            {selectedQuote}
            onSelect={() => turn.status === 'succeeded' && (selectedTurn = i)}
            onSelectQuote={(q) => select(i, q)}
            onCancel={() => cancel(i)}
          />
        {/each}
      </div>
      <form class="composer" onsubmit={send}>
        <textarea
          bind:value={input}
          onkeydown={onKeydown}
          rows="2"
          placeholder={busy ? 'Waiting for the answer…' : 'Ask about a rate, a threshold, an article… (Enter to send, Shift+Enter for a new line)'}
          disabled={!config.db_url || !!config.db_error}
        ></textarea>
        <button class="primary" disabled={busy || !input.trim()}>Send</button>
      </form>
    </section>

    <aside class="panel">
      <nav>
        <button class:on={tab === 'sources'} onclick={() => (tab = 'sources')}>
          Sources{panelResult ? ` (${panelResult.sources.length})` : ''}
        </button>
        <button class:on={tab === 'web'} onclick={() => (tab = 'web')}>
          Web{panelResult?.discoveries?.length ? ` · ${panelResult.discoveries.length} new` : ''}
        </button>
        <button class:on={tab === 'search'} onclick={() => (tab = 'search')}>Search</button>
      </nav>
      <div class="panel-body">
        <div hidden={tab !== 'sources'}>
          {#if !panelResult}
            <p class="muted">Sources of the selected answer appear here: quoted passages first, then everything the assistant retrieved.</p>
          {:else}
            {#if panelResult.quotes.length}<h3>Quoted</h3>{/if}
            {#each panelResult.quotes as q, i (i)}
              <ChunkCard
                chunk={sourceById[q.chunk_id] ?? { chunk_id: q.chunk_id, citation: q.citation, validity: q.validity, source_trust_class: q.source_trust_class }}
                dbUrl={config.db_url}
                label={`[${i + 1}]`}
                extract={q.extract}
                verified={q.verified}
                active={selectedQuote === i}
                open={selectedQuote === i}
              />
            {/each}
            {#if otherSources.length}<h3>Also retrieved</h3>{/if}
            {#each otherSources as s (s.chunk_id)}
              <ChunkCard chunk={s} dbUrl={config.db_url} />
            {/each}
          {/if}
        </div>
        <div hidden={tab !== 'web'}>
          <WebPanel result={panelResult} dbUrl={config.db_url} />
        </div>
        <div hidden={tab !== 'search'}>
          <SearchPanel dbUrl={config.db_url} {country} {asOf} />
        </div>
      </div>
    </aside>
  </main>
</div>

<style>
  .app { display: flex; flex-direction: column; height: 100%; }
  .top {
    display: flex; align-items: center; gap: 0.9rem; flex-wrap: wrap;
    padding: 0.5rem 1rem; background: var(--panel); border-bottom: 1px solid var(--border);
  }
  .top h1 { margin: 0; font-size: 1.05rem; }
  .top label { display: flex; align-items: center; gap: 0.35rem; font-size: 0.9em; }
  .spacer { flex: 1; }
  .app > .banner { margin: 0.5rem 1rem 0; }
  main { flex: 1; min-height: 0; display: flex; }
  .history {
    width: 260px; flex-shrink: 0; overflow-y: auto; padding: 0.7rem;
    border-right: 1px solid var(--border); background: var(--panel);
  }
  .history h2 { font-size: 0.95rem; }
  .conv {
    display: flex; flex-direction: column; align-items: flex-start; gap: 0.1rem;
    width: 100%; text-align: left; margin-bottom: 0.35rem; background: none;
  }
  .conv.on { border-color: var(--accent); background: var(--accent-soft); }
  .conv .title { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 100%; }
  .chat { flex: 1; min-width: 0; display: flex; flex-direction: column; }
  .thread { flex: 1; overflow-y: auto; padding: 1rem 1.2rem; }
  .empty { max-width: 40rem; margin: 3rem auto; }
  .empty li { margin: 0.3rem 0; }
  .composer {
    display: flex; gap: 0.5rem; padding: 0.6rem 1rem;
    border-top: 1px solid var(--border); background: var(--panel);
  }
  .composer textarea { flex: 1; resize: vertical; min-height: 2.6rem; }
  .panel {
    width: 40%; max-width: 640px; min-width: 340px; display: flex; flex-direction: column;
    border-left: 1px solid var(--border); background: var(--bg);
  }
  .panel nav { display: flex; gap: 0.3rem; padding: 0.5rem 0.7rem 0; }
  .panel nav button { border-radius: 6px 6px 0 0; border-bottom: none; }
  .panel nav button.on { background: var(--panel); border-color: var(--accent); color: var(--accent); }
  .panel-body { flex: 1; overflow-y: auto; padding: 0.7rem; border-top: 1px solid var(--border); }
  .panel-body h3 { font-size: 0.9rem; margin: 0.4rem 0; }
</style>
