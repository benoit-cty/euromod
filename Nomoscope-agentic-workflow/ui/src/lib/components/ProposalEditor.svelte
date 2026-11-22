<script>
  // "Correct the proposal": the reviewer's edits to the value, its dates, its
  // legal and source status and its references. The proposal stays editable
  // after a decision, so the reviewer sees exactly what they sign off on. The
  // form lives in DetailPanel (lib/proposal.js holds its rules and the Accept
  // gate); each field offers "↩ was …" to restore the value EUROMOD holds.
  import DateField from './DateField.svelte';
  import { humanize, trustLabel } from '@shared/lib/labels.js';
  import { LEGAL_STATUSES, SOURCE_TYPES } from '../vocabulary.js';
  import { newReference } from '../proposal.js';

  let {
    form = $bindable(),
    // the value envelope EUROMOD holds now (item.current_value)
    current = null,
    unit = '',
    dirty = false,
    open = $bindable(false),
    onundo,
  } = $props();

  // one-line, for the "was" hint
  const currentValueText = $derived.by(() => {
    const value = current?.value;
    if (value == null) return null;
    return Array.isArray(value) ? JSON.stringify(value) : String(value);
  });
  // the same value formatted the way the editor holds it
  const currentValueEdit = $derived.by(() => {
    const value = current?.value;
    if (value == null) return '';
    return Array.isArray(value) ? JSON.stringify(value, null, 2) : String(value);
  });

  // "↩ was …" restores the EUROMOD value of one field into the form.
  function restore(field) {
    if (field === 'value') {
      form.brackets = Array.isArray(current?.value);
      form.valueText = currentValueEdit;
      return;
    }
    form[field] = current?.[field] ?? '';
  }

  function isRestored(field) {
    if (!form) return true;
    if (field === 'value') return form.valueText === currentValueEdit;
    return form[field] === (current?.[field] ?? '');
  }
</script>

<!-- the current EUROMOD value of a field; click to put it back into the form -->
{#snippet wasButton(field, shown)}
  <button
    type="button"
    class="was"
    disabled={isRestored(field)}
    title={isRestored(field) ? 'Same as the current EUROMOD value' : `Restore the current EUROMOD value (${shown})`}
    onclick={() => restore(field)}
  >
    ↩ was {shown}
  </button>
{/snippet}

<details class="more" bind:open>
  <summary>
    Correct the proposal
    {#if dirty}<span class="badge edited">edited</span>{/if}
    <span class="hint">value, dates, legal status, references</span>
  </summary>
  <div class="body edit">
    <label class="field">
      <span class="cap">
        <span>Value <span class="muted">{unit ?? ''} {form.brackets ? '(bracket JSON)' : ''}</span></span>
        {@render wasButton('value', currentValueText ?? '—')}
      </span>
      {#if form.brackets}
        <textarea rows="8" bind:value={form.valueText}></textarea>
      {:else}
        <input bind:value={form.valueText} placeholder="number, formula ($PSS * 4) or text" />
      {/if}
    </label>

    <div class="grid">
      <label class="field">
        <span class="cap">
          Valid from
          {@render wasButton('valid_from', current?.valid_from ?? '—')}
        </span>
        <DateField bind:value={form.valid_from} />
      </label>
      <label class="field">
        <span class="cap">
          Valid to <span class="muted">(empty = open)</span>
          {@render wasButton('valid_to', current?.valid_to ?? 'open')}
        </span>
        <DateField bind:value={form.valid_to} />
      </label>
      <label class="field">
        <span class="cap">
          Legal status
          {@render wasButton('legal_status', current?.legal_status ?? '—')}
        </span>
        <select bind:value={form.legal_status}>
          <option value="">—</option>
          {#each LEGAL_STATUSES as status}<option value={status}>{humanize(status)}</option>{/each}
        </select>
      </label>
      <label class="field">
        <span class="cap">
          Source type
          {@render wasButton('source_type', current?.source_type ?? '—')}
        </span>
        <select bind:value={form.source_type}>
          <option value="">—</option>
          {#each SOURCE_TYPES as source}<option value={source}>{humanize(source)}</option>{/each}
        </select>
      </label>
      <label class="field">
        <span class="cap">
          Official journal date
          {@render wasButton('official_journal_date', current?.official_journal_date ?? '—')}
        </span>
        <DateField bind:value={form.official_journal_date} />
      </label>
    </div>

    <div class="refs">
      <h4>
        References
        <button class="link" onclick={() => form.references.push(newReference())}>+ add</button>
      </h4>
      {#if !form.references.length}
        <p class="muted">None. Add one, or set the source type to “National team”.</p>
      {/if}
      {#each form.references as ref, i}
        <div class="ref">
          <div class="grid">
            <label class="field">
              Citation title
              <input bind:value={ref.title} placeholder="JORFTEXT000…, art. 1" />
            </label>
            <label class="field">
              Link
              <input bind:value={ref.href} placeholder="https://…" />
            </label>
            <label class="field">
              Legal unit ref
              <input bind:value={ref.legal_unit_ref} placeholder="CGI, art. 197" />
            </label>
            <label class="field">
              Text id <span class="muted">(read only)</span>
              <input class="mono" value={ref.jrc_database_id} readonly tabindex="-1" />
            </label>
            {#if ref.source_trust_class}
              {@const trust = trustLabel(ref.source_trust_class)}
              <div class="trust">
                Source class
                <span class="badge {trust.raw}" title="{trust.hint} ({trust.raw})">{trust.label}</span>
              </div>
            {/if}
          </div>
          <label class="field">
            Quote from the law <span class="muted">(word for word)</span>
            <textarea rows="4" bind:value={ref.supporting_extract}></textarea>
          </label>
          {#if ref.supporting_extract !== ref._extract_orig}
            <p class="warn-text">Quote edited by hand: the automatic word-for-word check no longer covers it.</p>
          {/if}
          <label class="field">
            Reviewer note
            <input bind:value={ref.reviewer_note} />
          </label>
          <button class="link danger" onclick={() => form.references.splice(i, 1)}> remove reference </button>
        </div>
      {/each}
    </div>
    <div><button disabled={!dirty} onclick={onundo}>Undo my corrections</button></div>
  </div>
</details>

<style>
  .edit h4 {
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .refs h4 {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr));
    gap: 0.6rem 0.8rem;
  }
  .field input[readonly] {
    color: var(--muted);
    background: var(--panel-2);
    cursor: default;
  }
  .cap {
    display: flex;
    align-items: baseline;
    gap: 0.4rem;
    justify-content: space-between;
  }
  button.was {
    color: var(--accent);
    background: none;
    border: none;
    padding: 0;
    font-size: 0.75rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 60%;
    display: inline;
  }
  button.was:disabled {
    color: var(--muted);
    cursor: default;
    opacity: 1;
  }
  .refs {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .trust {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    color: var(--muted);
  }
  .ref {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 0.7rem;
    border-radius: 8px;
    background: var(--panel-2);
  }
  .warn-text {
    color: var(--warn);
    margin: 0;
    font-size: 0.85rem;
  }
  button.link.danger {
    color: var(--err);
    align-self: flex-start;
  }
</style>
