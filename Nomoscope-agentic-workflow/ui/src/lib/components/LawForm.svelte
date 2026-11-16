<script>
  // Add sources › An official law: an `ingest` job by the law's official
  // identifier or by a citation, fetched from the national portal with all its
  // articles and versions.
  import { countryName } from '@shared/lib/labels.js';

  // the jurisdictions the library holds
  let { jurisdictions = ['FR'] } = $props();

  let ingMode = $state('instrument'); // instrument | citation
  let jurisdiction = $state('fr');
  let nationalId = $state('');
  let citationText = $state('');
  let asOf = $state('');
  let sourceCode = $state('');
  let maxItems = $state(500);

  /** The job to submit; throws with what is missing. */
  export function request() {
    const args = [];
    if (ingMode === 'instrument') {
      if (!jurisdiction.trim() || !nationalId.trim()) throw new Error('jurisdiction and national id are required');
      args.push(jurisdiction.trim(), nationalId.trim());
    } else {
      if (!jurisdiction.trim() || !citationText.trim() || !asOf)
        throw new Error('jurisdiction, citation and as-of date are required');
      args.push(jurisdiction.trim(), citationText.trim(), asOf);
    }
    if (sourceCode.trim()) args.push('--source-code', sourceCode.trim());
    args.push('--max-items', String(maxItems));
    return { job_type: 'ingest', payload: { command: ingMode, args } };
  }
</script>

<div class="subform">
  <p class="muted">
    Give the law’s official reference; the importer fetches it from the national portal with all its
    articles and versions.
  </p>
  <div class="form-grid">
    <label class="field">
      Country
      <select bind:value={jurisdiction}>
        {#each jurisdictions as code (code)}
          <option value={code.toLowerCase()}>{countryName(code)}</option>
        {/each}
      </select>
    </label>
    <label class="field">
      I know its
      <select bind:value={ingMode}>
        <option value="instrument">official identifier</option>
        <option value="citation">citation (e.g. “CGI art. 197”)</option>
      </select>
    </label>
    {#if ingMode === 'instrument'}
      <label class="field wide">
        Official identifier
        <input bind:value={nationalId} placeholder="e.g. JORFTEXT000051168007" />
      </label>
    {:else}
      <label class="field wide">
        Citation
        <input bind:value={citationText} placeholder="e.g. CGI art. 197" />
      </label>
      <label class="field">
        Version in force on
        <input type="date" bind:value={asOf} />
      </label>
    {/if}
  </div>
  <details class="more">
    <summary>Advanced <span class="hint">source code, item limit</span></summary>
    <div class="body form-grid">
      <label class="field">
        Source code
        <input bind:value={sourceCode} placeholder="e.g. legifrance" />
      </label>
      <label class="field">
        Max items
        <input type="number" min="1" bind:value={maxItems} />
      </label>
    </div>
  </details>
</div>

<style>
  .subform { display: flex; flex-direction: column; gap: 0.9rem; }
  .subform > p.muted { margin: 0; }
</style>
