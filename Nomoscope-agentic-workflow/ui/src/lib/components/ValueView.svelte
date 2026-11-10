<script>
  // Renders one value envelope (scalar or bracket schedule); when `other` is
  // given, bracket cells that differ from it are highlighted.
  import { humanize } from '../labels.js';

  let { title, value, other = null, unit = '' } = $props();

  const isBrackets = $derived(Array.isArray(value?.value));

  function differs(index, key) {
    if (!other || !Array.isArray(other.value)) return false;
    const a = value.value[index]?.[key];
    const b = other.value[index]?.[key];
    return JSON.stringify(a) !== JSON.stringify(b);
  }

  // EUROMOD rates are fractions (`/1`, 0.2 = 20 %) or points (`/100`); say it
  // the way the law does, next to the stored figure.
  function unitHint(x) {
    if (typeof x !== 'number') return '';
    if (unit === '/1') return `= ${+(x * 100).toFixed(6)} %`;
    if (unit === '/100') return `= ${x} %`;
    return '';
  }

  function fmt(x) {
    if (x == null) return '—';
    return typeof x === 'number' ? x.toLocaleString('en-US') : String(x);
  }
</script>

<div class="value-view">
  <h3>{title}</h3>
  {#if !value}
    <p class="muted">none</p>
  {:else}
    {#if isBrackets}
      <table>
        <thead><tr><th>#</th><th>Threshold</th><th>Rate / amount</th></tr></thead>
        <tbody>
          {#each value.value as band, i}
            <tr>
              <td class="muted">{i + 1}</td>
              <td class:diff={differs(i, 'threshold')}>{fmt(band.threshold)}</td>
              <td class:diff={differs(i, 'rate') || differs(i, 'amount')}>
                {band.rate != null ? band.rate : fmt(band.amount)}
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    {:else}
      <div class="scalar" class:diff={other && JSON.stringify(other.value) !== JSON.stringify(value.value)}>
        {fmt(value.value)}
        {#if unitHint(value.value)}<span class="muted hint">{unitHint(value.value)}</span>
        {:else}<span class="muted">{unit}</span>{/if}
      </div>
    {/if}
    <dl>
      <dt>Valid</dt>
      <dd>{value.valid_from ?? '—'} → {value.valid_to ?? 'open-ended'}</dd>
      {#if value.legal_status}<dt>Status</dt><dd>{humanize(value.legal_status)}</dd>{/if}
      {#if value.source_type}<dt>Source</dt><dd>{humanize(value.source_type)}</dd>{/if}
      {#if value.official_journal_date}<dt>Published</dt><dd>{value.official_journal_date}</dd>{/if}
    </dl>
  {/if}
</div>

<style>
  .value-view { flex: 1; min-width: 14rem; }
  .scalar { font-size: 1.6rem; font-weight: 600; padding: 0.3rem 0; }
  .scalar .hint { font-size: 1rem; font-weight: 500; }
  .diff { background: var(--warn-soft); color: var(--warn); border-radius: 4px; }
  td.diff { font-weight: 600; }
  dl { font-size: 0.88rem; display: grid; grid-template-columns: auto 1fr; gap: 0.15rem 0.7rem; margin: 0.5rem 0 0; }
  dt { color: var(--muted); }
  dd { margin: 0; }
</style>
