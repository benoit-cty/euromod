<script>
  // Cited legal texts with the supporting extract highlighted — the reviewer
  // must be able to see the value in the law, not trust the model. Each hit can
  // be read in any language the DB holds for that version (authentic renderings,
  // official translations, machine translations), fetched on demand.
  import { api } from '../api.js';

  let { trace = [], extract = null, citedChunkId = null, dbUrl = '' } = $props();

  // chunk_id -> { loading, error, renderings[] } ; chunk_id -> unit_text_id
  let langs = $state({});
  let chosen = $state({});
  // chunk_id -> bool. `open` is a reactive attribute: without remembering what
  // the reviewer opened, picking a language would slam the panel shut again.
  let opened = $state({});
  const requested = new Set(); // plain: guards the fetch, must not be reactive

  const AUTHENTICITY_LABEL = {
    authentic: 'original',
    official_translation: 'official translation',
    machine_translation: 'machine translation',
  };

  async function loadLangs(chunkId) {
    if (!dbUrl || !chunkId || requested.has(chunkId)) return;
    requested.add(chunkId);
    langs[chunkId] = { loading: true, error: '', renderings: [] };
    try {
      const res = await api.chunkRenderings(dbUrl, chunkId);
      langs[chunkId] = { loading: false, error: '', renderings: res.renderings };
    } catch (e) {
      langs[chunkId] = { loading: false, error: String(e), renderings: [] };
    }
  }

  // the cited hit is open on arrival, so its languages load without a click
  $effect(() => {
    if (citedChunkId && dbUrl) loadLangs(citedChunkId);
  });

  // explicit pick, else the cited rendering from the DB (which also fills in
  // hits whose trace stored no content)
  function selected(hit) {
    const list = langs[hit.chunk_id]?.renderings ?? [];
    return (
      list.find((r) => r.unit_text_id === chosen[hit.chunk_id]) ??
      list.find((r) => r.is_cited) ??
      null
    );
  }

  function shownText(hit) {
    return selected(hit)?.content ?? hit.content ?? '';
  }

  function esc(text) {
    return text
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;');
  }

  function highlight(hit) {
    const safe = esc(shownText(hit));
    const rendering = selected(hit);
    // the extract is verbatim in the cited rendering only — never in a translation
    if (!extract || hit.chunk_id !== citedChunkId) return safe;
    if (rendering && !rendering.is_cited) return safe;
    const target = esc(extract);
    return safe.includes(target) ? safe.replace(target, `<mark>${target}</mark>`) : safe;
  }

  function langLabel(r) {
    const kind = AUTHENTICITY_LABEL[r.authenticity] ?? r.authenticity;
    return `${r.lang.toUpperCase()} · ${kind}`;
  }
</script>

<div>
  <h3>Cited legal text ({trace.length} retrieved)</h3>
  {#each trace as hit (hit.chunk_id)}
    <details
      open={opened[hit.chunk_id] ?? hit.chunk_id === citedChunkId}
      ontoggle={(e) => {
        opened[hit.chunk_id] = e.currentTarget.open;
        if (e.currentTarget.open) loadLangs(hit.chunk_id);
      }}
    >
      <summary>
        <strong>{hit.citation ?? hit.context_header}</strong>
        <span class="muted">
          {hit.method} · {hit.lang} · {hit.validity} · {hit.version_status}
          {#if hit.score != null}· score {hit.score.toFixed(3)}{/if}
        </span>
        {#if hit.chunk_id === citedChunkId}<span class="badge pass">cited</span>{/if}
      </summary>

      {#if langs[hit.chunk_id]?.loading}
        <p class="muted">loading languages…</p>
      {:else if langs[hit.chunk_id]?.error}
        <p class="muted">languages unavailable: {langs[hit.chunk_id].error}</p>
      {:else if langs[hit.chunk_id]?.renderings.length > 1}
        <div class="langs">
          <span class="muted">Language</span>
          {#each langs[hit.chunk_id].renderings as rendering}
            <button
              class:primary={selected(hit)?.unit_text_id === rendering.unit_text_id}
              title={rendering.mt_engine
                ? `machine translation from ${rendering.source_lang} (${rendering.mt_engine})`
                : rendering.source_lang
                  ? `translated from ${rendering.source_lang}`
                  : 'original language of this version'}
              onclick={() => (chosen[hit.chunk_id] = rendering.unit_text_id)}
            >
              {langLabel(rendering)}
            </button>
          {/each}
        </div>
      {:else if langs[hit.chunk_id]}
        <p class="muted">only one language stored for this version</p>
      {/if}

      {#if selected(hit) && !selected(hit).is_cited}
        <p class="muted">
          Showing a {AUTHENTICITY_LABEL[selected(hit).authenticity] ?? selected(hit).authenticity} —
          the verbatim extract is highlighted in the cited rendering only.
          {#if !selected(hit).aligned}
            No chunk with this offset in that language: the full version text is shown.
          {/if}
        </p>
      {/if}

      {#if shownText(hit)}
        <div class="law-text">{@html highlight(hit)}</div>
      {:else}
        <p class="muted">content not stored in trace</p>
      {/if}
      <p class="muted mono">chunk {selected(hit)?.chunk_id ?? hit.chunk_id}</p>
    </details>
  {:else}
    <p class="muted">No retrieval trace.</p>
  {/each}
</div>

<style>
  details { margin-bottom: 0.6rem; }
  summary { cursor: pointer; display: flex; gap: 0.5rem; align-items: baseline; flex-wrap: wrap; }
  p { margin: 0.25rem 0; }
  .langs { display: flex; align-items: center; gap: 0.3rem; flex-wrap: wrap; margin: 0.35rem 0; }
  .langs button { font-size: 0.8rem; padding: 0.15rem 0.45rem; }
</style>
