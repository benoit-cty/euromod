<script>
  // Add sources › Translate texts: a `translate` job for the texts with no
  // version in the target language. The model is picked from the list the
  // worker publishes (ops.worker_models), never typed: a free-text model
  // string is how a wrong deployment went unnoticed for a month.
  import { worker } from '../api.js';
  import ModelPicker from '@shared/components/ModelPicker.svelte';

  let model = $state('');
  let targetLang = $state('en');
  let trLimit = $state('');
  let requestTimeout = $state(120);
  let trDryRun = $state(false);

  const optionalInt = (value) => (String(value).trim() ? Number(String(value).trim()) : null);

  /** The job to submit; throws when there is no model to translate with. */
  export function request() {
    if (!model) throw new Error('no model to translate with — the worker has published none');
    return {
      job_type: 'translate',
      payload: {
        model,
        target_lang: targetLang.trim(),
        limit: optionalInt(trLimit),
        request_timeout: optionalInt(requestTimeout) ?? 120,
        dry_run: Boolean(trDryRun),
      },
    };
  }
</script>

<div class="subform">
  <p class="muted">Machine-translate texts that have no version in the target language yet.</p>
  <div class="form-grid">
    <label class="field wide">
      Language model
      <ModelPicker models={worker.llmModels} bind:value={model} />
    </label>
    <label class="field">
      Into
      <input bind:value={targetLang} placeholder="en" />
    </label>
  </div>
  <details class="more">
    <summary>Advanced <span class="hint">timeout, limit</span></summary>
    <div class="body form-grid">
      <label class="field">
        Request timeout (s)
        <input type="number" min="1" bind:value={requestTimeout} />
      </label>
      <label class="field">
        Limit
        <input type="number" min="1" bind:value={trLimit} placeholder="all" />
      </label>
      <label class="field check">
        <input type="checkbox" bind:checked={trDryRun} />
        Only count, change nothing
      </label>
    </div>
  </details>
</div>

<style>
  .subform { display: flex; flex-direction: column; gap: 0.9rem; }
  .subform > p.muted { margin: 0; }
</style>
