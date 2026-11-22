<script>
  // Legislation › search: the article search (`search_articles`: hybrid,
  // words or meaning, over the chunks in force on a date), each hit with its
  // matched words marked and — scored on the worker — the sentence that most
  // likely answers tinted.
  import { api } from '../api.js';
  import { library } from '../library.svelte.js';
  import { renderView, splitSentences } from '../highlight.js';
  import { authenticityLabel, countryName, trustLabel, versionStatusLabel } from '@shared/lib/labels.js';
  import { formatFixed } from '@shared/lib/format.js';
  import Icon from '@shared/components/Icon.svelte';

  const LANGUAGES = { en: 'English', fr: 'French', nl: 'Dutch', es: 'Spanish', lt: 'Lithuanian' };
  const langName = (code) => LANGUAGES[code] ?? code;

  let error = $state('');
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

  // the countries the library holds (statistics shared with the other pages)
  const stats = $derived(library.stats);

  const vectorSimilarity = (distance) => (distance == null ? null : 1 - Number(distance));

  async function search(event) {
    event?.preventDefault();
    if (!query.trim()) return;
    searching = true;
    error = '';
    try {
      results = await api.searchArticles({
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
      const similarities = await api.scoreSentences(forQuery, batch);
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

  /** Run the current search again (the shell's Refresh): a corpus that changed under us. */
  export async function rerun() {
    if (results) await search();
  }
</script>

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
                >
                  {item.label}
                </button>
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
        <span class="scoring">
          <span class="spinner" aria-hidden="true"></span> Highlighting the most relevant sentences…
        </span>
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
              <span class="badge" title={authenticityLabel(hit.authenticity).hint}>
                {langName(hit.lang)}{hit.authenticity !== 'authentic'
                  ? ` · ${authenticityLabel(hit.authenticity).label}`
                  : ''}
              </span>
              <span
                class="badge {hit.version_status === 'in_force' ? 'pass' : 'pending'}"
                title={versionStatusLabel(hit.version_status).hint}
              >
                {versionStatusLabel(hit.version_status).label}
              </span>
              {#if hit.source_trust_class && hit.source_trust_class !== 'evidence'}
                {@const trust = trustLabel(hit.source_trust_class)}
                <span class="badge {trust.raw}" title="{trust.hint} ({trust.raw})">{trust.label}</span>
              {/if}
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
                title={sentence.similarity != null ? `similarity ${formatFixed(sentence.similarity, 3)}` : undefined}
              >
                {#each sentence.parts as part}{#if part.mark}<mark>{part.text}</mark>{:else}{part.text}{/if}{/each}
              </span>
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
                <span>raw {formatFixed(hit.full_text_score, 4)}</span>
                <span>RRF +{formatFixed(hit.full_text_contribution, 5)}</span>
              </div>
              <div>
                <span class="score-label">Meaning match</span>
                <strong>{hit.vector_rank ? `#${hit.vector_rank}` : 'Not ranked'}</strong>
                <span>similarity {formatFixed(vectorSimilarity(hit.vector_distance), 4)}</span>
                <span>distance {formatFixed(hit.vector_distance, 4)}</span>
                <span>RRF +{formatFixed(hit.vector_contribution, 5)}</span>
              </div>
              <div class="score-total">
                <span class="score-label">Final</span>
                <strong>{formatFixed(hit.score, 5)}</strong>
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

<style>
  .search-form {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
  }
  .search-query {
    display: flex;
    gap: 0.6rem;
    align-items: center;
    position: relative;
  }
  .search-icon {
    position: absolute;
    left: 0.85rem;
    color: var(--muted);
    display: flex;
    pointer-events: none;
  }
  .query {
    flex: 1;
    min-height: 2.9rem;
    font-size: 1.05rem;
    padding-left: 2.6rem;
    border-radius: 10px;
  }
  .search-options {
    display: flex;
    gap: 1rem;
    align-items: center;
    flex-wrap: wrap;
  }
  .inline-field {
    flex-direction: row;
    align-items: center;
    gap: 0.5rem;
  }
  .inline-field select,
  .inline-field input {
    width: auto;
  }
  .options > summary {
    cursor: pointer;
    color: var(--accent);
    font-size: 0.9rem;
  }
  .options[open] {
    flex-basis: 100%;
  }
  .options-body {
    display: flex;
    gap: 1.2rem;
    flex-wrap: wrap;
    align-items: end;
    padding-top: 0.6rem;
  }
  .results {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
  }
  .retrieval-summary {
    display: flex;
    gap: 0.9rem;
    align-items: baseline;
    flex-wrap: wrap;
    color: var(--muted);
  }
  .retrieval-summary strong {
    color: var(--text);
  }
  .legend {
    display: inline-flex;
    gap: 0.35rem;
    align-items: center;
    font-size: 0.82rem;
  }
  .legend mark {
    margin-left: 0.4rem;
  }
  .swatch {
    display: inline-block;
    width: 0.9rem;
    height: 0.9rem;
    border-radius: 3px;
  }
  .swatch.best,
  .sentence.best {
    background: var(--answer);
  }
  .swatch.near,
  .sentence.near {
    background: var(--answer-soft);
  }
  .swatch.near {
    border: 1px solid var(--border);
  }
  .sentence.best,
  .sentence.near {
    border-radius: 3px;
    box-shadow: 0 0 0 1px var(--answer-soft);
  }
  .scoring {
    display: inline-flex;
    gap: 0.4rem;
    align-items: center;
    font-size: 0.85rem;
  }
  .hit {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
  }
  .hit > summary {
    cursor: pointer;
    padding: 0.8rem 1rem;
    list-style: none;
  }
  .hit > summary::-webkit-details-marker {
    display: none;
  }
  .hit-title {
    display: flex;
    justify-content: space-between;
    gap: 0.8rem;
    flex-wrap: wrap;
    align-items: baseline;
  }
  .hit-meta {
    display: flex;
    gap: 0.35rem;
    flex-wrap: wrap;
  }
  .hit-body {
    padding: 0 1rem 0.9rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .why > summary {
    cursor: pointer;
    color: var(--accent);
    font-size: 0.85rem;
  }
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
  .score-breakdown > div:last-child {
    border-right: 0;
  }
  .score-breakdown span {
    color: var(--muted);
    font-size: 0.82rem;
  }
  .score-breakdown .score-label {
    color: var(--text);
    font-weight: 600;
  }
  .score-total {
    background: var(--panel-2);
  }
  @media (max-width: 760px) {
    .score-breakdown {
      grid-template-columns: 1fr;
    }
    .score-breakdown > div {
      border-right: 0;
      border-bottom: 1px solid var(--border);
    }
  }
</style>
