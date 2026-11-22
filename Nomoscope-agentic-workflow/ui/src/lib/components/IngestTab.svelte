<script>
  // Add sources: four unrelated forms (LawForm, DocumentForm, EmbedForm,
  // TranslateForm), each describing a job (ops.jobs) the worker runs —
  // `ingest` (instrument / citation / document / route), `embed`, `translate`
  // — and one run bar that follows it until it finishes. Nothing runs on
  // this machine.
  import { onMount } from 'svelte';
  import { worker } from '../api.js';
  import { library } from '../library.svelte.js';
  import { summarize } from '@shared/lib/jobs.js';
  import { formatDuration } from '@shared/lib/format.js';
  import { createJobRun } from '../jobRun.svelte.js';
  import JobProgress from './JobProgress.svelte';
  import JobLog from './JobLog.svelte';
  import LawForm from './LawForm.svelte';
  import DocumentForm from './DocumentForm.svelte';
  import EmbedForm from './EmbedForm.svelte';
  import TranslateForm from './TranslateForm.svelte';
  import Icon from '@shared/components/Icon.svelte';

  const ACTIONS = {
    document: {
      run: 'Add this document',
      title: 'A document or web page',
      blurb: 'A circular, decree, guidance page or PDF you found.',
    },
    ingestion: {
      run: 'Import this law',
      title: 'An official law',
      blurb: 'From the national legal portal, by its reference.',
    },
    embeddings: {
      run: 'Make texts searchable',
      title: 'Make new texts searchable',
      blurb: 'Index texts added recently so the assistant can find them.',
    },
    translation: {
      run: 'Translate',
      title: 'Translate texts',
      blurb: 'Add English versions of texts that only exist in the national language.',
    },
  };

  // What the reviewer is adding. A found document is the common case, so it comes first.
  let sub = $state('document'); // document | ingestion | embeddings | translation
  // The forms, each kept mounted (hidden) so switching keeps what was typed.
  let forms = $state({});
  let documentReady = $state(false);

  // One job (or a document followed by its embeddings build) at a time; the
  // ingest, embed and translate CLIs report structured `@progress` events.
  const job = createJobRun({ workerAlive: () => worker.alive });
  // Errors outside a run: reading the library's vocabulary, checking a source.
  let error = $state('');

  // The vocabulary the store actually has: languages it is configured to index
  // (a text stored under any other is invisible to full-text search) and the
  // jurisdictions it holds; the seeds only cover the moment before it answers.
  const languages = $derived(library.stats?.languages?.length ? library.stats.languages : ['en']);
  const jurisdictions = $derived.by(() => {
    const codes = (library.stats?.by_country ?? []).map((row) => row.code).filter(Boolean);
    return codes.length ? codes : ['FR'];
  });

  onMount(() => {
    // A failure is shown: the pickers would otherwise sit on their seeds with no word of why.
    library.load().then(() => {
      if (library.error) error = `Could not read the library's languages and countries: ${library.error}`;
    });
  });

  async function run() {
    error = '';
    let req;
    try {
      req = forms[sub].request();
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
        const embedded = await job.follow('embed', forms.embeddings.payload());
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
    <div hidden={sub !== 'document'}>
      <DocumentForm
        bind:this={forms.document}
        bind:ready={documentReady}
        {jurisdictions}
        {languages}
        running={job.running}
        onerror={(e) => (error = e)}
      />
    </div>
    <div hidden={sub !== 'ingestion'}><LawForm bind:this={forms.ingestion} {jurisdictions} /></div>
    <div hidden={sub !== 'embeddings'}><EmbedForm bind:this={forms.embeddings} /></div>
    <div hidden={sub !== 'translation'}><TranslateForm bind:this={forms.translation} /></div>

    <div class="runbar">
      <button class="primary big" onclick={run} disabled={job.running || (sub === 'document' && !documentReady)}>
        {#if job.running}<span class="spinner light"></span> Working… {formatDuration(job.elapsed)}{:else}{ACTIONS[sub]
            .run}{/if}
      </button>
      {#if job.running}<button onclick={job.cancel} disabled={job.jobId == null}>Cancel</button>{/if}
    </div>

    <JobProgress run={job} />

    {#if job.summary}<p
        class="callout {job.summary.startsWith('Finished') ? 'ok' : job.summary.startsWith('Failed') ? 'err' : ''}"
      >
        {job.summary}
      </p>{/if}
    {#if job.error}<p class="callout err">{job.error}</p>{/if}
    {#if error}<p class="callout err">{error}</p>{/if}

    <JobLog lines={job.lines} jobId={job.jobId} folded />
  </div>
</section>

<style>
  .ingest {
    overflow: auto;
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
    min-height: 0;
    max-width: 60rem;
  }
  .choices {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
    gap: 0.8rem;
  }
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
  .choice.active {
    border-color: var(--accent);
    background: var(--accent-soft);
  }
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
  .choice-text {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
  }
  .maintenance {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    flex-wrap: wrap;
  }
  .maintenance .on {
    background: var(--accent-soft);
    color: var(--accent);
  }
  .form {
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
  }
  .runbar {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    flex-wrap: wrap;
  }
</style>
