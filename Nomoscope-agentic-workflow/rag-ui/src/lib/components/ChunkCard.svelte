<script>
  // One passage of the corpus: citation, version window, trust class, and the
  // text — with the quoted extract marked when there is one, or the search
  // terms when it comes from the direct search. Other language renderings
  // (authentic / machine translation) load on demand.
  import { api } from '../api.js';
  import { headlineRuns, locateExtract } from '../chat.js';

  let {
    chunk,
    dbUrl,
    label = '',
    extract = '',
    verified = null,
    headline = null,
    active = false,
    open = false,
  } = $props();

  let expanded = $state(false);
  let renderings = $state(null);
  let renderingIdx = $state(0);
  let loadError = $state('');
  let card = $state(null);

  $effect(() => {
    expanded = open;
  });
  $effect(() => {
    if (active && card) card.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  });

  const shown = $derived(renderings ? renderings[renderingIdx] : null);
  const content = $derived(shown ? shown.content : chunk.content ?? '');
  const located = $derived(extract ? locateExtract(content, extract) : null);
  const runs = $derived(!extract && headline && !shown ? headlineRuns(headline) : null);
  const preview = $derived((chunk.content ?? '').slice(0, 220));

  async function loadRenderings() {
    loadError = '';
    try {
      const res = await api.chunkRenderings(dbUrl, chunk.chunk_id);
      renderings = res.renderings;
      renderingIdx = 0;
    } catch (e) {
      loadError = String(e);
    }
  }

  function validityText(v) {
    if (!v) return '';
    const m = v.match(/[[(]([\d-]*),([\d-]*)[\])]/);
    if (!m) return v;
    return m[2] ? `${m[1]} → ${m[2]}` : `in force since ${m[1]}`;
  }
</script>

<article class="card" class:active bind:this={card}>
  <header>
    {#if label}<span class="label">{label}</span>{/if}
    <strong class="cit">{chunk.citation ?? chunk.context_header ?? 'passage'}</strong>
    {#if verified === true}<span class="badge ok" title="found character-for-character in this chunk">verbatim ✓</span>{/if}
    {#if verified === false}<span class="badge err" title="not found in the chunk — do not rely on it">not verbatim ✗</span>{/if}
    {#if chunk.source_trust_class === 'guidance'}<span class="badge warn" title="circular / doctrine: citable, but not legislation">guidance</span>{/if}
    {#if chunk.country}<span class="badge">{chunk.country}</span>{/if}
    {#if chunk.lang}<span class="badge">{chunk.lang}</span>{/if}
  </header>
  <div class="meta muted small">
    {#if chunk.context_header && chunk.citation}<span>{chunk.context_header}</span>{/if}
    {#if chunk.validity}<span>{validityText(chunk.validity)}</span>{/if}
  </div>

  {#if extract && !expanded}
    <blockquote class="extract">{extract}</blockquote>
  {/if}

  {#if expanded}
    {#if renderings}
      <div class="langs">
        {#each renderings as r, i (r.unit_text_id)}
          <button class:on={i === renderingIdx} onclick={() => (renderingIdx = i)} title={r.mt_engine ?? r.authenticity}>
            {r.lang}{r.authenticity === 'machine_translation' ? ' (MT)' : ''}
          </button>
        {/each}
      </div>
    {/if}
    <div class="text">
      {#if located}{located.before}<mark>{located.match}</mark>{located.after}{:else if runs}{#each runs as run}{#if run.hit}<mark>{run.text}</mark>{:else}{run.text}{/if}{/each}{:else}{content}{/if}
    </div>
    {#if extract && !located}
      <p class="muted small">The extract does not occur in this rendering.</p>
    {/if}
  {:else if !extract}
    <div class="text clamp">{#if runs}{#each runs as run}{#if run.hit}<mark>{run.text}</mark>{:else}{run.text}{/if}{/each}{:else}{preview}{(chunk.content ?? '').length > 220 ? '…' : ''}{/if}</div>
  {/if}

  <footer>
    <button class="link small" onclick={() => (expanded = !expanded)}>{expanded ? 'Collapse' : 'Full text'}</button>
    {#if expanded && !renderings}
      <button class="link small" onclick={loadRenderings}>Other languages</button>
    {/if}
    <span class="mono muted" title="chunks.id">{chunk.chunk_id.slice(0, 8)}</span>
  </footer>
  {#if loadError}<p class="banner err small">{loadError}</p>{/if}
</article>

<style>
  .card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 0.55rem 0.7rem;
    margin-bottom: 0.5rem;
  }
  .card.active { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-soft); }
  header { display: flex; flex-wrap: wrap; gap: 0.35rem; align-items: center; }
  .label { font-weight: 600; color: var(--accent); }
  .cit { font-size: 0.95em; }
  .meta { display: flex; flex-wrap: wrap; gap: 0.8rem; margin: 0.15rem 0 0.3rem; }
  .extract { margin: 0.3rem 0; padding: 0.3rem 0.6rem; border-left: 3px solid var(--accent); background: var(--panel-2); border-radius: 0 var(--radius) var(--radius) 0; white-space: pre-wrap; }
  .text { white-space: pre-wrap; line-height: 1.45; font-size: 0.92em; max-height: 28rem; overflow-y: auto; }
  .text.clamp { max-height: 5.5rem; overflow: hidden; color: var(--muted); }
  .langs { display: flex; gap: 0.3rem; margin-bottom: 0.3rem; }
  .langs button { padding: 0.05rem 0.45rem; font-size: 0.8em; }
  .langs button.on { background: var(--accent-soft); border-color: var(--accent); font-weight: 600; }
  footer { display: flex; gap: 0.8rem; align-items: center; margin-top: 0.3rem; }
  footer .mono { margin-left: auto; }
</style>
