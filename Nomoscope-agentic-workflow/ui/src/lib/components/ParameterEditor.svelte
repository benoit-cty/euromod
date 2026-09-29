<script>
  // Metadata editor for one parameter (ADR 0005), shown in the Parameters
  // tab's expanded row. Only metadata is editable — unit, source_type and the
  // language-keyed texts. Identity (model_target, parameter_key) and values
  // are shown locked: a value changes only through a review decision.
  // Each changed field is one params.edit_parameter call, which validates,
  // audits under current_user and applies it; the edit then travels in the
  // EUROMOD change set ("Export changes…").
  import { api } from '../api.js';

  let { dbUrl = '', param, onsaved = null } = $props();

  // Mirrors paramdb.KNOWN_UNITS and schema.SourceType; the database refuses
  // anything else (a pytest keeps the SQL lists in step with the Python ones).
  const UNITS = ['/1', 'ratio', 'currency', 'currency/hour', 'currency/day', 'currency/week', 'currency/month', 'currency/year'];
  const SOURCE_TYPES = [
    'legislation',
    'national_team',
    'administrative_guidance',
    'official_statistics',
    'parliamentary_bill',
    'government_announcement',
    'other',
  ];
  const TEXT_FIELDS = ['short_label', 'label', 'description', 'explanation'];

  let editing = $state(false);
  let unit = $state('');
  let sourceType = $state('');
  let lang = $state('en');
  let texts = $state({});
  let note = $state('');
  let saving = $state(false);
  let error = $state('');
  let history = $state([]);
  let historyError = $state('');

  const languages = $derived.by(() => {
    const seen = new Set(['en']);
    for (const f of TEXT_FIELDS) for (const l of Object.keys(param.texts?.[f] ?? {})) seen.add(l);
    return [...seen].sort();
  });

  function original(field) {
    return param.texts?.[field]?.[lang] ?? '';
  }

  function start() {
    unit = param.unit ?? '';
    sourceType = param.current_source_type ?? '';
    texts = Object.fromEntries(TEXT_FIELDS.map((f) => [f, original(f)]));
    note = '';
    error = '';
    editing = true;
  }

  // Re-seed the text boxes when the language switches mid-edit.
  function switchLang(next) {
    lang = next;
    texts = Object.fromEntries(TEXT_FIELDS.map((f) => [f, original(f)]));
  }

  // The edits to send, as [field, value]: a text edit replaces one language
  // of the field's object and keeps the others; an emptied text drops it.
  const changes = $derived.by(() => {
    if (!editing) return [];
    const out = [];
    if (unit && unit !== (param.unit ?? '')) out.push(['unit', unit]);
    if (sourceType && sourceType !== (param.current_source_type ?? '')) out.push(['source_type', sourceType]);
    for (const f of TEXT_FIELDS) {
      const next = (texts[f] ?? '').trim();
      if (next === original(f).trim()) continue;
      const value = { ...(param.texts?.[f] ?? {}) };
      if (next) value[lang] = next;
      else delete value[lang];
      out.push([f, value]);
    }
    return out;
  });

  async function save() {
    if (!changes.length || saving) return;
    saving = true;
    error = '';
    try {
      // One call per field: each is its own audited edit, and a refused one
      // stops here with the earlier ones recorded (the error says which).
      for (const [field, value] of changes) {
        try {
          await api.editParameter(dbUrl, param.model_target, field, value, note);
        } catch (e) {
          throw new Error(`${field}: ${e.message ?? e}`);
        }
      }
      editing = false;
      await loadHistory();
      await onsaved?.();
    } catch (e) {
      error = String(e.message ?? e);
    } finally {
      saving = false;
    }
  }

  async function loadHistory() {
    try {
      history = await api.parameterEdits(dbUrl, param.model_target);
      historyError = '';
    } catch (e) {
      historyError = String(e);
    }
  }

  $effect(() => {
    if (dbUrl && param.model_target && param.edit_count) loadHistory();
  });

  function show(v) {
    if (v === null || v === undefined) return '—';
    if (typeof v === 'string') return v;
    return Object.entries(v).map(([l, t]) => `${l}: ${t}`).join(' · ');
  }
</script>

<div class="editor">
  <div class="locked muted small">
    <span title="identity — never editable">🔒 <span class="mono">{param.parameter_key ?? param.model_target}</span></span>
    <span title="values change only through a review decision">🔒 value in store</span>
  </div>

  {#if !editing}
    <button onclick={start}>Edit metadata…</button>
  {:else}
    <div class="grid">
      <label>
        Unit
        <select bind:value={unit}>
          {#if !param.unit}<option value="">— none in the export</option>{/if}
          {#each UNITS as u (u)}<option value={u}>{u}</option>{/each}
        </select>
      </label>
      <label>
        Source type
        <select bind:value={sourceType}>
          {#if !param.current_source_type}<option value="">— none</option>{/if}
          {#each SOURCE_TYPES as s (s)}<option value={s}>{s}</option>{/each}
        </select>
      </label>
      <label>
        Language
        <select value={lang} onchange={(e) => switchLang(e.currentTarget.value)}>
          {#each languages as l (l)}<option value={l}>{l}</option>{/each}
        </select>
      </label>
    </div>
    {#if sourceType === 'national_team' && param.current_source_type !== 'national_team'}
      <p class="warn small">national_team routes this parameter around the pipeline: agent runs will no longer propose a value.</p>
    {/if}
    {#each TEXT_FIELDS as f (f)}
      <label>
        {f.replace('_', ' ')}
        {#if f === 'description' || f === 'explanation'}
          <textarea rows="3" bind:value={texts[f]}></textarea>
        {:else}
          <input bind:value={texts[f]} />
        {/if}
      </label>
    {/each}
    <label>
      Note (why — kept with the edit and exported)
      <input bind:value={note} placeholder="e.g. a rate, not an amount: see CGI art. 197" />
    </label>
    <div class="actions">
      <button class="primary" onclick={save} disabled={saving || !changes.length}>
        {saving ? 'Saving…' : `Save ${changes.length} change(s)`}
      </button>
      <button onclick={() => (editing = false)} disabled={saving}>Cancel</button>
    </div>
    {#if error}<p class="error">{error}</p>{/if}
  {/if}

  {#if history.length}
    <table class="history small">
      <thead><tr><th>When</th><th>Who</th><th>Field</th><th>From</th><th>To</th><th>Note</th></tr></thead>
      <tbody>
        {#each history as h (h.id)}
          <tr>
            <td class="mono">{h.edited_at.slice(0, 16)}</td>
            <td class="mono">{h.reviewer}</td>
            <td>{h.field}</td>
            <td>{show(h.previous)}</td>
            <td>{show(h.value)}</td>
            <td>{h.note ?? ''}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
  {#if historyError}<p class="error small">{historyError}</p>{/if}
</div>

<style>
  .editor { display: flex; flex-direction: column; gap: 0.45rem; margin-top: 0.5rem; max-width: 60rem; }
  .locked { display: flex; gap: 1.2rem; flex-wrap: wrap; }
  .grid { display: flex; gap: 0.6rem; flex-wrap: wrap; }
  label { display: flex; flex-direction: column; gap: 0.2rem; color: var(--muted); }
  label input, label textarea, label select { width: 100%; }
  textarea { font: inherit; resize: vertical; }
  .actions { display: flex; gap: 0.5rem; }
  .error { color: var(--err); margin: 0; }
  .warn { color: var(--err); margin: 0; }
  .small { font-size: 0.8rem; }
  .history { border-collapse: collapse; margin-top: 0.3rem; }
  .history th, .history td { text-align: left; padding: 0.15rem 0.5rem; border-top: 1px solid var(--border); vertical-align: top; }
  button { align-self: flex-start; }
</style>
