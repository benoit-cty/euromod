<script>
  // Hand-off to an external chat assistant: a ready-made research prompt the
  // reviewer pastes into Claude (or any assistant) when the pipeline did not
  // settle the value. The UI builds text only; it runs nothing (ADR 0004).
  // The parent remounts it per proposal, so a prompt never outlives its item.
  import { api } from '../api.js';
  import Icon from '@shared/components/Icon.svelte';
  import { buildHandoffPrompt } from '../handoff.js';

  let { item } = $props();

  let handoffText = $state('');
  let handoffOpen = $state(false);
  let handoffStatus = $state(''); // '' | 'copied' | 'manual'
  let handoffBusy = $state(false);
  const needsHandoff = $derived(item?.routing === 'not_found' || item?.routing === 'provisional');

  async function copyHandoff() {
    handoffBusy = true;
    let context = null;
    try {
      context = await api.parameterContext(item.model_target);
    } catch (e) {
      console.warn('parameter context unavailable; prompt built from the queue item alone', e);
    }
    handoffText = buildHandoffPrompt(item, context);
    handoffBusy = false;
    try {
      await navigator.clipboard.writeText(handoffText);
      handoffStatus = 'copied';
      setTimeout(() => (handoffStatus = ''), 3000);
    } catch {
      // no clipboard access: show the text so it can be copied by hand
      handoffStatus = 'manual';
      handoffOpen = true;
    }
  }
</script>

<div class="handoff">
  <button
    class:primary={needsHandoff}
    disabled={handoffBusy}
    title="Copy a research prompt with everything known about this parameter, to paste into Claude or another chat assistant"
    onclick={copyHandoff}
  >
    <Icon name="copy" size={16} />
    {handoffStatus === 'copied' ? 'Prompt copied' : 'Copy a prompt for an AI assistant'}
  </button>
  <span class="muted small">
    {#if handoffStatus === 'copied'}
      Paste it into Claude (or another assistant). If it finds the law, add the text under <em>Add sources</em> and check
      the parameter again.
    {:else if needsHandoff}
      Let a web-connected assistant search the law for this value.
    {/if}
  </span>
</div>
{#if handoffText}
  <details class="more" bind:open={handoffOpen}>
    <summary>
      The prompt
      <span class="hint">
        {handoffStatus === 'manual' ? 'the clipboard is not available — select it and copy' : 'what was copied'}
      </span>
    </summary>
    <div class="body">
      <textarea
        class="handoff-text mono"
        rows="14"
        readonly
        value={handoffText}
        onfocus={(e) => e.currentTarget.select()}></textarea>
    </div>
  </details>
{/if}

<style>
  .handoff {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-top: -0.3rem;
  }
  .handoff button {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
  }
  .handoff-text {
    width: 100%;
    font-size: 0.8rem;
    resize: vertical;
  }
</style>
