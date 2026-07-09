<script>
  // Cited legal texts with the supporting extract highlighted — the reviewer
  // must be able to see the value in the law, not trust the model.
  let { trace = [], extract = null, citedChunkId = null } = $props();

  function esc(text) {
    return text
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;');
  }

  function highlight(hit) {
    const safe = esc(hit.content ?? '');
    if (!extract || hit.chunk_id !== citedChunkId) return safe;
    const target = esc(extract);
    return safe.includes(target) ? safe.replace(target, `<mark>${target}</mark>`) : safe;
  }
</script>

<div>
  <h3>Cited legal text ({trace.length} retrieved)</h3>
  {#each trace as hit (hit.chunk_id)}
    <details open={hit.chunk_id === citedChunkId}>
      <summary>
        <strong>{hit.citation ?? hit.context_header}</strong>
        <span class="muted">
          {hit.method} · {hit.lang} · {hit.validity} · {hit.version_status}
          {#if hit.score != null}· score {hit.score.toFixed(3)}{/if}
        </span>
        {#if hit.chunk_id === citedChunkId}<span class="badge pass">cited</span>{/if}
      </summary>
      {#if hit.content}
        <div class="law-text">{@html highlight(hit)}</div>
      {:else}
        <p class="muted">content not stored in trace</p>
      {/if}
      <p class="muted mono">chunk {hit.chunk_id}</p>
    </details>
  {:else}
    <p class="muted">No retrieval trace.</p>
  {/each}
</div>

<style>
  details { margin-bottom: 0.6rem; }
  summary { cursor: pointer; display: flex; gap: 0.5rem; align-items: baseline; flex-wrap: wrap; }
  p { margin: 0.25rem 0; }
</style>
