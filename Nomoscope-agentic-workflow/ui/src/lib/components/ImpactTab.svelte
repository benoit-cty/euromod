<script>
  // Environmental impact of traced LLM calls: EcoLogits estimates computed by
  // the pipeline CLI over Phoenix spans (see nomoscope_workflow/impact.py).
  // Impacts are min–max ranges: proprietary model architectures are estimated.
  import { api } from '../api.js';

  let { dbUrl = '' } = $props();

  let report = $state(null);
  let projects = $state([]);
  let project = $state('');
  let zone = $state('EEE');
  let loading = $state(false);
  let error = $state('');
  let loadedOnce = $state(false);

  const zones = [
    { value: 'EEE', label: 'Europe (EEE)' },
    { value: 'WOR', label: 'World (WOR)' },
    { value: 'FRA', label: 'France (FRA)' },
  ];

  $effect(() => {
    if (dbUrl && !loadedOnce) {
      loadedOnce = true;
      loadProjects();
      load();
    }
  });

  async function loadProjects() {
    try {
      const res = await api.phoenixProjects(dbUrl);
      projects = res.projects ?? [];
    } catch {
      projects = []; // phoenix DB absent: the filter just stays empty
    }
  }

  async function load() {
    loading = true;
    error = '';
    try {
      report = await api.impactReport(dbUrl, project, zone);
    } catch (e) {
      error = String(e);
      report = null;
    } finally {
      loading = false;
    }
  }

  // Target of the shell's Reload button while this tab is showing.
  export async function reload() {
    await loadProjects();
    await load();
  }

  const fmt = (n, digits = 2) =>
    n == null ? '—' : Number(n).toLocaleString('en-US', { maximumFractionDigits: digits });

  // Energy in Wh below 1 kWh, else kWh; emissions in gCO2eq below 1 kg, else kg.
  const energyRange = (minKwh, maxKwh) =>
    maxKwh < 1
      ? `${fmt(minKwh * 1000)}–${fmt(maxKwh * 1000)} Wh`
      : `${fmt(minKwh, 3)}–${fmt(maxKwh, 3)} kWh`;
  const gwpRange = (minKg, maxKg) =>
    maxKg < 1
      ? `${fmt(minKg * 1000)}–${fmt(maxKg * 1000)} gCO₂eq`
      : `${fmt(minKg, 3)}–${fmt(maxKg, 3)} kgCO₂eq`;

  const mid = (lo, hi) => (lo + hi) / 2;
  // Illustrative orders of magnitude: ~12 Wh per smartphone full charge,
  // ~192 gCO2eq per km for an average petrol car.
  const phoneCharges = $derived(
    report ? mid(report.energy_kwh_min, report.energy_kwh_max) / 0.012 : 0
  );
  const carMeters = $derived(
    report ? (mid(report.gwp_kgco2eq_min, report.gwp_kgco2eq_max) / 0.192) * 1000 : 0
  );
</script>

<section class="panel impact">
  <div class="row">
    <label>
      Phoenix project
      <select bind:value={project} onchange={load}>
        <option value="">All projects</option>
        {#each projects as p}
          <option value={p.name}>{p.name}</option>
        {/each}
      </select>
    </label>
    <label>
      Electricity mix
      <select bind:value={zone} onchange={load}>
        {#each zones as z}
          <option value={z.value}>{z.label}</option>
        {/each}
      </select>
    </label>
    <button onclick={load} disabled={loading}>{loading ? 'Computing…' : 'Refresh'}</button>
  </div>

  {#if error}<p class="error">{error}</p>{/if}

  {#if report}
    {#if report.models.length === 0}
      <p class="muted">
        No LLM spans with token counts found — only real (non-mock) runs traced to Phoenix
        appear here.
      </p>
    {:else}
      <h2>Estimated impact of traced LLM calls</h2>
      <div class="cards">
        <div class="card">
          <div class="num">{fmt(report.total_calls, 0)}</div>
          <div class="muted">LLM calls</div>
        </div>
        <div class="card">
          <div class="num">{fmt(report.total_output_tokens, 0)}</div>
          <div class="muted">output tokens</div>
        </div>
        <div class="card">
          <div class="num">{energyRange(report.energy_kwh_min, report.energy_kwh_max)}</div>
          <div class="muted">energy</div>
        </div>
        <div class="card">
          <div class="num">{gwpRange(report.gwp_kgco2eq_min, report.gwp_kgco2eq_max)}</div>
          <div class="muted">emissions (GWP)</div>
        </div>
      </div>
      <p class="muted">
        ≈ {fmt(phoneCharges, 1)} smartphone charges · ≈ {fmt(carMeters, 0)} m driven in an
        average petrol car (midpoint estimates)
      </p>

      <h3>By model</h3>
      <table>
        <thead>
          <tr>
            <th>Model</th>
            <th>Provider</th>
            <th class="right">Calls</th>
            <th class="right">Prompt tok</th>
            <th class="right">Output tok</th>
            <th class="right">Energy</th>
            <th class="right">Emissions</th>
          </tr>
        </thead>
        <tbody>
          {#each report.models as m}
            <tr>
              <td class="mono">{m.model}</td>
              <td>{m.provider}</td>
              <td class="right">{fmt(m.calls, 0)}</td>
              <td class="right">{fmt(m.prompt_tokens, 0)}</td>
              <td class="right">{fmt(m.output_tokens, 0)}</td>
              {#if m.estimated}
                <td class="right">{energyRange(m.energy_kwh_min, m.energy_kwh_max)}</td>
                <td class="right">{gwpRange(m.gwp_kgco2eq_min, m.gwp_kgco2eq_max)}</td>
              {:else}
                <td class="right" colspan="2">
                  <span class="badge pending" title="model missing from the EcoLogits registry">
                    not in EcoLogits registry
                  </span>
                </td>
              {/if}
            </tr>
          {/each}
        </tbody>
      </table>

      <p class="muted footnote">
        Estimated with <a href="https://ecologits.ai" target="_blank" rel="noreferrer">EcoLogits</a>
        from Phoenix-traced token counts (electricity mix: {report.electricity_mix_zone}).
        Ranges reflect uncertainty about proprietary model architectures; energy scales with
        output tokens, so prompt tokens are shown for context only. Totals cover estimated
        models{#if report.not_estimated.length}; excluded: {report.not_estimated.join(', ')}{/if}.
      </p>
    {/if}
  {:else if loading}
    <p class="muted">Computing impact report…</p>
  {/if}
</section>

<style>
  .impact { overflow: auto; display: flex; flex-direction: column; gap: 0.8rem; min-height: 0; }
  .row { display: flex; gap: 0.5rem; align-items: end; flex-wrap: wrap; }
  label { display: flex; flex-direction: column; gap: 0.25rem; color: var(--muted); }
  .error { color: var(--err); }
  .cards { display: flex; gap: 0.6rem; flex-wrap: wrap; }
  .card {
    background: var(--panel-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    min-width: 7.5rem;
  }
  .num { font-size: 1.4rem; font-weight: 700; }
  .right { text-align: right; }
  .footnote { max-width: 60rem; }
  .footnote a { color: var(--accent); }
</style>
