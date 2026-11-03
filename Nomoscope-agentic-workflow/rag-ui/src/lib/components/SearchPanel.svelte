<script>
  // The RAG search without the chat: the review UI's Database-tab query
  // (hybrid = RRF over full text and BGE-M3 vectors), scoped by the chat's
  // country and date. Vector modes encode the query on the worker; with no
  // worker alive the search falls back to full text and says so.
  import { api } from '../api.js';
  import ChunkCard from './ChunkCard.svelte';

  let { dbUrl, country = '', asOf = '' } = $props();

  let query = $state('');
  let mode = $state('hybrid');
  let english = $state(false);
  let results = $state([]);
  let notice = $state('');
  let error = $state('');
  let busy = $state(false);
  let searched = $state(false);

  async function search(event) {
    event?.preventDefault();
    if (!query.trim() || busy) return;
    busy = true;
    error = '';
    try {
      const res = await api.searchArticles({
        db_url: dbUrl,
        query: query.trim(),
        country: country || null,
        as_of: asOf || null,
        languages: english ? ['en'] : null,
        mode,
        limit: 20,
      });
      results = res.results;
      notice = res.notice ?? '';
      searched = true;
    } catch (e) {
      error = String(e);
    } finally {
      busy = false;
    }
  }
</script>

<form onsubmit={search}>
  <input bind:value={query} placeholder="Search the corpus directly (no LLM)…" />
  <button class="primary" disabled={busy || !query.trim()}>{busy ? '…' : 'Search'}</button>
  <div class="opts small">
    <select bind:value={mode}>
      <option value="hybrid">hybrid</option>
      <option value="full_text">full text</option>
      <option value="vector">vector</option>
    </select>
    <label><input type="checkbox" bind:checked={english} /> English renderings only</label>
    <span class="muted">{country || 'all countries'} · in force {asOf || 'any date'}</span>
  </div>
</form>

{#if notice}<p class="banner warn small">{notice}</p>{/if}
{#if error}<p class="banner err small">{error}</p>{/if}
{#if searched && !results.length}<p class="muted">No passage matches.</p>{/if}
{#each results as r (r.chunk_id)}
  <ChunkCard chunk={r} {dbUrl} headline={r.headline} />
{/each}

<style>
  form { display: grid; grid-template-columns: 1fr auto; gap: 0.4rem; margin-bottom: 0.6rem; }
  .opts { grid-column: 1 / -1; display: flex; gap: 0.8rem; align-items: center; flex-wrap: wrap; }
</style>
