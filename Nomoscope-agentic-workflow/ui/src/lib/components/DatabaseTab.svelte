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
  let language = $state('');
  let mode = $state('hybrid');
  let results = $state(null);
  let searching = $state(false);

  const modes = [
    { value: 'hybrid', label: 'Hybrid' },
    { value: 'full_text', label: 'Full text' },
    { value: 'vector', label: 'Embeddings' },
  ];

  const formatScore = (value, digits = 5) => value == null ? '—' : Number(value).toFixed(digits);
  const vectorSimilarity = (distance) => distance == null ? null : 1 - Number(distance);

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
        languages: language ? [language] : null,
        mode,
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

  // Target of the shell's Reload button while this tab is showing: stats plus
  // the current search, so results reflect a corpus that changed under us.
  export async function reload() {
    await loadStats();
    if (results) await search();
  }
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
            <tr><th>Code</th><th>Name</th><th>Instr.</th><th>Units</th><th>Versions</th><th>In force</th><th>Texts</th><th>Chunks</th><th>Embedded</th></tr>
          </thead>
          <tbody>
            {#each stats.by_country as row}
              {@const embedded = row.chunks === 0 ? 0 : Math.round((row.embedded_chunks / row.chunks) * 100)}
              <tr>
                <td><strong>{row.code}</strong></td>
                <td>{row.name}</td>
                <td>{row.instruments}</td>
                <td>{row.legal_units}</td>
                <td>{row.versions}</td>
                <td>{row.in_force}</td>
                <td>{row.texts}</td>
                <td>{row.chunks}</td>
                <td>
                  {#if row.chunks === 0}
                    <span class="muted">—</span>
                  {:else if row.embedded_chunks === 0}
                    <span class="badge pending">none</span>
                  {:else}
                    <span class="badge pass" class:pending={embedded < 100}
                      >{row.embedded_chunks} ({embedded}%)</span>
                  {/if}
                </td>
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
  <form class="search-form" onsubmit={search}>
    <div class="search-query row">
      <input
        class="grow"
        placeholder="Ask in English, for example: personal income tax brackets and marginal rates"
        bind:value={query}
      />
      <button class="primary" type="submit" disabled={searching}>
        {searching ? (mode === 'full_text' ? 'Searching…' : 'Encoding and searching…') : 'Search'}
      </button>
    </div>
    <div class="search-options">
      <div class="segmented" aria-label="Search mode">
        {#each modes as item}
          <button
            type="button"
            class:active={mode === item.value}
            aria-pressed={mode === item.value}
            onclick={() => mode = item.value}
          >{item.label}</button>
        {/each}
      </div>
      <label>
        Country
        <select bind:value={country}>
          <option value="">All</option>
          {#each stats?.by_country ?? [] as row}<option value={row.code}>{row.code}</option>{/each}
        </select>
      </label>
      <label>
        Language
        <select bind:value={language}>
          <option value="">All languages</option>
          <option value="en">English</option>
          <option value="fr">French</option>
          <option value="nl">Dutch</option>
          <option value="es">Spanish</option>
          <option value="lt">Lithuanian</option>
        </select>
      </label>
      <label>
        In force on
        <input type="date" bind:value={asOf} />
      </label>
    </div>
  </form>

  {#if results}
    <div class="retrieval-summary">
      <strong>{results.results.length} result(s)</strong>
      <span>{results.ranking}</span>
      {#if results.model_id}<span>BGE-M3 · model {results.model_id}</span>{/if}
      <span>
        {results.filters.country ?? 'all countries'} ·
        {results.filters.languages?.join(', ') ?? 'all languages'} ·
        {results.filters.as_of ?? 'all validities'}
      </span>
    </div>
    {#each results.results as hit (hit.chunk_id)}
      <details>
        <summary>
          <strong>{hit.citation ?? hit.context_header}</strong>
          <span class="badge {hit.version_status === 'in_force' ? 'pass' : 'pending'}">{hit.version_status}</span>
          <span class="muted">
            {hit.country} · {hit.lang} · {hit.authenticity.replaceAll('_', ' ')} · score {formatScore(hit.score)}
          </span>
        </summary>
        <div class="score-breakdown" aria-label="Retrieval score breakdown">
          <div>
            <span class="score-label">Full text</span>
            <strong>{hit.full_text_rank ? `#${hit.full_text_rank}` : 'No match'}</strong>
            <span>raw {formatScore(hit.full_text_score, 4)}</span>
            <span>RRF +{formatScore(hit.full_text_contribution)}</span>
          </div>
          <div>
            <span class="score-label">BGE-M3</span>
            <strong>{hit.vector_rank ? `#${hit.vector_rank}` : 'Not ranked'}</strong>
            <span>similarity {formatScore(vectorSimilarity(hit.vector_distance), 4)}</span>
            <span>distance {formatScore(hit.vector_distance, 4)}</span>
            <span>RRF +{formatScore(hit.vector_contribution)}</span>
          </div>
          <div class="score-total">
            <span class="score-label">Final</span>
            <strong>{formatScore(hit.score)}</strong>
          </div>
        </div>
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
  .search-form { display: flex; flex-direction: column; gap: 0.65rem; }
  .search-query input { min-height: 2.35rem; }
  .search-options { display: flex; gap: 0.75rem; align-items: end; flex-wrap: wrap; }
  .segmented { display: inline-flex; border: 1px solid var(--border); border-radius: 6px; overflow: hidden; }
  .segmented button { border: 0; border-right: 1px solid var(--border); border-radius: 0; min-height: 2.1rem; }
  .segmented button:last-child { border-right: 0; }
  .segmented button.active { background: var(--accent); color: white; }
  .retrieval-summary {
    display: flex;
    gap: 0.45rem 0.9rem;
    align-items: baseline;
    flex-wrap: wrap;
    padding: 0.55rem 0;
    border-bottom: 1px solid var(--border);
    color: var(--muted);
  }
  .retrieval-summary strong { color: var(--text); }
  details { border-top: 1px solid var(--border); padding: 0.5rem 0; }
  summary { cursor: pointer; display: flex; gap: 0.5rem; align-items: baseline; flex-wrap: wrap; }
  .score-breakdown {
    display: grid;
    grid-template-columns: minmax(12rem, 1fr) minmax(16rem, 1.3fr) minmax(7rem, 0.5fr);
    border: 1px solid var(--border);
    border-radius: 6px;
    margin: 0.65rem 0;
  }
  .score-breakdown > div {
    display: flex;
    gap: 0.45rem 0.75rem;
    align-items: baseline;
    flex-wrap: wrap;
    padding: 0.55rem 0.7rem;
    border-right: 1px solid var(--border);
  }
  .score-breakdown > div:last-child { border-right: 0; }
  .score-breakdown span { color: var(--muted); font-size: 0.82rem; }
  .score-breakdown .score-label { color: var(--text); font-weight: 600; }
  .score-total { background: var(--panel-2); }
  @media (max-width: 1100px) { .tables { grid-template-columns: 1fr; } }
  @media (max-width: 760px) {
    .score-breakdown { grid-template-columns: 1fr; }
    .score-breakdown > div { border-right: 0; border-bottom: 1px solid var(--border); }
    .score-breakdown > div:last-child { border-bottom: 0; }
    .segmented { width: 100%; }
    .segmented button { flex: 1; }
  }
</style>
