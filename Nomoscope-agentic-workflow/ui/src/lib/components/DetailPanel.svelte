<script>
  import { api } from '../api.js';
  import ValueView from './ValueView.svelte';
  import SourceViewer from './SourceViewer.svelte';
  import DateField from './DateField.svelte';
  import Icon from './Icon.svelte';
  import { routingLabel, statusLabel, countryName, humanize, relativeTime } from '../labels.js';

  let {
    item,
    // every queue run of the same parameter, newest first (this one included)
    siblings = [],
    onselectrun = () => {},
    ondecide,
    dbUrl = '',
    phoenixEndpoint = 'http://localhost:6006',
    phoenixGid = '',
  } = $props();

  const runIndex = $derived(siblings.findIndex((r) => r.id === item?.id));

  function runLabel(run) {
    return run.system_year ?? run.as_of?.slice(0, 4) ?? '—';
  }

  function stepRun(delta) {
    const next = siblings[runIndex + delta];
    if (next) onselectrun(next.id);
  }

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
  // The correction form is folded away until needed; a blocked Accept opens it.
  let editOpen = $state(false);
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
        // Read-only: the class of the instrument this citation came from
        // (ADR 0001). Carried through the form so a hand-edited reference does
        // not silently lose what the value rests on.
        source_trust_class: r.source_trust_class ?? null,
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
    if (!form) return { ok: false, reason: 'there is no proposed value to accept' };
    if (item?.routing === 'provisional') {
      return {
        ok: false,
        reason:
          'provisional: the evidence is likely the previous year\'s value — ' +
          'ingest the missing finance act and re-run instead of accepting',
      };
    }
    if (!form.valid_from) return { ok: false, reason: 'the “valid from” date is missing' };
    // dates are hand-editable text, so they are checked before they can be saved
    for (const field of ['valid_from', 'valid_to', 'official_journal_date']) {
      const value = form[field];
      if (value && !ISO_DATE.test(value)) {
        return { ok: false, reason: `${humanize(field)} must be a date (YYYY-MM-DD)` };
      }
    }
    if (!form.legal_status) return { ok: false, reason: 'the legal status is missing' };
    const hasSource =
      form.source_type === 'national_team' ||
      form.references.some((r) => r.supporting_extract.trim());
    if (!hasSource) return { ok: false, reason: 'no reference quotes the law' };
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
        source_trust_class: r.source_trust_class || null,
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
      source_trust_class: null,
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
    <div class="empty-state grow">
      <Icon name="review" size={32} />
      <span class="big">Pick a proposal on the left</span>
      <span>You will see the value EUROMOD holds, the value found in the law, and the quote it rests on.</span>
    </div>
  {:else}
    {@const outcome = routingLabel(item.routing)}
    {@const ref0 = item.proposed_value?.references?.[0]}
    <div class="scroll">
      <header>
        <div class="title">
          <h2>{item.label ?? item.model_target}</h2>
          <div class="muted">
            {countryName(item.country)} · year {item.system_year ?? item.as_of?.slice(0, 4)}
          </div>
        </div>
        <div class="badges">
          <span class="badge {item.routing}" title={outcome.hint}>{outcome.label}</span>
          {#if item.guidance_only}
            <!-- ADR 0001: "Legislation is King" stays visible in every decision
                 record. Informational only — Accept is not blocked, because for a
                 circular-governed scheme the circular IS the operative text. -->
            <span
              class="badge guidance"
              title="Every citation on this proposal comes from administrative guidance (a circular or doctrine), not from legislation."
            >Guidance only</span>
          {/if}
          {#if item.status !== 'pending'}
            <span class="badge {item.status}">{statusLabel(item.status).label}</span>
          {/if}
        </div>
      </header>

      {#if siblings.length > 1}
        <!-- The queue keeps one item per (parameter, year) run; the list shows
             only the newest, so the other runs are reachable from here. -->
        <div class="runs">
          <span class="muted">Other years</span>
          <button class="step ghost" disabled={runIndex <= 0} title="Newer" onclick={() => stepRun(-1)}>‹</button>
          <div class="run-chips">
            {#each siblings as run (run.id)}
              <button
                class="chip"
                class:current={run.id === item.id}
                title="{routingLabel(run.routing).label} · {statusLabel(run.status).label}"
                onclick={() => onselectrun(run.id)}
              >
                <span class="year">{runLabel(run)}</span>
                {#if run.status !== 'pending'}<span class="badge {run.status}">{statusLabel(run.status).label}</span>{/if}
              </button>
            {/each}
          </div>
          <button
            class="step ghost"
            disabled={runIndex < 0 || runIndex >= siblings.length - 1}
            title="Older"
            onclick={() => stepRun(1)}>›</button
          >
        </div>
      {/if}

      <p class="callout {item.routing === 'not_found' ? 'err' : item.routing === 'unchanged' ? 'ok' : item.routing === 'provisional' ? 'info' : 'warn'} summary">
        {#if item.routing === 'provisional'}
          The text found cannot be tied to {item.system_year ?? item.as_of?.slice(0, 4)}: the value shown is
          probably <strong>last year’s</strong>. Nothing to accept yet. This year’s act is likely missing
          from the library; add it under <em>Add sources</em>, then check the parameter again.
        {:else if item.routing === 'not_found'}
          The assistant could not find a text stating this value. Reject it, or send it to the national
          team. If you know the law that sets it, add it under <em>Add sources</em> and check again.
        {:else}
          {outcome.hint}
        {/if}
      </p>

      <div class="side-by-side">
        <div class="value-card">
          <ValueView title="In EUROMOD now" value={item.current_value} unit={item.unit} />
        </div>
        <div class="arrow"><Icon name="arrow" size={22} /></div>
        <div class="value-card proposed">
          <ValueView
            title="Found in the law"
            value={item.proposed_value}
            other={item.current_value}
            unit={item.unit}
          />
        </div>
      </div>

      {#if item.critique && item.routing !== 'not_found'}
        {@const failed = [
          !item.critique.schema_valid && 'the proposal is not well-formed',
          !item.critique.citation_verified && 'the quote is not found word-for-word in the cited text',
          !item.critique.dates_consistent && 'the dates do not fit the year',
          !item.critique.values_sane && 'the value looks implausible',
        ].filter(Boolean)}
        <div class="checks-line" class:bad={item.critique.verdict !== 'pass'}>
          {#if item.critique.verdict === 'pass' && !failed.length}
            <Icon name="check" size={16} /> All automatic checks passed
          {:else}
            <Icon name="alert" size={16} />
            Automatic checks: {failed.length ? failed.join('; ') : 'see the issues below'}
          {/if}
        </div>
        {#if item.critique.issues.length}
          <!-- "note: …" lines are the critique explaining a rule it applied, not a problem -->
          <ul class="issues">
            {#each item.critique.issues as issue}
              {@const isNote = /^note:/i.test(issue)}
              <li class:note={isNote}>{isNote ? `Note: ${issue.replace(/^note:\s*/i, '')}` : issue}</li>
            {/each}
          </ul>
        {/if}
      {/if}

      {#if extract}
        <div class="quote">
          <h3>What the law says</h3>
          <blockquote>{extract}</blockquote>
          {#if ref0}
            <div class="cite muted small">
              {ref0.title ?? ref0.legal_unit_ref ?? ''}
              {#if ref0.source_trust_class}
                <span class="badge {ref0.source_trust_class}">{humanize(ref0.source_trust_class === 'evidence' ? 'legislation' : ref0.source_trust_class)}</span>
              {/if}
              {#if ref0.href}
                <button class="link" onclick={() => api.openExternal(ref0.href)}>open the official text ↗</button>
              {/if}
            </div>
          {/if}
        </div>
      {/if}

      <details class="more">
        <summary>
          Texts the assistant read
          <span class="hint">{item.retrieval_trace?.length ?? 0} passages, with the quote highlighted</span>
        </summary>
        <div class="body">
          <SourceViewer trace={item.retrieval_trace} {extract} {citedChunkId} {dbUrl} />
        </div>
      </details>

      {#if form}
        <details class="more" bind:open={editOpen}>
          <summary>
            Correct the proposal
            {#if dirty}<span class="badge edited">edited</span>{/if}
            <span class="hint">value, dates, legal status, references</span>
          </summary>
          <div class="body edit">
            <label class="field">
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
                <button class="link" onclick={addReference}>+ add</button>
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
                      <div class="trust">
                        Source class
                        <span class="badge {ref.source_trust_class}">{ref.source_trust_class}</span>
                      </div>
                    {/if}
                  </div>
                  <label class="field">
                    Quote from the law <span class="muted">(word for word)</span>
                    <textarea rows="4" bind:value={ref.supporting_extract}></textarea>
                  </label>
                  {#if ref.supporting_extract !== ref._extract_orig}
                    <p class="warn-text">
                      Quote edited by hand: the automatic word-for-word check no longer covers it.
                    </p>
                  {/if}
                  <label class="field">
                    Reviewer note
                    <input bind:value={ref.reviewer_note} />
                  </label>
                  <button class="link danger" onclick={() => form.references.splice(i, 1)}>
                    remove reference
                  </button>
                </div>
              {/each}
            </div>
            <div><button disabled={!dirty} onclick={resetForm}>Undo my corrections</button></div>
          </div>
        </details>
      {/if}

      {#if lineage || traceUrl}
        <details class="more">
          <summary>Technical details <span class="hint">model, run, trace</span></summary>
          <div class="body">
            {#if lineage}
              <p class="muted mono">
                run {lineage.run_id} · model {lineage.model} · prompt v{lineage.prompt_version} ·
                agent v{lineage.agent_version} · confidence {lineage.confidence ?? '—'}
              </p>
            {/if}
            <p class="muted mono">{item.model_target} · as of {item.as_of}</p>
            {#if item.critique}
              {#if item.routing === 'not_found' && item.critique.issues.length}
                <ul class="issues">
                  {#each item.critique.issues as issue}<li>{issue}</li>{/each}
                </ul>
              {/if}
              <ul class="checks">
                <li class:ok={item.critique.schema_valid}>schema valid</li>
                <li class:ok={item.critique.citation_verified}>citation verified (verbatim quote)</li>
                <li class:ok={item.critique.dates_consistent}>dates consistent</li>
                <li class:ok={item.critique.values_sane}>values sane</li>
              </ul>
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
        </details>
      {/if}
    </div>

    <footer class="actionbar">
      {#if decided}
        <p class="muted small decided">
          <span class="badge {item.status}">{statusLabel(item.status).label}</span>
          by {item.decision?.reviewer} · {relativeTime(item.decision?.decided_at)}
          {#if item.decision?.note}· “{item.decision.note}”{/if}
          · you can still change your decision; it will be added to the history.
        </p>
      {/if}
      {#if !form}
        <p class="muted small">No value was proposed: reject it, or send it to the national team.</p>
      {/if}
      <div class="actions">
        <input class="note" placeholder="Add a note (optional)" bind:value={note} />
        <button
          class="primary"
          disabled={!gate.ok}
          title={gate.ok ? '' : `Blocked: ${gate.reason}`}
          onclick={() => submit('accepted')}
        >
          <Icon name="check" size={16} />
          {dirty ? 'Accept with my corrections' : 'Accept'}
        </button>
        <button class="danger" onclick={() => submit('rejected')}>Reject</button>
        <button onclick={() => submit('escalated')} title="Escalate to the national team">Send to national team</button>
      </div>
      {#if !gate.ok && item.routing !== 'not_found'}
        <p class="muted small">
          Accept is not possible: {gate.reason}.
          {#if form && item.routing !== 'provisional'}
            <button class="link" onclick={() => (editOpen = true)}>Correct the proposal</button>
          {/if}
        </p>
      {/if}
    </footer>
  {/if}
</section>

<style>
  .detail { display: flex; flex-direction: column; min-height: 0; padding: 0; overflow: hidden; }
  .grow { flex: 1; justify-content: center; }
  .scroll { overflow: auto; flex: 1; display: flex; flex-direction: column; gap: 0.9rem; padding: 1.1rem 1.2rem; }
  header { display: flex; align-items: flex-start; gap: 0.8rem; justify-content: space-between; }
  header h2 { margin: 0 0 0.1rem; font-size: 1.2rem; }
  .badges { display: flex; gap: 0.35rem; flex-wrap: wrap; justify-content: flex-end; }
  .summary { margin: 0; }
  .side-by-side { display: flex; gap: 0.6rem; align-items: stretch; flex-wrap: wrap; }
  .value-card { flex: 1; min-width: 14rem; border: 1px solid var(--border); border-radius: 10px; padding: 0.8rem 1rem; }
  .value-card.proposed { border-color: var(--accent); background: color-mix(in srgb, var(--accent-soft) 40%, transparent); }
  .arrow { display: flex; align-items: center; color: var(--muted); }
  .checks-line { display: flex; align-items: center; gap: 0.45rem; color: var(--ok); font-weight: 600; font-size: 0.92rem; }
  .checks-line.bad { color: var(--warn); }
  .issues { color: var(--err); margin: -0.4rem 0 0; font-size: 0.9rem; }
  .issues li.note { color: var(--muted); }
  .quote h3 { margin-bottom: 0.3rem; }
  blockquote {
    margin: 0;
    padding: 0.7rem 0.9rem;
    border-left: 3px solid var(--accent);
    background: var(--panel-2);
    border-radius: 0 8px 8px 0;
    font-size: 1rem;
    line-height: 1.55;
  }
  .cite { margin-top: 0.35rem; display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; }
  .runs { display: flex; align-items: center; gap: 0.4rem; font-size: 0.85rem; min-width: 0; }
  .run-chips { display: flex; gap: 0.3rem; overflow-x: auto; padding-bottom: 0.15rem; }
  .runs .chip {
    gap: 0.35rem;
    padding: 0.15rem 0.55rem;
    border-radius: 999px;
    background: var(--panel-2);
    border-color: transparent;
    color: var(--muted);
    white-space: nowrap;
  }
  .runs .chip.current { border-color: var(--accent); color: var(--text); background: var(--accent-soft); }
  .runs .chip .year { font-variant-numeric: tabular-nums; }
  .runs .step { padding: 0.05rem 0.45rem; }
  .checks { list-style: none; padding: 0; margin: 0.3rem 0; display: flex; gap: 1rem; flex-wrap: wrap; font-size: 0.85rem; }
  .checks li::before { content: '✗ '; color: var(--err); }
  .checks li.ok::before { content: '✓ '; color: var(--ok); }

  .actionbar {
    border-top: 1px solid var(--border);
    padding: 0.8rem 1.2rem;
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
    background: var(--panel);
  }
  .actions { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; }
  .note { flex: 1; min-width: 12rem; }
  .decided { margin: 0; }

  .edit h4 { margin: 0; display: flex; align-items: center; gap: 0.5rem; }
  .refs h4 {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr)); gap: 0.6rem 0.8rem; }
  .field input[readonly] { color: var(--muted); background: var(--panel-2); cursor: default; }
  .cap { display: flex; align-items: baseline; gap: 0.4rem; justify-content: space-between; }
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
  button.was:disabled { color: var(--muted); cursor: default; opacity: 1; }
  .refs { display: flex; flex-direction: column; gap: 0.5rem; }
  .trust { display: flex; align-items: center; gap: 0.4rem; color: var(--muted); }
  .ref {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 0.7rem;
    border-radius: 8px;
    background: var(--panel-2);
  }
  .warn-text { color: var(--warn); margin: 0; font-size: 0.85rem; }
  button.link.danger { color: var(--err); align-self: flex-start; }
</style>
