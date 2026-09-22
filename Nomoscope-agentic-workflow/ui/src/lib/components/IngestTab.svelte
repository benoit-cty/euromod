<script>
  // Ingest tab: every sub-form describes a job (ops.jobs) the worker runs —
  // `ingest` (instrument / citation / document / route), `embed`, `translate`
  // — and follows its events until it finishes. Nothing runs on this machine.
  import { onMount } from 'svelte';
  import { api } from '../api.js';
  import { submitAndFollow, summarize } from '../jobs.js';

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
  let docSource = $state('');          // URL or file path (on the worker's host)
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
  // Backend, model path and device are the worker's business: it runs BGE-M3
  // on whatever it has (CUDA, else CPU). The form only says what to embed.
  let modelId = $state(1);
  let batchSize = $state(16);
  let embLimit = $state('');
  let embDryRun = $state(false);

  // --- translation form ---
  // The model is picked from the list the worker publishes (ops.worker_models),
  // never typed: a free-text model string is how a wrong deployment went
  // unnoticed for a month.
  let models = $state([]);            // [{ model, kind, is_default }] of kind llm
  let model = $state('');
  let workerAlive = $state(null);     // null = unknown yet
  let targetLang = $state('en');
  let trLimit = $state('');
  let requestTimeout = $state(120);
  let trDryRun = $state(false);

  // --- run state ---
  let running = $state(false);
  let jobId = $state(null);
  let logLines = $state([]);
  let summary = $state('');
  let error = $state('');
  let logEl = $state(null);

  // --- progress state ---
  // The worker turns the CLI's "@progress {json}" lines into progress events
  // and we render a real bar; ingestion runs (no totals) get an indeterminate
  // activity bar + elapsed time instead.
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
    loadWorker().catch(() => {});
  });

  // Tick the elapsed clock while a run is active.
  $effect(() => {
    if (!running) return;
    const t = setInterval(() => (now = Date.now()), 1000);
    return () => clearInterval(t);
  });

  async function loadWorker() {
    const status = await api.workerStatus(url.trim());
    workerAlive = (status.workers ?? []).some((w) => w.alive);
    models = (status.models ?? []).filter((m) => m.kind === 'llm');
    if (!models.some((m) => m.model === model)) {
      model = (models.find((m) => m.is_default) ?? models[0])?.model ?? '';
    }
  }

  // The kinds each jurisdiction offers, and the class each one implies, come
  // from the ingester so the two can never drift. `route` with no source
  // answers with the table alone, so the Kind select is populated before the
  // reviewer has pasted anything.
  async function loadKindTable() {
    const outcome = await routeSource();
    if (outcome?.kinds) kindTable = outcome.kinds;
  }

  onMount(() => {
    // needs a worker: the table comes back as a job result
    const t = setTimeout(() => loadKindTable().catch(() => {}), 500);
    return () => clearTimeout(t);
  });

  // Auto-scroll the log to the bottom as lines arrive.
  $effect(() => {
    logLines.length;
    if (logEl) logEl.scrollTop = logEl.scrollHeight;
  });

  // Ask the ingester what this input is, before any run starts: prefill for a
  // contributed document, announce-and-switch for a known official source, a
  // hint for something we will not ingest this way. One `route` job; the
  // worker stores the JSON line the CLI prints as the job's result.
  async function routeSource(source) {
    if (workerAlive === null) await loadWorker();
    if (!workerAlive) throw new Error('no worker is running — the source cannot be checked');
    const final = await submitAndFollow(url.trim(), 'ingest', {
      command: 'route',
      args: source ? [source] : [],
    });
    if (final.status !== 'succeeded') throw new Error(`route job #${final.id}: ${summarize(final)}`);
    return final.result ?? null;
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
      error = String(e.message ?? e);
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

  const optionalInt = (value) => (String(value).trim() ? Number(String(value).trim()) : null);

  function embedPayload() {
    return {
      model_id: Number(modelId),
      batch_size: Number(batchSize),
      limit: optionalInt(embLimit),
      dry_run: Boolean(embDryRun),
    };
  }

  // Build the job type + payload for the active sub-tab.
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
      return { job_type: 'ingest', payload: { command: ingMode, args } };
    }
    if (sub === 'document') {
      if (!docSource.trim()) throw new Error('paste a URL or a path first');
      if (routeOutcome?.outcome === 'refused') throw new Error(routeOutcome.hint);
      // A known official source is ingested by its adapter, from its national
      // id — never as a page. The library re-routes anyway; this only keeps
      // the log honest about which command actually ran.
      if (switchingToAdapter) {
        return {
          job_type: 'ingest',
          payload: {
            command: 'instrument',
            args: [routeOutcome.jurisdiction, routeOutcome.national_id, '--max-items', String(maxItems)],
          },
        };
      }
      if (!docValidFrom) throw new Error('a validity start date is required');
      return { job_type: 'ingest', payload: { command: 'document', args: documentArgs() } };
    }
    if (sub === 'embeddings') {
      return { job_type: 'embed', payload: embedPayload() };
    }
    // translation
    if (!model) throw new Error('no model to translate with — the worker has published none');
    return {
      job_type: 'translate',
      payload: {
        model,
        target_lang: targetLang.trim(),
        limit: optionalInt(trLimit),
        request_timeout: optionalInt(requestTimeout) ?? 120,
        dry_run: Boolean(trDryRun),
      },
    };
  }

  const handlers = {
    onSubmit: (id) => {
      jobId = id;
      logLines = [...logLines, { stream: 'system', line: `job #${id} submitted` }];
    },
    onLine: (e) => (logLines = [...logLines, e]),
    onProgress: (data) => {
      if (data) progress = data;
    },
  };

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
    jobId = null;
    logLines = [];
    progress = null;
    startedAt = Date.now();
    now = startedAt;
    running = true;
    try {
      if (workerAlive === false) {
        logLines = [{ stream: 'system', line: 'no worker alive — the job waits in the queue until one starts' }];
      }
      const final = await submitAndFollow(url.trim(), req.job_type, req.payload, handlers);
      summary = summarize(final);
      // A contributed document is only retrievable once its chunks are
      // embedded, so a successful `document` job is followed by an embeddings
      // build. A failed one chains nothing: there is nothing new to embed.
      if (final.status === 'succeeded' && req.payload.command === 'document') await runFollowUpEmbeddings();
    } catch (e) {
      error = String(e.message ?? e);
    } finally {
      running = false;
    }
  }

  async function runFollowUpEmbeddings() {
    summary = 'Document loaded. Building embeddings for the new chunks…';
    progress = null;
    startedAt = Date.now();
    now = startedAt;
    const final = await submitAndFollow(url.trim(), 'embed', embedPayload(), handlers);
    summary =
      final.status === 'succeeded'
        ? 'Finished successfully; the document is retrievable.'
        : `Document loaded, but the embeddings build ${summarize(final).toLowerCase()}`;
  }

  async function stop() {
    if (jobId != null) await api.cancelJob(url.trim(), jobId);
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
    {#if workerAlive === false}
      <span class="badge fail" title="ops.workers heartbeat stale">no worker alive</span>
    {:else if workerAlive}
      <span class="badge pass">worker alive</span>
    {/if}
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
      known official portal is ingested by that country's adapter instead. The worker fetches
      it, so a file path must be one the worker's host can read.
    </p>
    <div class="row">
      <label class="grow">
        URL or file path
        <input
          bind:value={docSource}
          onchange={precheckSource}
          placeholder="https://… or /data/contributed/circulaire.pdf"
          class="mono"
        />
      </label>
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
    <p class="muted">
      Build BGE-M3 vectors for chunks missing fresh embeddings, on the worker's GPU (or CPU
      when it has none — the worker decides).
    </p>
    <div class="grid">
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
    <p class="muted">Machine-translate unit texts missing a target-language rendering with an LLM served by the worker.</p>
    <div class="grid">
      <label class="grow">
        Model
        <select bind:value={model} disabled={!models.length}>
          {#each models as m (m.model)}
            <option value={m.model}>{m.model}{m.is_default ? ' (default)' : ''}</option>
          {:else}
            <option value="">no model published by the worker</option>
          {/each}
        </select>
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
    <button onclick={stop} disabled={!running || jobId == null}>Cancel</button>
    {#if jobId != null}<span class="muted mono">job #{jobId}</span>{/if}
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
      <div class="muted empty">Output will appear here when you run a job.</div>
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
