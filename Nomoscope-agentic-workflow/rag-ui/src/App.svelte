<script>
  // Nomoscope RAG chat. Each question is one `chat` job: the worker runs an
  // agent with legislation search, article read and official-portal web
  // search, and returns the answer with its quotes checked verbatim against
  // the corpus. The app itself only reads the database and submits jobs
  // (ADR 0004); conversations are those jobs, reopened from ops.jobs.
  import { onMount, tick } from 'svelte';
  import AppShell from '@shared/components/AppShell.svelte';
  import Icon from '@shared/components/Icon.svelte';
  import { countryName } from '@shared/lib/labels.js';
  import ModelPicker from '@shared/components/ModelPicker.svelte';
  import { api, submitAndFollow, worker } from './lib/api.js';
  import { applyStep, buildMessages, CHAT_PRIORITY, COUNTRIES, newConversationId, todayIso } from './lib/chat.js';
  import ChunkCard from './lib/components/ChunkCard.svelte';
  import SearchPanel from './lib/components/SearchPanel.svelte';
  import Turn from './lib/components/Turn.svelte';
  import WebPanel from './lib/components/WebPanel.svelte';

  let config = $state({ db_url: '', user: null, db_error: null });
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

  const busy = $derived(turns.some((t) => t.status === 'queued' || t.status === 'running'));
  const panelTurn = $derived(selectedTurn !== null ? turns[selectedTurn] : null);
  const panelResult = $derived(panelTurn?.status === 'succeeded' ? panelTurn.result : null);
  const quotedIds = $derived(new Set((panelResult?.quotes ?? []).map((q) => q.chunk_id)));
  const otherSources = $derived((panelResult?.sources ?? []).filter((s) => !quotedIds.has(s.chunk_id)));
  const sourceById = $derived(Object.fromEntries((panelResult?.sources ?? []).map((s) => [s.chunk_id, s])));

  onMount(init);
  // One worker status for the chat (ribbon, model picker, offline warning).
  $effect(() => worker.poll(15000));

  async function init() {
    try {
      config = await api.getEnvConfig();
      if (config.db_error) {
        error = `Database unreachable: ${config.db_error}`;
        return;
      }
      await loadConversations();
    } catch (e) {
      error = String(e);
    }
  }

  async function loadConversations() {
    try {
      conversations = (await api.listConversations()).conversations;
    } catch {
      conversations = [];
    }
  }

  async function send(event) {
    event?.preventDefault();
    const question = input.trim();
    if (!question || busy || !config.user) return;
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
      const final = await submitAndFollow('chat', payload, {
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
    if (!id) return;
    try {
      await api.cancelJob(id);
    } catch (e) {
      error = `Could not stop job #${id}: ${e}`;
    }
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
      const res = await api.conversationTurns(id);
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

<AppShell
  logoTitle="Nómos: ask the legislation"
  themeKey="rag-theme"
  workerAlive={worker.alive}
  workerHint={{
    online: 'The worker that answers questions is online.',
    offline: 'No worker is running: questions wait in the queue until one starts.',
  }}
  user={config.user}
  userHint="Your database login: every question is recorded under it."
  bind:error
  status={busy
    ? 'Waiting for the answer…'
    : turns.length
      ? `${turns.length} question(s) in this conversation`
      : 'Ready'}
>
  {#snippet tabs()}
    <button class="tab active" role="tab" aria-selected="true">Ask the legislation</button>
  {/snippet}

  {#snippet ribbon()}
    <div class="group">
      <div class="cmds">
        <button class="big-cmd" onclick={newChat} disabled={busy} title="Start a new conversation">
          <Icon name="plus" size={24} />
          <span>New chat</span>
        </button>
        <button
          class="big-cmd"
          class:on={showHistory}
          onclick={() => (showHistory = !showHistory)}
          title="Show or hide your past conversations"
        >
          <Icon name="history" size={24} />
          <span>History</span>
        </button>
      </div>
      <div class="group-label">Conversation</div>
    </div>
    <div class="group">
      <div class="cmds settings">
        <label class="inline">
          Country
          <select bind:value={country}>
            <option value="">all</option>
            {#each COUNTRIES as c}<option value={c}>{countryName(c)}</option>{/each}
          </select>
        </label>
        <label class="inline">In force on <input type="date" bind:value={asOf} /></label>
        <label class="inline">
          Model
          <ModelPicker models={worker.llmModels} bind:value={model} emptyText="worker default" />
        </label>
        <label class="inline toggle">
          <input type="checkbox" bind:checked={web} />
          <Icon name="globe" size={15} /> Search official portals
        </label>
      </div>
      <div class="group-label">Next question</div>
    </div>
    <div class="group spacer"></div>
  {/snippet}

  {#if worker.alive === false}
    <div class="callout warn banner">
      <span>
        No worker is running — questions wait in the queue until one starts (<span class="mono">
          docker compose --profile gpu up -d
        </span>).
      </span>
    </div>
  {/if}

  <main class:with-history={showHistory}>
    {#if showHistory}
      <aside class="history panel">
        <h3>Conversations</h3>
        {#if !conversations.length}<p class="muted small">None yet.</p>{/if}
        <div class="convs">
          {#each conversations as c (c.conversation_id)}
            <button
              class="conv"
              class:on={c.conversation_id === conversationId}
              onclick={() => openConversation(c.conversation_id)}
            >
              <span class="title">{c.title ?? '(untitled)'}</span>
              <span class="muted small">
                {c.country ? countryName(c.country) : 'all countries'} · {c.turns} turn(s) · {c.last_at.slice(0, 16)}
              </span>
            </button>
          {/each}
        </div>
      </aside>
    {/if}

    <section class="chat panel">
      <div class="thread" bind:this={thread}>
        {#if !turns.length}
          <div class="empty-state">
            <Icon name="chat" size={32} />
            <div class="big">Ask the legislation</div>
            <p class="intro">
              Answers are grounded in the Nomotheca corpus: every quote is checked character-for-character against the
              cited article. When the corpus lacks a source, the assistant searches the official portals and lists the
              act so you can ingest it.
            </p>
            <ul class="small">
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
          placeholder={busy
            ? 'Waiting for the answer…'
            : 'Ask about a rate, a threshold, an article… (Enter to send, Shift+Enter for a new line)'}
          disabled={!config.user}></textarea>
        <button class="primary" disabled={busy || !input.trim()}><Icon name="send" size={15} /> Send</button>
      </form>
    </section>

    <aside class="side">
      <div class="side-tabs" role="tablist">
        <button
          class="tab"
          class:active={tab === 'sources'}
          role="tab"
          aria-selected={tab === 'sources'}
          onclick={() => (tab = 'sources')}
        >
          <Icon name="book" size={15} /> Sources{panelResult ? ` (${panelResult.sources.length})` : ''}
        </button>
        <button
          class="tab"
          class:active={tab === 'web'}
          role="tab"
          aria-selected={tab === 'web'}
          onclick={() => (tab = 'web')}
        >
          <Icon name="globe" size={15} /> Web{panelResult?.discoveries?.length
            ? ` · ${panelResult.discoveries.length} new`
            : ''}
        </button>
        <button
          class="tab"
          class:active={tab === 'search'}
          role="tab"
          aria-selected={tab === 'search'}
          onclick={() => (tab = 'search')}
        >
          <Icon name="search" size={15} /> Search
        </button>
      </div>
      <div class="side-body">
        <div hidden={tab !== 'sources'}>
          {#if !panelResult}
            <p class="muted">
              Sources of the selected answer appear here: quoted passages first, then everything the assistant
              retrieved.
            </p>
          {:else}
            {#if panelResult.quotes.length}<h3>Quoted</h3>{/if}
            {#each panelResult.quotes as q, i (i)}
              <ChunkCard
                chunk={sourceById[q.chunk_id] ?? {
                  chunk_id: q.chunk_id,
                  citation: q.citation,
                  validity: q.validity,
                  source_trust_class: q.source_trust_class,
                }}
                label={`[${i + 1}]`}
                extract={q.extract}
                verified={q.verified}
                active={selectedQuote === i}
                open={selectedQuote === i}
              />
            {/each}
            {#if otherSources.length}<h3>Also retrieved</h3>{/if}
            {#each otherSources as s (s.chunk_id)}
              <ChunkCard chunk={s} />
            {/each}
          {/if}
        </div>
        <div hidden={tab !== 'web'}>
          <WebPanel result={panelResult} />
        </div>
        <div hidden={tab !== 'search'}>
          <SearchPanel {country} {asOf} />
        </div>
      </div>
    </aside>
  </main>
</AppShell>

<style>
  /* What the chat adds to the shared shell (@shared/shell.css). */
  .cmds.settings {
    display: grid;
    grid-template-columns: auto auto;
    gap: 0.35rem 1rem;
    align-items: center;
  }
  .settings select {
    max-width: 16rem;
  }

  main {
    flex: 1;
    min-height: 0;
    display: grid;
    grid-template-columns: minmax(0, 3fr) minmax(340px, 2fr);
    gap: 1rem;
  }
  main.with-history {
    grid-template-columns: 260px minmax(0, 3fr) minmax(340px, 2fr);
  }

  .history {
    display: flex;
    flex-direction: column;
    min-height: 0;
    padding: 0.9rem;
  }
  .convs {
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 2px;
    margin: 0 -0.3rem;
    padding: 0 0.3rem;
  }
  .conv {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.1rem;
    width: 100%;
    text-align: left;
    background: transparent;
    border-color: transparent;
    border-radius: 9px;
    padding: 0.5rem 0.7rem;
  }
  .conv:hover:not(:disabled) {
    background: var(--panel-2);
    border-color: transparent;
    box-shadow: none;
  }
  .conv.on,
  .conv.on:hover:not(:disabled) {
    background: var(--accent-soft);
    border-color: var(--accent);
  }
  .conv .title {
    font-weight: 600;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 100%;
  }

  .chat {
    display: flex;
    flex-direction: column;
    min-height: 0;
    padding: 0;
    overflow: hidden;
  }
  .thread {
    flex: 1;
    overflow-y: auto;
    padding: 1rem 1.2rem;
  }
  .empty-state {
    max-width: 40rem;
    margin: 2rem auto;
  }
  .empty-state .intro {
    margin: 0;
  }
  .empty-state ul {
    text-align: left;
    margin: 0.4rem 0 0;
  }
  .empty-state li {
    margin: 0.3rem 0;
    font-style: italic;
  }
  .composer {
    display: flex;
    gap: 0.5rem;
    padding: 0.6rem 0.8rem;
    border-top: 1px solid var(--border);
    background: var(--panel-2);
  }
  .composer textarea {
    flex: 1;
    resize: vertical;
    min-height: 2.6rem;
  }

  /* Source panel: EUROMOD tabs over a panel. */
  .side {
    display: flex;
    flex-direction: column;
    min-height: 0;
  }
  .side-tabs {
    display: flex;
    gap: 3px;
    padding-left: 0.5rem;
  }
  .side-tabs .tab {
    padding: 0.4rem 0.8rem;
  }
  .side-tabs .tab.active {
    padding-bottom: calc(0.4rem + 1px);
  }
  .side-body {
    flex: 1;
    overflow-y: auto;
    padding: 0.8rem;
    background: var(--panel-glass);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
  }
  .side-body h3 {
    margin: 0.4rem 0;
  }

  @media (max-width: 1000px) {
    main,
    main.with-history {
      grid-template-columns: 1fr;
      overflow: auto;
    }
  }
</style>
