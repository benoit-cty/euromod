<script>
  import ValueView from './ValueView.svelte';
  import SourceViewer from './SourceViewer.svelte';

  let { item, ondecide } = $props();

  let note = $state('');
  let editing = $state(false);
  let editedJson = $state('');

  $effect(() => {
    // reset the decision form when another item is selected
    void item?.id;
    note = '';
    editing = false;
  });

  const extract = $derived(item?.proposed_value?.references?.[0]?.supporting_extract ?? null);
  const citedChunkId = $derived(item?.proposed_value?.references?.[0]?.jrc_database_id ?? null);
  const lineage = $derived(item?.proposed_value?.lineage ?? null);
  const decided = $derived(item && item.status !== 'pending');

  // Acceptance-gated tier (Param_Schema doc 08 §4): the Accept button enforces
  // legal_status + at least one reference with a supporting extract.
  const gate = $derived.by(() => {
    const pv = item?.proposed_value;
    if (!pv) return { ok: false, reason: 'no proposed value' };
    if (!pv.legal_status) return { ok: false, reason: 'missing legal_status' };
    const hasSource =
      pv.source_type === 'national_team' ||
      (pv.references ?? []).some((r) => r.supporting_extract);
    if (!hasSource) return { ok: false, reason: 'missing reference with supporting extract' };
    return { ok: true, reason: '' };
  });

  function startEdit() {
    editedJson = JSON.stringify(item.proposed_value.value, null, 2);
    editing = true;
  }

  function saveEdit() {
    let value;
    try {
      value = JSON.parse(editedJson);
    } catch {
      alert('Edited value is not valid JSON');
      return;
    }
    ondecide('edited', note, value);
    editing = false;
  }
</script>

<section class="panel detail">
  {#if !item}
    <p class="muted">Select a queue item to review it.</p>
  {:else}
    <header>
      <div>
        <h2>{item.label ?? item.model_target}</h2>
        <div class="muted mono">{item.model_target} · as of {item.as_of}</div>
      </div>
      <span class="badge {item.routing}">{item.routing}</span>
      <span class="badge {item.status}">{item.status}</span>
    </header>

    <div class="side-by-side">
      <ValueView title="Current value" value={item.current_value} unit={item.unit} />
      <ValueView
        title="Proposed value"
        value={item.proposed_value}
        other={item.current_value}
        unit={item.unit}
      />
    </div>

    {#if item.critique}
      <div class="critique">
        <h3>Critique <span class="badge {item.critique.verdict}">{item.critique.verdict}</span></h3>
        <ul class="checks">
          <li class:ok={item.critique.schema_valid}>schema valid</li>
          <li class:ok={item.critique.citation_verified}>citation verified (verbatim quote)</li>
          <li class:ok={item.critique.dates_consistent}>dates consistent</li>
          <li class:ok={item.critique.values_sane}>values sane</li>
        </ul>
        {#if item.critique.issues.length}
          <ul class="issues">
            {#each item.critique.issues as issue}<li>{issue}</li>{/each}
          </ul>
        {/if}
      </div>
    {/if}

    {#if item.proposed_value?.original_language_quote || extract}
      <div>
        <h3>Quote</h3>
        <blockquote>{extract}</blockquote>
      </div>
    {/if}

    <SourceViewer trace={item.retrieval_trace} {extract} {citedChunkId} />

    {#if lineage}
      <div>
        <h3>Provenance</h3>
        <p class="muted mono">
          run {lineage.run_id} · model {lineage.model} · prompt v{lineage.prompt_version} ·
          agent v{lineage.agent_version} · confidence {lineage.confidence ?? '—'}
        </p>
        {#if lineage.model_answer}<p class="muted">{lineage.model_answer}</p>{/if}
      </div>
    {/if}

    <footer>
      {#if decided}
        <p class="muted">
          Decided: <span class="badge {item.status}">{item.status}</span>
          by {item.decision?.reviewer} at {item.decision?.decided_at}
          {#if item.decision?.note}— “{item.decision.note}”{/if}
        </p>
      {:else if editing}
        <textarea rows="8" bind:value={editedJson}></textarea>
        <div class="actions">
          <button class="primary" onclick={saveEdit}>Save as edited & accept</button>
          <button onclick={() => (editing = false)}>Cancel</button>
        </div>
      {:else}
        <input placeholder="Review note (optional)" bind:value={note} />
        <div class="actions">
          <button
            class="primary"
            disabled={!gate.ok}
            title={gate.ok ? '' : `Blocked: ${gate.reason}`}
            onclick={() => ondecide('accepted', note)}
          >
            Accept
          </button>
          <button disabled={!item.proposed_value} onclick={startEdit}>Edit…</button>
          <button class="danger" onclick={() => ondecide('rejected', note)}>Reject</button>
          <button onclick={() => ondecide('escalated', note)}>Escalate to national team</button>
        </div>
        {#if !gate.ok}<p class="muted">Accept blocked: {gate.reason}</p>{/if}
      {/if}
    </footer>
  {/if}
</section>

<style>
  .detail { overflow: auto; display: flex; flex-direction: column; gap: 0.9rem; min-height: 0; }
  header { display: flex; align-items: baseline; gap: 0.6rem; flex-wrap: wrap; }
  header h2 { margin: 0; }
  .side-by-side { display: flex; gap: 1.2rem; flex-wrap: wrap; }
  .checks { list-style: none; padding: 0; margin: 0.3rem 0; display: flex; gap: 1rem; flex-wrap: wrap; }
  .checks li::before { content: '✗ '; color: var(--err); }
  .checks li.ok::before { content: '✓ '; color: var(--ok); }
  .issues { color: var(--err); margin: 0.3rem 0; }
  blockquote {
    margin: 0.3rem 0;
    padding: 0.5rem 0.8rem;
    border-left: 3px solid var(--accent);
    background: var(--panel-2);
    border-radius: 0 8px 8px 0;
  }
  footer { border-top: 1px solid var(--border); padding-top: 0.7rem; display: flex; flex-direction: column; gap: 0.5rem; }
  footer input, footer textarea { width: 100%; }
  .actions { display: flex; gap: 0.5rem; flex-wrap: wrap; }
</style>
