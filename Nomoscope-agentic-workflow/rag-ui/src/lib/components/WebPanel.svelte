<script>
  // What a turn found on the web. Web text is never evidence: it is shown so
  // the analyst can open the official page, and an act the corpus lacks can
  // be ingested — an `ingest` job (archive-first: fetch → snapshot → parse →
  // chunk) followed by an `embed` job, exactly as the Ingest tab of the
  // review UI does. Ask again once it is in.
  import { api } from '../api.js';
  import { ingestPayload } from '../chat.js';
  import { lastLine, submitAndFollow } from '../jobs.js';

  let { result, dbUrl } = $props();

  // instrument_id -> { phase: ingesting | embedding | done | failed, jobId, message }
  let ingests = $state({});

  const discoveries = $derived(result?.discoveries ?? []);
  const webResults = $derived(result?.web_results ?? []);

  async function ingest(d) {
    const key = d.instrument_id;
    ingests[key] = { phase: 'ingesting', jobId: null, message: '' };
    try {
      const done = await submitAndFollow(dbUrl, 'ingest', ingestPayload(d), {
        onSubmit: (id) => (ingests[key].jobId = id),
      });
      if (done.status !== 'succeeded') {
        ingests[key] = { phase: 'failed', jobId: done.id, message: lastLine(done.error) };
        return;
      }
      ingests[key] = { phase: 'embedding', jobId: null, message: '' };
      const embedded = await submitAndFollow(dbUrl, 'embed', {}, {
        onSubmit: (id) => (ingests[key].jobId = id),
      });
      ingests[key] =
        embedded.status === 'succeeded'
          ? { phase: 'done', jobId: embedded.id, message: 'In the corpus and embedded — ask again.' }
          : { phase: 'failed', jobId: embedded.id, message: `ingested, but embedding failed (full-text search still finds it): ${lastLine(embedded.error)}` };
    } catch (e) {
      ingests[key] = { phase: 'failed', jobId: null, message: String(e) };
    }
  }
</script>

{#if !result}
  <p class="muted">Select an answer to see what it found on the web.</p>
{:else}
  {#if discoveries.length}
    <h3>Not in the corpus</h3>
    {#each discoveries as d (d.instrument_id)}
      {@const job = ingests[d.instrument_id]}
      <div class="disc">
        <div>
          <span class="badge">{d.country}</span>
          <span class="mono">{d.instrument_id}</span>
          <div class="small">{d.title}</div>
          <button class="link small" onclick={() => api.openExternal(d.url)}>{d.url}</button>
        </div>
        <div class="act">
          {#if !job || job.phase === 'failed'}
            <button class="primary" onclick={() => ingest(d)}>{job ? 'Retry' : 'Ingest'}</button>
          {:else if job.phase === 'done'}
            <span class="badge ok">ingested</span>
          {:else}
            <span class="badge info">{job.phase}…{job.jobId ? ` #${job.jobId}` : ''}</span>
          {/if}
        </div>
        {#if job?.message}<p class="small" class:err={job.phase === 'failed'}>{job.message}</p>{/if}
      </div>
    {/each}
  {/if}

  <h3>Web results</h3>
  {#if !webResults.length}
    <p class="muted small">No web search in this turn.</p>
  {/if}
  {#each webResults as w (w.url)}
    <div class="web">
      <button class="link" onclick={() => api.openExternal(w.url)}>{w.title || w.url}</button>
      <div class="muted small url">{w.url}</div>
      {#if w.snippet}<p class="small">{w.snippet}</p>{/if}
      {#each w.instrument_ids as i (i.id)}
        <span class="badge {i.in_corpus ? 'ok' : 'warn'}">{i.id} — {i.in_corpus ? 'in corpus' : 'not ingested'}</span>
      {/each}
    </div>
  {/each}
  <p class="muted small">Web pages are leads, never evidence: answers quote the corpus only.</p>
{/if}

<style>
  h3 { font-size: 0.9rem; margin: 0.8rem 0 0.4rem; }
  .disc, .web {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.5rem 0.7rem;
    margin-bottom: 0.5rem;
  }
  .disc { display: grid; grid-template-columns: 1fr auto; gap: 0.3rem 0.6rem; }
  .disc p { grid-column: 1 / -1; margin: 0; }
  .disc .err { color: var(--err); }
  .act { align-self: start; }
  .web p { margin: 0.3rem 0; }
  .url { word-break: break-all; }
  .link { text-align: left; word-break: break-all; }
</style>
