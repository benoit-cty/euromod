<script>
  import { api } from '../api.js';
  import ValueView from './ValueView.svelte';
  import SourceViewer from './SourceViewer.svelte';
  import DateField from './DateField.svelte';

  let {
    item,
    ondecide,
    dbUrl = '',
    phoenixEndpoint = 'http://localhost:6006',
    phoenixGid = '',
  } = $props();

  // Param_Schema doc 01 §"legal_status enum" / schema.py LegalStatus & SourceType.
  const LEGAL_STATUSES = [
    'enacted_in_force',
    'enacted_not_yet_in_force',
    'adopted_pending_publication',
    'bill_proposed',
    'announced',
    'national_team_estimate',
  ];
  const SOURCE_TYPES = [
    'legislation',
    'national_team',
    'administrative_guidance',
    'official_statistics',
    'parliamentary_bill',
    'government_announcement',
    'other',
  ];

  const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;

  let note = $state('');
  // The proposal is always editable — including after a decision — so the
  // reviewer sees exactly which fields they are signing off on.
  let form = $state(null);
  let baseline = $state('');

  function buildForm(pv) {
    if (!pv) return null;
    const brackets = Array.isArray(pv.value);
    return {
      brackets,
      valueText: brackets
        ? JSON.stringify(pv.value, null, 2)
        : pv.value == null
          ? ''
          : String(pv.value),
      valid_from: pv.valid_from ?? '',
      valid_to: pv.valid_to ?? '',
      legal_status: pv.legal_status ?? '',
      source_type: pv.source_type ?? '',
      official_journal_date: pv.official_journal_date ?? '',
      references: (pv.references ?? []).map((r) => ({
        title: r.title ?? '',
        href: r.href ?? '',
        jrc_database_id: r.jrc_database_id ?? '',
        legal_unit_ref: r.legal_unit_ref ?? '',
        supporting_extract: r.supporting_extract ?? '',
        // kept so an untouched extract keeps its verified offsets
        _extract_orig: r.supporting_extract ?? '',
        extract_offsets: r.extract_offsets ?? null,
        reviewer_note: r.reviewer_note ?? '',
      })),
    };
  }

  function resetForm() {
    // snapshot the plain object *before* it becomes state: reading `form` back
    // here would make the seeding effect depend on the form it writes, and every
    // keystroke would re-seed it (and blow the effect-depth guard).
    const next = buildForm(item?.proposed_value);
    baseline = JSON.stringify(next);
    form = next;
  }

  $effect(() => {
    // re-seed whenever another item is selected or the current one is re-saved
    void item;
    resetForm();
    note = '';
  });

  const extract = $derived(item?.proposed_value?.references?.[0]?.supporting_extract ?? null);
  const citedChunkId = $derived(item?.proposed_value?.references?.[0]?.jrc_database_id ?? null);
  const lineage = $derived(item?.proposed_value?.lineage ?? null);
  const decided = $derived(item && item.status !== 'pending');
  const dirty = $derived(form != null && JSON.stringify(form) !== baseline);

  // "was …" hints: the value currently in EUROMOD, field by field.
  const current = $derived(item?.current_value ?? null);
  const currentValueText = $derived.by(() => {
    const value = current?.value;
    if (value == null) return null;
    return Array.isArray(value) ? JSON.stringify(value) : String(value); // one-line, for the hint
  });
  // same value formatted the way the editor holds it
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

  // Phoenix deep-link for this run's trace (same shape as the Parameters tab);
  // without a resolved project gid we can only open the projects page.
  const traceUrl = $derived(
    item?.phoenix_trace_id
      ? phoenixGid
        ? `${phoenixEndpoint}/projects/${phoenixGid}/traces/${item.phoenix_trace_id}`
        : `${phoenixEndpoint}/projects`
      : null,
  );

  // Acceptance-gated tier (Param_Schema doc 08 §4): Accept enforces valid_from,
  // legal_status and at least one reference with a supporting extract — checked
  // against the *edited* form, so filling a gap in the form unblocks Accept.
  const gate = $derived.by(() => {
    if (!form) return { ok: false, reason: 'no proposed value to accept' };
    if (!form.valid_from) return { ok: false, reason: 'missing valid from' };
    // dates are hand-editable text, so they are checked before they can be saved
    for (const field of ['valid_from', 'valid_to', 'official_journal_date']) {
      const value = form[field];
      if (value && !ISO_DATE.test(value)) {
        return { ok: false, reason: `${field} must be YYYY-MM-DD` };
      }
    }
    if (!form.legal_status) return { ok: false, reason: 'missing legal_status' };
    const hasSource =
      form.source_type === 'national_team' ||
      form.references.some((r) => r.supporting_extract.trim());
    if (!hasSource) return { ok: false, reason: 'missing reference with supporting extract' };
    return { ok: true, reason: '' };
  });

  function parsedValue() {
    const text = form.valueText.trim();
    if (form.brackets) return JSON.parse(text); // caller catches
    if (text === '') return null;
    try {
      const parsed = JSON.parse(text);
      // formulas ($PSS * 4) and other free text stay strings
      return typeof parsed === 'object' ? text : parsed;
    } catch {
      return text;
    }
  }

  function editedFields(value) {
    return {
      // also carried here so an intentional null ("n/a" row) survives the wire,
      // where a null edited_value would read as "unchanged"
      value,
      valid_from: form.valid_from || null,
      valid_to: form.valid_to || null,
      legal_status: form.legal_status || null,
      source_type: form.source_type || null,
      official_journal_date: form.official_journal_date || null,
      references: form.references.map((r) => ({
        title: r.title || null,
        href: r.href || null,
        jrc_database_id: r.jrc_database_id || null,
        legal_unit_ref: r.legal_unit_ref || null,
        supporting_extract: r.supporting_extract || null,
        // a hand-edited extract no longer matches the verified offsets
        extract_offsets: r.supporting_extract === r._extract_orig ? r.extract_offsets : null,
        reviewer_note: r.reviewer_note || null,
      })),
    };
  }

  function addReference() {
    form.references.push({
      title: '',
      href: '',
      jrc_database_id: '',
      legal_unit_ref: '',
      supporting_extract: '',
      _extract_orig: '',
      extract_offsets: null,
      reviewer_note: '',
    });
  }

  function submit(action) {
    if (!form) {
      ondecide(action, note);
      return;
    }
    if (!dirty) {
      ondecide(action, note);
      return;
    }
    let value;
    try {
      value = parsedValue();
    } catch {
      alert('Bracket value is not valid JSON');
      return;
    }
    // an edited proposal that the reviewer signs off on is logged as "edited"
    ondecide(action === 'accepted' ? 'edited' : action, note, value, editedFields(value));
  }
</script>

<!-- the current EUROMOD value of a field; click to put it back into the form -->
{#snippet wasButton(field, shown)}
  <button
    type="button"
    class="was"
    disabled={isRestored(field)}
    title={isRestored(field)
      ? 'Same as the current EUROMOD value'
      : `Restore the current EUROMOD value (${shown})`}
    onclick={() => restore(field)}
  >
    ↩ was {shown}
  </button>
{/snippet}

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

    <SourceViewer trace={item.retrieval_trace} {extract} {citedChunkId} {dbUrl} />

    {#if lineage || traceUrl}
      <div>
        <h3>Provenance</h3>
        {#if lineage}
          <p class="muted mono">
            run {lineage.run_id} · model {lineage.model} · prompt v{lineage.prompt_version} ·
            agent v{lineage.agent_version} · confidence {lineage.confidence ?? '—'}
          </p>
        {/if}
        {#if traceUrl}
          <p class="muted mono">
            trace {item.phoenix_trace_id}
            <button
              class="link"
              title={phoenixGid
                ? 'Open this run’s trace in Phoenix'
                : 'Phoenix project not resolved — opens the projects list'}
              onclick={() => api.openExternal(traceUrl)}
            >
              open in Phoenix ↗
            </button>
          </p>
        {/if}
        {#if lineage?.model_answer}<p class="muted">{lineage.model_answer}</p>{/if}
      </div>
    {/if}

    <footer>
      {#if decided}
        <p class="muted">
          Decided: <span class="badge {item.status}">{item.status}</span>
          by {item.decision?.reviewer} at {item.decision?.decided_at}
          {#if item.decision?.note}— “{item.decision.note}”{/if}
          · still editable, a new decision is appended to the audit log
        </p>
      {/if}

      {#if form}
        <div class="edit">
          <h3>
            Proposal under review
            {#if dirty}<span class="badge edited">edited</span>{/if}
          </h3>

          <div class="grid">
            <label>
              <span class="cap">
                Valid from
                {@render wasButton('valid_from', current?.valid_from ?? '—')}
              </span>
              <DateField bind:value={form.valid_from} />
            </label>
            <label>
              <span class="cap">
                Valid to <span class="muted">(empty = open)</span>
                {@render wasButton('valid_to', current?.valid_to ?? 'open')}
              </span>
              <DateField bind:value={form.valid_to} />
            </label>
            <label>
              <span class="cap">
                Legal status
                {@render wasButton('legal_status', current?.legal_status ?? '—')}
              </span>
              <select bind:value={form.legal_status}>
                <option value="">—</option>
                {#each LEGAL_STATUSES as status}<option value={status}>{status}</option>{/each}
              </select>
            </label>
            <label>
              <span class="cap">
                Source type
                {@render wasButton('source_type', current?.source_type ?? '—')}
              </span>
              <select bind:value={form.source_type}>
                <option value="">—</option>
                {#each SOURCE_TYPES as source}<option value={source}>{source}</option>{/each}
              </select>
            </label>
            <label>
              <span class="cap">
                Official journal date
                {@render wasButton('official_journal_date', current?.official_journal_date ?? '—')}
              </span>
              <DateField bind:value={form.official_journal_date} />
            </label>
          </div>

          <label class="block">
            <span class="cap">
              <span>Value <span class="muted">{item.unit ?? ''} {form.brackets ? '(bracket JSON)' : ''}</span></span>
              {@render wasButton('value', currentValueText ?? '—')}
            </span>
            {#if form.brackets}
              <textarea rows="8" bind:value={form.valueText}></textarea>
            {:else}
              <input bind:value={form.valueText} placeholder="number, formula ($PSS * 4) or text" />
            {/if}
          </label>

          <div class="refs">
            <h4>
              References
              <button class="link" onclick={addReference}>+ add</button>
            </h4>
            {#if !form.references.length}
              <p class="muted">none — add one, or set source type to national_team</p>
            {/if}
            {#each form.references as ref, i}
              <div class="ref">
                <div class="grid">
                  <label>
                    Citation title
                    <input bind:value={ref.title} placeholder="JORFTEXT000…, art. 1" />
                  </label>
                  <label>
                    Link
                    <input bind:value={ref.href} placeholder="https://…" />
                  </label>
                  <label>
                    Legal unit ref
                    <input bind:value={ref.legal_unit_ref} placeholder="CGI, art. 197" />
                  </label>
                  <label>
                    Chunk id <span class="muted">(jrc_database_id — read only)</span>
                    <input class="mono" value={ref.jrc_database_id} readonly tabindex="-1" />
                  </label>
                </div>
                <label class="block">
                  Supporting extract <span class="muted">(verbatim quote)</span>
                  <textarea rows="4" bind:value={ref.supporting_extract}></textarea>
                </label>
                {#if ref.supporting_extract !== ref._extract_orig}
                  <p class="warn-text">
                    Extract edited by hand — the verbatim-citation check no longer covers it and the
                    offsets are dropped.
                  </p>
                {/if}
                <label class="block">
                  Reviewer note
                  <input bind:value={ref.reviewer_note} />
                </label>
                <button class="link danger" onclick={() => form.references.splice(i, 1)}>
                  remove reference
                </button>
              </div>
            {/each}
          </div>
        </div>
      {:else}
        <p class="muted">No proposed value on this item — reject or escalate it.</p>
      {/if}

      <input placeholder="Review note (optional)" bind:value={note} />
      <div class="actions">
        <button
          class="primary"
          disabled={!gate.ok}
          title={gate.ok ? '' : `Blocked: ${gate.reason}`}
          onclick={() => submit('accepted')}
        >
          {dirty ? 'Save edits & accept' : 'Accept'}
        </button>
        <button disabled={!dirty} onclick={resetForm}>Revert edits</button>
        <button class="danger" onclick={() => submit('rejected')}>Reject</button>
        <button onclick={() => submit('escalated')}>Escalate to national team</button>
      </div>
      {#if !gate.ok}<p class="muted">Accept blocked: {gate.reason}</p>{/if}
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
  footer input, footer textarea, footer select { width: 100%; }
  .actions { display: flex; gap: 0.5rem; flex-wrap: wrap; }
  .edit { display: flex; flex-direction: column; gap: 0.6rem; }
  .edit h3, .refs h4 { margin: 0; display: flex; align-items: center; gap: 0.5rem; }
  .refs h4 {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr)); gap: 0.5rem 0.7rem; }
  label { display: flex; flex-direction: column; gap: 0.2rem; color: var(--muted); font-size: 0.85rem; }
  label input, label textarea, label select { color: var(--text); font-size: 0.95rem; }
  label input[readonly] { color: var(--muted); background: var(--panel-2); cursor: default; }
  .cap { display: flex; align-items: baseline; gap: 0.4rem; justify-content: space-between; }
  button.was {
    color: var(--accent);
    background: none;
    border: none;
    padding: 0;
    font-size: 0.75rem;
    cursor: pointer;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 60%;
  }
  button.was:disabled { color: var(--muted); cursor: default; }
  .block { display: flex; flex-direction: column; }
  .refs { display: flex; flex-direction: column; gap: 0.5rem; }
  .ref {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    padding: 0.5rem;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--panel-2);
  }
  .warn-text { color: var(--warn); margin: 0; font-size: 0.85rem; }
  button.link {
    background: none;
    border: none;
    padding: 0;
    color: var(--accent);
    cursor: pointer;
    font-size: 0.85rem;
    align-self: flex-start;
  }
  button.link.danger { color: var(--err); }
</style>
