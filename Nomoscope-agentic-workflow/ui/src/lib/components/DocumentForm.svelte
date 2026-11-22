<script>
  // Add sources › A document or web page. A reviewer pastes a URL or a path
  // and states what the document is; the class is never stated, it follows
  // from the kind (ADR 0001). The source is checked first (an `ingest route`
  // job): a contributed document gets suggestions, a known official source is
  // imported as a law by its adapter, anything else gets a hint.
  import { onMount } from 'svelte';
  import { api, submitAndFollow, worker } from '../api.js';
  import { summarize } from '@shared/lib/jobs.js';
  import { countryName, humanize, trustLabel } from '@shared/lib/labels.js';

  // A recognised official source is imported by its adapter, up to this many items.
  const MAX_ITEMS = 500;

  let {
    // the library's vocabulary (lib/library.svelte.js)
    jurisdictions = ['FR'],
    languages = ['en'],
    // a run is going: no new check
    running = false,
    // can the page's run button go
    ready = $bindable(false),
    // an error outside the run (checking the source, searching instruments)
    onerror = () => {},
  } = $props();

  let docSource = $state(''); // URL or file path (on the worker's host)
  let docJurisdiction = $state('FR'); // the store's codes, as the select offers them
  let docLang = $state('fr');
  let docTitle = $state('');
  let docKind = $state('circulaire');
  let docValidFrom = $state('');
  let docImplements = $state(''); // '' = none
  let implementsQuery = $state('');
  let implementsResults = $state([]);
  // jurisdiction -> { kind: { norm_level, source_trust_class } }, straight from
  // the ingester's own table (`route`), so the UI keeps no copy of the mapping.
  let kindTable = $state({});
  let kindTableError = $state(''); // why the kinds could not be read
  let routeOutcome = $state(null); // { outcome, source, national_id, hint, ... }
  let routing = $state(false);

  let docKinds = $derived(
    Object.keys(kindTable[docJurisdiction.toUpperCase()] ?? {}).length
      ? kindTable[docJurisdiction.toUpperCase()]
      : (kindTable.DEFAULT ?? {}),
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
          routeOutcome?.outcome !== 'refused',
        ),
  );

  $effect(() => {
    ready = docReady;
  });

  // The kinds each jurisdiction offers, and the class each one implies, come
  // from the ingester so the two can never drift. `route` with no source
  // answers with the table alone, so the Kind select is populated before the
  // reviewer has pasted anything. It needs a worker: without one the Kind
  // select says why instead of waiting forever.
  onMount(() => {
    const t = setTimeout(async () => {
      try {
        const outcome = await routeSource();
        if (outcome?.kinds) kindTable = outcome.kinds;
      } catch (e) {
        kindTableError = String(e.message ?? e);
      }
    }, 500);
    return () => clearTimeout(t);
  });

  // Ask the ingester what this input is, before any run starts. One `route`
  // job; the worker stores the JSON line the CLI prints as the job's result.
  async function routeSource(source) {
    if (worker.alive === null) await worker.refresh();
    if (!worker.alive) throw new Error('no worker is running — the source cannot be checked');
    const final = await submitAndFollow('ingest', { command: 'route', args: source ? [source] : [] });
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
      onerror(String(e.message ?? e));
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
      onerror(String(e));
    }
  }

  /** The job to submit; throws with what is missing. A document job is followed by an embeddings build. */
  export function request() {
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
          args: [routeOutcome.jurisdiction, routeOutcome.national_id, '--max-items', String(MAX_ITEMS)],
        },
      };
    }
    if (!docValidFrom) throw new Error('a validity start date is required');
    return {
      job_type: 'ingest',
      payload: {
        command: 'document',
        args: [
          docSource.trim(),
          '--jurisdiction',
          docJurisdiction.trim(),
          '--lang',
          docLang.trim(),
          '--title',
          docTitle.trim(),
          '--kind',
          docKind,
          '--valid-from',
          docValidFrom,
          ...(docImplements ? ['--implements', docImplements] : []),
          '--progress-json',
        ],
      },
    };
  }
</script>

<div class="subform">
  <p class="muted">
    Paste a link (or a file path on the worker’s machine): PDF, web page, Markdown or text. We check it first. If it is
    on an official legal portal, it is imported as a law instead.
  </p>
  <div class="row">
    <input class="grow mono" bind:value={docSource} onchange={precheckSource} placeholder="https://…" />
    <button onclick={precheckSource} disabled={running || !docSource.trim()}>
      {#if routing}<span class="spinner"></span> Checking…{:else}Check{/if}
    </button>
  </div>

  {#if routeOutcome?.outcome === 'adapter'}
    <p class="callout ok">
      Recognised as an official text from {routeOutcome.source}: it will be imported as a law (<span class="mono">
        {routeOutcome.jurisdiction}
        {routeOutcome.national_id}
      </span>).
    </p>
  {:else if routeOutcome?.outcome === 'refused'}
    <p class="callout err">{routeOutcome.hint}</p>
  {/if}

  {#if !switchingToAdapter}
    <div class="form-grid">
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
        <span class="badge {docTrustClass}" title={trustLabel(docTrustClass).hint}>
          {trustLabel(docTrustClass).label}
        </span>
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
                <span class="muted small">
                  <span class="mono">{instrument.national_id}</span> · {humanize(instrument.instrument_type)}
                </span>
              </button>
            {/each}
          </div>
        {/if}
      </div>
    </details>
  {/if}
  {#if !ready && !running && !switchingToAdapter}
    <p class="muted small">Fill in the link, title, kind and date first.</p>
  {/if}
</div>

<style>
  .subform {
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
  }
  .subform > p.muted {
    margin: 0;
  }
  .trust {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0;
  }
  .results {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    max-height: 14rem;
    overflow: auto;
  }
  .result {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.1rem;
    text-align: left;
    background: var(--panel-2);
    border-color: transparent;
  }
  .result.chosen {
    border-color: var(--accent);
  }
</style>
