<script>
  // One question and its answer. While the worker runs the turn, its tool
  // calls stream in as steps; the answer's [n] markers select quote n in the
  // source panel, and links open in the system browser.
  import { api } from '../api.js';
  import { stepLabel } from '../chat.js';
  import { lastLine } from '../jobs.js';
  import { renderMarkdown } from '../markdown.js';

  let { turn, selected = false, selectedQuote = null, onSelectQuote, onSelect, onCancel } = $props();

  const running = $derived(turn.status === 'queued' || turn.status === 'running');
  const html = $derived(turn.result ? renderMarkdown(turn.result.answer) : '');
  const quotes = $derived(turn.result?.quotes ?? []);
  const unverified = $derived(quotes.filter((q) => !q.verified).length);
  let showSteps = $state(false);

  function onAnswerClick(event) {
    const cite = event.target.closest('button.cite');
    if (cite) {
      onSelectQuote?.(Number(cite.dataset.cite) - 1);
      return;
    }
    const link = event.target.closest('a.ext');
    if (link) {
      event.preventDefault();
      api.openExternal(link.dataset.href);
    }
  }
</script>

<section class="turn" class:selected>
  <div class="question">{turn.question}</div>

  <div class="answer" onclick={() => onSelect?.()} role="presentation">
    {#if turn.steps.length}
      <div class="steps">
        {#if running || showSteps}
          {#each turn.steps as step, i (i)}
            <div class="step small" class:done={step.done}>
              <span class="dot">{step.done ? '✓' : '…'}</span>
              <span>{stepLabel(step)}</span>
              {#if step.summary}<span class="muted">— {step.summary}</span>{/if}
            </div>
          {/each}
        {:else}
          <button class="link small muted" onclick={(e) => { e.stopPropagation(); showSteps = true; }}>
            {turn.steps.length} tool call(s)
          </button>
        {/if}
      </div>
    {/if}

    {#if running}
      <div class="status muted small">
        <span class="spinner"></span>
        {turn.status === 'queued' ? 'Waiting for the worker…' : 'Thinking…'}
        {#if turn.jobId}<span class="mono">job #{turn.jobId}</span>{/if}
        <button class="small" onclick={(e) => { e.stopPropagation(); onCancel?.(); }}>Stop</button>
      </div>
    {:else if turn.status === 'succeeded' && turn.result}
      <!-- svelte-ignore a11y_click_events_have_key_events -->
      <div class="md" onclick={onAnswerClick} role="presentation">{@html html}</div>
      {#if quotes.length}
        <div class="quotes small">
          {#each quotes as q, i (i)}
            <button
              class="qchip"
              class:bad={!q.verified}
              class:on={selected && selectedQuote === i}
              title={q.extract}
              onclick={(e) => { e.stopPropagation(); onSelectQuote?.(i); }}
            >
              [{i + 1}] {q.citation ?? q.chunk_id.slice(0, 8)}{q.verified ? '' : ' ✗'}
            </button>
          {/each}
        </div>
        {#if unverified}
          <p class="banner warn small">
            {unverified} quote(s) could not be found verbatim in the cited chunk — treat them as unsupported.
          </p>
        {/if}
      {/if}
      {#if turn.result.discoveries?.length}
        <p class="muted small">
          Found {turn.result.discoveries.length} official act(s) not in the corpus — see the Web tab to ingest.
        </p>
      {/if}
      <div class="foot muted small">
        <span>{turn.result.model}</span>
        <span>as of {turn.result.as_of}</span>
        {#if turn.result.usage?.requests}<span>{turn.result.usage.requests} model call(s)</span>{/if}
        {#if turn.jobId}<span class="mono">job #{turn.jobId}</span>{/if}
        {#if turn.result.phoenix_trace_id}<span class="mono" title="Phoenix trace id">trace {turn.result.phoenix_trace_id.slice(0, 12)}</span>{/if}
      </div>
    {:else}
      <p class="banner err small">
        {turn.status === 'cancelled' ? 'Stopped.' : `Failed: ${lastLine(turn.error)}`}
      </p>
    {/if}
  </div>
</section>

<style>
  .turn { margin-bottom: 1.2rem; }
  .question {
    margin-left: auto;
    max-width: 80%;
    width: fit-content;
    background: var(--header-bg);
    border: 1px solid var(--border-strong);
    padding: 0.5rem 0.8rem;
    border-radius: 10px 10px 2px 10px;
    white-space: pre-wrap;
  }
  .answer {
    margin-top: 0.5rem;
    max-width: 92%;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px 10px 10px 2px;
    box-shadow: var(--shadow);
    padding: 0.55rem 0.85rem;
  }
  .selected .answer { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
  .steps { margin-bottom: 0.35rem; }
  .step { display: flex; gap: 0.4rem; color: var(--muted); }
  .step.done .dot { color: var(--ok); }
  .status { display: flex; align-items: center; gap: 0.5rem; }
  .quotes { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.4rem; }
  .qchip { padding: 0.05rem 0.5rem; border-radius: 999px; font-size: 0.82em; }
  .qchip.on { background: var(--accent-soft); border-color: var(--accent); font-weight: 600; }
  .qchip.bad { color: var(--err); }
  .foot { display: flex; flex-wrap: wrap; gap: 0.8rem; margin-top: 0.4rem; }
</style>
