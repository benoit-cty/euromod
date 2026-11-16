<script>
  // Ingest tab: every sub-form describes a job (ops.jobs) the worker runs —
  // `ingest` (instrument / citation / document / route), `embed`, `translate`
  // — and follows its events until it finishes. Nothing runs on this machine.
  import { onMount } from 'svelte';
  import { api, submitAndFollow, worker } from '../api.js';
  import { library } from '../library.svelte.js';
  import ModelPicker from '@shared/components/ModelPicker.svelte';
  import { summarize } from '@shared/lib/jobs.js';
  import { formatDuration } from '@shared/lib/format.js';
  import { createJobRun } from '../jobRun.svelte.js';
  import JobProgress from './JobProgress.svelte';
  import JobLog from './JobLog.svelte';
  import { countryName, humanize } from '@shared/lib/labels.js';
  import Icon from '@shared/components/Icon.svelte';

  const ACTIONS = {
    document: { run: 'Add this document', title: 'A document or web page', blurb: 'A circular, decree, guidance page or PDF you found.' },
    ingestion: { run: 'Import this law', title: 'An official law', blurb: 'From the national legal portal, by its reference.' },
    embeddings: { run: 'Make texts searchable', title: 'Make new texts searchable', blurb: 'Index texts added recently so the assistant can find them.' },
    translation: { run: 'Translate', title: 'Translate texts', blurb: 'Add English versions of texts that only exist in the national language.' },
  };

  // What the reviewer is adding. A found document is the common case, so it comes first.
  let sub = $state('document'); // document | ingestion | embeddings | translation

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
  let docJurisdiction = $state('FR'); // the store's codes, as the select offers them
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
  let kindTableError = $state('');     // why the kinds could not be read
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
  let model = $state('');
  let targetLang = $state('en');
  let trLimit = $state('');
  let requestTimeout = $state(120);
  let trDryRun = $state(false);

  // --- run state ---
  // One job (or a document followed by its embeddings build) at a time; the
  // ingest, embed and translate CLIs report structured `@progress` events.
  const job = createJobRun({ workerAlive: () => worker.alive });
  // Errors outside a run: reading the library's vocabulary, checking a source.
  let error = $state('');

  // The vocabulary the store actually has: languages it is configured to index
  // (a text stored under any other is invisible to full-text search) and the
  // jurisdictions it holds. A failure is shown: the pickers would otherwise
  // sit on their seeds with no word of why.
  onMount(() => {
    library.load().then(() => {
      if (library.error) error = `Could not read the library's languages and countries: ${library.error}`;
    });
  });

  $effect(() => {
    const stats = library.stats;
    if (stats?.languages?.length) languages = stats.languages;
    const codes = (stats?.by_country ?? []).map((row) => row.code).filter(Boolean);
    if (codes.length) jurisdictions = codes;
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
    // needs a worker: the table comes back as a job result. Without one the
    // Kind select says why instead of waiting forever.
    const t = setTimeout(
      () => loadKindTable().catch((e) => (kindTableError = String(e.message ?? e))),
      500,
    );
    return () => clearTimeout(t);
  });

  // Ask the ingester what this input is, before any run starts: prefill for a
  // contributed document, announce-and-switch for a known official source, a
  // hint for something we will not ingest this way. One `route` job; the
  // worker stores the JSON line the CLI prints as the job's result.
  async function routeSource(source) {
    if (worker.alive === null) await worker.refresh();
    if (!worker.alive) throw new Error('no worker is running — the source cannot be checked');
    const final = await submitAndFollow('ingest', {
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
      if (routeOutcome?.kinds) {
        kindTable = routeOutcome.kinds;
        kindTableError = '';
      }
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
      const res = await api.searchInstruments(docJurisdiction.trim(), implementsQuery.trim());
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

  async function run() {
    error = '';
    let req;
    try {
      req = buildRequest();
    } catch (e) {
      error = String(e.message ?? e);
      return;
    }
    await job.session(async () => {
      const final = await job.follow(req.job_type, req.payload);
      job.summary = summarize(final);
      // A contributed document is only retrievable once its chunks are
      // embedded, so a successful `document` job is followed by an embeddings
      // build. A failed one chains nothing: there is nothing new to embed.
      if (final.status === 'succeeded' && req.payload.command === 'document') {
        job.summary = 'Document loaded. Building embeddings for the new chunks…';
        const embedded = await job.follow('embed', embedPayload());
        job.summary =
          embedded.status === 'succeeded'
            ? 'Finished successfully; the document is retrievable.'
            : `Document loaded, but the embeddings build ${summarize(embedded).toLowerCase()}`;
      }
    });
  }
</script>
<section class="ingest">
  <div class="choices">
    {#each ['document', 'ingestion'] as key}
      <button class="choice" class:active={sub === key} onclick={() => (sub = key)} disabled={job.running}>
        <span class="choice-icon"><Icon name={key === 'document' ? 'plus' : 'book'} size={20} /></span>
        <span class="choice-text">
          <strong>{ACTIONS[key].title}</strong>
          <span class="muted small">{ACTIONS[key].blurb}</span>
        </span>
      </button>
    {/each}
  </div>
  <div class="maintenance">
    <span class="muted small">Maintenance:</span>
    {#each ['embeddings', 'translation'] as key}
      <button class="ghost small" class:on={sub === key} onclick={() => (sub = key)} disabled={job.running}>
        {ACTIONS[key].title}
      </button>
    {/each}
    <div class="spacer"></div>
    {#if worker.alive === false}
      <span class="badge fail" title="No worker heartbeat: work will wait until one starts">worker offline</span>
    {/if}
  </div>

  <div class="panel form">
    {#if sub === 'ingestion'}
      <p class="muted">
        Give the law’s official reference; the importer fetches it from the national portal with all its
        articles and versions.
      </p>
      <div class="grid">
        <label class="field">
          Country
          <select bind:value={jurisdiction}>
            {#each jurisdictions as code (code)}
              <option value={code.toLowerCase()}>{countryName(code)}</option>
            {/each}
          </select>
        </label>
        <label class="field">
          I know its
          <select bind:value={ingMode}>
            <option value="instrument">official identifier</option>
            <option value="citation">citation (e.g. “CGI art. 197”)</option>
          </select>
        </label>
        {#if ingMode === 'instrument'}
          <label class="field wide">
            Official identifier
            <input bind:value={nationalId} placeholder="e.g. JORFTEXT000051168007" />
          </label>
        {:else}
          <label class="field wide">
            Citation
            <input bind:value={citationText} placeholder="e.g. CGI art. 197" />
          </label>
          <label class="field">
            Version in force on
            <input type="date" bind:value={asOf} />
          </label>
        {/if}
      </div>
      <details class="more">
        <summary>Advanced <span class="hint">source code, item limit</span></summary>
        <div class="body grid">
          <label class="field">
            Source code
            <input bind:value={sourceCode} placeholder="e.g. legifrance" />
          </label>
          <label class="field">
            Max items
            <input type="number" min="1" bind:value={maxItems} />
          </label>
        </div>
      </details>
    {:else if sub === 'document'}
      <p class="muted">
        Paste a link (or a file path on the worker’s machine): PDF, web page, Markdown or text. We check it
        first. If it is on an official legal portal, it is imported as a law instead.
      </p>
      <div class="row">
        <input
          class="grow mono"
          bind:value={docSource}
          onchange={precheckSource}
          placeholder="https://…"
        />
        <button onclick={precheckSource} disabled={job.running || !docSource.trim()}>
          {#if routing}<span class="spinner"></span> Checking…{:else}Check{/if}
        </button>
      </div>

      {#if routeOutcome?.outcome === 'adapter'}
        <p class="callout ok">
          Recognised as an official text from {routeOutcome.source}: it will be imported as a law
          (<span class="mono">{routeOutcome.jurisdiction} {routeOutcome.national_id}</span>).
        </p>
      {:else if routeOutcome?.outcome === 'refused'}
        <p class="callout err">{routeOutcome.hint}</p>
      {/if}

      {#if !switchingToAdapter}
        <div class="grid">
          <label class="field wide">
            Title
            <input bind:value={docTitle} placeholder="Circulaire Unédic n° 2025-01" />
          </label>
          <label class="field">
            Country
            <select bind:value={docJurisdiction} onchange={onJurisdictionChange}>
              {#each jurisdictions as code (code)}
                <option value={code}>{countryName(code)}</option>
              {/each}
            </select>
          </label>
          <label class="field">
            Language
            <select bind:value={docLang}>
              {#each languages as code (code)}
                <option value={code}>{code}</option>
              {/each}
            </select>
          </label>
          <label class="field">
            What is it?
            <select bind:value={docKind}>
              {#each Object.keys(docKinds) as label (label)}
                <option value={label}>{humanize(label)}</option>
              {:else}
                <option value="">{kindTableError ? 'unavailable: see below' : 'waiting for the worker…'}</option>
              {/each}
            </select>
          </label>
          <label class="field">
            In force from
            <input type="date" bind:value={docValidFrom} />
          </label>
        </div>
        {#if kindTableError && !Object.keys(docKinds).length}
          <p class="callout err">The document kinds could not be read: {kindTableError}</p>
        {/if}
        {#if docTrustClass}
          <p class="small trust">
            <span class="badge {docTrustClass}">{docTrustClass === 'evidence' ? 'Legislation' : humanize(docTrustClass)}</span>
            <span class="muted">
              {docTrustClass === 'evidence'
                ? 'Will be treated as legislation.'
                : docTrustClass === 'guidance'
                  ? 'Will be citable, but always shown as guidance rather than law.'
                  : 'Background only: never cited as evidence.'}
              This follows from “What is it?”.
            </span>
          </p>
        {/if}

        <details class="more">
          <summary>
            Link to the law it implements
            <span class="hint">{docImplements ? `linked to ${docImplements}` : 'optional'}</span>
          </summary>
          <div class="body">
            <div class="row">
              <input
                class="grow"
                bind:value={implementsQuery}
                oninput={searchInstruments}
                placeholder="search a law in the library by title or identifier"
              />
              {#if docImplements}<button onclick={() => (docImplements = '')}>Clear</button>{/if}
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
                    <span>{instrument.title ?? instrument.national_id}</span>
                    <span class="muted mono small">{instrument.national_id} · {instrument.instrument_type}</span>
                  </button>
                {/each}
              </div>
            {/if}
          </div>
        </details>
      {/if}
    {:else if sub === 'embeddings'}
      <p class="muted">
        Index the texts that are not searchable yet. Runs on the worker; needed after any import (adding a
        document does it for you).
      </p>
      <details class="more">
        <summary>Advanced <span class="hint">model, batch size, limit</span></summary>
        <div class="body grid">
          <label class="field">
            Model id
            <input type="number" min="1" bind:value={modelId} />
          </label>
          <label class="field">
            Batch size
            <input type="number" min="1" bind:value={batchSize} />
          </label>
          <label class="field">
            Limit
            <input type="number" min="1" bind:value={embLimit} placeholder="all" />
          </label>
          <label class="field check">
            <input type="checkbox" bind:checked={embDryRun} />
            Only count, change nothing
          </label>
        </div>
      </details>
    {:else}
      <p class="muted">Machine-translate texts that have no version in the target language yet.</p>
      <div class="grid">
        <label class="field wide">
          Language model
          <ModelPicker models={worker.llmModels} bind:value={model} />
        </label>
        <label class="field">
          Into
          <input bind:value={targetLang} placeholder="en" />
        </label>
      </div>
      <details class="more">
        <summary>Advanced <span class="hint">timeout, limit</span></summary>
        <div class="body grid">
          <label class="field">
            Request timeout (s)
            <input type="number" min="1" bind:value={requestTimeout} />
          </label>
          <label class="field">
            Limit
            <input type="number" min="1" bind:value={trLimit} placeholder="all" />
          </label>
          <label class="field check">
            <input type="checkbox" bind:checked={trDryRun} />
            Only count, change nothing
          </label>
        </div>
      </details>
    {/if}

    <div class="runbar">
      <button class="primary big" onclick={run} disabled={job.running || (sub === 'document' && !docReady)}>
        {#if job.running}<span class="spinner light"></span> Working… {formatDuration(job.elapsed)}{:else}{ACTIONS[sub].run}{/if}
      </button>
      {#if job.running}<button onclick={job.cancel} disabled={job.jobId == null}>Cancel</button>{/if}
      {#if sub === 'document' && !docReady && !job.running && !switchingToAdapter}
        <span class="muted small">Fill in the link, title, kind and date first.</span>
      {/if}
    </div>

    <JobProgress run={job} />

    {#if job.summary}<p class="callout {job.summary.startsWith('Finished') ? 'ok' : job.summary.startsWith('Failed') ? 'err' : ''}">{job.summary}</p>{/if}
    {#if job.error}<p class="callout err">{job.error}</p>{/if}
    {#if error}<p class="callout err">{error}</p>{/if}

    <JobLog lines={job.lines} jobId={job.jobId} folded />
  </div>
</section>

<style>
  .ingest { overflow: auto; display: flex; flex-direction: column; gap: 0.9rem; min-height: 0; max-width: 60rem; }
  .choices { display: grid; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); gap: 0.8rem; }
  .choice {
    justify-content: flex-start;
    align-items: flex-start;
    gap: 0.8rem;
    padding: 1rem 1.1rem;
    border-radius: var(--radius);
    border: 1.5px solid var(--border);
    background: var(--panel);
    text-align: left;
    box-shadow: var(--shadow);
  }
  .choice.active { border-color: var(--accent); background: var(--accent-soft); }
  .choice-icon {
    width: 2.3rem;
    height: 2.3rem;
    border-radius: 9px;
    background: var(--panel-2);
    color: var(--accent);
    display: grid;
    place-items: center;
    flex: none;
  }
  .choice-text { display: flex; flex-direction: column; gap: 0.15rem; }
  .maintenance { display: flex; align-items: center; gap: 0.3rem; flex-wrap: wrap; }
  .maintenance .on { background: var(--accent-soft); color: var(--accent); }
  .spacer { flex: 1; }
  .form { display: flex; flex-direction: column; gap: 0.9rem; }
  .form > p.muted { margin: 0; }
  .row { display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; }
  .grow { flex: 1; min-width: 16rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr)); gap: 0.7rem; align-items: end; }
  .wide { grid-column: span 2; }
  .trust { display: flex; align-items: center; gap: 0.5rem; margin: 0; }
  .results { display: flex; flex-direction: column; gap: 0.25rem; max-height: 14rem; overflow: auto; }
  .result { flex-direction: column; align-items: flex-start; gap: 0.1rem; text-align: left; background: var(--panel-2); border-color: transparent; }
  .result.chosen { border-color: var(--accent); }
  .runbar { display: flex; align-items: center; gap: 0.7rem; flex-wrap: wrap; }
  @media (max-width: 700px) { .wide { grid-column: auto; } }
</style>
