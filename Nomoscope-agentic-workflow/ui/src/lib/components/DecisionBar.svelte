<script>
  // The decision on a proposal: a note, Accept (gated, lib/proposal.js
  // acceptGate), Reject, Send to the national team. Decided items stay
  // decidable: a new decision is added to the history.
  import Icon from '@shared/components/Icon.svelte';
  import { statusLabel, relativeTime } from '@shared/lib/labels.js';

  let {
    item,
    hasForm = false,
    gate,
    dirty = false,
    note = $bindable(''),
    // why the last decision could not be sent
    error = '',
    onsubmit,
    onedit,
  } = $props();
</script>

<footer class="actionbar">
  {#if item.status !== 'pending'}
    <p class="muted small decided">
      <span class="badge {item.status}">{statusLabel(item.status).label}</span>
      by {item.decision?.reviewer} · {relativeTime(item.decision?.decided_at)}
      {#if item.decision?.note}· “{item.decision.note}”{/if}
      · you can still change your decision; it will be added to the history.
    </p>
  {/if}
  {#if !hasForm}
    <p class="muted small">No value was proposed: reject it, or send it to the national team.</p>
  {/if}
  <div class="actions">
    <input class="note" placeholder="Add a note (optional)" bind:value={note} />
    <button
      class="primary"
      disabled={!gate.ok}
      title={gate.ok ? '' : `Blocked: ${gate.reason}`}
      onclick={() => onsubmit('accepted')}
    >
      <Icon name="check" size={16} />
      {dirty ? 'Accept with my corrections' : 'Accept'}
    </button>
    <button class="danger" onclick={() => onsubmit('rejected')}>Reject</button>
    <button onclick={() => onsubmit('escalated')} title="Escalate to the national team">Send to national team</button>
  </div>
  {#if error}<p class="callout err">{error}</p>{/if}
  {#if !gate.ok && item.routing !== 'not_found'}
    <p class="muted small">
      Accept is not possible: {gate.reason}.
      {#if hasForm && item.routing !== 'provisional'}
        <button class="link" onclick={onedit}>Correct the proposal</button>
      {/if}
    </p>
  {/if}
</footer>

<style>
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
</style>
