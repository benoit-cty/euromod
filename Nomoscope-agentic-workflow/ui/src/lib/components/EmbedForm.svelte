<script>
  // Add sources › Make new texts searchable: an `embed` job for the chunks
  // with no vector yet. Backend, model path and device are the worker's
  // business: it runs BGE-M3 on whatever it has (CUDA, else CPU). The form
  // only says what to embed; a contributed document's follow-up build uses
  // the same settings (`payload()`).
  let modelId = $state(1);
  let batchSize = $state(16);
  let embLimit = $state('');
  let embDryRun = $state(false);

  const optionalInt = (value) => (String(value).trim() ? Number(String(value).trim()) : null);

  export function payload() {
    return {
      model_id: Number(modelId),
      batch_size: Number(batchSize),
      limit: optionalInt(embLimit),
      dry_run: Boolean(embDryRun),
    };
  }

  /** The job to submit. */
  export function request() {
    return { job_type: 'embed', payload: payload() };
  }
</script>

<div class="subform">
  <p class="muted">
    Index the texts that are not searchable yet. Runs on the worker; needed after any import (adding a document does it
    for you).
  </p>
  <details class="more">
    <summary>Advanced <span class="hint">model, batch size, limit</span></summary>
    <div class="body form-grid">
      <label class="field">
        Model id
        <input type="number" min="1" bind:value={modelId} />
      </label>
      <label class="field">
        Batch size
        <input type="number" min="1" bind:value={batchSize} />
      </label>
      <label class="field">
        Limit
        <input type="number" min="1" bind:value={embLimit} placeholder="all" />
      </label>
      <label class="field check">
        <input type="checkbox" bind:checked={embDryRun} />
        Only count, change nothing
      </label>
    </div>
  </details>
</div>

<style>
  .subform {
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
  }
  .subform > p.muted {
    margin: 0;
  }
</style>
