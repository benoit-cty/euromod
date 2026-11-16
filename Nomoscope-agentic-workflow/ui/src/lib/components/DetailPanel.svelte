<script>
  // One proposal on the review page: what EUROMOD holds, what the law says,
  // the quote it rests on, the checks, and the decision. The parts are their
  // own components (RunSwitcher, HandoffPrompt, CritiqueSummary,
  // ProposalEditor, DecisionBar); the correction form and the Accept gate
  // are state here, their rules in lib/proposal.js.
  import { untrack } from 'svelte';
  import { api } from '../api.js';
  import ValueView from './ValueView.svelte';
  import SourceViewer from './SourceViewer.svelte';
  import RunSwitcher from './RunSwitcher.svelte';
  import HandoffPrompt from './HandoffPrompt.svelte';
  import CritiqueSummary from './CritiqueSummary.svelte';
  import ProposalEditor from './ProposalEditor.svelte';
  import DecisionBar from './DecisionBar.svelte';
  import Icon from '@shared/components/Icon.svelte';
  import { routingLabel, statusLabel, trustLabel, countryName } from '@shared/lib/labels.js';
  import { acceptGate, buildForm, editedFields, parsedValue } from '../proposal.js';

  let {
    item,
    // every queue run of the same parameter, newest first (this one included)
    siblings = [],
    onselectrun = () => {},
    ondecide,
    phoenixEndpoint = 'http://localhost:6006',
    phoenixGid = '',
  } = $props();

  let note = $state('');
  // Why a decision could not be sent (shown in the decision bar, not alert()).
  let formError = $state('');
  // The correction form is folded away until needed; a blocked Accept opens it.
  let editOpen = $state(false);
  // The proposal is always editable — including after a decision — so the
  // reviewer sees exactly which fields they are signing off on.
  let form = $state(null);
  let baseline = $state('');

  function resetForm() {
    // snapshot the plain object *before* it becomes state: reading `form` back
    // here would make the seeding effect depend on the form it writes, and every
    // keystroke would re-seed it (and blow the effect-depth guard).
    const next = buildForm(item?.proposed_value);
    baseline = JSON.stringify(next);
    form = next;
  }

  // What the form was seeded from: another item, another run of it, or a new
  // decision on it. Not the object identity — the ribbon's Refresh hands over
  // equal items as new objects, and re-seeding on that discarded the
  // reviewer's unsaved corrections and note (code audit D18).
  const seedKey = $derived(
    item ? `${item.id}|${item.run_id ?? ''}|${item.status}|${item.decision?.decided_at ?? ''}` : '',
  );

  $effect(() => {
    void seedKey;
    untrack(resetForm);
    note = '';
    formError = '';
  });

  const extract = $derived(item?.proposed_value?.references?.[0]?.supporting_extract ?? null);
  const citedChunkId = $derived(item?.proposed_value?.references?.[0]?.jrc_database_id ?? null);
  const lineage = $derived(item?.proposed_value?.lineage ?? null);
  const dirty = $derived(form != null && JSON.stringify(form) !== baseline);
  const gate = $derived(acceptGate(form, item?.routing));

  // Phoenix deep-link for this run's trace (same shape as the Parameters tab);
  // without a resolved project gid we can only open the projects page.
  const traceUrl = $derived(
    item?.phoenix_trace_id
      ? phoenixGid
        ? `${phoenixEndpoint}/projects/${phoenixGid}/traces/${item.phoenix_trace_id}`
        : `${phoenixEndpoint}/projects`
      : null,
  );

  function submit(action) {
    formError = '';
    if (!form || !dirty) {
      ondecide(action, note);
      return;
    }
    let value;
    try {
      value = parsedValue(form);
    } catch (e) {
      formError = `The bracket value is not valid JSON (${e.message ?? e}): correct it under “Correct the proposal”.`;
      editOpen = true;
      return;
    }
    // an edited proposal that the reviewer signs off on is logged as "edited"
    ondecide(action === 'accepted' ? 'edited' : action, note, value, editedFields(form, value));
  }
</script>

<section class="panel detail">
  {#if !item}
    <div class="empty-state fill">
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

      <RunSwitcher {item} {siblings} {onselectrun} />

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

      {#key seedKey}<HandoffPrompt {item} />{/key}

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

      <CritiqueSummary {item} />

      {#if extract}
        <div class="quote">
          <h3>What the law says</h3>
          <blockquote>{extract}</blockquote>
          {#if ref0}
            <div class="cite muted small">
              {ref0.title ?? ref0.legal_unit_ref ?? ''}
              {#if ref0.source_trust_class}
                {@const trust = trustLabel(ref0.source_trust_class)}
                <span class="badge {trust.raw}" title="{trust.hint} ({trust.raw})">{trust.label}</span>
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
          <SourceViewer trace={item.retrieval_trace} {extract} {citedChunkId} />
        </div>
      </details>

      {#if form}
        <ProposalEditor bind:form bind:open={editOpen} current={item.current_value} unit={item.unit} {dirty} onundo={resetForm} />
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

    <DecisionBar
      {item}
      hasForm={form != null}
      {gate}
      {dirty}
      bind:note
      error={formError}
      onsubmit={submit}
      onedit={() => (editOpen = true)}
    />
  {/if}
</section>

<style>
  .detail { display: flex; flex-direction: column; min-height: 0; padding: 0; overflow: hidden; }
  .fill { flex: 1; justify-content: center; }
  .scroll { overflow: auto; flex: 1; display: flex; flex-direction: column; gap: 0.9rem; padding: 1.1rem 1.2rem; }
  header { display: flex; align-items: flex-start; gap: 0.8rem; justify-content: space-between; }
  header h2 { margin: 0 0 0.1rem; font-size: 1.2rem; }
  .badges { display: flex; gap: 0.35rem; flex-wrap: wrap; justify-content: flex-end; }
  .summary { margin: 0; }
  .side-by-side { display: flex; gap: 0.6rem; align-items: stretch; flex-wrap: wrap; }
  .value-card { flex: 1; min-width: 14rem; border: 1px solid var(--border); border-radius: 10px; padding: 0.8rem 1rem; }
  .value-card.proposed { border-color: var(--accent); background: color-mix(in srgb, var(--accent-soft) 40%, transparent); }
  .arrow { display: flex; align-items: center; color: var(--muted); }
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
  .issues { color: var(--err); margin: -0.4rem 0 0; font-size: 0.9rem; }
  .checks { list-style: none; padding: 0; margin: 0.3rem 0; display: flex; gap: 1rem; flex-wrap: wrap; font-size: 0.85rem; }
  .checks li::before { content: '✗ '; color: var(--err); }
  .checks li.ok::before { content: '✓ '; color: var(--ok); }
</style>
