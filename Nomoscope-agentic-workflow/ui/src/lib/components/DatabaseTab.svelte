<script>
  import { api } from '../api.js';
  import { renderView, splitSentences } from '../highlight.js';
  import { countryName, formatCount, humanize } from '../labels.js';
  import { countryReadiness } from '../readiness.js';
  import Icon from './Icon.svelte';

  const LANGUAGES = { en: 'English', fr: 'French', nl: 'Dutch', es: 'Spanish', lt: 'Lithuanian' };
  const langName = (code) => LANGUAGES[code] ?? code;

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
  // Sentence scoring per hit: chunk_id -> { status: 'loading'|'done'|'error', similarities, error }.
  // The top EAGER_HITS are scored right after a search in one encoder batch;
  // the rest when their <details> is expanded.
  let sentenceScores = $state({});
  let searchToken = 0;
  const EAGER_HITS = 5;

  const modes = [
    { value: 'hybrid', label: 'Best match', hint: 'words and meaning combined (recommended)' },
    { value: 'full_text', label: 'Exact words', hint: 'only texts containing your words' },
    { value: 'vector', label: 'Similar meaning', hint: 'texts about the same thing, in any wording' },
  ];

  // Per-country one-liners for the collapsed library summary.
  const countryRows = $derived.by(() => {
    if (!stats) return [];
    const inputs = new Map((stats.model_inputs?.by_country ?? []).map((r) => [r.code, r]));
    return stats.by_country.map((row) => ({ row, ...countryReadiness(row, inputs.get(row.code)) }));
  });
  const readyCount = $derived(countryRows.filter((c) => c.level === 'ready').length);

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
      sentenceScores = {};
      searchToken += 1;
      scoreHits(results.results.slice(0, EAGER_HITS), results.query, searchToken);
    } catch (e) {
      error = String(e);
      results = null;
    } finally {
      searching = false;
    }
  }

  // One encoder round trip for several hits: their scorable sentences are
  // flattened into a single batch and the similarities dealt back per hit.
  async function scoreHits(hits, forQuery, token) {
    const pending = hits.filter((hit) => !sentenceScores[hit.chunk_id]);
    if (pending.length === 0) return;
    const plan = pending.map((hit) => {
      const sentences = splitSentences(hit.content);
      return { hit, sentences, indices: sentences.map((s, i) => (s.scorable ? i : -1)).filter((i) => i >= 0) };
    });
    for (const { hit } of plan) sentenceScores[hit.chunk_id] = { status: 'loading' };
    const batch = plan.flatMap(({ sentences, indices }) => indices.map((i) => sentences[i].text));
    try {
      const similarities = await api.scoreSentences(url, forQuery, batch);
      if (token !== searchToken) return; // a newer search replaced these hits
      let offset = 0;
      for (const { hit, sentences, indices } of plan) {
        const perSentence = sentences.map(() => null);
        for (const i of indices) perSentence[i] = similarities[offset++];
        sentenceScores[hit.chunk_id] = { status: 'done', similarities: perSentence };
      }
    } catch (e) {
      if (token !== searchToken) return;
      for (const { hit } of plan) sentenceScores[hit.chunk_id] = { status: 'error', error: String(e) };
    }
  }

  function onToggle(event, hit) {
    if (event.currentTarget.open) scoreHits([hit], results.query, searchToken);
  }

  const scoringCount = $derived(Object.values(sentenceScores).filter((s) => s.status === 'loading').length);

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

<div class="db">
  <section class="panel search-panel">
    <form class="search-form" onsubmit={search}>
      <div class="search-query">
        <span class="search-icon"><Icon name="search" size={20} /></span>
        <input
          class="query"
          placeholder="Describe what you are looking for, e.g. income tax brackets and rates"
          bind:value={query}
        />
        <button class="primary big" type="submit" disabled={searching || !query.trim()}>
          {#if searching}<span class="spinner"></span> Searching…{:else}Search{/if}
        </button>
      </div>
      <div class="search-options">
        <label class="field inline-field">
          Country
          <select bind:value={country}>
            <option value="">All countries</option>
            {#each stats?.by_country ?? [] as row}<option value={row.code}>{countryName(row.code)}</option>{/each}
          </select>
        </label>
        <label class="field inline-field">
          In force on
          <input type="date" bind:value={asOf} />
        </label>
        <details class="options">
          <summary>More options</summary>
          <div class="options-body">
            <div class="field">
              Search method
              <div class="segmented" aria-label="Search method">
                {#each modes as item}
                  <button
                    type="button"
                    class:active={mode === item.value}
                    aria-pressed={mode === item.value}
                    title={item.hint}
                    onclick={() => (mode = item.value)}
                  >{item.label}</button>
                {/each}
              </div>
            </div>
            <label class="field">
              Language of the text
              <select bind:value={language}>
                <option value="">Any language</option>
                {#each Object.entries(LANGUAGES) as [code, name]}<option value={code}>{name}</option>{/each}
              </select>
            </label>
          </div>
        </details>
      </div>
    </form>
  </section>

  {#if error}<p class="callout err">{error}</p>{/if}

  {#if results}
    <section class="results">
      {#if results.notice}<p class="callout info">{results.notice}</p>{/if}
      <div class="retrieval-summary">
        <strong>{results.results.length} result{results.results.length === 1 ? '' : 's'}</strong>
        {#if scoringCount > 0}
          <span class="scoring"><span class="spinner" aria-hidden="true"></span> Highlighting the most relevant sentences…</span>
        {:else if results.results.length}
          <span class="legend" aria-label="Highlight legend">
            <span class="swatch best"></span> most likely answer
            <span class="swatch near"></span> close
            {#if results.mode !== 'vector'}<mark>word</mark> your words{/if}
          </span>
        {/if}
      </div>
      {#each results.results as hit, i (hit.chunk_id)}
        {@const scoring = sentenceScores[hit.chunk_id]}
        <details class="hit" open={i === 0} ontoggle={(event) => onToggle(event, hit)}>
          <summary>
            <div class="hit-title">
              <strong>{hit.citation ?? hit.context_header}</strong>
              <div class="hit-meta">
                <span class="badge">{countryName(hit.country)}</span>
                <span class="badge">{langName(hit.lang)}{hit.authenticity !== 'authentic' ? ` · ${humanize(hit.authenticity)}` : ''}</span>
                <span class="badge {hit.version_status === 'in_force' ? 'pass' : 'pending'}">
                  {hit.version_status === 'in_force' ? 'In force' : humanize(hit.version_status)}
                </span>
              </div>
            </div>
          </summary>
          <div class="hit-body">
            {#if hit.context_header && hit.citation}<p class="muted small">{hit.context_header}</p>{/if}
            {#if scoring?.status === 'error'}
              <p class="muted small">Sentence highlighting unavailable: {scoring.error}</p>
            {/if}
            <div class="law-text">
              {#each renderView(hit.content, hit.headline, scoring?.similarities) as sentence}
                <span
                  class="sentence"
                  class:best={sentence.level === 'best'}
                  class:near={sentence.level === 'near'}
                  title={sentence.similarity != null ? `similarity ${formatScore(sentence.similarity, 3)}` : undefined}
                >{#each sentence.parts as part}{#if part.mark}<mark>{part.text}</mark>{:else}{part.text}{/if}{/each}</span>
              {/each}
            </div>
            <details class="why">
              <summary>Why this result?</summary>
              <p class="muted small">
                {results.ranking}
                {#if results.model_id}· embedding model {results.model_id}{/if}
              </p>
              <div class="score-breakdown" aria-label="Retrieval score breakdown">
                <div>
                  <span class="score-label">Word match</span>
                  <strong>{hit.full_text_rank ? `#${hit.full_text_rank}` : 'No match'}</strong>
                  <span>raw {formatScore(hit.full_text_score, 4)}</span>
                  <span>RRF +{formatScore(hit.full_text_contribution)}</span>
                </div>
                <div>
                  <span class="score-label">Meaning match</span>
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
              <p class="muted mono">chunk {hit.chunk_id}</p>
            </details>
          </div>
        </details>
      {:else}
        <div class="empty-state">
          <span class="big">Nothing found</span>
          <span>Try other words, another country, or remove the date.</span>
        </div>
      {/each}
    </section>
  {:else if !searching}
    <div class="empty-state">
      <Icon name="book" size={32} />
      <span class="big">Search the library</span>
      <span>Ask in plain English; texts in other languages are found too.</span>
    </div>
  {/if}

  <details class="more">
    <summary>
      Library status
      <span class="hint">
        {#if stats}
          {formatCount(stats.totals.instruments)} laws and texts · {readyCount} of {countryRows.length} countries fully ready
        {:else if loading}
          loading…
        {/if}
      </span>
    </summary>
    <div class="body">
      {#if stats}
        <table class="summary-table">
          <thead>
            <tr><th>Country</th><th>Laws and texts</th><th>Searchable</th><th>Available in English</th><th>Status</th></tr>
          </thead>
          <tbody>
            {#each countryRows as c (c.row.code)}
              <tr>
                <td><strong>{countryName(c.row.code)}</strong></td>
                <td>{formatCount(c.row.instruments)}</td>
                <td>{c.embeddedPct == null ? '—' : `${c.embeddedPct}%`}</td>
                <td>{c.englishPct == null ? '—' : `${c.englishPct}%`}</td>
                <td>
                  {#if c.level === 'ready'}<span class="badge pass">Ready</span>
                  {:else}<span class="badge {c.level === 'partial' ? 'changed' : 'pending'}" title={c.problems.join('; ')}>
                    {c.problems[0]}</span>{/if}
                </td>
              </tr>
            {/each}
          </tbody>
        </table>

        <details class="more nested">
          <summary>Technical statistics <span class="hint">for the people maintaining the library</span></summary>
          <div class="body">
            <div class="row">
              <label class="field grow">
                Database URL
                <input bind:value={url} class="mono" />
              </label>
              <button onclick={loadStats} disabled={loading}>{loading ? 'Loading…' : 'Reload statistics'}</button>
            </div>
            <div class="cards">
              {#each Object.entries(stats.totals) as [key, count]}
                <div class="card">
                  <div class="num">{formatCount(count)}</div>
                  <div class="muted">{key.replaceAll('_', ' ')}</div>
                </div>
              {/each}
            </div>

            <div class="tables">
              <div>
                <h3>By jurisdiction</h3>
                <table>
                  <thead>
                    <tr><th>Code</th><th>Instr.</th><th>Units</th><th>Versions</th><th>In force</th><th>Texts</th><th>Chunks</th><th>Embedded</th></tr>
                  </thead>
                  <tbody>
                    {#each stats.by_country as row}
                      <tr>
                        <td><strong>{row.code}</strong></td>
                        <td>{row.instruments}</td>
                        <td>{row.legal_units}</td>
                        <td>{row.versions}</td>
                        <td>{row.in_force}</td>
                        <td>{row.texts}</td>
                        <td>{row.chunks}</td>
                        <td>{row.embedded_chunks}</td>
                      </tr>
                    {/each}
                  </tbody>
                </table>
              </div>
              <div>
                <h3>Translation status</h3>
                <table>
                  <thead>
                    <tr><th>Code</th><th>Authentic</th><th>Official transl.</th><th>Machine transl.</th></tr>
                  </thead>
                  <tbody>
                    {#each stats.by_country as row}
                      <tr>
                        <td><strong>{row.code}</strong></td>
                        <td>{row.authentic}</td>
                        <td>{row.official_translation}</td>
                        <td>{row.machine_translation}</td>
                      </tr>
                    {/each}
                  </tbody>
                </table>
              </div>
              <div class="wide">
                <h3>Model inputs</h3>
                <p class="muted note">
                  The two non-legislative inputs each country needs: its EUROMOD Country Report
                  (context for framing and display, never cited as evidence) and the enriched
                  parameter store loaded by <code>ingest-params</code>.
                </p>
                <table>
                  <thead>
                    <tr>
                      <th>Code</th>
                      <th>Country Report</th><th>CR chunks</th><th>CR embedded</th><th>CR loaded</th>
                      <th>Enriched parameters</th><th>Values</th><th>Income-year</th><th>Params loaded</th>
                    </tr>
                  </thead>
                  <tbody>
                    {#each stats.model_inputs.by_country as row}
                      {@const cr = row.country_report}
                      {@const p = row.parameters}
                      <tr>
                        <td><strong>{row.code}</strong></td>
                        <td>
                          {#if cr && cr.reports > 0}
                            <span class="badge pass" title={cr.ids ?? ''}>{cr.ids ?? 'loaded'}</span>
                          {:else}
                            <span class="badge pending">missing</span>
                          {/if}
                        </td>
                        <td>{cr?.chunks ?? 0}</td>
                        <td>{cr?.embedded_chunks ?? '—'}</td>
                        <td class="muted">{cr?.ingested_on ?? '—'}</td>
                        <td>
                          {#if p}
                            <span class="badge pass" title={p.source_files ?? ''}>{p.parameters}</span>
                          {:else if !stats.model_inputs.params_schema}
                            <span class="badge pending">no params schema</span>
                          {:else}
                            <span class="badge pending">missing</span>
                          {/if}
                        </td>
                        <td>{p?.model_values ?? '—'}</td>
                        <td>{p ? p.income_year : '—'}</td>
                        <td class="muted">{p?.ingested_on ?? '—'}</td>
                      </tr>
                    {/each}
                  </tbody>
                </table>
                {#if !stats.model_inputs.params_schema}
                  <p class="muted note">
                    The <code>params</code> schema does not exist in this database — run
                    <code>nomoscope-workflow init-param-db</code>, then <code>ingest-params</code>.
                  </p>
                {/if}
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
          </div>
        </details>
      {:else if !loading}
        <div class="row">
          <label class="field grow">
            Database URL
            <input bind:value={url} class="mono" />
          </label>
          <button onclick={loadStats}>Load statistics</button>
        </div>
      {/if}
    </div>
  </details>
</div>

<style>
  .db { overflow: auto; display: flex; flex-direction: column; gap: 1rem; min-height: 0; }
  .row { display: flex; gap: 0.5rem; align-items: end; flex-wrap: wrap; }
  .grow { flex: 1; min-width: 16rem; }
  .search-form { display: flex; flex-direction: column; gap: 0.8rem; }
  .search-query { display: flex; gap: 0.6rem; align-items: center; position: relative; }
  .search-icon { position: absolute; left: 0.85rem; color: var(--muted); display: flex; pointer-events: none; }
  .query { flex: 1; min-height: 2.9rem; font-size: 1.05rem; padding-left: 2.6rem; border-radius: 10px; }
  .search-options { display: flex; gap: 1rem; align-items: center; flex-wrap: wrap; }
  .inline-field { flex-direction: row; align-items: center; gap: 0.5rem; }
  .inline-field select, .inline-field input { width: auto; }
  .options > summary { cursor: pointer; color: var(--accent); font-size: 0.9rem; }
  .options[open] { flex-basis: 100%; }
  .options-body { display: flex; gap: 1.2rem; flex-wrap: wrap; align-items: end; padding-top: 0.6rem; }
  .results { display: flex; flex-direction: column; gap: 0.6rem; }
  .retrieval-summary { display: flex; gap: 0.9rem; align-items: baseline; flex-wrap: wrap; color: var(--muted); }
  .retrieval-summary strong { color: var(--text); }
  .legend { display: inline-flex; gap: 0.35rem; align-items: center; font-size: 0.82rem; }
  .legend mark { margin-left: 0.4rem; }
  .swatch { display: inline-block; width: 0.9rem; height: 0.9rem; border-radius: 3px; }
  .swatch.best, .sentence.best { background: var(--answer); }
  .swatch.near, .sentence.near { background: var(--answer-soft); }
  .swatch.near { border: 1px solid var(--border); }
  .sentence.best, .sentence.near { border-radius: 3px; box-shadow: 0 0 0 1px var(--answer-soft); }
  .scoring { display: inline-flex; gap: 0.4rem; align-items: center; font-size: 0.85rem; }
  .hit { background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius); box-shadow: var(--shadow); }
  .hit > summary { cursor: pointer; padding: 0.8rem 1rem; list-style: none; }
  .hit > summary::-webkit-details-marker { display: none; }
  .hit-title { display: flex; justify-content: space-between; gap: 0.8rem; flex-wrap: wrap; align-items: baseline; }
  .hit-meta { display: flex; gap: 0.35rem; flex-wrap: wrap; }
  .hit-body { padding: 0 1rem 0.9rem; display: flex; flex-direction: column; gap: 0.5rem; }
  .why > summary { cursor: pointer; color: var(--accent); font-size: 0.85rem; }
  .score-breakdown {
    display: grid;
    grid-template-columns: minmax(12rem, 1fr) minmax(16rem, 1.3fr) minmax(7rem, 0.5fr);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin: 0.5rem 0;
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
  .summary-table td, .summary-table th { padding: 0.45rem 0.6rem; }
  .nested { margin-top: 0.4rem; }
  .cards { display: flex; gap: 0.6rem; flex-wrap: wrap; }
  .card { background: var(--panel-2); border-radius: 8px; padding: 0.55rem 0.85rem; min-width: 7.5rem; }
  .num { font-size: 1.25rem; font-weight: 700; }
  .tables { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; align-items: start; }
  .tables .wide { grid-column: 1 / -1; }
  .note { margin: 0 0 0.4rem; font-size: 0.82rem; }
  @media (max-width: 1100px) { .tables { grid-template-columns: 1fr; } }
  @media (max-width: 760px) {
    .score-breakdown { grid-template-columns: 1fr; }
    .score-breakdown > div { border-right: 0; border-bottom: 1px solid var(--border); }
  }
</style>
