<script>
  import { onMount } from 'svelte';
  import { api } from '../api.js';

  let { dbUrl = '' } = $props();

  let url = $state(''); // seeded from dbUrl by the $effect below once config loads
  let sub = $state('ingestion'); // ingestion | document | embeddings | translation

  // --- ingestion form ---
  let ingMode = $state('instrument'); // instrument | citation
  let jurisdiction = $state('fr');
  let nationalId = $state('');
  let citationText = $state('');
  let asOf = $state('');
  let sourceCode = $state('');
  let maxItems = $state(500);

  // --- contributed-document form ---
  // A reviewer pastes a URL or picks a file and states what the document is.
  // The class is never stated: it follows from the kind (ADR 0001).
  let docSource = $state('');          // URL or local file path
  let docJurisdiction = $state('fr');
  let docLang = $state('fr');
  let docTitle = $state('');
  let docKind = $state('circulaire');
  let docValidFrom = $state('');
  let docImplements = $state('');      // '' = none
  let implementsQuery = $state('');
  let implementsResults = $state([]);
  // Both filled from the store / the ingester; the seeds only cover the moment
  // before those answer.
  let languages = $state(['en']);
  let jurisdictions = $state(['FR']);
  // jurisdiction -> { kind: { norm_level, source_trust_class } }, straight from
  // the ingester's own table (`route`), so the UI keeps no copy of the mapping.
  let kindTable = $state({});
  let routeOutcome = $state(null);     // { outcome, source, national_id, hint, ... }
  let routing = $state(false);

  let docKinds = $derived(
    Object.keys(kindTable[docJurisdiction.toUpperCase()] ?? {}).length
      ? kindTable[docJurisdiction.toUpperCase()]
      : (kindTable.DEFAULT ?? {})
  );
  let docTrustClass = $derived(docKinds[docKind]?.source_trust_class ?? '');
  // An adapter outcome supplies every field itself: the contributed fields are
  // hidden and the instrument command runs instead.
  let switchingToAdapter = $derived(routeOutcome?.outcome === 'adapter');
  let docReady = $derived(
    switchingToAdapter
      ? true
      : Boolean(
          docSource.trim() &&
            docJurisdiction.trim() &&
            docLang.trim() &&
            docTitle.trim() &&
            // A kind this jurisdiction actually offers: `circulaire` is not an
            // ES label, and the CLI would refuse it after the run had started.
            docKinds[docKind] &&
            docValidFrom &&
            routeOutcome?.outcome !== 'refused'
        )
  );

  // --- embeddings form ---
  let modelPath = $state('models/bge-m3-openvino');
  let backend = $state('openvino'); // torch | openvino
  let device = $state('');
  let modelId = $state(1);
  let batchSize = $state(16);
  let embLimit = $state('');
  let embDryRun = $state(false);

  // --- translation form ---
  let model = $state('azure_openai/gpt-5.6-luna');
  let targetLang = $state('en');
  let trLimit = $state('');
  let requestTimeout = $state(120);
  let trDryRun = $state(false);

  // --- run state ---
  let running = $state(false);
  let runId = $state('');
  let logLines = $state([]);
  let summary = $state('');
  let error = $state('');
  let logEl;

  // --- progress state ---
  // The CLI is run with --progress-json (embeddings/translate), which prints
  // machine-readable "@progress {json}" lines on stdout. We pull those out of
  // the log stream and render a real bar; ingestion runs (no totals) get an
  // indeterminate activity bar + elapsed time instead.
  const PROGRESS_PREFIX = '@progress ';
  let progress = $state(null); // { task, phase, done, total, translated?, embedded?, failed?, detail }
  let startedAt = $state(0);
  let now = $state(0);
  let elapsed = $derived(startedAt ? Math.max(0, Math.floor((now - startedAt) / 1000)) : 0);
  let pct = $derived(
    progress ? (progress.total > 0 ? Math.min(100, Math.round((progress.done / progress.total) * 100)) : 100) : 0
  );

  $effect(() => {
    if (dbUrl && !url) url = dbUrl;
  });

  // The vocabulary the store actually has: languages it is configured to index
  // (a text stored under any other is invisible to full-text search) and the
  // jurisdictions it holds.
  $effect(() => {
    if (!url.trim()) return;
    api
      .dbStats(url.trim())
      .then((stats) => {
        if (stats?.languages?.length) languages = stats.languages;
        const codes = (stats?.by_country ?? []).map((row) => row.code).filter(Boolean);
        if (codes.length) jurisdictions = codes;
      })
      .catch(() => {});
  });

  // Tick the elapsed clock while a run is active.
  $effect(() => {
    if (!running) return;
    const t = setInterval(() => (now = Date.now()), 1000);
    return () => clearInterval(t);
  });

  // The kinds each jurisdiction offers, and the class each one implies, come
  // from the ingester so the two can never drift. `route` with no source
  // answers with the table alone, so the Kind select is populated before the
  // reviewer has pasted anything.
  async function loadKindTable() {
    const outcome = await routeSource();
    if (outcome?.kinds) kindTable = outcome.kinds;
  }

  onMount(() => {
    loadKindTable().catch(() => {});
    const unlistenP = api.onIngestLog((payload) => {
      if (payload.run_id !== runId) return; // only the active run
      if (payload.stream === 'stdout' && payload.line.startsWith(PROGRESS_PREFIX)) {
        try {
          progress = JSON.parse(payload.line.slice(PROGRESS_PREFIX.length));
          return; // progress lines feed the bar, not the log
        } catch {
          // fall through: show the malformed line in the log
        }
      }
      logLines = [...logLines, payload];
    });
    return () => unlistenP.then((un) => un());
  });

  // Auto-scroll the log to the bottom as lines arrive.
  $effect(() => {
    logLines.length;
    if (logEl) logEl.scrollTop = logEl.scrollHeight;
  });

  // Ask the ingester what this input is, before any run starts: prefill for a
  // contributed document, announce-and-switch for a known official source, a
  // hint for something we will not ingest this way.
  // One `route` run, read off the log stream: the CLI prints exactly one JSON
  // line, and going through runIngest keeps every child process on the one
  // spawn/cancel path.
  async function routeSource(source) {
    const lines = [];
    const id = crypto.randomUUID();
    const unlisten = await api.onIngestLog((payload) => {
      if (payload.run_id === id && payload.stream === 'stdout') lines.push(payload.line);
    });
    try {
      await api.runIngest({
        run_id: id,
        command: 'route',
        db_url: url.trim(),
        args: source ? [source] : [],
      });
      const last = [...lines].reverse().find((line) => line.trim().startsWith('{'));
      return last ? JSON.parse(last) : null;
    } finally {
      unlisten();
    }
  }

  async function precheckSource() {
    const source = docSource.trim();
    routeOutcome = null;
    if (!source) return;
    routing = true;
    try {
      routeOutcome = await routeSource(source);
      if (routeOutcome?.kinds) kindTable = routeOutcome.kinds;
      const suggestions = routeOutcome?.suggestions ?? {};
      if (suggestions.title && !docTitle.trim()) docTitle = suggestions.title;
      if (suggestions.valid_from && !docValidFrom) docValidFrom = suggestions.valid_from;
    } catch (e) {
      error = String(e);
    } finally {
      routing = false;
    }
  }

  // Changing the country changes the words: an ES document is not a
  // `circulaire`. Fall back to the first kind the new jurisdiction offers.
  function onJurisdictionChange() {
    if (!docKinds[docKind]) docKind = Object.keys(docKinds)[0] ?? '';
    implementsResults = [];
    docImplements = '';
  }

  async function pickDocumentFile() {
    const { open } = await import('@tauri-apps/plugin-dialog');
    const picked = await open({
      multiple: false,
      filters: [{ name: 'Documents', extensions: ['pdf', 'html', 'htm', 'md', 'markdown', 'txt'] }],
    });
    if (typeof picked === 'string') {
      docSource = picked;
      await precheckSource();
    }
  }

  async function searchInstruments() {
    if (!implementsQuery.trim()) {
      implementsResults = [];
      return;
    }
    try {
      const res = await api.searchInstruments(url.trim(), docJurisdiction.trim(), implementsQuery.trim());
      implementsResults = res.instruments ?? [];
    } catch (e) {
      error = String(e);
    }
  }

  function documentArgs() {
    return [
      docSource.trim(),
      '--jurisdiction', docJurisdiction.trim(),
      '--lang', docLang.trim(),
      '--title', docTitle.trim(),
      '--kind', docKind,
      '--valid-from', docValidFrom,
      ...(docImplements ? ['--implements', docImplements] : []),
      '--progress-json',
    ];
  }

  function embeddingArgs() {
    const args = [
      '--model-path', modelPath.trim(),
      '--backend', backend,
      '--model-id', String(modelId),
      '--batch-size', String(batchSize),
      '--progress-json',
    ];
    if (device.trim()) args.push('--device', device.trim());
    return args;
  }

  // Build the CLI command + args for the active sub-tab.
  function buildRequest() {
    if (sub === 'ingestion') {
      const args = [];
      if (ingMode === 'instrument') {
        if (!jurisdiction.trim() || !nationalId.trim())
          throw new Error('jurisdiction and national id are required');
        args.push(jurisdiction.trim(), nationalId.trim());
      } else {
        if (!jurisdiction.trim() || !citationText.trim() || !asOf)
          throw new Error('jurisdiction, citation and as-of date are required');
        args.push(jurisdiction.trim(), citationText.trim(), asOf);
      }
      if (sourceCode.trim()) args.push('--source-code', sourceCode.trim());
      args.push('--max-items', String(maxItems));
      return { command: ingMode, args };
    }
    if (sub === 'document') {
      if (!docSource.trim()) throw new Error('paste a URL or pick a file first');
      if (routeOutcome?.outcome === 'refused') throw new Error(routeOutcome.hint);
      // A known official source is ingested by its adapter, from its national
      // id — never as a page. The library re-routes anyway; this only keeps
      // the log honest about which command actually ran.
      if (switchingToAdapter) {
        return {
          command: 'instrument',
          args: [routeOutcome.jurisdiction, routeOutcome.national_id, '--max-items', String(maxItems)],
        };
      }
      if (!docValidFrom) throw new Error('a validity start date is required');
      return { command: 'document', args: documentArgs() };
    }
    if (sub === 'embeddings') {
      const args = embeddingArgs();
      if (String(embLimit).trim()) args.push('--limit', String(embLimit).trim());
      if (embDryRun) args.push('--dry-run');
      return { command: 'embeddings', args };
    }
    // translation
    const args = [
      '--model', model.trim(),
      '--target-lang', targetLang.trim(),
      '--progress-json',
    ];
    if (String(requestTimeout).trim()) args.push('--request-timeout', String(requestTimeout).trim());
    if (String(trLimit).trim()) args.push('--limit', String(trLimit).trim());
    if (trDryRun) args.push('--dry-run');
    return { command: 'translate', args };
  }

  async function run() {
    error = '';
    summary = '';
    if (!url.trim()) {
      error = 'Database URL is required';
      return;
    }
    let req;
    try {
      req = buildRequest();
    } catch (e) {
      error = String(e.message ?? e);
      return;
    }
    runId = crypto.randomUUID();
    logLines = [];
    progress = null;
    startedAt = Date.now();
    now = startedAt;
    running = true;
    try {
      const res = await api.runIngest({
        run_id: runId,
        command: req.command,
        db_url: url.trim(),
        args: req.args,
      });
      if (res.canceled) summary = 'Canceled.';
      else if (res.success) summary = 'Finished successfully.';
      else summary = `Exited with code ${res.code ?? '?'}.`;
      // A contributed document is only retrievable once its chunks are
      // embedded, so the ingester chains the build itself (ingest.rs decides;
      // a failed run chains nothing).
      if (res.follow_up === 'embeddings') await runFollowUpEmbeddings();
    } catch (e) {
      error = String(e);
    } finally {
      running = false;
    }
  }

  async function runFollowUpEmbeddings() {
    summary = 'Document loaded. Building embeddings for the new chunks…';
    runId = crypto.randomUUID();
    progress = null;
    startedAt = Date.now();
    now = startedAt;
    const res = await api.runIngest({
      run_id: runId,
      command: 'embeddings',
      db_url: url.trim(),
      args: embeddingArgs(),
    });
    summary = res.success
      ? 'Finished successfully; the document is retrievable.'
      : `Document loaded, but the embeddings build exited with code ${res.code ?? '?'}.`;
  }

  async function stop() {
    if (runId) await api.stopIngest(runId);
  }

  function fmtElapsed(seconds) {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return m ? `${m}m ${String(s).padStart(2, '0')}s` : `${s}s`;
  }
</script>

<section class="panel ingest">
  <div class="row">
    <label class="grow">
      Database URL
      <input bind:value={url} class="mono" />
    </label>
  </div>

  <nav class="subtabs">
    <button class:primary={sub === 'ingestion'} onclick={() => (sub = 'ingestion')}>Ingestion</button>
    <button class:primary={sub === 'document'} onclick={() => (sub = 'document')}>Contributed document</button>
    <button class:primary={sub === 'embeddings'} onclick={() => (sub = 'embeddings')}>Embeddings</button>
    <button class:primary={sub === 'translation'} onclick={() => (sub = 'translation')}>Translation</button>
  </nav>

  {#if sub === 'ingestion'}
    <p class="muted">Resolve and load a national instrument or a point-in-time citation into the corpus.</p>
    <div class="grid">
      <label>
        Mode
        <select bind:value={ingMode}>
          <option value="instrument">Instrument (known national id)</option>
          <option value="citation">Citation (resolve at date)</option>
        </select>
      </label>
      <label>
        Jurisdiction
        <input bind:value={jurisdiction} placeholder="fr" />
      </label>
      {#if ingMode === 'instrument'}
        <label class="grow">
          National id
          <input bind:value={nationalId} placeholder="e.g. JORFTEXT000…" />
        </label>
      {:else}
        <label class="grow">
          Citation
          <input bind:value={citationText} placeholder="e.g. CGI art. 197" />
        </label>
        <label>
          As of
          <input type="date" bind:value={asOf} />
        </label>
      {/if}
      <label>
        Source code (opt.)
        <input bind:value={sourceCode} placeholder="e.g. legifrance" />
      </label>
      <label>
        Max items
        <input type="number" min="1" bind:value={maxItems} />
      </label>
    </div>
  {:else if sub === 'document'}
    <p class="muted">
      Add a document you found — a circular, an arrêté, a doctrine page — as a URL or a file
      (PDF, HTML, Markdown, text). Its trust class follows from the kind you state; a URL on a
      known official portal is ingested by that country's adapter instead.
    </p>
    <div class="row">
      <label class="grow">
        URL or file
        <input
          bind:value={docSource}
          onchange={precheckSource}
          placeholder="https://… or /home/reviewer/circulaire.pdf"
          class="mono"
        />
      </label>
      <button onclick={pickDocumentFile} disabled={running}>Pick file…</button>
      <button onclick={precheckSource} disabled={running || !docSource.trim()}>
        {routing ? 'Checking…' : 'Check'}
      </button>
    </div>

    {#if routeOutcome?.outcome === 'adapter'}
      <p class="notice">
        Recognised as {routeOutcome.source}, switching to the legislation ingester:
        <span class="mono">{routeOutcome.jurisdiction} {routeOutcome.national_id}</span>
        {#if routeOutcome.resolved_by && routeOutcome.resolved_by !== 'url'}
          <span class="muted"> (resolved via {routeOutcome.resolved_by})</span>
        {/if}
      </p>
    {:else if routeOutcome?.outcome === 'refused'}
      <p class="error">{routeOutcome.hint}</p>
    {/if}

    {#if !switchingToAdapter}
      <div class="grid">
        <label>
          Jurisdiction
          <select bind:value={docJurisdiction} onchange={onJurisdictionChange}>
            {#each jurisdictions as code (code)}
              <option value={code}>{code}</option>
            {/each}
          </select>
        </label>
        <label>
          Language
          <select bind:value={docLang}>
            {#each languages as code (code)}
              <option value={code}>{code}</option>
            {/each}
          </select>
        </label>
        <label class="grow">
          Title
          <input bind:value={docTitle} placeholder="Circulaire Unédic n° 2025-01" />
        </label>
        <label>
          Kind
          <select bind:value={docKind}>
            {#each Object.entries(docKinds) as [label, kind] (label)}
              <option value={label}>{label} ({kind.source_trust_class})</option>
            {/each}
          </select>
        </label>
        <label>
          In force from
          <input type="date" bind:value={docValidFrom} />
        </label>
        <div class="trust">
          <span class="badge {docTrustClass}">{docTrustClass}</span>
          <span class="muted">derived from the kind</span>
        </div>
      </div>

      <div class="row">
        <label class="grow">
          Implements (optional)
          <input
            bind:value={implementsQuery}
            oninput={searchInstruments}
            placeholder="search an ingested instrument by title or national id"
          />
        </label>
        <span class="muted">
          {docImplements ? `linked to ${docImplements}` : 'none'} — the statute can be ingested
          from the Ingestion sub-tab.
        </span>
        {#if docImplements}
          <button onclick={() => (docImplements = '')}>Clear</button>
        {/if}
      </div>
      {#if implementsResults.length}
        <div class="results">
          {#each implementsResults as instrument (instrument.national_id)}
            <button
              class="result"
              class:chosen={docImplements === instrument.national_id}
              onclick={() => {
                docImplements = instrument.national_id;
                implementsResults = [];
              }}
            >
              <span class="mono">{instrument.national_id}</span>
              <span class="muted"> {instrument.instrument_type} — {instrument.title ?? ''}</span>
            </button>
          {/each}
        </div>
      {/if}
    {/if}
  {:else if sub === 'embeddings'}
    <p class="muted">Build local BGE-M3 vectors for chunks missing fresh embeddings.</p>
    <div class="grid">
      <label class="grow">
        Model path
        <input bind:value={modelPath} placeholder="BAAI/bge-m3 or models/bge-m3-openvino" />
      </label>
      <label>
        Backend
        <select bind:value={backend}>
          <option value="torch">torch</option>
          <option value="openvino">openvino</option>
        </select>
      </label>
      <label>
        Device (opt.)
        <input bind:value={device} placeholder="cpu, cuda, NPU…" />
      </label>
      <label>
        Model id
        <input type="number" min="1" bind:value={modelId} />
      </label>
      <label>
        Batch size
        <input type="number" min="1" bind:value={batchSize} />
      </label>
      <label>
        Limit (opt.)
        <input type="number" min="1" bind:value={embLimit} placeholder="all" />
      </label>
      <label class="check">
        <input type="checkbox" bind:checked={embDryRun} />
        Dry run (count only)
      </label>
    </div>
  {:else}
    <p class="muted">Machine-translate unit texts missing a target-language rendering with an LLM.</p>
    <div class="grid">
      <label class="grow">
        Model
        <input bind:value={model} placeholder="openrouter/…, anthropic/…, openai/…" />
      </label>
      <label>
        Target lang
        <input bind:value={targetLang} placeholder="en" />
      </label>
      <label>
        Request timeout (s)
        <input type="number" min="1" bind:value={requestTimeout} />
      </label>
      <label>
        Limit (opt.)
        <input type="number" min="1" bind:value={trLimit} placeholder="all" />
      </label>
      <label class="check">
        <input type="checkbox" bind:checked={trDryRun} />
        Dry run (count only)
      </label>
    </div>
  {/if}

  <div class="row runbar">
    <button class="primary" onclick={run} disabled={running || (sub === 'document' && !docReady)}>
      {running ? 'Running…' : 'Run'}
    </button>
    <button onclick={stop} disabled={!running}>Stop</button>
    {#if summary}<span class="muted">{summary}</span>{/if}
  </div>

  {#if progress}
    <div class="progressbox">
      <div class="bar"><div class="fill" style="width: {pct}%"></div></div>
      <div class="pstatus muted">
        {progress.done}/{progress.total} ({pct}%)
        {#if progress.failed}<span class="perr"> · {progress.failed} failed</span>{/if}
        {#if running} · {fmtElapsed(elapsed)}{/if}
        {#if progress.detail} · {progress.detail}{/if}
      </div>
    </div>
  {:else if running}
    <div class="progressbox">
      <div class="bar indeterminate"><div class="fill"></div></div>
      <div class="pstatus muted">Working… {fmtElapsed(elapsed)}</div>
    </div>
  {/if}

  {#if error}<p class="error">{error}</p>{/if}

  <div class="log" bind:this={logEl}>
    {#each logLines as l, i (i)}
      <div class="line {l.stream}"><span class="mono">{l.line}</span></div>
    {:else}
      <div class="muted empty">Output will appear here when you run a script.</div>
    {/each}
  </div>
</section>

<style>
  .ingest { overflow: auto; display: flex; flex-direction: column; gap: 0.8rem; min-height: 0; }
  .row { display: flex; gap: 0.5rem; align-items: end; flex-wrap: wrap; }
  .grow { flex: 1; min-width: 16rem; }
  label { display: flex; flex-direction: column; gap: 0.25rem; color: var(--muted); }
  label input, label select { width: 100%; }
  label.check { flex-direction: row; align-items: center; gap: 0.4rem; }
  label.check input { width: auto; }
  .subtabs { display: flex; gap: 0.3rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr)); gap: 0.6rem; align-items: end; }
  .runbar { align-items: center; }
  .error { color: var(--err); }
  .notice { color: var(--accent); margin: 0; }
  .trust { display: flex; align-items: center; gap: 0.4rem; padding-bottom: 0.3rem; }
  /* .badge lives in styles.css: the same class marker everywhere it appears. */
  .results { display: flex; flex-direction: column; gap: 0.2rem; max-height: 12rem; overflow: auto; }
  .result { text-align: left; background: var(--panel-2); border: 1px solid var(--border); }
  .result.chosen { border-color: var(--accent); }
  .progressbox { display: flex; flex-direction: column; gap: 0.3rem; }
  .bar {
    height: 8px;
    background: var(--panel-2);
    border: 1px solid var(--border);
    border-radius: 999px;
    overflow: hidden;
  }
  .bar .fill { height: 100%; background: var(--accent); transition: width 0.3s ease; }
  .bar.indeterminate .fill { width: 30%; animation: bar-slide 1.2s ease-in-out infinite; }
  @keyframes bar-slide {
    from { margin-left: -30%; }
    to { margin-left: 100%; }
  }
  .pstatus { font-size: 0.85rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .pstatus .perr { color: var(--err); }
  .log {
    flex: 1;
    min-height: 12rem;
    overflow: auto;
    background: var(--panel-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.6rem 0.8rem;
    font-size: 0.85rem;
    line-height: 1.4;
  }
  .log .line { white-space: pre-wrap; word-break: break-word; }
  .log .line.stderr .mono { color: var(--err); }
  .log .line.system .mono { color: var(--accent); }
  .log .empty { padding: 0.2rem 0; }
</style>
