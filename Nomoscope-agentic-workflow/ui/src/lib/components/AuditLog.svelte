<script>
  let { decisions = [] } = $props();
</script>

<section class="panel log">
  <h2>
    Audit log
    <span class="muted">({decisions.length} decisions — this log is future training/validation data)</span>
  </h2>
  <div class="scroll">
    <table>
      <thead>
        <tr>
          <th>When</th><th>Parameter</th><th>as of</th><th>Routing</th>
          <th>Action</th><th>Reviewer</th><th>Conf.</th><th>Critique</th><th>Note</th>
        </tr>
      </thead>
      <tbody>
        {#each decisions as d}
          <tr>
            <td class="mono">{d.logged_at}</td>
            <td class="mono">{d.model_target}</td>
            <td>{d.as_of}</td>
            <td><span class="badge {d.routing}">{d.routing}</span></td>
            <td><span class="badge {d.action}">{d.action}</span></td>
            <td>{d.reviewer}</td>
            <td>{d.confidence ?? '—'}</td>
            <td>{d.critique_verdict ?? '—'}</td>
            <td>{d.note ?? ''}</td>
          </tr>
        {:else}
          <tr><td colspan="9" class="muted">No decisions logged yet.</td></tr>
        {/each}
      </tbody>
    </table>
  </div>
</section>

<style>
  .log { display: flex; flex-direction: column; min-height: 0; }
  .scroll { overflow: auto; flex: 1; }
</style>
