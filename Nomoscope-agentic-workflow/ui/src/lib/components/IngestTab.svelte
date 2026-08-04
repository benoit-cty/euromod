<script>
  import { onMount } from 'svelte';
  import { api } from '../api.js';

  let { dbUrl = '' } = $props();

  let url = $state(''); // seeded from dbUrl by the $effect below once config loads
  let sub = $state('ingestion'); // ingestion | embeddings | translation

  // --- ingestion form ---
  let ingMode = $state('instrument'); // instrument | citation
  let jurisdiction = $state('fr');
  let nationalId = $state('');
  let citationText = $state('');
  let asOf = $state('');
  let sourceCode = $state('');
  let maxItems = $state(500);

  // --- embeddings form ---
  let modelPath = $state('models/bge-m3-openvino');
  let backend = $state('openvino'); // torch | openvino
  let device = $state('');
  let modelId = $state(1);
  let batchSize = $state(16);
  let embLimit = $state('');
  let embDryRun = $state(false);

  // --- translation form ---
  let model = $state('azure_openai/gpt-5.4-nano');
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

  // Tick the elapsed clock while a run is active.
  $effect(() => {
    if (!running) return;
    const t = setInterval(() => (now = Date.now()), 1000);
    return () => clearInterval(t);
  });

  onMount(() => {
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
    if (sub === 'embeddings') {
      const args = [
        '--model-path', modelPath.trim(),
        '--backend', backend,
        '--model-id', String(modelId),
        '--batch-size', String(batchSize),
        '--progress-json',
      ];
      if (device.trim()) args.push('--device', device.trim());
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
    } catch (e) {
      error = String(e);
    } finally {
      running = false;
    }
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
    <button class="primary" onclick={run} disabled={running}>
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
