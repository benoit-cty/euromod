<script>
  import { api } from '../api.js';

  let { dbUrl = '' } = $props();

  let url = $state(''); // seeded from dbUrl by the $effect below once config loads
  let stats = $state(null);
  let error = $state('');
  let loading = $state(false);

  let query = $state('');
  let country = $state('');
  let asOf = $state('');
  let results = $state(null);
  let searching = $state(false);

  $effect(() => {
    if (dbUrl && !url) url = dbUrl;
  });

  async function loadStats() {
    loading = true;
    error = '';
    try {
      stats = await api.dbStats(url);
    } catch (e) {
      error = String(e);
      stats = null;
    } finally {
      loading = false;
    }
  }

  async function search(event) {
    event?.preventDefault();
    if (!query.trim()) return;
    searching = true;
    error = '';
    try {
      results = await api.searchArticles({
        db_url: url,
        query,
        country: country || null,
        as_of: asOf || null,
        limit: 25,
      });
    } catch (e) {
      error = String(e);
      results = null;
    } finally {
      searching = false;
    }
  }

  $effect(() => {
    if (url && !stats && !loading && !error) loadStats();
  });
</script>

<section class="panel db">
  <div class="row">
    <label class="grow">
      Database URL
      <input bind:value={url} class="mono" />
    </label>
    <button onclick={loadStats} disabled={loading}>{loading ? 'Loading…' : 'Refresh stats'}</button>
  </div>

  {#if error}<p class="error">{error}</p>{/if}

  {#if stats}
    <h2>Corpus statistics</h2>
    <div class="cards">
      {#each Object.entries(stats.totals) as [key, count]}
        <div class="card">
          <div class="num">{count}</div>
          <div class="muted">{key.replaceAll('_', ' ')}</div>
        </div>
      {/each}
    </div>

    <div class="tables">
      <div>
        <h3>By jurisdiction</h3>
        <table>
          <thead>
            <tr><th>Code</th><th>Name</th><th>Instr.</th><th>Units</th><th>Versions</th><th>In force</th><th>Texts</th><th>Chunks</th></tr>
          </thead>
          <tbody>
            {#each stats.by_country as row}
              <tr>
                <td><strong>{row.code}</strong></td>
                <td>{row.name}</td>
                <td>{row.instruments}</td>
                <td>{row.legal_units}</td>
                <td>{row.versions}</td>
                <td>{row.in_force}</td>
                <td>{row.texts}</td>
                <td>{row.chunks}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
      <div>
        <h3>Translation status</h3>
        <table>
          <thead>
            <tr><th>Code</th><th>Authentic</th><th>Official transl.</th><th>Machine transl.</th><th>Coverage</th></tr>
          </thead>
          <tbody>
            {#each stats.by_country as row}
              {@const coverage = row.text_versions === 0 ? 0 : Math.round((row.en_versions / row.text_versions) * 100)}
              <tr>
                <td><strong>{row.code}</strong></td>
                <td>{row.authentic}</td>
                <td>{row.official_translation}</td>
                <td>{row.machine_translation}</td>
                <td>
                  {#if row.text_versions === 0}
                    <span class="muted">—</span>
                  {:else if row.en_versions === 0}
                    <span class="badge pending">no English</span>
                  {:else}
                    <span class="badge pass" class:pending={coverage < 100}
                      >{coverage}% in English</span>
                  {/if}
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
      <div>
        <h3>Embedding models</h3>
        <table>
          <thead><tr><th>Id</th><th>Name</th><th>Provider</th><th>Dim</th><th>Default</th><th>Embedded chunks</th></tr></thead>
          <tbody>
            {#each stats.embedding_models as m}
              <tr>
                <td>{m.id}</td>
                <td>{m.name}</td>
                <td>{m.provider ?? '—'}</td>
                <td>{m.stored_dim}</td>
                <td>{m.is_default ? '✓' : ''}</td>
                <td>{m.embedded_chunks}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  {/if}

  <h2>Find law articles</h2>
  <form class="row" onsubmit={search}>
    <input
      class="grow"
      placeholder="Citation (e.g. CGI art 197) or full-text query (e.g. impôt revenu barème)…"
      bind:value={query}
    />
    <select bind:value={country}>
      <option value="">all countries</option>
      {#each stats?.by_country ?? [] as row}<option value={row.code}>{row.code}</option>{/each}
    </select>
    <input type="date" bind:value={asOf} title="version in force at this date" />
    <button class="primary" type="submit" disabled={searching}>
      {searching ? 'Searching…' : 'Search'}
    </button>
  </form>

  {#if results}
    <p class="muted">{results.results.length} result(s) for “{results.query}”</p>
    {#each results.results as hit (hit.chunk_id)}
      <details>
        <summary>
          <strong>{hit.citation ?? hit.context_header}</strong>
          <span class="badge {hit.version_status === 'in_force' ? 'pass' : 'pending'}">{hit.version_status}</span>
          <span class="muted">
            {hit.country} · {hit.lang} · {hit.validity} · score {hit.score.toFixed(3)}
          </span>
        </summary>
        <p class="muted">{hit.context_header}</p>
        <div class="law-text">{hit.content}</div>
        <p class="muted mono">chunk {hit.chunk_id}</p>
      </details>
    {:else}
      <p class="muted">No matches.</p>
    {/each}
  {/if}
</section>

<style>
  .db { overflow: auto; display: flex; flex-direction: column; gap: 0.8rem; min-height: 0; }
  .row { display: flex; gap: 0.5rem; align-items: end; flex-wrap: wrap; }
  .grow { flex: 1; min-width: 16rem; }
  label { display: flex; flex-direction: column; gap: 0.25rem; color: var(--muted); }
  label input { width: 100%; }
  .error { color: var(--err); }
  .cards { display: flex; gap: 0.6rem; flex-wrap: wrap; }
  .card {
    background: var(--panel-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    min-width: 7.5rem;
  }
  .num { font-size: 1.4rem; font-weight: 700; }
  .tables { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; align-items: start; }
  details { border-top: 1px solid var(--border); padding: 0.5rem 0; }
  summary { cursor: pointer; display: flex; gap: 0.5rem; align-items: baseline; flex-wrap: wrap; }
  @media (max-width: 1100px) { .tables { grid-template-columns: 1fr; } }
</style>
