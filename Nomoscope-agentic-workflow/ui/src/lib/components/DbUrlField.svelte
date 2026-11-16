<script>
  // The database the whole app reads, for the people maintaining it. The URL
  // is shown with its password masked; Connect hands what was typed to the
  // backend, which checks it answers before the app switches (`set_db_url`).
  // A masked password left as shown keeps the current one.
  let { dbUrl = '', onchangedb } = $props();

  // A draft over the prop: typing overrides it, a new prop value resets it.
  let draft = $derived(dbUrl);
  let busy = $state(false);
  let error = $state('');

  async function connect() {
    busy = true;
    error = '';
    try {
      await onchangedb(draft.trim());
    } catch (e) {
      error = String(e);
    } finally {
      busy = false;
    }
  }
</script>

<div class="row bottom">
  <label class="field grow">
    Database URL
    <input class="mono" value={draft} oninput={(e) => (draft = e.currentTarget.value)} />
  </label>
  <button onclick={connect} disabled={busy || !draft.trim() || draft.trim() === dbUrl}>
    {busy ? 'Connecting…' : 'Connect'}
  </button>
</div>
{#if error}<p class="callout err">{error}</p>{/if}
