<script>
  // Renders one value envelope (scalar or bracket schedule); when `other` is
  // given, bracket cells that differ from it are highlighted.
  let { title, value, other = null, unit = '' } = $props();

  const isBrackets = $derived(Array.isArray(value?.value));

  function differs(index, key) {
    if (!other || !Array.isArray(other.value)) return false;
    const a = value.value[index]?.[key];
    const b = other.value[index]?.[key];
    return JSON.stringify(a) !== JSON.stringify(b);
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
        {fmt(value.value)} <span class="muted">{unit}</span>
      </div>
    {/if}
    <dl>
      <dt>valid</dt>
      <dd>{value.valid_from} → {value.valid_to ?? 'open'}</dd>
      {#if value.legal_status}<dt>legal status</dt><dd>{value.legal_status}</dd>{/if}
      {#if value.source_type}<dt>source</dt><dd>{value.source_type}</dd>{/if}
      {#if value.official_journal_date}<dt>OJ date</dt><dd>{value.official_journal_date}</dd>{/if}
    </dl>
  {/if}
</div>

<style>
  .value-view { flex: 1; min-width: 14rem; }
  .scalar { font-size: 1.6rem; font-weight: 600; padding: 0.3rem 0; }
  .diff { background: var(--warn-soft); color: var(--warn); border-radius: 4px; }
  td.diff { font-weight: 600; }
  dl { display: grid; grid-template-columns: auto 1fr; gap: 0.15rem 0.7rem; margin: 0.5rem 0 0; }
  dt { color: var(--muted); }
  dd { margin: 0; }
</style>
