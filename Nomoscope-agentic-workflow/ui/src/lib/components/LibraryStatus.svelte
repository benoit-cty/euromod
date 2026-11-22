<script>
  // Legislation › Library status: per country, how much of the library is
  // there and usable (searchable, available in English), and — folded further
  // — the technical statistics and the database the app reads.
  import { library } from '../library.svelte.js';
  import { countryName } from '@shared/lib/labels.js';
  import { formatCount } from '@shared/lib/format.js';
  import { countryReadiness } from '../readiness.js';
  import DbUrlField from './DbUrlField.svelte';

  // dbUrl: the app's database, password masked; onchangedb switches the whole app.
  let { dbUrl = '', onchangedb } = $props();

  // The library statistics are shared with the other pages (library.svelte.js).
  const stats = $derived(library.stats);
  const loading = $derived(library.loading);
  let error = $state('');

  // Per-country one-liners for the collapsed library summary.
  const countryRows = $derived.by(() => {
    if (!stats) return [];
    const inputs = new Map((stats.model_inputs?.by_country ?? []).map((r) => [r.code, r]));
    return stats.by_country.map((row) => ({ row, ...countryReadiness(row, inputs.get(row.code)) }));
  });
  const readyCount = $derived(countryRows.filter((c) => c.level === 'ready').length);

  /** Read the statistics (again, when `force`d: the shell's Refresh). */
  export async function loadStats(force = true) {
    error = '';
    await library.load(force);
    error = library.error;
  }

  loadStats(false);
</script>

{#if error}<p class="callout err">{error}</p>{/if}
<details class="more">
  <summary>
    Library status
    <span class="hint">
      {#if stats}
        {formatCount(stats.totals.instruments)} laws and texts · {readyCount} of {countryRows.length} countries fully ready
      {:else if loading}
        loading…
      {/if}
    </span>
  </summary>
  <div class="body">
    {#if stats}
      <table class="summary-table">
        <thead>
          <tr>
            <th>Country</th><th>Laws and texts</th><th>Searchable</th><th>Available in English</th><th>Status</th>
          </tr>
        </thead>
        <tbody>
          {#each countryRows as c (c.row.code)}
            <tr>
              <td><strong>{countryName(c.row.code)}</strong></td>
              <td>{formatCount(c.row.instruments)}</td>
              <td>{c.embeddedPct == null ? '—' : `${c.embeddedPct}%`}</td>
              <td>{c.englishPct == null ? '—' : `${c.englishPct}%`}</td>
              <td>
                {#if c.level === 'ready'}<span class="badge pass">Ready</span>
                {:else}<span
                    class="badge {c.level === 'partial' ? 'changed' : 'pending'}"
                    title={c.problems.join('; ')}
                  >
                    {c.problems[0]}
                  </span>{/if}
              </td>
            </tr>
          {/each}
        </tbody>
      </table>

      <details class="more nested">
        <summary>Technical statistics <span class="hint">for the people maintaining the library</span></summary>
        <div class="body">
          <DbUrlField {dbUrl} {onchangedb} />
          <div>
            <button onclick={loadStats} disabled={loading}>{loading ? 'Loading…' : 'Reload statistics'}</button>
          </div>
          <div class="stats">
            {#each Object.entries(stats.totals) as [key, count]}
              <div class="stat">
                <div class="num">{formatCount(count)}</div>
                <div class="muted">{key.replaceAll('_', ' ')}</div>
              </div>
            {/each}
          </div>

          <div class="tables">
            <div>
              <h3>By jurisdiction</h3>
              <table>
                <thead>
                  <tr>
                    <th>Code</th><th>Instr.</th><th>Units</th><th>Versions</th><th>In force</th><th>Texts</th><th>
                      Chunks
                    </th><th>Embedded</th>
                  </tr>
                </thead>
                <tbody>
                  {#each stats.by_country as row}
                    <tr>
                      <td><strong>{row.code}</strong></td>
                      <td>{row.instruments}</td>
                      <td>{row.legal_units}</td>
                      <td>{row.versions}</td>
                      <td>{row.in_force}</td>
                      <td>{row.texts}</td>
                      <td>{row.chunks}</td>
                      <td>{row.embedded_chunks}</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
            <div>
              <h3>Translation status</h3>
              <table>
                <thead>
                  <tr><th>Code</th><th>Authentic</th><th>Official transl.</th><th>Machine transl.</th></tr>
                </thead>
                <tbody>
                  {#each stats.by_country as row}
                    <tr>
                      <td><strong>{row.code}</strong></td>
                      <td>{row.authentic}</td>
                      <td>{row.official_translation}</td>
                      <td>{row.machine_translation}</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
            <div class="wide">
              <h3>Model inputs</h3>
              <p class="muted note">
                The two non-legislative inputs each country needs: its EUROMOD Country Report (context for framing and
                display, never cited as evidence) and the enriched parameter store loaded by <code>ingest-params</code>.
              </p>
              <table>
                <thead>
                  <tr>
                    <th>Code</th>
                    <th>Country Report</th><th>CR chunks</th><th>CR embedded</th><th>CR loaded</th>
                    <th>Enriched parameters</th><th>Values</th><th>Income-year</th><th>Params loaded</th>
                  </tr>
                </thead>
                <tbody>
                  {#each stats.model_inputs.by_country as row}
                    {@const cr = row.country_report}
                    {@const p = row.parameters}
                    <tr>
                      <td><strong>{row.code}</strong></td>
                      <td>
                        {#if cr && cr.reports > 0}
                          <span class="badge pass" title={cr.ids ?? ''}>{cr.ids ?? 'loaded'}</span>
                        {:else}
                          <span class="badge pending">missing</span>
                        {/if}
                      </td>
                      <td>{cr?.chunks ?? 0}</td>
                      <td>{cr?.embedded_chunks ?? '—'}</td>
                      <td class="muted">{cr?.ingested_on ?? '—'}</td>
                      <td>
                        {#if p}
                          <span class="badge pass" title={p.source_files ?? ''}>{p.parameters}</span>
                        {:else if !stats.model_inputs.params_schema}
                          <span class="badge pending">no params schema</span>
                        {:else}
                          <span class="badge pending">missing</span>
                        {/if}
                      </td>
                      <td>{p?.model_values ?? '—'}</td>
                      <td>{p ? p.income_year : '—'}</td>
                      <td class="muted">{p?.ingested_on ?? '—'}</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
              {#if !stats.model_inputs.params_schema}
                <p class="muted note">
                  The <code>params</code> schema does not exist in this database — run
                  <code>nomoscope-workflow init-param-db</code>, then <code>ingest-params</code>.
                </p>
              {/if}
            </div>
            <div>
              <h3>Embedding models</h3>
              <table>
                <thead>
                  <tr><th>Id</th><th>Name</th><th>Provider</th><th>Dim</th><th>Default</th><th>Embedded chunks</th></tr>
                </thead>
                <tbody>
                  {#each stats.embedding_models as m}
                    <tr>
                      <td>{m.id}</td>
                      <td>{m.name}</td>
                      <td>{m.provider ?? '—'}</td>
                      <td>{m.stored_dim}</td>
                      <td>{m.is_default ? '✓' : ''}</td>
                      <td>{m.embedded_chunks}</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </details>
    {:else if !loading}
      <DbUrlField {dbUrl} {onchangedb} />
      <div><button onclick={loadStats}>Load statistics</button></div>
    {/if}
  </div>
</details>

<style>
  .summary-table td,
  .summary-table th {
    padding: 0.45rem 0.6rem;
  }
  .nested {
    margin-top: 0.4rem;
  }
  .tables {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    align-items: start;
  }
  .tables .wide {
    grid-column: 1 / -1;
  }
  .note {
    margin: 0 0 0.4rem;
    font-size: 0.82rem;
  }
  @media (max-width: 1100px) {
    .tables {
      grid-template-columns: 1fr;
    }
  }
</style>
